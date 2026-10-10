# NEW1 FIX5 build receipt — Codex MB23

**NEW1 FIX5 BUILD DONE for authorized sandbox scope.** Exactly one full four-suite acceptance completed **205/205**, exit 0, 17.621 s reported by unittest (17.808941958 s process wall), with **no ResourceWarnings and no ignored exceptions**. All **188 existing methods remain**, plus **17 new methods** (8 criterion-1, 9 criterion-2). All 17 have individual behavioral RED and frozen-candidate GREEN. The final six actual-parent controls pass. Qualification repetitions and every launch remain UNRUN by MB23.

Receipt: `results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/`. Worktree/root verified at session start and final branch remains `worktree-c10k-route-a`. MAESTRO18 verifies on the host and commits; GPT-6-Astra supplies binding review. No commit, push, merge, real diagnostic, model load, GPU gate operation, external inherited-mask launch, 20-solo batch, 3/3 batch or 100+10 repetitions were performed. Other builders' files were neither protected-hashed nor edited. Temporary fixture lifetime cleanup is confined to scratch roots; no repository artifact was deleted.

## Start pins and protected scope

All pins verified before the first edit; see `start_pins.json` and byte copies in `before/`.

| File | Verified start SHA-256 |
| --- | --- |
| `tools/new1_construction_diag.py` | `b1db5aa9ab2d6914c3f4b3601f0164a9c78686c443ebdaa3445f9ea9d0d391a4` |
| `tools/new1_identity_diag.py` | `1161503c55346fb5d47bbed462ec3de3b17698b0b94752dfef4d7bf4d0e2ff8a` |
| `tests/test_new1_construction_diag.py` | `c80e08c5b36ffb9e5c83a2a47d9fdf28b223fb9e7e5d47a003893b681cbf69d4` |
| `tests/test_new1_identity_diag.py` | `7a9a6d3b74fe600cb4784c5711cde6fc6c373e11743ab7538d8afc86e155c6b1` |
| `results/mathlab_staging/new1_construction_diag_scope.md` | `77f3086cac50de8ba5896e5d7e4e4d5a3661ec43d136fa8c1a2cab53d1f8c607` |
| `tools/new1_supervisor.py` | `a69d410724b65a5dbacaf8e34fc45b73c9f545daf54eda9b6cfeb150e344557b` |
| `tests/test_new1_supervisor.py` | `33c61282862cea1d0297396cb860963bfc48adf33d054db3f933fed11d6d23ec` |

Both supervisor files matched git HEAD at start and end. They remain byte-identical; `tools/new1_supervisor.py:411–428` skipped wait remains a separate open ownership issue. No warning is waived on that basis. The historical FIX4 runner stays untouched.

## What changed and why

- `tools/new1_identity_diag.py:366,375,400`: OwnedWorker captures the caller mask with a nonmutating empty-set query, then enters restoration protection before blocking. Descriptor/PID bookkeeping, kernel reaping and FIX4 containment are unchanged.
- `tools/new1_identity_diag.py:503,519`: deadline entry protects mask restoration before mutation. Deadline exit clears its timer/phase and restores the retained mask even when the blocking call itself raises. No absolute deadline or cleanup reserve is increased.
- `tools/new1_identity_diag.py:450,459,680`: one shared `check_enforcement()` returns the original caller mask or raises named `INVALID-ENFORCEMENT` for blocked SIGALRM/SIGINT. Direct supervision checks before any protected work; identity parent main checks before its first timed file operation.
- `tools/new1_identity_diag.py:538,651,659`: handler installation is inside the supervisor's final restoration protection; final cleanup retains the independent entry mask and executes timer/handler restoration even if the final blocking mutation raises. Existing cancellation logic is unchanged.
- `tools/new1_construction_diag.py:234`: actual construction main invokes the shared check before hashing its source or creating its namespace. Its ordinary catch returns Python 2 without output/ownership. `:25` repins the identity source so the corrected launch contract is internally consistent.
- `tests/test_new1_identity_diag.py:164–167`: original identity deadline method now asserts mask, pending signals, timer and handler preservation immediately after production return, before teardown. `:335–550` adds test-only snapshot/isolation helpers, real-mutation schedules and 14 FIX5 methods.
- `tests/test_new1_construction_diag.py:279–280` updates only the existing literal source-pin expectation. `:1286` adds 3 parent-entry refusal methods. No existing method is removed. These are the only two changed existing method bodies; `inventory_preservation.json` records the retained inventory.
- Scope receives only `Scope revision — FIX5`; its previous bytes are an exact prefix. `scope_prefix.json` proves byte count, prior hash and final scope hash after an intervening operation.

