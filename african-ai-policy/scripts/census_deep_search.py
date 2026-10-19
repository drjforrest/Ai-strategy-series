"""Deep census search with Tavily, harvesting and downloading strategy PDFs.

For each country x genre cell in the (filled) census sheet this script:
  1. runs Tavily advanced searches in each of the country's search languages, open web and
     (where known) restricted to official domains;
  2. visits up to N promising HTML result pages and the sheet's own source_url, and harvests
     PDF links from them (many ministry pages link the strategy PDF without it being indexed);
  3. keeps PDF candidates whose URL, title or snippet matches the genre's subject terms;
  4. optionally downloads the top candidates per cell, verifying they are real PDFs, and writes
     a manifest with SHA-256, size, final URL and retrieval time.

It never edits the census sheet. Every PDF is a candidate for human screening.

Setup
  export TAVILY_API_KEY=tvly-...
  PYTHONPATH=/tmp/census_pylib python3 scripts/census_deep_search.py --dry-run          # cost estimate only
  PYTHONPATH=/tmp/census_pylib python3 scripts/census_deep_search.py --genres AI --countries RWA KEN --download

Useful options
  --only-unresolved    cells coded Unresolved in search_outcome
  --only-missing-pdf   cells with a document_title but no source_url ending in .pdf
  --basic              Tavily basic depth (1 credit per query instead of 2)
  --max-downloads N    PDFs downloaded per cell (default 3)

Outputs
  outputs/census_search/tavily_<stamp>_queries.csv     every query, credits, hit count, errors
  outputs/census_search/tavily_<stamp>_candidates.csv  all PDF candidates per cell, ranked
  outputs/census_search/tavily_<stamp>_downloads.csv   manifest of downloaded files
  data/inbox/census_pdfs/<cell_id>/                    downloaded PDFs
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import ssl
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from census_search import (  # noqa: E402  shared helpers and country metadata
    CCTLD, GENRE_CODES, domains_for, languages_for, likely_official, read_cells)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SHEET = ROOT / "data" / "census_search_sheet_filled.xlsx"
OUTDIR = ROOT / "outputs" / "census_search"
PDF_DIR = ROOT / "data" / "inbox" / "census_pdfs"
CACHE = ROOT / ".cache" / "census_tavily"
TAVILY_URL = "https://api.tavily.com/search"
FOREIGN_TLDS = {t for t in CCTLD.values() if "." not in t}  # national ccTLDs, used to drop cross-country hits
UA = "Mozilla/5.0 (research census of public policy documents; Northeastern University)"

# Natural-language phrases (Tavily works best with plain phrases rather than Boolean syntax)
PHRASE = {
    "National AI strategy": {
        "en": "national artificial intelligence strategy",
        "fr": "stratégie nationale de l'intelligence artificielle",
        "pt": "estratégia nacional de inteligência artificial",
        "ar": "الاستراتيجية الوطنية للذكاء الاصطناعي",
        "es": "estrategia nacional de inteligencia artificial",
    },
    "Digital health strategy": {
        "en": "national digital health strategy",
        "fr": "stratégie nationale de santé numérique",
        "pt": "estratégia nacional de saúde digital",
        "ar": "الاستراتيجية الوطنية للصحة الرقمية",
        "es": "estrategia nacional de salud digital",
    },
    "Digital transformation strategy": {
        "en": "national digital transformation strategy",
        "fr": "stratégie nationale de transformation numérique",
        "pt": "estratégia nacional de transformação digital",
        "ar": "الاستراتيجية الوطنية للتحول الرقمي",
        "es": "estrategia nacional de transformación digital",
    },
}

# Accent-free keywords used to judge whether a PDF candidate is on topic (any one must match)
KEYWORDS = {
    "National AI strategy": ["artificial intelligence", "intelligence artificielle", "inteligencia artificial",
                             "inteligência artificial", "ai strategy", "ai policy", "strategie ia", "snia",
                             "الذكاء الاصطناعي", "للذكاء الاصطناعي", "ai", "ia", "nais", "snia"],
    "Digital health strategy": ["digital health", "ehealth", "e-health", "sante numerique", "e-sante",
                                "cybersante", "saude digital", "e-saude", "salud digital", "الصحة الرقمية", "للصحة الرقمية",
                                "health information", "health informatics"],
    "Digital transformation strategy": ["digital transformation", "digital economy", "digital strategy",
                                        "transformation numerique", "economie numerique", "strategie numerique",
                                        "transformacao digital", "economia digital", "transformacion digital",
                                        "التحول الرقمي", "للتحول الرقمي", "الاقتصاد الرقمي", "للاقتصاد الرقمي", "digital master plan", "ict policy"],
}


def fold(s: str) -> str:
    """Lowercase and strip accents so 'Santé numérique' matches 'sante numerique'."""
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(ch for ch in s if not unicodedata.combining(ch)).lower()


def _norm(s: str) -> str:
    """Fold accents and turn URL/file-name separators into spaces ('National_AI_Policy' -> 'national ai policy')."""
    return " " + re.sub(r"[\s_\-+.%/'\u2019()\[\],:;]+", " ", fold(urllib.parse.unquote(s))) + " "


def on_topic(genre: str, *texts: str) -> bool:
    blob = _norm(" ".join(t or "" for t in texts))
    return any(_norm(k) in blob for k in KEYWORDS[genre])


def is_pdf_url(url: str) -> bool:
    return urllib.parse.urlparse(url).path.lower().endswith(".pdf")


def host_of(url: str) -> str:
    return (urllib.parse.urlparse(url).hostname or "").lower().removeprefix("www.")


def tavily(query: str, key: str, depth: str, max_results: int,
           include_domains: list[str] | None = None) -> tuple[list[dict], bool]:
    """Tavily search with an on-disk cache keyed by the full request, so reruns are free."""
    body = {"query": query, "search_depth": depth, "max_results": max_results,
            "include_answer": False, "include_raw_content": False}
    if include_domains:
        body["include_domains"] = include_domains
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (hashlib.sha1(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest() + ".json")
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))["results"], True
    req = urllib.request.Request(TAVILY_URL, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    results = [{"title": r.get("title", ""), "url": r.get("url", ""),
                "snippet": (r.get("content") or "")[:500], "score": r.get("score")}
               for r in data.get("results", [])]
    f.write_text(json.dumps({"request": body, "retrieved": datetime.now(timezone.utc).isoformat(),
                             "results": results}, ensure_ascii=False), encoding="utf-8")
    return results, False


def _ctx(insecure: bool) -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    if insecure:  # some government sites have expired or misconfigured certificates
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch(url: str, insecure: bool, max_bytes: int, timeout: int = 45) -> tuple[bytes, str, str]:
    """Return (body, final_url, content_type), reading at most max_bytes.

    Python's TLS stack fails on servers that omit intermediate certificates (e.g. ict.go.ke),
    which macOS curl still verifies against the system trust store. On a verification failure
    we retry once with curl, so certificates are still verified."""
    url = urllib.parse.quote(url, safe=":/?&=%#+,;@~!$'()*[]")  # spaces/accents in some site URLs
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ctx(insecure)) as resp:
            body = resp.read(max_bytes + 1)
            return body, resp.geturl(), resp.headers.get("Content-Type", "")
    except urllib.error.URLError as exc:
        if "CERTIFICATE_VERIFY_FAILED" not in str(exc) or insecure:
            raise
        return fetch_with_curl(url, max_bytes, timeout)


def fetch_with_curl(url: str, max_bytes: int, timeout: int) -> tuple[bytes, str, str]:
    marker = "\n__CURL_META__"
    out = subprocess.run(
        ["curl", "-sSL", "--max-time", str(timeout), "--max-filesize", str(max_bytes + 1),
         "-A", UA, "-w", marker + "%{url_effective}\t%{content_type}", url],
        capture_output=True, timeout=timeout + 10)
    if out.returncode != 0:
        raise RuntimeError(f"curl exit {out.returncode}: {out.stderr.decode(errors='ignore')[:200]}")
    body, _, meta = out.stdout.rpartition(marker.encode())
    final, _, ctype = meta.decode(errors="ignore").partition("\t")
    return body, final or url, ctype


HREF = re.compile(r"""href\s*=\s*["']([^"'#]+?\.pdf(?:\?[^"']*)?)["']""", re.I)


