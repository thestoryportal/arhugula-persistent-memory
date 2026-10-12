**MAESTRO may bring this one real run to the operator now.** Qualification survives review; the proposed command matches FIX5. This is readiness for a separate go/no-go, not launch authorization.

Read-only review completed: no tests, launches, or edits. All **14 candidate hashes match at opening and closing**. All **13 embedded source/document pins** and the historical harvest-source hash also verify.

Below, `R` means `results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/`.

**1. Steps 3–5 — conform, with evidence boundaries**

| Step | Independently checked raw evidence | Ruling |
|---|---|---|
| 3 | 20 solo records/logs; 3 full records/logs, each containing all 205 methods in the retained order; 21 and 130 files respectively | PASS under r6’s quiet-host clearance |
| 4 | All five receipts; pre-exec and interpreter-entry masks/pending sets `[2,14]`; Python return 2 distinguished from native exit 2 | PASS |
| 5 | 100 solo records/logs; 10 full records/logs, each containing all 205 methods; 101 and 431 files respectively | PASS |

For all **133 batch invocations**, recorded log hashes recompute, printed summaries agree with their indexes, exits are zero, and no timeout, ResourceWarning diagnostic, ignored exception, or incomplete suite appears. All **1,862 recorded candidate-hash entries**—14 after each invocation—match the frozen manifest. The saved step-3 and step-5 checksum logs each contain 14 OK entries. Thus post-batch identity is independently supported by the final runner records, not merely the README.

The runner preserves fresh-process execution, suite order, explicit **205** count, warning enforcement, and first-failure stopping: `R/run_checks.py:15–24,39–66`. Raw anchors are `R/host_prequal_full_3/index.json:1`, `R/host_prequal_full_3/001.log:254`, and `R/host_full_10/index.json:1`.

I also checked the **546 auxiliary JSON receipts** across both full batches. FIX5 snapshots agree with their log records; acquired-child snapshots show matching reaping proof, collected guardians, absent workers/groups, closed channels, and empty streams. The direct `OwnedWorker` interruption fixtures without acquired children are not missing-reap failures; their fixture pipe is deliberately closed afterward (`tests/test_new1_identity_diag.py:484–523`).

There are **39 intentional native-exit-2 controls** across the 13 full runs. These are the retained missing-proof/terminal-failure tests, not unexpected suite exits; their expectations are explicit at `tests/test_new1_construction_diag.py:1257–1280`. No observed cleanup leakage disqualifies qualification.

Step 4’s parent interval is **0.000228083 s**, separately recorded from **0.012663667 s** startup. State is preserved; callbacks, ownership, and output lists are empty. `process.log` exactly matches `parent_return.json`. Empty `step4_stdout.log` is consistent: the outer launcher captures the child output into `process.log` (`R/fix5_inherited_mask_launch_01.py:45–62`).

Two limits remain explicit: these are **host receipts**, not evidence of sandbox execution; r6 expressly cleared the quiet-host sequence. Also, qualification does not identify the historical leaking instruction. FIX4 remains permanently **0/3**.

**2. Open supervisor issue — real, but not a blocker for this launch**

Construction main calls **`I.supervise`** at [tools/new1_construction_diag.py:240](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_construction_diag.py:240). It does not call `S.supervise`.

The skipped-wait vulnerability remains in [tools/new1_supervisor.py:411](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:411): signalling or deadline entry can fail before `process.wait()`. Importing `S` and using its helpers does not execute that branch.

The actual path uses `OwnedWorker`, guardian/worker reaping, and cleanup before terminal publication: `tools/new1_identity_diag.py:425–432,559–570,615–630`. This preserves r5/r6’s separation. The issue remains open for callers of `S.supervise`.

**3. Authorization — scientific scope unchanged; disclose the revised execution mechanism**

The 06:40Z authorization still describes the measurement exactly. The original construction helpers, measurement body, and command generator remain byte-identical; the four constructions, one native fp32 SVD, shared U/s/mask, unchanged `projector_matches`, independent counts/SHA/probes, and outcome rule survive. See [construction source:95](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_construction_diag.py:95), `:114–155,163–192`, and [scope:44](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_scope.md:44).

The operator should nevertheless see these execution differences from the original build:

