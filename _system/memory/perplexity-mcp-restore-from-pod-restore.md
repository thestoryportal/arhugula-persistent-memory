---
name: perplexity-mcp-restore-from-pod-restore
description: "RETIRED 2026-10-10 — pod restore path gone; Codex Perplexity MCP is now registered globally; do not act on this note"
metadata:
  type: reference
---
RETIRED 2026-10-10 by the memory audit (results/memory_audit_20261010/). /workspace/.pod_restore no longer exists; on 2026-10-10 the operator registered Perplexity for Codex globally with `codex mcp add perplexity --env PERPLEXITY_API_KEY=… -- npx -y @perplexity-ai/mcp-server` (key in ~/.codex config, not git; `codex mcp list` shows it enabled), and the repo's pod-era .codex/config.toml entry is commented out (commit 6cbb10c). Full prior text: `git show fd77f7e:memory_mirror/perplexity-mcp-restore-from-pod-restore.md`.
