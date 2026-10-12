# NEW1 supervisor reap round 4 — MB31 receipts

Status: **DONE**. MAESTRO26 requested evidence only for WIP `ec7561de2e5c16b6b64f30e29d012d7b5738521a`. The current supervisor and tests stayed byte-identical throughout; they were never swapped in the worktree. All persisted MB31 outputs are here or in the isolated copy.

## Fresh run receipts

| Receipt | Tests run | Failures | Errors / skips | Exit | Result |
| --- | --- | --- | --- | --- | --- |
| RED_causal_final.log | 101 | 22 | 0 / 0 | 1 | FAILED (failures=22) |
| GREEN_receipt.log | 101 | 0 | 0 / 0 | 0 | OK |

RED has 22 failure records across four test methods: **12 requirement-3 control-loss subtests, nine additional requirement-1 precedence subtests, and one requirement-2 structural guard failure**. It does not mean 22 independent test methods failed or that only 79 methods passed. The before-test inventory contains 97 methods; the final inventory contains the same 97 plus four new methods. All 97 existing methods pass in both fresh runs. GREEN is 101/101 OK.

The full set of failing identities **matches RED_strengthened.log**, including subtest parameters: fresh=22, strengthened=22, only fresh=0, only strengthened=0. This comparison corroborates the old log; that log has no recorded execution provenance and is **not** this causal receipt. Earlier RED_final.log / RED_causal.log used intermediate test copies according to the dispatch context and are not final-test causal receipts.

## Recorded provenance and fixture confinement

Copy directory: `/private/tmp/new1_reap_r4_mb31.2udziU`. `capture_receipts.py` created it using `mktemp -d /private/tmp/new1_reap_r4_mb31.XXXXXX`, copied worktree `tools/` and `tests/` with `cp -R`, then overwrote **only the copy's** supervisor with `before/new1_supervisor.py`. Copied bytecode caches were removed inside the copy. The executable for both runs is the worktree's `.venv/bin/python`.

RED, cwd `/private/tmp/new1_reap_r4_mb31.2udziU`, executed once:

```sh
LLMDB_ROOT=/private/tmp/new1_reap_r4_mb31.2udziU PYTHONDONTWRITEBYTECODE=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B -m unittest -v tests.test_new1_supervisor
```

