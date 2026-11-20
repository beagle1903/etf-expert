"""Resolve a pinned U.S. ticker list against a saved Nasdaq Trader directory."""

import argparse
import hashlib
import json
from pathlib import Path
import re

from broader_snapshot import parse_nasdaq
from check_broader_coverage import save_json


def discover(request, raw, source):
    tickers = request["tickers"]
    if (not isinstance(tickers, list) or not tickers
            or any(not isinstance(t, str) or not re.fullmatch(r"[A-Z][A-Z0-9.-]*", t) for t in tickers)
            or len(set(tickers)) != len(tickers)):
        raise ValueError("Tickers must be a nonempty list of unique uppercase symbols")
    digest = hashlib.sha256(raw).hexdigest()
    if source.get("error") or (source.get("sha256") and source["sha256"] != digest):
        raise ValueError("Directory collection failed or its saved hash does not match")
    rows, source_date = parse_nasdaq(raw.decode("utf-8-sig"))
    by_symbol = {}
    for row in rows:
        by_symbol.setdefault(row["symbol"], []).append(row)
    listings, outcomes = [], []
    for ticker in tickers:
        matches = by_symbol.get(ticker, [])
        if len(matches) == 1:
            # Directory name heuristics are not issuer-verified asset classes.
            listing = {**matches[0], "strategy": None}
            outcome = "resolved"
        else:
            listing = {"market": "US", "venue": None, "symbol": ticker, "name": None,
                       "strategy": None, "currency": None, "isin": None, "source": "nasdaq"}
            outcome = "not found" if not matches else "ambiguous directory matches"
        listings.append(listing)
        outcomes.append({"ticker": ticker, "status": outcome, "matches": matches})
    return {"listings": listings, "resolution": outcomes, "venue_source": {
        **source, "source_date": source_date, "sha256": digest}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    parser.add_argument("directory", type=Path)
    parser.add_argument("source_metadata", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() in {p.resolve() for p in (args.request, args.directory, args.source_metadata)}:
        parser.error("Output must differ from inputs")
    try:
        result = discover(json.loads(args.request.read_text(encoding="utf-8-sig")), args.directory.read_bytes(),
                          json.loads(args.source_metadata.read_text(encoding="utf-8-sig")))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        save_json(args.output, result)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    print(f"{sum(r['status'] == 'resolved' for r in result['resolution'])}/{len(result['resolution'])} resolved")


if __name__ == "__main__":
    main()
