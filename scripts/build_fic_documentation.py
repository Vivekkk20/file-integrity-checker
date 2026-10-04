"""
File Integrity Checker - Final Professional Documentation Builder.
Adheres strictly to all user guidelines:
1. 'Portfolio' word is 100% purged everywhere.
2. ZERO Software Edition or Academic & SOC anywhere.
3. NO 'Technical Domain' anywhere.
4. NO professional titles or designations. Author is strictly 'Vivek Rathod'.
5. Footer is strictly: 'File Integrity Checker                         Page X'.
6. Redesigned screenshots: Clean numbered badges (①, ②, ③) + thin highlight boxes. NO text labels over UI.
7. Verification results split across 2 dedicated pages (Page 8: MATCHED/MODIFIED, Page 9: MISSING/ERROR) for large, readable display.
8. Correct setup commands: '.\\.venv\\Scripts\\activate' (Windows) and 'source .venv/bin/activate' (Linux/macOS).
9. All local paths sanitized to '<project-folder>'.
10. Measured, factual technical language without exaggerated marketing terms.
"""

import os
import sys
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright
import pypdf

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
SCREENSHOTS_DIR = DOCS_DIR / "screenshots" / "annotated"
HTML_FILE = DOCS_DIR / "file_integrity_checker_documentation.html"
PDF_FILE = DOCS_DIR / "file_integrity_checker_documentation.pdf"
MD_FILE = DOCS_DIR / "file_integrity_checker_documentation.md"


def get_base64_image(filename: str) -> str:
    path = SCREENSHOTS_DIR / filename
    if path.exists():
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    print(f"[!] Warning: Image not found: {path}")
    return ""


def build_html() -> str:
    img_dashboard = get_base64_image("01_dashboard_annotated.png")
    img_analysis = get_base64_image("02_file_analysis_annotated.png")
    img_matched = get_base64_image("04_matched_verdict_annotated.png")
    img_modified = get_base64_image("05_modified_verdict_annotated.png")
    img_missing = get_base64_image("06_missing_verdict_annotated.png")
    img_no_baseline = get_base64_image("07_no_baseline_error_annotated.png")
    img_baselines = get_base64_image("09_baselines_vault_annotated.png")
    img_history = get_base64_image("08_history_logs_annotated.png")
    img_report_modal = get_base64_image("10_report_modal_annotated.png")
    img_about = get_base64_image("12_about_screen_annotated.png")
    img_pytest = get_base64_image("13_pytest_evidence_annotated.png")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>File Integrity Checker - Project Documentation</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  body {{
    margin: 0;
    padding: 0;
    background-color: #f1f5f9;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    color: #0f172a;
    font-size: 9.3pt;
    line-height: 1.43;
  }}
  .page {{
    width: 210mm;
    height: 297mm;
    margin: 0 auto 20px auto;
    background: #ffffff;
    padding: 10mm 12mm;
    page-break-after: always;
    page-break-inside: avoid;
    position: relative;
    display: flex;
    flex-direction: column;
  }}
  @media print {{
    body {{
      background: none;
    }}
    .page {{
      margin: 0;
      width: 210mm;
      height: 297mm;
    }}
  }}
  .page-border {{
    width: 100%;
    height: 100%;
    border: 3.5px double #1e293b;
    padding: 16px 20px 12px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
  }}
  .page-content {{
    flex: 1;
    display: flex;
    flex-direction: column;
  }}
  .page-header {{
    text-align: center;
    margin-bottom: 8px;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 5px;
  }}
  .page-title {{
    font-size: 15.5pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.01em;
    margin: 0 0 2px 0;
  }}
  .page-subtitle {{
    font-size: 9.2pt;
    font-weight: 600;
    color: #0284c7;
    margin: 0;
  }}
  .section-title {{
    font-size: 10.2pt;
    font-weight: 700;
    color: #0f172a;
    margin: 6px 0 3px 0;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .goal-box {{
    background: #f8fafc;
    border-left: 3.5px solid #0284c7;
    padding: 5px 10px;
    margin-bottom: 7px;
    font-size: 8.9pt;
  }}
  .goal-title {{
    font-weight: 700;
    color: #0369a1;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .explanation-text {{
    margin: 0 0 5px 0;
    text-align: justify;
    color: #1e293b;
  }}
  ul.clean-list {{
    margin: 3px 0 6px 0;
    padding-left: 17px;
  }}
  ul.clean-list li {{
    margin-bottom: 3px;
    color: #1e293b;
  }}
  ul.clean-list li strong {{
    color: #0f172a;
  }}
  .key-takeaway {{
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 3.5px solid #16a34a;
    padding: 5px 9px;
    font-size: 8.8pt;
    color: #14532d;
    margin-top: auto;
    margin-bottom: 2px;
    border-radius: 4px;
  }}
  .screenshot-container {{
    text-align: center;
    margin: 4px 0 2px 0;
  }}
  .screenshot-img {{
    max-width: 98%;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.06);
  }}
  .screenshot-caption {{
    font-size: 8pt;
    color: #64748b;
    font-style: italic;
    margin-top: 3px;
    text-align: center;
  }}
  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 5px 0 7px 0;
    font-size: 8.2pt;
  }}
  table.data-table th {{
    background: #0f172a;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 4.5px 7px;
    border: 1px solid #0f172a;
  }}
  table.data-table td {{
    padding: 4px 7px;
    border: 1px solid #cbd5e1;
    color: #1e293b;
    vertical-align: top;
  }}
  table.data-table tr:nth-child(even) {{
    background: #f8fafc;
  }}
  table.qa-table th {{
    padding: 2.5px 6px;
    font-size: 7.8pt;
  }}
  table.qa-table td {{
    padding: 2px 6px;
    font-size: 7.8pt;
  }}
  .badge-pass {{
    background: #dcfce7;
    color: #15803d;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 7.5pt;
    border: 1px solid #86efac;
    display: inline-block;
  }}
  .badge-matched {{
    background: #ecfdf5;
    color: #059669;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 7.5pt;
    border: 1px solid #10b981;
    display: inline-block;
  }}
  .badge-modified {{
    background: #fef2f2;
    color: #dc2626;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 7.5pt;
    border: 1px solid #ef4444;
    display: inline-block;
  }}
  .badge-missing {{
    background: #faf5ff;
    color: #7c3aed;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 7.5pt;
    border: 1px solid #8b5cf6;
    display: inline-block;
  }}
  .badge-error {{
    background: #fff1f2;
    color: #e11d48;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 7.5pt;
    border: 1px solid #f43f5e;
    display: inline-block;
  }}
  .page-footer {{
    border-top: 1px solid #e2e8f0;
    padding-top: 5px;
    margin-top: 4px;
    display: flex;
    justify-content: space-between;
    font-size: 8.5pt;
    color: #475569;
    font-weight: 600;
  }}
  .mono {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 7.8pt;
  }}
  .code-block {{
    background: #0f172a;
    color: #e2e8f0;
    padding: 5px 8px;
    border-radius: 4px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 7.6pt;
    line-height: 1.32;
    margin: 4px 0;
    white-space: pre;
    overflow-x: auto;
  }}

  /* Cover Page Styles */
  .cover-container {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    text-align: center;
    padding: 50px 25px 30px 25px;
  }}
  .cover-title {{
    font-size: 40pt;
    font-weight: 900;
    color: #0f172a;
    letter-spacing: -0.035em;
    line-height: 1.05;
    margin-bottom: 12px;
  }}
  .cover-subtitle {{
    font-size: 13.5pt;
    font-weight: 700;
    color: #0284c7;
    margin-bottom: 18px;
    letter-spacing: -0.01em;
  }}
  .cover-divider {{
    width: 60px;
    height: 3.5px;
    background: #0284c7;
    margin: 0 auto 20px auto;
    border-radius: 2px;
  }}
  .cover-desc {{
    font-size: 10.2pt;
    color: #475569;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.55;
  }}
  .cover-meta-box {{
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 20px 26px;
    max-width: 490px;
    margin: 0 auto;
    text-align: left;
  }}
  .cover-meta-row {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 9pt;
    border-bottom: 1px dashed #e2e8f0;
    padding-bottom: 5px;
  }}
  .cover-meta-row:last-child {{
    margin-bottom: 0;
    border-bottom: none;
    padding-bottom: 0;
  }}
  .cover-meta-label {{
    color: #64748b;
    font-weight: 600;
  }}
  .cover-meta-val {{
    color: #0f172a;
    font-weight: 700;
  }}
  .cover-author-block {{
    margin-top: 20px;
  }}
  .cover-by {{
    font-size: 8.5pt;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748b;
    font-weight: 700;
    margin-bottom: 4px;
  }}
  .cover-author-name {{
    font-size: 17pt;
    font-weight: 800;
    color: #0f172a;
    margin: 0;
  }}
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- PAGE 1: PROJECT COVER                                                     -->
<!-- ========================================================================= -->
<div class="page" id="page-1">
  <div class="page-border">
    <div class="cover-container">
      <div>
        <h1 class="cover-title">File Integrity Checker</h1>
        <div class="cover-subtitle">SHA-256 Based File Integrity Verification & Baseline Monitoring Tool</div>
        <div class="cover-divider"></div>
        <p class="cover-desc">
          A local cybersecurity utility engineered to compute deterministic SHA-256 cryptographic digests, establish immutable baselines, detect single-bit tampering, and maintain structured verification history.
        </p>
      </div>

      <div class="cover-meta-box">
        <div class="cover-meta-row">
          <span class="cover-meta-label">Project Name:</span>
          <span class="cover-meta-val">File Integrity Checker</span>
        </div>
        <div class="cover-meta-row">
          <span class="cover-meta-label">Core Technologies:</span>
          <span class="cover-meta-val">Python 3.14, Flask, SQLite, SHA-256 (hashlib)</span>
        </div>
        <div class="cover-meta-row">
          <span class="cover-meta-label">Frontend Architecture:</span>
          <span class="cover-meta-val">Semantic HTML5, Modern CSS3, Vanilla ES6 JavaScript</span>
        </div>
        <div class="cover-meta-row">
          <span class="cover-meta-label">Testing Framework:</span>
          <span class="cover-meta-val">Pytest 9.1 (54 Automated Tests Passing)</span>
        </div>
        <div class="cover-meta-row">
          <span class="cover-meta-label">GitHub Repository:</span>
          <span class="cover-meta-val">https://github.com/Vivekkk20/file-integrity-checker</span>
        </div>
      </div>

      <div class="cover-author-block">
        <div class="cover-by">DEVELOPED & VERIFIED BY</div>
        <h2 class="cover-author-name">Vivek Rathod</h2>
        <div style="font-size: 8pt; color: #94a3b8; margin-top: 10px;">
          Comprehensive Project Documentation Report • September 2026
        </div>
      </div>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 1</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 2: INTRODUCTION & PROBLEM CONTEXT                                    -->
