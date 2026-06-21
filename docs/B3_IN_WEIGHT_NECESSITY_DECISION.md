# B3 — In-Weight Necessity Decision (in-weight vs gated/routed side-store)

**Decision-ID:** `D-B3N-1` (the "B3" of the *hypothesis register* — "L2 in-weight may be unnecessary"; **disambiguated** from `D-B3-1`, which is the unrelated Q4_K_M quantization-survival experiment / CORPUS/17).
**Date:** 2026-06-21 · **Author:** lead experimentalist (Claude) · **Reviewed:** advisor (Opus) pre-authoring; gpt-5.5 cross-family (inline) — see §7.
**Type / label:** **Reasoned architectural position for the F1 readiness determination — NOT an empirical PASS.** No *single decisive pre-registered* falsifier exists for "is in-weight required"; the claim decomposes into discriminating requirements (§4), each argued from the spec read-contract + our own empirical results + (clearly-labeled) external directional priors. Calibration discipline: [[prototype-tautology-trap]], [[pass-label-not-equal-promotable-claim]].

---

## 0. The question (and why it is the highest-stakes open F1 item)

> **Is diffuse in-weight (MEMIT-class) parametric storage actually *required* by the LLM-as-Database spec, or would a gated/routed structured side-store satisfy the same read/write contract — possibly better?**

It is the highest-stakes item because the spec's entire thesis (§1, line 90) *is* in-weight: the shift "from in-context learning (RAG) to in-weight learning." If a side-store satisfies the contract, F1 cannot honestly be a clean "in-weight ready-with-conditions" — it must explicitly take a position. The field's published direction has converged *away* from diffuse in-weight (§5), and our own corruption evidence is consistent with that pressure — so this must be confronted head-on, not assumed.

## 1. The two *primary* discriminators (not an exhaustive decomposition)

Lookup, reverse lookup, and graph traversal are **not** discriminators: a structured side-store (KV / KG index) does all three. The two axes below are the **primary discriminators for the in-weight-vs-side-store decision** — they are **not** an exhaustive decomposition of the architecture choice (§1.1 names the dimensions they omit). The verdict is keyed to where the spec sits on each:

- **Axis A (READ):** Does the spec *require* knowledge to live **in the forward pass** — implicit "native knowing," no explicit retrieve-step — or is **explicit retrieve-then-condition** functionally adequate? Forward-pass native knowing is the **primary contractually-relevant** capability in-weight uniquely provides (it has other unique properties too — §2).
- **Axis B (WRITE):** Is the deployment write model **genesis/batch only**, or **incremental-at-scale**? Our corruption evidence is path-specific; this axis decides whether it even applies.

### §1.1 — Dimensions these two axes deliberately do NOT settle (cross-family review, §7)
The A/B axes decide *necessity of in-weight for the read/write contract*. They do **not** decide, and F1 must treat as **separate open questions**: **observability / auditability** (a side-store can expose exact provenance/state; diffuse in-weight cannot), **governance — delete / update / rollback / TTL / scoped visibility / conflict resolution** (materially different between the two), **security / trust boundary** (a routing+tool layer changes the threat model vs parametric memory), **routing & NL→query reliability** (see §2/§4 — the real hard part of a side-store), and **operational cost** (offline-GPU-edit→compile→CPU-serve vs index writes). Several of these *favor a side-store* (auditability, delete semantics); at least one (trust boundary / no external mutable state) *favors in-weight*. They are out of scope here but in scope for F1.

---

## 2. Axis A (READ) — does in-weight buy anything the contract requires?

**The primary contractually-relevant capability in-weight uniquely provides** over a structured side-store is *forward-pass native knowing*: the model conditions on the stored fact **without an explicit retrieve+inject step** (zero added retrieval latency; the fact is available mid-generation as parameters, not as injected context). *(In-weight also has other unique properties — no dependency on external mutable state, no retriever recall/routing failure mode, token-budget independence — none of which the spec makes contractual; they re-enter as §1.1 trade-offs, not as read-contract requirements. The read-contract case turns on native-knowing.)*

**What the spec actually requires of the read path:**

