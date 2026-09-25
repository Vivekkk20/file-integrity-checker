"""
Core engine modules for the File Integrity Checker.
Provides hashing, safe file handling, database management, comparison, and reporting.
"""

from .hasher import calculate_sha256
from .file_handler import get_file_metadata, validate_file_path
from .database import DatabaseManager
from .comparator import FileComparator, VerificationResult, VerificationStatus
from .reporter import ReportGenerator

__all__ = [
    "calculate_sha256",
    "get_file_metadata",
    "validate_file_path",
    "DatabaseManager",
    "FileComparator",
    "VerificationResult",
    "VerificationStatus",
    "ReportGenerator",
]
