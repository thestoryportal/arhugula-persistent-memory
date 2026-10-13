# R2W acceptance re-run by MAESTRO58 (2026-10-11 21:39Z)

Builder codexr2w4 replied `R2W FIX READY` at 49% context, with `r2w_report.md` written. MAESTRO58 reran every check from its own shell on these subject bytes. The script is reproduced at the end.

- Subject sha256, recomputed: F10 c49a43ed…, J9 5a5d7c45…, K9 2c1ba6e3…, P7 0e772a48…, I9 b95f3cfe…, test-first record fd8dc6b2…, report b789f53f…. The five subjects match `r2w4_handoff.md` and `r2w_report.md`. They were committed before the report at b0564cdb.
- Inputs and sources: after the builder's reply, `git status --short` over B, `experiments/`, `tools/c10w_p2_gate.py` and `tools/c10w_p2_rerun.py` shows only the new `r2w_report.md`. Every input (F9, J8, K8, P6, I8, C, V11, D15f, D14f, D13f, D9, D8) and source equals HEAD.
- Acceptance 1: `/usr/bin/python3 -B B/check_r2_schemas_v9.py`, exit 0. The default mode loads no profiles, so it derives 0 admission-origin occurrences and 0 D15 sites; acceptance 2 derives 43 and the per-origin site counts.
- Acceptance 2 and 3 ran under `/usr/bin/sandbox-exec -p '(version 1)(allow default)(deny file-write*)'`, both exit 0. Positive control first: the same profile refused a Python file write into B (PermissionError, Errno 1), and no file appeared.
- Acceptance 3 ran a second time under a stricter profile that also denies `process-exec` of `/usr/bin/git`, `/Library/Developer/CommandLineTools/usr/bin/git`, `.venv/bin/python` and its resolved target (`~/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11`). Exit 0, with the same 56 RED lines (identical by `diff`). Positive controls under that profile, run before it: a child `/usr/bin/git` and a child `.venv/bin/python` were both refused (PermissionError), a child `shasum` still ran (rc 0), and a file write into B was refused with no file left behind. R11B's 6 and R12A's seven Git probes, and R12B's 6 + 6 operands, are therefore mocked, not real process starts.
- My GREEN/RED lines for acceptance 2 and 3 are identical by `diff` to the builder's receipts `r2w4_acceptance_profiles.md` and `r2w4_mutation_controls.md`.
- Census (acceptance 3 scope, ruled by MAESTRO58 at 21:33Z the same way as round 11, `r2v_report.md:52`): the builder's readable-area census is recorded with 45 OS-denied macOS subtrees whose contents are unverified (`r2w4_census_summary.md`). The host-level proof is this run: `find B $TMPDIR -newer <mark>` after all runs lists only `$TMPDIR/` and the macOS-owned `TemporaryItems` directory. No file appeared in B.
- Mutation controls: 56 distinct RED lines (53 preserved + 3 D15: R12A, R12B, R12C), each with its own reason.

These are presence and recomputation checks. MAESTRO did not judge the D15 site classifications (37/6 and 232/27 count kinds; 24/19 and 107/152 operand sources), route V's refusal, route T's separate recording, the P1 same-seed family or any refusal; that is Astra's round 12.

Output of acceptance 1:
```
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D15 ADMISSION sites: count pinned_constant=0 loaded_data=0; operand-source pinned_literal=0 loaded_data=0
GREEN D15 SCIENCE sites: count pinned_constant=0 loaded_data=0; operand-source pinned_literal=0 loaded_data=0
GREEN D13 trace: 13 recorded queries, 0 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN: 114 schemas, 17 request kinds, 259 examples validated, 1411 hash references recomputed, 8 bindings rerendered, 16 observations checked
```

Output of acceptance 2 (verbatim):
```
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
```

Output of acceptance 3 under the stricter profile (verbatim):
```
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
RED R10D: exit 1: R10 verify-preflight admission-origin occurrence missing/merged: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10w_p2_stage.sh
GREEN mutation controls: 50 intended RED (46 preserved + 4 D13), zero filesystem writes
RED R11A: exit 1: R11 loaded_data site filtered by argv stage: git-ls-files
R11B fixture: P2 argv p2-shuf-s1; P3 certificate; linked/evidence/authorization prerequisites PASS; 6 mocked Git probes, no file writes or real Git/verifier launches; source reads/path resolution occur
RED R11B: exit 1: R11 reachable admission occurrence missing: verifier-descendant Git, p2-shuf-s1
RED R11C: exit 1: R11 first-stage exclusion unpinned: gate:103
GREEN mutation controls: 53 intended RED (50 preserved + 3 D14), zero filesystem writes
GREEN D15 ADMISSION sites: count pinned_constant=37 loaded_data=6; operand-source pinned_literal=24 loaded_data=19
GREEN D15 SCIENCE sites: count pinned_constant=232 loaded_data=27; operand-source pinned_literal=107 loaded_data=152
R12A fixture: P2 argv/P3 certificate; upstream/link prerequisites PASS; seven distinct mocked Git probes before pinned validate_phase:333 raises; no writes or real Git/verifier launches; source reads/path resolution occur
RED R12A: exit 1: R12 loaded_data count represented by an unpinned constant: verifier-p3
GREEN D15 ADMISSION sites: count pinned_constant=37 loaded_data=6; operand-source pinned_literal=24 loaded_data=19
GREEN D15 SCIENCE sites: count pinned_constant=232 loaded_data=27; operand-source pinned_literal=107 loaded_data=152
R12B fixture: profile 38 p2-eval; eval.json earlier linked adapters versus last-existing train/*.json later adapters; 6 + 6 disjoint mocked Git operands; no writes or real Git/verifier launches; source reads/path resolution occur
RED R12B: exit 1: R12 routes merged without pinned pre-spawn operand equality: profile 38
GREEN D15 ADMISSION sites: count pinned_constant=37 loaded_data=6; operand-source pinned_literal=24 loaded_data=19
GREEN D15 SCIENCE sites: count pinned_constant=232 loaded_data=27; operand-source pinned_literal=107 loaded_data=152
RED R12C: exit 1: R12 count bound unpinned: gate-phase-trains
GREEN mutation controls: 56 intended RED (53 preserved + 3 D15), zero filesystem writes
```

