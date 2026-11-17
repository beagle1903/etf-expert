import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("coverage_check", Path(__file__).parents[1] / "scripts/check_coverage.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_missing_fee_is_not_zero_and_zero_fee_is_present():
    missing = module.assess({"netExpenseRatio": None}, [], [])
    zero = module.assess({"netExpenseRatio": 0}, [], [])
    assert "expense_ratio_raw" in missing["missing"]
    assert zero["fields"]["expense_ratio_raw"] == {"netExpenseRatio": 0}


def test_nonfinite_and_blank_fields_are_missing():
    result = module.assess({"totalAssets": float("nan"), "category": " "}, [], [])
    assert "net_assets" in result["missing"]
    assert "category" in result["missing"]


def test_report_separates_listings_from_data_and_quote_type():
    row = {"symbol": "TEST", "market": "EU", "errors": {"profile": "failure"}, **module.assess({}, [{"Close": 1}], [])}
    text = module.report([row])
    assert "| EU | 1 | 0 | 1 | 0 |" in text
    assert "profile" in text
