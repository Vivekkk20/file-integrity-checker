"""
Comparison Engine Module.
Executes deterministic integrity checks comparing current file state against
trusted baselines and produces standardized statuses: MATCHED, MODIFIED, MISSING, ERROR.
"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional, Dict, Any
from pathlib import Path

from .hasher import calculate_sha256, HashCalculationError
from .file_handler import get_file_metadata, validate_file_path
from .database import DatabaseManager, get_utc_now_iso


class VerificationStatus(str, Enum):
    MATCHED = "MATCHED"
    MODIFIED = "MODIFIED"
    MISSING = "MISSING"
    ERROR = "ERROR"


@dataclass
class VerificationResult:
    """Represents the complete result of an integrity verification check."""
    status: str
    file_name: str
    file_path: str
    baseline_hash: Optional[str]
    current_hash: Optional[str]
    baseline_created_at: Optional[str]
    verified_at: str
    explanation: str
    details: str
    history_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FileComparator:
    """
    Coordinates integrity comparison between stored baselines and current files.
    """

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()

    @staticmethod
    def evaluate_status(
        baseline_hash: Optional[str],
        current_hash: Optional[str],
        file_exists: bool,
        error_message: Optional[str] = None,
    ) -> VerificationStatus:
        """
        Pure deterministic status evaluation based on inputs.
        """
        if error_message:
            return VerificationStatus.ERROR

        if not file_exists:
            return VerificationStatus.MISSING

        if not baseline_hash or not current_hash:
            return VerificationStatus.ERROR

        b_clean = baseline_hash.strip().lower()
        c_clean = current_hash.strip().lower()

        if b_clean == c_clean:
            return VerificationStatus.MATCHED
        else:
            return VerificationStatus.MODIFIED

    def verify_file(
        self,
        file_path: str,
        record_in_history: bool = True,
    ) -> VerificationResult:
        """
        Full verification workflow for a target file path:
        1. Resolve canonical path.
        2. Look up baseline in SQLite database.
        3. Check file existence and accessibility on disk.
        4. Calculate current SHA-256 hash if present.
        5. Evaluate status: MATCHED, MODIFIED, MISSING, ERROR.
        6. Log to verification_history and update last_verified_at.
        """
        now = get_utc_now_iso()
        is_valid, path_err, resolved_path = validate_file_path(file_path)

        if not is_valid or resolved_path is None:
            result = VerificationResult(
                status=VerificationStatus.ERROR.value,
                file_name=Path(file_path).name if file_path else "Unknown",
                file_path=file_path,
                baseline_hash=None,
                current_hash=None,
                baseline_created_at=None,
                verified_at=now,
                explanation="Invalid file path provided.",
                details=path_err or "Invalid file path.",
            )
            if record_in_history:
                record = self.db.log_verification(
                    file_name=result.file_name,
                    file_path=result.file_path,
                    baseline_hash=None,
                    current_hash=None,
                    status=result.status,
                    details=result.details,
                    verified_at=now,
                )
                result.history_id = record.get("id")
            return result

        canonical_path = str(resolved_path)
        file_name = resolved_path.name

        # Query baseline from database
        baseline = self.db.get_baseline_by_path(canonical_path)
        if not baseline:
            result = VerificationResult(
                status=VerificationStatus.ERROR.value,
                file_name=file_name,
                file_path=canonical_path,
                baseline_hash=None,
                current_hash=None,
                baseline_created_at=None,
                verified_at=now,
                explanation="No baseline found for this file. Create a baseline first before verifying.",
                details="Baseline record does not exist in local database.",
            )
            if record_in_history:
                record = self.db.log_verification(
                    file_name=result.file_name,
                    file_path=result.file_path,
                    baseline_hash=None,
                    current_hash=None,
                    status=result.status,
                    details=result.details,
                    verified_at=now,
                )
                result.history_id = record.get("id")
            return result

        baseline_hash = baseline["sha256"]
        baseline_created = baseline["created_at"]

        # Check disk metadata
        meta = get_file_metadata(canonical_path)

        if not meta["exists"]:
            result = VerificationResult(
                status=VerificationStatus.MISSING.value,
                file_name=file_name,
                file_path=canonical_path,
                baseline_hash=baseline_hash,
                current_hash=None,
                baseline_created_at=baseline_created,
                verified_at=now,
                explanation="File is missing. The baseline file cannot be found on disk.",
                details=f"File was expected at '{canonical_path}' but does not exist.",
            )
        elif not meta["is_readable"]:
            result = VerificationResult(
                status=VerificationStatus.ERROR.value,
                file_name=file_name,
                file_path=canonical_path,
                baseline_hash=baseline_hash,
                current_hash=None,
                baseline_created_at=baseline_created,
                verified_at=now,
                explanation="Access error. The file cannot be read due to permission or I/O constraints.",
                details=meta.get("error") or "Permission denied or unreadable file.",
            )
        else:
            try:
                current_hash = calculate_sha256(canonical_path)
                status = self.evaluate_status(baseline_hash, current_hash, file_exists=True)

                if status == VerificationStatus.MATCHED:
                    explanation = (
                        "Integrity verified. Current SHA-256 hash matches the trusted baseline exactly. "
                        "Note: A matching hash confirms the file content is unchanged relative to baseline; "
                        "it does not replace anti-malware inspection."
                    )
                    details = "Exact 256-bit cryptographic digest match."
                else:
                    explanation = (
                        "Integrity breach detected! Current SHA-256 hash differs from the trusted baseline. "
                        "The file content has been altered or replaced since the baseline was established."
                    )
                    details = f"Digest divergence: baseline={baseline_hash[:12]}... vs current={current_hash[:12]}..."

                result = VerificationResult(
                    status=status.value,
                    file_name=file_name,
                    file_path=canonical_path,
                    baseline_hash=baseline_hash,
                    current_hash=current_hash,
                    baseline_created_at=baseline_created,
                    verified_at=now,
                    explanation=explanation,
                    details=details,
                )
            except Exception as e:
                result = VerificationResult(
                    status=VerificationStatus.ERROR.value,
                    file_name=file_name,
                    file_path=canonical_path,
                    baseline_hash=baseline_hash,
                    current_hash=None,
                    baseline_created_at=baseline_created,
                    verified_at=now,
                    explanation="Processing failure during SHA-256 hash calculation.",
                    details=str(e),
                )

        # Log history and update last_verified_at in DB
        if record_in_history:
            record = self.db.log_verification(
                file_name=result.file_name,
                file_path=result.file_path,
                baseline_hash=result.baseline_hash,
                current_hash=result.current_hash,
                status=result.status,
                details=result.details,
                verified_at=now,
            )
            result.history_id = record.get("id")
            self.db.update_baseline_last_verified(canonical_path, now)

        return result
