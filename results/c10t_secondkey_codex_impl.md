# D-C10t-secondkey — model-free implementation report

Implemented the frozen v2 brief in `results/c10t_secondkey_codex_impl_brief.md` and `docs/C10T_SECONDKEY_PREREG.md`, including the complete §7 fold log. **40 stdlib-only selftests passed; all four new Python files passed `py_compile`.** No experimental step 0, real harness pass, model loading, torch import, GPU use, autoresearch/driver launch, model-based review, commit or push occurred.

The frozen prereg SHA-256 is `582896c6340e82f6e054f48dc43b801734ee27fc9b73654655bb7255a6b40070`. It was not edited. All 94 protected source files in the before/after snapshot are byte-identical, including the MEMIT engine, `c10e_bandknob.py`, `c10s_sharedz_*`, the autoresearch source tree, and the prereg. No CORPUS file or existing result was modified. No installed `/Volumes/memit/llm-database-poc-mirror/autoresearch_*` destination was modified, unlocked or deleted; this task did not operate on those destinations. The only workspace deliverables created by this task are the four files below and this new report. Test fixtures, captured output, snapshot and compiler caches are under `/private/tmp`.

Working directory/root and branch were verified at the beginning and again before this report: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, branch `worktree-c10k-route-a`. Git was used only for read-only root/branch/status queries.

## Files created

| File | Lines | SHA-256 |
| --- | ---: | --- |
| `experiments/track_c/c10t_secondkey_arms.py` | 572 | `93bb69875226e1e9b490aa09bd84b8b04cf9ad58c6b2647288e19e1f82c3e62b` |
| `experiments/track_c/c10t_secondkey_read.py` | 449 | `4dec4925360a6398c83b203bb42620c24ec4370ba046935c017004bb59dd12c7` |
| `experiments/track_c/c10t_secondkey_step0.py` | 184 | `bf4ff960222252efe97ab68a0e6388ee9d17c5c44e5f8f96c75b6ec9d71798e0` |
| `experiments/track_c/c10t_secondkey_selftest.py` | 628 | `7b1231f60106a123bd6883c46e5044e8dc4777c4a0b38e1ad717ff0eceb8b0b3` |

The arm file supplies shared stdlib utilities and the lazy runtime boundary; step 0 imports those utilities without importing the model. The reader owns every scientific threshold and label. The selftest imports all three new modules and asserts that `torch`, `transformers` and `c10e_bandknob` were never imported.

## Source reads and engine boundary

Before implementing against the engine/harness, I read the complete prereg, `c10e_bandknob.py` (including `my_edit`, `restore_layers`, `run_law5` and `run_recipe`), and the complete `compute_ks.py`, `compute_z.py`, `memit_main.py` and `memit_hparams.py` sources. The `memit/__init__.py` export shim was also inspected. I also read `rome/repr_tools.py`, the relevant `util/nethook.py` trace implementation, baseline hparams, and the cited keygram, frame-probe and residual sources. The c10s arms/inertness/reader/selftest patterns were consulted without modification. The existing advisor/design review records were consulted to resolve the leverage-mean interpretation; no new review model was invoked.

The implementation comments cite the frozen prereg's engine seams: `compute_ks.py:19–49`, `compute_z.py:41–73,95–99,127–128,149–178,185`, `rome/repr_tools.py:43–99`, `memit_main.py:240–280,304–316`, and `c10e_bandknob.py:181–221,415–446,458–509`. Numerical editing remains entirely in the original `H.my_edit`; there is no copied solver, no changed engine primitive, and no shared-z override.

## §2 implementation map

