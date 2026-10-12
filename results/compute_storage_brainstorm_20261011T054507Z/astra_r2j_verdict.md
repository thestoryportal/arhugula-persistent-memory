VERDICT: NO-GO

Gate 1 remains OPEN. The packet repairs the named QUERY and mandatory-hash omissions and substantially improves production profiles, but registration, guard execution and admission routing remain inconsistent.

Aliases below retain the request’s exact paths.

F1. [high] **D3 registers permitted recipes, not the process identities C requires before release.** Evidence: C:87,115–117; DR:28–34; F5:209,260–263; J4:333,355–381; `experiments/track_c/c10w_oracle_train.py:65–66`; `experiments/track_c/c10w_oracle_read.py:130–135`.

The root declaration supplies executable/argv/environment recipes and dependencies. It cannot supply future children’s PID/start/audit-token and parent/group identities. Ordinary `subprocess.run` releases those children without the selected mechanism registering those identities first. Later population reconciliation cannot establish pre-release registration, and a short-lived child can finish before a snapshot observes it.

`DECLARED_AT_ROOT_ADMISSION` correctly replaces the misleading science `BROKER_SUSPENDED` label, but relabelling does not satisfy C:115. A mismatch discovered after the root is already RUNNING also cannot retroactively prevent that child’s execution.

Consequence: D3 weakens the unchanged contract’s registration requirement. This is a Gate 1 mechanism gap, not merely missing Gate 2 evidence.

F2. [high] **The guard’s ordinary sandbox remains incompatible with its frozen invocation and assigned execution duties.** Evidence: F5:26,70,207; J4:4784–4786,10547–10556,14158–14174,16908–16910; P2:9–26.

The canonical `/invocation` now correctly names `science-guard`. However, J4 types it as `ScienceInvocationProfile`, which forbids a sandbox field, and production guard invocations carry none. Meanwhile, the GUARD `Process` requires a sandbox identity. The supplied `SandboxProfileGuard` has empty `exec_paths` and `deny_fork_exec=true`, while F5 assigns the guard execution of admission and payload.

No selected delegation sequence reconciles these constraints. The repaired science/ordinary `Process` union and restricted child roles are useful, but they do not resolve this guard boundary.

Consequence: implementers must either violate the ordinary sandbox requirements or invent another launch composition. D2 is consistent at the argv/template level, not yet across the full execution contract.

F3. [high] **The P2 wrapper restriction does not eliminate direct P2 admission bypasses.** Evidence: P2:7624–7644,8182–8184,1135–1141,1449–1451; I4:157–163,259; `tools/run_c10w_p2.sh:2–4`; `tools/run_c10w_p2_stage.sh:3–6,22–34`; `experiments/track_c/c10w_oracle_eval.py:352–374`; `tools/c10w_p2_gate.py:151–158`; C:85–87.

P2 profiles direct `c10w_oracle_eval.py P2 …` as TOP_LEVEL with `/usr/bin/true`. Direct trainer profiles likewise remain TOP_LEVEL and can select a P2 certificate. These paths retain internal certificate checks but omit the coordinator/wrapper’s current GPU admission and other outer launch obligations.

The 19 CHILD_ONLY recipes repair the previously identified dispatcher/inner-wrapper route. They do not justify I4’s broader assertion that P2 has “no admitted root route.” Absence of an executable pre-screen inside a child’s own `main()` is insufficient evidence that it is independently admissible.

Consequence: the 36 retained no-op admissions are not all established as safe independent entrypoints. At least direct P2 evaluation remains a concrete counterexample.

F4. [high] **D3’s admission receipt cannot hold a submitted TOP_LEVEL production tree.** Evidence: F5:209; J4:1415–1421; P2:130636–130638,330989,334464–334472; K4:1552–1576,1677–1707.

F5 requires the admission `ActionReceipt.input_receipts` to contain the owning profile and every `InvocationBinding`. That array permits at most **32** hashes.

TOP_LEVEL profile 46 has **34** bindings, numbered `Binding000` through `Binding033`: its required receipt therefore needs at least **35** entries. Profile 45 has 32 bindings and likewise exceeds the limit once its owning profile is included. K4 checks individual binding coverage but does not construct this required aggregate receipt.

Consequence: production coherence reports GREEN for trees whose frozen admission record is unrepresentable.

F5. [medium] **Variant-qualified refusals do not match several valid invocation forms.** Evidence: K4:1534–1545,1616–1623,1703–1706; P2:50087–50094,139924–139933,142475–142497; `tools/run_c10w_p2.sh:9–17`; `tools/run_c10w_p2_stage.sh:11–13`.

`refusal_matches` treats `ordinary` as an empty argument suffix and other variants as an exact suffix. But an ordinary coordinator invocation requires two arguments; `--reattempt-eval` requires a directory; and `p2-eval --reattempt` also requires a directory.

The corresponding parent declarations omit those required arguments, allowing their comparison with the refusal catalogue to pass. A real invocation containing the required operands would not match these refusal entries.

