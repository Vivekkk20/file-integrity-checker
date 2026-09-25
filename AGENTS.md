# AGENTS.md — File Integrity Checker

This document defines the primary architectural guidelines, functional specifications, and design boundaries for the **File Integrity Checker** project.

---

## 1. Project Overview & Objective

**File Integrity Checker** is a lightweight, local cybersecurity utility designed to detect unauthorized alterations to files by generating and comparing cryptographic checksums (SHA-256).

### Core Workflow:
```text
File Selection
      ↓
SHA-256 Hash Generation (Chunked)
      ↓
Baseline Creation (Stored in SQLite)
      ↓
File Verification (At any later point)
      ↓
Comparison (Baseline Hash vs Current Hash)
      ↓
Result Categorization:
  - MATCHED
  - MODIFIED
  - MISSING
  - ERROR
      ↓
Verification History Log & Report Generation
```

### Educational & Portfolio Objective:
- Provide an intuitive, beginner-friendly cybersecurity demonstration tool.
- Clearly educate users on the distinction between **hashing** and **encryption**.
- Clarify that a `MATCHED` hash guarantees integrity against the baseline, not absolute freedom from malware.

---

## 2. Scope Boundaries (What NOT to Build)

To keep Version 1 robust, maintainable, and strictly aligned with its primary purpose:
- **NO** SIEM (Security Information and Event Management) integration.
- **NO** Antivirus / signature scanning engine.
- **NO** Network scanning or remote telemetry.
- **NO** File encryption / decryption modules.
- **NO** Cloud storage uploads or remote database synchronization.
- **NO** Machine learning anomaly detectors or fake analytics scores.

All operations **must remain local** to the user's workstation.

---

## 3. Architecture & Modular Structure

The codebase must follow a strict separation of concerns. Do not place business logic in UI controllers or a monolithic script.

```text
file_integrity_checker/
├── core/
│   ├── __init__.py
│   ├── hasher.py          # SHA-256 chunked calculation using hashlib
│   ├── file_handler.py     # Safe path validation, file metadata, error guards
│   ├── database.py         # SQLite schema, baseline storage & history management
│   ├── comparator.py       # Deterministic comparison engine (MATCHED, MODIFIED, MISSING, ERROR)
│   └── reporter.py         # Formatted text & JSON report generator
├── web/
│   ├── templates/          # HTML templates for local web interface
│   │   └── index.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Modern, accessible cybersecurity design system
│   │   └── js/
│   │       └── app.js      # Interactive frontend client
│   └── server.py           # Flask/local web application routing & API endpoints
├── cli.py                  # Command-line interface for terminal usage and automation
├── tests/                  # Pytest test suite using temporary files
│   ├── test_hasher.py
│   ├── test_comparator.py
│   ├── test_database.py
│   ├── test_file_handler.py
│   ├── test_reporter.py
│   └── test_api.py
├── docs/                   # Full documentation suite
│   ├── architecture.md
│   ├── testing.md
│   └── security.md
├── AGENTS.md               # Primary architectural specification
├── README.md               # User-facing manual and guide
├── requirements.txt        # Pinned dependencies
└── .gitignore              # Repository hygiene
```

---

## 4. Technical Specifications

### Hash Engine (`core/hasher.py`)
- Algorithm: **SHA-256** via Python's standard library `hashlib.sha256()`.
- Chunked processing: Process files in standard buffer chunks (e.g., 64 KB = 65,536 bytes) to handle multi-gigabyte files with negligible memory footprint.
- Function signature: `calculate_sha256(file_path: str, chunk_size: int = 65536) -> str`.

### File Security & Input Validation (`core/file_handler.py`)
- Treat all file paths as untrusted input.
- Resolve absolute canonical paths; prevent null-byte injection.
- Validate file existence, read permissions, and non-directory status before hashing.
- Never execute or execute commands on target files (no `os.system` or `subprocess` on target paths).

### Database Engine (`core/database.py`)
- Storage: **SQLite** via standard library `sqlite3` (`integrity_checker.db`).
- **Baselines Table (`baselines`)**:
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `file_name` (TEXT NOT NULL)
  - `file_path` (TEXT UNIQUE NOT NULL)
  - `sha256` (TEXT NOT NULL)
  - `file_size` (INTEGER NOT NULL)
  - `created_at` (TEXT NOT NULL, ISO-8601 UTC)
  - `last_verified_at` (TEXT, ISO-8601 UTC)
- **Verification History Table (`verification_history`)**:
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `file_name` (TEXT NOT NULL)
  - `file_path` (TEXT NOT NULL)
  - `baseline_hash` (TEXT)
  - `current_hash` (TEXT)
  - `status` (TEXT NOT NULL: MATCHED, MODIFIED, MISSING, ERROR)
  - `details` (TEXT)
  - `verified_at` (TEXT NOT NULL, ISO-8601 UTC)

### Comparison Engine (`core/comparator.py`)
Deterministic status logic:
- `MATCHED`: Baseline exists, current file exists, `baseline_hash == current_hash`.
- `MODIFIED`: Baseline exists, current file exists, `baseline_hash != current_hash`.
- `MISSING`: Baseline exists, but current file does not exist on disk.
- `ERROR`: Target file cannot be accessed, read permission denied, or unhandled I/O fault.

---

## 5. UI/UX Specifications

The user interface must offer five core screens/tabs:
1. **Home / Dashboard**: Overview, quick file selection, summary metrics (total baselines, recent verifications, matched/modified counts), and fast actions.
2. **File Analysis**: Detailed breakdown of a selected file (file name, path, size, SHA-256 digest, calculation timestamp), with buttons to "Create Baseline" or "Verify Against Baseline".
3. **Verification Result**: Dedicated result card with distinct color-coded badges (`MATCHED` in emerald green, `MODIFIED` in amber/red, `MISSING` in purple/warning, `ERROR` in crimson), diff view of hashes, and explanation of findings.
4. **History**: Chronological log of all verification checks querying the local SQLite database directly (File, Status, Hash, Timestamp, Action to view full report).
5. **About**: Educational documentation explaining what file integrity checking is, how SHA-256 hashing works, cryptographic collisions, hashing vs encryption, and practical limitations.

### Design Aesthetics:
- Visual tone: Sleek, modern cybersecurity dark theme with glassmorphism, crisp typography (Inter / JetBrains Mono), smooth micro-interactions, responsive card layouts, and accessible contrast.
- No decorative fake charts or simulated threat scores. Real data only.

---

## 6. Testing & Quality Requirements

- Unit tests must mock or use isolated `tempfile` fixtures. Real user files must never be modified during test runs.
- Minimum test coverage:
  - Accurate SHA-256 generation.
  - Chunked hashing consistency on varying sizes.
  - Deterministic hash change on single-bit modification.
  - Status evaluation: MATCHED, MODIFIED, MISSING, ERROR.
  - Database CRUD: insert baseline, query baseline, update last verified, insert history.
  - API endpoint integration.
- Full end-to-end verification cycle test.

---

## 7. Security & Privacy Guarantees

- **100% Local**: No external HTTP requests, no tracking analytics, no telemetry, no cloud sync.
- **Principle of Least Privilege**: Only open files in read-only binary mode (`rb`).
- **Secret Hygiene**: Zero hardcoded credentials or API keys; strictly clean `.gitignore`.
