# R1N v11 prospective A–E chain and Gate D

RE=results/research_engine_phase1_20261011. N=RE/r1n_evaluate.py; A=RE/r1n_sizing_dispatch.py; J11=RE/intel_provisioning_manifest_v11.json. This checklist carries Astra r12 R1–R3 forward; it grants no execution authority (RE/astra_r1p12_verdict.md:21-25; RE/r1m_chain_stop_20261011.md:8).

## Before A: review and new authorization (R3)
- Astra must review v11 and its in-memory adapters. MAESTRO commits the reviewed seven new files and records their full hashes and A.PINS. The generator's fixed inputs determine the v11 raw-byte pin (A:12-21; RE/r1n_make_manifest_v11.py:8-12).
- Obtain a NEW operator authorization expressly covering exactly one conditional A–E chain and every gate below. The earlier authorization is spent. Any failure, uncertainty, expiry or stop ends this chain; another attempt requires another authorization. Never reuse anchor `0:a49c11de49ce…` (RE/r1m_chain_stop_20261011.md:8; RE/astra_r1p12_verdict.md:25).
- Reserve every writer of all five J11 admitted roots AND both Q.OLD_ROOTS through inventory. Record the operator at the Intel console and scheduled/MacPorts writers; unknown participation stops. Verify the v11 retained/registration roots are absent (J11:1620-1626,1728; RE/r1m_size_probe.py:19-20; RE/astra_r1p12_verdict.md:23).
- Enumerate the complete retained M3 receipt evidence. N automatically finds J's globs plus R1-prefixed .json/.out/.stderr/.exit/.final/.pending records; pass every other receipt path with --extra-receipt, and reconcile that same list with A's M3 accounting before dispatch. Unknown evidence stops (N:107-134; A:62-65).

## A: once, then preserve and commit
After the above gates only, use A with a new RE/r1j_probe_r1n_<stamp> prefix. Its CLI is probe-only. It verifies v11 and predecessor pins, substitutes both M manifest-loading literals in memory, and appends the v11 manifest pin to Q's verified identity member. It constructs no Intel state itself (A:27-59,71-75; RE/r1m_size_probe.py:251-273).
Preserve and commit capture .json, .stderr, .exit, .final.pending and .final, plus any other surviving sidecars and their hashes, on every outcome. Require qualified exit zero before B. M3 preservation/publication and timing rules remain those of M; blocking I/O and remote lifetime remain open limitations (RE/r1l_make_bundle.py:299-364; RE/astra_r1p12_verdict.md:15).

## B: fresh v11 measurement only
Run N with the committed capture and J11, adding the explicitly enumerated extra receipt paths. Never use --replay-cap in a chain. N requires the v11 member pins, stable root totals, qualified sizing final, complete sizing set <=135,168 bytes, and measurement age in [0,3600] seconds. Preserve/commit evaluator output, stderr, exit, and any pending/final records and hashes. FAIL stops before binding (N:42-84,107-134,137-175).
The current sizing set is charged once by its fixed envelope; all earlier sizing sets, including R1M, are measured retained M3 evidence. No constants, manifests or envelope interpretations may change after A (N:85-105,120-134; RE/astra_r1p12_verdict.md:21).

## C: fresh bind
MAESTRO must use A.load_maker(sizing=False) with M's normal bind arguments and real direct identity probe. Calling the original M CLI would load v10. This adapter retains the normal identity member, substitutes v11 in both build and dispatch, and includes omitted M3 records in receipt admission. Q's sizing result is never identity/binding authority (A:38-68; RE/r1l_make_bundle.py:21-29,256-270; RE/astra_r1p12_verdict.md:15).
Preserve and commit the fresh bind capture, stderr, exit, pending/final, bootstrap and complete hash before use. Verify qualification against the original bind deadline (RE/r1l_make_bundle.py:138-160,281-289).

## Gate D: MAESTRO records each check against committed evidence (R1, R2)
1. All reviewed source, generator, v11, adapter/member, evaluator and test hashes still match. Compare N's capture_sha256 and A's member hash with the committed sizing set (A:12-34; N:166-171).
2. Fresh sizing is qualified, matches v11, is not future-dated, and remains <=3,600 s old NOW. Historical CAP/replay_only PASS is inadmissible (N:42-62,151-171).
3. The COMPLETE sizing set, including stderr, exit and BOTH pending/final retained paths and any additional sidecars, is <=135,168 bytes. Unknown members or excessive demand stop. N already checks the total at B; repeat against committed bytes (N:120-134; RE/astra_r1p12_verdict.md:21).
4. Record N.evidence.matched_files and omitted_files and reconcile them with the complete evidence inventory, including CAP, EOUT, all their sidecars, current evaluator records and nonstandard/outside-RE receipts. Baseline omitted bytes are already charged separately by N. All additional uncharged evidence since B plus all other observed receipt/row/old-state drift must fit N.terms.drift_receipt_bytes = max(1,000,000,ceil(A's measured row bytes/5)). The allowance remains 38,000,000; any unknown or excess stops (N:19-34,85-105,107-145; RE/astra_r1p12_verdict.md:21).
5. Record an updated total demand including that additional evidence/drift, and require cumulative receipts <=38,000,000 and non-receipts + cumulative receipts <=2,000,000,000. No double credit for the reserved future sizing/bind/inventory envelopes (N:85-105).
6. Verify fresh retained and registration roots, core and anchor are unused; no state/anchor from attempt 0 is reused. Bind core must seal J11 and the fresh direct identity capture (J11:1620-1626,1728; RE/astra_r1p12_verdict.md:23-25).
7. Future collector additions remain <=65,536 encoded bytes and <=64 entries. Registration/window/summary each <=65,536, failure <=16,384, emergency/accounting/attempt each <=4,096. No evidence update. Hold receipt drift above AND LIVE drift <=100,000 bytes; LIVE calls remain 2N+V+H+3*64+256, with 65,536 non-progress bytes and total <=2,500,000 (N:23-29,85-103; RE/astra_r1p12_verdict.md:13).
8. Record sufficient time remaining in the bind's ORIGINAL 870-second window for inventory, receipt preservation and commits. Reservations still hold for the measured baseline AND old-state scopes. Unknown timing or writer control stops (RE/astra_r1p12_verdict.md:23; RE/r1m_report.md:61).
Only all eight passing checks permit a recorded GATE D GO. Numerical PASS alone is insufficient (RE/astra_r1p12_verdict.md:23).

## E: once under the same authorization
Use A.load_maker(sizing=False) with M's normal inventory arguments, fresh committed bind/hash/bootstrap and anchor `none` for the fresh core. Preserve and commit the attempt and every outcome within the original deadline. No retry, deletion or reuse of old state (A:38-68; RE/r1l_make_bundle.py:272-318; RE/r1m_report.md:62).

Context rule for every executor/successor: start a new step only at >=60% context left. At <=45%, any compaction or MAESTRO context stop, finish only the current edit, save, write RE/r1n_handoff.md with done/remaining/exact paths/next single step/open risks and this same rule, and reply R1N HANDOFF.
