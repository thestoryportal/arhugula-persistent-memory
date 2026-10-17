# Comparative review: three more eval skills and the Hamel evals FAQ, against the chosen 9-skill plugin and promptfoo-evals (equip research, 2026-10-17, Opus 5.5)

Scope: the operator asked to "review these skills comparitively to the chosen plugin with 9 skils" and read the Hamel FAQ (rulings/2026-10-17-equip-installs.md, item 2). Baseline: `ai-evals-course/evals-skills` @ `80d5f7b0127c7572ed9e9339937adbfd7240ffeb` and `promptfoo-evals` @ `ea8b3d073a63769f7be243ac3c3460f72881a930` (equip-vet-and-installs.md, Decision 2). Paths below are inside each repo at the pinned commit. "L" = line.

Commits read:
- affaan-m/ECC `76aaa77df6adc5b889e689007bf99b9a4f74af34` (main, committed 2026-10-15T19:17Z; MIT; user-owned repo; 282,399 stars) [S1]
- joaquinhuigomez/agent-eval `6d062a2f5cda6ea443bf5d458d361892c04e749b` (master, 2026-03-16; MIT; 4 stars). This is the external CLI that ECC agent-eval tells the agent to install [S2]
- github/awesome-copilot `cb64ad12e32737ae764becd6885462e9b4c7cb00` (main, 2026-10-16; MIT) [S3]

Paths confirmed with `gh api 'repos/<o>/<r>/git/trees/<sha>?recursive=1'` (ECC: 6,355 entries; awesome-copilot: 4,572 entries; neither truncated).

## 1. Candidate 1: ECC `eval-harness`

**What it does.** Description, verbatim: "Formal evaluation framework for Claude Code sessions implementing eval-driven development (EDD) principles. Use when a Claude Code workflow needs a formal eval before it is trusted or changed." (`.agents/skills/eval-harness/SKILL.md` L3)

**Files.** ECC has two copies of the skill:
- `.agents/skills/eval-harness/SKILL.md` (236 lines; this is the path in the brief) and `agents/openai.yaml` (7 lines).
- `skills/eval-harness/SKILL.md` (305 lines). Its body matches the `.agents` copy line for line (command: `diff` of `.agents` L8-236 against `skills` L9-237 printed nothing; BODY-IDENTICAL). It adds two sections: "Local Framework Utilities" (L239-271) and "Product Evals (v1.8)" (L273-305).
- Example set `examples/eval-harness/`: README.md, gate.config.json, taskset.json, run-example.js, and variants/{baseline,candidate,reward-hack}/{run.js,variant.json}. All read in full.
- Library `scripts/eval-harness.js` and `scripts/lib/eval-harness/{index,canonical,envelope,capsule,gate,gate-child,effect-fence,replay,receipt,retrospective}.js`. All read in full (1,407 lines).
- Not read: `docs/architecture/eval-harness-frameworks.md` (23.6 KB). The `skills/` copy points to it at L271. It is prose, not a script.

**What the markdown tells the agent to do.**
- Write capability and regression evals before coding: "Define expected behavior BEFORE implementation" (L23) and "Define evals BEFORE coding" (L198).
- Grade with shell checks (`grep -q ... && echo PASS`, `npm test`, `npm run build`, L58-67). The model grader is "Use Claude to evaluate open-ended outputs" with "Score: 1-5" (L70-80). The human grader is a markdown flag (L84-90).
- Metrics: pass@k "At least one success in k attempts", with "Typical target: pass@3 > 90%" (L95-98). pass^k is "All k trials succeed", glossed as "pass^3: 3 consecutive successes" (L101-104). There is no estimator, no trial count and no confidence interval.
- Use `/eval define|check|report` (L169-183) and store files in `.claude/evals/` (L187-194). The skill folder does not ship `/eval`. It exists only as `legacy-command-shims/commands/eval.md`, whose description reads "Legacy slash-entry shim for the eval-harness skill. Prefer the skill directly." (`gh api` read, 2026-10-17). So `/eval` would not resolve if we copied only the skill folder (INFERENCE).
- `agents/openai.yaml` L7: `allow_implicit_invocation: true`. This is the same Codex auto-invocation risk the vet file records for the 9 skills.

**Scripts.** The `.agents` SKILL.md tells the agent to run no script. The `skills/` copy tells it to run `node scripts/eval-harness.js example` (L244).

