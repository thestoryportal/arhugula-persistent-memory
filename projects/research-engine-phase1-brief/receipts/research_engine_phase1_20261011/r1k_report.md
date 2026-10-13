# R1K — round-9 validation repair; Intel binding qualification open
Aliases: RE = results/research_engine_phase1_20261011; C/B/S/M/W/T/P = RE/r1j_collector.py, r1j_bind_manifest.py, r1j_stub.py, r1j_make_bundle.py, r1j_host_commands.sh, test_r1k_collector.py, r1j_identity_probe.py; J = RE/intel_provisioning_manifest_v9.json; D = RE/r1k_report.md; V9 = RE/astra_r1p9_verdict.md.
L = /private/var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/r1k_udphlmmh (local raw receipts; not Intel evidence).
R1 holds only while the git-committed anchor is intact and unconsumed; Git remains independent authority; serialized M3 dispatch is a premise. Unknown outcomes require operator-reviewed recovery, never anchor reuse (M:85-132,281-291,309-316; T:1360-1435,1654-1666).
Intel identity stays open until binding's strict identity/realpath equality runs on Intel; acquisition stays disabled and results remain OBSERVATION-ONLY. Identical probe bytes preserve the separate historical observation before the bootstrap start, not current binding equality (B:48-63; C:177-206,1131-1137; T:1995).
The exit-status file is outside the capture hash. R1 publish rule: durable pending bytes only; exclusive .final.pending write, flush, file fsync and directory fsync precede a fresh M3 reading <= deadline, then os.link publishes .final exclusively and directory fsync follows. Pending is never authority, even committed; .exit is written once. No acceptance depends on a stderr marker; its successful write is merely extra diagnostic evidence (M:62-82,138-160,345-365; T:1803-1909).
ACCEPTED post-link directory-fsync narrowing (V9:9-14, F2): durable content before publication; directory-entry durability after link remains uncertain, with separately reviewed recovery after unknown/nonzero dispatch. A surviving .final can qualify once committed; unconditional rejection of every failed finalization is not established. The error marker cannot disqualify it (M:74-82,138-160,361-365; T:1873-1907).
R2 in-binding cutoff: Intel T0 is the first monotonic reading; the stub supplies T0 + budget. Binder checks before each identity measurement, on every probe-namespace Python line event in entry/chunk loops, after measurements and immediately before success output. Premise: normal Python tracing delivers these events; it does not interrupt blocking I/O or C operations (S:1-2,91-93; B:11-32,48,63,82-90; P:12-64; T:1909-1986,2010-2028).
I-INFER: T0 + budget <= GO-send time + budget = deadline - margin because Intel T0 precedes M3 READY receipt. Assumed clock-rate drift <= 100 ppm over 870 s is < 0.1 s, within the sealed 5 s margin; this inequality alone does not enforce binding or process lifetime (S:1-2,50-77; M:207-223; J:1523; B:11-32,85).
OPEN (V9:15-17, F3): stdout publication after the final check can finish late under blocking output or suspension (B:85-86); S:36 initial bundle read, blocking I/O and remote process lifetime remain open. Historical probe observation is distinct from strict current binding equality (S:15-36,66-94; B:48-63; C:813-842).

| Carried round-8 labels with round-9 corrections (D:7,10,21,30,36) | Answer or open reason |
|---|---|
| F1 | Durable pending publication replaces corrective rejection; pre-link failures leave no .final. V9 F2 accepts durable-content narrowing as above (M:62-82,345-365; T:1803-1909). |
| F2 | New evidence proves entry before cutoff, completed iterations and interruption before normal loop completion; bundle read/blocking I/O/process lifetime remain open (S:92; B:11-32,48,63,82-90; T:2010-2028). |
| F3 | Failed runs, per-dispatch reservation, output bound and committed-capture gate retained; .final.pending bytes charged (M:35-46,163-173,255-297,323-324; C:765-776; J:1526-1537; T:1757-1776,1988-2000). |
| F4 | Probe byte identity preserves historical observation linkage; Intel binding equality remains open until bind runs (T:1995; B:48-63). |
| F5 | Marker premise, cutoff inequality versus enforcement and original window explicit; citations target r1j sources (M:138-160,207-223; B:11-32,85; J:3081; T:2001-2009). |
| F6 | Coverage below states residual defects; test line numbers identify assertions, not proof a run passed (T:1803-2028). |
| R1 | F1 above; all surviving pending bytes committed in fixtures, bind consumption/qualified/require_anchor/successor dispatch refuse before ssh (T:1803-1871; M:110-160,287-291). |
| R2 | r1k_01 proves identity-loop entry time < the actual cutoff, at least one completed iteration, no normal loop completion, cutoff refusal with rc != 0, no success publication/.final, before M3 deadline; real stub/compiler/binder/collector/clocks, ample-budget control retained (T:1909-1968,2010-2028; actual binder global read at T:1923-1928, supplied at S:92; B:23,28; V9:29-31). |
| R3 | F3 above; exact probe SHA equality, v9 JSON/runtime paths and bash syntax asserted; no host acceptance implied (T:1988-2000; W:7-35; J:1526-1537). |
| R4 | F4-F6 above; prospective procedure preserves same-window commit order and every attempt; strict Intel equality and acquisition remain open (B:48-63; C:197-206; M:287-297; T:2001-2009; D:36-78). |
| R5 | Carried legacy label: current Intel identity remains open until strict bind equality runs (B:48-63). |

