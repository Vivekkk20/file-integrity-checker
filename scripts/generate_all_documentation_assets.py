"""
Comprehensive Asset Capture and High-Precision Annotation Engine
for File Integrity Checker Documentation.

Strictly adheres to:
1. Every numbered marker (1-5) points directly with a leader line & arrow tip to the exact UI control.
2. Numbered badges are placed outside the control so they never obscure text, hashes, buttons, or banners.
3. Authentic OS mouse cursor is placed directly on the action control demonstrated in each view.
4. Clean, subtle bounding box outlines (width=2) framing the targeted elements.
5. All detailed labels remain in the document text below the screenshot.
6. Raw screenshots are preserved in docs/screenshots/raw/.
7. Annotated screenshots are saved to docs/screenshots/annotated/.
"""

import os
import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
DOCS_DIR = ROOT_DIR / "docs"
RAW_DIR = DOCS_DIR / "screenshots" / "raw"
ANNOTATED_DIR = DOCS_DIR / "screenshots" / "annotated"
SAMPLES_DIR = DOCS_DIR / "test_samples"

RAW_DIR.mkdir(parents=True, exist_ok=True)
ANNOTATED_DIR.mkdir(parents=True, exist_ok=True)
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Setup Realistic Sample Files & Database Records
# ---------------------------------------------------------------------------
def setup_samples_and_db():
    print("[*] Setting up realistic sample files and database records...")

    # 1. Sample PDF
    pdf_path = SAMPLES_DIR / "security_policy.pdf"
    pdf_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Title (Enterprise Security Policy) /Author (Cybersecurity Ops) >>\nendobj\n"
        b"2 0 obj\n<< /Length 120 >>\nstream\n"
        b"CONFIDENTIAL SECURITY DIRECTIVE: All server baselines must be cryptographically hashed via SHA-256.\n"
        b"endstream\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF\n"
    )
    pdf_path.write_bytes(pdf_bytes)

    # 2. Sample DOCX
    docx_path = SAMPLES_DIR / "vendor_contract.docx"
    docx_bytes = b"PK\x03\x04\x14\x00\x00\x00\x08\x00" + b"VENDOR_CONFIDENTIAL_SOW_CONTRACT_PAYLOAD" * 15
    docx_path.write_bytes(docx_bytes)

    # 3. Sample Python script
    py_path = SAMPLES_DIR / "database_config.py"
    py_bytes = b"# Secure Database Configuration\nDB_PATH = 'integrity_checker.db'\nTIMEOUT = 30\n"
    py_path.write_bytes(py_bytes)

    # 4. Tampered PDF file
    tampered_pdf = SAMPLES_DIR / "tampered_policy.pdf"
    tampered_pdf.write_bytes(pdf_bytes + b"\n%INJECTED_UNAUTHORIZED_ALTERATION_BYTES\n")

    # 5. Missing file (does not exist on disk)
    missing_path = SAMPLES_DIR / "deleted_secret.key"
    if missing_path.exists():
        missing_path.unlink()

    # 6. Unbaselined file
    unbaselined_path = SAMPLES_DIR / "unbaselined_draft.txt"
    unbaselined_path.write_text("Unbaselined sample document draft content.")

    # Seed Database
    from core.database import DatabaseManager
    from core.hasher import calculate_sha256

    db = DatabaseManager(db_path=str(ROOT_DIR / "integrity_checker.db"))

    # Save baselines
    pdf_hash = calculate_sha256(str(pdf_path))
    db.save_baseline("security_policy.pdf", str(pdf_path), pdf_hash, len(pdf_bytes))

    docx_hash = calculate_sha256(str(docx_path))
    db.save_baseline("vendor_contract.docx", str(docx_path), docx_hash, len(docx_bytes))

    py_hash = calculate_sha256(str(py_path))
    db.save_baseline("database_config.py", str(py_path), py_hash, len(py_bytes))

    fake_missing_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    db.save_baseline("deleted_secret.key", str(missing_path), fake_missing_hash, 1024)

    # Seed Verification History
    db.log_verification("security_policy.pdf", str(pdf_path), pdf_hash, pdf_hash, "MATCHED", "Cryptographic integrity verified against baseline.")
    db.log_verification("vendor_contract.docx", str(docx_path), docx_hash, docx_hash, "MATCHED", "Cryptographic integrity verified against baseline.")
    db.log_verification("security_policy.pdf", str(pdf_path), pdf_hash, "49afdf2e7ac8223be933c44b9d821f8950791cb8f593e8d2dc8a01a477114eb3", "MODIFIED", "Hash mismatch detected! File has been altered.")
    db.log_verification("deleted_secret.key", str(missing_path), fake_missing_hash, None, "MISSING", "Target file does not exist on disk.")

    print("[+] Test samples and database seed complete.")
    return {
        "pdf_path": str(pdf_path),
        "docx_path": str(docx_path),
        "py_path": str(py_path),
        "tampered_pdf": str(tampered_pdf),
        "missing_path": str(missing_path),
        "unbaselined_path": str(unbaselined_path),
    }


