VERDICT: NO-GO

Reviewed `efef4529..4e679b15` on `corpus/icm-v2`. The worktree remained clean at `4e679b15ce92a83e9c0b3929ccd552f0b0d14ee1`.

The generator checks pass. Four defects block this gate. No file was edited.

## Findings

1. **BLOCKING — `code/state/resolve_path.py:83`: The resolver returns obsolete fragments for two rewritten runbook headings.**

   **Evidence:** I ran:
   ```sh
   LLMDB_ROOT=$PWD PYTHONPATH=code .venv/bin/python -B code/state/resolve_path.py \
     'EXPERIMENT_RUNBOOK.md#a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1'
   ```
   It returned:
   ```text
   program/runbook/08-experiment-decision-tree-tracks-af.md#a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1
   ```
   The heading at `program/runbook/08-experiment-decision-tree-tracks-af.md:13` now contains `evidence/CORPUS/14`. Its current fragment is:
   ```text
   a1--batch-vs-sequential-write--done--pass-robust-evidencecorpus14-d-a1-1
   ```
   The A2 heading at line 46 has the same defect. My check of all 517 sealed anchors found these two missing destination fragments. The resolver selects the correct file, but its fragment does not select the section. `build_index.py --check` still reports `INDEX CLEAN`.

   **Fix:** Map each historical fragment to both the current part and its current fragment. Add tests that verify the destination fragment exists. Do not test only the returned string.

2. **BLOCKING — `_system/governance/DISCIPLINE.md:49`: The close-out instructions falsely state that the renderer refreshes the old embedded status blocks.**

   **Evidence:** The line says:
   > “refreshes the generated status blocks in PROGRESS ⑤ / runbook §0.3 / checkpoint / bootstrap / README”

   `code/state/render_state.py:18–20` now defines only three targets:
   ```text
   program/STATUS.md
   _index/program-state.md
   program/scorecard.md
   ```
   The check command reported those three targets only. Step 5c made the quoted instruction false. `_system/governance/OPERATING-MODEL.md:15` also describes the runbook state as an embedded generated block.

   **Fix:** Name the three current views. Explain that the former entry points link to them. Distinguish sealed checkpoint history from current generated state.

3. **BLOCKING — `code/tests/CONTEXT.md:6`: The guide says CI still uses the old test path, although this range fixes that path.**

   **Evidence:** The guide says:
   > “CI reader at the new path: none found. `.github/workflows/ci.yml` still names an old tests path.”

   `.github/workflows/ci.yml:44` runs:
   ```sh
   LLMDB_ROOT="$PWD" python3 -B -S -m unittest discover -s code/tests -p test_git_automation.py -v
   ```
   The related “Reader search: none found” claims in `code/apps/CONTEXT.md:6` and `code/lab/CONTEXT.md:6` also omit the suites now named at `.github/workflows/ci.yml:46`.

   **Fix:** Update these reader statements to name the current CI commands and their modules.

4. **BLOCKING — `_system/governance/WORKFLOWS_OVERVIEW.md:12`: The workflow guide directs readers to `CLAUDE.md` for rules that this range moved out of that file.**

   **Evidence:** The canonical-source table assigns “Engine LAWs … + close-out gate” to `CLAUDE.md`. Line 130 repeats that location. The current `CLAUDE.md:8` explicitly says:
   > “It does not contain the rules.”

   The rules now live in `_system/governance/DISCIPLINE.md`, including the correctness gates at line 120, halt discipline at line 128, and close-out gate at line 134. This defect follows directly from steps 5a and 5b.

   **Fix:** Point the workflow table and section heading to the current governance sections. Keep `CLAUDE.md` described as the routing entry point.

## Rulings

1. **CONFIRM.** Keeping the conditional halt rule preserves the stated CLAUDE rule. It permits at most one speculative fix. It requires a halt if that fix does not clear the gate. Removing the conflicting AGENTS restatement is sound.

2. **CONFIRM.** The passages govern different decisions. One controls closure classification under an explicitly accepted contract change. The other forbids recommending a rejected fallback as the readiness path.

3. **CONFIRM, within the stated authorization boundary.** The deferred repoint can accompany the next authorized run. I tested C10Y’s read-only `preflight(env={})`. It raised `Halt: PREREG SHA MISMATCH`. `main()` calls that preflight before launch authorization and worker creation. Thus, the current entry point cannot silently reach calibration at this tree.

   This result is stronger than the claim that the driver has no current pin. Absence of a pin alone would not prove a launch refusal. The next C10Y authorization must retain the repoint and selftest as prerequisites when it repairs the pins. The terminal-owner scripts remain subject to new authorization before a rerun.

4. **REJECT.** Carrying the old `⭐ NEXT` content is reasonable for this restructure. It does not establish a passing guide audit. Findings 2–4 show that guide claims remain false at the reviewed head. Finding 1 also leaves the resolver incomplete. The round-7 report does not cover these defects.

## Open items

