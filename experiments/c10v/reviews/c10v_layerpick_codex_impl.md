# D-C10v-layerpick v2 — implementation report

**Implementation model:** GPT-6 (Codex, the session-provided identity). **Effort:** the runtime effort setting is not exposed to this agent; no more specific setting is asserted. **Independent implementation reviewer:** `gpt-6-astra`, `high`, fresh-context, read-only. **Date:** 2026-10-07. **Decision:** `D-C10v-layerpick`. **Implementation handoff:** DONE; first full selftest run green. **Experiment status:** UNVERIFIED / NOT RUN; no live LAW#3, LAW#5, selector, model, tokenizer, torch, MPS or GPU evidence was produced.

Task authority: `/Users/robertrhu/.claude/jobs/4d71207f/tmp/codexb_c10v_impl_brief.md`, frozen `docs/C10V_LAYERPICK_PREREG.md` v2, and the binding operator addendum requiring a prereg-derived test list before code, JSON-normalised roundtrips, threshold boundaries, HALT tests and the complete green suite output. `CLAUDE.md` and `DISCIPLINE.md` were read before implementation; dependent engine and harness sources were read with line numbers before writing the seam. This work prepares the step-4 H-8 test of the write path; it does not change F1 or any scientific verdict.

## Created files and SHA-256

Only these three source files and this named report were created in the worktree. No tools launcher was needed. Temporary plan, audit and output captures live under `/private/tmp`; synthetic test records are written in temporary directories and removed by their fixtures.

| File | SHA-256 of the complete source file |
| --- | --- |
| `experiments/track_c/c10v_layerpick_arms.py` | `83f54e523a23bccc321db26694b52877325eba6d08dbf46e6c8110e3c4e05e27` |
| `experiments/track_c/c10v_layerpick_read.py` | `54f083f64ad3c4980b49179b151b01940fe62b8d7e11759ef28d1287669f3f8a` |
| `experiments/track_c/c10v_layerpick_selftest.py` | `21ce699b6dcd34309055b7917114482b821f0afc99b49a12474f1b8af258d72a` |

The fourth file is `results/c10v_layerpick_codex_impl.md` (this report). Its complete-file SHA-256 is measured after writing and rereading it; it cannot contain its own complete-file hash without changing that hash. The three source hashes above identify the implementation actually tested. Later `identity.json` additionally freezes the prereg, hparams, screens, prior rho record, harness, mint helper, globals configuration, fingerprint tool and all vendored engine Python files.

The driver is 589 lines, reader 449 lines, and selftest 878 lines. It reuses the existing `compute_z`, `compute_ks`, `compute_P`, `my_edit`, `run_recipe`, evaluation and locality primitives. The only independent algebra is the prereg's small CPU proxy/HSIC calculation and numerical comparison; no engine write solver was reimplemented. Driver imports and `--help` remain model-free; the reader uses the standard library only.

## LAW#4 source reads and the seams they support

The following sources were read with line numbers before seam code. Ranges identify the contract used, rather than reconstructed signatures.

| Numbered source | Contract used |
| --- | --- |
| `experiments/track_c/c10e_bandknob.py:18–48` | Frozen env defaults, model/revision, fp16/MPS load boundary, ridge 1 and projector threshold 0.005. |
| `experiments/track_c/c10e_bandknob.py:67–97` | Target IDs and leading-space `(subject, target_new.str)` convention. |
| `experiments/track_c/c10e_bandknob.py:150–221` | Exact snapshot/restore, projector construction, override seam, update and cache semantics. |
| `experiments/track_c/c10e_bandknob.py:342–400` | Covariance file hashes, full/first/string and teacher-forced evaluation output shapes. |
| `experiments/track_c/c10e_bandknob.py:403–509` | `_LAW5_DEFAULT_CTX`, `Z_OVERRIDE`, hooks, original standing LAW#5 and one `run_recipe` call per recipe. |
| `experiments/track_c/c10e_bandknob.py:555–599` | `C10_RECIPES=candidate` and CLI-only persistence. The driver calls functions and never enters that harness main block. |
| `memit_dry_run/memit/memit/compute_z.py:14–21,76–95,127–128,188–231` | Actual target-solve signature, layer-specific pristine z, objective-anchored KL prompt, activation extraction signature. |
| `memit_dry_run/memit/memit/compute_ks.py:11–50` | Context-averaged, target-blind subject keys and returned row orientation. |
| `memit_dry_run/memit/memit/memit_main.py:101–169,240–284,304–323` | All z solved before writes, original ascending recomputation, covariance cache, process context cache. |
| `experiments/track_c/c10q_stacked_arms.py:13–15,47–65`; `c10q_stacked_read.py:1–79` | Inherited-knob refusal, fixed shift, complete override keys and exact-count precedent. |
| `experiments/track_c/c10l_mint_lib.py:1–185` (notably `:162–163`) | Existing tensor digest primitive; no helper changes. |
| `experiments/track_c/c10l_covgeom_step0.py:74–75,134–137` | Remaining-residual ratios and the corrected installed share `1 - rho_c`. |
| `experiments/track_c/c10p_twopass_arms.py:30–42` | Six canonical-frame never-edited subjects and edited-first-token membership definition. |
| `experiments/track_c/c10m_diag_arms.py:72–77` | Pristine, layer-8 A7 targets for diagnostic residuals. |
| `experiments/track_c/c10u_mint2_arms.py:45–54` and its identity/stage/HALT portions; predecessor reader/selftest | Exclusive creation, source identity, stage gates and the tuple roundtrip defect deliberately corrected. |
| `configs/hparams/qwen25_3b_memit_hparams.json:1–22`; engine `util/globals.py`, `globals.yml`, `util/device.py`; `tools/engine_fingerprint.py:31–48` | Frozen hp fields, actual path/device resolution and full fingerprint/cov-site gate. |

