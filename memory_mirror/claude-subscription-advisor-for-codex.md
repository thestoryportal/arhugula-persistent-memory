---
name: claude-subscription-advisor-for-codex
description: For Codex-led science, use Claude via claude.ai Max subscription as the out-of-family advisor; Codex/GPT is fallback or secondary
metadata:
  type: workflow
---

For **Codex-led** LLM-as-Database science work, the primary out-of-family advisor is now Claude through the local Claude Code CLI and the operator's `claude.ai` Max subscription. Use `tools/claude_advisor.sh`; it checks `claude auth status`, requires `authMethod=claude.ai`, and refuses API-key auth. It runs `claude -p --tools "" --no-session-persistence` with `tools/advisor_review_prompt.md`, default `CLAUDE_ADVISOR_MODEL=opus`, default `CLAUDE_ADVISOR_EFFORT=high`.

Why: Codex/GPT reviewing Codex-led work is same-family/weak independence. For Claude-led work, the older GPT-family Codex review remains the out-of-family route. Direction matters: use the opposite family from the authoring agent.

How to apply: before prereg/test authoring, approach commitments, stalls/surprises, and verdicts, feed Claude a compact review package with exact artifact paths and numbers:

```bash
cd /workspace
tools/claude_advisor.sh <<'EOF'
<design/finding/approach + evidence + exact numbers + relevant context>
EOF
```

Review output is input, not evidence; preregistered criteria and saved artifacts bind.
