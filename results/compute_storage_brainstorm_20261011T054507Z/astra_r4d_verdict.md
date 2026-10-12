VERDICT: NO-GO

The proposed direction is sound, but the record is not yet sufficiently frozen for dashboard dispatch. I4a/I4b remain OPEN.

`B/` means `results/compute_storage_brainstorm_20261011T054507Z/`.

F1. [high] **The nested payload schema remains descriptive rather than exact.** Evidence: `B/dashboard_host_status_record_v1.md:17,29–39` promises full schema validation and unknown-field rejection, but defines payloads through phrases such as “typed run set,” “state,” and “checkpoint/coverage/verification receipt pointers,” without their complete field names, types, state vocabularies or conditional requirements. Consequence: independent producer and reader implementations can disagree about valid records; A07 cannot deterministically establish rejection of malformed payloads.

F2. [high] **New-generation admission assumes authenticated liveness that the selected transport does not establish.** Evidence: `B/dashboard_host_status_record_v1.md:45,51,84–86` authenticates stored record bytes with HMAC, serves that fixed cache over HTTP, and nevertheless requires an “authenticated live endpoint” to introduce a generation. HMAC proves who signed those bytes, not that their collector incarnation is currently serving them. For example, an earlier generation never observed by Intel can be replayed while its timestamps remain fresh: it is neither a retired generation nor a same-generation sequence regression, and no explicit generation-start ordering rule excludes it. Consequence: the stated checks do not fully establish the promised replay rejection or current-generation transition.

F3. [medium] **Preservation of pane-activity behavior remains an unresolved dispatch condition.** Evidence: `B/dashboard_host_status_record_v1.md:102–108,134,163` excludes capture helpers, acknowledges that its roster cannot reproduce BUSY/WAITING/IDLE, and leaves first-rollout coverage undecided. Existing behavior uses pane capture at `tools/dashboard_queue.py:541–549`; preservation/change reconciliation is required by `B/integration_plan.md:26`. Consequence: displaying UNAVAILABLE is honest, but permanent removal of an existing observation capability is not automatically baseline preservation. A12 cannot establish equivalence until the selected behavior is explicit.

R1. Freeze the complete nested wire grammar, including state-dependent fields, provenance consistency, null/empty semantics and component freshness assignments. Supply canonical valid examples and malformed cases with predetermined outcomes.

R2. Define how a reader verifies a current boot/collector transition, rejects previously unseen older generations, and preserves sequence/generation rejection state across restart. Add controls for replay within the freshness window, reader restart, and missing/corrupt validation metadata. Reconcile this mechanism with the fixed-cache-only responder requirement.

R3. Resolve pane-activity scope before dispatch. Either preserve it through source-owned evidence and reviewed exact helper forms, or record an explicit accepted behavior change and adjust A12 accordingly.

**What I checked and did not check**

- **Identity:** Both supplied SHA-256 values matched, including a final recheck. Inspected HEAD was `e613222f57d0d1a94ce54f147ab5aafff78cb9b6`.
- **Lost observation:** The written rules correctly require UNAVAILABLE with advancing age for M3, Intel components, clients and transfer observations. I found no specified disconnected-to-idle/zero/completed fallback (`B/dashboard_host_status_record_v1.md:49,72–80`).
- **Launch forms:** The collector command statically matches the unchanged CLT exemption; H1–H3 are native non-compute commands. No continuous non-exempt M3 Python process is proposed. A03 appropriately demands independent actual-command evidence, including short-lived helpers, reexec and retained processes. This is not host acceptance.
- **V6:** The negative brief-text fixture plus genuine-process positive is sufficient for the specified R4 false-positive class. Checking the compute gate alone would be insufficient; A04 also requires ownership recognition (`:116–124,145`).
- **Controls:** Intel and M3 positives are distinct. A01–A12 state expected outcomes before execution, although F1–F3 prevent complete acceptance criteria from being settled.
- **Transport/resources:** One collector/responder and bounded Intel polling are a reasonable small mechanism. The 256 MiB Intel dashboard allocation is explicitly inside the ≤6 GB support target; fit remains unmeasured. The separate decoded-record size ceiling is removable without losing bounded-input control if strict base64 decoding occurs only after enforcing the envelope cap (`:84–88`).
- **R2 overlap:** No authority conflict found: R4 consumes only a separately published advisory summary and cannot grant, renew or resume disk work (`:159–161`). I did not review R2’s substantive clearance correctness.
- **Limits:** No files changed; no tests, gate execution, process inventories, services, network operations or commissioning ran. R1 provisioning, Drive activation and the backups audit were excluded. Memory supplied a launch-form pointer; current files supplied the findings.

A graft lookup was attempted and failed before returning results (`node` missing). No graft results were used; one failed call, no token savings reported.

