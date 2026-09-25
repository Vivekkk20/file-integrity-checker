"""
Unit tests for the SHA-256 Hashing Engine.
"""

import hashlib
import os
import tempfile
from pathlib import Path
import pytest

from core.hasher import calculate_sha256, HashCalculationError


class TestHasher:
    """Test suite for calculate_sha256."""

    def test_known_empty_file_hash(self, tmp_path):
        """Standard NIST test vector: empty file SHA-256."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_bytes(b"")

        expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        actual_hash = calculate_sha256(empty_file)

        assert actual_hash == expected_hash

    def test_known_content_hash(self, tmp_path):
        """Test SHA-256 calculation on known ASCII content."""
        sample_file = tmp_path / "sample.txt"
        content = b"The quick brown fox jumps over the lazy dog"
        sample_file.write_bytes(content)

        expected = hashlib.sha256(content).hexdigest()
        actual = calculate_sha256(sample_file)

        assert actual == expected

    def test_same_file_produces_identical_hash(self, tmp_path):
        """Ensure hashing is deterministic across multiple calls."""
        target = tmp_path / "data.bin"
        target.write_bytes(os.urandom(1024))

        hash1 = calculate_sha256(target)
        hash2 = calculate_sha256(target)

        assert hash1 == hash2

    def test_modified_file_produces_different_hash(self, tmp_path):
        """Verify the avalanche effect: single-bit modification completely changes hash."""
        target = tmp_path / "immutable.txt"
        target.write_bytes(b"Original trusted payload data.")

        baseline_hash = calculate_sha256(target)

        # Alter single character
        target.write_bytes(b"Original trusted payload data!")
        modified_hash = calculate_sha256(target)

        assert baseline_hash != modified_hash

    def test_chunking_with_large_payload(self, tmp_path):
        """Test file larger than default chunk buffer (e.g. 200KB with 16KB chunks)."""
        target = tmp_path / "large.dat"
        data = b"ABCDEF1234567890" * 12800  # ~204,800 bytes
        target.write_bytes(data)

        expected = hashlib.sha256(data).hexdigest()
        actual = calculate_sha256(target, chunk_size=16384)

        assert actual == expected

    def test_missing_file_raises_filenotfound(self, tmp_path):
        """Verify FileNotFoundError is raised when file does not exist."""
        non_existent = tmp_path / "does_not_exist.txt"
        with pytest.raises(FileNotFoundError):
            calculate_sha256(non_existent)

    def test_directory_raises_isadirectoryerror(self, tmp_path):
        """Verify IsADirectoryError is raised when given a directory."""
        folder = tmp_path / "subfolder"
        folder.mkdir()
        with pytest.raises(IsADirectoryError):
            calculate_sha256(folder)