## Preregistration to implementation and tests

Here `arms.py`, `read.py` and `selftest.py` mean the new `experiments/track_c/c10v_layerpick_*.py` files, respectively. All references are to the final hashed source.

| Prereg section / numbered criteria | Implementation file:line | Verification file:line |
| --- | --- | --- |
| §§0–1, lines 7–18: corrected remaining rho, hypotheses and bounded claim | `arms.py:165–192`; `read.py:319–385` | `selftest.py:236–243,341–352,407–419` |
| §2, lines 22–28: unchanged engine, hp, source and harness seams | `arms.py:69–144,260–303` | `selftest.py:284–339,632–678,866–870`; static fingerprint below |
| §2 step 0, lines 30–36: five-layer pristine keys, `G`, norm cells, two computations, measured delta, margined repeat map, concentration and published tables | `arms.py:152–192,475–507`; `read.py:68–108` | `selftest.py:236–261,564–630,818–840` |
| §2 HSIC, line 38: layer-8 A7 residuals, Gaussian median kernels, centered biased HSIC, contributions and agreement | `arms.py:195–220,532–540`; `read.py:257–273` | `selftest.py:263–277,564–630` |
| §2 arms, lines 40–45: A, B0=8, published B, size-preserving Bshuf; no C | `read.py:55–65`; `arms.py:503–531` | `selftest.py:284–318,473–477` |
| §2 execution 1–5, lines 47–52: pristine assigned-layer z for every arm, descending groups, hp-only layer change, exact `P[layer-4]`, zero cache, per-group full overrides, original bypass | `arms.py:238–303,430–467` | `selftest.py:284–339,649–658` |
| §2 proxy readouts, line 54: A1/A7 canonical plus three prompt ratios with own pristine denominators, realised dot fraction, full/group G predictions before writes, fp16 and layer norms | `arms.py:223–257,407–467`; `read.py:171–249` | `selftest.py:236–243,341–352,564–630` |
| §2 controls/probes, line 56: both controls under every recipe, six frame subjects, two explicitly labelled relation probes | `arms.py:394–404,430–467`; `read.py:171–218` | `selftest.py:354–357,379–419,564–630` |
| §2 LAW#5 (i)–(v), line 58: standing original path; original duplicate floor; active full-band identity; one request at layer 8; two largest groups versus independent lone writes | `arms.py:306–391`; `read.py:124–154` | `selftest.py:304–339,479–496,619–630,749–765,809–816` |
| §2 cell order, line 60: step0 then LAW#5, A/B0/B/Bshuf in one process, conditional fresh pass2, fixed published map and template hashes | `arms.py:475–555`; `read.py:360–431` | `selftest.py:429–477,680–718,720–807,818–864` |
| §3 validity first, lines 64–66: full fingerprint and cov sites, all LAW#5, repeat map, A1/A2≥68 per recipe, A envelope, overrides, tables/hashes, aggregate string equality | `read.py:95–154,157–294`; `arms.py:83–121,503–549` | `selftest.py:379–390,479–496,564–678,720–807` |
| §3 binding count, line 68: /72, three templates, 24-vector, 3/3 edge and layer cross-tabulation | `read.py:157–168,319–357` | `selftest.py:361–368,370–390` |
| §3 labels, lines 69–72: LEAD≥30; PARTIAL>18, gain≥10,<30; sized gate miss TRADEOFF; other NULL | `read.py:319–357` | `selftest.py:370–419` |
| §3 locality/write, line 74: L1, frame, described_as, L3, PPL and ratio1.5 boundaries; relation flips reported only | `read.py:324–340` | `selftest.py:392–419` |
| §3 attribution/replication/readings, lines 76–78: both ≥10 margins; fresh-process validity/locality/count/write gates; no shuffled adoption; layer counts, Spearman and prediction errors | `read.py:341–385`; `arms.py:483–548` | `selftest.py:279–282,421–477,842–864` |
| §4, line 82: no broader closure or historical verdict edits | `read.py:384–385`; no canonical document edits | Source preservation audit below |
| §5, line 86: operator go, paused/finished, steps1–3; HALT diagnostics and future closeout | `arms.py:35–121,558–585` | `selftest.py:500–562,632–678,720–864`; closeout is future experiment work |
| §§6–7, lines 90–104: implementation review, B0/Bshuf, numeric inertness, rho correction, C deferred, limited scientific claims | The union of the rows above, especially `arms.py:331–391`; this review record | First full suite green below; independent static PROCEED |
| Operator addendum: every persisted JSON kind exclusive write/read, JSON-normalised tuple regression, thresholds and HALT paths | `arms.py:35–55`; every persist call uses that writer | `selftest.py:500–540,542–864`; full persisted-chain positive control |

