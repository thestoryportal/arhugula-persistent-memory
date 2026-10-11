# Astra review — R1 Intel inventory budget re-plan v11, round 13

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run the probe, either evaluator, the adapter, the generator, the stub, the collector, binder or bundle entry points, the tests, ssh, or anything that fetches. Treat MAESTRO's test reruns as reported, not reproduced. Repository HEAD is the commit that adds this packet.

Aliases: `RE` = `results/research_engine_phase1_20261011`. `V12` = your round-12 verdict `RE/astra_r1p12_verdict.md` (898860a6, sha256 978b5bcf…): GO-WITH-CONDITIONS, one operator authorization for an A–E chain under R1–R3. As in round 12: `C/B/S/W/P/M/J/T` = `RE/r1j_collector.py / r1j_bind_manifest.py / r1j_stub.py / r1j_host_commands.sh / r1j_identity_probe.py / r1l_make_bundle.py / intel_provisioning_manifest_v10.json / test_r1l_collector.py`; `Q/E/TM/RM` = `RE/r1m_size_probe.py / r1m_evaluate.py / test_r1m_sizing.py / r1m_report.md`. New this round (builder codexr1n; brief `RE/codexr1n_brief.txt`, follow-up `RE/codexr1n_followup.txt`): `G` = `RE/r1n_make_manifest_v11.py`, `J11` = `RE/intel_provisioning_manifest_v11.json`, `N` = `RE/r1n_evaluate.py`, `A` = `RE/r1n_sizing_dispatch.py`, `GD11` = `RE/r1n_gate_d_checklist.md`, `TN` = `RE/test_r1n_replan.py`, `RN` = `RE/r1n_report.md`. RN cites raw builder logs at /private/tmp paths; they are not committed. Treat them as builder claims.

## What happened since round 12
The operator authorized one A–E chain under V12. Phase A dispatched Q once to the Intel Mac: rc 0, qualified final, empty stderr; capture `CAP` = `RE/r1j_probe_r1m_20261011T154940Z.json` (sha256 1c330b25…). Phase B ran E on CAP with J and printed FAIL (`RE/r1m_evaluate_20261011T154940Z.out`, sha256 e6be26ff…): required receipts 34,712,537 > 18,000,000; required setup 2,016,477,107 > 2,000,000,000; LIVE 2,175,092 ≤ 2,500,000. The chain stopped as designed: no bind, no Intel state created, no anchor used; the authorization is spent (`RE/r1m_chain_stop_20261011.md`, sha256 cc5853fd…). 61,743 rows, nearly all under /opt/local (20,114,046 row bytes). Anchor 0:a49c11de… stays consumed.

## Subjects (commit 789bd306), sha256 and lines
- G 1ceee5a04b2c8ae633a6a1c972c08bc76a172063217942831a1817d66d2454fb (66)
- J11 daf38de28b19ba61007d87730de5382a5ade54b1338a3cd0e620a395e9be5fd7 (3139)
- N 99e38c197d1387c6000940675ecc6c005c46e8f676423296567010fbdd4c70a5 (172)
- A 45a752a0bdc214b243d6831ecb1197e9247a48fb16e4292bd9e88daa57a8d8f3 (82)
- GD11 3732792a3d991b660cba376c2f32d0766937b6450af918d95ec24e812abd6311 (37)
- TN 0c227b4e30ad905fcb5df5f3278030747f8e8dad316ca8cddde30294df8b28d9 (217)
- RN e62858047841e4307889ca5a18cd8e31677f77adf40019a710c961ada56beff6 (66)
- Unchanged since round 12 (MAESTRO50 re-hashed; all match the round-12 packet): M c014f55e…, J 748fc72a…, Q 93900742…, E a2338d7d…, C 0f711171…, B 748bcea0…, S 49b4f418…, P 83c43792…, W a4b52fc2…, T 6b7060ae…, TM 0343190a….

## MAESTRO50 receipts
`/usr/bin/python3 -B -m unittest discover -s RE -p test_r1n_replan.py` ran 9, OK; `test_r1m_sizing.py` ran 10, OK; `test_r1l_collector.py` ran 64, OK. Only the seven new files changed in RE; no tracked predecessor changed. These are pass counts, not correctness.

MAESTRO50 found one defect in the first build and had it fixed before this review: the first seal (38,000,000) was CAP's demand including D(B), rounded up, so only 269,465 bytes covered drift between CAP and the next measurement (D(B) is charged at that measurement). The fix adds W1 = D(B_CAP) = 4,009,702 as seal headroom, not charged in the fresh R; the seal becomes 42,000,000 (RN:10–11,63; TN W1 PASS/FAIL controls).

## Review for
1. `retained_failure_extra` 70,000,000 → 16,384 (RN "Budget and source justification"; J:1378–1460,1473–1477; C:701–726,854–855,969–985). Does the source show the retained payload, build image and extraction remain charged to other components, and that the failure path writes at most one padded 16,384-byte record and no second full payload? Is anything that reserve covered now uncharged?
2. Sizing from CAP. The seal was sized after seeing CAP. Is the rule now fixed before the next measurement and free of post-measurement tuning: D(B) = max(1,000,000, ceil(B/5)) charged in R at the fresh measurement (W2), W1 = D(B_CAP) as seal headroom (W1), rounding up to the next 1,000,000, no CLI margin, capture age in [0, 3600] s (N; RN)? Is a 20% row envelope plus a 1 MB floor a defensible declared envelope for /opt/local (MacPorts) and the four not-yet-existing roots? Does `--replay-cap` (CAP replay) confer any chain or bind authority?
3. V12 R1 evidence accounting: N's charging of the omitted M3 evidence (CAP and EOUT side files, 8,296 bytes), `--extra-receipt`, and the next sizing set inside its fixed 135,168-byte envelope; unknown or excessive evidence stops at Gate D.
4. Adapter A: in-memory substitution of M's two literal v10 manifest loads (M:24,256) and Q's v10 hash (Q:18); probe-only CLI; fresh bind via `load_maker(sizing=False)`. A derives the v11 pin at run time from G's output (A:12) and does not list G in its own pin table (A:14–21); GD11:6,24 require MAESTRO to record all seven files' full hashes and Gate D to re-check them. Is that chain sufficient, or must A pin J11 (or G) by literal hash?
5. GD11: does it keep V12 R1–R3 (complete sizing-set accounting, committed qualification/freshness/roots/anchor/bounds/deadline/reservations, one authorization that ends on any stop)?
6. The alternatives in RN (summarize /opt/local; delete old r1h-v7 Intel state) are reported, not implemented. Note any reason one should be preferred.

## Verdict format
First line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; then exactly these four lines, each ending in yes or no:
`SIZING PROBE ALLOWED: <yes|no> dispatch Q once through adapter A (phase A of a new chain), after a new operator authorization`
`RERUN BIND ALLOWED AFTER SIZING PASS: <yes|no> run the v11 bind (phase C) only after N prints PASS on the committed fresh sizing capture`
`RERUN INVENTORY ALLOWED AFTER GATE D: <yes|no> run the v11 inventory (phase E) after MAESTRO's gate D (GD11) passes`
`ONE AUTHORIZATION FOR A–E: <yes|no>`
and "What I checked and did not check".
