# MAESTRO decisions for R2 round 9 (MAESTRO54, 2026-10-11 ~18:50Z)

Trigger: Astra round 8 says NO-GO (`astra_r2k_verdict.md`, V8; committed 9440fdfe). Its findings are F1–F3 (high) and F4 (note); its required changes are R1–R3, followed by a closure table. Alias for this file: D9. Rulings are numbered D10–D12 so they cannot be confused with the alias D8 (`r2_round8_decisions.md`).

This file is an addendum. It does not edit C (`shared_disk_clearance_contract_v1_1.md`), DR, D8 or any reviewed subject. Where it contradicts D8, this file governs. None of D10–D12 changes C. D10 is the refusal Astra's R1 itself names as the fallback, and A1 stays exactly as the operator approved it. So no operator ruling is needed for this round. Astra judges D10–D12 in round 9 as freeze changes.

## D10 (answers R1 / V8 F1): the admission subtree keeps C:115; compositions it cannot satisfy are refused

- An admission process, and every process it spawns, is a non-science helper. It is never an A1 science descendant, wherever it appears: as the broker's `existing_admission`, or as a child declared under a wrapper root (e.g. `p2-shuf-s1` declaring `tools/c10w_p2_gate.py` as `SCIENCE_CHILD` with `DECLARED_AT_ROOT_ADMISSION`). D8 A1 item 5 already says this; P3 did not apply it.
- MAESTRO checked the source. The unchanged gate (C:85) spawns three helpers through plain `subprocess.run` (`tools/c10w_p2_gate.py:63`): `python -B tools/engine_fingerprint.py` (:69), `/bin/ps -axww -o pid=,command=` (:75), and `/usr/bin/env tmux list-sessions …` (:79, so `env` plus `tmux`). The broker's suspended spawn (D8 D5) registers only the processes the broker spawns itself, not the admission's own children. Endpoint Security `AUTH_EXEC`, the one documented kernel-held pre-exec route, needs an entitlement that has not been established on this Mac (O8 §1D). **No C:115-compliant pre-release mechanism for admission helpers is established.**
- Therefore every composition whose admission spawns any helper is **refused**, with a new explicit refusal reason (`NOT_ADMITTED_ADMISSION_HELPER_UNREGISTERED:`), and is never labelled A1-compliant. The freeze gives admission helpers their own Process role (`ADMISSION_HELPER`: pre-release registration required, A1 authority forbidden), so the checker can reject A1 authority on any admission or admission-helper record. Admissions that spawn nothing (a retained `/usr/bin/true`, where D11 keeps one) are unaffected.
- The freeze may name Endpoint Security `AUTH_EXEC` as a candidate future mechanism. It must say plainly that the mechanism is unestablished, needs the entitlement, needs Gate 2 proof and needs a separate review. It must not claim it.
- **Consequence, recorded for the operator:** until such a mechanism is proven, or the operator chooses to widen A1, every science route admitted through `c10w_p2_gate.py` gets no positive R2 clearance. D8 already withholds positive clearance from descendant-bearing roots until Gate 2, so this changes no launch that was otherwise possible today. MAESTRO will put the widen-or-not choice to the operator when it becomes live, not before.

## D11 (answers R2 / V8 F2): direct P1/P3 evaluation loses its no-op admission; every retained no-op is re-audited against its real callers

- The direct P1 and P3 evaluator profiles (TOP_LEVEL, `/usr/bin/true`) become CHILD_ONLY under the dispatcher chain, or are refused with `NOT_ADMITTED_NO_PROFILE:`. Reason: the dispatcher that reaches these variants calls `guard_phase_projection` before evaluation (`experiments/track_c/c10w_oracle_step0.py:322` defines it; calls at :340 and :413). Direct evaluation skips that check (V8 F2). The evaluator's own elapsed-time/memory guard is a different check.
- Re-audit all 29 retained TOP_LEVEL no-op admissions. For each one, record: the search that finds every caller of its entrypoint (the exact `grep` command plus its hit list), and for each caller the cited lines of every check that caller performs before dispatch. Keep the no-op only where no caller performs a check that the direct route skips. Otherwise apply the first bullet's treatment. Replace each bare `outer_obligations=[]` claim with this caller record.
- The checker reruns each recorded search over the pinned sources and fails if the recomputed hit set differs from the record. This does not prove semantics, and the freeze and report must not say that it does. It does stop the audit from silently omitting a caller.

## D12 (answers R3 / V8 F3): every delegation binding reference resolves inside its own launch

- The checker resolves every binding-hash reference on a delegation record (at least `admission_binding_sha256` and `payload_binding_sha256`) to exactly one `InvocationBinding`. That binding must belong to the same profile tree, launch context and template as the delegation. The checker also checks each associated process identity against its invocation binding.
- The production validation path (`--profiles`) runs the complete reference-coherence validation used for J5's own construction, not only schema validation plus invocation reconstruction.
- Mutation control: V8 F3's static counterexample, executed in memory. Replace profile 000's delegation payload hash (P3:146267) with profile 003's payload-binding hash (P3:152336), keep both trees' binding records and context labels, update the whole-file pin, run it through the production validation path, and it must be RED for this reason.

## Carried unchanged

D8's A1, D4, D5 and D6, and DR except where D8 replaced it. V8's closures stand (R4 receipts, R5 refusal variants), and the builder must keep them closed. All 37 existing mutation controls stay RED. Commissioning stays a separate operator authorization, and all 18 parent cases plus 10 subcases stay UNRUN.
