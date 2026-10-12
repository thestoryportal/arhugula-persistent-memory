# R1F — local fixture repair; host qualification open
Aliases: RE = results/research_engine_phase1_20261011; C = RE/r1f_collector.py; B = RE/r1f_bind_manifest.py; S = RE/r1f_stub.py; M = RE/r1f_make_bundle.py; W = RE/r1f_host_commands.sh; T = RE/test_r1f_collector.py; J = RE/intel_provisioning_manifest_v6.json. Reviewed sources: commit 73b7ebeb.
R1 holds only while the git-committed anchor is intact; initial `none` trusts the absence of registration/retained state, and later runs require the independently preserved terminal sequence/hash (C:361-372,507-514; T:1068-1112). Intel identity stays open until the direct-runtime probe is captured and strict launcher/runtime equality passes (B:25-38; C:175-192). acquisition stays disabled and results remain OBSERVATION-ONLY (C:195-204,1110-1114). No host, crash, racing-writer or native commissioning acceptance is claimed.

| Round-5 finding/change | Answer or open reason |
|---|---|
| F1 | C:507-514,1122-1135,1220-1225; T:1068,1114,1139. Exact anchor comparison and final re-verification; rollback/rewrite, same-inode emptying and active receipt-edit fixtures. Trusted-anchor premise and host capture open. |
| F2 | C:117-133,145-170,279-297,1116-1120; T:1183. Complete capture hash checked before clock/writes; reviewed source core checked separately; evidence changes require the ledger. |
| F3 | S:18-37; B:25-38; T:984-1014,1223-1253. All members verified before first compile; verified probe namespace supplied to binder; real stub subprocess fixtures, including planted source/cache. |
| F4 | B:49-59; W:24-44,46-52; C:373-380,742-753; M:29-37. Binder emits stdout; capture stays on M3, no Intel export directory is created; start and receipt bytes carried forward. Open: consistency with J:1515 requires Astra. |
| F5 | C:175-192; W:7-8; T:1294-1305. Strict equality retained and direct CLT runtime selected. Open: actual Intel stdlib completeness and launcher compatibility. |
| F6 | T:1060-1066,1307-1311 and coverage table below. Wording tests do not establish truth; local fixtures do not qualify host lifecycle, native commissioning or Astra acceptance. |
| R1 | C:507-514,1122-1135; T:1068,1114,1139. Open: Astra must accept the independent git anchor premise; deletion/loss of trusted git state is outside this guarantee. Boundaries below. |
| R2 | C:117-133,145-170,1116-1120; T:1183-1221. Initial non-core/evidence/timestamp edits and coherent manufactured publication rejected against trusted capture SHA; active ledger deletion also rejected. |
| R3 | S:18-37; B:25-38; T:984-1014,1223-1253. Verified bytes compiled in fresh namespaces; no sibling import/cache substitution or probe source reread on this path. Intel execution open. |
| R4 | B:49-59; W:24-44,46-52; M:29-37; C:373-380,742-753. Receipt retains argv, hostname/uname, bootstrap start, input hashes, raw measured probe and bound-manifest hash. Open: carried-forward bootstrap interpretation of J:1515. |
| R5 | C:175-192; W:7-8; T:1294-1305. Open: direct-runtime Intel observation and qualification not captured; `/usr/bin/python3` is not admitted as a launcher alias. |

| Test | Could it pass with a relevant defect remaining? |
|---|---|
| `test_r1f_01_anchor_refuses_coordinated_rollback_and_rewrite`, T:1068-1112 | Yes. Rejects valid-prefix rollback and coherent start/window/chain rewrite; compromised independent anchor remains outside scope. |
| `test_r1f_02_final_verification_active_edit_and_same_inode_empty`, T:1114-1137 | Yes. Rejects active earlier-receipt edit and same-inode emptying; mutation after the final scan remains outside a snapshot guarantee. |
| `test_r1f_03_every_instrumented_write_boundary_refuses_restart`, T:1139-1181 | Yes. Cuts each instrumented occurrence in its initialization/evidence/stream/HALTED trace; no real power loss, short syscall or hardware durability proof. |
| `test_r1f_04_complete_publication_and_ledger_only_evidence`, T:1183-1221 | Yes. Rejects non-core edits, coherent resealing, ledger bypass and active ledger deletion; compromised capture authority remains outside scope. |
| `test_r1f_05_real_stub_verifies_before_compile_and_ignores_disk`, T:1223-1253 | Yes. Bad manifest blocks marker execution, positive control executes, planted source/cache and later disk replacement are ignored; no Intel runtime or concurrent-race proof. |
| `test_r1f_06_bind_stream_leaves_fake_intel_tree_identical`, T:1255-1274 | Yes. Real stub with fake identity leaves fixture tree unchanged and preserves receipt fields; actual ssh/wrapper publication is not executed. |
| `test_r1f_07_bootstrap_start_and_bytes_are_charged`, T:1276-1292 | Yes. Expired carried time refuses and capture bytes are charged; correctness of supplied byte accounting still relies on trusted M3 receipts. |
| `test_r1f_08_direct_runtime_and_strict_realpath`, T:1294-1305 | Yes. Launcher mismatch refuses and CLT selection is checked; actual Intel launcher/runtime relationship remains unverified. |
| `test_r1f_09_report_states_independent_anchor_qualifier`, T:1307-1311 | Yes. Required phrases only; neither truth nor citation support is established. |
| 27 carried test names; fake runner T:198-202; revised binder fixtures T:984-1028 | Yes. Fixture success does not establish host, network, native, crash or racing-writer acceptance. |
Carried r1e_05/06/07 now exercise the real stub with verified fake identity, source-hash refusal, measured-probe equality, repeat stdout publication and existing-window refusal; the fake identity is explicit (T:963-1028). Their historical names do not prove disk publication durability.

