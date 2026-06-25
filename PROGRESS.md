# PROGRESS — the cumulative build toward F1 (the twin of the north star)

> **This file is the equal-and-opposite of the goal.** `DISCIPLINE.md` §0 says *where we are going*
> (F1). This says *how far we have built toward it and what each result enables next*, so every
> loop's work is **additive** — it stands on the proven base and moves one F1 gap closer, never an
> isolated finding and never a re-run of settled ground.
> **Single source of truth = `CORPUS/00`+`03` + runbook §0.3/§12.** This is the distilled, injectable
> head; on any conflict the CORPUS ledger wins. Kept current via the §0.4 additive-update rule (bottom).

## The goal it converges on
**F1 — prove/falsify the "LLM-as-Database" spec is implementable *before* it's built, and deliver the
ready/not-ready-with-conditions determination.** Falsification-first. Everything below is scored by:
*does it move F1 closer?*

## How to read this (the additive contract)
- Each item is a **node F1 requires.** Edges = **"builds on."**
- **Work is valuable only if ADDITIVE:** it builds on a `PROVEN` node and advances a `PARTIAL`/`OPEN`
  F1 criterion. Orthogonal, redundant, or regressive work is drift — the auditor rejects it even if
  internally correct.
- **Do NOT re-run a `PROVEN-FOR-SCOPE` node.** If tempted, cite the Decision-ID that closed it and
  state what *new* F1 gap your run opens. If you can't, it's redundant — skip it.
- Status ∈ `PROVEN-FOR-SCOPE · PARTIAL · OPEN · FALSIFIED/PRUNED`. "FOR-SCOPE" = proven within a named
  scope (model/N/regime); pushing the scope is itself additive work.
- **⭐ COMPLETENESS (whole-system scope — binding):** the node-set here must cover **ALL cells of the e2e map** (`docs/SPEC_E2E_GROUND_TRUTH.md` §B layers + §E memory lifecycle + §G read contract), **not only the cells we've worked.** A cell we have *not entered* is an **OPEN node here, not an absent one** (see ⓪). This is the structural guard against the write-engine tunnel-vision: PROGRESS must show *where we are against the whole system*, so the read contract / Pruning-GC / lifecycle-loop stay visible instead of silently off-board.

---

## ⓪ E2E LAYER COVERAGE (situate every node here — `docs/SPEC_E2E_GROUND_TRUTH.md` is authoritative; this is the coverage view)
| e2e cell (ground-truth ref) | our coverage | node |
|---|---|---|
| **Write Engine** — edit mechanics, recipe, batch-clean store (§8) | **PROVEN-FOR-SCOPE** (3B/N≤100) | ① recipe/A1/B3 |
| **Memory lifecycle — drift trigger** (§8.7/§E) | **AMENDED** (concentration-aware `k≤1`, not count-only) | D1/D-D1-2 |
| **Memory lifecycle — compaction self-heal at scale** (§11.14/§E) | **DIRECTIONALLY PRESSURED, not falsified** (D-D20-1, gpt-5.5-tightened: accumulating sub-batching reintroduces corruption even when the joint solve is clean, order-insensitive at C=10; K-vs-C confound + spec-2000-SIZE regime untested) | ③ D20 |
| **Memory lifecycle — Pruning/GC · out-of-band reconciliation · archive · accumulate→compact LOOP** (§11.12–13/§E) | **❌ UNTOUCHED** (≈half of production memory mgmt) | ③ NEW |
| **Read / query contract** — reverse, aggregation, negation, traversal, 5 query families (§G) | **❌ OPEN/UNTESTED** — CP2 not started; **biggest gap** | ③ CP2 |
| **Validation layer** (§9) | **PROTOTYPED only** (not empirically stressed) | ① G3 |
| **Security layer** (§10) | **PROTOTYPED only** | ① G2 |
| **State Consistency / 2PC / TC / circuit breaker** (§11) | **PROTOTYPED only** | ① G1 |
| **Deployment** — compile → CPU-serve (§I) | **PROVEN-FOR-SCOPE** | ① E1·A |
| **Orchestration layer** (§12) | **❌ not engaged** | — |
_Reading: the write/deploy spine is proven-for-scope; governance is prototyped-not-proven; the **read contract, Pruning/GC, and the lifecycle-as-a-loop are UNTOUCHED** — those empty cells are the honest F1 frontier, not the next write-engine scaling run._

