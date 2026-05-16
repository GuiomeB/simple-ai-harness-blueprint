<!--
PR template — formalized risk rail declaration. Required at size M.
-->

## Summary

<One paragraph: what changed and why. Reference the task / ticket if applicable.>

## Risk rail

- **Rail: green | amber | red**

| Rail | When to use |
|---|---|
| `green` | small/local; no critical zone touched; no runtime/auth/release/migration change |
| `amber` | behavioural or transverse change; short human review or owner approval expected |
| `red` | critical path or production risk; full review mandatory; may require an ADR |

Rules:
- Critical zones are listed in `AGENTS.md §Critical zones`. Touching one → minimum `amber`.
- Any P1 / P2 / major finding during review → automatic reclassification to `red` until resolved.
- The rail does not replace local validation or required CI; it accelerates the right decisions.

## Validation evidence

- [ ] `<format>` ran clean
- [ ] `<typecheck>` passes
- [ ] `<test>` passes (new tests added if behaviour changed)
- [ ] If a critical zone was touched: `<smoke>` or relevant integration command ran
- [ ] If a runtime contract or release was touched: relevant doc (`STATUS_APP.md`, runbook) still accurate

## Karpathy doctrine check

- [ ] No silent assumptions; ambiguities surfaced and resolved before coding
- [ ] Minimal code, no speculative abstractions
- [ ] Diff stays within the declared scope; no opportunistic cleanups outside it
- [ ] Success criterion was defined before acting and is now verified

## Closes / relates to

<Closes #N> · <Fixes #N> · <relates to #N>