Boundary test alias `r1f_03` = `test_r1f_03_every_instrumented_write_boundary_refuses_restart` (T:1139-1181). Cuts occur after successful operations in that test's trace; this is fixture interruption coverage.

| Collector persistence path / boundaries | Coverage |
|---|---|
| Initialization: registration/retained/receipts/download mkdir and parent/root directory fsync (C:385-406,444-450) | Covered by `r1f_03`. |
| Journal: exclusive create, write, flush, file fsync, registration-directory fsync (C:552-569) | Covered by `r1f_03`; existing append-open has no separate cut and is not covered. |
| Exclusive receipts/window/checkpoints: create, write, flush, file fsync, parent-directory fsync (C:583-597) | Covered by `r1f_03`. |
| Evidence: empty create/flush/fsync, directory fsync, append open/write/flush/fsync, directory fsync and checkpoint (C:647-685) | Covered by `r1f_03` for its first append; a second append's distinct existing-ledger path is not covered by this trace. |
| Stream/summary persistence primitive: unbuffered create/write/file fsync, receipt-directory fsync, journal begin/commit (C:767-788) | Covered by `r1f_03` through `save('stream', ...)`; no userspace stream flush. |
| HALTED reserve: open/write/flush/file fsync, receipt-directory fsync, emergency journal begin/commit (C:688-714) | Covered by `r1f_03`. |
| Rename, stdout/stderr print/flush, short/partial syscall writes, failures inside fsync | Not covered by `r1f_03`; journal anchors print after file and directory fsync (C:552-569,441-448). |

Prospective MAESTRO sequence after Astra review and separate host clearance: probe with the direct runtime, then bind and inventory must run back to back, then commit the capture hash and last anchor. Bind starts M3 UTC before opening capture files; inventory charges capture+stderr+exit bytes (W:24-44; M:54-65; C:373-380,742-753). Binder stdout retains provenance; no copy-back or Intel binding file is used (B:49-59; W:30-34,46-52). Commands below are instructions, not executed host evidence; probe/bind use W:7-8's direct CLT runtime.

```bash
RE=results/research_engine_phase1_20261011
RUNTIME=/Library/Developer/CommandLineTools/usr/bin/python3
STAMP=$(/bin/date -u +%Y%m%dT%H%M%SZ)
PROBE=$RE/r1f_probe_$STAMP
BIND=$RE/r1f_bind_$STAMP
bash "$RE/r1f_host_commands.sh" probe "$PROBE"
bash "$RE/r1f_host_commands.sh" bind "$BIND" "$PROBE.json"
# Set HASH to the exact R1F-CAPTURE hash printed by bind on the trusted M3.
: "${HASH:?exact bind capture hash required}"
BOOTSTRAP_BYTES=$("$RUNTIME" -I -B "$RE/r1f_make_bundle.py" inventory --capture "$BIND.json" --expected-capture-sha256 "$HASH" --bootstrap-bytes-only)
bash "$RE/r1f_host_commands.sh" inventory "$BIND.json" "$HASH" none "$BOOTSTRAP_BYTES"
# Set CORE, SEQ and HEAD from the LAST R1F-ANCHOR printed by successful inventory.
: "${CORE:?last anchor core required}" "${SEQ:?last anchor sequence required}" "${HEAD:?last anchor head required}"
git add -- "$PROBE.json" "$PROBE.stderr" "$PROBE.exit" "$BIND.json" "$BIND.stderr" "$BIND.exit"
git commit -m "R1F capture-sha256=$HASH anchor=$CORE:$SEQ:$HEAD"
# Later: take HASH and COMMITTED_SEQ/COMMITTED_HEAD from that trusted commit, never the Intel registration.
bash "$RE/r1f_host_commands.sh" inventory "$BIND.json" "$HASH" "$COMMITTED_SEQ:$COMMITTED_HEAD" "$BOOTSTRAP_BYTES"
```
Questions for Astra: does the carried-forward bootstrap satisfy J:1515's first-writer clock requirement? Is a git-committed anchor an acceptable independent authority?

## Status

MAESTRO reran acceptance on committed sources (73b7ebeb): r1f 36 tests OK; unchanged r1e 27, r1d 18, r1c 9 tests OK; `bash -n RE/r1f_host_commands.sh` OK; v6 parses; all five r1f .py source files compile on `/usr/bin/python3` 3.9.6; the M3 probe prints parseable JSON and writes no file. R1F scope receipt: exactly nine new files, no previously tracked file edited. These are local receipts, not Intel qualification.
R1G edits only RE/r1f_report.md. Final verification command: `/usr/bin/python3 -B -m unittest discover -s results/research_engine_phase1_20261011 -p 'test_r1f_collector.py'`. Open: trusted git anchor premise, Intel direct-runtime identity, bootstrap interpretation, host/crash/racing-writer/native acceptance; acquisition disabled, OBSERVATION-ONLY.
Context rule for this session and every successor/team session: start a new step only at >=60% context left; at <=45%, any compaction or MAESTRO stop, finish only the current edit, save, append `## R1G HANDOFF` with done/remaining/next single step/this rule, then reply `R1G HANDOFF`.
