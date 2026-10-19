"""Systematic census search for African AI, digital-health and digital-transformation strategies.

Reads the Search_Log tab of data/census_search_sheet.xlsx and, for every country x genre cell,
builds the same structured queries in each of the country's search languages. Queries are run
(or, in plan mode, only written out) under up to three scopes:

  cctld     site:<country TLD>             e.g. site:rw   (site:au.int for the African Union)
  official  site:<domain> for each domain you entered in domains_searched / government_portal_url
  open      no site restriction, country name added (catches partner-hosted copies)

Outputs (in outputs/census_search/):
  <stamp>_queries.csv      every query issued, with scope, language, backend and hit count
  <stamp>_candidates.csv   de-duplicated candidate URLs per cell, with a likely_official flag
  <stamp>_manual_links.html  (plan mode) clickable search links, one block per cell

The script never edits the search sheet. Candidates are for human screening; classification
and eligibility are recorded by hand in census_search_sheet.xlsx.

Backends
  plan    no API; writes queries and clickable links for manual searching (default)
  brave   Brave Search API. Needs env BRAVE_API_KEY.
  google  Google Programmable Search JSON API. Needs env GOOGLE_API_KEY and GOOGLE_CSE_ID
          (engine configured to search the entire web).

Examples
  python scripts/census_search.py                                  # plan mode, all cells
  python scripts/census_search.py --backend brave --countries RWA KEN --genres AI DH
  python scripts/census_search.py --backend brave --scopes cctld official --max-results 10

Requires openpyxl (to read the sheet). Standard library otherwise.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    from openpyxl import load_workbook
except ImportError:  # pragma: no cover
    sys.exit("openpyxl is required: pip install openpyxl")

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "data" / "census_search_sheet.xlsx"
OUTDIR = ROOT / "outputs" / "census_search"
CACHE = ROOT / ".cache" / "census_search"

# ISO3 -> country-code top-level domain (AU uses its own domain)
CCTLD = {
    "BDI": "bi", "CMR": "cm", "CAF": "cf", "TCD": "td", "COG": "cg", "COD": "cd", "GNQ": "gq",
    "GAB": "ga", "STP": "st", "COM": "km", "DJI": "dj", "ERI": "er", "ETH": "et", "KEN": "ke",
    "MDG": "mg", "MUS": "mu", "RWA": "rw", "SYC": "sc", "SOM": "so", "SSD": "ss", "SDN": "sd",
    "TZA": "tz", "UGA": "ug", "DZA": "dz", "EGY": "eg", "LBY": "ly", "MRT": "mr", "MAR": "ma",
    "ESH": "eh", "TUN": "tn", "AGO": "ao", "BWA": "bw", "SWZ": "sz", "LSO": "ls", "MWI": "mw",
    "MOZ": "mz", "NAM": "na", "ZAF": "za", "ZMB": "zm", "ZWE": "zw", "BEN": "bj", "BFA": "bf",
    "CPV": "cv", "CIV": "ci", "GMB": "gm", "GHA": "gh", "GIN": "gn", "GNB": "gw", "LBR": "lr",
    "MLI": "ml", "NER": "ne", "NGA": "ng", "SEN": "sn", "SLE": "sl", "TGO": "tg", "AU": "au.int",
}

LANG_CODES = {"English": "en", "French": "fr", "Portuguese": "pt", "Arabic": "ar", "Spanish": "es"}

# Subject terms by genre and language. Kept deliberately parallel across languages so that
# every country is searched with equivalent terms. Edit here, then report the final lists in Methods.
SUBJECT = {
    "National AI strategy": {
        "en": '"artificial intelligence"',
        "fr": '"intelligence artificielle"',
        "pt": '"inteligência artificial"',
        "ar": '"الذكاء الاصطناعي"',
        "es": '"inteligencia artificial"',
    },
    "Digital health strategy": {
        "en": '("digital health" OR eHealth OR "e-health")',
        "fr": '("santé numérique" OR "e-santé" OR cybersanté)',
        "pt": '("saúde digital" OR "e-saúde")',
        "ar": '"الصحة الرقمية"',
        "es": '("salud digital" OR "e-salud")',
    },
    "Digital transformation strategy": {
        "en": '("digital transformation" OR "digital economy" OR "digital strategy")',
        "fr": '("transformation numérique" OR "économie numérique" OR "stratégie numérique")',
        "pt": '("transformação digital" OR "economia digital")',
        "ar": '("التحول الرقمي" OR "الاقتصاد الرقمي")',
        "es": '("transformación digital" OR "economía digital")',
    },
}
DOCTYPE = {
    "en": "(strategy OR policy OR plan OR roadmap OR framework)",
    "fr": '(stratégie OR politique OR plan OR "feuille de route" OR cadre)',
    "pt": "(estratégia OR política OR plano OR roteiro)",
    "ar": "(استراتيجية OR سياسة OR خطة)",
    "es": '(estrategia OR política OR plan OR "hoja de ruta")',
}

# Hostname patterns that usually indicate a government domain. A flag for screening only;
# confirm by hand before coding hosted_on_official_domain.
GOV_PATTERN = re.compile(r"(^|\.)(gov|gouv|go|govt|gv|gob)\.[a-z]{2}$|(^|\.)gov[a-z]{2}\.org$|(^|\.)au\.int$")


def read_cells(sheet: Path) -> list[dict]:
    """Return one dict per Search_Log row, keyed by the header's first word."""
    ws = load_workbook(sheet, read_only=True, data_only=True)["Search_Log"]
    rows = ws.iter_rows(values_only=True)
    header = [str(h).split(" ")[0] for h in next(rows)]
    return [dict(zip(header, r)) for r in rows if r and r[0]]


