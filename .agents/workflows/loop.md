---
description: The /loop workflow — the L+ autonomous-execution profile. Opt-in, ADR-gated. Turns a unit of work into a self-driving loop with hard brakes. NOT a default. The agent only enters this mode when explicitly activated.
---

# `/loop` workflow (L+ profile only)

A loop is a *unit of work* that runs, checks itself, and decides the next step —
not a cron job (fixed script) and not the default interactive mode. It is the
operational form of **M0** running unattended. **Activation is explicit and
opt-in.** Outside an activated loop, the default posture holds: clarify, small
diff, local validation (Karpathy rule 1).

Contract anchor: `docs/adr/ADR-0003-loop-state-contract.md`.

## Loop readiness check (before preconditions)

Answer all five. Any **no** → do not start a loop; use a one-off prompt instead.

1. **Repeats?** The task runs again (schedule, CI, PR cadence) — not a one-off.
2. **Verifiable?** Done/fail is observable (tests, validator, checklist, reviewer verdict).
3. **Context available?** Files, spec, and tools the loop needs are reachable.
4. **Stop condition clear?** Not "until it looks good" — a concrete PASS/FAIL signal.
5. **Safe review point?** A human can inspect output before irreversible action.

## Preconditions (do not start a loop without all of these)

1. **A trigger** — what starts the loop (a failing CI run, a PR opening, a
   schedule, a Slack message, a manual command).
2. **A verifiable goal** — captured in `docs/loops/<slug>/SPEC.md` (see below).
   No verifiable goal → no loop, just a confident token furnace.
3. **The L+ promotion criteria are met** (see `AGENTS.md §Autonomy profile`) and
   an ADR records the decision to run autonomously.

## Goal spec (`docs/loops/<slug>/SPEC.md`)

Rel-read **every iteration**. Copy this skeleton when opening a new loop:

```markdown
# Loop spec — <slug>

## Goal

## Done when        (verifiable signals, PASS/FAIL)

## Never touch      (forbidden paths/actions)

## Stop if          (immediate halt conditions)

## Budget           (iterations · tokens · wall-clock)

## Permission level (1–6, cf. §Permission ladder)
```

## State file (`docs/loops/<slug>/STATE.md`)

Operational memory between runs. Copy this skeleton:

```markdown
# Loop state — <slug>

## Current State    (status · focus · last updated)

## Last Run         (date · trigger · summary · files touched)

## Last Verification (PASS/FAIL · failed checks · action taken)

## Blockers

## Needs Human Review

## Next Run Should

## Do Not Repeat    (failed actions — do not retry)
```

**Hard contract:**

1. A run is **not complete** until STATE.md is updated.
2. Verification failures are **written** to STATE (silent failure is the bug).
3. STATE.md stays ≤ 60 lines; detailed history → `docs/loops/<slug>/reports/`.
4. Same blocker two consecutive runs → escalate to human review; do not retry blindly.

## Permission ladder

Six levels — record the active level in SPEC.md. New loops start at **≤ 2**.

| Level | Scope |
|---|---|
| 1 | Read-only analysis — inspect, summarize, no writes beyond STATE/reports |
| 2 | Draft outputs — write reports/plans under `docs/loops/<slug>/` or `outputs/` |
| 3 | Sandbox edits — modify files only in an isolated worktree/branch |
| 4 | Draft external actions — draft PR, draft ticket comment; no publish |
| 5 | Human-approved writes — apply after explicit approval |
| 6 | Automated low-risk writes — narrow scope, logged, rollback path exists |

Promotion: after **three stable runs** at the current level, a human may bump
the level in SPEC.md. Demote immediately on any boundary violation.

Sensitive-data policy: `.agents/rules/sensitive-data.md`.

## Scheduled run policy

When a loop runs on a schedule (including `/loop` in Claude Code):

- **Quiet mode** — no meaningful change → short STATE update; optional one-line report.
- **Attention mode** — change, failure, or review needed → full report + flag in
  `Needs Human Review`.
- Same blocker twice in a row → escalate; do not keep retrying.
- Verification fails twice in one run → mark run not accepted; stop.

## The three hard brakes (mandatory — a loop without these is forbidden)

- **Budget.** A ceiling on iterations *and* tokens/$ *and* wall-clock. Hitting any
  ceiling stops the loop.
- **No-progress detection.** If N consecutive iterations don't move the verifiable
  signal, stop. Looping without progress is the failure mode, not the goal.
- **Kill-switch.** A single explicit stop the human (or an out-of-band check) can
  trip at any time. The loop checks it every iteration.

## Loop shape

1. **Read state.** Read `docs/loops/<slug>/SPEC.md` and `STATE.md`; then cheap
   context (CI, issues, recent commits). Read-only.
2. **Pick the next action** toward the verifiable goal. One action.
3. **Do it** in an isolated worktree / branch. Never on `main`.
4. **Verify** — run `python scripts/validate_agent_context.py` when the harness
   is touched; invoke the `harness-reviewer` subagent
   (`.claude/agents/harness-reviewer.md`, read-only, the coder is not the judge).
5. **Decide.** Goal met → open a PR (push to `main` is hook-deferred for human
   approval) and stop. Not met but progressing → iterate. Not progressing, or a
   brake tripped → **stop and put the problem in the human's inbox.**
6. **Record.** Update `STATE.md` with assumptions, verification result, and next
   step. If a reusable lesson emerged, queue a `/learn`.

## Verification is stronger than "the agent says it's done"

Run tests. Typecheck. Use the reviewer subagent. Compare the diff to SPEC. In this
profile a claim is not done until something *checks* it — M0 plus the reviewer,
never the coder's own say-so.

## When NOT to loop

- The task is one-off → just prompt.
- The goal is vague or exploratory ("find a better product strategy") → sharpen
  the goal first.
- Any hard brake is missing → do not start.
- Loop readiness check failed → do not start.

## Reference

- `docs/adr/ADR-0003-loop-state-contract.md` — spec/state contract.
- `AGENTS.md §Autonomy profile` — promotion criteria, budgets, kill-switch.
- `AGENTS.md` M0 — the verification mechanism this loop runs unattended.
- `.github/workflows/headless-loop.yml` — headless runner (manual-dispatch only).
