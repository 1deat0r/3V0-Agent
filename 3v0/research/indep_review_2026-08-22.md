# Independent review of the 08-22 research digest — 2026-08-22
An adversarial re-check of the two arXiv digests (08-19, 08-22) against the ACTUAL codebase state,
done before taking any next step. Verdicts below override the digests where the digests read the
codebase cold and over- or mis-claimed.

All 23 papers cited in the 08-22 digest were verified live against the arXiv API (real, correct
dates/titles). No fabrication found. The problem was never the papers — it was that the digest's
next-action slate assumed gaps that the codebase had already closed.

## Ground truth: what already exists (verified in-tree, not assumed)

| 08-19 digest action | Status | Where |
|---|---|---|
| A — skill-authoring safety/reuse gate (misevolution) | **DONE** | `core/safe_evolve.py` (blocking/caution/clean + govern_reuse; regex, no LLM; test `tests/test_safe_evolve.py`) |
| B — SBCO decomposed-verifier bank + block-coordinate harness opt | **DONE** | `core/sbco.py` (HarnessConfig weights + rejection threshold, deterministic BCA, folds in safe_evolve) |
| C — memory consolidation / conflict reconciliation (MindMemOS) | **DONE** | `core/consolidate.py` + `core/memdb.py` (chain-anchor conflict identity; keep="newest" policy param; reversible) |
| Stone 5/6/7 — own read+write tools, own review process | **DONE** | `core/{decide,decide_skills,record,review_decide}.py`, `scripts/{record,record_skills,review_session,review}.py`; Stone 7 "built + live" |
| Evolution monitor (frozen held-out probe bank) | **DONE + peer-reviewed** | `EVOLUTION_PROBE.md` v0.2, revised 2026-08-18 post 3-expert review; bank `data/probe_bank_v1` (23 tasks, rubric pre-registered, pinned calibrated grader, first baseline run present in `probe_results.json`) |

## Where the 08-22 digest over-claimed (corrections)

1. **Phantom Gains (F1/F2) — NOT a blank gap; already largely mitigated.**
   EVOLUTION_PROBE §3 pre-registers a K=5 no-change calibration noise floor (2σ threshold +
   ≥2-consecutive-run reproducibility, "no measured change" language), §7 randomizes order, tracks
   first-seen vs re-seen, retires contaminated tasks, and §6 keeps decision coupling deliberately
   weak. This is precisely the noise-aware control discipline the Fragility paper demands.
   **Real Signature:** as the design says, the evolution monitor compares the *agent* across cadences
   against a calibration *grader* floor — it does NOT run a frozen *copy of the agent itself*
   through the identical pipeline as a null control. That is the genuinely missing piece. But note
   3V0 does not fine-tune/self-train its model, so Phantom Gains' specific training-artifact failure
   (LoRA ledger manufacturing gains on an untrained model) does not bite directly; what survives is
   the general "differencing two noisy estimates is artifact-prone" warning.

2. **Task-CoEvolve (F3) — recommended as a MUST, but it is ANTI-ALIGNED with this design.**
   The probe bank is frozen + held-out BY INVARIANT so the scoreline across cadences is comparable
   and Goodharting is bounded (§7). Co-evolving the validation tasks with the harness would break
   cross-cadence comparability and re-open the memorization/learning-the-bank risk the design
   explicitly declines to accept. The digest's blind priority here is wrong; downgrade from "must"
   to "only within a single run's *grader* step, never across cadences" — and even there, defer.
   The bank is small (23 tasks); the evaluation cost it saves is not the bottleneck this design has.

3. **Cross-Task Skill Transfer (F4 part, "text > code") — already aligned, near no-op.**
   Verified 3V0's skills on disk are YAML-frontmatter + natural-language markdown, each subtask-scoped
   (e.g. `apple/apple-notes/SKILL.md`). The paper's headline (text + subtask transfer beats code +
   whole-task) is already how 3V0 writes skills. The only live residue is: when distilling new skills
   from redo/review, keep them subtask-narrow and prose-y — which the AGENTS.md authoring standard
   already enforces. No new machinery required.

