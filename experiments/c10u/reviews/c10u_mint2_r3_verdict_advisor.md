FIX-FIRST

# D-C10u-mint2 r3 final verdict: independent adversarial review

- **Reviewer:** Claude Opus 5.5 advisor subagent (not the author; read-only; no GPU, no model load)
- **Date:** 2026-10-07
- **Reviewed:** the r3 verdict in the packet `c10u_r3_verdict_packet.md`; the deviation note §8.1 (`docs/C10U_MINT2_PREREG.md:187–256`, commit `3e6772d`); the reading `results/c10u_mint2/r3_read_after_replicateF.json` (READ); the records and logs under `results/c10u_mint2/r3/` and `results/c10u_mint2_logs/r3/`; the r1 and r2 records for comparison.

**Single most important thing to do next.** Before CORPUS gets the line "Block F = ROUTING-BLOCKED-UNDERFIT", add the fact that blocks its natural reading. The A7-multi(frozen) reference fails the same P3 admission screen that blocked the modifier-only arm: 17/24 aggregates ≥ 0.98 in r3, the same count as modifier seed 0 (B1). The label is still what the pinned reader yields. But block F tells us nothing about whether modifier-only fits worse than the plain string, and CORPUS must not read it that way.

## What I checked myself (records opened, not taken from the packet)

| Claim | Where I read it | Value | Matches? |
|---|---|---|---|
| Reader pin | `shasum -a 256 experiments/track_c/c10u_mint2_read.py` vs `r3/identity.json` `source_sha256` | `1223789a…` both | yes |
| Prereg pin, before §8.1 was appended | `git show 3e6772d~1:docs/C10U_MINT2_PREREG.md \| shasum` vs identity | `c54f443c…` both; HEAD `a2f181a0…` (§8.1 was appended, and `git diff` shows lines were only added after :186) | yes |
| A7-multi(frozen) r3 | `r3/F_r0_multi_snone.json` `arm.para_full_n` / `canon_full_n` / `para_first_n` | 14 / 8 / 53 | yes |
| mint-1(frozen) binding | `r3/F_r0_mint1_s{0,1,2}.json` `arm.para_full_binding_n`; `step0.recall_n` | 46 / 37 / 40; recall 0 for each | yes |
| Modifier admission | `r3/F_r0_modifier_s{0,1,2}.json` `admission.P3.n_ge_0.98`; `outcome`; `pid` | 17 / 13 / 14; UNDERFIT; null | yes |
| Modifier s0 underfit indices, r2 vs r3 | `r2/step0/F_r0_modifier_s0.json` and `r3/F_r0_modifier_s0.json` `admission.P3.underfit` | [1,5,8,12,13,16,20] vs [7,8,12,13,17,20,22] | yes |
| r1 modifier records re-read r0's step 0 | `r3/F_r1_modifier_s*.json` `step0_file` | `…/r3/step0/F_r0_modifier_s*.json` | yes |
| V2 multi | `r3/V2_r0_multi_snone.json` `arm.*` | 31 / 24 / 49 | yes |
| V2 mint-1 / mint-2 | `r3/V2_r0_mint1_s*.json` binding; `r3/V2_r0_mint2_s0.json` binding; `V2_r0_mint2_s{1,2}.json` `admission.P3.n_ge_0.98` | 51/46/38; 30; 20, 21 | yes |
| Replica bit-identical | My own leaf-by-leaf diff of every `r3/F_r0_*` against `r3/F_r1_*` | multi 3,706 leaves, mint-1 6,424 each, modifier 3,443/3,447/3,446. Only `/pid`, `/replicate` and `/when_utc` differ (modifier: only `/replicate`) | yes |
| Cross-attempt mint-1(frozen) | `F_r0_mint1_s*.json` in `results/c10u_mint2/`, `r2/` and `r3/` | r1 40/36/41, r2 34/35/37, r3 46/37/40; multi 10/10/14; ctx `aa476792`/`dd73fdc9`/`8638d12c`; `provenance.row_pairing.rows_sha256` `2c1d09e7`/`f50f9ea5`/`9d5cc3c8` in all three | yes |
| p4-save refusal | `results/c10u_mint2_logs/r3/p4-save.log:1–2`; diagnostic `reason`; no `p4save_*` or `edited/` in `r3/` (`ls`) | "HALT: P4 requires replicated LEAD/PARTIAL …", STAGE_EXIT=1 | yes |
| replicate-F finished | last line of `results/c10u_mint2_logs/r3/replicate-F.log` | `STAGE_EXIT=0` | yes |
| Reader-fix commit vs r3 start | `git show -s afbf8e9` vs `r3/reproduce_started.json` `when_utc` | 10:01:24 MDT = 16:01:24 UTC vs 16:01:40 UTC | yes |

