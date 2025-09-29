from __future__ import annotations

import argparse
import datetime as dt
import os
from typing import Dict, List, Sequence, Set, Tuple

import structlog
from pydantic import BaseModel, Field, field_validator


logger = structlog.get_logger()


class Settings(BaseModel):
    text: str = Field(default="BAREFOOTJOEY", description="Text to render in the contribution graph (uppercase recommended)")
    start_sunday: str | None = Field(
        default=None,
        description="Leftmost Sunday (YYYY-MM-DD). If not a Sunday, it will be shifted back to the previous Sunday. Defaults to last Sunday from today.",
    )
    commit_file: str = Field(default="contrib_log.txt", description="Path to file to mutate for commits")
    spacing_columns: int = Field(default=1, ge=0, le=3, description="Blank week columns between characters")

    @field_validator("text")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text must be non-empty")
        return value.upper()

    @field_validator("start_sunday")
    @classmethod
    def validate_date_format(cls, value: str | None) -> str | None:
        if value is None:
            return value
        try:
            _ = dt.date.fromisoformat(value)
        except Exception as exc:  # noqa: BLE001
            raise ValueError("start_sunday must be YYYY-MM-DD") from exc
        return value


# 5x7 font for required letters. Each entry is 7 strings of length 5 (rows top->bottom).
FONT_5x7: Dict[str, List[str]] = {
    "A": [
        "01110",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ],
    "B": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10001",
        "10001",
        "11110",
    ],
    "E": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "11111",
    ],
    "F": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "10000",
    ],
    "J": [
        "00111",
        "00001",
        "00001",
        "00001",
        "10001",
        "10001",
        "01110",
    ],
    "O": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ],
    "R": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10100",
        "10010",
        "10001",
    ],
    "T": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
    ],
    "Y": [
        "10001",
        "10001",
        "01010",
        "00100",
        "00100",
        "00100",
        "00100",
    ],
}


# Handcrafted compact 3x7 font for letters used in "BAREFOOTJOEY"
FONT_3x7: Dict[str, List[str]] = {
    "A": [
        "010",
        "101",
        "101",
        "111",
        "101",
        "101",
        "101",
    ],
    "B": [
        "110",
        "101",
        "101",
        "110",
        "101",
        "101",
        "110",
    ],
    "E": [
        "111",
        "100",
        "100",
        "110",
        "100",
        "100",
        "111",
    ],
    "F": [
        "111",
        "100",
        "100",
        "110",
        "100",
        "100",
        "100",
    ],
    "J": [
        "111",
        "001",
        "001",
        "001",
        "101",
        "101",
        "010",
    ],
    "O": [
        "010",
        "101",
        "101",
        "101",
        "101",
        "101",
        "010",
    ],
    "R": [
        "110",
        "101",
        "101",
        "110",
        "110",
        "101",
        "101",
    ],
    "T": [
        "111",
        "010",
        "010",
        "010",
        "010",
        "010",
        "010",
    ],
    "Y": [
        "101",
        "101",
        "010",
        "010",
        "010",
        "010",
        "010",
    ],
}


def nearest_previous_sunday(day: dt.date) -> dt.date:
    # Python weekday: Monday=0, Sunday=6
    days_since_sunday = (day.weekday() + 1) % 7
    return day - dt.timedelta(days=days_since_sunday)


def get_start_sunday(settings: Settings) -> dt.date:
    if settings.start_sunday:
        configured = dt.date.fromisoformat(settings.start_sunday)
        start = nearest_previous_sunday(configured)
    else:
        start = nearest_previous_sunday(dt.date.today())
    return start


