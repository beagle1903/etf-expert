"""Convert an issuer replay and optional Yahoo snapshot into local ETF research records."""

import argparse
from collections import Counter
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from itertools import combinations
import json
from pathlib import Path
import re
from typing import Literal, NotRequired, TypedDict


class Claim(TypedDict):
    source: str
    field: str
    raw_value: str | int | float
    raw_unit: str | None
    as_of: str | None
    date_status: Literal["dated", "undated", "conflicting"]
    annual_basis_points: NotRequired[str]
    metric: NotRequired[str]
    raw_text: NotRequired[str]


class Field(TypedDict):
    status: Literal["missing", "unattributed", "reported", "review", "conflicting"]
    claims: list[Claim]
    issues: list[str]


class Record(TypedDict):
    symbol: str
    market: str
    research_intent: str
    listing: dict[str, Field]
    share_class: dict[str, Field]
    fund: dict[str, Field]
    exposure: dict[str, Field]
    identity: dict[str, str | None]
    sources: dict[str, dict]
    issuer_attempts: list[dict]
    source_coverage: dict


# Issuing company is a source claim about the umbrella/entity, never a fund ID.
ISSUER_FIELDS = {
    "listing": {"listing_currency": "trading_currency"},
    "share_class": {
        "identifier": "identifier", "share_currency": "currency", "fee": "fee",
        "share_assets": "net_assets", "hedging": "hedging", "distribution": "distribution",
    },
    "fund": {"legal_entity": "issuing_entity", "base_currency": "base_currency", "net_assets": "net_assets"},
    "exposure": {
        "benchmark": "benchmark", "benchmark_ticker": "benchmark_ticker", "composition": "composition",
        "duration": "duration", "maturity": "maturity", "yield": "yield", "credit_quality": "credit_quality",
    },
}
YAHOO_FIELDS = {
    "listing": {"name": "name", "exchange": "venue", "trading_currency": "trading_currency", "quote_type": "quote_type"},
    "share_class": {"isin": "identifier", "expense_ratio_raw": "fee"},
    "fund": {},
    "exposure": {"benchmark": "benchmark", "category": "category"},
}
FEE_METRICS = {
    "ongoing charges figure": "ocf",
    "total expense ratio": "ter",
    "gross expense ratio": "gross_expense_ratio",
    "expense ratio": "expense_ratio",
}


def claim(source, label, value, unit=None, as_of=None, date_status=None) -> Claim:
    if as_of is not None and date.fromisoformat(as_of).isoformat() != as_of:
        raise ValueError(f"Expected ISO observation date for {source} {label}: {as_of}")
    return {
        "source": source, "field": label, "raw_value": value, "raw_unit": unit,
        "as_of": as_of, "date_status": date_status or ("dated" if as_of else "undated"),
    }


def issuer_claim(source, label, fact) -> Claim:
    unit = fact["unit"]
    result = claim(source, label, fact["value"], unit, fact["as_of"], fact.get("date_status"))
    if label != "fee" or not unit or not unit.startswith("percent per year; "):
        return result
    source_label = unit.removeprefix("percent per year; ")
    result["field"] = source_label
    if "raw_text" in fact:
        result["raw_text"] = fact["raw_text"]
    for prefix, metric in FEE_METRICS.items():
        if source_label.casefold().startswith(prefix):
            result["metric"] = metric
            break
    try:
        value = Decimal(str(fact["value"]))
    except InvalidOperation:
        return result
    if value.is_finite() and value >= 0:
        result["annual_basis_points"] = format(value * 100, "f")
    return result


def comparable(name, observation):
    if name == "fee":
        if "metric" in observation and "annual_basis_points" in observation:
            return observation["metric"], Decimal(observation["annual_basis_points"])
        return None
    if name == "identifier":
        value = observation["raw_value"]
        scheme = observation["raw_unit"]
        pattern = {"ISIN": r"[A-Z]{2}[A-Z0-9]{9}[0-9]", "CUSIP": r"[A-Z0-9]{9}"}.get(scheme)
        if pattern and isinstance(value, str) and re.fullmatch(pattern, value):
            return scheme, value
        return None
    if name in ("trading_currency", "currency", "base_currency", "benchmark", "hedging"):
        return name, str(observation["raw_value"]).strip().casefold()
    return None


