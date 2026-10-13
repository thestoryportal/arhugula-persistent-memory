1. **Not blocking — the r12 blocker is fixed.**  
   I replayed both sequences through the current code using the installed CPython `_internal_poll`, real SIGINT delivery, fake processes/signalling, and in-memory file sinks.

   | Sequence | Close raises `OSError` at | Result for both `KeyboardInterrupt` and `SystemExit(17)` |
   |---|---|---|
   | Successful `waitpid` → SIGINT before `returncode` assignment → group signal denied | Selector, stdout, stderr separately | Same original exception; exit value 17 retained; one simulated PID reap, zero PID signals, exactly one `wait(timeout=5)` |
   | `STOPPED-RESOURCE` → group signal denied → PID signal raises control exception | Selector, stdout, stderr separately | Same control exception; exit value 17 retained; exactly one `wait(timeout=5)` |

   All **12 variants passed**. At [supervisor:391](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:391), each failed exit preserves the governing control exception and annotates it. Consequently, [worker_lifetime:449](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:449) receives that exception intact. The alarm exits before bounded reaping; [line 626](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:626) re-raises it.

2. **Not blocking — the acquisition table covers the retained resources and their release paths.**  
   In [tools/new1_supervisor.py:442](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:442), the socket pair enters the owner. The remaining acquisition sites are worker lifetime **:507**, run timer **:508**, stdout **:526**, stderr **:527**, preallocated worker/initialization **:529/:532**, constructor handlers **:531**, selector **:536**, emergency-reap mask **:463**, and halt timer **:617**. All appear in the README table.

   These retained lifetimes route through the same `_release` mechanism, including early child closure at **:534** and final drainage at **:629**. I found no omitted retained resource. Helper-internal transient IO and existing poll/kill/terminate mask handling remain outside this ownership abstraction, as the README explicitly states.

   With no governing exception, release errors propagate; the root-close regression passed. Preserving the first control exception over a different cleanup control exception is appropriate: cleanup must not change the established cancellation or exit status. The shared selector/log tests, existing reap tests, and surrounding handler logic preserve that rule.

3. **Not blocking — the AST guard is useful, with concrete semantic limits.**  
   [tests/test_new1_supervisor.py:1589](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_supervisor.py:1589) walks the entire function, including nested helpers. I verified rejection of a new native `with`, direct `open()`, selector factory, and socket factory; nested opens/selectors/sockets were also rejected.

   The explicit call allowlist is narrow enough to catch ordinary new acquisition calls. It is not binding or control-flow analysis: my mutations **`receipt = socket.socket; leaked = receipt()`** and **`if False: resources.close(...)`** were accepted. Changes inside allowlisted external helpers also escape inspection. These limits prevent claiming universal ownership proof; neither bypass exists in the reviewed implementation.

4. **Not blocking — all 22 RED failures are causal.**  
   The saved [RED log:278](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_supervisor_reap_r4_20261010T215503Z/RED_causal_final.log:278) contains **12 control-loss failures, three ordinary-error replacement failures, six different-control replacement failures, and one intended structural failure**. No signature or fixture errors appear.

   Independently replaying the four new methods produced **22 failures/zero errors on the pinned old source**, versus **zero failures/errors on the current source**. All 28 evidence-artifact hashes and 30 receipt-manifest entries matched. Saved full-suite receipts show **101 tests, 22 failures** and **101 tests, OK**. The new regressions spawn no worker; existing full-suite tests include short subprocess stubs. I did not rerun the full suite.

5. **Not blocking — previously accepted behavior remains intact.**  
   [supervisor:24](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:24), **:341**, **:597**, **:617**, and `main()` preserve constants, resource caps, `terminate()`, terminal-commit authority, remaining-budget halt durability, outcome vocabulary, and exit mapping. Module assignments and all nine `supervise` event calls are unchanged.

   Targeted replays also passed the four r10 control-precedence rows, constructor-ownership cases, and shared five-second retry bound. Across this review, **18 distinct targeted methods passed** on current code.

6. **Not blocking — no additional blocker to entering launch-readiness review was found.**  
   Source/tests match `ec7561d`. [Geometry:200](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_geometry.py:200) and its tests remain byte-identical to `57420ab`, preserving r9’s projector acceptance. This supports advancement to launch-readiness review; it does not establish full-worker feasibility or authorize launch. No files changed or workers launched during this review.

🌱 graft reported ~141,506 tokens saved (~$0.09), one successful call.

VERDICT: GO