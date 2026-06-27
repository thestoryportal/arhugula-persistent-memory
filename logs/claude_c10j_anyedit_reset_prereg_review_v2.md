## Second-pass review — C10J AnyEdit Reset prereg

**Verdict: PROCEED** (to Stage-0 actions only).

All five FIX-FIRST items from the prior pass are resolved in the text:

1. **Locality metric pinned** — now consistently "the existing C10 locality score scale," with concrete thresholds (`≤5.0` pts below same-run MEMIT reference; `abs(delta_loc) ≤ 3.0` for inertness). ✓ *(Minor: the doc references the scale but never names what it is — defers to the C10 harness. Fine as de-dup discipline; resolve before the runner, not before Stage-0.)*
2. **Stage-0 window_size=50 probe** — explicit as ordered step 1, with its own artifact (`results/c10j_anyedit_window50_controls.json`) and a "Window-size false cause" confounder row. ✓
3. **Repo verification / upstream feasibility before local runner** — required order now puts repo-verify (step 0) and direct-upstream A1/A2 anchor (step 2) ahead of any new runner (step 3). ✓
4. **Insert-vs-update explicit** — Power/MDE section mandates A1/A2 be recorded as **novel inserts**, with a rerun rule if any item is an update over a prior. ✓
5. **No-op materiality defined** — `abs(delta_expr) ≤ 0.01`, `abs(delta_loc) ≤ 3.0`, no tensor changes in a pure no-op path, finite layer deltas. ✓

**Why PROCEED and not FIX-FIRST:** Stage-0 is exactly the three cheapest, can't-corrupt-science actions (repo verify, existing-harness window50 control probe, throwaway upstream smoke). None touch the science path, none license A7, and the design is genuinely falsification-first: the window50 probe is the cheapest thing that can overturn the entire motivation. The decision gate's bias rule (null = bounded hybrid; C10h numbers don't set thresholds) and bounded PASS meaning (licenses only an A7 addendum, closes no other spec layer) keep it anchored to F1. The C10h baselines cited (93.1/97.2 → 0/0; A7 12.5→1.4) match the canonical §0.3 record.

**Single most important next action:** Run the **Stage-0 `window_size=50` A1/A2 control probe on the existing C10h harness first** — it is the load-bearing falsifier. If default-window recovers A1/A2 with the *existing* harness, the C10h collapse was a window-setting artifact, not method-port drift, and the entire new-runner/parity effort is reframed (or unnecessary) before any of it is built. Do repo-verify (step 0, trivially fast) alongside it, but let the window50 result gate whether step 3 onward is worth authoring.

**One item to carry (non-blocking for Stage-0):** name the single locality metric explicitly in the prereg before the parity runner is written, so the `5.0`-point and `3.0`-point thresholds are unambiguous at verdict time.

Review is input; the saved Stage-0 artifacts and preregistered criteria bind.
