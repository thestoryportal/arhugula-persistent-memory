# R1J — local repairs; Intel binding qualification open
Aliases: RE = results/research_engine_phase1_20261011; C/B/S/M/W/T/P = RE/r1j_collector.py, r1j_bind_manifest.py, r1j_stub.py, r1j_make_bundle.py, r1j_host_commands.sh, test_r1j_collector.py, r1j_identity_probe.py; J = RE/intel_provisioning_manifest_v9.json.
R1 holds only while the git-committed anchor is intact and unconsumed; Git remains independent authority; serialized M3 dispatch is a premise. Unknown outcomes require operator-reviewed recovery, never anchor reuse (M:85-132,281-291,309-316; T:1360-1435,1654-1666).
Intel identity stays open until binding's strict identity/realpath equality runs on Intel; acquisition stays disabled and results remain OBSERVATION-ONLY. Identical probe bytes preserve the separate historical observation before the bootstrap start, not current binding equality (B:48-63; C:177-206,1131-1137; T:1984).
The exit-status file is outside the capture hash. R1 publish rule: durable pending bytes only; exclusive .final.pending write, flush, file fsync and directory fsync precede a fresh M3 reading <= deadline, then os.link publishes .final exclusively and directory fsync follows. Pending is never authority, even committed; .exit is written once. No acceptance depends on a stderr marker; its successful write is merely extra diagnostic evidence (M:62-82,138-160,345-365; T:1803-1909).
OPEN post-link directory-fsync narrowing: dispatch exits nonzero, nothing is unlinked or rewritten; file content is durable, only the directory entry's durability is uncertain. Surviving .final can qualify if subsequently committed: Astra must rule on this narrowing. The error marker cannot disqualify it (M:74-82,138-160,361-365; T:1873-1909).
R2 in-binding cutoff: Intel T0 is the first monotonic reading; the stub supplies T0 + budget. Binder checks before each identity measurement, on every probe-namespace Python line event in entry/chunk loops, after measurements and immediately before success output. Premise: normal Python tracing delivers these events; it does not interrupt blocking I/O or C operations (S:1-2,91-93; B:11-32,48,63,82-90; P:12-64; T:1911-1975).
I-INFER: T0 + budget <= GO-send time + budget = deadline - margin because Intel T0 precedes M3 READY receipt. Assumed clock-rate drift <= 100 ppm over 870 s is < 0.1 s, within the sealed 5 s margin; this inequality alone does not enforce binding or process lifetime (S:1-2,50-77; M:207-223; J:1523; B:11-32,85).
OPEN: S:36 initial bundle read, blocking I/O and remote process lifetime have no new timeout machinery; historical probe observation is distinct from strict current binding equality (S:15-36,66-94; B:48-63; C:813-842).

| Astra round-8 finding/change | Answer or open reason |
|---|---|
| F1 | Durable pending publication replaces corrective rejection; pre-link failures leave no .final. Post-link directory durability remains open as above (M:62-82,345-365; T:1803-1909). |
| F2 | Binder now enforces cutoff during identity loops and before publication; bundle read/blocking I/O/process lifetime remain open (S:92; B:11-32,48,63,82-90; T:1911-1975). |
| F3 | Failed runs, per-dispatch reservation, output bound and committed-capture gate retained; .final.pending bytes charged (M:35-46,163-173,255-297,323-324; C:765-776; J:1526-1537; T:1757-1776,1977-1989). |
| F4 | Probe byte identity preserves historical observation linkage; Intel binding equality remains open until bind runs (T:1984; B:48-63). |
| F5 | Marker premise, cutoff inequality versus enforcement and original window explicit; citations target r1j sources (M:138-160,207-223; B:11-32,85; J:3081; T:1990-1998). |
| F6 | Coverage below states residual defects; test line numbers identify assertions, not proof a run passed (T:1803-1998). |
| R1 | F1 above; all surviving pending bytes committed in fixtures, bind consumption/qualified/require_anchor/successor dispatch refuse before ssh (T:1803-1871; M:110-160,287-291). |
| R2 | F2 above; real stub/compiler/binder with verified fixture identity and real clocks crosses Intel cutoff before M3 deadline; ample budget succeeds; last publication check separately tested (T:1911-1975). |
| R3 | F3 above; exact probe SHA equality, v9 JSON/runtime paths and bash syntax asserted; no host acceptance implied (T:1977-1989; W:7-35; J:1526-1537). |
| R4 | F4-F6 above; prospective procedure preserves same-window commit order and every attempt; strict Intel equality and acquisition remain open (B:48-63; C:197-206; M:287-297; T:1990-1998). |
| R5 | Carried legacy label: current Intel identity remains open until strict bind equality runs (B:48-63). |

