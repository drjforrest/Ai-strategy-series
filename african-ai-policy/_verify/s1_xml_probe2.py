import zipfile, re
P=("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/Documents/"
   "Private Northeastern/08_Research and Scholarship/Projects/National AI Strategies/"
   "Manuscript/African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026-TABLE2FIX.docx")
xml = zipfile.ZipFile(P).read('word/document.xml').decode()

i = xml.rfind('Table S1')                 # the CAPTION, not the prose cross-ref
j = xml.find('<w:tbl>', i)
k = xml.find('</w:tbl>', j)
tbl = xml[j:k+8]
rows = re.findall(r'<w:tr\b.*?</w:tr>', tbl, re.S)
print("Table S1 rows:", len(rows))
for n, r in enumerate(rows):
    cells = re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', r)
    print(f"  row{n:2d}: {cells}")

# column widths from the header row, so a rebuilt row matches the grid
hdr_w = re.findall(r'<w:tcW w:w="(\d+)" w:type="pct"/>', rows[0])
print("\ncolumn widths (pct):", hdr_w)

# also grab the Table S2 structure (caption -> table)
i2 = xml.rfind('Table S2')
j2 = xml.find('<w:tbl>', i2); k2 = xml.find('</w:tbl>', j2)
rows2 = re.findall(r'<w:tr\b.*?</w:tr>', xml[j2:k2+8], re.S)
print("\nTable S2 rows:", len(rows2))
for n, r in enumerate(rows2):
    print(f"  row{n}: {re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', r)}")
