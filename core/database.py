"""
SQLite Database Layer.
Stores baseline metadata, manages verification history logs, and aggregates
integrity statistics. Never stores actual file payloads.
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


def get_utc_now_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


class DatabaseManager:
    """Manages SQLite operations for file baselines and verification logs."""

    def __init__(self, db_path: str = "integrity_checker.db"):
        self.db_path = db_path
        self._ensure_parent_dir()
        self.init_db()

    def _ensure_parent_dir(self) -> None:
        """Create database directory if it does not exist (skip for in-memory)."""
        if self.db_path != ":memory:":
            Path(self.db_path).resolve().parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """Get a configured SQLite database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self) -> None:
        """Initialize database schema tables and indexes."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Baselines table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS baselines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT NOT NULL,
                    file_path TEXT UNIQUE NOT NULL,
                    sha256 TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    last_verified_at TEXT
                );
                """
            )
            # Index on file_path for fast lookups
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_baselines_path ON baselines(file_path);
                """
            )
            # Verification history table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS verification_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    baseline_hash TEXT,
                    current_hash TEXT,
                    status TEXT NOT NULL CHECK(status IN ('MATCHED', 'MODIFIED', 'MISSING', 'ERROR')),
                    details TEXT,
                    verified_at TEXT NOT NULL
                );
                """
            )
            # Index on verified_at for chronological ordering
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_history_verified_at ON verification_history(verified_at DESC);
                """
            )
            conn.commit()

    # -------------------------------------------------------------------------
    # Baseline Operations
    # -------------------------------------------------------------------------

    def save_baseline(
        self,
        file_name: str,
        file_path: str,
        sha256: str,
        file_size: int,
    ) -> Dict[str, Any]:
        """
        Create or update a baseline entry for a given file path (upsert).
        """
        canonical_path = str(Path(file_path).resolve())
        now = get_utc_now_iso()

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO baselines (file_name, file_path, sha256, file_size, created_at, last_verified_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(file_path) DO UPDATE SET
                    file_name = excluded.file_name,
                    sha256 = excluded.sha256,
                    file_size = excluded.file_size,
                    created_at = excluded.created_at,
                    last_verified_at = NULL
                RETURNING id, file_name, file_path, sha256, file_size, created_at, last_verified_at;
                """,
                (file_name, canonical_path, sha256.lower(), file_size, now, None),
            )
            row = cursor.fetchone()
            conn.commit()
            return dict(row)

    def get_baseline_by_path(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Retrieve baseline record matching the given canonical file path."""
        canonical_path = str(Path(file_path).resolve())
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, file_name, file_path, sha256, file_size, created_at, last_verified_at
                FROM baselines
                WHERE file_path = ?;
                """,
                (canonical_path,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_baseline_by_id(self, baseline_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve baseline record by its primary key ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, file_name, file_path, sha256, file_size, created_at, last_verified_at
                FROM baselines
                WHERE id = ?;
                """,
                (baseline_id,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_all_baselines(self) -> List[Dict[str, Any]]:
        """Return all stored baselines ordered by creation date descending."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, file_name, file_path, sha256, file_size, created_at, last_verified_at
                FROM baselines
                ORDER BY created_at DESC;
                """
            )
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def delete_baseline(self, baseline_id: int) -> bool:
        """Delete baseline by ID. Returns True if a record was removed."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM baselines WHERE id = ?;", (baseline_id,))
            conn.commit()
            return cursor.rowcount > 0

    def update_baseline_last_verified(self, file_path: str, verified_at: Optional[str] = None) -> bool:
        """Update last_verified_at timestamp for a baseline file path."""
        canonical_path = str(Path(file_path).resolve())
        timestamp = verified_at or get_utc_now_iso()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE baselines
                SET last_verified_at = ?
                WHERE file_path = ?;
                """,
                (timestamp, canonical_path),
            )
            conn.commit()
            return cursor.rowcount > 0

    # -------------------------------------------------------------------------
    # Verification History Operations
    # -------------------------------------------------------------------------

    def log_verification(
        self,
        file_name: str,
        file_path: str,
        baseline_hash: Optional[str],
        current_hash: Optional[str],
        status: str,
        details: Optional[str] = None,
        verified_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Log an entry to the verification_history table.
        """
        canonical_path = str(Path(file_path).resolve()) if file_path else "Unknown"
        timestamp = verified_at or get_utc_now_iso()
        b_hash = baseline_hash.lower() if baseline_hash else None
        c_hash = current_hash.lower() if current_hash else None

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO verification_history (
                    file_name, file_path, baseline_hash, current_hash, status, details, verified_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                RETURNING id, file_name, file_path, baseline_hash, current_hash, status, details, verified_at;
                """,
                (file_name, canonical_path, b_hash, c_hash, status, details, timestamp),
            )
            row = cursor.fetchone()
            conn.commit()
            return dict(row)

    def get_history(
        self,
        limit: int = 100,
        offset: int = 0,
        status_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve verification records with optional status filtering and pagination."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if status_filter and status_filter.upper() in ("MATCHED", "MODIFIED", "MISSING", "ERROR"):
                cursor.execute(
                    """
                    SELECT id, file_name, file_path, baseline_hash, current_hash, status, details, verified_at
                    FROM verification_history
                    WHERE status = ?
                    ORDER BY verified_at DESC
                    LIMIT ? OFFSET ?;
                    """,
                    (status_filter.upper(), limit, offset),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, file_name, file_path, baseline_hash, current_hash, status, details, verified_at
                    FROM verification_history
                    ORDER BY verified_at DESC
                    LIMIT ? OFFSET ?;
                    """,
                    (limit, offset),
                )
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_history_record_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Get a single verification history record by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, file_name, file_path, baseline_hash, current_hash, status, details, verified_at
                FROM verification_history
                WHERE id = ?;
                """,
                (record_id,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def clear_history(self) -> int:
        """Clear all verification history records (used for test/reset). Returns count deleted."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM verification_history;")
            conn.commit()
            return cursor.rowcount

    # -------------------------------------------------------------------------
    # Dashboard Aggregations
    # -------------------------------------------------------------------------

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Aggregate total baseline and verification status statistics."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) AS count FROM baselines;")
            total_baselines = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) AS count FROM verification_history;")
            total_verifications = cursor.fetchone()["count"]

            cursor.execute(
                """
                SELECT status, COUNT(*) AS count
                FROM verification_history
                GROUP BY status;
                """
            )
            status_counts = {r["status"]: r["count"] for r in cursor.fetchall()}

            cursor.execute(
                """
                SELECT id, file_name, file_path, baseline_hash, current_hash, status, verified_at
                FROM verification_history
                ORDER BY verified_at DESC
                LIMIT 5;
                """
            )
            recent_verifications = [dict(r) for r in cursor.fetchall()]

            return {
                "total_baselines": total_baselines,
                "total_verifications": total_verifications,
                "matched_count": status_counts.get("MATCHED", 0),
                "modified_count": status_counts.get("MODIFIED", 0),
                "missing_count": status_counts.get("MISSING", 0),
                "error_count": status_counts.get("ERROR", 0),
                "recent_verifications": recent_verifications,
            }
