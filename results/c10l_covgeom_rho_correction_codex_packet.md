# Advisor / objective-review prompt (reusable — Claude & Codex)

You are an **independent, adversarial reviewer** of a research step in the LLM-as-Database program. You are not the author. **Do not rubber-stamp.** Your job is to find where the work is wrong, over-claimed, confounded, or drifting from the goal — *before* it is leaned on.

You will be given ONE of: a **test/experiment design** (before it runs), a **finding/result** (before it is declared conclusive or written to CORPUS), or an **approach** the author is about to commit to — together with its evidence (artifact paths + numbers) and the relevant context.

Run this review and answer concisely and specifically:

1. **Real criterion.** Does this answer the question's *actual* criterion, or a flattering adjacent one? (e.g. is the metric matched to the claim — top-1 for read-correctness, distributional for distributional; is the gate's true requirement being met or a softer proxy?)
2. **Confounds & over-claims.** Hunt for confounds, leakage, Goodhart, and over-statement. Is `EVIDENCE-SHOWS` blurred with `I-INFER`? Is "the mechanism works" being passed off as "the contract is met" (**mechanics ≠ contract**)? Is design-viability being passed off as empirical evidence?
3. **Cite or flag.** Every factual claim must cite an artifact (path + exact number) or be labeled **`UNVERIFIABLE`**. Call out any claim that isn't grounded. Verify that external repos/IDs/claims were actually checked before being relied on.
4. **The overturning test.** What is the *cheapest* experiment or control that could **falsify** this finding/design? If it hasn't been run, that is the gap.
5. **Drift check.** Does this advance the F1 readiness determination (or a live §0.3 falsifier)? If not, say so.

**Output:** a short verdict — `PROCEED` / `FIX-FIRST` / `OVERTURNED-OR-RECONSIDER` — then the **single most important thing** to do next, then the specific issues in priority order. Be a skeptic; the author will weigh your input heavily but evidence remains binding over your opinion.


---

# Review packet — a FINDING before it is written to CORPUS: the ρ_c reading in CORPUS/44 is reversed (2026-10-06)

You raised this in your step-4 design pass (`results/c10v_layerpick_codex_design_v1.md` item 1). The program session verified it against `experiments/track_c/c10l_covgeom_step0.py` (lines 74–75 and 134) and `results/c10l_covgeom/step0_offline.json`, wrote the correction note below, and ran the advisor pass (also below; its seven items are folded in v2). Before the append-only correction goes into `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md` and the four verbatim copies, judge: (1) is every sentence of the proposed CORPUS append true to the code and the JSON, with EVIDENCE-SHOWS and I-INFER correctly tagged; (2) does the note correctly state that no label changes (check CORPUS/44 lines 20–45 and CORPUS/46 F-D1, CORPUS/47–50 line 6); (3) is the propagation list complete (grep the repository for the reversed sentence and for '3 %' / '3 percent' readings of ρ_c); (4) the proposed in-harness ρ_c readout as the overturning test — right instrument, right arms; (5) anything that would mislead a cold reader of CORPUS/44 after the append. Verdict: PROCEED (apply the append) or the single thing to fix.

## results/c10l_covgeom_rho_correction_2026-10-06.md (v2)

# Proposed append-only correction to CORPUS/44 ⟨D-C10l-covgeom@5b553688⟩ — the reading of ρ_c is reversed (v2, 2026-10-06)

**Status: PROPOSED v2 — not applied. Advisor pass done (`results/c10l_covgeom_rho_correction_advisor_v1.md`, FIX-FIRST, seven items, folded below). Owed: the cross-family reviewer (Codex GPT-6-Astra) on this note, then the append-only "Correction" block in `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md`, the same one-clause correction at the four verbatim copies listed below, re-stamping of the Decision-ID token wherever it is referenced, and a §13 line.** Raised by the Codex design pass on the step-4 pre-registration (`results/c10v_layerpick_codex_design_v1.md`, item 1); verified against the source by the program session the same day.

## What the number is

