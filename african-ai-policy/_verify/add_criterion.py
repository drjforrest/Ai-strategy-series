"""Add the corpus inclusion criterion to Methods -> Data sources.

Bumps the version to v1.1 (substantive revision), leaves the v1.0 files alone.
"""
import zipfile, shutil, re, os

SRC = ("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/"
       "Documents/Private Northeastern/08_Research and Scholarship/Projects/"
       "National AI Strategies/Manuscript/"
       "African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026-FINAL.docx")
DST = SRC.rsplit("/", 1)[0] + "/African_AI_strategies_BMJGH_main_manuscript_v1.1-29sept2026.docx"

ANCHOR = "The primary corpus comprised 14 national AI strategy or policy entries"
CRITERION = (
    "Corpus inclusion required a dedicated national AI strategy, policy or "
    "roadmap document authored at national level, as distinct from AI "
    "provisions embedded within broader socio-economic development plans; "
    "included documents were further graded by form (final, draft, or official "
    "synthesis report), and this grading is carried into the limitations. "
)

xml = zipfile.ZipFile(SRC).read('word/document.xml').decode('utf-8')
n = xml.count(ANCHOR)
assert n == 1, f"anchor matched {n}x (want 1)"
xml = xml.replace(ANCHOR, CRITERION + ANCHOR, 1)

plain = re.sub(r'<[^>]+>', '', xml)
assert "Corpus inclusion required" in plain
assert plain.count("Corpus inclusion required") == 1
print("sentence inserted; occurrences =", plain.count("Corpus inclusion required"))

shutil.copy2(SRC, DST)
with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = (xml.encode('utf-8') if item.filename == 'word/document.xml'
                else zin.read(item.filename))
        zout.writestr(item, data)

# tidy my own intermediate revisions into Archive/
base = os.path.dirname(DST)
arch = os.path.join(base, "Archive")
os.makedirs(arch, exist_ok=True)
moved = []
for f in ["African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026-TABLE2FIX.docx",
          "African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026-CORRECTED.docx",
          "African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026-LG.docx",
          "African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026-FINAL.docx"]:
    src = os.path.join(base, f)
    if os.path.exists(src):
        shutil.move(src, os.path.join(arch, f))
        moved.append(f)
print("wrote", os.path.basename(DST))
for m in moved:
    print("  archived:", m)
