**FIX5 conforms to r5; qualification step 3 may start on the pinned bytes, subject to the conditions below.**

Read-only review: no tests, qualification runs, launches, or edits performed. All five candidate hashes and both supervisor hashes match. All **313 checksum entries** verify; closing frozen-candidate verification also has zero mismatches.

Below, `R` means `results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/`.

**1. Contract conformance — PASS**

The isolated FIX5 delta implements arrangement (c):

- `OwnedWorker.close_fd`, `start`, and `step` capture the original mask before mutation and establish restoration protection before blocking: `tools/new1_identity_diag.py:366`, `:375`, `:400`.
- Deadline entry and exit cover the former `:495`/`:510` vulnerabilities. Exit executes timer/phase cleanup even when the blocking call raises: `tools/new1_identity_diag.py:503`, `:519`.
- Handler installation is inside the outer restoration protection. Final cleanup restores the independently retained caller-entry mask, clears the timer, and restores handlers: `tools/new1_identity_diag.py:534`, `:651`.
- Shared `INVALID-ENFORCEMENT` refusal precedes protected work at direct supervision and both parent mains: `tools/new1_identity_diag.py:450`, `:459`, `:680`; `tools/new1_construction_diag.py:234`.

I found no missed named section, partial restoration in the specified schedules, deadline relaxation, or FIX5 change outside contract. The native fail-closed exits remain at `tools/new1_identity_diag.py:630` and `:647`. Both supervisor files remain unchanged; their separate skipped-wait issue remains open.

The commit diff includes earlier NEW1 work. FIX5 isolation is supported by the five independently verified pre-FIX5 copies and `R/candidate_delta.diff:1`. The historical scope is an exact preserved prefix; the additive revision begins at `new1_construction_diag_scope.md:559`.

**2. RED quality — all 17 qualify**

**C1: eight qualifying methods.** MAESTRO20’s reading is correct. The fixture pre-blocks only SIGUSR1; the wrapper calls the real `pthread_sigmask` first, then raises once at the targeted production frame and real `{SIGINT,SIGALRM}` mutation. It does not impose those enforcement bits independently. State and ownership observations precede fixture cleanup: `tests/test_new1_identity_diag.py:442`, `:456`, `:508`.

| C1 coverage | Qualifying RED |
|---|---|
| Deadline entry | `R/red_qualifying/004.log:1` |
| Deadline exit | `R/red_qualifying/005.log:1` |
| Deadline exit with owned child | `R/red_qualifying/006.log:1` |
| Handler installation | `R/red_qualifying/007.log:1` |
| Final handler restoration | `R/red_qualifying/008.log:1` |
| OwnedWorker start / step / close_fd | `R/red_qualifying/009.log:1`, `010.log:1`, `011.log:1` |

The mask REDs show `[30] → [2,14,30]`; handler installation instead leaves a substituted SIGINT handler. The exit schedule injects an entry-guard failure before phase assignment, then interrupts real exceptional `__exit__` cleanup. That qualifies without attributing the historical leak. Its owned-child variant includes matching reaping proof and closed ownership state.

The initial active-phase attempts in `R/red_all/005.log:16` and `006.log:16` **do not qualify** as restoration REDs: native termination prevented the required post-unwind observation. They are correctly excluded.

**C2: nine qualifying methods.** Direct supervision, construction main, and identity main each cover ALRM-only, INT-only, and both. Here the imposed entry mask and pending signals are the intended invalid precondition. Unchanged production reaches the protected-work sentinel instead of refusing; corrected production refuses before it. These are boundary sentinels, not replacement refusal logic: `tests/test_new1_identity_diag.py:392`; `tests/test_new1_construction_diag.py:1286`. Evidence: `R/red_qualifying/001.log:1`–`003.log:1`, `012.log:1`–`017.log:1`.

All 17 REDs bind unchanged production and exit 1; all 17 frozen GREENs restore/preserve the asserted state and exit 0.

**3. Steps 1–2 — PASS, with one reporting caveat**

Independent inventory inspection confirms **188 retained + 17 new = 205**, distributed **69/41/34/61**. Only the existing pin assertion and deadline-state assertion changed among existing methods.

The actual-parent driver invokes construction main and production supervision, with science boundaries stubbed. It configures `.2 s`, measures the parent interval separately, and observes ownership before temporary-directory cleanup: `R/parent_control.py:41`, `:63`, `:69`.

| Final control | Parent seconds | Ownership |
|---|---:|---|
| Unmasked blocked preflight | 0.102823541 | None acquired |
| Unmasked blocked monitor | 0.111038917 | Worker 52379 reaped; guardian 52378 collected |
| Unmasked resource/cleanup | 0.005282416 | Worker 52384 reaped; guardian 52383 collected |
| Preblocked preflight | 0.000287583 | None acquired |
| Preblocked monitor | 0.000301250 | None acquired |
| Preblocked resource/cleanup | 0.000289125 | None acquired |

Each corresponding `R/step2_actual_parent_final/<control>.json:5` records Python return **2**. The index separately records native interpreter exit **0** and return markers at `:14`, `:108`, `:245`, `:381`, `:465`, `:549`. Owned cases have matching proof, worker/group absence, closed channels, and empty streams. Preblocked cases preserve mask/pending state and have no callbacks, owner, namespace, or output.

The saved full run is **205/205 OK**, 17.621 s unittest time, 17.808941958 s process wall: `R/full_acceptance.log:49`; `R/acceptance_result.json:1`. Its 17 `ResourceWarning` text occurrences are echoed argv; there are zero `ResourceWarning:` diagnostics and zero ignored-exception markers.

The handoff’s acceptance claims agree with raw receipts, and its preserved-prefix hash recomputes. However, `R/build_report.md:157` says no compaction was observed, conflicting with your session account. I do not accept that sentence as reliable provenance. It does not invalidate the independently verified receipts.

**4. Runner and launcher — designs accepted**

`R/run_checks.py:15` preserves suite order and the solo target; `:40` preserves fresh-process execution and warning enforcement; `:65` explicitly requires **205** for full runs and stops on first failure. The saved historical-runner delta recomputes exactly.

The unrun launcher blocks and records signals before exec (`R/fix5_inherited_mask_launch_01.py:65`), captures fresh-interpreter entry state (`:7`), and uses the inherited branch without resetting the mask (`R/parent_control.py:50`). Startup and parent timing are separate; return, ownership, state, and native-exit evidence are checked (`launcher:50`). **Design acceptance supplies no execution authorization.**

**5. Step-3 clearance conditions**

1. Reverify the frozen manifest before starting; preserve these exact source/test/runner bytes throughout qualification and verify recorded hashes.
2. Coordinate a quiet host without competing test jobs. Run **20 consecutive solo runs**, then a **fresh 3/3 full four-suite batch**, through `R/run_checks.py`, using fresh receipt namespaces.
3. Stop on the first failure, warning, ignored exception, timeout, unexpected native exit, count mismatch, or cleanup leak. No selective restart, suite isolation, suppression, or relaxed bounds.
4. Step 4 still requires separate explicit operator authorization. The later **100 solo + 10 full** host bar and real-diagnostic approval remain unearned.

**FIX4 remains permanently 0/3. FIX5 step 3 starts at 0/20 solo and 0/3 full.** Neither one-off full-suite check contributes to that batch.

Graft savings unavailable: its single probe failed before producing a tally.

VERDICT: GO-QUALIFY