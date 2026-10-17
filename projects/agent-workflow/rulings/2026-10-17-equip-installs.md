# Operator rulings: equip installs (2026-10-17, chat, verbatim)

MAESTRO asked three questions (options and recommendations in `drafts/research/equip-vet-and-installs.md`). The operator answered:

1. promptfoo: "npx pin 0.123.1 (Recommended)"
2. Skills: "Both...but please review these skills comparitively to the chosen plugin with 9 skils as well...https://www.skills.sh/affaan-m/ecc/eval-harness, https://www.skills.sh/affaan-m/ecc/agent-eval, https://www.skills.sh/github/awesome-copilot/agentic-eval and this additional blog post: https://hamel.dev/blog/posts/evals-faq/"
3. marimo: "Keep global (Recommended)"

MAESTRO reading of 2: install the two vetted sets (ai-evals-course/evals-skills, 9 skills; promptfoo-evals), Claude only, into `~/.claude/skills/`, after a comparative review of the three named skills and the FAQ against the 9-skill plugin. The review is `drafts/research/skills-comparative.md`.

## MAESTRO actions and decisions (2026-10-17)
- Comparative review done: `drafts/research/skills-comparative.md`. MAESTRO read it and re-checked two decisive claims at the pinned commits (agent-eval `judge.py` returns pass when a task has no test; ECC `variants/reward-hack/run.js` reads the checker's answers and calls the network).
- Not installed: ECC eval-harness, ECC agent-eval, awesome-copilot agentic-eval (reasons in skills-comparative.md §6).
- Borrowed into the Phase 1 design: (1) a reward-hack positive control: every grader and gate must reject a cheating variant before a pass is trusted; (2) the per-run trial record `{passed, exit_code, duration, tokens, cost}` as the minimal trial schema; (3) FAQ additions 1-12 (skills-comparative.md §5) as inputs to sweep-common and the eval design.
- Installed: the 9 `ai-evals-course/evals-skills` skills @80d5f7b and `promptfoo-evals` @ea8b3d0, copied into `~/.claude/skills/` from the bytes MAESTRO read; `shasum -a 256 -c` passed on every file. Claude only; not for Codex.
- promptfoo is not installed; it runs as `npx -y promptfoo@0.123.1` at first use. marimo stays global 0.24.2.
