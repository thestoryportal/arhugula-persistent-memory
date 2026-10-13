# GPT-6-Astra (high) — review: CLAUDE.md / AGENTS.md alignment with the evolved workflow

Read-only. Worktree = current dir. The uncommitted diff is at /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/guidance_align.diff (also `git diff CLAUDE.md AGENTS.md tools/closeout_check.py`). 26 memory notes were also copied into memory_mirror/ from ~/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory (untracked new files).

## Operator's request
"Review CLAUDE.md and AGENTS.md comprehensively against our evolved workflow to ensure all is in alignment." Earlier: CLAUDE.md is an important place "as long as it isn't bloated. And if it is bloated that should be addressed."

## Ground truth for "the evolved workflow" — check every edited claim against these, cite file:line
memory_mirror/*.md (esp. context-management-every-session, operator-decision-scope, plain-language-to-operator, never-idle-arm-completion-watch, gpu-gate-refuses-any-venv-python, test-first-one-round-builds, rerun-never-patch, graft-disabled-audit-2026-10-08, llmdb-root-points-at-main-checkout, disk-budget-before-dispatch, approved-deletes-ask-then-rmtree, mps-offset-view-conversion-bug, notebooklm-via-browser-harness, local-only-no-rented-compute, operator-overnight-autonomy-2026-10-06), EXPERIMENT_RUNBOOK.md §3.3a, DISCIPLINE.md, .claude/settings.json, tools/closeout_check.py, tools/render_state.py, tools/engine_fingerprint.py, tools/autonomy_mission.json, /Users/robertrhu/.claude/memento/handoffs/maestro3_takeover_20261010.md (the latest binding directives).

## Decide
1. Any edited statement that is FALSE or contradicts a ground-truth source (file:line both sides)?
2. Any load-bearing workflow rule still MISSING or still STALE in either file (e.g. pod-era, 4090, CUDA, /workspace assumptions; deletion protocol; dispatch traps)?
3. Bloat: name any passage that repeats a decision moment already covered elsewhere in the same file (cite both lines). Do not flag length alone.
4. tools/closeout_check.py change: correct? does it introduce any silent failure or false GREEN?
5. Conflicts between CLAUDE.md and AGENTS.md (they must agree).

## Output
Under 700 words. First line: `VERDICT: ACCEPT` | `ACCEPT-WITH-FIXES` | `REJECT`. Then numbered findings, each with file:line, the problem, and the exact replacement text. No restating of the files.
