# D-C10s-sharedz: HALT at the LAW#5 inertness gate (2026-10-06, session 4d71207f)

**Verdict: HALT, nothing run past the gate.** Two of the five frozen inertness checks failed: (iii) triplicate and (iv) heterogeneous. Read-only diagnosis: the shared solve reproduces the engine's arithmetic. The frozen tolerances (1e-4) cannot be met at fp16 by any change in batch shape. The injection cell did not start. No science result exists; no label changes.

Records: `results/c10s_sharedz/inertness.json` (run identity inside), `architecture_profile/c10s_sharedz_halt_diagnostic.json` (the driver's halt record, left as written), log `results/c10s_sharedz_logs/inertness.log`. Preconditions met before the run: machine idle (no edit/prepare/safe-mode/ollama process), engine fingerprint PASS (d941a9fb, `_cov_cpu` 3).

## What the five checks returned

| Check | Result | Number |
|---|---|---|
| (i) floor: engine `compute_z` ×3, same process | pass | pairwise rel L2 = 0.0 → tolerance clamps to its 1e-4 minimum |
| (ii) `compute_z_shared([CANON])` vs engine | pass | rel 0.0, max-abs 0.0 (bit-identical) |
| (iii) `compute_z_shared([CANON]*3)` vs engine | **FAIL** | rel 0.122, max-abs 0.989 |
| (iv) `[CANON, T1, T2]` step-0 per-prompt NLL vs plain-forward reference | **FAIL** | max diff 0.0117 (tol 1e-4); lookup indices all correct; KL row last |
| (v) harness LAW#5 gate, `Z_OVERRIDE` unset | pass | Δexpr 0.0001, Δloc 0.30 |

## Why (iii) fails: amplified fp16 batch-shape rounding, not a code path difference

(ii) is bit-identical, so the function's code path equals the engine's when the batch is the same (7 rows). (iii) feeds 19 rows (18 rewriting + KL) of the same sentences. The model runs in fp16 (`c10e_bandknob.py:48`), and on MPS the kernels' rounding depends on batch shape. The trajectories, read from `inertness.json` `checks.{ii_single,iii_triplicate}.solve.history`:

- Step-0 NLL 8.4775 vs 8.4801 (Δ 0.0026), with identical inputs.
- The same shape all the way: both run the full 25-step budget (neither total loss reaches 0.05), both hit the clamp on 21 of 24 steps, both end at ‖delta‖ = max_norm = 49.06, final NLL 0.0140 vs 0.0156, fit 0.986 vs 0.985.
- Per-step NLL gaps stay below 0.09 throughout and below 0.003 at the end.

The end points still differ by 12 % relative L2 (max-abs 0.99) because delta sits on the clamp sphere for most of the solve. The loss is nearly flat along that sphere, so a small early gap moves the direction the optimiser settles on. The engine's z is therefore pinned down only up to roughly this spread under the engine's own budget. That is a property of the frozen engine, not of the driver. The check (i) floor measured run-to-run noise at a fixed batch shape (exactly 0 on this deterministic setup), so it could not absorb the batch-shape effect the prereg itself anticipated in (iii) ("the tolerance is measured, not assumed").

## Why (iv) fails: the same rounding, visible directly

The function's step-0 NLLs and the plain unpadded reference differ by up to 0.0117. The recorded same-padded-batch reference differs by 0.0137, and the two references disagree with each other by 0.0166. These are a few fp16 units at an NLL near 8. The parts of (iv) that catch indexing bugs passed: every lookup index matches, the KL row is last, 18 of 18 rewriting prompts are present, KL(ref‖init) is 1.0e-3 and the argmax agrees.

## Not concluded

- Nothing about the frame hypothesis (H-S1/H-S0): no shared target was solved for the 24 facts and none was injected.
- The diagnosis rests on one request (the inertness subject) and on the recorded trajectories. It reads the cause from the records and has not been tested by a fix.
- The driver was not changed. Under the halt rule (one speculative fix after a `cat -n` read, then HALT) and the operator's "HALT on any failure", no fix was attempted. Any fix changes a frozen gate and needs review first.

## What would let step 1 proceed (candidate, NOT adopted; needs the advisor + Codex before any run)

A post-freeze amendment A2 that replaces the bit-scale tolerances with criteria set by the measured batch-shape spread:

- (iii) passes if the step count, the stop reason and the clamp count match. Two more conditions: the final per-frame fit must agree within a stated margin, and the triplicate z and the engine z, injected by P6 on the canonical and held-out templates, must give the same full-sequence correctness for the inertness request.
- (iv) uses a tolerance derived from the disagreement between the two references (0.0166 here), for example 2× that spread, measured in the same process. The index and KL-row checks stay exact.

A rerun needs a new `OUT_DIR`, because the inertness script refuses an existing `inertness.json` and the driver binds the run to the inertness identity.
