# Lab View v2, Phase 1

The binding contract is projects/labviz-spec-v3/drafts/LABVIZ_V2_SPEC.md. Build from the worktree root:

```sh
.venv/bin/python -B code/apps/labviz/build.py
env -C "$PWD" MPLCONFIGDIR=/private/tmp/labviz-mpl TMPDIR=/private/tmp/labviz-review/test-tmp .venv/bin/python -B -m unittest tools.labviz.test_labviz
env -C "$PWD" MPLCONFIGDIR=/private/tmp/labviz-mpl .venv/bin/python -B -m unittest tools.labviz.test_mathlab
node --test code/apps/labviz/test_*.cjs
```

Open projects/labviz-spec-v3/receipts/bulk/labviz/site/index.html directly. The existing launcher and command lines are unchanged. Five destinations share the selected run and URL state: Map, Science lines, Runs, Inside the model, and Learn & evaluations. Classic line scripts load detailed cards on demand, including from file URLs.

cards.py reads recorded JSON and log text; context.py joins the Markdown registry, CORPUS headers, overlay, F1 conditions, architecture, hypotheses and decision ledger. It never imports experiment code or loads a model, tokenizer, adapter or tensor. Replays, sandbox records, telemetry folders and records marked NOT EVIDENCE or EXPLORATORY are excluded. Concurrent C10Z files are excluded from this Phase 1 build.

Every run-card measurement is sourced, derived with its operands, or explicitly missing. The card lists source hashes; cards/scales.json names the complete eligible applied-write population. Configured bands are outlines, separate from actual writes. Reader badges and gate booleans attach to their recorded configuration. C10 counts, teacher-forced scores, oracle measurements and other eras' measures retain distinct meanings. No percentage becomes an invented count.

Math lab (D-ML-1) appears in Runs: search `D-ML-1` or `mathlab_staging`. Only `results/mathlab_staging/runs/*/events.jsonl` supplies its state, through `tools.mathlab_events.read_events` and the shared `fold`. Both `results/mathlab/**` and `results/mathlab_staging/**` are excluded from generic JSON, log, verdict-label and applied-write-scale ingestion. Regeneration retires their former generic cards, pictures, unused chunks and uncited evidence mirrors. Cards show admission scope, experiment steps, stages, gate outcomes and thresholds, halts, resource samples, referenced staged Markdown findings, and candidate questions as ideas to test. Zero eligible mint arms is shown as a derivation only when all three recorded mint norm checks fail; terminal PASS remains harvest completion. Every MathLab card retains `MATH-PROXY` and "math estimate, not evidence", including picker, model, and compare routes. These cards have no score pictures.

MathLab citations name `src.reader=mathlab_events.read_events`: `.events` and `.errors` address that reader's result, with errors using the workspace-relative stream path. They are not raw JSONL paths or physical line numbers. Validation reruns the shared reader and fold, verifies their source hashes, and rejects a changed reader or fold rule source. Event bytes must match before and after the shared read; three unstable attempts abort before publishing. The accepted bytes supply the card hash and evidence mirror, keeping the saved snapshot consistent while a producer appends. Original JSONL and explicitly referenced findings are mirrored as evidence snapshots; parse errors and missing or rejected finding references remain visible.

program/registers/c10_evaluations.json is read-only. The five Lab View tables live here; all entries in contexts.json are DRAFT and await the program session's review. Unmatched or ambiguous contexts remain unknown with sourced candidates. Documentary model-family cards contain quoted findings, without invented scores or run pictures. Recorded event timestamps and untimed observations are separate.

The builder writes changed bytes only. Saved SVG/PNG summaries use typed card values and a deterministic SVG/Pillow renderer; Matplotlib regression fixtures also retain measured text sizes. images_manifest.json records picture widths, every text size, input keys and renderer identity. The renderer never starts a child process. CPU elapsed time, peak RSS and picture-call count are printed for the build-budget check, without a build timestamp in the site or cards.

Optional three.js/OrbitControls are pinned to 0.160.0. HTML labels and the 2D fallback remain available when the CDN or WebGL fails. The wiring animation is labelled "diagram, not recorded activity". Activity, piece text, logit lenses and historical internal flow remain named Phase 2/3 gaps.

review.mjs drives the file URL with Playwright from the approved scratch directory; measure.js records font transforms, composited contrast, targets, clipping, interaction counts and request bytes. It issues no reviewer verdict. The implementation report records the actual browser-launch limitations.
