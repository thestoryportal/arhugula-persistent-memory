# Re-Grounding Comprehensive Plan — Framework Council review packet

**Status:** DRAFT proposal under review (2026-06-22). Not yet durable runbook. This packet exists so the Framework Council can advise on the plan, with the cross-family Advisor (Opus) + Codex (gpt-5.5) reviews already folded in as inputs. **Council use here = spec-contract framing / domain-coverage audit of the PLAN (sanctioned), NOT confirming empirical conclusions.**

---

## 1. The recalibrated mandate (operator, this session)
Build a COMPREHENSIVE PLAN to fully run experiments that **definitively evidence (or disprove) the spec's requirements across ALL layers**. North star unchanged = **F1**: prove/falsify the LLM-as-Database spec is implementable before it's built; ready / not-ready-with-conditions.

- **GPU priority = evidence the MODEL ITSELF as the memory layer first.** Governance/protocol layers (Validation/Security/2PC/Orchestration) come *after* the model-memory proof is durable.
- **Outcome-level:** a requirement counts as met if the spec's prescribed mechanism works OR an evidenced equivalent achieves the same outcome.
- **Fold in BUT re-validate** every existing finding (honest re-grade; re-run only if a genuine gap surfaces).
- Deliverable = durable repo docs (sharpened north star, spec-requirement surfacing, research, hypotheses) → a **ready-to-execute comprehensive runbook**.

## 2. Where the program stands (to be folded in + re-validated)
- **PROVEN-FOR-SCOPE (3B / N≤100 / batch):** write→deploy spine — Genesis batch compile corruption-clean (A1) → survives Q4_K_M (B3/CORPUS-17) → serves edited facts on CPU (E1/CORPUS-18).
- **AMENDED §8.7:** count-only `edge_count_since_anchor` is the wrong predictor; corruption is relation-concentration- + edit-ORDER-dominated → concentration-aware guardrail **k≤1** (D1/B1/D-D1-2). 7B numeric transfer OPEN.
- **DECIDED (reasoned, not empirical PASS) — B3/D-B3N-1:** in-weight NOT contractually required; spec's write model = compaction-bounded HYBRID, in-weight-viable under 3 conditions (concentration-aware §8.7 · compaction-before-envelope · **compaction-at-scale cleanliness**).
- **DIRECTIONAL — D20:** accumulating sub-batched compaction can REINTRODUCE corruption even when the joint solve is clean; K-vs-C confound + true 2,000-SIZE regime open → pressures condition 3, not yet falsified.
- **COVERAGE MAP:** Write Engine + Deployment = PROVEN-for-scope. Validation/Security/2PC = PROTOTYPED only. **Read/query contract = biggest gap, untested. Memory-lifecycle LOOP (Pruning/GC, reconciliation, accumulate→compact→archive) = UNTOUCHED. Orchestration = not engaged.** Self-criticism driving this re-grounding: **work has been WRITE-ENGINE-CENTRIC, lost whole-system scope.**

## 3. THE PLAN PROPOSAL (after Advisor + Codex revisions)
1. **Matrix spine = a Database Behavioral Contract** (read/write/update/delete/transaction-visibility/provenance/authorization/lifecycle/deployment-equivalence), with spec layers mapped ONTO it — not organized by spec section order. (Structural fix for write-centrism; Codex.)
2. **Typed evidence-mode column** — each requirement gets its matched tool: `empirical-falsifier` (universal/reliability) · `constructive-demonstration` (existential/capability — "demonstrate proven" is correct here) · `threshold-calibration` (quantitative) · `fault-injection` (protocol correctness) · `formal/state-machine + red-team` (security invariants) · `comparative-benchmark` (in-weight vs RAG vs hybrid).
3. **Phase 1 = "memory-contract substrate," Read CO-EQUAL as a hard gate** (not a follow-on). Explicitly partition WHICH database obligations live in weights vs `.vindex`/Git/governance. Template the experiment-DESIGN workflow on the **Read contract**; use Write Engine only for a small matrix-format example + the cheap mechanical findings re-grade.
4. **Phasing = sequential-with-BINDING-seam-register.** Phase 1 (model-memory, GPU) → Phase 2 (governance/protocol). Seam register = Phase-1 experiments must EMIT the measurements Phase 2 consumes. Seams: post-write probe §8.9; drift contract §8.7; compaction §11.14; Pruning/delete §11.12; PLUS (added by review) negative reads, conflict/supersession, deletion-resurfacing-under-paraphrase, native-knowing/reason-over-fact, isolation (uncommitted not visible), rollback/abort-invisibility, quantized-query-equivalence, dual-medium content-class severity, CORE-retention-through-compaction, online-usable metrics.
5. **Four added deliverables:** target/capacity **scope envelope** (committed operating point: model size / N / churn); **risk-ranked falsifier priority** (attack spec-killers first, not layer-march); **evaluation-oracle** definition (who judges answer-correctness: deterministic canonicalization + adversarial human-reviewed samples; not naive exact-match, not unguarded LLM-judge); **baseline comparison** (in-weight vs RAG vs hybrid — does in-weight buy anything contractually?).
6. **Findings re-validation = re-grade against the typed bar + DEMOTE** confirmation/construction passes; restate every PROVEN-FOR-SCOPE with its full scope tuple (model · edit-count · relation-dist · chunking · quantization · probe-family · decoding · query-type · failure-detector).