def domains_for(cell: dict) -> list[str]:
    """Official domains the searcher entered for this cell (hostnames only)."""
    raw = " ".join(str(cell.get(k) or "") for k in ("government_portal_url", "domains_searched"))
    out = []
    for tok in re.split(r"[;,\s]+", raw):
        tok = tok.strip().lower()
        if not tok:
            continue
        host = urllib.parse.urlparse(tok if "//" in tok else "//" + tok).hostname or ""
        host = host.removeprefix("www.")
        if "." in host and host not in out:
            out.append(host)
    return out


def languages_for(cell: dict) -> tuple[list[str], list[str]]:
    """Split the sheet's suggested languages into searchable codes and unsupported names."""
    names = [s.strip() for s in str(cell.get("search_languages") or "English").split(";")]
    codes = [LANG_CODES[n] for n in names if n in LANG_CODES]
    skipped = [n for n in names if n not in LANG_CODES]
    return codes or ["en"], skipped


def build_queries(cell: dict, scopes: list[str]) -> list[dict]:
    genre, iso = cell["target_genre"], cell["iso3"]
    codes, _ = languages_for(cell)
    qs = []
    for lang in codes:
        base = f"{SUBJECT[genre][lang]} {DOCTYPE[lang]}"
        if "cctld" in scopes and iso != "ESH":
            qs.append({"scope": "cctld", "lang": lang, "q": f"{base} site:{CCTLD[iso]}"})
        if "official" in scopes:
            doms = domains_for(cell)
            if doms:
                site = " OR ".join(f"site:{d}" for d in doms)
                qs.append({"scope": "official", "lang": lang, "q": f"{base} ({site})"})
        if "open" in scopes:
            qs.append({"scope": "open", "lang": lang, "q": f'{base} "{cell["country"]}"'})
    return qs


