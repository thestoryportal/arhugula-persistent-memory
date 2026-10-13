Reviewer: Claude Sonnet 5.5 (advisor subagent), read-only

# Advisor review v2 — D-C10r-exp2ctl location-control driver (2026-10-06)

## Verdict: FIX-FIRST

The science patch is clean and the position rule is implemented exactly. The process-exclusion gate is broken in a way that I reproduced on this machine with the real `ps`. As written, the run aborts seconds after the editor starts. It also refuses at the first check on the operator's ordinary toolset.

## Single most important fix

Replace the command-name allowlist in `process_check` (`read_replay.py:313-329`) with ownership by process tree. Treat every transitive descendant of `child.pid` as owned. The runner already puts the editor in its own session (`run_replay.sh:143`, `start_new_session=True`), so every process in that session or process group is owned. Then narrow `MODEL_PROCESS` (`read_replay.py:288`) from "any Python" to processes that can contend for the GPU. Details are in issues 1 and 2. This touches only `read_replay.py`, not the frozen `edit.py`, so `EXPECTED_EDIT_SHA256` and `EXPECTED_DIFF_SHA256` stay valid.

## What I read, and what I ran

- Read in full: the prereg, redesign §3.1 and §3.4 (lines 60–260), the three driver files, impl report lines 1–350 plus the mock-test list. I did not read `results/c10r_exp2ctl_advisor_v1.md`.
- **Pinned files.** `git` on the sandbox repo is refused by this session's worktree guard.
  - `prepare.py` was read from the sandbox working tree. Its sha256 is `8e577d546080f06bbd25a685e9af03016117d1e133ff9ff97aa92e5ac22f21f1`, as required.
  - `92acd03:edit.py` was taken from the diff embedded in the impl report (lines 82–263). The sandbox working-tree `edit.py` is the loop's current file (LAYERS 8–12, weight 4.0), not `92acd03`, so I did not use it.
  - `c10e_bandknob.py` was not read.
- Ran only pure-Python or read-only probes, all scripts under `/tmp/rev_v2_*.py`. Nothing imported torch or transformers, and nothing was run from the fence.
  - `ps -Aww -o pid=,ppid=,lstart=,command=` via `/bin/ps`. In this review sandbox, `ps` is allowed and returned 558 rows.
  - `read_replay.process_check` on the live process table.
  - `read_replay.validate_score` on five recorded `score.json` files.
  - The driver's own `SELECTOR_CODE`, exec'd with the Rust `tokenizers` library, over all 432 fact/template pairs.

## The five questions

### 1. Science isolation: yes, the patch is isolated

Evidence is the diff in impl report lines 116–259 against the original lines shown there.

- **Only the Kp source changes.** `Kp` is now `grabbed[0][positions["indices"]].float().cpu()` instead of `grabbed[0][len(ids):].float().cpu()` (report diff lines 187 and 180). Forward input (`ids + tgt`), hook, `.float().cpu()`, concatenation, transpose and layer order are unchanged. `A`, `B`, `solve`, `upd_matrix_match_shape` and the `+=` cast are untouched (diff lines 229–231 and 249–250). The `Kp` that reaches `A = P[i] @ (Kf@Kf.T + PRESERVE_WEIGHT * Kp@Kp.T)` has the same dtype (fp32), device (CPU) and column order (fact-major, then template, then token) as the original.
- **The `PRESERVE_WEIGHT` line** changes only its comment (diff line 108). It stays `1.0` (float).
- **No RNG draw.** The added code is `hashlib`, `json`, `os`, `re` and `sys` imports, a file read, tokenizer offset calls, regexes, `torch.equal`, `isfinite`, `.square().sum()`, `P[i] @ Kp` and `.norm()`. None of these draw random numbers. `get_context_templates` is still the first RNG consumer; the added `ctx` logging comes after it (diff lines 202–217).
- **Added reads of the solve's inputs.** The extra `P[i] @ Kp` and `P[i] @ _replay_real` matmuls run after `upd` is computed and before the weight add. They only read.
- **The same-capture identity check is costless and inert, but weak.**
  - Cost: two extra index ops and `.cpu()` per forward, 2160 forwards in total, and no extra model forward.
  - Weakness: it compares `x[a:]` with `x[range(a,b)]` on one tensor. It can only fail if device advanced indexing is broken. It does not check that the control indices land where intended; that protection is `validate_positions` (issue 6).
  - The `"identity_equal": True` in the layer record (`read_replay.py:147`) is a literal, set after a raise-on-fail. The reader's `identity_equal is True` check (`:418`) therefore cannot fail independently. Harmless.
