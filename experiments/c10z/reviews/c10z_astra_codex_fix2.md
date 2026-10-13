BLOCKED: sandbox denied the prescribed full-log directory; code fixes and CPU verification are complete.

Prescribed logs: `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_fix2_logs/` — mkdir returned PermissionError [Errno 1] Operation not permitted.
Full logs retained at `/private/tmp/c10z_fix2_logs/codexi_4xmfoj1j/`.

Binding references below: `docs/C10Z_ASTRA_PREREG.md` and `EXPERIMENT_RUNBOOK.md:348`.

| Item | Changed file:line | Enforcing tests | Binding source |
|---|---|---|---|
| 1: child OUT_DIR | `experiments/track_c/c10z_astra_arms.py:1472`; `experiments/track_c/c10z_astra_selftest.py:1533` | `test_fix2_child_receives_parent_resolved_absolute_outdir` | Prereg :137, :204 |
| 2: failed-resident HALT | `experiments/track_c/c10z_astra_arms.py:1508`, :1517; `experiments/track_c/c10z_astra_selftest.py:1552`, :1592 | `test_fix2_failed_resident_detection_closes_halt_and_keeps_passes`; `test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields`; existing refusal regressions | D-C10z-fix1 (3), runbook :348; prereg :267, :323 |
| 3/H07: prior-process observations | `experiments/track_c/c10z_astra_selftest.py:1442` | `test_fix1_halt_sidecar_retains_completed_observations_for_both_processes` | Prereg :267 |
| 3/H08: watchdog diagnostic | `experiments/track_c/c10z_astra_selftest.py:1453`, :1463 | `test_fix1_watchdog_preserves_last_published_record` checks the watchdog's own sidecar and architecture diagnostic | Prereg :196, :225, :267, :323 |
| 3/H10/H11: session fields and architecture JSON | `experiments/track_c/c10z_astra_selftest.py:1432`, :1592 | `test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields`; `test_fix1_halt_sidecar_retains_completed_observations_for_both_processes` | Prereg :267, :323 |
| 3/G11: nonfinite go JSON | `experiments/track_c/c10z_astra_arms.py:1347`; `experiments/track_c/c10z_astra_selftest.py:1643` | `test_fix2_go_nonfinite_constants_and_overflow_refused` covers NaN, Infinity, -Infinity and positive/negative overflow; existing HALTED-V6 label retained | Prereg :219, :341–344 |
| 3/B3d: actual Session.record omissions | `experiments/track_c/c10z_astra_selftest.py:1656` | `test_fix2_session_record_absent_ceiling_matches_reader_omissions` checks stages 1 and 2 | Prereg :196, :265–267 |
| 3/B3g: disqualified K1 reason | `experiments/track_c/c10z_astra_selftest.py:1680` | `test_fix2_disqualified_missing_ceiling_is_k1_not_absent` checks PARTIAL and LEAD | Prereg :265, :272 |
| A32: driver Z0 sigma halt | `experiments/track_c/c10z_astra_selftest.py:1693` | `test_fix2_z0_sigma_halts_in_driver_at_frozen_boundary` uses tiny CPU logits; no behavior change | Prereg :147 |
| Test output isolation | `experiments/track_c/c10z_astra_selftest.py:383` | `test_transport_wait_publication_and_worker_failure` preserves its existing assertions and sends the new HALT diagnostic to its temporary directory | Fix2 file boundary |

RED (final, before production edit): 79 tests, 64.541s, FAILED (failures=12), exit 1; `/private/tmp/c10z_fix2_logs/codexi_4xmfoj1j/red_final.log`.
Failing tests: `test_fix2_child_receives_parent_resolved_absolute_outdir`, `test_fix2_failed_resident_detection_closes_halt_and_keeps_passes`, `test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields`.
Initial RED: 79 tests, 63.681s, failures=12/errors=2; missing synthetic geometry metadata corrected before production edit; `/private/tmp/c10z_fix2_logs/codexi_4xmfoj1j/red.log` and fixture-only PASS `/private/tmp/c10z_fix2_logs/codexi_4xmfoj1j/session_record_fixture.log`.
Initial failing tests: `test_fix2_child_receives_parent_resolved_absolute_outdir`, `test_fix2_failed_resident_detection_closes_halt_and_keeps_passes`, `test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields`, `test_fix2_session_record_absent_ceiling_matches_reader_omissions`.
GREEN (first production patch): 79 tests, 74.034s, OK, exit 0, failing tests none; `/private/tmp/c10z_fix2_logs/codexi_4xmfoj1j/green.log`.
Final GREEN after fixture isolation: 79 tests, 75.247s, OK, exit 0; `/private/tmp/c10z_fix2_logs/codexi_4xmfoj1j/green_scoped.log`. Own test diagnostic removed; audit: `/private/tmp/c10z_fix2_logs/codexi_4xmfoj1j/scope_cleanup.json`.

