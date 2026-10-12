VERDICT: NO-GO

The admission-origin V/T repair closes V11’s two concrete counterexamples. Gate 1 remains OPEN because D15’s science-origin application still omits reachable processes and operand families. Aliases follow the packet; `read`, `train`, `eval`, and `step0` below mean `experiments/track_c/c10w_oracle_{read,train,eval,step0}.py`.

F1. [high] **Profile 19 incorrectly represents `dispatch p1-project` as having no descendants.**

Evidence: P7:38102 declares `children: []`; :38118 selects `p1-project`; :38610 makes it TOP_LEVEL; :38638 leaves `composition_refusal` null. However, `step0:372–386` loads the P1 certificate and calls `T.require_training_preflight` **before** reaching the `p1-project` branch at :418. `train:65–66` launches the verifier even for an ordinary passing P1 certificate.

This omission predates this round—P6:39427 also has an empty child list—but remains material to the proposed freeze. K9:2814–2848 validates children already present; an empty list does not trigger a missing-science-occurrence check.

Consequence: A known descendant is undeclared, contrary to A1’s declaration requirement and F10:265. The profile also appears descendant-free despite F10:266 withholding positive clearance from descendant-bearing roots until observation commissioning. This is a source-derived coverage defect, not an observed runtime escape.

F2. [high] **Science-origin replication coverage still depends on argv phase instead of the loaded certificate.**

Evidence: K9:1661–1664 requires replication coverage for direct trainers, P3 evaluators and `p3-*` dispatchers. It excludes P1/P2 evaluators and other dispatcher stages.

Yet `eval:360–361` loads and verifies the certificate without first forcing its phase to equal evaluator argv. Likewise, `step0:383–386` verifies the loaded certificate before its later stage branches. `train:51–66` does not impose that equality. A passing P3 certificate reaches `read:588 → :538 → :543–550`, including the unbounded replication probes.

P7’s P1 evaluator children are fingerprint, verifier and P1 `phase_trains` (:2800,3057,3212; list ends :3338). Its P2 evaluator children likewise omit replication (:3987,4244,4399,4646,4926; list ends :5064). Their refusal strings omit that family (:3831,5566). The existing `phase_trains` and `disk_phases` families cannot substitute for replication’s separately loaded operands.

Consequence: The admission-side D14 repair remains closed, but its underlying reachability rule is not consistently applied to science origins under D15 item 6. Existing refusals protect these evaluator compositions; they do not make their coverage declarations complete. F1 identifies a related profile without a composition refusal.

F3. [note] **Route V, route T and the reported admission-count reduction are correctly represented.**

Evidence: P7:382153–382170 and J9:42113–42130 give V loaded-data cardinality. P7:382335–382368 gives T a separate loaded operand source and a six-probe bound pinned to `read:515`. Profile 38’s distinct route/family records are P7:382819–382832. K9:2568–2583 checks reachable admissions; :2753–2774 rejects route merging; :2824–2839 requires operand-domain refusal and preserves D10.

The dispatcher bounds **10/12/8** correctly account for `step0:414` plus `eval:357`. The separate P1 same-seed family is sound: `eval:431` calls the list-producing `phase_trains` before `next` selects an item, so up to five probes occur.

Consequence: **72 − 25 − 4 = 43** reflects replacement of indexed admission recipes by explicitly refused families, without dropping an admission route. The smaller aggregates are valid reconstructions of the supplied profiles, not bounds on unenumerated runtime populations. For the recorded metadata mappings inspected, I found no further bound derived solely from post-spawn validation; F1–F2 concern missing coverage.

F4. [note] **R12A–C and R11A–C pass their intended regression checks; the R10D diagnostic change is acceptable.**

Evidence: K9:2963–2971 requires seven distinct mocked probes before the pinned validator rejects the training-unit count. :2974–2987 establishes six plus six disjoint route operands. :3004–3029 reloads the baseline, applies each mutation separately and requires its specific diagnostic.

My run observed all **56 intended RED**, including:

| Control | Observed reason |
|---|---|
| R12A | Loaded-data count represented by an unpinned constant |
| R12B | Routes merged without pinned pre-spawn operand equality |
| R12C | Route T count bound unpinned |