- **Time budget.** The extra work is a few seconds of CPU. The recorded experiment 2 used 2011 s of the 2700 s `EDIT_BUDGET`, so there is headroom. I did not measure the replay.

### 2. Position rule fidelity: exact

- **Selector.** `read_replay.py:42-85` (`SELECTOR_CODE`) builds the seven word spans from `rq["prompt"].split("{}")`. They are The, capital, of (before the subject) and is, the, city, of (after it), shifted by the template's literal prefix length and the subject length. Each is matched to exactly one token by whitespace-stripped offset equality (`:56-68`). It requires seven distinct candidates and `m` in 1..7 (`:69-73`).
- **Cyclic rule.** `:74` is `candidates[(fact_i + template_i + j) % 7]`. This equals the frozen `start = (f+q)%7`, `C[(start+j)%7]`.
- **Arguments.** `fact_i` is the index into `requests`, which is fact order. `template_i` is the index into the flattened `ctx` (`read_replay.py:96-98`), so the six-template order matches the frozen anchor. `m = len(tgt)` from `tok(target, add_special_tokens=False)` (`:97`). The rule is applied to all three arms because it is the same function, and there is no fallback; every shortfall raises.
- **No tokenizer skew inside the run.** `:47-49` re-tokenizes the prefix and requires `input_ids == ids`, where `ids` is the exact list the model receives (`:99, :102`). Selection and model use the same tokenizer object and the same IDs.
- **Independent check.** I exec'd the driver's own `SELECTOR_CODE` over all 432 pairs (three arms, 24 facts, six templates), using the Rust tokenizer from `tokenizer.json`. I checked in a different way from the selector: `decode([id]).strip() == word` for each of the seven candidates, candidates ascending and distinct, indices equal to the frozen cyclic formula, and `m` equal to the registered `ntok`. All passed (`OK pairs 432`).
- **Not tested.**
  - HF `PreTrainedTokenizerFast` versus the Rust `Tokenizer`: UNVERIFIABLE here (loading it risks importing torch). The reader compares the HF-recorded IDs and offsets with the Rust re-encode (`read_replay.py:383-385`). A mismatch would invalidate a finished 50-minute run (issue 7).
  - `return_offsets_mapping=True` needs a fast tokenizer: UNVERIFIABLE (not tested).
- **A property of the rule, not a bug (issue 6).** For `q = 0` the template is `"{}"`, so `C[0]` ("The") is absolute token position 0, the attention-sink position. My run found control sets that include position 0 in 4 of 24 A1 pairs, 7 of 24 A2 pairs and 18 of 24 A7 pairs. All of these are `q = 0` pairs. The real value tokens can never sit at position 0.

### 3. Gates

The process-exclusion check is the problem. The other gates passed my read.

**Process check against the real macOS `ps`:**

- **Parsing works.** `ps -Aww -o pid=,ppid=,lstart=,command=` yields rows that split into 8 fields. `lstart` is 5 tokens, for example `Wed Sep 23 12:46:33 2026`. There were no malformed rows among 558 on this machine (`read_replay.py:293-301`).
- **It refuses.** I called `process_check("probe", None, "/tmp/nonexistent", [])` on the live table. It returned `ok=False` with 11 foreign matches:
  - the powerline `server.py` (pid 723)
  - `harness-dashboard/serve.py` (731)
  - pixeltable `postgres`, matched through `/python3.11/` in its path (937)
  - the loop's `edit.py` (29439)
  - the loop editor's multiprocessing resource tracker (29938)
  - the browser-harness daemon (72909)
  - four MCP servers: pixeltable-developer (89019), blender-mcp (89028) and two arxiv-mcp-server instances (89091, 84594)
  - a Codex session whose command line ends in `-C .../worktrees/c10k-route-a ...` (56244), caught by the `c10[^\s/]*` alternative
- **It would never kill the wrong process.**
  - `stop_owned` signals only `os.killpg(child.pid)`, after checking each recorded PID's `getpgid` equals `child.pid` (`run_replay.sh:64-97`).
  - The editor is started with `start_new_session=True` (`:143`), so that group is the runner's own.
  - Refusal is the only action taken against foreign processes.
- **It kills the run it launched (issue 1).** This is the defect.
  - The live loop's editor, pid 29439, has a child, pid 29938, whose command is `<sandbox>/.venv/bin/python -B -c from multiprocessing.resource_tracker import main;main(4)`. It started 4 seconds after the editor.
  - `MODEL_PROCESS` matches that string (checked). `process_check` exempts only a `prepare.py --score <run>` scorer and the fingerprint helper (`read_replay.py:313-329`), so the tracker lands in `foreign`.
  - `exclude("during_run")` fails (`run_replay.sh:151, :60`), `stop_owned()` kills the editor group (`:165`), and the run aborts within seconds. The scorer process will probably spawn its own tracker too.
  - The impl mock test `unowned_descendant_Python PASS ok=False` (impl report line 1997) encodes this as intended behavior. The mocks never included a tracker, and the real `ps` was denied to the implementer (report line 65).

