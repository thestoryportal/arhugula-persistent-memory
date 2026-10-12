CONFIRM

Reviewer: GPT-6-Astra (high)

- **Integrity/provenance complete.** Independently verified source, engine, model, tokenizer, cache, supervisor and environment hashes; dataset revision `b04c8d1ceb2f5cd4588862100d08de323dccfbaa`, 6,407,814-row order, permutation, selected row identities, text hashes and token IDs. Both saved populations contain all 36 tensors and matching provenance: **F1000 99,610 tokens; R1000 95,610**. Pinned code saves/fsyncs these before scoring. Clean supervisor-observed exit 0 after cleanup; **354.146 s < 3,060 s**. [Artifacts](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10z_v7_diagnostic/20261009T182427Z/verdict.json)

- **Independent CPU recomputation confirms A1.** Decoded saved tensors without Torch; SciPy average-tie Spearman against the recorded cache diagonals reproduces all 18 correlations within `1e-12`; all E values match exactly. F1000 fails at layer 8 (**0.7718877414**) and layer 12 (**0.7669838841**). R1000 passes every layer 4–12; minimum **0.9291099440**. Thus rule 1 is not triggered, rule 2 selects **exactly pinned R1000**. R5000 was correctly pinned but **not measured**; E does not affect routing. [Frozen table](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:750)

- **Earlier launch is a non-run.** `20261009T182053Z` exited 3 at GPU exclusivity, blocked by CPU unittest PID 24066, before probe execution/model loading. No population observations exist: it consumes no diagnostic measurement attempt and creates no reading-around. Its refusal remains preserved. [Refusal](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10z_v7_diagnostic/20261009T182053Z/worker.log)

- **Interpretation:** this establishes population-dependent V7 agreement and supports the population explanation; it does not establish universal cache/statistic correctness or recover attempt 3’s physical cause. Attempt-3 dataset identity remains **UNVERIFIABLE**; late-layer fidelity **UNVERIFIED**. Attempt 3 stays HALTED-V7. No candidate, method-family or F1 claim follows.

**Required before continuation**

1. Freeze the **A1 amendment**: reference-D population equals this exact R1000—dataset revision/config/split/length/order, ordered indices/row IDs/text hashes/token IDs/counts, immutable population-artifact hash, model/tokenizer/cache pins, unchanged arithmetic, precision, masking, 100-token truncation and 16-row batching.
2. Freeze/review implementation and tests: synchronize prereg/source hashes and driver/reader/manifest validators; reject any different population, including another valid-sized 1,000-row set. Preserve pre-validation persistence, exclusive/fsynced writes, process-2 byte identity and forced-failure retention tests. A1 retains 1,000 rows; A2’s 5,000-row budget changes do not apply.
3. Only then perform **benchmark drift rerun #3**, preserving previous outcomes and cumulative refusal counts. Existing STOP/refusal rules apply; no automatic fourth rerun. On admission, append benchmark hashes and recomputed ceilings, then create a fresh go record binding final sources, environment, amendment and exact population.
4. Use fresh `results/c10z_astra_attempt4/` and logs; rerun the complete baseline, LAW gates and V7. Diagnostic tensors do not substitute for gate completion. Another V7 failure remains HALTED-V7, with no further search authorized. [Continuation requirements](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:777)

🌱 graft reported ~196,875 tokens saved (~$0.10), 1 successful call.

