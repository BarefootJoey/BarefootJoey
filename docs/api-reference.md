## API Reference

### CLI synopsis

```powershell
python contrib_writer\contrib_writer.py [--preview] [--list-dates] [--text TEXT] [--start-sunday YYYY-MM-DD] [--spacing N] [--font-width 3|4|5] [--font-height 5|7] [--fit-weeks N] [--preview-weeks N] [--commit-file PATH] [--mutation-token TOKEN]
```

### Options

- `--text` (env: `TEXT`): message to draw; normalized to uppercase
- `--start-sunday` (env: `START_SUNDAY`): leftmost Sunday (YYYY-MM-DD); auto-aligns to previous Sunday if needed
- `--spacing` (env: `SPACING_COLUMNS`): blank week columns between letters (default 1)
- `--font-width` (env: `FONT_WIDTH`): compress glyphs to 3/4/5 columns; 3 may use handcrafted 3x7 or 3x5
- `--font-height` (env: `FONT_HEIGHT`): compress height to 5 or 7; with `--font-width 3` and `--font-height 5`, uses 3x5 glyphs
- `--fit-weeks` (env: `FIT_WEEKS`): auto-pick a width that fits within N columns (accounts for spacing)
- `--preview` / `--preview-weeks` (env: `PREVIEW_WEEKS`): show ASCII art and exit; clamp to N columns
- `--list-dates`: when previewing, list all scheduled dates
- `--commit-file` (env: `COMMIT_FILE`): file to mutate on scheduled days (default `contrib_writer/contrib_log.txt`)
- `--mutation-token` (env: `MUTATION_TOKEN`): extra token appended to ensure unique lines for multi-commit intensity

### Exit codes

- `0` on success (including no-op days)

### Internals (Python)

Main classes/functions in `contrib_writer/contrib_writer.py`:

- `Settings`: Pydantic model with fields `text`, `start_sunday`, `commit_file`, `spacing_columns`
- `nearest_previous_sunday(day)`: align any date to the preceding Sunday
- `get_start_sunday(settings)`: resolve configured or default start Sunday
- `stitch_text_to_columns(text, spacing, target_width, target_height)`: build a 7-row canvas of 0/1 pixels
- `schedule_dates_for_text(text, start_sunday, spacing, target_width, target_height)`: map dates → (week_col, weekday_row)
- `render_ascii_preview(...)`: produce ASCII art view of the canvas
- `run(settings, preview, list_dates, font_width, font_height, preview_weeks, mutation_token)`: main execution
- `parse_args(argv)`, `main(argv)`: CLI plumbing

Fonts are defined in `contrib_writer/fonts.py` for 5x7, 3x7, and 3x5 glyphs (A–Z).

