# Codex brief — D-C10t-secondkey verdict pass (step 2)

Review only: no model, no GPU; edit nothing but **`results/c10t_secondkey_codex_verdict.md`**; `/usr/bin/git`. Then say DONE.

## The run
Prereg `docs/C10T_SECONDKEY_PREREG.md` v2 FROZEN (+ program ruling D-C10t-p5rule, runbook §5.2). Implementation by Codex, advisor implementation review (PROCEED after fix round 1), first pass-1 HALT (float64 on MPS after A1/A2; `architecture_profile/c10t_secondkey_halt_diagnostic.json`, `results/c10t_secondkey/`) → one fix (4 readout sites; your review `results/c10t_secondkey_fix2_codex_review.md`) → rerun in `results/c10t_secondkey_r2/` (step 0 READY; selection scientifically identical to the published one, `results/c10t_secondkey_r2_selection_compare.json`). Logs `results/c10t_secondkey_logs/r2_{step0,pass1}.log`. Reader (model-free): `LLMDB_ROOT=<worktree> .venv/bin/python -B experiments/track_c/c10t_secondkey_read.py <worktree>/results/c10t_secondkey_r2`.

Printed: A1 70/72, A2 70/72; A7-single 15/72 (canon 7/24); A7-dup 15/72 (canon 8/24); A7-second-B10 23/72 (canon 15/24), gain 8, write ratio 2.05, F1 gates fail on 10 of 24 subjects (prefix bleed: new next-token hits on prompts that contain the value's first piece); label **NULL-LARGE-WRITE**; replication not pending.

## Questions
1. Validity: the rerun's binding to the published step-0 selection, the observer-inertness check (B3), LAW#5, the reference envelope, the duplicate control, source identity. Is the run valid, and is NULL-LARGE-WRITE the correct application of §3 (the gain < 10, the LARGE-WRITE qualifier, the F1 failures — would they make it TRADEOFF if sized)?
2. What may be recorded in CORPUS/53: the binding counts, the per-template split (6/8/9), canon 15 vs 7, the F1 prefix-bleed finding (what it means mechanistically for a value-internal key), the duplicate control's null, the write size; what each does and does not support.
3. Next per the prereg/sequence (step 3 D-C10u-mint2? step 4?). Name any candidate the record motivates, as a candidate only.
4. Exact proposed CORPUS/53 wording (same format as your CORPUS/52 proposal).

Format: header, **Verdict: label CONFIRMED / WRONG**, numbered items with file:line, the CORPUS/53 wording, the recommendation.
