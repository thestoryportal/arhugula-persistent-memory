"""Write the D-ML-1 build audit from saved evidence; stdlib only."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

W = Path(__file__).resolve().parents[2]
S = W / "results/mathlab_staging"
EXPECTED = "33e5aa4e0fc01e07e5b1b7e6fe234e07be41e9c9b2c8edf9496af5572d9b398a"
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert sha(W / "docs/MATHLAB_PREREG.md") == EXPECTED
scope = json.loads((S / "protected_scope.json").read_text())
baseline = json.loads(Path("/private/tmp/mathlab_build_protected_start.json").read_text())
(S / "protected_start.json").write_text(json.dumps(baseline, indent=2) + "\n")
scope["utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
scope["protected_changes"] = [
    dict(path=name, before=before, after=sha(W/name) if (W/name).is_file() else None)
    for name, before in baseline.items()
    if (sha(W/name) if (W/name).is_file() else None) != before
]
refs = {}
for name, item in scope["owned_files"].items():
    path = W/name
    item.update(sha256=sha(path), lines=len(path.read_text().splitlines()))
    if path.suffix == ".py":
        tree = ast.parse(path.read_text())
        refs[name] = {n.name: n.lineno for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
scope["events_integration_sha256"] = sha(W/"tools/mathlab_events.py")
scope["events_integration_matches_initial_shared_hash"] = scope["events_integration_sha256"] == "c295f131b7d1cbd1f5b0df28770588c728debcc17ae9f51364ce5dec2bc96b82"
(S/"protected_scope.json").write_text(json.dumps(scope, indent=2) + "\n")
(S/"source_references.json").write_text(json.dumps(refs, indent=2) + "\n")
status = subprocess.run(["git", "status", "--short"], cwd=W, capture_output=True, text=True, check=True).stdout
(S/"git_status_final.txt").write_text(status)

T = "mathlab/test_mathlab.py"
H = "tools/mathlab_harvest.py"
C = "mathlab/core.py"
R = "tools/mathlab_runtime.py"
A = "tools/mathlab_admit.py"
U = "tools/mathlab_cpu_runner.py"
def ref(file, symbol):
    return file + ":" + str(refs[file][symbol])
def tests(*names):
    return "; ".join(ref(T, n) + " (" + n.removeprefix("test_") + ")" for n in names)
def impl(file, *names):
    return "; ".join(ref(file, n) + " (" + n + ")" for n in names)

rows = [
("§0:15–21; §5:263", "MATH-PROXY labels; no behavioural promotion; prospective utility UNVERIFIED",
 tests("test_fixture_reproduction_then_calibration_uses_fresh_column_and_real_events"), impl(C,"calibration","run_notebook"), "CPU fixture PASS; science unrun"),
("§1:25–40", "Source-backed sequential projected ridge solve, L2=1, fp32 solve",
 tests("test_fp32_projector_and_solve_are_exact_and_fp64_diagnostic_only"), impl(C,"solve","projector"), "CPU PASS"),
("§2.1:75–80", "Separate model-free pre-import admission; explicit W/LLMDB_ROOT; only two reused gate functions",
 tests("test_harvest_launcher_refuses_before_dispatch","test_clean_cpu_admission"), "tools/run_mathlab_harvest.sh:3; "+impl(A,"probe","dispatch_check"), "Shell/CPU PASS; model-free import PASS"),
("§2.1:81; §6:274–281", "Harvest has no tail exception; both named terminal references/SHA and lead queue statement",
 tests("test_harvest_requires_both_terminal_status_hashes_and_queue_statement"), impl(A,"decide","status_reference"), "Fixture PASS; no lead clearance inferred"),
("§2.2:85–89", "Literal frozen s0 /ctx, both digests, identical contexts, restoration and inherited-context refusal",
 tests("test_context_pin_restores_after_body_error_and_detects_drift","test_frozen_record_and_target_hashes_are_bound","test_missing_authoritative_s0_context_refuses_shared_input"), impl(H,"frozen_records","lab_pinned_contexts","harvest"), "CPU/static PASS; live pin UNVERIFIED"),
("§2.2:90; §2.4:146", "Fresh A1/A2/A7 through run_recipe baseline, fresh measured counts, LAW#3 before mint",
 tests("test_law3_counts_and_stage_order","test_fixture_reproduction_then_calibration_uses_fresh_column_and_real_events"), impl(H,"baseline_gates","fresh_before_mint","harvest"), "Fixture/static PASS; real baseline UNVERIFIED"),
("§2.2:91–93,109–112", "Seed record/step0/target SHA and relative per-layer replay norm <=1e-3; seed-only failure",
 tests("test_frozen_record_and_target_hashes_are_bound","test_missing_seed_target_or_step0_is_seed_specific_source_failure","test_shared_failure_invalidates_all_and_per_arm_failure_only_one"), impl(H,"frozen_records","norm_agreement","replay_admission"), "CPU PASS; replay norm agreement UNVERIFIED"),
("§2.2:94–108", "Tokenizer ID/REV/files, original register, original audit_prompts/P2, exact 396/2376 and substring lookup",
 tests("test_pinned_tokenizer_identity_ignores_transient_batch_settings_without_mutation","test_p2_enumerated_fields_accept_wordlist_metadata_but_not_count_or_rows","test_shared_failure_invalidates_all_and_per_arm_failure_only_one"), impl(H,"tokenisation_contract","p2_equivalent","lookup_contract"), "Routing/identity-unit PASS; full historical tokenizer contract UNVERIFIED"),
("§2.2:99; §2.5:154–158", "Five audit source hashes before writer calls; full engine/harness source unchanged",
 tests("test_source_snapshot_covers_engine_primitives_and_detects_changes"), impl(H,"source_snapshot","tokenisation_contract","harvest"), "CPU/static PASS; fresh-process before/after source gate UNVERIFIED"),
("§2.3:117–133", "Original edit/shape code identities frozen before rebound; exact immediate-caller and one return match",
 tests("test_original_code_matches_after_rebinding_and_return_is_unique","test_shape_call_from_unrelated_code_is_ignored"), impl(H,"EditObserver","profile","bound"), "CPU AST harness-body PASS"),
("§2.3:125–131", "LAW#5 tagged before 24-subject check, exactly ordered five captures; 0/4/6/order/return failures halt",
 tests("test_law5_tag_precedes_24_subject_assertion_and_discards_tensors","test_capture_counts_0_4_6_wrong_order_and_missing_return_halt","test_preexisting_profile_refusal_and_exception_cleanup"), impl(H,"profile","validate_coverage","call"), "CPU PASS; harness LAW#5 UNVERIFIED"),
("§2.3:133–135", "Native operands, zero ca/hash/norm, Pi count/hash/four seeded probes; full update only A7",
 tests("test_science_subject_mismatch_and_nonzero_cache_halt","test_original_code_matches_after_rebinding_and_return_is_unique"), impl(H,"capture_operands","profile"), "CPU PASS; real operands UNVERIFIED"),
("§2.3:134–135", "detach().cpu().clone() before CPU casts; offset/non-contiguous views and source preservation",
 tests("test_same_dtype_cpu_copy_offset_noncontiguous_and_source_unchanged"), impl(H,"cpu_copy","conversion_selftest"), "CPU view PASS; MPS self-test UNVERIFIED by no-GPU instruction"),
("§2.3:136–141", "Wrapped/unwrapped A7 trial on restored pristine weights and distinct fresh zero caches; five captures",
 tests("test_parity_trials_restore_and_start_with_distinct_zero_caches"), impl(H,"parity_trial"), "Stub PASS; real applied-weight parity UNVERIFIED"),
("§2.4:141–149", "Admission/context/inertness/LAW#3/budget/memory failures halt with new diagnostic and failed gate",
 tests("test_halt_stages_immediately_preserves_harvest_and_emits_diagnostic","test_admission_probe_error_emits_failed_gate_and_staged_closeout"), impl(R,"stage_halt","gate"), "CPU/event PASS; live gates UNVERIFIED"),
("§2.5:150–164", "162 clean prompts/all positions/5 layers, original context keys, six in-loop and post-edit files, A7 weights",
 tests("test_new_outputs_flat_cpu_and_sha_shape_dtype_manifest"), impl(H,"prompt_specs","capture_prompts","capture_context_keys","harvest"), "Serialization/manifest PASS; complete real harvest UNVERIFIED"),
("§2.6:166–175", "3600 process cap; aggregate 900/300/1800/300/300 stages; projected-end refusal",
 tests("test_budget_projection_and_stage_cap","test_nested_stage_restores_outer_deadline_and_run_attach_keeps_one_start","test_exception_discards_failed_stage_and_restores_only_enclosing_alarm"), impl(R,"Budget","stage"), "CPU PASS"),
("§3:179", "Plain-Python marimo, one pydantic params model, exact PEP723 dependency set",
 tests("test_notebooks_have_frozen_pep723_dependencies_and_no_science_imports"), "mathlab/m2_solve_repro.py:1; mathlab/m3_calibration.py:1", "Metadata/static marimo PASS; exact UV execution BLOCKED"),
("§3:179; §6:286", "Torch ==2.8.0 == .venv; eight CPU threads; no MPS tensor use",
 tests("test_notebooks_have_frozen_pep723_dependencies_and_no_science_imports"), impl(C,"assert_environment","cpu64"), "CPU fixture PASS"),
("§3:181–187", "Exact fp32 projector/null count/SHA or four probes <=1e-6; A7 tensor/other norms <=1e-5",
 tests("test_fp32_projector_and_solve_are_exact_and_fp64_diagnostic_only","test_relative_zero_denominator_is_invalid_and_projector_zero_probes_need_sha"), impl(C,"projector","projector_matches","reproduce"), "Tiny fixture gate 2a PASS; real replay UNVERIFIED"),
("§3:187–188", "Float64 variant and cond(A) diagnostic only; never substitute for fp32 gate",
 tests("test_fp32_projector_and_solve_are_exact_and_fp64_diagnostic_only"), impl(C,"solve"), "CPU PASS"),
("§3:190–196", "Sequential clean-key additive approximation, every-layer error<=.25/cos>=.95; non-stopping scope",
 tests("test_gate2b_failed_approximation_is_scope_only","test_notebook_boundary_uses_real_budget_events_and_non_stopping_2b"), impl(C,"approximation_scope","reproduce"), "CPU PASS; fixture OPERANDS-ONLY; real scope UNVERIFIED"),
("§3:196; §4.1:203–208", "Effective fp16 cast/add rounding retained as named approximation",
 tests("test_fixture_reproduction_then_calibration_uses_fresh_column_and_real_events"), impl(C,"reproduce","calibration"), "Fixture/static PASS; real rounding UNVERIFIED"),
("§4.1:203–224", "Float64 keyed transfer, clipped mean; collateral all real non-lookup positions, negative even median",
 tests("test_proxy_position_sum_and_keyed_transfer","test_frozen_mean_clip_and_even_median"), impl(C,"proxy_values","score_values"), "CPU PASS"),
("§4.1:224; §4.3:247–253", "Zero denominator/non-finite invalidates whole proxy; no epsilon or row exclusion; both invalid => INVALID",
 tests("test_nan_is_not_excluded_or_epsilon_adjusted","test_invalid_tiers_shared_failure_fewer_mints_and_arithmetic_routing"), impl(C,"proxy_values","calibrate"), "CPU PASS"),
("§4.2:228–239", "Separate fresh/historical counts; actual >=10 tier margins before scoring",
 tests("test_fixture_reproduction_then_calibration_uses_fresh_column_and_real_events","test_invalid_tiers_are_checked_before_any_proxy_is_scored"), impl(C,"tier_status","calibration"), "CPU PASS; historical 999 negative control ignored"),
("§4.3:243–246", "PCG64(0), 2000 paired subject draws, shared across arms/proxies, three-paraphrase multiplicities",
 tests("test_paired_bootstrap_is_pcg64_zero_multiplicities_and_deterministic"), impl(C,"bootstrap_draws","calibrate"), "CPU PASS"),
("§4.3:243–253", "Nine or six strict point orderings; each >=1900/2000; one proxy PASS; frozen INVALID/FAIL routing",
 tests("test_nine_and_six_orderings_strictly_with_1900_bar","test_invalid_tiers_shared_failure_fewer_mints_and_arithmetic_routing"), impl(C,"ordering_passes","calibrate"), "CPU PASS; scientific calibration UNVERIFIED"),
("§4:255–259", "Injection/write consistency reported, never gating; P-coll beside historical edited-model 23/72",
 tests("test_fixture_reproduction_then_calibration_uses_fresh_column_and_real_events"), impl(C,"calibration"), "CPU/report plumbing PASS; no matched intervention claim"),
("§5:263–269", "New SHA manifests; immediate MATH-PROXY staged findings; canonical closeout reserved for lead",
 tests("test_new_outputs_flat_cpu_and_sha_shape_dtype_manifest","test_halt_stages_immediately_preserves_harvest_and_emits_diagnostic"), impl(R,"new_directory","save_tensors","stage_finding"), "CPU PASS; no canonical writes"),
("§5:265–269", "DuckDB read_json, all nine provenance fields, source wins, full rebuild",
 "mathlab/test_index.py:"+str(refs["mathlab/test_index.py"]["test_rebuild_rows_retain_source_pointer_and_sha"]), impl("mathlab/index.py","build_index")+"; "+impl(C,"index_references"), "Real DuckDB 1.5.5/Python3.12 PASS; frozen UV integration UNVERIFIED"),
("§6:274–281", "Probe error/tmux unconditional refusal; exact one-to-one PID+command+coordinator+statusSHA tail exception",
 tests("test_probe_error_cannot_use_tail_exception","test_tmux_session_cannot_use_tail_exception","test_tail_pid_command_hash_stage_and_duplicates_refuse"), impl(A,"decide","status_reference"), "CPU PASS; live ps-denial refused"),
("§6:281", "Exact nice/timeout/UV command; 2700/1800 deadlines and 300 index; dispatch proof single use",
 tests("test_cpu_runner_enforces_frozen_deadlines_and_watchdog_floor","test_saved_admission_cannot_be_replayed_by_another_process_or_after_finish","test_cpu_runner_requires_a_passing_event_closeout_even_with_exit_zero"), "tools/run_mathlab_cpu.sh:3; "+impl(U,"validate_notebook","main"), "Fixture PASS; UV success/niceness UNVERIFIED"),
("§6:283–285", "vm_stat free+inactive+speculative*16384; 5s watchdog kills below6; pre-cell8+reserve/10s/max300",
 tests("test_vm_stat_uses_free_inactive_speculative_16384_pages","test_pre_cell_reserve_wait_is_bounded_and_abort_is_staged","test_watchdog_reuses_cpu_samplers_and_handles_already_exited_parent"), impl(R,"vm_available_gib","wait_for_memory","pre_cell")+"; "+impl(U,"watch","terminate"), "CPU/stub PASS; production process-family sampling UNVERIFIED"),
("§6:285", "Full production shapes; measure RSS, raise underestimated reserve",
 tests("test_full_shape_measurement_raises_the_solve_cell_reserve"), "mathlab/core.py:16; results/mathlab_staging/peak_load.txt:3; peak_svd_summary.json:1; peak_solve_summary.json:1", "Load completed; SVD/solve time-limited; 9GiB solve reserve provisional; acceptance BLOCKED"),
("§6:285; §8:298–303", "Third resource/deadline abort operator; repeated2a or calibrationFAIL lab stop; two same-gate harvestHALTs block third",
 tests("test_internal_cpu_budget_abort_counts_toward_operator_resource_rule","test_stop_policy_blocks_third_same_gate_harvest_repeated_2a_and_calibration_fail","test_calibration_fail_remains_stop_when_index_later_aborts"), impl(R,"prior_aborts","enforce_stop_policy")+"; "+impl(C,"run_notebook"), "CPU PASS; archived outputs preserved"),
("Observability Part A:17–28", "Only real events.jsonl run-state authority; stages/progress/gates/resources/halts/findings/closeout",
 tests("test_real_shared_events_integrate_and_non_gating_scope_does_not_stop","test_cpu_runner_stages_prereg_refusal_before_dispatch","test_admission_probe_error_emits_failed_gate_and_staged_closeout"), impl(R,"Run","stage_halt")+"; "+impl(A,"main"), "Real shared module PASS; live refusal fold PASS; events module untouched"),
]

review = """# D-ML-1 build review record

