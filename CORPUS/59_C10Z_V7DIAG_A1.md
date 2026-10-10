# 59 — V7 population diagnostic: A1 confirmed; frozen R1000 continuation prepared

_Evidence snapshot: 2026-10-09 22:22 UTC, from the Astra FOLD-OK drafts. Subsequent run outcomes are outside this record; attempt 4 and MathLab step 3 remain PENDING._

_Record 2026-10-09. D-C10z-v7diag and D-C10z-a1pop. This is a statistic-fidelity diagnostic and continuation-preparation record; it does not close the ASTRA experiment or establish a candidate/F1 result._

<!-- BEGIN D-C10z-v7diag -->
## D-C10z-v7diag — DONE, diagnostic outcome A1 confirmed

⟨D-C10z-v7diag@d8c55e7b⟩

**Question and pre-registration.** Can the unchanged V7 statistic gate pass for a pre-pinned reference population, after attempt 3 faithfully HALTED-V7? The forward-only, pristine diagnostic was frozen before measurement in docs/C10Z_ASTRA_PREREG.md:702. It measures F1000 first and R1000 next; R5000 is conditional, never a population search. P requires finite Spearman rho ≥ 0.80 at every cached layer 4–12. E is reported only. The routing is INCONCLUSIVE if integrity/completion fails or F1000 passes; otherwise R1000 passing selects A1, conditional R5000 passing selects A2, and both failing selects D. There is no C branch. Arithmetic, masking, 100-token truncation, 16-row batching and all-36-layer capture remain fixed (docs/C10Z_ASTRA_PREREG.md:750; docs/C10Z_ASTRA_PREREG.md:777).

**EVIDENCE-SHOWS: A1.** The measured run is results/c10z_v7_diagnostic/20261009T182427Z/. Its verdict reports complete cleanup, complete measurement, A1, exactly pinned R1000 passing P, and supervisor-observed worker exit 0 (results/c10z_v7_diagnostic/20261009T182427Z/verdict.json:3; :10; :15; :95). GPT-6-Astra independently returned CONFIRM, verified provenance, decoded the saved tensors without Torch, reproduced all 18 correlations within 1e-12, and matched all E values exactly (results/c10z_v7_diagnostic/reading_astra.md:1; :5; :7).

| Population | Recorded nonpadding tokens | P | Limiting correlations | Consequence |
|---|---:|---|---|---|
| F1000 | 99,610 | false | layer 8 = 0.7718877413577638; layer 12 = 0.7669838841007325 | Does not trigger the F1000 INCONCLUSIVE branch |
| R1000 | 95,610 | true | minimum across layers 4–12 = 0.9291099440335273, at layer 8 | A1 selects this exact recorded population |
| R5000 | not measured | not evaluated | no observations | Correct conditional stop; no A2 claim |

Sources: results/c10z_v7_diagnostic/20261009T182427Z/verdict.json:29; :41; :66; :78; results/c10z_v7_diagnostic/reading_astra.md:5; :7. All measured correlations are defined and finite. Runtime was 354.146 s against the frozen 3,060-s cap, with clean exit after cleanup (results/c10z_v7_diagnostic/reading_astra.md:5).

**What this resolves.** The measured agreement is population-dependent and supports the population explanation of V7 behavior on these two pinned populations. It licenses the exact A1 continuation prescribed by the frozen routing, after its own amendment/build/admission gates.

**Caveats kept flush.** Attempt 3 remains HALTED-V7. Its original dataset identity is UNVERIFIABLE and its physical cause is unresolved; this fresh F1000 observation does not recover that historical identity. Late-layer fidelity remains UNVERIFIED. CPU recomputation of saved statistics is not CPU/MPS equivalence proof. No candidate, method-family rescue, deployable write, or F1 closure follows (docs/C10Z_ASTRA_PREREG.md:798; results/c10z_v7_diagnostic/reading_astra.md:11).

The earlier 20261009T182053Z launch exited 3 at GPU exclusivity before probe/model execution, with no population observations. Preserve that non-run refusal; it neither consumes a diagnostic measurement nor supplies a reading-around (results/c10z_v7_diagnostic/reading_astra.md:9).

**Decision and FORK.** D-C10z-v7diag: diagnostic DONE/A1, Astra CONFIRM. Continue only through D-C10z-a1pop's exact frozen population, final source pins, benchmark admission and fresh attempt-4 gates. Diagnostic tensors cannot substitute for baseline/LAW/V7 completion.
<!-- END D-C10z-v7diag -->

<!-- BEGIN D-C10z-a1pop -->
## D-C10z-a1pop — FROZEN preparation; benchmark #3 ADMITTED; attempt 4 PENDING

⟨D-C10z-a1pop@1ef441d3⟩

**Design and authority.** Section 12 A1-POP is FROZEN; Astra's implementation r2 is FREEZE+GO. The reviewed A1 build is commit 0ef326e5229ac449664da89ff4984603e1b2378d. The final prereg pin is 5ad59d2c960b44d18b5d1c5410028b969aab93298eed5d42c527bd81a4d18eac (docs/C10Z_ASTRA_PREREG.md:821; results/c10z_astra_attempt4_prep/a1_astra_r2.md:1; results/c10z_astra_attempt4_go_record.json:22).

