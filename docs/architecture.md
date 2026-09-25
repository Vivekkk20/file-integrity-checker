# Architecture & Technical Design

## 1. System Overview

**File Integrity Checker** is a local, privacy-first cybersecurity utility designed to detect unauthorized modifications to files through deterministic cryptographic hashing (SHA-256) and trusted baseline comparison.

```text
+--------------------------------------------------------------------------+
|                            USER INTERFACES                               |
|                                                                          |
|   +----------------------------+        +----------------------------+   |
|   |   Web UI (HTML5/CSS3/JS)   |        |   Command Line (cli.py)    |   |
|   |  - Home / Dashboard        |        |  - hash                    |   |
|   |  - File Analysis           |        |  - baseline                |   |
|   |  - Verification Result     |        |  - verify                  |   |
|   |  - History & Baselines     |        |  - list-baselines          |   |
|   |  - Educational About       |        |  - history / report        |   |
|   +--------------+-------------+        +--------------+-------------+   |
+------------------|-------------------------------------|-----------------+
                   | (REST API)                          | (Direct Call)
                   v                                     v
+--------------------------------------------------------------------------+
|                             CORE ENGINE                                  |
|                                                                          |
|   +-----------------------+              +---------------------------+   |
|   |      hasher.py        |              |      file_handler.py      |   |
|   |  - Streaming SHA-256  |              |  - Canonical path resolve |   |
|   |  - 64 KB chunk buffers|              |  - Access & size checks   |   |
|   +-----------+-----------+              +-------------+-------------+   |
|               |                                        |                 |
|               +-------------------+--------------------+                 |
|                                   |                                      |
|                                   v                                      |
|                      +--------------------------+                        |
|                      |      comparator.py       |                        |
|                      |  - Deterministic Verdict |                        |
|                      |  - MATCHED / MODIFIED    |                        |
|                      |  - MISSING / ERROR       |                        |
|                      +------------+-------------+                        |
|                                   |                                      |
|         +-------------------------+-------------------------+            |
|         |                                                   |            |
|         v                                                   v            |
|  +--------------+                                    +---------------+   |
|  |  database.py |                                    |  reporter.py  |   |
|  |  - SQLite    |                                    |  - Text Audit |   |
|  |  - Baselines |                                    |  - JSON Spec  |   |
|  |  - History   |                                    +---------------+   |
|  +-------+------+                                                        |
+----------|---------------------------------------------------------------+
           v
+-----------------------+
|  integrity_checker.db |  (Local SQLite File)
+-----------------------+
```

---

## 2. Component Breakdown

### 2.1 Hash Engine (`core/hasher.py`)
- **Algorithm**: Standard NIST SHA-256 (`hashlib.sha256()`).
- **Streaming Buffer**: Reads data in continuous 64 KB (65,536-byte) chunks.
- **Memory Footprint**: $O(1)$ constant memory usage regardless of whether the file is 10 KB or 100 GB.
- **Output**: 64-character lowercase hexadecimal digest string.

### 2.2 File Handler (`core/file_handler.py`)
- **Safety**: Paths are treated as untrusted strings.
- **Normalization**: Paths are stripped of accidental wrapper quotes, scanned for null-byte injections (`\x00`), and resolved to absolute canonical filesystem targets.
- **Metadata**: Collects file size, human-readable size, last modified timestamp (ISO UTC), and accessibility permissions.
- **Guarantees**: Target files are opened exclusively in read-only mode (`rb`). Files are never executed or passed to shell processes.

### 2.3 Database Layer (`core/database.py`)
- **Engine**: SQLite 3 (`integrity_checker.db`).
- **Tables**:
  - `baselines`: Stores trusted cryptographic baselines with unique file path constraint (`ON CONFLICT(file_path) DO UPDATE`).
  - `verification_history`: Append-only audit trail logging every verification attempt with timestamp, status, baseline hash, current hash, and context.
- **Security**: 100% parameterized queries (`?`), zero raw string interpolation.

### 2.4 Comparison Engine (`core/comparator.py`)
Deterministic status logic evaluates integrity:
- `MATCHED`: Target file exists on disk and its current SHA-256 digest matches the stored baseline hash exactly.
- `MODIFIED`: Target file exists on disk, but its current SHA-256 digest differs from the stored baseline hash.
- `MISSING`: Baseline entry exists in SQLite, but the target file is absent from disk.
- `ERROR`: Target file cannot be read due to file system permission constraints, missing baseline, or unhandled I/O faults.

### 2.5 Report Generator (`core/reporter.py`)
- **Text Format**: Structured security report suitable for terminal viewing, log archiving, and clipboard copying.
- **JSON Format**: Structured machine-readable schema for automated CI/CD pipeline consumption.
- **Advisory Footnotes**: Clarifies hashing vs encryption and emphasizes that `MATCHED` proves cryptographic consistency, not absence of malware.

---

## 3. Data Flow: Verification Lifecycle

```text
1. User provides file path (or uploads staged file).
2. file_handler.py validates canonical path and checks disk accessibility.
3. database.py queries `baselines` table for matching file_path.
4. If baseline is missing: Return ERROR ("No baseline found").
5. If file is missing from disk: Return MISSING.
6. hasher.py calculates SHA-256 of current file in 64KB blocks.
7. comparator.py compares baseline_hash with current_hash.
8. database.py logs verification event in `verification_history`.
9. database.py updates `last_verified_at` on the baseline entry.
10. UI/CLI displays color-coded verdict and allows downloading audit report.
```

---

## 4. Privacy & Data Protection Architecture

- **100% Local**: No external HTTP requests, no third-party telemetry, no cloud synchronization.
- **No Payload Storage**: The SQLite database only stores file metadata (paths, hashes, sizes, timestamps). The actual file contents are never copied into the database.
- **Ephemeral Upload Staging**: Files uploaded via the web interface are staged locally inside `staged_files/` for immediate chunked processing.

---

## 5. UI Design System & Google Stitch Integration

The web interface is built around modern cybersecurity design principles with deep inspiration and token compatibility from **Google Stitch** (Google Labs' AI-native design-to-code suite at `stitch.withgoogle.com`).

### Supported Theme Palettes:
1. **Google Stitch Pro (`stitch-dark`)** *(Default)*:
   - Modern AI-native aesthetic with luminous cyan accents (`#00d2ff`), cybernetic indigo glows, and frosted glass cards.
2. **Obsidian Matrix (`cyber-obsidian`)**:
   - High-contrast cybersecurity terminal palette with pitch-black canvas (`#040608`) and radiant matrix emerald (`#00ff88`).
3. **Midnight Cyberpunk (`midnight-neon`)**:
   - Synthwave-inspired deep midnight violet canvas (`#090714`) with hot neon magenta (`#ec4899`) and electric violet accents.
4. **Slate Titanium (`clean-slate`)**:
   - Refined enterprise security styling with deep titanium slate (`#0b0f19`) and sky-blue accents (`#38bdf8`).

### Google Stitch Studio & Token Bridge:
- **Client-Side Token Synchronization**: The UI features an interactive Stitch Studio allowing users to export active design tokens in JSON format or import custom Stitch schemas generated from natural language prompts.
- **Privacy Assurance**: The Stitch integration runs entirely within the local browser environment via CSS custom property mutation. File hashes, file names, and SQLite records are never transmitted externally.

