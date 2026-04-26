#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="

mkdir -p output

if [ ! -f "venv/bin/python3" ]; then
    rm -rf venv
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt --quiet
python3 crawler.py
