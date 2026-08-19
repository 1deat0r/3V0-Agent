"""Semantic tier for retrieval — bitdeer BAAI/bge-m3 embeddings + hybrid rank.

Closes the paraphrase (measured 0.12) and partial (0.06) gaps that no
deterministic lexical trick can soundly fix. Three pieces, all stdlib:

* ``embed_texts`` — batched /embeddings call to bitdeer bge-m3 (1024d). Uses a
  non-default User-Agent (Cloudflare 1010 blocks urllib's default UA — see
  native/llm.py) and retry_call because the provider can throttle.
* ``SemanticStore`` — a fact-embedding cache in a SQLite table on the memdb
  connection (persisted across injects), so repeated queries don't re-embed.
* ``SemanticRanker`` — merges lexical + cosine into a hybrid rank. OPT-IN via
  ``inject(..., semantic=ranker)``; any error degrades to the lexical result
  (the retrieval path is never blocked by the network).
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

from . import backoff

EMBED_URL = "https://api-inference.bitdeer.ai/v1/embeddings"
EMBED_MODEL = "BAAI/bge-m3"
DIMS = 1024
UA = "3V0-native-runtime/0.1.0"

_EMBED_TABLE = "fact_embeddings"


def _api_key() -> str:
    key = os.environ.get("BITDEER_API_KEY")
    if key:
        return key
    dotenv = Path("~/.hermes/profiles/3v0/.env").expanduser()
    try:
        for raw in dotenv.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line.startswith("BITDEER_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return ""


def embed_texts(texts: list[str], *, key: str | None = None, batch: int = 64,
                timeout: float = 30.0) -> list[list[float]]:
    """Embed ``texts`` (batched) via bitdeer bge-m3. Returns 1024‑d vectors.

    Raises backoff.ProviderError when the provider is unreachable / throttled,
    so callers (the semantic ranker) can degrade rather than fail retrieval.
    """
    key = key or _api_key()
    if not key:
        raise backoff.ProviderError(401, "no BITDEER_API_KEY", retryable=False)
    out: list[list[float]] = []
    for start in range(0, len(texts), batch):
        chunk = texts[start:start + batch]

        def _call():
            req = urllib.request.Request(
                EMBED_URL,
                data=json.dumps({"model": EMBED_MODEL, "input": chunk}).encode(),
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json", "User-Agent": UA},
                method="POST")
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return json.loads(resp.read().decode())
            except urllib.error.HTTPError as e:
                raise backoff.ProviderError(e.code, e.reason or str(e),
                                            retryable=True)
            except Exception as e:  # timeout / reset
                raise backoff.ProviderError(0, str(e), retryable=True)

        data = backoff.retry_call(_call)
        for item in sorted(data.get("data", []), key=lambda x: x.get("index", 0)):
            out.append([float(v) for v in item["embedding"]])

    if len(out) != len(texts):
        raise backoff.ProviderError(0, f"embed count mismatch {len(out)}/{len(texts)}",
                                    retryable=True)
    return out


def _ensure_table(conn) -> None:
    conn.execute(f"CREATE TABLE IF NOT EXISTS {_EMBED_TABLE} "
                 "(fact_id INTEGER PRIMARY KEY, vec TEXT)")
    conn.commit()


def _cos(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb + 1e-12)


class SemanticStore:
    """Fact-embedding cache backed by a table on the memdb connection."""

    def __init__(self, conn, *, embed_fn=embed_texts):
        self.conn = conn
        self.embed_fn = embed_fn
        _ensure_table(conn)

    def ensure(self, facts: list[dict]) -> None:
        """Embed + cache any fact lacking a stored vector (batched, one pass)."""
        missing = [f["id"] for f in facts
                   if not self._vec(f["id"])]
        if not missing:
            return
        by_id = {f["id"]: f for f in facts}
        for start in range(0, len(missing), 64):
            chunk = missing[start:start + 64]
            vecs = self.embed_fn([self._text(by_id[i]) for i in chunk])
            for fid, vec in zip(chunk, vecs):
                self.conn.execute(
                    f"INSERT OR REPLACE INTO {_EMBED_TABLE} (fact_id, vec) VALUES (?, ?)",
                    (fid, json.dumps(vec)))
            self.conn.commit()

    def vectors(self) -> dict[int, list[float]]:
        rows = self.conn.execute(
            f"SELECT fact_id, vec FROM {_EMBED_TABLE}").fetchall()
        return {r[0]: json.loads(r[1]) for r in rows}

    def _vec(self, fid: int):
        r = self.conn.execute(
            f"SELECT vec FROM {_EMBED_TABLE} WHERE fact_id=?", (fid,)).fetchone()
        return r[0] if r else None

    @staticmethod
    def _text(fact: dict) -> str:
        return " ".join(str(fact.get(k) or "") for k in
                        ("subject", "predicate", "object", "content"))


class SemanticRanker:
    """Lexical-gated cosine reranker.

    Merge lesson (measured): a weighted blend (alpha=0.6) scored 0.19 and RRF
    fusion 0.56 on the 16-pair paraphrase bench, but *pure cosine scores 0.81*
    — the lexical signal is pure noise for paraphrase and only drags the true
    fact down. Opposite extreme, pure cosine under-weights rich keyword matches
    (kw/nl/typo). So: gate how much to trust cosine on the query's lexical
    *discriminative power* across the candidate set:

        maxlex (max token-overlap with any fact)  ->  cosine weight g
            0   (no overlap: clear paraphrase)       -> 1.00
            1   (weak signal)                        -> 0.85
            2   (ambiguous keyword)                  -> 0.70
          >=3   (rich keyword match)                 -> 0.55

    ``cosn``/``lexn`` are each range-normalised over the candidate set so the
    blend is scale-consistent. ``lex_terms`` should be the *fuzzy-corrected*
    query terms (typo tier rewrote foverr->fiverr), so a misspelled keyword
    still gets full lexical credit and its embedding sees the corrected form —
    otherwise the gate would regress the typo class.
    """

    def __init__(self, store: SemanticStore, *, cosine_weights: dict[int, float] | None = None):
        self.store = store
        # maxlex -> cosine weight g (lexical weight = 1-g). Sorted asc.
        self._g = dict(cosine_weights or {0: 1.00, 1: 0.85, 2: 0.70, 3: 0.55})

    def _g_for(self, maxlex: int) -> float:
        best = self._g.get(maxlex)
        if best is not None:
            return best
        # above the largest explicit bucket -> smallest g (0.55); below 0 -> 1.0
        keys = sorted(self._g)
        if maxlex <= keys[0]:
            return self._g[keys[0]]
        return self._g[keys[-1]]

    def rerank(self, facts: list[dict], query: str, *, lex_terms: list[str] | None = None) -> list[dict]:
        self.store.ensure(facts)  # embed + cache any uncached facts (persisted)
        qv = self.store.embed_fn([query])[0]
        vecs = self.store.vectors()
        terms = lex_terms if lex_terms else [t for t in re.findall(r"[a-z0-9]+", query.lower())]
        if not facts:
            return facts

        scores = []
        for f in facts:
            hay = " ".join(str(f.get(k) or "") for k in
                           ("subject", "predicate", "object", "content")).lower()
            lex = sum(1 for t in terms if t in hay)
            v = vecs.get(f["id"])
            cos = _cos(qv, v) if v is not None else 0.0
            scores.append((f["id"], cos, lex))
        if not terms:  # nothing lexical to rely on -> pure cosine order
            by_id = {f["id"]: f for f in facts}
            return [by_id[i] for i, c, _ in sorted(scores, key=lambda x: x[1], reverse=True)]

        maxlex = max((s[2] for s in scores), default=0)
        cos_vals = [s[1] for s in scores]
        cmin, cmax = min(cos_vals), max(cos_vals)
        crange = max(cmax - cmin, 1e-12)
        g = self._g_for(maxlex)

        scored = []
        for i, c, lex in scores:
            cosn = (c - cmin) / crange
            lexn = (lex / maxlex) if maxlex else 0.0
            scored.append((g * cosn + (1 - g) * lexn, c, i))
        scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
        by_id = {f["id"]: f for f in facts}
        return [by_id[i] for _, _, i in scored]