The brief explicitly requested GPT-6-Astra at high reasoning after the build. The parent used a fresh, read-only GPT-6-Astra/high reviewer, with no torch/model imports, GPU calls, harvest dispatch, edits or commits authorized. Earlier FIX-FIRST findings were addressed with saved RED regressions before fixes. Final reviewer output:

> Final delta review: accepted. No new defect found. Overall build acceptance remains BLOCKED on exact UV execution and completed production-shape RSS measurement.
>
> The context guard requires the frozen s0 record SHA and uses its literal /ctx; no substitution remains. Admission probe errors produce allowed=false, a failed admission gate, staged finding, and exit 3. Recorded verification: 60 tests PASS, plus 1 real DuckDB test PASS. Frozen prereg SHA remains unchanged.
>
> Document s0's dual role explicitly: its target/step-0 failures are seed-specific; loss of its authoritative context record refuses the shared context gate. This is a conservative interpretation of section 2.2's named context authority alongside its per-arm failure rule.
>
> No unsafe dispatch or incorrect source provenance found in these corrections. No imports, execution, or edits were performed beyond read-only inspection.

The independent test-plan reader used the documented weaker same-family fallback. Its original FIX-FIRST findings concerned real event integration, harvest serialization/manifests, full-shape RSS, immediate stop staging/preserved outputs, and observer order/return/exception cleanup. Those have explicit tests. It inspected saved outputs; it reran no tests. It identified the same unresolved UV/full-peak checks. Its 57-test snapshot preceded the final 60-test run; the report uses the later evidence.

