# Lab View v2, Phase 1

The binding contract is docs/LABVIZ_V2_SPEC.md. Build from the worktree root:

```sh
.venv/bin/python -B tools/labviz/build.py
env -C "$PWD" MPLCONFIGDIR=/private/tmp/labviz-mpl TMPDIR=/private/tmp/labviz-review/test-tmp .venv/bin/python -B -m unittest tools.labviz.test_labviz
```

Open results/labviz/site/index.html directly. The existing launcher and command lines are unchanged. Five destinations share the selected run and URL state: Map, Science lines, Runs, Inside the model, and Learn & evaluations. Classic line scripts load detailed cards on demand, including from file URLs.

cards.py reads recorded JSON and log text; context.py joins the Markdown registry, CORPUS headers, overlay, F1 conditions, architecture, hypotheses and decision ledger. It never imports experiment code or loads a model, tokenizer, adapter or tensor. Replays, sandbox records, telemetry folders and records marked NOT EVIDENCE or EXPLORATORY are excluded. Concurrent C10Z files are excluded from this Phase 1 build.

Every run-card measurement is sourced, derived with its operands, or explicitly missing. The card lists source hashes; cards/scales.json names the complete eligible applied-write population. Configured bands are outlines, separate from actual writes. Reader badges and gate booleans attach to their recorded configuration. C10 counts, teacher-forced scores, oracle measurements and other eras' measures retain distinct meanings. No percentage becomes an invented count.

docs/c10_evaluations.json is read-only. The five Lab View tables live here; all entries in contexts.json are DRAFT and await the program session's review. Unmatched or ambiguous contexts remain unknown with sourced candidates. Documentary model-family cards contain quoted findings, without invented scores or run pictures. Recorded event timestamps and untimed observations are separate.

The builder writes changed bytes only. Saved SVG/PNG summaries use typed card values and a deterministic SVG/Pillow renderer; Matplotlib regression fixtures also retain measured text sizes. images_manifest.json records picture widths, every text size, input keys and renderer identity. The renderer never starts a child process. CPU elapsed time, peak RSS and picture-call count are printed for the build-budget check, without a build timestamp in the site or cards.

Optional three.js/OrbitControls are pinned to 0.160.0. HTML labels and the 2D fallback remain available when the CDN or WebGL fails. The wiring animation is labelled "diagram, not recorded activity". Activity, piece text, logit lenses and historical internal flow remain named Phase 2/3 gaps.

review.mjs drives the file URL with Playwright from the approved scratch directory; measure.js records font transforms, composited contrast, targets, clipping, interaction counts and request bytes. It issues no reviewer verdict. The implementation report records the actual browser-launch limitations.
