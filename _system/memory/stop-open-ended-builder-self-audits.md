---
name: stop-open-ended-builder-self-audits
description: A builder's "final audit" of a large spec does not converge across successors; once mechanical checks pass, stop it and send the subject to Astra with the unfinished audit named
metadata:
  type: feedback
---
When a builder's remaining work is an open-ended self-audit (first-failure precedence, "does each case really test its rule", precision), stop after the mechanical checks pass and send the subject to Astra, naming the unfinished audit items and any unaudited last edit in the packet.

**Why:** 2026-10-11, R4 dashboard record v3: R4D3, R4D3B and R4D3C each ran out of room mid-audit, and each pass added more controls (examples grew 5,729 → 5,966 lines) instead of closing. Each successor spent ~half its context just re-reading the 5,700-line examples file. Astra is the independent auditor anyway; its concrete findings converge where an open-ended self-audit keeps expanding.

**How to apply:** after the second handoff on the same audit, MAESTRO runs the mechanical checks itself (parse, citation bounds, every map reference resolves, every case has outcome/reason/scope), commits, and packets Astra with "treat the handoff's Remaining list as unverified". Mechanical checks prove presence, not correctness; say so in the packet. See [[trim-builder-reading-lists]] and [[context-management-every-session]].
