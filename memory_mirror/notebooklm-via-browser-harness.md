---
name: notebooklm-via-browser-harness
description: "NotebookLM moved to notebook.google.com ('Gemini Notebook'); the notebooklm CLI 0.8.2 fails against it (CSRF token not found). Reach it through Browser Harness in the operator's signed-in Chrome (storyportalrobert@gmail.com). Project notebooks: 'LLM as Database Agent Harness Integrated Specification v1.2' (25 sources) and 'The Model as a Graph: Querying LLM Weights with Larco' (50 sources)."
metadata:
  node_type: memory
  type: reference
  originSessionId: 6ffb3bc2-e19e-4357-8a56-33c06cb0cf38
  modified: 2026-10-06T14:25:17.965Z
---

Verified 2026-10-06. `notebooklm login` reused a stale saved browser profile and auth checks kept failing, because Google redirects to notebook.google.com. Browser Harness opened `https://notebooklm.google.com/` in the operator's real Chrome, already signed in, and listed every notebook.

**Why:** the operator wants NotebookLM as a research instrument. Don't type their Google credentials or pull browser cookies (a safety classifier stopped that path). Only use the page they're already signed into.

**How to apply:** feed Browser Harness a script file (`browser-harness < file.py`, since heredocs are refused by the shell guard): `new_tab(url)`, `wait_for_load()`, then read or ask through the page. Reuse one tab. If the CLI is updated for the new domain later, re-check with `notebooklm auth check --test --json`. See [[readme-plain-words-summary]] for the plain-language reporting rule.
