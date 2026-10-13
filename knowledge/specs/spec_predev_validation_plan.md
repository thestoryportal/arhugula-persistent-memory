# LLM-as-Database — Pre-Development Validation Program
_2026-06-17. Successor to `write_engine_viability_determination_plan.md` (viability now DETERMINED: see `write_engine_viability_determination_report.md`). Purpose: before spec development begins, stress the VALIDATED pieces toward real-database-workload conditions via falsification-oriented GPU experiments. Engine UNMODIFIED; same discipline (gates, one-fix-then-halt, LAW#5 for science-path, expression gate, checkpoint each result)._

## What is already validated (do not re-litigate)
- Same-entity multi-attribute locality is achievable in-weight; model- & size-dependent. Qwen-7B clean at Rung 0; small Qwen-3B reaches 100% sequential retention + 80.7% untouched + 100% expression via **in-solve AlphaEdit** (null-space P, `nullspace_threshold=0.005`, L2=1, + sequential `cache_c`), LAW#5-inertness-proven. GPT-J not viable.
- Validated config (the "write engine under test"): Qwen2.5-3B, band [4–8], v_loss 35, mom2_uw 5000, lm_head=embed_tokens, AlphaEdit in-solve (`s243h`/`s243i` harness; engine kmeng01/memit untouched).
- Metric: same-entity %-locality (JS), expression gate (post_p>0.5), cross-entity NS control.

## Scope of the validation so far (the gap this program closes)
n=6–8 entities, 3–4 single-token attributes, edit-PAIRS (≤2 sequential), country domain, fp16, one GPU, in-house metric, no read-layer round-trip, INSERT-only. A database needs: thousands of writes, novel records, CRUD, many fields/entities, diverse values, quantized CPU inference, query-layer reads. Each below is a falsification attempt.

## TIER 1 — Concept-critical (failure reshapes the spec before dev)
- **T1.1 Write durability at depth (FIRST; running).** Sequential stream 2→10→50→200→(1000) edits across entities×fields, cache_c spanning the whole stream. At checkpoints re-verify ALL prior edits (cumulative retention), same/cross-entity locality, expression, and a general-capability probe (held-out perplexity). GATE: cumulative retention and locality must not collapse with depth; perplexity must not blow up. FALSIFIES the concept if AlphaEdit's `cache_c` saturates / forgetting sets in. Artifact: `s244_durability.json`.
- **T1.2 Novel-entity insertion.** Insert facts about entities the model never knew (synthetic, multi-field). GATE: novel records express, read back, and stay local. FALSIFIES "database INSERT" if only known-entity modification works.
- **T1.3 Quantization survival.** Edit fp16 → quantize Q4_K (GGUF/llama.cpp) → re-measure retention/locality/expression. GATE: edits survive the quantization the CPU deployment requires. Most deployment-critical untested link.

## TIER 2 — Workload realism
- **T2.1 Full CRUD.** UPDATE (overwrite an edited field), DELETE (null/remove a fact in-weight), re-INSERT. GATE: update replaces cleanly; delete feasible without collateral.
- **T2.2 Scale of fields × entities.** 10–50 fields/entity; hundreds–thousands of entities. GATE: same-entity locality holds as fields pack; cross-entity interference bounded at scale (packing/collision limit).
- **T2.3 Value & domain diversity.** Multi-token values, numbers, dates; people/orgs/products; relational/inverse facts. GATE: locality generalizes beyond single-token country facts.
- **T2.4 Read-layer round-trip + query generalization.** Export edited model → LARQL vindex → LQL SELECT/DESCRIBE/INFER; test reads under paraphrases/synonyms. GATE: written facts retrievable through the real query layer under varied phrasings (quantify the relation-keying generalization trade).

## TIER 3 — Confidence & external validity
- **T3.1 External benchmarks.** RippleEdits, S2RKE, KnowEdit, MQuAKE on the AlphaEdit-Qwen recipe.
- **T3.2 Capacity / forgetting curve.** General benchmark (MMLU-subset, perplexity) vs edit count; locate capacity ceiling.
- **T3.3 Mechanistic.** Gemma Scope SAEs / causal tracing — confirm edits disentangled & land in the expected band (validates address-collision theory).
- **T3.4 Recipe portability + determinism.** Confirm on exact deploy model (+ smaller Qwen2.5-1.5B/0.5B for lighter CPU); bit-exact write-engine reproducibility; cross-seed stability.

## REFRAME (2026-06-17): the spec's `.vindex` overlay-cartridge model — our findings are CALIBRATION, not threats
Spec (§Abstract, §8.1 D11/C8): writes are MEMIT-computed ΔW stored as OVERLAY tiers on a PERMANENTLY FROZEN base; stacked overlays compose by SUMMATION ≈ sequential editing → our collision findings (same-entity, cross-entity-at-depth, novel-insert) TRANSFER directly to the overlay model (our in-place-edit+restore experiments are valid proxies for overlay ΔWs). The overlay approach does NOT escape covariance-collision physics. BUT the spec already has the mechanisms our findings calibrate:
- **drift_state / drift_tier / edge_count_since_anchor + "MEMIT sub-batch ceiling" (§9, GAP-1/2, OQ-W1, "implementation-phase numerics")** ← our T1.1 durability curve + T1.1b preserve-sampling ARE these thresholds.
- **ORTHOGONAL_PROJECTION directive + covariance balancer (§8.2/8.5)** ← our AlphaEdit null-space projection (Rung 3), thresh=0.005 tuning.
- **Compaction + COMPACTION_REGRESSION probe ("did prior facts survive a recompile")** ← our retention-survival findings.
- **Incremental L1-cache BUFFERED BATCH compile (§8.3)** ← means T1.2c (batched insert) tests the spec's ACTUAL write mode (more aligned, not ad-hoc).
ADDED TESTS (spec-structure): T2.5 compaction-regression (prior-fact survival across recompile); T2.6 tier isolation (separate .vindex tiers vs one summed overlay — does tiering reduce cross-collision?).

## Cross-cutting
- Promote the country battery into a LOCKED eval harness / regression suite so spec dev inherits CI gates. Determinism/known-baseline gates per CLAUDE.md.

## Sequencing
Tier 1 gates everything (T1.1 durability, T1.2 novel-insert, T1.3 quantization — any failure changes the spec). Then Tier 2 (workload), Tier 3 (external/mechanistic/portability). All GPU-bound; exhaust here before local-CPU dev.

## Decisions (to be assigned as run): D-S244-* 
## Artifacts: s244_durability.json · s244_novel.json · s244_quant.json · s244_crud.json · s244_scale.json · s244_diversity.json · s244_readlayer.json · external_bench/* · framework_finding v1.13+ · spec_predev_validation_report.md (close).
