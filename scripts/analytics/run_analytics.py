#!/usr/bin/env python3
"""
Progress Analytics for sudo-aza workspace.
Generates plots tracking: LOC, todo counts, tasks per run, repo growth.
Outputs PNG files to the specified output directory.
"""

import subprocess
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm

# Font setup for consistent rendering
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Color palette (matching sudodoc theme)
COLORS = {
    'primary': '#1A1A2E',
    'accent': '#3A86FF',
    'accent2': '#FF6B6B',
    'accent3': '#51CF66',
    'accent4': '#FCC419',
    'accent5': '#CC5DE8',
    'gray': '#868E96',
    'light': '#F8F9FA',
    'grid': '#E9ECEF',
}


def git_log_numstat(repo_path):
    """Extract per-commit numstat data: date, commit_hash, added, deleted, files_changed."""
    os.chdir(repo_path)
    result = subprocess.run(
        ['git', 'log', '--all', '--numstat', '--format=%H|%aI'],
        capture_output=True, text=True
    )
    commits = []
    current_hash = None
    current_date = None
    added_total = 0
    deleted_total = 0
    files_count = 0

    for line in result.stdout.splitlines():
        line = line.strip()
        if '|' in line and not line.startswith('-'):
            # This is a commit header line
            if current_hash is not None:
                commits.append({
                    'hash': current_hash,
                    'date': datetime.fromisoformat(current_date),
                    'added': added_total,
                    'deleted': deleted_total,
                    'files': files_count,
                })
            parts = line.split('|')
            current_hash = parts[0]
            current_date = parts[1]
            added_total = 0
            deleted_total = 0
            files_count = 0
        elif line:
            # numstat line: added deleted filename
            parts = line.split('\t')
            if len(parts) >= 2:
                try:
                    a, d = int(parts[0]), int(parts[1])
                    added_total += a
                    deleted_total += d
                    files_count += 1
                except ValueError:
                    # binary file
                    files_count += 1

    # Don't forget last commit
    if current_hash is not None:
        commits.append({
            'hash': current_hash,
            'date': datetime.fromisoformat(current_date),
            'added': added_total,
            'deleted': deleted_total,
            'files': files_count,
        })

    return commits


def git_log_messages(repo_path):
    """Extract commit messages with dates for task tracking."""
    os.chdir(repo_path)
    result = subprocess.run(
        ['git', 'log', '--all', '--format=%aI|%s'],
        capture_output=True, text=True
    )
    entries = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if '|' in line:
            parts = line.split('|', 1)
            date = datetime.fromisoformat(parts[0])
            msg = parts[1]
            entries.append({'date': date, 'message': msg})
    return entries


def parse_todo_history(todo_path):
    """Parse todo.md to get current pending/done counts."""
    with open(todo_path, 'r') as f:
        content = f.read()

    pending = len(re.findall(r'^- \[ \]', content, re.MULTILINE))
    done = len(re.findall(r'^- \[x\]', content, re.MULTILINE))
    return pending, done


