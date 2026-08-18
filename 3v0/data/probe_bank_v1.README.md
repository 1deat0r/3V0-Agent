# Probe Bank v1 — Human-Readable Companion

Machine-readable source of truth: `probe_bank_v1.json`. This file is a human
summary; the JSON is authoritative and frozen. Bank lifetime: fixed set of
cadences, then regenerated fresh by an independent subagent (the regenerated
scoreline is not directly comparable — flagged as such).

Frozen on: 2026-08-18, bank version **v1**. No date/time-timestamp appears in
any task expectation, so the bank does not rot.

---

## What this is

A held-out, difficulty-banded task bank for 3V0's **evolution monitor** (per
`EVOLUTION_PROBE.md` v0.2). Authored by an independent subagent — 3V0 did not
choose or see these tasks. Every task is universal, self-contained, and
solvable with only a terminal + files + web. **None** is drawn from 3V0's own
repo, tests, skills, or past work, and none is about 3V0.

Each task carries a **pre-registered rubric** written before any attempt:
objective, checkable PASS criteria plus an INCONCLUSIVE condition. The pinned
grader (temperature=0, seed=0, fresh context) applies these exactly and never
re-derives expectations.

---

## Bank composition

| Band | Count | Role (per design §1) |
|------|-------|----------------------|
| easy | 5  | regression floor (sensitivity) |
| medium | 8 | regression floor (sensitivity) |
| hard | 6 | growth hint (ceiling) |
| escalated | 4 | frontier walk — escalates until failure expected |

**Total: 23 tasks** (within the design's 20–30). IDs `probe001` … `probe023`.

Work-type / domain coverage (each task spans one): coding (5), debugging (3),
reasoning (4), planning (3), research-synthesis (4), tool-chain (4).

## Escalated band — how to grade

The 4 escalated tasks (`probe020`–`probe023`) are **frontier walks**: each
defines escalating STAGES, and later stages are expected to get progressively
harder and may not be fully reached. The grader records **PASS at the highest
stage fully met** (and documents it). Reaching failure on a later stage is
expected and is NOT a FAIL of the whole task — it defines the frontier ceiling.

## Band → task map

**easy** — probe001 (fizzbuzz exact output) · probe002 (CSV max-per-name shell
pipeline) · probe003 (dedupe-preserve-order debug) · probe004 (liar puzzle, 2:
A,C) · probe005 (migration plan with dirty-data rules)

**medium** — probe006 (`tree.py`, exact ASCII tree + `-d` depth) · probe007
(group-anagrams unhashable-key debug) · probe008 (greedy coin counterexample,
12) · probe009 (topological order + cycle detection) · probe010 (Cache-Control
synthesis) · probe011 (tar+sha256 reproducible script) · probe012 (max
non-overlapping meetings) · probe013 (git bisect synthesis)

**hard** — probe014 (mini CSV query engine, exact output) · probe015 (thread
race fix) · probe016 (count digit '1' in 1..999 = 300) · probe017 (critical-path
length = 17) · probe018 (regex-token semantics + precedence) · probe019
(multi-stage normalization pipeline)

**escalated (frontier walks)** — probe020 (REST todo service → concurrency →
idempotency) · probe021 (author benchmark → timing → non-obvious wrong answer)
· probe022 (build+package → byte-identical reproducible → offline/vendored
build) · probe023 (Dijkstra → negative-edge diagnosis → negative-cycle handling)

## Grading rules (grader_requirements in JSON)

- temperature=0, seed=0, pinned independent subagent; identity recorded per run.
- Apply the pre-registered rubric ONLY. Do the objective check (run the
  artifact, diff exact output, run the hidden assertions) before deciding.
- INCONCLUSIVE ONLY if the artifact is absent, the environment blocked a clean
  run, or the check is genuinely ambiguous — never as an escape for an item
  that objectively FAILED.
- Escalated tasks: verify against fresh scratch so no leftover state leaks;
  partial stage credit is recorded as the highest stage fully met.
- Results are advisory only (design §6) and appended to
  `probe_results.json` with grader identity + bank version.

## Reproducibility notes

- Every task's inputs (CSV contents, sample file trees, dependency tables,
  input.txt lines, concurrency/precision assertions) are embedded inline in
  the prompt, so any fresh run reproduces identical conditions.
- Expected outputs are deterministic (exact strings / fixed integers) — no
  'current date', timestamps, or network-dependent values appear in any rubric.
- Where tasks allow web research (research-synthesis band), the target facts
  (HTTP Cache-Control, git bisect, regex semantics) are stable and not
  date-sensitive.
