# R1E — fixture repair, Intel qualification open
Aliases: RE = results/research_engine_phase1_20261011; C = RE/r1e_collector.py; P = RE/r1e_identity_probe.py; B = RE/r1e_bind_manifest.py; W = RE/r1e_host_commands.sh; T = RE/test_r1e_collector.py; J = RE/intel_provisioning_manifest_v5.json; V = RE/astra_r1p4_verdict.md.
R1 remains open until Astra reviews this repair and the registration/resume cases are captured on Intel (V:66,76; T:800-888). Identity completeness remains open until corrected Intel capture and matching binding; the old observation is not bound (V:21-23; J:1589-1598; B:47-57). R2 repaired at source/fixture level; acquisition and native acceptance remain unverified (P:20-51; C:174-182; J:1622; V:44-48,72).
Lifecycle protection holds only while the registration survives intact; loss of all independent state is not covered. Existing registration causes pre-clock validation of directory identity, prior receipts and append state; accounting uses registered sizes and journal bytes (C:322-331,407-474,651-662). Failed windows are not recovered by rebinding or resealing (B:35-42; C:145-148).

| Round-4 item | Answer or open reason |
|---|---|
| F1 | C:298-376,407-474,651-662; T:800,825,846. External registration, original clock, device/inode/birth identity and creation token, chained receipt hashes; R1 remains open for reviewed Intel capture. |
| F2 | P:20-51; C:20-26,154-171; T:641,890. Traversal errors raise; all links bind text; file targets bind bytes even outside stdlib; escaping directory/dangling links refuse. Identity completeness remains open on Intel. |
| F3 | B:20-80; C:121-151; W:5-10; J:1551-1553. Reviewed input hashes precede imports; actual identity equals probe; exclusive fsynced publication, provenance and source-core reconstruction; commands use the bound file. |
| F4 | C:634-641,727-755,1103-1105; T:572,592. R1D final-persistence deadline and causal argv behavior retained. Source/fixture repair is not native child qualification (V:34). |
| F5 | C:68-118,154-171,287-293; T:673. Required policy coverage and duplicate-limit equality retained; J:1709,2714 adds the frozen registration path. No Intel admission claim (V:42). |
| F6 | C:528-566; T:846. Empty ledger, incomplete registration and tested interrupted writes refuse. Observation-only result and frozen acquisition gate remain (C:1014-1020; J:1622). |
| R1 | Open: source/fixture repair at C:298-376,407-518,651-691; review and Intel registration/resume capture still required (V:66,76; T:800-888). No guarantee after registration loss. |
| R2 | R2 repaired in source/fixtures (P:20-51; T:890-925); identity completeness remains open until corrected Intel capture and review (V:68,76). |
| R3 | B:20-80; C:121-151; T:942-1032; W:5-10. Hash checks, measured equality, provenance, exclusive durable output and reseal rejection; actual Intel binding is pending (J:1589-1598,3057). |
| R4 | Narrowed lifecycle and qualification claims above; report assertions at T:1034-1045. Acquisition and native acceptance remain unverified (C:174-182; J:1622; V:72). |

| Test name (18 retained names, 9 new criteria; T) | Line |
|---|---|
| test_01_cumulative_clock_across_invocations | T:180 |
| test_02_prewrite_byte_admission_and_cached_accounting | T:196 |
| test_03_durable_timeout_and_command_failure_receipts | T:215 |
| test_04_scoped_streaming_inventory_separates_baseline | T:247 |
| test_05_special_unreadable_and_changing_entries_are_observations | T:275 |
| test_06_phase_specific_guard_and_strict_observation_types | T:325 |
| test_07_actual_install_walk_rejects_unregistered_extra | T:351 |
| test_08_manifest_policy_artifact_types_lock_and_modes | T:365 |
| test_09_mode_results_partition_identity_without_verification | T:403 |
| test_r1d_01_core_seal_preserves_window_receipts_and_elapsed | T:440 |
| test_r1d_02_add_only_evidence_chain_rejects_tampering_and_core_slots | T:516 |
| test_r1d_03_identity_must_be_bound_and_match_before_any_clock_or_write | T:550 |
| test_r1d_04_final_summary_fsync_deadline_has_no_success_output | T:572 |
| test_r1d_05_real_cumulative_command_deadline_retains_active_argv | T:592 |
| test_r1d_06_probe_is_read_only_and_stdlib_function_is_shared | T:641 |
| test_r1d_07_single_policy_interpreter_wrapper_and_receipt_equality | T:673 |
| test_r1d_08_each_mode_entrypoint_established_and_open_partition | T:704 |
| test_r1d_09_unreviewed_acquisition_refuses_before_writes_or_children | T:751 |
| test_r1e_01_missing_renamed_emptied_replaced_root_refuses_without_clock | T:800 |
| test_r1e_02_prior_receipt_integrity_and_registered_accounting | T:825 |
| test_r1e_03_interrupted_initialization_and_append_boundaries_refuse | T:846 |
| test_r1e_04_identity_errors_symlink_text_and_target_bytes | T:890 |
| test_r1e_05_binder_checks_all_hashes_before_import_or_write | T:942 |
| test_r1e_06_binder_measures_identity_and_records_provenance | T:954 |
| test_r1e_07_binder_exclusive_durable_publication_preserves_v5 | T:975 |
| test_r1e_08_only_bound_reviewed_core_and_provenance_accepted | T:1004 |
| test_r1e_09_report_qualifies_lifecycle_and_host_acceptance | T:1034 |

