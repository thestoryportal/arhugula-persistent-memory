# Math lab observability — build brief (D-ML-1 tooling)

Status: build brief, 2026-10-08. Owner: lead (program session). Builder: Codex session `codexml`. Reviewer: GPT-6-Astra (high) after the build.

## What the operator asked for (verbatim)
"One thing about the Math lab, I want observability into it. So be sure to create a very user friendly dashboard to view as it runs that is part of teamdash. And we will want to integrate the feature and its data it into LabViz ultimately too."

## Context you need
The math lab (pre-registration `docs/MATHLAB_PREREG.md`, Decision-ID D-ML-1, under Astra review — read it, do NOT edit it) tests C10 hypotheses with linear algebra on saved tensors, on CPU, without loading the model. Steps: 1 harvest pass (one GPU job), 2 reproduce the harness's write solve offline (marimo notebook), 3 retro-prediction calibration against measured GPU results (FAIL = the lab stops, cheaply), 4 an autonomous hypothesis loop (later). Output is staging-only under `results/mathlab_staging/`. Results are tier MATH-PROXY: they can reorder the GPU queue, never promote a claim. The lab has not run yet; you are building the observability first, against fixtures.

The team dashboard is tmux-based: `tools/team_dashboard.sh` builds session `dashboard` with tabs (team, active, experiment, helpers). Each tab is a stdlib-only script run by `/usr/bin/python3`. Read `tools/dashboard_experiment.py` (closest model: plain words, `--once COLS ROWS` render mode, colours, width handling) and `tools/dashboard_live.py` (shared rules — reuse `gpu_state()` for "is another job on the GPU"; never re-derive what it already derives). Tests live in `tools/test_dashboard_live.py`; follow that style.

## Part A — the event contract (one source of truth)
1. Each lab run writes `results/mathlab_staging/runs/<run_id>/events.jsonl`: append-only, one JSON object per line, never rewritten. This file is the ONLY authority for run state. Do not add a separate status file — the dashboard (and later LabViz) derive state by folding the events.
2. New stdlib module `tools/mathlab_events.py`:
   - `emit(run_dir, type, **fields)` appends one validated line (`ts` ISO-8601 UTC, `schema: 1`, `run_id`, `type`, fields) with a single `O_APPEND` write + flush.
   - The event types form a closed, discriminated set; unknown type or missing/extra-required field → raise. Define at least: `run_started` (step, title, deadline_ts, pid), `admission` (allowed: bool, reasons: list), `stage_started` (stage, plain_words, cap_s), `progress` (stage, done, total, unit), `gate_result` (gate_id, plain_words, observed, bar, comparison, passed: bool), `stage_finished` (stage, outcome ∈ {PASS, FAIL, INVALID}, summary), `resource_sample` (avail_gib, floor_gib, rss_gib, cpu_pct), `finding_staged` (finding_id, tier="MATH-PROXY", summary, path), `candidate_added` (candidate_id, source, question, offline: bool), `halted` (reason, diagnostic_path), `run_finished` (outcome, summary). Adjust only if the prereg demands a field you can cite.
   - `fold(events) -> dict` is a PURE function producing the lab state the dashboard shows (current step/stage, per-step status, gates table, latest resources, findings, candidates, halt, recent events). The dashboard and LabViz both call this one function — the interpretation lives in one place.
   - `read_events(path)` returns events plus a list of parse errors; a malformed line is surfaced as a visible error in the UI, never silently skipped.
3. Steps 1–3 builds (later) will emit through this module; you are defining the contract they must use.

## Part B — the teamdash tab `mathlab` (`tools/dashboard_mathlab.py`)
Audience: the operator, a non-specialist, glancing at it. Plain words first; numbers with their meaning; no jargon without a one-line gloss.
- Header: what the lab is in one line; current run id, state (running / waiting for GPU / stopped: check failed / halted / finished / not started), elapsed vs the hard deadline.
- Step ladder 1→4 with ✓ ✗ ▶ · and one plain sentence each ("1 · Harvest: record the model's internal inputs for every prompt (one GPU pass)").
- Now: the current stage in plain words, a progress bar (done/total), time used vs cap.
- Checks: one row per pre-registered gate — what it checks in plain words, measured value, the bar, PASS/FAIL. A failed step-3 check must read as the designed cheap stop, not an error.
- Machine: free memory as a bar against the 8 GiB floor, lab process memory/CPU, and "GPU in use by <job>" from `dashboard_live.gpu_state()` when applicable.
- Findings (tier MATH-PROXY, labelled "math estimate, not evidence") and Candidate questions (source, offline yes/no).
- Last ~8 events, cleaned.
- Idle state (no runs yet — the state tonight): show the plan, the pre-registration's status line and SHA prefix read from `docs/MATHLAB_PREREG.md`'s header, and what the lab is waiting for. This is what the operator sees first, so make it good.
- Refresh every 2 s; `--once COLS ROWS` renders one frame to stdout for tests; adapts from 80 to 300 columns; colours consistent with the experiment tab.
- Wire it into `tools/team_dashboard.sh` as window `mathlab` right after `experiment`; update the header comment's tab list. (`teamdash mathlab` then opens it directly — the launcher passes the window name through.)

## Part C — LabViz forward requirement (record only)
Append a short section to `docs/LABVIZ_V2_SPEC.md` titled "Forward requirement — math lab (D-ML-1)": LabViz will ingest `results/mathlab_staging/runs/*/events.jsonl` through `tools/mathlab_events.fold`, plus staged findings; no second schema. Do not change LabViz code now.

## Tests (write first)
`tools/test_dashboard_mathlab.py` (stdlib unittest) with fixture event streams: no runs; harvest running with progress; waiting for GPU; step-2 PASS; step-3 gate FAIL → cheap stop; halted with diagnostic; finding + candidate staged; malformed line → visible error; contract rejects unknown type and missing field; `--once` renders at 80 and 200 columns without exceeding the width. Also run `/usr/bin/python3 -m unittest tools/test_dashboard_live.py` to prove nothing else broke.

## Constraints
- stdlib only for the dashboard and events module (they run under `/usr/bin/python3`); no torch import anywhere; nothing touches the GPU — an experiment (ASTRA attempt 3) is running on it now.
- Do not edit `docs/MATHLAB_PREREG.md`, `experiments/`, the engine, CORPUS, ledgers, the runbook, or other dashboard tabs (only the wiring line + comment in `team_dashboard.sh`). Do not rebuild or restart the live dashboard session; the lead does that. Do not commit.
- Bad output looks like: a status.json alongside events (two authorities); a dashboard that re-implements fold logic; jargon like "ρc" or "Kf" on screen without a plain gloss; a malformed event silently dropped; an idle screen that just says "no data".

## Report
Files written, test output (both suites), and a `--once 110 40` render pasted for: the idle state, a running harvest, and the step-3 cheap stop.
