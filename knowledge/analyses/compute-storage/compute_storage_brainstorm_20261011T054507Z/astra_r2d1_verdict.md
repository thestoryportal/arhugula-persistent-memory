VERDICT: GO-WITH-CONDITIONS

The redesign follows the operator’s direction and removes the failed descendant-list dependency. Apply the corrections below before adoption; implementation and host commissioning remain separately gated. References use your `B` and `RD` aliases.

F1. **[medium] R6 makes an approved recovery obligation optional without an explicit disposition.** Evidence: `RD:100` preserves content-once Intel recovery storage, but `RD:115` says it “remains optional.” HW1 choice 7 approved seven daily/four weekly restore points, restoring known files and an old version from Intel, with missing bulk fetched from Drive (`B/decisions_log.md:95–101`). Amendment 16 reduced the history allowance to 50 GB without dropping that scheme (`B/decisions_log.md:191`). Consequence: an implementation could treat Intel as an expendable download cache while claiming the earlier recovery choice was preserved. Choice 7 is missing from R5’s disposition accounting.

F2. **[high; commissioning condition] UID exclusion is logically sound under the stated confinement assumptions, but “full host process-table snapshot” needs a precise quiescence guarantee.** Evidence: `RD:27–28,36–37`. Consider an implementation that lists PIDs and then reads their credentials: a process could fork after the PID enumeration and exit before its credentials are inspected. Treating that disappearance as harmless could miss the surviving child. Fencing controller launches does not itself stop an already-running process from forking. Consequence: a nonempty activity account could be reported empty.

This is a missing acceptance condition, **not a demonstrated defect in a selected macOS API**—RD selects none. Require an observation method whose successful empty result cannot miss a surviving lineage; otherwise refuse. Two scans or an independent implementation are not automatically sufficient.

F3. **[medium] The privilege restrictions cover the named escape classes, but file-mediated execution across accounts needs an explicit test.** Evidence: `RD:29–31` expressly covers setuid/setgid helpers, cached sudo authorization, reusable authorization rights, scheduler submissions and cross-UID delegation; `RD:37` explicitly rejects unaccounted root-daemon activity. I found no escape that is *permitted* if those conditions actually hold.

However, protecting the controller and avoiding world-writable permissions (`RD:26,29,36`) does not explicitly establish protection of every trusted executable, imported module, hook, configuration file and replaceable parent directory. An activity account could write a group-writable script that an operator-account process later executes; its activity would then escape the UID predicate without calling sudo. Consequence: privilege confinement must include indirect execution through writable files, not merely privileged-command denial. This requires a targeted commissioning test and protection of the trusted execution paths—not another list of science descendants.

The Metal/MPS, silent CPU fallback, cache-recomputation and known-baseline risks are correctly explicit activation gates at `RD:36–37`. Successful account creation or a GPU smoke test alone cannot satisfy them.

F4. **[medium] S1–S12 provide prevention criteria, but the qualification claim must distinguish an established upper bound from a successful sample run.** Evidence: `RD:43–77`.

Every criterion has a concrete pass/fail test:

| Criterion | Checkable condition |
|---|---|
| S1 | Missing growth component refuses; qualified peak control stays within budget. |
| S2 | Below-bound refusal, equality acceptance, no double reservation. |
| S3 | Peak headroom floor and warning boundary. |
| S4 | Forbidden writers denied; permitted aggregate growth capped. |
| S5 | Timely observations; failed reads cannot remain healthy. |
| S6 | Queue deficit and maintenance dependency appear before admission. |
| S7 | No maintenance I/O during science; interrupted work remains charged. |
| S8 | No deletion without exact approval; changed identity/hold refuses. |
| S9 | Missing/corrupt/incomplete archive never qualifies as protected. |
| S10 | Capacity/time deficit blocks dependent admission. |
| S11 | Stale identity, reservations or unresolved work block dispatch. |
| S12 | Maximum qualified workload finishes without disk-full or quota-induced science termination. |

