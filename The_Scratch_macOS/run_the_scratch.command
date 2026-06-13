#!/bin/bash
cd "$(dirname "$0")"

export PYTHONPATH="$PWD"
export TK_SILENCE_DEPRECATION=1

python3 -m ui.app
