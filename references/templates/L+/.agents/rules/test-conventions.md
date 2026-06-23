---
name: test-conventions
description: Narrow technical conventions for test files. Auto-loads when a matching test file is edited; also reachable via the ROUTER.
# `globs:` is the reliable auto-load key for path-scoped rules (the documented
# `paths:` key is sometimes dropped by current tooling). Adapt these to your
# stack — they replace `<test-root>` once your real test layout exists.
globs:
  - "**/*.test.*"
  - "**/*.spec.*"
  - "**/tests/**"
  - "**/test/**"
---

# Rule — Test conventions

**Scope:** narrow technical conventions for test files. Not doctrine (capsules), not procedures (patterns), not workflows. Just rules.

**Pivot files:** test files under `<test-root>/` or co-located `*.test.ts` / `*.spec.ts` (adapt to your stack).

**How this rule loads:** the `globs:` frontmatter above makes it **auto-load** (zero token cost otherwise) whenever a matching test file is touched. This is *complementary* to `.agents/ROUTER.md`, not a replacement: globs cover "I'm editing file X → load the matching rule"; the ROUTER covers "this task family → load this capsule/pattern". Keep both in sync — a rule reachable by glob should still appear in the ROUTER's relevant rows.

---

## File naming

- One source file `foo.ts` → one test file `foo.test.ts` (or your stack's equivalent).
- Cross-file behaviour tests live in `<test-root>/integration/` (or `tests/integration/`), one feature per file.
- Smoke / E2E live in `<test-root>/e2e/` (or `scripts/smoke/`), named by the smoke scenario, not by the file under test.

## Test structure

- Top-level `describe` matches the unit under test (function name or component name).
- Nested `describe` blocks group by scenario (happy path, edge cases, error paths).
- One `it` / `test` block = one assertion of one behaviour. Don't pack 5 assertions into one test.

## RED state fidelity (TDD)

A test in the RED state must fail with an **assertion-style error**, not with:

- `TypeError` / `ReferenceError` / `Cannot find module` → fix the test setup
- `SyntaxError` → fix the test, not the code
- `No test found in suite` → fix the test, not the code

A test that fails for the wrong reason is not a valid RED. See `.agents/workflows/tdd-loop.md`.

## Fixtures and mocks

- Fixtures live in `<test-root>/fixtures/` or alongside their test file. Name them by what they represent, not by which test uses them.
- Mock at the boundary, not inside the unit under test. If your unit tests need deep internal mocking, the unit is too coupled — refactor before testing.
- A mock that returns a hard-coded value used by 3+ tests should become a fixture.

## What tests should assert

- Behaviour, not implementation. "Calling `foo(1)` returns `2`" is good. "Calling `foo(1)` calls `bar()` then `baz()`" is fragile.
- Invariants, especially in critical zones. If the capsule documents an invariant, at least one test should assert it.
- Error paths, not just happy paths. A function that throws should have a test that asserts the throw.

## What tests should NOT do

- Mutate shared state across tests. Each test is independent or it's broken.
- Sleep / wait for time. Use fake timers or explicit clocks.
- Hit the network. If you need to test network behaviour, use a recorded fixture or a mock.
- Skip themselves silently (`it.skip` without a TODO referencing a ticket).

## When this rule is updated

A `/learn` entry that lands here means a new test convention has emerged. Promote it to this file with a one-line entry under the relevant section above. If the rule grows past 150 lines, split it (one rule file per topic — fixtures, mocking, integration vs unit, etc.).

## Validation

After editing, run:

```bash
python scripts/validate_agent_context.py
```
