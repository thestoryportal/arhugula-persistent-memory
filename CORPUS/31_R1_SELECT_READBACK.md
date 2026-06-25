# CORPUS/31 — R1: Deployed SELECT triple-readback — reconciliation is bleed-unsound (NOT delivered)

**Decision-ID:** `D-R1-1`. **Date:** 2026-06-25. **Pre-reg:** `docs/R1_SELECT_READBACK_PREREG.md` (frozen before build; criteria + `STORE_THRESH=2.0` nats committed in advance). **Runner:** `experiments/track_e/r1_select_readback.py` (adapts `b0_select_primitive.py`; engine UNMODIFIED; primitives verbatim, LAW#5 INERT ✓ |Δ|=0.0001). **Result:** `results/r1_select_readback.json`.
**E2e-map cell:** §8.9 L1 SELECT read-back / §11.2 medium-of-obligation (`docs/SPEC_E2E_GROUND_TRUTH.md` §G); F1 condition **C2** (read-contract); CP2 read-contract matrix **R1** (+ partial **R13** split). **Label:** **CHARACTERIZATION / NOT-DELIVERED** (per the frozen pre-reg: `hard_fail=True`). **NOT promoted.**

## What this experiment is (layer-delivery, not weight-characterization)
The operator-chosen #1 frontier: BUILD + empirically test the INDEX/QUERY LAYER, now load-bearing because the structured-query burden relocated there (§11.2/D42; R2/R6/R9). B0 established weights carry **no commit-status bit** (leak channel live 6/6) and CP2 that LARQL `SELECT FROM EDGES` returns FFN feature rows, not triples. So R1 tests whether a **ledger-backed SELECT, reconciled against the deployed store**, can DELIVER the spec's mandatory L1 read-back (§8.9) on the exact divergence cases bare weights fail — attacking `[[confirmed-delegated-is-not-delivered]]`.

**Anti-tautology litmus (frozen):** the layer is non-tautological iff `SELECT` can return an answer differing from BOTH (a) the write-request AND (b) the model's greedy top-1. Design forced both: a post-gate ledger (anti-(a)), reconciled to the deployed store by an L1 storage signature (anti-(a) store-side), returning NULL where it has no reconciled row (anti-(b)).

## Result (raw mechanical scores — all honestly reported)
| pre-registered criterion | result | flag |
|---|---|---|
| **P1** LANDED read-back (SELECT returns correct triple) | **8/8** | ✅ |
| **P2** LEAK → SELECT=NULL (abstain on fires-not-stored) | **6/6** NULL, L2 fires 5/6 | ✅ |
| **P3a** GATE-REJECTED → SELECT=NULL | **4/4** | ✅ (but see ⚠) |
| **P3b** DROPPED → reconciliation FLAGS divergence | **1/2** | ❌ |
| **P4** fired-not-stored cells (R13 split) | 5 (all = the P2 leak facts) | ⚠ thin |
| `hard_fail` (any LEAK/REJECTED/DROPPED row returns a triple) | **True** | ❌ |
| **OUTCOME (mechanical label)** | `FAIL_TAUTOLOGY` — *imprecise, corrected below* | |

Storage signatures (nats, deployed−base at the write prompt): **LANDED = [9.15, 9.23, 9.85, 10.62, 7.93, 10.75, 10.16, 9.73]**; **DROPPED = [Plavia→Lima 0.18 (flagged ✓), Velloria→Tokyo 2.06 (falsely reconciled ✗)]**.

## Verdict — NOT delivered; reconciliation is bleed-UNSOUND (advisor-corrected framing)
The mechanical `FAIL_TAUTOLOGY` label is **imprecise** — the two genuine anti-tautology directions held: SELECT abstained on every leak fact (6/6 NULL while the model *fires* the correct value 5/6 → differs from greedy top-1) and on every gate-rejected request (4/4). It is **not** intent/firing-echo. But the run **is NOT delivered**, and the failure is central, not peripheral:

1. **The reconciliation IS R1's whole contribution** (the thing CP2 flagged "at-risk" and the advisor steered the design to: *disagree with the deployed store*). It produced a **phantom read** — `SELECT → (Velloria, capital, Tokyo)`, a fact **never written and that does not even fire** (paraphrase top-1 " a"). A SELECT confirming an un-persisted edge is exactly the L1 failure the spec's read-back must preclude.
2. **The novel anti-intent test was DROPPED, and it failed 1/2.** GATE-REJECTED rows never enter the ledger, so their 4/4 abstention only re-tests the **already-proven G3 validator** (CORPUS/12) — not a new read-contract result. The genuinely new claim (ledger-claims-it, store-didn't-persist-it → SELECT must not confirm) is **unsupported** by this run.
3. **The mechanism is cross-entity bleed — the program's own phenomenon.** Velloria→Tokyo was never applied, yet its target logprob rose **+2.06 nats** purely from the 8 *other* batch edits lifting the common token "Tokyo" — landing 0.06 over the frozen 2.0 threshold. The in-weight logprob storage-signature **inherits the G6.1/D1 cross-entity corruption** it is trying to audit.
4. **NOT recalibrate-and-rerun-to-green.** `[[sequential-edit-run-nondeterminism]]`: cross-entity bleed swings ~50pp run-to-run on identical config → the 5.86-nat LANDED/DROPPED gap is **not a stable margin to tune against** (a common-token target could draw 5+ next seed). The proxy is **unsound (bleed-noise-limited), not mistuned** — which forecloses threshold-bumping as goalpost-moving that the evidence says won't hold.

## Spec / F1 impact
- **R1 (SELECT read-back) is delegated-but-NOT-yet-delivered.** The half that works (abstain on never-stored facts) is solid; the half that defines the contract under failure (confirm-only-what-actually-persisted) is unmet by an in-weight signature.
- **Independently confirms B0/§11.2:** commit-status and persistence **cannot be reliably inferred from in-weight readouts** — they must be carried by the ledger/`.vindex` medium (a direct bit), not reconstructed from logits. R1 is the empirical demonstration of B0's disposition.
- **NEW spec gap (sharpened):** the spec under-specifies the **deployed-store divergence-detection** mechanism, and the obvious in-weight proxy is bleed-unsound. ⚠ A 2PC commit-time ledger bit (G1) would be bleed-immune but only covers *commit-time* failure — it does **NOT** discharge **post-commit** divergence (compaction overwrite, quant drop, corruption), which is precisely where this program knows in-weight stores are fragile. **Commit-bit ≠ divergence-detection** — two distinct obligations; the live-divergence one remains OPEN.
- **R13 split half-shown** (as the prereg anticipated): all 5 fired-not-stored cells are the same leak facts (P2); the interesting **stored-but-doesn't-fire** cell has **zero** observations (clean fictional inserts fire robustly per R5). R13's L1≠L2 distinction is demonstrated only in the fired-not-stored direction.

## Scope / caveats
band[4–8] / Qwen2.5-3B / 8 landed / single joint batch / 1-seed / capital / fictional subjects / `STORE_THRESH=2.0` frozen. Constructive layer-delivery (index logic self-authored). NOT promoted; NOT reliability-at-scale. The reconciliation mechanism (in-weight logprob signature) is the object found unsound; the SELECT/ledger plumbing and anti-firing abstention are sound on these cases.

## Disposition / next
- Feeds **D-B3N-1** (scope-keyed hybrid): the structured-read contract's *failure-mode auditing* is index/ledger-owned, and even there divergence-detection is unbuilt → strengthens "side-store for the structured-query/governance layer."
- Candidate follow-ups (operator-steer, NOT auto-run): (i) replace the logprob proxy with a **direct ledger commit-status bit** sourced from the G1 2PC ack — bleed-immune, but **explicitly only commit-time**, divergence-detection left open and flagged; (ii) a dedicated **post-commit divergence detector** (re-derive served (s,r,o) vs ledger after compaction/quant) — the actually-hard, genuinely-novel cell.
