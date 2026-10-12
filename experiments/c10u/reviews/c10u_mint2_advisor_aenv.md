Verdict: FIX-FIRST

# D-C10u-mint2 Amendment A-env: decorrelated advisor review

Reviewer: Claude Opus 5.5 (`claude-opus-5-5`), Anthropic, acting as the independent second opinion after Codex. Method: `tools/advisor_review_prompt.md`. Read-only review. I wrote no file except this one and ran no model, tokenizer, torch or GPU job. The pure-Python checks imported `c10u_mint2_read.py` and the `c10u_mint2_selftest.py` fixtures, monkeypatched in memory, from the session scratchpad.

**Most important:** the A4 correction is legitimate. Before r2 is pinned, though, the amendment has to make r2 the last attempt, remove a false statement about the schedule, and settle the change A4 makes to the *negative* direction labels. As drafted, the amendment says all readings are "Unchanged", and that claim is false on the newly admissible domain S ∈ [5, 10].

## Answers to the four questions

**Q1: Is this a legitimate correction or goalpost-moving?** It is a legitimate prospective correction. I would not close step 3 because of r1. r1 itself is correctly closed as HALTED under the original contract. Evidence:
- The narrow window was already known to be wrong before r1. A4 calls it "a drafting error" (`docs/C10L_COVGEOM_SPARSEBAND_PREREG.md:117`), and A4's reader fix landed at `2b995b0` (2026-10-05 07:34 MDT). The mint reader line dates from `0cb8ef09`, 2026-10-05 04:17 MDT (`git blame -L 9,9 experiments/track_c/c10l_mint_read.py`). The mint2 prereg was frozen on 2026-10-06 and copied the stale constant anyway (`docs/C10U_MINT2_PREREG.md:77`).
- A4 survived its own pre-declared overturning control: run 3's arm A was 13/72, inside [5, 18] (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:19`). The A4 text that declares this control is `docs/C10L_COVGEOM_SPARSEBAND_PREREG.md:123`.
- Every identical-arm observation recorded after A4 and before r1 lies in [5, 18]: 11 (`CORPUS/45:16`), 15 (`CORPUS/46:10`), 12 (`CORPUS/47:10`), 12 (`CORPUS/48:10`), 13 (`CORPUS/49:10`), 12 (`CORPUS/50:10`) and 16 (`CORPUS/50:30`).
- The old [11, 18] window would have rejected 3 of the 13 pre-r1 identical-arm observations: 10, 8 and 10 (`docs/C10L_COVGEOM_SPARSEBAND_PREREG.md:117`). r1's 10 (`results/c10u_mint2/F_r0_multi_snone.json:1036`) equals two of those earlier values. It is a mis-calibrated guard firing as expected, not a near miss that someone wants waved through.
- The draft does not refit anything to r1. It adopts A4 verbatim, including the tighter para_first upper bound of 59. That keeps the degrees of freedom at zero.

What would make this goalpost-moving is an open-ended right to rerun until something passes. The draft leaves that loophole open (item 1).

**Q2: Is the compatibility rule correct and sufficient?** It is correct for the positive labels, and I verified this against the actual code:
- All four truth-table rows reproduce with `_range_direction` (`experiments/track_c/c10u_mint2_read.py:405–415`) and `_single_label` (`:289–293`) plus the rule:
  - F, S=5, {15, 25, 36} goes from MODIFIER-RECOVERY to MIXED (per-seed labels NULL / PARTIAL / LEAD).
  - V2, S=5, {15, 16, 18} goes from SPAN-DIRECTION to MIXED (NULL / NULL / NULL).
  - F, S=5, {19, 22, 36} gives MODIFIER-RECOVERY.
  - F, S=11, {21, 25, 36} gives MODIFIER-RECOVERY.
- An exhaustive check found the rule changes nothing on the old domain. It covered S ∈ [11, 18], every candidate triple in [0, 72] and four M1 sets, for both blocks: 0 differences.
- The same check found the rule removes every positive-label/NULL-seed coexistence: 57,795 such cases under the current reader, 0 with the rule.

