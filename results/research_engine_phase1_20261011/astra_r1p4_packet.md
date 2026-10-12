# Astra review — R1 collector repair, round 4 (narrow)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run r1d_host_commands.sh, r1d_collector.py's entry point, or anything that fetches. The local unit tests need a writable temporary directory; in round 3 your sandbox had none, so treat MAESTRO's rerun below as reported, not reproduced. Repository HEAD is the commit that adds this packet. RE = `results/research_engine_phase1_20261011`.

Context: your round-3 verdict `RE/astra_r1p3_verdict.md` (sha256 5f26e9b2450f6295c7ca19bbe5a095ad036db0cc81e4b691cfc893bd12414b03) was NO-GO with required changes R1 (manifest lifecycle before inventory), R2 (two deadline defects), R3 (Intel toolchain identity and policy equality; acquisition stays disabled), R4 (trial approval stays conditional). The operator has since authorized the Intel build trial conditionally (Amendment 22, `results/compute_storage_brainstorm_20261011T054507Z/decisions_log.md`, last section); it is not part of this review.

MAESTRO's design decision for R1, given to the builder: the window seal hashes only a frozen policy core listed in `window_seal.core_keys`; later facts go into an add-only, hash-chained evidence ledger limited to `window_seal.evidence_slots`; the Intel interpreter identity is captured by a separate read-only probe before any window exists and bound into the core, and inventory refuses before any write while it is unbound.

Subject (drafted by Codex builder R1D; all r1c files and v3 untouched). MAESTRO42 checked on the M3: 18/18 `test_r1d_collector.py` tests and 9/9 unchanged `test_r1c_collector.py` tests pass on `/usr/bin/python3` 3.9.6; `bash -n` passes; v4 parses; the probe exits 0, prints parseable JSON and creates no file in a temporary cwd; the git scope is exactly these six new files; `hashlib.sha256(encoded(self.m))` no longer appears; the deadline check sits after the final summary and directory fsync and before success output (C:903–905, C:926); v4 keeps interpreter identity NEEDS-FETCH and `child_contract.reviewed` false.
- `RE/r1d_collector.py` (sha256 6b592281f7d4bf7ee5d0304eeb9bc3055d52b709b0cbde2fbf00fa62fa818d60)
- `RE/r1d_host_commands.sh` (sha256 f7529dfc6e82f68e801e90df327921a340965df6291af3a0a1f25d8ab21e2900)
- `RE/r1d_identity_probe.py` (sha256 89e548d40a3950accc0f9f09c28b0abb6590dc1dfa7e8b53e944d30280938881)
- `RE/test_r1d_collector.py` (sha256 c7716683ba287675bcf17f71a43a2c7e9a34ba5f250adde23d4c20e0bbaff00e): the nine carried-over r1c tests plus test_r1d_01..09, one per brief criterion.
- `RE/intel_provisioning_manifest_v4.json` (sha256 a65be19b612a4678f705a52c1dcb2fde537e1189515e618e3621cc816cb08e14)
- Builder report: `RE/r1d_report.md` (sha256 ede45916cb71ae905ca69b3863dc0540f552a0616bb61a466f49736a4e91bb49), including its proposed probe → bind → inventory sequence.

Known issue MAESTRO found: the report's bind step writes the bound identity and `core_sha256` back into `intel_provisioning_manifest_v4.json` in place. Program rule: never overwrite a manifest in place. MAESTRO's intended correction is to write the bound result to a new file (e.g. `intel_provisioning_manifest_v4_bound.json`, recording v4's sha256) and run inventory against that file. Say whether that is sufficient or what else the bind step needs.

Review for:
1. Do round-3 R1, R2 and R3 (F1–F5) now close, or are they correctly named open? Cite round-3 line → collector/test line. Could each test pass on a collector that still has the defect?
2. R1 lifecycle: can any sequence of later invocations, evidence updates, retained-directory changes or interrupted appends restart the clock, reset byte accounting, alter an earlier receipt, or change a core value? Is the core list complete for everything the window's limits depend on?
3. Is `r1d_identity_probe.py` read-only and sufficient as the Intel toolchain identity (executable bytes, version, flags, stdlib identity), and is the bind step sound once it writes a new file?
4. Is the v4 diff from v3 confined to what the repair needs, with no second source of truth or fallback path?
5. Any status mislabelled as verified, any claim not supported by its cited line.

Out of scope: the build-trial scope and Amendment 22; R2 lock completion beyond the collector; archive handoff and coexistence schedule; commissioning; the R2 clearance contract; the R4 dashboard record; Drive activation.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; a line "PROBE ALLOWED: <yes/no> run r1d_identity_probe.py on the Intel Mac (writes nothing)"; a line "INVENTORY ALLOWED AFTER BINDING: <yes/no> run r1d_host_commands.sh inventory against the bound manifest on the Intel Mac"; and "What I checked and did not check".
