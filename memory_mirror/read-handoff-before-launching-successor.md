---
name: read-handoff-before-launching-successor
description: When a builder hits the 40% line, read its handoff's Done / Half-applied sections before launching the pre-staged successor; a finished build needs verification, not a successor
metadata:
  type: feedback
---

A builder stopped at the 40% context line has not necessarily left work unfinished. Read the handoff's "Done" and "Half-applied" sections before launching the successor you pre-staged.

**Why:** On 2026-10-10 MB23 (NEW-1 FIX5) hit 37%, compacted, and wrote its handoff. The build was already complete: 205/205, all REDs and GREENs saved, nothing half-applied. Launching the staged MB25 would have spent a fresh session re-reading a finished build. The right step was MAESTRO verification, then Astra. A handoff written after a compaction also comes from summarized memory, so check its hash table against disk and SHA256SUMS before trusting it.

**How to apply:** On `CONTEXT HANDOFF WRITTEN`, read only the handoff's Done/Half-applied/Failing-tests sections (`sed -n` ranges). If half-applied is "none" and failing tests are "none", retire the builder, verify it yourself, and keep the successor brief on file in case review asks for rework. Related: [[context-management-every-session]], [[test-first-one-round-builds]].
