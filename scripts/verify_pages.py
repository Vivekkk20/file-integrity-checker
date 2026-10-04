import pypdf

reader = pypdf.PdfReader("docs/file_integrity_checker_documentation.pdf")
print(f"Total pages: {len(reader.pages)}")

for i, page in enumerate(reader.pages):
    lines = [l.strip() for l in page.extract_text().splitlines() if l.strip()]
    first_line = lines[0] if lines else "EMPTY"
    last_line = lines[-1] if lines else "EMPTY"
    first_ascii = first_line.encode("ascii", "replace").decode()[:55]
    last_ascii = last_line.encode("ascii", "replace").decode()[:40]
    print(f"Page {i+1:02d}: [TOP] {first_ascii:<55} | [BOTTOM] {last_ascii}")
