#!/usr/bin/env bash
set -euo pipefail
set -x

python -m compileall contrib_writer >/dev/null
python contrib_writer/contrib_writer.py --preview --preview-weeks 8 --fit-weeks 52 --text "TEST" --spacing 1 >/dev/null

python -m pip install --upgrade pip >/dev/null
python -m pip install structlog pydantic >/dev/null
python contrib_writer/contrib_writer.py --commit-file /tmp/contrib_writer_check_log.txt --mutation-token check >/dev/null || true

echo "OK"