Claude CLI auth was probed, not assumed absent: claude_auth_probe.txt records loggedIn=false, authMethod=none, exit 1. An earlier advisor wrapper invocation also refused without auth. There is no successful Claude review or out-of-family approval.

After the last Astra dispatch/provenance check, the builder added the prereg's non-gating injection-consistency reporting fields, verified by consistency_report_red.txt then the final 60-test suite. This small output-only delta does not modify any calibration gate. The later fixture-runner UV attempts validate staged refusal, not successful frozen execution. Neither later item is represented as an additional Astra review.
"""
(S/"build_review_astra.md").write_text(review)

header = f"""# MathLab steps 1–3 build report — D-ML-1

Recorded UTC: {scope["utc"]}

**Status: implementation built; BUILD ACCEPTANCE BLOCKED.** The final suite has **60 CPU/fixture tests PASS**, plus **1 real DuckDB test PASS**. Frozen-runtime headless success and complete production-shape peak RSS remain unverified. This report grants no harvest launch or GPU clearance. All results here are fixture/tooling checks, not scientific calibration or behavioural evidence.

## Authority and scope

The builder read docs/MATHLAB_BUILD_BRIEF.md and the complete FROZEN v4 prereg before implementation, verified the prereg hash first, and reverified it at closeout:

~~~text
{EXPECTED}  docs/MATHLAB_PREREG.md
~~~

