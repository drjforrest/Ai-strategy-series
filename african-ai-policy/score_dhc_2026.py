"""Score Canadian HI/HIM curricula and the pan-Canadian policy corpus against the
Digital Health Canada HIP Core Competencies.

Reproduces curriculum/score_curriculum_dhc.py exactly for --reference 2022 and
extends it to the 2026 Edition (65 statements, 7 domains, no sub-item splits),
adding the AI-explicit statement sub-profile.

Instrument unchanged: clean -> chunk (150w, 20w overlap, >=25w) ->
paraphrase-multilingual-MiniLM-L12-v2 -> cosine -> top_frac_mean (top 10%, floor 3).
"""
from __future__ import annotations

import argparse
import sys
from itertools import permutations
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path("/Users/j.forrest/dev/projects/data-science/ai-strategy-series/african-ai-policy")
sys.path.insert(0, str(REPO_ROOT))
import analyze_canada_benchmark as acb                      # noqa: E402
from src import alignment, competencies, preprocess         # noqa: E402
from src.models import load_embedding_model                 # noqa: E402

REPO = REPO_ROOT
PROJ = Path("/Users/j.forrest/dev/projects/data-science/Canadian-curriculum-AI-competencies")
RAW = PROJ / "paper2b_canada_ecosystem" / "raw"
CORPUS = RAW / "curriculum" / "corpus"
CANADA = REPO / "data" / "canada"

POLICY = {
    "AI for All (2026)": CANADA / "canada_ai.txt",
    "EAG reports (2021-22)": CANADA / "canada_hd.txt",   # the three EAG reports, concatenated
    "Interoperability Roadmap (2023)": RAW / "roadmap.txt",
    "AI4H principles (2025)": RAW / "ai4h.txt",
}
MIN_CHUNKS_PRIMARY, MIN_CHUNKS_FLOOR = 10, 3

REFS = {
    "2022": dict(
        statements=REPO / "data/dhc_competencies/Health Informatics Core Competencies Framework.csv",
        smap=REPO / "data/dhc_competencies/Health Information Management Competency Statements (CA Exam Tested).csv",
        smap_cols=["competency_id", "statement_id", "domain_id", "ca_exam_tested"],
    ),
    "2026": dict(
        statements=REPO / "data/dhc_competencies/2026/dhc_hip_competencies_2026_statements.csv",
        smap=REPO / "data/dhc_competencies/2026/dhc_statement_map_2026.csv",
        smap_cols=["competency_id", "statement_id", "domain_id", "ai_explicit"],
    ),
}


def ai_density(path: Path) -> tuple[int, int, float]:
    text = preprocess.clean_text(preprocess.load_text(path))
    n, w = len(acb.AI_TERM_RE.findall(text)), len(text.split())
    return n, w, (1000 * n / w if w else np.nan)


def convergence(mat: pd.DataFrame, programmes: list[str], anchors: list[str]):
    mu = mat.loc[programmes].mean()
    sd = mat.loc[programmes].std(ddof=0).replace(0, 1.0)
    z = (mat - mu) / sd
    anchor_vecs = {a: z.loc[a].to_numpy(float) for a in anchors}
    anchor_vecs["Pooled policy"] = np.mean([anchor_vecs[a] for a in anchors], axis=0)
    rows = []
    for p in programmes:
        v = z.loc[p].to_numpy(float)
        row = {"programme_id": p}
        for a, av in anchor_vecs.items():
            vc, ac = v - v.mean(), av - av.mean()
            row[f"r_{a}"] = float(vc @ ac / (np.linalg.norm(vc) * np.linalg.norm(ac)))
        rows.append(row)
    return pd.DataFrame(rows), z


def _ranks(v: np.ndarray) -> np.ndarray:
    order = np.argsort(-v, kind="mergesort")
    ranks = np.empty(len(v), float)
    ranks[order] = np.arange(1, len(v) + 1, dtype=float)
    sv = np.sort(v)[::-1]
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and np.isclose(sv[j + 1], sv[i]):
            j += 1
        if j > i:
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[np.isclose(v, sv[k])] = avg
        i = j + 1
    return ranks


def _spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = _ranks(a) - _ranks(a).mean(), _ranks(b) - _ranks(b).mean()
    den = np.linalg.norm(ra) * np.linalg.norm(rb)
    return float(ra @ rb / den) if den else np.nan


def order_concordance(dom: pd.DataFrame, reg: pd.DataFrame, text_set: str,
                      min_chunks: int) -> pd.DataFrame:
    doms = list(dom.columns)
    policy_docs = [c for c in dom.index if not str(c).startswith("CA-P")]
    pooled = dom.loc[policy_docs, doms].to_numpy(float).mean(axis=0)
    rows = []
    for group in ("named", "adjacent"):
        ids = reg.loc[(reg.group == group) & (reg[f"{text_set}_chunks"] >= min_chunks),
                      "programme_id"].tolist()
        ids = [p for p in ids if p in dom.index]
        if len(ids) < 2:
            continue
        profile = np.median(dom.loc[ids, doms].to_numpy(float), axis=0)
        rho = _spearman(profile, pooled)
        obs = abs(rho)
        hits = total = 0
        for perm in permutations(range(len(pooled))):
            total += 1
            if abs(_spearman(profile, pooled[list(perm)])) >= obs - 1e-12:
                hits += 1
        rows.append({"text_set": text_set, "min_chunks": min_chunks, "group": group,
                     "n_programmes": len(ids), "n_domains": len(doms),
                     "rho_order_vs_pooled_policy": round(rho, 4),
                     "exact_permutation_p": round(hits / total, 4),
                     "n_permutations": total,
                     "domain_order": " > ".join(d for _, d in
                                                sorted(zip(profile, doms), reverse=True))})
    return pd.DataFrame(rows)


