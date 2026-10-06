# Pre-registration — D-C10q-stacked: the stacked two-pass solve — a second edit applied on top of the first, aimed at the target re-solved on the once-edited model (v2 FROZEN, 2026-10-06)

**Status: v2 FROZEN after the Codex gpt-5.5 design pass (`results/c10q_stacked_advisor_v1.md`, FIX-FIRST: second-write qualifier, projector confound named, handle inertness in the implementation review, two non-claims, matched-energy permuted-target control added as pass S-perm — all folded). Implementation review next; nothing has run.** Decision-ID `D-C10q-stacked`. Operator instruction 2026-10-06 ("Run the stacked variant"), recorded as **D-C10q-rulings-1** with its companion: before the program leaves Qwen2.5-3B for any reason, an exhaustive research pass (paper and code repositories, then InfraNodus and other science-grounded agentic tools) surfaces every candidate solve. Lineage: CORPUS/49 (D-C10p-twopass ⟨D-C10p-twopass@12f87dc3⟩: fresh two-pass NULL at the margin; stacked untested by §2.4), CORPUS/48 (D-C10o-magnitude ⟨D-C10o-magnitude@31389765⟩). Rulings in force: D-C10k-rulings-1 (strict held-out bar binds), D-C10k-rulings-2, D-C10l-rulings-2.

## 0. Where this sits, and what it is

The second and last member of the "re-aim the target" family on the **§C write path**, read against the **§8.9 bar**. CORPUS/49 showed a *fresh* edit aimed at `z_post` gains 8/72 with a ×1.31 write. The stacked variant keeps the first edit in place and adds a second edit aimed at `z_post` on top: the second solve sees the once-edited model's own keys and covariance cache (sequential editing), which is the setting in which `z_post` was solved. Engine unmodified; the harness gains one more seam (a handle to the current arm's solve state, so a hook can apply a second edit) beside `Z_OVERRIDE`.

## 1. Question and hypotheses

- **H-Q1 (stacked helps):** the second, in-place edit aimed at `z_post` transfers materially better than the single edit.
- **H-Q0 (null):** it does not; the re-aim family is exhausted as a harness-side fix and the engine-path arms follow.
- **H-Q2 (trade-off):** it transfers better but two edits cost locality or controls.
- **Sham expectation (control):** a second in-place edit aimed at `z_pre` again should add almost nothing (the first edit already realises `z_pre` at the keyed position to ≈ 3 %, CORPUS/44 step 0), so its ΔW should be small and its readouts ≈ the single edit. A sham that moves the readout materially means "a second edit" rather than "a new target" is doing the work.

## 2. Design (one process; three full harness passes; arms A1, A2, A7; engine unmodified)

Pre-edit: fingerprint (full output); `z_pre` recorded. Harness seam: `run_recipe` publishes the current arm's solve state (`hp`, `P`, the arm's covariance cache, the pre-edit locality baselines) to a module-level handle before `my_edit`; the A7 hook may call `my_edit` once more with `Z_OVERRIDE` set and re-evaluate (`eval_arm` + the locality axes) while the first edit is still applied. Both passes run the harness's own LAW#5 gate and A1/A2 first.

