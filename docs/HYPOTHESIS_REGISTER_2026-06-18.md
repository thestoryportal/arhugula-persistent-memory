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
| D1 | Capacity law: interference = f(relation fan-out × N × model size × band × key-cosine). The core spec-readiness deliverable | **STRUCTURAL DONE+model-general+operator-APPROVED; NUMERIC guardrail SET (D-D1-2: k≤2, dual-reviewed; mixed-load→needs global-volume bound too)**; cross-model transfer OPEN (OQ-W1, 7B via determinism) | high | HIGH |
| D-NOISE | Sequential-edit held-out corruption is ~50pp run-to-run nondeterministic on the IDENTICAL config (7B seed3 20.8→70.8 on re-run; GPU nondeterminism, unverified mechanism) → single-run absolutes unreliable; BLOCKS numeric §8.7 thresholds on this instrument | **RESOLVED (D-D1-2):** 3B within-process SD=0; noise is 7B/across-process + edit-ORDER (intrinsic); lower-variance instrument BUILT (order-clustered bootstrap) → numeric guardrail set | — | HIGH (gates the numeric law) |
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

## J. ConnectedPapers graph review (2026-06-21) — prior-art LEADS (operator-built graphs)
Source: 3 operator-built ConnectedPapers co-citation graphs (seeds: **AlphaEdit** / **MEMIT** / **Connected-Papers-foundations**) exported to `research_and_specs/ConnectedPapers-for-*.bib` (41 nodes each). **DISCIPLINE: co-citation output = IDEATION → LEADS, NEVER evidence, NEVER `CORPUS/`** (§1/§3). arXiv IDs are from the .bib export; only **NeuralDB independently fetched + confirmed** (`external_evidence_notes.md` EV-3). Each lead → falsify by experiment or fold into F1 framing; verify before any port ([[verify-external-artifacts-before-effort]]). Graph B (LightMem/agent-memory) = mostly external-memory **contrast class** + co-author noise (Minecraft/multimodal) → low signal for in-weight; relevant minority = Mem0/MemoryOS (deployment competitor for the "why in-weight not RAG" F1 justification).