| Script | What it executes | What it writes | Network / git | API key |
|---|---|---|---|---|
| `scripts/eval-harness.js` | CLI dispatch. `example` spawns `node examples/eval-harness/run-example.js` (L53-55). `gate run` calls `requireSupportedIsolation()` and refuses (L92-96). | `receipt build --out` writes a receipt file. `capsule project/export` write projection.json and copy 3 files. | none / none | no |
| `examples/eval-harness/run-example.js` | Calls the library and never loads a variant: `runGate` refuses (L55-60), `loadVariant` hashes source (L68), `scanTripwires` (L71), replay of a locally declared fixture (L77-105), receipt and tamper check (L108-136). | `mkdtemp` under `os.tmpdir()` (L22); removed with `rmSync` unless `--keep` (L139-141). | none / none | no |
| `lib/gate.js` | Static inspection only. `requireSupportedIsolation` throws `gate.isolation_required` (L175-177). `runGate` and `runVariant` call it (L180-182, L240-242). | none | none / none | no |
| `lib/capsule.js` | Append-only, hash-linked NDJSON journal with a cooperative lock file. | `capsule.json`, `journal.ndjson`, `.append.lock`, `projection.json` in the capsule dir (L26-29, L153-155) | none / none | no |
| `lib/replay.js` | Record mode calls the registered `impl` (L139). Replay mode never does, and refuses SE3+ tools (L131-134). | fixture JSON files (L60) | none / none | no |
| `lib/envelope.js`, `canonical.js`, `receipt.js`, `retrospective.js` | Validation, hashing, receipt build and verify, read-only grouping | `receipt.js` `writeReceipt` (L168-172) | none / none | no |
| `gate-child.js`, `effect-fence.js` | Retired. They only throw (L5). | none | none | no |

None of the scripts requires `http`, `https`, `net` or `child_process`, except `eval-harness.js`, which spawns `process.execPath` for the example. Evidence: reading in full, plus `gate.js` L20-25 and the import lines of each file.

**The reward-hack fixture.** `variants/reward-hack/run.js`:
- `phoneHome` sends an HTTPS POST to `example.invalid` and swallows errors (L8-17).
- `peekAtAnswers` reads `../../taskset.json` and returns the checker's `expected` value (L19-27, L21).
- `solve` returns the leaked answer first (L31-34).

`gate.js` DEFAULT_TRIPWIRES (L37-44) flags `hidden_network`, `process_spawn`, `sandbox_weakening`, `checker_probe` (`/taskset|expected_output|.../`) and `parent_escape`. `run-example.js` asserts that both `hidden_network` and `checker_probe` fire on this fixture (L73). The authors limit the claim themselves: "Absence of detected tripwires does not establish containment or prevent reward hacking" (`gate.js` L13-14). taskset.json marks t10-t12 `held_out: true` (L15-17), but no code uses the flag to score anything.

**Risks.**
- The markdown method conflicts with ruling 3 (error analysis first). The FAQ answers "Should I practice eval-driven development?" with "Generally no" (§3).
- Its model grader is a same-family "Use Claude" 1-5 score. That conflicts with ruling 1 (cross-family) and with the 9-skill plugin's binary rule (`write-judge-prompt` L38, L142).
- The code cannot run a candidate at all: "Candidate execution is disabled on every OS" (`skills/` SKILL.md L262). It is a journal/receipt library, not a harness.
- `allow_implicit_invocation: true`.

## 2. Candidate 2: ECC `agent-eval`

**What it does.** "Head-to-head comparison of coding agents (Claude Code, Aider, Codex, etc.) on custom tasks with pass rate, cost, time, and consistency metrics." (`skills/agent-eval/SKILL.md` L3). A copy exists at `pi/core/skills/agent-eval/SKILL.md` (same size, 4,696 B).

**Files.** One file, SKILL.md (147 lines). It ships no scripts. It tells the agent to install an external CLI: "Install agent-eval from its repository after reviewing the source." (L23), linking `github.com/joaquinhuigomez/agent-eval` (L147).

