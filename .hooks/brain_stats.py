#!/usr/bin/env python3
"""Brain attention tracker — per-file stats, done compression, commit orchestration."""

import re
from datetime import date

from brain_common import (
    DONE_KEEP, DONE_LOG, GOALS_DIR, GOALS_FILE, PERIODS,
    git, last_touch_date, replace_block, touch_count,
)
from brain_dashboard import update_goals_md, update_goals_table

# ── Trend heuristic (quantitative, git-only) ───────────────────────────────────

def trend_label(counts):
    month     = counts["month"]
    trimester = counts["trimester"]
    year      = counts["year"]
    four_year = counts["4-year"]

    if four_year == 0:   return "new"
    if year      == 0:   return "dormant"
    if trimester == 0:   return "always-postponed"
    if month     == 0:   return "stalled"

    avg = trimester / 3
    if avg == 0:              return "advancing"
    if month >= avg * 1.5:    return "advancing"
    if month <= avg * 0.5:    return "decelerating"
    return "steady"

# ── Per-file stats block ───────────────────────────────────────────────────────

def build_stats_block(path):
    counts = {name: touch_count(path, days) for name, days in PERIODS}
    lt     = last_touch_date(path)
    trend  = trend_label(counts)

    rows = "\n".join(
        f"| {name:<11} | {counts[name]:>7} |"
        for name, _ in PERIODS
    )

    return (
        "<!-- stats:start -->\n"
        f"last-touch: {lt or '—'}  ·  trend: {trend}\n"
        "\n"
        "| period      | touches |\n"
        "|-------------|----------|\n"
        f"{rows}\n"
        "<!-- stats:end -->"
    )

# ── Done compression ───────────────────────────────────────────────────────────

DONE_RE = re.compile(r'\[x\]', re.IGNORECASE)


def compress_done(content, slug):
    start   = "<!-- done:start -->"
    end     = "<!-- done:end -->"
    pattern = re.compile(re.escape(start) + r"(.*?)" + re.escape(end), re.DOTALL)
    m       = pattern.search(content)
    if not m:
        return content, []

    inner      = m.group(1)
    lines      = inner.split("\n")
    done_lines = [l for l in lines if DONE_RE.search(l)]

    if len(done_lines) <= DONE_KEEP:
        return content, []

    keep    = done_lines[:DONE_KEEP]   # newest first → keep first N
    archive = done_lines[DONE_KEEP:]
    other   = [l for l in lines if not DONE_RE.search(l)]

    new_inner   = "\n".join(other + keep)
    new_content = pattern.sub(lambda _: start + new_inner + end, content)
    return new_content, archive


def append_done_log(slug, archived):
    today = date.today().isoformat()
    DONE_LOG.parent.mkdir(parents=True, exist_ok=True)

    if not DONE_LOG.exists():
        DONE_LOG.write_text(
            "# Done Log\n"
            "> Achievements archived from goal files. Newest last.\n"
            "> Format: date | goal | achievement\n\n---\n\n"
        )

    with open(DONE_LOG, "a") as f:
        for line in archived:
            item = re.sub(r'^>\s*\[x\]\s*', '', line, flags=re.IGNORECASE).strip()
            if item:
                f.write(f"{today} | {slug} | {item}\n")

# ── Commit orchestration ───────────────────────────────────────────────────────

def load_goal_files():
    files = {}
    for f in sorted(GOALS_DIR.glob("*.md")):
        slug = f.stem
        if re.match(r'^[A-Z]+$', slug):
            continue
        files[slug] = f
    return files


def staged_goal_files(goal_files):
    """Goal files the user actually staged this commit — the real-attention set.

    Decorating *every* goal file on every commit made each commit "touch" all
    of them, flattening touch_count to ~total-commits for every goal and
    destroying the attention signal. We only enrich what the user really edited.
    """
    out    = git("diff", "--cached", "--name-only")
    staged = {l.strip() for l in out.splitlines() if l.strip()}
    return {slug: p for slug, p in goal_files.items() if str(p) in staged}


def pre_commit():
    """Decorate only user-staged goal files, then refresh the aggregate dashboard."""
    goal_files = load_goal_files()
    if not goal_files:
        return

    targets  = staged_goal_files(goal_files)
    modified = []

    for slug, path in targets.items():
        original = path.read_text()
        content  = original

        updated = replace_block(content, "<!-- stats:start -->", "<!-- stats:end -->",
                                 build_stats_block(path))
        if updated:
            content = updated

        content, archived = compress_done(content, slug)
        if archived:
            append_done_log(slug, archived)

        if content != original:
            path.write_text(content)
            modified.append(str(path))
            print(f"[Brain] {slug}: updated")

    # Dashboard aggregates live git history for ALL goals — always fresh. GOALS.md
    # churn is not itself a measured signal, so refreshing it every commit is safe.
    update_goals_md(goal_files)
    update_goals_table(goal_files)

    to_stage = modified[:]
    if GOALS_FILE.exists():
        to_stage.append(str(GOALS_FILE))
    if to_stage:
        git("add", *to_stage)

    check_compass_reminder()


def check_compass_reminder():
    compass_log = DONE_LOG.parent / "compass-last.txt"
    if not compass_log.exists():
        print("[Brain] ⚠ compass review never run — try /compass")
        return
    try:
        last = date.fromisoformat(compass_log.read_text().strip())
        days = (date.today() - last).days
        if days >= 30:
            print(f"[Brain] ⚠ no compass review in {days} days — run /compass")
    except Exception:
        pass


def main():
    pre_commit()


if __name__ == "__main__":
    main()
