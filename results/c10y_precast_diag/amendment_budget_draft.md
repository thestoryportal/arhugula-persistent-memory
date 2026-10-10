# DRAFT — Amendment PRECAST-BUDGET

**Date:** 2026-10-09 (operator local date). **Decision-ID:** D-C10y-precast-budget. **Status: DRAFT / NOT FROZEN / NOT APPLIED / NO RUN AUTHORIZATION.** Intended append-only destination after review: `docs/C10Y_PRECAST_DIAG_SCOPE.md`. The frozen v2 text and its 2,820 s arithmetic remain unchanged. This file contains proposed amendment text, followed by drafting evidence and a handoff; only the marked proposal is intended for a later scope append.

<!-- BEGIN DRAFT AMENDMENT PRECAST-BUDGET -->
## Amendment PRECAST-BUDGET — 2026-10-09 — D-C10y-precast-budget — DRAFT

### Disposition and unchanged scientific contract

The run `results/c10y_precast_diag/20261009T225619Z/` remains **INCONCLUSIVE / SUPERVISOR-TIMEOUT**. `run.json` and `supervisor_timeout.json` record 2,812 s elapsed, cap 2,820 s, worker return code 137, incomplete A7 controls and cleanup, and A1 native/controls NOT-RUN. Retain its committed artifacts and the original diagnosis (`results/c10y_precast_diag/20261009T225619Z_diagnosis.md`); do not finish that namespace or classify its partial captures. Calibration 4 remains terminal ZERO_STEP-IDENTITY.

This proposal changes resource accounting only. It preserves the two arms, five layers per arm, identical-input contract, native captures, separate controls (b)/(c)/(d)/(e), observer validation, all measurements, classification order INCONCLUSIVE → R → S → UNCLASSIFIED, and K-reserved. No numerical tolerance, gate, input or scientific reading changes. No corrective execution, calibration 5, stage-1 dispatch or F1 closure follows. Adoption requires a written frozen amendment, implementation/source repinning and review, separate team admission, a fresh exclusive namespace, and operator-cleared GPU/disk state.

### Time budget from measured phases

The original 600 + 1,360 + 300 + 180 = 2,440 s estimate, multiplied by 1.15 and rounded to 2,820 s, remains the historical frozen budget. The replacement is calculated before dispatch from measured work; no cap may be increased in-run.

| Phase | Measured seconds | Evidence |
|---|---:|---|
| Setup | 8.738558 | `phase_setup_started.json` → `phase_setup_complete.json` |
| Model load | 7.223514 | corresponding model-load phase pair |
| Pristine capture | 34.622965 | corresponding pristine phase pair |
| Projectors | 420.800392 | corresponding projector phase pair |
| A7 targets | 411.631268 | corresponding A7-target phase pair |
| A1 targets | 363.237501 | corresponding A1-target phase pair |
| A7 native capture, all five layers | 578.185085 | corresponding A7-native phase pair |
| A7 full controls | ≥985, unfinished | diagnosis and INCOMPLETE phase/terminal records; **not a completed timing** |
| A1 native/controls | NOT-RUN | terminal phase summary |

All phase paths in this table are under the preserved run directory. Phase elapsed times include their existing capture/persistence overhead. The supervisor covers setup through cleanup and terminal publication; its termination grace remains inside the selected overall cap.

Let `T_fixed = 8.738558 + 7.223514 + 34.622965 + 420.800392 + 411.631268 + 363.237501 = 1246.254198 s`. For each arm `a`, define `C_ctrl[a]` as the **whole five-layer controls phase**, including common-factor preparation, controls (b)–(e), device products/repeats, realizations, all-pair statistics, conditioning/residuals, hash verification, durable writes and validation. A numerical-kernel timer alone does not measure this phase.

The proposed formula is:

```text
T_raw = T_fixed + T_native[A7] + T_native[A1]
        + C_ctrl[A7] + C_ctrl[A1] + T_tail
T_cap = 60 × ceil((1.15 × T_raw) / 60)
```

`T_tail = 180 s` retains the frozen terminal-serialization/restoration allowance; its sufficiency is UNVERIFIED. Phase-local writes already included in measured native/control phases must not be counted again as tail writes. Before freeze, bind every term and its measurement/extrapolation receipt. In particular, do not substitute the unfinished 985 s lower bound for a completed `C_ctrl` measurement.

A7 has two completed control cells, identified by completed `controls_A7_coined_coined_L4_numeric.json` and `...L5_numeric.json`. Their publication mtimes, measured from the controls start and prior cell completion, give approximately **449.628624 s** and **438.203349 s**, including the implemented comparison/conditioning/persistence work. These are cell timing estimates from file publication, not instrumented per-arm phase measurements. Rounded conservatively to 450 s/cell, they project **2,250 s/arm** for five cells. The current provisional model uses A7's 578.185085 s native time also for the unmeasured A1 native phase:

```text
T_raw_provisional = 1246.254198 + 2 × 578.185085 + 2 × 2250 + 180
                  = 7082.624368 s
T_cap_provisional = 60 × ceil(1.15 × 7082.624368 / 60)
                  = 8160 s = 136 min
```

**8,160 s is a DRAFT extrapolation, not an admitted or demonstrated sufficient cap.** A1 timings, remaining A7 layers, cleanup and any changed storage cost are UNVERIFIED. The single-packet CPU timer is to be run only after MAESTRO clears CPU contention with ASTRA. Its measured controls (b)–(e-CPU) are one input to `C_ctrl[a]`; multiply a per-layer result by five explicitly as an extrapolation, retain measured whole-cell costs, and account separately for omitted device/comparison/conditioning/persistence work. The MPS repeat in (e) cannot be timed by a CPU-only script and must not be reported as measured. Before adoption, obtain a defensible full `C_ctrl` receipt or an explicitly reviewed whole-phase projection for **each** arm. Any larger measured/prospective phase cost replaces its corresponding provisional term before recomputing the minute ceiling. This draft does not authorize those measurements or a rerun.

The timeout traceback lands in NumPy per-column quantiles while processing the third A7 cell. Consequently, the unfinished controls phase cannot be attributed wholly to float64 solves; the replacement budget includes statistics, conditioning, persistence and hashing as well as solve/product work.

### Disk budget and pre-dispatch floor

Before dispatch, inventory **incremental writes on the actual output filesystem**, not just free RAM or space on another volume. For each artifact family, record packet shape/dtype, packet count and measured serialized bytes. Use a family ledger `D_projected = Σ_j(N_j × b_j) + B_metadata + B_temp_peak`, where `b_j` is the measured size of the representative packet or family mean derived from an exact measured byte sum. The family-mean shorthand below does not replace the per-file inventory. Count all dtypes and all duplicates; a float64-only subtotal is not a complete disk plan.

Read-only metadata inspection of the preserved run found **622 .pt sidecars totaling 117,364,108,482 bytes**, plus 6,752,330 bytes of JSON. The existing serializer stores full model-state and dense operand copies at many observer/gate checkpoints. Completed A7 native captures and completed L4/L5 control cells provide this provisional uncompressed ledger:

| Family | Measured packets / bytes | Projected occurrences | Projected .pt bytes |
|---|---:|---:|---:|
| Fixed records, including pristine, projectors and both arms' targets | 51 / 8,596,403,387 | 1 | 8,596,403,387 |
| Complete native phase for one arm, five layers | 81 / 74,606,353,731 | 2 arms | 149,212,707,462 |
| Complete controls for one layer | 189 / 11,413,009,617 (same in L4 and L5) | 10 arm/layer cells | 114,130,096,170 |
| **Total** | | **2,103 .pt packets** | **271,939,207,019** |

This is **271.939 GB / 253.263 GiB** of new .pt writes. Shape/count equivalence for A1 and the remaining cells is a documented projection, not a completed run. A minimal proportional metadata estimate is `ceil(6,752,330 × 2,103 / 622) = 22,829,824 bytes`; replace it with the audited final writer plan and include any temporary compression/serialization copies in `B_temp_peak`. Do not treat rounding of the operator's incident note as a byte-accurate plan.

The dispatch condition is:

```text
free_bytes(output_filesystem) >= D_projected + 20 × 2^30
```

With the ledger above, the provisional minimum is **293,436,873,323 bytes = 273.284 GiB**, before any additional temporary-file allowance. This floor is additional free space while preserving the old run; already retained artifacts do not count as free space. Dispatch refusal is fail-closed and persisted before model load. Record the queried filesystem, available bytes, bound family ledger and floor in the admission record. Monitor available space against remaining projected writes plus the 20 GiB reserve before durable phases; refusal stops INCONCLUSIVE while retaining committed evidence. No automatic artifact deletion, offload, overwriting, restart or in-run budget increase follows. The operator owns archive/offload choices.

### Storage options constrained by frozen B1/B4

