---
name: lab-view-and-live-telemetry
description: "Operator ruling D-C10r-rulings-11 (2026-10-07 evening): Lab View web notebook (codexviz builds it); the program maintains docs/c10_evaluations.json at every close-out; steps 6/7 and ASTRA drivers get an opt-in, LAW#5-inert JSONL telemetry writer; steps 3-5 drivers untouched."
metadata:
  type: project
---

Full relay: `results/operator_relay_2026-10-07_labviz.md`; ledger row runbook §5.2 D-C10r-rulings-11.

**Lab View:** read-only web lab notebook on port 8765, built by tmux session `codexviz` (brief `results/labviz_codex_brief.md`, report `results/labviz_codex_impl.md`). Do not reuse that pane. Codex seeds `docs/c10_evaluations.json` from the scoreboard results; after its report lands, the program owns it.

**Program duty:** at every close-out, alongside [[c10k-route-a-resume]]'s scoreboard row, add/refresh one `docs/c10_evaluations.json` entry per experiment: question asked · result · what it rules out · what it leaves open · next step — plain words ([[plain-language-to-operator]]). Follow the schema Codex created; don't invent fields.

**Telemetry (step 6 C10X, step 7 C10Y, ASTRA C10Z, and later builds):** opt-in writer appending small JSONL snapshots to `results/<exp>/telemetry/` — per-layer write norms, per-position target probabilities, logit-lens top-k at each band layer for the probe prompts, phase markers. Off by default or proven inert (identical counts and records on vs off); test-first ([[test-first-one-round-builds]]); reviewed with the build; dated pre-observation amendment to each frozen prereg before its build.

**Why:** the operator wants to watch runs live and see the whole program history across every model tested, without loading a model.

**How to apply:** put the telemetry amendment + on/off inertness test in each build brief; never touch the C10U/C10V/C10W drivers for this.

**Status 2026-10-07 20:55:** Codex DONE 20:31 (report present, 7 tabs, 1,369 cards; 23/23 unittest re-run green by the program: `env -C <wt> MPLCONFIGDIR=/private/tmp/... .venv/bin/python -B -m unittest tools.labviz.test_labviz`). `docs/c10_evaluations.json` = `{source, entries[14]}`, seeded from the scoreboard → the program now owns it. Live serving (`tools/labviz_serve.sh`, binds 0.0.0.0:8765, rebuilds every 60 s) never verified: Codex's sandbox and this session's permission rules both refuse starting a server — the operator runs it. Outputs (results/labviz 169 MB, tools/labviz) are uncommitted.
**Duty moved to the program session (operator, 2026-10-07 ~21:00):** the remote-control Claude session that watched the team tmux sessions and was to notify the operator of Lab View completion + give phone access is blocked; "Now this is your job." So the program session notifies the operator (PushNotification; it is skipped while the terminal is active) and owns phone access. The auto-mode classifier refuses the program starting `tools/labviz_serve.sh` or even waiting on port 8765 ([Expose Local Services]) — the operator starts the server or adds a permission rule; do not work around it. Phone URL once served: http://robert-mbp.tail36ce25.ts.net:8765 (Tailscale userspace mode forwards tailnet TCP to local services, [[tailscale-remote-access]]).