Worktree: {W}

Branch: {scope["branch"]}. Observed HEAD: {scope["head"]}. No commits or mutating git commands were performed. Zero GPU/MPS execution, zero local model loads, and zero harvest dispatches. Torch tests used CPU tensors with eight threads and completed in about two seconds. Production-shape CPU probes were limited to 30 seconds each to honor the brief's short-test constraint.

The implementation added 13 files, listed below. It did not create or edit tools/mathlab_events.py; that independently supplied module was used for integration, with no stand-in. Its integration and final SHA are identical:

~~~text
{scope["events_integration_sha256"]}  tools/mathlab_events.py
~~~

The builder did not write the engine, harness, frozen prereg, CORPUS, ledgers, runbook, checkpoint, dashboards, .venv packages or other sessions' files. It did not restart dashboards. Step 4 and InfraNodus are outside this build. Findings/diagnostics generated by fixtures are labelled as fixtures and isolated; the real admission refusals are tooling findings only.

## What was built

| File | Purpose | SHA-256 |
|---|---|---|
"""
for name, item in scope["owned_files"].items():
    purposes = {"mathlab/core.py":"Frozen algebra, reproduction, calibration and notebook boundary",
                "mathlab/fixtures.py":"Tiny synthetic harvest",
                "mathlab/index.py":"Derived DuckDB rebuild",
                "mathlab/m2_solve_repro.py":"PEP723 marimo step 2",
                "mathlab/m3_calibration.py":"PEP723 marimo step 3",
                "mathlab/test_mathlab.py":"CPU/stub/fixture contract tests",
                "mathlab/test_index.py":"Real DuckDB provenance test",
                "tools/mathlab_admit.py":"Fail-closed pre-import admission and dispatch recheck",
                "tools/mathlab_runtime.py":"Events, budgets, manifests, staging and stop policy",
                "tools/mathlab_harvest.py":"Deferred live harvest and read-only observer",
                "tools/mathlab_cpu_runner.py":"CPU process runner/watchdog",
                "tools/run_mathlab_cpu.sh":"Pre-import CPU launcher",
                "tools/run_mathlab_harvest.sh":"Pre-import harvest launcher"}
    header += f"| {name} | {purposes[name]} | {item['sha256']} |\n"

header += """

