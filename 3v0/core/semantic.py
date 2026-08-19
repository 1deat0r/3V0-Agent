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
    """Hybrid reranker: cosine (semantic) merged with the lexical score."""

    def __init__(self, store: SemanticStore, *, alpha: float = 0.6):
        self.store = store
        self.alpha = alpha

    def rerank(self, facts: list[dict], query: str) -> list[dict]:
        self.store.ensure(facts)  # embed + cache any uncached facts (persisted)
        qv = self.store.embed_fn([query])[0]
        vecs = self.store.vectors()
        qterms = [t for t in query.lower().split()]

        def lex_score(f: dict) -> int:
            hay = " ".join(str(f.get(k) or "") for k in
                           ("subject", "predicate", "object", "content")).lower()
            return sum(1 for t in qterms if t in hay)

        lex = [lex_score(f) for f in facts]
        maxlex = max(lex) or 1.0
        scored = []
        for f, lx in zip(facts, lex):
            v = vecs.get(f["id"])
            cos = _cos(qv, v) if v is not None else 0.0
            hybrid = self.alpha * cos + (1 - self.alpha) * (lx / maxlex)
            scored.append((hybrid, f))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [f for _, f in scored]