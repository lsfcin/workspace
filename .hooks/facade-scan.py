#!/usr/bin/env python3
# Pre-Write hook: list existing facade exports before creating a new file in the same module.
import json, os, re, sys
from pathlib import Path

WORKSPACE = Path('/mnt/workspace')
FACADE_FOR = {
    '.ts': 'index.ts', '.tsx': 'index.tsx',
    '.js': 'index.js', '.jsx': 'index.jsx',
    '.py': '__init__.py',
    '.dart': 'index.dart',
}

data = json.load(sys.stdin)
if os.environ.get('CLAUDE_TOOL_NAME', '') != 'Write':
    sys.exit(0)

file_path = Path(data.get('file_path', ''))

# Only new files under Code/
if file_path.exists() or 'Code' not in file_path.parts:
    sys.exit(0)

facade_name = FACADE_FOR.get(file_path.suffix)
if not facade_name:
    sys.exit(0)

facade = file_path.parent / facade_name
# Skip if facade doesn't exist or we're writing the facade itself
if not facade.exists() or facade.resolve() == file_path.resolve():
    sys.exit(0)

content = facade.read_text(encoding='utf-8', errors='ignore')
exports = []

if file_path.suffix == '.py':
    m = re.search(r'__all__\s*=\s*\[([^\]]+)\]', content, re.DOTALL)
    if m:
        exports = re.findall(r'["\'](\w+)["\']', m.group(1))
    else:
        for line in content.splitlines():
            m2 = re.match(r'^from\s+\S+\s+import\s+(.+)', line)
            if m2:
                exports += [x.strip().split(' as ')[-1].strip() for x in m2.group(1).split(',')]
else:
    for block in re.findall(r'export\s+\{([^}]+)\}', content, re.DOTALL):
        for item in block.split(','):
            name = item.strip().split(' as ')[-1].strip().rstrip(';').strip()
            if name and re.match(r'^\w+$', name):
                exports.append(name)
    named = re.findall(
        r'export\s+(?:default\s+)?(?:type\s+)?(?:const|function|class|interface|enum)\s+(\w+)',
        content,
    )
    exports += named

exports = sorted(set(e for e in exports if e and re.match(r'^\w+$', e)))

try:
    rel = facade.relative_to(WORKSPACE)
except ValueError:
    rel = facade

if exports:
    print(f"📦 {rel} exports: {', '.join(exports)}")
    print(f"   Verify new file adds functionality not already covered above.")
else:
    print(f"📦 {rel} exists but exports nothing yet — ensure new file gets re-exported there.")

sys.exit(0)
