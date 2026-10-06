# Overnight plan 2026-10-06 → 07: the stacked arm, then a fenced autoresearch loop over the re-aim family (unattended)

**Operator instruction (2026-10-06, before sleeping):** pull the macOS PyTorch fork of Karpathy's autoresearch and set the next session up to run the science overnight on its own: the stacked arm first, then the autoresearch loop over the re-aim knobs, logging candidates. This plan is the hand-off; the next agent executes it in order and does not stop to ask.

## What is in place

- `external_prior_art/autoresearch-macos/` — the fork to use (miolini; PyTorch SDPA on MPS; head 537c6e6, 2026-03-17). `external_prior_art/autoresearch-upstream/` — karpathy's original (head 228791f, 2026-03-25), **diff reference only, never run** (needs an NVIDIA GPU). Both untracked in git (the folder is the program's external-artefact area).
- `experiments/track_c/autoresearch_reaim/program.md` — the fork's `program.md` conventions adapted to the C10 edit harness (one editable `knobs.json`, a fixed per-iteration script, one metric with hard guards, `results.tsv`, a loop that never stops to ask, iteration cap 12, STAGING output only). The fork's git keep/revert is replaced by knob snapshots: the program's branch stays a science ledger.
- NOT yet written: `experiments/track_c/autoresearch_reaim/run_iteration.py` and `knobs.json`. The next agent writes them from the existing drivers (`c10p_twopass_arms.py` for the fresh re-aim, `c10q_stacked_arms.py` for the stacked path, the `Z_OVERRIDE` / `_ARM_STATE` seams) — a thin orchestration that reads `knobs.json`, runs ONE edit experiment (A1 + A2 + A7, LAW#5 gate, locality axes, same-frame probe), and prints the summary block in `program.md`. Implementation review by Codex before the first iteration (the review is cheap; the loop is not).
- The band-search loop from June (`experiments/track_c/autoresearch_band_search/`) is the pod-era version and is NOT the template; the fork's conventions are.

## The fence (binding; DISCIPLINE §3, AUTONOMY.md "fenced units")

The loop is an optimizer. Its output is **candidates only**: `results/autoresearch_reaim/<tag>/{results.tsv, knobs_*.json, SUMMARY.md}`. It never writes `CORPUS/`, the runbook, the checkpoint, the ledgers, the hypothesis register or memory. A "keep" is not a result. The morning hand-off is `SUMMARY.md`; the operator (HIL) decides which candidate, if any, becomes a pre-registered falsifier with controls, advisor passes and the strict held-out bar. The guards exist so the optimizer cannot "win" by damaging the model; a guard failing on the baseline iteration is a HALT.

## Order of operations for the next session (unattended after step 1's advisor pass)

1. Advisor pass on amendment Q1 of `docs/C10Q_STACKED_SOLVE_PREREG.md`; fold; run D-C10q-stacked (three passes, ≈ 2.2 h); read; verdict pass; CORPUS/50; close-out ALL GREEN; commit; push.
2. Write `run_iteration.py` + `knobs.json` (baseline = the CORPUS/49 fresh two-pass configuration: `resolve_rounds 1, stack false, write_cap null, z_blend 1.0, layers [4,8], ridge 1.0`); Codex implementation review; fold.
3. Start the loop per `program.md` (tag `reaim-oct06`), cap 12, ≈ 25–40 min per iteration → 6–8 hours. Suggested first ideas in order: baseline → `stack true` (if CORPUS/50 was not NULL) or `write_cap 0.75` → `z_blend 0.5` → `resolve_rounds 2` with `write_cap 0.75` → `layers [4,10]` → `ridge 2.0` → combinations of the two best. Record every iteration; keep by the policy; never stop to ask.
4. In the morning: `SUMMARY.md` + a HIL report in chat (what was tried, the best knobs, guard values, the one candidate or "none"). Then the research pass per D-C10q-rulings-1 if the stacked arm was NULL — nothing moves from Qwen without it.

## Risks named now

- Per-process spread on the metric is ± 4–5/72; a 3-hit keep threshold will produce false keeps. That is acceptable for a candidate generator and is why nothing it finds counts until a pre-registered run with controls.
- An iteration is an edit experiment (≈ 30 min), so the overnight budget is ~12 iterations, not the fork's ~100.
- The Ollama server on this Mac can load unrelated models and slow runs (wall-clock only).
- A fresh session's background processes die with the session; the loop must run inside the session that started it (the Bash tool's background mode), with until-loops that name only files the loop creates.
