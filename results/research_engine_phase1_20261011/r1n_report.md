# R1N: v11 local replan, ready for Astra
Aliases: RE=results/research_engine_phase1_20261011; C=RE/r1j_collector.py; M=RE/r1l_make_bundle.py; J=RE/intel_provisioning_manifest_v10.json; Q=RE/r1m_size_probe.py; E=RE/r1m_evaluate.py; CAP=RE/r1j_probe_r1m_20261011T154940Z.json; EOUT=RE/r1m_evaluate_20261011T154940Z.out; G=RE/r1n_make_manifest_v11.py; J11=RE/intel_provisioning_manifest_v11.json; N=RE/r1n_evaluate.py; A=RE/r1n_sizing_dispatch.py; T=RE/test_r1n_replan.py; GD11=RE/r1n_gate_d_checklist.md.
Status: local fixtures GREEN; Astra review and a newly authorized real Intel A–E chain remain pending. The earlier chain stopped at B and its authorization is spent (RE/r1m_chain_stop_20261011.md:7-8). This work is an inventory-budget engineering replan, not an F1 scientific result.

## Budget and source justification
Keep setup cap 2,000,000,000. Raise receipts 18,000,000 -> 42,000,000; reduce retained_failure_extra 70,000,000 -> 16,384. Non-receipts become 1,911,780,954; planned_peak = non-receipts + sealed receipts = 1,953,780,954; margin 46,219,046 (G:11-34; T:38-48).
J explicitly reserves one failed attempt; its retained payload/build image stays charged above, and it forbids retry/additional full duplicates. Those components are retained archive/payload, extra image, source work/output, extraction and caches, whose budgets remain unchanged (J:1378-1453,1456-1460; T:27-37). C's failure mechanism writes one padded record <=16,384, refuses oversized argv before execution and never creates another full payload on HALT; incomplete downloads refuse retry and their payload bound is reserved before write (C:701-726,854-855,969-985; J:1634). Thus 16,384 covers that extra record; its separate receipt charge is conservatively retained too. This does not prove unmeasured source build or installation peaks: J's conditional status and blocking evidence slots remain (J:1473-1477).

## Fixed rule, before the NEXT measurement
The allowance was sized from CAP, not preregistered before CAP. Fix NOW: D(B)=max(1,000,000,ceil(B/5)), where B is exact measured encoded baseline row bytes, excluding the separate 65,536 future-collector reserve. At CAP B=20,048,510, D=4,009,702. Fix W1=D(B_CAP)=4,009,702 as additional seal headroom. Seal=ceil((37,730,535+4,009,702)/1,000,000)*1,000,000=ceil(41,740,237/1,000,000)*1,000,000=42,000,000 (CAP:2; G:11-14; N:18-34,85-106; /private/tmp/r1n_w1_cap_replay.json:1).
W1 spans CAP to the next chain's fresh measurement A (hours/days); W2 spans A to inventory (minutes). W1 is headroom in the seal, never charged in fresh R; W2=D(B_A) remains charged in R. The earlier 38 MB seal left only 269,465 bytes of W1 rounding slack; the separate W1 reserve fixes that defect before the next measurement (RE/codexr1n_followup.txt:3-7; G:11-14; N:85-106).
The 20% rule reserves one fifth of serialized baseline row demand for bounded changes; the 1 MB floor covers sparse/not-yet-existing roots and small evidence growth. MacPorts updates under /opt/local can add/change entries, metadata and path lengths; four other roots were absent at CAP. This is a declared engineering envelope, not an empirical growth probability. Unknown/excessive drift stops; writers remain reserved through inventory. Fresh collector additions also retain their independent 65,536-byte/64-entry bounds (CAP:2; Q:21-22,220-249; GD11:8-10,27-31).
The NEXT chain remeasures; that fresh v11 measurement alone decides chain PASS. Its D(B) is recomputed by the fixed rule, with no CLI margin overrides; capture age must be in [0,3600] seconds. CAP's --replay-cap mode requires exact pinned CAP bytes and prints replay_only=true, so its historical PASS supplies no chain/bind authority (N:42-62,138-176; T:113-125).
R = measured rows+65,536 + old Intel regular-file bytes + J-glob M3 bytes + omitted M3 bytes + both 2,500,000 dispatch envelopes + fixed overhead + D(B). PASS requires R<=42,000,000, non-receipts+R<=2,000,000,000 and LIVE<=2,500,000. LIVE=9*(2N+V+H+3*64+256)+65,536+100,000. Exact v11 equality is required (N:48-106).