def field(name, claims, sources) -> Field:
    attributed = [c for c in claims if sources[c["source"]]["listing_match"] != "unresolved"]
    values = [(c, comparable(name, c)) for c in attributed]
    issues = []
    if any(c["date_status"] == "conflicting" for c in claims):
        issues.append("conflicting_source_dates")
    for (a, left), (b, right) in combinations(values, 2):
        if left and right and left[0] == right[0] and left[1] != right[1]:
            if name == "identifier" or a["as_of"] == b["as_of"] or None in (a["as_of"], b["as_of"]):
                issues.append("different_values")
                break
    if name == "fee":
        issuer = [c["raw_value"] for c in attributed if "annual_basis_points" in c]
        yahoo = [c["raw_value"] for c in attributed if c["field"] in ("netExpenseRatio", "annualReportExpenseRatio")]
        if any(i != y for i in issuer for y in yahoo):
            issues.append("different_raw_fee_figures_with_unverified_units_or_basis")
    status = "missing"
    if claims:
        status = "reported" if attributed else "unattributed"
    if issues:
        status = "review" if issues == ["different_raw_fee_figures_with_unverified_units_or_basis"] else "conflicting"
    return {"status": status, "claims": claims, "issues": issues}


def normalize(member, issuer, attempts, yahoo=None, yahoo_run=None) -> Record:
    sources = {}
    groups = {}
    for scope, fields in ISSUER_FIELDS.items():
        groups[scope] = {name: [] for name in (*fields.values(), *YAHOO_FIELDS[scope].values())}
    for row in issuer:
        source = f"issuer:{row['attempt_index']}"
        attempt = attempts[row["attempt_index"]]
        if attempt["symbol"] != member["symbol"]:
            raise ValueError("Issuer observation and attempt refer to different symbols")
        sources[source] = {
            "url": row["url"], "collected_at_utc": row["collected_at_utc"],
            "kind": attempt["kind"], "listing_match": row.get("listing_match", "unresolved"),
            "listing_evidence": row.get("listing_evidence"), "source_dates": row.get("source_dates", {}),
            "warnings": row.get("warnings", []), "header_excerpt": row.get("header"),
            "attempt_index": row["attempt_index"],
        }
        issuer_fields = {**row["fields"]}
        if row.get("listing_currency"):
            issuer_fields["listing_currency"] = {"value": row["listing_currency"], "unit": None, "as_of": None}
        for scope, mapping in ISSUER_FIELDS.items():
            for label, name in mapping.items():
                if fact := issuer_fields.get(label):
                    groups[scope][name].append(issuer_claim(source, label, fact))
    coverage = {"issuer_observations": len(issuer), "yahoo": None}
    if yahoo is not None:
        sources["yahoo"] = {
            "url": yahoo["source_url"], "collected_at_utc": yahoo["collected_at_utc"],
            "kind": "profile", "listing_match": "requested_provider_symbol",
            "run": yahoo_run, "raw_file": f"{member['symbol']}.json",
        }
        coverage["yahoo"] = {
            key: yahoo[key] for key in ("price_rows", "holdings_rows", "errors", "missing")
        }
        coverage["yahoo"]["assets_with_unverified_scope"] = yahoo["fields"].get("net_assets", {})
        for scope, mapping in YAHOO_FIELDS.items():
            for label, name in mapping.items():
                for raw_field, value in yahoo["fields"].get(label, {}).items():
                    unit = "ISIN" if raw_field == "isin" else None
                    groups[scope][name].append(claim("yahoo", raw_field, value, unit))
    sections = {
        scope: {name: field(name, claims, sources) for name, claims in fields.items()}
        for scope, fields in groups.items()
    }
    # The diagnostic found this exact name/ticker pair in the same VTI source.
    for row in issuer:
        facts = row["fields"]
        if (facts.get("benchmark") or {}).get("value") == "Morningstar US Total Market Index" and (
            facts.get("benchmark_ticker") or {}
        ).get("value") == "CRSPTMT":
            benchmark = sections["exposure"]["benchmark"]
            benchmark["status"] = "conflicting"
            benchmark["issues"].append("issuer_benchmark_name_and_ticker_disagree")
            break

    identifier = sections["share_class"]["identifier"]
    keys = {
        key for c in identifier["claims"]
        if sources[c["source"]]["listing_match"] == "exact_code" and (key := comparable("identifier", c))
    }
    share_key = None
    if identifier["status"] != "conflicting":
        for scheme in ("ISIN", "CUSIP"):
            candidates = [value for kind, value in keys if kind == scheme]
            if len(candidates) == 1:
                share_key = f"{scheme}:{candidates[0]}"
                break
    return {
        "symbol": member["symbol"], "market": member["market"], "research_intent": member["intent"],
        "listing": sections["listing"], "share_class": sections["share_class"],
        "fund": sections["fund"], "exposure": sections["exposure"],
        "identity": {
            "listing_to_share_class": "source_supported" if share_key else "unresolved",
            "share_class_key": share_key, "share_class_to_fund": "unresolved", "fund_key": None,
        },
        "sources": sources,
        "issuer_attempts": [
            {**a, "attempt_index": index} for index, a in enumerate(attempts) if a["symbol"] == member["symbol"]
        ],
        "source_coverage": coverage,
    }


