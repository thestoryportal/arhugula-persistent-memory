PROCEED-WITH-CHANGES

The authorization is correct. Required changes concern launch supervision; I found no reason to change the frozen science code or raise the budget. Citations below abbreviate `experiments/track_c/c10w_oracle_{read,step0,train,eval}.py` as `read.py`, `step0.py`, `train.py`, and `eval.py`.

**BLOCKING**

1. **Make GPU inspection fail closed.** The wrapper treats an unsuccessful process probe as an empty result. My read-only `/bin/ps` probe returned “Operation not permitted”; the current pipeline does not distinguish that from no matching processes. Its exclusions also remove entire command lines containing `selftest`, `_read.py`, `_interim.py`, or `grep`.  
   **Exact change:** in `tools/run_c10w_p2_stage.sh:7–10`, capture and check each probe’s exit status before interpreting its output. Refuse on inspection failure. Inspect the complete process inventory for unknown Python/MLX/llama/other compute jobs; narrowly exempt verified model-free commands rather than blanket substrings. Keep a single launch coordinator so C10V pass2 cannot start between inspection and P2 launch. The required order is already explicit in `EXPERIMENT_RUNBOOK.md:363–364`.

2. **Replace the log-only waiter and distinguish child attempts from stage outcomes.** Early wrapper refusals create no outer log, so the proposed waiter can run forever; a killed launcher can likewise leave no completion marker. An inner `STAGE_EXIT=75` is an expected fit-miss signal that can legitimately precede a successful retry. Finally, the reader emits status `"UNSTABLE"`, not `"-UNSTABLE"`.  
   **Exact change:** capture the launcher PID before `disown`; monitor launcher termination, `launcher.out`, the outer stage status, and new HALT diagnostics. Missing completion after launcher death means STOP. Advance only on an exact outer `STAGE_EXIT=0`, no HALT, and—after evaluation—a parsed verdict whose status is neither `INVALID` nor `UNSTABLE`. Treat inner 75 according to the dispatcher’s retry chain, not as unconditional final failure.  
   Sources: `tools/run_c10w_p2_stage.sh:5–15`; `step0.py:294–302,398–409`; `read.py:433–434,467–468`; proposed waiter in `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10w_p2_prerun_packet.md:128,147,154`.

3. **Bind the fingerprint check to W, before every dispatch.** The proposed bare command inherits `LLMDB_ROOT`; the fingerprint tool explicitly prefers that environment value over its own location. It can therefore check the main checkout.  
   **Exact change:** before each stage, require successful completion of:
   ```bash
   LLMDB_ROOT="$W" "$W/.venv/bin/python" -B "$W/tools/engine_fingerprint.py"
   ```
   Preserve its output and refuse dispatch on failure. I ran this worktree-bound, model-free check: PASS, expected SHA and `_cov_cpu=3`. That does not replace the launch-time check. Sources: `tools/engine_fingerprint.py:31–48`; `CLAUDE.md:28`.

**Non-blocking**

- **Qualify the later-retry claim.** Replace “A retry in any later stage fits” with “Each isolated later-stage retry fits in the synthetic replay using P1’s worst measured time; accumulated retries or slower P2 attempts can still HALT.” Each replay row reconstructs its own prior history; it is not a simulation of several retries in one phase. Sources: `validate_auth_p2.py:55–64`; `step0.py:310–319`.
- **The validation script is evidence to inspect, not an automated pass/fail gate.** `show()` catches HALTs without failing the script, and negative controls do not assert that a HALT occurred. The saved output contains the expected outcomes, so this does not invalidate the reported checks. Before automated reuse, assert expected outcomes and return nonzero on disagreement. Sources: `validate_auth_p2.py:9–22`; `validate_auth_p2.out:1–9`.
- **Refuse-repeat is sequential, not atomic.** The existence test followed by `>` permits concurrent invocations to race. The stated single-coordinator, one-stage-at-a-time procedure avoids that race; do not describe it as a concurrency lock. Sources: `tools/run_c10w_p2_stage.sh:6,13`; `step0.py:377–381`.
- **Not every refusal produces a phase diagnostic.** Failures before `directory` is assigned produce stderr/exit 2 without the two JSON diagnostics. The revised watcher must retain that failure path. Sources: `step0.py:358,365–378,427–443`.

For the validation citations, `validate_auth_p2.py`, `validate_entry_p2.py`, and `validate_auth_p2.out` refer to the scratchpad directory named in the question.

**A. Authorization**

1. **Yes.** The actual record supplies every required P2 field. I independently reran `ensure_authorized`, certificate verification, and `require_training_preflight`, including its verifier subprocess; all passed without importing torch. The projection guard reads the same 448-minute field. Sources: `P1/authorization_P2.json:2–11`; `read.py:122–127,531–539,583–589`; `step0.py:322–352`; `train.py:51–68`.

2. **Yes.** The two embedded hashes identify P1 `eval.json` and `verdict.json`; the authorization’s own hash is returned separately and bound into the P2 certificate. All three currently match the packet exactly. Sources: `P1/authorization_P2.json:7–8`; `step0.py:344–352,379–381`; `read.py:535–536`.