## Test list recorded before source code

The prereg-derived list was written to `/private/tmp/c10v_layerpick_test_plan.md` before any new source code, then refined with the approach review before implementation. Its verbatim contents follow. This is the test-first evidence; the table above links the implemented tests to it.

# D-C10v-layerpick v2 — test list derived before code

Source: docs/C10V_LAYERPICK_PREREG.md numbered §§0–7; binding program addendum.
No experiment model/tokenizer/torch/GPU imports in selftests. Synthetic numpy linear algebra and harness fixtures only. Tests do not mint live gate evidence.

1. §2 Step0 (lines30–36): G=S(I+S)^-1 against an independent d-dimensional solve; singleton coefficient; projected-key norms; finite shapes; measured delta=max absolute repeated diagonal change; winner margins below/at/above delta; exact ties nearest8; reproducible/nonreproducible repeat maps; population24 and layers4..8; concentration19/20/21; stopped records retain full tables/context/hash/installed-share comparison. HALT/refusal for malformed selector, inconsistent fixed map, malformed contexts, missing sources.
2. §2 Arms and wrapper (40–52): A None-map and LAW5 bypass; active full-band identity; B0 all8; B fixed; Bshuf i+1 preserving sizes and changed-assignment count; descending8..4; skip empties; all targets solved before first write; assigned-layer compute_z; leading-space override keys present per group; P index layer-4; all other hp fields unchanged; fresh zero cache per group; exact hit count per arm. HALT for missing map subjects, bad layer set, incomplete target keys, inconsistent projector/hp, incorrect hit counts.
3. §2 Readouts (38,54–56,60): HSIC Gaussian median distances/centering/(n-1)^2; per-fact contributions and agreement; degenerate median explicitly diagnosed without selector gating; canonical and 3 paraphrase remaining ratios with own pristine denominators; realized fraction and full/group G prediction error; fp16 qualifier; A1+A7 both; frame edited-token membership vs relation pre/post changes; objective-anchored vs bystander labels; full/first/string/teacher-forced/conditional fields; exact per-template and 3/3 edge vectors and assigned-layer counts; tied-rank Spearman (constant input explicitly undefined).
4. §2 LAW5 (58): standing expr below/at/above0.05 and loc below/at/above3; measured duplicate floor and tolerance=max(1e-4,10floor); relative update distances below/at/above tolerance; active behavioral equality required even when duplicate floor nonzero; singleton layer8 numeric comparison; two-largest-groups vs independent restored lone writes; wrong projector/order faults detected. HALT separately for i,ii,iii,iv,v and gate records never fabricated from counters.
5. §3 Validity (64–68): full pinned fingerprint d941a9fb and cov sites2/3/4; source/identity/context/map hash mismatch or missing; nonfinite numeric fields; map repeat mismatch; each recipe A1/A2 at67/68/69; recipe A para4/5/6/17/18/19 and canon4/5/6/9/10/11; override expected-1/equal/expected+1; full-string exact equality/mismatch; shapes24x3, counts0..72 and duplicate/missing subjects; INVALID precedence over TRADEOFF. HALT before novel recipe for each failed live validity gate, and before markers for LAW3/LAW5/preflight failures.
6. §3 Labels (69–72): count18/19,29/30/31; gain9/10/11 outside envelope; inside[5,18] always NULL; LEAD does not require a further gain test; qualifying gain with failed locality/write-size =>TRADEOFF; every threshold has at/inside/outside tests.
7. §3 Locality and write (74): L1 A+0/+1/+2 of12; frame A+0/+1/+2 of6; described_as A-3 +/-epsilon; L3 28/29/30; generic PPL A+0.5 +/-epsilon; norm ratio1.5 +/-epsilon; relation flips reported not gated; LARGE-WRITE suffix and no gateA adoption; NULL-LARGE-WRITE retained when no qualifying gain.
8. §3 Attribution and replication (76–78): B vs B0 and Bshuf margins9/10/11 individually; invalid comparator cannot credit selector; pass2 required only for PARTIAL/LEAD B or B0; separate PID; pinned published map executed despite recomputed cross-process disagreement; same source identity and context hashes recorded; failed second validity/locality/count/write gates =>NOT-REPLICATED and no adoption; lead repeat must reach LEAD; partial may improve to LEAD; no pass2 =>pending NOT-REPLICATED; Bshuf reported but never causes replication/adoption alone.
9. §5 + brief safety: missing operator go / steps1–3 completion / paused-or-finished window; inherited harness knobs; occupied output including dangling symlink; root/worktree mismatch; engine fingerprint command fail/empty/wrong shape; missing/malformed LAW3 reference; source drift; stage dependency/hash/marker mismatch; output write/read corruption; exceptions persist HALT diagnostic with JSON-safe full state. No state-changing git. No stage marker before live baseline and LAW5 gates. CLI help and imports do not load model modules.
10. Every persisted JSON kind gets exclusive write/read roundtrip against JSON-normalised objects (nested tuple regression): identity.json, step0.json (ready/stopped), law5.json, law5_pass2.json, pass1.json, pass2.json, pass1_started.json, pass1_complete.json, pass2_started.json, pass2_complete.json, run.json (stopped/no-replication/replicated), architecture_profile/c10v_layerpick_halt_diagnostic*.json. Existing JSON preserved; NaN refused; persisted bytes verified.

