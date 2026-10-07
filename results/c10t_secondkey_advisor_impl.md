# D-C10t-secondkey — advisor implementation review (step 2)

reviewer: Claude advisor subagent, model Opus 5.5

**Verdict: FIX-FIRST.** Three small BLOCKING items, all driver/reader-side and none touching the engine or the frozen readings. Everything else checks out against prereg v2: the second-request construction, the wrapper seam, arm order, step 0, admission, labels, precedence, the second-process rule, halt ownership and provenance. Once B1–B3 are fixed and the selftest is re-run, PROCEED, with no re-review needed beyond a diff read.

Scope read with `cat -n`: `docs/C10T_SECONDKEY_PREREG.md` (all, including §7; SHA-256 `582896c6…0070`, unchanged), the four new files (hashes match the Codex report), `results/c10t_secondkey_codex_impl.md` and its brief, `c10e_bandknob.py:1–599`, `compute_z.py:20–262`, `compute_ks.py:1–50`, `repr_tools.py:1–140`, `memit_main.py:304–323` (context-template cache), `nethook.py:68–100`, `c10p_twopass_arms.py:26–47`, `c10l_covgeom_step0.py:98–140`, `tools/engine_fingerprint.py`. Model-free selftest re-run here with `.venv/bin/python -B …selftest.py`: **40/40 OK** (Python 3.11.16).

## What I verified (no action needed)

- **Second request, exactly as in §2.** `arms.py:135–141` builds `prompt="The capital of {}"`, `subject=c+" is the city of"+decode(V_ids[:j])`, `target=decode(V_ids[j:])`, bypassing `req()` (no double space). `j ∈ 1..n−1` is enforced (`:136`). The order is blocked: 24 canonical in FICTION order, then the 24 second requests (`:144–146`). The 24 canonical dicts match `run_recipe`'s `req(CANON,c,V)` byte for byte (`c10e_bandknob.py:480`, `:96–97`).
- **Engine path for the value-internal key.** compute_z formats the rewriting prompt as `context.format(prompt)+decode(target[:-1])` (`compute_z.py:46–50`). That prompt contains the extended subject, so its string equals the canonical rewriting prompt (audit check `canonical_rewriting_text`, `arms.py:168`). Labels are end-sliced (`compute_z.py:63–65`) to positions `b−1…b+m−2`, which predict `V[j…n−1]`. The lookup is at the extended subject's last token, `V[j−1]` (`repr_tools.py:85–90`, audit `:169`, `:173`). The KL row `"<c> is the city of <prefix> is a"` uses an unspaced word for an empty prefix (`repr_tools.py:64–70`) and is audited separately (`arms.py:177–180`). The same ID is the K column (`compute_ks.py:19–37`) and the `cur` column in `my_edit` (`c10e_bandknob.py:197–201`), so z, K and cur are aligned on one token per request. The audit implements every C2 condition, including the retokenisation across the prefix/remainder boundary (`prefix_ids`, `full_sentence_input_ids`, `arms.py:167,170`). Mid-word `j` that BPE re-splits are rejected there, not keyed silently.
- **Wrapper seam, engine unmodified.** `H.my_edit`, `H.compute_z` and `H.compute_ks` are rebound as module globals (`arms.py:496`). `run_recipe` and `my_edit` resolve them at call time (`c10e_bandknob.py:489,191,196,219`). The wrapper passes LAW#5 through (`arms.py:228`, `_LAW5_DEFAULT_CTX` set at `c10e_bandknob.py:430`) and passes A1/A2 through on the target mismatch (`:230`). It refuses a changed canonical list or an extra A7 call (`:232`) and publishes the actual list into `_ARM_STATE` (`:243`). The hook re-checks arm name, request identity, 48 fits and 2 compute_ks calls per layer (`:442–445`), so a plan/arm misorder cannot pass silently. `Z_OVERRIDE` is None and hits are 0 (`:234`, `:503`, reader `:295`). One `P` and one base snapshot are restored before every arm (`c10e_bandknob.py:461–474`). Arm order is A1, A2, A7-single, A7-dup, candidates (`arms.py:488–489`), matching §2.
- **A7-dup** is 24 canonical + 24 canonical through the unmodified `my_edit` (`arms.py:223`), i.e. 48 engine z and 48 K columns, which is the H-T3 control as frozen.
- **Context templates.** `get_context_templates` is cached per process (`memit_main.py:305–323`), so the ctx audited in `process_admission` (`arms.py:479–482`) is the ctx `my_edit` uses (`c10e_bandknob.py:182`). The audit re-runs per process and never reselects `j`. Failure raises before `run_recipe`, then HALT.
- **Step 0.** (a) `surprisal()` scores `s_{j+1}` at list index j (`step0.py:42–46`). `surprisal_selection` gives j* = argmax+1 and p10 = argmax over `s_2..s_n` (+1), with first-index ties (`read.py:45–53`). That is correct. (b) It uses the raw second moment and float32 SVD as `compute_P` (`step0.py:66–69`, `c10e_bandknob.py:169–175`). "Protected" means `S ≥ 0.005` (`read.py:56–57`), and the writable share `‖Pk‖²/‖k‖²` uses the complementary directions (`step0.py:83–86`). Both cuts, per-layer winners and margins, and the normalised alternative are present. (c) The screen, nearest-admissible mapping, merge on pre-admission agreement, INVALID-ADMISSION precedence and the "population never changed" rule are all in `read.py:92–126`. (d) Cross-template cosines and the `≤` H-T4 reading are present, with no stop (`step0.py:98–127`, `read.py:146–152`). (e) Requests, digests, overlap, ctx and cov hashes are written exclusively (`step0.py:162–170`).
- **Labels.** LEAD, PARTIAL (`18 < count < 30 ∧ gain ≥ 10`), TRADEOFF, NULL (`read.py:174–180`). All six locality gates plus the 24 per-prefix F1 gates on newly induced next-token hits (`read.py:161–171`). Qualifiers at the frozen strict boundaries (`read.py:187–196`). Replication: LEAD needs LEAD; PARTIAL needs PARTIAL or LEAD with gain ≥ 10. INVALID takes precedence in both processes (`read.py:376–426`). A7-single envelope [5, 18]/[5, 10] and A1/A2 ≥ 68 (`read.py:284–288`). The known A7 baselines (12–13/72, 7–8/24; c10p/c10q logs) sit inside the envelope.
- **Provenance and halt.** Own halt file `architecture_profile/c10t_secondkey_halt_diagnostic.json`, with a UUID suffix if one already exists (`arms.py:53–66`); never the step-1 or solvefeas files. The identity hashes the four new files, the harness, the hparams, both screens, the fingerprint tool, **the prereg**, and every vendored engine `.py` (`arms.py:23–25,69–76`). It is checked before model import and again before publishing (`arms.py:522,551`; `step0.py:169`). Writes use exclusive create plus reread (`:42–50`). `refuse_occupied` runs on every stage. All sixteen harness env knobs are refused, a superset of the four in §2 (`arms.py:26–27,108–110`). Band, fact_token and steps are asserted (`:126`).

