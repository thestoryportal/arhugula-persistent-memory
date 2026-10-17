# Equip 2: current research (arXiv)

Read M/projects/agent-workflow/brief/equip-common.md first.

Use the arXiv MCP tools (load them with ToolSearch, query "+arxiv search"; for example mcp__arxiv__search_papers, mcp__arxiv__get_abstract, mcp__arxiv__read_paper_section). Prefer 2025-2026 papers; include an older one only when it is the standard reference others cite.

Output: M/projects/agent-workflow/drafts/research/arxiv-agent-evals.md

Topics, one section each, 4-8 papers per topic, most relevant first:
1. Evaluating LLM coding agents and agentic workflows: benchmark and harness design, task design, graders (code-based, model-based, human), trajectory vs outcome grading, reliability metrics (pass@k, pass^k, variance across trials), contamination and overfitting to evals.
2. Context engineering for agents: what context an agent needs per step, retrieval and routing, instruction files (CLAUDE.md, AGENTS.md style), long-context degradation ("context rot"), measuring context sufficiency and precision.
3. Agent memory: episodic and semantic memory for agents, consolidation of session logs into durable memory, memory retrieval keyed to task, memory staleness and conflict, evaluation of memory systems.
4. Multi-agent orchestration: orchestrator-worker patterns, routing tasks to models by cost and capability, handoffs between sessions, measuring orchestration quality and cost.
5. LLM-as-judge reliability: judge bias, cross-family judging, calibration against human labels.

For each paper: arXiv id, title, date, one line on the question, the method in two lines, the key finding with a number where the paper gives one, and one line `Use for us:` (INFERENCE). Then `## Cross-paper takeaways`: at most 12 lines, each citing the papers it rests on.
