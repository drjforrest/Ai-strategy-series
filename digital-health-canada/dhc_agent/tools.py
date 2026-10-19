"""Tools the DHC agent can call: web search, page fetching, file download,
text extraction (PDF/DOCX/HTML), and persistent note-taking.

Every tool returns a plain string, which is what the model sees as the tool
result. Schemas for the model live in :data:`TOOL_SCHEMAS`, and
:meth:`ToolRunner.call` dispatches by name.
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypedDict, final

import requests
from bs4 import BeautifulSoup

from . import config

USER_AGENT = "Mozilla/5.0 (compatible; DHCAgent/1.0; research; +https://digitalhealthcanada.com)"
REQUEST_TIMEOUT = 30
MAX_FETCH_CHARS = 12_000  # characters of page text returned per fetch
MAX_EXTRACT_CHARS = 30_000  # characters of extracted document text returned
MAX_LINKS = 100  # links returned per fetch

# Tags stripped before extracting text, so tool results are mostly prose.
NOISE_TAGS = ("script", "style", "noscript", "form", "nav", "footer", "header", "aside", "iframe")


# --------------------------------------------------------------------------- #
# Low-level HTTP helpers
# --------------------------------------------------------------------------- #
def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def _get(url: str, *, stream: bool = False, timeout: int = REQUEST_TIMEOUT) -> requests.Response:
    """GET with a couple of retries and a small backoff."""
    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            resp = _session().get(url, stream=stream, timeout=timeout)
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            last_exc = exc
            time.sleep(1 + attempt * 2)
    raise RuntimeError(f"GET {url} failed after 3 attempts: {last_exc}")


def _clean_text(raw: str) -> str:
    text = re.sub(r"[ \t]+", " ", raw)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# --------------------------------------------------------------------------- #
# Individual tool implementations
# --------------------------------------------------------------------------- #
TAVILY_TIMELIMIT_DAYS = {"day": 1, "week": 7, "month": 30, "year": 365}


def web_search(query: str, max_results: int = 8) -> str:
    """General web search: Tavily when a key is configured, else DuckDuckGo."""
    try:
        results = _tavily_search(query, max_results, topic="general", days=None)
    except Exception as exc:  # Tavily configured but broken -> fall back quietly
        results = None
        print(f"[warn] Tavily search failed ({exc}); falling back to DuckDuckGo")
    if results is None:
        results = _web_search_ddgs(query, max_results)
    if not results:
        return "No results found."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r.get('title', '')}\n   URL: {r.get('href') or r.get('url', '')}\n   {r.get('body', '')}")
    return "\n\n".join(lines)


def tavily_search(query: str, max_results: int = 10, topic: str = "general", timelimit: str = "month") -> str:
    """Tavily-first deep search with topic and recency controls (radar mode's primary tool)."""
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        return (
            "ERROR: TAVILY_API_KEY is not set. Radar mode relies on Tavily - add your key to .env "
            "(get one at https://app.tavily.com)."
        )
    if topic not in ("general", "news", "finance"):
        topic = "general"
    days = TAVILY_TIMELIMIT_DAYS.get(timelimit, 30)
    try:
        results = _tavily_search(query, max_results, topic=topic, days=days)
    except Exception as exc:
        return f"ERROR: Tavily search failed: {exc}"
    if not results:
        return f"No Tavily results for '{query}' (topic={topic}, last {timelimit})."
    lines = []
    for i, r in enumerate(results, 1):
        date = r.get("published_date") or ""
        head = f"{i}. {r.get('title', '')}  [{date}]" if date else f"{i}. {r.get('title', '')}"
        body = (r.get("body") or "")[:500]
        lines.append(f"{head}\n   URL: {r.get('href', '')}\n   {body}")
    return "\n\n".join(lines)


def _tavily_search(query: str, max_results: int, *, topic: str, days: int | None) -> list[dict[str, str]] | None:
    """Raw Tavily call. Returns None when no API key is configured."""
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        return None
    payload: dict[str, Any] = {
        "api_key": key,
        "query": query,
        "max_results": max_results,
        "search_depth": "basic",
        "include_answer": False,
        "include_raw_content": False,
        "topic": topic,
    }
    if days is not None:
        payload["days"] = days
    resp = requests.post(
        "https://api.tavily.com/search",
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    return [
        {
            "title": r.get("title", ""),
            "href": r.get("url", ""),
            "body": r.get("content", ""),
            "published_date": r.get("published_date", ""),
        }
        for r in resp.json().get("results", [])
    ]


def _web_search_ddgs(query: str, max_results: int) -> list[dict[str, str]]:
    try:
        from ddgs import DDGS
    except ImportError as exc:
        raise RuntimeError(
            "The 'ddgs' package is not installed. Run: pip install -r requirements.txt"
        ) from exc
    with DDGS() as ddgs:
        return ddgs.text(query, max_results=max_results, backend="auto") or []


def fetch_page(url: str) -> str:
    """Fetch a URL and return its title, main text, and outbound links.

    Also usable on listing pages (e.g. /news/page/2/) to discover article links.
    """
    try:
        resp = _get(url)
    except Exception as exc:
        return f"ERROR fetching {url}: {exc}"
    ctype = resp.headers.get("Content-Type", "")
    if "html" not in ctype.lower():
        return (
            f"NOTE: {url} returned Content-Type '{ctype}', not HTML. "
            "If it is a PDF/DOCX attachment, use download_file then extract_text."
        )
    soup = BeautifulSoup(resp.text, "lxml")
    for tag in soup(NOISE_TAGS):
        tag.decompose()
    title = soup.title.get_text(strip=True) if soup.title else url
    article = soup.find("article") or soup.find("main") or soup.body or soup
    text = _clean_text(article.get_text("\n", strip=True))

    links: list[str] = []
    seen: set[str] = set()
    for a in article.find_all("a", href=True):
        href = str(a["href"]).strip()
        if not href.startswith("http"):
            continue
        if href in seen:
            continue
        seen.add(href)
        label = a.get_text(" ", strip=True)[:80]
        links.append(f"{label or '(no label)'} -> {href}")

    out = f"TITLE: {title}\nURL: {url}\n\n{text[:MAX_FETCH_CHARS]}"
    if len(text) > MAX_FETCH_CHARS:
        out += f"\n... (page text truncated at {MAX_FETCH_CHARS} chars)"
    if links:
        out += f"\n\nLINKS ({min(len(links), MAX_LINKS)} of {len(links)}):\n" + "\n".join(links[:MAX_LINKS])
    return out


def download_file(url: str, filename: str | None = None) -> str:
    """Download a file (newsletter PDF, report, etc.) into output/downloads."""
    config.DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    path_part = urllib.parse.urlparse(url).path
    name = filename or urllib.parse.unquote(Path(path_part).name) or "download.bin"
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    dest = config.DOWNLOADS_DIR / name
    if dest.exists():
        return f"Already downloaded: {dest} ({dest.stat().st_size} bytes)"
    try:
        resp = _get(url, stream=True)
    except Exception as exc:
        return f"ERROR downloading {url}: {exc}"
    ctype = resp.headers.get("Content-Type", "")
    with open(dest, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=65536):
            fh.write(chunk)
    return f"Downloaded {dest.stat().st_size} bytes -> {dest} (Content-Type: {ctype})"


def extract_text(path: str) -> str:
    """Extract readable text from a local PDF, DOCX, HTML, or plain-text file."""
    p = Path(path)
    if not p.exists():
        return f"ERROR: file not found: {p}"
    ext = p.suffix.lower().lstrip(".")
    text = ""
    try:
        if ext == "pdf":
            from pypdf import PdfReader

            reader = PdfReader(str(p))
            parts = [f"PDF: {p.name} ({len(reader.pages)} pages)"]
            for i, page in enumerate(reader.pages, 1):
                parts.append(f"--- page {i} ---\n{page.extract_text() or ''}")
            text = "\n".join(parts)
        elif ext in ("docx",):
            from docx import Document

            doc = Document(str(p))
            text = "\n".join(par.text for par in doc.paragraphs if par.text.strip())
        elif ext in ("txt", "md", "markdown", "json", "csv", "xml", "eml"):
            text = p.read_text(errors="replace")
        elif ext in ("html", "htm"):
            soup = BeautifulSoup(p.read_text(errors="replace"), "lxml")
            text = soup.get_text("\n", strip=True)
        else:
            return f"ERROR: unsupported file type '.{ext}' for {p}"
    except Exception as exc:
        return f"ERROR extracting text from {p}: {exc}"
    if not text.strip():
        return f"NOTE: no extractable text found in {p} (it may be a scanned/image-only PDF)."
    truncated = len(text) > MAX_EXTRACT_CHARS
    return text[:MAX_EXTRACT_CHARS] + (f"\n... (truncated at {MAX_EXTRACT_CHARS} chars)" if truncated else "")


# --------------------------------------------------------------------------- #
# Note-taking state
# --------------------------------------------------------------------------- #
class Note(TypedDict):
    """One extracted finding persisted to the corpus."""

    n: int
    source_url: str
    title: str
    date: str
    doc_type: str
    theme: str
    summary: str
    extracted_at: str


@dataclass
class NotesStore:
    """Accumulates extracted findings and persists them to disk."""

    records: list[Note] = field(default_factory=list)

    def add(self, source_url: str, title: str, date: str, doc_type: str, summary: str, theme: str = "other") -> int:
        record: Note = {
            "n": len(self.records) + 1,
            "source_url": source_url,
            "title": title,
            "date": date,
            "doc_type": doc_type,
            "theme": theme,
            "summary": summary,
            "extracted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        self.records.append(record)
        self._persist()
        return record["n"]

    def _persist(self) -> None:
        config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(config.FINDINGS_JSONL, "w", encoding="utf-8") as fh:
            for rec in self.records:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        with open(config.FINDINGS_MD, "w", encoding="utf-8") as fh:
            fh.write("# Extracted findings (raw notes)\n\n")
            for rec in self.records:
                fh.write(
                    f"## {rec['n']}. {rec['title']}\n\n"
                    f"- Date: {rec['date'] or 'n/a'}\n"
                    f"- Type: {rec['doc_type']}\n"
                    f"- Theme: {rec['theme']}\n"
                    f"- Source: {rec['source_url']}\n\n"
                    f"{rec['summary']}\n\n"
                )

    def markdown(self) -> str:
        if not self.records:
            return "No notes recorded yet."
        return "\n".join(
            f"[{r['n']}] {r['date'] or 'n/a'} | {r['doc_type']} | theme={r['theme']} | {r['title']}\n    Source: {r['source_url']}\n    {r['summary']}"
            for r in self.records
        )


# --------------------------------------------------------------------------- #
# Schemas + dispatcher
# --------------------------------------------------------------------------- #
TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for public information (news, newsletters, reports). "
            "Returns ranked results with titles, URLs, and snippets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query, e.g. 'Digital Health Canada newsletter archive'"},
                    "max_results": {"type": "integer", "description": "Max results to return (default 8)."},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tavily_search",
            "description": "Tavily-powered deep web search (radar mode's primary tool). Supports news-topic "
            "search and recency filtering. Use for scanning Digital Health Canada, Canadian digital health, "
            "and Canadian health informatics. Returns dated results with titles, URLs, and snippets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query."},
                    "max_results": {"type": "integer", "description": "Results to return, 1-20 (default 10)."},
                    "topic": {"type": "string", "enum": ["general", "news", "finance"], "description": "news = recent news articles; general = web pages (default general)."},
                    "timelimit": {"type": "string", "enum": ["day", "week", "month", "year"], "description": "Recency window (default month)."},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_page",
            "description": "Fetch a web page and return its title, main text, and links. "
            "Use on article pages and listing pages (e.g. news archive pages) to discover links.",
            "parameters": {
                "type": "object",
                "properties": {"url": {"type": "string", "description": "Absolute URL to fetch."}},
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "download_file",
            "description": "Download a binary file (PDF newsletter, report, etc.) into the downloads folder. "
            "Returns the local path to use with extract_text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Absolute URL of the file."},
                    "filename": {"type": "string", "description": "Optional local filename (defaults to the URL's filename)."},
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "extract_text",
            "description": "Extract readable text from a local file (PDF, DOCX, HTML, TXT) that was "
            "downloaded with download_file. Pass the local path returned by download_file.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Local file path."}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_notes",
            "description": "Persist one extracted finding (news release, newsletter article, report section, "
            "etc.) into the corpus. Call this for every distinct item you extract; the notes feed the final report.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_url": {"type": "string", "description": "URL the information came from."},
                    "title": {"type": "string", "description": "Title of the item."},
                    "date": {"type": "string", "description": "Publication date if known, else empty string."},
                    "doc_type": {"type": "string", "description": "news | newsletter | annual_report | podcast | research | policy | event | other"},
                    "theme": {"type": "string", "description": "Radar theme (optional): dhc_org | digital_health_canada | health_informatics | other", "enum": ["dhc_org", "digital_health_canada", "health_informatics", "other"]},
                    "summary": {"type": "string", "description": "Concise factual summary of key information (3-8 sentences)."},
                },
                "required": ["source_url", "title", "date", "doc_type", "summary"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_notes",
            "description": "Return all notes saved so far. Call this before composing your final answer so the "
            "report is grounded in what was actually extracted.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


@final
class ToolRunner:
    """Executes tool calls and returns string results for the model."""

    notes: NotesStore

    def __init__(self, notes: NotesStore | None = None):
        self.notes = notes or NotesStore()

    def call(self, name: str, arguments: str) -> str:
        args = json.loads(arguments or "{}")
        if name == "web_search":
            return web_search(args.get("query", ""), int(args.get("max_results", 8)))
        if name == "tavily_search":
            return tavily_search(
                args.get("query", ""),
                max_results=max(1, min(20, int(args.get("max_results", 10)))),
                topic=args.get("topic", "general"),
                timelimit=args.get("timelimit", "month"),
            )
        if name == "fetch_page":
            return fetch_page(args.get("url", ""))
        if name == "download_file":
            return download_file(args.get("url", ""), args.get("filename"))
        if name == "extract_text":
            return extract_text(args.get("path", ""))
        if name == "save_notes":
            n = self.notes.add(
                source_url=args.get("source_url", ""),
                title=args.get("title", ""),
                date=args.get("date", ""),
                doc_type=args.get("doc_type", "other"),
                theme=args.get("theme", "other"),
                summary=args.get("summary", ""),
            )
            return f"Saved note #{n}. ({len(self.notes.records)} notes total; use read_notes to see them.)"
        if name == "read_notes":
            return self.notes.markdown()
        return f"ERROR: unknown tool '{name}'"
