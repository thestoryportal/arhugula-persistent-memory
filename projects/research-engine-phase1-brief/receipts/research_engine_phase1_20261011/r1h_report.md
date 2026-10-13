# R1H — local fixture repair; Intel qualification open
Aliases: RE = results/research_engine_phase1_20261011; C = RE/r1h_collector.py; B = RE/r1h_bind_manifest.py; S = RE/r1h_stub.py; M = RE/r1h_make_bundle.py; W = RE/r1h_host_commands.sh; T = RE/test_r1h_collector.py; J = RE/intel_provisioning_manifest_v7.json; V = RE/astra_r1p6_verdict.md.
R1 holds only while the git-committed anchor is intact and unconsumed; git is the independent authority, and unknown outcomes require operator-reviewed recovery, never reuse (M:61-86,98-150,163-174; T:1353-1410). Initial `none` additionally trusts absence of Intel registration/retained state (C:363-377).
Intel identity stays open until the direct-runtime Intel probe is captured and binding's strict equality passes (B:25-38; C:177-194; V:79-81). acquisition stays disabled and results remain OBSERVATION-ONLY (C:197-206,1123; W:13-38).
The direct-runtime probe is a separate historical observation before the bootstrap start; its three capture files are not bootstrap bytes (J:1515). Provenance companions remain beside each capture; the exit-status file is outside the capture hash (M:34-40,169-227,234).

| Round-6 finding/change | Answer or open reason |
|---|---|
| F1 | M:61-71,134-168; T:1353. Exclusive M3 attempt record and file/directory fsync precede ssh; complete and partial-write lost-output rollback cannot reuse A. Open: trusted M3/git durability, real crash and racing writers. |
| F2 | M:147-150,179-193,206-227; C:721-745; T:1429. M3 supplies 870 minus elapsed minus 5 seconds; Intel uses process monotonic time. Hard M3 subprocess timeout and late-end failure. Host transport enforcement remains unqualified. |
| F3 | M:73-86,140-144,34-40; W:24-35; J:1515,3064; T:1499,1482. Committed capture bytes/hash before inventory, historical probe boundary, full update arguments, preserved companions. |
| F4 | C:119-172; S:17-40; T:987,997,1226. Complete verified-byte execution and trusted capture SHA checks retained; real stub subprocess probe/bind fixtures. Open: complete successful wrapper/ssh/stub inventory on Intel. |
| F5 | B:18-59; C:177-194; W:7-8,28,35; T:1258,1297,1509. Stdout binding, explicit SSH identity and direct CLT runtime; strict realpath equality retained. Open: Intel direct-runtime observation and qualification. |
| F6 | T:1063,1310,1518 and coverage table below. Qualification includes intact and unconsumed; fixture/wording checks do not establish universal closure. |
| R1 | M:61-71,134-168; T:1353. Source and fixtures repaired; open host durability and intact independent authority premise. |
| R2 | M:147-150,179-227; C:21,721-745; S:1-2,31; T:1429. Single M3 deadline, remote monotonic duration; open actual ssh termination/remote lifecycle. |
| R3 | M:73-86,140-144; J:1515,3064; W:24-35; T:1499,1482. Procedure and commitment gate repaired; publication needs MAESTRO's execution/preservation. |
| R4 | B:25-38; C:177-194; W:7-8,28,35; T:1551. Open: direct-runtime Intel probe/binding equality has not been executed by this task. |
| R5 | Legacy round-5 identity item remains open for the same reason as R4 (V:69-81; B:25-38). |

| Test | Could it pass with a relevant defect remaining? |
|---|---|
| `test_r1h_01_pending_attempt_blocks_lost_output_and_interrupted_append`, T:1353 | Yes: reproduces append, lost capture, restoration to A and refusal before mocked ssh, plus duplicate exclusive creation; not actual transport/power-loss or independent-authority compromise. |
| `test_r1h_02_single_m3_clock_and_monotonic_remote_budget`, T:1429 | Yes: offsets +/-300 seconds, actual bundled duration, remote pre-fetch/write expiry, expired dispatch and late M3 exit/final persistence; subprocess transport is fake, no host timing qualification. |
| `test_r1h_03_bind_capture_requires_committed_matching_bytes`, T:1499 | Yes: missing/different git blobs refuse before mocked ssh; git responses are fixtures, not proof of operational commitment. |
| `test_r1h_04_v7_commands_have_full_arguments_and_direct_runtime`, T:1515 | Yes: JSON, update syntax/arguments, margin and command/runtime text; no successful host sequence. |
| `test_r1h_05_every_wrapper_ssh_uses_explicit_identity`, T:1542 | Yes: grep-level argv checks; key availability/authentication and ssh behavior remain open. |
| `test_r1h_06_report_states_intact_and_unconsumed_boundary`, T:1551 | Yes: required wording only, not claim truth. |
| 36 carried names, T:221-1314 | Yes: fake roots/identity/children and instrumented interruption traces; real stub probe/bind at T:987-1029,1226-1277, but no real crash, short-write, fsync-failure, racing-writer or Intel acceptance. Carried clock fixtures now supply M3-derived budgets (T:176-185). |

