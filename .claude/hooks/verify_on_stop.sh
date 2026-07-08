#!/usr/bin/env bash
# L+ guardrail: if harness files were edited this turn, run the meta-validator
# before allowing Stop. Fail-open on any script error — a buggy gate must never
# block ordinary work.
set -euo pipefail

root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$root"

if ! git status --porcelain -- \
  AGENTS.md WORKFLOW.md .agents .claude 2>/dev/null | grep -q .; then
  exit 0
fi

if ! python3 scripts/validate_agent_context.py >/dev/null 2>&1; then
  echo "validator errors — fix before ending turn" >&2
  exit 2
fi

exit 0
