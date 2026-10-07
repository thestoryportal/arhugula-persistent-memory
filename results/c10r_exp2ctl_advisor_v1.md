Reviewer: Claude Sonnet 5.5 (advisor subagent), read-only

# Advisor review of D-C10r-exp2ctl (zero-preserve replay): pre-registration v1 draft + driver

Paths: `PREREG` = `docs/C10R_EXP2_ZEROPRESERVE_PREREG.md`; `RR` = `experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py`; `RUN` = `.../replay_exp2/run_replay.sh`; `SETUP` = `.../replay_exp2/setup_replay.sh`; `IMPL` = `results/c10r_exp2ctl_codex_impl_v1.md`; `SB` = `/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10`.

Reading limits: the harness guard refused every `git` call that targeted the sandbox repo, so I could not read `92acd03:edit.py` or `fd16592:edit.py` as git objects. I read the sandbox working tree (`SB/prepare.py` hashes to the pinned `8e577d54...`, so its line numbers are authoritative) and the program's copy of the baseline recipe (`experiments/track_c/autoresearch_c10/edit.py`, sha256 `0d03bf68...`, the same hash the equivalence records list as the baseline `edit.py`). `SB/edit.py` is a LATER loop commit than `92acd03` (it has `PROMPTS` and `KL_FACTOR = 0.125`), so any claim about `92acd03:edit.py` below rests on the diff context in `IMPL:76-125` and on the Codex review, and is labeled so.

## Verdict: FIX-FIRST

The driver is carefully built. The prereg's reading rule is wrong for this system, and one free, much sharper check is sitting unused.

## Single most important fix

Replace the count-band label (`PREREG:30-32`, `RR:92-99`) with a bit-identity anchor, and make the label conditional on it. The baseline recipe's saved weights are already known to reproduce bit-for-bit across separate processes. With `PRESERVE_WEIGHT = 0.0` the replay's solve should therefore reproduce the baseline's saved weights bit-for-bit (the baseline hashes are listed in issue 1). That makes the "7 plus ~4 spread" band meaningless, and it makes the three `saved_sha256` values in the replay's `score.json` the real validity and outcome gate. A proposed rewrite of §3 is in issue 1.

## Issues, in priority order

### 1. The cut-points (<=11 / 12-17 / >=18) are unjustified, and a determinism replay is not needed to fix that (answers Q1)

