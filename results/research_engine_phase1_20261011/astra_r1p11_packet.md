# Astra review — R1 inventory halt repair, round 11 (narrow)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run the wrapper, the stub, the collector, binder or bundle entry points, the tests, ssh, or anything that fetches. Treat MAESTRO's test reruns as reported, not reproduced. Repository HEAD is the commit that adds this packet.

Aliases: `RE` = `results/research_engine_phase1_20261011`; `V10` = your round-10 verdict `RE/astra_r1p10_verdict.md` (commit 6931d0c0), GO with BIND and INVENTORY ALLOWED. `C/B/S/W/P` as before: `RE/r1j_collector.py / r1j_bind_manifest.py / r1j_stub.py / r1j_host_commands.sh / r1j_identity_probe.py`; `M9` = `RE/r1j_make_bundle.py`, `J9` = `RE/intel_provisioning_manifest_v9.json`. `X` = `RE/r1j_inventory_0_a49c11de49ce.json` (+ `.stderr`, `.exit`), `H` = `RE/r1j_inventory_halt_diagnostic_20261011.json`. New this round: `M` = `RE/r1l_make_bundle.py`, `J` = `RE/intel_provisioning_manifest_v10.json`, `T` = `RE/test_r1l_collector.py`, `D` = `RE/r1l_report.md`, `HF` = `RE/r1l_handoff.md`, logs `RE/r1l_logs_20261011/` (raw builder logs; D cites them at their original /private/tmp paths).

What happened after V10: the operator authorized one attempt. On 2026-10-11 14:32:08–14:32:26Z the bind succeeded (qualified .final committed a806d691); inventory attempt 0 was REFUSED on Intel with `REFUSED: Cumulative receipt limit exceeded` (X.stderr:1, exit 1; evidence 08ad0ada; H at cd5ea2e3). Anchor 0:a49c11de… is consumed and is never retried. The builder (brief `RE/codexr1l_brief.txt`) was allowed one test-first fix in new r1l files (plus manifest v10 only if a sealed value must change). It replied `R1L BLOCKED`: the fix is done, but the exact Intel overshoot cannot be derived from X.

MAESTRO ruling (D-R1L-delta, open to your challenge): the exact historical overshoot is unrecoverable. The refusal logs no usage or amount, and H records only the limit. The root cause is accepted on (a) the source mechanism in D:4–9, (b) the exact local reproduction (D:18, 319 bytes over, terms summing to usage), and (c) the Intel bound (≤ 7,370,024 bytes left for the inventory, D:6–7; the 7,370,024 figure is D:7).

Subjects (commit 508123a8), sha256:
- M c014f55e69ff9dd2483ebd92fc82d36cd760f9b6d11248f1d405dfc660b2d694
- J 748fc72aa49bcdb963d99b89bbc29859237d1bbd32b84b8e05fd38d07bd9df3f
- T 6b7060ae2ed26dd60b8f93e8b4e2b9a7a5eb88260d0e0ca00b3b575f10a3c678
- D 12cf5ab8f7e23a547a5d988d14406decf752c9cfc97aedb71a98002784ffd9c2 (57 lines)
- HF 409f873db8d1cec0c15646f5811ae766cb283a7268e3e5095fbc4e17a8636505
- Evidence: X 8b15bd38…, H 12958d4b…
- Unchanged since round 10 (MAESTRO re-hashed, all match the round-10 packet): J9 43479b8d…, B 748bcea0…, C 0f711171…, W a4b52fc2…, P 83c43792…, M9 39daae76…, S 49b4f418…, `RE/test_r1k_collector.py` d2a9afa6….

MAESTRO48 receipts: `/usr/bin/python3 -B -m unittest discover -s RE -p test_<x>_collector.py` gave r1l 64 OK, r1k 62, r1j 61, r1i 54, r1h 42, r1f 36, r1e 27, r1d 18, r1c 9, all OK. `git status` showed no tracked file changed in RE. A leaf-by-leaf JSON diff J9→J shows exactly 10 changed leaves: `budget/components/12/bytes` and `collector/receipt_limit_bytes` 10,000,000 → 18,000,000; `budget/margin_bytes` 8,235,430 → 235,430; `budget/planned_peak_bytes` 1,991,764,570 → 1,999,764,570; six r1h-v7 → r1l-v10 state paths. M differs from M9 only by renames. These are pass counts and diffs, not correctness.

Review for:
1. Root cause: does D's arithmetic (D:4–13) trace the refusal to cumulative `writing_bytes` under the 10 MB allowance, and correctly rule out the 81,599 LIVE stdout lines as the charged bytes? Is D-R1L-delta acceptable, or does closing the halt need evidence that does not exist?
2. Fix: is raising the sealed allowance to 18 MB (D:14) one fix, inside the unchanged 2 GB setup cap, with accounting and admission logic unchanged? Does T show it failing first and passing after, through the real stub and collector?
3. Sizing risk: 18 MB is proven only for T's 32,000-file fixture (13,730,405 inventory bytes, D:16), not the real Intel tree. Using X's counts (3N+D=81,577 or 81,575, D:13) and the ≤ 7,370,024 byte bound, is 18 MB likely enough for the real inventory? If you cannot tell, what read-only evidence would settle it before a rerun? A second halt consumes another authorization.
4. Rerun procedure (D:22–57): fresh v10 bind, core and window; commit bind before inventory; no reuse of anchor 0:a49c11de…; old receipts still counted (D:23). Is it correct and complete?
5. Did the change weaken anything V10 accepted (durable-pending → cutoff → exclusive final link, binding tracing, strict identity equality, OBSERVATION-ONLY outputs)?

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; then exactly these two lines, each ending in yes or no:
`RERUN BIND ALLOWED: <yes|no> run M's v10 bind per D's procedure with a fresh window, after a new operator authorization`
`RERUN INVENTORY ALLOWED AFTER BINDING: <yes|no> run the v10 inventory mode after the fresh capture, .final and hash are committed`
and "What I checked and did not check".
