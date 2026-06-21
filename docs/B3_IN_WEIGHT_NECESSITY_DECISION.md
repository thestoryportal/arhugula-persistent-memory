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

**The spec contemplates both write models:** `genesis_prepared_timeout` **and** `incremental_prepared_timeout`, plus `parametric_deferred` (delayed reconciliation via Pruning catch-up) — i.e., the spec explicitly supports both a batch genesis core *and* incremental writes. So Axis B is **not pre-decided by the spec**; it is a deployment-profile choice. The corruption evidence applies **only** to the incremental-at-scale profile.

**Axis B finding:** In-weight is sufficient-and-defensible for the **genesis/batch** read-write contract at scope (our own data). The **incremental-at-scale** profile is exactly where the corruption findings + the field's convergence make a **routed/gated side-store the stronger candidate**.

---

## 4. The one real discriminator (and its answer)

No *single decisive pre-registered* falsifier exists for "is in-weight required"; the necessity claim **decomposes into discriminating requirements** (§4 + the overturning conditions below). The sharpest checkable sub-question:

> **Does a structured side-store fail any read the spec *contractually* requires?**

**Answer (from the spec read-contract + EV-2, on paper): No — conditional on reliable routing.** Every enforced read invariant — L1 SELECT read-back, reverse lookup / bidirectional traversal, multi-hop & aggregation — is satisfiable (and multi-hop is at-least-as-well served) by a structured KG/KV side-store **given a reliable NL→query / entity-resolution routing layer**. That routing layer is the side-store's real risk surface (it can fail under context budget, ambiguity, routing error, or prompt injection) and is itself an open F1 question, not assumed solved here. The one thing a side-store does not deliver *by construction* is the *forward-pass native-knowing preference* of line 90, which carries no contractual test.

**What would overturn this position toward "in-weight is required":**
1. A **confirmed deployment requirement** for reason-over-fact **mid-generation with no tool-call / no retrieval step** under a **hard latency budget** (none currently in the spec); **or**
2. A confirmed **incremental-write-at-scale** requirement where a side-store's routing *also* fails — which would not rescue diffuse in-weight (it corrupts on exactly that path), but would reframe the whole F1 verdict toward a third paradigm (Parametric-RAG / per-query injection, register D19).

---

## 5. External convergence — labeled as directional priors, NOT evidence (DISCIPLINE §3)

**Some external leads appear aligned with gated/routed/disjoint side-store or context-reasoning designs** rather than diffuse in-weight editing. This is *not* a verified "the field has converged" claim — **these are co-citation LEADS: directional priors, NEVER harness evidence, NEVER `CORPUS/`.** Only **NeuralDB** is independently confirmed as a real paper (EV-3); none verified in our harness. They are weighted accordingly below.

- **Gated/routed side-stores:** NeuralDB (KV-DB query + non-linear gated retrieval, 100K facts — closest published cousin to the spec; EV-3 confirmed), WISE, GRACE/MELO, MEMOIR (disjoint sparse masks), SCEN (per-fact experts), InComeS (gist-token KV) — register D9/§J.
- **Context-reasoning over editing:** SCR "No More Model Editing!", "Benchmarking & Rethinking KE" — register D13.
- **Named critiques of diffuse in-weight:** *Is Model Editing Built on Sand?* (shortcuts not semantics), *Mirage of Model Editing* (teacher-forcing inflates 96.8%→38.5%, fails @1000 edits) — KEO/D16; *Editing-Overfit/EVOKE* names our own E1 margin confound — D17.
- **Third paradigm:** Parametric-RAG / per-query adapter injection — register D19; self-updatable parametric memory (MEMORYLLM/Larimar/MemLLM) — D18.

**Anti-bias guard ([[in-weight-vs-sidestore-f1-question]], advisor):** everything loaded leans side-store, but our *own* empirical results support in-weight **at batch scope**. Elevating unverified external leads over our own data would be backwards for a falsification-first program. The leads are weighted as a **directional prior that the incremental path is where in-weight loses**, consistent with — not the driver of — our Axis-B finding. They do **not** by themselves decide the batch-path verdict.

---

## 6. VERDICT — scope-keyed conditional hybrid (hand F1 the conditional, not a blanket pick)

**In-weight is neither universally required nor universally wrong. The verdict is keyed to the deployment write-profile (Axis B), under a read contract (Axis A) that a side-store can already satisfy:**