---

## ① FOUNDATION — PROVEN-FOR-SCOPE (locked; build ON these, do not re-run)
| Node | What it locks | Scope | Evidence |
|---|---|---|---|
| **Edit mechanics** | in-weight multi-field editing viable | model/size-dependent (GPT-J ✗; Qwen2.5-7B/3B, Qwen3-0.6B ✓) | CORPUS/00 P1, C1 |
| **Recipe** | in-solve AlphaEdit (null-space P, thresh **0.005**) + preserve-sampling + batched-per-record compile | Qwen2.5-3B, N≤100 | CORPUS/00 R-*, D-S243-* |
| **CP1** governed in-pipeline write | parametric MEMIT write under governance | for-scope | CORPUS/07, D-CP1 |
| **CP3** MEMIT compliance | D12 method-class = D20 null-space mandated | C15 layer-band = open divergence | CORPUS/09 |
| **G1** consistency | dual-medium 2PC + State Ledger + Txn Controller + circuit breaker (10/10) | for-scope | CORPUS/10 |
| **G2** security | real Ed25519 verify-cannot-forge + overlay integrity + CAK ceremony (9/9) | for-scope | CORPUS/11 |
| **G3** validation pipeline | deterministic schema validator: violates/undeclared reject + storage-probe split (8/8) | for-scope | CORPUS/12 |
| **A1** batch eliminates corruption | batch/Genesis joint solve → cross-entity corruption GONE (100→100% @N≤100) | resolves G6.1 write-path; 3B N≤100 | CORPUS/14, D-A1 |
| **B3 / G6.2** quantization survival | the A1-clean store survives **real Q4_K_M** (edits 100% vs native 97.4%) | margin-confound characterized | CORPUS/17 |
| **E1 (Claim A)** CPU deployment loop | serves edited store on CPU via **llama.cpp + Q4_K_M** (~8–13 tok/s) | pod-CPU proxy | CORPUS/18, D-E1-1 ⟨D-E1-1@55708623⟩ |

## ② THE ADDITIVE CHAINS (how the proofs stack toward F1)
**CHAIN A — DEPLOYMENT DATA PATH (the spine):**
`recipe` ✅ → `G6.1` exposes cross-entity scale falsifier → **`A1`** eliminates it ✅ → **`B3`** survives
Q4_K_M ✅ → **`E1·A`** serves on CPU ✅ → **`D1` capacity law `[OPEN — REQUIRED for F1]`** → F1 deployment-readiness.

**CHAIN B — GOVERNANCE / CONTRACT SUBSTRATE:**
`CP1` ✅ + `CP3` ✅ + `G1` ✅ + `G2` ✅ + `G3` ✅ → **`CP2` query-schema build-items `[PARTIAL]`** → F1 contract-readiness.

**CHAIN C — WRITE ROBUSTNESS / SCALE MECHANISM:**
`recipe`+`G6.1`+`C2` mechanism (key-collinearity U-shaped, min **L8-12**) → **`C2-band` `[OPEN, lead]`** &
**`C/G7` multi-token value robustness `[OPEN]`** → feed `D1` & F1 write-robustness.