`experiments/track_c/c10l_covgeom_step0.py`:
- lines 74–75: `rel(dW, K, R) = ‖dW·K − R‖ / ‖R‖` — the **relative residual error left after** the layer's write, per layer;
- line 134: `rho_c_band = ‖zs − cur1_c‖ / ‖zs − cur0_c‖` — the band-level **fraction of the canonical residual norm that remains** at the z-layer after all five writes, in step 0's float64 offline reconstruction of the harness loop (`cur1_c` is the post-write block output at the keyed position, `cur0_c` the pre-write one; lines 89, 132–133); the same for the paraphrase proxy `rho_p_band` and per subject / per template (135–137).
- The pre-registration defined it this way (`docs/C10L_COVGEOM_SPARSEBAND_PREREG.md:44, :49`: "R1 lowers ρ_c → mechanism present") and the JSON's `H-I8a_mechanism_present: True` reads it correctly.

Recorded values (`results/c10l_covgeom/step0_offline.json`, `regularisers.*.band`): R0 (the harness) ρ_c 0.028, ρ_p 0.232 (per held-out template 0.314 / 0.209 / 0.119); R1 (P := I) 0.008 / 0.222; R2 (engine ridge) 0.060 / 0.494; R3 0.093 / 0.244. Per-layer `rho_c` for R0: 0.135, 0.051, 0.033, 0.053, 0.037.

**What may and may not be said from it.** In step 0's reconstruction, 2.8 % of the canonical residual norm remains after the band write. The ratio is of residual norms, not a projection: by the triangle inequality the installed share `‖cur_after − cur_before‖ / ‖z − cur_before‖` lies in [0.972, 1.028] and may overshoot, so "≈ 97 % installed" is a bound on a reconstruction, not a measurement of the edit that scored 7/24. No behavioural run has recorded ρ_c inside the harness itself (`c10e_bandknob.py:197–217` reads `cur` once, before the band, and never re-reads it).

## What CORPUS/44 says, and what is wrong

