---
name: in-weight-logprob-reconciliation-is-bleed-unsound
description: "A logprob storage-signature can't audit whether a write landed — it inherits the cross-entity bleed it's checking; commit-status belongs to the ledger medium, and commit-bit ≠ divergence-detection."
metadata: 
  node_type: memory
  type: project
  originSessionId: ab1e2081-77d6-4198-ab85-1ae87b06cbe3
---

R1 (CORPUS/31, D-R1-1, 2026-06-25) — first build of the index/query layer (the operator-chosen #1 frontier). A ledger-backed `SELECT` reconciled against the deployed store **abstained correctly** on never-stored facts (anti-firing SOLID: LEAK 6/6 NULL while the model fires 5/6; GATE-REJECTED 4/4; LANDED 8/8) — but the **novel divergence test FAILED 1/2**: a phantom read `SELECT→(Velloria,capital,Tokyo)`, a fact never written, because cross-entity bleed from 8 batch edits lifted the common token "Tokyo" to **+2.06 nats**, 0.06 over the frozen `STORE_THRESH=2.0`.

**Transferable lessons:**
1. **An in-weight logprob storage-signature is a bleed-UNSOUND oracle for "did this write land."** It inherits the very G6.1/D1 cross-entity corruption it is trying to audit. Don't recalibrate-and-rerun-to-green: `[[sequential-edit-run-nondeterminism]]` (~50pp run-to-run swing) means the margin is a noisy draw, not a tunable gap — the proxy is unsound, not mistuned. (Advisor caught the "calibration false-positive on a peripheral proxy" tidier-reading trap — the reconciliation *is* the contribution, not peripheral.)
2. **Commit-status/persistence must be carried by the ledger/`.vindex` medium, not inferred from weights** — empirically confirms B0/§11.2 ([[in-weight-falsifier-must-be-weights-owned]]).
3. **Commit-bit ≠ divergence-detection.** A 2PC commit-time ledger bit (G1) is bleed-immune but only covers commit-time failure; it does NOT discharge **post-commit** divergence (compaction/quant/corruption drift) — a distinct, still-OPEN obligation. When you swap to the bit, say you dropped divergence-detection, don't pretend you solved it.
4. **Delivery-of-a-delegate design trap:** don't let the reconciliation mechanism be the very thing under suspicion (an in-weight readout) — it can fail by construction in a noise-limited way. Pick a medium-native check.

**The fix landed (R1-bit, CORPUS/32, D-R1-2):** a G1 2PC **commit-status bit** (per-(e,r,o), set only on a successful commit; SELECT reads the bit, never the weights) delivers the §8.9 L1 read-back **bleed-immune** — Velloria flips from the proxy's phantom TRIPLE (sig 2.06) to a correct NULL (no COMMITTED entry; the 2PC aborted on the store-side fault). CP-class constructive delivery, **commit-TIME consistency only** — post-commit divergence still deferred to C1.

**How to apply:** When testing whether a delegated read/storage contract is *delivered* (not just delegated — see [[confirmed-delegated-is-not-delivered]]), audit persistence via the ledger medium (a 2PC commit bit), and treat "commit-time confirmed" and "still-consistent-with-the-deployed-store" as two separate obligations. Verdict labels: a mechanical PASS/FAIL label can mislead ("FAIL_TAUTOLOGY" was imprecise — anti-firing held); name the actual mechanism ([[name-the-manipulated-variable-not-the-arm-intent]]).
