import zipfile, re
P=("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/Documents/"
   "Private Northeastern/08_Research and Scholarship/Projects/National AI Strategies/"
   "Manuscript/African_AI_strategies_BMJGH_main_manuscript_v1.1-29sept2026.docx")
x=zipfile.ZipFile(P).read('word/document.xml').decode()

# --- Table S2 region ---
i=x.rfind('Table S2')
s=x.rfind('<w:p ',0,i); e=x.find('</w:p>',i)+6
print("### CAPTION PARA ###"); print(x[s:e][:900])

j=x.find('<w:tbl>',i); k=x.find('</w:tbl>',j)
tbl=x[j:k+8]
print("\n### TABLE: tblPr + grid ###")
print(tbl[:tbl.find('<w:tr')][:1400])
rows=re.findall(r'<w:tr\b.*?</w:tr>', tbl, re.S)
print(f"\n### rows: {len(rows)} ###")
print("### HEADER ROW ###"); print(rows[0][:1600])
print("\n### DATA ROW (template) ###"); print(rows[1][:1600])

# --- note paragraph after the table ---
n=x.rfind('The 10% threshold is the primary specification')
ns=x.rfind('<w:p ',0,n); ne=x.find('</w:p>',n)+6
print("\n### NOTE PARA ###"); print(x[ns:ne][:1100])
