# R2Q acceptance re-run by MAESTRO52 (2026-10-11 ~17:40Z)

R2Q2 replied BLOCKED only because Codex cannot nest a read-only sandbox inside its own (sandbox_apply: Operation not permitted). MAESTRO ran every acceptance step from its own shell. The builder's report (`r2q_report.md`) is unedited.

- Subject sha256 recomputed, matching r2q_report.md: F5 c2cce802…, J4 defa559b…, K4 ab7a37ca…, P2 f2c88935…, I4 a25f65fa…. F5:323–324 pins P2 and J4 at those values.
- Inputs F4, J3, K3, P, I3 and DR are unchanged from HEAD (`git diff --quiet`).
- Test-first R1–R4 were rerun on F4/J3/P before construction: all exit 1 with the messages in r2q_handoff.md.
- Acceptance 1: `/usr/bin/python3 -B B/check_r2_schemas_v4.py` exit 0:
  GREEN: 109 schemas, 17 request kinds, 248 examples validated, 1391 hash references recomputed, 6 bindings rerendered, 16 observations checked
- Acceptance 2: `--profiles B/science_launch_profiles_v2.json` exit 0:
  GREEN production coherence: R1-R4, D1 refusals, 679 binding vectors rerendered; native behavior UNVERIFIED
  GREEN profiles: 55 LaunchProfile entries, 0 not_admitted entries schema-validated, 168 not_admitted entries explicit refusals checked
- Acceptance 3: `/usr/bin/sandbox-exec -p '(version 1)(allow default)(deny file-write*)' /usr/bin/python3 -B B/check_r2_schemas_v4.py --mutation-controls` exit 0. Positive control: the same profile refused a Python file write (PermissionError, Errno 1; no file appeared). `find $TMPDIR B /private/tmp -newer <mark>` found no new file. Output:
```
RED M1: exit 1: schema lacks assertion: Hash
RED M2: exit 1: SSH request kind missing/non-wire: REQUEST_UNIT
RED M3: exit 1: missing/mismatched success mapping for REQUEST_UNIT
RED M4: exit 1: hash reference mismatch: example/Process/executable_sha256
RED M5: exit 1: missing schema or catalog entry: ['GrantRecord']
RED M6: exit 1: malformed required at GrantRecord
RED M7: exit 1: invocation source pointer unresolved: InvocationBindingExecutor/job_id: unresolved JSON pointer: /transfer/not_a_field
RED M8: exit 1: invocation rendered argv mismatch: InvocationBindingExecutor
RED M9: exit 1: invocation declaration binding mismatch: InvocationBinding/job_id
RED M10: exit 1: mandatory hash reference missing: example/InvocationBindingExecutor/profile_sha256
RED M11: exit 1: observation precommit revision mismatch: ObservationRecordScienceCleared
RED M12: exit 1: profiles[0]/authorized_payload/sandbox_profile_sha256: additional property
RED R1: exit 1: R1 guard composition mismatch: profile 0
RED R2: exit 1: R2 P2 inner launcher must be CHILD_ONLY under gated wrapper: profile 22
RED R3: exit 1: R3 science child role permits non-science authority
RED R4: exit 1: R4 P3 replication Git profile missing: profile 39 adapter 0
RED R6Q: exit 1: observation precommit revision mismatch: QUERYSuccessResponse/body/observation
RED R6H: exit 1: mandatory hash manifest omission: CheckpointRecord ['/policy_sha256']
RED E3: exit 1: invalid example: REQUEST_UNITRequest
RED E5: exit 1: missing refusal example: REQUEST_UNIT
RED E4S: exit 1: transition request sequence mismatch: ATTACH_STREAM
RED E4A: exit 1: authority derived state mismatch: AuthorityRecordStream
RED E4C: exit 1: invalid example: ActionReceipt
RED E4N: exit 1: clearance consumption binding mismatch: CONSUME_CLEARANCE
RED E4F: exit 1: admin fence kind mismatch: INITIALIZE
RED E4B: exit 1: ReceiptBlob hash mismatch: ReceiptBlob
GREEN mutation controls: 26 intended RED, zero filesystem writes
```
