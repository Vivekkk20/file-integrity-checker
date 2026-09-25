"""
Unit tests for the Report Generator module.
"""

import json
from core.reporter import ReportGenerator
from core.comparator import VerificationResult


class TestReporter:
    """Test suite for security audit report generation."""

    def test_to_text_report_contains_key_elements(self):
        result = VerificationResult(
            status="MATCHED",
            file_name="policy.pdf",
            file_path="C:/docs/policy.pdf",
            baseline_hash="aaaa" * 16,
            current_hash="aaaa" * 16,
            baseline_created_at="2026-09-25T12:00:00Z",
            verified_at="2026-09-25T14:30:00Z",
            explanation="Exact match against baseline.",
            details="Cryptographic digest match.",
        )

        report = ReportGenerator.to_text_report(result)
        assert "FILE INTEGRITY VERIFICATION REPORT" in report
        assert "VERDICT STATUS     : MATCHED" in report
        assert "TARGET FILE        : policy.pdf" in report
        assert "CYBERSECURITY ADVISORY NOTE:" in report

    def test_to_json_report_is_valid_json(self):
        data = {
            "status": "MODIFIED",
            "file_name": "binary.exe",
            "file_path": "C:/bin/binary.exe",
            "baseline_hash": "1111" * 16,
            "current_hash": "2222" * 16,
            "verified_at": "2026-09-25T15:00:00Z",
        }

        json_str = ReportGenerator.to_json_report(data)
        parsed = json.loads(json_str)

        assert parsed["report_type"] == "file_integrity_verification"
        assert parsed["data"]["status"] == "MODIFIED"
        assert "security_disclaimer" in parsed

    def test_to_history_summary_text(self):
        records = [
            {"id": 1, "status": "MATCHED", "verified_at": "2026-09-25T10:00:00Z", "file_name": "f1.txt", "file_path": "C:/f1.txt"},
            {"id": 2, "status": "MODIFIED", "verified_at": "2026-09-25T11:00:00Z", "file_name": "f2.txt", "file_path": "C:/f2.txt"},
        ]

        summary = ReportGenerator.to_history_summary_text(records)
        assert "VERIFICATION AUDIT HISTORY SUMMARY" in summary
        assert "MATCHED" in summary
        assert "MODIFIED" in summary
        assert "Total audit entries: 2" in summary
