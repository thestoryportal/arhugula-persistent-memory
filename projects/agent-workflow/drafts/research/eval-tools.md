# Eval tools we have or can get: promptfoo, marimo, local skills (equip research, 2026-10-17, Claude Sonnet 5.5)

M = /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory. Doc pages were read 2026-10-17 via WebFetch (summaries by a small model; quoted phrases are from those summaries, so re-check wording on the page before pinning a rule). Source numbers are in `## Sources`.

## promptfoo

### Installed?
- `command -v promptfoo` printed nothing, exit 1. NOT installed globally.
- `npx --no-install promptfoo --version` output: `npm error npx canceled due to missing packages and no YES option: ["promptfoo@0.124.1"]`. NOT in any local node_modules. (INFERENCE: 0.124.1 is the version npx would resolve; not verified against the registry.)
- Nothing was installed. Install paths per the docs [1]: `npx promptfoo@latest ...` (no install), `npm install -g promptfoo`, `brew install promptfoo`. The docs page does not state a Node version [1]. Agent providers need extra SDK packages: the Claude Agent SDK page says to install `@anthropic-ai/claude-agent-sdk@^0.3.273` alongside promptfoo [2] (UNVERIFIED for the OpenAI side, see [3]).

### How it evaluates agents, not only prompts
Core model: `promptfooconfig.yaml` defines `prompts`, `providers`, `tests` (with `vars` and `assert`) [1][8].

Agent providers:
| Provider | Id | Source |
|---|---|---|
| Claude Agent SDK / Claude Code | `anthropic:claude-agent-sdk`, alias `anthropic:claude-code` | [2] |
| OpenAI Codex SDK | `openai:codex-sdk` (alias `openai:codex`), optional `:<model>` suffix | [3] |
| Shell command | `exec: python chain.py` (script gets 3 args: prompt, options JSON, context JSON; stdout is the response) | [5] |
| Python / JavaScript custom providers | exist as separate pages (a `python` provider page and an `ApiProvider` guide); the exec page "does not document a `file://` config shape" | [5] |

- The Claude Agent SDK provider page: default is "a temporary directory with no tools enabled"; with `working_dir` it is "read-only access" (Read, Grep, Glob, LS) unless tools are widened with `append_allowed_tools`, `permission_mode` etc. `copy_working_dir: true` runs each step in a fresh copy of the directory. Limits: `max_turns`, `max_budget_usd`. `apiKeyRequired: false` "to use a local Claude Code session". Session ids are returned and can be resumed (`resume`, `continue`, `fork_session`). Also `skills`, `plugins`, `mcp`, `output_format` (JSON schema) [2].
- The Codex SDK page: options `working_dir` (must be in a Git repo unless `skip_git_repo_check: true`), `sandbox_mode` (`read-only`, `workspace-write` default, `danger-full-access`), `approval_policy`, `model_reasoning_effort`, `output_schema`, `persist_threads`, `thread_pool_size`, `enable_streaming`, `deep_tracing`. "Provider-level config is validated strictly, so a typo such as `sandboxMode` can fail provider loading." [3]
- No dedicated page exists for a "Claude Code" provider (`/docs/providers/claude-code/` returned 404); the alias on the Agent SDK page covers it [2].
- The exec provider page "does not discuss agents" [5]. A headless `claude -p` or `codex exec --json` run could be wrapped as an `exec:` provider (INFERENCE; not tested, and stdout-only means tool-call metadata would be lost unless the script prints it into the response text).

### Assertion types usable on agent runs [4]
Exact names from the assertion list page:
- Code graders: `javascript`, `python`, `ruby` ("runs a ... function that validates the output"), `contains`, `regex`, `equals`, `is-json`, `cost`, `latency`, `webhook`.
- Tool and trajectory: `tool-call-f1`, `is-valid-function-call`, `skill-used` ("checks that expected skills appear in provider skill metadata"), `trajectory:tool-used`, `trajectory:tool-args-match`, `trajectory:tool-sequence`, `trajectory:step-count`, `trace-span-count`, `trace-span-duration`, `trace-error-spans`.
- Model-graded: `llm-rubric`, `g-eval`, `factuality`, `model-graded-closedqa`, `select-best`, `trajectory:goal-success` ("an LLM judge decides whether a traced run reached its goal"), `pi`.
- Grouping and negation: `assert-set` (optional threshold); "Any type can be negated by prefixing `not-`".
- Claude Agent SDK tool calls appear in `response.metadata.toolCalls` (fields `id`, `name`, `input`, `output`, `is_error`, `parentToolUseId`); inspect them with a `javascript` assertion or `skill-used`. With tracing on there is a `gen_ai.turn N` span per round trip; `trace-span-count` can cap turns [2].
- Codex: shell, MCP, search and file steps are traced "when `enable_streaming` is on" and checkable with `trajectory:step-count`, `trajectory:tool-used`, `trajectory:tool-args-match`. `metadata.skillCalls` "is heuristic, inferred from commands that read `SKILL.md` files" [3]. Relevance to us: a "did the builder read the right CONTEXT.md" check could be a `javascript` or `trajectory:tool-args-match` assertion on file reads (INFERENCE).
- `llm-rubric` [9]: example `value: Is not apologetic and provides a clear, concise answer`; grader override by CLI `--grader`, `defaultTest.options.provider`, or per-assertion `provider` (precedence assertion, then test, then defaultTest); `threshold` 0.0 to 1.0; grader returns JSON `reason`, `score`, `pass`; prompt replaceable via `defaultTest.options.rubricPrompt` with `{{output}}` and `{{rubric}}`. Relevance: lets us set a different-family grader than the worker (C8 judge-collision rule, see section 3).
- Test-level `threshold`: "Test will fail if the combined score of assertions is less than this number" [8].

