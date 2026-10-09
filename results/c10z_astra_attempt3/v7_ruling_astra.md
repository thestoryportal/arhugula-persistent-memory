**FIX-FIRST.** The V7 halt is valid. Permit a separately preregistered diagnostic, with the routing below frozen before launch. Do not change V7 or reinterpret attempt 3.

1. **PROPERTY of the frozen instrument comparison; no demonstrated causal bug.**

   The implementation matches the preregistered statistic:

   - First 1,000 Wikipedia rows, first 100 tokens: `experiments/track_c/c10z_astra_arms.py:1127–1136`, matching `docs/C10Z_ASTRA_PREREG.md:78`.
   - `down_proj` inputs, masked non-padding tokens, CPU float64 squared accumulation, token-count normalization: `c10z_astra_arms.py:519`, `:1137–1156`.
   - The engine also measures masked `down_proj` inputs: `memit_dry_run/memit/rome/layer_stats.py:158–165`. Its cache stores an **unnormalized** second-moment sum, so dividing by `mom2.count` is correct: `memit_dry_run/memit/util/runningstats.py:483–506`.
   - Average-rank Spearman and the all-nine-layer ≥0.80 gate are implemented correctly: `c10z_astra_arms.py:1101–1107`, `:1493–1506`.

   Layers 8 and 12 actually failed, at **0.7718877414** and **0.7669838841**: `architecture_profile/c10z_astra_halt_diagnostic_20261009T022838.229295Z.json:83–92`. That requires HALT under `docs/C10Z_ASTRA_PREREG.md:158`.

   **However, downgrade the diagnosis’s causal certainty.** Its noise simulation *constructs* perturbations until they reproduce the observed correlation; it does not measure the missing `m` errors (`results/c10z_astra_attempt3/v7_cache_profile.py:15–23`). Narrower cache spread supports a rank-sensitivity hypothesis, but does not establish sampling noise or topical bias as the cause. Across-neuron max/median ratios also do not establish heavy tails across observations. High correlations cannot exclude structured numerical or provenance errors.

   Therefore: **faithful gate failure established; population bias, finite-sample variability, and numerical/cache mismatch remain competing explanations.** No line-level bug explaining V7 is established. The separate persistence defect is established in ruling 5.

2. **The diagnostic is admissible, outside ASTRA, subject to a frozen decision tree.**

   It may measure pristine reference statistics without executing the ASTRA solve, write, candidate evaluation, or reader. Use a separate diagnostic namespace and decision ID. Its outputs must never be inserted into attempt 3 or used to resume it. Any subsequent scientific reading requires a complete fresh attempt, consistent with D-C10w-p2rerun (`EXPERIMENT_RUNBOOK.md:381`).

   Freeze these populations now:

   - **F1000:** the original first-1,000-row recipe.
   - **R1000:** first 1,000 indices of the engine’s full-dataset permutation, using `random.Random(1).shuffle`.
   - **R5000:** first 5,000 indices of that same permutation, measured **only if R1000 fails**.

   `random_sample=1` is a deterministic sampler seed, not an instruction to use an arbitrary random sampler: `layer_stats.py:142–150`; `runningstats.py:1543–1556`, `:1595–1600`.

   Keep the ASTRA accumulation, precision, truncation, and 16-row batching identical across populations. Do **not** also adopt the cache’s length-sorted token-budget batching: that would confound population selection with execution shape (`rome/tok_dataset.py:61–79`). Compute R1000 and R5000 separately; blindly reusing prefix accumulations can change the partial-batch shape.

   Define \(P(S)\) as **all nine** layer-4–12 Spearman correlations finite and ≥0.80, using unrounded values. Freeze this ordered mapping:

   | Outcome | Binding disposition |
   |---|---|
   | Integrity/provenance failure, incomplete measurement, or F1000 unexpectedly passes V7 | **Diagnostic inconclusive; STOP.** Attempt 3 remains HALTED-V7. No amendment or attempt-4 admission from this probe. |
   | F1000 fails and \(P(R1000)\) | **A1:** use precisely the pinned R1000 population. |
   | F1000 fails, R1000 fails, and \(P(R5000)\) | **A2:** use precisely the pinned R5000 population, with the required budget amendment. |
   | Both random populations fail | **D:** retain HALTED-V7 as this configuration’s terminal admission outcome. |
   | Any outcome | **C is unavailable.** |

   **No 10,000-row escalation, seed search, layer exclusion, or “closest pass.”** Five thousand is the fixed A2 size for this decision tree.

   Report median absolute **natural-log** ratios per layer,
   \[
   E_l(S)=\operatorname{median}_j|\ln(m_{l,j}(S)/c_{l,j})|,
   \quad c_l=\operatorname{diag}(\texttt{mom2.mom2})/\texttt{mom2.count},
   \]
   but make them **report-only**. They cannot override the table.

   Two qualifications:

   - The driver resolves the dataset revision at runtime and places its identity in `dstats`, which was not saved (`c10z_astra_arms.py:1127–1136`, `:1156`). Recover historical identity where possible; otherwise label F1000 a **new measurement of the frozen recipe**, not recovery of attempt 3’s lost statistic. Pin the probe’s revision, row order, token IDs, and hashes before forwards.
   - The seed-1 samples may overlap the cache’s own sample. Agreement is instrument calibration, not independent validation or proof of late-layer fidelity. The prereg already leaves late-layer fidelity unverified (`:158`).

   The advertised **~10 minutes is UNVERIFIED**. At the existing 300-second-per-1,000-row allowance, F1000 + R1000 is 600 seconds; adding a separately measured R5000 makes 2,100 seconds, before setup and serialization. Record a bounded diagnostic authorization with explicit arithmetic before spending it. The existing allowance appears in the halt diagnostic at `:10–17`.

