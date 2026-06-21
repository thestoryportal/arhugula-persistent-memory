# Anti-drift system (how the context docs stay synced)

Reconciled design (Opus advisor + gpt-5.5 cross-family, 2026-06-21). Goal: end perpetual
documentation drift WITHOUT the false-green of "fingerprint everything" or the impossibility
of "auto-rewrite all prose". Honest boundary: it **auto-ENFORCES** currency (no stale commit
lands) and **auto-UPDATES** structured/generated status; it does **not** auto-write narrative
prose, and it only guards **registered** edges — so the primary cure is *not duplicating*.

## The three layers

1. **De-dup (the real cure).** Full detail of a result lives in ONE source (its `CORPUS/NN`
   writeup / the amendment / `docs/program_state.json`). Every other doc carries a thin
   self-contained summary: **Decision-ID + one-line verdict + pointer** — never a restated copy
   of evolving numbers/caveats/tables. Copying is what manufactured the k≤2→k≤1 drift.

2. **GENERATE what's mechanical** — `docs/program_state.json` → `tools/render_state.py`.
   Structured status (F1 scorecard, current-position/next-actions, governance status) is rendered
   into `<!-- BEGIN GENERATED:<block> --> … <!-- END GENERATED:<block> -->` regions in
   PROGRESS ⑤, runbook §0.3, SESSION_CHECKPOINT, SESSION_BOOTSTRAP, README.
   - Edit `docs/program_state.json`, then `python3 tools/render_state.py --write`. **Never edit
     between the markers.** `--check` = is any block stale (used by the hook).

3. **FINGERPRINT what's narrative** — `tools/closeout_check.py` + `tools/closeout_fingerprints.json`.
   Each result's canonical SOURCE span is content-hashed; every doc referencing the D-ID must carry
   `<D-ID>@<hash>`. Source change → hash change → dependents read STALE.
   - `--fp <D-ID>` prints the current token; `--currency <D-ID>` checks one; `--audit` checks all;
     `closeout_check.py <D-ID>` = presence + currency for an active close-out.

## Enforcement (automatic, every commit)
`tools/git_hooks/pre-commit` (installed via `git config core.hooksPath tools/git_hooks`) BLOCKS a
commit if `render_state.py --check` finds a stale generated block OR `closeout_check.py --audit`
finds a stale registered fingerprint. Bypass (rare/WIP): `git commit --no-verify`.

## Close-out workflow for a new/refined result
1. Write the ONE detailed source (`CORPUS/NN` / amendment).
2. Edit `docs/program_state.json` → `python3 tools/render_state.py --write`.
3. Register the source span in `tools/closeout_fingerprints.json`; stamp `<D-ID>@<hash>` in narrative refs.
4. Update ledgers with **pointers, not copies**.
5. `python3 tools/closeout_check.py <D-ID>` → ✅; commit (hook re-verifies).

## What it deliberately does NOT do
- Fingerprint process docs (DISCIPLINE/CLAUDE/AGENTS) or the spec — they don't restate results.
- Guarantee zero drift across arbitrary prose — only registered edges + generated blocks. An
  unregistered restatement still drifts; the defense is the de-dup norm (don't restate).
- Auto-write prose. Stale narrative must be edited by an agent; the hook just won't let it commit.