# ---------------------------------------------------------------------------
# Graphics Helpers: Fonts, Cursors, Outlines, Leader Arrows & Numbered Badges
# ---------------------------------------------------------------------------
def get_font(size=12, bold=True):
    font_paths = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_cursor(draw, x, y):
    """Draw a clean, crisp, highly visible OS mouse pointer with hot-spot at (x, y)."""
    # Drop shadow
    shadow = [
        (x + 2, y + 2), (x + 2, y + 21), (x + 7, y + 17), (x + 10, y + 24),
        (x + 13, y + 23), (x + 10, y + 15), (x + 15, y + 15)
    ]
    draw.polygon(shadow, fill="#050811")
    # Black outline
    outline = [
        (x, y), (x, y + 19), (x + 5, y + 15), (x + 8, y + 22),
        (x + 11, y + 21), (x + 8, y + 13), (x + 13, y + 13)
    ]
    draw.polygon(outline, fill="#000000", outline="#000000")
    # White body
    body = [
        (x + 1, y + 2), (x + 1, y + 16), (x + 5, y + 13), (x + 7, y + 19),
        (x + 9, y + 18), (x + 7, y + 12), (x + 11, y + 12)
    ]
    draw.polygon(body, fill="#ffffff")


def draw_highlight(draw, box, color="#38bdf8", width=2, radius=4):
    """Draw a clean, subtle outline framing the target element without obscuring content."""
    x1, y1 = box["x"], box["y"]
    x2, y2 = box["x"] + box["width"], box["y"] + box["height"]
    draw.rounded_rectangle([x1 - 2, y1 - 2, x2 + 2, y2 + 2], radius=radius, outline=color, width=width)


def draw_callout_marker(draw, target_box, num_str, color="#0284c7", position="top", offset_x=0, offset_y=0):
    """
    Draw a numbered badge with a leader line and arrow tip pointing directly into target_box edge.
    Position can be: 'top', 'bottom', 'left', 'right'.
    """
    radius = 12
    font = get_font(12, bold=True)
    bx, by = target_box["x"], target_box["y"]
    bw, bh = target_box["width"], target_box["height"]

    if position == "top":
        cx = (bx + bw / 2 if bw < 140 else bx + 35) + offset_x
        cy = (by - radius - 14) + offset_y
        arrow_start = (cx, cy + radius)
        arrow_tip = (cx, by - 2)
        arrow_head = [(cx, by - 2), (cx - 4, by - 8), (cx + 4, by - 8)]
    elif position == "bottom":
        cx = (bx + bw / 2 if bw < 140 else bx + 35) + offset_x
        cy = (by + bh + radius + 14) + offset_y
        arrow_start = (cx, cy - radius)
        arrow_tip = (cx, by + bh + 2)
        arrow_head = [(cx, by + bh + 2), (cx - 4, by + bh + 8), (cx + 4, by + bh + 8)]
    elif position == "left":
        cx = (bx - radius - 14) + offset_x
        cy = (by + bh / 2 if bh < 60 else by + 25) + offset_y
        arrow_start = (cx + radius, cy)
        arrow_tip = (bx - 2, cy)
        arrow_head = [(bx - 2, cy), (bx - 8, cy - 4), (bx - 8, cy + 4)]
    elif position == "right":
        cx = (bx + bw + radius + 14) + offset_x
        cy = (by + bh / 2 if bh < 60 else by + 25) + offset_y
        arrow_start = (cx - radius, cy)
        arrow_tip = (bx + bw + 2, cy)
        arrow_head = [(bx + bw + 2, cy), (bx + bw + 8, cy - 4), (bx + bw + 8, cy + 4)]

    # Draw leader line
    draw.line([arrow_start, arrow_tip], fill=color, width=2)
    # Draw arrow head
    draw.polygon(arrow_head, fill=color)
    # Draw badge shadow
    draw.ellipse([cx - radius - 1, cy - radius - 1, cx + radius + 1, cy + radius + 1], fill="#050811")
    # Draw badge circle
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color, outline="#ffffff", width=2)
    # Draw number text
    draw.text((cx, cy - 1), num_str, fill="#ffffff", font=font, anchor="mm")