`candidate_delta.diff` compares against the pinned start, not git HEAD, which already contains prior builders' uncommitted NEW1 work. `static_preservation.json` proves every existing science function is AST-identical, except named supervisor/parent entry functions. All native `_exit` calls, including the prior `I:614` and `I:631` fail-stops, remain unchanged. LAUNCH_S, CLEANUP_S, .2-s control budgets and .3-s requirements are unchanged. No retry is introduced in production.

## Behavioral RED to GREEN

Inventory was written before production edits in `fix5_inventory.json`: **205 = 69 construction + 41 identity + 34 geometry + 61 supervisor**. Original breakdown was 66/27/34/61 = 188. Counts are explicit, not inferred from successful output.

Each qualifying RED has exit 1, a completed method and an expected behavioral assertion failure, without ResourceWarning or ignored exception. Its source manifest proves both production scripts were unchanged. `red_validation.json` audits all 17. Each final GREEN has exit 0, one completed method, pristine output and source/test hashes matching `candidate_frozen.json`.

| Criterion / method | Qualifying RED log | Individual frozen GREEN log |
| --- | --- | --- |
| C2 `test_fix5_c2_construction_main_sigalrm_refuses_before_file_work` | `red_qualifying/001.log` | `green_frozen/001.log` |
| C2 `test_fix5_c2_construction_main_sigint_refuses_before_file_work` | `red_qualifying/002.log` | `green_frozen/002.log` |
| C2 `test_fix5_c2_construction_main_both_refuses_before_file_work` | `red_qualifying/003.log` | `green_frozen/003.log` |
| C1 `test_fix5_c1_deadline_entry_restores_unrelated_block` | `red_qualifying/004.log` | `green_frozen/004.log` |
| C1 `test_fix5_c1_deadline_exit_restores_unrelated_block` | `red_qualifying/005.log` | `green_frozen/005.log` |
| C1 `test_fix5_c1_deadline_exit_with_owned_child_reaps_before_cleanup` | `red_qualifying/006.log` | `green_frozen/006.log` |
| C1 `test_fix5_c1_handler_install_restores_substituted_handler` | `red_qualifying/007.log` | `green_frozen/007.log` |
| C1 `test_fix5_c1_handler_restore_restores_caller_mask` | `red_qualifying/008.log` | `green_frozen/008.log` |
| C1 `test_fix5_c1_owned_start_restores_mask_after_mutation` | `red_qualifying/009.log` | `green_frozen/009.log` |
| C1 `test_fix5_c1_owned_step_restores_mask_after_mutation` | `red_qualifying/010.log` | `green_frozen/010.log` |
| C1 `test_fix5_c1_owned_close_fd_restores_mask_after_mutation` | `red_qualifying/011.log` | `green_frozen/011.log` |
| C2 `test_fix5_c2_direct_sigalrm_refuses_without_consuming_pending` | `red_qualifying/012.log` | `green_frozen/012.log` |
| C2 `test_fix5_c2_direct_sigint_refuses_without_consuming_pending` | `red_qualifying/013.log` | `green_frozen/013.log` |
| C2 `test_fix5_c2_direct_both_refuses_without_consuming_pending` | `red_qualifying/014.log` | `green_frozen/014.log` |
| C2 `test_fix5_c2_identity_main_sigalrm_refuses_before_file_work` | `red_qualifying/015.log` | `green_frozen/015.log` |
| C2 `test_fix5_c2_identity_main_sigint_refuses_before_file_work` | `red_qualifying/016.log` | `green_frozen/016.log` |
| C2 `test_fix5_c2_identity_main_both_refuses_before_file_work` | `red_qualifying/017.log` | `green_frozen/017.log` |

