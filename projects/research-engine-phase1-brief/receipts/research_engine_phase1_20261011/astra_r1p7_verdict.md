VERDICT: NO-GO

Aliases: `RE = results/research_engine_phase1_20261011`; `V = RE/astra_r1p6_verdict.md`; `C = RE/r1h_collector.py`; `M = RE/r1h_make_bundle.py`; `S = RE/r1h_stub.py`; `B = RE/r1h_bind_manifest.py`; `W = RE/r1h_host_commands.sh`; `T = RE/test_r1h_collector.py`; `J = RE/intel_provisioning_manifest_v7.json`; `D = RE/r1h_report.md`.

Counterexamples below are source-derived, not executed reproductions.

F1. [high] **The original A-replay counterexample is repaired, but interrupted finalization can leave an unqualified success receipt.** Evidence: V:7–23,93 → M:61–70,139–167,169–183,200–219; M:98–118; T:1353–1427,1482–1497.

For the requested replay:

- Preserve A; inventory consumes A through an exclusive, file-and-directory-synced M3 attempt record before SSH.
- Whether Intel completes an append or interrupts it, losing the capture and restoring Intel to A cannot reuse A: M:140–141 refuses before SSH.
- A crash after durable attempt creation but before capture reservation leaves the same dead end. Missing, nonzero or anchorless captures cannot supply a successor.
- A crash before attempt durability cannot have dispatched SSH. If the record survives, it blocks; if it does not, no remote history was created by that attempt.

However, finalization publishes `0\n` at M:207 and fsyncs it at M:208–210 **before** the final deadline check at M:211. Consider:

1. SSH succeeds and the first completion check is just before the deadline.
2. The zero exit receipt becomes durable.
3. Final persistence crosses the deadline.
4. A crash or persistence error prevents M:211–219 from replacing zero with failure.

The preserved files now advertise success despite incomplete deadline qualification. `require_anchor()` accepts the committed zero-exit capture without separate evidence that finalization completed. The same publication pattern affects bind captures. An expired deadline independently prevents later dispatch, but does not correct the false success receipt.

**Consequence:** round-6 R1’s specific lost-output/restoration defect closes under intact M3 authority. Overall unknown-outcome handling and R2’s durable late-failure requirement do not close.

F2. [high] **Intel wall-clock skew is repaired; the remote duration can nevertheless become stale before Intel starts measuring it.** Evidence: V:25–37,95 → M:147–183; S:1–2,31; C:721–743; T:1429–1497.

Intel no longer subtracts an M3 timestamp from its own wall clock. Either sign of Intel clock offset leaves the supplied duration unchanged.

But M:148 calculates the duration before bundle construction, attempt persistence, capture reservation and SSH startup. Nothing bounds that interval to five seconds or refreshes the transmitted duration afterward.

For example, with bootstrap at zero:

- M3 samples elapsed 600 seconds and bundles a 265-second allowance.
- Preparation/connection delays Intel’s process start until elapsed 630 seconds.
- Intel’s local expiry is then elapsed 895 seconds, beyond the M3 deadline of 870.

The M3 timeout normally records failure at its deadline. It controls the local SSH subprocess; this source supplies no independently established guarantee that the remote collector stops then. D:16 correctly leaves remote lifecycle qualification open. The five-second margin alone does not establish that guarantee.

**Consequence:** the cross-clock subtraction defect closes, but conservative end-to-end enforcement remains open. Normal late-return checks are present; F1 additionally prevents an unconditional claim that late runs cannot leave success receipts.

F3. [medium] **The named R3 procedure repairs are present, but complete receipt accounting remains open.** Evidence: V:39–49,97 → M:73–85,127–145,34–40; W:31–35; J:1463–1466,1515,3064; C:753–764; D:39–55,75; T:1499–1540.

The repaired parts are substantive:

- Inventory requires the bind capture’s working bytes to equal its committed Git blob and requires that blob’s SHA-256 to equal the supplied authority. Uncommitted or differently committed capture bytes refuse before SSH.
- D:42–51 places the capture/hash commit before consumption.
- J:1515 explicitly classifies the fresh probe as a separate observation before bootstrap; its exclusion is consistent with that boundary.
- J:3064 supplies five arguments after `inventory`, matching W:31–33.
- Capture companions are preserved; the procedure commits them. The exit companion remains outside the capture hash, as disclosed.

The remaining discrepancy is explicit in D:75: M3 attempt records and inventory stdout/stderr/exit are not charged. J:1466 still defines the receipt allowance as **“All inventories, stdout/stderr and evidence.”** Naming the omission does not reconcile it with that contract.

**Consequence:** round-6 R3’s enumerated capture/probe/argument repairs close in source and procedure. Complete accounting must remain open; “not a new accounting rule” does not justify excluding newly introduced receipts from an existing all-receipts rule.

F4. [informational] **The explicit SSH key preserves round-6 F4/F5’s accepted execution and launcher design. Intel qualification remains open.** Evidence: V:51–71,99 → W:28,35; S:16–42; B:25–38,49–59; C:119–194; T:997–1017,1226–1277,1297–1308,1542–1549.

