# Astra review — R1 collector repair + Intel build-trial scope, round 3 (narrow)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run r1c_host_commands.sh, r1c_collector.py or anything that fetches; you may run the local unit tests (`/usr/bin/python3 -B -m unittest discover -s results/research_engine_phase1_20261011 -p 'test_r1c_collector.py'`), which use fake roots and stubs. Repository HEAD is the commit that adds this packet. RE = `results/research_engine_phase1_20261011`.

Context: your round-2 verdict `RE/astra_r1p2_verdict.md` was NO-GO. Its R1 asked to repair the collector and re-review it narrowly before execution (F2–F6). Its R3 asked for one bounded Intel source-build trial, which needs explicit operator authorization. This round covers only those two items.

Subject (drafted by Codex builder R1C; MAESTRO41 checked: 9/9 tests pass on `/usr/bin/python3` 3.9.6, one per criterion; `bash -n` passes; v3 JSON parses; the collector contains no literal 900, 600000000, 10000000 or '1.5.5'; v2→v3 keeps the same 48 artifact IDs, changes `fetch_command` on each, retypes the three r3-* entries, changes the duckdb-lock `source_url`, and adds top-level `collector` and `preinstall` blocks):
- `RE/r1c_collector.py` (sha256 c3b9e215b8a0375d3d6af3c24fb195a7259269234f20b1cab96656ca326b714c)
- `RE/r1c_host_commands.sh` (sha256 83bde481db29d782d03db3adff1ed3d645bc5cd8afd0e029733ca3067b3ffe2b)
- `RE/test_r1c_collector.py` (sha256 5f8c3b90d6815025142dc7d3206ea99ad6648573bc1bb89b0688b300caf7a917)
- `RE/intel_provisioning_manifest_v3.json` (sha256 056835b1fbc352af5093939b18f905d0befeab49f73241e7dd9b1efde0db97ca)
- `RE/intel_build_trial_scope_v1.md` (sha256 2a4076c96528352f8d1d38f5419b01fc57616cc992fa07d37fbac4ff18868c59)
- Builder report and finding map: `RE/r1c_report.md` (sha256 ee5d7cd1ba4c0293c819cfff49130d03405a14fd086c7683f08610cd4a7dac00); its "R1C HANDOFF" names what stays open.
The builder brief's numbered criteria 1–9 are the test names test_01..test_09.

Review for:
1. Do F2, F3, F4, F5 and F6 of round 2 now close for the collector, or are they correctly named open? Cite round-2 verdict line → collector/test line. Do the tests actually exercise each criterion, or could they pass on a collector that still has the defect?
2. Is `r1c_host_commands.sh inventory` (and any other mode) safe to run on the Intel Mac as the next read-only step: writes confined to admitted roots, cumulative clock and byte admission enforced, durable failure receipts, no install/build/sync/selfupdate/cleanup path? Name any mode that must not run yet.
3. Is the v3 manifest diff confined to what the repair needs, with no new second source of truth or fallback path?
4. Trial scope: is `intel_build_trial_scope_v1.md` bounded, reversible and honest enough to put to the operator (4 GB scratch, two hours, five source ports serially, MacPorts state redirected to scratch, real prefix verified unchanged)? What must be true before it runs (e.g. the stage/image adapter and hard-cap enforcement it names as open)?
5. Any status mislabelled as verified, any claim not supported by its cited line.

Out of scope: R2 lock completion beyond the collector; R4 archive handoff and coexistence schedule (round-2 F1); R5 commissioning; R2 clearance contract; R4 dashboard record; Drive activation.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; a line "NEXT STEP ALLOWED: <yes/no> run r1c_host_commands.sh inventory on the Intel Mac"; a line "TRIAL SCOPE READY FOR OPERATOR: <yes/no>"; and "What I checked and did not check".
