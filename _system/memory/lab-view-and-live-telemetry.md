---
name: lab-view-and-live-telemetry
description: Program owns program/registers/c10_evaluations.json (one plain-words entry per experiment at close-out); new builds carry opt-in LAW#5-inert JSONL telemetry
metadata:
  type: project
---

Operator ruling D-C10r-rulings-11 (2026-10-07 evening). Full relay: `results/operator_relay_2026-10-07_labviz.md`; ledger row runbook §5.2 D-C10r-rulings-11.

**Lab View:** read-only web lab notebook on port 8765 (`code/apps/labviz/labviz_serve.sh`, rebuilds every 60 s; built by Codex session `codexviz`, report `results/labviz_codex_impl.md`). Codex seeded `program/registers/c10_evaluations.json` from the scoreboard; the program owns it since 2026-10-07. The program does not start the server itself: the auto-mode classifier refuses starting or probing a network-exposed server, so the operator starts it (or adds a permission rule) — do not work around it. Phone URL once served: http://robert-mbp.tail36ce25.ts.net:8765 ([[tailscale-remote-access]]). The GPU gate exempts the Lab View server and its rebuild (`code/lab/runners/c10w_p2_gate.py` EXEMPT).

**Program duty:** at every close-out, alongside the `program/registers/c10_scoreboard.json` update, add/refresh one `program/registers/c10_evaluations.json` entry per experiment: question asked · result · what it rules out · what it leaves open · next step — plain words ([[plain-language-to-operator]]). Follow the schema Codex created; don't invent fields.

**Telemetry (step 6 C10X, step 7 C10Y, ASTRA C10Z, and later builds):** opt-in writer appending small JSONL snapshots to `results/<exp>/telemetry/` — per-layer write norms, per-position target probabilities, logit-lens top-k at each band layer for the probe prompts, phase markers. Off by default or proven inert (identical counts and records on vs off); test-first ([[test-first-one-round-builds]]); reviewed with the build; dated pre-observation amendment to each frozen prereg before its build.

**Why:** the operator wants to watch runs live and see the whole program history across every model tested, without loading a model.

**How to apply:** put the telemetry amendment + on/off inertness test in each build brief; never touch the C10U/C10V/C10W drivers for this.
