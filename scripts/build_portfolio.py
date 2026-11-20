"""Construct an illustrative portfolio from saved screened ETF evidence."""

import argparse
from collections import defaultdict
from dataclasses import dataclass, replace
from decimal import Decimal
import json
from pathlib import Path
import re

from screen_etfs import FEE_METRICS, Filters, assess, compare, decimal, fee_evidence, observation_date, source_url


BPS = 10_000


@dataclass(frozen=True)
class Allocation:
    strategy: str
    positions: int
    weight_bps: int
    fee_metric: str
    fee_cap_bps: Decimal | None
    max_duration_years: Decimal | None
    max_below_ig_pct: Decimal | None
    hedged_to: str | None


def validate_fields(value, allowed, name):
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    unknown = set(value) - set(allowed.split())
    if unknown:
        raise ValueError(f"Unknown {name} fields: {', '.join(sorted(unknown))}")


def amount(value, name, maximum=None):
    if value is None:
        return None
    parsed = decimal(value)
    if parsed is None or parsed < 0 or (maximum is not None and parsed > maximum):
        raise ValueError(f"Invalid {name}")
    return parsed


def cash_cents(value):
    match = re.fullmatch(r"(\d+)(?:\.(\d{1,2}))?", str(value), re.ASCII)
    if not match:
        raise ValueError("Cash must be nonnegative with at most two decimal places")
    return int(match[1]) * 100 + int((match[2] or "").ljust(2, "0"))


def validate_profile(profile):
    validate_fields(profile, "as_of market currency initial_cash recurring_cash excluded_symbols max_age_days allocations",
                    "profile")
    date = observation_date(profile.get("as_of"))
    age = profile.get("max_age_days", 180)
    market, currency = profile.get("market"), profile.get("currency")
    if not date or type(age) is not int or age < 0:
        raise ValueError("Use a YYYY-MM-DD comparison date and nonnegative integer evidence age")
    if market not in ("US", "EU") or currency not in ("USD", "EUR"):
        raise ValueError("Use a US or EU market and USD or EUR trading currency")
    exclusions = profile.get("excluded_symbols", [])
    if not isinstance(exclusions, list) or any(not isinstance(s, str) or not s.strip() for s in exclusions):
        raise ValueError("Excluded symbols must be a list of nonempty strings")
    allocations = {}
    raw_allocations = profile.get("allocations")
    if not isinstance(raw_allocations, list) or not raw_allocations:
        raise ValueError("Specify at least one allocation")
    for allocation in raw_allocations:
        validate_fields(allocation,
                        "strategy positions weight_bps fee_metric fee_cap_bps max_duration_years max_below_ig_pct hedged_to",
                        "allocation")
        strategy, metric = allocation.get("strategy"), allocation.get("fee_metric")
        positions, weight = allocation.get("positions"), allocation.get("weight_bps")
        if strategy not in ("equity", "bond") or strategy in allocations:
            raise ValueError("Specify each asset class at most once, using equity or bond")
        if metric not in FEE_METRICS:
            raise ValueError(f"Invalid {strategy} fee metric. Use one of {', '.join(FEE_METRICS)}")
        if type(positions) is not int or type(weight) is not int or not 1 <= positions <= weight <= BPS:
            raise ValueError(f"{strategy} needs integer positions and weight_bps, with 1 <= positions <= weight_bps")
        duration = amount(allocation.get("max_duration_years"), "duration cap")
        credit = amount(allocation.get("max_below_ig_pct"), "credit cap", maximum=100)
        hedge = allocation.get("hedged_to")
        if hedge is not None and (not isinstance(hedge, str)
                                  or not (hedge == "unhedged" or re.fullmatch(r"[A-Z]{3}", hedge))):
            raise ValueError("Hedge target must be a three-letter currency code or unhedged")
        if strategy == "equity" and any(value is not None for value in (duration, credit, hedge)):
            raise ValueError("Duration, credit and hedge limits apply to the bond allocation")
        allocations[strategy] = Allocation(
            strategy, positions, weight, metric, amount(allocation.get("fee_cap_bps"), "fee cap"), duration, credit, hedge
        )
    if sum(a.weight_bps for a in allocations.values()) != BPS:
        raise ValueError("Allocation weights must sum to 10,000 basis points")
    filters = Filters(date, age, market=market, currency=currency,
                      excluded_symbols=tuple(s.strip().upper() for s in exclusions))
    return filters, allocations, cash_cents(profile.get("initial_cash")), cash_cents(profile.get("recurring_cash"))