| Read requirement (spec) | Side-store can satisfy? |
|---|---|
| **L1 storage probe** — `SELECT` read-back confirms an edge was written (§ "L1 — Storage probe", line 391) | **Yes** — exact KV lookup |
| **Reverse lookup / bidirectional traversal** — "Every edge supports reverse lookup; no write-only edges" (D4, line 287) | **Yes** — a structured KG indexes both directions natively (EV-2) |
| **Multi-hop / aggregation reads** (the read-contract surface, E3) | **Yes (given routing)** — a structured KG is at-least-competitive, *beating* vector-RAG on exactly these (EV-2: 6/10, directional only) |

*(All "Yes" cells assume a reliable NL→query routing layer — §4. The table establishes the side-store has no contractual *capability* gap, not that routing is a solved problem.)*

**Correction to the register's framing.** The register asserted "B3 = E3: multi-hop needs in-weight, so L1 retrieval can't do reason-over-fact." **EV-2 weakens that premise** ([Pra0809/xai-knowledge-graph], hypothesis register §H): a structured KG **wins** on structural / multi-hop / aggregation reads (6/10 vs vector-RAG — directional, n=10, judge-biased, not a transportable number). So the in-weight case does **not** rest on multi-hop — a structured side-store does multi-hop at least as well. **It rests primarily on the spec's stated paradigm preference at line 90.**

**Is "native knowing / zero-latency / no prompt reconstruction" a hard requirement or a stated preference?** The spec text resolves this:

- Line 90 ("agents natively 'know' … without requiring prompt reconstruction") sits in **§1 Purpose and Paradigm** — the *motivating thesis*, framed as a paradigm shift. It is **not** a numbered guarantee, an interface contract (Appendix B), or a contractually-tested invariant.
- There is **no latency SLA, no response-time budget, no "must reason over fact mid-generation without a tool call" clause** anywhere in the spec (grep: `latency|SLA|milliseconds|response time|inference budget` → no hard read-latency requirement).
- The *one* latency signal that exists — `drift_state.p95_latency_ratio` — is a **health/compaction trigger that tolerates up to 2× baseline** before even *scheduling* action (§ line 846). And reads **block** against `.vindex` during the mount window with **no stale-read fallback** (line 642). These are **deployment-health signals, suggestive not resolving**: they argue against a *strict zero-latency SLA*, but do **not** by themselves prove that prompt-reconstruction / tool-retrieval is *semantically acceptable* for the read contract. They lower the bar for "is native-knowing contractually mandatory"; they don't eliminate it.

**Axis A finding:** In-weight is **not contractually necessary** for the read path *as the spec enforces it*. Its primary unique value — forward-pass native knowing — is a **stated design preference (the paradigm motivation), not a tested hard requirement.** A structured side-store satisfies every *enforced* read invariant **given reliable routing / NL→query translation** (entity resolution, schema grounding, ambiguity handling, tool-invocation reliability — the genuinely hard part of a side-store, §4). Whether the native-knowing preference is worth its cost is exactly the F1 conditional, and it is decided by Axis B.

---

## 3. Axis B (WRITE) — where the corruption evidence does and does not apply

This is where prior framing was blurred and at risk of **double-counting**. Our corruption findings are **path-specific**:

- **Genesis / batch-rebuild path** — *clean at scope.* A1: 100→100% held-out at N≤100 (CORPUS/14); B3/D-B3-1: survives real Q4_K_M (edited 100% vs native 97.4%, CORPUS/17); E1: CPU-serves the edited store (CORPUS/18). **D-SCOPE-1 pins the *deployment* model as batch-rebuild.** On this path in-weight is **empirically sufficient** for the read/write contract at scope (3B / N≤100).
- **Incremental / sequential path** — *this is where corruption bites.* G6.1 cross-entity read corruption (CORPUS/13); D-D1-2 §8.7 guardrail `k≤1` (corruption is edit-order- and held-out-set-dominated; CORPUS/22); mixed-load shows other-relation *volume* corrupts a relation's reads. **All incremental.**

**So "our evidence pressures in-weight" is true for the incremental path and *false* for the batch path.** Counting incremental corruption against the batch deployment model is the double-count to avoid.

