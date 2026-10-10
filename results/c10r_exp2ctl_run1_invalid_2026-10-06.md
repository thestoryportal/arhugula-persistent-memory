# D-C10r-exp2ctl run 1: INVALID (infrastructure), 2026-10-06 ~22:35

**Verdict: INVALID, no binding label.** The replay ran to completion (invocation `369e041ff3ef438eaabc0c1509b2ef41`, run folder `autoresearch_replay_c10_exp2loc/runs/20261006-220010_92acd03`, `REPLAY_EXIT=2`). The reader failed it on `frozen_checkout_source_diff`, `fresh_invocation_score_receipt`, `tokenizer_equality_before_dispatch` and `fidelity_before_after`, all for one reason: "unpermitted tracked-file change: .gitignore". Log: `results/c10s_sharedz_logs/exp2ctl_run_replay.log`.

**Cause (read-only diagnosis).** Two lines were appended to the clone's tracked `.gitignore` at 21:54:21. That is after `setup_replay.sh` (`replay_setup.json` 21:52:42) and the tokenizer precheck (21:52:54), and before the run started (22:00:10):

    # graft's local graph cache — regenerable, not committed (run `graft build`).
    /graft/

This is graft's signature. The graft code-index tool, active in this Claude session and in the Codex sessions, indexes repositories and appends its cache folder to `.gitignore`. The second Codex window was started at 21:53:32 and is the likely trigger; the attribution is not proven. The engine fingerprint, scorer, tokenizer cache, three-arm context records and the count/position primitives all passed. Nothing on the science path changed.

**Non-binding counts (not a result):** H = 7 (heldout_full), C = 0, O = 7, D = 90.03 (dw_total). Guards ok. These are recorded only so the rerun can be compared against them; they carry no label.

**The one fix (halt discipline: one speculative fix, then HALT).** Rerun into a fresh clone `autoresearch_replay_c10_exp2loc_r2` and make its `.gitignore` read-only (mode 444) immediately after `setup_replay.sh`, before the precheck. Git does not track that mode change, so the frozen-diff check is unaffected, and graft can no longer append. If the rerun fails any check for any reason, HALT.

**Lesson for the sealing work (D-C10r-seal):** graft writes caches and `.gitignore` lines into any repository it indexes. The sealed sandbox and the scorer areas must be out of graft's reach, and the pre-launch sweep must check for a `graft/` cache.
