# Astra NEW-1 r13: re-review of the supervisor reap fix, round 4

You are GPT-6-Astra, the cross-family reviewer for the LLM-as-Database program. This is a read-only review. Repo: this worktree, branch `worktree-c10k-route-a`. Subject commit **ec7561d** (code); receipts completed in **4a6efe8**.

## Subject
Your r12 verdict (`results/mathlab_staging/new1_supervisor_reap_astra_r12.md`, VERDICT: NO-GO) had one blocker in 6acb65b: the log files (old :466) and the selector (old :473) exit before `worker_lifetime` captures the governing exception, so a `close()` OSError raised while KeyboardInterrupt or SystemExit propagates replaces it and `supervise` returns INVALID-WORKER. This was the fourth round in which a cleanup boundary was missed, so round 4 was briefed to fix the class, not the instance: every resource `supervise` acquires after the worker can exist is released through one owner that enforces the precedence table, and an AST guard fails if `supervise` gains a boundary or acquisition that bypasses it.
- Source: `tools/new1_supervisor.py`, 3bb767f0… → 3144949d…. Review with `git diff 6acb65b ec7561d -- tools/new1_supervisor.py` (88 lines changed).
- Tests: `tests/test_new1_supervisor.py`, 01b1fd26… → eccabf81…, 101 tests (subtests included). The AST guard is at :1589 and :1661.
- Receipts: `results/mathlab_staging/new1_supervisor_reap_r4_20261010T215503Z/README.md` (mechanism; AST guard scope and limits; table of every acquisition site in `supervise`; precedence table; classification of every RED failure). `RED_causal_final.log`: the final tests run on 3bb767f0 in an isolated copy tree with recorded provenance, 101 run, 22 failures. `GREEN_receipt.log`: 101/101. `supervisor.diff`, `tests.diff`, `evidence.json`. MAESTRO26 reran both independently: RED 22 with the same failing set, GREEN 101 OK.

## Questions
1. r12 blocker: replay your r12 table through the new code: both r11 sequences, with selector close raising OSError, and the stdout and stderr close variants for KeyboardInterrupt and SystemExit(17). Is the original control exception preserved, the exit value 17 kept, and the PID reaped exactly once within the bound?
2. The class: is there truly one release mechanism? Check the README's acquisition-site table against the code: is any resource that `supervise` acquires after the worker can exist missing from the table or released outside the owner? With nothing in flight, does a release error still propagate (not suppressed)? When a release raises a *different* control exception while one is in flight, the original wins: is that the right rule, and does it hold at every site?
3. The AST guard: does it inspect what the README says it inspects? Would it fail on a new native `with`, a direct `open()`, a selector factory, or a new socket inside `supervise` or its nested helpers? Name any bypass it would miss, and say whether the call allowlist is narrow enough to mean something.
4. Are the 22 RED failures causal (control loss, ordinary-error replacement, or the intended structural failure), not signature or fixture mismatches, with no real worker spawned?
5. Unchanged: exit codes and outcome strings, terminal-commit authority, event names, 2,700 s, 300 s cell wait, resource caps, the halt-durability budget, `REAP_TIMEOUT_S = 5`, the `terminate()` change and everything r10–r12 accepted.
6. Anything else that blocks this supervisor, together with r9's projector fix (57420ab), from entering the launch-readiness review?

## Output
Give numbered findings with file:line, each marked blocking or not blocking. End with exactly one line: `VERDICT: GO`, `VERDICT: GO-WITH-CONDITIONS` (list the conditions), or `VERDICT: NO-GO`.

A finding on question 1 that does not replay your r12 sequences through the new code will not be accepted. A finding on question 2 must name the acquisition site by file:line.
