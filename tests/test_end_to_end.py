"""
End-to-End Workflow Verification Test.
Executes the complete lifecycle prescribed in Section 15 of the Master Execution Prompt:
Create file -> Generate baseline -> Verify (MATCHED) -> Modify -> Verify (MODIFIED) -> Delete -> Verify (MISSING).
"""

from pathlib import Path
from core.database import DatabaseManager
from core.comparator import FileComparator, VerificationStatus
from core.hasher import calculate_sha256
from core.reporter import ReportGenerator


def test_master_end_to_end_workflow(tmp_path):
    # 1. Initialize isolated database and comparator
    db_file = tmp_path / "e2e_integrity.db"
    db = DatabaseManager(db_path=str(db_file))
    comparator = FileComparator(db)

    # 2. Step 1: Create test file
    test_file = tmp_path / "critical_asset.conf"
    initial_content = "server_port=8443\nssl_enabled=true\nallow_root=false\n"
    test_file.write_text(initial_content)
    file_path_str = str(test_file.resolve())

    # 3. Step 2: Generate baseline
    initial_hash = calculate_sha256(file_path_str)
    baseline_record = db.save_baseline(
        file_name=test_file.name,
        file_path=file_path_str,
        sha256=initial_hash,
        file_size=len(initial_content),
    )
    assert baseline_record["id"] is not None
    assert baseline_record["sha256"] == initial_hash

    # 4. Step 3: Verify unchanged file -> Expect MATCHED
    result_matched = comparator.verify_file(file_path_str, record_in_history=True)
    assert result_matched.status == VerificationStatus.MATCHED.value
    assert result_matched.baseline_hash == initial_hash
    assert result_matched.current_hash == initial_hash
    assert "matches the trusted baseline" in result_matched.explanation
    assert "A MATCHED result confirms" in result_matched.advisory

    # 5. Step 4: Modify test file
    tampered_content = "server_port=8443\nssl_enabled=false\nallow_root=true\n"
    test_file.write_text(tampered_content)

    # 6. Step 5: Verify again -> Expect MODIFIED
    result_modified = comparator.verify_file(file_path_str, record_in_history=True)
    assert result_modified.status == VerificationStatus.MODIFIED.value
    assert result_modified.baseline_hash == initial_hash
    assert result_modified.current_hash != initial_hash
    assert "breach detected" in result_modified.explanation.lower()
    assert "SECURITY ALERT" in result_modified.advisory
    assert "A MATCHED result confirms" not in result_modified.advisory

    # 7. Step 6: Delete test file
    test_file.unlink()
    assert not test_file.exists()

    # 8. Step 7: Verify again -> Expect MISSING
    result_missing = comparator.verify_file(file_path_str, record_in_history=True)
    assert result_missing.status == VerificationStatus.MISSING.value
    assert result_missing.current_hash is None
    assert "missing" in result_missing.explanation.lower()
    assert "FILE ABSENT" in result_missing.advisory
    assert "A MATCHED result confirms" not in result_missing.advisory

    # 9. Step 8: Verify a file with no baseline -> Expect ERROR / NO_BASELINE
    unbaselined_file = tmp_path / "unregistered_asset.txt"
    unbaselined_file.write_text("unregistered file without any baseline")
    result_no_base = comparator.verify_file(str(unbaselined_file.resolve()), record_in_history=True)
    assert result_no_base.status == VerificationStatus.ERROR.value
    assert "No baseline found" in result_no_base.explanation
    assert "NO BASELINE ESTABLISHED" in result_no_base.advisory
    assert "A MATCHED result confirms" not in result_no_base.advisory
    assert "MATCHED" not in result_no_base.advisory

    # 10. Verify History Log Integrity
    history = db.get_history()
    assert len(history) == 4
    # Most recent first: ERROR (no baseline), MISSING, MODIFIED, MATCHED
    assert history[0]["status"] == VerificationStatus.ERROR.value
    assert history[1]["status"] == VerificationStatus.MISSING.value
    assert history[2]["status"] == VerificationStatus.MODIFIED.value
    assert history[3]["status"] == VerificationStatus.MATCHED.value

    # 11. Verify Report Generation for all events
    report_text_matched = ReportGenerator.to_text_report(result_matched)
    assert "VERDICT STATUS     : MATCHED" in report_text_matched
    assert "A MATCHED status proves data integrity" in report_text_matched

    report_text_no_base = ReportGenerator.to_text_report(result_no_base)
    assert "VERDICT STATUS     : ERROR" in report_text_no_base
    assert "NO BASELINE" in report_text_no_base
    assert "A MATCHED status proves" not in report_text_no_base

    report_json = ReportGenerator.to_json_report(result_modified)
    assert '"status": "MODIFIED"' in report_json
    assert "Integrity breach" in report_json
