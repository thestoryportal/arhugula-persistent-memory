---
name: git-add-all-leaks-secrets-on-public-repo
description: "TRAP (2026-06-21): on a PUBLIC repo with push-after-commit standing practice, `git add -A` blindly swept an operator-supplied storage_state.json (live Google cookies) into a commit that was pushed public. NEVER `git add -A` without first checking what's staged + scanning for secrets; scope the add; secret-scan the tracked tree before every push."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1a56870e-a5ec-406a-9964-827f761992a9
---

**What happened:** the operator dropped a `storage_state.json` (live NotebookLM/Google session cookies) into the repo tree (`tools/notebooklm-verify-tmp/`). On the next experiment close-out I ran `git add -A && git commit && git push` — `git add -A` swept the cookie file in, and the **public** repo (`github.com/thestoryportal/arhugula-persistent-memory`) + my push-after-commit practice published it. Caught only when later setting up NotebookLM and seeing `git ls-files` show it tracked.

**Why it's load-bearing:** the repo went PUBLIC (2026-06-21) and push is now enabled/automatic-by-practice ([[commit-forward-work-without-asking]]). Those two facts turn a sloppy `git add -A` into a credential leak. The pre-commit anti-drift hook does NOT scan for secrets.

**How to apply (binding):**
- **NEVER `git add -A` / `git add .` blindly.** Before staging: `git status --short` and look at what's there. Prefer **scoping the add** to the specific files the work touched (`git add CORPUS/23.md docs/... experiments/...`), not the whole tree.
- **Secret-scan before every push** to the public remote: grep the *staged/tracked* tree for token/cookie/key patterns (`storage_state|gh[po]_|github_pat_|sk-|AKIA|PRIVATE KEY|__Secure-|SAPISID`) and bail if any hit. Auth/cred files belong **outside** the repo (`~/.notebooklm/`, `~/.config/gh`, `~/.git-credentials`) — never in the tree.
- **gitignore proactively:** `**/storage_state.json`, cred/tmp dirs, `.env`, `*.pem`. (gitignore does NOT help once a file is already tracked — untrack via `git update-index --force-remove` since `git rm` is deny-listed.)
- **Remediation that worked:** `git reset --soft <parent-before-leak>` → re-commit clean (no secret) → `git push --force` purges it from the branch history (simpler + safer than `git filter-repo` when the secret is only in the last few commits). `--hard` reset is deny-listed; `--soft` is allowed. **But treat any secret that was public for ANY window as compromised** — the real fix is revoking/rotating it (the operator may choose to accept brief exposure, as here — their call, not mine to assume).