C1 mask schedules call the real pthread_sigmask first and raise once before the old restoration protection. Saved injection records bind prior source lines **495** (entry), **510** (exit), **636** (final handler restoration), **367/375/400** (OwnedWorker close/start/step), and real handler substitution. Before-state blocks only unrelated SIGUSR1 `[30]`; unchanged production unwinds leaving `[2,14,30]` in mask-boundary REDs. Snapshot and ownership observation occur after production unwinds, before any fixture cleanup; no test resets the mask to pass. GREEN preserves `[30]`, original handlers, zero timer and pending state.

The initial active-phase exit injections reached real native exit 2 without a post-unwind snapshot (`red_all/005.log`, `006.log`). They are retained, but **not qualifying restoration REDs**. The second genuine schedule raises once at the production entry guard before phase assignment; real `__enter__` exceptional cleanup then executes `__exit__` at 510. One version starts with no owner; the other waits until a child is registered/released, then fails the next deadline entry. Both return Python 2 on unchanged production, exposing the stranded mask. The owned-child snapshot includes matching wait proof, collected guardian, absent worker and closed channels/empty streams. The final helper additionally probes group absence with real `os.killpg(pid, 0)`. `red_all` is not a discarded batch or a source of GREEN evidence. There were **2** genuine exit-boundary attempts, below the 3-attempt stop cap.

C2 intentionally imposes ALRM-only, INT-only and both at caller entry, and queues the corresponding pending signals. This is caller-refusal evidence, distinct from C1's production-mutation evidence. Unchanged source reaches a protected source/output operation, rather than named refusal. Corrected direct supervision raises `S.Stop(code='INVALID-ENFORCEMENT')`; both actual mains return Python 2 through ordinary catches. Snapshots assert mask, pending set, handlers and timer unchanged, no source verification/directory/output/callback/worker acquisition, and no stdout. No caller signal is unblocked or consumed. Rejection uses neither an alarm nor synchronous output persistence.

The full four-suite shared-process order is preserved. New intentional-fault/pending-signal methods use contained child fixtures to prevent their expected RED masks from poisoning unrelated tests; the 188 existing methods still execute in the same ordered suite process. Original deadline preservation is checked before teardown. No suite/module isolation, warning suppression or test deletion was used to obtain full acceptance.

`green_individual/` records the first implementation GREENs. `green_final/` records the stronger group-absence helper. `green_frozen/` binds all individual GREENs to the final source/test pins, including the updated existing literal pin and additive scope. None substitutes for the full shared suite result.

## Step-2 actual-parent controls

`parent_control.py` calls the actual construction main and corrected production supervision. It does not replace main/deadline/ownership algorithms. Worker command, preflight, admission, monitor and scratch root are injected at science/IO boundaries, with explicit I.DEADLINE_S=.2 and S.SAMPLE_S=.01 fixture constants. Real source hashing, namespace creation in unmasked controls, timers, raw-fork guardian, kernel reaping and channels remain production paths. Science, real input verification/admission, models and GPU gate are stubbed.

Python return is recorded immediately after D.main; native status below is the separately observed fresh control interpreter exit. All rows have a return marker and pre-cleanup observation. No native `_exit` is patched or converted into Python return.

| Control | Python return | Native interpreter exit | Parent seconds | Ownership before fixture cleanup |
| --- | --- | --- | --- | --- |
| `unmasked_blocked_preflight` | 2 | 0 | 0.102823541 | No ownership acquired; normal bounded STOPPED-DEADLINE terminal |
| `unmasked_blocked_monitor` | 2 | 0 | 0.111038917 | worker 52379 proof matches; guardian 52378 collected (code 0); worker/group absent; all channels closed; streams empty |
| `unmasked_resource_cleanup` | 2 | 0 | 0.005282416 | worker 52384 proof matches; guardian 52383 collected (code 0); worker/group absent; all channels closed; streams empty |
| `preblocked_blocked_preflight` | 2 | 0 | 0.000287583 | No owner/callback/source verification/directory/output; mask and pending `[2,14]` preserved |
| `preblocked_blocked_monitor` | 2 | 0 | 0.000301250 | No owner/callback/source verification/directory/output; mask and pending `[2,14]` preserved |
| `preblocked_resource_cleanup` | 2 | 0 | 0.000289125 | No owner/callback/source verification/directory/output; mask and pending `[2,14]` preserved |

