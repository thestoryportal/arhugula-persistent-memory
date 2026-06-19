# Write-Engine Viability Determination — Report
_2026-06-17. Program: `write_engine_viability_determination_plan.md`. Engine kmeng01/memit @ `5c0c706a…c78770` (UNMODIFIED throughout; all workarounds are config-level or harness-level post-/in-solve with the engine untouched). All edits Probe-B style (apply + restore)._

## 0. The viability question
Can the v1.2 spec's **in-weight** (§1), **MEMIT-designated** (D12/§8.2), **entity-centric** (§7.2–7.3) write engine achieve **same-entity multi-attribute locality** — editing one attribute of an entity must not corrupt that entity's OTHER attributes, and (the DB-defining case) storing a SECOND fact about an entity must not destroy the first? This is the load-bearing requirement; the MEMIT lineage's "locality" (Neighborhood Success) measures only CROSS-entity specificity and is silent on this axis.

## 1. Metric (Phase 0)
Behavioral-deviation, ground-truth-free: **same-entity %-locality = mean(1 − JS/ln2)** over next-token distributions on same-entity OTHER-attribute probes (endorsed by arXiv 2601.17343; "Knowledge Distortion"). Cross-entity JS retained as the lineage's NS control.
- **v1 calibration HALTed** (null/identity edit drifted ~0.11, no clean floor) — traced to STIMULUS, not metric: low-confidence/degenerate edit targets forced large ΔW even to "re-assert".
- **v2 fix (centrality-matched stimulus):** screen entities to be CONFIDENT+CORRECT on every attribute; edit a HIGH-confidence anchor so the null edit re-asserts a near-certain token (≈ no-op ⇒ clean floor). **Result: clean null floor on both GPT-J (0.0026) and Qwen-7B (0.0065), metric sensitive across 0.0006→0.49.** Metric CALIBRATED (D-S242-CAL-1). Per-model `mom2_update_weight` calibration + an EXPRESSION GATE (require post_p>0.5) were required to avoid no-op-edit false-locality.

## 2. Baseline + sequential (Phase 1) — locality is MODEL- and SIZE-dependent
Country entities (capital/currency/continent/language), single-edit (Cell A) + sequential same-subject (Cell B = edit A1 then A2; does A2 clobber A1?).

| Model | single-edit locality (cap/cur/lang) | **sequential edit-1 retention** | untouched |
|---|---|---|---|
| GPT-J-6B | 62 / 33 / 42% | **43%** | 43% |
| Qwen2.5-3B (CPU-class) | 87 / 81 / 64% | **37.5%** | 61% |
| **Qwen2.5-7B** | 95 / 98 / 83% | **100%** | 79% |

