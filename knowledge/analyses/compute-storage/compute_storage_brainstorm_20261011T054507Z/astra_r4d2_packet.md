# Astra review — R4 dashboard host-status record, round 2

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run collectors, dashboards, services, tmux, the gate, or anything on either Mac. Repository HEAD is the commit that adds this packet. B = `results/compute_storage_brainstorm_20261011T054507Z`.

Context: your round-1 verdict `B/astra_r4d_verdict.md` (sha256 665eabc7da73598e281302ec8beda07a25dd733a57b71ace36856f223c4e0495) was NO-GO: F1 nested payload schema descriptive, F2 generation admission assumed liveness HMAC cannot give, F3 pane-activity scope unresolved; required changes R1–R3. For R3, MAESTRO decided to PRESERVE per-session BUSY/WAITING/IDLE (operator asked for a never-stale queue view; `B/integration_plan.md:26` requires preserving today's behaviour).

Subject (drafted by Codex builder R4D2; v1 untouched). MAESTRO42 checked: scope is exactly these three new files; the examples file parses with 60 cases, each with a predetermined outcome (14 ACCEPT, 46 UNAVAILABLE); the report maps F1–F3 and R1–R3 to v2 lines.
- `B/dashboard_host_status_record_v2.md` (sha256 18cea57f829d273e580cc9bd5b7b7866d96b2adb62285a004fc369fa634173c4)
- `B/dashboard_record_v2_examples.json` (sha256 e40e38b3959a5bb73ed15c83a297831fbc03efc7212ef1c3568a061d13aa03cf)
- `B/r4d2_report.md` (sha256 52c45dfd5bf9d54105b9ca45b20a4caa1cc5d7d14fd6cd3bfdbe33181ce4b3a6)

Tradeoff MAESTRO wants judged (v2 §3.1, lines ~108–116): a signed snapshot can never introduce a generation; every collector boot or re-exec requires a manual, out-of-band console pin installed on the Intel reader by the operator, and the feed shows UNAVAILABLE/TRANSITION_UNVERIFIED until then. That is a recurring operator chore after every M3 reboot or collector crash. Before this goes to the operator as a cost, say whether an automatic transition can close F2 with equal strength while keeping the responder a fixed cache — for example, the Intel reader verifying the current collector tuple (boot id, PID, start time, reserved counter, committed snapshot hash) through a separately authenticated read-only channel to the M3 (e.g. a pinned-key ssh forced command that only reads those values), with the reader still rejecting older and unverified generations. If yes, name what that channel must guarantee. If no, say why manual pinning is the minimum.

Review for:
1. Do F1–F3 and R1–R3 close, or are they correctly named open? Cite round-1 line → v2/examples line.
2. R1: is the nested grammar complete and exact enough that independent producer and reader implementations must agree? Do the malformed cases cover every rule, and is each predetermined outcome right?
3. R2: does the generation-counter / reader high-water / pin design reject older unseen generations inside the freshness window, sequence regressions and replays, across reader restart and with missing or corrupt reader state? Is it consistent with the fixed-cache responder?
4. R3: are the H4/H5 pane-capture helper forms exact and matched to the unchanged gate (`tools/c10w_p2_gate.py`), and does A12 test equivalence with `tools/dashboard_queue.py:541–549`?
5. The transition tradeoff above.
6. Any status mislabelled as verified, any claim not supported by its cited line.

Out of scope: R1 provisioning/collector; Drive activation; the R2 shared-disk clearance contract (R4 only consumes its advisory summary); commissioning.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; a line "AUTOMATIC TRANSITION POSSIBLE: <yes/no> <one-line reason>"; a line "DASHBOARD BUILD ALLOWED: <yes/no>"; and "What I checked and did not check".
