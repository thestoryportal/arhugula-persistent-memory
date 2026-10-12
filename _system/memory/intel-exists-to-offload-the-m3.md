---
name: intel-exists-to-offload-the-m3
description: "The Intel Mac's purpose is to take slow side work (uploads, retries, verification) off the M3; designs that move it back to the M3 get rejected"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f54ceb52-ce54-432e-a7b7-f1683803dfb2
  modified: 2026-10-11T23:50:37.508Z
---

R2 v2 (2026-10-11) had the M3 upload its own memit files to Drive between science jobs. Operator: "The whole point of the Intel is to offload work like uploading. So it kind of defeats the purpose." Approved instead: the M3 pushes files over the cable into the Intel's approved staging, and the Intel does the Drive upload, retries and checks on its own. The Intel still never reads memit, because the M3 initiates the push. The operator also declined separate macOS science/backup accounts and accepted observe-and-stop (the push yields to the existing `check_gpu` gate).

**Why:** the M3's time belongs to science; the Intel was bought to carry everything else.

**How to apply:** when a design removes a shared resource (see [[remove-shared-resource-before-policing-it]]), keep the work on the Intel by changing who initiates the transfer (M3 pushes) rather than moving the work onto the M3. Prefer reusing an existing gate over new host machinery such as accounts or reboots ([[m3-hosts-the-team-no-routine-reboots]]).
