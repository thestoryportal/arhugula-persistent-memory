#!/usr/bin/env bash
# Subscription-backed Claude advisor review for LLM-as-Database.
# Uses local Claude Code auth (claude.ai / Max subscription), not an Anthropic API key.
set -euo pipefail
ROOT="${LLMDB_ROOT:-/workspace}"
CLAUDE_BIN="${CLAUDE_BIN:-$(command -v claude || true)}"
MODEL="${CLAUDE_ADVISOR_MODEL:-opus}"
EFFORT="${CLAUDE_ADVISOR_EFFORT:-high}"
PROMPT_FILE="${ADVISOR_PROMPT:-$ROOT/tools/advisor_review_prompt.md}"

if [ -z "$CLAUDE_BIN" ]; then
  echo "FATAL: claude CLI not found. Install/login Claude Code before advisor review." >&2
  exit 127
fi
if [ ! -f "$PROMPT_FILE" ]; then
  echo "FATAL: advisor prompt missing: $PROMPT_FILE" >&2
  exit 2
fi

AUTH_JSON="$($CLAUDE_BIN auth status 2>/dev/null || true)"
if ! printf '%s' "$AUTH_JSON" | grep -q '"loggedIn": true'; then
  echo "FATAL: Claude CLI is not logged in. Run: claude auth login or claude setup-token." >&2
  exit 3
fi
if ! printf '%s' "$AUTH_JSON" | grep -q '"authMethod": "claude.ai"'; then
  echo "FATAL: Claude advisor must use claude.ai subscription auth, not API-key auth." >&2
  echo "$AUTH_JSON" >&2
  exit 4
fi

if [ -t 0 ] && [ "$#" -gt 0 ]; then
  ITEM="$*"
else
  ITEM="$(cat)"
fi

exec "$CLAUDE_BIN" -p   --model "$MODEL"   --effort "$EFFORT"   --tools ""   --no-session-persistence   "$(cat "$PROMPT_FILE")

--- ITEM UNDER REVIEW ---
$ITEM"
