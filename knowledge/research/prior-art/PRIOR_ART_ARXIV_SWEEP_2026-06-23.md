# Editing / Memory / Eval Prior-Art arXiv Sweep — 2026-06-23

_Comprehensive arXiv sweep of the **editing/memory/eval paper axis** (the §J/§K axis), keyed to §0.3 (CP2 → D20 → 7B/GQA → F1). Six parallel search agents, one per sub-axis (+1 CP2 rerun). The **paper-side counterpart** to the repo sweep (`docs/PRIOR_ART_REPO_SWEEP_2026-06-23.md`, register §M) and a refresh of the ConnectedPapers graph review (register §J, which had flagged this cluster "saturating")._

> **FENCE (binding, DISCIPLINE §1/§3):** every entry is a **LEAD** — an arXiv paper verified to *exist* with the stated title/date, **NOT** read in full and **NOT** verified on our stack. Abstract-level relevance only. Nothing here is `CORPUS/` evidence; each lead is folded into F1 *framing* or falsified by our own pre-registered test before any promotion ([[verify-external-artifacts-before-effort]]).
> **✅ Verification (performed by the main agent, not just the subagents):** `export.arxiv.org/api` HTTP-429 rate-limited the parallel *subagents* mid-sweep, so they fell back to abs-page/WebSearch channels. Because asserted-by-the-tool-that-mislabeled-HYPE is not independent verification, **all 57 reported arXiv IDs were then batch-verified by the main agent in two `id_list=` export-API calls on 2026-06-23 — every ID returned with a title matching its table row; zero missing, zero confabulations** ([[verify-external-artifacts-before-effort]]). IDs are real (2025–2026 = 2505.*–2606.*, valid as of today). Caveats that remain: abstracts were **not read in full** (relevance is abstract-level; a few model-size fields are "not stated," not inferred), and **2505.18343's published title genuinely is "…Graph-Based External Memory" but the method is in-weight "HYperbolic Parameter Editing"** (the one title-vs-method trap; caught + reclassified, see N6).
> **No tool install was required** — the official arXiv API + WebSearch/WebFetch sufficed; the audited arXiv-MCP servers (unvetted, single-author) were deliberately NOT installed.

---

## 0. The load-bearing findings (what changes an open-question framing)

These **sharpen, temper, or complicate** an open §0.3 cell — distinct from the many confirmatory papers in the per-axis tables. **Verbs calibrated; cross-family/cross-metric analogs are NOT corroboration of our own results** (the LocFT lesson, [[editing-memory-eval-prior-art-landscape]]).

