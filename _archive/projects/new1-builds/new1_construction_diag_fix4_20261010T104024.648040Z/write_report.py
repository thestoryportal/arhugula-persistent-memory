"""Build the stopped FIX4 evidence packet from saved receipts."""
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path.cwd();RECEIPT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
audit=json.loads((RECEIPT/'audit_release.json').read_text())
baseline=json.loads((RECEIPT/'baseline.json').read_text())
reds=json.loads((RECEIPT/'red_fix4/index.json').read_text())
greens=json.loads((RECEIPT/'green_fix4/index.json').read_text())
full=json.loads((RECEIPT/'sandbox_full_3/index.json').read_text())[0]
rel=str(RECEIPT.relative_to(ROOT))
solo_name='tests.test_new1_construction_diag.ConstructionDiagnosticTests.test_stalled_launch_returns_within_bound_and_late_handle_cleans_once'
suite_names='tests.test_new1_construction_diag tests.test_new1_identity_diag tests.test_new1_geometry tests.test_new1_supervisor'
solo_command='LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -W error::ResourceWarning -m unittest '+solo_name+' -v'
full_command='LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -W error::ResourceWarning -m unittest '+suite_names+' -v'
host_commands=('LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -W error::ResourceWarning '+rel+'/run_checks.py solo --count 100 --label host_solo_100\n'
               'LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -W error::ResourceWarning '+rel+'/run_checks.py full --count 10 --label host_full_10\n')
(RECEIPT/'host_repetition_commands.txt').write_text(host_commands)
rows=[]
explanations=[
 ('Legacy kills==1 assertion failed with legitimate kills 0/code 2.','(0,2); real worker/guardian reaped once; OS absence and closure at supervisor return.'),
 ('Forced captured group refusal caused guardian escape and parent native exit 2.','(1,-9); worker observed live before guardian termination; ownership closed before return.'),
 ('After WNOHANG observed live, WNOWAIT observed worker exit; group refusal escaped.','(1,2); actual exited status retained after a real attempted termination; one real reap per PID.'),
 ('Setup exception reached PID-tagged inherited-supervisor sentinels.','Guardian native exit 2 inside child lifecycle; explicit no-worker failure proof; parent failure return.'),
 ('Final receipt send exception reached inherited-supervisor sentinels.','Actual worker reaped once before send failure; child remains contained; parent missing-proof fail-stop 2.'),
 ('Dedicated deterministic RED retained parent supervise:612 after signalling refusal.','Ordinary STOPPED-LAUNCH returns with ownership and unittest completion; genuine proof/output failures retain native fail-stops.')]
for index,(red,green) in enumerate(zip(reds,greens),1):
    name=red['targets'][0].rsplit('.',1)[1]
    rows.append('| `'+name+'` | `red_fix4/'+f'{index:03d}.log'+'` — '+explanations[index-1][0]+' | `green_fix4/'+f'{index:03d}.log'+'` — '+explanations[index-1][1]+' |')
hash_rows='\n'.join('| `'+p+'` | `'+h+'` |' for p,h in audit['changed_sha256'].items())
failed_names=[
 'test_blocked_halt_persistence_cannot_extend_total_deadline',
 'test_blocking_admission_is_interrupted_by_whole_run_deadline',
 'test_cell_alarm_interrupts_blocked_persistence_inside_total_cap',
 'test_supervisor_cell_deadline_interrupts_a_blocked_resource_probe',
 'test_watchdog_enforces_during_blocked_persistence',
 'test_watchdog_refuses_memory_drop_during_blocking_admission']
