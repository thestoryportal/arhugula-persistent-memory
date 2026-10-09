# 58 — Engine-path target construction (step 6): process-1 reading VALID; I-1 NULL, I-2 INVALID-CONTROLS; neither advances

_Record 2026-10-08. Decision-ID D-C10x-enginepath (CLOSED by this entry) ⟨D-C10x-enginepath@45fa3e90⟩. Pre-registration docs/C10X_ENGINEPATH_PREREG.md FROZEN v2.2 + Amendments T, M, P, Z, B (§10–§14), sha256 3eb899d9… (`run.json` `prereg_sha256`). Run directory results/c10x_enginepath_rerun3/, run identity `c10x_enginepath_rerun3_86153` (pid 86153), source commit 0bc9abd8, started 2026-10-08T23:30:50Z (17:30:50 MDT), finished 2026-10-09T01:25:34Z (19:25:34 MDT), status COMPLETE (`run.json`). Binding reader output results/c10x_enginepath_rerun3_logs/read_p1.out (sha256 322f8790…; JSON-equal to `reader.json`, sha256 b3debe4a…), status **VALID**, `errors` [], produced by the pinned reader experiments/track_c/c10x_enginepath_read.py sha256 d377b5fd… (driver `c10x_enginepath_arms.py` sha256 c3487253…). Engine unmodified, fingerprint d941a9fb / PASS, `_cov_cpu` 3 (`run.json` `fingerprint`). Go record results/c10x_enginepath_go_p1_rerun3.json sha256 54fa5a70… (D-C10x-go). Re-run under D-C10w-p2rerun: predecessor results/c10x_enginepath_rerun2, cause STAGE_PROJECTION_REFUSED (`run.json` `replacement`). Verdict review: GPT-6-Astra high, results/c10x_rerun3_reading_astra.md — **CONFIRM, no BLOCKING**. Lineage: CORPUS/44 (P6 injection vs write), CORPUS/46, CORPUS/51, CORPUS/53, CORPUS/57._

## Verdict

> D-C10x-enginepath, rerun3 process 1: VALID; I-1 NULL (17/72 versus 12/72), I-2 INVALID-CONTROLS (A1 64/72, A2 65/72); neither advances, process 2 is not run, and step 6 closes on this harness-specific reading without a mechanism or method-family conclusion.

