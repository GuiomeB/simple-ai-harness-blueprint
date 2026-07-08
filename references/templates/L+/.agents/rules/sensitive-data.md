# Sensitive data — global rule (all agents, all loops)

Agents and loops must not read, copy, summarize, or expose secrets unless the
task explicitly requires it **and** a human approved that scope.

## Never surface in outputs

- `.env` and `.env.*` files
- API keys, tokens, passwords, cloud credentials
- Private keys (`*.pem`, `id_rsa`, SSH keys)
- Session cookies or auth headers from logs

If sensitive data appears in a tool response or file, do not quote it. Replace
with `[REDACTED]` and flag **Needs Human Review** in the loop's `STATE.md` (or
in your completion message when not in a loop).

## Permission review

Re-audit tool and MCP permissions whenever a new connector is added. Scheduled
or unattended loops must not gain write scope to external systems without an
explicit level bump in `SPEC.md` (see `.agents/workflows/loop.md §Permission ladder`).

## Cross-reference

- Loop state contract: `docs/adr/ADR-0003-loop-state-contract.md`
- Deterministic deny list: `.claude/settings.json` (L+ profile)
