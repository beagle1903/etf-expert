"""Compare and screen the saved issuer-reviewed ETF cohort without network access."""

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote, urlsplit


FEE_METRICS = (
    "expense_ratio", "gross_expense_ratio", "net_expense_ratio",
    "total_annual_fund_operating_expenses", "ter",
)
IDENTIFIERS = {"CUSIP": r"[0-9A-Z]{9}", "ISIN": r"[A-Z]{2}[0-9A-Z]{9}[0-9]"}
VENUE_NAMES = {"Q": "Nasdaq", "P": "NYSE Arca", "Z": "Cboe BZX", "XETR": "Xetra"}


@dataclass(frozen=True)
class Filters:
    as_of: date
    max_age_days: int = 180
    market: str | None = None
    strategy: str | None = None
    currency: str | None = None
    excluded_symbols: tuple[str, ...] = ()
    fee_caps: dict[str, Decimal] = field(default_factory=dict)
    max_duration: Decimal | None = None
    max_below_ig: Decimal | None = None
    hedged_to: str | None = None


def decimal(value):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    return result if result.is_finite() else None


def observation_date(value):
    try:
        parsed = date.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed.isoformat() == value else None


def date_problem(value, filters):
    observed = observation_date(value)
    if observed is None:
        return "missing or invalid observation date"
    age = (filters.as_of - observed).days
    if age < 0:
        return "observation postdates the comparison date"
    if age > filters.max_age_days:
        return f"observation is {age} days old (limit {filters.max_age_days})"
    return None


def conflict(record, name):
    return name in (record.get("conflicts") or ())


def source_url(source):
    url = source.get("url") if isinstance(source, dict) else None
    if isinstance(url, str):
        try:
            target = urlsplit(url)
        except ValueError:
            return None
        if target.scheme in ("http", "https") and target.netloc:
            return url
    return None


def fee_amount(claim):
    amount = decimal(claim.get("annual_basis_points"))
    if amount is None or amount < 0:
        return None
    if "raw_percent" in claim:
        percent = decimal(claim["raw_percent"])
        if percent is None or percent * 100 != amount:
            return None
    return amount


def fee_evidence(record, metric, filters):
    if conflict(record, "fee") or conflict(record, metric):
        return None, "conflicting fee evidence"
    claims = [claim for claim in record.get("annual_fees") or () if claim.get("metric") == metric]
    if not claims:
        return None, "requested fee metric missing"
    dated = [(observation_date(claim.get("as_of")), fee_amount(claim), claim) for claim in claims]
    eligible = [(observed, amount, claim) for observed, amount, claim in dated
                if observed is not None and observed <= filters.as_of]
    if not eligible:
        return None, "no fee observation dated on or before comparison date"
    latest = max(observed for observed, _, _ in eligible)
    peers = [(amount, claim) for observed, amount, claim in eligible if observed == latest]
    amounts = {amount for amount, _ in peers}
    if None in amounts:
        return None, "invalid fee amount or unit conversion"
    if len(amounts) != 1:
        return None, "conflicting fee amounts on the same date"
    amount = peers[0][0]
    if any(observed is None and other != amount for observed, other, _ in dated):
        return None, "conflicting or invalid undated fee claim"
    if problem := date_problem(latest.isoformat(), filters):
        return None, problem
    if not any(source_url(claim.get("source") or record.get("fee_and_exposure_source")) for _, claim in peers):
        return None, "fee source missing"
    return amount, None


def share_class(record):
    identifier = record.get("identifier") or {}
    kind, value = identifier.get("type"), identifier.get("value")
    if (not conflict(record, "identifier") and kind in IDENTIFIERS
            and isinstance(value, str) and re.fullmatch(IDENTIFIERS[kind], value)
            and record["listing"].get("venue") and source_url(record.get("listing_source"))
            and source_url(record.get("fee_and_exposure_source"))):
        return f"{kind}:{value}"
    return None


def credit_bucket(label):
    label = " ".join(label.upper().replace("−", "-").split())
    if label in {"CASH", "CASH AND/OR DERIVATIVES", "CASH AND DERIVATIVES"}:
        return "cash"
    if label == "AAA OR ABOVE":
        return "investment_grade"
    rating = label.removesuffix(" RATED")
    if re.fullmatch(r"AAA|AA[+-]?|A[+-]?|BBB[+-]?", rating):
        return "investment_grade"
    if re.fullmatch(r"BB[+-]?|B[+-]?|CCC[+-]?|CC|C|D", rating):
        return "below"
    return "unknown"


