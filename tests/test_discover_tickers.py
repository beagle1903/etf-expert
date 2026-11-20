import sys
import json
import subprocess
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from discover_tickers import discover
from build_portfolio import build


DIRECTORY = ("Nasdaq Traded|Symbol|Security Name|Listing Exchange|ETF|Test Issue\n"
             "Y|AAA|iShares MSCI Fund|Q|Y|N\n"
             "File Creation Time: 1120202603:04|||||\n").encode()


def test_discovery_preserves_unresolved_and_does_not_assert_classification():
    result = discover({"tickers": ["AAA", "MISSING"]}, DIRECTORY, {"url": "https://example.com"})
    assert [x["status"] for x in result["resolution"]] == ["resolved", "not found"]
    assert [x["symbol"] for x in result["listings"]] == ["AAA", "MISSING"]
    assert all(x["strategy"] is None for x in result["listings"])
    assert result["listings"][1]["venue"] is None
    with pytest.raises(ValueError):
        discover({"tickers": ["AAA", "AAA"]}, DIRECTORY, {})
    with pytest.raises(ValueError):
        discover({"tickers": ["AAA"]}, DIRECTORY, {"sha256": "wrong"})


def test_unresolved_asset_class_is_unknown_not_an_exclusion():
    profile = {"as_of": "2026-11-20", "market": "US", "currency": "USD", "initial_cash": "1",
               "recurring_cash": "0", "allocations": [{"strategy": "equity", "positions": 1,
               "weight_bps": 10000, "fee_metric": "expense_ratio"}]}
    listing = {"market": "US", "venue": None, "symbol": "MISSING", "strategy": None}
    row = build([{"listing": listing}], profile)["candidates"][0]
    assert row["screen_status"] == "unknown"
    assert "asset class is unresolved" in row["reasons"]
    assert "asset class has no profile allocation" not in row["reasons"]
    profile["excluded_symbols"] = ["MISSING"]
    excluded = build([{"listing": listing}], profile)["candidates"][0]
    assert excluded["screen_status"] == "failed"
    assert "symbol explicitly excluded" in excluded["reasons"]


@pytest.mark.parametrize(("listing_market", "currency", "reason"), [
    ("EU", None, "outside market US"),
    ("US", "EUR", "trades in EUR, outside currency USD"),
])
def test_unresolved_asset_class_still_applies_common_profile_filters(listing_market, currency, reason):
    profile = {"as_of": "2026-11-20", "market": "US", "currency": "USD", "initial_cash": "1",
               "recurring_cash": "0", "allocations": [{"strategy": "equity", "positions": 1,
               "weight_bps": 10000, "fee_metric": "expense_ratio"}]}
    record = {"listing": {"market": listing_market, "venue": "XETR", "symbol": "TEST", "strategy": None},
              "trading_currency": currency, "listing_source": {"url": "https://example.org/listing"}}
    row = build([record], profile)["candidates"][0]
    assert row["screen_status"] == "failed"
    assert reason in row["reasons"]


@pytest.mark.parametrize("input_name", ["request", "directory", "metadata"])
def test_discovery_rejects_input_at_temporary_output_path(tmp_path, input_name):
    paths = {name: tmp_path / f"{name}.json" for name in ("request", "directory", "metadata")}
    paths[input_name] = tmp_path / "discovered.tmp"
    paths["request"].write_text(json.dumps({"tickers": ["AAA"]}), encoding="utf-8")
    paths["directory"].write_bytes(DIRECTORY)
    paths["metadata"].write_text("{}", encoding="utf-8")
    before = paths[input_name].read_bytes()
    script = Path(__file__).parents[1] / "scripts" / "discover_tickers.py"
    result = subprocess.run([sys.executable, str(script), *(str(paths[name]) for name in
                            ("request", "directory", "metadata")), "--output", str(tmp_path / "discovered.json")],
                            capture_output=True, text=True)
    assert result.returncode != 0
    assert paths[input_name].read_bytes() == before
