# 02 — VALIDATION & VERIFICATION CHAIN (hypothesis → theory → provable validation)
_For each load-bearing claim: the falsifiable hypothesis, the method, the measurement, the pass criterion set BEFORE the result, and the verdict. This is the scientific spine — the council audits the LOGIC here, not just the numbers._

### C1 — In-weight same-entity multi-attribute editing is achievable (model-dependent)
- **Hypothesis:** A MEMIT-class edit of one attribute can leave the entity's other attributes intact (same-entity locality), for at least some models.
- **Method:** Calibrate a JS-based same-entity-locality metric with a clean null-edit floor (P0); single-edit on GPT-J/Qwen-7B/Qwen-3B (P1).
- **Criterion:** clean null floor (>~95% locality on a no-op) AND a real edit's same-entity locality clearly above floor noise for ≥1 model.
- **Verdict:** PROVEN, model-dependent. Floors 99%+. Single-edit same-entity: GPT-J 67.98% (fails), Qwen-7B 99.86%, Qwen-3B 98.41%. → C1 holds for Qwen, not GPT-J.

### C2 — Sequential multi-field writes don't have to clobber prior writes
- **Hypothesis:** Stock MEMIT clobbers earlier edits on the same entity; an in-solve null-space method (AlphaEdit) + accumulating cache can prevent it.
- **Method:** edit attr-1 then attr-2 on same entity; measure edit-1 retention. Compare stock MEMIT vs in-solve AlphaEdit; tune nullspace_threshold. LAW#5: prove harness reproduces engine (inertness) first.
- **Criterion:** AlphaEdit retention ≫ MEMIT, with expression intact, inertness proven.
- **Verdict:** PROVEN. MEMIT 33% → AlphaEdit 100% retention; threshold 0.005 gives 100% ret + 80.69% untouched + 100% expression; inertness gate passed.

### C3 — Cross-entity collapse at write-depth is real, and fixable by preserve-sampling
- **Hypothesis (falsification):** writing many same-relation facts corrupts UN-edited entities' same-relation facts.
- **Method:** 33-edit stream; track edited-fact retention, un-edited control locality, perplexity. Then seed cache with a sample of un-edited entities' keys; measure held-out controls.
- **Criterion:** if control locality collapses → falsified-as-clean; if preserve-sampling restores held-out controls → mitigation works.
- **Verdict:** PARTIAL→MITIGATED. Edited retention 100% + ppl flat (good); control collapsed 99.83%→11.99% (falsified clean); preserve-sampling restored held-out control 22%→78% (mitigation generalizes; coverage knob).

### C4 — Novel-record INSERT needs batched (joint) compile
- **Hypothesis:** creating new multi-field records (entities the model never knew) differs from updating known ones.
- **Method:** insert 6 fictional entities × 3 fields, sequential vs relation-keyed vs batched-joint; measure full-record retention.
- **Criterion:** identify which method gives ≥~90% full-record retention.
- **Verdict:** PROVEN. sequential 0/6, relation-keyed 1/6, **batched-joint 6/6** → batched compile (= spec's L1-buffered batch compile) is required for novel inserts.

### C5 — Edits survive 4-bit quantization
- **Hypothesis:** in-weight edits persist through Q4 (CPU deployment requirement).
- **Method:** edit fp16 → block-wise 4-bit round-trip → re-measure retention/post_p/ppl.
- **Criterion:** retention preserved (≥~90%).
- **Verdict:** PROVEN for edit-survival (100%→100%, post_p 0.98→0.957). CAVEAT: ppl 4.14→9.23 is the crude simulated quantizer; real GGUF-Q4_K UNTESTED.

### C6 — Full CRUD + compaction hold (Qwen2.5 and Qwen3)
- **Verdict:** PROVEN. CRUD INSERT/UPDATE/DELETE ~100% (Qwen2.5) / 6,5,6/6 (Qwen3); compaction-regression 100%→100% both.

### C7 — The recipe transfers to the LARQL-servable model (Qwen3-0.6B)
- **Hypothesis:** results are model-specific, so they must be re-measured on the deployment model.
- **Method:** recompute covariances + hparams for Qwen3; re-run smoke/multi-fact/scale/CRUD/compaction.
- **Criterion:** recipe expresses + clean locality without re-engineering.
- **Verdict:** PROVEN (no recalibration needed): smoke post_p 0.851, multi-fact controls 100% top1, CRUD/compaction pass. Scale: retention holds, control-loc coverage-knob (0.6B collides faster — model-size effect).

### C8 — LARQL serves our externally-edited weights, in-weight, on CPU
- **Verdict:** PROVEN. CPU positive control (Qwen3→Paris clean); decoupled serve of our merged edit; and the **bridge** (`.vlp` overlay → APPLY frozen base → COMPILE) serves France→Berlin 79% via walk-FFN with controls preserved + rollback to Paris. No LARQL code.

### C9 — The spec's FULL contracts are satisfied  ← NOT PROVEN
- **Status:** OPEN. C1–C8 establish write/read/overlay MECHANICS. They do NOT establish: 2PC/State-Ledger consistency (G1), write authorization/audit (G2), deterministic validation pipeline (G3), full query schema incl. DELETE (G4), operator-CPU (G5), efficiency-at-scale (G6), multi-token robustness (G7). **C9 is the council's audit subject.**

### C-D1B1 — Drift is relation-concentration-conditioned, and the law is model-general (D1 + B1)
- **Hypothesis:** held-out same-relation corruption at fixed total edit count is driven by per-relation edit-concentration (not global edge-count), and this holds across model size.
- **Method:** D1 concentration-vs-dilution + dose-response @ fixed total-N (Qwen2.5-3B); B1 ports the dose-response to Qwen2.5-7B (matched). LAW#5 inertness gate each run.
- **Criterion (pre-registered):** corruption rises with capital-edit-count at fixed total-N (concentration drives it); REPLICATE on a 2nd model = monotone + pos-control + expr≥95%.
- **Verdict:** D1 CONFIRM (directional, dual-reviewed, D-D1-1); B1 REPLICATE on 7B → law MODEL-GENERAL (D-B1-2). Size *threshold* UNRESOLVED — instrument is ~50pp run-to-run nondeterministic (7B seed3 20.8→70.8 on identical-config re-run); 'collapse' was noise, not a tail. → §8.7 structural amendment promotable; numeric threshold needs a lower-variance instrument.