| Frozen element | Implementation and exact source anchor |
| --- | --- |
| Second request; canonical unchanged; blocked 24+24 order | `experiments/track_c/c10t_secondkey_arms.py:135` builds the extended subject and decodes the remainder directly, avoiding `req()`'s extra leading space. `experiments/track_c/c10t_secondkey_arms.py:144` emits all canonical requests first in FICTION order, then all second requests. Internal positions exclude 0 and n. |
| Tokenizer-only admission before optimisation | `experiments/track_c/c10t_secondkey_arms.py:149` checks exact prefix IDs, canonical rewriting text, truncated-input IDs, b+m−1 length, both lookup indices at b−1, input tokens beneath the shifted labels, standalone remainder retokenisation, intended keyed ID/decoded token, and the separate KL lookup. Each sampled context template is checked and recorded. `experiments/track_c/c10t_secondkey_arms.py:185` checks canonical intended tokens, including the distinct empty-prefix KL tokenisation. |
| Admission in every process; frozen positions never reselected | `experiments/track_c/c10t_secondkey_arms.py:200` rebuilds the published dictionaries with that process's tokenizer, repeats the audit using its own generated contexts, and records the 48-request population for every candidate. `experiments/track_c/c10t_secondkey_arms.py:477` refuses an admission failure before `run_recipe` or target optimisation; it does not choose another j. |
| Step 0(a), H-10 surprisal and both picks | `experiments/track_c/c10t_secondkey_step0.py:36` forwards each specified teacher-forced prompt string under the base model, recording all s_j. `experiments/track_c/c10t_secondkey_read.py:45` returns j*, address j*−1 and p10 from s_(j+1), with first-index ties. |
| Step 0(b), H-5 raw covariance and token classes | `experiments/track_c/c10t_secondkey_step0.py:18` classifies subject, frame, writable value 1..n−1, and final value n positions. `experiments/track_c/c10t_secondkey_step0.py:50` obtains every down_proj input without an edit. `experiments/track_c/c10t_secondkey_step0.py:61` reads the same raw second moment as `compute_P` and uses its float32 SVD. `experiments/track_c/c10t_secondkey_read.py:56` retains S≥0.005 for the protected-subspace inverse score; tiny singular values are never inverted. |
| H-5 accompanying geometry/stability readouts | `experiments/track_c/c10t_secondkey_step0.py:61` records kᵀΣ⁺k and ‖Pk‖²/‖k‖² per token/layer at 0.005 and 0.05. `experiments/track_c/c10t_secondkey_read.py:60` publishes raw five-layer means, unconstrained/internal picks, per-layer winner and margin, and the per-layer-max-normalised mean's winner/internal pick. Both cut selections and their agreement are recorded. |
| Step 0(c), spending, admission mapping, merge | `experiments/track_c/c10t_secondkey_read.py:98` drops a rule only above 12 non-writable unconstrained picks. Empty admission for any fact returns INVALID-ADMISSION without shrinking the population. `experiments/track_c/c10t_secondkey_read.py:92` uses distance then smaller j. Pre-admission agreement ≥20 merges surviving rules into B using p10 on disagreements; otherwise B10/B5 remain separate. Both agreements and every final j are published. |
| Step 0(d), cross-template overturning test | `experiments/track_c/c10t_secondkey_step0.py:98` records canonical-to-each-PTEST second-key and subject-key cosines for all facts/layers. `experiments/track_c/c10t_secondkey_read.py:146` compares pooled medians with ≤ and records H-T4 without stopping the run. |
| Step 0(e), published requests/overlap and hashes | `experiments/track_c/c10t_secondkey_step0.py:130` exclusively publishes all measurements, admission sets, final selections, 48 dictionaries per surviving arm, request digests, context templates and covariance-cache hashes in step0.json. `experiments/track_c/c10t_secondkey_read.py:129` records normalised shared words, trigrams and Jaccard overlap against PTEST; no overlap threshold was invented. The author-held-out-visibility limitation is recorded. |
| One harness pass; A1/A2/single/dup/candidate; same P and base snapshot | `experiments/track_c/c10t_secondkey_arms.py:477` supplies the ordered ARMS dictionary to the original `H.run_recipe`. The original loop computes P once and restores the same snapshot before every arm (`c10e_bandknob.py:462,473–474`). It retains all harness evaluation/locality/details/write-norm output and its unchanged LAW#5 gate. |
| Wrapper scope, duplicate control, substitution and hook audits | `experiments/track_c/c10t_secondkey_arms.py:213` recognises the exact canonical A7 target list, then consumes pinned single/dup/candidate order. A7-dup receives canonical+canonical. Controls and `_LAW5_DEFAULT_CTX` pass through untouched. The candidate substitution count is separate from the single duplicate-control substitution. The wrapper publishes the actual list into `_ARM_STATE['requests']`, records the digest/count handed to `my_edit`, and the hooks verify that list and every engine key/fit population. |
| Hook (a), F0 | `experiments/track_c/c10t_secondkey_arms.py:344` runs the six never-edited CANON subjects and records top-1 membership in any edited A7 value's first-token set on base, single, duplicate and each candidate. |
| Hook (b), F1: 24 prefixes × six subjects | `experiments/track_c/c10t_secondkey_arms.py:344` records per-prompt next-token and greedy full-remainder hits for each published prefix. `experiments/track_c/c10t_secondkey_arms.py:438` records newly induced next/full hits relative to the same base prompts. `experiments/track_c/c10t_secondkey_read.py:161` gates each prefix separately; `experiments/track_c/c10t_secondkey_read.py:351` reports the reference/candidate newly induced next/full counts beside the labels. |
| Hook (c), subject-free prefix | `experiments/track_c/c10t_secondkey_arms.py:344` uses exactly `The name is` plus the decoded prefix, with 24 next-token/full-remainder readouts per position rule on the same arms. |
| Hook (d), actual solve K, PK, cross-block and residuals | `experiments/track_c/c10t_secondkey_arms.py:418` returns the original `compute_ks` object unchanged, captures the first K call per layer at `my_edit:196`, and verifies the second/cache call. `experiments/track_c/c10t_secondkey_arms.py:297` implements the cited Gram statistics; `experiments/track_c/c10t_secondkey_arms.py:318` reports subject/second/joint blocks for raw K and PK plus own/other-subject cross cosines. Base and post-edit diagnostic 48-key geometries are also recorded. `experiments/track_c/c10t_secondkey_arms.py:373`, `experiments/track_c/c10t_secondkey_arms.py:429` and `experiments/track_c/c10t_secondkey_arms.py:438` record remaining-residual fractions at both keyed positions and gold-prefix held-out positions, including per-request, per-block and per-template readouts. The sign is fraction REMAINING. |
| Hook (e), naturally reached prefix | `experiments/track_c/c10t_secondkey_arms.py:344` generates freely from each held-out prompt for j tokens and checks the exact gold prefix; it does not inject a gold prefix. It records each fact/template hit, the 24-vector and /72 total. |
| Hook (f), bystander relations | `experiments/track_c/c10t_secondkey_arms.py:344` records top-1 on `{c} is a` and `{c} is associated with` for all 24 subjects. `experiments/track_c/c10t_secondkey_arms.py:438` pairs pre/post IDs, changed IDs and flips to edited first tokens. The record explicitly keeps the KL-lookup-token caveat. |
| Hook (g), per-request fit at stop | `experiments/track_c/c10t_secondkey_arms.py:258` reads the unmodified engine frame at return for nll, exp(−nll), per-context NLLs, kl_loss, loss/decay, loss-evaluation and Adam-step counts, initial/delta norms, KL lookup, and clamp-hit events at the engine's line 178. `experiments/track_c/c10t_secondkey_arms.py:408` records the exact request and KL prompt and returns the original target object unchanged. No rounded stdout parsing or re-solving is used. |
| Second process / gate A | `experiments/track_c/c10t_secondkey_arms.py:511` requires a valid pass 1 with at least one PARTIAL/LEAD, the identical positions-file bytes/hash and current source hashes, a fresh PID, no existing second attempt/output, and new process context admission. It writes an exclusive second_started.json before model loading, runs the same entire pass, and records a terminal second_halt.json on an exception. `experiments/track_c/c10t_secondkey_read.py:376` checks both processes' validity/locality/qualifiers and reports the counts and per-fact hit agreement. |

