# Pattern — Review a parallel-ticket PR

**Pivot trigger:** any PR authored by another agent (Cursor, Codex CLI, Antigravity, …) on a ticket you didn't implement yourself.

**Shape:** process pattern. Cross-agent review goes beyond "the diff looks clean".

**When to use:** when an agent (or a human contributor) hands you a PR for review and you weren't the implementer. "A clean diff is not enough" — the implementation may match the diff but miss the *intent* of the ticket, the *invariants* of the zone, or the *patterns* the codebase expects.

---

## Five checks, in this order

### 1. Scope check

Does the PR scope match the ticket scope?

- Did the implementer add anything the ticket didn't ask for? → flag as out-of-scope. Karpathy rule 3.
- Did the implementer skip anything the ticket asked for? → flag as incomplete.
- Is the diff size consistent with the estimate? If it crosses the ~500 lines / >2 axes split threshold (`WORKFLOW.md §2`), the PR should have been split.

### 2. Pattern fidelity

Does the implementation follow the existing patterns of the codebase?

- Open `.agents/patterns/INDEX.md` for the pivot files touched. If a pattern exists, does the PR follow it?
- If the PR diverges, is the divergence justified? Did the author update the pattern (or write a new one)?
- "Looks similar to other code in the repo" is not pattern fidelity. The pattern is the explicit doc; check against it.

### 3. Invariants

Does the PR preserve the invariants of the zone?

- Open the capsule (`.agents/context/<domain>.md`) for the touched zone. Re-read the doctrine and the anti-patterns.
- Cross-check the diff against each anti-pattern. A PR that introduces a documented anti-pattern is `red`-rail by default.
- If the PR adds tests, do the tests assert the invariant or just the happy path?

### 4. Local validation

Run the validation matrix step for the touched zone (`AGENTS.md §Minimal validation matrix`). Locally. Don't trust the CI alone.

- If tests pass locally but the validation feels superficial → ask for an additional test that exercises the invariant.
- If the PR touches `AGENTS.md` / `.agents/**`: run `python scripts/validate_agent_context.py`.

### 5. Risk rail consistency

Is the declared rail consistent with what the PR actually touches?

- `green` PR touching a CODEOWNERS path → the CI gate should have caught it; if not, flag it manually.
- `amber` PR touching a critical zone with unconvincing tests → reclassify to `red`.
- `red` PR with a clean diff and full validation evidence → can proceed to merge once approved.

## What to do when the PR fails one check

- **Scope or pattern fidelity** → request changes; reference the specific pattern or ticket section.
- **Invariants violated** → block the merge; ask for a test that reproduces the invariant, then for the fix.
- **Validation insufficient** → request additional evidence (smoke output, screenshot, log excerpt).
- **Rail mismatch** → ask the author to reclassify and re-push. No silent rail edits during review.

## Anti-patterns

- Approving a PR because "the diff looks fine" without checking against the pattern or capsule.
- Approving a PR because "the CI is green". The CI is one signal; this review pattern is the other.
- Asking for changes on every cosmetic concern. Stay on scope, pattern, invariants, validation, rail.
- Letting a `green` PR through that touches a CODEOWNERS path. If the CI gate didn't catch it, that's a `/learn friction` candidate.

## Reusability

This pattern is **generic**. It applies whether the implementer is a human, an agent, or a copilot. Don't write a project-specific copy unless your review process diverges materially.

## Validation

After editing this pattern, run:

```bash
python scripts/validate_agent_context.py
```