**B1 requires actual operands/state identity**, including K, cur, residual R, P, C, L2, assembled systems/right-hand sides, factors and native/control updates with dtype/shape/orientation/tensor-byte identities. Measurements 4–6 require their full stated per-column results, fp16 realizations, realized updates and diagnostics. **B4 requires each completed target, operand packet, factor, update and computed gate input to be durably retained before its dependent gate**, including offending values and partial work. Hashes alone do not satisfy either requirement for a unique required tensor.

- **Lossless compression is a possible separately reviewed representation change.** Keep exact original dtype/shape/orientation and raw tensor-byte hashes; preserve a compressed-file hash and exact decoder/version. Measure compressed bytes and encode/decode time on the affected packet families before selecting a new ledger/cap. Demonstrate byte-exact decoding and interrupted/exclusive-write retention. Complete, flush/fsync and validate the referenced payload and metadata before evaluating dependent gates. Do not assume a compression ratio or quantize/demote fp64 operands. Include peak temporary disk use; the 20 GiB reserve is not an implicit allowance for arbitrarily large scratch files.
- **Hash/summary-only records are limited to identities or summaries that the frozen scope already represents that way.** They cannot replace a unique native/float64 operand, system, solution, update, realization, required per-column measurement, or tensor-valued gate input. Duplicate payloads may instead reference an already committed, full, immutable, exact-hash-matching payload in the fresh namespace, provided replay remains complete and each phase's exclusive durable metadata precedes its gate. This is lossless storage deduplication, not permission to discard raw evidence; it needs explicit writer/reader and partial-failure review before adoption.

For either representation option, redo the measured byte/count ledger and full-phase time model. A sparse or hash-only post-hoc rewrite of this failed run is not proposed. Unchanged scientific gates and persist-before-gate ordering remain binding.
<!-- END DRAFT AMENDMENT PRECAST-BUDGET -->

## Drafting evidence and limits (not scope-append text)

Read in full: the run diagnosis, `run.json`, `supervisor_timeout.json`, every `phase_*.json`, Codex Y3's handoff, and frozen v2 scope including B1/B4 and the 2,820 s arithmetic. Source arithmetic inspected directly: `experiments/track_c/c10y_precast_diag.py` controls / compare_cell and `c10y_directdw_arms.py` factor_solve. No numerical computation on tensor packets, model/tokenizer import, GPU work or measurement-script execution occurred while drafting. Directory statistics and JSON metadata were read with stdlib only.

The operator's incident note reports **131 float64 .pt packets / 105 GB** and disk exhaustion that killed attempt 4's first start. The read-only inventory above uses a different, explicit definition: all 622 .pt sidecars; 415 contain at least one JSON-described float64 tensor and total 24,073,856,821 bytes, while 75 contain a float64 tensor of at least 100 MB and total 23,746,899,069 bytes. **The note's count/dtype definition is not reconciled by this draft.** Preserve the incident note and use the whole measured file ledger for admission rather than assuming it is the complete write budget.

The draft uses metadata/stat observations taken during preparation; the operator may later move packets to `~/Backups/memit_offload/c10y_precast_20261009T225619Z/`. Do not sum original and offload copies as future writes. Re-inventory the actual chosen output filesystem at admission. No old artifacts were moved or deleted by Codex Z3.

The companion `results/c10y_precast_diag/measure_controls.py` accepts one A7 recipe-A layer packet or its JSON metadata. Prefer `controls_A7_coined_coined_L4_control_inputs.pt`, which contains the saved common fp32 factor X; `operands_A7_coined_coined_L4_A.pt` is also accepted and requires a timed fp32 factor-preparation step. Default discovery checks the original run and the operator's offload directory. If only the .pt was offloaded, the script can use matching metadata retained in the original run, with a mandatory sidecar SHA-256 check. It imports no harness/driver/model/tokenizer and never calls CUDA/MPS. It prints phase seconds and process-lifetime peak RSS; CPU-only (e) explicitly leaves the MPS repeat NOT-MEASURED. It writes no tensors, records or labels.

Future invocation example, **not run and not authorized by this draft**:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python results/c10y_precast_diag/measure_controls.py \
  "$HOME/Backups/memit_offload/c10y_precast_20261009T225619Z/controls_A7_coined_coined_L4_control_inputs.pt"
