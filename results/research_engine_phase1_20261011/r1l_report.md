# R1L — receipt capacity repair; local GREEN, exact Intel overshoot blocked
RE = results/research_engine_phase1_20261011; C/S/B = RE/r1j_collector.py, r1j_stub.py, r1j_bind_manifest.py; M = RE/r1l_make_bundle.py; J = RE/intel_provisioning_manifest_v10.json; T = RE/test_r1l_collector.py; X = RE/r1j_inventory_0_a49c11de49ce.json; H = RE/r1j_inventory_halt_diagnostic_20261011.json.
Scope: new maker copied from r1j, new test copied from R1K, new v10 copied from v9; original hashes unchanged; all 62 carried test bodies identical after path retargeting (/private/tmp/r1l_scope_20261011.log:1-12). No host acceptance is claimed (RE/astra_r1p10_verdict.md:30-34).
Root cause: the inventory stream's `writing_bytes` grows by each encoded observation; the receipt pre-admission refuses its next row or final registration commit when the cumulative sum would exceed 10,000,000. The limit is enforced before writing; stored usage need not cross it (C:765-784,790-807; X:29,81608-81610).
`usage()` = bootstrap + measured/reserved M3 + registry + emergency-journal reservation + registered non-download sizes + current writing bytes. Until the inventory commits, its bytes are in `writing_bytes`, not `registered`; halt preserves them and writes the reserved failure receipt (C:357-366,586-590,697-727,765-776).
Intel arithmetic: bind capture 113,394 + exit 2 + final 98 = bootstrap 113,494; pending 98 is separately charged, so pre-dispatch measured M3 = 113,592 and bootstrap + M3 argument = 113,592 + 2,500,000 = 2,613,592 (RE/r1j_bind_20261011T143208Z.json:1-2; RE/r1j_bind_20261011T143208Z.exit:1; RE/r1j_bind_20261011T143208Z.final:1; RE/r1j_bind_20261011T143208Z.final.pending:1; M:35-46,163-173,294-297).
With failure.json's registered 16,384 bytes, remaining allowance for inventory + window + registry + emergency reservation is 10,000,000 - 2,613,592 - 16,384 = 7,370,024 bytes; actual stream capacity is smaller (C:363-366,374-401,765-776; J:1634).
X's 81,599 LIVE lines occupy 734,391 bytes, 10 anchors occupy 1,430, and READY occupies 75: total 735,896. Live stdout never increments `writing_bytes`; the 2,500,000 output reservation already covers it. It did not cause this refusal (S:69-77; C:765-776; M:294; X:1-81610; H:19-27).
Exact host crossing amount is NOT recoverable from X: it publishes anchors, not inventory rows or usage/amount; stderr gives only the refusal. Let W=partial inventory bytes, R=registry bytes before halt, Q=registered window bytes, E=emergency reservation, A=rejected row/commit bytes: δ=2,613,592+16,384+W+R+Q+E+A-10,000,000 > 0. W is the growing term; δ's numeric value, W and A are UNVERIFIABLE without retained Intel receipt/admission evidence. Refusal precedes writing A (C:447-448,550-575,765-784,790-807; X:29,81608-81610; RE/r1j_inventory_0_a49c11de49ce.stderr:1).
All transport_check call sites: `_check_write` calls its injected guard once per admission; `remaining` calls it once per clock check; `halt` calls it once per invocation. Binder and identity have no TRANSPORT_CHECK calls; binder uses check_cutoff (C:550-559,697-701,745-755; S:69-85; B:11-32).
Inventory frequencies: one walk remaining per observed entry; one remaining per nonempty baseline hash chunk; one _check_write per row, whose internal remaining adds another check after failure.json exists; journal/exclusive writes add the same guards. Checks stay unchanged (C:550-575,592-607,874-880,918-944,790-807).
Intel attempt's setup through stream-begin emits 20 calls = 16 _check_write + 4 remaining; failure invokes halt twice (admit_bytes then main's exception path); X has no inventory commit between anchors 7 and 8 (C:374-431,550-607,697-701,1265-1275; X:1-29,81608-81610).
If refusal was a row admission, N attempted rows and D nonempty hash chunks satisfy 3N+D=81,577; direct-site counts are 16+N, 4+2N+D, 2. If final stream-commit admission refused, 3N+D=81,575, counts 17+N, 5+2N+D, 2. X cannot distinguish those branches or separate N/D; it does establish 81,599 checks and an uncommitted inventory stream (C:790-807,874-880,918-944; X:29,81608-81610).
ONE repair: seal receipt allowance 18,000,000 in both receipt component and collector; planned peak becomes 1,999,764,570, margin 235,430, within unchanged setup cap 2,000,000,000. Eight extra MB is the largest whole-MB increase fitting the prior 8,235,430 margin (J:1372,1463-1471,1633; RE/intel_provisioning_manifest_v9.json:1470-1471).
Fresh retained/registration paths are lifecycle companions of the new sealed window, preserving expired HALTED state without deleting or reusing it. Maker changes only its two manifest filename references; r1j capture/attempt names remain so receipt_usage still counts all old failures/pending bytes (J:122,1620-1626,1728; M:23-24,163-173,256,281-299; /private/tmp/r1l_scope_20261011.log:9).
Why more allowance: the honest 32,000-file fixture writes 13,730,405 inventory bytes; with M3 reservation alone it needs at least 16,230,503 before other receipts. Ten MB cannot admit it; 18 MB passes without dropping rows/fields/hashes. This is a bounded workload proof, NOT proof the entire Intel tree fits 18 MB (T:2031-2053,2114-2129; /private/tmp/r1l_green2_20261011.log:608).
Guarantees preserved: accounting/admission and output bound unchanged; durable pending → cutoff check → exclusive final link unchanged; binding tracing/strict identity equality unchanged; acquisition remains disabled and outputs OBSERVATION-ONLY. This follows unchanged production hashes, maker's manifest-only delta, sealed-policy equality and carried tests (C:177-206,765-788,1131-1137; B:11-32,48-63,82-90; M:62-82,138-160,345-365; T:2131-2154; /private/tmp/r1l_scope_20261011.log:1-9).
RED: full discover with `-k test_r1l_` selected all 64 tests because module name matches; 62 carried passed, two new failed. Real stub/collector inventory refused exit 1; used 9,999,890 + next row 429 = 10,000,319: overshoot 319; W=7,471,614, registry=2,632, registered=17,150, E=544, bootstrap=7,852, M3=2,500,098. Sum equals used; 52,282 calls = 17,436 _check_write + 34,844 remaining + 2 halt (/private/tmp/r1l_red_20261011.log:608,611-631; T:2054-2114).
First GREEN candidate: child succeeded, test glob selected inventory-accounting; fixed only fixture selection to exclude that file. No second production repair (/private/tmp/r1l_green_20261011.log:608-623; T:2100-2103).
GREEN exact acceptance: `LLMDB_ROOT=$PWD /usr/bin/python3 -B -m unittest discover -s results/research_engine_phase1_20261011 -p 'test_r1l_collector.py'` → 64/64; unchanged R1K command → 62/62. Positive transport counts 32,032 _check_write + 64,031 remaining = 96,063; stdout 867,151 bytes, no stderr (/private/tmp/r1l_green2_20261011.log:608-613; /private/tmp/r1l_carried_20261011.log:610-612).
Raw local logs: /private/tmp/r1l_{red,green,green2,carried}_20261011.log. Hashes and predecessor before/after pins: /private/tmp/r1l_scope_20261011.log:1-16. Fixture roots were temporary; identity/transport substitutions are fixture-only (T:2054-2101).
Rerun is prospective, requires Astra + operator GO, and is NOT executed. Commit approved R1L package before starting its clock. Original 14:32:08Z + 870 s expired at 14:46:38Z; a fresh v10 bind/core/window is mandatory. Never retry old 0:a49c11de49ce… or use its capture as success (H:3-6,21,33-36; J:1513,1620,1728; M:281-311; RE/astra_r1p10_verdict.md:34).
Receipt budget now retained: old bind 113,592 + failed inventory 735,896+43+2 + attempt 404 = 849,937 bytes. Both fresh dispatches each require 2,500,000 remaining allowance. Worst M3 reservation including both is 5,849,937, leaving 12,150,063 of 18 MB for Intel receipts. Actual inventory budget is 18 MB minus measured old+fresh-bind receipts minus 2.5 MB, including pending separately, with bootstrap counted once (M:163-173,256-266,294-297; H:19-27; RE/r1j_attempt_0_a49c11de49ce.json:1; RE/r1j_inventory_0_a49c11de49ce.stderr:1; RE/r1j_inventory_0_a49c11de49ce.exit:1).
MAESTRO sequence below preserves capture/exit/pending/final on every result, commits bind before inventory, and commits attempt/inventory before this fresh bind's original expiry. No retries on nonzero/unknown outcomes; surviving final needs separate review. Finish within 870 s including commits remains unmeasured (M:138-160,281-318,345-375; RE/r1k_report.md:6-10,36).
```bash
set -euo pipefail
set -C
umask 077
RE=results/research_engine_phase1_20261011
RT=/Library/Developer/CommandLineTools/usr/bin/python3
PROBE=$RE/intel_identity_probe_r1h_20261011T131105Z.json
STAMP=$(/bin/date -u +%Y%m%dT%H%M%SZ)
BIND=$RE/r1j_bind_r1l_$STAMP
START=$(/bin/date -u +%Y-%m-%dT%H:%M:%SZ)
set +e
"$RT" -I -B "$RE/r1l_make_bundle.py" bind --dispatch-m3 --capture-prefix "$BIND" --probe "$PROBE" --bootstrap-start-utc "$START" --ssh-argv ssh -T -i ~/.ssh/intel_mac_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes robertrhu_node2@192.168.10.2
RC=$?
set -e
for F in "$BIND.json" "$BIND.stderr" "$BIND.exit" "$BIND.final.pending" "$BIND.final"; do if [[ -f $F ]]; then git add -- "$F"; fi; done
git commit -m "R1L fresh bind receipts; preserve exact outcome"
if [[ $RC != 0 ]]; then exit "$RC"; fi
HASH=$("$RT" -I -B -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$BIND.json")
BOOT=$("$RT" -I -B "$RE/r1l_make_bundle.py" inventory --capture "$BIND.json" --expected-capture-sha256 "$HASH" --bootstrap-bytes-only)
CORE=$("$RT" -I -B -c 'import json,sys; b=open(sys.argv[1],"rb").read(); p=json.loads(b.split(b"\n",1)[1] if b.startswith(b"R1I-READY ") else b); print(json.loads(p["bound_manifest_json"])["window_seal"]["core_sha256"])' "$BIND.json")
[[ $HASH =~ ^[0-9a-f]{64}$ && $CORE =~ ^[0-9a-f]{64}$ && $BOOT =~ ^[1-9][0-9]*$ ]]
INV=$RE/r1j_inventory_0_${CORE:0:12}
ATTEMPT=$RE/r1j_attempt_0_${CORE:0:12}.json
set +e
"$RT" -I -B "$RE/r1l_make_bundle.py" inventory --dispatch-m3 --capture "$BIND.json" --expected-capture-sha256 "$HASH" --expected-anchor none --bootstrap-bytes "$BOOT" --ssh-argv ssh -T -i ~/.ssh/intel_mac_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes robertrhu_node2@192.168.10.2
RC=$?
set -e
for F in "$ATTEMPT" "$INV.json" "$INV.stderr" "$INV.exit" "$INV.final.pending" "$INV.final"; do if [[ -f $F ]]; then git add -- "$F"; fi; done
git commit -m "R1L inventory attempt and exact outcome; never retry anchor"
exit "$RC"
```
Command arguments/runtime/identity match preserved wrapper policy; fresh maker selects v10, and dispatch itself enforces expiry and committed capture qualification (RE/r1j_host_commands.sh:7-12,24-35; M:23-24,256-311,380-410).
Open: exact Intel numerical overshoot and row-vs-commit branch need evidence absent from X; complete Intel workload/transport/filesystem acceptance and actual same-window completion remain unverified. No stdout, cutoff, accounting, anchor or identity checks were weakened (C:765-807; RE/astra_r1p10_verdict.md:8-16,30-34; /private/tmp/r1l_scope_20261011.log:1-9).