### One label recomputed by hand: `mint1_s2` (block F, r3)

I applied the pinned rule (`c10u_mint2_read.py:122–131` gates, `:341–345` `_single_label`, `:380–392` replication) to the raw fields of `r3/F_r0_mint1_s2.json` (candidate) and `r3/F_r0_multi_snone.json` (reference):

- count = `arm.para_full_binding_n` = 40 (= `para_full_n` 40 − `step0.recall_n` 0). 40 is outside NULL_BAND [11, 18] and ≥ LEAD_MIN 30, so the provisional label is LEAD.
- L1: candidate `L1_flipped_to_edited_value` 0 ≤ ref 0 + 1, and `L1_minted_n` 0, so it passes. same_frame: 0 ≤ 1 + 1, and `frame_minted_n` 0, so it passes. described_as: 92.17 ≥ 88.22 − 3, so it passes. L3: 30 ≥ 29, and `L3_minted_n` 0, so it passes. cannibal 0 ≤ 2 and sibling 0 ≤ 3, so both pass.
- generic_ppl: `generic_ppl_post` 22.074 ≤ 21.522 + 0.5 = 22.022 is **false**.
- Not clean, so LEAD becomes **TRADEOFF**. TRADEOFF is not in {LEAD, PARTIAL}, so no replication suffix is added. Hand result **TRADEOFF** = READ `F.arms.mint1_s2.label`. ✔

I did the same for `mint1_s0` and `mint1_s1`. Their ppl posts are 21.767 and 21.91, both ≤ 22.022, and every other gate passes. Their replicas are DONE with binding ≥ 30 and every gate passing (`:388`), so both are **LEAD**. ✔ Seed 1's margin on the ppl gate is 0.112.

**Labels: every label in the verdict is what the frozen prereg, A-env and the pinned reader yield from the records.** I found no label error and nothing that must be HALTED or marked INVALID. The FIX-FIRST is about what the verdict and CORPUS may *say*.

---

## BLOCKING

### B1. The fit screen that blocked arm B is failed equally by the in-block reference. ROUTING-BLOCKED-UNDERFIT must be scoped accordingly.

**Evidence.** The A7-multi arm solves its 24 targets with the same `capture_targets` (`experiments/track_c/c10u_mint2_arms.py:819` → `:447–465`). That function parses the same engine "avg prob" aggregate that P3 admission uses (`:454–457`; the step-0 call is `:729`). The multi throws the aggregates away (`z_rows, _, fits, _ = …`, `:819`) and its record carries `admission.P3.fits = []` (`r3/F_r0_multi_snone.json`). They are printed to its log, though:

| arm (r3 unless noted) | target ids | aggregates ≥ 0.98 of 24 | min | source |
|---|---|---|---|---|
| A7-multi(frozen) r0 | 4–6 | **17** | 0.852 | `r3/logs/behavior_F_r0_multi_snone.log` (`capture … avgprob=`) |
| A7-multi(frozen) r1 | 4–6 | 17 | 0.852 | `r3/logs/behavior_F_r1_multi_snone.log` |
| A7-multi(frozen), attempt r1 | 4–6 | 17 | — | `results/c10u_mint2/logs/behavior_F_r0_multi_snone.log` |
| A7-multi(frozen), attempt r2 | 4–6 | 19 | — | `results/c10u_mint2/r2/logs/behavior_F_r0_multi_snone.log` |
| modifier-only s0 / s1 / s2 | 3–4 | 17 / 13 / 14 | 0.017 / 0.536 / 0.013 | `r3/logs/step0_F_r0_modifier_s*.log`; = `admission.P3.n_ge_0.98` |
| A7-multi(V2) | 4–6 | **14** | 0.631 | `r3/logs/behavior_V2_r0_multi_snone.log` |
| mint-2(V2) s1 / s2 | 2 | 20 / 21 | — | `r3/V2_r0_mint2_s{1,2}.json` |
| mint-1(frozen) s0 | 1 | 24 | 0.993 | `r3/logs/step0_F_r0_mint1_s0.log` |

