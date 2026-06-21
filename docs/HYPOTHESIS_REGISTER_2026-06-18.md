# Consolidated Hypothesis Register — 3 deep-thinking passes (2026-06-18)
Synthesis of: Pass 1 (E1-attribution de-confounding H1–H6) + Pass 2 (novel approaches) + Pass 3 (foundational).
Status: COLLAPSED=tested&ruled-out · OPEN=untested · PARTIAL=corroborated-not-proven. Cost/Value are rough.

## A. E1 — LARQL-serving attribution
| # | Hypothesis | Status | Cost | Value |
|---|---|---|---|---|
| A1 | Garbage = Q4_K_M dequant bug, not bias (H1) | COLLAPSED (0.5B non-quant also 0-bias) | — | — |
| A2 | Bias-drop co-incidental; real cause = decompile (H2) | PARTIAL (corr. strong; not causal) | — | — |
| A3 | My vocab edit (→151936) corrupts output (H3) | COLLAPSED (HF config IS 151936) | — | — |
| A4 | --level inference omits vs --level all (H4) | COLLAPSED (level-all 0.5B also 0-bias) | — | — |
| A5 | LARQL globally broken now / wrong path (H5) | COLLAPSED (Qwen3 serves clean now) | — | — |
| A6 | n=1 observation (H6) | COLLAPSED (4 prompts systematic garbage) | — | — |
| A7 | **Bias ablation in HF Qwen2.5-3B** — zero q/k/v bias, probe recall. Garbage→bias causal; "Paris"→attribution WRONG | **OPEN — DECISIVE** | ~5min | **HIGH (can overturn)** |
| A8 | Bias tensor norm vs activation scale — is bias even large enough to be catastrophic? | OPEN | trivial | med |
| A9 | Airtight: safetensors-to-vindex on edited 3B (non-quant, same model) | OPEN (near-redundant) | ~1hr | low |

## B. Serving / deployment architecture
| # | Hypothesis | Status | Cost | Value |
|---|---|---|---|---|
| B1 | E1 should re-decide B1's model: Qwen3 (LARQL-servable) not Qwen2.5-7B (un-servable) | OPEN (decision) | — | HIGH |
| B2 | DB query-layer ≠ LARQL vindex: external triple-index (G3 prototyped) over llama.cpp serve → keeps Qwen2.5 + recovers DB reads + sidesteps bias | OPEN | med | HIGH |
| B3 | **L2 in-weight may be unnecessary** — L1 retrieval (KNN+ROUTE VERIFY, no-code, works) may suffice for exact-lookup DB. Questions the core thesis | OPEN — FOUNDATIONAL | low (analysis) | HIGH |
| B4 | Governance↔science miscalibration: does drift-detection fire on real G6.1 corruption? (built before corruption characterized; keyed to wrong variable) | OPEN | med | med-HIGH |
| B5 | Hybrid read: in-weight store + L1 ROUTE-VERIFY fallback for corrupted reads — end-to-end accuracy untested | OPEN | med | med |

## C. Editing-method space (beyond MEMIT family)
| # | Hypothesis | Status | Cost | Value |
|---|---|---|---|---|
| C1 | **GRACE/WISE non-interference methods structurally avoid cross-entity corruption** (parked prematurely; CPU-write-friendly; OK for exact-lookup) | OPEN (grace_dry_run exists) | med | HIGH |
| C2 | **Cross-entity corruption is a KEYING artifact** — relation-inclusive subject reformulation (subject_last, NO engine patch) cuts key cosine 0.92-0.93 at source. Corpus-identified, UNRUN | OPEN — cheap root-cause | low | HIGH |
| C3 | **DB-specific write: explicit same-relation neighbor RE-ASSERTION in the solve** (we know the facts; distinct from A2 key-sentinels) — fixes incremental path | OPEN — novel | low-med | HIGH |
| C4 | A3/BetaEdit port (λ1·Σ + τ-P-refresh) — parked on incremental-requirement gate | PARKED | med | cond. |