def score(docs: dict[str, Path], comp_df, comp_embeds, model) -> pd.DataFrame:
    rows = [{"country": d, "chunk_id": i, "chunk_text": c}
            for d, p in docs.items() for i, c in enumerate(preprocess.load_and_chunk(p))]
    frame = pd.DataFrame(rows, columns=["country", "chunk_id", "chunk_text"])
    return alignment.build_alignment_scores(frame, comp_df, comp_embeds, model,
                                            cache_embeddings=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference", choices=sorted(REFS), required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    cfg = REFS[args.reference]
    OUT = Path(args.out); OUT.mkdir(parents=True, exist_ok=True)

    comp_df = competencies.load_competencies(cfg["statements"])
    smap = pd.read_csv(cfg["smap"])[cfg["smap_cols"]]
    reg = pd.read_csv(CORPUS / "programme_corpus_register.csv")
    model = load_embedding_model()
    if not model.name.startswith("sentence-transformers"):
        raise SystemExit(f"ABORT: backend {model.name}")
    print("model:", model.name, "| reference:", args.reference,
          "|", len(comp_df), "reference items ->", smap.statement_id.nunique(), "statements")
    comp_embeds = competencies.embed_competencies(comp_df, model, save_path=None)
    group_keys = [c for c in ("statement_id", "domain_id", "ca_exam_tested", "ai_explicit")
                  if c in smap.columns]

    for text_set in ("primary", "extended"):
        elig = reg[(reg[f"{text_set}_chunks"] >= MIN_CHUNKS_FLOOR) & (reg.group != "unresolved")]
        docs = dict(POLICY)
        docs.update({pid: CORPUS / text_set / f"{pid}.txt" for pid in elig.programme_id})
        long = score(docs, comp_df, comp_embeds, model).merge(smap, on="competency_id")
        stmt = long.groupby(["country"] + group_keys, as_index=False)["similarity_score"].mean()
        stmt.to_csv(OUT / f"statement_long_{text_set}.csv", index=False)

        dom = stmt.pivot_table(index="country", columns="domain_id", values="similarity_score")
        dom.to_csv(OUT / f"domain_matrix_{text_set}.csv")
        smat = stmt.pivot_table(index="country", columns="statement_id", values="similarity_score")
        smat.to_csv(OUT / f"statement_matrix_{text_set}.csv")

        subsets = {"": dom, "stmt_": smat}
        if "ca_exam_tested" in stmt.columns:
            subsets["exam_"] = stmt[stmt.ca_exam_tested].pivot_table(
                index="country", columns="domain_id", values="similarity_score")
        if "ai_explicit" in stmt.columns:
            ai_stmt = stmt[stmt.ai_explicit]
            subsets["ai_"] = ai_stmt.pivot_table(index="country", columns="statement_id",
                                                 values="similarity_score")
            subsets["aidom_"] = ai_stmt.pivot_table(index="country", columns="domain_id",
                                                    values="similarity_score")
            ai_stmt.pivot_table(index="country", columns="statement_id",
                                values="similarity_score").to_csv(
                OUT / f"ai_statement_matrix_{text_set}.csv")

        oc = pd.concat([order_concordance(dom, reg, text_set, thr)
                        for thr in (MIN_CHUNKS_PRIMARY, MIN_CHUNKS_FLOOR)], ignore_index=True)
        oc.to_csv(OUT / f"domain_order_concordance_{text_set}.csv", index=False)
        print(oc.to_string(index=False))

        dens = pd.DataFrame([(d, *ai_density(p)) for d, p in docs.items()],
                            columns=["document", "ai_terms", "words", "ai_per_1k"])
        dens.to_csv(OUT / f"ai_density_{text_set}.csv", index=False)

        for thr in (MIN_CHUNKS_PRIMARY, MIN_CHUNKS_FLOOR):
            progs = elig.loc[elig[f"{text_set}_chunks"] >= thr, "programme_id"].tolist()
            for tag, mat in subsets.items():
                conv, z = convergence(mat, progs, list(POLICY))
                conv = conv.merge(reg, on="programme_id").merge(
                    dens.rename(columns={"document": "programme_id"}), on="programme_id")
                conv.to_csv(OUT / f"convergence_{tag}{text_set}_min{thr}.csv", index=False)
                if tag == "":
                    z.to_csv(OUT / f"zprofiles_{text_set}_min{thr}.csv")
            print(f"{text_set} min{thr}: {len(progs)} programmes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
