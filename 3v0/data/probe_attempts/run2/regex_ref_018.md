# Regex token reference (Python `re` semantics)

**(1) `\b` — word boundary.** A zero-width assertion that the current position sits between a word character (`[A-Za-z0-9_]`) and a non-word character (or start/end of string); it matches nothing itself.
Example: `re.search(r"\bcat\b", "a cat sat")` matches the word `cat` (boundaries before `c` and after `t`), but `\bcat\b` does **not** match in `"scatter"` — the `cat` there sits between two word chars (`s`…`t`), so there is no boundary before it.

**(2) `\B` — NOT a word boundary.** The inverse of `\b`: asserts the position is **not** between a word and a non-word char (typically *between two word characters*).
Example: `re.search(r"\Bcat\B", "scatter")` matches `cat` inside `scatter` — it is preceded by `s` and followed by `t` (both word chars, so no boundaries). The same pattern does **not** match in `"a cat"` where `cat` stands at word boundaries.

**(3) `(?<=...)` lookbehind.** A zero-width assertion that the text *immediately before* the current position matches `...`; the asserted text is **not** included in the match.
Example: `re.search(r"(?<=pre)(\w+)", "presuffix")` matches `suffix` (the lookbehind requires `pre`, which is consumed as an assertion, not part of the match).

**(4) `(?<!...)` negative lookbehind.** Asserts the text immediately preceding does **not** match `...`.
Example: `(?<!un)happy` matches `happy` in `"very happy"`, but does **not** match in `"unhappy"` because the preceding text `un` does match the negative assertion, invalidating it.

**(5) `(?:...)` non-capturing group.** Groups the enclosed atoms so quantifiers/alternation apply to the group as a unit, but forms **no back-reference** (group 1 is not created).
Example: `re.findall(r"(?:ab)+", "xabababy")` matches `ababab`; `\1` is unavailable because the group is non-capturing.

**(6) `(?P<name>...)` named group.** Captures the matched text under an explicitly **named** group, retrievable by name.
Example: `m = re.search(r"(?P<year>\d{4})", "in 1984")` → `m.group("year")` returns `"1984"`.

## Precedence (tightest → loosest)
1. **Quantifier** (`*`, `?`, `+`, `{m,n}`) — binds **tightest**, applying to the immediately preceding atom or group.
2. **Concatenation** — adjacency of atoms/groups.
3. **Alternation `|`** — **loosest** precedence.

Consequence: in `ab|cd`, the `|` splits the whole expression (`ab` or `cd`), so `a(?:bc|d)` is needed to make the alternation apply to just `bc` vs `d`. A quantifier applies to one atom by default, e.g. `ab*` is `a` followed by zero-or-more `b`s, not `(ab)*`.
