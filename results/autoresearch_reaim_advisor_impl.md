`FIX-FIRST`

Single most important next action: make the launch/fence path clean before starting overnight: pre-create `iter_NN/` before shell redirection, and stop importing driver scripts for helper functions.

Priority issues:

1. **First iteration can fail before Python starts.** `program.md` tells the loop to redirect stdout to `results/autoresearch_reaim/<tag>/iter_<NN>/run.log`, but `run_iteration.py` only creates that directory after Python starts. Shell redirection opens the log first, so the prescribed command can fail if the directory does not already exist. Cite: `experiments/track_c/autoresearch_reaim/program.md:14`, `experiments/track_c/autoresearch_reaim/run_iteration.py:28`.

2. **Fence is not clean: helper imports have top-level side effects outside the autoresearch tree.** `run_iteration.py` imports `FRAME_SUBJECTS, frame_probe` from `c10p_twopass_arms.py`; that driver creates `results/c10p_twopass` at import time and rewrites env identity fields. Cite: `run_iteration.py:77`, `c10p_twopass_arms.py:11-19`. Because `c10e_bandknob` has already snapshotted its module globals, the main harness identity likely survives; but “outputs only under `results/autoresearch_reaim/<tag>/...`” is false as written. Cite: `run_iteration.py:67-75`, `c10e_bandknob.py:31-35`.

3. **Write-cap “exactness” is over-claimed.** The cap assumes `my_edit` is linear in the residual, but `my_edit` recomputes `K` and `cur` inside a sequential per-layer loop after earlier layer writes, then updates cache afterward. That makes the full multi-layer edit at best locally/approximately linear, not exactly linear. Cite: `run_iteration.py:127-146`, `c10e_bandknob.py:194-220`. Cheapest fix: after the capped redo, compute the actual `dw_total(d) / dw1_total` and hard-fail or mark invalid if it exceeds cap plus a small fp16 tolerance.

4. **dW₁ measurement is not exactly the harness `delta_norm`.** The stacked hook measures effective weight difference from a base snapshot, while the harness reports `upd.float().norm()` before casting and adding to fp16 weights. That is close, but not exactly the same quantity. Cite: `run_iteration.py:161`, `c10e_bandknob.py:213-217`. Report it as effective fp16-applied norm, not exact harness update norm.

5. **Ridge wrapper wiring is technically correct, but `law5_ok` is narrower than the optimizer may imply.** `run_recipe` calls the module global `run_law5`, so the wrapper is used, and `my_edit` reads global `L2`, so `H.L2 = K.ridge` reaches the solve. Cite: `run_iteration.py:114-124`, `c10e_bandknob.py:463`, `c10e_bandknob.py:209`. But the LAW#5 gate always runs at `L2=1.0`, so `law5_ok` validates default harness parity, not ridge-modified candidate parity. Fine for a fenced candidate generator; not evidence.

6. **Fresh-mode state handoff looks correct.** Pass 0 resolves `z_next` on the edited model, pass `k` aims at the previous pass’s blended target, and `resolve_rounds=0` leaves `dw_ratio=1.0` against its own pass-0 reference. Cite: `run_iteration.py:155-158`, `run_iteration.py:209-218`, `run_iteration.py:188-199`.

7. **Logger guards match `program.md`.** The thresholds in `log_row.py` match the guard list in `program.md`, and keep/discard uses `+3/72` over best kept. Cite: `log_row.py:6-23`, `program.md:20-22`.

Drift check: this advances F1 only as a fenced optimizer for C10 candidates, not as evidence. That framing is correct in the plan and program, but the fence/import issues should be fixed before the overnight run. Cite: `docs/AUTORESEARCH_REAIM_OVERNIGHT_PLAN.md:10-18`, `EXPERIMENT_RUNBOOK.md:42-45`.

🌱 graft saved ~13,019 tokens this turn.