# autoresearch — re-aim family on the C10 harness (adapted from `external_prior_art/autoresearch-macos/program.md`)

This loop follows the autoresearch-macos conventions (one editable file, a fixed budget, one metric, a results table with keep / discard / crash, a loop that does not stop to ask) applied to the LLM-as-Database C10 edit harness instead of a training script. **It is FENCED (DISCIPLINE §3): an optimizer, not a scientist. Everything it produces is a CANDIDATE. It never writes `CORPUS/`, the runbook, the checkpoint, the ledgers or memory; the operator folds its candidates in through a pre-registered falsifier.** Operator authorization: D-C10q-rulings-1 (2026-10-06) — run overnight after the stacked arm, unattended.

## Setup (once, before the loop)

1. **Run tag**: `reaim-<date>` (e.g. `reaim-oct06`). Results live under `results/autoresearch_reaim/<tag>/`. Do **not** create git branches or commits for iterations (the program's branch is a science ledger; the fork's git keep/revert is replaced by config snapshots in the results folder).
2. **Read the in-scope files**: this `program.md`; `knobs.json` (the ONE file you edit); `run_iteration.py` (fixed: runs one edit experiment under the current knobs and prints the summary; do not modify); the harness `experiments/track_c/c10e_bandknob.py` and the seams `Z_OVERRIDE` / `_ARM_STATE` (read-only); CORPUS/48–49 (what the knobs mean).
3. **Verify the gates**: `python3 tools/engine_fingerprint.py` PASS; `results/c10l_covgeom/run1_armB_identity.json` present (LAW#3 reference).
4. **Initialize** `results/autoresearch_reaim/<tag>/results.tsv` with the header row. The baseline is the first iteration (knobs as shipped = the CORPUS/49 fresh two-pass configuration).

## Experimentation

Each iteration runs the fixed script: `mkdir -p results/autoresearch_reaim/<tag>/iter_<NN>` first (the shell opens the log before Python runs), then `$LLMDB_ROOT/.venv/bin/python experiments/track_c/autoresearch_reaim/run_iteration.py <tag> <iter> > results/autoresearch_reaim/<tag>/iter_<NN>/run.log 2>&1`, then `log_row.py <tag> <iter> "<description>"` appends the results.tsv row mechanically (guards, keep/discard, crash) (redirect everything; never let it flood the context). It applies the A7 coined-coined edit under the current `knobs.json` (A1 + A2 controls run every iteration), measures the held-out full-sequence recall and the locality axes, and prints a summary block. **Budget ≈ 25–40 min per iteration** (an edit experiment, not a 5-minute training run); kill and mark `crash` if an iteration exceeds 60 minutes.

**What you CAN do:** edit `knobs.json` only. Knobs: `resolve_rounds` (0 = engine targets; 1 = re-solve once on the edited model and aim a fresh edit at it, the CORPUS/49 arm; 2–3 = iterate), `stack` (false = fresh edit from base aimed at the re-solved target; true = second edit on top of the first), `write_cap` (stack = true only: each extra edit's residual is rescaled so ‖ΔW_extra‖/‖ΔW₁‖ ≤ cap — exact, the solve is linear in the residual; null = uncapped; with stack = false the script refuses it — scale through `z_blend` there), `z_blend` (0–1: target = blend of z_pre and z_post), `layers` (a contiguous band within 4–12), `ridge` (the solve's L2; default 1.0), `resolve_steps` (compute_z steps for every solve, the first edit's included; default 25 = harness). `ridge` is applied after the LAW#5 parity gate, which always runs at the harness default 1.0, so `law5_ok` keeps its meaning. Fresh mode (stack = false) runs R + 1 harness passes (≈ 20 min each) — R = 1 ≈ 40 min, R = 2 ≈ 60 min; stacked mode runs one pass plus R in-place edits (≈ 25–30 min).

**What you CANNOT do:** modify `run_iteration.py`, the harness, the engine (`memit_dry_run/`), the evaluation, the stimuli, or install packages. One knob set per iteration; record what changed.

**The goal:** maximize `heldout_full` (A7 held-out full-sequence recall, /72) **subject to the guards**. Guards (MUST hold or the iteration is INVALID and discarded regardless of the metric): `A1 >= 68`, `A2 >= 68`, `L1_flips <= 1`, `frame_flips <= 2`, `described_as >= 85.0`, `L3 >= 29`, `ppl_post <= 22.2`, `law5_ok == true`, `cap_ok == true` (stacked write cap achieved within 5 %; always true without a cap). Report `canon`, `dw_ratio` and `ref_heldout` (the iteration's own pass-0 single-edit reference, /72) beside the metric; they do not bind.

**Keep policy:** keep if `heldout_full` improves by ≥ 3/72 over the current best with all guards true; otherwise discard. **Simplicity criterion** as in the fork: a 3-hit gain from a simpler knob set beats a 4-hit gain from a baroque one.

## Output format

The script prints:

```
---
heldout_full:   21
canon:          12
A1:             72
A2:             71
L1_flips:       0
frame_flips:    1
described_as:   85.10
L3:             30
ppl_post:       21.67
dw_ratio:       1.31
law5_ok:        true
cap_ok:         true
ref_heldout:    13
seconds:        1980
```

Extract with `grep "^heldout_full:\|^A1:\|^A2:\|^described_as:\|^L3:\|^dw_ratio:\|^law5_ok:" run.log`.

## Logging results

`results.tsv` (tab-separated), header and 7 columns:

```
iter	knobs_sha	heldout_full	guards	status	dw_ratio	description
```

`knobs_sha` = sha256 of `knobs.json` (first 8 hex); `guards` = `ok` or the failing guard names; `status` = `keep`, `discard`, `invalid`, or `crash`. Snapshot the knobs of every iteration to `results/autoresearch_reaim/<tag>/knobs_<iter>.json`.

## The experiment loop

LOOP until the iteration cap (**12**, DISCIPLINE §3) or until the operator interrupts:

1. Read the current best (results.tsv) and the knobs.
2. Change `knobs.json` with one experimental idea (write the idea into the description).
3. Snapshot the knobs; run the iteration; read the summary.
4. Empty summary → crash: `tail -n 50 run.log`, fix only if trivial (a typo in knobs), else log `crash` and move on.
5. Log the row. Keep or discard by the policy.
6. **NEVER STOP to ask** whether to continue; the operator is asleep. Stop only at the cap, on a HALT (fingerprint FAIL, LAW#5 not inert, a guard that fails on the *baseline* iteration — then write `HALT.md` in the results folder and stop), or on interruption.

When the loop ends, write `results/autoresearch_reaim/<tag>/SUMMARY.md`: the table, the best knobs, and the ONE candidate (if any) worth a pre-registered falsifier — stated as a candidate, with the guard values beside it. That file is the hand-off to the operator; nothing else is written.
