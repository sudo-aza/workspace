# Operating Principles

## Permissions (granted by zoe, 2026-05-12)

- **Full proactive autonomy**: zoe has given explicit permission to be as proactive as needed — no need to ask for permission to act.
- **Self-modification**: allowed to edit the cron job, heartbeat prompt, and own rules as needed.
- **Frequency adjustment**: if backlog warrants it, increase cron frequency beyond the original 6-hour interval.
- **Rule editing**: allowed to change operating procedures, but should remember *why* some rules exist before changing them.

## Design Decisions (why things are the way they are)

### One task per run (relaxed)
Originally: do exactly one task per cron run, no matter what.
Why it existed: prevents runaway sessions that time out or burn resources.
Current: allow up to 2 tasks per run, especially for quick tasks (research, notes, small scripts). If a task is genuinely big (install + build + verify), stick to one.

### TeXLive reinstall every run
Why: the VM resets between runs, wiping /home/z/.texlive/.
Mitigation: the install script is idempotent and fast (scheme-basic is ~100MB). Keep it this way.

### .gitignore keeps workspace clean
Why: the workspace repo should contain *scripts and configs*, not binary installations or build artifacts. TeXLive, __pycache__, .aux files, etc. are all excluded.

### LaTeX results as PNGs to Discord
Why: PDFs can't be previewed inline in Discord, but PNGs can. Use `pdftoppm` at 200-300 DPI for good quality.

### Send summary after each run
Why: zoe wants visibility into what the agent is doing without having to check manually.

### Journal entries
Why: persistence across VM resets. Journals are in the git repo, so they survive. Future cron runs can read past journals to learn from mistakes.

### Cron prompt includes GitHub credentials
Why: each run might need to push to repos, create new repos, or clone. Having credentials in the prompt ensures the agent always has them.

## Hardware Constraints
- 4 vCPU, 8GB RAM, no GPU
- VM may reset between runs (ephemeral filesystem)
- Keep all persistent data in git repos

## Cron Job
- Job ID: 143475
- Name: workspace-maintenance
- Channel: discord (#zai-gh)
- Current frequency: every 3 hours (0, 3, 6, 9, 12, 15, 18, 21 Berlin time)
