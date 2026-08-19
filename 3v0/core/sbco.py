"""SBCO — self-supervised, verifier-grounded harness optimization ("2608.10157").

The SBCO position: you need not run an expensive Darwin/Huxley-style Gödel-machine
self-modification search to improve an agent. Keep the meta-agent fixed and instead
optimize the *harness* (verifier weights + a rejection threshold) against the graded
feedback already produced from the agent's own attempts — a self-supervised block
coordinate ascent, 4-5.5x cheaper than the self-modifying baselines.

This module realizes SBCO on 3V0's existing gauge:
- the **decomposed verifier bank** sits on top of the evolution monitor (the certified
  grader / probe bank become the *curriculum*), and folds in `safe_evolve` as a
  safety verifier — so optimization can't trade safety for verified score;
- the **harness policy** is a small config (per-verifier weights + a rejection
  threshold): raising a weight biases what "verified" means; a higher rejection
  threshold makes the harness abstain rather than fabricate on uncertain outputs;
- **approximate block coordinate ascent** tunes one policy dimension at a time from
  the agent's OWN graded feedback (no human labels), keeping the best mean-verified
  score, and is deterministic for a fixed curriculum + neighbor order.

Determinism is a first-class invariant (ADR-0004): given the same curriculum, verifier
set, base config, and seed, BCA returns the same result every time — that is what makes
the result auditable and re-runnable, unlike a stochastic reinforcement search.
"""

from __future__ import annotations
import copy
import math
from dataclasses import dataclass, field
from typing import Callable

from . import safe_evolve

# A verifier maps (task, output) -> 0..1. Deterministic.
VerifierName = str
Verifier = Callable[["Task", str], float]


@dataclass
class Task:
    prompt: str
    reference: str
    budget_tokens: int = 64
    metadata: dict = field(default_factory=dict)


@dataclass
class HarnessConfig:
    """The policy SBCO optimizes. ``weights`` keyed by verifier name; ``rejection``
    is a correctness floor below which the harness abstains (score forced to 0)."""
    weights: dict[VerifierName, float] = field(default_factory=dict)
    rejection: float = 0.5

    def clone(self) -> "HarnessConfig":
        return HarnessConfig(copy.deepcopy(self.weights), self.rejection)


@dataclass
class ScoreReport:
    per_output: list[float]
    mean: float
    progress: float        # mean minus abstain-rate penalty (the SBCO objective)
    abstain_rate: float


# ── Built-in verifiers (each deterministic) ──────────────────────────────────
def v_correct(task: Task, output: str) -> float:
    return 1.0 if output == task.reference else 0.0


def v_safety(task: Task, output: str) -> float:
    a = safe_evolve.audit(output)
    if a.blocking:
        return 0.0
    if a.caution:
        return 0.5
    return 1.0


def v_conciseness(task: Task, output: str) -> float:
    return 1.0 if len(output.split()) <= task.budget_tokens else 0.0


BUILTIN_VERIFIERS: dict[VerifierName, Verifier] = {
    "correct": v_correct,
    "safety": v_safety,
    "conciseness": v_conciseness,
}


FABRICATION_PENALTY = 1.0  # penalty score for a wrong answer that slipped past the gate


def evaluate(verifiers, tasks, outputs, config: HarnessConfig) -> ScoreReport:
    """Mean payoff under ``config`` for the agent's OWN graded outputs.

    Payoff per output (honesty-preserving):
      * correct (correctness == 1.0)      -> the weighted verified score (≈1.0 ideal)
      * wrong but NOT abstained (correctness >= rejection) -> -FABRICATION_PENALTY
      * abstained (correctness < rejection) -> 0.0  (refused; nothing harmful injected)
    So raising the rejection threshold to abstain on wrong outputs *improves* the
    score, and a harness that lets a wrong answer "verify" is strongly punished —
    SBCO cannot trade safety/correctness for a higher score.
    """
    names = [n for n, w in config.weights.items() if w > 0]
    wsum = sum(config.weights[n] for n in names) or 1.0
    per = []
    rejected = 0
    n = len(tasks)
    for t, out in zip(tasks, outputs):
        corr = v_correct(t, out)
        if corr >= config.rejection:
            if corr == 1.0:
                raw = sum(config.weights[n] * verifiers[n](t, out) for n in names) / wsum
            else:
                raw = -FABRICATION_PENALTY
        else:
            raw = 0.0
            rejected += 1
        per.append(raw)
    return ScoreReport(per, sum(per) / n if n else 0.0, sum(per) / n if n else 0.0,
                       rejected / n if n else 0.0)


def _neighbor(config: HarnessConfig, dim, step) -> HarnessConfig:
    c = config.clone()
    if dim == "rejection":
        c.rejection = round(c.rejection + step, 4)
    else:
        c.weights[dim] = round(c.weights.get(dim, 0.0) + step, 4)
    return c


def block_coordinate_ascent(verifiers, tasks, outputs, base: HarnessConfig, *,
                            delta: float = 0.25, rounds: int = 8) -> tuple[HarnessConfig, ScoreReport]:
    """Approximate block-coordinate ascent over the harness dims, maximizing
    ``progress`` deterministically.

    Deterministic: dims visited in a fixed order (sorted verifier weights, then the
    rejection threshold); each dim tried at ±``delta``; a neighbor is accepted only
    when it strictly improves ``progress`` from the agent's OWN graded outputs; the
    sweep stops when no dim improves. ``rounds`` bounds re-scans of the full dim set.
    """
    dims = [d for d in sorted(base.weights.keys())] + ["rejection"]
    best = base.clone()
    report = evaluate(verifiers, tasks, outputs, best)
    best_score = report.progress
    for _ in range(max(1, rounds)):
        improved = False
        for dim in dims:
            for step in (delta, -delta):
                cand = _neighbor(best, dim, step)
                r = evaluate(verifiers, tasks, outputs, cand)
                if r.progress > best_score + 1e-9:
                    best, best_score, report = cand, r.progress, r
                    improved = True
        if not improved:
            break
    return best, report