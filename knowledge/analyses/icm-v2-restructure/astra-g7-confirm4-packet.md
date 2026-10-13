# Astra high, fourth confirm round: heading parser on `corpus/icm-v2`

Your last verdict was NO-GO: the line scanner `heading_entries()` missed Setext, blockquote and list headings, mis-tracked fences, and counted headings inside HTML comments. It is in `/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261012T114331Z-2ec28dcb/icm-v2/phase3/step6/8e/astra/verdict.md`. The fix is commit `f39822e8` (lane 8f). Review only `git diff 0dd74910..f39822e8`.

You are read-only. Do not edit any file. Run repo Python with `LLMDB_ROOT=$PWD PYTHONPATH=code .venv/bin/python -B`. `markdown-it-py 3.0.0` is installed in `.venv`. Do not run model or GPU work.

The change: `heading_entries()` now takes `heading_open` tokens from `MarkdownIt('commonmark')`, in document order, including headings in blockquotes and lists. `heading_slug()`, the dedup loop and `resolve()` are unchanged. The lane reports the anchor map byte-identical and zero slug differences between old scanner and parser over all split parts and the three monoliths.

## Questions

1. Rerun your round-3 section 2 script. Which cases now give `rc=2` (or, for `HTML comment`, the original section)? The `slug transfer` and `explicit ID` cases are known limits; the operator accepted them as NON-BLOCKING (they go to OPEN-ITEMS).
2. List EVERY remaining class of live edit that makes an old anchor resolve, with exit 0, to a section other than the one it named at the pin, in this one answer. Exclude the two known limits above.
3. Is any statement or test in `0dd74910..f39822e8` false or wrong? Is the new dependency declared consistently (`pyproject.toml`, `uv.lock`, `.github/workflows/ci.yml`)?
4. Ruling 4: is the restructure fit to merge?

## Output

First line exactly `VERDICT: GO` or `VERDICT: NO-GO`. Then one section per question. Mark each finding BLOCKING or NON-BLOCKING, with file:line and the command and output that prove it. Do not repeat items from earlier verdicts. Do not report style preferences as findings.
