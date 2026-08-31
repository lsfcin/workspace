# wos
> What the workspace declares about itself, and what the session-close ritual really does.

Two responsibilities, after the instruments moved to [`session/`](session/CONTEXT.md) in 2026-08-17's
fanout split.

**Declaration** — three files that must agree, checked against each other and never trusted.
[`test_deps.py`](test_deps.py) on `core/tools/deps.txt`, and the feature registry split in two:
[`test_features.py`](test_features.py) asks whether the declaration is complete and inside its closed
sets, [`test_features_wiring.py`](test_features_wiring.py) asks whether a row claiming a switch has
one. Data and behaviour are different questions with different failure modes — a row can be
perfectly well-formed and still name a file that never reads the law, which is the failure that cost
the first ablation run its entire signal ([`core/SPECS.md`](../../../SPECS.md) § AD-14).

**The ritual** moved into [`close/`](close/CONTEXT.md) 2026-08-25, at the fanout signal: what a
session close does is a different question from what the workspace declares about itself, and
[`core/SPECS.md`](../../../SPECS.md) § AD-09 governs it alone.

Zero-token, no network. Each test builds its own repo and bare origin; nothing touches the real
workspace.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`close/`](close/CONTEXT.md) | Coverage for the session-close ritual: what the script really does, and what the skills claim. |
| [`diagram/`](diagram/CONTEXT.md) | Coverage for the workspace picture, split the way its source is: what it draws, and what it claims. |
| [`session/`](session/CONTEXT.md) | The instruments: what a session costs, what fills its window, and what a read was served. |

| File | Interface | Description |
|------|-----------|-------------|
| [`test_b6_google_skills.py`](test_b6_google_skills.py) | [`test_b6_google_skills.pyi`](test_b6_google_skills.pyi) | B6 regression — every Google-backed tool family has a skill wrapper. Half the families carried a core/skills/<name>.md and half did not, on no stated rule; the question re-litigated itself every time a family landed. Ruled 2026-08-31 (Lucas): add where missing, never half — the rule is a sentence in core/tools/SPECS.md § Adding a tool, and this spec is the sentence made checkable. Scope is the Google families the ruling names; a family outside the set is a SPECS change first, not a silent pass here. |
| [`test_deps.py`](test_deps.py) | [`test_deps.pyi`](test_deps.pyi) | T0 declared dependencies (core/tools/SPECS.md § Declared dependencies): a third-party import the tool surface uses must be declared, and every tool must run under the workspace venv. |
| [`test_features.py`](test_features.py) | [`test_features.pyi`](test_features.pyi) | T0 the feature registry's declaration half (core/SPECS.md § AD-14): every feature is declared, answered, and inside the closed sets its columns may draw from. |
| [`test_features_wiring.py`](test_features_wiring.py) | [`test_features_wiring.pyi`](test_features_wiring.pyi) | T0 the feature registry's honesty half (core/SPECS.md § AD-14): a row claiming a switch must really have one, and throwing the switch must move the observable. |
| [`test_flow_loops.py`](test_flow_loops.py) | [`test_flow_loops.pyi`](test_flow_loops.pyi) | T0 the flow layer's loop bound (core/flows/CONTEXT.md § Rules that hold for every flow): a step that declares a loop must declare its numeric cap. Zero-token, no network. |
| [`test_norms.py`](test_norms.py) | [`test_norms.pyi`](test_norms.pyi) | T0 the norms layer (core/SCHEMA-layers.md § Layer: norm): the always-loaded rule block is generated, and generating it is what makes a rule switchable. |
| [`test_permissions.py`](test_permissions.py) | [`test_permissions.pyi`](test_permissions.pyi) | T0/T1 the permission registry and its renderer: every level is fully declared, and the rendered config is a function of the declaration rather than of whatever the last session clicked. |
<!-- routing:end -->
