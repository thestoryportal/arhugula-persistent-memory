# skills.sh eval-skill candidates: find and vet, install nothing (equip research, 2026-10-17, Claude Sonnet 5.5)

Method: skills.sh search API (`https://skills.sh/api/search?q=<term>&limit=15`, fetched 2026-10-17; the home page search box is client-rendered and returned no results to a fetch, so the JSON endpoint was the source of install counts), then `gh api` for repo metadata, file trees, SKILL.md text and last-commit dates of each SKILL.md path. Install counts are as shown by that API on 2026-10-17. Stars, license, owner type come from `gh api repos/<owner>/<repo>`. "Owner verified" = GitHub shows the owner as an Organization; I did not see any skills.sh verification badge in what I fetched (UNVERIFIED whether skills.sh has one). Nothing was installed or run.

## 1. How skills are found here (local)

- Local find-skills: `/Users/robertrhu/.claude/skills/find-skills/SKILL.md`. Names "Three Marketplaces" (line 21): skills.sh via the `skills` CLI (lines 25-36), agentskill.sh via `/learn:learn` (38-51), skillsmp.com REST API with `SKILLSMP_API_KEY` (53-55). Line 27: "Use `skills` directly, NOT `npx skills`. The `npx skills` invocation fails." Yet lines 72 and 116 still say `npx skills find` / `npx skills add <owner/repo@skill> -g -y` (internal inconsistency in the file). Quality gate, lines 83-87: prefer 1K+ installs, "Be cautious with anything under 100", trusted sources `vercel-labs`, `anthropics`, `microsoft`, repos "<100 stars should be treated with skepticism". Install is `-g -y` (global, no confirmation) at line 116: a reviewer should know this skips the prompt.
- Local skill-creator: 26 cached copies exist (`find ~/.claude -name SKILL.md -path '*skill-creator*'`). Canonical one read: `/Users/robertrhu/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/SKILL.md`. It creates, edits, evals and packages skills ("measure skill performance", description line 3; packaging to a `.skill` file, line 416). It ships `agents/`, `assets/`, `eval-viewer/`, `references/`, `scripts/`. `grep -n -i -E 'skills\.sh|marketplace|npx|install'` over it finds only line 34 (jargon aside), 416, 439, 440 (all about the local `.skill` file); and across all 26 copies `grep -i 'skills.sh\|npx skills'` returned nothing. Conclusion: skill-creator does NOT connect to skills.sh. (Note: skills.sh itself lists `anthropics/skills/skill-creator`, 408,145 installs, i.e. same skill distributed there.)
- `skills` CLI: `which skills` -> "skills not found" (so the Volta binary find-skills line 25 mentions is not on PATH in this shell). `npx --no-install skills --help` -> `npm error npx canceled due to missing packages and no YES option: ["skills@1.7.2"]`. Not cached; not installed by me.
- Local skills already present in `~/.claude/skills` relevant to this topic (from `ls`): `benchmark`, `benchmark-models`, `skill-scenario-generator` (+ `-workspace`), `context-save`, `context-restore`, `learn`, `marimo-notebook`, `marimo-pair`, `marimo-batch`, `jupyter-to-marimo`, `streamlit-to-marimo`, `implement-paper(-auto)`, `auto-paper-demo`, `anywidget-generator`, `wasm-compatibility`, `add-molab-badge`, `infranodus-gap-audit`, `icm-workspace`, `icm-architect`, `atomic-ticketizer`, `skillify`. The marimo-team set is already installed locally.

## 2. Searches run (skills.sh API, 2026-10-17)

Terms: eval, promptfoo, llm-as-judge, context-engineering, agent-memory, marimo, benchmark, trajectory, test-scenarios. Notes: "benchmark" and "trajectory" returned mostly noise (golang-benchmark, sales, single-cell); the only trajectory-relevant hit is `langsmith-dataset` (dataset types include "trajectory") and `ruvnet/ruflo/reasoningbank-with-agentdb` (1,132 installs, not vetted, see Open questions). "eval" ranking is dominated by unrelated high-install skills (Azure, Prisma), so install count alone is a poor relevance signal (INFERENCE). Many promptfoo skills exist; the official ones have low counts (333 and under).

## 3. Candidates (best first for our program; 15)

Fields: URL = `https://skills.sh/<id>`. All are plain-markdown skills unless a script is named. "Net/code" = what could run code or call the network.