failure_list='\n'.join('- `tests.test_new1_supervisor.SupervisorTests.'+name+'`' for name in failed_names)
text='''# NEW1 FIX4 — MB17 build report

**NEW1 FIX4 STOPPED — sandbox repeatability acceptance failed.** Six new regressions have behavioral RED→GREEN evidence; all 182 existing methods remain. The corrected stalled-launch test passed **20/20 consecutive fresh-process solo runs**. The first required full-suite run completed **188 methods: 182 passed, 6 failed**, exit **1**, with a ResourceWarning. The driver stopped; required full runs 2–3 were not restarted or replaced. This candidate is not accepted and has no launch approval.

MAESTRO11 verifies and commits; GPT-6-Astra reviews. No commit, push, merge, real diagnostic, model/GPU launch, real admission, real numerical input read/rehash or repository artifact deletion was performed. The diagnostic authorization remains unchanged. Receipt budget: 8 MiB; initial free space was **86,346,117,120 bytes**, exceeding that budget plus 20 GiB. Current receipt byte accounting and the final inventory are in `release_manifest.json`.

## Abrupt-exit attribution before implementation (criterion 3)

`observe_abrupt.py` ran the unchanged failing solo schedule from an external process, preserving actual `os._exit` calls. It captured an occurrence on **attempt 1**, below the 200-attempt stop limit. `capture_001.log`, `capture_001.jsonl` and `capture_index.json` preserve exit status 2, absent unittest completion, PID/role, caller stacks, exception history, original deadline remaining and owned PID/proof/descriptor state. Lifecycle source remained SHA **14329bd0daa00bb109010464c26988b5014c6b6e9b92e39152028a9af7033cbe** throughout capture and deterministic replay.

| Role / PID | Observed cause and exit site | Ownership / deadline observation |
|---|---|---|
| Guardian **85274**, owned worker **85275** | `PermissionError(1, 'Operation not permitted')` at old `kill_worker:279`, propagated through `watchdog:340/346` and `OwnedWorker.start:381` into the inherited supervisor. Both inherited cleanup attempts then raised `OSError(9, 'Bad file descriptor')`. Actual `_exit(2)` caller: old `supervise:612`. | Guardian's inherited owner had guardian PID 0, no worker/proof and partly closed channels. Approximately **0.7415 s** remained. This PID was the guardian, not the actual parent. |
| Actual parent **85239** | Primary `STOPPED-LAUNCH: worker creation/registration exceeded launch bound`. Both cleanup attempts raised `INVALID-CLEANUP: guardian exit lacks worker reaping proof`. Actual `_exit(2)` caller: old `supervise:612`. | Guardian exit 2 had been collected; worker PID 85275 was registered, worker proof absent, owned descriptor slots all closed, no streams remained. Approximately **0.7400 s** remained. |

This attributes the newly captured occurrence only. Historical MB15 runs 06 and 18 remain unattributed. The captured trace does not supply the worker's historical exit status or establish why group signalling returned EPERM; no such claim is made.

`deterministic_before/trace.jsonl`, `red.log` and `receipt.json` then forced the captured guardian group-signalling refusal in the same stalled-launch fixture with unchanged lifecycle source. Both guardian and actual parent again reached old `supervise:612`, without unittest completion. Before implementation, the dedicated criterion-3 regression in `red_c3_deterministic/` reproduced that chain with a controlled live pre-release worker. These saved schedules precede the lifecycle edit. Instrumentation logs exceptions and exit callers but invokes the real native exit, without converting it into a return or exception.

## Change and scope

- `kill_worker` now falls back from ProcessLookupError or PermissionError on group signalling to SIGKILL of the already-owned PID. A refused direct PID signal still raises; signal return alone never proves reaping. Kill attempts retain the guardian's actual wait status.
- Guardian signal/session setup now executes inside its existing protected lifecycle, so a setup failure can report the true no-worker-created failure. The raw-fork child branch has an unconditional `_exit(2)` boundary around `watchdog`; setup/final-send exceptions or a returning guardian cannot unwind into inherited supervisor/unittest code.
- The stalled-launch test retains STOPPED-LAUNCH, the **.3 s** bound, **.05 s** launch/cleanup fixture bounds and absent arithmetic marker. The overstrict kills==1 assertion is replaced with worker-proof identity, real guardian/worker OS checks and stream/descriptor closure before fixture teardown. Controlled schedules separately assert (0,2), (1,-9) and (1,2), with no global biconditional.
- The external regression fixture records ownership immediately after the real supervisor returns and before result-file reads or fixture teardown. It counts successful real worker/guardian waitpid collections, probes worker absence, verifies guardian waitpid is already consumed and checks all owned descriptors/streams closed. Exit-between-wait-and-kill uses native waitid(WNOWAIT) only to observe a real exited worker without consuming its waitpid status. Fixture workers are bounded synthetic processes and never reach real arithmetic.
- Construction source and its existing pin test receive the necessary identity-source SHA update. The scope receives an additive **Scope revision — FIX4**, followed by an explicit verification-stop appendix; the initial **107,748 bytes** remain an exact prefix. The tested pre-stop scope SHA is **4e33c59495837e1f6753985cda27d7ef79a51f1e4b2f5724f0396146f754b8c8**. The final scope SHA below adds stop documentation only.

`supervise` is byte-identical to entry, including all three emergency exit bodies, the existing bounded cleanup fallback, timer handling and terminal error recording. No emergency exit was deleted or softened; no retries or caps were added/increased. All other identity functions/class methods are byte-identical except kill_worker/watchdog/OwnedWorker.start. Construction source differs only by its necessary identity pin. Scientific functions, inputs, projector gate, scalar output schema, four constructions and authorization remain unchanged.

## Per-criterion behavioral evidence

All six individual REDs completed a unittest method and failed behaviorally before the implementing change. PID-tagged external records are saved alongside each log. The dedicated C3 deterministic RED additionally proves the captured trigger independent of the removed kill assertion.

| New method | RED | GREEN |
|---|---|---|
'''+ '\n'.join(rows)+'''

The C3 GREEN contains separate externally observed missing-reaping-proof and terminal-output/stderr failures. Each preserves native parent exit **2**, a captured emergency exit caller and exception/deadline evidence, no successful ownership return and no unittest completion. C2's final-send GREEN demonstrates actual worker reaping before the receipt fails and no child escape into the inherited supervisor. Successful ordinary cleanup remains externally distinguishable by a Python return, complete ownership snapshot and completed unittest.

Two harness issues are retained and excluded from behavioral RED or acceptance evidence: an f-string parse failure before any tests executed, corrected before RED capture, and `green_fix4_first/001.log`, which mistakenly classified signal-0 OS ownership probes as termination attempts. The observer event label was corrected; production did not change for that failure. `red_fix4/index.json` initially flagged the text `error::ResourceWarning` in failed assertion metadata as a warning. Its original bytes remain preserved; the audit rescanned actual warning lines and found no ResourceWarning in those six REDs. The required full-run warning below is real and disqualifying.

## Acceptance results and unresolved failure

Method inventory: **66 construction + 27 identity + 34 geometry + 61 supervisor = 188**. All **182 entry methods** remain; **180 are byte-identical**, with only the named stalled-launch assertion and identity pin test changed. No identity/geometry/supervisor test source was edited. New methods: 3 criterion 1, 2 criterion 2, 1 criterion 3.

`sandbox_solo_20/index.json` binds all 20 saved solo logs, source/test hashes, command, exit status, complete one-test results and warning scans. Every run exited 0 and completed OK. No selective restart occurred.

`sandbox_full_3/001.log` / `index.json` record the first required full command, **Ran 188 tests in 34.615 s / FAILED (failures=6)**, native exit 1, approximately **34.800 s** wall time. The six failures were:

'''+failure_list+'''

Observed mismatches include elapsed **2.0103 s versus <.3 s**, **1.0123 s versus <.2 s**, **.2811 s versus <.2 s**, INVALID-ADMISSION instead of STOPPED-DEADLINE, STOPPED-DEADLINE instead of STOPPED-RESOURCE, and INVALID-WORKER instead of STOPPED-RESOURCE. The log also reports `ResourceWarning: subprocess 25689 is still running` from Popen.__del__. All six new FIX4 methods passed within that run, but full-suite acceptance failed.

The failing deadline fixture passed in a separate fresh-process solo control (`supervisor_solo_control.log/json`). A diagnostic-only run of the complete sequence under `observe_suite_state.py` reported **188 passing methods** (`suite_state.log`, `suite_state_result.json`). Its **376 before/after samples** (`suite_state.json`) recorded empty main-thread signal masks, default SIGALRM handlers and inactive timers. That observation rules out a persistent main-thread mask/handler/timer leak at those boundaries, not all possible interference. The timing/signal mechanism remains unresolved. Protected source/test hashes remained identical; this does not establish whether the first failure predates FIX4 or is caused by the candidate.

The diagnostic PASS does not replace the failed required run. Required full runs 2–3 remain **UNRUN** after the fail-stop, and the accepted required full-run count is **0/3**. Discarding the failed run or starting a fresh success count on the same unchanged candidate would violate the no-selective-restart contract. No unrelated protected-file fix or cap relaxation was attempted. MB17 therefore stops without a DONE claim.

The exact failing full command was:

```sh
'''+full_command+'''
```

The exact corrected solo command was:

```sh
'''+solo_command+'''
```

## Static audit, receipts and pins

`audit_release.py`, `audit_release.log/json` and `audit_command.json` report **STATIC-PASS / ACCEPTANCE-FAIL**, exit **1**. The auditor retains the failure gate; it does not relabel the failed repetition as PASS. It verifies the allowed lifecycle diff, byte-identical supervisor/Output/scientific/helper bodies, constant/source/input assignments, construction-only pin change, all existing methods, scope prefix, current source pins and historical source, protected files, prior receipts, REDs/GREENs, every repetition log/hash and the exact unexecuted launch command. It imports no torch/numpy/transformers/safetensors, runs no admission and reads no numerical input.

**19 protected files** and **181 pre-existing receipt files** match entry hashes. This includes dashboard, Drive-backup and launchd exclusions as inventoried in baseline.json. Concurrent unrelated work was preserved. A scoped diff against MB17's actual entry snapshots is saved in `mb17_changed.diff`; the broader git HEAD diff contains prior builders' work and is not MB17's change inventory.

| Changed existing file | Final SHA-256 |
|---|---|
'''+hash_rows+'''

`release_manifest.json` binds these hashes, the unchanged protected inventory, current source/input pin dictionaries, audit/acceptance states and SHA-256/byte counts of every fresh receipt except itself. Before hashes/copies are in `baseline.json` and `before_*`. New receipts were absent at entry. `launch_command.txt` is generated from the unchanged source launch-command function with the final scope and construction-source hashes, read back exactly and **not executed**. It is a review artifact, not launch approval. The nice increment, environment, source/input checks, namespace, output contract and authorization remain the existing launch contract.

## Exact MAESTRO host repetition commands — UNRUN

Run from the branch worktree only after review of this stopped candidate. The recorder creates fresh directories, invokes the exact fresh-process unittest commands with -B, PYTHONDONTWRITEBYTECODE=1 and -W error::ResourceWarning, preserves every log/status/source hash, rejects incomplete counts/warnings/timeouts/ignored exceptions and stops on the first failure. Existing directory reuse refuses; no selective restarting is authorized.

```sh
'''+host_commands+'''
```

These commands request **100 solo + 10 full-suite** host runs. None were run by MB17. Sandbox and host repetition are practical thresholds, not proofs of non-flakiness; deterministic schedule coverage remains essential.

## Handoff to MAESTRO11 / Astra

Completed: criterion-3 capture and deterministic unchanged-source replay; six numbered RED→GREEN regressions; minimal lifecycle containment/signalling correction; immediate ownership checks; all 182 existing methods retained; scope prefix and protected/prior receipts preserved; 20 consecutive solo pre-checks; all evidence, audit, final pins and unexecuted launch command refreshed. No source edit is half-applied.

Open: first required full-suite run failed six existing deadline/resource methods and emitted a ResourceWarning. The diagnostic-only full PASS does not clear that failure. Further required sandbox repetitions, host 100/10 repetition and binding Astra acceptance remain unestablished. No real scientific/GPU/model/admission work or commit/merge is permitted by this packet.

Exact changed paths and SHA-256 values are the table above and release_manifest.json. The exact failing command and six method IDs are above; saved failure evidence is `sandbox_full_3/001.log`. Next step: MAESTRO11/Astra review that failure and the signal-state controls, determine the minimal authorized investigation/fix if one is necessary, then qualify an explicitly reviewed candidate with all failures retained. Do not overwrite or read around the failed batch or treat the written launch command as approval.

**Binding context directive, restated:** watch Context N% left. Start a new piece of work only at **60% left or more**. At **40% left or less**, stop starting work, append a handoff at the end of build_report.md with completed/half-applied work, exact changed paths and SHA-256 values, failing tests/exact commands and next step, then reply **CONTEXT HANDOFF WRITTEN**. If context is compacted, do so immediately. Restate this directive in every handoff.
'''
initial=RECEIPT/'build_report.md'
if not (RECEIPT/'build_report_initial.md').exists():
    (RECEIPT/'build_report_initial.md').write_bytes(initial.read_bytes())