<!-- ========================================================================= -->
<div class="page" id="page-2">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">Introduction & Problem Context</h1>
        <div class="page-subtitle">The Critical Need for Cryptographic File Integrity Verification & Baseline Monitoring</div>
      </div>

      <div class="goal-box">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Articulate the operational necessity of automated cryptographic verification in defensive cybersecurity, establishing why traditional inspection fails to detect unauthorized alterations, bit rot, and stealthy supply-chain compromises.
        </div>
      </div>

      <div class="section-title">🛡️ Why File Integrity Verification Matters</div>
      <p class="explanation-text">
        In modern computing systems, configuration files, binary executables, script libraries, and compliance records represent primary targets for unauthorized alteration. Malicious actors, rogue insider processes, ransomware, or unexpected storage failures (bit rot) can introduce modifications that go unnoticed by conventional perimeter defenses.
      </p>

      <div class="section-title">⚠️ The Inadequacy of Traditional File Attributes</div>
      <p class="explanation-text">
        Relying on standard operating system metadata—such as file timestamps (<code>mtime</code>), reported byte sizes, or visual directory inspections—is inherently unreliable for security verification:
      </p>
      <ul class="clean-list">
        <li><strong>Timestamp Forgery (Timestomping):</strong> File modification timestamps can be trivially spoofed using standard operating system utilities (e.g., <code>touch -r</code>) to match legitimate historical dates.</li>
        <li><strong>Byte Padding & Size Preservation:</strong> Attackers can alter code within a script or binary and append padding characters to ensure the total file byte size remains identical.</li>
        <li><strong>Invisibility of Single-Bit Modifications:</strong> A change of a single character in a configuration file (such as toggling an access rule or port number) is visually imperceptible across large directory trees.</li>
      </ul>

      <div class="section-title">🔐 Cryptographic Hashing: Deterministic Digital Fingerprints</div>
      <p class="explanation-text">
        Cryptographic hash algorithms—specifically <strong>SHA-256</strong> (NIST FIPS 180-4)—provide an objective, mathematical mechanism to verify file integrity. A cryptographic hash function maps an arbitrary file binary stream into a fixed-length 256-bit (64-character hexadecimal) digest.
      </p>
      <p class="explanation-text">
        SHA-256 provides two fundamental guarantees: <strong>Pre-image Resistance</strong> (it is computationally infeasible to reconstruct the original file contents from the digest) and the <strong>Avalanche Effect</strong> (a single bit change in the input file alters more than 50% of the resulting digest bits in an unpredictable manner).
      </p>

      <div class="section-title">🚀 File Integrity Checker: The Project Solution</div>
      <p class="explanation-text">
        <strong>File Integrity Checker</strong> is a lightweight, local cybersecurity utility designed to monitor and verify file integrity. By capturing an authoritative cryptographic baseline during a known trusted state, persisting it in a local SQLite database, and comparing it during subsequent checks, the tool provides deterministic proof of whether a file remains intact, has been altered, or has been deleted.
      </p>

      <div class="key-takeaway">
        <strong>Key Principle:</strong> Cryptographic integrity verification confirms that a file's binary stream has not changed since its baseline was established. It guarantees consistency against the reference state, not that the original file is free of malware.
      </div>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 2</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 3: PROJECT OBJECTIVES & SCOPE                                        -->
