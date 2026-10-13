# Pre-registration — D-C10m-diag: gold-first-token-constrained read, edit + inject in one forward pass, and a third N seed (v2 FROZEN, 2026-10-05)

**Status: v2 FROZEN after the Codex gpt-5.5 v1 review (`results/c10m_diag_advisor_v1.md`, FIX-FIRST: items 1, 2, 3, 6 folded below; items 4, 5, 7 confirmed the design). Implementation (driver + reader) is next; nothing has run.** Decision-ID `D-C10m-diag`. Lineage: CORPUS/44 F-A5 (the edit+inject discriminator the advisor endorsed as the next diagnostic), `docs/INFRANODUS_INBOX_REVIEW_2026-10-05_round3.md` lead 1 (H-C10l-read-partition), CORPUS/45 addendum F-M7 (H-C10l-N-seed3). Rulings in force: D-C10k-rulings-1, D-C10k-rulings-2, D-C10l-rulings-1.

## 0. Where this sits on the e2e map, and what it is not

Both diagnostics read the **§C write path** (MEMIT compile of a coined value) through the **§F post-write verification** lens: they ask *where* the A7 coined-coined write fails after it is applied, not whether any contract is met. The third N seed extends the CORPUS/45 replication. None of the three is contract evidence; none changes a §6 label; C10 stays OPEN/BLOCKING whatever they return. They are cheap, they cannot be rescued into a result by post-hoc reading, and they decide what the next *mechanism* arm is (lead 5 mint z-layer, I-1 OverTone, or first-token targeting).

## 1. Questions and pre-stated hypotheses

| id | question | hypotheses (written before the run) |
|---|---|---|
| Q1 read partition (lead 1) | On the edited model, if the gold first value token is forced and the rest free-runs, how much of the A7 held-out gap closes? | **DRIFT**: constrained-full ≫ free-full → the residual is first-token selection, a cheap target. **CHAIN**: constrained-full stays low while teacher-forced per-token is high → the autoregressive chain fails after the first token even when started right. **ABSENT**: both low → the write is not there on those subjects. CORPUS/45's per-position curve (59/66/51/19/34/20 of 72) predicts CHAIN on roughly half the subjects. |
| Q2 edit + inject (CORPUS/44 F-A5) | With the harness edit applied **and** the pre-edit `zs` injected at the subject-last token in the same forward pass, does the value decode? | **H1 collateral**: ≈ edit-only counts → the edit's change at non-keyed positions (frame and generated tokens) breaks the decode even when the keyed residual is exact. **H2 read-differently**: ≈ injection-only counts → an edit-realised z is read downstream unlike an injected one, and the two interventions are not measuring the same thing. |
| Q3 third N seed (F-M7) | Is the N seed-to-seed spread (46/42 vs 34) a seed effect or the tail of the process spread? | **SEED-SENSITIVE**: the three-seed range ≥ 10/72. **SPREAD**: range < 10/72. Either way rule 1 of B3 stays UNSUPPORTED (34 < 38 already). |

## 2. Design (one diagnostic run + one replication pair; engine unmodified)

**Run D (Q1 + Q2), one process, baseline recipe, arms `A1_single` + `A7_coined_coined` on `experiments/track_c/c10e_bandknob.py` through a new driver `experiments/track_c/c10m_diag_arms.py` (same pattern as `c10l_mint_arms.py`: `ARM_HOOKS` seam, `LAW3_REF`, `DECISION_ID`, `PREREG`, `OUT`).**

1. **Before `H.main()` (pre-edit, same process):** for the 24 A7 requests compute `zs` with the harness's `compute_z` at layer 8 (hparams `HP_BASE`, engine context templates) exactly as `c10l_covgeom_p6_zinject.py:68`; keep the 24 vectors in memory, record their norms and a SHA-256 of the stacked tensor. Then the **in-process injection control**: `Inject(idx, z)` (the forward hook of `c10l_covgeom_p6_zinject.py:31–46`, subject-last index from `get_words_idxs_in_templates(..., "last")`) on the unedited model, greedy-decode `len(tids)` on `CANON` and the three `PTEST` templates → `inj_pre_canon` /24, `inj_pre_para` /72. Hook removed afterwards (context manager).
2. **The edit:** the harness's own `my_edit` for the A7 arm, unchanged (band 4–8, AlphaEdit-style solve, LAW#5 inertness gate as in every run).
3. **Post-edit hook (edit still applied, before the harness restores):**
   - **free-full** — the harness's `full_seq_match` (already reported as `para_full_n`, `canon_full_n`);
   - **constrained-full** — append `tids[0]` to the prompt, greedy-decode `len(tids) − 1`, match `tids[1:]` (one function, mirrors `full_seq_match`; a `constrained_string` readout decodes `len(tids) + 1` and compares text, as `string_match` does); on 24 `CANON` and 72 `PTEST`; per subject;
   - **teacher-forced per token** — the harness's `teacher_forced_pertok` per subject (already in the arm JSON as the per-position curve);
   - **edit + inject** — `Inject(idx, z_pre)` on the edited model, greedy-decode `len(tids)` on `CANON` and `PTEST` → `inj_post_canon` /24, `inj_post_para` /72, per template. **Binding uses the pre-edit `z_pre`** (the same vector P6 measures; advisor item 4). A `z_post` recomputed by `compute_z` on the edited model and injected the same way is **reported as a secondary** (`inj_post_zpost_*`), never read for H1/H2: it answers a different question (whether the edited model has a new reachable target).
4. Locality axes (L1, `described_as`, L3) and A1 come from the harness as usual; the hook adds no weight change.

