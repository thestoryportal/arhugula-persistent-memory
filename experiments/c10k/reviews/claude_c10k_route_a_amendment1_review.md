**Verdict: FIX-FIRST.**

Changing one layer's threshold is a reasonable fix, and the amendment keeps edit outcomes out of the selection. Three things still need fixing before the projector stage re-runs:
- The L8 pass is marginal.
- The pass was measured on the same A1 keys whose edits the amendment will then grade.
- The argument that this is a "minimal departure" may not hold for this model.

*Scope of this review:* my one attempt to open the repo (a graft search for the projector-stage code) was denied, so I could not read any files. Every number below comes from the amendment's own tables. Anything that depends on source code is marked **UNVERIFIABLE (not read)**.

## The single most important thing to do next

**Check that L8 at 0.03 still passes on keys it wasn't tuned on.** This is cheap: no edit, only CPU projector maths on a matrix that already exists.
- Take a set of edit-like keys that is not in A1, A2 or A7: last-prompt-token inputs on new fictional subjects built the same way as A1. Measure L8 survival and protection at 0.03.
- Also bootstrap the 24 A1 keys to get a confidence interval on survival = 0.241.
- If the interval's lower end, or the held-out survival, drops below 0.2, the D8 fix is fitted to these 24 keys rather than a real property of L8. Re-halt in that case.

Pre-register this as part of D8 now, before running it.

## Issues, most important first

**1. The L8 pass is marginal and was selected using the keys A1 will be graded on.** EVIDENCE-SHOWS (§1 table): L8 at 0.03 gives survival 0.241 against a bound of 0.2, and protection 0.465 against a bound of 0.5. Both margins are under 0.05, and survival is averaged over only n=24 keys.
- No A1 outcome was used, but the projector was still chosen so that *those exact A1 keys* get through. That is key-level leakage. A1's edit success under D8 will partly reflect this tuning.
- The §3 wording "no A1/A2/A7 outcome has been computed" is accurate but does not cover this.
- Also check: is "survival" a ratio of summed norms or a mean of per-key ratios? **UNVERIFIABLE (not read).** If it is a single aggregate, a minority of A1 keys could pass the 0.2 bound well while most fall below it. Report the per-key spread.

**2. The "minimal departure from the shipped value" argument may not hold.**
- From memory of AlphaEdit's `get_project`, I believe upstream applies `nullspace_threshold` to the raw eigenvalues of its covariance. If so, 0.02 means something specific to the 7B model's activation scale.
- This port applies 0.02 to a *normalised* 3B covariance (prereg D4). Unless D4's normalisation is shown to match upstream's eigenvalue scale, 0.02 on this model is already an arbitrary point. In that case "L4–L7 kept at the shipped value" does not buy the comparability with upstream that §3 claims.
- Fix: cite the exact line in D4 and in upstream's `get_project` (**UNVERIFIABLE (not read)**). If the scales differ, restate the rationale honestly: "one fixed reference value, departed from as little as possible." The rule still stands without the comparability claim.

**3. The rule was written after the sweep was seen.** The heading says "rule fixed before any outcome is seen". That is true for edit outcomes, not for gate outcomes: the sweep, which picks out L8 = 0.03, was in hand when "minimal departure" was chosen over "maximise protection".
- Say this plainly in §3, e.g. "rule chosen post-sweep, pre-edit."
- The choice of sweep grid also matters. "Next larger sweep value" depends on a grid of 0.005, 0.01, 0.02, 0.03, 0.05 and 0.1. A value such as 0.025 might pass L8 with better protection. State whether the grid was set before the halt. If it wasn't, fix the grid in the amendment.

**4. The survival gate may measure the wrong keys (real-criterion check).** Survival is measured on last-prompt-token keys. AnyEdit edits long outputs window by window, so the keys it actually writes are at several positions per window, not only the last prompt token.
- If those keys sit differently relative to the protected subspace, passing the gate does not show that the real edit survives the projector.
- This flaw is inherited from the parent prereg, but D8 now relies on that gate to justify a change. Add one survival check on keys from the real AnyEdit windows at L8 (same CPU-only cost as the main check).

**5. Check the launcher wiring against the sweep.** `--thresholds 0.02,0.02,0.02,0.02,0.03` has to map to L4→L8 in order. The sweep script and the launcher are separate code paths.
- When the projector stage re-runs, the launcher's own gate output must reproduce the sweep's numbers (L8 0.465/0.241; L4–L7 matching the 0.02 row) to about 1e-3 before any edit runs.
- Pre-register this as a parity check. A mismatch means HALT.

**6. Minor points.**
- The §2 I-INFER explanation (fictional-subject keys concentrate in directions Wikipedia also uses) is plausible but untested, and nothing in D8 depends on it. Keep it labelled I-INFER and keep it out of CORPUS.
- The parent-FAIL clause gains "per-layer threshold" as a sensitivity axis. Bound that so it can't turn into open-ended tuning: one sensitivity cell (R1-S), diagnostic only, as written.
- On drift: whether Route A is a live §0.3 falsifier for the F1 determination is **UNVERIFIABLE (not read)**. Confirm it against §0.3 before spending more compute on it.

## What would turn this into PROCEED

Pre-register three checks as part of D8:
- the held-out-key and bootstrap check from the top section;
- the window-position survival check (#4);
- the launcher parity check (#5).

Then, in the text, fix the D4 scale claim (#2) and label the rule as written post-sweep (#3).

If the held-out check passes, D8 is defensible. If it fails, the honest result is that this projector design has no threshold that both protects knowledge and lets edits through at L8 of this model. That is itself a scoped finding, and better than a tuned pass.
