---
name: codex-review-embed-evidence-and-effort
description: "Codex (gpt-5.5) cross-family review gotchas — its sandbox often can't read repo files (embed evidence inline) and high reasoning effort times out ~600s (use medium / longer timeout)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7e49dca7-c684-465a-936b-1c2ce4852502
---

Running the cross-family adversarial review via `codex exec -m gpt-5.5` (the independence gate, `tools/advisor_review_prompt.md`) has two recurring operational gotchas:

1. **Codex's bubblewrap sandbox often can't read repo files** ("ordinary filesystem reads are unavailable / launcher failed" — bubblewrap not on PATH, bundled one flaky) → it returns `FIX-FIRST: UNVERIFIABLE` without actually reviewing. **Fix:** embed the evidence INLINE in the prompt — `cat` the CORPUS doc + a python-extracted per-run summary INTO the prompt string (verified-by-me), so codex reviews the text rather than needing file access.
2. **High reasoning effort times out** (`timeout 600` → exit 143). gpt-5.5 at the config default `high` can exceed 10 min. **Fix:** pass `-c model_reasoning_effort="medium"` and/or a longer `timeout` (700s+). Medium was plenty for a focused finding-review.

Invocation that worked: `timeout 700 env CODEX_HOME=/workspace/.codex /workspace/bin/codex exec -m gpt-5.5 -c model_reasoning_effort="medium" "$PROMPT"` (codex-cli 0.141.0, ChatGPT-OAuth `auth.json` present). It DID give substantive, useful FIX-FIRST/PROCEED verdicts that improved the claim wording. Related: [[codex-chatgpt-oauth-model-slug]].
