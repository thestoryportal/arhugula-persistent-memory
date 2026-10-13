# Astra review packet: ICM v2 phase 3 promote gate (G7)

You are the binding cross-family reviewer at a promote gate. Write in Simplified Technical English (STE): short sentences, active voice.

## Task

Review `git diff efef4529..4e679b15` on branch `corpus/icm-v2`. Your working directory is that worktree, at `4e679b15`. Decide if this branch can go to a PR and merge to `master`.

The branch restructures the repo `arhugula-persistent-memory` into an ICM workspace ("v2"): a short routing `CLAUDE.md` with generated twins (`AGENTS.md`, `routing.md`), one `CONTEXT.md` guide per folder down to the second level, generated `_index/`, stamped experiment and project records, a code map (`map/`), governance text fixed for the v2 layout, settings deny rules, Codex hooks, CI paths, and Mac-native readiness probes in the Codex context guard. The moves and path rewrites (steps 1 to 4) were reviewed and committed before `efef4529`. They are not in scope, except where a change in this range makes them false.

Approved design: `/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261012T114331Z-2ec28dcb/icm-v2/DESIGN.md`. Read "Target tree" (lines 37-61) and the phase table (lines 225-235). Phase 3's gate is: CI green; fingerprint `d941a9fb`; suite failures a subset of the baseline; resolver check; walk test; cold start at most 8k tokens.

Commits in range (oldest first):

- `77e98ebe` ICM v2 step 5a: move the CLAUDE.md and AGENTS.md payload to _system/governance
- `4de58f23` ICM v2 step 5e: generate _index/ and resolve old paths
- `3e25d9cb` ICM v2 step 5c: render the program state as short generated views
- `b61e40d5` ICM v2 step 5b: route from a short root CLAUDE.md with generated twins
- `60b69de7` ICM v2 step 5d2: add a guide to every folder down to the second level
- `57a3a6e9` ICM v2 step 5d1: stamp the experiment and project records
- `5232c10b` ICM v2 step 5f: add the code map catalog and noun index, with map/ twins
- `9471e82a` ICM v2 step 6d: fix governance text for the v2 layout
- `31a218fa` ICM v2 step 6c: point CI at the v2 test paths and check the indexes
- `97e03014` ICM v2 step 6a: make the settings deny rules match file edits
- `a060b972` ICM v2 step 6b: run the Codex hooks from any checkout of the repo
- `dc96d71b` ICM v2 item 7a: fix the guide text that failed the walk test
- `fdb8629f` ICM v2 item 7b: fix the guide text that failed the re-walk
- `1c014a52` ICM v2 step 6e: Mac-native readiness probes in the Codex context guard
- `d9d576b3` ICM v2 item 7c: fix the guide text that failed the final walk
- `7af51401` ICM v2 item 7d: fix stale guide paths found by the walk and a path trace
- `037c5715` ICM v2 item 7e: fix the guide text that failed the round-5 walk
- `4e679b15` ICM v2 item 7f: fix old-layout paths found by the round-6 walk

## What to check

1. Every guide statement in the changed `CLAUDE.md`, `CONTEXT.md` and `_system/governance/` text is true of the tree at `4e679b15`. A guide that sends a reader to a file, a section or a command that does not exist, or that does not work as written, is a defect.
2. Generated files match their generators. Do not read `_index/` row by row (32,700 of the 38,100 added lines). Run the checks instead (commands below).
3. Settings (`.claude/settings.json`), Codex config and hooks (`.codex/`), CI (`.github/workflows/ci.yml`) and `code/agents/codex_context_guard.py`: they do what their commit messages say, and they fail visibly, not silently.
4. The four MAESTRO rulings below. For each, reply CONFIRM or REJECT with a reason.
5. The open items below. For each, say if it blocks the merge (yes or no) and why.

Run these from the worktree root. The shell's global `LLMDB_ROOT` points at the old-layout main checkout, so always set it:

```
export LLMDB_ROOT=$PWD PYTHONPATH=code
.venv/bin/python -B code/state/build_index.py --check        # expect INDEX CLEAN
.venv/bin/python -B -S code/state/render_state.py --check    # expect all generated views current
.venv/bin/python -B -S code/agents/twins.py --check; echo rc=$?   # expect rc=0
```

The sandbox is read-only. Do not try to edit, commit or fix anything.

## Definitions and rulings (data)

