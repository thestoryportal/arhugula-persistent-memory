# R2U / R2U2 report — static delivery
B = results/compute_storage_brainstorm_20261011T054507Z; paths below are relative to B. R2U built the five subjects; R2U2 wrote only this report, resumed without rebuilding or rerunning acceptance. MAESTRO verified committed subject bytes at 68bbe401.
Five subject SHA256 values, freshly recomputed with `shasum -a 256`; all match r2u_handoff.md:
```text
61c21fada5da7de5aa8f60b1c36e7d1bc544f8ef7a1e7cc47f3f0d7007d607e9  shared_disk_clearance_freeze_v8.md
22c05403e421615ce13a46e1461270e0a82226556b397830d9cbfb248ffb6424  shared_disk_clearance_schemas_v7.json
09e7c86c2077d9944cde70cee3a7e85c63b59002330d8438ba38a3d55a3c9600  check_r2_schemas_v7.py
94992853eb83d36673254611c6b88204981d7c90a5ad04dfb8c4aaf6c0588c0f  science_launch_profiles_v5.json
a11f5c9a65e0a9151101983002b133386f1f75b4f0c9d1fa3aa77237045103d9  science_launch_inventory_v7.md
```
R1 implementation: recorded admission-origin traces replace the fixed ADMISSION_NAMES mechanism; six gate-bearing profiles [23,26,29,32,35,38] add six verify-preflight and six Git occurrences. All 42 derived admission occurrences require ADMISSION_HELPER / C:115 / PRE_RELEASE_REQUIRED without A1; shared science-origin recipes retain separate SCIENCE_CHILD/A1 records.
R1 closing lines: F8 shared_disk_clearance_freeze_v8.md:336,339,359–360 records imported verifier/Git paths, verifier descendants, conditional P3 replication and re-attempt paths, plus exact queries/hit lists; K7 check_r2_schemas_v7.py:2336–2341 reruns grep, :2355–2382 derives/validates origins and preserves science authority, :2385–2417 compares hits/source pins/trace records and enforces composition refusal, :2439–2460 adds the four targeted controls.
Composition refusal remains NOT_ADMITTED_ADMISSION_HELPER_UNREGISTERED:. Earlier closures remain mapped at F8:340–344: retained callers/direct P1/P3 restrictions, delegation references, bounded aggregate receipts and refusal variants.
Lexical limit: RECORDED_QUERIES_ONLY_NOT_COMPLETE_CALL_GRAPH; 13 recorded queries and reviewed edges, not a complete call graph. Proof is static only. C:115 helper registration/pre-release mechanism is unestablished; native containment/commissioning and all 18 parent + 10 subcases remain UNRUN; Gate 1 OPEN pending Astra round 10.
Test-first receipt: [r2u_test_first_red.log](r2u_test_first_red.log); K7 against F7/J6/P4, each branch separately exited 1 before building F8/J7/P5, with its own defect:
```text
FAIL: R10 verify-preflight admission-origin misclassified SCIENCE_CHILD/DECLARED_AT_ROOT_ADMISSION/D-R2C-A1
FAIL: R10 git-ls-files admission-origin misclassified SCIENCE_CHILD/DECLARED_AT_ROOT_ADMISSION/D-R2C-A1
```
Acceptance 1 — `/usr/bin/python3 -B B/check_r2_schemas_v7.py`, exit 0; saved [r2u_acceptance_default.log](r2u_acceptance_default.log):
```text
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D13 trace: 13 recorded queries, 0 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN: 114 schemas, 17 request kinds, 259 examples validated, 1411 hash references recomputed, 8 bindings rerendered, 16 observations checked
```
Acceptance 2 — `/usr/bin/python3 -B B/check_r2_schemas_v7.py --profiles B/science_launch_profiles_v5.json`, exit 0; saved [r2u_acceptance_profiles.log](r2u_acceptance_profiles.log):
```text
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D13 trace: 13 recorded queries, 0 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN admission aggregates: 25 TOP_LEVEL, 55 total; max TOP_LEVEL 36 input receipts, 4271 UTF-8 bytes; frozen bounds 64 / 8192 blob / 262144 file
GREEN all aggregate maxima: 54 input receipts / 5477 UTF-8 bytes; frozen bounds 64 / 8192 / 262144
GREEN round 8: R1-R6; A1 descendant exception only; guard/broker, chain admission, aggregate receipts, source-valid refusals, one launch context; Gate 2 UNVERIFIED
GREEN round 9: R1 admission helper refusal, R2 caller audit, R3 same-launch delegation references and process identities
GREEN D13 trace: 13 recorded queries, 42 admission-origin occurrences derived; recorded queries only, no complete call graph or native proof
GREEN production coherence: R1-R4, D1 refusals, 737 binding vectors rerendered; native behavior UNVERIFIED
GREEN profiles: 55 LaunchProfile entries, 0 not_admitted entries schema-validated, 174 not_admitted entries explicit refusals checked
```
Acceptance 3 — `/usr/bin/python3 -B B/check_r2_schemas_v7.py --mutation-controls`, exit 0. All 50 intended RED lines (46 preserved + 4 D13) are in [r2u_acceptance_mutations.log](r2u_acceptance_mutations.log); four R10 lines and final GREEN verbatim:
```text
RED R10A: exit 1: R10 verify-preflight admission-origin carries A1/science authority: /children/15
RED R10B: exit 1: R10 git-ls-files admission-origin carries A1/science authority: /children/43
RED R10C: exit 1: R10 recomputed trace hit-set mismatch: starts-train
RED R10D: exit 1: R10 verify-preflight admission-origin occurrence missing/merged: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10w_p2_stage.sh
GREEN mutation controls: 50 intended RED (46 preserved + 4 D13), zero filesystem writes
```
Before/after census: B files 193→193 and entries 193→193; task TMPDIR files/entries 1→1; created=[] and removed=[] in both roots. Logs/census outputs pre-existed before measurement. Receipts: [r2u_census_before.json](r2u_census_before.json), [r2u_census_after.json](r2u_census_after.json), [r2u_census_summary.json](r2u_census_summary.json).
TMPDIR measured: /var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/r2u_census_25cr3kvj (task-specific; ambient Apple-protected directory excluded; xcrun cache warmed before census). Census proves no created files/directories during the measured run.
MAESTRO corroboration: [r2u_maestro_acceptance.md](r2u_maestro_acceptance.md):5–14 records matching hashes/unchanged inputs, acceptance 1 exit 0, and acceptance 2/3 exit 0 under deny-write sandbox with a working positive control; no B file appeared. Static checks do not constitute a trace-design ruling or runtime acceptance.
Acceptance exit receipts: [r2u_acceptance_summary.json](r2u_acceptance_summary.json). Inputs and subjects were not edited by R2U2; no builder, acceptance rerun, commit or real launch was performed.