## Requirement → test → implementation

All prereg references below name docs/MATHLAB_PREREG.md. Test references name the actual test methods, not inferred coverage. CPU or stub PASS proves plumbing only. The frozen 11008/2048 tensor shapes and the real model path remain separate from the tiny test dimensions.

| Prereg section and line | Requirement | Test / evidence | Implementation | Verification boundary |
|---|---|---|---|---|
"""
for row in rows:
    header += "| " + " | ".join(row) + " |\n"

header += f"""

## Source reads used to author the implementation

LAW#4 numbered reads preceded code. Load-bearing citations:

- experiments/track_c/c10e_bandknob.py:181–221: original sequential write, fp32 CPU solve, shape helper and second key pass; :166–178: projector; :423–444: LAW#5; :473–495: restores, zero caches, write/evaluation and ARM_HOOKS.
- memit_dry_run/memit/memit/compute_ks.py:19–50: context-group averaging; memit_dry_run/memit/rome/repr_tools.py:43–94,135–147: substring lookup and engine batching; memit_dry_run/memit/memit/memit_main.py:304–323: context cache.
- experiments/track_c/c10u_mint2_arms.py:210–256,273–282,787–794: exact P2 fields, original audit_prompts inventory, and replay registration; experiments/track_c/c10l_mint_lib.py:24–37,178–185: original registration and library inventory.
- experiments/track_c/c10x_enginepath_arms.py:126–137,467–473,912–929: context pin, original-before-rebound order and profiler precedent.
- tools/c10w_p2_gate.py:67–84: only check_fingerprint/check_gpu are reused. Fresh-process import checks loaded no torch, transformers, harness, memit or rome modules.
- CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:23 and CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:30,34: non-gating historical injection comparisons. These counts never enter calibration outcomes.

Current engine fingerprint check PASS: d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65, _cov_cpu=3. Full output is included below and in engine_fingerprint.txt.

## Test-first evidence and commands

Initial RED: 38 tests, 41 failures including subtests, with implementation files absent. The test file and failing output existed before implementation. Later review/edge regressions each have their own saved RED output before the fix. Final GREEN: 60 tests PASS; the separate real DuckDB test PASS gives 61 unique final tests. Older snapshots are retained and are not added to the final count.

Exact final commands, from this worktree:

~~~sh
/opt/homebrew/bin/rtk proxy .venv/bin/python -B -m unittest mathlab.test_mathlab -v
PYTHONPATH=/Users/robertrhu/.cache/uv/archive-v0/waLE3HFo0DjN44MZ /opt/homebrew/bin/rtk proxy /Users/robertrhu/.local/share/uv/python/cpython-3.12-macos-aarch64-none/bin/python3.12 -B -m unittest mathlab.test_index -v
/opt/homebrew/bin/rtk proxy /Users/robertrhu/.local/share/uv/tools/marimo/bin/marimo check mathlab/m2_solve_repro.py mathlab/m3_calibration.py
/opt/homebrew/bin/rtk proxy bash -n tools/run_mathlab_cpu.sh tools/run_mathlab_harvest.sh
LLMDB_ROOT='{W}' /opt/homebrew/bin/rtk proxy .venv/bin/python -B tools/engine_fingerprint.py
/opt/homebrew/bin/rtk proxy .venv/bin/python -B tools/mathlab_admit.py --kind cpu
~~~

Unit and DuckDB commands returned 0; marimo check and bash syntax check returned 0 with empty output. Admission returned the expected refusal code 3. Fresh driver imports and AST compilation passed without importing any model-loading module. Owned stale-bytecode paths were checked before final tests: zero files to remove. -B prevented new bytecode writes.

The live CPU admission probe reported Operation not permitted for /bin/ps, refused, emitted a failed admission gate, staged a finding and finished INVALID. admission_live_probe_final.txt and admission_live_event_check.json preserve the actual event read/fold positive control. This does not establish an idle GPU or coordinator-tail clearance.

## Notebook and dependency verification

Both notebooks have the exact frozen PEP723 set: marimo, duckdb, pydantic, psutil, numpy, torch==2.8.0. .venv has Python 3.11.16 and Torch 2.8.0. No packages were installed into it.