**Runs S (Q3):** `MINT_INITS=N MINT_N_SEED=2 MINT_INIT_TAG=_seed2 OUT=results/c10l_mint/step0_probe_seed2.json c10l_mint_step0.py` (its own I-11 / P-iv / P3 gates; HALT if excluded) → `MINT_ARM=N MINT_STEP0=results/c10l_mint/step0_probe_seed2.json OUT=results/c10l_mint/arm_N_seed2.json c10l_mint_arms.py`. Nothing else changes.

Outputs: `results/c10m_diag/diag_run.json` (run D, with `zs_sha256`, `z_norms`, per-subject rows, per-template counts), `results/c10l_mint/step0_probe_seed2.json`, `results/c10l_mint/arm_N_seed2.json`, logs beside them. Mechanical reader `experiments/track_c/c10m_diag_read.py` applies §3 and prints the labels; no model judgement.

## 3. Pre-registered readings (frozen before the run; exact counts; the reader computes them)

**Validity (any failure → INVALID, no reading):** fingerprint d941a9fb at load; `LAW3_REF` A1/A2 ≥ 68/72; LAW#5 INERT; A1 ≥ 68/72 in run D; A7 edit-only `para_full_n` inside the identical-baseline envelope [5, 18]/72 and `canon_full_n` inside [5, 10]/24 (CORPUS/44); `inj_pre_para` ≥ 44/72 and `inj_pre_canon` ≥ 22/24 (the P6 reference 49/72, 24/24 minus the recorded per-process spread of ±3–5/72, CORPUS/44 F-A4; advisor item 1 — a lower control means the injection site or `zs` is not the P6 one and the run stops); L3 ≥ 29/30.

**Q1 — read partition** (`C` = constrained-full /72, `F` = free-full /72, `T_s` = teacher-forced fraction for subject `s`, `C_s` ∈ {0..3}):
- **DRIFT-LEAD** if `C − F ≥ 15/72` **and** `C ≥ 30/72` (the LEAD bar of CORPUS/44); **DRIFT-PARTIAL** if `C − F ≥ 15/72` and `C < 30/72` (first-token selection matters, but forcing it does not reach LEAD; advisor item 2).
- **CHAIN-PRESENT** if `C − F ≤ 5/72` and at least 8 subjects have `T_s ≥ 0.75` with `C_s ≤ 1`; **CHAIN-DOMINANT** only if those subjects are a majority (≥ 13/24; advisor item 3).
- **ABSENT-DOMINANT** if `C − F ≤ 5/72` and fewer than 8 subjects have `T_s ≥ 0.75`.
- **MIXED** otherwise. Per-subject table always reported (`F_s`, `C_s`, `T_s`, value, token count).
- What each label buys: DRIFT-LEAD → a first-token-targeting arm (cheap, harness-side) is next; DRIFT-PARTIAL → that arm is a secondary, the chain still has to be fixed; CHAIN-PRESENT / CHAIN-DOMINANT → lead 5 (mint z-layer) / I-1 OverTone stay the queue; ABSENT → the (i) predictors move up.

**Q2 — edit + inject** (`P_pre` = `inj_pre_para`, `P_post` = `inj_post_para`, `K_post` = `inj_post_canon`, `E` = edit-only `para_full_n`):
- **H2 (read-differently)** if `K_post ≥ 20/24` and `P_post ≥ P_pre − 10`.
- **H1 (collateral)** if `K_post ≤ 12/24` or `P_post ≤ E + 10`.
- **INDETERMINATE** otherwise (reported as such; no third hypothesis invented after the fact).
- Consequence: H1 → the next mechanism arm must change what the edit does at non-keyed positions (I-1 / I-2 territory, or a narrower write); H2 → injection ceilings stop being used as "the target admits LEAD" evidence and the P6 step is retired from future preregs.

**Q3 — third N seed** (`R` = max − min of the binding count over N seeds 0, 1, 2, using seed 0 = 46 (original, the CORPUS/45 row) and 42 (fourth replicate) both listed, `R` computed on the three distinct seeds with seed 0 = 46):
- **SEED-SENSITIVE** if `R ≥ 10/72`; **SPREAD** if `R < 10/72`.
- The B3 rules are re-evaluated with the new row for the record only; rule 1 cannot flip to SUPPORTED (replicate 2 is already −4).

## 4. What is NOT claimed, whatever the outcome

No §6 label of CORPUS/45 or §5 label of CORPUS/44 changes. "The write is there" is never inferred from a teacher-forced curve alone (INBOX review §3). An injection count is never contract evidence (§8.9). The third seed does not re-open G-vs-N. None of this can change the F1 label; what it does is decide the live C10 mechanism fork recorded in the runbook and checkpoint (which arm runs next). C10 stays OPEN/BLOCKING.

## 5. Runtime and halt discipline

Run D ≈ 45 min on the M3 Pro (24 × `compute_z` ≈ 4 min; pre-edit injection control ≈ 3 min; harness arms ≈ 30 min; post-edit hooks ≈ 8 min). Runs S ≈ 5 + 20 min. Halt discipline as in the mint prereg: one speculative fix after a `cat -n` read, then HALT with `architecture_profile/sNNN_halt_diagnostic.json`. Engine, LARQL, git unmodified. Close-out through `tools/closeout_check.py D-C10m-diag` (register the fingerprint source once the CORPUS entry exists).

## 6. Reviews

v1 → Codex gpt-5.5 advisor pass (`results/c10m_diag_advisor_v1.md`, FIX-FIRST) → v2 frozen with items 1 (control gate 44/72), 2 (DRIFT split by the LEAD bar), 3 (CHAIN-PRESENT vs -DOMINANT), 6 (F1 wording) folded; items 4 (pre-edit z binds; recomputed z secondary), 5 (hook mechanics read correctly), 7 (third seed secondary, same prereg) confirmed. Next: implementation review of the driver and reader before the run; cross-family at the verdict.
