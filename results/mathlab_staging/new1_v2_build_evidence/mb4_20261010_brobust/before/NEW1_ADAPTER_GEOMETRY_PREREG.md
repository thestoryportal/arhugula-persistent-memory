# NEW-1 — Adapter versus closed-form update geometry

**FROZEN v2 · 2026-10-09 (D-NEW1-1; GPT-6-Astra r1 FIX-FIRST → r2 FREEZE, `results/mathlab_staging/new1_prereg_astra_r2.md`) · computation NOT RUN — execution gated on a reviewed build with verified supervisor enforcement.** Tier: **MATH-PROXY — math estimate, not evidence**. This pre-registration may only reorder or prune the GPU queue; it never promotes a scientific claim, a write route, a C10 label, or F1 readiness. This revision authorizes the CPU build and small synthetic fixture arithmetic, never pinned-input geometry, model/tokenizer import, GPU execution or commits.

## 1. Question and map cell

NEW-1 comes from `results/mathlab_staging/infranodus_trial/SUMMARY.md:13–16`, a sharpened ideation lead, not evidence. Where does the ceiling oracle's trained rank-16 adapter put its per-layer weight-update energy in the covariance input basis, how many singular directions carry that energy, and how much do its input/output subspaces overlap the closed-form update? The registered comparison is the five **down_proj matrices at layers 4, 5, 6, 7, 8**, one historical P1 seed (s0), no pooling with P2 or a retrain.

The relevant layer is **Write Engine (§8)** (`docs/SPEC_E2E_GROUND_TRUTH.md:14`) and the cell is **§8.9 L2 post-write firing of multi-token CORE values / C10** (`docs/SPEC_EXPERIMENT_OVERLAY.md:22`). The framework prescribes behavioral verification, including generation/assertion/constraint probes; storage success with behavioral failure remains a named failure (`docs/SPEC_E2E_GROUND_TRUTH.md:64–66`). This offline geometry touches the write mechanism and may order its tests. It supplies none of those behavioral probes or a storage/CPU-deployment gate.

Known observations, not predictions of this draft: the replicated rank-16 oracle recalled min(70,71)=70/72 versus same-process closed-form A7 9–16/72, but is **PARTIAL-CEILING-LOCALITY-COST(G4,G6), BIGRAM**, with no gate-clean reference and independent-prereg-only routing (`CORPUS/57_C10W_ORACLE_FINAL.md:9–16`, `:25–30`, `:48–56`). A1/A2 oracle P1 are behavioral positives at 72/72 (`CORPUS/57_C10W_ORACLE_FINAL.md:34`). Last-token keys, ridge/collinearity, and restored write magnitude do not establish paraphrase transfer or clean locality (`CORPUS/43_C10K_KEYING_ABLATION.md:19–21`, `:41–50`; `CORPUS/42_C10K_ROUTEA_CONTROLS_NOT_RECOVERED.md:13–19`, `:25–35`). Those narrower mechanism findings are motivation, not an attribution of the oracle's gain.

## 2. Pinned inputs (SHA-256, full file bytes)

All listed hashes were checked with stdlib streaming SHA-256 during drafting. Adapter values and covariance/update arrays were not loaded or analysed. Adapter JSON headers and scalar scale/layer fields were read as metadata; harvest tensor shapes come from the hash-pinned manifest. Paths are rooted at this worktree unless an absolute cache path is specified.

Let `P = results/c10w_oracle/p1_20261007T223707_598959Z` and `H = results/mathlab/harvest_20261009T184950.056951Z`. Adapter paths are exactly `P/adapters/<arm>_s0_r16.safetensors`; paired provenance records are exactly `P/train/<arm>_s0_r16.json`. Each adapter is 4,179,028 bytes; headers pin `A_l: F32[16,11008]`, `B_l: F32[2048,16]`, `scale=1.0`, and layers `[4,5,6,7,8]`.