def candidate_key(candidate):
    return candidate["market"], candidate["venue"], candidate["symbol"]


def evidence_sources(record):
    risk = record.get("bond_risk") or {}
    hedge = record.get("currency_hedge") or {}
    sources = [
        record.get("listing_source"), record.get("fee_and_exposure_source"),
        risk.get("source"), hedge.get("source"),
    ]
    sources.extend(fee.get("source") for fee in record.get("annual_fees") or ())
    return list(dict.fromkeys(url for source in sources if (url := source_url(source))))


def candidates(records, filters, allocations):
    rows = []
    identity_labels = defaultdict(set)
    rules = {
        strategy: replace(
            filters, strategy=strategy,
            fee_caps={a.fee_metric: a.fee_cap_bps} if a.fee_cap_bps is not None else {},
            max_duration=a.max_duration_years, max_below_ig=a.max_below_ig_pct, hedged_to=a.hedged_to,
        )
        for strategy, a in allocations.items()
    }
    for base in compare(records, Filters(filters.as_of, filters.max_age_days)):
        record = base["record"]
        listing = record["listing"]
        strategy = listing.get("strategy")
        allocation = allocations.get(strategy)
        result = assess(record, rules[strategy]) if allocation else assess(record, filters)
        status, reasons = result["status"], result["reasons"].copy()
        if allocation is None and strategy in ("equity", "bond"):
            status, reasons = "failed", ["asset class has no profile allocation", *reasons]
        elif allocation is None:
            status = "unknown" if status != "failed" else status
            reasons.append("asset class is unresolved")
        fee = None
        if status == "passed":
            fee, problem = fee_evidence(record, allocation.fee_metric, rules[strategy])
            if problem:
                status = "unknown"
                reasons.append(f"{allocation.fee_metric} · {problem}")
        exposure = record.get("exposure") or ""
        label = " ".join(exposure.casefold().split()) if isinstance(exposure, str) else ""
        identity = result["identity"]
        if status == "passed":
            identity_labels[identity].add((strategy, label))
        risk = record.get("bond_risk") or {}
        credit_range = result["credit_range"]
        rows.append({
            "symbol": listing["symbol"], "market": listing["market"], "venue": listing.get("venue"),
            "strategy": strategy, "currency": record.get("trading_currency"),
            "identity": identity, "exposure": exposure, "exposure_key": label,
            "researched": bool(source_url(record.get("fee_and_exposure_source")) or source_url(risk.get("source"))),
            "comparison_ready": base["comparison_ready"], "screen_status": status, "reasons": reasons,
            "ranking_fee_bps": str(fee) if fee is not None else None,
            "ranking_fee_metric": allocation.fee_metric if allocation else None,
            "fee_observations": record.get("annual_fees") or [],
            "duration_years": risk.get("duration_years"), "duration_as_of": risk.get("duration_as_of"),
            "below_ig_range_percent": [str(bound) for bound in credit_range] if credit_range else None,
            "credit_as_of": risk.get("credit_as_of"),
            "sources": evidence_sources(record),
            "evidence": record,
        })
    for row in rows:
        if row["screen_status"] == "passed" and len(identity_labels[row["identity"]]) > 1:
            row["screen_status"] = "unknown"
            row["reasons"].append("same class has inconsistent exposure labels or asset classes")
    return rows


