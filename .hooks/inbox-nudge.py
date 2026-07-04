#!/usr/bin/env python3
# SessionStart — warn Lucas + agent when brain/INBOX.md has piled up past a threshold,
# so capture doesn't silently grow and scatter. Paired with the /roundup session-end drain.
import os
import re
import sys
import time

INBOX = '/mnt/workspace/brain/INBOX.md'
WARN_AT = 15
LOUD_AT = 25
STALE_DAYS = 10


def read_body(text):
    marker = '<!-- add entries below'
    idx = text.find(marker)
    if idx == -1:
        return text
    nl = text.find('\n', idx)
    body = text[nl + 1:] if nl != -1 else ''
    return body


def count_entries(body):
    blocks = re.split(r'\n\s*\n', body)
    entries = []
    for block in blocks:
        stripped = block.strip()
        is_empty = not stripped
        is_comment = stripped.startswith('<!--')
        is_rule = stripped == '---'
        skip = is_empty or is_comment or is_rule
        if not skip:
            entries.append(stripped)
    return len(entries)


def main():
    exists = os.path.exists(INBOX)
    if not exists:
        return 0
    with open(INBOX, encoding='utf-8') as f:
        text = f.read()
    body = read_body(text)
    n = count_entries(body)
    if n < WARN_AT:
        return 0
    age_days = (time.time() - os.path.getmtime(INBOX)) / 86400
    level = 'LOUD' if n >= LOUD_AT else 'warn'
    lines = []
    lines.append(f'INBOX-NUDGE [{level}]: brain/INBOX.md holds {n} untriaged entries '
                 f'(threshold {WARN_AT}; last touched {age_days:.0f}d ago).')
    lines.append('Tell Lucas at the start of your reply and offer to run /brain-inbox, '
                 'or fold a drain into /roundup at session end.')
    sys.stdout.write('\n'.join(lines) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