Acceptance: smallest three-file implementation satisfying these requirements; run .venv/bin/python -B experiments/track_c/c10v_layerpick_selftest.py entirely green; paste full output into results/c10v_layerpick_codex_impl.md; cite source and prereg/code file:line; include SHA256, later stage commands, stage time estimates, honest unverified runtime gates, implementation resolutions and open questions. DONE only afterwards.

Additional reviewer cases before code: pass2 recomputed concentrated but reproducible map must not suppress running the published diverse map; in-process nonreproducible recomputation remains INVALID. Different pass2 context templates permitted but hashed. LEAD->PARTIAL replication fails; PARTIAL->LEAD succeeds when other gates hold; attribution must also survive pass2 for selector adoption. Step0 stop writes step0+run and no LAW5/started markers. Literal prereg line60 schedules pass2 for qualifying B or B0 even when B attribution fails; adoption remains separately forbidden per78.


## Complete first-run selftest output

Exact suite command (the outer shell used `/opt/homebrew/bin/rtk proxy`; Python `-B` suppresses bytecode creation):

```sh
.venv/bin/python -B experiments/track_c/c10v_layerpick_selftest.py
```

Exit 0. The first complete execution passed all 34 tests, including subtests for every listed prereg threshold and gate. A small standard-library capture wrapper ran exactly that subprocess and saved its combined stdout/stderr to `/private/tmp/c10v_layerpick_selftest_output.txt`; total capture wall time was 1.698 seconds. No implementation change was made after this suite run. Entire captured suite output:

```text
test_complete_persisted_chain_positive_control_and_every_chain_gate_halt (__main__.SafetyAndPersistenceTests.test_complete_persisted_chain_positive_control_and_every_chain_gate_halt) ... ok
test_every_record_kind_json_normalised_roundtrip_and_exclusive (__main__.SafetyAndPersistenceTests.test_every_record_kind_json_normalised_roundtrip_and_exclusive) ... ok
test_every_validity_gate_routes_to_halt_diagnostic (__main__.SafetyAndPersistenceTests.test_every_validity_gate_routes_to_halt_diagnostic) ... ok
test_import_and_help_never_import_model_modules (__main__.SafetyAndPersistenceTests.test_import_and_help_never_import_model_modules) ... ok
test_json_nonfinite_corruption_and_each_io_failure (__main__.SafetyAndPersistenceTests.test_json_nonfinite_corruption_and_each_io_failure) ... ok
test_law5_layer_coverage_and_missing_floor_observations (__main__.SafetyAndPersistenceTests.test_law5_layer_coverage_and_missing_floor_observations) ... ok
test_occupied_dangling_symlink_bad_maps_and_wrapper_keys_halt (__main__.SafetyAndPersistenceTests.test_occupied_dangling_symlink_bad_maps_and_wrapper_keys_halt) ... ok
test_preflight_gate_halts_and_never_loads_harness (__main__.SafetyAndPersistenceTests.test_preflight_gate_halts_and_never_loads_harness) ... ok
test_real_pass2_runs_published_map_despite_concentrated_reselection (__main__.SafetyAndPersistenceTests.test_real_pass2_runs_published_map_despite_concentrated_reselection) ... ok
test_real_stage_dependency_selector_source_and_candidate_halts (__main__.SafetyAndPersistenceTests.test_real_stage_dependency_selector_source_and_candidate_halts) ... ok
test_real_stage_each_law5_failure_suppresses_recipes_and_markers (__main__.SafetyAndPersistenceTests.test_real_stage_each_law5_failure_suppresses_recipes_and_markers) ... ok
test_real_stage_order_law5_and_baseline_before_any_marker (__main__.SafetyAndPersistenceTests.test_real_stage_order_law5_and_baseline_before_any_marker) ... ok
test_real_step0_stops_publish_table_without_law5_or_markers (__main__.SafetyAndPersistenceTests.test_real_step0_stops_publish_table_without_law5_or_markers) ... ok
test_source_and_law3_identity_gates_halt (__main__.SafetyAndPersistenceTests.test_source_and_law3_identity_gates_halt) ... ok
test_stopped_output_no_law5_no_markers_and_pending_chain (__main__.SafetyAndPersistenceTests.test_stopped_output_no_law5_no_markers_and_pending_chain) ... ok
test_actual_numeric_law5_and_order_projector_fault_sensitivity (__main__.SelectorAndNumericalTests.test_actual_numeric_law5_and_order_projector_fault_sensitivity) ... ok
test_concentration_19_20_21_and_nonreproducible (__main__.SelectorAndNumericalTests.test_concentration_19_20_21_and_nonreproducible) ... ok
test_frame_membership_and_relation_labels (__main__.SelectorAndNumericalTests.test_frame_membership_and_relation_labels) ... ok
test_hsic_formula_contributions_and_degenerate_diagnostic (__main__.SelectorAndNumericalTests.test_hsic_formula_contributions_and_degenerate_diagnostic) ... ok
test_map_none_and_law5_bypass_and_active_band_identity (__main__.SelectorAndNumericalTests.test_map_none_and_law5_bypass_and_active_band_identity) ... ok
test_margin_delta_below_at_above_and_nearest8_tie (__main__.SelectorAndNumericalTests.test_margin_delta_below_at_above_and_nearest8_tie) ... ok
test_proxy_matches_independent_full_solve_and_singleton (__main__.SelectorAndNumericalTests.test_proxy_matches_independent_full_solve_and_singleton) ... ok
test_proxy_uses_own_pristine_denominators_and_fp16_qualifier (__main__.SelectorAndNumericalTests.test_proxy_uses_own_pristine_denominators_and_fp16_qualifier) ... ok
test_spearman_ties_and_constant (__main__.SelectorAndNumericalTests.test_spearman_ties_and_constant) ... ok
test_wrapper_groups_targets_hparams_projectors_and_fresh_cache (__main__.SelectorAndNumericalTests.test_wrapper_groups_targets_hparams_projectors_and_fresh_cache) ... ok
test_attribution_9_10_11_against_each_control (__main__.ThresholdTests.test_attribution_9_10_11_against_each_control) ... ok
test_complete_fixture_and_per_template_edge_reading (__main__.ThresholdTests.test_complete_fixture_and_per_template_edge_reading) ... ok
test_controls_and_baseline_envelope_boundaries (__main__.ThresholdTests.test_controls_and_baseline_envelope_boundaries) ... ok
test_count_and_gain_boundaries (__main__.ThresholdTests.test_count_and_gain_boundaries) ... ok
test_each_locality_threshold_inside_at_outside (__main__.ThresholdTests.test_each_locality_threshold_inside_at_outside) ... ok
test_law5_strict_thresholds_floor_and_relative_tolerance (__main__.ThresholdTests.test_law5_strict_thresholds_floor_and_relative_tolerance) ... ok
test_replication_rules_fresh_context_fixed_map_and_loss_of_attribution (__main__.ThresholdTests.test_replication_rules_fresh_context_fixed_map_and_loss_of_attribution) ... ok
test_replication_schedule_and_never_adopt_shuffled (__main__.ThresholdTests.test_replication_schedule_and_never_adopt_shuffled) ... ok
test_write_ratio_and_relation_report_only (__main__.ThresholdTests.test_write_ratio_and_relation_report_only) ... ok

----------------------------------------------------------------------
Ran 34 tests in 1.549s

OK
C10V_LAYERPICK_SELFTEST_PASS: synthetic only; torch/transformers/tokenizers/model imports absent
```

