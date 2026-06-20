---
name: commit-forward-work-without-asking
description: Operator standing-auth (2026-06-20) — commit forward research work to LOCAL master without asking each time; push/PR stays operator-gated
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7e49dca7-c684-465a-936b-1c2ce4852502
---

**Operator directive (2026-06-20, robert):** Claude may **commit forward research work to local `master` without asking each time** — the commit step is pre-authorized for all forward work (experiments, fold-ins, living-doc updates, infra). Do not pause to ask "should I commit?" for routine forward progress.

**Why:** keeps the durable git record current without round-trips; the operator was repeatedly approving commits ("Commit D1 fold in", "commit it") and made it standing. Extends [[standing-auth-forward-requirements]] (which pre-authorizes infra/downloads/cov/disk) to the commit action.

**How to apply:**
- Commit fold-ins / experiment results / doc updates as work completes, with the standard trailers (Co-Authored-By + Claude-Session). Default pattern: branch → commit → ff-merge to `master`, local-only (matches the C2-band / D1-Phase-2 precedent).
- **Still gated (do NOT do without asking):** `git push` / opening PRs / anything leaving the pod — operator preference is **local-only, no GitHub** (also network-blocked from Claude's Bash). [[scope-gate-batch-is-deployment-model]]-style irreversible/outward actions still need a human gate.
- Exclude local-only files from commits (e.g. `.claude/settings.local.json`).
- The correctness LAWs and the supervised-promotion discipline are unchanged — "commit freely" is about the *git action*, not about lowering the bar for what counts as a promoted/proven result.
