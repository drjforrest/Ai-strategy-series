#!/usr/bin/env python3
"""Build the Year 1 Roadmap (Research & Scholarship) as a Word document.
Facts reconciled to the repo as of 7 Oct 2026 (Paper1_methods_precise, Research_program_strategy,
Canada_benchmark_findings, Paper2_HIMSS_submission_FINAL, CIS_definition_section_edited).
Run with: /tmp/docxenv/bin/python _verify/build_year1_roadmap.py
"""
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "drafts" / "Year1_Roadmap_Research_Scholarship_2026-10-07.docx"
FIG1 = ROOT / "outputs" / "figures_for_manuscript" / "Figure1.png"
FIG2 = ROOT / "outputs" / "figures_for_manuscript" / "Figure2.png"

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(sec, side, Inches(1))
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
normal.paragraph_format.space_after = Pt(6)


def runs(par, text):
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not tok:
            continue
        if tok.startswith("**"):
            par.add_run(tok[2:-2]).bold = True
        elif tok.startswith("*"):
            par.add_run(tok[1:-1]).italic = True
        else:
            par.add_run(tok)
    return par


def H(text, level=1):
    doc.add_heading(text, level=level)


def P(text):
    return runs(doc.add_paragraph(), text)


def B(items, style="List Bullet"):
    for it in items:
        runs(doc.add_paragraph(style=style), it)


def N(items):
    B(items, style="List Number")


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def figure(path, caption):
    doc.add_picture(str(path), width=Inches(6.3))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = runs(doc.add_paragraph(), caption)
    for r in cap.runs:
        r.font.size = Pt(9.5)


# ---------------------------------------------------------------- Title
t = doc.add_heading("Year 1 Roadmap for Research and Scholarship", level=0)
P("*Computational Implementation Science in Global Digital Health*")
P("Jamie I. Forrest, PhD, MPH  |  MS Health Informatics, Northeastern University, Vancouver  |  Draft, October 7, 2026")

# ---------------------------------------------------------------- Challenge
H("The Challenge")
P("AI and digital health policy has expanded rapidly across global health systems, with governments, multilateral agencies, and private actors producing increasingly sophisticated strategies, roadmaps, and governance frameworks. These strategies often signal high levels of ambition, emphasizing transformation through artificial intelligence, data-driven health systems, and digital infrastructure modernization.")
P("Despite this proliferation of policy activity, there remains a persistent and structurally important misalignment between policy intent, workforce and system capacity, and real-world implementation conditions.")
P("In many contexts, particularly across low- and middle-income health systems but also in high-income settings such as Canada, AI and digital health strategies are formulated as if enabling conditions already exist or will emerge in parallel. In practice, those conditions (technical infrastructure, trained workforce capacity, regulatory maturity, interoperability standards, and sustainable investment pathways) are uneven, fragmented, or underdeveloped.")
P("The result is a recurring translation gap between what policies assume is possible and what health systems can actually operationalize. The gap is not merely technical; it is structural. It emerges from the interaction of three partially decoupled systems:")
B([
    "**Policy ecosystems,** which often prioritize vision-setting, innovation narratives, and strategic positioning.",
    "**Workforce ecosystems,** which vary significantly in their ability to produce the competencies that digital and AI-enabled health systems require.",
    "**Investment ecosystems,** where private and public capital may reinforce selected components of digital transformation while neglecting system-wide integration and equity.",
])
P("Implementation is therefore treated as a downstream challenge rather than an embedded design constraint, and ambitious digital health strategies risk becoming aspirational artifacts rather than executable system blueprints.")
P("A further complication is that established implementation science frameworks, while robust for evaluating discrete interventions, are less equipped to analyze policy-to-system alignment at scale, particularly when the intervention is itself computational and its enabling conditions are shaped by rapidly evolving AI capabilities and cross-sector investment. This creates a need for an integrative analytical approach capable of:")
B([
    "Linking policy language to measurable system capacity.",
    "Evaluating whether governance assumptions are operationally valid.",
    "Mapping alignment (or misalignment) across policy, workforce, and capital systems.",
    "Providing scalable, reproducible computational methods for comparison across regions and over time.",
])
P("Without such an approach, digital transformation in health systems will continue to be driven by policy aspiration rather than implementation feasibility, deepening inequities, inefficiencies, and fragmented system development. This research program responds by developing a framework for **Computational Implementation Science in Global Digital Health**, designed to interrogate systematically how AI and digital health strategies move, or fail to move, from conceptual intent to real-world operational capacity.")

