---
name: commit-forward-work-without-asking
description: Commit forward work freely, push every commit to the worktree branch, never merge; if a gate blocks an authorized action, have the operator relax it
metadata:
  type: feedback
---

**Operator directive (2026-06-20, robert):** Claude may **commit forward research work without asking each time** — the commit step is pre-authorized for all forward work (experiments, fold-ins, living-doc updates, infra). Do not pause to ask "should I commit?" for routine forward progress. **Push (2026-06-21, renewed by D-C10r-rulings-10 on 2026-10-07):** the remote is `github.com/thestoryportal/arhugula-persistent-memory` (public in 2026-06; PRIVATE per `gh repo view` on 2026-10-10) and the operator wants it current.

**Why:** keeps the durable git record current without round-trips; the operator was repeatedly approving commits ("Commit D1 fold in", "commit it") and made it standing. Extends [[standing-auth-forward-requirements]] to the commit action.

**How to apply (current rule, CLAUDE.md:17):**
- Commit fold-ins / experiment results / doc updates as work completes, with the standard trailers, on the worktree branch; then `git push origin <branch>` after every commit. **Never merge** — the operator merges.
- **General principle (2026-06-21):** when a permission/safety gate blocks an action the operator authorized *in intent*, **relax the control through the legitimate channel** (the operator edits the permission), **do NOT build a mechanism that routes around the gate** (hook, wrapper, subprocess). A post-commit auto-push hook was correctly rejected by the safety classifier as a permission bypass.
- `reset --hard` / `clean` / force-push stay gated (the deny list in `.claude/settings.json`).
- Repo hygiene: scope every `git add` and never commit tokens ([[git-add-all-leaks-secrets-on-public-repo]]); exclude local-only files (e.g. `.claude/settings.local.json`).
- The correctness LAWs and the supervised-promotion discipline are unchanged — "commit freely" is about the *git action*, not about lowering the bar for what counts as a promoted/proven result.
- History: until 2026-06 the pattern was branch → commit → ff-merge to local `master` on the pod; that is superseded by push-to-branch, never-merge.