| Arm | Adapter SHA-256 | Paired training-record SHA-256 |
|---|---|---|
| `A7_coined_coined` | `4e2ae47a450f7014b4d3b003c125796beeb9b37ac94a32f937a65f6187cd124f` | `a4c4757f6251f8600c47689738b0ba0525827018126f543d376fe49794939977` |
| `A1_single` | `23c199f91412da368d5e2c9204cbac06f2153dd8958da572d69c1ba7785cefe1` | `11d1dbef51b0babfd8ceb1cb794ff6a84080b0b08da82c84250d7449dbfe99dc` |
| `A2_coherent2` | `d5d9832620fb2db0c6f1ed984ef5e79b34361f61efb253ccc873c07885b35e90` | `37c32338c1420a2f385e5d8281c97c30fd9b2b6ab5b83ae0a990753b26220e0e` |
| `A7_canon` | `869905010f81fd3c6e006b3a5cf0a809221ac7b5b315f7a3665ee2f58874cd53` | `dd35028e619ed762a6ed430de056f6eb6b3c71153b425eba711b1847dd84e3c4` |
| `A7_shuf` | `9ce29297d07622e47d5354bd769b26cc0ce89d07128769cfeea39e84a5df094b` | `3938136ee161d8afdc55b47798854c8ea92e53badffd23ba5463c3f83194d6a0` |

Model: **Qwen/Qwen2.5-3B @ 3aab1f1954e9cc14eb9509a215f9e5ca08227a9b**, as recorded by every adapter's training record. Shared training inputs: `results/c10w_oracle/step0_20261007T223638_531381Z/train_inputs.json`, SHA `d0fa96af0de8d98c5b0fbd90609cd2f2fa1d27a03013c1db9c530e3ec804c050`. Step-0 record: same directory `step0.json`, SHA `82ef86437b5ba00fa78a1b55cfe64e4d85baaceb37aa0726f3015c2b2f7d673e`. Recorded trainer source `experiments/track_c/c10w_oracle_train.py`, SHA `64a01fbcbbd8e836f67e623bc50f66ecff8dd59a29d7c82db3bba287d76ea463`. Its `:71–98` fixes the product orientation and saved scale; no PEFT alpha/r rescaling is implied.

Closed-form operand: `H/inloop_A7_coined_coined.pt`, SHA **`abb882982f406ddd5d6536529ce49dee8f31ad3b3243495e93687266e7c6582f`**, 463,160,213 bytes. Select **only `l4.upd_precast` through `l8.upd_precast`**, each `[2048,11008]` fp32, captured before fp16 casting/application. Do not substitute `weights_A7.pt` subtraction, a fresh solve, or the historical scalar norm. Manifest: `H/manifest.json`, SHA **`bb9a6f9ad76678ae2289151c9fa64fb0033a6b8b2d7aff0b9a03150180f1ba7e`**. Its recorded source-start/source-end maps agree; its 24 canonical subjects match the adapter training-input order. This is a later harvest, not the exact same-process P1 closed-form tensor behind its 9/72 score. **Retain harvest 1 throughout: never combine harvest identities, admissions, tensors or source maps; harvest 2 is not an operand of NEW1.**

Covariance cache directory is exactly `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/`. Each listed NPZ is 484,705,442 bytes and has `mom2.mom2: F32[11008,11008]` and scalar int64 `mom2.count`.

| Layer | Cache filename under that directory | SHA-256 |
|---|---|---|
| 4 | `model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz` | `f6ae787454e5bae9eff52155ac699386351246b03e60ab68d728335b0c9a5b58` |
| 5 | `model.layers.5.mlp.down_proj_float32_mom2_t100_100000.npz` | `26773779c5f95647c844fb42c553221aa81e48206cb3e61602237b3da4e53b3d` |
| 6 | `model.layers.6.mlp.down_proj_float32_mom2_t100_100000.npz` | `72a4a42bf7586f1b7de5bfce365263d2a84b66f6ffc4ce20f9fa113d115887fd` |
| 7 | `model.layers.7.mlp.down_proj_float32_mom2_t100_100000.npz` | `ed2f4c64356fc6388ae4623ccc2bfc9101660fe92a787c193d593a24992aaba5` |
| 8 | `model.layers.8.mlp.down_proj_float32_mom2_t100_100000.npz` | `430c1aa56a7cde6626ff02e241b45fd706d02d81d97931536fbed38d8974dd2a` |

`C_l = mom2.mom2 / mom2.count`, division in the stored dtype before conversion to CPU fp32, matching `mathlab/core.py:215–221`. This is the **uncentered input second moment** the program calls covariance; do not recenter or trace-normalize it. The first harvest records MathLab prereg SHA `4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507`; preserve that historical binding despite later amendments. Its rejected mint-arm admissions are unaffected; this task consumes only fresh A7 updates, not mint replay.

Before an eventual run, require all hashes, shapes, layer order, model revision, 24-subject order and A7 value-map identity to match these recorded sources. Verify the captured projector count/hash or the four registered projection probes under the existing math-lab 1e-6 relative-error rule (`mathlab/core.py:51–66`). A missing identity, nonfinite/zero update, cache mismatch or projector mismatch is **INVALID-SOURCE/ARITHMETIC**, not a failed prediction; no replacement inputs or dropped layers.

