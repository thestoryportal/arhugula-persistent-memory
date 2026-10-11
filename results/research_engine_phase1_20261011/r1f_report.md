# R1F — local fixture repair; host qualification open
Aliases: RE = results/research_engine_phase1_20261011; C = RE/r1f_collector.py; P = RE/r1f_identity_probe.py; B = RE/r1f_bind_manifest.py; S = RE/r1f_stub.py; M = RE/r1f_make_bundle.py; W = RE/r1f_host_commands.sh; T = RE/test_r1f_collector.py; J = RE/intel_provisioning_manifest_v6.json; V = RE/astra_r1p5_verdict.md.
R1 holds only while the git-committed anchor is intact; the initial `none` run trusts the absence of a registration, and later runs require its independently preserved terminal sequence/hash (C:279,469; T:1065). Intel identity stays open until the direct-runtime probe is captured and strict launcher/runtime equality passes; the prior r1e observation is not bound (C:175; B:25; V:90-95). acquisition stays disabled and results remain OBSERVATION-ONLY; native acceptance is unverified (C:195,1099; J:1622).

| Round-5 finding/change | Answer or open reason |
|---|---|
| F1 | C:279,469,513,1118; T:1065,1111,1136. Exact independent head, final re-verification, same-inode emptying and active receipt edit; host capture open. |
| F2 | C:117,145,1112; T:1180. Complete publication hash precedes clock/writes, source core remains a second layer, later evidence enters only the ledger. |
| F3 | S:18,31; B:10,25; T:974,1208. All members verify before first compile; probe functions supplied from the verified namespace; real stub subprocess tests. |
| F4 | B:10,45; W:24,30,46; C:279,738; T:1239,1258. No Intel export/control directory; stdout binding receipt; carried M3 bootstrap start/bytes. |
| F5 | C:175; P:20; T:1276. Strict equality retained and direct CLT launcher selected; actual Intel completeness and launcher compatibility open. |
| F6 | T:1057,1289 and coverage table below. Claims limited to local fixtures; host lifecycle, native commissioning and Astra acceptance open (V:97-116). |
| R1 | C:469,513,549,1118; T:1065,1111,1136. Independent anchor premise requires Astra acceptance; deletion/loss of trusted git state is outside this guarantee. |
| R2 | C:117,145,1112; T:1180. Capture SHA rejects initial evidence/timestamp edits and internally consistent manufactured publications. |
| R3 | S:18,31; B:25; T:974,1208. No sibling loader, cache substitution or source reread; binder is verified before execution. |
| R4 | B:45; W:24,30,46; C:279,738; T:1239,1258. Bind and inventory bootstrap accounted; J:1513 interpretation remains an Astra question. |
| R5 | C:175; T:1276; W:7-8. Intel direct-runtime observation and qualification remain open; /usr/bin/python3 is not admitted as a launcher alias. |

| Test → could it pass with a relevant defect remaining? | Scope / remaining defect |
|---|---|
| r1f_01 (T:1065) → Yes | Coordinated valid-prefix rollback and coherent start/window/chain rewrite refuse; compromised independent anchor remains outside scope. |
| r1f_02 (T:1111) → Yes | Active earlier-receipt edit and same-inode emptying refuse; concurrent mutation after the final scan remains outside a snapshot guarantee. |
| r1f_03 (T:1136) → Yes | Cuts every instrumented occurrence; no real power loss, short syscall or hardware durability proof. |
| r1f_04 (T:1180) → Yes | Non-core edits, remanufactured core/provenance and ledger bypass refuse; compromised capture authority is outside scope. |
| r1f_05 (T:1208) → Yes | Real isolated stub, one-byte bad member, marker positive control, planted source/cache and post-bundle disk replacement; no Intel runtime proof. |
| r1f_06 (T:1239) → Yes | Real fake bind leaves fake Intel tree byte-identical; actual ssh/wrapper publication not executed. |
| r1f_07 (T:1258) → Yes | Carried expired time_total_s and charged bootstrap bytes; supplied byte count still relies on trusted M3 accounting. |
| r1f_08 (T:1276) → Yes | Strict invoked/runtime realpath mismatch refuses; actual CLT relationship remains unverified on Intel. |
| r1f_09 (T:1289) → Yes | Required qualification wording and questions; presence alone cannot establish truth. |
| 27 carried names (T:221-1057) → Yes | Fake child runners and selected IO patches do not prove host, network, native or universal lifecycle acceptance. |
Replacements retaining names: r1e_05 checks all source hashes through the real stub, r1e_06 measures verified fake identity in-process, r1e_07 checks stdout-only repeat publication/source preservation plus existing-window refusal; retired disk-publisher/loader subjects no longer exist (T:974-1029; B:10-57). r1d_01 now exercises real ledger updates instead of a mocked constructor/path entrypoint; r1d_07 checks remote-command policy; r1e_09 checks R1F qualifications (T:484,705,1057). Fixture receipts allowance includes the newly charged capture; constructors consume capture bytes and frozen hashes rather than share mutable manifest objects (T:94,177).