The original exact inner UV attempts for both notebooks exited 2 on PyPI DNS failure. They are retained in headless_attempts.json, m2_uv_headless.txt and m3_uv_headless.txt. They alone were not runner acceptance.

The later fixture_runner_uv_check.py invoked the real CPU runner and its exact nice/timeout/UV command for each notebook. Only admission, process sampling and the fixture diagnostic root were stubbed; the prereg hash check, Popen, UV resolver and real shared events were exercised. Both UV children exited 2 on DNS resolution, the runner exited 3, and each event stream ended INVALID with a staged CPU-EXECUTION diagnostic. These are m2_runner_uv_headless.txt and m3_runner_uv_headless.txt. Neither notebook's frozen-runtime computation ran.

A separate direct Python marimo step-2 run completed on tiny fixture data using cached real marimo 0.24.2 and pydantic 2.13.5 with .venv Torch 2.8.0. Gate 2a PASS; gate 2b OPERANDS-ONLY; final event PASS. m2_direct_headless.txt contains the full result. This bypassed UV dependency resolution and used fixture admission, so it is weaker evidence and does not satisfy §3's exact frozen-runtime requirement. Step 3's real functions, nine/six ordering logic, bootstrap and event boundary pass CPU fixture tests; its actual marimo headless runtime remains UNVERIFIED.

Cached DuckDB 1.5.5 was available only as a CPython 3.12 binary. Its real read_json/provenance/rebuild test ran under cached Python 3.12, separately from the Torch 2.8/Python 3.11 tests. Cache/tool probes found no compatible CPython 3.11 DuckDB. The frozen dependency probe also failed on DNS. No wrong-ABI package or fake DuckDB was substituted.

Both exact-run logs show nice: setpriority: Operation not permitted. Niceness enforcement in this sandbox is UNVERIFIED; the required command is present. Production process-family psutil sampling also encountered a sandbox permission boundary during the peak probe's first attempt. Tests cover that fail-closed runner path; no successful live watchdog acceptance is claimed.

## Production-shape synthetic resource checks

All synthetic tensors were CPU-only; eight Torch threads; no model or science harness imported. Workloads used the actual core algebra functions and real matrix dimensions. The measurement watcher sampled the direct child PID and vm_stat, terminated at 30 seconds or available memory <6 GiB, and did not infer GPU-idle status.

| Workload | Shapes | Result | Peak observation |
|---|---|---|---|
| A7 update save/load | Five fp32 2048×11008 matrices, weights_only=True | Completed, exit 0, about 2s including process startup | Native ru_maxrss 1.021682739 GiB; 1s sampler 0.832672119 GiB |
| SVD projector | fp32 11008×11008 covariance | Killed at 30.413s, exit -15; UNVERIFIED-TIME-LIMIT | Sampled 3.232498169 GiB, lower bound |
| Exact solve + fp64/condition diagnostics | P and zero ca 11008×11008; Kf 11008×24; rf 2048×24 | Killed at 30.401s, exit -15; UNVERIFIED-TIME-LIMIT | Sampled 8.083297729 GiB, lower bound |

The completed load measurement covers the largest A7 update file, not an entire production notebook or all files simultaneously. The interrupted SVD/solve probes cannot establish complete peaks or deadlines. In particular, the observed solve lower bound already exceeds the prereg's estimated <=6 GiB peak.

The solve reserve was raised from 4 to **9 GiB**, for both exact and clean-approximation solve paths, before final testing. This increase follows §6's raise-a-reserve rule. It is provisional, not proof that 9 GiB bounds the complete workload. SVD remains 4 GiB, load 2 GiB, bootstrap 1 GiB; each is added to the 8 GiB pre-cell floor. Complete full-shape peak measurement and freeze-confirmation remain OPEN/BLOCKING.

Raw samples and native output: peak_load.json/.txt, peak_svd.json/.txt, peak_solve.json/.txt and their summary JSONs. The preserved original helpers are in verification_scripts/. Their embedded /private/tmp paths are the paths used for the recorded attempts; copied scripts are evidence snapshots, not a portability promise.

## Review and protected-file audit

build_review_astra.md records the actual requested GPT-6-Astra/high review and weaker test-plan review, including the remaining acceptance blockers. There is no successful Claude review: its actual CLI auth probe returned loggedIn=false/authMethod=none.

The protected snapshot covers {len(baseline)} files. {len(baseline)-len(scope["protected_changes"])} are byte-identical to the start snapshot. The frozen prereg, harness c10e_bandknob, all five historical audit sources, frozen record/target identities and engine fingerprint remain verified. Seven protected files drifted during concurrent workspace activity; the builder made no edits to them. Owner attribution is not independently proven by hashes. The exact before/after hashes are in protected_start.json and protected_scope.json:

"""
for change in scope["protected_changes"]:
    header += "- " + change["path"] + ": " + change["before"] + " → " + str(change["after"]) + "\n"
header += """

The whole worktree is dirty, including other sessions' changes; git_status_final.txt is an observation, not this builder's ownership list. No global-tree unchanged claim is made. tools/mathlab_events.py is excluded from ownership and its observed integration hash is unchanged.