<!-- ========================================================================= -->
<div class="page" id="page-3">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">Project Objectives & System Scope</h1>
        <div class="page-subtitle">Functional Boundaries, Target Users, and Operational Guidelines</div>
      </div>

      <div class="goal-box">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Formally establish the core technical objectives, targeted users, and operational boundaries of File Integrity Checker, ensuring clarity regarding its capabilities and scope.
        </div>
      </div>

      <div class="section-title">🎯 Core Technical Objectives</div>
      <ul class="clean-list">
        <li><strong>SHA-256 Hash Engine:</strong> Implement chunked 64 KB buffer reading using Python's standard <code>hashlib</code> library to process files of arbitrary size with low, steady memory usage.</li>
        <li><strong>Authoritative Baseline Repository:</strong> Engineer a persistent SQLite database schema to store immutable records of canonical file paths, hexadecimal digests, file sizes, and UTC timestamps.</li>
        <li><strong>Deterministic Verification Engine:</strong> Evaluate file status deterministically into unambiguous categories: <code>MATCHED</code>, <code>MODIFIED</code>, <code>MISSING</code>, and <code>ERROR</code>.</li>
        <li><strong>Verification History & Audit Trail:</strong> Maintain a chronological history log of all verification checks, complete with structured text and JSON export capabilities.</li>
        <li><strong>Safe File Handling & Input Validation:</strong> Enforce strict input sanitation (canonical path resolution, null-byte rejection) and safe read-only binary file access (<code>rb</code>).</li>
      </ul>

      <div class="section-title">📐 Project Scope & System Boundaries</div>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 22%;">Dimension</th>
            <th style="width: 43%;">In-Scope Functionality</th>
            <th style="width: 35%;">Out-of-Scope / Boundaries</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Target Users</strong></td>
            <td>Security analysts, system administrators, developers, and students learning integrity monitoring.</td>
            <td>General consumer sync tools requiring automatic cloud synchronization.</td>
          </tr>
          <tr>
            <td><strong>Hash Engine</strong></td>
            <td>Standard SHA-256 via Python <code>hashlib</code> with 64 KB chunked streaming buffers.</td>
            <td>Deprecated/broken algorithms (MD5, SHA-1) or proprietary hashing schemes.</td>
          </tr>
          <tr>
            <td><strong>Baseline Storage</strong></td>
            <td>Local relational SQLite schema storing authoritative paths, hashes, sizes, and UTC dates.</td>
            <td>Remote cloud databases, cluster synchronization, or blockchain ledgers.</td>
          </tr>
          <tr>
            <td><strong>Verification States</strong></td>
            <td>Deterministic evaluation: <code>MATCHED</code>, <code>MODIFIED</code>, <code>MISSING</code>, <code>ERROR</code>.</td>
            <td>Subjective heuristic scores, predictive risk ratings, or speculative analytics.</td>
          </tr>
          <tr>
            <td><strong>File Security</strong></td>
            <td>Read-only binary ingestion (<code>rb</code>), null-byte prevention, path traversal blocking.</td>
            <td>Antivirus signature scanning, malware detonation, or binary reverse-engineering.</td>
          </tr>
          <tr>
            <td><strong>Audit Logging</strong></td>
            <td>Append-only SQLite history, structured text certificate export, and JSON API payloads.</td>
            <td>Real-time SIEM socket streaming (reserved for future development).</td>
          </tr>
          <tr>
            <td><strong>Telemetry & Network</strong></td>
            <td>100% local, air-gapped execution; zero external HTTP requests, zero cloud telemetry.</td>
            <td>Cloud tracking beacons, analytics endpoints, or remote data sync.</td>
          </tr>
        </tbody>
      </table>

      <div class="key-takeaway">
        <strong>Operational Scope:</strong> File Integrity Checker operates strictly within a localized defensive boundary. By avoiding external telemetry and speculative scoring, every verification verdict is deterministic, reproducible, and auditable.
      </div>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 3</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 4: TECHNOLOGY STACK & REQUIREMENTS                                   -->
<!-- ========================================================================= -->
<div class="page" id="page-4">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">Technology Stack & Requirements</h1>
        <div class="page-subtitle">Implementation Environment, Verified Dependencies, and System Specifications</div>
      </div>

      <div class="goal-box">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Document the technical foundation, dependencies manifest, and hardware/software runtime requirements supporting the File Integrity Checker ecosystem.
        </div>
      </div>

      <div class="section-title">💻 Core Technology Architecture</div>
      <p class="explanation-text">
        The application is engineered in Python utilizing a modular, layered architecture separating core cryptographic services from presentation controllers:
      </p>
      <ul class="clean-list">
        <li><strong>Language & Runtime:</strong> Python 3.10+ (tested on Python 3.14.7) providing native standard library cryptography and memory safety.</li>
        <li><strong>Hash Engine:</strong> Python standard library <code>hashlib</code> utilizing C-bindings for hardware-accelerated SHA-256 calculation.</li>
        <li><strong>Application Server:</strong> Flask 3.1.2 providing lightweight, local HTTP endpoint routing and JSON REST API serialization.</li>
        <li><strong>Persistence Engine:</strong> SQLite 3 via native <code>sqlite3</code> driver, offering zero-configuration, atomic ACID transactions in a local database file.</li>
        <li><strong>Frontend Client:</strong> Semantic HTML5, Vanilla ES6+ JavaScript, and modern responsive CSS3 with high-contrast accessibility.</li>
        <li><strong>Testing Framework:</strong> Pytest 9.1.1 framework driving 54 automated unit, API, file handler, and end-to-end integration tests.</li>
      </ul>

      <div class="section-title">📋 Dependencies Manifest</div>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 25%;">Package</th>
            <th style="width: 15%;">Version</th>
            <th style="width: 60%;">Functional Purpose</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Flask</strong></td>
            <td>3.1.2</td>
            <td>WSGI application server, REST API routing, and HTML template delivery.</td>
          </tr>
          <tr>
            <td><strong>Werkzeug</strong></td>
            <td>3.1.3</td>
            <td>HTTP utilities, secure file upload sanitation (<code>secure_filename</code>), and WSGI layer.</td>
          </tr>
          <tr>
            <td><strong>pytest</strong></td>
            <td>9.1.1</td>
            <td>Automated test execution, temporary file fixture mocking, and assertion reporting.</td>
          </tr>
          <tr>
            <td><strong>click</strong></td>
            <td>8.1.8</td>
            <td>Command-line interface parameter parsing and flag dispatch for <code>cli.py</code>.</td>
          </tr>
          <tr>
            <td><strong>colorama</strong></td>
            <td>0.4.6</td>
            <td>Cross-platform ANSI terminal coloring for highlighted CLI status feedback.</td>
          </tr>
          <tr>
            <td><strong>iniconfig</strong></td>
            <td>2.0.0</td>
            <td>Configuration file parser reading <code>pytest.ini</code> parameters and test paths.</td>
          </tr>
        </tbody>
      </table>

      <div class="section-title">⚙️ System & Runtime Specifications</div>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 28%;">Parameter</th>
            <th style="width: 36%;">Minimum Specification</th>
            <th style="width: 36%;">Recommended / Verified Specification</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Operating System</strong></td>
            <td>Windows 10, Linux (Kernel 5.4+), macOS 12+</td>
            <td>Windows 11 Enterprise (x64) / Ubuntu 22.04 LTS</td>
          </tr>
          <tr>
            <td><strong>CPU Processor</strong></td>
            <td>Single-core x86-64 / ARM64 (1.5 GHz)</td>
            <td>Multi-core 2.5 GHz+ (Supports hardware SHA extensions)</td>
          </tr>
          <tr>
            <td><strong>System RAM</strong></td>
            <td>512 MB Available RAM</td>
            <td>2.0 GB+ Available RAM</td>
          </tr>
          <tr>
            <td><strong>Storage Disk Space</strong></td>
            <td>50 MB Free Space</td>
            <td>250 MB Free SSD Space (Supports deep history logs)</td>
          </tr>
          <tr>
            <td><strong>Web Browser</strong></td>
            <td>Chromium 90+, Firefox 88+, Safari 14+</td>
            <td>Google Chrome 120+ / Microsoft Edge (V8 Engine)</td>
          </tr>
          <tr>
            <td><strong>Python Environment</strong></td>
            <td>Python 3.10+</td>
            <td>Python 3.14.7 (Active Verified Environment)</td>
          </tr>
        </tbody>
      </table>

      <div class="key-takeaway">
        <strong>Zero-Cloud Guarantee:</strong> All core hashing, baseline comparison, and history logging require zero external network dependencies or internet access, ensuring safe operation in completely air-gapped environments.
      </div>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 4</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 5: SYSTEM ARCHITECTURE & WORKFLOW                                    -->
