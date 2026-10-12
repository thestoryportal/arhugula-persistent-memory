# R2T acceptance re-run by MAESTRO54 (2026-10-11 ~19:12Z)

Builder codexr2t handed off at 36% context after building F7/J6/K6/P4/I6 and running acceptance 1–3 itself (`r2t_handoff.md`). MAESTRO54 reran the checks before briefing the successor, on these subject bytes.

- Subject sha256, recomputed: F7 c4a39020…, J6 36a9ad6c…, K6 e63f2375…, P4 0f2ca842…, I6 faae4c6f…. All five match the handoff. F7:326, :327 and :331 pin P4, J6 and I6 at those values. Nothing pins F7's own hash.
- Inputs F6, J5, K5, P3, I5, C, V8, D9, D8, DR and O8 are unchanged from HEAD (`git diff --quiet HEAD`).
- Acceptance 1: `/usr/bin/python3 -B B/check_r2_schemas_v6.py`, exit 0:
  GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
  GREEN: 114 schemas, 17 request kinds, 259 examples validated, 1411 hash references recomputed, 8 bindings rerendered, 16 observations checked
- Acceptance 2 and 3 ran under `/usr/bin/sandbox-exec -p '(version 1)(allow default)(deny file-write*)'`. Positive control: the same profile refused a Python file write into B (PermissionError, Errno 1), and no file appeared.
- Census: `find B $TMPDIR -newer <mark>` before and after differed only by four macOS-owned directories under `$TMPDIR` (`$TMPDIR/` itself, `TemporaryItems`, `com.apple.chrono/TemporaryItems`, `duetexpertd/TemporaryItems`). The sandbox denied every write by the checked process, so the checker did not create them. No file appeared in B.
- Label drift found (no check fails on it): F7:331 calls I6's pin "I5 whole-file bytes", and F7:360 says "F/J/P/I5/K5". The successor corrects both labels; MAESTRO does not hand-edit frozen subjects.

These are presence and recomputation checks. MAESTRO did not judge any frozen choice, profile, caller audit or refusal; that is Astra's round 9.

Output of acceptance 2 and 3 under the sandbox (verbatim; the repeated GREEN preamble lines inside acceptance 3 are omitted):
```
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN admission aggregates: 25 TOP_LEVEL, 55 total; max TOP_LEVEL 36 input receipts, 4271 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN production coherence: R1-R4, D1 refusals, 725 binding vectors rerendered; native behavior UNVERIFIED
GREEN profiles: 55 LaunchProfile entries, 0 not_admitted entries schema-validated, 174 not_admitted entries explicit refusals checked
PROFILES_EXIT=0
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
RED R8R6: exit 1: R8 R6 cross-context substitution in production tree
GREEN mutation controls: 37 intended RED (26 old + 11 round8), zero filesystem writes
RED R9R1A: exit 1: R9 R1 admission/helper carries A1 authority or science role: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10w_p2_stage.sh
RED R9R1B: exit 1: R9 R1 admission/helper carries A1 authority or science role: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10w_p2_stage.sh
RED R9R1C: exit 1: R9 R1 admission-spawned helper composition not refused: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10w_p2_stage.sh
RED R9R2A: exit 1: R9 R2 direct P1/P3 evaluator bypasses dispatcher projection: profile 4
RED R9R2B: exit 1: R9 R2 direct P1/P3 evaluator bypasses dispatcher projection: profile 6
RED R9R2C: exit 1: R9 R2 caller hit set differs: profile 0
RED R9R3A: exit 1: R9 R3 delegation reference foreign profile/context/template: payload_binding_sha256
RED R9R3B: exit 1: R9 R3 delegation reference foreign profile/context/template: admission_binding_sha256
RED R9R3C: exit 1: R9 R3 process identity disagrees with invocation binding
GREEN mutation controls: 46 intended RED (37 preserved + 9 round9), zero filesystem writes
MUTATION_EXIT=0
```

## Addendum, MAESTRO54 ~19:17Z: label correction and the committed F7 bytes

Successor codexr2t2 corrected the two labels before MAESTRO's commit 3f4f150b, so that commit holds F7 = 8d6ab32f4427a9aa… (label-corrected), not c4a39020… (the bytes checked above). MAESTRO confirmed that codexr2t2's backup copy hashes to c4a39020… and that `diff` against the current F7 changes exactly lines 331 and 360 (the two labels). It then reran on the current bytes (F7 8d6ab32f…; J6, K6, P4 and I6 unchanged): acceptance 1 exit 0; under the same deny-write sandbox, acceptance 2 exit 0 ("GREEN profiles: 55 LaunchProfile entries, 0 not_admitted entries schema-validated, 174 not_admitted entries explicit refusals checked") and acceptance 3 exit 0 ("GREEN mutation controls: 46 intended RED (37 preserved + 9 round9), zero filesystem writes"). Builder report: `r2t_report.md` (55 lines, unedited).
