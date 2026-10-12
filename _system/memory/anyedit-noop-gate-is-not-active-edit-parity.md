---
name: anyedit-noop-gate-is-not-active-edit-parity
description: A no-op/LAW#5 pass proves a port leaves weights alone, not that active edits match upstream; add active single-fact parity + token-alignment gates.
metadata:
  type: feedback
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

Source: D-C10h-anyedit-pilot / D-C10h-anyedit-window50-controls (2026-06-27). Borne out again by Route A: R0 LAW#5 INERT, yet controls para 0/72 (CORPUS/42).

**Second port gate — token alignment (2026-06-26, D-C10h-anyedit-viability):** upstream AnyEdit tokenizes `answer` standalone but computes keys over `question + answer`, so a Qwen continuation-tokenization mismatch can create a false rescue or a false failure. A no-GPU check on A7 passed 24/24 suffix alignment with leading-space answers. Any port harness must emit answer IDs, continuation suffix IDs, decoded text, window boundaries and lookup indices for every request, and abort on mismatch or malformed decoded text.
