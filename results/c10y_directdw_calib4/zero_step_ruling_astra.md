**FIX-FIRST. Choose option 3 for the current design: calibration 4 remains terminal `ZERO_STEP-IDENTITY`. Fix the recording defect; neither proposed tolerance amendment is justified by this evidence.**

Read-only review completed. The current driver, harness and prereg hashes match calibration 4’s recorded identities ([calibration.json:799–807](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw_calib4/calibration.json:799)). No model, simulation or tests were run.

1. **PROPERTY of the implemented comparison; no demonstrated causal arithmetic BUG. The persistence BUG is separate.**

   The numerical paths are different:
   
   - Recipe A solves the full right-hand side on CPU fp32, then casts and adds to fp16 weights: [c10e_bandknob.py:205–217](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10e_bandknob.py:205).
   - C10Y solves the factor on CPU, transfers factors to the model device, then forms and merges their product: [c10y_directdw_arms.py:238–243](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:238), [:562–563](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:562), [:635](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:635).

   The gate faithfully compares **realized updates**, using CPU-float64 relative Frobenius distance, and requires count identity. It correctly halted: [driver:1762–1772](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:1762), [:2630–2667](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:2630). The diagnostic establishes distances **0.00015952–0.00029340** and counts **8/53/13 versus 8/52/12**, ordered canon/first/full: [diagnostic:10–21](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_halt_diagnostic_20261009T023240Z_CALIB4.json:10), [:624–627](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_halt_diagnostic_20261009T023240Z_CALIB4.json:624).

   **Required qualifications to the diagnosis:**
   
   - “Cannot pass by construction” is unsupported. Non-bit-exact arithmetic can still satisfy a finite tolerance and identical discrete outputs. Prereg :45 disclaims bit-exactness; :47 nevertheless promises zero-step reduction, and :129–131 explicitly define its empirical acceptance criteria. This is an unfulfilled requirement, not a logical proof that the check is impossible. [Prereg:45–47](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Y_DIRECTDW_PREREG.md:45), [:129–132](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Y_DIRECTDW_PREREG.md:129).
   - The simulation uses **random factors and injected perturbations**, real pristine weights, and norms borrowed from C10X. It performs neither this run’s solves nor model inference. It illustrates rounding amplification; it does not measure calibration 4’s fp32 gap, condition number, changed-element fraction, or prompt margins. [fp16_realize.py:5–17](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw_calib4/fp16_realize.py:5).
   - Net `+1/+1` does not establish one changed prompt; multiple gains and losses could cancel. “Borderline” and “expected” remain hypotheses.
   - The exact repeat floor and capture distances were lost. Reaching (iii) supports that (ii) passed under the inspected control flow; it does not recover those measurements.

   Competing explanations remain numerical reassociation/device effects, solve conditioning, and an unisolated state/input or implementation discrepancy. The first is plausible, not conclusively established.

2. **Reject options 1 and 2 as admission amendments on this packet. Select option 3 now.**

   **Option 1:** recipe A’s fp32-versus-float64 discrepancy is not an established upper bound on the *different* factored solve plus MPS product. Both paths’ errors matter. Multiplying that gap by ten supplies no demonstrated guarantee. A per-run tolerance also becomes more permissive when the reference becomes less numerically reliable.

   The proposed `±1` allowance matches the already observed failure. Freezing an ε before seeing margins does **not** make that allowance independent of observed outcomes. A margin rule additionally needs a precisely defined token/prefix statistic and a justified relationship to logit perturbations; neither is supplied.

   **Option 2:** a planned-update comparison is useful diagnostic evidence, but `k·cond(M)·ε₃₂` is not yet a specified acceptance bound. The norm, constant, matrix construction errors, right-hand-side errors, product errors and non-vacuity limit remain unspecified. More fundamentally, small pre-cast error does not establish the original deployed behavioral reduction.

   **Check (iv) cannot replace either missing comparison.** It compares the factored hooked model with the factored merged model, not either with recipe A. Both could agree perfectly while disagreeing with recipe A. [driver:1937–1944](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:1937).

   Thus these are **post-failure relaxations as currently proposed**, for the same substantive reason ASTRA option C was refused: the replacement statistic/bar lacks independent justification for the requirement it would replace. [ASTRA ruling:58–64](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10z_astra_attempt3/v7_ruling_astra.md:58).

   **Exact disposition:** retain (iii) and (iii-b); introduce **no replacement statistic, bar, ε, or count allowance**. Calibration 4 supplies no candidate verdict, method-family falsification, capacity conclusion or F1 closure. A separately justified redesign remains possible; it is not approved here.

