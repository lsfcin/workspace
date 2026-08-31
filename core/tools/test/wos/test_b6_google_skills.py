# B6 regression — every Google-backed tool family has a skill wrapper.
# Half the families carried a core/skills/<name>.md and half did not, on no stated rule; the
# question re-litigated itself every time a family landed. Ruled 2026-08-31 (Lucas): add where
# missing, never half — the rule is a sentence in core/tools/SPECS.md § Adding a tool, and this
# spec is the sentence made checkable. Scope is the Google families the ruling names; a family
# outside the set is a SPECS change first, not a silent pass here.
from conftest import WORKSPACE_ROOT

FAMILIES = {
    'mail': 'gmail',
    'calendar': 'calendar',
    'files': 'drive',
    'slides': 'gslides',
    'forms': 'gforms',
    'docs': 'gdocs',
}


def test_every_google_family_has_a_skill():
    missing = [f'{family}/{provider}' for family, provider in FAMILIES.items()
               if not (WORKSPACE_ROOT / 'core/skills' / f'{provider}.md').exists()]
    assert not missing, f'families without a skill wrapper: {missing}'


def test_the_rule_is_stated_where_the_next_family_reads_it():
    specs = (WORKSPACE_ROOT / 'core/tools/SPECS.md').read_text(encoding='utf-8')
    assert 'Every Google-backed family gets a skill wrapper' in specs