Mutation: 120/122 KILLED; 2 SURVIVED; 0 ERROR; required O02/H07/H08/H10/H11/G11/B3d/B3g/A32 all KILLED.
Survivors: `G21_mkdir_before_fresh_check`, `B3c_record_classify_no_ceilings`.
Baselines: 79-test scratch PASS before and after mutants; full `BASELINE_pre.log` and final `BASELINE.log` preserved in the mutation logs. The harness prints the final baseline twice.
Harness rerun in full after fixture isolation: reviewer copy; only BASE moved into scratch and --check made nonzero on bad targets. All 122 targets matched once; no re-anchors needed; no no-op mutants.
Full mutation output: `/private/tmp/c10z_fix2_logs/codexi_4xmfoj1j/mutations_scoped/run.log`; full per-mutant output: `/private/tmp/c10z_fix2_logs/codexi_4xmfoj1j/mutations_scoped/logs/`; provenance: `/private/tmp/c10z_fix2_logs/codexi_4xmfoj1j/mutations_scoped/input_provenance.json`.
`c10z_astra_read.py`, launcher, engine, `c10e_bandknob.py` and frozen prereg unchanged; frozen thresholds, labels, stage order and budget constants preserved; no CLI/env option added. CPU-only fixtures; no model/tokenizer/MPS load.

| ID | Result | ID | Result |
|---|---|---|---|
| R01 | KILLED | R02 | KILLED |
| R03 | KILLED | R04 | KILLED |
| R05 | KILLED | R06 | KILLED |
| R07 | KILLED | R08 | KILLED |
| R09 | KILLED | R10 | KILLED |
| R11 | KILLED | R12 | KILLED |
| R13 | KILLED | R14 | KILLED |
| R15 | KILLED | R16 | KILLED |
| R17 | KILLED | R18 | KILLED |
| R19 | KILLED | R20 | KILLED |
| R21 | KILLED | R22 | KILLED |
| R23 | KILLED | R24 | KILLED |
| R25 | KILLED | R26 | KILLED |
| R27 | KILLED | R28 | KILLED |
| R29 | KILLED | R30 | KILLED |
| R31 | KILLED | R32 | KILLED |
| R33 | KILLED | R34 | KILLED |
| R35 | KILLED | R36 | KILLED |
| R37 | KILLED | A01 | KILLED |
| A02 | KILLED | A03 | KILLED |
| A04 | KILLED | A05 | KILLED |
| A06 | KILLED | A07 | KILLED |
| A08 | KILLED | A09 | KILLED |
| A10 | KILLED | A11 | KILLED |
| A12 | KILLED | A13 | KILLED |
| A14 | KILLED | A15 | KILLED |
| A16 | KILLED | A17 | KILLED |
| A18 | KILLED | A19 | KILLED |
| A20 | KILLED | A21 | KILLED |
| A22 | KILLED | A23 | KILLED |
| A24 | KILLED | A25 | KILLED |
| A26 | KILLED | A27 | KILLED |
| A28 | KILLED | A29 | KILLED |
| A30 | KILLED | A31 | KILLED |
| A32 | KILLED | A33 | KILLED |
| A34 | KILLED | G01 | KILLED |
| G02 | KILLED | G03 | KILLED |
| G04 | KILLED | G05 | KILLED |
| G06 | KILLED | G07 | KILLED |
| G08 | KILLED | G09 | KILLED |
| G10 | KILLED | G11 | KILLED |
| G12 | KILLED | G13 | KILLED |
| G14 | KILLED | G15 | KILLED |
| G16 | KILLED | G17 | KILLED |
| G18 | KILLED | G19 | KILLED |
| G20 | KILLED | G21 | SURVIVED |
| H01 | KILLED | H02 | KILLED |
| H03 | KILLED | H04 | KILLED |
| H05 | KILLED | H06 | KILLED |
| H07 | KILLED | H08 | KILLED |
| H09 | KILLED | H10 | KILLED |
| H11 | KILLED | H12 | KILLED |
| B3a | KILLED | B3b | KILLED |
| B3c | SURVIVED | B3d | KILLED |
| B3e | KILLED | B3f | KILLED |
| B3g | KILLED | B3h | KILLED |
| B3i | KILLED | B3j | KILLED |
| B3k | KILLED | B3l | KILLED |
| B3m | KILLED | O01 | KILLED |
| O02 | KILLED | S01 | KILLED |
| S02 | KILLED | S03 | KILLED |
