import hashlib
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
import check_broader_coverage as pilot
from broader_snapshot import parse_nasdaq, parse_xetra, select_candidates


NASDAQ = """Nasdaq Traded|Symbol|Security Name|Listing Exchange|ETF|Test Issue
Y|AAXJ|iShares MSCI Asia ETF|Q|Y|N
Y|AAGX|iShares MSCI New ETF|Q|Y|N
Y|AGZ|iShares Agency Bond ETF|P|Y|N
Y|TEST|iShares MSCI Test ETF|Q|Y|Y
Y|STOCK|A Stock|Q|N|N
N|MISSING|iShares MSCI Other ETF|Q|Y|N
File Creation Time: 1118202603:04|||||
"""
XETRA = """Market:;XETR
Date Last Update:;18.11.2026
Product Status;Instrument Status;Instrument Type;MIC Code;Mnemonic;Instrument;ISIN;Currency;Product Assignment Group Description
Active;Active;ETF;XETR;AA;ISHS MSCI Equity;IE00B4KBBD01;EUR;EXCHANGE TRADED FUNDS - PASSIV
Active;Active;ETF;XETR;AAA;ISHS MSCI Equity;IE00B4KBBD01;USD;EXCHANGE TRADED FUNDS - PASSIV
Active;Active;ETF;XETR;BB;ISHS Corp Bond;IE000Q0UH3Y7;EUR;EXCHANGE TRADED FUNDS - RENTEN
Active;Inactive;ETF;XETR;INACT;ISHS Corp Bond;IE000Q0UH3Y7;EUR;EXCHANGE TRADED FUNDS - RENTEN
Active;Active;ETN;XETR;NOTE;ISHS Corp Bond;IE000Q0UH3Y7;EUR;EXCHANGE TRADED FUNDS - RENTEN
"""
US_CATALOGUE = """<table>
<tr><th>Ticker</th><th>Name</th><th>Gross Expense Ratio (%)</th><th>Net Expense Ratio (%)</th></tr>
<tr><td><a href="/fund/aaxj">AAXJ</a></td><td>iShares MSCI Asia ETF</td><td>0.04</td><td>0.00</td></tr>
</table>"""


def save_response(folder, key, value, index):
    data = value.encode("utf-8")
    file = f"{key}-{index}.raw"
    (folder / file).write_bytes(data)
    return {"source": key, "sha256": hashlib.sha256(data).hexdigest(), "raw_file": file,
            "collected_at_utc": "2026-11-18T08:00:00Z", "error": None, "final_url": f"https://test/{key}"}


def test_count_accounting_and_requested_scope():
    us, us_date = parse_nasdaq(NASDAQ)
    eu, eu_date = parse_xetra(XETRA)
    assert (us_date, eu_date) == ("2026-11-18T03:04", "2026-11-18")
    assert (len(us), len(eu)) == (3, 3)
    rows, groups, excluded = select_candidates(us + eu, {"AAGX", "BB.DE"}, 2)
    assert [r["symbol"] for r in rows] == ["AAXJ", "AGZ", "AA"]
    assert groups["EU/bond"]["shortfall"] == 2
    assert excluded["duplicate_class_or_symbol_within_group"] == 1
    assert excluded["original_symbol"] == 2
    assert len(rows) + sum(excluded.values()) == len(us + eu)


def test_replay_retains_successes_failed_sources_and_frozen_cohort(tmp_path):
    attempts = [
        save_response(tmp_path, "nasdaq", NASDAQ, 0),
        save_response(tmp_path, "xetra", XETRA, 1),
        save_response(tmp_path, "ishares-us", US_CATALOGUE, 2),
        {"source": "sec", "error": "403", "collected_at_utc": "2026-11-18T08:00:00Z"},
    ]
    report = pilot.build_report(tmp_path, attempts, 2)
    rows = {r["listing"]["symbol"]: r for r in report["records"]}
    assert len(rows) == 5
    assert rows["AAXJ"]["facts"]["ishares-us"]["Net Expense Ratio (%)"] == "0.00"
    assert rows["AAXJ"]["facts"]["ishares-us"]["product_url"] == "https://test/fund/aaxj"
    assert rows["AGZ"]["research_attempted"] and not rows["AGZ"]["research_collected"]
    assert not rows["BB"]["research_attempted"]
    assert report["coverage"]["US/equity"]["comparison_ready"] == 0
    assert report["parse_outcomes"][3]["error"] == "403"

    newer = NASDAQ.replace("AAXJ", "REPLACED").replace("1118202603:04", "1119202603:04")
    attempts.append(save_response(tmp_path, "nasdaq", newer, 4))
    attempts.append(save_response(tmp_path, "ishares-us", "<html>temporary outage</html>", 5))
    new = pilot.build_report(tmp_path, attempts, None)
    assert new["records"] == report["records"]
    assert new["sources"]["ishares-us"]["raw_file"] == "ishares-us-2.raw"
    assert "No US catalogue rows" in new["parse_outcomes"][-1]["error"]


def test_incomplete_nasdaq_refresh_preserves_earlier_parseable_snapshot(tmp_path):
    attempts = [
        save_response(tmp_path, "nasdaq", NASDAQ, 0),
        save_response(tmp_path, "xetra", XETRA, 1),
        save_response(tmp_path, "nasdaq", NASDAQ.replace(
            "Y|AAXJ|iShares MSCI Asia ETF|Q|Y|N", "Y|AAXJ"
        ), 2),
    ]
    report = pilot.build_report(tmp_path, attempts, 2)
    assert report["sources"]["nasdaq"]["raw_file"] == "nasdaq-0.raw"
    assert report["venue_counts"]["nasdaq"] == 3
    assert "AAXJ" in [row["listing"]["symbol"] for row in report["records"]]
    error = report["parse_outcomes"][-1]["error"]
    assert "Incomplete source row at line 2" in error
    assert "Security Name" in error
