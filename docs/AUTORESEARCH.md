# Autoresearch in this program — how we use it now (single source of truth)

**Decision IDs:** operator ruling D-C10r-rulings-1 (2026-10-06): follow Karpathy's `autoresearch` exactly, as the macOS fork directs. Implementation decision D-C10r-impl-1 (2026-10-06) is this document. Every other mention of autoresearch in the repo should carry a pointer here, not a restated copy.

We run Karpathy's autoresearch loop, through the macOS fork (`external_prior_art/autoresearch-macos/`, read in full 2026-10-06), on the C10 edit harness. One Claude Code agent edits a single recipe file, writes 24 coined two-word capitals into Qwen2.5-3B, reads the held-out score, keeps or discards, and repeats until a human stops it. Whatever it keeps is a candidate. Candidates enter the program only through a separately pre-registered falsifier.

## How to run it

First run the equivalence check once (about an hour; see "The fence" below). Then run the launcher from your own terminal. It refuses to start if an experiment or Ollama is running, or if `results/autoresearch_c10_equivalence.json` is missing, failed, or recorded for a different `prepare.py`, `edit.py` or harness than the current ones.

```bash
PY=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python
$PY /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/check_equivalence.py
```

```bash
bash /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/launch.sh
```

The launcher builds the sandbox at `/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10` (its own git repository on branch `autoresearch/master`, outside the program checkout and sharing no history with it) and copies in the reviewed source from `experiments/track_c/autoresearch_c10/`. It commits that as the base and opens Claude Code there with the fork's kickoff line. The agent proposes a run tag, creates `autoresearch/<tag>`, checks the setup and asks you to confirm. After you confirm, it loops with no cap and never asks again.

- **Watch it** in its tmux session (`tmux attach -t autoresearch`), or read `results.tsv` and the git log in the sandbox directory.
- **Stop it** by interrupting the session. If a run is mid-flight, kill it with `pkill -f edit.py`.
- **Collect the results** from the sandbox directory. `results.tsv`, `runs/*/score.json` and the `autoresearch/<tag>` branch are the record. Fold a candidate in only through a pre-registered test.

The research source lives on the program branch under `experiments/track_c/autoresearch_c10/`. Edit it there, get it reviewed, and relaunch. Never edit the sandbox copy by hand.

## The fork's files, mapped to an editing experiment

The fork is built for training. Its agent edits `train.py`, which trains a small GPT for exactly 5 minutes, and `prepare.py` holds the data, the tokenizer and the fixed metric `evaluate_bpb`. We kept the structure and replaced the training run with an edit run.

| Fork | Ours | What changed and why |
|---|---|---|
| `prepare.py`: constants, one-time data prep, dataloader, `evaluate_bpb` (do not change) | `prepare.py`: constants (seed, edit budget, guards), setup checks (engine fingerprint, harness hash, reference run, engine-parity gate), runtime utilities (model, tokenizer, engine solver functions, the facts per arm), `evaluate(apply_edit)` (do not change) | The fork keeps the metric out of the agent's file, so we moved our metric and guards out of the editable unit too. In the earlier draft, `run_iteration.py` computed its own score. `evaluate` applies the agent's `apply_edit` to each arm and saves the changed weights. A separate scorer process (`prepare.py --score`) then loads the unedited model, applies those weights and replays the harness's per-arm measurement. It never runs the agent's code, so runtime monkey-patching, hooks and state cannot reach the score. |
| `train.py`: the single editable file (model, optimizer, loop; hyperparameters edited in place) | `edit.py`: the single editable file (hyperparameters edited in place, projector, `apply_edit`) | The baseline is the harness's own edit function: one batched MEMIT write through the AlphaEdit null-space projector, layers 4–8. `knobs.json` is gone, because the fork has one file and no config file. |
| `program.md`: the human's file | `program.md`: the fork's text, with editing's metric, guards, timing, output block and results columns | Kept verbatim wherever it still holds. One deviation is listed below. |
| `README.md` | `README.md`: the same shape | Describes the experiment and the guards. No corpus findings. |
| `CLAUDE.md` / `AGENTS.md`, git-ignored, "generated per-session by launchers" | none | Not needed. The two machine facts the agent cannot infer are fixed at the root instead: `.venv` is a link the launcher makes, so commands are `.venv/bin/python …`, and program.md tells the agent that a run outlasts the shell tool's 10-minute limit. On this Mac `grep` is aliased to ripgrep, where the fork's `grep "a\|b"` matches nothing, so program.md uses `grep -e a -e b`, which both tools read the same way. |
| `pyproject.toml` | `pyproject.toml` | Lists what is installed in the shared environment. No `uv sync`, because the environment belongs to the program checkout. |

