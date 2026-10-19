import zipfile, re
P = ("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/"
     "Documents/Private Northeastern/08_Research and Scholarship/Projects/"
     "National AI Strategies/Manuscript/"
     "African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026.docx")
xml = zipfile.ZipFile(P).read('word/document.xml').decode('utf-8')
print("document.xml chars:", len(xml))

for val in ["+0.236", "0.236", "+0.494", "-0.494", "+0.180"]:
    i = xml.find(val)
    print(f"\n=== '{val}' at char {i} ===")
    if i > 0:
        print(repr(xml[max(0,i-260):i+90]))