All configured parent bounds are **.2 s**, and every measured fixture parent interval is **<.3 s**. Interpreter startup/process wall is separately recorded and has no .3-s qualification claim. Unmasked preflight/monitor errors are STOPPED-DEADLINE; unmasked resource/cleanup is STOPPED-RESOURCE. Preblocked variants reject INVALID-ENFORCEMENT before ownership acquisition. Full logs, hash-bound index, snapshots and return markers are in `step2_actual_parent_final/`.

The first six controls are retained in `step2_actual_parent/`; they passed but probed worker/group-leader absence via getpgid. The final six were run after changing the ownership observer to probe the actual process group with signal 0. This stronger observation motivated the final controls; no failed control was selectively restarted, and no investigation/qualification repetition cap was extended.

## Sandbox acceptance and external qualification commands

Executed exactly once, saved `acceptance_command.json`, `full_acceptance.log`, `acceptance_result.json`:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -W error::ResourceWarning -m unittest tests.test_new1_construction_diag tests.test_new1_identity_diag tests.test_new1_geometry tests.test_new1_supervisor
```

Result: **205 methods, OK, exit 0**, no ResourceWarnings, no ignored exceptions, no timeout; all frozen file hashes agree before/after. Log SHA-256: `4bbf486c67d776cd86241b2ff5bb595373545982fa61880c643fbff586004151`.

`run_checks.py` is the FIX5 copy. It keeps fresh-process execution, 120-second observer timeout, suite order, raw stdout/stderr capture, failure/ignored-exception/warning checks and stop-on-first-failure behavior. Its explicit expected full count is 205 at line 65, with module breakdown in `fix5_inventory.json`. Only target selection (frozen FIX5 inventory), new receipt environment/source hashes and expected count change; unused ast import is removed. `runner_delta.diff` records the exact difference; historical runner hash is preserved in `candidate_frozen.json`. A single test-mode probe uses the runner for each individual RED/GREEN; the full accepted command above uses the user's exact argv without the runner's historical verbose flag.

These commands are **written, not executed by MB23**. MAESTRO18 coordinates a quiet host with no competing test load. From the named worktree root, verify `candidate_sha256.txt` first. Advance only after the preceding batch is completely clean; on any failure stop and retain the fresh namespace. No selective restart or replacement batch is authorized here.

```sh
LLMDB_ROOT=$PWD shasum -a 256 -c results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/candidate_sha256.txt
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/run_checks.py solo --count 20 --label host_prequal_solo_20
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/run_checks.py full --count 3 --label host_prequal_full_3
```

After those prerequisites, r5 item 4 requires new explicit operator authorization for exactly one externally inherited-mask launch. The written launcher is **UNRUN**; the following flag is for that later authorized operator invocation and grants no permission in this build:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/fix5_inherited_mask_launch_01.py --operator-authorized fix5_inherited_mask_launch_01 --output results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/fix5_inherited_mask_launch_01
```

The external before-exec phase blocks `[2,14]` and queues both pending signals, then execs a fresh interpreter. The entered phase captures initial mask/pending state before importing the diagnostic, never sets that mask again, calls actual construction main with science stubbed, and records Python return 2 separately from native child exit 2. The outer observer requires return/ownership/state/timing markers, emits its own native status, and stops on failure without another attempt. Exec-startup seconds are distinct from the .2-s parent interval; no arbitrary whole-interpreter startup cap is claimed. Only static AST parsing was performed on this launcher.

