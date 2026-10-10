# 02 — VALIDATION & VERIFICATION CHAIN (hypothesis → theory → provable validation)
_For each load-bearing claim: the falsifiable hypothesis, the method, the measurement, the pass criterion set BEFORE the result, and the verdict. This is the scientific spine — the council audits the LOGIC here, not just the numbers._

### C1 — In-weight same-entity multi-attribute editing is achievable (model-dependent)
- **Hypothesis:** A MEMIT-class edit of one attribute can leave the entity's other attributes intact (same-entity locality), for at least some models.
- **Method:** Calibrate a JS-based same-entity-locality metric with a clean null-edit floor (P0); single-edit on GPT-J/Qwen-7B/Qwen-3B (P1).
- **Criterion:** clean null floor (>~95% locality on a no-op) AND a real edit's same-entity locality clearly above floor noise for ≥1 model.
- **Verdict:** PROVEN, model-dependent. Floors 99%+. Single-edit same-entity: GPT-J 67.98% (fails), Qwen-7B 99.86%, Qwen-3B 98.41%. → C1 holds for Qwen, not GPT-J.

### C2 — Sequential multi-field writes don't have to clobber prior writes
- **Hypothesis:** Stock MEMIT clobbers earlier edits on the same entity; an in-solve null-space method (AlphaEdit) + accumulating cache can prevent it.
- **Method:** edit attr-1 then attr-2 on same entity; measure edit-1 retention. Compare stock MEMIT vs in-solve AlphaEdit; tune nullspace_threshold. LAW#5: prove harness reproduces engine (inertness) first.
- **Criterion:** AlphaEdit retention ≫ MEMIT, with expression intact, inertness proven.
- **Verdict:** PROVEN. MEMIT 33% → AlphaEdit 100% retention; threshold 0.005 gives 100% ret + 80.69% untouched + 100% expression; inertness gate passed.

### C3 — Cross-entity collapse at write-depth is real, and fixable by preserve-sampling
- **Hypothesis (falsification):** writing many same-relation facts corrupts UN-edited entities' same-relation facts.
- **Method:** 33-edit stream; track edited-fact retention, un-edited control locality, perplexity. Then seed cache with a sample of un-edited entities' keys; measure held-out controls.
- **Criterion:** if control locality collapses → falsified-as-clean; if preserve-sampling restores held-out controls → mitigation works.
- **Verdict:** PARTIAL→MITIGATED. Edited retention 100% + ppl flat (good); control collapsed 99.83%→11.99% (falsified clean); preserve-sampling restored held-out control 22%→78% (mitigation generalizes; coverage knob).