### C1. hamelsmu/evals-skills (6 skills: error-analysis, write-judge-prompt, validate-evaluator, eval-audit, build-review-interface, generate-synthetic-data; also evaluate-rag)
- URL: https://skills.sh/hamelsmu/evals-skills/write-judge-prompt (775 installs; other five skills' counts not retrieved, UNVERIFIED). Repo https://github.com/hamelsmu/evals-skills, owner hamelsmu (User, not org; owner-verified: no). 1,678 stars, MIT, repo pushed 2026-08-16. SKILL.md last commits: 2026-03-03 (judge, error-analysis, eval-audit), 2026-06-10 (validate-evaluator).
- Says (write-judge-prompt): "Design LLM-as-Judge evaluators for subjective criteria that code-based checks cannot handle... Do NOT use when the failure mode can be checked with code (regex, schema validation, execution tests)." error-analysis: "systematically identify and categorize failure modes in an LLM pipeline by reading traces". eval-audit: "Audit an LLM eval pipeline and surface problems: missing error analysis, unvalidated judges, vanity metrics". validate-evaluator: "Calibrate an LLM judge against human labels using data splits, TPR/TNR, and bias correction".
- Ships: markdown only per tree (`skills/*/SKILL.md`). Net/code: validate-evaluator line 183 suggests `pip install judgy` (a suggestion in text, not run by the skill); eval-audit links hamel.dev posts and arXiv 2404.12272.
- Vet: read all six SKILL.md for stack assumptions (they assume traces + human labelling of a product LLM pipeline; our "pipeline" is the build belt); check no instruction to install packages without asking; scope overlap with local `skill-scenario-generator` (test cases) and `benchmark*` (gstack perf). Single individual author, not an org.

### C2. promptfoo/promptfoo `promptfoo-evals` (and siblings promptfoo-provider-setup, promptfoo-redteam-*)
- URL: https://skills.sh/promptfoo/promptfoo/promptfoo-evals (333 installs). Repo https://github.com/promptfoo/promptfoo, owner promptfoo (Organization, owner-verified: GitHub org yes). 26,089 stars, MIT, pushed 2026-10-17. SKILL.md last commit 2026-09-12.
- Says: "Write, run, and improve non-redteam Promptfoo eval suites for a configured target: test cases, assertions, rubrics, datasets, and CI gates."
- Ships: `plugins/promptfoo/skills/promptfoo-evals/{SKILL.md, agents/openai.yaml, references/eval-patterns.md}`; also `.claude/skills/promptfoo-evals/` with `references/cheatsheet.md`.
- Net/code: instructs `npx promptfoo validate config`, `npx promptfoo eval -c ... -o output.json --no-cache --no-share` (SKILL.md ~lines 62-72) and "Install or upgrade with `npx promptfoo@latest` only when needed"; `--env-file .env` "only when needed". Runs code and calls provider APIs when used.
- Vet: the `@latest` upgrade instruction (unpinned npx); `--no-share` present (good); `agents/openai.yaml` content (Codex-side metadata); that evals call model APIs with our keys; overlap: none installed locally (promptfoo is named in the program spec, INFERENCE).

### C3. daymade/claude-code-skills `promptfoo-evaluation`
- URL: https://skills.sh/daymade/claude-code-skills/promptfoo-evaluation (1,519 installs; copies exist at 4 installs under other owners, do not use). Repo https://github.com/daymade/claude-code-skills, owner daymade (User). 1,472 stars, MIT, pushed 2026-10-17. SKILL.md last commit 2026-03-02.
- Says: "Configures and runs LLM evaluation using Promptfoo framework. Use when setting up prompt testing, creating evaluation configs (promptfooconfig.yaml), writing Python custom assertions, implementing llm-rubric for LLM-as-judge, or managing few-shot examples in prompts."
- Ships: `SKILL.md` (447 lines), `references/promptfoo_api.md`, `scripts/metrics.py` (Python script, not read; could not confirm what it runs).
- Net/code: `npx promptfoo@latest init/eval/view`; mentions `apiBaseUrl: https://your-relay.example.com/api` (example) and "Default grader uses available API keys (OpenAI -> Anthropic -> Google)" (line ~201).
- Vet: read `scripts/metrics.py`; unpinned `@latest`; third-party relay example; duplicate of C2 in scope (C2 is the upstream/official source, INFERENCE: prefer reviewing C2 first).