## BLOCKING

**B1. Pre-model refusals run after the stage's permanent marker is written, so a shell-environment slip can make the replication permanently INVALID.**
In stage `first`, `run.json` is written at `arms.py:532` before `runtime()` (`:549`) runs the knob refusal and the fingerprint. In stage `second`, `second_started.json` is written at `:547` before them. A leftover `OUT`, `DECISION_ID`, `C10_ARMS` or similar in the tmux shell (earlier c10* runs exported exactly these) has two effects:
- **Stage `first`:** it leaves an occupied `run.json`, which has to be moved aside by hand.
- **Stage `second`:** it writes `second_halt.json`, and the reader then returns INVALID for the whole experiment for good (`read.py:400–403`). That is a non-science failure mislabelling a LEAD or PARTIAL replication.

The no-retry guard only needs to bind once the model run starts.

*Fix:* split `runtime()` into `preflight(root)` (the knob refusal at `:108–110` plus the fingerprint subprocess at `:112–118`; no imports) and `load_harness(root, out_dir, fingerprint)` (the rest). In `main()`, call `fingerprint = preflight(root)` right after `require_sources` and `step0_validity` (`:522–525`), before the `if STAGE == "first"` branch. Pass it into `load_harness` at `:549`. Do the same in `step0.py:138`. Add one selftest asserting that a set knob refuses with `run.json` and `second_started.json` absent.

**B2. The reader adds an unfrozen INVALID condition: `para_string_n != para_full_n` on any A7 arm.**
`read.py:315` makes any id-versus-string difference INVALID for A7-single, A7-dup and the candidates. §3's validity list (prereg :61) does not contain it. Prereg :63 says only "`para_string_n` equal" inside the binding-count line. Every sibling prereg reads the string count as reported beside (C10S :43, C10Q :36), and C10P :38 says "must agree within 2 or the discrepancy is reported", not INVALID. `string_match` can legitimately exceed the id match when the model emits the same text under another tokenisation (`c10e_bandknob.py:121–130`). So one such hit would turn a real LEAD into INVALID.

