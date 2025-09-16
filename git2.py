# Create a bundle of handy Python scripts and zip them for download.
import os, zipfile, stat, textwrap, pathlib, json, sys, hashlib, socket, ssl
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

base = "/mnt/data/python-utility-scripts"
os.makedirs(base, exist_ok=True)

def write_executable(rel_name: str, content: str):
    path = os.path.join(base, rel_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.lstrip())
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)
    return path

readme = """
# Python Utility Scripts

All scripts are **stdlib-only** (no extra pip install needed). Make them executable and run with Python 3.11+.

## Included
- `tz_diff.py` — Convert time between timezones or show difference (IST, EDT, etc.).
- `log_watch.py` — Tail a log file with optional regex filter & context.
- `http_check.py` — Check URL status/latency and TLS certificate expiry.
- `dir_tree.py` — Pretty tree of a directory with sizes and ignore patterns.
- `csv_to_json.py` — Convert CSV to JSON (`--ndjson` optional).
- `find_duplicates.py` — Find duplicate files by SHA-256.
- `github_list_prs.py` — List open PRs via GitHub REST (needs `GITHUB_TOKEN`).
- `repo_audit.py` — Quick git repo audit (default branch, last commit, contributors).

## Quick start
```bash
chmod +x *.py
python3 tz_diff.py --from "2025-08-17 10:00" --src America/New_York --dst Asia/Kolkata
python3 log_watch.py app.log --grep "ERROR|WARN" --context 2
python3 http_check.py https://example.com
python3 dir_tree.py . --max-depth 3 --ignore ".git,node_modules"
python3 csv_to_json.py data.csv > data.json
python3 csv_to_json.py data.csv --ndjson > data.ndjson
python3 find_duplicates.py /path/to/dir
GITHUB_TOKEN=... python3 github_list_prs.py owner repo
python3 repo_audit.py
