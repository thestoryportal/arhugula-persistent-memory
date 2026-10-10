**Ready for one attempt only after the conditions below are satisfied.** No numerical or lifecycle blocker remains in the reviewed implementation; complete-workload feasibility remains unverified.

Live HEAD is **`b9cb229d422360fe94dcb84f58434f36848bdb15`**, superseding the packet’s `e27629d`. The scoped diff from `ec7561d` is empty, all eight supplied hashes match, and none of those files has working-tree changes. I ran only read-only checks and short system-Python checks—no supervisor, worker, `.venv` Python, or tests.

1. **Q1 — Parameter enforcement: not blocking, subject to the qualifications below.**

   | Parameter | Independently checked enforcement |
   |---|---|
   | 2,700-second budget | `tools/new1_supervisor.py:24` sets 2700; `:203` starts the monotonic clock; `:206–212` calculates remaining time. Controller creation at `:435` precedes admission at `:513`, prereg hashing through `:643`, and worker imports. The alarm is entered at `:508`. |
   | 11-GiB observed family RSS | `:27`, `:227`: stops on **`rss_gib > 11`**, not equality. `:154–161` sums the worker’s process group and recursively discovered descendants. This is sampled enforcement, not a hard allocation limit. |
   | Eight threads | Supervisor environment at `:523`; worker `torch.set_num_threads(8)` at `tools/new1_geometry.py:507`. |
   | Nice 10 | `tools/new1_supervisor.py:640` requests an **increment of 10**. It does not establish absolute niceness 10; Q2 applies. |
   | Native SVD: 13 GiB available | Reserve 5 at `:29`, additive 8 at `:243`, gate **`available >= required`** at `:248`; requested before SVD at `tools/new1_geometry.py:156–157`. |
   | Float64 SVD/checks: 19 GiB | Reserves 11 at supervisor `:29`; requests at geometry `:162`, `:164`, and **`:539`**. |
   | Maximum cell wait: 300 seconds | Supervisor `:25`, `:244`; expiry raises STOPPED-RESOURCE at `:211`. `:212` takes the minimum with remaining run time; waits cannot extend the total budget. |
   | Abort floor: 6 GiB | `:28`, `:227`: stops on **`available < 6`**, not equality. |
   | Admission floor: 8 GiB | Initial admission checks `available >= 8` at `tools/mathlab_admit.py:32`; heavy cells require 8 plus their reserve at supervisor `:243`. |
   | Fresh namespace | Main’s timestamped directory and exclusive creation at `:638–639`; existing event-stream refusal at `:434`. See Q6’s scope qualification. |
   | One attempt/no retry | One `supervise()` call at `:646`, with no retry loop. **Single-use authorization is not code-enforced.** Moreover, `:185–190` counts only recorded resource/deadline `halted` events; deadlines without that event escape this counter. |

   These values match Amendment B at `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:218–224`. The table’s numeric claims are correct; **absolute niceness and complete retry accounting require operational enforcement**.

2. **Q2 — Niceness: blocking precondition C1.**

   **Yes: record the actual worker’s niceness as 10.** The supervisor must start at niceness 0 for its `nice -n 10` command to produce the prescribed value. The previous command does not independently establish that starting state (`results/mathlab_staging/new1_b_go_astra.md:21–28`; `tools/new1_supervisor.py:640`).

   **C1:** Before invocation, verify the launching process will give the supervisor niceness 0. Immediately after worker creation, record its PID, parent/group identity, and **niceness = 10** in the dispatch receipt. An unavailable or mismatching observation requires stopping the dispatch and returning to the operator.

   My `/bin/ps` probe was denied by this sandbox; current host niceness and process clearance are **UNVERIFIED**, not clear.

3. **Q3 — Memory: not blocking for one explicitly authorized validation attempt.**

   Recalculation from the saved event stream confirms:

   - Peak **8.537597656 GiB**, versus profile **8.056793213 GiB**: **+0.480804443 GiB / +5.9677%**.
   - Headroom to 11 GiB: **2.462402344 GiB**.
   - `1.25 × peak = 10.671997070 GiB`.
   - Adding the maximum extra gather first gives **8.989013672 GiB**; multiplying by 1.25 gives **11.236267090 GiB**.
   - L4’s additional gather is **0.354514122 GiB**; adding it to the last **5.718414307-GiB** sample gives **6.072928429 GiB**.

   Sources: `results/mathlab_staging/runs/new1_20261010T053945.884468Z/events.jsonl:251`, `:266`; `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:216`.

   The pessimistic sum does **not** demonstrate a likely breach: it combines allocations from different phases. Check-function locals expire on return, `Vh` is explicitly released at geometry `:187`, C at `:538`, and construction follows the 19-GiB gate at `:539`. The second gather is visible at `:202`. Conversely, the 6.07-GiB calculation is **not a projector-phase peak bound**.

   Captured L5–L8 counts are smaller (`architecture_profile/s_new1_b_halt_diagnostic.json:24–29`), but they do not bound allocator retention, backend workspace, or later phases. Bundle mmap residency and the unobserved update/control phases remain unresolved (`tools/new1_geometry.py:424–475`, `:527`). Keep all caps unchanged; do not present the 25% sensitivity as a mandatory measured safety margin or a completion guarantee.

