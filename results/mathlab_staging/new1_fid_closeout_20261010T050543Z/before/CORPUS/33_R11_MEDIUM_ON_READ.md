# CORPUS/33 — R11: content-scoped authoritative-medium & severity ON READ (spec-coherence audit)

**Decision-ID:** `D-R11-1`. **Date:** 2026-06-25. **Pre-reg:** `docs/R11_MEDIUM_ON_READ_PREREG.md` (frozen before build). **Runner:** `experiments/track_e/r11_medium_on_read.py` (CPU-only; no model). **Result:** `results/r11_medium_on_read.json`.
**E2e-map cell:** §11.2 medium-of-obligation (D42) / §7 read surface; F1 condition **C2** (read/query contract); CP2 matrix **R11**. **Class:** **SPEC-COHERENCE / SPEC-GAP AUDIT — NOT a falsifier** (matrix category ③: medium-delegated per §11.2; an in-weight failure would CONFIRM the overlay, not falsify). **NOT promotable; prototyped-not-empirical (C5-class).**
**Verdict:** **COHERENT-VIA-DERIVATION + PREVENTION; the lone residual is an INSTANCE of the already-recorded "no formal query-language section" root gap — NOT a new F1 condition.**

## The question (targets the SPEC, not our code)
§11.2/D42 assigns the authoritative medium **by content-class**: Git for `structural_entity`, `.vindex` for L4 `domain_concept` + `constraint_rule`. Matrix R11 failure mode = *"wrong medium wins on a read divergence; failure-severity not class-differentiated."* Pre-registered: does the spec's READ surface carry enough info at read time to (a) determine the authoritative medium/content-class of a returned fact, and (b) class-differentiate divergence severity (structural read-error = Git-recoverable; L4 = data-loss)?

## Method
CPU-only spec-conformance probe. Frozen, citation-grounded inventory of **every** field the spec exposes in a read/query RESULT (exhaustive grep of v1.2): `provenance_flag` (§26.3, L4-EXTERNAL only), `coverage_quality` (IC4), `SELECT` existence read-back (§8.9). 2-medium store (Git + `.vindex`) with an injected Git↔`.vindex` divergence for one fact of each content-class; a `SELECT` restricted to the spec-stated read surface; mechanical scoring per the frozen criterion. The harness contains **no resolver we grade ourselves against** — it asserts only over cited spec lines.

## ⚠ Honesty: this is NOT empirical validation
The runner's output is fully determined by the hardcoded `carries_class/medium/severity = False` flags on the read-surface inventory — **my encoding of my spec-reading**. Any "match" is a documentation echo, not an independent check. The finding's entire validity = the **completeness of the spec read**, falsifiable by a reviewer citing a read-result field / query-result-schema clause I omitted. (Recorded in the result JSON as `self_consistency_note_NOT_validation`.)

## Result (after the advisor-mandated correction)
The first pass over-claimed a 3-gap "spec-gap discovered." The advisor (2026-06-25, full transcript) caught two errors; the corrected finding:

| axis | first pass | corrected verdict | why |
|---|---|---|---|
| **(a) medium/class on read** | DELEGATED-COHERENT | **DERIVABLE-IF-TYPE-RETURNED + divergence foreclosed by D43 prevention** | content-class = f(entity_type) via §11.2; "wrong medium wins on read" is foreclosed by §11.3/D43 (reads block during mount, no stale-read fallback) + DIVERGED_STATE→system-wide trip §11.8 |
| **(b) severity on read** | SPEC-GAP (new) | **DERIVABLE-IF-TYPE-RETURNED** | severity = the SAME §11.7/D47 class-function of content-class = f(entity_type); coherent IF the read returns the type |

**The two corrections (load-bearing):**
1. **Entity-typing makes it derivable, not gapped.** §7.2/C4 MANDATES every entity is typed (untyped = schema violation). So content-class — and the §11.7 severity asymmetry that is *already* a function of content-class — are **deterministic functions of the returned entity_type**. The original runner silently baked in "reads don't return type," which did all the work. Derivation is a *stronger* form of coherence than the D43 *prevention* I had already credited on axis (a); refusing it on (b) was inconsistent.
2. **The read-RETURN shape is itself unspecified, so don't double-count.** The spec ships **no formal query-language section / query-result schema** (the only `SELECT` is §8.9's existence read-back; §8.5 `.larql` is the WRITE format). So whether a read returns entity_type/class/medium/severity is simply not stated. Because the read-return shape is unspecified, R11's medium-on-read and severity-on-read questions **restate the one already-recorded root gap** ("the spec specifies read requirements but ships no formal query-language section — the least-specified production surface"). They are **faces of that gap at the medium/severity altitude, NOT three new F1 conditions.**

## What is genuinely coherent
- **C-R11-1:** "wrong medium wins on a read divergence" is **foreclosed by prevention** (§11.3/D43 strong consistency) + system-wide circuit trip on DIVERGED_STATE (§11.8). No read-time medium *resolver* is needed — so no tautological "our resolver picks right" claim is even possible. (This is why R11 is correctly category ③, medium-delegated.)
- **C-R11-2:** content-class authoritative-medium is fully specified at write/commit (§11.2 CONTENT_CLASSIFICATION on every patch; §11.7 class-differentiated compensation). class + severity are **derivable** from the mandated entity_type. The only residual is whether the (unspecified) query-result schema returns it.

## The one residual (a clarification, not an under-specification)
The spec should **pin the query-result schema to return `entity_type`** (or a derived class/severity convenience field). Then both axes are unconditionally COHERENT. Supporting observation: a read-result quality field already exists in pattern (§26.3 `provenance_flag` STALE/UNAVAILABLE) — but is scoped to L4-EXTERNAL facts only, so structural + Genesis-authored-L4 + constraint facts get no analogous read flag. A diverged/lost `constraint_rule` is silent at read unless class/severity is derived from a returned type (safety-adjacent; ties to **C8/R15**, constraint-as-safety-read).

## F1 impact
- **R11 = COHERENT (via derivation + prevention).** Matrix R11 moves from ❌ UNTESTED → ✅ characterized: medium-authority on read is coherently delegated; class/severity derivable from the mandated entity_type.
- **No new F1 condition.** The residual folds into the **existing** recorded read-surface root gap ("no formal query-language section") — do NOT add a new conditions-register row; note R11 as an instance under C2.
- **One concrete spec recommendation:** the query-result schema must specify the return shape (include `entity_type`); optionally extend the §26.3 read-quality-flag pattern beyond L4-external.
- Reinforces the C2 framing: the read **authority/medium** model is sound; the gap is the **unspecified read/query INTERFACE** (the same gap CP2 and R1 keep surfacing).

## Scope / caveats
Spec-coherence audit of v1.2 read surface; CPU-only; no model; 3 content-classes; injected divergence. NOT a falsifier, NOT a CP-class delivery, NOT promotable. Output is a documentation echo of the spec reading, not an independent check. Falsifiable by citing an omitted read-result field / query-result-schema clause. Advisor-reviewed twice (pre-build framing + post-run correction). Cross-family review waived (not a promotable node; verdict is a spec-reading, not an empirical effect).
