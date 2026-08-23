"""Unit tests for the ENV-FUNNEL scanner's AST classifier (tickets #20/#21).

The classifier is the contract gate for the funnel: it must reliably tell
branded READS (migrate to branded_env) apart from writes/pops (later half)
and unprefixed wire vars (documented exceptions).
"""

import importlib.util
import sys
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "env_funnel_scan.py"
_spec = importlib.util.spec_from_file_location("env_funnel_scan", _SCRIPT)
scan = importlib.util.module_from_spec(_spec)
# Register before exec: the module defines dataclasses with deferred
# annotations, and their resolution looks the module up in sys.modules.
sys.modules["env_funnel_scan"] = scan
_spec.loader.exec_module(scan)


def kinds_of(src: str) -> list[tuple[str, str]]:
    return [(k, v) for _, k, v in scan.classify_source(src)]


def test_branded_get_read_is_classified():
    out = kinds_of('X = os.environ.get("EV0_MODEL", "")\n')
    assert out == [("branded_read", "EV0_MODEL")]


def test_canonical_spelling_counts_as_branded_too():
    out = kinds_of('X = os.environ.get("3V0_HOME")\n')
    assert out == [("branded_read", "3V0_HOME")]


def test_os_getenv_prefixed_is_a_read():
    out = kinds_of('X = os.getenv("EV0_TUI_SKILLS")\n')
    assert out == [("branded_read", "EV0_TUI_SKILLS")]


def test_bracket_load_vs_store_vs_del():
    src = (
        'a = os.environ["EV0_A"]\n'
        'os.environ["EV0_B"] = "1"\n'
        'del os.environ["EV0_C"]\n'
    )
    assert kinds_of(src) == [
        ("branded_bracket_read", "EV0_A"),
        ("branded_write", "EV0_B"),
        ("branded_del", "EV0_C"),
    ]


def test_setdefault_and_pop_are_not_reads():
    src = (
        'os.environ.setdefault("EV0_QUIET", "1")\n'
        'os.environ.pop("EV0_YOLO_MODE", None)\n'
    )
    kinds = {k for k, _ in kinds_of(src)}
    assert kinds == {"branded_write", "branded_pop"}
    assert not ({"branded_read"} & kinds)


def test_unprefixed_wire_vars_stay_unprefixed():
    out = kinds_of(
        'server = os.getenv("IRC_SERVER", "")\n'
        'os.environ["TERMINAL_CWD"] = cwd\n'
    )
    assert ("unprefixed_read", "IRC_SERVER") in out
    assert ("unprefixed_write", "TERMINAL_CWD") in out
    assert all(not k.startswith("branded") for k, _ in out)


def test_dynamic_key_is_flagged_for_manual_review():
    out = kinds_of('key = "EV0_" + suffix\nv = os.environ.get(key)\n')
    assert ("dynamic", "<dynamic>") in out


def test_multiline_call_keeps_call_line():
    src = (
        "_g = float(\n"
        '    os.environ.get("EV0_TTL_S") or 60\n'
        ")\n"
    )
    assert kinds_of(src) == [("branded_read", "EV0_TTL_S")]
    assert [line for line, _, _ in scan.classify_source(src)] == [2]


def test_non_environ_calls_are_ignored():
    out = kinds_of(
        'd = {}\n'
        'x = d.get("EV0_NOT_ENV")\n'
        'y = getenv("EV0_BARE_GETENV")\n'  # bare getenv without os. is out of scope
    )
    assert out == []


def test_check_gate_finds_leftover_branded_reads(tmp_path, capsys):
    f = tmp_path / "m.py"
    f.write_text('A = os.environ.get("EV0_LEFT", "")\n', encoding="utf-8")
    findings = scan.scan_paths([str(f)])
    leftovers = scan.branded_reads(findings)
    assert len(leftovers) == 1
    assert leftovers[0].var == "EV0_LEFT"


def test_check_gate_passes_clean_package(tmp_path):
    f = tmp_path / "clean.py"
    f.write_text(
        'from env_compat import branded_env\n'
        'A = branded_env("LEFT") or ""\n',
        encoding="utf-8",
    )
    findings = scan.scan_paths([str(f)])
    assert scan.branded_reads(findings) == []
