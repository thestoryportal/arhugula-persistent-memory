PROCEED

Independent Opus advisor, pre-run review of D-C10w-oracle phase P2 (authorization + launch plan). Read-only; no stage, GPU, torch or codex run. I did not read the parallel Astra review. All paths are relative to W = /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a, with P1 = W/results/c10w_oracle/p1_20261007T223707_598959Z.

## BLOCKING

None. Nothing in the frozen code, the authorization file, the wrapper or the plan has to change before `p2-a7-s1`. The residual risk raised in Problem 1 is accepted below (B9), with reasons. The advisories are cheap and I recommend them. None of them is a gate.

## What I verified independently (not taken from the packet)

- Hashes, re-computed: `P1/authorization_P2.json` = 1a35ace1…ce43, `P1/eval.json` = f8886427…bd60f, `P1/verdict.json` = 1a77abb3…8ec8a2. These match the `p1_eval_sha256`/`p1_verdict_sha256` fields in the file. `tools/run_c10w_p2_stage.sh` = 5bb10e0a…53b1. Both files are tracked in git (`git ls-files`; commit 621e29d).
- All 15 step-0 frozen refs re-hashed OK against `step0_20261007T223638_531381Z/step0.json`. The prereg sha d2aa240e… equals `PREREG_SHA` (read.py:20). Git shows no diff on `experiments/track_c/`, `tools/engine_fingerprint.py` or `memit_dry_run`.
- First-stage guard arithmetic in Python floats: `0.+0+38.*2400/400+220.` = 448.0, and `<= 448` is True.
- P1 preconditions for the P2-only same-seed block (eval.py:441–448): `P1/eval.json` `oracle_p1` A7 has `extra.generated` with 72 entries, 72 distinct (subj, template) pairs, and an `ids` key on each. Every one of the 5 P1 `train_records` carries `record_file`, which `verify_linked_train` (read.py:525–528) needs for disk_phases/replication_for.
- P1 adapters are git-ignored (`.gitignore:25 *.safetensors`). That satisfies `require_untracked_adapter` (read.py:139–140), and a P2 adapter path is ignored the same way.
- Live `ps`: the wrapper's pattern (run_c10w_p2_stage.sh:7) matches only pid 79246 (`c10v_layerpick_arms.py pass1`). It does not match the Lab View http.server, context_watch.py or the dashboard tiles.

## A. Authorization

1. **Yes, it meets every consumer.** `require_authorization` (read.py:122–127) reads only `auth["P2"]`. It needs `authorized is True`, a truthy `recorded_by` and `recorded_at`, and the two P1 hashes (:126). `budget_minutes` reaches `check_phase_minutes` (:117–119). The consumers are `ensure_authorized` (step0.py:343–352), `authorized_phase_entry` (read.py:531–539), the eval (eval.py:363–366), `replication_for` (read.py:545–546) and `disk_phases` (read.py:601–602). The projection guard (step0.py:325–331) reads only `ruling.get("budget_minutes")`. Its identity `require` at :328–330 is P1-only.
2. **Yes, the hash bindings are correct.** Every consumer compares against `sha_file(p1/"eval.json")` and `sha_file(p1/"verdict.json")` (step0.py:344–348; read.py:536, :546, :601; eval.py:366). The file's own hash is bound later, by `file_ref` into the P2 preflight.json (step0.py:352, :380), and is checked by `verify_ref` (read.py:535; eval.py:365).
3. **Yes, the unit is minutes.** The guard compares it to minute projections (step0.py:319, :331; read.py:478 `P2_minutes`). As the packet notes, `budget_minutes` *replaces* `PHASE_LIMITS` and is not capped by it (read.py:118). At 448 the two are equal, so this has no effect.
4. **Yes, the extra keys are harmless.** Nothing reads top-level `class`/`decision_id` from the authorization. Every reader indexes `[phase]` (read.py:123–124; step0.py:327).
5. **Yes, the replay uses production code** (scratchpad/validate_auth_p2.py:13, :18–22, :28, :33, :35, :51, :71): `S.ensure_authorized`, `R.verify_preflight_certificate`, `T.require_training_preflight` (with the real verify-preflight subprocess, train.py:65–68), `S.guard_training_unit` and `S.guard_phase_projection`. The script's local `pend` (:46–50) only *prints* the projection. The PASS/HALT column comes from the production guard. Two minor shortcuts: the certificate is JSON-round-tripped instead of going through `write_json` (finite() is skipped, but the values are finite); and `entry_preflight` ran in the validation shell, not in the wrapper's env. Neither can change the outcome. See C.
6. **Yes, it is within authority.** EXPERIMENT_RUNBOOK.md:364 says verbatim "the program writes `<p1>/authorization_P2.json` … citing this D-ID". The `recorded_by` string cites D-C10r-rulings-12 and the 448 bound. `authorization_P3.json` correctly does not exist yet.

## B. Launch plan