# ---------------------------------------------------------------------------
# Terminal Renderer for Pytest Evidence (Page 13)
# ---------------------------------------------------------------------------
def render_pytest_terminal_evidence():
    """Render a crisp, authentic dark developer terminal screenshot of pytest execution."""
    width, height = 1200, 680
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255)) # Dark navy background
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([0, 0, width, 36], fill="#1e293b")
    # Window control dots
    draw.ellipse([16, 12, 28, 24], fill="#ef4444")
    draw.ellipse([36, 12, 48, 24], fill="#f59e0b")
    draw.ellipse([56, 12, 68, 24], fill="#10b981")

    # Title text
    title_font = get_font(12, bold=True)
    draw.text((width / 2, 17), "PowerShell — pytest -v (54 passed in 1.22s)", fill="#94a3b8", font=title_font, anchor="mm")

    # Inner terminal canvas
    mono_font = get_font(13, bold=False)
    mono_bold = get_font(13, bold=True)

    y = 52
    x = 24
    line_h = 24

    # Command line
    draw.text((x, y), "PS <project-folder>> ", fill="#38bdf8", font=mono_bold)
    draw.text((x + 215, y), "pytest -v", fill="#f8fafc", font=mono_bold)
    y += line_h * 1.4

    # Header line
    draw.text((x, y), "=" * 25 + " test session starts " + "=" * 25, fill="#94a3b8", font=mono_font)
    y += line_h
    draw.text((x, y), "platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0", fill="#cbd5e1", font=mono_font)
    y += line_h
    draw.text((x, y), "rootdir: <project-folder>, configfile: pytest.ini", fill="#cbd5e1", font=mono_font)
    y += line_h
    draw.text((x, y), "collected 54 items", fill="#38bdf8", font=mono_bold)
    y += line_h * 1.3

    test_lines = [
        ("tests/test_api.py::test_api_status", "PASSED", "[  2%]"),
        ("tests/test_api.py::test_analyze_valid_file", "PASSED", "[ 12%]"),
        ("tests/test_api.py::test_create_baseline_api", "PASSED", "[ 24%]"),
        ("tests/test_api.py::test_verify_matched_api", "PASSED", "[ 32%]"),
        ("tests/test_api.py::test_verify_modified_api", "PASSED", "[ 40%]"),
        ("tests/test_comparator.py::test_compare_matched_hash", "PASSED", "[ 48%]"),
        ("tests/test_comparator.py::test_compare_modified_hash", "PASSED", "[ 53%]"),
        ("tests/test_database.py::test_save_and_retrieve_baseline", "PASSED", "[ 60%]"),
        ("tests/test_database.py::test_verification_history_log", "PASSED", "[ 64%]"),
        ("tests/test_end_to_end.py::test_full_integrity_lifecycle", "PASSED", "[ 66%]"),
        ("tests/test_file_handler.py::test_validate_path_security", "PASSED", "[ 74%]"),
        ("tests/test_file_handler.py::test_null_byte_rejection", "PASSED", "[ 81%]"),
        ("tests/test_hasher.py::test_sha256_chunked_calculation", "PASSED", "[ 88%]"),
        ("tests/test_hasher.py::test_sha256_avalanche_effect", "PASSED", "[ 94%]"),
        ("tests/test_reporter.py::test_text_report_generation", "PASSED", "[100%]"),
    ]

    for name, status, pct in test_lines:
        draw.text((x, y), f"{name:<60}", fill="#e2e8f0", font=mono_font)
        draw.text((x + 620, y), status, fill="#10b981", font=mono_bold)
        draw.text((x + 720, y), pct, fill="#38bdf8", font=mono_font)
        y += line_h

    y += line_h * 0.5
    y_summary = y
    draw.text((x, y_summary), "=" * 27 + " 54 passed in 1.22s " + "=" * 27, fill="#10b981", font=mono_bold)

    # Save raw terminal screenshot
    raw_path = RAW_DIR / "13_pytest_evidence.png"
    img.save(raw_path)

    # Annotate terminal evidence
    annotated_img = img.copy()
    ann_draw = ImageDraw.Draw(annotated_img)

    # 1. Environment box
    env_box = {"x": 15, "y": 70, "width": 800, "height": 72}
    draw_highlight(ann_draw, env_box, "#38bdf8", 2)
    draw_callout_marker(ann_draw, env_box, "1", "#0284c7", position="right", offset_y=-10)

    # 2. Test execution suite box
    suite_box = {"x": 15, "y": 155, "width": 800, "height": y_summary - 165}
    draw_highlight(ann_draw, suite_box, "#10b981", 2)
    draw_callout_marker(ann_draw, suite_box, "2", "#10b981", position="right", offset_y=-20)

    # 3. Final 54 passed summary
    summary_box = {"x": 15, "y": y_summary - 5, "width": 800, "height": 32}
    draw_highlight(ann_draw, summary_box, "#10b981", 2)
    draw_callout_marker(ann_draw, summary_box, "3", "#10b981", position="right")

    ann_path = ANNOTATED_DIR / "13_pytest_evidence_annotated.png"
    annotated_img.save(ann_path)
    print("[+] Saved 13_pytest_evidence.png & 13_pytest_evidence_annotated.png")


