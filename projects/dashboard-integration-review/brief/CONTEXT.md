# Shared context for the dashboard/skills integration review (MAESTRO46, 2026-10-11)

Operator's request, verbatim: "I've gathered dashboard tools repos, a variety of skills, data vizualization tools repos, data dashboarding and viz best practices and TUI dashboard repos to analyze and review as potential integrations into our work across these and other domains. [...] launch Codex agents focused on domains included to conduct a review, assessment, research for how they might integrate into our workflows."
Operator hold, still in force: no building of the terminal dashboard or LabViz until the operator has reviewed this context. This review informs that decision; it builds nothing.

## Who we are
- An empirical research program ("LLM-as-Database"): edit facts into language models (MEMIT) and test, falsification-first, whether the spec is implementable. Runs on one MacBook M3 Pro (48 GB, Apple MPS, no CUDA). A second Intel Mac is being set up as a helper host.
- Team: MAESTRO (Claude Code) orchestrates Codex builder sessions in tmux; a cross-family reviewer ("Astra", GPT via `codex exec`) reviews every promote gate. The operator is often remote on an iPhone (Termius into tmux, Claude remote control).
- Claude's weekly usage is tight; Codex carries heavy reading and building.
- Evidence culture: every number is sourced from a recorded file, derived with operands, or shown as missing. Stale data must show as UNAVAILABLE, never as idle/OK. Claims cite file:line.
- Data shapes: JSON / JSONL result records under results/, Markdown ledgers (CORPUS/, runbook), a queue/program state in docs/program_state.json, run logs. Private research data: prefer local/self-hosted; flag anything that sends data to a third party or phones home.

## Our current surfaces
A. Terminal dashboard: tmux session `dashboard`, 8 tabs (team, active, experiment, mathlab, helpers, science, storage, queue), each a stdlib Python script (tools/dashboard_*.py) or shell loop. Read on a phone screen via Termius. Constraint: a GPU safety gate refuses experiment launches while any non-exempt Python process runs; the queue tab is exempt only because it launches as exactly `/usr/bin/python3 <path>` (system Python 3.9, stdlib). A tab that needs a venv or third-party Python package would block experiment launches. Non-Python binaries (Go, Rust, Node) are not Python, but still add install/maintenance cost.
B. LabViz ("Lab View v2"): a static site built by tools/labviz/build.py (venv Python) into results/labviz/site/, opened as a file URL. Vanilla app.js, SVG/Pillow renderer, optional three.js pinned to 0.160.0, Playwright review script. Five views: Map, Science lines, Runs, Inside the model, Learn & evaluations. Spec: docs/LABVIZ_V2_SPEC.md.
C. Planned, not built: a phone dashboard hosted on the Intel Mac that reads one frozen status record; old data shows UNAVAILABLE. Under review, on hold.
D. Agent skills: Claude Code loads skills (SKILL.md packages); a third-party skill runs with our agent's tool access, so its install safety matters (scripts it runs, network calls, prompt-injection-style instructions).
