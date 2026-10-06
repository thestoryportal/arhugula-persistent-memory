---
name: autoresearch-editing-loop-per-fork
description: "Autoresearch is Karpathy's loop run exactly as the macOS fork directs, adapted from training to editing (D-C10r-impl-1, 2026-10-06): fixed prepare.py owns the metric and guards, one editable edit.py, the fork's program.md, operator-launched in safe mode via experiments/track_c/autoresearch_c10/launch.sh; single source docs/AUTORESEARCH.md."
metadata:
  node_type: memory
  type: project
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
---

The fork is a training loop: the agent edits `train.py`, and `prepare.py` holds the fixed metric. For C10 the four agent-facing files were adapted. `prepare.py` stays fixed and holds the seed, a 900 s per-arm edit budget, the setup gates and `evaluate(apply_edit)`, which owns the metric and guards. `edit.py` is the only editable file, and its baseline is the harness's edit. `program.md` is the fork's text with editing's specifics. `README.md` keeps the fork's shape and carries no corpus findings. The operator runs `experiments/track_c/autoresearch_c10/launch.sh`, which builds the sandbox worktree on `autoresearch/master` and starts `claude --safe-mode --model claude-opus-5-5 --effort xhigh --dangerously-skip-permissions` with the fork's kickoff line.

**Why:** the operator wants the fork followed exactly, with no cap, no seeded ideas and a sandboxed context (D-C10r-rulings-1). The first draft broke the fork's key property, because its editable unit computed its own score. `--bare` was rejected because it never reads the subscription login.

**How to apply:** don't route ideas to the loop. "Candidate knob for the loop" wording conflicts with no-seeded-ideas. Don't give the loop agent corpus context. Edit the source on the program branch, never the sandbox copy. Check the loop's baseline against LAW#3 outside the sandbox. Fold a kept recipe in only through a pre-registered falsifier re-verified across seeds. Details and deviations: `docs/AUTORESEARCH.md`. See [[autoresearch-is-not-a-faithfulness-gate]], [[c10-stacked-solve-tradeoff]].