3. **Option C is not authorized for this recovery.**

   Neither a replacement magnitude statistic nor its acceptance bar has an independently established relationship to adequate ASTRA null-space weighting. Inventing a factor-of-two bound now would still be a post-failure relaxation. Restricting Spearman to favorable layers would directly remove failed checks.

   This matters because `D` enters both the joint system and the weight update (`docs/C10Z_ASTRA_PREREG.md:78–80`); a median discrepancy alone leaves potentially influential tails uncontrolled.

   **Exact ruling: retain all-layer Spearman ≥0.80; no replacement statistic or replacement bar.** Log-ratio measurements are descriptive only. C would require a separate redesign with independent justification, outside this authorization.

4. **The team may authorize benchmark drift rerun #3 under the delegation stated in this request—but only as a named, bounded exception.**

   D-C10r-rulings-14 alone authorizes measurement-driven budget increases; it does **not** independently repeal the driftcap (`EXPERIMENT_RUNBOOK.md:384`). The authority for this exception is the operator’s current **“All questions are to be decided with the team”** delegation, which the drafter must record explicitly.

   Authorize exactly one third drift rerun **only after**:

   - The fixed probe rule selects A1 or A2.
   - The amendment and complete implementation diff are reviewed and frozen.
   - Required checks pass and any budget change has recorded arithmetic.
   - The resulting source change makes the existing benchmark unusable.

   Then run one fresh benchmark, preserve all earlier records and refusal counts, and bind a fresh go record to its actual hashes and ceilings. **No fourth rerun is automatically authorized; STOP/refusal rules remain binding.** Source identity invalidation and rebinding are explicit in `docs/C10Z_ASTRA_PREREG.md:489`, `:499–517`; the previously approved second rerun is recorded at `EXPERIMENT_RUNBOOK.md:388`.

5. **Saving the existing `m` before V7 is a record-only correction, if implemented narrowly.**

   The defect is exact: the gate at `c10z_astra_arms.py:1107` raises before serialization at `:1108–1113`; the diagnostic includes checks but omits `dstats` (`:1693–1695`). This violates the offending-output retention requirement in `CLAUDE.md:37`.

   Persist the already computed CPU `dstats` before its validating gates, using exclusive creation and the existing flush/fsync behavior (`c10z_astra_arms.py:1118–1120`). Preserve exact input bytes in the process-2 copy branch. Do not recompute, recast, normalize, reload into the calculation, or change thresholds.

   **No separate known-ceiling GPU isolation run is required solely for that serialization relocation.** Require a regression test demonstrating that a forced V7 failure leaves a loadable, value-identical statistic and provenance, while gate values and outcomes remain unchanged. A saved statistic is not a completed manifest or permission to resume.

   Source hashing still forces benchmark renewal. Also, **A1/A2 are scientific input changes**, and must not be described as record-only. Attempt 4 must execute its full baseline and LAW gates afresh.

The drafter should append the following skeleton, preserving the existing preregistration. Bracketed fields are provenance or budget fields to complete **before the relevant launch**, not discretionary branches.