### Repeats and per-trial results
- Config: `evaluateOptions.repeat`, "Number of times to run each test case. Defaults to 1"; `commandLineOptions.repeat` sets a CLI default. The reference page "doesn't document a `--repeat` flag" [8].
- The CLI page lists `--repeat <number>`: "Number of times to run each test" [6]. The two pages disagree on the flag; verify with `promptfoo eval --help` after the operator approves an install (UNVERIFIED which is current).
- Per-trial result shape: the outputs page "doesn't document a repeat option or per-trial results" [7]. UNVERIFIED how repeats appear in JSON; assume one result row per repeat and check with a positive control before relying on it.
- Caveat for agents: Claude Agent SDK responses are cached on prompt + config + working-dir files, so repeats of an identical test can return the cached answer; "Calls using `copy_working_dir` are never cached" [2]. Use `--no-cache` / `PROMPTFOO_CACHE_ENABLED=false` / `options.bustCache: true` for real repeated trials [2][3][6].

### Caching
- On by default, `evaluateOptions.cache` (default true) [8]; CLI `--no-cache` "Do not read or write results to disk cache" [6]; disk cache in a `cache` folder under `PROMPTFOO_CONFIG_DIR` (default `~/.promptfoo`) [6]; CI: `PROMPTFOO_CACHE_PATH`, `PROMPTFOO_CACHE_TTL` [10].
- Claude Agent SDK: with MCP servers configured caching is off unless `cache_mcp: true` [2]. Codex: cache key includes prompt, working dir, model, output schema, sandbox mode, reasoning effort, network and approval settings [3].

### Output formats
- `-o/--output` accepts csv, txt, json, jsonl, yaml, yml, html, xml, junit.xml, several `-o` allowed [6][7][10]. JSON top-level: `version`, `timestamp`, `results` (`prompts`, `providers`, `outputs`, `stats`) [7]. `promptfoo eval` with no output flag opens the "Interactive web viewer (default)"; `promptfoo view` is "Local-only (no data sent externally)" [7].
- Export: `promptfoo export eval <evalId>` writes JSON [6].

### CI use
- GitHub Actions example: `npx promptfoo@latest eval -c promptfooconfig.yaml --share -o results.json -o report.html`; fail threshold via `--fail-on-error` or a `jq` pass-rate check; upload artifacts `if: always()` [10].
- Exit code 100 "when there is at least 1 test case failure" (also below `PROMPTFOO_PASS_RATE_THRESHOLD`); `PROMPTFOO_FAILED_TEST_EXIT_CODE` overrides [6].
- `--share` creates a shareable URL (sends data off-machine; leave off for our repo, `--no-share` overrides config) [6].

### Storing results over time
- Local history directory: `PROMPTFOO_CONFIG_DIR`, "Directory that stores eval history", default `~/.promptfoo` [6]. `commandLineOptions.write` (default true) controls saving to that directory; `writeLatestResults: true` makes them appear in the web UI [8]. `promptfoo list` lists evals; `promptfoo export eval <evalId>` dumps one [6]. The docs fetched do not name a database file, so SQLite is not confirmed (UNVERIFIED).
- INFERENCE for our program: keep the durable record in the repo as `-o results.jsonl` per run, plus our own run manifest, rather than relying on `~/.promptfoo` (outside git, per-user).

