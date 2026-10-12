# Lab View acceptance tests (written before implementation)

Source: `results/labviz_codex_brief.md`, including Full history and Every model tested.
This is a read-only evidence viewer for the write engine / behavioral validation
cells of the F1 map. It makes no new scientific verdicts.

1. Builder exists; first run must fail before production code exists.
2. Single-arm synthetic counts remain exact; binding counts take precedence.
3. Missing fields stay null and pictures explicitly say "not recorded for this run".
4. Percentages are never rounded back into counts.
5. Real legacy arms + detail, recipe wrappers, mint records, reader probability
   arrays, training records, retained-fact records, and per-unit arrays parse.
6. A 24 × 3 grid uses recorded Boolean answers only; missing cells stay unknown.
7. Teacher-forced positions are labelled separately from free-answer outcomes.
8. Probabilities stay separate from teacher-forced hit rates.
9. Side effects preserve recorded denominators and before/after writing quality.
10. Layer sizes are attached only to the matching arm and recipe.
11. Model tags come from recorded fields, referenced hparams, or cited evidence;
    unknown remains "model not recorded". Reviewer names are not tested models.
12. The tower takes real layer counts and exact edited layer sets; no guessed band.
13. A model inventory covers documented earlier lines and distinguishes tested,
    configured, and mentioned-only models. Transition notes cite their sources.
14. Harness log and training log parsers preserve each observation, including zeros.
15. Terminal logs cannot be described as running; timestamps/staleness are visible.
16. Every results folder is surveyed, flat June files included; unsupported and
    unreadable files are listed. Every numbered CORPUS verdict and scoreboard
    row appears, without manufacturing absent historical experiments.
17. Evaluations seed has exactly one entry per scoreboard result; all five fields
    are source-bound. Later builds read it without overwriting operator updates.
18. Build round trip: HTML parses, seven tabs exist, every referenced image exists,
    SVG and PNG are both saved, source citations resolve, no broken card links.
19. Second build has stable IDs and bytes for unchanged inputs; images are reused.
20. Phone CSS constrains all elements to the viewport, has no fixed minimum width
    exceeding 390 px, and provides 44 px touch targets and high contrast text.
21. Browser checks at 390 px portrait and 844 px landscape: all tabs, selector,
    History links and offline / WebGL-unavailable fallback, with screenshots if
    the managed sandbox allows a browser to run.
22. No torch/model/tokenizer import or science-path execution; only authorised
    output files change. Server syntax is valid and binds port 8765 with a 60 s
    rebuild loop; live serving is checked if socket binding is permitted.

The explicit request to create `docs/c10_evaluations.json` is the brief's specific
exception to its output-directory rule. No commits or canonical science updates.
