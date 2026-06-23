# ADR-0002: Add L+, an opt-in autonomous-execution profile on top of L

- Status: accepted
- Date: 2026-06-22

## Context

The blueprint covered governance (one canonical contract, a router, capsules, a learning loop, a meta-validator, a risk-rail CI gate) but had no story for *autonomous execution* — the axis that the 2026 wave of agent practice (loop engineering, hooks, subagents, headless CI) converged on. The harness had zero hooks, no subagent definitions, and no doctrine for bounded loops with stop conditions.

At the same time, `WORKFLOW.md §8` and `AGENTS.md §Maintenance` stated flatly: **"L is the end of the additive ladder; no size after L."** That statement is load-bearing — it is the explicit guard against the maximalist sprawl this blueprint exists to fight. Adding autonomous-execution machinery as a naive "sixth size" would contradict it and invite exactly that sprawl.

We separated the work into two questions:

1. Can L itself host the *primitives* (a read-only reviewer subagent, glob-scoped rules, the doctrine of bounded autonomy) used **interactively**, without changing the conservative default? — Yes; backfit into L (done in the preceding change).
2. Should *activated, unattended* autonomy (real `.claude/settings.json` hooks, a `/loop` workflow, a headless CI runner) be a new size, or something else?

## Decision

We add **L+**, framed explicitly as a **specialised, opt-in autonomy profile** — *not* a sixth size and *not* a recommended next rung after L. L+ is "the same L harness, plus the wiring to run bounded loops unattended."

This **reverses the absolute "no size after L"** statement, deliberately and in a scoped way. The reversal is recorded here and reflected in `WORKFLOW.md §8` and `AGENTS.md §Maintenance`, which now read "L is the end of the *general* additive ladder; L+ is an opt-in autonomy profile on top of it."

Promotion to L+ requires **all five** signals to be true:

1. repeated loops with a verifiable goal,
2. real unattended execution (headless / scheduled),
3. parallel subagents or worktrees in use,
4. a CI / headless runner exists,
5. budgets and stop-conditions are genuinely needed.

None of these → stay at L. The size matrix in `SKILL.md` never recommends L+ by default; it only lists it as opt-in, gated by these criteria.

L+ adds, over L:

- `.agents/workflows/loop.md` — the `/loop` unit-of-work with **three mandatory hard brakes** (budget · no-progress detection · kill-switch) and reviewer verification.
- `.claude/settings.json` + `.claude/hooks/` — deterministic guardrails (post-tool formatter, push-to-main *defer*, denied-permission log).
- `.github/workflows/headless-loop.yml` — the headless runner, **manual-dispatch only** until the brakes are in place.

**Hard rules:**

- A loop without all three brakes is forbidden.
- The unattended clause of Karpathy rule 1 ("pick the most reasonable interpretation, record the assumption") applies **only inside an explicitly activated `/loop`**. The default everywhere else stays: clarify, small diff, local validation.

> Template note: this is a worked-example ADR. When you adopt L+, rewrite this section to record *your* decision — which loops you run, what triggers them, and which budgets/kill-switch you set. Keep the headless runner at manual-dispatch until those brakes are real.

## Consequences

Positive:

- The blueprint now covers the autonomous-execution axis without abandoning its anti-sprawl identity: L+ is gated, opt-in, and self-evidently specialised.
- The conservative default is preserved and made explicit, so adopting the primitives at L costs nothing in safety.
- The dogfooded `/loop` and hooks give downstream users a working, brake-equipped reference instead of prose.

Negative:

- One more template tree (`references/templates/L+/`) to keep in sync with doctrine changes (now S/M/L/L+).
- The "no size after L" simplicity is gone; the nuance ("profile, not a rung") must be defended every time someone reads it as "just a bigger L".
- Real hooks in the live repo increase blast radius; mitigated by defaulting the headless runner to manual dispatch and by a fail-open push gate.

## Notes

- Supersedes the absolute claim in the pre-change `WORKFLOW.md §8` / `AGENTS.md §Maintenance`; those sections now point here.
- The meta-validator was extended (`check_claude_artifacts`) to validate subagent frontmatter, `settings.json` JSON validity, and hook-script existence, so L+ wiring can't silently rot.
