# Paper 2b abstract — number verification and changes from the 6 Oct memo
15 Oct 2026. All values read from `african-ai-policy/outputs/` (corpus v2, regenerated 14 Oct) or computed directly on `data/canada/*.txt`.
The Canadian texts are byte-identical (SHA-1) to `digital-health-canada/docs/canada_{ai,hd}.txt`.

## Source of every number in the abstract
| Abstract value | Source |
|---|---|
| 13,483 / 28,670 words; 37.68 and 0.42 AI terms/1k | `outputs/canada/canada_ai_density.csv` (6 Oct; Canadian inputs unchanged) |
| African AI 19.29–46.86/1k, median 38.56 (n=15) | `outputs/connectivity/ai_density_by_set.csv` (v2) |
| African DH 0.00–1.11/1k (n=15) | same file |
| Canada mean alignment 0.4524 AI / 0.5952 HD; HD > AI on 9/9 | `outputs/canada/canada_alignment_raw.csv` |
| African national AI mean 0.4826 (15, AU excluded); African DH 0.6022 | `outputs/connectivity/alignment_all_sets.csv` (v2) |
| Canada AI below African national AI mean on 7/9 components | computed vs. national-only means |
| C5: HD 0.668 (highest; C9 0.660 is next, margin 0.008), AI 0.442; gap 0.226 (largest Canadian gap) vs African 0.108 | as above |
| Interoperability terms: HD 73, AI 2 (both concern AI models and standards) | regex `interoperab` on cleaned text |
| Cross-references: 0 either way; AI names "health data strategy" 0 times, "Expert Advisory Group" 0; HD names the Pan-Canadian AI Strategy 0 times | `analyze_linkage.py` dictionaries plus targeted regex |
| Jaccard 0.00 under the African agency dictionary; African matched pairs 0.000–0.125 (n=9) | `analyze_linkage._agencies` applied to Canada; `outputs/connectivity/linkage_shared_actors.csv` |
| Canada-specific 7-body list: CIHI and Statistics Canada in both (Jaccard 0.333) | `outputs/canada/canada_linkage_proxy.csv` |

## Corrections to `drafts/Canada_benchmark_findings_2026-10-06.md` (and briefing deck slide 11)
1. **African comparators were v1 (12+AU).** African AI median density is now 38.6, not 35.5, so Canada (37.7) sits just *below* the median (rank 9 of 16), not "at" it. African AI mean alignment is now 0.483 (national only; 0.481 with AU), not 0.472.
2. **"AI strategy names the health-data strategy: Yes" was a regex false positive.** The matched phrase "pan-Canadian health data platform" describes **VITAL**, a clinical-data platform, not the Pan-Canadian Health Data Strategy.
3. **"Canada is more connected (Jaccard 0.333)" is not like-for-like.** That value came from a Canada-specific 7-body list. The African dictionary gives **0.00**. The "design choice" leg of the 6 Oct headline (Canada measurably more connected) does not hold under the identical instrument. The abstract now says the disconnect replicates and that connection remains a design decision not yet taken.
4. **The asymmetry claim ("HD strategy does not name the AI strategy") was confounded by timing.** The EAG reports (2021–2022) predate *AI for All* (June 2026). The fair test is the 2017 Pan-Canadian AI Strategy, which they also do not name.
5. **Do not link to Paper 1's "AU standards gap".** Corpus v2 places the AU anchor below the national mean on all nine domains, so that wording must be re-derived (see `corpus_v2_changes_2026-10-14.md`).
6. **Track name.** The template lists "In Support of Connected Health"; the website now calls it "Bridges Not Silos: The Future of Connected Health".
7. **"Highest domain" for C5 is fragile:** 0.668 vs C9 0.660. The abstract's main C5 claim rests on the gap (0.226 vs 0.108) instead.

## Not rerun
The embedding scores were not re-generated: the Canadian inputs and model are unchanged, and `.venv` is currently missing (`./run.sh` fails), so `analyze_canada_benchmark.py` cannot run as-is. Its hard-coded African reference strings (lines ~156–158, ~212–213) are v1 and should be updated before the next run.
