#!/usr/bin/env bash
# Always run with the project venv interpreter.
#
# The venv is a uv-created spawn of pyenv's 3.12.0
# (.venv/pyvenv.cfg -> home = ~/.pyenv/versions/3.12.0/bin). The ambient
# `python3` on this Mac is 3.9 WITHOUT sentence-transformers, which makes
# src/models.py silently fall back to the lexical TF-IDF backend and produces
# scores that are NOT comparable with the semantic matrix. This shim removes
# the choice.
#
# Usage:
#   ./run.sh analyze_connectivity.py     # any script
#   ./run.sh -m pytest -q                # module form
#   ./run.sh -c "import torch; print(torch.__version__)"
set -euo pipefail

cd "$(dirname "$0")"

PY=".venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "error: $PY not found or not executable." >&2
  echo "Rebuild it with:" >&2
  echo "  uv venv --python 3.12.0 .venv" >&2
  echo "  uv pip install --python .venv/bin/python -r requirements.txt" >&2
  exit 1
fi

exec "$PY" "$@"
