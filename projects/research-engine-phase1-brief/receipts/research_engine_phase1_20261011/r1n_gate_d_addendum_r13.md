# R1N chain: Astra round 13 conditions added to GD11 (MAESTRO50, 2026-10-11)

Verdict: `RE/astra_r1p13_verdict.md` (sha256 277a9d63…), GO-WITH-CONDITIONS; all four permission lines yes. GD11 (`RE/r1n_gate_d_checklist.md`, sha256 3732792a…) is a reviewed subject and is not edited; this file adds R1–R3 as MAESTRO's binding steps. RE = results/research_engine_phase1_20261011.

## Reviewed identities (R1 trust anchor; recheck before A, after C, and at Gate D check 1)
G 1ceee5a04b2c8ae633a6a1c972c08bc76a172063217942831a1817d66d2454fb · J11 daf38de28b19ba61007d87730de5382a5ade54b1338a3cd0e620a395e9be5fd7 · N 99e38c197d1387c6000940675ecc6c005c46e8f676423296567010fbdd4c70a5 · A 45a752a0bdc214b243d6831ecb1197e9247a48fb16e4292bd9e88daa57a8d8f3 · GD11 3732792a3d991b660cba376c2f32d0766937b6450af918d95ec24e812abd6311 · TN 0c227b4e30ad905fcb5df5f3278030747f8e8dad316ca8cddde30294df8b28d9 · RN e62858047841e4307889ca5a18cd8e31677f77adf40019a710c961ada56beff6. Predecessors as in the round-13 packet (M c014f55e…, J 748fc72a…, Q 93900742…, E a2338d7d…, C 0f711171…, B 748bcea0…, S 49b4f418…, P 83c43792…, W a4b52fc2…). Any mismatch stops the chain. A's run-time pin (A:12) is not the anchor; these recorded hashes are (V13 F5, R1).

## Before A
1. R1: `shasum -a 256` all files above; every one matches, or stop.
2. Intel read-only survey (as before the R1M chain): no scheduled writers; fresh v11 roots absent; old r1h-v7 roots present and unchanged in file list and sizes from CAP. Any other writer stops.
3. Operator authorization file committed: one A–E chain under GD11 and this addendum.

## Evidence accounting (R2; feeds Gate D checks 4–5)
Enumerate every retained receipt, inside and outside RE, including CAP, EOUT and their sidecars (8,296 bytes at CAP), the R1M evaluation records, the new sizing set and any nonstandard path. Run N with every such path as `--extra-receipt`. A's census calls `local_accounting` without those extras (V13 F4), so record N's total and A's census side by side and use the larger, without double counting. The complete new sizing set must be ≤ 135,168 bytes; all later unreserved evidence and drift come out of the fixed D(B). Unknown or excessive demand stops. No allowance changes after measurement.

## Execution (R3)
Under one new authorization: A once; B with a committed, fresh (≤ 3,600 s), non-replay PASS before C; C; Gate D with all eight GD11 checks recorded against committed evidence; E once. Reservations, freshness and the original bind deadline hold through preservation and commits. Every failure, uncertainty, expiry or stop ends the authorization; no retry, and anchor 0:a49c11de… stays consumed.
