#!/usr/bin/env python3
"""
File Integrity Checker — Command-Line Interface (CLI).
Allows fast cryptographic integrity auditing, baseline storage, and report generation
directly from your terminal.
"""

import argparse
import sys
from pathlib import Path

from core.hasher import calculate_sha256
from core.file_handler import get_file_metadata, validate_file_path
from core.database import DatabaseManager
from core.comparator import FileComparator, VerificationStatus
from core.reporter import ReportGenerator


def cmd_hash(args, db: DatabaseManager):
    """Calculate and display SHA-256 for a target file."""
    meta = get_file_metadata(args.file_path)
    if not meta["exists"]:
        print(f"[ERROR] {meta['error']}", file=sys.stderr)
        sys.exit(1)
    if not meta["is_readable"]:
        print(f"[ERROR] {meta['error']}", file=sys.stderr)
        sys.exit(1)

    try:
        digest = calculate_sha256(meta["file_path"])
        print(f"File Name : {meta['file_name']}")
        print(f"File Path : {meta['file_path']}")
        print(f"File Size : {meta['file_size_human']} ({meta['file_size']} bytes)")
        print(f"SHA-256   : {digest}")
    except Exception as e:
        print(f"[ERROR] Failed to calculate hash: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_baseline(args, db: DatabaseManager):
    """Establish or update trusted baseline for a target file."""
    meta = get_file_metadata(args.file_path)
    if not meta["exists"] or not meta["is_readable"]:
        print(f"[ERROR] {meta.get('error') or 'Cannot read file'}", file=sys.stderr)
        sys.exit(1)

    try:
        digest = calculate_sha256(meta["file_path"])
        record = db.save_baseline(
            file_name=meta["file_name"],
            file_path=meta["file_path"],
            sha256=digest,
            file_size=meta["file_size"],
        )
        print("[SUCCESS] Trusted baseline established!")
        print(f"Baseline ID : {record['id']}")
        print(f"File Name   : {record['file_name']}")
        print(f"File Path   : {record['file_path']}")
        print(f"SHA-256     : {record['sha256']}")
        print(f"Timestamp   : {record['created_at']}")
    except Exception as e:
        print(f"[ERROR] Failed to establish baseline: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_verify(args, db: DatabaseManager):
    """Verify target file against its stored baseline."""
    comparator = FileComparator(db)
    result = comparator.verify_file(args.file_path, record_in_history=True)

    if args.json:
        print(ReportGenerator.to_json_report(result))
    else:
        print(ReportGenerator.to_text_report(result))

    if result.status == VerificationStatus.MATCHED.value:
        sys.exit(0)
    elif result.status == VerificationStatus.MODIFIED.value:
        sys.exit(2)
    elif result.status == VerificationStatus.MISSING.value:
        sys.exit(3)
    else:
        sys.exit(1)


def cmd_list_baselines(args, db: DatabaseManager):
    """List all stored baselines."""
    baselines = db.list_all_baselines()
    if not baselines:
        print("No stored baselines found.")
        return

    print("=" * 80)
    print(f"{'ID':<6} {'FILE NAME':<24} {'SIZE':<12} {'CREATED AT':<22}")
    print("-" * 80)
    for b in baselines:
        print(f"{b['id']:<6} {b['file_name'][:22]:<24} {str(b['file_size']) + ' B':<12} {b['created_at'][:19]:<22}")
        print(f"       Path   : {b['file_path']}")
        print(f"       SHA-256: {b['sha256']}")
    print("=" * 80)
    print(f"Total Baselines: {len(baselines)}")


def cmd_delete_baseline(args, db: DatabaseManager):
    """Delete a baseline by its ID."""
    success = db.delete_baseline(args.id)
    if success:
        print(f"[SUCCESS] Baseline ID {args.id} deleted.")
    else:
        print(f"[ERROR] Baseline ID {args.id} not found.", file=sys.stderr)
        sys.exit(1)


def cmd_history(args, db: DatabaseManager):
    """Display verification history audit log."""
    records = db.get_history(limit=args.limit, status_filter=args.status)
    print(ReportGenerator.to_history_summary_text(records))


def cmd_report(args, db: DatabaseManager):
    """Print detailed verification report for a specific history record ID."""
    record = db.get_history_record_by_id(args.id)
    if not record:
        print(f"[ERROR] Verification record ID {args.id} not found.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(ReportGenerator.to_json_report(record))
    else:
        print(ReportGenerator.to_text_report(record))


def cmd_serve(args, db: DatabaseManager):
    """Launch the local web user interface."""
    from web.server import create_app
    app = create_app(db_path=args.db)
    print(f"[INFO] Starting File Integrity Checker local web server on http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


def main():
    parser = argparse.ArgumentParser(
        description="File Integrity Checker — Cryptographic SHA-256 Baseline & Verification Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--db", default="integrity_checker.db", help="Path to SQLite database file")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # hash
    p_hash = subparsers.add_parser("hash", help="Calculate SHA-256 of a file")
    p_hash.add_argument("file_path", help="Path to file")

    # baseline
    p_base = subparsers.add_parser("baseline", help="Create or update baseline for a file")
    p_base.add_argument("file_path", help="Path to file")

    # verify
    p_ver = subparsers.add_parser("verify", help="Verify a file against stored baseline")
    p_ver.add_argument("file_path", help="Path to file")
    p_ver.add_argument("--json", action="store_true", help="Output results in JSON format")

    # list-baselines
    subparsers.add_parser("list-baselines", help="List all stored baselines")

    # delete-baseline
    p_del = subparsers.add_parser("delete-baseline", help="Delete a baseline by ID")
    p_del.add_argument("id", type=int, help="Baseline ID")

    # history
    p_hist = subparsers.add_parser("history", help="Show verification history")
    p_hist.add_argument("--status", choices=["MATCHED", "MODIFIED", "MISSING", "ERROR"], help="Filter by status")
    p_hist.add_argument("--limit", type=int, default=50, help="Maximum entries to show")

    # report
    p_rep = subparsers.add_parser("report", help="Generate full report for a verification event")
    p_rep.add_argument("id", type=int, help="Verification history ID")
    p_rep.add_argument("--json", action="store_true", help="Output report in JSON")

    # serve
    p_srv = subparsers.add_parser("serve", help="Launch local web application UI")
    p_srv.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    p_srv.add_argument("--port", type=int, default=5000, help="Port to listen on (default: 5000)")
    p_srv.add_argument("--debug", action="store_true", help="Enable debug mode")

    parsed_args = parser.parse_args()
    db = DatabaseManager(db_path=parsed_args.db)

    commands = {
        "hash": cmd_hash,
        "baseline": cmd_baseline,
        "verify": cmd_verify,
        "list-baselines": cmd_list_baselines,
        "delete-baseline": cmd_delete_baseline,
        "history": cmd_history,
        "report": cmd_report,
        "serve": cmd_serve,
    }

    cmd_fn = commands.get(parsed_args.command)
    if cmd_fn:
        cmd_fn(parsed_args, db)


if __name__ == "__main__":
    main()
