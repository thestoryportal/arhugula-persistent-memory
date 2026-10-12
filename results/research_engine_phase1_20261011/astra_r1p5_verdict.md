VERDICT: NO-GO

Aliases: `RE = results/research_engine_phase1_20261011`; `V = RE/astra_r1p4_verdict.md`; `C = RE/r1e_collector.py`; `P = RE/r1e_identity_probe.py`; `B = RE/r1e_bind_manifest.py`; `T = RE/test_r1e_collector.py`; `J = RE/intel_provisioning_manifest_v5.json`; `W = RE/r1e_host_commands.sh`; `D = RE/r1e_report.md`.

Counterexamples below are source-derived, not executed reproductions.

F1. [high] **R1 repairs retained-state damage with an intact registration, but does not establish the requested protection against registration tampering.** Evidence: V:5–13,66 → C:323–329,407–474,651–662; T:800–888.

The new code rejects missing/replaced roots and altered, missing or added receipts during resume. Registered sizes prevent receipt truncation alone from reducing accounting.

However, the registration’s chain has no independently trusted terminal digest or sequence number. A concrete counterexample:

1. Preserve registration bytes immediately after successful initialization.
2. Collect additional receipts.
3. Restore that valid registration prefix and remove the corresponding later receipts.
4. Resume with the unchanged manifest and original retained directory.

C:407–446 accepts the valid prefix; C:448–472 finds exactly its registered files; C:651–662 counts fewer bytes. The registration still exists. Similarly, rewriting the start record, matching `window.json`, its registered hash and subsequent chain links can change the clock without changing the core. Public hashes provide consistency, not an independent authority against coordinated rewriting.

Moreover, integrity verification occurs at construction, not before final success: an earlier receipt changed after construction can survive the current invocation without refusal, although a later resume detects it (C:329,1103–1105).

**Consequence:** round-4 R1 remains open. “No guarantee after registration loss” is an acceptable explicit limitation only with an accepted independent-state preservation premise. It does not describe the surviving-but-rewritten registration counterexample. D:4’s stronger “survives intact” qualification acknowledges a narrower guarantee than the packet asks to establish.

F2. [high] **R3 rejects changed cores but does not authenticate the complete binder publication or its initial evidence.** Evidence: V:23–27,70 → C:121–149,333–337,360–366; J:2716–2735; T:1004–1032.

Before the first window, change an evidence slot in an otherwise valid bound manifest—for example `/authorization/technical_review` or `/host/pool_map`. It remains outside the core digest. `verify_binding()` reconstructs and compares only the core; initialization adopts the supplied evidence as `evidence_initial`. No chained evidence update is required for that alteration.

Changing `binding_provenance.utc_time` to another syntactically valid timestamp also passes. All provenance fields are ordinary, reproducible data; the collector does not check an independently supplied digest of the complete published bound file. Thus a manifest with internally consistent manufactured provenance is not distinguishable from a binder-produced publication.

**Consequence:** missing provenance, stale hashes and the tested core reseals refuse, but “only bound” and “edited manifests refuse” are too broad. R3 remains open even with an untouched registration.

F3. [medium] **The binder verifies three source files before importing the collector, but does not guarantee execution of the verified probe bytes.** Evidence: V:70 → B:25–47; C:20–24; T:942–995.

B executes the verified collector byte buffer, which is good. That collector then uses `exec_module()` to load the sibling probe from disk. The binder’s second source-byte check does not eliminate replacement between check and load, or execution of accepted cached bytecode.

This is supported by the locally inspected Python 3.9 loader: `_bootstrap_external.py:939–980` reads and executes accepted cached bytecode; `dont_write_bytecode` controls cache **writing** at line 985. `-B` therefore does not close this gap.

The proposed sequence also records the binder’s own hash rather than checking its reviewed hash before executing it (B:63; D:53–54,68).

**Consequence:** verify executable inputs before their first execution and execute the already-verified probe bytes. The tests mock `_load_verified()` on the successful binding paths, so they cannot establish this property.

F4. [high] **The proposed export/capture/bind sequence conflicts with the frozen accounting contract and contaminates the intended install baseline.** Evidence: D:49–68; J:104–121,1461–1464,1513–1514,1601–1612; C:333–343,651–662,765–782,980–995.

**(a)** Exporting repository files into `/Users/robertrhu_node2/research-engine-phase1/` introduces new control files into an install root before its baseline. Inventory labels those files `baseline`; the later install comparison requires a rule for every actual entry and will reject unlisted export files.

Use a separately frozen Intel control/export directory outside all install, retained and registration roots. Merely executing read-only source there does **not** require membership in `admitted_write_roots`. Its creation and any outputs still require explicit scope and accounting. If the collector is to inventory that directory, adding it to the frozen admitted-root list requires a reviewed revision; do not silently reseal v5.

**(b)** The Intel stdout capture and bound file cannot silently be exempted. J:1513 starts the clock before the first provisioning-related writer, including verification writes; J:1464 includes all inventories, stdout/stderr and evidence. Yet C starts its clock later and counts only registration/registered retained files. Export creation, the probe capture and bound publication escape that mechanism.

The packet’s “binder before any window” decision therefore needs explicit reconciliation with the frozen clock rule: either a reviewed bootstrap phase whose original start and bytes carry forward, or an expressly approved contract amendment. Moving files outside install roots does not itself exempt their cost.

