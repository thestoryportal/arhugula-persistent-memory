VERDICT: NO-GO

Aliases: `RE = results/research_engine_phase1_20261011`; `V = RE/astra_r1p7_verdict.md`; `C/B/S/M/W/T = RE/r1i_collector.py / r1i_bind_manifest.py / r1i_stub.py / r1i_make_bundle.py / r1i_host_commands.sh / test_r1i_collector.py`; `J = RE/intel_provisioning_manifest_v8.json`; `D/H = RE/r1i_report.md / r1i_handoff.md`.

Counterexamples below are source-derived, not executed reproductions.

F1. [high] **The original zero-exit crash sequence closes, but failure during final-receipt persistence still depends on a subsequent corrective write.** Evidence: V:16–25,90 → M:62–71,127–151,335–354; T:1611–1652; H:15.

The requested original replay now fails closed:

- SSH succeeds and `.exit` becomes durable with zero.
- A crash before qualification or `.final` creation leaves no acceptable final receipt.
- Post-sync expiry also withholds `.final`.
- Bind consumption requires committed qualification at M:281; successor acceptance requires it at M:116–118.

However, `exclusive_record()` writes and flushes the complete positive `.final` **before** its file and directory fsyncs finish. If that persistence fails, rejection depends on subsequently appending a marker to stderr at M:352.

A remaining sequence is:

1. Complete canonical `.final` bytes reach the file.
2. Final fsync fails.
3. The process crashes before the stderr marker, or that corrective write also fails.
4. The surviving companions, including `.final`, are committed.

`qualified()` then accepts: the positive JSON is complete, `.exit` is zero, timestamps qualify, and the rejection marker is absent. Both bind consumption and `require_anchor()` can accept those bytes.

**Consequence:** this moves the vulnerable positive-publication boundary; it does not establish unconditional failure closure across final-persistence errors. H:15 names double-I/O failure and unknown-final publication as open, and D:48–56,81 supplies an operational prohibition against publishing uncertain finals. Those are additional premises, not the criterion-1 guarantee that failed finalization itself leaves unusable authority. T:1623–1652 lets the corrective marker finish and therefore misses this sequence.

F2. [high] **READY/GO repairs stale budget calculation, but the binder does not enforce the resulting remote cutoff throughout execution.** Evidence: V:27–41,92 → M:198–210; S:65–94; B:23–38,57–60; `RE/r1i_identity_probe.py:12–16,25–50`; T:1682–1755.

The timing arithmetic is sound under the stated clock-rate assumption: T0 precedes READY reception, and budget is calculated afterward. Arbitrarily long preparation or READY/GO delay cannot move the **calculated** `T0 + budget` beyond `deadline − margin`; sufficiently long delay causes refusal.

But after the stub’s last module-loading check, S:91–92 calls the binder without another deadline guard. The binder performs identity measurement at B:23 and again through B:38/C:182. Those scans have no budget checks, and B:59 publishes success without a final check.

For example, on a common elapsed-time axis:

- Deadline: 870; margin: 5.
- T0 and GO calculation occur around 840; budget is approximately 25.
- Identity work finishes around 868.
- The binder publishes success after its remote cutoff of approximately 865.
- M3 can still receive and qualify it before 870.

This requires ordinary lengthy identity work, not necessarily a blocked syscall.

Framing improvements are substantive: EOF and malformed GO refuse; the post-verification wait uses the T0-based cap; inventory checks detect observable stdin/stdout disconnection before guarded effects. However, the initial bundle read has no timeout (S:36), and later blocking I/O/process lifetime remains unqualified, as D:13,83 acknowledges.

**Consequence:** round-7’s preparation/transport defect closes in the budget calculation. “Intel enforces T0 plus budget” at J:1516 is broader than the implementation. The new delay test checks arithmetic and collector boundaries; the real-stub test exercises refusal paths, not a bind that crosses its remote cutoff.

F3. [informational] **The requested M3 receipt-accounting repair is present, including retained failures and `.final`; the committed-capture gate is preserved.** Evidence: V:43–55,94 → M:154–164,246–258,273–288,300–315; C:765–788; J:1463–1466,1525–1535; T:1508–1522,1757–1776.

The listed attempt and bind/inventory companions are measured from file sizes without filtering for success. Dispatch reserves the configured bound; captured output is bounded, with space withheld for attempt/status/final/error overhead. Intel receives measured M3 usage plus the current reservation, subtracting bootstrap bytes already separately charged.

Committed capture equality, supplied hash equality, committed companions and final qualification precede inventory dispatch.

**Consequence:** round-7 R3’s identified omission closes at source level for the listed files under serialized operation and intact retained authority. The tests do not establish concurrent-writer safety or operational preservation; the report appropriately discloses those limits.

