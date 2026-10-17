# Equip step 0: vet results and install decisions (MAESTRO, 2026-10-17, Opus 5.5)

MAESTRO read all four research files in full and checked them against their sources. The equip research is complete. Three install decisions need the operator. Each one has a recommendation below. Nothing is installed yet.

## Decisions for the operator

**1. promptfoo: run it with npx at a pinned version. Do not install it globally.**
Command form: `npx -y promptfoo@0.123.1 eval -c <config> -o <run>/results.jsonl --no-cache --no-share`.
- 0.123.1 was released on 2026-09-18 (29 days ago). The latest version, 0.124.1, was released on 2026-10-08 (9 days ago), so it is newer than the two-week minimum age.
- 0.123.1 requires `@anthropic-ai/claude-agent-sdk` 0.3.263 (released 2026-09-06) and `@openai/codex-sdk` ^0.153.2, so its own dependencies bring both agent providers.
- Node here is v26.8.2. promptfoo needs Node >= 22.22.0.
- `--no-share` stops result upload. Model and grader calls still send data to their providers.
- The first run downloads into the npm cache (`~/.npm/_npx`). That cache is outside the repo.

**2. Skills: copy the vetted files into `~/.claude/skills/` for Claude sessions only.**
- `ai-evals-course/evals-skills` at commit `80d5f7b0127c7572ed9e9339937adbfd7240ffeb`: install all nine skills (evals-start, error-discovery, eval-audit, write-code-eval, write-judge-prompt, validate-evaluator, generate-synthetic-data, build-review-interface, evaluate-rag).
- `promptfoo/promptfoo` at commit `ea8b3d073a63769f7be243ac3c3460f72881a930`: install `plugins/promptfoo/skills/promptfoo-evals/` (SKILL.md, references/eval-patterns.md).
- Install by copying the exact bytes that MAESTRO read. The `skills` CLI does not work here (see skills-sh-candidates.md §1), and `npx skills add` takes the latest commit, which nobody has read.
- Do not install them for Codex now. Each skill ships `agents/openai.yaml` with `allow_implicit_invocation: true`, so a Codex builder could invoke one without being asked. Decide this in Phase 4, when builder skills are designed.

**3. marimo: keep the global 0.24.2. Do not add it to `M/.venv`.**
Run notebooks with `uv run --with marimo --with duckdb marimo run <nb.py>`, or declare dependencies with PEP 723 metadata in the notebook. This keeps the project lock file unchanged.

## Vet record

### Candidate C1 changed: use `ai-evals-course/evals-skills`, not `hamelsmu/evals-skills`
Line 4 of the hamelsmu README says the repository is deprecated and the skills moved to `ai-evals-course/evals-skills` (Shreya Shankar and Hamel Husain). The successor is owned by a GitHub Organization, is licensed Apache-2.0, has 1,522 stars, is not archived, and was last pushed on 2026-09-24. Plugin version 0.3.1.

What MAESTRO read in full: error-discovery (SKILL.md + review-loop.md), eval-audit, validate-evaluator, write-judge-prompt, evals-start, write-code-eval, promptfoo-evals (plugin copy) + its `agents/openai.yaml`, all plugin manifests and the README. Read by heading and risk scan only: generate-synthetic-data, build-review-interface, evaluate-rag.

Risk scan (grep for install, network, shell, delete, push, upload, credential, and prompt-override phrases):
- No scripts, no hooks, no MCP servers. Every file is markdown, JSON, YAML or one PNG.
- The only install text is the suggestion `pip install judgy` (validate-evaluator line 183). Our rule: `uv run --with judgy`, never pip.
- error-discovery starts a local Python `http.server` and a review web app. That is by design, for an interactive human review session.
- promptfoo-evals tells the agent to "Install or upgrade with `npx promptfoo@latest` only when needed". Our rule overrides this: use the pinned version from decision 1.

### Method conflicts and our rulings
1. **The judge's model family.** write-judge-prompt says "The same model used for the main task works as judge". Our rule stays cross-family (charter Phase 6; c8-eval-engineer judge-collision rule; arXiv 2604.22891 and 2608.18091). Also hide authorship from judges (2608.18091).
2. **Judge alignment metric.** validate-evaluator and eval-audit require TPR and TNR for a judge against human labels, and keep Cohen's kappa for human-to-human agreement only. c8-eval-engineer lists kappa as one option. Ruling: TPR/TNR plus Rogan-Gladen correction plus a bootstrap CI for judge-vs-human; kappa for two human labelers. This matches arXiv 2511.21140.
3. **Error analysis first.** evals-skills ("Do not recommend building evaluators ... before completing error analysis") and c8 (Husain loop, FM-G) agree. Phase 2 starts with manual error discovery on real transcripts, before any grader is written.

## Research file status
| File | Checked against | Result |
|---|---|---|
| anthropic-demystifying-evals.md | Full article text read in Chrome | All verbatim quotes match. Additions are in its "MAESTRO verification" section. |
| eval-tools.md | npm registry; skill files | promptfoo latest is 0.124.1, confirmed. The repeat flag and per-trial result shape stay UNVERIFIED until the first pinned run. |
| skills-sh-candidates.md | GitHub repos at pinned commits | C1 is deprecated (see above). C2 is clean. |
| arxiv-agent-evals.md | `get_abstract` re-fetch of 7 papers | All exist and the key numbers match. Numbers come from abstracts only. |

## Sources
- Vetted file copies: the session scratchpad (`.../scratchpad/vet/c1n`, `.../vet/c2`). The commits above are the durable reference.
- `gh api repos/ai-evals-course/evals-skills` and `repos/hamelsmu/evals-skills` (2026-10-17).
- `npm view promptfoo dist-tags engines time`, `npm view promptfoo@0.123.1 peerDependencies optionalDependencies`, `npm view @anthropic-ai/claude-agent-sdk time`, `node --version` (2026-10-17).
