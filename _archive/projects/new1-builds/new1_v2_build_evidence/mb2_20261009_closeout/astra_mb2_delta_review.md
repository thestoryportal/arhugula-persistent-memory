# NEW1 MB2 closeout delta review — 2026-10-09

**FIX-FIRST for BUILD ONLY.** The three earlier findings are repaired in the inspected delta, but one success-path process-group cleanup race remains. No real geometry, model/GPU work, tests or numerical computation was run by this reviewer. Same-family GPT review has weaker independence; MAESTRO's Claude orchestration does not make this particular review out-of-family. This is not formal FREEZE or execution authorization.

## Remaining blocker: successful EOF can bypass group termination

At `tools/new1_supervisor.py:299–301`, the loop terminates the isolated group only when its first poll observes leader exit. A permitted schedule is: that poll observes the worker alive; the worker then closes IPC and exits; the bottom poll at `:336` observes exit with EOF. The valid-result branch breaks at `:339` without passing through group termination. The removed unconditional cleanup means successful publication at `:341–350` can follow without any group kill. A remaining same-group child that has closed its inherited control descriptor can therefore survive completion. The current IPC-holding-grandchild fixture (`tests/test_new1_supervisor.py:352–361`) exercises the top-poll path, not this EOF race.

**Minimal correction:** before the successful `break`, if `kill_sent` is false, terminate the isolated group and record `worker_exited=True` / `kill_sent=True`. Keep the existing flag so the already-cleaned path never repeats a stale group kill. Do not restore an unconditional final kill.

**Cheapest overturning fixture:** a deterministic stub/mocked poll schedule that returns alive at the first poll and exited at the final EOF poll, after a valid complete message. Assert exactly one group termination before prediction publication and preserve the successful result. Retain the real grandchild fixtures. No numerical work is needed.

## Prior findings resolved by source inspection

- **Freeze identity:** `tools/new1_supervisor.py:66–73` hashes the exact bytes it parses and checks the authoritative title/status, accepting a historical draft footer without weakening the whole-file pin. Both CLI admission (`:382–385`) and worker pre-import admission (`tools/new1_geometry.py:414–417`) call it. Positive/draft/hash-mismatch and worker-boundary fixtures are at `tests/test_new1_supervisor.py:121–168`.
- **Reparented group accounting:** `tools/new1_supervisor.py:131–154` now reads PGID, requires the worker's isolated group identity, and includes same-group members plus descendants. The synthetic reparenting fixture is at `tests/test_new1_supervisor.py:111–119`; real child shutdown fixtures are at `:323–361`. Early leader exit triggers cleanup at supervisor `:299–301`; the remaining alternate exit path is described above.
- **Bounded failure durability:** supervisor `:351–367` stops computation first, applies the original remaining deadline to reaping and halt persistence, preserves the original failure code, and explicitly reports incomplete closeout if persistence cannot finish. The blocked-halt fixture (`tests/test_new1_supervisor.py:363–378`) requires no fabricated halt/completion event. This preserves the strict spending-cap boundary in `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:113–115,128–131`.

The frozen 13-GiB SVD admission, 300-second per-cell wait, strict observed RSS/available-memory inequalities and shared event module remain represented by the supervisor's fixed reserves, `observe` and `wait_cell` (`tools/new1_supervisor.py:24–30,176–218`). No new algebraic or primary/secondary endpoint change was identified in this bounded delta.

## Evidence boundary and next step

Author-run receipt `mb2_red_supervisor.txt` ends with **32 tests, three failures/five errors**. Author-run `mb2_green_new1.txt` ends with **55 tests in 2.837 s, OK**. I read those receipts and the actual changed source/tests; I did not rerun them. They do not refute the unexercised bottom-poll exit schedule.

Next: add the one deterministic regression first, apply the conditional cleanup, and rerun the affected fixture suite. Parent still owns the isolated shared-suite verification, protected-source/artifact audit and dated build closeout. Real geometry and complete-workload resource feasibility remain **NOT RUN / UNVERIFIED**; no queue action or scientific claim follows from build acceptance.

**Context rule, binding through every handoff:** watch Context N% left; before approximately 20%, stop starting new work, write done / in-flight / exact paths / next step / risks into this review, and notify the parent so a fresh successor can continue. Every handoff restates this rule.

## Final bounded delta re-review — 2026-10-09

**PROCEED for BUILD ONLY.** This supersedes the FIX-FIRST verdict above; the historical finding and its evidence remain preserved. No remaining concrete blocker was identified in this bounded repair review.

The bottom EOF/exit path now calls `terminate(process)` before its successful break when `kill_sent` is false, and records both cleanup flags (`tools/new1_supervisor.py:336–341`). The previously cleaned top-poll path retains its flag (`:299–301`), so the repair does not restore unconditional duplicate group termination. Prediction publication follows the protected break (`:343`).

The deterministic fixture at `tests/test_new1_supervisor.py:380–397` supplies a valid hello/completion frame followed by EOF and the poll schedule `[None, None, None, 0]`: alive at the second iteration's top, exited at its bottom. It requires successful completion, exactly one `killpg(123, SIGKILL)` and exactly one direct-worker reap. The author-run `mb2_red_exit_race.txt` records the intended pre-fix failure: one test, expected one group kill but observed zero. The final `mb2_green_new1.txt` records **56 tests in 2.915 s, OK**. I inspected the source, fixture and receipts; I ran no tests or numerical work.

The earlier freeze-parser, PGID accounting and bounded failure-closeout repairs remain as assessed above. Parent-owned isolated shared-suite verification, artifact/protected-source audit and dated report closeout still determine final handoff completeness. This review neither runs nor authorizes real geometry, changes the frozen criteria, establishes full-workload feasibility, or admits a queue action. Same-family review retains weaker independence.

**Context rule, restated:** watch Context N% left; before approximately 20%, stop starting new work, record done / in-flight / exact paths / next step / risks in this review, and notify the parent for a fresh successor. Every handoff restates this rule.
