# R1I — local repair; Intel binding qualification open
Aliases: RE = results/research_engine_phase1_20261011; C/B/S/M/W/T = RE/r1i_collector.py, r1i_bind_manifest.py, r1i_stub.py, r1i_make_bundle.py, r1i_host_commands.sh, test_r1i_collector.py; J = RE/intel_provisioning_manifest_v8.json; V = RE/astra_r1p7_verdict.md.
R1 holds only while the git-committed anchor is intact and unconsumed. Git remains independent authority; unknown outcomes need operator-reviewed recovery, never reuse (M:74-121,272-285,299-310; T:1360-1435,1654-1666).
Intel identity stays open until binding's strict identity/realpath equality passes; acquisition stays disabled and results remain OBSERVATION-ONLY (B:25-38; C:177-206,1131-1137).
MAESTRO's committed `RE/intel_identity_probe_r1h_20261011T131105Z.json` is a separate historical observation before the bootstrap start, not bootstrap bytes: exit 0, realpath `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9` (that JSON:1; companion .exit:1; J:1515; T:1789-1790). The r1i probe bytes are unchanged; this observation does not prove binding equality (T:1789-1790; B:25-38).
The exit-status file is outside the capture hash. Zero alone is provisional: only the canonical, committed qualified `.final`, matching committed `.exit`, authorizes consumption. Final-write/fsync errors mark retained stderr as failed, even if a complete final line survives (M:127-152,338-355; T:1611-1652).
I-INFER: T0 + budget <= GO-send time + budget = deadline - margin, because Intel T0 precedes M3 receipt of READY; neither clock's absolute offset enters the budget. Assumed clock-rate drift <= 100 ppm over 870 s is < 0.1 s, inside the sealed 5 s margin (S:1-2,50-77; M:198-214,249; J:1523; T:1437-1506,1682-1705). This is a mathematical bound, not measured Intel transport behavior.
All evidence updates are usable only inside the original 870 s window from bind start; anything later needs separately reviewed recovery. No ordinary update resets the deadline (J:1513-1516,3080; M:280-295; W:24-35).

| Astra round-7 finding/change | Answer or open reason |
|---|---|
| F1 | M:62-72,127-152,299-355; T:1611-1680. Immutable exit, exclusive final after payload/status/directory syncs; crash, write/fsync error, post-sync expiry and pre-reservation crash tests. Open: power loss and intact Git/operator commitment premises. |
| F2 | S:1-2,50-94; M:166-244; C:550-560,730-755; T:1682-1755. READY then GO; fresh sealed-margin budget, T0 enforcement and disconnection guard before effects. Open: actual Intel/SSH lifecycle, blocking IO/process lifetime beyond the bound. |
| F3 | M:154-164,249-261,281-288,315-316; C:765-776; J:1463-1466,1525-1536; T:1757-1776. One existing receipt allowance; on-disk failed/successful M3 bytes plus current dispatch reservation feed Intel admission. Committed-capture order retained. |
| F4 | S:36-49,80-94; B:25-38; C:119-194; W:28,35; T:999-1018,1228-1279,1299-1309. Verified-buffer execution/direct CLT runtime retained. Open: binding equality on Intel; prior probe is separate observation (r1i_report.md:5). |
| F5 | M:249,280-295; J:1523,3080; T:1778-1787,1524-1549. Sealed margin read at GO, no literal 5 in maker; original window unchanged. |
| F6 | Coverage below and T:1792-1796. Prior report's V:79-81 and T:1551 identity citations replaced by B:25-38/C:177-194; M:1 now describes M3 receipt writes. Fixture counts do not establish host acceptance. |
| R1 | F1 above; zero exit without committed final is refused before transport (M:127-152,281; T:1611-1680). |
| R2 | F2 above; preparation/transport delay charged by round trip, without cross-clock subtraction (M:198-214; S:66-77; T:1682-1755). |
| R3 | F3 above; no separate stored receipt counter, failures retained and charged (M:154-164,218-224,249-261; T:1757-1776). |
| R4 | F4-F6 above; strict identity stays open, same-window rule and margin consolidated (B:25-38; M:249,280-295; T:1778-1796). |
| R5 | Legacy identity item stays open until Intel bind equality passes (B:25-38; C:177-194). |

| Test | Could it pass with a relevant defect remaining? |
|---|---|
| `r1i_01` four tests, T:1611-1680 | Yes: injected crash/error boundaries and committed-byte fixtures; not a physical power-loss, double IO failure or Git-authority compromise. |
| `r1i_02` delay/skew, T:1682-1705; carried `r1h_02`, T:1437-1506 | Yes: simulated M3 time and fake transport, plus collector clock controls; not actual clock-rate or network-delay measurements. |
| `r1i_02` real stub/expired GO, T:1706-1755 | Yes: real verified-buffer stub covers READY/GO, missing/malformed GO, cap, stdin EOF and closed stdout before effects; no Intel host, remote child lifecycle or later racing disconnection. |
| `r1i_03`, T:1757-1776 | Yes: real local pipes and on-disk failure accounting with fake transport; not concurrent writers or operational Git preservation. |
| `r1i_04` and carried `r1h_04`, T:1778-1787,1524-1549 | Yes: exact margin delta, AST/JSON and command syntax/count; no successful host wrapper execution. |
| `r1i_05`, T:1789-1790 | Yes: exact SHA equality protects historical probe linkage; not Intel binding equality. |
| `r1i_06`, T:1792-1796 | Yes: wording can coexist with behavioral defects. |
| 42 carried names, T:224-1565 | Yes: fake roots/identity/children and transport instrumentation; actual stub probe/bind at T:999-1031,1228-1279; no host/power-loss acceptance. |