1. **⚠ N1 — CP2 novelty REFRAMED: a formal query-language-over-a-network EXISTS (Grohe), but not over *decoded facts*.** **Grohe et al., "Query languages for neural networks"** ([2408.10362](https://arxiv.org/abs/2408.10362), ICDT 2025) + follow-up [2601.09381](https://arxiv.org/abs/2601.09381) define **FO(SUM) — an explicit "abstraction of SQL"** — as a declarative query language over a **network-as-weighted-graph** (aggregation/recursion over weight terms; worked queries: #edges/#weights/#triangles). This is the **closest formal cousin to LQL/LARQL and serious foundational prior art we must cite.** **BUT it queries the NUMERIC weight/neuron structure, one level BELOW factual knowledge** — the paper explicitly "does not mention factual (subject, relation, object) tuples." → **Calibration of §M's M1:** the claim "query-DSL-over-weights is LARQL-only" is **too strong at the formal level** (Grohe got there first, numeric altitude); it **holds at the FACTUAL-readback altitude** — no paper proposes a structured READ/QUERY contract over a model's *decoded* in-weight facts (SELECT facts / negation / "violates" / multi-hop / reverse over s-r-o). CP2 sits in the empty cell between Grohe (numeric) and "Crawling the Internal KB" ([2301.12810](https://arxiv.org/abs/2301.12810), prompt-extraction of an s-r-o KG, not a query language). (Maps: **CP2 / M1 / K1**.)

2. **⚠ N2 — D20's framing PREMISE is itself untested, and one adjacent paper complicates it.** The exact **sub-batched closed-form (MEMIT-style) compaction at the ~2000 boundary** question is **unaddressed** in the literature. The nearest neighbor — **"Is Bigger Edit Batch Size Always Better?"** ([2405.00664](https://arxiv.org/abs/2405.00664), Llama-3, MEMIT/ROME/EMMET to 4096) — defines the sequential-batch hybrid but **(a)** measures **general/downstream degradation, NOT cross-entity read corruption**, **(b)** does **no compaction**, and **(c) ⚠ finds smaller sequential batches degrade LESS than one big joint batch** → this points **AGAINST D20's premise** that "the single joint solve is the clean reference and sub-batching reintroduces corruption." So D20's batch-clean-vs-subbatch-corrupts assumption is itself a **falsifiable, untested claim** with one complicating data point — must be stated, not assumed, in D20/F1. The closest *mechanistic* neighbor is **RLSEdit** ([2601.15686](https://arxiv.org/abs/2601.15686), soft recursive-least-squares = closed-form recursive lifelong update) — worth a deep read. (Maps: **D20 / D-B3N-1 cond.3**.)

3. **⚠ N3 — OQ-W1 GQA edit-transfer is UNADDRESSED at the paper level too** (confirms §M/M3 from the repo side — now both repos *and* papers). Every GQA×editing query returned zero; papers edit GQA models (Llama-2/3, Qwen2.5-7B, Qwen3-8B) but treat GQA as incidental — none characterizes an edited K/V direction propagating through `repeat_interleave` to a whole group. Genuine white space. (Maps: **K6**; OQ-W1's GQA half.)

4. **⚠ N4 — a sharper OQ-W1 risk than GQA: Qwen stores facts in EARLY ATTENTION, not mid-MLP.** "Do All Autoregressive Transformers Remember Facts the Same Way?" ([2509.08778](https://arxiv.org/abs/2509.08778), known) finds the **Qwen family concentrates factual recall in early *attention* layers, not the mid-MLP band** other models use → a **direct caution that our MLP `down_proj` band [4-8] recipe may not transfer cleanly to Qwen at scale, independent of GQA.** This is the more load-bearing OQ-W1 signal. Supporting: ACE ([2510.07896](https://arxiv.org/abs/2510.07896)) edits Q→V neuron pathways on **Qwen3-8B**; Golden-Layers/LGA ([2602.20207](https://arxiv.org/abs/2602.20207)) = layer-choice-as-function-of-architecture; IFMET ([2410.06331](https://arxiv.org/abs/2410.06331)) = multi-hop recall uses deeper MLP than single-hop. **No 2025–26 paper does an in-study model-size sweep of recipe+drift-threshold transfer to 7B** → also unowned. (Maps: **OQ-W1 / B1 / C2-band**.)

5. **⚠ N5 — the eval-critique cluster is NOT saturated; three NEW existential threats to the in-weight thesis.** Beyond QAEdit/Sand/EVOKE, F1 must confront: **[2606.00570](https://arxiv.org/abs/2606.00570)** ("Revisiting Parameter-Based KE: Theoretical Limits" — **autoregressive** eval + a **"dimensional-collapse" theory** → parameter editors damage core abilities and **lose to a retrieval baseline**); **[2604.05995](https://arxiv.org/abs/2604.05995)** ("The Model Agreed But Didn't Learn" — edits = **surface compliance**, internal belief unchanged); **[2510.17941](https://arxiv.org/abs/2510.17941)** ("Believe It or Not" — measures how *shallowly* implanted facts are believed). These add a **theoretical-limits argument** + a **belief-depth/surface-compliance** framing we don't yet have. New shared benchmarks to report against: logical-rule entailment ([2606.10554](https://arxiv.org/abs/2606.10554)), TRACK multi-hop-under-conflict ([2601.15495](https://arxiv.org/abs/2601.15495)), ground-truth-free locality ([2601.17343](https://arxiv.org/abs/2601.17343)), EtCon TF-vs-AR gap ([2512.04753](https://arxiv.org/abs/2512.04753)). (Maps: **E-cluster / F1 / D11 / D13**.)

6. **⚠ N6 — B3 NEW lit is genuinely MIXED → reinforces the scope-keyed hybrid (D-B3N-1), with a NEW in-weight-FAVORING counterweight.** The strongest new head-to-head, **User-as-Engram** ([2606.19172](https://arxiv.org/abs/2606.19172)): local **parametric** edits **OVERTAKE a retrieval pipeline past ~100 facts**, ~33,000× smaller footprint, zero per-query context cost — a citable **in-weight-favoring** crossover. ⚠ **Sign-flip caught:** two papers titled "…external memory" — **HYPE** ([2505.18343](https://arxiv.org/abs/2505.18343), "HYperbolic Parameter Editing") and **MeG** ([2512.14395](https://arxiv.org/abs/2512.14395), dynamic weight generation) — are **actually in-weight editors**, do NOT count toward side-store convergence. Side-store/in-context convergence still holds for the incremental/lifelong regime (RECIPE [2405.03279](https://arxiv.org/abs/2405.03279), ERASE [2406.11830](https://arxiv.org/abs/2406.11830), DR-IKE [2510.21059](https://arxiv.org/abs/2510.21059), LMLM [2505.15962](https://arxiv.org/abs/2505.15962)). Net: sharpens the discriminator to **per-query-context-cost vs edit-count crossover**, not a blanket "side-store wins." (Maps: **B3 / D9 / D-B3N-1**.)

7. **N7 — G7 multi-token is a crowded PORT target (confirms §M).** **FABLE** ([2604.12559](https://arxiv.org/abs/2604.12559), beats UnKE/AnyEdit, code) is the strongest new port candidate; RILKE ([2511.20892](https://arxiv.org/abs/2511.20892)), EtCon ([2512.04753](https://arxiv.org/abs/2512.04753)), CoRSA ([2602.03696](https://arxiv.org/abs/2602.03696)) follow. G7 = port + re-tune for our N=100 same-relation batch, not a from-scratch method. (Maps: **G7 / K7**.)

8. **⚠ N8 — our cross-entity corruption MECHANISM cell is UNDER-ADDRESSED (contribution space).** The strongest recent mechanism papers — MEMIT-Merge ([2502.07322](https://arxiv.org/abs/2502.07322)), RoSE ([2603.15518](https://arxiv.org/abs/2603.15518)), [2502.06868](https://arxiv.org/abs/2502.06868) — are all **same-SUBJECT** (identical/collinear keys from one shared subject forced to different values). **Our cell is same-RELATION / different-entity** (different subjects whose keys share a relation *direction*) — **a different phenomenon.** No paper directly models same-relation-direction subspace corruption of held-out entities. Closest = **Knowledge in Superposition** ([2408.07413](https://arxiv.org/abs/2408.07413), derives the canonical "interference term" for corruption of *unrelated* facts, code) → best framing: our same-relation corruption as a **specialization of the superposition/interference account**, with spectral/singular-direction disruption ([2505.12636](https://arxiv.org/abs/2505.12636), [2502.19416](https://arxiv.org/abs/2502.19416)) secondary. (Maps: **D2 / D7 / D12 / G6.1**.)

---

## 1. CP2 — query/read contract over weights

| arXiv ID | Title | Date | What it does | query-DSL-over-weights? |
|---|---|---|---|---|
| [2408.10362](https://arxiv.org/abs/2408.10362) | Query languages for neural networks (Grohe et al., ICDT'25) | 2024-08 | **FO(SUM) ≈ SQL** over a network-as-weighted-graph; white-box aggregation queries | **YES — numeric weight graph, NOT decoded facts.** Closest formal cousin to LQL. |
| [2601.09381](https://arxiv.org/abs/2601.09381) | Query Languages for ML Models (Grohe) | 2026-01 | FO(SUM)+IFP(SUM) recursion; expressiveness/complexity | YES — same numeric altitude |
| [2301.12810](https://arxiv.org/abs/2301.12810) | Crawling the Internal Knowledge-Base of LMs (Cohen/Geva/Berant) | 2023-01 | Extracts an (s,r,o) KG from an LM by prompt-crawling (82–92% precision) | NO — prompt extraction to external graph; closest *factual* cousin |
| [2505.15962](https://arxiv.org/abs/2505.15962) | LMLM — Limited-Memory LMs (externalize facts to a DB at pretrain) | 2025-05 | Pretrains a model that stores facts in an **external DB**, inspectable/updatable | NO — externalize-to-external-DB; LLM-as-DB-adjacent |
| [2402.14273](https://arxiv.org/abs/2402.14273) · [2505.19286](https://arxiv.org/abs/2505.19286) | LMs as KBs at Scale · Graph-Perspective probing | 2024–25 | NL-probe LM-as-KB · correlate knowledge with graph properties | NO — NL-probing/analysis |

**Verdict:** factual query-contract genuinely novel (empty cell between Grohe-numeric and prompt-extraction); **must cite Grohe as formal prior art** and position LQL as its factual-knowledge specialization. (Do NOT double-count LARQL/vindex — that's the program's own prior art, §K.)

## 2. D20 — mass/sequential editing at scale + collapse + compaction

| arXiv ID | Title | Date | Relevance |
|---|---|---|---|
| [2405.00664](https://arxiv.org/abs/2405.00664) | Is Bigger Edit Batch Size Always Better? (Llama-3) | 2024-05 | **Closest to the mechanism** — sequential-batch hybrid, MEMIT/ROME/EMMET to 4096; **smaller seq batches degrade LESS** (complicates D20 premise); general-degradation metric, no compaction |
| [2601.15686](https://arxiv.org/abs/2601.15686) | Soft Recursive Least-Squares for Lifelong Editing (RLS) | 2026-01 | Closed-form recursive lifelong update — closest *mechanistic* neighbor to sub-batched closed-form |
| [2502.19416](https://arxiv.org/abs/2502.19416) | Norm Growth & Stability in Localized Sequential KE | 2025-02 | Clean collapse-cause: edited-matrix Frobenius norm grows monotonically; subspace shift (distinct from Norm-Anchors) |
| [2401.07453](https://arxiv.org/abs/2401.07453) · [2406.11263](https://arxiv.org/abs/2406.11263) | Editing at Scale → Gradual & Catastrophic Forgetting · Understanding LLM Collapse in Editing | 2024 | Two-phase collapse characterization; root-cause |
| [2503.00035](https://arxiv.org/abs/2503.00035) (EAC) · [2506.12384](https://arxiv.org/abs/2506.12384) (R-SFT+merge) | Editing-Anchor Compression · Model Merging for KE | 2025 | The two "compaction/merge" near-misses — **both gradient-FT/anchor-prune, NOT closed-form sub-batch** |
| [2505.15702](https://arxiv.org/abs/2505.15702) (LyapLock) · [2510.01172](https://arxiv.org/abs/2510.01172) (SPHERE) · [2606.19679](https://arxiv.org/abs/2606.19679) (LOKI) · [2605.11836](https://arxiv.org/abs/2605.11836) (Lifelong-Norm) · [2605.08143](https://arxiv.org/abs/2605.08143) (HoReN) · [2510.16089](https://arxiv.org/abs/2510.16089) (STABLE) | Various lifelong-collapse mitigations | 2025–26 | Preservation-bound / energy / null-space / normalization / Hopfield families — runnable mitigations to test against |
| [2512.14395](https://arxiv.org/abs/2512.14395) (MeG) · [2508.03741](https://arxiv.org/abs/2508.03741) (Latent Scalpel) · [2510.22139](https://arxiv.org/abs/2510.22139) (sparse-mask) | Massive/dynamic-weight editing | 2025 | "Massive" edits via hypernetwork/latent/sparsity (counts not always stated) |

**Verdict:** sub-batched-closed-form-MEMIT-compaction-at-2000 is **unaddressed**; D20 stays a real open opportunity, but its premise needs the [2405.00664](https://arxiv.org/abs/2405.00664) complication folded in.

## 3. 7B / GQA transfer (OQ-W1)

| arXiv ID | Title | Date | Relevance |
|---|---|---|---|
| [2509.08778](https://arxiv.org/abs/2509.08778) | Do All Autoregressive Transformers Remember Facts the Same Way? (known) | 2025-09 | **⚠ Qwen = early-attention recall, not mid-MLP** → cautions our `down_proj` band recipe may not transfer to Qwen |
| [2510.07896](https://arxiv.org/abs/2510.07896) | ACE: Attribution-Controlled KE for Multi-hop | 2025-10 | Q→V neuron-pathway editing on **Qwen3-8B** (our family) |
| [2602.20207](https://arxiv.org/abs/2602.20207) | Golden Layers (LGA) | 2026-02 | Layer-choice via gradient analysis "across LLM types" |
| [2410.06331](https://arxiv.org/abs/2410.06331) (IFMET) · [2408.15091](https://arxiv.org/abs/2408.15091) (Relation Also Knows) | Multi-hop uses deeper MLP · recall is relation-focused | 2024 | Where-to-edit / depth evidence |
| [2606.00570](https://arxiv.org/abs/2606.00570) | Revisiting Parameter-Based KE: Theoretical Limits | 2026-05 | Dimensional-collapse capacity argument (also §5) |
| [2605.16686](https://arxiv.org/abs/2605.16686) (tensor-MEMIT MoE) · [2602.10965](https://arxiv.org/abs/2602.10965) (MoEEdit) | Editing MoE LLMs | 2026 | Architecture-dependence axis (MoE, not GQA) |

**Verdict:** GQA-transfer unaddressed (N3); the sharper risk is N4 (Qwen attention-vs-MLP storage); no in-study size-sweep of recipe+threshold transfer.

## 4. Eval / falsification (F1)

| arXiv ID | Title | Date | Threat/benchmark |
|---|---|---|---|
| [2606.00570](https://arxiv.org/abs/2606.00570) | Revisiting Parameter-Based KE: Theoretical Limits | 2026-05 | **Existential** — AR eval + dimensional-collapse → editors lose to retrieval |
| [2604.05995](https://arxiv.org/abs/2604.05995) | The Model Agreed But Didn't Learn (surface compliance) | 2026-04 | **Existential** — edits = surface mimicry, belief unchanged |
| [2510.17941](https://arxiv.org/abs/2510.17941) | Believe It or Not (belief-depth of implanted facts) | 2025-10 | **Existential** — how shallowly facts are believed |
| [2601.17343](https://arxiv.org/abs/2601.17343) · [2512.04753](https://arxiv.org/abs/2512.04753) | Are We Evaluating Edit Locality Properly? · EtCon (TF-vs-AR gap) | 2026/25 | Locality re-definition · teacher-forcing-vs-autoregressive gap |
| [2601.15495](https://arxiv.org/abs/2601.15495) (TRACK) · [2606.10554](https://arxiv.org/abs/2606.10554) (logical-rule entailment) | Multi-hop under conflict · entailed-question benchmark | 2026 | Shared benchmarks to report against |
| [2605.05090](https://arxiv.org/abs/2605.05090) · [2506.03490](https://arxiv.org/abs/2506.03490) (MedEditBench) · [2606.00477](https://arxiv.org/abs/2606.00477) (UniKE cross-modal) · [2605.06096](https://arxiv.org/abs/2605.06096) (EC-Bench) | Side-effect auditing · domain/modality generalization-failure benches | 2025–26 | Locality/shortcut evidence (domain/multimodal) |

⚠ [2602.01977](https://arxiv.org/abs/2602.01977) (EVK-Bench) is **WITHDRAWN** — cite cautiously. **Verdict:** critique cluster NOT saturated; N5 trio is mandatory F1 reading.

## 5. In-weight vs side-store (B3/D9)

| arXiv ID | Title | Date | Class / sign |
|---|---|---|---|
| [2606.19172](https://arxiv.org/abs/2606.19172) | User as Engram (local parametric edits vs retrieval) | 2026-06 | **in-weight-FAVORING** — edits overtake retrieval past ~100 facts |
| [2505.18343](https://arxiv.org/abs/2505.18343) (HYPE) · [2512.14395](https://arxiv.org/abs/2512.14395) (MeG) | "external memory"-titled but actually **in-weight** | 2025 | ⚠ sign-flip — NOT side-store evidence |
| [2405.03279](https://arxiv.org/abs/2405.03279) (RECIPE) · [2406.11830](https://arxiv.org/abs/2406.11830) (ERASE) · [2510.21059](https://arxiv.org/abs/2510.21059) (DR-IKE) · [2505.15962](https://arxiv.org/abs/2505.15962) (LMLM) | Gated retrieval-of-soft-prompts · editable external KB · policy-optimized in-context retriever · externalize-to-DB | 2024–25 | side-store / in-context convergence (incremental regime) |
| [2503.07903](https://arxiv.org/abs/2503.07903) (MemReasoner) · [2409.19401](https://arxiv.org/abs/2409.19401) (EMG-RAG) | Episodic-memory architecture · editable memory-graph RAG | 2024–25 | self-updatable / editable-store |

**Verdict:** MIXED → reinforces D-B3N-1 scope-keyed hybrid; User-as-Engram is the citable in-weight counterweight (N6).

## 6. Multi-token (G7) + corruption mechanism (D2/D7/D12)

| arXiv ID | Title | Date | Category |
|---|---|---|---|
| [2604.12559](https://arxiv.org/abs/2604.12559) | FABLE — fine-grained fact anchoring (beats UnKE/AnyEdit, code) | 2026-04 | **G7 — strongest port candidate** |
| [2511.20892](https://arxiv.org/abs/2511.20892) (RILKE) · [2512.04753](https://arxiv.org/abs/2512.04753) (EtCon) · [2602.03696](https://arxiv.org/abs/2602.03696) (CoRSA) | Representation-intervention lifelong · edit-then-consolidate · conflict-resolving multi-update | 2025–26 | G7 / multi-update |
| [2408.07413](https://arxiv.org/abs/2408.07413) | Knowledge in Superposition (interference term, code) | 2024-08 | **Mechanism — closest to our cross-entity cell** (unrelated-fact corruption via superposition) |
| [2505.12636](https://arxiv.org/abs/2505.12636) | Deceptiveness of KE / Superficial Editing (attention-head + singular dirs) | 2025-05 | Mechanism — attention-drift + spectral (secondary) |
| [2502.07322](https://arxiv.org/abs/2502.07322) (MEMIT-Merge) · [2603.15518](https://arxiv.org/abs/2603.15518) (RoSE) · [2502.06868](https://arxiv.org/abs/2502.06868) | Same-SUBJECT key collision / activation drift | 2025–26 | ⚠ **same-subject ≠ our same-relation** — different phenomenon |
| [2604.05876](https://arxiv.org/abs/2604.05876) (MCircKE) · [2510.07896](https://arxiv.org/abs/2510.07896) (ACE) | Circuit-level / neuron-pathway propagation | 2026 | Mechanism (multi-hop application gap) |

**Verdict:** G7 = port target (FABLE); the same-relation/different-entity corruption mechanism is an **under-addressed cell = our contribution space** (N8).

---

## 7. Sequencing & reconciliation with §M

- **§0.3 ORDER unchanged** (CP2 → D20 → 7B → F1). Papers complement the §M repos: where §M found *runnable code*, this sweep finds the *claims/critiques/mechanisms* to frame F1 against and the *premises to stress-test*.
- **The three calibrations that matter most** (don't let an unread abstract move confidence — the LocFT lesson): **N1** tempers §M/M1 (Grohe formal prior art exists at the numeric level); **N2** says D20's own batch-clean premise is untested + one paper complicates it; **N4** flags a concrete OQ-W1 risk (Qwen early-attention storage) sharper than the GQA question.
- **F1 must newly confront** the N5 existential trio (dimensional-collapse/retrieval-wins, surface-compliance, belief-depth) — these are not in our current citations.
- **Contribution space confirmed** (white cells): factual query-contract (CP2, vs Grohe-numeric), same-relation-direction corruption mechanism (N8), GQA edit-transfer (N3), in-study 7B recipe+threshold size-sweep (N4).
- **Highest-leverage bounded reads if/when taken** (all operator-gated, none started): [2405.00664](https://arxiv.org/abs/2405.00664) (D20 premise) + [2601.15686](https://arxiv.org/abs/2601.15686) RLSEdit (closed-form lifelong); [2606.00570](https://arxiv.org/abs/2606.00570) (F1 existential); [2408.07413](https://arxiv.org/abs/2408.07413) (our corruption mechanism); [2408.10362](https://arxiv.org/abs/2408.10362) Grohe (CP2 positioning). None promotes without its own pre-registered falsifier on our stack.

_Generated 2026-06-23 from a 6+1-agent parallel arXiv sweep; every ID page-verified on arxiv.org. Register pointer: §N._
