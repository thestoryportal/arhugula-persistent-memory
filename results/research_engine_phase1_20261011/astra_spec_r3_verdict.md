# Astra spec r3 verdict — research-engine phase 1
Verdict: NO-GO

## S1 properties

P1 authority/scope. MET — SR names the shared root, exact marker, sole writer, reservation owner and coordinator coverage, including future model/MPS launches. Coverage is explicitly procedural. Evidence: `science_reservation_contract_v1.md:11–17,85–87`.

P2 state. MET — Valid IDLE requires an exact marker and a successfully observed empty active set. Every entry—including malformed, temporary and hidden entries—means SCIENCE; missing/unreadable authority means UNAVAILABLE. Pending precedes the coordinator’s wait. Evidence: `science_reservation_contract_v1.md:23–38`.

P3 validity/transitions. PARTIAL — Identity, nonexpiry, multiple reservations and restart behavior are specified, but concurrent duplicate creation and release after coordinator failure can remove protection from a still-running launch. Evidence: `science_reservation_contract_v1.md:38–44`; T4 below.

P4 coordination. PARTIAL — Starting observation before admission improves detection but does not serialize pending publication against admission or RE publication. Evidence: `science_reservation_contract_v1.md:48–54`; `phase1_spec_v3.md:146,209`; T1 below.

P5 enforcement. PARTIAL — Non-Python observation, ownership records, escalation and termination receipts are specified. Watcher death, blocking operations, clock changes and loss of memit leave the promised bounds unsupported. Evidence: `science_reservation_contract_v1.md:58–66`; T2–T3 below.

## Findings

T1. [severity: blocking] **The idle-check race remains.** Evidence: `science_reservation_contract_v1.md:49–54,59`; `phase1_spec_v3.md:146,209`. A permitted interleaving is: watcher observes empty → admission observes IDLE → science creates its pending entry → RE begins work before the next poll. Similarly, pending can appear after the pre-publication check but before pointer replacement. The publisher lock is not shared with the reservation writer. Consequence: pending science can coexist with an IDLE-based admission or completed publication; subsequent cancellation cannot undo publication. SR’s “no window” claim is false. A defined ordering point is required; another unsynchronized check is insufficient.

T2. [severity: blocking] **Watcher loss does not guarantee termination of all owned processes.** Evidence: `science_reservation_contract_v1.md:61–65`; `phase1_spec_v3.md:188,194`. Only RE Python processes check heartbeat freshness. If the watcher dies during a Java-only phase, no surviving enforcer is specified. If Python does detect loss, its prescribed response is to halt without publishing, not to terminate Neo4j and confirm all owned processes absent. Ownership, heartbeat and receipt files also reside on memit: authority loss can simultaneously remove access to the information needed for shutdown. Consequence: Neo4j may survive indefinitely, with no termination receipt. The `lstart` check mitigates ordinary PID reuse, but the contract also leaves the comparison-to-signal race and newly spawned processes during shutdown unspecified.

T3. [severity: blocking] **The elapsed-time guarantees do not follow from the specified watcher.** Evidence: `science_reservation_contract_v1.md:59,62–66`. Observation is bounded by “1 s + one poll’s runtime,” but poll runtime has no bound. `neo4j stop` is not explicitly asynchronous or time-limited; a blocking invocation can prevent the +25-second escalation. Heartbeat freshness and deadlines use UTC without a monotonic elapsed-time rule. Consequence: a hung command or backward clock adjustment can extend shutdown beyond the claimed bound. The asserted publication-to-termination maximum of 31 seconds omits poll runtime. Moreover, SR explicitly accepts overlap while v3 retains “no concurrent science” (`phase1_spec_v3.md:207`); v2 required termination within “30 s total” (`phase1_spec_v2.md:205`). These requirements are inconsistent, not merely more precise.

T4. [severity: blocking] **Reservation transitions permit false IDLE under concurrency or coordinator failure.** Evidence: `science_reservation_contract_v1.md:34,38–42`. Duplicate prevention is an existence check followed by a write/rename, with no exclusive claim or serialization. Two invocations can both observe absence, then sequentially publish the same launch ID successfully; releasing either removes the only entry protecting both. Separately, ordinary release is allowed after coordinator exit, including failure, without the all-processes-gone condition required for stale-entry recovery. Consequence: a surviving science child can lose its reservation. The one-shot admission classifier might catch it, but the continuous backstop matches coordinator paths, not every science worker (`science_reservation_contract_v1.md:59–60`). Entry fsync followed by rename also lacks an explicit directory-durability requirement despite the restart guarantee (`:38–43`).

