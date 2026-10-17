# Rules for every equip research task (read this first, then your own brief)

Program: M/projects/agent-workflow/brief/charter.md (M = /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory). Read its "Operator, verbatim" section once, so you know what the research is for. In short: we will (1) define the ideal workflow for every agent role on our atomic-ticket build belt (orchestrator MAESTRO, builders, fixers, pre-reviewer, binding reviewer Astra, prober, sweep subagents, scripted stations), (2) measure the historical and current baseline with history and evals, (3) find the causes of the gap in our repo's context architecture, governance, skills and tools, (4) design the fix, including a memory architecture that consolidates session transcripts into durable repo context, (5) implement it, (6) keep evals as a lasting, scientifically durable instrument. Agents run as Claude Code sessions and subagents (Claude models) and Codex CLI sessions (OpenAI models), on macOS, in an ICM repo (folders + CONTEXT.md files route each agent to what it needs).

Your job is research for MAESTRO, who designs from your file. It is not design.

## Hard rules
- Write ONLY your one output file under M/projects/agent-workflow/drafts/research/. Edit nothing else. No commits.
- Install nothing (no npm, pip, brew, npx skills add, plugin install). Reading `--help` or `--version` of a tool that is already installed is allowed. Network reads (web pages, arXiv, package registries, GitHub pages) are allowed.
- Every claim cites its source: a URL (with the section or quote) or an arXiv id with its title, or `path:line` for local files, or the exact command and its output. Mark anything you infer as INFERENCE. A claim you cannot source is marked UNVERIFIED.
- Prefer primary sources (the author's page, the paper, the official docs) over blog summaries. Give each source's date.
- Quote short exact phrases where wording matters. Do not paraphrase a rule into a stronger or weaker one.
- Keep your context lean: read what you need; do not paste whole documents into your output.

## Output form
Markdown. First line: `# <title> (equip research, 2026-10-17, <model>)`. Then the sections your brief names, then `## Open questions for MAESTRO`, `## Sources` (numbered, with date). Hard cap: 400 lines.

Bad output: "Evals should be rigorous and use good metrics." (no source, says nothing). Good output: "Grade the outcome in the environment, not the transcript's claims: the article's example checks the database state after a booking task [URL, section 'Grading']."

When done, reply in at most 15 lines: the output path, its line count, the five findings you think matter most for our program.
