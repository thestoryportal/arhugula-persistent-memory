# Astra r1 verdict — compute and storage architecture
Verdict: GO-WITH-CONDITIONS

## Findings

Citation roots: `design.md`, `integration_plan.md`, and `decisions_log.md` are under `results/compute_storage_brainstorm_20261011T054507Z/`. `RE/` means `results/research_engine_phase1_20261011/`. `activation_plan_v4.md` is under `results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/`.

F1. [severity: condition] **Section 8 still gives MAESTRO discretion to choose an M3-first upload after choice 11 settled Intel-first.** Evidence: `design.md:263` permits finishing the existing rollout before migrating, versus `decisions_log.md:133–139` and `design.md:273` approving the first upload from Intel. Consequence: the implementation owner could select the rejected alternative without obtaining an amendment to the settled choice.

F2. [severity: condition] **The shared-disk coordination requirement does not yet define affirmative clearance before science starts.** Evidence: `design.md:235` requires an allowance and asks active transfers to pause, but defers clearance mechanics and latency; versus `RE/astra_spec_r5_verdict.md:35–61`, which identifies incomplete lifecycles, unproven process absence, deadline failures, and clearance invalidated by authority restoration. Consequence: moving compute to Intel alone does not prevent an admitted transfer or surviving transfer child from reading memit during M3 science. This is an explicitly deferred implementation contract, not an observed runtime failure.

F3. [severity: condition] **The builder-return contract requires M3 checks but does not explicitly place their successful completion before canonical commitment of an affected M3-targeted change.** Evidence: `design.md:212–214` specifies returned receipts and queues required M3 checks; `design.md:377` keeps them open; versus `CLAUDE.md:17`, which requires MAESTRO to rerun verification before committing. Consequence: Intel GREEN could be integrated while a stack-dependent M3 check remains merely queued, unless the acceptance ordering is made explicit.

F4. [severity: condition] **Host attribution and collector compatibility are requirements for a future dashboard brief, not established enforcement.** Evidence: `design.md:267–269,378` defers transport and runtime proof; versus `tools/c10w_p2_gate.py:22–39,43–54,73–84`, which classifies actual local command lines and refuses failed observation. Consequence: an incorrectly located collector could report Intel processes as M3 state, while a model-free but non-exempt Python command on M3 could still block science admission.

F5. [severity: condition] **The integration seed omits later dashboard acceptance receipts already present in the repository.** Evidence: `integration_plan.md:26` relies on the builder handoff’s five unverified host checks, versus `results/dashboard_audit_20261010/fix_20261010T234721Z/host_MB38_green_20261011T004402Z_dVvWIw/run.log:32–41`, which records five host checks passing, and its `run.exit:1`, which records zero; storage activation is also recorded in `results/dashboard_storage_mb22_20261010T192500Z/host_verification_maestro19.md:3–7`. Consequence: reconciliation from the seed alone could repeat completed work or select an obsolete acceptance baseline. These historical receipts still need comparison with the selected current source hashes.

F6. [severity: note] **Two settled choices remain phrased as unanswered section checks.** Evidence: `design.md:136,307` asks for approval and says friend scope will be asked later, versus `decisions_log.md:65–73,143–159` recording those answers. Consequence: a successor could unnecessarily reopen settled choices. The section approval headers and whole-design status otherwise correctly identify approval.

## Required changes before MAESTRO acts on the design

R1. Make Intel-first the sole selected initial-upload route in §8 and integration row I2. Retain M3-first only as historical alternative or as a future operator-approved amendment. Mark the two stale section checks as answered; preserve the decision log.

R2. Before dispatching affected transfer or research-engine builds, freeze the replacement disk-clearance contract. Specify admission ordering, transfer ownership including descendants, pause acknowledgment, science-clearance eligibility, release/resume rules, coordinator/link loss, authority restoration, and a bounded failure outcome. Science must not receive clearance from a pause request alone. Include controls for an active transfer, coordinator death, interrupted pause, stale clearance and malformed/unavailable observations.

R3. Add an explicit acceptance dependency for builder returns: each M3-targeted change lists which checks are Intel-compatible and which require the actual M3 environment; required M3 checks must pass against the reconciled candidate before MAESTRO accepts and commits that change. Intel-only infrastructure instead requires its applicable Intel commissioning. Preserve exact source, patch, environment and RED/GREEN identities.

R4. Before dashboard dispatch, freeze the host-status record and collector launch forms. Require source-host/run/generation identity, source observation time, stale/disconnected behavior, and distinct Intel/M3 positive controls. Acceptance must demonstrate that every M3 collector and helper’s actual command line satisfies the unchanged admission rules; “model-free” alone is insufficient.

