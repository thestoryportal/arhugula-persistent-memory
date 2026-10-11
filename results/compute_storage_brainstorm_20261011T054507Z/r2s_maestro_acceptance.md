# R2S acceptance re-run by MAESTRO53 (2026-10-11 ~18:26Z)

Builder codexr2s handed off at its context limit after building F6/J5/K5/P3/I5 (`r2s_handoff.md`). MAESTRO53 reran its checks before briefing the successor. Successor codexr2s2 then reran acceptance without sandbox-exec, rebuilt nothing and wrote `r2s_report.md`, which is unedited. The subject bytes below are the ones MAESTRO checked; they are unchanged in the report.

- Subject sha256, recomputed: F6 6ecf96e4…, J5 66af0014…, K5 921c347d…, P3 874b332d…, I5 c5f35494…. F6:326–331 pins P3, J5 and I5 at those values.
- Inputs F5, J4, K4, P2, I4, C, DR, D8 (`r2_round8_decisions.md`), O8 (`r2_round8_options.md`) and V7 are unchanged from HEAD (`git diff --quiet`).
- Test-first: six REDs, one per V7 R1–R6, were recorded against F5/J4/P2 before construction. They are quoted in `r2s_handoff.md` (the raw `r2s_test_first_red.log` is git-ignored).
- Acceptance 1: `/usr/bin/python3 -B B/check_r2_schemas_v5.py` exit 0:
  GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
  GREEN: 114 schemas, 17 request kinds, 259 examples validated, 1410 hash references recomputed, 8 bindings rerendered, 16 observations checked
- Acceptance 2 and 3 ran under `/usr/bin/sandbox-exec -p '(version 1)(allow default)(deny file-write*)'`. Positive control: the same profile refused a Python file write (PermissionError, Errno 1), and no file appeared.
- Acceptance 2: `--profiles B/science_launch_profiles_v3.json` exit 0 (PROFILES_EXIT=0).
- Acceptance 3: `--mutation-controls` exit 0 (MUTATION_EXIT=0).
- Census: `find B $TMPDIR -newer r2s_handoff.md` before and after differed by one path, `$TMPDIR/TemporaryItems`. That is an empty macOS-owned directory, modified 18:25:16Z around the run's start. The sandbox denied every write by the checked process, so the checker did not create it. No file appeared in B.

These are presence and recomputation checks. MAESTRO did not judge any frozen choice, profile, mapping or refusal; that is Astra's round 8.

Output of acceptance 2 and 3 (verbatim):
```
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN admission aggregates: 29 TOP_LEVEL, 55 total; max TOP_LEVEL 36 input receipts, 4271 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN production coherence: R1-R4, D1 refusals, 729 binding vectors rerendered; native behavior UNVERIFIED
GREEN profiles: 55 LaunchProfile entries, 0 not_admitted entries schema-validated, 168 not_admitted entries explicit refusals checked
PROFILES_EXIT=0
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN admission aggregates: 29 TOP_LEVEL, 55 total; max TOP_LEVEL 36 input receipts, 4271 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN production coherence: R1-R4, D1 refusals, 729 binding vectors rerendered; native behavior UNVERIFIED
GREEN profiles: 55 LaunchProfile entries, 0 not_admitted entries schema-validated, 168 not_admitted entries explicit refusals checked
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
RED R8R1A: exit 1: R8 R1 science descendant authority must be A1, not C:115
RED R8R1B: exit 1: R8 R1 root lacks full pre-release registration
RED R8R1C: exit 1: R8 R1 observation gap must retain UNRESOLVED with no terminal release
RED R8R2A: exit 1: R8 R2 guard sandbox must deny fork/exec and have empty exec_paths
RED R8R2D: exit 1: R8 R2 guard sandbox must deny fork/exec and have empty exec_paths
RED R8R2B: exit 1: R8 R2 delegation requires provisioned science launch broker
RED R8R2C: exit 1: R8 R2 broker cannot hold authority-write or bulk-write capability
RED R8R3: exit 1: R8 R3 direct P2 trainer/evaluator bypasses coordinator admission: profile 5
RED R8R4: exit 1: R8 R4 root admission receipt exceeds frozen input_receipts bound: needs 65
RED R8R5: exit 1: R8 R5 refusal misses source-valid required operands: ordinary
GREEN admission aggregates: 29 TOP_LEVEL, 55 total; max TOP_LEVEL 36 input receipts, 4271 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
RED R8R6: exit 1: R8 R6 cross-context substitution in production tree
GREEN mutation controls: 37 intended RED (26 old + 11 round8), zero filesystem writes
MUTATION_EXIT=0
```
