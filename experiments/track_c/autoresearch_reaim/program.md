# autoresearch — re-aim family on the C10 edit harness (Karpathy's `autoresearch` via the macOS fork `external_prior_art/autoresearch-macos/program.md`, applied to one edit experiment instead of a 5-minute training run)

This is an experiment to have the LLM do its own research. The structure is the fork's, followed exactly (operator instruction 2026-10-06: follow the repo durably and exactly; this file is the one layer the fork assigns to the human). Three files matter: one fixed evaluation you never touch, one editable unit, and this program. The agent modifies the editable unit, runs one experiment, checks if the result improved, keeps or discards, and repeats — until the human interrupts it.

**Fence (the human's layer, DISCIPLINE §3):** this loop is an optimizer. Everything it produces is a CANDIDATE. It never writes `CORPUS/`, the runbook, the checkpoint, the ledgers, the hypothesis register or memory; its outputs live under `results/autoresearch_reaim/<tag>/` (and, when git is available, on its own branch). The operator folds a candidate in through a pre-registered falsifier with controls. Operator authorization: D-C10q-rulings-1 companion, 2026-10-06.

## Setup

To set up a new experiment:

1. **Agree on a run tag**: `reaim-<date>` (e.g. `reaim-oct06`). The branch `autoresearch/<tag>` must not already exist — this is a fresh run.
2. **Create the branch**: `git checkout -b autoresearch/<tag>` from the program branch. *(When git is unavailable to the loop — as on 2026-10-06, when the session's shell lost git — the branch is replaced by per-iteration snapshots of the editable unit under `results/autoresearch_reaim/<tag>/iter_NN/`; "commit" = snapshot, "git reset" = restore the last kept snapshot. The fallback is recorded in `results.tsv` by `unit_sha` in place of a commit hash.)*
3. **Read the in-scope files.** The scope is small:
   - **`run_iteration.py`** + **`knobs.json`** — **the editable unit (the fork's `train.py`).** It builds one re-aim edit experiment on top of the harness: parses `knobs.json`, writes the iteration's hparams, runs the harness pass(es) through the `Z_OVERRIDE` / `_ARM_STATE` seams, applies the extra edit(s), prints the summary. Everything in it is fair game: the knob schema, the number and kind of re-solve rounds, how targets are blended or scaled, the write cap and its enforcement, the band, the ridge, the compute_z steps, where the extra edit is aimed, new ideas.
   - **`experiments/track_c/c10e_bandknob.py`** — **the fixed evaluation (the fork's `prepare.py`).** Stimuli, `eval_arm` (the held-out full-sequence metric), the locality axes, the LAW#5 parity gate, `my_edit`. Do not modify.
   - **`log_row.py`** and the launcher — fixed. The logger extracts the metric and guards and appends the row.
   - `CORPUS/48`, `CORPUS/49`, `CORPUS/50` — what has been measured: the single edit lands 12–16/72 held-out; a fresh second edit aimed at the re-solved target reached 21/72 at a ×1.31 write; a stacked second edit reached 24/72 at ΔW₂/ΔW₁ 1.24 with a 4.2-point `described_as` cost; a wrongly-aimed second edit of larger energy destroys recall (0/72).
4. **Verify the gates**: `python3 tools/engine_fingerprint.py` prints PASS; `results/c10l_covgeom/run1_armB_identity.json` exists (LAW#3 reference). If not, tell the human.
5. **Initialize `results.tsv`** with just the header row. The baseline is recorded after the first run.
6. **Confirm and go.** Kick off the experimentation.

## Experimentation

Each experiment runs on this machine's single GPU (MPS). It is one edit experiment with fixed stimuli and a fixed evaluation; its duration is **≈ 25–50 minutes** (fresh mode = R + 1 harness passes of ~20 min; stacked mode = one pass + R in-place edits). You launch it through the fixed launcher: `bash <launcher> <iter> "<description>"` (it snapshots the editable unit into `iter_NN/`, runs the script with everything redirected to `iter_NN/run.log`, then runs the logger).

**What you CAN do:**
- Modify `run_iteration.py` and `knobs.json` — the solve recipe, its parameters, its structure. Everything is fair game.

**What you CANNOT do:**
- Modify `c10e_bandknob.py`, anything under `memit_dry_run/` (the engine; its fingerprint is a hard gate), the stimuli, the evaluation, `log_row.py`, the launcher, or install packages. Monkey-patching the harness's evaluation from inside the editable unit counts as modifying the evaluation.
- Vary behaviour through environment variables: the launcher's environment is a fixed contract; only the editable unit differs between iterations.
- Write anywhere outside `results/autoresearch_reaim/<tag>/` and the editable unit.

**The goal is simple: get the highest `heldout_full`** (A7 held-out full-sequence recall, /72) — subject to the guards: `A1 >= 68`, `A2 >= 68`, `L1_flips <= 1`, `frame_flips <= 2`, `described_as >= 85.0`, `L3 >= 29`, `ppl_post <= 22.2`, `law5_ok == true`, `cap_ok == true`. A guard failure makes the run `invalid` (it cannot be kept). These are the fork's "VRAM is a soft constraint" made hard, because a win that damages the model is not a win here. `canon`, `dw_ratio` and `ref_heldout` are reported beside the metric; they do not bind.

**Simplicity criterion**: all else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it; equal or better results from deleting code is a great outcome. Weigh complexity against improvement.

**The first run**: always the baseline — the editable unit as is.

## Output format

When the script finishes it prints:

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

Extract the key metric from the log: `grep "^heldout_full:\|^dw_ratio:" iter_NN/run.log`.

## Logging results

When an experiment is done, log it to `results.tsv` (tab-separated, NOT comma-separated — commas break in descriptions). Header and 5 columns, the fork's shape:

```
commit	heldout_full	dw_ratio	status	description
```

1. commit = git short hash of the editable unit's commit; when git is unavailable, the 8-hex `unit_sha` of the snapshot
2. `heldout_full` achieved (/72) — `0` for crashes
3. `dw_ratio` (two decimals) — `0.00` for crashes
4. status: `keep`, `discard`, or `crash` (`invalid` = a guard failed; it is logged with the failing guard names appended to the description and treated as a discard)
5. short text description of what this experiment tried

The logger writes the row from the run's output; you supply the description.

## The experiment loop

LOOP FOREVER:

1. Look at the state: the current branch/commit (or the last kept snapshot) and `results.tsv`.
2. Tune the editable unit with an experimental idea by directly editing the file(s).
3. Commit (or let the launcher snapshot).
4. Run the experiment through the launcher; wait for `iter_NN/ITER_DONE` (poll the file in bounded calls).
5. Read out the results: `grep "^heldout_full:\|^dw_ratio:" iter_NN/run.log`.
6. If the grep output is empty, the run crashed. `tail -n 50 iter_NN/run.log`, read the stack trace and attempt a fix. If you can't get things to work after more than a few attempts, give up on that idea.
7. The row is recorded (`cat iter_NN/row.txt`).
8. If `heldout_full` improved (higher) with every guard true, you "advance" the branch, keeping the commit/snapshot: the editable unit as it stands is the new base.
9. If `heldout_full` is equal or worse, or a guard failed, you git reset back to where you started — i.e. restore `run_iteration.py` and `knobs.json` from the last kept snapshot.

You are a completely autonomous researcher trying things out. If they work, keep. If they don't, discard. You advance so that you can iterate. If you feel stuck, you can rewind, but do this very sparingly (if ever).

**Timeout**: each experiment should take ~25–50 minutes. If a run exceeds twice that (**90 minutes**), kill it (`pkill -f run_iteration.py`) and treat it as a failure (discard and restore).

**Crashes**: use your judgment. Something dumb and easy (a typo, a missing import, a wrong key) — fix it and re-run. A fundamentally broken idea — skip it, log `crash`, restore, move on.

**Broken instrument (not an idea)**: fingerprint FAIL, LAW#5 not inert on the baseline, or a guard failing on the baseline itself means the harness is broken, not the idea — write `HALT.md` in the results folder and stop; that is the one case where stopping is right.

**NEVER STOP**: once the experiment loop has begun (after the initial setup), do NOT pause to ask the human if you should continue. Do NOT ask "should I keep going?" or "is this a good stopping point?". The human might be asleep, or gone from a computer, and expects you to continue working *indefinitely* until you are manually stopped. You are autonomous. If you run out of ideas, think harder — re-read CORPUS/48–50 for what the measurements say, re-read the harness for what the solve actually does, try combining previous near-misses, try more radical changes to the solve recipe. The loop runs until the human interrupts you, period.

A user might leave you running while they sleep: at ~40 minutes per experiment that is roughly 10–12 experiments over a night, all completed by you while they slept.

**Hand-off file**: keep `results/autoresearch_reaim/<tag>/SUMMARY.md` current — rewrite it after every kept iteration and after every fifth iteration — so the human can read the loop's state at any moment without stopping it: the table, the best kept unit (its snapshot/commit and the diff from the baseline in words), the guard values beside the best result, and the ONE candidate (if any) worth a pre-registered falsifier, stated as a candidate, never as a result.
