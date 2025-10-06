Contribution Writer
===================

Plan and render text on your GitHub contributions graph by creating commits only on specific dates. Supports previewing the artwork, narrowing character width to fit 52 weeks, and increasing intensity by making multiple commits on scheduled days.

Files
- `contrib_writer.py`: CLI tool to plan/preview and mutate a file on scheduled days
- `.github/workflows/contrib-writer.yml`: CI workflow to run daily and push commits
- `contrib_writer/contrib_log.txt`: append-only file mutated to trigger commits

Requirements (local)
- Python 3.10+
- `pip install structlog pydantic`

CLI Usage
```powershell
(venv) python contrib_writer/contrib_writer.py [--preview] [--list-dates] [--text TEXT] [--start-sunday YYYY-MM-DD] [--spacing N] [--font-width 3|4|5] [--fit-weeks N] [--preview-weeks N] [--commit-file PATH] [--mutation-token TOKEN]
```

Key options
- `--text`: message to draw (default: BAREFOOTJOEY)
- `--start-sunday`: leftmost Sunday (YYYY-MM-DD). If not a Sunday, it auto-adjusts back to the previous Sunday
- `--spacing`: blank week columns between letters (default: 1)
- `--font-width`: compress letters to width 3/4/5 columns. Width 3 uses a handcrafted 3x7 font for letters in "BAREFOOTJOEY" to preserve shapes
- `--fit-weeks`: auto-pick a font width to fit within N weeks (uses spacing)
- `--preview`: print ASCII preview and exit
- `--preview-weeks`: clamp preview to N week columns (default: 52)
- `--list-dates`: when previewing, list all scheduled dates
- `--commit-file`: file to mutate on scheduled days (default: contrib_writer/contrib_log.txt)
- `--mutation-token`: arbitrary token to force unique lines when doing multiple commits in a loop

Environment variables (equivalents)
- `TEXT`, `START_SUNDAY`, `SPACING_COLUMNS`, `FONT_WIDTH`, `FIT_WEEKS`, `PREVIEW_WEEKS`, `COMMIT_FILE`, `MUTATION_TOKEN`

Preview examples
- 52-week preview, width auto-fit:
```powershell
(venv) python contrib_writer/contrib_writer.py --preview --fit-weeks 52 --preview-weeks 52 --text "TRADINGVIEW" --spacing 1 --start-sunday 2025-10-05

# Example Output:
{"total_pixels": 141, "start_sunday": "2025-10-05", "today": "2025-10-06", "event": "schedule_generated", "level": "info", "timestamp": "2025-10-06T20:21:42.030982Z"}
Start Sunday: 2025-10-05  Weeks: 47  Height: 7
██···█··██··███·███··█···█··███·███··█··███·█·█
█·█·█·█·█·█·█···█···█·█·█·█··█····█·█·█·█···█·█
█·█·█·█·█·█·█···█···█·█·█·█··█····█·█·█·█····█·
██··███·██··██··██··█·█·█·█··█····█·█·█·██···█·
█·█·█·█·██··█···█···█·█·█·█··█··█·█·█·█·█····█·
█·█·█·█·█·█·█···█···█·█·█·█··█··█·█·█·█·█····█·
██··█·█·█·█·███·█····█···█···█···█···█··███··█·
```
- 52-week preview, force 3-column glyphs:
```powershell
(venv) python contrib_writer/contrib_writer.py --preview --preview-weeks 52 --font-width 3 --text "BAREFOOTJOEY" --spacing 1 --start-sunday 2025-10-05

# Example Output:
{"total_pixels": 141, "start_sunday": "2025-10-05", "today": "2025-10-06", "event": "schedule_generated", "level": "info", "timestamp": "2025-10-06T20:19:49.712836Z"}
Start Sunday: 2025-10-05  Weeks: 47  Height: 7
██···█··██··███·███··█···█··███·███··█··███·█·█
█·█·█·█·█·█·█···█···█·█·█·█··█····█·█·█·█···█·█
█·█·█·█·█·█·█···█···█·█·█·█··█····█·█·█·█····█·
██··███·██··██··██··█·█·█·█··█····█·█·█·██···█·
█·█·█·█·██··█···█···█·█·█·█··█··█·█·█·█·█····█·
█·█·█·█·█·█·█···█···█·█·█·█··█··█·█·█·█·█····█·
██··█·█·█·█·███·█····█···█···█···█···█··███··█·
```
- List all dates alongside the preview:
```powershell
(venv) python contrib_writer/contrib_writer.py --preview --list-dates --preview-weeks 52 --font-width 3 --text "BAREFOOTJOEY" --spacing 1 --start-sunday 2025-10-05
```

Intensity (commit multiples)
- To brighten cells, make multiple commits on a scheduled day. Each commit must change tracked content. Use `--mutation-token` to ensure unique lines.

PowerShell (local) example with 50 commits:
```powershell
for ($i=1; $i -le 50; $i++) {
  python contrib_writer\contrib_writer.py --mutation-token $i
  git add -A
  git commit -m "intensity $i"
}
```

GitHub Actions
The workflow `.github/workflows/contrib-writer.yml` runs daily and pushes if there are changes.

Defaults set in the workflow step env:
- `TEXT='BAREFOOTJOEY'`
- `START_SUNDAY='2025-10-05'`
- `SPACING_COLUMNS='1'`
- `FONT_WIDTH='3'`, `FIT_WEEKS='52'`
- `MULTI_COMMITS='50'` (number of intensity commits)

In CI, it performs one planning run and then loops `MULTI_COMMITS` times, writing to `contrib_writer/intensity.txt` and calling the script with `--mutation-token $i` to ensure unique diffs, committing each iteration, and pushing at the end.

Fonts
- Primary font is 5x7 per-letter bitmaps
- A compact handcrafted 3x7 font exists for characters used in "BAREFOOTJOEY" (preserves shapes like `Y`). For other characters at width 3, the script falls back to column-compression which may alter diagonals

Notes
- Columns map to weeks left→right, rows map to weekdays top→bottom (Sun..Sat)
- Choose a `START_SUNDAY` that aligns with the calendar window when you want the art to begin