def _get_json(url: str, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_brave(q: str, n: int) -> list[dict]:
    key = os.environ.get("BRAVE_API_KEY") or sys.exit("Set BRAVE_API_KEY")
    url = "https://api.search.brave.com/res/v1/web/search?" + urllib.parse.urlencode(
        {"q": q, "count": min(n, 20)})
    data = _get_json(url, {"X-Subscription-Token": key})
    return [{"title": r.get("title", ""), "url": r.get("url", ""), "snippet": r.get("description", "")}
            for r in data.get("web", {}).get("results", [])]


def search_google(q: str, n: int) -> list[dict]:
    key = os.environ.get("GOOGLE_API_KEY") or sys.exit("Set GOOGLE_API_KEY")
    cx = os.environ.get("GOOGLE_CSE_ID") or sys.exit("Set GOOGLE_CSE_ID")
    out = []
    for start in range(1, n + 1, 10):  # API returns at most 10 per page
        url = "https://www.googleapis.com/customsearch/v1?" + urllib.parse.urlencode(
            {"key": key, "cx": cx, "q": q, "num": min(10, n - start + 1), "start": start})
        items = _get_json(url).get("items", [])
        out += [{"title": i.get("title", ""), "url": i.get("link", ""), "snippet": i.get("snippet", "")}
                for i in items]
        if len(items) < 10:
            break
    return out


BACKENDS = {"brave": search_brave, "google": search_google}


def cached_search(backend: str, q: str, n: int, pause: float) -> tuple[list[dict], bool]:
    """Run a query once per backend/query/n; reruns read from cache so they cost nothing."""
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (hashlib.sha1(f"{backend}|{n}|{q}".encode()).hexdigest() + ".json")
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))["results"], True
    results = BACKENDS[backend](q, n)
    f.write_text(json.dumps({"backend": backend, "q": q, "n": n,
                             "retrieved": datetime.now(timezone.utc).isoformat(),
                             "results": results}, ensure_ascii=False), encoding="utf-8")
    time.sleep(pause)
    return results, False


def likely_official(url: str, user_domains: list[str]) -> bool:
    host = (urllib.parse.urlparse(url).hostname or "").lower().removeprefix("www.")
    return bool(GOV_PATTERN.search(host)) or any(host == d or host.endswith("." + d) for d in user_domains)


GENRE_CODES = {"AI": "National AI strategy", "DH": "Digital health strategy",
               "DT": "Digital transformation strategy"}