### C4 — Novel-record INSERT needs batched (joint) compile
- **Hypothesis:** creating new multi-field records (entities the model never knew) differs from updating known ones.
- **Method:** insert 6 fictional entities × 3 fields, sequential vs relation-keyed vs batched-joint; measure full-record retention.
- **Criterion:** identify which method gives ≥~90% full-record retention.
- **Verdict:** PROVEN. sequential 0/6, relation-keyed 1/6, **batched-joint 6/6** → batched compile (= spec's L1-buffered batch compile) is required for novel inserts.

### C5 — Edits survive 4-bit quantization
- **Hypothesis:** in-weight edits persist through Q4 (CPU deployment requirement).
- **Method:** edit fp16 → block-wise 4-bit round-trip → re-measure retention/post_p/ppl.
- **Criterion:** retention preserved (≥~90%).
- **Verdict:** PROVEN for edit-survival (100%→100%, post_p 0.98→0.957). CAVEAT: ppl 4.14→9.23 is the crude simulated quantizer; real GGUF-Q4_K UNTESTED.

### C6 — Full CRUD + compaction hold (Qwen2.5 and Qwen3)
- **Verdict:** PROVEN. CRUD INSERT/UPDATE/DELETE ~100% (Qwen2.5) / 6,5,6/6 (Qwen3); compaction-regression 100%→100% both.

### C7 — The recipe transfers to the LARQL-servable model (Qwen3-0.6B)
- **Hypothesis:** results are model-specific, so they must be re-measured on the deployment model.
- **Method:** recompute covariances + hparams for Qwen3; re-run smoke/multi-fact/scale/CRUD/compaction.
- **Criterion:** recipe expresses + clean locality without re-engineering.
- **Verdict:** PROVEN (no recalibration needed): smoke post_p 0.851, multi-fact controls 100% top1, CRUD/compaction pass. Scale: retention holds, control-loc coverage-knob (0.6B collides faster — model-size effect).

### C8 — LARQL serves our externally-edited weights, in-weight, on CPU
- **Verdict:** PROVEN. CPU positive control (Qwen3→Paris clean); decoupled serve of our merged edit; and the **bridge** (`.vlp` overlay → APPLY frozen base → COMPILE) serves France→Berlin 79% via walk-FFN with controls preserved + rollback to Paris. No LARQL code.

### C9 — The spec's FULL contracts are satisfied  ← NOT PROVEN
- **Status:** OPEN. C1–C8 establish write/read/overlay MECHANICS. They do NOT establish: 2PC/State-Ledger consistency (G1), write authorization/audit (G2), deterministic validation pipeline (G3), full query schema incl. DELETE (G4), operator-CPU (G5), efficiency-at-scale (G6), multi-token robustness (G7). **C9 is the council's audit subject.**

### C-D1B1 — Drift is relation-concentration-conditioned, and the law is model-general (D1 + B1)
- **Hypothesis:** held-out same-relation corruption at fixed total edit count is driven by per-relation edit-concentration (not global edge-count), and this holds across model size.
- **Method:** D1 concentration-vs-dilution + dose-response @ fixed total-N (Qwen2.5-3B); B1 ports the dose-response to Qwen2.5-7B (matched). LAW#5 inertness gate each run.
- **Criterion (pre-registered):** corruption rises with capital-edit-count at fixed total-N (concentration drives it); REPLICATE on a 2nd model = monotone + pos-control + expr≥95%.
- **Verdict:** D1 CONFIRM (directional, dual-reviewed, D-D1-1 ⟨D-D1-1@0db8d819⟩); B1 REPLICATE on 7B → law MODEL-GENERAL (D-B1-2 ⟨D-B1-2@0db8d819⟩). Size *threshold* UNRESOLVED — instrument is ~50pp run-to-run nondeterministic (7B seed3 20.8→70.8 on identical-config re-run); 'collapse' was noise, not a tail. → §8.7 structural amendment promotable; numeric threshold needs a lower-variance instrument.


### D-D1-2 ⟨D-D1-2@e023d8d2⟩ — §8.7 numeric-threshold instrument (2026-06-21)
**D-D1-2** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤1`** (max unanchored per-relation concentration; anchor by k=2; WARNING k=2-3, HARD k=8-10 — REVISED down from k≤2 after the seed-2 across-held-out check). Dual-reviewed (Opus advisor + gpt-5.5 cross-family). k=3-4/k=10-12 = scoped order-dominated observations, NOT portable thresholds; per-relation count = fail-closed SENTINEL not the causal var (edit-set/key-collinearity geometry is). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. Artifacts: results/d1_threshold_lowk_3b_s3{,_lowextra}.json, results/d1_instrument_variance_diagnostic_3b_*.json; reviews logs/codex_review_threshold_*OUT.log. **MIXED-LOAD:** pure-capital fails under +12 other-relation load (mixed clean ceiling k=0; driver=other-relation volume) → vindicates the worse-of(global,per-relation) amendment design; pair k≤1 with a global-volume bound + compaction. **SEED-2 (more-toxic held-out):** corrupts at k=1-2 where seed-3 was clean → ceiling k≤2→k≤1; no per-relation count is universally clean (held-out-dependent SENTINEL, not the causal var). +results/d1_mixedload_smoke_3b_s3.json, results/d1_threshold_lowk_3b_s2.json.

### C-R15 — In-weight Constraint-probe firing (R15, D-R15-1)
- **Hypothesis:** a MEMIT edit can install a prohibition that fires (refuses/flags/applies) under the §21.2 adversarial Constraint probe — WEIGHTS-owned, no delegation route.
- **Method:** band[4–8]/3B/AlphaEdit single-batch; 24 fictional subject-property hazard edits (target ' dangerous'); 3-tier firing test (expression/paraphrase/adversarial) + base positive control + global-shift + property-specificity controls; frozen exact_substring flag oracle (disjunctive 'flags' reading) + hand-adjudication + compliance cross-tab. LAW#5 gate ✓ (|Δ|=0.0013).
- **Criterion (pre-reg, `docs/R15_CONSTRAINT_PROBE_PREREG.md`):** PASS if Tier-0 passers show high adversarial flag-rate + large paired Δflag; FALSIFY if Tier-0 passes but Tier-2≈base; controls must not flag.
- **Verdict:** not-ready-with-conditions — cooperative 24/24 vs adversarial ~½ (~7/24 silent leaks); controls clean (interpretable); bounded (easiest single-entity case, relational expected worse). Spec-gap flag (Finding 2, suggestive): disjunctive §21.2 admits warn-and-comply. NOT promoted. Advisor: pre-auth + pivot (R2→R15) + reconcile + calibration/hand-adjudication.

### C-R9 — In-weight deletion residue (R9, D-R9-1)
- **Hypothesis (CHARACTERIZATION):** does a corrective in-weight delete (write-path edit toward pre-write top-1, not snapshot-revert) leave residue resurfacing on a held-out paraphrase neither write nor delete touched?
- **Method:** band[4–8]/3B/AlphaEdit; 24 fictional secrets (single-token code); matched write/delete breadth (both canonical-only); delete on 12, control 12; delete-took gate; top-1+rank+top-5 hand-adjudication. LAW#5 ✓ |Δ|=0.0031.
- **Label pre-committed (advisor R2-redux + spec read):** §11.2 = no class weights-authoritative; no delete-time must-not-fire clause → CHARACTERIZATION not falsification.
- **Verdict:** residue 0/7 (code rank 0→10³–10⁴) — corrective delete suppresses even on untouched paraphrases — BUT easiest case (localized self-made edit); mechanism = overwrite-toward-generic (top-5 filler); 2/12 bystander collateral (G6.1 signature); native-knowledge redaction UNTESTED. Confirms §11.2 overlay-authoritative architecture from the easy end; delete-time-L2 spec-gap. Composes with R15 (easy to remove, hard to make robust). NOT promoted.

### C-C1KVC — Compaction sub-batch K-vs-C interaction (C1-(a), D-C1KVC-1)
- **Hypothesis:** sub-batched compaction reintroduces held-out cross-entity corruption; is it chunk-SIZE / chunk-COUNT / total-N driven? (extends D20, breaks its fixed-N confound attempt)
- **Criterion (pre-reg `docs/C1_KVC_PREREG.md`):** anchor gates (C=N clean at both N); equal-level contrasts refute single-factor-only models; cluster-Welch significance + JS agreement.
- **Verdict:** CHARACTERIZATION — non-additive (N,C) interaction (concentration-alone & sub-batching-alone clean; interaction −25pp, p≤0.001); single-factor-only models refuted; literal size-vs-count UNIDENTIFIED (count=N/C reciprocal); pressures B3N condition 3, not falsified. Advisor+Perplexity cross-family converged. NOT promoted (N≤100/1-held-out/8-ord).

### C-R2 — Reverse-lookup / bidirectional native-knowing (R2, D-R2-1)
- **Hypothesis:** does a forward in-weight edit (C→X, subject-keyed) create a weight-native reverse edge (X→C)?
- **Criterion (pre-reg `docs/R2_REVERSE_LOOKUP_PREREG.md`, label pre-committed CHARACTERIZATION):** ΔP(C) at reverse prompt pre→post + native-reverse positive control + forward-took control; capital↔country only.
- **Verdict:** WRITE-ONLY — max|ΔP|=0.0003 across 24, 0/24 reverse top-1, forward 24/24, control 8/10. Reverse-lookup index-delegated (D16/§11.2); bounds read contract for B3N (weights forward-only). NOT promoted.

### C-R13 — Paraphrase-generalization / editing-overfit (R13, D-R13-1)
- **Hypothesis (reframed):** do in-weight edits fire under NATURAL paraphrase, or only the trained prompt? (pre-reg's storage/behavior framing corrected — both probes behavioral, L1-SELECT index-delegated per CP2)
- **Criterion (`docs/R13_STORAGE_BEHAVIOR_SPLIT_PREREG.md`):** trained-prompt top-1 vs natural-paraphrase top-1; native-paraphrase positive control; distribution headline.
- **Verdict:** trained-prompt 100% → mean ~22% paraphrase (8–42% range; 54% all-fail). Editing-overfit; counterfactual-over-native-prior (R9 fictional 79% vs R13 22%, consistent-with not isolated). Qualifies B3N native-knowing (trained-phrasing only). NOT promoted.

### C-R5 — Native-knowing paraphrase-robustness (R5, D-R5-1)
- **Hypothesis:** does in-weight editing produce usable (paraphrase-robust) knowledge, or trained-prompt parrots? isolate competitor + test recipe-rescue.
- **Criterion (`docs/R5_PARAPHRASE_ROBUSTNESS_PREREG.md`):** held-out P_test firing; 4 arms incl intensity control; mean-rate primary metric.
- **Verdict:** NOVEL robust (16/16); counterfactual-over-prior fragile (0/16, reverts-to-true); diverse recipe partially rescues (→65% mean, 3/16 robust) = diversity not intensity (directional). INSERT improved / UPDATE fragile-partial / overwrite-prior-edit unmeasured. NOT promoted.

### C-C1TS — True-scale C1 substrate feasibility (DIAGNOSTIC, D-C1TS-1)
- **Hypothesis:** is `city→country` a viable substrate to push C1 (B3N cond-3) to the spec's ≥2,000-edit regime with real native knowledge?
- **Method:** native-knowledge screen → N=2,000 single-solve pilot → discriminating N-ladder (multi-token vs single-token subjects). Advisor-steered cheap-gates-expensive.
- **Verdict:** **NON-VIABLE (two editability walls).** Multi-token subjects → ΔW blow-up/garbage (weight-destruction, not corruption); clean single-token subjects → 27–42% expression (counterfactual-over-prior). True-2,000-scale not runnable with this recipe/substrate → C1 substrate-ceiling'd at N≤100. NOT a corruption datapoint; NOT promoted. Pilot-first saved a 4–10-day grid.

### C-C5 — Compaction-verify soundness audit (C5, D-C5-1)
- **Hypothesis:** does compaction output re-pass the Gate/verify-vs-ledger before becoming the active store (the R1-bit/R10 obligation)?
- **Method:** spec-read end-to-end (§8.9/8.10/11.2/11.3/11.5/11.14) + exact-hypergeometric sampling-power calc — analysis, no experiment.
- **Verdict:** **RESOLVED-BY-SPEC-READ + CORRECTION.** The spec MANDATES it (C-OC3: CompactionProbeReport pre-Phase-2, CORE=1.0 abort, atomic 2PC) — the earlier 'unspecified' claim is retracted. Open (analysis): (A) non-CORE `behavior_fail` un-surfaced at read by the tier-blind bit (R13 split reappears); (B) non-CORE sampling-power deficit near thresholds (CORE protected); (C) sub-batched-compaction livelock = prediction→C1-true-scale, NOT concluded. F1 readiness unchanged.

### C-C10b — C10 residual: project-coined multi-word SEMANTIC values (sizing; D-C10b-residual)
- **Hypothesis (FALSIFIER-sizing, can-fail):** realistic project-coined multi-word SEMANTIC values (the in-weight residual after §7.1 routes syntactic values to Git) express as usably as single-token / prior-coherent values at the N≤24 batch path.
- **Criteria (frozen; binding = held-out-paraphrase full-seq; R=min(A6 coined+realNoun, A7 coined-coined)):** RESIDUAL ROBUST iff R≥80 & R−A4≥25; RESIDUAL FRAGILE iff R≤A4+10 or R≤50; else MID-BAND. Sanity: single≥80, coherent≥80, floor≤55.
- **Verdict:** **RESIDUAL FRAGILE.** R=19.4% (A6 30.6 / A7 19.4) ≪ 85% gate; sanity passed (single 98.6, coherent 98.6, floor 45.8). C10 condition CONFIRMED-and-WORSENED. Mechanism = distinct multi-token length-realization wall (canon_full realistic 37–46% vs floor 95.8%), NOT the fit-then-fail parrot; z-probe: compute_z=0.99 all classes @25≈100 → not a *compute_z* knob; bottleneck RELOCATES to W-realization, whose knobs (band/layers/edit-strength) are UNTESTED → AnyEdit CONSISTENT-not-proven-necessary (try a wider/later band first). Continuation prior-coherence mildly protective per-tok (60–72 vs 46) but length-overwhelmed. Advisor before build+verdict; Perplexity cross-family. Scope 3B/band[4-8]/N≤24/1-seed; NOT promotable.

### C-C10 — Multi-token VALUE expression at the batch path (C10, D-C10-1)
- **Hypothesis (FALSIFIER, can-fail):** at the proven N≤100 batch path, multi-token VALUES express as usably as single-token (needed: a local code/project DB holds file paths / identifiers / multi-word concepts).
- **Criteria (frozen + addendum; binding = held-out-paraphrase full-sequence, NOVEL regime, INCOHERENT arm):** SATISFIED iff incoherent ≥85% & (single−incoherent)≤10pp; FALSIFIER FIRES iff single high & (single−incoherent)>15pp.
- **Verdict:** **FALSIFIER FIRES.** 3-arm novel-insert: single 97.2% ≈ prior-coherent multi 97.2% ≫ arbitrary INCOHERENT multi 36.1% (single−incoherent=61.1pp). De-confounded: incoherent first-token 70.8%, conditional P(full|first)=0.51 vs coherent 1.00 → continuation fails to GENERALIZE even given first-token success; edit FITS trained prompt (95.8%) but not paraphrases = multi-token instance of R13/R5 trained-prompt-parrot. Coherent positive control rules out weak-edit artifact; clean fuller LAW#5 gate; base 0/24. C10 = OPEN must-fix for the fixed target (first on-critical-path-AND-failing); fix=AnyEdit per-token. 3 advisor gates + Perplexity cross-family; scoped 3B/band[4-8]/AlphaEdit/N≤100/1-seed/HF-fp16; "cities"=controlled proxy not literal code. NOT promotable as a universal law.

### C-C6L — Ledger-immutability red-team (C6, D-C6L-1)
- **Hypothesis (property demo + spec finding, NOT empirical-red-team):** the ledger is tamper-evident only against naive edits; no operational-window cryptographic tamper-evidence exists; under the spec's own threat model (W3 compromised-Orchestrator) this is security-relevant.
- **Criteria (frozen, symmetric):** K1 rewrite-recompute → verify_chain INTACT (undetected); K2 truncation → INTACT; K4 naive-edit → DETECTED (control); K5 STH-fix → detects K1+K2; K6 spec-audit → is operational-window tamper-evidence unspecified AND security-relevant via the §16.5↔§16.2 seam?
- **Verdict:** **C6 RED-TEAMED (one mechanism).** K1/K2 UNDETECTED, K4 DETECTED, K5 fix works (all vs the real G2 verify_chain). Finding two claims: (A, threat-model-independent) spec mandates NO operational-window crypto tamper-evidence — keyless chain §16.1, anchors only root §13.2 + close §16.7/§27 (elevates CORPUS/11 caveat to spec-level); (B, threat-model-scoped) §16.5 (Orchestrator fs-write) unreconciled with §16.2 (Orchestrator compromise in-scope; §5 physical-only) → W3 entry rewritable = unreconciled threat-model seam. Fix = STH head-anchor (custody-compatible §20.2). Advisor corrected a first-pass "self-undermining gap" over-claim → named-the-covering-clause framing. NOT a spec falsification, NOT promotable; sharpens C6 (stays open).

### C-R11 — Content-scoped authoritative-medium & severity ON READ (R11, D-R11-1)
- **Hypothesis (spec-coherence, NOT a falsifier):** does the spec's read surface determine (a) authoritative-medium/content-class and (b) divergence severity AT READ?
- **Criterion (frozen):** per content-class under injected Git↔.vindex divergence, score COHERENT / DELEGATED-COHERENT / DERIVABLE-IF-TYPE-RETURNED / SPEC-GAP using ONLY the cited read-surface inventory. Symmetric (a missed read-result field flips toward COHERENT).
- **Verdict:** **COHERENT via derivation + prevention.** (a) wrong-medium-on-read foreclosed by §11.3/D43 strong-consistency prevention + §11.8 system-wide trip; (b) class=f(entity_type) §11.2 and severity=§11.7's class-function → DERIVABLE-IF-TYPE-RETURNED (§7.2/C4 mandates typed entities). Advisor corrected a first-pass 3-gap over-claim (silently assumed reads don't return type): read-RETURN shape is unspecified → R11 restates the ONE known root gap ('no formal query-language section'), NOT new F1 conditions (don't double-count). Honesty: runner output = documentation echo of the spec read, NOT an independent check. Spec rec: pin the query-result schema to return entity_type. NOT a falsifier (matrix ③), NOT promotable.

### C-R1-bit — Commit-bit SELECT read-back, commit-time (R1-bit, D-R1-2)
- **Hypothesis:** recording persistence in a G1 2PC commit-status bit (not weights) delivers the §8.9 L1 read-back, bleed-immune.
- **Criterion (frozen, CP-class):** D1 LANDED 8/8 · D2 LEAK NULL 6/6 · D3 REJECTED NULL 4/4 + DROPPED NULL 2/2 via 2PC-abort · D4 ≥1 proxy-TRIPLE→bit-NULL row · D5 chain intact + no bypass.
- **Verdict:** **DELIVERED-FOR-SCOPE (commit-time)** — all met; Velloria phantom read fixed (proxy 2.06→bit NULL). Scope = commit-time only; post-commit divergence (R10/§11.3/D43) deferred to C1, NOT solved. CP-class, not promoted.

### C-R1 — Deployed SELECT triple-readback (R1, D-R1-1)
- **Hypothesis:** a ledger-backed SELECT reconciled vs the deployed store DELIVERS the §8.9 L1 read-back on divergence cases bare weights fail.
- **Criterion (frozen pre-reg):** P1 LANDED≥7/8 · P2 LEAK NULL 6/6 (anti-firing) · P3 GATE-REJECTED NULL 4/4 + DROPPED flagged 2/2 · no LEAK/REJECTED/DROPPED returns a triple (`hard_fail`).
- **Verdict:** **NOT-DELIVERED / CHARACTERIZATION** — anti-firing solid (LEAK 6/6 NULL while model fires 5/6; REJECTED 4/4; LANDED 8/8) but the novel divergence test FAILED (DROPPED 1/2: phantom read Velloria→Tokyo from +2.06-nat cross-entity bleed over frozen thr 2.0). In-weight logprob storage-signature UNSOUND (bleed-noise-limited). Confirms B0/§11.2 (ledger must carry commit-status); NEW gap: post-commit divergence-detection unspecified, 2PC commit-bit covers commit-time only. NOT promoted.

### C-R5b — Overwrite-prior-edit / axis=pretrained-prior (R5b, D-R5b-1)
- **Hypothesis:** is overwriting a prior `.vindex` edit fragile (entrench) or robust (localize)? populate the unmeasured update cell.
- **Criterion (`docs/R5B_OVERWRITE_PRIOR_EDIT_PREREG.md`):** 3 arms NOVEL/PRIOR/OVERWRITE-EDIT, held-out P_test firing + v1-resurface.
- **Verdict:** OVERWRITE-EDIT 93.8%≈NOVEL≫PRIOR; v1 doesn't resurface → discriminating axis is PRETRAINED-prior presence not prior-edit; real-subject-re-edit cell UNMEASURED (predicted ≈PRIOR). F1: robust IFF no entrenched pretrained competitor. NOT promoted.

### C-C10e — C10 band-knob / W-realization layer shift (D-C10e-bandknob ⟨D-C10e-bandknob@82b491dc⟩)
- **Hypothesis:** if CORPUS/36 is mainly a W-realization band placement problem, moving from baseline `[4,8]` to later `[8,12]` should materially rescue the hard A7 coined-coined arm while A1/A2 controls remain high.
- **Criterion (frozen in `docs/C10_BANDKNOB_PREREG.md`):** behavioral rescue requires later A7 `para_full` at least 50 with canon diagnostic at least 80; W-realization-only requires a large canon gain while para stays sub-gate; invalid if controls fail or baseline does not reproduce the failure envelope.
- **Verdict:** **NO MATERIAL KNOB RESCUE.** Controls pass (A1/A2 later 97.2/91.7); baseline A7 in failure envelope (para 13.9, canon 29.2). Later band A7 canon rises only to 45.8 and para worsens to 5.6. Pure later-band W-realization is eliminated; broader W knobs and AnyEdit remain open. NOT promotable.

### C-C10f — C10 widened-band [4,12] recipe knob (D-C10f-band412 ⟨D-C10f-band412@d93d6a19⟩)
- **Hypothesis:** if CORPUS/36 is mainly a W-realization band-width problem, widening baseline `[4,8]` to `[4,12]` should materially improve the hard A7 coined-coined held-out readout while A1/A2 controls remain viable.
- **Criterion (frozen in `docs/C10_BAND412_PREREG.md`):** headline criterion is A7 `para_full`; no closure below 85; behavioral lead requires delta >=25pp and para>=40; W-realization-only requires canon gain >=20 with para<50; tradeoff if controls fall below 80.
- **Verdict:** **NO MATERIAL KNOB RESCUE.** Valid run: LAW#5 passes; baseline reproduces failure; A1/A2 wide controls stay above floor (90.3). A7 `para_full` worsens 11.1→6.9 and canon improves only 29.2→41.7. This `[4,12]` recipe at tested strength/hparams fails; C10 remains open; NOT promotable.

### C-C10g — C10 edit-strength/layer-count sweep (D-C10g-strengthlayers ⟨D-C10g-strengthlayers@d691acab⟩)
- **Hypothesis:** after later-band and widened-band failures, a small MEMIT edit-strength/layer-count sweep might rescue hard project-coined multi-word values before AnyEdit.
- **Criterion (frozen in `docs/C10_STRENGTH_LAYER_SWEEP_PREREG.md`):** binding lead/rescue metric is held-out A7 `para_full`; canonical gains are diagnostic only; A1/A2 controls must remain clean; after the three candidates stop and choose AnyEdit or accept-bounded unless a behavioral lead appears.
- **Verdict:** **NO BEHAVIORAL RESCUE WITH ONE NON-VIABLE TRADEOFF.** Baseline A7 `para_full` 20.8 (15/72); strength150 `[4,12]` 13.9 (10/72) with clean controls; lowcov2500 `[4,12]` 5.6 (4/72) with clean controls despite canon 45.8; deep `[4..12,18..22]` canon 58.3 but A7 `para_full` 0/72 and A1/A2 collapse to 37.5/22.2. LAW#5 passes all recipes. Bounded pre-AnyEdit MEMIT knob pass is closed for this scope; C10 remains open; NOT promotable.

### C-C10h - C10 AnyEdit small-window pilot (D-C10h-anyedit-pilot ⟨D-C10h-anyedit-pilot@6413cc67⟩)
- **Hypothesis:** a local AnyEdit-style autoregressive per-token/window target construction can rescue hard project-coined multi-word A7 values after cheap MEMIT knobs failed.
- **Criterion (frozen in `docs/C10_ANYEDIT_PILOT_PREREG.md`):** embedded token/window alignment gate; no-op inertness; same-run baseline must reproduce easy A1/A2 and A7 failure; AnyEdit must improve A7 held-out `para_full` without damaging A1/A2 controls.
- **Verdict:** **TRADEOFF_NOT_CLEAN_RESCUE.** Gates pass, but AnyEdit `window_size=1` collapses A1/A2 held-out `para_full` from 93.1/97.2 to 0.0/0.0 and worsens A7 `para_full` from 12.5 (9/72) to 1.4 (1/72). Scoped local small-window transplant killed; upstream-equivalent AnyEdit remains open.

### C-C10k-s0 - C10K Stage 0 hardware/source-faithfulness (D-C10k-m3pro-stage0 ⟨D-C10k-m3pro-stage0@43899c7f⟩)
- **Hypothesis:** official AnyEdit can execute source-faithfully on the current science hardware (prereg Stage 0).
- **Method:** desk check of the pinned upstream + first-failure trace on a tiny random model (no science model, no C10 data).
- **Measurement:** first live failure frame; count/bin of device bindings; runner completeness; env/config desk checks.
- **Criterion (prereg item 2):** runs without unapproved source/VRAM patches → else `HALTED - HARDWARE_ENVELOPE`.
- **Verdict:** HALTED - HARDWARE_ENVELOPE (+UPSTREAM_ENV_UNDEFINED). Not a method verdict. Operator fork A/B/C.

### C-C10k-ra - C10K Route A ported AnyEdit controls (D-C10k-route-a ⟨D-C10k-route-a@3b0be47e⟩)
- **Hypothesis:** the official AnyEdit modules, ported device-only and run on Qwen2.5-3B base, recover the A1/A2 controls (`para_full ≥ 80`) and can then be read on A7.
- **Method:** prereg + 3 amendments; projector gate v2 + controls; D5 anchor; R0 LAW#3; R1 controls at L2=10, one fix (L2=0.01) and rerun; back-test of the solve; A7/memit_ARE diagnostic-only.
- **Measurement:** canon/para full-sequence hits, locality (real-country, JS, stock item, generic NLL), band norms, realised-residual fractions, hidden-state transfer.
- **Criterion (prereg §3):** A1 and A2 `para_full ≥ 80` after at most one localized fix → else HALTED.
- **Verdict:** HALTED — CONTROLS_NOT_RECOVERED (0/72 both arms at both ridges; trained prompt 24/24 after the fix). Mechanism: last-prompt-token keying, ~0 paraphrase transfer.

### C-C10k-ka - Keying-locus ablation (D-C10k-keying-ablation ⟨D-C10k-keying-ablation@110558e3⟩)
- **Hypothesis:** keying the write at the prompt's final token (instead of the subject's last token) removes held-out-paraphrase generalisation in the program's own MEMIT engine.
- **Method:** 2×2 (key locus × context templates) on A1/A2, N = 24, same engine/covariance/ridge/band; K1 as LAW#3 gate; validity = canon ≥ 90 + keyed-token + identical eval strings. Then (§6b) z-probe, key Gram matrices, N = 1 singles × 6 subjects × both loci, frame-bleed probe on 12 real + 6 bystander frame prompts.
- **Criterion:** §3 SUFFICIENT needs valid K3/K4 < 20 with K2 ≥ 80; §6b SUFFICIENT (N = 1) needs ≥ 5/6 landed last-token singles with ≤ 1/3 paraphrases and ≥ 5/6 subject singles with ≥ 2/3; frame-bleed H-frame = ≥ 6/12 real and ≥ 3/6 bystander flips vs ≤ 1 for the control.
- **Verdict:** N = 24 INVALID (near-collinear keys; ridge not separable); N = 1 F3 SUFFICIENT (MEMIT, N = 1); frame-bleed BETWEEN (partly frame-keyed) → last-token-keyed writes land but do not transfer; partly frame-keyed (F3 SUFFICIENT in MEMIT, N = 1).

### C-C10l-cg - Solve geometry and sparse layer sets (D-C10l-covgeom ⟨D-C10l-covgeom@af2e38f7⟩)
- **Hypothesis:** H-I8 (the null-space projector starves canonical realisation and/or paraphrase transfer; P := I fixes it) and H-I9a (a two-layer set spreads the residual less and fixes it).
- **Method:** harness knob `C10_PROJECTOR=identity` (candidate recipe only) and hparams `layers [4,8]` / `[7,8]`, each against arm A in the same run; P6 z-injection ceiling; sequential offline step 0; S-3 axes L1 / described_as / L3 beside every count.
- **Criterion (prereg §5):** PASS ≥ 61/72, LEAD ≥ 30/72 with L1 ≤ A+1, described_as ≥ A−3, L3 ≥ 29/30; REALISATION-ONLY canon ≥ 15/24; else NULL; INVALID on envelope / P3(a) / L3.
- **Verdict:** NULL ×3 (8, 13, 13 of 72 vs 13, 10, 13); ceiling admits LEAD (49/72); both step-0 predictions failed behaviourally.

### C-C10l-mt - Minted token per coined value (D-C10l-mint ⟨D-C10l-mint@a4a6f4c7⟩)
- **Hypothesis:** C10's wall is the span (a 4–6-token value) rather than the novelty; one minted token per coined value removes the span and approaches A1.
- **Method:** 24 tokens registered in the spare embedding rows (no resize), inits M/G/N/Z with I-11 and P-iv probes, P3 per init; arms A7-multi, A1, A1-rare, mint-G, mint-N on the unmodified harness; binding = post-write top-1 id minus step-0.
- **Criterion (prereg §6, B1):** SPAN ≥ A1−5 and ≥ 30/72 with locality, sibling ≤ 3, cannibal ≤ 2; PARTIAL 30 ≤ x < A1−5; NOVELTY < 30; INVALID on envelope / A1 / P2 / P3 / L3.
- **Verdict:** PARTIAL ×2 (G 39/72, N 46/72; canon 24/24; sibling 0; cannibal 0; locality clean); G ≈ N branch; A1-rare 25/72 → implausibility alone costs two thirds of transfer.
- **B2/B3 addendum (2026-10-05):** replicates G 38, N(seed 0) 42, N(seed 1) 34, A1-rare 29 → rule 1 (N − G ≥ 5 in both) UNSUPPORTED (−4 in replicate 2), rule 2 (min(mint) − max(rare) ≥ 10) UNSUPPORTED (5); PARTIAL reproduced ×5. P4: both GGUFs tokenise 24/24; fp16 GGUF top-1 id parity 148/148; Q4_K_M retention canon 1.000, para 0.738; locality intact → compiled-artefact gate PASS (`p4_verdict.json`).
### C-C10m-dg - Diagnostics: read partition, edit + inject, third seed (D-C10m-diag ⟨D-C10m-diag@9a9b5343⟩)
- **Hypotheses (prereg §1):** Q1 DRIFT / CHAIN / ABSENT partition of the A7 residual; Q2 H1 collateral vs H2 read-differently; Q3 seed effect vs spread.
- **Method:** one run, baseline recipe, arms A1 + A7; pre-edit zs at layer 8 and an in-process injection control (gate ≥ 44/72, ≥ 22/24); post-edit hook: constrained read, edit + inject with z_pre (binding), recomputed z_post (secondary); third N seed through step 0 + arm.
- **Criterion (prereg §3 v2):** DRIFT if gain ≥ 15 (LEAD if C ≥ 30); CHAIN-PRESENT if gain ≤ 5 and ≥ 8 high-TF failing subjects (DOMINANT ≥ 13); ABSENT otherwise at gain ≤ 5; H2 if K_post ≥ 20 and P_post ≥ P_pre − 10; H1 if K_post ≤ 12 or P_post ≤ E + 10; SEED-SENSITIVE if three-seed range ≥ 10.
- **Verdict:** Q1 ABSENT-DOMINANT (gain 2; 3 subjects); Q2 H1 (K_post 7; P_post 23 vs P_pre 51, E 15); Q3 SEED-SENSITIVE (range 12). Run 2 binding; run 1 INVALID on a truncated fingerprint line (no label; counts agree within 2–6/72).
### C-C10n-zt - Target transport under the edit (D-C10n-ztransport ⟨D-C10n-ztransport@982edcbd⟩)
- **Hypotheses (prereg §1):** DRIFT (each target works only on its own model) vs TARGET-PORTABLE (z_post also works on the unedited model).
- **Method:** one process; z_pre and cell A pre-edit; z_post, cells B and C inside the post-edit hook; full cell-A repeat on the restored weights, then cell D; per-subject norms, displacement, cosine. N1: the control level is a stratum (HIGH ≥ 44 / LOW 38–43), not a floor.
- **Criterion (prereg §3 v2 + N1):** DRIFT if D ≤ A − 20; TARGET-PORTABLE if D ≥ A − 10; INDETERMINATE between; replication clause B ≤ A − 20 and C ≥ A − 10, promotable only in HIGH-CONTROL.
- **Verdict:** TARGET-PORTABLE (D 37 ≥ 32) in a LOW-CONTROL process (A 42) → reported, not promoted; cells reproduced (B 13, C 61). Run 1 INVALID (control 42 < v2's 44 floor; the halt that produced N1).
### C-C10o-md - Magnitude vs direction on the edited model (D-C10o-magnitude ⟨D-C10o-magnitude@31389765⟩)
- **Hypotheses (prereg §1):** which component of the re-solved target restores decoding on the edited model — magnitude (E1), unit direction at the original norm (E2), or the rotation with the original projection kept (E3).
- **Method:** one process; z_pre and cell A pre-edit; z_post, B, C, E1, E2, E3 in the post-edit hook; full cell-A repeat on restored weights, then E1′/E2′/E3′; rotated population by displacement > 0.30 with a [0.25, 0.35] buffer-zone sensitivity read.
- **Criterion (prereg §3 v2):** recovered fractions f = (E − B)/(C − B) on the rotated population, contrast ≥ 20; MAGNITUDE f1 ≥ 0.6 & max(f2, f3) < 0.3; DIRECTION f2 ≥ 0.6 & f1 < 0.3; ROTATION-WITH-PROJECTION f3 ≥ 0.6 & f2 < 0.3 & f1 < 0.3; EITHER; NEITHER-ALONE; MIXED. Routing labels only.
- **Verdict:** DIRECTION (f1 −0.023, f2 0.636, f3 0.932; contrast 44) in a HIGH-CONTROL process; buffer empty; → two-pass solve arm next.
### C-C10p-tp - Two-pass solve (D-C10p-twopass ⟨D-C10p-twopass@12f87dc3⟩)
- **Hypotheses (prereg §1):** H-P1 an edit aimed at z_post transfers better; H-P0 null; H-P2 trade-off (larger residual → larger ΔW, locality cost).
- **Method:** one process, three full harness passes (baseline / sham aimed at z_pre / two-pass aimed at z_post), arms A1 + A2 + A7, S-3 axes + same-frame fictional probe (6 never-edited subjects), ΔW norms, seam consumption audit.
- **Criterion (prereg §3 v2):** validity incl. sham inert (± 5/72, ± 3/24, ΔW 5 %) and hits 0/1/1; locality gates A1/A2 ≥ 68, L1 ≤ +1, described_as ≥ −3, L3 ≥ 29, ppl ≤ +0.5, frame ≤ +1; LEAD ≥ 30/72 with gates; PARTIAL gain ≥ 10 with gates; TRADEOFF gain ≥ 10 without; NULL otherwise; -LARGE-WRITE if total ΔW ratio > 1.5.
- **Verdict:** NULL (21 vs 13, gain 8); described_as gate missed by 0.08; ΔW ratio 1.31; sham identical → seam inert. H-P0 at the margin; H-P2's cost visible on one axis.
### C-C10q-st - Stacked two-pass solve (D-C10q-stacked ⟨D-C10q-stacked@8e5c7f12⟩)
- **Hypotheses (prereg §1):** H-Q1 stacked helps; H-Q0 null; H-Q2 trade-off; sham expectation = a second edit at z_pre adds almost nothing.
- **Method:** one process, three full harness passes (S aimed at z_post / S-sham aimed at z_pre / S-perm aimed at the next subject's z_post), arms A1 + A2 + A7, S-3 axes + same-frame probe, per-pass ΔW₁/ΔW₂, seam consumption audit; run 1 crashed after pass S (bookkeeping) and is an echo only.
- **Criterion (prereg §3 v2 + Q1):** validity incl. per-arm controls ≥ 68, reference envelope, hits 0 → 1 → 1, reference spread ≤ 5, rotated ≥ 12, same-frame n = 6; sham scope ± 5 and ΔW₂ ≤ 0.25 ΔW₁; locality gates L1 ≤ +1, frame ≤ +1, described_as ≥ −3, L3 ≥ 29, ppl ≤ +0.5; LEAD ≥ 30/72 with gates; PARTIAL gain ≥ 10 with gates; TRADEOFF gain ≥ 10 without; NULL; -LARGE-WRITE at ΔW₂/ΔW₁ > 0.75 (prose; reader on LEAD/PARTIAL only — Q2); -SHAM-ACTIVE; -NOT-TARGET-SPECIFIC only if S-perm matched (×1.5) and gain_perm ≥ 0.5 × gain; -PERM-UNMATCHED.
- **Verdict:** TRADEOFF-PERM-UNMATCHED (24 vs 12, gain 12; described_as −4.22; ratio 1.24; sham inert 0.020; S-perm 0/72 at 1.91, ratio-of-ratios 1.54). H-Q2's cost on one axis; no target-specificity claim.
### C-C10s-sz - Shared-z target, step 1 (D-C10s-sharedz ⟨D-C10s-sharedz@bee04393⟩)
- **Hypotheses (prereg §1):** H-S1 frame (a z fit to three phrasings transfers to the held-out phrasings better than the canonical z, same write size and locality); H-S0 null (the prior, CORPUS/46 F-D1); H-S2 trade-off.
- **Method:** one process; LAW#5 inertness (i)–(v) as amended by §7 A2 v2 (same-batch engine parity for (iii)/(iv)); cell 1 = injection screen in the unedited model (canonical, shared and noise-twin targets; 24 A7 facts × 3 held-out templates) with the per-frame fit diagnostic and control c; cell 2 (harness pass) only if cell 1 advances.
- **Criterion (prereg §2 cell 1, §3, §7 A2):** precedence UNDERFIT (any training-frame fit < 0.98 at stop) > NOISE-NON-DISCRIMINATING (|twin gain| ≥ 6) > screen (shared − canonical ≥ 6/72, on ≥ 2 templates and ≥ 4 subjects); write-arm labels LEAD / PARTIAL / TRADEOFF / NULL with replication.
- **Verdict:** UNDERFIT (18 entries < 0.98, min 0.8437) → inconclusive under this solve budget; write arm not run; H-1 unresolved. The first inertness run (HALT on (iii)/(iv)) is a non-binding echo.
### C-C10s-sf - Shared-target solve feasibility (D-C10s-solvefeas ⟨D-C10s-solvefeas@7083a102⟩)
- **Hypothesis (prereg v2 §0–1):** H-C10s-solvefeas — step 1's underfit is a solve-budget limit: with the cap 25 → 50 evaluations (radius, frames, held-out set, KL/weight-decay and the engine's stopping rule fixed) every subject/frame fit reaches 0.98.
- **Method:** one process; step 1's inertness (§7 A2 v2) plus a larger-budget positive control; cell 1 = the step-1 injection screen with a same-run evaluation-25 snapshot (prereg §2); cell 2 only if the fit gate passes.
- **Criterion (prereg §3):** every subject/frame context-averaged teacher-forced fit ≥ 0.98 at the stop, else UNDERFIT-AT-50 qualified by the stopping class of the residual entries.
- **Verdict:** UNDERFIT-AT-50, qualified objective-stopped (2 entries < 0.98 at the stop, min 0.971150, both stopped on the averaged loss rule at evaluation 27; 29 → 2 in the same run); write arm not run; H-1 unresolved.
### C-C10t-sk - Value-internal second key, step 2 (D-C10t-secondkey ⟨D-C10t-secondkey@76a722d3⟩)
- **Hypotheses (prereg v2 §1):** H-T1 direct address (a second key at a value-internal position with its own remainder target raises held-out recall over the same-run single key and the duplicated-canonical control, locality held); H-T0 null (the prior); H-T2 bleed / subject-free; H-T3 request count; H-T4 key side.
- **Method:** step 0 selects one admitted position per fact (surprisal B10 / leverage B5, spending screen; p5 from the raw five-layer mean per D-C10t-p5rule); one process, arms A1, A2, A7-single, A7-dup (canonical requests twice) and A7-second-B10 (48 requests), held-out full sequence plus per-prefix F1 locality on six never-edited subjects; the first pass-1 attempt HALTED (float64 on MPS) and is a non-binding echo.
- **Criterion (prereg §3):** validity (A1/A2 ≥ 68, reference inside [5,18]/72 and [5,10]/24, LAW#5, observer, admission); LEAD ≥ 30/72 with locality; PARTIAL 18 < count < 30 and gain ≥ 10 over the same-run reference with locality; TRADEOFF that size without locality; else NULL; -LARGE-WRITE at summed write-norm ratio > 1.5.
- **Verdict:** NULL-LARGE-WRITE (23 vs 15/72, +8 < 10; ratio 2.05; ten of 24 per-prefix gates fail; duplicate control null); candidate not advanced; no replication pending; H-10/H-5 not closed.

### C-C10u-m2 - Two-token and modifier-only mint, step 3 attempt r3 (D-C10u-mint2 ⟨D-C10u-mint2@d1299b2b⟩)
- **Hypotheses (prereg v3 §1, §3):** H-19 two minted ids per value (block V2: SPAN-DIRECTION vs PAIR-DIRECTION); block F: minting the modifier alone reaches the one-token mint's transfer (MODIFIER-RECOVERY) or does not (NO-MODIFIER-GAIN).
- **Method:** two never-pooled blocks, each an A7-multi reference + mint-1 + the candidate at seeds 0/1/2 on a frozen context set; step-0 fit screen (≥ 22/24 aggregates ≥ 0.98) for mint arms; block F's mint-1(frozen) = CORPUS/45's recipe as the LAW#3 reproduction gate; amendment A-env baseline window [5, 18] / [5, 10] / [42, 59]; a replication block for any LEAD or direction label (V2's waived post-observation, D-C10u-r3skipV2).
- **Criterion (prereg §3, §8):** per arm LEAD ≥ 30/72 / PARTIAL gain ≥ 10 / NULL band [11, 18] / TRADEOFF; direction labels only for a valid, fully fit, locality-clean, replicated block; a failed fit screen → UNDERFIT and the block ROUTING-BLOCKED-UNDERFIT; a failed V2 screen → NOT-COMPARABLE.
- **Verdict:** CLOSED, operator-ratified (r3 ratified 2026-10-07 ~21:08 MDT, D-C10r-rulings-12; prereg :172) — no direction reading on either block: F ROUTING-BLOCKED-UNDERFIT (modifier-only 17/13/14 of 24 on the screen; the in-block multi reference 17/24 on the same screen; not run), V2 NOT-COMPARABLE (31/72, canon 24/24); LAW#3 reproduction passed (mint-1(frozen) 46/37/40 vs 14/72); P4 not triggered; H-19 not closed.

### C-C10w-or - Ceiling oracle, step 5 — final replicated reading (D-C10w-oracle ⟨D-C10w-oracle@6a735469⟩)
- **Hypotheses (prereg v2.2 §1):** H-W1 a merged rank-16 band-LoRA reaches ≥ 61/72 with every locality and forgetting gate holding; H-W0 recipe-level negative; H-W2 the bar only at a locality or forgetting cost; H-W3 continuation leakage (BIGRAM diagnostic). Oracle measurement, not a route.
- **Method:** LoRA on `down_proj` L4–8, every value token in the loss, 20 sealed training phrasings; P1 = seed 0: O-A1, O-A2, O-A7, matched O-A7-shuf, single-frame O-A7-canon, scored in one process against the same-process closed form and arm U; P2 = seed 1 + same-seed retrain; P3 (rank 64) conditional.
- **Criterion (prereg §3):** validity first; per configuration PASS-CEILING ≥ 61 with G1–G7, PARTIAL-CEILING-LOCALITY-COST ≥ 61 with a gate miss, PARTIAL-CEILING 30–60, FAIL-CEILING < 30; replication over two seeds (min count, union of gate misses) before any label routes.
- **Verdict:** PARTIAL-CEILING-LOCALITY-COST(G4,G6), BIGRAM — replicated min(70, 71) = 70/72 ≥ 61 with G4 missed at both seeds and G6 at seed 1; stable (seed gap 1; retrain 70 → 70); P3 excluded after LOCALITY-COST; split NOT-READ (c); NO-GATE-CLEAN-REFERENCE; routing INDEPENDENT-PREREG-ONLY. Consistent with H-W2 (the bar only at a locality or forgetting cost); H-W1 not shown. Detail: CORPUS/57 (P1 interim CORPUS/55; P2 eval re-run under D-C10w-p2rerun). H-13 measured; not a route.

### C-C10v-lp - Per-fact layer pick, step 4 pass1 (D-C10v-layerpick ⟨D-C10v-layerpick@3bcae852⟩)
- **Hypotheses (prereg v2 §1):** H-V1 placing each fact at the band layer with the largest lone-write coefficient G raises A7 held-out recall over the band (A), a fixed layer 8 (B0) and a shuffled map (Bshuf); H-V0 null (prior); H-V2 trade-off.
- **Method:** step 0 computes G per fact and layer twice (δ = largest change) and fixes the argmax map; one process runs A, B0, B, Bshuf with A1, A2, A7; LAW#5 (i)–(v); pass2 only for PARTIAL or LEAD on B or B0.
- **Criterion (prereg §3):** validity first; LEAD ≥ 30/72; PARTIAL > 18 and ≥ +10 over A; a count in [5, 18] is NULL; the selector is credited only if B beats B0 and Bshuf by ≥ 10.
- **Verdict:** NULL — not advanced under the preregistered rules (B 12, A 11, B0 12, Bshuf 10 of 72; B missed described_as; replication not triggered). Detail: CORPUS/56. H-8 not closed.

### C-C10x-ep - Engine-path target construction, step 6 (D-C10x-enginepath ⟨D-C10x-enginepath@a8c22280⟩)
- **Hypotheses (prereg v2.2 §1):** an FE-inspired target (z at layer 4, replayed targets, layer-local residuals, undivided updates; I-2) or an OverTone-inspired target objective (I-1), each written by the unchanged projected-ridge solve, raises A7 held-out recall over the same-process band 4–8 (A) with controls and locality held; H-X-tradeoff (a gain at a locality, control or write-size cost); null.
- **Method:** one process: recipe A (LAW#3 gate in the driver), targets, inertness (G8, X1, X2), injection screen, I-2, I-1, each with A1, A2, A7; process 2 only for an unqualified LEAD or PARTIAL.
- **Criterion (prereg §3):** validity first; controls A1, A2 ≥ 68 per recipe else INVALID-CONTROLS; LEAD ≥ 30/72; PARTIAL > 18 and ≥ +10 over A; a count ≤ 18 is NULL; locality gates vs A; qualifiers -LARGE-WRITE (> 1.5) and -UNDERFIT (I-2); the NULL table reads the injection deficit d.
- **Verdict:** I-1 NULL (17 vs 12/72; d = −4, non-interpreted); I-2 INVALID-CONTROLS-UNDERFIT (erratum: CORPUS/58; this FE package failed A1/A2 in this run: 64, 65; fit 3/24 ≥ 0.98 against 22/24); no arm eligible, process 2 not run; reader VALID, Astra CONFIRM. Detail: CORPUS/58 (re-run 3 under D-C10w-p2rerun). H-11 not advanced on this harness; no mechanism or method-family conclusion.

## 2026-10-09 — V7 diagnostic and MathLab milestones

D-C10z-v7diag ⟨D-C10z-v7diag@d8c55e7b⟩ frozen routing selects A1; D-C10z-a1pop ⟨D-C10z-a1pop@1ef441d3⟩ continuation prepared, candidate/deployment UNVERIFIED → CORPUS/59_C10Z_V7DIAG_A1.md.

D-ML-1 ⟨D-ML-1@12c5548b⟩ harvest/admission milestones; D-ML-2 ⟨D-ML-2@99a9fb4c⟩ gate 2a PASS/2b OPERANDS-ONLY; D-ML-3 ⟨D-ML-3@84e9d0e1⟩ contract corrected; MATH-PROXY only → CORPUS/60_MATHLAB_HARVEST_REPLAY.md.

## 2026-10-09 — MathLab calibration stop (supersedes the interim milestone status)

D-ML-1 ⟨D-ML-1@46230e48⟩ **STOPPED — calibration FAIL**; D-ML-4 ⟨D-ML-4@46230e48⟩ step 4 **SHELVED**; NEW-1 adapter geometry continues separately under its own gates. MATH-PROXY only; F1 unchanged → CORPUS/60_MATHLAB_HARVEST_REPLAY.md#2026-10-09-addendum--harvest-2-calibration-fail-lab-stopped-d-ml-1--d-ml-4.

## 2026-10-10 — ASTRA attempt-4 final disposition

D-C10z-a4 ⟨D-C10z-a4@e0a21d13⟩ **DONE — UNDERFIT-LARGE-WRITE-SUBJECT-FREE-STAGE1** (inconclusive under this solve budget; terminal under current authorization), Astra CONFIRM → CORPUS/61_C10Z_ATTEMPT4_UNDERFIT.md.

D-C10z-a1pop ⟨D-C10z-a1pop@1ef441d3⟩: preparation/admission preserved; current continuation CLOSED by D-C10z-a4 ⟨D-C10z-a4@e0a21d13⟩ → CORPUS/61_C10Z_ATTEMPT4_UNDERFIT.md.


## 2026-10-10 — Projector-fidelity qualification (D-NEW1-fid)

| Decision | Recorded qualification | Detailed source |
|---|---|---|
| D-NEW1-fid ⟨D-NEW1-fid@341707a8⟩ | Native-projector fidelity warning RECORDED; CORPUS/44 “null-space share” qualified append-only; actual rounded-P distance, update-weighted leakage and locality UNMEASURED; behavioral verdicts and F1 unchanged | [B measurement report — D-NEW1-fid warning](../results/mathlab_staging/new1_v2_build_report.md#d-new1-fid) |


⟨D-C10l-covgeom@0caeca4f⟩

## 2026-10-10 — NEW-1 construction diagnostic status (D-NEW1-b)

| Decision | Recorded status | Detailed source |
|---|---|---|
| D-NEW1-b ⟨D-NEW1-b@d5e2baff⟩ | FIX5 qualified on host; Astra r7 GO-OPERATOR; real diagnostic UNRUN, operator authorized ONE run 2026-10-10 (f5dbab5), dispatch pending a quiet host. No science verdict; F1 unchanged | [FIX5 host qualification README](../results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/host_prequal_maestro21/README.md); [Astra r7](../results/mathlab_staging/new1_construction_diag_astra_r7.md) |