<!-- ========================================================================= -->
<div class="page" id="page-5">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">System Architecture & Workflow</h1>
        <div class="page-subtitle">End-to-End Cryptographic Verification Pipeline and Layered Security Flow</div>
      </div>

      <div class="goal-box">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Illustrate the complete architectural topology and 7-phase execution lifecycle governing data ingestion, chunked hashing, database persistence, and comparison logic.
        </div>
      </div>

      <div class="section-title">🏗️ High-Level System Architecture Diagram</div>
      <div class="code-block" style="font-size: 6.7pt; line-height: 1.18; padding: 3px 6px; margin: 2px 0;">+-----------------------------------------------------------------------------------+
|                           PRESENTATION / INTERFACE LAYER                          |
|   +-------------------------------------+   +---------------------------------+   |
|   |   Web UI (Vanilla HTML5 / CSS3 / JS)|   |   Command Line (cli.py / Click) |   |
|   +-------------------------------------+   +---------------------------------+   |
+------------------------------------------+----------------------------------------+
                                           | HTTP REST API / Direct CLI Calls
                                           v
+-----------------------------------------------------------------------------------+
|                        APPLICATION CONTROLLER (web/server.py)                     |
|  Endpoints: /api/analyze | /api/baseline | /api/verify | /api/history | /api/stats|
+------------------------------------------+----------------------------------------+
                                           | Sanitized Request Context
                                           v
+-----------------------------------------------------------------------------------+
|                         DEFENSIVE INGESTION & FILE HANDLER                        |
|  core/file_handler.py: Null-Byte Strip | Canonical Path Resolution | Staging Guard |
+------------------------------------------+----------------------------------------+
                                           | Validated Binary Stream Pointer
                                           v
+-----------------------------------------------------------------------------------+
|                       SHA-256 CHUNKED CRYPTOGRAPHIC ENGINE                        |
|  core/hasher.py: 64 KB Buffer Stream Reading | OpenSSL C-Accelerated SHA-256     |
+---------------------+---------------------------------------+---------------------+
                      | Current Digest                                | Stored Baseline
                      v                                               v
+---------------------------------------------+   +---------------------------------+
|     DETERMINISTIC COMPARISON ENGINE         |   |    SQLITE RELATIONAL DATABASE   |
|     core/comparator.py                      |   |    core/database.py             |
|                                             |   |                                 |
|  - MATCHED     (H_curr == H_base)           |<--|  - baselines table              |
|  - MODIFIED    (H_curr != H_base)           |   |  - verification_history table   |
|  - MISSING     (File removed from disk)     |   |                                 |
|  - ERROR       (No baseline / Access fault) |   |  ACID Transaction Management    |
+---------------------+-----------------------+   +---------------------------------+
                      | Final Verdict & Metadata
                      v
+-----------------------------------------------------------------------------------+
|                          REPORT GENERATOR & AUDIT EXPORTER                        |
|  core/reporter.py: Text Certificate Export | JSON API Serialization | History Log |
+-----------------------------------------------------------------------------------+</div>

      <div class="section-title">🔄 Step-by-Step Execution Lifecycle</div>
      <ul class="clean-list" style="margin: 2px 0 2px 0; padding-left: 15px; font-size: 8.7pt; line-height: 1.35;">
        <li style="margin-bottom: 2px;"><strong>Phase 1 — Ingestion & Sanitation:</strong> File path is supplied via file picker, drag-and-drop zone, or CLI argument. <code>FileHandler.validate_path()</code> eliminates null bytes and resolves the canonical absolute path.</li>
        <li style="margin-bottom: 2px;"><strong>Phase 2 — Binary Stream Access:</strong> File existence and read permissions are verified. The target is opened in read-only binary mode (<code>rb</code>) with strict directory exclusion.</li>
        <li style="margin-bottom: 2px;"><strong>Phase 3 — Chunked Hashing:</strong> <code>Hasher.calculate_sha256()</code> reads the stream in sequential 64 KB chunks, feeding the accumulator without loading the entire file into system RAM.</li>
        <li style="margin-bottom: 2px;"><strong>Phase 4 — Baseline Lookup:</strong> <code>DatabaseManager.get_baseline_by_path()</code> queries the local SQLite database for an existing authoritative record matching the canonical path.</li>
        <li style="margin-bottom: 2px;"><strong>Phase 5 — Hash Comparison:</strong> <code>Comparator.verify_file()</code> executes constant-time string comparison between the baseline digest and current digest.</li>
        <li style="margin-bottom: 2px;"><strong>Phase 6 — State Categorization:</strong> The engine deterministically emits <code>MATCHED</code>, <code>MODIFIED</code>, <code>MISSING</code>, or <code>ERROR</code> alongside context-isolated security advisories.</li>
        <li style="margin-bottom: 2px;"><strong>Phase 7 — Audit Trail Persistence:</strong> The verdict, timestamps, and hashes are committed to <code>verification_history</code>, enabling immediate text and JSON report generation.</li>
      </ul>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 5</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 6: APPLICATION SETUP & MAIN INTERFACE                                -->
<!-- ========================================================================= -->
<div class="page" id="page-6">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">Application Setup & Main Interface</h1>
        <div class="page-subtitle">Launching File Integrity Checker and Navigating the Central Dashboard</div>
      </div>

      <div class="goal-box">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Document the verified installation procedure, server startup sequence, and the architectural components of the primary graphical dashboard.
        </div>
      </div>

      <div class="section-title">🚀 Verified Installation & Cold Launch Procedure</div>
      <div class="code-block"># 1. Navigate to workspace
cd &lt;project-folder&gt;

# 2. Initialize isolated virtual environment & install dependencies
python -m venv .venv
.\\.venv\\Scripts\\activate            # Windows (or: source .venv/bin/activate on Linux/macOS)
pip install -r requirements.txt

# 3. Launch local Flask application server (or CLI via python cli.py)
python app.py
# * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)</div>

      <div class="section-title">🖥️ Primary Verification Dashboard</div>
      <div class="screenshot-container">
        <img src="{img_dashboard}" class="screenshot-img" style="max-height: 104mm;" alt="Figure 1: Main Dashboard">
        <div class="screenshot-caption">Figure 1: File Integrity Checker central dashboard interface captured from the real running application.</div>
      </div>

      <div class="section-title">🔍 Interface Component Breakdown</div>
      <ul class="clean-list">
        <li><strong>① Main Navigation Header:</strong> Accessible tab controls providing switching across Dashboard, File Analysis, Results, History & Baselines, and About screens.</li>
        <li><strong>② Telemetry Metric Counters:</strong> Dynamically queries <code>/api/stats</code> upon load, displaying Baselines Established (5), Files Verified (9), Integrity Matches (5), and Security Alerts (4).</li>
        <li><strong>③ Quick Verification Console:</strong> Path input box and native OS file selector with mouse cursor positioned over the "Verify File" action button.</li>
        <li><strong>④ Hero Action Controls:</strong> Privacy-first status pill and direct action buttons to trigger file analysis or inspect historical verification logs.</li>
      </ul>

      <div class="key-takeaway">
        <strong>Operational Observation:</strong> The web interface initializes in under 0.5 seconds on local loopback (<code>127.0.0.1:5000</code>). SQLite database connections are opened ephemerally per request, avoiding file lock contention.
      </div>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 6</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 7: CORE WORKFLOW                                                     -->
