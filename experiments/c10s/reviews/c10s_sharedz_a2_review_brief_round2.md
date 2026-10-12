# Review brief round 2 — D-C10s-sharedz amendment A2 v2

Same rules as round 1 (review only; no model load; edit nothing but your output file). Output file for Codex: **`results/c10s_sharedz_codex_a2_review_round2.md`**; for the Claude advisor: **`results/c10s_sharedz_advisor_a2_round2.md`**. Then say DONE.

## What changed since round 1
The tolerance draft is withdrawn. A2 v2 (`docs/C10S_SHARED_Z_PREREG.md` §7 A2) adopts Codex round-1 item 1's control for both (iii) and (iv), and moves the noise twin into the driver's cell 1 (Codex item 5).
- **(iii):** `compute_z_shared([CANON]*3)` vs the UNMODIFIED engine `compute_z(CANON request, R.ctx_triplicate(ctx))`, gated at the (i) tolerance; the 7-row vs 19-row engine distance is recorded.
- **(iv):** `compute_z_shared([CANON,T1,T2])` vs the unmodified engine on `{**rq, "prompt": "{}"}` with `R.ctx_heterogeneous(ctx, FRAMES)` (each context template `c` → `c.format(f)` for the three phrasings), gated at the (i) tolerance. Exact gates: `R.plan_matches` (the solve's ordered list equals `R.engine_plan`, a re-derivation of `compute_z.py:46-51` from the engine-side inputs, written apart from `build_prompt_plan`), lookup indices, row count, KL row last. The step-0 NLL references are recorded only.
- **(vi):** in `c10s_sharedz_arms.py` `injection_cell`, per fact, the twin = engine `compute_z(rq, R.ctx_triplicate(ctx))` on the driver's own `ctx`, injected on PTEST and paired with that fact's canonical held-out outcomes. `R.noise_twin_verdict` is admissible iff |twin gain| < 6 (the advisor's stricter form; the reverse screen is recorded). `R.cell1_outcome(fit, twin, screen)`: UNDERFIT, then NOISE-NON-DISCRIMINATING, then the screen. The result is persisted in `inject.json["noise_twin"]` and printed by the reader.
- Selftest: 11 tests, including model-free proof that `engine_plan(ctx_heterogeneous)` and `engine_plan(ctx_triplicate)` equal the harness plans, and that plan_matches rejects dropped contexts, CANON off row 0, a missing KL row, an extra duplicate and a swapped frame order.
- Stale text fixed (status line, validity wording, padded-reference docstring, A1's displaced sentence).

Diff: `/usr/bin/git diff HEAD -- docs/C10S_SHARED_Z_PREREG.md experiments/track_c/c10s_sharedz_arms.py experiments/track_c/c10s_sharedz_inertness.py experiments/track_c/c10s_sharedz_read.py experiments/track_c/c10s_sharedz_selftest.py`.

## Questions
1. Are your round-1 BLOCKING items resolved? Go item by item: resolved / not resolved / superseded, with evidence.
2. Is the engine-with-crafted-context reference truly the same batch? Check `compute_z.py:46-73` (prompt list, padding, targets, lookup indices, KL row) against `compute_z_shared`, including the bare `"{}"` prompt and any brace or format hazard in the sampled context templates.
3. Is parity at the (i) tolerance (floor-based, min 1e-4) safe from false halts? Is there any source of difference left between the two same-batch solves (for example, does `find_fact_lookup_idx` or `target_init` see different strings)?
4. Driver change: correctness of the twin's pairing (the twin's held-out hits paired with the same fact's canonical held-out hits, in PTEST order); the extra cost; anything the twin solve could disturb (the process-global context cache, the model state, the order of solves relative to the canonical/shared solves).
5. New blocking issues.

Output format as round 1: header line (reviewer, model, effort, date), **Verdict: PROCEED or FIX-FIRST**, numbered items with file:line, BLOCKING/ADVISORY, the exact fix.
