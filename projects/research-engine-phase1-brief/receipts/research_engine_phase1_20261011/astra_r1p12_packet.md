# Astra review — R1 Intel sizing build, round 12 (narrow)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run the probe, the evaluator, the wrapper, the stub, the collector, binder or bundle entry points, the tests, ssh, or anything that fetches. Treat MAESTRO's test reruns as reported, not reproduced. Repository HEAD is the commit that adds this packet.

Aliases: `RE` = `results/research_engine_phase1_20261011`; `V11` = your round-11 verdict `RE/astra_r1p11_verdict.md` (b43f2073): GO-WITH-CONDITIONS, RERUN BIND yes after a new operator authorization, RERUN INVENTORY no until R1 (read-only sizing of the complete admitted Intel roots), R2 (retained Intel state reconciled with the cumulative budget) and R3 (D:13 qualified, procedure split at the inventory gate). `C/B/S/W/P/M/J/T/D` as in round 11: `RE/r1j_collector.py / r1j_bind_manifest.py / r1j_stub.py / r1j_host_commands.sh / r1j_identity_probe.py / r1l_make_bundle.py / intel_provisioning_manifest_v10.json / test_r1l_collector.py / r1l_report.md`. New this round (builder codexr1m, brief `RE/codexr1m_brief.txt`): `Q` = `RE/r1m_size_probe.py`, `E` = `RE/r1m_evaluate.py`, `TM` = `RE/test_r1m_sizing.py`, `RM` = `RE/r1m_report.md`. RM cites raw builder logs at /private/tmp paths; they are not committed. Treat them as builder claims.

Nothing ran on the Intel Mac since round 11. Anchor 0:a49c11de… stays consumed and is never retried.

Subjects (commit 0b135cbd), sha256:
- Q 93900742211b38cf6cf136eec5752b8f4958dc7782982c2999045ffac18ba029 (281 lines)
- E a2338d7dec2ea03bac96edc4aa71b9864c6403a8b03b4cf2d8a5a5615c32faac (133 lines)
- TM 0343190a27e664bfe8f3a4960919320990e18f11c952fb33dedd0d35f79c1627 (285 lines)
- RM 0a382d662b4e5f1e060b77ad7dff75f0a59c16c917b15790ccd1ad37b01b823d (70 lines)
- Unchanged since round 11 (MAESTRO49 re-hashed; all match the round-11 packet): M c014f55e…, J 748fc72a…, T 6b7060ae…, D 12cf5ab8…, C 0f711171…, B 748bcea0…, S 49b4f418…, W a4b52fc2…, P 83c43792…. Q pins C and J by these hashes (Q:17–18).

MAESTRO49 receipts: `/usr/bin/python3 -B -m unittest discover -s RE -p test_r1m_sizing.py` ran 10 tests, OK; `test_r1l_collector.py` ran 64, OK. `git status` showed only Q, E, TM and RM new in RE and no tracked RE file changed. Static check: Q's only `os.open` flags are `O_RDONLY|O_DIRECTORY|O_NOFOLLOW` (Q:24) and `O_RDONLY|O_NOFOLLOW|O_NONBLOCK` (Q:120); its only writes are stdout/stderr (Q:278,280); stdlib imports only; rows are sized with C's own `encoded()` (Q:60–74). These are pass counts and a grep, not correctness.

Budget rule chosen by the builder (RM R2; E:57–73): every measured old Intel regular-file byte is charged inside the same 18,000,000-byte receipt allowance, with no exclusion; R = O + I + L + 6,360,448 must be ≤ 18,000,000 and 1,981,764,570 + R ≤ 2,000,000,000. Constants were fixed before any measurement and have no override flags.

Proposed authorization unit (MAESTRO): if you allow it, MAESTRO asks the operator ONE question authorizing phases A–E of RM:43–62 as a single chain, with every stop rule kept: A sizing probe once; B local evaluator, FAIL stops; C fresh v10 bind; D MAESTRO gate, any doubt stops; E inventory once. A stop anywhere ends the authorization; a new attempt needs a new one.

Review for:
1. R1: is Q read-only and complete for J's five admitted roots and the two old-state scopes (no writes, no state roots, no collector construction, symlink refusal)? Does its serialized-row bound use C's real encoding with fixed-width hash placeholders, and do the 131,072-byte summary cap and the 128-file old-state refusal fail closed instead of truncating to PASS?
2. R2: is charging all old Intel bytes inside the one 18 MB allowance a correct reading of J:1456–1467 and C:357–366,765–807? Are E's fixed envelopes complete (registration, window, summary, failure, emergency, accounting, attempt, capture, drift) and conservative, and is LIVE dispatch bounded separately against its 2,500,000-byte limit? Is anything in E tunable after measurement?
3. R3: are D:13's equations correctly qualified (2N+V+H, RM:39), and does the A–E split put a real stop between bind and inventory?
4. The sizing dispatch (RM:40–57): M's probe transport with Q substituted only for the identity member, in memory, probe-only. Does it weaken any guarantee V10/V11 accepted (identity pinning, durable-pending → cutoff → exclusive final link, binding tracing, OBSERVATION-ONLY outputs)? Is its own window and evidence treatment (sizing evidence, not identity or bind authority) sound?
5. Is one operator authorization for the A–E chain acceptable, or should inventory (E) need its own?

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; then exactly these four lines, each ending in yes or no:
`SIZING PROBE ALLOWED: <yes|no> dispatch Q once through the RM adapter (phase A), after a new operator authorization`
`RERUN BIND ALLOWED AFTER SIZING PASS: <yes|no> run M's v10 bind (phase C) only after E prints PASS on the committed sizing capture`
`RERUN INVENTORY ALLOWED AFTER GATE D: <yes|no> run the v10 inventory (phase E) after MAESTRO's gate D passes`
`ONE AUTHORIZATION FOR A–E: <yes|no>`
and "What I checked and did not check".
