# MB45 — Drive r13 package for MAESTRO / Astra review round 13

Sandbox acceptance: **69/69 GREEN; zero failures/errors/skips; suite/driver exit 0**.
42 new methods plus all 27 byte-identical K12 tests pass against the r13 copies.
Host reruns, real candidate creation/commit/push/PR/CI/merge, native service,
activation and live Drive/science acceptance remain UNRUN. This is a review
package, not those acceptances. F1 connection: reproducible backup/release
integration preserves research evidence; no scientific interpretation changes.

Frozen reviewed K12: results/backup_gdrive_host_20261011/r12_package_20261011T024815Z/.
No K12 or Astra verdict was edited. The before/ originals are byte-identical;
K12's other accepted inputs are copied, with original paths also retained in
v4 scope/pins. protected_r13_after.json confirms all 561 protected entries have
identical bytes, size and mode (all seven production files, both backup tests,
K12 and gate/hygiene included). copied_inputs_audit.json verifies unchanged
copies. Source/root/branch/current and dispatched HEADs: source_context.json.
The shared HEAD advanced in another session during reading; root and branch
remained the same. MB45 ran no writing git command in the real repo.

## Test -> RED -> GREEN

| Controls | RED against exact K12 code | Final GREEN / exit |
|---|---|---|
| Candidate (19 original methods) | 18 assertion failures / 19, 0 errors/skips, group exit 1 | 19/19 pass, exit 0 |
| Added same-candidate three-mode round trip (1 method) | K12 writes no verified-SHA receipt; 1 assertion failure, exit 1 | 1/1 pass, exit 0 |
| Plan order / all 11 missing rows / empty row / command adjacency (16 methods) | 15 assertion failures / 16, 0 errors/skips, group exit 1 | 16/16 pass, exit 0 |
| Observed heads + gate report binding (6 methods) | helper absent; 6 assertions fail, exit 1 | 6/6 pass, exit 0 |
| All unmodified K12 tests (8 scope + 9 plan + 10 log) | Existing accepted r12 regressions, not new REDs | 27/27 pass, all group exits 0 |
| Combined new RED controls | 42 run, 40 expected assertion failures, 2 pass; 0 errors/skips; suite exits 1 | New 42/42 pass |
| Full final suite | Saved REDs precede new implementation | 69/69 pass, suite and driver exits 0 |
| Default filesystem executable probe | Existing accepted r12 behavior retained | PASS, capture exit 0 |

The original RED is r13_sandbox_red/ (41 run / 39 assertion failures).
The added round-trip RED is commands/r13_clean_pipeline_red/ (1 run / 1 failure).
RED driver exit 0 means its expected failing suites were reproduced; their own
suite exits are 1, never normalized into PASS. The final accepted GREEN is
r13_release_final_green/. The earlier r13_sandbox_green/ attempt (68 run, one
plan diagnostic failure) is preserved honestly; its extra command was refused
under CANDIDATE_ROW but also needed CANDIDATE_ORDER. The diagnostic was fixed
without changing the assertion. r13_sandbox_final_green/ has 68/68 pass before
the added round-trip. The final 69-method suite supersedes both earlier attempts.

For staged/commit REDs, test_r13.py's explicit adapter invokes K12's *existing*
verify mode, never rewritten code. Hidden bytes/modes/parents are accepted by
that legacy working-tree check. K12 has no PR/gate-binding API: those REDs are
missing-interface assertion failures (underlying exit 2), distinctly labelled.
The GREEN requires real refusal exit 1 and the named reason, never an arbitrary
unsupported-command failure. Synthetic repos and local bare origins are under
/private/tmp, with /usr/bin/python3 -B, isolated HOME, BACKUP_TEST_NO_RCLONE=1.

| Required negative / positive control | K12 RED observation | r13 GREEN observation |
|---|---|---|
| Out-of-scope tracked blob staged, working-tree bytes restored | verify accepts (exit 0); assertion fails | verify-staged refuses index tree mismatch (exit 1) |
| Allowlisted corruption staged, working-tree bytes restored | verify accepts (exit 0); assertion fails | verify-staged refuses index tree mismatch (exit 1) |
| Same two cases committed then working-tree bytes restored | verify accepts both (exit 0); assertions fail | verify-commit refuses commit tree mismatch (each exit 1) |
| Wrong executable mode in index / commit, working-tree mode unchanged | verify accepts both (exit 0) | corresponding full tree refuses (each exit 1) |
| Parent differs from origin/master / two parents | verify accepts both (exit 0) | only-parent check refuses (each exit 1) |
| Different PR head / different remote head | API absent (exit 2), binding assertions fail | three-SHA equality refuses (each exit 1) |
| Malformed observed SHA | API absent (exit 2) | SHA validation refuses (exit 1) |
| Ignored untracked file | legacy verify accepts (exit 0) | no-untracked gate includes ignored files (exit 1) |
| Clean candidate staged -> commit -> PR binding | legacy has no connecting SHA receipt | all three modes PASS using one verified SHA file |
| Complete committed tree, dirty working-tree bytes afterward | working-tree verifier refuses | commit-object verifier PASS; actual committed bytes are authority |
| Gate report wrong head / malformed report | helper absent (exit 2) | failure, never waiver (each exit 1) |

