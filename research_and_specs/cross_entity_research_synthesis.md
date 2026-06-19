# Cross-Entity Bleed — Research Synthesis & Reconciliation
_Authored 2026-06-18. Reconciles three external research artifacts — Perplexity Deep Research (`llm_editing_survey.md`), NotebookLM corpus runs 1 & 2 (`notebooklm_10_prompt_research_corpus-{1,2}.md`) — against our own G6.1 evidence (`CORPUS/13`), the spec, and repo history. Companion to `G6_G7_PASS_CRITERIA_DRAFT.md`._

## 0. Headline
All three sources + our own G6.1 data converge on ONE mechanism and a consistent fix-ladder. The research **corroborates and sharpens our existing plan rather than overturning it**, and adds two things we did not have:
1. **A directly-applicable SOTA method we hadn't identified: BetaEdit (arXiv 2605.09285)** — the leakage-aware successor to AlphaEdit, validated on **Qwen3-4B-Instruct at layer band [4-8]** (our exact setup) — which *formalizes our mechanism hypothesis* and reframes the "Qwen 4B" question.
2. **A spec-level finding:** G6.1 shows the spec's `OQ-W1` drift model (locality degrades as a function of cumulative *edge count*) is monitoring the **wrong variable** — interference is **relation-fan-out-conditioned**, not volume-conditioned.

## 1. Mechanism — CONFIRMED by all sources + our data
The cross-entity collapse is **shared-relation-direction interference**, triangulated:
- **Math (Perplexity):** keys decompose as `k_{e,r} = k_e + k_r + ε`; all same-relation facts share `k_r`; for a held-out key the first-order read change is `ΔW·k_h`, nonzero whenever `k_h` is not orthogonal to the update span or explicitly preserved. The shared `k_r` is **high-variance → sits in the editable subspace, NOT the low-singular-value null-space** AlphaEdit's `P` protects (threshold 0.005). Our `cache_c` preserves *edited* keys only — "sparse over edited facts, not a covering set over the relation manifold." **This is exactly our hypothesis, now with literature backing.**
- **BetaEdit (Perplexity):** proves real covariance is effectively full-rank, so practical "null-space" methods use a **truncated-SVD pseudo-null space where `P·K₀ ≠ 0`**, and that **leakage accumulates over long edit streams** → our monotonic 100→92→58→42% decay.
- **Our own corpus (NotebookLM):** the **original MEMIT paper itself** reports high-fan-out relations **P127 ("owned by company") and P641 ("athlete plays sport") suffer specificity collapse** — "capital" is exactly such a relation. The **LARQL "LLMs Are Databases" source** states it plainly: relations are "shared multi-entity slots"; an uncalibrated edit "hijacks all the other capital queries." Superposition/polysemanticity (Anthropic Toy Models / Scaling Monosemanticity) is the root cause.
- **Verdict:** mechanism is no longer hypothesis — it is consensus. A capacity ceiling exists but is **relation-conditioned** (key overlap, fan-out, conditioning, leakage, preservation coverage), **not a universal edits-per-N law** (no source proves one).

## 2. The biggest new finding: BetaEdit reframes "Qwen 4B"
Earlier I said 4B was "nowhere it needs to be." **BetaEdit changes that.** It uses **Qwen3-4B-Instruct on band [4-8]** as a primary validation model and stays nonzero at 10,000 edits where AlphaEdit/RECT/PRUNE/EMMET collapse to zero. So:
- Qwen3-4B is now a **defensible scale/comparison model** — running our G6.1 stress on it lets us compare directly against BetaEdit's published curves.
- BUT BetaEdit's own reported specificity is still weak at extreme scale (e.g., 43.9 specificity at 10K edits on LLaMA3/ZsRE) — it keeps editing *alive*, it does not *solve* cross-entity isolation. So BetaEdit is a **stronger base solver to build the relation-balanced fix on top of**, not the fix itself.
- Note the model-size tension (NotebookLM corpus-2 open Q): nobody has tested whether a *small dense* model has more tightly-packed polysemantic clusters → faster cross-entity collapse at lower N. **Our own evidence already partially answers this** (Qwen-7B clean, 3B fails sequential) — G6.1 + a 4B/7B replication would quantify the size-dependence.

## 3. Convergent #1 recommendation (Perplexity + our refined candidate-1)
Both the survey and our advisor-refined plan land on the SAME top prototype: **relation-balanced in-solve sentinels.**
- For each hot relation `r`, maintain THREE disjoint key sets: edited `K_E(r)`, previously-edited preserved `K_P(r)`, and **held-out same-relation sentinel `K_S(r)`** — and add `K_S` to the preservation objective **inside the solve** (penalize `‖ΔW·K_S‖` / preserve `W·K_S`), NOT post-hoc (BetaEdit: pseudo-null leakage makes post-hoc structurally too late — which is exactly why our prior post-hoc Rung-3 only reached 50%).
- **Blocking design requirement (advisor):** the sentinel pool `K_S` and the eval held-out pool must be DISJOINT, both disjoint from edited — or we rebuild the tautology trap.
- **Known risk:** if the relation-shared direction is the *only* path to express the edit in early band [4-8], constraining it may lower edit efficacy → may force the later/mid band (ties to the C15 test, cov warming now) or push high-fan-out relations to side memory.

