from pptx import Presentation
OUT = "_deck_out/"
for f in ["Paper-Series-Briefing-for-Co-Authors.pptx", "Year-1-Roadmap-for-Research-and-Scholarship.pptx"]:
    prs = Presentation(OUT + f)
    print("="*90); print(f, "| slides:", len(prs.slides)); print("="*90)
    for i, slide in enumerate(prs.slides):
        for sh in slide.shapes:
            if getattr(sh, "has_table", False):
                for r in sh.table.rows:
                    cells=[c.text for c in r.cells]
                    if cells and cells[0] in ("Paper 2a","Paper 2b","Paper 3"):
                        print(f"  slide{i+1} TABLE: {cells}")
            elif sh.has_text_frame:
                t = sh.text_frame.text.strip()
                if t and ("2b" in t or "competenc" in t.lower() and len(t)>60 or "Canadian" in t and len(t)>50):
                    print(f"  slide{i+1} [{sh.name}]: {t[:280]}")
