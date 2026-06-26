---
name: c10-status-and-session-b-residual-test
description: Deployment target FIXED (local Intel CPU + batch writes); C10 multi-token-value falsifier OPEN/CONDITIONAL/bounded; session-B = option B residual-test with project-coined multi-word SEMANTIC values
metadata: 
  node_type: memory
  type: project
  originSessionId: 77383f65-76b8-42d1-a7de-d3da62645250
---

**Deployment target FIXED 2026-06-26 (operator): `local Intel CPU + batch writes`** (re-Genesis model). F1 re-scoped (`docs/F1_DETERMINATION.md` header block): C4/§8.7/D1-incremental DROP from critical path; **C1 REFRAMES** to batch-genesis-at-scale (gated on TARGET FACT-COUNT — still unset, worth pinning); **C10 multi-token values + C3 firing + C2 read-layer + real-Intel-CPU-serving** = the on-target frontier.

**C10 (D-C10-1, CORPUS/35) = FALSIFIER FIRED, OPEN/CONDITIONAL, severity-BOUNDED-not-dissolved.** At the N≤100 batch path: single-token 97% & prior-coherent multi-token 97% paraphrase-robust, but **arbitrary (non-prior-coherent) multi-token values 36%** (the edit FITS the trained prompt but doesn't GENERALIZE). §7.1/D1 removes the SYNTACTIC subset (file paths/identifiers/exact strings → Git, not in-weight), BUT the residual = **project-coined multi-word SEMANTIC named entities (§7.2 domain_concept) with no prior** = the fragile class, plausibly ENRICHED (a project KB's value-prop IS the base-model-unknown facts). c10c: naive diverse-training is NOT a fix (interference); the wall = generalization at the continuation position, localized → mechanistic case FOR the AnyEdit fix.

**Three open moves (operator-gated): (A)** AnyEdit port (`jianghoucheng/AnyEdit`, Qwen2.5-compat; multi-day; PORT real solve, don't reimplement — BetaEdit lesson; payoff unproven); **(B) the residual-test ← OPERATOR CHOSE THIS for the next (fresh) session**; (C) accept C10 as the bounded limitation.

**SESSION-B (option B) GOAL:** size the REAL in-weight C10 exposure — do **project-coined multi-word SEMANTIC values** (the kind an actual project KB holds, e.g. "Qorvex subsystem", "Vindex overlay compiler") behave like the fragile incoherent arm (~36%) or better? **Design** (per [[in-weight-value-expression-experiment-design]]): novel no-prior subjects; VALUES = project-coined multi-word semantic named entities (no pretrained prior — verify pre-edit base ~0); binding metric = held-out-paraphrase FULL-SEQUENCE; include single-token + prior-coherent-multi-token controls to anchor; COUNT-MATCH arms; reuse `experiments/track_c/c10b_novel_multitoken.py`. ⚠ The key uncertainty: are real project-coined terms more *compositional/predictable* than "Amsterdam Ankara" (Perplexity's caveat #4)? That's exactly what this measures. Pre-register + advisor before build AND before verdict; default to the less-flattering reading ([[default-to-the-less-flattering-reading]]).

Fresh-session entry: `SESSION_CHECKPOINT.md` top (2026-06-26 continuation) + `docs/F1_DETERMINATION.md` (C10 row + severity bound).