def credit_bounds(weights):
    if not isinstance(weights, dict) or not weights:
        return None
    totals = Counter()
    for label, raw in weights.items():
        amount = decimal(raw)
        bucket = credit_bucket(label)
        if amount is None or amount > 100 or (amount < 0 and bucket != "cash"):
            return None
        totals[bucket] += amount
    total = sum(totals.values())
    if total <= 0 or total > Decimal("100.10"):
        return None
    below = totals["below"]
    unknown = totals["unknown"] + max(0, 100 - total)
    return below, max(below, min(100, below + unknown))


def bond_evidence(record, filters):
    risk = record.get("bond_risk") or {}
    duration = decimal(risk.get("duration_years"))
    bounds = credit_bounds(risk.get("credit_weights_percent"))
    duration_problem = date_problem(risk.get("duration_as_of"), filters)
    credit_problem = date_problem(risk.get("credit_as_of"), filters)
    if conflict(record, "duration"):
        duration_problem = "conflicting duration evidence"
    elif risk.get("duration_method") != "effective" or duration is None:
        duration_problem = "effective duration missing or invalid"
    if conflict(record, "credit"):
        credit_problem = "conflicting credit evidence"
    elif bounds is None:
        credit_problem = "credit weights missing or invalid"
    if not source_url(risk.get("source")):
        duration_problem = duration_problem or "duration source missing"
        credit_problem = credit_problem or "credit source missing"
    return duration, bounds, duration_problem, credit_problem


def assess(record, filters):
    listing = record["listing"]
    symbol, market, venue = listing["symbol"], listing["market"], listing.get("venue")
    strategy = listing.get("strategy")
    currency = record.get("trading_currency")
    excluded, failures, unknown, passed = [], [], [], []
    gaps = []
    identifier = share_class(record)
    if not identifier:
        gaps.append("share-class identifier missing, unsourced or conflicting")
    if (not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency)
            or not source_url(record.get("listing_source")) or conflict(record, "trading_currency")):
        gaps.append("trading currency missing, unsourced or conflicting")
        currency = None
    exposure = record.get("exposure")
    if (not isinstance(exposure, str) or not exposure.strip() or conflict(record, "exposure")
            or not source_url(record.get("fee_and_exposure_source"))):
        gaps.append("issuer exposure evidence missing or conflicting")
    if strategy not in ("equity", "bond") or not venue:
        gaps.append("venue or asset class unresolved")
    fees = {metric: fee_evidence(record, metric, filters) for metric in FEE_METRICS}
    if all(amount is None for amount, _ in fees.values()):
        observed = [metric for metric in FEE_METRICS if any(
            claim.get("metric") == metric for claim in record.get("annual_fees") or ()
        )]
        detail = ", ".join(f"{metric} · {fees[metric][1]}" for metric in observed)
        gaps.append("no usable annual fee" + (f" ({detail})" if detail else ""))
    unknown.extend(gaps)

    if filters.market and market != filters.market:
        excluded.append(f"outside market {filters.market}")
    if filters.strategy and strategy in ("equity", "bond") and strategy != filters.strategy:
        excluded.append(f"outside strategy {filters.strategy}")
    if filters.currency and currency and currency != filters.currency:
        excluded.append(f"trades in {currency}, outside currency {filters.currency}")
    if symbol.upper() in filters.excluded_symbols:
        excluded.append("symbol explicitly excluded")

    if filters.fee_caps:
        fee_passes, fee_failures, fee_unknowns = [], [], []
        for metric, cap in sorted(filters.fee_caps.items()):
            amount, problem = fees[metric]
            if problem:
                fee_unknowns.append(f"{metric} · {problem}")
            elif amount > cap:
                fee_failures.append(f"{metric} {amount} bp exceeds {cap} bp")
            else:
                fee_passes.append(f"{metric} {amount} bp at or below {cap} bp")
        if fee_passes:
            passed.extend(fee_passes)
        elif fee_unknowns:
            unknown.extend(fee_unknowns)
        else:
            failures.extend(fee_failures)

    bounds = None
    if strategy == "bond":
        duration, bounds, duration_problem, credit_problem = bond_evidence(record, filters)
        for problem in (duration_problem, credit_problem):
            if problem:
                gaps.append(problem)
                unknown.append(problem)
        if filters.max_duration is not None and not duration_problem:
            detail = f"effective duration {duration} years"
            if duration > filters.max_duration:
                failures.append(f"{detail} exceeds {filters.max_duration} years")
            else:
                passed.append(f"{detail} at or below {filters.max_duration} years")
        if filters.max_below_ig is not None and not credit_problem:
            low, high = bounds
            cap = filters.max_below_ig
            if low > cap:
                failures.append(f"known below-investment-grade weight {low}% exceeds {cap}%")
            elif high > cap:
                unknown.append(f"below-investment-grade range {low}% to {high}% straddles {cap}%")
            else:
                passed.append(f"below-investment-grade upper bound {high}% at or below {cap}%")
        if filters.hedged_to:
            hedge = record.get("currency_hedge") or {}
            target = hedge.get("target")
            if (conflict(record, "currency_hedge") or not isinstance(target, str)
                    or not (target == "unhedged" or re.fullmatch(r"[A-Z]{3}", target))
                    or not source_url(hedge.get("source"))):
                unknown.append("bond hedge target missing, unsourced or conflicting")
            elif problem := date_problem(hedge.get("as_of"), filters):
                unknown.append(f"bond hedge target · {problem}")
            elif target != filters.hedged_to:
                failures.append(f"reported bond hedge is {target}, required {filters.hedged_to}")
            else:
                passed.append(f"reported bond hedge matches {target}")

    status = "failed" if excluded or failures else "unknown" if unknown else "passed"
    reasons = excluded + failures + unknown + passed
    return {
        "record": record, "status": status, "comparison_ready": not gaps, "excluded": bool(excluded),
        "identity": identifier, "credit_range": bounds, "reasons": reasons or ["required evidence present"],
    }