```

**Verification boundary:** syntax/static/source review only; the script is **UNRUN**, including its help path. No `C_ctrl` value from this new script is asserted. Evidence/snapshots: `/private/tmp/c10y_precast_budget_z3.zgxis3d9/`. Frozen scope/implementation/result phase records remain unchanged; no commits or launches.

## Handoff / standby

Done: draft proposal and CPU measurement script. In flight: static validation only until the final verification receipt is appended. Next: MAESTRO/Astra review; any permitted measurement waits for explicit CPU/GPU clearance after ASTRA, then terms/byte counts are bound before amendment adoption and fresh-namespace admission. Attempt-4 outcome standby retains priority if MAESTRO interrupts. Risks: unmeasured per-arm totals, unmeasured compression/temporary-write cost, unreconciled incident-count definition, and no runtime script validation.

**Binding context rule:** watch `Context N% left`; before about 20%, stop starting new work, write done/in-flight work, exact paths, next step and open risks into the task report, and tell MAESTRO to start a fresh successor. Every handoff restates this rule.

## Final drafting verification — 2026-10-10T00:03:38.291539+00:00

Static syntax compilation and import/device scan PASS; packet interface checked against JSON metadata without loading a tensor; time/disk arithmetic PASS. All 27 snapshotted scope/source/result-phase files are unchanged. The measurement script was not imported, executed, or run for help; numerical/runtime behavior remains UNVERIFIED. Only the two requested deliverables were created. Verification receipt: `/private/tmp/c10y_precast_budget_z3.zgxis3d9/verification.json`.

Completion handoff: drafting and static validation are done; no work is in flight. Next is MAESTRO/Astra review, then only separately authorized measurements after ASTRA CPU/GPU clearance. Attempt-4 outcome standby retains priority. Binding context rule: watch `Context N% left`; before about 20%, stop starting new work, write a precise done/in-flight/paths/next-step/risk handoff into the task report, and tell MAESTRO to start a fresh successor. Every handoff restates this rule.

## Disk budget (Z4)

**2026-10-10 UTC; D-C10y-precast-budget remains DRAFT / NOT FROZEN / NOT APPLIED / NO RUN AUTHORIZATION.** This section completes the metadata reconciliation and expands the existing provisional ledger; it is the single amendment home. No tensor was opened, loaded, decoded or hashed. No timer, science reader, model/GPU work, launch, deletion or commit was performed. Attempt-4 outcome assessment remains standby for MAESTRO2.

Notation: `R = results/c10y_precast_diag/20261009T225619Z/`; `D = experiments/track_c/c10y_precast_diag.py`; `S = R/OPERANDS_MANIFEST_sizes.txt`. All bytes below are logical serialized file bytes, including serializer overhead and repeated payloads. `GB = 10^9 B`; `GiB = 2^30 B`. The audit command reproduced at the end reads text/JSON and file metadata only. Its size histograms, sample filenames and manifest line numbers are the packet-size evidence for every projection row.

### (a) Incident / manifest / 622-packet reconciliation

The incident statement at `EXPERIMENT_RUNBOOK.md:259` and `R/OFFLOADED_OPERANDS.json:1` is **105 GB**; the latter records **131 files** moved, with zero reported failures. The preserved size manifest and checksum manifest each have **131 unique filenames**, with exactly equal filename sets (`S:1–131`; `R/OPERANDS_SHA256SUMS.txt:1–131`; audit assertions). Their exact serialized sum is **112,269,967,565 B = 112.269967565 GB = 104.559555 GiB**. Arithmetic reconciles “105” as the rounded **GiB** count of the moved large-packet set. **I-INFER** that the note used this rounded binary unit; the original measurement command is not available here to establish its historical unit. The exact decimal-GB total is 112.269967565. The original note is retained; units are explicit here and the dtype description is corrected from recorded JSON below.

The manifest set equals every reconstructed packet of at least **100,000,000 B** (audit set-equality assertion); this establishes membership, not the operator's historical selection algorithm. Only **75 of its 131 packets** contain a JSON-described float64 tensor, totaling **23,746,899,069 B** of whole files. The other **56**, totaling **88,523,068,496 B**, contain no float64 tensor. The complete inventory has **415 float64-containing packets / 24,073,856,821 B**; the additional **340 / 326,957,752 B** are outside the large-file manifest. These are counts of files containing that dtype, including any other tensors in each file, not counts or byte sums of individual float64 members. Calling all 131 files “float64 operands” misses the large fp32 state/system/operand copies and the mixed fp16/fp32/fp64 packets.

| Writer family | Writer source | All pre-offload .pt: count | All pre-offload bytes | 131-file manifest: count | Manifest bytes |
|---|---|---:|---:|---:|---:|
| Pristine full-model weights | D:644–646 | 1 | 6,172,004,127 | 1 | 6,172,004,127 |
| Five projectors, one packet | D:653–658 | 1 | 2,423,523,673 | 1 | 2,423,523,673 |
| Individual targets, both arms | D:609–618 | 48 | 468,912 | 0 | 0 |
| Aggregate targets | D:619 | 1 | 406,675 | 0 | 0 |
| Native tokenized batches | D:377–384 | 30 | 599,510 | 0 | 0 |
| Native Q intermediates | D:285–300 | 15 | 7,302,297,135 | 15 | 7,302,297,135 |
| Native direct/factor solve inputs | D:303–305,327–330 | 15 | 24,109,066,975 | 15 | 24,109,066,975 |
| Native A/Y operands and updates | D:336–350 | 10 | 17,728,717,400 | 10 | 17,728,717,400 |
| Native Y factors | D:360–369 | 5 | 2,441,351,785 | 5 | 2,441,351,785 |
| Observer on/off state snapshots | D:415–431 | 4 | 11,512,160,668 | 4 | 11,512,160,668 |
| Inertness gate inputs, both snapshots persisted again | D:432; Journal.gate D:56–60 | 2 | 11,512,160,258 | 2 | 11,512,160,258 |
| Controls, device observations, realizations and column statistics | D:451–480,490–508,555–605 | 487 | 28,480,151,659 | 75 | 23,387,485,839 |
| Aggregate update sets | D:573–576 | 3 | 5,681,199,705 | 3 | 5,681,199,705 |
| **Total** | **Audit union, no double counting** | **622** | **117,364,108,482** | **131** | **112,269,967,565** |

The **622 / 117,364,108,482 B** union exactly reproduces Z3's inventory (`amendment_budget_draft.md:61`; `handoff_codexz3_20261010.md:59`). It consists of fixed **51 / 8,596,403,387 B**, complete A7 native **81 / 74,606,353,731 B**, complete A7-L4 and L5 controls **189 / 11,413,009,617 B each**, and unfinished L6 controls **112 / 11,335,332,130 B**. L7/L8 controls and A1 native/controls were not written. The L6 partial is counted in the incident inventory and is not used as a complete-cell estimate.

Current run-directory metadata gives **526 .pt / 25,099,989,424 B**: retained manifest A7-L4 **35 / 20,005,848,507 B**, plus the manifest-excluded **491 / 5,094,140,917 B**. The absent manifest members are **96 / 92,264,119,058 B = 85.927657 GiB**, reconciling §3.3a's rounded “86 GB.” The retained 35 plus absent 96 equal the original 131. All retained manifest sizes match stat metadata. All 131 recorded checksum strings match their corresponding JSON `artifacts` strings; **no checksum was recomputed and no archived/deleted payload was verified**. The audit reconstructs missing-file sizes from S rather than pretending they remain on disk. The operator says the 96 offload files are gone; `R/OFFLOAD_DELETED.json` records that action. Z4 did not inspect the backup directory or verify deletion.

JSON stat totals are **1,780 files / 6,753,416 B**. Excluding the later operational receipts `OFFLOADED_OPERANDS.json` (**342 B**) and `OFFLOAD_DELETED.json` (**744 B**) reproduces Z3's baseline **6,752,330 B** exactly. These historical receipts are not prospective C10Y scientific packets. This distinction retains the existing metadata projection rather than treating offload receipts as part of the frozen writer.

### (b) Full-run projected writes: A7 + A1, layers 4–8, all controls

Counts use the two arms and five layers (`D:15–16,660–670`), 24 targets per arm (`D:662`), both native paths and their observer-on/off validation (`D:417–432`), and the actual completed control-cell writers. Each control cell contains **16 update candidates**: seven in `D:565–574` plus nine returned by `D:459–480`. This gives **120 = 16×15/2** update pairs, **16** realized-weight comparisons, and **12 = 3×4** additional column-statistic groups inside the numeric packet (`D:586–603`). The captured three batch slots per native path/layer are observed A7 metadata, not the observer's weaker minimum-two coverage check (`D:404`).

The audit checks **every L4 packet against the corresponding L5 packet's size**, not only their aggregate sums. Metadata shows common dense shapes: projector/system **[11008,11008]**, update/weight **[2048,11008]**, and key/factor **[11008,24]**; representative metadata are `R/operands_A7_coined_coined_L4_A.json`, `R/controls_A7_coined_coined_L4_system64.json`, and `R/controls_A7_coined_coined_L4_realized_recipe_A.json`. Individual target sizes are measured for both arms. A1 native/control packet equivalence and the unwritten remaining cells are **projections, not runtime measurements**. Admission must recheck pinned dimensions, batch shapes/counts, tensor aliasing and serializer behavior; no reduction is credited for a smaller-looking arm. All existing duplicate packets remain counted.

For stat-derived rows, the sample is under R and is emitted with its exact byte size by the audit. Manifest-derived rows additionally cite S's line. Source D supplies the multiplicity. Each data row is **bytes per packet × full-run count = projected bytes**.

| Family / representative packet | Bytes per packet × count | Projected bytes | Size basis; count source |
|---|---:|---:|---|
| Pristine weights | 6,172,004,127 × 1 | 6,172,004,127 | S:112; D:644–646 |
| Projector set | 2,423,523,673 × 1 | 2,423,523,673 | S:113; D:657 |
| Individual targets | 9,769 × 48 | 468,912 | stat `target_A1_single_00.pt`, all 48 checked; D:611–616,662 |
| Aggregate targets | 406,675 × 1 | 406,675 | stat `targets.pt`; D:619 |
| **Fixed subtotal** | **51 packets** | **8,596,403,387** | **Sum of preceding four rows** |
| Native batch slot 0 | 46,821 × 20 | 936,420 | stat `batch_A7_coined_coined_L4_A_0.pt`; D:377–384,417 |
| Native batch slot 1 | 7,141 × 20 | 142,820 | stat `batch_A7_coined_coined_L4_A_1.pt`; same source |
| Native batch slot 2 | 5,989 × 20 | 119,780 | stat `batch_A7_coined_coined_L4_A_2.pt`; same source |
| Q intermediates, A/Y/factor | 486,819,809 × 30 | 14,604,594,270 | S:83; D:296–299 |
| Native Y factors | 488,270,357 × 10 | 4,882,703,570 | S:76; D:360–369 |
| Y factor solve inputs | 1,456,425,493 × 10 | 14,564,254,930 | S:116; D:303–305 |
| A/Y direct solve inputs | 1,682,693,951 × 20 | 33,653,879,020 | S:114; D:327–330 |
| A/Y operand packets | 1,772,871,740 × 20 | 35,457,434,800 | S:102; D:336–350 |
| A observer on/off snapshots | 2,648,968,517 × 4 | 10,595,874,068 | S:98; D:421–429 |
| Y observer on/off snapshots | 3,107,111,817 × 4 | 12,428,447,268 | S:100; D:421–429 |
| A inertness gate packet | 5,297,936,351 × 2 | 10,595,872,702 | S:81; D:432 |
| Y inertness gate packet | 6,214,223,907 × 2 | 12,428,447,814 | S:82; D:432 |
| **Native subtotal, both arms** | **162 packets** | **149,212,707,462** | **2 × measured A7 native family** |
| Update-pair + realized-weight column statistics | 882,845 × 1,360 | 1,200,669,200 | stat `controls_A7_coined_coined_L4_compare_assembled32_direct64__assembled32_factored64.pt`; D:586–591 |
| Common factors + factor repeat | 1,452,065 × 20 | 29,041,300 | stat `controls_A7_coined_coined_L4_common_factors.pt`; D:477–478,563–564 |
| Float64 factor solutions, promoted/assembled systems | 2,115,113 × 20 | 42,302,260 | stat `controls_A7_coined_coined_L4_assembled32_factor_solution64.pt`; D:467–468,472–473 |
| Numeric packet, including 12 nested column-statistic groups | 10,581,267 × 10 | 105,812,670 | stat `controls_A7_coined_coined_L4_numeric.pt`; D:596–603 |
| Device product observer off/on weights | 45,090,345 × 60 | 2,705,420,700 | stat `controls_A7_coined_coined_L4_common_observer_off.pt`; D:505–507,566–572 |
| Device product inputs | 46,344,161 × 30 | 1,390,324,830 | stat `controls_A7_coined_coined_L4_common_inputs.pt`; D:494,566–572 |
| Fp32 products and direct-repeat solution, seven per cell | 90,179,113 × 70 | 6,312,537,910 | stat `controls_A7_coined_coined_L4_cpu32_product.pt`; D:459,475–480,568–570 |
| Device coverage gate off/on weights persisted again | 90,179,365 × 30 | 2,705,380,950 | stat `controls_A7_coined_coined_L4_common_coverage.pt`; D:508,566–572 |
| Device products with left/right factors | 91,432,929 × 30 | 2,742,987,870 | stat `controls_A7_coined_coined_L4_common_product.pt`; D:502,566–572 |
| Dense float64 solutions/products, seven per cell | 180,356,649 × 70 | 12,624,965,430 | S:1; D:460,465–466,469–474 |
| Fp16 weights + float64 realized updates, all 16 candidates | 225,445,669 × 160 | 36,071,307,040 | S:7; D:578–584 |
| Promoted-before-assembly float64 system | 1,152,272,541 × 10 | 11,522,725,410 | S:25; D:461–464 |
| Complete control input packet | 1,773,928,825 × 10 | 17,739,288,250 | S:4; D:455,561–565 |
| Aggregate 16-update packet, all copies retained | 1,893,733,235 × 10 | 18,937,332,350 | S:129; D:573–576 |
| **Controls subtotal, all ten cells** | **1,890 packets** | **114,130,096,170** | **10 × complete-cell 189 / 11,413,009,617 B** |
| **All .pt writes** | **51 + 162 + 1,890 = 2,103 packets** | **271,939,207,019** | **Fixed + native + controls subtotals** |
| Projected JSON allowance, one budget block | 22,829,824 × 1 | 22,829,824 | `ceil(6,752,330 × 2,103 / 622)`; reconstructed baseline JSON stats |
| **Total projected incremental writes, before extra scratch** | | **271,962,036,843** | **.pt total + JSON allowance** |
| Reserve required by §3.3a | 21,474,836,480 × 1 | 21,474,836,480 | `20 × 2^30`; runbook:263 |
| **Pre-dispatch free-disk floor, before extra scratch** | | **293,436,873,323 B = 273.284384 GiB** | **Total writes + reserve** |

This ledger is recomputable without family means. The JSON allowance remains a **proportional estimate**, not a measured complete-run JSON total; additional storage receipts/codec metadata must be added. The current serializer writes directly into its exclusive final .pt file, then flushes/fsyncs and hashes it (`experiments/track_c/c10y_directdw_arms.py:1299–1304`; `D:44–60`); it schedules no second on-disk serialization copy. Actual peak allocated space, filesystem overhead, abnormal/partial-file allowances and any new compression/archive scratch are **UNMEASURED**. Bind `B_temp_peak` and any increase in metadata before admission: final floor is **293,436,873,323 + B_temp_peak + additional_metadata_bytes**, never a downward-rounded “273 GB.”

The metadata-only filesystem command actually run was `/opt/homebrew/bin/rtk proxy /opt/homebrew/bin/node -` with `fs.statfsSync(path,{bigint:true})`, multiplying `bsize × bavail`. Snapshot paths/results: `/Volumes/memit`, **4,096 B × 22,425,388 available blocks = 91,854,389,248 B**; `/Users/robertrhu`, **4,096 B × 51,480,668 blocks = 210,864,816,128 B**. These are snapshots, not dispatch receipts. Memit's snapshot is **201,582,484,075 B below even the base floor**. The operator's approximate 86/110 GiB report is superseded for this snapshot by statfs; internal SSD space changed after the operator's reclamation. The internal SSD remains excluded as an archive tier (`EXPERIMENT_RUNBOOK.md:262`). Retained old evidence is already consuming space and supplies no future-write credit.

### (c) Storage choices preserving frozen B1/B4

Every option retains the **full unique tensors**, their original dtypes/shapes/orientations and raw tensor identities before dependent gates; no hash-only replacement is proposed. Binding text: `docs/C10Y_PRECAST_DIAG_SCOPE.md:19–23,30–39,69–71`. Storage changes must preserve Journal's persist/flush/fsync-before-predicate ordering (`D:44–60`), exclusive publication, offending values and partial work on failure. The amounts below are **additional new-run occupancy** with the old run retained. The 20 GiB reserve is a separate free-space requirement.

Let `M = 22,829,824 B`, `T` be measured additional scratch/partial-file peak, `C` be the sum of measured losslessly compressed packet sizes, and `A` be additional archive/codec metadata above M. Neither compression ratio nor archive performance has been measured.

| Option | Bytes needed on memit at peak / admission floor | What changes | Still needs measurement / review |
|---|---|---|---|
| **Run as scoped on a larger hot volume** | Enlarged/replacement memit: **271,962,036,843 + T B** occupancy; **293,436,873,323 + T B** minimum free. If all fresh output is placed on a separate larger volume, new tensor occupancy on memit is zero and that volume needs the same floor. | Preserve current uncompressed writer and all duplicate packets. A different output volume/root must honor exclusive namespaces and source/input bindings; the current output root is fixed in D:123–133,758–760, so a symlink is not an admitted shortcut. | Confirm actual writable filesystem, remaining shapes/aliasing/metadata and allocated-space peak; any path/launcher change gets review and repinning. Time-cap sufficiency remains separately unverified. |
| **Lossless compression with byte-exact decode** | **C + M + A + T B** occupancy; add **21,474,836,480 B** reserve. C is **UNMEASURED**. At the operator's approximate 86 GiB, even with A=T=0, C must be at most **70,844,130,560 B** (about **26.052%** of uncompressed .pt bytes). | Change representation and reader/verification path; preserve every unique full payload, original dtype/raw tensor hash, codec/version and compressed-file identity. Decode must reproduce original tensor bytes exactly; no demotion or quantization. Retain committed payload/metadata before gates. | Measure every family’s compressed sizes, encode/decode time and concurrent input/output scratch. Prove byte-exact roundtrip, exclusive/fsynced writes, partial-failure retention and complete replay; Astra writer/reader review and full time/disk rebudget. No ratio is assumed to fit. |
| **Per-cell persist → hash → archive to gdrive → delete hot copy under §3.3a** | A conservative schedule retaining fixed records and the current arm's complete native prerequisites, archiving each finished control cell before the next and archiving that arm's native packets before the next arm peaks at **8,596,403,387 + 74,606,353,731 + 11,413,009,617 = 94,615,766,735 B** of .pt. With M: **94,638,596,559 + A + T B** occupancy; floor **116,113,433,039 + A + T B = 108.139061 GiB + extras**. **This simple schedule still exceeds present memit capacity.** | Persist/hash full local packets before their gates; complete dependent checks, verify a full immutable remote copy against the original file SHA, publish durable location/size/hash receipts, then delete only the archived hot copies. Preserve all science JSON/hashes in the durable records tier. A transfer failure retains local full packets and stops. Future reads restore or losslessly stream the exact archived payload. | `gdrive` OAuth is **not authorized** per operator. Requires retention disposition under runbook:260–262, review of in-run archival, dependency/replay and interrupted-transfer semantics, reader/path repinning, measured bandwidth/verification/hydration scratch and archive-inclusive cap. A more aggressive native-checkpoint archive/hydration schedule could lower peak, but its bound is **UNMEASURED / NOT REVIEWED**; the largest present writer packet alone is **6,214,223,907 B** (S:82). No archive or deletion is authorized here. |

The archive row's **108.139061 GiB** is a specific conservative schedule, not a universal lower bound: earlier archival of native checkpoints needs an explicit last-use/restore plan. The unchanged code retains all files and still needs the full-run floor. Do not replace that floor merely because the first cell or the named timing sample fits. The internal SSD is not an alternative archive tier, and §3.3a's approved deletion of this old INCONCLUSIVE run is not blanket permission to discard unique live-run evidence.

**Recommendation for Astra/operator decision:** use a larger authorized hot output volume with the existing full uncompressed persistence contract and at least **293,436,873,323 B additional free space**, plus the reviewed metadata/scratch additions. It has the directly sized representation and least evidence-contract change. Present memit does not admit the full run. If a larger volume is unavailable, develop and review a measured native-checkpoint-plus-cell gdrive schedule after OAuth; the simple per-cell schedule above does not fit, and compression remains an unmeasured alternative. This is a recommendation only; freeze, implementation, source repinning, time/disk admission and dispatch remain separate decisions.

### Reproducible metadata audit command (executed by Z4)

The following exact command produced the family totals, dtype-containing file counts, packet-size histograms and sample/manifest-line bindings above. It **never reads a .pt payload**. JSON checksum equality is equality of already recorded strings, not new tensor/file hashing.

```sh
/opt/homebrew/bin/rtk proxy /opt/homebrew/bin/node - <<'JS'
const fs=require('fs'),p=require('path'),assert=require('assert/strict');
const R='results/c10y_precast_diag/20261009T225619Z';
const text=n=>fs.readFileSync(p.join(R,n),'utf8');
const S=new Map(text('OPERANDS_MANIFEST_sizes.txt').trim().split('\n').map((s,i)=>{
  const m=s.match(/^(\d+) (.+\.pt)$/);assert(m);return[m[2],{bytes:+m[1],line:i+1}];}));
