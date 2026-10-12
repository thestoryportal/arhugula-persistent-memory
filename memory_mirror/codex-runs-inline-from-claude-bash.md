---
name: codex-runs-inline-from-claude-bash
description: Run the GPT-6-Astra cross-family review inline from Claude's Bash, BEFORE posing a decision to the operator; Perplexity may advise during auth failure; promotion stays blocked until Astra-high review completes
metadata:
  type: feedback
---

Cross-family Codex review runs **inline from Claude's own Bash** — it is not a separate-host or "pod-only" step (first verified 2026-06-21 on the pod, where the carry-forward belief "codex cannot run from Claude's tools" was false). The current command is CLAUDE.md:16 / AGENTS.md:102: `codex exec --model gpt-6-astra -c model_reasoning_effort=high -c mcp_servers.graft.enabled=false -s read-only --skip-git-repo-check -C <worktree> -o out.md < packet.md`.

**Why cross-family reviews once silently stopped running (2026-06):** (1) behavioral — leaned on `advisor()` (Opus) at every gate and never invoked the out-of-family path; (2) a stale "can't reach network" belief ([[exhaust-options-before-blocked]] — a falsifiable blocker treated as fixed); (3) the codex binary dropped off PATH after a pod restart.

**Why:** the independence obligation (DISCIPLINE §3.1) needs a *different model family* — `advisor()` (Opus) alone is not independence. **How to apply:** at any load-bearing interpretation/promote gate, run the Astra review inline; don't defer it.

**Sequencing (operator expectation, 2026-06-21):** run the cross-family review **BEFORE posing a decision for operator approval**, not after. The operator rejected a premature decision-question with "Call Codex out of family review first" — they want the independent input *in hand* when they decide. Gate sequence: build understanding → `advisor()` → **Astra cross-family** → reconcile both → THEN present the decision/approval.

**⚠ Auth can EXPIRE mid-session (2026-06-25):** the ChatGPT-OAuth token died partway through a session (`refresh_token_reused` / `token_expired`, 401) and codex failed every call until the operator re-ran `codex login` (suggest `! codex login`). Perplexity (`mcp__perplexity__perplexity_reason`) may provide advisory input when Codex authentication fails, but it does not replace the binding Astra-high promote review. Keep promotion blocked until that review completes; do not waive it because a result appears decisive.


Give every advisor/reviewer invocation its own output path, including concurrent reviews of the same packet; shared output paths can race (lesson carried over from the retired c10k-route-a-resume note).