K8:2367 and K9:2364 both require `matched`; changing that assertion’s diagnostic does not weaken its boolean. The surrounding matching logic changed separately, and the preserved R10D mutation still rejects the merged origin.

Consequence: These controls close the requested counterexamples. They do not test the science omissions above. R11B’s output is appropriately narrowed at K9:2516 to no file writes or real Git/verifier launches, while acknowledging source reads/path resolution.

F5. [low] **F10 still names an obsolete acceptance procedure.**

Evidence: F10:317 says this revision uses K5/P3 and `r2s_report.md`, while :330 and :359 require K9 and the current packet.

Consequence: This is a contradictory verification instruction, although the current manifest and actual acceptance runs make the intended procedure clear. It does not invalidate the K9 receipts, but should be corrected before freezing the successor.

F6. [note] **Earlier narrow closures and operational boundaries remain preserved.**

Evidence: K9:2182–2207 retains caller-query checks; :2210–2261 retains same-launch delegation and process-identity checks; :2029–2044 retains the schema-valid 65-input aggregate counterexample. All 53 predecessor controls remain intended RED.

F10:207,263 preserves composition refusal; :209 preserves A1; :266 preserves observation uncertainty; :12,277 preserves Intel-local work and absence of an idle-Intel prerequisite. F10:336,359–360 preserves separate commissioning authorization and all **18 parent cases plus 10 subcases UNRUN**.

Consequence: V11 F3–F5, V10 F2, V8 R2/R3 and earlier R4–R6 remain closed **within their previously reviewed static scope**. I found no additional contractual relaxation, Intel-dependent ordinary-science wait, or science-triggered Intel termination. F1–F2 are failures to represent the unchanged requirements faithfully.

**Required changes**

R1. Complete science-origin coverage for the already identified verifier/replication paths. Include `p1-project`’s verifier, and include replication wherever a loaded certificate can select P3 unless pinned pre-spawn code excludes it. Keep independent operand sources separate; refuse uncovered families and propagate those refusals. Add isolated controls for the empty-child `p1-project` model and P1/P2 argv with a passing P3 certificate. Check expected occurrences independently of the supplied child list, then rebuild bindings, aggregates, inventory and pins and rerun acceptance. Preserve source bytes, C, A1 and D10.

R2. Correct F10:317’s obsolete checker/profile/report references when producing that successor.

| V11 R1 bullet | Closure |
|---|---|
| Account for disk-selected records and probes before validation failure | **Closed for admission route V.** Loaded-data family and seven-probe control replace the false six bound. Science application remains incomplete under F2. |
| Keep verifier and `phase_trains` operand sources distinct | **Closed.** Separate V/T families and distinct profile-38 bindings; no cross-origin merging. |
| Add isolated seven-operand and differing-route controls | **Closed.** R12A/B produce their intended RED; R12C protects T’s bound pin. |
| Correct claims, rebuild/repin/rerun, and refuse uncovered cases | **Partly closed.** Reconstruction and acceptance pass; science coverage/refusal omissions F1–F2 and stale instruction F5 remain. |

**What I checked and did not check**

I reviewed V11, D15 and the carried decisions, relevant C/F10 clauses, targeted P7/J9 records, checker logic, pinned source paths, builder RED evidence and MAESTRO’s acceptance record. P7/J9 were read selectively.

I independently ran `/usr/bin/python3 -B K9`:

- Default: **exit 0** — 114 schemas, 17 request kinds, 259 examples, 1,411 hash references, eight bindings, 16 observations.
- `--profiles P7`: **exit 0** — 55 profiles, 215 refusals, 506 reconstructed bindings including eight schema-local bindings, 13 queries, 43 admission occurrences.
- `--mutation-controls`: **exit 0**, **56 intended RED**.
- Aggregate maxima: TOP_LEVEL **14 inputs / 2,797 bytes**; all-profile **27 / 3,668**.

The reported per-origin metadata totals reproduced exactly. They count represented occurrences; they do not establish completeness.

I made no edits and ran no custom reproduction, science, transfer, native observer or commissioning case. I did not independently repeat MAESTRO’s stricter sandbox/census experiment or separately recompute every packet digest and HEAD comparison. F1–F2 are source-derived findings.

