PROCEED

**BLOCKING**
None. None of the four traces turned up a path that makes the launch unsafe or the P2 reading untrustworthy.

Trace summary (all read at session time; `python -B -m unittest tools.test_c10w_p2_gate` ran 13 tests, all OK):
- (a) Advancing past a failed or HALTed stage: not possible. run_c10w_p2.sh:33 advances only when wrapper rc==0 AND the outer last line is exactly `STAGE_EXIT=0`. That line can only come from run_c10w_p2_stage.sh:19, because the inner STAGE_EXIT goes into the per-directory child log (step0.py:300), not stdout. Lines :34 and :36 then stop on a new diagnostic or on HALT.json in the newest p2_*. That `sort|tail -1` picks the same directory as R.latest_directory (read.py:488-495). The dispatcher writes HALT.json and the diagnostic only on its raise path (step0.py:427-433), so the stage rc is always nonzero there. On resume, :26 skips only `STAGE_EXIT=0` logs and refuses any other log. Predecessor pid 79246 is gone, and pass1.log ends `STAGE_EXIT=0`.
- (b) Admitting while a GPU job runs, or after a failed probe: closed for every Python, ollama, llama or mlx process. Failure handling:
  - ps rc≠0 or empty output refuses (gate:76). tmux errors other than no-server refuse (gate:80). Fingerprint rc≠0 refuses.
  - A non-Halt exception in the guards crashes the gate (rc 1), and wrapper:16 refuses on any rc≠0.
  - On today's inventory the classifier flags nothing. The labviz server, CLT dashboards and the uv MCP servers are all exempt, and the T3 evidence shows that an unexempted `.venv` python blocks.
- (c) Gate replay matches the dispatcher for the guards it replays:
  - entry_preflight (gate:92 / step0:356); load_frozen of the latest step0 (gate:93 / step0:365); ensure_authorized (gate:94 / step0:375).
  - prior-unit PASS (gate:105-107 / step0:389-392); SHUF 800-step selection (gate:108-110 / step0:393-396); guard_training_unit (gate:113 / step0:397); retry800 matched (gate:115 / step0:400).
  - eval: guard_phase_projection plus phase_trains (gate:120-122 / step0:412-414).
  - First stage: the gate's empty temp dir and `p1_directory`-bearing proof give the same projection inputs as the fresh dir and cert (step0:378-381), since the projection only reads `train/*.json` and `proof["p1_directory"]`. The one guard it does not replay is non-blocking item 1 below.
- (d) Nothing writes into results/c10w_oracle/ or touches a hashed source. The gate path is read-only: load_json, sha_file, verify_ref, and `git ls-files` (read.py:133). It runs with -B (no `__pycache__` in experiments/track_c) and uses a system tempdir. The wrapper writes only results/c10w_oracle_logs/{S.log, S.gate.*.json}. The coordinator writes only p2-coordinator.log and p2-read.json. None of these files is among step0.json's 17 hashed `sources`.

Non-blocking:
1. Not replayed: the gate skips `T.require_training_preflight(...)` (step0.py:385-386, which runs for every P2 stage including p2-eval). If it fails at p2-a7-s1, the dispatcher HALTs a freshly created P2 dir instead of the gate refusing. The risk is low: the same cert passed every P1 stage, and the only new path (authorized_phase_entry) re-checks what ensure_authorized already checks. It can be replayed model-free (c10w_oracle_train.py has only stdlib imports at module level). Optional fix at gate:100: build the cert the way step0:379-380 does and call it with `R.sha_file(step0/"step0.json")` and `R.frozen_provenance(frozen)`.
2. Detection gaps: gate:51 takes argv[0] as the text before the first space, so an executable whose path contains spaces (e.g. under "Application Support") fails open. Non-Python Metal or GPU binaries (LM Studio, other apps) are also invisible. No such process exists now; these are covered by the stated rule "no other GPU job until COORDINATOR_EXIT".
3. gate:80: `error connecting` also matches permission-denied socket errors, so they are treated as "no server". This is a fringe case.
4. Commit tools/c10w_p2_gate.py, run_c10w_p2.sh, test_c10w_p2_gate.py and the modified run_c10w_p2_stage.sh before launch. They are currently untracked or modified, and the gate record does not carry its own sha, so admitted records are only attributable to a committed version.
5. Make sure the watcher is not a non-exempt Python process; otherwise every gate refuses with finish 6 and the GPU sits idle. On a resume after a finish-7 caused by an external diagnostic, the SKIP path (:26-27) does not re-check halt diagnostics. HALT.json is still caught by latest_directory, so diagnose the stop before relaunching.