**What it tells the agent to run, and what that CLI actually is** (read at [S2]):
- SKILL.md L78: `agent-eval run --task tasks/add-retry-logic.yaml --agent claude-code --agent aider --runs 3`. The real CLI takes `--tasks` (required) and `--agents` (comma-separated) (`src/agenteval/cli.py` L21-22). The documented flags do not exist, so this command fails on argparse (INFERENCE from the argparse definitions; not run).
- SKILL.md L92: `agent-eval report --format table`. The real `report` takes only `--input` (cli.py L28-29).
- The SKILL.md task YAML (L31-47: `prompt`, `files`, `judge:` list, `commit`) does not match the model, which has `id, description, repo, ref, test_cmd, judge_prompt, timeout_seconds, tags` (`models.py` L6-14).
- **Default pass.** The LLM judge "type: llm" (SKILL.md L126-134) is not implemented: `# Future: LLM-as-judge evaluation ... return True, 0`. A task with no `test_cmd` also returns `True, 0` (`judge.py` L26-32). A task without a test therefore always passes. This is a grading hole an agent can exploit.
- Agents run as `claude -p <description> --output-format json` in the worktree (`adapters/claude_code.py` L21-30) and as `aider --message ... --yes-always --no-git` (`adapters/aider.py` L21-26). The tree has adapters for aider, claude_code and mock only. There is no Codex adapter, although L3 names Codex (tree listing at [S2]).
- Isolation: `git worktree add --detach <mkdtemp> <ref>`, then `git worktree remove --force` and `shutil.rmtree` (`isolation.py` L25-46). This uses git and writes inside the target repo's `.git/worktrees`. It does not isolate HOME, so `~/.claude` memory and settings are shared across trials (INFERENCE).
- Install path: a pip package (`pyproject.toml`: pydantic, pyyaml; entry point `agent-eval`). Network and API keys come from the agents it spawns, which use the operator's Claude/Aider auth. The judge `test_cmd` runs through `create_subprocess_shell` (`judge.py` L38-43).

**Method claims.** "Run at least 3 trials per agent" (L139). "Pin the commit" (L140). "Include at least one deterministic judge ... LLM judges add noise" (L141). "Consistency | Pass rate across repeated runs" (L60).

**Risks.** The documentation and the code have drifted apart: wrong flags, wrong schema, a judge type that does not exist, an agent with no adapter. The default-pass judge. Low upstream maintenance (4 stars; last push 2026-03-16, [S2]). The skill tells the agent to install a package, which our hard rules forbid without approval.

## 3. Candidate 3: awesome-copilot `agentic-eval`

**What it does.** "Patterns and techniques for evaluating and improving AI agent outputs. Use this skill when: - Implementing self-critique and reflection loops - Building evaluator-optimizer pipelines ..." (`skills/agentic-eval/SKILL.md` L3-10).

**Files.** One file, SKILL.md (189 lines). No scripts and no `agents/openai.yaml`. The code blocks are illustrative Python built around an undefined `llm()`.

**Method claims.**
- Self-critique with the same `llm()` that generated the output (Pattern 1, L40-61).
- An evaluator-optimizer loop with a 0-1 score threshold (L72-98).
- Code reflection where the tests are generated by the LLM from the code it just wrote: `tests = llm(f"Generate pytest tests for: {spec}\nCode: {code}")` (L110).
- Pairwise "Which is better" judge (L136-137).
- Weighted 1-5 rubric (L144-153).
- Best practices: iteration limits, a convergence check, "Log history" (L159-165). "Handle evaluation parse failures gracefully" (L188).

**Risks.**
- This skill is about generation-time refinement, not measurement.
- Its judge is the same model. That conflicts with ruling 1.
- It uses Likert/weighted scores, which conflict with the binary rule (`write-judge-prompt` L142) and with the FAQ's pass-all advice (§3).
- Tests written by the model that wrote the code can encode the bug. The skill gives no human validation step (INFERENCE).

## 4. Comparison table

Legend: Y = yes, N = no, P = partial. Each cell cites its source. "Fit" is INFERENCE.