R5. Refresh and split the integration completion table before affected dispatch:

- Include the later storage and MB38 host receipts, their source identities, and any subsequent changes.
- Refresh the queue from its current revision: `docs/program_state.json:31` now says `2026-10-11T07:07:21Z`, versus the seed’s `06:51:40Z`.
- Give each affected row a named owner, selected version/hash, disposition, shared paths/interfaces, resource commitments, predecessor receipts and permitting review.
- Map every r3/r4/r5 finding to **already resolved**, **premise removed**, **replacement requirement**, or **still open**, with evidence.

The table’s prescribed fields and completion rules at `integration_plan.md:49–51` are checkable. Its current single `I1–I8 OPEN` row is not a completed reconciliation or dispatch clearance.

## What I checked and did not check

**Subject identity and choices.** All three supplied SHA-256 values matched. I read all 15 choices and design sections 1–14. The design carries the approved roles, separate copies, selective storage, library access, copying schedule, caps, retention, Intel model prohibition, independent Intel work, dashboard scope, connections, conditional friend trial and fallback. F1 and F6 are the exceptions to cleanly settled wording.

**Space arithmetic.** The allocation is correctly **686 decimal GB**, plus **100 GB free**, giving **786 GB before existing OS/user usage** (`design.md:154–165`). This does not prove fit on the unmeasured disk. Inventory is a hard predecessor: caps are conditional on capacity/use, unavailable observations block admission, and §13 requires confirmation before bulk work (`design.md:81,89,393`). Concurrent peak writes and the separate **20 GiB** reserve remain binding. The plan also identifies that the **268.5 GiB** parked set exceeds **100 GB** staging (`integration_plan.md:25`).

**What relocation removes.** Intel-local databases/builders no longer compete for M3 CPU or unified memory, so stopping those processes solely because M3 science starts is unnecessary (`design.md:230–233`). The old watcher, JVM-killing and reservation mechanisms need not survive unchanged merely to enforce that obsolete same-host exclusion.

**What relocation does not remove.** Shared-disk transfers still require safe admission, ownership, pause, release and restoration behavior—the failure classes behind r3 T1–T5, r4 U1–U6 and r5 V1–V6 remain relevant wherever the replacement coordinator depends on them. Local Intel resource enforcement, bounded session shutdown, valid observation, publication integrity and host commissioning also remain. R5 V7’s omitted no-resume rule and V8’s incomplete failure controls require explicit disposition, not silent deletion. Provisioning identities must be repinned for Intel; earlier resolved package-lock defects should not be relabelled unresolved simply because they appeared in r3/r4. The design expressly requires this finding-by-finding accounting (`design.md:239–245`).

**Drive obligations.** I found no blanket waiver of write pause, final catch-up, full content verification, the three operator OKs or approved bandwidth limits. They are preserved by reference at `design.md:259,263,281–286` and `integration_plan.md:24`. The inherited plan specifies the daytime **08:00–23:00, 512 KiB/s** upload cap (`activation_plan_v4.md:273`), included-writer pause through final inventory (`:314–325,383–397`), complete content coverage and full-population download fallback when required (`:335,362`), and scheduled-successor verification before retirement (`:436,452`). An Intel checkpoint upload cannot itself discharge live-source convergence. The amended plan must retain these obligations or identify explicitly reviewed amendments.

**Repo rules and friend fallback.** Git/evidence authority, MAESTRO-only canonical mutation, M3 internal-SSD restrictions and exact-path deletion approval are preserved (`design.md:79–93,206`). Borrowed data is gated by engine identity, applicable determinism/inertness and known-baseline reproduction before promotion (`design.md:346–352`; `CLAUDE.md:30–34`). No core service, recovery duty or committed science schedule depends on the loan (`design.md:358–363`). Infrastructure acceptance is correctly separated from F1/scientific evidence.

**Queue coverage.** All eight current `work_queue` entries are represented in the integration map; I found no omitted published queue item. The older integrated queue and superseded overnight plan are appropriately distinguished from current authority. The concrete evidence omission is F5. Exhaustive live-owner reconciliation remains MAESTRO’s required task, expressly acknowledged at `integration_plan.md:9,34`.

This was static, read-only review. I did not run tests, installers, services, network/Drive operations, process inventories, transfers, models or commissioning, and wrote no files or context-save artifacts. Hardware capacity, cable behavior, native compatibility and operational enforcement remain unverified. Memory supplied a dashboard launch pointer; current code and saved receipts supplied the review evidence. The graft lookup failed before returning results; no token savings were reported.

