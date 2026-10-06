# Pre-registration — D-C10n-ztransport: does the solve's target drift under the edit, or is injection on an edited model a different intervention? (v2 FROZEN, 2026-10-05)

**Status: v2 FROZEN after the Codex gpt-5.5 design pass (`results/c10n_ztransport_advisor_v1.md`, FIX-FIRST: all five items folded below). Implementation review next; nothing has run.** Decision-ID `D-C10n-ztransport`. Lineage: CORPUS/46 F-D3 (D-C10m-diag ⟨D-C10m-diag@9a9b5343⟩) and its advisor's separating test; CORPUS/44 P6; rulings D-C10l-rulings-2 (diagnostics before mechanism changes), D-C10k-rulings-2 (Qwen2.5-3B only).

## 0. Where this sits, and what it is not

A one-run diagnostic on the **§C write path** read through **§F post-write verification**: it asks what the edit does to the *target vector* the solve aimed at, so the next mechanism arm (I-1 OverTone / I-2 forward replay / narrower write) is chosen on evidence. It is not contract evidence (§8.9), changes no label in CORPUS/44–46, and cannot change the F1 label. C10 stays OPEN/BLOCKING.

## 1. The question and the four cells

CORPUS/46 established, on this harness, that the pre-edit target `z_pre` carries the value to 51/72 on the unedited model and to 23/72 once the band 4–8 edit is applied, while a target recomputed on the edited model, `z_post`, carries it to 55/72 there. Two readings fit: **(DRIFT)** the edit moves the geometry the target must occupy, so each z works only on its own model; **(TARGET-QUALITY)** `z_post` is simply a better vector, which would also work on the unedited model, meaning the solve under-shot its own target. The missing cell separates them: `z_post` injected into the **unedited** model.

| | injected into the pre-edit model | injected into the post-edit model |
|---|---|---|
| `z_pre` (compute_z on the pre-edit model) | **A** — control (CORPUS/46: 51–54/72) | **B** — CORPUS/46 binding cell (17–23/72) |
| `z_post` (compute_z on the post-edit model) | **D** — the new cell | **C** — CORPUS/46 secondary (55–60/72) |

Plus the geometry per subject: ‖`z_pre`‖, ‖`z_post`‖, ‖`z_post` − `z_pre`‖, cosine(`z_pre`, `z_post`), and the per-subject hit pattern across A/B/C/D.

## 2. Design (one process, baseline recipe, arms A1 + A7, engine unmodified)

Driver `experiments/track_c/c10n_ztransport_arms.py`, reusing the D-C10m-diag functions (`compute_zs`, `inject_sweep`, `z_record`, the P6 `Inject` hook) without change.

1. **Pre-edit:** fingerprint (full tool output stored); `z_pre` for the 24 A7 requests at layer 8; cell **A** = `inject_sweep(z_pre)` on the unedited model (validity gate below).
2. **The edit:** the harness's own `my_edit` (band 4–8), LAW#5 gate as always.
3. **Post-edit hook (edit still applied):** `z_post` = `compute_zs` on the edited model; cell **B** = `inject_sweep(z_pre)`; cell **C** = `inject_sweep(z_post)`; `z_post` kept in memory with its SHA-256 and norms.
4. **After `H.main()` returns** (the harness has restored the base weights — `run_recipe` ends with `restore_layers`): repeat the **whole** cell A sweep (all 24 subjects, 96 prompts); the per-subject, per-template rows must match the pre-edit A rows exactly (advisor item 2 — the same observation surface D depends on), then cell **D** = `inject_sweep(z_post)` on the restored model.
5. Geometry (descriptive, not a gate — advisor item 1): per subject ‖`z_pre`‖, ‖`z_post`‖, ‖`z_post` − `z_pre`‖, the normalized displacement ‖`z_post` − `z_pre`‖ / ‖`z_pre`‖ and the cosine; summary means and the per-subject table.

Output `results/c10n_ztransport/run.json`; reader `experiments/track_c/c10n_ztransport_read.py` applies §3 and prints the table. Runtime ≈ 55 min (two `compute_z` sweeps ≈ 8 min, four injection sweeps ≈ 12 min, harness arms ≈ 30 min).

## 3. Pre-registered readings (frozen before implementation; counts /72 on the 72 PTEST prompts, canon /24 reported beside)

**Validity (any failure → INVALID, no reading):** fingerprint d941a9fb in the stored output; LAW#5 INERT; A1 ≥ 68/72; A7 edit-only `para_full` in [5, 18] and canon in [5, 10]; cell A ≥ 44/72 and ≥ 22/24; the full post-restore repeat of cell A identical to the pre-edit rows (all 24 subjects × 4 templates); L3 ≥ 29/30.

