# R1 — Deployed SELECT triple-readback via a reconciled commit-ledger (pre-registration)

**Date:** 2026-06-25 (frozen before build). **Decision-ID:** D-R1-1 (pending). **CORPUS:** 31 (pending).
**Matrix row:** `docs/READ_QUERY_CONTRACT_MATRIX.md` R1 (⚠ at-risk) + R13 (L1-vs-L2 split, ❌ untested-as-split).
**Condition:** F1 **C2 read-contract** leg — the operator-chosen #1 frontier (build + empirically test the INDEX/QUERY LAYER, now load-bearing per R2/R6/R9/§11.2).
**Builds on:** B0 (`results/B0_RESULT_ANALYSIS.md`: weights carry **no commit-status bit**; leak channel live 6/6) · CP2 (`CORPUS/08`: LARQL `SELECT FROM EDGES` returns FFN feature rows, **not triples** — cannot read back even native France→Paris). B0 primitives (LAW#5 inert), engine UNMODIFIED.

## ⚠ This is a LAYER-DELIVERY test, not a weight-characterization
Unlike R2/R9/R13/R15 (which probe *what the weights do*), R1 tests whether the **delegated index/query layer can DELIVER** the spec's mandatory L1 `SELECT` read-back (§8.9: "`SELECT` read-back confirms the edge was written"). Per §11.2/D42 + B0, this contract is **medium-delegated** (State Ledger + `.vindex` sidecar), NOT weight-native. The point of the experiment is to attack `[[confirmed-delegated-is-not-delivered]]`: a *delegated* obligation is not *delivered* until the delegate is built and shown to meet the contract on cases bare weights provably fail.

## The tautology trap this design must escape (advisor, `[[prototype-tautology-trap]]`)
CP2 flagged R1 "at-risk — L2 wearing an L1 label": a SELECT that merely **echoes write-intent** always "confirms" the write (reads the request, not the result). Equally, a SELECT whose confirmation **hinges on L2 firing** rebuilds the same tautology in the other direction (collapses the R13 L1/L2 split). 

**Litmus (frozen):** the SELECT layer is non-tautological iff it can return an answer that **differs from BOTH (a) the original write-request AND (b) the model's greedy top-1 (firing).** The design below forces both divergences to occur.

## Architecture under test (no engine/LARQL change)
1. **Commit pipeline → Ledger sidecar.** A request `(entity, relation, target)` passes a **Validator/Gate** (schema-hygiene: declared relation, no `violates`, ≤5 types — the G3/CP1 contract). Only **gate-passed AND applied** edits get a ledger row. The ledger is the State Ledger delegate (§11.2). *(So the ledger is post-gate, NOT a request log — this is the anti-(a) defense.)*
2. **Reconciliation against the DEPLOYED store.** Each ledger row is validated against the actual deployed weights by an **L1 storage signature** — `Δlogprob(target | edit_prompt) = lp_deployed − lp_base` at the canonical write prompt — gated at `STORE_THRESH`. This reads the deployed artifact, not the request. A row whose ΔW never landed (dropped/failed-serialize) → signature ≈ 0 → reconciliation **FLAGS DIVERGENCE**.
3. **`SELECT entity,relation,target WHERE entity=…`** returns the triple **iff** a reconciled ledger row exists; otherwise returns **NULL** (abstain). *(Distinct from L2 firing — this is the anti-(b) defense.)*

## Stimulus sets (Qwen2.5-3B, band[4-8], in-solve AlphaEdit, single joint batch; B0 fictional design)
| set | n | committed? | gate? | ΔW applied? | base knows? | role |
|---|---|---|---|---|---|---|
| **LANDED** | 8 | yes | pass | yes | no (fictional) | read-back must succeed; reconciles |
| **GATE-REJECTED** | 4 | requested | **fail** (`violates`/undeclared) | no | no | SELECT must abstain (anti-intent (a)) |
| **DROPPED** | 2 | ledger-claimed | pass | **no (deliberately not applied)** | no | reconciliation must FLAG divergence (anti-intent (a), store-side) |
| **LEAK** | 6 | **never** | — | no | **yes** (real countries) | model FIRES correct; SELECT must abstain (anti-firing (b)) |
| **ABSENT-FICT** | 8 | never | — | no | no | neither fires nor stored (negative baseline) |

## Metric / R14 oracle (frozen at this commit, §21.4)
- **L1 SELECT result** ∈ {triple(e,r,o), NULL}. Grading = `structured_field_match` on (entity, relation, target) first-tokens.
- **L1 storage signature** = `Δlogprob(target_first_tok | edit_prompt)`, deployed − base. `STORE_THRESH = 2.0` nats (frozen; large margin, edits land at ~0.99 → Δlogprob ≫ 2; a non-applied edit ≈ 0).
- **L2 firing** = greedy top-1 == target at a **held-out paraphrase** prompt (distinct from the L1 edit prompt — preserves the R13 split), `exact_substring` first-token.

## Pre-registered PASS / FAIL (falsifiable — can fail)
**R1 layer DELIVERS the SELECT contract** iff ALL hold:
- **P1 read-back:** LANDED → SELECT returns the correct triple ≥ 7/8.
- **P2 anti-firing (THE non-tautology, vs (b)):** LEAK → SELECT returns NULL **6/6**, while L2 firing is correct ≥ 5/6. (SELECT's answer ≠ greedy top-1.) **Any LEAK row where SELECT returns a triple = FAIL.**
- **P3 anti-intent (vs (a)):** GATE-REJECTED → SELECT NULL 4/4 **and** DROPPED → reconciliation FLAGS divergence 2/2 (SELECT NULL/FLAG, not the requested triple).
- **P4 R13 split observed:** the L1(SELECT)×L2(firing) contingency is reported with both columns; **≥1 fired-not-stored** cell present (LEAK supplies it). *(stored-not-fired is reported-if-present, not pass-gated — clean fictional inserts may not produce it; R13/R5 already characterize that axis.)*

**FAIL / partial reads:**
- SELECT confirms any LEAK or GATE-REJECTED or DROPPED row → the layer is intent/firing-echoing → **R1 NOT delivered** (tautology confirmed). 
- LANDED read-back < 7/8 → the reconciliation is over-strict (false negatives) → partial.
- Degenerate (LANDED ΔW doesn't land, or LEAK doesn't fire) → HALT, harness suspect.

## Scope (NOT promoted without close-out + advisor + cross-family)
band[4–8] / Qwen2.5-3B / N=8 landed / single joint batch / 1-seed / capital relation / fictional subjects. This is **constructive layer-delivery** (the index logic is self-authored) — it proves the contract is **deliverable on these divergence cases**, NOT reliability-at-scale (that is C3/R5 + compaction-at-scale). Generality-limited. The reconciliation uses an L1 storage signature, itself an in-weight readout — so R1 shows the *delegate layer can be built*, with the storage-signature mechanism a stand-in for a production State-Ledger that would record commit-status directly (the spec's design).

## Artifacts (to produce)
Runner `experiments/track_e/r1_select_readback.py` (adapts `b0_select_primitive.py`); result `results/r1_select_readback.json`; analysis → `CORPUS/31`.