Prospective MAESTRO sequence after Astra review and separate host clearance: bind and inventory must run back to back, with capture + .final + hash committed between them; every attempt is committed, all dispatches inside one original 870 s window (W:24-35; M:272-355; J:3078). The carried-forward bootstrap now includes .final bytes; other measured M3 receipts and the current dispatch reservation are charged without double counting (M:35-46,285-288; C:765-776).
```bash
set -euo pipefail
RE=results/research_engine_phase1_20261011
RUNTIME=/Library/Developer/CommandLineTools/usr/bin/python3
PROBE=$RE/intel_identity_probe_r1h_20261011T131105Z.json
STAMP=$(/bin/date -u +%Y%m%dT%H%M%SZ)
BIND=$RE/r1i_bind_$STAMP
# Existing committed probe is the separate pre-bootstrap observation (r1i_report.md:5).
set +e
bash "$RE/r1i_host_commands.sh" bind "$BIND" "$PROBE"
RC=$?
set -e
# On nonzero RC: preserve existing files, commit ordinary companions only, halt.
if [[ $RC != 0 ]]; then
  for X in "$BIND.json" "$BIND.stderr" "$BIND.exit"; do if [[ -f $X ]]; then git add -- "$X"; fi; done
  git commit -m "R1I failed bind; qualified final withheld pending reviewed recovery"
  exit "$RC"
fi
HASH=$("$RUNTIME" -I -B -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$BIND.json")
git add -- "$BIND.json" "$BIND.stderr" "$BIND.exit" "$BIND.final"
git commit -m "R1I bind capture-sha256=$HASH; committed qualified final"
BOOTSTRAP_BYTES=$("$RUNTIME" -I -B "$RE/r1i_make_bundle.py" inventory --capture "$BIND.json" --expected-capture-sha256 "$HASH" --bootstrap-bytes-only)
CORE=$("$RUNTIME" -I -B -c 'import json,sys; raw=open(sys.argv[1],"rb").read(); p=json.loads(raw.split(b"\n",1)[1] if raw.startswith(b"R1I-READY ") else raw); print(json.loads(p["bound_manifest_json"])["window_seal"]["core_sha256"])' "$BIND.json")
ANCHOR=none
# Repeat this block for successors only within the same window; never retry an anchor.
SEQ=${ANCHOR%%:*}; HEAD=${ANCHOR#*:}
if [[ $ANCHOR == none ]]; then SEQ=0; HEAD=$CORE; fi
INV=$RE/r1i_inventory_${SEQ}_${HEAD:0:12}
ATTEMPT=$RE/r1i_attempt_${SEQ}_${HEAD:0:12}.json
set +e
if [[ -n ${EVIDENCE_UPDATE_JSON:-} ]]; then
  bash "$RE/r1i_host_commands.sh" inventory "$BIND.json" "$HASH" "$ANCHOR" "$BOOTSTRAP_BYTES" "$EVIDENCE_UPDATE_JSON"
else
  bash "$RE/r1i_host_commands.sh" inventory "$BIND.json" "$HASH" "$ANCHOR" "$BOOTSTRAP_BYTES"
fi
RC=$?
set -e
for X in "$ATTEMPT" "$INV.json" "$INV.stderr" "$INV.exit"; do if [[ -f $X ]]; then git add -- "$X"; fi; done
if [[ $RC == 0 ]]; then git add -- "$INV.final"; fi
git commit -m "R1I attempt and preserved companions; exit=$RC"
[[ $RC == 0 ]] || exit "$RC"
# This extracts a candidate; dispatch rechecks committed final/status/all companions.
ANCHOR=$(git show "HEAD:$INV.json" | "$RUNTIME" -I -B -c 'import sys; rows=[s.split() for s in sys.stdin if s.startswith("R1H-ANCHOR ")]; assert rows; print(":".join(rows[-1][2:]))')
# Return to SEQ/HEAD for another inventory/evidence update before original expiry.
```
On any unknown outcome or missing/partial/unparseable final, keep every file (including failed .final bytes) charged on disk and stop for operator-reviewed recovery; do not publish uncertain .final as authority or reuse an anchor (M:99-152,272-285,299-355; J:1526-1536).
Local verification receipt: `/usr/bin/python3 -B -m unittest discover -s RE -p test_r1i_collector.py`: 54 OK (42 carried names + 12 criterion tests, T:224-1796); unchanged predecessor discovery patterns test_r1c/r1d/r1e/r1f/r1h_collector.py: 9/18/27/36/42 OK. `bash -n RE/r1i_host_commands.sh`, v8/update/procedure syntax and JSON: OK (W:1-38; J:3080; T:1524-1549). Direct CLT `-I -B RE/r1i_identity_probe.py` on M3: parseable JSON, no RE file changes, probe SHA256 `83c4379281c8a7f0e5b99f6894cfc6824587333b8fd720930fa804d4fde625c8` (T:1789-1790). Initial copies were RED; targeted final-fsync test was RED then GREEN after preserving failure stderr (T:1623-1652; M:134-135,349-355). No Intel dispatch was executed by this task (W:2; local framing fixtures T:1706-1755).
Noticed, not fixed: blocking IO can leave a remote process alive; no host lifecycle qualification beyond effect/deadline checks is supplied (S:66-77; C:813-842; V:27-45).
Context rule for this and every successor/team session: start a new step only at >=60% context left; at <=45%, any compaction or MAESTRO stop, finish only the current edit, save, add `
