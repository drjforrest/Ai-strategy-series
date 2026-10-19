"""Agentic seeker/extractor for Digital Health Canada's public communications.

Exports are resolved lazily (PEP 562) so importing ``dhc_agent`` never eagerly
imports the submodules — this keeps the package free of import cycles.
"""

from __future__ import annotations

__version__ = "0.1.0"

_LAZY: dict[str, str] = {
    "Agent": ".agent",
    "DEFAULT_MISSION": ".config",
    "NotesStore": ".tools",
    "RADAR_MISSION": ".config",
    "RADAR_THEMES": ".config",
    "SEED_URLS": ".config",
    "ToolRunner": ".tools",
    "agent": ".agent",
    "config": ".config",
    "report": ".report",
    "tools": ".tools",
}

__all__ = sorted(_LAZY) + ["__version__"]


def __getattr__(name: str):
    """Lazily import a submodule/attribute on first access."""
    module_name = _LAZY[name]
    import importlib

    module = importlib.import_module(module_name, __name__)
    value = getattr(module, name)
    globals()[name] = value  # cache so subsequent lookups skip __getattr__
    return value
