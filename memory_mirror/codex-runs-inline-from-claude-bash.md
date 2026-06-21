---
name: codex-runs-inline-from-claude-bash
description: Cross-family Codex review CAN run inline from Claude's Bash — network is reachable; don't defer it as "pod-only"
metadata:
  type: feedback
---

The carry-forward assumption that "the autonomy driver / codex CANNOT run from Claude's network-sandboxed tools → must be a pod process" is **STALE/FALSE** (verified 2026-06-21). From Claude's own Bash this session: outbound `TCP 443` to api.openai.com succeeds, `/workspace/bin/codex` exists (codex-cli 0.141.0), `codex login status` = "Logged in using ChatGPT", auth.json + config.toml (gpt-5.5, high effort) present on the NV volume.

**Why cross-family reviews silently stopped running:** (1) behavioral — leaned on `advisor()` (Opus) at every gate and never invoked the out-of-family gpt-5.5 path; (2) the stale "can't reach network" belief above ([[exhaust-options-before-blocked]] — a falsifiable blocker treated as fixed); (3) `codex` not on PATH after a pod restart ([[pod-restart-wipes-system-python-ml-stack]]) — `/workspace/bin` dropped from PATH; no cron/driver launched.

**How to run it inline (works):**
```
export PATH="/workspace/bin:$PATH" CODEX_HOME=/workspace/.codex
setsid bash -c 'timeout 540 codex exec -c model_reasoning_effort=medium --skip-git-repo-check "$(cat PROMPT.md)" > OUT.log 2>&1' &
```
Embed all evidence in the prompt (codex sandbox can't read repo files), medium effort (high ~600s timeouts), background + waiter (it's CPU/network → parallel to GPU work, no contention). See [[codex-review-embed-evidence-and-effort]], [[codex-chatgpt-oauth-model-slug]].

**Why:** the independence obligation (DISCIPLINE §3.1) needs a *different model family* — `advisor()` (Opus) alone is not independence. **How to apply:** at any load-bearing interpretation/promote gate, run the Codex (gpt-5.5) review inline; don't defer it as pod-only.

**Sequencing (operator expectation, 2026-06-21):** run the cross-family Codex review **BEFORE posing a decision for operator approval**, not after. The operator rejected a premature decision-question with "Call Codex out of family review first" — they want the independent input *in hand* when they decide. So the gate sequence is: build understanding → `advisor()` (Opus) → **Codex (gpt-5.5) cross-family** → reconcile both → THEN present the decision/approval to the operator. Don't ask them to approve until both reviews are done.
