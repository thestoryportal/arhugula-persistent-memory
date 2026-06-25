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
