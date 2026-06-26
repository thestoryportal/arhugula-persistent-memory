# CORPUS — LLM-as-Database Viability Evidence (single source of truth)
_Built 2026-06-18. Purpose: a deduplicated, provenance-anchored evidence corpus for (a) the Framework Council adversarial review, (b) self-review, (c) human-in-the-loop review. Every claim resolves to a raw artifact in `/workspace/`._

## Read order
1. **`00_MASTER_EVIDENCE.md`** — canonical experiment ledger (one row per experiment, exact numbers, status). THE source of truth.
2. **`01_PROVENANCE_MANIFEST.md`** — claim → {script, result file, exact numbers}. Anti-hallucination backbone.
3. **`02_VANDV_CHAIN.md`** — hypothesis → method → measurement → criterion → verdict, per claim.
4. **`03_STATUS_LEDGER.md`** — proven / partial / untested / **corrected-from** (every reversal, with why).
5. **`04_ENV_AND_DEPS.md`** — environment, toolchain, version traps, reproducibility.
6. **`05_SPEC_CONTRACTS_BY_DOMAIN.md`** — the spec's own contracts per council domain = the audit baseline.
7. **`07_CP1_GOVERNED_INPIPELINE_WRITE.md`** — CP1 result (2026-06-18): governed in-pipeline parametric MEMIT write PROVEN-FOR-SCOPE.
8. **`08_CP2_QUERY_SCHEMA_CAPABILITY.md`** — CP2 result (2026-06-18): LARQL LQL verbs execute (DELETE works) but L1 triple-readback / 5 families / violates-rejection are our schema-layer build items.
9. **`09_CP3_MEMIT_COMPLIANCE.md`** — CP3 result (2026-06-18): D12 method-class CONFIRMED (null-space = D20-mandated); C15 layer-band an open divergence.
10. **`10_G1_TWO_PHASE_COMMIT.md`** — G1 result (2026-06-18): dual-medium 2PC + State Ledger + Transaction Controller + circuit breaker PROVEN-FOR-SCOPE (10/10).
11. **`11_G2_SECURITY_LAYER.md`** — G2 result (2026-06-18): REAL Ed25519 — verify-cannot-forge (structural), content-level overlay integrity, CAK CeremonyToken verifier PROVEN-FOR-SCOPE (9/9).
12. **`12_G3_VALIDATION_PIPELINE.md`** — G3 result (2026-06-18): deterministic schema validator delivers the CP2-surfaced contracts (violates/undeclared rejection + storage-probe split) + §9 invariants PROVEN-FOR-SCOPE (8/8).
13. **`13_G6_1_SCALE_OF_N.md`** — G6.1 result (2026-06-18): **first empirical falsifier, SPLIT.** Write-side PASS at N=100 (98% retention, apply-expression 100%); **cross-entity consistency FAIL — held-out reads at the edited relation corrupted, scale-amplifying (100→42%).** Falsifies "cross-entity-clean at scale"; scopes the prior same-entity "VALIDATED."
14. **`14_A1_BATCH_VS_SEQUENTIAL.md`** — A1 (2026-06-18): batch/Genesis ELIMINATES the G6.1 cross-entity corruption (flat 100→100→100% @N≤100); corruption was incremental-schedule `cache_c` leakage, not in-weight storage.
15. **`15_A2_RELATION_BALANCED_SENTINELS.md`** — A2 (2026-06-18): in-solve same-relation sentinels HALVE the runtime-incremental corruption (8→16–17/20 @N=100, λ_s≈1–2) but don't arrest the N50→100 decline → PARTIAL.
16. **`16_A2b_REFRESH_KS.md`** — A2b (2026-06-18): refreshing the sentinel keys K_S against drifted W does NOT help (3-seed paired + clean seed-0) → **K_S staleness RULED OUT**; large drift + zero benefit = entity-specific residual → A3 (BetaEdit). Official BetaEdit repo found (port, not reimplement).
- **17 — B3 / G6.2 Q4_K_M QUANTIZATION SURVIVAL** = PASS: A1-clean batch store survives real Q4_K_M (edits 100% vs native 97.4%); margin confound characterized; E1 untested.
- **24 — R15 L2 CONSTRAINT-PROBE firing (D-R15-1, 2026-06-24)** = not-ready-with-conditions: the sharpest WEIGHTS-owned read-contract falsifier (§21.2, no delegation route). v1 subject-property hazard edits express perfectly + fire under cooperative paraphrase (24/24) but adversarial firing collapses to ~½ (hand-adj ~11–14/24, ~7/24 silent compliance-leaks; 2/24 explicit refusals). Controls clean. Bounded: easiest single-entity case (relational archetype expected worse). Spec-gap flag (Finding 2): §21.2 disjunctive pass admits warn-and-comply (suggestive).
17. **`additional_research.md`** — prior art + research pointers.
8. **`COUNCIL_PROTOCOL.md`** — rules every council subagent runs under (cite-or-flag; evidence vs inference; verdict schema).
9. **`domains/*_PACKAGE.md`** — focused per-specialist package (contract + relevant evidence + open questions + audit charge).

## Scope of what was tested (one paragraph)
In-weight, MEMIT-class knowledge editing was validated as a write engine for the "LLM-as-Database" spec, then composed with **LARQL** (the spec's read/query/deploy layer) on CPU. Editing science validated on **Qwen2.5** (3B/7B) + GPT-J baseline; re-validated on the LARQL-servable **Qwen3-0.6B**. A **decoupled bridge** (our clean edit → `.vlp` overlay → `APPLY` on frozen base → `COMPILE`) achieves clean+in-weight+governed serving with no LARQL code. **What is proven = write/read/overlay MECHANICS. What is NOT yet tested = full spec CONTRACTS** (2PC/State-Ledger consistency, write authorization/audit, deterministic validation pipeline, full query schema SELECT/DELETE, operator Intel-CPU). The council's job is to audit evidence against contracts per domain.

## Headline status (see 03 for the full ledger)
- ✅ In-weight multi-field editing viable; model/size-dependent (GPT-J fails, Qwen-7B clean, Qwen-3B/Qwen3-0.6B work with recipe).
- ✅ Recipe = in-solve AlphaEdit (null-space P, `nullspace_threshold=0.005`) + preserve-sampling + batched-per-record compile.
- ✅ Decoupled bridge: clean + in-weight + governed-overlay, on CPU, **no LARQL code**.
- ⚠️ Governance proven = file-level frozen-base + overlay + rollback. NOT the spec's 2PC/State-Ledger. (Gap.)
- ⚠️ Security (write authz/audit/signing), validation pipeline, full query schema, operator-CPU: **UNTESTED**. (Gaps.)

- **37 — C10 W-realization band-knob (D-C10e-bandknob ⟨D-C10e-bandknob@82b491dc⟩, 2026-06-26)** = NO MATERIAL KNOB RESCUE: later `[8,12]` worsens A7 para_full 13.9 to 5.6 while canon_full only 29.2 to 45.8; A1/A2 controls high; pure later-band W-realization eliminated, broader knobs and AnyEdit remain open.
