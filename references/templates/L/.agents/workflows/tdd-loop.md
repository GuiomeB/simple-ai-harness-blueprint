---
description: Test-driven development state machine for new business logic or new mutations. Optional but typical at size M. Hard rule on the RED state to prevent false positives.
---

# `/tdd-loop` workflow

State machine for any new business logic, new mutation, or behavioural change to a critical zone.

## States

### RED — write a failing test before touching the implementation

- Write the test that captures the new expected behaviour.
- Run `<test>`.
- The test **must fail** with an **assertion-style error** (`AssertionError`, `expect(...)` failure), not with a `TypeError` / `SyntaxError` / import error / "no test found in suite".
- If the failure is anything else, fix the test, not the implementation.

A test that fails for the wrong reason is not a valid RED state. Common false positives:

- Missing import → `ReferenceError` / `Cannot find module` → fix the test
- Misspelled symbol → `TypeError` → fix the test
- Empty `describe` block → `No test found` → fix the test

### GREEN — write the minimal code that makes the test pass

- Implement exactly what the test demands. Nothing more.
- No speculative cases. No "while I'm in here" cleanups.
- Re-run `<test>`. The test must pass; other tests must still pass.
- Run `<typecheck>` and any zone-specific validation from `AGENTS.md §Minimal validation matrix`.

### REFACTOR — clean the implementation without changing behaviour

- Tests stay green throughout.
- Run `<test>` after each non-trivial refactor step (rename a variable → OK, batch-refactor 5 things → run tests).
- Run `<lint>` and `<format>` at the end.
- If the refactor reveals a new sub-behaviour to test, return to RED for that sub-behaviour.

## Mandatory zones

TDD is mandatory for any change to:

- <Engine / core domain logic — e.g. `shared/engine/*`>
- <Mutation handlers / write-path code>
- <Auth / session / identity>
- <Any file flagged as CRITICAL in `AGENTS.md §Critical zones`>

For UI/cosmetic changes, TDD is encouraged but not enforced — visual regression and component tests are usually enough.

## When the loop fails

If you cannot get to RED with a clean assertion error after 2 attempts:

- The test fixture or setup is wrong → fix that first.
- The behaviour being captured may be ambiguous → return to the user for clarification (Karpathy rule 1).
- The zone may need a new pattern (at L) or a capsule update.

## Exit criteria

A `/tdd-loop` is complete when:

- The new behaviour is captured by at least one test
- All tests pass
- `<typecheck>` and zone validation pass
- The risk rail is declared in the resulting PR / commit

## Reference

- Test patterns and fixtures: <link to your test conventions file, or `.agents/rules/test-patterns.md` at L>
- Critical zones: `AGENTS.md §Critical zones`