## 3. Objects, statistics and numerical validity (fixed before analysis)

For layer \(l\), adapter \(D_l=sB_lA_l\) is a **2048×11008 output-by-input** update, using the saved scalar \(s=1\). Promote the saved fp32 factors to CPU float64 **before** multiplying. Closed form \(M_l\) is the saved fp32 `l{l}.upd_precast`, promoted unchanged to float64. This compares pre-cast update geometry, not the fp16 merged/applied intervention.

The observed harness path is AlphaEdit-style: \(A=P(KK^T+ca)+I\), \(B=PKR^T\), \(M=\operatorname{solve}(A,B)^T\), with \(P=Q_{\sigma<0.005}Q_{\sigma<0.005}^T\) (`experiments/track_c/c10e_bandknob.py:166–178`, `:205–217`). Its captured cache is expected to be zero and must be validated. **Do not describe this as a \(5000C\) ridge solve.** C suppresses directions through the projector here. For an ideal P, left-multiplying the solve by \(I-P\) gives \((I-P)M^T=0\); near-zero excluded energy is therefore a structural expectation, not a new explanation of the performance gap. Historical null-space share 1.000 is already reported in `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:25`; removing P was not a sufficient fix (`:29`, `:37`).

Compute exactly **one full 11008² native-fp32 covariance SVD per layer**, as in `mathlab/core.py:44–48`: \(C=U\Sigma V^T\), decreasing singular values, \(Q=U\). Reuse that decomposition for every arm/control. Before calling Q a covariance eigenbasis, require: positive moment count and finite C; symmetry \(\|C-C^T\|_F/\|C\|_F\le10^{-6}\); SVD reconstruction \(\|C-U\Sigma V^T\|_F/\|C\|_F\le10^{-5}\); **PSD reconstruction** \(\|C-Q\Sigma Q^T\|_F/\|C\|_F\le10^{-5}\); and orthogonality \(\|Q^TQ-I\|_F/\sqrt{11008}\le10^{-5}\). Nonnegative singular values alone do not prove PSD. Use blocked products/float64 reductions for these checks, no full float64 covariance decomposition, silent symmetrization, clipping, or cutoff change. Require the recomputed native-fp32 P to match the captured projector count/hash or all four frozen probes (relative error ≤1e-6), and validate `ca_zero`, `ca_norm`, `ca_sha256`, and `upd_sha256` against tensor bytes. Then require \(E_{\rm excluded}(M_l)\le10^{-4}\) at every layer as a parity/instrument control, not a scientific prediction.

**Fixed bins:** \(d=11008\), **k=1024**, top T = modes 1…1024; bottom B = modes 9985…11008; excluded X = all modes with \(\sigma_i\ge0.005\); allowed N = modes with \(\sigma_i<0.005\). Record all subset dimensions. For each update \(Z\in\{D,M,\text{four adapter controls},\text{random controls}\}\):

\[
 E_S(Z)=\frac{\|ZQ_S\|_F^2}{\|Z\|_F^2},\quad S\in\{T,B,X,N\}.
\]

C acts on the **input** side (right multiplication); no output-side covariance projection. Report top/bottom/allowed/excluded fractions and top/bottom differences between D and M separately for each of the five layers, with all arm/control rows. The complement identities must hold within 1e-5. Compute in blocks of at most 256 covariance columns, float64 accumulation; use factored products for adapters/random controls, the actual saved dense M for its energies.

For singular values \(s_i(Z)\), use the **singular-energy participation ratio**, not an unstated entropy definition:

\[
 r_{\rm eff}(Z)=\frac{(\sum_i s_i^2)^2}{\sum_i s_i^4},\qquad
 r_{95}(Z)=\min\{r:\sum_{i=1}^r s_i^2\ge0.95\sum_i s_i^2\}.
\]