Tests are synthetic instrumentation evidence. The synthetic linear solver is deliberately a test fixture, not a substitute for the frozen engine's live LAW#5 audit. It includes distinct projectors and a shallower-write/deeper-activation dependency, so deliberately wrong projector and ascending-order variants fail the production numerical comparison. Failure-routing tests call the actual production gate functions and HALT handler; separate actual `runtime_stage` tests verify the marker and downstream execution order. They do not confer live baseline or inertness evidence.

## Other checks and independent review

All three sources parsed successfully without imports or bytecode writes. Driver and reader `--help` exited 0 inside the selftest; the suite asserted the absence of `torch`, `transformers`, `tokenizers` and `c10e_bandknob` from its imported modules.

Static, model-free engine check:

```sh
LLMDB_ROOT="$PWD" .venv/bin/python -B tools/engine_fingerprint.py
```

Exit 0, exact output:

```text
engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py
  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a…)
  _cov_cpu 3  (expected 3)
```

An out-of-family Claude approach review was attempted using `tools/claude_advisor.sh` under the repo's [advisor-review contract](../.codex/skills/advisor-review/SKILL.md). It returned exit 3, `FATAL: Claude Code is not logged in.` No Claude review was claimed. The authorized fallback was a fresh-context GPT-6-Astra/high read-only reviewer: weaker family independence than Claude, explicitly disclosed. It reviewed the approach, then the actual three source artifacts and returned **PROCEED to the model-free selftest and implementation handoff**, with no remaining static blocking defect. Its final checks included selector/pristine targets (`arms.py:152–192,238–257`), grouping (`:266–302`), numeric LAW#5 (`:311–391`), baseline-before-marker/candidate stopping (`:503–531`), reader/source/proxy/chain integrity and the actual-stage failure tests. It did not load model modules or claim live scientific validation. Any verdict/promote review required by prereg line 86 remains required after real results.

## Implementation decisions for textual ambiguities

1. **Margin and ties** (`prereg:33`): delta is measured globally across repeated diagonal cells; margin equality qualifies. Exact argmax ties choose the tied layer nearest 8. A margin below delta falls back to 8, following the band's z-layer wording. This is not a chosen numerical threshold.
2. **Baseline A and pristine readout targets** (`prereg:41,48,51,54,58`): a None map delegates the original `my_edit` untouched, using its existing `Z_OVERRIDE` seam to pin the same layer-8 pristine targets measured by the readout. The standing LAW#5 sets `_LAW5_DEFAULT_CTX` and bypasses all wrapper/target substitution with zero override hits. The active full-band identity check actually executes one full-band group, rather than treating None as proof of that new path.
3. **Largest groups and tolerance** (`prereg:58`): equal-size groups break ties toward the higher layer; execution remains descending. The relative update denominator uses a positive numerical floor for zero-reference norm; a changed zero update is correspondingly large. The duplicate floor records all five distances and both exact behavioral count differences. The tolerance is `max(1e-4,10*floor)`; active behavioral equality stays exact even if the duplicate behavioral floor is nonzero.
4. **LARGE-WRITE naming** (`prereg:71,74,101`): a PARTIAL/LEAD-sized count with ratio>1.5 reads `TRADEOFF-LARGE-WRITE`, implementing the explicit write-size gate-miss rule at line 71. The fold log's `LEAD-LARGE-WRITE` example conflicts with that rule; `count_label` retains the underlying LEAD/PARTIAL-sized count for auditing. NULL with ratio>1.5 retains `NULL-LARGE-WRITE`. No LARGE-WRITE reading passes gate A.
5. **Frame “flip”** (`prereg:56`, source `c10p_twopass_arms.py:36–42`): frame flips mean post-edit top-1 membership in the edited values' first-token IDs, matching the actual predecessor. Relation flips are pre/post top-1 changes, recorded separately. `"is a"` is explicitly objective-anchored.
6. **Second process schedule versus adoption** (`prereg:60,76,78`): any final PARTIAL/LEAD on B or B0 schedules a second process, including an unattributed B, following the literal cell rule. Adoption still requires attribution for B in both processes. A first-process LEAD must repeat as LEAD; a PARTIAL can repeat PARTIAL or improve to LEAD. Fresh templates are permitted and hashed. A fresh reproducible but concentrated or disagreeing selector does not replace or suppress the published diverse map; a within-process map mismatch remains INVALID. The pass2 record reports agreement and states that it replicates a fixed map, not the selection procedure.
7. **HSIC/ratio degeneracy** (`prereg:38,54,76`): a zero median distance yields an explicit undefined diagnostic, never a selector gate or invented bandwidth. Zero pristine ratio denominators produce JSON nulls and explicit indices, not nonfinite JSON numbers. Constant Spearman input is explicitly null. Integrity/shape checks still require the diagnostic record.
8. **String equality** (`prereg:66`): the binding equality is exact aggregate full-string count/percentage versus full-token count/percentage. Individual string hit vectors are recorded; no additional per-row equality gate was invented.
9. **Historical LAW#3 reference** (brief's c10u convention; `prereg:66`): accept the explicit `baseline` recipe, or an unambiguous sole recipe, requiring full band, standing LAW#5 and exact A1/A2≥68. The earlier `results/c10q_stacked/passS.json` is a concrete eligible reference: sole recipe `A7_stacked`, full band, A1 70/72, A2 71/72, A7 canonical8/24 and para12/72, reference SHA-256 `102163c6dab328007e2bb879e433c0df6045bf73f718548abac569995002ffd6`. The historical reference is a preflight check; the C10V same-process A and all new LAW#5 checks still must run before a started marker. No rounded historical score was reconstructed as an exact count.
10. **Stage safety** (brief plus `prereg:60,86`): LAW#5 and the live A are included at the start of both pass1 and pass2. `law5.json` is a data record, not a started marker; it can exist when the later live A fails, with no started/complete marker. Occupied stage outputs, including dangling symlinks, are refused. A pending replication has no terminal `run.json`; a stopped selector publishes step0/run but no LAW#5 or pass marker. No speculative repair occurs automatically after a live failure.