### C4. langchain-ai/langsmith-skills `langsmith-evaluator` and `langsmith-dataset`
- URLs: https://skills.sh/langchain-ai/langsmith-skills/langsmith-evaluator (4,851), https://skills.sh/langchain-ai/langsmith-skills/langsmith-dataset (4,710). Repo https://github.com/langchain-ai/langsmith-skills, owner langchain-ai (Organization). 163 stars, MIT, pushed 2026-10-17. SKILL.md last commit 2026-09-18.
- Says (evaluator): "Creating Evaluators - LLM-as-Judge, custom code; ... Defining Run Functions - how to capture outputs and trajectories from your agent; ... Running Evaluations - locally with evaluate() or auto-run via LangSmith. Uses the langsmith CLI tool." (dataset): "Covers dataset types (final_response, single_step, trajectory, RAG), CLI management commands, SDK-based creation, and example management."
- Ships: markdown only (`config/skills/<name>/SKILL.md`; 495 and 331 lines).
- Net/code: requires `LANGSMITH_API_KEY`, `OPENAI_API_KEY`; text includes `curl -fsSL https://cli.langsmith.com/install.sh | sh` and `curl -sSL https://raw.githubusercontent.com/langchain-ai/langsmith-cli/main/scripts/install.sh | sh` (pipe-to-shell), `pip install langsmith ...`, `langsmith trace export` (sends/receives traces from a hosted service).
- Vet: whole approach is vendor-hosted (LangSmith); our traces are local transcripts (INFERENCE: mostly useful as a reference for the trajectory/dataset taxonomy, not as a dependency); pipe-to-shell installers; data-exfiltration question if traces are uploaded.

### C5. wshobson/agents `llm-evaluation`
- URL: https://skills.sh/wshobson/agents/llm-evaluation (12,512). Repo https://github.com/wshobson/agents, owner wshobson (User). 40,969 stars, MIT, pushed 2026-10-17. SKILL.md last commit 2026-05-22.
- Says: "Implement comprehensive evaluation strategies for LLM applications using automated metrics, human feedback, and benchmarking."
- Ships: `SKILL.md` (145 lines), `references/details.md`. Risk grep of SKILL.md found no curl/npx/pip/key lines.
- Vet: generic (BLEU/ROUGE-style metrics, A/B testing) rather than agent-specific (INFERENCE from description; body not fully read); check for stale advice on LLM-as-judge bias.

### C6. affaan-m/ECC `eval-harness`
- URL: https://skills.sh/affaan-m/ecc/eval-harness (10,600). Repo https://github.com/affaan-m/ECC (renamed; skills.sh id says `ecc`), owner affaan-m (User). 282,384 stars, MIT, pushed 2026-10-15. SKILL.md (`.agents/skills/eval-harness/`) last commit 2026-09-18.
- Says: "Formal evaluation framework for Claude Code sessions implementing eval-driven development (EDD) principles. Use when a Claude Code workflow needs a formal eval before it is trusted or changed." Frontmatter `allowed-tools: Read, Write, Edit, Bash, Grep, Glob`.
- Ships: SKILL.md (236 lines), `agents/openai.yaml`, and an `examples/eval-harness/` set: `run-example.js`, `gate.config.json`, `taskset.json`, `variants/{baseline,candidate,reward-hack}/run.js`. A "reward-hack" variant exists (interesting as an anti-gaming test).
- Net/code: the skill grants Bash; example `run.js` files execute Node code.
- Vet: read `run-example.js` and the variants; the Bash grant; unusually large repo (282K stars, a bundle of hundreds of skills, INFERENCE: install a single skill, not the bundle); overlap with local `benchmark*` is low.

### C7. affaan-m/ECC `agent-eval`
- URL: https://skills.sh/affaan-m/ecc/agent-eval (9,236). Same repo/owner/license as C6. `skills/agent-eval/SKILL.md` last commit 2026-08-12.
- Says: "Head-to-head comparison of coding agents (Claude Code, Aider, Codex, etc.) on custom tasks with pass rate, cost, time, and consistency metrics."
- Ships: SKILL.md; line 49-82: "Each agent run gets its own git worktree" created "from the specified commit" (isolation without Docker). Frontmatter tools include Bash.
- Vet: creates git worktrees and runs agent CLIs (changes repo state; conflicts with our worktree discipline and branch hygiene, see CLAUDE.md section 9); check cleanup of worktrees; cost of repeated agent runs.

