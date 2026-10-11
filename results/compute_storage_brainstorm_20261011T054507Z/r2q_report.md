# R2Q2 report — BLOCKED only on required read-only execution
B = results/compute_storage_brainstorm_20261011T054507Z; F5/J4/K4/P2/I4 are new copied-and-scripted subjects. Gate 1 OPEN; native Gate 2/3, 18 parent+10 subcase cases UNRUN. No input edit/commit/science/real launch.
Computed subject and receipt SHA-256 (shasum -a 256, independently matched hashlib):
c2cce8027c3bddf4c2e64764664a845b74c68a03593d914640b7f978de602ac8  shared_disk_clearance_freeze_v5.md
defa559b55c969a8542583abab5f2d41efc3b60514359047f43d06877bbe4b54  shared_disk_clearance_schemas_v4.json
ab7a37ca5fd0e9d8d61996bf3a66f265a6b835e69c677113895e4e724b4ece37  check_r2_schemas_v4.py
f2c8893509f1ae86f0d9af8c4016a220ae3ddcb56f268b632f0da5a0dd4c3c43  science_launch_profiles_v2.json
a25f65faf5b621e3b78bc2444c5bb597188aa3451f0cb5a2dba363156710405a  science_launch_inventory_v4.md
e757a49d93cf783500a6156f29bafffd0227957a1cb3eb5d7086b2f6a6ebb7bb  r2q_test_first_red.log
31547f91f0639a8a07b3c24daf5ae54e9c71b136d8be4dc3ff23ebca814bf33e  r2q2_acceptance.log
8da0cc7425fede460c79143a96239a21addaabb427f0f00c59d6a3afb685a3b6  r2q2_input_hashes.log
83d5b0927110167d2821d5c1a47724b6f40aae2089429a8941f454ece6478649  r2q2_handoff.md
R1: canonical science-guard /invocation, launch_id/SELF declarations, /authorized_payload and external owning-template receipts; F5:207; §9:336; K4:1552.
R2: 19 CHILD_ONLY recipes; dispatcher→inner-stage→gated wrapper→refused coordinator preserved; claim→refused reattempt wrapper. Audited all 49 true admissions, retained 36 with cited absence evidence; F5:208; §9:337; K4:1583.
R3: closed Process science/ordinary unions, canonical science invocation reference in population/observation, sandbox mandatory elsewhere, child science roles and no AUTHORITY_WRITE; F5:70; §9:338; K4:1626.
R4: 66 Git recipes across 11 profiles, exact adapter bindings/offline environment; complete tree registered at root admission under DECLARED_AT_ROOT_ADMISSION; F5:209-210; §9:339; K4:1657.
R5: DR D1; 139 NOT_ADMITTED_NO_PROFILE refusals replace retirement inference, LATE_BOUND_ARGV retained, exact refused descendant routes invalidate parents; F5:211; §9:340; K4:1534. Draft-prefix-only parent check corrected to preserve DR refusals, with exact argv matching.
R6: fresh QUERY validates current authority; independently frozen mandatory pointers drive manifest coverage; production semantic checks and 26 isolated in-memory controls; F5:212; §9:341; K4:675,1495,1677. Static GREEN; required read-only control execution remains unverified.
F5 is 360 lines; schemas/profiles pins at F5:324,323. Eight predecessor-pinned inputs UNCHANGED; r2q2_input_hashes.log carries computed identities.
Test-first final failures below were saved before construction by R2Q and reproduced by MAESTRO; full commands remain r2q_test_first_red.log (all exit 1):
R1: exit 1: FAIL: R1 guard composition mismatch: profile 0
R2: exit 1: FAIL: R2 P2 inner launcher must be CHILD_ONLY under gated wrapper: profile 22
R3: exit 1: FAIL: R3 science child role permits non-science authority
R4: exit 1: FAIL: R4 P3 replication Git profile missing: profile 1 adapter 0
Acceptance 1: /usr/bin/python3 -B B/check_r2_schemas_v4.py → exit 0:
GREEN: 109 schemas, 17 request kinds, 248 examples validated, 1391 hash references recomputed, 6 bindings rerendered, 16 observations checked
Acceptance 2: /usr/bin/python3 -B B/check_r2_schemas_v4.py --profiles B/science_launch_profiles_v2.json → exit 0:
GREEN production coherence: R1-R4, D1 refusals, 679 binding vectors rerendered; native behavior UNVERIFIED
GREEN profiles: 55 LaunchProfile entries, 0 not_admitted entries schema-validated, 168 not_admitted entries explicit refusals checked
Acceptance 3: /usr/bin/python3 -B B/check_r2_schemas_v4.py --mutation-controls → exit 0 in managed workspace-write sandbox; required READ-ONLY execution UNVERIFIED:
GREEN mutation controls: 26 intended RED, zero filesystem writes
RED M1: exit 1: schema lacks assertion: Hash; RED M2: exit 1: SSH request kind missing/non-wire: REQUEST_UNIT
RED M3: exit 1: missing/mismatched success mapping for REQUEST_UNIT; RED M4: exit 1: hash reference mismatch: example/Process/executable_sha256
RED M5: exit 1: missing schema or catalog entry: ['GrantRecord']; RED M6: exit 1: malformed required at GrantRecord
RED M7: exit 1: invocation source pointer unresolved: InvocationBindingExecutor/job_id: unresolved JSON pointer: /transfer/not_a_field; RED M8: exit 1: invocation rendered argv mismatch: InvocationBindingExecutor
RED M9: exit 1: invocation declaration binding mismatch: InvocationBinding/job_id; RED M10: exit 1: mandatory hash reference missing: example/InvocationBindingExecutor/profile_sha256
RED M11: exit 1: observation precommit revision mismatch: ObservationRecordScienceCleared; RED M12: exit 1: profiles[0]/authorized_payload/sandbox_profile_sha256: additional property
RED R1: exit 1: R1 guard composition mismatch: profile 0; RED R2: exit 1: R2 P2 inner launcher must be CHILD_ONLY under gated wrapper: profile 22
RED R3: exit 1: R3 science child role permits non-science authority; RED R4: exit 1: R4 P3 replication Git profile missing: profile 39 adapter 0
RED R6Q: exit 1: observation precommit revision mismatch: QUERYSuccessResponse/body/observation; RED R6H: exit 1: mandatory hash manifest omission: CheckpointRecord ['/policy_sha256']
RED E3: exit 1: invalid example: REQUEST_UNITRequest; RED E5: exit 1: missing refusal example: REQUEST_UNIT
RED E4S: exit 1: transition request sequence mismatch: ATTACH_STREAM; RED E4A: exit 1: authority derived state mismatch: AuthorityRecordStream
RED E4C: exit 1: invalid example: ActionReceipt; RED E4N: exit 1: clearance consumption binding mismatch: CONSUME_CLEARANCE
RED E4F: exit 1: admin fence kind mismatch: INITIALIZE; RED E4B: exit 1: ReceiptBlob hash mismatch: ReceiptBlob
R6Q and R6H each update the mutated bundle’s whole-file schema pin before checking; controls create no files/directories.
Equivalent find "$TMPDIR" -newer B/codexr2q_brief.txt counts: 2 before / 2 after, created 0, removed 0, using isolated caller-prewarmed /private/tmp/r2q2_controls_precreated. Initial xcrun_db creation was reproduced by no-checker Python-launcher positive control; original TMPDIR census failed exit 1. Both attempts are preserved.
BLOCKER: /usr/bin/sandbox-exec -p '(version 1)(allow default)(deny file-write*)' ... failed before Python: sandbox_apply: Operation not permitted, exit 71. No approval escalation/retry; no claim of read-only or commissioning acceptance.
Exact next step is in r2q2_handoff.md: rerun only controls/census through MAESTRO’s existing read-only runner; then Gate-1 Astra review. Synthetic guard/vector hashes are fixtures, never installed binary/run authority.
