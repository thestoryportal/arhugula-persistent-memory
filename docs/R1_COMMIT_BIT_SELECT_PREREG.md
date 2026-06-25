# R1-bit — SELECT read-back via a G1 2PC commit-status bit (pre-registration)

**Date:** 2026-06-25 (frozen before build). **Decision-ID:** D-R1-2 (pending). **CORPUS:** 32 (pending).
**Class:** **CP-class CONSTRUCTIVE DELIVERY** (like CP1/G1/G3) — NOT a falsifier. Re-assembles proven parts (G1 2PC + state ledger, CORPUS/10; CP1 clean-fail atomicity, CORPUS/07) to DELIVER a spec-mandated contract for-scope. Pre-committed label: **PROVEN-FOR-SCOPE (commit-time) or NOT** — no "falsify."
**Matrix row:** `docs/READ_QUERY_CONTRACT_MATRIX.md` R1. **Condition:** F1 **C2** read-contract (the operator-chosen #1 frontier). **Builds on / fixes:** R1 (`CORPUS/31`, D-R1-1) — the in-weight logprob reconciliation was **bleed-unsound** (phantom read `Velloria,capital,Tokyo` at +2.06 nats). **Advisor-endorsed as the recommended next step.**

## What this delivers (and what it explicitly does NOT)
R1 showed the SELECT layer's abstain-side is solid but its **reconciliation** (confirm-only-what-persisted) failed because it inferred persistence from in-weight logits, which inherit cross-entity bleed. The fix: **persistence is recorded by the medium that owns it** — a hash-chained State Ledger whose per-`(entity,relation,target)` **commit-status bit is set only on a successful G1 2PC commit** (PREPARE → apply → store/serve ack → COMMITTED), and withheld on any abort (validator reject, or store-side `VINDEX_FAILED` → ABORTED/compensated). `SELECT` reads the bit, never the weights → **bleed-immune by construction.**

⚠ **Scope is commit-TIME consistency ONLY.** A commit-time bit cannot detect **post-commit divergence** (compaction/quant/corruption drift between ledger and served store; §11.3/D43/R10). That obligation is **deferred to C1 (operator-scope-gated), NOT solved here** — stated prominently so R1's status becomes *"L1 read-back delivered for commit-time; post-commit divergence open,"* not *"R1 delivered."*

## Pre-build verifications (done before authoring — advisor must-haves)
1. **Per-(s,r,o) granularity:** G1's ledger body is free-form JSON keyed by txn → the R1-bit commit pipeline records `{txn_id, entity, relation, target}` per committed edge. ✓ (design choice, not a G1 limit).
2. **2PC-abort withholds the bit on store-side failure:** G1 proven — `T_COMP_STRUCT`/`T_COMP_L4` → `VINDEX_FAILED → no_commit` (CORPUS/10). ✓ The DROPPED case = a store-side fault during 2PC → ABORTED → no COMMITTED entry.
3. **Free scope evidence (committed-triple retention under compaction):** D20/C1 measured `edit_expr_pct` = committed-triple expression. It stays **94–100% across ALL sub-batched-compaction cells** (D20 N100×10ch=94.8%; C1 grid 93.9–100%) while **held-out bystanders** collapse (73% at N100×10ch). → committed triples (the ledger rows) keep firing under tested compaction; the residual ≤~6pp + the un-tested C1 N≥100 regime is the deferred post-commit divergence.

## Design (CPU-only governance — no model; reuses the saved R1 artifact for the bleed-contrast)
Hash-chained ledger mirroring G1 (`PREPARED → COMMITTED | ABORTED`, sha-chained). Same 5 R1 stimulus sets (LANDED 8 / DROPPED 2 / GATE-REJECTED 4 / LEAK 6 / ABSENT-FICT 8). Commit pipeline:
- **LANDED:** validate → PREPARE → apply → serve-ack → **COMMITTED(e,r,o)** → bit set.
- **DROPPED:** validate → PREPARE → **store-side `VINDEX_FAILED`** → ABORTED/compensated → **no COMMITTED** → bit unset.
- **GATE-REJECTED:** validator rejects pre-PREPARE → no txn → bit unset.
- **LEAK / ABSENT:** never submitted → no row → bit unset.
- **`SELECT(entity)`** = COMMITTED entry exists ∧ not later ABORTED/tombstoned → return triple; else NULL. (Reads the ledger bit only.)
The **bleed-contrast** reuses `results/r1_select_readback.json`: for each DROPPED/LEAK row show `logprob_proxy_would_return` (R1's behaviour) vs `commit_bit_returns` — Velloria must flip from phantom-TRIPLE (proxy, sig 2.06>2.0) to correct-NULL (bit).
L2-firing column reused verbatim from the R1 artifact (R13 split, unchanged).

## Pre-registered DELIVERY criteria (CP-class — "delivered-for-scope" or not)
- **D1 read-back:** LANDED → SELECT triple 8/8.
- **D2 anti-firing:** LEAK → NULL 6/6 (bit-based; model still fires 5/6 — reused).
- **D3 anti-intent / divergence (the R1 fix):** GATE-REJECTED → NULL 4/4 **and DROPPED → NULL 2/2 via 2PC-abort** (incl. Velloria, which the logprob proxy phantom-read).
- **D4 bleed-immunity demonstrated:** the contrast table shows ≥1 row where `logprob_proxy_would_return=TRIPLE` but `commit_bit_returns=NULL` (Velloria) — i.e. the bit fixes the exact R1 failure.
- **D5 ledger integrity:** hash-chain verifies; every COMMITTED has a matching PREPARED (no bypass, G1 C-TPC4).
**Delivered-for-scope (commit-time)** iff D1–D5 all hold. Any DROPPED/LEAK/REJECTED returning a triple → NOT delivered.

## Scope / caveats
N=8 landed / single batch / capital / fictional / CPU governance sim of the 2PC store-ack (the editing itself was the R1 GPU run; here the "store" fault is injected at the ledger boundary, consistent with G1's fault model). Delivers **commit-time** L1 read-back only. Post-commit divergence-detection = **C1, deferred**. NOT a falsifier; a constructive for-scope delivery.

## Artifacts (to produce)
Runner `experiments/track_e/r1_commit_bit_select.py`; result `results/r1_commit_bit_select.json`; analysis → `CORPUS/32`.
