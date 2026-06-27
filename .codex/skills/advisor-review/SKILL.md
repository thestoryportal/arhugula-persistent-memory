---
name: advisor-review
description: >-
  Independent, adversarial out-of-family review of a research step (design /
  finding / approach) in the LLM-as-Database program. In Codex sessions the
  default reviewer is Claude via local claude.ai Max subscription auth, not an
  API key. Use before authoring a test set, before declaring a result conclusive
  or writing it to CORPUS, before committing to an approach, or when stuck.
---

# advisor-review (Claude out-of-family advisor)

For Codex-authored work, the primary advisor is **Claude via the local Claude
Code CLI authenticated with the operator's claude.ai Max subscription**. This is
out-of-family relative to Codex and does not use an Anthropic API key.

## How to Invoke

Feed the design/finding/approach and its evidence on stdin:

```bash
cd /workspace
printf '%s
' '<PASTE: design OR finding OR approach, with artifact paths + exact numbers + relevant context>'   | tools/claude_advisor.sh
```

The wrapper checks `claude auth status` and refuses API-key auth; it requires
`authMethod=claude.ai`. It uses `CLAUDE_ADVISOR_MODEL=opus` and
`CLAUDE_ADVISOR_EFFORT=high` by default. Override only deliberately:

```bash
CLAUDE_ADVISOR_MODEL=opus CLAUDE_ADVISOR_EFFORT=xhigh tools/claude_advisor.sh <<'EOF'
<review package>
EOF
```

For a code/diff review, include the relevant diff excerpt or a concise file/line
summary in the review package. Keep Claude's tools disabled in the wrapper; the
reviewer judges the evidence you supply rather than exploring the repo with its
own hidden context.

## Fallback / Secondary Review

If Claude subscription auth is unavailable, use Codex/GPT-family review only as
a fallback or secondary check, and label it as weaker independence for Codex-led
work:

```bash
CODEX_HOME=/workspace/.codex codex exec -m gpt-5.5 "$(cat /workspace/tools/advisor_review_prompt.md)

<PASTE: review package>"
```

## Review Contract

Run `/workspace/tools/advisor_review_prompt.md` verbatim: real criterion vs
flattering adjacent; confounds and over-claims; `EVIDENCE-SHOWS` vs `I-INFER`;
cite-or-flag every factual claim; cheapest overturning test; F1 drift check.
Output a one-word verdict (`PROCEED` / `FIX-FIRST` /
`OVERTURNED-OR-RECONSIDER`), then the single most important next action, then
issues in priority order.

## Discipline

- Review is **input, not authority**; evidence and preregistered criteria bind.
- The reviewer does **not** see the Codex transcript. Missing evidence is
  `UNVERIFIABLE`, not assumed.
- Review output is never CORPUS evidence.
- Cross-family independence is the point: for Codex-led work, prefer Claude;
  for Claude-led work, use a GPT-family reviewer.
