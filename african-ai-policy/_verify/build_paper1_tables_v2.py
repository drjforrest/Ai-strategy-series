"""Build Paper 1 tables (corpus v2, reference date 30 Sep 2026) as a Word document.

Every number is read from outputs/ — nothing is typed by hand except document
titles/years/languages in Table 1(a), which come from the source PDFs.

    PYTHONPATH=. python _verify/build_paper1_tables_v2.py
Writes drafts/Paper1_tables_corpus_v2_2026-10-14.docx
"""
from __future__ import annotations

import math
import re
import subprocess
import sys

import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from scipy import stats

from src import config

O = config.OUTPUTS_DIR
OUT = config.PROJECT_ROOT / "drafts" / "Paper1_tables_corpus_v2_2026-10-14.docx"
M = "\u2212"  # true minus


def f(x, d=3, sign=True):
    if pd.isna(x):
        return "—"
    s = f"{x:+.{d}f}" if sign else f"{x:.{d}f}"
    return s.replace("-", M)


def crit_r(n, alpha=0.05):
    t = stats.t.ppf(1 - alpha / 2, n - 2)
    return t / math.sqrt(t * t + n - 2)


# ---------- Table 1(a) metadata (from source PDFs) ----------
DOCS = {
    "Benin": ("National Artificial Intelligence and Big Data Strategy (SNIAM)", "2023", "English"),
    "Côte d'Ivoire": ("Stratégie Nationale de l'Intelligence Artificielle (SNIA 2030)", "2024", "French"),
    "Egypt": ("National Artificial Intelligence Strategy, 2nd ed. (2025–2030)", "2025", "English"),
    "Ethiopia": ("National Artificial Intelligence Policy‡", "2024", "English‡"),
    "Ghana": ("Republic of Ghana National Artificial Intelligence Strategy (2025–2035)", "2025", "English"),
    "Kenya": ("Kenya Artificial Intelligence Strategy (2025–2030)", "2025", "English"),
    "Lesotho": ("Artificial Intelligence Policy and Implementation Plan (second draft)¶", "2025", "English"),
    "Mauritania": ("National Artificial Intelligence Strategy of Mauritania (2025–2029)", "2024", "English"),
    "Mauritius": ("AI for Mauritius: National Artificial Intelligence Strategy (2025–2029)", "2026", "English"),
    "Nigeria": ("National Artificial Intelligence Strategy", "2025", "English"),
    "Rwanda": ("National AI Policy", "2023", "English"),
    "Senegal": ("Stratégie de Développement de l'Intelligence Artificielle", "2023", "French"),
    "South Africa": ("Draft National Artificial Intelligence Policy§¶", "2026", "English"),
    "Tanzania": ("Tanzania National AI Strategy Framework (draft v0.6)¶", "2025", "English"),
    "Zambia": ("National Artificial Intelligence Strategy (2024–2026)", "2024", "English"),
    "Zimbabwe": ("National Artificial Intelligence Strategy (2026–2030)", "2025", "English"),
    "African Union": ("Continental Artificial Intelligence Strategy", "2024", "English"),
}


def add_table(doc, title, header, rows, note=None, bold_rows=()):
    p = doc.add_paragraph()
    r = p.add_run(title); r.bold = True; r.font.size = Pt(10)
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]; c.text = ""
        run = c.paragraphs[0].add_run(str(h)); run.bold = True; run.font.size = Pt(9)
    for k, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(v)); run.font.size = Pt(9)
            if k in bold_rows:
                run.bold = True
            if i > 0 and isinstance(v, str) and (v[:1] in "+−0123456789—" ):
                cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if note:
        note = re.sub(r"(?<![A-Za-z])-(?=\d)", M, note)
        n = doc.add_paragraph(); nr = n.add_run(note); nr.italic = True; nr.font.size = Pt(8)
    doc.add_paragraph()