### C8. github/awesome-copilot `agentic-eval`
- URL: https://skills.sh/github/awesome-copilot/agentic-eval (10,201). Repo https://github.com/github/awesome-copilot, owner github (Organization). 40,129 stars, MIT, pushed 2026-10-16. SKILL.md last commit 2026-01-19.
- Says: "Patterns and techniques for evaluating and improving AI agent outputs... self-critique and reflection loops; evaluator-optimizer pipelines; test-driven code refinement; rubric-based or LLM-as-judge evaluation systems."
- Ships: SKILL.md only (189 lines); no network or install lines found by grep.
- Vet: it is about iterative self-improvement of outputs (generation-time critique), not measuring an agent baseline (INFERENCE from description); older (Jan 2026).

### C9. muratcankoylan/Agent-Skills-for-Context-Engineering (skills `evaluation`, `advanced-evaluation`, `filesystem-context`, `context-compression`, `context-degradation`, `harness-engineering`, `context-optimization`)
- URLs: https://skills.sh/muratcankoylan/agent-skills-for-context-engineering/context-engineering-collection (4,128; the collection entry). Copies of `evaluation` / `advanced-evaluation` appear under `shipshitdev/skills` (169 / 184 installs): use the original. Repo owner muratcankoylan (User). 18,153 stars, MIT, pushed 2026-10-12. `evaluation` last commit 2026-06-29; `filesystem-context` 2026-10-01.
- Says (evaluation): "building agent evaluation systems: deterministic checks, regression suites, multi-dimensional rubrics, quality gates, production monitoring, baseline comparison, and outcome measurement for agent pipelines." (filesystem-context): "durable scratchpads, tool-output offloading, just-in-time discovery, cross-agent handoff files, filesystem memory, or cleanup policies for context stored outside the prompt."
- Ships: Python scripts: `evaluation/scripts/evaluator.py`, `advanced-evaluation/scripts/evaluation_example.py`, `filesystem-context/scripts/filesystem_context.py`, `context-compression/scripts/compression_evaluator.py` (+ tests), `context-degradation/scripts/degradation_detector.py`, `context-optimization/scripts/compaction.py`, `context-fundamentals/scripts/context_manager.py`. `evaluator.py` imports only `typing, dataclasses, enum, time, re, random` (grep of imports; no `requests`/`subprocess`).
- Vet: scripts are teaching examples (INFERENCE); confirm nothing executes on load; collection is large, pick skills individually; overlap with our own ICM context routing (`icm-workspace`, `icm-architect`) and `context-save/restore`.

### C10. addyosmani/agent-skills `context-engineering`
- URL: https://skills.sh/addyosmani/agent-skills/context-engineering (55,000). Repo https://github.com/addyosmani/agent-skills, owner addyosmani (User). 107,810 stars, MIT, pushed 2026-10-13. SKILL.md last commit 2026-09-07.
- Says: "Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, or when you need to configure rules files and context for a project."
- Ships: SKILL.md (353 lines); repo also has `evals/cases/context-engineering.json` and `evals/fixtures/context-engineering/context-audit.md` (the author evals his own skill; useful as an example of skill-level evals).
- Net/code: grep found only example commands (`npx tsc --noEmit`, "Never commit .env files or secrets") inside rule-file examples.
- Vet: generic web-dev rules-file advice (INFERENCE); direct overlap with our `CLAUDE.md` + ICM `CONTEXT.md` routing, which is more specific; check for advice that contradicts the repo's "signpost, not rules" CLAUDE.md design.

### C11. marimo-team/marimo-pair `marimo-pair` (and `retro-marimo-pair`)
- URL: https://skills.sh/marimo-team/marimo-pair/marimo-pair (12,195); https://skills.sh/marimo-team/marimo-pair/retro-marimo-pair (4,253). Repo https://github.com/marimo-team/marimo-pair, owner marimo-team (Organization). 428 stars, Apache-2.0, pushed 2026-09-16. SKILL.md last commit 2026-09-16.
- Says: "Drive a live marimo notebook as a workspace: run Python in the same kernel the user does, inspect live notebook state, and commit durable notebook changes." `allowed-tools: Bash(bash **/scripts/discover-servers.sh *), Bash(bash **/scripts/execute-code.sh *), Read`.
- Ships: `scripts/discover-servers.sh`, `scripts/execute-code.sh`, `reference/*.md`.
- Vet: scripts run arbitrary Python in a live kernel by design (execute-code.sh); `marimo-pair` is ALREADY installed locally, so the review is whether our local copy matches this version (diff by hash). Other marimo-team skills (`marimo-notebook` 5,794, `marimo-batch` 3,583, etc.) are also already local.