**The spec PRE-DECIDES Axis B — and it is a *compaction-bounded hybrid*, NOT batch-only** (§8.3, §8.4, §8.7, §8.10; this corrects an earlier "batch-only / open operator question" framing — the operator was right to send this back to the spec). The spec's operating model is explicit:
- **§8.3 — two modes:** *Genesis Mode* (batch compile, mints the initial `.vindex`) **and** *Incremental Mode* (smaller patches buffered via an L1 Cache before MEMIT compile).
- **§8.4 — the tier stack carries `incremental_NNNN.vindex` *per-commit overlays*** on top of the frozen genesis tiers → incremental in-weight writes **are** part of the architecture, accumulating as stacked overlays.
- **§8.7 — drift-from-anchor thresholds** bound that accumulation: warning at 1,500 / hard-suspend at 8,000 edges *since the last anchor*.
- **§8.10 — compaction** = a **full MEMIT re-run** (a batch rebuild) every ≤30 days or at the drift trigger, which **resets the anchor to a clean state.**

So the spec's deployment model is: **a batch genesis core + bounded incremental per-commit overlays, periodically re-batched (compacted) back to a clean anchor.** D-SCOPE-1's "batch is the deployment model" was the program's choice of which path to *validate first* (the clean, achievable core) — **not** a claim that the spec omits incremental writes. It does not.

**This is the most important reconciliation in the document, and it makes our own D1/§8.7 work the linchpin:** the spec's §8.7 drift trigger is **edge-COUNT-based**, but our D1/D-D1-2 results proved edge-count is the **wrong variable** — corruption is **relation-concentration- and edit-order-dominated** (the §8.7 amendment, `k≤1`). A count-only threshold of 1,500 would let a *concentrated* burst corrupt held-out reads long before the count trips. **The §8.7 concentration-aware amendment is exactly the fix that keeps the spec's incremental overlays inside the clean envelope between compactions.**

**Axis B finding (spec-grounded):** In-weight is the spec's substrate for **both** genesis and incremental overlays. It is **viable for the spec's compaction-bounded hybrid CONDITIONAL on**: (a) the drift guardrail being **concentration-aware** (our amendment), not count-only; **and** (b) **compaction running before the clean envelope is exceeded.** The routed/gated side-store becomes the stronger candidate **only if real incremental churn is high enough that compaction cannot run often enough to keep each inter-anchor window clean** — i.e., genuine high-churn-online editing, which is a *more demanding* profile than the spec's bounded-then-compacted overlays.

---

## 4. The one real discriminator (and its answer)

No *single decisive pre-registered* falsifier exists for "is in-weight required"; the necessity claim **decomposes into discriminating requirements** (§4 + the overturning conditions below). The sharpest checkable sub-question:

> **Does a structured side-store fail any read the spec *contractually* requires?**

**Answer (from the spec read-contract + EV-2, on paper): No — conditional on reliable routing.** Every enforced read invariant — L1 SELECT read-back, reverse lookup / bidirectional traversal, multi-hop & aggregation — is satisfiable (and multi-hop is at-least-as-well served) by a structured KG/KV side-store **given a reliable NL→query / entity-resolution routing layer**. That routing layer is the side-store's real risk surface (it can fail under context budget, ambiguity, routing error, or prompt injection) and is itself an open F1 question, not assumed solved here. The one thing a side-store does not deliver *by construction* is the *forward-pass native-knowing preference* of line 90, which carries no contractual test.

