# Astra review — R1 collector repair, round 9 (narrow)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run the wrapper, the stub, the collector, binder or bundle entry points, ssh, or anything that fetches. Treat MAESTRO's test reruns as reported, not reproduced. Repository HEAD is the commit that adds this packet.

Aliases: `RE` = `results/research_engine_phase1_20261011`; `V8` = your round-8 verdict `RE/astra_r1p8_verdict.md` (commit 7f64cc1b), NO-GO with required changes R1–R4 (V8 lines near the end). `C/B/S/M/W/T` = `RE/r1j_collector.py / r1j_bind_manifest.py / r1j_stub.py / r1j_make_bundle.py / r1j_host_commands.sh / test_r1j_collector.py`; `J` = `RE/intel_provisioning_manifest_v9.json`; `D` = `RE/r1j_report.md`.

Subjects (commit 9a8f51bb), sha256:
- J 43479b8d6a3c43b9f953027e3bb6aa3bb9205709901b59ab39c1778c7a21befe
- B 748bcea0c247fb3d80ccbf572641e931cbd2794600f9e1f699cc79e427f34a83
- C 0f71117106f639c55a3d7bc588d252a947c188218c3ee7c8f4f8698c60a5aa2d
- W a4b52fc281030ebec2c5cefd433173d3bbe732710af12d1808fbcd7768c24542
- `RE/r1j_identity_probe.py` 83c4379281c8a7f0e5b99f6894cfc6824587333b8fd720930fa804d4fde625c8 (byte-identical to r1i/r1h probe)
- M 39daae7684024256eddd52d0845fd6945415c72136d5df3b09f9e52ebfa89ec0
- D 3755af99450940bc2df46e641610d0c928b01e5db79a1a97fc6139ac8adebb40
- S 49b4f418cb9ef0ffc13fc9c8f999c9c916a00cc8957de537975d6a6d508ccefd
- T ef04bd1a435d49aa7fc683a6405f7bcd826f4ddc8fb94eb812ed0d7fb84ed238

MAESTRO's design decisions given to the builder (brief committed as `RE/codexr1j_brief.txt`):
- R1: the positive receipt never appears under the `.final` name before its bytes are durable. The canonical final line goes to `<prefix>.final.pending` (O_CREAT|O_EXCL), is flushed and fsynced with its directory; then, only if a fresh M3 reading is ≤ the deadline, `os.link(pending, final)` (no overwrite) and a second directory fsync. Any error or crash before the link leaves no `.final`. `.final.pending` is never authority and is charged to receipts. If the directory fsync after the link fails, nothing is unlinked or rewritten; the dispatcher exits nonzero and the report names this as an explicit narrowing for your ruling. No acceptance path may depend on the stderr marker.
- R2: the stub passes the Intel cutoff (T0 + budget, monotonic) to the binder, which checks it before each identity measurement, at bounded intervals inside identity loops, and immediately before success output; past the cutoff it publishes nothing and exits nonzero. The S bundle read, blocking I/O and remote process lifetime stay OPEN, with no new timeout machinery.
- R3: round-8 receipt accounting and committed-capture order unchanged. R4: report premises explicit; probe-observation vs binding-equality distinction and same-870-s-window rule kept.

MAESTRO46 verified only: `/usr/bin/python3 -B -m unittest discover -s RE -p test_r1j_collector.py` 61 OK (54 carried + 7 criterion tests); predecessor sets r1i 54, r1h 42, r1f 36, r1e 27, r1d 18, r1c 9 OK; `bash -n` W OK; J parses; probe `cmp` identical to r1i; D is 82 lines with no handoff section; only the nine r1j/v9 files are new. Grep shows `.final.pending` + `os.link` at M:76–80 and cutoff checks at B:11–13,18,23,31,85. These are presence checks, not correctness.

Review for:
1. Does V8 R1 close: can any committed surviving bytes from a failed or interrupted final persistence (including a complete `.final.pending`) be accepted by bind consumption, `require_anchor()`, successor acceptance or `qualified()`? Is the post-link directory-fsync narrowing acceptable as stated, or what must change?
2. Does V8 R2 close: can the binder publish success after T0 + budget? Does the real-stub cutoff test actually cross the cutoff during identity work without mocking the binder or loader?
3. Are R3 and R4 preserved/closed, and did any repair weaken a previously closed guarantee (committed-capture gate, anchor single use, strict identity/realpath equality, acquisition disabled, OBSERVATION-ONLY)?
4. Is the bind + inventory sequence in D executable as written within one 870 s window?

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; then exactly these two lines, each ending in yes or no:
`BIND ALLOWED: <yes|no> run the r1j wrapper's bind mode with the committed r1h probe capture`
`INVENTORY ALLOWED AFTER BINDING: <yes|no> run the r1j wrapper's inventory mode after the capture, .final and hash are committed`
and "What I checked and did not check".
