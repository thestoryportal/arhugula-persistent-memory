**One C4 documentation requirement remains OPEN** at HEAD `a946812b6391af234a08d066f151a0d109ece392`, branch `worktree-c10k-route-a`.

| Condition | Status | Evidence |
|---|---|---|
| C1 | **CLOSED-AT-DISPATCH** | `tools/new1_dispatch.sh:5` disables background niceness adjustment; `:161–166` requires recorder niceness 0; `:258–263` records worker identity/niceness and requests SIGINT on mismatch. |
| C2 | **CLOSED** | `results/mathlab_staging/new1_launch_c4_20261011/new1_b2_one_invocation_authorization.md:7–18` explicitly authorizes one invocation, consumption despite subsequent admission refusal, no retry, and full-workload resource validation. |
| C3 | **CLOSED** | Capture and disposition: `tools/new1_dispatch.sh:223–304`. Deadline/resource accounting without a terminal event: `tools/new1_dispatch_report.py:19–40,70–113,168–178`. Committed `maestro_green_02/test.log:45–47` records **42 tests, OK**; `command.json:12` records niceness **0**. |
| C4 | **OPEN** | All **11 hashes verify**, and closeout exits **0**, token **`D-NEW1-b@8abea439`**. However, the specifically required append to the existing detailed record is absent; see below. |
| C5 | **CLOSED-AT-DISPATCH** | `tools/new1_dispatch.sh:169–188` checks disk, fingerprint and admission before consumption. `:178` prevents lowering the **21-GiB** floor. Supervisor admission repeats at `tools/new1_supervisor.py:513–519`. MAESTRO must maintain the coordinated quiet host and paused poll; the probes do not reserve the host. |

**C4’s remaining requirement:** the prior review explicitly required appending the correction/readiness disposition to the existing detailed record (`results/mathlab_staging/new1_launch_readiness_astra.md:106`). That [record still ends with the fixes and readiness review as future gates](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_real_dispatch_20261010T2031Z/README.md:22). Closeout now fingerprints the new manifest (`tools/closeout_fingerprints.json:186–188`), so its GREEN result does not establish that this earlier obligation was completed.

Append a short, committed superseding pointer to the manifest and accepted fixes, preserving the historical diagnostic and its cause limitation. Then recheck closeout at the resulting HEAD. This requires no numerical amendment or additional run authorization.

**Q9 command:** yes—the executed environment assignments, interpreter, arguments and prereg hash match exactly, provided the recorder starts in the prescribed worktree (`tools/new1_dispatch.sh:192–193,217–222`). Background capture and the SIGINT-handler restoration wrap that command.

**Consumption and niceness paths:**

- No handled pre-check refusal reaches `invocation.json`: refusal exits at `:106`, and the last hash check precedes its creation at `:194–209`. Failure after that boundary consumes authorization, including supervisor admission refusal.
- An observed initial worker niceness mismatch triggers SIGINT. Missing worker observation prevents accepting PASS and blocks subsequent compute (`tools/new1_dispatch_report.py:146–166`).
- This is **one-time niceness observation**, not continuous enforcement: after `worker_pid` is populated, `tools/new1_dispatch.sh:251` skips further niceness checks. A later external renice could therefore go undetected. That does not defeat the prescribed initial inheritance, but an unconditional “never undetected” claim would be false.

No additional blocker identified beyond the C4 append and the dispatch-time conditions. No supervisor, worker, `.venv` Python or test suite was run. Closeout’s memory-mirror warning was advisory.

🌱 graft reported approximately 45,942 tokens saved; one successful lookup.

VERDICT: GO-WITH-CONDITIONS
