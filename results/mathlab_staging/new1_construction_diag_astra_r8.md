**Accept this run as MEASURED and apply Branch 1.** The separate-gather fix is justified. This does **not** establish the original worker’s historical cause or authorize another real run.

Read-only review: no edits, tests, or numerical execution. I independently verified the result hash, all three input hashes, all 13 embedded source pins, historical harvest-source hash, and all 14 candidate hashes; the candidate manifest also verified at review end.

**Q1 — Acceptance holds; no material inconsistency found.**

The namespace contains exactly `result.json` and `receipt.jsonl`, totaling **20,594 bytes**. Dispatch exited **0**. The final receipt is `terminal`/`MEASURED`, binding the independently recomputed SHA **`7e03238c…7d7a7`**, with no subsequent halt. See [dispatch stdout:1–4](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_real_dispatch_20261010T2031Z/dispatch_stdout.txt:1) and [receipt:1–6](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag/construction_20261010T203101.002212Z/receipt.jsonl:1).

The result records **91.4508 s**, sampled peak family RSS **4.21944 GiB**, eight threads, CPU fp32, and worker nice 10; the receipt records parent nice 10. Native U/s/mask/indices metadata agree before and after. The receipt spans approximately **91.459 s**, consistent with result timing plus completion work. See [result:20–134,520–545](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag/construction_20261010T203101.002212Z/result.json:520).

The two small RSS samples printed in the receipt do not contradict the higher reported peak: heartbeat samples update `peak` without appending every sample. Cleanup precedes result publication, and terminal writing flushes/fsyncs before successful return ([identity supervisor:549–621](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_identity_diag.py:549), `:209–219`).

`MEASURED` is valid diagnostic status, with no geometry or scientific PASS implied.

**Q2 — Branch 1 applies, with the historical-cause limitation retained.**

| Constructions | Projector SHA | Four probe relative errors | Unchanged gate |
|---|---|---|---|
| `list_shared`, `long_shared` | `0fff6d76…` | 2.95875e-6–3.18767e-6 | Reject |
| `list_separate`, `long_separate` | `0281d02c…`, exactly capture | All zero | Accept |

All four report allowed/excluded counts **8645/2363**. Corresponding operand bytes and strides agree; storage sharing and gather count differ. Index representation has no measured effect. These are internally consistent observations ([four construction records:144–497](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag/construction_20261010T203101.002212Z/result.json:144)).

That satisfies the predeclared separation rule exactly ([scope:48–58](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_scope.md:48)). SHA equality supplies stronger agreement than four sampled probes for the two successful constructions; neither observation establishes projector fidelity or behavior.

**Yes, the original worker could still differ.** Its float64 SVD/check interval and allocation history were omitted here ([geometry:150–197](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_geometry.py:150)). Its actual count, projector SHA, and individual residuals were not logged. The historical diagnostic’s count argument explicitly uses another measurement ([halt diagnostic:19–35](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/s_new1_b_halt_diagnostic.json:19)). Therefore retain: **construction discrepancy demonstrated here; historical HALT cause not conclusively established**.

**Q3 — The proposed construction change is the right single numerical fix.**

Change only the native capture-compared projector to **two independent gathers from the same native U and unchanged allowed indices**. Production currently gathers once ([geometry:200–202](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_geometry.py:200)); the producer gathers twice ([c10e_bandknob.py:173–175](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10e_bandknob.py:173)). Preserve normalization, decompositions, masks, execution order, thresholds, `projector_matches`, and engine bytes.

The failing-first test should directly exercise **production `native_projector`**:

- Use small nonempty synthetic native-fp32 U and fixed indices. Observe real indexing/matmul operands while delegating to real tensor operations.
- Require two gathers from that U with identical indices, independent operand storage, unchanged native values/dtype, and right-hand values equal to the left transpose.
- Current code must fail the independent-storage/two-gather assertion; corrected code must pass. Reverting to `Q@Q.T` must fail again.
- Compare the returned projector with an independently constructed two-gather reference and exercise the unchanged capture gate. Retain count-mismatch, SHA-success, probe-fallback, and failing-probe controls.

