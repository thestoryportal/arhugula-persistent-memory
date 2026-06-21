# SESSION BOOTSTRAP — read this FIRST in any fresh context
_Updated 2026-06-18. This is the single entry point for re-grounding a new session on the "LLM-as-Database" program. It orients; the detail lives in the files it points to. If you are a fresh agent context: read this top-to-bottom, then `CORPUS/README.md`, then skim the spec. Do not start work until grounded._

<!-- BEGIN GENERATED:program-state -->
**📍 PROGRAM STATE (updated 2026-06-21 (session-close))** — _auto-generated from `docs/program_state.json` — DO NOT edit between the markers; run `python3 tools/render_state.py --write`._

- **North star:** F1 — prove/falsify the 'LLM-as-Database' spec is implementable BEFORE it is built; deliver a ready / not-ready-with-conditions determination. Falsification-first.
- **Latest:** D-D1-2: §8.7 numeric drift guardrail SET on Qwen2.5-3B = max unanchored per-relation concentration **k≤1** (conservative; corruption is edit-order/held-out-DOMINATED, not count-determined; mixed-load shows other-relation volume corrupts too → pair with a global-volume bound). §8.7 structural amendment = operator-APPROVED + model-general (3B+7B). INFRA (this session): a 3-layer anti-drift doc system was built — edit THIS file + run `python3 tools/render_state.py --write` to update status; a pre-commit hook blocks stale commits (`tools/ANTI_DRIFT.md`). Next-arc is F1 SCIENCE (below), NOT more doc infra.
- **F1 status:** NOT delivered. Deployment data-path spine PROVEN-FOR-SCOPE (recipe→A1 batch-clean→B3 Q4_K_M→E1·A CPU-serve; 3B / N≤100 / batch). Blocks on: CP2 (contract) + D1 numeric cross-model transfer + the B3 in-weight-vs-side-store architecture decision. Everything ~3B/N≤100/batch-scoped.
- **Next actions (priority):**
  1. B3 — is diffuse in-weight storage even required vs a routed/gated side-store? (highest-stakes; analysis-heavy/low-compute; the 6-graph ConnectedPapers review shows the field converges on side-stores)
  2. 7B numeric-threshold transfer via the proven determinism path (OQ-W1 cross-model)
  3. CP2 query-schema build-items (L1 triple-readback + 5 query families + violates-rejection — contract-readiness)
  4. → F1 reconciliation & determination
<!-- END GENERATED:program-state -->

> **⚠️ CURRENT STATUS (2026-06-21) — §3 "immediate next work" below is STALE (it predates the empirical arc).** Since then: **G6.1** (cross-entity read corruption falsifier), **A1** (batch eliminates it), **B1/B3** (size + Q4_K_M survival), **C2/C2-band**, **D1** (capacity law → drift is per-relation-concentration, not global edge-count), **B1 size-term** (law model-general on 7B), and **D-D1-2 ⟨D-D1-2@e023d8d2⟩** (§8.7 numeric guardrail `k≤2`, dual-reviewed; mixed-load shows it needs a global-volume bound too) are all DONE. The §8.7 structural amendment is **operator-approved** (`docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md`). **NEXT = 7B size-term via determinism (OQ-W1 transfer) → B3 (in-weight-necessity vs routed side-store, the field-convergence signal from the 2026-06-21 ConnectedPapers review, register §J) → CP2 schema build-items → F1 readiness.** Canonical "what's next" = `EXPERIMENT_RUNBOOK.md` §0.3 + `SESSION_CHECKPOINT.md` top block (NOT §3 below).

═══════════════════════════════════════════════════
## 0. WHAT THIS PROGRAM IS (one screen)
We are pre-development-validating a **specification**: "LLM as Database — Agent Harness Architecture" (`research_and_specs/llm-as-database-v1_2-integrated-spec.md`). The thesis: treat a transformer's FFN as a **physically queryable + editable graph database** — knowledge lives **in-weight** (semantic "map"), edited via **MEMIT**, stored as **`.vindex`** overlays on a **frozen base**, queried via **LQL** (LARQL), with Git holding the **code** (syntactic "territory"). The spec was authored/debated by a **7-skill Framework Council** (`/workspace/skills/`). The goal of ALL the experimentation (this session + many prior months) is to **prove the spec is implementable before building it** — falsification-first, evidence over opinion.

**Operator context:** the user is the spec owner, **learning ML/LLM as they go** — make every decision *legible*, never push an expertise-gated call onto them, and defer hard calls to *evidence*, not authority. Deployment target is **TBD** — may be a remote GPU, not necessarily a local Intel CPU (so the pod is a valid proxy).

