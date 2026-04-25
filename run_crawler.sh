#!/bin/bash
cd "$(dirname "$0")"

echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="
pip3 install -r requirements.txt --quiet
python3 crawler.py