```text
Amendment V7-DIAG — [UTC date]
Decision IDs: [diagnostic ID], [conditional drift-3 exception ID]
Status: post-attempt-3, pre-diagnostic-observation.

Authority
The operator delegated: “All questions are to be decided with the team.”
Record the delegation's source and timestamp.
D-C10r-rulings-14 supplies measurement-driven budget authority.
This amendment grants only the bounded actions stated below.

Historical disposition
Attempt 3 remains closed HALTED-V7.
Its artifacts and diagnostic remain unchanged.
No candidate verdict, NULL, method-family conclusion, or F1 closure follows.
The faithful gate failure is established; its physical cause is unresolved.

Diagnostic boundary
Use fresh namespace results/c10z_v7_diagnostic/[UTC]/.
Pristine-model, forward-only reference-statistic measurement.
No ASTRA solve/write, candidate evaluation, reader promotion, or attempt resume.
The diagnostic does not count as an ASTRA attempt.
Never backfill diagnostic outputs into attempt 3.

Pre-forward pins
Record hashes of the probe, original driver, engine, model, tokenizer,
cache files, environment, and this amendment.
Pin dataset revision, length/order, selected row IDs, text hashes and token IDs.
Record whether attempt-3 dataset identity was recovered.
Unrecovered historical identity must remain explicitly UNVERIFIABLE.

Populations and execution
F1000 = first 1,000 rows of the pinned dataset.
R1000 = first 1,000 indices of the full permutation produced by
          random.Random(1).shuffle(list(range(dataset_length))).
R5000 = first 5,000 indices of that identical permutation.
Use the original ASTRA statistic computation, precision, masking,
100-token truncation and 16-row batching for every population.
Measure F1000, then R1000.
Measure R5000 only if F1000 and R1000 fail V7.
Compute each population independently at its prescribed batch shapes.
Save m for all 36 layers, token counts and provenance before scoring.
No seed, population, sample-size or batching search is authorized.

Statistics
c_l = diag(cache["mom2.mom2"]) / cache["mom2.count"].
rho_l(S) = average-tie-rank Spearman(m_l(S), c_l).
P(S) = every rho_l(S), l=4,...,12, is finite and >= 0.80.
Use unrounded values; equality passes.
Report E_l(S) = median_j(abs(ln(m_lj(S)/c_lj))).
Zero ratios have explicitly represented infinite log error.
E is report-only and never changes routing.
Late-layer fidelity remains UNVERIFIED.

Ordered routing
1. Integrity/provenance failure, incomplete measurement, or P(F1000):
   diagnostic INCONCLUSIVE; STOP; no amendment selection or attempt-4 admission.
2. Otherwise, P(R1000): select A1, exactly pinned R1000.
3. Otherwise, P(R5000): select A2, exactly pinned R5000.
4. Otherwise: select D; retain terminal HALTED-V7 for this configuration.
C is prohibited under this amendment.
No 10,000-row extension, alternate seed, layer exclusion or threshold change.

Budget
Before diagnostic dispatch, record [cap], [per-phase arithmetic and sources].
The conditional R5000 branch must already fit that authorization.
Timeout/incompletion follows routing rule 1; no within-run cap increase.
For A2, amend reference-D projections and affected ceiling calculations
and validators consistently before attempt 4. Record measured timing inputs.
Do not merely increase a go-record ceiling.

Persistence correction
Save the existing dstats before validating it; retain exclusive writes,
flush/fsync, process-2 input-byte preservation, and unchanged arithmetic.
Remove the later duplicate save.
Test forced-V7-failure retention and unchanged scientific values/outcomes.
Saved diagnostic artifacts never imply successful admission.

Conditional benchmark and attempt 4
Only A1/A2 permits this continuation.
Freeze and review the amendment, implementation and tests first.
Authorize exactly benchmark drift rerun #3 under the recorded delegation.
Preserve previous benchmark outcomes and cumulative refusal counts.
No automatic fourth rerun; existing STOP/refusal rules remain effective.
On an admissible benchmark, append its hashes/ceilings and create a fresh
go record bound to the final sources, environment and amendment.
Use fresh results/c10z_astra_attempt4/ and fresh logs.
Run the complete required baseline, LAW gates and V7 again.
Do not reuse the diagnostic as attempt-4 gate completion.
A new V7 failure remains HALTED-V7; this amendment grants no further search.
```

No model execution, tests, or edits were performed in this review.

🌱 graft reported ~193,667 tokens saved (~$0.10), 1 successful call.

