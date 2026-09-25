# File Integrity Checker

A lightweight, local, privacy-first cybersecurity utility to establish trusted SHA-256 baselines, detect unauthorized file modifications, and verify digital file integrity.

---

## 1. Project Overview

In computer security, **File Integrity Monitoring (FIM)** is essential for detecting unauthorized alterations caused by malware (ransomware, rootkits), configuration drift, or accidental corruption.

**File Integrity Checker** allows users to:
1. Select any local file.
2. Compute its cryptographic **SHA-256** checksum via memory-safe 64 KB streaming buffers.
3. Establish an immutable, trusted **baseline** saved locally in an SQLite database.
4. Verify files at any later point and receive immediate, deterministic verdicts:
   - `MATCHED`: Cryptographic digest matches the baseline exactly.
   - `MODIFIED`: Digest diverges from the baseline (unauthorized modification detected).
   - `MISSING`: Target file has been deleted or moved from disk.
   - `ERROR`: Target file cannot be accessed or baseline does not exist.
5. Review complete audit logs and export formal security audit reports in text or JSON format.

---

## 2. Key Features

- **Double Interface**: Full modern local web interface with cybersecurity dark mode + command-line interface (CLI) for automation.
- **Streaming SHA-256 Engine**: Constant $O(1)$ memory consumption using 64 KB buffer blocks, easily handling files from kilobytes to multi-gigabytes without system strain.
- **Persistent Local Database**: Baselines and verification history stored locally in SQLite (`integrity_checker.db`).
- **100% Local & Privacy-Preserving**: No external requests, no cloud uploads, and no analytics tracking. File contents never leave your computer and are never stored in the database.
- **Defensive File Handling**: Absolute canonicalization, null-byte injection rejection, and strict read-only binary mode (`rb`). Target files are never executed.
- **Portfolio-Ready & Educational**: Built-in guidance explaining the difference between hashing and encryption, and why `MATCHED` confirms data integrity rather than malware absence.

---

## 3. Technology Stack

- **Backend**: Python 3.10+ (Standard Library `hashlib`, `sqlite3`, `pathlib`, `argparse`)
- **Web Server**: Flask 3.1
- **Frontend**: Semantic HTML5, Vanilla CSS3 (Sleek dark theme, glassmorphism, glowing status badges, responsive layout), Vanilla JavaScript (Fetch API, drag-and-drop, tab views)
- **Typography**: Google Fonts (Inter for UI, JetBrains Mono for hashes and terminal output)
- **Testing**: Pytest (36 unit, integration, API, and end-to-end tests)

---

## 4. Architecture

```text
file_integrity_checker/
├── AGENTS.md               # Primary project architecture specification
├── README.md               # User documentation & guide
├── requirements.txt        # Pinned project dependencies
├── pytest.ini              # Pytest configuration
├── .gitignore              # Repository hygiene
├── app.py                  # Web application launcher
├── cli.py                  # Terminal command-line interface
├── core/
│   ├── __init__.py
│   ├── hasher.py          # Chunked SHA-256 engine
│   ├── file_handler.py     # Safe path resolution & metadata inspection
│   ├── database.py         # SQLite baseline & history storage
│   ├── comparator.py       # Deterministic comparison engine
│   └── reporter.py         # Text & JSON audit report generation
├── web/
│   ├── __init__.py
│   ├── server.py           # Flask REST API & routing
│   ├── templates/
│   │   └── index.html      # 5-screen single page web app
│   └── static/
│       ├── css/style.css   # Dark cybersecurity design system
│       └── js/app.js       # Client controller & async handlers
├── tests/                  # 36 automated unit & integration tests
│   ├── test_hasher.py
│   ├── test_file_handler.py
│   ├── test_database.py
│   ├── test_comparator.py
│   ├── test_reporter.py
│   ├── test_api.py
│   └── test_end_to_end.py
└── docs/
    ├── architecture.md     # In-depth architectural design
    ├── testing.md          # Test suite documentation & inventory
    └── security.md         # Threat model & cryptographic guarantees
```

---

## 5. Installation & Setup

### Prerequisites
- Python 3.10 or later installed on Windows, macOS, or Linux.
- Git (optional, for cloning).

### Setup Instructions

