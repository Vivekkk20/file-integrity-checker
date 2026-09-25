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