## 4. ADVISOR (Opus, cross-family) feedback — folded in
- Epistemology under-typed: add requirement-TYPE column (universal→falsify; existential→constructive proof; threshold→calibrate; comparative→A/B). Operator's "demonstrate proven" instinct is correct for the capability class.
- Template on **Read** (design workflow), Write only for findings re-grade — templating where the method's risk (tautology on an unworked cell) is ABSENT is the trap one level up.
- Phasing sequential-with-seam-register OK, but: (i) guard Phase 1 against collapsing back to write-centric; (ii) test model behavior at GOVERNANCE-REALISTIC operating points; (iii) missed seams: native-knowing/reason-over-fact as first-class; dual-medium content-class severity (Git-authoritative structural vs `.vindex`-authoritative layer4 → failure bar differs by class); CORE-retention-through-compaction=1.0 as a possible spec-killer.
- Missing deliverables: target-scope envelope; risk-ranked falsifier priority.
- Findings re-validation = re-grade + explicit demotion of construction/confirmation passes.

## 5. CODEX (gpt-5.5, cross-family) feedback — folded in (full log: logs/codex_regrounding_review_OUT.log)
- "Proposal risks an honest-looking F1 that is really a memory-EDITING F1, not a DATABASE F1." Invert center of gravity to the read/query contract with explicit DATABASE WORKLOAD SEMANTICS.
- Split evidence types (empirical / constructive / fault-injection / formal-state-machine / red-team). Protocol correctness (2PC atomicity, rollback), security invariants (non-bypassability), governance/auditability need constructive/formal evidence, NOT just empirical survival.
- "PROVEN-FOR-SCOPE" must name the full scope tuple or it inflates.
- Seam register must be BINDING not decorative. Missed seams: read semantic contract (what is a query/answer/refusal/unknown/stale/conflict), negative reads, conflict resolution, provenance-conditioned reads, deletion semantics (no resurfacing under paraphrase), isolation, rollback/abort visibility, quantized deployment equivalence of query behavior, monitoring observability, capacity envelope.
- "Model as memory layer" is NOT separable from governance if the memory contract includes commit-status/delete/provenance/versioning → Phase 1 = "memory-contract substrate" defining what lives in weights vs overlay/Git/governance.
- Missing experiment classes: read/query workload suite; false-positive measurement; OOD/adversarial prompting (prompt injection, leading questions); compositionality (A→B,B→C ⇒ A→C?); update semantics (overwrite/supersede/merge); deletion/pruning/GC resurfacing; longitudinal lifecycle; crash/fault matrix; external-overlay-dependence (`.vindex`/Git stale/unavailable/inconsistent); security boundary tests; scale realism (relation/entity skew, namespace collisions); evaluation oracle; baseline comparison.
- One change: matrix STARTS with the Database Behavioral Contract; Phase 1 includes a read/query falsifier suite as a HARD GATE, not follow-on.

---

## 6. COUNCIL MANDATE (this packet)
Each specialist: advise on whether THE PLAN (§3, as revised by §4/§5) will **comprehensively evidence YOUR domain's spec contracts across all layers** — and what it will systematically MISS. Be adversarial. Stay in domain. Cite spec clauses (CORPUS/05 + the spec) and existing evidence (CORPUS/00-02) under COUNCIL_PROTOCOL rules (cite-or-flag; EVIDENCE-SHOWS vs I-INFER; mechanics ≠ contract). Build on the Advisor/Codex points — do not merely repeat them.
