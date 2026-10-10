# 60 — MathLab: preserved replay failures, corrected norm contract, and bounded offline reproduction

_Evidence snapshot: 2026-10-09 22:22 UTC, from the Astra FOLD-OK drafts. Subsequent run outcomes are outside this record; attempt 4 and MathLab step 3 remain PENDING._

_Record 2026-10-09. D-ML-1 / D-ML-2 / D-ML-3. Tier: I-INFER (MATH-PROXY). Interim instrumentation record; no behavioral claim, proxy-calibration PASS, prospective queue utility, route closure or F1 closure._

<!-- BEGIN D-ML-1 -->
## D-ML-1 — harvest milestones; lab calibration still unverified

⟨D-ML-1@12c5548b⟩

**Question and design.** Can a read-only observer harvest the unchanged harness's operands, then reproduce its solve offline before considering frozen proxy calibration? The preregistration separates step 1 harvest, step 2 exact replay and step 3 calibration. LAW#5, observer parity, LAW#3 and frozen context/tokenization/source identities precede mint replay; gate/admission labels are independent of proxy scores (docs/MATHLAB_PREREG.md:141; :177; :241). The lab writes only staging outputs; supervised fold-in belongs to the lead, and nothing is promoted above I-INFER (MATH-PROXY) (docs/MATHLAB_PREREG.md:263; :264).

**EVIDENCE-SHOWS: two distinct completed harvests.**

| Record | Harvest 1 | Harvest 2, under NORM-CONTRACT |
|---|---|---|
| Operand namespace | results/mathlab/harvest_20261009T184950.056951Z/ | results/mathlab/harvest_20261009T203705.724371Z/ |
| Event namespace | results/mathlab_staging/runs/harvest_20261009T184932Z_95961/ | results/mathlab_staging/runs/harvest_20261009T203702Z_6589/ |
| Terminal event | run_finished PASS, 19:26:01.185631Z | run_finished PASS, 21:14:57.130179Z |
| Mint shared identity checks | passed | passed |
| mint1_s0 / s1 / s2 admission | INVALID-REPLAY / INVALID-REPLAY / INVALID-REPLAY | ADMITTED / ADMITTED / ADMITTED |
| Admitted mint seeds | 0 | 3 |
| Norm check | Original fp64-versus-historical-fp32 comparison failed | Returned native scalar check passed all 15 layer/seed comparisons, relative error 0 |
| Manifest SHA-256 | bb9a6f9ad76678ae2289151c9fa64fb0033a6b8b2d7aff0b9a03150180f1ba7e | ef72e0adf4d6da5c3272c57a4189b919226dbf290615773d36af9bc746df0731 |
| Frozen prereg SHA-256 | 4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507 | 85b389ec92248dbccf61d4ecc1de65f47bedf5ce99f88f17866f0db29d3e4bf8 |

Sources: results/mathlab_staging/runs/harvest_20261009T184932Z_95961/events.jsonl:842; results/mathlab_staging/runs/harvest_20261009T203702Z_6589/events.jsonl:842; results/mathlab/harvest_20261009T184950.056951Z/manifest.json:4; :71113; :71231; results/mathlab/harvest_20261009T203705.724371Z/manifest.json:4; :71257; :71379. PASS in these terminal events means the operand-harvest process completed; it is not a claim that every mint admission gate passed.

Fresh baseline counts used by the manifests are A1 68/72, A2 71/72 and A7 14/72 in both harvests. In harvest 2 the mint calibration counts 46/37/40 are **verified historical counts**, not new mint behavioral evaluations (results/mathlab/harvest_20261009T184950.056951Z/manifest.json:71122; results/mathlab/harvest_20261009T203705.724371Z/manifest.json:71270). LAW#3, LAW#5, observer parity and source-unchanged gates passed; observer parity used torch.equal at all five band layers. The observer does not replace the harness/engine write primitive (results/mathlab/harvest_20261009T203705.724371Z/manifest.json:32421; :32610; :32657; :51942).

