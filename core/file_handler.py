"""
Safe File Handler Module.
Validates file paths, guards against path injection, checks accessibility,
and extracts file metadata without executing any untrusted data.
"""

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Tuple, Optional


def format_bytes_human(size_in_bytes: int) -> str:
    """Format byte count into human-readable representation."""
    if size_in_bytes < 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_in_bytes)
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}" if unit_index > 0 else f"{int(size)} {units[unit_index]}"


def validate_file_path(raw_path: str) -> Tuple[bool, Optional[str], Optional[Path]]:
    """
    Validate that an input path string is safe, non-null, and resolvable.

    Args:
        raw_path: Untrusted string input representing a file path.

    Returns:
        (is_valid, error_message, resolved_path)
    """
    if not raw_path or not isinstance(raw_path, str):
        return False, "File path cannot be empty or non-string.", None

    # Guard against null-byte injection
    if "\x00" in raw_path:
        return False, "Null byte detected in path.", None

    trimmed_path = raw_path.strip()
    # Strip any enclosing quotes from command-line or file drag-and-drop
    if (trimmed_path.startswith('"') and trimmed_path.endswith('"')) or (
        trimmed_path.startswith("'") and trimmed_path.endswith("'")
    ):
        trimmed_path = trimmed_path[1:-1].strip()

    if not trimmed_path:
        return False, "File path cannot be empty.", None

    try:
        path = Path(trimmed_path).resolve()
    except Exception as e:
        return False, f"Invalid file path syntax: {e}", None

    return True, None, path


def get_file_metadata(file_path: str) -> Dict[str, Any]:
    """
    Inspect a file and return comprehensive metadata safely.

    Args:
        file_path: Raw path to the target file.

    Returns:
        Dictionary containing metadata:
        - file_name: Name of file
        - file_path: Canonical resolved absolute path string
        - file_size: Size in bytes (integer)
        - file_size_human: Human-readable size string
        - exists: Whether the file exists
        - is_file: Whether it is a regular file
        - is_readable: Whether read permission is granted
        - last_modified: ISO-8601 UTC timestamp of last modification
        - error: Error description if inaccessible, else None
    """
    is_valid, err, path = validate_file_path(file_path)
    if not is_valid or path is None:
        return {
            "file_name": os.path.basename(file_path) if file_path else "Unknown",
            "file_path": str(file_path) if file_path else "",
            "file_size": 0,
            "file_size_human": "0 B",
            "exists": False,
            "is_file": False,
            "is_readable": False,
            "last_modified": None,
            "error": err or "Invalid file path.",
        }

    canonical_path_str = str(path)
    file_name = path.name

    if not path.exists():
        return {
            "file_name": file_name,
            "file_path": canonical_path_str,
            "file_size": 0,
            "file_size_human": "0 B",
            "exists": False,
            "is_file": False,
            "is_readable": False,
            "last_modified": None,
            "error": f"File does not exist on disk: {canonical_path_str}",
        }

    if path.is_dir():
        return {
            "file_name": file_name,
            "file_path": canonical_path_str,
            "file_size": 0,
            "file_size_human": "0 B",
            "exists": True,
            "is_file": False,
            "is_readable": False,
            "last_modified": None,
            "error": f"Path is a directory, not a regular file: {canonical_path_str}",
        }

    # Verify read accessibility
    is_readable = os.access(path, os.R_OK)
    if not is_readable:
        return {
            "file_name": file_name,
            "file_path": canonical_path_str,
            "file_size": 0,
            "file_size_human": "0 B",
            "exists": True,
            "is_file": True,
            "is_readable": False,
            "last_modified": None,
            "error": f"Read permission denied: {canonical_path_str}",
        }

    try:
        stat_info = path.stat()
        mtime = datetime.fromtimestamp(stat_info.st_mtime, tz=timezone.utc).isoformat()
        return {
            "file_name": file_name,
            "file_path": canonical_path_str,
            "file_size": stat_info.st_size,
            "file_size_human": format_bytes_human(stat_info.st_size),
            "exists": True,
            "is_file": True,
            "is_readable": True,
            "last_modified": mtime,
            "error": None,
        }
    except Exception as e:
        return {
            "file_name": file_name,
            "file_path": canonical_path_str,
            "file_size": 0,
            "file_size_human": "0 B",
            "exists": True,
            "is_file": True,
            "is_readable": False,
            "last_modified": None,
            "error": f"Failed to read file stats: {e}",
        }
