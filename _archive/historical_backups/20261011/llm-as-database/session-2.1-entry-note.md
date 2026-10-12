# Session 2.1 Entry Note — GPU Procurement Research

> **Workstream:** 1 — Empirical POC Scoping (post-v1.2 sealed spec)
> **Session:** 2.1 — GPU Procurement Research
> **Position in arc:** Opens after Session 2.0 (target model commitment, three-tier strategy adopted: GPT-J 6B → LLaMA 3.1 8B with Mistral 7B v0.3 secondary). Precedes Stage 0 corpus authorship and Stage 1 (MEMIT-COMPAT-PROTO-1) execution.
> **Primary skill:** `memit-specialist`
> **Secondary skill:** `aiSecOps-specialist` (Warden — for tenant isolation and audit posture criteria)
> **Closes:** OQ-WS1-4 (multi-GPU parallelization decision; inherited from Session 1.7) and unblocks Stage 0 execution prep.

---

## Curation Notice — Read Before Beginning

The KB has been re-curated for this session. The four downstream calibration protocol documents that were removed for Session 2.0 are now **re-added**, because GPU sourcing depends on every stage's GPU-hour estimate, wall-clock envelope, and per-stage memory profile.

This is intentional. The KB is curated per session phase, not held static. Previous-session removals are not permanent.

The newly-added documents for this session:

- `memit-drift-proto-1.md` — Stage 2 sweep design; ~400-1,200 GPU-hours; longest single-stage runtime.
- `epsilon-calib-proto-1.md` — Stage 3a; ~200-400 GPU-hours; 15-cell × pre/post replicate matrix.
- `compaction-probe-calib-proto-1.md` — Stage 3b; ~300-600 GPU-hours; 7,500-edge corpus × N=10 + M=10 multi-event sweep.
- `judge-calib-proto-1.md` — Stage 3c; ~50-100 GPU-hours; includes p95 ≤ 800ms judge inference latency budget.

The newly-added recommendation artifact from Session 2.0:

- `MEMIT_Target_Model_Recommendation__Survey_of_Eleven_Open-Weights_Candidates.md` — committed three-tier strategy. GPU requirements: GPT-J 6B (≈12GB FP16) and LLaMA 3.1 8B (≈16GB FP16) need to coexist or load sequentially with persistent storage between sessions.

## Active KB Documents (10)

| Document | Role in this session |
|---|---|
| `memit-compat-proto-1.md` | Stage 1 GPU profile — PF-3 perplexity, PF-5 covariance precomputation, SECT, OP, CFB. |
| `memit-drift-proto-1.md` | Stage 2 GPU profile — 36+ measurement points × ≥3 replicates × 4 sweeps. |
| `epsilon-calib-proto-1.md` | Stage 3a GPU profile — 15 cells × 200 patches × 3-5 replicates × pre/post. |
| `compaction-probe-calib-proto-1.md` | Stage 3b GPU profile — longest single-stage runtime; oracle construction is GPU-heavy. |
| `judge-calib-proto-1.md` | Stage 3c GPU profile + judge inference latency budget (p95 ≤ 800ms on deployment GPU class). |
| `write-engine-poc-scope.md` | Aggregate POC scope. |
| `poc-execution-plan-and-spec-revision-rule.md` | Workstream 1 closing synthesis — full GPU-hour envelope (~1,000-2,400) and wall-clock estimates (7-11 weeks multi-GPU, 12-22 weeks single-GPU). |
| `llm-as-database-v1_2-integrated-spec.md` | Appendix A deployment preconditions — single OS user owning harness process; filesystem readable only by harness user; A11 break-glass custodian rule. |
| `MEMIT_Target_Model_Recommendation__Survey_of_Eleven_Open-Weights_Candidates.md` | Committed three-tier strategy; per-model VRAM requirements. |
| `llm-as-database-agent-harness-framework.md` | Paradigm context; useful if the session needs to explain why MEMIT specifically requires CUDA-class compute (matrix-multiplication-heavy covariance precomputation, FFN parameter access). |

## Documents NOT in the KB for this session

- `tension-map-v5.md` and `gap-backlog-v5.md` — neither has direct relevance to GPU procurement. The closing artifact and protocol documents already carry forward the relevant tensions and gaps. Removed to focus the context.

## Tools Expected in This Session

- **Web search** — required and primary. Pricing changes weekly; current cloud-GPU rates, free-tier eligibility, Apple Silicon model availability, and provider feature sets must be looked up. Do not rely on training data for pricing or availability.
- **Web fetch** — required for provider Terms of Service (audit posture under HC-4), Apple spec sheets, and any toolchain-compatibility documentation (MPS backend status pages, MLX framework readme, etc.).
- **Deep Research** — recommended if the operator wants a thorough survey across many providers and modalities; not required if the candidate field can be bounded quickly.

Tools that do NOT apply: image search, maps, weather, calendar, email, drive, recipes, places, conversation_search.

## Procurement Modalities In Scope

The session evaluates three modalities side-by-side:

1. **Free-tier cloud GPU** (Google Colab, Kaggle, Lightning AI, etc.).
2. **Paid cloud GPU rental** (RunPod, Lambda Labs, Vast.ai, CoreWeave, Together.ai, Modal, Paperspace, AWS/GCP/Azure on-demand or reserved, etc.).
3. **Self-hosted Apple Silicon** (current Mac Studio and MacBook Pro configurations with M3 Ultra, M4 Pro, M4 Max, M4 Ultra). The operator's current machine (2020 Intel 16GB MacBook Pro) is categorically incapable of running any candidate; this modality evaluates whether an Apple Silicon upgrade is competitive against cloud GPU.

## Output Discipline

The session output is a **recommendation**, not a procurement commitment. The operator commits in a follow-up. The recommendation should land as a single document the operator can read, decide on, and either move to procurement or open a focused follow-on session.

Do not treat Apple Silicon as either a foregone-yes or a foregone-no. Evaluate it against the same criteria as cloud-GPU candidates, with the toolchain-compatibility question (HC-2 below) made explicit. The MEMIT literature precedent on Apple Silicon is currently zero — this is a real condition that must be surfaced honestly, parallel to how SC-6 was treated for target model commitment in Session 2.0.

Do not extend into Stage 0 corpus drafting in this session. Do not draft architecture_profile.json — that's the next session.

---

*Entry note ends. The fresh session prompt follows in `session-2.1-prompt.md`.*