*Fix:* in `read.py:315`, keep only the row-consistency half: `x["para_string_n"] != sum(sum(r["para_string_hits"]) for r in rows)`. Drop `x["para_string_n"] != x["para_full_n"]`. In `pass_reading`, report `"string_minus_full": cand["para_string_n"] - cand["para_full_n"]` beside the decomposition. The selftest edit at `selftest.py:508` still fails through the row check. Add a case with one extra string hit in the rows and in the aggregate, and assert the label is unchanged.

**B3. The new compute_z observer is never shown to be inert. The LAW#5 gate does not exercise it, and the envelope is too wide to detect a change.**
`observe_solve` (`arms.py:258–294`) installs `sys.settrace` around the science-path `compute_z` for every A7 request, including A7-single. On Python 3.11 (the venv), every trace event runs a fast-to-locals copy and a write-back on the compute_z frame and on every frame it calls (CPython `call_trampoline`). By CPython semantics the write-back is value-preserving, and I expect it to be inert. However, the program's LAW#5 ("demonstrate inertness; do not assume it"; CLAUDE.md gate 2) applies to harness-side changes. Here, `run_law5` runs with the collector inactive (`arms.py:409`, `c10e_bandknob.py:430–435`), so it never touches the observer. The only remaining check is the A7-single envelope, which is 14 counts wide. This is a new seam the frozen prereg did not foresee (§2 says only "LAW#5 gate as it stands").

*Fix:* in `run_pass`, after `process_admission` (`arms.py:480–482`) and before the collector is swapped in (`:496`), add an observer-inertness check (c10s floor rule, `c10s_sharedz_inertness.py` (i)):

```python
def observer_inertness(H, hp, ctx, requests):
    rows = []
    for rq in (requests[0], requests[R.N]):            # first canonical, first second-key request
        args = (H.model, H.tok, rq, hp, hp.layers[-1], ctx)
        with contextlib.redirect_stdout(io.StringIO()):
            a, b = H.compute_z(*args), H.compute_z(*args)  # engine, unobserved, twice
            c, _ = observe_solve(H.compute_z, args)        # engine, observed
        floor = float((a - b).float().norm() / a.float().norm())
        tol = max(10 * floor, 1e-4)
        rel = float((c - a).float().norm() / a.float().norm())
        rows.append({"subject": rq["subject"], "floor": floor, "tol": tol, "observed_rel": rel, "ok": rel <= tol})
    if not all(r["ok"] for r in rows):
        raise ValueError("compute_z observer not inert: " + json.dumps(rows))
    return rows
```

Call it with `next(iter(step["requests"].values()))`, and record it as `"observer_inertness"` in the pass record. In `read.validity`, add `if not record["observer_inertness"] or not all(r["ok"] for r in record["observer_inertness"]): reasons.append("observer inertness failed")`. Add matching selftest fixtures. Cost: six compute_z on the base model, about 1–2 min per process, with no weight write.

## ADVISORY