# ---------------------------------------------------------------- Aims
H("Aims and Objectives")
H("Overall Aim (Year 1)", 2)
P("To examine critically how AI and digital health strategies are conceptualized, operationalized, and enacted across African health systems, with Canada as a high-income benchmark, identifying gaps between policy intent, workforce capacity, and real-world implementation. The overarching goal is a coherent conceptual and empirical foundation for an emerging field of Computational Implementation Science in Global Digital Health that integrates policy analysis, workforce studies, and investment flows.")
H("Specific Objectives", 2)
N([
    "**Analyze AI strategies as policy instruments.** Examine whether African AI strategies engage the competencies required for safe, effective, and equitable digital health systems, and whether policy emphasis corresponds to independently measured capability (Paper 1).",
    "**Test the connectivity of AI and health policy.** Determine whether national AI strategies and national digital health strategies function as one connected policy system or two parallel, unlinked streams, and what that means for implementation coherence (Paper 2a).",
    "**Test whether the gap is structural or a design choice.** Apply the same instrument to Canada's national AI strategy (*AI for All*, June 2026) and the Pan-Canadian Health Data Strategy (Expert Advisory Group reports), and compare their competency profiles and connectivity with the African corpus (Paper 2b).",
    "**Evaluate workforce training pipelines against policy-assumed competencies.** Assess whether health informatics and digital health training programs produce the competencies that national strategies assume, using a responsible-AI competency overlay derived from Papers 1 and 2 (Paper 3).",
    "**Examine private capital in African digital health transformation.** Analyze how private investment aligns with or diverges from public AI and digital health strategies, with attention to equity, sovereignty, and digital neocolonial dynamics (Paper 4).",
    "**Name and formalize Computational Implementation Science.** Articulate CIS as the implementation science of computational interventions, with policy, workforce, and capital ecosystems as determinants of whether its computational conditions can be met (Overarching Commentary).",
])

# ---------------------------------------------------------------- Table
H("Table of Activities")
rows = [
    ("Paper 1", "AI strategies (rhetoric)",
     "Do AI strategies engage the competencies safe digital health requires, and does their emphasis track measured capability?",
     "BMJ Global Health",
     "Manuscript v2.0 on the 12 + AU corpus (Oct 5, 2026); self peer review complete. Next: methods precision fixes, then co-author review."),
    ("Paper 2a", "AI strategies vs digital health strategies (connectivity)",
     "Are AI policy and health policy one connected system or two parallel, unlinked streams?",
     "HIMSS27 poster (Global Health Informatics call), then journal",
     "\"Connected Agendas?\" abstract submission-ready. Due 5:00 PM ET, Sunday, Oct 11, 2026; finalize author list."),
    ("Paper 2b", "Canadian benchmark",
     "How do Canada's national AI strategy (AI for All, 2026) and Pan-Canadian Health Data Strategy compare with the African corpus, and is the AI and health-data disconnect structural or a design choice?",
     "e-Health 2027 (Digital Health Canada), Connected Health track; oral first choice",
     "Canadian pair scored with the identical instrument (Oct 6). Abstract due 5:00 PM PT, Oct 20, 2026."),
    ("Paper 3", "The training system (capacity)",
     "Does the workforce being trained actually supply the competencies the policies assume?",
     "Decided after results (HELINA, AMIA, MedInfo, or JMIR)",
     "Data extraction started; protocol v0.1 (Oct 5) under revision with four design gates open."),
    ("Paper 4", "Private capital for digital (and health) transformation",
     "How do AI strategies align with reported private-sector investment?",
     "Lancet Global Health, with a critique of digital neocolonialism",
     "Concept only; exploratory policy and capital divergence analysis (Oct 6)."),
    ("Commentary", "Computational Implementation Science",
     "Can CIS be named and formalized to open new opportunities for the real-world evaluation of computational, including large language model-based, interventions?",
     "Implementation Science Communications (Debate) or npj Digital Medicine (Perspective)",
     "In draft; to be strategically timed, not rushed."),
]
headers = ("Paper", "Object of study", "Question in one line", "Target output", "Status and key dates")
widths = (Inches(0.85), Inches(1.05), Inches(1.95), Inches(1.15), Inches(1.5))
tbl = doc.add_table(rows=1, cols=5)
tbl.style = "Table Grid"
tbl.autofit = False
for j, h in enumerate(headers):
    c = tbl.rows[0].cells[j]
    c.text = ""
    r = c.paragraphs[0].add_run(h)
    r.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    shade(c, "1F3864")
for row in rows:
    cells = tbl.add_row().cells
    for j, val in enumerate(row):
        cells[j].text = ""
        r = cells[j].paragraphs[0].add_run(val)
        if j == 0:
            r.bold = True
for row in tbl.rows:
    for j, c in enumerate(row.cells):
        c.width = widths[j]
        for p in c.paragraphs:
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.size = Pt(9)
doc.add_paragraph()