Then retain the separate host bar:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/run_checks.py solo --count 100 --label host_solo_100
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/run_checks.py full --count 10 --label host_full_10
```

These repetitions are practical qualification thresholds, not proof of non-flakiness. Failed FIX4 remains permanently 0/3. Neither this one sandbox pass nor the written commands authorize real diagnostic execution.

## Changed/new file hashes

`candidate_frozen.json` binds all candidate source/test/runner/control/launcher hashes. The following table lists all five changed repository files and new executable/inventory artifacts. The generated **`SHA256SUMS`** contains every changed repository file and every new receipt file, including start copies, all failed/RED/GREEN logs/snapshots, control records, this report and diffs. Its own hash is emitted in final verification output, avoiding a self-referential checksum. All are recomputable from these paths.

| File | Final SHA-256 |
| --- | --- |
| `tools/new1_identity_diag.py` | `919b3a11a836973ea4c0d2abdd2514634ea62792e6009e828a63d81f297c3d0d` |
| `tools/new1_construction_diag.py` | `744f063374a766efbfffc5a1ede73be04a323210e6b4dad48e569e5a41545ec3` |
| `tests/test_new1_identity_diag.py` | `047e1425a30be7daa58194a5f94862b865dee5f09ff0060ed51d6902e5d0ca0e` |
| `tests/test_new1_construction_diag.py` | `995e81cde32c2defd0379ec5bd87d1f78638b462293a3179c479fd73e565a686` |
| `results/mathlab_staging/new1_construction_diag_scope.md` | `19dda1126da0f2df2fa5418583cbcd1ba6a4be8411fcb52965b7396e369b9217` |
| `tools/new1_supervisor.py` | `a69d410724b65a5dbacaf8e34fc45b73c9f545daf54eda9b6cfeb150e344557b` |
| `tests/test_new1_supervisor.py` | `33c61282862cea1d0297396cb860963bfc48adf33d054db3f933fed11d6d23ec` |
| `tools/new1_geometry.py` | `018ce4d97f817ecd816a4fd3fb47316e78fda7007984449e93f423d0eb1f4a5e` |
| `tests/test_new1_geometry.py` | `57afd2504c9ce065e85be5e5d4237122bea3e329324ff557775cea9e9faa260f` |
| `results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/fix5_inventory.json` | `f257c10b8eb86df14f1bdcb4eeb03d614323206a6fbe8694ae5cb16e65a680ea` |
| `results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/run_checks.py` | `e0157653709d4778f23db334544afe8038bb7ae555c96180cd5e167d78510d21` |
| `results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/parent_control.py` | `8e477e56428e79dc7d429e71ddd7497424fec97d10a7a60aa1e9bf439411adcb` |
| `results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/run_parent_controls.py` | `52a8cb74469cde86acf5c268a86766a84d886d067edb98e95a54a4469653f04d` |
| `results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/fix5_inherited_mask_launch_01.py` | `dd7ea183d5d99d395c6dbd1b0e307f2460120bfa29d42d6a9fc02211597c8ab1` |

## Limits and ready handoff

The saved schedules prove the specific mask/handler restoration vulnerabilities and early refusal of disabled enforcement. They **do not identify the historical leaking instruction**, observer contribution, native-thread effects, warned-PID attribution, or host load causation. `S.supervise` skipped wait remains separate and open. No CPU fixture is promoted to scientific evidence or F1 closure. Astra review, 20-solo, 3/3, external inherited-mask control, 100+10 host repetitions and real diagnostic remain **UNRUN / not earned by this build**.

Done: both r5 corrections, pinned source/test inventory, 17 individual behavioral RED and final GREENs, six final actual-parent controls with pre-cleanup ownership, exact full sandbox command 205/205, additive scope/prefix proof, frozen FIX5 runner, unexecuted authorization-gated launcher, hash manifests and this report. Half-applied work: none. Running commands: none after closeout. Current failing tests: none on the corrected frozen candidate; all intentionally failing REDs and first-attempt native exits are preserved at their named paths.

Next step: MAESTRO18 reads this report and `candidate_frozen.json`, verifies `SHA256SUMS`, and sends this concrete candidate/evidence to GPT-6-Astra. MAESTRO owns host execution and commits. Do not run the inherited-mask launcher without new explicit operator authorization. Changed paths/hashes are the table above and `SHA256SUMS`; exact future host commands are above. Keep other builders' work untouched.

Binding context directive, restated for every successor/team session: watch **Context N% left**. Start a new piece of work only at **60% left or more**. At **40% left or less**, stop starting work, append a precise handoff to `build_report.md` covering done/half-applied work, exact file paths/SHA-256, failing tests and exact commands, and next step; reply exactly **CONTEXT HANDOFF WRITTEN**. If **Context compacted** appears, do that immediately. Hand off before roughly 20% and avoid compaction; the stricter 60%/40% thresholds control earlier. Restate this directive in every handoff. No compaction was observed during this build.


## CONTEXT HANDOFF — operator stop at 37% (2026-10-10T19:56:40.640074+00:00)

MAESTRO reported **37% context left**, below the 40% stop line. The command in flight finished before this handoff. **No further work was started** beyond this requested handoff and its checksum refresh. Running commands: **none**. This is the authoritative successor handoff; it preserves the preceding completed-build receipt as an exact prefix (22308 bytes, SHA-256 `0d4fb5f4d87d4d75f414cb212bed3a5f9270092604ecc1a60869d7c1ba57477d`). Reply status is CONTEXT HANDOFF WRITTEN, not a new qualification claim.

### Done

- Start pins and worktree/branch verified; both supervisor files remain unchanged vs git HEAD. All 188 existing test methods remain.
- Both r5 arrangement-(c) production corrections are applied: guarded original-mask restoration for OwnedWorker/deadline/handler critical sections, and shared INVALID-ENFORCEMENT refusal at direct supervision and both parent mains before timed filesystem work. Construction source pin and existing literal pin expectation are updated. Original identity deadline method checks signal-state preservation before teardown.
- Frozen inventory: **205 total = 69 construction + 41 identity + 34 geometry + 61 supervisor**; **17 new methods = 8 C1 + 9 C2**.
- All 17 behavioral REDs against unchanged production saved in `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/red_qualifying/`; all 17 individual final-candidate GREENs saved in `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/green_frozen/`. Indexes bind exact commands, exits and file hashes. Initial nonqualifying active-phase native-exit attempts are retained in `red_all/005.log` and `006.log`; qualifying line-510 evidence uses the second genuine schedule, including an owned child and post-unwind ownership snapshot. No fixture mask repair.
- Final six actual-parent controls pass in `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/step2_actual_parent_final/`: Python return 2, separately observed native interpreter exit 0, .2-s parent budget, every parent interval <.3 s, state preserved, and complete pre-cleanup ownership/channel/group observations in child cases. Preblocked cases acquire no owner and create no diagnostic output.
- Exactly one authorized full shared-process four-suite command passed **205/205**, exit 0, no ResourceWarnings, no ignored exceptions, no timeout. `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/full_acceptance.log` SHA-256 is `4bbf486c67d776cd86241b2ff5bb595373545982fa61880c643fbff586004151`; `acceptance_command.json` and `acceptance_result.json` bind its command/count and unchanged before/after candidate hashes.
- Additive FIX5 scope revision preserves all prior bytes; `scope_prefix.json` records proof. FIX5 runner copy preserves historical execution/failure-stop contract and explicitly expects 205. Historical runner is untouched. Inherited-mask launcher is written, AST-parsed only and **UNRUN**, requiring separate explicit operator authorization.
- Build report, frozen manifest, source/preservation diffs and checksum inventory are written. Other builders' files are untouched and excluded from protected hashes. No commit, push, merge, model/GPU gate operation, real diagnostic or external inherited-mask launch was performed.

### Half-applied / in-flight

**None.** Production, tests and requested receipt deliverables are complete for this build scope. No test or subprocess remains in flight. No handoff-time source/test edit was made. This section only appends to build_report.md and refreshes SHA256SUMS so the report's appended bytes are covered.

### Exact changed repository paths and current SHA-256

| Absolute path | SHA-256 |
| --- | --- |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_construction_diag.py` | `744f063374a766efbfffc5a1ede73be04a323210e6b4dad48e569e5a41545ec3` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_identity_diag.py` | `919b3a11a836973ea4c0d2abdd2514634ea62792e6009e828a63d81f297c3d0d` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_construction_diag.py` | `995e81cde32c2defd0379ec5bd87d1f78638b462293a3179c479fd73e565a686` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_identity_diag.py` | `047e1425a30be7daa58194a5f94862b865dee5f09ff0060ed51d6902e5d0ca0e` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_scope.md` | `19dda1126da0f2df2fa5418583cbcd1ba6a4be8411fcb52965b7396e369b9217` |

