"""
Re-annotate ONLY 03_analysis_dropzone_annotated.png and 11_stitch_studio_annotated.png
from their original raw captures with mathematical pixel-perfection.
DO NOT touch any of the other 11 screenshots.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "docs" / "screenshots" / "raw"
ANNOTATED_DIR = ROOT_DIR / "docs" / "screenshots" / "annotated"


def get_font(size=14, bold=True):
    for fp in [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
    ]:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_cursor(draw, x, y):
    """Draw a clean, crisp, highly visible OS mouse pointer with hot-spot at (x, y)."""
    shadow = [
        (x + 2, y + 2), (x + 2, y + 23), (x + 8, y + 19), (x + 12, y + 27),
        (x + 16, y + 25), (x + 12, y + 17), (x + 18, y + 17)
    ]
    draw.polygon(shadow, fill="#050811")
    outline = [
        (x, y), (x, y + 21), (x + 6, y + 17), (x + 10, y + 25),
        (x + 14, y + 23), (x + 10, y + 15), (x + 16, y + 15)
    ]
    draw.polygon(outline, fill="#000000", outline="#000000")
    body = [
        (x + 1, y + 2), (x + 1, y + 18), (x + 6, y + 15), (x + 9, y + 22),
        (x + 12, y + 20), (x + 9, y + 14), (x + 14, y + 14)
    ]
    draw.polygon(body, fill="#ffffff")


def draw_highlight(draw, box, color="#38bdf8", width=2, radius=4):
    """Draw a clean, subtle outline framing the target element without obscuring content."""
    x1, y1 = box["x"], box["y"]
    x2, y2 = box["x"] + box["width"], box["y"] + box["height"]
    draw.rounded_rectangle([x1 - 2, y1 - 2, x2 + 2, y2 + 2], radius=radius, outline=color, width=width)


def draw_badge(draw, cx, cy, num_str, color="#0284c7", radius=14):
    """Draw a numbered circular badge."""
    font = get_font(13, bold=True)
    draw.ellipse([cx - radius - 1, cy - radius - 1, cx + radius + 1, cy + radius + 1], fill="#050811")
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color, outline="#ffffff", width=2)
    draw.text((cx, cy - 1), str(num_str), fill="#ffffff", font=font, anchor="mm")


def draw_arrow(draw, start, end, color="#0284c7"):
    """Draw a leader line with a directional arrow head."""
    draw.line([start, end], fill=color, width=2)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    if abs(dx) > abs(dy):
        sign = 1 if dx > 0 else -1
        head = [end, (end[0] - sign * 7, end[1] - 5), (end[0] - sign * 7, end[1] + 5)]
    else:
        sign = 1 if dy > 0 else -1
        head = [end, (end[0] - 5, end[1] - sign * 7), (end[0] + 5, end[1] - sign * 7)]
    draw.polygon(head, fill=color)


def annotate_03_analysis_dropzone():
    raw_path = RAW_DIR / "03_analysis_dropzone.png"
    out_path = ANNOTATED_DIR / "03_analysis_dropzone_annotated.png"
    print(f"[*] Annotating {raw_path.name} -> {out_path.name}...")

    img = Image.open(raw_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 1. Active Ingestion Mode Tab [File Picker / Drag & Drop]
    tab_box = {"x": 355, "y": 320, "width": 280, "height": 46}
    draw_highlight(draw, tab_box, "#0284c7", 2)
    draw_arrow(draw, (495, 300), (495, 318), "#0284c7")
    draw_badge(draw, 495, 286, "1", "#0284c7")

    # 2. Drag & Drop Capture Zone (Dashed Container)
    drop_box = {"x": 140, "y": 374, "width": 1640, "height": 352}
    draw_highlight(draw, drop_box, "#38bdf8", 2)
    draw_arrow(draw, (89, 460), (138, 460), "#38bdf8")
    draw_badge(draw, 75, 460, "2", "#38bdf8")

    # 3. Analyzed Target File Identification Pill
    pill_box = {"x": 145, "y": 804, "width": 422, "height": 82}
    draw_highlight(draw, pill_box, "#10b981", 2)
    draw_arrow(draw, (89, 845), (143, 845), "#10b981")
    draw_badge(draw, 75, 845, "3", "#10b981")

    # 4. [Create / Update Baseline] Action Button
    create_box = {"x": 899, "y": 818, "width": 340, "height": 51}
    draw_highlight(draw, create_box, "#0284c7", 2)
    draw_arrow(draw, (1069, 802), (1069, 816), "#0284c7")
    draw_badge(draw, 1069, 788, "4", "#0284c7")

    # 5. [Verify File Integrity] Action Button
    verify_box = {"x": 1251, "y": 818, "width": 278, "height": 51}
    draw_highlight(draw, verify_box, "#38bdf8", 2)
    draw_arrow(draw, (1390, 802), (1390, 816), "#38bdf8")
    draw_badge(draw, 1390, 788, "5", "#0284c7")

    # Mouse cursor inside the dropzone
    draw_cursor(draw, 960, 520)

    img.save(out_path)
    print(f"[+] Successfully saved {out_path.name}")


def annotate_11_stitch_studio():
    raw_path = RAW_DIR / "11_stitch_studio.png"
    out_path = ANNOTATED_DIR / "11_stitch_studio_annotated.png"
    print(f"[*] Annotating {raw_path.name} -> {out_path.name}...")

    img = Image.open(raw_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 1. Google Stitch Status Banner
    banner_box = {"x": 488, "y": 266, "width": 944, "height": 128}
    draw_highlight(draw, banner_box, "#0284c7", 2)
    draw_arrow(draw, (429, 330), (486, 330), "#0284c7")
    draw_badge(draw, 415, 330, "1", "#0284c7")

    # 2. Quick Preset Palettes (buttons row)
    preset_box = {"x": 488, "y": 462, "width": 944, "height": 48}
    draw_highlight(draw, preset_box, "#10b981", 2)
    draw_arrow(draw, (429, 486), (486, 486), "#10b981")
    draw_badge(draw, 415, 486, "2", "#10b981")

    # 3. Active Design Tokens (JSON) Textarea
    json_box = {"x": 488, "y": 586, "width": 944, "height": 260}
    draw_highlight(draw, json_box, "#38bdf8", 2)
    draw_arrow(draw, (429, 716), (486, 716), "#38bdf8")
    draw_badge(draw, 415, 716, "3", "#0284c7")

    # 4. [Apply Custom Tokens] Action Button
    apply_box = {"x": 764, "y": 924, "width": 268, "height": 38}
    draw_highlight(draw, apply_box, "#0284c7", 2)
    draw_arrow(draw, (898, 908), (898, 922), "#0284c7")
    draw_badge(draw, 898, 894, "4", "#0284c7")

    # 5. [Done] Modal Dismiss Action Button
    done_box = {"x": 1327, "y": 1060, "width": 105, "height": 52}
    draw_highlight(draw, done_box, "#10b981", 2)
    draw_arrow(draw, (1299, 1086), (1325, 1086), "#10b981")
    draw_badge(draw, 1285, 1086, "5", "#10b981")

    # Mouse cursor on Apply Custom Tokens button
    draw_cursor(draw, 898, 943)

    img.save(out_path)
    print(f"[+] Successfully saved {out_path.name}")


if __name__ == "__main__":
    annotate_03_analysis_dropzone()
    annotate_11_stitch_studio()
    print("[SUCCESS] Exclusively re-annotated the 2 target screenshot files.")
