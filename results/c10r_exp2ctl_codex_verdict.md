# D-C10r-exp2ctl — verdict review of location-control run r3

**Reviewer:** Codex  
**Model:** GPT-6 (exact deployment ID not exposed in this session)  
**Effort:** runtime effort setting not exposed  
**Date:** 2026-10-06 (America/Denver)  
**Scope:** review only. No model or GPU run; the existing reader was rerun without importing torch. Only this review file is authored.

**Verdict: label CONFIRMED.** The binding output is **NO-GAIN-WITHOUT-VALUE-POSITIONS / NO-COLLISION-RECOVERY; quality=OK**. This is a valid negative observation for the specified common-word control. **The size confound remains; the preregistration assigns no mechanism label.**

Citation roots: ordinary paths are relative to the program worktree. `R3/` means `/Volumes/memit/llm-database-poc-mirror/autoresearch_replay_c10_exp2loc_r3/`; `LOOP/` means `/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/`. `LOG` means `results/c10s_sharedz_logs/exp2ctl_r3_run_replay.log`; `READER` means `experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py`. These aliases define the file:line citations below.

1. **Validity: r3 is binding under frozen v2, including its amendments.**

   I independently reran `read_replay.py` on the exact score and receipt with the pinned `.venv/bin/python -B`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`, and a PATH resolving Git to `/usr/bin/git`. It exited 0, repeated all **17 VALIDITY PASS** rows and all **nine GUARD PASS** rows, and reproduced the reported counts and labels. Its tokenizer check reported `torch_imported=false`. This checks the existing artifacts; it is not another science run (`READER:434–436,563–730`; `LOG:297–338,411–412`).

   - **Frozen source:** detached standalone HEAD is `92acd0378d23f4935df9a8bccc0137b36695a40f`; only `edit.py` differs. The executed edit hash is `60556b67bf70062703309fb3ee7232da3f51c4fdf3615a170f0643f9f62baa82`, and the exact permitted-diff hash is `2eb6b215b1d659451e82d24ba972768770cebd5b0f5fd14395892ca1d6497fcf`. The audit compares every tracked file against the pinned tree plus the prescribed patch, including tracked graft files; it does not merely trust a commit label (`READER:243–264`; `LOG:300,304`).
   - **Fresh receipt:** invocation `de9c2372baab48e5ac7559108957987c` binds the one fresh run `runs/20261006-230318_92acd03`, child exit 0, score SHA `5f77c132af977e5f8381af8f7dcdc19d8804561837cadfa9b48170b016c033f5`, all three saved-weight hashes, launch, and three arm provenance records. Initial runs are empty; there is exactly one run directory and score. Receipt failures are empty, and reader/runner exits are 0 (`R3/replay_launch.json:9`; `R3/runner_receipt.json:2,6,38,1163,1170–1171`; `READER:584–606,622–635`; `LOG:301`).
   - **Tokenizer, positions, and capture fidelity:** the precheck compared HF IDs/offsets against the cached Rust tokenizer over 432 pairs and was **11.706 seconds old at dispatch**, inside the frozen 3600-second limit. All three edit-time context lists match the full frozen `e8605172…9fb330` hash and scorer prefix. Every layer has the required count-matched columns (A1 144, A2 288, A7 792); the cyclic selections exclude position 0, subject tokens, and appended value positions. The explicit original-value gather equals the suffix slice on the same captured forward. These are distinct checks from the fixed harness's LAW#5: that gate does not itself certify the deliberately different preserve solve (`R3/tokenizer_precheck.json:3–5`; `R3/replay_launch.json:367`; `READER:439–499,601–640`; `LOG:302–308`; `results/c10r_exp2ctl_codex_redesign_v1.md:238`).
   - **Runtime and exclusivity:** engine fingerprint `d941a9fb…98d3d65` passes with the explicit program root. The before/after fidelity manifests agree over 82 files, the pinned interpreter, macOS, package versions (transformers 4.51.0), model/tokenizer revision, and numeric environment. The process log has **1805 observations**: two before dispatch, one after preflight, 1801 during the run, one after exit; no probe failures. It has five transient foreign detections involving four `c10s_sharedz_selftest.py` processes, with a longest streak of **two** polls, no confirmed contender, and no INVALID mark. The frozen N1 rule rejects three consecutive observations, so these do **not** invalidate r3. Do not describe the record as “no foreign detections.” The inspected selftest uses CPU tensors and imports no model; that source observation is consistent with these being detector false positives for GPU competition (`LOG:303,326–327`; `R3/process_exclusion.jsonl:555,968,1209,1539–1540`; `READER:389–406,654–699`; `docs/C10R_EXP2_LOCATIONCTL_PREREG.md:28–30`; `experiments/track_c/c10s_sharedz_selftest.py:2–5,54–59,451–455`).
   - **Guards and norm comparability:** all nine fixed guards pass: A1/A2 69/69, L1 flips 0, frame count 1, described-as 90.33, L3 30, perplexity 21.594, LAW#5/scope true. Across the 15 arm/layer pairs, control/real summed-square ratios are 0.130210–0.943117 and projected-key norm ratios 0.581166–1.71711, within the frozen [0.1,10] window. No DEGRADED or non-comparable qualifier applies. This broad comparability window is not update-norm matching or proof of equal geometry (`LOG:309–337`; `docs/C10R_EXP2_LOCATIONCTL_PREREG.md:40`).

   **The lock did not change the science.** v2 applies UF_IMMUTABLE to pre-existing entries, including Git metadata and the runtime symlink entry, without following that link. Root and future outputs stay writable. The host logged LOCK PASS over 69 entries with replacement/unlink/chmod/nested-write refusals and a working new-output positive control; current read-only inspection finds the flags still set. Exact source/diff and runtime checks still pass. This addresses incidental graft writes, not an owner deliberately clearing flags (`experiments/track_c/autoresearch_c10/replay_exp2/lock_clone.py:10–21,29–48,76–118`; `LOG:196,300,326`).

   **The two earlier attempts supply no binding evidence.** Run 1 completed but was INVALID because graft changed tracked `.gitignore`; r2 was refused at tokenizer precheck because a tracked graft cache changed and dispatched no edit/scorer. The operator then authorized the locked fresh rerun; r3 did not relax the recipe, thresholds, or validity gates. Its fresh paths/receipt and frozen hashes exclude reuse of either attempt's score. Their observed failures concern indexing metadata, not a changed science path; the evidence does not indicate contamination of r3. Run 1's matching counts remain a non-binding echo, not replication (`results/c10r_exp2ctl_run1_invalid_2026-10-06.md:3–17`; `architecture_profile/c10r_exp2ctl_halt_diagnostic.json:14–18`; `results/c10s_sharedz_logs/exp2ctl_r2_run_replay.log:233–235`; `EXPERIMENT_RUNBOOK.md:333`).

2. **Label: the frozen rules are applied correctly.**

   Raw A7 per-fact hit vectors sum to **H=7/72**, partitioned into **C=0/48** (16 collision-head facts × three held-out prompts) and **O=7/24** (the other eight facts × three). C measures full-sequence held-out hits, not first-token hits or a count of collisions prevented. The reader verifies the 16/8 partition and H=C+O (`READER:502–547`; `LOG:299,338,387–410`).

   **NO-GAIN-WITHOUT-VALUE-POSITIONS** means this weight-1, count-matched common-word control has H in **0–7**, the frozen baseline endpoint range; here it equals 7. **NO-COLLISION-RECOVERY** means **zero full-sequence held-out reads** on the collision-head subset. Those thresholds are the recorded endpoints, not confidence intervals or a noise allowance (`docs/C10R_EXP2_LOCATIONCTL_PREREG.md:36–39,48`; `READER:409–416`).

   These labels do not assert that value positions are necessary, that preservation was removed, or that the proposed head-trigger mechanism was observed. Preserve weight remains 1.0. With H≤7 and **D<131.421**, the applicable interpretation is explicitly **“size confound remains; no mechanism label”**, despite quality=OK and passing norm comparability (`docs/C10R_EXP2_LOCATIONCTL_PREREG.md:22,44–45`; `LOG:338,411`).

3. **What is supported, and what remains open.**

   | Recorded endpoint/control | H /72 | C /48 | O /24 | D |
   |---|---:|---:|---:|---:|
   | Loop baseline | 7 | 0 | 7 | 88.974 |
   | Loop experiment 2, attributed to 92acd03 | 18 | 13 | 5 | 131.421 |
   | Valid location control r3 | 7 | 0 | 7 | 90.030 |

   Endpoint definitions: `docs/C10R_EXP2_LOCATIONCTL_PREREG.md:36`. I checked the original score vectors and summaries, not only the ledger's rounded norms (`LOOP/runs/20261006-131156_nocommit/score.json:3–18,1318–1907`; `LOOP/runs/20261006-142644_nocommit/score.json:3–18,1318–1907`; `LOG:299,338`).

   **EVIDENCE-SHOWS:** this specified generic preserve constraint, at its resulting write size, is insufficient to reproduce either experiment 2's full-read gain or its collision-subset recovery. It is a negative instance of “a count-matched common-word constraint suffices,” not evidence that every preserve matrix behaves alike.

   **I-INFER, bounded by the preregistration:** H-location is **not falsified**, but its frozen **H-location survives** reading requires D≥131.421 and is **not earned**. Necessity of value-token positions, the head-trigger story, and geometry/magnitude alternatives remain unresolved. Norm comparability does not equalize the Gram matrices' direction or spectrum, and the final write norm was not held fixed (`docs/C10R_EXP2_LOCATIONCTL_PREREG.md:14–16,40,43–45`).

   The control's D is only **1.056 (+1.19%)** above baseline and **41.391 (31.50%)** below experiment 2. Thus **“experiment 2 gained because it made a larger change” remains live**, neither demonstrated nor excluded. D is the scorer's sum of Frobenius norms across saved A7 weight deltas, rounded to three decimals; similar D is not bit-identical weights (`LOG:338`; `R3/prepare.py:273,279–286`).

   There is **one valid control invocation, seed 0**, comprising separate editor and scorer processes; no across-seed evidence or independent valid replication is supplied. Matching run-1 counts cannot supply that replication. Do not import the unseeded harness's ±4–5 spread, claim statistical significance, or invent a noise band (`docs/C10R_EXP2_LOCATIONCTL_PREREG.md:48`; `R3/runner_receipt.json:2,6`).

   **The original gain's attribution remains a premise.** `LOOP/results.tsv:4` associates 92acd03 with 18 and rounded D=131.4, matching the exact 18/72, D=131.421 score. But that score and its edits record say `commit="nocommit"`; no executed-source hash or corresponding receipt binds that historical run to 92acd03. r3's strong provenance binds **r3**, and cannot retroactively repair the original link or reproduce the original value-position arm (`LOOP/runs/20261006-142644_nocommit/score.json:3,15,31`; `results/autoresearch_c10_exp2_codex_review.md:19`; `docs/C10R_EXP2_LOCATIONCTL_PREREG.md:16,52`).

   This touches the write layer's compile/preserve solve, not the whole readiness determination. No §8.9 closure, CORPUS promotion/label change, route change, or F1 advance follows; C10 stays OPEN/BLOCKING (`docs/C10R_EXP2_LOCATIONCTL_PREREG.md:10,50–52`; `docs/SPEC_E2E_GROUND_TRUTH.md:14,64–65`).

4. **Exact wording for later fold-in; neither target document is edited here.**

   **Register candidate note:**

   > **D-C10r-exp2ctl (2026-10-06; candidate control, not CORPUS):** valid locked-clone r3 under the frozen v2 location-control preregistration → **NO-GAIN-WITHOUT-VALUE-POSITIONS / NO-COLLISION-RECOVERY; quality=OK**. The specified count-matched common-word preserve constraint returned H=7/72, C=0/48, O=7/24, D=90.03; all guards and norm-comparability checks passed. It did not reproduce experiment 2's gain. Because D<131.421, the frozen reading is **size confound remains; no mechanism label**. H-location necessity and geometry/larger-update explanations remain OPEN; the head-trigger mechanism is unproven. One valid seed-0 control invocation; the original 18/72-to-92acd03 attribution still rests on the loop ledger, not executed-source provenance. C10 OPEN/BLOCKING; F1 unchanged. Detailed review and artifact citations: `results/c10r_exp2ctl_codex_verdict.md`.

   **Runbook §5.2 row:**

   | Choice / decision | Status | Record / reasoning | Next |
   |---|---|---|---|
   | **Loop experiment-2 location control (D-C10r-exp2ctl, 2026-10-06)** | **DONE — valid candidate control; labels CONFIRMED; size confound remains** | Frozen v2, locked fresh r3: **NO-GAIN-WITHOUT-VALUE-POSITIONS / NO-COLLISION-RECOVERY; quality=OK**. The common-word control gives no gain, but its write is smaller than experiment 2's, so no mechanism label is earned. Original 18/72 attribution and cross-seed replication remain unverified; invalid run 1 and refused r2 are not evidence. Detailed record: `results/c10r_exp2ctl_codex_verdict.md`. | Candidate note only; no CORPUS label, route, or F1 change. C10 OPEN/BLOCKING. Existing D-C10r-rulings-7 sequencing and reviewed sealing before loop relaunch remain binding. |

