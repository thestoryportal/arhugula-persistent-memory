# LLM-as-Database — Parametric Knowledge Editing as a Storage Substrate

<!-- BEGIN GENERATED:program-state -->
**📍 PROGRAM STATE (updated 2026-06-25 (index/query layer R1 read-back arc — commit-time delivered; paused))** — _auto-generated from `docs/program_state.json` — DO NOT edit between the markers; run `python3 tools/render_state.py --write`._

- **North star:** F1 — prove/falsify the 'LLM-as-Database' spec is implementable BEFORE it is built; deliver a ready / not-ready-with-conditions determination. Falsification-first.
- **Latest:** **INDEX/QUERY LAYER — R1 SELECT READ-BACK arc (2026-06-25, paused at clean state).** Operator-chosen #1 frontier. **R1 (D-R1-1, CORPUS/31) = NOT-DELIVERED**: a ledger-backed SELECT reconciled via an in-weight logprob signature abstains correctly (LEAK 6/6 NULL while model fires; REJECTED 4/4; LANDED 8/8) but the novel divergence test failed 1/2 — a phantom read (Velloria→Tokyo) from +2.06-nat cross-entity bleed over the frozen threshold → **in-weight storage-signature is bleed-unsound** (confirms B0/§11.2: the ledger medium must carry commit-status). **R1-bit (D-R1-2, CORPUS/32) = DELIVERED-FOR-SCOPE (commit-time)**: the advisor-recommended fix — a G1 2PC **commit-status bit** (SELECT reads the ledger, not the weights → bleed-immune); all criteria met, Velloria flips proxy-TRIPLE→bit-NULL. **Scope = commit-time ONLY; post-commit divergence (compaction/quant drift) recorded — no redundant GPU run — as a C5 governance gap** (commit-bit false-certifies the ~5% of committed triples C1 shows compaction diverges → strong read-consistency R10/D43 needs compaction output re-verified at mount; matrix R10 + F1 register C5 annotated). **F1 net readiness UNCHANGED** (NOT-READY-WITH-CONDITIONS); a condition sharpened + re-allocated. PAUSED per operator (auto-recommend loop into diminishing returns).
- **F1 status:** DETERMINATION DRAFTED 2026-06-24 (`docs/F1_DETERMINATION.md`) = **NOT-READY-WITH-CONDITIONS** (draft-with-open-conditions, NOT a clean close; shippable as the honest current state). Deployment data-path spine PROVEN-FOR-SCOPE (recipe→A1 batch-clean→B3 Q4_K_M→E1·A CPU-serve; 3B/N≤100/band[4-8]/single-batch/1-seed/fictional). Architecture = scope-keyed COMPACTION-BOUNDED HYBRID (D-B3N-1), in-weight a serving copy per the verified §11.2/D42 structural finding (no class weights-authoritative). Determination carries a 10-row CONDITIONS REGISTER of first-class falsifiers: C1 compaction-at-scale (sharpest; D20 directionally negative) · C2 read-contract (biggest gap) · C3 R5-at-scale · C4 7B numeric transfer (OQ-W1) · C5 governance+orchestration (prototyped-not-empirical) · C6 security (un-red-teamed) · C7 Pruning/GC (untouched) · C8 R15-adversarial · C9 R9-native-deletion · C10 multi-token/G7. C1/C2 closing negative would move the verdict toward not-implementable-as-specified. Closure-path lead = UNGATED `tools/power.py` pool-sizing.
- **Next actions (priority):**
  1. PAUSED 2026-06-25 at a clean state (R1 read-back delivered for commit-time; trackers green; memory mirrored). Resume by choosing a frontier — these are operator-reserved scoping decisions, not auto-pickable:
  2. (1) TRUE-SCALE C1 — post-commit divergence at true scale (the genuinely-valuable R1-class follow-up). Needs the OPERATOR to set stimulus-pool design (real multi-domain single-token pool vs explicit fictional confound; country/Knowledge caps ~78 entities) AND a GPU-hours budget. The §0.3-reserved scope call.
  3. (2) C5 MOUNT-VERIFY GOVERNANCE — does compaction output re-pass the Gate/verify-vs-ledger before becoming the active served store? The obligation R1-bit/R10 surfaced; Phase-2 governance/fault-injection (CPU-ish), promotes a prototyped-not-empirical layer.
  4. (3) CPU-CHEAP QUERY CELL — R4 namespace / R7 aggregation-negation / R8 multi-hop / R16 provenance. Mostly index/governance-delegated; lower F1 value (R8 tautology-trap, R7 spec-under-specified) but additive.
  5. (4) GOVERNANCE/SECURITY/PRUNING C5/C6/C7 — prototyped not empirical, security un-red-teamed, Pruning/GC untouched (Phase-2 red-team).
  6. STANDING: re-auth codex/gpt-5.5 (refresh_token_reused; Perplexity-Sonar = working cross-family fallback). Guardrails: spec-first · pre-register + advisor before build AND before verdict · name-the-manipulated-variable · cross-family on interpretation-subtle results (waive on decisive).