Reference-D is exactly results/c10z_astra_attempt4_prep/reference_R1000.json, raw SHA-256 a477f1c4917de988682da097d460c3d70b4c3bd33856d83c1d0c7714f78aab68: the recorded dataset revision/order, ordered indices, row IDs, text hashes/texts, token IDs and counts, 1,000 rows and 95,610 tokens. Another coherent 1,000-row set is inadmissible. The frozen model/tokenizer/cache identities and original arithmetic, precision, masking, truncation and batch shapes apply; CPU fixtures do not establish MPS equivalence. A1 retains the 1,000-row/300-s reference-D allowance; A2's 5,000-row budget does not apply (docs/C10Z_ASTRA_PREREG.md:831; :835; :837; :864).

**EVIDENCE-SHOWS: benchmark drift rerun #3 admitted.** Selected record: results/c10z_astra_benchmark/20261009T202713Z_drift3_a1/benchmark.json, raw SHA-256 facebb52c2300c5af785e63f4f85af09f222a15e4673ba53b93da11314e8d669. Benchmark source SHA-256 is 3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041. The persisted receipt independently validates raw arrays, final source/environment bindings, unchanged weights and exact frozen sizing. Astra returned ADMIT+GO (results/c10z_astra_attempt4_prep/admission_receipt_drift3.md:15; :16; :18; :109; results/c10z_astra_attempt4_prep/go4_astra.md:1; :13).

| Admission item | Recorded/recomputed result |
|---|---|
| Benchmark status / timing source | COMPLETE / BENCHMARK; weights_unchanged=true; suspect=false; outliers=false |
| Nominal stage ceilings C01 / C2 / C3 | 9,900 / 14,100 / 24,060 seconds |
| Absolute admission bounds | 7,200 ≤ 9,900 ≤ 10,800; 2(9,900 + 14,100) = 48,000 ≤ 55,800 |
| Nominal supremum / separately recorded stage sum | 48,000 s / 48,060 s |
| Prior outcomes/counts | Four retained benchmark records, 0 refusals, 0 STOPs; no reset |
| Additional rerun authority | This named #3 only; no automatic fourth rerun |

Sources: results/c10z_astra_attempt4_prep/admission_receipt_drift3.md:14; :16; :17; :19; :48; :51; :52; :53; :54; results/c10z_astra_attempt4_prep/go4_astra.md:9; :11. These are nominal sizing deadlines, not a hard completion guarantee (results/c10z_astra_attempt4_prep/admission_receipt_drift3.md:58). Preserve every earlier benchmark outcome and attempt-3 artifact.

**Go publication and pending work.** The live-path file results/c10z_astra_attempt4_go_record.json is present and byte-identical to the reviewed draft, SHA-256 850988a5df22446d1f456c2ce270e2bffcd988c6f118bcb14d77f4f1ae9ca04f. It binds the benchmark/script hashes, exact ceilings, amendment, prereg and exact population, with operator_yes=true and one_gpu_job=true (results/c10z_astra_attempt4_go_record.json:2; :3; :4; :5; :20; :21; :22; :25; results/c10z_astra_attempt4_prep/admission_receipt_drift3.md:111).

**Publication-metadata caveat.** Its decision_notes["0"] still says "draft only, not a live go or dispatch", and recorded_by still says pending live publication (results/c10z_astra_attempt4_go_record.json:11; :24). The file's presence at the live path is verified; this draft does not invent a later publication timestamp, revised recorder, or launch-validation receipt. Astra's statement that the live file was absent was true at its earlier review, not at this cutoff (results/c10z_astra_attempt4_prep/go4_astra.md:17; :19). MAESTRO owns any resolution through the frozen publication/binding procedure; do not silently edit go bytes or infer GPU clearance from this file.

At this cutoff results/c10z_astra_attempt4/ does not exist: **attempt 4 PENDING, no result claimed**. A fresh namespace must rerun the full baseline, LAW gates, V7 and subsequent candidate/process-2 gates. Exact source/environment bindings must remain valid. Another V7 failure is terminal HALTED-V7 under this authorization, without a further population search or automatic benchmark #4 (docs/C10Z_ASTRA_PREREG.md:866; :868; :870; results/c10z_v7_diagnostic/reading_astra.md:18).

**Decision and FORK.** D-C10z-a1pop: FROZEN; named benchmark #3 ADMITTED; approved go bytes present at live path; attempt 4 PENDING. Candidate success, locality, deployment, MPS equivalence and F1 implications remain UNVERIFIED. This closes only the recorded preparation milestone after MAESTRO's tracker fold-in, not the future attempt.
<!-- END D-C10z-a1pop -->

## 2026-10-10 — Current continuation status superseded

D-C10z-a1pop ⟨D-C10z-a1pop@1ef441d3⟩: preparation/admission preserved; current continuation CLOSED by D-C10z-a4 ⟨D-C10z-a4@e0a21d13⟩ → CORPUS/61_C10Z_ATTEMPT4_UNDERFIT.md. Historical preparation snapshot and both fingerprinted spans above remain unchanged.