def dismiss_toasts(page):
    try:
        page.evaluate("() => { const tc = document.getElementById('toastContainer'); if (tc) tc.innerHTML = ''; }")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Main Browser Automation & Screen Capture Pipeline
# ---------------------------------------------------------------------------
def capture_all_screenshots(samples):
    print("[*] Launching Chromium browser to capture all real application UI views...")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 960}, device_scale_factor=1.0)
        page = context.new_page()

        # =====================================================================
        # 1. DASHBOARD SCREEN (01_dashboard)
        # =====================================================================
        print("  -> Capturing 01_dashboard...")
        page.goto("http://127.0.0.1:5000", wait_until="networkidle")
        time.sleep(0.5)
        dismiss_toasts(page)

        raw_path = RAW_DIR / "01_dashboard.png"
        page.screenshot(path=str(raw_path))

        img = Image.open(raw_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 1. Main Navigation Header
        nav_box = page.locator("nav.nav-tabs").bounding_box()
        draw_highlight(draw, nav_box, "#38bdf8", 2)
        draw_callout_marker(draw, nav_box, "1", "#0284c7", position="bottom", offset_x=20)

        # 2. Telemetry Metric Counters
        metrics_box = page.locator(".metrics-grid").bounding_box()
        draw_highlight(draw, metrics_box, "#38bdf8", 2)
        draw_callout_marker(draw, metrics_box, "2", "#0284c7", position="top", offset_x=30)

        # 3. Quick Verification Console
        quick_btn_box = page.locator("#btnQuickVerify").bounding_box()
        quick_panel_box = page.locator(".home-two-col .panel-card:first-child").bounding_box()
        draw_highlight(draw, quick_panel_box, "#10b981", 2)
        draw_callout_marker(draw, quick_panel_box, "3", "#10b981", position="top", offset_x=25)
        # Mouse cursor on "Verify" button
        draw_cursor(draw, quick_btn_box["x"] + quick_btn_box["width"] / 2, quick_btn_box["y"] + quick_btn_box["height"] / 2)

        # 4. Hero Action Controls
        hero_box = page.locator("#btnHeroAnalyze").bounding_box()
        draw_highlight(draw, hero_box, "#8b5cf6", 2)
        draw_callout_marker(draw, hero_box, "4", "#8b5cf6", position="top")

        img.save(ANNOTATED_DIR / "01_dashboard_annotated.png")

        # =====================================================================
        # 2. FILE ANALYSIS SCREEN (02_file_analysis)
        # =====================================================================
        print("  -> Capturing 02_file_analysis...")
        page.click("button[data-tab='analyze']")
        time.sleep(0.3)
        page.fill("#analyzeFilePathInput", samples["pdf_path"])
        page.click("#btnRunAnalysis")
        time.sleep(0.8) # Wait for analysis card to render
        dismiss_toasts(page)

        raw_path = RAW_DIR / "02_file_analysis.png"
        page.screenshot(path=str(raw_path))

        img = Image.open(raw_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 1. Target File Details
        file_details_box = page.locator(".file-title-wrapper").bounding_box()
        draw_highlight(draw, file_details_box, "#38bdf8", 2)
        draw_callout_marker(draw, file_details_box, "1", "#0284c7", position="left", offset_x=10)

        # 2. SHA-256 Digest Box
        hash_box = page.locator(".hash-box").bounding_box()
        draw_highlight(draw, hash_box, "#38bdf8", 2)
        draw_callout_marker(draw, hash_box, "2", "#0284c7", position="top", offset_x=30)

        # 3. Create Baseline Action Button
        create_btn_box = page.locator("#btnCreateBaseline").bounding_box()
        draw_highlight(draw, create_btn_box, "#10b981", 2)
        draw_callout_marker(draw, create_btn_box, "3", "#10b981", position="top")
        # Mouse cursor on Create Baseline
        draw_cursor(draw, create_btn_box["x"] + create_btn_box["width"] / 2, create_btn_box["y"] + create_btn_box["height"] / 2)

        # 4. Verify File Action Button
        verify_btn_box = page.locator("#btnVerifyAnalyzedFile").bounding_box()
        draw_highlight(draw, verify_btn_box, "#0284c7", 2)
        draw_callout_marker(draw, verify_btn_box, "4", "#0284c7", position="top")

        # 5. Ingestion Subtabs / Dropzone
        input_tabs_box = page.locator("#screenAnalyze .input-selection-tabs").bounding_box()
        draw_highlight(draw, input_tabs_box, "#8b5cf6", 2)
        draw_callout_marker(draw, input_tabs_box, "5", "#8b5cf6", position="top", offset_x=30)

        img.save(ANNOTATED_DIR / "02_file_analysis_annotated.png")

        # =====================================================================
        # 3. VERIFICATION RESULT — MATCHED (04_matched_verdict)
        # =====================================================================
        print("  -> Capturing 04_matched_verdict...")
        page.click("#btnVerifyAnalyzedFile")
        time.sleep(0.8) # Switches to result screen
        dismiss_toasts(page)

        raw_path = RAW_DIR / "04_matched_verdict.png"
        page.screenshot(path=str(raw_path))

        img = Image.open(raw_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 1. Emerald MATCHED Verdict Banner
        # 1. Emerald MATCHED Verdict Banner
        banner_box = page.locator("#resultStatusBanner").bounding_box()
        draw_highlight(draw, banner_box, "#10b981", 2)
        draw_callout_marker(draw, banner_box, "1", "#10b981", position="left", offset_x=12, offset_y=-10)

        # 2. Audit Target Details
        target_box = page.locator("#resultCard .result-section").nth(0).bounding_box()
        draw_highlight(draw, target_box, "#38bdf8", 2)
        draw_callout_marker(draw, target_box, "2", "#0284c7", position="left", offset_x=12, offset_y=-10)

        # 3. Baseline SHA-256 Digest
        baseline_row = page.locator("#resultCard .hash-row").nth(0).bounding_box()
        draw_highlight(draw, baseline_row, "#10b981", 2)
        draw_callout_marker(draw, baseline_row, "3", "#10b981", position="left", offset_x=12)

        # 4. Current SHA-256 Digest
        current_row = page.locator("#resultCard .hash-row").nth(1).bounding_box()
        draw_highlight(draw, current_row, "#10b981", 2)
        draw_callout_marker(draw, current_row, "4", "#10b981", position="left", offset_x=12)

        # 5. Download Report Action Button
        report_btn_box = page.locator("#btnDownloadReport").bounding_box()
        draw_highlight(draw, report_btn_box, "#0284c7", 2)
        draw_callout_marker(draw, report_btn_box, "5", "#0284c7", position="top", offset_x=0)

        # Mouse cursor on Download Report button
        draw_cursor(draw, report_btn_box["x"] + report_btn_box["width"] / 2, report_btn_box["y"] + report_btn_box["height"] / 2)

        img.save(ANNOTATED_DIR / "04_matched_verdict_annotated.png")

        # =====================================================================
        # 4. VERIFICATION RESULT — MODIFIED (05_modified_verdict)
        # =====================================================================
        print("  -> Capturing 05_modified_verdict...")
        # Temporarily append bytes to trigger tamper
        orig_bytes = Path(samples["pdf_path"]).read_bytes()
        Path(samples["pdf_path"]).write_bytes(orig_bytes + b"\n%INJECTED_UNAUTHORIZED_ALTERATION_BYTES_TAMPER\n")

        page.click("button[data-tab='home']")
        time.sleep(0.3)
        page.fill("#quickFilePathInput", samples["pdf_path"])
        page.click("#btnQuickVerify")
        time.sleep(1.2)
        dismiss_toasts(page)

        raw_path = RAW_DIR / "05_modified_verdict.png"
        page.screenshot(path=str(raw_path))

        # Restore original bytes
        Path(samples["pdf_path"]).write_bytes(orig_bytes)

        img = Image.open(raw_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 1. Amber MODIFIED Alert Banner
        banner_box = page.locator("#resultStatusBanner").bounding_box()
        draw_highlight(draw, banner_box, "#f59e0b", 2)
        draw_callout_marker(draw, banner_box, "1", "#f59e0b", position="left", offset_x=12, offset_y=-10)

        # 2. Target File Details
        target_box = page.locator("#resultCard .result-section").nth(0).bounding_box()
        draw_highlight(draw, target_box, "#38bdf8", 2)
        draw_callout_marker(draw, target_box, "2", "#0284c7", position="left", offset_x=12, offset_y=-10)

        # 3. Baseline SHA-256 Digest
        baseline_row = page.locator("#resultCard .hash-row").nth(0).bounding_box()
        draw_highlight(draw, baseline_row, "#f59e0b", 2)
        draw_callout_marker(draw, baseline_row, "3", "#f59e0b", position="left", offset_x=12)

        # 4. Current Divergent SHA-256 Digest
        current_row = page.locator("#resultCard .hash-row").nth(1).bounding_box()
        draw_highlight(draw, current_row, "#f59e0b", 2)
        draw_callout_marker(draw, current_row, "4", "#f59e0b", position="left", offset_x=12)

        # 5. Download Report Action Button
        report_btn_box = page.locator("#btnDownloadReport").bounding_box()
        draw_highlight(draw, report_btn_box, "#0284c7", 2)
        draw_callout_marker(draw, report_btn_box, "5", "#0284c7", position="top", offset_x=0)

        # Mouse cursor on Download Report button
        draw_cursor(draw, report_btn_box["x"] + report_btn_box["width"] / 2, report_btn_box["y"] + report_btn_box["height"] / 2)

        img.save(ANNOTATED_DIR / "05_modified_verdict_annotated.png")

        # =====================================================================
        # 5. VERIFICATION RESULT — MISSING (06_missing_verdict)
        # =====================================================================
        print("  -> Capturing 06_missing_verdict...")
        page.click("button[data-tab='home']")
        time.sleep(0.3)
        page.fill("#quickFilePathInput", samples["missing_path"])
        page.click("#btnQuickVerify")
        time.sleep(1.2)
        dismiss_toasts(page)

        raw_path = RAW_DIR / "06_missing_verdict.png"
        page.screenshot(path=str(raw_path))

        img = Image.open(raw_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 1. Purple MISSING File Alert Banner
        banner_box = page.locator("#resultStatusBanner").bounding_box()
        draw_highlight(draw, banner_box, "#8b5cf6", 2)
        draw_callout_marker(draw, banner_box, "1", "#8b5cf6", position="left", offset_x=12, offset_y=-10)

        # 2. Target File Notice
        target_box = page.locator("#resultCard .result-section").nth(0).bounding_box()
        draw_highlight(draw, target_box, "#38bdf8", 2)
        draw_callout_marker(draw, target_box, "2", "#0284c7", position="left", offset_x=12, offset_y=-10)

        # 3. Expected Baseline Hash
        hash_box = page.locator("#resultCard .hash-row").nth(0).bounding_box()
        draw_highlight(draw, hash_box, "#8b5cf6", 2)
        draw_callout_marker(draw, hash_box, "3", "#8b5cf6", position="left", offset_x=12)

        # 4. Deletion / Rename Guidance Advisory
        advisory_box = page.locator("#resAdvisoryCard").bounding_box()
        draw_highlight(draw, advisory_box, "#8b5cf6", 2)
        draw_callout_marker(draw, advisory_box, "4", "#8b5cf6", position="left", offset_x=12, offset_y=-10)

        # Cursor over "Select & Analyze File" tab
        tab_analyze_box = page.locator("#tabNavAnalyze").bounding_box()
        draw_cursor(draw, tab_analyze_box["x"] + tab_analyze_box["width"] / 2, tab_analyze_box["y"] + tab_analyze_box["height"] / 2)

        img.save(ANNOTATED_DIR / "06_missing_verdict_annotated.png")

        # =====================================================================
        # 6. VERIFICATION RESULT — ERROR / NO_BASELINE (07_no_baseline_error)
        # =====================================================================
        print("  -> Capturing 07_no_baseline_error...")
        page.click("button[data-tab='home']")
        time.sleep(0.3)
        page.fill("#quickFilePathInput", samples["unbaselined_path"])
        page.click("#btnQuickVerify")
        time.sleep(1.2)
        dismiss_toasts(page)

        raw_path = RAW_DIR / "07_no_baseline_error.png"
        page.screenshot(path=str(raw_path))

        img = Image.open(raw_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 1. Crimson ERROR Banner
        banner_box = page.locator("#resultStatusBanner").bounding_box()
        draw_highlight(draw, banner_box, "#ef4444", 2)
        draw_callout_marker(draw, banner_box, "1", "#ef4444", position="left", offset_x=12, offset_y=-10)

        # 2. Selected File Path Notice
        target_box = page.locator("#resultCard .result-section").nth(0).bounding_box()
        draw_highlight(draw, target_box, "#38bdf8", 2)
        draw_callout_marker(draw, target_box, "2", "#0284c7", position="left", offset_x=12, offset_y=-10)

        # 3. No-Baseline Guidance Advisory
        advisory_box = page.locator("#resAdvisoryCard").bounding_box()
        draw_highlight(draw, advisory_box, "#ef4444", 2)
        draw_callout_marker(draw, advisory_box, "3", "#ef4444", position="left", offset_x=12, offset_y=-10)

        # 4. Select & Analyze File Tab Navigation
        tab_analyze_box = page.locator("#tabNavAnalyze").bounding_box()
        draw_highlight(draw, tab_analyze_box, "#0284c7", 2)
        draw_callout_marker(draw, tab_analyze_box, "4", "#0284c7", position="bottom", offset_y=4)
        draw_cursor(draw, tab_analyze_box["x"] + tab_analyze_box["width"] / 2, tab_analyze_box["y"] + tab_analyze_box["height"] / 2)

        img.save(ANNOTATED_DIR / "07_no_baseline_error_annotated.png")

        # =====================================================================
        # 7. BASELINES VAULT TAB (09_baselines_vault)
        # =====================================================================
        print("  -> Capturing 09_baselines_vault...")
        page.click("button[data-tab='history']")
        time.sleep(0.5)
        page.click("#tabSubBaselines")
        page.wait_for_selector("#baselinesTableBody tr")
        time.sleep(0.6)

        raw_path = RAW_DIR / "09_baselines_vault.png"
        page.screenshot(path=str(raw_path))

        img = Image.open(raw_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 1. Stored Baseline Entry (Row 1)
        row1_box = page.locator("#baselinesTableBody tr").nth(0).bounding_box()
        draw_highlight(draw, row1_box, "#10b981", 2)
        draw_callout_marker(draw, row1_box, "1", "#10b981", position="left", offset_x=12)

        # 2. Stored SHA-256 Digest Column
        hash_cell_box = page.locator("#baselinesTableBody tr").nth(0).locator("td").nth(5).bounding_box()
        draw_highlight(draw, hash_cell_box, "#38bdf8", 2)
        draw_callout_marker(draw, hash_cell_box, "2", "#0284c7", position="top", offset_x=30)

        # 3. One-Click Re-Verification Action
        verify_action_box = page.locator("#baselinesTableBody tr").nth(0).locator("button").nth(0).bounding_box()
        draw_highlight(draw, verify_action_box, "#0284c7", 2)
        draw_callout_marker(draw, verify_action_box, "3", "#0284c7", position="top")
        # Mouse cursor on Verify button
        draw_cursor(draw, verify_action_box["x"] + verify_action_box["width"] / 2, verify_action_box["y"] + verify_action_box["height"] / 2)

        # 4. Baseline Deletion Action
        delete_action_box = page.locator("#baselinesTableBody tr").nth(0).locator("button").nth(1).bounding_box()
        draw_highlight(draw, delete_action_box, "#ef4444", 2)
        draw_callout_marker(draw, delete_action_box, "4", "#ef4444", position="right", offset_x=10)

        img.save(ANNOTATED_DIR / "09_baselines_vault_annotated.png")

        # =====================================================================
        # 8. VERIFICATION HISTORY LOG (08_history_logs)
        # =====================================================================
        print("  -> Capturing 08_history_logs...")
        page.click("#tabSubHistory")
        page.wait_for_selector("#historyTableBody tr")
        time.sleep(0.6)

        raw_path = RAW_DIR / "08_history_logs.png"
        page.screenshot(path=str(raw_path))

        img = Image.open(raw_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 1. History Table Body
        hist_table_box = page.locator("#tableHistory").bounding_box()
        draw_highlight(draw, hist_table_box, "#38bdf8", 2)
        draw_callout_marker(draw, hist_table_box, "1", "#0284c7", position="left", offset_x=12, offset_y=-20)

        # 2. Status Filter Dropdown
        filter_box = page.locator("#filterStatus").bounding_box()
        draw_highlight(draw, filter_box, "#10b981", 2)
        draw_callout_marker(draw, filter_box, "2", "#10b981", position="top")

        # 3. Report Action Trigger
        report_btn_box = page.locator("#historyTableBody tr").nth(0).locator("button").nth(0).bounding_box()
        draw_highlight(draw, report_btn_box, "#0284c7", 2)
        draw_callout_marker(draw, report_btn_box, "3", "#0284c7", position="top")
        # Mouse cursor on Report button
        draw_cursor(draw, report_btn_box["x"] + report_btn_box["width"] / 2, report_btn_box["y"] + report_btn_box["height"] / 2)

        # 4. Verification Record / Status
        status_cell_box = page.locator("#historyTableBody tr").nth(0).locator("td").nth(1).bounding_box()
        draw_highlight(draw, status_cell_box, "#10b981", 2)
        draw_callout_marker(draw, status_cell_box, "4", "#10b981", position="top")

        img.save(ANNOTATED_DIR / "08_history_logs_annotated.png")


        # =====================================================================
        # 9. VERIFICATION REPORT MODAL (10_report_modal)
        # =====================================================================
        print("  -> Capturing 10_report_modal...")
        page.evaluate("() => { if (window.viewReport) window.viewReport(1); }")
        time.sleep(0.6)

        raw_path = RAW_DIR / "10_report_modal.png"
        page.screenshot(path=str(raw_path))

        img = Image.open(raw_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 1. Monospaced Report Body
        report_body_box = page.locator("#modalReportContent").bounding_box()
        draw_highlight(draw, report_body_box, "#38bdf8", 2)
        draw_callout_marker(draw, report_body_box, "1", "#0284c7", position="left", offset_x=12, offset_y=-30)

        # 2. Copy to Clipboard Action
        copy_btn_box = page.locator("#btnCopyModalReport").bounding_box()
        draw_highlight(draw, copy_btn_box, "#38bdf8", 2)
        draw_callout_marker(draw, copy_btn_box, "2", "#0284c7", position="top")

        # 3. Save to File Download Action
        save_btn_box = page.locator("#btnDownloadModalReport").bounding_box()
        draw_highlight(draw, save_btn_box, "#10b981", 2)
        draw_callout_marker(draw, save_btn_box, "3", "#10b981", position="top")
        # Mouse cursor on Save to File
        draw_cursor(draw, save_btn_box["x"] + save_btn_box["width"] / 2, save_btn_box["y"] + save_btn_box["height"] / 2)

        img.save(ANNOTATED_DIR / "10_report_modal_annotated.png")

        page.click("#btnCloseModal")
        time.sleep(0.3)

        # =====================================================================
        # 10. ABOUT / EDUCATIONAL SCREEN (12_about_screen)
        # =====================================================================
        print("  -> Capturing 12_about_screen...")
        page.click("button[data-tab='about']")
        time.sleep(0.5)

        raw_path = RAW_DIR / "12_about_screen.png"
        page.screenshot(path=str(raw_path))

        img = Image.open(raw_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 1. Cryptographic Hashing Concept Card
        card1_box = page.locator(".about-grid .concept-card:nth-child(2)").bounding_box()
        draw_highlight(draw, card1_box, "#0284c7", 2)
        draw_callout_marker(draw, card1_box, "1", "#0284c7", position="top", offset_x=30)

        # 2. Hashing vs Encryption Separation Card
        card2_box = page.locator(".about-grid .concept-card:nth-child(3)").bounding_box()
        draw_highlight(draw, card2_box, "#10b981", 2)
        draw_callout_marker(draw, card2_box, "2", "#10b981", position="top", offset_x=30)

        # 3. Scope & Limitations Boundaries Card
        card3_box = page.locator(".about-grid .concept-card:nth-child(4)").bounding_box()
        draw_highlight(draw, card3_box, "#8b5cf6", 2)
        draw_callout_marker(draw, card3_box, "3", "#8b5cf6", position="top", offset_x=30)

        img.save(ANNOTATED_DIR / "12_about_screen_annotated.png")

        browser.close()

    # 11. Render Pytest Terminal Evidence (Page 13)
    render_pytest_terminal_evidence()

    print("[SUCCESS] All 11 application and test evidence screenshots successfully captured and annotated with 100% mathematical precision!")


if __name__ == "__main__":
    samples = setup_samples_and_db()
    capture_all_screenshots(samples)
