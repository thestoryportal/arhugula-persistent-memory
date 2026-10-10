---
name: codex-sandbox-no-network
description: Codex builders run in a workspace-write sandbox without network — Drive/gh/remote checks must be run by MAESTRO, not briefed to them
metadata:
  type: feedback
---
2026-10-10: codexmb3's Drive backup build could not run its rclone self-test or the real `--dry-run` sizing ("Drive verification BLOCKED by sandbox DNS"); the Codex start scripts use `-s workspace-write`, which has no network.

**Why:** a brief that asks a builder for live-network evidence yields a BLOCKED line instead, and the gap is easy to miss in the reply.

**How to apply:** in builder briefs, say network checks are out of scope and mocked in tests; MAESTRO runs the live Drive/gh/CI verification itself after review. Related: [[gdrive-rclone-remote]].