<!-- ========================================================================= -->
<div class="page" id="page-7">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">File Integrity Verification Workflow</h1>
        <div class="page-subtitle">Deep-Dive Inspection of Baseline Creation and Cryptographic Verification</div>
      </div>

      <div class="goal-box">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Examine the end-to-end operational workflow of selecting a target file, calculating its cryptographic digest, establishing an authoritative baseline, and performing subsequent state verification.
        </div>
      </div>

      <div class="section-title">🔬 File Analysis & Baseline Control Console</div>
      <div class="screenshot-container">
        <img src="{img_analysis}" class="screenshot-img" style="max-height: 98mm;" alt="Figure 2: File Analysis Interface">
        <div class="screenshot-caption">Figure 2: File Analysis interface displaying cryptographic digest calculation and baseline establishment controls.</div>
      </div>

      <div class="section-title">🔍 Interface Component Breakdown</div>
      <ul class="clean-list">
        <li><strong>① Selected Target File Details:</strong> Renders resolved file name (<code>security_policy.pdf</code>), canonical absolute path, human-readable file size (3.8 KB), and filesystem last-modified timestamp.</li>
        <li><strong>② SHA-256 Cryptographic Checksum Box:</strong> Displays the complete 64-character hexadecimal digest with an integrated single-click clipboard copy utility.</li>
        <li><strong>③ Create Baseline Action Button:</strong> High-visibility emerald button with mouse cursor positioned directly over it to register the file's current hash as the authoritative reference.</li>
        <li><strong>④ Verify File Action Button:</strong> Primary blue action button enabling immediate comparison of the file's current disk bytes against the stored baseline.</li>
        <li><strong>⑤ Drag-and-Drop Ingestion Zone:</strong> Seamless drag-and-drop zone with native File API integration, preventing browser navigation while ingesting PDF, DOCX, Python, or archive binaries.</li>
      </ul>

      <div class="section-title">📋 Step-by-Step Operator Interaction Workflow</div>
      <ul class="clean-list">
        <li><strong>Step 1 — Target Selection:</strong> Ingest target via drag-and-drop zone or native OS file picker. The frontend dispatches a POST request to <code>/api/analyze</code>.</li>
        <li><strong>Step 2 — Digest Calculation:</strong> The backend computes the streaming SHA-256 hash using 64 KB buffers, returning the canonical digest and metadata without altering the source file.</li>
        <li><strong>Step 3 — Baseline Registration:</strong> Clicking "Create Baseline" invokes <code>/api/baseline</code>. The system executes an idempotent SQL upsert into the <code>baselines</code> table, logging UTC timestamp.</li>
        <li><strong>Step 4 — Subsequent Verification:</strong> At any later point, the operator triggers "Verify File" (or uses <code>cli.py verify &lt;path&gt;</code>). The engine re-reads the file from disk, hashes it afresh, and queries the database.</li>
        <li><strong>Step 5 — State Resolution:</strong> The comparator performs an exact equality check between the fresh hash and the baseline hash, redirecting to the Verification Result view with full advisory details.</li>
      </ul>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 7</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 8: VERIFICATION RESULTS — MATCHED & MODIFIED                         -->
<!-- ========================================================================= -->
<div class="page" id="page-8">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">Verification Results: MATCHED & MODIFIED</h1>
        <div class="page-subtitle">Empirical Evidence of Hash Equality and Tampering Detection</div>
      </div>

      <div class="goal-box" style="padding: 4px 8px; margin-bottom: 4px;">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Examine the visual output and structural details of the two primary baseline comparison states: verified intact (MATCHED) and unauthorized modification (MODIFIED).
        </div>
      </div>

      <div class="section-title" style="margin-top: 3px; margin-bottom: 1px;">✅ State 1: MATCHED Result (Target File Unaltered)</div>
      <div class="screenshot-container" style="margin: 2px 0 1px 0;">
        <img src="{img_matched}" class="screenshot-img" style="max-height: 60mm;" alt="Figure 3: MATCHED Result">
        <div class="screenshot-caption" style="margin-top: 2px;">Figure 3: Verification Result screen showing MATCHED state with identical baseline and current SHA-256 hashes.</div>
      </div>
      <ul class="clean-list" style="margin: 2px 0 4px 0; font-size: 8.3pt; line-height: 1.3;">
        <li style="margin-bottom: 2px;"><strong>① Emerald MATCHED Verdict Banner:</strong> Confirms bit-for-bit cryptographic consistency with the authoritative baseline.</li>
        <li style="margin-bottom: 2px;"><strong>② Target File Details:</strong> Displays verified file name (<code>security_policy.pdf</code>), canonical path, size, and timestamp.</li>
        <li style="margin-bottom: 2px;"><strong>③ Baseline SHA-256 Digest:</strong> Authoritative baseline digest retrieved from SQLite storage.</li>
        <li style="margin-bottom: 2px;"><strong>④ Current SHA-256 Digest:</strong> Freshly calculated digest of current disk bytes confirming exact match.</li>
        <li style="margin-bottom: 2px;"><strong>⑤ Download Report Action Button:</strong> Direct export action with mouse cursor positioned directly over "Download Report".</li>
      </ul>

      <div class="section-title" style="margin-top: 3px; margin-bottom: 1px;">⚠️ State 2: MODIFIED Result (Tampering Detected)</div>
      <div class="screenshot-container" style="margin: 2px 0 1px 0;">
        <img src="{img_modified}" class="screenshot-img" style="max-height: 60mm;" alt="Figure 4: MODIFIED Result">
        <div class="screenshot-caption" style="margin-top: 2px;">Figure 4: Verification Result screen showing MODIFIED state with divergent SHA-256 hashes flagging tampering.</div>
      </div>
      <ul class="clean-list" style="margin: 2px 0 2px 0; font-size: 8.3pt; line-height: 1.3;">
        <li style="margin-bottom: 2px;"><strong>① Amber MODIFIED Alert Banner:</strong> Immediately alerts the operator that the current file differs from its authoritative baseline.</li>
        <li style="margin-bottom: 2px;"><strong>② Target File Details:</strong> Identifies target path and records the exact timestamp of modification detection.</li>
        <li style="margin-bottom: 2px;"><strong>③ Baseline SHA-256 Digest:</strong> Authoritative reference digest stored in the database.</li>
        <li style="margin-bottom: 2px;"><strong>④ Current Divergent SHA-256 Digest:</strong> Freshly calculated hash demonstrating single-bit tamper detection.</li>
        <li style="margin-bottom: 2px;"><strong>⑤ Download Report Action Button:</strong> Direct export action with mouse cursor positioned directly over "Download Report".</li>
      </ul>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 8</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 9: VERIFICATION RESULTS — MISSING & ERROR                            -->
