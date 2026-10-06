**FIX-FIRST**

**Next: stop the fifth launch and remove access to the full reference-run JSON.** I demonstrated a readable history route under the deployed v5 profile.

1. **The reference exception contains coined-value findings.** [`results/c10l_covgeom/run1_armB_identity.json`](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10l_covgeom/run1_armB_identity.json:318) exposes baseline A7 **13/72** versus identity-projector A7 **8/72**, plus canonical **7/24 versus 4/24**. The packet’s “control-arm numbers only, no coined-value finding” claim is false.

2. **The full exception is unnecessary.** [`prepare.py:143`](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/prepare.py:143) checks only whether baseline A1/A2 totals each reach **68**. Perform that historical check outside the loop and expose only its validation result. I would accept that minimal exception; I do **not** accept this complete experiment record.

**Empirical verification:** profile-protected read returned all **107,254 bytes**, parsed both A7 results, and exited **0**. README, preregistration, and the previously exposed experiment bytecode were denied; sandbox `program.md` remained readable. [Saved probe evidence](/Users/robertrhu/.gstack/projects/thestoryportal-arhugula-persistent-memory/checkpoints/20261006-113635-autoresearch-fence-v5-review.md).

**Cheapest closure test:** require this exact JSON read to fail while setup, shell capture and GPU execution succeed. Actual agent consumption of the history and fifth-launch equivalence are **UNVERIFIABLE** here; reachability is demonstrated.

**Drift:** this supports C10 candidate generation toward F1, but violates the separate no-history criterion in [`docs/AUTORESEARCH.md`](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/AUTORESEARCH.md). I did not signal the running process.