# ---------------------------------------------------------------- Methodology overview
H("Methodology: Broad Overview")
P("The program uses a multi-method, mixed qualitative and computational approach to examine alignment between policy intent, system capacity, and implementation reality. One reproducible instrument (clean, segment, embed, score) is carried across the empirical papers, so that findings are comparable across document genres, countries, and languages.")
H("1. Policy and strategy corpus analysis", 2)
P("Structured collection and screening of AI and digital health policy documents across jurisdictions (African Union member states, the African Union itself, and Canada as a benchmark). AI strategies, digital health strategies, and digital transformation strategies are treated as separate census populations rather than pooled.")
H("2. Computational text analysis (NLP)", 2)
B([
    "Multilingual sentence-transformer embeddings (English and French in one semantic space) scored against fixed reference frameworks such as the nine WHO digital health core components.",
    "Measurement of semantic alignment, conceptual overlap, and divergence across policy domains.",
    "Deterministic, embedding-independent checks (lexicons, cross-references, shared actors) wherever a semantic score could be confounded by shared policy register.",
])
H("3. Comparative implementation gap analysis", 2)
B([
    "Strategy emphasis against independently measured system capacity, with explicit circularity guards.",
    "Policy-defined competencies against workforce training outputs.",
    "Public-sector goals against private-sector investment activity.",
])
H("4. Workforce and training mapping", 2)
P("A census of academic curricula and professional training frameworks in health informatics and digital health, coded against foundational informatics domains and a responsible-AI-in-health overlay, to test whether policy-assumed capability exists in practice.")
H("5. Investment flow analysis", 2)
P("Exploration of private-sector and venture investment in digital health and AI, its geographic and thematic distribution, and its alignment with public strategy.")
H("6. Integrative synthesis", 2)
P("Findings across streams are integrated into a conceptual model of how misalignment emerges across policy, workforce, and capital systems.")

# ---------------------------------------------------------------- Paper 1 example
H("Methodology Example: Paper 1, Rhetoric and Readiness")
P("**Corpus.** Thirteen documents: 12 national AI strategies (Benin, Côte d'Ivoire, Egypt, Ghana, Kenya, Mauritius, Nigeria, Rwanda, Senegal, South Africa, Tanzania, Zimbabwe) and the African Union Continental AI Strategy as a regional anchor, in English and French. Ethiopia and Morocco were excluded a priori on genre grounds and retained as contrast cases.")
P("**Rhetoric measure.** Documents were segmented into overlapping passages of about 150 words, embedded with paraphrase-multilingual-MiniLM-L12-v2, and scored against the nine core components of the WHO Global Strategy on Digital Health 2020–2027. Each component score is the mean of a document's strongest 10 percent of passages (floored at three), which keeps short and long strategies on comparable footing (Figure 1).")
P("**Operationalization measure.** A separate, hand-audited bilingual lexicon scores six execution levers: timelines, budget, agencies, regulation, monitoring, and implementation. The primary index is breadth, the share of levers a strategy addresses at above-median intensity (Figure 2).")
P("**Rhetoric versus readiness.** The same instrument scored each strategy against the nine dimensions of the Oxford Insights Government AI Readiness Index, paired with measured readiness for the 11 countries with Oxford scores (99 country-by-dimension cells). A prespecified circularity guard separates the two dimensions partly scored by reading strategy text (Vision; Governance and Ethics) from the seven built from independent data.")
P("**Results.** Strategy emphasis leaned toward the text-proximate dimensions (mean r = +0.16) and away from the independent ones (mean r = −0.05; pooled r = −0.005), in the direction the guard predicts, but the separation was not statistically significant (exact permutation p = 0.083) and is reported as exploratory. Alignment, operationalization, and measured capability behave as non-equivalent constructs. The most durable finding is that the African Union Continental AI Strategy is markedly thin on standards and interoperability relative to the African Union Digital Transformation Strategy.")
P("**Outputs.** The BMJ Global Health manuscript and a reusable, circularity-guarded instrument carried into Papers 2a and 2b. The maturity-model typology originally envisaged is deferred until the operationalization measure is formalized.")
figure(FIG1, "**Figure 1.** AI-strategy alignment with the nine WHO digital health core components, shown as within-component z-scores relative to the 12 national strategies. The African Union strategy is plotted as an anchor and excluded from standardization.")
figure(FIG2, "**Figure 2.** Semantic alignment (mean raw cosine across the nine WHO components) against operationalization breadth (share of six execution levers above the sample median) for the 12 national strategies. Dashed lines mark medians. Strategies that align most closely with WHO language are not those that specify most about execution.")

