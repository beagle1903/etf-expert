from copy import deepcopy
from pathlib import Path
import sys

import pytest


sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from build_portfolio import build


def fund(symbol, fee, *, exposure=None, identifier=None, strategy="equity"):
    source = {"url": "https://fund.example/evidence"}
    return {
        "listing": {"market": "EU", "venue": "XETR", "symbol": symbol, "strategy": strategy},
        "identifier": {"type": "ISIN", "value": identifier or f"IE000000{ord(symbol[0]):03d}0"},
        "trading_currency": "EUR", "listing_source": source, "fee_and_exposure_source": source,
        "exposure": exposure or f"Benchmark {symbol}",
        "annual_fees": [{"metric": "ter", "annual_basis_points": fee, "as_of": "2026-11-06"}],
        "bond_risk": {
            "duration_years": "4.30", "duration_method": "effective", "duration_as_of": "2026-11-06",
            "credit_weights_percent": {"BBB": "98", "BB": "1", "Not Rated": "1"},
            "credit_as_of": "2026-10-31", "source": source,
        } if strategy == "bond" else None,
    }


def profile():
    return {
        "as_of": "2026-11-18", "market": "EU", "currency": "EUR",
        "initial_cash": "1000.01", "recurring_cash": "0.02",
        "allocations": [{"strategy": "equity", "positions": 3, "weight_bps": 10000, "fee_metric": "ter"}],
    }


def test_full_scope_fee_sorting_and_exact_rounding():
    funds = [fund("C", 15), fund("B", 15), fund("A", 20), fund("Z", 5)]
    result = build(funds, profile())
    assert result == build(list(reversed(funds)), profile())
    assert result["counts"]["requested"] == result["counts"]["eligible"] == 4
    assert result["counts"]["shortlisted"] is None
    positions = result["positions"]
    assert [p["symbol"] for p in positions] == ["Z", "B", "C"]
    assert [p["weight_bps"] for p in positions] == [3334, 3333, 3333]
    assert [p["initial_cash_cents"] for p in positions] == [33341, 33330, 33330]
    assert [p["recurring_cash_cents"] for p in positions] == [1, 1, 0]
    assert result["cash"]["initial_allocated_cents"] == 100001
    assert result["cash"]["recurring_allocated_cents"] == 2


def test_same_class_and_equal_exposure_share_the_capacity():
    one = fund("A", 10, exposure="Same benchmark")
    duplicate = fund("B", 12, exposure=" same   benchmark ", identifier=one["identifier"]["value"])
    related = fund("C", 13, exposure="Same benchmark")
    rows = [one, duplicate, related, fund("D", 15), fund("E", 20)]
    result = build(rows, profile())
    assert [p["symbol"] for p in result["positions"]] == ["A", "D", "E"]
    candidates = {r["symbol"]: r for r in result["candidates"]}
    assert candidates["B"]["selection"] == "share class already selected"
    assert candidates["C"]["selection"] == "exposure label already selected in this asset class"
    duplicate["exposure"] = "Inconsistent benchmark claim"
    result = build(rows, profile())
    assert [p["symbol"] for p in result["positions"]] == ["C", "D", "E"]
    assert {r["symbol"] for r in result["candidates"] if r["screen_status"] == "unknown"} == {"A", "B"}


def test_bond_limits_and_explicit_exclusions_change_the_positions():
    equities = [fund(s, 15) for s in "ABC"]
    bonds = [fund("D", 10, strategy="bond"), fund("E", 11, strategy="bond"), fund("F", 12, strategy="bond")]
    bonds[0]["bond_risk"]["duration_years"] = "4.31"
    bonds[2]["bond_risk"]["credit_weights_percent"] = {"BBB": "99", "BB": "1"}
    item = profile()
    item["excluded_symbols"] = ["a"]
    item["allocations"] = [
        {"strategy": "equity", "positions": 2, "weight_bps": 6001, "fee_metric": "ter"},
        {"strategy": "bond", "positions": 1, "weight_bps": 3999, "fee_metric": "ter", "fee_cap_bps": 12,
         "max_duration_years": "4.30", "max_below_ig_pct": "1"},
    ]
    result = build(equities + bonds, item)
    assert [p["symbol"] for p in result["positions"]] == ["F", "B", "C"]
    assert [p["weight_bps"] for p in result["positions"]] == [3999, 3001, 3000]
    rows = {r["symbol"]: r for r in result["candidates"]}
    assert rows["A"]["screen_status"] == rows["D"]["screen_status"] == "failed"
    assert rows["E"]["screen_status"] == "unknown"
    assert result["counts"]["eligible"] == 3


def test_infeasible_profile_keeps_reasons_and_withholds_cash():
    item = profile()
    item["allocations"] = [
        {"strategy": "equity", "positions": 1, "weight_bps": 9000, "fee_metric": "ter"},
        {"strategy": "bond", "positions": 1, "weight_bps": 1000, "fee_metric": "ter"},
    ]
    result = build([fund("A", 0), fund("B", 0)], item)
    assert result["status"] == "infeasible" and result["positions"] == []
    assert result["counts"]["requested"] == 2 and result["counts"]["eligible"] == 2
    assert result["cash"]["initial_allocated_cents"] == 0
    assert result["cash"]["initial_unallocated_cents"] == 100001
    assert result["blockers"] == ["bond needs 1 distinct positions and only 0 fit the rules"]


def test_invalid_profile_reports_inexact_cash_and_invalid_weights():
    item = profile()
    wrong_cash = deepcopy(item)
    wrong_cash["initial_cash"] = "1000.001"
    with pytest.raises(ValueError, match="decimal places"):
        build([], wrong_cash)
    item["allocations"][0]["weight_bps"] = 9000
    with pytest.raises(ValueError, match="sum to 10,000"):
        build([], item)
