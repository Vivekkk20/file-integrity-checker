"""
Local Web Server & REST API.
Serves the web user interface and provides secure API endpoints for file analysis,
baseline persistence, cryptographic verification, audit history, and reporting.
"""

import json
import os
from pathlib import Path
from typing import Optional
from flask import Flask, render_template, request, jsonify, Response
from werkzeug.utils import secure_filename

from core.hasher import calculate_sha256
from core.file_handler import get_file_metadata, validate_file_path
from core.database import DatabaseManager
from core.comparator import FileComparator, VerificationStatus
from core.reporter import ReportGenerator


def create_app(db_path: str = "integrity_checker.db") -> Flask:
    """Application factory for the File Integrity Checker web service."""
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).parent / "templates"),
        static_folder=str(Path(__file__).parent / "static"),
    )

    app.config["DB_PATH"] = db_path
    app.config["UPLOAD_FOLDER"] = str(Path(app.root_path).parent / "staged_files")
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1 GB max upload limit
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.jinja_env.auto_reload = True

    # Ensure upload directory exists
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    @app.after_request
    def add_no_cache_headers(response):
        """Disable caching to guarantee the latest scripts, styles, and templates are always served."""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    def get_db() -> DatabaseManager:
        return DatabaseManager(db_path=app.config["DB_PATH"])

    # -------------------------------------------------------------------------
    # Frontend Routes
    # -------------------------------------------------------------------------

    @app.route("/")
    def index():
        return render_template("index.html")

    # -------------------------------------------------------------------------
    # API Routes
    # -------------------------------------------------------------------------

    @app.route("/api/stats", methods=["GET"])
    def api_stats():
        """Retrieve aggregated dashboard metrics."""
        db = get_db()
        stats = db.get_dashboard_stats()
        return jsonify({"success": True, "stats": stats})

    @app.route("/api/analyze", methods=["POST"])
    def api_analyze():
        """
        Analyze a file by path or uploaded payload.
        Computes SHA-256 and retrieves filesystem metadata.
        """
        data = request.get_json(silent=True) or {}
        raw_path = data.get("file_path", "").strip()

        if not raw_path:
            return jsonify({
                "success": False,
                "error": "A valid file_path parameter is required.",
            }), 400

        meta = get_file_metadata(raw_path)
        if not meta["exists"]:
            return jsonify({
                "success": False,
                "error": meta.get("error", "File not found on disk."),
                "metadata": meta,
            }), 404

        if not meta["is_readable"]:
            return jsonify({
                "success": False,
                "error": meta.get("error", "Permission denied."),
                "metadata": meta,
            }), 403

        try:
            sha256 = calculate_sha256(meta["file_path"])
            db = get_db()
            existing_baseline = db.get_baseline_by_path(meta["file_path"])

            return jsonify({
                "success": True,
                "metadata": meta,
                "sha256": sha256,
                "has_baseline": existing_baseline is not None,
                "baseline": existing_baseline,
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to compute SHA-256: {str(e)}",
                "metadata": meta,
            }), 500

    @app.route("/api/upload", methods=["POST"])
    def api_upload():
        """
        Stage an uploaded file into the local staged_files directory for integrity checking.
        """
        if "file" not in request.files:
            return jsonify({"success": False, "error": "No file uploaded."}), 400

        uploaded_file = request.files["file"]
        if uploaded_file.filename == "":
            return jsonify({"success": False, "error": "Empty filename."}), 400

        filename = secure_filename(uploaded_file.filename)
        if not filename:
            filename = "uploaded_file.bin"

        dest_dir = Path(app.config["UPLOAD_FOLDER"])
        dest_path = dest_dir / filename
        uploaded_file.save(dest_path)

        meta = get_file_metadata(str(dest_path))
        sha256 = calculate_sha256(str(dest_path))
        db = get_db()
        existing_baseline = db.get_baseline_by_path(str(dest_path))

        return jsonify({
            "success": True,
            "metadata": meta,
            "sha256": sha256,
            "has_baseline": existing_baseline is not None,
            "baseline": existing_baseline,
        })

    @app.route("/api/baseline", methods=["POST"])
    def api_create_baseline():
        """
        Create or update a trusted baseline for a target file.
        """
        data = request.get_json(silent=True) or {}
        file_path = data.get("file_path", "").strip()

        if not file_path:
            return jsonify({"success": False, "error": "Missing file_path."}), 400

        meta = get_file_metadata(file_path)
        if not meta["exists"] or not meta["is_readable"]:
            return jsonify({"success": False, "error": meta.get("error", "File not accessible.")}), 400

        try:
            sha256 = calculate_sha256(meta["file_path"])
            db = get_db()
            record = db.save_baseline(
                file_name=meta["file_name"],
                file_path=meta["file_path"],
                sha256=sha256,
                file_size=meta["file_size"],
            )
            return jsonify({
                "success": True,
                "message": "Baseline created successfully.",
                "baseline": record,
            })
        except Exception as e:
            return jsonify({"success": False, "error": f"Failed to create baseline: {str(e)}"}), 500

    @app.route("/api/verify", methods=["POST"])
    def api_verify():
        """
        Verify a target file against its stored baseline.
        """
        data = request.get_json(silent=True) or {}
        file_path = data.get("file_path", "").strip()

        if not file_path:
            return jsonify({"success": False, "error": "Missing file_path."}), 400

        db = get_db()
        comparator = FileComparator(db)
        result = comparator.verify_file(file_path, record_in_history=True)

        return jsonify({
            "success": True,
            "result": result.to_dict(),
        })

    @app.route("/api/baselines", methods=["GET"])
    def api_list_baselines():
        """List all stored baselines."""
        db = get_db()
        baselines = db.list_all_baselines()
        return jsonify({"success": True, "baselines": baselines})

    @app.route("/api/baselines/<int:baseline_id>", methods=["DELETE"])
    def api_delete_baseline(baseline_id: int):
        """Delete a baseline by its numeric ID."""
        db = get_db()
        deleted = db.delete_baseline(baseline_id)
        if deleted:
            return jsonify({"success": True, "message": f"Baseline {baseline_id} deleted."})
        return jsonify({"success": False, "error": f"Baseline {baseline_id} not found."}), 404

    @app.route("/api/history", methods=["GET"])
    def api_history():
        """Retrieve verification history with optional filtering."""
        status_filter = request.args.get("status")
        limit = request.args.get("limit", 50, type=int)
        offset = request.args.get("offset", 0, type=int)

        db = get_db()
        history = db.get_history(limit=limit, offset=offset, status_filter=status_filter)
        return jsonify({"success": True, "history": history})

    @app.route("/api/report/<int:history_id>", methods=["GET"])
    def api_report(history_id: int):
        """Generate a verification audit report in text or JSON format."""
        format_type = request.args.get("format", "text").lower()
        db = get_db()
        record = db.get_history_record_by_id(history_id)

        if not record:
            return jsonify({"success": False, "error": "Verification record not found."}), 404

        if format_type == "json":
            return jsonify({
                "success": True,
                "report": json.loads(ReportGenerator.to_json_report(record)),
            })
        else:
            text_report = ReportGenerator.to_text_report(record)
            return Response(text_report, mimetype="text/plain")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
