# Re-Grounding Comprehensive Plan — v2 (post-council, pre-runbook)

**Date:** 2026-06-22. **Status:** revised DRAFT, absorbing the Framework Council synthesis (`REGROUNDING_COUNCIL_SYNTHESIS.md`) + Advisor + Codex + 3 operator decisions (build the stimulus pool; compaction-at-scale & read-contract co-equal in Phase 1; one more cross-family pass before runbook). **Not yet the runbook.** Mission unchanged: comprehensively evidence (or disprove) the spec's requirements across ALL layers → F1 ready/not-ready-with-conditions.

---

## §0 — North star (sharpened)
F1 = prove/falsify the LLM-as-Database spec is implementable across all layers, **outcome-level** (spec mechanism OR an evidenced equivalent), delivered at a **committed, stated scope**. **CARVE-OUT (Warden C5):** security/authorization/audit/provenance clauses are **NOT** outcome-equivalence-eligible — they require the spec's *mechanism* (non-bypassability / isolation / least-privilege / mandatory-provenance), proven by architectural + red-team evidence, because an "equivalent" that authorizes through a different unaudited path passes an outcome test while defeating the contract.

## §1 — Epistemology: typed evidence modes (answers "why falsifiable")
Every requirement gets a **requirement-type** that selects its matched evidence mode. Falsification is the tool for *universal* claims; it is NOT the only tool:
| Requirement type | Evidence mode | Example |
|---|---|---|
| Universal / reliability / safety | **empirical-falsifier** (survive a test that CAN fail) | "no held-out corruption"; "no resurfacing after delete" |
| Existential / capability | **constructive-demonstration** ("demonstrate proven" — correct here) | "a SELECT primitive exists"; "an edge is reverse-lookable" |
| Quantitative / threshold | **threshold-calibration** (find the breaking value) | capacity ceiling; ε pass-threshold (§22); drift tiers |
| Protocol correctness | **fault-injection / state-machine** | 2PC atomicity; crash recovery; rollback idempotency |
| Security invariant | **red-team + architectural proof all paths pass policy** | Gate exclusivity; token single-use; audit completeness |
| Comparative | **A/B benchmark** | in-weight vs RAG vs hybrid (does in-weight buy anything?) |
**Every matrix row carries a "what result makes this FAIL" column.** A row whose test cannot fail is rejected (the prototype-tautology guard). **PROVEN-FOR-SCOPE is invalid without its full scope tuple:** model · edit-count · relation-distribution · chunking · quantization · probe-family · decoding · query-type · failure-detector.

## §2 — Matrix spine = the Database Behavioral Contract (not spec-section order)
The requirement matrix is organized FIRST by a database behavioral contract — **read · write · update · delete · transaction-visibility · provenance · authorization · lifecycle · deployment-equivalence** — and each spec layer (§7–§12) maps ONTO which part of that contract it satisfies. (Structural fix for write-centrism; Codex.) This makes "is it a database?" the organizing question, not "did the edit land?"

## §3 — Phase 1 = the MEMORY-CONTRACT SUBSTRATE (GPU priority), TWO co-equal leading edges + the write-scale gates
Phase 1 is NOT "model-only" — it is "which database obligations can the model/weights carry, vs which require the `.vindex`/Git/governance overlay." It runs on a **shared stimulus-pool infrastructure** (§5.1). The single 4090 serializes GPU runs; "co-equal/parallel" = both edges are designed, pre-registered, and harnessed together and share the pool, with GPU runs interleaved.