def summarize(records: list[Record]) -> dict:
    counts = Counter()
    for record in records:
        counts["converted"] += 1
        statuses = {
            fact["status"]
            for scope in ISSUER_FIELDS
            for fact in record[scope].values()
        }
        for status in ("conflicting", "review"):
            counts[status] += status in statuses
        counts["unresolved_listing_to_share_class"] += record["identity"]["share_class_key"] is None
        counts["unresolved_share_class_to_fund"] += record["identity"]["fund_key"] is None
        counts["without_source_observations"] += not record["sources"]
    return dict(counts)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("issuer_assessment", type=Path, help="JSON produced by assess_issuers.py")
    parser.add_argument("--yahoo-run", type=Path, help="Optional saved Yahoo run folder with the same universe")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assessment = read_json(args.issuer_assessment)
    if "observations" not in assessment:
        parser.error("Replay the saved issuer runs with the current assess_issuers.py before normalizing")
    universe = [{k: row[k] for k in ("symbol", "market", "intent")} for row in assessment["rows"]]
    if args.yahoo_run and read_json(args.yahoo_run / "universe.json") != universe:
        parser.error("Issuer and Yahoo universe snapshots differ")
    records = []
    symbols = {row["symbol"] for row in universe}
    if len(symbols) != len(universe) or any(row["symbol"] not in symbols for row in assessment["observations"]):
        parser.error("Issuer assessment has duplicate members or observations outside the universe")
    for member in universe:
        symbol = member["symbol"]
        yahoo_path = args.yahoo_run / f"{symbol}.json" if args.yahoo_run else None
        yahoo = read_json(yahoo_path) if yahoo_path and yahoo_path.is_file() else None
        if yahoo and any(yahoo[k] != value for k, value in member.items()):
            parser.error(f"Yahoo record does not match requested member {symbol}")
        evidence = [row for row in assessment["observations"] if row["symbol"] == symbol]
        records.append(normalize(member, evidence, assessment["attempts"], yahoo,
                                 args.yahoo_run.name if args.yahoo_run else None))
    result = {"requested_listings": len(universe), "summary": summarize(records), "records": records}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"]))


if __name__ == "__main__":
    main()
