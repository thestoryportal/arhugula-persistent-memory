# ASTRA attempt 3 — HALTED-V7 diagnosis (2026-10-08 ~20:45 MDT)

**Verdict: PROPERTY, not a code bug (moderate-high confidence).** The driver computes exactly the statistic the frozen prereg specifies, and that statistic genuinely misses the ≥ 0.80 bound at layers 8 (0.772) and 12 (0.767). The cause is that deep-layer second moments sit in a very narrow range, so a typical per-neuron difference between the 1,000-row reference and the 100,000-row cache reorders them. One secondary defect: the halt does not preserve the statistic it judged (see §4). Diagnosis only: no fix applied, nothing launched.

Halt: `STAGE_0_EXIT=2`, `HALTED-V7: D/cache Spearman <.80`; diagnostic `architecture_profile/c10z_astra_halt_diagnostic_20261009T022838.229295Z.json` (`checks.V7.spearman`); run `results/c10z_astra_attempt3/` (`halt_p1.json`). Driver `experiments/track_c/c10z_astra_arms.py` SHA-256 e3829f41…; the attempt passed recipe A (LAW#3) and V8 (Cholesky ok, cond(G) 1.84e6) before V7.

## 1. What is computed vs what the cache holds (LAW#4 read)
| | D statistic `m^l_j` (driver) | Cache diagonal (V7 reference) |
|---|---|---|
| Tensor | input to `mlp.down_proj`, forward pre-hook (`:519`, `:1143–1147`) | input to `mlp.down_proj`, `Trace(..., retain_input=True)` (`memit_dry_run/memit/rome/layer_stats.py:158–162`) |
| Rows | the **first** 1,000 rows of `wikimedia/wikipedia` 20231101.en, streamed in dump order (`:1129–1131`) — as prereg §2.2 item 5 (`docs/C10Z_ASTRA_PREREG.md:78`) specifies | a **random** sample (`random_sample=1`) of 100,000 rows of the same dump (`layer_stats.py:97–99`, `:142–151`); `mom2.count` = 9,459,215 tokens |
| Truncation | `tok(text)["input_ids"][:100]` (`:1132`) | `tokenizer(text, truncation=True, max_length=100)` (`rome/tok_dataset.py:30`; `t100`); Qwen adds no BOS, so equivalent |
| Statistic | uncentered mean of x² per neuron: Σx²/non-padding tokens (`:1146`, `:1156`) | uncentered second moment; V7 takes `diag(mom2)/count` (`:1104`) |
| Precision | fp16 activation on MPS → `.float()` on MPS → `.cpu()` → `.double()`; squared and summed in float64 on CPU (`:1145–1146`) | float32 features (`layer_stats.py:164`) |
| Comparison | `spearman()` with average ranks for ties (`:1493–1506`) | — |

Padding is right-side and masked (`:1140`, `:1145`). The boolean-mask index yields a fresh contiguous tensor, and the conversion is the safe `.to(X).cpu()` pattern, not the faulty combined device+dtype conversion on an offset view. Squaring happens in float64, so fp16 overflow cannot occur. Normalization is a per-layer scalar, so it cannot change ranks. Every element matches the prereg; the one designed difference is first-1,000 rows vs a random 100,000.

## 2. Evidence (`v7_cache_profile.py` → `v7_cache_profile.json`, CPU, numpy, peak RSS 0.58 GB)
`m` itself cannot be recomputed without the model: it was never saved (§4). The cache side was profiled per layer instead. "Noise for observed" is the spread of per-neuron multiplicative noise, applied to the cache, that reproduces the observed Spearman.

| Layer | Observed Spearman | Spread of cache diagonal (IQR, log10) | Noise for observed (log-σ) |
|---|---|---|---|
| 4 | .986 | 3.84 | 0.20 |
| 5 | .980 | 3.11 | 0.50 |
| 6 | .953 | 1.04 | 0.50 |
| 7 | .873 | 0.72 | 0.64 |
| 8 | **.772** | **0.36** | 0.58 |
| 9 | .814 | 0.42 | 0.54 |
| 10 | .801 | 0.42 | 0.56 |
| 11 | .808 | 0.33 | 0.40 |
| 12 | **.767** | **0.35** | 0.50 |

- **No bug signature.** The cache has no non-finite values and no zeros. The correlations are high and fall smoothly with depth. A neuron misalignment, wrong tensor or conversion corruption would give near-zero or erratic correlations, not 0.77–0.99.
- **The drop tracks spread, not error size.** From layer 5 to 12 the implied per-neuron discrepancy is roughly constant, about 1.5–1.9×. The cache diagonal's spread collapses from 3.1 decades to 0.35, so the same relative discrepancy that barely moves ranks at layers 4–6 reorders them at 8–12.
- **The discrepancy itself is plausible as a sampling and population effect.** Deep-layer activations are heavy-tailed (max/median 120–420), and the first 1,000 dump rows are a fixed early-article slice, not a random sample. Without `m`, the cause cannot be split between sample size and topical bias.

## 3. Conclusion
PROPERTY. The frozen D recipe (first 1,000 rows × 100 tokens) does not track the 100,000-row cache to Spearman ≥ 0.80 at deep cached layers. Under the prereg (`:158`) this is a correct HALT of the instrument. It is not a harness or driver defect, and not a science-path result. No ASTRA verdict exists.

## 4. Secondary defect (diagnostic completeness)
`prepare_instruments` halts at `:1107`, before `dstats.pt` is saved at `:1113`, and the halt record does not carry `m`. The statistic that failed is therefore lost (36 × 11,008 float32 ≈ 1.6 MB). CLAUDE.md halt discipline asks for the offending output to be kept for later comparison. Any attempt 4 should save `dstats.pt` (or `m` in the halt JSON) before the V7 require. This is an artifact-ordering change, not a science-path change.

## 5. Options for the team (none applied; each needs a dated prereg amendment and GPT-6-Astra review; attempt 3 is closed as HALTED-V7 and is not read around (D-C10w-p2rerun); any re-run is attempt 4 in a fresh namespace)
0. **Recommended first: a diagnostic probe, outside the run, forward passes only, about 10 GPU-min.** Compute and SAVE `m` for (a) the frozen first-1,000 rows and (b) 1,000 rows drawn with the cache's own sampler (`random_sample=1`), and optionally (c) 5,000 random rows. For each, report Spearman and the median |log(m/cache)| per layer against the cache. This separates population bias (b fixes it) from sample size (only c fixes it), and its results decide among A1, A2 and C. It does not touch the engine or harness; this is the precedent of the z0 probe.
- **A1 — representative reference, same size.** Draw the 1,000 rows with the cache's sampler instead of the first rows. Same cost (300 s allowance). It changes D's population, so `H_in` and the D pins change. Justified only if probe (b) passes V7.
- **A2 — larger reference.** For example 5,000–10,000 random rows. The D cost scales to about 1,500–3,000 s against the 300 s `reference_D` allowance, which needs a budget amendment (D-C10z-budget). Justified if only probe (c) passes.
- **B — use the cache diagonal for the cached layers 4–12.** This mixes instruments: late layers, which ASTRA selects (§2.1), would still use D, and V7 would no longer validate the method that produces their weights. Not recommended.
- **C — re-scope V7's statistic** to D's use, for example a bound on median |log(m/cache)|, or Spearman restricted to the cached layers where spread allows. Risk: a threshold chosen after seeing a failure. It must be justified independently of the observed values, so Astra should rule on it before any data from option 0 is seen.
- **D — accept the HALT** as the ASTRA outcome: the frozen instrument fails its own sanity check. Record HALTED-V7 and close or redesign.

**Rerun and budget rules to check before attempt 4.** Under D-C10z-driftcap (runbook §5, row "ASTRA amendment fold rulings"), at most one drift re-run of the benchmark is on the program's own call, and a second returns to the operator. Benchmark re-run #2 (20261009T012936Z) was already the operator-approved second. If attempt 4 needs another benchmark re-run (any hashed source change, such as a D-recipe amendment or a driver edit), that is a third and returns to the operator's authority. Overnight the operator has delegated decisions to the team: record it as a team ruling with Astra, citing that delegation.

## Reviewer qualification (appended 2026-10-09; GPT-6-Astra high, results/c10z_astra_attempt3/v7_ruling_astra.md ruling 1)

The verdict above overstates causal certainty. What is established: the driver computes the pre-registered statistic faithfully (c10z_astra_arms.py:519, :1127–1156; layer_stats.py:158–165; runningstats.py:483–506) and the V7 gate failed faithfully (layers 8 and 12 at 0.7718877414 and 0.7669838841). What is NOT established: the cause. The noise simulation in v7_cache_profile.py (:15–23) constructs perturbations until they reproduce the observed correlation; it does not measure the missing m errors. Narrower cache spread supports a rank-sensitivity hypothesis but does not establish sampling noise or topical bias, and high correlations cannot exclude structured numerical or provenance errors. Population bias, finite-sample variability and numerical/cache mismatch remain competing explanations. Read "PROPERTY" as "faithful gate failure, no line-level bug found", not as an identified mechanism. The diagnostic of Amendment V7-DIAG (docs/C10Z_ASTRA_PREREG.md §11) is the pre-registered way to discriminate.
