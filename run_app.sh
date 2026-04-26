#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="

mkdir -p output

if [ ! -f "venv/bin/activate" ]; then
    rm -rf venv
    python3 -m venv --without-pip venv
    curl -sS https://bootstrap.pypa.io/get-pip.py | venv/bin/python3
fi

source venv/bin/activate
pip install -r requirements.txt --quiet
python3 app.py