What is wrong:
- `PREREG:30` justifies "<= 11" as "the baseline 7 plus the per-process spread of ~4". Nothing cites that spread. CORPUS attributes it to sampling the context templates once per process: `CORPUS/50_C10Q_STACKED_SOLVE.md:30` ("context templates are sampled once per process ... the +/-4-5 cross-process envelope"). The legacy harness has no seed (I grepped `experiments/track_c/c10e_bandknob.py` for `SEED|manual_seed`: no match). The loop does seed: `prepare.py:35` (`SEED = 0`) and `prepare.py:83` (`torch.manual_seed(SEED)`). So the +/-4 band describes a regime this replay is not in.
- The determinism evidence is stronger than "the baseline reproduced 7/72 exactly". Three separate processes produced bit-identical saved weights for the baseline recipe. The A1, A2 and A7 `saved_sha256` values are `2f72fee2...`, `f94e1be2...` and `c30664a9...` in all three of:
  - `results/autoresearch_c10_equivalence_2026-10-06T0815.json` (key `saved_sha256`; started 08:15:43; outside the fence; older `prepare.py` `5260f46d...`);
  - `results/autoresearch_c10_equivalence.json` (same key; started 11:46:53);
  - `SB/runs/20261006-131156_nocommit/score.json` (key `saved_sha256`; the loop's baseline, run under Seatbelt).
  The scorer is deterministic given the weights (equivalence JSON, key `scorer_vs_run_recipe`: every compared field equal). The scorer's templates hash is `e8605172dce0` in all four loop scores I listed and in both equivalence files.
- Given that, the expected replay outcome is a hard identity, not a band. The baseline recipe is `A = P[i] @ (Kf @ Kf.T + cache[i]) + RIDGE*I` with `cache` zero-initialised (`experiments/track_c/autoresearch_c10/edit.py:64,72`). The experiment-2 equation, per the Codex review `results/autoresearch_c10_exp2_codex_review.md:33`, is `Kf @ Kf.T + PRESERVE_WEIGHT * Kp @ Kp.T`. With weight 0.0 the added term is exactly zero (barring inf/NaN in `Kp`, which would have broken the model), so the solve is bitwise the baseline's. The extra forward passes, hooks and diagnostics change no weights and draw no random numbers (Codex review Q4, `:56-62`). The predicted outcome: A1, A2 and A7 hashes equal to the baseline's, `heldout_full` 7, `dw_total` 88.974. The prereg's own prediction (`PREREG:15`) says the same, but its labels do not use it.
- Consequences of the current bands:
  - A replay landing at 8-11 would be labelled SUPPORTS-PRESERVE even though it would show the code is not inert (weights differing from the baseline's at weight 0). That is the real finding in that case, and the bands hide it.
  - PARTIAL-PRESERVE (12-17) implies a dose-response that a two-point design (weight 0 versus weight 1) cannot show.
  - If the hashes do match the baseline, the count is 7 by arithmetic and the label is nearly tautological. Say so in the document.

Recommendation on the determinism control (Q1): do NOT schedule the unmodified `92acd03` replay (about 50 more GPU minutes) up front. The three-process hash agreement already shows the environment is deterministic. The weight-0 replay is its own determinism test, because its hashes can be compared with hashes made in other processes and environments. Run the unmodified replay only if the weight-0 hashes differ from the baseline's. In that case it is the right diagnostic: it should reproduce the recorded experiment-2 values (A7 hash `5b43681d...` and `dw_total` 131.421 in `SB/runs/20261006-142644_nocommit/score.json`; 18/72) and it tells you whether the replay environment or non-inert code is to blame.

Proposed §3 rewrite (keep the existing label names, change the conditions):
- Validity: the existing items PLUS A1, A2 and A7 `saved_sha256` all equal the baseline values above, and the edit-time template hash starts with `e8605172dce0` (issue 2).
- All hashes equal, `heldout_full` == 7, `dw_total` == 88.974: label `SUPPORTS-PRESERVE (exact reproduction of the baseline)`. State in §4 that this means the whole 7 to 18 difference is attributable to the presence of the term in the solve, and nothing about why it helps (issue 8).
- Hashes differ from the baseline: no label; HALT as "UNEXPECTED-NONINERT"; record `heldout_full` descriptively; trigger the unmodified `92acd03` replay.
- Drop the 11 / 17 thresholds, or keep them as non-binding description.

### 2. The edit-time template hash is recorded but never checked against anything (Q2, Q4)

`RR:117-121` computes `context_ok` by re-hashing each record's own list and comparing it with the record's own hash. That is a tautology; it fails only if the file is corrupted. The scorer's `gates.templates_sha` check (`PREREG:27`, `RR:166`) covers only the scorer process (`prepare.py:158-163`), not the edit process; the Codex review says the same (`results/autoresearch_c10_exp2_codex_review.md:64`).

A real anchor exists and is free. `prepare.py:163` hashes `json.dumps(templates).encode()`; the logging does the same (`RR:24`), so the serialisations are identical. `check_equivalence.py:63-68` shows that a process which sampled the templates after running the edit got the same 12-character prefix as the scorer (`seed_reproduces_templates: true`, `e8605172dce0`, in both equivalence JSONs), even though the scorer samples after the law5 edit. So the list does not depend on what ran before it; if any random draw ever lands before the edit-time sampling, the prefix changes.

Fix: in `RR:provenance_checks`, require `len(records) == 3`, require all three `edit_context_templates_sha256` values to be identical (the engine caches the list per process, `memit_main.py:304-323`), and require each to start with `e8605172dce0`. A mismatch is INVALID. Without this, "same random-draw position as the original" is asserted, not tested.

### 3. LAW#1 (engine fingerprint before dispatch) is not run before the replay starts (Q4)

`RUN:12-46` never calls `tools/engine_fingerprint.py`. The only fingerprint check is inside the scorer's `setup_checks` (`prepare.py:136-139,158-161`), which runs after the ~2000-second edit (`SB/runs/20261006-142644_nocommit/score.json`, `summary.edit_seconds` 2011.0). A failed gate therefore costs the whole edit. `CLAUDE.md` makes it LAW: "Before any dispatch, run `python3 tools/engine_fingerprint.py`". The tool imports no torch (`tools/engine_fingerprint.py:24-29`), so it is safe beside a live GPU job.

Trap: `tools/engine_fingerprint.py:31` reads `LLMDB_ROOT` from the environment, and the login shell points that at the main checkout (memory note `llmdb-root-env-points-at-main-checkout`). Run it with `LLMDB_ROOT` set explicitly to the program checkout (`PROGRAM_ROOT`, `prepare.py:28`), so it checks the engine the run will load.

Fix: add the call, with the explicit env var, to `RUN` before the MPS check, exiting non-zero on failure. Also print `gates.fingerprint` (recorded in both existing scores as "engine fingerprint PASS: ...") in the reader.

### 4. The GPU-exclusion pattern misses most GPU jobs the program itself runs (Q4)

`PREREG:22` and `RUN:12` use `pgrep -fl 'edit.py|prepare.py|safe-mode|ollama'`. That catches the loop (`edit.py`, `prepare.py --score`) and the loop's agent session (`safe-mode`), but not the program's own step-1 stage drivers or any other harness run (`c10e_bandknob.py`, `check_equivalence.py`, a notebook kernel). `PREREG:23` schedules the replay right after step 1's stages, which is exactly when a leftover process is most likely. Failure mode: two jobs share the GPU, `edit_seconds` grows past the 2700-second budget (`prepare.py:36`; experiment 2 already used 2011 s, a 689 s margin), and the replay dies at `prepare.py:205,211` after most of an hour.

The loop is described as "paused" (`PREREG:19`), but nothing enforces it; a loop relaunch during the replay is not guarded.

Fix: widen the pattern to the shared interpreter, e.g. `pgrep -fl '\.venv/bin/python|c10e_bandknob|experiments/track_c|safe-mode|ollama'` (the loop wrapper's command line is `.venv/bin/python edit.py`, `experiments/track_c/autoresearch_c10/run.sh:21`). Have `RUN` print the matched list, and have the operator confirm the loop session and `kill_run.sh` state before launch.

### 5. Fidelity to the original run: what could drift, and what is actually checked (answers Q2)

Verified (with evidence):
- Harness bytes are gated: `prepare.py:31,63-65`.
- The interpreter is the same file chain in both cases: the sandbox `.venv` resolves to the worktree `.venv`, which resolves to the main checkout `.venv` (`ls -la` of the links); `SETUP:31-32` links the clone straight to that final target; the scorer uses `PROGRAM_ROOT/.venv/bin/python` (`prepare.py:29,222`). That venv holds torch 2.8.0 and transformers 4.51.0, mtimes 10-03, before every recorded run.
- Config and engine files have mtime 10-04 (hparams, both screens, `engine_fingerprint.py`, `memit_main.py`, `compute_z.py`, `generate.py`, `repr_tools.py`), so they predate the 10-06 runs. mtime is not a hash, but it is evidence against drift.
- The run environment is not numerically relevant: the baseline hashes in issue 1 came both from inside the Seatbelt profile (loop) and from outside it (equivalence checks), so `RUN:46` running without Seatbelt (`autoresearch_c10/run.sh:21`) is covered.

Unchecked or unpinned:
- `prepare.py:32,113` reads `configs/hparams/qwen25_3b_memit_hparams.json`, and the harness reads the two `configs/screens/*.json` files; none is hash-gated, and `engine_fingerprint.py:32,40-43` hashes only `memit_main.py`.
- Covariance caches and the model snapshot (`HF_HUB_OFFLINE=0` per the `IMPL` path-audit table) are unhashed. UNVERIFIABLE by me whether the model revision is truly pinned.
- OS version at the time of the original runs (`sw_vers` now says 26.6.2): UNVERIFIABLE.
- The MPS check is weaker than the original: `RUN:39` checks `is_available()` only, while `autoresearch_c10/run.sh:12` also allocates a tensor on the device.
- Whether run 142644 really executed `92acd03:edit.py`: UNVERIFIABLE. Both scores record `edits.commit = "nocommit"`, so the link rests on the ledger row `SB/results.tsv:4` (dw 131.4 matches 131.421). The 18/72 leg of the contrast is therefore unanchored (issue 6).

The single check that covers all of this at once is the hash anchor in issue 1: if the replay's weights match the baseline's, nothing on that list changed the numbers. Additionally have `RUN` write, beside `replay_launch.json`, `torch.__version__`, `sw_vers`, and `shasum -a 256` of the three config files and of `compute_z.py`, `generate.py`, `repr_tools.py`. These are diagnostics for the case where the hashes do NOT match.

### 6. The prereg should state the premise its contrast stands on

`PREREG:7` and `PREREG:13-14` define H-P1 versus H-P0 using the recorded 18 as the other leg. The replay produces only the weight-0 leg. The 18 comes from run 142644, whose edit source is linked to `92acd03` only by the ledger (issue 5). `PREREG:38` already has a "not claimed" section; add: "the 18 is taken from the recorded run, not reproduced here". If both legs from the same stack are wanted, the cheapest way is the conditional unmodified `92acd03` replay in issue 1, which should reproduce A7 hash `5b43681d...` and 18/72. State that it is not scheduled unless the weight-0 hashes differ.

### 7. Logging inertness and `sys._getframe(1).f_locals["run_dir"]` (answers Q3)

Verified against the patch text (`RR:15-38`; diff in `IMPL:76-125`):
- No random draws, no model calls: only `hashlib`, `json`, `os` and file I/O. It reads `ctx` without mutating it (`json.dumps` is read-only).
- The insertion sits after `get_context_templates` (`RR:47-49`), so it cannot move a draw ahead of template sampling. The four extra imports sit before `from prepare import`, hence before `torch.manual_seed` (`prepare.py:83`).
- The top-level hash runs before `_T_READY` (`prepare.py:128`), so the edit budget does not count it; the in-`apply_edit` part costs milliseconds.
- The frame lookup is safe for all three arms: `evaluate` calls `apply_edit(facts(arm))` directly at `prepare.py:209`, from the frame where `run_dir` was bound at `prepare.py:195`, before the arm loop. The venv is Python 3.11 (site-packages path), where `f_locals` is a plain snapshot dict, so the read is harmless.
- The forbidden-name check (`prepare.py:69-76`) passes on the patched source (`IMPL` self-test, lines 160-162).
- A logging failure would crash early (after template sampling, before the long `compute_z`), which is the right place to fail.

Gap: "inert" is argued, not demonstrated. CLAUDE.md LAW#5 asks for demonstration. If the weight-0 weights hash-match the baseline (issue 1), that demonstrates that the logging and the extra passes are inert in the strongest possible sense. Say that in the prereg and in the reader output.

### 8. Design: the control is necessary but nearly foregone, and it does not separate "the preserve mechanism" from "a bigger update" (real criterion, over-claims, overturning test)

- `PREREG:34` lists `dw_total` as "reported beside". The recorded experiment-2 update was 47.7% larger (88.974 to 131.421; `summary.dw_total` in the two scores, as in the Codex review `:95`). So "the term carries the win" is confounded with "a larger, more aggressive write carries the win". A weight-0 control cannot separate these, because weight 0 is the baseline by arithmetic.
- The per-fact split already points at the claimed mechanism: collision facts 0/48 to 13/48, the other 8 facts 7/24 to 5/24 (fixtures in `IMPL:225,242,287,304`). Pre-register what is expected under H-P1 in the replay (collision 0/48, other 7/24; automatic if the hashes match), so the reader's printout is a stated reading and not decoration.
- The cheapest control that does discriminate (a second GPU slot, not a blocker for this one): the same `92acd03` code at weight 1, but with `Kp` taken at an equal number of positions that are not coined value tokens (for example random common-word tokens in the same templates). If the gain persists, the effect is regularisation or norm, not preservation at collision heads.
- Drift check: this advances the loop-win-to-register hygiene step (`PREREG:7,38`), not F1 directly; the prereg already says so. Acceptable at about 50 GPU minutes.

### 9. Reader and runner gaps (answers Q4: crash, guard failure, partial run, wrong commit)

Covered well: a crash or scorer failure yields no `score.json` (`prepare.py:224-225,293`), so the runner exits non-zero (`RUN:49-51`); a wrong checkout, wrong `edit.py` bytes, wrong `prepare.py` or harness bytes, or borrowed objects raise in `RR:65-89`; the fixtures show INVALID with exit 2 (`IMPL` lines 202-252 and 264-314).

Not covered:
1. `RR:106-128` does not require exactly three provenance records. A truncated or duplicated log passes `all(...)` over whatever is present. Add `len(records) == 3` (issue 2).
2. `score["edits"]["commit"]` (`prepare.py:220`) should be `"92acd03"` (the clone has git, unlike the Seatbelt run); `score["seed"] == 0` and `score["edit_budget"] == 2700` (`prepare.py:292-293`) are unchecked. Add all three; they bind the score to the clone.
3. The provenance is bound to `score.json` only by sitting in the same directory. The synthetic fixture in `IMPL` (lines 322-392) shows a copied baseline score plus fabricated provenance passes all seven gates. Binding to `saved_sha256` (issue 1) and `edits.commit` closes this.
4. `RR:153` does `r["val"].split()[0]`; an empty `val` raises `IndexError`, which `main` (`RR:199-204`) does not catch, so the reader dies with a traceback and exit 1 and prints no INVALID/HALT line. Add `IndexError` to the except list.
5. The `[68, 71]` window for A1/A2 (`RR:167-168`, `PREREG:27`) has an arbitrary upper bound (a later loop run recorded A2 = 71, `SB/runs/20261006-151845_nocommit/score.json`). Under the determinism evidence it should be exact equality (69, 69).
6. `PREREG:32` says a guard failure "does not rescue the term", while the Codex falsifier required "at least 18/72 with every guard passing" (`results/autoresearch_c10_exp2_codex_review.md:105`). The prereg is the stricter reading, which is fine, but say that it is intentional.
7. `RUN` does not tell the operator which run directory to read, does not invoke the reader, and does not save the exit code. A relaunch after a halt would leave several run directories in the clone. Fix: after the wait, find `runs/*/score.json`, fail unless there is exactly one, run the reader on it, write `run.rc`, and exit with a distinct non-zero code for "no score".
8. The `pgrep` branch logic in `RUN:12-22` is correct (`$?` in the `else` branch is the condition's status; 1 means no match), so only its pattern matters (issue 4).

### 10. Prereg bookkeeping

- `PREREG:3` says "v1 DRAFT" while `PREREG:25` says "frozen at v2". Freeze explicitly after these fixes.
- `PREREG:21` describes the logging as "SHA-256 of the executed `edit.py` and of the edit-time context-template list". The actual permitted patch is larger: it also reads `replay_launch.json` inside `apply_edit` and appends the full template list and the launch audit to a JSONL file (`RR:15-38`). Replace the §2 sentence with a pointer to `RR:41-55` and pin the two deterministic hashes from the scratch-clone self-test: `edit_py_sha256 35f3b1a49ec140dadaf4df108afb2138c4e7a2a6c294926bc3f6aa9c587d0c95` and `diff_sha256 1b2a6e4c4a5c59163328da224090d9eac6c9e75058800f3cb5c459eb5355d31e` (`IMPL:62-63`; both depend only on `92acd03:edit.py` and the patch).
- Add this review to the §6 log.

## Answers to the four standing questions, in one place

1. Cut-points: not justified for a seeded run; replace with the hash anchor (issue 1). The recorded evidence is enough; the unmodified replay is conditional, not up front.
2. Faithfulness: interpreter chain, harness bytes and (by mtime) configs and engine are the same. Not hash-checked: configs, engine files other than `memit_main.py`, covariance caches, model snapshot, OS version. The edit-time templates are logged but compared with nothing (issues 2 and 5). The hash anchor covers all of it at once.
3. Logging: inert by inspection; the frame lookup is safe for all three arms; inertness becomes a demonstrated fact only through the hash anchor (issue 7).
4. Gates and exit codes: crash, wrong commit and wrong bytes are covered. Not covered: record count, edit-time template identity, `edits.commit`, engine fingerprint before launch, GPU exclusion beyond `edit.py`/`prepare.py`, and which run the reader reads (issues 2, 3, 4, 9).
