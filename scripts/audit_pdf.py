import pypdf
import re

reader = pypdf.PdfReader("docs/file_integrity_checker_documentation.pdf")
full_text = ""
for i, page in enumerate(reader.pages):
    full_text += f"\n--- PAGE {i+1} ---\n" + page.extract_text()

portfolio_matches = re.findall(r"portfolio", full_text, re.IGNORECASE)
print(f"Matches for 'Portfolio': {len(portfolio_matches)}")
if portfolio_matches:
    print("  Found:", portfolio_matches)

tech_domain_matches = re.findall(r"technical\s*domain", full_text, re.IGNORECASE)
print(f"Matches for 'Technical Domain': {len(tech_domain_matches)}")

author_matches = re.findall(r"(?:Vivek\s*Rathod[^\n]*)", full_text, re.IGNORECASE)
print(f"Author occurrences: {author_matches}")

designation_matches = re.findall(r"(?:Security Engineer|Full-Stack Developer|SOC Analyst|Security Analyst Vivek)", full_text, re.IGNORECASE)
print(f"Designation matches: {designation_matches}")

path_matches = re.findall(r"[A-Za-z]:[\\/](?:projects|Users|home)[^\s]*", full_text)
print(f"Matches for absolute machine paths: {len(path_matches)}")
if path_matches:
    print("  Found paths:", path_matches)

broken_activate = re.findall(r"Scriptsctivate", full_text)
print(f"Matches for broken Scriptsctivate: {len(broken_activate)}")

correct_activate = re.findall(r"\.venv\\Scripts\\activate", full_text)
print(f"Matches for correct .venv\\Scripts\\activate: {len(correct_activate)}")

edition_matches = re.findall(r"Software Edition:[^\n]*", full_text)
print(f"Software Edition line: {edition_matches}")

exaggerated_terms = [
    "mathematically sound defensive utility",
    "absolute cryptographic certainty",
    "production-grade",
    "enterprise-scale",
    "forensic-grade",
    "100% verified",
    "guaranteed security"
]
for term in exaggerated_terms:
    m = re.findall(re.escape(term), full_text, re.IGNORECASE)
    print(f"Exaggerated term '{term}': {len(m)} matches")
