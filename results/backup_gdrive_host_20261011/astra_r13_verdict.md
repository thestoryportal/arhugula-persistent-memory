**K13 closes r12 item 1 under the repository’s existing cooperative merge protocol. MAESTRO may create the backup-only candidate and proceed through plan v4, subject to the conditions below.**

References: **K13** = `results/backup_gdrive_host_20261011/r13_package_20261011T032105Z`; **P** = `K13/activation_plan_v4.md`.

1. **r12 finding — CLOSED, subject to the binding-window condition.** Verification now compares the complete index or candidate commit’s path/blob/type/mode entries against `origin/master` overlaid with the allowlisted source entries. Pins are checked against Git blobs; commit verification requires exactly one parent, equal to the base, and writes an exclusive verified-SHA receipt. Restoring working-tree bytes cannot conceal contaminated index or commit objects from these comparisons. (`K13/candidate.py:63–124,133–175`.)

2. **Binding window — adequate under the established cooperative premise; not independently race-proof.** The plan requires fresh PR and remote-head observations inside the reserved window, equality with the verified SHA, immediate gate invocation, and comparison with the gate’s reported head afterward. (`P:126–153`; `K13/gate_binding.py:9–27`.)

   There is a real interval between those observations and the gate’s first head capture. A change during that interval could become the gate’s accepted head; the later comparison would detect it only after merging. Once captured, the gate repeatedly checks stability and supplies that captured SHA to its merge operation. (`tools/git_merge_gate.py:166–172,198–203,220–245`.)

   **I do not require a gate modification if MAESTRO actually establishes and maintains the prescribed reservation, suspension and drain.** That is already the repository’s explicit operational premise—not a guarantee supplied by the local lock. Merely asserting that the reservation exists is insufficient. If participation cannot be established, STOP; a stronger alternative must compare the verified SHA with the **same applying invocation’s** captured head before its merge side effect. A separate dry run or post-merge comparison does not close that interval. (`CLAUDE.md:52–54`; `P:72,119,126–153`.)

3. **Contamination coverage — the requested cases are covered; no blocking named variant remains.**

   The controls explicitly exercise staged and committed contamination, both out-of-scope and allowlisted, concealed by restored working-tree bytes; wrong executable modes; wrong and multiple parents; different PR and remote heads; and a committed deletion of a base path. The final candidate log records all 20 controls passing. (`K13/test_r13.py:72–134,162–177`; `K13/r13_release_final_green/CandidateTest.log:1–25`.)

   Gitlinks, renames and case-only differences lack dedicated empirical controls. Nevertheless, the implementation covers them structurally: gitlinks retain their `160000/commit` identity; allowlisted source gitlinks are rejected; deletions and renames change the complete key set; path comparisons preserve exact case. APFS working-tree aliasing does not make unequal index/commit keys equal. This is **code-derived coverage**, not a claim that those filesystem variants were run. (`K13/candidate.py:63–102,133–157`.)

   The RED evidence also needs precise labeling: contamination controls expose K12’s false acceptance, while missing binding APIs produce different RED failures. The contract explicitly distinguishes them. (`K13/r13_sandbox_red/CandidateTest.log:70–88`; `K13/TEST_CONTRACT_R13.md:3–10`.)

4. **Scope growth — accept the frozen evidence-bearing backup PR.** The scope contains nine production/test inputs plus backup-specific evidence, with 1,187 paths totaling **8,222,920 bytes**. The freezer explicitly retains K12’s scope and adds K13 evidence while excluding operational receipts. This is reasonable audit scope; reducing it now to production files and a summary receipt would require rebuilding the pin/reference closure. No scope reduction is required for this release. (`K13/selected_committed_paths.txt:1–36`; `K13/freeze_receipt.py:11–37`; `K13/operational_checks/commands/r13_host_freeze/stdout.txt:1`.)

**Previously accepted findings remain accepted.** My read-only checks verified all 1,185 current pins, all 522 K12 copy pairs, all 561 protected entries, the v3/v4 line mapping, and the pinned committed blobs in source commit `bdc1ad167afeedb94ccd60137b591eb78044c899`. The accepted verifier and fixture helpers remain byte-identical; the plan changes preserve the later activation gates. The current plan checker also returned `PASS []`. (`K13/pins_v4.sha256:1–1185`; `K13/k12_copy_manifest.json:1`; `K13/protected_r13_after.json:3370–3371`; `K13/erratum_v4.md:3–25`; `K13/commands/r13_host_plan_check/stdout.txt:1`.)

The prompt’s test-directory references need correction: the original RED receipt contains **41 tests/39 failures**, with the separate round-trip RED adding **1/1**. `r13_sandbox_final_green/` contains **68/68**; the final **69/69** receipt is `r13_release_final_green/`. The host package independently records **69/69**, with zero failures, errors or skips. These are saved execution receipts; this review did not rerun the mutating fixture suites. (`K13/r13_sandbox_red/result.json:74–80`; `K13/commands/r13_clean_pipeline_red/stderr.txt:1–14`; `K13/r13_sandbox_final_green/result.json:59–65`; `K13/r13_release_final_green/result.json:59–65`; `K13/commands/r13_host_package_driver/stdout.txt:1–7`.)

The conditions are:

1. **Candidate identity:** preserve the reviewed package, capture the fetched base/source identities, and obtain successful staged and exact-commit verification before publication. Any changed candidate requires fresh verification and receipts. (`P:31–48,74–105`; prior freshness ruling: `results/backup_gdrive_host_20261011/astra_r12_verdict.md:31`.)
2. **Merge binding:** record actual writer suspension/drain and reservation participation; maintain the window through the gate and its immediate head comparison. Require verified SHA = PR head = remote head = gate head. Any mismatch means STOP and preservation, including the merged SHA if applicable. (`CLAUDE.md:54`; `P:126–153`.)
3. **Activation remains separately gated:** retain every operator approval, including the write pause and full content verification/read-back budget; require the later completion and successor evidence before retirement. This review grants no activation or retirement approval. (`P:7–9,325,383–397,452–477`.)

**VERDICT: GO-WITH-CONDITIONS (1–3).**

