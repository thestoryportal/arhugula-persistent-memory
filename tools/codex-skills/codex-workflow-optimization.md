# Codex Workflow Optimization

Use this note to keep Codex turns fast without weakening the repository guardrails.

## Worktree Hygiene

- Run `just codex-worktree-gc` as a dry-run when worktree buildup is suspected.
- Run `just codex-worktree-gc --reap` only after reviewing the dry-run candidates.
- The command removes worktrees only. It never deletes branch refs, never touches dirty
  worktrees, skips the current/default worktree, and requires merge proof by ancestry
  or exact merged-PR head SHA.
- Dirty leftovers should be preserved first with an explicit stash or commit, then the
  cleaned worktree can be removed.

## Verification Tiers

- Tier 0 context: `just codex-preflight`.
- Tier 1 focused: `just test-one <file-or-node>` or a tool-specific test file.
- Tier 2 Codex provider-free: `just codex-test` or `just codex-test <file-or-node>`.
- Tier 3 Codex PR-ready local gate: `just codex-check`.
- Tier 4 full/live: `just check` or live e2e recipes only when the operator explicitly
  intends live provider, Docker, cloud, or credentialed execution.

`just codex-test` and `just codex-check` strip live provider environment variables and
exclude `e2e` tests, matching the normal CI shape more closely when a local `.env` has
paid or credentialed provider keys loaded.

`just codex-check` also runs `uv sync --all-packages` before pyright so a fresh isolated
worktree does not waste a turn on unresolved workspace-package imports.

## Cache

The justfile exports `UV_CACHE_DIR=/tmp/arhugula-uv-cache` unless the operator already
set `UV_CACHE_DIR`. This avoids repeated Codex sandbox friction on the user home cache
while staying overrideable for normal local shells and CI.