const H=new Map(text('OPERANDS_SHA256SUMS.txt').trim().split('\n').map(s=>{
  const m=s.match(/^([0-9a-f]{64})  (.+\.pt)$/);assert(m);return[m[2],m[1]];}));
assert.equal(S.size,131);assert.deepEqual([...S.keys()].sort(),[...H.keys()].sort());
const files=fs.readdirSync(R),live=new Map(files.filter(n=>n.endsWith('.pt')).map(n=>[n,fs.statSync(p.join(R,n)).size]));
const all=new Map([...S].map(([n,v])=>[n,v.bytes]));
for(const[n,b]of live){if(S.has(n))assert.equal(b,S.get(n).bytes);all.set(n,b);}
const refs=x=>x&&typeof x==='object'?(x.tensor_artifact?[x]:Object.values(x).flatMap(refs)):[];
const meta=new Map([...all].map(([n])=>{const j=JSON.parse(text(n.replace(/\.pt$/,'.json'))),r=refs(j);
  assert(r.length);assert(r.every(t=>t.tensor_artifact===n));if(H.has(n))assert.equal(j.artifacts[n],H.get(n));return[n,r];}));
const sum=rows=>[rows.length,rows.reduce((s,[n,b])=>s+b,0)];
const emit=(label,rows)=>console.log(JSON.stringify({label,count:rows.length,bytes:sum(rows)[1]}));
for(const[label,rows]of [['all',[...all]],['live',[...live]],['manifest',[...S].map(([n,v])=>[n,v.bytes])],
 ['retained_manifest',[...S].filter(([n])=>live.has(n)).map(([n,v])=>[n,v.bytes])],
 ['missing_manifest',[...S].filter(([n])=>!live.has(n)).map(([n,v])=>[n,v.bytes])]])emit(label,rows);