### New executable/inventory deliverables and current SHA-256

| Absolute path | SHA-256 |
| --- | --- |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/candidate_frozen.json` | `7e2a6df28c0b0c2acc08afe6bfdd6ff70c69d119796cc23c23926134987bbd19` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/candidate_sha256.txt` | `591c103eeadf4f7fc0b631e4405c819a0492ae257820229c576b9e6bb9e64eca` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/fix5_inherited_mask_launch_01.py` | `dd7ea183d5d99d395c6dbd1b0e307f2460120bfa29d42d6a9fc02211597c8ab1` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/fix5_inventory.json` | `f257c10b8eb86df14f1bdcb4eeb03d614323206a6fbe8694ae5cb16e65a680ea` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/parent_control.py` | `8e477e56428e79dc7d429e71ddd7497424fec97d10a7a60aa1e9bf439411adcb` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/run_checks.py` | `e0157653709d4778f23db334544afe8038bb7ae555c96180cd5e167d78510d21` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/run_parent_controls.py` | `52a8cb74469cde86acf5c268a86766a84d886d067edb98e95a54a4469653f04d` |

Every remaining new receipt, copy, log, JSON and diff has its exact path and SHA-256 in **`/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/SHA256SUMS`**, refreshed after this append, including the final build_report.md. Paths in it are relative to the absolute worktree root `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`; no other builder's file is included. The report's final hash and the checksum list's own hash are printed by the handoff write command; their self-hashes cannot be embedded in their own bytes.

### Failing tests and exact commands

**Current corrected candidate failing tests: none.** Exact completed acceptance command (do not rerun in this context-exhausted session):

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -W error::ResourceWarning -m unittest tests.test_new1_construction_diag tests.test_new1_identity_diag tests.test_new1_geometry tests.test_new1_supervisor
```