| Deployment profile | Recommended store | Basis |
|---|---|---|
| **Genesis / batch-rebuild core** (the D-SCOPE-1 deployment model; 3B / N≤100, compile-offline → serve-CPU) | **In-weight is viable at tested scope** | Our own data: A1 clean, B3 quant-survives, E1 CPU-serves. Native-knowing delivered with **no observed corruption cost at this scope**. *Viable-at-tested-scope, NOT architecture-final:* untested across relation diversity, larger N, 7B transfer (OQ-W1), deletes/updates, adversarial reads, and long-term drift — all F1 follow-ons. The batch core needs **no per-relation guardrail** (see note). |
| **Incremental high-churn at scale** | **Route to a gated/structured side-store** (diffuse in-weight not recommended) | Our corruption data (G6.1, D-D1-2 k≤1, mixed-load) + side-store-aligned external priors (§5). Diffuse in-weight fights interference the side-store avoids by construction. |

> **Guardrail-placement note (cross-family review §7.5):** the §8.7 `k≤1` + global-volume guardrails are **incremental-path** instruments — they bound *per-relation concentration and total volume since anchor on the sequential write path*. They govern the **incremental row only**. The **batch-rebuild core does not import them**: it compiles a clean store in one shot (A1 100%), so there is no since-anchor accumulation to bound. F1 must apply `k≤1` as a condition on *any residual/incremental mode*, **not** on the batch core — otherwise incremental failure is silently re-imported into the batch path (the double-count §3 warns against).

**F1 instruction:** Do **not** write F1 as a blanket "in-weight ready-with-conditions," nor as a broad architectural settlement. Write it as a **scope-keyed hybrid**: in-weight for the genesis/batch core **at tested scope** (conditions = stay within the validated envelope: batch-rebuild, ~3B, N≤100; the §8.7 `k≤1` + global-volume guardrails attach to *any incremental/residual mode*, **not** the batch core itself), and a routed side-store read-path for incremental high-churn (with the routing-reliability caveat, §4) — plus the explicit notes that **if** a hard mid-generation / zero-latency reason-over-fact requirement is ever confirmed (Axis A flips to "hard requirement"), in-weight's necessity must be re-opened; and **if** incremental-at-scale is confirmed required, the candidate is a side-store / Parametric-RAG, **not** diffuse in-weight. The §1.1 dimensions (auditability, delete/update governance, security, routing, cost) remain separate F1 sub-decisions.

---

## 7. Calibration & review

- **Label:** reasoned architectural position, not an empirical PASS (no falsifier exists for the necessity claim). The one checkable sub-discriminator (§4) is answered on-paper from the spec + EV-2.
- **Advisor (pre-authoring):** mandated the two-axis frame; caught the double-count risk (incremental corruption vs batch path); flagged the confirmation-bias-toward-side-store trap and the "label as position not PASS" requirement. All incorporated.
- **gpt-5.5 cross-family (inline, FIX-FIRST — applied):** concurs the verdict is "directionally right." Required fixes folded in: (1) axes are "primary discriminators," not exhaustive — added §1.1 (observability/governance/security/routing/cost omitted, several favor side-store); (2) softened "only thing in-weight buys" → "primary contractually-relevant" (§2); (3) side-store satisfies invariants "**given reliable routing/NL→query translation**" — routing is the real risk surface (§2/§4); (4) verdict "viable at tested scope," not "sufficient/architecture-final" (§6); (5) **guardrail-placement fix** — `k≤1` governs incremental/residual mode, NOT the batch core (§6 note) [the main leak it caught]; (6) "no single *pre-registered* falsifier," claim decomposes (§0/§4); (7) demoted "field convergence" → "some external leads appear aligned" (§5); (8) latency evidence marked "suggestive not resolving" (§2). Direction unchanged; calibration tightened.
- **Scope:** all empirical anchors are 3B / N≤100 / batch. Cross-model (7B) numeric transfer (OQ-W1) is still open and is the *next* science item, but it does not change the architectural verdict (it sharpens the §8.7 condition value, not the in-weight-vs-side-store position).

**Open follow-ons (do not block F1):** confirm with the operator whether the deployment profile is batch-only or includes incremental-at-scale (decides which row of §6 governs); the answer is the single biggest lever on the F1 verdict.

---
_Refs: spec §1 (line 88–90), §"L1 storage probe" (391), D4 reverse-lookup (287), `drift_state.p95_latency_ratio` (376/846), reads-block-during-mount (642), `genesis_prepared_timeout`/`incremental_prepared_timeout`/`parametric_deferred` (923–944). CORPUS/13,14,17,18,22. Hypothesis register §B/§H/§J. Memories: [[in-weight-vs-sidestore-f1-question]], [[scope-gate-batch-is-deployment-model]], [[match-metric-to-the-claim]], [[evidence-over-scaffolding]]._
