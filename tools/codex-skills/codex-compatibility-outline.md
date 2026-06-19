# Codex Compatibility Outline

This note codifies the operator-approved Codex setup direction for this repository.

## Durable Setup Sequence

1. Add root `AGENTS.md` as the compact Codex-authoritative projection of `CLAUDE.md`.
2. Add axis-local `AGENTS.md` files for `harness-is`, `harness-as`, `harness-cp`, and `harness-od`.
3. Add project `.codex/config.toml` for instruction discovery and hooks. Keep provider/auth/profile settings user-level.
4. Map load-bearing Claude hooks into Codex hooks:
   - `SessionStart`: roadmap/status and posture reminder.
   - `PreToolUse`: X-AL-3 and destructive-command boundary checks.
   - `PermissionRequest`: paid-provider, credential, destructive, and network review notes.
   - `Stop`: verification and PR-state reminder.
   - `SessionStart` and `Stop` also run `tools/codex_context_guard.py` so context
     freshness, worktree isolation, dashboard drift, and closeout obligations are
     materialized from HEAD instead of remembered. Hard guard findings propagate
     as hook failures.
5. Keep reusable workflows as Codex skills under `.agents/skills` or installed user skills. Package as plugins only for distribution.
   - Repo-local shims now live under `.agents/skills/` for overlay queries, roadmap continuation, self-heal, PR shipping, and CLAUDE governance optimization.
6. Use `.codex/notes/deterministic-context-workflow.md` as the Codex source of
   truth for context-rot prevention; run `just codex-preflight` before work,
   `just codex-checkpoint <label>` at mid-arc re-grounding points, and
   `just codex-closeout` before final response, commit, or PR.
   - Credential-gated units advance to the credential boundary first. When no
     HIL/operator-approval surface is available, log the gate with
     `just codex-credential-gate ...`, update a human-facing tracking surface,
     and continue to the next implementable unit once non-credential work is
     proven closed.
7. Run substantive Codex work in isolated worktrees and land changes through reviewable PRs with strict CI.
8. Validate instruction discovery with `codex --ask-for-approval never "Summarize the current instructions."` and nested `--cd` checks.

## Memory Rule

Required team guidance belongs in `AGENTS.md` and checked-in docs. Codex memories are optional generated state under `CODEX_HOME`; do not hand-edit them as the primary rules surface.
