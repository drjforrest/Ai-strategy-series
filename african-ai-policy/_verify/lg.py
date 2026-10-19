"""Replace 'crosswalk' with 'application', fix a mislabel, add the scope sentence.

Guards: every needle must match exactly once; a post-check asserts the term
'crosswalk' no longer appears anywhere in the document.
"""
import zipfile, shutil, re, os

SRC = ("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/"
       "Documents/Private Northeastern/08_Research and Scholarship/Projects/"
       "National AI Strategies/Manuscript/"
       "African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026-CORRECTED.docx")
DST = SRC.replace("-CORRECTED.docx", "-LG.docx")

EDITS = [
 # (1) Summary box — verb form "cross-walked"; "compared with" is the precise wording.
 ("No study has quantitatively cross-walked the full text of African AI strategies "
  "against a standardised digital-health competency framework,",
  "No study has quantitatively compared the full text of African AI strategies "
  "with a standardised digital-health competency framework,"),

 # (2) Abstract Methods — state it is an application to an external reference.
 ("and retained the Oxford Government AI Readiness Index crosswalk and "
  "continental-convergence analyses.",
  "and applied the same instrument to the nine Oxford Government AI Readiness "
  "Index dimensions as an external reference, alongside continental-convergence "
  "analyses."),

 # (3) Aggregation — name the artefact, and drop the 'readiness' mislabel (this
 #     matrix holds text-derived emphasis, not readiness).
 ("the identical analysis produced both the WHO competency matrix and the Oxford "
  "readiness crosswalk.",
  "the identical analysis produced both the WHO competency matrix and the Oxford "
  "dimension-emphasis matrix."),

 # (4) NEW: state that the two Oxford-dependent and convergence analyses use
 #     different country sets, so the reader is not left to infer it.
 ("Analyses were repeated excluding Morocco.",
  "Analyses were repeated excluding Morocco. The Oxford comparison and the "
  "convergence analysis operate on different country sets: the Oxford comparison "
  "is bounded by the coverage of the readiness index and includes 12 countries, "
  "whereas convergence uses all 14 national entries."),
]

xml = zipfile.ZipFile(SRC).read('word/document.xml').decode('utf-8')
for old, new in EDITS:
    n = xml.count(old)
    assert n == 1, f"matched {n}x (want 1): {old[:70]!r}"
    xml = xml.replace(old, new, 1)

# post-check: the disliked term must be gone entirely
plain = re.sub(r'<[^>]+>', '', xml)
leftover = re.findall(r'cross[- ]?walk\w*', plain, re.I)
assert not leftover, f"term still present: {leftover}"
print(f"crosswalk occurrences after edit: {len(leftover)}")

shutil.copy2(SRC, DST)
with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = (xml.encode('utf-8') if item.filename == 'word/document.xml'
                else zin.read(item.filename))
        zout.writestr(item, data)
print("wrote", os.path.basename(DST))
