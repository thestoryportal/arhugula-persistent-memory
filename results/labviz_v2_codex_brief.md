# Task: build "Lab View v2", Phase 1 (everything the runs already recorded)

Worktree (your cwd): `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, called `<wt>` below.

Read these first:
- `CLAUDE.md` and `DISCIPLINE.md`;
- the binding design: `docs/LABVIZ_V2_SPEC.md`, all of it, especially §2 (rules), §3 (data inventory with jq paths), §4A (design and usability), §5 (per-item design), §6 (run card) and §11 (program context model and map);
- the v1 brief `results/labviz_codex_brief.md` and v1 report `results/labviz_codex_impl.md`;
- the 3D notes `/private/tmp/claude-501/labviz_3d_investigation.md`.

Operator ruling: **D-C10r-labviz-2** (`EXPERIMENT_RUNBOOK.md:372`).

## When to start

**Start only when no GPU coordinator is live (no python while a GPU stage gate is armed).**
- Before any python command, check: `pgrep -fl python` lists no experiment driver, and no `results/*_logs/*.gate.*.json` stage is waiting on a next stage.
- If a coordinator is live, stop and report "blocked: GPU coordinator live".
- During the work, run python only through the test command and the builder below.

## Who it is for

1. **The operator:** an architect with no ML background, on a Mac and an iPhone (Safari, portrait and landscape) over Tailscale. They asked for the ten recommendations and the four asks (a)–(d) in spec §4. They also asked that **all historical science** be read in its own terms, not C10's (spec §11), and that the UI be properly organised and readable (spec §4A; fonts were too small, and content was not connected across lines of science).
2. **An AI reader:** it must reason from the run-card JSON, never from pixels.

## Hard rules

1. **Read-only on science.**
   - Never edit experiment drivers (`experiments/`), the engine (`memit_dry_run/`), preregs (`docs/*PREREG*`), `CORPUS/`, ledgers, or any results JSON or log.
   - Never import or run anything under `experiments/` or `memit_dry_run/`.
   - Never load a model, a tokenizer or torch. Never open `.safetensors`, `.pt` or `.npz`. Never use the GPU.
   - Read `config.json` only from `hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/`. Never read tokenizer or vocabulary files.
2. **Every number shown comes from a file, with its path.** Each value in a run card is a leaf `{value, src:{file, path}}`, or `{value, derived, inputs, rule_src}` (spec §6). Missing → `{value:null, missing, tier}`, and the page says "not recorded for this run" plus how it could be obtained. Never invent, interpolate or round a percentage back into a count.
3. **Gate exemption must survive.** `tools/c10w_p2_gate.py:21–30` exempts exactly `.venv/bin/python -B -m http.server 8765 --bind 0.0.0.0 --directory results/labviz/site` and `.venv/bin/python -B tools/labviz/build.py`.
   - Keep the builder's entry point and command line byte-identical: no new CLI flags.
   - Do not change `tools/labviz_serve.sh`.
   - Do not start, probe or curl the server on port 8765.
4. **Files you may change or create:**
   - `tools/labviz/**`;
   - new data tables `tools/labviz/{labels,gates,links,stimulus,contexts}.json`;
   - generated output under `results/labviz/` (`site/`, `runs/`, new `cards/`, `review/`).

   Nothing else. `docs/c10_evaluations.json` is read-only for you now; the program session maintains it.
5. **Test-first.**
   - Write the tests below before the code, and record them failing in the report.
   - Use small synthetic fixtures plus the real records named in the tests.
   - Run tests only with: `env -C <wt> MPLCONFIGDIR=/private/tmp/labviz-mpl .venv/bin/python -B -m unittest tools.labviz.test_labviz`. Add the new tests to `tools/labviz/test_labviz.py`; v1's tests must stay green.
6. **Smallest code that meets the spec.** No speculative options. Plain HTML, CSS and JS. three.js stays pinned at `https://cdn.jsdelivr.net/npm/three@0.160.0/`, with the 2D fallback.
7. **Evidence tiers are labelled** (spec §2.4). Phase 1 shows RECORDED data only. Any place that would need a replay or telemetry says so, with the tier name.

## Data sources

Spec §3 lists every family with jq-verified paths and sample values. The main ones:
- `results/c10v_layerpick/{step0,pass1,run}.json`;
- `results/c10w_oracle/{step0_*,p1_*,p2_*}/` (`eval.json`, `verdict.json`, `train/*.json`, `*.log`) and `results/c10w_oracle_logs/*.gate.*.json`;
- `results/c10u_mint2/r3/*.json` and `r3_read_after_*.json`;
- the earlier C10 harness files;
- the program documents in spec §11.1.

**Verify every path with jq before writing code against it** (CLAUDE.md §6). If a path in the spec does not resolve, stop and report it. Do not guess a replacement.

## What to build (in this order; spec section in brackets)

1. **Foundation: information architecture and type** [§4A.1–4A.2].
   - Five-destination navigation on every page: Map (home), Science lines, Runs, Inside the model, Learn & evaluations.
   - A status strip, breadcrumb, context chip and evidence-tier badge on every page.
   - Body text 16–17px; nothing below 13px, including picture text at rendered size; prose at most 72ch wide; contrast ≥ 4.5:1 for text and ≥ 3:1 for marks.
   - First view ≤ 1 MB. Line chunks load as classic `<script>` files, so the page works from `file://`. Load `model.js` as a classic script.
   - Fix every row of the §4A.3 audit.
2. **Program context model** [§11.1–11.3].
   - Parse the registry (54 rows, by regex over whole rows), the CORPUS headers, the overlay, the e2e layers, the F1 conditions C1–C10, the hypothesis register and the runbook tracks into namespaced nodes and sourced edges.
   - Assign each run a context by the §11.2 rule.
   - Add the curated `contexts.json` era framing, with verbatim-quote citations.
   - Remove every C10 hard-coding listed in §11.3, so each tab captions a run in its own era's terms.
3. **Connections map with focus mode**, as the home page [§11.4]. Phone version: drill-down list.
4. **Run cards** [§6, item 10]: `results/labviz/cards/<card-id>.json` plus `cards/index.json`, with a `context` block. Every page section links to its card.
5. **Result badge** [item 1], with `labels.json`.
6. **Per-fact strip and fact panel** [items 2 and a, recorded parts], with `stimulus.json` bound by SHA to `experiments/track_c/c10e_bandknob.py`. The builder checks the strings with a text search, never by importing the file.
7. **Side-effect gauge** [item 3], with `gates.json`: limits derived from prereg rules, and checked against the recorded gate booleans.
8. **Write sizes** [item 4]: one shared scale per unit, numbers printed on the bars, only written layers coloured, the configured band drawn as an outline, and the 3D picker opening on the newest run with writes.
9. **Compare view** [item 5].
10. **Plain-words captions** through `links.json` [item 6].
11. **C10V per-fact layer map and margins** [item 8].
12. **C10W training-step slider** [item 9]: recorded loss and step times only.
13. **Parts of a layer and the wiring diagram**, in 2D and 3D [items b and c, static]. Show the "untouched" basis: "by design" for MEMIT, "hash-verified" for C10W.
14. **Recorded-event timeline** [item d, Phase 1 scope].
15. **Design review** [§4A.5].
    - Open `file://<wt>/results/labviz/site/index.html` (never the 8765 server) with a headless browser driven by node (`/opt/homebrew/bin/node`; Playwright or Puppeteer) or the session's browser tool. No python.
    - Screenshot at 1440 × 900, 390 × 844 and 844 × 390, covering the screens listed in §4A.5. Dump computed styles.
    - Save everything to `results/labviz/review/<UTC>/`.
    - Have a decorrelated reviewer judge the §4A.4 criteria. Fix every FAIL before reporting done.

Not in Phase 1: telemetry, the tokenizer extract, replays, the player, the logit lens, and per-part activity. Show their places as "needs telemetry / needs an observation replay (NOT EVIDENCE)".

## Tests (write first; each must fail before its code exists)

1. **Leaf integrity:** every leaf in every generated card resolves with its jq-style path in its file to the same value. No bare number appears outside a leaf.
2. **C10V B0 write colouring:** the written layers of `recipes.B0` (A7) are exactly {8}; the configured band is 4–8; only layer 8 is coloured. B·A7 writes 4–8 with values 4.85 / 16.13 / 27.69 / 9.71 / 16.31 (rounded in the test only).
3. **Badge:** the C10V card shows 12 of 72, goal 61 (from `docs/c10_scoreboard.json:.goal`), label `NULL`. The C10W P1 card shows 70 of 72 and "not yet labelled" (`verdict.json:.final_label` is null). An unknown label renders verbatim in grey.
4. **Side-effect gauge:** the B·A7 described-as value is 86.17; the derived limit is 87.0 (90.0 − 3, prereg `:74`); it shows FAIL; and the derived result agrees with `run.json:.readings.B.locality_gates.described_as == false`.
5. **Per-fact strip:** 24 cells from `detail.A7_coined_coined[].para_full_hits`. For C10U, the binding arm uses the teacher-forced strip type with its own title. Missing cells are hatched.
6. **Stimulus binding:** each transcribed string occurs verbatim in `experiments/track_c/c10e_bandknob.py`, and the file's SHA-256 equals `pass1.json:.identity.source_sha256["experiments/track_c/c10e_bandknob.py"]` (`1f6be581…e695`). A changed SHA shows "not transcribed for this code version".
7. **Layer map:** `step0.json` gives a 24 × 5 G table; the margins come from `winning_margins[0]`, with the repeat in `[1]`; `map_reproduced` is true; `spearman_G_edge` is −0.479.
8. **Training slider:** each C10W train record yields 40 loss points (10…400) and 400 step times. No per-step answers are shown.
9. **Untouched basis:** the C10W train record reads "hash-verified: 434 of 434 unchanged"; the MEMIT record reads "by design".
10. **Context model:**
    - 54 registry rows parsed, including the 9-, 11- and 12-field rows;
    - `exp:A7`, `hyp:A:A7` and the arm `A7_coined_coined` are distinct;
    - registry `track_e` is not merged with runbook "TRACK E";
    - c10u records map to `exp:C10U-mint2` by result path;
    - an unmatched run shows "context not recorded" with candidates;
    - every `contexts.json` quote occurs at its cited line;
    - every edge's source line names both ends.
11. **No C10 framing outside C10:** the rendered Mistral-7B model page and a G6.1 run page contain none of "of 72", "goal 61", "reworded", "made-up", "C10".
12. **Map:** focus on `cond:C10` reaches `spec:§8.9` and the decisions, experiments and CORPUS entries named by the overlay's C10-chain row (expected set derived from the files). `model:Mistral-7B` links to `era:t-branch`.
13. **Readability contract (CSS):** no font-size below 13px in any rule; body ≥ 16px; prose `max-width ≤ 72ch`; picture text ≥ 13px at a 600px render; 44px targets; no fixed width above 390px; the 3D canvas ≤ 70vh.
14. **Payload:** the first view is ≤ 1 MB. Line chunks are classic scripts. `model.js` is not loaded as `type="module"`.
15. **Build round trip:** HTML parses; every image, chunk and card referenced exists; a second build gives identical bytes on unchanged inputs; no file outside the allowed paths changes; no forbidden import (torch, transformers, tokenizers, experiment modules).

## Deliverable

Write `results/labviz_v2_codex_impl.md` containing:
- a model and effort header;
- every file created or changed, with its SHA-256;
- the jq verification of every data path you used, and any spec path that did not resolve;
- the test list with its failing-first output and its final green output;
- the §4A.5 review: the screenshot list, the computed-style summary (minimum font size, minimum contrast), and the reviewer's verdict table, with its fixes;
- open issues.

Then say DONE. No commits, no canonical science updates.
