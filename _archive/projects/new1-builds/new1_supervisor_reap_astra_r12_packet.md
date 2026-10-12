# Astra NEW-1 r12: re-review of the supervisor reap fix, round 3

You are GPT-6-Astra, the cross-family reviewer for the LLM-as-Database program. This is a read-only review. Repo: this worktree, branch `worktree-c10k-route-a`, subject commit **6acb65b**.

## Subject
Your r11 verdict (`results/mathlab_staging/new1_supervisor_reap_astra_r11.md`, VERDICT: NO-GO) left two blockers in 61d31d4. Finding 1: PID ownership across an interrupt between `waitpid` and the `returncode` update. Finding 2: heartbeat cleanup at ~:414 turning a new control exception into a note. Finding 6 qualified the round-2 RED at :1342. Codex MB29 fixed these test-first and also audited every cleanup boundary.
- Source: `tools/new1_supervisor.py`, e61d4802… → 3bb767f0…. Review it with `git diff 61d31d4 6acb65b -- tools/new1_supervisor.py`. MB29 also changed `terminate()` (~:341) so that its first signal exception survives a secondary wait error.
- Tests: `tests/test_new1_supervisor.py`, 4e8d70a1… → 01b1fd26…, with 3 new tests (subtests included).
- Receipts: `results/mathlab_staging/new1_supervisor_reap_r3_20261010T213139Z/` (README.md with the approach, the boundary audit and the precedence table; RED_causal.log on e61d4802 with the final test file, 97 run, 8 failures; GREEN.log 97/97; diffs; evidence.json). MAESTRO25 checked the before/ pins, that RED_causal_tests.py equals the final test file, and that a host rerun is OK. MB29 reports that the round-2 test (now :1423) passes on e61d4802, so its round-2 RED was a signature failure, as you said.

## Questions
1. r11 finding 1: reproduce your r11 sequence (the installed `_internal_poll`, waitpid succeeds, SIGINT before `returncode` is set, group signalling fails). Can a single-PID signal now reach a released PID? Is any signal deferral bounded, documented, and free of wrapping anything that can block longer than the reap bound? Does it change how quickly the run alarm or a Ctrl-C takes effect in a way that matters?
2. r11 finding 2: reproduce your r11 sequence (`observe()` raises STOPPED-RESOURCE, group signalling fails, PID signalling raises KeyboardInterrupt, lifetime cleanup succeeds). Does KeyboardInterrupt now propagate after exactly one bounded reap? Is the precedence table true at every cleanup boundary MB29 lists, and is any boundary missing?
3. The `terminate()` change at ~:341: is it correct and in scope? Does it alter any outcome you accepted in r10/r11?
4. Are the RED failures causal (the targeted behavior, not a signature or fixture mismatch), with no real worker spawned?
5. Unchanged: exit codes and outcome strings, terminal-commit authority, event names, 2,700 s, 300 s cell wait, resource caps, the halt-durability budget, `REAP_TIMEOUT_S = 5`, and everything r11 findings 3-7 accepted.
6. Anything else that blocks this supervisor, together with r9's projector fix (57420ab), from entering the launch-readiness review?

## Output
Give numbered findings with file:line, each marked blocking or not blocking. End with exactly one line: `VERDICT: GO`, `VERDICT: GO-WITH-CONDITIONS` (list the conditions), or `VERDICT: NO-GO`.

A finding that does not replay both r11 sequences through the new code will not be accepted.
