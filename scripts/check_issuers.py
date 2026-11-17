"""Download official source candidates; retain failures and text for local review.

This is a coverage experiment, not a fund eligibility or identity validator.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]


def now():
    return datetime.now(timezone.utc).isoformat()


def pdf_text(data):
    with pdfium.PdfDocument(data) as doc:
        pages = []
        for page in doc:
            textpage = page.get_textpage()
            try:
                pages.append(textpage.get_text_range())
            finally:
                textpage.close()
                page.close()
        return "\n\f\n".join(pages)


def collect(source, folder, index):
    result = {**source, "collected_at_utc": now(), "error": None}
    started = time.monotonic()
    try:
        request = Request(source["url"], headers={"User-Agent": "ETFExpertResearch/0.1 (local coverage study)", "Accept": "application/pdf,text/html"})
        with urlopen(request, timeout=35) as response:
            data = response.read(25_000_001)
            result.update(status=response.status, final_url=response.url,
                          content_type=response.headers.get("Content-Type"),
                          last_modified=response.headers.get("Last-Modified"))
        if len(data) > 25_000_000:
            raise ValueError("Response exceeded 25 MB bound")
        suffix = ".pdf" if data.startswith(b"%PDF-") else ".csv" if source["kind"] == "holdings" and b"<html" not in data[:1000].lower() else ".html"
        name = f"{source['symbol']}-{index}{suffix}"
        (folder / name).write_bytes(data)
        result.update(raw_file=name, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
        if suffix == ".pdf":
            text = pdf_text(data)
            (folder / f"{source['symbol']}-{index}.txt").write_text(text, encoding="utf-8")
            result.update(text_file=f"{source['symbol']}-{index}.txt", text_chars=len(text))
        elif source.get("kind") == "factsheet":
            raise ValueError("Expected PDF, received non-PDF response; no coverage credited")
        elif source.get('kind') == 'holdings' and suffix != '.csv':
            raise ValueError('Expected holdings CSV, received another content type; no coverage credited')
    except Exception as exc:
        if isinstance(exc, HTTPError):
            result["status"] = exc.code
            name = f"{source['symbol']}-{index}-error.html"
            (folder / name).write_bytes(exc.read())
            result["raw_file"] = name
        result["error"] = f"{type(exc).__name__}: {exc}"
    result["elapsed_seconds"] = round(time.monotonic() - started, 3)
    result["completed_at_utc"] = now()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=ROOT / "data/issuer_sources.json")
    parser.add_argument("--symbols", nargs="+", help="Explicit subset for probing; default checks all 24")
    parser.add_argument("--kinds", nargs="+", choices=['factsheet', 'product', 'holdings'], help="Explicit source types; default attempts all")
    args = parser.parse_args()
    sources = json.loads(args.sources.read_text(encoding="utf-8"))
    universe = json.loads((ROOT / "data/universe.json").read_text(encoding="utf-8"))
    expected = {m["symbol"] for m in universe}
    if {s["symbol"] for s in sources if s["kind"] == "factsheet"} != expected:
        raise ValueError("Factsheet candidates must cover the unchanged sample exactly")
    if args.symbols and not set(args.symbols) <= expected:
        raise ValueError("Unknown requested symbol")
    folder = ROOT / "data/runs" / ("issuers-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    folder.mkdir(parents=True)
    (folder / "sources.json").write_text(json.dumps(sources, indent=2), encoding="utf-8")
    (folder / "universe.json").write_text(json.dumps(universe, indent=2), encoding="utf-8")
    run = {"started_at_utc": now(), "python": platform.python_version(),
           "pdfium": pdfium.PYPDFIUM_INFO.version, "requested_symbols": args.symbols or sorted(expected), "requested_kinds":args.kinds, "results": []}
    for i, source in enumerate(sources):
        if args.symbols and source["symbol"] not in args.symbols:
            continue
        if args.kinds and source['kind'] not in args.kinds:
            continue
        result = collect(source, folder, i)
        run["results"].append(result)
        (folder / "collection.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
        print(source["symbol"], result.get("status"), result["error"] or result.get("text_chars", "saved"), flush=True)
        time.sleep(0.5)
    run["completed_at_utc"] = now()
    (folder / "collection.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
    print(folder)


if __name__ == "__main__":
    main()
