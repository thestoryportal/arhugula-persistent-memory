VERDICT: NO-GO

Collector execution remains blocked. The trial proposal is ready for **conditional operator consideration**, not execution.

Aliases: `RE = results/research_engine_phase1_20261011`; `V = RE/astra_r1p2_verdict.md`; `C = RE/r1c_collector.py`; `T = RE/test_r1c_collector.py`; `J = RE/intel_provisioning_manifest_v3.json`; `S = RE/intel_build_trial_scope_v1.md`.

F1. [high] **Running inventory now seals an unresolved manifest into a window that cannot accept the required later evidence.** Evidence: C:157–175 hashes the entire manifest and rejects any changed manifest on subsequent invocations. J:1588–1590 leaves Intel interpreter identity unresolved; J:1611–1622 leaves the child contract unreviewed; J:30–32 leaves host identity/pools unresolved. J:1698 expressly prohibits resetting the window. T:109–123 tests only repeated use of an unchanged manifest.

**Consequence:** inventory can start the cumulative provisioning clock, but completing the missing contract or admission fields makes continuation refuse. This is fail-closed, but it is not a usable collection-to-admission sequence. Resolve the manifest lifecycle before the first inventory write; changing the retained root must not become an implicit clock reset.

F2. [high] **The cumulative deadline is not checked after the final durable summary write.** Evidence: V:36–42 → C:247–254 adds cumulative checking, but C:288–300 checks before writing/fsync and returns without a final deadline check. C:706–708 then returns the summary; C:724–726 prints it and exits successfully. J:1513 defines the endpoint as after durable checks.

**Consequence:** if the final summary write/fsync crosses the deadline, the collector can report success after expiry. T:109–123 exercises expiry between invocations, not expiry during final persistence. Round-2 F2 therefore remains partially open.

F3. [medium] **A real cumulative timeout can lose the active command’s identity in the immutable failure receipt.** Evidence: C:316,327 calls `remaining()` inside `_execute`; C:253 calls `halt()` without `argv`; C:222–223 preserves that first receipt. The later handler at C:360–361 cannot add the command. T:152–168 injects `TimeoutExpired` directly, bypassing this path.

**Consequence:** the tested timeout case preserves `argv`, but the cumulative-deadline path can persist `argv: null`. Preserve command context when creating the first causal receipt and test the actual deadline path.

F4. [medium] **Collector toolchain qualification remains an explicit, unmet prerequisite.** Evidence: V:78–80,90 requires the toolchain to be pinned before execution. J:1588–1590 correctly labels Intel identity unobserved. C:719–721 checks a minimum version, executable pathname and isolation flags; it does not establish executable/stdlib content identity. T:328–330 merely checks wrapper text.

**Consequence:** removing the environment-selected interpreter is an improvement, but does not close toolchain qualification. Obtain the Intel identity through a separately authorized read-only probe and bind it before starting this window. The report correctly leaves this open at RE/r1c_report.md:12,14,56.

Round-2 disposition and test coverage:

| Round-2 item | Verdict → implementation/test | Disposition |
|---|---|---|
| **F2** | V:36–42 → C:157–194,247–300,451–488; T:109–174 | Persistent clock, cached-byte accounting, pre-download reservation and injected command failures are meaningfully exercised. **Partially open:** F1–F3 above. Tests do not exercise the real child timeout/size-enforcement path. |
| **F3** | V:44–50 → C:371–449; T:176–252 | **Original global `/private/tmp` walk defect repaired.** Inventory streams admitted roots, separates origins and records special/incomplete entries. Tests exercise those behaviors, although socket metadata is mocked. Child behavior remains correctly open and disabled by J:1612. |
| **F4** | V:52–60 → C:54–123,584–616; T:254–292 | **Named guard and unregistered-extra defects repaired at implementation level.** Tests include a positive preinstall case with postinstall placeholders, malformed observations and an actual extra file. They cover one synthetic install root, not complete native registry/distribution acceptance; that remains open in the report. |
| **F5** | V:62–72 → C:618–708; T:332–366 | **Correctly retained as observation-only/open.** Derived archive inspection does not claim ABI/interface verification. However, test_09 calls `result()` directly for most modes; it does **not** behaviorally verify every mode’s established/open partition. |
| **F6** | V:74–80 → C:526–582,719–721; T:294–330; J:1565–1700 | Numeric policy migration, supplied-local-artifact typing and removal of lock-path fallback are substantially repaired. **Toolchain identity remains open.** Literal absence and wrapper substring checks are narrower than executable-policy verification. |

