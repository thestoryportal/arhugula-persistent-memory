---
name: codex-runs-inline-from-claude-bash
description: Run the GPT-6-Astra cross-family review inline from Claude's Bash, BEFORE posing a decision to the operator; perplexity_reason if Codex auth expires
metadata:
  type: feedback
---

Cross-family Codex review runs **inline from Claude's own Bash** — it is not a separate-host or "pod-only" step (first verified 2026-06-21 on the pod, where the carry-forward belief "codex cannot run from Claude's tools" was false). The current command is CLAUDE.md:16 / AGENTS.md:102: `codex exec --model gpt-6-astra -c model_reasoning_effort=high -c mcp_servers.graft.enabled=false -s read-only --skip-git-repo-check -C <worktree> -o out.md < packet.md`.

**Why cross-family reviews once silently stopped running (2026-06):** (1) behavioral — leaned on `advisor()` (Opus) at every gate and never invoked the out-of-family path; (2) a stale "can't reach network" belief ([[exhaust-options-before-blocked]] — a falsifiable blocker treated as fixed); (3) the codex binary dropped off PATH after a pod restart.

**Why:** the independence obligation (DISCIPLINE §3.1) needs a *different model family* — `advisor()` (Opus) alone is not independence. **How to apply:** at any load-bearing interpretation/promote gate, run the Astra review inline; don't defer it.

**Sequencing (operator expectation, 2026-06-21):** run the cross-family review **BEFORE posing a decision for operator approval**, not after. The operator rejected a premature decision-question with "Call Codex out of family review first" — they want the independent input *in hand* when they decide. Gate sequence: build understanding → `advisor()` → **Astra cross-family** → reconcile both → THEN present the decision/approval.

**⚠ Auth can EXPIRE mid-session + a working fallback (2026-06-25):** the ChatGPT-OAuth token died partway through a session with `refresh_token_reused` / `token_expired` (401) — codex then fails every call until the operator re-runs `codex login` (interactive; suggest `! codex login`). **Cross-family fallback when codex is down: `mcp__perplexity__perplexity_reason`** — a genuinely different model family from the Opus advisor; it caught real, load-bearing errors (metric-mismatch, identification confound, insert-vs-update mapping). Pass the full evidence inline; it's not repo-aware. **Calibrate cross-family by result type ([[review-diminishing-returns-evidence-is-binding]]):** WAIVE it for decisive/foregone/mechanistically-forced results with a noted reason; RUN it where the interpretation is subtle (metric choice, identification, over-claim).