Prospective MAESTRO sequence after Astra review and separate Intel clearance: bind and inventory must run back to back **with the capture/hash commit between them**, all bootstrap work inside 870 seconds (W:24-35; M:140-150,179-216). The carried-forward bootstrap charges bind capture, stderr and exit bytes; attempt/inventory receipts stay preserved independently on M3 (M:34-40,163-227; C:753-764). Commands below are instructions, not executed host evidence (W:2).
```bash
set -euo pipefail
RE=results/research_engine_phase1_20261011
RUNTIME=/Library/Developer/CommandLineTools/usr/bin/python3
STAMP=$(/bin/date -u +%Y%m%dT%H%M%SZ)
PROBE=$RE/r1h_probe_$STAMP
BIND=$RE/r1h_bind_$STAMP
bash "$RE/r1h_host_commands.sh" probe "$PROBE"
git add -- "$PROBE.json" "$PROBE.stderr" "$PROBE.exit"
git commit -m "R1H direct-runtime probe: historical observation before bootstrap"
bash "$RE/r1h_host_commands.sh" bind "$BIND" "$PROBE.json"
HASH=$("$RUNTIME" -I -B -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$BIND.json")
git add -- "$BIND.json" "$BIND.stderr" "$BIND.exit"
git commit -m "R1H bind capture-sha256=$HASH"
BOOTSTRAP_BYTES=$("$RUNTIME" -I -B "$RE/r1h_make_bundle.py" inventory --capture "$BIND.json" --expected-capture-sha256 "$HASH" --bootstrap-bytes-only)
CORE=$("$RUNTIME" -I -B -c 'import json,sys; print(json.loads(json.load(open(sys.argv[1]))["bound_manifest_json"])["window_seal"]["core_sha256"])' "$BIND.json")
INV=$RE/r1h_inventory_0_${CORE:0:12}
ATTEMPT=$RE/r1h_attempt_0_${CORE:0:12}.json
set +e
bash "$RE/r1h_host_commands.sh" inventory "$BIND.json" "$HASH" none "$BOOTSTRAP_BYTES"
RC=$?
set -e
git add -- "$ATTEMPT" "$INV.json" "$INV.stderr" "$INV.exit"
git commit -m "R1H initial attempt, capture and companions; exit=$RC"
[[ $RC == 0 ]] || exit "$RC"
ANCHOR=$("$RUNTIME" -I -B -c 'import sys; assert open(sys.argv[2],"rb").read()==b"0\n"; rows=[x.split() for x in open(sys.argv[1]) if x.startswith("R1H-ANCHOR ")]; assert rows; print(":".join(rows[-1][2:]))' "$INV.json" "$INV.exit")
# Later: obtain ANCHOR and HASH from these committed M3 bytes, never Intel state.
SEQ=${ANCHOR%%:*}
HEAD=${ANCHOR#*:}
INV=$RE/r1h_inventory_${SEQ}_${HEAD:0:12}
ATTEMPT=$RE/r1h_attempt_${SEQ}_${HEAD:0:12}.json
set +e
bash "$RE/r1h_host_commands.sh" inventory "$BIND.json" "$HASH" "$ANCHOR" "$BOOTSTRAP_BYTES"
RC=$?
set -e
git add -- "$ATTEMPT" "$INV.json" "$INV.stderr" "$INV.exit"
git commit -m "R1H successor attempt, capture and companions; exit=$RC"
[[ $RC == 0 ]] || exit "$RC"
# Evidence update instead of ordinary inventory: append EVIDENCE_UPDATE_JSON as fifth argument (J:3064).
```
If a capture companion is missing, commit the existing attempt/receipts individually and stop for operator-reviewed recovery; never reuse the anchor (M:88-119,134-137). For another successor, repeat extraction from the last committed zero-exit capture and the later block (M:98-119).

Local acceptance: 42 r1h tests; unchanged r1c/r1d/r1e/r1f: 9/18/27/36 OK (/tmp/r1h_acceptance.log:550-552; /tmp/r1c_acceptance.log:3-5; /tmp/r1d_acceptance.log:3-5; /tmp/r1e_acceptance.log:3-5; /tmp/r1f_acceptance.log:509-511). RED receipts: /tmp/r1h_red.log and /tmp/r1h_sync_red.log; scope-before hashes: /tmp/r1h_scope_before.json:1. Final syntax/JSON/compile/M3-probe/scope receipts: /tmp/r1h_verification.txt:1-7. No Intel commissioning evidence is supplied (T:987-1029,1353-1464).
Noticed, not fixed: M3 attempt/inventory capture bytes are preserved but are not added to the collector byte budget (M:34-40,163-227; C:753-764); this task specifies bind-byte carryover, not a new accounting rule.
Context rule for this session and every successor/team session: start a new step only at >=60% context left; at <=45%, any compaction or MAESTRO stop, finish only the current edit, save, add `## R1H HANDOFF` (done, remaining, exact paths, next single step, open risks, this rule), then reply `R1H HANDOFF`.