```bash
# 1. Clone repository or navigate to workspace
cd "d:/projects/file integity checker"

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Windows (cmd):
.\.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 6. Usage Guide

### Option A: Launching the Web Interface

Start the local web application:

```bash
python app.py
```

Then open your browser to:
```
http://127.0.0.1:5000/
```

#### Available Web Screens:
1. **Home / Dashboard**: Overview metrics (Active Baselines, Total Verifications, Matched, Modified), recent activity feed, and quick verify input.
2. **File Analysis**: Enter a local path or drop a file to inspect file size, disk timestamps, and live SHA-256 digest. Actions: "Create / Update Baseline" and "Verify File Integrity".
3. **Verification Result**: Color-coded verdict card (`MATCHED`, `MODIFIED`, `MISSING`, `ERROR`) with side-by-side hash comparison and download report option.
4. **History & Baselines**: Search and filter historical verification checks or inspect and delete active baselines.
5. **About**: Educational reference explaining file integrity, SHA-256 mechanics, hashing vs. encryption, Google Stitch token architecture, and scope limits.

#### Theme Customization & Google Stitch Integration:
- **Theme Switcher**: Select between 4 cybersecurity themes in the header:
  - **Google Stitch Pro** (AI-native design system with cyan & indigo glows)
  - **Obsidian Matrix** (Terminal emerald green and pitch-black canvas)
  - **Midnight Cyberpunk** (Synthwave neon magenta and electric violet)
  - **Slate Titanium** (Clean enterprise navy and sky blue)
- **Google Stitch Studio & Token Bridge**: Click the **Stitch Studio** button in the header to:
  - Export active design tokens in JSON schema for use in Google Stitch (`stitch.withgoogle.com`).
  - Import custom AI-generated JSON tokens to dynamically restyle the application in real-time.
  - 100% private: All token synchronization happens purely client-side; local files and hashes are never transmitted.

---

### Option B: Using the Command-Line Interface (CLI)

The `cli.py` utility provides instant terminal commands:

#### 1. Calculate SHA-256 Hash
```bash
python cli.py hash "C:\path\to\file.txt"
```

#### 2. Establish or Update a Baseline
```bash
python cli.py baseline "C:\path\to\file.txt"
```

#### 3. Verify File Integrity
```bash
python cli.py verify "C:\path\to\file.txt"
```
*Outputs verification report and sets exit codes: 0 for MATCHED, 2 for MODIFIED, 3 for MISSING, 1 for ERROR.*

To export verification output as JSON:
```bash
python cli.py verify "C:\path\to\file.txt" --json
```

#### 4. List All Stored Baselines
```bash
python cli.py list-baselines
```

#### 5. View Verification Audit History
```bash
python cli.py history
python cli.py history --status MODIFIED --limit 20
```

#### 6. Export Report for a Historical Record
```bash
python cli.py report 1
python cli.py report 1 --json
```

#### 7. Start Web Server via CLI
```bash
python cli.py serve --port 5000
```

---

## 7. Example Verification Lifecycle

```bash
# 1. Create a sample configuration file
echo "port=8080" > config.ini

# 2. Establish trusted baseline
python cli.py baseline config.ini

# 3. Verify immediately -> MATCHED
python cli.py verify config.ini

# 4. Modify the file (simulating unauthorized change)
echo "port=9999" > config.ini

# 5. Verify again -> MODIFIED
python cli.py verify config.ini

# 6. Delete file (simulating deletion)
rm config.ini

# 7. Verify again -> MISSING
python cli.py verify config.ini
```

---

## 8. Automated Testing

All tests use temporary files created by pytest's `tmp_path` fixture:

```bash
pytest
```

Output:
```text
============================= 36 passed in 1.15s ==============================
```

Tests verify:
- NIST SHA-256 test vectors (including empty string).
- Single-bit alteration avalanche effect.
- 64 KB chunking on large files.
- Deterministic comparison verdicts (`MATCHED`, `MODIFIED`, `MISSING`, `ERROR`).
- SQLite CRUD transactions, upserts, and history filtering.
- Path sanitization, quotes stripping, and null-byte rejection.
- REST API endpoints and file upload staging.
- Full 7-step end-to-end verification lifecycle.

---

## 9. Security & Privacy Considerations

- **Strictly Local**: No file data, checksums, or paths are ever transmitted over the network.
- **Never Executes Files**: Files are treated as untrusted binary data and opened strictly in read-only mode (`rb`).
- **No Shell Execution**: The application avoids `os.system` or `subprocess` calls on file paths.
- **SQL Injection Prevention**: All SQLite queries use strict parameter binding (`?`).
- **Memory Safety**: Fixed 64 KB chunk streaming prevents memory exhaustion on large files.
- **Advisory Note**: A `MATCHED` hash proves data consistency with the baseline; it does not replace anti-malware inspection.

---

## 10. Limitations & Future Scope

### Limitations (By Design)
- Operates on individual files (Version 1 deliberately avoids complex recursive filesystem directory tree monitoring to remain simple and reliable).
- Does not monitor live kernel filesystem events in real-time (not a daemon or Windows filter driver).

### Future Roadmap
- Recursive directory baseline generation.
- Export audit reports in PDF format.
- Optional HMAC baseline signing with user password.
