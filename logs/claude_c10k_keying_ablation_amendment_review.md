Tool access was blocked for this review. graft was denied in don't-ask mode, and this session has no file-read or shell tool, so I could not open the engine source or any results JSON. Everything below comes from the prereg text alone. Claims that depend on code or artifacts are marked **UNVERIFIABLE (here)**. I also couldn't write the review to `logs/claude_c10k_keying_ablation_amendment_review.md`; it needs to be saved there before the run.

---

## Verdict: **FIX-FIRST** (on the §6 amendment)

**Most important fix:** run K1′ in every case, at the same ridge weight as each valid last-token cell. Right now it runs only if K3″ is valid, and only at weight 50. Without a subject-keyed control at the same weight, a low `para_full` in a valid K3′ or K3″ cell has two equally good explanations. One is the key locus. The other is that a 10–100× smaller ridge reduces paraphrase generalisation for any key. In that case the SUFFICIENT reading says nothing about where the edit is keyed.

## Issues, in priority order

**1. The SUFFICIENT reading is confounded by the ridge weight (real criterion; mechanics ≠ contract).**
- §1 asks about the key locus with the ridge held fixed. The amendment changes the ridge and the locus at the same time.
- Lowering `mom2_update_weight` makes the solve fit the edit keys more exactly and pay less attention to the covariance prior. That plausibly makes the update more specific to those keys, whichever token they come from. (I-INFER; this is the confound, not a claim that it happens.)
- **Fix:** run K1′ at each weight where a K3 or K4 cell is valid. SUFFICIENT should require K1′ `para_full` ≥ 80 at that weight.
- The same control also covers a damage explanation: paraphrases failing because a 100×-smaller ridge broke the model's handling of the paraphrase contexts. If K1′ generalises with similar locality loss, damage does not explain a K3 failure.
- This also removes issue 5.

**2. The "both cells still INVALID" reading isn't supported by the mechanism you cite.**
- The amendment says last-token keys sit 17–180× under the covariance ridge (`results/c10k_route_a/memit_ridge_diag.json`, UNVERIFIABLE here).
- At weight 50 the ridge is only 100× smaller, so keys at the 100–180× end are still suppressed. The ridge account itself therefore predicts canon could stay below 90 at both grid points.
- Reading "both INVALID" as "the ridge is not the (only) limiter" could reject the mechanism on a grid that was never large enough to test it.
- **Cheapest falsifier, at no extra cost:** pre-register a dose-response prediction. Canon should rise monotonically across weight 5000 (29.2 / 25.0 A1, first pass) → 500 → 50.
  - Canon flat or falling: the ridge mechanism is falsified.
  - Canon rising but staying below 90: consistent with the ridge, but the grid is too coarse. That is inconclusive, not "the ridge is not the limiter."
- If you want a decisive cell, the grid needs a point that clears 180× (weight ≤ 25). Otherwise keep {500, 50} and reword this branch.
- The claim that ridge strength scales linearly with `mom2_update_weight` comes from my memory of upstream MEMIT (`solve(w·C + KKᵀ, K)`). It is UNVERIFIABLE here; check `memit_main.py` before relying on "10× / 100× smaller."

**3. K4 was dropped without saying so, and it is the cleaner cell.**
- The heading says "K3′/K4′", but the table contains only K3′, K3″ and K1′.
- In v3, OVERTURNED required K4 ≥ 80 because K4 is the closest analogue to the port. The amendment moves the binding reading to K3, which has templates on, and gives no reason.
- This hides a second possible cause on the solve side. With templates on, the last-token key is an average over prefixed contexts. The prompt-final token's representation likely varies with the prefix much more than the subject's last token does. So the averaged key may not match the key the canonical eval prompt produces.
- K4 (templates off) was also INVALID (25.0 / 8.3), so this can't be the whole story. It is still an alternative explanation for K3, and K4′ would remove it.
- **Fix:** add a K4 cell at weight 50 at least, make it the binding OVERTURNED cell as in v3, and report K3 alongside.

**4. No rule for when the grid cells disagree.**
- Both weights run, but nothing says which cell binds if, say, K3′ is valid with `para_full` 10 and K3″ is valid with 60.
- **Fix:** pre-register which cell binds. I'd suggest the largest valid weight, since it is closest to the operating regime. Any disagreement of 30 pp or more between valid cells should read as MIXED or INTERACTION. Also state that both cells run whatever the first one shows.

**5. The locality guard is one-sided.**
- SUFFICIENT is allowed "regardless of locality". But heavy locality damage is exactly the condition under which paraphrase prompts fail for reasons that have nothing to do with keying.
- The bleed guard covered false positives for OVERTURNED; nothing covers false positives for SUFFICIENT. The matched K1′ from issue 1 closes this; without it, the asymmetry stands.

**6. The amendment doesn't say which arm binds.**
- A2 canon was 4.2 / 8.3 in the first pass, so A1 could become valid while A2 stays invalid.
- **Fix:** state that A1 binds as in §3, that A2 validity is read separately, and that an invalid A2 cell does not block an A1 reading.

**7. Two wording over-claims.**
- "K2 ≥ 80 already holds, so templates are excluded": K2 is subject keying at weight 5000 with templates off. It says nothing about templates for last-token keys at weight 50. The K3 cells have templates on anyway, so drop the sentence.
- "The ridge mechanism … confirmed behaviourally": a valid cell at small weight shows the ridge is *a* limiter. The `para_full` result is a separate claim about generalisation. Keep the two apart.

**8. Scope (drift check).**
- The amendment does advance a live question. It is the only route to moving F3 off I-INFER inside this engine, and it bears on option (ii)'s rationale (`docs/C10K_ROUTEA_RESULT.md` §5, UNVERIFIABLE here).
- But any result at weight 50, with locality expected to degrade, is about mechanism and not about deployment. Say so in the readings.
- One point the decision may not need this run for: K3/K4 couldn't place the write at all at the operating weight. That writability finding (first-pass canon 29/25/4/8) already supports a practical "key at the subject" rule on engineering grounds. The amendment decides whether F3's *generalisation* claim holds, not whether the memory rule is usable.

## Suggested run set (≈ 20 min per cell)
| cell | weight | condition |
|---|---|---|
| K3′ | 500 | always |
| K3″ | 50 | always |
| K4″ | 50 | always (binding for OVERTURNED) |
| K1′ | each weight with a valid K3/K4 cell | always; required for a SUFFICIENT reading |

That's ≈ 1.3–1.7 h. Pre-register the canon dose-response prediction, the rule for choosing the binding cell, and the reworded both-INVALID branch before the first cell starts.