| # | Lead (source paper, arXiv) | Maps to | builds-on / would-advance | Status | Cost | Value |
|---|---|---|---|---|---|---|
| D8 | **Norm-growth is the sequential-collapse driver** — NAS *Norm Anchors* (2602.02543, "positive norm-feedback loop", ~exp growth, fix=rescale value-vec to orig norm, +4× horizon) + Gupta *Better Regularization* (2502.01636, Frobenius constraint→10K) + DeltaEdit (2505.07899). → **the §8.7 drift variable may be cumulative (per-relation) ‖ΔW‖, not edit-count/concentration.** | D1 / §8.7 / D-NOISE | builds-on D1 (D-D1-1) + the ΔW-norm log already in B1 §2.1 / threshold-instrument §4. would-advance the numeric §8.7 threshold | **OPEN — TESTABLE IN-PLACE** (instrument already logs cumulative ‖ΔW‖_F; check corruption-vs-norm in the sweep output; TEST the field's claim, don't adopt) | ~0 (already logged) | **HIGH (could set the threshold variable)** |
| D9 | **Gated/routed SIDE-STORE structurally avoids cross-entity corruption** — NeuralDB (2507.18028, "linear L&E = KV-DB query"; non-linear gated retrieval fires only on edited facts; 100K facts on Llama-3-8B) + WISE (side-memory+routing) + GRACE/MELO. Closest prior art to the LLM-as-DB spec. | B3 / C1 / spec core | builds-on B3 (drop diffuse L2?) + C1 (GRACE/WISE family). would-advance the F1 in-weight-vs-side-store decision | **OPEN — VERIFY REPO BEFORE PORT** (EV-3: paper confirmed real; no repo link surfaced — GitHub-check before effort) | low (read) → med (port) | **HIGH (bears on the thesis)** |
| D10 | **A1 batch-clean is independently corroborated** — LocFT-BF *Fine-tuning Done Right* (2509.22072): breadth-first (batch/epoch) beats depth-first (sequential) b/c per-edit over-optimization induces cross-edit interference; 100K edits/72B. | A1 (D-A1-1) | builds-on A1. would-advance F1 (external grounding that batch/Genesis path is the right deployment model) | OPEN — F1 framing (corroboration, not new test) | ~0 | med-HIGH |
| D11 | **Eval-critique cluster = our rigor corroborated + the thesis's standing threat** — *Mirage of Model Editing*/QAEdit (2502.11177, teacher-forcing inflates 96.8%→38.5% real, fails @1000 edits) + *Is Model Editing Built on Sand?* (2510.00625, edits = shortcuts not semantics, collapse under negation). | E-cluster / F1 honesty | builds-on our autoregressive-top-1 discipline + G6.1 scale-corruption. would-advance F1 (must confront "editing is illusory" head-on) | OPEN — F1 must address | low (framing) | **HIGH (F1 credibility)** |
| D12 | **Competing mechanisms for cross-entity corruption** — SADR *Over-Attention* (2502.14838, "Attention Drift": heads over-attend edited entity) + REVIVE *Spectral* (2601.11042, edits disrupt DOMINANT singular dirs) + SUIT (2509.24502) / SPHERE (2510.01172, both on Qwen2.5-7B). Our mechanism (shared relation dir in editable subspace) is ONE of these. | D2 / D7 / C2 | builds-on D2/C2 mechanism. would-advance D1 (which geometry actually drives the corruption) | OPEN — discriminating check mostly no-GPU | low-med | med-HIGH |
| D13 | **Context-reasoning may beat in-weight editing** — SCR *No More Model Editing!* (2503.05212) + *Benchmarking & Rethinking KE* (2505.18690): in-context reasoning > parameter editing under realistic eval. Deployment incarnation = Graph-B external memory (Mem0/MemoryOS). | B3 / E3 (thesis falsifier) | builds-on B3/E3. would-advance the core F1 in-weight-necessity verdict | OPEN — the highest-stakes thesis lead | low (analysis) | **HIGH** |
| D14 | **Localization ≠ editing-site** — Hase *Does Localization Inform Editing?* — causal-trace storage location does NOT predict best edit layer. Challenges the locate-then-edit band premise. | C2 / C15 band-selection | builds-on our band work (L4-8 vs L8-12 vs spec L15-25). would-advance F1 band-choice justification | OPEN — confirm our band choices don't rest on the refuted assumption | low | med-HIGH |
| E4+ | **RippleEdits = the field's name for our cross-entity read corruption** — *Evaluating the Ripple Effects of KE* (Cohen et al.). Strengthens existing **E4**. | E4 (existing) | builds-on G6.1/D1. would-advance F1 (map our per-relation-concentration law onto RippleEdits categories for shared vocabulary + external benchmark) | OPEN — extends E4 | med | med-HIGH |
| D15 | **Cross-architecture recall analysis** — *Do All Autoregressive Transformers Remember Facts the Same Way?* — overlaps our DONE cross-architecture ceiling (Llama/Mistral/Qwen, entity-local-not-attribute-local). | cross-arch ceiling (DONE) | builds-on the cross-arch ceiling result. would-advance F1 (compare BEFORE citing ours as novel — corroborate or partial-scoop) | OPEN — comparison owed before F1 | low (read) | med-HIGH |
| (ref) | **Bedrock citations** — Geva *FFN Layers Are KV Memories* (FFN=KV store = the literal "LLM-as-DB" basis) + *Dissecting Recall* (subject-enrich→attribute-extract, underlies entity-vs-attribute-local). | foundations | — | reference for F1 | — | — |

