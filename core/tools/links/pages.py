# pages.py — a course page and its artefacts mirrored into the publish repo and pushed, in one call, for links/cfpages
#
# A course page lives at academy/teaching/classes/<course>/<file>.md and is served from
# outputs/links/<course>/<file>.md. The mapping is the directory name, so there is no table to keep.
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
CLASSES = ROOT / 'academy' / 'teaching' / 'classes'

# A page may carry a block that a generator draws; the generator runs before the copy, so a stale
# drawing never reaches the site. Keyed on the marker the page itself holds: declaring a block IS
# asking for its generator.
GENERATORS = {'<!-- painel:dados-': ROOT / 'academy' / 'teaching' / 'structure' / 'painel.py'}

# Internal files that sit beside the artefacts and must never reach a public repo.
PRIVATE = {'CONTEXT.md'}


class Refused(Exception):
    pass


def mirror_of(page: pathlib.Path, publish: pathlib.Path, classes: pathlib.Path = CLASSES) -> pathlib.Path:
    """classes/<course>/<file> -> publish/<course>/<file>; anything else has no public place."""
    page = page.resolve()
    try:
        course, name = page.relative_to(classes.resolve()).parts
    except ValueError:
        raise Refused(f"{page} is not a course page — publish takes {classes}/<course>/<file>.md")
    return publish / course / name


def redraw(page: pathlib.Path) -> list[str]:
    """Run every generator the page declares; return the ones that ran."""
    text = page.read_text(encoding='utf-8')
    ran = []
    for marker, script in GENERATORS.items():
        if marker in text:
            subprocess.run([sys.executable, str(script), str(page)], check=True)
            ran.append(script.name)
    return ran


def mirror(page: pathlib.Path, publish: pathlib.Path, classes: pathlib.Path = CLASSES) -> list[pathlib.Path]:
    """Copy the page, and its artefatos/ when it has one, into the publish repo; return the targets."""
    target = mirror_of(page, publish, classes)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(page, target)
    copied = [target]
    artefacts = page.parent / 'artefatos'
    if artefacts.is_dir():
        (target.parent / 'artefatos').mkdir(exist_ok=True)
        for f in sorted(artefacts.glob('*.md')):
            if f.name not in PRIVATE:
                copied.append(pathlib.Path(shutil.copy2(f, target.parent / 'artefatos' / f.name)))
    return copied


def push(publish: pathlib.Path, paths: list, message: str) -> None:
    """git add exactly these paths, commit when something is staged, push.

    `add` by path and never `commit -am`: -a skips a file the repo has never seen, which is every
    new artefact. Nothing staged means nothing to COMMIT, never nothing to push — a commit left by a
    run that failed at the push is exactly when the site is still stale.
    """
    subprocess.run(['git', 'add', '--', *map(str, paths)], cwd=publish, check=True)
    if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=publish).returncode:
        subprocess.run(['git', 'commit', '-q', '-m', message], cwd=publish, check=True)
    # -u origin HEAD: the same call works on the first push, when there is no upstream yet.
    subprocess.run(['git', 'push', '-q', '-u', 'origin', 'HEAD'], cwd=publish, check=True)
