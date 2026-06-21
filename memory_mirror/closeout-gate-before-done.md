---
name: closeout-gate-before-done
description: "Every experiment/session close ends with `python3 tools/closeout_check.py <D-ID>` = ✅ ALL GREEN — the canonical-tracker close-out is a MECHANICAL gate, not a prose norm; never hand the operator the job of checking it. ⚠️ BUT the gate checks PRESENCE not CURRENCY — a refined result after the first close-out won't re-propagate automatically; re-propagate to the FULL set on every refinement"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f4d82a89-8dda-448d-8fc0-cf79fc2d6af9
---

The write-side of the read↔write context loop (propagating a result to ALL canonical trackers) **silently lapsed** this loop (2026-06-21): I updated the salient docs (the `CORPUS/NN` writeup, runbook §0.3, `SESSION_CHECKPOINT`, memories) but missed the scattered trackers (`CORPUS/00-03`, `EVIDENCE_INDEX`, `EXPERIMENT_REGISTRY`, `PROGRESS`, `HYPOTHESIS_REGISTER`). The operator had to catch it.

**Root cause:** the close-out set was **prose-only** (DISCIPLINE §1.1 / runbook §0.4) with **no enforcement gate**, and the documented list was itself **incomplete** (omitted PROGRESS, CORPUS/01, CORPUS/02, HYPOTHESIS_REGISTER). Under a long session the soft norm got partially applied.

**The fix (durable, in-repo):** `tools/closeout_check.py <D-ID>` greps every canonical tracker (+ runbook §0.3/§12/§13 section-level + the CORPUS writeup + memory-mirror sync) for the Decision-ID and exits non-zero on any gap. It is wired as a **BINDING gate** in DISCIPLINE §1.1 + §3, runbook §0.4, CLAUDE.md, AGENTS.md, AUTONOMY.md.

**How to apply:**
- An experiment/session is **NOT done** until `python3 tools/closeout_check.py <D-ID>` is **✅ ALL GREEN**. Run it as the LAST step before declaring done or writing the checkpoint — and BEFORE telling the operator it's complete.
- Checking coverage is the **script's** job, never the operator's. If the operator is asking "did you update X?", the gate failed to run.
- When a new canonical tracker is added to the program, extend `REQUIRED` in `tools/closeout_check.py` (the gate is only as complete as that list).
- Write canonical docs via shell/python (Edit-tool reverts on this network FS — [[verify-canonical-state-edits-persist]]); the gate re-reads from disk so it doubles as a persistence check.

**⚠️ CURRENCY BLIND SPOT (caught by the operator 2026-06-21, D-D1-2):** the gate is a **string-presence** check — it verifies the D-ID *appears* in each tracker, NOT that each tracker's *content is current*. When a result **REFINES after the first close-out** (D-D1-2: the `k≤2` guardrail was later revised to `k≤1` + a mixed-load addendum + a seed-2 across-held-out finding), the gate stayed ✅ GREEN while **7 ledgers (CORPUS/00-03, EVIDENCE_INDEX, EXPERIMENT_REGISTRY, PROGRESS) silently kept the STALE `k≤2` one-liner** — because the refinements were hand-folded only into the *salient* docs (amendment, checkpoint, §0.3, CORPUS/22). There is **no auto-sync**; a green gate gave **false comfort about currency**.
- **How to apply:** every time a result CHANGES (not just first-closes), **re-propagate the new content to the FULL canonical set**, not only the docs you happened to hand-edit — then re-run the gate (which still only confirms presence). Treat each refinement as its own mini close-out. If the operator asks "are all the docs current?", the answer is almost certainly *no* unless you explicitly re-propagated.
- Better long-term: make the gate **content-aware** (e.g. assert a freshness token / result-hash per D-ID across trackers), since presence-only is the known weakness. Until then, the discipline is manual re-propagation on every refinement.