## Exact later stage commands

These are handoff commands, **not executed in this implementation session**. Use them only after the program has concluded steps 1–3, the operator has given go for step4, and autoresearch is actually paused or finished (`prereg:7,86`). Flags record those operator facts; they are not permission granted by this report. This worktree remains the runtime root so the hashed sources match. Run each stage as its own new Python process. The known historical reference above is pinned during identity creation; later drift is refused.

Common shell setup in the authorized program session:

```sh
C10V_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
cd "$C10V_ROOT"
```

Step0, no weight edit (loads the model and computes pristine keys/projectors):

```sh
env LLMDB_ROOT="$C10V_ROOT" "$C10V_ROOT/.venv/bin/python" -B \
  "$C10V_ROOT/experiments/track_c/c10v_layerpick_arms.py" step0 \
  --root "$C10V_ROOT" --law3-ref "$C10V_ROOT/results/c10q_stacked/passS.json" \
  --operator-go --steps-1-3-complete --autoresearch-state paused
```

If step0 prints READY, pass1 performs numeric LAW#5 and same-process A before any started marker, then B0/B/Bshuf with all controls/readouts:

```sh
env LLMDB_ROOT="$C10V_ROOT" "$C10V_ROOT/.venv/bin/python" -B \
  "$C10V_ROOT/experiments/track_c/c10v_layerpick_arms.py" pass1 \
  --root "$C10V_ROOT" --law3-ref "$C10V_ROOT/results/c10q_stacked/passS.json" \
  --operator-go --steps-1-3-complete --autoresearch-state paused
```

Only if the pass1 reading says `replication_needed: true`, launch pass2 as a fresh process:

```sh
env LLMDB_ROOT="$C10V_ROOT" "$C10V_ROOT/.venv/bin/python" -B \
  "$C10V_ROOT/experiments/track_c/c10v_layerpick_arms.py" pass2 \
  --root "$C10V_ROOT" --law3-ref "$C10V_ROOT/results/c10q_stacked/passS.json" \
  --operator-go --steps-1-3-complete --autoresearch-state paused
```

Read the stopped result or completed pass records without model imports:

```sh
env LLMDB_ROOT="$C10V_ROOT" "$C10V_ROOT/.venv/bin/python" -B \
  "$C10V_ROOT/experiments/track_c/c10v_layerpick_read.py" \
  "$C10V_ROOT/results/c10v_layerpick" --root "$C10V_ROOT"
```

Replace `paused` with `finished` only when that is the actual autoresearch state. Inherited knobs named at `arms.py:17–19` are refused, including model/hparam/output/context/device/recipe overrides; resolve the owning program environment before launch. Every output is exclusive-create. After any HALT, preserve that run and its diagnostic; a later specifically authorized retry can use a fresh subdirectory via `--out-dir "$C10V_ROOT/results/c10v_layerpick/<new-run-id>"` consistently for all stages and reader. Do not erase/reuse old records. No separate `law5` stage is exposed because its evidence belongs to the same live pass process.

