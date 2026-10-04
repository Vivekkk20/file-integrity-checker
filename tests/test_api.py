"""
Integration tests for the Flask Web Server and REST API endpoints.
"""

import io
import pytest
from web.server import create_app
from core.database import DatabaseManager


class TestAPI:
    """Test suite for web application endpoints."""

    @pytest.fixture
    def app(self, tmp_path):
        db_file = tmp_path / "api_test.db"
        app = create_app(db_path=str(db_file))
        app.config["TESTING"] = True
        return app

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_index_route(self, client):
        res = client.get("/")
        assert res.status_code == 200
        assert b"File Integrity Checker" in res.data
        assert b"SHA-256" in res.data

    def test_api_stats(self, client):
        res = client.get("/api/stats")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert "total_baselines" in data["stats"]
        assert "total_verifications" in data["stats"]

    def test_api_analyze_valid_file(self, client, tmp_path):
        sample = tmp_path / "test_api_sample.txt"
        sample.write_text("API analysis content")

        res = client.post("/api/analyze", json={"file_path": str(sample)})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["sha256"]) == 64
        assert data["metadata"]["file_name"] == "test_api_sample.txt"

    def test_api_analyze_missing_file(self, client, tmp_path):
        ghost = tmp_path / "ghost_file.txt"
        res = client.post("/api/analyze", json={"file_path": str(ghost)})
        assert res.status_code == 404
        data = res.get_json()
        assert data["success"] is False

    def test_api_baseline_and_verify(self, client, tmp_path):
        target = tmp_path / "target.txt"
        target.write_text("Version 1.0 Content")
        path_str = str(target)

        # Create baseline
        res_b = client.post("/api/baseline", json={"file_path": path_str})
        assert res_b.status_code == 200
        data_b = res_b.get_json()
        assert data_b["success"] is True
        assert data_b["baseline"]["file_name"] == "target.txt"

        # Verify unchanged -> MATCHED
        res_v1 = client.post("/api/verify", json={"file_path": path_str})
        assert res_v1.status_code == 200
        data_v1 = res_v1.get_json()
        assert data_v1["success"] is True
        assert data_v1["result"]["status"] == "MATCHED"

        # Modify file and verify -> MODIFIED
        target.write_text("Version 2.0 Content Tampered")
        res_v2 = client.post("/api/verify", json={"file_path": path_str})
        assert res_v2.status_code == 200
        data_v2 = res_v2.get_json()
        assert data_v2["result"]["status"] == "MODIFIED"

        # Check history
        res_h = client.get("/api/history")
        assert res_h.status_code == 200
        data_h = res_h.get_json()
        assert len(data_h["history"]) >= 2

        # Check report
        history_id = data_v1["result"]["history_id"]
        res_rep = client.get(f"/api/report/{history_id}?format=text")
        assert res_rep.status_code == 200
        assert b"FILE INTEGRITY VERIFICATION REPORT" in res_rep.data

    def test_api_upload(self, client):
        data = {
            "file": (io.BytesIO(b"Uploaded binary test content"), "uploaded_test.txt"),
        }
        res = client.post("/api/upload", data=data, content_type="multipart/form-data")
        assert res.status_code == 200
        res_json = res.get_json()
        assert res_json["success"] is True
        assert len(res_json["sha256"]) == 64

    def test_index_contains_theme_and_stitch_components(self, client):
        res = client.get("/")
        assert res.status_code == 200
        html = res.data.decode("utf-8")
        assert 'id="themeSelect"' in html
        assert 'id="btnOpenStitchStudio"' in html
        assert 'id="stitchModal"' in html
        assert 'value="stitch-dark"' in html
        assert 'value="cyber-obsidian"' in html
        assert 'value="midnight-neon"' in html
        assert 'value="clean-slate"' in html
        assert "Google Stitch" in html

    def test_api_verify_file_without_baseline_returns_correct_advisory(self, client, tmp_path):
        target = tmp_path / "orphan_test_file.txt"
        target.write_text("Unbaselined content")
        res = client.post("/api/verify", json={"file_path": str(target)})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        result = data["result"]
        assert result["status"] == "ERROR"
        assert "No baseline found" in result["explanation"]
        assert "NO BASELINE ESTABLISHED" in result["advisory"]
        assert "A MATCHED result confirms" not in result["advisory"]
        assert "MATCHED" not in result["advisory"]

    def test_api_headers_prevent_caching(self, client):
        res = client.get("/")
        assert res.status_code == 200
        cache_control = res.headers.get("Cache-Control", "")
        assert "no-store" in cache_control
        assert "no-cache" in cache_control

    def test_index_html_has_versioned_assets_and_neutral_banner(self, client):
        res = client.get("/")
        html = res.data.decode("utf-8")
        assert 'style.css?v=' in html
        assert 'app.js?v=' in html
        assert 'class="result-banner status-matched"' not in html
        assert 'id="btnDownloadAnalyzedFile"' in html

    def test_api_download_staged_file(self, client):
        file_content = b"Staged audit file content for download test"
        data = {
            "file": (io.BytesIO(file_content), "staged_download_test.bin"),
        }
        res_upload = client.post("/api/upload", data=data, content_type="multipart/form-data")
        assert res_upload.status_code == 200
        meta = res_upload.get_json()["metadata"]
        staged_path = meta["file_path"]

        # Download staged file
        res_down = client.get(f"/api/download?file_path={staged_path}")
        assert res_down.status_code == 200
        assert "attachment" in res_down.headers.get("Content-Disposition", "")
        assert "staged_download_test.bin" in res_down.headers.get("Content-Disposition", "")
        assert res_down.data == file_content

    def test_api_download_baselined_file(self, client, tmp_path):
        target = tmp_path / "baselined_download.txt"
        target_content = "Confidential baseline file payload 12345"
        target.write_text(target_content)
        path_str = str(target)

        # Baseline the file
        res_b = client.post("/api/baseline", json={"file_path": path_str})
        assert res_b.status_code == 200

        # Download the baselined file
        res_down = client.get(f"/api/download?file_path={path_str}")
        assert res_down.status_code == 200
        assert "attachment" in res_down.headers.get("Content-Disposition", "")
        assert "baselined_download.txt" in res_down.headers.get("Content-Disposition", "")
        assert res_down.data.decode("utf-8") == target_content

    def test_api_download_arbitrary_unbaselined_file_blocked(self, client, tmp_path):
        # Create an unbaselined file outside workspace
        foreign_file = tmp_path / "unauthorized_secret.key"
        foreign_file.write_text("Secret key data")
        
        # In a real environment, any file not in baselines or upload folder or workspace is forbidden
        # If tmp_path is outside project workspace and not in baselines, it should be 403
        res = client.get(f"/api/download?file_path={foreign_file}")
        # Not baselined and not in upload_folder
        assert res.status_code == 403
        data = res.get_json()
        assert data["success"] is False
        assert "Access denied" in data["error"]

    def test_api_download_missing_file_returns_404(self, client):
        res = client.get("/api/download?file_path=nonexistent_file_path_1234.txt")
        assert res.status_code in (403, 404)

    def test_api_download_empty_path_returns_400(self, client):
        res = client.get("/api/download?file_path=")
        assert res.status_code == 400

    def test_api_report_download_attachment(self, client, tmp_path):
        target = tmp_path / "report_test.txt"
        target.write_text("Sample file for report download")
        path_str = str(target)

        client.post("/api/baseline", json={"file_path": path_str})
        res_v = client.post("/api/verify", json={"file_path": path_str})
        history_id = res_v.get_json()["result"]["history_id"]

        res_rep = client.get(f"/api/report/{history_id}?download=true")
        assert res_rep.status_code == 200
        assert "attachment" in res_rep.headers.get("Content-Disposition", "")
        assert f"integrity_audit_report_{history_id}.txt" in res_rep.headers.get("Content-Disposition", "")
        assert b"FILE INTEGRITY VERIFICATION REPORT" in res_rep.data

    def test_drag_and_drop_html_and_js_elements(self, client):
        """Verify DOM elements and global drag/drop event prevention scripts exist."""
        res = client.get("/")
        assert res.status_code == 200
        html = res.data.decode("utf-8")
        assert 'id="globalDragOverlay"' in html
        assert 'id="quickFileDropArea"' in html
        assert 'id="fileDropzone"' in html
        assert 'id="anaFileExtBadge"' in html
        assert 'id="anaMetaFileExt"' in html

        # Verify app.js contains global preventDefault for dragover & drop
        res_js = client.get("/static/js/app.js?v=2.7.0")
        assert res_js.status_code == 200
        js_code = res_js.data.decode("utf-8")
        assert "preventDefault()" in js_code
        assert "extractDroppedFile" in js_code
        assert "globalDragOverlay" in js_code

    def test_upload_and_verify_pdf_lifecycle(self, client):
        """
        Verify PDF upload, baseline creation, unchanged verification (MATCHED),
        and modified verification (MODIFIED).
        """
        # 1. Stage initial PDF (raw binary PDF stream)
        pdf_bytes_v1 = b"%PDF-1.4\n%Binary stream integrity target v1.0\n%%EOF"
        data_v1 = {
            "file": (io.BytesIO(pdf_bytes_v1), "security_policy.pdf"),
        }
        res_u1 = client.post("/api/upload", data=data_v1, content_type="multipart/form-data")
        assert res_u1.status_code == 200
        d_u1 = res_u1.get_json()
        assert d_u1["success"] is True
        assert d_u1["metadata"]["file_extension"] == ".pdf"
        assert d_u1["metadata"]["file_name"] == "security_policy.pdf"
        hash_v1 = d_u1["sha256"]
        path_v1 = d_u1["metadata"]["file_path"]

        # 2. Create baseline for PDF
        res_b = client.post("/api/baseline", json={"file_path": path_v1})
        assert res_b.status_code == 200
        assert res_b.get_json()["baseline"]["sha256"] == hash_v1

        # 3. Verify unchanged PDF -> MATCHED
        res_v1 = client.post("/api/verify", json={"file_path": path_v1})
        assert res_v1.status_code == 200
        assert res_v1.get_json()["result"]["status"] == "MATCHED"

        # 4. Modify PDF content and re-stage
        pdf_bytes_v2 = b"%PDF-1.4\n%Binary stream integrity target v2.0 TAMPERED\n%%EOF"
        data_v2 = {
            "file": (io.BytesIO(pdf_bytes_v2), "security_policy.pdf"),
        }
        res_u2 = client.post("/api/upload", data=data_v2, content_type="multipart/form-data")
        assert res_u2.status_code == 200
        assert res_u2.get_json()["sha256"] != hash_v1

        # 5. Verify modified PDF -> MODIFIED
        res_v2 = client.post("/api/verify", json={"file_path": path_v1})
        assert res_v2.status_code == 200
        assert res_v2.get_json()["result"]["status"] == "MODIFIED"

    def test_upload_and_verify_docx_lifecycle(self, client):
        """
        Verify DOCX upload, baseline creation, and unchanged verification (MATCHED).
        """
        docx_bytes = b"PK\x03\x04\x14\x00\x06\x00DOCX_BINARY_STREAM_CONTENT_MOCK_BYTES"
        data = {
            "file": (io.BytesIO(docx_bytes), "contract_nda.docx"),
        }
        res_u = client.post("/api/upload", data=data, content_type="multipart/form-data")
        assert res_u.status_code == 200
        d_u = res_u.get_json()
        assert d_u["success"] is True
        assert d_u["metadata"]["file_extension"] == ".docx"
        assert d_u["metadata"]["file_name"] == "contract_nda.docx"
        docx_path = d_u["metadata"]["file_path"]

        # Baseline DOCX
        res_b = client.post("/api/baseline", json={"file_path": docx_path})
        assert res_b.status_code == 200

        # Verify unchanged DOCX -> MATCHED
        res_v = client.post("/api/verify", json={"file_path": docx_path})
        assert res_v.status_code == 200
        assert res_v.get_json()["result"]["status"] == "MATCHED"

    def test_upload_multiple_common_file_types(self, client):
        """
        Verify common file types: .txt, .pdf, .docx, .py, .jpg, .png, .zip.
        """
        test_files = [
            ("notes.txt", b"plain text notes", ".txt"),
            ("document.pdf", b"%PDF-1.4\nsome pdf data", ".pdf"),
            ("report.docx", b"PK\x03\x04docx data", ".docx"),
            ("script.py", b"print('secure hash check')", ".py"),
            ("photo.jpg", b"\xff\xd8\xff\xe0\x00\x10JFIF", ".jpg"),
            ("graphic.png", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR", ".png"),
            ("archive.zip", b"PK\x03\x04zip archive content", ".zip"),
        ]

        for filename, raw_bytes, expected_ext in test_files:
            data = {"file": (io.BytesIO(raw_bytes), filename)}
            res = client.post("/api/upload", data=data, content_type="multipart/form-data")
            assert res.status_code == 200
            res_json = res.get_json()
            assert res_json["success"] is True
            assert res_json["metadata"]["file_extension"] == expected_ext
            assert len(res_json["sha256"]) == 64

    def test_sha256_generated_from_bytes_not_file_path(self, client, tmp_path):
        """
        Verify SHA-256 is strictly computed from raw file bytes,
        independent of filename or filesystem path.
        """
        shared_payload = b"CRITICAL_CRYPTOGRAPHIC_IDENTICAL_BYTES_2026"
        
        file1 = tmp_path / "first_location.txt"
        file2 = tmp_path / "second_different_name.pdf"
        file1.write_bytes(shared_payload)
        file2.write_bytes(shared_payload)

        res1 = client.post("/api/analyze", json={"file_path": str(file1)})
        res2 = client.post("/api/analyze", json={"file_path": str(file2)})

        assert res1.status_code == 200
        assert res2.status_code == 200
        assert res1.get_json()["sha256"] == res2.get_json()["sha256"]

        # Different bytes with identical names must yield different SHA-256
        file3 = tmp_path / "different_bytes.txt"
        file3.write_bytes(b"DIFFERENT_PAYLOAD_BYTES")
        res3 = client.post("/api/analyze", json={"file_path": str(file3)})
        assert res3.get_json()["sha256"] != res1.get_json()["sha256"]

    def test_directory_cannot_be_analyzed(self, client, tmp_path):
        """Verify directories are rejected and not treated as regular files."""
        subfolder = tmp_path / "test_folder"
        subfolder.mkdir()

        res = client.post("/api/analyze", json={"file_path": str(subfolder)})
        # Directory should return error
        assert res.status_code in (400, 403, 404, 500)
        data = res.get_json()
        assert data["success"] is False
        assert "directory" in data["error"].lower()



