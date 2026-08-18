# arXiv self-evolution research digest — 2026-08-19
Grounding for 3V0's evolution toward a self-evolving ASI harness.
Freshest arXiv crawl reachable: 2026-08-17. All citations dated; v1 preprints (unreviewed).

## Seven kernels mapped to 3V0

### 1. HELIX `2608.13951` (08-14) — Model–harness co-evolution, recursive self-improvement
Agent acts through a runtime harness (context/tools/control/stopping) that shapes both capability
AND the trajectories it learns from. Loop: harness for fixed model → update model from verified
sibling trajectories → rebuild harness as model changes. Source-traceable substrate (typed ports,
reusable atoms, recipes, runtime policies) with explicit auditable interventions; harness evolution
produces matched successes/regressions/near-misses as data for model updates.
**→ 3V0:** this is the native-twin + probe-bank loop made explicit. Adopt: treat harness evolution as
a data *generator* for model improvement (probe sibling coverage), not just capability.

### 2. Evo-Harness `2608.15071` (08-15) — Context-to-harness one-shot skill compilation
Online harness learning: frozen agent improves by continuously updating a structured harness across
sequential tasks; distils noisy single-shot executions into reusable cross-domain skill harnesses.
Evaluated on SWE-bench, TerminalBench2, WebArena-Infinity, etc.
**→ 3V0:** codifies the redo-log → skill loop. Adopt: compile one-shot probe/redo executions into
harness skills, validated across topics, not just stored.

### 3. SBCO `2608.10157` (08-10) — Self-supervised, verifier-grounded harness optimization
Same family as Darwin/Huxley Gödel Machines (open-ended self-reference, agent edits own code) but
**self-supervised, not self-referential**: learns a decomposed bank of verifiers + a harness policy via
approximate block-coordinate ascent from its OWN graded feedback — fixed meta-agent, no human labels.
Matches/exceeds self-modifying baseline at 4–5.5× LESS compute.
**→ 3V0:** the evolution monitor (certified grader + hold-out bank + advisory grading) already embodies
this. Adopt: "decomposed bank of verifiers" + block-coordinate *harness* optimization from own feedback
— the exact cheap path to ASI-style self-improvement without landing on the expensive Gödel-machine
self-modification search.

### 4. Hierarchical Self-Improvement `2608.08466` (08-09) — Task-specific evolvable harnesses
Harness is hot-swapped per task family via a fixed task-injection seam, rewritten from environment
feedback; three scopes: task harness / evolver / meta-evolver (frozen outer anchor).
**Two honest bounds:** feedback-fidelity bound (needs informative reward) and backbone-capability bound
(harness redesign cannot beat the frozen model's ceiling — no gain on NLE). Used **DeepSeek-V4-Flash**
as frozen backbone.
**→ 3V0:** confirms the native-twin seam design; WARNS that harness/memory evolution cannot exceed the
substrate model's capability ceiling — a real, sobering upper bound on self-evolution without substrate
upgrade or preference-learning the model.

### 5. Practice Makes Unsafe `2608.12851` (08-13) — Skill misevolution (SAFETY)
Self-improving agents turn successful trajectories into persistent policy. An *unsafe success* thus
becomes reusable. Evolution optimizes task outcome, not procedure safety → skill misevolution; risk
attributed across authoring → retrieval → execution. SafeEvolve wrapper: repair unsafe content + govern
reuse; −26.7pp unsafe retrieval, −17.3pp fresh-session harm, benign utility −0.4.
**→ 3V0 (MUST adopt):** auto-authored skills/redo from successes carry this exact risk. Add a
lifecycle-aware safety gate to skill authoring: what updates may write, and what executors may reuse.

### 6. MindMemOS `2608.12428` (08-12) — Self-evolving memory operating layer
Unified entity-property-time structure; scenario-adaptive schemas via validation-driven evolutionary
search (MindMemEvolve); consolidation "dreaming" merges/reconciles; implicit corrective feedback as
HITL; trajectory→refined skills. 94.03% LOCOMO, 70.63% PersonaMem.
**→ 3V0:** the operator's stated main goal (memory/retrieval). Adopt: schema evolution via
validation-driven search + conflict-resolving consolidation (the LycheeMemoryV2 lazy-vs-eager thread
from prior review), + corrective-feedback loop into retention.

### 7. VCE-Skill `2608.16544` (08-17) — Version-change experience as evolution prior
Public skill version histories provide reusable evolution priors; fuse them with trajectory evidence.
**→ 3V0:** currently ignores public skill histories; adopt as a prior when evolving skills.

## Secondary (scan)
- **Agent Gym `2608.15591`** (08-16): human-in-the-loop continuous eval/evolution → §5 human anchor.
- **AQuA `2608.12841`** (08-13): recursive evidence→hypothesis improvement loop (research agents).
- **Compete at Every Price Point `2608.16207`** (08-17): agentic evolution over a menu of LLMs → cheap/fast substrate routing; relevant to substrate-scheduler autonomy.
- **Self-evolving network verifiers `2608.11340`** (08-11): the grader/verifier itself evolves.
- **QUMem `2608.16168`** (08-17): query-conditioned user-state memory in LLM agents.

## Cross-cutting design lessons for the ASI self-evolving harness
1. **Harness is the leverage and the curriculum.** What 3V0 can do is shaped by its harness (tools,
   memory seams, control, stopping) AND that harness decides the trajectories it learns from.
   Evolve harness explicitly, with source-traceable, auditable interventions (HELIX/HSI).
2. **Verifier-grounded, self-supervised, cheap** beats self-referential Gödel-machine search (SBCO)
   on cost-effectiveness. 3V0's evolution monitor is already on the right side.
3. **Honest ceiling:** harness/memory/skill evolution cannot exceed the frozen substrate model's
   capability (HSI backbone bound). Self-evolution is bounded without (a) a stronger substrate or
   (b) preference-learning / updating the model itself.
4. **Safety is a lifecycle property** of self-improvement, not static behavior: govern what updates
   write and what executors reuse (misevolution).
5. **Consolidation + corrective feedback** are the memory-schema optimizers; lazy-vs-eager tension
   governs cost (MindMemOS vs LycheeMemoryV2).

## Next-action slate (ranked for 3V0)
- A: Add a **skill-authoring safety/reuse gate** (misevolution) to skill_manage / redo ingestion.
- B: Fold SBCO's "decomposed verifier bank + block-coordinate harness opt" into the evolution monitor
  design doc (probe bank → harness-optimizer, not just grader).
- C: Memory consolidation (MindMemOS "dreaming"): retract/merge superseded facts — partially done via
  add_fact(supersedes); extend to conflict reconciliation.
- D: One-shot redo → harness-skill compilation (Evo-Harness), validated cross-topic.
- E: Note the backbone-capability bound in CUTOVER/roadmap: self-evolution ceiling = substrate model.