## CAP replay: every charged term
All numbers below are the local replay output, not a fresh Intel observation (N:85-106; /private/tmp/r1n_w1_cap_replay.json:1).
| Term | Bytes |
|---|---:|
| Inventory rows including future-collector rows | 20,114,046 |
| Old Intel state | 7,386,341 |
| J-glob retained M3 records | 851,702 |
| Omitted retained M3 records | 8,296 |
| Fresh bind dispatch | 2,500,000 |
| Inventory dispatch | 2,500,000 |
| Registration; window; summary (each) | 65,536 |
| Failure | 16,384 |
| Emergency journal; accounting; attempt (each) | 4,096 |
| Next sizing set | 135,168 |
| Drift D(B) | 4,009,702 |
Required receipts=37,730,535; required setup=1,949,511,489; LIVE calls=223,284; LIVE bytes=2,175,092; PASS with replay_only=true. Unchanged E on CAP/J at CAP's measurement time still prints FAIL, 34,712,537 receipts and 2,016,477,107 setup (EOUT:1; T:50-67; /private/tmp/r1n_w1_green.log:6).
R12 R1 accounting: omitted CAP .json=6,978, .stderr=0, .exit=2, .final=103, .final.pending=103; EOUT .out=1,108, .exit=2, total=8,296. N finds all extant R1-prefixed receipt suffixes, including .pending; supplemental --extra-receipt enumerates any other receipt paths. Current sizing is excluded from that union and charged once by its 135,168 envelope; earlier sizing stays charged. Nonempty stderr counts. Unknown/unlisted evidence stops at Gate D; new evaluator evidence and all additional drift consume the fixed D(B), without enlarging it (N:108-146; /private/tmp/r1n_w1_cap_replay.json:1; GD11:24-28).

## Exact changed-path diff (generator output)
Only these 13 paths differ; all other JSON values, including format schema R1H-v7 and setup cap, are preserved. Filename and fresh state-root identities distinguish v11 (G:18-48; T:23-48).
| JSON path | v10 -> v11 |
|---|---|
| /budget/components/11/bytes | 70000000 -> 16384 |
| /budget/components/11/basis | ALLOWANCE -> COLLECTOR-FAILURE-BOUND |
| /budget/components/11/evidence | results/research_engine_phase1_20261011/astra_r1p_verdict.md:27 -> r1j_collector.py:701-726; intel_provisioning_manifest_v10.json:1456-1460 |
| /budget/components/12/bytes | 18000000 -> 42000000 |
| /budget/planned_peak_bytes | 1999764570 -> 1953780954 |
| /budget/margin_bytes | 235430 -> 46219046 |
| /collector/receipt_limit_bytes | 18000000 -> 42000000 |
| /paths/probe_tmp | /private/tmp/r1l-intel-provisioning-v10 -> /private/tmp/r1l-intel-provisioning-v11 |
| /collector/retained_dir | /private/tmp/r1l-intel-provisioning-v10 -> /private/tmp/r1l-intel-provisioning-v11 |
| /collector/admitted_write_roots/3 | /private/tmp/r1l-intel-provisioning-v10 -> /private/tmp/r1l-intel-provisioning-v11 |
| /collector/admitted_write_roots/4 | /private/tmp/r1l-intel-window-registration-v10 -> /private/tmp/r1l-intel-window-registration-v11 |
| /collector/child_contract/allowed_write_roots/0 | /private/tmp/r1l-intel-provisioning-v10 -> /private/tmp/r1l-intel-provisioning-v11 |
| /collector/registration_path | /private/tmp/r1l-intel-window-registration-v10/window.jsonl -> /private/tmp/r1l-intel-window-registration-v11/window.jsonl |
J11 SHA256=daf38de28b19ba61007d87730de5382a5ade54b1338a3cd0e620a395e9be5fd7; sizing identity member SHA256=933fd4e06af215f0afd6c545a1144a615fad7d0b17a991e6e0aa8783e5cbd94a (A:12,33-35; N:15,37-39).

