"""Repair Table 2 in the 25-Sep manuscript so it matches the repository.

Each of the nine coefficients is replaced with the value from
outputs/rhetoric_vs_readiness/per_dimension_correlation.csv (the shipped,
regenerable artefact). Each search string must occur exactly once; the script
aborts without writing if any count differs.

Writes to a NEW filename so the original revision is preserved.
"""
import zipfile, shutil, sys, os

SRC = ("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/"
       "Documents/Private Northeastern/08_Research and Scholarship/Projects/"
       "National AI Strategies/Manuscript/"
       "African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026.docx")
DST = SRC.replace(".docx", "-TABLE2FIX.docx")

# manuscript value -> repository value
FIX = {
    "+0.236": "+0.228",   # Vision
    "+0.180": "+0.189",   # Governance and Ethics
    "+0.105": "+0.071",   # Maturity
    "+0.033": "-0.044",   # Adaptability
    "-0.086": "-0.222",   # Innovation Capacity
    "-0.088": "-0.065",   # Data Availability
    "-0.118": "-0.188",   # Digital Capacity
    "-0.141": "-0.169",   # Human Capital
    "-0.494": "-0.172",   # Infrastructure
}

zin = zipfile.ZipFile(SRC)
xml = zin.read('word/document.xml').decode('utf-8')

# --- guard: every needle must be unique ---
bad = []
for old in FIX:
    n = xml.count(f"<w:t>{old}</w:t>")
    print(f"  <w:t>{old}</w:t>  occurrences: {n}")
    if n != 1:
        bad.append((old, n))
if bad:
    print(f"\nABORT -- not unique: {bad}")
    sys.exit(1)

new_xml = xml
for old, new in FIX.items():
    new_xml = new_xml.replace(f"<w:t>{old}</w:t>", f"<w:t>{new}</w:t>")

# --- write a new archive, copying every other member untouched ---
shutil.copy2(SRC, DST)
with zipfile.ZipFile(SRC) as zin2, zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin2.infolist():
        data = (new_xml.encode('utf-8') if item.filename == 'word/document.xml'
                else zin2.read(item.filename))
        zout.writestr(item, data)

print(f"\nWrote {os.path.basename(DST)}")
print("original preserved:", os.path.basename(SRC))