Positive controls and census (verbatim from the run):
```
PC1 deny-write: rc=1 exists=no PermissionError: [Errno 1] Operation not permitted: B/__pc_probe
PC2 strict: /usr/bin/git rc=1 PermissionError; .venv/bin/python rc=1 PermissionError; shasum child rc=0; write rc=1 exists=no PermissionError
A1 rc=0; A2 rc=0; A3 rc=0; A3s rc=0; RED identical; RED count 56, distinct 56
CENSUS: /var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/ and .../T/TemporaryItems only
```

Script (MAESTRO58 scratchpad `r2w_accept.zsh`):
```zsh
#!/bin/zsh
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
B=$W/results/compute_storage_brainstorm_20261011T054507Z
O=${0:h}/r2w_accept_out; rm -rf $O; mkdir -p $O
K=$B/check_r2_schemas_v9.py; P=$B/science_launch_profiles_v7.json
W1='(version 1)(allow default)(deny file-write*)'
W2='(version 1)(allow default)(deny file-write*)(deny process-exec (literal "/usr/bin/git") (literal "/Library/Developer/CommandLineTools/usr/bin/git") (literal "'$W'/.venv/bin/python") (literal "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11"))'
cd $W
touch $O/mark; sleep 1
echo "A1"; /usr/bin/python3 -B $K > $O/a1.txt 2>&1; echo "A1 rc=$?"
echo "PC1 deny-write"; /usr/bin/sandbox-exec -p "$W1" /usr/bin/python3 -B -c "open('$B/__pc_probe','w')" > $O/pc1.txt 2>&1; echo "PC1 rc=$? exists=$([[ -e $B/__pc_probe ]] && echo YES || echo no)"; tail -1 $O/pc1.txt
echo "A2 deny-write"; /usr/bin/sandbox-exec -p "$W1" /usr/bin/python3 -B $K --profiles $P > $O/a2.txt 2>&1; echo "A2 rc=$?"
echo "A3 deny-write"; /usr/bin/sandbox-exec -p "$W1" /usr/bin/python3 -B $K --mutation-controls > $O/a3.txt 2>&1; echo "A3 rc=$?"
echo "PC2 strict"; for c in /usr/bin/git $W/.venv/bin/python; do /usr/bin/sandbox-exec -p "$W2" /usr/bin/python3 -B -c "import subprocess,sys; subprocess.run(['$c','--version'])" > $O/pc2.txt 2>&1; echo "  $c rc=$? $(tail -1 $O/pc2.txt)"; done
/usr/bin/sandbox-exec -p "$W2" /usr/bin/python3 -B -c "import subprocess; print(subprocess.run(['shasum','-a','256','$K'],capture_output=True).returncode)" > $O/pc2s.txt 2>&1; echo "  shasum child rc=$(cat $O/pc2s.txt)"
/usr/bin/sandbox-exec -p "$W2" /usr/bin/python3 -B -c "open('$B/__pc_probe','w')" > $O/pc2w.txt 2>&1; echo "  write rc=$? exists=$([[ -e $B/__pc_probe ]] && echo YES || echo no) $(tail -1 $O/pc2w.txt)"
echo "A3 strict"; /usr/bin/sandbox-exec -p "$W2" /usr/bin/python3 -B $K --mutation-controls > $O/a3s.txt 2>&1; echo "A3s rc=$?"
diff <(grep '^RED' $O/a3.txt) <(grep '^RED' $O/a3s.txt) > /dev/null && echo "RED identical" || echo "RED DIFFER"
echo "RED count a3=$(grep -c '^RED' $O/a3.txt) distinct=$(grep '^RED' $O/a3.txt | sort -u | wc -l | tr -d ' ')"
grep -E 'mocked|R12A|R12B fixture' $O/a3s.txt | cut -c1-200 | head -4
echo "CENSUS"; find $B $TMPDIR -newer $O/mark 2>/dev/null | grep -v "^${O:h}" | head -20
echo DONE
```