Use every singular value of the saved matrix for these two statistics. Adapter singular values come exactly from the small QR core: \(B=Q_BR_B\), \(A^T=Q_AR_A\), SVD of \(sR_BR_A^T\). M uses an economy SVD of the **2048×11008** float64 operand (not another 11008² SVD). Record norms and numerical rank \(r_\tau=\#\{s_i>10^{-6}s_1\}\); numerical rank does not replace effective rank.

For each pair (D,M), (A1,M), (A2,M), (canon,M), (shuf,M), and (random,M), take leading input and output singular subspaces, retaining at most **16** directions above \(10^{-6}s_1\). For either coordinate side a,b:

\[
 c_j=s_j(Q_a^TQ_b),\quad \theta_j=\arccos(c_j),\qquad
 O_{16}(a,b)=\frac1{16}\|Q_a^TQ_b\|_F^2=\frac1{16}\sum_j c_j^2.
\]

Report every actual principal angle in degrees, the two retained ranks, and input/output \(O_{16}\). Missing dimensions contribute zero to the fixed denominator; self-overlap is r/16, not necessarily 1. Roundoff outside [0,1] by at most 1e-8 may be clamped for `acos`; larger excursions are INVALID-ARITHMETIC. Also report **flattened signed matrix cosine** \(\langle D,M\rangle_F/(\|D\|_F\|M\|_F)\) and norm ratio \(\|D\|_F/\|M\|_F\), not signed entries between arbitrary SVD bases.

**Tie rule:** covariance boundaries are **j=1024 for top-k** and **j=9984 for bottom-k**; the update boundary is **j=16** when more than 16 numerical directions survive. At each applicable boundary require \((s_j-s_{j+1})/\max(s_j,s_{j+1},10^{-12}s_1)>10^{-4}\); equality/failure makes that bin or overlap INVALID-SUBSPACE. For update overlap only, no leading-16 boundary test is needed if all retained numerical directions fit within 16. A covariance-bin tie does not invalidate the complete allowed/excluded partition, and a singular-vector tie does not invalidate participation ratio. Zero/nonfinite normalization, failed source checks or numerical gates are INVALID, never prediction FAIL. Each prediction needs its statistic valid on **all five fixed layers**; otherwise it is INVALID, not recomputed on a favorable subset. No adaptive k, rank, epsilon, layer, seed or input substitution.

## 4. Predictions and falsifiers

These are **method-conditioned geometry predictions**, fixed without inspecting adapter spectra, projections or angles. Numeric margins are operational choices, not calibrated behavioral thresholds. `PASS` below means only `MATH-PROXY / <prediction> PASS`; there is no combined scientific PASS, p-value, population inference or independence claim for five layers.

For 20 random controls, let q95 be the **19th sorted value** (nearest rank, ceil(.95×20)), never interpolated. For each prediction, all conditions must hold in the **same at least 3 of 5 layers**. A valid result below the margin is FAIL; an impossible margin above 1 stays FAIL rather than being relaxed.

| Prediction | Numeric PASS rule | What valid FAIL means |
|---|---|---|
| **H-COV — excess energy in directions this solve excludes** | \(E_X(D)\ge0.25\), \(E_X(D)-E_X(M)\ge0.15\), **and** \(E_X(D)\ge q95(E_X(R))+0.10\) | No registered excess beyond this projector-imposed contrast and the orientation control. It does not rule out every covariance mechanism. |
| **H-TOP — large-variance concentration** (secondary) | \(E_T(D)-E_T(M)\ge0.10\) **and** \(E_T(D)\ge q95(E_T(R))+0.05\) | Registered top-k concentration absent. Bottom-k fractions remain a predeclared descriptive readout, not a replacement hypothesis. |
| **H-RANK — distributed adapter energy** | \(r_{\rm eff}(D)\ge8\) **and** \(r_{\rm eff}(D)/r_{\rm eff}(M)\ge1.25\) | The specified rank distribution contrast is absent; neither a model-capacity bound nor permission to escalate to rank 64. |
| **H-OVERLAP — distinct but non-random input orientation** | input \(O_{16}(D,M)\le0.25\) **and** \(O_{16}(D,M)\ge q95(O_{16}(R,M))+0.05\) | No registered structured low-overlap contrast. Low overlap alone is ordinary in high dimension and cannot select a mechanism. |

Input overlap is the predictive endpoint; output overlap/angles, matrix cosine, norm ratios and r95 are descriptive. **Secondary M16 diagnostic:** from the already-computed economy SVD of M, define \(M_{16}=U_{:16}\Sigma_{:16}V_{:16}^{T}\), retaining up to 16 directions with \(s_i>10^{-6}s_1\). Report retained energy \(\sum_{i=1}^{r}s_i^2/\sum_i s_i^2\), participation-ratio effective rank and all four covariance fractions of M16. The existing j=16 boundary-validity rule applies when more than 16 numerical directions survive; a tied cutoff makes M16 geometry INVALID-SUBSPACE while full-M effective rank and complete allowed/excluded energy remain valid. This is descriptive only, never a substitute for full M in a primary endpoint. Report all outcomes, no selection of the winning statistic. The shuffle comparison is not an automatic invalidation: if \(|E_X(D)-E_X(\text{shuf})|\le0.05\) in ≥3/5 layers, label the excluded-energy contrast **NON-SPECIFIC**. A shuffled difference in this one statistic never establishes specificity for top/bottom energy, rank, overlap, or behavior.

## 5. Controls and S-3 boundaries

- **A1 and A2:** behavioral positive controls of the source oracle (P1 72/72 each), same rank/seed/band/trainer. Compute the same geometry. Their spectra are not assumed known and failure to mimic A7 is not an instrument failure.
- **A7_canon:** reduced training-frame coverage contrast, 24/24 training fit versus 480/480 for the multi-frame adapters; not a clean behavioral negative/reference. The canonical split is NOT-READ because its locality gates fail (`CORPUS/57_C10W_ORACLE_FINAL.md:12–14`, `:34`). No attribution of frame diversity from this contrast.
- **A7_shuf:** specificity negative for the intended mapping (matched cross-scores 0/72), positive for fitting a permuted mapping (`CORPUS/57_C10W_ORACLE_FINAL.md:30`, `:34`). Random-like or shuffle-like geometry blocks a semantic-specific/causal reading; no label laundering from its training fit.
- **Random rank-16, matched Frobenius norm:** **20 draws per layer**, NumPy 2.4.6 `Generator(PCG64(20261009+100*l+j))`, j=0…19. Generate output 2048×16 and then input 11008×16 independent standard-normal arrays, reduced float64 QR, fix each QR diagonal sign positive. Set \(R_j=(\|D_l\|_F/4)U_jV_j^T\), equal singular energies, rank 16. Serialize/hash the factors and scale before deriving their statistics; these generated-control SHAs are **NOT GENERATED / NOT RUN**, not invented current input pins. Their effective rank is 16 by construction, an instrument control. Expected energy is dim(S)/11008; expected fixed-16 input overlap with M is r/11008 for the **retained comparison rank \(r=\min(16,r_\tau(M))\)** (16/11008 when all 16 survive). Report every draw, mean, q95 and dimensions; no best-draw selection or statistical significance claim. The null has a flat spectrum and does not control the trained spectrum or prove semantic specificity.
- **Secondary spectrum-matched orientation null:** reuse exactly the same 20 seeded U/V QR directions as each flat-spectrum random control and define \(R^{\rm spectrum}_j=U_j\operatorname{diag}(s(D))V_j^T\), using all 16 adapter singular values (including any numerical zeros), with no additional rescaling. Report its norm, effective rank, covariance fractions and input/output overlap distributions. Its norm and effective rank must agree with D within 1e-10 relative norm / 1e-8 effective-rank error. This controls spectral concentration descriptively; **it never replaces the flat-spectrum q95 baseline, any primary endpoint or any primary PASS/FAIL rule**. Save/hash both secondary control factors and spectrum before statistics.
- **Future instrument tests, before real arithmetic:** known small diagonal/indefinite covariance; rank-1/rank-16 equal-spectrum matrices; self-overlap r/16; scaling/sign and whole-eigenspace basis-rotation invariance; transposed-axis rejection; zero/nonfinite input rejection; cutoff ties; projector parity. On random controls require relative matched-norm error ≤1e-10, effective-rank error ≤1e-8, and mean energy within 0.01 of dim(S)/11008. Numerical/instrument failure produces INVALID with diagnostics. No controls were computed during drafting.

**S-3 applies literally** (`docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:93`): locality and held-out generalization are separate axes, with separate numeric behavioral criteria. This study bears on **candidate update geometry relevant to the under-generalization axis**, with a possible preservation tradeoff. It measures **neither** held-out recall nor locality/forgetting. Energy in a protected direction is not evidence of harm, and energy retained in null(C) is not evidence of transfer or clean locality. The future write must independently meet its frozen held-out full-sequence and all locality criteria; the oracle's ≥61/72 target and G4/G6 misses remain their original reading. No response at subject-last versus frame/value positions, paraphrase-key firing or decoded generation is measured here: those need separately preregistered key-response/position interventions. Optimizer, frame coverage, unconstrained write size, covariance protection, precision and cross-process context differences remain confounded.

## 6. CPU spending and memory

**Future run only, after review/freeze and separate execution authorization.** Existing deps, CPU only, no model/tokenizer/engine runtime import, MPS/CUDA, inference, training or harvesting. Pin Python 3.11.16, torch 2.8.0, NumPy 2.4.6, safetensors 0.8.0 (package metadata inspected with stdlib, not imported during drafting); eight CPU threads, one worker at `nice -n 10`, one layer at a time. Read the saved update bundle CPU-only with `weights_only=True, mmap=True`; no silent eager-load fallback.

The existing **full-shape synthetic** 11008² fp32 SVD measurement is 78.9521 s and sampled peak RSS **4.60876 GiB** (`results/mathlab_staging/peak_svd_full.json`, SHA `7ecf3e185cb041ac7eb6393ce57da8a58d9af44448df6d71650b743f9e3784b6`; source caveats `docs/MATHLAB_PREREG.md:367–380`). Five covariance SVDs estimate **≈395 s / 6.6 min**, not five simultaneous 4.6-GiB allocations. Reuse each basis for all controls. Reuse the full-shape estimate only for the covariance decomposition; complete-workload feasibility remains unverified.

> “Before numerical imports, require the fail-closed CPU admission contract of MATHLAB_PREREG §6. Before each heavy cell require available memory ≥8 GiB plus its declared reserve; the covariance-SVD reserve is 5 GiB, hence admission requires ≥13 GiB. Wait at most 300 s within the unchanged 1,800-s deadline. A NEW1-specific supervisor must enforce the deadline, terminate on observed worker RSS exceeding 6 GiB or available memory below 6 GiB, and refuse on monitoring failure. The existing MathLab runner does not establish these NEW1 protections. Execution remains gated on verified enforcement and declared reserves for every heavy cell.”

The NEW1 spending caps remain **1,800 s total monotonic wall time** from before admission, hashing or imports, and **6 GiB observed worker-process-family RSS**. Monitoring continues during admission and cell waits. The observed-limit sampling cadence is at most one second plus bounded probe latency; it cannot certify that no transient peak occurred between observations. The supervisor alone acknowledges heavy cells; reserve declarations are fixed below, and no lower-reserve or direct-worker bypass is allowed.

| Heavy cell | Declared reserve above the 8 GiB floor | Required available memory |
|---|---|---|
| Numerical imports | 1 GiB | 9 GiB |
| Harvest/adapter/covariance load | 2 GiB | 10 GiB |
| Native-fp32 covariance SVD | 5 GiB | **13 GiB** |
| Covariance validity / projector checks | 2 GiB | 10 GiB |
| Float64 economy update SVD / adapter QR | 2 GiB | 10 GiB |
| Blocked energy / subspace projections | 2 GiB | 10 GiB |
| Random controls | 1 GiB | 9 GiB |
| Output serialization | 1 GiB | 9 GiB |

Release covariance SVD workspace before update SVDs, use 256-column blocks and stream layers; no full float64 C or materialized random dense updates. Every diagnostic, resource receipt, control artifact and numerical result is flushed/fsynced before its corresponding gate event. Run state is only `events.jsonl`, emitted through `tools/mathlab_events.py`; output JSONs carry operands/statistics/diagnostics, never a second status authority. A STOPPED or monitoring refusal has no prediction verdict.


Loading/hashing, PSD/parity validation, dense 2048×11008 update SVDs, control products and output are **untimed**. The reference spectra are synthetic, measurements are one sample on a shared machine, and reserve/RSS coverage of this complete workload is **UNVERIFIED**. 1,800 s / 6 GiB are spending caps, not demonstrated feasibility. Deadline/memory/I/O failure yields **STOPPED / no prediction verdict**; preserve partial diagnostics, never read a missing layer as FAIL or silently raise the cap. This draft spends no such budget and does not start or interrupt step 2.

## 7. What could change the queue

No queue changes occur on draft completion. NEW-1 predictions are uncalibrated. Under `docs/MATHLAB_PREREG.md:17–21`, `:263`, actual proxy-driven reorder/prune needs calibration **and demonstrated prospective utility**; an existing residual-proxy pass is not calibration of these new geometry statistics. Until that is separately preregistered and satisfied, the table is a conditional recommendation for review only. Never close a route or restart a completed/live run. “Prune” means deprioritize unspent optional work, not mark a method falsified.

| Future eligible pattern (all relevant endpoints valid) | Exact candidate queue consequence, conditional on that utility gate |
|---|---|
| H-COV PASS; H-TOP PASS supports the large-variance version | Move **Step 8 / H-4 Moir covariance-from-own-text** ahead of another optional norm/ridge-only repeat; consider the **deferred engine-path trace-matched covariance diagnostic** first. This motivates a covariance/input-geometry comparison, not a promised recall gain. Moir source: `docs/INTEGRATED_QUEUE_2026-10-07.md:24`; deferred variant: `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:37`. |
| H-COV FAIL | Lower the priority of an **additional covariance-only exploratory run** relative to position/objective tests; do not cancel Moir's independent rationale or revive/erase the already NULL P:=I result. |
| H-OVERLAP PASS, particularly with H-RANK PASS | Move the unrun **H-30 position-graft diagnostic** / later **H-6 position-separated gated write** ahead of another magnitude-only repeat, under an independent prereg that controls norm and training frames. Their status/rationale sources are `CORPUS/57_C10W_ORACLE_FINAL.md:14`, `:54` and `docs/INTEGRATED_QUEUE_2026-10-07.md:27`. Geometry cannot choose subject/frame/value positions; that intervention must discriminate them. |
| H-OVERLAP FAIL or rank contrast absent | Do not promote H-30/H-6 on a geometry-specific argument. Preserve their independent collateral/position rationale and existing order. Rank 64, a new model, or a completed C10X/C10Y/ASTRA rerun is not authorized. |
| NON-SPECIFIC shuffle result, INVALID or STOPPED | No semantic-specific queue recommendation; INVALID/STOPPED means **no change**. Keep the S-3 locality controls ahead of any interpretation of a successful fit. |

Existing I-8 P:=I and sparse-band tests already ran; C10X/C10Y/ASTRA have their own current prerequisites. This document supplies no automatic rerun, no clean-ceiling reference and no mechanism attribution (`CORPUS/57_C10W_ORACLE_FINAL.md:14`, `:48–56`). No source record, label, frozen preregistration, producer, shared contract, dashboard, ledger or canonical tracker is edited.

## 8. Draft record and execution boundary

**No real geometry computed:** no pinned matrix/factor/covariance/update payload decoding, SVD, rank, energy, angle, inference or training. Build tests use small synthetic matrices only. Only the saved scalar scale and five layer IDs were decoded as metadata. Only stdlib file hashes, JSON/safetensors/NPY headers, saved scale/layer metadata, subject-order and recorded-source checks were performed. All geometric predictions remain **NOT RUN / UNVERIFIED**. Any later output must carry MATH-PROXY, the exact input hashes, all five layers/controls, validity decisions and individual prediction outcomes; stage it for review, never promote a claim or relabel prior evidence.

Advisor-review was applied before final criteria were authored. Claude auth was probed (`loggedIn=false`); independent same-family fallback is **weaker independence**. The initial FIX-FIRST identified the forced projector contrast, dimension-null overlap, missing numerical/tie rules and historic-contract drift. This version adds random-baseline guards in the same layers, separates statistic-specific INVALID, pins the original harvest and keeps queue consequences utility-gated. Review text is `/private/tmp/new1-prereg-ux4bb37p/criteria_advisor_review.md`; drafting metadata checks are in that directory. Draft completion is not execution approval.

**Context rule, binding through every handoff:** watch `Context N% left`; before ~20%, stop starting new work and write done/in-flight work, exact paths, next step and risks into the task report, then say so for a fresh successor. Every handoff restates this rule. For this draft, the task report is this file; remaining next step is review/freeze before any separately authorized computation.

## Handoff — 2026-10-09

**Done:** DRAFT v1 is written with exact input pins, formulas, fixed predictions, controls, S-3 boundaries, spending caps and conditional queue consequences. The full final advisor artifact was read; its retained-rank and cutoff-index clarifications are applied, satisfying its conditional **PROCEED for DRAFT delivery only**. No geometry was run. **In flight:** final document validation and local session-state capture only. **Exact paths:** this draft, `/private/tmp/new1-prereg-ux4bb37p/input_inventory.json`, `metadata_checks.json`, `protected_source_audit.json`, and `final_draft_advisor_review.md`. **Next step:** finish those static checks and deliver the draft; any execution requires review/freeze and separate authorization. **Risks:** geometric predictions and complete-workload resource feasibility remain NOT RUN / UNVERIFIED; this proxy has no calibration or demonstrated prospective utility, so no queue action is currently eligible.

**Context rule, restated:** watch `Context N% left`; before ~20%, stop starting new work, save done/in-flight work, exact paths, next step and risks into the task report, then say so for a fresh successor. Every handoff restates this rule. This draft is the task report; the handoff is saved here.

**Draft closeout — 2026-10-09:** static validation passed for 15 existing input pins, five adapter provenance pins and 23 explicit file:line citations; seven protected sources are unchanged. The advisor's two final clarifications are applied. Local session state is captured in `/private/tmp/new1-prereg-ux4bb37p/session_checkpoint.md`. No drafting work remains; review/freeze and separately authorized execution remain future steps.

## 9. Fold log — Astra NEW1 r1 (2026-10-09)

Source: `results/mathlab_staging/new1_prereg_astra_r1.md`, FIX-FIRST. Primary input pins, bins, thresholds, prediction rules and utility gate are unchanged.

| Item | Disposition | Fold |
|---|---|---|
| B1 CPU admission, additive reserve and verified supervisor enforcement | **FOLDED / verbatim** | §6 contains the review's exact quoted replacement text. NEW1-specific supervisor and CPU computation worker are built tests first; no real geometry is authorized by this build. |
| ADV retain harvest 1; never combine identities/admissions | FOLDED | §2 explicitly binds only harvest 1 and its unchanged A7 SHA `abb882982f406ddd5d6536529ce49dee8f31ad3b3243495e93687266e7c6582f`. |
| ADV descriptive M16 truncation | FOLDED | §4 reports retained energy, effective rank and covariance fractions under the fixed boundary rule; full M remains every primary comparator. |
| ADV spectrum-matched random null | FOLDED | §5 reuses seeded orientations with s(D); descriptive only, preserving flat-spectrum primary q95. |
| ADV undefined random-like veto | FOLDED | §7 removes that undefined veto; numeric primary guards and the frozen shuffle rule remain. |
| ADV workload budget caveat | FOLDED | §6 retains complete-workload **UNVERIFIED** disclosure; caps and reserves are spending/admission limits, not demonstrated feasibility. |

**Build-only boundary:** this revision authorizes implementation and synthetic fixture verification, never the real adapter/covariance/harvest geometry. Implementation and RED/GREEN evidence are reported in `results/mathlab_staging/new1_v2_build_report.md`. DRAFT v2 remains NOT FROZEN.

## Amendment A1 (D-NEW1-a1)

**2026-10-10 UTC — team-delegated decision by MAESTRO2; the operator may veto.** Adopt only the first choice in `results/mathlab_staging/new1_svd_ruling_astra.md` (GPT-6-Astra: FAITHFUL-GATE-FAILURE). This append-only amendment clarifies §3, originally line 51, of FROZEN v2; all frozen v2 bytes above this section remain unchanged. Tier remains **MATH-PROXY — math estimate, not evidence**.

For the covariance validity checks, promote the temporary **U, s, Vh and C blocks to CPU float64 before scaling and before every blocked matrix product**. Scale promoted U blocks by promoted singular values, reconstruct in float64 blocks, and compute the SVD reconstruction, PSD reconstruction and orthogonality residuals and reductions in float64. Casting an already-computed fp32 scale or product to float64 does not satisfy A1. Preserve the original formulas and use covariance blocks of at most 256 columns; do not materialize a full float64 C.

The covariance decomposition itself remains **native fp32, exactly one full covariance SVD per layer**, reused for every arm/control. **Q is the unmodified native U**; returned singular values and cutoff-selected subsets retain their native-fp32 origin. Construct the native-fp32 P from that same Q and the same native singular-value mask; its captured count/hash or four frozen projection probes must still match. Temporary float64 check operands must never replace or modify the native U, s, Vh, C, Q or P used by the registered estimand and identity checks.

All cutoffs, bins, tie rules, acceptance thresholds and other gates are unchanged: symmetry relative error **≤1e-6**; SVD and PSD reconstruction relative errors **≤1e-5**; orthogonality error **≤1e-5**; native projector parity relative error **≤1e-6**; complement checks **1e-5**. There is **no tolerance relaxation, basis refinement, float64 covariance SVD, second covariance decomposition, symmetrization, clipping or cutoff change**. The existing float64 economy SVD for the saved update is unaffected. Resource reserves, 1,800-second deadline, 300-second wait and 6-GiB RSS cap remain unchanged; full-workload feasibility remains UNVERIFIED.

The halted attempt `results/mathlab_staging/runs/new1_20261010T022922.650234Z` remains **INVALID-WORKER / INVALID, predictions NOT COMPUTED**, with all events, diagnostics and old-hash receipts preserved. Its recorded L4 validity failure is not reclassified under A1. Promotion may separate check-product rounding from native factorization error; passing the unchanged gates on the real inputs remains **UNVERIFIED**. This amendment authorizes the narrow implementation and small synthetic CPU verification only; it performs no real geometry or automatic relaunch. Any separately authorized future attempt must use a fresh run namespace and pin the SHA-256 of the complete preregistration including this amendment.
