## Review — C10J AnyEdit Reset Stage-1 Prereg

**VERDICT: FIX-FIRST** (consistent with the earlier advisor return the gate cites). The core design is sound and actually *fixes* the C10h epistemic error — but there are concrete researcher-degrees-of-freedom and cheaper-test gaps to close before any harness is written.

### Single most important thing to do next
**Run the cheapest decisive probe first, and pin the locality metric.** Before authoring a fresh "source-faithful" runner, re-run the *existing* C10h harness (`experiments/track_c/c10h_anyedit_pilot.py`) on **A1/A2 only with upstream `window_size` (≈50) instead of 1**. The C10h collapse (93.1/97.2 → 0.0/0.0) happened at `window_size=1`, which defeats AnyEdit's entire autoregressive-window mechanism — so the most likely cause is the window, not port unfaithfulness. This single-knob run either kills the local route cheaply or de-risks the build with one input change instead of a new runner. Falsification-first says try the thing that can fail cheapest first.

### Issues in priority order

1. **Locality metric is unpinned (FIX-FIRST, DOF leak).** The threshold reads "no more than 5pp below MEMIT … *or* no more than 5.0 points below reference on the existing C10 locality score scale." An "or" between two scales is exactly the post-hoc selection the prereg elsewhere guards against. Pick **one** locality metric now. Same issue, smaller: the behavior gate is *absolute* (80%) while locality is *relative-to-same-run-MEMIT* — reconcile the logic (see #4).

2. **A cheaper decisive test is missing (the window probe above).** The prereg jumps to "construct an A1/A2 parity runner" without first establishing that the documented collapse is even a port problem. Add an explicit Stage-0 window-knob run as the gate's first action.

3. **Local re-implementation re-introduces the exact failure mode that sank C10h.** "Method-port drift / local hybrid mistaken for upstream" is listed as your #1 confounder — and your remedy is to hand-build another local runner. The most source-faithful A1/A2 anchor is **running upstream AnyEdit code directly** (throwaway env; infra is pre-approved) and only then porting. The prereg defers "upstream runner investment" to the FAIL fork; it belongs *up front* as the faithfulness anchor, or you must justify why a re-implementation is more decisive than running the original. `UNVERIFIABLE` from here: whether the upstream env conflicts with the 4.51.0/Qwen pins — but that's a reason to test it, not to skip it.

4. **Single-run × documented ~50pp GPU-nondeterminism swing vs. an absolute 80% boundary.** Your own corpus records ~50pp run-to-run swings on held-out reads. A single seed/order landing near 80% may be noise. This is *partly* mitigated **only if** A1/A2 are novel **inserts** (insert-robust, near-ceiling, stable) rather than counterfactual **updates over priors** (the fragile/swinging case). The prereg never states which A1/A2 are. **Make insert-vs-update status explicit**; if any A1/A2 is an update, a single run at the boundary is unsafe — require a confirmatory re-run on any result within ~10pp of 80%, or bind to "within Xpp of same-run MEMIT" so the noise is differenced out.

5. **Elevate repo verification to a pre-harness checkpoint.** "Confirm `jianghoucheng/AnyEdit` exists, is the LLM (not image) path, record the commit" is buried as Stage-1 step 1, yet it gates everything and your own history (the fabricated-arXiv-id near-miss) says verify external artifacts *before* effort. Make it the literal first gate; if it fails, no runner is written.

6. **Minor.** "No material expression/locality movement under no-op" — "material" is undefined; bind it to the standard LAW#5 tolerance (|Δexpr|≈0) rather than a word.

### What's genuinely right (keep)
- **A1/A2-must-recover-before-A7 with a `hard_case_licensed:false` lock** is the correct fix for the C10h error (interpreting an A7 number from a harness that had destroyed the easy controls). This is the spine of the gate and it holds.
- **`para_full` as the binding metric** is the right read-correctness measure; canonical/first-token/norms-as-diagnostics-only is correct.
- **Bias-fencing of C10h** (failure-modes-only, not thresholds/interpretation) and **one-fix-then-halt** are well-stated.
- **Drift check: passes.** This advances the live §0.3 C10 falsifier and the F1 in-weight-vs-side-store question, and the decision-meaning table correctly refuses to over-claim (a pass upgrades only the tested write/serve tuple, not read/governance/scale).

Resolve #1 (pin locality) and #2/#3 (cheapest probe + upstream anchor) and this is a clean PROCEED. Evidence remains binding over this opinion.
