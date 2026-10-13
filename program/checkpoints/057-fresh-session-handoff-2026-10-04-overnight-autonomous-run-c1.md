## FRESH SESSION HANDOFF - 2026-10-04 (overnight autonomous run; C10K Stage 0 HALTED on the M3 Pro — operator fork)

**Start here after context reset.** Hardware is the operator's MacBook M3 Pro 48 GB (D-HW-1); the pod is gone. The science path is re-validated here: P-8 device-neutral engine (fingerprint `d941a9fb…`), band [4-8] caches regenerated, LAW#3 (C2 vs CORPUS/20, A1 vs CORPUS/14) and LAW#5 gates PASS, B3 deployment spine PASS on the prebuilt llama.cpp (`results/law3_repro_2026-10-03/`). L9-12 caches were computing at handoff.

**C10K Stage 0 = HALTED - HARDWARE_ENVELOPE ⟨D-C10k-m3pro-stage0@43899c7f⟩ (CORPUS/41; `docs/C10K_M3PRO_STAGE0_DIAGNOSTIC.md`).** Unmodified official AnyEdit cannot execute on the MPS build (first failure `memit_ARE/compute_z.py:35`); the official runner is incomplete and holds the projector; the README environment cannot load the shipped Qwen2.5 configs; only Instruct configs ship. **The next step is an operator decision, not a run:** Route A (pre-register a declared device-port deviation; anchors: static identity + differential vs the vendored engine, each with declared deviations; 7B-Instruct probably does not fit at upstream's fp32 default), Route B (prereg hardware-scope amendment, then rented CUDA; still Instruct/launcher/reconstructed-stack deviations), or Route C (accept-bounded; not an F1 closure). Pre-decision read DONE (`docs/C10K_MEMIT_ARE_REDUCTION_NOTE.md`): `memit_ARE` does **not** reduce to MEMIT (extra `K_p` preservation term in the solve; last-token keying; no KL), so Route A has no local inertness anchor — it is a mechanism lead only; Route B remains the only faithful execution and answers a neighbouring estimator's question.

**Toolchain:** Command Line Tools are broken on this machine (ld rejects the SDK stubs) — no native builds; llama.cpp = official prebuilt `b11382`; LARQL blocked until reinstalled.

**Stop rule honored:** no C10 A1/A2/A7 run.