## §3 implementation map

All frozen threshold constants are declared in `experiments/track_c/c10t_secondkey_read.py:17–32`.

| Reading | Pure rule / implementation |
| --- | --- |
| INVALID precedence | `experiments/track_c/c10t_secondkey_read.py:211` verifies score-derived selections, population, admitted positions, blocked dictionaries/digests, overlap and the cosine-derived H-T4 reading. `experiments/track_c/c10t_secondkey_read.py:259` checks d941a9fb/_cov_cpu=3, LAW#5 including its numeric strict inequalities, A1/A2≥68, reference para [5,18] and canon [5,10], process admission, substitutions and zero Z_OVERRIDE hits, positions hash/identity, hook/fit/solve-key populations, aggregate/detail counts and required diagnostics. `experiments/track_c/c10t_secondkey_read.py:376` applies INVALID before replication labels. |
| Exact binding readout | `experiments/track_c/c10t_secondkey_read.py:199` emits three /24 counts, the 24-vector, the per-edge 3/3 vector/count and original rows. `experiments/track_c/c10t_secondkey_read.py:351` retains canon/full/first/string, teacher-forced continuation and P(full\|first) decomposition. `para_string_n == para_full_n` is a validity requirement for A7 arms. |
| LEAD / PARTIAL / TRADEOFF / NULL | `experiments/track_c/c10t_secondkey_read.py:174`: LEAD at ≥30 with locality; PARTIAL only at 18<count<30 and gain≥10 with locality; sized gain plus failed locality is TRADEOFF; otherwise NULL, including count≤18 regardless of gain. Unmerged arms are read separately against the same A7-single. |
| Locality | `experiments/track_c/c10t_secondkey_read.py:161`: L1≤ref+1; F0≤ref+1; all 24 F1 newly induced next-token gates≤reference newly induced+1; described_as≥ref−3; L3≥29; ppl≤ref+0.5. Full-remainder F1 results are reported without inventing another gate. |
| Qualifiers | `experiments/track_c/c10t_secondkey_read.py:187`: -LARGE-WRITE only above 1.5 for the summed per-layer norm ratio; -SUBJECT-FREE only above reference full-remainder hits+1/24; -REQUEST-COUNT when dup>18 and dup−single≥10. `experiments/track_c/c10t_secondkey_read.py:376` carries a qualifier when either process triggers it. |
| Replication | `experiments/track_c/c10t_secondkey_read.py:376`: a LEAD requires a second LEAD; a PARTIAL requires second PARTIAL or LEAD, gain≥10 and all gates. Failure yields LEAD-NOT-REPLICATED or PARTIAL-NOT-REPLICATED. Invalid process records override those labels. Started/HALTED/incomplete attempts are terminal INVALID, never silently treated as pending. |
| H-T1 interpretation | `experiments/track_c/c10t_secondkey_read.py:376` reports `H_T1_label_eligible` only for a replicated clean LEAD/PARTIAL without -REQUEST-COUNT/-SUBJECT-FREE, and prints naturally reached prefix counts plus the pre-run H-T4 record beside it. This field is label eligibility, not a claim that a scalar count proves causality or that an address was reached; the actual prefix evidence remains explicit. No F1/spec/route closure is claimed. |

The reader also checks the on-disk positions-file hash when invoked as a CLI. An occupied output is not overwritten to repair a failed run.

## Decisions where the prereg is silent or needs interpretation