| Test | Could it pass with a relevant defect remaining? |
|---|---|
| r1j_01 pending failures, T:1803-1871 | Yes: injected persistence/crash and committed-byte fixtures can miss physical power loss or competing writers; they include marker failure/absence and all surviving bytes. |
| r1j_01 publish order/post-link, T:1873-1909 | Yes: simulated clock and fake transport; directory-entry durability after physical power loss remains open, and post-link error content can qualify if committed. |
| r1j_02 real cutoff and ample budget, T:1911-1957 | Yes: real local stub/binder/loader/clocks with a verified fake identity loop; no Intel filesystem/SSH behavior or blocked syscall/lifecycle acceptance. |
| r1j_02 last publish check, T:1959-1975 | Yes: synthetic cutoff advancement during JSON encoding, actual binder; not a blocked stdout or real Intel timing test. |
| r1j_03, T:1977-1989 | Yes: file sizes, JSON, syntax and SHA assertions; no concurrent writer safety or current Intel binding equality. |
| r1j_04, T:1990-1998 | Yes: wording can coexist with behavioral defects. |
| 54 carried names, T:224-1796 | Yes: fake roots/identity/transport, plus local real stub paths; no host/power-loss proof. Accounting/output bounds and original committed-capture order remain asserted (T:1508-1522,1757-1776). |

