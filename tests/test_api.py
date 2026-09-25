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