4. **Q4 — Time: not blocking under C2 below.**

   Event timestamps independently give **77.222330 + 159.321278 + 14.474513 = 251.018121 seconds**. Five equivalents are **1,255.090605 seconds**, leaving **1,444.909395 seconds**. These are extrapolations, not five-layer measurements (`events.jsonl:16`, `:93`, `:249`, `:265` in the namespace above).

   The older **2,525.888606-second** projection already includes a 50% covariance margin and 600-second allowance, leaving **174.111394 seconds** (`results/mathlab_staging/new1_v2_build_evidence/mb4_20261010_brobust/resource_projection.json:14–19`).

   The fix adds one gather per layer, not another decomposition (`tools/new1_geometry.py:200–202`). **I infer** that its direct copy cost is small relative to the measured SVDs, but its full-worker timing and allocation effects are unmeasured. Deadline risk is acceptable for this bounded feasibility attempt; successful completion is not established.

5. **Q5 — Lifecycle/reap: not blocking; incomplete deadline recording requires C3.**

   | Halt | Current cleanup path |
   |---|---|
   | INVALID-WORKER | Exited-worker detection invokes `terminate()` at supervisor `:542–544`; it attempts signalling and `wait(timeout=5)` at `:341–352`. Missing completion/nonzero exit becomes INVALID-WORKER at `:579–581`. |
   | Resource stop during SVD | The parent heartbeat observes resources, kills the worker group, and propagates the stop at `:492–503`. Lifetime cleanup then waits independently of remaining run time at `:448–487`. |
   | Deadline | Alarm expiry raises STOPPED-DEADLINE at `:106–114`. The owner exits the run alarm before the separately bounded lifetime reap (`:507–508`, `:458–464`). Expired time can prevent the halt receipt/event at `:617`; stderr reporting follows at `:623`. |

   The reap is **attempted and bounded**, not guaranteed under every OS failure. An unsuccessful wait is explicitly reported as an unreaped PID (`:477–486`). That must not be described as successful cleanup.

   R13’s accepted exception-preservation evidence remains applicable to these unchanged bytes (`results/mathlab_staging/new1_supervisor_reap_astra_r13.md:4–16`). Its AST guard remains limited, not a universal ownership proof (`:18–21`).

   **No terminal event on deadline is acceptable for this sole attempt only with C3:** capture supervisor stdout, stderr, exit status, actual namespace, and post-exit worker/group disposition in an external dispatch receipt. Missing terminal publication means **incomplete/no prediction verdict**, even if geometry artifacts exist; `tools/mathlab_events.py:288–303` suppresses provisional NEW1 findings. Record any reap failure and block subsequent compute until resolved. The five-second emergency reap is teardown beyond the computation budget, not extra computation authorization.

6. **Q6 — Fresh namespace/no retry: blocking precondition C2.**

   The endorsed **main entry point** guarantees exclusive creation of its generated directory (`tools/new1_supervisor.py:638–639`). `supervise()` alone is weaker: `:434` rejects an existing event stream, not every possible nonempty directory. Do not invoke it directly or pre-create the generated directory.

   Procedural enforcement is sufficient for **one supervised invocation**; a new token subsystem is unnecessary for this scope.

   **C2:** Create fresh operator authorization naming exactly one invocation of the endorsed command, its source manifest, and the expected namespace pattern:

   `results/mathlab_staging/runs/new1_YYYYMMDDTHHMMSS.ffffffZ`

   Record the actual directory and PID after dispatch. Invocation consumes authorization **even if admission refuses**. No retry loop, second manual invocation, resume, or cap increase is authorized. The filename itself need not encode the invocation; its contents and dispatch linkage must be unambiguous. The previous authorization is consumed (`results/mathlab_staging/new1_b_run_authorization.md:5–9`).

