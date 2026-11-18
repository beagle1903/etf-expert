import json
from pathlib import Path
import subprocess
import sys

import pytest


sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from normalize_records import issuer_claim, normalize


def member(symbol="AAA.DE"):
    return {"symbol": symbol, "market": "EU", "intent": "Global equity"}


def fact(value, unit=None, as_of="2026-10-31", **extra):
    return {"value": value, "unit": unit, "as_of": as_of, **extra}


def observation(symbol, fields, index=0, match="exact_code"):
    attempt = {
        "symbol": symbol, "kind": "factsheet", "error": None,
        "url": "https://issuer.test/factsheet", "collected_at_utc": "2026-11-17T15:00:00Z",
    }
    return {**attempt, "listing_match": match, "fields": fields, "attempt_index": index}, attempt


def test_fee_normalization_keeps_metric_zero_precision_and_observation_date():
    gross = issuer_claim("issuer:0", "fee", fact(
        0.0945, "percent per year; gross expense ratio", raw_text="Gross Expense Ratio (%) 0.0945"
    ))
    assert gross["annual_basis_points"] == "9.4500"
    assert gross["raw_text"].endswith("0.0945")
    assert gross["metric"] == "gross_expense_ratio"
    assert gross["as_of"] == "2026-10-31"
    zero = issuer_claim("issuer:0", "fee", fact(0, "percent per year; Total Expense Ratio :", None))
    assert zero["annual_basis_points"] == "0"
    assert zero["metric"] == "ter"
    assert zero["date_status"] == "undated"
    unverified = issuer_claim("issuer:0", "fee", fact(0.01, "unknown unit"))
    assert "annual_basis_points" not in unverified
    with pytest.raises(ValueError):
        issuer_claim("issuer:0", "fee", fact(0.01, as_of="2026-11-31"))


def test_share_class_links_require_attribution_and_identifier():
    fields = {"identifier": fact("IE00B5BMR087", "ISIN"), "benchmark": fact("Example Index"),
              "legal_entity": fact("Example plc"), "share_currency": fact("USD"),
              "listing_currency": fact("EUR"), "base_currency": fact("GBP")}
    records = []
    for symbol, match, identifier in (
        ("AAA.DE", "exact_code", "IE00B5BMR087"),
        ("AAA.AS", "exact_code", "IE00B5BMR087"),
        ("BBB.DE", "exact_code", "IE00BDBRDM35"),
        ("CCC.DE", "ticker_only", "IE00B5BMR087"),
        ("DDD.DE", "unresolved", "IE00B5BMR087"),
    ):
        row, attempt = observation(symbol, {**fields, "identifier": fact(identifier, "ISIN")}, match=match)
        records.append(normalize(member(symbol), [row], [attempt]))
    assert [r["identity"]["share_class_key"] for r in records] == [
        "ISIN:IE00B5BMR087", "ISIN:IE00B5BMR087", "ISIN:IE00BDBRDM35", None, None,
    ]
    assert all(r["identity"]["fund_key"] is None for r in records)
    assert records[-1]["share_class"]["identifier"]["status"] == "unattributed"
    first = records[0]
    assert first["listing"]["trading_currency"]["claims"][0]["raw_value"] == "EUR"
    assert first["share_class"]["currency"]["claims"][0]["raw_value"] == "USD"
    assert first["fund"]["base_currency"]["claims"][0]["raw_value"] == "GBP"
    assert first["share_class"]["hedging"]["status"] == "missing"


def test_conflicts_keep_observations_and_different_fee_bases():
    fees = [
        fact(0.07, "percent per year; Total Expense Ratio", "2026-10-31"),
        fact(0.08, "percent per year; Total Expense Ratio", "2026-11-06"),
        fact(0.09, "percent per year; gross expense ratio", "2026-11-06"),
        fact(0.10, "percent per year; Total Expense Ratio", "2026-11-06"),
    ]
    rows, attempts = zip(*(observation("AAA.DE", {"fee": fee}, i) for i, fee in enumerate(fees)))
    prior = normalize(member(), rows[:3], attempts)
    assert prior["share_class"]["fee"]["status"] == "reported"
    result = normalize(member(), rows, attempts)
    assert result["share_class"]["fee"]["status"] == "conflicting"
    assert len(result["share_class"]["fee"]["claims"]) == 4

    a, b = rows[:2]
    a["fields"]["identifier"] = fact("IE00B5BMR087", "ISIN")
    b["fields"]["identifier"] = fact("IE00BDBRDM35", "ISIN", "2026-11-06")
    b["fields"]["duration"] = fact("Effective Duration 6.0 years", "years", None, date_status="conflicting")
    result = normalize(member(), rows[:2], attempts)
    assert result["share_class"]["identifier"]["status"] == "conflicting"
    assert result["identity"]["share_class_key"] is None
    assert result["exposure"]["duration"]["issues"] == ["conflicting_source_dates"]
    assert result["exposure"]["duration"]["claims"][0]["as_of"] is None


def test_yahoo_fee_is_raw_and_cannot_fill_share_class_currency():
    row, attempt = observation("AAA.DE", {"fee": fact(0.09, "percent per year; Total Expense Ratio")})
    yahoo = {
        "source_url": "https://finance.yahoo.test/quote/AAA.DE/", "collected_at_utc": "2026-11-17T16:00:00Z",
        "fields": {"expense_ratio_raw": {"netExpenseRatio": 0.2}, "trading_currency": {"currency": "EUR"}},
        "price_rows": 2, "holdings_rows": 0, "errors": {"holdings": "unavailable"}, "missing": ["isin"],
    }
    record = normalize(member(), [row], [attempt], yahoo)
    fee = record["share_class"]["fee"]
    assert fee["status"] == "review"
    assert fee["claims"][1]["field"] == "netExpenseRatio"
    assert fee["claims"][1]["as_of"] is None
    assert fee["claims"][1]["raw_unit"] is None
    assert "annual_basis_points" not in fee["claims"][1]
    assert record["share_class"]["currency"]["status"] == "missing"
    assert record["source_coverage"]["yahoo"]["errors"] == {"holdings": "unavailable"}


def test_cli_keeps_no_data_member_and_failed_attempt(tmp_path):
    row, attempt = observation("AAA.DE", {"identifier": fact("IE00B5BMR087", "ISIN")})
    failed = {**attempt, "symbol": "BBB.DE", "error": "HTTP 404"}
    assessment = tmp_path / "assessment.json"
    assessment.write_text(json.dumps({
        "rows": [member(), member("BBB.DE")], "observations": [row], "attempts": [attempt, failed],
    }), encoding="utf-8")
    output = tmp_path / "records.json"
    script = Path(__file__).parents[1] / "scripts" / "normalize_records.py"
    subprocess.run([sys.executable, str(script), str(assessment), "--output", str(output)], check=True)
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["requested_listings"] == result["summary"]["converted"] == 2
    assert result["summary"]["without_source_observations"] == 1
    assert result["summary"]["unresolved_listing_to_share_class"] == 1
    no_data = result["records"][1]
    assert no_data["symbol"] == "BBB.DE"
    assert no_data["share_class"]["fee"]["status"] == "missing"
    assert no_data["issuer_attempts"] == [{**failed, "attempt_index": 1}]
