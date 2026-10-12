FIX-FIRST  
Reviewer: GPT-6-Astra (high)

**BLOCKING**

1. **GPU probe can falsely report free.** `tools/dashboard_mathlab.py:120` trusts `running=None`, but `tools/dashboard_live.py:167` converts nonzero `ps` exits into empty output. Its matcher also excludes `mathlab_harvest.py`. **Fix:** propagate unsuccessful/empty inventories as unavailable; recognize the harvest in the shared detector. Test actual subprocess failure responses, not just a mocked exception.

2. **Real streams overflow the dashboard.** `tools/dashboard_mathlab.py:189` renders every gate before resources/findings; `:223` silently truncates everything after row 40. Step 2 emits 50–60 per-arm/layer checks alone (`mathlab/core.py:246`, `:259`). Resources, findings, candidates and the sole MATH-PROXY banner disappear. The rendered admission check also lost its required bar through horizontal clipping. **Fix:** reserve section space, pin the evidence disclaimer, prioritize failures, paginate checks, and summarize structured observations while keeping thresholds visible. Test builder-sized streams at 110×40.

3. **INVALID calibration becomes a failed experiment.** `tools/mathlab_events.py:184` treats every unsuccessful aggregate calibration gate as FAIL. The builder emits `observed="INVALID", passed=False` (`mathlab/core.py:337`), so until `run_finished` arrives the screen incorrectly announces “Designed cheap stop.” **Fix:** preserve aggregate PASS/FAIL/INVALID explicitly in `fold()`; only FAIL triggers that explanation. Test the stream immediately after the aggregate gate.

4. **Planned checks disagree with producer identifiers.** `tools/dashboard_mathlab.py:25` expects `context_pin`, `baseline`, `inertness`, `budget`, `memory`; producers emit `context`, `law3`, `law5`/`observer-parity`, and stage-specific budget/memory IDs. Completed checks remain “not checked,” alongside duplicate rows. **Fix:** align the shared gate contract with producers; perform any aggregate interpretation in `fold()`, with producer-shaped fixtures.

5. **Admission success can masquerade as step completion.** `tools/mathlab_admit.py:112` assigns standalone admission to step 1/2; `:132` emits `run_finished=PASS`. `tools/mathlab_events.py:176` consequently marks Harvest/Reproduce passed although neither ran. **Fix:** distinguish admission-only completion from experiment-step completion in the shared contract; verify successful admission leaves the experiment step unstarted.

**ADVISORY**

- `tools/dashboard_mathlab.py:83`: newest-file selection silently hides other runs. Show the selection policy and other active-run count.
- Tests are non-vacuous: **43 passed**. One **110×40 headless render completed**; current admission refusal and GPU launch-probe exception appeared honestly as INVALID/unavailable. Blockers above are static findings.
- Prereg SHA matches `33e5aa4e…`. State uses `read_events()`/pure `fold()`; no DuckDB authority found. Torn-line/schema rejection has meaningful coverage.
- Teamdash insertion and name-based launcher look correct; live tmux behavior remains **UNVERIFIED**. LabViz forward requirement preserves the shared contract. No files edited.

Graft: 0 tokens saved; lookup failed because Node was absent from PATH.

