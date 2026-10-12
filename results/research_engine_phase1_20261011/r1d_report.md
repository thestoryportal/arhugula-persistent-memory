# R1D collector — local fixture acceptance
Aliases: RE = results/research_engine_phase1_20261011; C = RE/r1d_collector.py; T = RE/test_r1d_collector.py; P = RE/r1d_identity_probe.py; W = RE/r1d_host_commands.sh; J4 = RE/intel_provisioning_manifest_v4.json; V = RE/astra_r1p3_verdict.md.
The interpreter and core digest remain unbound; inventory is not ready for Intel execution (J4:1589–1597,3053; C:224–230). Acquisition remains disabled (J4:1620; C:140–148).

| Round-3 item | Answer or open reason |
|---|---|
| F1 | C:67–118,224–313,345–403,451–477,918–924; T:414,490. Core-only hash, persistent clock, add-only evidence, byte accounting and preserved prior receipts. |
| F2 | C:903–905; T:546. Final summary file/directory fsync precedes deadline check and success output at C:926. |
| F3 | C:434–440,528–556; T:566. Active argv reaches the first immutable failure on both real remaining() deadline sites. |
| F4 | C:120–137; P:20–47; T:524,615. Open: actual Intel identity must be captured and bound before the window; J4:1589–1597 stays NEEDS-FETCH. |
| F5 | C:128–136,252–258; W:5; T:646,677. Executable/flags and receipt component equality are checked; all modes use collect() dispatch in the new partition test. |
| F6 | Open: trial adapter, exact prerequisites, confinement, hard caps and lifetime prefix verification remain unresolved; conditional proposal only (V:39–41,51). |
| R1 | C:67–118,345–403,918–924; J4:2152,2712. Only sealed evidence slots may be filled; frozen limits/root/identity cannot be updated through the ledger. |
| R2 | C:434–440,903–905; T:546,566. Both deadline defects have behavioral coverage. |
| R3 | C:120–148,252–258; T:524,646,724. Open: Intel identity and reviewed curl/write-root/redirect/unknown-length enforcement receipts; acquisition stays false (J4:1620; V:49). |
| R4 | Open: operator approval cannot bypass trial adapter/prerequisite/confinement/cap/prefix gates; no trial dispatch was added (V:51; C:821–902). |

| Test name | Source |
|---|---|
| test_01_cumulative_clock_across_invocations | T:154 |
| test_02_prewrite_byte_admission_and_cached_accounting | T:170 |
| test_03_durable_timeout_and_command_failure_receipts | T:189 |
| test_04_scoped_streaming_inventory_separates_baseline | T:221 |
| test_05_special_unreadable_and_changing_entries_are_observations | T:249 |
| test_06_phase_specific_guard_and_strict_observation_types | T:299 |
| test_07_actual_install_walk_rejects_unregistered_extra | T:325 |
| test_08_manifest_policy_artifact_types_lock_and_modes | T:339 |
| test_09_mode_results_partition_identity_without_verification | T:377 |
| test_r1d_01_core_seal_preserves_window_receipts_and_elapsed | T:414 |
| test_r1d_02_add_only_evidence_chain_rejects_tampering_and_core_slots | T:490 |
| test_r1d_03_identity_must_be_bound_and_match_before_any_clock_or_write | T:524 |
| test_r1d_04_final_summary_fsync_deadline_has_no_success_output | T:546 |
| test_r1d_05_real_cumulative_command_deadline_retains_active_argv | T:566 |
| test_r1d_06_probe_is_read_only_and_stdlib_function_is_shared | T:615 |
| test_r1d_07_single_policy_interpreter_wrapper_and_receipt_equality | T:646 |
| test_r1d_08_each_mode_entrypoint_established_and_open_partition | T:677 |
| test_r1d_09_unreviewed_acquisition_refuses_before_writes_or_children | T:724 |

