# LLM-as-Database — Parametric Knowledge Editing as a Storage Substrate

<!-- BEGIN GENERATED:program-state -->
**📍 PROGRAM STATE (updated 2026-06-25 (F1 DETERMINATION FINALIZED — R11 read-contract COHERENT + C6 ledger-immutability red-teamed folded in; verdict NOT-READY-WITH-CONDITIONS, CONCLUDED))** — _auto-generated from `docs/program_state.json` — DO NOT edit between the markers; run `python3 tools/render_state.py --write`._

- **North star:** F1 — prove/falsify the 'LLM-as-Database' spec is implementable BEFORE it is built; deliver a ready / not-ready-with-conditions determination. Falsification-first.
- **Latest:** **F1 DETERMINATION FINALIZED (2026-06-25) — verdict NOT-READY-WITH-CONDITIONS, CONCLUDED as the deliverable** (`docs/F1_DETERMINATION.md`). Two more readiness-moving legs folded in since the C1-true-scale diagnostic, neither changing the net verdict: **(1) R11** content-scoped authoritative-medium & severity ON READ (D-R11-1, CORPUS/33) — **COHERENT via derivation + prevention** (wrong-medium-on-read foreclosed by §11.3/D43; class/severity DERIVABLE from the §7.2/C4-mandated entity_type); its residual is an *instance* of the known 'no formal query-language section' gap, NOT a new condition. **(2) C6** ledger-immutability red-team (D-C6L-1, CORPUS/34) — property-demo + spec finding vs the real G2 verify_chain: rewrite-recompute/truncation undetected, naive-edit caught (control), CT-style Signed-Tree-Head fix works; finding = (A) spec mandates NO operational-window crypto tamper-evidence (keyless chain §16.1; anchors only root §13.2 + close §16.7) + (B) §16.5↔§16.2 unreconciled threat-model seam → **C6 not-red-teamed → red-teamed (one mechanism)**. Both advisor-gated (caught a real over-claim in each → new memory: name-the-covering-clause before stamping a 'gap'). **The advisor's analysis is binding: no single solo action flips NOT-READY-WITH-CONDITIONS** → the operator fork is RESOLVED to CONCLUDED. F1 net readiness UNCHANGED.
- **F1 status:** DETERMINATION DRAFTED 2026-06-24 (`docs/F1_DETERMINATION.md`) = **NOT-READY-WITH-CONDITIONS** (draft-with-open-conditions, NOT a clean close; shippable as the honest current state). Deployment data-path spine PROVEN-FOR-SCOPE (recipe→A1 batch-clean→B3 Q4_K_M→E1·A CPU-serve; 3B/N≤100/band[4-8]/single-batch/1-seed/fictional). Architecture = scope-keyed COMPACTION-BOUNDED HYBRID (D-B3N-1), in-weight a serving copy per the verified §11.2/D42 structural finding (no class weights-authoritative). Determination carries a 10-row CONDITIONS REGISTER of first-class falsifiers: C1 compaction-at-scale (sharpest; D20 directionally negative) · C2 read-contract (biggest gap) · C3 R5-at-scale · C4 7B numeric transfer (OQ-W1) · C5 governance+orchestration (prototyped-not-empirical) · C6 security (un-red-teamed) · C7 Pruning/GC (untouched) · C8 R15-adversarial · C9 R9-native-deletion · C10 multi-token/G7. C1/C2 closing negative would move the verdict toward not-implementable-as-specified. Closure-path lead = UNGATED `tools/power.py` pool-sizing.
- **Next actions (priority):**
  1. F1 IS CONCLUDED (2026-06-25) as the NOT-READY-WITH-CONDITIONS deliverable; the conditions register is characterized AND bounded. The falsification frontier for the 3B/AlphaEdit/single-token-real-knowledge regime is reached. Remaining work is operator-reserved, on two axes:
  2. (A) HARDEN-MORE (additive, does NOT flip the verdict; diminishing F1 value): further bounded red-team / fault-injection legs — Gate/single-use-token forgery, 2PC/ledger fault-injection, key-custody/HSM, pruning/GC (C5/C6/C7).
  3. (B) REGIME / BUILD (the only paths that could CHANGE the verdict; operator scope call): a different REGIME (larger model / better edit method / a deployment avoiding counterfactual-over-prior at scale — ties to deployment-target-TBD) to push C1/C3 past the substrate ceiling; OR BUILD the index/query (C2) + governance (C5) layers, now engineering not falsification.
  4. RECOMMENDATION: treat F1 as delivered and gate further work on (B). If neither axis is taken, F1 stands as NOT-READY-WITH-CONDITIONS with a bounded conditions register.
  5. STANDING: re-auth codex/gpt-5.5 (refresh_token_reused; Perplexity-Sonar = working cross-family fallback). Guardrails: spec-first · pre-register + advisor before build AND before verdict · name-the-covering-clause before stamping a 'gap' · cross-family on interpretation-subtle results.
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
