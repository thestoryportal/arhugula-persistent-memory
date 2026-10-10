---
name: notebooklm-via-browser-harness
description: "NotebookLM moved to notebook.google.com and the CLI fails; use Browser Harness in the signed-in Chrome. Notebooks: spec v1.2, 'Model as a Graph'"
metadata:
  type: reference
---

Verified 2026-10-06. `notebooklm login` reused a stale saved browser profile and auth checks kept failing, because Google redirects to notebook.google.com ("Gemini Notebook"). Browser Harness opened `https://notebooklm.google.com/` in the operator's real Chrome, already signed in, and listed every notebook. Re-checked 2026-10-10: CLI 0.8.4 `notebooklm auth check --test --json` still returns `"status": "error"`. Project notebooks: "LLM as Database Agent Harness Integrated Specification v1.2" and "The Model as a Graph: Querying LLM Weights with Larco". The pod-era CLI notebook IDs (2026-06-21, unverified since the domain move) are in `git show fd77f7e:memory_mirror/notebooklm-install-and-notebook-ids.md`.

**Why:** the operator wants NotebookLM as a research instrument. Don't type their Google credentials or pull browser cookies (a safety classifier stopped that path). Only use the page they're already signed into.

**How to apply:** feed Browser Harness a script file (`browser-harness < file.py`): `new_tab(url)`, `wait_for_load()`, then read or ask through the page. Reuse one tab. If the CLI is updated for the new domain later, re-check with `notebooklm auth check --test --json` before relying on it. NotebookLM answers are corpus-grounded advisory synthesis, never authoritative: check our own `research_and_specs/` corpus first ([[research-first-and-verify-tool-availability]]); evidence still comes from `CORPUS/` + primary sources. Never put a `storage_state.json` (live Google cookies) in the repo tree ([[git-add-all-leaks-secrets-on-public-repo]]). See [[readme-plain-words-summary]] for the plain-language reporting rule.