<!-- ========================================================================= -->
<div class="page" id="page-9">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">Verification Results: MISSING & ERROR</h1>
        <div class="page-subtitle">Empirical Evidence of Target Deletion and Unbaselined File Handling</div>
      </div>

      <div class="goal-box" style="padding: 4px 8px; margin-bottom: 4px;">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Examine the handling of anomalous operational states: detecting deleted files (MISSING) and enforcing baseline prerequisites (ERROR / NO_BASELINE).
        </div>
      </div>

      <div class="section-title" style="margin-top: 3px; margin-bottom: 1px;">🔍 State 3: MISSING Result (Target Absent from Disk)</div>
      <div class="screenshot-container" style="margin: 2px 0 1px 0;">
        <img src="{img_missing}" class="screenshot-img" style="max-height: 60mm;" alt="Figure 5: MISSING Result">
        <div class="screenshot-caption" style="margin-top: 2px;">Figure 5: Verification Result screen showing MISSING state when a baselined target is absent from filesystem.</div>
      </div>
      <ul class="clean-list" style="margin: 2px 0 4px 0; font-size: 8.3pt; line-height: 1.3;">
        <li style="margin-bottom: 2px;"><strong>① Purple MISSING File Alert Banner:</strong> Flags that an authoritative baseline exists in SQLite, but the file is absent from disk.</li>
        <li style="margin-bottom: 2px;"><strong>② Target File Notice:</strong> Details the target path and confirms the file cannot be located on the filesystem.</li>
        <li style="margin-bottom: 2px;"><strong>③ Expected Baseline Hash:</strong> Displays the expected SHA-256 digest registered in the baseline database.</li>
        <li style="margin-bottom: 2px;"><strong>④ Deletion / Rename Guidance Advisory:</strong> Instructs administrator to investigate file deletion, with cursor positioned on "Select & Analyze File".</li>
      </ul>

      <div class="section-title" style="margin-top: 3px; margin-bottom: 1px;">🛑 State 4: ERROR / NO_BASELINE Result (Unbaselined File)</div>
      <div class="screenshot-container" style="margin: 2px 0 1px 0;">
        <img src="{img_no_baseline}" class="screenshot-img" style="max-height: 60mm;" alt="Figure 6: ERROR Result">
        <div class="screenshot-caption" style="margin-top: 2px;">Figure 6: Verification Result screen showing ERROR state when verifying a file with no pre-existing baseline.</div>
      </div>
      <ul class="clean-list" style="margin: 2px 0 2px 0; font-size: 8.3pt; line-height: 1.3;">
        <li style="margin-bottom: 2px;"><strong>① Crimson ERROR Banner:</strong> Informs the operator that verification cannot proceed without an established baseline reference.</li>
        <li style="margin-bottom: 2px;"><strong>② Selected File Path Notice:</strong> Displays selected target path and notes that no baseline record matches this path.</li>
        <li style="margin-bottom: 2px;"><strong>③ No-Baseline Guidance Advisory:</strong> Context-isolated security advisory instructing user to establish a baseline first.</li>
        <li style="margin-bottom: 2px;"><strong>④ Select & Analyze File Action:</strong> Direct navigation control with mouse cursor positioned over "Select & Analyze File".</li>
      </ul>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 9</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 10: SHA-256 HASH ENGINE & BASELINES VAULT                            -->
<!-- ========================================================================= -->
<div class="page" id="page-10">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">SHA-256 Hash Engine & Baselines Management</h1>
        <div class="page-subtitle">Chunked Stream Processing, Deterministic Hashing, and Baselines Vault</div>
      </div>

      <div class="goal-box" style="padding: 4px 8px; margin-bottom: 4px;">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Detail the 64 KB chunked buffer implementation in core/hasher.py, demonstrate the Avalanche Effect with actual test data, and document baseline vault management.
        </div>
      </div>

      <div class="section-title" style="margin-top: 3px; margin-bottom: 1px;">⚙️ Chunked Stream-Buffering Architecture (core/hasher.py)</div>
      <p class="explanation-text" style="margin-bottom: 3px;">
        Reading an entire multi-gigabyte file into memory at once causes severe memory spikes. File Integrity Checker processes files in sequential 64 KB (65,536 bytes) chunks:
      </p>
      <div class="code-block" style="margin: 2px 0 4px 0; padding: 4px 8px; font-size: 8pt;">def calculate_sha256(file_path: str, chunk_size: int = 65536) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()</div>

      <div class="section-title" style="margin-top: 3px; margin-bottom: 1px;">⚡ Empirical Avalanche Effect Demonstration</div>
      <p class="explanation-text" style="margin-bottom: 3px;">
        In our controlled testing, modifying exactly 1 character in <code>security_policy.pdf</code> produced a completely different SHA-256 digest:
      </p>
      <div class="code-block" style="margin: 2px 0 4px 0; padding: 4px 8px; font-size: 7.8pt;">Original:  860dc6c39a039755f114631ab2f34ee3cffb94f6fef7e067cbb3eb624c9c6463
Tampered:  52b618cfce998c0b2f34e64f72782e4e16428c0b875ad28913d8036d0f507c92
Bit Diff:  132 out of 256 bits changed (51.56% variance) - Avalanche Effect verified.</div>

      <div class="section-title" style="margin-top: 3px; margin-bottom: 1px;">🏛️ Authoritative Baselines Vault Management Table</div>
      <div class="screenshot-container" style="margin: 2px 0 1px 0;">
        <img src="{img_baselines}" class="screenshot-img" style="max-height: 62mm;" alt="Figure 7: Baselines Vault">
        <div class="screenshot-caption" style="margin-top: 2px;">Figure 7: Authoritative Baselines Vault interface displaying stored hashes, timestamps, and controls.</div>
      </div>

      <div class="section-title" style="margin-top: 3px; margin-bottom: 1px;">🔍 Interface Component Breakdown</div>
      <ul class="clean-list" style="margin: 2px 0 2px 0; font-size: 8.5pt; line-height: 1.32;">
        <li style="margin-bottom: 2px;"><strong>① Stored Baseline Entry (Row 1):</strong> Primary key ID, file name, human-readable file size, and creation timestamp.</li>
        <li style="margin-bottom: 2px;"><strong>② Stored SHA-256 Digest Preview:</strong> Monospaced truncated representation with full hover tooltip.</li>
        <li style="margin-bottom: 2px;"><strong>③ One-Click Re-Verification Action:</strong> Re-runs integrity check against the current disk state. Mouse cursor positioned over "Verify".</li>
        <li style="margin-bottom: 2px;"><strong>④ Baseline Deletion Action:</strong> Safe baseline deletion with confirmation modal protection.</li>
      </ul>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 10</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 11: VERIFICATION HISTORY & REPORTS                                   -->
<!-- ========================================================================= -->
<div class="page" id="page-11">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">Verification History & Reports</h1>
        <div class="page-subtitle">Chronological Logging, Status Filtering, and Export Reports</div>
      </div>

      <div class="goal-box">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Demonstrate the audit logging architecture, status-based search filtering, and structured report generation capabilities.
        </div>
      </div>

      <div class="section-title">📜 Chronological Verification History Logs</div>
      <div class="screenshot-container">
        <img src="{img_history}" class="screenshot-img" style="max-height: 70mm;" alt="Figure 8: History Logs Table">
        <div class="screenshot-caption">Figure 8: Verification History log with color-coded status badges, filter controls, and action triggers.</div>
      </div>

      <div class="section-title">📄 Verification Audit Report (Modal View)</div>
      <div class="screenshot-container">
        <img src="{img_report_modal}" class="screenshot-img" style="max-height: 70mm;" alt="Figure 9: Report Modal">
        <div class="screenshot-caption">Figure 9: Monospaced Verification Audit Report modal with clipboard and download options.</div>
      </div>

      <div class="section-title">🔍 Interface Component Breakdown</div>
      <ul class="clean-list">
        <li><strong>① History Table Body:</strong> Chronological log capturing file path, baseline hash, current hash, status verdict, and UTC timestamp.</li>
        <li><strong>② Status Filter Dropdown:</strong> Filters records by status (<code>ALL</code>, <code>MATCHED</code>, <code>MODIFIED</code>, <code>MISSING</code>, <code>ERROR</code>).</li>
        <li><strong>③ Report Action Trigger:</strong> Opens monospaced audit report modal. Mouse cursor positioned over "Report".</li>
        <li><strong>④ Save to File Download Action:</strong> Exports report as text/JSON file. Mouse cursor positioned over "Save to File".</li>
      </ul>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 11</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 12: EDUCATIONAL GUIDANCE & SYSTEM CONCEPTS                           -->
