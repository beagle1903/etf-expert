"""Collect and replay a bounded US and Xetra ETF coverage pilot."""

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from time import monotonic
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from broader_snapshot import GROUPS, PARSERS, parse_issuer_us, research, select_candidates


ROOT = Path(__file__).resolve().parents[1]
US_SCREENER_QUERY = urlencode({
    "dcrPath": "/templatedata/config/product-screener-v3/data/en/us-ishares/ishares-product-screener-backend-config",
})
DE_SCREENER_QUERY = urlencode({
    "country": "de", "language": "de", "siteName": "de-ishares-v2", "userType": "individual",
})
SOURCES = {
    "nasdaq": "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqtraded.txt",
    "xetra": "https://www.cashmarket.deutsche-boerse.com/resource/blob/1528/fd4f73721b4ba9ab3d3f2b119c3798eb/data/t7-xetr-allTradableInstruments.csv",
    "sec": "https://www.sec.gov/files/investment/data/other/investment-company-series-class-information/investment-company-series-class-2026.csv",
    "ishares-us": "https://www.ishares.com/us/products/etf-investments",
    "ishares-de": "https://www.ishares.com/de/privatanleger/de/produkte/produktliste",
    "ishares-de-legacy": "https://www.ishares.com/de/privatanleger/de/produkte/etf-investments",
    "ishares-de-data": "https://www.ishares.com/de/privatanleger/de/product-data.jsn",
    "ishares-us-data": "https://www.ishares.com/us/product-data.jsn",
    "ishares-us-screener": "https://www.ishares.com/us/product-screener/product-screener-v3.1.jsn?" + US_SCREENER_QUERY,
    "ishares-de-screener": (
        "https://www.ishares.com/varnish-api/blk-product-screener-server/api/v1/product-screener/product-data?"
        + DE_SCREENER_QUERY
    ),
    "danimoth": "https://framerusercontent.com/assets/9P7xYXRDqQbeREtGVGAa9z23Ac.csv",
}
MAX_BYTES = 16_000_000


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def fetch_source(key, folder, index, timeout, user_agent):
    url = SOURCES[key]
    started = monotonic()
    result = {"source": key, "url": url, "collected_at_utc": datetime.now(timezone.utc).isoformat(), "error": None}
    try:
        with urlopen(Request(url, headers={"User-Agent": user_agent}), timeout=timeout) as response:
            result.update(
                status=response.status, final_url=response.url, last_modified=response.headers.get("Last-Modified"),
                content_type=response.headers.get("Content-Type"),
            )
            data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Response exceeded 16 MB bound")
        name = f"{key}-{index}.raw"
        (folder / name).write_bytes(data)
        result.update(raw_file=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    except (HTTPError, URLError, OSError, ValueError) as exc:
        if isinstance(exc, HTTPError):
            result.update(status=exc.code, final_url=exc.url)
            exc.close()
        result["error"] = f"{type(exc).__name__}: {exc}"
    result["elapsed_seconds"] = round(monotonic() - started, 3)
    return result


def load_sources(folder, attempts):
    parsed, sources, outcomes = {}, {}, []
    for attempt in attempts:
        key = attempt["source"]
        outcome = {"source": key, "collected_at_utc": attempt["collected_at_utc"], "error": attempt["error"]}
        outcomes.append(outcome)
        if attempt["error"]:
            continue
        try:
            raw = (folder / attempt["raw_file"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != attempt["sha256"]:
                raise ValueError("Cached response hash mismatch")
            text = raw.decode("utf-8-sig")
            rows, source_date = (parse_issuer_us(text, attempt["final_url"]) if key == "ishares-us"
                                 else PARSERS[key](text))
        except (OSError, ValueError, csv.Error) as exc:
            outcome["error"] = str(exc)
            continue
        parsed[key] = rows
        sources[key] = {**attempt, "source_date": source_date, "rows_or_keys": len(rows)}
    return parsed, sources, outcomes


def build_report(folder, attempts, per_group):
    parsed, sources, outcomes = load_sources(folder, attempts)
    universe_path = folder / "pilot-universe.json"
    if universe_path.is_file():
        universe = read_json(universe_path)
        if per_group is not None and universe["per_group"] != per_group:
            raise ValueError("This snapshot has a fixed pilot universe. Use a new directory for a different quota.")
        # Keep the discovery metadata with the frozen listing rows, even after source refreshes.
        sources.update(universe["venue_sources"])
    else:
        per_group = per_group or 10
        venues = parsed.get("nasdaq", []) + parsed.get("xetra", [])
        baseline = {row["symbol"] for row in read_json(ROOT / "data/universe.json")}
        listings, groups, excluded = select_candidates(venues, baseline, per_group)
        universe = {
            "per_group": per_group, "groups": groups, "exclusions": excluded, "listings": listings,
            "venue_counts": {key: len(parsed[key]) for key in ("nasdaq", "xetra") if key in parsed},
            "venue_sources": {key: sources[key] for key in ("nasdaq", "xetra") if key in sources},
        }
        # An unavailable venue file is a scope shortfall. Allow deliberate retry
        # of initial discovery until both venue files have parsed.
        if len(universe["venue_sources"]) == 2:
            save_json(universe_path, universe)
    attempted_sources = {a["source"] for a in attempts}
    records = [research(row, parsed, sources, attempted_sources) for row in universe["listings"]]
    coverage = {}
    for group in GROUPS:
        rows = [r for r in records if f"{r['listing']['market']}/{r['listing']['strategy']}" == group]
        coverage[group] = {
            **universe["groups"][group],
            **{name: sum(r[name] for r in rows) for name in (
                "research_attempted", "research_collected", "normalized", "unresolved", "comparison_ready"
            )},
            "field_counts": {
                name: sum(r["required_evidence"].get(name, False) for r in rows)
                for name in sorted({name for r in rows for name in r["required_evidence"]})
            },
            "source_counts": {
                key: sum(key in r["facts"] for r in rows)
                for key in ("ishares-us", "danimoth", "sec", "ishares-us-screener", "ishares-de-screener")
            },
            "secondary_hedge_claims": sum(r["facts"].get("danimoth", {}).get("is_hedged", "") != "" for r in rows),
            "secondary_holdings_counts": sum(bool(r["facts"].get("danimoth", {}).get("number_of_holdings")) for r in rows),
            "raw_fee_claims": sum(bool(
                r["facts"].get("ishares-us", {}).get("Gross Expense Ratio (%)")
                or r["facts"].get("danimoth", {}).get("ter")
            ) for r in rows),
            "screener_undated_duration_claims": sum(
                r["listing"]["strategy"] == "bond" and any(
                    isinstance(r["facts"].get(key, {}).get("effectiveDuration"), dict)
                    for key in ("ishares-us-screener", "ishares-de-screener")
                )
                for r in rows
            ),
        }
    report = {
        "venue_counts": universe["venue_counts"], "exclusions": universe["exclusions"], "coverage": coverage,
        "sources": sources, "attempts": attempts, "parse_outcomes": outcomes, "records": records,
    }
    save_json(folder / "coverage.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="Local directory for raw inputs and results")
    parser.add_argument("--fetch", nargs="+", choices=SOURCES, help="Fetch named inputs; omit for offline replay")
    parser.add_argument("--refresh", action="store_true", help="Fetch even when a successful response is cached")
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--per-group", type=int, help="Set the per-market/strategy quota for a new pilot (default 10)")
    parser.add_argument("--user-agent", default="ETF Expert research (https://github.com/beagle1903/etf-expert)")
    args = parser.parse_args()
    if (args.per_group is not None and args.per_group < 1) or args.timeout <= 0:
        parser.error("Quota and timeout must be positive")
    path = args.snapshot / "collection.json"
    attempts = read_json(path) if path.is_file() else []
    if args.fetch:
        args.snapshot.mkdir(parents=True, exist_ok=True)
        for key in dict.fromkeys(args.fetch):
            if not args.refresh and any(a["source"] == key and not a["error"]
                                        and (args.snapshot / a["raw_file"]).is_file() for a in attempts):
                print(f"{key}: using cached response")
                continue
            result = fetch_source(key, args.snapshot, len(attempts), args.timeout, args.user_agent)
            attempts.append(result)
            save_json(path, attempts)
            print(f"{key}: {result['error'] or str(result['bytes']) + ' bytes saved'}", flush=True)
    if not attempts:
        parser.error("No saved responses. Fetch the intended inputs first.")
    report = build_report(args.snapshot, attempts, args.per_group)
    for group, counts in report["coverage"].items():
        print(f"{group}: {counts['requested']}/{counts['target']} requested, "
              f"{counts['research_collected']} collected, {counts['comparison_ready']} comparison-ready")
    print(args.snapshot / "coverage.json")


if __name__ == "__main__":
    main()