3. **The record defect is confirmed; repair is required before any future calibration.**

   All sixteen named files across calib1–4 contain `{}\n`. The causal chain is exact: local records accumulate inside `instrument_prefix`; the caller’s `prefix={}` is replaced only on successful return; an exception therefore sends the empty object to `persist_prefix`, which manufactures empty placeholders. [driver:2498–2501](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:2498), [:1359–1375](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:1359), [:1303–1315](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:1303).

   Approve a **record-only correction** that:
   
   - Saves already computed records and offending gate inputs before their gates, including baseline rows, capture floor/distances, partial ledger, overlap audit and available parity records.
   - Uses immutable phase records or another explicit partial-record scheme; does not permanently freeze an early incomplete aggregate.
   - Preserves exclusive creation and flush/fsync; marks unexecuted checks **NOT-RUN**, never passed or silently `{}`. Existing primitives already support exclusive durable writes: [driver:124–132](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:124).
   - Passes forced-halt regression tests proving retained values, unchanged gate outcome, cleanup, and refusal to overwrite existing artifacts.

   Recomputing solves or adding new numerical diagnostics is additional instrumentation, not merely moving serialization. No historical backfill. The correction is necessary but **not sufficient** for calibration-5 admission.

4. **Delegation permits team decisions; it does not justify a success-seeking retry. No calibration 5 is authorized by this ruling.**

   The operator’s quoted delegation supplies decision authority. D-C10r-rulings-14 supplies measurement-driven budget authority, with recorded arithmetic and review when prereg caps change; it does not itself change science gates. [Runbook:385](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/EXPERIMENT_RUNBOOK.md:385).

   A future calibration 5 requires a **new team admission decision** grounded in a demonstrated causal correction or independently justified redesign—not merely repaired logging. Before dispatch: freeze and review the amendment and implementation, pass required tests, repin sources and inputs, record spend arithmetic, confirm GPU availability, preserve resource/deadline guards, and use a fresh namespace and diagnostic. Run all required baseline and LAW checks afresh. The standing rerun rule prohibits reading around a compromised run; it does not establish that an unchanged retry will be informative. [Runbook:382](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/EXPERIMENT_RUNBOOK.md:382).

   The cheapest informative follow-up is preservation and comparison of the **actual** reference pre-cast update, factors and device product on identical inputs. That would distinguish numerical mechanisms; it would not automatically qualify them.

The drafter should append:

```text
Amendment ZERO-STEP-DISPOSITION — [UTC date]
Decision ID: [team-assigned ID]
Status: post-calibration-4 observation; no new admission criteria.

Authority
Operator delegation: session transcript, 2026-10-08 19:43:41 MDT:
“All questions are to be decided with the team. I am going to bed
so won't be available for HIL.”
D-C10r-rulings-14 supplies measurement-driven budget authority.

Historical disposition
Calibration 4 remains terminal HALTED / ZERO_STEP-IDENTITY.
Preserve all historical artifacts and diagnostics unchanged.
The gate failure is established; its numerical cause is not isolated.
No candidate verdict, capacity conclusion, or F1 closure follows.

Criteria
Retain §2.8(ii), (iii), (iii-b), and (iv) unchanged.
No precision-floor replacement, condition-scaled admission bound,
margin epsilon, or ±1 allowance is adopted.
Train–deploy parity does not substitute for recipe-A reduction.

Persistence correction
Retain actual completed and partial records before validating gates.
Use exclusive durable writes and explicit NOT-RUN/incomplete status.
Preserve offending inputs, gate outcomes and cleanup behavior.
Require forced-halt retention and overwrite-refusal regression tests.
Do not backfill historical runs or fabricate missing measurements.

Continuation
This amendment authorizes no calibration 5 or stage-1 dispatch.
Any new diagnostic or redesign requires a separately frozen,
reviewed scope and bounded spend record under team delegation.
Any subsequently admitted calibration uses a fresh namespace,
fresh diagnostic, pinned identities and all required baseline gates.
No diagnostic result retroactively changes calibration 4.
```

Graft: 1 failed call; token savings unavailable.

