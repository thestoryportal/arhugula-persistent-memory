# Operator ruling relayed by the operator-facing session — 2026-10-07 evening (record as D-C10r-rulings-11)

Operator, verbatim: "Yes, proceed." (to a two-part visualization plan), then "And can we apply all of our historical data to the visualization as well?" and "And historically on all of the models we have tested".

**Part 1 — Lab View (being built now by tmux session `codexviz`; do not reuse it).** A read-only web lab notebook on port 8765 (brief `results/labviz_codex_brief.md`, report `results/labviz_codex_impl.md`): per-run images from existing records, plain-language explanations, a 3D layer view, the full program history from June 2026 across every model tested, and an Evaluations page fed by `docs/c10_evaluations.json`. **You maintain `docs/c10_evaluations.json`** from now on, alongside `docs/c10_scoreboard.json`: one entry per experiment — question asked, result, what it rules out, what it leaves open, next step — in plain words.

**Part 2 — live telemetry in the not-yet-built drivers** (step 6 C10X, step 7 C10Y, ASTRA C10Z): an opt-in writer that appends small JSONL snapshots during a run to `results/<exp>/telemetry/` (per-layer write norms, per-position target probabilities, logit-lens top-k at each band layer for the probe prompts, phase markers), so Lab View can show runs live without loading a model. It must not change any computed result: off by default, or proven inert under LAW#5 (identical counts and records with telemetry on vs off); test-first; reviewed with the build; folded in as a dated pre-observation amendment where a prereg is frozen. Existing drivers (steps 3, 4, 5) stay untouched.

LAWs, reviews and one GPU run at a time are unchanged.