## D. Capacity / mechanism (the D1 cluster = F1 deliverable)
| # | Hypothesis | Status | Cost | Value |
|---|---|---|---|---|
| D1 | Capacity law: interference = f(relation fan-out × N × model size × band × key-cosine). The core spec-readiness deliverable | **STRUCTURAL DONE+model-general (§8.7 amendment, D-D1-1+D-B1-2)**; numeric threshold OPEN (instrument-noise-limited) | high | HIGH |
| D-NOISE | Sequential-edit held-out corruption is ~50pp run-to-run nondeterministic on the IDENTICAL config (7B seed3 20.8→70.8 on re-run; GPU nondeterminism, unverified mechanism) → single-run absolutes unreliable; BLOCKS numeric §8.7 thresholds on this instrument | **PROMOTED (finding, D-B1-2)** → next-arc = deterministic/batch/higher-N instrument | — | HIGH (gates the numeric law) |
| D2 | Mechanistic: WHY batch eliminates corruption — SVD edit-deltas, project on shared-relation direction, null-space occupancy. Convert inference→evidence | OPEN | med | HIGH |
| D3 | Ground capacity in null-space DIMENSION (compute_P reports it) — principled bound, not fitted | OPEN | low-med | med-HIGH |
| D4 | Corruption law is model-SPECIFIC (Phase-1: locality is) — bounds D1 generality | OPEN | high | med |
| D5 | Quantization × cross-entity-corruption INTERACTION — does A1 batch-clean survive Q4_K? (B3 tested edits, not isolation) | OPEN | med | med-HIGH |
| D6 | B1 size-density (Qwen2.5-7B): does A1 batch-clean replicate upward? | DONE-PARTIAL (D-B1-1, CORPUS/19). NB distinct from D-B1-2 (D1 concentration law's model-size term, DONE: REPLICATE + threshold unresolved) | — | med |

## E. Evaluation validity
| # | Hypothesis | Status | Cost | Value |
|---|---|---|---|---|
| E1 | Margin confound is program-WIDE (compute_z inflation distorts A1/A2/G6.1 cross-entity + locality metrics, not just B3) | OPEN | med | HIGH |
| E2 | Robustness/calibration: edited fact under sampling/temp/paraphrase; "stored vs barely-expressed" | OPEN | low-med | med-HIGH |
| E3 | Read-contract surface: reverse lookup, aggregation, negation, 5 relation families on READ — the real DB query semantics | OPEN | med | HIGH |
| E4 | Ripple/multi-hop (RippleEdits): France→Oslo, does "Eiffel Tower in ___" stay consistent? | OPEN | med | med-HIGH |

## F. Frontier
| # | Hypothesis | Status | Cost | Value |
|---|---|---|---|---|
| F1 | SAE/superposition decomposition (A6): edit in sparse feature basis to avoid shared-direction leakage no λ_s arrests | OPEN | high | high (if linear fixes plateau) |
| F2 | Temporal durability: drift across SUCCESSIVE batch rebuilds (deployment = periodic rebuild; only 1 batch tested) | OPEN | med | med-HIGH |

## TOP PICKS (cheap × decisive × foundational)
1. **A7** bias ablation — can overturn the E1 attribution in 5 min.
2. **C2** relation-inclusive keying — cheap, unrun, attacks corruption root cause.
3. **B3 + B2** — question whether L2 is needed; if it is, decouple the DB layer from LARQL. Reframes the whole deployment story.
4. **C1/C3** — GRACE and DB-specific neighbor re-assertion: methods that *structurally* avoid the corruption we keep fighting.
5. **D1/D2** — the capacity law + its mechanism: the actual F1 deliverable.

## G. Advisor additions (Pass-4 input — one outside voice, eliminates nothing)
| # | Hypothesis | Status | Cost | Value |
|---|---|---|---|---|
| NEW-1 | Sharpen A7: compare LARQL garbage TOKEN-FOR-TOKEN vs HF-Qwen2.5 bias-zeroed. Match→bias is the WHOLE story; different→second bug (decompile) layered on bias | OPEN — do as part of A7 | ~5min | HIGH |
| NEW-2 | "Wikidata output matching: 0/512 clusters labeled" in convert log = Qwen2.5-specific decompile-degradation signal, independent of bias. Check Qwen3 labeled nonzero | OPEN — cheap | trivial | med-HIGH |
| NEW-3 | correct() prefix-match labeling confound (a==b or startswith) underneath G6.1/A1/B1 cross-entity %. Distinct from margin confound (probability vs labeling rule). Audit exact-match flips | OPEN | low | med-HIGH |
| NEW-4 | Write-type asymmetry: all results use counterfactual REASSIGNMENT (overwrite). DB also INSERTs (no prior competitor) + DELETEs — different interference profiles. DB use-case is insertion-heavy | OPEN | med | med-HIGH |

### Advisor review notes (input, not authority):
- TOP-5 ranking endorsed. After A7, highest-leverage = B3/B2 + C2.
- C1 (GRACE): structurally avoids corruption but MOVES it to serving (GRACE adapters don't serve via llama.cpp/LARQL free) — trades write-problem for serve-integration problem.
- B3 (drop L2) and E3 (read-contract) are the SAME decision twice: L1 retrieval can't support multi-hop "reason OVER the stored fact". Decide B3 against E3.
- SEQUENCING (binding): run A7 + read B1 BEFORE more theorizing — evidence should prune the register first.

## H. External-evidence references (catalog triage, 2026-06-19)
External repos found by reading the content (not stars) of all 130 in [`research_and_specs/llm_research_tools_high_value.md`](../research_and_specs/llm_research_tools_high_value.md). **None is a knowledge-editing implementation** — these are *adjacent* corroboration/tools, keyed to the hypotheses they bear on. **Caveat (`[[verify-external-artifacts-before-effort]]`):** all are external, unvetted, mostly single-author repos — treat as **leads/corroboration**, verify before relying on any number or method.

| Hypothesis | External evidence | Relevance |
|---|---|---|
| **D2** (method only) ~~C2~~ | [skgallagher/ELLMTrees-paper](https://github.com/skgallagher/ELLMTrees-paper) | ⚠️ **VERIFIED — DOWNGRADE** (`research_and_specs/external_evidence_notes.md` EV-1): its "key matrices" = attention **W_k** carrying *fine-tuning lineage* (RF-distance phylogeny), **NOT** our down_proj activation keys. Same word, different object — **not** C2 corroboration. Residual: its RF / permutation-null method may be reusable for D2 (edit-delta structure vs a random-relabel null). |
| **F1** (SAE / superposition) | [Melodiz/llm-research-projects](https://github.com/Melodiz/llm-research-projects) · [ADEL9st/LLM-Mind-Visualizer](https://github.com/ADEL9st/LLM-Mind-Visualizer) | SAE feature-recovery + superposition geometry with **known ground truth**; logit-lens / residual-stream / direction-ablation tooling (GGUF adapters). Method references if we test the sparse-feature-basis fix. |
| **D2** (interference geometry, mechanism) | [sasakimc/semantic-resilience-project](https://github.com/sasakimc/semantic-resilience-project) | Representation-collapse experiments (stance-drift on Qwen2.5, embedding/stance metrics, run-schema) — low-dim "semantic mode" framing. |
| **D5, E1** (quant × corruption; margin confound) | [tanueihorng/llm-ethics-benchmark](https://github.com/tanueihorng/llm-ethics-benchmark) | Matched **fp16→INT8→NF4** pairs + a **refusal_margin** module + repro kit — an independent quantization-survival harness measuring behavior by margins. |
| **E2 (+E1)** (calibration / stored-vs-expressed) | [cscheffler/elicit-model-beliefs](https://github.com/cscheffler/elicit-model-beliefs) · [Pankick/llm-research](https://github.com/Pankick/llm-research) | Belief **stability across paraphrases** vs model size on Qwen2.5; confidence-vs-correctness (**AUROC/ECE**, next-token distribution) on Qwen2.5. Direct methods for the read-robustness/margin question. |
| **F2, D1** (temporal durability / capacity / forgetting) | [vivsn289/Adaptive-Self-rehearsal](https://github.com/vivsn289/Adaptive-Self-rehearsal) · [luisroberto0/project-hebb](https://github.com/luisroberto0/project-hebb) | Catastrophic-forgetting + adaptive rehearsal on **Qwen2.5-3B** (3 seeds, lm-eval, paired SE); continual-learning/plasticity with CI95 + honest negatives + **CPU-latency deployment** analysis. |
| **C1** (non-interference methods) | [luisroberto0/project-hebb](https://github.com/luisroberto0/project-hebb) | Bio-inspired local-plasticity learning = a non-interference paradigm in the GRACE/WISE family of "structurally avoid corruption." |
| **B2, B3, E3** (external query-index vs in-weight) | [Pra0809/xai-knowledge-graph](https://github.com/Pra0809/xai-knowledge-graph) · [Anandesh-Sharma/awesome-agentic-memory](https://github.com/Anandesh-Sharma/awesome-agentic-memory) | ✓ **VERIFIED** (EV-2): xai-knowledge-graph is a real **GraphRAG-vs-vector-RAG** comparison — structured KG query **wins on structural / multi-hop / aggregation reads**, RAG on synthesis (win 6/10). Directional prior that the external index should be a **structured KG, not plain L1-KNN** → input to B2/E3. **SCOPE: n=10, paper-domain, judge-biased — not a transportable number.** awesome-agentic-memory = unvetted lead (external/lifelong memory map). |
| **C4** (BetaEdit port, tooling) | [going-doer/paper2code](https://github.com/going-doer/paper2code) | ICLR-2026 paper→code automation + repro benchmark — could accelerate reimplementing editing-method papers (the parked BetaEdit port). |
| **Methodology / harness exemplars** (cross-cutting; esp. NEW-3 audit discipline) | [whenpoem/aiscientist](https://github.com/whenpoem/aiscientist) · [Zhonghao1995/research-skills](https://github.com/Zhonghao1995/research-skills) · [WhaSukGO/LenaLab](https://github.com/WhaSukGO/LenaLab) · [priyamDalmia/hpc-for-ml-researchers](https://github.com/priyamDalmia/hpc-for-ml-researchers) | Pre-registration + verification harness; tested calibration/uncertainty/repro skills; held-out generator⟂verifier eval gates; reproducible cluster job templates. Reusable for our own experiment discipline. |
| **Discovery feed** | [tmgthb/Autonomous-Agents](https://github.com/tmgthb/Autonomous-Agents) | Daily-updated index of agent/LLM papers — surface new editing/interp/eval work as it appears. |
| **Tooling — autoresearch search loop** (for config-space sub-problems, e.g. C2 band-[8-12]) | [karpathy/autoresearch](https://github.com/karpathy/autoresearch) (canonical loop) · [wjgoarxiv/autoresearch-skill](https://github.com/wjgoarxiv/autoresearch-skill) (installed → `~/.codex/skills/`) · [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) (98-skill lib) | Autonomous propose→experiment→evaluate→keep/revert loops for **SEARCH** problems (best band/hparams). ⚠️ **OPTIMIZER, NOT falsifier** — Goodhart-prone; outputs are **hypothesis-generation only**. Re-verify any winner with pre-registered criteria + the inertness gate + `advisor()`; **never write a loop winner into `CORPUS/`**. Wired example: `experiments/track_c/autoresearch_band_search/` (honest EXACT-match evaluator + retention/expression guard + frozen held-out). `firecrawl/AI-research-SKILLs` = redundant smaller copy of Orchestra's. |


## I. C2-band fold-in (2026-06-20, `CORPUS/21`, D-C2band-1)
| # | Hypothesis | Status | Cost | Value |
|---|---|---|---|---|
| C2-band | Editing in low-collinearity band [8-12] reduces SEQUENTIAL cross-entity corruption | **TESTED → REAL-BUT-UNDERPOWERED, NOT PROMOTED** (mechanical PASS +18.73pp cross-JS; real redistribution — within-loc FALL + expr 100% exclude under-editing; underpowered 1 seed, within-entity top-1 cost & mechanism unmeasured) | done | mechanistic (feeds D1) IF de-confounded |
| D7 | **Depth rotates the key basis: relation-clustered (L4-8) → entity-clustered (L8-12).** Predicts same-entity / different-relation key collinearity is inversely-U — HIGHER at L8-12. Explains the cross↑/within↓ trade. builds-on: C2 (CORPUS/20). would-advance: D1 capacity law + C15 tension | OPEN — UNMEASURED (CORPUS/20 measured only same-relation) | low (compute_ks, no edits) | HIGH (decides the C2-band MECHANISM — basis-rotation vs other geometry; feeds D1) |
| C2-band-dc-b | Edited-entity within-attribute TOP-1 measured directly both arms — the VALUE gate: does the within-entity JS perturbation flip real reads, or is the cost distributional-only? | OPEN — gating | low (re-run, log it) | HIGH |
| C2-band-dc-c | Per-band edit-Δ-norm + depth-matched SHAM/null-edit control — removes injection-depth + edit-magnitude confounds from the locality deltas | OPEN | low-med | med-HIGH |
| C2-band-dc-d | ≥3 seeds + ≥2 write orderings on the JS delta — gives the ≥5pp pre-reg threshold a null distribution | OPEN | med | med |

**Sequencing (binding, updated post cross-family review):** the **norm-matched/sham control (dc-c) is now THE primary overturning gate** — gpt-5.5 (FIX-FIRST) flagged that the redistribution claim is not yet shown causal (edit-strength/Δ-norm/depth-metric confounds open). Run dc-c FIRST to confirm the effect is real at all; D7 + dc-b then characterize mechanism + cost. Run D7 (no-edit collinearity curve) for the MECHANISM — if within-entity collinearity is flat/lower at L8-12, the basis-rotation *explanation* is dead (some other depth-dependent geometry), but the redistribution itself still stands (within-loc FALL + expr 100% already exclude an under-editing artifact). dc-b (within-attr top-1) is the VALUE gate. Pre-register + `advisor()` before any re-run.
