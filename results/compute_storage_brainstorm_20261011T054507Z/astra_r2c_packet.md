# Astra review — shared-disk clearance contract v1 (R2 / I1b), fresh round

You are the program's independent cross-family reviewer. Work read-only: read and search only. Repository HEAD is the commit that adds this packet.

Context: your r1 verdict on the two-Mac design (`results/compute_storage_brainstorm_20261011T054507Z/astra_r1_verdict.md`, call the folder B/) required a separately reviewed shared-disk clearance contract (lines 24 and 47). The operator approved the division of work (choice 9, `B/decisions_log.md:115–121`); the design rule is `B/design.md:233–235`, and the gates stay unchanged (`B/design.md:216`). The approved work map row is `B/integration_r5_completion_table.md:96` (I1b); its section 5 maps 15 earlier findings to R2. Your Intel RE amendment verdict (`results/research_engine_phase1_20261011/astra_intel_a1_verdict.md`, F2 and R2) accepted the research engine's side of this interface and requires R2 to stay external and blocking. The earlier same-host science reservation contracts SR v1–v3 were NO-GO (`results/research_engine_phase1_20261011/astra_spec_r3_verdict.md`, r4, r5).

Subject:
- `B/shared_disk_clearance_contract_v1.md` (sha256 866ba46246779034b39f64e3071d797e8db8fe17bb433789cfc71eedad3ac22c). Drafted by a Codex builder (R2C), verified by MAESTRO39: no existing file changed; `tools/c10w_p2_gate.py` unchanged (sha256 fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26); no default-to-proceed and no "coordinator unreachable means idle" (line 109); no rule that terminates the research engine or Intel databases; ordinary science needs no Intel query or reachability (line 61); five citations opened and confirmed (`B/decisions_log.md:115–121`, `B/design.md:216`, `B/design.md:233–235`, `B/astra_r1_verdict.md:49`, `B/integration_r5_completion_table.md:186`).
- Builder report: `B/r2c_report.md`.

Review for:
1. Does it meet your required controls at `B/astra_r1_verdict.md:24` and `:47`, and does every one of the 15 findings the work map assigns to R2 map to a clause that actually meets it (or is honestly OPEN)?
2. Safety direction: is there any path where missing, stale, malformed or unreachable information leads to a new shared-disk start or a science clearance? Any path where ordinary science waits on the Intel Mac? Any path that terminates Intel work as a science precondition (superseded, `B/design.md:243`)?
3. Pause and resume: is a pause request ever treated as clearance? Is resume only by the explicit rule (V7 part ii, `B/integration_r5_completion_table.md:192`)?
4. Simplicity against the SR v1–v3 failure pattern: does this design add moving parts with their own timing holes? Name any clause that could be removed or merged without losing a control.
5. Acceptance tests A01–A18: is each pass/fail stated before running, and is each control covered by at least one real-pair test?
6. The open items (O-list, `B/r2c_report.md:51–54`): are they the right freezes to require before dispatch, and is anything missing?

Out of scope: the Intel provisioning freeze (R1); the dashboard record (R4); Drive activation; the backups audit.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; "What I checked and did not check".
