# T1 write approval: no write token loads unless Lucas approved, in a later turn, the exact plan it carries out.
import json

import pytest

import gauth
import sheets_core
import write_approval as wa


@pytest.fixture
def plan_state(tmp_path, monkeypatch):
    """A clean process: own state dir, a session whose turn is '1', and no CODE on the command line."""
    monkeypatch.setenv("WOS_SESSION_STATE", str(tmp_path))
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "s1")
    (tmp_path / "turn_s1").write_text("1", encoding="utf-8", newline="\n")
    for name, value in (("_code", ""), ("_gated", False), ("_approved", ""), ("_consumed", False)):
        monkeypatch.setattr(wa, name, value)
    return tmp_path


def plan(state, capsys):
    """Step 1: run the gate without CODE and return the CODE it printed."""
    with pytest.raises(SystemExit) as stop:
        wa.gate("sheets set", "id A1", [["x"]], ["Notas!A1: '' → 'x'"], revision=[])
    assert stop.value.code == wa.AWAITING
    assert "AWAITING LUCAS" in capsys.readouterr().out
    return json.loads((state / "pending_write.json").read_text(encoding="utf-8"))["code"]


def approve(state, monkeypatch, code, turn="2"):
    (state / "turn_s1").write_text(turn, encoding="utf-8", newline="\n")
    monkeypatch.setattr(wa, "_code", code)


@pytest.mark.parametrize("argv", [["x", "--approve", "abc123", "y"], ["x", "--approve=abc123", "y"]])
def test_the_code_leaves_argv_before_any_parser_sees_it(argv):
    assert wa.take_code(argv) == "abc123" and argv == ["x", "y"]


def test_a_plan_approved_in_a_later_turn_unlocks_one_process_and_is_spent(plan_state, monkeypatch, capsys):
    approve(plan_state, monkeypatch, plan(plan_state, capsys))
    wa.gate("sheets set", "id A1", [["x"]], [], revision=[])
    wa.consume("sheets")
    wa.consume("sheets")  # a second write in the same process reuses the approval
    assert not (plan_state / "pending_write.json").exists()


@pytest.mark.parametrize("why,change", [
    ("same turn", lambda s, m, c: approve(s, m, c, turn="1")),
    ("wrong code", lambda s, m, c: approve(s, m, "000000")),
    ("expired", lambda s, m, c: (approve(s, m, c), m.setattr(wa, "TTL_S", -1))),
])
def test_an_approval_lucas_did_not_give_is_refused(plan_state, monkeypatch, capsys, why, change):
    change(plan_state, monkeypatch, plan(plan_state, capsys))
    with pytest.raises(SystemExit, match="REFUSED"):
        wa.gate("sheets set", "id A1", [["x"]], [], revision=[])
    assert not wa._approved, why


def test_a_document_that_moved_since_the_plan_is_refused(plan_state, monkeypatch, capsys):
    approve(plan_state, monkeypatch, plan(plan_state, capsys))
    with pytest.raises(SystemExit, match="changed since"):
        wa.gate("sheets set", "id A1", [["x"]], [], revision=[["someone typed here"]])


@pytest.mark.parametrize("grant", sorted(g for g, row in gauth.grants().items() if row[1]))
def test_a_write_token_without_a_gate_is_refused_before_it_loads(plan_state, grant):
    """Every write grant grants.txt declares, a new one included: no allowlist to forget to grow."""
    with pytest.raises(PermissionError, match="write_approval.gate"):
        gauth.auth("personal", grant, write=True)


def test_consenting_to_a_write_token_needs_no_plan(plan_state):
    wa.consent()  # gcli.auth_command, for an `auth --write`: a dead write token must stay renewable
    wa.consume("drive")


def gdrive(monkeypatch, names: dict):
    """The gdrive CLI with Drive's file metadata faked: no network, no token."""
    from conftest import WORKSPACE_ROOT
    from importlib.machinery import SourceFileLoader
    from importlib.util import module_from_spec, spec_from_loader
    loader = SourceFileLoader("gdrive_cli", str(WORKSPACE_ROOT / "core/tools/files/gdrive"))
    cli = module_from_spec(spec_from_loader(loader.name, loader))
    loader.exec_module(cli)
    monkeypatch.setattr(gauth, "resolve_alias", lambda a: "personal")
    monkeypatch.setattr(cli, "_meta", lambda alias, fid: {"id": fid, "name": names[fid], "modifiedTime": "t0"})
    return cli


def test_trashing_many_files_is_one_plan_that_names_each_of_them(plan_state, monkeypatch, capsys):
    cli = gdrive(monkeypatch, {"a1": "Ata.pdf", "b2": "Notas"})
    with pytest.raises(SystemExit) as stop:
        cli.cmd_rm(None, ["a1", "b2"])
    out = capsys.readouterr().out
    assert stop.value.code == wa.AWAITING and out.count("CODE") == 1
    assert "'Ata.pdf' (a1)" in out and "'Notas' (b2)" in out


def test_a_local_file_edited_after_its_upload_plan_is_refused(plan_state, monkeypatch, capsys, tmp_path):
    cli = gdrive(monkeypatch, {})
    doc = tmp_path / "aula.md"
    doc.write_text("v1", encoding="utf-8", newline="\n")
    with pytest.raises(SystemExit):
        cli.cmd_put(None, str(doc), "root", None, None)
    code = json.loads((plan_state / "pending_write.json").read_text(encoding="utf-8"))["code"]
    doc.write_text("v2", encoding="utf-8", newline="\n")
    approve(plan_state, monkeypatch, code)
    with pytest.raises(SystemExit, match="changed since"):
        cli.cmd_put(None, str(doc), "root", None, None)


def test_a_body_replace_shows_its_diff_capped_and_saves_all_of_it(plan_state):
    old = "\n".join(f"linha {i}" for i in range(200))
    new = old.replace("linha 150", "linha cento e cinquenta")
    assert wa.diff_lines(old, old, "doc.md") == []
    lines = wa.diff_lines("", new, "doc.md")
    assert lines[0] == "doc.md: +200 / -0 linhas" and len(lines) == 1 + wa.SHOWN + 1
    assert str(plan_state / "pending_write.diff") in lines[-1]
    assert "+linha cento e cinquenta" in (plan_state / "pending_write.diff").read_text(encoding="utf-8")




def test_the_plan_names_only_the_cells_that_change():
    old = {"range": "'Aba 2'!B2:C3", "values": [["1", "2"], ["3"]]}
    assert sheets_core.cell_lines(old, [["1", "9"], ["3", "4"]]) == ["Aba 2!C2: '2' → '9'", "Aba 2!C3: '' → '4'"]