## Candidate modes and publication contract

create SOURCE_REPO SOURCE_COMMIT CANDIDATE_PATH retains K12 export/stage behavior
and then runs verify-staged. Branch stays backup-gdrive-r12 because that is the
approved PR/remote branch. It never commits/pushes/fetches/opens a PR.

verify-staged CANDIDATE_PATH SOURCE_COMMIT compares the entire stage-0 index to
origin/master's full recursive tree with exactly the literal source overlay,
including path, mode, type and blob. It then hashes index blobs through cat-file,
requires git diff --quiet, and rejects all untracked files, including ignored.
The old verify API delegates to this stronger staged gate for K12 compatibility.

verify-commit CANDIDATE_PATH SOURCE_COMMIT COMMIT_SHA [--receipt-file PATH]
compares the complete supplied commit tree and only parent to the base, hashes
commit blobs, then exclusively creates a fsynced SHA receipt. Default is
operational_checks/verified_commit_sha.txt. Plan/host actions use
operational_checks/r13_verified_commit_sha.txt. Existing receipt is a failure;
use a fresh reviewed receipt/label, never overwrite a successful binding.

verify-pr-head VERIFIED_SHA_FILE OBSERVED_PR_SHA OBSERVED_REMOTE_SHA requires
three valid equal full SHAs and makes no network call. gate_binding.py heads
validates saved gh JSON and exactly one ls-remote row for the approved ref and
calls that API; gate validates the gate report's head_sha against the same file.
The gate itself accepts no expected-head argument. Its existing protections
remain unchanged; the reserved/drained writer window is still a premise, with
both observations immediately before the gate and comparison afterward. Any
mismatch is a failure; preserve the report/merged SHA, never waive or undo.

## Plan v4 and Astra r13 map

activation_plan_v3.md is a byte-identical historical copy for the unmodified K12
regression test. Execute v4 only. check_plan CLI always requires the v4 candidate
sequence; the Python API retains historical v3/single-row primitive checks.
erratum_v4.md maps every changed v3 range to v4; plan_v3_v4_line_map.json also
maps all unchanged ranges and records exact before/after text. Declarations,
pin references, re-review labels and integration rows are the only changes;
activation/recovery/launch/install/successor/retirement logic is preserved.

Required correction from Astra, verbatim: "verify the staged tree before commit
and the exact candidate commit tree before publication/merge, including complete
path set, blobs and modes; bind that verified commit SHA to the PR head. Add
negative controls for staged contamination hidden by restored working-tree bytes,
committed contamination similarly hidden, and a different PR head."

| Astra r12 item 1 requirement | r13 file:line |
|---|---|
| Complete base/source tree entries | candidate.py:63 |
| Index path/blob/type/mode entries | candidate.py:73 |
| Base plus source overlay and unchanged exceptions | candidate.py:83 |
| SHA-256 pins from verified index/commit blobs | candidate.py:105 |
| Staged gate + working-tree/index equality + all untracked | candidate.py:138 |
| Commit tree, only base parent, durable exclusive SHA receipt | candidate.py:152 |
| Verified SHA = PR SHA = remote branch SHA | candidate.py:171 |
| Read-only gh/ls-remote observation parsing | gate_binding.py:9 |
| Gate report head_sha mismatch is a failure | gate_binding.py:20 |
| Missing/reordered/empty rows and immediate gate adjacency | check_plan.py:60 |
| Create -> staged -> commit -> commit verification -> push -> PR | activation_plan_v4.md:76 |
| Reserved-window dual observation -> binding -> gate -> report compare | activation_plan_v4.md:128 |

## Before/after SHA-256s

| File | Before SHA-256 (K12) | After SHA-256 (r13) |
|---|---|---|
| candidate.py | `d68c0f067b03390e233b86f27a0a7ccd55dc5d3781d4173746fdaeb7ae008af6` | `ce8f94b6043caf9e921070cf58ef77e5f6e8e78f168fbba3606ce7107706eb01` |
| check_plan.py | `cba298519ee2fdffccea12f855989a389e353e703bc32692183b2aa8d9620646` | `6bf4ea1ae6828ddc142f4f85a4b943b8a8cd93873c542e633b99c96c4c36872b` |
| activation_plan_v4.md | `3621a5e301fc126021b04bd0125ad0ee043812678711f304ffe92691aa3bab15` | `80ada7fd10c5c5416995865100f006f31767e64357a3a6686fa695cf18cde9e1` |
| freeze_receipt.py | `80da5ab83852e74c647dc7cf5fa2ad425bb1e7f3fe6aef09a6dc4b48fc843dd7` | `6131b3e66465ca08697feef9bb6bc85a6a619306305f5778f518814a751eaea7` |
| host_commands_r13.sh | `6512ba530cfb7a6d225c90ec2adbc9724d27151c9155140e0666f762fca34735` | `3e1f656fecfb7c38ccdc9e9563f80f50403e80bfa952afa82c2d88b25ddda37d` |
| source_context.json | `7a64f20c1eb42c03bed9a5e1860d06bed37dcbe2664fe8fe670ec471d94a7354` | `4aed1b6c0d356ea7b88591e29174f6b3dee671050a0d3bebccd09d69a5d96b4c` |
| test_r13.py | new | `c022d57f974e9c1554851f07eb632ab032b28a6d6eeb85fdbe7778b9d1a6e1f4` |
| run_r13.py | new | `1a5f148fd84ebc81189f604d9a9cdb229104932a4956c425e850d09ae369ce90` |
| gate_binding.py | new | `caf0507c5fbcab1ae2a488e14f55039a6ad70fa7cb81432edc8476ee65ec842d` |