**Diagnosis and evidentiary boundary.** The historical writer's scalar is float(upd.float().norm()), a native CPU fp32 reduction of the fp32 pre-cast update. The first observer instead compared a CPU fp64 reduction. On all five preserved A7 updates, the native reduction equals the historical scalar exactly, while the fp64 reduction reproduces the 0.00192023–0.00602151 discrepancy. The original bar is 1e-3 relative (results/mathlab_staging/mint_norm_diagnosis.md:7; :28). Astra's diagnosis-only review was GO (results/mathlab_staging/mint_norm_diagnosis_20261009T193234.646267Z/astra_diagnosis_review.txt:1; :5).

For the first harvest's mint failures, measurement mismatch is a **strong inference**, not a same-tensor per-seed demonstration: mint pre-cast tensors/native returned norms and historical full mint tensors were not retained. Equal norms cannot establish tensor identity; matching current projectors cannot establish historical projector identity (results/mathlab_staging/mint_norm_diagnosis.md:9; :74; results/mathlab_staging/mint_norm_diagnosis_20261009T193234.646267Z/astra_diagnosis_review.txt:6).

**What this resolves and does not.** Harvest 2 establishes admission under the amended comparison on its own fresh identity. It does not relabel, backfill or admit any harvest-1 mint arm. Harvest 1 has fewer than two admitted mint seeds and is ineligible for valid calibration under the frozen rule; no step-3 execution or verdict on it is asserted. Three admitted seeds make harvest 2 eligible for the unchanged nine-ordering calibration criterion after its own step-2 gate, not a calibration PASS (docs/MATHLAB_PREREG.md:244; :247; :249; :253; :397; :406).

**Decision and FORK.** D-ML-1: two completed operand harvests preserved separately; first mint replay INVALID-REPLAY, second all three mint seeds ADMITTED. The first-harvest step-2 result is recorded under the D-ML-2 span below. Continue harvest-2 reproduction/calibration on its own artifacts through unchanged gates; calibration and prospective utility remain UNVERIFIED. Harvest-2 step 2 started at 21:15:35Z; completion and verdict remain UNVERIFIED at the reviewed snapshot (results/mathlab_staging/runs/m2_20261009T211535Z_57196/events.jsonl:1). Step 3 PENDING; it has not run in this reading. These subsequent outputs remain outside this milestone close-out.
<!-- END D-ML-1 -->

<!-- BEGIN D-ML-2 -->
## D-ML-2 — M2-BUDGET implemented; harvest-1 step 2 PASS with zero replay errors

⟨D-ML-2@99a9fb4c⟩

**Pre-registered resource correction.** Section 14 M2-BUDGET raises step 2's hard deadline to 6,540 s and the SVD pre-cell reserve to 5 GiB; solve reserve remains 9 GiB, step 3 remains 1,800 s, and the index remains 300 s. The watchdog, memory floor/wait, abort policy, niceness/timeout procedure and scientific gates are unchanged. The implementation was test-first and accepted on CPU fixture/tooling evidence; it does not authorize reinterpretation of earlier outputs (docs/MATHLAB_PREREG.md:380; :389; :391; results/mathlab_staging/build_report.md:1823; :1831; :1842).

**EVIDENCE-SHOWS: bounded reproduction on harvest 1.** The requested run results/mathlab_staging/runs/m2_20261009T192821Z_82233/ started at 19:28:21.660761Z and finished PASS at 20:27:00.569802Z, about 3,519 s within its 6,540-s deadline. Gate 2a passed 15 arm/layer comparisons: A1_single, A2_coherent2 and A7_coined_coined, five layers each. Every projector/update check passed and every recorded relative error is 0.0 (results/mathlab_staging/runs/m2_20261009T192821Z_82233/events.jsonl:1; :1543; :1547).

