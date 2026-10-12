R2P: INITIALIZE correction; baseline checker RED: transition receipt state mismatch: INITIALIZE.
/x-construction/hash_references/644/source_name: AuthorityRecordReconciled → AuthorityRecordInitialized
/x-construction/examples/ActionReceiptINITIALIZE/instance/after_state_sha256: 1ccc82b1b6ca44d37d741b390173638eae163c8fd4e872031d9684a156ed1a47 → d98ace8410fee4fe56b9d2a365fc68d06af4b59400342f45f4daebf9c03dab81
/x-construction/examples/INITIALIZESuccessResponse/instance/decision_receipt: bac2092bdaed8e5473e3d98d8bdd1c7c9d1c901e619a354e0180f6d8fc3dd762 → 3c986178182ca718ea8e7ab4ea6b38de881928739a394724c4970d16416719ce
/x-construction/examples/INITIALIZESuccessResponse/instance/body/action_receipt: bac2092bdaed8e5473e3d98d8bdd1c7c9d1c901e619a354e0180f6d8fc3dd762 → 3c986178182ca718ea8e7ab4ea6b38de881928739a394724c4970d16416719ce
/x-construction/examples/AuthorityRecordInitialized/instance/last_decision: bac2092bdaed8e5473e3d98d8bdd1c7c9d1c901e619a354e0180f6d8fc3dd762 → 3c986178182ca718ea8e7ab4ea6b38de881928739a394724c4970d16416719ce
F4 line 316 (§8 schemas pin): ba89e266bf983d653b8a5e5d462413e08e87845339cd366a8939e6d761d406c8 → e8ed7828c09b9b04eaddad3c82a1f5f48672ef7c36ff0380aa3bc5ede8d29a6f
J3 old sha256: ba89e266bf983d653b8a5e5d462413e08e87845339cd366a8939e6d761d406c8
J3 new sha256: e8ed7828c09b9b04eaddad3c82a1f5f48672ef7c36ff0380aa3bc5ede8d29a6f
Scope verified: reversing the five JSON changes restores J3's original sha256; K3 and K3R unchanged; F4 only line 316 changed.
/usr/bin/python3 -B B/check_r2_schemas_v3.py: exit 0
GREEN: 109 schemas, 17 request kinds, 244 examples validated, 1380 hash references recomputed, 6 bindings rerendered, 15 observations checked
/usr/bin/python3 -B B/check_r2_schemas_v3.py --mutation-controls: exit 0
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