| Collector persistence path / boundaries | Coverage |
|---|---|
| Initialization: registration/retained/receipts/download mkdir, parent/root directory fsync (C:371-390,442) | Covered after each instrumented occurrence by T:1136. |
| Journal: exclusive create, write, flush, file fsync, registration-directory fsync (C:549-566) | Covered by T:1136; existing append open performs no write and is not covered. |
| Exclusive receipts/window/checkpoints: create, write, flush, file fsync, parent-directory fsync (C:580-595) | Covered by T:1136. |
| Evidence ledger: empty create/flush/fsync, directory fsync, append open/write/flush/fsync, directory fsync and checkpoint (C:644-682) | Covered by T:1136. |
| Stream/summary: unbuffered create/write/file fsync, receipt-directory fsync and journal begin/commit (C:763-783) | Covered by T:1136; no userspace flush on unbuffered stream. |
| HALTED reserve: open/write/flush/file fsync, receipt-directory fsync, emergency journal begin/commit (C:684-712) | Covered by T:1136. |
| Rename | None in collector persistence paths (C:349-427,549-711,763-783). |
| Print/flush to stdout/stderr; syscall short/partial write and exceptions inside fsync | Not covered by boundary cuts; anchors print only after journal durability; no host power-loss claim (C:439,549; T:1136). |

Prospective MAESTRO sequence after Astra review and separate host clearance: bind and inventory must run back to back; bind starts the M3 UTC clock before opening output files, and the window charges capture+stderr+exit bytes (W:24-35; C:279,738; T:1258). Probe is observation only; no binding files or bundle are written on Intel (S:18-38; B:10-57; W:35). These commands are instructions, not executed host evidence (T:1239).
```bash
RE=results/research_engine_phase1_20261011
RUNTIME=/Library/Developer/CommandLineTools/usr/bin/python3
STAMP=$(/bin/date -u +%Y%m%dT%H%M%SZ)
PROBE=$RE/r1f_probe_$STAMP
BIND=$RE/r1f_bind_$STAMP
bash "$RE/r1f_host_commands.sh" probe "$PROBE"
bash "$RE/r1f_host_commands.sh" bind "$BIND" "$PROBE.json"
# Set HASH to the exact R1F-CAPTURE hash printed by bind, from the trusted M3.
: "${HASH:?exact bind capture hash required}"
BOOTSTRAP_BYTES=$("$RUNTIME" -I -B "$RE/r1f_make_bundle.py" inventory --capture "$BIND.json" --expected-capture-sha256 "$HASH" --bootstrap-bytes-only)
bash "$RE/r1f_host_commands.sh" inventory "$BIND.json" "$HASH" none "$BOOTSTRAP_BYTES"
# Immediately preserve the last R1F-ANCHOR core/seq/head and HASH with the capture receipts in MAESTRO's git record.
# MAESTRO alone commits: git add -- "$BIND.json" "$BIND.stderr" "$BIND.exit"; git commit -m "R1F capture-sha256=$HASH anchor=CORE:SEQ:HEAD"
# Subsequent inventory must take HASH and SEQ:HEAD from that trusted commit, never from the Intel registration.
bash "$RE/r1f_host_commands.sh" inventory "$BIND.json" "$HASH" "$COMMITTED_SEQ:$COMMITTED_HEAD" "$BOOTSTRAP_BYTES"
```
Final acceptance is pending; the latest 36-test GREEN and remaining checks are recorded in the handoff below. Test-first baseline: 36 tests, exit 1, failures=9/errors=58; new interface, fixed stub and direct-launcher assertions fail (T:177,974,1276).
Session context: start a new step only at >=60% context left; at <=45% or compaction, stop, append `## R1F HANDOFF` with done/remaining/exact paths/next single step/this rule, then reply `R1F HANDOFF`.