Prospective MAESTRO sequence after Astra review and separate host clearance: bind and inventory must run back to back, with capture + .final + hash committed between them; every attempt and pending companion is committed inside one original 870 s window. No update resets it. The carried-forward bootstrap includes final bytes; pending is separately charged by measured M3 receipts, without double counting bootstrap (W:24-35; M:35-46,287-297; J:1513-1516,1526-1537,3081).
```bash
set -euo pipefail
RE=results/research_engine_phase1_20261011
RUNTIME=/Library/Developer/CommandLineTools/usr/bin/python3
PROBE=$RE/intel_identity_probe_r1h_20261011T131105Z.json
STAMP=$(/bin/date -u +%Y%m%dT%H%M%SZ)
BIND=$RE/r1j_bind_$STAMP
set +e
bash "$RE/r1j_host_commands.sh" bind "$BIND" "$PROBE"
RC=$?
set -e
if [[ $RC != 0 ]]; then
  for X in "$BIND.json" "$BIND.stderr" "$BIND.exit" "$BIND.final.pending"; do if [[ -f $X ]]; then git add -- "$X"; fi; done
  git commit -m "R1J failed bind; preserve pending evidence; review any surviving final"
  exit "$RC"
fi
HASH=$("$RUNTIME" -I -B -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$BIND.json")
git add -- "$BIND.json" "$BIND.stderr" "$BIND.exit" "$BIND.final.pending" "$BIND.final"
git commit -m "R1J bind capture-sha256=$HASH; committed qualified final"
BOOTSTRAP_BYTES=$("$RUNTIME" -I -B "$RE/r1j_make_bundle.py" inventory --capture "$BIND.json" --expected-capture-sha256 "$HASH" --bootstrap-bytes-only)
CORE=$("$RUNTIME" -I -B -c 'import json,sys; raw=open(sys.argv[1],"rb").read(); p=json.loads(raw.split(b"\n",1)[1] if raw.startswith(b"R1I-READY ") else raw); print(json.loads(p["bound_manifest_json"])["window_seal"]["core_sha256"])' "$BIND.json")
ANCHOR=none
# Repeat from SEQ only before original expiry; never retry a consumed anchor (M:281-291).
SEQ=${ANCHOR%%:*}; HEAD=${ANCHOR#*:}
if [[ $ANCHOR == none ]]; then SEQ=0; HEAD=$CORE; fi
INV=$RE/r1j_inventory_${SEQ}_${HEAD:0:12}
ATTEMPT=$RE/r1j_attempt_${SEQ}_${HEAD:0:12}.json
set +e
if [[ -n ${EVIDENCE_UPDATE_JSON:-} ]]; then
  bash "$RE/r1j_host_commands.sh" inventory "$BIND.json" "$HASH" "$ANCHOR" "$BOOTSTRAP_BYTES" "$EVIDENCE_UPDATE_JSON"
else
  bash "$RE/r1j_host_commands.sh" inventory "$BIND.json" "$HASH" "$ANCHOR" "$BOOTSTRAP_BYTES"
fi
RC=$?
set -e
for X in "$ATTEMPT" "$INV.json" "$INV.stderr" "$INV.exit" "$INV.final.pending"; do if [[ -f $X ]]; then git add -- "$X"; fi; done
if [[ $RC == 0 ]]; then git add -- "$INV.final"; fi
git commit -m "R1J attempt and preserved companions; exit=$RC"
[[ $RC == 0 ]] || exit "$RC"
ANCHOR=$(git show "HEAD:$INV.json" | "$RUNTIME" -I -B -c 'import sys; rows=[s.split() for s in sys.stdin if s.startswith("R1H-ANCHOR ")]; assert rows; print(":".join(rows[-1][2:]))')
```
Unknown outcome, missing final or nonzero dispatch: preserve every byte, leave any uncertain final uncommitted, halt for separately reviewed recovery; never consume pending or reuse an anchor (M:74-82,110-132,281-291,358-370).
Noticed, not fixed: blocking I/O may outlive the remote cutoff; process lifetime remains open (S:36,66-77; C:813-842).
Local RED execution: 61 tests, 15 failures/1 error against retargeted copies, including real bind cutoff publication; fixture names/runtime prefix corrected before that run (`/private/tmp/r1j_red_fixture_corrected.log:719-753`). Local GREEN execution: 61 tests, zero failures/errors, OK (`/private/tmp/r1j_green_final.log:609-611`); T citations elsewhere are assertions, not run receipts.
Unchanged predecessor executions: r1c 9 OK (`/private/tmp/r1j_predecessor_test_r1c_collector.log:3-5`), r1d 18 OK (`/private/tmp/r1j_predecessor_test_r1d_collector.log:3-5`), r1e 27 OK (`/private/tmp/r1j_predecessor_test_r1e_collector.log:4-6`), r1f 36 OK (`/private/tmp/r1j_predecessor_test_r1f_collector.log:509-511`), r1h 42 OK (`/private/tmp/r1j_predecessor_test_r1h_collector.log:550-552`), r1i 54 OK (`/private/tmp/r1j_predecessor_test_r1i_collector.log:603-605`).
Validation execution: 137 existing files unchanged, nine authorized additions; v9 parses, wrapper/report script bash syntax passes; direct M3 CLT -I -B probe produces parsed JSON and no RE file changes, SHA256 83c4379281c8a7f0e5b99f6894cfc6824587333b8fd720930fa804d4fde625c8 (`/private/tmp/r1j_validation.log:1-5`; M3 output `/private/tmp/r1j_m3_probe.json:1`).
Noticed, not fixed: the carried substring check can flag CLT commands with an unquoted script argument; the new M3 probe command uses a quoted argument (T:1310; J:1569). Strict runtime/realpath assertions remain intact (T:1299-1310).
