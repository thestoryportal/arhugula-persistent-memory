# 54 — Two-token and modifier-only mint (step 3, r3): no direction reading on either block; one-token mint reproduced (CLOSED, operator-ratified)

**Ratified by the operator 2026-10-07 ~21:08 MDT (D-C10r-rulings-12, Q2; operator verbatim "Yes on all 5."; runbook §5.2): r3 accepted; status CLOSED.** This changes no result, label, number or interpretation below.

_Result 2026-10-07 UTC. Decision-ID D-C10u-mint2. ⟨D-C10u-mint2@d1299b2b⟩ Pre-registration docs/C10U_MINT2_PREREG.md v3 FROZEN + amendment A-env (§8, ruling D-C10u-Aenv) + post-observation deviation note §8.1 (written after r3's last stage; it changes no rule, threshold or label). Attempt r3, run c10u-d12d79257d0d457a8cdd6b1d44ddeed9, first stage started 2026-10-07T16:01:40Z, source digest 67c73b97079941ba4bc6dcc101d4999a2a24a3a141203ff2ded1e66286fd34ed (results/c10u_mint2/r3/identity.json:2, :80; results/c10u_mint2/r3/reproduce_started.json:119). Pinned reader experiments/track_c/c10u_mint2_read.py sha256 1223789a…, prereg sha256 c54f443c… for the text before §8.1 (docs/C10U_MINT2_PREREG.md:190; results/c10u_mint2_r3_facts.md:8). Binding reading results/c10u_mint2/r3_read_after_replicateF.json (READ below); records results/c10u_mint2/r3/; logs results/c10u_mint2_logs/r3/. Engine unmodified, fingerprint d941a9fb/PASS, _cov_cpu=3 (results/c10u_mint2/r3/F_r0_multi_snone.json:100–102). Authority: program rulings D-C10u-r3go and D-C10u-r3skipV2 under D-C10r-rulings-9 (runbook §5.2); the operator ratification required by prereg :172 was given 2026-10-07 ~21:08 MDT (D-C10r-rulings-12). Verdict reviews: results/c10u_mint2_r3_verdict_astra.md (GPT-6-Astra high) and results/c10u_mint2_r3_verdict_advisor.md (Opus advisor), both FIX-FIRST on wording, both confirming every label; their text is folded into prereg §8.1 (:258). Facts sheet: results/c10u_mint2_r3_facts.md. Lineage: CORPUS/44 ⟨D-C10l-covgeom@af2e38f7⟩, CORPUS/45 ⟨D-C10l-mint@a4a6f4c7⟩, CORPUS/53._

## Pre-registration and claim class

Step 3 of the research-pass sequence (H-19) is a routing screen on the write path for the §8.9 L2 multi-token value cell: Qwen2.5-3B fp16 on MPS, band 4–8, the C10 harness through its `ARM_HOOKS` and `Z_OVERRIDE` seams, engine unmodified. It has two comparison blocks that are never pooled. Block F keeps the frozen values: A7-multi(frozen) is the string reference; mint-1(frozen) at seeds 0, 1 and 2 is CORPUS/45's recipe re-run as the in-block upper reference and as the LAW#3 reproduction gate; modifier-only at seeds 0, 1 and 2 mints the 8 modifiers and leaves each head as base pieces. Block V2 uses the redrawn value set A7-V2: A7-multi(V2), mint-1(V2) and mint-2(V2), the last with each word as its own minted id. Sources: docs/C10U_MINT2_PREREG.md:76–78, :105.

Step 0 admits a mint arm only if at least 22 of its 24 engine fit aggregates are ≥ 0.98. Below that the arm is UNDERFIT and gets no behavioural run, and a block in which any mint arm is not fully fit reads ROUTING-BLOCKED-UNDERFIT with no direction label (:72, :115). The screen comes from the one-id mint prereg and is applied only to mint arms. Per-arm labels are read against the same-block A7-multi: LEAD at ≥ 30/72 with every gate held; PARTIAL at a gain ≥ 10 below 30; NULL inside [11, 18] whatever the gain; TRADEOFF for a PARTIAL- or LEAD-sized count with a gate miss (:92). The direction labels (block F: MODIFIER-RECOVERY, NO-MODIFIER-GAIN, MIXED; block V2: SPAN-DIRECTION, PAIR-DIRECTION, MIXED) need a valid, fully fit, locality-clean block and its replication block (:94–102, :177–179). Amendment A-env set the baseline window to CORPUS/44's A4 values, para_full [5, 18], canon [5, 10], para_first [42, 59], as block F's LAW#3 guard and block V2's comparability screen; a V2 screen failure labels the block NOT-COMPARABLE and suspends its direction reading pending a diagnosis (:78, :175). No outcome closes H-19, and no label in CORPUS/44–50 changes (:111).

r3 is the third attempt. r1 HALTED at the block-F LAW#3 multi window (:168). r2 closed HALTED-HARNESS on a driver defect (:200; runbook §5.2 D-C10u-r3go (1)). Neither is pooled with r3. Prereg :172 allows no r3 "unless the operator records a new ruling"; r3 ran on program rulings under D-C10r-rulings-9, and V2 gate-A replication was waived after stage `v2` had been observed (D-C10u-r3skipV2). Both are deviations from the frozen protocol, disclosed in §8.1 items 1 and 7 (:200, :222–233).

## VERDICT — CLOSED (operator-ratified); no direction reading on either block

D-C10u-mint2 (step 3), attempt r3 — CLOSED, operator-ratified: program-authorized under D-C10r-rulings-9 and ratified by the operator under D-C10r-rulings-12 as prereg :172 requires; V2 replication was waived post-observation. Neither block gave a direction reading, so neither new representation advanced. Block F is ROUTING-BLOCKED-UNDERFIT: the modifier-only arm was never run because all three seeds failed the one-id fit screen (17/13/14 of 24), a screen the in-block multi-token reference also fails (17/24), so nothing follows about modifier-only versus the string. Block V2 is NOT-COMPARABLE: its baseline was far above the window (31/72, canon 24/24). The LAW#3 reproduction of CORPUS/45's one-token mint passed: 46/37/40 against the in-block reference's 14/72 on full-answer binding (the reference leads on first word, 53/72), labelled LEAD/LEAD/TRADEOFF under this prereg's ≥ 30 scheme; the seed-2 TRADEOFF comes from the reference's perplexity drop; CORPUS/45's PARTIAL is unchanged; the replica matched exactly under fixed inputs, which shows repeatability, not robustness. P4 was not triggered; C10/F1 unchanged.

The pinned reader reproduces READ exactly (results/c10u_mint2_r3_verdict_astra.md:5). Both reviewers recomputed the labels from the raw records and found no label error and nothing that must be HALTED or marked INVALID (results/c10u_mint2_r3_verdict_advisor.md:30–41; results/c10u_mint2_r3_verdict_astra.md:23–35).

**Block F (r3; the r1 replica block is identical in every count and gate).**

| Arm | Step-0 fit: aggregates ≥ 0.98 of 24 | Full answer /72 (binding) | First word /72 | Canonical /24 | Gain over reference | Failed gates | Label |
|---|---:|---:|---:|---:|---:|---|---|
| A7-multi(frozen), reference | 17 (screen not applied to this arm) | 14 | 53 | 8 | — | — | inside the original and the A4 window |
| mint-1(frozen) seed 0 | 24 | 46 | 46 | 24 | +32 | none | LEAD |
| mint-1(frozen) seed 1 | 24 | 37 | 37 | 24 | +23 | none | LEAD |
| mint-1(frozen) seed 2 | 24 | 40 | 40 | 24 | +26 | generic perplexity | TRADEOFF |
| modifier-only seeds 0 / 1 / 2 | 17 / 13 / 14 | not run | not run | not run | — | — | UNDERFIT (each) |

Sources: READ :3, :5–21, :912–928, :1819–1835, :2726–2766, :2772–2795; records results/c10u_mint2/r3/F_r0_*.json (`arm.para_full_binding_n`, `arm.para_first_n`, `arm.canon_full_n`, `admission.P3.n_ge_0.98`); reference fit count from results/c10u_mint2/r3/logs/behavior_F_r0_multi_snone.log (results/c10u_mint2_r3_verdict_advisor.md:51–57). For a one-id value the first word is the whole answer, so mint-1's first-word and full-answer counts coincide.

**Block V2 (r3; no replica was run).**

| Arm | Step-0 fit: aggregates ≥ 0.98 of 24 | Full answer /72 (binding) | First word /72 | Canonical /24 | Gain over reference | Failed gates | Label |
|---|---:|---:|---:|---:|---:|---|---|
| A7-multi(V2), reference | 14 (screen not applied to this arm) | 31 | 49 | 24 | — | — | screen failed: 31 > 18 and 24 > 10 |
| mint-1(V2) seed 0 | 24 | 51 | 51 | 24 | +20 | none | LEAD-NOT-REPLICATED-NOT-COMPARABLE |
| mint-1(V2) seed 1 | 24 | 46 | 46 | 24 | +15 | none | LEAD-NOT-REPLICATED-NOT-COMPARABLE |
| mint-1(V2) seed 2 | 24 | 38 | 38 | 24 | +7 | none | LEAD-NOT-REPLICATED-NOT-COMPARABLE |
| mint-2(V2) seed 0 | 23 | 30 | 47 | 23 | −1 | described_as, sibling | TRADEOFF-NOT-COMPARABLE |
| mint-2(V2) seeds 1 / 2 | 20 / 21 | not run | not run | not run | — | — | UNDERFIT-NOT-COMPARABLE (each) |

Sources: READ :2799–2817, :3255–3271, :3709–3725, :4163–4179, :4724–4742; records results/c10u_mint2/r3/V2_r0_*.json (same fields); reference fit count from results/c10u_mint2/r3/logs/behavior_V2_r0_multi_snone.log (results/c10u_mint2_r3_verdict_advisor.md:58). mint-1(V2) seed 2 is labelled LEAD by the absolute ≥ 30 rule although its gain, +7, is below the +10 PARTIAL margin; mint-2(V2) seed 0 is LEAD-sized at 30 with a gain of −1 and two failed locality gates, and one of its values (Fluvane) is under 0.98 at one position (docs/C10U_MINT2_PREREG.md:229–230). READ gives `V2.reasons = []` for this value-based screen failure, a reporting gap that leaves the verdict unaffected (:217, :228).

## The fit screen and block F

The A7-multi(frozen) reference solves its 24 targets through the same `capture_targets` and the same engine aggregate as the mint arms' step 0, and 17 of its 24 aggregates are ≥ 0.98 in r3 (17 in attempt r1, 19 in attempt r2). Modifier-only seed 0's 17/24 equals that count; seeds 1 and 2 (13, 14) lie 3–4 below it, a gap not shown to exceed the reference's own attempt-to-attempt movement. The screen does not predict behaviour for multi-id targets here: A7-multi(V2) passed 14/24 and still scored canonical 24/24 and full answer 31/72, and V2's mint-2 seeds 1 and 2 (20, 21) fit better than V2's own reference (14). ROUTING-BLOCKED-UNDERFIT therefore records that the arm-B behavioural run was not made under the one-id screen of :72. It is not a finding that the modifier-only representation, or two minted ids, fit worse than the string. Sources: docs/C10U_MINT2_PREREG.md:193; results/c10u_mint2_r3_verdict_advisor.md:47–64.

The prereg disagrees with itself on a failed P3 screen: :90 lists it among the INVALID conditions, while :72 and :115 route it to UNDERFIT with no behavioural run. The reader pinned before r3 implements :72 and :115. Under the :90 reading block F would read INVALID instead; either way it has no direction reading. Sources: docs/C10U_MINT2_PREREG.md:204–209; results/c10u_mint2_r3_verdict_advisor.md:102.

## The one-token mint reproduction and its labels

mint-1(frozen) is CORPUS/45's recipe, and its three counts are this block's LAW#3 reproduction, not a new result. 46/37/40 lie inside the per-seed windows [32, 56], [24, 44] and [26, 46], median 40 ≥ 30, and the block-F reference's 14/8/53 lies inside both the original window and A4 (docs/C10U_MINT2_PREREG.md:77, :202; READ :2772–2795). CORPUS/45 labelled the same recipe at 34–46/72 PARTIAL under its own scheme (CORPUS/45_C10L_MINT_TOKEN.md:61). This prereg defines LEAD at ≥ 30/72 (:92). The change of word is a change of scheme, not an empirical improvement, and CORPUS/45's label stands (results/c10u_mint2_r3_verdict_astra.md:33; :111). The mint leads the reference on full-answer binding; the reference leads on first word, 53/72 against 46, 37 and 40.

Seed 2's only failed gate is generic perplexity: post-write 22.074 against the reference's 21.522 + 0.5 = 22.022 (READ :1822–1830; rule `c10u_mint2_read.py:130`). The miss comes from the comparator side. The reference's own write lowered generic perplexity from 21.755 to 21.522, while seed 2's own rise was +0.319 (21.755 → 22.074). In attempts r1 and r2 the same seed's post-write perplexity was 21.932 and 21.989, and it passed this gate against references of 21.59 and 21.981 (descriptive, not pooled; source digests differ). TRADEOFF is the label. It is not evidence that the one-token mint raises generic perplexity by more than 0.5. Sources: docs/C10U_MINT2_PREREG.md:194; results/c10u_mint2_r3_verdict_advisor.md:72–80.

READ's nested `replica.label` "LEAD-NOT-REPLICATED" for seeds 0 and 1 is the replica read without a replica of its own; the arm label is the outer `label` (READ :6, :457, :913, :1364; :194).

## Repeatability, not robustness

Every r3/F_r0 record matched its r3/F_r1 counterpart in every JSON leaf except `replicate`, `pid` and `when_utc` where present (multi 3,706 leaves, each mint-1 record 6,424, modifier records 3,443/3,447/3,446). Both replicates loaded the same frozen context set, the mint arms reused r0's init rows and solved targets through `Z_OVERRIDE`, and the r1 modifier records re-read r0's step-0 admission. This establishes observed repeatability with fixed contexts, inits and cached mint targets, not zero population variance or robustness to context resampling. Gate A, as specified at :78, held fixed the context sample that CORPUS/44 F-A4 identified as the source of the ±4–5 process envelope, so it did not measure that envelope. A V2 replica would have tested fresh-process recurrence under the same fixed inputs; it was not run, and its result is unknown. Sources: docs/C10U_MINT2_PREREG.md:233–247; results/c10u_mint2_r3_facts.md:122–149; results/c10u_mint2_r3_verdict_astra.md:15–19.

Across attempts, each with freshly sampled contexts and the same init rows, mint-1(frozen) seed 0 scored 40 (r1), 34 (r2) and 46 (r3); seed 1 scored 36, 35 and 37; seed 2 scored 41, 37 and 40; the reference scored 10, 10 and 14. All nine mint-1 cells are ≥ 34. These counts are descriptive only: not pooled, not a replication, confounded by source changes between attempts, and they relabel nothing. Sources: docs/C10U_MINT2_PREREG.md:249–254; results/c10u_mint2_r3_verdict_advisor.md:100.

## Validity, P4 and advisories carried forward

No r3 record reads INVALID. LAW#5 passed in every record (|Δexpr| ≤ 0.0002). The in-run A1 control is exactly 68/72 in every block-F record, the floor of :90, and 70/72 in every V2 record; "valid" here has zero margin on that control in block F, and the r1 replica is the same measurement, not a second one. Sources: results/c10u_mint2_r3_facts.md:29; results/c10u_mint2_r3_verdict_advisor.md:99.

`p4-save` refused before its stage marker and before any model work: no configuration carries a LEAD or PARTIAL label among the mint-2 and modifier-only arms, so P4 is NOT TRIGGERED, neither a PASS nor a FAIL, and no compiled-artefact claim is made (docs/C10U_MINT2_PREREG.md:86, :256; results/c10u_mint2_logs/r3/p4-save.log:1–2).

Advisories carried, not resolved here:
- **Authority.** D-C10r-rulings-8's blanket approval was already in force when :172 was written, and :172 still required a new operator ruling, so the standing approvals do not by themselves meet it. Until the operator records a ruling on r3, nothing in the queue routes on r3's labels (results/c10u_mint2_r3_verdict_advisor.md:103–108).
- **V2 diagnosis owed.** :78 suspends V2's direction reading "pending a diagnosis". The diagnosis is still owed. A model-free first step is to tabulate A7-multi(V2)'s per-value fits (14/24) and its per-position teacher-forced curve from the existing record. "V2 stimuli invalid" is not a permitted reading (:78; results/c10u_mint2_r3_verdict_advisor.md:109).
- **Open reader advisories.** A2, A4 and A5 of results/c10u_mint2_readerfix2_advisor.md have no recorded disposition; none affected an r3 count (docs/C10U_MINT2_PREREG.md:215–220). P4 eligibility of a ROUTING-BLOCKED block (advisory A6) is still unconfirmed by the operator (:211).

## Not claimed

Not a finding that modifier-only or mint-2 fits or writes worse than the string. Not a SPAN-DIRECTION, PAIR-DIRECTION, MODIFIER-RECOVERY or NO-MODIFIER-GAIN reading. Not an upgrade of CORPUS/45: its PARTIAL label and its counts stand. Not evidence that the one-token mint is robust to context resampling or to a new seed draw. Not a claim that MPS computation is deterministic in general, or that context sampling is the only stochastic source. Not a compiled-artefact claim. No CORPUS/44–53 label changes; H-19 stays open; the 61/72 program bar is not reached; C10 remains OPEN/BLOCKING and F1 is unchanged. Sources: docs/C10U_MINT2_PREREG.md:111, :245; results/c10u_mint2_r3_facts.md:180–181.

## Decision-ID and FORK

D-C10u-mint2: closed, r3 ratified by the operator (D-C10r-rulings-12, 2026-10-07 ~21:08 MDT), with no direction reading on either block; neither new representation advanced; one-token mint LAW#3 reproduction passed; P4 not triggered.

Do not re-run step 3 under the same design. If arm B is to be read, the fit screen must first be made symmetric with the reference or replaced, by a prospective amendment under an operator ruling; changing it after these observations would make it post hoc (results/c10u_mint2_r3_verdict_advisor.md:111). For any successor prereg: define replication as a fresh context draw with the same inits, and require gain ≥ 10 for LEAD as well as ≥ 30 (:101).

Cheapest overturning control (Astra), candidate only: before claiming robustness, preregister one fixed mint-1 seed plus its multi reference on a newly sampled context set with regenerated targets and unchanged science code, and test the same LEAD and locality gates. It bears on the write-path diagnostic and closes neither H-19 nor F1. No run or adoption is implied (results/c10u_mint2_r3_verdict_astra.md:39).

_Verdict sentence merged from the GPT-6-Astra and advisor verdict reviews (results/c10u_mint2_r3_verdict_astra.md:41–43; results/c10u_mint2_r3_verdict_advisor.md:119–121) and adopted by the program session under D-C10r-rulings-9._
