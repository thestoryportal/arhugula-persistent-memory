# Astra review round 10 — shared-disk clearance freeze v8, schemas v7, checker v7, launch inventory v7 and profiles v5 (R2 / I1b, Gate 1)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. You may run the checker below with `/usr/bin/python3 -B` (stdlib only; it writes no files, and its mutation controls run in memory); run nothing else. Repository HEAD is the commit that adds this packet. P5 is 435,728 lines and J7 41,598: read them by targeted search (e.g. `grep -n`), never in full.

Aliases: `B` = `results/compute_storage_brainstorm_20261011T054507Z/`; `C` = `B/shared_disk_clearance_contract_v1_1.md` (sha256 25c93f5f584d5a1dfff3b0610b32922a289be6d91449765862de3331334062f1, unchanged); `V9` = your round-9 verdict `B/astra_r2l_verdict.md` (sha256 a551d35ef6db3ad14889919b58159b87ebf7091cc7c8dff50fba6869f2d90c44), NO-GO with F1 (high), F2–F4 (notes) and one required change, R1, at V9:46. Round-9 subjects remain in the tree unchanged for comparison: F7, J6, K6, P4, I6.

Subjects, sha256 and lines:
- `F8` = `B/shared_disk_clearance_freeze_v8.md` 61c21fada5da7de5aa8f60b1c36e7d1bc544f8ef7a1e7cc47f3f0d7007d607e9 (360). Pins P5, J7 and I7 at F8:326–331. §9 maps V9 R1 at F8:336, :339 and :359–360; earlier mappings at :340–344.
- `J7` = `B/shared_disk_clearance_schemas_v7.json` 22c05403e421615ce13a46e1461270e0a82226556b397830d9cbfb248ffb6424 (41,598); admission_trace begins at J7:40752.
- `K7` = `B/check_r2_schemas_v7.py` 09e7c86c2077d9944cde70cee3a7e85c63b59002330d8438ba38a3d55a3c9600 (2,524); trace_hits :2336, traced_occurrences :2355, round-10 checks :2385, mutation controls :2439.
- `P5` = `B/science_launch_profiles_v5.json` 94992853eb83d36673254611c6b88204981d7c90a5ad04dfb8c4aaf6c0588c0f (55 LaunchProfiles, 174 not_admitted entries); admission_trace begins at P5:434882.
- `I7` = `B/science_launch_inventory_v7.md` a11f5c9a65e0a9151101983002b133386f1f75b4f0c9d1fa3aa77237045103d9 (263).
- `D13f` = `B/r2_round10_decisions.md` 8d9f39f2f6aee4bb37ff50dd2155648aabc9dcf3c836b6ed85f5d7395611ecfc (36; MAESTRO55). Ruling D13 answers V9 R1: a process's role follows its origin, not its recipe, and the admission audit is a recorded transitive trace that K7 recomputes. It does not amend C; A1 (`B/r2_round8_decisions.md`) and D10–D12 (`B/r2_round9_decisions.md`) stand. Judge D13 as a freeze change.
- Builder records: `B/r2u_report.md` 17523a27465beac9801ccbbda75e3ede5779c46e0befed2f14e2c6e7bf72eeb0 (51), `B/r2u_handoff.md`, briefs `B/codexr2u_brief.txt` and `B/codexr2u2_brief.txt`, input pins `B/r2u_input_pins.json`, censuses `B/r2u_census_*.json`, summary `B/r2u_acceptance_summary.json`, first-attempt evidence `B/r2u_initial_census_failure.json`. MAESTRO's rerun is `B/r2u_maestro_acceptance.md` e09af0d8072f184dabadbf7ee5a86c77e45e2274a91bd18d6d2b0414b476c849 (84).

Process record (disclosed so you can weigh it):
1. Builder codexr2u wrote K7's D13 checks first and ran them on F7/J6/P4. They failed separately for the verify-preflight branch and the git ls-files branch, each misclassified as SCIENCE_CHILD / DECLARED_AT_ROOT_ADMISSION / D-R2C-A1 (quoted in r2u_report.md; the raw log is git-ignored). It built F8/J7/K7/P5/I7 and ran acceptance 1–3. A first mutation/census attempt failed on an overflow fixture; it was corrected and not counted as acceptance. It handed off at its context limit before writing the report.
2. MAESTRO55 recomputed the hashes, confirmed that all 12 pinned inputs are unchanged, and reran acceptance from its own shell. Default: exit 0. `--profiles P5` and `--mutation-controls` ran under `sandbox-exec` denying every file write, both exit 0: "42 admission-origin occurrences derived" and "50 intended RED (46 preserved + 4 D13)". A positive control confirmed the sandbox refuses writes. These are presence and recomputation checks; MAESTRO judged no frozen choice.
3. Successor codexr2u2 wrote r2u_report.md from the accepted bytes and rebuilt nothing. MAESTRO rechecked the five subject hashes afterwards; this packet's generator asserts they are unchanged.
4. Builder construction choices MAESTRO did not rule on (r2u_handoff.md):
   - K7 drops the hand-written ADMISSION_NAMES. It reruns 13 recorded source queries and derives occurrences from recorded root selectors, process sites, supported stages and per-profile recipe sets. Unreviewed admission stages and applications refuse.
   - Gate-bearing profiles 23, 26, 29, 32, 35 and 38 each gain one admission-origin verify-preflight occurrence and one p2-eval Git occurrence, for 42 admission-origin occurrences in all.
   - In profile 38, the evaluator's fingerprint occurrence keeps SCIENCE/A1, while the gate's fingerprint stays ADMISSION/C:115.
   - The verifier's P3-only Git branch is treated as conditional, and absent for the current P2 admissions.
   - Origin and trace-site fields became required in the exact child schema. Construction profile, context and binding hashes and broker argv identities were rebased, and production broker argv hash references were added.
   - The existing R8R4 mutation fixture's children were given the required origin fields, so that control still reaches its original 65-input error.
   - All-profile aggregate maxima are 54 inputs / 5,477 bytes, alongside TOP_LEVEL 36 / 4,271.
   - The census used an isolated TMPDIR.

Review for:
1. Does V9 R1 close? Answer closed, partly closed (what remains) or open, with evidence. Do V8 R2/R3 and the earlier R4–R6 stay closed after the profile and schema changes?
2. D13 item 1: is every process reachable from an admission root represented as an ADMISSION_HELPER occurrence without A1 authority? That covers processes reached directly, through imported functions (including T.require_training_preflight and R.phase_trains), as descendants of an admission child (including verify-preflight's own process starts), and on the re-attempt path. Are science-origin uses of the same recipes kept as separate records with A1, never merged? Is the profile-38 fingerprint split right?
3. D13 items 2–3: is the recorded query set adequate for each admission source? Are its hit lists and reached sites correct? Does K7 derive the admission-origin set rather than hand-list it, and does F8 avoid claiming a complete call graph? Is the conditional P3-only Git branch treatment sound?
4. Are the four new controls (R10A–R10D) isolated and RED for their own reasons? Does the R8R4 fixture change preserve that control's original intent?
5. Does any frozen choice contradict or weaken a C clause beyond A1, add a default-to-proceed, put a science wait on the Intel Mac or terminate Intel work? Are composition refusal (D10), the Gate 1/2/3 boundaries, the separate commissioning authorization and the UNRUN status of all 18 parent cases plus 10 subcases preserved?

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; a table closing V9 R1; "What I checked and did not check".
