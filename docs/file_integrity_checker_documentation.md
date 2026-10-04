# File Integrity Checker — Professional Project Documentation
## SHA-256 Based File Integrity Verification & Baseline Monitoring Tool
**Project Name:** File Integrity Checker  
**Developed & Verified By:** Vivek Rathod  
**Core Technologies:** Python 3.14, Flask, SQLite, SHA-256 (hashlib)  
**Frontend Architecture:** Semantic HTML5, Modern CSS3, Vanilla ES6 JavaScript  
**Testing Framework:** Pytest 9.1 (54 Automated Tests Passing)  
**GitHub Repository:** [https://github.com/Vivekkk20/file-integrity-checker](https://github.com/Vivekkk20/file-integrity-checker)  

---

## Page 1 — Project Cover & Identity

### Project Identity
- **Project Name:** File Integrity Checker
- **Core Technologies:** Python 3.14, Flask, SQLite, SHA-256 (hashlib)
- **Frontend Architecture:** Semantic HTML5, Modern CSS3, Vanilla ES6 JavaScript
- **Testing Framework:** Pytest 9.1 (54 Automated Tests Passing)
- **GitHub Repository:** [https://github.com/Vivekkk20/file-integrity-checker](https://github.com/Vivekkk20/file-integrity-checker)
- **Developed & Verified By:** Vivek Rathod

---

## Page 2 — Introduction & Problem Context

### 🎯 Goal
Articulate the operational necessity of automated cryptographic verification in defensive cybersecurity, establishing why traditional inspection fails to detect unauthorized alterations, bit rot, and stealthy supply-chain compromises.

### Why File Integrity Matters
In modern computing systems, configuration files, binary executables, script libraries, and compliance records represent primary targets for unauthorized alteration. Malicious actors, rogue insider processes, ransomware, or unexpected storage failures (bit rot) can introduce modifications that go unnoticed by conventional perimeter defenses.

### Why Traditional File Attributes Fail
- **Timestamp Forgery (Timestomping):** File modification timestamps can be trivially spoofed using standard operating system utilities (e.g., `touch -r`) to match legitimate historical dates.
- **Byte Padding & Size Preservation:** Attackers can alter code within a script or binary and append padding characters to ensure the total file byte size remains identical.
- **Invisibility of Single-Bit Modifications:** A change of a single character in a configuration file (such as toggling an access rule or port number) is visually imperceptible across large directory trees.

### Cryptographic Hashing: Deterministic Digital Fingerprints
Cryptographic hash algorithms—specifically **SHA-256** (NIST FIPS 180-4)—provide an objective, mathematical mechanism to verify file integrity. A cryptographic hash function maps an arbitrary file binary stream into a fixed-length 256-bit (64-character hexadecimal) digest.

SHA-256 provides two fundamental guarantees: **Pre-image Resistance** (it is computationally infeasible to reconstruct the original file contents from the digest) and the **Avalanche Effect** (a single bit change in the input file alters more than 50% of the resulting digest bits in an unpredictable manner).

---

## Page 3 — Project Objectives & System Scope

### 🎯 Goal
Formally establish the core technical objectives, targeted users, and operational boundaries of File Integrity Checker, ensuring clarity regarding its capabilities and scope.

### Core Technical Objectives
1. **SHA-256 Hash Engine:** Implement chunked 64 KB buffer reading using Python's standard `hashlib` library to process files of arbitrary size with low, steady memory usage.
2. **Authoritative Baseline Repository:** Engineer a persistent SQLite database schema to store immutable records of canonical file paths, hexadecimal digests, file sizes, and UTC timestamps.
3. **Deterministic Verification Engine:** Evaluate file status deterministically into unambiguous categories: `MATCHED`, `MODIFIED`, `MISSING`, and `ERROR`.
4. **Verification History & Audit Trail:** Maintain a chronological history log of all verification checks, complete with structured text and JSON export capabilities.
5. **Safe File Handling & Input Validation:** Enforce strict input sanitation (canonical path resolution, null-byte rejection) and safe read-only binary file access (`rb`).

### Project Scope & System Boundaries
| Dimension | In-Scope Functionality | Out-of-Scope / Boundaries |
|---|---|---|
| **Target Users** | Security analysts, system administrators, developers, and students | General consumer sync tools requiring automatic cloud sync |
| **Hash Engine** | Standard SHA-256 via Python `hashlib` with 64 KB chunked streaming buffers | Deprecated algorithms (MD5, SHA-1) or proprietary hashing schemes |
| **Baseline Storage** | Local relational SQLite schema storing authoritative paths, hashes, sizes | Remote cloud databases, cluster synchronization, or blockchain ledgers |
| **Verification States** | Deterministic evaluation: `MATCHED`, `MODIFIED`, `MISSING`, `ERROR` | Subjective heuristic scores, predictive risk ratings, or speculative analytics |
| **File Security** | Read-only binary ingestion (`rb`), null-byte prevention, traversal blocks | Antivirus signature scanning, malware detonation, or binary reverse-engineering |
| **Audit Logging** | Append-only SQLite history, structured text certificate export, JSON payloads | Real-time SIEM socket streaming (reserved for future development) |
| **Telemetry & Network** | 100% local, air-gapped execution; zero external HTTP requests | Cloud tracking beacons, analytics endpoints, or remote data sync |

---

## Page 4 — Technology Stack & Requirements

### 🎯 Goal
Document the technical foundation, dependencies manifest, and hardware/software runtime requirements supporting the File Integrity Checker ecosystem.

### Dependencies Manifest
| Package | Version | Functional Purpose |
|---|---|---|
| **Flask** | 3.1.2 | WSGI application server, REST API routing, and HTML template delivery |
| **Werkzeug** | 3.1.3 | HTTP utilities, secure file upload sanitation (`secure_filename`) |
| **pytest** | 9.1.1 | Automated test execution, temporary file fixture mocking, assertions |
| **click** | 8.1.8 | Command-line interface parameter parsing and flag dispatch |
| **colorama** | 0.4.6 | Cross-platform ANSI terminal coloring for highlighted CLI feedback |
| **iniconfig** | 2.0.0 | Configuration file parser reading `pytest.ini` settings |

### System & Runtime Requirements
| Parameter | Minimum Specification | Recommended / Verified Specification |
|---|---|---|
| **Operating System** | Windows 10, Linux (Kernel 5.4+), macOS 12+ | Windows 11 Enterprise (x64) / Ubuntu 22.04 LTS |
| **CPU Processor** | Single-core x86-64 / ARM64 (1.5 GHz) | Multi-core 2.5 GHz+ (Supports hardware SHA extensions) |
| **System RAM** | 512 MB Available RAM | 2.0 GB+ Available RAM |
| **Storage Disk Space** | 50 MB Free Space | 250 MB Free SSD Space (Supports deep history logs) |
| **Web Browser** | Chromium 90+, Firefox 88+, Safari 14+ | Google Chrome 120+ / Microsoft Edge (V8 Engine) |
| **Python Environment** | Python 3.10+ | Python 3.14.7 (Active Verified Environment) |

---

## Page 5 — System Architecture & Workflow

### 🎯 Goal
Illustrate the complete architectural topology and 7-phase execution lifecycle governing data ingestion, chunked hashing, database persistence, and comparison logic.

### Step-by-Step Execution Lifecycle
1. **Phase 1 — Ingestion & Sanitation:** File path is sanitized via `FileHandler.validate_path()`, resolving canonical absolute paths.
2. **Phase 2 — Binary Stream Access:** File existence and permissions are validated; target is opened in read-only binary mode (`rb`).
3. **Phase 3 — Chunked Hashing:** `Hasher.calculate_sha256()` reads the stream in sequential 64 KB chunks, feeding the accumulator without RAM spikes.
4. **Phase 4 — Baseline Lookup:** `DatabaseManager.get_baseline_by_path()` queries SQLite for existing authoritative records.
5. **Phase 5 — Hash Comparison:** `Comparator.verify_file()` executes constant-time string comparison between digests.
6. **Phase 6 — State Categorization:** System deterministically emits `MATCHED`, `MODIFIED`, `MISSING`, or `ERROR`.
7. **Phase 7 — Audit Trail Persistence:** The verdict, timestamps, and hashes are committed to `verification_history`.

---

## Page 6 — Application Setup & Main Dashboard

### 🎯 Goal
Document the verified installation procedure, server startup sequence, and the architectural components of the primary graphical dashboard.

### Real Screenshot Evidence
- **Figure 1: File Integrity Checker central dashboard interface** (`docs/screenshots/annotated/01_dashboard_annotated.png`)

### Interface Component Breakdown
- **① Main Navigation Header:** Accessible tab controls providing switching across Dashboard, File Analysis, Results, History & Baselines, and About screens.
- **② Telemetry Metric Counters:** Displays Baselines Established (5), Files Verified (9), Integrity Matches (5), and Security Alerts (4).
- **③ Quick Verification Console:** Path input box and native OS file selector with mouse cursor positioned over the "Verify File" action button.
- **④ Hero Action Controls:** Privacy-first status pill and direct action buttons to trigger file analysis or inspect historical verification logs.

---

## Page 7 — File Integrity Verification Workflow

### 🎯 Goal
Examine the end-to-end operational workflow of selecting a target file, calculating its cryptographic digest, establishing an authoritative baseline, and performing subsequent state verification.

### Real Screenshot Evidence
- **Figure 2: File Analysis and verification interface** (`docs/screenshots/annotated/02_file_analysis_annotated.png`)

### Interface Component Breakdown
- **① Selected Target File Details:** Renders resolved file name (`security_policy.pdf`), canonical path, human-readable size, and timestamp.
- **② SHA-256 Cryptographic Checksum Box:** Displays complete 64-character hexadecimal digest with clipboard copy utility.
- **③ Create Baseline Action Button:** High-visibility emerald button with mouse cursor positioned directly over it to register the file's current hash.
- **④ Verify File Action Button:** Primary blue action button comparing current disk bytes against the stored baseline.
- **⑤ Drag-and-Drop Ingestion Zone:** Seamless drag-and-drop zone supporting PDF, DOCX, Python, or archive binaries.

---

## Page 8 — Verification Results: MATCHED & MODIFIED

### 🎯 Goal
Examine the visual output and structural details of the two primary baseline comparison states: verified intact (MATCHED) and unauthorized modification (MODIFIED).

### Real Screenshot Evidence
- **Figure 3: Verification Result screen showing MATCHED state** (`docs/screenshots/annotated/04_matched_verdict_annotated.png`)
  - ① Emerald MATCHED Verdict Banner
  - ② Target File Details
  - ③ Side-by-Side Hash Equality Proof
  - ④ MATCHED Security Advisory Guidance
- **Figure 4: Verification Result screen showing MODIFIED state** (`docs/screenshots/annotated/05_modified_verdict_annotated.png`)
  - ① Amber MODIFIED Alert Banner
  - ② Target File Details
  - ③ Divergent SHA-256 Hashes Mismatch
  - ④ Incident Response Advisory Guidance

---

## Page 9 — Verification Results: MISSING & ERROR

### 🎯 Goal
Examine the handling of anomalous operational states: detecting deleted files (MISSING) and enforcing baseline prerequisites (ERROR / NO_BASELINE).

### Real Screenshot Evidence
- **Figure 5: Verification Result screen showing MISSING state** (`docs/screenshots/annotated/06_missing_verdict_annotated.png`)
  - ① Purple MISSING File Alert Banner
  - ② Missing Path Notice & Expected Baseline
  - ③ Deletion / Rename Guidance Advisory
- **Figure 6: Verification Result screen showing ERROR state** (`docs/screenshots/annotated/07_no_baseline_error_annotated.png`)
  - ① Crimson ERROR Banner
  - ② Target File Notice
  - ③ Baseline Prerequisite Advisory (The ERROR state displays the appropriate no-baseline guidance and does not display MATCHED messaging)

---

## Page 10 — SHA-256 Hash Engine & Baselines Management

### 🎯 Goal
Detail the 64 KB chunked buffer implementation in core/hasher.py, demonstrate the Avalanche Effect with actual test data, and document baseline vault management.

### The Avalanche Effect Demonstrated
- **Original:** `860dc6c39a039755f114631ab2f34ee3cffb94f6fef7e067cbb3eb624c9c6463`
- **Tampered:** `52b618cfce998c0b2f34e64f72782e4e16428c0b875ad28913d8036d0f507c92`
- **Bit Diff:** 132 out of 256 bits changed (51.56% variance) — Avalanche Effect verified.

### Real Screenshot Evidence
- **Figure 7: Authoritative Baselines Vault Management Table** (`docs/screenshots/annotated/09_baselines_vault_annotated.png`)
  - ① Stored Baseline Entry (Row 1)
  - ② Stored SHA-256 Digest Preview
  - ③ One-Click Re-Verification Action
  - ④ Baseline Deletion Action

---

## Page 11 — Verification History & Reports

### 🎯 Goal
Demonstrate the audit logging architecture, status-based search filtering, and structured report generation capabilities.

### Real Screenshot Evidence
- **Figure 8: Verification History log with color-coded status badges** (`docs/screenshots/annotated/08_history_logs_annotated.png`)
  - ① History Table Body
  - ② Status Filter Dropdown
  - ③ Report Action Trigger
  - ④ Re-verify Action Button
- **Figure 9: Monospaced Verification Audit Report modal** (`docs/screenshots/annotated/10_report_modal_annotated.png`)
  - ① Report Certificate Header
  - ② Monospaced Report Body with Cryptographic Proofs
  - ③ Save to File Download Action

---

## Page 12 — Educational Guidance & System Concepts

### 🎯 Goal
Examine the educational concepts embedded directly within the application, clarifying the difference between hashing and encryption, and defining defensive boundaries.

### Real Screenshot Evidence
- **Figure 10: Educational About screen articulating hashing fundamentals** (`docs/screenshots/annotated/12_about_screen_annotated.png`)
  - ① Cryptographic Hashing Concept Card
  - ② Hashing vs. Encryption Separation Card
  - ③ Operational Scope Boundaries Card

---

## Page 13 — Quality Assurance & Test Matrix

### 🎯 Goal
Provide a formal quality assurance matrix mapping core functional and security specifications to empirical test results, substantiated by the automated pytest suite execution log.

### Automated Test Suite Verification Log (54 Tests Passing)
```text
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: file-integrity-checker, configfile: pytest.ini
collected 54 items

tests/test_api.py ......................                                 [ 40%]
tests/test_comparator.py .......                                         [ 53%]
tests/test_database.py ......                                            [ 64%]
tests/test_end_to_end.py .                                               [ 66%]
tests/test_file_handler.py ........                                      [ 81%]
tests/test_hasher.py .......                                             [ 94%]
tests/test_reporter.py ...                                               [100%]

============================= 54 passed in 1.22s ==============================
```

---

## Page 14 — Security Considerations & Roadmap

### 🎯 Goal
Review the application's defensive security controls, identify current technical boundaries, and outline a realistic future development roadmap.

### Defensive Considerations
- **Strict Path Sanitation:** Rejection of null bytes and canonical path resolution prevent traversal exploits.
- **Read-Only Binary Access:** Files are opened strictly in binary read-only mode (`rb`); zero execution.
- **Staging Directory Isolation:** Drag-and-drop uploads are isolated in temporary staging directories.
- **Zero External Attack Surface:** Zero telemetry beacons, external CDN dependencies, or cloud analytics.

### Strategic Technical Roadmap (Future Scope)
| Future Enhancement | Proposed Implementation | Anticipated Security Impact |
|---|---|---|
| **Real-Time Filesystem Monitoring** | Integrate Python `watchdog` daemon utilizing OS-level event APIs | Immediate notification upon unauthorized file modification |
| **Cryptographically Signed Baselines** | Asymmetric Ed25519 or HMAC-SHA256 digital signatures over records | Prevents offline tampering of the local SQLite database |
| **Multi-Algorithm Composite Hashes** | Concurrent calculation of SHA-256 and BLAKE3 digests in parallel | Long-term agility and resilience against algorithm weaknesses |
| **Enterprise SIEM Forwarder** | RFC 5424 Syslog / CEF JSON socket emitter to external log collectors | Centralized audit visibility across multi-host environments |

---

## Page 15 — Project Conclusion & Sign-Off

### 🎯 Goal
Summarize completed technical achievements, demonstrate real-world defensive cybersecurity relevance, and provide formal project sign-off and authorship credits.

### Summary of Completed Work
- Implemented chunked 64 KB SHA-256 stream hashing.
- Developed an ACID-compliant SQLite baseline and history schema.
- Validated deterministic 4-state verification (`MATCHED`, `MODIFIED`, `MISSING`, `ERROR`).
- Built local web interface with drag-and-drop file ingestion alongside CLI tool (`cli.py`).
- Achieved 100% pass rate across 54 automated pytest tests.

### Author & Repository Details
- **Project Author:** **Vivek Rathod**
- **GitHub Repository:** [https://github.com/Vivekkk20/file-integrity-checker](https://github.com/Vivekkk20/file-integrity-checker)
