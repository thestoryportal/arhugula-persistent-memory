# MAESTRO decisions for R2 round 7 (MAESTRO52, 2026-10-11 ~17:15Z)

Trigger: Astra round 6, NO-GO (`astra_r2i_verdict.md`, required changes R1–R6 at :79–89). This file is an addendum. It does not edit DS (`r2_inventory_scope_decision.md`) or DC (`r2_science_containment_decision.md`), which are reviewed subjects; where it contradicts them, this file governs. Astra judges each decision below as a freeze change in round 7.

## D1 (answers R5): DS's activity rationale is withdrawn and replaced

DS item 1 said: "the queued re-test reuses the Arm R recipe … so C10W is the family the next science run will launch." That is wrong (verdict F5, :48–56).
- Arm R is the AutoResearch loop's best recipe at sandbox commit `73f78ce` (`/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10`), paired with Arm M, the minted-token lead (CORPUS/45). It is not the C10W LoRA oracle (`results/autoresearch_reaim/operator_ruling_retest_20261011.md:6–18`).
- That ruling approves planning only. The re-test's pre-registration, its executable and its run authorization are all still to come (same file, :6 and :17–18). Its work-queue items `retest-plan`, `retest-freeze` and `retest-run` are all `blocked` (`docs/program_state.json:320` onward).
- C10W step 5 is CLOSED: final replicated reading ⟨D-C10w-oracle@6a735469⟩, CORPUS/57, "P3 not required" (`EXPERIMENT_RUNBOOK.md:53`). No C10W run is authorized or pending.
- A zero basename match in narrative program state is not a retirement test. It is withdrawn as evidence.

Corrected activity basis. A launcher is active only when an authoritative decision (a Decision-ID in runbook §5 or an operator ruling file) authorizes or queues a run that launches it, directly or as a descendant. On that basis no science launcher in the repo is active today. The next science entrypoint, the re-test's, does not exist yet. It must get a complete SCIENCE LaunchProfile, reviewed before it runs under R2 clearance. That is the `what_would_admit` clause every refusal already carries, so the re-test needs no change to the refusal policy.

What stays from DS:
- Every science launcher without a complete profile is explicitly refused. The refusal prefix becomes `NOT_ADMITTED_NO_PROFILE:`; `RETIRED_NOT_ADMITTED:` is retired because "retired" was the unsound claim. The citation becomes this file, D1.
- `LATE_BOUND_ARGV:` refusals stand (verdict F5 found them supported).
- Refusal binds every route to the launcher: direct, manual, scheduled and as a descendant of an admitted parent (verdict F5, :50). An admitted parent whose declared children include a refused launcher is itself not admitted.

Why C10W keeps its profiles even though it is not active: it is the only family whose admission runs through an existing gate and coordinator (`tools/c10w_p2_gate.py`, `tools/run_c10w_p2_stage.sh`). That makes it the worked production example that R1, R2 and R4 test the freeze against. Its profiles are kept as that example, not because a run is coming. Round 6's R4 asks for its transitive children to be completed, so they are.

## D2 (selects R1): one production guard/profile composition, J3's

J3's SCIENCE construction is canonical. `science-guard` owns `/invocation` and declares `launch_id` and `self_sha256`. The science payload lives under `/authorized_payload`. `InvocationBinding.template_path` resolves inside the owning profile (K3:513–518, 553–558, unchanged). Every production SCIENCE profile in P is rebuilt to that shape, the wordlist and trainer included. Each must have guard template ownership, launch-context declarations and binding receipts. F4, J3 and P must state the same construction. No external wrapper composition is frozen; one would need its own decision and review.

## D3 (selects R4): how a permitted science child is registered before it runs

Unchanged science code spawns children with ordinary `subprocess.run`, and the gate's bytes stay unchanged, so no broker can sit in front of each spawn. The selected mechanism is declared-tree registration at root admission:
- When the root launcher is admitted, its admission record registers its complete declared descendant set: every (child entrypoint, variant) with its argv template, bindings and dependency identities, including transitive ones such as the P3 replication `git ls-files` probes. That registration exists before any process of the tree executes.
- Observation reconciles each observed descendant against that registered set by exact match.
- A descendant that matches no registered entry fails the full-population comparison that F4:242 already requires ("Compare the full population to broker ledger … Denied/incomplete observations fail"), so it receives no clearance (C:115–119). This decision adds no new consequence, no default-to-proceed, no science wait on the Intel Mac and no termination of Intel work.
- The `BROKER_SUSPENDED` label is not used for science children. Their registration is labelled `DECLARED_AT_ROOT_ADMISSION`. Non-science profiles keep their broker and sandbox requirements unchanged.

Proving this on real hardware stays Gate 2/3 work (verdict F4, :46).

## Not decided here

R2 (top-level versus child-only entrypoints), R3 (science `Process` representation and role restriction) and R6 (checker additions) are construction work. They go to the builder brief `codexr2q_brief.txt` with the direction stated there.
