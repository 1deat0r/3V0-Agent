"""Fuzzy / typo-tolerant candidate expansion (retrieval stone 2).

The exact-token tier (retrieval_fts.py) is perfect when a query repeats target
vocabulary verbatim (verified to recall@1=1.0 under a real budget), but it
collapses on typos: "fivver" never exact-matches "fiverr". This tier adds a
deterministic, embedding-free noisy-channel correction:

    for each query term, if it does NOT verbatim-match any content token, find
    a content token within edit distance <= 1 and substitute the real token
    (deterministic tie-break: closest length, then lexicographically smallest).

So a typo'd term is corrected BEFORE scheduling (FTS candidate_ids) and scoring
(keyword overlap), making the true target both surface and rank top on the
already-measured typo queries. Genuinely ambiguous one-token queries (the
"partial" class) are left to the later, gated embedding tier — this tier does
not invent disambiguation it cannot justify.
"""
from __future__ import annotations

import re

from . import memdb


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


_VOCAB_CACHE: dict[int, tuple] = {}  # id(conn) -> (fingerprint, vocab)


def build_vocab(conn, min_len: int = 3) -> set[str]:
    """Every content token across the store's valid facts (deterministic set).

    Fingerprint-cached per connection, keyed by a cheap aggregate (count, maxid)
    so cache-hit injects don't re-read every fact; facts are only materialised
    and tokenised on a genuine staleness miss.
    """
    fp = tuple(conn.execute(
        "SELECT COUNT(*), COALESCE(MAX(id), 0) FROM facts WHERE valid_to IS NULL"
    ).fetchone())
    cid = id(conn)
    cached = _VOCAB_CACHE.get(cid)
    if cached is not None and cached[0] == fp:
        return cached[1]
    vocab: set[str] = set()
    for f in memdb.valid_facts(conn):
        hay = " ".join(str(f.get(k) or "") for k in
                       ("subject", "predicate", "object", "content"))
        vocab.update(t for t in _words(hay) if len(t) >= min_len)
    _VOCAB_CACHE[cid] = (fp, vocab)
    return vocab


def _within_ed1(a: str, b: str) -> bool:
    """True if Damerau-Levenshtein distance(a, b) <= 1 (fast, no DP).

    Supports the common real typos: one substitution, one insertion, one
    deletion, or one adjacent transposition ("teh" -> "the").
    """
    if a == b:
        return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if abs(la - lb) == 1:  # one insertion / deletion
        if la > lb:  # ensure a is the shorter
            a, b, la, lb = b, a, lb, la
        i = j = edits = 0
        while i < la and j < lb:
            if a[i] != b[j]:
                edits += 1
                if edits > 1:
                    return False
                j += 1
            else:
                i += 1
                j += 1
        return True
    # equal length: <=1 substitution, OR one adjacent transposition
    diffs = [i for i in range(la) if a[i] != b[i]]
    if len(diffs) <= 1:
        return True
    if len(diffs) == 2:
        i, j = diffs
        return a[i] == b[j] and a[j] == b[i]
    return False


def expand_term(term: str, vocab: set[str]) -> str | None:
    """Correct an unknown term to a known content token within ed <= 1, or None."""
    if term in vocab:
        return None
    candidates = [v for v in vocab if _within_ed1(term, v)]
    if not candidates:
        return None
    candidates.sort(key=lambda v: (abs(len(v) - len(term)), v))  # deterministic
    return candidates[0]


def expand_query(terms: list[str], vocab: set[str]) -> list[str]:
    """Return the term list with each unknown (typo'd) term substituted by its
    nearest known token; identity terms unchanged. Cheap no-op if nothing changes.
    """
    out = list(terms)
    changed = False
    for i, t in enumerate(out):
        fixed = expand_term(t, vocab)
        if fixed is not None and fixed != t:
            out[i] = fixed
            changed = True
    if not changed:
        return out
    # drop duplicate/noise after correction? keep length aligned; de-dup remains to caller
    return out