The ≥ 22/24 screen came from the one-id mint prereg (`C10L_MINT_TOKEN_PREREG.md:34`, `:100`, cited at prereg :72). It is applied only to mint arms (:72, :115). The comparator it is measured against fails it in all three attempts (17, 19, 17), with longer targets. The screen also does not predict behaviour for multi-id targets. A7-multi(V2) passed only 14/24 and still scored canon 24/24 and para_full 31/72. Modifier s0 (17) equals the reference. Seeds 1 and 2 (13, 14) sit 3–4 below it, a gap that has not been shown to exceed attempt-to-attempt variation (the multi moved 17 → 19 → 17).

So ROUTING-BLOCKED-UNDERFIT is the correct *label* under :72, but it is not evidence that the modifier-only representation is harder to write than the string. The packet's phrase "could not be tested" is accurate. Any CORPUS or queue wording such as "modifier-only underfits" or "arm B fails to fit", without the comparator's number beside it, would be an over-claim. §8.1 is silent on this, and none of the review files I searched raise it (`grep` over `results/c10u_mint2*.md` for multi + 0.98/admission/avgprob: no hit). Under the same screen, block V2's mint-2 UNDERFIT seeds (20, 21) fit *better* than V2's own reference (14).

**Exact replacement text.** In `docs/C10U_MINT2_PREREG.md:193`, append to the end of the "Block F: ROUTING-BLOCKED-UNDERFIT" bullet:

> The screen is not applied to the reference arm, and the reference fails it. A7-multi(frozen) solves its targets through the same `capture_targets` (`c10u_mint2_arms.py:819`, `:447–465`) and the same engine aggregate, and only 17 of its 24 aggregates are ≥ 0.98 (`r3/logs/behavior_F_r0_multi_snone.log`, identical in `F_r1`; attempt r1: 17; attempt r2: 19). A7-multi(V2) has 14/24 (`r3/logs/behavior_V2_r0_multi_snone.log`) and still scored canon 24/24. Modifier seed 0's 17/24 equals the reference's count, and seeds 1 and 2 (13, 14) lie 3–4 below it. ROUTING-BLOCKED-UNDERFIT therefore records that the arm-B behavioural run was not made under the one-id screen of :72. It is not a finding that the modifier-only representation fits worse than the string, and no such comparison may be drawn from it.

Add a §8.1 item 10 with the same fact for V2 (mint-2 s1/s2 at 20/21 vs the V2 reference at 14), so that "UNDERFIT-NOT-COMPARABLE" is not read as mint-2 underfitting relative to the string.

### B2. Seed 2's TRADEOFF comes from the comparator, not from a perplexity cost of the arm. The note must say so.

**Evidence.** The gate is post(arm) ≤ post(reference) + 0.5 (`c10u_mint2_read.py:130`). This is the house convention: the same form appears in `c10p_twopass_read.py:55`, `c10s_sharedz_read.py:332`, `c10t_secondkey_read.py:176` and `c10v_layerpick_read.py:348`, so it is not a defect. In r3, though, the reference's own write *lowered* generic ppl from 21.755 to 21.522 (−0.233; `r3/F_r0_multi_snone.json` `arm.locality_axes.generic_ppl_pre/post`). mint-1 s2's own rise is 21.755 → 22.074 = +0.319, within the stub's "generic perplexity rise ≤ 0.5" (`results/research_pass_2026-10-06/prereg_stubs.md:10`) if that is read as the arm's own rise. The same seed's post was 21.932 in attempt r1 (reference post 21.59) and 21.989 in attempt r2 (reference post 21.981). It **passed** this gate in both attempts. Its post-write ppl is stable across attempts (21.93 / 21.99 / 22.07), and the reference's moves (21.59 / 21.98 / 21.52). The r3 miss of 0.052 is driven by the r3 reference's low draw.

The label TRADEOFF stands (pinned reader, binding). But "TRADEOFF on generic perplexity" will be read downstream as "minting costs fluency at seed 2", and the records do not show that.

**Exact replacement text.** In `docs/C10U_MINT2_PREREG.md:194`, after "…`r3/F_r0_mint1_s2.json` and `r3/F_r0_multi_snone.json`).", insert:

> The miss comes from the comparator side of the gate. The reference's own write lowered generic perplexity from 21.755 to 21.522, while seed 2's own rise was +0.319 (21.755 → 22.074). In attempts r1 and r2 the same seed's post-write perplexity was 21.932 and 21.989, and it passed this gate against references of 21.59 and 21.981 (descriptive under :186; not pooled; source digests differ). TRADEOFF is the label. It is not evidence that the one-token mint raises generic perplexity by more than 0.5.