**(c)** The printed SHA-256 comparison establishes **copy integrity**, assuming a trusted capture of the successful Intel binder output. It is not sufficient provenance or inventory admission by itself. Preserve the binder command, host attribution, exit status, reviewed input hashes, raw probe and output digest; verify complete publication identity at consumption. F2 currently prevents the collector from enforcing that last property.

**Consequence:** neither binding nor inventory should proceed using D:49–68 as written.

F5. [medium] **The named stdlib omissions are repaired in source, but Intel completeness and launcher compatibility remain unverified.** Evidence: V:15–21,68 → P:20–51; T:890–925; `RE/intel_identity_probe_20261011T113404Z.json:1`; C:154–170; J:1580.

The corrected walker raises traversal errors, binds symlink text and file-target contents, inventories internal directory targets through their real paths, and refuses dangling or escaping directory links. These address round-4 F2’s specific omissions. The old 1,635-entry observation neither enumerates omitted links nor proves that the corrected probe accepts the actual CLT tree.

There is also an unresolved launcher assumption: the observation reports the CLT executable and framework realpath, while J names `/usr/bin/python3`; C:164 requires the latter’s filesystem realpath to equal the reported runtime realpath. Launcher redirection is not necessarily symlink resolution. The observation does not supply that required equality. The local M3 `/usr/bin/python3` is a regular executable, but that is not Intel verification.

**Consequence:** retain Intel identity qualification as open. Establish the launcher/runtime relationship explicitly; do not weaken equality or claim a successful probe alone qualifies the collector.

F6. [informational] **The report preserves important open statuses, but its tests do not support universal lifecycle or binding claims.** Evidence: V:44–48,72 → D:3–17,69–72; C:174–182,1014–1020; T:1034–1045.

Acquisition remains disabled and results remain `OBSERVATION-ONLY`. The earlier final-persistence deadline and causal-`argv` repairs remain present (V:29–34 → C:634–641,727–755,1103–1105; T:572–639). These are source/test assessments, not reproduced host acceptance.

The nine new tests have these limits:

| Test | Could it pass with a relevant defect remaining? |
|---|---|
| `r1e_01`, T:800–823 | Yes. Covers resume with untouched registration; “empty” recreates the root rather than emptying the original inode. No active-invocation mutation coverage. |
| `r1e_02`, T:825–844 | Yes. Meaningfully checks receipt-only damage and cached accounting; leaves coordinated registration rollback uncovered. |
| `r1e_03`, T:846–888 | Yes. Exercises selected post-directory-fsync cuts, not every write/flush/fsync boundary or valid-prefix rollback. |
| `r1e_04`, T:890–925 | It exposes the original link-target and missing-error-handler defects. It can still pass without actual Intel layout qualification. |
| `r1e_05`, T:942–952 | Exposes failure to reject each supplied bad hash before `_load_verified`; does not test cached-bytecode execution or binder preflight. |
| `r1e_06`, T:954–973 | Yes. Loader and measured identity are mocked; native measurement/import correctness remains untested. |
| `r1e_07`, T:975–1002 | Checks ordinary no-clobber behavior, source preservation and fsync calls. Does not exercise a racing publisher, crash publication or fsync failure. Source does use `O_EXCL`. |
| `r1e_08`, T:1004–1032 | Yes. Tests core/provenance mutations, but misses changed initial evidence, timestamp edits and manufactured consistent provenance. |
| `r1e_09`, T:1034–1045 | Yes. Checks wording and table presence, not truth or citation support. |

**Consequence:** round-4 R4 is substantially addressed in wording, but D:10,16’s binding claims and the host sequence need correction. Round-4 R1 and R3 remain implementation-open; R2’s named walker defects are repaired, with Intel qualification open.

Required changes:

R1. Establish an independently trusted registration state against rollback/rewrite, or obtain explicit acceptance of a narrower trusted-registration threat model. Add coordinated journal/receipt rollback, same-inode emptying and active-invocation mutation cases. State exactly which interrupted-write boundaries are covered.

R2. Bind the complete initial manifest publication to an independently trusted digest/receipt. Refuse initial evidence edits; subsequent evidence must enter through the ledger. Test manufactured provenance and non-core edits.

R3. Execute verified probe bytes without cache substitution or rereading races. Verify the reviewed binder/probe before first execution. Exercise the real import path in tests.

R4. Replace the host sequence with a frozen separate control/export location and explicit bootstrap write/time accounting consistent with J:1513. Specify the provenance retained across copy-back.

R5. Capture the corrected Intel probe as observation, resolve the launcher/runtime identity relationship, and revise the report’s closure claims and test-coverage descriptions accordingly.

PROBE ALLOWED: yes run r1e_identity_probe.py on the Intel Mac — observation only, using `/usr/bin/python3 -I -B` and the prior stdin-streaming approach without Intel file writes; verify the supplied probe bytes first.

BIND ALLOWED: no run r1e_bind_manifest.py on the Intel Mac

INVENTORY ALLOWED AFTER BINDING: no

What I checked and did not check:

- Inspected the collector, probe, binder, wrapper, tests, report, relevant v5 policies, round-4 verdict and Intel observation.
- All eight supplied hashes matched before and after review. HEAD remained `2c8e9b03`; the implementation commit adds exactly the seven named files.
- Did not execute tests, probe, binder, collector, wrapper, fetches or Intel commands. MAESTRO’s test, syntax and probe results remain **reported, not reproduced**.
- Wrote no files; ran no graft commands/tools. Excluded workstreams were not reviewed.