The fixed harness `experiments/track_c/c10e_bandknob.py` is copied into the sandbox read-only. `prepare.py` refuses to run if the program's copy changes its SHA-256.

**Why a copy, and why program.md forbids reading outside the sandbox (2026-10-06, first launch, run tag `oct6`).** The harness was a symbolic link at first. Ten minutes into its baseline the agent followed the link's target, listed the program's `experiments/track_c/`, and sent a helper agent to summarize the earlier C10 experiments and their result files. That breaks the sandboxed-context ruling (D-C10r-rulings-1: the agent forms every idea from its in-scope files and its results table), so the program session stopped the run before the baseline finished, killed the helper before it reported, and relaunched. Three changes, after a Codex GPT-6-Astra review of the first two (`results/autoresearch_c10_advisor_sandbox_fix.md`, FIX-FIRST): the launcher copies the harness instead of linking it and checks the copy's hash against the equivalence result on every launch; the sandbox is a standalone repository outside the program checkout, because the reviewer showed that the earlier worktree shared the program's object database (`git show worktree-c10k-route-a:docs/AUTORESEARCH.md` succeeded from inside it); and `program.md` says in words that everything outside the sandbox directory is off limits as a source of information to the agent and to any helper it starts, the program checkout named in `prepare.py` included, while the runtime dependencies there (engine, model, caches) stay usable by its runs. Context isolation is a binding condition of the ruling in its own right, separate from the scorer's independence. With permissions disabled, the written rule is honored, not enforced; the launch settings described under "Context isolation and permissions" are the enforced part, and their reach is recorded there.

The model substitution: the operator's relaunch order (2026-10-06, 10:10) read "run the auto research with Fable 5.5 high". The dashboard's harness listing of the installed Claude Code offered one Fable model, `claude-fable-5-1` ("Fable 5.1"), beside Opus 5.5, Sonnet 5.5 and Haiku 4.5, so the author launched `claude-fable-5-1 --effort high` and told the operator the substitution in the same report.

## The three design choices

- **Single file to modify.** The agent edits only `edit.py`. The stimuli, the metric and the guards sit in `prepare.py`, and scoring runs in a separate process that sees only the changed weights. `prepare.py` also refuses an `edit.py` that names the evaluation data or quotes the held-out prompts. It refuses weights changed outside `apply_edit`, and it fails any run that changes a non-MLP tensor (the `scope_ok` guard).
- **Fixed time budget becomes a fixed edit budget.** The recipe gets at most 45 minutes of wall clock for all its own work (`EDIT_BUDGET = 2700`): `edit.py`'s top-level setup plus the three edits. Model loading and evaluation are excluded, and a run over budget is a crash. Counting the setup closes the route of precomputing outside the budget. A run takes roughly 30–80 minutes, so a night yields about eight to ten experiments. As in the fork, this makes experiments comparable and finds the best recipe for this machine within the budget. The seed is fixed (`SEED = 0`), so the engine's sampled context templates are identical across runs. Without that, process-to-process spread would be mistaken for improvement.
- **Self-contained.** One GPU, one file, one metric. Guards stop a win that damages the model from counting: the two control arms at 68/72 or above, plus the locality axes, perplexity and the engine-parity gate. `dw_total` is a soft constraint, like the fork's VRAM.

