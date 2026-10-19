import zipfile, re
P=("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/Documents/"
   "Private Northeastern/08_Research and Scholarship/Projects/National AI Strategies/"
   "Manuscript/African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026-TABLE2FIX.docx")
xml = zipfile.ZipFile(P).read('word/document.xml').decode()

def para_for(anchor):
    i = xml.find(anchor)
    if i < 0: return None, "ANCHOR NOT FOUND"
    s = xml.rfind('<w:p ', 0, i)
    e = xml.find('</w:p>', i) + 6
    return xml[s:e], None

for anchor in ["Ranking national strategies by how closely",
               "Aggregation sensitivity clarified",
               "The prespecified 10% threshold is the primary analysis",
               "Three cautions qualify this result",
               "pooled r = -0.041 across 108"]:
    p, err = para_for(anchor)
    print("="*70)
    print("ANCHOR:", anchor[:50], "->", err or "found")
    if p:
        runs = re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', p)
        print("  runs:", runs)