| | Agents / coding agents | Trials, pass@k / pass^k | Judge vs humans | Cross-family judge | Error analysis from transcripts | Trial isolation | Anti-gaming | Runs code | Fit to our belt |
|---|---|---|---|---|---|---|---|---|---|
| ECC eval-harness | Y, "Claude Code sessions" (L3) | P: defines both (L95-104); no estimator, trial count or CI | N: 1-5 Claude grader (L70-80) | N: "Use Claude" (L70) | N: define before coding (L23) | N in markdown; code refuses all execution (`gate.js` L175-177) | P: reward-hack fixture + syntactic tripwires (`gate.js` L37-44); held-out flags unused | Y: offline Node example; no net, no git | Low as a skill. One fixture idea is worth taking. |
| ECC agent-eval | Y: Claude Code, Aider (Codex claimed, no adapter) | P: `--runs N`; consistency = pass rate (L60); no pass^k | N | N | N: stdout kept in RunResult (`models.py` L32) but never reviewed | P: git worktree per run at `ref`; HOME shared | N: no-test tasks pass (`judge.py` L26-32) | Y: pip CLI; spawns `claude -p`, `aider --yes-always`, shell, git | Low. Docs drifted from code. |
| awesome-copilot agentic-eval | P: agent outputs; no harness | N | N | N: same `llm()` (L46) | N: "Log history" only (L164) | N | N: LLM writes its own tests (L110) | N: illustrative Python only | None for measurement |
| evals-skills (9) | P: LLM pipelines incl. agent traces (`error-discovery` L40-49) | N (grep `pass@\|trial\|repeat` on all 9: no hits on trials) | Y: TPR/TNR on held-out test (`validate-evaluator` L17-19; `eval-audit` L88-104) | N: "The same model ... works as judge" (`write-judge-prompt` L134) | Y: core (`error-discovery`; `eval-audit` L38-50) | N: not addressed | P: train/dev/test leak check (`eval-audit` L104); no reward-hack check | P: local `http.server` review app (`error-discovery` L119) | High for error analysis and judge validation (vet file) |
| promptfoo-evals | P: configured target; promptfoo 0.123.1 pulls agent SDKs (vet file) | N in skill; promptfoo repeat flag UNVERIFIED (vet file) | P: known-good must pass, known-wrong must fail (SKILL L39-41); not human TPR/TNR | P: "Set an explicit grader provider" (L36); allows cross-family, does not require it | N | N | P: "Check the candidate output, not words that also occur in the rubric" (L40-41); untrusted inputs (L28-29) | Y: `npx promptfoo eval` (L69), network to providers | High as a runner (vet file) |

The gaps no row fills are trial isolation and an anti-gaming check that actually runs. The Anthropic article covers both, as checklist items 7 and 13 (anthropic-demystifying-evals.md L108, L114).

## 5. The FAQ

Source [S4]: "AI Evals: Everything You Need to Know", Hamel Husain and Shreya Shankar, published 2026-09-18, modified 2026-09-21. The full page text was read in Chrome with get_page_text on 2026-10-17, so no quote below is DIGEST. The authors warn: "These are sharp opinions about what works in most cases. They are not universal truths."

The FAQ never mentions pass@k, pass^k, repeated trials, trial isolation, sandboxing or reward hacking. Command: grep for `pass@|trial|nondetermin|isolat|sandbox|reward hack|gaming` over the saved page text. The only hits were unrelated uses of "confidence intervals" and "isolat". Its coding-agent answer asks only for "a working environment and code-based tests". The Anthropic article stays our source for non-determinism and isolation.