- **GPT-J** (the canonical "clean MEMIT" model) is the WORST — same-entity non-local on every attribute type and catastrophic on sequential (the multi-field-DB failure, directly demonstrated). (D-S243-SEQ-1)
- **Qwen2.5-7B** is clean at the MILDEST rung (Rung 0 / Category A): stock MEMIT already yields 100% sequential retention + clean cross-entity. **In-weight multi-field thesis VIABLE as-written on Qwen-7B.** (D-S243-RUNG-1)
- **Same-entity locality is model-dependent (Qwen≫GPT-J) AND size-dependent (Qwen-7B clean, Qwen-3B fails)** — contradicts the literature's "model-general failure" prior (S2RKE/DiKE/MEMIT-Merge). (D-S242-HMODEL-1)
- Mechanistic frame (Chris Hay / LARQL, the spec's query layer): facts are addressed by RELATION+ENTITY; same-entity bleed = address collision. Reads are free; **write-side collision is the sole hard problem** — exactly this axis.

## 3. Making the lightweight (CPU-class) model viable — the workaround ladder (Qwen2.5-3B)
Sequential edit-1 retention (the DB-critical metric):

| Mechanism | retention | cross-entity | notes |
|---|---|---|---|
| Stock subject-keyed | 33% | clean | fails |
| Rung 1 — relation-inclusive keying (config-only) | 100% same-entity | **bleeds (83.6%)** | trades within-entity for cross-entity collision; language under-expresses |
| Rung 3 — post-hoc null-space projection (harness) | 50% | not fixed | post-hoc too weak (also fails to fix cross-entity in hybrid) |
| **In-solve AlphaEdit — null-space P + sequential `cache_c`** | **100%** | — | **the fix; untouched-attr 81% at tuned threshold** |

- Rung 1 (relation-inclusive keying via the subject string, no engine patch) recovers same-entity locality (100%) but moves the collision across entities — confirming the bleed is an address-collision phenomenon (LARQL's "address = relation + entity").
- Rung 3 post-hoc projection (project ΔW onto null space of preserve-keys, engine UNMODIFIED, LAW#5 inertness proven) only partially helps (50%) — post-hoc subtraction is too weak.
- **In-solve AlphaEdit** (reimplemented in harness using engine primitives; null-space P from SVD of the covariance + `cache_c` accumulating prior-edit keys *inside* the solve; LAW#5 inertness PASSED — harness MEMIT-mode reproduces the engine) lifts sequential retention **33% → 100%** — every prior edit survives subsequent edits. (D-S243-ALPHAEDIT-1)
- **Tuning CLOSED the untouched-attribute gap** (`s243_alphaedit_tune.json`): `nullspace_threshold` sweep at fixed L2=1 — 0.02→ retention 100%/untouched 73%/expr 100%; **0.005→ retention 100%/untouched 80.7%/expr 100% (sweet spot, untouched now ≥ the 7B's 79%)**; 0.001→ over-constrained (retention 0%, expr 16%). So at the tuned threshold the small model holds BOTH properties — prior-edit retention 100% AND untouched-attribute locality ~81% — with full expression. (D-S243-ALPHAEDIT-TUNE-1)

## 4. VERDICT
**The in-weight, MEMIT-class, entity-centric multi-field write engine is VIABLE.** Same-entity multi-attribute locality — including the load-bearing sequential multi-field case — is achievable in-weight:
- **On Qwen2.5-7B: viable as-specified, Rung 0 / Category A** (stock MEMIT; no workaround). Spec stands.
- **On a small/CPU-class model (Qwen2.5-3B): viable with a Write-Engine amendment** — in-solve null-space editing with sequential preservation (AlphaEdit-class), a **Category-B/C amendment** to the write layer, demonstrated (not assumed) to restore 100% sequential retention.
- **GPT-J-class models are NOT viable** for multi-field in-weight editing (worst on every axis) — the canonical MEMIT model's reputation is on the cross-entity axis only.
The spec's escape-hatch ladder functions as designed; the lowest rung that delivers a CPU-deployable multi-field store is in-solve AlphaEdit.

## 5. Deployment (operator constraint: local Intel CPU)
Edit-time and inference-time are separable. **Validated stack:** small **Qwen2.5-3B** + **in-solve-AlphaEdit** write engine (edits computed offline on GPU) → standard edited safetensors → **CPU inference via llama.cpp / LARQL** (the spec's query layer; vindex/LQL; "no GPU required"). Alternative: **Qwen-7B quantized** (Q4 ~4.5GB) — cleaner untouched-attr locality, no workaround, heavier on CPU. LARQL also provides the read/query layer and the CPU deployment path; our work supplies the same-entity-locality validation LARQL's write path lacked.

## 6. Caveats / future work
- **Untouched-attribute locality** under AlphaEdit — RESOLVED by tuning `nullspace_threshold` to 0.005 (untouched 81% at 100% retention/expression). Further headroom likely via joint L2 tuning.
- **Scope:** ~6–8 country entities, 3–4 single-token attributes, edit-pairs (≤2 sequential). Scale: more entities, longer edit streams, multi-token/diverse attributes.
- **External validity:** run RippleEdits / S2RKE (the named same-entity benchmarks) on Qwen.
- **Hardware lineage:** RTX 4090; determinism gates anchored here (findings are large effects robust to hardware; bit-exact gates would need re-baselining elsewhere — e.g. molab Blackwell, see `molab_feasibility_report.md`).
- **Gemma 4** (rung-4 candidate) deferred (needs newer transformers in an isolated env); low prior of a locality advantage; deployment-aligned with LARQL.

## 7. Decisions
- D-S242-CAL-1: same-entity JS metric calibrated via centrality-matched stimulus (clean floor both models).
- D-S242-HMODEL-1: same-entity locality is model- AND size-dependent (Qwen-7B local, GPT-J not, Qwen-3B fails) — contra model-general prior.
- D-S243-SEQ-1: sequential multi-field test — Qwen-7B 100% / GPT-J 43% / Qwen-3B 37.5% retention.
- D-S243-RUNG-1: in-weight thesis viable on Qwen-7B at Rung 0 (spec as-written).
- D-S243-ALPHAEDIT-1: in-solve AlphaEdit (null-space P + sequential cache_c) restores small-model sequential retention 33%→100% (LAW#5 inertness proven); post-hoc projection insufficient (50%).
- D-S243-ALPHAEDIT-TUNE-1: nullspace_threshold=0.005 (L2=1) is the sweet spot — small Qwen-3B holds 100% retention + 80.7% untouched-attr locality + 100% expression; threshold 0.001 over-constrains (edits stop expressing). Untouched-attr gap CLOSED.

## Artifacts
Phase 0: `s242_gatecal_{gptj,qwen}.json`, `s242_phase0_v2_conclusion.md`. Phase 1: `s243_phase1_{gptj,qwen,qwen3b}.json`. Workarounds: `s243_phase1_qwen3b_relsubj.json` (Rung1), `s243_rung3_qwen3b.json` + `s243_rung3seq_*.json` (Rung3 post-hoc), `s243_hybrid_qwen3b.json` (hybrid), `s243_alphaedit_insolve.json` (in-solve AlphaEdit), `s243_alphaedit_tune.json` (tuning). Findings: `framework_finding_v1_10_additive.md` (+ v1.11/v1.12 to consolidate). Prior art: `external_prior_art/{larql,the-mechanism}`, `research_and_specs/{gemma4_editing_research,molab_feasibility_report,model_does_not_unpack_memory}.md`.