### B3. The verdict as worded leads with a reference-arm result and drops the provisional status. The CORPUS sentence must be fixed.

**Evidence.**
- Step 3's question was the span/modifier *direction* (§3 :94–103). Both blocks returned no direction (READ `F.direction` = ROUTING-BLOCKED-UNDERFIT, `V2.direction` = NOT-COMPARABLE, `raw_direction` null for both).
- mint-1(frozen) is "CORPUS/45's recipe re-run in this session as the in-block upper reference" (:76). Its three counts are the LAW#3 reproduction (:77). They are not a new result.
- CORPUS/45 labelled the same recipe at 34–46 **PARTIAL** under its own scheme (`CORPUS/45_C10L_MINT_TOKEN.md:61`). Calling the same counts "LEAD" in a new entry, with no note, reads as an upgrade, which §4 forbids ("No label in CORPUS/44–50 changes", :111).
- "Beat the in-block multi-token reference" is true only on full-sequence binding. On first-id, the reference scores **53**/72 against mint-1's 46/37/40 (`arm.para_first_n`; for a one-id value, first equals full).
- The :172 condition is unmet (§8.1 item 1, `EXPERIMENT_RUNBOOK.md:338`, `:342`, `:347`). The verdict sentence must carry that status, not only the note.

**Exact replacement text.** The CORPUS verdict line, verbatim:

> D-C10u-mint2 (step 3), attempt r3 — PROVISIONAL (program-authorized under D-C10r-rulings-9; operator ratification of r3 pending per prereg :172): **no direction reading on either block.** Block F = ROUTING-BLOCKED-UNDERFIT: the modifier-only arm was not run because all three seeds failed the one-id P3 screen (17/13/14 of 24, against 22). The in-block A7-multi reference fails the same screen (17/24), so this says nothing about modifier-only versus the string. Block V2 = NOT-COMPARABLE: its string baseline was far above the window (31/72, canon 24/24), and V2 replication was waived (D-C10u-r3skipV2). The LAW#3 reproduction passed: mint-1(frozen), CORPUS/45's recipe, scored 46/37/40 against the in-block A7-multi 14/72. Under this prereg's ≥ 30 scheme that is LEAD/LEAD/TRADEOFF, and the seed-2 TRADEOFF comes from the reference's ppl drop. CORPUS/45's PARTIAL is unchanged. Gate A was bit-identical (frozen contexts), so it shows repeatability, not robustness. P4 NOT TRIGGERED.

---

## ADVISORY

- **A1. The A1 validity floor holds with zero margin in block F.** In every F record the in-run A1 control is exactly 68/72 hits (`recipe.detail.A1_single`, summed `para_full_hits`), the :90 floor (`read.py:237–238`, CONTROL_MIN 68). V2 records have 70. The r1 replica is the same measurement (bit-identical), not a second pass. Add one line to §8.1 so that a later "valid" is not read as comfortable. Note that `identity.law3_reference.scores.A1_single` = 71 is the preflight value, not the in-run control.
- **A2. Cross-attempt descriptives actually support ≥ 30 better than gate A did.** mint-1(frozen) scored ≥ 34 in all 9 seed × attempt cells (r1 40/36/41, r2 34/35/37, r3 46/37/40), with gains over the same-attempt multi of 23–32. This is the robustness evidence gate A was meant to supply. It may be reported descriptively under :186 (not pooled, confounded by source changes), and it is a fairer summary than "the real spread is 37–46".
- **A3. Prereg design flaw for any successor: gate A (:78) cannot measure what it says.** §8.1 item 8 is right and complete on this. A successor prereg should define replication as a fresh context draw (new `contexts_*.json` from a fresh A7-multi process) with the same inits. The LEAD rule (:92) is absolute (≥ 30), with no gain requirement. In V2, mint-2 s0 at 30 with gain −1 would have been LEAD if its two gates had passed, and only NOT-COMPARABLE prevented that. A successor should require gain ≥ 10 for LEAD as well.
- **A4. §8.1 item 3 should name the alternative label.** Under :90's literal reading ("P3 admission screen … any failure → INVALID"), block F would read INVALID rather than ROUTING-BLOCKED-UNDERFIT. Either way there is no direction. Say so in one clause, so the reader sees that the choice was immaterial to the outcome and was fixed before observation (reader pinned at `afbf8e9`, before r3).
- **A5. §8.1 item 1 omits the point that weakens the delegation argument the most.** D-C10r-rulings-8's blanket approval (`EXPERIMENT_RUNBOOK.md:338`, 2026-10-06 ~23:55) was already in force when :172 was written (A-env committed `7b9a30d` 2026-10-07 06:34 MDT). Yet :172 still required that "the operator records a new ruling". The standing approvals therefore cannot be read as satisfying :172 by themselves. Suggested sentence, appended to item 1 before "**How r3 is to be read:**":

  > :172 was written while D-C10r-rulings-8's blanket approval was already in force (A-env commit `7b9a30d`, 06:34 MDT), and it still required a new operator ruling, so the standing approvals do not by themselves meet it.

  A smaller point: the runbook times D-C10u-Aenv at ~07:30 MDT (`:343`), after D-C10u-r2go at ~07:20 (`:344`), but the A-env text was committed at 06:34. Cite the commit time.