**Spurious fail or pass elsewhere:**

- **The one-shot clone is burned early (issue 3).** `run_replay.sh:30-35` creates `replay_launch.json` before any gate. After any pre-dispatch refusal the clone is consumed ("destination was already invoked"), so the operator must re-run setup.
- **Fragility (issue 4).**
  - A single empty-command or malformed `ps` row raises (`read_replay.py:298`).
  - Any foreign hit during the run kills it.
  - `after_preflight` (`run_replay.sh:131-135`) can catch the preflight's resource tracker while it is still dying. That is plausible but UNVERIFIABLE whether `import torch; is_available()` spawns one.
- **Pass on an invalid run.** Polling is every 1 s, so a short foreign GPU job can slip through (the implementer acknowledged this, report line 44). With the narrower pattern I recommend, GPU users that are not named python (llama.cpp servers, LM Studio) would also slip. Add them to the pattern.
- **No spurious failure found elsewhere.**
  - `validate_score` accepted five real recorded scores (positive control on real data). Results: 131156 H7/C0/O7/D88.974; 134836 H7/C0/O7/D90.678; 142644 H18/C13/O5/D131.421, guards ok; 151845 H26/C15/O11/D147.666, guards `failed:described_as`; 160157 H29/C15/O14/D147.553.
  - Fingerprint, template-hash and fidelity file lists check out. All six fidelity packages are present in `.venv` and `transformers` is 4.51.0, so an uncaught `PackageNotFoundError` is moot.
  - Every file in `fidelity_inputs` exists on disk: snapshot files, shards, index, nine covariance files, configs and `reference_controls.json`.
  - The scorer's command line `PYTHON <dest>/prepare.py --score <run_dir>` (`prepare.py:222`) matches the prefix and name pattern at `read_replay.py:319-323`.

### 4. Labels: exact

- `primary_label` (`read_replay.py:337-339`): H ≤ 7 is NO-GAIN-WITHOUT-VALUE-POSITIONS, 8..17 is PARTIAL-GAIN, ≥ 18 is FULL-GAIN-WITHOUT-VALUE-POSITIONS. This matches prereg §4.
- `secondary_label` (`:342-344`): C = 0 is NO-COLLISION-RECOVERY, 1..12 is PARTIAL-COLLISION-RECOVERY, ≥ 13 is FULL-COLLISION-RECOVERY. This matches.
- Guards (`:602`) are identical to `prepare.py:42-52`. `quality` is DEGRADED when any guard fails (`:612`). A1/A2 below 68 also fail the metadata gate (`:557`), so that case is INVALID, which is consistent with prereg §3.
- `LABEL ...` is printed only in the `else` branch when `failures` is empty (`:620-623`).
- **Deviation.** On any validity failure the reader still prints `NON-BINDING count-only labels: primary=... secondary=...` with the full label strings (`:618-619`). Prereg §3 says INVALID means "no label". A grep for `primary=` finds both lines (issue 5).
- The reader does not print the §4 reading rows (for example "H ≤ 7 with D < 131.421 means no mechanism label"). It prints D and the differences, so the operator applies the reading by hand. That is acceptable.

### 5. Proportion

The reader is 650 lines. The structure is justified except for the items in "Things to cut".

## Numbered issues, priority order

1. **Resource-tracker child killed as foreign (certain; aborts the run).**
   - Where: `read_replay.py:313-329` (exemption by command match), `run_replay.sh:151` and `:60` (check and require), `:162-165` (kill).
   - Failure: the editor's `multiprocessing.resource_tracker` child matches `MODEL_PROCESS` and is not exempt, so the runner kills its own editor seconds after launch. Observed live: pid 29938 under editor 29439.
   - Fix: build `descendants` as the transitive closure of `ppid` from `child_pid`. Alternatively, add `pgid` to the ps columns (`-o pid=,ppid=,pgid=,...`) and treat `pgid == child.pid` as owned. Remove the `prefix`, `run_path` regex and `helper_argv` special cases. Keep the identity pin (`start` and `command`) only for the recorded editor PID. Add a unit test where a tracker child of the editor and a scorer child both appear.

