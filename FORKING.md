<!--

// ██████████████████████████████████████████████████████████████████████
// █▄─▄─▀██▀▄─██▄─▄▄▀█▄─▄▄─█▄─▄▄─█─▄▄─█─▄▄─█─▄─▄─███▄─▄█─▄▄─█▄─▄▄─█▄─█─▄█
// ██─▄─▀██─▀─███─▄─▄██─▄█▀██─▄███─██─█─██─███─███─▄█─██─██─██─▄█▀██▄─▄██
// █▄▄▄▄██▄▄█▄▄█▄▄█▄▄█▄▄▄▄▄█▄▄▄███▄▄▄▄█▄▄▄▄██▄▄▄██▄▄▄███▄▄▄▄█▄▄▄▄▄██▄▄▄██
// ██████████████████████████████████████████████████████ FORKING.md ████

 © BarefootJoey  -->

### 🚀 Use this as your GitHub Profile

You can use this repository as a template for your own profile README. When a repository has the same name as your GitHub username, its `README.md` appears on your GitHub profile page.

#### ⚡ Quick start
1. Fork this repository to your account (Go back to the [project root](https://github.com/BarefootJoey/BarefootJoey/tree/main) and click Fork at the top right).
2. Rename your fork so the repository name is exactly your GitHub username as found in the address of your GitHub profile (e.g., `yourname/yourname`).
3. Make the repository Public: Settings → General → Change visibility → Public.
4. Enable Actions: open the Actions tab and, if prompted, click “I understand my workflows, go ahead and enable them”.
5. Set workflow permissions: Settings → Actions → General → Workflow permissions → select “Read and write permissions”.
6. Add repository secrets for commit identity: Settings → Secrets and variables → Actions → New repository secret, then add:
   - `GIT_AUTHOR_NAME` → your display name (e.g., `Jane Doe`)
   - `GIT_AUTHOR_EMAIL` → a verified email on your GitHub account, or your GitHub noreply email (`USERNAME@users.noreply.github.com`). Using an email not linked to your account may prevent contributions from appearing on your graph.
7. Run the workflow once manually to verify: Actions → “Contribution Writer” → “Run workflow”. Confirm it commits to `main`.

#### 📝 Update your README content
Open `README.md` and replace any references to `BarefootJoey` with your info. Common places to update:
- View counter badge (`komarev.com/...username=YOUR_USERNAME`)
- Stars/Forks/Issues badges for your repo slug (`YOUR_USERNAME/YOUR_USERNAME`)
- Contributors image (`contrib.rocks/image?repo=YOUR_USERNAME/YOUR_USERNAME`)
- Trophy, Streak, and Stats images (`...username=YOUR_USERNAME` in their URLs)
- Social links (Website, Telegram, Twitter/X, Kaggle, TradingView, etc.)
- Cash App, Wakatime, or other external badges

Tip: Use your editor’s Find/Replace for `BarefootJoey` → `YOUR_USERNAME` and double-check URLs that contain the repo slug.

#### 🎛️ Customize the contribution automation
This repo includes a workflow at `.github/workflows/contrib-writer.yml` that can create stylized commits to render text on your GitHub contribution graph.

Edit the following environment values in that workflow to personalize behavior:
- `TEXT`: The text to render across your graph (e.g., `YOURNAME`).
- `START_SUNDAY`: A recent Sunday to align the rendering (format `YYYY-MM-DD`).
- `COMMIT_FILE`: File to append for commits (default: `contrib_writer/contrib_log.txt`).
- `SPACING_COLUMNS` and `FONT_WIDTH`: Tweak spacing/letter width.
- `FIT_WEEKS`: How many weeks to fit on the graph (e.g., `52`).
- `MULTI_COMMITS`: Number of small commits on “pixel” days for intensity.
- `schedule.cron`: When to run automatically (uses UTC). Adjust as needed, or remove the schedule block to disable automatic runs.

Permissions and identity:
- Ensure repository “Workflow permissions” are set to “Read and write permissions”.
- The workflow uses `GIT_AUTHOR_NAME` and `GIT_AUTHOR_EMAIL` to attribute commits. The email must be associated with your GitHub account (or use your noreply email) for commits to count toward your graph.

#### 🧪 Optional: Test locally
If you want to run the contribution writer locally:
1. Install Python 3.11.
2. Create a virtual environment (optional, but recommended) and install dependencies from [requirements.txt](contrib_writer/requirements.txt):
   - `python -m venv venv` → activate it
   - `pip install structlog pydantic`
3. Run: `python contrib_writer/contrib_writer.py`
   - The workflow sometimes runs the script multiple times with a `--mutation-token` to intensify commits; you generally don’t need this locally.

#### 🛠️ Troubleshooting
- No commits from workflow:
  - Check Actions tab for errors.
  - Confirm “Workflow permissions” are set to Read and write.
  - Ensure you added both `GIT_AUTHOR_NAME` and `GIT_AUTHOR_EMAIL` secrets.
  - Verify the email is verified on your GitHub account or use your noreply email.
- Commits don’t appear on your contribution graph:
  - Contributions count only if authored by your account email and pushed to the default branch (`main`).
  - Private repos don’t show contributions unless you enable “Include private contributions” in your GitHub profile settings.
  - Cron runs in UTC; visualize timing accordingly.
- Want to stop automation: disable the workflow in Actions, remove the `schedule` block, or delete `.github/workflows/contrib-writer.yml`.

That’s it! After these steps, your fork named `YOUR_USERNAME` will power your profile README, and the optional automation can draw text on your contribution graph.
