## User Guide

### Concepts

- Columns represent weeks, left → right.
- Rows represent weekdays (Sun..Sat), top → bottom.
- A "pixel" is a date where the tool will create/record a commit.

### Fonts and sizing

- Base font is 5x7 (A–Z supported).
- Compact fonts:
  - 3x7 for A–Z when `--font-width 3` is set
  - 3x5 for A–Z when `--font-width 3 --font-height 5` is set (centered vertically)
- Spacing between letters is controlled by `--spacing` (default 1 week column).
- Use `--fit-weeks 52` to auto-compress to fit a year view.

### Start Sunday alignment

- `--start-sunday` accepts any date. If it is not a Sunday, the tool aligns to the previous Sunday.
- If omitted, the tool defaults to the most recent Sunday from today.

### Preview and dry-run

- `--preview` prints ASCII art and exits without touching files.
- `--preview-weeks` limits how many week columns are shown.
- `--list-dates` prints every scheduled date with its column/row.

### Writing commits locally

- Without `--preview`, the tool appends a line to `--commit-file` (default: `contrib_writer\contrib_log.txt`) on days that match the schedule.
- Pair this with a `git add/commit/push` to create contributions on those dates.

### Intensity (darker cells)

- Make multiple commits on a scheduled day. Use `--mutation-token` to ensure each commit changes content.

### Environment variables

Equivalent to CLI flags:

- `TEXT`, `START_SUNDAY`, `SPACING_COLUMNS`, `FONT_WIDTH`, `FONT_HEIGHT`, `FIT_WEEKS`, `PREVIEW_WEEKS`, `COMMIT_FILE`, `MUTATION_TOKEN`

### GitHub Actions (optional automation)

You can run the tool daily in CI to push commits automatically when needed. Create `.github/workflows/contrib-writer.yml`:

```yaml
name: contrib-writer
on:
  schedule:
    - cron: '0 6 * * *'  # daily at 06:00 UTC
  workflow_dispatch: {}

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install structlog pydantic
      - name: Plan once and record intensity commits
        env:
          TEXT: 'BAREFOOTJOEY'
          START_SUNDAY: '2025-10-05'
          SPACING_COLUMNS: '1'
          FONT_WIDTH: '3'
          FIT_WEEKS: '52'
          PREVIEW_WEEKS: '52'
          MULTI_COMMITS: '20'
        run: |
          python contrib_writer/contrib_writer.py --preview --fit-weeks $FIT_WEEKS --preview-weeks $PREVIEW_WEEKS --text "$TEXT" --spacing $SPACING_COLUMNS --start-sunday $START_SUNDAY
          for i in $(seq 1 ${MULTI_COMMITS}); do
            python contrib_writer/contrib_writer.py --mutation-token $i
            git add -A
            git commit -m "intensity $i" || true
          done
      - name: Push changes if any
        run: |
          git push || echo "Nothing to push"
```

Adjust schedule/parameters as desired. The preview step logs the plan for observability.

