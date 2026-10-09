# MathLab observability report — D-ML-1

The original observability build supplies the shared schema-1 event reader/fold,
view-only dashboard and fixtures. This report records its review fixes;
Codex MB's separate build_report.md is preserved.

## Astra FIX-FIRST correction — 2026-10-09

The five blockers in /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/astra_mathlab_dash_out.md are fixed in one contract/layout implementation round. A subsequent presentation-only correction restores adjacent plain-language descriptions after the independent reviewer spotted their omission.

Changed files: `tools/mathlab_events.py`, `tools/dashboard_mathlab.py`, `tools/dashboard_live.py`, `tools/test_dashboard_mathlab.py`, `tools/test_dashboard_live.py`. Producer instructions only: `results/mathlab_staging/producer_changes_for_mb.md`.

1. Shared GPU inventory reports nonzero/empty ps responses as unavailable; the harvest process is recognized. Tests use real subprocess responses.
2. The disclaimer is pinned; resource/finding/question sections have reserved space; failed checks remain first and pinned; all 63 fixture checks paginate with thresholds and descriptions. Pages rotate every ten seconds. Structured measurements are summarized; event bytes retain full values.
3. The fold preserves aggregate calibration PASS/FAIL/INVALID immediately. Only aggregate FAIL triggers the cheap-stop explanation.
4. The fold owns producer-ID groups for context, LAW#3, LAW#5/observer-parity and emitted stage budget/memory checks.
5. Optional schema-1 purpose distinguishes admission and experiment runs; legacy admission receipts also leave experiment steps unstarted.

Selection is visibly newest events file by modification time; the count of other active runs is event-derived, not process liveness.

### Test-first evidence

Commands: `/usr/bin/python3 -B -m unittest tools/test_dashboard_mathlab.py -v` and `/usr/bin/python3 -B -m unittest tools/test_dashboard_live.py -v`. Initial RED: 53 tests, 3 failures/12 errors; 27 tests, 2 failures/4 errors. Readability regression RED: one test, one failure. Final output:

```text
Ran 53 tests in 0.220s
OK
Ran 27 tests in 0.126s
OK
```

The shared suite retains its pre-existing unclosed-file ResourceWarning. Full logs, source diffs and renders: `/private/tmp/mathlab-astra-fix-ko6gcs3_`. Both scoped git whitespace checks and real `--once 110 40` pass.

### Independent review and evidence boundaries

The bounded fallback GPT-6-Astra reviewer returned PROCEED after an independent 80-test rerun and a 63-gate render; its presentation delta also returns PROCEED. Artifact: `/private/tmp/mathlab-astra-fix-ko6gcs3_/review.md`. Claude subscription auth was probed and unavailable (`loggedIn=false`, `authMethod=none`); same-family review is weaker independence. Live tmux is UNVERIFIED; no restart was performed.

Codex MB's `acceptance_20261009T172912.342899Z` fixture is present: 13 validated events, zero parse errors, one stage, four gates, two findings, HALTED/INVALID. The newer admission refusal is an admission-only INVALID receipt and does not mark Reproduce completed. These checks establish observability plumbing, not scientific calibration or behavioural evidence.

No producer, engine, model, prereg or canonical tracker was edited by this work; no GPU/model imports, launches, commits or service restarts. At the final hash check, the producer implementation files match their starting values; `mathlab/test_mathlab.py` changed concurrently. This work did not edit that producer test file. Exact drift is recorded in protected_end.json. The prereg changed concurrently from `33e5aa4e…`; its current hash and the latest recorded prereg refusal are retained in protected_end.json and the actual render. This work did not write the prereg and makes no claim about who changed it.

### idle — 110×40 fixture

