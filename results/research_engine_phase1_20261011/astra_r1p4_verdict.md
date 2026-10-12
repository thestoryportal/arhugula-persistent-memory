VERDICT: NO-GO

Aliases: `RE = results/research_engine_phase1_20261011`; `V = RE/astra_r1p3_verdict.md`; `C = RE/r1d_collector.py`; `T = RE/test_r1d_collector.py`; `P = RE/r1d_identity_probe.py`; `J = RE/intel_provisioning_manifest_v4.json`; `B = RE/r1d_report.md`.

F1. [high] **R1 remains partially open: the window survives ordinary invocations and evidence updates, but its persistence depends on the retained directory remaining intact.** Evidence: V:7–9,45 → C:267–298 creates a new clock whenever the named root is absent or empty. All previous-window state resides inside that root.

A concrete counterexample, inferred from the code: run inventory, close it, rename the retained directory, then invoke inventory with the **unchanged bound manifest**. C:273–298 recreates the original pathname and starts another clock; C:451–470 accounts only the newly created files. No changed core or recomputed seal is needed.

Similarly, ordinary historical receipts have no independently checked content inventory: C:451–468 counts their current sizes. Editing or truncating an earlier inventory/summary receipt can go undetected and reduce accounting. Evidence records have stronger protection through their checkpoint hashes, but those checkpoints also reside in the retained directory.

T:480–487 changes the manifest’s root without recomputing its seal; it does not exercise disappearance/replacement of the directory under an unchanged manifest. T:509–516 tests ledger corruption while retaining checkpoints.

**Consequence:** ordinary continuation is repaired, but “never restart” and preservation under retained-directory changes are not established. These tests can pass with the defects above.

F2. [medium] **R3’s identity mechanism remains incomplete: the probe hashes an incomplete stdlib inventory without necessarily reporting incompleteness.** Evidence: V:19–21,49 → P:20–33 excludes symlink directories and symlink files, and calls `os.walk` without an error handler. Directory enumeration errors can therefore omit subtrees without failing the probe. An omitted symlink’s target or bytes can change without changing the digest.

C:125–137 compares the resulting identity exactly, but equality of incomplete inventories does not establish complete stdlib identity. T:633–644 explicitly expects the symlink to be omitted; it contains no unreadable-subtree or changed-link-target case.

The probe does read executable bytes, version, flags and host attributes at P:36–43. Invoked with `/usr/bin/python3 -I -B`, its source contains no file-writing operation.

**Consequence:** the probe is suitable for read-only observation, but its current output is insufficient to close toolchain qualification. Intel identity is correctly still labelled `NEEDS-FETCH` at J:1589–1597.

F3. [medium] **Writing the bound manifest to a new filename is necessary, but insufficient to make the bind step sound.** Evidence: B:48–58 checks placeholder state, selected identity fields and root absence, then computes a digest of whatever manifest was supplied. It neither verifies the supplied manifest against the reviewed v4 SHA-256 nor verifies the collector/probe before importing them. Merely recording a supplied file’s hash would preserve provenance without establishing that it was the reviewed input.

Replacing `manifest_path.write_text(...)` with another `write_text(...)` also permits overwriting an existing bound file and provides no explicit file/directory durability check. The documented inventory and update commands still name unbound v4 at B:60–62 and J:1550,3056.

**Consequence:** the corrected binder needs reviewed-input verification, exclusive durable output creation, identity qualification before publication, and explicit commands using the bound file. A renamed destination alone does not supply these guarantees.

F4. [informational] **Round-3 R2 closes at implementation and behavioral-test level.** Evidence:

- V:11–13,47 → C:480–491,903–905,926 places the final deadline check after summary file and directory fsync, before successful output. T:546–564 advances the clock after that persistence and requires nonzero exit, empty stdout and a HALTED receipt.
- V:15–17,47 → C:434–440,528–556 carries active `argv` into the first cumulative-timeout receipt. T:566–613 exercises both `_execute()` deadline sites, with mocked process/selector boundaries.

**Consequence:** these tests would expose the two original defects. This is source/test assessment, not a reproduced test result or native child-enforcement qualification.

F5. [informational] **The current core list covers the collector’s limits, and the named policy-equality defects are repaired.** Evidence: V:33–37 → C:82–109 requires coverage of collector policy and relevant budget/identity fields; J:2152–2222 includes the clock, byte limits, roots, interpreter, child policy and seal lists. All **558 core paths and 339 evidence slots** resolve and have no core/evidence overlap.

C:130–135 checks executable/flags/minimum-version policy; C:252–258 checks component totals and receipt allowance equality. T:646–675 checks wrapper agreement and behavioral rejection of policy mismatches.

