# 47 — Target transport under the edit: the recomputed target is PORTABLE (LOW-CONTROL, reported, not promoted); where the edit fails, the edited model wants a 30 % longer, rotated target that also decodes on the unedited model

_Result 2026-10-05. Decision-ID D-C10n-ztransport ⟨D-C10n-ztransport@982edcbd⟩. Pre-registered `docs/C10N_ZTRANSPORT_PREREG.md` (v2 frozen after the Codex gpt-5.5 design pass; implementation pass; amendment N1 after a pre-registered halt, with its own pass; verdict pass before this entry — `results/c10n_ztransport_advisor_{v1,impl,n1,verdict}.md`). Records `results/c10n_ztransport/run.json` (run 2, the one run under N1, **binding**), `run_halt_1.json` (run 1, INVALID under v2 — the halt that produced N1; `architecture_profile/s27_c10n_halt_diagnostic.json`), `logs_c10n_chain.log` (full readout with the per-subject table). Driver `experiments/track_c/c10n_ztransport_arms.py` (library reuse of the D-C10m-diag functions; P6 injection hook unchanged); reader `c10n_ztransport_read.py`. Engine unmodified (fingerprint d941a9fb stored in full; LAW#5 INERT 0.0003). LAW#3 reference: D-C10l-covgeom ⟨D-C10l-covgeom@af2e38f7⟩ run 1 arm A. Lineage: CORPUS/46 F-D3 (D-C10m-diag ⟨D-C10m-diag@9a9b5343⟩)._

## Claim class
**Pre-registered diagnostic on the program's C10 harness — Qwen2.5-3B fp16 MPS, band 4–8, N = 24, 24 fictional subjects × 3 held-out paraphrases, one process in the LOW-CONTROL stratum. Mechanism-routing evidence for the next C10 arm; not contract evidence (§8.9); no label in CORPUS/44–46 changes; no bearing on the F1 label. C10 stays OPEN/BLOCKING.**

## VERDICT — TARGET-PORTABLE by the frozen rule, in a LOW-CONTROL process (reported; not promoted as a CORPUS/46 replication)

Instrumentation gates all GREEN: fingerprint; LAW#5; A1 71/72; A7 edit-only canon 7/24, para 12/72 (envelope [5, 18]); cell A canon 23/24 (≥ 22) and para 42/72 (instrument range ≥ 38); the full post-restore repeat of cell A identical on all 24 subjects × 4 templates; L1 0/12, `described_as` 90.3, L3 30/30.

| cell | canon /24 | held-out para /72 | per PTEST template |
|---|---|---|---|
| **A** `z_pre` → pre-edit model (control) | 23 | 42 | 11 / 14 / 17 |
| **B** `z_pre` → post-edit model | 7 | 13 | 2 / 5 / 6 |
| **C** `z_post` → post-edit model | 24 | 61 | 18 / 21 / 22 |
| **D** `z_post` → pre-edit model (the new cell) | 15 | 37 | 11 / 11 / 15 |

Control history with identical mechanics: 49 (CORPUS/44 P6), 54 and 51 (CORPUS/46), 42 (run 1, halted), 42 (this run) → **LOW-CONTROL** (A < 44; N1). CORPUS/46's cells are reproduced in this process (B 13 ≤ A − 20 = 22; C 61 ≥ A − 10 = 32) but, being LOW-CONTROL, the run is **not** promoted as a replication. **Reading:** D 37 ≥ A − 10 → **TARGET-PORTABLE**; DRIFT would have needed D ≤ 22.

**Geometry (descriptive):** mean cosine(`z_pre`, `z_post`) 0.854 [0.811, 1.000], mean normalized displacement 0.621. Bimodal: four subjects (Zorbland, Brinduun, Pradnoll, Thelby) at cosine 1.000 and displacement 0.02 (norm 80 → 79); the other twenty at cosine 0.81–0.84 and displacement 0.73–0.75 with norms 71–93 → 92–122 (≈ 1.3×). Held-out counts by group (from `run.json`): the four identical-target subjects score 10/12 in every cell (A, B, C, D) and account for 10 of the 13 B hits; the twenty rotated subjects score A 32, B 3, C 51, D 27 of 60.

## Findings (scoped: one LOW-CONTROL process; N = 24; one model)

- **F-Z1 (EVIDENCE-SHOWS, in this LOW-CONTROL process).** The recomputed target is portable: it carries the value on the unedited model (37/72) nearly as well as the original target (42/72), while carrying it far better on the edited model (61 vs 13). The DRIFT branch — each target working only on the model it was solved on — is not supported here.
- **F-Z2 (EVIDENCE-SHOWS, in this process).** The targets split in two. Four subjects' recomputed targets are the original ones to 2 % and those four account for 10 of the 13 held-out hits the original target still gets on the edited model; the remaining twenty subjects' recomputed targets are ≈ 30 % longer and rotated (cosine ≈ 0.82), and those decode strongly on the edited model (51/60) and acceptably on the unedited one (27/60 against 32/60 for the original target). This is consistent with CORPUS/44 step 0 (the edit realises `z_pre` at the keyed position to ≈ 3 %) only as a consistency, not a mechanism: injection and the weight edit remain different interventions (CORPUS/44 F-A3).
- **F-Z3 (I-INFER; H-C10n-magnitude for the register).** After the edit the original target no longer decodes at the keyed position for twenty subjects, a longer rotated one does, and that one is not worse on the unedited model. Cheapest next read (two cells, no engine change, ≈ 40 min): inject `z_pre` scaled by each subject's norm ratio into the edited model (magnitude alone), and inject `z_post`'s direction at `z_pre`'s norm (direction alone). It separates "the edit attenuates the keyed signal downstream" from "the edit rotates the required direction".
- **Method.** The injection control spans 42–54/72 over five processes with identical mechanics; it is a stratum, not a floor (N1), and any future injection-control rule on this harness is written that way. Run 1 halted correctly under v2's floor and is not retroactively validated.

## What this changes

- By the prereg's consequence map, **solve-side diagnostics come before engine-path changes**: the magnitude/direction read (F-Z3) first, then `compute_z` convergence and the AlphaEdit projector's effect on the target; I-1 OverTone / I-2 forward replay stay queued behind them. CORPUS/46's H1 bucket stands (B reproduced here). A HIGH-CONTROL repeat of this 2 × 2 is the way to promote the reading if a stronger claim is ever needed; it is not needed for routing.
- Not written here, by the advisor's instruction: DRIFT; "the solve under-shot"; "exactly the subjects where the edit fires"; any mechanism about positions, `compute_z` quality or the projector (prereg §4); replication of CORPUS/46 (LOW-CONTROL); contract evidence; any CORPUS/44–46 label change; any F1 change.
- Limitations: one LOW-CONTROL process; N = 24; one model (D-C10k-rulings-2); fp16 MPS; the control's own spread (42–54) is larger than the ±4 within-configuration process spread assumed when the first floor was set.


⟨D-C10l-covgeom@0caeca4f⟩