F5. [medium] **The manifest diff is repair-scoped, but complete policy deduplication is not established.** Evidence: structural comparison found the same ordered 48 artifact IDs, with artifact changes confined to fetch commands, the DuckDB lock’s absolute source path, and the three R3 entries’ route/verification requirements. Other changes are schema, task scope, named probe root, command pointers and the added collector/preinstall blocks. Budget, host, selection, tree and commissioning blocks remain unchanged.

There is no new package/version or lock-path fallback. However, receipt allowance exists at both J:1460–1463 and J:1604, while interpreter executable/flags appear in J:1578–1583 and independently in RE/r1c_host_commands.sh:5. C:719–721 does not compare those manifest executable/flags fields.

**Consequence:** the current values agree, but absence of competing policy representations is not fully proven. Derive these values or mechanically assert equality; do not describe literal removal alone as complete F6 closure.

F6. [informational] **The Intel trial scope is appropriately bounded and candid about its missing execution machinery.** Evidence: S:5–7 limits the proposal to five serial, single-attempt ports and requests separate authority; S:21–37 specifies the scratch root, independent logical/allocated 4,000,000,000-byte caps, 7,200-second clock and fresh pool admission. S:15–17,41–46 explicitly blocks execution pending the stage/image adapter, exact inputs/prerequisites and enforceable child-tree confinement/caps. S:50–54 requires full prefix comparisons, lifetime write evidence and retained failures.

**Consequence:** suitable for conditional operator approval. Before execution, all named gates must be satisfied, including source-route equivalence, exact command vectors, ACL/xattr enumeration, exclusive writer reservation and enforcement that bounds in-flight growth. Endpoint equality alone cannot establish that no transient outside write occurred. “Reversible” here means isolated retained scratch with separately approved deletion—not automatic rollback.

Required changes:

R1. **Resolve the persistent-window/manifest lifecycle before inventory.** Freeze prerequisites before starting, or supply a reviewed evidence-update mechanism that preserves the original clock, byte accounting and prior receipts without relaxing frozen policy.

R2. **Close both deadline defects.** Check elapsed time after final persistence and before successful completion; preserve active command identity on cumulative timeout. Add behavioral cases for both paths.

R3. **Bind the Intel collector toolchain and policy equality.** Keep acquisition disabled until the curl identity, write-root behavior, redirects and unknown-length size enforcement are reviewed.

R4. **Keep trial approval conditional.** Operator approval alone must not bypass the unresolved adapter, prerequisite, confinement, hard-cap and prefix-verification gates.

NEXT STEP ALLOWED: no — run r1c_host_commands.sh inventory on the Intel Mac

The shorthand also omits the required manifest argument; the complete proposed command is at J:1550. Inventory writes receipts and starts the provisioning window. It dispatches no child process, and I found no install/build/sync/selfupdate/cleanup dispatch path. Acquisition modes—`fetch`, `wheel`, `archive-index`, and network-backed `inspect`—must remain blocked. `guard`, `compare-installed` and `r3` also lack their required current evidence; no blanket mode clearance is granted.

TRIAL SCOPE READY FOR OPERATOR: yes — conditional proposal only

What I checked and did not check:

- Read all six subjects, the round-2 verdict and relevant cited local authority. All six supplied hashes matched before and after review. JSON parsed; shell syntax passed.
- Attempted the authorized unittest command: **nine setup errors**, all because the read-only sandbox had no writable temporary directory. No test body ran. This neither reproduces nor contradicts MAESTRO’s reported 9/9 result.
- HEAD changed from `bac3c607db061a4cf30e4b2309cbc5ebdf50a770` to `2b6bab56fe3c984dd6fc38e957dc82985e5ab215`. The intervening changes affected only `docs/program_state.json` and `memory_mirror/trim-builder-reading-lists.md`; this verdict binds to the unchanged subject hashes.
- Did not execute the wrapper or collector entry point, fetch, access Intel, build/install, or write review artifacts. External MacPorts source citations were not independently retrieved. Excluded workstreams were not reviewed.
- A higher-priority hook forced one graft CLI attempt; it failed with `env: node: No such file or directory`. No graph output was used; no token savings were reported.