7. **Q7 — Complete-workload validation: blocking addition to C2.**

   **Restate the former C2 explicitly.** The consumed attempt did not validate the whole workload; Amendment B still labels full-workload reserves, RSS, other-layer timing, and nice-10 completion UNVERIFIED (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:222`).

   Fresh authorization must expressly permit **this sole full five-layer attempt to serve as complete-workload resource validation**. Otherwise, the validate-before-execution prerequisite remains unsatisfied (`results/mathlab_staging/new1_b_go_astra.md:11`).

   STOPPED-RESOURCE or STOPPED-DEADLINE means **no completed geometry verdict and no queue change**, not prediction FAIL or a lab stop. It counts toward the same-step third-abort rule (`docs/MATHLAB_PREREG.md:284`).

   **C3 also requires explicit abort accounting:** count deadline/resource stops from the dispatch evidence even when `halted` is absent. The existing retry scanner cannot do that (`tools/new1_supervisor.py:185–190`). I verified five existing namespaces, each with one start and none with a recorded resource/deadline halt. Regardless of that count, this authorization permits no second invocation.

8. **Q8 — Correction/source identity: blocking precondition C4.**

   The launch record must pin the **full hashes**, not just commit labels:

   ```text
   tools/new1_supervisor.py
   3144949d9d9ed97739f4aa5e67250e5c72640796233a2b82963e3932a758a6af
   tools/new1_geometry.py
   ce43a26d24fb9cd0e2a2ff4d4ddd63bdd7de9ff4d2349b017f77914a31271f77
   docs/NEW1_ADAPTER_GEOMETRY_PREREG.md
   1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f
   ```

   **C4:** Save one authoritative launch manifest containing actual HEAD, the eight verified source/test/prereg hashes, fix commits `57420ab`/`ec7561d`, r9/r13 and this review, exact command, resource budget, and authorization reference. Reverify source hashes immediately before dispatch and preserve that receipt.

   Append the correction/readiness disposition to the existing D-NEW1-b detailed record, reference it from runbook §5, update the structured next-action state, propagate the fingerprint, and rerun closeout. Current records still describe the fixes as future work (`docs/program_state.json:11`; `EXPERIMENT_RUNBOOK.md:460`; `tools/closeout_fingerprints.json:186–188`).

   **Do not amend the numerical preregistration:** its pin stays unchanged. R8 explicitly requires recording the correction/new identity without a numerical amendment (`results/mathlab_staging/new1_construction_diag_astra_r8.md:57`). Preserve all historical HALTs and the historical-cause limitation. Current runtime receipts alone are insufficient: they record prereg/input hashes, not both executing source hashes (`tools/new1_supervisor.py:644`; `tools/new1_geometry.py:555–556`).

9. **Q9 — Other blockers and endorsed command.**

   - **Admission: blocking precondition C5.** Require fresh successful CPU admission and working process-family monitoring. Coordinate a quiet host, including no conflicting Python/GPU-summary poll. Do not bypass refusal or manufacture a coordinator-tail exception (`tools/mathlab_admit.py:29–73`; `tools/c10w_p2_gate.py:73–84`). Live clearance was unavailable in this sandbox.
   - **Existing closeout: not blocking for the old diagnostic record.** I ran `LLMDB_ROOT="$PWD" /usr/bin/python3 -B tools/closeout_check.py D-NEW1-b`: exit **0**, current token **`9113c350`**, all required trackers GREEN. It emitted an advisory memory-mirror warning. This does not replace C4’s closeout after recording the fixes.
   - **Disk: not blocking at the observed 80 GiB free.** Factor arrays plus both spectra total **167,142,400 bytes**, before NPZ headers, JSON, logs, and receipts (`tools/new1_geometry.py:402–411`, `:464–466`). Record a conservative **1-GiB projected-write allowance**, explicitly a planning allowance, and recheck **free space ≥21 GiB** immediately before dispatch.
   - **Fix evidence: not blocking.** Saved GREEN logs show **35 geometry tests** and **101 supervisor tests** (`results/mathlab_staging/new1_projector_fix_20261010T204522Z/GREEN.log:38`; `results/mathlab_staging/new1_supervisor_reap_r4_20261010T215503Z/GREEN_receipt.log:261`). I did not rerun them. The fresh engine fingerprint check also passed.

   **Endorsed command, only after C1–C5 and fresh operator approval, with the external dispatch capture required by C3:**

   ```sh
   cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a &&
   /usr/bin/env PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin \
     TMPDIR=/private/tmp LLMDB_ROOT="$PWD" \
     LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= \
     OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 \
     "$PWD/.venv/bin/python" -B "$PWD/tools/new1_supervisor.py" \
     --prereg-sha 1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f
   ```

Graft: one successful lookup; its savings tally was unavailable in the truncated output.

VERDICT: GO-WITH-CONDITIONS

