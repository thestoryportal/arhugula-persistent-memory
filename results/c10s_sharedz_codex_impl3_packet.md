# Advisor / objective-review prompt (reusable — Claude & Codex)

You are an **independent, adversarial reviewer** of a research step in the LLM-as-Database program. You are not the author. **Do not rubber-stamp.** Your job is to find where the work is wrong, over-claimed, confounded, or drifting from the goal — *before* it is leaned on.

You will be given ONE of: a **test/experiment design** (before it runs), a **finding/result** (before it is declared conclusive or written to CORPUS), or an **approach** the author is about to commit to — together with its evidence (artifact paths + numbers) and the relevant context.

Run this review and answer concisely and specifically:

1. **Real criterion.** Does this answer the question's *actual* criterion, or a flattering adjacent one? (e.g. is the metric matched to the claim — top-1 for read-correctness, distributional for distributional; is the gate's true requirement being met or a softer proxy?)
2. **Confounds & over-claims.** Hunt for confounds, leakage, Goodhart, and over-statement. Is `EVIDENCE-SHOWS` blurred with `I-INFER`? Is "the mechanism works" being passed off as "the contract is met" (**mechanics ≠ contract**)? Is design-viability being passed off as empirical evidence?
3. **Cite or flag.** Every factual claim must cite an artifact (path + exact number) or be labeled **`UNVERIFIABLE`**. Call out any claim that isn't grounded. Verify that external repos/IDs/claims were actually checked before being relied on.
4. **The overturning test.** What is the *cheapest* experiment or control that could **falsify** this finding/design? If it hasn't been run, that is the gap.
5. **Drift check.** Does this advance the F1 readiness determination (or a live §0.3 falsifier)? If not, say so.

**Output:** a short verdict — `PROCEED` / `FIX-FIRST` / `OVERTURNED-OR-RECONSIDER` — then the **single most important thing** to do next, then the specific issues in priority order. Be a skeptic; the author will weigh your input heavily but evidence remains binding over your opinion.


---

# Review packet — D-C10s-sharedz IMPLEMENTATION review, round 3 (2026-10-06): is the round-2 blocker fixed; is the driver run-ready?

