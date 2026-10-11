GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D15 ADMISSION sites: count pinned_constant=0 loaded_data=0; operand-source pinned_literal=0 loaded_data=0
GREEN D15 SCIENCE sites: count pinned_constant=0 loaded_data=0; operand-source pinned_literal=0 loaded_data=0
GREEN D13 trace: 13 recorded queries, 0 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN admission aggregates: 25 TOP_LEVEL, 55 total; max TOP_LEVEL 14 input receipts, 2797 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
GREEN all aggregate maxima: 27 input receipts / 3668 UTF-8 bytes; frozen bounds 64 / 8192 / 262144
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D15 ADMISSION sites: count pinned_constant=37 loaded_data=6; operand-source pinned_literal=24 loaded_data=19
GREEN D15 SCIENCE sites: count pinned_constant=232 loaded_data=27; operand-source pinned_literal=107 loaded_data=152
GREEN D13 trace: 13 recorded queries, 43 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN production coherence: R1-R4, D1 refusals, 506 binding vectors rerendered; native behavior UNVERIFIED
GREEN profiles: 55 LaunchProfile entries, 0 not_admitted entries schema-validated, 215 not_admitted entries explicit refusals checked
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
RED R4: exit 1: R4 P3 replication Git profile missing: profile 39 operand family
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
GREEN admission aggregates: 25 TOP_LEVEL, 55 total; max TOP_LEVEL 14 input receipts, 2797 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
GREEN all aggregate maxima: 27 input receipts / 3668 UTF-8 bytes; frozen bounds 64 / 8192 / 262144
RED R8R6: exit 1: R8 R6 cross-context substitution in production tree
GREEN mutation controls: 37 intended RED (26 old + 11 round8), zero filesystem writes
RED R9R1A: exit 1: R9 R1 admission/helper carries A1 authority or science role: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10w_p2_stage.sh
RED R9R1B: exit 1: R9 R1 admission/helper carries A1 authority or science role: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10w_p2_stage.sh
RED R9R1C: exit 1: R9 R1 admission-spawned helper composition not refused: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10w_p2_stage.sh
RED R9R2A: exit 1: R9 R2 direct P1/P3 evaluator bypasses dispatcher projection: profile 4
RED R9R2B: exit 1: R9 R2 direct P1/P3 evaluator bypasses dispatcher projection: profile 6
RED R9R2C: exit 1: R9 R2 caller hit set differs: profile 0
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D15 ADMISSION sites: count pinned_constant=0 loaded_data=0; operand-source pinned_literal=0 loaded_data=0
GREEN D15 SCIENCE sites: count pinned_constant=0 loaded_data=0; operand-source pinned_literal=0 loaded_data=0
GREEN D13 trace: 13 recorded queries, 0 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN admission aggregates: 25 TOP_LEVEL, 55 total; max TOP_LEVEL 14 input receipts, 2797 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
GREEN all aggregate maxima: 27 input receipts / 3668 UTF-8 bytes; frozen bounds 64 / 8192 / 262144
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
RED R9R3A: exit 1: R9 R3 delegation reference foreign profile/context/template: payload_binding_sha256
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D15 ADMISSION sites: count pinned_constant=0 loaded_data=0; operand-source pinned_literal=0 loaded_data=0
GREEN D15 SCIENCE sites: count pinned_constant=0 loaded_data=0; operand-source pinned_literal=0 loaded_data=0
GREEN D13 trace: 13 recorded queries, 0 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN admission aggregates: 25 TOP_LEVEL, 55 total; max TOP_LEVEL 14 input receipts, 2797 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
GREEN all aggregate maxima: 27 input receipts / 3668 UTF-8 bytes; frozen bounds 64 / 8192 / 262144
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
RED R9R3B: exit 1: R9 R3 delegation reference foreign profile/context/template: admission_binding_sha256
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D15 ADMISSION sites: count pinned_constant=0 loaded_data=0; operand-source pinned_literal=0 loaded_data=0
GREEN D15 SCIENCE sites: count pinned_constant=0 loaded_data=0; operand-source pinned_literal=0 loaded_data=0
GREEN D13 trace: 13 recorded queries, 0 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN admission aggregates: 25 TOP_LEVEL, 55 total; max TOP_LEVEL 14 input receipts, 2797 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
GREEN all aggregate maxima: 27 input receipts / 3668 UTF-8 bytes; frozen bounds 64 / 8192 / 262144
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
RED R9R3C: exit 1: R9 R3 process identity disagrees with invocation binding
GREEN mutation controls: 46 intended RED (37 preserved + 9 round9), zero filesystem writes
RED R10A: exit 1: R10 verify-preflight admission-origin carries A1/science authority: /children/15
RED R10B: exit 1: R10 git-ls-files admission-origin carries A1/science authority: /children/17
RED R10C: exit 1: R10 recomputed trace hit-set mismatch: starts-train
FAIL: WRONG RED R10D: R10 verify-preflight admission recipe missing: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10w_p2_stage.sh

EXIT 1
