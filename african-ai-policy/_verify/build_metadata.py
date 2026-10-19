"""Assemble a corpus metadata CSV from files on disk (only verifiable fields)."""
import pathlib, re, csv, pandas as pd

D = pathlib.Path("data")
NS, DH = D / "national_strategies", D / "digital_health_strategies"

def words(p): return len(p.read_text(encoding="utf-8", errors="ignore").split())

def years(text):
    ys = sorted(set(re.findall(r"\b(20[12]\d)\b", text)))
    return ", ".join(ys[:6])

PRIMARY = [  # country, title, domain, issuing_body, status, period, lang
 ("Benin","Stratégie Nationale d'Intelligence Artificielle et Big Data (SNIAM)","AI strategy","Ministry of Digital Affairs and Digitalization","adopted","","French"),
 ("Côte d'Ivoire","Stratégie de Développement de l'IA à l'horizon 2030","AI strategy","Ministère de la Transition Numérique et de la Digitalisation","adopted","to 2030","French"),
 ("Egypt","Egypt National Artificial Intelligence Strategy (2nd ed.)","AI strategy","Ministry of Communications and Information Technology","adopted","2025-2030","English"),
 ("Ethiopia","Digital Ethiopia 2025 + Digital Ethiopia 2030 Vision","Digital transformation","Federal Democratic Republic of Ethiopia","adopted","to 2025 / to 2030","English"),
 ("Ghana","Republic of Ghana National Artificial Intelligence Strategy","AI strategy","Ministry of Communications and Digitalisation","adopted","2023-2033","English"),
 ("Kenya","Kenya Artificial Intelligence Strategy","AI strategy","Ministry of ICT and Digital Economy","adopted","2025-2030","English"),
 ("Mauritius","The Mauritius Artificial Intelligence Strategy","AI strategy (working-group report)","Working Group on AI","report","","English"),
 ("Morocco","AI in Morocco: conference-synthesis report","AI roadmap (report)","—","report","","English"),
 ("Nigeria","National Artificial Intelligence Strategy","AI strategy","Federal Ministry of Communication, Innovation and Digital Economy","adopted","2025-","English"),
 ("Rwanda","The National AI Policy","AI policy","Ministry of ICT and Innovation","adopted","","English"),
 ("Senegal","Stratégie de Développement de l'Intelligence Artificielle","AI strategy","—","adopted","","French"),
 ("South Africa","Draft South Africa National Artificial Intelligence Strategy","AI strategy (draft)","Department of Communications and Digital Technologies","draft","2026","English"),
 ("Tanzania","The Tanzania National Artificial Intelligence Strategy Framework (Draft v0.6)","AI strategy (draft)","Ministry of Communication and Information Technology","draft","2025-","English"),
 ("Zimbabwe","Zimbabwe National Artificial Intelligence Strategy","AI strategy","—","adopted","2026-2030","English"),
 ("African Union","Continental Artificial Intelligence Strategy","AI strategy (continental)","African Union Commission","adopted","","English"),
]
FILES = {c: NS/f"{f}" for c,f in {
 "Benin":"benin_ai.txt","Côte d'Ivoire":"cote_divoire_ai.txt","Egypt":"egypt_ai.txt",
 "Ethiopia":"ethiopia_ai.txt","Ghana":"ghana_ai.txt","Kenya":"kenya_ai.txt",
 "Mauritius":"mauritius_ai.txt","Morocco":"morocco_ai.txt","Nigeria":"nigeria_ai.txt",
 "Rwanda":"rwanda_ai.txt","Senegal":"senegal_ai.txt","South Africa":"south_africa_ai.txt",
 "Tanzania":"tanzania_ai.txt","Zimbabwe":"zimbabwe_ai.txt","African Union":"african_union_ai.txt"}.items()}

DH_META = [("Rwanda","The National Digital Health Strategic Plan","Digital health strategy","Ministry of Health","superseded","2018-2023","English","rwanda_dh.txt"),
 ("Namibia","National eHealth Strategy","eHealth strategy","Ministry of Health & Social Services","current","2021-2025","English","namibia_dh.txt"),
 ("Mauritius","A Roadmap for Digital Health Transformation in Mauritius","Digital health roadmap","Ministry of Health and Wellness / UNDP","current","","English","mauritius_dh.txt"),
 ("Uganda","Digital Transformation Roadmap","Digital transformation","—","current","2023/24-2027/28","English","uganda_dh.txt")]

rows=[]
for c,t,dom,body,st,per,lang in PRIMARY:
    f=FILES[c]; txt=f.read_text(encoding="utf-8",errors="ignore")
    rows.append(dict(collection="AI strategies", country=c, document_title=t, policy_domain=dom,
        issuing_body=body, status=st, planning_period=per, language=lang,
        local_filename=f.name, word_count=len(txt.split()),
        years_mentioned=years(txt), source_url="TO CONFIRM"))
for c,t,dom,body,st,per,lang,fn in DH_META:
    f=DH/fn; txt=f.read_text(encoding="utf-8",errors="ignore")
    rows.append(dict(collection="Digital health / transformation", country=c, document_title=t,
        policy_domain=dom, issuing_body=body, status=st, planning_period=per, language=lang,
        local_filename=fn, word_count=len(txt.split()), years_mentioned=years(txt),
        source_url="TO CONFIRM"))

out=pathlib.Path("data/corpus_metadata.csv")
pd.DataFrame(rows).to_csv(out, index=False)
print("wrote", out, "|", len(rows), "rows")
print()
df=pd.DataFrame(rows)[["collection","country","status","planning_period","word_count"]]
print(df.to_string(index=False))
