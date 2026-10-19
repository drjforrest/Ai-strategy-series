"""Configuration for the Digital Health Canada (DHC) news agent.

Settings come from environment variables (optionally loaded from a local
``.env`` file). See ``.env.example`` for the full list.
"""

from __future__ import annotations

import os
from pathlib import Path

try:  # python-dotenv is optional; plain env vars work fine without it
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
HTTP_REFERER = os.getenv("HTTP_REFERER", "")
APP_TITLE = os.getenv("APP_TITLE", "Digital Health Canada News Agent")
OUTPUT_DIR = Path(os.getenv("DHC_OUTPUT_DIR", "output"))
DOWNLOADS_DIR = OUTPUT_DIR / "downloads"
FINDINGS_JSONL = OUTPUT_DIR / "findings.jsonl"
FINDINGS_MD = OUTPUT_DIR / "findings.md"
TRANSCRIPT_MD = OUTPUT_DIR / "transcript.md"
REPORT_MD = OUTPUT_DIR / "report.md"
REPORT_JSON = OUTPUT_DIR / "report.json"

# Known entry points on digitalhealthcanada.com (verified August 2026).
# The agent is expected to discover more on its own, but these give it a
# reliable starting point so it does not waste budget fumbling around.
SEED_URLS = {
    "news_releases": "https://digitalhealthcanada.com/news/",
    "newsletter_signup": "https://digitalhealthcanada.com/sign-up-for-news/",
    "annual_reports_index": "https://digitalhealthcanada.com/about/annual-reports/",
    "annual_report_2025_26": "https://digitalhealthcanada.com/annual-report-2025-26/",
    "podcasts": "https://digitalhealthcanada.com/podcasts/",
    "homepage": "https://digitalhealthcanada.com/",
}

DEFAULT_MISSION = (
    "Gather and summarize information from Digital Health Canada's public "
    "communications. Specifically: "
    "(1) browse the news/communique archive at https://digitalhealthcanada.com/news/ "
    "(it is paginated as /news/page/N/ - sample a few recent pages), fetch the most "
    "relevant recent articles, and extract their key facts; "
    "(2) look for publicly available newsletter archives (the newsletter sign-up page "
    "is https://digitalhealthcanada.com/sign-up-for-news/; archives may be hosted "
    "externally, e.g. Constant Contact - use web_search to locate them); "
    "(3) check the annual reports at https://digitalhealthcanada.com/about/annual-reports/ "
    "and https://digitalhealthcanada.com/annual-report-2025-26/ and download any PDFs. "
    "Download newsletter/report PDFs into the downloads folder, call save_notes for "
    "every distinct item you extract, then produce a structured report with dates, "
    "titles, key facts, and source URLs. Prefer primary sources on "
    "digitalhealthcanada.com. Do not invent facts - only report what you actually "
    "found in fetched content."
)

# Themes the radar mode sweeps. Used in the radar system prompt and as the
# allowed values of the save_notes 'theme' field.
RADAR_THEMES = {
    "dhc_org": "Digital Health Canada the organization (news, leadership, reports, events)",
    "digital_health_canada": "Digital health in Canada broadly (policy, programs, funding, AI in health, EHR/EMR, telehealth)",
    "health_informatics": "Canadian health informatics (research, academia, conferences, CIHI, HIMSS, professional practice)",
}
RADAR_THEME_KEYS = tuple(RADAR_THEMES)

# Coverage guardrails for radar mode: the loop rejects a final answer until
# every theme has at least this many saved notes, and pushes back at most
# RADAR_MAX_PUSHBACKS times before accepting whatever is available.
RADAR_MIN_ITEMS_PER_THEME = 2
RADAR_MAX_PUSHBACKS = 2

# Rough USD-per-million-token prices for cost estimation (prompt, completion).
# Used only for reporting an estimate at the end of a run.
MODEL_PRICES_USD = {
    "openai/gpt-4o-mini": (0.15, 0.60),
    "openai/gpt-4.1-mini": (0.40, 1.60),
    "openai/gpt-4o": (2.50, 10.00),
}
DEFAULT_MODEL_PRICES_USD = (0.15, 0.60)

RADAR_MISSION = (
    "Act as a Canadian digital-health / health-informatics intelligence radar. Use the "
    "tavily_search tool (preferred; web_search as backup) to sweep the web for recent, "
    "notable developments across three themes: "
    "(1) dhc_org - Digital Health Canada the organization (announcements, leadership, "
    "reports, events); "
    "(2) digital_health_canada - digital health in Canada broadly (federal/provincial "
    "policy and programs, funding, AI in healthcare, EHR/EMR, telehealth, cybersecurity); "
    "(3) health_informatics - Canadian health informatics (research, academic programs, "
    "conferences such as e-Health, CIHI, HIMSS, professional associations). "
    "Run several targeted tavily_search queries per theme, mixing topic=news for recency "
    "and topic=general for depth, with recent timelimits. Fetch the most promising pages, "
    "download any PDF reports/announcements, save one note per distinct item (set the "
    "theme field), and finish with a digest organized by the three themes, each with "
    "dated items, key facts, and source URLs. Distinguish items directly from/about "
    "Digital Health Canada from the wider ecosystem. Only report facts you actually "
    "found in fetched content - never invent dates, quotes, or figures."
)