3. **Yes, minutes.** Training wall seconds are divided by 60, and the resulting projection is compared directly with `budget_minutes`. Sources: `step0.py:311–319,331`; `read.py:117–119`.

4. **Yes.** The writer adds those keys, and authorization validation selects `auth["P2"]` without rejecting additional top-level keys. Sources: `read.py:76–83,122–127`.

5. **The named authorization/certificate/guard functions are genuinely exercised; the complete launch path is not.** Certificate construction is reproduced in memory, while directory creation and writing are omitted. The eval authorization fragment calls the actual helpers but does not call `run_eval`. Detailed coverage is below. Sources: `validate_auth_p2.py:13–35,41–73`.

6. **Yes.** D-C10r-rulings-12 expressly authorizes the program to write this P2 record under the operator’s 448-minute approval; P3 remains conditional. Source: `EXPERIMENT_RUNBOOK.md:364`.

**B. Launch plan**

1. **Correct and complete:** six training stages in the stated order, then `p2-eval`. Sources: `read.py:28–33,483–485`; prereg `docs/C10W_ORACLE_PREREG.md:280–283`.

2. **Correct for the stage itself.** The unset list matches `FORBIDDEN_ENV`, the inline root overrides the inherited value, and the inner launcher changes to W. Apply the same root binding to the fingerprint command. Sources: `tools/run_c10w_p2_stage.sh:12–14`; `tools/run_c10w_stage.sh:9–15`; `read.py:21–22`.

3. **Correct on ordinary completion, with the supervision corrections above.** The outer log records dispatcher exit; inner logs record individual child exits. Retry and matched-retry children have separate suffixed filenames, so `<stage>.log` alone need not contain the final successful attempt. Sources: `tools/run_c10w_p2_stage.sh:13–15`; `step0.py:294–302,398–409`.

4. **Insufficient as an exclusivity guarantee.** It can miss `python /tmp/train.py`, `python -c ...`, or non-Python GPU applications, and can block benign Python work whose arguments contain a matching path. A persistent idle `autoresearch` tmux session also blocks it. Inspection failures currently fail open. Source: `tools/run_c10w_p2_stage.sh:7–10`.

5. **Correct under serialized invocation.** Refusal before log creation permits a later launch attempt; once the outer log exists, repeat is refused. It does not make concurrent invocation safe. Sources: `tools/run_c10w_p2_stage.sh:6–15`; `step0.py:294–297`.

6. **Yes for detachment and stdin handling.** Capture `$!` before `disown` for supervision. Shell acceptance of the background command is not evidence of stage success; the wrapper’s recorded exit is. Sources: `tools/run_c10w_p2_stage.sh:14–15`; launch command in `c10w_p2_prerun_packet.md:122–128`.

7. **Yes, the initial arithmetic is robust.** With no completed attempts, the operands produce exactly `448.0`: `38.0 × 2400 / 400 + 220.0`. I independently recomputed it through `training_projection`. Equality passes; there is no initial floating-point epsilon problem. Sources: `step0.py:310–319`; `read.py:117–119`.

8. **Yes.** The first-pair retry guards include the failed attempt and both 800-step mates. Their prospective training-plus-eval component alone is 524 minutes, already above 448; the recorded elapsed time raises it further. The forced A7 retry after the first shuffled retry is unreachable under this budget because the shuffled retry guard fails first. Sources: `step0.py:313–340,399–409`; `validate_auth_p2.out:18–19,24`.

9. **Accept as disclosed residual risk, not a blocker.** The legitimate consequence is a permanently HALTED P2, never permission to relax the guard. Perfect P1 fits support trying the authorized schedule but do not prove seed-1 fits will pass. Record that acceptance in the P2 go disposition while retaining 448 unchanged. Sources: `EXPERIMENT_RUNBOOK.md:354,364`; `SESSION_CHECKPOINT.md:15`; `step0.py:399–402,427–433`.

10. **Add the fail-closed inspection and worktree fingerprint gate; repair supervision.** The allow-list, environment clearing, logs, and stopped-Ollama requirement are appropriate. The tmux-session prohibition is conservative relative to “loop paused,” but follows the adopted launcher convention. Sources: `tools/run_c10w_p2_stage.sh:5–15`; `docs/C10W_ORACLE_PREREG.md:273`; `EXPERIMENT_RUNBOOK.md:363`.

**C. Gate replay coverage**