def harvest_pdf_links(page_url: str, insecure: bool) -> list[tuple[str, str]]:
    """PDF links on an HTML page, as (absolute_url, link_text_or_filename)."""
    body, final, ctype = fetch(page_url, insecure, max_bytes=5_000_000)
    if "html" not in ctype.lower():
        return []
    text = body.decode("utf-8", errors="ignore")
    out = []
    for m in HREF.finditer(text):
        absu = urllib.parse.urljoin(final, m.group(1).strip())
        label = urllib.parse.unquote(Path(urllib.parse.urlparse(absu).path).name)
        if absu not in [u for u, _ in out]:
            out.append((absu, label))
    return out


def safe_name(url: str) -> str:
    name = urllib.parse.unquote(Path(urllib.parse.urlparse(url).path).name) or "document.pdf"
    name = re.sub(r"[^\w.\-]+", "_", fold(name))[:120]
    return name if name.endswith(".pdf") else name + ".pdf"


def download_pdf(url: str, cell_id: str, insecure: bool, max_mb: int, seen_sha: set | None = None) -> dict:
    row = {"cell_id": cell_id, "url": url, "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    try:
        body, final, ctype = fetch(url, insecure, max_bytes=max_mb * 1_000_000, timeout=120)
    except Exception as exc:
        return {**row, "status": f"error: {type(exc).__name__}: {exc}"[:300]}
    if len(body) > max_mb * 1_000_000:
        return {**row, "final_url": final, "status": f"skipped: larger than {max_mb} MB"}
    if not body.startswith(b"%PDF"):
        return {**row, "final_url": final, "content_type": ctype, "status": "skipped: not a PDF"}
    sha = hashlib.sha256(body).hexdigest()
    if seen_sha is not None:
        if sha in seen_sha:
            return {**row, "final_url": final, "status": "skipped: identical to an earlier download",
                    "bytes": len(body), "sha256": sha}
        seen_sha.add(sha)
    folder = PDF_DIR / cell_id
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / safe_name(final)
    if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != sha:
        path = path.with_name(path.stem + "_" + sha[:8] + ".pdf")
    path.write_bytes(body)
    return {**row, "final_url": final, "content_type": ctype, "status": "downloaded",
            "bytes": len(body), "sha256": sha, "local_path": str(path.relative_to(ROOT))}


# Country names in the query language (English name used when absent). Without these, a French
# query containing "Morocco" drifts toward France's own national AI strategy.
LOCAL_NAME = {
    "fr": {"CMR": "Cameroun", "CAF": "République centrafricaine", "TCD": "Tchad",
           "COD": "République démocratique du Congo", "GNQ": "Guinée équatoriale", "COM": "Comores",
           "MUS": "Maurice", "DZA": "Algérie", "MRT": "Mauritanie", "MAR": "Maroc", "TUN": "Tunisie",
           "BEN": "Bénin", "GIN": "Guinée", "SEN": "Sénégal", "AU": "Union africaine"},
    "ar": {"TCD": "تشاد", "COM": "جزر القمر", "DJI": "جيبوتي", "ERI": "إريتريا", "SOM": "الصومال",
           "SDN": "السودان", "DZA": "الجزائر", "EGY": "مصر", "LBY": "ليبيا", "MRT": "موريتانيا",
           "MAR": "المغرب", "ESH": "الجمهورية العربية الصحراوية الديمقراطية", "TUN": "تونس",
           "AU": "الاتحاد الأفريقي"},
    "pt": {"GNQ": "Guiné Equatorial", "STP": "São Tomé e Príncipe", "MOZ": "Moçambique",
           "GNB": "Guiné-Bissau", "AU": "União Africana"},
    "es": {"GNQ": "Guinea Ecuatorial", "ESH": "República Árabe Saharaui Democrática"},
}

ALIASES = {"CIV": ["Ivory Coast", "Cote d'Ivoire", "Ivoirien"], "CPV": ["Cape Verde", "Cabo Verde"],
           "COD": ["DRC", "DR Congo", "RDC", "Congo-Kinshasa"], "COG": ["Congo-Brazzaville"],
           "SWZ": ["Swaziland"], "STP": ["Sao Tome"], "GMB": ["The Gambia"], "TZA": ["Tanzanie"],
           "ESH": ["Sahrawi", "Western Sahara"], "AU": ["African Union", "Union africaine", "AU"]}
# Names that are substrings of other countries' names: match as whole words only
WHOLE_WORD = {"niger", "guinea", "guinee", "congo", "sudan", "soudan", "au"}


def mentions_country(cell: dict, *texts: str) -> bool:
    """True if any text names the cell's country (English, local or alias names, accent-folded).

    Whole-word match for ambiguous names (Niger/Nigeria, Guinea/Equatorial Guinea); compact
    substring match otherwise, so 'MauritiusAIStrategy2018.pdf' still matches 'Mauritius'."""
    iso = cell["iso3"]
    names = {cell["country"], *ALIASES.get(iso, [])}
    names |= {d[iso] for d in LOCAL_NAME.values() if iso in d}
    blob = _norm(" ".join(t or "" for t in texts))
    compact = blob.replace(" ", "")
    for n in names:
        nn = _norm(n)
        if nn.strip() in WHOLE_WORD or len(nn.strip()) <= 4:
            if nn in blob:
                return True
        elif nn.replace(" ", "") in compact:
            return True
    return False


def plan_queries(cell: dict) -> list[dict]:
    genre, country, iso = cell["target_genre"], cell["country"], cell["iso3"]
    codes, _ = languages_for(cell)
    official = domains_for(cell)
    src = str(cell.get("source_url") or "")
    if src and likely_official(src, official) and host_of(src) not in official:
        official.append(host_of(src))
    qs = []
    for lang in codes:
        name = LOCAL_NAME.get(lang, {}).get(iso, country)
        q = f"{name} {PHRASE[genre][lang]} pdf"
        qs.append({"scope": "open", "lang": lang, "q": q, "domains": None})
        if official:
            qs.append({"scope": "official", "lang": lang, "q": q, "domains": official})
    title = str(cell.get("document_title") or "").strip()
    if title:  # search the known title directly; often the fastest route to the official PDF
        qs.append({"scope": "title", "lang": "", "q": f"{title} {country} pdf", "domains": None})
    return qs


def select_cells(args) -> list[dict]:
    cells = read_cells(args.sheet)
    if args.countries:
        want = {c.upper() for c in args.countries}
        cells = [c for c in cells if c["iso3"] in want]
    if args.genres:
        want_g = {GENRE_CODES[g] for g in args.genres}
        cells = [c for c in cells if c["target_genre"] in want_g]
    if args.only_unresolved:
        cells = [c for c in cells if c.get("search_outcome") == "Unresolved"]
    if args.only_missing_pdf:
        cells = [c for c in cells if c.get("document_title") and not is_pdf_url(str(c.get("source_url") or ""))]
    return cells


def process_cell(cell: dict, args, key: str, qlog, cand_rows: list) -> list[dict]:
    genre, cid = cell["target_genre"], cell["cell_id"]
    tld = CCTLD.get(cell["iso3"], "")
    official = domains_for(cell)
    cands: dict[str, dict] = {}

    def local(u: str) -> bool:
        """Hosted in the country's own domain, an official domain from the sheet, or govmu.org."""
        h = host_of(u)
        return (bool(tld) and (h == tld or h.endswith("." + tld))) or \
            any(h == d or h.endswith("." + d) for d in official) or \
            (cell["iso3"] == "MUS" and h.endswith("govmu.org"))  # Mauritius uses govmu.org, not .mu

    def add(url, scope, lang, title, snippet, score, via):
        if url in cands:
            return
        h = host_of(url)
        # Drop documents hosted in another African country's domain (e.g. an Egyptian .eg PDF
        # returned for Morocco). Generic domains (.org, .int, .com) are kept for screening.
        if tld != "au.int" and any(h.endswith("." + t) and t != tld for t in FOREIGN_TLDS):
            return
        if tld != "au.int" and (h == "au.int" or h.endswith(".au.int")):
            return  # the continental strategy is the AU cell's document, not a national one
        official_or_local = local(url)
        if scope != "sheet" and not official_or_local and not mentions_country(cell, url, title, snippet):
            return  # third-party document that never names the country (e.g. France's or India's strategy)
        cands[url] = {"cell_id": cid, "country": cell["country"], "target_genre": genre, "url": url,
                      "scope": scope, "lang": lang, "title": title, "snippet": (snippet or "")[:300],
                      "tavily_score": score, "found_via": via,
                      "likely_official": official_or_local and likely_official(url, official),
                      "country_tld": bool(tld) and (h.endswith("." + tld) or h == tld)}

    src = str(cell.get("source_url") or "")
    pages = []
    if src:
        if is_pdf_url(src):
            add(src, "sheet", "", cell.get("document_title") or "", "", None, "sheet source_url")
        else:
            pages.append((src, "sheet"))

    for q in plan_queries(cell):
        row = {"cell_id": cid, "scope": q["scope"], "lang": q["lang"], "query": q["q"],
               "include_domains": ";".join(q["domains"] or []), "depth": args.depth,
               "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        try:
            results, hit = tavily(q["q"], key, args.depth, args.max_results, q["domains"])
            row.update(from_cache=hit, n_results=len(results),
                       credits=0 if hit else (2 if args.depth == "advanced" else 1))
            if not hit:
                time.sleep(args.pause)
        except Exception as exc:
            row.update(error=f"{type(exc).__name__}: {exc}"[:300]); results = []
        qlog.writerow(row)
        for r in results:
            u = r["url"]
            if is_pdf_url(u):
                if on_topic(genre, u, r["title"], r["snippet"]):
                    add(u, q["scope"], q["lang"], r["title"], r["snippet"], r["score"], "tavily result")
            elif on_topic(genre, r["title"], r["snippet"]) and local(u):
                pages.append((u, q["scope"]))

    seen_pages = set()
    for page, scope in pages:
        if page in seen_pages or len(seen_pages) >= args.harvest_pages:
            continue
        seen_pages.add(page)
        try:
            for u, label in harvest_pdf_links(page, args.insecure):
                if on_topic(genre, u, label):
                    add(u, scope, "", label, f"linked from {page}", None, "harvested from page")
        except Exception:
            continue

    ranked = sorted(cands.values(), key=lambda c: (c["scope"] != "sheet", not c["likely_official"],
                                                   not c["country_tld"], -(c["tavily_score"] or 0)))
    for i, c in enumerate(ranked, 1):
        c["rank"] = i
    cand_rows.extend(ranked)
    return ranked


def load_env_key(path: Path, name: str) -> str | None:
    """Read NAME=value from a .env file without printing or exporting it."""
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("export "):
            line = line[7:]
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip("'\"") or None
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", type=Path, default=DEFAULT_SHEET)
    ap.add_argument("--countries", nargs="*", help="ISO3 codes (default: all)")
    ap.add_argument("--genres", nargs="*", choices=list(GENRE_CODES), help="AI DH DT (default: all)")
    ap.add_argument("--only-unresolved", action="store_true")
    ap.add_argument("--only-missing-pdf", action="store_true")
    ap.add_argument("--basic", action="store_true", help="basic depth (1 credit/query) instead of advanced (2)")
    ap.add_argument("--max-results", type=int, default=10)
    ap.add_argument("--harvest-pages", type=int, default=3, help="HTML pages scanned for PDF links per cell")
    ap.add_argument("--download", action="store_true", help="download top PDF candidates")
    ap.add_argument("--max-downloads", type=int, default=3)
    ap.add_argument("--max-mb", type=int, default=80)
    ap.add_argument("--insecure", action="store_true", help="tolerate bad TLS certificates when fetching pages/PDFs")
    ap.add_argument("--pause", type=float, default=3.2, help="seconds between live Tavily calls")
    ap.add_argument("--dry-run", action="store_true", help="show cells, queries and credit estimate only")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    args = ap.parse_args()
    args.depth = "basic" if args.basic else "advanced"

    cells = select_cells(args)
    plans = {c["cell_id"]: plan_queries(c) for c in cells}
    n_q = sum(len(p) for p in plans.values())
    per = 1 if args.basic else 2
    print(f"{len(cells)} cells, {n_q} Tavily queries, depth={args.depth}, "
          f"up to {n_q * per} credits (cached queries cost 0)")
    if args.dry_run:
        for cid, qs in plans.items():
            for q in qs:
                print(f"  {cid:8s} {q['scope']:8s} {q['lang']}  {q['q']}"
                      + (f"   [domains: {', '.join(q['domains'])}]" if q["domains"] else ""))
        return
    key = os.environ.get("TAVILY_API_KEY") or load_env_key(ROOT / ".env", "TAVILY_API_KEY") \
        or sys.exit("Set TAVILY_API_KEY in the environment or in .env at the repo root.")
    if not args.yes and input("Proceed? [y/N] ").strip().lower() != "y":
        return

    OUTDIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    qpath, cpath, dpath = (OUTDIR / f"tavily_{stamp}_{n}.csv" for n in ("queries", "candidates", "downloads"))
    qf = ["cell_id", "scope", "lang", "query", "include_domains", "depth", "run_utc",
          "from_cache", "n_results", "credits", "error"]
    cf = ["cell_id", "country", "target_genre", "rank", "url", "scope", "lang", "found_via",
          "likely_official", "country_tld", "tavily_score", "title", "snippet"]
    df = ["cell_id", "url", "final_url", "status", "bytes", "sha256", "local_path",
          "matches_corpus_file", "content_type", "retrieved_utc"]
    # Hashes of PDFs already in the corpus, so a download can confirm a corpus file's provenance
    corpus_hashes = {}
    if args.download:
        for sub in ("national_strategies", "digital_health_strategies", "AU_strategy"):
            for p in (ROOT / "data" / sub).glob("*.pdf"):
                corpus_hashes[hashlib.sha256(p.read_bytes()).hexdigest()] = str(p.relative_to(ROOT))
    cand_rows: list[dict] = []
    credits = 0
    with qpath.open("w", newline="", encoding="utf-8") as qfh, dpath.open("w", newline="", encoding="utf-8") as dfh:
        qw = csv.DictWriter(qfh, qf); qw.writeheader()
        dw = csv.DictWriter(dfh, df, extrasaction="ignore"); dw.writeheader()

        class Counting:
            def writerow(self, row):
                nonlocal credits
                credits += row.get("credits") or 0
                qw.writerow(row)

        for i, cell in enumerate(cells, 1):
            ranked = process_cell(cell, args, key, Counting(), cand_rows)
            got = 0
            if args.download:
                folder = PDF_DIR / cell["cell_id"]
                seen = {hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob("*.pdf")} \
                    if folder.exists() else set()
                for c in ranked[: args.max_downloads * 2]:  # extra tries absorb duplicates/failures
                    if got >= args.max_downloads:
                        break
                    res = download_pdf(c["url"], cell["cell_id"], args.insecure, args.max_mb, seen)
                    res["matches_corpus_file"] = corpus_hashes.get(res.get("sha256", ""), "")
                    dw.writerow(res); dfh.flush()
                    got += res.get("status") == "downloaded"
            print(f"[{i}/{len(cells)}] {cell['cell_id']:8s} {len(ranked):3d} PDF candidates"
                  + (f", {got} downloaded" if args.download else "") + f"  (credits so far {credits})")

    with cpath.open("w", newline="", encoding="utf-8") as cfh:
        cw = csv.DictWriter(cfh, cf, extrasaction="ignore"); cw.writeheader(); cw.writerows(cand_rows)
    print(f"credits used: {credits}\nwrote {qpath}\nwrote {cpath}" + (f"\nwrote {dpath}" if args.download else ""))


if __name__ == "__main__":
    main()
