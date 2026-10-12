# R2W final report — D15 conservative operand-domain repair
B = results/compute_storage_brainstorm_20261011T054507Z. Static candidate FIX READY for Astra round 12; no commits or real launches.
Acceptance 3 scope accepted by MAESTRO in this turn, following B/r2v_report.md:52; all subject bytes unchanged from r2w4_handoff.md.

Final subject SHA256 (computed with shasum -a 256):
shared_disk_clearance_freeze_v10.md c49a43ed417c840940e871b3dca9e8d68de619abd31fc9e8ec5f309bd9a51656
shared_disk_clearance_schemas_v9.json 5a5d7c4502169717589bdc22da1a6758d1796fd9cf2578de03ea78fa7e13db7c
check_r2_schemas_v9.py 2c1ba6e3564c0e96c5dd68b5efa8dba4a0a14edfa290268a84096a1156b601c5
science_launch_profiles_v7.json 0e772a48659f788b56f5c53ab061e249df8ff50f608bfacc3a6d64eb091fd27d
science_launch_inventory_v9.md b95f3cfe0368cc9e63d8766f66b474f2d7b8eef1752a69ee19c58c1e1f0f966a

V11 R1: route V is one loaded_data-count operand family per reachable disk-loaded certificate admission; probes precede validate_phase, so no TRAIN_UNITS bound is inferred. Route T remains a separate disk-selected family, count at most six pinned to read:515. No pre-spawn operand equality or cross-origin sharing is inferred.
Every recorded occurrence carries pinned count/operand-source metadata. Uncovered loaded families gain NOT_ADMITTED_OPERAND_DOMAIN_UNENUMERATED:<site>; D10 NOT_ADMITTED_ADMISSION_HELPER_UNREGISTERED: remains; SCIENCE/A1 authority is retained without extending its coverage.
Closing lines: F10:210,339 (§9 maps V11 R1 and preserves earlier closures); K9:2718 r12_counts, :2753 r12_route_equality, :2777 r12_operand_sources, :2803 round12_checks, :2855 fixture, :2999 controls; J9/P7 admission_trace and child count/operand_source records.
Dispatcher phase_trains upper bounds 10/12/8 include step0:414 plus eval:357; direct bounds remain 5/6/4. P2 evaluator P1 same-seed lookup at eval:428,430–431 is a separate refused family (at most five). No bound establishes selected operand equality.
43 admission occurrences = 72 - 25 (five V sets six→one) - 4 (profile 38 six→two). 498 production binding vectors rebuilt; receipt maxima updated in F10/I9.
R2W4 acceptance fixes propagated resealed artifacts/states, mapped science enrollment kind to DESCENDANT, and corrected the missing-occurrence diagnostic for R10D; its require(matched, ...) assertion is unchanged.

Saved test-first RED on unchanged F9/J8/P6 (each exit 1; never rewritten):
FAIL: R12 loaded_data count represented by an unpinned constant: verifier-p3
FAIL: R12 routes merged without pinned pre-spawn operand equality: profile 38
Saved RED SHA256 fd8dc6b2a3e27d8656d4496a2a58267078b898984f85c7ed01bba01fe828477f; full output and baseline: B/r2w_test_first_red.md.

Acceptance 1: /usr/bin/python3 -B B/check_r2_schemas_v9.py — EXIT 0; full receipt B/r2w4_acceptance_default.md.
GREEN: 114 schemas, 17 request kinds, 259 examples validated, 1411 hash references recomputed, 8 bindings rerendered, 16 observations checked

Acceptance 2: /usr/bin/python3 -B B/check_r2_schemas_v9.py --profiles B/science_launch_profiles_v7.json — EXIT 0; full receipt B/r2w4_acceptance_profiles.md.
GREEN admission aggregates: 25 TOP_LEVEL, 55 total; max TOP_LEVEL 14 input receipts, 2797 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
GREEN all aggregate maxima: 27 input receipts / 3668 UTF-8 bytes; frozen bounds 64 / 8192 / 262144
GREEN D15 ADMISSION sites: count pinned_constant=37 loaded_data=6; operand-source pinned_literal=24 loaded_data=19
GREEN D15 SCIENCE sites: count pinned_constant=232 loaded_data=27; operand-source pinned_literal=107 loaded_data=152
GREEN D13 trace: 13 recorded queries, 43 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN production coherence: R1-R4, D1 refusals, 506 binding vectors rerendered; native behavior UNVERIFIED
GREEN profiles: 55 LaunchProfile entries, 0 not_admitted entries schema-validated, 215 not_admitted entries explicit refusals checked

Acceptance 3: /usr/bin/python3 -B B/check_r2_schemas_v9.py --mutation-controls — EXIT 0; full receipt B/r2w4_mutation_controls.md.
RED R12A: exit 1: R12 loaded_data count represented by an unpinned constant: verifier-p3
RED R12B: exit 1: R12 routes merged without pinned pre-spawn operand equality: profile 38
RED R12C: exit 1: R12 count bound unpinned: gate-phase-trains
GREEN mutation controls: 56 intended RED (53 preserved + 3 D15), zero filesystem writes
All 56 distinct control IDs independently matched their own CONTROL_MESSAGES diagnostics; all 53 earlier controls preserved. R12A reaches seven distinct mocked probes before pinned validation failure; R12B reaches 6+6 disjoint route operands. No file writes or real Git/verifier launches by fixtures; source reads/path resolution occur.
Accessible census (receipts precreated): B 242→242 entries; TMPDIR 182065→182065 entries; zero created/removed files, directories or symlinks. Full lists: B/r2w4_census_before.json and B/r2w4_census_after.json; identical snapshots.
Exact caveat: 45 PermissionError(errno=1) subtrees are listed in B/r2w4_census_summary.md; their contents are UNVERIFIED. No exhaustive host-TMPDIR census claim. Host-level zero-write proof belongs to MAESTRO’s deny-write sandbox acceptance, which MAESTRO runs next; that host proof is pending here. Census wrapper exit 3 records this visibility limitation; K9 exit 0 is separate.

F10 schemas/profiles/inventory/interface/runtime pins equal independently computed shasum. Final verification rechecks all five subject hashes against the handoff, all 14 protected inputs/sources against /private/tmp/r2w2_input_hashes.json, and the locked RED hash.
Gate 1 OPEN pending Astra round 12; Gate 2/3 and all 18 parent plus 10 subcases UNRUN. C:85, A1 and D10 unchanged; Intel-local work continues with no Intel-dependent science wait or termination.
No subjects, protected inputs, saved RED, receipts or handoff edited in this completion turn; only this report written. Next: MAESTRO deny-write sandbox proof and Astra round 12.
Context rule retained: start new work only at >=60%; at 45%, MAESTRO context-stop, or any compaction, stop starting work and write a separate handoff with exact hashes/state/next step and this rule; never append it to a report or tested file.
