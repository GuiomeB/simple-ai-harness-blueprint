# CI / Agent Rulebook — local notes (gitignored)

> **This file is local and not committed.** Add `_local/` to your `.gitignore`.
> Its purpose is to preserve the *rationale* of CI and agent infrastructure
> choices that would otherwise live in your head.

This is the place to write down:

- Why your CI is structured the way it is (which jobs gate, which signal, which are optional).
- Why you chose specific risk-rail thresholds and CODEOWNERS paths.
- Which agents are in the loop, which files they read, which workflows triggered their adoption.
- Decisions that didn't warrant a full ADR but you don't want to lose.
- Exceptions you've granted (e.g. "validator warning W is expected on file X because of legacy reason Y, revisit by date Z").

## Structure (suggested)

```markdown
## CI architecture

<What jobs run, in what order, what gates what. Budget notes — minute consumption, cache strategies.>

## Agent ecosystem

| Agent | Config file | Reading status | Notes |
|---|---|---|---|
| Claude Code | CLAUDE.md | active | <how it's used in this repo> |
| Codex CLI | AGENTS.md | active | <how it's used> |
| ...  |  |  |  |

## Risk rail / CODEOWNERS rationale

<Why these paths are critical. Why others were considered but excluded.>

## Validator exceptions

<Warnings you accept, with reason and revisit date.>

## Maintenance log

<Append-only log of when you updated CI, what you changed, and why. One line per change.>
```

## Why this file is not in the repo

The information here is *operational* and *opinionated*. It's useful to you but:

- It would clutter the public-facing repo for users who just want to apply the blueprint.
- It often contains environment-specific notes (your CI minutes budget, your team's preferences) that don't generalize.
- It evolves much faster than the rest of the blueprint and would create noise in commit history.

If a rule documented here becomes universal enough to share with all contributors, promote it to `WORKFLOW.md` or an ADR.

## Periodic review

Skim this file every 1–2 months. Items that are stale (the exception no longer applies, the rationale is now in an ADR) can be deleted. Items that have grown into real procedures can be promoted to patterns or rules.