def compare(records, filters):
    by_listing = {}
    for record in records:
        listing = record["listing"]
        key = listing["market"], listing.get("venue") or "", listing["symbol"]
        if key in by_listing:
            raise ValueError("Snapshot contains duplicate market/venue/symbol keys")
        by_listing[key] = record
    return [assess(by_listing[key], filters) for key in sorted(by_listing)]


def cell(value):
    if value is None or value == "":
        return "—"
    return " ".join(str(value).split()).replace("|", r"\|")


def source_links(record):
    sources = [
        ("listing", record.get("listing_source")),
        ("fee / exposure", record.get("fee_and_exposure_source")),
        ("bond risk", (record.get("bond_risk") or {}).get("source")),
        ("hedge", (record.get("currency_hedge") or {}).get("source")),
    ]
    sources.extend(("fee claim", fee.get("source")) for fee in record.get("annual_fees") or ())
    result = {}
    for label, source in sources:
        if url := source_url(source):
            result.setdefault(url, []).append(label)
    return ", ".join(f"[{' / '.join(dict.fromkeys(labels))}]({quote(url, safe=':/?&=#%+@$,;~!*')})"
                     for url, labels in result.items()) or "—"


def summary(rows):
    statuses = Counter(row["status"] for row in rows)
    return {
        "input": len(rows), "comparison-ready": sum(row["comparison_ready"] for row in rows),
        "passed": statuses["passed"], "failed": statuses["failed"], "unknown": statuses["unknown"],
        "explicit exclusions within failed": sum(row["excluded"] for row in rows),
    }


