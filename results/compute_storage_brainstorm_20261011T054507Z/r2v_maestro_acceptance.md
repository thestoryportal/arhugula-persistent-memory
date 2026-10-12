# R2V acceptance re-run by MAESTRO56 (2026-10-11 20:31Z)

Builder codexr2v replied `R2V FIX READY` at 46% context, with `r2v_report.md` written. MAESTRO56 reran every check from its own shell on these subject bytes.

- Subject sha256, recomputed: F9 7eb7fda1…, J8 9c5c28bc…, K8 9e7e59cd…, P6 583db6d3…, I8 5bd7762f…, test-first record 60584df6…, report d4848b5e…. All match `r2v_report.md`. F9:326, :327 and :331 pin P6, J8 and I8 at those values. Nothing pins F9's own hash.
- Inputs and sources: `git diff --quiet HEAD` holds for F8, J7, K7, P5, I7, C, V10, D14f, D13f, D9, D8, `tools/c10w_p2_gate.py`, `tools/c10w_p2_rerun.py` and `experiments/track_c/`. The builder added only its seven new files.
- Acceptance 1: `/usr/bin/python3 -B B/check_r2_schemas_v8.py`, exit 0. The default mode loads no profiles, so it derives 0 admission-origin occurrences; acceptance 2 derives 72.
- Acceptance 2 and 3 ran under `/usr/bin/sandbox-exec -p '(version 1)(allow default)(deny file-write*)'`, both exit 0. Positive control: the same profile refused a Python file write into B (PermissionError, Errno 1), and no file appeared.
- Acceptance 3 ran a second time under a stricter profile that also denies `process-exec` of `/usr/bin/git`, `/Library/Developer/CommandLineTools/usr/bin/git`, `.venv/bin/python` and its resolved target (`~/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11`). Exit 0, with the same 53 RED lines (identical by `diff`) and "R11B fixture: … 6 mocked Git probes". Positive controls under that profile: a child `/usr/bin/git` and a child `.venv/bin/python` were both refused (PermissionError), `shasum` still ran (rc 0), and a file write was refused. This shows R11B's Git and verify-preflight calls are mocked, not real process starts.
  - Disclosed: a first stricter attempt denied the whole CommandLineTools subtree, which also stopped `/usr/bin/python3` itself from starting (exit 71, no checks ran), and its literal `.venv` path missed the resolved target. The positive controls exposed both faults. That attempt is not counted.
- Census: `find B $TMPDIR -newer <mark>` after each run lists only `$TMPDIR/` and macOS-owned `TemporaryItems` directories. No file appeared in B.
- Mutation controls: 53 distinct RED lines (50 preserved + 3 D14: R11A, R11B, R11C), each with its own reason.

For Astra to judge (MAESTRO did not rule on it): R11B builds its counterexample by extracting the pinned function bodies of `verify_preflight_certificate`, `authorized_phase_entry`, `replication_for`, `require_untracked_adapter`, `adapter_is_tracked` (`c10w_oracle_read.py`) and `require_training_preflight` (`c10w_oracle_train.py`) with `ast`, and executing them in a namespace where IO, references, authorization and `subprocess.run` are mocked (K8:2467–2513).

These are presence and recomputation checks. MAESTRO did not judge the selector model, the 30 new occurrences, the first-stage exclusion or any refusal; that is Astra's round 11.

Output of acceptance 1:
```
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D13 trace: 13 recorded queries, 0 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN: 114 schemas, 17 request kinds, 259 examples validated, 1411 hash references recomputed, 8 bindings rerendered, 16 observations checked
```
Output of acceptance 2, then the lines acceptance 3 adds beyond acceptance 2's repeated preamble (verbatim, de-duplicated):
```
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D13 trace: 13 recorded queries, 0 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN admission aggregates: 25 TOP_LEVEL, 55 total; max TOP_LEVEL 36 input receipts, 4271 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
GREEN all aggregate maxima: 54 input receipts / 5477 UTF-8 bytes; frozen bounds 64 / 8192 / 262144
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D13 trace: 13 recorded queries, 72 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN production coherence: R1-R4, D1 refusals, 797 binding vectors rerendered; native behavior UNVERIFIED
GREEN profiles: 55 LaunchProfile entries, 0 not_admitted entries schema-validated, 174 not_admitted entries explicit refusals checked
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
RED R10A: exit 1: R10 verify-preflight admission-origin carries A1/science authority: /children/15
RED R10B: exit 1: R10 git-ls-files admission-origin carries A1/science authority: /children/22
RED R10C: exit 1: R10 recomputed trace hit-set mismatch: starts-train
RED R10D: exit 1: R10 verify-preflight admission-origin occurrence missing/merged: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10w_p2_stage.sh
GREEN mutation controls: 50 intended RED (46 preserved + 4 D13), zero filesystem writes
RED R11A: exit 1: R11 loaded_data site filtered by argv stage: git-ls-files
R11B fixture: P2 argv p2-shuf-s1; P3 certificate; linked/evidence/authorization prerequisites PASS; 6 mocked Git probes, zero real IO/spawns
RED R11B: exit 1: R11 reachable admission occurrence missing: verifier-descendant Git, p2-shuf-s1, adapter 0
RED R11C: exit 1: R11 first-stage exclusion unpinned: gate:103
GREEN mutation controls: 53 intended RED (50 preserved + 3 D14), zero filesystem writes
```
