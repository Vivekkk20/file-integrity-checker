"""
Unit tests for the SQLite Database Manager.
"""

import pytest
from core.database import DatabaseManager


class TestDatabaseManager:
    """Test suite for SQLite baseline and verification history persistence."""

    @pytest.fixture
    def db(self, tmp_path):
        db_file = tmp_path / "test_integrity.db"
        return DatabaseManager(db_path=str(db_file))

    def test_save_and_retrieve_baseline(self, db, tmp_path):
        test_file = tmp_path / "app.conf"
        test_file.write_text("setting=1")

        canonical_path = str(test_file.resolve())
        sha256 = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

        baseline = db.save_baseline(
            file_name="app.conf",
            file_path=canonical_path,
            sha256=sha256,
            file_size=9,
        )

        assert baseline["id"] is not None
        assert baseline["file_name"] == "app.conf"
        assert baseline["file_path"] == canonical_path
        assert baseline["sha256"] == sha256
        assert baseline["file_size"] == 9

        # Retrieve by path
        fetched = db.get_baseline_by_path(canonical_path)
        assert fetched is not None
        assert fetched["id"] == baseline["id"]
        assert fetched["sha256"] == sha256

        # Retrieve by ID
        fetched_id = db.get_baseline_by_id(baseline["id"])
        assert fetched_id is not None
        assert fetched_id["file_path"] == canonical_path

    def test_baseline_upsert_updates_existing(self, db, tmp_path):
        test_file = tmp_path / "data.csv"
        test_file.write_text("a,b,c")

        path = str(test_file.resolve())
        hash1 = "aaaa" * 16
        hash2 = "bbbb" * 16

        # Initial baseline
        b1 = db.save_baseline("data.csv", path, hash1, 5)
        # Update baseline
        b2 = db.save_baseline("data.csv", path, hash2, 10)

        assert b1["id"] == b2["id"]
        assert b2["sha256"] == hash2
        assert b2["file_size"] == 10

        baselines = db.list_all_baselines()
        assert len(baselines) == 1

    def test_delete_baseline(self, db, tmp_path):
        test_file = tmp_path / "temp.log"
        test_file.write_text("test")

        b = db.save_baseline("temp.log", str(test_file.resolve()), "cccc" * 16, 4)
        assert db.delete_baseline(b["id"]) is True
        assert db.get_baseline_by_id(b["id"]) is None
        assert db.delete_baseline(b["id"]) is False

    def test_update_baseline_last_verified(self, db, tmp_path):
        test_file = tmp_path / "secret.key"
        test_file.write_text("key")
        path = str(test_file.resolve())

        db.save_baseline("secret.key", path, "dddd" * 16, 3)
        assert db.get_baseline_by_path(path)["last_verified_at"] is None

        db.update_baseline_last_verified(path)
        updated = db.get_baseline_by_path(path)
        assert updated["last_verified_at"] is not None

    def test_log_and_filter_verification_history(self, db):
        db.log_verification("f1.txt", "C:/f1.txt", "hashA", "hashA", "MATCHED", "OK")
        db.log_verification("f2.txt", "C:/f2.txt", "hashB", "hashC", "MODIFIED", "Altered")
        db.log_verification("f3.txt", "C:/f3.txt", "hashD", None, "MISSING", "File gone")

        all_history = db.get_history()
        assert len(all_history) == 3

        matched_history = db.get_history(status_filter="MATCHED")
        assert len(matched_history) == 1
        assert matched_history[0]["status"] == "MATCHED"

        modified_history = db.get_history(status_filter="MODIFIED")
        assert len(modified_history) == 1
        assert modified_history[0]["status"] == "MODIFIED"

    def test_dashboard_stats(self, db, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("test")
        db.save_baseline("test.txt", str(f.resolve()), "eeee" * 16, 4)

        db.log_verification("test.txt", str(f.resolve()), "eeee" * 16, "eeee" * 16, "MATCHED")
        db.log_verification("test.txt", str(f.resolve()), "eeee" * 16, "ffff" * 16, "MODIFIED")

        stats = db.get_dashboard_stats()
        assert stats["total_baselines"] == 1
        assert stats["total_verifications"] == 2
        assert stats["matched_count"] == 1
        assert stats["modified_count"] == 1
        assert len(stats["recent_verifications"]) == 2