## 4. Spec reconciliation — a real finding for the spec
- **OQ-W1 / GAP-1** (from our own spec, surfaced by NotebookLM corpus-2): "Cumulative edit volume degradation threshold (model-specific)… Blocked by: Target model selection + write-volume stress test." **G6.1 IS that deferred stress test** — and it shows the spec's drift model (warning @1,500 edges, hard-stop @8,000 edges, sub-batch @2,000) is **monitoring the wrong variable**: interference is **relation-fan-out-conditioned, not edge-count-conditioned**. 100 capital edits corrupt cross-entity reads while 100 *diverse* edits might not. → **Recommend the spec add a per-relation fan-out / interference-slope drift signal**, not just a global edge counter.
- **"Disambiguation anchors"**: corpus-1 said absent; corpus-2 found the real spec contracts — **C2 "all entity names must be compositionally unambiguous" + C4 "untyped entities are schema violations."** These are schema-level; they do NOT address *relation*-level fan-out collision (the actual failure). Gap stands.
- **Genesis**: "single atomic 2PC across L1-L4; partial Genesis invalid" + MEMIT batch 2,000/sub-batch — Genesis is a **batch** write, reinforcing why batch-vs-sequential must be characterized (we only tested sequential).

## 5. Updated candidate ranking (post-research)
| Rank | Approach | Status change | In-weight? | Cost |
|---|---|---|---|---|
| 1 | **Relation-balanced in-solve sentinels** (3 disjoint pools) | **Strongly endorsed** — Perplexity #1 + our candidate-1 converge | Yes | cheap (cached 3B) |
| 2 | **BetaEdit leakage-aware solve** (history-refresh, pseudo-null leakage compensation) | **NEW** — implement & compare; validated on our exact Qwen3-4B/[4-8] | Yes | medium (port BetaEdit) |
| 3 | **Batch / breadth-first relation re-solve** | confirmed cheap & mandatory (Genesis is batch); but MEMIT's `E_mix` null result tempers hope batch *alone* fixes it | Yes | cheap (~1-line) |
| 4 | **WISE-style side memory for high-fan-out relations** | the ceiling-breaker / hybrid; WISE reports locality 1.00; matches spec's own Git/.vindex + tiered-memory hybrid | Hybrid | medium |
| 5 | **SAE-guided disentanglement (Qwen-Scope)** | frontier; residual-stream-SAE → down_proj bridge **unestablished in any source** (both confirm) → multi-week research, gated on 1-3 | Yes | high |

## 6. What the research warns us NOT to do
- **Don't expect batch alone to fix it** — MEMIT's own `E_mix` experiment: relation diversity "neither positively nor negatively" affects scaling; sources are SILENT on whether same-relation batching balances vs concentrates. Batch must carry relation-balanced sentinels to matter.
- **Don't trust λ-tuning as the fix** — increasing covariance protection (λ / threshold) raises specificity but monotonically *kills* efficacy/generalization (MEMIT + our own thresh=0.001 → ret 0% result). It's a dial, not a solution.
- **Don't lean on the apples-to-oranges threshold** — our pre-registered "cross-entity ≥ baseline−5" used a within-entity n=2 baseline; the monotonic top-1 collapse is the real evidence.
- **Don't over-invest in SAE yet** — both sources independently confirm NO published bridge from residual-stream SAEs to closed-form down_proj edits. High ceiling, but unproven and basis-mismatched.

## 7. Recommended next moves (cheapest-first, all reuse the G6.1 held-out-top-1 metric)
1. **Already running:** mid-late band cov compute (C15/BLUE band test).
2. **Build now (cached 3B):** (a) batch-vs-sequential at N=100 [the cheap miss]; (b) **relation-balanced in-solve sentinels with 3 disjoint pools** [the convergent #1 fix].
3. **Port & compare:** BetaEdit leakage-aware solve (then optionally replicate on Qwen3-4B to anchor against its published curves).
4. **Spec action:** log the OQ-W1 "wrong variable" finding (drift should be relation-fan-out-conditioned) for the spec owner.
5. **Hold:** WISE-style side memory (ceiling-breaker if 2-3 hit a wall) and SAE program (frontier, gated).
6. **Evaluation upgrade (all sources agree):** formal 5-way locality split (edited / held-out same-relation / same-entity other-relation / unrelated / global) + track top-1 AND gold-logit margin AND KL; run N=10,25,50,100,250,500,1000 in BOTH sequential and batch.

## 8. New references to pull (not previously in our repo)
BetaEdit (2605.09285) · LocFT-BF (2509.22072) · O-Edit (2410.11469) · RECT (2401.04700) · PRUNE (2405.16821) · DiKE (2505.18774, already in easyedit_assets) · FiNE (2503.01090) · WISE (2405.14768) · MELO (2312.11795) · EMMET (2403.14236) · "Model Editing at Scale" (2401.07453) · RippleEdits (2307.12976) — adopt as external-validity benchmark.
