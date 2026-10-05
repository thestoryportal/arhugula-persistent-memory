# 46 — Where the A7 coined-value write fails: gold-first-token read ABSENT-DOMINANT, edit + inject in the H1 (collateral) bucket, minted-token N init SEED-SENSITIVE

_Result 2026-10-05. Decision-ID D-C10m-diag ⟨D-C10m-diag@9a9b5343⟩. Pre-registered `docs/C10M_DIAG_READPARTITION_EDITINJECT_PREREG.md` (v2 frozen after the Codex gpt-5.5 design pass; implementation pass before the run; verdict pass before this entry — `results/c10m_diag_advisor_v1.md`, `c10m_diag_advisor_impl.md`, `c10m_diag_advisor_verdict.md`). Records `results/c10m_diag/diag_run2.json` (**binding**), `diag_run.json` (non-binding provenance echo, see Validity), `logs_c10m_chain.log`, `logs_run_d2.log`; `results/c10l_mint/step0_probe_seed2.json`, `inits/N_seed2.pt`, `arm_N_seed2.json`. Driver `experiments/track_c/c10m_diag_arms.py` (harness `ARM_HOOKS` seam; P6 injection hook reused unchanged); reader `c10m_diag_read.py` (mechanical §3 labels). Engine unmodified (fingerprint d941a9fb recorded in the binding JSON; LAW#5 INERT, |Δexpr| 0.0002). LAW#3 reference: D-C10l-covgeom ⟨D-C10l-covgeom@5b553688⟩ run 1 arm A. Ruling in force: D-C10l-rulings-2 (run this before any mechanism change)._

## Claim class
**Pre-registered diagnostics on the program's C10 harness — Qwen2.5-3B fp16 MPS, band 4–8, N = 24, 24 fictional subjects × 3 held-out paraphrases. They locate where the A7 coined-value write fails after it is applied and decide the next mechanism arm. They are not contract evidence (§8.9), change no §5/§6 label of CORPUS/44–45, and do not bear on the F1 label. C10 stays OPEN/BLOCKING.**

## VERDICT — Q1 ABSENT-DOMINANT · Q2 H1 (collateral bucket) · Q3 SEED-SENSITIVE

Binding run (run 2), every validity gate GREEN: fingerprint d941a9fb; LAW#5 INERT; A1 72/72; A7 edit-only `para_full` 15/72 and canon 7/24 inside the identical-baseline envelope ([5, 18], [5, 10]); pre-edit injection control canon 24/24, para 51/72 (gate ≥ 22, ≥ 44); L1 0/12, `described_as` 90.6, L3 30/30.

| readout (run 2, binding) | canon /24 | held-out para /72 | per PTEST template |
|---|---|---|---|
| injection control, pre-edit model, `z_pre` at subject-last (P6 mechanics) | 24 | 51 | 16 / 17 / 18 |
| A7 edit-only (harness `full_seq_match`; `para_first` 55) | 7 | 15 | — |
| **Q1** constrained read: gold first token forced, rest free-runs (string readout identical) | 7 | 17 | — |
| **Q2** edit applied **and** `z_pre` injected, same forward pass (BINDING) | 7 | 23 | 8 / 7 / 8 |
| secondary (not binding): a target recomputed on the edited model, injected the same way | 24 | 55 | — |

Per subject (run 2): constrained minus free gain is 2/72; subjects with teacher-forced continuation ≥ 0.75 yet constrained ≤ 1/3 paraphrases: 3 of 24 (Glimsto, Fluvane, Trannak). The full 24-row table (`F_s`, `C_s`, `T_s`) is in `logs_c10m_chain.log`.

**Q3 (third N seed, CORPUS/45 F-M7):** step 0 admitted N(seed 2) (effective rank 23.72, 0 live, 0 cannibal, P3 24/24); arm N seed 2 binding 36/72, canon 24/24, sibling 0, cannibal 0, L1 0/12, L3 30/30, A1 69. Seeds 0 / 1 / 2 = 46 / 34 / 36 (seed-0 fourth replicate 42 listed, not ranged) → range 12 ≥ 10 → **SEED-SENSITIVE**.

**Labels by the frozen §3 rules:** Q1 — gain 2 ≤ 5 and 3 < 8 high-TF failing subjects → **ABSENT-DOMINANT**. Q2 — `K_post` 7 ≤ 12 → **H1 (collateral)**; H2 needed `K_post` ≥ 20 and `P_post` ≥ 41. Q3 — **SEED-SENSITIVE**.

**Validity note on run 1 (`diag_run.json`, 12:33–13:23).** Its JSON holds only the first line of the fingerprint tool's output (the PASS line without the hash), because the driver kept one line; the reader therefore labels it INVALID and it carries **no label**. The tool exits non-zero on any hash mismatch and the driver aborts on that, so the gate did pass at load, and the engine is git-clean at the same hash; the JSON was not edited. The driver now stores the full output and run 2 was made as the binding run. Run 1 is kept as a provenance echo only: its counts (injection control 24 / 54; edit-only 8 / 13; constrained 8 / 15; edit + inject 8 / 17; secondary 24 / 60) sit beside run 2's.

## Findings (scoped as above; one binding run, N = 24, one model)

- **F-D1 (EVIDENCE-SHOWS).** The edit + inject diagnostic lands in the pre-registered H1 bucket: with the band 4–8 edit applied, injecting the same `z_pre` that carries the value to 51/72 on the unedited model yields 23/72 and canon 7/24 — close to edit-only (15/72, 7/24) and far below the pre-edit control. The numbers do not isolate which non-keyed position or downstream component is responsible.
- **F-D2 (EVIDENCE-SHOWS).** Forcing the gold first token moves the held-out count from 15 to 17/72 under this constrained greedy readout; chain failure after a correct start is present on 3 subjects only. First-token selection is not the residual.
- **F-D3 (EVIDENCE-SHOWS, secondary; I-INFER marked).** The edited model still admits a high-performing recomputed target under the same injection procedure (24/24, 55/72). **Hypothesis (not inferred here):** the solve's target and the geometry the edit realises downstream drift apart under the edit. The cheapest separating test (advisor): store `z_pre` and `z_post`, inject each on the pre-edit and the post-edit model at the same prompts (2 × 2), and report ‖`z_post` − `z_pre`‖, cosine and per-subject success deltas — this separates vector-target drift from "injection on an edited model is a different intervention".
- **F-D4 (EVIDENCE-SHOWS).** The minted-token random init is seed-sensitive on this harness (range 12/72 across three seeds against a ±4 process spread). A single-seed ordering between inits is not evidence; init comparisons pre-register ≥ 3 seeds.
- **Method.** The in-process injection control reproduces P6 (49/72 in CORPUS/44) at 51–54/72 across processes; the P6 ceiling is a property of the unedited model and must not be read as the ceiling of the edited one.

## What this changes

- **The mechanism fork is decided for now:** H1. The next mechanism arm must change what the edit does at non-keyed positions (I-1 OverTone / I-2 forward replay on the engine path, or a narrower write); first-token targeting is dropped (F-D2); the H2 consequence (retiring injection ceilings) does not fire. Before I-1/I-2, the 2 × 2 transport diagnostic of F-D3 is the cheapest next read (no engine change, ≈ 1 h), and the (i) predictors (I-4/I-4b) move up on the ABSENT reading.
- CORPUS/44's P6 "the target admits LEAD" reading is now scoped to the unedited model (F-D1, Method).
- CORPUS/45 F-M7 is answered: seed-sensitive; H-C10l-N-seed3 closes; any future init ordering needs ≥ 3 seeds.
- Not written here, by the advisor's instruction: "collateral change is sufficient/causal"; "the write is there" from the teacher-forced curve; "nothing of the value is present" beyond the constrained greedy readout; injection counts as contract evidence; "the edit destroys the target" (F-D3); any §5/§6 label change; any F1 change.
- Limitations: one binding run (run 1 agrees on every count within 2–6/72 but carries no label); N = 24; one model (D-C10k-rulings-2); fp16 MPS.
