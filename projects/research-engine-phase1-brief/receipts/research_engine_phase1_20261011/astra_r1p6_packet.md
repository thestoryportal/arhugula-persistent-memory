# Astra review — R1 collector repair, round 6 (narrow)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run the wrapper, the stub, the collector, binder or bundle entry points, or anything that fetches. The local unit tests need a writable temporary directory, which your sandbox has lacked; treat MAESTRO's rerun as reported, not reproduced. Repository HEAD is the commit that adds this packet. RE = `results/research_engine_phase1_20261011`.

Context: your round-5 verdict `RE/astra_r1p5_verdict.md` (sha256 71c9a94104fda7581178cf91b12044e998057eb186f8a6e04bf7704afd416f02) was NO-GO with R1 (trusted registration against rollback/rewrite), R2 (complete initial publication bound to an independent digest), R3 (execute verified bytes, no cache or reread race), R4 (separate control location, bootstrap write/time accounting per v5 J:1513, copy-back provenance), R5 (capture the corrected probe; launcher/runtime relationship; narrow claims). Under its PROBE ALLOWED line MAESTRO ran `r1e_identity_probe.py` on the Intel Mac via ssh stdin to `/usr/bin/python3 -I -B -` after verifying its sha256 (nothing written on Intel): `RE/intel_identity_probe_r1e_20261011T115851Z.json` (sha256 f2f6aa3b967f59be9430c8ae3ccce16b079bb6301704f166088ef36f04f28152), an observation only. It reports executable `/Library/Developer/CommandLineTools/usr/bin/python3` and realpath `.../Python3.framework/Versions/3.9/bin/python3.9`.

MAESTRO's design decisions given to the builder:
- R1: the trust anchor lives off the Intel Mac. The collector prints `R1F-ANCHOR <core> <seq> <head>` after every registration append; MAESTRO commits the last one to git; every run takes `--expected-anchor` (`none` only when no registration exists) and refuses before any write on mismatch. The full registration and every receipt are re-verified before success.
- R2: the collector takes `--expected-capture-sha256` (the git-committed hash of the complete binder capture) and takes the bound manifest only from those verified bytes; core and seal checks remain a second layer.
- R3: no Python source is imported or read from disk on the Intel Mac. A fixed stub, passed as `-c` text, reads one stdin bundle and verifies every member against hashes in its argv before compiling anything, then runs each from memory.
- R4: binding writes nothing on the Intel Mac, so there is no Intel export or control directory. The binder prints the bound manifest and a binding receipt to stdout, captured on the M3. Binding is a bootstrap phase: its M3 start time becomes the window's clock start and its M3 capture bytes are counted, so bind and inventory run back to back.
- R5: v6 invokes `/Library/Developer/CommandLineTools/usr/bin/python3 -I -B` directly; strict realpath equality between the invoked path and the runtime stays; `/usr/bin/python3` leaves the trust path.

Subject (drafted by Codex builders R1F and R1G; committed 73b7ebeb plus the report update; all r1c/r1d/r1e files and v3/v4/v5 untouched). MAESTRO43 checked on the M3: `test_r1f_collector.py` 36/36 (27 carried over + test_r1f_01..09); r1e 27/27, r1d 18/18, r1c 9/9 unchanged, all on `/usr/bin/python3` 3.9.6; `bash -n` passes; v6 parses; all five r1f .py files compile; the r1f probe prints JSON and creates no file in a temporary cwd; git scope is exactly nine new files; no `importlib`, `exec_module` or `__import__` in any r1f source; no `open()` or write call in the binder; every Python path in the wrapper, bundle maker and v6 is the CLT runtime.
- `RE/r1f_collector.py` (sha256 a3657912827120b626f94f0a2f0dbf7642a5f709b4a0a36bd5db851ac9440be9)
- `RE/r1f_identity_probe.py` (sha256 83c4379281c8a7f0e5b99f6894cfc6824587333b8fd720930fa804d4fde625c8)
- `RE/r1f_bind_manifest.py` (sha256 949ede37ce3d4cc1b2850c44f879501bf660d08b574066ac31aa303de39d1e66)
- `RE/r1f_stub.py` (sha256 03b4aecb63ff6f7586a9565d2d5470e3c934c384a001db811301a9ab7e0dc1b9)
- `RE/r1f_make_bundle.py` (sha256 48e47a2b41565c4c1326e45d5506f3cb8bef62958bf40b32fa76a2c2c1ccaf3c)
- `RE/r1f_host_commands.sh` (sha256 bd44f9a95d5b15804a3afcdd6894035c33a40f2a3387755375eb9a70960b4b58)
- `RE/test_r1f_collector.py` (sha256 ac5e13731cf8df675b186e5eb14dcfed1c6acf5ee37a355c865edb8565c3afb5)
- `RE/intel_provisioning_manifest_v6.json` (sha256 fbbcba6ce2b4cb8bb66624a68882a1c66a032bd2570dc9c471dbf387bf43541f)
- Builder report: `RE/r1f_report.md` (sha256 d1f78ba47a94633ad8522d32a7fbc72912f384bce71431c85ea621d3a1ed554c), with the probe → bind → inventory sequence and the builder's two questions.

Questions; answer each:
(a) Does the carried-forward bootstrap (M3 start time as the window's clock start; M3 capture, stderr and exit-status bytes counted against the receipts allowance) satisfy the clock rule (v5 J:1513 = v6 J:1515) and the receipts allowance (v5 J:1461–1464), given that v6's `time_total_s` is 870 s and bind and inventory must therefore run back to back?
(b) Is a git-committed anchor (sequence number and chain head, captured from the collector's stdout over ssh) an acceptable independent authority against registration rollback and rewrite? If the last anchor line is lost in transit, the next run refuses; is that fail-closed state acceptable?
(c) Does invoking the CLT runtime directly, with strict realpath equality, resolve your round-5 F5 launcher concern, pending a probe captured that way?

Review for:
1. Do round-5 R1–R5 (F1–F6) now close, or are they correctly named open? Cite round-5 line → source/test line. Could each new test pass on code that still has the defect?
2. R1: can any sequence (valid-prefix rollback, coordinated rewrite of start record/window.json/chain, same-inode emptying, mutation during the active invocation, interrupted write at any listed boundary) restart the clock, reduce accounting or alter evidence without refusal, given the anchor is intact?
3. R2: are non-core evidence edits, timestamp edits and manufactured consistent provenance refused against the committed capture hash? Does later evidence enter only through the ledger?
4. R3: does the stub verify every member before any compile, and do the collector and binder run only verified bytes with no cache or disk reread? Do the tests exercise the real stub subprocess?
5. R4/R5: does binding write nothing on the Intel Mac; is the copy-back provenance (argv, host, exit status, input hashes, raw probe, bound digest) complete; is the launcher handled without weakening equality?
6. Questions (a)–(c) above.
7. Any status mislabelled as verified, any claim not supported by its cited line.

Out of scope: the build trial and Amendment 22; archive handoff/coexistence; commissioning; the R2 clearance contract; the R4 dashboard record; Drive activation.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; then these lines: "PROBE ALLOWED: <yes/no> run r1f_identity_probe.py on the Intel Mac via the r1f wrapper's probe mode", "BIND ALLOWED: <yes/no> run the r1f wrapper's bind mode", "INVENTORY ALLOWED AFTER BINDING: <yes/no> run the r1f wrapper's inventory mode immediately after binding"; and "What I checked and did not check".