The authoritative result is results/mathlab/m2_20261009T192823.926873Z/manifest.json, SHA-256 812f8dbdaa872aa4f46e5f38862a1d772cd2e5fe16184a751870f4c8913d359a. Its harvest pointer/hash is exactly the **first** harvest; its prereg pin is the first harvest's 4852d1a2… (results/mathlab/m2_20261009T192823.926873Z/manifest.json:4; :5; :9). The completed run is never merged or repinned to harvest 2.

**Meaning of "bit-exact".** All five A7 full-tensor comparisons have zero relative Frobenius error: the replayed native fp32 pre-cast updates match the saved A7 updates exactly. A1 and A2 have zero error on the frozen **fp64 norm** comparison; their full pre-cast tensors were not retained, so this record does not claim their full-tensor identity. This is the actual gate shape, not 15 retained full-tensor comparisons (docs/MATHLAB_PREREG.md:160; :181; :183; :184; mathlab/core.py:255; :258; results/mathlab/m2_20261009T192823.926873Z/manifest.json:11).

**Scope gate and rounding, kept flush.** Gate 2b is OPERANDS-ONLY, not ALT-SOLVES-ADMITTED. It is a scope gate and does not stop the lab; alternative solves require their own authorized harvest. The A7 fp16 cast/add relative rounding differences at layers 4–8 are 0.001152968798870012, 0.0019109179517091414, 0.002105904822271678, 0.0012443304932961555 and 0.0009435913501004509. Exact replay of pre-cast updates does not imply bit-exact deployed changes (results/mathlab/m2_20261009T192823.926873Z/manifest.json:134; :135; docs/MATHLAB_PREREG.md:188; :194; :196).

**Decision and FORK.** D-ML-2: bounded resource amendment implemented, and this one harvest-1 step-2 run PASS. Its mint arms remain INVALID-REPLAY and were excluded from the 15 replay comparisons; it cannot validate mint admission or calibration. This run's observed completion does not establish a universal deadline/memory guarantee for larger admitted-arm workloads. No behavioral or prospective queue-utility claim follows.
<!-- END D-ML-2 -->

<!-- BEGIN D-ML-3 -->
## D-ML-3 — NORM-CONTRACT FROZEN, corrected implementation reviewed, fresh admission recorded

⟨D-ML-3@84e9d0e1⟩

**One measurement-contract correction.** Section 15 is a post-failure frozen amendment, with all Astra r1 BLOCKING/ADVISORY folded. Persist n_native from the unchanged H.my_edit return for the same observed write; do not recompute it. Compare |n_native − delta_norm_F| / delta_norm_F ≤ 1e-3 using CPU fp64 subtraction/division. Record producer Torch version and thread count; missing/nonfinite scalars fail closed. Retain captured fp64 upd_norm for diagnostic analysis and as the unchanged non-A7 gate-2a reference. A1/A7 historical comparisons remain reported-only; mint keeps per-arm admission. No solve/cast/add, target, context, projector, shared-check, LAW gate, threshold or tensor-identity rule changes (docs/MATHLAB_PREREG.md:395; :402; :403; :404).

**Review and implementation.** Astra implementation r1 found a real persistence blocker: coverage failure occurred before native scalars/producer metadata were preserved. The persistence-only fix collects and saves those returns before coverage enforcement, retains duplicate occurrences without falsely assigning overwritten scalar values, and leaves the CAPTURE HALT intact. Astra r2 returned GO, verified the exact 85b389ec… prereg pin and unchanged harness/engine/core, and reran 77 MathLab plus 53 dashboard tests (results/mathlab_staging/dml3_impl_astra_r1.md:6; results/mathlab_staging/build_report.md:1999; :2003; :2005; :2007; results/mathlab_staging/dml3_impl_astra_r2.md:1; :6; :10; :11; :12).

