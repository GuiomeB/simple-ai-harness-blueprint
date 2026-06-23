# Architecture Decision Records

Short, dated records of decisions that change a load-bearing assumption of the project.

## When to write an ADR

Write an ADR for any decision that:

- changes a load-bearing assumption (auth strategy, data flow, deployment topology),
- affects more than one critical zone,
- introduces or removes a non-bypassable rule,
- adopts or retires a library that's central to the system,
- is taken under significant uncertainty and needs a revisit threshold (use `.agents/patterns/spike-with-revisit-thresholds.md`).

Don't write an ADR for routine implementation choices, code style, or anything reversible in a single commit.

## File naming

```
docs/adr/ADR-<NNNN>-<short-slug>.md
```

- `<NNNN>` is a zero-padded sequential number starting at `0001`.
- `<short-slug>` is kebab-case, ≤ 6 words.

## Statuses

| Status | Meaning |
|---|---|
| `proposed` | Drafted but not yet committed to. May be open for discussion. |
| `spike` | Time-boxed decision with revisit thresholds. See the spike pattern. |
| `accepted` | The decision is in effect. |
| `superseded by ADR-<N>` | A later ADR replaces this one. The new ADR cites this one. |
| `deprecated` | The decision no longer applies but is preserved for historical context. |

## Minimum template

```markdown
# ADR-<NNNN>: <slug>

- Status: proposed | spike | accepted | superseded by ADR-<N> | deprecated
- Date: <YYYY-MM-DD>

## Context

<2–4 paragraphs. What forces are at play? What constraints? What was tried before?>

## Decision

<One paragraph. The choice made, in active voice.>

## Consequences

<2–4 bullets. Both positive and negative. What becomes easier? What becomes harder?>
```

For a `spike` ADR, add Revisit thresholds, Fallback, and a Revisit-by date — see `.agents/patterns/spike-with-revisit-thresholds.md`.

## Hygiene

- One decision per ADR. If you find yourself writing a second decision, write a second ADR.
- ADRs are append-only as a corpus, but individual ADRs can be edited until they reach `accepted` status. After `accepted`, edits are restricted to clarifications and superseding.
- Reference ADRs from `AGENTS.md`, capsules, or patterns when the doctrine you're documenting traces back to a specific decision.
- Run `python scripts/validate_agent_context.py` after adding or editing an ADR — it catches broken cross-links.

## Recommended first ADR

`docs/adr/ADR-0001-record-architectural-decisions.md` — the meta-decision to use ADRs. Already shipped with this template; edit to match your team's actual adoption.
