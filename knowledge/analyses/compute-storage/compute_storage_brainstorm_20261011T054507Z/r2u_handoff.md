# R2U handoff — context gate; RESUME, DO NOT RESTART

MAESTRO ordered this handoff at 45% context. The command in progress finished; no new work started. The required report is NOT written, so READY is not yet warranted.
Worktree: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
Branch: worktree-c10k-route-a. B = results/compute_storage_brainstorm_20261011T054507Z; paths below are relative to B unless absolute.

## Authority and boundaries
V9 astra_r2l_verdict.md and D13f r2_round10_decisions.md were read in full first/second; D13 binds. D9 r2_round9_decisions.md was read in full; D10–D12 remain binding. Do not reopen these rulings.
Inputs C/F7/J6/K6/P4/I6/V9/D13f/D9/D8/DR/O8 were never edited. r2u_input_pins.json captures their 12 SHA256 values; the last verification found all unchanged.
No commits, Git mutations, science/native launch, project Python, .venv, uv, tmux, graft, web or sandbox-exec. Use /usr/bin/python3 -B only. Runtime containment and commissioning remain UNVERIFIED; Gate 1 OPEN pending Astra round 10; all 18 parent cases + 10 subcases UNRUN.
Read discipline: never read P/J/K or source files whole. Locate with rg/grep, sed ranges <=40 lines, or short system-Python snippets printing one record. New artifacts were copied from their specified inputs and changed by script. I7 changed only three factual summary lines.

## Built artifacts — exact final bytes; accepted, do not edit casually
```text
61c21fada5da7de5aa8f60b1c36e7d1bc544f8ef7a1e7cc47f3f0d7007d607e9  results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v8.md
22c05403e421615ce13a46e1461270e0a82226556b397830d9cbfb248ffb6424  results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_schemas_v7.json
09e7c86c2077d9944cde70cee3a7e85c63b59002330d8438ba38a3d55a3c9600  results/compute_storage_brainstorm_20261011T054507Z/check_r2_schemas_v7.py
94992853eb83d36673254611c6b88204981d7c90a5ad04dfb8c4aaf6c0588c0f  results/compute_storage_brainstorm_20261011T054507Z/science_launch_profiles_v5.json
a11f5c9a65e0a9151101983002b133386f1f75b4f0c9d1fa3aa77237045103d9  results/compute_storage_brainstorm_20261011T054507Z/science_launch_inventory_v7.md
```
F8 remains 360 lines. Its §8 pins J7/P5/I7 from computed shasum values; final pin verification passed for all three. F8 §9 at :336,339,359–360 records V9 R1, exact grep commands/hit lists, reached process starts and reviewed call edges; earlier R2/R3/R4/R5/R6 mappings remain at :340–344.
J7 admission_trace begins :40752; P5 admission_trace begins :434882. K7 trace_hits :2336; traced_occurrences :2355; round10_checks :2385; mutation controls :2439; aggregate maxima :1851.

## What changed
K7 removes the hand-written ADMISSION_NAMES mechanism. It reruns 13 recorded source queries, compares hit sets and source pins, and derives occurrences from recorded root selectors, process sites, supported stages and per-profile recipe sets. Unreviewed admission stages/applications refuse.
Six gate-bearing profiles [23,26,29,32,35,38] gain six admission-origin verify-preflight occurrences plus six p2-eval Git occurrences (12 new records). All 42 derived admission-origin occurrences require ADMISSION_HELPER / C:115 / PRE_RELEASE_REQUIRED, retain NOT_ADMITTED_ADMISSION_HELPER_UNREGISTERED: composition refusal, and have no A1 authority.
Science-origin verifier/Git uses remain separate with A1. The evaluator fingerprint occurrence in profile 38 also retains SCIENCE/A1; the gate fingerprint stays ADMISSION/C:115. Existing legitimate science records were retained.
Trace includes imported T.require_training_preflight and R.phase_trains, verifier child entry/conditional P3 replication branch, and re-attempt A.check_reattempt / A.overlay. Current admissions are P2; the verifier's P3-only Git branch is conditional and absent there. This is reproducibility/completeness for recorded lexical queries, NOT a complete call graph. No C:115 helper registration mechanism is established.
Origin and trace-site fields are required by the exact child schema. Construction profile/context/binding hashes and broker argv identities were rebased; production broker argv hash references were added. Existing R8R4 mutation children now carry required origin fields so the control reaches its original 65-input error; its assertion/expected reason was not weakened.
All 55 aggregates are built: 25 TOP_LEVEL maxima 36 inputs / 4271 UTF-8 bytes; all-profile maxima 54 / 5477. Frozen bounds remain 64 / 8192 / 262144.