**Acceptance boundary.** R2's CPU review left live corrected-harvest acceptance unverified at that earlier time. The separately authorized fresh harvest subsequently finished and admitted all three seeds under the corrected native comparison; its exact manifest/admission outcomes are in the D-ML-1 span above. Producer metadata records Torch 2.8.0 and 12 CPU threads (results/mathlab/harvest_20261009T203705.724371Z/manifest.json:13571; :71257; :71379). This later record is not a retrospective upgrade of harvest 1.

**Decision and FORK.** D-ML-3: FROZEN NORM-CONTRACT implemented and reviewed GO; its one fresh harvest records corrected mint admission. The 1e-3 bar and admission-dependent calibration criteria are unchanged. Fewer than two admitted seeds would remain INVALID calibration; with three, the unchanged nine-ordering/bootstrap rule applies. No further metric change or additional harvest is authorized by this amendment, irrespective of outcome (docs/MATHLAB_PREREG.md:408). Calibration, behavioral utility and F1 remain UNVERIFIED.
<!-- END D-ML-3 -->

<!-- BEGIN MATHLAB CALIBRATION STOP 2026-10-09 -->
## 2026-10-09 addendum — harvest-2 calibration FAIL; lab STOPPED (D-ML-1 / D-ML-4)

_This final reading supersedes the interim step-2/step-3 status in the dated snapshot above; it preserves both harvests and all earlier replay failures. Decisions: D-ML-1 final calibration reading; D-ML-4 calibration FAIL lab stop and step-4 shelving. Tier: **I-INFER (MATH-PROXY)**. Independent review: GPT-6-Astra (high), **CONFIRM**, `results/mathlab_staging/m3_reading_astra.md` (read in full)._

### Artifacts and admission

| Record | Exact artifact |
|---|---|
| Harvest 2 | `results/mathlab/harvest_20261009T203705.724371Z/manifest.json` |
| Step 2 run | `results/mathlab_staging/runs/m2_20261009T211535Z_57196/events.jsonl` |
| Step 2 output | `results/mathlab/m2_20261009T211538.263001Z/manifest.json` |
| Step 3 run/admission | `results/mathlab_staging/runs/m3_20261009T225554Z_55441/events.jsonl`, `admission.json` in the same run directory |
| Step 3 output | `results/mathlab/m3_20261009T225557.353172Z/calibration.json`, `manifest.json` in the same output directory |
| Frozen rule | `docs/MATHLAB_PREREG.md` §4.3 / §8; SHA-256 `85b389ec92248dbccf61d4ecc1de65f47bedf5ce99f88f17866f0db29d3e4bf8` |

Harvest-2 manifest SHA-256 is `ef72e0adf4d6da5c3272c57a4189b919226dbf290615773d36af9bc746df0731`; its step-2 manifest SHA-256 is `c2efd6bd8ddcb31e103dbf0c356a81e5901971121a39aba476dead05d83dffde`. Step 3 binds these exact sources and the same frozen prereg. Astra independently rehashed **56 file references** successfully and confirmed that all **73 harvest source hashes** remain unchanged. Admission passed; **all three mint arms are ADMITTED**. These are the corrected harvest-2 inputs, not the INVALID-REPLAY mints of harvest 1.

**Step 2 on harvest 2: PASS, 61/61 gate-2a checks.** Its terminal event is PASS at `2026-10-09T22:55:45.960191Z`. Gate 2b remains **OPERANDS-ONLY**; it does not invalidate this calibration and does not establish deployed fp16 bit equality.

### Frozen criterion and valid tiers

A proxy passes only if every top arm strictly exceeds every admitted middle arm, every admitted middle arm strictly exceeds A7, and **each of the nine required orderings holds in at least 1,900/2,000 paired subject bootstrap resamples**. The same subject draw is shared across both proxies and all arms: **PCG64(0), 24 subjects, three paraphrases each**. Calibration passes when at least one proxy passes (`docs/MATHLAB_PREREG.md` §4.3).

