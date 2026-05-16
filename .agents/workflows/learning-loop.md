# `/learn` workflow

Capture and diffuse actionable lessons from frictions, refactors, incidents, or no-go candidates. The single mechanism that lets this harness *improve itself* outside of releases.

For post-release retrospectives, use `/retro` instead (`.agents/workflows/retro.md`).

## Why per-event, not a rolling log

A single growing `friction-log.md` accretes without forcing a decision. Per-event files with a strict "one action retained" constraint force triage and diffusion. The log is a side-effect; the **diffusion** is the value.

## Invocation

```
/learn <family> <short-slug>
```

| Family | Use for |
|---|---|
| `friction` | A recurring dev / agent friction (same mistake twice or more) |
| `incident` | Production or runtime issue requiring post-hoc explanation |
| `refactor` | A meaningful refactor that revealed a procedure worth capturing |
| `candidate` | A release candidate blocked or rejected |

For a release of a cycle (GO or NO-GO), use `/retro <YYYY-MM-DD>` instead.

## Output: one short file at `docs/learn/LEARN_<family>_<slug>_<YYYY-MM-DD>.md`

Use this exact template. Keep it under 40 lines total.

```markdown
# Learning Loop — <short title>

- Family: friction | incident | refactor | candidate
- Date: <YYYY-MM-DD>
- Source: <file / ticket / event that triggered this>

## What helped
- <2–4 concrete bullets>

## What slowed us down
- <2–4 concrete bullets>

## One action retained
> <imperative, present tense, under 20 words>

Lands in: <target artefact — e.g. AGENTS.md, a capsule, a pattern, a rule, a project skill>

## Diffusion
- <file changed> — <one-line description of the change>
```

## Hard constraints

1. **One action only.** If multiple actions seem necessary, pick the one that most reduces recurrence. Defer the others.
2. **The action must land somewhere executable.** Updating `AGENTS.md` counts. Updating a capsule counts. Writing a new pattern counts. Adding a rule counts. A `LEARN_*.md` file alone does not count — it's the audit trail.
3. **The output file is ≤ 40 lines.**

## Steps

1. **Qualify the event.** Choose the family. State in one sentence what triggered the `/learn`.
2. **Draft the four blocks.** What helped, what slowed us down, the one action, where it lands.
3. **Validate with the user.** Confirm factual accuracy, the action retained, and its landing place. Do not diffuse without confirmation.
4. **Diffuse.** Edit the target artefact. Minimal — one action, one diff.
5. **Write the trace.** Create `docs/learn/LEARN_<family>_<slug>_<YYYY-MM-DD>.md` with the template above, including the `Diffusion` section.
6. **Run the validator.** `python scripts/validate_agent_context.py`. The diffusion must not break the harness's internal coherence.
7. **Conclude in 3 lines.** What was created or updated; the action retained and its destination; the next moment a `/learn` is worth running.

## What this workflow is NOT for

- Post-release retrospectives → use `/retro`.
- Documenting architectural choices → write an ADR under `docs/adr/`.
- Tracking tech debt → goes in your tracker, not here.

## Promotion criteria for emerging artefacts

- A `/learn friction` that lands in `AGENTS.md` three times on the same theme → promote to a capsule or pattern.
- A `/learn refactor` that documents a recurring procedure → write a pattern in `.agents/patterns/`.
- A `/learn incident` that reveals a new technical convention → add a rule in `.agents/rules/`.