F4. [informational] **The committed probe satisfies the previously missing direct-runtime observation, but does not establish binding equality.** Evidence: V:57–63,96 → `RE/intel_identity_probe_r1h_20261011T131105Z.json:1`, companion `.exit:1`; B:25–38; T:1789–1790.

I verified the capture SHA-256, zero exit companion, empty stderr, committed presence, and byte equality of the r1h/r1i probe sources. The capture contains the reported x86_64, macOS 14.8.9, Python 3.9.6, CLT executable/realpath and 1,637-entry stdlib identity.

**Consequence:** accept this as the separate historical runtime observation. Strict current identity and realpath equality remain correctly open until bind executes. No binding acceptance follows from the probe alone.

F5. [low] **Margin duplication and same-window wording are repaired; closure and citation claims still need qualification.** Evidence: V:65–86,96 → M:249,279–295; J:1523,3078–3080; D:5–21,81–84; H:6,9–15; T:1778–1796.

The dispatcher reads the manifest margin, the exact-delta test checks coupling, and the report explicitly preserves the original 870-second window. The earlier incorrect identity citations are replaced with relevant binding checks.

Remaining reporting issues:

- D:6’s error-marker claim needs its successful-corrective-write premise kept explicit.
- D:7’s cutoff inequality must be distinguished from actual enforcement during bind.
- H’s references to “this report:78/79” are stale after relocation; they no longer identify the verification receipt/open-risk text.
- Test source lines identify assertions, not evidence that a particular acceptance run passed.

**Consequence:** round-7 R4’s specific margin/window/citation repairs mostly close; unconditional R1/R2 closure does not. Acquisition-disabled and OBSERVATION-ONLY labels remain appropriate.

F6. [medium] **All twelve new tests can pass while relevant gaps remain.** Evidence: V:73–86 → T:1611–1796.

| New test | Relevant defect it can miss |
|---|---|
| `01_zero_exit_without_final…`, 1611–1621 | Complete positive final surviving failed persistence. |
| `01_final_errors_and_post_sync_expiry…`, 1623–1652 | Interruption/failure before the corrective stderr marker. |
| `01_attempt_durable_before_reservation_crash`, 1654–1666 | Final-publication defects; this test does directly cover its named crash boundary. |
| `01_success_final_is_accepted_only_after_commit`, 1668–1680 | Ambiguous final persistence; transport supplies a synthetic successful anchor. |
| `02_delays_and_wall_skews…`, 1682–1704 | Binder overrun; T0 is modeled separately from the fake transport. |
| `02_real_stub_no_go…`, 1730–1748 | Successful bind crossing budget; later disconnection/blocking-I/O boundaries. |
| `02_expired_go_kills_transport`, 1750–1755 | Remote lifecycle after GO; it checks the local fake transport. |
| `03_disk_accounting…`, 1757–1766 | Concurrent changes and remote/M3 integration. |
| `03_output_bound…`, 1768–1776 | Real SSH behavior and other persistence failures. |
| `04_sealed_margin…`, 1778–1787 | Actual enforcement of the calculated cutoff. |
| `05_probe_bytes_identical`, 1789–1790 | Current Intel binding equality. |
| `06_report_round_trip…`, 1792–1796 | Incorrect behavior despite required wording. |

**Consequence:** these are useful targeted tests, but reported 54/54 does not establish the remaining guarantees.

Required changes:

R1. Remove reliance on a post-failure corrective stderr write to invalidate a published positive final, or obtain an explicit reviewed narrowing of the guarantee. Add cases interrupting final persistence before that marker and failing the marker write; test subsequent bind and successor consumption of all surviving committed bytes.

R2. Enforce the remote budget during binding identity work and before successful publication. Add a real-stub bind case that crosses `T0 + budget` while remaining inside the M3 deadline. Keep process-lifetime and blocking-I/O limits separately open rather than claiming the cutoff equation proves them.

R3. Retain the receipt-accounting repair and committed-capture ordering.

R4. Update closure claims and relocated handoff citations. Preserve the probe-observation/binding-equality distinction and same-window restriction.

BIND ALLOWED: no run the r1i wrapper's bind mode with the committed r1h probe capture

INVENTORY ALLOWED AFTER BINDING: no run the r1i wrapper's inventory mode after the capture, .final and hash are committed

What I checked and did not check

- Read the round-7 verdict, brief, report, handoff, relevant implementation and test paths, manifest changes, and committed probe companions.
- All ten supplied subject hashes matched on initial and final checks. Probe hash and source-byte equality also matched.
- HEAD advanced from packet commit `3629479a` to `310c1f21` during review through unrelated queue/memory commits. Subject bytes remained unchanged and matched HEAD.
- Did not run tests, entry points, SSH, graft, fetches or Intel commands. MAESTRO’s test results remain **reported, not reproduced**.
- No files were written; excluded workstreams were not reviewed.