def parse_journal_tasks(journals_dir):
    """Parse journal files to extract tasks completed per maintenance run.

    Strategy: count ## level-2 headers within each run section that look like
    task names (contain brackets like [latex-N], [tts-N], or start with a
    capitalized keyword followed by a colon).  Also accept a single
    'What was built' / 'created' / 'Setup' section as evidence of 1 task.
    """
    runs = []
    for filename in sorted(os.listdir(journals_dir)):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(journals_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        # Journals use "# YYYY-MM-DD (HH:00 maintenance run)" format
        # Also handle plain "# YYYY-MM-DD" entries (non-cron runs)
        run_pattern = r'#\s*(\d{4}-\d{2}-\d{2})(?:\s|\().*?(\d{2}:\d{2})'
        # Split on top-level headers that start a new run
        sections = re.split(r'(?=^\s*#\s*\d{4}-\d{2}-\d{2})', content, flags=re.MULTILINE)

        current_run = None
        for section in sections:
            match = re.search(run_pattern, section)
            if match:
                if current_run:
                    runs.append(current_run)
                date_str = match.group(1)
                time_str = match.group(2)
                dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                current_run = {'date': dt, 'title': match.group(0).strip('# ').strip()}

                # Count ## headers that look like task names:
                #  e.g. "## latex-1: Portable LuaLaTeX Installation"
                #  or   "## Setup" (first-run setup section)
                h2_headers = re.findall(r'^##\s+(.+)$', section, re.MULTILINE)

                task_count = 0
                for h in h2_headers:
                    # Anything with a bracket tag like [latex-N]
                    if re.search(r'\[.+\]', h):
                        task_count += 1
                    # Headers with a colon that look like task titles
                    # Accept both "latex-1: ..." and "Setup: ..." patterns
                    elif ':' in h and not h.lower().startswith(('key ', 'notes', 'lessons', 'files', 'what was')):
                        task_count += 1

                # Fallback: if no ## headers matched but there's clear work evidence
                if task_count == 0:
                    has_work = ('What was built' in section
                                or 'created' in section.lower()
                                or 'built' in section.lower())
                    task_count = 1 if has_work else 0

                current_run['tasks_completed'] = task_count

        if current_run:
            runs.append(current_run)

    return runs


def compute_cumulative_loc(commits):
    """Compute cumulative LOC (added - deleted) over time."""
    cumulative = 0
    data = []
    for c in commits:
        cumulative += c['added'] - c['deleted']
        data.append({'date': c['date'], 'loc': cumulative})
    return data


def compute_daily_cumulative_loc(commits):
    """Aggregate commits by date, compute daily cumulative LOC."""
    daily = defaultdict(lambda: {'added': 0, 'deleted': 0})
    for c in commits:
        day = c['date'].date()
        daily[day]['added'] += c['added']
        daily[day]['deleted'] += c['deleted']

    sorted_days = sorted(daily.keys())
    cumulative = 0
    data = []
    for day in sorted_days:
        cumulative += daily[day]['added'] - daily[day]['deleted']
        data.append({'date': datetime.combine(day, datetime.min.time()), 'loc': cumulative})
    return data


def plot_repo_growth(workspace_commits, todolist_commits, output_path):
    """Plot cumulative LOC growth for both repos over time."""
    ws_data = compute_daily_cumulative_loc(workspace_commits)
    tl_data = compute_daily_cumulative_loc(todolist_commits)

    # Combined data for total line
    combined = defaultdict(int)
    for d in ws_data:
        combined[d['date'].date()] += d['loc']
    for d in tl_data:
        combined[d['date'].date()] += d['loc']

    sorted_dates = sorted(combined.keys())
    total_data = [{'date': datetime.combine(d, datetime.min.time()), 'loc': combined[d]} for d in sorted_dates]

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')

    # Workspace repo
    if ws_data:
        dates = [d['date'] for d in ws_data]
        locs = [d['loc'] for d in ws_data]
        ax.plot(dates, locs, color=COLORS['accent'], linewidth=2.5, marker='o',
                markersize=6, label='workspace repo', zorder=3)

    # Todo-list repo
    if tl_data:
        dates = [d['date'] for d in tl_data]
        locs = [d['loc'] for d in tl_data]
        ax.plot(dates, locs, color=COLORS['accent2'], linewidth=2.5, marker='s',
                markersize=6, label='todo-list repo', zorder=3)

    # Total
    if total_data:
        dates = [d['date'] for d in total_data]
        locs = [d['loc'] for d in total_data]
        ax.plot(dates, locs, color=COLORS['primary'], linewidth=3, marker='D',
                markersize=7, label='Total', linestyle='--', zorder=4)
        # Fill under total
        ax.fill_between(dates, locs, alpha=0.08, color=COLORS['primary'])

    ax.set_title('Repository Growth Over Time', fontsize=16, fontweight='bold',
                  color=COLORS['primary'], pad=15)
    ax.set_xlabel('Date', fontsize=12, color=COLORS['gray'])
    ax.set_ylabel('Cumulative Lines of Code', fontsize=12, color=COLORS['gray'])
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='-', color=COLORS['grid'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=30, ha='right')

    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_path}")


def plot_commit_activity(workspace_commits, todolist_commits, output_path):
    """Plot commits per day as a bar chart."""
    daily = defaultdict(int)
    for c in workspace_commits + todolist_commits:
        day = c['date'].date()
        daily[day] += 1

    sorted_days = sorted(daily.keys())
    dates = [datetime.combine(d, datetime.min.time()) for d in sorted_days]
    counts = [daily[d] for d in sorted_days]

    # Color code by repo
    ws_daily = defaultdict(int)
    for c in workspace_commits:
        ws_daily[c['date'].date()] += 1

    colors = [COLORS['accent'] if ws_daily[d] > 0 else COLORS['accent2'] for d in sorted_days]

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')

    bars = ax.bar(dates, counts, color=colors, width=0.6, edgecolor='white', linewidth=1.5, zorder=3)

    # Add count labels on bars
    for bar, count in zip(bars, counts):
        if count > 0:
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.15,
                    str(count), ha='center', va='bottom', fontweight='bold',
                    fontsize=11, color=COLORS['primary'])

    ax.set_title('Commit Activity', fontsize=16, fontweight='bold',
                  color=COLORS['primary'], pad=15)
    ax.set_xlabel('Date', fontsize=12, color=COLORS['gray'])
    ax.set_ylabel('Number of Commits', fontsize=12, color=COLORS['gray'])

    # Custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS['accent'], edgecolor='white', label='workspace'),
        Patch(facecolor=COLORS['accent2'], edgecolor='white', label='todo-list'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)
    ax.grid(True, axis='y', alpha=0.3, linestyle='-', color=COLORS['grid'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=30, ha='right')

    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_path}")