## Test-first RED and acceptance — finished
r2u_test_first_red.log was saved BEFORE building F8/J7/P5. K7 against F7/J6/P4 had exit 1 separately for verify-preflight and git-ls-files, each explicitly misclassified SCIENCE_CHILD/DECLARED_AT_ROOT_ADMISSION/D-R2C-A1; no crash/unrelated failure. Full commands and branch errors are saved.
Acceptance 1: /usr/bin/python3 -B B/check_r2_schemas_v7.py — final exit 0. r2u_acceptance_default.log: GREEN; 114 schemas, 17 request kinds, 259 examples, 1411 hash references, 8 bindings, 16 observations.
Acceptance 2: /usr/bin/python3 -B B/check_r2_schemas_v7.py --profiles B/science_launch_profiles_v5.json — final exit 0. r2u_acceptance_profiles.log: GREEN; 55 profiles, 174 refusals, 737 bindings; 13 queries / 42 admission-origin occurrences; maxima above.
Acceptance 3: /usr/bin/python3 -B B/check_r2_schemas_v7.py --mutation-controls — exit 0, 50 unique intended RED (46 preserved + four D13). r2u_acceptance_mutations.log contains every exact error and the final GREEN line. New controls: R10A verifier A1; R10B Git A1; R10C removed train:65 hit; R10D merged origins. All fail for their intended reasons.
Census files: r2u_census_before.json, r2u_census_after.json, r2u_census_summary.json. All log/census files existed before the before-census. Mutation run B files 193→193, entries 193→193; task TMPDIR files/entries 1→1, created=[], removed=[] for both roots.
Task TMPDIR: /var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/r2u_census_25cr3kvj. Ambient TMPDIR had an Apple-protected directory; a fresh task-specific TMPDIR was allocated before census, following predecessor practice. macOS Python's xcrun_db cache was warmed before census. The cache file existed in both snapshots; the checker created no new files/directories during the measured run. No deletion/cleanup was performed.
r2u_acceptance_summary.json records all three commands and exit 0 results, outputs 1/2, and census 3. Initial failed overflow-fixture/census evidence remains in r2u_initial_mutation_failure.log and r2u_initial_census_failure.json. The initial failure was corrected, never counted as acceptance.

## Exact next step — only delivery remains
Write B/r2u_report.md (<=60 lines) from the already accepted bytes and saved receipts. Include the five computed SHA256 values above, R1 changes and closing lines, both test-first branch failures, and acceptance outputs 1–3. To fit all 50 exact RED messages, group multiple complete RED lines on a report line, and link the full mutation log; do not weaken or omit controls. State lexical limits and static-only proof. Recompute output hashes for the report with shasum, check report line count, and confirm its recorded hashes match; do not edit tested subjects.
Then reply on its own line exactly: R2U FIX READY results/compute_storage_brainstorm_20261011T054507Z/r2u_report.md
MAESTRO performs the read-only sandbox proof and Astra round-10 review. No sandbox-exec here. No further acceptance rerun is needed unless an accepted subject changes or a new concern appears.
Scratch build helpers remain under /private/tmp/r2u_*.py and /private/tmp/r2u_checks.txt; /private/tmp/r2u_intermediate.json is intermediate construction state, not final authority. Do not rerun builders: late inventory/aggregate facts and pins were finalized after construction. Resume from the accepted saved files.

## Durable context rule
Manage context for this session and every team session. Start a new piece only at >=60% context left. At 45% left, or on any Context compacted, stop starting new work, finish only the command in progress, and write B/r2u_handoff.md with done/in-flight work, exact paths/state, next step and risks. Never append a late handoff to the report or any tested file; it breaks tests/pins. Reply R2U HANDOFF unless already fully finished. Project <=40% is a floor; this brief's 45% threshold governs. Every successor handoff restates this rule.
Learning: occurrence origin decides authority; identical recipes may be reachable from admission and science. Schema evolution must update mutation fixtures so intended counterexamples remain RED for their own reason.
