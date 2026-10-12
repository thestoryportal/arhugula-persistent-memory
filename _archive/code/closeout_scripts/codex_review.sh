#!/bin/bash
# gpt-5.5 cross-family review (DISCIPLINE.md: Claude-led work uses a GPT-family reviewer at the promote gate). Local Codex CLI, ChatGPT OAuth.
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
cd "$W" || exit 1
DOC="${1:-docs/C10K_ROUTEA_RESULT.md}"; OUT="${2:-logs/codex_c10k_route_a_result_review.md}"
codex exec -m gpt-5.5 --sandbox read-only -C "$W" "$(cat tools/advisor_review_prompt.md)

--- ITEM UNDER REVIEW (a RESULT before it is written to CORPUS; two Claude advisor rounds already applied; you are the cross-family check) ---
$(cat "$DOC")" > "$OUT" 2> "${OUT%.md}.err"
echo "CODEX_RC=$?"