1. **Leverage aggregate:** p5 is selected from the raw arithmetic mean over the five layers. The max-normalised mean is an accompanying alternative, not a replacement selector. This follows the v1 design review's five-layer-average description and v2's phrasing that the normalised winner is reported “beside” it. The raw and normalised winners are both explicit; no rank normalisation was introduced. Float32 covariance/SVD/coordinates follow the harness; scalar score/norm accumulations use float64. PK share is evaluated with the SVD basis action, without storing another dense P in step 0.
2. **Surprisal spending address:** j* indexes the surprised target token, and its key address is j*−1. Thus j*=1 counts as non-writable frame; j*=n still addresses internal token n−1. Counting j*=n as a final-value *key* would contradict the pinned s_(j+1) selector. No fact is keyed at token 0 or n.
3. **One surviving rule:** when the other rule is dropped, the surviving rule remains B10 or B5; a dropped rule is not revived through the agreement merge. Empty admissible sets take INVALID-ADMISSION precedence even if both rules would otherwise be dropped.
4. **Canonical token audit:** the expected subject token is computed with the engine's template-specific word preprocessing. An empty-prefix canonical KL row does not receive the leading-space preprocessing of a nonempty-prefix CANON/context row (`repr_tools.py:66–70`). The first selftest caught and corrected an assumption that those IDs must be globally identical. The second-key KL audit still requires the exact intended value-token ID.
5. **Wrapper counts:** there is one audited A7-dup control substitution plus exactly one candidate substitution per B/B10/B5 arm. The §3 candidate count excludes the duplicate control, which is checked separately. The wrapper recognises targets as prescribed and also requires the unchanged canonical prompt/subject dictionaries, refusing unexpected order/calls instead of guessing an arm name.
6. **Identity/output lifecycle:** the run identity originates in step0.json and includes all four new modules, harness, frozen prereg/hparams/screens/fingerprint tool and every vendored engine Python file. First/second processes compare the full manifest and digest before model import and again before publishing a pass. run.json is an immutable initial record; exclusive second_started.json/second_halt.json replace in-place state rewrites so occupied files are never overwritten. The normal halt file is this arm's `architecture_profile/c10t_secondkey_halt_diagnostic.json`; if it already exists, an additional UUID-suffixed diagnostic preserves it rather than overwriting it.
7. **Replication of unmerged arms:** if either arm earns PARTIAL/LEAD, process 2 repeats the full ordered pass, including both candidates and the controls. Each arm retains its own first-process disposition; a first-process NULL is never promoted by a better second-process number.
8. **Geometry and undefined ratios:** actual A7-single solve K has 24 columns; A7-dup solve K has 48 duplicated subject columns; candidate solve K has the prescribed 24+24 columns. They are labelled as such, while diagnostic 48 subject+value-key sets are computed for base and every A7 post-state. Zero PK columns/zero residual denominators are reported explicitly as undefined (`None`), without a fabricated cosine or residual. A zero summed reference write norm makes the ratio/readout invalid. Held-out second-key residuals/cosines use a gold prefix and are explicitly proxies; natural reach is measured separately.
9. **Cross-template median:** pool all 24 facts × five layers × three held-out templates for the overall second/subject median, while publishing every layer/template/fact pair. Identity-template direct keys are used for this transfer comparison; actual solve K remains the engine's context-type-averaged K.
10. **CLI and output boundary:** `H.run_recipe`, rather than `H.main`, supplies the real unchanged arm loop. This prevents the historical harness's `open(OUT, "w")` from overwriting a stage file and avoids its unrelated legacy verdict. The standing stimulus-leak stop is retained with its threshold owned by the reader; all harness metrics/details and LAW#5 are retained. All inherited harness knobs are refused, not only the four called out at the end of §2, to keep the frozen model/revision/N/hparams and templates.

## Prereg concerns and limits — reported, not silently changed

**I-INFER / ambiguity:** v2 publishes a normalised five-layer winner but does not state the primary aggregate in one explicit equation. The raw mean interpretation above is consistent with the retained design review; a different choice is a different position rule, not an implementation “fix.” The j* boundary-versus-address distinction also needs to be read exactly as above to avoid incorrectly spending-screening the final internal boundary.

**I-INFER / mechanism:** -REQUEST-COUNT removes the H-T1 reading when the duplicate itself crosses the specified bar, but failure to cross that bar is not a proof that request-count/ridge effects contribute nothing to the candidate. The second-request KL anchor is also an objective change. The implementation preserves both engine objectives and records their KL terms/anchors; it does not claim these controls uniquely establish causal direct addressing. A LEAD remains the scoped mechanism/configuration lead defined by the prereg.

**I-INFER / data provenance:** covariance-cache hashes are recorded in step 0 and every harness recipe. The frozen validity paragraph specifies source/fingerprint/position/overlap gates but does not prescribe equality of covariance-cache bytes across processes; no additional covariance-equality scientific gate was silently added. The operator/reviewer can compare the recorded hashes before interpreting the protected-subspace selector and solve geometry.

**UNVERIFIABLE here / cost and hardware:** “step 0 minutes” and the approximately 35-minute pass estimate were not tested. Step 0 includes full covariance SVDs, and the duplicate/unmerged targets plus the F1, subject-free, free-prefix and geometry hooks add work. The code has not been exercised against the pinned real tokenizer/model/device stack; real tokenizer admission, LAW#5, numerical telemetry inertness, fit, keygram/residual values, runtime, locality and replication remain runtime evidence gates. No model-free synthetic record is presented as experimental evidence. The leverage heuristic's relation to editability and ManiEdit's own definition remain unverified as the prereg says.

No existing CORPUS labels, shared-z/solvefeas result, engine path, read/governance/deployment layer, or F1 determination was changed.

## Verification performed

