"""Parity tests for the local direct-read fast path in ShellFileOperations.

The fast path (_can_direct_read/_direct_read_plain) promises to be
byte-identical to the shell ``sample + sed|cut + wc -l + tail`` pipeline for
the cases it handles. These tests pin the exact edges where a naive Python
reimplementation diverges (all four were real divergences found in review):

1. wc-vs-split line counting on trailing-newline files (past-EOF hint said
   51 when the shell says 50)
2. final unterminated line: invisible to ``wc -l`` but printed by sed
3. binary-by-extension files (.bin with perfectly text bytes)
4. image extensions must fall through to the shell path's vision redirect
5. BOM stripped from the first page only, like the shell path
"""

import json

import pytest

from tools.file_tools import read_file_tool


def _write(tmp_path, name, data):
    p = tmp_path / name
    if isinstance(data, str):
        p.write_text(data, encoding="utf-8")
    else:
        p.write_bytes(data)
    return p


def test_past_eof_hint_counts_lines_like_wc(tmp_path, monkeypatch):
    monkeypatch.setenv("TERMINAL_CWD", str(tmp_path))
    # 50 complete lines + trailing newline: split() says 51, wc says 50.
    p = _write(tmp_path, "r.txt", "\n".join(f"l{i}" for i in range(1, 51)) + "\n")
    result = json.loads(read_file_tool(str(p), offset=900, limit=50))
    hint = result.get("hint") or ""
    assert "beyond the end" in hint
    assert "(50 lines total)" in hint


def test_final_unterminated_line_is_counted_and_printed(tmp_path, monkeypatch):
    monkeypatch.setenv("TERMINAL_CWD", str(tmp_path))
    # No trailing newline: wc counts 2, but sed prints 3 lines.
    p = _write(tmp_path, "u.txt", "a\nb\nc")
    result = json.loads(read_file_tool(str(p), offset=1, limit=10))
    body = result.get("output") or result.get("content") or ""
    # Line-number format is ``N|content``; all three lines visible including
    # the wc-invisible unterminated one.
    assert "1|a" in body and "2|b" in body and "3|c" in body
    assert result.get("total_lines") == 2  # wc parity, not the sed view


def test_truncation_hint_uses_wc_count(tmp_path, monkeypatch):
    monkeypatch.setenv("TERMINAL_CWD", str(tmp_path))
    p = _write(tmp_path, "t.txt", "x\n" * 30)  # wc=30
    result = json.loads(read_file_tool(str(p), offset=1, limit=10))
    assert result.get("truncated") is True
    assert "Use offset=11" in (result.get("hint") or "")


def test_binary_by_extension_stays_binary_disclosure(tmp_path, monkeypatch):
    monkeypatch.setenv("TERMINAL_CWD", str(tmp_path))
    # Text bytes under a binary extension: classification is by extension
    # BEFORE the UTF-8 sample; the fast path must agree with the wrapper.
    p = _write(tmp_path, "looks_text.bin", b"just text, really\n")
    result = json.loads(read_file_tool(str(p)))
    err = result.get("error") or ""
    assert "binary" in err.lower()
    assert ".bin" in err


def test_image_extension_falls_through_to_vision_redirect(tmp_path, monkeypatch):
    monkeypatch.setenv("TERMINAL_CWD", str(tmp_path))
    p = _write(tmp_path, "pic.png", b"\x89PNG-not-really-but-extension-rules\n")
    result = json.loads(read_file_tool(str(p)))
    blob = (result.get("error") or "") + (result.get("hint") or "")
    assert "vision_analyze" in blob


def test_bom_stripped_from_first_page_only_semantics(tmp_path, monkeypatch):
    monkeypatch.setenv("TERMINAL_CWD", str(tmp_path))
    p = _write(tmp_path, "bom.txt", "﻿first\nsecond\n")
    result = json.loads(read_file_tool(str(p), offset=1, limit=10))
    body = result.get("output") or result.get("content") or ""
    assert "﻿" not in body.splitlines()[0]
