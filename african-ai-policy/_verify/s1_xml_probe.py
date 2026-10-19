import zipfile, re
P=("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/Documents/"
   "Private Northeastern/08_Research and Scholarship/Projects/National AI Strategies/"
   "Manuscript/African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026-TABLE2FIX.docx")
xml = zipfile.ZipFile(P).read('word/document.xml').decode()

# find the Table S1 caption, then the following <w:tbl>
i = xml.find('Table S1')
j = xml.find('<w:tbl>', i)
k = xml.find('</w:tbl>', j)
tbl = xml[j:k+8]
print("Table S1 XML length:", len(tbl))
rows = re.findall(r'<w:tr\b.*?</w:tr>', tbl, re.S)
print("rows found:", len(rows))
print("\n--- first (header) row ---")
print(rows[0][:1200])
print("\n--- second (data) row ---")
print(rows[1][:1400])