assert.deepEqual([...all].filter(([n,b])=>b>=100000000).map(([n])=>n).sort(),[...S.keys()].sort());
for(const[label,rows]of [['all',[...all]],['manifest',[...S].map(([n,v])=>[n,v.bytes])]]){
 const groups={};for(const[n,b]of rows)(groups[n.split('_')[0]]??=[]).push([n,b]);
 for(const[k,v]of Object.entries(groups).sort())emit(label+':'+k,v);
 emit(label+':contains_float64',rows.filter(([n])=>meta.get(n).some(t=>t.dtype==='torch.float64')));}
const fixed=[...all].filter(([n])=>/^(pristine_weights|projectors|target_|targets)/.test(n));
const native=[...all].filter(([n])=>!/^(pristine_weights|projectors|target_|targets|controls_|updates_)/.test(n));
const cells=l=>[...all].filter(([n])=>n.startsWith('controls_A7_coined_coined_L'+l+'_')||n==='updates_A7_coined_coined_L'+l+'.pt');
const l5=new Map(cells(5).map(([n,b])=>[n.replace('_L5','_L4'),b]));assert.equal(l5.size,cells(4).length);
for(const[n,b]of cells(4))assert.equal(l5.get(n),b);
for(const[label,rows]of [['fixed',fixed],['native_A7',native],['control_L4',cells(4)],['control_L5',cells(5)],['partial_L6',cells(6)]]){
 emit(label,rows);const groups={};for(const[n,b]of rows)(groups[b]??=[]).push(n);
 if(label!=='control_L5'&&label!=='partial_L6')for(const[b,names]of Object.entries(groups).sort((a,b)=>+a[0]-+b[0]))
  console.log(JSON.stringify({label,bytes_per_packet:+b,count:names.length,total:+b*names.length,sample:names[0],basis:S.has(names[0])?'OPERANDS_MANIFEST_sizes.txt:'+S.get(names[0]).line:'stat '+p.join(R,names[0])}));}
const jsonBytes=files.filter(n=>n.endsWith('.json')).reduce((s,n)=>s+fs.statSync(p.join(R,n)).size,0);
const baseline=jsonBytes-fs.statSync(p.join(R,'OFFLOADED_OPERANDS.json')).size-fs.statSync(p.join(R,'OFFLOAD_DELETED.json')).size;
console.log(JSON.stringify({json_files:files.filter(n=>n.endsWith('.json')).length,json_bytes:jsonBytes,baseline_json_bytes:baseline,
 full_packets:fixed.length+2*native.length+10*cells(4).length,
 full_pt_bytes:sum(fixed)[1]+2*sum(native)[1]+10*sum(cells(4))[1],metadata_allowance:Math.ceil(baseline*2103/all.size)}));
JS
```

### Completion / standby checkpoint

Metadata verification: all 32 bytes-per-packet products (30 .pt rows plus metadata and reserve), the 2,103-packet sum and the total/floor arithmetic recomputed correctly; manifest set/recorded-hash-string equality and every completed L4/L5 corresponding packet size passed. The original 119 lines remain unchanged; scoped diff whitespace check passed. This validates the metadata ledger, not numerical/runtime behavior or dispatch clearance. Context-save pointer checkpoint: `/private/tmp/c10y_disk_budget_z4.ifGC1c/gstack/projects/c10k-route-a/checkpoints/20261010-010529-codex-z4-disk-budget-done-standby.md` (temporary; this report remains the durable home).

Done: one appended Disk budget (Z4) section, exact incident/family reconciliation, full recomputable write ledger and conditional storage recommendation. In flight: no measurements, transfers, science reading or dispatch. Paths: this amendment draft; frozen scope `docs/C10Y_PRECAST_DIAG_SCOPE.md`; evidence R and its two operand manifests; successor procedure `results/c10z_astra_attempt4_prep/handoff_codexz3_20261010.md:88–107`. Next: Astra/operator review of the resource/storage proposal. **Task 2 remains standby until MAESTRO2 asks**; then follow Z3 §3 steps 1–7 and write `results/c10z_astra_attempt4/outcome_reading_z4.md`. A permission judgment never launches process 2.

Open risks: projected A1/remaining-cell sizes and metadata; unmeasured allocated/scratch peak, encode/decode/archive costs and time-cap sufficiency; gdrive authorization pending; future Task-2 native worker exit/exclusivity/disk evidence must be obtained independently. Old unique payloads outside the retained sample are unavailable by operator disposition; their recorded sizes/hashes are metadata evidence only.

**BINDING context directive (operator, AGENTS.md): watch `Context N% left`; before approximately 20% remains, stop new work, write done/in-flight work, exact paths, next step and open risks into the task report, tell MAESTRO2 and ask for a fresh successor. Never approach full-window compaction. Every handoff restates this rule; apply it to every team session orchestrated.**

## Disk budget fix round 1 (Y4)

**Resource-only response to GPT-6-Astra FIX-FIRST; D-C10y-precast-budget remains DRAFT / NOT FROZEN / NOT APPLIED / NO RUN AUTHORIZATION.** Review read in full: `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/astra_z4budget_out.md`, especially required fixes at lines 48–52. Z4's preceding text is preserved. This append qualifies its recommendation and supplies the missing reference and last-use schedules; it does not implement them.

Notation: `D = experiments/track_c/c10y_precast_diag.py`; `R = results/c10y_precast_diag/20261009T225619Z/`; `S = R/OPERANDS_MANIFEST_sizes.txt`; `scope = docs/C10Y_PRECAST_DIAG_SCOPE.md`. Bytes are logical serialized file bytes, including serializer overhead. Commands C1/C2 below were executed by Y4 using only text/source/JSON reads and stat/statfs. Manifest-only sizes describe previously recorded files, not verified remote payloads. A7 native and completed L4/L5 cells are observed; A1 native/controls and unwritten cells remain **UNVERIFIED projections**. No additional native-copy deduplication receives credit.

### 1. References preserve the observations and remove four duplicate families

B1/B4 require full actual inputs and durable computed gate inputs (`scope:19–23,30–39,69–71`), not another serialization of the same retained value. The proposed reference records must be exclusive and fsynced before their predicate, resolve immutable full payloads by record/file/member identity with dtype/shape/orientation and tensor-byte identity, and verify/decode those payloads before evaluation. The existing ordering is `D:44–60`; the current reader at `D:89–106` supports local sidecars only. Reference/archive resolution therefore requires implementation review and source repinning; these are conditional savings, not measured rewritten output.

| Duplicate family removed | Full-run bytes removed | Writer and size evidence | What the revised reader/predicate resolves instead |
|---|---:|---|---|
| Native inertness input sidecars containing already-saved observer snapshots | `2 × (5,297,936,351 + 6,214,223,907) = 23,024,320,516` | Snapshots `D:427–431`; duplicate gate `D:432` through `D:56–60`; `S:81–82`. Two arms, both paths (`D:15–16,417,664–667`). | For each arm/path, retain separate `observer_<arm>_<path>_off.json/.pt` and `..._on.json/.pt`. The inertness input JSON references both; `exact(off,on)` at `D:432` receives their verified decoded observations. Keep the coverage and outcome records. |
| Device coverage input sidecars containing already-saved off/on weights | `90,179,365 × 3 × 10 = 2,705,380,950` | Actual off/on writes `D:505–507`; duplicate gate `D:508`; native/common/repeat calls `D:566,571–572`. C1 stat: `controls_A7_coined_coined_L4_common_coverage.pt` = 90,179,365 B. | Preserve each call's two actual `<prefix>_observer_off` and `..._observer_on` packets, plus scalar `n`. Resolve those two weight members for `n == 1 and exact(off,on)` at `D:508`. The full original off/on packets, 45,090,345 B each by C1 stat, remain budgeted. |
| Aggregate 16-update sidecars containing previously saved pre-cast updates | `1,893,733,235 × 10 = 18,937,332,350` | Individual writes `D:457–480,502,568–570`; assembly `D:565–575`; duplicate aggregate `D:576`; `S:129`. | Keep the aggregate's logical 16-name dictionary as durable member references to the native operands and individual products below. Its finiteness predicate (`D:64–72`) resolves the same full pre-cast values; realization, pair statistics and repeat checks continue to consume them (`D:578–607`). |
| Complete control-input sidecars duplicating recipe-A operands plus the already-saved common X | `1,773,928,825 × 10 = 17,739,288,250` | `D:455,558–565`; `S:4`. C1 stat: existing common-factor packet = 1,452,065 B, already counted and retained. | Resolve `operands_<arm>_L<l>_A.json/.pt` for all original fields, with X supplied by `controls_<arm>_L<l>_common_factors.json/.pt:X` saved at `D:563–564`. This is the **matched recipe-A X** installed at `D:565`, not the native X initially placed in the transient dictionary at `D:561`. Finiteness and controls `D:453–480` see the same complete dictionary. |

For the aggregate update references, let `p = controls_<arm>_L<l>`. Every target below remains a full packet; member notation names the decoded dictionary value.

| Aggregate member(s) | Full retained source member | D lines |
|---|---|---|
| `recipe_A`, `native_direct` | `operands_<arm>_L<l>_A:update`, `operands_<arm>_L<l>_Y:update` | 336–350,558–565 |
| `native_device`, `common_device`, `device_repeat` | `p_native_product:update`, `p_common_product:update`, `p_repeat_product:update` | 502,566,571–574 |
| `native_cpu32_product`, `native_cpu32_product_repeat` | Their corresponding `p_<name>:update` packets | 568–570,573 |
| `cpu32_product`, `promoted32_product`, `solve64_direct`, `solve64_factored`, `assembled32_direct64`, `assembled32_factored64`, `direct32_repeat`, `factor32_repeat_product`, `cpu32_product_repeat` | Each corresponding `p_<name>:update` packet, all nine retained separately | 457–480,575 |

**Observer-on and observer-off remain two separately recorded observations.** Neither native nor device observations may be merged on the assumption that inertness will pass (`scope:23`; `D:421–432,505–508`). The removed gate files contain extra copies; the actual on/off payloads are not removed from the evidence set.

**Realizations cannot replace pre-cast updates.** Cast/add is information-losing: distinct fp32/fp64 updates can produce the same fp16 result. Measurement 5 independently requires both realized weights and the CPU-promoted difference `W_post − W0` (`scope:38`; `D:578–584`). Keep all 16 realized packets per cell: `225,445,669 × 16 × 10 = 36,071,307,040 B` (`S:7–22`; `D:578–584`), as well as the full pre-cast sources used by measurements 1–4 and 6. No realized-packet savings are credited.

Recomputed conditional accumulation floors, preserving the existing estimated JSON allowance and reserve:

```text
M = ceil(6,752,330 × 2,103 / 622) = 22,829,824 B       [C1]
reserve = 20 × 2^30 = 21,474,836,480 B                [runbook:263]
unchanged writer = 271,939,207,019 + M + reserve
                 = 293,436,873,323 B                [C1; D writers above]

