---
name: importing-external-files-traps
description: Traps when copying outside files into the repo or reading a builder's last reply token (hierarchical instruction loading, *token* gitignore, verify staging after failed git add, READY hidden behind HANDOFF)
metadata:
  type: feedback
---

Hit by MAESTRO40 on 2026-10-11 while importing 142 backup-SSD documents (`docs/historical_backups/20261011`, commit 7e03fd45).

- **An imported `CLAUDE.md` or `AGENTS.md` can become active through hierarchical loading or an explicit instruction read.** Claude Code loads nested CLAUDE.md and Codex loads AGENTS.md hierarchically, so an imported old one silently steers future sessions. Rename on import (we used `CLAUDE.historical.md`) and record the rename in the provenance index.
- **`.gitignore:50` `*token*` silently drops any file whose name contains "token"** (e.g. "…delegation token design.md"). Compare staged count to expected count; if a secret scan of the content is clean, `git add -f` that one exact path. Never loosen the rule.
- **A failed `git add` does not prove the index is unchanged.** On an ignored-path refusal, inspect the actual staged set before retrying; filter `*.log` and other ignored paths out of manifest-driven adds.
- **A watcher that reports only the last reply token can hide a finished job.** codexbk4 had already replied `BK4 AUDIT READY` when MAESTRO's queued ≤45% stop message made it append a handoff and reply `BK4 HANDOFF`. On any HANDOFF, read the handoff's first lines before starting a successor.

**Why:** each would have cost a wrong successor session, a silently missing file, or stale instructions loaded into every later session.
**How to apply:** before any bulk import, grep target basenames for instruction-file names, then check staged == expected. Related: [[codex-watch-anchor-replies-read-context-from-rollout]], [[approved-deletes-ask-then-rmtree]].