Consequence: D1’s all-route refusal policy is sound, but K4 has not established its implementation. General refusal of unprofiled roots remains protective; the claimed descendant-refusal propagation is incomplete.

F6. [medium] **K4 can still accept bindings assembled from different launch contexts.** Evidence: F5:117,140–142; K4:538–608,1562–1576,1682–1685; P2:145078–145104,145160–145221.

For each bound value, K4 checks the source record’s hash, owning profile and declared pointer. It does not require the guard, payload and descendant bindings in one launch construction to use the same context/launch identity.

A static counterexample is to add a second schema-valid context for profile 1 with another launch ID and directory, then bind the payload’s directory to that context while retaining the guard’s original context. Updating the affected source hash, rendered array/hash and whole-file pin satisfies the implemented comparisons. This is a **static deduction, not an executed mutation**.

Consequence: recomputation proves each substitution locally, but not that the complete tree belongs to the cleared launch. Production checks need a launch-scoped binding relationship.

F7. [note] **The specific R6 repairs, corrected activity rationale and commissioning boundaries are preserved.** Evidence: DR:7–20; `results/autoresearch_reaim/operator_ruling_retest_20261011.md:6–18`; `docs/program_state.json:324–382`; `EXPERIMENT_RUNBOOK.md:53`; F5:211–219,274,336–357; K4:617–621,703–707,1377–1386.

D1 correctly distinguishes AutoResearch Arm R from C10W, uses authoritative decisions and dependencies rather than basename absence, and requires the future re-test entrypoint to receive its own reviewed profile. This is a sound admission basis, not a live process observation.

The six replication Git recipes across the 11 affected profiles address the identified P3 branch; F5 specifies their source-derived adapter values, and K4 checks their presence and offline environment. Synthetic vectors remain appropriately labelled.

QUERY revision checking and independent mandatory-hash obligations now reject the two V6 counterexamples. I found no newly specified idle-Intel prerequisite, science-triggered Intel termination or automatic transfer resume. Separate commissioning authorization and all **18 parent cases plus 10 subcases UNRUN** remain explicit.

Required changes:

R1. Replace or revise D3 with a concrete mechanism satisfying C’s process registration before release, including transient and orphaned descendants. Any relaxation of C must be explicit and separately approved.

R2. Reconcile guard invocation typing, mandatory sandbox identity and admission/payload execution through one selected, implementable composition.

R3. Audit admission by complete launch dependency chain. Restrict direct P2 trainer/evaluator routes so they cannot omit the required coordinator/gate obligations; correct the claim that P2 has no admitted root route.

R4. Make the complete root-admission receipt representable. Add production aggregate construction checks against the frozen cardinality and size bounds.

R5. Define structured refusal variants covering required operands and valid arities. Correct impossible parent argv declarations and test refusal propagation using actual source-valid invocations.

R6. Bind each production tree’s guard, payload and child receipts to one authenticated launch context. Add an isolated cross-context substitution control, then repin and rerun the packet.

| V6 requirement | Closure |
|---|---|
| R1 — Single production guard composition | **Partly closed.** Guard ownership, declarations and template receipts agree; ordinary sandbox/execution composition remains inconsistent. F2. |
| R2 — TOP_LEVEL/CHILD_ONLY and justified no-ops | **Partly closed.** Wrapper chain improved; direct P2 routes and impossible parent argv remain. F3, F5. |
| R3 — Science exemption and process accounting | **Partly closed.** Science `Process` representation and child role/capability restrictions repaired; guard boundary remains unresolved. F2. |
| R4 — Transitive children and pre-execution registration | **Partly closed.** Identified P3 Git recipes added; D3 does not satisfy C:115, and aggregate admission receipts overflow. F1, F4. |
| R5 — Correct activity rationale | **Closed for the requested rationale correction.** D1 is sound; refusal enforcement has the separate remaining defect F5. |
| R6 — QUERY, independent hash obligations and production checks | **Named repairs closed; broader semantic assurance partly closed.** Both controls reproduce RED and `--profiles` runs production checks, but F4–F6 escape those checks. |

**What I checked and did not check**

I read V6, DR, relevant contract/freeze sections, targeted J4/P2 constructions, inventory and builder records, checker logic, and the cited launch-source branches. J4 and P2 were searched and read selectively, never in full.

I independently ran the authorized checker with `/usr/bin/python3 -B`:

- Default: **exit 0**, 109 schemas, 17 request kinds, 248 examples, 1,391 hash references, six bindings and 16 observations.
- `--profiles P2`: **exit 0**, 55 profiles, 168 explicit refusals and 679 rerendered binding vectors.
- `--mutation-controls`: **exit 0**, all **26 intended RED**, including R6Q and R6H.

These ran in this managed read-only environment. I did not independently repeat MAESTRO’s separate sandbox positive control or filesystem census. K4 checked its configured pins and production dependency identities; I did not independently recompute every packet digest or exhaustively verify every profile.

No files were edited. No science, services, transfers, native observation or commissioning ran. The additional counterexamples above are source/schema deductions, not executed launches or custom mutations.