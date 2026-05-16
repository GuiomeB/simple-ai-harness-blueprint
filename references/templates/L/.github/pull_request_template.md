<!--
PR template — formalized risk rail declaration. Machine-enforced at size L:
the CI job `pr-rail-guard` fails any PR declared `green` that touches a path
listed in `.github/CODEOWNERS`.
-->

## Summary

<One paragraph: what changed and why. Reference the task / ticket if applicable.>

## Risk rail

- **Rail: green | amber | red**

| Rail | When to use |
|---|---|
| `green` | small/local; no `.github/CODEOWNERS` path touched; no runtime/auth/release/migration change |
| `amber` | behavioural or transverse change; short human review or owner approval expected |
| `red` | critical path or production risk; full review mandatory; may require an ADR |

Rules:
- Touching any path under `.github/CODEOWNERS` → minimum `amber`. The CI gate enforces this.
- Any P1 / P2 / major finding during review → automatic reclassification to `red` until resolved.
- The rail does not replace local validation or required CI; it accelerates the right decisions.

## Validation evidence

- [ ] `<format>` ran clean
- [ ] `<typecheck>` passes
- [ ] `<test>` passes (new tests added if behaviour changed)
- [ ] If a critical zone was touched: `<smoke>` or relevant integration command ran
- [ ] If `AGENTS.md` / `.agents/**` / `WORKFLOW.md` were touched: `python scripts/validate_agent_context.py` ran clean
- [ ] If runtime / release was touched: relevant doc (`STATUS_APP.md`, runbook) still accurate

## Karpathy doctrine check

- [ ] No silent assumptions; ambiguities surfaced before coding
- [ ] Minimal code, no speculative abstractions
- [ ] Diff stays within the declared scope
- [ ] Success criterion was defined before acting and is now verified

## Closes / relates to

<Closes #N> · <Fixes #N> · <relates to #N>
