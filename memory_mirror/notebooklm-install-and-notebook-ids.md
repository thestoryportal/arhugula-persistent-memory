---
name: notebooklm-install-and-notebook-ids
description: "NotebookLM programmatic access (notebooklm-py) — install state, login step, and the two relevant notebook IDs. Installed 2026-06-21 via uv tool (notebooklm-py 0.7.2, CLI at ~/.local/bin/notebooklm); NOT yet authed (operator must run `notebooklm login`). Pod restart wipes the install + auth."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1a56870e-a5ec-406a-9964-827f761992a9
---

**Programmatic NotebookLM access** (`teng-lin/notebooklm-py`), installed 2026-06-21 per the repo's recommended path (operator-requested). Full detail + reactivation recipe: `tools/codex-skills/notebooklm-mcp-codex-audit.md` (top banner).

- **Install:** `pip install uv` → `uv tool install "notebooklm-py[browser]"` → **`notebooklm-py==0.7.2`**, CLI at **`/root/.local/bin/notebooklm`**. Put `~/.local/bin` on PATH: `export PATH="$HOME/.local/bin:$PATH"`.
- **✅ AUTH LIVE + WORKING (2026-06-21):** the operator logged in on their laptop and supplied `storage_state.json`; it's installed **OUTSIDE the repo** at `/root/.notebooklm/profiles/default/storage_state.json`. `notebooklm auth check --test --json` → `status: ok` (token_fetch true). Chromium is present — `notebooklm ask` runs **headless from the pod** end-to-end (test query returned a real grounded answer). So I (or the operator) can query NotebookLM via Bash: `export PATH="$HOME/.local/bin:$PATH"; notebooklm use <id>; notebooklm ask "<q>"`.
- **⚠ NEVER put `storage_state.json` in the repo tree** (it holds live Google cookies; repo is PUBLIC). It briefly leaked once (committed via `git add -A`, force-push-purged) — see [[git-add-all-leaks-secrets-on-public-repo]]. Keep it under `~/.notebooklm/` only; the repo's `tools/notebooklm-verify-tmp/` is gitignored.
- **Re-auth (if pod restart wipes `~/.notebooklm/`):** operator re-logs-in on laptop → copies a fresh `storage_state.json` to the profile path (NOT into the repo).
- **(historical)** Initial login path: `notebooklm login` opens a browser for Google sign-in — **can't complete on a headless pod** (no display); hence the laptop-login + copy-cookie-file approach above.
- **⭐ Relevant notebook IDs (operator-provided 2026-06-21 — use these, NOT the old `Agent Harness Engineering` pin):**
  - `f667f1f2-7624-4039-b521-6ca37b437b6b`
  - `23ba5f2d-8317-4412-bb8a-f7c30af4c017`
  - select with `notebooklm use <id>`; `notebooklm ask "<q>"`; `notebooklm list` to confirm titles.
- **⚠ Pod restart wipes `~/.local` (the prior 2026-06-07 setup got wiped) + `~/.notebooklm/` auth** — re-run `uv tool install` and `notebooklm login` after any restart ([[pod-restart-wipes-system-python-ml-stack]]).
- **Discipline:** NotebookLM = corpus-grounded **advisory synthesis**, NOT authoritative for load-bearing claims; check our own `research_and_specs/` corpus FIRST ([[research-first-and-verify-tool-availability]]); outputs are leads/context, evidence still comes from `CORPUS/` + primary source.
