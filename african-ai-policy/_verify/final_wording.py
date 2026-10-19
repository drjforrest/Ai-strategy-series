"""Final pass: replace the four 'prespecified' uses, add the repository URL.

Guards: each needle must match exactly once. Post-checks assert no
'prespecified' remains and the URL is present.
"""
import zipfile, shutil, re, os

SRC = ("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/"
       "Documents/Private Northeastern/08_Research and Scholarship/Projects/"
       "National AI Strategies/Manuscript/"
       "African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026-LG.docx")
DST = SRC.replace("-LG.docx", "-FINAL.docx")

REPO = "https://github.com/drjforrest/african-ai-strategies"

EDITS = [
 # 1. Methods — the Ethiopia convention is a corpus/code convention, not a
 #    prospective scientific decision.
 ("in accordance with the prespecified convention for multi-part strategies",
  "in accordance with the corpus convention for multi-part strategies"),

 # 2. Results — 'primary' names the role the threshold plays.
 ("under the prespecified 10% aggregation rule, Rwanda was most convergent",
  "under the primary 10% aggregation rule, Rwanda was most convergent"),

 # 3. Discussion — same substitution.
 ("mirrored the continental vision under the prespecified 10% aggregation rule, "
  "and its position",
  "mirrored the continental vision under the primary 10% aggregation rule, "
  "and its position"),

 # 4. Table S2 note — the old sentence was tautological; name the inference
 #    structure instead (primary specification vs sensitivity analyses).
 ("The prespecified 10% threshold is the primary analysis. Spearman rank "
  "correlation between the 5% and 20% rankings was 0.61.",
  "The 10% threshold is the primary specification; the 5% and 20% thresholds "
  "are reported as sensitivity analyses. Spearman rank correlation between the "
  "5% and 20% rankings was 0.61."),

 # 5. Data availability — give the resolvable repository URL.
 ("available in the project repository.",
  f"available at {REPO}."),
]

xml = zipfile.ZipFile(SRC).read('word/document.xml').decode('utf-8')
for old, new in EDITS:
    n = xml.count(old)
    assert n == 1, f"matched {n}x (want 1): {old[:72]!r}"
    xml = xml.replace(old, new, 1)

# ---- post-checks ----
plain = re.sub(r'<[^>]+>', '', xml)
left = re.findall(r'pre[-\s]?specified', plain, re.I)
assert not left, f"'prespecified' still present: {left}"
assert plain.count(REPO) == 1, f"URL count = {plain.count(REPO)}"
print("post-check: 'prespecified' remaining =", len(left))
print("post-check: repo URL occurrences  =", plain.count(REPO))

shutil.copy2(SRC, DST)
with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = (xml.encode('utf-8') if item.filename == 'word/document.xml'
                else zin.read(item.filename))
        zout.writestr(item, data)
print("wrote", os.path.basename(DST))
