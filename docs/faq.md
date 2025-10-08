## FAQ & Troubleshooting

### Nothing happened today — why no commit?

The tool only records on dates that contain a "pixel" for your text. Use `--preview --list-dates` to verify the plan, adjust `--start-sunday`, or shorten width via `--fit-weeks`.

### How do I fit within exactly 52 weeks?

Use `--fit-weeks 52` (and adjust `--spacing` if needed). For tighter fit, try `--font-width 3` or `--font-width 3 --font-height 5`.

### Do lowercase letters work?

Input is normalized to uppercase; fonts support A–Z.

### I see repeated lines aren’t added — is that expected?

Yes. The tool avoids duplicate lines in the commit file; use `--mutation-token` to ensure unique content for multiple commits on the same day.

### Can I preview without changing files?

Yes, use `--preview`. Add `--preview-weeks` and `--list-dates` for more context.

### How do I change which file is mutated?

Pass `--commit-file PATH` or set `COMMIT_FILE`. Ensure the path is tracked by Git.