Together, S1–S4 can protect the run: if actual additional consumption stays within the reserved bounds, S3 leaves at least 100 GiB at peak. S5 is supplementary observation, not the safety mechanism. No criterion authorizes automatic deletion, counts an unverified upload as reclaimed space, or intentionally terminates active science.

The remaining qualification issue is `RD:44`: passing one maximum-size/failure-path control does not establish an upper bound for every admitted input, retry sequence or cache state. Consequence: the implementation brief must identify the admitted workload envelope and justify its aggregate bound. A science quota that stops writes on overrun would violate S12 rather than repair an underestimated budget.

F5. **[low] Design adoption and operational acceptance are conflated in one sentence.** Evidence: `RD:76` says missing enforcement evidence keeps “adoption/activation acceptance OPEN,” while `RD:120` places adoption before implementation and host commissioning. Consequence: the document creates an avoidable circular gate. Design adoption can approve conditional requirements; activation must await their demonstrated enforcement.

F6. **[informational] R1 and most of R4–R7 faithfully implement the ruling, with accurate checked citations.** Evidence:

- `RD:11–17` prohibits direct and indirect Intel access to memit, including legacy senders; the status exception is bounded telemetry. This matches `B/r2_redesign_operator_ruling.md:7–11`.
- `RD:81–86` correctly requires M3 maintenance upload, stable source generations, full verification, Git receipts, explicit lag and actual Intel visibility. The cited 5 TiB/about 4.9 TiB figure is accurately labelled historical (`memory_mirror/gdrive-rclone-remote.md:8`). The 287.177 GB path population is distinguished from Intel’s deduplicated payload (`B/decisions_log.md:234–238`).
- `RD:107–118` correctly retires the old dispatch contract without erasing its evidence. G1/G2 remain bookkeeping gaps without a demonstrated bypass (`B/r2_sweep_report.md:74–76`); tracer completeness remains unresolved (`B/r2tr_maestro_acceptance.md:18–27`). The I1a–I1c correction and downstream references checked accurately.
- `RD:124–126` implements the no-memit archive-staging instruction, including interrupted-part verification and refusal when true streaming is unavailable.
- R5’s quoted operator answers match the inspected decision log. The peak-floor semantic change, first/steady-state uploader change, cable-route restriction and dedicated-account proposal are appropriately left for operator disposition. F1 above is the material omission.
- The existing gate, backup-wrapper and storage-display descriptions match the cited source ranges. Those sources do not establish the proposed controller or host enforcement.

**Required changes**

R1. Resolve the recovery contradiction. The smallest correction is to preserve HW1 choice 7 explicitly, including its amended history cap and restore checks, and replace “recovery remains optional” with “recovery is not a prerequisite to first upload.” If optional recovery is intended, quote choice 7 and seek an explicit replacement decision.

R2. Add a UID-quiescence acceptance condition covering fork/exit churn, disappearing PIDs, PID reuse and incomplete credential observations. Require evidence for the selected observation primitive’s empty-set guarantee; ambiguity refuses switching. Retain the existing delayed-launch and same-boot switching tests.

R3. Extend confinement commissioning to group/ACL-writable trusted scripts, modules, hooks, configuration and parent-directory replacement. Include an attempted file-mediated execution under the operator account and an attempted daemon-mediated action after the originating worker exits.

R4. State that S1 qualification covers a frozen workload/input envelope with justified peak bounds; a passing sample is corroboration. Freeze the aggregate accounting and actual support-writer enforcement before activation, including retained retries and temporary allocation/free/reallocation.

R5. Separate design adoption from activation at `RD:76`; retain the sequence at `RD:120`.

The design is **not materially over-built for its safety requirements**. The smallest adoptable revision is these clarifications and tests. Keep tar/zip optional, use one M3 controller, and avoid recreating P8-style executable/descendant inventories.

**What I checked and did not check**

Verified both supplied SHA-256 hashes and RD’s 133-line count, including a final recheck. Read the ruling and decision log in full; inspected RD, the drafting brief, relevant integration/layout/history records, and cited implementation ranges.

This was a static, read-only review. No host/account enforcement, process-observation primitive, MPS reproduction, filesystem cap, transfer, restore or commissioning test was executed. No files were changed.

