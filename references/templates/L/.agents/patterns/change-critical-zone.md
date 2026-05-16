# Pattern — Change a critical zone

**Pivot files:** any file listed in `AGENTS.md §Critical zones` with risk level CRITICAL.

**Shape:** execution pattern. Procedure for editing dangerous code without breaking invariants.

**When to use:** any time you're about to modify a file in `AGENTS.md §Critical zones` or a path under `.github/CODEOWNERS` flagged as critical.

---

## Pre-edit checklist

Before opening the file:

1. **Read its capsule.** Open `.agents/context/<domain>.md` for this file's domain. Re-read the doctrine and the anti-patterns.
2. **Read its tests.** Open the test file(s) covering this code. If they don't exist or feel thin → escalate; don't edit blind.
3. **Read the file header.** Critical files often carry a doctrinal comment at the top explaining a non-obvious invariant. Don't strip those comments.
4. **State your success criterion explicitly.** Before any edit, write down the verifiable criterion: "this test goes from red to green", "this smoke command exits 0", "this assertion holds in property test X". No silent intent.

If steps 1 or 2 are blocked (no capsule, no tests), the right move is **not** to edit. The right move is to:

- write the capsule first (≤ 150 lines, doctrine + anti-patterns + pivot files), and / or
- write the test first (TDD: `.agents/workflows/tdd-loop.md`).

## During the edit

- Keep the diff scope minimal. Karpathy rule 3.
- Run the validation matrix step for this zone (`AGENTS.md §Minimal validation matrix`) after every meaningful change, not only at the end.
- If you discover an invariant that wasn't documented, stop and document it in the capsule before continuing.

## Post-edit checklist

- [ ] All tests covering the zone pass.
- [ ] The zone-specific validation command passes (`<smoke>`, `<typecheck>`, or whatever the matrix lists).
- [ ] If the edit changed behaviour, a new test was added.
- [ ] If the edit revealed a new doctrinal rule, the capsule was updated.
- [ ] PR rail is `amber` or `red` (never `green` for a critical zone). The CI gate enforces this against CODEOWNERS.
- [ ] If the edit involved an architectural choice, an ADR was written under `docs/adr/`.

## Anti-patterns

- Touching a critical file without reading its capsule and tests first.
- "Quick fix" on a critical file in a `green`-rail PR. If it's critical, the rail is at least `amber`.
- Editing the file's doctrinal header comment to make a new behaviour look "consistent" with the old. Either the invariant holds and the comment stays, or the invariant changes and an ADR explains why.
- Adding `// TODO` markers inside critical code. If the work is incomplete, the task is over-scoped — split it.

## Reusability

This is a **generic execution pattern**. Don't write a project-specific copy unless a critical zone genuinely needs procedure that diverges (e.g. a zone requires a specific snapshot or migration step). In that case: name the new pattern `change-<specific-zone>.md` and register it in INDEX.md.

## Validation

After editing this file or adding a sibling pattern, run:

```bash
python scripts/validate_agent_context.py
```
