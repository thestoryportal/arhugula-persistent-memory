# LLM-as-Database — Parametric Knowledge Editing as a Storage Substrate

<!-- BEGIN GENERATED:program-state -->
**📍 PROGRAM STATE (updated 2026-06-21)** — _auto-generated from `docs/program_state.json` — DO NOT edit between the markers; run `python3 tools/render_state.py --write`._

- **North star:** F1 — prove/falsify the 'LLM-as-Database' spec is implementable BEFORE it is built; deliver a ready / not-ready-with-conditions determination. Falsification-first.
- **Latest:** D-D1-2: §8.7 numeric drift guardrail SET on Qwen2.5-3B = max unanchored per-relation concentration **k≤1** (conservative; corruption is edit-order/held-out-DOMINATED, not count-determined; mixed-load shows other-relation volume corrupts too → pair with a global-volume bound). §8.7 structural amendment = operator-APPROVED + model-general (3B+7B).
- **F1 status:** NOT delivered. Deployment data-path spine PROVEN-FOR-SCOPE (recipe→A1 batch-clean→B3 Q4_K_M→E1·A CPU-serve; 3B / N≤100 / batch). Blocks on: CP2 (contract) + D1 numeric cross-model transfer + the B3 in-weight-vs-side-store architecture decision. Everything ~3B/N≤100/batch-scoped.
- **Next actions (priority):**
  1. B3 — is diffuse in-weight storage even required vs a routed/gated side-store? (highest-stakes; analysis-heavy/low-compute; the 6-graph ConnectedPapers review shows the field converges on side-stores)
  2. 7B numeric-threshold transfer via the proven determinism path (OQ-W1 cross-model)
  3. CP2 query-schema build-items (L1 triple-readback + 5 query families + violates-rejection — contract-readiness)
  4. → F1 reconciliation & determination
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