2. **`MODEL_PROCESS` flags any Python or `c10*` token, so the gate cannot pass on this machine.**
   - Where: `read_replay.py:288`.
   - Failure: 11 foreign matches today (listed above). It also flags any process whose command line ends in `...c10k-route-a`, such as the Codex session.
   - Fix: match GPU contenders only.
     - Script names anchored to `.py`: `(edit|prepare|check_equivalence)\.py` and `c10[a-z0-9_]*\.py`.
     - Python executables located under `PROGRAM_ROOT/.venv`, the sandbox, fence or replay `.venv` directories.
     - Names `ollama`, `llama`, `ipykernel`, `jupyter` and `safe-mode`.
   - Do not match bare `python`.
   - Print the operator a one-line list of what must be closed before the window (the loop and Ollama).

3. **A pre-dispatch refusal consumes the one-shot clone.**
   - Where: `run_replay.sh:33-35` (`launch_path.open("x")` runs before all gates), `:166-203` (`finally` writes `runner_receipt.json`, `run.rc` and `run.log` even when nothing launched).
   - Failure: every refusal in issue 2's class forces a new setup.
   - Fix: reserve the invocation (create `replay_launch.json`) only after `after_preflight` passes, immediately before `Popen`. Pre-dispatch failures should print, exit 2 and write nothing to `dest`.

4. **Transient probe errors and short-lived processes can kill a 50-minute run.**
   - Where: `read_replay.py:298` (empty-command row raises), `run_replay.sh:151` (one foreign hit kills), `:131-135` (preflight tracker race, UNVERIFIABLE).
   - Fix: skip rows with an empty command. On a foreign hit, re-probe once after about 1 s and fail only if the same PID is still foreign. For `during_run`, consider recording the event and letting the reader mark INVALID instead of killing, because concurrent foreign work cannot change the weights.

5. **Label strings printed on INVALID.**
   - Where: `read_replay.py:618-619`.
   - Failure: contradicts prereg §3 ("INVALID, HALT, exit 2, no label"), and a grep for `primary=` finds a label on an invalid run.
   - Fix: print `NON-BINDING counts: H=.. C=.. O=.. D=..` with no label names, or delete the line.

6. **The control includes the attention-sink position, so "ordinary common words" may not hold. This is an interpretation caveat, not a driver defect.**
   - Where: frozen rule `redesign_v1.md:96-117`, `read_replay.py:74`.
   - Evidence: from my selector run, `q = 0` control sets include token position 0 in 4 of 24 (A1), 7 of 24 (A2) and 18 of 24 (A7) pairs. Whether position 0 has an outlier key norm at layers 4–8 is UNVERIFIABLE without the model.
   - Failure: if it does, `Kp Kp.T` is dominated by about 18 columns, and "H ≤ 7, D ≥ 131.421 means H-location survives" could instead mean "a sink-dominated constraint".
   - Fix without touching `edit.py`:
     - The reader prints `control_sumsq / value_sumsq` and `control_PKp_fro / value_PKp_fro` per layer (the data is already in the layer records, `read_replay.py:149-150`).
     - Add one pre-registered sentence to prereg §4: if either ratio is more than 10 at any layer, report "control not norm-comparable" beside the label.
     - Re-freeze the prereg text only.

7. **HF-versus-Rust tokenizer equality is unverified before the GPU window.**
   - Where: `read_replay.py:383-385` against selector `:47-49`.
   - Failure: a mismatch, or a slow tokenizer where `return_offsets_mapping` is unsupported, would waste the run (the second case would fail within minutes; the first would only show after about 50 minutes).
   - Fix: a no-model, no-GPU check by the operator before the window. Load `AutoTokenizer.from_pretrained(snapshot)` in a separate process and compare `input_ids` and `offset_mapping` for the 432 prefixes with the Rust tokenizer.

## Things to cut before the run

- The command-name classification in `process_check` (`:313-329`, `shlex`, `helper_argv`, `run_path` regex). Issue 1 replaces it.
- The `NON-BINDING` label line (issue 5).
- The self-test scaffolding in the live paths: `REPLAY_READER_SELFTEST` and `synthetic_fixture` (`read_replay.py:490-495, :621-622`; `run_replay.sh:108`). Move it to a test file.
- The duplicated fingerprint validation in runner (`run_replay.sh:124-127`) and reader (`read_replay.py:517-527`). Keep one.
- Optional, only if edit.py is ever re-frozen: the same-capture identity check and its literal `identity_equal: True` (`read_replay.py:105-108, :147`).
- Do not cut `validate_positions` (`read_replay.py:367-422`): it is the independent re-derivation of the position rule, and it is what protects the result.
- Do not cut the before-and-after fidelity hashes. They cost wall time but not GPU time and do not risk the run.

## Note on reviewer independence

I found the central defect by running the code against the real process table, which the implementer could not do. The implementer's own review was a fresh Codex fallback (impl report line 63), not an independent Claude pass.
