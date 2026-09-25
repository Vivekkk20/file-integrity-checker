"""
Unit tests for the File Comparator engine.
"""

import pytest
from core.database import DatabaseManager
from core.comparator import FileComparator, VerificationStatus
from core.hasher import calculate_sha256


class TestComparator:
    """Test suite for deterministic comparison logic."""

    @pytest.fixture
    def db(self, tmp_path):
        db_file = tmp_path / "test_comparator.db"
        return DatabaseManager(db_path=str(db_file))

    def test_evaluate_status_matched(self):
        hash_val = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        status = FileComparator.evaluate_status(
            baseline_hash=hash_val,
            current_hash=hash_val.upper(),  # Test case-insensitivity
            file_exists=True,
        )
        assert status == VerificationStatus.MATCHED

    def test_evaluate_status_modified(self):
        h1 = "aaaa" * 16
        h2 = "bbbb" * 16
        status = FileComparator.evaluate_status(
            baseline_hash=h1,
            current_hash=h2,
            file_exists=True,
        )
        assert status == VerificationStatus.MODIFIED

    def test_evaluate_status_missing(self):
        status = FileComparator.evaluate_status(
            baseline_hash="aaaa" * 16,
            current_hash=None,
            file_exists=False,
        )
        assert status == VerificationStatus.MISSING

    def test_evaluate_status_error_on_message(self):
        status = FileComparator.evaluate_status(
            baseline_hash="aaaa" * 16,
            current_hash="aaaa" * 16,
            file_exists=True,
            error_message="Disk failure",
        )
        assert status == VerificationStatus.ERROR

    def test_verify_file_lifecycle(self, db, tmp_path):
        """Test full verification flow with real filesystem operations."""
        comparator = FileComparator(db)

        target_file = tmp_path / "document.txt"
        target_file.write_text("Confidential Draft v1")
        path_str = str(target_file.resolve())

        # 1. Verification without baseline -> ERROR
        res_no_baseline = comparator.verify_file(path_str)
        assert res_no_baseline.status == VerificationStatus.ERROR.value
        assert "No baseline found" in res_no_baseline.explanation

        # 2. Establish Baseline
        hash_v1 = calculate_sha256(path_str)
        db.save_baseline("document.txt", path_str, hash_v1, len("Confidential Draft v1"))

        # 3. Verify unchanged -> MATCHED
        res_matched = comparator.verify_file(path_str)
        assert res_matched.status == VerificationStatus.MATCHED.value
        assert res_matched.baseline_hash == hash_v1
        assert res_matched.current_hash == hash_v1
        assert res_matched.history_id is not None

        # 4. Modify file -> MODIFIED
        target_file.write_text("Tampered Content v2")
        res_modified = comparator.verify_file(path_str)
        assert res_modified.status == VerificationStatus.MODIFIED.value
        assert res_modified.current_hash != hash_v1

        # 5. Delete file -> MISSING
        target_file.unlink()
        res_missing = comparator.verify_file(path_str)
        assert res_missing.status == VerificationStatus.MISSING.value
        assert res_missing.current_hash is None