**Sequencing (J):** D8 is **free + immediate** (test against the instrument sweep already queued). D11/D13 are **F1-framing** (the thesis's two strongest external threats — must be confronted in the readiness write-up, no new compute). D9 (NeuralDB) + D15 (cross-arch) need a **read/verify** before they gate any effort. D12/D14 are cheap no-GPU mechanism/band checks. None promotes without its own falsifying test (DISCIPLINE §3 — co-citation = lead, not evidence).

### J.2 — MEMOIR + foundations-variant graphs (2026-06-21, graphs 4–5)
Two more operator graphs (seeds **MEMOIR** lifelong-editing + a 2nd **foundations** neighborhood). Heavy overlap with the central cluster (AlphaEdit/NeuralDB/WISE/Mirage/Built-on-Sand/SADR/O-Edit/Model-Editing-at-Scale) → confirms the core. The foundations-variant adds the **lifelong adapter/routing family** (LEMoE, Reversible Routing-LoRA, RAG Continuous-Prompt, In-Context Editing, SCEN) — all **reinforce D9** (gated/routed side-store) + **D13** (in-context). **Two GENUINELY NEW high-value leads** (the field has *named our problem and our confound*):

| # | Lead (source paper) | Maps to | Why it matters | Status |
|---|---|---|---|---|
| D16 | **KEO / SetKE** — *Knowledge Editing for Knowledge Elements Overlap* (2025): names **"Knowledge Element Overlap (KEO)"** — triplets sharing a common element cause editing conflicts/degradation — and proposes **Knowledge Set Editing** (edit the overlapping set jointly) + benchmark **EditSet**. | **G6.1/D1** (problem) + **A1** (solution) | **The field's name for our exact cross-entity same-relation corruption** (facts sharing the relation element) — AND their joint set-edit fix is conceptually **our A1 batch result**. Strong external mapping of both our problem and our solution; EditSet is a ready benchmark. | OPEN — compare/read before F1 cites ours as novel |
| D17 | **Editing Overfit / EVOKE** — *Uncovering Overfitting in LLM Editing* (2024): edited models assign **disproportionately high prob to the edit target** ("Editing Overfit"), hurting generalization; benchmark **EVOKE** + metrics; common mitigations ineffective. | **E1** (margin confound) | **External naming + benchmark of our E1 margin confound** (compute_z inflates edited margins, median 0.979). Corroborates E1 and gives a named benchmark to measure it. | OPEN — strengthens E1 |

**Reinforcements (not new):** MEMOIR (sparse activation masks → edits occupy **disjoint** param subsets + activation-pattern routing) and SCEN (per-fact expert + indexing neuron) and InComeS (gist-token KV compression + cross-attention selection) are all **D9 side-store/routing variants** — three more independent votes that the field's answer to our corruption is "route edits to disjoint/gated stores." *Retention-after-fine-tuning* (edited knowledge forgets faster under downstream FT) → minor **F2** durability lead. *RippleCOT* + *Multi-Hop Factual Shortcuts* (~20% of failures = pretraining-co-occurrence shortcuts) → **E4/D11**.

### J.3 — MEMORYLLM graph (2026-06-21, graph 6) — self-updatable parametric memory
Seed **MEMORYLLM**; neighborhood = long-context (Infini-attention, StreamingLLM, InfLLM, RULER, LongBench, LongLoRA…) + self-updatable-memory architectures. Mostly the **"context/external-memory instead of weight-editing" contrast class** → reinforces **D13**. Diminishing returns on this axis (flagged). **One new lead:**

| # | Lead | Maps to | Why it matters | Status |
|---|---|---|---|---|
| D18 | **Self-updatable parametric memory** — MEMORYLLM / M+ (scalable long-term memory) / **Larimar** (episodic memory control) / **MemLLM** (finetune LLM to use an explicit **read-write memory**). | B3 / D9 / **spec read-write contract** | The architectural **midpoint** between diffuse in-weight editing and external RAG: a model with an **explicit, updatable read/write memory interface** — the closest published cousin to the LLM-as-database **read/write contract** itself (not just the write side). Larimar/MemLLM are the ones to read for the spec's interface positioning. | OPEN — spec-positioning read; not a falsifier |

### J.4 — MoE / Parametric-Knowledge-Injection graph (2026-06-21, graph 7)
Seed *Decoupled MoE for Parametric Knowledge Injection*; 0 overlap with the editing graphs (different cluster: Parametric-RAG + frozen-LM-reader + legal-IR co-author noise). One new lead:

| # | Lead | Maps to | Why it matters | Status |
|---|---|---|---|---|
| D19 | **Parametric RAG / per-query knowledge injection** — Parametric RAG, Decoupled-MoE, GenPoE, "Decoupling Knowledge and Context via Cross-Attention": encode retrieved knowledge into **transient per-query adapter/expert parameters** at inference. | B3 / D9 / D13 / spec offline-edit-vs-online-inject | A **third paradigm** between diffuse in-weight editing and context-RAG — bears on the spec's edit-offline-vs-inject-online design choice and the B3 in-weight-necessity question. | OPEN — spec-positioning read |

**Also-relevant (minor):** *Large Scale Knowledge Washing* (deletion at scale) + *Forgetting before Learning* (parametric arithmetic updating) → **NEW-4** (DELETE write-type). *Adaptive Token Biaser* / *Outdated-Issue-Aware Decoding* → decoding-time edit handling (a D13 variant). Long-context methods themselves = out of scope for in-weight editing.

**Cumulative graph-review verdict (6 graphs):** the central editing cluster is **well-mapped and saturating**; new graphs now mostly re-surface known nodes. Net yield = leads **D8–D18** + E1/E4 strengthened. The dominant cross-graph signal is unchanged and strong: **the field routes edits to gated/disjoint/explicit side-stores (D9/D18) or avoids weight edits via context (D13); diffuse in-weight editing has a named failure mode (KEO/D16) and a named confound (Editing-Overfit/D17).** This is the F1 in-weight-necessity question (B3) — the highest-value next analysis. Further editing-neighborhood graphs = strong diminishing returns ([[evidence-over-scaffolding]]).


**D-D1-2 closure (2026-06-21):** D8 norm-growth lead folds into the §8.7 instrument result — **D-D1-2** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤2`** (max unanchored per-relation concentration; anchor before k=3). Dual-reviewed (Opus advisor + gpt-5.5 cross-family). k=3-4/k=10-12 = scoped order-dominated observations, NOT portable thresholds; per-relation count = fail-closed SENTINEL not the causal var (edit-set/key-collinearity geometry is). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. Artifacts: results/d1_threshold_lowk_3b_s3{,_lowextra}.json, results/d1_instrument_variance_diagnostic_3b_*.json; reviews logs/codex_review_threshold_*OUT.log.