initial.write_text(text)
diff=[]
for path in baseline['before']:
    original=(RECEIPT/('before_'+Path(path).name)).read_text().splitlines(True)
    current=(ROOT/path).read_text().splitlines(True)
    diff.extend(difflib.unified_diff(original,current,fromfile='MB17-entry/'+path,tofile=path))
(RECEIPT/'mb17_changed.diff').write_text(''.join(diff))
from tools import new1_construction_diag as D
assert all(sha(ROOT/p)==h for p,h in audit['changed_sha256'].items())
inventory={str(p.relative_to(RECEIPT)):{'sha256':sha(p),'bytes':p.stat().st_size}
           for p in RECEIPT.rglob('*') if p.is_file() and p.name!='release_manifest.json'}
manifest=dict(utc=datetime.now(timezone.utc).isoformat(),status='NEW1 FIX4 STOPPED',
    changed_sha256=audit['changed_sha256'],before_sha256=baseline['before'],protected_sha256=baseline['protected'],
    scope_prefix_bytes=audit['scope_prefix_bytes'],source_pins=D.SOURCE_PINS,input_pins=D.INPUT_PINS,
    new_tests=6,existing_methods=182,total_methods=188,solo_passes=20,required_full_saved=1,
    required_full_accepted=0,required_full_failures=6,diagnostic_only_full_tests=188,
    audit_status=audit['status'],launch_executed=False,host_repetitions_executed=False,
    receipt_bytes=sum(v['bytes'] for v in inventory.values()),receipt_budget_bytes=8388608,receipts=inventory)
assert manifest['receipt_bytes']<manifest['receipt_budget_bytes']
(RECEIPT/'release_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(dict(report=str(initial),manifest_sha256=sha(RECEIPT/'release_manifest.json'),
                     receipt_bytes=manifest['receipt_bytes'],changed_sha256=audit['changed_sha256'])))
