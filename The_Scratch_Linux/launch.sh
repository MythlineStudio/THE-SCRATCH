#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"

if ! command -v python3 >/dev/null 2>&1; then
    echo
    echo "=========================================="
    echo "THE SCRATCH REQUIRES PYTHON"
    echo "=========================================="
    echo
    echo "Python 3 was not found."
    echo
    echo "Download Python:"
    echo "https://www.python.org/downloads/"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

if [ ! -x "$VENV_DIR/bin/python" ]; then
    python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m ensurepip --upgrade >/dev/null 2>&1 || true

if [ -f requirements.txt ]; then
    "$VENV_DIR/bin/python" -m pip install -r requirements.txt
fi

"$VENV_DIR/bin/python" -m ui.app

echo
read -p "Press Enter to close..."