The rule is not sufficient, for three reasons:
- A4 also changes when the negative labels can be reached (item 3).
- The draft's statement about the schedule is false (item 2).
- The draft's plan of "separate constants" would split one rule into two authorities (item 4).

Constant-coupling inventory after the split. Only the line-21 constant and the literal at `:333` carry the window:

| Use | Line | Should become |
|---|---|---|
| `_single_label` | `:290` | `NULL_BAND` (11, 18) |
| replication exclusion (a literal) | `:333` | `NULL_BAND` |
| LAW#3 multi guard | `:377` | A4 |
| V2 screen, all three keys | `:421` | v3 numbers |
| proposed compatibility rule | (new) | `NULL_BAND[1]` |

The control trigger (`stage_plan`, `:549`) reads `raw_direction`. It follows the new rule only if the rule lives inside `_range_direction`. No other module uses `ENVELOPE`: grep over `experiments/track_c/c10u_mint2_*.py tools/*.py` hits only `c10u_mint2_read.py:21, :290, :377, :421`, plus the literal at `:333`.

**Q3: Is the bookkeeping fix correct?** Yes. Emitting lists at `:402` fixes both `missing` and `replication_missing`, because `:456` copies `b["missing"]` from the same function. Keeping `write_json` strict (`experiments/track_c/c10u_mint2_arms.py:45–54`) is right.

I serialised a stage-completion record, built exactly as at `arms.py:1027–1031`, over 11 fixture scenarios:
- reproduce-only
- frozen-partial
- complete F, with and without a replica
- F with a partial replica
- complete V2
- V2 PENDING-CONTROL
- V2 with controls
- HALT-LAW3
- NOT-COMPARABLE
- empty

Only three failed the round-trip: reproduce-only, frozen-partial and partial-replica. Every failure was a tuple in `missing` or `replication_missing`. I found no tuple keys, sets, non-string dict keys or other non-native values in any scenario. The draft's test must cover `replication_missing` as well (item 7).

**Q4: Over-claims and inconsistencies.** See items 2, 3, 6 and 9 below.

## Issues

### 1. BLOCKING: no stopping rule for attempts

The draft forbids widening the window further. It does not forbid an r3. Without that, "attempt until a guard passes" stays open, which is the garden of forking paths that LAW#3 exists to stop. `CLAUDE.md` halt discipline allows "AT MOST ONE speculative fix … If that fix does not clear the gate, HALT". A-env *is* that fix.

Add to the end of the "r1 stays HALTED" paragraph:

> **r2 is the last attempt under D-C10u-mint2.** A-env is the program's one fix for this gate. If r2 misses any LAW#3 gate (the mint-1(frozen) per-seed windows, the median ≥ 30 rule, or the A4 multi guard, in block F or its replication), D-C10u-mint2 closes as HALTED with both attempts reported. There is no r3 and no further guard or reader change unless a new operator ruling is recorded in runbook §5 before any r3 data exists. r2's own block-F A7-multi is the pre-declared overturning test of A4 on this harness: a miss means A4's "known spread" story does not hold here, and that miss is reported as such.

### 2. BLOCKING: false statement about the schedule

