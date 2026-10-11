# R2O checker v3 report — BLOCKED D1 acceptance
B = results/compute_storage_brainstorm_20261011T054507Z. All B/path:line citations expand to that prefix.
Out = B/check_r2_schemas_v3.py. T = /var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/r2o-proof-f40ufn3z. T/path:line expands to that receipt directory.

Default acceptance exits 1: FAIL: transition receipt state mismatch: INITIALIZE (T/default.log:2).
Cause: B/shared_disk_clearance_schemas_v3.json:26819 binds ActionReceiptINITIALIZE.after_state_sha256 to AuthorityRecordReconciled; its transition instead selects AuthorityRecordInitialized at :33530. Out:1062 preserves the required endpoint equality.
Receipt/source hash: 1ccc82b1b6ca44d37d741b390173638eae163c8fd4e872031d9684a156ed1a47; transition endpoint hash: d98ace8410fee4fe56b9d2a365fc68d06af4b59400342f45f4daebf9c03dab81 (sources above; independently recomputed).

D1 implementation — copied B/check_r2_schemas_v2.py:1 to Out; repointed defaults Out:16. C1 keyword/schema correctness Out:283; C2 independent §3/mapping/root checks Out:151,359; C3 instances Out:381,455; C4 references/blobs/cycles/transitions Out:753; C5 success/refusal coverage Out:455. M1–M6 preserved Out:1254; harness Out:1332.
D1 adaptations — 358-line F4 guard is 360 at Out:153; new typed propertyNames maps and maxProperties validated at Out:99,283,381, matching B/shared_disk_clearance_schemas_v3.json:10087. Keyword controls preceded support (T/keywords.py:1); unsupported names/size assertions were RED.
D1 adaptations — null revision in nonauthority absence is not a prior authority (Out:866); approval's renamed observed fields are separated (Out:1012), replacing B/check_r2_schemas_v2.py:765's old shape. No carried transition assertion was removed.
D2 — Out:668 checks precommit epoch/sequence, ledger generation, pending launch, host/boot, receipt observed/resulting pairs, exact +1, replacement 1, null initialization, QUERY and PENDING publication; approval observed pair and proposed_epoch separately. Out:775 runs it after listed hashes. Count is 15 distinct transition-proof observations, not every standalone observation example.
D3 — Out:536 dereferences source_field, checks declaration/value/source identity and SELF, reconstructs all six bindings' argv and sorted environment, then compares arrays and derived hashes. Owning unions/duplicates/ceilings checked at Out:526. SCIENCE template shapes come through Out:455; no sandbox assumption is introduced.
D3 — Out:610 independently traverses nested schema instances and manifest pointers; 765 carried mandatory hashes require unique references. Absent/out-of-range/null carry none; malformed pointers fail. Every mandatory_hash_sources citation resolves to a nonblank F4 line.
D4 — --profiles at Out:1462 validates every profiles entry as LaunchProfile, including ScienceInvocationProfile/ScienceChildProfile; known not_admitted schemas validated at Out:1418, unknown schemas explicitly counted. Out:1367 prints every specific path/assertion error. Separate mode validates profiles without claiming whole-freeze acceptance.