first-three savings = 23,024,320,516 + 2,705,380,950 + 18,937,332,350
                    = 44,667,033,816 B
first-three floor = 293,436,873,323 − 44,667,033,816
                  = 248,769,839,507 B

all-four savings = 44,667,033,816 + 17,739,288,250
                 = 62,406,322,066 B
all-four .pt writes = 271,939,207,019 − 62,406,322,066
                    = 209,532,884,953 B
all-four floor = 248,769,839,507 − 17,739,288,250
               = 231,030,551,257 B
```

Both reference floors require **additional reference/archive metadata, allocated-space overhead and scratch**. M is the old proportional estimate, not a measurement of the new writer; no metadata reduction is assumed. References alone do not make present memit fit.

### 2. Last-use archival schedule and recomputable peaks

The candidate below applies all four reference changes. It retains the fixed records and **all remaining native prerequisites of the current arm**; it archives each path's two snapshots after its inertness gate, each completed control cell before the next cell, and the arm's remaining native prerequisites before the next arm. Keeping all native prerequisites until the arm boundary avoids claiming unchecked finer-grained savings. A7 and A1 execute serially (`D:664–670`), so their hot tensor occupancy is not added together.

First, the tensor blocks used by every schedule row:

| Fixed block F | Bytes × count | Subtotal | Byte source; writer / last local payload reader |
|---|---:|---:|---|
| Pristine weights | 6,172,004,127 × 1 | 6,172,004,127 | `S:112`; `D:644–646`, finite-gate read `D:56–60`. In-memory pristine still serves restoration `D:183–198,647`. |
| Projector set | 2,423,523,673 × 1 | 2,423,523,673 | `S:113`; writer `D:657`, explicit disk read `D:658`; in-memory P is passed to both arms at `D:667`. |
| Individual targets, both arms | 9,769 × 48 | 468,912 | C1 stat representative `target_A1_single_00.pt` and exact fixed-set sum; writer/own finite-gate read `D:611–618,56–60`; 24 requests per arm `D:662`. |
| Aggregate targets | 406,675 × 1 | 406,675 | C1 stat `targets.pt`; writer `D:619`, explicit last disk read `D:620`; in-memory override installed `D:663`. |
| **F, held through terminal publication** | **51 packets** | **8,596,403,387** | **Sum of these four rows; C1 exact inventory.** |

| Native prerequisite family, one arm | Per-layer bytes in A / Y | Five-layer A subtotal | Five-layer Y subtotal | Byte source; D writer |
|---|---:|---:|---:|---|
| Three tokenized batch slots | 46,821 + 7,141 + 5,989 = 59,951 / 59,951 | 299,755 | 299,755 | C1 stats `batch_A7_coined_coined_L4_A_{0,1,2}.pt`; `D:377–384` |
| Q intermediate packets | 486,819,809 / 2 × 486,819,809 | 2,434,099,045 | 4,868,198,090 | `S:83–85`; `D:285–300` |
| Direct solve inputs | 1,682,693,951 / 1,682,693,951 | 8,413,469,755 | 8,413,469,755 | `S:114–115`; `D:327–330` |
| Y factor solve inputs | 0 / 1,456,425,493 | 0 | 7,282,127,465 | `S:116`; `D:303–305` |
| Full native operand/update packets | 1,772,871,740 / 1,772,871,740 | 8,864,358,700 | 8,864,358,700 | `S:102–103`; `D:336–350` |
| Y native factors | 0 / 488,270,357 | 0 | 2,441,351,785 | `S:76`; `D:360–369` |
| **N_A / N_Y** | | **19,712,227,255 (30 packets)** | **31,869,805,550 (45 packets)** | **Sum of the columns; C1 reconstructs both exact sets.** |

Native Q/solve inputs have their persistence/inertness reads at `D:224–247,263–270,350–355,360–371`; later checks use copied/live values, not another disk load. Batches are explicitly read for native comparison at `D:443–445`. Both native operand packets and Y factors are read there (`D:436–442`) and again for their control cell (`D:558–560`); their in-memory values supply residual/conditioning/repeat/realization checks through `D:592–607`. Retain all these packets until that arm's last cell is durably complete, even where an individual packet's local last use is earlier.

```text
A snapshots = 2 × 2,648,968,517 = 5,297,937,034 B       [S:98–99; D:429]
Y snapshots = 2 × 3,107,111,817 = 6,214,223,634 B       [S:100–101; D:429]
N = N_A + N_Y = 51,582,032,805 B

C = one unchanged complete control cell
    − its three duplicate coverage sidecars
    − its aggregate update sidecar
    − its complete control-input sidecar
  = 11,413,009,617 − 3 × 90,179,365 − 1,893,733,235 − 1,773,928,825
  = 7,474,809,462 B; 189 − 3 − 1 − 1 = 184 retained .pt packets
  [C1 L4/L5 exact complete-cell sums; S:4,129; D:455–480,490–508,555–605]
