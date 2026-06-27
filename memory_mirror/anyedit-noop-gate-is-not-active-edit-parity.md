---
date: 2026-06-27
source: D-C10h-anyedit-pilot / D-C10h-anyedit-window50-controls
scope: LLM-as-Database C10 AnyEdit gates
---

# AnyEdit No-Op Gate Is Not Active Edit Parity

LAW#5/null no-op and token-alignment gates are necessary, but they did not prove
the AnyEdit transplant was edit-capable. In C10h, both small-window and
upstream-equivalent-window paths could pass inertness/token checks while active
A1/A2 edits collapsed. The no-op gate proves the transplant can avoid changing
weights when asked to do nothing; it does not prove the active ARE target,
lookup position, loss mask, or update geometry matches upstream AnyEdit.

Add an active single-fact parity gate before future port evidence: one easy A1
request must reproduce upstream-equivalent tensor traces closely enough to
explain the edit path, and must recover A1/A2 behavior before any hard A7
claim is licensed. Treat a no-op-only pass as "harness inertness", not "port
validity".