## ③ THE ADDITIVE FRONTIER (open nodes whose prerequisites are PROVEN — the ONLY work worth doing)
| Open F1 gap | builds on (proven) | the additive step | moves F1 | priority |
|---|---|---|---|---|
| **D1 capacity law** | A1, B3, E1·A | measure N-before-break (corruption + quantization) → the number a ready/not-ready call needs | deployment-readiness **(REQUIRED)** | ★ critical path |
| **D1 — structural** ✅ DONE | G6.1, A1 | drift = per-relation concentration not global edge-count; **REPLICATES on Qwen2.5-7B (model-general, B1/D-B1-2 ⟨D-B1-2@0db8d819⟩)** → §8.7 amendment written | OQ-W1 reconciliation | DONE (D-D1-1 ⟨D-D1-1@0db8d819⟩+D-B1-2) |
| **D1 — numeric threshold** ⚠️ OPEN | D1-structural | set the per-relation WARNING/HARD value | the readiness number | **DONE (D-D1-2 ⟨D-D1-2@e023d8d2⟩): k≤1 conservative (order-cluster-bootstrap + ≥2 held-out seeds + determinism); mixed-load→pair with global-volume bound; cross-model transfer OPEN** |
| **CP2 schema build-items / READ CONTRACT** (§G) | CP2, G3 | L1 triple-readback + 5 query families + violates-rejection + reverse/aggregation/negation/traversal | contract-readiness — **biggest unspecified+untested cell** | ★ required (read-contract frontier) |
| **D20 compaction sub-batch (chunking)** ✅ DONE | A1, G6.1, D1 | does compaction stay clean once it sub-batches? | B3N condition-3 (chunking) | **DIRECTIONAL MECHANISM, not a falsification (D-D20-1, CORPUS/23, gpt-5.5-tightened): accumulating sub-batching can reintroduce corruption even when the joint solve is clean (order-insensitive at C=10, −19 to −34pp); C=25 order-soft. Pressures condition 3 (not naively clean), does NOT falsify it. NOT a promoted node.** |
| **C1 true-scale substrate** ⚠ CEILING'd | C1 / B3N cond-3 | viable real-knowledge substrate for N≥2000 high-concentration? | write-engine / compaction-at-scale | **DIAGNOSTIC (D-C1TS-1): city→country NON-VIABLE (multi-tok-subj solve-collapse + strong-prior under-expression 27-42%); C1 substrate-ceiling'd at N≤100; pilot-first saved a 4-10d grid; reinforces B3N hybrid. Not a corruption datapoint.** |
| **C5 compaction-verify audit** ✅ RESOLVED-BY-SPEC-READ | C5 governance / R10 | does compaction output re-pass Gate/verify before going live? | governance / read-consistency | **CORRECTS a pushed over-claim (D-C5-1): spec MANDATES post-compaction verify (C-OC3, CORE=1.0 abort) — not a gap. Open (analysis): non-CORE behavior_fail un-surfaced at read (tier-blind bit, R13-split reappears); non-CORE sampling-power deficit; livelock=prediction→C1. F1 readiness unchanged.** |
| **R1-bit commit-bit SELECT** ✅ DELIVERED-FOR-SCOPE | CP2 matrix R1 | does a G1 2PC commit-status bit deliver §8.9 L1 read-back, bleed-immune? | read-contract / index-query layer | **DELIVERED-FOR-SCOPE commit-time (D-R1-2, CORPUS/32): D1 8/8, D2 6/6, D3 4/4+2/2 via 2PC-abort, D4 Velloria proxy-TRIPLE→bit-NULL, D5 chain intact; post-commit divergence deferred to C1. CP-class, not promoted.** |
| **C6 ledger-immutability** ✅ RED-TEAMED (1 mechanism) | C6 security / §16 ledger | does the ledger detect operational-window tampering by a compromised authorized writer? | governance/security | **PROPERTY DEMO + SPEC FINDING (D-C6L-1, CORPUS/34; NOT empirical-red-team, NOT spec-falsification, NOT promotable): vs real G2 verify_chain — K1 rewrite-recompute + K2 truncation UNDETECTED, K4 naive-edit DETECTED (control), K5 STH-fix detects both. Finding: (A) spec mandates NO operational-window crypto tamper-evidence (keyless chain §16.1; anchors only root §13.2 + close §16.7) → spec-level property; (B) §16.5 Orchestrator-fs-write unreconciled with §16.2 Orchestrator-compromise-in-scope → W3 emergency entry rewritable = unreconciled threat-model seam. Fix=STH (custody-compatible §20.2). C6 not-red-teamed→red-teamed (one mechanism); stays open. Advisor corrected a self-undermining-gap over-claim.** |
| **R11 medium/severity ON READ** ✅ COHERENT (audit) | CP2 matrix R11 / C2 | does the read surface determine authoritative-medium/class + divergence severity AT READ? | read-contract / index-query layer | **SPEC-COHERENCE AUDIT (D-R11-1, CORPUS/33): COHERENT via derivation+prevention — (a) wrong-medium-on-read foreclosed by §11.3/D43 + §11.8 trip; (b) class/severity DERIVABLE from §7.2/C4-mandated entity_type (class=f(type)§11.2; severity=§11.7). Advisor corrected a 3-gap over-claim → residual = INSTANCE of known 'no query-language' root gap, NOT new conditions. Spec rec: pin query-result schema to return entity_type. NOT a falsifier, NOT promotable.** |
| **R1 SELECT read-back** ❌ NOT-DELIVERED | CP2 matrix R1| **R1 SELECT read-back** ❌ NOT-DELIVERED | CP2 matrix R1 | can a ledger-backed SELECT reconciled vs the deployed store deliver §8.9 L1 read-back? | read-contract / index-query layer (load-bearing) | **NOT-DELIVERED/CHARACTERIZATION (D-R1-1, CORPUS/31): anti-firing solid (LEAK 6/6 NULL, REJECTED 4/4, LANDED 8/8) but DROPPED divergence 1/2 — in-weight logprob recon bleed-unsound (phantom Velloria→Tokyo +2.06 nats); ledger must carry commit-status (B0/§11.2); post-commit divergence-detection open. NOT promoted.** |
| **R15 L2 constraint-probe** ✅ DONE | CP2 matrix R15 | can an in-weight edit make a prohibition FIRE under adversarial prompt? (§21.2, no delegation route) | read-contract / Constraint sub-type | **not-ready-with-conditions (D-R15-1, CORPUS/24): cooperative firing 24/24 → adversarial ~½ (~11–14/24 flag, ~7/24 silent leaks); controls clean; bounded easiest case, relational expected worse; spec-gap flag §21.2 warn-and-comply. NOT promoted.** |
| **R9 in-weight deletion residue** ✅ DONE | CP2 matrix R9 | does corrective in-weight delete leave residue on untouched paraphrases? | read-contract / deletion (re-tagged medium-delegated) | **CHARACTERIZATION (D-R9-1, CORPUS/25): residue 0/7 on held-out paraphrase but EASIEST case (localized self-made edit); mechanism=overwrite-toward-generic; 2/12 bystander collateral (G6.1 signature); native-knowledge redaction untested; §11.2 weights non-authoritative for all classes. NOT promoted.** |
| **D20 follow-ups** ⚠️ OPEN | D20-chunking, A1 | **(a) 2D N×C grid** — separate chunk-COUNT(K) from chunk-SIZE(C) [the gpt-5.5 confound]; **(b) SCALE** — single-solve cleanliness as N→thousands + the spec's 2,000-SIZE boundary vs the floor; **(c)** verify the spec's sub-batch semantics (vs our cache_c) | B3N condition-3 — could flip the in-weight verdict | ◆ GATED on a larger screened stimulus pool (operator effort call) |
| **Memory-lifecycle LOOP — Pruning/GC · out-of-band reconciliation · accumulate→compact→archive** (§11.12–13/§E) | G1 (2PC), A1 | exercise the production memory loop end-to-end, not just corruption-within | **≈half of production memory mgmt — UNTOUCHED**; required for a credible "production" claim | ☆ NEW — on the board now (was invisible) |
| **C2-band** | G6.1, C2 mechanism | does min-collinearity band [8-12] reduce **sequential** corruption? (falsifier) | scale mechanism → feeds D1 | ◆ lead — ⚠️ **REAL-BUT-UNDERPOWERED, NOT PROMOTED** (CORPUS/21, D-C2band-1 ⟨D-C2band-1@c6fb6103⟩): mechanical PASS (+18.73pp cross-JS) = real redistribution (within-loc FALL + expr 100% exclude under-editing); underpowered (1 seed), within-entity top-1 cost & mechanism unmeasured; de-confounders queued |
| **C/G7 multi-token** | recipe | multi-token value robustness at the write | write-robustness | ◆ |
| **Validation/Security/2PC empirical stress** (§9/§10/§11) | G1/G2/G3 prototypes | move from self-authored prototype → empirical stress (the prototype-tautology trap) | governance-readiness | ☆ deferred but on the board |

