#!/usr/bin/env python3
"""Brain attention tracker — per-file stats, done compression, GOALS.md dashboard."""

import re
import subprocess
from datetime import date, datetime
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────

BRAIN      = Path("brain")
GOALS_FILE = BRAIN / "GOALS.md"
DONE_LOG   = BRAIN / ".log" / "done.md"
GOALS_DIR  = BRAIN / "goals"

PERIODS = [
    ("month",     30),
    ("trimester", 90),
    ("semester",  180),
    ("year",      365),
    ("2-year",    730),
    ("4-year",    1460),
]

DONE_KEEP = 3

# ── Git helpers ────────────────────────────────────────────────────────────────

def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def touch_count(path, days):
    out = git("log", "--oneline", f"--since={days} days ago", "--", str(path))
    return len([l for l in out.splitlines() if l.strip()])


def last_touch_date(path):
    out = git("log", "-1", "--format=%ci", "--", str(path))
    return out[:10] if out else None

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

# ── Stats block ────────────────────────────────────────────────────────────────

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

# ── Block replacement ──────────────────────────────────────────────────────────

def replace_block(content, start, end, new_block):
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(content):
        return None
    return pattern.sub(lambda _: new_block, content)

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

# ── GOALS.md dashboard ─────────────────────────────────────────────────────────

def bar(count, max_val, width=10):
    if max_val == 0:
        max_val = 1
    filled = count * width // max_val
    return "█" * filled + "░" * (width - filled)


def area_from_file(path):
    with open(path) as f:
        for line in f:
            m = re.match(r'^# \[ *(\w+) ', line)
            if m:
                return m.group(1).lower()
    return None


def timing_display(text):
    """Shorten long timing strings to a date-like fragment for table display."""
    if not text or text == "—":
        return "—"
    if len(text) <= 18:
        return text
    m = re.search(
        r'(mid-|before\s+|after\s+|early\s+|late\s+)?'
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d*',
        text, re.IGNORECASE
    )
    if m:
        return m.group(0).strip()
    m = re.search(r'\d+\s+\w+', text)
    if m:
        return m.group(0)
    return text[:18] + "…"


def parse_goal_file(path):
    content = path.read_text()
    lines   = content.splitlines()
    result  = {}

    for line in lines:
        # Header may be 2-field [ area | horizon ] or 3-field [ area | subarea | horizon ]
        m = re.match(r'^# \[ *(\w+)(?: *\| *\w+)* *\| *(\w+) *\] *(.+)', line)
        if m:
            result['area']    = m.group(1).lower()
            result['horizon'] = m.group(2).lower()
            result['title']   = m.group(3).strip()
            break
    if 'title' not in result:
        return None

    # Timing block: anchor first, target as fallback
    timing_block = []
    in_timing = False
    for line in lines:
        if '>**timing**' in line:
            in_timing = True
            continue
        if in_timing:
            if re.match(r'^>?\*\*\w', line) or re.match(r'^##', line):
                break
            timing_block.append(line)

    timing_str = "\n".join(timing_block)
    t_display  = "—"
    am = re.search(r'anchor\s*·\s*([^\n*\\]+)', timing_str)
    tm = re.search(r'target\s*·\s*([^\n*\\]+)', timing_str)
    if am:
        val = am.group(1).strip()
        if val and val != "—":
            t_display = timing_display(val)
    if t_display == "—" and tm:
        val = tm.group(1).strip()
        if val and val != "—":
            t_display = timing_display(val)
    result['timing'] = t_display

    # Selected next achievement: first content line after the heading
    selected = "—"
    in_sel = False
    for line in lines:
        if re.match(r'^## selected next achievement', line, re.IGNORECASE):
            in_sel = True
            continue
        if in_sel:
            s = line.strip()
            if s and not s.startswith('**ease') and not s.startswith('<!--'):
                selected = s[:55] + ("…" if len(s) > 55 else "")
                break

    result['selected'] = selected
    result['file']     = path.name
    return result


