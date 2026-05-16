# Pattern — Decision spike with revisit thresholds

**Pivot trigger:** any architecture or technical choice taken under significant uncertainty, where postponing is worse than choosing.

**Shape:** decision pattern. Time-boxed choice with explicit triggers to revisit.

**When to use:** when you must commit to an approach (library, schema, deployment topology, write-path strategy) before all evidence is in, and you want to avoid the "decision becomes permanent by accident" failure mode.

---

## The shape of a spike decision

A spike decision has five mandatory parts. Skipping any of them turns a spike into a silent commitment.

1. **The choice made.** One sentence.
2. **The uncertainty acknowledged.** What you don't yet know, and why you can't wait to know it.
3. **The time-box.** A concrete duration or a concrete milestone after which you'll revisit.
4. **The revisit thresholds.** Specific, measurable triggers that force a revisit *before* the time-box if hit.
5. **The fallback.** What you'd do if the decision turns out wrong.

A spike with no revisit threshold and no fallback is not a spike. It's a permanent choice dressed in tentative language.

## Template

Write this in an ADR under `docs/adr/ADR-<NNNN>-<slug>.md`:

```markdown
# ADR-<NNNN>: <slug>

- Status: spike
- Date: <YYYY-MM-DD>
- Revisit-by: <date or milestone>

## Choice

<One sentence. The thing being committed to.>

## Uncertainty

<What we don't yet know. Why we can't wait.>

## Revisit thresholds (any of these triggers a re-decision)

- <Threshold 1 — measurable, time-bound, observable>
- <Threshold 2>
- <Threshold 3>

## Fallback

<What we'd do if we reverse this decision. The lighter the fallback, the smaller the spike.>

## Inputs at decision time

- <Data, benchmark, prototype result, or expert input that shaped the choice>
```

## Examples of revisit thresholds

- "If error rate on path X exceeds 1% over 7 days, revisit."
- "If a single ticket on this stack takes more than 3 days of implementation, revisit."
- "If we hit feature requirement Y (currently out of scope) within 6 months, revisit."
- "If the library's maintainer marks the API as deprecated, revisit immediately."

**Bad thresholds:** "if it doesn't work", "if we don't like it", "if we run into problems". Those aren't thresholds — they're vague intentions.

## What to do at the revisit date

1. Re-read the ADR. Has any threshold been crossed?
2. Has new evidence appeared that would have changed the original decision?
3. Decide one of three outcomes, and record it in the ADR:
   - **Confirm** — promote status from `spike` to `accepted`. Remove the revisit-by date.
   - **Revise** — write a new ADR superseding this one. Mark this ADR's status as `superseded by ADR-<N>`.
   - **Postpone** — extend the revisit-by date by a concrete delta with a one-line justification. Avoid postponing more than once; a second postponement means the decision is implicit.

## Anti-patterns

- Marking an ADR as `accepted` from day one to skip the revisit discipline.
- Setting a revisit-by date 12+ months out. By then the context is unrecognizable. Cap at 6 months for most spikes.
- Writing revisit thresholds that are unobservable in practice.
- Treating a spike as permission to ignore tests or invariants. Spike is on the *decision*, not on the *execution quality*.

## Reusability

This is a **generic decision pattern**. Use the same shape regardless of whether the spike is about a library choice, a write-path strategy, or a deployment topology. Project-specific variants are rarely worth their own pattern file.

## Validation

After adding an ADR that uses this pattern, run:

```bash
python scripts/validate_agent_context.py
```
