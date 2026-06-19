# Deterministic Codex Context Workflow

Codex must not rely on remembered workflow state for load-bearing claims. This
note is the source of truth for preventing context rot, drift, and hallucinated
closeout in Codex sessions for this repository.

## Operating Principle

Every substantive Codex arc materializes state from repository instruments at
defined gates. Memory, checkpoints, prior chat, and dashboard prose are
orientation only until re-grounded against HEAD.

The `just` recipes are the mandatory command surface. Direct
`tools/codex_context_guard.py` invocation is equivalent only when it uses the
same mode and flags.

## Required Gates

For speed-oriented command choices that preserve these gates, use
`.codex/notes/codex-workflow-optimization.md`.

### 1. Preflight

Run before substantive work:

```bash
just codex-preflight
```

The preflight materializes:

- repository root, cwd, branch, HEAD, and linked-worktree status
- dirty status and changed files
- roadmap dashboard hash versus computed workspace hash
- open fork-doc count and latest retirement batch
- dashboard snapshot freshness when dashboard sources changed
- a local checkpoint artifact at `.harness/.checkpoints/codex-context-latest.json`

Hard failures stop work until resolved.

### 2. Edit Gate

All edits occur in isolated Codex worktrees. The root checkout is read/status
only. If the guard sees edits in the root checkout, the arc is invalid.

Do not mix design/spec/plan/fork-doc changes with implementation/test changes
unless the operator explicitly requested a design-phase/back-flow arc.

### 3. Cite Gate

For `C-*`, `U-*`, `H_T-*`, `ADR-*`, or CXA seam claims:

```bash
just overlay-query ...
```

Use `rg` for sibling `design-substrate/**` prose drift because the semantic
overlay intentionally does not scan sibling spec bodies.

### 4. Drift Recheck

After long work, merges, rebases, or context transition, rerun:

```bash
just codex-preflight
```

Treat memory/checkpoint "remaining work" as advisory until rechecked against
the current dashboard, git state, and source files.

For an explicit mid-arc checkpoint:

```bash
just codex-checkpoint mid-arc
```

The checkpoint records the current context fingerprint, HEAD, branch, changed
files, status entries, dashboard state, and findings. It is ignored by git and
exists to make context-refresh moments inspectable rather than remembered.

### 5. Closeout

Run before final response, commit, or PR:

```bash
just codex-closeout
```

Closeout checks:

- worktree-only edit discipline
- design/implementation boundary
- dashboard hash drift on the default branch
- stale committed human dashboard snapshot when dashboard sources changed
- cite-bearing changes that require `just overlay-check`
- missing tracking-surface review
- fresh checkpoint match against current HEAD/status/dashboard

The closeout recipe first writes a `pre-closeout` checkpoint, then runs the
closeout guard with `--require-fresh-checkpoint`. A stale or missing checkpoint
is a hard failure when freshness is required.

### 6. Credential Gates

Credential-gated units are not skipped. Codex drives the unit as far as it can
without credential material or paid-provider execution:

1. build the stdlib/mockable/provider-free slice
2. run the narrow verification that proves non-credential work is closed
3. stop at the exact credential or paid-provider gate
4. use an available HIL/operator-approval surface when one exists
5. when no HIL surface is available, log the gate for human review

Log the gate with:

```bash
just codex-credential-gate --unit R-NNN \
  --gate "OPENAI_API_KEY required for live mixed-provider e2e" \
  --forward-closed "provider-free tests passed; only live provider call remains" \
  --resume "ask operator for OPENAI_API_KEY authorization, then run the live e2e" \
  --command "OPENAI_API_KEY=<name-only> uv run pytest ..."
```

The command appends `.harness/codex_credential_gates.jsonl`, redacting
secret-like `NAME=value` fragments before writing. The ledger records only gate
metadata, never credential values.

After logging a credential gate, update a human-facing tracking surface
(`Project_Roadmap_v1.md` or `.harness/roadmap_status.md`) so the pending gate is
visible the next time a human engages with Codex. Closeout hard-fails if the
credential ledger changed without that tracking update. Once the gate is logged
and all non-credential forward actions are proven closed, Codex proceeds to the
next implementable unit instead of parking the session.

### 7. Tracking Surface Audit

No substantive task is complete until required tracking surfaces are updated or
explicitly reported as not applicable:

- `Project_Roadmap_v1.md`
- `.harness/roadmap_status.md`
- `tools/dashboard/roadmap.html`
- `.harness/substitutions.yaml`
- retirement batches under `.harness/phase-7d-retirement-events-batch-*.md`
- credential gates under `.harness/codex_credential_gates.jsonl`
- fork docs under `.harness/class_*_fork_*.md`
- axis `CLAUDE.md` / `AGENTS.md` files when posture changes
- clearance markers for design/spec/plan amendments
- memory entries when a pattern reaches the memory threshold

Dashboard snapshots have a stricter currentness rule: `.harness/roadmap_status.md`
is refreshed first, then `tools/dashboard/roadmap.html` is regenerated only with
`python3 tools/dashboard/generate.py --root .`. Do not hand-edit the snapshot or
copy volatile masthead values into it. `generate.py` derives visible `HEAD`,
`LAST`, `HASH`, `OPEN FORKS`, closure counts, and status-filter state from live
git/filesystem/roadmap inputs so stale count prose does not become durable UI.

The PR body or final response must report implementation status, verification,
tracking updates, and any owed follow-on refresh.

## Tool Contract

`tools/codex_context_guard.py` is the deterministic checker. It has three modes:

```bash
just codex-preflight
just codex-checkpoint <label>
just codex-credential-gate --unit ... --gate ... --forward-closed ... --resume ...
just codex-closeout
just codex-context-check
```

Related Codex-local optimization commands:

```bash
just codex-worktree-gc          # dry-run safe stale-worktree cleanup
just codex-worktree-gc --reap   # remove only clean merged worktree candidates
just codex-test                 # provider-free non-e2e pytest lane
just codex-check                # sync + lint + typecheck + provider-free non-e2e pytest
```

`codex-context-check` is the combined hard gate for local validation. It exits
nonzero on hard violations and requires a fresh checkpoint. The local closeout
and context-check recipes pass `--include-branch-diff`, so a clean feature
worktree is still checked against committed changes since the merge-base with
the default branch.

CI runs the guard directly without local checkpoint freshness because
`.harness/.checkpoints/` is intentionally untracked. The CI invocation passes
explicit `--base-ref` / `--head-ref` values from the GitHub event so the guard
checks the committed PR range instead of an empty clean-checkout status.
`--allow-dashboard-drift` only downgrades non-default-branch drift; it cannot
mask default-branch dashboard drift. When `gh pr list` is unavailable, the guard
emits `OPEN_PRS_UNAVAILABLE` instead of silently treating the open-PR set as
authoritative.

The Codex `SessionStart` and `Stop` hooks invoke the same guard. Hook failures
propagate nonzero when the guard reports a hard finding or cannot run.
