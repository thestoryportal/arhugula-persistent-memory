---
name: durable-artifact-path-collision
description: Adding a new mode to a result-writing script can silently overwrite a canonical prior artifact via the default output-path branch — check the path logic.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: faa20de1-5a6b-48c2-9b82-b32bd2d440cd
---

When extending a harness with a new run mode (e.g. `WRITE_MODE=batch_staircase` in `g6_scale_n.py`), the output-filename logic only special-cased `WRITE_MODE=="batch"`, so the new mode fell through the `else` branch and wrote to the **default** path `g6_scale_n_result.json` — silently **overwriting the canonical A0/G6.1 sequential falsifier result**.

**Why:** result filenames derived by a conditional (`X if mode==A else DEFAULT`) assume only the known modes exist; a third mode collides with DEFAULT. The overwrite is silent — the run reports success while clobbering a load-bearing prior artifact.

**How to apply:** (1) Before launching a new mode of a result-writing script, read the output-path line and confirm the new mode gets its OWN filename. Prefer `DEFAULT if mode==canonical else f"..._{mode}_..."` (invert the condition so only the one canonical mode owns the default name). (2) Durable results that took GPU-minutes are not sacred — they can be clobbered by your own next run; the binding copy is whatever the run's stdout log captured (here `g6_scale_n_v2.log` preserved the A0 numbers, so the science survived; only the JSON needed regenerating). (3) Recover by regenerating the authentic artifact (re-run), not by hand-fabricating a partial JSON from remembered values — fabricated data in a canonical file is worse than a missing one. Relates to [[evidence-over-scaffolding]] and [[match-metric-to-the-claim]].

**RECURRED 2026-06-18 (post-B3):** the B1 7B run (`g6_scale_n_param.py`, default output path) overwrote `g6_scale_n_batch_result.json` — the 3B A1 canonical PASS artifact. Same root cause (WRITE_MODE default output path is model-agnostic). Recovered by re-running the canonical 3B batch (data also safe in `a1_batch.log` + `CORPUS/14`); added a `RESULT_TAG` env to the param script. Lesson held: parametrized harnesses MUST namespace their output path by model/variant.
