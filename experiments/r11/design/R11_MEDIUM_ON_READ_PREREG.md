# R11 — Content-scoped authoritative-medium & severity *on read* (pre-registration)

**Date:** 2026-06-25 (frozen before build). **Decision-ID:** D-R11-1 (pending). **CORPUS:** 33 (pending).
**Class:** **SPEC-COHERENCE / SPEC-GAP AUDIT — NOT a falsifier, NOT a CP-class delivery.** Per the read/query contract matrix (`docs/READ_QUERY_CONTRACT_MATRIX.md` line 33), R11 is **category ③: STORAGE/AUTHORITY → medium-delegated per §11.2; an in-weight failure CONFIRMS the overlay, it does not falsify.** "Fault-injection" in the matrix evidence-type column is a *testing technique*, not an evidence class — fault-injecting a resolver **we author** would only test our own routing code = the [[prototype-tautology-trap]]. Advisor (2026-06-25, full-transcript) mandated this reframing: **target the SPEC, not our resolver.**
**Frontier note:** the 2026-06-25 FRONTIER INFLECTION holds — the weights-owned falsifiers are exhausted; *all* remaining C2 read-contract legs (R4/R7/R8/R11/R16) are non-falsifiers. This is design-viability / spec-gap BUILD work (the #1 ungated priority), explicitly **prototype-class**. The result will be labelled **prototyped-not-empirical (C5-class), NOT a promotable node.**
**Matrix row:** R11. **Condition:** F1 **C2** read-contract (the operator-chosen #1 frontier; biggest gap). **Builds on:** R1/R1-bit (CORPUS/31, 32) — which delivered commit-TIME SELECT read-back via a ledger commit-bit; R2 (CORPUS/27, weights write-only); B0/R6 (commit-status ledger-delegated); §11.2/D42 (no content class is weights-authoritative — the load-bearing structural finding).

## The question (targets the SPEC's read surface, not our code)
§11.2/D42 assigns the **authoritative medium by content-class**: **Git** authoritative for `structural_entity`; **`.vindex`** authoritative for Layer-4 `domain_concept` + `constraint_rule`. The matrix R11 failure mode is *"wrong medium wins on a read divergence; failure-severity not class-differentiated."* The pre-registered question is **whether the spec's READ/query result surface carries enough information, at read time, to:**

- **(a) MEDIUM/CLASS-ON-READ:** determine the content-class / authoritative medium of a returned fact (structural→Git-auth vs L4→`.vindex`-auth), and
- **(b) SEVERITY-ON-READ:** class-differentiate the failure severity of a read divergence/integrity concern (a structural read-error is Git-recoverable; an L4 read-error is potential data loss — the asymmetry the spec itself encodes for *compensation* in §11.7/D47).

This is decided by **reading the spec**, made concrete by a constructive demonstration (below). The demonstration's read-surface inventory is grounded **only in cited spec lines** so a FAIL is a property of the spec text, not of our harness.

## Spec read-surface inventory (frozen — every read-time-exposed field, with citation)
Exhaustive grep of the spec (v1.2, 2909 lines) for read/query-result exposure. The query/read **result** surface exposes exactly:
1. `provenance_flag ∈ {STALE, UNAVAILABLE}` — **"visible in query results"**, §26.3 (line 1871). **Scope: Layer-4 *external-sourced* facts only** (advisory, never blocking, C-EXT-PROV2).
2. `coverage_quality` flag — IC4 (line 2130): "Orchestrator receives query results with `coverage_quality` flag; empty results route to documentation ingestion."
3. L1 storage probe: `SELECT` read-back "confirms the edge was written" — §8.9 (line 391). Confirms *existence*; specifies no class/medium/severity field on the returned value.
4. (Archived entries carry a read-time decompression/verify *cost*, §27 line 2035 — not a content field.)

Content-class differentiation is specified **only OFF the read path**:
- **Write time:** `CONTENT_CLASSIFICATION ∈ {structural, layer4_domain}` mandatory on every `.larql` patch (§11.2, line 638); recorded in the PREPARED/COMMITTED ledger entries (§11.5).
- **Commit/compensation time:** class-differentiated compensation (§11.7/D47, line 690): structural → auto-revert Git; layer4_domain → retry ×5, Git revert needs human confirmation. **This is the severity asymmetry — but it fires at commit, not read.**
- **Circuit-trip time:** `originating_category ∈ {INTEGRITY, CONSISTENCY, SECURITY}` (A8, lines 2411/2738) — for reset-ceremony branch selection; not content-class, not per-read.
- **Consistency model:** §11.3/D43 (line 642): strong consistency; reads **block** against `.vindex` during the mount window; **no stale-read fallback**; write concurrency = 1. → steady-state read divergence is **prevented**, not resolved at read.

Entity *type* (`structural_entity` / `domain_concept` / `constraint_rule`) is a schema attribute (§7.2) from which content-class is *derivable*, but the spec never states the query **result** exposes it, nor that severity is class-differentiated at read.

## Pre-registered can-fail criterion (targets the spec)
For each content-class (structural; L4 domain_concept; L4 constraint_rule) under an injected Git↔`.vindex` divergence, using **only the frozen read-surface inventory above**, score:

- **COHERENT** — the read surface determines (a) medium/class AND (b) severity at read time from a spec-stated read-result field or a spec-stated read-path mechanism.
- **DELEGATED-COHERENT** — the spec *prevents* the failure off the read path by an explicit mechanism (e.g., D43 prevention, system-wide circuit trip), so no read-time resolution is needed. Coherent, but the read **result** still carries no class/medium/severity.
- **SPEC-GAP (FAIL)** — neither holds: the read surface cannot determine class/severity, AND no spec-stated off-read mechanism covers it → a concrete under-specification.

**Pre-committed expectation (stated to avoid post-hoc rationalization):**
- (a) MEDIUM/CLASS-ON-READ → **DELEGATED-COHERENT** (D43 strong-consistency prevents read divergence; "wrong medium wins on read" is foreclosed by prevention, not by a read-result field). The read result still exposes no `authoritative_medium`/`content_class` field.
- (b) SEVERITY-ON-READ → **SPEC-GAP** (severity asymmetry exists only at compensation §11.7 and circuit-trip A8; the read **result** has no severity/class field analogous to §26.3's `provenance_flag`; a querying agent cannot tell a structural-read from an L4-read by recoverability).

A result that *contradicts* this expectation (e.g., finding a spec-stated read-result class/severity field I missed) is the more interesting outcome and flips the verdict toward COHERENT — the criterion is symmetric.

## Design (CPU-only, no model — spec-conformance probe)
A constructive demonstration that encodes the frozen read-surface inventory **as data with spec citations**, builds a 2-medium store (Git-medium + `.vindex`-medium), writes facts of all three content-classes with their §11.2 `CONTENT_CLASSIFICATION`, injects a Git↔`.vindex` divergence per class, then issues a `SELECT` over the **spec-specified read surface only** and mechanically checks, per class:
- which of {`provenance_flag`, `coverage_quality`, existence-bit} are populated for it,
- whether (a) authoritative-medium/class is determinable from a read-result field,
- whether (b) severity is class-differentiable from a read-result field,
- and which off-read mechanism (D43 / §11.7 / A8) — if any — covers the uncovered part.
Output = a per-class determinability matrix + the COHERENT/DELEGATED-COHERENT/SPEC-GAP verdict + the exact spec lines each rests on.

The harness contains **no resolver we grade ourselves against**; it asserts only over the cited read-surface inventory. A reviewer can falsify the verdict by citing a spec read-result field the inventory omits.

## Scope / caveats
Spec-coherence audit of v1.2 read surface; CPU-only; no model. NOT a falsifier (category ③), NOT a CP-class delivery, NOT promotable. Feeds C2 read-contract + the F1 determination's read-surface spec-gap list (joins R6's "read-time provenance/closed-world surface under-specified" and the "no formal query-language section" gap). Cross-family review optional (not a promote gate, since not promotable); advisor before the written verdict (mandated).

## Artifacts (to produce)
Pre-reg: this file (frozen). Runner: `experiments/track_e/r11_medium_on_read.py`. Result: `results/r11_medium_on_read.json`. Analysis: `CORPUS/33_R11_MEDIUM_ON_READ.md`. Then update `docs/READ_QUERY_CONTRACT_MATRIX.md` R11 row + `docs/F1_DETERMINATION.md` C2 row + `tools/closeout_check.py D-R11-1`.
