# Write-Engine Viability Determination — Comprehensive Experimental Program
# Mandate (operator, 2026-06-17): "work through all necessary experiments comprehensively in order to genuinely prove or disprove viability of implementing the specification."
# Supersedes the single-session S2.41 kickoff. Engine UNMODIFIED unless a phase explicitly modifies the science path (then LAW #5 isolation applies).

## The viability question (precise)
The v1.2 spec (`research_and_specs/llm-as-database-v1_2-integrated-spec.md`) is **in-weight** (§1: in-weight learning, NOT RAG), **MEMIT-designated** (D12/§8.2: ROME/GRACE/FT excluded), over an **entity-centric data model** (§7.2–7.3: many relations per entity). Therefore the load-bearing requirement is **same-entity multi-attribute locality**: editing one attribute of an entity must not corrupt that entity's OTHER attributes. This program determines whether that is achievable in-weight (spec stands, possibly with a D12 *amendment*) or not (D12 *revisit* → parameter-preserving pivot → v1.3).

## What is already established (do not re-litigate)
- **Gate A (S2.40, PDF-/run-verified):** GPT-J — canonical clean MEMIT model — is effective + cross-entity-specific (KL≈0) but NOT same-subject-local (drift 2.48). The MEMIT paper's NS metric is cross-entity only; same-entity locality is unmeasured by the lineage.
- **Literature (`s240_literature_scan.md` + `research_and_specs/llm-knowledge-editing-same-entity-locality.md`):** same-entity failure is mechanistic and model-general — ROME/MEMIT key at `subject_last`, so an entity's attributes share ~one key ("related knowledge perturbation", NAACL 2025; MEMIT-Merge 90%→50%; BlackboxNLP subject-sharing poorly preserved). Same-entity locality is solved only by parameter-preserving methods (SERAC/GRACE ~99–100%) or, in-weight, partially by DiKE (representation disentanglement). AlphaEdit null-space helps but its P is cross-entity.
- **Implication:** the planned S2.41 MODEL×CORPUS cross (X1) is low-information — the research predicts H-PROBE/model-general (cfb-v4's low drift was attribute-selection luck, "Flex Tape" effect). DEPRIORITIZED; folded into Phase 1 as a small confirmatory cell, not a standalone arm.
- **Therefore (per operator 2026-06-17):** stock-MEMIT same-entity locality is treated as ALREADY DISPROVEN (Gate A + research). Phase 1 is a tight metric-anchored *confirmation*, not a re-derivation; the program's weight moves to the in-paradigm workarounds (the spec's mild escape hatches) and, only if those fail, the spec's strong escape hatches.

## Escape-hatch hierarchy — using the spec's OWN D12-revisit + Category A/B/C rules
The spec and POC plan (`proposals/poc-execution-plan-and-spec-revision-rule.md` §3.1, §4) pre-define the escape hatches for an OQ-W2-negative finding. We climb this ladder mildest→strongest and STOP at the first rung that restores same-entity locality, so the in-weight thesis is preserved as far as the evidence allows:

| Rung | Escape hatch (spec's term) | Phase | Spec-edit class | Preserves in-weight thesis? |
|---|---|---|---|---|
| 0 | **§8.2 safeguards as-specified** — the spec ALREADY mandates "orthogonal projection (new fact vectors orthogonal to existing features, preventing polysemantic cluster corruption)" + "covariance balancer". Phase 1 tests whether these, as currently specced, suffice. | 1 | A (provisional) | yes |
| 1 | **Engine-config: relation-inclusive keying** (`fact_token` change). Mildest; no science-path patch. | 2 | B (write-engine config amendment) | yes |
| 2 | **Make §8.2 orthogonal projection ENTITY-AWARE** (null-space P built from the entity's own other attributes). NOT a new mechanism — it operationalizes the safeguard the spec already requires, using data only a DB has. | 3 | B (amendment to §8.2 / D20) | yes |
| 2b | **`.vindex` tier sharding** (§8.4) — store same-entity attributes in orthogonal overlay subspaces (WISE-style); the tier stack already exists for independent rollback. | 3b (cond.) | B | yes |
| 3 | **Target-band redeclaration** (D12-revisit option a) — different MEMIT target layers (ties to v1.7.2 front-loading + BLUE boundary-layer). | 3c (cond.) | B/C | yes |
| 4 | **Model swap** (D12-revisit option b) — a base model that is intrinsically more same-entity-local. (Research: largely model-GENERAL, so low prior — but DiKE-trainable or disentangled-representation models are candidates.) Logged candidate: **Gemma 4 E4B** (dense GeGLU, on-GPU fit; Gemma Scope SAEs for disentanglement) — see `gemma_rung4_candidate_note.md`. | 4 | C → v1.3 | yes |
| 5 | **GRACE / parameter-preserving pivot** (D12-revisit option c) — same-entity locality by construction. | 4 | C → v1.3 | **softens** (in-weight→hybrid) |
| 6 | **Architectural redesign** (D12-revisit option d) — last resort. | 4 | C → v1.3 | no |

Rungs 0–2b are **Category B amendments that keep the in-weight thesis** (and 1–2 extend safeguards the spec already names). Rungs 4–6 are **Category C / D12 revisit → v1.3**. The verdict = the lowest rung that restores same-entity locality at acceptable expression/generalization cost; if none does up through rung 5, viability of the in-weight thesis is DISPROVEN and rung 5 (GRACE existence proof) is the demonstrated fallback.

## Metric (adopted; grounds all phases)
Behavioral-deviation, ground-truth-free (validated by arXiv 2601.17343; matches survey "Knowledge Distortion"):
- **Primary same-entity-locality metric:** Jensen–Shannon divergence over next-token distribution on same-subject OTHER-attribute probes, JS∈[0,ln2]. Report **%-locality = mean(1 − JS/ln2)** and **fraction of probes below the calibrated floor**.
- **Secondary:** top-1 flip-rate; KL (continuity with S2.39/40); expression = post p(target).
- **Cross-entity specificity** (the lineage's NS) retained as a control — must stay clean throughout.

## Phases, gates, and the prove/disprove decision tree

### Phase 0 — GATE-CAL (metric calibration). PRECONDITION; gates everything.
On GPT-J-6B and Qwen2.5-7B:
- **Null/identity edit:** target_new = model's CURRENT top-1 for the edit prompt. Expect drift ≈ 0 everywhere (the true floor).
- **True-reassert edit:** target_new = the true object. Expect ≈ floor.
- **Destructive control:** maximize update magnitude (low mom2_update_weight). Expect high drift everywhere (ceiling).
- **kl_factor sensitivity:** sweep the essence-KL factor; same-entity drift MUST move monotonically with it.
- **GATE:** null-edit floor ≈ 0 on both models AND destructive ceiling high AND metric monotonic in kl_factor. If a null edit already drifts high → harness broken at a deeper level → **HALT**. Sets the per-model floor/ceiling that define "local" vs "corrupted" for Phases 1–4.

### Phase 1 — Baseline confirmation + Rung-0 test (compressed; failure already proven).
Stock-MEMIT same-entity failure is established (Gate A + research) — Phase 1 does NOT re-derive it at scale. It (a) re-anchors it on the Phase-0-calibrated metric, and (b) tests Rung 0: whether the spec's §8.2 safeguards *as currently specified* already suffice. Tight:
- **Entity set:** ~8 well-known real entities the models encode confidently, spanning the "Flex Tape" attribute types (birthplace/citizenship/occupation/creation-date/location/composition). Smaller n than a from-scratch proof because the effect is already established; n only needs to anchor the metric + attribute-type spread.
- **Single-edit cell:** edit one counterfactual attribute; same-entity drift on ≥4 other attributes + cross-entity controls. GPT-J + Qwen (1 Llama cell folds in the deprioritized X1 cross as confirmation of model-generality).
- **Sequential same-subject cell (the key NEW datum):** edit A1 of entity E, then A2 of E; does the A2 edit corrupt stored A1? (related-knowledge-perturbation; NAACL 2025 / MEMIT-Merge). This is the multi-field-DB-defining test and was never run in S2.x.
- **Rung-0 check:** run with the spec's §8.2 orthogonal-projection + covariance-balancer safeguards ON (as the engine implements them) vs OFF — does the spec-as-written already mitigate same-entity drift? If yes → much milder verdict; if no → §8.2's projection is cross-entity-only (as the AlphaEdit analysis predicts), motivating the entity-aware Rung 2.
- **Output:** calibrated baseline same-entity %-locality + attribute-type breakdown + sequential-collapse rate + Rung-0 verdict. The number the workarounds must beat.

### Phase 2 — Workaround A: relation-inclusive keying.
- Switch engine `fact_token` `subject_last → last` (key at the prompt's final, relation-inclusive token). Re-run the Phase 1 batteries.
- **Measure:** same-entity drift reduction; expression retention; generalization cost (paraphrase still fires?). For a *database* (exact field lookups) reduced subject-generalization is acceptable.
- **Pass:** same-entity %-locality near the Phase-0 floor AND expression intact. Config-level change (no science-path patch) — cheapest viable escape.

### Phase 3 — Workaround B: entity-aware null-space projection.
- Implement AlphaEdit-style projection of ΔW onto the null space of P, where **P is built from the edited entity's OWN other (s, r′) keys** (the DB knows them — general editing cannot do this). Science-path change → **LAW #5**: isolate against a known-ceiling Llama result with empty/orthogonal P (prove inertness) before trusting any verdict.
- **Measure:** same-entity preservation + expression + cross-entity specificity.
- **Pass:** same-entity %-locality near floor with expression intact and projection demonstrably inert in the null case.
- (Optional Phase 3b if A & B both partial: combine A+B; or WISE-style overlay sharding via the `.vindex` tier stack.)

### Phase 4 — Verdict + existence proof (climb the escape-hatch ladder; stop at the lowest rung that works).
Evaluate rungs in order; the verdict is the LOWEST rung that restores same-entity locality at acceptable expression/generalization cost:
- **Rung 0 passes (Phase 1)** → spec's §8.2 safeguards already suffice → Category A, spec stands as-written.
- **Rung 1 or 2 passes (Phase 2/3)** → in-weight VIABLE via a **Category B amendment** to the Write Engine layer (relation-inclusive keying, or entity-aware orthogonal projection — the latter operationalizes the §8.2 safeguard the spec already mandates). In-weight thesis preserved. Quantify the trade.
- **Rungs 0–2 fail → escalate conditionally:** Rung 2b (`.vindex` tier sharding, §8.4) → Rung 3 (target-band redeclaration; reuse v1.7.2/BLUE) → Rung 4 (model swap / DiKE-class). Each is gated by the prior rung's failure; run only as needed.
- **All in-weight rungs (0–4) fail →** in-weight same-entity locality DISPROVEN for MEMIT-class editing. Invoke **Rung 5: GRACE existence proof** — confirm a parameter-preserving engine achieves same-entity locality by construction on the identical battery, turning the "GRACE pivot" escape hatch from assertion into demonstrated fact. Route as **D12 revisit / Category-C → v1.3**; Schema/Validation/Security/State-Consistency/Orchestration layers survive the write-engine swap.
- **Either branch genuinely determines viability, and names the exact spec escape hatch invoked** — that is the deliverable (`write_engine_viability_determination_report.md`).

## Discipline
- Engine fingerprint gate every session (`5c0c706a…c78770`, `_cov_cpu==3`). Phases 0–2 are engine-UNMODIFIED (config-only). Phase 3 modifies the science path → LAW #5 isolation + one-fix-then-halt.
- Every phase: JSON artifact + summary block + decision IDs. No promotion past an unmet gate. A clean HALT is success.
- Determinism/known-baseline gates per CLAUDE.md where a prior characterized arm is re-run.

## Artifacts (per phase)
s241_gatecal.json · s242_baseline_failure.json · s243_relation_keying.json · s244_entity_nullspace.json · s24X_grace_existence.json (conditional) · framework_finding v1.10 (metric+baseline) → v1.11 (workarounds) → v1.12 (verdict) · write_engine_viability_determination_report.md (Phase 4).