## Existing hard-codes and in-memory compatibility
M:24 and M:256 load intel_provisioning_manifest_v10.json. A substitutes exactly those two literals in memory for BOTH build and dispatch. Q:18 hard-codes the v10 hash; A appends the v11 hash assignment to the verified Q member. Q:260's v10 filename is a standalone fallback, bypassed because S supplies VERIFIED_MEMBERS. C has no v10 filename/hash/cap constant: it checks receipt equality and peak component sum from the passed manifest (A:33-68; Q:255-269; C:323-336). C, M and Q remain unchanged (/private/tmp/r1n_w1_scope_verify.log:1).
Fresh bind/inventory must use A.load_maker(sizing=False) with normal M arguments: it retains the direct identity member and charges omitted M3 evidence. Original M CLI remains v10. A's CLI is sizing-only; no host dispatch was run here. Gate D keeps V12 R1 evidence accounting, R2 committed qualification/freshness/roots/anchor/bounds/deadline/reservations and R3 one new authorization/stop semantics (A:46-75; GD11:7-35; RE/astra_r1p12_verdict.md:21-25). Timing/blocking-I/O/remote-lifetime limits remain open (RE/astra_r1p12_verdict.md:15).

## Alternatives: report only
Summarize /opt/local instead of recording every entry: CAP's per-root Q summary serialized with Q.output_bytes is 1,182 bytes; replacing its 20,047,776 measured row bytes would save 20,046,594 receipt bytes before any other changed terms (CAP:2; Q:36-40,230-249). This proposed representation loses individual file digest/path/metadata and symlink-target evidence, weakening baseline reconstruction and changed-file attribution; aggregate counts cannot serve C's per-row purpose (C:882-915). No such inventory change is implemented.
Remove old r1h-v7 Intel state before a new chain: this could save 7,386,341 bytes, comprising 7,367,301 provisioning and 19,040 registration. It alone would still leave v10's required receipts at 27,326,196 >18,000,000. Deletion would destroy retained failure/provenance evidence and requires the operator's approval of exact Intel paths, sizes and method; no deletion is proposed for this authorized local build or performed (CAP:2; RE/r1m_chain_stop_20261011.md:13-14; Q:19-20).

## Local verification and scope
Original build: seven pre-implementation tests RED with missing-module errors; EOUT supplies the real behavioral FAIL. Follow-up: new growth controls and the tightened peak assertion ran before the seal edit; RED=3 failures/9, including the required growth PASS control actually returning FAIL under 38 MB. GREEN=9/9; the prior controls still pass (T:23-156,196-213; /private/tmp/r1n_w1_red.log:3-36; /private/tmp/r1n_w1_green.log:3-9).
W1 controls: delta=floor(4,009,702*5/6)-1,000=3,340,418 bytes PASSes with R=41,739,037; delta=4,009,703 bytes FAILs with R=42,542,179>42,000,000. Both keep LIVE fixed at 2,175,092 and use fresh synthetic CLI captures. W1 is absent from charged terms (T:158-213; /private/tmp/r1n_w1_green.log:8-9).
Original growth control adds 4,009,703 encoded row bytes (>CAP reserve), plus 12,350 rows: receipt demand 42,543,883, FAIL; LIVE still 2,397,392, isolating the receipt rejection (T:69-87; /private/tmp/r1n_w1_green.log:7). Unchanged suites: test_r1l_collector.py 64/64, test_r1m_sizing.py 10/10 (/private/tmp/r1n_w1_r1l_green.log:611-613; /private/tmp/r1n_w1_r1m_green.log:33-35).
Pinned-stub disposable-root smoke: exit 0, stdout 3,462, stderr 0, snapshots unchanged; fixture overrides only root policy/manifest pin/old scopes. Original fresh synthetic CLI smoke: PASS with 7,115-byte sizing set; oversized stderr produces FAIL (/private/tmp/r1n_w1_stub_smoke.log:1; /private/tmp/r1n_fresh_cli_smoke.log:1-2). These are local fixtures, not Intel acceptance. All 14 follow-up protected predecessor/CAP/EOUT/instruction pins remain unchanged (/private/tmp/r1n_w1_scope_verify.log:1; A:13-21).
Acceptance commands: /usr/bin/python3 -B -m unittest discover -s RE -p 'test_r1n_replan.py'; repeat with 'test_r1l_collector.py' and 'test_r1m_sizing.py'. This follow-up edits only the seven authorized R1N files; G generated replacement bytes deterministically, and the committed prior J11 hash was checked before its authorized replacement. No commits, host dispatches, SSH or model/GPU work (RE/codexr1n_followup.txt:7-11; /private/tmp/r1n_w1_scope_verify.log:1-10). GD11 preserves the successor context rule (GD11:37).