```

C retains the individual pre-cast updates, common/repeat factors, device inputs/products and both observations, float64 systems/solutions, all 16 realizations, all 136 pair/weight statistics packets, and the numeric packet. Its last disk reads are its own persist-before-finiteness reads (`D:56–72`) and factor-repeat reload (`D:604`); subsequent calculations and repeat/weight predicates finish at `D:605–607`. A revised writer must durably publish the returned cell summary and its numeric/reference bindings **before archival**; today `D:670` appends that summary only in memory and the aggregate science summary is written later at `D:671–672`. That extra completion receipt is a required implementation change and an unmeasured metadata/time cost.

The following occupancy rows run **once for each arm**, after the previous arm's native packets and completed cells have left memit. “Archive” always means full immutable remote copy, verified durability/identity and fsynced location/size/hash receipt before deleting the hot copy; it never means discarding the evidence.

| Stage / written tensors | Last reader or predicate / chosen archive boundary | Peak local .pt bytes at this row | After successful archive/delete |
|---|---|---:|---:|
| Fixed F, written once for the whole run | Local reads listed above; keep F through restoration and terminal publication (`D:647,673–676,684–708`). Archive after the terminal records, before the next dispatch. No early fixed-record savings credited. | **F = 8,596,403,387** | F remains during both arms |
| A observer-on: N_A plus its actual on snapshot | Coverage `D:431,402–406`; snapshot is still needed by inertness `D:432`. Keep it while observer-off executes. | F + N_A + 2,648,968,517 = **30,957,599,159** | No archival yet |
| A observer-off: its distinct off snapshot | Both decoded snapshots are compared at `D:432` through `D:57–60`. | F + N_A + 5,297,937,034 = **33,606,567,676** | No archival before gate outcome |
| A inertness gate: reference JSON and outcome, no duplicate .pt | After persisted outcome `D:60,432`, archive both A snapshots. Native comparison has no later snapshot reads (`D:434–448`). Keep their science JSON/references/outcome. | **33,606,567,676** | F + N_A = **28,308,630,642** |
| Y observer-on: N_Y plus its actual on snapshot | Coverage `D:431,402–406`; Y snapshot still needed at `D:432`. | F + N_A + N_Y + 3,107,111,817 = **63,285,548,009** | No archival yet |
| Y observer-off: its distinct off snapshot | Y inertness predicate `D:432`, decoding and outcome `D:57–60`. | F + N_A + N_Y + 6,214,223,634 = **66,392,659,826** | No archival before gate outcome |
| Y inertness gate: reference JSON and outcome, no duplicate .pt | After persisted outcome, archive both Y snapshots; no snapshot reads at `D:434–448`. | **66,392,659,826** | F + N = **60,178,436,192** |
| Native comparison: science JSON only | Read operands/factors/batches at `D:436–445`; publish native comparison `D:448`. Retain all N through the arm's controls. | F + N = **60,178,436,192** | Same |
| L4 control cell: 184 packets C plus reference/completion JSON | Finish `D:603–607`, commit cell summary; archive the entire completed cell before L5 (`D:669–670`). | F + N + C = **67,653,245,654** | F + N = **60,178,436,192** |
| L5 control cell: same retained family C | Same last readers; durable completion and verified archive before L6. | F + N + C = **67,653,245,654** | F + N = **60,178,436,192** |
| L6 control cell: projected C | Same last readers; durable completion and verified archive before L7. | F + N + C = **67,653,245,654** | F + N = **60,178,436,192** |
| L7 control cell: projected C | Same last readers; durable completion and verified archive before L8. | F + N + C = **67,653,245,654** | F + N = **60,178,436,192** |
| L8 control cell: projected C | Same last readers; durable completion and verified archive before the arm boundary. | F + N + C = **67,653,245,654** | F + N = **60,178,436,192** |
| A7 arm boundary: no new tensors | After all five returned summaries are committed, archive all remaining N_A/N_Y. No later A7 tensor read in the A1 loop (`D:664–670`). | F + N = **60,178,436,192** | F = **8,596,403,387**, then start A1 at the A-on row |
| A1 arm boundary: no new tensors | After all five A1 summaries are committed, archive all remaining N. Finalization consumes science JSON/booleans (`D:671–708`), not native packets. | F + N = **60,178,436,192** | F = **8,596,403,387** |
| Cleanup/terminal, then fixed-record archive | In-memory pristine restoration ends at `D:183–198,647,675`; worker/finalizer records `D:676,689–708`. Verify and archive F after terminal publication. | F = **8,596,403,387** | **0** new-run .pt bytes; retain science records and remote full payloads |

Reproduction of Astra's successful-schedule peaks:

```text
native peak = F + N_A + N_Y + 2 × 3,107,111,817
            = 66,392,659,826 B

controls peak = F + N_A + N_Y + C
              = 67,653,245,654 B

floor before new overhead = max(native peak, controls peak) + M + reserve
                          = 67,653,245,654 + 22,829,824 + 21,474,836,480
                          = 89,150,911,958 B

total full .pt bytes to archive across the schedule
 = F + 2 × (N_A + N_Y + A snapshots + Y snapshots) + 10 × C
 = 8,596,403,387 + 2 × (19,712,227,255 + 31,869,805,550
                       + 5,297,937,034 + 6,214,223,634)
   + 10 × 7,474,809,462
 = 209,532,884,953 B