| Item | Blocks merge | Reason |
|---|---|---|
| 1. Main-checkout Edit gap | **no** | The rules protect the session worktree. The separate main-checkout gap is an explicit phase-5 carry. The current rule forms match the documented permission semantics. See [Claude Code permissions](https://code.claude.com/docs/en/permissions#read-and-edit). |
| 2. Old graft override in memory | **no** | This protected memory text is outside the range. The changed governance commands remove the override. |
| 3. Pod-era workflow text | **no** | Lines 157–160 predate this range. This range did not make those deployment claims false. Finding 4 concerns a different claim that this range did invalidate. |
| 4. STORAGE vocabulary | **no** | A vocabulary update can carry. The existing storage and deletion constraints still apply. |
| 5. Nine empty experiment folders | **no** | Empty folders do not enter Git. The index uses Git-carried paths. Removal can wait for authorization. |
| 6. Intel-copy TMPDIR failures | **no** | The baseline comparison uses internal-disk temporary storage. The saved current receipt lists all 30 Intel-copy tests as `ok`. This does not establish correctness on the memit volume. |
| 7. Broad process warning | **no** | The guard deliberately reuses the compute-process rule. This produces a warning, not a false science verdict or a hidden failure. |
| 8. Hook tests absent from CI | **no** | The packet provides a separate M3 qualification and mutation receipt. Keep that check required for the final candidate until CI covers it. |
| 9. Stale `⭐ NEXT` markers | **no** | These markers come from pre-existing program-state content. Their correction belongs to the next program decision. They do not authorize a run. |
| 10. Pre-split TSV destinations | **no** | The resolver translates all three monolith paths to existing split folders. Raw-map normalization can carry. The separate fragment defect in Finding 1 blocks this gate. |
| 11. Legacy reproduction outputs | **no** | Those paths describe where the retained group-B scripts write. They are not instructions to treat ignored output as committed evidence. |

## Checks run

All repository Python checks used `LLMDB_ROOT=$PWD` and `-B`. They used `PYTHONPATH=code` unless stated otherwise.

| Command or read-only check | Result |
|---|---|
| `git rev-parse --show-toplevel`; `git branch --show-current`; `git rev-parse HEAD`; `git status --short` | Correct worktree and branch. Exact reviewed head. Clean before and after review. |
| `git diff --stat efef4529..4e679b15`; `git diff --name-only efef4529..4e679b15`; targeted `git diff` reads | Reviewed the changed file set and implementation diffs. |
| `.venv/bin/python -B code/state/build_index.py --check` | Exit 0; `INDEX CLEAN`. |
| `.venv/bin/python -B -S code/state/render_state.py --check` | Exit 0; all three generated views current. |
| `.venv/bin/python -B -S code/agents/twins.py --check; echo rc=$?` | `rc=0`. |
| `.venv/bin/python -B code/gates/closeout_check.py --audit` | Exit 0; 43 registered fingerprints current; `AUDIT CLEAN`. |
| `.venv/bin/python -B code/memit/engine_fingerprint.py` | PASS; SHA-256 `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65`; `_cov_cpu 3`. |
| In-memory `build_anchor_map()` comparison | Generated bytes equal `_index/anchor-map.tsv`. No output file written. |
| Resolver checks for `tools/closeout_check.py` and the three original monolith paths | All resolve to existing destinations. |
| Resolver destination-fragment check across 517 sealed anchors | **FAIL:** two returned fragments do not exist in their destination files. See Finding 1. |
| YAML stamp check across 48 experiment guides and nine project guides | IDs, listed code/run/output paths, and populated preregistration hashes passed. |
| Cold-start byte count | 16,086 bytes, or 4,021.5 tokens by bytes/4. Below 8,000. |
| Seven selected `test_codex_hooks.HostProbeTest` tests | All passed. Covered MPS refusal, missing engine, warnings, failed optional probes, memory parsing, process filtering, and visible command failure/timeout. Used `PYTHONPATH=code:code/agents`. |
| `c10y_directdw_arms.preflight(env={})` | Refused with `PREREG SHA MISMATCH`. No worker or model run started. |
| Saved suite receipt inspection and status recount | 44 receipt files; 1,243 normalized `ok` tokens. The saved comparison reports zero token, exit-code, or load/missing/timeout regressions. |
| Saved settings control logs | Protected Write denied; allowed Write succeeded. Logs disclose ignored allow/additional-directory entries for the untrusted scratch project. |
| Saved round-7 walk and hook mutation report | Read. Walk verdict remains `NO-GO`. Mutation report records each negative test failing on its own mutant. |
| `gh api …/commits/4e679b15…/check-runs` | Could not connect to `api.github.com`. |
| GitHub connector workflow-run query for the exact SHA | Connector not connected. Hosted CI remains **UNVERIFIED** here. |

I did not rerun the full suite or the full native hook suite because those checks create fixtures or use host probes. Their saved receipts remain distinct from the read-only checks above. Exact-head PR CI and post-merge master CI remain required under phase 4.