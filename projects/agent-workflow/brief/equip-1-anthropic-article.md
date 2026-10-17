# Equip 1: the Anthropic article on agent evals

Read M/projects/agent-workflow/brief/equip-common.md first.

Source: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (fetch it; read all of it; follow links it gives to other Anthropic engineering posts or docs only where the article relies on them).

Output: M/projects/agent-workflow/drafts/research/anthropic-demystifying-evals.md

Sections:
1. `## What the article says, in its order`: a faithful digest, one subsection per article section, with its key claims and short exact quotes. Include every definition (task, trial, grader, transcript, outcome, harness, suite, or whatever terms it uses), every grader type and when it recommends each, every metric (for example pass@k vs pass^k, if present), and every recommended practice and warning.
2. `## Practices as a checklist`: each practice as one testable line ("Each task has a reference solution that passes its graders"), citing the section.
3. `## Mapping to our program`: for each practice, which of our phases (1-6, see the charter) it bears on and how, marked INFERENCE.
4. `## What the article does not cover` that our program needs (for example: multi-agent orchestration, Codex agents, context and memory evaluation), marked INFERENCE.
