---
description: Post-release retrospective. Invoke within 24h after every release of a cycle (GO or NO-GO). Captures what helped, what slowed us down, and ONE action to diffuse into the system.
---

# `/retro` workflow

Specialized adapter of the learning loop for post-release events. For everything else (incident, friction, refactor, blocked candidate), use `/learn`.

## When to invoke

- Within **24 hours** after every release of a cycle.
- Whether the release was GO or NO-GO. A blocked release often produces the most actionable lesson.

## Invocation

```
/retro <YYYY-MM-DD>
```

Where `<YYYY-MM-DD>` is the date of the release of cycle.

## Steps

### 1. Load the cycle context

- The release doc of the cycle (e.g. `docs/RELEASE_CYCLE_<YYYY-MM-DD>.md` if you keep one) — or the merge commit / tag.
- `STATUS_APP.md` for current axes and known debt.
- The last `/learn` files in `docs/learn/` — to avoid restating already-diffused lessons.

### 2. Draft the retrospective

Template, target ≤ 30 lines:

```markdown
# Retro — Cycle <YYYY-MM-DD>

- Outcome: GO | NO-GO | partial
- Release: <sha or tag>

## What helped
- <2–4 concrete bullets — moves that made the cycle work>

## What slowed us down
- <2–4 concrete bullets — frictions, blockers, surprises>

## One action retained
> <imperative, present tense, under 20 words>

Lands in: <target artefact — AGENTS.md / WORKFLOW.md / a capsule / a pattern / a rule / STATUS_APP.md / a runbook>
```

### 3. Validate with the user

Confirm factual accuracy, the action retained, and the landing destination **before** diffusing anything.

### 4. Diffuse

Edit exactly **one** target artefact. Minimal — one action, one diff.

### 5. Write the trace

Create `docs/retro/RETRO_CYCLE_<YYYY-MM-DD>.md` with the draft above, plus:

```markdown
## Diffusion
- <file changed> — <one-line description>
```

### 6. Run the validator

```
python scripts/validate_agent_context.py
```

If the validator reports new warnings or errors, fix them or document an explicit exception in `_local/CI_RULEBOOK.md`.

### 7. Conclude in 3 lines

- What was created or updated (include the `RETRO_CYCLE_*.md` filename).
- The action retained and its destination.
- The next moment a `/retro` (or `/learn`) is worth running.

## Hard constraints

1. **One action only.**
2. **The action lands in an executable artefact.** A `RETRO_*.md` alone does not count.
3. **The output file is ≤ 30 lines.**

## What `/retro` is NOT for

- A single friction outside a release → `/learn friction`.
- An incident postmortem → `/learn incident` + a dedicated runbook entry.
- An architectural choice → write an ADR (`docs/adr/ADR-<N>-<slug>.md`).
- A celebratory write-up → keep it in your team channel.