```text
■ MATH LAB · test math estimates using saved model inputs                                                     
 MATH-PROXY · math estimate, not evidence
 Run none yet · not started
 View: newest events file by mtime · other active runs (events): 0
 Elapsed / hard deadline: not started; no launch is implied by this display.
 Pre-registration: DRAFT fixture. Not frozen.
 Current file SHA256: 19420f50590f · docs/MATHLAB_PREREG.md
 Waiting: pre-registration freeze.
 GPU free (no running job reported); admission decides
 Waiting: harvest launcher missing · tools/run_mathlab_harvest.sh
 Waiting: harvest driver missing · tools/mathlab_harvest.py
 Waiting: step-2 notebook missing · mathlab/m2_solve_repro.py
 Waiting: step-3 notebook missing · mathlab/m3_calibration.py
 PLAN · ✓ passed ✗ failed ▶ current · not recorded ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 · 1 · Harvest: record internal model inputs for every prompt (one GPU pass).
 · 2 · Reproduce: repeat the saved write calculation on CPU; check it matches.
 · 3 · Calibrate: check estimates against past results; failure stops cheaply.
 · 4 · Candidate questions: explore ideas later, after a new written plan.
 NOW ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Waiting for a stage to start; the plan above shows what comes next.
 CHECKS · 0 recorded · 0 failed / 0 invalid · page 1/1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 · Safe launch · need engine unchanged; GPU queue cleared
 · Same prompt inputs · need frozen context and tokenisation match
 · Observation changes nothing · need LAW#5 and observer-parity pass
 · Known model answers reproduce · need all three fresh baselines pass their frozen ranges
 · Stay inside time limits · need each emitted stage projection fits its deadline
 · Enough free memory · need stage >=8 GiB; calculation >=8 GiB + reserve
 · Reproduce saved calculations · need projection <=1e-6; write/size error <=1e-5
 · Clean inputs approximate the write · need whole-write error <=25%; direction >=95% (scope only)
 · At least one estimate matches past results · need strict orders; each >=1900/2000 rechecks
 MACHINE · samples from this run; GPU display is shared ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Free memory [················] not sampled · floor 8 GiB
 Lab memory / CPU not sampled · GPU free (no running job reported); admission decides
 FINDINGS · MATH-PROXY: math estimate, not evidence (0) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 None staged yet.
 CANDIDATE QUESTIONS (0; newest 3) · ideas to test ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 None yet; step 4 needs its own pre-registration.
 LAST EVENTS · newest 1 of 0 recent ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 No run events yet; this is the plan before launch.
```

### harvest — 110×40 fixture

```text
■ MATH LAB · test math estimates using saved model inputs                                                     
 MATH-PROXY · math estimate, not evidence
 Run fixture-run · running · step 1
 View: newest events file by mtime · other active runs (events): 0
 Elapsed 3m00s / hard deadline 1h00m · ends 2026-10-08T19:00:00Z · 57m00s left
 PLAN · ✓ passed ✗ failed ▶ current · not recorded ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ▶ 1 · Harvest: record internal model inputs for every prompt (one GPU pass).
 · 2 · Reproduce: repeat the saved write calculation on CPU; check it matches.
 · 3 · Calibrate: check estimates against past results; failure stops cheaply.
 · 4 · Candidate questions: explore ideas later, after a new written plan.
 NOW ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Record the unedited model's inputs for every prompt
 █████░░░░░░░░░░░ 48/162 prompts · stage time 2m00s / cap 5m00s
 CHECKS · 0 recorded · 0 failed / 0 invalid · page 1/1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 · Safe launch · need engine unchanged; GPU queue cleared
 · Same prompt inputs · need frozen context and tokenisation match
 · Observation changes nothing · need LAW#5 and observer-parity pass
 · Known model answers reproduce · need all three fresh baselines pass their frozen ranges
 · Stay inside time limits · need each emitted stage projection fits its deadline
 · Enough free memory · need stage >=8 GiB; calculation >=8 GiB + reserve
 · Reproduce saved calculations · need projection <=1e-6; write/size error <=1e-5
 · Clean inputs approximate the write · need whole-write error <=25%; direction >=95% (scope only)
 · At least one estimate matches past results · need strict orders; each >=1900/2000 rechecks
 MACHINE · samples from this run; GPU display is shared ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Free memory ████████┃███░░░░ 12.5 GiB · floor 8 GiB (┃) · +4.5 GiB above floor
 Lab memory 1.2 GiB · CPU 64% · GPU free (no running job reported); admission decides
 FINDINGS · MATH-PROXY: math estimate, not evidence (0) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 None staged yet.
 CANDIDATE QUESTIONS (0; newest 3) · ideas to test ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 None yet; step 4 needs its own pre-registration.
 LAST EVENTS · newest 1 of 5 recent ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 18:03:00 Machine: free 12.5 GiB; lab 1.2 GiB; CPU 64%
```