**What would overturn this position toward "in-weight is required":**
1. A **confirmed deployment requirement** for reason-over-fact **mid-generation with no tool-call / no retrieval step** under a **hard latency budget** (none currently in the spec); **or**
2. A confirmed **high-churn-online write rate** (beyond the spec's bounded-then-compacted overlays) where a side-store's routing *also* fails — which would not rescue diffuse in-weight (it corrupts on exactly that path), but would reframe the F1 verdict toward a third paradigm (Parametric-RAG / per-query injection, register D19).

---

## 5. External convergence — labeled as directional priors, NOT evidence (DISCIPLINE §3)

**Some external leads appear aligned with gated/routed/disjoint side-store or context-reasoning designs** rather than diffuse in-weight editing. This is *not* a verified "the field has converged" claim — **these are co-citation LEADS: directional priors, NEVER harness evidence, NEVER `CORPUS/`.** Only **NeuralDB** is independently confirmed as a real paper (EV-3); none verified in our harness. They are weighted accordingly below.

- **Gated/routed side-stores:** NeuralDB (KV-DB query + non-linear gated retrieval, 100K facts — closest published cousin to the spec; EV-3 confirmed), WISE, GRACE/MELO, MEMOIR (disjoint sparse masks), SCEN (per-fact experts), InComeS (gist-token KV) — register D9/§J.
- **Context-reasoning over editing:** SCR "No More Model Editing!", "Benchmarking & Rethinking KE" — register D13.
- **Named critiques of diffuse in-weight:** *Is Model Editing Built on Sand?* (shortcuts not semantics), *Mirage of Model Editing* (teacher-forcing inflates 96.8%→38.5%, fails @1000 edits) — KEO/D16; *Editing-Overfit/EVOKE* names our own E1 margin confound — D17.
- **Third paradigm:** Parametric-RAG / per-query adapter injection — register D19; self-updatable parametric memory (MEMORYLLM/Larimar/MemLLM) — D18.

**Anti-bias guard ([[in-weight-vs-sidestore-f1-question]], advisor):** everything loaded leans side-store, but our *own* empirical results support in-weight **for the spec's compaction-bounded hybrid scope** (genesis clean; incremental viable under the concentration-aware guardrail + compaction). Elevating unverified external leads over our own data would be backwards for a falsification-first program. The leads are weighted as a **directional prior that *unbounded high-churn* is where in-weight loses**, consistent with — not the driver of — our Axis-B finding. They do **not** by themselves decide the spec-model verdict.

---

## 6. VERDICT — scope-keyed conditional hybrid (hand F1 the conditional, not a blanket pick)

**OPERATIVE VERDICT (the spec's own deployment model — §8.3/§8.4/§8.7/§8.10).** The spec is a **compaction-bounded hybrid**: a batch genesis core **+** bounded incremental per-commit overlays **+** periodic compaction that re-batches to a clean anchor. The verdict follows that model:

> **In-weight is the viable substrate for the spec's compaction-bounded hybrid, and B3 does NOT falsify the spec's in-weight thesis — CONDITIONAL on two guardrails the spec already half-specifies:** (1) the §8.7 drift trigger must be **concentration-aware** (our D-D1-2 amendment, `k≤1`), not count-only — this is the fix that keeps each inter-compaction window inside the clean envelope; and (2) **compaction must run before that envelope is exceeded.** A routed/gated **side-store is the stronger candidate only for genuine high-churn-online editing** — a profile *beyond* the spec's bounded-then-compacted overlays — and even then conditional on an unproven NL→query routing layer (§4).

The three rows map the deployment profiles against the spec's model:

| Deployment profile | In the spec? | Store | Basis / condition |
|---|---|---|---|
| **Genesis core** (batch compile; 3B / N≤100) | **Yes — §8.3 Genesis Mode** | **In-weight, viable at tested scope** | A1 clean, B3 quant-survives, E1 CPU-serves. No per-relation guardrail needed (one-shot solve, §6-note). *Viable-at-tested-scope, NOT architecture-final* (untested at larger N, 7B, deletes/updates, adversarial reads, long-term drift — F1 follow-ons). |
| **Bounded incremental overlays + compaction** (the spec's runtime model) | **Yes — §8.3 Incremental Mode + §8.7 + §8.10** | **In-weight, viable WITH conditions** | Per-commit overlays accumulate, bounded by §8.7 drift, reset by §8.10 compaction. **Condition: §8.7 must be concentration-aware (our `k≤1` amendment), not count-only; compaction must run before the clean envelope is exceeded.** This is where our D1/§8.7 work directly serves the spec. |
| **High-churn online editing at scale** (beyond bounded-then-compacted) | **Not required by the spec as written** | **Route to a gated/structured side-store** — *conditional on an unproven NL→query routing layer (§4)* | Our corruption data (G6.1, D-D1-2 k≤1, mixed-load) shows diffuse in-weight loses if churn outpaces compaction. A genuine *new* requirement, not the spec's current model. |

> **Guardrail-placement note (cross-family review §7.5):** the §8.7 `k≤1` + global-volume guardrails are **incremental-path** instruments — they bound *per-relation concentration and total volume since anchor on the sequential write path*. They govern the **incremental row only**. The **batch-rebuild core does not import them**: it compiles a clean store in one shot (A1 100%), so there is no since-anchor accumulation to bound. F1 must apply `k≤1` as a condition on *any residual/incremental mode*, **not** on the batch core — otherwise incremental failure is silently re-imported into the batch path (the double-count §3 warns against).

**F1 instruction:** Write F1's B3 position as **"in-weight is viable for the spec's compaction-bounded hybrid (§8.3/§8.7/§8.10), with two named conditions"** — NOT "batch-only ready," and NOT a blanket "recommend side-store." The two conditions are load-bearing and both trace to our own work: **(1)** the §8.7 drift trigger must be **concentration-aware** (the D-D1-2 `k≤1` + global-volume amendment), not the spec's current count-only 1,500/8,000 — author this as a concrete §8.7 spec amendment; **(2)** compaction (§8.10) must be scheduled to fire before the clean envelope is exceeded for the project's actual write rate. Carry the side-store as the recommendation **only** for a *high-churn-online* profile beyond the spec's bounded-then-compacted overlays (candidate = gated side-store / Parametric-RAG; conditional on the unproven routing layer, §4). Re-open Axis A only if a hard mid-generation / zero-latency reason-over-fact requirement is ever confirmed. The §1.1 dimensions (auditability, delete/update governance, security, routing, cost) remain separate F1 sub-decisions. **The remaining operator input is a calibration, not a fork: what is the project's realistic incremental write *rate*? — it sets the compaction cadence (condition 2) and whether the high-churn row ever applies.**

---

## 7. Calibration & review

- **Label:** reasoned architectural position, not an empirical PASS (no falsifier exists for the necessity claim). The one checkable sub-discriminator (§4) is answered on-paper from the spec + EV-2.
- **Advisor (pre-authoring):** mandated the two-axis frame; caught the double-count risk (incremental corruption vs batch path); flagged the confirmation-bias-toward-side-store trap and the "label as position not PASS" requirement. All incorporated.
- **gpt-5.5 cross-family (inline, FIX-FIRST — applied):** concurs the verdict is "directionally right." Required fixes folded in: (1) axes are "primary discriminators," not exhaustive — added §1.1 (observability/governance/security/routing/cost omitted, several favor side-store); (2) softened "only thing in-weight buys" → "primary contractually-relevant" (§2); (3) side-store satisfies invariants "**given reliable routing/NL→query translation**" — routing is the real risk surface (§2/§4); (4) verdict "viable at tested scope," not "sufficient/architecture-final" (§6); (5) **guardrail-placement fix** — `k≤1` governs incremental/residual mode, NOT the batch core (§6 note) [the main leak it caught]; (6) "no single *pre-registered* falsifier," claim decomposes (§0/§4); (7) demoted "field convergence" → "some external leads appear aligned" (§5); (8) latency evidence marked "suggestive not resolving" (§2). Direction unchanged; calibration tightened.
- **Scope:** all empirical anchors are 3B / N≤100 / batch. Cross-model (7B) numeric transfer (OQ-W1) is still open and is the *next* science item, but it does not change the architectural verdict (it sharpens the §8.7 condition value, not the in-weight-vs-side-store position).

- **Advisor (done-state pass):** flagged that D-SCOPE-1 is a standing decision and pushed toward "batch-only settles it decisively." **The operator then correctly redirected to the spec itself** — which is *primary source* and shows the deployment model is a **compaction-bounded hybrid (§8.3/§8.4/§8.7/§8.10), not batch-only.** So the verdict was reframed a second time: D-SCOPE-1 was the program's *test-first* scope choice, while the *spec contract* includes bounded incremental overlays + compaction. The advisor under-weighted the spec text; the spec is binding. (Process lesson → DISCIPLINE: when a decision's answer lives in the spec, read the spec FIRST, before framing it as an open question.)

**Remaining operator input (a calibration, not a fork):** what is the project's realistic **incremental write rate**? It sets the compaction cadence (condition 2 of the verdict) and whether the high-churn-online row ever applies. It does **not** change the architectural verdict — the spec's bounded-then-compacted hybrid is in-weight-viable under the two conditions regardless.

---
_Refs: spec §1 (line 88–90), §"L1 storage probe" (391), D4 reverse-lookup (287), `drift_state.p95_latency_ratio` (376/846), reads-block-during-mount (642), `genesis_prepared_timeout`/`incremental_prepared_timeout`/`parametric_deferred` (923–944). CORPUS/13,14,17,18,22. Hypothesis register §B/§H/§J. Memories: [[in-weight-vs-sidestore-f1-question]], [[scope-gate-batch-is-deployment-model]], [[match-metric-to-the-claim]], [[evidence-over-scaffolding]]._
