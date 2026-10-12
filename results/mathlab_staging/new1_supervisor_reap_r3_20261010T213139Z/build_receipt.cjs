'use strict';
const fs=require('node:fs'), path=require('node:path'), crypto=require('node:crypto'), assert=require('node:assert/strict');
const receipt=__dirname, root=process.cwd();
const command='LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest -v tests.test_new1_supervisor';
const pins={
  'tools/new1_supervisor.py':'e61d4802fa6c9d4b6a8ecb1c4f612e0a1285a5e21bf104d5ea8f5e1c7e93d65a',
  'tests/test_new1_supervisor.py':'4e8d70a1695a48a6eb3a04d7eee7b41a3a7923c6a26cd3fe96f538ca46e81c90'
};
const read=p=>fs.readFileSync(p,'utf8'), sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const r=p=>path.join(receipt,p), w=p=>path.join(root,p);
const source=read(w('tools/new1_supervisor.py')), tests=read(w('tests/test_new1_supervisor.py'));
const beforeSource=read(r('before/new1_supervisor.py')), beforeTests=read(r('before/test_new1_supervisor.py'));
const red=read(r('RED_causal.log')), green=read(r('GREEN.log'));
const line=(text,needle)=>{const i=text.split('\n').findIndex(s=>s.includes(needle)); assert(i>=0,needle); return i+1;};
const names=text=>[...text.matchAll(/^    def (test_\w+)\(/gm)].map(m=>m[1]);
const baselineNames=names(beforeTests), finalNames=names(tests), additions=finalNames.filter(n=>!baselineNames.includes(n));
assert.equal(sha(r('before/new1_supervisor.py')),pins['tools/new1_supervisor.py']);
assert.equal(sha(r('before/test_new1_supervisor.py')),pins['tests/test_new1_supervisor.py']);
assert.equal(baselineNames.length,94); assert.equal(finalNames.length,97); assert.equal(additions.length,3);
const insertedStart=tests.indexOf('    def test_interrupted_poll_never_signals_pid_released_before_returncode(self):');
const insertedEnd=tests.indexOf('    def test_pid_fallback_ownership_check_cannot_be_interrupted_by_watchdog_poll(self):',insertedStart);
assert(insertedStart>=0 && insertedEnd>insertedStart);
assert.equal(tests.slice(0,insertedStart)+tests.slice(insertedEnd),beforeTests,'all existing tests and helpers must be byte-identical');
assert.equal(source.slice(0,source.indexOf('@contextlib.contextmanager\ndef worker_reaping():')),
  beforeSource.slice(0,beforeSource.indexOf('def kill_worker(process):')),'accepted prefix including caps and constructor must be unchanged');
const predictionBlock=text=>text.slice(text.indexOf('def publish_predictions('),text.indexOf('def supervise('));
assert.equal(predictionBlock(source),predictionBlock(beforeSource));
const closeout=text=>text.slice(text.indexOf('\n    except BaseException as error:\n        # The exact fsynced inode'));
assert.equal(closeout(source),closeout(beforeSource),'terminal authority, halt budget, endpoint close and exit mapping must be unchanged');
assert.equal(read(r('RED_causal.exit')).trim(),'1'); assert.equal(read(r('GREEN.exit')).trim(),'0');
assert.match(red,/^Ran 97 tests /m); assert.match(red,/^FAILED \(failures=8\)$/m); assert(!/^ERROR:/m.test(red));
assert.match(green,/^Ran 97 tests /m); assert.match(green,/^OK$/m); assert(!/^(FAIL|ERROR):/m.test(green));
const failures=[...red.matchAll(/^FAIL: (test_\w+).*$/gm)].map(m=>m[1]);
assert.equal(failures.length,8); assert(failures.every(n=>additions.includes(n)));
assert.equal(sha(r('RED_causal_tests.py')),sha(w('tests/test_new1_supervisor.py')));
assert.equal(sha(r('GREEN_tests.py')),sha(w('tests/test_new1_supervisor.py')));
assert.equal(sha(r('GREEN_supervisor.py')),sha(w('tools/new1_supervisor.py')));
assert.equal((source.match(/process\.poll\(/g)||[]).length,1);
assert.equal((source.match(/process\.wait\(/g)||[]).length,2);
const sourceStat=fs.statSync(w('tools/new1_supervisor.py')), redStat=fs.statSync(r('RED_causal.log')), greenStat=fs.statSync(r('GREEN.log'));
assert(redStat.mtimeMs<=sourceStat.mtimeMs && sourceStat.mtimeMs<=greenStat.birthtimeMs,'causal RED must precede source edit and GREEN start');
const phase=(file,exitFile)=>({
  log:path.relative(root,r(file)), log_sha256:sha(r(file)), command,
  exit_code:Number(read(r(exitFile)).trim()), tests:97,
  failures:file==='GREEN.log'?0:8, errors:0,
  started_utc:fs.statSync(r(file)).birthtime.toISOString(), finished_utc:fs.statSync(r(file)).mtime.toISOString()
});
const boundaries=[
  ['Constructor deferred delivery','constructor_ownership(process)', 'Unchanged selector; original controls retained. Existing constructor fixtures.'],
  ['Signal-mask restoration','def worker_reaping()', 'Selector applies before a restoration error can replace the in-flight error.'],
  ['Single-PID fallback','def kill_worker(process)', 'Ownership check and signal share the guard; completed reaps prohibit PID fallback.'],
  ['Termination signal then wait','def terminate(process)', 'First signal error and wait error use the selector; always attempts the bounded wait. New causal termination regression.'],
  ['Heartbeat signal cleanup','def heartbeat()', 'New cleanup control is raised; lifetime reaping follows. Original controls still win. New and existing heartbeat regressions.'],
  ['Lifetime signal and reap','def worker_lifetime()', 'Original/control/signalling/wait precedence preserved; one five-second retry deadline. Successful reap flag is stored before deferred delivery. Existing lifetime regressions.'],
  ['Terminal commit verification','except BaseException as verification_error:', 'Unchanged accepted terminal authority and control precedence; postcommit fixtures.'],
  ['Halt closeout','except BaseException as closeout_error:', 'Unchanged accepted control precedence and original remaining-budget rule; halt failure fixtures.'],
  ['Endpoint closing','except BaseException as close_error:', 'Unchanged selector; close failure fixture.'],
  ['Stderr reporting','def report_error(', 'Unchanged reporting-note rule, including failed stderr fixtures.']
].map(([name,needle,check])=>({name,line:line(source,needle),check}));
const evidence={
  receipt:path.relative(root,receipt), branch:'worktree-c10k-route-a', status:'BUILD_DONE_FIXTURE_ONLY',
  source_identity:{
    'tools/new1_supervisor.py':{start_sha256:pins['tools/new1_supervisor.py'],final_sha256:sha(w('tools/new1_supervisor.py'))},
    'tests/test_new1_supervisor.py':{start_sha256:pins['tests/test_new1_supervisor.py'],final_sha256:sha(w('tests/test_new1_supervisor.py'))}
  },
  red:{...phase('RED_causal.log','RED_causal.exit'),supervisor_sha256:pins['tools/new1_supervisor.py'],tests_sha256:sha(r('RED_causal_tests.py')), failing_methods:[...new Set(failures)]},
  green:{...phase('GREEN.log','GREEN.exit'),supervisor_sha256:sha(w('tools/new1_supervisor.py')),tests_sha256:sha(w('tests/test_new1_supervisor.py'))},
  rejected_initial_red:{...phase('RED.log','RED.exit'),tests_sha256:sha(r('RED_tests.py')),reason:'Heartbeat observe injection ran during pre-worker controller.check; its two wait-count failures are not causal blocker-2 evidence.'},
  checks:{baseline_methods:94,new_methods:additions,all_existing_tests_and_helpers_byte_identical:true,
    accepted_prefix_and_constructor_unchanged:true,prediction_publication_unchanged:true,
    terminal_closeout_and_exit_mapping_unchanged:true,all_worker_poll_wait_calls_guarded:true,red_before_source_edit_before_green:true,
    git_diff_check:'passed'},
  ownership_strategy:{signals:['SIGINT','SIGALRM'],poll:'nonblocking',wait_max_timeout_s:5,
    retry_budget_s:5,mask_scope:'Main-thread worker poll, bounded worker wait, and nonblocking PID ownership-check/signal; each prior mask restored.'},
  boundaries_checked:boundaries,
  artifacts:Object.fromEntries(['before/new1_supervisor.py','before/test_new1_supervisor.py','RED.log','RED.exit','RED_tests.py',
    'RED_causal.log','RED_causal.exit','RED_causal_tests.py','GREEN.log','GREEN.exit','GREEN_supervisor.py','GREEN_tests.py',
    'supervisor.diff','tests.diff','final.diff','build_receipt.cjs'].map(p=>[p,sha(r(p))])),
  limitations:['All new process construction and group/PID signalling are faked; suite retains existing short subprocess fixtures.',
    'No long-lived NEW1 worker, model, MPS run, real PID reuse, or launch-readiness claim.',
    'Host verification and binding Astra review remain OPEN.'],
  tooling:{graft_successful_calls:2,reported_tokens_saved:85797,reported_dollars:'$0.04 plus <$0.01',
    note:'A graft callers query reported automatic graph refresh (7 changed inputs); direct source edits were restricted to the two authorized files.'}
};
const tick=String.fromCharCode(96), code=s=>tick+s+tick, fence=s=>tick.repeat(3)+s;
const sref=needle=>'tools/new1_supervisor.py:'+line(source,needle);
const tref=name=>'tests/test_new1_supervisor.py:'+line(tests,'def '+name+'(');
const logref=(text,needle)=>'RED_causal.log:'+line(text,needle);
const pidAssertion=red.split('\n').find(s=>s.startsWith('AssertionError: [call(123,'));
const heartbeatAssertions=red.split('\n').filter(s=>s.startsWith('AssertionError: None is not'));
const terminateAssertion=red.split('\n').find(s=>s.startsWith("AssertionError: OSError('fixture wait failed') is not KeyboardInterrupt"));
assert(pidAssertion && heartbeatAssertions.length===2 && terminateAssertion);
const report=[
  '# MB29 — NEW1 supervisor reap R3',
  '',
  'BUILD DONE: 97/97 tests GREEN; all 94 existing test methods and helpers remain byte-identical. Fixture evidence only. MAESTRO25 host verification and binding GPT-6-Astra review remain OPEN.',
  '',
  'The two supplied SHA-256 pins matched before the first edit; worktree and branch were verified. Read Astra r11 in full and the required R2 precedence table, source ranges, installed CPython poll, and fake patterns.',
  '',
  '## R11 blocker 1 — ownership across interrupted reaping',
  '',
  'Choice: defer SIGINT and SIGALRM around the supervisor’s own worker poll/wait operations. '+code(sref('def worker_reaping()'))+' masks both signals, restores the exact prior mask on every exit, and applies the existing exception selector if pending delivery raises while restoring it. '+code(sref('def poll_worker('))+' contains the sole raw poll; its callers are heartbeat '+code(sref('and poll_worker(process) is None'))+', loop top '+code(sref('if poll_worker(process) is not None and not worker_exited'))+', and loop EOF '+code(sref('if poll_worker(process) is not None and eof'))+'. The raw waits are guarded at '+code(sref('with worker_reaping(): process.wait(timeout=REAP_TIMEOUT_S)'))+' and '+code(sref('process.wait(timeout=timeout)'))+'.',
  '',
  'Why: installed CPython subprocess.py:1990 reaps with waitpid before :1992 stores returncode. Keeping that interval uninterruptible makes returncode a current ownership fact before cleanup can use PID fallback. Group cleanup remains unconditional. '+code(sref('def kill_worker(process)'))+' retains the protected ownership-check/PID-signal interval using the same guard.',
  '',
  'Deferral bound: every masked body is a nonblocking worker poll, a nonblocking ownership check/PID signal, or wait(timeout <= REAP_TIMEOUT_S = 5). No selector, resource probe, persistence, admission, constructor IO, complete retry loop, or arbitrary worker execution is masked. A wait keeps its existing finite timeout; emergency retries share the existing absolute five-second deadline. The successful reap flag is set inside the guard before pending delivery, and '+code(sref('if worker_reaped: break'))+' prevents a second wait after that success. The original 2,700-second deadline and 300-second cell deadline continue to be checked after delivery; no deadline is reset or extended.',
  '',
  'Regression: '+code(additions.find(n=>n.includes('interrupted_poll')))+' at '+code(tref(additions.find(n=>n.includes('interrupted_poll'))))+'. It uses the installed Popen._internal_poll with fake successful waitpid and a trace-triggered real SIGINT on the first line after waitpid returns. At injection, returncode is still None. It covers all three poll call sites, denies group signalling, intercepts all PID signals, retains the same original KeyboardInterrupt, and asserts one wait(timeout=5) and no PID fallback. It never sets returncode before injecting the interrupt.',
  '',
  'Causal RED on the pinned e61d4802 source, all three subcases ('+code(logref(red,pidAssertion))+', also RED_causal.log:152 and :160):',
  '',
  fence('text'),pidAssertion,fence(''),
  '',
  '## R11 blocker 2 — new heartbeat cleanup control exception',
  '',
  'At '+code(sref('chosen=preferred_exception(error,signal_error)'))+', heartbeat cleanup now selects the governing exception before noting an error. A new KeyboardInterrupt/SystemExit overrides an ordinary Stop and propagates into lifetime cleanup; an original control exception remains the same object and exit value. It therefore survives the bounded reap rather than becoming a note on STOPPED-RESOURCE.',
  '',
  'Regression: '+code(additions.find(n=>n.includes('heartbeat_cleanup')))+' at '+code(tref(additions.find(n=>n.includes('heartbeat_cleanup'))))+'. After worker creation, observe raises Stop(STOPPED-RESOURCE); group signalling fails; PID signalling raises the specified KeyboardInterrupt or SystemExit(23); lifetime cleanup succeeds. Both cases assert exactly one wait(timeout=5), then propagation of that same control object; SystemExit retains code 23.',
  '',
  'Causal RED ('+code(logref(red,heartbeatAssertions[0]))+' and '+code(logref(red,heartbeatAssertions[1]))+'):',
  '',
  fence('text'),...heartbeatAssertions,fence(''),
  '',
  'The cleanup-boundary audit also found that terminate’s bare finally wait could replace its first signal exception. '+code(sref('def terminate(process)'))+' now attempts the same bounded wait and uses the selector, retaining a secondary wait error as a note when it loses. '+code(additions.find(n=>n.includes('terminate_preserves')))+' at '+code(tref(additions.find(n=>n.includes('terminate_preserves'))))+' covers original KeyboardInterrupt, SystemExit(17), and ordinary PermissionError over an ordinary wait error; one bounded wait occurs in each case. Its causal RED is '+code(logref(red,terminateAssertion))+':',
  '',
  fence('text'),terminateAssertion,fence(''),
  '',
  '## Exception precedence and cleanup boundaries',
  '',
  '| Priority | Result |',
  '| --- | --- |',
  '| Original control | Original KeyboardInterrupt/SystemExit wins unchanged: same object and exit value. |',
  '| Cleanup control | Without an original control exception, the first cleanup control exception propagates after bounded reaping. |',
  '| Original ordinary | Otherwise, the original ordinary error beats secondary signalling/reap errors, including timeout. |',
  '| No original | The first cleanup error governs. |',
  '| Printing | Failure becomes an exception note and never chooses the governing exception. |',
  '',
  'The R2 precedence table is unchanged; R3 makes the heartbeat and terminate boundaries follow it. Audit of each boundary (static inspection plus applicable existing/new fixtures in GREEN):',
  '',
  '| Boundary | Final source line | Check |',
  '| --- | --- | --- |',
  ...boundaries.map(b=>'| '+b.name+' | '+code('tools/new1_supervisor.py:'+b.line)+' | '+b.check+' |'),
  '',
  '## R11 finding 6 — round-2 RED qualification',
  '',
  'The unchanged round-2 '+code('test_pid_fallback_ownership_check_cannot_be_interrupted_by_watchdog_poll')+' is now at '+code(tref('test_pid_fallback_ownership_check_cannot_be_interrupted_by_watchdog_poll'))+'. It passes on e61d4802 (RED_causal.log:62) because that source already guards the ownership-check/signal interval. Its old round-2 RED was a signature failure (object != 123 against the old numeric-PID helper), not causal evidence of interrupted reaping. It cannot be made causally RED on e61d4802 for the same already-fixed property without changing its target. R3 preserves it byte-for-byte and adds the separate installed-poll regression above.',
  '',
  '## Source identity',
  '',
  '| File | Start SHA-256 | Final SHA-256 |',
  '| --- | --- | --- |',
  ...Object.entries(evidence.source_identity).map(([p,h])=>'| '+code(p)+' | '+code(h.start_sha256)+' | '+code(h.final_sha256)+' |'),
  '',
  'The before/ copies match the start pins. RED_causal_tests.py equals GREEN_tests.py and the final test file. GREEN_supervisor.py equals the final source. Full artifact hashes and timestamps are in evidence.json.',
  '',
  '## Saved execution evidence',
  '',
  'Each log contains exactly one invocation of:',
  '',
  fence('sh'),command,fence(''),
  '',
  '| Log | Source | Count | Result | Exit |',
  '| --- | --- | --- | --- | --- |',
  '| RED_causal.log | e61d4802 | 97 | 8 causal subtest failures across 3 new methods; 0 errors; all 94 existing methods pass | 1 |',
  '| GREEN.log | Final source | 97 | 97 OK; 0 failures/errors | 0 |',
  '',
  'RED_causal.log:187–189 records the RED summary; GREEN.log:116–118 records GREEN. The log paths are '+code(evidence.red.log)+' and '+code(evidence.green.log)+'.',
  '',
  'RED.log and RED_tests.py preserve the earlier rejected fixture setup attempt: 97 tests, eight failures, zero errors, with two heartbeat failures caused by observe being injected during the pre-worker controller.check. That attempt is not blocker-2 RED evidence. Injection was moved into the post-creation selector heartbeat before changing the supervisor; RED_causal.log then records the required swallowed-control assertions.',
  '',
  'The audit verifies byte preservation of all 94 existing tests/helpers, the accepted source prefix (caps, Controller and constructor), prediction publication, and the full terminal/closeout/exit-mapping suffix. All worker poll/wait calls were inspected and are guarded. git diff --check passed. R11 findings 3–7, exit codes/outcome strings, terminal-commit authority, event names, 2,700 seconds total, 300 seconds cell wait, resource caps, halt-durability budget, and REAP_TIMEOUT_S = 5 are preserved.',
  '',
  'All new tests intercept process construction and group/PID signalling. The full required suite retains its existing short subprocess fixtures. No real long-running NEW1 worker, model/MPS work, PID reuse, commit, push, merge, unrelated deletion, or write to tools/test_dashboard_mathlab.py was performed. Existing integer-SystemExit closeout diagnostics remain in GREEN; the unchanged closeout code still preserves the original control object and exit value. Host/live execution and Astra approval are UNVERIFIED.',
  '',
  'Tooling note: the required graft query reported an automatic graph refresh of seven changed inputs. Direct edits are limited to the two authorized source/test files and this fresh receipt; graph results were used for navigation, not acceptance evidence.',
  '',
  '## Final diff against the pinned before files',
  '',
  'Machine-readable copies: supervisor.diff, tests.diff, and final.diff. The source half is against e61d4802fa6c9d4b6a8ecb1c4f612e0a1285a5e21bf104d5ea8f5e1c7e93d65a; the test half is against the supplied 4e8d70a1 pin.',
  '',
  fence('diff'),read(r('final.diff')).trimEnd(),fence(''),
  '',
  '## MAESTRO handoff',
  '',
  'Done: both r11 blockers fixed with causal RED and complete GREEN; all receipt artifacts saved. Half-applied work: none. In-flight commands: none. Exact paths/hashes: source identity table above and evidence.json. Failing final tests: none. The only RED failures are the saved pre-fix assertions and the separately identified rejected fixture attempt.',
  '',
  'Next: MAESTRO25 verifies the final two SHA-256 values and this receipt on the host with the exact test command above, submits the final source/tests plus evidence to binding GPT-6-Astra, and owns any commit. No launch is authorized by this fixture result.',
  '',
  'Binding context directive: watch Context N% left for this session and every orchestrated team session. Start a new piece of work only at 60% left or more. At 40% left or less, or immediately upon Context compacted, stop starting work, write a handoff at the end of README with done/half-applied/in-flight work, exact paths and SHA-256 values, failing tests and exact commands, next step and open risks, then reply exactly CONTEXT HANDOFF WRITTEN. Restate this directive in every successor handoff.',
  ''
].join('\n');
fs.writeFileSync(r('README.md'),report,{flag:'wx'});
evidence.artifacts['README.md']=sha(r('README.md'));
fs.writeFileSync(r('evidence.json'),JSON.stringify(evidence,null,2)+'\n',{flag:'wx'});
assert.equal(read(r('README.md')),report);
const persisted=JSON.parse(read(r('evidence.json')));
assert.equal(persisted.green.exit_code,0); assert.equal(persisted.green.tests,97);
console.log(JSON.stringify({receipt:evidence.receipt,baseline_methods:94,new_methods:additions,
  red:{tests:97,failures:8,errors:0},green:{tests:97,failures:0,errors:0},
  source_identity:evidence.source_identity,readme_sha256:sha(r('README.md')),
  evidence_sha256:sha(r('evidence.json')),receipt_bytes:fs.readdirSync(receipt,{withFileTypes:true})
    .filter(d=>d.isFile()).reduce((n,d)=>n+fs.statSync(r(d.name)).size,0)},null,2));

