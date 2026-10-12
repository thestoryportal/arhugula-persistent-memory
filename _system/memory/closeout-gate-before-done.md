---
name: closeout-gate-before-done
description: Close-out = `LLMDB_ROOT=$PWD python3 tools/closeout_check.py <D-ID>` ALL GREEN (presence + --fp currency); older D-IDs going RED is expected
metadata:
  type: feedback
---

The write-side of the read↔write context loop (propagating a result to ALL canonical trackers) **silently lapsed** on 2026-06-21: the salient docs were updated (the `CORPUS/NN` writeup, runbook §0.3, `SESSION_CHECKPOINT`, memories) but the scattered trackers (`CORPUS/00-03`, `EVIDENCE_INDEX`, `EXPERIMENT_REGISTRY`, `PROGRESS`, `HYPOTHESIS_REGISTER`) were missed and the operator had to catch it. Root cause: the close-out set was **prose-only** with no enforcement gate, and the documented list was itself incomplete.

**The fix (durable, in-repo):** `tools/closeout_check.py <D-ID>` greps every canonical tracker (+ runbook §0.3/§12/§13 section-level + the CORPUS writeup + memory-mirror sync) for the Decision-ID and exits non-zero on any gap. It is wired as a **BINDING gate** in DISCIPLINE §1.1 + §3, runbook §0.4, CLAUDE.md, AGENTS.md, AUTONOMY.md.

**How to apply:**
- An experiment/session is **NOT done** until `python3 tools/closeout_check.py <D-ID>` is **✅ ALL GREEN**. Update the checkpoint and all required trackers, then run the gate as the LAST step before declaring done; rerun it after any subsequent tracker edit — and BEFORE telling the operator it's complete. From a worktree, prefix `LLMDB_ROOT=<worktree path>` or it checks the main checkout ([[llmdb-root-env-points-at-main-checkout]]).
- Checking coverage is the **script's** job, never the operator's. If the operator is asking "did you update X?", the gate failed to run.
- When a new canonical tracker is added to the program, extend `REQUIRED` in `tools/closeout_check.py` (the gate is only as complete as that list).
- Write canonical docs via shell/python (Edit-tool writes reverted on RunPod FUSE; recurrence on local memit is UNVERIFIED — [[verify-canonical-state-edits-persist]]); the gate re-reads from disk so it doubles as a persistence check.

**Currency layer (since 2026-06-21, after a presence-only gate stayed GREEN while 7 ledgers kept a stale `k≤2` line, D-D1-2):** for D-IDs registered in `tools/closeout_fingerprints.json` (D-ID → canonical SOURCE span), the gate hashes that span and requires the token `<D-ID>@<8hex>` in every tracker; a changed source makes every old token read **STALE** (distinct from MISSING). How to use: (1) register the source span; (2) `python3 tools/closeout_check.py --fp <D-ID>` prints the current token; (3) embed it in EVERY tracker in the same edit that updates the prose; (4) on any refinement re-run `--fp`, update each tracker, re-run the gate. Every refinement is its own mini close-out. Bare D-IDs fall back to presence-only. The wider three-layer design (de-dup, generated blocks via `tools/render_state.py --write`, fingerprints, pre-commit hook in `tools/git_hooks/`) is documented in `tools/ANTI_DRIFT.md`; see [[anti-drift-enforce-not-autowrite]].

**Point-in-time, not a permanent invariant (2026-06-25):** the GENERATED 'latest' trackers (SESSION_CHECKPOINT/PROGRESS/§0.3, rendered from program_state) hold only the **most recent** D-ID; the §13 check follows the section-selection logic in `tools/closeout_check.py`, not a last-header/latest-only assumption. Closing out a NEW experiment therefore turns the PREVIOUS D-ID's gate RED. **This is expected — do NOT chase it.** The permanent multi-experiment record lives in the MANUAL trackers (CORPUS/00–03, EVIDENCE_INDEX, EXPERIMENT_REGISTRY, HYPOTHESIS_REGISTER); verify older findings there, not by re-running `closeout_check <old-D-ID>`.

**Close-out traps (2026-10-06/07):** stamp a new CORPUS file's bare `Decision-ID X.` line before deriving its token, because the hash covers the whole file with only `⟨…⟩`/`D-…@hex` stamps stripped (`closeout_check.py:72-75`) — two passes until stable; the §13 check applies to EVERY open D-ID, so keep every open token in the checked top-level §13 section; runbook §5.2 rows and §12 bullets differ in format; `closeout_check.py --audit` must be clean before commit.
