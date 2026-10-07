# Codex brief — D-C10r-exp2ctl verdict pass (location control, run r3)

Review only: no model, no GPU; edit nothing but **`results/c10r_exp2ctl_codex_verdict.md`**; `/usr/bin/git`; export `GIT_OPTIONAL_LOCKS=0` for any git reads in the replay clone (it is immutable). Then say DONE.

## The run
Prereg `docs/C10R_EXP2_LOCATIONCTL_PREREG.md` v2 FROZEN; driver `experiments/track_c/autoresearch_c10/replay_exp2/` v3.1 plus `lock_clone.py` v2 (your round-2 review). Clone `/Volumes/memit/llm-database-poc-mirror/autoresearch_replay_c10_exp2loc_r3` (immutable), invocation `de9c2372baab48e5ac7559108957987c`, run folder `runs/20261006-230318_92acd03`. Full reader output: `results/c10s_sharedz_logs/exp2ctl_r3_run_replay.log` (every VALIDITY row and GUARD PASS; `REPORTED` H 7, C 0, O 7, D 90.03; `LABEL primary=NO-GAIN-WITHOUT-VALUE-POSITIONS secondary=NO-COLLISION-RECOVERY quality=OK`; `REPLAY_EXIT=0`). Earlier attempts: run 1 INVALID (graft), r2 refused at precheck; `results/c10r_exp2ctl_run1_invalid_2026-10-06.md`, `architecture_profile/c10r_exp2ctl_halt_diagnostic.json`. Context: experiment 2 (`92acd03`) = 18/72 with dw_total 131.421; the baseline = 7/72 with 88.974.

## Questions
1. **Validity:** is r3 a valid binding run under the prereg (frozen source, fresh receipt, tokenizer equality, fidelity, exclusivity, guards)? Did the lock or the two invalid attempts affect anything the label depends on?
2. **Label:** is the reader's label the correct application of the prereg's frozen rules? Spell out what NO-GAIN-WITHOUT-VALUE-POSITIONS and NO-COLLISION-RECOVERY mean in the prereg's own terms.
3. **What it supports and what it does not.** H-location vs H-geometry; the write size (90.03 here, close to the baseline, vs 131.421 for experiment 2) and whether "a larger change" is still a live explanation of experiment 2's gain; one process, one seed; the premise that the 18/72 run executed `92acd03`.
4. **Exact wording** for the register note (a candidate note, not CORPUS) and for runbook §5.2.

Format: header (reviewer, model, effort, date), **Verdict: label CONFIRMED / WRONG**, numbered items with file:line, the exact wording.