═══════════════════════════════════════════════════
## 1. RE-GROUND IN THIS ORDER
0. **`EXPERIMENT_RUNBOOK.md`** (NEW 2026-06-18) — the LIVING operating roadmap from the current blocker to spec implementation-readiness: role/system-prompt, tools, disciplines, hygiene, knowledge-base index, decisions ledger, dependency/sourcing catalog, the Track A–F experiment decision tree (with pre-written code), readiness checklist, risk register, live status dashboard. **Its §0.3 is the single source of "what's next." Start here for any experimental work.**
1. **This file** (arc + norms + environment).
2. **`CORPUS/README.md`** → then `CORPUS/00_MASTER_EVIDENCE.md` (every experiment + exact numbers + status), `03_STATUS_LEDGER.md` (proven/corrected/open + the CP1-3 checkpoints), `06_SPEC_WRITE_PATH_AND_BRIDGE_FRAMING.md` (how our work maps to the spec — the most important framing).
3. **The spec** `research_and_specs/llm-as-database-v1_2-integrated-spec.md` (§7-§12 are the six layers; read them — do NOT work from grep excerpts, that caused a real misframing this session).
4. **Auto-memory** (`MEMORY.md` index, loaded each session) — durable lessons + traps.
5. `LARQL_INTEGRATION_ASSESSMENT.md` (the LARQL narrative + the bridge).

═══════════════════════════════════════════════════
## 2. THE ARC — what the experiments were meant to evidence, and what they surfaced
**Arc:** spec authored (council) → **write-engine viability determination** (Phase 0 metric calibration → Phase 1 model/size dependence; `write_engine_viability_determination_report.md`) → **pre-dev validation** (Tiers 1-2: durability, novel-insert, quantization, CRUD, compaction, scale, diversity; `spec_predev_validation_plan.md`) → **recipe development** (in-solve AlphaEdit + preserve-sampling + batched compile) → **Qwen3 re-validation** (deployment-servable model, A1-A5) → **LARQL integration + the decoupled bridge**. (Prior months live in the artifacts: `framework_finding_v1_10` = 10 iterations; `s229_*` etc. = many prior sessions; git/memory hold the rest.)

**What is PROVEN (mechanics)** — full detail in `CORPUS/00`:
- In-weight multi-field editing is viable, **model/size-dependent** (GPT-J fails; Qwen-7B clean; Qwen-3B & Qwen3-0.6B work with the recipe).
- **Recipe:** in-solve AlphaEdit (null-space/orthogonal projection, `nullspace_threshold=0.005`) + preserve-sampling (cross-entity) + batched-per-record compile (novel inserts). Edits survive 4-bit. Full CRUD + compaction hold. Transfers to Qwen3 with no recalibration.
- LARQL serves edited weights **in-weight on CPU**; the **bridge** (our clean ΔW → `.vlp` overlay → `APPLY` on frozen base → `COMPILE`) works end-to-end, no LARQL code (`build_vindex_overlay.py`).
- Our AlphaEdit null-space step **aligns with the spec's mandatory D20 orthogonal-projection safeguard.**

