"""Point the Discussion's country-exclusion caution at Supplementary Table S3."""
import zipfile, shutil, re, os

SRC = ("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/"
       "Documents/Private Northeastern/08_Research and Scholarship/Projects/"
       "National AI Strategies/Manuscript/"
       "African_AI_strategies_BMJGH_main_manuscript_v1.2-29sept2026.docx")
DST = SRC.replace("_v1.2-29sept2026.docx", "_v1.3-29sept2026.docx")
assert DST != SRC

OLD = "permutation p = 0.083). These cautions support"
NEW = ("permutation p = 0.083). A leave-one-country-out analysis of the same "
       "separation is reported in Supplementary Table S3. These cautions support")

xml = zipfile.ZipFile(SRC).read('word/document.xml').decode('utf-8')
n = xml.count(OLD)
assert n == 1, f"anchor matched {n}x (want 1)"
xml = xml.replace(OLD, NEW, 1)

plain = re.sub(r'<[^>]+>', '', xml)
assert "is reported in Supplementary Table S3" in plain
assert plain.count("Supplementary Table S3") == 1   # the Discussion cross-reference
assert plain.count("Table S3:") == 1                # the caption in Supplementary Material
print("inserted; 'Supplementary Table S3' occurrences:", plain.count("Supplementary Table S3"))

shutil.copy2(SRC, DST)
with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        d = (xml.encode('utf-8') if item.filename == 'word/document.xml'
             else zin.read(item.filename))
        zout.writestr(item, d)

# tidy my intermediate revisions
base = os.path.dirname(DST); arch = os.path.join(base, "Archive")
os.makedirs(arch, exist_ok=True)
for f in ["African_AI_strategies_BMJGH_main_manuscript_v1.1-29sept2026.docx",
          "African_AI_strategies_BMJGH_main_manuscript_v1.2-29sept2026.docx"]:
    src = os.path.join(base, f)
    if os.path.exists(src):
        shutil.move(src, os.path.join(arch, f))
        print("  archived:", f)
print("wrote", os.path.basename(DST))