def report(rows, filters):
    lines = ["# ETF comparison and screening", "", f"Comparison date {filters.as_of}. "
             f"Maximum observation age {filters.max_age_days} calendar days.", ""]
    for key, value in summary(rows).items():
        lines.append(f"- **{key.capitalize()}** {value}")
    rules = [
        ("Market", filters.market), ("Strategy", filters.strategy), ("Trading currency", filters.currency),
        ("Excluded symbols", ", ".join(sorted(filters.excluded_symbols))),
        ("Fee caps (annual bp)", ", ".join(f"{m} at most {cap}" for m, cap in sorted(filters.fee_caps.items()))),
        ("Bond duration cap (years)", filters.max_duration),
        ("Bond below-investment-grade cap (%)", filters.max_below_ig),
        ("Bond hedge", filters.hedged_to),
    ]
    lines += ["", "## Applied filters", ""]
    lines += [f"- {label} {value}" for label, value in rules if value is not None and value != ""]
    if lines[-1] == "":
        lines.append("Required evidence and freshness only.")
    lines += ["", "## Listings", "",
              "| Listing | Strategy | Class ID | Trade currency | Class currency | Fund base currency | Annual fees (bp and date) | Benchmark or strategy | Effective duration (years and date) | Below-IG range (% and credit date) | Hedge | Outcome and reasons | Sources |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]

    classes, exposures = defaultdict(list), defaultdict(list)
    exposure_names = {}
    for row in rows:
        r = row["record"]
        listing = r["listing"]
        venue = listing.get("venue") or "unresolved venue"
        label = f"{listing['symbol']} · {VENUE_NAMES.get(venue, venue)}"
        if row["identity"]:
            classes[row["identity"]].append(label)
        exposure = r.get("exposure")
        if isinstance(exposure, str) and exposure.strip() and not conflict(r, "exposure") and source_url(r.get("fee_and_exposure_source")):
            key = " ".join(exposure.casefold().split())
            exposures[key].append(label)
            exposure_names.setdefault(key, exposure)
        fees = ", ".join(f"{f.get('metric')} {f.get('annual_basis_points', '—')} · {f.get('as_of') or 'undated'}"
                         for f in r.get("annual_fees") or ())
        risk = r.get("bond_risk") or {}
        bounds = row["credit_range"]
        credit = f"{bounds[0]} to {bounds[1]} · {risk.get('credit_as_of') or 'undated'}" if bounds else None
        duration = risk.get("duration_years")
        hedge = r.get("currency_hedge") or {}
        values = (
            label, listing.get("strategy"), row["identity"], r.get("trading_currency"),
            r.get("share_class_currency"), r.get("fund_base_currency"), fees, exposure,
            f"{duration} · {risk.get('duration_as_of') or 'undated'}" if duration is not None else None,
            credit, f"{hedge['target']} · {hedge.get('as_of') or 'undated'}" if hedge.get("target") else None,
            f"{row['status']} · " + ". ".join(row["reasons"]),
        )
        lines.append("| " + " | ".join([*map(cell, values), source_links(r)]) + " |")

    for title, groups in (("Supported cross-listings of a share class", classes), ("Matching exposure labels", exposures)):
        lines += ["", f"## {title}", ""]
        matches = [f"- {cell(exposure_names.get(key, key))} · {', '.join(map(cell, group))}"
                   for key, group in sorted(groups.items()) if len(group) > 1]
        lines.extend(matches or ["None identified in the supplied evidence."])
    lines += ["", "Matching exposure labels alone give no estimate of holdings overlap. "
              "Bond credit ranges preserve disclosed weights and allow for unknown categories and residual exposure. "
              "Blank currency and hedge fields indicate missing evidence. "
              "Portfolio currency weights require separate source evidence.", ""]
    return "\n".join(lines)


def number_arg(value):
    amount = decimal(value)
    if amount is None or amount < 0:
        raise argparse.ArgumentTypeError("Expected a finite nonnegative number")
    return amount


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="Saved full-cohort manual-coverage.json")
    parser.add_argument("--as-of", required=True, help="Comparison date, YYYY-MM-DD")
    parser.add_argument("--max-age-days", type=int, default=180)
    parser.add_argument("--market", choices=("US", "EU"))
    parser.add_argument("--strategy", choices=("equity", "bond"))
    parser.add_argument("--currency", help="Listing trading currency")
    parser.add_argument("--exclude-symbol", action="append", default=[])
    parser.add_argument("--fee-cap", action="append", default=[], metavar="METRIC=BPS")
    parser.add_argument("--max-duration", type=number_arg, help="Effective duration cap in years for bonds")
    parser.add_argument("--max-below-ig", type=number_arg, help="Maximum below-investment-grade weight in percent for bonds")
    parser.add_argument("--hedged-to", help="Require a dated bond hedge target in this currency, or 'unhedged'")
    parser.add_argument("--output", type=Path, help="Save Markdown to this path. Default prints the report.")
    args = parser.parse_args()
    if args.output and args.output.resolve() == args.snapshot.resolve():
        parser.error("Choose a report path distinct from the input snapshot")
    as_of = observation_date(args.as_of)
    if as_of is None or args.max_age_days < 0:
        parser.error("Use a YYYY-MM-DD date and a nonnegative maximum age")
    if args.max_below_ig is not None and args.max_below_ig > 100:
        parser.error("Below-investment-grade cap must be between 0 and 100")
    currency = args.currency.upper() if args.currency else None
    hedge = args.hedged_to.upper() if args.hedged_to else None
    if hedge == "UNHEDGED":
        hedge = "unhedged"
    if any(not re.fullmatch(r"[A-Z]{3}", value) for value in (currency, hedge) if value and value != "unhedged"):
        parser.error("Use a three-letter currency code")
    fees = {}
    for cap in args.fee_cap:
        metric, _, value = cap.partition("=")
        if metric not in FEE_METRICS or metric in fees:
            parser.error("Fee caps must name a supported metric once: " + ", ".join(FEE_METRICS))
        try:
            fees[metric] = number_arg(value)
        except argparse.ArgumentTypeError as error:
            parser.error(str(error))
    filters = Filters(
        as_of=as_of, max_age_days=args.max_age_days, market=args.market, strategy=args.strategy,
        currency=currency, excluded_symbols=tuple(s.upper() for s in args.exclude_symbol), fee_caps=fees,
        max_duration=args.max_duration, max_below_ig=args.max_below_ig, hedged_to=hedge,
    )
    try:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        rows = compare(snapshot["records"], filters)
    except (OSError, AttributeError, TypeError, KeyError, ValueError) as error:
        parser.error(f"Could not read comparison snapshot: {error}")
    result = report(rows, filters)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
        print(args.output)
        print(json.dumps(summary(rows)))
    else:
        # Preserve readable output on Windows consoles and legacy-codepage pipes.
        print(result.encode(sys.stdout.encoding or "utf-8", errors="backslashreplace")
              .decode(sys.stdout.encoding or "utf-8"))


if __name__ == "__main__":
    main()