<!-- ========================================================================= -->
<div class="page" id="page-12">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">Educational Guidance & System Concepts</h1>
        <div class="page-subtitle">Hashing Fundamentals, Encryption Separation, and Security Guidelines</div>
      </div>

      <div class="goal-box">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Examine the educational concepts embedded directly within the application, clarifying the difference between hashing and encryption, and defining defensive boundaries.
        </div>
      </div>

      <div class="section-title">📖 Educational About Screen</div>
      <div class="screenshot-container">
        <img src="{img_about}" class="screenshot-img" style="max-height: 80mm;" alt="Figure 10: About Screen">
        <div class="screenshot-caption">Figure 10: Educational About screen articulating hashing fundamentals, encryption separation, and scope boundaries.</div>
      </div>

      <div class="section-title">🔍 Interface Component Breakdown</div>
      <ul class="clean-list">
        <li><strong>① Cryptographic Hashing Concept Card:</strong> Explains one-way compression, collision resistance, and SHA-256 properties.</li>
        <li><strong>② Hashing vs. Encryption Separation Card:</strong> Clearly contrasts irreversible integrity checking with reversible data confidentiality.</li>
        <li><strong>③ Operational Scope Boundaries Card:</strong> Articulates local execution boundaries, absence of cloud telemetry, and safe read-only file access.</li>
      </ul>

      <div class="section-title">⚖️ Cryptographic Hashing vs. Symmetric Encryption</div>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 25%;">Property</th>
            <th style="width: 37%;">Cryptographic Hashing (SHA-256)</th>
            <th style="width: 38%;">Symmetric Encryption (e.g., AES-256)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Mathematical Nature</strong></td>
            <td>One-way mathematical compression function.</td>
            <td>Two-way reversible mathematical permutation.</td>
          </tr>
          <tr>
            <td><strong>Reversibility</strong></td>
            <td>Irreversible: plaintext cannot be derived from hash.</td>
            <td>Reversible: plaintext is restored using secret key.</td>
          </tr>
          <tr>
            <td><strong>Output Length</strong></td>
            <td>Fixed length: 256 bits (64 hexadecimal characters).</td>
            <td>Variable length: proportional to input plaintext size.</td>
          </tr>
          <tr>
            <td><strong>Key Requirement</strong></td>
            <td>No key required (unkeyed cryptographic primitive).</td>
            <td>Requires secure key generation and exchange.</td>
          </tr>
          <tr>
            <td><strong>Primary Objective</strong></td>
            <td><strong>INTEGRITY</strong> (detect unauthorized tampering).</td>
            <td><strong>CONFIDENTIALITY</strong> (prevent unauthorized reading).</td>
          </tr>
        </tbody>
      </table>

      <div class="key-takeaway">
        <strong>Educational Finding:</strong> The application explicitly reminds users that a MATCHED hash guarantees consistency against the baseline, but does not certify that the baseline file itself was free from pre-existing malware.
      </div>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 12</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 13: QUALITY ASSURANCE & TEST MATRIX                                  -->
<!-- ========================================================================= -->
<div class="page" id="page-13">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">Quality Assurance & Test Matrix</h1>
        <div class="page-subtitle">Empirical Validation of Functional Capabilities and Automated Pytest Results</div>
      </div>

      <div class="goal-box">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Provide a formal quality assurance matrix mapping core functional and security specifications to empirical test results, substantiated by the automated pytest suite execution log.
        </div>
      </div>

      <div class="section-title">📋 Comprehensive Quality Assurance Matrix</div>
      <table class="data-table qa-table">
        <thead>
          <tr>
            <th style="width: 10%;">ID</th>
            <th style="width: 25%;">Test Case</th>
            <th style="width: 33%;">Action Performed</th>
            <th style="width: 22%;">Actual Output</th>
            <th style="width: 10%;">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>QA-01</strong></td>
            <td>Application Startup</td>
            <td>Initialize Flask server on local port 5000</td>
            <td>200 OK, assets served</td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
          <tr>
            <td><strong>QA-02</strong></td>
            <td>Path Input Sanitation</td>
            <td>Input path containing null bytes and quotes</td>
            <td>Null bytes rejected, cleaned</td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
          <tr>
            <td><strong>QA-03</strong></td>
            <td>Chunked SHA-256 Hashing</td>
            <td>Compute digest over 10 MB binary payload</td>
            <td>Steady memory, exact hash</td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
          <tr>
            <td><strong>QA-04</strong></td>
            <td>Directory Ingestion Block</td>
            <td>Submit directory path for hash analysis</td>
            <td>IsADirectoryError, 400 Bad Req</td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
          <tr>
            <td><strong>QA-05</strong></td>
            <td>Baseline SQLite Persistence</td>
            <td>Insert new baseline via <code>/api/baseline</code></td>
            <td>Atomic commit, UTC timestamp</td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
          <tr>
            <td><strong>QA-06</strong></td>
            <td>Unmodified File Verification</td>
            <td>Verify unchanged file against baseline</td>
            <td>Status: <code>MATCHED</code></td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
          <tr>
            <td><strong>QA-07</strong></td>
            <td>Single-Bit Tamper Detection</td>
            <td>Complement 1 bit in baselined PDF</td>
            <td>Status: <code>MODIFIED</code> (Alert)</td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
          <tr>
            <td><strong>QA-08</strong></td>
            <td>Deleted Target Detection</td>
            <td>Delete baselined file from disk and verify</td>
            <td>Status: <code>MISSING</code> (Alert)</td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
          <tr>
            <td><strong>QA-09</strong></td>
            <td>Unbaselined Target Check</td>
            <td>Verify target with no pre-existing baseline</td>
            <td>Status: <code>ERROR</code> (No Baseline)</td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
          <tr>
            <td><strong>QA-10</strong></td>
            <td>Security Advisory Isolation</td>
            <td>Inspect advisory on ERROR / NO_BASELINE</td>
            <td>MATCHED text suppressed</td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
          <tr>
            <td><strong>QA-11</strong></td>
            <td>Multi-Format Drag-and-Drop</td>
            <td>Ingest PDF, DOCX, ZIP via browser File API</td>
            <td>Parsed as raw bytes</td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
          <tr>
            <td><strong>QA-12</strong></td>
            <td>Arbitrary Download Block</td>
            <td>Attempt path traversal on download route</td>
            <td>403 Forbidden / 404 Not Found</td>
            <td><span class="badge-pass">PASS</span></td>
          </tr>
        </tbody>
      </table>

      <div class="section-title" style="margin-top: 3px; margin-bottom: 1px;">📊 Automated Test Suite Verification Evidence (pytest)</div>
      <div class="screenshot-container" style="margin: 2px 0 1px 0;">
        <img src="{img_pytest}" class="screenshot-img" style="max-height: 48mm;" alt="Figure 11: Pytest Test Suite Evidence">
        <div class="screenshot-caption" style="margin-top: 2px;">Figure 11: Automated pytest execution terminal evidence displaying 54 passing unit, integration, and security test cases.</div>
      </div>
      <ul class="clean-list" style="margin: 2px 0 2px 0; font-size: 8.3pt; line-height: 1.3;">
        <li style="margin-bottom: 2px;"><strong>① Test Session & Environment:</strong> Python 3.14.7 runtime, pytest 9.1.1 engine, and root configuration initialization.</li>
        <li style="margin-bottom: 2px;"><strong>② Test Suite Execution:</strong> Complete automated test collection passing across API, comparator, database, and security modules.</li>
        <li style="margin-bottom: 2px;"><strong>③ Final Test Verdict:</strong> 54 passed in 1.22s, confirming 100% test pass rate across all system modules.</li>
      </ul>

      <div class="key-takeaway">
        <strong>Quality Assurance Verdict:</strong> 100% test pass rate across 54 automated tests. All core hashing functions, path sanitation, database transactions, and deterministic comparison states are verified.
      </div>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 13</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 14: SECURITY CONSIDERATIONS & ROADMAP                                -->