Change 3 says: "The conditional schedule … follows the direction after this rule, so an all-NULL block triggers no control or replication." That is false for replication, for two reasons:
- **Replication is triggered by any arm labelled LEAD or PARTIAL, including the mint-1 reference arms** (`c10u_mint2_read.py:476–481`, through `run_reading`'s `pending` at `:328`). The LAW#3 gate (`:369`) and the V2 screen (`:421`) both require a mint-1 median ≥ 30. That means at least two LEAD mint-1 seeds in every block that gets as far as the schedule.
- **A negative direction is set to PENDING-REPLICATION** (`:504–505`). This matches the prereg, which requires a replication for PAIR-DIRECTION and NO-MODIFIER-GAIN (`docs/C10U_MINT2_PREREG.md:96`, `:101`, `:78`).

Simulated with the A-env reader (A4 at `:377`, NULL band kept, compatibility rule in `_range_direction`):

| Block | S | Candidates | Per-seed labels | Direction | Replication runs |
|---|---|---|---|---|---|
| F | 5 | {15, 16, 17} | all NULL | MIXED | `stage_plan("replicate-F")` returns 7 runs |
| F | 11 | {12, 13, 14} | all NULL | NO-MODIFIER-GAIN → PENDING-REPLICATION | 7 runs |
| V2 | 11 | {12, 13, 14} | all NULL | — | control 0, replicate-V2 7 runs |

The budget ruling already expects this ("expects replication to trigger in practice (≈ 28 runs)", `EXPERIMENT_RUNBOOK.md:341`).

Replace that sentence with:

> The matched 48-row control is triggered by `raw_direction == SPAN-DIRECTION` (`c10u_mint2_read.py:549`), and the rule is applied inside `_range_direction`, so a block whose candidate seeds include a NULL seed never triggers the control. Replication is unaffected by this rule. It is triggered by any LEAD or PARTIAL arm, including the mint-1 reference arms that the median ≥ 30 rule makes LEAD in practice (`:476–481`), and by any non-MIXED direction, negative ones included (`:504–505`). So both replication blocks are expected to run (≈ 28 runs, `EXPERIMENT_RUNBOOK.md:341`).

### 3. BLOCKING: A4 silently changes the negative labels; the "Unchanged" list is false

On the old domain (S ≥ 11), three NULL candidate seeds always read PAIR-DIRECTION or NO-MODIFIER-GAIN, because max ≤ 18 implies max − S ≤ 7 < 10. On S ∈ [5, 10], a candidate set whose maximum lies in [S + 10, 18] has three NULL seeds but reads **MIXED**. Example: S = 5, MO = {15, 16, 17}. The exhaustive count is 1,715 candidate triples per block for S ∈ [5, 10], and 0 for S ≥ 11.

So lowering the admissible S changes routing on the negative side as well. The draft discusses only the positive side, and then lists "the +10 gain … halt discipline" as unchanged. The frozen prose for NO-MODIFIER-GAIN, "no seed gains the PARTIAL margin over the string" (`docs/C10U_MINT2_PREREG.md:101`), is also ambiguous here: a seed at 16 with S = 5 has gain 11, yet `_single_label` labels it NULL.

**Recommended fix (mirror of the positive rule).** Add to change 3:

> **Negative-direction compatibility rule (new, routing only).** PAIR-DIRECTION (V2) and NO-MODIFIER-GAIN (F) are issued if max(candidate) − S < 10 **or** max(candidate) ≤ 18, the top of the NULL interval, in the block and in its replication block. Why: on S ≥ 11 the second clause is implied by the first, so nothing changes on the old domain. On S ∈ [5, 10] it keeps the frozen meaning, "no seed is advanced", when every seed is NULL by the interval rule. Truth table (counts only, gates clean): F, S = 5, MO = {15, 16, 17} → NO-MODIFIER-GAIN (MIXED without this rule); F, S = 5, MO = {12, 14, 19} → MIXED (19 − 5 = 14 ≥ 10 and 19 > 18, so neither clause holds; per-seed labels NULL / NULL / PARTIAL; this row shows the clause does not absorb a seed above the NULL interval); F, S = 11, MO = {12, 13, 14} → NO-MODIFIER-GAIN, as before.

I verified the clause exhaustively for S ∈ [5, 18], every triple in [0, 72]:
- `max − S < 10 or max ≤ 18` holds exactly when all three seeds are NULL under `_single_label` (assertion held on every case).
- 0 differences from the current rule for S ≥ 11.
- 0 overlap with the positive labels after the item-2 rule.

**Acceptable alternative** if the program will not add a rule: keep the frozen formula and state plainly in A-env that "on S ∈ [5, 10] a block whose three candidate seeds are all NULL reads MIXED, not PAIR-DIRECTION / NO-MODIFIER-GAIN, whenever max(candidate) ≥ S + 10". Then delete "the +10 gain" from the "Unchanged" list, or qualify it. Either way the choice must be explicit and frozen before r2.

### 4. BLOCKING: "separate constants" would split one rule into two; the rule's location matters

Change 2 says "In code these are separate constants." Items (b) and (c) are one rule, the NULL interval, applied at first reading and at replication. Giving them two constants creates two authorities that can drift apart. The compatibility rules of item 3 must read that same constant, not a literal 18.

Replace the last sentence of change 2 with:

> In code: `LAW3_MULTI_F = {"para_full_n": (5, 18), "canon_full_n": (5, 10), "para_first_n": (42, 59)}`, used only by `reproduction_gate` (`c10u_mint2_read.py:377`); `V2_SCREEN = {"para_full_n": (11, 18), "canon_full_n": (5, 10), "para_first_n": (48, 62)}`, used only by `_comparability` (`:421`); `NULL_BAND = (11, 18)`, used by `_single_label` (`:290`), by the replication exclusion (`:333`, which replaces the literal `11 <= … <= 18`), and by both compatibility rules as `NULL_BAND[1]`. Both compatibility rules sit inside `_range_direction`, so `raw_direction` (`:472`, read by `stage_plan` at `:549`) and the replication block's direction (`:471`, compared at `:506`) carry them. `ENVELOPE` is removed.

Tests required before r2, beside the round-trip test of item 7, in `c10u_mint2_selftest.py`. This follows the precedent `test_modifier_recovery_truth_table_frozen_at_v3`, selftest `:385–392`.
- (i) Every A-env truth-table row of change 3 and item 3, run through `block_reading` with a replication block.
- (ii) A4 boundaries for the F multi in both replicates: para_full 4/5/18/19, canon 4/5/10/11, para_first 41/42/59/60.
- (iii) V2 screen boundaries unchanged: para_full 10/11/18/19, para_first 47/48/62/63.
- (iv) The old-domain equivalence (S ∈ [11, 18]: directions identical with and without both rules).

The existing test at selftest `:330–332` (multi 11 passes, 19 fails) remains valid under A4.

### 5. ADVISORY (reviewer disagreement with Codex, for the operator): the V2 screen keeps a floor the amendment itself calls mis-derived

Codex recommends keeping V2's screen at the v3 numbers (`results/c10u_mint2_codex_envelope.md:65`), and the draft follows. I disagree, mildly, for two reasons.

First, no V2 data exists in r1. Changing V2's screen now is *fully* prospective, so it is cleaner than the block-F change.

Second, a NOT-COMPARABLE result suspends the V2 direction reading (`c10u_mint2_read.py:487–492`). V2 is arm A's span question, the main science of step 3. The frozen v3 numbers trace to the same stale source (`docs/C10U_MINT2_PREREG.md:77–78`, "the same envelope"). On the frozen stimuli, the [11, 18] floor rejected 3 of 13 identical-arm observations. Replication is effectively always triggered (item 2), so two V2 multi runs must both pass (`:487`). **I-INFER**: if the V2 baseline has a similar spread (UNVERIFIABLE, since V2 has different heads), roughly 1 − 0.77² ≈ 40 % of r2s lose the V2 direction to a guard already documented as mis-derived.

Codex's counter-argument is real: V2's screen is a comparability screen, not a reproduction guard, and A4's evidence comes from the frozen stimuli. With items 3 and 4 in place, the label semantics would stay safe if the V2 screen also took A4.

**Operator choice**, either:
- (a) keep the v3 numbers and add to change 2(a): "expected cost: on the frozen-set spread, ≈ 1 in 4 V2 multi runs falls below 11; a V2 NOT-COMPARABLE outcome in r2 is reported with this caveat"; or
- (b) set `V2_SCREEN := A4` as a declared comparability-scope change, with its own sentence of rationale, made before any V2 data exists.

My lean is (b), but this is a genuine fork. Codex and I disagree, which is itself a signal to surface rather than resolve silently.

### 6. ADVISORY: justification omits the strongest evidence; para_first edge risk is not disclosed

**Add to "Why", after "carried in CORPUS/46–49":**

> A4's own pre-declared overturning control passed: run 3's arm A was 13/72 (`CORPUS/44:19`; declared at `docs/C10L_COVGEOM_SPARSEBAND_PREREG.md:123`). Every identical-arm observation recorded after A4 and before r1 lies in [5, 18]: 11, 15, 12, 12, 13, 12 and 16 (`CORPUS/45:16`, `46:10`, `47:10`, `48:10`, `49:10`, `50:10`, `50:30`). The [11, 18] window would have rejected 3 of the 13 pre-r1 identical-arm observations.

**Disclose the para_first edge:**

> The original mint multi's para_first was 59 (`results/c10l_mint/arm_multi.json:253`), exactly A4's upper bound. A para_first of 60–62 in r2 halts, although the v3 window would have passed it. This is accepted, not refitted.

**State the effective-floor consequence:**

> In block F, S may now be as low as 5. With the compatibility rule, the lowest candidate count that can carry MODIFIER-RECOVERY falls from 21 to 19. S is reported beside every gain.

### 7. ADVISORY: round-trip test scope

Extend change 4 to read: "…emitted as JSON lists (`c10u_mint2_read.py:402`: `sorted([str(k), str(s)] for k, s in …)`), which fixes both `missing` and `replication_missing` (`:456`)." The test must include a stage-completion record with:
- a partial initial block (reproduce stage);
- a complete initial block with a partial replication block (this exercises `replication_missing`);
- a complete V2 block with controls;
- a HALT-LAW3 reading.

Each record goes through the real `write_json` into a temporary directory. My 11-scenario check found nothing else that is non-native.

### 8. ADVISORY: the r2 procedure would truncate r1's committed stage logs

The stage wrapper used for r1, `/Users/robertrhu/.claude/jobs/4d71207f/tmp/run_c10u_stage.sh:9–11`, has two problems for r2:
- It passes no `--out-dir`, so the driver defaults to `results/c10u_mint2` (`experiments/track_c/c10u_mint2_arms.py:1076`).
- It redirects with `>` to `results/c10u_mint2_logs/$STAGE.log`.

A naive r2 launch therefore truncates r1's `reproduce.log` and `frozen.log`, both committed and cited at `SESSION_CHECKPOINT.md:26`, *before* the driver refuses on the changed source identity (`:138–140`).

Add to "r2 procedure":

> Every r2 stage runs with `--out-dir results/c10u_mint2/r2` and writes its stage log under `results/c10u_mint2_logs/r2/`. No r1 file is opened for writing.

### 9. ADVISORY: forward pointers in the frozen text, and the cost the operator will be quoted

- Prereg `:3`: amend the status line to "v3 FROZEN (2026-10-06) + Amendment A-env (2026-10-07, §8)".
- Prereg `:77`: append "(block F: superseded by §8 A-env for attempt r2)" after the literal window and its `c10l_mint_read.py:9` citation.
- Prereg `:78`: change "inside the same envelope" to "inside the v3 window [11, 18] / [5, 10] / [48, 62]", or to the item-5 choice.

Without these pointers, a reader of §2 applies the old window.

Also, `SESSION_CHECKPOINT.md:27` quotes the rerun as "~6 h". The budget ruling puts the first 14 runs alone at 14–17 h, about 28 runs in total (`EXPERIMENT_RUNBOOK.md:341`). Correct the figure before the operator's yes/no.

## Overturning test and drift

- **Cheapest falsifier of the A4 premise.** r2's own block-F A7-multi, read under A4, pre-declared (item 1). No separate control is needed.
- **Drift.** Step 3 is a diagnostic lead, not a §0.3 falsifier (`docs/C10U_MINT2_PREREG.md:9`). A-env repairs the instrument and routing. It is not evidence for the F1 determination, and it changes no CORPUS/44–53 label (`:111`).
