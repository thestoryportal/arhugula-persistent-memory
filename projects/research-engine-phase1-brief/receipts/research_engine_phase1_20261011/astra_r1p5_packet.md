# Astra review — R1 collector repair, round 5 (narrow)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run the wrapper, the collector or binder entry points, or anything that fetches. The local unit tests need a writable temporary directory, which your sandbox has lacked; treat MAESTRO's rerun as reported, not reproduced. Repository HEAD is the commit that adds this packet. RE = `results/research_engine_phase1_20261011`.

Context: your round-4 verdict `RE/astra_r1p4_verdict.md` (sha256 97320561c71c3128a7aa09f46a2a1cff6442b35d67c6140ff1c4b1d6bda68e52) was NO-GO with R1 (missing/replaced retained state must fail closed; validate prior receipts; interrupted-append cases), R2 (complete stdlib identity), R3 (reviewed no-clobber bind), R4 (narrow claims). Under its PROBE ALLOWED line MAESTRO ran `r1d_identity_probe.py` on the Intel Mac via `ssh … '/usr/bin/python3 -I -B -' < probe` (nothing written on Intel); output `RE/intel_identity_probe_20261011T113404Z.json`, an observation only, not bound.

MAESTRO's design decisions given to the builder: R1 — a registration record outside the retained directory, at a path frozen in the core, created exclusively, fsynced, counted in clock and bytes, binding the core digest, original start, retained-directory identity and a chained list of receipt path/size/SHA-256; once it exists, no new window for that core. R3 — a dedicated binder run on the Intel Mac before any window, the only way to make a bound manifest.

Subject (drafted by Codex builder R1E; all r1c/r1d files and v3/v4 untouched). MAESTRO42 checked on the M3: `test_r1e_collector.py` 27/27 (18 carried-over + test_r1e_01..09), r1d 18/18 and r1c 9/9 unchanged, all on `/usr/bin/python3` 3.9.6; `bash -n` passes; v5 parses; the r1e probe exits 0, prints JSON and creates no file in a temporary cwd; git scope is exactly these seven new files; the registration is opened with mode 'xb' (C:488) and the bound file with O_CREAT|O_EXCL (B:67–68); the probe's os.walk has an onerror handler (P:25).
- `RE/r1e_collector.py` (sha256 3471a2f379450f0c41195a60ff3bfdcc117d282617ec555b93a7777480eb9cc2)
- `RE/r1e_identity_probe.py` (sha256 3172ef39ba74105b854735ad12113bde9df8d13c6332fe857885ce939dcad5cb)
- `RE/r1e_bind_manifest.py` (sha256 03d53b66ad5069497e51a95b9c2ec03b761ba8c837cedfcab7dd3d35be660d12)
- `RE/r1e_host_commands.sh` (sha256 40438dc9399a358668c18aa938b785256d2a4898a1519dcfc272e8202ba66418)
- `RE/test_r1e_collector.py` (sha256 fd776835f6d5d39ca1f5ff49445a8d905f05d0f186f41729006b331236de43c1)
- `RE/intel_provisioning_manifest_v5.json` (sha256 23ebba24bb9f95847bc94239585fa489c97e57c5788cc9a5f23d33b177341f67)
- Builder report: `RE/r1e_report.md` (sha256 df4b03d8255f360329a2fc03d3f867c1134b738c9b936909ec3a9bbea315518e), with its probe → bind → copy back → inventory sequence (lines ~50–66).

Questions MAESTRO found in the proposed sequence; answer each:
(a) The sequence runs from an Intel export root `/Users/robertrhu_node2/research-engine-phase1/`, which is also an admitted install root in v5. Does placing the exported repository files there corrupt the install-root baseline or the later install comparison? If so, where must the export live, and must it be an admitted root?
(b) The probe's stdout redirect to `/private/tmp/r1e-intel-identity.json` and the bound file are writes on the Intel Mac made before any window. Are they acceptable outside the window's byte/clock accounting, or must they be scoped and counted?
(c) Is copying the bound file back to the M3 by scp with the printed SHA-256 check sufficient provenance before inventory?

Review for:
1. Do round-4 R1–R4 (F1–F3, F6) now close, or are they correctly named open? Cite round-4 line → collector/probe/binder/test line. Could each new test pass on code that still has the defect?
2. R1: can any sequence (root rename, replacement, emptying, receipt edit/truncation/deletion/addition, interrupted append at any boundary, registration tampering) restart the clock, reduce accounting or alter earlier evidence without refusal, given the registration survives? Is the stated limit (no guarantee after registration loss) acceptable and correctly labelled?
3. R2: is the identity inventory now complete and fail-closed for the CLT stdlib layout seen in the observation?
4. R3: does the binder verify every input before importing code, measure the identity itself, record provenance, publish exclusively and durably, and leave v5 unchanged? Does the collector refuse unbound, edited and resealed manifests?
5. Questions (a)–(c) above.
6. Any status mislabelled as verified, any claim not supported by its cited line.

Out of scope: the build trial and Amendment 22; archive handoff/coexistence; commissioning; the R2 clearance contract; the R4 dashboard record; Drive activation.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; then these lines: "PROBE ALLOWED: <yes/no> run r1e_identity_probe.py on the Intel Mac", "BIND ALLOWED: <yes/no> run r1e_bind_manifest.py on the Intel Mac", "INVENTORY ALLOWED AFTER BINDING: <yes/no>"; and "What I checked and did not check".