### C12. Arize-ai/arize-skills `arize-evaluator`
- URL: https://skills.sh/arize-ai/arize-skills/arize-evaluator (3,010). Repo https://github.com/Arize-ai/arize-skills, owner Arize-ai (Organization). 65 stars, MIT, pushed 2026-10-16. SKILL.md last commit 2026-10-16.
- Says: "Handles LLM-as-judge and code evaluator workflows on Arize including creating/updating evaluators, running evaluations on spans or experiments... Requires the ax CLI and a configured Arize profile".
- Ships: SKILL.md (446 lines) + `references/{ax-profiles,ax-setup,cli-reference,troubleshooting}.md`. Line 27: "Never read `.env` files or search the filesystem for credentials."
- Vet: vendor-locked to the Arize platform and `ax` CLI (needs account + API key); low stars (65, under find-skills' stated 100-star caution line). Likely useful only as a reference of an evaluator lifecycle (INFERENCE).

### C13. phuryn/pm-skills `test-scenarios`
- URL: https://skills.sh/phuryn/pm-skills/test-scenarios (2,815). Repo https://github.com/phuryn/pm-skills, owner phuryn (User). 27,146 stars, MIT, pushed 2026-10-16. SKILL.md last commit 2026-03-03.
- Says: "Create comprehensive test scenarios from user stories with test objectives, starting conditions, user roles, step-by-step actions, and expected outcomes."
- Ships: SKILL.md (86 lines) at `pm-execution/skills/test-scenarios/` plus a command file.
- Vet: written for product QA from user stories, not agent evals (INFERENCE); overlaps local `skill-scenario-generator` (ADF testable_prompts). Low value for us.

### C14. sickn33/agentic-awesome-skills `agent-memory-systems`
- URL: https://skills.sh/sickn33/agentic-awesome-skills/agent-memory-systems (1,984). Repo owner sickn33 (User), 47,775 stars, MIT, pushed 2026-10-17. SKILL.md last commit 2026-10-14. Frontmatter: `source: vibeship-spawner-skills (Apache 2.0)`, `risk: safe` (self-declared).
- Says: "Design tenant-scoped memory, retrieval and retention for agents. Use when planning RAG, conversation history, vector stores or remembering across sessions."
- Ships: SKILL.md (39 lines) + `references/detailed-guide.md`. Repo is a mass aggregation (copies of this skill appear under 3 plugin directories).
- Vet: provenance chain (aggregator of another source) and the self-declared "risk: safe" is not evidence; thin SKILL.md; RAG/vector oriented, ours is repo-file memory (INFERENCE).

### C15. rohitg00/agentmemory (skills `remember`, `recall`, `handoff`, `agentmemory-*`)
- URLs: https://skills.sh/rohitg00/agentmemory/remember (13,666), `/recall` (13,572), `/agentmemory-architecture` (10,402), `/agentmemory-hooks` (10,394). Repo https://github.com/rohitg00/agentmemory, owner rohitg00 (User). 29,620 stars, Apache-2.0, pushed 2026-10-16.
- Says (handoff): "Resume the most recent agent session for the current working directory, leading with any unanswered question."
- Ships: a plugin, not just markdown: `plugin/.claude-plugin/plugin.json`, `plugin/hooks.json`, `plugin/hooks/hooks.{codex,copilot,antigravity,devin}.json`, plus REST API and MCP-tools skills (names `agentmemory-rest-api`, `agentmemory-mcp-tools`). I did not read the hooks or the server code.
- Vet: HIGHEST RISK in this list. Hooks fire on every session and capture session content; a REST/MCP memory server implies a daemon and a data store; decide where transcripts go (could contain secrets or case material); conflicts with our own planned memory consolidation design; overlaps local `context-save`/`context-restore`, and `memento:*`.

## Recommendation inputs

Not recommendations to install. MAESTRO decides after vetting.

Overlap with local skills (both named):
- C11 marimo-pair / marimo-team skills vs local `marimo-pair`, `marimo-notebook`, `marimo-batch`, `jupyter-to-marimo`, `streamlit-to-marimo`, `implement-paper`, `anywidget-generator`: already installed, nothing to add; only compare versions.
- C13 test-scenarios vs local `skill-scenario-generator` (ADF testable_prompts).
- C6/C7/C3/C2 (eval harness / promptfoo) vs local `benchmark` and `benchmark-models` (gstack performance/cross-model benchmarks, INFERENCE from their descriptions in the session skill list) and `skill-creator` (has its own eval runner and `eval-viewer`, `agents/`): partial overlap on "run evals of a skill/prompt".
- C10, C9 (`context-engineering`, `filesystem-context`) vs local `icm-workspace`, `icm-architect`, `context-save`, `context-restore`, plus repo `CLAUDE.md` routing.
- C15, C14 (agent memory) vs local `context-save`/`context-restore` and the `memento:*` skills.

Likely gaps (INFERENCE; no local skill covers these):
- LLM-as-judge design and calibration against human labels (C1 write-judge-prompt, validate-evaluator; none local). The calibration step (TPR/TNR on a held-out human-labelled split) is the part most relevant to "scientifically durable" evals.
- Error analysis from traces / eval audit (C1 error-analysis, eval-audit): matches step 2-3 of the charter (measure baseline from history, find causes). Our "traces" are Claude/Codex transcripts.
- A declarative eval runner with CI gates (C2 promptfoo-evals), which can drive both Claude and OpenAI models (INFERENCE: promptfoo supports multiple providers; not verified here).
- Anti-gaming eval example (C6 `variants/reward-hack`).
- Trajectory dataset taxonomy (C4 langsmith-dataset: final_response, single_step, trajectory, RAG), as a reference only.

Cautions from this survey:
- Install count is weak evidence: top "eval" hits (Azure, Prisma, rigorpilot at ~460K) are unrelated; relevant eval skills sit at 100-12K.
- Only C2, C4, C8, C11, C12 have GitHub Organization owners; the rest are individuals.
- Several candidates carry unpinned `npx ...@latest` or pipe-to-shell installer text (C2, C3, C4); `find-skills` itself installs with `-g -y`.
- Nothing here uses Codex-specific format, but C2, C6 ship `agents/openai.yaml`, so they are the ones with explicit Codex-side metadata.

## Open questions for MAESTRO

1. Is the `skills` CLI meant to be reachable (not on PATH here, and `npx --no-install` says `skills@1.7.2` is not cached)? find-skills line 27 says it is a "Volta global binary".
2. Do you want the C1 skills vetted line by line first? They are the closest match to the charter (judge validation, error analysis) and are markdown-only.
3. Should the review also cover `ruvnet/ruflo/reasoningbank-with-agentdb` (1,132 installs) and `neolabhq/context-engineering-kit` (many skills at ~1.3K installs, including `judge-with-debate`, `memorize`, `reflect`)? I saw them in search results but did not vet them.
4. skills.sh per-skill pages and any security-audit data ("Audits" section on the site) were not read; whether to check them before install is your call.

## Sources

1. https://skills.sh (home; fetched 2026-10-17): leaderboard tabs, sections Packs, Topics, Official, Audits, Docs.
2. https://skills.sh/api/search?q=eval | promptfoo | llm-as-judge | context-engineering | agent-memory | marimo | benchmark | trajectory | test-scenarios (fetched 2026-10-17): install counts.
3. `gh api repos/<owner>/<repo>` for each repo (2026-10-17): stars, license, owner type, pushed_at.
4. `gh api repos/<repo>/git/trees/main?recursive=1` and `.../contents/<path>` raw SKILL.md, `.../commits?path=<path>` (2026-10-17): files, text, last-commit dates.
5. https://github.com/hamelsmu/evals-skills ; https://github.com/promptfoo/promptfoo ; https://github.com/daymade/claude-code-skills ; https://github.com/langchain-ai/langsmith-skills ; https://github.com/wshobson/agents ; https://github.com/affaan-m/ECC ; https://github.com/github/awesome-copilot ; https://github.com/addyosmani/agent-skills ; https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering ; https://github.com/marimo-team/marimo-pair ; https://github.com/Arize-ai/arize-skills ; https://github.com/phuryn/pm-skills ; https://github.com/sickn33/agentic-awesome-skills ; https://github.com/rohitg00/agentmemory
6. Local: `/Users/robertrhu/.claude/skills/find-skills/SKILL.md` lines 21-119; `/Users/robertrhu/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/SKILL.md`; commands `which skills`, `npx --no-install skills --help`.
