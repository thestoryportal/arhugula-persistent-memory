VERDICT: NO-GO

Gate 1 remains OPEN. The packet repairs the original clearance-revision error and INITIALIZE hash target, but production admission, profile composition and science-process accounting remain inconsistent.

Aliases below retain the packet’s exact paths.

F1. [high] **The production profiles do not implement the guard-binding construction demonstrated by J3.** Evidence: F4:34,158–161; J3:13935–14022; P:8–15,160–165,302–304,1005–1035.

J3’s SCIENCE profile places `science-guard` in `/invocation`, with `launch_id` and `self_sha256` declarations. P instead places the science payload in both `/invocation` and `/authorized_payload`; its wordlist profile has no bindings, and the trainer declares only payload parameters. Targeted searching found no guard, launch-ID or self-hash declaration in P.

An external wrapper is a possible design, but the freeze must specify its composition with P and how its `InvocationBinding.template_path` resolves. The existing binding checker resolves templates inside the owning profile, where P’s `/invocation` means the payload (K3:513–518,553–558).

Consequence: V5 R2 closes for the synthetic example, but not for the submitted production interface. Implementers currently face two meanings of `LaunchProfile.invocation`.

F2. [high] **The no-op admission representation permits a P2 route that omits its required outer gate.** Evidence: P:48923–48929,51699–51712; `tools/run_c10w_stage.sh:13–15`; `tools/run_c10w_p2_stage.sh:3–6,22–34`; C:85–87.

P admits `run_c10w_stage.sh p2-shuf-s1` with `/usr/bin/true`. That script directly executes the dispatcher. The separate P2 wrapper supplies the fingerprint/GPU/dispatch gate and explicitly requires launch through the single coordinator. The profiles contain no top-level-versus-child-only restriction preserving that route.

For the wordlist, the documented no-op faithfully represents the absence of a separate executable pre-screen gate (I3:152–157). It does not establish scientific admission. Extending that representation to a callable P2 inner launcher loses a real outer admission obligation.

Consequence: unchanged gate *bytes* do not establish unchanged admission. This profile offers a route around G unless additional, presently unfrozen caller restrictions apply.

F3. [high] **DC is defensible in principle, but its schema implementation is internally contradictory and does not securely delimit the exemption.** Evidence: C:115–119; F4:115–118,217,241; J3:385–406,4662–4677,10194–10234.

C does not require a science sandbox. Observation-based science accounting can satisfy it if registration, descendant ownership and closure remain complete. However:

- Every `Process` still requires a nonnull `sandbox_profile_sha256` identifying a `SandboxProfile`. Unsandboxed science therefore cannot be represented faithfully in the process/capability population.
- `ScienceChildProfile.role` accepts the general `Role` type, while its invocation always omits the sandbox field. It also permits `RECOVERY_EXCLUSIVE_CREATE` and `AUTHORITY_WRITE`. The science-only exemption is not constrained to science roles.

`shared_disk_access` supplies a useful READ/WRITE declaration. It does not itself establish pre-spawn registration, dispatch ownership or cessation.

Consequence: the split needs reconciliation throughout enrollment and observation, not merely at invocation shape. The assertion that every non-science invocation retains its required sandbox identity is not established.

F4. [high] **The C10W child inventory is incomplete, and broker enrollment is declared without a concrete integration mechanism for existing spawns.** Evidence: P:543–762,116409–119102; `experiments/track_c/c10w_oracle_train.py:65–66,137–144`; `experiments/track_c/c10w_oracle_read.py:133–134,531–550,583–588`; F4:239–242.

A concrete missing branch is P3 training:

1. The trainer invokes `verify-preflight`.
2. For P3, that verifier invokes `authorized_phase_entry`.
3. This calls `replication_for`, which performs `/usr/bin/git ls-files --error-unmatch -- <adapter>` probes for P2 adapters.

The direct trainer profile lists only the verifier child. The fixed `p3-shuf-s0` profile likewise lists verifier/trainer variants but lacks those Git invocations and their adapter bindings. P3 dispatch also reaches that replication check through `ensure_authorized` (`c10w_oracle_step0.py:343–350,375`).

Separately, `BROKER_SUSPENDED` labels do not explain how unchanged Python/shell subprocess calls reach the coordinator’s suspended-spawn broker. G itself uses ordinary `subprocess.run` (G:62–79), while F4 requires its bytes unchanged. Post-spawn observation cannot provide registration before execution.

Consequence: exact matching would reject a legitimate declared branch, or enforcement would have to tolerate an undeclared child. Gate 1 needs the integration mechanism selected; its native proof can remain Gate 2/3 work.

F5. [medium] **DS’s refusal policy is acceptable in principle; its activity determination is not sound.** Evidence: DS:3,6–8; `docs/program_state.json:316–337`; `results/autoresearch_reaim/operator_ruling_retest_20261011.md:6–18`.

R1 does **not** require executable profiles for every retired launcher. A complete catalogue can explicitly refuse unsupported routes, provided refusal applies to direct, manual, scheduled and descendant launch paths.

But zero basename matches in narrative program state do not prove retirement. DS’s concrete inference is also wrong: Arm R is the AutoResearch recipe at sandbox commit `73f78ce`, paired with the minted-token arm—not the C10W LoRA oracle. The cited ruling authorizes planning, with the executable and run authorization still to follow.