def update_goals_table(goal_files):
    if not GOALS_FILE.exists():
        return

    rows = []
    for slug, path in sorted(goal_files.items()):
        g = parse_goal_file(path)
        if not g:
            continue
        rows.append(
            f"| {g['title']} | {g['area']} | {g['horizon']} | {g['timing']} "
            f"| {g['selected']} | [→](goals/{g['file']}) |"
        )

    new_table = (
        "<!-- goals:start -->\n"
        "## active goals\n\n"
        "| goal | area | horizon | timing | selected achievement | file |\n"
        "|------|------|---------|--------|---------------------|------|\n"
        + "\n".join(rows) + "\n"
        "<!-- goals:end -->"
    )

    content = GOALS_FILE.read_text()
    result  = replace_block(content, "<!-- goals:start -->", "<!-- goals:end -->", new_table)
    if result and result != content:
        GOALS_FILE.write_text(result)
        print("[Brain] GOALS.md active goals updated")


def update_goals_md(goal_files):
    if not GOALS_FILE.exists():
        return

    area_touches = {a: 0 for a in ["health", "career", "finances", "fun", "spiritual"]}
    goal_touches = {}

    for slug, path in goal_files.items():
        c    = touch_count(path, 14)
        goal_touches[slug] = c
        area = area_from_file(path)
        if area and area in area_touches:
            area_touches[area] += c

    area_max = max(area_touches.values()) or 1
    goal_max = max(goal_touches.values()) or 1
    now      = datetime.now().strftime("%Y-%m-%d %H:%M")

    area_lines = "".join(
        f"{a:<12} {bar(area_touches[a], area_max)}   {area_touches[a]} touches\n"
        for a in ["health", "career", "finances", "fun", "spiritual"]
    )
    goal_lines = "".join(
        f"{slug:<24} {bar(goal_touches[slug], goal_max)}   {goal_touches[slug]} touches\n"
        for slug in sorted(goal_touches)
    )

    # Hook only replaces the data block — pareto/gap sections are preserved between commits
    new_data = (
        "<!-- data:start -->\n"
        f"## attention dashboard  _(auto-updated on every commit)_\n"
        f"last-updated: {now}\n\n"
        f">**areas** — last 14 days  \n"
        f"```\n{area_lines}```\n\n"
        f">**goals** — last 14 days  \n"
        f"```\n{goal_lines}```\n"
        "<!-- data:end -->"
    )

    content = GOALS_FILE.read_text()

    # Prefer data markers (preserves agent-written pareto/gap sections)
    result = replace_block(content, "<!-- data:start -->", "<!-- data:end -->", new_data)

    if result is None:
        # Bootstrap: first run — build full stats block including agent section placeholders
        full_block = (
            "<!-- stats:start -->\n"
            + new_data + "\n\n"
            ">**pareto**  \n"
            "*— (run compass review)*\n\n"
            ">**gap**  \n"
            "*— (run compass review)*\n"
            "<!-- stats:end -->"
        )
        result = replace_block(content, "<!-- stats:start -->", "<!-- stats:end -->", full_block)

    if result and result != content:
        GOALS_FILE.write_text(result)
        print("[Brain] GOALS.md updated")

# ── Main ───────────────────────────────────────────────────────────────────────

def load_goal_files():
    files = {}
    for f in sorted(GOALS_DIR.glob("*.md")):
        slug = f.stem
        if re.match(r'^[A-Z]+$', slug):
            continue
        files[slug] = f
    return files


def pre_commit():
    """Run before commit: update stats/goals, stage modified files."""
    goal_files = load_goal_files()
    if not goal_files:
        return
    modified   = []

    for slug, path in goal_files.items():
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

    update_goals_md(goal_files)
    update_goals_table(goal_files)

    goals_files_changed = [str(p) for p in [GOALS_FILE] + list(GOALS_DIR.glob("*.md"))
                           if p.exists()]
    subprocess.run(["git", "add"] + goals_files_changed, capture_output=True)

    check_compass_reminder()


def main():
    pre_commit()


def check_compass_reminder():
    compass_log = BRAIN / ".log" / "compass-last.txt"
    if not compass_log.exists():
        print("[Brain] ⚠ compass review never run — try /compass")
        return
    try:
        from datetime import timedelta
        last    = date.fromisoformat(compass_log.read_text().strip())
        days    = (date.today() - last).days
        if days >= 30:
            print(f"[Brain] ⚠ no compass review in {days} days — run /compass")
    except Exception:
        pass


if __name__ == "__main__":
    main()