1. **Pass S — stacked (binding):** the standard A7 edit (baseline readout, recorded as this pass's own single-edit reference), then in the hook: re-solve `z_post` on the edited model; second `my_edit` aimed at `z_post` with the first edit in place and the first edit's keys in the cache; full re-evaluation (canon, held-out full-sequence, first, string, L1, same-frame fictional, `described_as`, L3, perplexity) and the second edit's per-layer ΔW.
2. **Pass S-sham:** identical, but the second edit is aimed at `z_pre` (the same targets the first edit used). This is a **near-no-op seam control** (the first edit already realises `z_pre`), not a magnitude-matched control.
3. **Pass S-perm (matched-energy negative control, advisor's overturning test):** identical to S, but the second edit is aimed at the re-solved targets **permuted across subjects** (a fixed derangement: subject *i* receives `z_post` of subject *i + 1* in `FICTION` order, the last receives the first). The second write's energy matches S's; the targets are semantically wrong. If S-perm also improves, "new target" is overturned.

**Confound named (advisor item 3):** the second solve uses the once-edited model's keys and the arm's cache (which already holds the first edit's K Kᵀ — sequential editing), but the AlphaEdit null-space projector `P` is computed once from the **base** covariance and reused; this is "edited-model keys under a base-covariance projector", not a fully re-estimated edited-model solve.

The order of the three passes is fixed (S, S-sham, S-perm). Output `results/c10q_stacked/{passS,passSsham,passSperm,run}.json`; reader `experiments/track_c/c10q_stacked_read.py`. Runtime ≈ 2.2 h.

## 3. Pre-registered readings (frozen before implementation; exact counts)

**Validity (any failure → INVALID):** fingerprint d941a9fb; LAW#5 INERT in both passes; single-edit references in both passes with A1 ≥ 68, A2 ≥ 68, A7 `para_full` in [5, 18] and canon in [5, 10]; the two single-edit references within ± 5/72 of each other (same process; a wider gap means the pass structure is not stable); override consumed exactly once per pass (the second edit) and never by the first; rotated population ≥ 12.

**Sham control (binds the reading's scope):** S-sham's stacked readout within ± 5/72 of its single-edit reference **and** its second-edit total ΔW ≤ 0.25 × the first edit's. If the sham moves the readout by more than 5 or writes more than a quarter of the first edit, the S result is reported with the label suffix **-SHAM-ACTIVE** (a second edit alone does something; the new-target reading is not separable in this process).

**Locality gates for pass S (stacked vs its own single-edit reference):** A1 ≥ 68 and A2 ≥ 68 after the second edit; L1 flips ≤ reference + 1; same-frame fictional flips ≤ reference + 1; `described_as` ≥ reference − 3; L3 ≥ 29/30; generic perplexity ≤ reference + 0.5.

**Binding count:** pass S stacked A7 `para_full` /72 (string readout beside it).
- **LEAD** if ≥ 30/72 and all locality gates hold.
- **PARTIAL** if gain over the single-edit reference ≥ 10/72 and < 30, gates hold.
- **TRADEOFF** if gain ≥ 10 but a gate fails.
- **NULL** if gain < 10.
**Write-size qualifier (advisor items 1–2):** the direct confound is the second write itself: **‖ΔW₂‖ / ‖ΔW₁‖** (summed over layers) is reported for every pass; for pass S a ratio above **0.75** (the second edit rivals the first) adds **-LARGE-WRITE**; the total ratio is reported, not bound. Expected: S-sham ≤ 0.25 (its residual is nearly spent); a target-specific second write sits between.

**Target-specificity control (pass S-perm):** if S-perm's stacked gain over its own single-edit reference is ≥ 0.5 × S's gain (and S's gain ≥ 10), the label carries **-NOT-TARGET-SPECIFIC** (a second write of matched energy, aimed wrong, does as much). S-perm's locality axes are reported beside it.

**What each buys.** LEAD → replicate in a second process; then the lifecycle items and a CORPUS/overlay claim as a lead, not closure. PARTIAL → an iterated variant (third pass) with the write size capped is the one remaining harness-side arm before the engine path. TRADEOFF → report; the engine-path arms next. NULL → the re-aim family is exhausted on this harness: I-1 OverTone / I-2 forward replay (engine path, LAW#5 discipline) are next, under the research-pass ruling before any model change.

## 4. Not claimed, whatever the outcome

No label in CORPUS/44–49 changes. LEAD or PARTIAL is a harness-side mechanism lead only — not §8.9 contract closure (the contract is behavioural post-write readback across the whole surface; this is one write-path arm), not route closure, not an F1 change. No mechanism about positions or components. Two seams are harness knobs, inert at default; the implementation review must show the solve-state handle is read-only by default and leaves no-hook output unchanged (the single-edit references here must sit inside the identical-baseline envelope, and the C10p pass-1 baseline is the no-handle comparator). An inactive S-sham does not prove the gain is target-specific under matched write magnitude — only S-perm addresses that. The engine is untouched.

## 5. Halt discipline and close-out

One speculative fix after a `cat -n` read, then HALT with a diagnostic JSON. Close-out through `tools/closeout_check.py D-C10q-stacked` once the CORPUS entry exists (stamp the source's own IDs before deriving the token). Cross-family gpt-5.5 at the verdict and at the promote gate if LEAD.

## 6. Reviews

v1 → Codex gpt-5.5 design pass (`results/c10q_stacked_advisor_v1.md`, FIX-FIRST, folded incl. pass S-perm) → v2 frozen → implementation review (seam diff + driver + reader; handle inertness) → run → verdict pass → CORPUS/50.
