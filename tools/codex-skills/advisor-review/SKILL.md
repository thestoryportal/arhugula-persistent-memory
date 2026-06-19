---
name: advisor-review
description: |
  Objective, independent adversarial review of a test design, finding, or approach —
  the Codex equivalent of Claude's advisor(). TRIGGER at the discipline thresholds
  (DISCIPLINE.md §3): BEFORE authoring any test/criteria set or new harness; BEFORE
  declaring a result conclusive or writing it to CORPUS/; when stuck/looping; before
  committing to an approach. DO NOT TRIGGER for trivial mechanical edits.
allowed-tools: [Read, Bash]
---

# advisor-review — independent objective review (advisor-equivalent for Codex)

Claude has `advisor()` (a stronger model that auto-sees the full transcript). Codex has no auto-transcript reviewer, so you **build** the same function: an INDEPENDENT reviewer, fed the finding + evidence, prompted adversarially. **Independence is the point — use a DIFFERENT / STRONGER model than yourself** (same-model reading our own corpus = weak independence, runbook §2.5).

## How to invoke

**A) Code / diff review** (a harness or experiment you just wrote):
```bash
# one-time: git init the repo so review can diff (also unlocks /review)
git -C "$LLMDB_ROOT" rev-parse 2>/dev/null || (cd "$LLMDB_ROOT" && git init -q && git add -A && git commit -qm baseline)
codex review --uncommitted -m <stronger-model> "$(cat "$LLMDB_ROOT/tools/advisor_review_prompt.md")"
```

**B) Reasoning / finding / design review** (no diff — the advisor's main value):
Spawn an independent reviewer on a different/stronger model, feeding it the review prompt + the finding + its cited evidence:
```bash
codex exec -m <stronger-model> "$(cat "$LLMDB_ROOT/tools/advisor_review_prompt.md")

--- ITEM UNDER REVIEW ---
<the test design / finding / approach, with artifact paths + exact numbers + relevant CORPUS/spec context pasted in>"
```
(Or hand the same prompt + context to a fresh subagent.)

## Rules
- **Feed it the evidence.** Unlike Claude's advisor, it does NOT see your transcript — paste the finding, the artifact paths + exact numbers, and the relevant `CORPUS/`/spec context.
- **Different/stronger model** for genuine independence.
- The review is **input, not authority**: weigh it heavily, but **evidence is binding** over its opinion. On an evidence-vs-review conflict, reconcile in one more pass (don't silently override).
- Honor the bounds (DISCIPLINE.md §3): ≥1 before authoring a test set and before declaring done; don't re-review the same unchanged state.
