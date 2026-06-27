---
date: 2026-06-27
source: Perplexity MCP restore during C10h review
scope: Codex research tooling
---

# Perplexity MCP Restore From Pod Restore

After a terminal/session reset, `codex mcp list` may show no Perplexity server even
though the pod has a restore record. Check `/workspace/.pod_restore/mcp/servers.json`
for a `perplexity` server definition. In this repo, the safe Codex MCP config should
point to `tools/perplexity_mcp_from_restore.py`, which reads the restore file at
runtime and avoids storing secret values in tracked `.codex/config.toml`.

In this session, restoring the server initially embedded the key in `.codex/config.toml`;
that was corrected to the wrapper path before checkpointing. `codex mcp list` then
showed Perplexity enabled, but the current Codex tool surface did not refresh to
expose `perplexity_reason` in the same turn. Direct API use was possible only after
explicit user approval to send non-public research context externally. Do not echo
keys from restore files; redact credential-like values when inspecting config.