- **A6. Put the ratification question to the operator explicitly, in one line, with a recommendation.** D-C10r-rulings-10 ("yes to all your questions", `:351`) lists four answered items, and none is r3. D-C10u-r3go (2) (`:347`) also says "any further HALT in r3 stops step 3 for an operator report". p4-save's "HALT:" exit is procedural under D-C10u-r2go (2) (`:344`), but that ruling's wording is scoped to r2. The operator report is owed in any case. My recommendation is to ratify. The measurements are valid under every pinned gate, and ratification changes no label. Until it is recorded, nothing in the queue should route on r3's labels.
- **A7. V2's :78 "pending a diagnosis" stays open and must be recorded as owed.** It must not be dropped. A model-free first step exists: the A7-multi(V2) per-value fits (14/24, with para_full 31) and the per-position teacher-forced curve (`arm.extra.per_position_teacher_forced`) can be tabulated without a GPU. Do not write "V2 stimuli invalid" (:78 forbids it).
- **A8. §8.1 item 8 "with that input fixed, the rest of the computation was deterministic on this machine"** is I-INFER, supported by the bit-identical replica (EVIDENCE-SHOWS for these 7 record pairs). It is not shown in general. Label it as inference. The citation `memit_main.py:304–320` → `util/generate.py:116–119` (`torch.multinomial` over top-k) checks out. CORPUS/44:32 cites the older `generate.py:40–43` for the same sampler, so the two citations disagree on line numbers.
- **A9. Drift check.** r3 does not advance the F1 determination beyond CORPUS/45. The one positive output re-confirms a known result, and the step's routing question is unanswered on both blocks. Do not re-run step 3 under the same design. If arm B is to be read, the screen must first be made symmetric or replaced by a prospective amendment under an operator ruling. Changing it after these observations makes it post hoc and needs that ruling.

## Overturning tests

- **For "ROUTING-BLOCKED-UNDERFIT means arm B cannot be written":** a zero-cost test, already run by this review. Read the reference's own aggregates from the existing logs. It overturned the natural reading (B1).
- **For "mint-1(frozen) LEAD, replicated":** a fresh-context-draw block, which gate A was meant to be and was not. The existing three attempts are the closest proxy (A2). They do not overturn ≥ 30 at any seed, but they are not a pre-registered test.
- **For "seed 2 TRADEOFF = perplexity cost":** zero-cost, from the r1/r2 records (B2). It overturned the reading, not the label.

## Proposed one-sentence CORPUS verdict

D-C10u-mint2 (step 3), attempt r3, PROVISIONAL pending the operator's ratification required by prereg :172: **neither block gave a direction reading.** Block F is ROUTING-BLOCKED-UNDERFIT: the modifier-only arm was never run because all three seeds failed the one-id fit screen (17/13/14 of 24), a screen the in-block multi-token reference also fails (17/24), so nothing follows about modifier-only versus the string. Block V2 is NOT-COMPARABLE: its baseline was far above the window (31/72, canon 24/24), and its replication was waived. The LAW#3 reproduction of CORPUS/45's one-token mint passed: 46/37/40 against the in-block reference's 14/72, labelled LEAD/LEAD/TRADEOFF under this prereg's ≥ 30 scheme. The seed-2 TRADEOFF comes from the reference's perplexity drop, CORPUS/45's PARTIAL is unchanged, and the bit-identical gate-A replica shows repeatability, not robustness. P4 was not triggered.