(Astra's one-line record verdict, verbatim.)

- **I-1 (OverTone-inspired target objective): NULL.** A7 held-out full-sequence 17/72 against recipe A's 12/72 in the same process (+5): not sized (a count ≤ 18 is never sized, prereg :136). Controls A1 69/72, A2 72/72; no locality axis failed (`failed_locality` []); write ratio 0.982; no qualifier. Interpretation row 7 → NULL table: injection screen d = 51 − 55 = −4, inside the declared non-interpreted band −5 ≤ d ≤ 5 — "the reweighted target was not a better target for this write" (prereg :157–178; reader `null_row` NON-INTERPRETED).
- **I-2 (FE-inspired forward-replay target at layer 4): INVALID-CONTROLS.** This FE package failed the A1/A2 controls in this run (70→64, 71→65; floor 68, prereg :134). Interpretation row 2. The arm is not advanced and never triggers replication; it is not a halt and not a process-level invalidity. It licenses no spreading conclusion, no method-family rejection and no F1 change (Astra ADVISORY 1; prereg :162, :184).
- **Process 2 is not run.** `replication_eligible` is [] (no arm is LEAD or PARTIAL); Astra exercised the admission predicate: `PROCESS2_WITHOUT_ELIGIBLE_PROCESS1` (`c10x_enginepath_arms.py:176`; prereg :180).
- **What it buys (prereg :180, "What each buys"):** NULL and INVALID-CONTROLS → not advanced; the sequence moves to step 7; no claim that the engine path is exhausted, and a NULL never exhausts a method family. C10 stays OPEN/BLOCKING; F1 is unchanged.

**Plain meaning:** two published ideas for building a better target vector before the weight write were tried on the program's harness. Re-weighting the target's tokens (OverTone) moved recall of made-up two-word names from 12 to 17 of 72 reworded questions, too small to count under the preregistered margin. Re-building the target with forward replay at layer 4 (FE) made the ordinary single-token and two-token control facts worse (64 and 65 of 72, below the 68 floor), so its made-up-name count (9/72) is not read. Neither is taken forward.

## Counts (process 1, band 4–8, same process)

| Recipe | A1 para | A2 para | A7 para full | A7 canonical | A7 first token | A7 `described_as` | Perplexity | Label |
|---|---|---|---|---|---|---|---|---|
| A (baseline) | 70/72 | 71/72 | 12/72 | 8/24 | 52/72 | 89.31 | 21.755 → 21.606 | LAW#3 reference |
| I-1 OverTone | 69/72 | 72/72 | 17/72 | 8/24 | 59/72 | 88.56 | 21.755 → 21.5 | NULL |
| I-2 FE | 64/72 | 65/72 | 9/72 | 6/24 | 40/72 | 90.87 | 21.755 → 21.6 | INVALID-CONTROLS |

Source: `pass1.json` per-arm `para_full_n` (Astra: counts agree with per-prompt flags) and `process.log:27–29`, `:45–47`, `:58–60`. L1 0/12 and L3 30/30 in every arm of every recipe. Write ratios (Σ_l ‖ΔW_l‖_F arm / A, A7, CPU float64): I-1 0.9823342155998702, I-2 0.6713946698545705 (reader; from `write_norms_float64`, not printed in the log).

## Validity and gates

- **Reader status VALID**, `errors` []; Astra re-executed the pinned classifier under the recorded Python 3.11.16 and reproduced every field exactly.
- **LAW#3 known-baseline gate (recipe A, enforced in the driver before any candidate work):** A1 70 ≥ 68, A2 71 ≥ 68; A7 para 12 ∈ [5, 18], canonical 8 ∈ [5, 10], first token 52 ∈ [42, 59] (prereg :132). PASS.
- **LAW#5 inertness:** INERT in all three recipes, displayed |Δexpr| 0.0001 (raw 0.00012618303298950195), |Δloc| 0.21, `candidate_calls` 0 (`pass1.json` `law5_gate`); every recorded inertness check passes (`run.json` `inertness`: G8, X1-(i)–(v), X2-(ii)–(vii)).
- **Identity:** all 15 declared sources match at preflight, start, end and now; all four companion records match `run.json`; the go-record hash matches (Astra review).
- **Injection screen (unedited model, held-out /72; `inject.json`):** reference z_8 @ 8 = 51; I-1 z_8^OT @ 8 = 55; I-2 z_4 @ 4 = 32.
- **Budget (Amendment B, D-C10x-targetscap):** stage wall times setup 25.9 s, A 1566.2 s, targets 1984.3 s (cap 3600), inertness 1788.2 s, injection 95.4 s, I-2 722.2 s, I-1 714.6 s, final 4.2 s (`run.json` `timings`); total ≈ 6900 s against PROCESS_BUDGET 16200 s. Measured peak process RSS 13,468,893,184 bytes (unified-memory peak UNVERIFIED, `run.json` `memory`).

## Recorded beside the labels (observations, not labels)

- **I-2 fit screen.** The §2.5 I-2 fit screen (prereg :86: z_4 average probability ≥ 0.98 on ≥ 22/24 A7 facts) measured **3 of 24** (`targets.json` `targets.engine4.a7_fit`). The binding label stays INVALID-CONTROLS: interpretation row 2 precedes row 4, and the pinned reader attaches qualifiers only to arms that pass the controls (`c10x_enginepath_read.py:445–451`), so no -UNDERFIT is recorded on this arm.
- **I-2 write placement.** The A7 per-layer ‖ΔW_l‖_F under I-2 is 52.46 / 4.44 / 0.78 / 0.76 / 0.91 at layers 4–8, against recipe A's 15.81 / 12.07 / 11.98 / 19.92 / 28.45 (`pass1.json` `delta_norms`). This is the recorded shape of the write; it does not identify why the controls fell.
- **I-2 injection.** The layer-4 target injects 32/72 against the reference's 51/72 before any write. The NULL table applies only to NULL arms, so no NULL-table row is read for I-2.

## Process history (D-C10x-enginepath, all process 1)

1. **Original process 1** (results/c10x_enginepath/, launched 08:50 under D-C10x-go): HALTED 10:00 at 'W0 X2-vii exact zero' — fp16 −0.0 → +0.0 flips changed raw bytes, not values. Remedy: §13 Amendment Z (value-equality identity; D-C10x-signedzero, Astra GO).
2. **Re-run 1** (results/c10x_enginepath_rerun1/, 13:21): passed inertness; halted at the final record write on non-JSON scorer flags; its interim counts are not a result (commit 69544bc). Remedy: JSON coercion and strict-JSON validation at every stage (c658fb0, Astra GO).
3. **Re-run 2** (results/c10x_enginepath_rerun2/): HALTED STAGE_PROJECTION_REFUSED early in the targets stage under the frozen slowest-unit projection (prereg :118). Remedy: §14 Amendment B, targets cap 3600 s and PROCESS_BUDGET 16200 s under D-C10r-rulings-14 (D-C10x-targetscap; 7b3895a, 9897229; Astra GO).
4. **Re-run 3** (this record): COMPLETE; reader VALID.

Each compromised attempt was re-run, never read around (D-C10w-p2rerun). **Provenance note (Astra ADVISORY 3):** the go record's `at` field says 2026-10-08T17:45:00-06:00, while the run started 17:30:50 MDT. Preflight already holds that go record with its matching hash, so authorization is not in question, but the go-record timestamp is not a coherent chronology and should not be cited as one. Invocation note (ADVISORY 2): the pinned CLI requires absolute paths, and its exit code 0 does not by itself establish validity (it returns 0 after an INVALID result too); validity rests on the saved VALID result and the reproduced classifier.

## Not claimed

Not a mechanism reading and not a method-family conclusion: NULL does not close target construction, token reweighting, other OverTone settings (λ, ε, n), other band layers, or FE with MEMIT's own λC regulariser (prereg §4, :184). I-2's result is that this FE package failed the controls in this run, not that FE (or forward replay, or spreading) damages controls in general. I-1 makes no claim that the continuation tokens get an objective in the weight solve (prereg §0 item 2). Two binary audit files were hash-checked; their fresh numerical replay is UNVERIFIED (Astra ADVISORY 4). No CORPUS/36–57 label changes; C10 remains OPEN/BLOCKING; F1 is unchanged.

## Decision-ID and next

D-C10x-enginepath: **CLOSED** — process 1 VALID; I-1 NULL (17 vs 12/72, d = −4 non-interpreted); I-2 INVALID-CONTROLS (A1 64, A2 65); neither advances; process 2 not run. Next under the research-pass sequence: step 7 (C10Y, measurement-only; calibration memory-gated, D-C10y-memfloor); ASTRA attempt 3 (D-C10z-v5fix, operator-approved); the offline math lab D-ML-1 ⟨D-ML-1@12c5548b⟩ (prereg v2 in review).

_Verdict sentence: on the C10 harness, neither engine-path target construction advanced the coined-value write — the OverTone-inspired objective scored 17/72 against the same-process baseline's 12/72 (NULL, below the margin), and the FE-inspired layer-4 package failed the single-token and two-token controls in this run (64 and 65/72 against 68), so step 6 closes with no candidate taken forward, no process 2, and no mechanism or method-family conclusion; C10 remains OPEN/BLOCKING and F1 is unchanged._

## Erratum (appended 2026-10-08 ~20:05 MDT) — I-2 qualifier ⟨D-C10x-enginepath@a8c22280⟩

Appended after a cross-family labeling review; the text above, including the line that ends "so no -UNDERFIT is recorded on this arm" in *Recorded beside the labels*, is kept unchanged as the original record. Review: GPT-6-Astra high, results/c10x_underfit_label_astra.md — **DISAGREE** with that treatment (packet results/c10x_underfit_label_packet.md). The frozen prereg binds over its implementation. Astra's erratum, verbatim:

> **Erratum — I-2 qualifier.** The prereg-compliant reported label is **INVALID-CONTROLS-UNDERFIT**. A1 64/72 and A2 65/72 fail the 68/72 control floor, so INVALID-CONTROLS remains the primary outcome and interpretation row 2 applies. Independently, only 3/24 A7 z₄ targets meet fit ≥0.98 against the required 22/24; §2.5 therefore requires -UNDERFIT. Interpretation precedence does not remove qualifiers (§3:157). The pinned reader emitted INVALID-CONTROLS with an empty qualifier list because it suppresses qualifiers on control-failing arms; that historical output is preserved, and this prereg–reader discrepancy is recorded explicitly. I-2 remains not advanced and ineligible for replication; no spreading or method-family conclusion follows.

**Known reader defect (recorded, not fixed).** The pinned reader experiments/track_c/c10x_enginepath_read.py (sha256 d377b5fd…) applies qualifiers only when the base class is not INVALID-CONTROLS (`:445–451`), while the prereg requires the I-2 fit qualifier whenever the screen fails (§2.5 `:86`; "every applicable one recorded" `:149`) and states that interpretation "does not change any label" (`:157`). The reader is not modified (it is pinned); its output read_p1.out / reader.json (status VALID, I-2 `label` INVALID-CONTROLS, `qualifiers` []) stays the preserved historical output, and this erratum carries the prereg-compliant label. No other field of the reading changes: I-1 NULL; replication_eligible []; process 2 not run; reader status VALID.

Corrected one-line verdict: D-C10x-enginepath, rerun3 process 1: VALID; I-1 NULL (17/72 versus 12/72), I-2 INVALID-CONTROLS-UNDERFIT (A1 64/72, A2 65/72; fit 3/24 ≥ 0.98 against 22/24); neither advances, process 2 is not run, and step 6 closes on this harness-specific reading without a mechanism or method-family conclusion.

⟨2026-10-09 MathLab cross-reference: D-ML-1@46230e48; D-ML-4@46230e48 — STOPPED/calibration FAIL; step 4 SHELVED; latest reading: CORPUS/60_MATHLAB_HARVEST_REPLAY.md (dated calibration-stop addendum)⟩
