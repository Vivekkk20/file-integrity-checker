"""
Standalone Programmatic End-to-End Workflow Verification Script.
Executes:
Create test file -> Create baseline -> Verify unchanged (MATCHED)
-> Modify file -> Verify (MODIFIED) -> Delete file -> Verify (MISSING).
"""

import sys
import tempfile
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.database import DatabaseManager
from core.comparator import FileComparator, VerificationStatus
from core.hasher import calculate_sha256
from core.reporter import ReportGenerator

def main():
    print("===================================================================")
    print("     PROGRAMMATIC END-TO-END VERIFICATION WORKFLOW RUNNER         ")
    print("===================================================================")

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        tmp_path = Path(temp_dir)
        db_path = tmp_path / "standalone_verify.db"
        db = DatabaseManager(str(db_path))
        comparator = FileComparator(db)

        # -------------------------------------------------------------
        # STEP 1: Create test file
        # -------------------------------------------------------------
        test_file = tmp_path / "system_auth.conf"
        initial_data = "ALLOW_ANONYMOUS=false\nSESSION_TIMEOUT=900\nCIPHER_SUITE=TLS_AES_256_GCM_SHA384\n"
        test_file.write_text(initial_data, encoding="utf-8")
        canonical_path = str(test_file.resolve())
        print(f"\n[STEP 1] Created test file: {test_file.name}")
        print(f"         Path : {canonical_path}")
        print(f"         Size : {len(initial_data)} bytes")

        # -------------------------------------------------------------
        # STEP 2: Create baseline
        # -------------------------------------------------------------
        initial_hash = calculate_sha256(canonical_path)
        baseline = db.save_baseline(
            file_name=test_file.name,
            file_path=canonical_path,
            sha256=initial_hash,
            file_size=len(initial_data),
        )
        print(f"\n[STEP 2] Established baseline in SQLite:")
        print(f"         Baseline ID : {baseline['id']}")
        print(f"         SHA-256     : {baseline['sha256']}")
        print(f"         Timestamp   : {baseline['created_at']}")

        # -------------------------------------------------------------
        # STEP 3: Verify unchanged file -> MATCHED
        # -------------------------------------------------------------
        res_matched = comparator.verify_file(canonical_path, record_in_history=True)
        print(f"\n[STEP 3] Verifying unchanged file against baseline:")
        print(f"         Status Verdict : {res_matched.status}")
        print(f"         Baseline Hash  : {res_matched.baseline_hash}")
        print(f"         Current Hash   : {res_matched.current_hash}")
        print(f"         Explanation    : {res_matched.explanation[:60]}...")
        assert res_matched.status == VerificationStatus.MATCHED.value, f"Expected MATCHED, got {res_matched.status}"
        assert res_matched.baseline_hash == res_matched.current_hash
        assert "A MATCHED result confirms" in res_matched.advisory
        print("         >>> CONFIRMED: MATCHED")
        print(f"         Advisory Check : PASSED (MATCHED advisory active)")

        # -------------------------------------------------------------
        # STEP 4: Modify file
        # -------------------------------------------------------------
        tampered_data = "ALLOW_ANONYMOUS=true\nSESSION_TIMEOUT=9999\nCIPHER_SUITE=TLS_AES_256_GCM_SHA384\n"
        test_file.write_text(tampered_data, encoding="utf-8")
        new_hash = calculate_sha256(canonical_path)
        print(f"\n[STEP 4] Modified file content (unauthorized tampering simulated):")
        print(f"         New content SHA-256 : {new_hash}")
        assert new_hash != initial_hash, "Hash should change after modification"

        # -------------------------------------------------------------
        # STEP 5: Verify again -> MODIFIED
        # -------------------------------------------------------------
        res_modified = comparator.verify_file(canonical_path, record_in_history=True)
        print(f"\n[STEP 5] Verifying altered file against baseline:")
        print(f"         Status Verdict : {res_modified.status}")
        print(f"         Baseline Hash  : {res_modified.baseline_hash}")
        print(f"         Current Hash   : {res_modified.current_hash}")
        print(f"         Explanation    : {res_modified.explanation[:60]}...")
        assert res_modified.status == VerificationStatus.MODIFIED.value, f"Expected MODIFIED, got {res_modified.status}"
        assert res_modified.baseline_hash != res_modified.current_hash
        assert "SECURITY ALERT" in res_modified.advisory
        assert "A MATCHED result confirms" not in res_modified.advisory
        print("         >>> CONFIRMED: MODIFIED")
        print(f"         Advisory Check : PASSED (MODIFIED advisory active, zero MATCHED text)")

        # -------------------------------------------------------------
        # STEP 6: Delete test file
        # -------------------------------------------------------------
        test_file.unlink()
        print(f"\n[STEP 6] Deleted file from disk: {test_file.name}")
        assert not test_file.exists(), "File should be deleted"

        # -------------------------------------------------------------
        # STEP 7: Verify again -> MISSING
        # -------------------------------------------------------------
        res_missing = comparator.verify_file(canonical_path, record_in_history=True)
        print(f"\n[STEP 7] Verifying deleted file against baseline:")
        print(f"         Status Verdict : {res_missing.status}")
        print(f"         Baseline Hash  : {res_missing.baseline_hash}")
        print(f"         Current Hash   : {res_missing.current_hash}")
        print(f"         Explanation    : {res_missing.explanation}")
        assert res_missing.status == VerificationStatus.MISSING.value, f"Expected MISSING, got {res_missing.status}"
        assert res_missing.current_hash is None
        assert "FILE ABSENT" in res_missing.advisory
        assert "A MATCHED result confirms" not in res_missing.advisory
        print("         >>> CONFIRMED: MISSING")
        print(f"         Advisory Check : PASSED (MISSING advisory active, zero MATCHED text)")

        # -------------------------------------------------------------
        # STEP 8: Verify a file with no baseline -> ERROR / NO_BASELINE
        # -------------------------------------------------------------
        unbaselined_file = tmp_path / "never_baselined.cfg"
        unbaselined_file.write_text("unregistered config")
        res_no_base = comparator.verify_file(str(unbaselined_file.resolve()), record_in_history=True)
        print(f"\n[STEP 8] Verifying file with NO baseline:")
        print(f"         Status Verdict : {res_no_base.status}")
        print(f"         Explanation    : {res_no_base.explanation}")
        print(f"         Advisory       : {res_no_base.advisory[:70]}...")
        assert res_no_base.status == VerificationStatus.ERROR.value
        assert "No baseline found" in res_no_base.explanation
        assert "NO BASELINE ESTABLISHED" in res_no_base.advisory
        assert "A MATCHED result confirms" not in res_no_base.advisory
        assert "MATCHED" not in res_no_base.advisory
        print("         >>> CONFIRMED: ERROR / NO_BASELINE")
        print(f"         Advisory Check : PASSED (NO_BASELINE advisory active, zero MATCHED text)")

        # -------------------------------------------------------------
        # Audit Trail Check
        # -------------------------------------------------------------
        history = db.get_history()
        print(f"\n[AUDIT] Verified SQLite Audit Trail Log:")
        print(f"         Total records logged: {len(history)}")
        for r in history:
            print(f"         - Record #{r['id']}: [{r['status']:<8}] {r['file_name']} at {r['verified_at'][:19]}")

        assert len(history) == 4
        assert history[0]["status"] == "ERROR"
        assert history[1]["status"] == "MISSING"
        assert history[2]["status"] == "MODIFIED"
        assert history[3]["status"] == "MATCHED"

    print("\n===================================================================")
    print("   COMPLETE 8-STEP WORKFLOW & ADVISORY ISOLATION VERIFIED!        ")
    print("===================================================================")

if __name__ == "__main__":
    main()
