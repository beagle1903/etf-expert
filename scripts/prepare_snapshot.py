"""Assemble a fixed discovery cohort and locally reviewed facts for offline use."""

import argparse
import json
from pathlib import Path

from check_broader_coverage import save_json
from screen_etfs import FEE_METRICS, conflict, decimal, source_url


def listing_key(listing):
    return listing["market"], listing["venue"], listing["symbol"]


def prepare_snapshot(cohort, reviewed):
    listings = cohort["listings"]
    keys = [listing_key(listing) for listing in listings]
    if len(set(keys)) != len(keys):
        raise ValueError("Discovery cohort contains duplicate listing keys")
    discovered = dict(zip(keys, listings, strict=True))

    review_by_key = {}
    for review in reviewed["records"]:
        key = listing_key(review["listing"])
        if key not in discovered:
            raise ValueError(f"Reviewed listing is outside the discovery cohort: {key}")
        if key in review_by_key:
            raise ValueError(f"Duplicate reviewed listing: {key}")
        if review["listing"] != discovered[key]:
            raise ValueError(f"Reviewed listing metadata differs from the discovery cohort: {key}")
        review_by_key[key] = review

    records = []
    for key in keys:
        listing = discovered[key]
        if key not in review_by_key:
            records.append({"listing": listing, "review_status": "missing"})
            continue
        record = review_by_key[key]
        if (strategy := record.get("reviewed_strategy")) is not None:
            if (listing.get("strategy") is not None or strategy not in ("equity", "bond")
                    or not source_url(record.get("fee_and_exposure_source"))
                    or conflict(record, "strategy")):
                raise ValueError(f"Cannot apply reviewed strategy to {key}")
            record = {**record, "listing": {**listing, "strategy": strategy}}
        fees = []
        for claim in record.get("annual_fees") or ():
            percent = decimal(claim.get("raw_percent"))
            if ("annual_basis_points" not in claim and claim.get("metric") in FEE_METRICS
                    and percent is not None and percent >= 0):
                claim = {**claim, "annual_basis_points": format(percent * 100, "f")}
            fees.append(claim)
        records.append({**record, "annual_fees": fees} if record.get("annual_fees") is not None else record)
    return {
        **reviewed, "records": records, "requested_listing_count": len(keys),
        "reviewed_listing_count": len(review_by_key),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cohort", type=Path, help="Pinned pilot-universe.json from discovery")
    parser.add_argument("reviewed", type=Path, help="JSON with the manually verified records and source attempts")
    parser.add_argument("--output", type=Path, required=True, help="Path for the assembled JSON snapshot")
    args = parser.parse_args()
    outputs = {args.output.resolve(), args.output.with_suffix(".tmp").resolve()}
    if outputs & {args.cohort.resolve(), args.reviewed.resolve()}:
        parser.error("Choose an output path distinct from both inputs")
    try:
        cohort = json.loads(args.cohort.read_text(encoding="utf-8-sig"))
        reviewed = json.loads(args.reviewed.read_text(encoding="utf-8-sig"))
        snapshot = prepare_snapshot(cohort, reviewed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        save_json(args.output, snapshot)
    except (OSError, AttributeError, KeyError, TypeError, ValueError) as error:
        parser.error(f"Could not assemble reviewed snapshot: {error}")
    print(f"{snapshot['reviewed_listing_count']}/{snapshot['requested_listing_count']} reviewed listings")
    print(args.output)


if __name__ == "__main__":
    main()
