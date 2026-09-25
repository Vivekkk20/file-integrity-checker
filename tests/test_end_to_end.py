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

    # 5. Step 4: Modify test file
    tampered_content = "server_port=8443\nssl_enabled=false\nallow_root=true\n"
    test_file.write_text(tampered_content)

    # 6. Step 5: Verify again -> Expect MODIFIED
    result_modified = comparator.verify_file(file_path_str, record_in_history=True)
    assert result_modified.status == VerificationStatus.MODIFIED.value
    assert result_modified.baseline_hash == initial_hash
    assert result_modified.current_hash != initial_hash
    assert "breach detected" in result_modified.explanation.lower()

    # 7. Step 6: Delete test file
    test_file.unlink()
    assert not test_file.exists()

    # 8. Step 7: Verify again -> Expect MISSING
    result_missing = comparator.verify_file(file_path_str, record_in_history=True)
    assert result_missing.status == VerificationStatus.MISSING.value
    assert result_missing.current_hash is None
    assert "missing" in result_missing.explanation.lower()

    # 9. Verify History Log Integrity
    history = db.get_history()
    assert len(history) == 3
    # Most recent first: MISSING, MODIFIED, MATCHED
    assert history[0]["status"] == VerificationStatus.MISSING.value
    assert history[1]["status"] == VerificationStatus.MODIFIED.value
    assert history[2]["status"] == VerificationStatus.MATCHED.value

    # 10. Verify Report Generation for all 3 events
    report_text = ReportGenerator.to_text_report(result_matched)
    assert "VERDICT STATUS     : MATCHED" in report_text

    report_json = ReportGenerator.to_json_report(result_modified)
    assert '"status": "MODIFIED"' in report_json