# ---------------------------------------------------------------- CIS
H("What Is Computational Implementation Science?")
P("**Computational Implementation Science (CIS)** is the implementation science of computational interventions: the study of how tools whose behavior can change after deployment (model versions, decision thresholds, input data distributions, hardware, and vendor dependencies) are adopted, integrated, monitored, adapted, governed, sustained, and ultimately retired in real-world health systems.")
P("The defining condition is not that software is present, but that computational change can alter the identity, performance, or distributional effects of the intervention over time. A stable rule-based reminder delivered through an electronic health record is adequately studied with conventional digital health implementation approaches. A triage model that is retrained, shifts its thresholds across versions, or performs unevenly across subgroups and settings requires additional constructs and measures.")
P("Established frameworks (CFIR, RE-AIM, Proctor's implementation outcomes taxonomy, NASSS, and the Dynamic Sustainability Framework) remain essential. CIS asks what must be added when the intervention is not a fixed innovation. Three gaps are especially important:")
B([
    "**Computational fidelity:** whether the deployed version, threshold, input pipeline, and model behavior match the evaluated specification, not only whether the intervention was delivered as intended.",
    "**Computational maintenance:** sustained performance under changing populations, data, and workflows (calibration, drift, subgroup effects), not only continued delivery.",
    "**Designed exit:** recalibration, restriction, replacement, or retirement treated as legitimate implementation outcomes.",
])
P("**CIS complements implementation science and is distinct from AIM-IS** (Fontaine et al., 2026). The distinction is directional: AIM-IS asks how computational methods can strengthen implementation science; CIS asks how implementation science must adapt when the object being implemented is computational. The two are siblings, not rivals.")
P("**Core contribution.** CIS supports evaluation of not only whether an intervention works, but:")
B([
    "whether the system is structurally capable of supporting it;",
    "whether policy intent is realistically implementable;",
    "whether ecosystem components (policy, workforce, and capital) are aligned.",
])
P("**How the empirical papers relate to CIS.** Papers 1 through 4 use computational methods to measure the outermost layer of computational conditions: whether the policy, workforce, and investment ecosystems on which any AI-enabled health intervention depends are actually in place. The commentary names the field; the papers supply its first measurement instruments.")
P("[Insert CIS circular figure: implementation phases, implementation outcomes, and computational conditions, with the monitor, audit, recalibrate, and suspend loop at the center and AIM-IS outside the circle.]")

H("Why Is CIS Needed?")
P("Current implementation frameworks, and the emerging AIM-IS agenda, do not fully account for:")
B([
    "the speed and scale of AI-enabled health transformation;",
    "the role of large-scale policy ecosystems in shaping implementation;",
    "the influence of private capital on health system design;",
    "the increasingly computational nature of health governance itself.",
])
P("CIS addresses this gap by enabling systematic, computable evaluation of implementation environments rather than isolated interventions.")

# ---------------------------------------------------------------- Partnerships
H("Partnerships for Success")
B([
    "Biomedical Research Institute, Stellenbosch University",
    "Rwanda Biomedical Centre, Government of Rwanda",
    "Centre for Impact, Innovation and Capacity Building for Health Information Systems and Nutrition (CIIC-IN)",
    "Health Equity and Resilience Observatory, University of British Columbia",
    "Bouvé College of Health Sciences, Northeastern University",
])

# ---------------------------------------------------------------- Next steps
H("Next Steps")
H("Measurement upgrades", 2)
P("Evolve current proxies for sector salience and policy and capital alignment into a formal semantic measurement instrument, operationalizing alignment strength as a coded construct rather than keyword co-occurrence. Formalize the six-lever operationalization score (Figure 2) as a coded, inter-rater-checked instrument and apply it to the Canadian corpus.")
H("Currency and scope", 2)
P("Fix a census date for the expanded corpus (about 28 AI strategies identified across African Union member states, up from 13 analyzed), with a scheduled annual refresh, and keep AI, digital health, and digital transformation strategies as separate census populations. Introduce a Phase 2 program-director survey to validate workforce and implementation assumptions directly, addressing cost and ethics explicitly. Consider extending the instrument to additional LMIC regions to test the generalizability of observed alignment patterns.")
H("Teaching integration", 2)
P("Embed the responsible-AI overlay and Canadian benchmark outputs in MSHI curriculum development as structured teaching artifacts for digital health governance, implementation science, and AI policy modules. A Canadian pilot of the Paper 3 overlay on five to eight health informatics programs will calibrate coding before the African census and feed directly into MSHI program design. Align outputs with annual teaching and scholarship goals so the research program and the curriculum develop together.")

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
print(f"wrote {OUT}")
