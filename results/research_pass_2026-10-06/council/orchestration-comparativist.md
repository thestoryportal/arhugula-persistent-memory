## orchestration-comparativist

Lens: how each top hypothesis sits inside the write path of spec §12 / §8.3–§8.4 and e2e §C–§D. Fixed facts held against all three: the atomic unit is `{module_code, test_suite, .larql_patch, declared_dependencies}` (§C.1); the Coder drafts the patch, the TGA authors tests, no reasoning agent holds both mediums (§C.2); Patch Authorization Gate → Commit Executor → MEMIT → Git is deterministic, non-reasoning code (§12.2); the Commit Executor is the sole writer behind a FIFO at concurrency 1 (C-OR6); 2PC commits Git first, `.vindex` second, with an overlay hash in `COMMITTED` (§C.6); overlays accumulate as `incremental_NNNN.vindex`, tiered for independent rollback (§8.4); idle-window fires on no `PREPARED` for 30 min (§12.8). All three stubs are Genesis-shaped (one batch, N = 24); none tests the Incremental shape, where each hypothesis has to live.

### H-1 — shared z over canonical + two paraphrase forms

**Objections.**
1. The paraphrase forms are now write inputs, and the atomic unit has no slot for them: either the `.larql` grammar grows a per-fact paraphrase field the Coder authors (a reasoning agent shaping the parametric target), or the Commit Executor generates them, which breaks the §12.2 non-reasoning rule.
2. In production the held-out probe is the §8.9 L2 behavioural check drawn by the Validator from the same template family the Coder sees; the stub's "disjoint from the sealed templates" is an experimenter guarantee that the pipeline does not reproduce.
3. The per-patch compile cost rises with the prompt set inside `compute_z`; the stub's 35 min is a harness-pass number, not a per-overlay latency, and every `incremental_NNNN` pays it while holding the session lock at concurrency 1.
4. The paraphrase set is a new persistent artifact with no governance tier: if it is not committed to Git, compaction (§8.10) cannot rebuild the overlay it produced.

**Measurement or control.** (1) Name the field in the patch and the author of it; (2) log per-fact lexical overlap between training forms and held-out templates, generator blind to the probe set; (3) log `compute_z` wall time per fact, arm A vs B; (4) assign the tier and store the set with the overlay hash.

**In the stub?** (1) No. (2) Asserted, not measured. (3) No. (4) No.

### H-18 — minted row trained by embedding-only tuning

**Objections.**
1. A minted token changes the tokenizer for every runtime that touches text: Coder, TGA, Validator probes, the GGUF serving path; a Validator on the unextended tokenizer renders the id as bytes and its `code_pass_patch_fail` verdicts are void.
2. On this tied model the trained row is also the output row, so the overlay is an embedding/head delta, not a band ΔW; §8.4 independent rollback presumes the mount/unmount is a clean inverse, and that is untested.
3. Vocabulary becomes a function of the mount set: unmounting `incremental_0003` removes a token that `incremental_0004`'s text may tokenise through, so later overlays' probes change under earlier rollbacks.
4. The "few hundred steps on MPS" run inside the Commit Executor is not bit-reproducible (CLAUDE.md gate 2: cross-process weight reproduction does not hold on GPU), so a Git-ahead recovery cannot regenerate the `COMMITTED` overlay hash.

**Measurement or control.** (1) Tokenise the full probe set under every runtime's tokenizer and diff; (2) apply, unmount, assert bit-identical embedding matrix and 0/72 step-0 recall restored; (3) tokenisation stability of all mounted overlays after removing one; (4) two runs, same init seed, compare overlay hash and top-1 behaviour.

**In the stub?** (1) P2 233/233 and P4 24/24 cover one process and the GGUF chain, not an agent fleet: partial. (2) No. (3) No; P2 checks only the forward direction. (4) The two N seeds are init seeds, not re-run determinism: no.

### H-13 — merged band-LoRA write

**Objections.**
1. A gradient loop replaces the closed-form solve inside Phase 1; a 2–3 h stub (training included) means a `PREPARED` entry or session lock outlives the 30 min idle-window heuristic (§12.8) and serialises every write behind it at concurrency 1.
2. The write path must be deterministic (§12.2); a LoRA writer with early stop on training-phrasing EM has a data-dependent step count and MPS non-determinism, and it has no fingerprint at all — the stub's fingerprint is on the engine it does not use.
3. Sequential incremental overlays are each trained against a base that includes the earlier ones; unmounting `incremental_0003` while keeping `0004` yields weights `0004` was never trained on, so §8.4 independent rollback fails by construction unless deltas are stored unmerged.
4. The ~20 generated phrasings per fact are model output feeding the writer: same authorship fault as H-1 (1), and the generic-capability floor the Validator would need per patch (source: 57 → 40 with rank) is named but has no number.

**Measurement or control.** (1) Training wall time at N = 24 and at N = 1–5 per incremental patch, reported as lock hold time; (2) two same-seed runs, overlay hash + behavioural diff, plus a SHA on the LoRA writer; (3) train two sequential overlays, unmount the first, re-probe the second; (4) pre-set the capability floor as a number and name the phrasing author.

**In the stub?** (1) Aggregate hours only: no. (2) No. (3) No, Genesis shape only. (4) Floor named, not numbered; author unnamed.

### Common fault

All three stubs measure recall after one batch write on one process. None measures the two things the §C pipeline is built around: a reproducible overlay hash under 2PC, and independent unmount of one overlay among several. Until those two are in each stub, a pass tells F1 the write works once, not that it is a write the Commit Executor can own.
