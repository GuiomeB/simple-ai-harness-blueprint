# `/learn` workflow

Capture and diffuse actionable lessons from frictions, refactors, incidents, or releases. The single mechanism that lets this harness *improve itself*.

## Why per-event, not a rolling log

A single growing `friction-log.md` accretes without forcing a decision. Per-event files with a strict "one action retained" constraint force triage and diffusion. The log is a side-effect; the **diffusion** is the value.

## Invocation

```
/learn <family> <short-slug>
```

| Family | Use for |
|---|---|
| `friction` | A recurring dev / agent friction (the same mistake twice or more) |
| `incident` | Production or runtime issue requiring post-hoc explanation |
| `refactor` | A meaningful refactor that revealed a procedure worth capturing |
| `release` | A release cycle (use this when no dedicated `/retro` is set up yet) |
| `candidate` | A release candidate blocked or rejected |

## Output: one short file at `docs/learn/LEARN_<family>_<slug>_<YYYY-MM-DD>.md`

Use this exact template. Keep it under 40 lines total.

```markdown
# Learning Loop — <short title>

- Family: friction | incident | refactor | release | candidate
- Date: <YYYY-MM-DD>
- Source: <file / ticket / event that triggered this>

## What helped
- <2–4 concrete bullets>

## What slowed us down
- <2–4 concrete bullets>

## One action retained
> <imperative, present tense, under 20 words>

Lands in: <target artefact — e.g. AGENTS.md, WORKFLOW.md, an existing capsule, etc.>

## Diffusion
- <file changed> — <one-line description of the change>
```

## Hard constraints

1. **One action only.** Not two, not three. If multiple actions feel necessary, pick the one that most reduces the chance of recurrence. Save the others for next time.
2. **The action must land somewhere executable.** Updating `AGENTS.md` counts. Updating a `.agents/context/*.md` capsule (at M+) counts. Writing a new pattern (at L) counts. A `LEARN_*.md` file alone does not count — it's only the audit trail.
3. **The output file is < 40 lines.** If you can't say it in 40 lines, you don't yet understand the action.

## Steps

1. **Qualify the event.** Choose the family. State in one sentence what triggered the `/learn`.
2. **Draft the four blocks.** What helped, what slowed us down, the one action, where it lands.
3. **Validate with the user.** Confirm factual accuracy, the action retained, and its landing place. Do not diffuse without confirmation.
4. **Diffuse.** Edit the target artefact. Keep the edit minimal — one action, one diff.
5. **Write the trace.** Create `docs/learn/LEARN_<family>_<slug>_<YYYY-MM-DD>.md` with the template above, including the `Diffusion` section listing files actually changed.
6. **Conclude in 3 lines.**
   - what was created or updated (include the `LEARN_*.md` filename)
   - the action retained and its destination
   - the next moment a `/learn` would be worth running

## What this workflow is NOT for

- Writing a long retrospective narrative — that's `/retro` at size M+.
- Documenting architectural choices — that's an ADR (`docs/adr/`) at L.
- Capturing tech debt — that goes in your tracker, not here.

## At M and L

- At M, `.agents/workflows/retro.md` is added for post-release retrospectives. Use `/retro` for releases and `/learn` for everything else.
- At L, a `validate_agent_context.*` script runs after every diffusion to ensure the system's internal coherence is preserved.