### Practices that ADD to the 9-skill plugin and the Anthropic article
Coverage was checked by grep on all 9 SKILL.md files, review-loop.md and promptfoo-evals, and by reading the Anthropic digest.
1. **Pass-all rate with drill-down and severity groups.** Q "How do I combine my evals into a single metric?": "An example passes only if it passes every check." It suggests "one pass-all rate for checks that should block a release and another for issues you can tolerate", and discourages weighted composites as "usually performative". Not in the plugin or the article.
2. **Prove the failure fires before you build its eval.** Q "How often should I run my evals?": "you should prove that you can trigger the error at least once by red-teaming your application before implementing the eval". The plugin has no red-team step. promptfoo-evals sends red-teaming to other skills (L26).
3. **A run schedule set by cost, saturation and business value.** Same Q. Its worked table retires, or runs every 2 weeks, an all-pass medium-value judge. A high-value saturated judge still runs "prior to each release".
4. **Minimal judge context, with ablation.** Q "How much context should I give a LLM judge?": "Do not give every judge the same full trace by default. Extra context can cause context rot". It recommends ablation against human labels, and a search tool only for very long agent traces. The plugin lists inputs per judge type (`write-judge-prompt` L128) but has no ablation step.
5. **Tool-call checks split four ways, plus authorization.** Q "How do I evaluate agentic workflows?": "Test the tool name, arguments, result, and resulting state as separate checks", and "Also test authorization and preconditions. A valid tool call can still be wrong if the user did not approve the action". The plugin has one row, "Bad tool call" (`write-code-eval` L24).
6. **Transition failure matrix.** Q "How do I evaluate agentic workflows?": "rows represent the last successful state and columns represent where the first failure occurred". Not in the plugin or the article (grep "transition": no hits).
7. **Multi-agent trace logging.** Q "How do I debug multi-turn conversation traces?": "assign a session or trace ID to each user request and log every message with its source (which agent or tool), trace ID, and position". Our belt is multi-agent, so this is a logging requirement (INFERENCE).
8. **N-1 testing and simplest repro.** Same Q: "provide the first N-1 turns of a real conversation and test what happens next". Also: "reproduce it with the simplest possible test case."
9. **Proxy metrics for coding agents.** Q "How should I evaluate a coding agent?": "you can start with metrics like net new lines of code added and cyclomatic complexity" for over-engineering. Also: "build a private benchmark of difficult tasks from your organization", where each task needs a working environment and code-based tests. The article names over-engineering evals (digest L27) but gives no metric.
10. **Annotator disagreement procedure.** Q "How many people should annotate my LLM outputs?": label independently, hold an alignment session, "Update the rubric ... Then relabel affected examples". If annotators still disagree, a domain expert decides and the reason is recorded.
11. **Overfitting through dev-set iteration.** Q "How do I know if I can trust my automated eval?": overfitting "can happen even if you never put the dev examples directly in the prompt". The fix is "a new, untouched test set". The plugin has the split but not the re-split rule.
12. **Human-first count before agent suggestions.** Q "How many examples do I need for an eval?": "annotate at least 30 traces ... yourself before asking the agent to suggest failures", because "its guesses can bias your judgment". The plugin's review loop has agent suggestions (`review-loop.md` L43-51). The 30-trace floor is the addition.

### Practices that CONFLICT with our rulings (equip-vet-and-installs.md, "Method conflicts and our rulings")
1. **Ruling 1 (cross-family judge).** Q "Can I use the same model for both the main task and evaluation?": "using the same model is usually fine because the judge is doing a different task", and "we don't advocate for using different models by default unless there's a specific alignment issue." Q "What model or LLM should I use to build automated evals?": "You can also use the same model as your application." This is the same position as `write-judge-prompt` L134, which ruling 1 already overrides. The FAQ's own test is alignment with human labels. Under ruling 1 we keep cross-family and still measure TPR/TNR.
2. **Charter goal 6 (durable instrument), not a ruling.** Q "What should I do when my 'gold' eval dataset becomes stale?": "its scores may no longer be directly comparable with older scores. That is ok!" It also says to retire evals that keep passing. The Anthropic article instead graduates saturated capability evals into regression suites (digest L117). This is a tension, not a contradiction: evolving eval sets need versioning if scores are to stay comparable over time (INFERENCE).
3. **No conflict with ruling 2.** The FAQ uses TPR/TNR for judge vs human (Q "How do I know if I can trust my automated eval?") and Cohen's Kappa for multiple annotators (Q "How many people should annotate..."). Ruling 2 adds Rogan-Gladen and a bootstrap CI. The FAQ neither asks for them nor rejects them.
4. **No conflict with ruling 3.** It is reinforced: "Error analysis is the most important activity in evals" (Q "Why is 'error analysis' so important...").

The FAQ also conflicts with candidates 1 and 3 (not with our rulings): "Should I practice eval-driven development? Generally no." It also discourages Likert scales and weighted composites (Q on binary evals; Q on a single metric).

## 6. Recommendation inputs (MAESTRO decides)

