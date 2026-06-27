---
date: 2026-06-27
source: operator workflow critique after methodology skill deployment
scope: Codex/Claude science workflow
---

# Skills Are Contracts, Not Agents

Codex/Claude skills are semantic operating instructions plus optional referenced
assets/scripts. A `SKILL.md` does not create independent reasoning, autonomy, or
new tools by itself. It only shapes the main agent's behavior unless paired with
an executable tool, MCP, advisor call, or subagent.

Use skills as concise contracts: no checklist preambles, no massive schema dumps,
no generic recitation. High-value scientific reasoning should be agentized or
tooled: deterministic scripts for gates/stats, Claude/GPT/subagents for
adversarial or creative review, and explicit proposer -> critic -> designer
separation for stuck science arcs.