**Replication of CORPUS/46 (reported, binds the reading's scope):** B ≤ A − 20 (the H1 bucket) and C ≥ A − 10 **and C ≥ 44/72** (an absolute floor matching the control gate, so "z_post carries the value" cannot mean a low-30s count — advisor item 3). If either fails, the §3 labels below are still computed but the entry says "CORPUS/46 cells not reproduced in this process" and the drift reading is not promoted.

**The reading (one of three):**
- **DRIFT** if `D ≤ A − 20`: each target works only on the model it was solved on → the edit moves the geometry the target must occupy. The label is behaviour-primary (cell D); the geometry (normalized displacement, cosine) is reported beside it and does not gate (advisor item 1).
- **TARGET-PORTABLE** if `D ≥ A − 10`: `z_post` also carries the value on the unedited model. This shows portability only; it does not show that `z_pre` "under-shot" or that the solve objective is defective (advisor item 4).
- **INDETERMINATE** otherwise; the geometry is reported and no further hypothesis is invented after the fact.

**What each buys:** DRIFT → I-1 OverTone / I-2 forward replay (which re-solve against the realised geometry) are the right next arms; a narrower write is the cheaper alternative to try first if the per-layer norms point at the band edges. TARGET-PORTABLE → run solve-side diagnostics first (`compute_z` convergence and steps, the objective, the AlphaEdit projector's effect on the target) before any engine-path change. INDETERMINATE → I-1 / I-2 proceed on CORPUS/46's H1 bucket alone.

## 4. Not claimed, whatever the outcome

No label in CORPUS/44–46 changes. Injection counts are not contract evidence. "The edit destroys the target" is not written (C/D show reachable targets). A DRIFT reading does not say *which* positions carry the drift (that is the H1 bucket's open question, not this run's). Neither DRIFT nor TARGET-PORTABLE proves a mechanism about `compute_z` quality, projector failure or generated-token positions; each only licenses the next diagnostic fork (advisor item 5). Nothing here can change the F1 label; it decides the live C10 mechanism fork recorded in the runbook. C10 stays OPEN/BLOCKING.

## 5. Halt discipline and close-out

One speculative fix after a `cat -n` read, then HALT with a diagnostic JSON. Engine, LARQL and git unmodified. Close-out through `tools/closeout_check.py D-C10n-ztransport` once the CORPUS entry exists (register the source span first; stamp the bare IDs in the source before computing the token).

## 6. Reviews

v1 → Codex gpt-5.5 design pass (`results/c10n_ztransport_advisor_v1.md`, FIX-FIRST: geometry descriptive with normalized displacement, full A repeat, C ≥ 44 floor, TARGET-PORTABLE, extra non-claim — all folded) → v2 frozen → implementation review → run → verdict pass → CORPUS/47.

## 7. Amendments (post-freeze; each with its own advisor pass before the affected step runs)

### N1 — control gate re-derived from all observations after a pre-registered halt (2026-10-05; `architecture_profile/s27_c10n_halt_diagnostic.json`)

**Gate that forced it:** run 1 (16:02) stopped before the edit by §3's own rule: the pre-edit injection control came in at 42/72 (canon 23/24) against the 44/72 floor. The floor had been set as "P6 reference 49 minus the 3–5 process spread" from three observations (49, 54, 51); the fourth sits 7 below the previous minimum. The engine samples context templates per process (CORPUS/44 F-A4), so `compute_z` targets and their injection counts move per process; the lesson of CORPUS/44 applies — derive the envelope from all observations, never a subset.

**Change (after the Codex pass on N1, `results/c10n_ztransport_advisor_n1.md`, FIX-FIRST folded):** the control level **A is a measured stratum, not a success gate**. The instrumentation gates stay (fingerprint, LAW#5, A1 ≥ 68, A7 edit-only envelope, canon ≥ 22/24 on cell A, post-restore identity of cell A, L3); an A below the observed envelope (**A < 38/72**) is INVALID (instrument out of range). Otherwise the four cells always run and the labels are computed as frozen (A-relative: DRIFT D ≤ A − 20; TARGET-PORTABLE D ≥ A − 10; INDETERMINATE between — margins unchanged; at A = 42 that is D ≤ 22 vs D ≥ 32, conservative towards INDETERMINATE). The replication clause is stratified: **HIGH-CONTROL** if A ≥ 44 and C ≥ 44 (with B ≤ A − 20 and C ≥ A − 10) → the reading may be promoted as a CORPUS/46 replication; **LOW-CONTROL** if 38 ≤ A < 44 or 38 ≤ C < 44 → the reading is reported, may guide the next diagnostic, and is **not** promoted as a CORPUS/46 replication unless corroborated by a HIGH-CONTROL process. The halted run remains INVALID under v2; N1 does not retroactively validate it (its artefacts are kept as `results/c10n_ztransport/run_halt_1.json`, `logs_run_halt_1.log`). A fresh process runs once under N1; it is not re-run on its A.

**Record:** the control now spans 42–54/72 over four processes with the same mechanics; CORPUS/47 reports A's position in that spread beside the cells, and any future injection-control rule on this harness is a stratum, not a floor.
