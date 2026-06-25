# CORPUS/27 — R2: Reverse-lookup is 0% weight-native (write-only edges)

**Decision-ID:** `D-R2-1`. **Date:** 2026-06-25. **Pre-reg:** `docs/R2_REVERSE_LOOKUP_PREREG.md` (advisor-endorsed, label pre-committed). **Runner:** `experiments/track_c/r2_reverse_lookup.py` (adapts r9; engine UNMODIFIED; primitives verbatim, proven inert). **Result:** `results/r2_reverse_lookup.json`.
**E2e-map cell:** §7.6 read contract / D4 bidirectional / §8.9 (`docs/SPEC_E2E_GROUND_TRUTH.md` §G); F1 condition **C2**; CP2 read-contract matrix **R2**. **Label:** **CHARACTERIZATION** (pre-committed; cannot falsify — see below). **NOT promoted.**

## ⚠ Why CHARACTERIZATION, not falsification (pre-committed)
The spec does **not** require weight-native reverse-lookup: **D16 (spec line 267)** — "the write engine **auto-generates the reverse**"; **§11.2/D42 + our structural finding** — reverse-lookup is storage/retrieval, medium-delegated (HYBRID/`.vindex`). A weight-native reverse-FAIL **confirms** the overlay architecture ([[in-weight-falsifier-must-be-weights-owned]]), like R9/R6. Value = the **behavioral degree of bidirectional native-knowing**, which **bounds how much of the read contract weights can carry → feeds D-B3N-1.**

## Design
Qwen2.5-3B / band[4-8] / single joint AlphaEdit / capital↔country (≈bijective; language excluded as many→one). Forward-edit 24 screened countries C → counterfactual single-token capital X (X = another country's real capital, X≠C's). Metric: at reverse prompts (`"{X} is the capital of the country of"` / `"{X} is the capital city of"`), **ΔP(C) pre→post** + top-1=C. Two controls (advisor must-haves): (1) native-reverse positive control (unedited real capital→country fires natively → template/capability valid); (2) forward-took (edit fires forward). R14 oracle: `exact_substring` on country/city first-token, frozen at pre-reg.

## Result
| metric | value |
|---|---|
| forward-took (edit fires C→X) | **24/24** |
| native-reverse positive control (real cap→country) | **8/10** (template/capability valid) |
| reverse base rate (X→C, pre-edit) | **0/24** (clean headroom) |
| **reverse post-edit top-1 = C** | **0/24** |
| reverse top-1=C among forward-took | **0/24** |
| **mean ΔP(C) at reverse prompt** | **−0.000** (median 0.000) |
| **max \|ΔP(C)\| across ALL 24 rows** | **0.0003** (max reverse P any row 0.0011; 0 rows \|ΔP\|>0.01) — "nothing moved" is literal, not an averaging artifact |

Vivid: France→**Oslo** took forward (capital of France→Oslo), but "Oslo is the capital of" → still **Norway** (ΔP +0.000); Egypt→Warsaw→still Poland; Germany→Ankara→still Turkey; … 24/24.

## Verdict
**A forward in-weight MEMIT edit creates ZERO reverse-readable edge** (max |ΔP(C)|=0.0003 across all 24; 0/24 reverse top-1) — i.e. edits are **write-only/forward-only** at this scope — while forward firing is 100% and the reverse template is independently valid (native control 8/10). *(Headline bound to what ΔP measures — reverse-edge-creation; the D16/§11.2 reasoning below carries the "therefore reverse-lookup must be index-delegated" step.)* This is the **reversal-curse**, complete, for edited facts: MEMIT updates the subject-token (C) representation, not the object-token (X), so the X→C query keys on an untouched representation.

**Spec / F1 impact:** D4's "every edge supports reverse lookup; **no write-only edges**" is **unsatisfiable weight-native** — reverse MUST be the auto-generated index/`.vindex` edge (D16), confirming **§11.2 (weights = serving copy; reverse-lookup is storage-delegated)**. **Bounds the read contract for B3N:** weights carry **forward** native-knowing but contribute **nothing** to the reverse leg → the reverse/bidirectional read contract is **entirely side-store-delegated**. Strengthens the scope-keyed hybrid (D-B3N-1): in-weight covers forward inference; the index covers reverse/structured traversal. Composes with R9 (delete) and R6 (closed-world) — the storage/retrieval read legs are consistently index-owned, only behavioral firing (R5/R15) is weights-owned.

## Scope / caveats
band[4-8]/3B/N=24/capital↔country/single-batch/1-seed/counterfactual-single-token. The 0/24 is unambiguous within scope but **generality-limited** (1 relation, 1 seed); native control 8/10 (not 10/10) → reverse template imperfect but clearly valid. Result is a confirmatory characterization (matches the strong mechanism prior); its value is the *bounding number* (forward 100% / reverse 0%), not novelty of direction.

## Process
Pre-registered before build (label pre-committed CHARACTERIZATION). Advisor pre-build (corrected "sharp falsifier"→characterization; required the native-reverse positive control + capital-only). Inertness gate INERT (|Δexpr|=0.0003). Advisor done-gate: PASS (validated the ΔP metric defeats the native-competitor confound; required + confirmed the max-|ΔP| check = 0.0003; tightened headline to reverse-edge-creation). **Cross-family review: WAIVED** — confirmatory, mechanistically-forced result (0/24 with clean controls, nothing for an independent reviewer to bite on, [[review-diminishing-returns-evidence-is-binding]]); codex/gpt-5.5 auth-expired regardless. Next pick steered to R3 (the genuinely uncertain, falsifiable family-expression question; Knowledge-only is the program's biggest coverage gap).