GREEN, cwd `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, executed once:

```sh
LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a PYTHONDONTWRITEBYTECODE=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B -m unittest -v tests.test_new1_supervisor
```

`tests/test_new1_supervisor.py:31` hardcodes `tempfile.TemporaryDirectory(dir='/private/tmp')`. To meet the write/deletion boundary without editing tests, both commands inherited the same recorded startup hook at `/private/tmp/new1_reap_r4_mb31.2udziU/receipt_support/sitecustomize.py`. It redirects stdlib `tempfile.mkdtemp` requests for `/private/tmp` into `/private/tmp/new1_reap_r4_mb31.2udziU/fixtures`; it leaves the supervisor, test bytes, assertions, releases, mocks, and signal behavior unchanged. The hook records requested/allocated roots in the copy. Each run allocated 101 fixture roots, all inside the copy, and the tests cleaned only those roots. This is an explicit fixture-location adjustment, not an undisclosed ordinary-environment run.

| Inherited variable | Value for both commands (except per-run log) |
| --- | --- |
| NEW1_RECEIPT_TMPLOG | /private/tmp/new1_reap_r4_mb31.2udziU/RED_causal_final_fixture_roots.jsonl / /private/tmp/new1_reap_r4_mb31.2udziU/GREEN_receipt_fixture_roots.jsonl |
| NEW1_RECEIPT_TMPROOT | /private/tmp/new1_reap_r4_mb31.2udziU/fixtures |
| PYTHONPATH | /private/tmp/new1_reap_r4_mb31.2udziU/receipt_support |
| PYTHONPYCACHEPREFIX | /private/tmp/new1_reap_r4_mb31.2udziU/empty_pycache |
| TMPDIR | /private/tmp/new1_reap_r4_mb31.2udziU/fixtures |

`PYTHONPYCACHEPREFIX` selected a fresh, nonexistent cache location; `-B` and `PYTHONDONTWRITEBYTECODE=1` kept it absent in both runs, so worktree stale `.pyc` files were neither read nor deleted. `evidence.json` recorded each command, cwd, inherited environment, supervisor/test hashes and start time **before** launch; it then recorded exit, completion time, output hash and post-run hashes. The capture script prevents duplicate RED or GREEN runs. Estimated additional writes were at most 8 MiB; recorded free space exceeded that plus 20 GiB on both volumes. No temporary copy was deleted.

## Release mechanism and why it covers r12

The committed fix chooses one `ResourceOwner` (`tools/new1_supervisor.py:376`) rather than separate cleanup handlers at individual resources. `context` (:380) stores the resource's exit callback before entering it; `acquire_many` (:385) registers both socket close callbacks. Every entry passes through `_release` (:391), which catches `BaseException`, selects the governing exception using `preferred_exception` (:268), and attaches the losing error as a note. `close` (:414) drains all remaining entries in LIFO order before raising a newly selected winner. `scope` (:421) passes the propagating exception into that drain, then re-raises it. Early `release(child)` (:534) uses the same callback/precedence path and retains a failed entry for final cleanup. Callback return values cannot suppress the governing exception.

`supervise` creates one owner (:441), registers worker lifetime before construction (:507), and uses that owner's scopes for the log files (:525), constructor handlers (:530), selector (:535), bounded reap (:462), and halt-durability timer (:616). Final root drain is :629. The installed timer exits before the worker lifetime's separate five-second reap. A worker handle is assigned at :529 before `Popen.__init__` at :532 can spawn and raise, preserving ownership of an eventual PID.

In old `before/new1_supervisor.py:466`, native stdout/stderr `with` exits could replace the control exception; the old selector `with` at :473 could do the same before old worker_lifetime captured the governing exception at :393. The current selector/log exits run through `_release`, so an OSError becomes a note on the original KeyboardInterrupt or SystemExit(17). The fresh final-test RED reproduces both reviewer r11 sequences with fake processes/signals and the installed CPython `_internal_poll`; it does not launch the real NEW1 geometry worker. Fixture worker subprocesses elsewhere in the suite are stdlib stubs created by the tests.

## Precedence table

Here “in flight” means the exception delivered to the owner at that cleanup boundary. “Ordinary” excludes KeyboardInterrupt and SystemExit. The existing control-promotion rule remains: a new control exception may replace an ordinary exception, while the first control exception always wins.

| In flight | Release error | Result |
| --- | --- | --- |
| None | None | Continue normally. |
| None | Ordinary exception | Propagate the release exception from the owner. |
| None | KeyboardInterrupt / SystemExit | Propagate that control exception. |
| Ordinary exception (including worker error / Stop) | None | Preserve the original exception. |
| Ordinary exception | Ordinary exception | Preserve original; add a release-failure note. |
| Ordinary exception | KeyboardInterrupt / SystemExit | Release control wins under the existing table; add prior-exception note. |
| KeyboardInterrupt / SystemExit | None | Preserve the same original control object and SystemExit code. |
| KeyboardInterrupt / SystemExit | Ordinary exception | Preserve original control; add release-failure note. |
| KeyboardInterrupt / SystemExit | KeyboardInterrupt / SystemExit | Preserve first control object/code; add release-failure note. |

These are owner-level results. A propagated ordinary exception reaching supervise's handler may still map to its existing outcome code; an unmasked root release error escapes the final drain. The precedence test also checks that latter case at `tests/test_new1_supervisor.py:1578`, so an ordinary root close error is not silently suppressed. SystemExit(17) identity/code are explicitly checked at :1520/:1523 and :1544/:1547. No deadline, outcome, event or resource-cap changes are made by this receipt task.

## Every acquisition site in supervise

All lines below refer to the current pinned `tools/new1_supervisor.py`. The nine explicit owner-routed acquisition calls extracted from its AST are also listed verbatim in evidence.json. Setup, scope markers, worker allocation, and reviewed helper I/O are included to make the boundary explicit; helper internals are not claimed to be recursively covered by this AST test.

| File:line | Resource / acquisition | Release / ownership |
| --- | --- | --- |
| tools/new1_supervisor.py:432 | Path(run_dir) | Path value only; no retained OS handle; before any worker. |
| tools/new1_supervisor.py:433 | Run directory creation | Persistent output namespace; no retained handle and no directory deletion. |
| tools/new1_supervisor.py:435 | Controller | Clock/monitor/path state (constructor at :200); no closable resource. |
| tools/new1_supervisor.py:441 | Single ResourceOwner | One LIFO entry list; scopes drain portions; final drain at :629. |
| tools/new1_supervisor.py:442 | socket.socketpair: parent and child endpoints | acquire_many registers both close callbacks (:385-389); child early release at :534; parent/root leftovers drain at :629. Failed early child release remains registered for final cleanup. |
| tools/new1_supervisor.py:507 | worker_lifetime context | Registered before worker allocation; ResourceOwner invokes __exit__; cleanup :448-487 kills/signals and waits for owned worker, with REAP_TIMEOUT_S=5. |
| tools/new1_supervisor.py:508 | Whole-run hard_deadline context | Owned __exit__ restores timer/handler (:99); LIFO removes alarm before worker_lifetime performs separately bounded reaping. |
| tools/new1_supervisor.py:526 | worker_stdout.log open('xb') | context stores the manager before __enter__; __exit__/close through _release when :525 scope drains. |
| tools/new1_supervisor.py:527 | worker_stderr.log open('xb') | Same owner path as stdout; LIFO closes stderr before stdout at the :525 scope boundary. |
| tools/new1_supervisor.py:529 | Preallocated subprocess.Popen handle | Assigned to process before __init__; the previously registered worker_lifetime owns its eventual PID, even if construction raises after spawning. |
| tools/new1_supervisor.py:531 | constructor_ownership signal-handler context | Owned __exit__ restores handlers and delivers deferred signals (:281-310); drained by the :530 owner scope. |
| tools/new1_supervisor.py:532 | Worker created by subprocess.Popen.__init__ (call continues at :533) | Previously registered worker_lifetime kills/signals and waits; Popen's internal constructor resources retain stdlib ownership. |
| tools/new1_supervisor.py:536 | selectors.DefaultSelector context / selector backend | Owned __exit__ calls close through _release; the :535 scope exits before log scopes, while retaining the governing exception. |
| tools/new1_supervisor.py:463 | worker_reaping signal-mask context inside worker_lifetime | Owned __exit__ restores the prior mask (:314-323); :462 scope drains after bounded wait, using the same release precedence. |
| tools/new1_supervisor.py:617 | Halt-durability hard_deadline context | Owned __exit__ restores timer/handler; :616 scope drains within the existing remaining budget. |
| tools/new1_supervisor.py:462, 506, 525, 530, 535, 616 | resources.scope() context values / stack markers | Borrow the same owner; scope records a marker and drains entries after it through close/_release (:421-428). No independent resource owner. |
| tools/new1_supervisor.py:570 | path.read_text() artifact read | Helper owns its temporary file internally; returns text, no retained handle in supervise. |
| tools/new1_supervisor.py:576 | Path.glob iterator consumed by list() | Directory iteration is consumed locally; returns a count, no retained lifetime resource. |
| tools/new1_supervisor.py:509, 514, 516, 517, 520, 573, 576, 586, 588, 589, 591, 593, 618, 621 | emit/receipt/publish_predictions/durable_json helper I/O | Helpers return data/receipt/publication values; transient file/directory handles remain internal to those reviewed helpers. These calls are allowlisted, not recursively audited by this guard. |
| tools/new1_supervisor.py:522, 538, 556, 567, 570, 589, 590 | Environment, buffer, parsed data, path and receipt/publication values | In-memory state/metadata; no independent close callback. The terminal publication is captured at :491 and verified at :602. |

Selector registration (:537) borrows the already owned parent socket; unregister (:551) removes the registration. Poll/kill/terminate helpers retain their existing internal signal-mask handling. Neither creates an additional retained resource in supervise.

## AST guard: inspection and limits

`tests/test_new1_supervisor.py:1589` parses the full source of supervise and walks it, including nested helpers. It prints `OWNERSHIP_AST` records for **every With/AsyncWith boundary, every Call, and each owner acquisition factory** (:1614). Every with must be `resources.scope()` (:1618); calls must be in the explicit reviewed allowlist (:1600). Unknown factories, direct opens and direct closes fail (:1623). It additionally requires exactly one worker-lifetime registration and preallocated handle inside that lifetime (:1626), exactly one constructor-ownership scope with the sole initializer inside it (:1639), exactly one correctly named owner (:1651), and root final drain (:1655).

The guard test at :1661 also checks six deliberately unmanaged mutations: arbitrary native with, arbitrary factory call, direct file open, direct parent close, duplicate owner, and initializer outside constructor ownership (:1669). GREEN therefore checks both acceptance of current ownership and rejection of those additions.

It would catch r12's selector/log-file exits because their native with boundaries are not owner scopes and their raw factory calls are not allowlisted. Fresh RED reports exactly those findings: stdout/stderr native with at old :466 and selector native with at old :473, plus direct opens and selector factory. The structural assertion identifies 24 findings (`RED_causal_final.log:460`; full list :467). This is an expected structural RED, not a claim that its assertion itself detects lost control. Logged old-source probes at :499 os.getpid and :513 expression.glob further agree with the recorded old source. The guard is a reviewed-call/structure guard, not a semantic proof of arbitrary helper internals or a guarantee that changing an allowlisted callee needs no review.

## Every fresh RED failure classified

All methods belong to `tests.test_new1_supervisor.SupervisorTests`. Subtest parameters are part of each identity. Requirement-3 rows inject **OSError at the selected close**; six cover interrupted poll / successful waitpid and six cover heartbeat cleanup. All twelve reach the control-identity assertion after fixture/reap/release assertions have passed, then show `caught=None` and returned `INVALID-WORKER`: the control was lost. All six SystemExit variants use expected code **17**. None passes on old source, and none fails because of an import, fixture, missing-name or unrelated error. Non-causal failures: **0**.

| Test name and subtest | Requirement / coverage | Assertion text from RED_causal_final.log | Classification |
| --- | --- | --- | --- |
| test_resource_release_precedence_and_unmasked_release_error (boundary='selector', release='OSError') | 1: ordinary Stop versus ordinary close error | RED_causal_final.log:283 — AssertionError: 'INVALID-WORKER' != 'STOPPED-RESOURCE' | Causal precedence failure |
| test_resource_release_precedence_and_unmasked_release_error (boundary='stdout', release='OSError') | 1: ordinary Stop versus ordinary close error | RED_causal_final.log:294 — AssertionError: 'INVALID-WORKER' != 'STOPPED-RESOURCE' | Causal precedence failure |
| test_resource_release_precedence_and_unmasked_release_error (boundary='stderr', release='OSError') | 1: ordinary Stop versus ordinary close error | RED_causal_final.log:305 — AssertionError: 'INVALID-WORKER' != 'STOPPED-RESOURCE' | Causal precedence failure |
| test_resource_release_precedence_and_unmasked_release_error (boundary='selector', original='KeyboardInterrupt', release='SystemExit') | 1: original control versus different release control | RED_causal_final.log:316 — AssertionError: SystemExit(23) is not KeyboardInterrupt() : release control replaced the original control exception | Causal precedence failure |
| test_resource_release_precedence_and_unmasked_release_error (boundary='selector', original='SystemExit', release='KeyboardInterrupt') | 1: original control versus different release control | RED_causal_final.log:324 — AssertionError: KeyboardInterrupt() is not SystemExit(17) : release control replaced the original control exception | Causal precedence failure |
| test_resource_release_precedence_and_unmasked_release_error (boundary='stdout', original='KeyboardInterrupt', release='SystemExit') | 1: original control versus different release control | RED_causal_final.log:332 — AssertionError: SystemExit(23) is not KeyboardInterrupt() : release control replaced the original control exception | Causal precedence failure |
| test_resource_release_precedence_and_unmasked_release_error (boundary='stdout', original='SystemExit', release='KeyboardInterrupt') | 1: original control versus different release control | RED_causal_final.log:340 — AssertionError: KeyboardInterrupt() is not SystemExit(17) : release control replaced the original control exception | Causal precedence failure |
| test_resource_release_precedence_and_unmasked_release_error (boundary='stderr', original='KeyboardInterrupt', release='SystemExit') | 1: original control versus different release control | RED_causal_final.log:348 — AssertionError: SystemExit(23) is not KeyboardInterrupt() : release control replaced the original control exception | Causal precedence failure |
| test_resource_release_precedence_and_unmasked_release_error (boundary='stderr', original='SystemExit', release='KeyboardInterrupt') | 1: original control versus different release control | RED_causal_final.log:356 — AssertionError: KeyboardInterrupt() is not SystemExit(17) : release control replaced the original control exception | Causal precedence failure |
| test_resource_release_preserves_control_after_interrupted_poll (boundary='selector', control='KeyboardInterrupt') | 3: r11 sequence 1: waitpid succeeds, SIGINT before returncode, group signal denied; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:364 — AssertionError: None is not KeyboardInterrupt() : selector release lost original control after waitpid; returned 'INVALID-WORKER' | Causal control loss |
| test_resource_release_preserves_control_after_interrupted_poll (boundary='selector', control='SystemExit') | 3: r11 sequence 1: waitpid succeeds, SIGINT before returncode, group signal denied; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:372 — AssertionError: None is not SystemExit(17) : selector release lost original control after waitpid; returned 'INVALID-WORKER' | Causal control loss |
| test_resource_release_preserves_control_after_interrupted_poll (boundary='stdout', control='KeyboardInterrupt') | 3: r11 sequence 1: waitpid succeeds, SIGINT before returncode, group signal denied; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:380 — AssertionError: None is not KeyboardInterrupt() : stdout release lost original control after waitpid; returned 'INVALID-WORKER' | Causal control loss |
| test_resource_release_preserves_control_after_interrupted_poll (boundary='stdout', control='SystemExit') | 3: r11 sequence 1: waitpid succeeds, SIGINT before returncode, group signal denied; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:388 — AssertionError: None is not SystemExit(17) : stdout release lost original control after waitpid; returned 'INVALID-WORKER' | Causal control loss |
| test_resource_release_preserves_control_after_interrupted_poll (boundary='stderr', control='KeyboardInterrupt') | 3: r11 sequence 1: waitpid succeeds, SIGINT before returncode, group signal denied; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:396 — AssertionError: None is not KeyboardInterrupt() : stderr release lost original control after waitpid; returned 'INVALID-WORKER' | Causal control loss |
| test_resource_release_preserves_control_after_interrupted_poll (boundary='stderr', control='SystemExit') | 3: r11 sequence 1: waitpid succeeds, SIGINT before returncode, group signal denied; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:404 — AssertionError: None is not SystemExit(17) : stderr release lost original control after waitpid; returned 'INVALID-WORKER' | Causal control loss |
| test_resource_release_preserves_control_from_heartbeat_cleanup (boundary='selector', control='KeyboardInterrupt') | 3: r11 sequence 2: STOPPED-RESOURCE heartbeat, group signal denied, PID signal raises control; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:412 — AssertionError: None is not KeyboardInterrupt() : selector release lost heartbeat cleanup control; returned 'INVALID-WORKER' | Causal control loss |
| test_resource_release_preserves_control_from_heartbeat_cleanup (boundary='selector', control='SystemExit') | 3: r11 sequence 2: STOPPED-RESOURCE heartbeat, group signal denied, PID signal raises control; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:420 — AssertionError: None is not SystemExit(17) : selector release lost heartbeat cleanup control; returned 'INVALID-WORKER' | Causal control loss |
| test_resource_release_preserves_control_from_heartbeat_cleanup (boundary='stdout', control='KeyboardInterrupt') | 3: r11 sequence 2: STOPPED-RESOURCE heartbeat, group signal denied, PID signal raises control; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:428 — AssertionError: None is not KeyboardInterrupt() : stdout release lost heartbeat cleanup control; returned 'INVALID-WORKER' | Causal control loss |
| test_resource_release_preserves_control_from_heartbeat_cleanup (boundary='stdout', control='SystemExit') | 3: r11 sequence 2: STOPPED-RESOURCE heartbeat, group signal denied, PID signal raises control; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:436 — AssertionError: None is not SystemExit(17) : stdout release lost heartbeat cleanup control; returned 'INVALID-WORKER' | Causal control loss |
| test_resource_release_preserves_control_from_heartbeat_cleanup (boundary='stderr', control='KeyboardInterrupt') | 3: r11 sequence 2: STOPPED-RESOURCE heartbeat, group signal denied, PID signal raises control; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:444 — AssertionError: None is not KeyboardInterrupt() : stderr release lost heartbeat cleanup control; returned 'INVALID-WORKER' | Causal control loss |
| test_resource_release_preserves_control_from_heartbeat_cleanup (boundary='stderr', control='SystemExit') | 3: r11 sequence 2: STOPPED-RESOURCE heartbeat, group signal denied, PID signal raises control; selected close raises OSError; preserve original control (SystemExit code 17) | RED_causal_final.log:452 — AssertionError: None is not SystemExit(17) : stderr release lost heartbeat cleanup control; returned 'INVALID-WORKER' | Causal control loss |
| test_supervise_resource_acquisitions_share_precedence_owner | 2: AST ownership guard: 24 unmanaged boundary/acquisition/ownership findings on old source | RED_causal_final.log:460 — AssertionError: Lists differ: [('unreviewed call/acquisition', 11, 'sock[1423 chars]in')] != [] | Expected structural RED; not a control-loss assertion |

For the three ordinary Stop rows, the diff assertion also prints `ordinary release replaced original Stop` at log :286/:297/:308. The structural guard prints its full unmanaged-site explanation through :493. Those are the additional causal requirement-1 failures and the intentional requirement-2 failure, respectively; they are not silently relabelled as requirement-3 control-loss tests.

## SHA-256 pins and every saved test copy

Receipt-relative paths below are relative to this directory; worktree and isolated paths are labelled. Before-source/test pins and current source/test pins were verified before either run. The isolated RED test and RED_strengthened_tests.py are byte-identical to the current final tests; the earlier intermediate copies differ.

| Kind | Path | SHA-256 |
| --- | --- | --- |
| before | before/new1_supervisor.py | 3bb767f01257d4fd8d38fb21e132f5c89bfd3fa31959805dccf2555549ccf32f |
| before | before/test_new1_supervisor.py | 01b1fd268dbd8ceab42f13d4244f1e5e92205cdcb88e24d2c4c0fe1f5666d927 |
| worktree after | tools/new1_supervisor.py | 3144949d9d9ed97739f4aa5e67250e5c72640796233a2b82963e3932a758a6af |
| worktree after | tests/test_new1_supervisor.py | eccabf81552a1ec416d494e6b609597f902ec014f3fb7041059fc61dc73a8616 |
| worktree after | tools/test_dashboard_mathlab.py | b46d9c852706e20e8dca40cca8f56793559f3441cf30f5b9e8257a0ea0dab02e |
| saved test copy | GREEN_first_tests.py | 16d0bf6cd5f7fbef6906a72feb8e28e4e077f913e934c190854889c028f90827 |
| saved test copy | RED_causal_tests.py | 16d0bf6cd5f7fbef6906a72feb8e28e4e077f913e934c190854889c028f90827 |
| saved test copy | RED_final_tests.py | e2da8bbe0f4ec1e576621ad48b5e928028aef3705c36fa267a8cffebbb9cf401 |
| saved test copy | RED_strengthened_tests.py | eccabf81552a1ec416d494e6b609597f902ec014f3fb7041059fc61dc73a8616 |
| saved test copy | RED_tests.py | 5cf1de3ae7e61861074a35b27ee31ea739dd71d8d0c970bd46070c1444a4ef68 |
| saved test copy | before/test_new1_supervisor.py | 01b1fd268dbd8ceab42f13d4244f1e5e92205cdcb88e24d2c4c0fe1f5666d927 |
| saved source copy | GREEN_first_supervisor.py | 3144949d9d9ed97739f4aa5e67250e5c72640796233a2b82963e3932a758a6af |
| isolated RED file | /private/tmp/new1_reap_r4_mb31.2udziU/tools/new1_supervisor.py | 3bb767f01257d4fd8d38fb21e132f5c89bfd3fa31959805dccf2555549ccf32f |
| isolated RED file | /private/tmp/new1_reap_r4_mb31.2udziU/tests/test_new1_supervisor.py | eccabf81552a1ec416d494e6b609597f902ec014f3fb7041059fc61dc73a8616 |
| fixture routing hook | /private/tmp/new1_reap_r4_mb31.2udziU/receipt_support/sitecustomize.py | 53f121768bcd468df2f4161b75e964be7201247d79ece214b66e5803563d45ad |

## Diffs and artifact hashes

The requested unified diffs are **supervisor.diff** and **tests.diff**. Both `diff -u` commands returned 1 (differences found), with nonempty stdout and no stderr. Exact commands and hashes are in evidence.json. This captures the committed WIP change relative to MB29's before copies; it is not a new source edit by MB31.

| Artifact | SHA-256 |
| --- | --- |
| GREEN.exit | 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa |
| GREEN.log | eb1dd846d1aae4e8715ee8af34367f53ac090626f083f97496028880f8fb40e4 |
| GREEN_final.exit | 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa |
| GREEN_final.log | e950bc9da20c61f379c4ba9b4df94d1ab2143e5591bb6aa29f00c8ddd4b01149 |
| GREEN_receipt.exit | 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa |
| GREEN_receipt.log | 264b6a1f8526581fda10d1fa6377437638c9837a148d98ebd03cc2fde44b4e6d |
| RED.exit | 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865 |
| RED.log | c22bf7e00c1ade15533a58de270e717c0f1430f86a1a0bf26d6d93844ce2e092 |
| RED_causal.exit | 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865 |
| RED_causal.log | 9c3beade9c656698a881275f77d004c55741d604bc81d3a7406ef7ce29d2c501 |
| RED_causal_final.exit | 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865 |
| RED_causal_final.log | ed2623f821551243817322555704be2b2fe1f154c3aeaf9b7ab6e0497353ebaf |
| RED_final.exit | 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865 |
| RED_final.log | cae662ad122a6e115a3df5856882814dcc17b485d5ab20ab5658a5ad986358be |
| RED_strengthened.exit | 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865 |
| RED_strengthened.log | b41c13b1bcf95c08e452f0ef32c280cc5df726a89b81b811b1986bde0fd100b9 |
| supervisor.diff | 6705c5362443ee96de6ec08f54cd483b5c2fea73f80ba19c51bbcf2d20111cba |
| tests.diff | 145c44ad766451f093c1cb5233937e848b7030b89d2ab438a347d8677775bc2e |

All captured receipt artifacts (including saved source/test copies and the two evidence helper scripts) are hashed in evidence.json. receipt_manifest.json separately hashes the final README.md and evidence.json without a self-referential hash. capture_receipts.py is the capture implementation; write_receipts.py derives this README/classification/diffs and never runs tests.

## Scope and completion record

MB31 made no edits to worktree tools/ or tests/, no real worker/model/GPU/MPS run, no commit/push/merge, and no process kill outside the processes created by the fixture suite. tools/test_dashboard_mathlab.py already had an unrelated uncommitted change on entry; its hash remains `b46d9c852706e20e8dca40cca8f56793559f3441cf30f5b9e8257a0ea0dab02e`. The final tools/tests hash comparison excludes only MB32's four authorized paths below; every other file's bytes match the entry snapshot. MB32's results/backup_gdrive_host_20261010/locked_release_*/ receipts are also outside MB31 scope.

| Expected concurrent MB32 path (ignored) |
| --- |
| tools/launchd/MemitGdriveBackup.applescript |
| tools/launchd/build_gdrive_applet.sh |
| tools/launchd/stage_gdrive_release.sh |
| tools/test_backup_gdrive_addendum.py |

EVIDENCE-SHOWS: final tests causally fail on the pinned old source and all 101 pass on the pinned WIP source, with recorded provenance and zero non-causal failures. Limits: fixture/static verification only; no scientific NEW1 execution or admission claim. The next owner is MAESTRO26 for receipt review and the existing promotion workflow; no further implementation is proposed or performed here. Session context is preserved in this README within the authorized write boundary.

CONTEXT DIRECTIVE (binding; survives any future handoff): watch “Context N% left” in the status line. Start a new piece of work only at 60% left or more. At 40% left or less, stop starting work and write a handoff at the end of this README with what is done, what is half-applied, exact paths and SHA-256 of changed files, failing tests with exact commands, and next step; reply exactly “CONTEXT HANDOFF WRITTEN”. On “Context compacted”, do that at once.