**`verdict` stamp (step 5d1, `R/icm-v2/phase3/step5/5d1/status-map.md:3`):** "`verdict` means a terminal disposition is recorded. The outcome (pass, fail, inconclusive, or a non-experiment analysis) is in the cited source; read it before you use the record."

**Ruling 1, halt rule (6d).** `DISCIPLINE.md` § Halt discipline had two lines: the old CLAUDE.md rule (at most one speculative fix; halt only if that fix does not clear the gate) and the old AGENTS.md "One-fix-then-halt" line (halt after one fix, always). MAESTRO kept the CLAUDE.md wording (now `DISCIPLINE.md:130`) and dropped the AGENTS restatement (old `:133`).

**Ruling 2, in-weight memory contract (6d).** The AGENTS-sourced line ("not an F1 closure, unless the spec and operator explicitly accept that relaxation") and the North-star fallback rule govern different acts: classifying a closure, and recommending a fallback. MAESTRO kept both (`DISCIPLINE.md:13-20` and `:143-148`).

**Ruling 3, halt-diagnostic writers (new, for this gate).** `DISCIPLINE.md:131` and `DESIGN.md:155` put halt diagnostics in `experiments/<id>/runs/<slug>/halts/`. Eight live writers still write to `architecture_profile/`, which v2 git-ignores (group B guard, `efef4529`). The full inventory is `R/icm-v2/phase3/step6/6d/REPORT.md` § "Fix round 1", Defect 2. "Group A" means repoint the code. "Group B" means leave the code; its output lands in an ignored legacy root. MAESTRO decides:

| Writer | Owner status (`_index/experiments.md`) | Group | Action |
|---|---|---|---|
| `code/lab/track_c/c10y_directdw_arms.py:1290-1295,1600` | c10y: unstamped; `program/STATUS.md:23` lists it as ⭐ NEXT, halted at calibration | A | Not edited in this merge. The repoint (and its selftest) becomes a stated precondition of the next c10y authorization brief. The script's current hash is in no pin (the G5 rewrite already changed it), so any c10y run needs new pins and a prospective authorization anyway. |
| `b1_size_dose_response.py:128,144`, `d1_threshold_instrument.py:148,160,360`, `c10v_layerpick_arms.py:52`, `c10w_oracle_step0.py:431`, `c10x_enginepath_arms.py:287`, `c10z_astra_arms.py:1730`, `c10s_sharedz_read.py:64,67` (follow-up mode) | each owner stamped `verdict` | B | No change. A re-run needs a new authorization; that brief carries the repoint. |
| `c10s_sharedz_arms.py:54`, `c10t_secondkey_arms.py:56`, `c10u_mint2_arms.py:65`, `mathlab_runtime.py:287`, `run_c10z_v7_diag.py:110` | — | — | Already v2 shape, or follow their output dir. No change. |

Check: is it safe to merge with these writers as they are? Is a c10y run before the repoint possible without someone noticing?

**Ruling 4, walk-test bar (new, for this gate).** The handoff bar was a walk verdict of GO. No round gave GO. Each round's walker also audits every guide statement it opens, and each round found a new batch in a new place (6, 4, 2, 4, 3, 5, then 0 guide-text findings). Rounds 4-7 landed tasks 2-12 with no search. Round 7's only finding is the "⭐ NEXT" markers at `program/STATUS.md:23,30` on halted or closed items. That text is generated from `program/program_state.json` content, it predates v2 (the old runbook carried it), and choosing "what is next" is a program decision, not restructure scope. MAESTRO decides: the walk test passes for the merge; the ⭐ NEXT cleanup carries to the next program session (open item 9). Check: is that safe, or is any guide still false?

## Acceptance evidence (MAESTRO, on the M3)

