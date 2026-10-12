---
name: record-provenance-per-test-run
description: every RED/GREEN receipt must record the source+test SHA-256 and exact command it ran; a log without them cannot be cited
metadata:
  type: feedback
---

Every RED or GREEN run a builder saves must record, next to the log, the exact command, the cwd, and the SHA-256 of the source and test files that actually ran. Swapping the old source in place and back leaves no trace.

**Why:** MB29 (NEW-1 reap round 4, 2026-10-10) ran the owed causal RED (final tests eccabf81 on old source 3bb767f0, 22 failures) as `RED_strengthened.log`, then compacted. Nothing recorded what it ran against; MAESTRO26 could only infer it from OWNERSHIP_AST line numbers that exist only in the old file, and had to pay a fresh builder (MB31) to rerun it with provenance before Astra r13.

**How to apply:** in every test-first brief, require an isolated copy tree (mktemp) for RED-on-old-source and a command.json / evidence.json entry with command, cwd and both hashes per run. When a log lacks them, rerun rather than cite it. Related: [[test-first-one-round-builds]], [[rerun-never-patch]].