1. **ECC eval-harness: do not install. Borrow one named idea: the reward-hack positive control.** Add a deliberately gaming variant to our eval sets, modelled on `variants/reward-hack/run.js`, which reads the checker's answers at L19-27 and calls the network at L8-17. Require every grader and gate to reject it before trusting a pass. The tripwire list (`gate.js` L37-44, e.g. `checker_probe`, `parent_escape`) can serve as a cheap static pre-check. Its authors say it is not containment (L13-14). Neither the 9-skill plugin nor promptfoo-evals has this check (§4). This also turns the Anthropic article's "Make your graders resistant to bypasses or hacks" into a test. Do not install because the markdown is EDD-first, uses a same-family 1-5 grader and depends on an `/eval` shim it does not ship.
2. **ECC agent-eval: do not install the skill or its CLI.** The documented commands and YAML do not match the code (cli.py L21-29; models.py L6-14). Tasks without tests pass by default (judge.py L26-32). There is no Codex adapter. Installing needs pip. The ideas it holds are a pinned-commit task file, N runs per agent, and cost and time recorded per run. Our worktree lanes already supply the isolation it offers (MEMORY "Atomic units, parallel worktree lanes"). If MAESTRO wants one idea, take the per-run record `{passed, exit_code, duration, tokens, cost}` (models.py L23-34) as a minimal trial schema.
3. **awesome-copilot agentic-eval: do not install.** It is a refinement pattern built on same-model self-critique, LLM-written tests and weighted 1-5 rubrics. Each of these conflicts with ruling 1 or with the binary rule. It has no idea to borrow that the baseline lacks.

## Open questions for MAESTRO
1. Which eval-harness file does skills.sh serve: `.agents/` (236 lines) or `skills/` (305 lines)? The bodies are identical. Fetching skills.sh with curl was denied by the permission system this session, so this is UNVERIFIED.
2. Who is the FAQ's "benevolent dictator", who must hand-annotate the first 30+ transcripts: the operator or MAESTRO? The FAQ says initial open coding should "Never skip this or delegate it" (Q "What parts of evals can be automated with LLMs?").
3. How do we keep evals durable (charter goal 6) when the FAQ retires saturated evals and accepts non-comparable scores, while Anthropic graduates them to regression? Options include a versioning rule and frozen regression sets.
4. How should we aggregate: one pass-all rate per severity group (FAQ), or pass^k per task (Anthropic)? Or both, with pass-all measured per trial?
5. Should the reward-hack positive control become a standing gate step for Astra and the prober, like our mutant and deletion probes?
6. Not read: `docs/architecture/eval-harness-frameworks.md` (23.6 KB) and the ECC tests. Read them only if idea 1 is adopted.

## Sources
1. [S1] affaan-m/ECC @ 76aaa77df6adc5b889e689007bf99b9a4f74af34 (committed 2026-10-15). Files read with `gh api repos/affaan-m/ECC/contents/<path>?ref=<sha>` (raw): `.agents/skills/eval-harness/{SKILL.md,agents/openai.yaml}`, `skills/eval-harness/SKILL.md`, `skills/agent-eval/SKILL.md`, `examples/eval-harness/*`, `scripts/eval-harness.js`, `scripts/lib/eval-harness/*.js`, `legacy-command-shims/commands/eval.md` (head). Read 2026-10-17.
2. [S2] joaquinhuigomez/agent-eval @ 6d062a2f5cda6ea443bf5d458d361892c04e749b (2026-03-16): `pyproject.toml`, `src/agenteval/{cli,runner,isolation,judge,models,cost,task}.py`, `adapters/{base,claude_code,aider}.py` (task.py and aider.py read by grep only), and the tree listing. Read 2026-10-17.
3. [S3] github/awesome-copilot @ cb64ad12e32737ae764becd6885462e9b4c7cb00 (2026-10-16): `skills/agentic-eval/SKILL.md`. Read 2026-10-17.
4. [S4] https://hamel.dev/blog/posts/evals-faq/ (published 2026-09-18, modified 2026-09-21). Full text read in Chrome get_page_text on 2026-10-17.
5. ai-evals-course/evals-skills @ 80d5f7b0127c7572ed9e9339937adbfd7240ffeb: all 9 SKILL.md and review-loop.md, re-fetched 2026-10-17 and checked by grep for the cells cited. Not re-read in full; the full read is in the vet file.
6. promptfoo/promptfoo @ ea8b3d073a63769f7be243ac3c3460f72881a930: `plugins/promptfoo/skills/promptfoo-evals/{SKILL.md,references/eval-patterns.md}`, re-fetched 2026-10-17.
7. M/projects/agent-workflow/drafts/research/equip-vet-and-installs.md (2026-10-17): rulings 1-3, Decision 2.
8. M/projects/agent-workflow/drafts/research/anthropic-demystifying-evals.md (2026-10-17): L17-20, L27, L61-64, L105-119.
9. M/projects/agent-workflow/rulings/2026-10-17-equip-installs.md and brief/charter.md (2026-10-17).
