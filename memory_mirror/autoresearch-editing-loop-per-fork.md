---
name: autoresearch-editing-loop-per-fork
description: "Autoresearch = Karpathy loop per the macOS fork: fixed prepare.py owns the metric, one editable edit.py, no seeded ideas; outputs are leads only"
metadata:
  type: project
---

The fork is a training loop: the agent edits `train.py`, and `prepare.py` holds the fixed metric. For C10 the four agent-facing files were adapted (D-C10r-impl-1, 2026-10-06). `prepare.py` stays fixed and holds the seed, a 900 s per-arm edit budget, the setup gates and `evaluate(apply_edit)`, which owns the metric and guards. `edit.py` is the only editable file, and its baseline is the harness's edit. `program.md` is the fork's text with editing's specifics. `README.md` keeps the fork's shape and carries no corpus findings. `experiments/track_c/autoresearch_c10/launch.sh` now execs the v13 fence launcher (`v13_launcher.py:18`: `claude --safe-mode --model claude-fable-5-1 --effort high --permission-mode dontAsk …`, Fable 5.1 high replaced Opus 5.5 xhigh at the 2026-10-06 relaunch). Single source for the setup and its deviations: `docs/AUTORESEARCH.md` (its launcher paragraph at line 20 still describes the pre-v13 sandbox builder).

**Why:** the operator wants the fork followed exactly, with no cap, no seeded ideas and a sandboxed context (D-C10r-rulings-1). The first draft broke the fork's key property, because its editable unit computed its own score. `--bare` was rejected because it never reads the subscription login.

**How to apply:** don't route ideas to the loop. "Candidate knob for the loop" wording conflicts with no-seeded-ideas. Don't give the loop agent corpus context. Edit the source on the program branch, never the sandbox copy. Check the loop's baseline against LAW#3 outside the sandbox. Fold a kept recipe in only through a pre-registered falsifier re-verified across seeds. See [[autoresearch-sandbox-fence-and-tmux-driving]], [[c10-stacked-solve-tradeoff]].

**Not a faithfulness gate (C10i, 2026-06-27):** never use autoresearch to decide whether an external method port is scientifically valid. It is an optimizer / candidate generator and Goodhart-prone by construction; run it only after the measurement frame, held-out guard and method-faithfulness gate are stable. Its outputs are leads for the hypothesis register, never CORPUS evidence or promotion claims. Port validity comes from experiment-gate + method-replication checks + advisor review (source faithfulness, positive controls, active trace, metric matching, bias/confound audit, cross-family review) — [[method-ports-need-replication-faithfulness-gate]].
