"""Prepare and check a local ETF issuer-review worksheet."""

import argparse
from datetime import date
import json
from pathlib import Path
import re

from check_broader_coverage import save_json
from discover_tickers import discover
from prepare_snapshot import listing_key, prepare_snapshot
from screen_etfs import (
    FEE_METRICS, Filters, assess, bond_evidence, date_problem, fee_evidence, observation_date,
)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def listing_keys(listings):
    if not isinstance(listings, list) or not listings:
        raise ValueError("Provide a nonempty listing list")
    keys = [listing_key(listing) for listing in listings]
    if any(market not in ("US", "EU") or (venue is not None and not isinstance(venue, str))
           or not isinstance(symbol, str) or not re.fullmatch(r"[A-Z0-9][A-Z0-9.-]*", symbol)
           for market, venue, symbol in keys):
        raise ValueError("Invalid listing market, venue or symbol")
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate listing keys")
    return keys


def make_worksheet(request, directory=None, source=None):
    if "listings" in request and "tickers" in request:
        raise ValueError("Provide either tickers or listings")
    if "tickers" in request:
        if directory is not None:
            request = {**request, **discover(request, directory, source)}
        else:
            tickers = request["tickers"]
            if (not isinstance(tickers, list) or any(
                    not isinstance(ticker, str) or not re.fullmatch(r"[A-Z][A-Z0-9.-]*", ticker)
                    for ticker in tickers)):
                raise ValueError("Tickers must be a list of unique uppercase symbols")
            request = {**request, "listings": [{"market": "US", "symbol": t} for t in tickers]}
    elif directory is not None:
        raise ValueError("Saved Nasdaq input applies only to a U.S. ticker list")

    listings = [listing if "venue" in listing else {**listing, "venue": None}
                for listing in request["listings"]]
    keys = listing_keys(listings)
    return {
        "listings": listings,
        "discovery": {key: value for key, value in request.items() if key != "listings"},
        "rows": [
            {"market": market, "venue": venue, "symbol": symbol, "review": None}
            for market, venue, symbol in keys
        ],
        "attempts": [],
    }


def check_worksheet(worksheet, filters):
    listings = worksheet["listings"]
    keys = listing_keys(listings)
    by_key = dict(zip(keys, listings, strict=True))
    row_keys = listing_keys(worksheet["rows"])
    if set(row_keys) != set(keys):
        raise ValueError("Worksheet rows must match the pinned listing keys")

    reviewed = {"records": [], "attempts": worksheet["attempts"], "discovery": worksheet["discovery"]}
    for key, row in zip(row_keys, worksheet["rows"], strict=True):
        facts = row["review"]
        if facts is None:
            continue
        if (not isinstance(facts, dict) or not facts
                or {"listing", "review_status"} & facts.keys()):
            raise ValueError(f"{key}: use null or a nonempty review object without listing or review_status")
        reviewed["records"].append({"listing": by_key[key], **facts})

    # Check the same normalized evidence the downstream commands will use.
    snapshot = prepare_snapshot(worksheet, reviewed)
    resolution = {("US", result["ticker"]): result["status"]
                  for result in worksheet["discovery"].get("resolution", [])}
    for record in snapshot["records"]:
        market, venue, symbol = listing_key(record["listing"])
        state = "unreviewed" if record.get("review_status") == "missing" else "reviewed"
        lookup = resolution.get((market, symbol), "venue recorded" if venue else "venue unresolved")
        result = assess(record, filters)
        details = []
        bond_problems = []
        if record["listing"].get("strategy") == "bond":
            _, _, duration, credit = bond_evidence(record, filters)
            bond_problems = [p for p in (duration, credit) if p]
            details.extend(f"{label}: {problem}" for label, problem in
                           (("duration", duration), ("credit", credit)) if problem)
            risk = record.get("bond_risk") or {}
            for label, problem in (("duration", duration), ("credit", credit)):
                date_gap = date_problem(risk.get(f"{label}_as_of"), filters)
                if date_gap and date_gap != problem:
                    details.append(f"{label} date: {date_gap}")
            if hedge := record.get("currency_hedge"):
                if gap := date_problem(hedge.get("as_of"), filters):
                    details.append(f"hedge date: {gap}")
        details.extend(reason for reason in result["reasons"] if reason not in bond_problems)
        fees = record.get("annual_fees") or ()
        for index, claim in enumerate(fees, 1):
            if observation_date(claim.get("as_of")) is None:
                details.append(f"fee claim {index}: missing or invalid observation date")
        for metric in dict.fromkeys(claim.get("metric") for claim in fees):
            if metric in FEE_METRICS:
                _, problem = fee_evidence(record, metric, filters)
            else:
                problem = "unsupported fee metric"
            if problem:
                details.append(f"{metric}: {problem}")
        if record.get("conflicts"):
            details.append("reviewer flagged conflicts: " + ", ".join(record["conflicts"]))
        print(f"{market}/{venue or '?'}/{symbol} [{lookup}; {state}] " + "; ".join(details))
    count = snapshot["reviewed_listing_count"]
    print(f"{count}/{len(keys)} reviewed listings")
    return reviewed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    generate = commands.add_parser("init", help="Create a worksheet with blank issuer reviews")
    generate.add_argument("request", type=Path, help="Pinned ticker list or discovery cohort JSON")
    generate.add_argument("--directory", type=Path, help="Saved Nasdaq Trader directory")
    generate.add_argument("--source-metadata", type=Path, help="Collection metadata for the saved directory")
    generate.add_argument("--output", type=Path, required=True)
    export = commands.add_parser("export", help="Show evidence gaps and write reviews for snapshot assembly")
    export.add_argument("worksheet", type=Path)
    export.add_argument("--as-of", type=date.fromisoformat, required=True)
    export.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "init":
        if bool(args.directory) != bool(args.source_metadata):
            parser.error("Use --directory and --source-metadata together")
        inputs = (args.request, args.directory, args.source_metadata)
    else:
        inputs = (args.worksheet,)
    output_paths = {args.output.resolve(), args.output.with_suffix(".tmp").resolve()}
    if output_paths & {path.resolve() for path in inputs if path is not None}:
        parser.error("Choose an output path distinct from the inputs")

    try:
        if args.command == "init":
            if args.output.exists():
                raise ValueError("Choose a new worksheet path to preserve any existing review")
            result = make_worksheet(
                read_json(args.request),
                args.directory.read_bytes() if args.directory else None,
                read_json(args.source_metadata) if args.source_metadata else None,
            )
            print(f"{len(result['rows'])} listings in worksheet")
        else:
            result = check_worksheet(read_json(args.worksheet), Filters(args.as_of))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        save_json(args.output, result)
    except (OSError, AttributeError, KeyError, TypeError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
