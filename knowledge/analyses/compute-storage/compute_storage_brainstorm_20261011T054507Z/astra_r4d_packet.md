# Astra review — dashboard host-status record and collector launch forms v1 (R4 / I4a, I4b), fresh round

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Repository HEAD is the commit that adds this packet.

Context: your r1 verdict on the two-Mac design (`results/compute_storage_brainstorm_20261011T054507Z/astra_r1_verdict.md`, folder B/) required, at line 28: "R4. Before dashboard dispatch, freeze the host-status record and collector launch forms. Require source-host/run/generation identity, source observation time, stale/disconnected behavior, and distinct Intel/M3 positive controls. Acceptance must demonstrate that every M3 collector and helper's actual command line satisfies the unchanged admission rules; 'model-free' alone is insufficient." Work-map rows `B/integration_r5_completion_table.md:103–104` (I4a, I4b) and V6 at :191. The design places the dashboard service on the Intel Mac (`B/design.md:249–270`).

Subject:
- `B/dashboard_host_status_record_v1.md` (sha256 9853d81329676598b641e416e58d965a80a1945cfa50a8232a20a29b6b836f92). Drafted by a Codex builder (R4D), verified by MAESTRO39: no existing file changed; `tools/c10w_p2_gate.py` unchanged (sha256 fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26). MAESTRO39 loaded the gate module and tested the proposed M3 collector command line (line 97) against its real `EXEMPT_RE`: exempt = True; `/bin/ps` and `/opt/homebrew/bin/tmux` do not match `COMPUTE_EXE`; a `.venv/bin/python` form of the same script is not exempt. Lost observation is UNAVAILABLE with age, not idle (lines 74, 80).
- Builder report: `B/r4d_report.md`.

Review for:
1. Does the record carry source-host, run and generation identity and source observation time, and does a reader reject malformed, stale, wrong-host or replayed records as UNAVAILABLE?
2. Stale/disconnected behavior per view: is any path shown as idle, empty or zero when observation is lost?
3. Launch forms: is every M3 collector and helper listed with an exact command line, and does each satisfy the unchanged gate? Is the V6 negative control sufficient? Is any continuous non-exempt M3 Python process introduced (`B/design.md:269`)?
4. Transport and resources: is it the simplest mechanism over the Thunderbolt link, within Intel support memory (`B/design.md:218`)? Name anything removable without losing a control.
5. Positive controls for Intel and M3 are distinct, and every acceptance test states pass/fail before running.
6. Preserved behavior (`B/integration_plan.md:26`) and overlap with the shared-disk clearance contract (`B/shared_disk_clearance_contract_v1.md`, reviewed separately): any conflict?

Out of scope: R1 provisioning, R2 contract content, Drive activation, the backups audit.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; "What I checked and did not check".
