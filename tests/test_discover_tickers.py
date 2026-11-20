import sys
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