<!-- END GENERATED:program-state -->

A falsification-first research program testing whether facts can be **stored in, retrieved from, governed within, and deployed from an LLM's weights** — treating a transformer as a queryable database rather than an opaque generator. Editing is done with the MEMIT/AlphaEdit family (closed-form `down_proj` null-space solves); the program stress-tests a written spec (`research_and_specs/llm-as-database-v1_2-integrated-spec.md`) toward implementation-readiness.

This repo is organized for a research audience: every headline claim resolves to a raw artifact, every experiment is pre-registered and re-runnable, and caveats are kept flush with results. It follows the **ML Reproducibility Checklist** (Pineau et al.), **"Good enough practices in scientific computing"** (Wilson et al.), **Model-Cards** disclosure norms (Mitchell et al.), and **FAIR** principles.

> **North star (never drift):** the goal is the **F1 spec-implementation-readiness determination** for the LLM-as-Database thesis — *is it buildable?* Everything serves F1. Operating discipline (goal, context-triggers, failure-thinking, tool thresholds) is in **[`DISCIPLINE.md`](./DISCIPLINE.md)**.
>
> **New here? Read in this order:** this README → `REPRODUCIBILITY.md` → `docs/EXPERIMENT_REGISTRY.md` → `CORPUS/README.md` (the evidence) → `research_and_specs/…spec.md` (the contract). For the live roadmap and "what's next," see `EXPERIMENT_RUNBOOK.md` §0.3.

---

## Headline findings (what is PROVEN / PARTIAL / FALSIFIED)

