#!/usr/bin/env bash
# Start ExpenseFlow from Git Bash, macOS, or Linux.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "Python 3 is required. Install it, then run this script again." >&2
  exit 1
fi

if [[ ! -x .venv/bin/python ]]; then
  "$PYTHON" -m venv .venv
fi
.venv/bin/python -m pip install -r requirements.txt
exec .venv/bin/python app.py