## Correction used to write the ranked list below
`retrieval_fts.py` (BM25) indexes **facts/memory**, NOT skills — so "skill selection is BM25 top-N"
in my first pass was wrong. Verified in-tree: skills are session-**preloaded by explicit identifier**
(`agent/skill_commands.py::build_preloaded_skills_prompt`), driven by `3v0 -s`, `EV0_TUI_SKILLS`,
or config/desktop bundles — not auto-retrieved or ranked per turn. Attention is guarded today by the
AGENTS.md HARDLINE `description ≤ 60 chars` rule ("dilute the model's attention when many skills are
loaded") plus platform gating and bundle curation. So the Optimal-Skill-Selection paper maps to the
**preload-decision** layer (which identifiers to preload), which is currently operator/env-directed,
not to a real retriever code path. That downgrades it from "do now, real code port" to "design idea
for automatic preload."

## What is GENUINELY net-new and implementable (ranked, corrected)

1. **Add the frozen-*agent* null control to the probe pipeline.**
   This is the strongest net-new action and it is independent of the skill-selection misread. It is
   the natural completion of EVOLUTION_PROBE §3: the design calibrates the *grader's* noise floor and
   compares the live agent across cadences, but it never pushes a *frozen snapshot of the agent*
   through the identical bank + grader as a null, and reports each live run as the delta vs. that
   null. This closes the one remaining Phantom Gains / Fragility hole (differencing two noisy
   estimates). Small, testable, preserves the frozen/held-out bank invariant — the design already
   says the bank's "regenerated scoreline is not directly comparable," and A/B-ing live-vs-frozen
   snapshot at a fixed commit is exactly the kind of control it lacks. Do first.

2. **Skill preload budget (Optimal Skill Selection) — design note, not a port.**
   If/when 3V0 automates which skills to preload into a bounded prompt, model it as a token-budgeted
   monotone-submodular packing (BPS, provable bicriteria) over the preload candidates, on top of the
   existing disabled/platform/bundle filters. Today preload is operator-driven, so there is no code
   path to change; record this as the governing design when auto-preload lands. Do NOT retrofit a
   retriever that does not exist.

3. **SkillForge-style repo synthesis** — genuinely absent (no match for synthesize-issue-from-core/-
   tests) and well-matched if 3V0 wants project-specific skills for its own evolving repo. But it is
   a project, not a one-line port; 3V0 already has a working skill pipeline (seed/sync/decide +
   record). Land after #1; tag for the roadmap.

## Papers that are informational for 3V0 but have no direct 3V0-shaped implementation (do NOT build)
- Task-CoEvolve (see §2 above), EnvHarness, AI4AI-Bench, Inducing Task Models, MidTool, Wuying-
  Browser-Agent, LEGO-RL, Agent Lightning, Governance Records as Supervision, ComponentBench —
  research context for the browser substrate and agentic-RL ambitions, no current 3V0 code path.
- Safety/bench papers (HarnessRisk, MaliciousSkillBench, D²ACCI, Governance at the Boundary,
  Obedience) — audit/boundary context; note there IS already an in-repo audit tree (`docs/audit/`).
  Screen them into that existing audit discipline rather than starting new parallel work.
- SkillGate (selector credit starvation) — forward-looking caution for any future RL-tuned skill
  selection, not actionable now.

## Bottom line (independent priority, after correction)
1. **Frozen-agent null control in the probe** — closes the last measurement hole; small, testable,
   preserves the frozen-bank invariant. Do first (cost ~1 frozen snapshot run per cadence/lifetime).
2. **Skill-preload budget** (2608.19993) — *design note* for automatic preload; no current code path
   (preload is operator/env-driven; BM25 is memory, not skills). Record it, don't build it.
3. **SkillForge repo-synthesis** — roadmap after #1; biggest lift, no urgent trigger.
4. Delete/ignore the rest of the 08-22 slate's "musts" (F1/F2/F3 as stated) — they were either
   answered by code that already existed or anti-aligned (Task-CoEvolve breaks the frozen bank).

This review supersedes the action slate inside `arxiv_self_evolution_2026-08-22.md`. If both files
are kept, read this one last.

## Resolution (2026-08-22, item #1 implemented)
Item #1 (frozen-agent null control) is now live in `native/probe.py::null_control` + tests
(`tests/test_native_probe.py::NullControlTest`, 6 cases, all green) and documented in
`EVOLUTION_PROBE.md` (§3 addendum + §9 rollout steps 4/6). Semantics: a cadence run is asserted only
as its live-vs-frozen-null per-band delta; `off` = both inside the calibrated band; `null-drift` = the
frozen null itself left the band (control stale, comparison invalid — re-freeze, do not claim);
`growth-hint`/`regression-suspect` = live outside while null inside, advisory only pending the >=2-run
`apply_trend` gate. Item #2 kept as design note (no auto-preload code path). Item #3 remains roadmap.
No new runtime deps; stdlib-only, mirrors `probe.py` conventions.