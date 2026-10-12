## §7 — STANDING SCIENTIFIC CONTEXT
═══════════════════════════════════════════════════════════════════════

### §7.1 — The mechanism (CONSENSUS across all sources + our data)
Cross-entity collapse = **shared-relation-direction interference**. Keys decompose `k_{e,r}=k_e+k_r+ε`; all same-relation facts share `k_r`. The shared `k_r` is **high-variance → lies in the editable subspace, NOT the low-singular-value null-space** AlphaEdit's `P` protects. `cache_c` preserves *edited* keys only (sparse over the relation manifold). BetaEdit proves real covariance is full-rank → truncated-SVD pseudo-null leaks (`P·K₀≠0`) and leakage **accumulates** with edits → our monotonic 100→42% decay. Confirmed independently by: Perplexity (math + BetaEdit), our corpus (MEMIT's own P127/P641 collapse; LARQL "hijacks all the other capital queries"), superposition theory, and G6.1.

### §7.2 — The spec assumption G6.1 violated (the readiness-relevant finding)
Spec `OQ-W1`/`GAP-1` models edit-locality degradation as a function of **cumulative edge count** (drift warn @1,500 / hard-stop @8,000 / sub-batch @2,000). G6.1 shows interference is **relation-fan-out-conditioned, not volume-conditioned** — 100 capital edits corrupt cross-entity reads while 100 diverse edits likely would not. → The spec's drift signal is **monitoring the wrong variable** (Track D derives the right one). This is the central reconciliation item.

### §7.3 — Proven foundation (do not relitigate; G6.1 scoped it)
- In-weight multi-field editing viable, **model/size-dependent** (GPT-J fails; 7B clean; 3B & 0.6B work with recipe).
- Recipe = in-solve AlphaEdit (null-space, thresh 0.005) + preserve-sampling + batched-per-record compile. Survives 4-bit (crude sim). Full CRUD + compaction hold.
- Decoupled bridge (clean ΔW → `.vlp` → APPLY on frozen base → COMPILE) works on CPU, no LARQL code.
- Governance CP1–G3 PROVEN-FOR-SCOPE (2PC, ledger, Ed25519, validation pipeline).
- **Scope correction:** the "COMPLETE multi-field store VALIDATED" headline was **same-entity / small-N only**. Cross-entity-at-scale is OPEN (this runbook's Track A).

### §7.4 — Evidence & metric standards (use in every Track-A run)
- **5-way locality split**: edited · held-out same-relation · same-entity other-relation · unrelated · global.
- **Track all**: top-1 correctness AND gold-logit margin AND KL-from-pre on held-out same-relation; apply-time expression separately from end retention.
- **Staircase** N = (10/)25/50/100(/250/500/1000) in BOTH sequential and batch.
- **Disjoint pools** (edit / sentinel / eval). **Positive controls** mandatory.
- **Falsifiable PASS bound** for the cross-entity fix (derived from DB viability, not anchored): held-out same-relation **top-1 correctness ≥ baseline−5 pts at N=100** with **no monotonic decay** (slope ≥ −2 pts/rung), while write-side retention ≥95% and apply-expression ≥95%.

### §7.5 — Glossary
- **retention** = fraction of edited facts still top-1-correct at end.
- **apply-time expression** = edit expresses (target is top-1) immediately when written (guards false-no-op).
- **held-out same-relation top-1** = correctness of never-edited entities on the edited relation (THE cross-entity metric).
- **within-entity locality** = edited entity's OTHER attributes intact.
- **CEloc / JS-loc** = cross-entity locality via distributional JS (supporting, not the top-1 claim).
- **fan-out** = # entities sharing a relation (the conjectured capacity driver).
- **sentinel keys K_S** = held-out same-relation keys added to the in-solve preservation term (A2).

═══════════════════════════════════════════════════════════════════════
