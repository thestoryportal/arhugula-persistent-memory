# GPT-6-Astra (high) — r13: Google Drive backup release package

Read-only. Worktree = current dir (branch `worktree-c10k-route-a`, HEAD `bdc1ad16`). Main checkout `M` = `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory`.

Your r12 verdict was NO-GO on one point (`results/backup_gdrive_host_20261011/astra_r12_verdict.md:5–16`): candidate verification read the working tree, so staged or committed contamination hidden by restored working-tree bytes could pass, and nothing bound the verified commit to the PR head. Your r12 accepted everything else; your rulings on freshness, statistics lines and self-pinning stand (`:31–56`). Builder MB45 answered in one new receipt **K13** = `results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/`. Its map is `K13/README.md:93–123`. Use it as an index only and cite raw files. K12's changed files are preserved in `K13/before/k12_before/`.

The question: **does K13 close r12 item 1, without reopening anything accepted, so that MAESTRO may create the backup-only candidate and take it through plan v4's gated sequence?** Rule on the finding and on each question below, then give one verdict line: GO, GO-WITH-CONDITIONS (numbered, each testable) or NO-GO.

## What changed (verify; do not take on trust)

- `K13/candidate.py`:
  - `index_entries` :73 (from `ls-files -s`);
  - `tree_entries` :63 (from `ls-tree -r`);
  - `expected_tree` :83 (origin/master's full tree overlaid with the allowlisted source entries);
  - `compare_tree` :133;
  - `verify_staged` :138 (index vs expected, worktree == index, no untracked files);
  - `verify_commit` :152 (commit tree vs expected, sole parent = origin/master; writes the verified-SHA receipt);
  - `verify_pr_head` :171;
  - `create` :178 (stages, then runs verify-staged).
- `K13/gate_binding.py`: `heads` :9 (PR head and remote head vs the verified SHA); `gate` :20 (the gate report's head_sha vs the verified SHA).
- Plan v4 `K13/activation_plan_v4.md`, erratum `K13/erratum_v4.md`, line map `K13/plan_v3_v4_line_map.json`. Host entry: `K13/host_commands_r13.sh` (candidate, verify-staged, verify-commit, verify-pr-head, gate-head).
- Tests: `K13/test_r13.py`. RED first (`K13/r13_sandbox_red/`: 42 controls, 40 expected failures) against K12's candidate; GREEN 69/69 including all 27 K12 tests (`K13/r13_sandbox_final_green/`).

## Host evidence (MAESTRO32, niceness 0, this Mac)

`K13/operational_checks/maestro_host_20261011T033648Z/rcs.txt`: pins, check, package, fixture, freeze, pins-final, all rc=0.
- Plan check: `K13/commands/r13_host_plan_check/stdout.txt` = `PASS []`.
- Package: `K13/commands/r13_host_package_driver/stdout.txt`: Candidate 20, PlanOrder 16, BindingReceipt 6, Scope 8, Plan 9, Log 10. Zero failures, errors or skips.
- Fixture: `K13/r13_host_local_check/driver.stdout.txt`: clean, excluded-only and symlink pass; same-size corruption fails on alpha.txt.
- Freeze: `K13/operational_checks/commands/r13_host_freeze/stdout.txt`: 1,187 scope paths, 1,185 pins, 8.2 MB.

## MAESTRO32's questions (rule on each)

1. **Binding window.** The gate takes no expected-head input (`tools/git_merge_gate.py:170–200`). Plan v4 runs verify-pr-head inside the reserved window immediately before the gate, and gate-head afterwards. Between those two, only the cooperative reservation stops the head moving. If it moves, gate-head only *detects* the problem after the merge. Is that binding adequate, or is a stronger one needed without modifying the gate (e.g. the gate's own start-of-run head capture compared before merge)?
2. **Contamination coverage.** Do the RED controls cover the cases you named? Out-of-scope and allowlisted contamination, staged and committed, hidden by restored working-tree bytes; wrong modes; a non-master parent; a different PR head or remote head. Are any variants still open (a submodule/gitlink entry, a deletion of an origin/master path, a rename, a case-only path difference on APFS)?
3. **Scope growth.** The candidate scope grew from 504 paths (r12) to 1,187 (8.2 MB), largely by copying K12 inputs into K13. Is a backup-only PR carrying r11–r13 evidence the right scope, or should it carry only the production/test files plus the final receipt?

Not yet run, by design: candidate creation and verification, push, PR creation, the merge gate, and activation. Activation needs the operator's OKs on the ~287 GB read-back and the write pause.

Write the verdict to the `-o` file. Cite file:line for every claim.
