import json
from pathlib import Path
import subprocess
import sys


SCRIPTS = Path(__file__).parents[1] / "scripts"


def run(script, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          check=True, capture_output=True, text=True).stdout


def test_worksheet_retains_unresolved_untouched_and_conflicting_review(tmp_path):
    request = tmp_path / "request.json"
    request.write_text('{"tickers":["BOND","BLANK","MISSING"]}', encoding="utf-8")
    directory = tmp_path / "nasdaq.txt"
    directory.write_text(
        "Nasdaq Traded|Symbol|Security Name|Listing Exchange|ETF|Test Issue\n"
        "Y|BOND|Example bond|Q|Y|N\nY|BLANK|Example equity|P|Y|N\n"
        "File Creation Time: 1120202603:04|||||\n", encoding="utf-8"
    )
    source = {"url": "https://example.org/listing", "collected_at_utc": "2026-11-20T10:51:00Z"}
    metadata = tmp_path / "source.json"
    metadata.write_text(json.dumps(source), encoding="utf-8")
    worksheet = tmp_path / "worksheet.json"
    reviews = tmp_path / "reviewed.json"
    snapshot = tmp_path / "snapshot.json"
    run("review_worksheet.py", "init", request, "--directory", directory,
        "--source-metadata", metadata, "--output", worksheet)
    document = json.loads(worksheet.read_text(encoding="utf-8"))
    assert [item["review"] for item in document["rows"]] == [None, None, None]
    assert document["listings"][0]["venue"] == "Q"
    assert document["listings"][0]["strategy"] is None
    assert document["listings"][2]["venue"] is None

    issuer = {"url": "https://example.org/issuer", "collected_at_utc": "2026-11-20T11:00:00Z"}
    first = {"metric": "expense_ratio", "raw_percent": "0.08", "as_of": "2026-09-30", "source": issuer}
    second = {**first, "raw_percent": "0.09", "source": {**issuer, "url": "https://example.org/other"}}
    third = {**first, "as_of": None}
    document["rows"][0]["review"] = {
        "reviewed_strategy": "bond",
        "identifier": {"type": "CUSIP", "value": "123456789"},
        "trading_currency": "USD", "listing_source": source, "fee_and_exposure_source": issuer,
        "exposure": "Example aggregate", "annual_fees": [first, second, third],
        "bond_risk": {"duration_method": "effective", "duration_years": "5", "source": issuer},
        "conflicts": ["credit"],
    }
    document["attempts"] = [{"url": "https://example.org/blocked", "error": "HTTP 403"}]
    worksheet.write_text(json.dumps(document), encoding="utf-8")
    before = worksheet.read_bytes()
    diagnostic = run("review_worksheet.py", "export", worksheet, "--as-of", "2026-11-20", "--output", reviews)
    assert "BLANK [resolved; unreviewed]" in diagnostic
    assert "MISSING [not found; unreviewed]" in diagnostic
    assert "conflicting fee amounts on the same date" in diagnostic
    assert "fee claim 3: missing or invalid observation date" in diagnostic
    assert "duration: missing or invalid observation date" in diagnostic
    assert "credit: conflicting credit evidence" in diagnostic
    assert worksheet.read_bytes() == before
    exported = json.loads(reviews.read_text(encoding="utf-8"))
    assert exported["records"][0]["annual_fees"] == [first, second, third]
    assert exported["records"][0]["listing"]["strategy"] is None
    run("prepare_snapshot.py", worksheet, reviews, "--output", snapshot)
    result = json.loads(snapshot.read_text(encoding="utf-8"))
    assert result["requested_listing_count"] == 3
    assert result["reviewed_listing_count"] == 1
    assert result["records"][0]["listing"]["strategy"] == "bond"
    assert [r["review_status"] for r in result["records"][1:]] == ["missing", "missing"]
    assert result["attempts"] == document["attempts"]
    assert result["discovery"]["venue_source"]["source_date"] == "2026-11-20T03:04"


def test_worksheet_rejects_dropped_rows(tmp_path):
    request = tmp_path / "request.json"
    request.write_text(json.dumps({"listings": [
        {"market": "EU", "venue": "XETR", "symbol": "2B7A", "strategy": "bond"},
        {"market": "US", "symbol": "SECOND"},
    ]}), encoding="utf-8")
    worksheet = tmp_path / "worksheet.json"
    run("review_worksheet.py", "init", request, "--output", worksheet)
    data = json.loads(worksheet.read_text(encoding="utf-8"))
    data["rows"].pop()
    worksheet.write_text(json.dumps(data), encoding="utf-8")
    reviewed = tmp_path / "reviewed.json"
    result = subprocess.run([
        sys.executable, str(SCRIPTS / "review_worksheet.py"), "export", str(worksheet),
        "--as-of", "2026-11-20", "--output", str(reviewed),
    ], capture_output=True, text=True)
    assert result.returncode != 0
    assert "match the pinned listing keys" in result.stderr
    assert not reviewed.exists()