| Area | Result | Evidence |
|---|---|---|
| **Governance** (in-pipeline write, 2PC, security, validation) | ✅ PROVEN-FOR-SCOPE (design-viability — these test our own control flow, not nature; weaker-than-empirical) | `CORPUS/07–12` (CP1–CP3, G1–G3) |
| **Single/few-fact, same-entity store** | ✅ VALIDATED (Qwen2.5; model- & size-dependent — Qwen2.5-7B local, GPT-J not) | Phase-1, `docs/framework_findings/` |
| **Cross-entity store at scale (sequential)** | ❌ FALSIFIED — held-out same-relation reads corrupt 100→41.7% with N (the first empirical falsifier) | `CORPUS/13` (G6.1) |
| **Batch / Genesis write at scale** | ✅ ELIMINATES the corruption at 3B (flat 100→100→100%) | `CORPUS/14` (A1) |
| **In-solve sentinels / K_S refresh** | 🟡 PARTIAL / ruled-out (halve but don't arrest the sequential decline; staleness not the cause) | `CORPUS/15–16` (A2, A2b) |
| **Real Q4_K_M quantization survival** | ✅ PASS — edits survive deployment quantization (edited 100% vs native 97.4%) | `CORPUS/17` (B3) |
| **CPU deployment serving** | ✅ Claim A PASS via **llama.cpp** (~8–13 tok/s) · ❌ Claim B FALSIFIED via **LARQL** (drops Qwen2.5 attn bias; A7 causal proof) | `CORPUS/18` (E1) |
| **Size-density (3B→7B)** | 🟡 PARTIAL — batch-clean does not *fully* replicate at 7B (100→91.7%) | `CORPUS/19` (B1) |
| **Cross-entity mechanism (keying)** | ⛔ relation-keying PRUNED; same-relation key collinearity is U-shaped in depth (min L8–12) — a measured mechanism + a spec-C15 tension | `CORPUS/20` (C2) |

**Net state:** the **batch-rebuild deployment path** is clean at 3B and survives Q4_K_M; CPU serving works via llama.cpp. Open frontier: whether in-weight storage (L2) is even required vs. retrieval (L1) + an external query index; the capacity law (D1 — structural DONE+model-general; §8.7 numeric guardrail set conservative at per-relation **k≤1** on 3B, D-D1-2 ⟨D-D1-2@e023d8d2⟩, cross-model transfer open); and whether the edit-validated family (Qwen2.5) should move to the LARQL-servable family (Qwen3). See `docs/HYPOTHESIS_REGISTER_2026-06-18.md`.

---

## Repository map

```
README.md  REPRODUCIBILITY.md          ← start here
EXPERIMENT_RUNBOOK.md                   ← living roadmap (§0.3 = what's next, §0.4 = update protocol)
SESSION_CHECKPOINT.md  SESSION_BOOTSTRAP.md  EVIDENCE_INDEX.md  CLAUDE.md
CORPUS/                 ← THE evidence ledger (numbered findings 00–20 + provenance/status ledgers)
research_and_specs/     ← the governing spec + research synthesis
docs/                   ← EXPERIMENT_REGISTRY, HYPOTHESIS_REGISTER, framework_findings/, session_summaries/, runbooks/
experiments/            ← re-runnable code by track: governance/ scale/ track_a/ track_b/ track_c/ deployment/
configs/                ← hparams/ screens/ probes/
results/   logs/        ← structured result JSONs · run logs
archive/                ← frozen historical scripts (s-series), notebooks, stale subdirs
memory_mirror/          ← durable cross-session learnings
— infrastructure (large, unmoved) —
memit_dry_run/ (MEMIT engine)  external_prior_art/ (larql, BetaEdit)  hf_cache/  covariance_caches/
llama_cpp_src/  b3_edited_qwen3b/  b3_q4km.vindex/  *.gguf  stage_1_sect/  architecture_profile/
```

## Quickstart / reproduce

```bash
export LLMDB_ROOT=/workspace          # default; set if the repo lives elsewhere
# a no-GPU sanity check (re-derives the B3 quantization verdict from stored predictions):
python experiments/track_b/b3_verdict.py
# a GPU mechanism probe (~1 min: loads Qwen2.5-3B, prints the key-collinearity depth map):
python experiments/track_c/c2_key_collinearity.py
```
Every experiment's exact command, inputs, and expected artifact are in **`REPRODUCIBILITY.md`** and **`docs/EXPERIMENT_REGISTRY.md`**.

## Scope & honest caveats (read before citing)
- **Model/range:** primarily Qwen2.5-3B (some 7B, Qwen3-0.6B); N ≤ 100 edits; Q4_K_M only; mostly single-seed, single write-ordering. Counterfactual-reassignment edits (not insertion/deletion).
- **Governance (CP1–G3) is design-viability**, not empirical falsification — it verifies our code implements the spec's contracts, a weaker category (see `CORPUS/03` and `[[prototype-tautology-trap]]`).
- **A measurement confound runs through the edit metrics:** MEMIT's `compute_z` inflates edited-fact margins vs native (`CORPUS/17`) — read retention numbers with that in mind.
- Reproducibility was preserved across a 2026-06-18 repo reorganization via a `LLMDB_ROOT` path convention; pre-reorg snapshot at `/root/migration_backup/`.