Calibration uses **A1=68, A2=71, mint s0/s1/s2=46/37/40, A7=14**. A1/A2/A7 are fresh harvest outcomes; the mint counts are verified historical outcomes, not new behavioral evaluations. Tier margins are **22** (top minus middle) and **23** (middle minus bottom), both at least 10. All **12 arm/proxy arrays contain 72 finite values**; there is no INVALID-ARITHMETIC. Astra's independent NumPy recomputation from the saved values exactly matches the scores, point orderings and bootstrap counts; its review used no model/torch/GPU execution.

### VERDICT — valid calibration FAIL, the designed cheap stop

| Arm | Sρ | Scoll |
|---|---:|---:|
| A1 | 0.753970 | −0.049858 |
| A2 | 0.725869 | −0.050704 |
| mint s0 | 0.758199 | −0.051046 |
| mint s1 | 0.733293 | −0.049738 |
| mint s2 | 0.740254 | −0.049699 |
| A7 | 0.758815 | −0.051835 |

Each cell gives **strict point ordering; bootstrap count /2,000**. Every row must have a true point ordering and count ≥1,900 for that proxy to pass.

| Required ordering | ρ | coll |
|---|---:|---:|
| A1 > s0 | false; 742 | true; 1403 |
| A1 > s1 | true; 1926 | false; 890 |
| A1 > s2 | true; 1641 | false; 1233 |
| A2 > s0 | false; 49 | true; 1058 |
| A2 > s1 | false; 589 | false; 579 |
| A2 > s2 | false; 221 | false; 814 |
| s0 > A7 | false; 975 | true; 1247 |
| s1 > A7 | false; 156 | true; 1474 |
| s2 > A7 | false; 340 | true; 1210 |

**Both proxies FAIL**, so the “at least one proxy passes” rule fails. The authoritative step-3 terminal event is **FAIL** at `2026-10-09T22:56:07.955045Z`, **12.964 s** after run start, consistent with the exit **3** reported in the reviewed reading. A stage-completion PASS records completion of work and does not override the terminal calibration FAIL. This is a valid failed calibration, not INVALID-TIERS, INVALID-REPLAY or an arithmetic failure.

### Consequences, caveats and FORK

**D-ML-4: STOPPED — calibration FAIL; step 4 SHELVED.** The lab stops under the frozen §8 (`docs/MATHLAB_PREREG.md:258`). An amended proxy requires a **written amendment and calibration on unused arms**; rescoring these six arms is not calibration. The step-4 draft is retained **SHELVED / NOT FROZEN / NOT RUN** because its explicit harvest-2 calibration-PASS prerequisite failed (`docs/MATHLAB_STEP4_PREREG.md:3`). No step-4 launch or queue action follows.

This is a **MATH-PROXY tooling finding only**: these two frozen proxies fail the registered tier-separation criterion on these arms. It supplies no behavioral claim, route closure, F1 conclusion or statement about other proxies. The additive residual ignores attention and later-layer responses; fp16 cast-and-add rounding remains an approximation. The reported injection/write consistency checks are non-gating and never calibration evidence. The uniform-random-ranking calculation is not a calibrated false-positive rate: the mint seeds are correlated and the arm families were chosen deliberately. Prospective queue utility remains **UNVERIFIED**.

**NEW-1 continues separately and is not falsified or automatically shelved.** It pins **harvest 1**, has its own descriptive geometry predictions, and retains its independent build/execution gates (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:29`). This fold and Astra's review authorize no launch. Geometry-driven queue use still needs its **own calibration and demonstrated prospective utility** (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:135`). Do not merge harvest-1 and harvest-2 operands, admissions or claims.

FORK: close the current lab at its preregistered cheap stop; retain step 4 shelved. Any future proxy work must take the written-amendment/unused-arms route. Keep NEW-1's separately gated descriptive work distinct. Engine/science sources, frozen rules and result artifacts are unchanged by this supervised documentation fold.
<!-- END MATHLAB CALIBRATION STOP 2026-10-09 -->

Current calibration/stop currency: ⟨D-ML-1@46230e48⟩ ⟨D-ML-4@46230e48⟩.