## Context isolation and permissions

The fork's README says to "spin up your Claude/Codex or whatever you want in this repo (and disable all permissions)". We follow both halves.

- **Context.** `claude --safe-mode` disables CLAUDE.md discovery, skills, plugins, hooks, MCP servers and custom agents. The agent therefore sees only what it reads in the sandbox. That is the operator's sandboxed-context ruling, with no CORPUS, docs, runbook or memory. We did not use `--bare`, because it accepts only an API key and never reads the subscription login.
- **Permissions.** The launcher passes `--dangerously-skip-permissions`, as the fork directs, so the loop never stops on a prompt. The less permissive alternative is `--permission-mode dontAsk` with an allow-list. It also never blocks, but it silently denies anything unlisted, so a missed command would stall the loop.
- **The fence (2026-10-06, after the first launch's breach).** `experiments/track_c/autoresearch_c10/sandbox_settings.py` writes a settings file the launcher passes with `--settings`: Claude Code's Bash filesystem sandbox (which covers every process a shell command starts) denies reads and writes under the program checkout, the main repository, the Connected Papers collection, the genesis artifacts and the backup, and allows reads only where a run needs them (the shared `.venv` and its uv interpreter, the engine, the model cache, the covariance caches, the hyperparameter files, the harness, the fingerprint tool, the reference run); `permissions.deny` rules of the form `Read(//abs/path/**)` close the Read tool, which the Bash sandbox does not cover; and `"allowUnsandboxedCommands": false` puts the sandbox in strict mode, so the agent's "retry this command unsandboxed" option is ignored (the second launch showed why: when the fence lacked `configs/screens`, the agent correctly diagnosed the missing path and simply re-ran the setup check outside the sandbox). **The model runs need a second layer.** Claude Code's sandbox profile denies every `sysctl` read, and PyTorch's MPS backend queries the OS version through one; inside that sandbox it concludes the Mac predates macOS 13 and falls back to the CPU without a word (the third launch's setup check ran 30 minutes on the CPU; probes 6–8). No setting opens `sysctl`, so the three wrappers `setup.sh`, `run.sh` and `kill_run.sh` are listed in `excludedCommands` and run outside Claude Code's sandbox — inside a macOS Seatbelt profile the same script writes (`sandbox_settings.py … --seatbelt` → `.sandbox.sb`): default allow (so `sysctl`, Metal and the network work), the same read denials, re-opened only for the runtime set, writes only where a run writes; the scorer and fingerprint subprocesses inherit it. Probes 9–10: a wrapper called in a compound form (`./run.sh; …`) stays inside Claude Code's sandbox and fails with `sandbox_apply: Operation not permitted`; called bare it runs under the profile with the GPU on and the program files still unreadable. Hence program.md's rule that the wrappers are launched as bare commands through the shell tool's background option. Verified in disposable `claude -p` sessions with the exact launch flags (`results/autoresearch_c10_sandbox_probe.md`): `cat`, a Python `open()`, `ls` of `experiments/track_c/`, `git log` and `git show master:README.md` against the program checkout, the Read tool on `EXPERIMENT_RUNBOOK.md`, and a `touch` into the checkout all fail with "Operation not permitted" or "denied by your permission settings"; the positive controls (the sandbox's own files, the reference run, the covariance caches, the hyperparameter files, a write into the sandbox, an HTTPS request) succeed. Two things the probes could not test: `--safe-mode` sessions started with `-p` have no Glob, Grep or Agent tool, so the deny on helper agents is untested (the first launch's interactive session did have one); and a denied path pattern that is wrong fails silently, so a changed path layout needs a new probe. The equivalence check is unaffected: prepare.py, edit.py and the harness are byte-identical.
- **Model.** Fable 5.1 (`--model claude-fable-5-1`) at high effort (`--effort high`) — operator choice at the 2026-10-06 relaunch, replacing Opus 5.5 at extra-high effort from D-C10r-rulings-1.
- **Git hooks** of the program repository are switched off for the session, because they guard the research branch, not the sandbox.