T5. [severity: condition] **The existing gates do not establish SR’s claimed universal protection or zero delay.** Evidence: `science_reservation_contract_v1.md:7,54,59–60`; `tools/c10w_p2_gate.py:22–53,73–84`; `tools/run_c10v_stage.sh:7–15`. C10W blocks nonexempt RE Python, so science can wait for RE shutdown. C10V instead filters particular science command patterns; ordinary RE Python and Java do not match that filter. Consequence: procedural reservation adoption is acceptable as an explicit cooperative premise, but these gates cannot substitute for it or prove that only Java overlaps science. The process backstop is supplemental protection, not complete coverage of omitted reservations or orphan workers. Preserve the gates; correct the coverage and delay claims and enforce the reservation lifecycle.

T6. [severity: condition] **Production-root creation and host acceptance have a circular ordering as written.** Evidence: `phase1_spec_v3.md:191,227`; `science_reservation_contract_v1.md:83,87`. MAESTRO creates the production root after BUILD1 promote, but real-root host termination is an acceptance obligation; without the root, host RE dispatch is blocked. Consequence: either promotion precedes required host evidence or the evidence cannot be obtained. Name a separate, bounded commissioning gate before final acceptance/promotion, preserving host termination as mandatory.

T7. [severity: condition] **§13 still lacks a complete pre-install identity baseline.** Evidence: `phase1_spec_v3.md:238–240`; `provisioning_dryrun_20261011.txt:3–19`; `phase1_spec_v2.md:234–235`. The receipt establishes Neo4j’s version and the install/upgrade names, but not the stated cypher-shell/JDK versions, dependency versions or bottle hashes. The repeat guard compares formula names; wheel identity is recorded at installation although a “different … hash” must refuse, without identifying the expected hash. Consequence: §13 is not fully settled for freeze beyond its two operator answers. Freeze the package/wheel identity manifest before mutation and validate against it; retain interface smoke verification before BUILD1 dispatch.

## Required before freeze

- Resolve T1–T4 with explicit ordering, lifecycle and shutdown contracts. Add deterministic controls for publication races, concurrent duplicate reservations, coordinator death with surviving children, watcher death during Java-only operation, hanging stop/observation commands, clock changes, PID reuse and loss of memit.
- Reconcile the timing/overlap requirements and accurate gate coverage in T3/T5 without changing science classifiers or exemptions.
- Resolve the commissioning order and pre-install identity baseline in T6/T7.
- Obtain the two already-named operator answers: shared-dependency upgrades and reservation-step adoption.

AC17 and AC21 are substantially checkable: the valid-IDLE positive control, pending/running-at-start refusals, IDLE→pending transition, authority-loss behavior and confirmed termination appear at `phase1_spec_v3.md:49,53` and `science_reservation_contract_v1.md:70–81`. Real host termination remains expressly mandatory at SR `:83`. However, the current cases do not establish the missing guarantees above; heartbeat-stale→Python-halt alone cannot prove whole-session termination.

## What I checked and did not check

Reviewed filenames above resolve under `results/research_engine_phase1_20261011/`, except the explicitly named `tools/` paths.

Verified these hashes before and after review:

- SR: `ee6f0c3aef920bc610de8dba711396669ed2ca3e916e7cbcd3280093091109ea`
- v2: `2e021f9228c308c9508578e734ea4daffdd3ae15af10eb2d86045c5dafb2f139`
- v3: `cbd1131974135d56ca9950740c9013fb467bac7cc869b15aa8e7931e88aa6fee`

Read r2’s verdict, SR, v3, the complete v2→v3 diff, the provisioning receipt and both cited gates. Functional edits match §15’s named sections. Additional changes are the version preamble, §13 activity statement and §15 itself; no unrelated functional section changed. R2–R4 were not re-reviewed. The timing/overlap inconsistency identified in T3 prevents an unqualified finding that all v2 requirements were preserved.

This was static contract review. Counterexamples are inferred permitted interleavings, not observed implementation failures. No tests, services, installs, science, file edits or context-save writes were performed.

🌱 graft reported ~124,341 tokens saved this turn, 1 successful call; its results supplied no review evidence.