**Do not require finding a tiny matrix whose two constructions round differently.** That numerical discriminator can depend on size/backend. A frozen synthetic example is useful if available, but byte inequality alone does not reproduce a 1e-6 gate failure. Label the deterministic regression as construction-contract evidence; full-worker recovery remains unverified.

The acceptance contract remains:

**matching count AND (matching SHA OR all four probe relative errors ≤1e-6).**

Neither SHA-only nor probe-only acceptance should replace it ([geometry:230–240](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_geometry.py:230); [Amendment B:202](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:202)). Exact reference bytes are an appropriate fixture assertion, not a new universal launch gate.

There is no second offending site in the two named files: `new1_identity_diag.path_report` **already uses two gathers** at [line 105](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_identity_diag.py:105). Preserve the construction diagnostic’s shared controls.

**Q4 — Propose one fresh full Amendment-B attempt, after readiness review.**

The intended next real attempt is the **complete five-layer D-NEW1-b worker**, including its float64/check interval, adapters, controls, and unchanged gates. Branch 1 does not require an intervening exact-worker L4 diagnostic.

Retain **2,700 s total**, **11 GiB observed worker-family RSS**, one CPU worker/eight threads/final nice 10, fresh fail-closed admission, 13 GiB available for native SVD, 19 GiB for float64 SVD/checks, 300-second maximum cell wait inside the total budget, and the 6-GiB available-memory abort floor. Reassess projected output and extra-gather memory without increasing caps ([Amendment B:218–224](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:218)).

**A launch blocker remains:** the full worker uses `new1_supervisor.supervise`, whose exception path can skip `process.wait()` after signalling failure or deadline exhaustion ([supervisor:411–424](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:411)). R7 expressly left this open because the construction diagnostic used another supervisor. Its qualification cannot transfer to a full-worker launch. Resolve this through separately scoped lifecycle work and review; do not conceal it inside the numerical fix.

No numerical prereg amendment is required for source-faithful construction with unchanged estimands and gates. Record the correction and new source identity. **Astra launch-readiness review and fresh operator authorization are required**, covering the final implementation, enforcement, caps, fresh namespace, no retry, and whether this sole attempt again serves as complete-workload resource validation. The previous C1/C2 approval was for one consumed attempt ([authorization:5–9](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_b_run_authorization.md:5)).

**Q5 — Propagate the diagnostic now; preserve the unresolved worker status.**

No scientific condition blocks recording this accepted measurement and Branch-1 disposition. The full-worker launch blocker need not delay that update.

The proposed README currently documents execution acceptance, but not this outcome ruling ([README:14](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_real_dispatch_20261010T2031Z/README.md:14)). Append the reviewed interpretation, limitations, and next gates before using it as the fingerprint source. The existing fingerprint still points to host qualification and says real execution is UNRUN ([fingerprints:186–188](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/closeout_fingerprints.json:186)).

Close out **this diagnostic/status refinement**, retaining the original **INVALID-WORKER / predictions NOT COMPUTED**, pending fix/rerun, and unchanged F1 status. Refresh references and generated trackers; require `LLMDB_ROOT="$PWD" .venv/bin/python -B tools/closeout_check.py D-NEW1-b` to report ALL GREEN before declaring tracker closeout complete ([DISCIPLINE.md:48–50](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/DISCIPLINE.md:48)).

**Conditions:**

1. Preserve the accepted diagnostic and all historical HALTs; make no historical-cause or geometry-PASS claim.
2. Save failing-first construction evidence and passing regressions for the single numerical fix; leave acceptance thresholds unchanged.
3. Resolve and review full-worker lifecycle enforcement before launch.
4. Obtain Astra readiness review and fresh operator approval for one capped, fresh-namespace full attempt; no automatic retry.
5. Propagate the narrow result with current fingerprints and a GREEN closeout check.

🌱 graft reported ~34,625 tokens saved (~$0.02), one successful call.

VERDICT: BRANCH-1-FIX

