# Editing / Memory / Eval Prior-Art Repo Sweep — 2026-06-23

_Comprehensive GitHub sweep of the **editing/memory/eval implementation axis** (the §J/§K axis), keyed to the current §0.3 priorities: **CP2 (read/query contract) → D20 (compaction-at-scale) → 7B/GQA transfer (OQ-W1) → F1**. Six parallel search agents, one per sub-axis; **every repo verified live via the GitHub REST API on 2026-06-23** (stars / last-push / language / archived). This is the high-yield counterpart to the LOW-yield general-tooling batch (register §L)._

> **FENCE (binding, DISCIPLINE §1/§3):** every entry is a **LEAD** — verified to *exist* on GitHub with the stated metadata, **NOT verified on our Qwen2.5-3B/7B + AlphaEdit + Q4_K_M stack**. None has been run by us. Co-existence ≠ corroboration. Nothing here is `CORPUS/` evidence; each lead must be falsified by our own pre-registered test or folded into F1 *framing* before any promotion ([[verify-external-artifacts-before-effort]], [[prototype-tautology-trap]]).
> **⚠ Search caveat:** authenticated GitHub *code*-search was unavailable to the agents (web + repo-name/keyword only). A brand-new, low-star repo (esp. a query-DSL-over-weights) could be missed; the major named candidates per axis are covered.

---

## 0. The six load-bearing findings (what actually changes our open questions)

These are the items that **sharpen or pre-empt** an open §0.3 cell — distinct from the many merely-confirmatory repos catalogued below.

