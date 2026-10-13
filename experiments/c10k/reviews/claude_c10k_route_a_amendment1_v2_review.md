# Adversarial review: Route A Amendment 1 (v2), per-layer threshold D8

**Verdict: FIX-FIRST.** The rule is deterministic and the selection procedure is sound. The gate's statistic, though, cannot tell whether the projector protects anything. The amendment's interpretive claims go further than its numbers. And the "pre-registration" isn't committed yet.

**Reviewer limitation:** the graft tools were denied (don't-ask mode), and this session has no file-read tools. Every line-number citation in §3 and §4 of the amendment is therefore **UNVERIFIABLE by this reviewer**. My numerical points use only the tables in the document. My point about the commit state uses the session-start `git status` snapshot.

## Single most important thing

**Before the chain runs, compute a projected-interference control from the keys already extracted, and pre-register how it will be read.** It needs no edit and runs on the CPU in minutes.

Every gate statistic is a *norm ratio* ‖Pk‖/‖k‖. Taking the per-key ratio on one population against the other gives the selectivity, survival_edit / leakage_wiki:

| layer (chosen) | A1 survival / wiki leakage | ARE-window / wiki leakage |
|---|---|---|
| L4 @0.01 | 0.436 / 0.419 = **1.04** | 0.90 |
| L5 @0.02 | **1.09** | 1.06 |
| L6 @0.02 | **0.83** | 1.01 |
| L7 @0.02 | **0.81** | 1.18 |
| L8 @0.03 | **0.54** | 1.25 |

Selectivity stays nearly constant as the threshold changes:

- **L8:** 0.50, 0.52, 0.54 and 0.54 at 0.02, 0.025, 0.03 and 0.035.
- **L4:** 1.07, 1.04 and 0.98 at 0.005, 0.01 and 0.02.

So the threshold only slides each layer along a fixed line. The window between the 0.2 and 0.5 bounds exists exactly when selectivity is at least 0.4. In effect the gate tests that one condition; it does not test protection. At L6–L8 the projector weakens the edit key *more* than it weakens Wikipedia keys.

This pattern fits two different stories, and the norm ratio cannot separate them:

- **Protective:** P removes the high-variance directions that both key populations share, and what remains of Pk_e is close to orthogonal to Pk.
- **Not protective:** P just attenuates everything by roughly the same amount.

The quantity that actually matters for collateral damage comes from the single-key minimum-norm update. Writing a unit response on k_e gives interference ⟨Pk_e, Pk⟩ / ‖Pk_e‖² on a wiki key k. Compute that, averaged over the Wikipedia keys, at each layer, and divide it by the same quantity with P = I. A ratio well below 1 means the null-space projection buys protection per unit of edit. A ratio of about 1 or more at L8 means the projection protects nothing, and any A2 PASS would have to be explained some other way.

This is the cheapest test that could overturn the premise that D8's thresholds make the protection/efficacy trade-off meaningful. Pre-register its reading thresholds now.

## Issues in priority order

1. **The pre-registration is not committed.** At session start, `docs/C10K_ROUTEA_AMENDMENT_1_PER_LAYER_THRESHOLD.md` and `experiments/track_c/c10k_route_a_launcher.py` were modified, and `results/c10k_route_a/projector_gate_v2.json` was untracked. The launcher change also postdates the chain commit `7e74c60`. Commit the amendment, the gate JSON and the launcher before any edit, or "pre-registered" is not established. Also record the **full** SHA-256 of the `.pt` file in the committed JSON (whether `logs/*.pt` is tracked is UNVERIFIABLE), and confirm the backup covers it.

2. **The SHA check may only be printed, not enforced.** §0 says the run stage "prints" the SHA prefix; §4 says "Mismatch → HALT" without saying what halts. Make the launcher assert that the hash equals `c27203012b6a…` (full hash) and abort before any edit. A printed value that someone has to compare by eye is not a gate.

3. **The gate's keys may not be the keys the solve uses (a LAW#4 risk).** MEMIT-family key computation averages over context-template prefixes. AnyEdit's window keys are also teacher-forced on the target text. Whether `c10k_route_a_gate_v2.py` extracts keys with the ported module's own key function and templates is UNVERIFIABLE here. If it doesn't, all four survival statistics describe a different key distribution from the one the solve uses. Cheap control: on 2–3 A1 and A7 items, take the cosine between the gate keys and the keys from the ported module's own key path. Proceed only if it is about 1.

4. **"The L8 pass is a property of the layer, not of the 24 keys" over-claims.** The held-out subjects presumably share the arm's prompt templates and generator (UNVERIFIABLE). Since v2, held-out survival is also one of the *selection* conditions, so it is no longer a pure holdout. Narrow the claim to: not specific to these 24 subjects, within the same prompt family.

5. **§3 comparability is overstated.** Upstream applies its cutoff to the same normalised statistic (`mom2/count`), but the cutoff is an *absolute* eigenvalue in units of activation variance. Those units are not comparable between a 3B base model and a 7B/8B Instruct model. "0.02 is upstream's value on upstream's scale, not an arbitrary point" therefore does not carry over to this model. To compare operating points, report a scale-free equivalent next to it: the kept-rank fraction (L8: 8368/11008 = 0.76) and the eigen-energy fraction removed. D8 itself is unaffected, because the rule is deterministic. Only the "minimal departure" rationale is ornamental.

6. **The provenance of the L4 statistic switch needs one line.** The v2 per-key A1 survival for L8 at 0.02 (0.177) equals the parent HALT value (0.177, `ec714f1`). That suggests the parent gate already used the per-key mean and only v1's sweep used the aggregate. If so, say "v1 deviated from the parent statistic; v2 restores it." If not, the binding statistic changed between parent and v2, and that needs disclosing. Either way the L4 choice was made with the table visible. It is defensible, because the prereg wording forces it, but it should be stated in those terms.

7. **R1-S has little information value.** Because selectivity barely moves (0.525 vs 0.537), moving L8 from 0.03 to 0.025 shifts it about 12% along the same line. If R1-S is meant to inform anything, swap it for the interference control above, or add an arm that changes something other than the threshold.

8. **The bootstrap CIs are narrower than the real uncertainty.** They resample keys only. Covariance-estimation noise and the choice of the 200 held-out articles aren't captured, so [0.236, 0.248] reflects low between-key spread, not robustness. Label it that way.

9. **The per-layer gate can't see joint behaviour.** The solve spreads the residual across L4–L8, so L8's weakened survival (0.242) will push update mass into the other layers. Add one line to the scope string's caveats: the per-layer gate doesn't predict where the joint solve puts the update.

**Drift check:** if Route A is the operator-chosen successor on the §0.3 C10 falsifier, this is on-path. I couldn't read the runbook, so that is UNVERIFIABLE by me.

---

Separately: the claude.ai Gmail and Google Calendar connectors need authorization in your claude.ai connector settings before they can be used. Nothing in this review needed them.
