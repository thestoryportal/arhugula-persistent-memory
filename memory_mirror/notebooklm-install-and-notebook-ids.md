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
- **Auth (operator-gated, interactive — NOT done by the agent):** `notebooklm login` (browser Google sign-in; `[browser]` extra pulls Chromium ~170 MB on first login; may need `playwright install chromium` + a headless/display path on the pod). Verify: `notebooklm auth check --test --json`.
- **⭐ Relevant notebook IDs (operator-provided 2026-06-21 — use these, NOT the old `Agent Harness Engineering` pin):**
  - `f667f1f2-7624-4039-b521-6ca37b437b6b`
  - `23ba5f2d-8317-4412-bb8a-f7c30af4c017`
  - select with `notebooklm use <id>`; `notebooklm ask "<q>"`; `notebooklm list` to confirm titles.
- **⚠ Pod restart wipes `~/.local` (the prior 2026-06-07 setup got wiped) + `~/.notebooklm/` auth** — re-run `uv tool install` and `notebooklm login` after any restart ([[pod-restart-wipes-system-python-ml-stack]]).
- **Discipline:** NotebookLM = corpus-grounded **advisory synthesis**, NOT authoritative for load-bearing claims; check our own `research_and_specs/` corpus FIRST ([[research-first-and-verify-tool-availability]]); outputs are leads/context, evidence still comes from `CORPUS/` + primary source.