archive packet count = 51 + 2 × (30 + 45 + 4) + 10 × 184 = 2,049
```

**The peaks are derived logical-byte occupancy for the successful schedule, not empirical allocated-space or failure/replay bounds.** Peak admission would require explicit acceptance of revised accounting: the present policy at `EXPERIMENT_RUNBOOK.md:263` says **projected writes + 20 GiB**, which for all four references alone is still 231,030,551,257 B. The existing frozen writer archives nothing. Neither this table nor an early last-use inference overrides that policy or grants deletion/Drive authorization (`runbook:260–264`).

### 3. Unmeasured overhead, failure/replay contract and recommendation

The following remain **UNMEASURED / UNVERIFIED**; no runtime receipt or time allowance is asserted:

- **Transfer time and bandwidth:** the schedule transfers 209,532,884,953 B of .pt payloads plus metadata; the four snapshot barriers, ten cell barriers and two arm barriers are on the proposed in-run critical path. Fixed-record archival is post-terminal in this schedule and separately gates the next dispatch. Measure each cohort's copy time and effective bandwidth; no transfer overlap or bandwidth floor is assumed.
- **Scratch and allocated-space overhead:** remote verification/hydration, partial downloads/uploads, buffers, filesystem allocation overhead, partial/error packet publication and new reference/archive/completion JSON are not measured. The normal peak assumes no second full local copy and no prior arm/cell still present when the next starts. An extra pristine-sized copy is 6,172,004,127 B (`S:112`), larger than the current spare overhead budget below; verification cannot silently assume such a staging copy fits.
- **Remote durability verification:** neither gdrive authentication nor immutable remote object publication, size/hash verification, completed-transfer durability or restore receipts have been demonstrated. Current inspection only uses manifest sizes and recorded metadata, not rehashed or decoded payloads. Approval must bind the verification mechanism and its transfer/scratch cost.
- **Failure and replay:** implement and review reference resolution and append-only remote-location receipts, preserving original names, sizes, file/member identities and all full payloads. A failed/partial/unverified transfer retains the local committed packet, publishes an explicit failure and stops before the next tensor cohort; a gate failure retains its offending values. Timeout/interruption must preserve completed receipts and partial evidence (`scope:71`; `D:74–87,678–681,699–724,727–742`). No deleted local packet may be required by a subsequent local-only read. Replay must resolve archived dependencies, restore/stream byte-exact payloads with bounded scratch, and retain B1/B4 persist-before-gate ordering and exclusive-write refusal (`D:44–60,89–108`). Interrupted-transfer, forced-halt, replay and overwrite-refusal behavior remains unrun and requires separately authorized qualification; this append performs no tests and authorizes no resume.
- **Time added to the cap:** for each critical-path archival cohort, measure `T_copy + T_verify + T_receipt + T_delete`, plus reference verification/decoding and any bounded failure/hydration cost. Let their incremental total above the already timed phase work be `Delta_storage`; it is **unknown, not zero**. The provisional rebudget is `T_cap = 60 × ceil(1.15 × (7082.624368 + Delta_storage) / 60)` (`draft:47–53`). The draft's 8,160 s does not include a measured new archival allowance. If new whole-phase measurements already include archival, use them without double-counting. Report post-terminal fixed-archive time separately and block the next dispatch until it finishes. Bind transfer/verification timeouts before freeze; no in-run cap increase follows.

**Fresh memit statfs (C2), 2026-10-10T01:39:45.420Z:** `/Volumes/memit`, **4,096 B × 22,415,054 available blocks = 91,812,061,184 B available**. Against the candidate base floor **89,150,911,958 B**, current headroom is **2,661,149,226 B** for all additional metadata/scratch/allocation allowances. Admission requires `additional_overhead_peak <= 2,661,149,226 B` at this snapshot, plus a new statfs receipt when dispatch is actually considered. Existing evidence and ASTRA's concurrent occupancy are already reflected in available space; no reclamation credit is assumed.

**Requalified recommendation:** **larger volume** is the unchanged-writer option, needing **293,436,873,323 B** additional free space plus its reviewed overhead. **References + last-use archival** is the evidence-preserving candidate that **may fit present memit**, with the derived **89,150,911,958 B** floor and the snapshot headroom above. It is not a validated or authorized dispatch option. **Dispatch remains BLOCKED pending writer/reader implementation review and source repinning, measured storage/failure/replay overhead and the archive-inclusive time budget, gdrive authorization and remote-durability verification, explicit acceptance of peak accounting under §3.3a, and fresh disk admission.** No larger volume is proven unavoidable after these changes; no current option admits a run.

### Executed metadata/stat-only commands

C1 reconstructs recorded sizes from S plus live stat metadata, prints fixed/native/control blocks and retained packet sizes, and recomputes the reference floors, schedule rows and total. It never reads a .pt payload. Its relevant results are reproduced in the tables/equations above; the reconstructed inventory is **622 packets / 117,364,108,482 B**, complete native A7 is **81 / 74,606,353,731 B**, and completed L4/L5 are **189 / 11,413,009,617 B each**. These are old-run metadata observations, not remote verification.

```sh
/opt/homebrew/bin/rtk proxy env -u NO_COLOR /opt/homebrew/bin/node - <<'JS'
const fs=require('fs'),p=require('path');
const R='results/c10y_precast_diag/20261009T225619Z';
const inv=new Map(fs.readFileSync(p.join(R,'OPERANDS_MANIFEST_sizes.txt'),'utf8').trim().split('\n').map(line=>{const m=line.match(/^(\d+) (.+\.pt)$/);if(!m)throw Error('Malformed size manifest');return[m[2],BigInt(m[1])];}));
const files=fs.readdirSync(R);
for(const n of files.filter(n=>n.endsWith('.pt'))){const b=fs.statSync(p.join(R,n),{bigint:true}).size;if(inv.has(n)&&inv.get(n)!==b)throw Error('Size mismatch: '+n);inv.set(n,b);}
const sum=rows=>rows.reduce((s,[n,b])=>s+b,0n);
const rows=test=>[...inv].filter(([n])=>test(n));
const fixed=rows(n=>/^(pristine_weights|projectors|target_|targets)/.test(n));
const native=rows(n=>!/^(pristine_weights|projectors|target_|targets|controls_|updates_)/.test(n));
const na=rows(n=>/^(batch|intermediate|solve_inputs|operands)_A7_coined_coined_.*_A(?:_|\.)/.test(n));
const ny=rows(n=>/^(batch|intermediate|solve_inputs|operands|factors)_A7_coined_coined_.*_Y(?:_|\.)/.test(n));
const cell=l=>rows(n=>n.startsWith('controls_A7_coined_coined_L'+l+'_')||n==='updates_A7_coined_coined_L'+l+'.pt');
const coverage=sum(cell(4).filter(([n])=>n.endsWith('_coverage.pt')));
const aggregate=inv.get('updates_A7_coined_coined_L4.pt'),inputs=inv.get('controls_A7_coined_coined_L4_control_inputs.pt');
const gate=sum(rows(n=>n.startsWith('inertness_A7_coined_coined_')));
const snapshots=path=>sum(rows(n=>n.startsWith('observer_A7_coined_coined_'+path+'_')));
const F=sum(fixed),A=sum(na),Y=sum(ny),C=sum(cell(4))-coverage-aggregate-inputs;
const baseline=files.filter(n=>n.endsWith('.json')&&!['OFFLOADED_OPERANDS.json','OFFLOAD_DELETED.json'].includes(n)).reduce((s,n)=>s+fs.statSync(p.join(R,n),{bigint:true}).size,0n);
const count=fixed.length+2*native.length+10*cell(4).length;
const M=(baseline*BigInt(count)+BigInt(inv.size)-1n)/BigInt(inv.size),reserve=20n*2n**30n;
const original=F+2n*sum(native)+10n*sum(cell(4));
const removed=[2n*gate,10n*coverage,10n*aggregate,10n*inputs];
const stages={fixed:F,A_on:F+A+snapshots('A')/2n,A_off:F+A+snapshots('A'),A_archived:F+A,Y_on:F+A+Y+snapshots('Y')/2n,Y_off:F+A+Y+snapshots('Y'),Y_archived:F+A+Y,control:F+A+Y+C,cell_archived:F+A+Y,arm_archived:F};
const emit=x=>console.log(JSON.stringify(x,(_,v)=>typeof v==='bigint'?v.toString():v));
for(const [name,v] of [['fixed',fixed],['native_A_core',na],['native_Y_core',ny],['native_all',native],['control_L4',cell(4)],['control_L5',cell(5)]])emit({name,count:v.length,bytes:sum(v)});
for(const n of ['target_A1_single_00.pt','targets.pt','batch_A7_coined_coined_L4_A_0.pt','batch_A7_coined_coined_L4_A_1.pt','batch_A7_coined_coined_L4_A_2.pt','controls_A7_coined_coined_L4_common_coverage.pt','controls_A7_coined_coined_L4_common_observer_off.pt','controls_A7_coined_coined_L4_common_factors.pt'])emit({stat:n,bytes:fs.statSync(p.join(R,n),{bigint:true}).size});
emit({inventory_count:inv.size,inventory_bytes:sum([...inv]),full_count:count,original,baseline_JSON:baseline,M,reserve,removed,F,A,Y,C,stages,reference_floor_3:original+M+reserve-removed.slice(0,3).reduce((s,b)=>s+b,0n),reference_floor_4:original+M+reserve-removed.reduce((s,b)=>s+b,0n),archive_PT_total:F+2n*(A+Y+snapshots('A')+snapshots('Y'))+10n*C,archive_floor:stages.control+M+reserve});
JS
```

C2 is the freshly executed filesystem query used for the headroom above:

```sh
/opt/homebrew/bin/rtk proxy env -u NO_COLOR /opt/homebrew/bin/node - <<'JS'
const fs=require('fs');
const s=fs.statfsSync('/Volumes/memit',{bigint:true});
const free=s.bsize*s.bavail;
console.log(JSON.stringify({utc:new Date().toISOString(),path:'/Volumes/memit',bsize:s.bsize,bavail:s.bavail,free_bytes:free,candidate_floor:89150911958n,headroom:free-89150911958n},(_,v)=>typeof v==='bigint'?v.toString():v));
JS
```

### Completion / MAESTRO2 handoff

Done: one append to `results/c10y_precast_diag/amendment_budget_draft.md`, answering all three required fixes with four byte-bound reference families, explicit readers, per-stage archival/peak arithmetic and fresh statfs headroom. In flight: no measurements, transfers, tests, science reading or dispatch. Exact source/report paths: this amendment draft; `docs/C10Y_PRECAST_DIAG_SCOPE.md`; `experiments/track_c/c10y_precast_diag.py`; `results/c10y_precast_diag/20261009T225619Z/OPERANDS_MANIFEST_sizes.txt`; review `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/astra_z4budget_out.md`. Next: MAESTRO2 routes this appended fix round to GPT-6-Astra; implementation and qualification remain separate work. Open risks: all unmeasured overhead/failure/replay items above, A1/remaining-cell size projection, policy acceptance and Drive authorization. Verification boundary: text/metadata arithmetic only; no .pt load/hash/decode, Python, control timer, model/GPU work, code change, launch, deletion or commit. Text verification: the original 280 draft lines and protected scope/writer/manifest/review text are unchanged.

**BINDING context directive (operator, AGENTS.md): watch `Context N% left`; before approximately 20% remains, stop starting new work, write done/in-flight work, exact paths, next step and open risks into the task report, tell MAESTRO2 and ask for a fresh successor. Never approach full-window compaction. Every handoff restates this rule; apply it to every team session orchestrated.**

## Controls timing measurement (MAESTRO2, 2026-10-10 ~01:55Z)

`measure_controls.py --threads 8` ran once on CPU after ASTRA attempt 4 exited (no CPU contention), on the retained `controls_A7_coined_coined_L4_control_inputs.pt`; output `results/c10y_precast_diag/controls_timing_A7_L4_20261010T014510Z.jsonl` (exit 0). Numerical core for one A7-L4 cell: (b) 0.010 s, (c) 7.582 s, (d) 3.647 s, (e-CPU) 2.718 s, total **13.957 s**; process peak RSS **8.68 GiB**; (e) MPS repeat NOT_MEASURED_CPU_ONLY. Against the ~450 s observed per completed cell publication (Z3 §Time budget), the solve/product kernels are ≈3% of a cell: the remaining time is serialization + fsync + hashing of ≈11.4 GB per cell and per-column statistics (the original timeout traceback was in NumPy per-column quantiles). Implication for this amendment: the reference proposals (Y4 §1) reduce time as well as bytes, and `C_ctrl` should be re-estimated from write/hash/statistics throughput, not kernel time. One sample, single machine; not a whole-cell `C_ctrl` measurement.
