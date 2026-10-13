# Task: build "Lab View" — a local, read-only visual lab notebook for the C10 experiments (Part 1)

Worktree (your cwd): /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a. Read `CLAUDE.md` and `DISCIPLINE.md` first.

## Who it is for
The operator: an architect with no ML background who wants to (1) SEE what each experiment did inside the model, (2) LEARN the ideas in plain, non-technical language, and (3) keep an evaluated visual history that helps the team get past blocks. It is opened in a browser on a Mac and on an iPhone (Safari, portrait and landscape) over Tailscale.

## Hard rules
1. Read-only on science: never edit, import-and-mutate, or run anything under `experiments/`, `memit_dry_run/`, `CORPUS/`, `docs/*PREREG*`; never load a model, tokenizer or torch; never use the GPU. Read result JSON/log files only.
2. Every picture shows real recorded data only. If a field is missing for a run, the picture says "not recorded for this run" — never invent or interpolate.
3. Test-first (operator rule): derive the test list from this brief before coding; tests use small synthetic fixtures plus at least one real record per supported schema; include a build round-trip test (build → files exist → HTML parses → every image referenced exists), a missing-field test, and a phone-width check (no element wider than 390 px by CSS rule). Run them green and paste output in your report.
4. New files only: `tools/labviz/` (package), `tools/labviz_serve.sh`, `results/labviz/` (generated output; add `results/labviz/site/` to `.gitignore` except the per-run images under `results/labviz/runs/` which are committed). No edits to existing files except `.gitignore`.
5. Use the repo venv `.venv/bin/python -B` (matplotlib, numpy, jinja2 available; no plotly). Front end: plain HTML/CSS/JS; three.js from `https://cdn.jsdelivr.net/npm/three@0.160.0/` (module build + OrbitControls) for the 3D view, with a graceful 2D fallback if WebGL or the CDN is unavailable.
6. Smallest code that meets this brief; no speculative options.

## Data sources (survey them first and cite file paths in your report)
- Per-run records: `results/c10u_mint2/**/{F,V2}_r*_*.json` (step 3; arm fields such as `para_full_binding_n`, `canon_full_n`, `extra.per_fact_position_curve`, `extra.per_position_teacher_forced`, `extra.relation_flips`, `extra.same_frame_flips`, `extra.post_geometry`, `locality_*`), their readings `results/c10u_mint2/r3_read_after_*.json`, and the per-run logs `results/c10u_mint2/**/logs/behavior_*.log` (lines `A1_single ... n: canon x/24 para y/72 ... L1 a/12 L3 b/30 ... ppl p->q`).
- Step 5: `results/c10w_oracle/*/` (stage logs with `step N loss X` training lines and harness lines; JSON outputs under `train/`, `adapters/` metadata only — never open .safetensors).
- Older experiments: `results/c10*` folders — support any record that carries harness-style per-arm counts; list unsupported schemas in the report rather than guessing.
- The plain-language scoreboard `docs/c10_scoreboard.json` (brief, results, queue) — the history spine from 2026-06 onward.

## Full history (operator request: "apply all of our historical data")
Cover the WHOLE program history, not only step 3/5. Survey every experiment output folder under `results/` (all `c10*`, `c2*`, `a1*`, `law3_repro_*`, `autoresearch_*` and any other folder holding run records) and every `CORPUS/NN_*.md` verdict header. Give every run that has per-arm or per-fact data its own card and saved image (oldest data first is fine for the build; display newest first). Runs without machine-readable detail still appear: one card per CORPUS verdict / scoreboard row with its plain verdict and a link-style reference (`CORPUS/NN`), so the History timeline and Evaluations span June 2026 to now with no gaps. List in the report every folder you surveyed, how many runs each contributed, and any you could not parse.

## Every model tested (operator request: "historically on all of the models we have tested")
The program has tested more than one model line over its history (survey `CORPUS/`, `results/`, `configs/hparams/`, `docs/` and `memory_mirror/` for model names, e.g. Qwen2.5-3B and earlier lines). Tag every run card and every History point with the model it used (from the record, the hparams file it names, or the CORPUS doc — never guessed; "model not recorded" otherwise). The 3D view takes the model from the selected run and draws that model's real layer count and edited band (read from its config/hparams or the record). Add a **Models** tab: one panel per model line with its size, layers, when it was used, what was tested on it, its best results, and a plain-language note on why the program moved on (cite the CORPUS doc). List every model found and its sources in the report.

## What to build
`tools/labviz/build.py` (re-runnable, idempotent) generates `results/labviz/site/index.html` + assets, and per-run images `results/labviz/runs/<run-id>.svg` (also `.png`). `tools/labviz_serve.sh` rebuilds every 60 s and serves the site on port 8765 (bind 127.0.0.1 and the LAN; Tailscale delivers to localhost) with `python -m http.server`.

Pages (one responsive single-page app with tabs; large touch targets; dark theme with high-contrast text — the operator found light-grey text unreadable):
1. **Now** — the latest run and the running experiment if any (from the newest logs): what it is in plain words, progress, latest scores.
2. **Runs** — one card per run, newest first, each with its saved image and: *What we tried* (plain words), *What the picture shows*, *What it means*, *Side effects*. Images per run:
   - a 24 × 3 grid (facts × reworded templates), green right / red wrong, when per-fact data exists;
   - word-by-word confidence curve (per-position probability) when recorded;
   - a side-effects strip (real facts flipped /12, unrelated facts kept /30, writing-quality change);
   - for training runs, the loss curve.
3. **3D model** — an interactive tower of Qwen2.5-3B's 36 layers (thin slabs, labelled), the edited band (layers 4–8) highlighted; for the selected run, per-layer write sizes as glowing bars if recorded (else the band only, labelled "write sizes not recorded"); touch rotate/zoom; a caption explaining what a layer is in one sentence.
4. **History** — every scoreboard result on one timeline chart (score out of 72, goal line at 61, baseline ~14, colour by kind), each point linking to its card where one exists.
5. **Learn** — 8–12 short illustrated explainers in plain words, each tied to our data: what a language model is; layers; what "writing a fact into the model" means; why reworded questions are the hard part; what a made-up name is and why it splits into pieces (tokens); the vocabulary-word idea; side effects and why we check them; baselines, repeats and why one run is not proof; the ceiling test; what "the goal 61 of 72" means. No jargon without a one-line definition.
6. **Evaluations** — a structured entry per experiment: question asked · result · what it rules out · what it leaves open · next step; read from `docs/c10_evaluations.json` (create it with entries derived ONLY from `docs/c10_scoreboard.json` results; the program session will maintain it). Show a "patterns" panel: which kinds of idea moved the score and which did not.

## Deliverable
Write `results/labviz_codex_impl.md`: model/effort header; files created with SHA-256; data-source survey (supported/unsupported schemas); the test list and its green output; how to run (`bash tools/labviz_serve.sh`); a screenshot description of each tab at phone width; open issues. Then say DONE.
