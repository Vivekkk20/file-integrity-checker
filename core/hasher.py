"""
SHA-256 Hashing Engine.
Calculates cryptographic checksums using Python's hashlib in streaming chunks
to ensure memory safety with arbitrarily large files.
"""

import hashlib
import os
from typing import Union
from pathlib import Path


class HashCalculationError(Exception):
    """Raised when SHA-256 hash generation fails."""
    pass


def calculate_sha256(file_path: Union[str, Path], chunk_size: int = 65536) -> str:
    """
    Calculate the SHA-256 hexadecimal digest for a given file.

    Args:
        file_path: Path to the target file.
        chunk_size: Size of data blocks to read into memory per iteration (default 64KB).

    Returns:
        Hexadecimal string representation of the SHA-256 hash (64 characters).

    Raises:
        FileNotFoundError: If the target file does not exist.
        IsADirectoryError: If the target path is a directory.
        PermissionError: If read permissions are lacking.
        HashCalculationError: For any other I/O or operating system errors.
    """
    path = Path(file_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.is_dir():
        raise IsADirectoryError(f"Target path is a directory, not a regular file: {path}")

    hasher = hashlib.sha256()

    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
    except PermissionError as pe:
        raise PermissionError(f"Permission denied accessing file: {path}") from pe
    except OSError as oe:
        raise HashCalculationError(f"Operating system error reading file {path}: {oe}") from oe
    except Exception as e:
        raise HashCalculationError(f"Unexpected error calculating SHA-256 for {path}: {e}") from e

    return hasher.hexdigest().lower()
