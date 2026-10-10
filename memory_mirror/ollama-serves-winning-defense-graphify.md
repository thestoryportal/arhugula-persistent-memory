---
name: ollama-serves-winning-defense-graphify
description: "Ollama on the MBP serves nomic-embed-text to the operator's winning-defense graphify refresh (launchd com.rhu.graphify.refresh, every 20 min); it shares the GPU with experiments. Stopped 2026-10-06 on the operator's instruction; restart with brew services start ollama."
metadata:
  node_type: memory
  type: reference
  originSessionId: 6ffb3bc2-e19e-4357-8a56-33c06cb0cf38
  modified: 2026-10-06T11:39:49.123Z
---

Ollama runs as a Homebrew service (`sh.brew.ollama`). Killing the process doesn't stick, so stop it with `brew services stop ollama`. Its client is `/Users/robertrhu/Projects/winning-defense/scripts/refresh_graph.sh`, the launchd job `com.rhu.graphify.refresh` with a StartInterval of 1200 s, whose extraction embeds through Ollama. Stopping Ollama makes that job fail until Ollama is restarted.

**Why:** the operator asked why an unused Ollama should stay up and slow runs. It was in use, but by another project. They chose to stop it (2026-10-06).

**How to apply:** before a GPU run, `pgrep -fl ollama`. If it's running, say what uses it and let the operator decide. The autoresearch launcher refuses to start while Ollama runs. Remind the operator to restart it afterwards for the graphify job. Related: [[local-only-no-rented-compute]].