def write_manual_links(path: Path, plan: list[tuple[dict, list[dict]]]) -> None:
    parts = ["<!doctype html><meta charset='utf-8'><title>Census search links</title>",
             "<style>body{font-family:Arial,sans-serif;max-width:1100px;margin:2em auto}"
             "h3{margin-bottom:.2em}code{font-size:.85em}li{margin:.3em 0}</style>",
             "<h1>Census search links</h1><p>One block per country x genre cell. "
             "Record the queries you ran in search_terms_used.</p>"]
    for cell, qs in plan:
        parts.append(f"<h3>{html.escape(cell['cell_id'])}: {html.escape(cell['country'])}, "
                     f"{html.escape(cell['target_genre'])}</h3><ul>")
        for q in qs:
            link = "https://www.google.com/search?q=" + urllib.parse.quote(q["q"])
            parts.append(f"<li>[{q['scope']}, {q['lang']}] <a href='{link}' target='_blank'>"
                         f"<code>{html.escape(q['q'])}</code></a></li>")
        _, skipped = languages_for(cell)
        if skipped:
            parts.append(f"<li><em>Not auto-generated for: {html.escape(', '.join(skipped))}. "
                         "Search by hand if needed.</em></li>")
        parts.append("</ul>")
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backend", choices=["plan", "brave", "google"], default="plan")
    ap.add_argument("--sheet", type=Path, default=SHEET)
    ap.add_argument("--countries", nargs="*", help="ISO3 codes (default: all)")
    ap.add_argument("--genres", nargs="*", choices=list(GENRE_CODES), help="AI DH DT (default: all)")
    ap.add_argument("--scopes", nargs="*", choices=["cctld", "official", "open"],
                    default=["cctld", "official", "open"])
    ap.add_argument("--max-results", type=int, default=10, help="results per query (default 10)")
    ap.add_argument("--pause", type=float, default=1.1, help="seconds between live API calls")
    ap.add_argument("--only-unsearched", action="store_true",
                    help="skip cells whose search_outcome is already filled in")
    args = ap.parse_args()

    cells = read_cells(args.sheet)
    if args.countries:
        wanted = {c.upper() for c in args.countries}
        cells = [c for c in cells if c["iso3"] in wanted]
    if args.genres:
        wanted_g = {GENRE_CODES[g] for g in args.genres}
        cells = [c for c in cells if c["target_genre"] in wanted_g]
    if args.only_unsearched:
        cells = [c for c in cells if not c.get("search_outcome")]
    plan = [(c, build_queries(c, args.scopes)) for c in cells]
    n_q = sum(len(q) for _, q in plan)
    print(f"{len(cells)} cells, {n_q} queries, backend={args.backend}")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    qlog_path = OUTDIR / f"{stamp}_queries.csv"
    qfields = ["cell_id", "country", "target_genre", "scope", "lang", "query", "backend",
               "run_utc", "from_cache", "n_results", "error"]
    cand_fields = ["cell_id", "country", "iso3", "target_genre", "rank", "scope", "lang",
                   "likely_official", "is_pdf", "title", "url", "snippet", "query"]

    if args.backend == "plan":
        with qlog_path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, qfields)
            w.writeheader()
            for cell, qs in plan:
                for q in qs:
                    w.writerow({"cell_id": cell["cell_id"], "country": cell["country"],
                                "target_genre": cell["target_genre"], "scope": q["scope"],
                                "lang": q["lang"], "query": q["q"], "backend": "plan"})
        links = OUTDIR / f"{stamp}_manual_links.html"
        write_manual_links(links, plan)
        print(f"wrote {qlog_path}\nwrote {links}")
        return

    cand_path = OUTDIR / f"{stamp}_candidates.csv"
    with qlog_path.open("w", newline="", encoding="utf-8") as qf, \
         cand_path.open("w", newline="", encoding="utf-8") as cf:
        qw, cw = csv.DictWriter(qf, qfields), csv.DictWriter(cf, cand_fields)
        qw.writeheader(); cw.writeheader()
        for i, (cell, qs) in enumerate(plan, 1):
            seen: set[str] = set()
            user_doms = domains_for(cell)
            for q in qs:
                row = {"cell_id": cell["cell_id"], "country": cell["country"],
                       "target_genre": cell["target_genre"], "scope": q["scope"], "lang": q["lang"],
                       "query": q["q"], "backend": args.backend,
                       "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
                try:
                    results, hit = cached_search(args.backend, q["q"], args.max_results, args.pause)
                    row.update(from_cache=hit, n_results=len(results))
                except Exception as exc:  # log and continue; rerun later from cache
                    row.update(error=f"{type(exc).__name__}: {exc}")
                    results = []
                qw.writerow(row)
                for rank, r in enumerate(results, 1):
                    url = r["url"]
                    if not url or url in seen:
                        continue
                    seen.add(url)
                    cw.writerow({"cell_id": cell["cell_id"], "country": cell["country"],
                                 "iso3": cell["iso3"], "target_genre": cell["target_genre"],
                                 "rank": rank, "scope": q["scope"], "lang": q["lang"],
                                 "likely_official": likely_official(url, user_doms),
                                 "is_pdf": urllib.parse.urlparse(url).path.lower().endswith(".pdf"),
                                 "title": r["title"], "url": url, "snippet": r["snippet"],
                                 "query": q["q"]})
            print(f"[{i}/{len(plan)}] {cell['cell_id']}: {len(seen)} unique candidates")
    print(f"wrote {qlog_path}\nwrote {cand_path}")


if __name__ == "__main__":
    main()
