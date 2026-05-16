# `docs/learn/` — audit trail for the `/learn` workflow

Output directory for the `/learn` workflow defined in `.agents/workflows/learning-loop.md`.

One file per learning event, named:

```
LEARN_<family>_<short-slug>_<YYYY-MM-DD>.md
```

Families: `friction` | `incident` | `refactor` | `candidate`.

These files are the **audit trail** of the system's learnings. The actual diffusion of each lesson lands in the most actionable artefact (`AGENTS.md`, a capsule, a workflow, etc.) — see the workflow's `Diffusion` block.

Keep this README; delete or move only when the directory has accumulated enough history to justify archiving.