## R1F HANDOFF
Done: all nine authorized files exist under RE; tests were written first, followed by copied R1E subjects and repairs. Exact paths: RE/{r1f_collector.py,r1f_identity_probe.py,r1f_bind_manifest.py,r1f_stub.py,r1f_make_bundle.py,r1f_host_commands.sh,test_r1f_collector.py,intel_provisioning_manifest_v6.json,r1f_report.md} (T:28,177,974; C:279; B:10; S:7; M:14; W:1; J:1).
Saved receipts: initial RED ran 36 tests, failures=9/errors=58; tightened RED ran 9 tests, failures=2/errors=0 (active ledger deletion and invoked argv spelling). Latest GREEN: exit 0, 36 tests, failures=0/errors=0, `Ran 36 tests in 6.575s; OK` (T:1180,1255; receipt retained here).
Exact latest command: `/usr/bin/python3 -B -m unittest discover -s results/research_engine_phase1_20261011 -p 'test_r1f_collector.py'`.
Unchanged regression receipts: `/usr/bin/python3 -B -m unittest discover -s results/research_engine_phase1_20261011 -p 'test_r1e_collector.py'`: exit 0, 27 tests, failures=0/errors=0; same command with `test_r1d_collector.py`: 18 tests, failures=0/errors=0; with `test_r1c_collector.py`: 9 tests, failures=0/errors=0. These ran before the last R1F-only fixes; existing files were not edited.
Last edit saved: B preserves a verified invocation prefix and checks its realpath; M builds the remote command from that identical prefix; J unsupported wrapper commands are explicitly BLOCKED; C verifies registered receipts before evidence append and validates the registration namespace at final verification (B:35; M:22; C:461,647,1123; J:1007). Fresh read-only reviewer reported no concrete residual defect in those fixes; it ran no tests or host commands.
Remaining: refresh every report citation to the final line numbers; correct any stale report claim/table; finish exact current-source acceptance (R1F plus unchanged R1C/D/E, bash syntax, JSON/3.9 syntax, standalone M3 probe and no-file check); compare existing reviewed hashes below and confirm exactly nine additions. Earlier syntax/JSON checks passed before the final edits, so final-source checks remain pending. No Intel/ssh/network/tmux/opt-local run, commit, or bundle-on-disk occurred.
Next single step: refresh the report's file:line citations against the saved R1F sources, without expanding scope; then finish the pending acceptance gate in a fresh session.
Open risks: Intel identity and direct-launcher equality are unqualified; acquisition remains disabled; anchor protection depends on independently preserved trusted git state; full host/crash/racing-writer acceptance is absent (C:175,195; S:18; T:1136; J:1624). The bootstrap/anchor questions below still require Astra.
Context rule, binding for the successor and every team session: start a new step only at >=60% context left; at <=45% or any compaction, stop starting work, finish only the active edit, append a precise R1F handoff (done/remaining/exact paths/next single step/open risks), and reply R1F HANDOFF.
Reviewed-subject before SHA-256 pins (captured at session start; not yet compared after edits): {"results/research_engine_phase1_20261011/r1e_host_commands.sh":"40438dc9399a358668c18aa938b785256d2a4898a1519dcfc272e8202ba66418","results/research_engine_phase1_20261011/intel_provisioning_manifest_v5.json":"23ebba24bb9f95847bc94239585fa489c97e57c5788cc9a5f23d33b177341f67","results/research_engine_phase1_20261011/r1e_report.md":"df4b03d8255f360329a2fc03d3f867c1134b738c9b936909ec3a9bbea315518e","results/research_engine_phase1_20261011/intel_provisioning_manifest_v4.json":"a65be19b612a4678f705a52c1dcb2fde537e1189515e618e3621cc816cb08e14","results/research_engine_phase1_20261011/r1c_report.md":"ee5d7cd1ba4c0293c819cfff49130d03405a14fd086c7683f08610cd4a7dac00","results/research_engine_phase1_20261011/test_r1d_collector.py":"c7716683ba287675bcf17f71a43a2c7e9a34ba5f250adde23d4c20e0bbaff00e","results/research_engine_phase1_20261011/test_r1c_collector.py":"5f8c3b90d6815025142dc7d3206ea99ad6648573bc1bb89b0688b300caf7a917","results/research_engine_phase1_20261011/intel_provisioning_manifest_v3.json":"056835b1fbc352af5093939b18f905d0befeab49f73241e7dd9b1efde0db97ca","results/research_engine_phase1_20261011/r1e_bind_manifest.py":"03d53b66ad5069497e51a95b9c2ec03b761ba8c837cedfcab7dd3d35be660d12","results/research_engine_phase1_20261011/r1e_identity_probe.py":"3172ef39ba74105b854735ad12113bde9df8d13c6332fe857885ce939dcad5cb","results/research_engine_phase1_20261011/r1d_report.md":"ede45916cb71ae905ca69b3863dc0540f552a0616bb61a466f49736a4e91bb49","results/research_engine_phase1_20261011/r1e_collector.py":"3471a2f379450f0c41195a60ff3bfdcc117d282617ec555b93a7777480eb9cc2","results/research_engine_phase1_20261011/r1d_host_commands.sh":"f7529dfc6e82f68e801e90df327921a340965df6291af3a0a1f25d8ab21e2900","results/research_engine_phase1_20261011/test_r1e_collector.py":"fd776835f6d5d39ca1f5ff49445a8d905f05d0f186f41729006b331236de43c1","results/research_engine_phase1_20261011/r1c_collector.py":"c3b9e215b8a0375d3d6af3c24fb195a7259269234f20b1cab96656ca326b714c","results/research_engine_phase1_20261011/r1d_collector.py":"6b592281f7d4bf7ee5d0304eeb9bc3055d52b709b0cbde2fbf00fa62fa818d60","results/research_engine_phase1_20261011/r1d_identity_probe.py":"89e548d40a3950accc0f9f09c28b0abb6590dc1dfa7e8b53e944d30280938881","results/research_engine_phase1_20261011/r1c_host_commands.sh":"83bde481db29d782d03db3adff1ed3d645bc5cd8afd0e029733ca3067b3ffe2b"}
Questions for Astra: does the carried-forward bootstrap satisfy J:1513? Is a git-committed anchor an acceptable independent authority?
