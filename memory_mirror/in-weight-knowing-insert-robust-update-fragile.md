---
name: in-weight-knowing-insert-robust-update-fragile
description: In-weight (MEMIT/AlphaEdit) native-knowing is paraphrase-robust for NOVEL inserts but fragile for counterfactual UPDATES over priors; diversity (not intensity) partially rescues
metadata:
  type: project
---

R13+R5 (CORPUS/28,29; D-R13-1, D-R5-1; Qwen2.5-3B band[4-8], N≤24, 1-seed) — empirical bound on the paradigm payoff ("agents natively know"):

- **Trained-prompt firing ≠ usable knowledge.** A counterfactual edit fires ~100% on its trained prompt but only ~22-25% (mean) across held-out natural paraphrases. ALWAYS measure native-knowing with HELD-OUT paraphrases (L2 behavioral probe), never the trained string — the latter massively over-reports. Use mean-paraphrase-hit-rate as the primary "usable" metric; all-N-hit is too brittle, any-1-hit too lenient.
- **The fragility is COMPETITOR-SPECIFIC, not generic.** NOVEL facts (fictional/thin subject, no native competitor = the realistic new-project-fact condition) are paraphrase-ROBUST (100%, 16/16 all-hit). Counterfactual-over-dense-prior (France→Oslo vs entrenched France→Paris) is fragile (0/16 all-hit), and ~75% of paraphrase failures REVERT TO THE TRUE fact — the native prior reasserts; the edit is a narrow trained-template attractor that fails to override it.
- **A generalization-aware recipe partially rescues, and it's paraphrase DIVERSITY not training INTENSITY:** training on diverse paraphrases lifts counterfactual-over-prior 25→65% mean; training 3× on the SAME prompt barely helps (31%). (Diversity-vs-intensity isolation directional, underpowered at N=16 — confirm before hard-coding a recipe amendment.)
- **F1 / B3N consequence (two-sided):** the INSERT path (new facts) gives usable in-weight native-knowing; the UPDATE path (overwrite known facts — spec-required §8/§11.12) is fragile-but-partially-rescuable vs pretraining; **overwrite-of-a-prior-edit is a SEPARATE UNMEASURED cell** (a prior edit may localize=easier OR entangle=harder — do NOT assume it's "between" novel and pretrained-prior). Links [[in-weight-vs-sidestore-f1-question]], [[in-weight-necessity-is-scope-keyed-hybrid]], [[match-metric-to-the-claim]].
