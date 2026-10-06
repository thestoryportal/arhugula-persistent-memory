# autoresearch-edit

The idea: give an AI agent a small but real model-editing setup and let it experiment autonomously overnight. It modifies the edit recipe, writes a set of facts into a language model's weights, checks whether the model now recalls them in words it was never shown, keeps or discards, and repeats. You wake up in the morning to a log of experiments and (hopefully) a better recipe. This is Karpathy's [autoresearch](https://github.com/karpathy/autoresearch), run through the [macOS fork](https://github.com/miolini/autoresearch-macos), with the training run replaced by an edit run. As there, you are not touching the Python files like you normally would as a researcher. You program `program.md`, the Markdown file that gives the agent its context.

The experiment: 24 fictional countries get a fictional capital each, written into Qwen2.5-3B (fp16, Apple MPS) by editing the MLP weights directly, with no training. The capitals are two coined words. The edit is given one prompt per fact, "The capital of {} is the city of". The model is then asked through three other phrasings it never saw, and a read counts only if it greedily produces the whole two-word value. That is 72 held-out reads.

## How it works

The repo is deliberately kept small and only really has three files that matter:

- **`prepare.py`** — fixed constants, setup checks (engine fingerprint, harness hash, an engine-parity gate), runtime utilities (the loaded model and tokenizer, the engine's solver functions, the facts to write), and the evaluation, which runs as a separate process on the weights the edit changed. Not modified.
- **`edit.py`** — the single file the agent edits. Contains the full edit recipe: hyperparameters, the projector, and `apply_edit`, which writes the facts into the weights. Everything is fair game. **This file is edited and iterated on by the agent**.
- **`program.md`** — baseline instructions for one agent. Point your agent here and let it go. **This file is edited and iterated on by the human**.

`prepare.py` wraps a fixed harness, `c10e_bandknob.py` (linked in, read-only), which loads the model and holds the stimuli and the metric's building blocks. The edit engine underneath is a vendored MEMIT implementation whose source hash is checked before every run.

By design, the edit recipe gets a **fixed budget of 45 minutes of wall clock** for everything it does, regardless of what that is. The metric is **heldout_full** (held-out full-value reads out of 72) — higher is better — and a run counts only if every **guard** holds:

- **Controls `A1` and `A2`.** The same recipe is applied, from the unedited model, to 24 easy facts with one-token and two-token real capitals, and each must stay at 68/72 or above. A recipe that only works for the coined values is not a recipe.
- **Locality.** These measure what else the edit changed. `L1_flips` counts real countries whose answer became an edited value. `frame_flips` counts unedited fictional countries in the same prompt that now emit one. `described_as` is how much of the edited subjects' "<subject> is described as" distribution survives. `L3` counts unrelated real countries whose answer is unchanged. `ppl_post` is perplexity on generic sentences.
- **`law5_ok`.** This engine-parity gate confirms the harness's own edit function still matches the engine.
- **`scope_ok`.** Every changed tensor is an MLP weight.

`dw_total`, the total size of the weight change, is reported as a soft constraint, like the fork's peak VRAM.

## Quick start

**Requirements:** Apple Silicon Mac with MPS, the program checkout at `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a` (engine, model cache, covariance caches, stimulus screens), and its virtual environment. No downloads, no `uv`: `.venv` is a link to that checkout's environment, which is shared and must not be re-synced.

```bash
# 1. Check the setup (~5 min: loads the model, runs the gates)
.venv/bin/python prepare.py

# 2. Manually run a single edit experiment (~30-80 min)
.venv/bin/python edit.py
```

If the above commands all work ok, your setup is working and you can go into autonomous research mode.

## Running the agent

Run `./launch.sh` from this directory. It starts Claude Code here with permissions set for unattended work, and with no outside context: no global or project instructions, skills, plugins, hooks or MCP servers. Then prompt:

```
Hi have a look at program.md and let's kick off a new experiment! let's do the setup first.
```

The `program.md` file is essentially a super lightweight "skill".

## Project structure

```
prepare.py        — constants, setup checks, runtime utilities, evaluation (do not modify)
edit.py           — the edit recipe (agent modifies this)
program.md        — agent instructions
c10e_bandknob.py  — fixed harness, linked read-only
pyproject.toml    — dependencies
.venv             — link to the shared environment
```

## Design choices

- **Single file to modify.** The agent only touches `edit.py`. This keeps the scope manageable and diffs reviewable. The metric, guards and stimuli sit in `prepare.py`, and the scoring runs in a separate process that never executes `edit.py`'s code; it sees only the weights the edit changed.
- **Fixed edit budget.** The recipe gets at most 45 minutes of wall clock for all its own work, top-level setup and three edits together (model loading and evaluation excluded), so a run takes roughly 30–80 minutes. This makes experiments directly comparable whatever the recipe does, and the search finds the best recipe for this machine within that budget. A run over budget is a crash. The seed is fixed too, so the engine's sampled context templates are the same in every run.
- **Self-contained.** No external dependencies beyond the program's environment. One GPU, one file, one metric, plus guards that stop a win that damages the model from counting.

## Platform support

Apple Silicon only (MPS, fp16). MPS has no float64, so keep tensor math on the GPU in float32 or lower, and do float64 on the CPU if you need it. Memory is 48 GB unified. The model takes about 6 GB; `prepare.py` keeps a copy of the unedited weights to restore between arms, and the scorer process holds a second model while it measures.

## License

The autoresearch structure is MIT (Karpathy; miolini's macOS fork).