1. **A pre-registered outcome is filed as a HALT.** INVALID-ADMISSION returns exit code 2 at `step0.py:173` and `arms.py:535`, and both `__main__` blocks route any nonzero exit to `halt()` (`step0.py:179–182`, `arms.py:567–570`). The result is up to two `c10t_secondkey_halt_diagnostic*.json` files reading "step0 exit: 2" for a frozen §2(c) outcome. *Fix:* print the outcome and return 0, or use a dedicated exit code (for example 3) that `__main__` re-raises without calling `halt()`.
2. **The leverage aggregate is an interpretation and needs a ruling on record before step 0.** p5 is chosen from the raw five-layer mean (`read.py:72,87`), with the max-normalised mean only reported beside it. That is consistent with the v1 "five-layer average" text and with Codex design item 1, but v2 never states the primary aggregate. The choice fixes p5, the agreement count and therefore merge versus unmerged. Record a one-line D-ID ruling (raw mean) before step 0 runs.
3. **Root consistency.** The harness is imported from the script's directory (`arms.py:18`), but files are hashed under `LLMDB_ROOT` (`:73–76`). Add `assert Path(__file__).resolve().parents[2] == root` in both mains. Also, `halt()` uses the raw `LLMDB_ROOT` string (`:54`), and the harness `os.chdir`s into the engine (`c10e_bandknob.py:8`). A relative `LLMDB_ROOT` would therefore drop the diagnostic inside `memit_dry_run/memit/`. Pass the resolved root to `halt()`, or set the module global to it in `main()`. The commands below use an absolute path in any case.
4. **The prereg is in the identity**, as asked, so any edit to `docs/C10T_SECONDKEY_PREREG.md` (including the status line) between step 0 and the last pass blocks every stage (`require_sources`). Update the status line before step 0, or not until the verdict.
5. **LAW#3 is checked after the fact.** The A7-single envelope is read only by the reader, so a baseline miss still spends about 40 more GPU minutes on A7-dup and the candidates. The frozen design allows this (one pass, validity read afterwards). An optional early stop after A7-single is a convenience, not a requirement.
6. **Large-record serialization.** `write_json(..., allow_nan=False)` runs only after a pass of about 1 h (`arms.py:552`). A single non-finite value would lose the in-memory record. On failure, dump `json.dumps(record, default=str)` to `pass1.unserializable.json` before re-raising.
7. **Cheap cross-check:** compare the recorded `fits[i]["kl_lookup_idx"]` (`arms.py:279`) with the step-0 admission `kl.lookup_idx` for each second request, inside `validity`. They are equal by construction today; the check would catch drift.
8. **Diagnostic for (a):** the surprisal prompt is a string (as frozen), so for inadmissible mid-word `j` the forwarded context may not equal `CANON_ids + V_ids[:j−1]`. Record a per-`j` boolean `prompt_ids_match` in `surprisal()` so a reader can see which scores were taken under a retokenised context.
9. **Runtime.** The prereg's "≈ 35 min" is stale for this design; see below.

## Cost

- **Step 0.** It loads the model on MPS and runs forward passes only: no weight write, no z optimisation, no `my_edit`. Expect about 10–15 min. Model load and context sampling take about 2 min. Five float32 CPU SVDs of the 11008 × 11008 band covariances dominate, the same as `compute_P`. Surprisal (about 130 forwards), sentence keys and cross-template cosines take under 2 min. A missing covariance cache would instead trigger a long `get_cov` collection; the harness hashes the cache files and raises if any is absent (`c10e_bandknob.py:342–355`).
- **Pass 1, merged B.** Expect about 55–65 min, plus about 2 min for the B3 check. For comparison, the c10p 3-arm pass took about 23 min wall time (logs_c10p_chain.log). Here A7-dup and each candidate run 48 compute_z instead of 24, and each A7 arm adds 1–2 min of F0/F1/subject-free/prefix-reached/bystander probes and 48-key geometry.
- **Pass 1, unmerged B10 + B5.** Expect about 70–80 min.
- **Pass 2.** Same as pass 1, and only if the reader reports `replication_pending`.
- **Worst case:** about 3 h of GPU in total. These figures are untested; nothing here has been run on the model.

## Exact commands (after B1–B3 are fixed and the selftest passes; on the operator's go)

Preconditions: step 1's verdict is recorded (prereg §5). The autoresearch loop is paused and Ollama is stopped. No other GPU job is running.

```sh
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
# preflight (each must pass / print nothing where stated)
pgrep -fl "edit.py|prepare.py|safe-mode|ollama"                     # prints nothing
env | grep -E '^(MODEL_ID|MODEL_REV|HP_CANDIDATE|OUT|CANDIDATE_NAME|DECISION_ID|PREREG|RUN_LABEL|Z_OVERRIDE|C10_PROJECTOR|N_EDIT|C10_SUBJECT_OFFSET|C10_ARMS|C10_KEY_LOCUS|C10_CTX_TEMPLATES|C10_RECIPES|OUT_DIR|POSITIONS)='   # prints nothing
LLMDB_ROOT=$W .venv/bin/python tools/engine_fingerprint.py           # exit 0, d941a9fb, _cov_cpu 3
LLMDB_ROOT=$W .venv/bin/python -B experiments/track_c/c10t_secondkey_selftest.py

# step 0 (~10-15 min), then print the selection; commit results/c10t_secondkey/step0.json (published before the run)
LLMDB_ROOT=$W nohup .venv/bin/python experiments/track_c/c10t_secondkey_step0.py > logs/c10t_secondkey_step0.log 2>&1 &
LLMDB_ROOT=$W .venv/bin/python experiments/track_c/c10t_secondkey_read.py $W/results/c10t_secondkey

# harness pass 1 (~1 h merged / ~1 h 15 unmerged), then the label
LLMDB_ROOT=$W nohup .venv/bin/python experiments/track_c/c10t_secondkey_arms.py first > logs/c10t_secondkey_pass1.log 2>&1 &
LLMDB_ROOT=$W .venv/bin/python experiments/track_c/c10t_secondkey_read.py $W/results/c10t_secondkey

# only if the reader prints "replication_pending": true (a PARTIAL or LEAD)
LLMDB_ROOT=$W nohup .venv/bin/python experiments/track_c/c10t_secondkey_arms.py second > logs/c10t_secondkey_pass2.log 2>&1 &
LLMDB_ROOT=$W .venv/bin/python experiments/track_c/c10t_secondkey_read.py $W/results/c10t_secondkey
```

