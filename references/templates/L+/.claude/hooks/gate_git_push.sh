#!/usr/bin/env bash
# L+ guardrail: defer any `git push` that targets `main` so a human approves it
# out of band (pairs with headless deferred permissions). Everything else is
# allowed. Defaults to "allow" on any parse failure — a buggy gate must never
# block ordinary work.
set -euo pipefail

payload="$(cat 2>/dev/null || true)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty' 2>/dev/null || true)"

case "$cmd" in
  *"git push"*"origin main"*|*"git push"*" main"*|*"git push"*"HEAD:main"*)
    jq -nc '{permissionDecision:"defer", reason:"Push to main requires human approval (L+ guardrail)."}'
    ;;
  *)
    jq -nc '{permissionDecision:"allow"}'
    ;;
esac