Both wrapper dispatch sites name the requested key and options. This changes authentication selection without weakening complete-member verification, verified-buffer execution, direct CLT invocation, stdout binding or strict identity/realpath equality.

The failed r1f receipt contains authentication refusal, exit `1` and an empty capture. It supplies no Intel runtime observation. The reported M3 probe likewise cannot qualify Intel.

**Consequence:** retain F4/F5’s source-level acceptance. Round-6 R4’s direct-runtime Intel observation and subsequent binding equality are correctly named open.

F5. [low] **The duplicated margin is a maintenance defect, not a present-value mismatch; the single 870-second window is intentional under v7.** Evidence: M:147–150; J:1513–1523,1711,3062–3064; T:1443–1445,1524.

Both margin values currently equal five. The tests do not establish exact synchronization: T:1524 pins the manifest to five, while T:1445 checks an inequality. A stricter dispatcher margin could change without failing that assertion. Reading the sealed value, or explicitly validating equality, would remove the duplication. This is separate from F2’s elapsed-delay problem.

Every inventory and evidence update uses the original bootstrap deadline. J:1711 expressly prohibits resetting the clock for evidence updates. Therefore, **both MAESTRO observations are true**: this implements one cumulative window, and `update_command` becomes unusable after that window. It is usable for updates within the remaining window, not for indefinite later maintenance.

**Consequence:** do not introduce a fresh deadline as a routine repair. Clarify D:58’s “Later” to mean within the original window; anything beyond it requires separately reviewed recovery or authority.

F6. [medium] **The report generally distinguishes fixtures from host acceptance, but coverage and citation claims need tightening.** Evidence: V:73–99 → D:3–29,74–75; T:1353–1556.

| New test | Could pass with a relevant defect remaining? |
|---|---|
| `r1h_01`, T:1353–1427 | Yes. Meaningfully exercises complete/partial append, lost capture, restored A and refusal. Does not inject a crash between M3 attempt creation and capture reservation, or test F1’s finalization gap. |
| `r1h_02`, T:1429–1497 | Yes. Exercises opposite Intel offsets, expiry and late completion. Its late-fsync simulation lets the corrective code finish; interruption or failure before correction is absent. Preparation/transport delay is absent. |
| `r1h_03`, T:1499–1513 | Yes. Detects missing/different committed blobs through mocked Git. Does not establish operational preservation, companion finalization or successful wrapper execution. |
| `r1h_04`, T:1515–1540 | Yes. Checks command syntax/count and configured values; does not prove deadline lifecycle or exact margin coupling. |
| `r1h_05`, T:1542–1549 | Yes. Checks lines containing `ssh -T`; does not prove authentication or exhaustively detect other possible SSH invocation forms. Source inspection confirms the two current sites. |
| `r1h_06`, T:1551–1556 | Yes. Required wording can coexist with incorrect behavior. |

Specific inaccurate citations include D:4’s `V:79–81`, which discusses tests rather than Intel identity qualification, and D:18’s `T:1551`, which tests report wording rather than binding equality. M:1’s “Every mode writes stdout only” is also stale: dispatch now writes M3 receipts.

**Consequence:** round-6 R4/F6’s qualifications are improved, but the report must incorporate F1–F3 and correct these references. Reported test counts do not establish universal closure.

Required changes:

R1. Make terminal qualification fail closed across crashes and persistence errors. A provisional SSH exit of zero must not alone authorize bind consumption or successor acceptance. Add interruption/error cases after zero-status persistence and before final deadline qualification, plus the requested attempt-created/capture-not-reserved boundary.

R2. Account for preparation and transport delay between duration calculation and Intel’s monotonic baseline. Establish conservative remote enforcement without assuming a five-second upper bound or assuming local SSH termination proves remote termination. Test delayed preparation/start and disconnection behavior.

R3. Reconcile M3 attempt/inventory receipts with J:1466’s existing allowance, including pre-write bounds and retained-failure accounting, or obtain an explicit reviewed scope amendment. Preserve the repaired committed-capture gate and sequence.

R4. Correct report citations and closure claims; make the same-window update restriction explicit. Retain direct-runtime Intel identity as open until observed and strictly matched. Consolidate or validate the duplicated margin.

PROBE ALLOWED: yes run r1h_identity_probe.py on the Intel Mac via the r1h wrapper's probe mode

BIND ALLOWED: no run the r1h wrapper's bind mode

INVENTORY ALLOWED AFTER BINDING: no run the r1h wrapper's inventory mode after the capture is committed

What I checked and did not check:

- Read the packet, round-6 verdict, nine subject files, relevant carried tests and r1f→r1h differences. All ten supplied hashes matched on initial and final checks; the identity probe is byte-identical to r1f.
- Confirmed `7697cb73` adds exactly nine files. HEAD was already beyond the packet commit and advanced from `2712fd56` to `362185f5` during review; subject hashes remained unchanged. The only committed RE addition after the implementation was the review packet.
- Inspected the failed probe’s capture and companions. Did not independently verify SSH configuration/key availability.
- Did not run tests, entry points, SSH, graft, fetches or Intel commands. MAESTRO’s test/runtime results remain **reported, not reproduced**. No files were edited; excluded workstreams were not reviewed.

