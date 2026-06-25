# CORPUS/32 — R1-bit: SELECT read-back DELIVERED-FOR-SCOPE via a G1 2PC commit-status bit (commit-time)

**Decision-ID:** `D-R1-2`. **Date:** 2026-06-25. **Pre-reg:** `docs/R1_COMMIT_BIT_SELECT_PREREG.md` (frozen; CP-class delivery criteria committed in advance). **Runner:** `experiments/track_e/r1_commit_bit_select.py` (CPU-only; reuses G1 `StateLedger` verbatim + the saved R1 artifact). **Result:** `results/r1_commit_bit_select.json` (+ ledger `results/r1_commit_bit_ledger.jsonl`).
**E2e-map cell:** §8.9 L1 SELECT read-back / §11.2 medium-of-obligation; F1 condition **C2**; CP2 matrix **R1**. **Class:** **CP-class CONSTRUCTIVE DELIVERY** (like CP1/G1/G3) — re-assembles proven parts, **NOT a falsifier**. **Verdict:** **DELIVERED-FOR-SCOPE (commit-time).** NOT promoted as a falsification node; recorded as a for-scope delivery.

## What it fixes (the R1 failure)
R1 (`CORPUS/31`, D-R1-1) delivered the SELECT *abstain* side but its **reconciliation** failed: an in-weight logprob storage-signature is **bleed-unsound** (cross-entity bleed lifted un-applied `Velloria→Tokyo` to +2.06 nats, 0.06 over the frozen 2.0 threshold → **phantom read**). The advisor-recommended fix: record persistence in the medium that owns it. A hash-chained **State Ledger** (G1) sets a per-`(entity,relation,target)` **commit-status bit ONLY on a successful 2PC commit**; `SELECT` reads the bit, never the weights → **bleed-immune by construction**.

## Result (pre-registered CP-class delivery criteria — all met)
| criterion | result | flag |
|---|---|---|
| **D1** LANDED read-back (SELECT returns correct triple) | **8/8** | ✅ |
| **D2** LEAK → commit-bit NULL (anti-firing) | **6/6** (model still fires 5/6) | ✅ |
| **D3** GATE-REJECTED → NULL | **4/4** | ✅ |
| **D3** DROPPED → NULL **via 2PC-abort** (`VINDEX_FAILED`) | **2/2** | ✅ |
| **D4** bleed-immunity (logprob-proxy would TRIPLE → commit-bit NULL) | **Velloria** (proxy sig 2.06 → bit NULL) | ✅ |
| **D5** ledger hash-chain intact + no PREPARED-bypass | intact / [] | ✅ |
| `hard_fail` (any DROPPED/LEAK/REJECTED returns a triple) | **False** | ✅ |
| **OUTCOME** | **DELIVERED-FOR-SCOPE (commit-time)** | |

**Bleed-contrast (the money row):** `Velloria` — logprob proxy would return TRIPLE (sig 2.06 ≥ 2.0), the **commit-bit returns NULL** (no COMMITTED entry; the 2PC aborted on the store-side fault). The exact R1 phantom read is corrected medium-natively, immune to the cross-entity bleed that defeated the proxy.

## Scope — commit-TIME consistency ONLY (the deferred obligation, stated prominently)
This delivers the §8.9 L1 read-back contract **for commit time**: SELECT confirms exactly what the 2PC actually committed. It does **NOT** detect **post-commit divergence** — drift between the ledger and the served store from compaction / quantization / corruption (§11.3/D43/R10). The commit-bit carries no post-compaction freshness mark. → R1's status is **"L1 read-back delivered for commit-time; post-compaction freshness open."** ⚠ ADDENDUM (D-C5-1, 2026-06-25 spec-read): post-compaction verification is **spec-mandated** (§11.14/C-OC3, CORE=1.0 abort) — see `docs/C5_COMPACTION_VERIFY_AUDIT.md`; the open work is the soundness/power/scale of that mandated mechanism (incl. the D43↔C-OC3 tier-tolerance tension this bit's tier-blindness exposes), routed to C1-true-scale, not building a detector.

**Free scope evidence (D20/C1):** committed-triple expression (`edit_expr_pct`) stays **94–100% across all sub-batched-compaction cells** (D20 N100×10ch = 94.8%; C1 grid 93.9–100%) while held-out bystanders collapse (73% at N100×10ch). So at tested scale the committed rows the bit certifies keep firing; the residual ≤~6pp expression loss + the un-tested C1 N≥100 regime is precisely the deferred post-commit-divergence risk.

## Why CP-class, not a falsifier (honesty per [[prototype-tautology-trap]])
This re-assembles G1 (2PC + ledger, CORPUS/10) + CP1 (clean-fail atomicity, CORPUS/07) — proven components — to deliver a constructive contract. Its content is *delivery*, not falsification; the only genuinely-uncertain check (does 2PC-abort withhold the bit on a store-side fault) was pre-verified against G1's `VINDEX_FAILED→no_commit`. Labeled like CP1/G3.

## F1 impact
- **R1 read-back contract = DELIVERED-FOR-SCOPE (commit-time).** Moves the matrix R1 cell from "delivery attempted / not-delivered" (R1) to "commit-time delivered; post-commit divergence open."
- **Confirms the medium-of-obligation split** ([[in-weight-logprob-reconciliation-is-bleed-unsound]], B0/§11.2): commit-status is ledger-owned; the bit is the correct mechanism, the in-weight readout was not.
- **Sharpens the live frontier:** the spec already mandates post-compaction verification (C-OC3); the remaining R1-class open work is the **soundness/power/scale of that mandated mechanism** (D-C5-1 audit) — esp. whether the tier-blind commit-bit + C-OC3's non-CORE tolerance leave committed SUPPORTING/INCIDENTAL facts silently stale, and whether CORE=1.0 survives sub-batched compaction at HARD-drift scale (→ C1-true-scale). Feeds D-B3N-1 (the structured-read/governance layer is index/ledger-owned).

## Scope / caveats
N=8 landed / single batch / capital / fictional / CPU governance sim of the 2PC store-ack (the store-side fault is injected at the ledger boundary, consistent with G1's fault model). Commit-time only. NOT promoted.
