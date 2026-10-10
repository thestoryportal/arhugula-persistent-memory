FIX-FIRST

**Single most important thing:** the code is ready; the launch command is not. Before `step0`, launch every stage through a small launcher script, like `tools/run_c10u_stage_r3.sh:11-13`. The script does `mkdir -p results/c10v_layerpick_logs`, runs the stage with `> <stage>.log 2>&1 < /dev/null`, and appends `STAGE_EXIT=$rc` to the log. Start it with `nohup bash <launcher> <stage> > /dev/null 2>&1 & disown`. The watcher should wait for `STAGE_EXIT=` or a new `architecture_profile/c10v_layerpick_halt_diagnostic_*.json`. It should not judge by log growth.

No code change is needed. Only one launch-plan item is BLOCKING.

## What I verified (evidence)

- **Code state.** No c10v, harness or prereg source has changed since 9120bd6. `git diff --stat 9120bd6 HEAD` lists only c10u, c10w and c10z files. `git status` shows no changes to these files. `results/c10v_layerpick/` does not exist.
- **Selftest.** 43 tests OK, `C10V_LAYERPICK_SELFTEST_PASS`, both in the worktree and in a scratch mirror.
- **Engine fingerprint.** PASS: d941a9fb…, `_cov_cpu` 3 (`tools/engine_fingerprint.py`).
- **Preflight reference.** `law3_reference(results/c10q_stacked/passS.json)` returns ok. The sha256 is 102163c6…, the recipe is `A7_stacked` and the scores are A1 70, A2 71.
- **Fact 4 (autoresearch).** `tmux has-session -t autoresearch` returns "can't find session". See issue 6 for a trap in how this is checked.
- **Fact 5 (GPU).** No model process is running. The largest python process has an RSS of about 30 MB.
- **Model and covariance caches.** The model cache has 2 safetensors shards. The covariance caches for layers 4–8 are present in STATS_DIR (`memit_dry_run/memit/globals.yml`).

## Numbered issues

1. **BLOCKING: the launch command as written can false-HALT or lose its HALT text and exit status.**
   - The plan redirects stdout only, and the log directory does not exist (`ls results/c10v_layerpick_logs` → No such file).
   - Every HALT reaches the console only as `SystemExit("HALT: …")` on **stderr** (`experiments/track_c/c10v_layerpick_arms.py:55`, `:591`).
   - The model load writes a "Loading checkpoint shards" progress bar to stderr (`experiments/track_c/c10e_bandknob.py:48`; the model has 2 shards). Left unredirected, stderr is the launching Bash call's pipe.
     - If the call returns and the pipe closes, that write raises BrokenPipeError. `main()` (`:590-591`) turns it into a procedural HALT at model load.
     - Otherwise the call may block until the run ends.
   - With `& disown`, the exit status is lost.
   - Fix (launch plan only): the launcher described above. Use the same pattern for the reader call. This precedent is what D-C10u-r2go (3) uses (`EXPERIMENT_RUNBOOK.md:346`). Step 5 also had launch-plan-only BLOCKING items (`:352`).

2. **ADVISORY: N1 is fixed. My own mutation run found no new BLOCKING gap.**
   - **Test.** The loop at `c10v_layerpick_selftest.py:932-941` runs the real `runtime_stage` and asserts each specific reason via `assertIn` on the diagnostic (`:752`).
     - `set_score` rewrites the detail rows (`:55-65`), so `recipe_integrity` passes and the halt comes from `recipe_validity`, not from `SUMMARY_COUNTS`. That was the old non-discriminating path.
     - `:942-943` assert that no started or complete marker is written.
   - **Mutation set-up.** Scratch mirror `/private/tmp/claude-501/c10v_mut/root`, with a real `results/` directory. A symlinked `results/` produces a spurious 67-failure baseline. Mutants were applied only there; the script is `/private/tmp/claude-501/c10v_mut/tools/mutate.py`. The baseline was green before and after.
   - **Killed:**
     - M1g (`arms.py:519` → `recipe_integrity`)
     - M1i (`read.py:262` validity skipped)
     - M1h (`read.py:301` → `recipe_integrity`)
     - Control off-by-one; controls checked for A1 only
     - FULL_STRING percent check dropped
     - Envelope bounds (para lower, canon upper)
     - ZERO_BASELINE_WRITE dropped
     - Live-A halt swallowed (`:521`)
     - A validity hard-coded before the gate
     - Started marker moved before live A
     - REPLICATION_NOT_NEEDED dropped
     - The `_LAW5_DEFAULT_CTX` bypass removed
     - Tolerance floor raised ×100
   - **Survivors.** None of these makes the run invalid. Each is correct as written (read).
     - (a) `read.py:252` `para_string_n == para_full_n`: equivalent. `para_full_string` is derived from `para_string_n` (`arms.py:463`), and the rounding at 1/72 steps keeps distinct counts distinct.
     - (b) `arms.py:535` RECIPE_INTEGRITY halt swallowed. The pass still halts at `pass_integrity` (`:549-550`), but only after the remaining candidate recipes have run (up to about 2 h wasted). The test does not pin where the halt happens.
     - (c) `arms.py:510` frozen-vs-current covariance gate: untested, and nothing else catches it.
     - (d) `arms.py:493` / `:138-143` pass1 context pin: untested. The pin is correct: `memit_main.py:304-323` reads the module-global cache the driver sets. However, the reader never compares the pass ctx with step0.json's ctx (`read.py:431`).
     - (e) `arms.py:555` run.json gating: untested. A premature run.json would make pass2 refuse with OCCUPIED (`:582`), and the reader would flag PREMATURE_TERMINAL_RECORD (`read.py:452`).
   - **Other HALT paths in the live A/B gates.** None found untested in a way that could pass a bad record. The LAW#5 III/IV/V requires in the driver are backed by `law5_reading` (`read.py:136-154`, called at `arms.py:395`).

