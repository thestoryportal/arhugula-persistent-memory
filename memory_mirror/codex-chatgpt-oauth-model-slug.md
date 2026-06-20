---
name: codex-chatgpt-oauth-model-slug
description: "Codex CLI 0.141.0 with ChatGPT-account OAuth rejects gpt-5 and gpt-5-codex (\"not supported when using Codex with a ChatGPT account\"); the account-valid model is gpt-5.5 (the built-in default)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1f1e8076-86fc-496b-a0f8-78b35f0d70e6
---

On this pod, Codex CLI `0.141.0` authenticated via ChatGPT-account OAuth (not API key) **rejects** both `-m gpt-5-codex` and `-m gpt-5` with HTTP 400 `invalid_request_error: "The '<model>' model is not supported when using Codex with a ChatGPT account"` (each also warns "Model metadata for `<model>` not found"). The **account-valid model is `gpt-5.5`** — confirmed by running `codex exec` with NO `-m` and no config `model` override: the header showed `model: gpt-5.5` and it returned correctly.

**How to apply:** for cross-family advisor-review via Codex+ChatGPT-OAuth, use `gpt-5.5` (pinned in `/workspace/.codex/config.toml` + `.codex/skills/advisor-review/SKILL.md` + `tools/setup_codex.sh`). `gpt-5-codex` is API-key-billing only. If `gpt-5.5` ever 400s, re-run with no `-m` to discover the new default rather than guessing slugs. The `bubblewrap not on PATH` warning is harmless (Codex uses a bundled copy).

Setup details: `CODEX_HOME=/workspace/.codex` (durable NV volume; `/root/.codex` is ephemeral on RunPod), binary at `/workspace/bin/codex`, auth at `/workspace/.codex/auth.json` (git-ignored secret; world-readable since the volume forces mode 666). Install/repair via `tools/setup_codex.sh`. Cross-family review runs as a POD process (autonomy driver `--mode agent`, web terminal, or `!` prefix) — NOT from Claude's network-sandboxed Bash tool. Related: [[pass-label-not-equal-promotable-claim]], [[review-diminishing-returns-evidence-is-binding]], [[deployment-target-intel-cpu]].
