#!/bin/bash
cd "$(dirname "$0")"

echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="

mkdir -p output

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt --quiet
python3 crawler.py
