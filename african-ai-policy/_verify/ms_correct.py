"""Apply the remaining structural corrections to the 25-Sep manuscript.

Each edit asserts it matched, and every substitution is scoped (table edits are
confined to their own table block). Writes a new file; input is left untouched.

Corrected:
  1. Table S1   - rebuilt for 14 countries (was 12, stale)
  2. Table S2   - r values + top-3 ordering
  3. p78 prose  - convergence ranking
  4. p79 prose  - aggregation-sensitivity numbers
  5. Table S2 note - Spearman + bootstrap CI
  6. p73 prose  - report the Morocco-exclusion p (was cited but not reported)
  7. Figure 2 caption - strip a stray ``` artefact
"""
import zipfile, shutil, re, sys, os

SRC = ("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/"
       "Documents/Private Northeastern/08_Research and Scholarship/Projects/"
       "National AI Strategies/Manuscript/"
       "African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026-TABLE2FIX.docx")
DST = SRC.replace("-TABLE2FIX.docx", "-CORRECTED.docx")

# values from analyze_convergence_tables.py (14-country corpus)
S1_ROWS = [  # rank, country, r  (3 dp)
    (1,  "Rwanda",            "+0.638"),
    (2,  "South Africa",      "+0.489"),
    (3,  "Côte d’Ivoire",     "+0.459"),
    (4,  "Nigeria",           "+0.328"),
    (5,  "Mauritius",         "+0.254"),
    (6,  "Egypt",             "+0.200"),
    (7,  "Senegal",           "+0.050"),
    (8,  "Tanzania",          "-0.032"),
    (9,  "Kenya",             "-0.109"),
    (10, "Zimbabwe",          "-0.128"),
    (11, "Morocco",           "-0.153"),
    (12, "Ghana",             "-0.210"),
    (13, "Benin",             "-0.501"),
    (14, "Ethiopia",          "-0.607"),
]

xml = zipfile.ZipFile(SRC).read('word/document.xml').decode('utf-8')
report = []
def note(ok, what):
    report.append(("OK " if ok else "!! ") + what)

# ---------------------------------------------------------------- 1. Table S1
i = xml.rfind('Table S1')
j = xml.find('<w:tbl>', i); k = xml.find('</w:tbl>', j)
tbl = xml[j:k + 8]
rows = re.findall(r'<w:tr\b.*?</w:tr>', tbl, re.S)
assert len(rows) == 13, f"expected 13 S1 rows, got {len(rows)}"
prefix = tbl[:tbl.find('<w:tr')]
template = rows[1]

new_rows = [rows[0]]
for rank, country, r in S1_ROWS:
    row = template
    row = row.replace('<w:t>1</w:t>', f'<w:t>{rank}</w:t>', 1)
    row = row.replace('<w:t>Rwanda</w:t>', f'<w:t>{country}</w:t>', 1)
    row = row.replace('<w:t>+0.57</w:t>', f'<w:t>{r}</w:t>', 1)
    assert f'<w:t>{rank}</w:t>' in row and f'<w:t>{country}</w:t>' in row \
           and f'<w:t>{r}</w:t>' in row, f"row build failed for {country}"
    new_rows.append(row)
new_tbl = prefix + ''.join(new_rows) + '</w:tbl>'
xml = xml[:j] + new_tbl + xml[k + 8:]
note(True, f"Table S1 rebuilt: 13 -> {len(new_rows)} rows")

# ---------------------------------------------------------------- 2. Table S2
i = xml.rfind('Table S2')
j = xml.find('<w:tbl>', i); k = xml.find('</w:tbl>', j)
s2 = xml[j:k + 8]
orig = s2
for old, new in [('+0.580', '+0.632'), ('+0.574', '+0.638'), ('+0.539', '+0.621')]:
    assert s2.count(f'<w:t>{old}</w:t>') == 1, f"S2 {old} not unique"
    s2 = s2.replace(f'<w:t>{old}</w:t>', f'<w:t>{new}</w:t>')
old_top3 = 'Rwanda; Côte d’Ivoire; South Africa'
assert s2.count(f'<w:t>{old_top3}</w:t>') == 2, "S2 top3 count != 2"
s2 = s2.replace(f'<w:t>{old_top3}</w:t>',
                '<w:t>Rwanda; South Africa; Côte d’Ivoire</w:t>')