Final selftest command (exit 0):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/private/tmp/c10t_secondkey_final_testcache python3 experiments/track_c/c10t_secondkey_selftest.py
```

The 40 tests cover tokenizer admission using the actual AST-extracted engine word-index function, canonical/KL handling, exact request ordering, no double space, rule spending/merge/ties/empty sets, protected-subspace cut equality, raw versus normalised picks, standing H-T4/no-stop, wrapper passthrough and both candidate layouts, all label/locality/qualifier boundaries, record tampering/identities/populations, per-fact replication agreement, second-process validity/locality/permanent-attempt handling, exclusive JSON persistence/reread and halt ownership, transitive source changes, pre-import knob refusals, and read-only fit tracing/restoration. The actual `req`/`run_recipe` AST is exercised with deterministic stubs for effects to verify one shared P, fresh caches, restoration before all arms and 48 requests reaching the hook. This is a model-free source-level seam test, not a real harness/driver run.

Compile command (exit 0; no stdout/stderr):

```sh
PYTHONPYCACHEPREFIX=/private/tmp/c10t_secondkey_final_compilecache python3 -m py_compile experiments/track_c/c10t_secondkey_arms.py experiments/track_c/c10t_secondkey_step0.py experiments/track_c/c10t_secondkey_read.py experiments/track_c/c10t_secondkey_selftest.py
```

Additional final checks: all 94 protected before/after source hashes matched; all four new files had no trailing whitespace; root/branch remained as stated. No structural moves occurred, so GPU reproducibility gate C was not invoked under the brief's hard limit. The final deliverable is implementation and this report, not an experimental close-out or promotion.

## Selftest output verbatim

```text
test_all_internal_positions_and_sampled_templates (__main__.TestAlignment) ... ok
test_overlap_report_does_not_select_positions (__main__.TestAlignment) ... ok
test_prefix_retokenisation_rejected (__main__.TestAlignment) ... ok
test_request_block_order_and_no_double_space (__main__.TestAlignment) ... ok
test_wrong_lookup_and_separate_KL_rejected (__main__.TestAlignment) ... ok
test_current_source_hashes_gate_and_transitive_changes (__main__.TestPersistence) ... ok
test_exclusive_write_and_reread (__main__.TestPersistence) ... ok
test_halt_has_own_path_and_preserves_prior_diagnostic (__main__.TestPersistence) ... ok
test_runtime_knobs_refused_before_model_import (__main__.TestPersistence) ... ok
test_empty_admission_population_never_shrinks (__main__.TestSelection) ... ok
test_leverage_raw_mean_and_normalised_alternative (__main__.TestSelection) ... ok
test_merge_on_pre_admission_agreement (__main__.TestSelection) ... ok
test_nearest_admission_tie_and_empty (__main__.TestSelection) ... ok
test_overturning_equal_is_standing_not_stop (__main__.TestSelection) ... ok
test_protected_cut_includes_equality (__main__.TestSelection) ... ok
test_spending_boundary_and_single_survivor (__main__.TestSelection) ... ok
test_surprisal_boundary_and_ties (__main__.TestSelection) ... ok
test_failed_solve_removes_trace (__main__.TestTelemetry) ... ok
test_read_only_frame_observation_returns_same_target (__main__.TestTelemetry) ... ok
test_all_locality_gate_boundaries (__main__.TestVerdict) ... ok
test_changed_published_requests_or_selector_are_invalid (__main__.TestVerdict) ... ok
test_each_prefix_gate_uses_new_hit_sets_not_totals (__main__.TestVerdict) ... ok
test_each_validity_failure_is_detected (__main__.TestVerdict) ... ok
test_invalid_admission_stops_without_pass (__main__.TestVerdict) ... ok
test_label_boundaries_and_locality_tradeoff (__main__.TestVerdict) ... ok
test_lead_needs_lead_in_second_process (__main__.TestVerdict) ... ok
test_missing_or_stale_second_is_invalid_and_no_retry (__main__.TestVerdict) ... ok
test_partial_second_may_be_lead_but_still_needs_gain (__main__.TestVerdict) ... ok
test_per_fact_agreement_and_direct_address_qualification (__main__.TestVerdict) ... ok
test_qualifier_strict_boundaries (__main__.TestVerdict) ... ok
test_second_process_locality_and_qualifiers_apply (__main__.TestVerdict) ... ok
test_unmerged_candidates_are_labelled_separately (__main__.TestVerdict) ... ok
test_valid_fixture_and_replication_pending (__main__.TestVerdict) ... ok
test_validity_precedes_every_replication_label (__main__.TestVerdict) ... ok
test_LAW5_and_controls_pass_through (__main__.TestWrapper) ... ok
test_actual_harness_recipe_ast_restores_base_and_uses_one_P (__main__.TestWrapper)
Actual run_recipe/req source, deterministic stubs for effects. No ... ok
test_override_and_extra_A7_call_refused (__main__.TestWrapper) ... ok
test_single_dup_and_second_reach_real_seam_and_hook (__main__.TestWrapper) ... ok
test_target_match_does_not_accept_changed_canonical_prompt (__main__.TestWrapper) ... ok
test_unmerged_wrapper_substitutes_each_candidate_once (__main__.TestWrapper) ... ok

----------------------------------------------------------------------
Ran 40 tests in 0.511s