1. **CP2 — no query-*DSL* over weights surfaced among the obvious read-side neighbors (search-bounded, not exhaustive).** Swept both edit-side and read/inspect-side. The read-side neighbors that *do* access internal knowledge — **PatchScopes, nnsight, SelfIE, TransformerLens, LAMA** — all do so via **natural-language probing or Python intervention APIs, NOT a declarative query DSL** with relational/typed semantics (SELECT/WALK/INFER + aggregation/negation/multi-hop/reverse/"violates"). **NeuralDB** (2507.18028) states the "weights-as-queryable-KV-database" *concept* but ships **no code and no query language**. → Supports (does not prove) that the CP2 read/query contract is **novel**: claim is "no query-DSL surfaced among the obvious neighbors via name/web search," NOT "verified none exists." **⚠ Authenticated GitHub code-search was unavailable** — a brand-new low-star DSL repo could be missed; this is the claim we most *want* true, so hold it as search-bounded. Substrates to build on: [nnsight](https://github.com/ndif-team/nnsight) + [mega002/ff-layers](https://github.com/mega002/ff-layers). (Maps: **CP2** / **K1**.)

2. **⚠ Compaction-at-scale (D20) — the field has RUNNABLE mitigation baselines, but they are NOT A1 corroboration and do NOT exercise the D20 mechanism.** Unlike most axes this one is **not thin in code**. The 2025–26 sequential-collapse-mitigation wave converges on one story: **long sequential editing collapse is real, is driven by edited-matrix NORM GROWTH, and is mitigable by anchoring to the unedited-base norm** ([ENCORE](https://github.com/scalable-model-editing/encore) 10K / [NAS](https://github.com/SasyaTitech/NAS) ~20K — both closed-form-editor drop-ins). **⚠ Calibration (advisor):** **LocFT-BF** (100K/72B, "breadth-first beats depth-first") is **gradient fine-tuning**, not closed-form MEMIT — its batch-vs-sequential contrast is a **cross-family ANALOG, not corroboration of our A1 MEMIT single-joint-solve result**. And **D20's actual falsifier is MEMIT compaction being SUB-BATCHED at the ~2000 boundary** (multiple *sequential closed-form* solves); LocFT's gradient-FT pipeline **does not touch that mechanism** → it is **neither an A1 corroboration nor a D20 pre-emption** (different method family AND different mechanism). What IS load-bearing: ENCORE/NAS give us **runnable norm-anchoring mitigations to test against** our sub-batched compaction, and the norm-growth diagnosis aligns with D8. (Maps: **D20 / D8**; A1 link DEMOTED to cross-family analog.)

3. **⚠ The GQA K/V edit-transfer sub-question (K6) is narrowed — but OQ-W1's 7B numeric-threshold transfer is UNTOUCHED.** **No public repository characterizes knowledge-editing edit-transfer under GQA.** Mechanism (verified): every mainstream editor (EasyEdit, AlphaEdit, AnyEdit, UltraEdit, LocFT) edits **MLP down/up-proj** weights, where GQA's K/V head-sharing is **architecturally orthogonal** — so they edit GQA models routinely *without ever touching the GQA mechanism*. **Our inference (NOT verified):** our recipe also edits `down_proj` (band [4-8] MLP), so **GQA's `repeat_interleave` is *likely* orthogonal to our edit site too** → this narrows **K6** (the GQA edit-transfer sub-concern). **⚠ Scope (advisor): this does NOT narrow OQ-W1 proper** — OQ-W1 = does the recipe's *numeric threshold transfer to 7B via determinism*, an MLP-side question the GQA orthogonality says nothing about. The genuinely-uncharacterized case (an edited **K/V** direction hitting all heads in a group) is open **everywhere** — we'd be first if we test it; **pyvene** is the instrument. (Maps: **K6** narrowed; **OQ-W1 / B1** untouched.)

4. **G7 (multi-token) is NOT novel territory — there is a ready port path.** Contrast with CP2: multi-token/long-form editing is a **crowded, active** field. **AnyEdit** (autoregressive chunk-wise, plug-and-play over MEMIT/AlphaEdit, up to 458-token objects) is the canonical method; **UnKE** (+UnKEBench eval data) and **μKE** (fixes AnyEdit's cross-chunk dependency loss) follow. G7 has a concrete adopt/port target rather than an open void. (Maps: **G7 / K7**.)

5. **NeuralDB has NO public code — confirmed (corrects the §J D9 "GitHub-check before effort").** Verified across two agents: the paper (2507.18028) has no code link, the author has no public repos, and the only `facebookresearch/NeuralDB` (349★, **archived** 2022) is an unrelated 2021 "database-reasoning-over-text" project — **do not confuse them**. NeuralDB — the closest published cousin to our LLM-as-DB thesis — would have to be **reimplemented** to test; budget accordingly. (Maps: **D9 / B3 / CP2**.)

6. **The AlphaEdit canonical code + the sequential-null-space successor are now located.** `jianghoucheng/AlphaEdit` (448★, ICLR'25 Outstanding) is the canonical code for *our own* serve method; **EvoEdit** (sequential null-space, extends AlphaEdit's *static* null-space, 3.5× faster) is the direct successor to run against our AlphaEdit baseline. (Maps: **recipe / D20 / C2**.)

---

## 1. CP2 — read/query contract over edited weights (the biggest empty cell)

**Verdict: no competing query-DSL surfaced (search-bounded).** A structured query DSL over model-internal knowledge did not surface among the obvious read-side neighbors — they give *read/inspect access* (NL-probe or Python API) or the *FFN-as-KV foundation*, not a relational/typed query contract. ⚠ Authenticated code-search was unavailable; treat as "none surfaced," not "verified none exists."

| Repo | ★ | Last push | What it is | Relevance to CP2 |
|---|--:|---|---|---|
| **NeuralDB** (paper 2507.18028) | — | — | "Editing = querying a neural KV database"; gated non-linear FFN retrieval, 100K facts | Closest **concept** to CP2/in-weight-store. **NO CODE** (confirmed). Reimplement to test. |
| [ndif-team/nnsight](https://github.com/ndif-team/nnsight) | 967 | 2026-06-21 | Programmatic read/intervene on internals via tracing context | Most credible **substrate** to build a query layer on; gives access, not a DSL |
| [PAIR-code/interpretability](https://github.com/PAIR-code/interpretability) (patchscopes) | org | active | PatchScopes — decode hidden reps via NL inspection prompts | Read internals via **NL**, not relational query |
| [TransformerLensOrg/TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) | 3588 | 2026-06-22 | Standard mech-interp cache/patch library | Building block for a read layer; Python hooks, no DSL |
| [mega002/ff-layers](https://github.com/mega002/ff-layers) | 103 | 2021-09-05 | Geva "FFN layers are key-value memories" code | The **theoretical basis** for FFN-as-KV (and LARQL's vindex). Reference. |
| [facebookresearch/LAMA](https://github.com/facebookresearch/LAMA) | 1390 | 2024-07-07 | LM-as-KB cloze probing | Queries via **text prompts**, not weights |
| [tonychenxyz/selfie](https://github.com/tonychenxyz/selfie) · [zepingyu0512/neuron-attribution](https://github.com/zepingyu0512/neuron-attribution) · [epfml/interpret-lm-knowledge](https://github.com/epfml/interpret-lm-knowledge) | 58 / 52 / 25 | 2024–22 | Self-interpret embeddings · locate value/query neurons · extract (s,r,o) KG via cloze | Read/locate tooling; NL-probe, no DSL |

---

## 2. D20 — compaction-at-scale / sequential-collapse (the sharpest open falsifier)

**Verdict: NOT thin in code.** A heavily-implemented 2025–26 wave; the methods are small drop-ins. The frontier (RLSEdit Woodbury, REVIVE spectral) is the code-gap.

| Repo | ★ | Last push | What it implements | Scale / mechanism |
|---|--:|---|---|---|
| [ICT-STAR/LocFT](https://github.com/ICT-STAR/LocFT) | 0 | 2026-05-07 | LocFT-BF — localized FT, **breadth-first** epoch + mini-batch gradient aggregation | **100K edits / 72B**; depth-first(seq) vs breadth-first(batch) = the IV. **Corroborates A1.** (0★ but official code of 2509.22072) |
| [scalable-model-editing/encore](https://github.com/scalable-model-editing/encore) | 2 | 2025-02-04 | ENCORE — Most-Probable Early Stop + **Frobenius-norm constraint** on MEMIT/EMMET/AlphaEdit | **10K** sequential, 61% faster than MEMIT; norm-growth = named failure |
| [SasyaTitech/NAS](https://github.com/SasyaTitech/NAS) | 1 | 2026-05-06 | Norm-Anchor Scaling — rescale value vec to **unedited-base norm** (one-line drop-in) | **~20K** atomic seq edits; only baseline avoiding clear collapse; delays collapse 4× |
| [jianghoucheng/AlphaEdit](https://github.com/jianghoucheng/AlphaEdit) | 448 | 2025-10-15 | **AlphaEdit canonical code** (null-space projection; ICLR'25 Outstanding) | Seq to ~3,000 before collapse. **The code for our own method.** |
| [simplew4y/EvoEdit](https://github.com/simplew4y/EvoEdit) | 0 | 2025-10-11 | EvoEdit (2510.13851) — **sequential** null-space alignment, 3.5× faster than AlphaEdit | Direct AlphaEdit successor; the "does it reduce cross-edit corruption" comparator |
| [NUSTM/MEMIT-Merge](https://github.com/NUSTM/MEMIT-Merge) | 1 | 2025-09-11 | Merges value computation for **same-subject** facts (fixes K-V collision 50%→90%) | Maps to our **same-entity-locality** corruption — part of it is a same-entity batch artifact with a known fix |
| [jianghoucheng/NSE](https://github.com/jianghoucheng/NSE) | 12 | 2024-10-15 | Neuron-Level Sequential Editing (ACL'25) — neuron-subset + orig-weight value opt | Anti-forgetting, sequential, MEMIT-based |
| [mjy1111/PRUNE](https://github.com/mjy1111/PRUNE) · [JasonForJoy/Model-Editing-Hurt](https://github.com/JasonForJoy/Model-Editing-Hurt) (RECT) · [scalable-model-editing/rebuilding-rome](https://github.com/scalable-model-editing/rebuilding-rome) (r-ROME) | 11 / 37 / 12 | 2025 | Condition-number restraint · regularize-to-preserve · fix disabling-edits/collapse + add seq capability | Sequential general-ability preservation; plug-ins on ROME/MEMIT |
| [scalable-model-editing/unified-model-editing](https://github.com/scalable-model-editing/unified-model-editing) (EMMET) · [scalable-model-editing/efficient-model-editing](https://github.com/scalable-model-editing/efficient-model-editing) (FastMEMIT) | 29 / 5 | 2024–25 | Batched ROME/MEMIT unification · cut cov-precompute to <0.1% | **FastMEMIT directly cuts our cov-inversion cost** ([[memit-cov-inversion-not-a-hang]]) |
| [kmeng01/memit](https://github.com/kmeng01/memit) | 551 | 2024-01-31 | MEMIT official — single joint batch solve | The baseline the batch≈2000 claim rests on |
| [Thartvigsen/GRACE](https://github.com/Thartvigsen/GRACE) · [eric-mitchell/mend](https://github.com/eric-mitchell/mend) | 85 / 259 | 2024–23 | GRACE codebook side-store (1000s seq) · MEND hypernetwork | Side-store / older scale baselines |

**Code-pending frontier (do not over-weight):** [Euphoria040201/RLSEdit](https://github.com/Euphoria040201/RLSEdit) (0★, **README-only, no code yet**) — soft recursive least-squares, Woodbury online update, 10K edits, per-edit cost independent of history (highly on-target — watch for code drop). **REVIVE/REVIVEEDIT** (2601.11042) — spectral dominant-subspace preservation, up to 20K edits, claims MEMIT collapses at 3k / AlphaEdit at 8k — **no public code** (anonymized).

---

## 3. 7B / GQA transfer (OQ-W1) + editing toolkits

**Verdict: the GQA edit-transfer gap is real and confirmed in code — but our edit site (MLP `down_proj`) may make it largely orthogonal.**

| Repo | ★ | Last push | What it implements | Models / GQA / quant |
|---|--:|---|---|---|
| [XiaojieGu/UltraEdit](https://github.com/XiaojieGu/UltraEdit) | 54 | 2026-05-17 | Training/subject/memory-free lifelong edit; 1-step closed-form shift + lifelong norm | **Qwen2.5-7B-Instruct, 7B on a 24GB GPU, 2M edits** — highest stack-match |
| [ICT-STAR/LocFT](https://github.com/ICT-STAR/LocFT) | 0 | 2026-05-07 | LocFT-BF (see §2) | **Qwen2.5 7B→14B→32B→72B** (our exact ladder), Llama3-8B, Mistral-7B; edits MLP not K/V |
| [stanfordnlp/pyvene](https://github.com/stanfordnlp/pyvene) | 886 | 2026-03-06 | General intervention lib on arbitrary internals incl. **per-head/KV states** | The **instrument** to characterize GQA edit-transfer (`repeat_interleave` effect) |
| [hartvigsen-group/composable-interventions](https://github.com/hartvigsen-group/composable-interventions) | 29 | 2025-02-27 | Compose edit×unlearn×**compression**; runs `edit=memit compress=awq wbits=8` | **MEMIT × AWQ-8bit on Llama3-8B (GQA)** — closest quant-aware editing in the wild |
| [jianghoucheng/AnyEdit](https://github.com/jianghoucheng/AnyEdit) | 47 | 2025-11-06 | Autoregressive long-form editing (see §6) | Llama3-8B, **Qwen2.5-7B**; GQA not addressed |
| [zjunlp/EasyEdit](https://github.com/zjunlp/EasyEdit) | 2852 | 2026-06-22 | Reference toolkit (ROME/MEMIT/AlphaEdit/WISE/GRACE/UltraEdit/SimIE…) | **MAJOR recent update** (EasyEdit2 steering + UltraEdit/SimIE) — our vendored assets may be stale. Quantized models NOT supported. |
| [hiyouga/FastEdit](https://github.com/hiyouga/FastEdit) · [zjunlp/CaKE](https://github.com/zjunlp/CaKE) · [YJiangcm/LTE](https://github.com/YJiangcm/LTE) | 1366 / 20 / 37 | 2023–25 | One-command ROME (stale, MHA-era) · circuit-aware multi-hop · learning-to-edit | Toolkits; FastEdit pre-GQA |

**Quant-native lead (unverified repo):** MobiEdit (2506.13772) — BP-free zeroth-order ROME, mixed-precision, **Qwen2.5-3B on phone NPUs**; most quant-aware editing found but **no verifiable public repo**.

---

## 4. B3 / D9 — in-weight vs gated/routed side-store

**Verdict: the side-store family is well-implemented and benchable from ONE repo (EasyEdit). NeuralDB — the closest cousin — is the code gap.**

| Repo | ★ | Last push | What it implements | Class |
|---|--:|---|---|---|
| [zjunlp/EasyEdit](https://github.com/zjunlp/EasyEdit) | 2852 | 2026-06-22 | **Bundles WISE + GRACE + MELO + MEMOIR** under one API | **Side-store hub** — compare gated/routed side-stores vs our in-weight on the SAME read contract without porting 4 codebases. **WISE lives only here** (no standalone). |
| [Thartvigsen/GRACE](https://github.com/Thartvigsen/GRACE) | 85 | 2024-12-21 | Discrete KV codebook adaptor; ε-ball nearest-key routing | Editing side-store — purest "retrieval fires only on edited facts" |
| [qym7/MEMOIR](https://github.com/qym7/MEMOIR) · [ECNU-ICALK/MELO](https://github.com/ECNU-ICALK/MELO) · [TAL-auroraX/SCEN](https://github.com/TAL-auroraX/SCEN) · [Syon-Li/InComeS](https://github.com/Syon-Li/InComeS) | 4 / 28 / 5 / 1 | 2024–26 | Sparse-mask residual memory · neuron-indexed dynamic LoRA · per-sample expert nets · gist-token KV compression | Routed/gated side-store variants (D9 family) |
| [wangyu-ustc/MemoryLLM](https://github.com/wangyu-ustc/MemoryLLM) (+M+) · [IBM/larimar](https://github.com/IBM/larimar) · [amodaresi/MemLLM](https://github.com/amodaresi/MemLLM) | 318 / 35 / 13 | 2025–24 | Self-updating latent memory pool (~1M updates) · episodic memory + selective-forget · explicit read/write memory API | **Self-updatable parametric memory = the middle path (D18)** — strongest non-in-weight parametric baselines |
| [oneal2000/PRAG](https://github.com/oneal2000/PRAG) · [izziva/dmoe-pipeline](https://github.com/izziva/dmoe-pipeline) | 233 / 0 | 2025–26 | Parametric RAG (docs→per-query LoRA) · Decoupled-MoE injection (community port) | Per-query parametric injection (D19) |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) · [letta-ai/letta](https://github.com/letta-ai/letta) · [topoteretes/cognee](https://github.com/topoteretes/cognee) · [getzep/zep](https://github.com/getzep/zep) · [BAI-LAB/MemoryOS](https://github.com/BAI-LAB/MemoryOS) | 59k / 23k / 19k / 4.7k / 1.5k | 2026 | Universal/agent memory products | **Contrast class** (generic agent memory). zep's temporal validity windows are mildly relevant to edit-supersession. |

---

## 5. E-cluster — editing eval/benchmark harnesses (F1 honesty)

**Verdict: the field's strongest eval critiques are all runnable harnesses we can borrow + report against.** Only the negation/"shortcut" critique lacks code.

| Repo | ★ | Last push | Benchmarks | Confronts our |
|---|--:|---|---|---|
| [WanliYoung/Revisit-Editing-Evaluation](https://github.com/WanliYoung/Revisit-Editing-Evaluation) | 18 | 2025-08-27 | **QAEdit + WILD** ("Mirage of Model Editing"; 96.8%→38.5% teacher-forcing inflation) | **D11** — THE teacher-forced-vs-autoregressive harness; borrow WILD live-decoding, report on QAEdit |
| [edenbiran/RippleEdits](https://github.com/edenbiran/RippleEdits) | 57 | 2024-04-15 | Ripple effects: 6 criteria (composition, 2-hop, aliasing, relation-specificity) | **E4 / G6.1** — the field's name for our cross-entity corruption; shared benchmark |
| [Acruxos/EVOKE](https://github.com/Acruxos/EVOKE) | 7 | 2025-04-22 | EVOKE — editing-overfit metrics DP/CAP/EOS | **E1 / D17** — operationalizes our margin/over-assignment confound |
| [henryzhongsc/MQuAKE-Remastered](https://github.com/henryzhongsc/MQuAKE-Remastered) | 7 | 2026-03-29 | Cleaned multi-hop edit benchmark (fixes 33–76% MQuAKE label corruption) | Multi-hop portability — **use instead of raw [princeton-nlp/MQuAKE](https://github.com/princeton-nlp/MQuAKE)** (125★) |
| [ECNU-Text-Computing/Knowledge-Editing-Benchmark](https://github.com/ECNU-Text-Computing/Knowledge-Editing-Benchmark) | 0 | 2025-12-22 | Newest (Dec'25) **explicitly non-teacher-forced** multi-edit + portability; SCR baseline | Autoregressive multi-edit bar (D13) |
| [baixianghuang/HalluEditBench](https://github.com/baixianghuang/HalluEditBench) · [ExplainableML/WikiBigEdit](https://github.com/ExplainableML/WikiBigEdit) · [THU-KEG/Event-Level-Knowledge-Editing](https://github.com/THU-KEG/Event-Level-Knowledge-Editing) (ELKEN) · [feyzaakyurek/dune](https://github.com/feyzaakyurek/dune) · [qizhou000/UniEdit](https://github.com/qizhou000/UniEdit) | 27 / 10 / 12 / 24 / 3 | 2024–26 | 5-axis hallucination edit · 500K lifelong Wikidata · event-ripple · NL-edit locality · unified bench | Portability/locality/robustness + lifelong-scale eval data |

**No repo (port ourselves):** "Is Model Editing Built on Sand?" (2510.00625, negation/shortcut critique) — no public code; the PP/PN/NN/NP edit×test protocol is small and well-specified, port it for the negation leg of CP2's `violates`-rejection.

---

## 6. G7 — multi-token / long-form value editing

**Verdict: crowded, active, NOT novel — there is a ready port path (AnyEdit).**

| Repo | ★ | Last push | What it implements |
|---|--:|---|---|
| [jianghoucheng/AnyEdit](https://github.com/jianghoucheng/AnyEdit) | 47 | 2025-11-06 | ICML'25 — autoregressive chunk-wise editing of each chunk's key token; **plug-and-play over MEMIT/AlphaEdit**; up to 458-token objects. **The canonical G7 method to study/port.** |
| [TrustedLLM/UnKE](https://github.com/TrustedLLM/UnKE) | 24 | 2025-02-18 | ICLR'25 — unstructured KE, non-local block KV storage; ships **UnKEBench** eval data |
| [PurCL/muke](https://github.com/PurCL/muke) | 14 | 2025-08-20 | COLM'25 — μKE (Matryoshka) fixes AnyEdit's cross-chunk dependency loss |
| [THU-KEG/Event-Level-Knowledge-Editing](https://github.com/THU-KEG/Event-Level-Knowledge-Editing) | 12 | 2024-04-25 | Event-level (one edit → many facts) — multi-fact adjacent |

---

## 7. Sequencing & dedup notes

- **Author cluster:** `jianghoucheng` = AlphaEdit author; also ships **NSE, AnyEdit, EvoEdit-context**. The AlphaEdit *canonical code* (448★) is now located — we use the method but should pull the reference repo.
- **Name collision:** two distinct `EvoEdit` repos — `simplew4y/EvoEdit` (null-space, 2510.13851) ≠ `zeaoji/EvoEdit` (free-text lifelong, 2512.04545). Don't conflate.
- **Inside-EasyEdit, not standalone:** WISE, SimIE, UltraEdit-integration, NAMET, CORE all live in `zjunlp/EasyEdit` — don't hunt for separate repos.
- **No-code (reimplement to test):** NeuralDB, REVIVE, "Built on Sand", MobiEdit, DMoE(official). RLSEdit = code-pending.
- **Nothing here changes the §0.3 ORDER** (CP2 → D20 → 7B → F1), but it **arms** each cell: CP2 gets a search-bounded novelty signal + read-substrates (nnsight/ff-layers); D20 gets runnable norm-anchoring mitigation baselines (ENCORE/NAS) to *test against* — **not** A1 corroboration (LocFT is cross-family gradient-FT, doesn't exercise sub-batched MEMIT compaction); OQ-W1 gets UltraEdit/LocFT comparators on our model family + pyvene (the GQA instrument), and K6 (the GQA sub-question) is *likely* narrowed by our MLP edit-site (inference, unverified) while **OQ-W1's 7B numeric-threshold transfer stays open**; F1 eval gets QAEdit/WILD + RippleEdits + EVOKE to report against; G7 gets AnyEdit as a port target.
- **Highest-leverage single action if/when one is taken:** pull `zjunlp/EasyEdit` (current) for a side-by-side WISE/GRACE/MEMOIR-vs-in-weight bench on the same read contract (B3/D9), and `WanliYoung/Revisit-Editing-Evaluation` for the QAEdit/WILD eval-honesty bar. Both are bounded and decision-relevant. **All gated on the operator** — these are leads, not a commitment to port.

_Generated 2026-06-23 from a 6-agent parallel GitHub sweep; metadata verified live via the GitHub REST API. Register pointer: §M._
