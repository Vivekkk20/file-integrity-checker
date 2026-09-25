"""
Report Generator Module.
Generates human-readable plain text and structured JSON integrity audit reports
from verification results or historical log records.
"""

import json
from typing import Dict, Any, List, Union
from .comparator import VerificationResult


class ReportGenerator:
    """Produces security audit reports for file integrity events."""

    @staticmethod
    def to_text_report(data: Union[VerificationResult, Dict[str, Any]]) -> str:
        """
        Format a single verification result into a structured text audit report.
        """
        if isinstance(data, VerificationResult):
            info = data.to_dict()
        else:
            info = dict(data)

        status = info.get("status", "UNKNOWN")
        file_name = info.get("file_name", "N/A")
        file_path = info.get("file_path", "N/A")
        baseline_hash = info.get("baseline_hash") or "NONE"
        current_hash = info.get("current_hash") or "NOT_CALCULATED"
        baseline_created = info.get("baseline_created_at") or "N/A"
        verified_at = info.get("verified_at", "N/A")
        explanation = info.get("explanation", info.get("details", "N/A"))
        details = info.get("details", "")

        divider = "=" * 70
        sub_divider = "-" * 70

        lines = [
            divider,
            "               FILE INTEGRITY VERIFICATION REPORT",
            divider,
            f"VERDICT STATUS     : {status}",
            f"TARGET FILE        : {file_name}",
            f"CANONICAL PATH     : {file_path}",
            f"VERIFICATION TIME  : {verified_at}",
            sub_divider,
            "CRYPTOGRAPHIC HASH COMPARISON (SHA-256):",
            f"  Trusted Baseline : {baseline_hash}",
            f"  Current File     : {current_hash}",
            f"  Baseline Created : {baseline_created}",
            sub_divider,
            "ANALYSIS & EXPLANATION:",
            f"  {explanation}",
        ]

        if details and details != explanation:
            lines.append(f"  Technical Context: {details}")

        lines.extend([
            sub_divider,
            "CYBERSECURITY ADVISORY NOTE:",
            "  * SHA-256 verification proves content matches the trusted baseline.",
            "  * A MATCHED status proves integrity, not absence of malware.",
            "  * Cryptographic hashing is a one-way digest, distinct from encryption.",
            divider,
        ])

        return "\n".join(lines)

    @staticmethod
    def to_json_report(data: Union[VerificationResult, Dict[str, Any]], indent: int = 2) -> str:
        """
        Serialize verification result into structured JSON.
        """
        if isinstance(data, VerificationResult):
            info = data.to_dict()
        else:
            info = dict(data)

        payload = {
            "report_type": "file_integrity_verification",
            "version": "1.0",
            "data": info,
            "security_disclaimer": (
                "SHA-256 verification confirms cryptographic consistency against a stored baseline. "
                "It does not assess malware payload or executable intent."
            ),
        }
        return json.dumps(payload, indent=indent)

    @staticmethod
    def to_history_summary_text(records: List[Dict[str, Any]]) -> str:
        """
        Format a list of verification history records into a tabular summary report.
        """
        divider = "=" * 88
        sub_divider = "-" * 88

        lines = [
            divider,
            "                     VERIFICATION AUDIT HISTORY SUMMARY",
            divider,
            f"{'ID':<6} {'STATUS':<10} {'TIMESTAMP':<24} {'FILE':<20} {'PATH'}",
            sub_divider,
        ]

        if not records:
            lines.append("No verification records logged.")
        else:
            for r in records:
                r_id = str(r.get("id", "-"))
                status = str(r.get("status", "UNKNOWN"))
                ts = str(r.get("verified_at", ""))[:19]
                fname = str(r.get("file_name", ""))[:18]
                fpath = str(r.get("file_path", ""))
                if len(fpath) > 30:
                    fpath = "..." + fpath[-27:]
                lines.append(f"{r_id:<6} {status:<10} {ts:<24} {fname:<20} {fpath}")

        lines.append(divider)
        lines.append(f"Total audit entries: {len(records)}")
        return "\n".join(lines)