Graft's one query may update graft/.cache/ask-index.json, which is outside the protected-source snapshot. Its closeout SHA is a8e05aabb816533935d1721f8c54a94608cf67decce5d1a5ac1480df45121497; no cache-baseline equality is claimed. Reported query savings: approximately 249,100 tokens ($0.13), one successful call.

## Exact deferred launch commands and admission schema

These commands were not run. The lead must provide the timestamped queue record and later select the actual harvest/output paths. Nothing in this report establishes that C10X rerun3 or ASTRA attempt3 has exited, or that another coordinator is absent.

~~~sh
cd '"""+str(W)+"""'
export LLMDB_ROOT="$PWD"
unset C10_CTX_TEMPLATES
MATHLAB_QUEUE_RECORD="$LLMDB_ROOT/results/mathlab/admission_<UTC>.json"
tools/run_mathlab_harvest.sh "$MATHLAB_QUEUE_RECORD"
~~~

Replace <UTC> with the lead's real timestamped admission filename. The launcher sets W explicitly, runs the separate model-free admission, and execs the driver only on exit 0. The driver binds the proof to that shell PID and rechecks current inventory and referenced file hashes before the sole model import. No P2 dispatcher is called.

The prereg leaves the lead-record serialization unspecified; this build uses:

~~~json
{
  "terminal_sources": [
    {"coordinator": "c10x-rerun3", "path": "<lead-named terminal JSON>", "sha256": "<actual SHA-256>"},
    {"coordinator": "astra-attempt3", "path": "<lead-named terminal JSON>", "sha256": "<actual SHA-256>"}
  ],
  "no_other_coordinator_live_or_pending": true
}
~~~

Each referenced terminal JSON must have a terminal top-level status. Accepted literal statuses are PASS, FAIL, DONE, HALTED, INVALID, COMPLETE, STOPPED, or strings beginning HALTED-/STOPPED-. Raw exit codes or missing fields do not establish a terminal status.

For the CPU-only coordinator-tail exception, optional MATHLAB_ADMISSION points at a lead record with blocking_processes entries containing exact pid, command, coordinator, status_file and sha256. Every referenced status JSON must have past_last_gated_stage=true. Any inventory error, autoresearch tmux session, missing process or mismatch refuses. Harvest never gets this exception.

After an admitted harvest and successful build acceptance, the CPU commands are:

~~~sh
tools/run_mathlab_cpu.sh mathlab/m2_solve_repro.py 2700 --harvest-dir "$HARVEST_DIR"
tools/run_mathlab_cpu.sh mathlab/m3_calibration.py 1800 --harvest-dir "$HARVEST_DIR" --reproduction-dir "$M2_DIR"
~~~

HARVEST_DIR and M2_DIR must name the actual fresh successful directories. The defaults put results in new results/mathlab/m2_<UTC>/ and m3_<UTC>/ directories and rebuild only the derived results/mathlab/calibration.duckdb. Run-state authority remains results/mathlab_staging/runs/<run_id>/events.jsonl. admission.json is a launch proof, not a second status authority.

## Deviations, interpretations, and required follow-up

1. **Exact UV notebook success is BLOCKED.** Actual attempts, including fixture attempts through the real runner, failed on PyPI DNS. Direct Python m2 and separate DuckDB tests do not substitute for the frozen dependency/runtime gate. Niceness and live process-family watchdog acceptance are also unverified here.
2. **Complete production-shape peak RSS is BLOCKED.** Full SVD and solve did not complete inside the 30-second test ceiling. Sampled values are lower bounds. The observed solve estimate forced a 9GiB reserve increase; its upper bound and production deadlines still need completed validation before freeze-confirmation.
3. **All live harvest claims are UNVERIFIED.** No model/GPU ran. Real MPS view safety, wrapped/unwrapped applied-weight parity, harness LAW#5 and LAW#3, the full original 396/2376 tokenizer audit, source-unchanged runtime capture, historical replay norm agreement, complete prompt/output shapes and scientific calibration remain pending.
4. **s0 has two roles.** Its record is the literal frozen shared /ctx authority (§2.2:86) as well as a seed outcome source. Missing/wrong-SHA s0 context record conservatively refuses CONTEXT rather than substituting another record. Missing s0 targets/step0, or seed1/seed2 record/target/step0/norm failure, remains seed-specific. This dual-role refusal interpretation is explicit and accepted by the final reviewer; no multi-record context substitution remains.
5. **Lead JSON field names are an implementation choice.** Their validation preserves the prereg's terminal-source/tail evidence requirements. The lead must supply real records in that documented schema. The builder did not manufacture live queue or tail clearance.
6. **CPU self-test supersedes MPS build self-test tonight.** The user/brief forbids GPU work, so offset/non-contiguous conversion tests used CPU. The real-device self-test is installed as a harvest gate and remains unrun.
7. **Shared changes are not builder changes.** Seven protected paths changed relative to the start snapshot; they are listed with both hashes. They were not restored or overwritten. The shared events module was supplied by its owner and left untouched.
8. **Canonical closeout is deferred by design.** No CORPUS/ledger/runbook/checkpoint edits, closeout promotion, commits, step4, or InfraNodus calls occurred. The lead performs supervised fold-in later. The required context-save handoff is local to staging because its standard home-state destination lies outside the writable roots; no global memory or canonical checkpoint was written.