Exact sequence for MAESTRO, after review and separate Intel clearance (V:74-76). On Intel, run from the admitted export root; stdout capture is a separate shell write, while the probe itself has no file writer (P:12-65; J:1605,1612). Keep v5 and all three implementation files unchanged; the binder verifies the first three hashes and records its own hash (B:25-32,59-65).
```bash
RE=results/research_engine_phase1_20261011
set -euo pipefail; set -C
/usr/bin/python3 -I -B "$RE/r1e_identity_probe.py" > /private/tmp/r1e-intel-identity.json
/usr/bin/python3 -I -B "$RE/r1e_bind_manifest.py" "$RE/intel_provisioning_manifest_v5.json" "$RE/r1e_collector.py" "$RE/r1e_identity_probe.py" /private/tmp/r1e-intel-identity.json "$RE/intel_provisioning_manifest_v5_bound.json" 23ebba24bb9f95847bc94239585fa489c97e57c5788cc9a5f23d33b177341f67 3471a2f379450f0c41195a60ff3bfdcc117d282617ec555b93a7777480eb9cc2 3172ef39ba74105b854735ad12113bde9df8d13c6332fe857885ce939dcad5cb
# Record the printed bound SHA-256 (B:78-80). Now on the M3 worktree:
RE=results/research_engine_phase1_20261011
test ! -e "$RE/intel_provisioning_manifest_v5_bound.json"
scp "robertrhu_node2@192.168.10.2:/Users/robertrhu_node2/research-engine-phase1/$RE/intel_provisioning_manifest_v5_bound.json" "$RE/intel_provisioning_manifest_v5_bound.json"
: "${INTEL_BOUND_SHA256:?set to the exact SHA printed by the Intel binder}"
test "$(shasum -a 256 "$RE/intel_provisioning_manifest_v5_bound.json" | awk '{print $1}')" = "$INTEL_BOUND_SHA256"
# Digest mismatch aborts before inventory (B:78-80).
# Back on Intel, in the same export root:
RE=results/research_engine_phase1_20261011
bash "$RE/r1e_host_commands.sh" inventory "$RE/intel_provisioning_manifest_v5_bound.json"
# Later add-only update, same bound file (C:568-599,1120-1126):
bash "$RE/r1e_host_commands.sh" inventory "$RE/intel_provisioning_manifest_v5_bound.json" EVIDENCE_UPDATE_JSON
```
Binder SHA-256: `03d53b66ad5069497e51a95b9c2ec03b761ba8c837cedfcab7dd3d35be660d12` (B:63). The copy source assumes the admitted `/Users/robertrhu_node2/research-engine-phase1` export root (J:1605,1612); adjust only the export transport path if MAESTRO exported elsewhere, never the frozen retained/registration/install paths (C:145-148,298-311). The scp commands above are instructions for MAESTRO, not executed evidence.
Local acceptance: `/usr/bin/python3 -B -m unittest discover -s results/research_engine_phase1_20261011 -p 'test_r1e_collector.py'`: exit 0, 27 tests OK (/private/tmp/r1e_green.log:3-5); unchanged R1D: 18 OK (/private/tmp/r1e_r1d_regression.log:3-5); unchanged R1C: 9 OK (/private/tmp/r1e_r1c_regression.log:3-5). These are fixture results (T:180-1045).
`bash -n RE/r1e_host_commands.sh`, v5 JSON parsing and Python 3.9 syntax: pass (/private/tmp/r1e_validation.log:1; W:1-10; J:1). `/usr/bin/python3 -I -B RE/r1e_identity_probe.py`: M3 exit 0, parseable JSON, empty temporary cwd; no binding (/private/tmp/r1e_probe_acceptance.log:1; T:641-671).
Test-first RED: /private/tmp/r1e_red.log:429-431; tightened initialization-boundary RED: /private/tmp/r1e_boundary_red.log:17-27,39-41. Scope: 70 existing non-exec-log files byte-identical; exactly seven authorized additions; exec logs never read (/private/tmp/r1e_scope_acceptance.log:1; before hashes /private/tmp/r1e_scope_before.json:1).
Open: Intel identity/registration capture and Astra review; artifact acquisition, toolchain/native commissioning and storage/time fit remain unverified (J:1589-1598,1622; V:44-48,68,72,74-76). Frozen child_contract.reviewed=false is preserved; no receipt can authorize curl (C:174-182; J:1622; V:44-48,72).
Session gate: next single step is Astra review of the seven R1E files. Context rule: start a new step only at >=60% left; at <=40% or compaction, stop, append `## R1E HANDOFF` here with done/remaining/exact paths/next single step/this rule, and reply `R1E HANDOFF`.
