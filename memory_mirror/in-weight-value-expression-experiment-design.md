---
name: in-weight-value-expression-experiment-design
description: "Value-expression experiment design: bind to held-out full-sequence match; coherent+incoherent continuation arms; count-matched requests; novel names"
metadata:
  type: reference
---

Hard-won recipe from C10 (multi-token VALUE expression, D-C10-1; runners `experiments/track_c/c10b_novel_multitoken.py` + `c10c_diverse_train.py`). Reuse for ANY in-weight value-expression/firing experiment.

**Binding metric = held-out-paraphrase FULL-SEQUENCE match. NOT canonical.** Canonical/trained-prompt expression is a `compute_z` teacher-forcing artifact (it optimizes the exact prompt) → ~tautological, over-reports (R13). For multi-token values measure the FULL sequence (greedy-decode `len(target_ids)`, exact match), plus first-token, plus the within-arm `first − full` gap and the **conditional P(full | first-correct)** (the clean "did it store/generalize the continuation, not just the first token?" — de-confounds a merely-weaker first-token edit).

**Three confounds that WILL fool you (each needs a controlling arm, not a caveat):**
1. **Counterfactual-over-prior FLOOR.** Editing a counterfactual over a real entity (overwrite a known capital) floors usable expression for ALL arms (R13/R5) → underpowered + unrepresentative. **Use NOVEL no-prior subjects** (fictional names; R5 `FICTION` pool — multi-token fictional subjects are fine + paraphrase-robust at N≤24; the C1 subject-ΔW-blowup is a SCALE phenomenon only). Pre-edit base must be ~0/N.
2. **Prior-coherence of the CONTINUATION inflates multi-token results.** A multi-token value whose continuation is a known bigram ("Cape Town") gets a free ride from the base-model prior → 97%, MASKING fragility. The real test = INCOHERENT continuation (two unrelated single-tokens, "Amsterdam Ankara") → 36%. **Always include the coherent multi-token arm as a positive control** (rules out "weak edit") AND the incoherent arm as the binding case. Note: fragility axis = prior-coherence, ORTHOGONAL to syntax-vs-semantics (don't conflate; [[default-to-the-less-flattering-reading]]).
3. **Request-COUNT interference.** "Does diverse training help?" by adding training prompts to one arm changes the EDIT-REQUEST COUNT (e.g. 3 prompts×N = 3N requests) → pure interference degrades everything, swamping the diversity signal → uninformative. **Count-match the requests across arms** ([[fixed-budget-sweep-couples-iv-with-complement]]).

**Always:** same subjects across arms (isolate the value variable); fuller LAW#5 inertness gate (p-delta AND locality, not p-delta alone — C10 Run-1 used p-delta-only and passed thin at 0.0471); 1-seed gives a valid WITHIN-experiment contrast but generality needs replication ([[single-seed-limits-generality-not-significance]]); decisive falsifier → cross-family review (GPT-6-Astra high; Perplexity/Sonar may advise during auth failure but cannot replace the binding review; promotion stays blocked until Astra-high completes). **Cov recompute cost** was ~20 min PER PROCESS on the 2026-06 pod (no disk persistence there) — measure it on the current setup before budgeting. **Filename trap:** `.gitignore` `*token*` (credential rule) eats "mul­ti**token**" filenames → use "multitok" or `git add -f` after a secret-scan.