def main() -> int:
    ops = pd.read_csv(O / "operationalization" / "operationalization_index.csv").set_index("country")
    pdim = pd.read_csv(O / "sensitivity" / "readiness_per_dimension.csv")
    summ = pd.read_csv(O / "sensitivity" / "readiness_summary.csv").set_index("variant")
    loo = pd.read_csv(O / "sensitivity" / "readiness_loo.csv")
    dimmeta = pd.read_csv(O / "rhetoric_vs_readiness" / "per_dimension_correlation.csv")
    s1 = pd.read_csv(O / "au_convergence" / "table_s1_convergence.csv")
    ci = pd.read_csv(O / "au_convergence" / "convergence_bootstrap_ci.csv").set_index("country")
    s2 = pd.read_csv(O / "au_convergence" / "table_s2_threshold_sensitivity.csv")
    auc = pd.read_csv(O / "sensitivity" / "au_convergence_compare.csv")

    doc = Document()
    st = doc.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(10)
    h = doc.add_paragraph(); hr = h.add_run("Paper 1 — tables for corpus v2 (reference date 30 September 2026)")
    hr.bold = True; hr.font.size = Pt(12)
    doc.add_paragraph("Generated from repository outputs on branch corpus-v2-cutoff-2026-09-30 by "
                      "_verify/build_paper1_tables_v2.py. Table 1(b) (WHO domain definitions) is unchanged from v3.0 "
                      "and is not reproduced here.").runs[0].font.size = Pt(8)

    # ---- Table 1(a)
    nat = [c for c in DOCS if c != "African Union"]
    rows = [(c, *DOCS[c], f"{int(ops.loc[c, 'n_words']):,}") for c in nat]
    rows.append(("African Union†", *DOCS["African Union"], f"{int(ops.loc['African Union', 'n_words']):,}"))
    add_table(doc, f"Table 1(a). Countries and AI-strategy documents included in the primary corpus "
                   f"({len(nat)} national + AU; reference date 30 September 2026). Words are the cleaned text used in the analysis.",
              ["Country", "Strategy document", "Year", "Language", "Words"], rows,
              note="† Regional anchor, analysed separately from the national set (word count after the pipeline's text cleaning; 22,159 before cleaning). ‡ Bilingual Amharic/English publication; "
                   "only the English text was analysed (Amharic removed before chunking). § Published for comment in the "
                   "Government Gazette on 10 April 2026 and withdrawn by the Minister on 26 April 2026 after fictitious "
                   "references were identified; retained in the primary analysis and removed in sensitivity analyses "
                   "(Table S4). ¶ Officially published draft or consultation version; eligible under the inclusion rule and removed together in the no-drafts sensitivity analysis (Table S4). Language was not an inclusion criterion. Excluded: Morocco (no stand-alone AI-strategy text), "
                   "Uganda (digital-transformation roadmap), Angola (national AI strategy planned in the ICT White Paper "
                   "2023–2027 but not adopted by the reference date), Libya (Arabic text; PDF extraction could not yet be "
                   "validated), Algeria, Namibia, Tunisia and Cameroon (no full text located by the reference date). Superseded texts replaced: Ghana (2022 draft, 2023–2033) "
                   "and Mauritius (2018 working-group strategy). The Digital Ethiopia 2025/2030 documents are not used.")

    # ---- Table 2
    n_p, n_z = int(summ.loc["primary", "n_countries"]), int(summ.loc["no_ZA", "n_countries"])
    pv = pdim.pivot(index="dimension", columns="variant", values="pearson_r")
    meta = dimmeta.set_index("dimension")
    order = sorted(pv.index, key=lambda d: (not meta.loc[d, "text_proximate"], -pv.loc[d, "primary"]))
    rows = [(d, meta.loc[d, "pillar"], "Text-proximate" if meta.loc[d, "text_proximate"] else "Independent",
             f(pv.loc[d, "primary"]), f(pv.loc[d, "no_ZA"])) for d in order]
    sp, sz = summ.loc["primary"], summ.loc["no_ZA"]
    big = pv["primary"].abs().idxmax()
    add_table(doc, "Table 2. Per-dimension correlation between text-derived strategic emphasis and independently "
                   "measured 2024 Oxford AI readiness, with the circularity guard",
              ["Oxford dimension", "Pillar", "Type", f"Pearson r (n = {n_p})", f"Pearson r, excl. South Africa (n = {n_z})"],
              rows,
              note=(f"Primary set ({n_p} countries, {int(sp.n_cells)} nested country-by-dimension cells): text-proximate "
                    f"mean r = {f(sp.tp_mean_r)}; independent mean r = {f(sp.ind_mean_r)}; separation = {f(sp.separation)}; "
                    f"mean of the nine per-dimension correlations = {f(sp.mean_r_all9)}; exact permutation over the nine "
                    f"dimensions p = {sp.perm_p:.3f} ({int(sp.perm_hits)} of {int(sp.n_perm)} dimension pairs). Excluding "
                    f"South Africa ({n_z} countries, {int(sz.n_cells)} cells): {f(sz.tp_mean_r)}, {f(sz.ind_mean_r)}, "
                    f"{f(sz.separation)}; p = {sz.perm_p:.3f} ({int(sz.perm_hits)} of {int(sz.n_perm)}). No single "
                    f"correlation reaches two-tailed significance (critical |r| ≈ {crit_r(n_p):.2f} at n = {n_p}; "
                    f"{crit_r(n_z):.2f} at n = {n_z}); the largest magnitude is {big} ({f(pv.loc[big, 'primary'])}). "
                    "Positive values indicate that strategies saying more about a dimension also score higher on it. "
                    "Because each dimension is standardised over the same countries, the pooled cell-level r equals "
                    "the mean of the nine per-dimension r and is not reported separately."))

    # ---- Table S1
    rows = [(int(r["rank"]), r.country, f(r.convergence_r), f"{f(ci.loc[r.country, 'lo95'])} to {f(ci.loc[r.country, 'hi95'])}")
            for _, r in s1.iterrows()]
    add_table(doc, "Table S1. Convergence of each national strategy's digital-health competency profile to the "
                   "African Union continental vision (10% aggregation, primary)",
              ["Rank", "Country", "Convergence r", "95% bootstrap CI"], rows,
              note=f"Positive values indicate a competency profile aligned with the continental vision; negative values "
                   f"indicate divergence in relative emphasis. {len(s1)} national entries. Percentile bootstrap over the "
                   f"nine competency domains (20,000 resamples). Intervals excluding zero: " + (", ".join(
                   f"{c} ({'positive' if ci.loc[c, 'lo95'] > 0 else 'negative'})" for c in s1.country
                   if ci.loc[c, "lo95"] > 0 or ci.loc[c, "hi95"] < 0) or "none") + ".")

    # ---- Table S2
    rows = [(r.threshold + (" (primary)" if r.threshold == "10%" else ""), r.rank1, f(r.rank1_r), r.top3)
            for _, r in s2.iterrows()]
    add_table(doc, "Table S2. Aggregation-threshold sensitivity for convergence to the continental vision",
              ["Threshold", "Rank 1", "Rank 1 r", "Top 3"], rows)

    # ---- Table S3
    full = {v: summ.loc[v] for v in ("primary", "no_ZA")}
    rows = []
    for v, lab in (("primary", f"All {n_p} countries"), ("no_ZA", f"Excluding South Africa ({n_z})")):
        rows.append((f"{lab}: none withheld", f(full[v].tp_mean_r), f(full[v].ind_mean_r), f"{full[v].perm_p:.3f}"))
        for _, r in loo[loo.variant == v].iterrows():
            rows.append((f"   {r.country_withheld}", f(r.tp_mean_r), f(r.ind_mean_r), f"{r.perm_p:.3f}"))
    nsig_p = int(loo[(loo.variant == "primary")]["sig_0.05"].sum())
    nsig_z = int(loo[(loo.variant == "no_ZA")]["sig_0.05"].sum())
    sigc = ", ".join(loo[(loo.variant == "primary") & loo["sig_0.05"]].country_withheld)
    tpneg = ", ".join(f"{a} ({'all' if b == 'primary' else 'excl. ZA'})" for a, b in
                      loo[loo.tp_mean_r < 0][["country_withheld", "variant"]].itertuples(index=False))
    allrows = pd.concat([loo[["variant", "tp_mean_r", "ind_mean_r"]],
                         pd.DataFrame([{"variant": v, "tp_mean_r": full[v].tp_mean_r, "ind_mean_r": full[v].ind_mean_r} for v in full])])
    ind_all_neg = bool((allrows.ind_mean_r < 0).all())
    s3_note = ("The independent-dimension mean is negative in every variant. " if ind_all_neg else
               f"The independent-dimension mean is negative in {int((allrows.ind_mean_r < 0).sum())} of {len(allrows)} variants. ")
    s3_note += (f"The text-proximate mean turns negative in some variants ({tpneg}). " if tpneg else
                "The text-proximate mean is positive in every variant. ")
    s3_note += (f"In the full set, {nsig_p} single-country removal{'s' if nsig_p != 1 else ''} reach p ≤ 0.05 ({sigc}); "
                if nsig_p else "No single-country removal reaches p ≤ 0.05 in the full set; ")
    s3_note += (f"excluding South Africa, {nsig_z} do. " if nsig_z else "none does excluding South Africa. ")
    s3_note += "The smallest attainable p is 1/36 = 0.028. This table is the basis for presenting the readiness comparison as exploratory."
    add_table(doc, "Table S3. Leave-one-country-out robustness of the circularity guard",
              ["Country withheld", "Text-proximate mean r", "Independent mean r", "Exact permutation p"], rows,
              bold_rows=(0, n_p + 1),
              note=s3_note)

    # ---- Table S4
    sd = summ.loc["no_drafts"]
    rows = [("Countries / cells", f"{n_p} / {int(sp.n_cells)}", f"{n_z} / {int(sz.n_cells)}", f"{int(sd.n_countries)} / {int(sd.n_cells)}"),
            ("Text-proximate mean r", f(sp.tp_mean_r), f(sz.tp_mean_r), f(sd.tp_mean_r)),
            ("Independent mean r", f(sp.ind_mean_r), f(sz.ind_mean_r), f(sd.ind_mean_r)),
            ("Separation", f(sp.separation), f(sz.separation), f(sd.separation)),
            ("Exact permutation p", f"{sp.perm_p:.3f}", f"{sz.perm_p:.3f}", f"{sd.perm_p:.3f}")]
    for _, r in auc.iterrows():
        rows.append((f"AU convergence r — {r.country}", f"{f(r.profile_r_to_AU_primary)} (rank {int(r.rank_primary)})",
                     "—" if pd.isna(r.profile_r_to_AU_noZA) else f"{f(r.profile_r_to_AU_noZA)} (rank {int(r.rank_noZA)})",
                     "—" if pd.isna(r.profile_r_to_AU_noDrafts) else f"{f(r.profile_r_to_AU_noDrafts)} (rank {int(r.rank_noDrafts)})"))
    add_table(doc, "Table S4. Sensitivity of the main results to excluding South Africa's withdrawn draft and to excluding all draft documents",
              ["Quantity", "Primary (all entries)", "Excluding South Africa", "Excluding all drafts (South Africa, Tanzania, Lesotho)"], rows,
              note="WHO-competency alignment and operationalization scores are computed per document and are unchanged "
                   "by excluding South Africa, except that operationalization breadth is defined relative to the corpus "
                   "median. AU convergence is re-standardised within the reduced national set.")

    # ---- Table S5 (Olufadewa external validity)
    r = subprocess.run([sys.executable, "crosscheck_olufadewa.py"], capture_output=True, text=True,
                       cwd=config.PROJECT_ROOT)
    lines = r.stdout.splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.strip().startswith("country quality_rating"))
    body = []
    for l in lines[i0 + 1:]:
        if not l.strip():
            break
        parts = l.split()
        body.append((" ".join(parts[:-3]), parts[-3], f"{float(parts[-2]):.3f}"))
    rho_line = next(l for l in lines if l.startswith("Spearman(who_alignment"))
    add_table(doc, "Table S5. External validity: WHO-competency alignment of national digital-health strategies "
                   "versus independent expert ratings (Olufadewa et al., 2024)",
              ["Country", "Expert rating", "WHO alignment (digital-health strategy)"], body,
              note=(rho_line.replace("Spearman(who_alignment vs expert rating)", "Spearman ρ (alignment vs rating)")
                    + ". Unit: the dedicated digital-health strategy corpus (Paper 2 Group 2), not the AI strategies; "
                    "Mauritius is absent from the Olufadewa census. Strategies rated 'Strong' sit below the 'Moderate' "
                    "group, indicating that alignment captures articulated emphasis rather than expert-judged quality."))

    # ---- Table S6 (Oxford 2025 temporal-alignment sensitivity)
    o25 = O / "sensitivity" / "oxford2025"
    S6 = pd.read_csv(o25 / "readiness2025_summary.csv")
    P6 = pd.read_csv(o25 / "readiness2025_per_dimension.csv")
    setlab = {"all": "All", "no_ZA": "Excl. South Africa", "predates_index": "Strategy predates index", "no_drafts": "Excl. all drafts"}
    pv6 = P6.pivot(index="dimension", columns="set", values="pearson_r")
    q6 = P6.pivot(index="dimension", columns="set", values="q_BH")
    pill = pd.read_csv(config.DATA_DIR / "oxford_readiness_indices" / "oxford_dimensions_2025_dims14_embed.csv")
    meta6 = P6.drop_duplicates("dimension").set_index("dimension")
    order6 = sorted(pv6.index, key=lambda d: (not meta6.loc[d, "strict_tp"], not meta6.loc[d, "broad_tp"], -pv6.loc[d, "all"]))
    rows = []
    for d in order6:
        typ = "Text-proximate (strict)" if meta6.loc[d, "strict_tp"] else ("Text-proximate (broad only)" if meta6.loc[d, "broad_tp"] else "Independent")
        rows.append((d, typ, *[f"{f(pv6.loc[d, s])} (q = {q6.loc[d, s]:.3f})" for s in ("all", "no_ZA", "predates_index", "no_drafts")]))
    ns = S6.drop_duplicates("set").set_index("set").n_countries.astype(int)
    summ_txt = "; ".join(
        f"{setlab[r.set]} ({int(r.n_countries)} countries), {r.guard} guard: text-proximate {f(r.tp_mean_r)}, "
        f"independent {f(r.ind_mean_r)}, separation {f(r.separation)}, p = {r.perm_p:.3f} ({int(r.perm_hits)}/{int(r.n_perm)})"
        for r in S6.itertuples())
    add_table(doc, "Table S6. Temporal-alignment sensitivity: text-derived emphasis versus Oxford Insights GAIRI 2025 "
                   "readiness (six pillars, 14 dimensions)",
              ["Oxford 2025 dimension", "Type",
               f"r, all (n = {ns['all']})", f"r, excl. South Africa (n = {ns['no_ZA']})",
               f"r, strategy predates index (n = {ns['predates_index']})", f"r, excl. all drafts (n = {ns['no_drafts']})"], rows,
              note=("Pearson r with Benjamini–Hochberg q across the 14 dimensions within each country set. Strict guard: "
                    "Policy vision and Policy commitment (Policy Capacity pillar), whose indicators are scored from the "
                    "existence and content of the national AI strategy. Broad guard adds every dimension with at least one "
                    "strategy- or policy-document-scored indicator (2025 Methodology Report). 'Strategy predates index' "
                    "drops Ghana, Mauritius, South Africa and Zimbabwe (launched March–April 2026; latest 2025 index source "
                    "dated December 2025). Exact permutation tests: " + summ_txt + "."))

    # ---- Table S7 (operationalization vs Oxford 2025 Policy commitment)
    V = pd.read_csv(o25 / "operationalization_vs_policy_commitment.csv")
    J = pd.read_csv(o25 / "operationalization_vs_policy_commitment_data.csv", index_col=0)
    rows = [(c, f"{int(round(r.operationalization_index * 6))}/6", f"{r.policy_commitment_2025:.1f}",
             "post-index" if c in {"Ghana", "Mauritius", "South Africa", "Zimbabwe"} else "")
            for c, r in J.sort_values("policy_commitment_2025", ascending=False).iterrows()]
    vtxt = "; ".join(f"{('all' if r.set == 'all' else 'strategy predates index')}, {r.measure.replace('_', ' ')}: "
                     f"ρ = {f(r.spearman_rho)}, p = {r.p:.3f}, n = {int(r.n)}" for r in V.itertuples())
    add_table(doc, "Table S7. External benchmark for the operationalization index: breadth versus Oxford 2025 "
                   "'Policy commitment' (expert-scored actions, responsible agencies, timeline and budget)",
              ["Country", "Operationalization breadth", "Oxford 2025 Policy commitment", "Timing"], rows,
              note="Spearman rank correlations: " + vtxt + ". 'post-index' marks strategies launched after the 2025 "
                   "index data (scored by Oxford on earlier or draft documents).")

    OUT.parent.mkdir(exist_ok=True)
    doc.save(OUT)
    print(f"wrote {OUT}")
    print("Table 2 summary:", dict(n=n_p, tp=round(sp.tp_mean_r, 3), ind=round(sp.ind_mean_r, 3), p=round(sp.perm_p, 3),
                                  crit=round(crit_r(n_p), 3), largest=(big, round(pv.loc[big, 'primary'], 3))))
    print("S3:", nsig_p, sigc, "| noZA", nsig_z, "| tp<0:", tpneg)
    print("S5:", rho_line, "n rows", len(body))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