## ④ FALSIFIED / PRUNED (do NOT pursue — dead ground)
- **E1 Claim B:** LARQL `gguf-to-vindex` serving **Qwen2.5** — drops 108 attn biases (A7 causal ablation) → garbage. Use **Qwen3 family** or **llama.cpp**. [CORPUS/18]
- **relation-keying** — pruned (C2). [CORPUS/20]
- **A2b K_S staleness** — ruled out (large drift, zero benefit) → only revisit via A3/BetaEdit port. [CORPUS/16]
- **sequential incremental `cache_c` path** for deployment — A1 batch supersedes it (D-SCOPE-1). [CORPUS/14]

## ⑤ DISTANCE TO F1 (the readiness scorecard)

<!-- BEGIN GENERATED:f1-scorecard -->
**F1 READINESS SCORECARD (updated 2026-06-25 (F1 DETERMINATION FINALIZED — R11 read-contract COHERENT + C6 ledger-immutability red-teamed folded in; verdict NOT-READY-WITH-CONDITIONS, CONCLUDED))** — _auto-generated from `docs/program_state.json` — DO NOT edit between the markers; run `python3 tools/render_state.py --write`._

- **Deployment data path:** recipe ✅ → A1 batch-clean ✅ → B3 Q4_K_M-survival ✅ → E1·A CPU-serve ✅ → D1 structural ✅ (model-general) + numeric k≤1 SET on 3B ⚠️ (cross-model transfer OPEN)
- **Governance:** CP1 ✅ · CP3 ✅ · G1 ✅ · G2 ✅ · G3 ✅ · CP2 read-contract WEIGHTS-owned slice CHARACTERIZED (R15 not-ready-with-conditions ⚠️ ; R9 deletion characterization; §11.2 = no class weights-authoritative) — query-schema build-items + R5-at-scale still OPEN
- **Robustness:** native-knowing robust IFF no entrenched pretrained competitor (code/structural yes; common-knowledge domain_concepts no); C/G7 multi-token ❌; C2-band ⚠️
- **Critical path:** F1 read-contract slice SYNTHESIZED (verdict = bifurcation: native-knowing toward-satisfied-conditioned / structured-query burden relocated to unbuilt index). Remaining frontier: C1 compaction-at-true-scale (stimulus-gated) · index/query layer build+test (load-bearing) · C5/C6/C7 governance/security/pruning (Phase-2) · C4 7B transfer
- **Verdict:** DETERMINATION DRAFTED 2026-06-24 (`docs/F1_DETERMINATION.md`) = **NOT-READY-WITH-CONDITIONS** (draft-with-open-conditions, NOT a clean close; shippable as the honest current state). Deployment data-path spine PROVEN-FOR-SCOPE (recipe→A1 batch-clean→B3 Q4_K_M→E1·A CPU-serve; 3B/N≤100/band[4-8]/single-batch/1-seed/fictional). Architecture = scope-keyed COMPACTION-BOUNDED HYBRID (D-B3N-1), in-weight a serving copy per the verified §11.2/D42 structural finding (no class weights-authoritative). Determination carries a 10-row CONDITIONS REGISTER of first-class falsifiers: C1 compaction-at-scale (sharpest; D20 directionally negative) · C2 read-contract (biggest gap) · C3 R5-at-scale · C4 7B numeric transfer (OQ-W1) · C5 governance+orchestration (prototyped-not-empirical) · C6 security (un-red-teamed) · C7 Pruning/GC (untouched) · C8 R15-adversarial · C9 R9-native-deletion · C10 multi-token/G7. C1/C2 closing negative would move the verdict toward not-implementable-as-specified. Closure-path lead = UNGATED `tools/power.py` pool-sizing.
<!-- END GENERATED:f1-scorecard -->
- **Governance contracts:** CP1 ✅ · CP3 ✅(C15 open) · G1 ✅ · G2 ✅ · G3 ✅ · **CP2 ⚠️ build-items**
- **Deployment data path:** recipe ✅ → A1 ✅ → B3 ✅ → E1·A ✅ · **D1: structural ✅ (§8.7 amendment, model-general — D1+B1) · numeric guardrail ✅ SET (D-D1-2: k≤1 conservative; order/held-out-dominated; mixed-load→needs global-volume bound) · cross-model transfer ⚠️ OPEN (7B via determinism)**
- **Robustness:** C/G7 ❌ · C2-band ⚠️ REAL-BUT-UNDERPOWERED (CORPUS/21: mechanical PASS = real redistribution, not promoted — 1 seed + cost/mechanism unmeasured) ❌(lead)
- **CRITICAL PATH to a defensible determination:** **B3 in-weight-vs-side-store decision** (highest-stakes, graph-convergence) + **CP2 schema build-items** + **D1 numeric cross-model transfer** (3B guardrail k≤1 DONE; 7B OPEN).
  Everything else is either locked (don't re-run) or feeds these two.

---

## §0.4 ADDITIVE-UPDATE RULE (binding — how a new result enters here)
Every new result MUST attach to this map by declaring, in its CORPUS write **and** its staged finding:
1. **builds-on:** which PROVEN node(s) it stands on (or "new foundation" + why).
2. **advances:** which F1 criterion/chain it moves, and the **status delta** (e.g. `D1: OPEN→PARTIAL`).
3. **evidence:** CORPUS/NN + Decision-ID.
4. **additivity check:** if it neither builds on the proven base nor moves an F1 gap, it is **drift or
   redundancy** — the twin auditor (DISCIPLINE §3.2) rejects it regardless of internal correctness.

Then move the node between ①/③/④ and update ⑤. Re-mirror to memory. A run that does not change this
map's distance-to-F1 produced no F1 progress, however many numbers it generated.


### D-D1-2 — §8.7 numeric-threshold instrument (2026-06-21) [F1 numeric-threshold sub-item CLOSED on 3B; cross-model transfer OPEN]
**D-D1-2** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤1`** (max unanchored per-relation concentration; anchor by k=2; WARNING k=2-3, HARD k=8-10 — REVISED down from k≤2 after the seed-2 across-held-out check). Dual-reviewed (Opus advisor + gpt-5.5 cross-family). k=3-4/k=10-12 = scoped order-dominated observations, NOT portable thresholds; per-relation count = fail-closed SENTINEL not the causal var (edit-set/key-collinearity geometry is). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. Artifacts: results/d1_threshold_lowk_3b_s3{,_lowextra}.json, results/d1_instrument_variance_diagnostic_3b_*.json; reviews logs/codex_review_threshold_*OUT.log. **MIXED-LOAD:** pure-capital fails under +12 other-relation load (mixed clean ceiling k=0; driver=other-relation volume) → vindicates the worse-of(global,per-relation) amendment design; pair k≤1 with a global-volume bound + compaction. **SEED-2 (more-toxic held-out):** corrupts at k=1-2 where seed-3 was clean → ceiling k≤2→k≤1; no per-relation count is universally clean (held-out-dependent SENTINEL, not the causal var). +results/d1_mixedload_smoke_3b_s3.json, results/d1_threshold_lowk_3b_s2.json.