def compress_glyph_to_width(glyph: List[str], target_width: int) -> List[str]:
    """Compress a 5-column glyph to target_width (3..5) by removing least-dense columns.

    Keeps column order stable; discourages removing edge columns unless necessary.
    """
    if not glyph:
        return glyph
    current_width = len(glyph[0])
    if target_width >= current_width:
        return glyph
    columns = list(range(current_width))
    # Precompute density per column across rows
    def density(col: int) -> int:
        return sum(1 for r in range(len(glyph)) if glyph[r][col] == '1')

    while len(columns) > target_width:
        # Score columns: lower score => more likely to remove
        scores: List[Tuple[float, int]] = []
        for idx, col in enumerate(columns):
            score = float(density(col))
            # discourage trimming first/last columns
            if idx == 0 or idx == len(columns) - 1:
                score += 0.5
            scores.append((score, idx))
        _, remove_idx = min(scores, key=lambda t: t[0])
        del columns[remove_idx]

    # Rebuild compressed glyph using selected columns in order
    compressed: List[str] = []
    for r in range(len(glyph)):
        row_chars = [glyph[r][c] for c in columns]
        compressed.append(''.join(row_chars))
    return compressed


def stitch_text_to_columns(text: str, spacing: int, target_width: int | None = None) -> List[List[str]]:
    """Return a 2D glyph canvas as list of 7 rows of N columns (strings of '0'/'1').

    We build by concatenating character columns with spacing blank columns of width=spacing.
    """
    rows: List[List[str]] = [[] for _ in range(7)]
    for index, ch in enumerate(text):
        if ch not in FONT_5x7:
            raise ValueError(f"Unsupported character in font: {ch}")
        glyph = FONT_5x7[ch]
        if target_width == 3 and ch in FONT_3x7:
            glyph = FONT_3x7[ch]
        elif target_width is not None and 3 <= target_width < len(glyph[0]):
            glyph = compress_glyph_to_width(glyph, target_width)
        # append 5 columns
        for r in range(7):
            rows[r].extend(list(glyph[r]))
        # add spacing columns except after last char
        if index != len(text) - 1:
            for r in range(7):
                rows[r].extend(list("0" * spacing))
    return rows


def schedule_dates_for_text(text: str, start_sunday: dt.date, spacing: int, target_width: int | None = None) -> Dict[dt.date, Tuple[int, int]]:
    """Compute mapping of date -> (week_column, weekday_row) where a pixel should be on.

    - week_column advances left-to-right over time: each column is one week.
    - weekday_row is 0..6 matching Sunday..Saturday.
    """
    canvas_rows = stitch_text_to_columns(text, spacing, target_width=target_width)
    dates: Dict[dt.date, Tuple[int, int]] = {}
    num_columns = len(canvas_rows[0]) if canvas_rows else 0
    for c in range(num_columns):
        for r in range(7):
            if canvas_rows[r][c] == "1":
                day = start_sunday + dt.timedelta(days=c * 7 + r)
                dates[day] = (c, r)
    return dates


def ensure_file_exists(path: str) -> None:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Contribution writer log. Do not edit manually.\n")


def append_if_missing(path: str, line: str) -> bool:
    ensure_file_exists(path)
    with open(path, "r", encoding="utf-8") as f:
        contents = f.read().splitlines()
    if line in contents:
        return False
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return True


def render_ascii_preview(text: str, start_sunday: dt.date, spacing: int, target_width: int | None = None, max_weeks: int | None = 52) -> str:
    canvas_rows = stitch_text_to_columns(text, spacing, target_width=target_width)
    # rows are 7 tall; columns wide; map '1' to '█' and '0' to '·'
    lines: List[str] = []
    if max_weeks is not None:
        # clamp to max weeks columns
        trimmed_rows = [row[:max_weeks] for row in canvas_rows]
    else:
        trimmed_rows = canvas_rows
    for r in range(7):
        line_chars: List[str] = []
        for ch in trimmed_rows[r]:
            line_chars.append('█' if ch == '1' else '·')
        lines.append(''.join(line_chars))
    header = f"Start Sunday: {start_sunday.isoformat()}  Weeks: {len(trimmed_rows[0]) if trimmed_rows else 0}  Height: 7"
    return header + "\n" + "\n".join(lines)


