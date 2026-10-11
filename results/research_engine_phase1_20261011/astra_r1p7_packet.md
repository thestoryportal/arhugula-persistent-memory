# Astra review — R1 collector repair, round 7 (narrow)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run the wrapper, the stub, the collector, binder or bundle entry points, ssh, or anything that fetches. The local unit tests need a writable temporary directory, which your sandbox has lacked; treat MAESTRO's rerun as reported, not reproduced. Repository HEAD is the commit that adds this packet. RE = `results/research_engine_phase1_20261011`.

Context: your round-6 verdict `RE/astra_r1p6_verdict.md` (sha256 49a5e4133552158fb8fac002b7fb5808b6655d64cbd959672a316edefe848a34) was NO-GO with R1 (off-host pending attempt; consumed anchor never reused after an unknown outcome), R2 (cross-machine elapsed time without assuming equal clocks), R3 (capture authority preserved before consumption; probe receipts classified; J:3062 argument list; provenance companions), R4 (direct-runtime probe as observation; strict binding equality; report qualifications). It accepted round-5 R2 and R3's execution repair (F4) and the binding/launcher design (F5), and allowed the probe.

The probe did not run. MAESTRO invoked `bash RE/r1f_host_commands.sh probe RE/intel_identity_probe_r1f_20261011T124523Z` with the r1f bytes verified equal to HEAD; ssh was refused at authentication before reaching the Intel Mac (`RE/intel_identity_probe_r1f_20261011T124523Z.stderr`, exit file `1`, empty capture; commit 3096ad7c). Cause: the M3's ssh configuration sets `IdentitiesOnly yes` for every host and has no Intel entry, so the wrapper's bare `ssh` offered only the default key. Nothing ran on the Intel Mac. The fix is in the subject: every wrapper ssh call names the Intel-only key.

MAESTRO's design decisions given to the builder:
- R1: before ssh, inventory creates `RE/r1h_attempt_<seq>_<head12>.json` with O_CREAT|O_EXCL and fsyncs it and the directory; an existing record refuses before ssh; inventory captures stdout/stderr/exit on the M3 with no-clobber names; the successor anchor is the last `R1H-ANCHOR` line of a zero-exit capture; a consumed anchor with a missing, nonzero or anchorless capture is a dead end needing operator-reviewed recovery, never a retry. MAESTRO commits each attempt record and capture.
- R2: the M3 is the only wall clock. Each dispatch computes remaining = 870 − (M3 now − M3 bootstrap start) − transit margin, refuses if ≤ 0, and passes remaining seconds to Intel; Intel enforces that budget on its own process monotonic clock and never subtracts an M3 timestamp from an Intel reading. The M3 runs ssh under a hard subprocess timeout at the M3 deadline and records an M3 end past the deadline as a failed run.
- R3: inventory refuses unless the bind capture is committed in git and its committed bytes hash to the supplied value; sequence bind → commit capture + hash → inventory inside 870 s; the fresh probe is a separate observation before the bootstrap start; v7's update_command carries the full argument list.
- SSH: every wrapper ssh call passes `-i ~/.ssh/intel_mac_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes`.

Subject (builder R1H; commit 7697cb73; all r1c–r1f files and v3–v6 untouched). MAESTRO44 checked on the M3: `test_r1h_collector.py` 42/42 (36 carried over + test_r1h_01..06); r1f 36/36, r1e 27/27, r1d 18/18, r1c 9/9 unchanged, all on `/usr/bin/python3`; `bash -n` passes; v7 parses; the r1h probe run by the CLT runtime in an empty temporary cwd prints JSON (realpath `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`, 1,637 stdlib entries) and creates no file; no `importlib`, `exec_module` or `__import__` in any r1h source; git scope is exactly nine new files.
- `RE/r1h_collector.py` (sha256 b67194d23401afbbf9d7b8d758729621e44bd21be0a99819973ca25167968441)
- `RE/r1h_identity_probe.py` (sha256 83c4379281c8a7f0e5b99f6894cfc6824587333b8fd720930fa804d4fde625c8; byte-identical to r1f)
- `RE/r1h_bind_manifest.py` (sha256 36dadb9b44753b381c44dc8218ad1dfe7f3685d8251719dfc1cf8e8e34ed44c5)
- `RE/r1h_stub.py` (sha256 3292e22a09929bc7feb312c67da337bcef4f0e1b215b9e309c2470d4de6b21c5)
- `RE/r1h_make_bundle.py` (sha256 81b31fc7ec83fa9e00ba1a5516ab0cde1f3e6d42b58526785913012879b84076; now the M3 dispatcher: attempt record, deadline, ssh subprocess, captures)
- `RE/r1h_host_commands.sh` (sha256 62ba9a1aa584c8e8e5c2cc5c0a6d2ed4cf85f0962c9ca867f41747576c13202e)
- `RE/test_r1h_collector.py` (sha256 61a880b2a38f0ea40ea7673da8989a6c578090619078b7fff0fcfb3db03cfeb5)
- `RE/intel_provisioning_manifest_v7.json` (sha256 bd96fac6ab256ded664ea3b231ebb69dc6b96dbaad6a4e5e43c4cd377eac1119)
- Builder report: `RE/r1h_report.md` (sha256 f608e7afda6213a332764729749d0bdafe3be6a92365f39b63f5ff9113d496e3)

MAESTRO's own observations, for you to confirm or dismiss:
- The transit margin is stated twice: v7 `/budget/transit_margin_seconds` = 5 and a literal `- 5` at `RE/r1h_make_bundle.py:148`. Is that a defect (two sources of truth) or acceptable given a test pins them?
- The deadline is bootstrap start + 870 s for every inventory, so every inventory, including later evidence updates, must finish inside one 870 s window from the bind. Is that the intended reading of v7's `time_total_s`, or does it make the update_command unusable after the first window?

Review for:
1. Do round-6 R1–R4 (F1–F3, F6) now close, or are they correctly named open? Cite round-6 line → source/test line. Could each new test pass on code that still has the defect?
2. R1: replay your F1 sequence (preserve A; inventory appends; output lost; Intel restored to A; invoke again with intact A), including an interrupted append and a crash between attempt-record creation and capture reservation. Does every path refuse before ssh or reach a dead end that cannot be retried?
3. R2: with the Intel wall clock offset either way, can any path give Intel more time than 870 − M3 elapsed − margin, or let a run past the M3 deadline be recorded as success?
4. R3: can inventory consume a capture whose bytes are not committed, or whose committed hash differs? Is the probe-boundary statement correct under v7 J:1515? Does v7's update_command now match the wrapper's argument count?
5. The ssh change: does naming the key in the wrapper alter anything Astra accepted in round 6 (F4/F5)?
6. The two MAESTRO observations above.
7. Any status mislabelled as verified, any claim not supported by its cited line.

Out of scope: the build trial and Amendment 22; archive handoff/coexistence; commissioning; the R2 clearance contract; the R4 dashboard record; Drive activation.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; then these lines: "PROBE ALLOWED: <yes/no> run r1h_identity_probe.py on the Intel Mac via the r1h wrapper's probe mode", "BIND ALLOWED: <yes/no> run the r1h wrapper's bind mode", "INVENTORY ALLOWED AFTER BINDING: <yes/no> run the r1h wrapper's inventory mode after the capture is committed"; and "What I checked and did not check".