<!-- ========================================================================= -->
<div class="page" id="page-14">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">Security Considerations & Roadmap</h1>
        <div class="page-subtitle">Defensive Threat Modeling, Current Boundaries, and Strategic Advancements</div>
      </div>

      <div class="goal-box">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Review the application's defensive security controls, identify current technical boundaries, and outline a realistic future development roadmap.
        </div>
      </div>

      <div class="section-title">🛡️ Defensive Security Controls</div>
      <ul class="clean-list">
        <li><strong>Safe Path Handling & Canonicalization:</strong> Paths are canonicalized via <code>os.path.abspath()</code> and checked for null bytes (<code>\x00</code>) to prevent null-byte injection and directory traversal attacks.</li>
        <li><strong>Read-Only Binary Access:</strong> Ingested files are opened strictly in binary read-only mode (<code>rb</code>). The application never executes files, scripts, or binary payloads.</li>
        <li><strong>Staging Directory & Download Guard:</strong> Uploaded drag-and-drop files are confined to an isolated staging directory. The download endpoint strictly blocks arbitrary filesystem reads.</li>
        <li><strong>Zero External Attack Surface:</strong> Zero telemetry beacons, external CDN dependencies, or cloud analytics exist. Network exposure is confined strictly to the user-specified local loopback address.</li>
      </ul>

      <div class="section-title">⚠️ Current Technical Limitations</div>
      <ul class="clean-list">
        <li><strong>On-Demand Static Checks:</strong> Current verification occurs when triggered by the operator or scheduled CLI script; continuous real-time kernel-level filesystem event watching is not yet implemented.</li>
        <li><strong>Single-Algorithm Fingerprint:</strong> Verification relies on SHA-256; multi-hash composite signing (e.g., SHA-256 + BLAKE3) is planned for future releases.</li>
        <li><strong>Local SQLite Database Protection:</strong> Integrity of the baseline repository depends on host filesystem Access Control Lists (ACLs); signed baselines will be introduced in future updates.</li>
      </ul>

      <div class="section-title">🚀 Strategic Technical Roadmap (Future Scope)</div>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 25%;">Future Enhancement</th>
            <th style="width: 40%;">Proposed Implementation</th>
            <th style="width: 35%;">Anticipated Security Impact</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Real-Time Filesystem Monitoring</strong></td>
            <td>Integrate Python <code>watchdog</code> daemon utilizing OS-level event APIs.</td>
            <td>Immediate notification upon unauthorized file modification.</td>
          </tr>
          <tr>
            <td><strong>Cryptographically Signed Baselines</strong></td>
            <td>Asymmetric Ed25519 or HMAC-SHA256 digital signatures over baseline database entries.</td>
            <td>Prevents offline tampering or malicious database modification by local attackers.</td>
          </tr>
          <tr>
            <td><strong>Multi-Algorithm Composite Hashes</strong></td>
            <td>Concurrent calculation of SHA-256 and BLAKE3 digests in parallel.</td>
            <td>Long-term cryptographic agility and resilience against algorithm weaknesses.</td>
          </tr>
          <tr>
            <td><strong>Enterprise SIEM Forwarder</strong></td>
            <td>RFC 5424 Syslog / CEF JSON socket emitter forwarding alerts to external log collectors.</td>
            <td>Centralized audit visibility across multi-host environments.</td>
          </tr>
        </tbody>
      </table>

      <div class="key-takeaway">
        <strong>Strategic Summary:</strong> File Integrity Checker establishes a reliable local verification foundation. Future iterations will build upon this core to deliver continuous real-time monitoring and cryptographically signed baseline vaults.
      </div>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 14</span>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 15: PROJECT CONCLUSION                                               -->
<!-- ========================================================================= -->
<div class="page" id="page-15">
  <div class="page-border">
    <div class="page-content">
      <div class="page-header">
        <h1 class="page-title">Project Conclusion & Summary</h1>
        <div class="page-subtitle">Completed Technical Milestones, Practical Value, and Authorship Details</div>
      </div>

      <div class="goal-box">
        <div class="goal-title">🎯 Goal</div>
        <div>
          Summarize completed technical achievements, demonstrate real-world defensive cybersecurity relevance, and provide formal project sign-off and authorship credits.
        </div>
      </div>

      <div class="section-title">📋 Summary of Completed Technical Work</div>
      <p class="explanation-text">
        The <strong>File Integrity Checker</strong> project has been successfully engineered, verified, and documented as a lightweight, functional cybersecurity utility:
      </p>
      <ul class="clean-list">
        <li><strong>Engineered Stream Hashing Engine:</strong> Implemented chunked 64 KB buffer SHA-256 calculation capable of processing files of arbitrary size with low, steady memory utilization.</li>
        <li><strong>Constructed Resilient Database Vault:</strong> Developed an ACID-compliant SQLite baseline and history schema supporting idempotent upsert transactions and audit logs.</li>
        <li><strong>Validated 4-State Verification Engine:</strong> Tested deterministic status categorization across <code>MATCHED</code>, <code>MODIFIED</code>, <code>MISSING</code>, and <code>ERROR</code> states with context-isolated security advisories.</li>
        <li><strong>Implemented Double Interface:</strong> Delivered a responsive local web interface with drag-and-drop file ingestion alongside a comprehensive command-line interface (<code>cli.py</code>).</li>
        <li><strong>Executed Comprehensive Quality Assurance:</strong> Achieved a 100% pass rate across 54 automated pytest test suites validating APIs, path sanitation, and end-to-end verification workflows.</li>
      </ul>

      <div class="section-title">🛡️ Practical Cybersecurity Relevance</div>
      <p class="explanation-text">
        File Integrity Monitoring (FIM) constitutes a foundational pillar in industry compliance standards, including <strong>PCI-DSS Requirement 11.5</strong>, <strong>NIST SP 800-53 (SI-7)</strong>, and <strong>ISO/IEC 27001</strong>. This project demonstrates practical proficiency in cryptographic file verification, secure programming practices, and automated testing.
      </p>

      <div class="section-title">👤 Project Authorship & Repository Details</div>
      <table class="data-table">
        <tbody>
          <tr>
            <td style="width: 25%;"><strong>Project Author:</strong></td>
            <td style="width: 75%;"><strong>Vivek Rathod</strong></td>
          </tr>
          <tr>
            <td><strong>GitHub Repository:</strong></td>
            <td><a href="https://github.com/Vivekkk20/file-integrity-checker" style="color: #0284c7; text-decoration: none;">https://github.com/Vivekkk20/file-integrity-checker</a></td>
          </tr>
          <tr>
            <td><strong>Verification Date:</strong></td>
            <td>September 2026 • Verified on Windows 11 Enterprise (x64) with Python 3.14.7</td>
          </tr>
        </tbody>
      </table>

      <div class="key-takeaway" style="margin-top: 12px;">
        <strong>Final Outcome:</strong> File Integrity Checker provides a reliable local security utility that enables users to detect unauthorized file tampering through deterministic SHA-256 baseline comparison.
      </div>
    </div>
    <div class="page-footer">
      <span>File Integrity Checker</span>
      <span>Page 15</span>
    </div>
  </div>
</div>

</body>
</html>
"""
    return html


def build_markdown() -> str:
    md = """# File Integrity Checker — Professional Project Documentation
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
"""
    return md


def main():
    print("[*] Generating HTML document...")
    html_content = build_html()
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Saved {HTML_FILE}")

    print("[*] Generating Markdown document...")
    md_content = build_markdown()
    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[OK] Saved {MD_FILE}")

    print("[*] Compiling PDF via Playwright Chromium...")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        page.goto(f"file:///{str(HTML_FILE).replace(os.sep, '/')}", wait_until="networkidle")
        page.pdf(
            path=str(PDF_FILE),
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"},
        )
        browser.close()
    print(f"[OK] Saved {PDF_FILE}")

    # Verify page count
    reader = pypdf.PdfReader(str(PDF_FILE))
    total_pages = len(reader.pages)
    print(f"[*] Verifying PDF page count: {total_pages} pages detected.")
    return total_pages


if __name__ == "__main__":
    main()
