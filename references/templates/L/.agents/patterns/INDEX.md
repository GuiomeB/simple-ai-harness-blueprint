# Patterns INDEX

Registry of patterns ↔ pivot files in the codebase. For task-family routing (which pattern when), see `.agents/ROUTER.md`. This index serves the inverse lookup: "I'm editing file X — is there a pattern for it?"

The validator script (`scripts/validate_agent_context.py`) checks that every `.md` file under `.agents/patterns/` (except `INDEX.md`) is referenced here, and vice versa.

## Patterns shipped with this template

| Pattern | Pivot files in the codebase | Pattern shape |
|---|---|---|
| [`change-critical-zone.md`](./change-critical-zone.md) | files flagged CRITICAL in `AGENTS.md §Critical zones` | execution (protocol for editing dangerous code) |
| [`review-parallel-ticket.md`](./review-parallel-ticket.md) | any PR authored by another agent on a parallel ticket | process (cross-agent review beyond clean diff) |
| [`spike-with-revisit-thresholds.md`](./spike-with-revisit-thresholds.md) | any architecture choice taken under uncertainty | decision (time-boxed choice with explicit revisit triggers) |
| [`tiered-model-workflow.md`](./tiered-model-workflow.md) | `docs/loops/**`, any multi-agent or tiered handoff run | execution (tier discovery + Definition of Ready) |

## Conventions

- One pattern = one procedure, keyed to **at least one pivot file or one trigger**.
- Hard cap: 120 lines per pattern. If it grows, split or promote a section to a capsule or rule.
- Each pattern includes a "Reusability" note: when to write *another* instance of this kind of pattern vs reuse this one.
- A pattern with no pivot file and no clear trigger is orphan — delete it or rewrite it.

## Adding a new pattern

1. Identify the recurring procedure (≥ 2 occurrences in real work).
2. Identify the pivot file(s) or trigger(s).
3. Write the pattern (≤ 120 lines) following the shape of an existing one.
4. Add a row to this INDEX with the pattern, pivots, and shape.
5. Run `python scripts/validate_agent_context.py` to verify the registration.
6. If the pattern routes from a specific task family, add a row in `.agents/ROUTER.md`.

## Removing a pattern

- If a pattern hasn't been touched in 3 months and its procedure has been absorbed into product code (linters, generators, base components), retire it.
- Document the retirement in `_local/CI_RULEBOOK.md` (gitignored) so the rationale survives.
- Run the validator to catch dangling references.
