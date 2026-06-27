## Advisor review — C10J AnyEdit Stage-0 diagnostic

**VERDICT: FIX-FIRST**

The halt/route *direction* is correct and conservatively bounded — nothing improper gets promoted, and the gate is respected. But the diagnostic as drafted has a mis-citation hazard that must be closed before it becomes a durable doc, because it turns on *what actually ran*, which the current write-up leaves ambiguous.

---

### Single most important next action
Before committing, **pin down and state precisely what the "AnyEdit window50" run actually exercised**, and record the failure *signature*:
- Did the run invoke AnyEdit's actual contribution (autoregressive/chunked **multi-token decomposition** — the thing memory says is "mechanistically matched to the multi-token W-realization failure"), or was it the **existing MEMIT-class C10h harness with `window_size=50`**? The phrase "local upstream-window transplant" reads like the latter.
- Record the **near-no-op signature** — `locality≈99.88` with `canon_full≈25/8.3` and `para_full=0.0` — as the leading explanation. Near-perfect locality + near-zero edit success is the fingerprint of *an edit that barely applied*, i.e. an integration/port artifact, not a method verdict.

This distinction is the whole scientific content. If decomposition was not exercised, the run is essentially irrelevant to AnyEdit and labeling the file/result "AnyEdit" is the recurring **name-the-manipulated-variable** error (the variable that actually moved was `window_size` in the MEMIT harness). Stated honestly, this *strengthens* your route decision: "this was not AnyEdit's method → official AnyEdit must be run in its own env" is cleaner than "AnyEdit failed."

---

### Issues in priority order

1. **(FIX) Faithful characterization of the run.** As above. Without it the doc is at real risk of being cited downstream as "AnyEdit is ineffective for C10," which your own EXPLICIT-LIMITATION line disclaims — but the I-INFER ("did not recover A1/A2 behavior") plus the "AnyEdit" filename undercut the disclaimer. Make the no-op/decomposition status load-bearing, not a footnote.

2. **(FIX) Declare the decision_id / provenance deviation.** The file is C10J-namespaced but stamps `D-C10h-anyedit-window50-controls` and the log says C10h. Prereg lists "undeclared upstream deviation" as INVALID-triggering. (a) Confirm this run did **not overwrite** any canonical C10h result (path-collision trap is in your own memory); (b) record the mislabel as a **declared deviation** so it can't read as a hidden one. Treating-as-diagnostic-only is the right call; just declare it.

3. **(OK — affirm) Negative-from-aggregate is legitimate here.** The result is gate-BLOCKED (aggregate-only, no per-unit arrays) and prereg calls aggregate-only INVALID. Using it to **halt/de-license** rather than to **promote** is consistent: you don't need per-unit arrays to refuse escalation on a catastrophic 0%, and the diagnostic correctly sets CORPUS=NO / A7=NO. Keep it explicitly framed as "insufficient to *promote*, sufficient to *stop*."

4. **(Drift / scope) Don't let AnyEdit-rescue become a sink.** AnyEdit is optional (not F1-required absent a spec amendment), and C10 already has a validated F1-viable answer: **accept-bounded → route project-coined multi-word values to Git/index/side-store (hybrid)** (`c10-accept-bounded-means-hybrid`). Of your three valid routes, the bounded-hybrid one *already closes C10 for F1 viability*. The official-upstream-env attempt is only worth its cost if F1 genuinely needs *general in-weight* multi-token storage. Surface that to the operator as a route-priority question rather than defaulting to "stand up the official env."

5. **(Minor) "Does not prove official AnyEdit ineffective" is correctly stated** — and the upstream-feasibility evidence backs it (no Qwen2.5-3B config in upstream hparams; `nltk` import failure ⇒ upstream never actually ran). That's a clean, honest boundary. Keep it.

**Drift check:** This advances F1 by *conserving* effort against a non-required method and routing to a cheaper validated answer — provided the doc is made faithful about what ran. The decision is sound; the write-up needs the two fixes above first.
