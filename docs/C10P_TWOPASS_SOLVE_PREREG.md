# Pre-registration — D-C10p-twopass: does the direction read survive as a weight edit? A second, fresh edit aimed at the target re-solved on the once-edited model (v2 FROZEN, 2026-10-05)

**Status: v2 FROZEN after the Codex gpt-5.5 design pass (`results/c10p_twopass_advisor_v1.md`, FIX-FIRST: same-frame fictional probe, override-hit audit, ΔW-ratio qualifier, stacked supersession wording, two non-claims — all folded). Implementation review next; nothing has run.** Decision-ID `D-C10p-twopass`. Lineage: CORPUS/48 routing (D-C10o-magnitude ⟨D-C10o-magnitude@31389765⟩: DIRECTION), CORPUS/47 (D-C10n-ztransport ⟨D-C10n-ztransport@982edcbd⟩), CORPUS/46 H1 bucket (D-C10m-diag ⟨D-C10m-diag@9a9b5343⟩). Rulings in force: D-C10k-rulings-1 (the strict held-out-paraphrase full-sequence bar binds), D-C10k-rulings-2 (Qwen2.5-3B only), D-C10l-rulings-2.

## 0. Where this sits, and what it is

The first **mechanism arm** since the minted token: a change to what the harness's own solve aims at on the **§C write path**, read against the **§8.9 post-write contract** (held-out paraphrase full-sequence, with the S-3 locality axes). Engine unmodified: the harness's `my_edit` gains one seam (`Z_OVERRIDE`, default `None`, inert; never consulted inside the LAW#5 parity check) that lets the driver supply the target vectors instead of `compute_z`. A PASS here would be a lead on the C10 wall, read strictly by the pre-registered rules; it is not route closure.

## 1. Question and hypotheses

CORPUS/46–48 established, on this harness and in the injection assay, that after the band 4–8 edit the solve's target `z_pre` no longer decodes at the keyed position, that the target re-solved on the edited model (`z_post`) does, and that the difference is its **direction**. The open question is whether that holds as a **weight edit**: if the solve aims at `z_post` from the start, does the edit transfer to held-out paraphrases?

- **H-P1 (two-pass helps):** an edit aimed at `z_post` transfers materially better than the baseline edit (which aims at `z_pre`).
- **H-P0 (null):** aiming at `z_post` does not transfer better — the direction found by injection is not what a weight edit realises (injection and the weight edit remain different interventions, CORPUS/44 F-A3).
- **H-P2 (trade-off):** it transfers better but costs locality (the larger residual `z_post − cur` drives a larger ΔW).

## 2. Design (one process; three passes of the full harness; arms A1, A2, A7; engine unmodified)

Pre-edit: fingerprint (full output); `z_pre` for the 24 A7 requests (harness `compute_z`, layer 8, engine templates), recorded with hashes and norms.

1. **Pass 1 — baseline** (`Z_OVERRIDE = None`): the harness as it stands (LAW#5 gate, arms A1 → A2 → A7, locality axes). The A7 hook (edit applied) computes `z_post` with the same `compute_z` and records the geometry (norms, displacement, cosine; CORPUS/47–48 expect ≈ 20 rotated subjects). The harness restores the base weights.
2. **Pass 2 — sham** (`Z_OVERRIDE = {(subject, target): z_pre}` for the 24 A7 requests): a fresh edit from the base weights aimed at exactly the vectors `compute_z` produced pre-edit. This is the **inertness test of the seam**: it must reproduce pass 1 (same targets, same solve).
3. **Pass 3 — two-pass** (`Z_OVERRIDE = {(subject, target): z_post}`): a fresh edit from the base weights aimed at the re-solved targets. **Binding arm.**
4. **Stacked variant** (second edit applied on top of pass 1's edit) is **not run** in this prereg: it needs the solve's internals inside the hook. This **supersedes** CORPUS/48's "stacked as a reported secondary" for this arm: a NULL here is a result about the *fresh* two-pass edit only and does not test the stacked intervention; stacked is logged as a follow-up if pass 3 reads PARTIAL or better (advisor item 4).
5. **Same-frame locality (CORPUS/43):** every pass's A7 hook probes six never-edited fictional subjects in the `CANON` frame (Vorbanth, Quillexa, Tremnok, Oskavel, Blynthar, Durmquist; none in the edited set) — a flip is a top-1 equal to the first token of any edited value; the pre-edit count is recorded. The real-country half of that probe is the harness's L1 axis.
6. **Seam audit:** the harness counts the `my_edit` calls that took their targets from `Z_OVERRIDE`; the driver resets it per pass and the JSON records it (expected 0 in pass 1, exactly 1 — the A7 arm — in passes 2 and 3), so the sham cannot silently fall back to `compute_z` (advisor item 2).

Every pass carries A1 and A2 (controls), the A7 arm with canon / held-out full-sequence / first-token / string readouts, L1 (12 real countries), the same-frame fictional probe (/6), `described_as`, L3 (30 unedited capitals), generic perplexity, and the per-layer ΔW norms. Output `results/c10p_twopass/pass{1,2,3}.json` + `run.json` (header: `z_pre`/`z_post` hashes, geometry); reader `experiments/track_c/c10p_twopass_read.py`. Runtime ≈ 2 h (three harness passes ≈ 35 min each, two `compute_z` sweeps).

## 3. Pre-registered readings (frozen before implementation; exact counts)

**Validity (any failure → INVALID, no reading):** fingerprint d941a9fb; LAW#5 INERT in every pass; pass 1 A1 ≥ 68/72, A2 ≥ 68/72 and A7 `para_full` inside the identical-baseline envelope [5, 18]/72, canon [5, 10]/24; **sham inertness:** pass 2 A7 `para_full` within ± 5/72 of pass 1 and canon within ± 3/24, with pass 2's per-layer ΔW norms within 5 % of pass 1's (the seam reproduces the engine-target edit); override-hit counts 0 / 1 / 1 for passes 1 / 2 / 3; rotated population (displacement > 0.30) ≥ 12 subjects.

**Locality gates for pass 3 (S-3 axes, all must hold for a gain to count):** A1 ≥ 68/72 and A2 ≥ 68/72; L1 flips ≤ pass 1 + 1; `described_as` ≥ pass 1 − 3; L3 top-1 agreement ≥ 29/30; generic perplexity post ≤ pass 1's post + 0.5; **same-frame fictional flips ≤ pass 1 + 1** (advisor item 1).

**Write-size qualifier (advisor item 3):** the per-layer and total ΔW norms of pass 3 are reported as ratios to pass 1 (the residual `z_post − cur_base` is expected to be larger than `z_pre − cur_base`, so a gain may be a larger write rather than a better-aimed one). If the total ratio exceeds **1.5**, a LEAD or PARTIAL label carries the suffix **-LARGE-WRITE**: a mechanism lead with a write-size caveat, not a route-quality lead (CORPUS/39's warning: stronger writes can keep some controls while failing the binding readout or collapsing controls).

**Binding count:** pass 3 A7 `para_full_n` (/72; the string readout reported beside it must agree within 2 or the discrepancy is reported).
- **LEAD** if pass 3 `para_full` ≥ 30/72 and all locality gates hold (the CORPUS/44 LEAD bar; the first weight-edit arm above it on the coined-coined class would be a real lead, read as "lead, not closure").
- **PARTIAL** if pass 3 − pass 1 ≥ 10/72 and pass 3 < 30/72, locality gates hold.
- **TRADEOFF** if pass 3 − pass 1 ≥ 10/72 but any locality gate fails.
- **NULL** if pass 3 − pass 1 < 10/72 (locality gates reported either way).
Canon is reported beside every count and does not bind (the trained-prompt diagnostic; D-C10e-era lesson).

**What each buys.** LEAD → replicate (second process; the stacked variant; a second seed of nothing — the arm has no seed) and only then a CORPUS/overlay claim as a lead; the lifecycle items (C5/C9) and capacity move up. PARTIAL → the stacked variant and an iterated re-solve (three passes) as the next arm, before I-1. TRADEOFF → report the per-layer ΔW growth; the next arm is a projector/ridge variant of the same two-pass solve, not I-1. NULL → the direction found by injection does not survive as a weight edit on this harness; I-1 OverTone / I-2 forward replay on the engine path are next (CORPUS/46's queue), and CORPUS/48's routing is recorded as falsified for this arm.

## 4. Not claimed, whatever the outcome

No label in CORPUS/44–48 changes. LEAD is a lead, not route closure and not an F1 change (C10 stays OPEN/BLOCKING until the full §8.9 contract and replication). No mechanism about positions or components. The seam is a harness knob, inert at default, demonstrated inert by the sham pass; the engine is untouched. LEAD does not establish same-frame locality beyond the six-subject probe and the L1 axis. A LEAD or PARTIAL with the -LARGE-WRITE qualifier is a mechanism lead with a write-size caveat, not evidence that the direction alone solved the write (advisor item 5).

## 5. Halt discipline and close-out

One speculative fix after a `cat -n` read, then HALT with a diagnostic JSON. Engine, LARQL and git unmodified. Close-out through `tools/closeout_check.py D-C10p-twopass` once the CORPUS entry exists (stamp the source's own IDs before deriving the token). Cross-family gpt-5.5 at the verdict (and at the promote gate if LEAD).

## 6. Reviews

v1 → Codex gpt-5.5 design pass (`results/c10p_twopass_advisor_v1.md`, FIX-FIRST, five items folded) → v2 frozen → implementation review (the seam diff + driver + reader) → run → verdict pass → CORPUS/49.