| Path | What was actually exercised | What remains unreplayed or dependent on future state |
|---|---|---|
| **Dispatcher entry and frozen inputs** | Production `entry_preflight`, `stage_names`, `latest_directory("p1")`, `latest_directory("step0")`, `load_frozen`, and `ensure_authorized`. The entry script prints the stage-membership result rather than asserting it. Sources: `validate_entry_p2.py:6–12`; `validate_auth_p2.py:13,30`. | Successful `latest_directory("p2")` cannot be replayed before P2 exists; its no-HALT requirement remains live. The first stage does not call it. Sources: `step0.py:377–382`; `read.py:488–494`. |
| **Directory/certificate creation** | The certificate’s values are constructed and JSON-round-tripped, then checked by production functions. Sources: `validate_auth_p2.py:23–33`. | `new_phase`, fresh-directory exclusivity, creation of `train/` and `adapters/`, and production `write_json` at this location were **not** executed. Timestamp collision, permissions, storage failure, or record collision remain possible. No production `require` was bypassed inside the certificate verifier; creation itself was omitted. Sources: `step0.py:286–291,378–384`; `read.py:76–99`. |
| **Training dispatch and guards** | Production `guard_training_unit` and `guard_phase_projection` run on synthetic attempt files. The separately constructed `pending` dictionary supplies the displayed projection, while the real guard independently reconstructs its own pending state. Sources: `validate_auth_p2.py:41–53,65–73`. | Prior-unit PASS checks were not replayed; they are vacuous for the first stage. Child-log nonexistence, child return-code checks, and successful matched retry execution also remain live. Sources: `step0.py:296,389–409`. |
| **Trainer `137–146`** | The constituent frozen-input and certificate functions were exercised, including the separate production verifier. Sources: `validate_auth_p2.py:30–33`; `train.py:51–68`. | `run_attempt` itself was not called. The exact unit/**steps** admissibility require and record-nonexistence require were not executed. `validate_entry_p2.py:12` is a tautological membership expression and omits `steps`; it is not a replay of `train.py:144`. The declared first unit and 400 steps satisfy the source predicate, but actual record absence remains a launch-time check. Sources: `train.py:137–146`; `step0.py:388,393,398`. |
| **Eval entry `352–366`** | Certificate and authorization helpers were exercised. I also independently reran `phase_trains(P1,"P1")`, verifying all five existing P1 adapters. Sources: `validate_auth_p2.py:32–35`; `read.py:513–522`. | P2 `phase_trains` requires six future PASS records, valid adapter hashes and untracked adapters. Equality of every P2 training provenance with the frozen provenance was not replayed. Sources: `eval.py:354–366`; `read.py:513–522`. |
| **Eval completion `419–459`** | No P2 completion replay occurred. Sources: `validate_auth_p2.py:34–35,65–73`. | Attempt-record references, timing aggregation, adapter loading, and same-seed checks are future-state dependent. Specifically **nonzero cosine denominator (`439`), matching prompt order (`445`), and exactly 72 comparisons (`448`) were not replayed**. Neither were final runtime guards, exclusive eval/verdict writes, or P2 `validate_phase`/`disk_phases`/`read_measurement`. Sources: `eval.py:419–459`. |
| **Reader `replication_for`, `542–552`** | Its authorization helper was exercised elsewhere; **`replication_for` itself was not called**. P2 authorization does not enter the P3 branch that calls it. Sources: `step0.py:349–351`; `validate_auth_p2.py:13–35`. | All its P2-record checks remain live: latest non-HALTED directory, phase/P1 linkage, authorization reference and budget, frozen provenance, exact linked training-record equality, adapter hashes/untracked status, and complete phase validation. Sources: `read.py:542–552`. |

The remaining P2 phase-validation requirements include actual environment, complete control/recipe manifests, null and restoration evidence, hit counters, arm/probe consistency, LAW#3/LAW#5, complete matched training identities, fit and frozen-parameter evidence, protocol/provenance, matched A7/shuffled step counts, the positive control, and same-seed denominator/cosine validity. These are **not pre-run PASS claims**. They must remain live gates; manufacturing P2 outcomes to replay them would not verify the future experiment. Sources: `read.py:293–355`.

**D. Before `p2-a7-s1`**

- Complete the three blocking launch-plan changes above, fold both independent reviews, and record the planned `D-C10w-p2go` disposition. The authority and handoff explicitly require the reviews/disposition. Sources: `EXPERIMENT_RUNBOOK.md:364`; `SESSION_CHECKPOINT.md:15`.
- Let C10V pass1 finish and confirm all its compute processes have exited; reserve the next GPU interval for P2 **before pass2**. My process inspection was sandbox-denied, so live exclusivity remains **UNVERIFIED**. The inspected pass1 log had not yet supplied completion. Sources: `EXPERIMENT_RUNBOOK.md:363–364`; `results/c10v_layerpick_logs/pass1.log:37–40`.
- Refresh worktree fingerprint, hash bindings, frozen-source verification, no-P1-HALT, no-P2-directory, and no-existing-P2-outer-log checks immediately before launch. My read-only checks currently pass these file-state conditions, but they can change before launch. Sources: `read.py:488–505`; `step0.py:343–381`; `tools/run_c10w_p2_stage.sh:6`.
- **No frozen-science edit or new science-code commit is needed.** Runtime identity is enforced by frozen file hashes, not a required HEAD commit. Record launcher/procedure changes through the normal handoff workflow; preserve pinned files byte-for-byte and keep adapters untracked. Sources: `read.py:130–140,497–505`; `SESSION_CHECKPOINT.md:15`.

Graft: one failed lookup; no savings reported.

