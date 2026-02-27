#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --upgrade pip >/dev/null
python3 -m pip install structlog pydantic >/dev/null

python3 -m compileall contrib_writer >/dev/null
python3 contrib_writer/contrib_writer.py --preview --preview-weeks 8 --fit-weeks 52 --text "TEST" --spacing 1 >/dev/null

python3 contrib_writer/contrib_writer.py --commit-file /tmp/contrib_writer_check_log.txt --mutation-token check >/dev/null || true

echo "OK"
