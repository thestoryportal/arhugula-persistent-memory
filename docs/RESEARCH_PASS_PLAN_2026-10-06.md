# Research pass plan — D-C10q-rulings-1 (v2, 2026-10-06 night: v1 → Codex gpt-5.5 advisor pass `results/research_pass_advisor_v1.md` FIX-FIRST, six items folded below; executes only after the operator's morning HIL on the D-C10q-stacked verdict)

> **Operator ruling D-C10r-rulings-2 (2026-10-06, day) — supersedes the OpenResearch fences in §2 row E and the order there.** The pass starts after the autoresearch loop's first results and runs on the OpenResearch CLI (`orx` 0.2.16, installed from the release archive with a verified SHA-256; the desktop app is not used) with all of its local capabilities: projects, the experiment tree as a hypothesis ledger, agent sessions, `discover` / `paper`, evidence, and the local dashboard (`orx up`, 127.0.0.1:4791) opened for the operator's observability. No login is needed (login covers only accounts, email and managed compute). Limits: OpenResearch agents generate and log hypotheses but do not run experiments; hypotheses are run outside their domain through the program's pre-registered falsifiers. Managed or rented compute stays out (local-only). Analytics are off (`orx telemetry off`). Outputs remain leads, never CORPUS. InfraNodus (MCP, connected) is an agent tool for the run as well: gap analysis, conceptual bridges, research questions and us-versus-prior-art differences over the pass's hits and our corpus, without the two-call cap in §2 row F; its outputs are leads too.


**Ruling (operator, 2026-10-06, runbook §5.2 D-C10q-rulings-1):** before the program moves away from Qwen2.5-3B for any reason, an exhaustive research pass across paper and code repositories, then InfraNodus and other science-grounded agentic tools, surfaces every candidate solve — editing methods and model families; the 48 GB fp16 envelope, not parameter count, bounds models. **Route commitment stays with the operator (HIL).** This plan is the pass's pre-registration: what is searched, with which instruments, what counts as a hit, how it is logged, and what the operator receives. Step 0 (RESEARCH-FIRST) is done: `docs/RESEARCH_PASS_CORPUS_INVENTORY_2026-10-06.md` — the pass searches the inventory's **gap list**, not the candidate list.

## 0. Situating on the e2e map

The pass serves the §C write path against the §F/§8.9 behavioural-readback bar: C10 (a coined multi-token value written into weights must be read back through held-out paraphrases) is OPEN/BLOCKING for F1. Every candidate is judged on one question: *could it carry a five-token coined value to held-out phrasings in-weight, locally, under the strict held-out full-sequence bar (D-C10k-rulings-1)?* Side stores (WISE/GRACE/MELO, P-Tokens…) answer a different question and are logged as engineering fallbacks only (RB:305), never as F1 routes.

## 1. Branch on the D-C10q-stacked verdict (filled in after CORPUS/50)

- **NULL (the prior; run-1 echo was gain 9, described_as −7.7, ratio 1.27):** the re-aim family is exhausted on this harness. The pass runs in full (§2–§5) *before* I-1 / I-2 are pre-registered, per the ruling.
- **PARTIAL / TRADEOFF:** the pass still runs (the ruling is unconditional on leaving Qwen), but the first morning item is the capped iterated variant the prereg names; the pass's model-family half is lower priority.
- **LEAD:** replicate in a second process first; the pass's editing-method half is deferred and the model-family half is **paused, not closed** — D-C10q-rulings-1 remains unsatisfied for any model move until the pass has run (advisor item 6).

## 1a. Frozen candidate-class taxonomy (advisor item 1 — exhaustive means every class gets a disposition, not that 15 strings were searched)

Each class ends the pass with one disposition: `candidate` / `candidate-needs-C10-eval` / `lead` / `fallback` / `empty` (searched, nothing public) — see §4 for the definitions. In-scope = writes or mounts knowledge into model parameters with no read-time side store (spec §C/§F in-weight contract); `fallback` = engineering escape hatch under RB:305, never an F1 route.

