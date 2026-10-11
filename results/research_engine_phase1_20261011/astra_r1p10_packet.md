# Astra review — R1 collector repair, round 10 (narrow)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run the wrapper, the stub, the collector, binder or bundle entry points, the tests, ssh, or anything that fetches. Treat MAESTRO's test reruns as reported, not reproduced. Repository HEAD is the commit that adds this packet.

Aliases: `RE` = `results/research_engine_phase1_20261011`; `V9` = your round-9 verdict `RE/astra_r1p9_verdict.md` (commit 73d09700), narrow NO-GO with required changes R1–R2 (V9:36–40). `C/B/S/M/W/J/P` as in round 9: `RE/r1j_collector.py / r1j_bind_manifest.py / r1j_stub.py / r1j_make_bundle.py / r1j_host_commands.sh / intel_provisioning_manifest_v9.json / r1j_identity_probe.py`. New this round: `T` = `RE/test_r1k_collector.py`, `D` = `RE/r1k_report.md`.

Scope: V9 R1 and R2 only. V9 accepted the R1 durable-before-publish narrowing (F2), the R2 source repair (F3) and preserved R3/R4 (F4). The builder was allowed to add only T and D (brief `RE/codexr1k_brief.txt`); no production file changed.

Subjects (commit a17412cd), sha256:
- T d2a9afa6a8fc9bf6233eb0cc0afb77a351013dcd0f852431a86c8d8ac8746a52 (copy of r1j's test with 61 carried tests plus the new `r1k_01`)
- D c56792315cb693da8428d3351d7ff26d48ec0e5985d3b731a51004ffab4383f3 (83 lines)
- Unchanged since round 9, MAESTRO re-hashed and all match the round-9 packet: J 43479b8d…, B 748bcea0…, C 0f711171…, W a4b52fc2…, P 83c43792…, M 39daae76…, S 49b4f418…, `RE/r1j_report.md` 3755af99…, `RE/test_r1j_collector.py` ef04bd1a….

MAESTRO47 rerun receipt (V9 R2 asks for it): `/usr/bin/python3 -B -m unittest discover -s RE -p test_<x>_collector.py` gave r1k 62 OK, r1j 61 OK, r1i 54 OK, r1h 42 OK, r1f 36 OK, r1e 27 OK, r1d 18 OK, r1c 9 OK. `git diff --name-only HEAD` showed no tracked file changed in RE; only T and D were new. These are pass counts, not correctness.

Review for:
1. Does V9 R1 close? Does `r1k_01` (T near 2010–2028, with its fixture near 1909–1968) show from observable evidence that the identity loop began before `T0 + budget` and was interrupted inside the loop, with normal loop completion not reached, while binder, loader and clocks stay real and the ample-budget positive control is retained? Could it still pass if the expiry happened before the first `identity_work()` check, or if loop tracing were removed?
2. Does V9 R2 close? Do D's R2 row and coverage table match that evidence, and does D separate the executable same-window procedure from measured completion within 870 s?
3. Did the change weaken anything V9 accepted or found preserved?

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; then exactly these two lines, each ending in yes or no:
`BIND ALLOWED: <yes|no> run the r1j wrapper's bind mode with the committed r1h probe capture`
`INVENTORY ALLOWED AFTER BINDING: <yes|no> run the r1j wrapper's inventory mode after the capture, .final and hash are committed`
and "What I checked and did not check".