The intentionally failing behavioral REDs are all 17 method IDs and exact interpreter commands in `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/red_qualifying/index.json`; each individual log is indexed in the RED-to-GREEN table above. They are historical evidence, not current failures. The command that saved them on unchanged production was:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/run_checks.py red --label red_qualifying
```

The exact completed final individual-GREEN command was:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/run_checks.py green --label green_frozen
```

Do not rerun either command into its existing exclusive namespace. The prior FIX4 failed 0/3 and investigation receipts remain unchanged; they are not newly earned FIX5 qualification. No new test/failure investigation is pending in this build.

### Next step and open risks

**MAESTRO18**, in a fresh session, verifies this report, the appended handoff and `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/SHA256SUMS`, then sends `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/candidate_frozen.json`, source/test changes and RED/GREEN/control evidence to **GPT-6-Astra** for binding review. MAESTRO18 owns host coordination, execution and commits. The 20-solo prerequisite, fresh 3/3 batch and later 100+10 host repetitions are **UNRUN by MB23**; exact runner commands are already above. Coordinate them on a quiet host with no competing test load and stop on the first failure. The externally inherited-mask control **fix5_inherited_mask_launch_01** remains **UNRUN and separately operator-gated**; do not execute its written launcher without the new explicit authorization. Real diagnostic approval is separate.

Open limits remain: the historical leaking instruction is not attributed; observer/native-thread/host-load contributions and warned-PID origin remain unresolved; unchanged `tools/new1_supervisor.py:411–428` skipped wait is a separate ownership issue. No fixture pass proves scientific correctness, host qualification or launch readiness. Do not touch MB21/MB22 files or expand the correction scope.

### Binding CONTEXT DIRECTIVE — restated verbatim in substance

Watch **Context N% left** in the status line for this and every team/successor session. Start a new piece of work only at **60% left or more**. At **40% left or less**, **stop starting work**. Write a handoff section at the end of **build_report.md** covering **what is done, what is half-applied, exact paths and SHA-256 of changed files, failing tests with exact commands, and the next step**. Then reply exactly **CONTEXT HANDOFF WRITTEN**. If **Context compacted** appears, do the same at once. Repository context management also says hand off before about 20% and avoid compaction; the stricter 60%/40% directive controls earlier. **Every handoff restates this directive so it survives all handoffs.** MAESTRO's current 37% notice requires this handoff now; finish no further build or verification work in this session.