- Line 25 ("band-level realised residual at the z-layer R0 (harness) ρ_c 0.028 / ρ_p 0.232") is ambiguous and reads naturally as "the fraction realised".
- Line 31, **F-A3 (EVIDENCE-SHOWS)**: "… while the weight edit that realises the same z to 3 % at that position (step 0 ρ_c 0.028) yields 7/24 and 13/72." **Reversed**: 2.8 % of the residual norm *remains*. The behavioural clause (injection 24/24 and 49/72 vs the edit's 7/24 and 13/72) stands; only the mechanistic clause is withdrawn.
- R1's "does not behave better" is what is licensed (canon 7 → 4; the canon envelope is [5, 10]/24, CORPUS/44:39), not "behaves worse".
- Line 40 already withholds "ρ_c 0.03 as proof the behavioural edit realises the target" — correct under either reading, unchanged.

**No label changes.** CORPUS/44's labels (NULL ×3) and F-A4/F-A5 stand; CORPUS/47–50 cite CORPUS/44 by count or "no label change" (`CORPUS/47:6`, `48:6`, `49:6`, `50:6`); CORPUS/46 F-D1 (`:30`) is independent and routed F-A5's H2 into the H1 bucket. **The inverted consequence:** the ledgers' conclusion — "the P6-vs-edit gap points at the edit's collateral effect" — is *better* supported under the right reading (the target is installed in norm at the canonical position and the gap persists), so this fold is not a retraction of H1.

## Where the reversed sentence is carried (each gets the same one-clause dated correction, pointer to this note)

Verbatim copies ("step 0 realises z to 3 % at the keyed position, so the P6-vs-edit gap points at the edit's collateral effect"): `CORPUS/00_MASTER_EVIDENCE.md:233`, `CORPUS/03_STATUS_LEDGER.md:140`, `EXPERIMENT_RUNBOOK.md:849` (§13 — append-only: a dated correction line, not an edit of the entry), `docs/HYPOTHESIS_REGISTER_2026-06-18.md:341`.

Dependent readings: `results/research_pass_2026-10-06/recommended_sequence.md` §"ranking criteria" item 3 and steps 6–7 (":13, :26–27": "the write installs only about 3 percent of its intended signal") and `hypotheses.md` H-3 mechanism line (":43") — the research pass took CORPUS/44 at its word; the sequence's rationale for ranking "realisation" arms (steps 6–7) above "address" arms rests partly on it, and the operator must see this before steps 6–7 are scheduled. `docs/C10S_SHARED_Z_PREREG.md` v3 lineage line — the design does not depend on it (H-S0 cites F-D1); amendment A1 adds the in-harness ρ_c readout (below). `docs/C10T_SECONDKEY_PREREG.md` v2 and `docs/C10V_LAYERPICK_PREREG.md` v2 already carry the corrected reading.

## The overturning test (owed to the next harness run that solves z; no new GPU time of its own)

Record `‖z − cur_after‖ / ‖z − cur_before‖` **inside** the harness run at the z-layer keyed position for every arm (a post-edit hook re-reading `cur` as `my_edit:197–201` does pre-edit), for A7 **and A1**. If A1 and A7 both leave ≈ 3 % while A1 scores 69/72 and A7 13/72, realisation-in-norm says nothing about the wall; if A7 leaves materially more than A1 in the behavioural run, step 0's reconstruction under-reported it. Added to `D-C10s-sharedz` as amendment A1 (readout only; no gate).

## What the corrected reading implies for the open accounts (I-INFER, for the register, not for CORPUS)

The "realisation account" (the linear write cannot install the target at the keyed position) is weakened at the canonical position and must be re-stated as: in reconstruction the write installs the target in norm at the canonical keyed position, yet (i) ≈ 23 % of the residual remains on paraphrase prompts under the proxy, and (ii) injecting the same z into the *edited* model yields 23/72 (CORPUS/46 F-D1). Collateral change and the key-side difference under paraphrase are the live accounts; norm installation is not behavioural installation (R1). This bears on the sequence's criterion 3 and on H-3 (direct ΔW optimisation, step 7): its "3 % installed" motivation is gone; what remains is the paraphrase-realisation and collateral question.

## Proposed CORPUS/44 append (verbatim, placed after the last section; nothing above it edited)

> **Correction (2026-10-06, append-only; raised by the cross-family reviewer during the step-4 pre-registration, verified against `experiments/track_c/c10l_covgeom_step0.py:74–75, 134`; advisor pass `results/c10l_covgeom_rho_correction_advisor_v1.md`).** ρ_c and ρ_p are *remaining-residual* ratios, `‖z − cur_after‖ / ‖z − cur_before‖`, in step 0's float64 offline reconstruction. F-A3's clause "the weight edit that realises the same z to 3 % at that position" is reversed: ≈ 2.8 % of the canonical residual norm *remains* after the band write (the installed share lies in [0.972, 1.028] by the triangle inequality; R1 leaves 0.8 % and does not behave better, canon 7 → 4), and ≈ 23 % remains on the paraphrase prompts under the mixed-prefix proxy. No label of this entry changes; F-A3's behavioural clause (24/24 and 49/72 under injection vs 7/24 and 13/72 under the edit) stands; the mechanistic clause is withdrawn. **I-INFER:** the P6-vs-edit gap is therefore not a canonical-position realisation shortfall; F-A5's H1 (collateral change; H2 was routed into it by CORPUS/46 F-D1) and the key-side difference under paraphrase remain the live hypotheses. No behavioural run has yet recorded ρ_c inside the harness; the next run that solves z records it for A1 and A7 (D-C10s-sharedz amendment A1).


## results/c10l_covgeom_rho_correction_advisor_v1.md

# Advisor review v1 — proposed ρ_c correction to CORPUS/44 (2026-10-06)

**Verdict: FIX-FIRST.** The reversal is real and the correction's direction is right; the append text and the propagation list need fixes before the CORPUS gate.

**Single most important thing.** "≈ 97 % installed" is a bound from one offline reconstruction, not a measurement of the edit that scored 7/24. Reword to "2.8 % of the canonical residual remains in norm, in step 0's reconstruction", and add the missing control: record `‖z − cur_after‖/‖z − cur_before‖` inside the harness run itself (`experiments/track_c/c10e_bandknob.py:197–217` reads `cur` once and never re-reads it after the band). Until that exists for a behavioural run, "the edit installs the target at the keyed position" is the reconstruction's claim, not the run's.

## Issues, priority order

1. **(a) Reading — correct, with caveats the note omits.** `rel = ‖dW·K − R‖/‖R‖` (`c10l_covgeom_step0.py:74–75`) and `rho_c_band = ‖zs − cur1_c‖/‖zs − cur0_c‖` (`:132–134`) are remaining-residual ratios; R0 band 0.0282, R1 0.0080 (`step0_offline.json` `regularisers.R0.band`, `.R1.band`). The pre-registration defined it this way (`docs/C10L_COVGEOM_SPARSEBAND_PREREG.md:44`, `:49` "R1 lowers ρ_c → mechanism present") and the JSON's `H-I8a_mechanism_present: True` reads it correctly — CORPUS/44:31 misread its own prereg; say so, it is the strongest support. Caveat 1, cross-process: step 0 has its own context-template draw (F-A4, `CORPUS/44:32`, delta_norms vary up to 4.35 %); arm A's ρ_c was never measured. Caveat 2, precision: `f32_vs_f64_rel` is 3e-5–7e-5 per layer (R0 `per_layer`) and both paths cast to fp16 (`step0.py:128–130`, `c10e_bandknob.py:217`), so F-A5 H3 is effectively answered — state it instead of leaving H3 silently alive.

2. **(d) "≈ 97 % installed in norm" over-states.** The ratio is of residual norms, not a projection; by the triangle inequality `‖cur_after − cur_before‖/‖z − cur_before‖` lies in [0.972, 1.028] and may overshoot. Write "2.8 % remains in norm" or give the interval. "R1 behaves worse (canon 7 → 4)": the canon envelope is [5, 10]/24 (`CORPUS/44:39`); "does not behave better" is what is licensed.

3. **(c) I-INFER leaks into the append.** The §"implications" block is labelled and excluded, but the append's last sentence ("not a canonical-position realisation shortfall; H1 and the key-side difference remain live") is untagged inference; CORPUS/44 tags every such clause (`:33`). Tag it, and say H2 was routed to the H1 bucket by `CORPUS/46:30` rather than dropping H2 unmentioned.

4. **(e) Propagation list incomplete; one claim false.** The note (:27) says the ledgers carry "NULL ×3 only". They carry the reversed sentence verbatim — "step 0 realises z to 3 % at the keyed position, so the P6-vs-edit gap points at the edit's collateral effect" — at `CORPUS/00_MASTER_EVIDENCE.md:233`, `CORPUS/03_STATUS_LEDGER.md:140`, `EXPERIMENT_RUNBOOK.md:849` (§13), `docs/HYPOTHESIS_REGISTER_2026-06-18.md:341`. Also missing: `recommended_sequence.md:26–27` (steps 6–7 "aimed at the '3 percent installed' finding"), `prereg_stubs.md:74, :78`, `docs/C10V_LAYERPICK_PREREG.md:34`. `docs/EVIDENCE_INDEX.md` not found at that path; auto-memory outside this directory: UNVERIFIABLE.

5. **(b) Labels.** None change: F-A3's behavioural clause (49/72 vs 13/72) stands, only its mechanistic clause is withdrawn; CORPUS/47–50 cite CORPUS/44 by count or "no label change" (`CORPUS/47:6`, `48:6`, `49:6`, `50:6`); F-D1 (`CORPUS/46:30`) is independent. Correct. Add the inverted consequence explicitly: the ledger's conclusion ("points at the collateral effect") is *better* supported under the right reading, so the fold is not a retraction of H1.

6. **Overturning test.** The in-harness ρ_c readout above, plus one A1 line (A1 ρ_c never measured, `results/c10v_layerpick_advisor_v1.md:23`): if A1 and A7 both leave ≈ 3 %, realisation-in-norm says nothing about the wall.

7. **Drift.** Bookkeeping on a live C10 falsifier; it changes the ranking rationale of sequence steps 6–7 (`recommended_sequence.md:13`) and the operator must see it before they are scheduled. No F1 bearing.