**What is NOT proven (the next work)** — `CORPUS/03` + `06`:
- **CP1** governed *in-pipeline* MEMIT write (we only did offline compile + the bridge bypasses the Gate — a C16 violation as a production path). **CP2** LARQL query-schema capability (`SELECT` read-back = spec's mandatory L1 probe, `DELETE FROM EDGES`, triple/relation-families/`violates`). **CP3** confirm AlphaEdit counts as "MEMIT" (D12). Then governance gaps **G1** 2PC/State-Ledger, **G2** authz/audit, **G3** validation pipeline; capability/scale **G6** (real GGUF-Q4_K, scale), **G7** multi-token.

**The key reframe (don't relitigate):** there is **no "bridge-vs-spec-architecture" decision** to agonize over. The spec IS the architecture (Commit-Executor→Gate→2PC→Ledger governed write path); our recipe is the **engine internals**; LARQL is the **`.vindex`/serve** layer; the bridge was **viability scaffolding**. Architecture-*ownership* is settled; the open items are empirical viability tests (CP1-3, G*) — **pod-runnable now**.

═══════════════════════════════════════════════════
## 3. IMMEDIATE NEXT WORK — UPDATED 2026-06-18 (CP1-3 + G1/G2/G3 DONE; G6/G7 next)
**DONE this session (all PROVEN-FOR-SCOPE; see `CORPUS/07`–`12` + the consolidated handoff at the top of `SESSION_CHECKPOINT.md`):** CP1 governed in-pipeline parametric write · CP2 LARQL query-schema (verbs run; L1-triple/5-families/violates are OUR layer) · CP3 D12 MEMIT-compliance confirmed (C15 band open) · G1 dual-medium 2PC+ledger+TC+circuit-breaker · G2 real-Ed25519 security (verify-cannot-forge) · G3 deterministic validation pipeline (delivers the CP2-surfaced contracts).

**NEXT — G6/G7 (the categorically different, empirical run):** real GGUF-Q4_K (not the crude sim quantizer), larger Qwen3, overlay size at scale + many-overlay behavior, multi-token value robustness, and the **CP3 C15 band recalibration** (our band [4-8] diverges from C15's L15-25/32-layer). ⚠️ Unlike CP1-G3 (self-authored contract prototypes that pass because we built them to — [[prototype-tautology-trap]]), **G6/G7 can ACTUALLY FAIL** → it is the binding falsification evidence. **Set falsifiable pass criteria BEFORE the runs; let numbers fall where they land.** Then D1/G5 (deployment hardware) contingent.
**Scope reminder:** all the above are *viability prototypes*, NOT the production harness (later dev project; orchestrator Path A/B/C TBD). Each = bounded experiment + durable result + honest CORPUS update.

═══════════════════════════════════════════════════
## 4. HOW TO WORK HERE (norms — these are load-bearing)
- **Engine + LARQL are UNMODIFIED.** Workarounds are config/our-own-code only. Honor the CLAUDE.md LAWs: fingerprint gate, determinism, known-baseline reproduction, **read source before authoring**, science-path-patch isolation (prove inertness). One-fix-then-halt discipline.
- **Evidence discipline:** set falsifiable pass criteria BEFORE the result; cite artifact path + exact number or flag `UNVERIFIABLE`; distinguish `EVIDENCE-SHOWS` vs `I-INFER`; **log every correction/reversal honestly** (see `CORPUS/03` — this session had several). Do NOT glaze over failures; do NOT overclaim ("high-certainty/proven" got recalibrated twice by the advisor — keep language precise: *mechanics proven; these contracts untested*).
- **Advisor:** call `advisor()` (no args; it sees the full transcript) BEFORE substantive work, when stuck, when changing approach, and before declaring done. Weight it heavily; it caught real over-corrections this session. It's enabled via `/advisor` (model: Opus 4.8).
- **Council caveat:** the 7-skill council is a **spec-authoring** tool. Same-model subagents reading our own corpus = **weak independence / confirmation-amplification** — do NOT use them to "confirm" self-authored conclusions. A *different* model cold-reading the corpus is better, but **review ≠ evidence**; the binding signal is empirical.
- **HIL gates:** stop and surface decisions that are the operator's to make; make them legible; offer a recommendation, not a survey; don't infer approval from navigation.
- **Durable-save discipline:** save deliverables to `/workspace`; update the CORPUS + `SESSION_CHECKPOINT.md`; re-mirror memory (`cp /root/.claude/projects/-root/memory/*.md /workspace/memory_mirror/`). `/dev/shm/` is RAM (ephemeral) — reproducible from scripts, never the source of truth.

═══════════════════════════════════════════════════
## 5. ENVIRONMENT & PERSISTENCE (traps that cost time this session)
- Pod: RunPod, RTX 4090 (24GB) + ~500GB RAM + `/dev/shm` 29GB tmpfs (RAM-speed). `/workspace` = persistent network volume (slow I/O — run heavy I/O on `/dev/shm`, not the network FS). `/` overlay = ephemeral on pod restart.
- **transformers pin = 4.51.0** (Qwen3 support + memit engine work; 4.45 lacks Qwen3, 5.x breaks the engine nethook). tf 4.51 uses `torch_dtype=`. torch 2.4.1+cu124.
- **LARQL build deps** (apt): rust(rustup), libssl-dev, pkg-config, cmake, protobuf-compiler, libopenblas-dev. Cap BLAS threads (`OPENBLAS_NUM_THREADS=8` etc.) or `convert` thrashes. LARQL is Metal-first; CPU path works (positive control).
- **Reusable assets:** `build_vindex_overlay.py` (the bridge packager, model-agnostic); `qwen3_06b_memit_hparams.json` / `qwen25_3b_memit_hparams.json`; `covariance_caches/` (Qwen3 band cached — ~70 min to recompute fresh); editing scripts `s24*.py` (engine at `memit_dry_run/memit`); LARQL at `external_prior_art/larql` (`cargo build --release`; binary `target/release/larql`).
- **On a fresh POD (not just context):** restore memory: `mkdir -p /root/.claude/projects/-root/memory && cp /workspace/memory_mirror/*.md /root/.claude/projects/-root/memory/`. Rebuild `/dev/shm` artifacts from scripts. Re-`cargo build` LARQL if `/` was wiped.

═══════════════════════════════════════════════════
## 6. TASK LEDGER (carry forward — recreate as TaskCreate items in the fresh session)
DONE: A1-A5 (Qwen3 re-validation), B1-B4 (overlay characterization), D2 (LARQL native write immature); **CP1, CP2, CP3, G1, G2, G3 (all 2026-06-18, PROVEN-FOR-SCOPE — `CORPUS/07`–`12`)**. OPEN: **G6/G7** (scale/efficiency + multi-token + C15 band — the empirical falsification run, gated next); D1/G5 (deployment-hardware) contingent. (Detail in `CORPUS/03` + `00 §Known Gaps`; per-prototype caveats in `CORPUS/07`–`12`.)

> **Always-in-context discipline:** load `DISCIPLINE.md` — north-star goal (F1), context read-triggers, deep-thinking-on-failure protocol, and tool/loop thresholds (binds Claude + Codex).
