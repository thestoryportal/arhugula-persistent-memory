# Task: build "Lab View v2", Phase 1 (everything the runs already recorded)

Worktree (your cwd): `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, called `<wt>` below.

Read these first:
- `CLAUDE.md` and `DISCIPLINE.md`;
- the binding design: `docs/LABVIZ_V2_SPEC.md` (v2, folded 2026-10-08), all of it, especially §2 (rules, build budget), §3 (data inventory with jq paths, incl. §3.10 non-C10), §4A (design and usability), §5 (per-item design, the role, label and gate tables), §6 (run card and leaf types), §9.1 (ingestion boundary) and §11 (program context model and map);
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
2. **Every value in a card is a typed leaf (spec §6):** JSON-source `{value, src:{file, path}}` (full recorded precision; only rendering rounds), document-source `{value, src:{file, line, quote}}`, derived `{value, derived, inputs[], rule_src}`, or missing `{value:null, missing, tier}`. Only the spec's whitelisted structural keys may be bare. Every cited file is in the card's `sources[]` with its SHA-256. Missing → the page says "not recorded for this run" plus how it could be obtained. Never invent, interpolate or round a percentage back into a count.
3. **Gate exemption must survive.** `tools/c10w_p2_gate.py:25–26` exempts exactly `.venv/bin/python -B -m http.server 8765 --bind 0.0.0.0 --directory results/labviz/site` and `.venv/bin/python -B tools/labviz/build.py`.
   - Keep the builder's entry point and command line byte-identical: no new CLI flags.
   - Do not change `tools/labviz_serve.sh` (SHA-256 `c90afb9ce1bd8c3b54af95f4534f055404587a0105045e931ee34d6cb9a05a4b`). It reruns the builder every 60 s, during GPU stages too.
   - The production builder (`tools/labviz/build.py` and every module it imports at run time, e.g. `render.py`) starts no child process (`subprocess`, `os.system`, `multiprocessing`). The test module `tools/labviz/test_labviz.py` may run the `jq` binary through `subprocess` (test 1), and nothing else.
   - Do not start, probe or curl the server on port 8765.
4. **Build budget and determinism (spec §2.3).** Write a file only when its bytes change; skip pictures whose inputs are unchanged. No output carries wall-clock time (no `built_utc`); a rebuild on unchanged inputs gives identical bytes. Budget: warm rebuild ≤ 15 s and ≤ 1.5 GB peak RSS; cold build ≤ 120 s and ≤ 2 GB. Measure both with `/usr/bin/time -l` around the unchanged command line and report them; a miss is reported, not hidden.
5. **Files you may change or create:**
   - `tools/labviz/**`;
   - new data tables `tools/labviz/{labels,gates,links,stimulus,contexts}.json`;
   - generated output under `results/labviz/` (`site/`, including `site/cards/`; `runs/`; `review/`);
   - your report `results/labviz_v2_codex_impl.md`;
   - two scratch directories: `/private/tmp/labviz-mpl/` (Matplotlib cache for the tests) and `/private/tmp/labviz-review/` (the Playwright install, its npm cache and its browsers). Run every npm and Playwright command there with `npm_config_cache=/private/tmp/labviz-review/npm-cache` and `PLAYWRIGHT_BROWSERS_PATH=/private/tmp/labviz-review/ms-playwright`, so nothing is written under `~/Library/Caches` or `~/.npm`.

   Nothing else. `docs/c10_evaluations.json` is read-only for you now; the program session maintains it.
6. **Tables you transcribe, not design.** `labels.json` = spec §5 item 1 label table, exactly; `gates.json` = the §5 item 1 role table and the §5 item 3 gate table, exactly; `links.json` = spec §5 item 6. `contexts.json` you may draft: mark every entry `"status": "DRAFT"`, with machine-checked quotes; the program session reviews it before publication (spec open point 5), and the site shows DRAFT framing as "draft framing, not yet reviewed".
7. **Test-first.**
   - Write the tests below before the code, and record them failing in the report.
   - Use small synthetic fixtures plus the real records named in the tests.
   - Run tests only with: `env -C <wt> MPLCONFIGDIR=/private/tmp/labviz-mpl .venv/bin/python -B -m unittest tools.labviz.test_labviz`. Add the new tests to `tools/labviz/test_labviz.py`; v1's tests must stay green.
8. **Smallest code that meets the spec.** No speculative options. Plain HTML, CSS and JS. three.js stays pinned at `https://cdn.jsdelivr.net/npm/three@0.160.0/`, with the 2D fallback. No text drawn on a canvas (3D labels become HTML overlays).
9. **Evidence tiers are labelled** (spec §2.4: RECORDED, TELEMETRY, REPLAY (NOT EVIDENCE), EXPLORATORY). Phase 1 shows RECORDED data only. Any place that would need a replay or telemetry says so, with the tier name.

## Data sources

Spec §3 lists every family with jq-verified paths and sample values. The main ones:
- `results/c10v_layerpick/{step0,pass1,run}.json` (`run.json:.pass_sha256.pass1` binds the reading to `pass1.json`);
- `results/c10w_oracle/{step0_*,p1_*,p2_*}/` (`eval.json`, `verdict.json`, `interim_reader_configuration_v2.json`, `train/*.json`, `HALT.json`, `*.log`) and `results/c10w_oracle_logs/*.gate.*.json`;
- `results/c10u_mint2/r3/*.json` and **only** `results/c10u_mint2/r3_read_after_replicateF.json` for C10U labels and gates (never `_v2` or `_frozen`);
- the earlier C10 harness files, and the non-C10 records of spec §3.10;
- the program documents in spec §11.1.

**Verify every path with jq before writing code against it** (CLAUDE.md §6). If a path in the spec does not resolve, stop and report it. Do not guess a replacement.

## What to build (in this order; spec section in brackets)

1. **Foundation: information architecture and type** [§4A.1–4A.2].
   - Five-destination navigation on every page: Map (home), Science lines, Runs, Inside the model, Learn & evaluations.
   - A status strip, breadcrumb, context chip and evidence-tier badge on every page. Mark the run or model content with `data-region="content"`.
   - Body text 16–17px; nothing below 13px at rendered size; prose at most 72ch wide; contrast ≥ 4.5:1 for text and ≥ 3:1 for marks.
   - First view ≤ 1 MB. Line chunks load as classic `<script>` files, so the page works from `file://`. Load `model.js` as a classic script.
   - Fix every row of the §4A.3 audit.
2. **Ingestion boundary** [§9.1]: the RECORDED reader skips `results/replays/`, `results/sandbox/` and every `telemetry/` folder, and any record whose `evidence_status` starts with "NOT EVIDENCE" or "EXPLORATORY".
3. **Program context model** [§11.1–11.3].
   - Parse the registry (54 rows, by regex over whole rows, with the §11.1 D-ID grammar and §11.2 brace expansion), the CORPUS headers, the overlay, the e2e layers, the F1 conditions C1–C10, the hypothesis register and the runbook tracks into namespaced nodes and typed edges (direct / curated / derived).
   - Choose each experiment's decision and each run's context by the §11.2 rules; ties stay unknown with candidates.
   - Draft `contexts.json` (era per registry row, era framing) with verbatim-quote citations, marked DRAFT.
   - Remove every C10 hard-coding listed in §11.3, so each tab captions a run in its own era's terms.
4. **Connections map with focus mode**, as the home page [§11.4]. Phone version: drill-down list.
5. **Run cards** [§6, item 10]: `results/labviz/site/cards/<card-id>.json` plus `site/cards/index.json`, with `identity.role`, joins and a `context` block. Every page section links to its card.
6. **Result badge** [item 1]: on C10 cards, roles decide what it shows; non-C10 cards show their own sourced label or status and measure; goal and label only on binding cards; C10W prints `verdict.json:.class` verbatim; `labels.json` transcribed.
7. **Per-fact strip and fact panel** [items 2 and a, recorded parts]. Question text by the §3.6 precedence: recorded stimulus, else the SHA-bound `stimulus.json` (bound to `experiments/track_c/c10e_bandknob.py` by SHA, role and order, checked as text, never by importing), else "not transcribed".
8. **Side-effect gauge** [item 3]: ✓/✗ only from recorded booleans for the exact configuration; rule limits as "derived reference line" without ✓/✗; "not judged yet" where nothing is recorded.
9. **Write sizes** [item 4]: one shared scale per unit, numbers printed on the bars, only written layers coloured, the configured band drawn as an outline, no predicted, replay or sandbox value on a RECORDED ruler, and the 3D picker opening on the newest run with writes.
10. **Compare view** [item 5], with the eligibility contract.
11. **Plain-words captions** through `links.json` keyed by record or phase directory [item 6].
12. **C10V per-fact layer map and margins** [item 8], all reading leaves from `.readings.B`.
13. **C10W training-step slider** [item 9]: recorded loss and step times only.
14. **Parts of a layer and the wiring diagram**, in 2D and 3D [items b and c, static], with the exact "untouched" wording of spec §3.5.
15. **Recorded-event scrubber** [item d, Phase 1 scope]: recorded events only. The Phase 3 replay player is not part of this build.
16. **Design self-check** [§4A.5].
    - Open `file://<wt>/results/labviz/site/index.html` (never the 8765 server) with Playwright driven by `/opt/homebrew/bin/node`. Playwright is not installed (checked 2026-10-08; cached Chromium builds only, no WebKit): install it under `/private/tmp/labviz-review/` and install Chromium and WebKit there with `npx playwright install chromium webkit`, using the two environment variables of rule 5. No python.
    - Run Chromium and WebKit at 1440 × 900, 390 × 844, 360 × 780, 844 × 390, and 1440 × 900 at 200 % zoom, over the screens of §4A.5. Measure what §4A.4 lists (text size as computed `font-size` × rendered transform scale, incl. SVG via `getScreenCTM()`; boxes only for clipping and layout; composited contrast, target rectangles, first-view bytes from the request log, scripted tap and keystroke counts, URL state, keyboard and touch) into `results/labviz/review/<UTC>/measure.json`, with screenshots.
    - This is a **self-check**: report the numbers; do not judge PASS/FAIL as the reviewer. The program session runs the decorrelated review after you report.

Not in Phase 1: telemetry, the tokenizer extract, replays, the replay player, the logit lens, per-part activity and the sandbox. Show their places as "needs telemetry / needs an observation replay (NOT EVIDENCE)".

## Tests (write first; each must fail before its code exists)

1. **Leaf integrity:** every leaf in every card is one of the four types and valid by spec §6: JSON-source paths resolve (grammar `.k`, `["k"]`, `[n]` only) to the exact value; document-source quotes occur at their line and contain the value; derived inputs are valid leaves and recompute the value; no bare value outside the whitelist; `sources[]` hashes match. Cross-check ≥ 50 JSON-source leaves (every family, every grammar form) with the `jq` binary. Full precision: B·A7 layer 8 `write_size` = `16.31455421447754`.
2. **C10V B0 write colouring:** the written layers of `recipes.B0` (A7) are exactly {8}; the configured band is 4–8; only layer 8 is coloured. B·A7 writes layers 4–8 (layer 8 = `16.31455421447754`).
3. **Badge and roles:**
   - C10V B·A7 (binding): 12 of 72, goal 61 from `docs/c10_scoreboard.json:.goal`, label `NULL`.
   - C10V B·A1: role `control`, no goal, no label chip; recipe A·A7: `reference`; Bshuf·A7: `shuffled-control`, with `NULL-CONTROL-ONLY` shown under the role line.
   - C10W P1 `oracle_p1`·A7: 70 of 72, "not judged yet" (`verdict.json:.final_label` null), `.class` printed verbatim, and the interim chip `PARTIAL-CEILING-LOCALITY-COST` captioned "oracle measurement, not a route".
   - C10U `r3/F_r0_mint1_s0.json`: `LEAD` (from `r3_read_after_replicateF.json`). `r3/F_r1_mint1_s0.json` (same binding count 46, replicate 1): no label chip, "replica of mint1_s0".
   - **Wrong-reader fixture:** a reading whose counts match but whose family, recipe, arm, seed or replicate differs, or whose `pass_sha256` / `p1_eval.sha256` does not match, never attaches.
   - An unknown label renders verbatim in grey with "label not in Lab View's table".
   - **Non-C10 badges** (the role table applies to `results/c10*` cards only): the R5 card (`results/r5_paraphrase_robustness.json`) shows its recorded label `CHARACTERIZATION` (class `characterization`) and per-arm `ptest_mean_rate`, with no goal and no 72-scale; the G6.1 card (`results/g6_scale_n_result.json`) shows the registry status "SPLIT (cross-entity FALSIFIED)" (`docs/EXPERIMENT_REGISTRY.md:13`, document-source leaf) and no label chip, no goal.
4. **Label table:** `labels.json` equals the spec §5 item 1 table (parsed from the spec's markdown), and every label string the spec §3.9 enumeration finds in the real records has a row. Only a final PASS-type label maps to `pass`. A rendered-colour check: for one chip of every class, the computed background colour is green only for `pass`.
5. **Side-effect gauge:**
   - B·A7 described_as 86.17 shows ✗ because `run.json:.readings.B.locality_gates.described_as` is false; its reference line is 87.0, derived from 90.0 (prereg `:74`).
   - Consistency: the gate-table rule reproduces **every present** recorded boolean: C10V 3 readings × 5 (15), the 7 C10U binding-reading arms that carry `.gates` (49), the C10W interim configuration × 7. The 5 C10U UNDERFIT readings without `.gates` (`F` `modifier_s0`–`s2`, `V2` `mint2_s1`, `mint2_s2`) render no glyph and no invented outcome. Boundary fixtures (at the limit passes, one past fails) and a mismatch fixture.
   - C10W P1 `closedform` and `oracle_canon_s0` configurations show reference lines and "not judged yet", no ✓/✗. C10W's reference arm is `recipes.closedform.arms.A7_coined_coined` (described_as 87.56); G4 checks the canonical frame and all 20 training frames; G6 uses U = `eval.json:.u.A7_coined_coined` for every configuration, O-A7-canon included (there is no `.u.A7_canon`); G7 uses the matched shuf control.
6. **Per-fact strip:** 24 cells from `detail.A7_coined_coined[].para_full_hits`. For C10U, the binding arm uses the teacher-forced strip type with its own title. Missing cells are hatched.
7. **Stimulus:**
   - `results/c10e_bandknob.json` shows its **recorded** `.stimulus` text; C10V shows the SHA-bound transcription (`pass1.json:.identity.source_sha256["experiments/track_c/c10e_bandknob.py"]` = `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695`); a changed SHA shows "not transcribed for this code version".
   - Role and order are bound (`CANON` at `:51`; `PTEST` entry j at line 53 + j); a **permuted-template** transcription fails.
   - C10W: `generated[3i+j].subj` = `detail[i].subj` and `.template` = `PTEST[j]`.
8. **Layer map:** `step0.json` gives a 24 × 5 G table; margins from `winning_margins[0]`, repeat in `[1]`; `map_reproduced` true; the footer's statistic is `run.json:.readings.B.spearman_G_edge` = `−0.3162875387734472` (the test asserts the path; B0's −0.479… never appears on B's map).
9. **Training slider:** each C10W train record yields 40 loss points (10…400) and 400 step times. No per-step answers are shown.
10. **Untouched basis:** a C10W card reads exactly "the 434 base tensors were hash-verified frozen during adapter training; the evaluated model has the adapter's ΔW merged into down_proj 4–8; `base_band_hash` = `final_band_hash` shows the base was restored after evaluation", and colours down_proj 4–8 as written. A MEMIT card reads "by design (the engine writes only down_proj)".
11. **Context model:** the spec §11.5 list, including: 54 rows parsed (9-, 11-, 12-field rows); `exp:A7`, `hyp:A:A7`, `A7_coined_coined` distinct; registry `track_e` ≠ runbook "TRACK E"; `C10U-mint2`'s decision is `D-C10u-mint2`, not `D-C10r-rulings-12`; the §11.2 fixtures (brace rows `:19`, `:25`, `:60`; "D-ID" on `:59`; `ROUTING-BLOCKED-UNDERFIT`; basename `run.json`; `c10u_mint2/r2/`; a tie); each of the 54 rows has exactly one era; every `contexts.json` quote occurs at its line; every edge is valid for its type.
12. **No C10 framing outside C10:** in `[data-region="content"]` of the rendered Mistral-7B model page, a G6.1 run page and a D1 capacity-law page, none of: "of 72", "goal 61", "reworded", "made-up", "C10". (The status strip, navigation, breadcrumb and connections panel are outside the region.)
13. **Map:** focus on `cond:C10` reaches `spec:§8.9` and the decisions, experiments and CORPUS entries named by the overlay's C10-chain row (expected set derived from the files). `model:Mistral-7B` links to `era:t-branch`.
14. **Readability contract (CSS and measurement):** no font-size below 13px in any rule; the measurement script reports computed `font-size` × transform scale, and its fixtures behave: 12px text with a large line height fails, 16px SVG text scaled by 0.5 fails, 13px unscaled SVG text passes; body ≥ 16px; prose `max-width ≤ 72ch`; 44px targets; no fixed width above 360px; the 3D canvas ≤ 70vh; no `fillText` on a canvas.
15. **Payload:** the first view is ≤ 1 MB. Line chunks are classic scripts. `model.js` is not loaded as `type="module"`.
16. **Ingestion boundary:** fixtures under `results/replays/`, `results/sandbox/`, a `telemetry/` folder, and a NOT EVIDENCE / EXPLORATORY record elsewhere produce no RECORDED card and no value in any `headline`, `label`, `gates` or `scale`.
17. **Links:** each `links.json` key's CORPUS file exists, its first 12 lines contain the record's `decision_id`, and an evaluation entry has that `ref`. C10W P2 (`p2_20261008T034226_086980Z/`) shows "no plain-words evaluation linked yet".
18. **Compare eligibility:** the same 24 facts in shuffled row order join by subject; runs with different templates or scoring kinds show "not comparable".
19. **Build round trip:** HTML parses; every image, chunk and card referenced exists; a second build on unchanged inputs gives identical bytes; no output contains the build time; no file outside the allowed paths changes; no forbidden import (torch, transformers, tokenizers, experiment modules) in `tools/labviz/*.py`, and no child-process call in the production builder and its run-time modules (the test module may call `jq`); `tools/labviz_serve.sh` keeps its SHA-256; the two exempt command lines in `tools/c10w_p2_gate.py:25–26` still match the builder and server invocations in `tools/labviz_serve.sh:7`, `:10`, `:15`.
20. **Derived meaning:** every derived leaf lists every operand (the `configured` leaf includes the card's own `layer` as a structural operand) and recomputes from them; every derived context edge carries its whole chain (spec §6 example: registry `:60` → overlay `:22` → F1 `:71` / e2e `:14`). Must-fail fixtures: an operand removed, a chain link removed, a card whose write size exceeds its `scale.max`. `scale.max` comes from `results/labviz/site/cards/scales.json`, whose operand set equals the eligible population (spec §5 item 4); at 2026-10-08 its absolute-size maximum is `113.7967300415039` (`results/c10h_anyedit_pilot.json`), and no C10V card may carry 55.42212677001953 (B0·A2 is 55.45940399169922).
21. **Write kinds kept apart:** a fixture with offline predicted sizes (`dW_fro`-style) and an injection measurement produces no value on a RECORDED ruler and no change to `scales.json`.
22. **Bindings:** a fixture run whose recorded hparams SHA differs from `configs/hparams/qwen25_3b_memit_hparams.json` shows "hparams for this run's code version not read"; one whose `.model.revision` differs from the snapshot shows no `config.json` facts.
23. **3D picker default:** with fixtures of different dates, the picker opens on the newest card that has writes, never on one without.
24. **Recorded-event scrubber:** events from gate records, log markers, loss points and record timestamps are ordered by their recorded time (ties by source path, then line), and the scrubber visits only them.
25. **Write-on-change:** on a warm rebuild with unchanged inputs, no output file's mtime changes and the picture renderer is called zero times (count the calls).
26. **Non-C10 content:** the G6.1 card has 100 `records` leaves (`entity`, `field`, `expressed_at_apply`, `retained_at_end`) and 3 `rungs`; the R5 card has the 4 arms with `ptest_mean_rate`, per-fact `ptest_hits` and `ptest_obs`, and its recorded `templates.P_test` as the question text.

## Deliverable

Write `results/labviz_v2_codex_impl.md` containing:
- a model and effort header;
- every file created or changed, with its SHA-256;
- the jq verification of every data path you used, and any spec path that did not resolve;
- the test list with its failing-first output and its final green output;
- the measured cold and warm build time and peak RSS against the §2.3 budget;
- the §4A.5 self-check: what you installed and where, the screenshot list, and the measurement summary (minimum rendered text size, minimum composited contrast, smallest target, first-view bytes, task tap counts). No reviewer verdict: the program session runs that review;
- the DRAFT `contexts.json` entries awaiting review;
- open issues.

Then say DONE. No commits, no canonical science updates.