Expected runtime record inventory:

- `identity.json`: immutable run ID and source/reference digests.
- `step0.json`: both tables/norms/margins, measured delta, context list/hash, fixed map and stop status; stop additionally writes `run.json`.
- `law5.json`, `pass1_started.json`, `pass1.json`, `pass1_complete.json`: first-process proof, post-gate marker, all four recipes and completion hash.
- `law5_pass2.json`, `pass2_started.json`, `pass2.json`, `pass2_complete.json`: conditional fresh-process proof and results.
- `run.json`: terminal stopped/no-replication/replicated reading only; pending pass1 replication remains a reader-produced NOT-REPLICATED reading, without a terminal file.
- Any HALT: exclusively named `architecture_profile/c10v_layerpick_halt_diagnostic_<uuid>.json`, exception/state and latest captured solve stdout; no completion marker for the failed stage.

## Time estimates and open runtime questions

| Stage | Estimate and basis |
| --- | --- |
| Model-free full selftest | Measured 1.549 seconds in the suite; capture/process wall time 1.698 seconds. |
| Step0 | Prereg line60 says minutes. Budget roughly 5–30 minutes including model load and covariance/projector work; cold covariance/SVD cost is unmeasured here and could exceed that estimate. |
| LAW#5 at the start of each pass | Additional repeated band writes, evaluation, singleton and two-group controls plus pristine target solves. Allow roughly 30–90 minutes as an unmeasured planning estimate; do not treat it as a benchmark or timeout gate. |
| Pass1, four recipes | Prereg line60: 35–60 minutes per recipe, hence 140–240 minutes for the four recipes, plus the live gate/startup overhead above. |
| Conditional pass2 | Same four-recipe and gate estimate; fresh process/model/templates, fixed published map. |
| Reader | Model-free; normally seconds, subject to source-file reads. Not benchmarked. |

Open experimental questions are deliberately still open: whether the selector concentrates or repeats; whether the original numeric floor/active identity/singleton/multigroup checks are INERT on real MPS/fp16 writes; whether live A falls inside its envelope; whether each recipe preserves controls; whether group predictions survive composed shallower interference; whether B/B0 gains, locality, write size, attribution and fresh-process replication pass. Cached covariance paths come from the unchanged engine `globals.yml`, including its main-clone absolute paths; actual covariance file hashes are recorded and must agree across recipes and processes. No model or tokenizer was loaded to verify cache availability or runtime compatibility. A missing/drifting runtime dependency is a HALT, not permission to modify the engine.

After real results, the program still needs verdict review, any LEAD promote review, the CORPUS/ledger/runbook closeout and `tools/closeout_check.py D-C10v-layerpick` (prereg line86). They are not implementation checks and were not invoked or represented as passed here. This report contains the session handoff; canonical checkpoint/context/memory files were left to their owning program session under the task's no-existing-file-edits rule.

## Workspace preservation audit

At entry and at handoff, `git rev-parse --show-toplevel` identified this exact worktree and `git branch --show-current` returned `worktree-c10k-route-a`. No mutating git command was run. `README.md` was already modified at entry and was left intact.

An initial byte-digest snapshot covered 1,543 tracked regular files. At the handoff check, **139 relevant existing engine/prereg/harness/helper/config/source files matched their entry digests** (`C10V_ENGINE_PREREG_DEPENDENCY_PRESERVATION_PASS`), including the frozen C10V prereg and vendored engine. No existing file was edited by this implementation session.

The workspace-wide unchanged assertion did **not** pass: seven non-C10V paths differed from the initial snapshot while this work ran. This is reported as observed drift, without claiming the whole shared worktree remained unchanged or assigning an unverified actor. None was restored, overwritten or cleaned up:

- `EXPERIMENT_RUNBOOK.md`
- `SESSION_CHECKPOINT.md`
- `docs/C10U_MINT2_PREREG.md`
- `docs/INTEGRATED_QUEUE_2026-10-07.md`
- `experiments/track_c/c10u_mint2_read.py`
- `experiments/track_c/c10u_mint2_selftest.py`
- `results/research_pass_2026-10-06/recommended_sequence.md`

No `results/c10v_layerpick/` experiment directory exists at handoff. The only worktree artifacts authored for this task are the three new C10V sources and this report. The successful Graft lookup ran with `GRAFT_NO_REFRESH=1`, `GRAFT_NO_GITIGNORE=1`, `GRAFT_NO_IGNORE=1`; no upgrade was performed. Reported Graft savings: approximately 45,557 tokens, one successful call (one earlier failed executable lookup), no dollar figure provided.
