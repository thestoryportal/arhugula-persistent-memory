---
name: git-add-all-leaks-secrets-on-public-repo
description: "Never `git add -A`: check `git status --short`, scope the add, secret-scan before every push; auth files live outside the tree"
metadata:
  type: feedback
---

**What happened:** the operator dropped a `storage_state.json` (live NotebookLM/Google session cookies) into the repo tree (`tools/notebooklm-verify-tmp/`). On the next experiment close-out I ran `git add -A && git commit && git push` — `git add -A` swept the cookie file in, and the **public** repo (`github.com/thestoryportal/arhugula-persistent-memory`) + my push-after-commit practice published it. Caught only when later setting up NotebookLM and seeing `git ls-files` show it tracked.

**Why it's load-bearing:** the repo went PUBLIC (2026-06-21) and push is enabled/automatic-by-practice ([[commit-forward-work-without-asking]]). (As of 2026-10-10 `gh repo view --json visibility` reports PRIVATE; the rule stands — visibility can change and pushed secrets stay in history.) Those two facts turn a sloppy `git add -A` into a credential leak. The pre-commit hook (`code/ops/git/hooks/pre-commit`, live via core.hooksPath) now blocks credential filenames and token signatures in staged changes. Still scope every add; the hook is a backstop, not a substitute.

**How to apply (binding):**
- **NEVER `git add -A` / `git add .` blindly.** Before staging: `git status --short` and look at what's there. Prefer **scoping the add** to the specific files the work touched (`git add evidence/CORPUS/23.md docs/... experiments/...`), not the whole tree.
- **Secret-scan before every push** to the public remote: grep the *staged/tracked* tree for token/cookie/key patterns (`storage_state|gh[po]_|github_pat_|sk-|AKIA|PRIVATE KEY|__Secure-|SAPISID`) and bail if any hit. Auth/cred files belong **outside** the repo (`~/.notebooklm/`, `~/.config/gh`, `~/.git-credentials`) — never in the tree.
- **gitignore proactively:** `**/storage_state.json`, cred/tmp dirs, `.env`, `*.pem`. (gitignore does NOT help once a file is already tracked — untracking requires authorization for the exact Git operation; never substitute a different command to bypass a denial.)
- **Historical remediation, not standing authorization (history rewriting and force-push require explicit approval and coordinated Git-writer reservation):** `git reset --soft <parent-before-leak>` → re-commit clean (no secret) → `git push --force` rewrites the affected branch history; it does not erase other copies or undo exposure. `--hard` reset is deny-listed; `--soft` is allowed. **But treat any secret that was public for ANY window as compromised** — the real fix is revoking/rotating it (the operator may choose to accept brief exposure, as here — their call, not mine to assume).
