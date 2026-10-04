# 41 — C10K Stage 0 on the M3 Pro: HALTED - HARDWARE_ENVELOPE (+ UPSTREAM_ENV_UNDEFINED)

_Diagnostic 2026-10-04. Decision-ID D-C10k-m3pro-stage0 ⟨D-C10k-m3pro-stage0@2e04a432⟩. Pre-registered in `docs/C10K_ANYEDIT_OFFICIAL_UPSTREAM_PREREG.md` (Stage 0; hardware scope superseded by D-HW-1). Full detail: `docs/C10K_M3PRO_STAGE0_DIAGNOSTIC.md`. Artifacts: `logs/c10k_stage0_desk_check.log`, `logs/c10k_stage0_cuda_classification.json`, `logs/c10k_stage0_first_failure_trace.log`, `logs/c10k_stage0_mps_svd_check.log`, `architecture_profile/c10k_m3pro_stage0_halt_diagnostic.json`, advisor reviews `logs/claude_c10k_m3pro_stage0_review{,_v2,_v3}.md`._

## Claim class
**Hardware/source-faithfulness diagnostic — NOT a method verdict on AnyEdit and NOT C10 evidence.** No science model was loaded; no C10 A1/A2/A7 ran (stop rule honored).

## VERDICT — HALTED - HARDWARE_ENVELOPE, with a secondary code UPSTREAM_ENV_UNDEFINED

| Finding | Value | Artifact |
|---|---|---|
| First live failure of unmodified upstream `memit_ARE` on this machine (tiny random Qwen2 on CPU, stock item, shipped hparams) | `memit_ARE/compute_z.py:35` `.to("cuda")` → `AssertionError: Torch not compiled with CUDA enabled` | first-failure trace log |
| Hard device bindings on the on-path files | 27 (17 in algorithm modules incl. `util/layer_stats.py`; 10 in the runner) | cuda classification json |
| Official runner complete? | **No** — `experiments/evaluate_uns.py:29` imports `glue_eval`, which does not ship; and the AlphaEdit null-space projector (`get_project`, SVD) lives in the runner (lines 262–275), not in `AlphaEdit_ARE/` | desk-check log |
| README environment | `transformers==4.23.1`, `pytorch==1.12.1`, "One A100 80G GPU"; no lockfile. **4.23.1 cannot load the shipped Qwen2.5 configs** (Qwen2 module: absent 4.36.2, present 4.37.0) → the "upstream-compatible environment" is undefined by upstream on any hardware | desk-check log |
| Shipped configs | `Qwen2.5-7B-Instruct`, `Llama3-8B-Instruct` only — **Instruct**, no 3B; the program's line is base Qwen2.5-3B/7B (new finding; the prereg never mentions Instruct) | desk-check log |
| Upstream default load | fp32 `.cuda()` (`evaluate_uns.py:86`): 7B ≈ 28.3 GB weights + 5 × 1.34 GB fp32 18944² projectors ≈ 35 GB before activations, vs MPS recommended ceiling 37.4 GB here → fitting would need dtype/offload "local tricks" the prereg forbids for PASS (I-INFER; not load-tested) | mps svd check log |

## What this does and does not change
- C10 remains **OPEN/BLOCKING** (unchanged). C10K Stage 0 cannot pass on the M3 Pro as pre-registered.
- Forward routes are the operator's call: **A** declared device-port deviation (shim or anchored patch; two possible anchors, each with caveats), **B** prereg scope amendment then rented CUDA (still Instruct-model + launcher + reconstructed-stack deviations), **C** accept-bounded (not an F1 closure).
- Advisor (3 rounds): halt holds; routes section corrected; "stop revising and hand the A-vs-B decision to the operator."