Confirm each background job is alive from its log and PID before reporting progress. On any HALT, stop: read `architecture_profile/c10t_secondkey_halt_diagnostic*.json`, apply at most one fix after a `cat -n` read, and never move or delete an occupied output without the lead's ruling.

## Diff read (fix round 1)

reviewer: Claude advisor subagent, model Opus 5.5. I read `/usr/bin/git diff HEAD` for the four c10t files and its overall `--stat`. The only other files changed are a one-row addition to `EXPERIMENT_RUNBOOK.md` (§5.2 `D-C10t-p5rule`, line 338) and the Codex report. The prereg SHA-256 is still `582896c6…0070`, and the engine and harness are untouched. The selftest re-run here gives **53/53 OK**.

**Verdict: PROCEED.**

- **B1: fixed as specified.** `runtime()` is split into `preflight(root)`, which does the knob refusal and the fingerprint subprocess with no imports, and `load_harness(root, out_dir, fingerprint)`. `arms.py:553` calls `fp = preflight(root)` after `require_sources` and `step0_validity`, and before both permanent markers: `write_json(run.json)` at `:560` and `second_started.json` at `:575`. `step0.py` also calls `preflight` before `load_harness` and before `step0.json` exists. New selftests confirm that a stale `OUT` and a fingerprint failure leave none of the six stage files.
- **B2: fixed as specified.** `read.py` now checks only that `para_string_n` equals its row sum. `pass_reading` reports `string_minus_full`. The new test `test_extra_string_hit_is_reported_without_changing_label` covers the case.
- **B3: fixed as specified, and it runs before any data is trusted.** In `run_pass`, `observer_inertness` (`arms.py:305`, called at `:510`) runs after the per-process admission (`:504`). It runs before `pre_base_report` (`:515`), before the collector and wrapper swap (`:521`), and before `run_recipe`, including LAW#5 (`:524`), all on base weights. `H.compute_z` is still the engine function at that point. It solves twice unobserved and once observed at both loci: the first canonical request and the first second-key request. The tolerance is max(10 × floor, 1e-4), held as a pure rule in the reader (`observer_inertness_reading`). On failure it raises `ValueError`. That goes to `main`'s `except`, which writes `second_halt.json` on stage 2, and then to `__main__`'s `halt(..., root=RUN_ROOT)`, which writes `architecture_profile/c10t_secondkey_halt_diagnostic.json`. That is the c10t path, and no pass record is written. `validity` also requires two rows at the expected subjects, `ok is True`, and a recomputed reading identical to the recorded one. A failure in process 2 therefore makes the experiment INVALID, which matches "every gate in both processes."
- **Advisories taken, all correct.**
  - INVALID-ADMISSION now returns 0 in both `step0.main` and `arms.main`. It is a recorded outcome and no HALT file is written. The reader still prints the label and exits 2.
  - Both mains assert that the script's repo root equals `LLMDB_ROOT`, before preflight. `halt()` uses `RUN_ROOT`, which is resolved at import, before the harness `chdir`.
  - The `D-C10t-p5rule` ruling sits in `R.PROGRAM_RULINGS`. It is carried in the identity and checked by `require_sources`, `identity_matches` and `step0_validity`. That is an additional integrity check, not a change to any reading.
- **Nothing else changed in the science path.** I found no edits to the selectors, the request construction, the wrapper, hooks, gates, labels or qualifiers beyond the items above. The remaining diff is docstrings and new selftests.

The run commands above stand unchanged. B3 adds about 1–2 min per process.
