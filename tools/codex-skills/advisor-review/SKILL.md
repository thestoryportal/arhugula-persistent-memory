---
name: advisor-review
description: |
  Objective, independent adversarial review of a test design, finding, or approach.
  For Codex-authored work, default to Claude via local claude.ai Max subscription
  auth (`tools/claude_advisor.sh`), not Codex/GPT self-family review. TRIGGER at
  the discipline thresholds (DISCIPLINE.md §3): BEFORE authoring any test/criteria
  set or new harness; BEFORE declaring a result conclusive or writing it to
  CORPUS/; when stuck/looping; before committing to an approach. DO NOT TRIGGER
  for trivial mechanical edits.
allowed-tools: [Read, Bash]
---

# advisor-review — Claude out-of-family advisor for Codex work

For Codex sessions, the independent advisor is **Claude**, reached through the
local Claude Code CLI authenticated with the operator's claude.ai Max
subscription. This avoids same-family Codex/GPT self-review and does not use an
Anthropic API key.

## How to invoke

**A) Reasoning / finding / design review**:

```bash
cd "$LLMDB_ROOT"
tools/claude_advisor.sh <<'EOF'
<the test design / finding / approach, with artifact paths + exact numbers + relevant CORPUS/spec context pasted in>
EOF
```

`tools/claude_advisor.sh` runs:

- `claude -p` in non-interactive print mode;
- model from `CLAUDE_ADVISOR_MODEL` (default `opus`);
- effort from `CLAUDE_ADVISOR_EFFORT` (default `high`);
- `--tools ""` and `--no-session-persistence` so the review is based on the
  supplied package, not hidden transcript/tool context;
- an auth check requiring `claude.ai` subscription login.

**B) Code / diff review**:

Include the relevant diff/file-line excerpts in the review package and run the
same wrapper. Do not let the advisor's repo exploration substitute for feeding
the evidence.

**Fallback / secondary only:** if Claude auth is unavailable, a GPT/Codex review
can still be used, but label it as weaker independence for Codex-led work:

```bash
codex exec -m <stronger-model> "$(cat "$LLMDB_ROOT/tools/advisor_review_prompt.md")

--- ITEM UNDER REVIEW ---
<review package>"
```

## Rules

- **Feed it the evidence.** The advisor does not see your transcript.
- **Different model family** for genuine independence: Claude for Codex-led work;
  GPT-family for Claude-led work.
- The review is **input, not authority**: evidence and preregistered criteria bind.
- Honor DISCIPLINE.md §3: at least once before authoring a test set/new harness
  and before declaring done; do not re-review unchanged state.
