"""One-pass Yahoo coverage diagnostic; no eligibility or allocation decisions."""
import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import time

import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {
    "name": ("longName", "shortName"),
    "quote_type": ("quoteType",),
    "exchange": ("exchange",),
    "trading_currency": ("currency",),
    "category": ("category",),
    "net_assets": ("totalAssets",),
    "expense_ratio_raw": ("annualReportExpenseRatio", "netExpenseRatio"),
    "benchmark": ("benchmark", "benchmarkName"),
    "isin": ("isin",),
}


def present(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        return False
    if isinstance(value, (float, int)):
        return math.isfinite(value)
    return True


def assess(info, prices, holdings):
    fields = {}
    for name, keys in FIELDS.items():
        hits = {key: info[key] for key in keys if present(info.get(key))}
        fields[name] = hits
    return {
        "fields": fields,
        "missing": [key for key, value in fields.items() if not value],
        "price_rows": len(prices),
        "holdings_rows": len(holdings),
        "observed_quote_type": info.get("quoteType"),
    }


def collect(member):
    ticker = yf.Ticker(member["symbol"])
    result = {**member, "source_url": f"https://finance.yahoo.com/quote/{member['symbol']}/", "collected_at_utc": datetime.now(timezone.utc).isoformat(), "errors": {}}
    info, prices, holdings = {}, [], []
    try:
        info = ticker.get_info()
    except Exception as exc:
        result["errors"]["profile"] = f"{type(exc).__name__}: {exc}"
    try:
        frame = ticker.history(period="1mo", auto_adjust=False, timeout=15, raise_errors=True)
        prices = json.loads(frame.reset_index().to_json(orient="records", date_format="iso"))
    except Exception as exc:
        result["errors"]["prices"] = f"{type(exc).__name__}: {exc}"
    try:
        frame = ticker.funds_data.top_holdings
        holdings = json.loads(frame.reset_index().to_json(orient="records"))
    except Exception as exc:
        result["errors"]["holdings"] = f"{type(exc).__name__}: {exc}"
    result.update(assess(info, prices, holdings))
    result["raw"] = {"info": info, "prices": prices, "holdings": holdings}
    return result


def report(rows):
    lines = ["# Yahoo ETF coverage diagnostic", "",
             f"Collected: {datetime.now(timezone.utc).isoformat()}", "",
             "One sample pass; no completeness, reliability or eligibility claim. Profile/holdings observation dates are not established by collection time.", "",
             "Expense fields retain Yahoo names and raw units; no comparable fee metric has been validated. Missing benchmark/ISIN means absent from this profile response, not unavailable from every Yahoo interface.", "",
             "| Market | Listings | ETF quote type | Prices present | Holdings present |", "|---|---:|---:|---:|---:|"]
    for market in ("US", "EU"):
        group = [r for r in rows if r["market"] == market]
        lines.append(f"| {market} | {len(group)} | {sum(r['observed_quote_type'] == 'ETF' for r in group)} | {sum(r['price_rows'] > 0 for r in group)} | {sum(r['holdings_rows'] > 0 for r in group)} |")
    lines += ["", "| Profile field present | US | EU |", "|---|---:|---:|"]
    for field in FIELDS:
        counts = [sum(bool(r["fields"][field]) for r in rows if r["market"] == m) for m in ("US", "EU")]
        lines.append(f"| {field} | {counts[0]} | {counts[1]} |")
    lines += ["", "| Listing | Prices | Holdings | Missing profile fields | Failed stages |", "|---|---:|---:|---|---|"]
    for r in rows:
        lines.append(f"| {r['symbol']} | {r['price_rows']} | {r['holdings_rows']} | {', '.join(r['missing']) or 'none'} | {', '.join(r['errors']) or 'none'} |")
    lines += ["", "Raw responses and detailed errors are saved locally alongside this report. Price timestamps are retained in those responses. Partial holdings do not establish complete fund overlap.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--universe", type=Path, default=ROOT / "data/universe.json")
    args = parser.parse_args()
    members = json.loads(args.universe.read_text(encoding="utf-8"))
    symbols = [m["symbol"] for m in members]
    if not members or len(symbols) != len(set(symbols)):
        raise ValueError("Universe must be nonempty with unique symbols")
    folder = ROOT / "data/runs" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    folder.mkdir(parents=True)
    (folder / "universe.json").write_text(json.dumps(members, indent=2), encoding="utf-8")
    (folder / "environment.json").write_text(json.dumps({"yfinance_version": yf.__version__, "requested_listings": len(members)}, indent=2), encoding="utf-8")
    rows = []
    for member in members:
        print(f"Collecting {member['symbol']}", flush=True)
        row = collect(member)
        rows.append(row)
        (folder / f"{member['symbol']}.json").write_text(json.dumps(row, indent=2, default=str), encoding="utf-8")
        (folder / "report.md").write_text(report(rows), encoding="utf-8")
        time.sleep(0.5)
    print(f"Report: {folder / 'report.md'}")


if __name__ == "__main__":
    main()