- Generator checks on `4e679b15`: `build_index --check` INDEX CLEAN; `render_state --check` all generated views current; `twins --check` rc=0; `closeout_check --audit` AUDIT CLEAN.
- Engine fingerprint (`LLMDB_ROOT=$PWD .venv/bin/python -B code/memit/engine_fingerprint.py`): PASS on `4e679b15`, sha256 `d941a9fb…`, `_cov_cpu 3`. Earlier, at `a060b972`: PASS `d941a9fb`, `_cov_cpu 3`.
- Test suite vs baseline `res-old4` (44 files): on `4e679b15`, 0 regressions over 44 files (1,243 ok vs `res-old4` 1,221; `R/icm-v2/phase3/step6/7/suite/regressions-4e679b15.txt`). Earlier, at `a060b972`: 0 regressions (1,243 ok vs 1,221). The positive control `res-new2` still lists regressions.
- Walk test (fresh Sonnet, 12 tasks, guides only): round 1 NO-GO (6 findings, fixed in 7a), round 2 4 findings (fixed in 7b), round 3 on `1c014a52` 2 (fixed in 7c), round 4 on `d9d576b3` 4 plus a MAESTRO path trace (fixed in 7d), round 5 on `7af51401` 3 (fixed in 7e), round 6 on `037c5715` 5 plus a stronger path trace (fixed in 7f). Round 7 on `4e679b15`: tasks 2-12 land with no search; 0 guide-text findings; one finding on program-state content (see Ruling 4). Reports: `R/icm-v2/phase3/step6/7/walk-sonnet-r1.md` … `-r7.md`.
- Cold start (bytes/4): `CLAUDE.md` + root `CONTEXT.md` + `program/STATUS.md` + the largest folder guide (`map/CONTEXT.md`) = 16,086 bytes, about 4,022 tokens (round-7 walk; MAESTRO measured 15,808 at `a060b972`). Budget 8,000.
- `code/agents/test_codex_hooks.py` on the M3: 15/15 OK at `4e679b15` (CI skips the READY test off Darwin arm64). Mutation check: each of `test_mps_false_reaches_cli` and `test_missing_engine_reaches_cli` fails on its own mutant only (`R/icm-v2/phase3/step6/7/mutation-6e.md`).

(`R` = `/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261012T114331Z-2ec28dcb`.)

## Open items (MAESTRO proposes all as carry, not merge-blocking)

1. Settings gap: the `/path` deny rules protect only the session's own worktree. The main checkout has no `Edit` deny by absolute path. Planned for phase 5 (repo sync).
2. `_system/memory/codex-runs-inline-from-claude-bash.md` still recommends `-c mcp_servers.graft.enabled=false`, which fails on Codex 0.162.1. Protected path; its own small change.
3. Pod-era text at `_system/governance/WORKFLOWS_OVERVIEW.md:157-160`.
4. `_system/governance/STORAGE.md` is not yet in the D1 vocabulary.
5. Nine empty experiment folders (`deployment governance infra_scripts scale track_a`-`track_e`). Removal waits for operator approval.
6. `code/ops/intel/test_memit_intel_copy.py` fails 7 tests when `TMPDIR` is on the `/Volumes/memit` volume and passes on internal disk. Cause not found. The suite runner requires an internal-disk `SUITE_TMPDIR`.
7. The guard's running-process WARN also counts other non-exempt Python processes on the host (it reuses the `c10w_p2_gate` rule).
8. CI does not run `code/agents/test_codex_hooks.py`. MAESTRO runs it on the M3 before merge.
9. `program/STATUS.md:23,30` mark halted or closed items "⭐ NEXT" (generated from `program_state.json`; Ruling 4).
10. `_index/path-map.tsv` rows for the three split monoliths (`EXPERIMENT_RUNBOOK.md`, `SESSION_CHECKPOINT.md`, the v1.2 integrated spec) name the pre-split file. `code/state/resolve_path.py` resolves all three to their split folders; a raw TSV read does not.
11. `REPRODUCIBILITY.md:42,61` name output files in the ignored legacy roots `logs/` and `results/`. That is where those group-B scripts write when re-run.

## Output

Write one Markdown file (your `-o` path). Its first line is exactly `VERDICT: GO` or `VERDICT: NO-GO`. Then:

1. **Findings**, numbered. Each has: `file:line` at `4e679b15`, the defect in one sentence, the evidence (the command you ran and its output, or the quoted line), the fix, and a class: BLOCKING or CARRY.
2. **Rulings**: Rulings 1-4, each CONFIRM or REJECT with one reason.
3. **Open items**: items 1-11, each "blocks merge: yes/no" with one reason.
4. **Checks run**: each command and its result.

GO means: no BLOCKING finding, and no REJECT on a ruling that changes merge safety.

Do NOT write findings like these:
- "The guides could be clearer in places." (no `file:line`, no evidence)
- "`_index/experiments.md` row 41 looks odd." (a generated row; report a generator check failure instead)
- A defect in text that this range did not change and did not make false.
