---
name: approved-deletes-ask-then-rmtree
description: Bash rm is deny-listed in this repo; for an approved deletion, ask the operator via AskUserQuestion, then delete the one verified path with python3 shutil.rmtree
metadata:
  type: feedback
---

Every Bash `rm` Claude issues here is refused: main-repo `.claude/settings.json:13-16` denies `Bash(rm *)`, `Bash(* rm *)`, `Bash(rm:*)`, `Bash(* rm:*)` (worktree settings also deny `rm -rf ~*`). Deny beats allow rules and beats any approval. The pattern also matches any Bash command whose text contains " rm " (a heredoc writing a memory file was refused for that reason), so write such text with the Write tool.

**Why:** 2026-10-10 the operator rejected "hand me the `! rm` command" and said: "I want you to ask my permission for you to run it yourself." They approved, and Claude deleted the 86 GB C10Y offload with `shutil.rmtree` (internal SSD 110 → 196 GiB free).

**How to apply:** for a deletion that is already policy-approved (runbook §3.3a) — verify the target (contents, size, hashes in git), ask via AskUserQuestion naming the exact path, size, and the `python3 shutil.rmtree` method, then on Yes delete exactly that path with a precondition assert and verify it is gone. Never use rmtree/find without that explicit per-path Yes. Related: [[disk-budget-before-dispatch]].
