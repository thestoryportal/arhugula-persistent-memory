---
name: claude-subscription-advisor-for-codex
description: For Codex-led science, the out-of-family advisor is Claude via code/agents/claude_advisor.sh (Max subscription); run with LLMDB_ROOT=$PWD
metadata:
  type: reference
---

For **Codex-led** LLM-as-Database science work, the primary out-of-family advisor is Claude through the local Claude Code CLI and the operator's `claude.ai` Max subscription (`_system/governance/CODEX.md:40`). Use `code/agents/claude_advisor.sh`; it checks `claude auth status`, requires `authMethod=claude.ai`, and refuses API-key auth. It runs `claude -p --tools "" --no-session-persistence` with `code/agents/advisor_review_prompt.md`, default `CLAUDE_ADVISOR_MODEL=opus`, default `CLAUDE_ADVISOR_EFFORT=high`.

Why: Codex/GPT reviewing Codex-led work is same-family/weak independence. For Claude-led work, the GPT-family review (GPT-6-Astra high, `_system/governance/OPERATING-MODEL.md:20-21`) remains the out-of-family route. Direction matters: use the opposite family from the authoring agent.

How to apply: before prereg/test authoring, approach commitments, stalls/surprises, and verdicts, feed Claude a compact review package with exact artifact paths and numbers. The script still defaults `ROOT` to the pod path `/workspace` (`code/agents/claude_advisor.sh:5`), so set `LLMDB_ROOT` to the checkout you are in:

```bash
LLMDB_ROOT=$PWD code/agents/claude_advisor.sh <<'EOF'
<design/finding/approach + evidence + exact numbers + relevant context>
EOF
```

Review output is input, not evidence; preregistered criteria and saved artifacts bind.