### Exact config shape for one agent eval
Assembled from the doc fragments [2][4][8] (not run; no install allowed). `working_dir`, `copy_working_dir`, `max_turns`, `max_budget_usd`, `permission_mode`, `sandbox`, `skills` are from [2]; `evaluateOptions.repeat` and `threshold` from [8]; `javascript`, `skill-used`, `trace-span-count`, `llm-rubric` from [4][9]. Whether `evaluateOptions.repeat` is valid inside a file that also sets `tracing` is UNVERIFIED.
```yaml
# promptfooconfig.yaml
description: builder reads its context file before editing
prompts:
  - '{{task}}'
providers:
  - id: anthropic:claude-agent-sdk
    config:
      working_dir: ./fixture-repo        # relative to this config file
      copy_working_dir: true              # fresh copy per trial, never cached
      permission_mode: acceptEdits
      max_turns: 25
      max_budget_usd: 2
      sandbox: { enabled: true }
evaluateOptions:
  repeat: 5
  cache: false
tests:
  - description: ticket T-example
    vars: { task: 'Do ticket T-example per CLAUDE.md' }
    threshold: 0.8
    assert:
      - type: javascript            # outcome in the environment/tool calls
        value: "context.providerResponse.metadata.toolCalls.some(t => t.name === 'Read' && JSON.stringify(t.input).includes('CONTEXT.md'))"
      - type: trace-span-count      # turn cap (needs tracing enabled)
        value: { pattern: 'gen_ai.turn*', max: 25 }
      - type: llm-rubric
        value: 'The change only touches files named in the ticket'
        provider: openai:gpt-5-mini   # different family than the worker
```
The `trace-span-count` value shape and the `javascript` `context` variable name are my reading, UNVERIFIED; check the assertion pages before use.

## marimo

### Installed?
- `command -v marimo` printed `/Users/robertrhu/.local/bin/marimo`; `marimo --version` printed `0.24.2`.
- `ls M/.venv/bin | grep -i marimo` printed nothing (not in the project venv). So marimo is a global tool (installed in `~/.local/bin`), not a repo dependency; a notebook that needs project packages would have to run via `uv run --with ...` or PEP 723 script metadata (the marimo-notebook skill mentions PEP 723 metadata; see below).

### What notebooks give for eval analysis
From marimo.io [11]: "Reactive execution" ("Run one cell and marimo reacts by running affected cells"); built-in SQL cells with DuckDB among the supported backends; app mode ("served as web apps via the marimo CLI or exported as WebAssembly-powered HTML"); notebooks "run as scripts locally or in pipelines"; "pure Python" `.py` files that "work with Git version control".
- Skill text confirms: `uv run marimo run <notebook.py>` for app mode [12 line 71]; `mo.ui.*` controls (slider, form, anywidget) [12]; when `pytest` is present marimo runs pytest on cells [12 line 256]; SQL has a reference file (`references/SQL.md`, line 271) [12].
- Scheduled runs: the marimo-batch skill describes "an opintionated skill to prepare a marimo notebook to make it ready for a scheduled run", with a Pydantic model as the source of truth for batch parameters [13].
- INFERENCE for us: a `.py` notebook diffs cleanly in git (unlike ipynb), reads JSONL results through duckdb, and gives an operator-facing dashboard (per-role pass rate, trial spread) with sliders for filters. Reactive cells make re-slicing one result set cheap.

### Local marimo skills
Found by `find -L ~/.claude ~/.codex ~/.agents -name SKILL.md -path '*marimo*'`. Plain `find ~/.claude ...` without `-L` returns nothing because these are symlinks (`~/.claude/skills/marimo-notebook -> ../../.agents/skills/marimo-notebook`; `marimo-pair -> /Users/robertrhu/Projects/marimo/marimo-pair`). Copies also exist under `~/.codex/skills/` (4 of them; no marimo-pair there).

| Skill | Path | Description (quoted) | Use for evals |
|---|---|---|---|
| marimo-notebook | `/Users/robertrhu/.claude/skills/marimo-notebook/SKILL.md` (277 lines) | "Write a marimo notebook in a Python file in the right format." | Author the results-analysis notebook (cell format, PEP 723, `marimo check`, SQL reference) |
| marimo-pair | `/Users/robertrhu/.claude/skills/marimo-pair/SKILL.md` | "Work inside a running marimo notebook's kernel — execute code, create cells, and build a notebook as an artifact. Use when the user wants to start a marimo notebook or work in an active marimo session." (allowed-tools: `Bash(bash **/scripts/discover-servers.sh *)`, `Bash(bash **/scripts/execute-code.sh *)`, `Read`) | Interactive exploration of a live result set with the operator watching; not for unattended runs |
| marimo-batch | `/Users/robertrhu/.claude/skills/marimo-batch/SKILL.md` (108 lines) | "An opintionated skill to prepare a marimo notebook to make it ready for a scheduled run." | Make the baseline report notebook parameterised and runnable by a script/cron (Phase 6 lasting instrument) |
| jupyter-to-marimo | `/Users/robertrhu/.claude/skills/jupyter-to-marimo/SKILL.md` | "Convert a Jupyter notebook (.ipynb) to a marimo notebook (.py)." | Not needed unless an existing ipynb appears |
| streamlit-to-marimo | `/Users/robertrhu/.claude/skills/streamlit-to-marimo/SKILL.md` | "Convert a Streamlit app to a marimo notebook" | Not needed |