Source GREEN line: NONE (T/default.log:2). Development fixture only (T/fixture.log:2):
GREEN: 109 schemas, 17 request kinds, 244 examples validated, 1380 hash references recomputed, 6 bindings rerendered, 15 observations checked
Fixture changes exactly one hash-reference source to AuthorityRecordInitialized, reseals dependents/pins; F4/J3 on disk remain unchanged. It demonstrates checker behavior, not acceptance of the frozen bundle.
All new controls were written first and escaped the carried checker on that coherent fixture before guards: T/precheck-red.log:7. Archived precheck checker: T/precheck-checker.py:1.
--mutation-controls on unchanged F4/J3 exits 0, all twelve intended messages (T/controls.log:1):
RED M1 exit=1 FAIL: schema lacks assertion: Hash
RED M2 exit=1 FAIL: SSH request kind missing/non-wire: REQUEST_UNIT
RED M3 exit=1 FAIL: missing/mismatched success mapping for REQUEST_UNIT
RED M4 exit=1 FAIL: hash reference mismatch: example/Process/executable_sha256
RED M5 exit=1 FAIL: missing schema or catalog entry: ['GrantRecord']
RED M6 exit=1 FAIL: malformed required at GrantRecord
RED M7 exit=1 FAIL: invocation source pointer unresolved: InvocationBindingExecutor/job_id: unresolved JSON pointer: /transfer/not_a_field
RED M8 exit=1 FAIL: invocation rendered argv mismatch: InvocationBindingExecutor
RED M9 exit=1 FAIL: invocation declaration binding mismatch: InvocationBinding/job_id
RED M10 exit=1 FAIL: mandatory hash reference missing: example/InvocationBindingExecutor/profile_sha256
RED M11 exit=1 FAIL: observation precommit revision mismatch: ObservationRecordScienceCleared
RED M12 exit=1 FAIL: profiles[0]/invocation/sandbox_profile_sha256: additional property
M7–M11 isolation: disabling only each intended semantic guard in TMPDIR leaves the corrected fixture GREEN, including other hashes/pins/transitions (T/isolation.log:1). M12 removal boundary and schema-named not_admitted errors also checked (T/isolation.log:6).

--profiles current P snapshot: sha256 d0a6ee8f64043ab3cfbf0051dd46d8176649ea4a710088a66836f713ba1bfc14 (T/profiles.log:1).
GREEN profiles: 7 LaunchProfile entries, 0 not_admitted entries schema-validated, 15 not_admitted entries without a J3 schema
Snapshot T/profiles-snapshot.json:1 matches P bytes before/after validation; seven profiles are at B/science_launch_profiles_v1.json:3, not_admitted at :11996. MAESTRO must rerun after the parallel owner finalizes P. No P write.

F4 rules hard-coded (all citations B/shared_disk_clearance_freeze_v4.md):
- :71,74,324 — durable receipt endpoints, canonical parsed blobs, QUERY read-only; canonical UTF-8 hashes omit only authority.last_decision (Out:753,1092,1143).
- :64,94,98,99,102,113,163,169,176,177,178,179,180,181,246 — precommit observation/receipt pairs, +1 or replacement 1, old approval pair/separate proposed epoch, PENDING before final proof, null initialization, QUERY (Out:668,1012).
- :158,159,160,161 — owning declaration union, typed substitutions, source pointers/SELF, science context values, full rendered arrays/hashes (Out:526,536).
- :162 — mandatory hash pointer recursion, null/missing applicability and source citations (Out:610).
- :186,187,188,189,190,191,196,285 — operation-specific fencing, reconciliation/history exclusion and initialization in recovery (Out:882,1005,1065).
- :219,220,221,222,223,224,225,226,227,228,229,230,231,234 — exact state edges, derived exclusion/state and no recovery release without reconciliation (Out:471,848,979).
- :212,213,214,215,221,222,223,225,226,227,228,229,230,231,240 — terminal/paused closure, exact enrolled coordinator consume, fresh resumed unit/nonce, one-use clearance and atomic science archive (Out:901,931,945,967).
- :316; B/shared_disk_clearance_schemas_v3.json:10531 — synthetic schema projection excludes x-construction; deployed full-file pin remains distinct (Out:758,1132).

Noticed, not fixed: J3 INITIALIZE receipt references the wrong after-state example (B/shared_disk_clearance_schemas_v3.json:26822 versus :33530); schema owner must reconcile and reseal, then rerun both acceptance commands.
Scope: only Out, this Report, Handoff and TMPDIR written; standard-library imports only, no product execution. Protected inputs compare unchanged against T/before.json:1.
F4 sha256 02e17d9c19d5597a8619426d8ba8a5014dd9ab52f5b4e7a1a7847c99731bbc98
J3 sha256 ba89e266bf983d653b8a5e5d462413e08e87845339cd366a8939e6d761d406c8
K2 sha256 07e9b06f457845585f639d034311cc3acba6511b4cde86718fe5f844644a3d52
Out sha256 6427223c840d8594e9497c226df5987979b8e653d4a3801d6fa3c71f5d6ffb78
Static synthetic verification only; no host/operational/scientific acceptance.
