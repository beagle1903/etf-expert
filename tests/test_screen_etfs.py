from copy import deepcopy
from dataclasses import replace
from datetime import date
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys


sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from screen_etfs import Filters, assess, compare, report, summary


AS_OF = date(2026, 11, 18)
SOURCE = {"url": "https://fund.example/evidence"}


def listing(symbol="FUND", strategy="bond"):
    return {
        "listing": {"market": "EU", "venue": "XETR", "symbol": symbol, "strategy": strategy},
        "identifier": {"type": "ISIN", "value": "IE000I2WYEU9"},
        "trading_currency": "EUR", "listing_source": SOURCE, "fee_and_exposure_source": SOURCE,
        "exposure": "Shared Benchmark",
        "annual_fees": [{"metric": "ter", "annual_basis_points": "20", "raw_percent": "0.20",
                         "as_of": "2026-11-06"}],
        "bond_risk": {
            "duration_years": "5.10", "duration_method": "effective", "duration_as_of": "2026-11-06",
            "credit_weights_percent": {"BBB-": "90", "BB+": "5", "Cash and/or Derivatives": "5"},
            "credit_as_of": "2026-10-31", "source": SOURCE,
        },
    }


def test_inclusive_limits_and_asset_specific_rules():
    filters = Filters(AS_OF, fee_caps={"ter": Decimal(20)},
                      max_duration=Decimal("5.10"), max_below_ig=Decimal(5))
    record = listing()
    assert assess(record, filters)["status"] == "passed"
    assert assess(record, replace(filters, max_duration=Decimal("5.09")))["status"] == "failed"
    assert assess(record, replace(filters, max_below_ig=Decimal("4.99")))["status"] == "failed"
    assert assess(record, replace(filters, fee_caps={"ter": Decimal("19.999")}))["status"] == "failed"
    equity = listing(strategy="equity")
    equity["bond_risk"] = None
    assert assess(equity, replace(filters, max_duration=Decimal(0)))["status"] == "passed"


def test_credit_uncertainty_does_not_become_zero_or_a_measured_failure():
    record = listing()
    record["bond_risk"]["credit_weights_percent"] = {"BBB-": "91", "B": "2", "Other": "3", "Cash": "1"}
    filters = Filters(AS_OF, max_below_ig=Decimal(5))
    result = assess(record, filters)
    assert result["credit_range"] == (2, 8)
    assert result["status"] == "unknown" and result["comparison_ready"]
    assert assess(record, replace(filters, max_below_ig=Decimal(1)))["status"] == "failed"
    assert assess(record, replace(filters, max_below_ig=Decimal(8)))["status"] == "passed"
    record["bond_risk"]["credit_weights_percent"] = {"A": "101"}
    assert assess(record, filters)["status"] == "unknown"


def test_missing_fee_metrics_conflicting_claims_and_stale_dates():
    record = listing(strategy="equity")
    exact = Filters(AS_OF, max_age_days=12, fee_caps={"ter": Decimal(20)})
    assert assess(record, exact)["status"] == "passed"
    stale = assess(record, replace(exact, max_age_days=11))
    assert stale["status"] == "unknown"
    assert any("12 days old" in reason for reason in stale["reasons"])
    missing = assess(record, replace(exact, fee_caps={"net_expense_ratio": Decimal(20)}))
    assert missing["status"] == "unknown" and missing["comparison_ready"]
    claim = record["annual_fees"][0]
    new_claim = {**claim, "annual_basis_points": "21", "raw_percent": "0.21"}
    record["annual_fees"].append(new_claim)
    assert "conflicting fee amounts on the same date" in " ".join(assess(record, exact)["reasons"])
    new_claim["as_of"] = "2026-11-19"
    assert assess(record, exact)["status"] == "passed"
    new_claim["as_of"] = None
    assert assess(record, exact)["status"] == "unknown"
    record["annual_fees"] = [claim]
    record["conflicts"] = ["exposure"]
    assert assess(record, exact)["status"] == "unknown"


def test_cross_listings_are_distinct_from_label_matches_and_exclusions():
    one, two, three = (listing(symbol) for symbol in ("ONE", "TWO", "THREE"))
    two["listing"]["venue"] = "XAMS"
    three["identifier"]["value"] = "IE0000MR4GH9"
    filters = Filters(AS_OF, excluded_symbols=("THREE",), hedged_to="EUR")
    one["currency_hedge"] = {"target": "EUR", "as_of": "2026-11-06", "source": SOURCE}
    rows = compare([one, two, three], filters)
    assert summary(rows) == {
        "input": 3, "comparison-ready": 3, "passed": 1, "failed": 1, "unknown": 1,
        "explicit exclusions within failed": 1,
    }
    text = report(rows, filters)
    assert text == report(compare([three, two, one], filters), filters)
    assert "- ISIN:IE000I2WYEU9 · TWO · XAMS, ONE · Xetra" in text
    assert "- Shared Benchmark · TWO · XAMS, ONE · Xetra, THREE · Xetra" in text
    assert "bond hedge target missing" in text
    assert "symbol explicitly excluded" in text


def test_cli_saves_source_linked_report_without_dropping_unresolved_rows(tmp_path):
    snapshot = tmp_path / "cohort.json"
    missing = deepcopy(listing("MISS"))
    missing["bond_risk"] = None
    missing_venue = listing("NOVENUE")
    missing_venue["listing"]["venue"] = None
    snapshot.write_text(json.dumps({"records": [listing(), missing, missing_venue]}), encoding="utf-8")
    output = tmp_path / "screen.md"
    script = Path(__file__).parents[1] / "scripts" / "screen_etfs.py"
    result = subprocess.run([
        sys.executable, str(script), str(snapshot), "--as-of", "2026-11-18",
        "--fee-cap", "ter=20", "--output", str(output),
    ], check=True, capture_output=True, text=True)
    assert json.loads(result.stdout.splitlines()[-1])["unknown"] == 2
    text = output.read_text(encoding="utf-8")
    assert "**Input** 3" in text and "**Comparison-ready** 1" in text
    assert "MISS" in text and "https://fund.example/evidence" in text
    assert "NOVENUE · unresolved venue" in text and "venue or asset class unresolved" in text
