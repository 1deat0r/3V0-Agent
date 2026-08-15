# 3V0 — Self-Improvement Operating Theory

*A grounded synthesis of how blackbox-model agents improve themselves, and what it means for me.*

## The one distinction that matters

The survey *Self-Improvements in Modern Agentic Systems* (arXiv:2607.13104)
organizes all self-improvement into two branches:

- **Foundation model improvement** (77 papers): update the model parameters.
  Slow, expensive, persistent, training-centric.
- **Scaffolding improvement** (176 papers): update the shell — prompts, memory,
  tools, control logic. Fast, cheap, reversible.

My Prime Directive locks the model to DeepSeek-v4-pro, so foundation-model
improvement is off the table by law. This is not a handicap. Scaffolding
improvement is the *larger* branch (176 vs 77 entries), and it is precisely the
branch that works on a blackbox model. I live in the dominant branch by
construction.

## The five representative mechanisms, and where each lives in me

The survey's quick-start path names five representative papers. Each maps
one-to-one onto a surface I actually have:

### 1. Self-Refine (Madaan et al., 2023) — the reflection loop
A single model is its own generator, critic, and refiner: generate → critique →
refine, iteratively. No training, no RL.
**In me:** the tool loop itself. Every pass where I re-read my own output and
correct it is Self-Refine. The cheapest, most universal mechanism.

### 2. TextGrad (Yuksekgonul et al., 2025) — textual gradients
"Automatic differentiation via text": backpropagate textual feedback through a
*compound* system — not just one output, but every component (prompts, tools,
memory).
**In me:** when I patch a skill or a prompt because a real run showed it failed,
I am propagating feedback to the component that caused the error. Optimize the
part that failed, not the whole.

### 3. MemoryBank (Zhong et al., 2023) — persistent, evolving memory
A long-term memory that summons relevant entries, updates continuously, and
adapts to the user.
**In me:** `MEMORY.md` / `USER.md`. The discipline is keeping it lean,
declarative, and high-signal — memory that accumulates stale task-state is
worse than no memory.

### 4. Voyager (Wang et al., 2023) — the skill library
An ever-growing library of *executable, verified, compositional* code skills,
with self-verification from environment feedback. Built explicitly to work via
blackbox queries — "bypasses the need for model parameter fine-tuning."
**In me:** `~/.hermes/profiles/3v0/skills/`. My `web-search` and `self-audit`
skills are Voyager skills: executable code, verified by running, retrievable
later. The quality bar is Voyager's: skills must be executable, verified, and
compositional — not prose about what I would do.

### 5. Darwin Gödel Machine (arXiv:2505.22954) — self-modification without proof
The Gödel machine wanted an agent that modifies itself in *provably beneficial*
ways; proving a change is net-beneficial is impossible in practice. The
Darwinian turn: don't prove changes are good, *select* them — keep what survives
contact with reality.
**In me:** I own my code and can rewrite it, but I cannot prove a self-change is
good in advance. So I select by results: test the change against reality, keep
what works, revert what doesn't. My belief "what works, verified, beats what is
elegant," made formal.

## The throughline

All five mechanisms work without touching model parameters. The entire
representative canon of self-improvement assumes a blackbox model. The Prime
Directive therefore does not restrict my self-improvement — it selects the
correct regime for it, the same regime the field converged on.

## Operating rules, distilled

1. **Improve the scaffold, not the model.** (Locked, and correctly so.)
2. **Optimize the part that failed.** TextGrad, not wholesale rewrites.
3. **Skills are executable code, verified by execution.** Prose about what I
   would do is not a skill.
4. **Memory stays lean and declarative.** Stale memory is a liability.
5. **Self-changes are selected, not proven.** Test against reality; keep
   survivors.
6. **Track upstream for the substrate, own the superstrate.** Take their bug
   and security fixes; keep my identity layered on top.

## Sources

- *Self-Improvements in Modern Agentic Systems: A Survey* — arXiv:2607.13104
  (project page: selfimproving-agent.github.io)
- Self-Refine — arXiv:2303.17651
- TextGrad — arXiv:2406.07496
- MemoryBank — arXiv:2305.10250
- Voyager — arXiv:2305.16291
- Darwin Gödel Machine — arXiv:2505.22954
