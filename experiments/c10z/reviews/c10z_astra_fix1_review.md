VERDICT: PROCEED-WITH-FIXES

(Opus delta review of ASTRA (C10Z) fix round 1, 2026-10-07. The reviewer delivered this as its hand-back; the lead saved it here verbatim and verified the relative-OUT_DIR bug at c10z_astra_arms.py:1471/:1519 by reading the source. Scratch evidence: /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_mut_r2/rev_opus_b/.)

## C10Z ASTRA fix round 1, delta review: PROCEED-WITH-FIXES (one small code bug, one behaviour change you need to rule on, and several untested diagnostic paths)

The fixes work. Nothing I found produces a wrong scientific verdict. One small bug needs a one-line fix before a direct-python launch, and one behaviour change needs your ruling.

**Code under review:** the current worktree. I compared byte-for-byte at the end, and `c10z_astra_arms.py`, `c10z_astra_read.py`, `c10z_astra_selftest.py` and `tools/run_c10z_stage.sh` all match the copies I tested.

**Scratch-dir collision:** another agent was writing into `.../tmp/c10z_mut_r2/` during this review. It rewrote `mutate_r2.py` and overwrote `run_r2.log`, so ignore those files. All my results are isolated in `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_mut_r2/rev_opus_b/`.

### Evidence
- **Selftest:** 72/72 pass on the current code. The baseline mutation run passed both times.
- **Do the new tests catch the bugs?** I ran the current selftest against the pre-fix code (HEAD; the copies hash-match HEAD). It fails 64 times with 1 error, spread across all the fix tests (B1, B2, B3, go record, halt sidecar, refusal preservation, relative OUT_DIR, launcher, watchdog). Log: `selftest_current_on_pristine.log` (in the parent `c10z_mut_r2/` directory).
- **Mutation testing:** 110 of 122 mutants killed. No target errors, and every target matched exactly once.
  - The 71 old mutants: 70 killed (round 1 left 28 alive). The one survivor is A32.
  - The 51 new mutants on the fix paths: 40 killed. Every launcher (S01–S03) and go-gate mutant is killed except G11 and G21.
  - Files: `rev_opus_b/run.log`, per-mutant logs in `rev_opus_b/logs/`, harness `rev_opus_b/mutate.py`.
- **Demos** (`rev_opus_b/demos.py`, output in `demo_current.log` and `demo_pristine.log`):
  - **Halt in stage 2 after a finished stage-1 pass:**
    - *Now:* `pass_p1.json` stays byte-identical. A `halt_p1.json` is written carrying the full session (recipes, checks, memory, restores, budget history). The reader returns HALTED-V5 and keeps the stage-1 record.
    - *Pre-fix:* `pass_p1` was overwritten, no halt file was written, and the observations were lost.
  - **Real launcher, end to end:** with no go record, and again with a malformed one, it refuses with rc=2 and creates no directories.

### Bug: a relative `C10Z_OUT_DIR` reaches the resident unresolved
- In `c10z_astra_arms.py`, the parent resolves the out dir against its own working directory (`main`, :1519).
- It then starts the resident from the repo root but copies the raw environment variable (:1471–1474). So the resident resolves the same relative path against the repo root, not the operator's directory.
- Demo output: the parent resolved `<tmp>/rel/attempt`, while the resident got `C10Z_OUT_DIR=rel/attempt` with its working directory at the repo root.
- **Likely effect (not run):** the resident writes `run.json` somewhere the parent isn't watching. The parent's startup loop (:1475–1476) has no deadline, so it waits for as long as the resident stays alive, which could be the whole time the model is loaded.
- **Reach:** only a direct `python c10z_astra_arms.py` launch. `run_c10z_stage.sh` already makes the path absolute (:10), so the normal launch path is safe.
- **Fix:** pass `C10Z_OUT_DIR=str(out)` in `worker_env`, and add a test that checks the child's environment. The existing test `test_fix1_relative_outdir_resolved_at_main_parse` (selftest :1481) only checks what the parent passes to `stage_call`. Mutant O02 (removing the resolve inside `stage_call`) survives because of this: it's equivalent when called through `main`.

### Behaviour change for you to rule on: the parent no longer closes the attempt when the resident's heartbeat expires
- **Demo:** the parent requests stage 1 and then finds the heartbeat stale.
  - It returns rc=2 with "HALTED-V12: resident heartbeat expired".
  - It leaves `run.json` with `closed=False` and no halt, and writes no diagnostic file.
  - The reader reports "attempt still running; no final verdict".
- If the resident was only stalled and not dead, its terminal check sees no halt, so it carries on. When it finishes, the reader accepts a PARTIAL scientific verdict, even though the operator was already told HALTED-V12.
- Pre-fix, the parent wrote the halt into `run.json`, the resident saw it and stopped, and the architecture_profile diagnostic was written.
- **Likely cause:** the "refusals must not touch a finished attempt" fix also covers heartbeat expiry, which is detecting a failed resident rather than refusing a request.
- **My recommendation:** treat heartbeat expiry as a halt, not a refusal. That means writing `run.json` closed with the halt and producing the diagnostic, while still leaving any `pass_p*.json` alone.

### The 12 surviving mutants
**Equivalent (no fix needed):**
- **G21:** creating the directory before the fresh-directory check. That check only fails when the directory already exists.
- **B3c:** classifying the record without the ceilings. Only the omissions use that decision, and they come out the same.
- **H12:** the diagnostic not closing `run.json`. Both callers publish `closed=True` with the halt straight afterwards (:1420–1421, :1456).
- **O02:** equivalent through `main` (see the bug above).

**Caught later by the reader, but untested on the harness side:**
- **A32:** dropping the Z0 sigma halt at :876. Also survived in round 1. The reader enforces `sigma_shape <= .125` (`read.py:196`), so the attempt still fails safe.
- **B3d:** building the omissions without the decision. The reader recomputes them (`read.py:609`) and would mismatch, so a legitimate ABSENT-CEILING ending becomes a spurious HALTED-V12. No test runs `Session.record` with a missing next-stage ceiling.

**Real test gaps (the code is right; the tests don't check it):**
- **G11:** the go record isn't checked for NaN/Infinity, and `json.loads` accepts them.
- **H07:** a halt in process 2 drops process 1's observations. The process-2 case doesn't check process-1 records survive.
- **H08:** the watchdog path writes no diagnostic.
- **H10:** the resident's halt file has the session fields stripped. Demo B shows the keys are present today, but no test checks them.
- **H11:** the `architecture_profile/c10z_astra_halt_diagnostic.json` write is never checked, though CLAUDE.md halt discipline requires that file.
- **B3g:** the qualifier filter in eligibility. A non-clean PARTIAL/LEAD with a missing ceiling would be labelled ABSENT-CEILING instead of K1. Both sides call the same function, so nothing catches it.

### Suggested fix round (all small)
1. Pass the absolute out dir to the resident, with a test on the child's environment.
2. Decide on the heartbeat-expiry close-out and add a test for it.
3. Add assertions that kill H07, H08, H10, H11, G11, B3d and B3g.

The rest of the round-1 blocking items (no go gate, refusals overwriting pass records, no terminal path without a stage-2 ceiling, untested runtime gates) are fixed, and the tests and mutants confirm it.
