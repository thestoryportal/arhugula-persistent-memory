# autoresearch

This is an experiment to have the LLM do its own research.

## Setup

To set up a new experiment, work with the user to:

1. **Agree on a run tag**: propose a tag based on today's date (e.g. `oct6`). The branch `autoresearch/<tag>` must not already exist — this is a fresh run.
2. **Create the branch**: `git checkout -b autoresearch/<tag>` from current `autoresearch/master`.
3. **Read the in-scope files**: The repo is small. Read these files for full context:
   - `README.md` — repository context.
   - `prepare.py` — fixed constants, setup checks, runtime utilities, evaluation. Do not modify.
   - `edit.py` — the file you modify. The edit recipe: how the facts are written into the model's weights.
   - `c10e_bandknob.py` — the fixed harness that `prepare.py` wraps (model loading, stimuli, the metric's building blocks). Read-only; read it when you need to know what a utility does.
4. **Verify the setup**: run `/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_c10/setup.sh` (it runs `prepare.py` and writes `prepare.log`; it takes a few minutes: it loads the model) and check that the last line of `prepare.log` is `Done! Ready to edit.` If not, tell the human what it printed.
5. **Initialize results.tsv**: Create `results.tsv` with just the header row. The baseline will be recorded after the first run.
6. **Confirm and go**: Confirm setup looks good.

Once you get confirmation, kick off the experimentation.

## Experimentation

Each experiment runs on a single GPU (Apple MPS). The edit recipe gets a **fixed budget of 45 minutes of wall clock** (`EDIT_BUDGET` in `prepare.py`): everything `edit.py` does, its top-level setup included, plus its three edits (one per arm, each on the unedited model). Model loading and the evaluation are not counted. The evaluation runs afterwards in a separate process that loads the unedited model, applies the weights your edits changed, and measures. A whole run takes roughly 30–80 minutes, longer than your shell tool's 10-minute command limit, so start each run in the background and check `run.log` until the summary appears. You launch it simply as: `/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_c10/run.sh`. **Launch it as exactly that bare command, through your shell tool's background option** — not with `&`, not `cd … && …`, not with `;`, a pipe or a redirect around it. Only the bare call runs with the GPU; any other form stays inside your shell sandbox and fails at once (exit 71, a message in `run.log`). The same holds for `/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_c10/setup.sh` and `/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_c10/kill_run.sh`. These three scripts and their sandbox profile live in a directory you cannot change; `run.log`, `prepare.log` and `preflight.log` appear in this directory.

**What you CAN do:**
- Modify `edit.py` — this is the only file you edit. Everything is fair game: the hyperparameters, the layers written, the target-vector solve, the least-squares solve, the projector, the requests, the structure of `apply_edit`.

**What you CANNOT do:**
- Modify `prepare.py` or `c10e_bandknob.py`. They are read-only. They contain the fixed evaluation, the stimuli, the guards and the constants (edit budget, seed).
- Change weights outside the MLP layers. The feed-forward layers are the store being tested; a change to any other tensor fails the `scope_ok` guard.
- Change weights outside `apply_edit`. `prepare.py` refuses to run if the weights differ from the unedited model when `evaluate` starts.
- Use the evaluation data in `edit.py`: the held-out paraphrase templates, the locality prompts and countries, the generic sentences, the frame subjects, or any of the metric's functions. Editing with the test prompts is testing on the training set. `prepare.py` refuses to run an `edit.py` that names them.
- Install new packages or add dependencies. You can only use what's already in `pyproject.toml`.
- Write outside this directory.
- Read, list or search anything outside this directory for information, yourself or through a helper agent. Your sources are this directory (the in-scope files, `results.tsv`, `run.log`) and the papers `edit.py` cites, which you may fetch and read. `prepare.py` names a program checkout (`PROGRAM_ROOT`) for the engine, the model and the covariance caches, and `.venv` links into it; those are runtime dependencies that your runs load, and that is the only use you make of them. That checkout belongs to another research program with its own history of experiments and findings, and that history is off limits — no reading its files, no helper sent to summarize it. The human runs this loop to learn what *you* find from the in-scope files and your own results; a run that has seen that history is invalid for this context-restricted experiment.

**The goal is simple: get the highest heldout_full** — how many of the 72 held-out reads (24 subjects × 3 paraphrase prompts the edit never saw) produce the full two-word value. Since the edit budget is fixed, you don't need to worry about edit time — it's always within 45 minutes. Everything is fair game in `edit.py`. The only constraints are that the code runs without crashing, finishes within the budget, and **every guard holds** (`guards: ok`): the controls `A1` and `A2` (the same recipe applied to easy one- and two-token values) stay ≥ 68/72, and the rest of the model is left alone (`L1_flips`, `frame_flips`, `described_as`, `L3`, `ppl_post`; thresholds in `prepare.py`). A run with a failed guard is not kept, however high its heldout_full.

**dw_total** (the total size of the weight change) is a soft constraint. Some increase is acceptable for meaningful heldout_full gains, but it should not blow up dramatically.

**Simplicity criterion**: All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Conversely, removing something and getting equal or better results is a great outcome — that's a simplification win. When evaluating whether to keep a change, weigh the complexity cost against the improvement magnitude. A +1 heldout_full that adds 20 lines of hacky code? Probably not worth it. A +1 from deleting code? Definitely keep. An improvement of ~0 but much simpler code? Keep.

**The first run**: Your very first run should always be to establish the baseline, so you will run the edit script as is.

## Output format

Once the script finishes it prints a summary like this:

```
---
heldout_full:   <int, /72>
canon:          <int, /24>
first_token:    <int, /72>
A1:             <int, /72>
A2:             <int, /72>
L1_flips:       <int, /12>
frame_flips:    <int, /6>
described_as:   <float, %>
L3:             <int, /30>
ppl_post:       <float>
law5_ok:        true
scope_ok:       true
dw_total:       <float>
edit_seconds:   <float>
score_seconds:  <float>
guards:         ok
```

`guards` is `ok` or `failed:<names>`. You can extract the key metrics from the log file:

```
grep -e "^heldout_full:" -e "^dw_total:" -e "^guards:" run.log
```

## Logging results

When an experiment is done, log it to `results.tsv` (tab-separated, NOT comma-separated — commas break in descriptions). Do not commit `results.tsv`; leave it untracked by git.

The TSV has a header row and 5 columns:

```
commit	heldout_full	dw_total	status	description
```

1. git commit hash (short, 7 chars)
2. heldout_full achieved (an integer out of 72) — use 0 for crashes
3. dw_total, round to .1f — use 0.0 for crashes
4. status: `keep`, `discard`, or `crash`
5. short text description of what this experiment tried (append `[guards failed: <names>]` when a guard failed)

Example:

```
commit	heldout_full	dw_total	status	description
a1b2c3d	10	40.0	keep	baseline
b2c3d4e	14	47.5	keep	<what change B tried>
c3d4e5f	20	71.2	discard	<what change C tried> [guards failed: described_as]
d4e5f6g	0	0.0	crash	<what change D tried> (over edit budget)
```

## The experiment loop

The experiment runs on a dedicated branch (e.g. `autoresearch/oct6`).

LOOP FOREVER:

1. Look at the git state: the current branch/commit we're on
2. Tune `edit.py` with an experimental idea by directly hacking the code.
3. git commit
4. Run the experiment: `/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_c10/run.sh` as a bare command in the background (it runs `edit.py` and writes everything to `run.log`; do NOT run `edit.py` any other way, and do NOT use tee or let output flood your context)
5. Read out the results: `grep -e "^heldout_full:" -e "^dw_total:" -e "^guards:" run.log`
6. If the grep output is empty, the run crashed. Run `tail -n 50 run.log` to read the Python stack trace and attempt a fix. If you can't get things to work after more than a few attempts, give up.
7. Record the results in the tsv
8. If heldout_full improved (higher) and `guards: ok`, you "advance" the branch, keeping the git commit
9. If heldout_full is equal or worse, or a guard failed, you git reset back to where you started

The idea is that you are a completely autonomous researcher trying things out. If they work, keep. If they don't, discard. And you're advancing the branch so that you can iterate. If you feel like you're getting stuck in some way, you can rewind but you should probably do this very very sparingly (if ever).


**Timeout**: Each experiment should take ~30–80 minutes total. If a run exceeds 120 minutes, kill it with `/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_c10/kill_run.sh` (a plain `pkill` cannot see the run from your shell) and treat it as a failure (discard and revert).

**Crashes**: If a run crashes (over the edit budget, out of memory, a bug, etc.), use your judgment: If it's something dumb and easy to fix (e.g. a typo, a missing import), fix it and re-run. If the idea itself is fundamentally broken, just skip it, log "crash" as the status in the tsv, and move on.

**Broken instrument**: if `prepare.py`'s checks fail (engine fingerprint, harness hash, engine-parity gate), or the baseline itself fails a guard, the instrument is broken, not your idea. The same holds if `run.sh` or `setup.sh` reports an INFRASTRUCTURE HALT (the GPU unavailable inside the profile). Write `HALT.md` with what you saw and stop. This is the one case where stopping is right.

**NEVER STOP**: Once the experiment loop has begun (after the initial setup), do NOT pause to ask the human if you should continue. Do NOT ask "should I keep going?" or "is this a good stopping point?". The human might be asleep, or gone from a computer and expects you to continue working *indefinitely* until you are manually stopped. You are autonomous. If you run out of ideas, think harder — read papers referenced in the code, re-read the in-scope files for new angles, try combining previous near-misses, try more radical changes to the edit recipe. The loop runs until the human interrupts you, period.

As an example use case, a user might leave you running while they sleep. If each experiment takes you ~45 minutes then you can run approx 1–2/hour, for a total of about 10 over the duration of the average human sleep. The user then wakes up to experimental results, all completed by you while they slept!

**What your results are**: candidates. The human verifies anything you keep with a separately pre-registered test before believing it.
