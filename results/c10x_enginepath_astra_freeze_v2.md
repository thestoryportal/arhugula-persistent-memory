**FIX-FIRST.** Add enforceable stage budgets first; §2.7 currently explicitly supplies estimates, not deadlines.

References below are to [the v2 preregistration](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10X_ENGINEPATH_PREREG.md). All 13 v1 BLOCKING requests have substantive body changes; none is merely changelogged. The remaining partial fixes concern classification validity, numerical transcription and reduction acceptance.

**BLOCKING**

1. **No hard budgets or pre-start refusal** (§2.7, lines 107–117). The requested freeze condition is absent. Proposed replacement—these are spending limits, not measured runtimes:

   > Hard wall-clock caps, in minutes: setup/import/preflight 10; recipe A 34; target construction 40; inertness and independent audits 50; injection 25; I-2 recipe 34; I-1 recipe 34; final verification/serialization 13. Every operation, including hashing, restoration and diagnostic capture, belongs inside its stage cap. Each process is capped at 250 minutes; two processes at 500 minutes.  
   > Before starting each stage, record its projected duration. Initially use its stated cap; when comparable timings exist, use the larger of that allowance and the projection from the slowest measured comparable work units, including remaining overhead. Refuse the stage if its projection exceeds its cap or the remaining process budget after reserving subsequent stages. Recheck before each work unit. An independent watchdog enforces stage and process deadlines, including blocked native calls. Projection refusal or timeout yields HALTED/incomplete, never NULL; no subsequent stage runs and no cap is extended in-run. Process 2 uses the same rules and incorporates process-1 measured timings.

2. **I-1 can inherit the FE dispatch state** (§2.2 line 44; §2.7 line 103). Dispatch selects FE whenever `FE_STATE` remains set; the I-1 instruction sets only `Z_OVERRIDE`. Counters would catch this after wasted execution. Replace the recipe-state instructions with:

   > Immediately before every recipe, explicitly assign both states: A = `(FE_STATE=None, H.Z_OVERRIDE=None)`; I-2 = `(FE_STATE=the frozen FE state, H.Z_OVERRIDE=None)`; I-1 = `(FE_STATE=None, H.Z_OVERRIDE=the frozen OverTone table)`. Reset both recipe counters then. Restore both states to `None` in `finally`, including after standalone checks, and verify W0 before proceeding.

3. **Validity rejects legitimate undefined diagnostics** (§3 line 127). The unchanged evaluator intentionally returns `tf_pertok_cont=None` when there are no continuation tokens—necessarily A1—and `cond_full_given_first=None` when first-token hits are zero ([harness lines 391–392](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10e_bandknob.py:391)). Thus advisor #4/Codex #4’s classification repair remains operationally incomplete. Replace “no missing or non-finite datum” with:

   > Every required field is present and every applicable numeric datum is finite. Preserve `tf_pertok_cont=null` iff its recorded continuation-token denominator is zero, and `cond_full_given_first=null` iff `para_first_n=0`; record an explicit zero-denominator reason. These diagnostic nulls do not invalidate an arm. Any other missing value, unexpected null, NaN or Inf is INVALID. All binding gates require defined finite inputs.

4. **Reduction acceptance has contradictory boundaries** (§2.4 line 71; §7 line 197). “Within tolerance” permits nonzero error ≤1e-4, while “any resulting distance fails” and “bit-exact by construction” prescribe exact equality. The Codex #16 fold is only partial. Replace those clauses with:

   > X1-(ii) passes iff every nonzero-reference returned-z relative error is ≤1e-4, the measured floor is ≤1e-5, and step counts agree exactly. Zero references require exact equality. An exactly-zero engine CE receives the declared constant clip branch; any resulting difference is judged by these same predicates. Bit-exactness is an expectation, not a separate acceptance requirement or a proven consequence of the algebra.

5. **The active objective still permits two precision transcriptions** (§2.3 lines 53–54). “Logits … in float32” can mean casting the engine’s computed logits or recomputing the head projection in fp32; the source uses the former engine-dtype projection before `log_softmax` ([compute_z.py:140](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/compute_z.py:140)). This leaves Codex #14’s declared-arithmetic audit underspecified. Replace with:

   > Compute `raw_logits = ln_f(full_repr) @ lm_w + lm_b` once in the engine dtype, then `log_probs = torch.log_softmax(raw_logits, dim=2)` exactly as the engine. Factoring line 140 to name this intermediate changes no arithmetic. Construct detached targets from `raw_logits[scored_mask].detach().float()`. In `extra`, use the differentiable `log_probs[scored_mask].float()`; cast the completed extra term once to `ce.dtype` before addition and clipping. Do not recompute a fp32 head projection or fp32 log-softmax for the optimization objective. The independent audit reproduces these operations and casts.

**ADVISORY**

- **LAW#3 is repaired:** recipe A precedes candidate construction, with inclusive `[5,18]`, `[5,10]`, `[42,59]` and A1/A2 ≥68/72 (§2.7:99; §3:129; `CORPUS/44:39`). The base-class predicates partition all **2,044** enumerated baseline/count/locality cases; both injection tables partition all **145** possible integer deficits. This was model-free predicate verification.
- **LAW#5 coverage is materially repaired:** W0, active singleton reduction, multi-layer null/observer checks and G8 are in the body (§2.4:67–81). Their empirical passage remains **UNVERIFIED**.
- **Write-only verdict: WRITE-QUALIFIES, by design.** Both arms optimize a temporary hidden vector, install persistent weight updates through the harness’s closed-form solve, and use ordinary greedy model inference for binding recall. No prompt-time retrieval or intervention is specified for that readout (`compute_z.py:83,104–105`; `c10e_bandknob.py:209–217,108–117`). Precisely, this is the projected-ridge **harness** solve, not unchanged MEMIT’s covariance-regularized solve (`memit_main.py:200–206`). Effectiveness and §8.9/F1 closure remain unproven.
- Remove causal parentheticals from interpretation rows 2–3: neither a failed control nor excessive write size alone establishes “clip underfits” or “front-loading costs locality.” Also define—or delete—the unspecified “spread … across six context-templated prompts” diagnostic (§2.2:42), and state that replication’s control/locality/qualifier requirements apply **per candidate**, not jointly across both candidates (§3:150).

Read-only review; no model execution. Exact runtime model ID and configured effort are **UNVERIFIABLE** here. Graft: one failed invocation; savings unreported.

