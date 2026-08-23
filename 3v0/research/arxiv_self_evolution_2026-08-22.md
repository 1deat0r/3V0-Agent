# arXiv self-evolution research digest — 2026-08-22
Freshest arXiv crawl reachable: 2026-08-20. Supersedes the 08-19 digest (which capped at 08-17);
this file covers papers landed **after** 08-17 that the prior digest had not yet seen. All citations
dated; v1 preprints (unreviewed).

> **READ `indep_review_2026-08-22.md` LAST.** It is the independent re-check of this digest against
> the actual codebase and **overrides the action slate below** (several "musts" were already built,
> and one recommendation — Task-CoEvolve adaptive selection — conflicts with the frozen-bank
> invariant). Read that judgment, not just these kernels, before acting.

## Eight fresh kernels mapped to 3V0

### 1. Phantom Gains `2608.20290` (08-20) — auditing self-improvement against a MEASURED NULL
Improvement is now judged by problem-level gain/loss transitions, which means differencing two noisy
estimates → artifact-prone. Seven measurement failures identified, several standard practice, ALL
visible when a frozen control runs through the identical pipeline but invisible without it: single
greedy-decoding ledgers manufacture capability changes on an *untrained* model (inference-batching
artifact); a "sharpening vs acquisition" expansion statistic gave an untrained model a 0.280 rate;
threshold repairs did not replicate across the frozen comparisons.
**→ 3V0 (MUST adopt before trusting any self-evolution claim):** every evaluation of
memory/skill/harness changes needs a frozen-baseline control run through the SAME pipeline, and
noise-aware transition counts (not naive diff of noisy estimates). This is the correct prior for the
background-review fork + curator: measure gains/losses against a control, not in isolation. Directly
hardens 3V0's claim to genuine (not phantom) self-evolution.

### 2. On the Fragility of Self-Improving Agents `2608.18066` (08-18) — variance + task order
Re-evaluation of memory-based self-improving agents (textual memory bank improved over an online task
stream): (a) eval is inherently noisy on complex/multi-step tasks and the self-improving loop
amplifies that noise; (b) improvement is highly task-order dependent; (c) methods are underspecified
(as from which run/prompt/order a number was reported). Prior works report default (favorable) orders.
**→ 3V0:** adopt multi-run variance + shuffled-task-order reporting in all memory/skill experiments;
treat a single-run number as unfalsifiable. Complements §1: fix the measurement, then audit against a
null.

### 3. Task-CoEvolve `2608.20169` (08-20) — harness optimization via ADAPTIVE validation-task selection
Harness iteration rewrites harness code from validation performance; cost is evaluation of a fixed set
every round, even for tasks that stop being discriminative as the harness evolves. Co-evolve
validation tasks with the harness: tasks where candidate harnesses DISAGREE are most informative;
estimate full-set performance from partial evals. Substantial eval-cost reduction without losing
selection quality.
**→ 3V0:** the probe-bank / hold-out-bank in the evolution monitor should be *adaptive*, not static —
feature tasks the candidate harness variants disagree on, and subsample once tasks become consistently
solved. Directly cuts the cost curve of SBCO-style harness opt (§B of the 08-19 slate).

### 4. Optimal Skill Selection, provable bicriteria `2608.19993` (08-20) — skill/token-budget packing
Skill selection is a first-order determinant of performance AND token cost, yet current agents score
skills by semantic relevance and pack top-k/greedy with no quality/cost guarantee — redundant or poor
skills waste context and can degrade. Casts it as monotone submodular benefit minus context penalty
under a hard token budget; BPS algorithm with provable bicriteria guarantees (near-optimal benefit,
strict token bounds).
**→ 3V0:** apply to skill_manage/context packing — a provable guarantee that the *set* of loaded
skills is the right one under a hard prompt-cache-budget, instead of naive top-k. Ties into the
prompt-cache-scope and TOKEN_EFFICIENCY invariants: skill selection should be budget-aware AND
provably near-optimal.

### 5. SkillGate `2608.18852` (08-19) — training in-policy skill SELECTION (selector credit starvation)
Which skill to read is now a policy decision mid-episode, but no existing signal trains it; RL over the
candidate slate fails a structural problem: selector credit starvation — under broadcast sequence-level
advantage, the few tokens naming the chosen skill get vanishing and increasingly wrong-signed credit
as trajectories lengthen; a correct choice is punished whenever subsequent execution fails.
**→ 3V0:** illustrates WHY naive outcome-signaling on skill choice mis-trains; when 3V0 moves toward
RL-tuned skill selection it must give the selector its own credit path (e.g., counterfactual credit,
not shared trajectory advantage). Relevant for the skill-authoring/selection loop.

### 6. SkillForge `2608.18933` (08-19) — self-distill project-specific skills from the REPO ITSELF
Self-evolving agents lack project-specific knowledge; existing approaches depend on historical
issue-resolution signals or costly per-issue test-time exploration. SkillForge synthesizes
project-specific issues by re-implementing test-covered core functionality of the repo, resolves those,
and distills reusable project-specific skills — proactive, no waiting for real issues, no per-issue
cash.
**→ 3V0:** matches 3V0's own project (repo is 3V0's to evolve); adopt "synthesize issues from the
repo's core + tests, resolve, distill" for project-specific skill acquisition across the 3V0 codebase —
without burning real persona issues.