3. **ADVISORY: the go basis (B) holds, but cite the right words and disclose it.**
   - **The operator's go.** The prereg demands "the operator's go" (`docs/C10V_LAYERPICK_PREREG.md:3`, `:86`). The flags are self-asserted (`arms.py:84-86`).
     - The strongest basis is the operator's own instruction in D-C10r-rulings-9 (`EXPERIMENT_RUNBOOK.md:344`): use the research list as the integrated queue and work autonomously. Step 4 is in that queue. Rulings-8 ("recommendations are rulings") alone is weaker.
     - This is not the self-authorization pattern the program refused. That limit was writing a record that relaxes a guard (`:352`, memory `operator-overnight-autonomy-2026-10-06`). Running a frozen, reviewed, compute-only prereg relaxes nothing.
     - It is still a step-specific "operator's go" met by delegation. That is the same situation as r3, which the program flagged for ratification (`:351`, checkpoint item 6). It also contrasts with ASTRA and steps 6–7, where the program asked for explicit goes (`:353`).
     - Record D-C10v-go citing rulings-9 verbatim. Disclose it at close-out. Add one line to the operator message already owed: "step 4 is running under your standing go-ahead; say stop if not."
   - **Steps 1–3.** Step 3 CLOSED PROVISIONAL (`:94`, CORPUS/54) satisfies "after steps 1–3" as sequencing: it has been run and read. Ratification concerns r3's legitimacy, not completion. No element of step 4's design depends on step 3: §3 refers only to the step-1 target (`prereg:78`), and step 1 is UNDERFIT. Say this in the D-C10v-go row.

4. **ADVISORY: GPU order (D).** Starting now is sound if the rule is written down first.
   - P2 cannot be authorized for some time. The verdict reviews, CORPUS/55, close-out and then the operator's yes all come first (checkpoint item 1).
   - **Rule.** A stage in flight finishes. P2 goes next, ahead of pass2. pass2 is a fresh process by design (`arms.py:492`), and the identity survives a gap as long as the hashed sources stay unchanged.
   - **Never kill mid-stage.** That leaves `identity.json`, `law5.json` or `pass1_started.json` behind. A relaunch then refuses (OCCUPIED, `arms.py:47-48`, `:580-583`) and needs a fresh `--out-dir` under `results/c10v_layerpick/`, which means a new identity and a new step0.
   - **Timing (I-INFER).** "2.5–4 h total" covers step0 plus pass1 only. That is 4 recipes at 35–60 min each (`prereg:60`) plus LAW#5 (i)–(v). If replication triggers, pass2 adds about as much again, for roughly 5–8 h in total.

5. **ADVISORY: freeze the hashed sources for the whole window, including read time.**
   - The identity hashes these files (`arms.py:19`, `:69-73`; `read.py:16-21`):
     - the prereg and the selftest
     - `c10e_bandknob.py` and `c10l_mint_lib.py`
     - the hparams file and `globals.yml`
     - `step0_offline.json`
     - every engine .py file
   - `assert_sources` runs at `:500`, `:514`, `:524` and `:548`.
   - The reader also requires the **current** files to match (`read.py:416-418`).
   - Therefore:
     - Do not edit the prereg status line.
     - Tell the Codex panes not to touch the shared harness files (`c10e_bandknob.py`, `c10l_mint_lib.py`) until step 4 is read. The ASTRA telemetry build is a candidate to touch them.
     - Run and save the reader output immediately after each stage.

6. **ADVISORY: the fact-4 check needs a trap note.**
   - PID 51198 is the tmux server hosting the `codex`…`codexj` panes. Its argv still reads `tmux new-session -d -s autoresearch … autoresearch_c10/launch.sh`.
   - So `pgrep -f autoresearch` gives a false positive, and `pkill -f autoresearch` would kill every Codex pane.
   - Check with `tmux has-session -t autoresearch` only.

7. **ADVISORY: the watcher must expect long silences.**
   - `quiet()` (`arms.py:58-66`) hides stdout for every `compute_z` (72 per recipe) and for every LAW#5 capture (`:319`).
   - So between model load and the first recipe banner, the log can be static for a long time. A "no output → stalled" heuristic would false-alarm; this is the class of the r2 false HALT.
   - On success, each stage ends with a line: `C10V_STEP0: <status>` (`:506`) or `C10V_<STAGE>_COMPLETE` (`:559`).

8. **ADVISORY: the preflight reference is a non-baseline recipe.**
   - passS.json's only recipe is `A7_stacked`. It is acceptable because it is preflight-only (identity field `preflight_controls_reference`, `arms.py:79`, `:107`) and the binding LAW#3 gate is the same-process recipe A (`:517-521`).
   - The `law3` naming (`--law3-ref`, `LAW3_REFERENCE*`) still misleads a reader of a halt diagnostic. This is delta-review A5.

9. **ADVISORY: one cost to wall-clock time only.** A QEMU VM ("Try Omarchy", 20 GB, hvf, virtio-gpu-gl) has been up for about 5 days. It was also present during step 5 P1, so it does not affect validity.

**The overturning test (item 4 of the prompt).** The cheapest falsifier is step0 itself. It takes minutes, and a "concentrated map" or "map not reproducible" result ends the experiment with no write (`read.py:86-89`; `arms.py:503-507`). It is correctly placed first.

**Drift check.** The work is on-sequence: step 4 of the agreed queue, a write-path placement lead only (`prereg:82`). The verdict must not be read as F1 or §8.9 closure.