Structural comparison found the same ordered **48 artifact IDs**. Artifact changes are exclusively command-pointer updates. Budget, host, selection, tree and commissioning objects are unchanged. Remaining changes concern version/task scope, collector-root references, interpreter identity and the seal/evidence mechanism.

**Consequence:** round-3 F5’s specific duplicate-policy defects close. I found no new operative fallback or competing limit authority. This does not repair F1’s loss-of-state problem.

F6. [informational] **Observation and acquisition status are generally candid; several coverage claims need narrower wording.** Evidence: C:813–819 retains `OBSERVATION-ONLY`; J:1620 keeps acquisition unreviewed; C:140–148,824 enforces that gate. B:3,10,15,72 correctly leaves Intel/native qualification open.

The claim that interrupted appends always refuse is broader than C:345–380 establishes: an interruption after creating an empty ledger but before writing any record leaves zero records and zero checkpoints, which is accepted. It preserves the clock, but is not detected as an interrupted append. Likewise, B:7,13 should not imply protection against the retained-directory scenarios in F1.

**Consequence:** retain the open labels and distinguish tested corruption cases from universal lifecycle guarantees. Frozen `child_contract.reviewed=false` cannot be promoted through this evidence ledger; collecting its receipts does not authorize acquisition.

The nine new tests have these practical limits:

| Test | Could it pass while a relevant defect remains? |
|---|---|
| `r1d_01`, T:414–487 | Yes: checks ordinary continuation and stale-seal mutations, not directory replacement or resealed alternate roots. |
| `r1d_02`, T:490–522 | Yes: detects the tested ledger corruptions, not ordinary receipt modification, lost root, or empty interrupted append. |
| `r1d_03`, T:524–544 | Yes: identity comparison is exercised against a mocked identity; incomplete real measurement can pass. |
| `r1d_04`, T:546–564 | Not with the original final-persistence deadline defect. |
| `r1d_05`, T:566–613 | Not with the original missing-`argv` defect at either tested deadline site. |
| `r1d_06`, T:615–644 | Yes: explicitly permits symlink omission; its no-write observation covers the temporary cwd. |
| `r1d_07`, T:646–675 | Meaningful coverage of the named equality defects; literal absence alone is not policy completeness. |
| `r1d_08`, T:677–722 | Yes: tests actual dispatch/summary partitions, but stubs identity-producing helpers and bypasses constructor qualification. |
| `r1d_09`, T:724–748 | Meaningfully checks pre-write refusal of the specified acquisition paths; does not qualify a future reviewed child. |

Required changes:

R1. **Make missing/replaced retained state fail closed.** Use a durable, independently located window-registration record binding the approved manifest/core to its original clock and retained state. Resume must reject missing/replaced state rather than silently initialize. Validate prior receipt identities/accounting, and add cases for root relocation, receipt truncation and interrupted append boundaries. The registration must itself follow the existing clock/write-budget rules.

R2. **Complete the identity inventory.** Fail on traversal errors; bind symlink identities and relevant target contents, or reject layouts whose executable stdlib closure is not covered. Test unreadable subtrees and changed symlink targets. Keep Intel qualification open until the corrected probe is captured and matched.

R3. **Replace the bind recipe with a reviewed, no-clobber publication sequence.** Verify the exact supplied v4 and implementation hashes before importing code; preserve the original manifest; validate the complete identity against the running Intel interpreter; record source/probe provenance; exclusively create and fsync the bound file and its parent; record its resulting hash. Inventory and subsequent evidence updates must explicitly use that bound file. Do not recompute seals or substitute roots to recover a failed window.

R4. **Narrow the report’s lifecycle claims.** Record R1 and identity completeness as open; retain R2 as repaired and acquisition/native acceptance as unverified.

PROBE ALLOWED: yes — run r1d_identity_probe.py on the Intel Mac (writes nothing), using `/usr/bin/python3 -I -B`; its current output is observation, not completed toolchain qualification.

INVENTORY ALLOWED AFTER BINDING: no — run r1d_host_commands.sh inventory against the bound manifest on the Intel Mac only after the lifecycle, identity and binding corrections above are reviewed.

What I checked and did not check:

- Read the six subjects and round-3 verdict; all seven supplied hashes matched before and after review. Parsed JSON/Python source and compared v3/v4 structure. The builder commit adds exactly the six named files.
- Did not run tests, the probe, collector/wrapper execution, fetches, or native operations. MAESTRO’s 18/18, 9/9, shell-syntax and probe results remain **reported, not reproduced**.
- HEAD advanced from `338a4fc4` to `28f8fc20` during review. Intervening changes concern program state and dashboard records; subject hashes remained unchanged.
- No files were written and no graft command/tool was run. Amendment 22 and the excluded workstreams were not reviewed.