### 7. Cross-Task Skill Transfer `2608.20274` (08-20) — task-level vs subtask-level, text vs code
Controlled study of how skill induction shapes transfer: task-level skills mostly REDUCE performance
below no-memory baseline; subtask-level skills raise it; text skills transfer better than code skills.
The study analyzes two complementary properties — specificity and how well a skill's preconditions
match where it is retrieved (see paper). Strong caution against naive "skill from a finished task"
reuse.
**→ 3V0:** when compiling redo/skills (Evo-Harness path and SkillForge), favor SUBTASK-granularity
induction and text (natural-language) representation over whole-task / code skills — else risk net
negative transfer. Directly informs §D of the 08-19 slate (one-shot redo → harness-skill compilation).

### 8. Beyond Memory Majority: Latent-Source Reasoning `2608.19701` (08-20) — multi-agent memory arbitration
**→ 3V0:** multi-agent/subagent memory arbitration; relevant to delegation_context and the
curator/background_review forks disagreeing on a fact — simple majority over sources is
inadequate; reason about the latent source/relational structure.

## Secondary (scan)
- **AI4AI-Bench `2608.20318`** (08-20): benchmark for recursive self-improvement in algorithmic design.
- **Inducing Task Models `2608.20319`** (08-20): recover task models from computer-use traces —
  relevant to browser-agent trajectory learning.
- **MidTool `2608.20314`** (08-20): mid-training data synthesis for agentic tool use.
- **EnvHarness `2608.19880`** (08-20): awakening static worlds for agent learning (more learning signal).
- **Governance Records as Supervision `2608.18324`** (08-18): verifier-selected self-training for
  structured workflow repair — evidence-records → training signal.
- **ComponentBench `2608.18307`** (08-18): diagnosing component-level failures in computer-use agents.
- **StagedWorkspace `2608.18050`** (08-18): versioned workspace for knowledge-work agents —
  source-intent preservation (ties to FACET).
- **HarnessRisk `2608.17597`** (08-18): lifecycle-oriented benchmark for agent-harness SAFETY.
- **Agent Lightning v1.0 `2608.17528`** (08-18): harnessed agentic RL at speed.
- **LEGO-RL `2608.17393`** (08-18): harness-native RL for coding agents.
- **Wuying-Browser-Agent `2608.17319`** (08-18): fundamental long-horizon browser agents (real-world
  centric) — relevant to the browser substrate.
- **FACET `2608.18580`** (08-19): preserving source intent + executable state across terminal task synthesis.
- **Governance at the Boundary `2608.16055`** (08-17): agent decomposition degrades policy compliance —
  a safety/oversight boundary cost of subagents.
- **Obedience to Authority `2608.16177`** (08-17): measuring LLM obedience in the Milgram paradigm —
  a caution for 3V0's own governance/control seams.
- **D²ACCI `2608.17756`** (08-18): dual-loop diagnostic protocol for evidence-preserving agent memory.
- **StateFuse `2607.05844`** (07-07): deterministic conflict-PRESERVING memory for multi-agent systems —
  complements MindMemOS conflict-resolution (retract/merge vs preserve-both).
- **Optimal Skill Selection provable (BPS)** → §4; **Phantom Gains** → §1.

## Cross-cutting design lessons (delta on the 08-19 set)
1. **Measurement first, claims second.** The single most transferable fresh lesson: none of 3V0's
   self-evolution claims are trustworthy without (a) a frozen control through the identical pipeline
   and (b) noise-aware, order-aware reporting. Phantom Gains + Fragility are the two must-reads.
2. **Harness optimization should co-evolve its validation tasks** (Task-CoEvolve) and pick informative
   (currently-disagreeing) tasks, not a static set — cheap and more discriminative.
3. **Skill selection is a budgeted optimization, not top-k ranking** (provable). And transfer favors
   SUBTASK granularity + text over whole-task + code — a concrete guard against net-negative reuse.
4. **Skills/self-improvement can look great and be an artifact** — synthesize-from-repo is the
   cheap way to get project-specific skills without burning real issues (SkillForge).
5. **Selector credit starvation** warns that RL-based skill/selector training shares credit
   pathologically; give the selector its own counterfactual credit.

## Next-action slate (delta ranked for 3V0)
- **F1 (do now):** add a measured-null control + noise-aware diff to the evolution monitor /
  background-review before further self-evolution claims. (Phantom Gains)
- **F2:** report variance + shuffled task order + underspecification for memory/skill experiments.
  (Fragility)
- **F3:** make the probe/hold-out bank adaptive: prefer tasks candidate harness variants disagree on;
  subsample once consistently solved. (Task-CoEvolve)
- **F4:** skill compilation favors SUBTASK text skills over whole-task code; guard skill_manage against
  net-negative transfer. (Cross-Task Transfer + SkillForge; sharpens 08-19 §D/Evo-Harness)
- **F5:** budget-aware provable skill packing rather than top-k/greedy under the prompt-cache bound.
  (Optimal Skill Selection)
- **F6:** distil project-specific skills by synthesizing repo-core+test issues, resolve, distill.
  (SkillForge — very aligned with 3V0 owning its own repo)
- **F7:** if/when RL-tuning skill selection, use counterfactual selector credit, not trajectory
  advantage. (SkillGate)