- Authenticated release and an independent guardian now contain worker creation, cancellation, parent death, and cleanup.
- Launch has a **5-second sub-bound**. Cleanup/reporting reserves consume the original **600-second absolute budget**, rather than extending it.
- Missing ownership proof or exhausted terminal-reporting time can cause native fail-closed exit without a complete terminal receipt.
- FIX5 restores caller signal state and rejects blocked SIGALRM/SIGINT before protected file work.
- Identity, construction, test, and scope hashes changed.

These are documented safety corrections, not increased caps or expanded science: `tools/new1_identity_diag.py:244–265,295–354,450–461,541–543,630–659`; `new1_construction_diag_scope.md:525–567`.

No numerical-scope amendment is needed. **A fresh explicit go/no-go must identify FIX5 and these operational changes**, because r4/r5 reserve real-run approval separately. No retry, speculative repair, exact-worker execution, tolerance change, or adapter-energy work is included.

**4. Launch command — correct for these bytes**

Both supplied CLI hashes match. Construction’s embedded identity pin is already **`919b3a11…`**, not the historical pin retained in the scope’s original section. The additive FIX5 revision explicitly supersedes it: [construction source:24](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_construction_diag.py:24), `scope:567,577–582`.

Construction preflight uses its own `SOURCE_PINS`, inherited identity source pins, and three input pins; it does **not** invoke identity’s separate `verify_launch` or require the old identity scope hash (`construction:43–54`; `identity:26–43`). I found no stale FIX5 dependency pin. The derived command agrees with `launch_command` at `construction:203–212`; no correction is needed.

**5. Preconditions for the operator-approved attempt**

1. **Obtain explicit approval for exactly one FIX5 attempt**, with the unchanged outcome rule and no automatic retry. Preserve every prior failure and qualification receipt.
2. **Recheck the 14-file manifest immediately before dispatch.** Freeze these bytes through completion. Parent and worker must successfully verify all embedded source, historical-source, and real-input pins; real-input verification was not performed in this review.
3. **Require the worktree-bound engine fingerprint and fresh admission.** Run `LLMDB_ROOT="$PWD" .venv/bin/python -B tools/engine_fingerprint.py`; failure stops. The diagnostic also invokes fingerprint, process/tmux inventory, and memory checks through fresh `mathlab_admit.probe('cpu')` before ownership acquisition (`identity:222–224,578–583`; `mathlab_admit:29–73`). Maintain a quiet admission window: no competing non-exempt Python/model/test jobs or dashboard `--gpu-summary` poll, no pending competing compute launch, and working inventory tools. Denied or malformed observation is refusal.
4. **Maintain the resource/environment contract:** CPU, eight threads, final nice exactly 10, usable output streams, enforceable signal state, 600 seconds total, family RSS strictly below 11 GiB. Recheck disk at dispatch: projected output is **<1,000,000 bytes**, requiring that amount plus **20 GiB** free. This review observed approximately **80.3 GiB** available.
5. **Require a fresh output namespace and complete acceptance evidence.** Successful execution must leave only `result.json` and `receipt.jsonl`, combined below 1,000,000 bytes, with exit 0 and a durable final `terminal`/`MEASURED` receipt binding the result SHA. Preserve admission, resource, worker, provenance, and four-construction evidence. A result file alone is uncommitted; any late halt, missing terminal, or nonzero exit prevents acceptance. Preserve partial artifacts and stop—no retry (`scope:42`; `identity:197–219,615–647`).

Exact command, after those preconditions:

```sh
new1_nice_increment=$(LLMDB_ROOT="$PWD" .venv/bin/python -B -c 'import os,sys;current=os.getpriority(os.PRIO_PROCESS,0);sys.exit("starting niceness exceeds 10") if current>10 else None;print(10-current)') || exit "$?"
LLMDB_ROOT="$PWD" LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 /usr/bin/nice -n "$new1_nice_increment" .venv/bin/python -B tools/new1_construction_diag.py --scope-sha 19dda1126da0f2df2fa5418583cbcd1ba6a4be8411fcb52965b7396e369b9217 --source-sha 744f063374a766efbfffc5a1ede73be04a323210e6b4dad48e569e5a41545ec3
```

Full-size numerical behavior and live resource enforcement remain unverified until that authorized attempt. `MEASURED` would describe a valid diagnostic, not scientific PASS or F1 closure.

🌱 graft reported approximately 41,571 tokens saved; one successful call and one failed probe.

VERDICT: GO-OPERATOR

