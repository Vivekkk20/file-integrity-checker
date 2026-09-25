"""
Unit tests for the Safe File Handler module.
"""

from pathlib import Path
from core.file_handler import validate_file_path, get_file_metadata, format_bytes_human


class TestFileHandler:
    """Test suite for file validation and metadata inspection."""

    def test_format_bytes_human(self):
        assert format_bytes_human(0) == "0 B"
        assert format_bytes_human(512) == "512 B"
        assert format_bytes_human(1024) == "1.00 KB"
        assert format_bytes_human(1024 * 1024) == "1.00 MB"
        assert format_bytes_human(1024 * 1024 * 1024 * 2) == "2.00 GB"

    def test_validate_path_valid(self, tmp_path):
        sample = tmp_path / "valid.txt"
        sample.write_text("ok")

        is_valid, err, resolved = validate_file_path(str(sample))
        assert is_valid is True
        assert err is None
        assert resolved == sample.resolve()

    def test_validate_path_strips_quotes(self, tmp_path):
        sample = tmp_path / "quoted.txt"
        sample.write_text("ok")

        is_valid, err, resolved = validate_file_path(f'"{sample}"')
        assert is_valid is True
        assert resolved == sample.resolve()

    def test_validate_path_null_byte_rejected(self):
        is_valid, err, resolved = validate_file_path("file\x00malicious.txt")
        assert is_valid is False
        assert "Null byte" in err

    def test_validate_path_empty_rejected(self):
        is_valid, err, resolved = validate_file_path("   ")
        assert is_valid is False
        assert "empty" in err.lower()

    def test_get_metadata_existing_file(self, tmp_path):
        target = tmp_path / "metadata_test.bin"
        target.write_bytes(b"A" * 2048)

        meta = get_file_metadata(str(target))
        assert meta["exists"] is True
        assert meta["is_file"] is True
        assert meta["is_readable"] is True
        assert meta["file_size"] == 2048
        assert meta["file_name"] == "metadata_test.bin"
        assert meta["error"] is None

    def test_get_metadata_missing_file(self, tmp_path):
        missing = tmp_path / "ghost.txt"
        meta = get_file_metadata(str(missing))

        assert meta["exists"] is False
        assert meta["is_file"] is False
        assert meta["error"] is not None
        assert "does not exist" in meta["error"]

    def test_get_metadata_directory(self, tmp_path):
        folder = tmp_path / "docs_folder"
        folder.mkdir()

        meta = get_file_metadata(str(folder))
        assert meta["exists"] is True
        assert meta["is_file"] is False
        assert "directory" in meta["error"].lower()