### cheap-stop — 110×40 fixture

```text
■ MATH LAB · test math estimates using saved model inputs                                                     
 MATH-PROXY · math estimate, not evidence
 Run fixture-run · stopped: check failed · step 3
 View: newest events file by mtime · other active runs (events): 0
 Elapsed 2m00s / hard deadline 1h00m · ends 2026-10-08T19:00:00Z
 Designed cheap stop: estimates failed calibration. No claim is promoted.
 Neither estimate passed calibration; stop the lab cheaply.
 PLAN · ✓ passed ✗ failed ▶ current · not recorded ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 · 1 · Harvest: record internal model inputs for every prompt (one GPU pass).
 · 2 · Reproduce: repeat the saved write calculation on CPU; check it matches.
 ✗ 3 · Calibrate: check estimates against past results; failure stops cheaply.
 · 4 · Candidate questions: explore ideas later, after a new written plan.
 NOW ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Compare math estimates with past model results
 Progress not recorded · stage time 2m00s / cap 30m00s
 CHECKS · 2 recorded · 1 failed / 0 invalid · page 1/1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 FAIL calibration · bar meets "PASS" · measured "FAIL"
  At least one estimate passes the past-result check
 PASS tier_separation · bar >= 10 · measured 19
  Past results form distinct groups
 · Safe launch · need engine unchanged; GPU queue cleared
 · Same prompt inputs · need frozen context and tokenisation match
 · Observation changes nothing · need LAW#5 and observer-parity pass
 · Known model answers reproduce · need all three fresh baselines pass their frozen ranges
 · Stay inside time limits · need each emitted stage projection fits its deadline
 · Enough free memory · need stage >=8 GiB; calculation >=8 GiB + reserve
 · Reproduce saved calculations · need projection <=1e-6; write/size error <=1e-5
 · Clean inputs approximate the write · need whole-write error <=25%; direction >=95% (scope only)
 MACHINE · samples from this run; GPU display is shared ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Free memory [················] not sampled · floor 8 GiB
 Lab memory / CPU not sampled · GPU free (no running job reported); admission decides
 FINDINGS · MATH-PROXY: math estimate, not evidence (0) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 None staged yet.
 CANDIDATE QUESTIONS (0; newest 3) · ideas to test ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 None yet; step 4 needs its own pre-registration.
 LAST EVENTS · newest 1 of 6 recent ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 18:02:00 Run finished FAIL: Neither estimate passed calibration; stop the lab cheaply.
```

### builder-63-checks — 110×40 fixture