| Test | Could it pass with a relevant defect remaining? |
|---|---|
| r1j_01 pending failures, T:1803-1871 | Yes: injected persistence/crash and committed-byte fixtures can miss physical power loss or competing writers; they include marker failure/absence and all surviving bytes. |
| r1j_01 publish order/post-link, T:1873-1909 | Yes: simulated clock and fake transport; directory-entry durability after physical power loss remains open, and post-link error content can qualify if committed. |
| r1k_01 loop entry/interruption, T:2010-2028; r1j_02 ample budget, T:1962-1968 | Entry time < actual cutoff, completed iterations, no loop completion and cutoff refusal are asserted before M3 deadline. Yes: verified substituted identity/local transport do not prove Intel filesystem/SSH behavior, blocked syscall or lifecycle acceptance (T:1909-1951). |
| r1j_02 last publish check, T:1970-1986 | Yes: synthetic cutoff advancement during JSON encoding, actual binder; not a blocked stdout or real Intel timing test. |
| r1j_03, T:1988-2000 | Yes: file sizes, JSON, syntax and SHA assertions; no concurrent writer safety or current Intel binding equality. |
| r1j_04, T:2001-2009 | Yes: wording can coexist with behavioral defects. |
| 54 carried names, T:224-1796 | Yes: fake roots/identity/transport, plus local real stub paths; no host/power-loss proof. Accounting/output bounds and original committed-capture order remain asserted (T:1508-1522,1757-1776). |

Prospective MAESTRO sequence after Astra review and separate host clearance: bind and inventory must run back to back, with capture + .final + hash committed between them. The procedure runs bind → commit → inventory in order inside the original 870 s window if sufficient time remains; completion within 870 s is not measured, including commits (V9:23-25, F5). Every attempt and pending companion must be committed before original expiry; no update resets it. The carried-forward bootstrap includes final bytes; pending is separately charged by measured M3 receipts, without double counting bootstrap (W:24-35; M:35-46,287-297; J:1513-1516,1526-1537,3081).
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
R1K scope: only T and D added as copies; production r1j_* and v9 unchanged. All 61 carried test names remain; six report reads target D so the 90-line limit applies to this report. No Intel/SSH/network/tmux run, host acceptance or new timeout machinery.
Local RED: new assertions on the copied original fixture fail at missing entry evidence (L/red_missing_entry.log:1-18). GREEN: new test and ample-budget control pass (L/green_new_test.log:1-7; L/green_positive.log:1-7); Observed entry 0.121690833 < cutoff 0.25023905226130705, 13 completed iterations, no completion marker, rc 1 and no .final (L/green_observed/capture.stderr:1-15; L/green_observed/observed.json:1); assertions elsewhere are not run receipts.
Scratch counterexample: scratch copy changes only T, budget target 0.3 → 0.12 s at T:1914; actual GO budget 0.05331789970398404 s, rc 1, Intel monotonic budget expired before identity entry, no .final. New test FAILS at the missing-entry assertion (L/scratch_preloop.log:1-18; L/preloop_observed/observed.json:1; L/preloop_observed/capture.stderr:1). The first 0.03 s probe exhausted budget before GO; that is not the Intel counterexample.
Acceptance: exact /usr/bin/python3 -B -m unittest discover commands with -s RE and -p test_r1k_collector.py / test_r1j_collector.py pass 62/62 and 61/61 respectively (L/green_62.log:610-612; L/green_r1j_61.log:609-611). All 150 pre-existing RE files unchanged; only T/D added, report 83 lines and bash block parses (L/scope_audit_final.json:1; test names L/test_names.json:1).
Noticed, not fixed: blocking I/O/remote process lifetime and the carried CLT substring check remain open (S:36,66-77; C:813-842; T:1310; J:1569).