def run(
    settings: Settings,
    preview: bool = False,
    list_dates: bool = False,
    font_width: int | None = None,
    preview_weeks: int | None = 52,
    mutation_token: str | None = None,
) -> int:
    structlog.configure(processors=[structlog.processors.add_log_level, structlog.processors.TimeStamper(fmt="iso"), structlog.processors.JSONRenderer()])
    start = get_start_sunday(settings)
    today = dt.date.today()
    mapping = schedule_dates_for_text(settings.text, start, settings.spacing_columns, target_width=font_width)
    pixel = mapping.get(today)
    logger.info("schedule_generated", total_pixels=len(mapping), start_sunday=str(start), today=str(today))

    if preview:
        ascii_art = render_ascii_preview(settings.text, start, settings.spacing_columns, target_width=font_width, max_weeks=preview_weeks)
        print(ascii_art)
        if list_dates:
            ordered = sorted(mapping.items(), key=lambda kv: kv[0])
            for day, (col, row) in ordered:
                print(f"{day.isoformat()} col={col} row={row}")
        return 0

    if not pixel:
        logger.info("no_commit_today")
        return 0
    week_col, weekday_row = pixel
    token_suffix = f" token={mutation_token}" if mutation_token else ""
    line = f"{today.isoformat()} {settings.text} col={week_col} row={weekday_row}{token_suffix}"
    changed = append_if_missing(settings.commit_file, line)
    if changed:
        logger.info("commit_needed", file=settings.commit_file, line=line)
    else:
        logger.info("already_recorded", file=settings.commit_file, line=line)
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate file changes on specific dates to draw text on GitHub contributions.")
    parser.add_argument("--text", default=os.getenv("TEXT", None), help="Text to render (defaults to env TEXT or BAREFOOTJOEY)")
    parser.add_argument(
        "--start-sunday",
        dest="start_sunday",
        default=os.getenv("START_SUNDAY", None),
        help="Leftmost Sunday YYYY-MM-DD (defaults to env START_SUNDAY or last Sunday)",
    )
    parser.add_argument("--commit-file", default=os.getenv("COMMIT_FILE", None), help="File to mutate (defaults to env COMMIT_FILE or contrib_log.txt)")
    parser.add_argument("--spacing", type=int, default=os.getenv("SPACING_COLUMNS", None), help="Blank week columns between characters (default 1)")
    parser.add_argument("--preview", action="store_true", help="Show ASCII preview and exit")
    parser.add_argument("--list-dates", action="store_true", help="When previewing, list all scheduled dates")
    parser.add_argument("--font-width", type=int, choices=[3, 4, 5], default=os.getenv("FONT_WIDTH", None), help="Compress glyphs to given width (default 5)")
    parser.add_argument("--preview-weeks", type=int, default=int(os.getenv("PREVIEW_WEEKS", 52)), help="Limit preview to this many week columns (default 52)")
    parser.add_argument("--fit-weeks", type=int, default=os.getenv("FIT_WEEKS", None), help="Auto-compute font width to fit total weeks (uses spacing)")
    parser.add_argument("--mutation-token", default=os.getenv("MUTATION_TOKEN", None), help="Extra unique token to ensure file changes per commit")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    settings = Settings(
        text=args.text or "BAREFOOTJOEY",
        start_sunday=args.start_sunday,
        commit_file=args.commit_file or "contrib_log.txt",
        spacing_columns=int(args.spacing) if args.spacing is not None else 1,
    )
    # Determine font width: explicit beats fit-weeks; else default 5
    font_width: int | None = args.font_width
    if font_width is None and args.fit_weeks:
        n = len(settings.text)
        total_spacing = settings.spacing_columns * max(0, n - 1)
        # available per-char width to fit
        avail = max(1, args.fit_weeks - total_spacing)
        est = avail // max(1, n)
        font_width = min(5, max(3, est))
    return run(
        settings,
        preview=bool(args.preview),
        list_dates=bool(args.list_dates),
        font_width=font_width,
        preview_weeks=int(args.preview_weeks) if args.preview_weeks else None,
        mutation_token=args.mutation_token,
    )


if __name__ == "__main__":
    raise SystemExit(main())