1. **Yes, the order is correct and complete.** read.py:28–33 and :483–485 give 6 training stages plus `p2-eval`. The dispatcher enforces a prior PASS (step0.py:389–392), and the eval requires all six (`phase_trains`, step0.py:414; read.py:513–522).
2. **Yes, the env is correct.** run_c10w_p2_stage.sh:12 unsets exactly `FORBIDDEN_ENV` (read.py:21–22). `LLMDB_ROOT=$W` is set inline (:14). run_c10w_stage.sh:9–14 checks it, exports it and cds into the worktree. `run_child` re-pins `LLMDB_ROOT` for every child (step0.py:299).
3. **Yes, the logs are correct.** The outer log gets the exclusivity line plus the full stage output plus `STAGE_EXIT` (:13–15). The inner `<p2dir>/<stage>.log` gets `STAGE_EXIT` from `run_child` (step0.py:295–300). A retry writes a separate inner log, `<stage>-retry800`.
4. **The exclusivity check is adequate, and it fails closed.** Gaps (advisory A3): `grep -E 'python.*…'` is case-sensitive, so it misses a process whose argv[0] is a framework `…/Python.app/Contents/MacOS/Python`. Live examples are pids 60203 and 723 (CLT and Homebrew Python, no torch, so they are not GPU users). `tmux has-session -t` also prefix-matches. And the check runs only at launch (see A2). A benign false match exits 3 before the log is created, so the stage can be retried. It cannot block P2 permanently.
5. **Yes, refuse-repeat is correct.** :6 runs before the exclusivity check and keys on the outer log only. `run_child` also refuses an existing inner log (step0.py:296).
6. **Yes, `nohup … & disown` with `< /dev/null` is correct.** It is the same pattern used for P1 and C10V. Optional: macOS sleep would stall MPS. P1 ran about 5 h without `caffeinate`, so this is not required.
7. **Yes, the 448.00 ≤ 448 boundary is robust.** At the first stage `completed` is empty (fresh dir, step0.py:288–290, :335), so `per400` = 38.0 and the projection = 228.0 + 220.0 = 448.0 exactly. No measured float enters the sum (verified in Python).
8. **Yes, the characterization is right, and the risk is stronger than "measured" suggests: it is structural.** On a first-pair retry, `fitted` is empty or holds only A7-s1, and `matched_retry` adds the mate at 800 even when the mate is already fitted at 400 (step0.py:337–339). The pending steps are therefore 3200 = 8 × 38 = 304 min. 304 + 220 = 524 > 448 even with **zero** minutes spent. No pre-stage check, faster training or ordering trick can rescue a first-pair retry at 448.
9. **Accept the risk as residual, as in D-C10w-p1budget (EXPERIMENT_RUNBOOK.md:354).** It is not a blocker:
   - (a) **The prereg anticipates it.** Prereg :310 sets P2 at 310–448 min *without* retries. :312 says retries are "additional and charged in full". :314 and :316 say "Exceeding a limit requires a recorded budget ruling before further units" and "HALT for the existing budget ruling". The guard HALT *is* that stop-and-ask. The operator's 448 equals the prereg limit, and the program cannot raise it (runbook:364).
   - (b) **It fails closed with no contamination.** The exception path writes HALT.json and the diagnostic only in the P2 directory (step0.py:427–433). The failed 400-step record is kept as evidence. P1, its adapters and the authorization are untouched. No adapter is evaluated.
   - (c) **The probability is low.** All five P1 fits were 480/480 or 24/24 against thresholds of 456/23 (train.py:37–39). Loss fell below 0.05 by step 80–170 of 400, and the final loss was ≤ 4.6e-4 (P1/train/*.json `losses`). Seed 1 changes only the init and data order.
   - (d) **The cost is bounded and P2 is recoverable.** "Permanent" applies to the *directory* (read.py:493), not to P2. A fresh first stage creates a new `p2_<stamp>` (step0.py:377–381; the microsecond stamp means no collision). `latest_directory` picks the newest (read.py:490–494), and `disk_phases` ignores the dead directory because it has no eval.json (read.py:597). Recovery needs no code change. It needs an operator budget ruling, a recorded deviation for re-running `p2-a7-s1` (the D-C10w-p1budget "no stage repeated" rule), and a new outer log name. The loss is about 9–18 GPU-min plus one round trip to the operator.
   - **The alternatives fail.** Stage reordering is impossible without editing hashed frozen code (read.py:31–33 is in `sources.reader`, and the dispatcher enforces order at step0.py:389–392). A pre-stage model-free check adds nothing for the first pair (point 8 shows the result is structural). It is useful only from `p2-canon-s1` on (A5). The only way to remove the risk is a contingent raise *by the operator*. That is the operator's call, and I do not recommend making launch wait on it.
10. **The wrapper contains exactly what P2 needs, nothing extra.** The allow-list (:5), ollama check (:10, per prereg :273) and `< /dev/null` (:14) are additions over the P1 wrapper and are all justified. Nothing is missing.

## C. Gate replays: `require`s on the P2 path that were not replayed, and whether any can fail at launch

- **step0.py:355–410.**
  - Replayed: `entry_preflight` (validation env only), `stage_names`, both `latest_directory` calls, `load_frozen`, `ensure_authorized`, `require_training_preflight` and `guard_training_unit`.
  - Not replayed: `new_phase`/`fresh_directory` (read.py:96–99) and `write_json` of the certificate (read.py:76–83: exclusive create plus finite()). Both are trivial on a new microsecond-stamped directory, and the certificate's floats are finite (178.044…, P1 `wall_seconds`). The prior-unit check (:389–392) has nothing to check at the first stage. Later it needs `records[-1]` PASS, which by construction is the newest of the 400/800 tags.
  - None of these can fail at launch.
- **train.py:137–146.** :138–142 were replayed through the same functions. :144 holds for every P2 unit; the phase comes from `proof["phase"]` = "P2". :146 holds in a fresh directory. The model-side guards (90-min per attempt :42–48; the driver-bytes limit; `frozen_parameters_unchanged`) ran on the same code in P1.
- **eval.py:352–366 and :419–459.** These cannot fail at p2-a7-s1, because they run only at p2-eval. The P2-only parts, never exercised in P1, are:
  - :386 `next(...)` over `unit_for_recipe`. It maps oracle_s1, oracle_s0rt and oracle_canon_s1 onto the six `TRAIN_UNITS["P2"]` (eval.py:339–341, read.py:29), so it holds.
  - :431 `phase_trains(P1,"P1")`. Replayed: it passes.
  - :439 a nonzero ΔW norm. This is model-side.
  - :445 and :448 ordering and denominator 72. The P1 side is verified above (72 entries, 72 distinct pairs). The P2 side relies on the same deterministic iteration in the same frozen evaluator.
  - :459 `read_measurement(disk_phases(...))`.
  None of these can be replayed model-free before P2 trains. They remain the first-run risk of the P2 eval, and that risk is fail-closed.
- **read.py:542–552** runs only after P2's eval. Its preconditions on the P1 side (record_file links, untracked adapters) hold.

## D. Blockers before `p2-a7-s1`

There are none beyond the packet's own checklist (§4 items 1–6): pass1 `STAGE_EXIT` and no track_c python left; `tools/engine_fingerprint.py` PASS; both reviews; hashes unchanged; no `p2_*` directory; no `P1/HALT.json`. Those are required and sufficient.

## Advisories (priority order)

- **A1. Freeze the hashed sources for the whole of P2.** Do this as D-C10v-go did for C10V. `load_frozen` re-hashes all 15 step-0 refs in every dispatch, trainer and eval (read.py:497–505). An edit by *any* session therefore HALTs the next P2 stage. The refs include the shared harness `experiments/track_c/c10e_bandknob.py`, `experiments/track_c/c10p_twopass_arms.py`, `tools/engine_fingerprint.py`, `configs/hparams/qwen25_3b_memit_hparams.json`, `configs/screens/g6_screen_qwen3b{,_v2}.json` and `docs/C10W_ORACLE_PREREG.md`. Do not append any note to the C10W prereg until P2 is read. The same applies to `P1/eval.json`, `P1/verdict.json` and `P1/authorization_P2.json` (packet §2b). Record this in the launch D-ID and in the Codex ASTRA/telemetry build briefs: their build is queued (runbook:365) while P2 runs. Add "hashes unchanged" to the per-stage check, not only the pre-launch check.
- **A2. Let P2 hold the GPU between stages.** The exclusivity check runs only at launch (run_c10w_p2_stage.sh:7–10). Record that no C10V pass2, ASTRA benchmark or other GPU job starts between `p2-a7-s1` and `p2-eval`'s `STAGE_EXIT`. Another session's launcher may lack this check.
- **A3. Harden the exclusivity pattern, optional, at the next wrapper edit only.** Use `grep -iE` or add `Python.app`. Use `tmux has-session -t '=autoresearch'` for an exact name. This is not needed now: nothing on the machine with torch runs under a framework Python.
- **A4. Disclose to the operator, and pre-write the HALT response.** The 20:30 question (SESSION_CHECKPOINT.md:37) asked for "up to 448 min" without saying that the first pair then has **zero** retry headroom. Say it in one plain line in the launch record. Have the first-pair-HALT response ready: stop, then make a decision-ready ask with a number (for example spent + 8 × 38 + 220 + a margin) and the recovery path from B9(d).
- **A5. Run the projection model-free before each stage from `p2-canon-s1` on.** Use the *actual* train records and compute what a retry at the upcoming stage would project. The margins are thin: about 11.8 min at canon (436.17) and about 23.7 min at shuf-rt (424.34). If P2 attempts run slower than P1's 8.72 min per 400 steps, a later retry could also be refused. Knowing this before dispatch lets the program ask the operator early instead of hitting a HALT.
- **A6. Correct the packet's wording.** It says the HALT kills P2 "permanently". That is true of the directory (read.py:493). The phase itself is recoverable under a ruling, per B9(d). Use the accurate wording in the D-ID.