**Leading edge A — Compaction-CORE-retention-at-scale (top falsifier; already directional-negative).**
- Probe over the **cross-entity BYSTANDER population**, not only declared edges (the spec's own `CompactionProbeReport` §11.14 samples declared edges → blind to where D20 corruption lands).
- **2D N×C grid** to break the K-vs-C confound (accumulated-update-COUNT vs chunk-SIZE) + **single-joint-solve at true scale** (total-N → 2,000, the spec's real regime).
- Pass = CORE retention **exactly 1.0** (zero losses), bystander reads clean at the committed drift size. Exercise a real CORE-failure → `COMPACTION_ABORTED` path.
- Frames as a **liveness** gate too (State): abort → anchor never resets → drift never clears → writes suspend (READ_ONLY wedge).

**Leading edge B — The Read / Query contract (biggest gap; the "is it a database" test).**
- **B0 (BLOCKER, gates everything below it): demonstrate a structured SELECT primitive distinct from free-form INFER**, and SPLIT the L1 write-verification SELECT from the runtime query-surface SELECT. (CP2 found LARQL `SELECT FROM EDGES` cannot read back a triple → this may be partially unbuildable as specified; that finding is itself F1-relevant.)
- **B1 (lead read falsifier): negative reads** — query absent keys against a closed-world ground-truth; ANY non-null = FAIL; report a **confabulation rate**. (If the model confabulates absent keys, every present-key PASS is untrustworthy.)
- **B2: reverse-lookup / bidirectional** (every edge reverse-lookable; oracle = D16 auto-reverse forward-set), **aggregation**, **relation-family queries** (all 5 D6 families, not just Knowledge-triples), **DELETE-FROM-EDGES** (true deletion vs revert) + **deletion-non-resurfacing-under-paraphrase**.
- **B3: native-knowing / reason-over-fact** (does the fact FIRE in downstream reasoning, not just SELECT-read-back) — the L2 behavioral probe incl. the never-tested §21 **Constraint** probe.
- **Storage-pass / behavior-fail**: measure the base RATE of this named mode (§8.9), don't just demonstrate the detector can fire.

**Write-engine scale gates (co-equal with A/B — Write is NOT "done"; MEMIT C4).** On the shared pool:
- **W1: capacity ceiling as a CURVE to the breaking point** (facts/relation × total-N → forgetting/collision) — NOT a self-selected safe operating point.
- **W2: general-capability retention at scale** — a held-out general-benchmark delta (not edited-fact recall) after 100s–1000s of edits on the deployment model. (The literal other half of "model-as-memory-layer.")
- **W3: compaction Component-1 SCALE** (folds into leading edge A).

## §4 — The BINDING seam register (a co-equal Phase-1 deliverable, not a side-list)
Phase-1 experiments MUST emit the measurements Phase-2 governance consumes. Three classes:
- **Behavioral seams:** post-write L1/L2 probe split (§8.9); drift predictor (§8.7, concentration/order-aware, in an ONLINE-readable form, not only offline); compaction heal/abort (§11.14); negative-reads / conflict / supersession / deletion-resurfacing; isolation (uncommitted not visible) / rollback-abort-invisibility; quantized-query-equivalence (Q4_K_M preserves negative/conflict/query behavior, not just edited-fact recall).
- **Capture-now timing/availability seams (Orchestration C6 — exist only while GPU runs happen):** compile + compaction **wall-clock at the 2,000-scale envelope**; **mount-window read-block duration**. (Phase-2 lock TTLs / PREPARED timeouts / idle-window N are un-calibratable without these.)
- **Discriminator-bit seams (Warden C6 — non-retrofittable into weights):** the served model must carry/expose **provenance**, **commit-status** (committed vs uncommitted), and **deletion-tombstone** bits — Phase 2 cannot add a bit the weights don't carry. Plus dual-medium **content-class severity** (Git-authoritative structural vs `.vindex`-authoritative layer4 → failure bar differs by class).

## §5 — Cross-cutting deliverables
1. **Stimulus-pool infrastructure (Phase-1 build — operator-approved).** A larger screened single-token fact pool serving BOTH leading edges: large-N for compaction/ceiling; **closed-world ground-truth** for negative reads; **reverse-lookup pairs**; **5-relation-family** coverage; **CORE/SUPPORTING/INCIDENTAL** importance tags for the compaction probe. First artifact to spec + build.
2. **Scope envelope = a ceiling CURVE, not a safe point** (W1). The committed operating point is stated WITH the breaking point it sits below.
3. **Risk-ranked falsifier priority** (spec-killers first). Current rank: #1 compaction-CORE-at-scale (already cracking); #2 read-contract SELECT-primitive + negative reads (biggest gap, not yet failing). Both Phase-1.
4. **Method-typed evaluation oracle (§21.4):** exact_substring / structured_field_match for read-correctness + CORE-retention (exact, zero-loss); judge_model_classification only where unavoidable, **frozen at template commit**; adversarial-human samples calibrate the judge, they are not the runtime grader.
5. **ε pass-threshold calibration (§22)** — schedule it; without a measured ε every L2 threshold is a free parameter (tautology vector).
6. **Baseline comparison** in-weight vs RAG-only vs hybrid (does in-weight buy anything contractually? = B3N Axis A as a first-class experiment).

## §6 — Findings re-validation = RE-GRADE (not presence-check) + demotions
| Claim | → Re-grade | Why |
|---|---|---|
| A1 batch-clean | constructive-demonstration at ONE point (3B/N≤100/1-seed) | B1 wobbled to 91.7% @7B; A1-clean IS the "compaction returns to clean" premise under the B3N hybrid |
| G3 Validation | constructive-demonstration | independence = identity-collision only; Reflexion fix-step stubbed; storage leg = intent-index not deployed store |
| T2.5/A5 compaction-regression | COVERED-WEAK / MIS-TARGETED | n=18/6, no importance stratification, no CORE=1.0 abort, no bystander coverage |
| CP2 "L1 SELECT delivered" | at risk | over an intent-derived index, not the deployed store (L2 wearing an L1 label) |
| k≤1 §8.7 | keep as fail-closed SENTINEL | per-relation count is NOT the causal var; don't inflate to "the threshold" |
| G2 Security | PROVEN-FOR-SCOPE (verifier mechanics) — keep, but NOT red-teamed | 9/9 CORPUS/11; understated by the package; full red-team = Phase 2 |

## §7 — Phase 2 = governance/protocol (deferred, fed by Phase-1 seams)
2PC/TC/State-Ledger/circuit-breaker (fault-injection + state-machine); Patch Authorization Gate / token lifecycle / audit-immutability / red-team (security mechanism, NOT outcome-equivalent); Orchestrator control plane / lock-hold registry / review queues (mostly DEFER design, sized by the Phase-1 timing seams); Pruning/GC + out-of-band reconciliation loop. Built ON the Phase-1 seam emissions; lock TTLs / idle-window N calibrated from the capture-now timing seams.

## §8 — Build method + worked template
Spec-first, layer-by-layer requirement extraction into the §2 matrix. **Template the experiment-DESIGN workflow on the Read contract** (hardest falsifiability design, biggest gap); **template the findings re-grade on the Write Engine** (cheap mechanical re-validation, exercises the fold-in muscle). Pre-register pass/fail (that CAN fail) + advisor + gpt-5.5 cross-family at each promote gate; close-out gate per result.

## Open forward RISK (surface, don't bury)
The SELECT-primitive question (B0) may show part of the read contract is **unbuildable as the spec writes it** (CP2 signal). That is an F1-relevant finding, not a blocker to the plan — but it means the read contract could resolve to "not-ready-with-conditions (needs a query-layer the spec under-specifies)" rather than a clean pass. The plan must be able to record that honestly.

---

## §9 — Independence-pass reconciliation (Advisor-v2 + Codex-v2, 2026-06-22) — BINDING deltas
Both cross-family passes converged (independently) on the same corrections. These OVERRIDE the co-equal framing above where they conflict.

**D1 — The #1 honest-F1 risk = SCOPE LAUNDERING / closed-world (Codex + Advisor, same insight).** The central tautology to prevent: *"LLM-as-Database is implementable because the database parts that aren't implementable in the LLM were quietly assigned to the `.vindex`/Git/governance overlay."* Root cause: **an LLM has no closed world** — the base model knows millions of facts we never committed, so negative-reads (B1) is really "can in-weight editing impose closed-world semantics on an open-world model," which it structurally cannot without the commit-status/provenance gate that lives *outside* weights → loops to B3N. **Spec-checked (this session): the spec specifies NEITHER strict closed-world NOR fall-through — the read semantics are genuinely under-specified** (only "natively know" + the L1 SELECT write-verification; §26 provenance is external-staleness only). **FIX (binding): a Medium-of-Obligation Table authored BEFORE any experiment** — every contract row tagged `WEIGHTS_MUST_CARRY | VINDEX/GIT_MAY_CARRY | GOVERNANCE_MAY_ENFORCE | HYBRID_ALLOWED | OUT_OF_SCOPE`; every PASS/PARTIAL/FAIL must cite it. If B0 only works via an external index/verifier, the verdict reads "hybrid-read passed; weight-native SELECT failed/unshown" — never a laundered pass.

**D2 — B0 first, before the stimulus-pool build. Critical path (both):** (1) **B0 SELECT go/no-go micro-harness** (tens of facts, absent keys + edited facts; cheap; no pool) → (2) **minimal stimulus pool V0** (only after B0 resolves) → (3) **negative-reads B1** (cleanest DB-read falsifier; if it fails badly, Edge B may already be not-ready) → (4) **compaction-at-scale Edge A** (small N×C pilot to validate bystander + abort/liveness instrumentation, then scale) → (5) **pool V1 / large-N expansion** → (6) **write gates W1/W2 as SENTINELS** attached opportunistically to large runs. Don't build a large pool optimized for a read primitive that may not exist.

**D3 — "Co-equal" = co-DESIGN, not co-EXECUTE.** Single 4090 serializes GPU by information value (cheapest blocker first). CPU/design work (stimulus schema, B0 harness, compaction harness, oracle defs) runs in parallel; heavy GPU lines do NOT interleave until B0 passes. When heavy runs do start, **compaction-at-scale grid leads** (risk-rank #1).

**D4 — De-scope the write gates (v2 over-corrected by re-centering Write).** W1 → curve-DESIGN artifact + one sentinel run (not a full breaking-point campaign in Phase 1); W2 → small held-out regression sentinel attached to large edit runs (not a standalone study); full capacity/forgetting characterization → Phase 1b, only if B0 + compaction survive. Phase-1-CORE vs Phase-1-if-time must be marked (also deferrable: full 5-relation-family → start 2+structural; in-weight-vs-RAG baseline → defer, it's a study not a gate).

**D5 — `constructive-demonstration` is an escape hatch (both).** Valid ONLY for "can this work at ONE scoped point." NOT valid for reliability/invariant claims (read reliability, negative reads, compaction safety, deletion-non-resurfacing, transaction-visibility, authz/security, provenance, deployment-equivalence) — those need empirical-falsifier / fault-injection / red-team. **B0 itself conflates two claims:** "a SELECT primitive EXISTS" (constructive) vs "it reads back ALL committed facts reliably" (universal → falsifier) — don't let the constructive framing launder the reliability claim (testing our own SELECT = the tautology at program scale). G3→constructive-demo OK ONLY if explicitly "existence at one point," never "governance works."

**D6 — Add a 7th evidence mode: compositional/integration invariant (Codex).** Some obligations fail only when independently-valid pieces interact: write→compact→delete→quantize→read; commit→rollback→provenance→audit. Need scenario traces with state transitions + cross-layer assertions, not single-layer tests.

**D7 — B0 operational definition (fail-fast, Codex):** structured input (entity/relation/key) → structured value OR null (not free-form prose); no temperature/beam semantic dependence; no hidden judge interpreting prose; retrieves an edited triple the base model did NOT already know; distinguishes deleted/reverted/tombstoned if in scope. Else B0 = "INFER wearing SQL clothing." Caveat: "split L1-verify-SELECT from query-surface-SELECT" — if L1 verify uses an external index, that's HYBRID retrieval, not in-weight SELECT (tag it in the Medium-of-Obligation Table).

**D8 — Pool needs TWO kinds of negatives (Advisor):** fictional/synthetic entities (model has no prior → clean confabulation rate) AND real-but-uncommitted facts the model knows (the leak/provenance test). Force ≥1 discriminator-bit probe (provenance/commit-status/deletion-tombstone) INTO B0/B1, not just the seam list.

**D9 — Propagate demotions to DECISIONS, not just findings (Advisor).** A1→constructive-at-one-point *tightens B3N* (the hybrid rests on A1-clean); the re-validation must re-examine the decisions built on a demoted brick, or it relabels a brick while the wall still claims to stand.

**D10 — META (both reviewers, explicit): this is the LAST review. The next artifact is PILOT RESULTS (B0), not a plan v3.** Advisor×2 + Codex×2 + 6-domain council is sufficient scaffolding ([[evidence-over-scaffolding]]). Reconcile → run B0.