## The fence

The loop is an optimizer. Its output is a candidate, never evidence (DISCIPLINE §3). It never writes `CORPUS/`, the runbook, the checkpoint, the ledgers, the hypothesis register or memory. The program session does not steer its ideas: the program routes no idea to the loop. This supersedes the earlier routing of the "capped iterated variant" to the loop (CORPUS/50 "What this changes"; the 2026-10-06 close-out text). That variant stays an OPEN register entry for a possible pre-registered arm.

The program session's jobs are to:
1. before the first launch, run `experiments/track_c/autoresearch_c10/check_equivalence.py` (operator-approved, about an hour). It must report PASS. That requires four things: edit.py's baseline changes the same weights as the harness's edit, bit for bit; the separate scorer reproduces the harness's `run_recipe` numbers exactly; the seed reproduces the context templates across processes; and the saved tensors' hashes are recorded. If it fails, the loop would be optimizing a wrapper, not C10. Investigate under the halt discipline (one fix after a read, then halt) and do not launch;
2. check the loop's first (baseline) run against the known single-edit envelope, outside the sandbox (LAW#3); and
3. read the sandbox's `results.tsv` and git log (the fork's own record; SUMMARY.md was dropped 2026-10-06 because it served the human, not the science) and fold any candidate in through a pre-registered falsifier with controls, re-verified across seeds, because the loop's seed is fixed.

## Deliberate deviations from the fork

- **Broken-instrument stop.** If `prepare.py`'s checks fail, or the baseline itself fails a guard, the agent writes `HALT.md` and stops. The fork never stops. This program's LAW#1 says an engine fingerprint failure is a halt, and a loop that keeps crashing on a broken instrument produces nothing.
- **Interpreter.** `$PY` is the shared virtual environment, not `uv run`.
- **`results.tsv` is untracked**, as Karpathy's upstream `program.md` requires. The macOS fork dropped that line.
- **Papers.** `edit.py` cites the methods its baseline implements (ROME arXiv:2202.05262, MEMIT arXiv:2210.07229, AlphaEdit arXiv:2410.02355), as the fork's `train.py` names nanochat and its techniques, so the fork's "read papers referenced in the code" has something to point at. The agent can read them with Claude Code's built-in web tools.

## Retired (2026-10-06, D-C10r-impl-1)

These are retired. Each folder carries a RETIRED.md and a banner at the top of its agent-facing files. The session that made this change was not permitted to delete them, so deleting them is the operator's step: `git rm -r experiments/track_c/autoresearch_reaim experiments/track_c/autoresearch_band_search`. Git history keeps them.

- `tools/autoresearch-skill/`: the wjgoarxiv loop. It was never present in this checkout, though several docs named it as the runner.
- `experiments/track_c/autoresearch_band_search/`: a June config search for that runner, with a 12-iteration cap. It was never run.
- `experiments/track_c/autoresearch_reaim/`: the first adaptation. It had two editable files (`run_iteration.py` + `knobs.json`), a script that scored itself, snapshots instead of git, and corpus findings in its program. Its last unmarked state is commit `dffd570`. Its killed baseline's partial output, `results/autoresearch_reaim/`, is untracked and can be deleted.

`docs/AUTORESEARCH_REAIM_OVERNIGHT_PLAN.md` stays as a dated record with a superseded banner. The autonomy driver (`tools/autonomy_driver.py`, AUTONOMY.md) is a separate regime and does not launch autoresearch.

## Operational notes

- **Ollama.** It shares the GPU, and the launcher refuses to start while it runs. Your winning-defense graphify refresh, a launchd job every 20 minutes, embeds through Ollama and fails while Ollama is stopped. Restart Ollama with `brew services start ollama` when the loop is not running.
- **Durations.** A harness pass with three arms took about 34 minutes on 2026-10-06, measured from the c10q run log.