README's before hash and final README/pin hashes are saved in
operational_checks/final_sha256.json, excluded from candidate scope to avoid
self-hashing. pins_v4.json/sha256 supersede and hash-link frozen K12 pins_v3;
no older manifest is edited. They retain all nine input hashes and the four
unchanged exceptions. Freeze after host evidence settles, then pins-final;
changed evidence/pins must be re-reviewed before source commit/candidate actions.

## Exact MAESTRO host commands

Run one action at a time from this worktree, inspect each saved stdout/stderr/
exit, and stop on nonzero. All action receipts use fresh r13_* labels; labels
and SHA receipts are exclusive and cannot be reused. Frozen r12 evidence stays
historical. These host runs were not performed in the sandbox.

```sh
R="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261011/r13_package_20261011T032105Z"
/bin/sh "$R/host_commands_r13.sh" pins
/bin/sh "$R/host_commands_r13.sh" check
/bin/sh "$R/host_commands_r13.sh" package
/bin/sh "$R/host_commands_r13.sh" fixture
/bin/sh "$R/host_commands_r13.sh" freeze
/bin/sh "$R/host_commands_r13.sh" pins-final
```

After host evidence/review/pins settle and MAESTRO commits this source receipt,
export MAESTRO_SOURCE_COMMIT (full reviewed source SHA) and
MAESTRO_CANDIDATE_PATH (fresh nonexistent isolated absolute path). Then:

```sh
/bin/sh "$R/host_commands_r13.sh" candidate
/bin/sh "$R/host_commands_r13.sh" verify-staged
```

MAESTRO commits the candidate as plan row 1.1-commit directs; capture rev-parse
HEAD and validate exactly one full SHA, then export MAESTRO_CANDIDATE_COMMIT:

```sh
/bin/sh "$R/host_commands_r13.sh" verify-commit
```

Only then push/open PR under GO using v4 rows 1.1-push/1.1-pr. Inside the reserved
merge window, set MAESTRO_PR_NUMBER from the validated saved PR output:

```sh
/bin/sh "$R/host_commands_r13.sh" verify-pr-head
```

Immediately run the existing merge gate per v4 row 1.1-gate. Its successful
JSON report path is MAESTRO_GATE_REPORT; compare before advancing:

```sh
/bin/sh "$R/host_commands_r13.sh" gate-head
```

Use either the plan's direct capture rows or host wrappers for these candidate
checks, not both on the same fixed labels/SHA receipt. If using wrappers, they
share exactly the same fixed SHA receipt and dual-source/gate semantics.
The full plan retains every existing operator/MAESTRO GO and STOP.

## Completion / successor handoff

Done: required new object/index/commit/head modes, same-candidate round trip,
plan v4/order gate, exact host wrapper, copied frozen inputs, before copies,
69-method acceptance, v3/v4 erratum, protected/copy audits and v4 freeze/pins.
No half-done code/test or in-flight sandbox process remains. Additional final
checks and their hashes are in operational_checks/. No production/gate/hygiene/
backup-test changes, real-repo writing git, remote rclone, launchctl, real HOME,
~/Library or ~/Applications writes, or unowned process termination occurred.
Small receipts and ephemeral Git fixtures stay under the 100 MB budget.

Next single step: MAESTRO runs host_commands_r13.sh pins, then advances each
host action above to Astra r13 review; no sandbox PASS authorizes activation.
MAESTRO alone updates docs/program_state.json and commits/publishes anything.
Open risks: host native/Drive/real PR/CI/merge behavior is UNRUN; the cooperative
writer reservation remains an operational premise, not server enforcement.

Context directive (binding operator 2026-10-10): watch Context N% left. Start a
new piece of work only at >=60% left. At <=40% left, or on any Context compacted,
stop starting work, append a handoff here with done/half-done, exact paths,
SHA-256s, test state and a single next step, then reply MB45 HANDOFF. Restate
this directive in every successor handoff. context_save.md preserves this arc
inside the only authorized receipt directory; no global memory update occurred.