Read the four v3 files in full with line numbers (`experiments/track_c/c10s_sharedz_arms.py`, `_inertness.py`, `_read.py`, `_selftest.py`) and your round-2 review (below). Confirm the engine and harness are unchanged against HEAD. Judge: (1) the round-2 blocker — second process permanent and authoritative, UNDERFIT terminal, same-run retry refused, reader honours the recorded outcome; (2) the two qualifications (init exceptions inside the halt boundary; the same-padded-batch diagnostic reference recorded beside the frozen one, HALT unchanged); (3) the naming; (4) anything v3 introduced. Verdict: PROCEED (run-ready; remaining steps are the operator's go and a paused loop) or the single thing to fix. Nothing runs; do not run the code. Keep it short.

## The implementer's v3 report (paths under experiments/track_c/)
1. Permanent second process — `c10s_sharedz_arms.py:627` `R.retry_refusal` halts on any recorded second_process (prints outcome); `:643` writes `second_process = {outcome: STARTED, started_utc, identity, fingerprint, pass1_label}` BEFORE solving; `:651` UNDERFIT terminal (fit numbers kept, no pass2.json, halt non-zero); `:654` COMPLETED after a validated pass 2. Reader `c10s_sharedz_read.py:266–312`: `SECOND_OUTCOMES`, `second_process_state`, `retry_refusal`; `verdict` consults the outcome — UNDERFIT → `<LEAD|PARTIAL>-NOT-REPLICATED` with disposition "candidate not advanced"; STARTED/COMPLETED without pass2 → INVALID (second process); pass2 present but outcome ≠ COMPLETED → INVALID. Tests `c10s_sharedz_selftest.py:188–218`.
2. Halt coverage — `arms.py:112–127`: the model-loading imports sit inside a try/except that writes the HALT diagnostic and exits non-zero; docstring `:27–38`.
3. Inertness (iv) — `c10s_sharedz_inertness.py:89` `reference_nll_padded_batch` (same padded batch, delta = 0, engine loss path) recorded beside the unpadded reference with the three difference maxima (`:144–145`); HALT still on the frozen unpadded reference at 1e-4.
4. Naming — `arms.py:422–430, :453–456`; reader print `read.py:323`.
Self-test: 9 tests pass; engine/harness hashes unchanged.

## results/c10s_sharedz_codex_impl_v2.md (round 2)

**FIX-FIRST.** The single most important fix is to make the second-process attempt permanent and authoritative: record its start before solving, preserve UNDERFIT as a terminal outcome, and prevent an implicit same-run retry.

I read all four v2 files, the frozen design plus A1, round 1, and the specified engine/harness paths. No experiment, self-test, or reviewed code was executed; no files were edited.

The remaining blocker is a **static failure-path counterexample**:

- UNDERFIT records `second_process.outcome = "UNDERFIT"` and exits before creating `pass2.json`. [arms:625](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:625)
- The reader interprets absent `pass2.json` as replication pending, without consulting that outcome. It therefore prints the provisional LEAD/PARTIAL again. [read:312](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_read.py:312), [read:277](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_read.py:277)
- Another `second` invocation checks only whether `pass2.json` exists, then can overwrite `run["second_process"]` with a fresh solve. **I-INFER:** this permits selecting a successful replication while erasing earlier UNDERFIT attempts, contrary to the frozen “candidate not advanced” disposition. [arms:604](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:604), [arms:622](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:622), [prereg:51](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10S_SHARED_Z_PREREG.md:51)

The six round-1 issues:

| # | Judgment | Evidence |
|---|---|---|
| 1 | **FIXED** | Gather → float32 mask → sum → divide matches the engine; the extra numerical KL gate is removed. [read:91](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_read.py:91), [inertness:116](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_inertness.py:116). I accept the expanded per-context reference coverage, with the numerical caveat below. |
| 2 | **FIXED** | Each process supplies its locality gates and write ratio; either ratio above **1.5** qualifies the label. [read:180](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_read.py:180), [read:266](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_read.py:266). |
| 3 | **FIXED** | Pass-2 UNDERFIT halts before `run_pass("2", ...)`. [arms:625](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:625). |
| 4 | **FIXED for the identified paths** | Completed passes undergo immediate validity checking and diagnostic HALT; inertness records persist progressively and on exceptions. [arms:523](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:523), [inertness:138](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_inertness.py:138). Universal coverage remains overstated—see below. |
| 5 | **NOT FIXED completely** | Source comparisons, identity pairing, and occupied-result refusal are implemented. [arms:546](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:546), [read:234](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_read.py:234). Failed second attempts remain overwriteable as described above. |
| 6 | **FIXED for the identified arithmetic/activation errors** | Addition now casts once; canonical reconstruction uses captured `target_init`, with the plain-forward comparison recorded. [arms:327](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:327), [arms:400](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:400). |

The four residual ambiguities:

- **(a) Rebinding: acceptable statically, but not literally invisible to LAW#5.** Its harness-side solve invokes the wrapper; the engine-side solve does not. The wrapper returns the original tensor unchanged, and taking the last `n` captures excludes the earlier gate target. [arms:456](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:456), [arms:472](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:472), [harness:423](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10e_bandknob.py:423). Empirical inertness remains **UNVERIFIABLE without execution**.
- **(b) Capture/control: acceptable with precise naming.** The hook captures `target_init`, not the optimizer’s delta. Canonical delta remains a subtraction-based reconstruction; the shared control uses the actual saved `_delta`. Do not claim demonstrated bitwise recovery of the canonical optimizer delta. [arms:308](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:308), [arms:407](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:407).
- **(c) A `1e-4` HALT would establish gate failure, not necessarily an implementation defect.** The reference still uses individual unpadded forwards against the shared batch. Matching reduction precision does not eliminate forward-shape differences. Preserve the threshold; diagnose any miss with an independent **same-padded-batch, delta-zero** reference before attributing it. [inertness:73](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_inertness.py:73), [inertness:101](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_inertness.py:101).
- **(d) Shared reduction helper: accept.** The operations match engine lines 141–149; moving them into a function does not change the objective. [read:97](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_read.py:97).

One additional qualification: **“every failure writes HALT JSON” is false.** Model-loading imports execute before the bottom-level exception boundary, so initialization exceptions bypass it. [arms:102](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:102), [arms:636](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_arms.py:636).

**Cheapest overturning check, after authorization:** construct a valid pass 1 plus `second_process.outcome="UNDERFIT"` and **no pass2 file**; verify terminal non-advancement and rejection of a same-run retry. The existing UNDERFIT test supplies a completed pass-2 record, which the repaired driver no longer produces on that path. [selftest:171](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10s_sharedz_selftest.py:171).

Repository checks confirmed unchanged engine/harness files against HEAD: Git blobs `5a702dfe173ff8b598d6ebd73bd674d16d9f3ec5` and `8065bf11ce2322be59fb25ec2c4c106701c45ed7`; engine-directory diff empty; `memit_main.py` SHA-256 remains `d941a9fb…8d3d65`.

The work advances the H-1 write-target candidate toward F1. It cannot establish §8.9 or F1 closure, consistent with the [frozen scope](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10S_SHARED_Z_PREREG.md:55).