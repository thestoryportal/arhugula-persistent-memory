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
