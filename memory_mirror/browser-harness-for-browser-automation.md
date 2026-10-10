---
name: browser-harness-for-browser-automation
description: "Standing preference (operator, 2026-10-06): always use Browser Harness for browser automation, not Claude in Chrome."
metadata:
  type: feedback
---

The operator's words: "Always use Browser Harness for browser automation. It is much better than claude in chrome."

**Why:** it drives their real, signed-in Chrome directly and has worked where other routes failed. On 2026-10-06 it reached NotebookLM after the CLI and cookie routes broke.

**How to apply:** for any task that needs a browser (clicking, logged-in pages, JS-rendered or protected sites), load the browser-harness skill and drive it with a script file (`browser-harness < script.py`), because the shell guard refuses heredocs. Don't load the Claude in Chrome tools. Plain public fetches still use curl or a fetch tool. See [[notebooklm-via-browser-harness]].

**Chrome extensions available to Browser Harness (2026-10-06):** Google Scholar, and InfraNodus in the browser. Pair them: run a Google Scholar search, then let the InfraNodus extension graph the results page for clusters, gaps and connections.
