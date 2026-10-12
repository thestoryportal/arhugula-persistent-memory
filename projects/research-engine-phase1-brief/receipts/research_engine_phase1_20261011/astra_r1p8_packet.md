# Astra review — R1 collector repair, round 8 (narrow)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run the wrapper, the stub, the collector, binder or bundle entry points, ssh, or anything that fetches. The local unit tests need a writable temporary directory, which your sandbox has lacked; treat MAESTRO's rerun as reported, not reproduced. Repository HEAD is the commit that adds this packet. RE = `results/research_engine_phase1_20261011`.

Context: your round-7 verdict `RE/astra_r1p7_verdict.md` (commit 4d4a99e6) was NO-GO with R1 (fail-closed terminal qualification across crashes/persistence errors; attempt-created/capture-not-reserved case), R2 (preparation/transport delay between budget calculation and Intel's baseline; conservative remote enforcement), R3 (M3 receipts reconciled with the J:1466 allowance), R4 (report citations, same-window rule, margin duplication). It allowed the probe.

The probe ran. MAESTRO45 invoked `bash RE/r1h_host_commands.sh probe RE/intel_identity_probe_r1h_20261011T131105Z` with r1h bytes equal to HEAD: exit 0, empty stderr, capture sha256 f2f6aa3b967f59be9430c8ae3ccce16b079bb6301704f166088ef36f04f28152 (commit c9c42c68). The capture reports x86_64, macOS 14.8.9, CLT Python 3.9.6, executable `/Library/Developer/CommandLineTools/usr/bin/python3`, realpath `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`, stdlib 1,637 files. Nothing was written on the Intel Mac. This is a separate observation before any bootstrap; bind has not run.

MAESTRO's design decisions given to the builder (brief committed as `RE/codexr1i_brief.txt`):
- R1: `.exit` is written once and never rewritten. A new exclusive-create `<prefix>.final` (canonical JSON: exit 0, qualified true, m3_deadline, m3_qualified_at) is the only success authority, created only after stdout, stderr and `.exit` and the directory are fsynced and an M3 reading taken after those syncs is ≤ the deadline. Bind consumption, `require_anchor()` and successor acceptance require the committed `.final`. Missing, partial or unparsable `.final` is a dead end.
- R2: the stub reads monotonic T0 first, verifies the one-line bundle, prints `R1I-READY <request sha256>`, and waits (capped by v8 `/budget/pre_go_cap_seconds` from T0) for `R1I-GO <budget>`, doing no fetch or write before GO. The M3 computes budget = deadline − now − margin when it sends GO, so Intel's end ≤ GO-send time + budget = deadline − margin regardless of preparation or transport delay. The M3 hard timeout stays.
- R3: M3 receipts (attempt records, every bind/inventory .json/.stderr/.exit/.final, failed runs included) are charged to the existing J:1466 allowance, measured from on-disk sizes; a per-dispatch bound `/budget/max_dispatch_receipt_bytes` is checked before dispatch and enforced during it.
- R4: the margin is read from sealed v8 `/budget/transit_margin_seconds`; report citations corrected; same-window rule stated.

Subject (builder R1I; commit a369d87f; every existing file untouched). MAESTRO45 checked on the M3, all on `/usr/bin/python3 -B`: `test_r1i_collector.py` 54/54 (42 carried + 12 criterion tests); r1h 42, r1f 36, r1e 27, r1d 18, r1c 9 unchanged and passing; `bash -n` passes; v8 parses; r1i probe byte-identical to r1h; no `importlib`/`exec_module` in stub, collector or binder; no `truncate(`/`seek(` in the dispatcher. One correction by MAESTRO: the builder appended its context handoff to the report after its own acceptance run, pushing the report to 97 lines and failing the carried 90-line test; MAESTRO moved that section verbatim to `RE/r1i_handoff.md`, after which 54/54 pass. The builder's handoff lists its own open risks; read it.
- `RE/r1i_collector.py` (sha256 aa2d039812fe43f22108253f26b10cb8cc0261ed47ab410bb9262c0f70f6972d)
- `RE/r1i_stub.py` (sha256 a6836d70743a4aa505817b6ac0b54df0a9a57d1efbdcd26889378ffcbcedbbb5)
- `RE/r1i_bind_manifest.py` (sha256 d1ff53a058cae5ade7731c43516eec3c144a0ecd3e58109b7084fff587c55818)
- `RE/r1i_make_bundle.py` (sha256 27f0304dfe2dbc566a87cb2066b554886b398d45dbb71144ffa2e0de98c491a9)
- `RE/r1i_host_commands.sh` (sha256 862b7732a3f5f6876e2132bd23f3669810081bc1b284d96402d46c3d0ead24ef)
- `RE/r1i_identity_probe.py` (sha256 83c4379281c8a7f0e5b99f6894cfc6824587333b8fd720930fa804d4fde625c8)
- `RE/intel_provisioning_manifest_v8.json` (sha256 dd713adaa121f8ac4f4177a2ed6a89a9aa09a987217d7c470470375fa9869ea0)
- `RE/test_r1i_collector.py` (sha256 c728e27e9f59542683cf39806ff34a2c2f545be3376206239d777a5876891540)
- `RE/r1i_report.md` (sha256 9c09659512cb2d3cd97d76b47ba3754f58664d9910f24b9deb1278646e44214e); `RE/r1i_handoff.md` (sha256 e045e49d616e24841d5f4a7d30f626d7f88e4f1db11a181be1d928e192f28e4f)

Review for:
1. Do round-7 R1–R4 (F1–F3, F5, F6) now close, or are they correctly named open? Cite round-7 line → source/test line. Could each new test pass on code that still has the defect?
2. R1: replay your F1 sequence (SSH succeeds; zero status persisted; crash or persistence error before final qualification), plus the attempt-created/capture-not-reserved crash. Can any path leave something that bind consumption, `require_anchor()` or successor acceptance treats as success?
3. R2: with a preparation or transport delay of any length before Intel T0, or between READY and GO, can Intel run past deadline − margin? Is the READY/GO framing robust to stdin EOF, a malformed GO, and disconnection after GO?
4. R3: are all M3 receipts charged against J:1466 from the files themselves, with failed runs retained and charged, and is the committed-capture gate unchanged?
5. Does the probe capture above satisfy the direct-runtime observation the earlier rounds required, as an observation only, with strict binding equality still to be checked at bind?
6. Any status mislabelled as verified, any claim not supported by its cited line.

Out of scope: the build trial and Amendment 22; archive handoff/coexistence; commissioning; the R2 clearance contract; the R4 dashboard record; Drive activation.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; then these lines: "BIND ALLOWED: <yes/no> run the r1i wrapper's bind mode with the committed r1h probe capture", "INVENTORY ALLOWED AFTER BINDING: <yes/no> run the r1i wrapper's inventory mode after the capture, .final and hash are committed"; and "What I checked and did not check".
