---
name: native-knowledge-screen-is-not-editability
description: "A native-knowledge screen (model knows the fact) is necessary-not-sufficient for an edit-corruption substrate; editability (clean subject + expressible counterfactual) is the real gate, and weight-destruction ≠ corruption."
metadata: 
  node_type: memory
  type: project
  originSessionId: ab1e2081-77d6-4198-ab85-1ae87b06cbe3
---

C1 true-scale (D-C1TS-1, `docs/C1_TRUESCALE_SUBSTRATE_DIAGNOSTIC.md`, 2026-06-25). The long-gated C1 falsifier (B3N cond-3: does compaction stay clean at the spec's ≥2,000-edit regime?) needs a high-cardinality real-knowledge substrate. `city→country` screened 2,631 facts the model natively knows (single-token country) — looked like the gate was finally cleared. It was not.

**An edit-corruption substrate must satisfy ALL of these *simultaneously*** — and a native-knowledge screen only checks the last one:
1. single-token VALUE (clean grading + single-token edit),
2. **clean (≤2-tok) SUBJECT** — `city→country` fails: only 115/2,631 single-token; multi-token subjects (Itaquaquecetuba…) are **key-collinear → ill-conditioned AlphaEdit solve → ΔW blow-up (8900 vs 207) → model emits garbage "!"** ,
3. **EXPRESSIBLE counterfactual** — `city→country` fails: even clean single-token subjects express only **27–42%** because counterfactuals fight an entrenched pretrained prior ([[in-weight-knowing-insert-robust-update-fragile]] R5/R13 fragility) < the ≥85% under-editing gate,
4. cardinality ≥ target N,
5. native knowledge (the screen).

Clean-subject single-token relations cap ~78–118 (country→capital 78, element→symbol ~118), so **true-2,000-scale single-relation high-concentration C1 with real knowledge is not runnable with this recipe/substrate.** The 78-entity country pool stays the clean ceiling; C1 is now characterized AND **substrate-ceiling'd**.

**Transferable lessons:**
- **`!`-everywhere / 0% on everything = weight DESTRUCTION, not knowledge corruption** — a different axis. Real corruption flips held-out to *wrong-but-real* values (C1-(a): 73% retention), never universal garbage. Don't write a blow-up up as a scale/corruption finding.
- **Screen for editability, not just knowledge:** before committing GPU to a large-N edit experiment, screen subject-token-length AND counterfactual expressibility, not only native correctness.
- **Pilot-first + cheap-diagnostic (advisor-steered) earns its keep:** one N=2,000 pilot (62 min) + two ~5-min ladders revealed the substrate was broken and **prevented a 4–10-day wasted grid**. Cost-anchor a run before sizing a grid; let the cheap step gate the expensive one.
- **Frontier inflection:** this marks where the 3B/AlphaEdit/single-token-real-knowledge falsification regime hits its evidence frontier — remaining F1 movement is BUILD (index/query, governance) or REGIME-change (bigger model / better edit method), not one-more-3B-run. Reinforces [[in-weight-necessity-is-scope-keyed-hybrid]] (unstable counterfactual-at-scale = the incremental path, already side-store-routed; the proven batch core edits novel facts and is unaffected).
