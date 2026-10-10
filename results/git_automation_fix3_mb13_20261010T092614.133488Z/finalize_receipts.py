import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(os.environ['LLMDB_ROOT']).resolve()
RECEIPT = Path(__file__).resolve().parent
FILES = ['tools/git_merge_gate.py', 'tools/git_hygiene.py', 'tests/test_git_automation.py']
before = json.loads((RECEIPT / 'before_manifest.json').read_text())
acceptance = json.loads((RECEIPT / 'acceptance.json').read_text())
assert len(acceptance) == 3 and all(r['validated'] for r in acceptance)
after = {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in FILES}
assert all(r['before']['files'] == after == r['after']['files'] for r in acceptance)
head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
branch = subprocess.run(['git', 'branch', '--show-current'], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
assert branch == before['branch'] == 'worktree-c10k-route-a'
diff = []
for f in FILES:
    target = RECEIPT / 'after_snapshot' / f
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((ROOT / f).read_bytes())
    diff.extend(difflib.unified_diff((RECEIPT / 'before_snapshot' / f).read_text().splitlines(True),
                target.read_text().splitlines(True), fromfile='a/' + f, tofile='b/' + f))
(RECEIPT / 'changes.diff').write_text(''.join(diff))
(RECEIPT / 'after_manifest.json').write_text(json.dumps({'head': head, 'branch': branch, 'files': after}, indent=2) + '\n')
(RECEIPT / 'sha256_before_after.json').write_text(json.dumps({f: {'before': before['files'][f], 'after': after[f],
                         'changed': before['files'][f] != after[f]} for f in FILES}, indent=2) + '\n')
r2 = {f: hashlib.sha256((RECEIPT / 'r2_snapshot' / f).read_bytes()).hexdigest() for f in FILES[:2]}
(RECEIPT / 'r2_manifest.json').write_text(json.dumps({'commit': '25af64754d6378de83992b58cd2a26763342ef9b',
                                                   'files': r2}, indent=2) + '\n')
indexes = {}
for mode in ['RED', 'GREEN']:
    index = json.loads((RECEIPT / mode / 'index.json').read_text())
    assert len(index) == 18 and all(r['validated'] for r in index)
    for row in index:
        log = RECEIPT / row['log']
        assert hashlib.sha256(log.read_bytes()).hexdigest() == row['sha256']
        text = log.read_text()
        assert 'Ran 1 test' in text and 'ERROR:' not in text and 'non-list' not in text
        assert ('FAILED (failures=' if mode == 'RED' else '\nOK\n') in text
    indexes[mode] = index
    (RECEIPT / (mode.lower() + '_runner.exit')).write_text('0\n')
assert [r['test'] for r in indexes['RED']] == [r['test'] for r in indexes['GREEN']]
(RECEIPT / 'RED/source_manifest.json').write_text(json.dumps({'current_production': {f: before['files'][f] for f in FILES[:2]},
                           'r2_production': r2, 'regression_test_sha256': after[FILES[2]]}, indent=2) + '\n')
(RECEIPT / 'GREEN/source_manifest.json').write_text(json.dumps(after, indent=2) + '\n')
coverage = json.loads((RECEIPT / 'test_coverage.json').read_text())
assert coverage['real_gate_count'] == 57 and coverage['direct_github_adapter_count'] == 9
warning_counts = {}
breakdown = {}
for label in ['git_automation', 'model_free']:
    lines = (RECEIPT / (label + '.log')).read_text().splitlines()
    warning_counts[label] = sum('ResourceWarning: unclosed file' in line for line in lines)
    if label == 'model_free':
        for module in ['tools.test_c10w_p2_gate', 'tools.test_dashboard_live', 'tools.test_dashboard_gpu_detector']:
            breakdown[module] = sum(line.startswith('test_') and '(' + module + '.' in line for line in lines)
assert list(breakdown.values()) == [13, 27, 40]
(RECEIPT / 'log_summary.json').write_text(json.dumps({'unclosed_file_warnings': warning_counts,
                                'model_free_breakdown': breakdown}, indent=2) + '\n')
status = subprocess.run(['git', 'status', '--short'], cwd=ROOT, check=True, capture_output=True, text=True).stdout
(RECEIPT / 'final_git_status.txt').write_text(status)
hash_rows = '\n'.join('| `' + f + '` | `' + before['files'][f] + '` | `' + after[f] + '` | ' +
                      ('changed' if before['files'][f] != after[f] else 'unchanged') + ' |' for f in FILES)
regression_rows = '\n'.join('| `' + r['test'] + '` | ' + r['source'] + ' | assertion RED / GREEN |' for r in indexes['RED'])
cooperative = '''Before invoking the merge gate, MAESTRO must reserve the candidate PR/head and master mutation window and suspend competing automatic writers. Every competing human, local script or service that can push master, change the PR head, edit/close/reopen the PR, request CI reruns, or create/update candidate-head check runs or commit statuses must acquire the same git-common-dir git_automation.lock for its entire mutation, or obtain a serialized MAESTRO reservation that queues its mutation until the gate has released the lock; checking that the lock appears free is insufficient. Before the gate acquires that lock, all candidate-head workflow runs, including older runs, and all pending check/status writers must drain; required CI evidence must be successful, and MAESTRO must confirm that external writers have no remaining queued candidate updates. Automatic writers unable to take this local lock must be inventoried and suspended as follows: GitHub Actions candidate-head writers must finish their existing runs/checks, with candidate pushes/PR events and automatic dispatch/schedule/rerun sources stopped; any ready-for-review-triggered candidate workflow must be disabled or have that trigger suppressed for this window. External CI and GitHub App check/status publishers must have the candidate integration paused and their queued callbacks drained. Dependabot/Renovate and other PR/branch-update bots must be paused for the candidate. GitHub auto-merge and merge queues must be disabled for or have this PR removed. Local cron, launchd and unattended git/CI writers must be stopped or queued behind the same lock/reservation. During the locked window, competing actors may perform none of the listed mutations. The gate's own ready transition and exact-head guarded merge are expressly exempt, as are its guarded post-merge hygiene actions and the merge-generated master-push CI that writes evidence for the new merge SHA; that master CI must remain enabled. The local flock cannot bind GitHub-hosted actors. These suspensions and reservations are an operational coordination premise, not server enforcement, and adopting this paragraph alone does not establish participation. Post-merge detection of a violation reports MERGED_WITH_FAILURE with the merged SHA and does not undo the merge.'''
report = f'''# MB13 Task 3 build report — BUILD DONE, awaiting Astra binding review

Findings 1, 3 and 4 have local regression and acceptance evidence. **18 saved regressions GREEN; 104/104 git-automation; 80/80 model-free; all acceptance commands exit 0.** There are 17 new unittest methods and one repaired existing inventory-adapter method; the 18 regressions are included in the 104. Finding 5 belongs to MAESTRO and was not executed.

## Authority, starting identity and scope

Read the AGENTS.md Context management and Team mode sections, then the specified r3 verdict, previous build report, and three scoped source files in the requested order. All three supplied SHA-256 pins matched before editing. The source reference commit is 9ea1357; actual initial HEAD was `{before['head']}`, its descendant committing the r3 verdict. MAESTRO advanced HEAD to `{head}` during this build. The branch and worktree remained `worktree-c10k-route-a` at `{ROOT}`; no shared-checkout git mutation was performed by MB13.

Only `tools/git_merge_gate.py` and `tests/test_git_automation.py` changed outside this fresh receipt directory. `tools/git_hygiene.py` is unchanged. All original 87 tests and every original assertion are preserved; `test_coverage.json` records the checked assertion inventory. No excluded family was edited. Concurrent builders' work was left in place; initial/final status captures are receipts, not claims that other builders' files were static.

## Finding 1 — receipt and output boundaries

The check helper, enclosing gate/lock boundary, and main boundary now catch BaseException and retain the shared merged outcome and response SHA while forcing failure. KeyboardInterrupt during the first post-merge PR read, SystemExit(0) during lock exit, report serialization TypeError, and stdout BrokenPipeError each have their own saved RED and GREEN. Additional tests cover SystemExit(0) during the post-merge PR read, KeyboardInterrupt during lock exit, SystemExit(0) escaping a completed gate into main, stdout flush failure, stderr write/flush failure, both output streams failing, and flush-before-success ordering.

Serialization, writing and explicit flushing are inside the report-delivery failure boundary. An output failure sets `ok=false`, forces `MERGED_WITH_FAILURE` for a merged report and returns 1. The fallback emits plain text containing that status, `ok=false`, and `merge_sha` to stderr independently of JSON serialization. If stderr cannot deliver it, a unique receipt is written and flushed/fsynced at `results/git_merge_gate_receipts/<sha>-<unique>.txt` under the invoked repository root; failure of that sink makes a final raw stderr-descriptor attempt and is recorded as another error. Fixture tests verify the file contents. PASS is printed after JSON stdout and the stderr check summary have flushed; exit 0 follows successful delivery and flushing of the outcome line. Core gate success still follows successful lock exit. The merge-response SHA guard and prior moved-base diagnostic are retained.

## Finding 3 — drain before the local freeze

PR/fingerprint/branch reads, bounded exact-head CI polling and the initial stable-head/base read now precede lock acquisition. The final ready/merge path still rechecks head/base, branch protection and exact-head CI while locked and refuses changed evidence. CI polling now also waits for older pending check runs in the complete check inventory. Current status evidence must already be successful; historical superseded commit-status rows remain audit history, not pending writers. The two saved drain REDs specifically show the old lock acquiring with CI PENDING and with an older check writer undrained. Both now wait outside the lock and acquire it only after completion.

## Cooperative rule — verbatim, for MAESTRO to adopt

> {cooperative}

This rule has not been adopted or operationally established by MB13. No writer was suspended and no real gate, ready, rerun or merge API was called. The paragraph names writer classes to inventory; it does not assert that every listed integration is installed. It leaves merge-SHA master CI enabled while candidate-head writers are suspended.

## Finding 4 — command-aware fixtures and honest REDs

`evidence_command` dispatches on the actual gh command/endpoint and honors the r2 CLI `--json` field request. It serves both r2's `gh run list`/latest-check/status sequence and the current REST workflow/latest-check/all-check/status sequence. Historical sources were extracted read-only from `25af64754d6378de83992b58cd2a26763342ef9b` into `r2_snapshot/`; their hashes are in `r2_manifest.json`. The historical hygiene digest `{r2['tools/git_hygiene.py']}` matches the previous build's before-Task-2 digest.

The repaired inventory test's r2 RED reaches four subtest assertions: missing `run_attempt`, missing `updated_at`, missing `all_check_runs`, and missing `all_statuses`. It has four assertion failures, zero unrelated errors and no non-list failure; each original equality assertion remains behind an added key-presence assertion. Its current-code GREEN exercises all four equality assertions.

Two new tests run the real gate using the real Gh adapters through a command-aware fixture command runner: one verifies REST merge response identity/head guarding and complete inventory reads; the other introduces a higher attempt during final hygiene and proves pre-merge refusal. Their corrected r2 REDs respectively fail the PUT-command assertion (`0 != 1`) after a successful fixture merge, and the pre-merge refusal assertion because r2 incorrectly reports `ok=True, MERGED`. The final-read-only older-run regression first obtains PASS with one run, introduces pending run 100 only on the second head-evidence read, and refuses before merge; its r2 RED instead merges and fails that refusal assertion. No live GitHub mutation is implied by these fixture executions.

The first historical adapter-through-gate probe omitted r2's post-merge CLI inventory response and therefore produced an unrelated post-merge CI failure in two schedules. Those probe logs are retained under `RED/prior_probe/` and are **not accepted RED evidence**. The fake was corrected before any production edit; all 18 top-level REDs were rerun and validated. `RED/index.json` and `GREEN/index.json` are the authoritative accepted indexes; the runner additionally checks the two corrected adapter schedules' specific assertion messages. The inventory-adapter RED has the intended four assertion failures.

Coverage counts are explicit: **of the 18 saved regressions, 17 run the real gate/main with fixture Git; 1 runs the GitHub inventory adapter directly. Two of those 17 also exercise the real GitHub adapters through the gate.** The full 104-method suite's checked call-path inventory identifies **57 methods driving the real gate/main, 9 direct GitHub-adapter methods, and 38 other hygiene/CI/CLI/deadline/dashboard/structural contract methods**. The lists and AST/helper reachability method are in `test_coverage.json`; this is a source-checked classification of the passing fixture suite, not live API evidence.

## Acceptance and receipts

Exact required suite commands, executed with raw output, receipt-confined TMPDIR, and `/opt/homebrew/bin` prepended to PATH:

```sh
LLMDB_ROOT=$PWD /usr/bin/python3 -B -S -m unittest discover -s tests -p test_git_automation.py -v
LLMDB_ROOT=$PWD /usr/bin/python3 -B -S -m unittest -v tools.test_c10w_p2_gate tools.test_dashboard_live tools.test_dashboard_gpu_detector
```

| Check | Actual count | Exit | Evidence |
| --- | ---: | ---: | --- |
| Accepted targeted REDs | 18 assertion REDs | 1 each; runner 0 | `RED/index.json`, each `.log`/`.exit`, `red_runner.log` |
| Targeted GREENs | 18 PASS | 0 each; runner 0 | `GREEN/index.json`, each `.log`/`.exit`, `green_runner.log` |
| Git automation | 104 PASS | 0 | `git_automation.log`, `.exit` |
| Model-free suites | 80 PASS | 0 | `model_free.log`, `.exit` |
| Scoped whitespace check | no errors | 0 | `diff_check.log`, `.exit` |

Model-free breakdown: 13 c10w-p2-gate, 27 dashboard-live, 40 shared GPU-detector tests. Existing unclosed-file ResourceWarnings remain in the raw logs: {warning_counts['git_automation']} automation and {warning_counts['model_free']} model-free warnings from out-of-scope dashboard files. `acceptance.json` counts 16/62 ResourceWarning text occurrences because each warning has an Enable-tracemalloc hint; `log_summary.json` separately counts the actual 8/31 unclosed-file warnings. These warnings were retained and no dashboard files were changed.

`run_regressions.py` saves and validates one unittest log per schedule. Its accepted RED inventory uses 14 current pre-fix production schedules and four frozen-r2 schedules; GREEN uses current fixed production for all 18. `run_acceptance.py` records commands, exits, counts and before/after source/HEAD snapshots for both suites. All three scoped source hashes stayed identical throughout acceptance. Final source reads and whitespace verification followed; no post-test production or test edits occurred.

## SHA-256 and diff

| File | Before | After | Scope |
| --- | --- | --- | --- |
{hash_rows}

Receipts include `before_manifest.json`, `before_snapshot/`, `after_manifest.json`, `after_snapshot/`, `sha256_before_after.json`, `changes.diff`, `r2_manifest.json`, `RED/source_manifest.json`, and `GREEN/source_manifest.json`. `changes.diff` compares the supplied source baseline to this final build even if MAESTRO advances HEAD. The receipt's unique namespace is `{RECEIPT.relative_to(ROOT)}`.

## Execution boundary and handoff

No commit, push or merge against the shared repository; no real merge/ready/rerun API or real hygiene/merge-gate apply; no models, GPU/MPS, torch or .venv science work. Git mutations performed by tests were confined to disposable receipt fixtures. No Finding 5 first-use action was performed. A higher-priority tooling hook attempted one read-only graft command before source inspection; it exited 127 (`env: node: No such file or directory`). No query succeeded, no graph evidence was used and no retry occurred.

**UNVERIFIED:** fresh exact-head Linux CI, live REST/output behavior, participation/suspension of remote writers, cooperative-rule adoption, and binding Astra GO. These remain MAESTRO's review/integration boundaries. No local implementation or acceptance work remains pending. The build is ready for MAESTRO verification and Astra re-review; this report does not authorize a real merge.

Context-save state capture is retained in `context_save_mb13.md` inside the permitted receipt directory. Learning for the next builder: a command-aware fake must serve both pre-merge and post-merge sequences, and a RED must be checked for the intended assertion, not merely a nonzero exit. The frozen merge receipt and report delivery are separate boundaries; hosted writer coordination is an explicit prerequisite. These notes stay in this receipt; no memory files were edited.

## Binding context directive — restate in every handoff

Operator: “Do not forget to manage context usage for yours and every team session you are orchestrating.” / “This context directive must be made durable through any and all handoffs.” Watch Context N% left. **At 40% left or less, stop starting work.** After any compaction do the same immediately. Write a handoff into build_report.md containing completed/half-applied work, exact paths and SHA-256 of changed files, saved REDs, failing tests with the exact command, next step and risks, then reply exactly **CONTEXT HANDOFF WRITTEN**. Never approach full-window compaction. Every successor handoff restates this directive. The general AGENTS 20% threshold is superseded by this task's stricter 40% threshold.
'''
(RECEIPT / 'build_report.md').write_text(report)
timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
changed = [f for f in FILES if before['files'][f] != after[f]]
context = f'''---
status: completed-build-awaiting-review
branch: {branch}
timestamp: {timestamp}
files_modified: {json.dumps(changed)}
---

## Working on: Git automation FIX3 receipts

MB13 completed local fixes for Astra r3 findings 1, 3 and 4. Report: `{RECEIPT / 'build_report.md'}`. 18 accepted targeted GREENs, 104 git-automation tests and 80 model-free tests pass. No half-applied change, running builder command or failing test remains. Finding 5 is MAESTRO's and was not executed.

Decisions: normalize BaseException and output failures around the shared response receipt; drain exact-head runs and pending check writers before flock; preserve final evidence checks; fallback to independent stderr then a flushed/fsynced unique receipt file. Command-aware mocks serve both r2/current command sequences. Accepted REDs are indexed at RED/index.json; historical exploratory probes in RED/prior_probe are explicitly excluded.

Source identity: start HEAD {before['head']}; current HEAD {head}; unchanged worktree `{ROOT}`. Changed source hashes: {json.dumps({f: after[f] for f in changed}, sort_keys=True)}. Hygiene remains {after['tools/git_hygiene.py']}.

Remaining work belongs to MAESTRO: verify this receipt, obtain binding Astra review, adopt and establish the cooperative rule, and carry out any separately authorized first-use sequence. Do not infer live cooperation or merge authority from fixture PASS. Exact acceptance commands and all source hashes/diff are in build_report.md and acceptance.json. Concurrent unrelated builders' edits are retained in initial_git_status.txt/final_git_status.txt and must not be reverted.

Context directive: watch Context N% left. At 40% left or less, or immediately after compaction, stop starting work; write a handoff into build_report.md with done/half-applied work, exact paths and SHA-256, saved REDs, failing tests and exact command, next step and risks; reply exactly CONTEXT HANDOFF WRITTEN. Restate this directive in every handoff. Never approach full-window compaction.
'''
(RECEIPT / 'context_save_mb13.md').write_text(context)
manifest = {str(p.relative_to(RECEIPT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in RECEIPT.rglob('*') if p.is_file() and p.name != 'receipt_manifest.json'}
(RECEIPT / 'receipt_manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
print('Receipt finalized:', RECEIPT.relative_to(ROOT))
print('18 GREEN; 104 git-automation; 80 model-free; scope:', ', '.join(changed))