(Also in the session skill list: `add-molab-badge`, `anywidget-generator`, `auto-paper-demo`, `implement-paper*`, `marimo-pair`. Only the five above have `marimo` in the path.)

## Local eval-related skills

Method: listed SKILL.md under `~/.claude/skills` (including `synced/<ids>/`), `~/.claude/plugins`, `~/.codex/skills`, then `grep -il -E "eval|scenario|benchmark|grader|judge|harness|review"`. That regex hits roughly 80+ files because "review" and "harness" are everywhere (the `synced/` set is an "agent harness council" skill pack). Below are only those that would matter to an agent-workflow eval program. `<S>` = `/Users/robertrhu/.claude/skills/synced/64b41406-d159-4623-870b-4d98e20857d0_3e2ca3e4-6f17-4aae-b6ef-6c82f5b79038`.

### Read in full: clearly about evals

**c8-eval-engineer**, `<S>/c8-eval-engineer/SKILL.md` (370 lines). Description (quoted, truncated): "Voice C8 of the agent harness council (Slate E11) — Eval Engineer. Use when the operator names C8, or for the out-of-loop, statistical, population-level eval discipline — eval-set construction, holdout design, counterfactual baselines, judge-human alignment, judge-base-model collision, gate catch-rate, Reflexion-loop convergence, routing accuracy, drift detection, regression-vs-prior-version, the Husain manual-review→categorize→automate→align loop, meta-eval, expected-HITL-invocations-per-session operator-burden primitive."
Method:
1. Every eval surfaces five fields: holdout source, split rule, leakage prevention, freshness rule, counterfactual baseline. "Single-arm claims are a quality failure (FM-H)" (lines 190-198).
2. Husain loop, four stages: manual review of 20-50 outputs per change, categorize failures into a taxonomy, automate a code assertion or LLM judge per category, align the judge with humans on a held-out set. "New automated assertions skipping the manual-review predecessor stage are a discipline failure (FM-G)" (lines 202-213).
3. Judge calibration: alignment metric (agreement, Cohen's kappa, Spearman, F1), default floors "kappa >= 0.6 categorical; F1 >= 0.75 binary; Spearman >= 0.7 ordinal" (a "proposing posture", line 224), rerun cadence on new model version/prompt/drift/quarterly, judge-base-model collision mitigated by a different-family judge or a human-aligned holdout (lines 217-229).
4. Keep drift detection (operational, time-windowed over recent traces) separate from regression testing (pre-deploy, version pair, frozen golden set) (FM-K, lines 233-244, 325).
5. Meta-eval recursion "bottoms out" at human review of a sample; every recursive case must name where humans enter (lines 248-256).
6. Primitive catalog (line 114 on) includes end-state evaluation ("explicitly recommended over turn-by-turn analysis for state-mutating agents"), tool-call correctness, gate catch-rate and false-positive rate, token-amplification ratio, and `expected_hitl_invocations_per_session` per workflow class with mean/median/p95.
7. Limits: it is a council "voice" tied to a separate harness project (references `s11-...` files in a project KB that is not in this repo); its Layer-3/C5/C7 vocabulary is overhead for us. The discipline (items 1-6) is reusable. Carries a caveat that the skill's thresholds are "proposing", not measured.

**skill-creator** (Anthropic), canonical copy `/Users/robertrhu/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator/SKILL.md` (485 lines; also 7 cached copies under `~/.claude/plugins/.../skill-creator/<hash>/` and a synced copy `<S>/skill-creator/SKILL.md`; `~/.claude/skills/skill-creator` does not exist). Description: "Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy." Folder has `agents/{grader,comparator,analyzer}.md`, `eval-viewer/`, `scripts/{run_eval,run_loop,aggregate_benchmark,generate_report,improve_description,package_skill}.py`.
Method:
1. Test cases in `evals/evals.json`, prompts first, assertions drafted while runs execute (lines 141-205).
2. Per test case, spawn with-skill and baseline subagents "in the same turn"; baseline is no-skill for a new skill or a snapshot of the old version when improving (lines 169-190). Workspace layout `<skill>-workspace/iteration-N/eval-<name>/{with_skill,old_skill}/outputs/`.
3. Capture timing/token data per run; a grader subagent (`agents/grader.md`) checks each assertion against transcript and outputs and also "critique[s] the evals themselves" ("A passing grade on a weak assertion is worse than useless"); writes `grading.json`.
4. `python -m scripts.aggregate_benchmark` produces `benchmark.json`/`benchmark.md` with pass_rate, time, tokens as mean +/- stddev and delta; then an analyst pass for patterns the aggregate hides (always-pass assertions) (lines 221-234).
5. Human review in an HTML viewer (Outputs tab, Benchmark tab), feedback saved to a JSON file, then rewrite and rerun into `iteration-N+1` (lines 253-320).
6. Optional blind comparison: two outputs to an independent agent "without telling it which is which" (`comparator.md`) (line 325-331).
7. Description optimisation loop (`run_loop.py`): 20 trigger queries, 60% train / 40% held-out split, each query run 3 times for a trigger rate, up to 5 iterations (lines 333-380).
Relevance: this is the closest existing implementation of baseline-vs-variant with repeats and variance for Claude subagents, and a trigger-eval for whether a skill/CONTEXT.md route fires. Its scripts call Claude (not read in full here; UNVERIFIED how they invoke it, `run_eval.py` not opened).

**skill-scenario-generator**, `/Users/robertrhu/.claude/skills/skill-scenario-generator/SKILL.md` (7.7 KB). Description: "Generates test scenarios for Agent Deployment Framework (ADF) skills. Use whenever the user wants to create test cases, generate scenarios, validate skill behavior, or test a skill file from the ADF." Method: read the skill, extract purpose/trigger keywords/"does not cover"/sibling skills; write four XML scenarios (happy path, edge case, ambiguous, out-of-scope/refusal targeting a named sibling), each `<purpose>` = a realistic user message plus `<evaluation><criterion>` lines for a human reviewer; checklist forbids meta-language revealing a test (e.g. "create an eval"). Hard-wired to `~/Projects/agent-deployment-framework/` paths, so it needs adaptation for us. The four-scenario shape (happy/edge/ambiguous/out-of-scope) is reusable for role-card scenarios (INFERENCE).

**harness-adversarial-reviewer**, `<S>/harness-adversarial-reviewer/SKILL.md` (390 lines). Description: "Adversarial reviewer for the multi-LLM agent harness engineering project. Use at the four checkpoint phases (P3a-CK, P3-CK, P5-CK, P6-CK) to red-team completed artifacts ... and produce a finding-classified review report". Method:
1. Read-only reviewer; output is `Adversarial_Review_NN.md` with findings in three classes (Class 3 re-open the phase, Class 2 revise current artifact, Class 1 documentation drift), each finding with Location, Defect, Discriminator, Evidence, Resolution path (lines 34-80).
2. Severity via a deterministic discriminator tree: project-commitment violation (c), requires upstream-artifact revision (b), affects current-phase substance (a); first match wins (lines 148-195).
3. Mandatory "Findings considered and rejected" section, target 8-12 substantive entries; "an empty rejected-findings list is itself a finding" (lines 81, 131).
4. Self-audit before emit: severity distribution sanity, evidence on every finding, no author-mode drift (resolution paths describe shape, not replacement text), decided/proposing/open labels (lines 133-144).
5. Cross-artifact systemic pattern rule: same finding shape in 3 or more artifacts becomes a workflow-template fix, 2 is only a candidate (lines 118-127).
6. Named failure modes of the reviewer itself (severity inflation/deflation, smoothing, empty rejected list) at lines 347-361.
Limits: tuned to a different project (ADRs, "V3 system prompt", `/mnt/skills/user/...` paths). Reusable idea for Astra/pre-review role cards and for grading reviewers: judge the reviewer by its rejected-findings transparency and planted-defect catch rate (INFERENCE).

### Skimmed (description or headings only), relevance noted
| Skill | Path | What it would give us |
|---|---|---|
| validation-contract-architect / c5-validation-contract | `<S>/validation-contract-architect/SKILL.md`, `<S>/c5-validation-contract/SKILL.md` | In-loop gate/validator contract design (the C8 skill says C5 owns gates, C8 measures them). Not read in full. |
| c7-observability | `<S>/c7-observability/SKILL.md` | Trace/span schema, the substrate C8 consumes. Not read in full. |
| orchestration-comparativist | `<S>/orchestration-comparativist/SKILL.md` | Compares orchestration designs; possible input to role-topology comparison. Not read. |
| atomic-ticketizer | `/Users/robertrhu/.codex/skills/atomic-ticketizer/SKILL.md` (also in the Claude skill list) | Description: "Use when an approved implementation plan must be cut into atomic tickets that many fresh builders implement in parallel worktree lanes, each closed and merged to master within minutes. Refuses a plan with no approval line." This is the belt we are evaluating, not an eval tool. |
| benchmark / benchmark-models (gstack) | `/Users/robertrhu/.claude/skills/benchmark/SKILL.md` (symlink to `gstack/benchmark`) | Descriptions in the session skill list: "Performance regression detection using the browse daemon" (web page perf) and "Cross-model benchmark for gstack skills". `benchmark-models` could be a pattern for same-task-different-model runs; not read, UNVERIFIED. |
| review, qa, qa-only, investigate, codex (gstack) | `/Users/robertrhu/.claude/skills/{review,qa,investigate,codex}/SKILL.md` | Product-workflow skills ("Pre-landing PR review", "Systematically QA test a web application", "Systematic debugging", "OpenAI Codex CLI wrapper"), not eval tools. They are subjects of eval (agent workflows), not instruments. |
| memento: message-in-a-bottle, next, ceiling; laws: code, prompt, prose, chat | `~/.claude/plugins/cache/memento/memento/0.7.0/skills/*`, `~/.claude/plugins/cache/promptctl/laws/0.24.1/skills/*` | Part of the system under study (handoff and craft-guidance skills), not eval tools. |

## Other tools already here

### duckdb in the project venv
`M/.venv/bin/python -c "import duckdb; print(duckdb.__version__)"` printed `1.5.6`. Can query JSONL directly (`read_json_auto`) for transcript and result analysis (INFERENCE; not run on a transcript here).

### Claude headless
- `claude --version` printed `2.1.301 (Claude Code)`. `claude --help` lists `-p, --print`, `--output-format <format>` (with `stream-json` mentioned "--print and --output-format=stream-json"), `--input-format` (print only), `--include-hook-events`, `--include-partial-messages`. Full help not read; the exact format values (text/json/stream-json) are UNVERIFIED beyond what the grep showed. Per the repo memory, `claude -p --add-dir` "eats prompt" (MEMORY.md entry "Team session launch traps"), so test before building on it.
- The Claude Agent SDK is not installed here (no check made for `@anthropic-ai/claude-agent-sdk`; promptfoo's provider needs it [2]). UNVERIFIED.

### Codex headless
`codex --version` printed `codex-cli 0.162.1`. `codex exec --help` (grep) shows: `--json` "Print events to stdout as JSONL"; `-o, --output-last-message <FILE>`; `--output-schema <FILE>` "Path to a JSON Schema file describing the model's final response shape"; `--ephemeral`; `-s, --sandbox <SANDBOX_MODE>`; `--dangerously-bypass-approvals-and-sandbox`; subcommands `resume` ("Resume a previous session by id or pick the most recent with --last") and `review` ("Run a code review against the current repository"). The existing Codex builder sessions here have `originator: codex_exec`, `source: exec` (see below), so our builders already run via `codex exec`.

### Reading Claude session transcripts
- Directory: `~/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/` (the project dir with `/` turned into `-`). Contains 44 top-level `<sessionId>.jsonl` files (`ls $D/*.jsonl | wc -l` printed 44) and per-session directories. 85 entries total in the dir (`ls | wc -l` printed 85). Per session `<sessionId>/subagents/agent-<agentId>.jsonl` plus `agent-<agentId>.meta.json`, and `<sessionId>/tool-results/<id>.txt` (large tool outputs spilled to files). `ls $D/*/subagents/*.jsonl | wc -l` printed 222 subagent transcripts.
- Record types counted in the first 3000 lines of one session (`820d41d4-...jsonl`): `assistant` 460, `attachment` 407, `user` 235, `bridge-session` 89, `mode` 88, `atis-latch` 88, `last-prompt` 87, `ai-title` 86, `queue-operation` 54, `system` 37, `file-history-delta` 23, `file-history-snapshot` 12, `artifact-comment-monitor` 2, `artifact-autoreact-ledger` 1, `cost-state` 1.
- Keys of a `user` record: `cwd, entrypoint, gitBranch, isMeta, isSidechain, message, parentUuid, sessionId, timestamp, type, userType, uuid, version`. Keys of an `assistant` record: `advisorModel, apiBlockIndex, cwd, effort, entrypoint, gitBranch, isSidechain, message, parentUuid, perTurnEffort, requestId, requestedModel, serverClassifierRequest, sessionId, session_id, thinkingDisplay, thinkingDurationMs, timestamp, type, userType, uuid, version`. `message` holds the API-style `role`/`content` blocks (not expanded here).
- `head -c 1500` of the first part of that file shows setup records first: `{"type":"mode","mode":"normal","sessionId":...}`, `{"type":"bridge-session",...,"bridgeSessionId":...}`, `{"type":"file-history-snapshot",...}`, then an `attachment` record with `"hookName":"SessionStart:clear"` and a hook stdout payload.
- Subagent file: `.meta.json` is `{"agentType":"general-purpose","description":"Walk test of TICKETS guide","toolUseId":"toolu_...","spawnDepth":1,"requestShape":"background","requestNonInteractive":true,"model":"sonnet"}`. The first record of the `.jsonl` has `"isSidechain":true`, `promptId`, `agentId`, `type:"user"`, `message.content` = the full prompt the parent wrote. So the exact brief given to each subagent, its model, and its description are recoverable. Useful for measuring "what did the orchestrator hand over".
- Caution: a session file can hold a context-clear boundary (`SessionStart:clear` hook) and MAESTRO's reset via memento starts new session ids; linking sessions into one ticket needs `bridgeSessionId`/branch/cwd (INFERENCE).

### Reading Codex session transcripts
- Directory: `~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-<timestamp>-<uuid>.jsonl`. Year dirs `2025`, `2026`; 2026 months `03 04 06 07 08 09 10`. `find ~/.codex/sessions -name '*.jsonl' | wc -l` printed 6081 files.
- One recent builder file (`2026/10/14/rollout-2026-10-14T16-12-41-01a13c79-...jsonl`, cwd `/Volumes/memit/llmdb-lanes/T002`): line 1 is `{"timestamp":..., "ordinal":0, "type":"session_meta","payload":{creator_user_id, creator_account_id, session_id, id, timestamp, cwd, runtime_workspace_roots, originator:"codex_exec", cli_version:"0.162.1", source:"exec", thread_source:"user", model_provider:"openai", base_instructions:{text:...}, ...}}`. Top-level keys: `timestamp`, `ordinal`, `type`, `payload`.
- Counts of (type, payload.type) in the first 4000 lines: `event_msg/item_completed` 74, `token_usage_record` 23, `event_msg/token_count` 23, `response_item/custom_tool_call` 22, `response_item/custom_tool_call_output` 22, `response_item/reasoning` 21 (content is `encrypted_content`), `response_item/message` 11, `session_meta` 1, `event_msg/task_started` 1, `world_state` 1, `turn_context` 1, `event_msg/task_complete` 1.
- Payload keys: `task_started`: `collaboration_mode_kind, model_context_window, root_turn_id, started_at, turn_attribution, turn_id`; `turn_context`: `approval_policy, cwd, effort, model, sandbox_policy, permission_profile, ...`; `custom_tool_call`: `call_id, id, input, name, status, type`; `item_completed`: `completed_at_ms, item, started_at_ms, thread_id, turn_id`. So per-turn model, effort, sandbox, tool calls with timings, and token counts are all in the file. Reasoning text is encrypted (not readable).
- An older file (2025-12-20, cli 0.73.0) has a different shape (`session_meta` without `ordinal`, `git` block, `response_item` messages, `event_msg`), so a parser must tolerate version differences.

## Fit for our program

Phase 2 = baseline (measure historical and current behavior); Phase 6 = lasting evals. "Setup" means what must happen before it works. Costs are INFERENCE unless cited.

| Tool | Phase 2 (baseline) | Phase 6 (lasting evals) | Cost | Setup needed |
|---|---|---|---|---|
| duckdb 1.5.6 in `M/.venv` | Query Claude and Codex jsonl for tool calls, file reads, turn counts, token use per role/ticket; no new inference | Same queries as scheduled analysis over new transcripts | Free, local | Write the parsers (record shapes above); none to install |
| marimo 0.24.2 (global) | Notebook over the baseline tables: per-role distributions, flagged outliers | `marimo-batch`-style parameterised report + app-mode dashboard for the operator | Free | Run through `uv run --with` or PEP 723 deps since not in `M/.venv`; use marimo-notebook skill |
| `claude -p` / `codex exec --json` | Replay fixed tasks headlessly in a fixture repo to get comparable runs; Codex `--json` gives an event stream | Trial runner for fresh-session evals (builders are already `codex_exec`) | Inference cost per trial (model dependent) | Verify `-p` flags with a tiny positive control; `--ephemeral` and `--output-schema` exist for Codex |
| skill-creator scripts + grader/comparator/analyzer agents | Reuse the baseline-vs-variant workspace layout and benchmark stats (mean +/- stddev) for subagent trials | `run_loop` style held-out split and repeats for trigger/routing evals (does a role read the right CONTEXT.md?) | Subagent tokens; 3 repeats per query in its default loop | Read `run_eval.py`/`aggregate_benchmark.py` before adopting; they target skills, adapt to roles |
| c8-eval-engineer (discipline) | Checklist for every eval: holdout, leakage, freshness, counterfactual baseline; Husain loop: manually review 20-50 real transcripts first | Judge alignment floors, different-family judge, drift vs regression split, human floor | Free (reading); human time for manual review | Strip the council vocabulary; adopt items 1-6 above |
| harness-adversarial-reviewer (method) | Pattern for grading reviewer roles (Astra, pre-review): planted-defect catch rate, rejected-findings transparency | Permanent regression set of planted defects | Free | Adapt; its content is for another project |
| skill-scenario-generator (shape) | Scenario types for role cards: happy, edge, ambiguous, out-of-scope | Keeps scenario sets uniform | Free | Re-point its hard-coded `~/Projects/agent-deployment-framework` paths |
| promptfoo (NOT installed) | Could run N repeats of a fixture task against `anthropic:claude-agent-sdk` and `openai:codex-sdk` with `javascript`, `skill-used`, `trajectory:*` and `llm-rubric` assertions, JSON/JSONL out, web viewer | CI-style gate with exit code 100, JUnit XML, history in `~/.promptfoo` | Inference per trial plus judge calls; free tool | Operator approval to install (npx or npm), the two SDK packages, API keys or local-session auth (`apiKeyRequired: false` for Claude; Codex "Optional if Codex is already signed in via ChatGPT"); verify repeat flag and result shape first. Needs a Git repo for Codex `working_dir` |

## Open questions for MAESTRO
1. Does the operator allow installing promptfoo (and the Claude Agent SDK package)? Without it, all agent trials need a hand-built runner on `claude -p` and `codex exec --json`, with duckdb + marimo for analysis. A throwaway install under /tmp was not done (rule: install nothing).
2. promptfoo's fit is weakest where our roles depend on repo state across a whole ticket lifecycle (worktree lanes, gates). Do fixture repos with `copy_working_dir` capture enough of that, or does the baseline have to come from historical transcripts only?
3. Which judge family grades which worker? Claude workers need a non-Claude judge (and vice versa) per the C8 collision rule; do we have usable non-Claude credentials for judge calls inside promptfoo, or would Codex be the grader through `codex exec`?
4. How do Claude sessions map to tickets? The jsonl has `cwd`, `gitBranch`, `sessionId`, `bridgeSessionId` but no ticket id field; a transcript-to-ticket join may need the ticket ledgers (not examined here).
5. Codex reasoning is encrypted in rollouts; is tool-call and command evidence enough for process evals, or do we also need the final messages (`-o`)?

## Sources
1. promptfoo, Getting started, https://www.promptfoo.dev/docs/getting-started/ (read 2026-10-17; undated page).
2. promptfoo, Claude Agent SDK provider, https://www.promptfoo.dev/docs/providers/claude-agent-sdk/ (2026-10-17).
3. promptfoo, OpenAI Codex SDK provider, https://www.promptfoo.dev/docs/providers/openai-codex-sdk/ (2026-10-17).
4. promptfoo, Assertions and metrics (expected outputs), https://www.promptfoo.dev/docs/configuration/expected-outputs/ (2026-10-17).
5. promptfoo, Custom script / exec provider, https://www.promptfoo.dev/docs/providers/custom-script/ (2026-10-17).
6. promptfoo, Command line, https://www.promptfoo.dev/docs/usage/command-line/ (2026-10-17).
7. promptfoo, Output formats, https://www.promptfoo.dev/docs/configuration/outputs/ (2026-10-17).
8. promptfoo, Configuration reference, https://www.promptfoo.dev/docs/configuration/reference/ (2026-10-17).
9. promptfoo, llm-rubric, https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/ (2026-10-17).
10. promptfoo, CI/CD integration, https://www.promptfoo.dev/docs/integrations/ci-cd/ (2026-10-17).
11. marimo home page, https://marimo.io/ (2026-10-17).
12. Local: `/Users/robertrhu/.claude/skills/marimo-notebook/SKILL.md` (mtime of target not recorded; lines cited inline).
13. Local: `/Users/robertrhu/.claude/skills/marimo-batch/SKILL.md`, `.../marimo-pair/SKILL.md`, `.../jupyter-to-marimo/SKILL.md`, `.../streamlit-to-marimo/SKILL.md`.
14. Local: `<S>/c8-eval-engineer/SKILL.md` (file dated Oct 3 2026), `<S>/harness-adversarial-reviewer/SKILL.md`, `/Users/robertrhu/.claude/skills/skill-scenario-generator/SKILL.md` (Apr 22 2026), `/Users/robertrhu/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator/SKILL.md` (Oct 9 2026).
15. Commands run 2026-10-17: `command -v promptfoo`, `npx --no-install promptfoo --version`, `command -v marimo`, `marimo --version`, `M/.venv/bin/python -c "import duckdb..."`, `claude --version`, `claude --help`, `codex --version`, `codex exec --help`, `find`/`head -c` over `~/.claude/projects/...` and `~/.codex/sessions/...`.