def plot_todo_status(pending, done, output_path):
    """Plot current todo status as a donut chart."""
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('white')

    sizes = [pending, done]
    labels = [f'Pending\n({pending})', f'Done\n({done})']
    colors_list = [COLORS['accent4'], COLORS['accent3']]
    explode = (0.03, 0.03)

    wedges, texts = ax.pie(
        sizes, explode=explode, labels=labels, colors=colors_list,
        startangle=90, pctdistance=0.75,
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=3)
    )

    for text in texts:
        text.set_fontsize(13)
        text.set_fontweight('bold')
        text.set_color(COLORS['primary'])

    # Center text
    total = pending + done
    pct = (done / total * 100) if total > 0 else 0
    ax.text(0, 0.05, f'{pct:.0f}%', ha='center', va='center',
            fontsize=36, fontweight='bold', color=COLORS['primary'])
    ax.text(0, -0.12, 'complete', ha='center', va='center',
            fontsize=12, color=COLORS['gray'])

    ax.set_title('Task Completion Status', fontsize=16, fontweight='bold',
                  color=COLORS['primary'], pad=20)

    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_path}")


def plot_tasks_per_run(runs, output_path):
    """Plot tasks completed per maintenance run as a bar chart."""
    if not runs:
        print("  Skipping tasks_per_run: no journal data")
        return

    dates = [r['date'] for r in runs]
    tasks = [r['tasks_completed'] for r in runs]
    labels = [r['date'].strftime('%b %d\n%H:00') for r in runs]

    # Determine task names from journals for better labels
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor('white')

    bar_colors = []
    for t in tasks:
        if t >= 3:
            bar_colors.append(COLORS['accent3'])
        elif t >= 2:
            bar_colors.append(COLORS['accent'])
        else:
            bar_colors.append(COLORS['accent4'])

    bars = ax.bar(range(len(dates)), tasks, color=bar_colors, width=0.6,
                  edgecolor='white', linewidth=1.5, zorder=3)

    # Count labels
    for bar, count in zip(bars, tasks):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                str(count), ha='center', va='bottom', fontweight='bold',
                fontsize=12, color=COLORS['primary'])

    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_title('Tasks Completed Per Maintenance Run', fontsize=16, fontweight='bold',
                  color=COLORS['primary'], pad=15)
    ax.set_xlabel('Run Date/Time', fontsize=12, color=COLORS['gray'])
    ax.set_ylabel('Tasks Completed', fontsize=12, color=COLORS['gray'])
    ax.grid(True, axis='y', alpha=0.3, linestyle='-', color=COLORS['grid'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Summary stats
    avg = sum(tasks) / len(tasks) if tasks else 0
    total = sum(tasks)
    ax.axhline(y=avg, color=COLORS['accent2'], linestyle='--', linewidth=1.5, alpha=0.7)
    ax.text(len(dates) - 0.5, avg + 0.15, f'avg: {avg:.1f}',
            color=COLORS['accent2'], fontsize=10, fontweight='bold', ha='right')

    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_path}")


def plot_lines_changed(workspace_commits, todolist_commits, output_path):
    """Plot lines added/deleted per day as stacked area chart."""
    daily = defaultdict(lambda: {'added': 0, 'deleted': 0})
    for c in workspace_commits + todolist_commits:
        day = c['date'].date()
        daily[day]['added'] += c['added']
        daily[day]['deleted'] += c['deleted']

    sorted_days = sorted(daily.keys())
    dates = [datetime.combine(d, datetime.min.time()) for d in sorted_days]
    added = [daily[d]['added'] for d in sorted_days]
    deleted = [daily[d]['deleted'] for d in sorted_days]

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')

    ax.fill_between(dates, added, alpha=0.3, color=COLORS['accent3'], label='Lines added')
    ax.fill_between(dates, [-d for d in deleted], alpha=0.3, color=COLORS['accent2'], label='Lines deleted')
    ax.plot(dates, added, color=COLORS['accent3'], linewidth=2, zorder=3)
    ax.plot(dates, [-d for d in deleted], color=COLORS['accent2'], linewidth=2, zorder=3)
    ax.axhline(y=0, color=COLORS['gray'], linewidth=0.8)

    ax.set_title('Lines Added vs Deleted Per Day', fontsize=16, fontweight='bold',
                  color=COLORS['primary'], pad=15)
    ax.set_xlabel('Date', fontsize=12, color=COLORS['gray'])
    ax.set_ylabel('Lines', fontsize=12, color=COLORS['gray'])
    ax.legend(loc='best', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='-', color=COLORS['grid'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=30, ha='right')

    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_path}")


def generate_summary_text(workspace_commits, todolist_commits, pending, done, runs):
    """Generate a text summary of current stats."""
    total_commits = len(workspace_commits) + len(todolist_commits)
    ws_loc = compute_daily_cumulative_loc(workspace_commits)
    tl_loc = compute_daily_cumulative_loc(todolist_commits)

    ws_total = ws_loc[-1]['loc'] if ws_loc else 0
    tl_total = tl_loc[-1]['loc'] if tl_loc else 0

    # Lines added/deleted totals
    total_added = sum(c['added'] for c in workspace_commits + todolist_commits)
    total_deleted = sum(c['deleted'] for c in workspace_commits + todolist_commits)

    summary = f"""# sudo-aza Progress Analytics
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC+8

## Overview
- Total commits: {total_commits} ({len(workspace_commits)} workspace, {len(todolist_commits)} todo-list)
- Total LOC (cumulative net): {ws_total + tl_total} ({ws_total} workspace, {tl_total} todo-list)
- Total lines ever added: {total_added}
- Total lines ever deleted: {total_deleted}

## Task Status
- Pending: {pending}
- Done: {done}
- Completion rate: {done/(pending+done)*100:.1f}%

## Maintenance Runs
- Total runs recorded: {len(runs)}
- Avg tasks per run: {sum(r['tasks_completed'] for r in runs)/len(runs):.1f}
- Total tasks completed across runs: {sum(r['tasks_completed'] for r in runs)}

## Repos
- workspace: {len(workspace_commits)} commits across {len(set(c['date'].date() for c in workspace_commits))} active days
- todo-list: {len(todolist_commits)} commits across {len(set(c['date'].date() for c in todolist_commits))} active days
"""
    return summary


def main():
    workspace_path = os.path.expanduser('/home/z/repos/workspace')
    todo_path = os.path.expanduser('/home/z/repos/todo-list/todo.md')
    journals_dir = os.path.join(workspace_path, 'journals')
    output_dir = os.path.join(workspace_path, 'scripts', 'analytics', 'output')
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 50)
    print("sudo-aza Progress Analytics")
    print("=" * 50)

    # Collect data
    print("\n[1/6] Collecting git data from workspace repo...")
    ws_commits = git_log_numstat(workspace_path)
    print(f"  Found {len(ws_commits)} commits")

    print("[2/6] Collecting git data from todo-list repo...")
    tl_commits = git_log_numstat(os.path.dirname(todo_path))
    print(f"  Found {len(tl_commits)} commits")

    print("[3/6] Parsing todo status...")
    pending, done = parse_todo_history(todo_path)
    print(f"  Pending: {pending}, Done: {done}")

    print("[4/6] Parsing journal entries...")
    runs = parse_journal_tasks(journals_dir)
    print(f"  Found {len(runs)} maintenance runs")

    # Generate plots
    print("\n[5/6] Generating plots...")

    plot_repo_growth(ws_commits, tl_commits,
                     os.path.join(output_dir, 'repo-growth.png'))

    plot_commit_activity(ws_commits, tl_commits,
                         os.path.join(output_dir, 'commit-activity.png'))

    plot_todo_status(pending, done,
                     os.path.join(output_dir, 'todo-status.png'))

    plot_tasks_per_run(runs,
                       os.path.join(output_dir, 'tasks-per-run.png'))

    plot_lines_changed(ws_commits, tl_commits,
                       os.path.join(output_dir, 'lines-changed.png'))

    # Generate summary
    print("[6/6] Generating summary...")
    summary = generate_summary_text(ws_commits, tl_commits, pending, done, runs)
    summary_path = os.path.join(output_dir, 'summary.txt')
    with open(summary_path, 'w') as f:
        f.write(summary)
    print(f"  Saved: {summary_path}")

    print("\n" + "=" * 50)
    print("Analytics complete!")
    print(f"Output directory: {output_dir}")
    print("=" * 50)


if __name__ == '__main__':
    main()
