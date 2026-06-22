---
description: The /loop workflow — the L+ autonomous-execution profile. Opt-in, ADR-gated. Turns a unit of work into a self-driving loop with hard brakes. NOT a default. The agent only enters this mode when explicitly activated.
---

# `/loop` workflow (L+ profile only)

A loop is a *unit of work* that runs, checks itself, and decides the next step —
not a cron job (fixed script) and not the default interactive mode. It is the
operational form of **M0** running unattended. **Activation is explicit and
opt-in.** Outside an activated loop, the default posture holds: clarify, small
diff, local validation (Karpathy rule 1).

## Preconditions (do not start a loop without all of these)

1. **A trigger** — what starts the loop (a failing CI run, a PR opening, a
   schedule, a Slack message, a manual command).
2. **A verifiable goal** — a deterministic stop signal (tests pass + CI green),
   or a reviewer-model check against a written spec. No verifiable goal → no loop,
   just a confident token furnace.
3. **The L+ promotion criteria are met** (see `AGENTS.md §Autonomy profile`) and
   an ADR records the decision to run autonomously.

## The three hard brakes (mandatory — a loop without these is forbidden)

- **Budget.** A ceiling on iterations *and* tokens/$ *and* wall-clock. Hitting any
  ceiling stops the loop.
- **No-progress detection.** If N consecutive iterations don't move the verifiable
  signal, stop. Looping without progress is the failure mode, not the goal.
- **Kill-switch.** A single explicit stop the human (or an out-of-band check) can
  trip at any time. The loop checks it every iteration.

## Loop shape

1. **Read state.** Yesterday's CI failures, open issues, recent commits, the loop's
   own state file. Cheap, read-only.
2. **Pick the next action** toward the verifiable goal. One action.
3. **Do it** in an isolated worktree / branch. Never on `main`.
4. **Verify** — run `python scripts/validate_agent_context.py`; invoke the
   `harness-reviewer` subagent (`.claude/agents/harness-reviewer.md`, read-only,
   the coder is not the judge).
5. **Decide.** Goal met → open a PR (push to `main` is hook-deferred for human
   approval) and stop. Not met but progressing → iterate. Not progressing, or a
   brake tripped → **stop and put the problem in the human's inbox.**
6. **Record.** Write the loop's assumptions and outcome to its state file. If a
   reusable lesson emerged, queue a `/learn`.

## Verification is stronger than "the agent says it's done"

Run tests. Typecheck. Use the reviewer subagent. Compare the diff to the spec. In
this profile a claim is not done until something *checks* it — that something is
M0 plus the reviewer, never the coder's own say-so.

## When NOT to loop

- The task is one-off → just prompt.
- The goal is vague or exploratory ("find a better product strategy") → a loop will
  optimise toward a vague sentence and waste budget. Sharpen the goal first.
- Any hard brake is missing → do not start.

## Reference

- `AGENTS.md §Autonomy profile` — promotion criteria, budgets, kill-switch.
- `AGENTS.md` M0 — the verification mechanism this loop runs unattended.
- `.github/workflows/<headless-loop>.yml` — the headless runner template.
