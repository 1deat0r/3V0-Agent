#!/usr/bin/env python3
"""Phase R1c: AST-offset sweep for identifiers missed by tokenize.

tokenize on 3.11 treats identifiers INSIDE f-string braces as part of the
STRING token, so the tokenizer sweep missed real variable references like
f'EV0_HOME={ev0_home}'. Use ast.Name/Attribute node offsets to rename those
precisely (string literals still untouched).
"""
from pathlib import Path
import ast
import subprocess

files = subprocess.run(["git", "ls-files", "*.py"],
                       capture_output=True, text=True).stdout.split()


def sweep_text(text: str) -> tuple[str, int]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return text, 0
    edits = []  # (lineno, col_offset, end_col_offset, old_id, new_id)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and "ev0_" in node.id and "threev0_" not in node.id:
            edits.append((node.lineno, node.col_offset, node.end_col_offset,
                          node.id, node.id.replace("ev0_", "threev0_")))
        elif isinstance(node, ast.Attribute) and "ev0_" in node.attr and "threev0_" not in node.attr:
            # attribute access on a Name like gateway_cli._sync_ev0_home_from_systemd_unit
            pass  # ast.Name inside handles the full token? No — attr is separate.
    if not edits:
        return text, 0
    lines = text.splitlines(keepends=True)
    n = 0
    # apply from last to first so offsets stay valid
    for lineno, col, endcol, _old, new in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True):
        line = lines[lineno - 1]
        # Only edit if the span is still the old value (don't double-edit nested)
        seg = line[col:endcol]
        if "ev0_" in seg and "threev0_" not in seg:
            lines[lineno - 1] = line[:col] + seg.replace("ev0_", "threev0_") + line[endcol:]
            n += 1
    return "".join(lines), n


total = changed = 0
for f in files:
    p = Path(f)
    try:
        data = p.read_text()
    except Exception:
        continue
    new, n = sweep_text(data)
    if n:
        p.write_text(new)
        total += n
        changed += 1
print(f"ast-swept {changed} files, {total} name tokens")

# Now handle monkeypatch-style attribute TARGET strings (functional: they
# reference renamed module functions by name — sweeping keeps them correct).
import re
def sweep_setattr_strings(text: str) -> tuple[str, int]:
    # patterns: setattr(x, "get_ev0_home", v)  /  setattr(x, "_sync_ev0_home_...", ...)
    n = 0
    def repl(m):
        nonlocal n
        if "ev0_" in m.group(1) and "threev0_" not in m.group(1):
            n += 1
            return m.group(0).replace(m.group(1), m.group(1).replace("ev0_", "threev0_"))
        return m.group(0)
    out = re.sub(r'setattr\([^,]+,\s*"([^"]*ev0_[^"]*)"', repl, text)
    return out, n

total2 = changed2 = 0
for f in files:
    p = Path(f)
    try:
        data = p.read_text()
    except Exception:
        continue
    new, n = sweep_setattr_strings(data)
    if n:
        p.write_text(new)
        total2 += n
        changed2 += 1
print(f"setattr-string swept {changed2} files, {total2} tokens")