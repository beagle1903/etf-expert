import json
from pathlib import Path
import subprocess
import sys


def test_prepared_snapshot_preserves_missing_members_and_failed_attempts(tmp_path):
    first = {"market": "EU", "venue": "XETR", "symbol": "FIRST", "strategy": "equity"}
    second = {**first, "symbol": "SECOND"}
    attempts = [{"symbol": "FIRST", "error": "HTTP 404", "collected_at_utc": "2026-11-18T08:00:00Z"}]
    cohort = tmp_path / "cohort.json"
    reviewed = tmp_path / "reviewed.json"
    prepared = tmp_path / "prepared.json"
    cohort.write_text(json.dumps({"listings": [first, second]}), encoding="utf-8")
    reviewed.write_text(json.dumps({
        "records": [{"listing": second, "annual_fees": [{"metric": "ter", "raw_percent": "0.12"}]}],
        "attempts": attempts,
    }), encoding="utf-8")
    scripts = Path(__file__).parents[1] / "scripts"
    subprocess.run([sys.executable, str(scripts / "prepare_snapshot.py"), str(cohort), str(reviewed),
                    "--output", str(prepared)], check=True)
    result = json.loads(prepared.read_text(encoding="utf-8"))
    assert result["requested_listing_count"] == 2 and result["reviewed_listing_count"] == 1
    assert result["attempts"] == attempts
    assert result["records"][0] == {"listing": first, "review_status": "missing"}
    assert result["records"][1]["annual_fees"][0] == {
        "metric": "ter", "raw_percent": "0.12", "annual_basis_points": "12.00",
    }
    screen = tmp_path / "screen.md"
    subprocess.run([sys.executable, str(scripts / "screen_etfs.py"), str(prepared),
                    "--as-of", "2026-11-18", "--output", str(screen)], check=True)
    assert "**Unknown** 2" in screen.read_text(encoding="utf-8")
