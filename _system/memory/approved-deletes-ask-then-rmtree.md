---
name: approved-deletes-ask-then-rmtree
description: Bash rm is deny-listed on protected paths (main .claude/settings.json); regenerable bulk is reclaimed autonomously via reclaim.py (2026-10-15); other deletes ask per path, then python3 shutil.rmtree
metadata:
  type: feedback
---

Bash `rm` is deny-listed on protected paths only: the main checkout's `.claude/settings.json:12-27` denies `rm`/`rmdir` on `*CORPUS*`, `*_system/memory*`, `*code/memit/vendor*`, `*data/covariance*`, `*hf_cache*`, `*reproducibility_manifest*`, and `rm -rf` of / and ~. Deny beats allow rules and beats any approval. A blanket pattern also matches any Bash command whose text contains " rm " (a heredoc writing a memory file was refused for that reason), so write such text with the Write tool.

**Why:** 2026-10-10 the operator rejected "hand me the `! rm` command" and said: "I want you to ask my permission for you to run it yourself." They approved, and Claude deleted the 86 GB C10Y offload with `shutil.rmtree` (internal SSD 110 → 196 GiB free).

**How to apply:** whichever settings file applies, for a deletion that is already policy-approved (runbook §3.3a) — verify the target (contents, size, hashes in git), ask via AskUserQuestion naming the exact path, size, and the `python3 shutil.rmtree` method, then on Yes delete exactly that path with a precondition assert and verify it is gone. Never use rmtree/find without that explicit per-path Yes. Related: [[disk-budget-before-dispatch]].

**Regenerable bulk (operator 2026-10-15 ~17:35 MDT: "I want you to autonomously mange disk storage space safely and effectively."):** no per-path ask. Inspect first. Never touch receipts, proof, predecessor bytes or the STORAGE.md deny-list. Delete via the allow-listed `LEAN/tools/reclaim.py LIST [--apply]`. The per-path ask still covers everything else.
