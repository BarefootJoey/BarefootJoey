## Quickstart

### 1) Preview artwork (no file changes)

```powershell
venv\Scripts\Activate.ps1
python contrib_writer\contrib_writer.py --preview --fit-weeks 52 --preview-weeks 52 --text "GITHUB" --spacing 1 --start-sunday 2025-10-05
```

Add `--list-dates` to print every scheduled date.

### 2) Choose your timeframe

- `--start-sunday YYYY-MM-DD` sets the leftmost column. If the date is not a Sunday, the tool uses the previous Sunday automatically.
- `--fit-weeks N` picks a glyph width that fits within N weeks (includes spacing).

### 3) Record a scheduled day locally

On a day that matches your schedule, run the tool without `--preview` to mutate the commit file (default `contrib_writer\contrib_log.txt`). This signals that a commit is needed.

```powershell
python contrib_writer\contrib_writer.py --text "README"
git add -A
git commit -m "record pixel"
git push
```

### 4) Increase intensity (multiple commits on the same day)

```powershell
for ($i=1; $i -le 10; $i++) {
  python contrib_writer\contrib_writer.py --mutation-token $i
  git add -A
  git commit -m ("intensity " + $i)
}
git push
```

Notes

- Use `--commit-file PATH` to change which file is mutated.
- The tool uppercases text and supports A–Z characters.

