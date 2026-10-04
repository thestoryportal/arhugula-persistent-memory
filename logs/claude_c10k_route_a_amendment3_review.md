Note on method: I couldn't load a `laws:*` skill because there's no Skill tool in this session, so I applied prose discipline by hand. The verdict comes first, each claim is tagged EVIDENCE-SHOWS, I-INFER or UNVERIFIABLE, and each issue ends in something to do. Graft was denied in don't-ask mode and I have no file-read tools, so I could not open any artifact. Every number below is checked only for consistency with the amendment's own text. Nothing was confirmed against `solve_gain_diag.json`, `AlphaEdit_ARE_main.py:128-130` or the result JSONs; treat all of them as **UNVERIFIABLE by this reviewer**.

---

## Verdict: **FIX-FIRST**

## The single most important thing

Before the rerun, run one offline check on the recorded A1/A2 keys and residuals, with no edit outcome involved:

- **(a) Back-test the diagnostic.** At L2=10, does the diagnostic reproduce the halted run's observed numbers? Those are update norms 4.2 / 4.9 / 7.5 / 20 / 51 and a z-error falling 98 → 87.
- **(b) Check the solve's precision.** At L2=0.01, does the module's fp32-on-MPS solve match an fp64-on-CPU solve of the same system? Compare relative error of `upd` and of the realised fractions.

If (a) fails, the calibration quantity behind the rule hasn't been shown to describe the module, and the rule has no footing. If (b) fails, the rerun measures rounding error, not AnyEdit. Both run in seconds.

---

## Issues, in priority order

**1. Conditioning at L2=0.01 in fp32 may be fatal. (I-INFER from §2's own numbers.)**
`A = P(KKᵀ+KpKpᵀ) + L2·I`. On the subspace P removes, the eigenvalues of A are about L2, while the top eigenvalue at L4 is 231,128. At L2=0.01 that gives a condition number of about 2.3×10⁷. At L2=0.001 it is 2.3×10⁸. fp32 has roughly 7 significant digits, so the L4 solve may have no correct digits.
- The diagnostic's tables don't settle this. They may have been computed in a different precision or by a different solve routine. **UNVERIFIABLE** which one was used, so state it.
- The re-run D5 anchor is the right instinct. But its pass criterion under the new L2 isn't pre-registered. Say now what an anchor failure means (halt, or fp64 solve as a pre-declared fallback). Otherwise it becomes a second "fix".

**2. The 231,128 top eigenvalue at L4 probably comes from a single huge preservation key. (I-INFER.)**
With mean ‖k‖² of about 48 across 266 keys, an eigenvalue of 231k needs a key with norm around 480. That looks like the BOS / attention-sink position inside `Kp`. If so:
- it alone sets the condition number;
- its preservation constraint is the one most likely to be numerically violated at small L2;
- the "every layer" rule is then being bound partly by an artifact.

Find out which key drives the top eigenvalue at L4 and L7 before the rerun.

**3. The amendment says the projector is not the problem; its own table says otherwise.**
§1 says the failure is "not in … projector". §2 shows P removes 80–95 % of edit-key energy: A1 L8 ‖k‖²=565 → ‖Pk‖²=33; L4 48 → 9.1. The weak solve is "ridge ≈ projected energy". Either side of that ratio could be the outlier, and the projector is the Amendment-1-rescaled one.
- Consequences:
  - §4's claim that "the official AnyEdit setting on this model is now known to be non-functional at L2 = 10" is over-stated. It is non-functional at L2=10 **combined with the Amendment-1 threshold and fp32 on MPS**.
  - Shrinking the ridge 1000× to make up for a projector that strips most of the key energy forces large weight updates along low-variance key directions. That is exactly where locality damage would hide.
- Cheap check: report ‖Pk‖²/‖k‖² under upstream's original threshold. If it is much higher, the localized fix belongs on the threshold, not on L2. That needs an operator call, because only one fix is allowed.

**4. The 0.85 threshold rests on a "compounding" argument that is probably wrong.**
In MEMIT-family solves, each layer recomputes the current residual after earlier layers have been applied. Its target is (z − cur)/(remaining layers), so an early-layer shortfall is carried forward to later layers rather than compounded.
- If that holds here, the binding constraint is mainly L8. A1 L8 already reaches 0.943 at L2=0.03, so the rule picks a ridge 3× smaller than necessary, which raises the risk in issue 1.
- **LAW #4:** `cat -n` the AnyEdit layer loop and confirm whether `cur_zs` is recomputed per layer before keeping this rationale.
- Separately, the rule was written after the calibration table existed. That is acceptable, because no edit outcome entered. But disclose it, and note that the outcome is robust: any threshold in (0.709, 0.868] gives 0.01.

**5. The calibration measures fit on the edit keys; the gate measures paraphrase.**
The gate is `para_full ≥ 80`, but the realised-fraction diagonal is computed on edit-window keys only. A smaller ridge fits those keys more sharply and may transfer *less* to paraphrase keys.
- The halted run's pattern, canon 11/24 versus para 0/72, fits both readings: "too weak everywhere" or "paraphrase keys lie outside the edited subspace".
- Cheap falsifier: compute the transferred fraction `R·Kᵀ P A⁻ᵀ k_para` on paraphrase keys at L2 = 10 and 0.01. **Record it only as a pre-run prediction; do not use it to choose L2**, since that would leak the eval set.
- If the predicted transfer stays far below the gate at L2=0.01, the rerun is likely to fail. That makes an informative prediction, not a reason to change the fix.

**6. "Mean diagonal" isn't quite "realised residual".**
The realised change is `R·M` with `M = Kᵀ P A⁻ᵀ K`. The diagonal ignores off-diagonal terms, which are large when several keys come from overlapping window positions of one sequence.
- Use ‖R·M − R‖_F / ‖R‖_F on the halted run's actual residuals. This is the same computation as the back-test in the top action.
- Report the per-item minimum alongside the mean, because the gate is per item.

**7. Locality is too weak to detect the damage this fix makes likely.**
At about 50× larger update norms (I-INFER), 11/12 real-country probes plus one JS number won't detect broad damage.
- Record a held-out perplexity / fluency number on generic text as a **diagnostic, not a gate**. Adding a gate now would itself be a post-hoc change.
- §3 already says a locality break is "recorded as such, not as recovered". Good; keep that.

**8. Scope and the stop rule.**
- The prereg permits a "launcher/data fix". An L2 change alters the solve, which is the science path under LAW #5. Record explicitly that the operator accepts an hparam change as falling inside "launcher/data". Otherwise a later reviewer can fairly call this a second, unsanctioned kind of change.
- This is also the third amendment to the solve's operating regime (threshold, dtype, L2). Each is defensible alone; together, a PASS tests "an AnyEdit-shaped solve tuned to this model", not AnyEdit.

**9. Drift (F1).**
- A PASS gives a mechanism lead with weak external validity, for the reason in issue 8.
- The most F1-useful output may already be in hand: on a 3B base model, the AlphaEdit-family null-space projection removes 80–95 % of edit-key energy at L4–L8. That is a statement about how much room the null space leaves on this model.
- Make sure that number is written to CORPUS whichever way the rerun goes. It survives both outcomes, and it is the finding most at risk of being lost if attention stays on rescuing the gate.
