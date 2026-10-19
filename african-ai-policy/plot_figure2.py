"""Figure 2 (Paper 1, post-reframing): semantic alignment vs operationalization.

Carries the *robust* finding of Paper 1 — that textual alignment with the WHO
competencies and operationalization breadth are distinct constructs — and so
takes the main-figure slot that the exploratory rhetoric-readiness scatter
previously held. The rhetoric-readiness scatter moves to supplementary.

  x = mean WHO core-component alignment (raw cosine, mean of 9 domains)
  y = operationalization breadth (share of 6 execution levers above median)

Countries are annotated; median crosshairs mark the four quadrants. Rwanda and
Zimbabwe anchor the high-operationalization / lower-alignment region; Côte
d'Ivoire and Senegal anchor high-alignment / low-operationalization. The African
Union is excluded (regional anchor, not a national observation).

Inputs : outputs/alignment_scores.csv
         outputs/operationalization/operationalization_index.csv
Output : outputs/figures_for_manuscript/Figure2.png

    ./run.sh plot_figure2.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src import config

ANCHOR = "African Union"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--scores", type=Path, default=config.ALIGNMENT_SCORES_CSV)
    p.add_argument("--ops", type=Path, default=config.OPERATIONALIZATION_CSV)
    p.add_argument("--out", type=Path,
                   default=config.OUTPUTS_DIR / "figures_for_manuscript" / "Figure2.png")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    for pth in (args.scores, args.ops):
        if not pth.exists():
            print(f"Missing input: {pth}")
            return 1

    align = pd.read_csv(args.scores)
    mean_align = (align[align.country != ANCHOR]
                  .groupby("country")["similarity_score"].mean()
                  .rename("mean_alignment"))

    ops = pd.read_csv(args.ops).set_index("country")["operationalization_index"].rename("breadth")

    df = pd.concat([mean_align, ops], axis=1, join="inner").reset_index()
    if df.empty:
        print("No overlapping countries between alignment and operationalization outputs.")
        return 1

    xm, ym = df.mean_alignment.median(), df.breadth.median()

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.axvline(xm, color="#6b6b6b", lw=1, ls="--", zorder=1)
    ax.axhline(ym, color="#6b6b6b", lw=1, ls="--", zorder=1)
    ax.scatter(df.mean_alignment, df.breadth, s=70, color="#0072B2",
               edgecolor="white", linewidth=0.8, zorder=3)
    # Label placement: breadth is discrete (k/6), so countries often share a row.
    # When a point's right-hand neighbour on the same row is close, put its label
    # on the left instead, so adjacent labels never collide.
    xlo, xhi = df.mean_alignment.min(), df.mean_alignment.max()
    close = (xhi - xlo) * 0.12
    df = df.sort_values(["breadth", "mean_alignment"]).reset_index(drop=True)
    for i, r in df.iterrows():
        same_row = df[(abs(df.breadth - r.breadth) < 1e-9) & (df.mean_alignment > r.mean_alignment)]
        left = (not same_row.empty) and (same_row.mean_alignment.min() - r.mean_alignment < close)
        ax.annotate(r["country"], (r.mean_alignment, r.breadth),
                    xytext=(-6, 5) if left else (6, 5), textcoords="offset points",
                    ha="right" if left else "left", fontsize=8.5, color="#222222")

    # Axis limits padded beyond the 0..1 index range so edge points are not clipped.
    ax.set_xlim(xlo - (xhi - xlo) * 0.10, xhi + (xhi - xlo) * 0.12)
    ax.set_ylim(-0.08, 1.10)
    ax.set_yticks([k / 6 for k in range(7)])
    ax.set_yticklabels([f"{k}/6" for k in range(7)])
    # Quadrant labels pinned to the axes corners (independent of the data range).
    for (x, y, t, ha, va) in [(0.02, 0.98, "high operationalization\nlow alignment", "left", "top"),
                              (0.98, 0.98, "high alignment\nhigh operationalization", "right", "top"),
                              (0.02, 0.02, "low alignment\nlow operationalization", "left", "bottom"),
                              (0.98, 0.02, "high alignment\nlow operationalization", "right", "bottom")]:
        ax.text(x, y, t, transform=ax.transAxes, ha=ha, va=va, fontsize=8,
                color="#6b6b6b", style="italic")

    ax.set_xlabel("Mean WHO digital-health competency alignment (raw cosine)", fontsize=10, color="#6b6b6b")
    ax.set_ylabel("Operationalization breadth (share of 6 execution levers above median)",
                  fontsize=10, color="#6b6b6b")
    ax.set_title("Semantic alignment and operationalization are distinct constructs\n"
                 f"(n = {len(df)} national AI strategies; dashed lines = medians)",
                 fontsize=12, color="#222222", weight="bold")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    fig.tight_layout()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=150, facecolor="white", bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote {args.out}")
    print(f"  n = {len(df)}  |  median alignment {xm:.3f}, median breadth {ym:.3f}")
    print("  high breadth: " + ", ".join(df[df.breadth >= ym].sort_values("breadth", ascending=False)["country"]))
    print("  high alignment: " + ", ".join(df[df.mean_alignment >= xm].sort_values("mean_alignment", ascending=False)["country"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
