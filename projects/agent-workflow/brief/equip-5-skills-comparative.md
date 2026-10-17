# Equip 5: comparative review of three more eval skills and the Hamel evals FAQ

Read M/projects/agent-workflow/brief/equip-common.md first; its hard rules apply. Then read M/projects/agent-workflow/drafts/research/equip-vet-and-installs.md (what is already vetted and chosen, and our method rulings).

Operator, verbatim: "Both...but please review these skills comparitively to the chosen plugin with 9 skils as well...https://www.skills.sh/affaan-m/ecc/eval-harness, https://www.skills.sh/affaan-m/ecc/agent-eval, https://www.skills.sh/github/awesome-copilot/agentic-eval and this additional blog post: https://hamel.dev/blog/posts/evals-faq/"

Output: M/projects/agent-workflow/drafts/research/skills-comparative.md (cap 300 lines).

## The baseline you compare against
- The chosen plugin: `ai-evals-course/evals-skills` at commit `80d5f7b0127c7572ed9e9339937adbfd7240ffeb` (9 skills: evals-start, error-discovery, eval-audit, write-code-eval, write-judge-prompt, validate-evaluator, generate-synthetic-data, build-review-interface, evaluate-rag).
- Also chosen: `promptfoo/promptfoo` `plugins/promptfoo/skills/promptfoo-evals/` at commit `ea8b3d073a63769f7be243ac3c3460f72881a930`.
- Read them with `gh api "repos/<owner>/<repo>/contents/<path>?ref=<sha>" -H 'Accept: application/vnd.github.raw'`.

## The candidates
1. affaan-m/ECC `eval-harness` (SKILL.md at `.agents/skills/eval-harness/`; example set at `examples/eval-harness/`: run-example.js, gate.config.json, taskset.json, variants/{baseline,candidate,reward-hack}/run.js).
2. affaan-m/ECC `agent-eval` (`skills/agent-eval/`).
3. github/awesome-copilot `agentic-eval`.
Confirm each path with `gh api 'repos/<owner>/<repo>/git/trees/<sha>?recursive=1'`. Record the commit SHA you read. Read every file in each skill folder, and every script the skill tells the agent to run, in full. For each script say what it executes, what it writes, whether it touches the network or git, and whether it needs an API key.

## The blog post
Read https://hamel.dev/blog/posts/evals-faq/ as raw page text in Chrome: load the tools with ToolSearch query `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__tabs_close_mcp`, create your own tab, navigate, call get_page_text, close the tab. Click nothing. Do not use WebFetch for it: WebFetch returns a small-model digest, not the page. If Chrome fails twice, use WebFetch and mark every quote from it DIGEST.

## Sections of the output
1. One section per candidate: what it does (quote its description), files and scripts, risks, its method claims.
2. Comparison table. Rows: the 3 candidates, the 9-skill plugin, promptfoo-evals. Columns: evaluates agents/coding agents (not only product LLM output); multiple trials and pass@k/pass^k; judge validation against humans; cross-family judging; error analysis from transcripts; trial isolation; anti-gaming (reward-hack) checks; runs code; fit to our belt (one line, INFERENCE).
3. The FAQ: practices that ADD to the 9-skill plugin and the Anthropic article, and practices that CONFLICT with our rulings in equip-vet-and-installs.md. Short verbatim quotes, each with its FAQ question heading.
4. Recommendation inputs: for each candidate, one of install / do not install / borrow one named idea, with the reason. MAESTRO decides.
5. `## Open questions for MAESTRO`, `## Sources`.

Bad output: "eval-harness is a solid, well-structured framework." (no evidence, no comparison). Good output: "eval-harness `variants/reward-hack/run.js` writes a fake pass to its result file (line N); the 9-skill plugin has no anti-gaming check, so this is the one idea to borrow."

Context rule: if your context passes 45%, write what you have to the output file, mark unfinished sections INCOMPLETE, and stop.