| class | examples already known to the corpus | scope |
|---|---|---|
| E1 locate-then-edit, closed-form (MEMIT / AlphaEdit family; covariance, null-space, projector variants; RoSE, BLUE, MEMIT-Merge, SWEA, DiKE, PMET, AcE) | CORPUS/37–49; inventory rows 1, 7 | in-scope (the current engine) |
| E2 sequential / lifelong null-space editors (BetaEdit, SUIT, Gupta et al. cluster) | inventory 1, 3d | in-scope |
| E3 long-form / autoregressive-position editors (AnyEdit, AnyEdit++, μKE, UnKE, FABLE, FOVEATED, OverTone I-1, forward replay I-2) | inventory 3a–3c, 4, 5 | in-scope |
| E4 hypernetwork editors emitting real weight deltas (MEND, PropMEND, DAFNet) | ARC:9; PAS addendum 5 | in-scope if the delta is written; `fallback` if it needs an inference-time module |
| E5 LoRA / merged-adapter writes (adapter merged or mounted as a parametric overlay, no router) | not in the corpus | in-scope if merged; `fallback` if routed (MELO, GRACE-style gating) |
| E6 continued pretraining / fine-tuning on the coined facts (incl. "Fresh in memory", "Synthetic Worlds", KILM) | ARC:7–9, 83 | in-scope as a spec-amendment challenger (not the write engine; F1 would need to say so) |
| E7 parametric memory-layer / value-slot architectures without external lookup (Kformer slots, MemoryLLM pool, Larimar) | PAS addenda 3, 9 | in-scope only if read without lookup; else `fallback` |
| E8 vocabulary-extension / tokenizer families beyond the mint arm (grounded token init 2604.02324, token distillation, multi-token vocabulary additions, GS-Quant codes, byte/tokenizer-free models) | CORPUS/45; ARC:178–186 | in-scope |
| E9 side stores (WISE, GRACE, MELO, P-Tokens, OnceEdit, HoReN, RILKE, NeuralDB) | inventory 2a–2c | `fallback` by ruling (RB:305) — logged, never a route |
| M1 untied-embedding models ≤ prefilter | inventory 8 | model family |
| M2 multi-token-prediction pretrained checkpoints | inventory 9 | model family |
| M3 diffusion LMs (LLaDA, Dream; MDM-KE) | inventory 10 | model family |
| M4 open-data models (OLMo-2, Pythia) | inventory 11 | model family |
| M5 hybrid / SSM / MoE | inventory gap 7 | model family (expected `empty`) |

## 2. Instruments, in order, each bounded

| # | Instrument | Status on this Mac | Budget | Output |
|---|---|---|---|---|
| A | arXiv MCP (`mcp__arxiv__search_papers`, `semantic_search`, `citation_graph`) | available | ≤ 12 queries | hits → `results/research_pass_2026-10-06/arxiv_log.json` |
| B | GitHub (`gh search repos`, `gh api` for READMEs, license, last push) | `gh` authenticated | ≤ 25 repo checks | `repo_log.json` |
| C | OpenReview, Papers-with-Code, Hugging Face (`huggingface_hub` model search by config: `tie_word_embeddings`, MTP heads, diffusion LMs, size ≤ 14 B) | WebFetch / `uv run --with huggingface_hub` | ≤ 10 queries | `hf_candidates.json` |
| D | Connected Papers graphs: the 25 + INBOX bibs (`tools/connected_papers_index.py` already indexes 88 graphs / 2,123 papers; 149 unseen) | local | re-run the index; read the unseen cluster for the gap keywords | index diff |
| E | OpenResearch `orx discover` (alphaXiv full-text + OpenAlex) — `docs/PRIOR_ART_OPENRESEARCH_2026-10-06.md` §proposed use. **Fences (advisor item 4):** `orx telemetry off` before the smoke query; record the exact CLI version; no `orx install-skills`, no `orx up`, no project / experiment tree, no login / managed compute; endpoint routing of `discover` stays UNVERIFIED and its hits are leads only | not installed; unsigned CLI or desktop app | ≤ 10 queries, ≤ 5 `orx paper --full` | `alphaxiv_log.json` |
| F | InfraNodus (MCP, key-gated; present in this session's tool list) | available | 1 `difference_between_texts` (our gap list vs. the pass's hit abstracts) + 1 `generate_research_questions` | leads → register §J |

Order A → B → C → D → E → F. Every hit is deduplicated against the inventory's "already verified" list and `_arxiv_pass_log.json` before it is read; a repeated id is logged as `seen` and not re-verified.

**Exit condition (frozen; advisor item 5):** the pass exits only when (i) every class in §1a has a disposition, (ii) every new artifact is deduped and triaged, (iii) the BetaEdit-id and AnyEdit++-repo contradictions are resolved, and (iv) two consecutive *independent search instruments capable of adding a new class* (A, B, C, D, E — not F) add no new candidate class after dedupe. InfraNodus synthesis over already-found hits never counts toward (iv).

## 3. Queries (the field's vocabulary — the 2026-10-05 arc's advisor item 7 and 11; plus the inventory's uncovered axes)