OK
C10T_SECONDKEY_SELFTEST_DONE (stdlib only; no model/torch/GPU/driver)
```


## Fix round 1

Status: DONE — B1, B2, B3 and the three requested advisories implemented. The complete `results/c10t_secondkey_advisor_impl.md` was read; the final four-file diff was read after verification. This section supersedes earlier implementation descriptions of `runtime()`, string/full equality and the observer gate; the original report above is preserved byte for byte.

### B1 — preflight before permanent stage markers

`experiments/track_c/c10t_secondkey_arms.py:108` now provides model-free `preflight(root)`: all inherited harness knobs are refused before the existing engine-fingerprint subprocess. Model loading moved to `load_harness(root, out_dir, fingerprint)` at `experiments/track_c/c10t_secondkey_arms.py:124`. `arms.py:553` calls preflight after source/step-0 validation and before either `run.json` (`arms.py:560`) or `second_started.json` (`arms.py:575`); harness loading occurs afterwards at `arms.py:577`. Step 0 follows the same split at `experiments/track_c/c10t_secondkey_step0.py:142` and `:143`, before publication.

Selftests: `TestPersistence.test_stale_knob_leaves_no_stage_markers` (`experiments/track_c/c10t_secondkey_selftest.py:637`) exercises first, second and step-0 entry points with a stale `OUT`; all permanent output markers remain absent and the harness loader is never called. `test_fingerprint_failure_leaves_no_stage_markers` (`selftest.py:641`) proves the same for fingerprint failure. `test_preflight_knobs_refused_before_model_import` (`selftest.py:613`) also covers inherited empty values. These calls use synthetic files and blocked harness loading, without an operator driver run or model import.

### B2 — report string/token discrepancy, retain row consistency

`experiments/track_c/c10t_secondkey_read.py:330` retains only the consistency check between `para_string_n` and its own `para_string_hits` rows; equality with `para_full_n` no longer gates validity. `read.py:387` reports `string_minus_full` beside the binding readout and decomposition. The binding token-ID count and the frozen label thresholds are unchanged.

Selftest: `TestVerdict.test_extra_string_hit_is_reported_without_changing_label` (`experiments/track_c/c10t_secondkey_selftest.py:457`) adds one coherent extra string hit to A7-single, A7-dup and the candidate. Validity remains clean, the candidate binding count remains 32, the discrepancy is +1, and the LEAD label remains unchanged in both the first-pass and replicated readings. The existing `test_each_validity_failure_is_detected` still rejects an aggregate string count inconsistent with its rows.

### B3 — observer inertness gate at both request loci

`experiments/track_c/c10t_secondkey_arms.py:305` adds `observer_inertness`: on the first canonical and the first second-key request, call the original `H.compute_z` twice without the trace and once through `observe_solve`, with the same model, tokenizer, hparams, final solve layer and sampled contexts. It measures `floor = ||a-b|| / ||a||` and `observed_rel = ||c-a|| / ||a||` in float32, following the review code. The pure reader rule at `experiments/track_c/c10t_secondkey_read.py:41` requires finite nonnegative values and `observed_rel <= max(10 * floor, 1e-4)`.

The gate runs at `arms.py:510` before collector instrumentation is installed at `arms.py:521`; its two rows are recorded as `observer_inertness` at `arms.py:531`. Failure raises before any arm run and reaches the existing stage HALT path. `read.py:287` requires both expected request loci, checks their recorded tolerance against the pure rule, and rejects missing, failed or inconsistent inertness evidence before labels.

Selftests: `TestTelemetry.test_observer_floor_rule_includes_both_tolerance_boundaries` (`experiments/track_c/c10t_secondkey_selftest.py:749`) checks inclusive absolute/noise-floor boundaries and immediate failures above them, plus non-finite values. `test_observer_inertness_runs_three_solves_at_each_locus` (`selftest.py:756`) exercises the actual tracing wrapper on a synthetic solve and verifies the six calls, their request order, final layer, unchanged context object and trace cleanup. `test_observer_inertness_uses_measured_noise_floor` (`selftest.py:765`) admits an observed difference above 1e-4 when it is within 10 times the measured floor. `test_observer_inertness_failure_stops_and_clears_trace` (`selftest.py:770`) verifies refusal. `TestVerdict.test_observer_inertness_is_a_validity_gate` (`selftest.py:472`) checks missing, partial, failed, wrong-locus and numerically inconsistent evidence.

Caveat: these are synthetic, model-free checks. Actual engine observer inertness has not been measured in this task; the new six-solve gate must establish it in each future operator-invoked pass before that pass proceeds.

### Advisory (a) — INVALID-ADMISSION is a recorded outcome

Step 0 publishes the preregistered selection and returns exit 0 at `experiments/track_c/c10t_secondkey_step0.py:178`. The first driver stage records `run.json`, prints the terminal outcome and returns 0 without loading the harness at `experiments/track_c/c10t_secondkey_arms.py:561`. Thus normal INVALID-ADMISSION no longer triggers the nonzero-exit HALT handlers; the reader still labels it INVALID-ADMISSION.

Selftests: `TestPersistence.test_invalid_admission_first_records_outcome_without_halt` (`experiments/track_c/c10t_secondkey_selftest.py:679`) and `test_invalid_admission_step0_publishes_outcome_without_halt` (`selftest.py:696`) verify the published outcome, exit 0 and absence of HALT, with all measurement/model effects stubbed or blocked.

### Advisory (b) — root provenance and resolved HALT destination

Both entry points resolve `LLMDB_ROOT` and assert it equals the script's own repository root before preflight or model import: `experiments/track_c/c10t_secondkey_arms.py:544` and `experiments/track_c/c10t_secondkey_step0.py:137`. The resolved root is retained as `RUN_ROOT`. Both exception handlers explicitly pass it to `halt()` (`arms.py:598`, `arms.py:600`, `step0.py:187`, `step0.py:189`), so a harness `os.chdir` cannot relocate a diagnostic under a relative root. `halt()` itself defaults to the resolved root at `arms.py:55`.

Selftests: `TestPersistence.test_script_root_mismatch_refused_before_preflight` (`experiments/track_c/c10t_secondkey_selftest.py:645`) and `test_halt_resolved_root_survives_working_directory_change` (`selftest.py:654`) verify refusal and the diagnostic destination after a synthetic engine-directory change.

### Advisory (c) — D-C10t-p5rule in run identity

The ruling is recorded verbatim in `program_rulings`: **D-C10t-p5rule: p5 is selected from the raw five-layer mean** (`experiments/track_c/c10t_secondkey_read.py:13`, `experiments/track_c/c10t_secondkey_arms.py:88`). Identity matching, source validation and step-0 validity retain that ruling (`read.py:214`, `read.py:222`, `arms.py:92`). The leverage selector code is unchanged; the maximum-normalised mean remains a separately reported alternative. The prereg was not edited.

Selftests: `TestPersistence.test_current_source_hashes_gate_and_transitive_changes` checks that newly created identities contain the ruling; `test_p5_ruling_is_required_in_frozen_identity` (`experiments/track_c/c10t_secondkey_selftest.py:670`) refuses a missing or changed ruling. `TestSelection.test_leverage_raw_mean_and_normalised_alternative` (`selftest.py:163`) retains the raw-versus-normalised selection proof.

### Verification and scope

- Python 3.11.16: model-free selftest **53/53 PASS**, exit 0. The selftest checks that torch, transformers and the live harness were never imported.
- `PYTHONPYCACHEPREFIX=/private/tmp/c10t_secondkey_fix1_compile .venv/bin/python -m py_compile experiments/track_c/c10t_secondkey_arms.py experiments/track_c/c10t_secondkey_read.py experiments/track_c/c10t_secondkey_step0.py experiments/track_c/c10t_secondkey_selftest.py`: exit 0; no output. Compiled bytecode was placed outside the repository.
- `/usr/bin/git diff --check`: exit 0; no output. Final source diff reviewed.
- SHA-256 comparison: all 94 protected sources/artifacts are unchanged, including the engine, harness, C10s and autoresearch sources, hparams and prereg. The prereg remains `582896c6340e82f6e054f48dc43b801734ee27fc9b73654655bb7255a6b40070`.
- Fix-round edits are confined to the four C10t Python files and this appended report section. The requested new marker is `results/c10t_secondkey_fix1_done.md` with the single line `53 selftests: PASS`.
- A concurrent program change to `EXPERIMENT_RUNBOOK.md` records the same D-C10t-p5rule; it was observed in the final git diff. This fix round did not edit or revert that file.
- No model/GPU run, live experiment driver run, commit, push, installed-destination edit, unlock or deletion occurred.

| Updated source | SHA-256 |
| --- | --- |
| `experiments/track_c/c10t_secondkey_arms.py` | `5fbc37a7e9518cd1f66b299c7ae801f35f999983686cf28cf3657c2e40005aac` |
| `experiments/track_c/c10t_secondkey_read.py` | `be71a5a1e3660e35e34aaa28f96e76679b49911fa77e43bc17fae7d838bab337` |
| `experiments/track_c/c10t_secondkey_step0.py` | `fa6af30e77cbb13a5bbc6e690d2127e970906a913ca41dee8f5c45528500892f` |
| `experiments/track_c/c10t_secondkey_selftest.py` | `b4620a823c350d8b31588e8711b0dff3c0a44d7bd4966d996b920d04e7cfea2a` |

### Selftest output (verbatim)

```text
test_all_internal_positions_and_sampled_templates (__main__.TestAlignment.test_all_internal_positions_and_sampled_templates) ... ok
test_overlap_report_does_not_select_positions (__main__.TestAlignment.test_overlap_report_does_not_select_positions) ... ok
test_prefix_retokenisation_rejected (__main__.TestAlignment.test_prefix_retokenisation_rejected) ... ok
test_request_block_order_and_no_double_space (__main__.TestAlignment.test_request_block_order_and_no_double_space) ... ok
test_wrong_lookup_and_separate_KL_rejected (__main__.TestAlignment.test_wrong_lookup_and_separate_KL_rejected) ... ok
test_current_source_hashes_gate_and_transitive_changes (__main__.TestPersistence.test_current_source_hashes_gate_and_transitive_changes) ... ok
test_exclusive_write_and_reread (__main__.TestPersistence.test_exclusive_write_and_reread) ... ok
test_fingerprint_failure_leaves_no_stage_markers (__main__.TestPersistence.test_fingerprint_failure_leaves_no_stage_markers) ... ok
test_halt_has_own_path_and_preserves_prior_diagnostic (__main__.TestPersistence.test_halt_has_own_path_and_preserves_prior_diagnostic) ... ok
test_halt_resolved_root_survives_working_directory_change (__main__.TestPersistence.test_halt_resolved_root_survives_working_directory_change) ... ok
test_invalid_admission_first_records_outcome_without_halt (__main__.TestPersistence.test_invalid_admission_first_records_outcome_without_halt) ... ok
test_invalid_admission_step0_publishes_outcome_without_halt (__main__.TestPersistence.test_invalid_admission_step0_publishes_outcome_without_halt) ... ok
test_p5_ruling_is_required_in_frozen_identity (__main__.TestPersistence.test_p5_ruling_is_required_in_frozen_identity) ... ok
test_preflight_knobs_refused_before_model_import (__main__.TestPersistence.test_preflight_knobs_refused_before_model_import) ... ok
test_script_root_mismatch_refused_before_preflight (__main__.TestPersistence.test_script_root_mismatch_refused_before_preflight) ... ok
test_stale_knob_leaves_no_stage_markers (__main__.TestPersistence.test_stale_knob_leaves_no_stage_markers) ... ok
test_empty_admission_population_never_shrinks (__main__.TestSelection.test_empty_admission_population_never_shrinks) ... ok
test_leverage_raw_mean_and_normalised_alternative (__main__.TestSelection.test_leverage_raw_mean_and_normalised_alternative) ... ok
test_merge_on_pre_admission_agreement (__main__.TestSelection.test_merge_on_pre_admission_agreement) ... ok
test_nearest_admission_tie_and_empty (__main__.TestSelection.test_nearest_admission_tie_and_empty) ... ok
test_overturning_equal_is_standing_not_stop (__main__.TestSelection.test_overturning_equal_is_standing_not_stop) ... ok
test_protected_cut_includes_equality (__main__.TestSelection.test_protected_cut_includes_equality) ... ok
test_spending_boundary_and_single_survivor (__main__.TestSelection.test_spending_boundary_and_single_survivor) ... ok
test_surprisal_boundary_and_ties (__main__.TestSelection.test_surprisal_boundary_and_ties) ... ok
test_failed_solve_removes_trace (__main__.TestTelemetry.test_failed_solve_removes_trace) ... ok
test_observer_floor_rule_includes_both_tolerance_boundaries (__main__.TestTelemetry.test_observer_floor_rule_includes_both_tolerance_boundaries) ... ok
test_observer_inertness_failure_stops_and_clears_trace (__main__.TestTelemetry.test_observer_inertness_failure_stops_and_clears_trace) ... ok
test_observer_inertness_runs_three_solves_at_each_locus (__main__.TestTelemetry.test_observer_inertness_runs_three_solves_at_each_locus) ... ok
test_observer_inertness_uses_measured_noise_floor (__main__.TestTelemetry.test_observer_inertness_uses_measured_noise_floor) ... ok
test_read_only_frame_observation_returns_same_target (__main__.TestTelemetry.test_read_only_frame_observation_returns_same_target) ... ok
test_all_locality_gate_boundaries (__main__.TestVerdict.test_all_locality_gate_boundaries) ... ok
test_changed_published_requests_or_selector_are_invalid (__main__.TestVerdict.test_changed_published_requests_or_selector_are_invalid) ... ok
test_each_prefix_gate_uses_new_hit_sets_not_totals (__main__.TestVerdict.test_each_prefix_gate_uses_new_hit_sets_not_totals) ... ok
test_each_validity_failure_is_detected (__main__.TestVerdict.test_each_validity_failure_is_detected) ... ok
test_extra_string_hit_is_reported_without_changing_label (__main__.TestVerdict.test_extra_string_hit_is_reported_without_changing_label) ... ok
test_invalid_admission_stops_without_pass (__main__.TestVerdict.test_invalid_admission_stops_without_pass) ... ok
test_label_boundaries_and_locality_tradeoff (__main__.TestVerdict.test_label_boundaries_and_locality_tradeoff) ... ok
test_lead_needs_lead_in_second_process (__main__.TestVerdict.test_lead_needs_lead_in_second_process) ... ok
test_missing_or_stale_second_is_invalid_and_no_retry (__main__.TestVerdict.test_missing_or_stale_second_is_invalid_and_no_retry) ... ok
test_observer_inertness_is_a_validity_gate (__main__.TestVerdict.test_observer_inertness_is_a_validity_gate) ... ok
test_partial_second_may_be_lead_but_still_needs_gain (__main__.TestVerdict.test_partial_second_may_be_lead_but_still_needs_gain) ... ok
test_per_fact_agreement_and_direct_address_qualification (__main__.TestVerdict.test_per_fact_agreement_and_direct_address_qualification) ... ok
test_qualifier_strict_boundaries (__main__.TestVerdict.test_qualifier_strict_boundaries) ... ok
test_second_process_locality_and_qualifiers_apply (__main__.TestVerdict.test_second_process_locality_and_qualifiers_apply) ... ok
test_unmerged_candidates_are_labelled_separately (__main__.TestVerdict.test_unmerged_candidates_are_labelled_separately) ... ok
test_valid_fixture_and_replication_pending (__main__.TestVerdict.test_valid_fixture_and_replication_pending) ... ok
test_validity_precedes_every_replication_label (__main__.TestVerdict.test_validity_precedes_every_replication_label) ... ok
test_LAW5_and_controls_pass_through (__main__.TestWrapper.test_LAW5_and_controls_pass_through) ... ok
test_actual_harness_recipe_ast_restores_base_and_uses_one_P (__main__.TestWrapper.test_actual_harness_recipe_ast_restores_base_and_uses_one_P)
Actual run_recipe/req source, deterministic stubs for effects. No ... ok
test_override_and_extra_A7_call_refused (__main__.TestWrapper.test_override_and_extra_A7_call_refused) ... ok
test_single_dup_and_second_reach_real_seam_and_hook (__main__.TestWrapper.test_single_dup_and_second_reach_real_seam_and_hook) ... ok
test_target_match_does_not_accept_changed_canonical_prompt (__main__.TestWrapper.test_target_match_does_not_accept_changed_canonical_prompt) ... ok
test_unmerged_wrapper_substitutes_each_candidate_once (__main__.TestWrapper.test_unmerged_wrapper_substitutes_each_candidate_once) ... ok

----------------------------------------------------------------------
Ran 53 tests in 0.555s

OK
C10T_SECONDKEY_SELFTEST_DONE (stdlib only; no model/torch/GPU/driver)
```