Proposed sequence for MAESTRO, after separate Intel execution clearance (V:49,55–59). Run from the admitted Intel export root. Save the exact probe stdout as /private/tmp/r1d-intel-identity.json as a separate MAESTRO capture step; the probe itself writes nothing (P:12–47). Bind once before any window exists; never rebind after inventory (C:224–230,283–297).
```bash
RE=results/research_engine_phase1_20261011
/usr/bin/python3 -I -B "$RE/r1d_identity_probe.py"
# MAESTRO captures that Intel JSON, then binds the reviewed v4 before its first window:
/usr/bin/python3 -I -B - "$RE/intel_provisioning_manifest_v4.json" "$RE/r1d_collector.py" /private/tmp/r1d-intel-identity.json <<'PY'
import importlib.util, json, sys
from pathlib import Path
manifest_path, collector_path, probe_path = map(Path, sys.argv[1:])
m = json.loads(manifest_path.read_bytes()); identity = json.loads(probe_path.read_bytes())
if m['window_seal']['core_sha256'] != 'NEEDS-FETCH' or any(v != 'NEEDS-FETCH' for v in m['collector']['interpreter']['identity'].values()): raise SystemExit('Already bound; no rebinding')
if set(identity) != set(m['collector']['interpreter']['identity']): raise SystemExit('Incomplete probe object')
if Path(m['collector']['retained_dir']).exists(): raise SystemExit('Window root already exists; no rebinding')
if identity['machine'] != m['host']['arch'] or identity['flags'] != {'isolated': 1, 'dont_write_bytecode': 1}: raise SystemExit('Wrong host or flags')
spec = importlib.util.spec_from_file_location('r1d', collector_path)
api = importlib.util.module_from_spec(spec); spec.loader.exec_module(api)
if not api.pin(identity['executable_sha256']) or not api.pin(identity['stdlib']['sha256']) or 'NEEDS-FETCH' in json.dumps(identity): raise SystemExit('Unbound identity')
m['collector']['interpreter']['identity'] = identity
m['window_seal']['core_sha256'] = api.core_digest(m)
manifest_path.write_text(json.dumps(m, indent=2, allow_nan=False) + '\n')
PY
bash "$RE/r1d_host_commands.sh" inventory "$RE/intel_provisioning_manifest_v4.json"
```
Later evidence update: `bash "$RE/r1d_host_commands.sh" inventory "$RE/intel_provisioning_manifest_v4.json" EVIDENCE_UPDATE_JSON`; the input has exactly `slot` and `value`, and each slot can be filled once (C:383–403,918–924). The first chain predecessor is the seal; immutable per-record heads detect edits and complete-line truncation. Interrupted appends refuse rather than restart (C:345–380).

Acceptance commands and observed local receipts (temporary logs are not Intel evidence):
- `/usr/bin/python3 -B -m unittest discover -s results/research_engine_phase1_20261011 -p 'test_r1d_collector.py'`: exit 0, 18 tests, OK (/private/tmp/r1d_green.log:1–5); initial RED was 18 missing-implementation failures (/private/tmp/r1d_red.log:1–10); update-entrypoint RED was a missing ledger value (/private/tmp/r1d_update_entrypoint_red.log:1–14).
- `/usr/bin/python3 -B -m unittest discover -s results/research_engine_phase1_20261011 -p 'test_r1c_collector.py'`: exit 0, 9 tests, OK (/private/tmp/r1d_r1c_regression.log:1–5).
- `bash -n results/research_engine_phase1_20261011/r1d_host_commands.sh` and `/usr/bin/python3 -B -m json.tool results/research_engine_phase1_20261011/intel_provisioning_manifest_v4.json`: exit 0 (W:1–5; J4:1).
- `/usr/bin/python3 -I -B results/research_engine_phase1_20261011/r1d_identity_probe.py`: M3 exit 0, JSON parsed; no-file behavior also checked in a temporary cwd (P:47; T:615–644). No M3 identity is bound as Intel evidence (J4:1589–1597).

Retained local test stdout: `Ran 18 tests in 0.735s — OK`; unchanged R1C: `Ran 9 tests in 0.122s — OK` (/private/tmp/r1d_green.log:3–5; /private/tmp/r1d_r1c_regression.log:3–5).

Open: native inventory, artifact trust/ABI/interfaces, setup fit and trial/native commissioning acceptance remain unproved; observations never become verification (C:813–819; V:49–59; J4:1521–1548). The frozen false staging/build/install and child-reviewed values cannot be promoted through evidence (J4:14–17,1620; C:77–100,383–386).
Session context: next action is Astra review of these six new files, then separately cleared Intel probe/binding. Context rule: start a new step only at >=60% left; at <=40% or compaction, stop, append R1D HANDOFF here with done/remaining/paths/next single step/this rule, and reply R1D HANDOFF.

Scope receipt: all 60 existing RE files remain byte-identical, including every r1c_* file and v3; exactly the six authorized new files were added (/private/tmp/r1d_scope_acceptance.log:1; before hashes at /private/tmp/r1d_scope_before.json:1). No Intel execution or native acceptance is claimed (J4:1589–1597,1620; V:55–59).
