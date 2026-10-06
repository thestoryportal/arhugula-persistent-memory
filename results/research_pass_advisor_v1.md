FIX-FIRST

Single most important change: freeze a candidate-class taxonomy before execution, not just 15 query strings. The plan is wide, but not yet exhaustive in the ruling’s sense of “every candidate solve — editing methods AND model families” (`EXPERIMENT_RUNBOOK.md:316`). Add the missing classes below, then make the exit condition class-based.

Issues, in priority order:

1. Exhaustiveness gap: the plan misses in-weight-but-not-MEMIT routes.
   The spec’s target is facts physically in model weights / `.vindex`, behaviorally read back after write (`docs/SPEC_E2E_GROUND_TRUTH.md:7-8`, `docs/SPEC_E2E_GROUND_TRUTH.md:64-65`). The plan covers MEMIT-like edit methods and some model families (`docs/RESEARCH_PASS_PLAN_2026-10-06.md:30-47`), but should add explicit classes for:
   - continued pretraining / instruction tuning on coined facts: in-weight but off the current MEMIT write-engine contract; still in-scope as a candidate solve or spec-amendment challenger. The prior arc already found “Fresh in memory” and “Synthetic Worlds” in this class (`docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:7-9`, `docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:83`).
   - LoRA / merged-adapter writes: in-scope if merged or mounted as a parametric overlay with no read-time side store; fallback if it uses external retrieval/routing.
   - hypernetwork editors such as MEND / PropMEND: in-scope if they emit real weight deltas; the arc already names MEND in the novel-entity literature (`docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:9`).
   - retrieval-free memory-layer / value-slot architectures: in-scope only if memory is parametric and behaviorally read without external lookup; fallback if it becomes a query index.
   - vocabulary-extension/tokenizer families beyond the current mint arm: grounded token initialization, token distillation, byte/tokenizer-free families, multi-token vocabulary additions. The arc already made token initialization blocking for option iv (`docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:178-186`).

2. The hit criterion is basically right, but needs sharper wording.
   Criterion (d), held-out paraphrase recall on a multi-token target, is correctly strict because D-C10k-rulings-1 makes full-sequence held-out behavior the binding bar (`EXPERIMENT_RUNBOOK.md:305`). But the current wording could exclude useful methods because the corpus says the published cell is empty (`docs/RESEARCH_PASS_CORPUS_INVENTORY_2026-10-06.md:41-51`).
   Freeze this instead: “A candidate is a public artifact that writes or mounts knowledge into model parameters, has a verified path to local execution or measurement under D-HW-1, and can be evaluated on C10: exact full-sequence held-out paraphrase recall for a coined multi-token target, plus locality. If the paper does not report C10 but the artifact supports measuring it, log `candidate-needs-C10-eval`; if it cannot support that measurement, log `lead` or `fallback`.”

3. The 48 GB rule is directionally honest, but state a hard prefilter.
   The ruling says the envelope is 48 GB fp16, not parameter count (`docs/RESEARCH_PASS_PLAN_2026-10-06.md:3`; `EXPERIMENT_RUNBOOK.md:327`). Your “weights ≤ ~28 GB + solve headroom” is acceptable as an outer bound for 13–14B fp16, but only if streamed layer-by-layer and verified by a smoke solve.
   Arithmetic, assuming common dimensions and marking exact configs as pass-time verification:
   - 7–8B: fp16 weights ≈ 14–16 GB. For d=4096, one fp32 d×d covariance is 4096²×4 = 64 MiB; five edited layers = 320 MiB. A live solve/SVD with C, P/A, KKᵀ, U/V/workspace is roughly 4–8 matrices = 256–512 MiB per active layer. Expected working set: ~20–24 GB plus MPS overhead.
   - 13–14B: fp16 weights ≈ 26–28 GB. For d=5120, one fp32 d×d matrix is 100 MiB; five covariances = 500 MiB; solve workspace roughly 400–800 MiB per active layer, higher if not streamed. Expected working set: ~32–38 GB plus MPS overhead.
   Hard wording: “Candidate prefilter: fp16 weights ≤ 28 GB decimal / ~26 GiB, d≤5120 unless verified otherwise, edited band ≤5 layers or streamed, and a one-layer `_cov_cpu`/null-space solve smoke must pass before promotion from lead to candidate.”

4. OpenResearch is justified, but fence it more tightly.
   It is not redundant if used for alphaXiv full-text keyword search, because that is the stated gap versus arXiv MCP / Connected Papers (`docs/PRIOR_ART_OPENRESEARCH_2026-10-06.md:15`, `docs/PRIOR_ART_OPENRESEARCH_2026-10-06.md:29`). The 10-query / 5-fulltext cap is sane (`docs/PRIOR_ART_OPENRESEARCH_2026-10-06.md:39-42`). Add fences: no `orx install-skills`, no `orx up`, no project/experiment tree, no login/managed compute, telemetry off before smoke, record exact CLI version, and treat endpoint routing as UNVERIFIED because the doc says discover’s host path was not read (`docs/PRIOR_ART_OPENRESEARCH_2026-10-06.md:15`, `docs/PRIOR_ART_OPENRESEARCH_2026-10-06.md:31-35`).

5. Exit condition: make “exhaustive” decidable.
   Do not reuse the weak “two passes” shape unless “pass” means a search surface capable of adding new classes. Prior advisor issue 7 was exactly that the old exit could be met by construction (`results/infranodus_research_arc_2026-10-05/advisor_review_results_2026-10-05.md:60-65`), though the arc later fixed it with two field-vocabulary search passes (`docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:101-103`).
   Freeze: “The pass exits only when every frozen candidate class has a disposition, every new artifact is deduped and triaged, BetaEdit/AnyEdit++ contradictions are resolved, and two consecutive independent search instruments capable of adding new classes add no new candidate class after dedupe. InfraNodus synthesis over already-found hits does not count as one of the two.”

6. HIL boundary mostly holds, with one branch needing wording.
   §5 says shortlist ≤3, prereg stubs only, no route commitment, no CORPUS entry (`docs/RESEARCH_PASS_PLAN_2026-10-06.md:53-58`). That is not a hidden commitment if the full candidate table remains visible. But §1’s “LEAD” branch drops the model-family half “for now” (`docs/RESEARCH_PASS_PLAN_2026-10-06.md:13`). Reword to: “paused, not closed; D-C10q-rulings-1 remains unsatisfied for any model move.” That keeps the operator’s route authority intact.