The timestamp-directory and dispatcher-digest refusals are supported by the cited source paths (P:157957–158066). The direct `freeze` form correctly remains separately profiled because its directory is supplied before invocation. I found no demonstrated fixed variant wrongly refused in those examined branches.

Consequence: retain explicit non-admission, but correct its rationale and map activity through authoritative decisions and launch dependencies. The next re-test entrypoint is not yet established; C10W cannot be claimed as that entrypoint from this evidence. No deployed refusal/bypass behavior was tested, and F1/F4 leave the proposed enforcement incomplete.

F6. [medium] **K3 closes important construction checks but still admits specific semantic omissions.** Evidence: K3:536–607,610–664,692–699,1052–1056,1418–1465; J3:12479–12482,33579–33581.

The six supplied bindings now undergo source-pointer dereferencing, declaration/value comparison and complete argv/environment reconstruction. The original pending-revision comparison is corrected.

Two remaining counterexamples follow statically from the checker:

- **Swapped QUERY revision:** change `QUERYSuccessResponse.body.observation.observed_sequence` from `3` to `4`, then update the whole-file schema pin. K3 skips QUERY in observation revalidation and never compares that fresh returned observation with the current authority. The field is schema-valid and has no reference enforcing its equality.
- **Omitted mandatory reference:** remove `/policy_sha256` from the `CheckpointRecord` mandatory-field manifest and remove the corresponding root-example reference. K3 checks supplied manifest entries and nonblank citation locations, but never reconciles the manifest with F4’s independently stated hash obligations. The omission therefore removes its own checking obligation.

These are **static deductions, not executed mutations**. Also, `--profiles` performs schema validation only; it does not run production declaration/coherence checks.

Consequence: GREEN establishes the advertised checked constructions, not complete observation or reference coherence. V5 R3/R4 remain partly closed.

F7. [note] **The INITIALIZE repair and major operational boundaries are preserved.** Evidence: J3:26817–26824,33527–33533; K3:1060–1069; F4:163–181,243–255,283–301,328,354.

INITIALIZE’s after-state reference now names `AuthorityRecordInitialized`, matching its transition. The checker verifies the resulting receipt/state links and passes. The old observed pair and replacement epoch are separately represented for reconciliation.

I found no newly specified idle-Intel reachability prerequisite, science-triggered Intel database/RE termination, automatic transfer resume or permission from uncertain authority. Independent recovery restrictions remain. Gate 2 still requires separate commissioning authorization; all 18 parent cases and 10 named subcases remain UNRUN. F2 prevents an unqualified claim that existing science admission is preserved.

Required changes:

R1. Freeze one production guard/profile composition, including guard template ownership, launch-context declarations and binding receipts. Make F4, J3 and P agree.

R2. Distinguish independently admissible entrypoints from child-only recipes. Preserve the P2 gate/coordinator obligations; retain `/usr/bin/true` only where absence of a separate admission is established.

R3. Reconcile unsandboxed science with `Process`, enrollment and observation records. Restrict the exemption by actual role/capability, preserving mandatory sandbox identities elsewhere.

R4. Complete the transitive C10W child profiles, including P3 replication Git probes. Select how every permitted child is registered before execution while preserving the unchanged gate.

R5. Correct DS’s activity rationale using the operator’s actual re-test decision. Retired routes may remain explicitly refused; their complete profiling is not required for this freeze.

R6. Check QUERY’s fresh observation against current authority and reconcile mandatory hash obligations independently of the supplied manifest. Add isolated controls for both omissions, rerun production semantic checks, and resubmit the pinned packet with every commissioning boundary retained.

| V5 requirement | Closure |
|---|---|
| R1 — Complete inventory and launch profiles | **Partly closed.** Substantial catalogue, profiles and explicit refusals supplied; admission routes, transitive children and enforcement composition remain incomplete. F1–F5. |
| R2 — Consistent science launch-ID binding | **Partly closed.** Synthetic declaration/context/rendering repaired; production guard composition remains inconsistent. F1. |
| R3 — Observation and revision semantics | **Partly closed.** Original clearance and replacement-epoch defects repaired; fresh QUERY observation escapes revision validation. F6–F7. |
| R4 — Semantic checks and negative controls | **Partly closed.** Pointer/render/declaration checks added; independent reference completeness remains insufficient. F6. |
| R5 — Pinned resubmission and preserved boundaries | **Partly closed.** Resubmission, recovery and Gate 2/3 boundaries preserved; unchanged admission cannot be affirmed. F2, F7. |

**What I checked and did not check**

I read the prior verdict, contract and relevant freeze sections, DC/DS, builder briefs/reports, checker logic, targeted schema constructions, inventory, selected production profiles and their source branches. P was searched and read in targeted ranges, never in full.

The authorized default checker exited **0**:

`GREEN: 109 schemas, 17 request kinds, 244 examples validated, 1380 hash references recomputed, 6 bindings rerendered, 15 observations checked`

The profile check exited **0**: **55 LaunchProfiles**, with **168 not_admitted entries explicitly outside J3 schema validation**.

Mutation controls could not start: the read-only sandbox denied creation of their TMPDIR directory. I therefore did not independently reproduce MAESTRO’s mutation results or execute the counterexamples above.

I did not independently recompute every packet/source digest, exhaustively verify every profile, or establish deployed bypass prevention. No repository files were written; no graft, science, services, transfers, native observation or commissioning ran. Host behavior remains UNVERIFIED.