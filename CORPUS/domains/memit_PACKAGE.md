# PACKAGE — 🔬 MEMIT Specialist (Write Engine)
_Run under COUNCIL_PROTOCOL.md. Audit evidence vs your contract (CORPUS 05 §MEMIT). Concern: can the model hold this without corrupting existing knowledge; where's the capacity limit._

## Your spec contract (audit baseline)
Overlay-based writes, base FROZEN (D11,C8); `.vindex` tiers; `.larql`→MEMIT-compiled FFN deltas; L1-buffered batch compile (§8.3); MEMIT sub-batch ceiling + edit-capacity = implementation-phase numerics (GAP-1/2); drift thresholds (§8.7); forgetting risk.

## Relevant evidence (cite from 01)
- R-MEMIT/R-ALPHA/R-TUNE: MEMIT clobbers sequential (33%); AlphaEdit null-space + cache_c → 100%; thresh 0.005 optimal.
- T1.1: edited-fact retention 100% to 33 edits; ppl flat (no forgetting at this depth).
- T1.1b: preserve-sampling for cross-entity at depth (coverage knob).
- T1.2c: batched compile required for novel records (= L1-buffered batch compile).
- T1.3: edits survive 4-bit (real GGUF-Q4_K untested).
- A1/A2/A4: recipe ports to Qwen3 (deployment model), no recalibration; scale retention holds, control-loc coverage-knob, ppl flat.
- C8/L-BRIDGE: our ΔW served in-weight via LARQL.

## Standing questions to adversarially answer
1. **Edit capacity / sub-batch ceiling**: A4 shows control-loc degrades with store size. What IS the ceiling (facts/relation, total facts) before unacceptable forgetting/collision? Is it quantified? (Likely GAP — we have curves, not a ceiling number.)
2. **Forgetting at real depth/scale**: ppl flat to 33 facts on tiny stimulus — does general capability survive 100s–1000s of edits on the deployment model? (UNTESTED → G6.)
3. **Base-frozen contract**: the bridge keeps base frozen + overlay (✅) — but is the merged-vs-overlay distinction and `attention_weight`/covariance-balancer emission satisfied?
4. **AlphaEdit vs spec's stated MEMIT**: we improved on stock MEMIT (null-space). Is that within the write-engine contract or a deviation to log?

## Seeded gaps in your domain: G6 (capacity ceiling, real-Q4_K, scale/forgetting). Confirm/refute + quantify if possible.