**Editing methods (gap list items 2, 3, 4, 6, 8, 9; classes E1–E9):**
0. per class E4–E8 one query in the class's own vocabulary: "hypernetwork knowledge editing weight delta", "LoRA merge knowledge injection paraphrase", "continual pretraining new entity recall paraphrase", "parametric memory layer no retrieval", "token embedding initialization new entity editing"
1. covariance regularization editing generalization
2. layer selection residual locate-then-edit
3. null-space editing generalization tradeoff
4. out-of-vocabulary entity editing / novel entity weight injection paraphrase
5. multi-token target knowledge editing paraphrase generalization
6. sequential model editing coined entity held-out
7. BetaEdit null-space sequential (resolves the arXiv-id contradiction: 2605.09285)
8. "Keys to Robust Edits" (2024) — read in full (flagged blocking before any keying decision)
9. "The Tokens Remember" 2609.29045 — read in full (tokenization premise check, flagged BLOCKING at ARC:65)
10. WISE / MELO / MDM-KE on MPS (repo issues + code grep for `.cuda(`, flash-attn, triton) — runnability only

**Model families (gap list items 1, 5, 7):**
11. untied embeddings (HF config `tie_word_embeddings: false`): candidates to check — Llama-3.1-8B, Mistral-7B, OLMo-2-7B, Gemma-2-9B? (Gemma ties), Qwen2.5-7B (ties? verify), Phi-3-medium; each with: editability evidence in the literature, covariance-corpus availability, and the **hard prefilter** below

**Hard memory prefilter (advisor item 3; replaces "~28 GB"):** fp16 weights ≤ 28 GB decimal (≈ 26 GiB); hidden size d ≤ 5120 unless verified otherwise; edited band ≤ 5 layers or streamed; and a one-layer `_cov_cpu` / null-space solve smoke must pass on the M3 Pro before any model is promoted from `lead` to `candidate`. Arithmetic (exact configs verified at pass time): 7–8 B → weights 14–16 GB; d = 4096 → one fp32 d×d covariance 64 MiB, five layers 320 MiB, live solve/SVD workspace 4–8 matrices ≈ 256–512 MiB per active layer → working set ≈ 20–24 GB + MPS overhead. 13–14 B → weights 26–28 GB; d = 5120 → 100 MiB per matrix, five covariances 500 MiB, workspace 400–800 MiB per active layer (more if not streamed) → working set ≈ 32–38 GB + MPS overhead, inside 48 GB only if streamed layer-by-layer and confirmed by the smoke solve.
12. multi-token-prediction pretrained open checkpoints (DeepSeek-V3 is MoE/too big; Meta's MTP Llama-2 research models — released? ; 2603.17942 / 2505.10518 titles in the register) — any ≤ 14 B?
13. diffusion LMs: LLaDA-8B, Dream-7B — MPS serving feasibility + MDM-KE eval section (RB:836)
14. open-data: OLMo-2-7B / OLMo-2-13B, Pythia-6.9B/12B — AlphaEdit/MEMIT results in the literature; the Moir covariance paper used OLMo-2-7B
15. hybrid / SSM / MoE editability (one query; expected empty)

## 4. What counts as a hit (pre-registered, so the pass cannot be flattered)

**Frozen wording (advisor item 2):** a **candidate** is a public artifact (paper + code, or a HF checkpoint, verified by id) that writes or mounts knowledge into model parameters, has a verified path to local execution or measurement under D-HW-1 (no CUDA-only kernels in its code path; passes the §3 prefilter), and can be evaluated on C10: exact full-sequence held-out paraphrase recall for a coined multi-token target, plus locality. If the paper does not report C10 but the artifact supports measuring it → `candidate-needs-C10-eval`. If it cannot support that measurement → `lead`; if it is a read-time side store → `fallback`; a class with no public artifact → `empty`. The cell-empty claim is restated narrowly per the 2026-10-05 advisor's item 11: "not found in N papers read at the evaluation section plus the logged query hits."

## 5. Deliverables to the operator (HIL packet, morning)

1. `results/research_pass_2026-10-06/` logs (one JSON per instrument) + `docs/RESEARCH_PASS_REPORT_2026-10-06.md`: the candidate table (≤ 10 rows: name · class · artifact ids · local-runnability · what it would be measured on · cost estimate in runs) and the lead list.
2. A **ranked shortlist of ≤ 3** with the cheapest pre-registerable falsifier for each, stated as a prereg stub (hypothesis, binding count, controls, gates).
3. The two contradictions from the inventory resolved (BetaEdit id; AnyEdit++ repo).
4. No route commitment. No CORPUS entry. Register entries (§J) for every lead with builds-on / would-advance / source.

## 6. Reviews

v1 → Codex gpt-5.5 advisor pass (`results/research_pass_advisor_v1.md`, FIX-FIRST: taxonomy, hit wording, hard prefilter, OpenResearch fences, exit condition, LEAD wording — all folded) → **v2 (this)** → execute after the operator's HIL on CORPUS/50 → report → HIL on the shortlist.

## 7. Not claimed

That the pass will find a route; that any model family is pre-selected; that InfraNodus or OpenResearch outputs are evidence (leads only); that the 48 GB bound admits 14 B for editing (the solve's covariance and projector add headroom — to be computed per candidate).