def select(rows, allocations):
    positions, blockers, capacity = [], [], {}
    for strategy, a in sorted(allocations.items()):
        pool = sorted(
            (row for row in rows if row["strategy"] == strategy and row["screen_status"] == "passed"),
            key=lambda row: (Decimal(row["ranking_fee_bps"]), row["symbol"], row["venue"]),
        )
        taken, identities, labels = [], set(), set()
        for row in pool:
            identity, label = row["identity"], row["exposure_key"]
            if identity in identities:
                row["selection"] = "share class already selected"
            elif label in labels:
                row["selection"] = "exposure label already selected in this asset class"
            elif len(taken) == a.positions:
                row["selection"] = "position limit reached with lower fees or an earlier tie-break"
            else:
                taken.append(row)
                identities.add(identity)
                labels.add(label)
                row["selection"] = "selected by ascending fee, then symbol and venue"
        capacity[strategy] = {
            "requested_positions": a.positions, "eligible_listings": len(pool),
            "distinct_exposure_labels": len({row["exposure_key"] for row in pool}),
            "fee_at_selection_cutoff_bps": taken[-1]["ranking_fee_bps"] if len(taken) == a.positions else None,
        }
        if len(taken) < a.positions:
            blockers.append(f"{strategy} needs {a.positions} distinct positions and only {len(taken)} fit the rules")
            continue
        weight, extra = divmod(a.weight_bps, a.positions)
        for index, row in enumerate(taken):
            positions.append({**row, "weight_bps": weight + (index < extra), "rank_within_asset_class": index + 1})
    if blockers:
        for row in rows:
            if row["screen_status"] == "passed":
                row["selection"] = "allocation withheld because portfolio is infeasible"
        return [], blockers, capacity
    return positions, [], capacity


def allocate_cents(positions, cents):
    amounts, remainders = [], []
    for position in positions:
        whole, remainder = divmod(cents * position["weight_bps"], BPS)
        amounts.append(whole)
        remainders.append(remainder)
    order = sorted(range(len(amounts)), key=lambda i: (-remainders[i], i))
    for index in order[:cents - sum(amounts)]:
        amounts[index] += 1
    return amounts


def build(records, profile):
    filters, allocations, initial, recurring = validate_profile(profile)
    rows = candidates(records, filters, allocations)
    positions, blockers, capacity = select(rows, allocations)
    if positions:
        initial_cash = allocate_cents(positions, initial)
        recurring_cash = allocate_cents(positions, recurring)
        for position, start, contribution in zip(positions, initial_cash, recurring_cash, strict=True):
            position.update(initial_cash_cents=start, recurring_cash_cents=contribution)
    selected = {candidate_key(row) for row in positions}
    for row in rows:
        row["selected"] = candidate_key(row) in selected
        row.setdefault("selection", f"screen {row['screen_status']}")
    return {
        "status": "infeasible" if blockers else "allocated",
        "profile": profile,
        "cash": {
            "currency": filters.currency,
            "initial_budget_cents": initial, "recurring_budget_cents": recurring,
            "initial_allocated_cents": sum(row["initial_cash_cents"] for row in positions),
            "recurring_allocated_cents": sum(row["recurring_cash_cents"] for row in positions),
            "initial_unallocated_cents": initial if blockers else 0,
            "recurring_unallocated_cents": recurring if blockers else 0,
        },
        "counts": {
            "requested": len(rows), "researched": sum(row["researched"] for row in rows),
            "comparison_ready": sum(row["comparison_ready"] for row in rows),
            "eligible": sum(row["screen_status"] == "passed" for row in rows),
            "shortlisted": None, "selected": len(positions),
        },
        "allocated_weight_bps": sum(row["weight_bps"] for row in positions),
        "allocation_capacity": capacity, "positions": positions, "blockers": blockers, "candidates": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="Saved issuer-reviewed manual-coverage.json")
    parser.add_argument("profile", type=Path, help="Illustrative portfolio profile JSON")
    parser.add_argument("--output", type=Path, help="Save full JSON report, including all candidate reasons")
    args = parser.parse_args()
    if args.output and args.output.resolve() in {args.snapshot.resolve(), args.profile.resolve()}:
        parser.error("Choose an output path apart from the inputs")
    try:
        records = json.loads(args.snapshot.read_text(encoding="utf-8"))["records"]
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
        result = build(records, profile)
        output = json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output + "\n", encoding="utf-8")
            print(json.dumps({key: result[key] for key in ("status", "counts", "cash", "blockers")}))
            print(args.output)
        else:
            print(output)
    except (AttributeError, OSError, KeyError, TypeError, ValueError) as error:
        parser.error(f"Could not construct portfolio: {error}")
    return 1 if result["status"] == "infeasible" else 0


if __name__ == "__main__":
    raise SystemExit(main())