```text
■ MATH LAB · test math estimates using saved model inputs                                                     
 MATH-PROXY · math estimate, not evidence
 Run fixture-run · running · step 2
 View: newest events file by mtime · other active runs (events): 0
 Elapsed 3m00s / hard deadline 1h00m · ends 2026-10-08T19:00:00Z · 57m00s left
 PLAN · ✓ passed ✗ failed ▶ current · not recorded ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 · 1 · Harvest: record internal model inputs for every prompt (one GPU pass).
 ▶ 2 · Reproduce: repeat the saved write calculation on CPU; check it matches.
 · 3 · Calibrate: check estimates against past results; failure stops cheaply.
 · 4 · Candidate questions: explore ideas later, after a new written plan.
 NOW ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Repeat the saved write calculation on CPU
 Progress not recorded · stage time 3m00s / cap 45m00s
 CHECKS · 63 recorded · 3 failed / 0 invalid · page 1/11 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 FAIL 2a-update-mint1_s2-8 · bar <= 1e-05 · measured 0.001
  Offline write reproduces the saved calculation
 FAIL 2a · bar meets "all matches within frozen tolerances" · measured object:30
  Exact offline reproduction of the recorded write
 FAIL 2b · bar meets {"relative_error_max":0.25,"cosine_min":0.95} · measured "OPERANDS-ONLY" (scope only)
  Clean inputs support first-order alternative solves
 PASS admission · bar meets "allowed" · measured object:2
  The launch is allowed by all admission checks
 PASS 2a-projector-A1_single-4 · bar meets {"null_n":20,"probe_relative_max":1e-06} · measured object:2
  Offline projection matches the recorded write
 PASS 2a-update-A1_single-4 · bar <= 1e-05 · measured 1e-07
  Offline write reproduces the saved calculation
 PASS 2a-projector-A1_single-5 · bar meets {"null_n":20,"probe_relative_max":1e-06} · measured object:2
  Offline projection matches the recorded write
 PASS 2a-update-A1_single-5 · bar <= 1e-05 · measured 1e-07
  Offline write reproduces the saved calculation
 MACHINE · samples from this run; GPU display is shared ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Free memory ████████┃███░░░░ 12.5 GiB · floor 8 GiB (┃) · +4.5 GiB above floor
 Lab memory 1.2 GiB · CPU 64% · GPU free (no running job reported); admission decides
 FINDINGS · MATH-PROXY: math estimate, not evidence (1) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 F1: Saved a math estimate
 results/mathlab_staging/F1.md
 CANDIDATE QUESTIONS (1; newest 3) · ideas to test ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 C1 · manual · offline yes · Would smaller writes help?
 LAST EVENTS · newest 1 of 8 recent ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 18:00:00 Candidate: Would smaller writes help?
```

### actual-once — 110×40 actual CLI

```text
■ MATH LAB · test math estimates using saved model inputs                                                     
 MATH-PROXY · math estimate, not evidence
 Run admission_20261009T173935.992389Z · finished · step 2 · admission only
 View: newest events file by mtime · other active runs (events): 0
 INVALID: no verdict; operator review needed.
 Elapsed 0m00s / hard deadline 4m59s · ends 2026-10-09T17:44:35.992624+00:00
 PREREG: frozen preregistration changed
 PLAN · ✓ passed ✗ failed ▶ current · not recorded ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 · 1 · Harvest: record internal model inputs for every prompt (one GPU pass).
 · 2 · Reproduce: repeat the saved write calculation on CPU; check it matches.
 · 3 · Calibrate: check estimates against past results; failure stops cheaply.
 · 4 · Candidate questions: explore ideas later, after a new written plan.
 NOW ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PREREG: frozen preregistration changed
 CHECKS · 1 recorded · 1 failed / 0 invalid · page 1/1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 FAIL admission · bar meets "allowed" · measured object:7
  The launch is allowed by all admission checks
 · Same prompt inputs · need frozen context and tokenisation match
 · Observation changes nothing · need LAW#5 and observer-parity pass
 · Known model answers reproduce · need all three fresh baselines pass their frozen ranges
 · Stay inside time limits · need each emitted stage projection fits its deadline
 · Enough free memory · need stage >=8 GiB; calculation >=8 GiB + reserve
 · Reproduce saved calculations · need projection <=1e-6; write/size error <=1e-5
 · Clean inputs approximate the write · need whole-write error <=25%; direction >=95% (scope only)
 · At least one estimate matches past results · need strict orders; each >=1900/2000 rechecks
 MACHINE · samples from this run; GPU display is shared ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Free memory [················] not sampled · floor 8 GiB
 Lab memory / CPU not sampled · GPU state unavailable: [Errno 1] Operation not permitted: '/bin/ps'
 FINDINGS · MATH-PROXY: math estimate, not evidence (1) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 09_mathlab_admission_20261009T173935.995130Z: Waiting for admission: PREREG: frozen preregistration changed
 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/logs/pending
 CANDIDATE QUESTIONS (0; newest 3) · ideas to test ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 None yet; step 4 needs its own pre-registration.
 LAST EVENTS · newest 1 of 5 recent ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 17:39:35 Run finished INVALID: PREREG: frozen preregistration changed
```

