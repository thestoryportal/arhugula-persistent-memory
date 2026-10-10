---
name: ollama-serves-winning-defense-graphify
description: Ollama serves the operator's winning-defense graphify refresh and shares the GPU; stopped 2026-10-06; restart with brew services start ollama
metadata:
  type: reference
---

Ollama runs as a Homebrew service (`sh.brew.ollama`). Killing the process doesn't stick, so stop it with `brew services stop ollama`. Its client is `/Users/robertrhu/Projects/winning-defense/scripts/refresh_graph.sh`, the launchd job `com.rhu.graphify.refresh` with a StartInterval of 1200 s, whose extraction embeds through Ollama. Stopping Ollama makes that job fail until Ollama is restarted.

**Why:** the operator asked why an unused Ollama should stay up and slow runs. It was in use, but by another project. They chose to stop it (2026-10-06).

**How to apply:** before a GPU run, `pgrep -fl ollama`. If it's running, say what uses it and let the operator decide. The autoresearch launcher refuses to start while Ollama runs. Remind the operator to restart it afterwards for the graphify job. Related: [[local-only-no-rented-compute]].
