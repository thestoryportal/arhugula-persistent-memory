# R4D report
Status: RECORD READY FOR ASTRA; proposed freeze only, host acceptance UNRUN.
Scope: two new Markdown files; no existing file edited, code written, commit,
collector/test/service launched, network operation, dashboard restart or tmux call.
Workspace verified: c10k-route-a, branch worktree-c10k-route-a.
Drift check: accurate support-host observation protects M3 science admission;
this is infrastructure for F1, not a scientific result (B/design.md:214,269).

Deliverable: B/dashboard_host_status_record_v1.md.
Citation alias B = results/compute_storage_brainstorm_20261011T054507Z/.
Read the requested sources in order, excluding *_exec.log files.
Read current storage/reload code, gate-launch receipt and concurrent R2 draft.

Requirement coverage:
1. Record identity/schema/per-view payload: freeze §§1–2; reader/writer paths,
   atomic publication, authentication and malformed/wrong-host rules: §3.
2. Named staleness values and all three views' disconnect behavior: §4.
3. Small Thunderbolt transport: §5; one in-process M3 responder, Intel polling,
   bounded bytes/time/memory; <=6 GB Intel support target includes dashboard.
4. Exact M3 collector command and every native helper: §6; character-level CLT
   regex match at tools/c10w_p2_gate.py:35; helpers satisfy :22,51–53 by being
   non-compute, not by a fabricated regex exemption. V6 negative control: §6.
5. Distinct Intel/M3 positives and predeclared PASS/FAIL: §8, A01–A12, all UNRUN.
6. Storage/freshness/reload baseline and explicit changes/limits: §7; historical
   composite is not current/multi-host acceptance (B/astra_r5table_verdict.md:11).
7. Shared-disk overlap/open transport question: §9; R4 does not consume R2
   authority or add an Intel/dashboard dependency to M3 science.

Open inputs for MAESTRO/Astra:
- Implementation owner, permitting review and selected source/profile hashes.
- Commissioned host/boot IDs, private-link endpoint and host-secret provisioning.
- Real CLT/helper command evidence, Intel environment and measured memory fit.
- Whether first rollout requires live pane-busy detail: minimal roster marks
  unsupported activity UNAVAILABLE; richer capture needs a reviewed launch form.
- Whether R2 shares a transport/profile or publishes an advisory display summary;
  current default is independent records and no clearance-service dependency.

Read-only source pins captured before writing (SHA-256):
tools/c10w_p2_gate.py fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26
tools/dashboard_queue.py 099bb6334242339d12b168dd93c3450a4ca2b2d8301794b6d8f4ee942478aa6e
tools/team_dashboard.sh f5dc68bf586ea9a6a33539fee0cd2646547d151dbc876661d76da5917477d3e1
tools/dashboard_queue_tab.sh d3fbf908b733d9e901f34a6ba7420fd23ae1b1ed6cde7b165dcad371b0957f27
B/design.md 20f88e7c50acff3e0061dd9c6dee0e70e68627a197e5921e9acb344a075717b1
B/integration_r5_completion_table.md 8f43668d555d02e553e5513ecb1ba3428dd31b1631a0d7d393a7a4012ff4fd81
B/integration_plan.md 9d5974aa737dcaa8aefdb02f0eadeddc227233911ba5ef49a5105a88f9b36185
Final static verification: all seven read-only pins unchanged after writing;
all seven requested topics covered with citations; one collector/three helpers
have exact launch text and gate classification; 12 real-pair cases remain UNRUN.
Freeze SHA-256: 9853d81329676598b641e416e58d965a80a1945cfa50a8232a20a29b6b836f92.

Session context saved here within the two-file authorization; no separate
context-save artifact or memory update. Next: MAESTRO submits this freeze to Astra.
Learning: literal launcher text differs from the real CLT process executable;
static regex compatibility cannot stand in for actual-command commissioning.
Binding context directive for successors/team sessions: start new work only at
>=60% context left; at <=40% or any compaction stop starting work, write exact
done/in-flight paths, next steps and open risks into the report, and hand off.