The next acceptance work is completed exact-UV fixture execution with the frozen dependencies, completed production-shape CPU peak/deadline verification with reserves adjusted to measurement, and a fresh reviewer/freeze-confirmation. Only after that may the lead supply live admission and dispatch the single gated harvest. No automatic third launch or re-tuned proxy is authorized.

## Full test output

The following appendices preserve full initial/final unit output and every saved regression/intermediate unit-output file. Static checks with empty stdout are identified with their successful exit, rather than fabricated output. Full notebook-result JSON remains in its separate artifact.
"""

output_files = ["tests_red.txt", "tests_green.txt", "index_green.txt"]
output_files += [p.name for p in sorted(S.glob("*_red.txt")) if p.name != "tests_red.txt"]
output_files += [p.name for p in sorted(S.glob("*_green.txt")) if p.name not in output_files]
output_files += ["tests_intermediate.txt", "tests_green_candidate.txt", "engine_fingerprint.txt",
                 "admission_live_probe_final.txt", "m2_runner_uv_headless.txt", "m3_runner_uv_headless.txt",
                 "m2_uv_headless.txt", "m3_uv_headless.txt", "frozen_uv_dependencies.txt", "claude_auth_probe.txt"]
for name in output_files:
    body = (S/name).read_text()
    header += "\n### " + name + "\n\n~~~text\n" + body + ("" if body.endswith("\n") else "\n") + "~~~\n"
header += "\n### Static checks\n\nmarimo_check.txt: exit 0, empty stdout/stderr. launcher_syntax.txt: exit 0, empty stdout/stderr. All owned Python files parsed and compiled via stdlib AST without execution.\n"
(S/"build_report.md").write_text(header)

context = f"""---
status: in-progress
branch: {scope["branch"]}
timestamp: {scope["utc"]}
files_modified:
""" + "".join("  - " + n + "\n" for n in scope["owned_files"]) + """
---

# Working on: MathLab frozen build acceptance

Implemented D-ML-1 steps 1–3 test-first, with 60 CPU/fixture tests plus 1 real DuckDB test PASS. No GPU/MPS execution, local model loads, harvest dispatches, commits or .venv installs. Shared tools/mathlab_events.py was never created/edited by the builder. Frozen prereg SHA 33e5aa4e0fc01e07e5b1b7e6fe234e07be41e9c9b2c8edf9496af5572d9b398a verified before work and at closeout.

Read results/mathlab_staging/build_report.md first. It includes the requirement/test/implementation table, complete RED/GREEN output, exact deferred launch commands and audit scope. BUILD ACCEPTANCE BLOCKED on completed frozen UV headless runs and full production-shape RSS/deadline measurement. DNS prevents dependencies; managed sandbox denies /bin/ps and nice priority changes. SVD/solve probes were killed after 30s; observed solve RSS >=8.0833GiB, reserve raised to9 for both solve paths but still provisional. Load native peak1.02168GiB completed, covering A7 update load only.

Decisions: events.jsonl is sole run-state authority; direct Python marimo and separate Python3.12 DuckDB runs are weaker evidence, not frozen-runtime acceptance. Literal frozen s0 /ctx authority must exist and hash-match; no alternative source substitution. Loss of this record refuses shared CONTEXT; its target/step0 failures remain seed-specific. Fresh counts and historical columns never combine. Gate2b is non-stopping; gate2a/calibration/resource/harvest repeat rules bind.

Remaining work:
1. Resolve dependency access outside this sandbox without installing into .venv; run both exact UV notebooks through the CPU launcher on fixtures.
2. Complete production-shape CPU resource/deadline measurements under operator-approved bounds; raise reserves to measured need, then obtain freeze-confirmation.
3. Lead alone supplies timestamped queue record, verifies real GPU/coordinator admission, and runs harvest. All model/MPS science claims remain UNVERIFIED.
4. Supervised canonical fold-in later; builder did not edit CORPUS, ledgers, runbook or checkpoint.

Seven protected files drifted during concurrent work; protected_scope.json records their before/after hashes. Never restore them from this session's baseline. git_status_final.txt includes other owners' work. GPT-6-Astra/high reviewed corrections and accepted their code/provenance, while keeping build acceptance BLOCKED. Claude CLI auth was genuinely probed and reports loggedIn=false. Verification scripts and all fixture namespaces are preserved in staging; no automatic retries, commits or new science are authorized.

Context-save location deliberately stays in writable staging rather than home state or the canonical SESSION_CHECKPOINT.md. No global memories were updated.
"""
context_path = S / ("context_" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".md")
assert not context_path.exists()
context_path.write_text(context)
evidence = {}
for path in sorted(S.iterdir()):
    if path.is_file() and path.name != "evidence_manifest.json":
        evidence[path.name] = dict(sha256=sha(path), bytes=path.stat().st_size)
(S/"evidence_manifest.json").write_text(json.dumps(evidence, indent=2) + "\n")
print(json.dumps({"report":str(S/"build_report.md"),"report_bytes":(S/"build_report.md").stat().st_size,
                  "requirements":len(rows),"context":str(context_path),"protected_drift":len(scope["protected_changes"])},indent=2))