xml = xml[:j] + s2 + xml[k + 8:]
note(s2 != orig, "Table S2 values + top-3 ordering updated")

# ---------------------------------------------------------------- 3-7. prose
EDITS = [
 # 3. convergence ranking prose
 ("(profile r = +0.57), followed by Côte d’Ivoire (+0.43) and South Africa "
  "(+0.38), then Mauritius (+0.21) and Nigeria (+0.20), with Egypt near neutral "
  "(+0.05) (Table S1). The most divergent were Benin (-0.60), Zimbabwe (-0.28), "
  "Kenya (-0.28), Morocco (-0.22), Ghana (-0.22) and Senegal (-0.16).",
  "(profile r = +0.64), followed by South Africa (+0.49) and Côte d’Ivoire "
  "(+0.46), then Nigeria (+0.33) and Mauritius (+0.25), with Egypt near neutral "
  "(+0.20) and Tanzania just below it (-0.03) (Table S1). The most divergent "
  "were Ethiopia (-0.61), Benin (-0.50), Ghana (-0.21), Morocco (-0.15), "
  "Zimbabwe (-0.13) and Kenya (-0.11)."),
 # 4. aggregation sensitivity prose
 ("At the 5% threshold, South Africa ranked first (r = +0.580), followed by "
  "Nigeria and Egypt; at the 10% threshold, Rwanda ranked first (r = +0.574), "
  "followed by Côte d’Ivoire and South Africa; and at the 20% threshold, Rwanda "
  "again ranked first (r = +0.539), followed by Côte d’Ivoire and South Africa. "
  "The Spearman correlation between the 5% and 20% rankings was only 0.35. "
  "Bootstrapping the nine-domain profile for Rwanda yielded a wide confidence "
  "interval around the convergence estimate (95% CI 0.321 to 0.961)",
  "At the 5% threshold, South Africa ranked first (r = +0.632), followed by "
  "Nigeria and Egypt; at the 10% threshold, Rwanda ranked first (r = +0.638), "
  "followed by South Africa and Côte d’Ivoire; and at the 20% threshold, Rwanda "
  "again ranked first (r = +0.621), followed by South Africa and Côte d’Ivoire. "
  "The Spearman correlation between the 5% and 20% rankings was 0.61. "
  "Bootstrapping the nine-domain profile for Rwanda yielded a wide confidence "
  "interval around the convergence estimate (95% CI 0.248 to 0.975)"),
 # 5. Table S2 note
 ("The prespecified 10% threshold is the primary analysis. Spearman rank "
  "correlation between the 5% and 20% rankings was 0.35. Rwanda’s 10% "
  "convergence estimate was r = +0.574 with bootstrap 95% CI 0.321 to 0.961,",
  "The prespecified 10% threshold is the primary analysis. Spearman rank "
  "correlation between the 5% and 20% rankings was 0.61. Rwanda’s 10% "
  "convergence estimate was r = +0.638 with bootstrap 95% CI 0.248 to 0.975,"),
 # 6. report the Morocco-exclusion result
 ("and should be read alongside the Morocco-exclusion sensitivity.",
  "and should be read alongside the Morocco-exclusion sensitivity, which "
  "attenuates the separation (text-proximate mean r = +0.165 versus independent "
  "mean r = \u22120.054; permutation p = 0.083)."),
 # 7. stray markdown fence in the Figure 2 caption
 ("<w:t>```</w:t>", ""),
]
for old, new in EDITS:
    n = xml.count(old)
    assert n == 1, f"edit matched {n} times (want 1): {old[:60]!r}"
    xml = xml.replace(old, new, 1)
    note(True, f"prose edit applied: {old[:52]!r}...")

# ---------------------------------------------------------------- write
shutil.copy2(SRC, DST)
with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = (xml.encode('utf-8') if item.filename == 'word/document.xml'
                else zin.read(item.filename))
        zout.writestr(item, data)

print("\n".join(report))
print(f"\nWrote {os.path.basename(DST)}")
