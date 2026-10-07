Verdict: FIX-FIRST

**Single most important fix:** move LAW#3 reproduction before the first adapter training; the current schedule trains all five P1 adapters first (`docs/C10W_ORACLE_PREREG.md:244–246`).

**Reviewer: `gpt-6-astra`, effort `high`.** Confirmed by [session metadata](/Users/robertrhu/.codex/sessions/2026/10/07/rollout-2026-10-07T07-20-06-01a11685-71b6-7701-b83f-85a11be67f7f.jsonl:8).

Below, **P** means `docs/C10W_ORACLE_PREREG.md`. Reviewed SHA-256: `31bc8edc44d717f85bc5e0619346b3abfb71590fdf51e202af75bceda6460179`. Read-only static review; runtime gates remain **UNVERIFIABLE**.

1. **BLOCKING — correct LAW#3 thresholds, wrong execution order; P3 omits oracle inertness.**  
   P:214–218 requires reproduction before *trust*, while P:244–246 explicitly trains before reproduction. That falls short of the requested pre-training gate and `CLAUDE.md:30`. The envelope itself correctly matches `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`: full **[5,18]/72**, canonical **[5,10]/24**, first-token **[42,59]/72**, inclusive.

   P3 lists U → closed form → trained recipes, omitting LAW#5(ii), despite its validity requirement at P:303; the P3 budget likewise omits null evaluation (P:254,280). Thus Codex #5/#8 are not fully implemented despite P:441,444.

   **Exact replacement/addition for P:214 and the start of §2.8:**
   > LAW#3 must pass before any candidate adapter is trained or read. After step 0, run a baseline-only preflight: fingerprint, U and stimulus checks, LAW#5(ii) zero-adapter behavior and restore, then the unchanged closed-form A1/A2/A7 recipe with its standing LAW#5 gate. Require A1/A2 ≥68/72 and A7 para_full_n ∈ [5,18]/72, canon_full_n ∈ [5,10]/24, para_first_n ∈ [42,59]/72, endpoints inclusive. Any miss HALTs before training. Each trainer verifies the passing preflight record and matching frozen provenance before loading the model. Every subsequent evaluation process repeats these controls before applying a trained adapter.

   **Replace P3’s evaluation sequence at P:254 with:**
   > fingerprint → U and stimulus checks → LAW#5(ii) zero-adapter behavior and restore → closedform with LAW#3 → oracle_r64_s0 → oracle_r64_s1. LAW#5(i) runs before each recipe’s arms; restore checks and hit counters must pass before its results are trusted.

   Charge the added preflight and P3 null evaluation to §2.9; its current totals cannot remain unchanged (P:273–281).

2. **BLOCKING — the fold retains a causal attribution that the control cannot support.**  
   P:361(b) says “The transfer came from the 19 extra frames.” Yet the canonical control is rank 16 only, while PASS can come from rank 64 (P:347,355). A permitted counterexample is r16 **29/29**, r64 **61/61**, canonical-r16 **29/29**, with gates clean: the routing attributes a jointly changed rank/frame result solely to frames. Independent 400→800 retries can also break step matching (P:54,159). Advisor #1 and Codex #1 remain partially unresolved despite P:425,437.

   **Replace P:361(b):**
   > (b) The rank-16 canonical-only recipe did not reach a replicated minimum of 30/72. This does not establish that the extra frames caused the successful result. A rank-64 PASS has no matched rank-64 canonical control here. Steps 6–7 proceed only on their independent preregistered rationale; the result may motivate a separately preregistered multi-frame test without causal attribution.

   **Replace “differs from it only…” / “separate phrasing diversity…” at P:53:**
   > This is a fixed-update-budget frame ablation. Interpret paired frame contrasts only at the same rank, seed and final training-step count. Report unmatched contrasts descriptively.

3. **BLOCKING — numeric labels partition correctly, but one routing case has no defined reference.**  
   The four valid configuration cases at P:327–330 exhaust integer counts **0–72** without overlap; the rank-combination table at P:343–351 also partitions its stated inputs. However, P:362 requests the highest gate-clean replicated count without handling an empty set.

   Counterexample: r16 **61/61 with G6 missed**, canonical control also misses G6. Final label is LOCALITY-COST, P3 does not run, canonical split is NOT-READ, and **zero** gate-clean O-A7 ranks exist (P:345,355,362). The label-order fixes from advisor #4/Codex #3 are present; their downstream reference handling remains incomplete.

   **Replace the reference-selection sentences at P:362:**
   > Under split (a) or (b), the reference is O-A7-canon’s replicated count. Under (c), select the maximum replicated minimum among completed, valid, stable O-A7 ranks with G1–G7 passing at both seeds. If that set is empty, record reference_count = null and reference_status = NO-GATE-CLEAN-REFERENCE. Report attained counts and gate costs; do not substitute a costly count or issue a reference-based comparison.

4. **BLOCKING — FAIL prose overstates the minimum-seed rule.**  
   H-W0 correctly uses the **minimum** seed count (P:28,337), but P:23 and P:363 say the evaluated recipes “stayed below 30/72.” Both ranks could score **29/44**, with an identical seed-0 retrain: the seed gap is exactly **15**, so final FAIL is permitted although two fitted adapters scored **44** (P:335,337,351). This leaves advisor #6/Codex #1 incompletely corrected.

   **Replace the corresponding FAIL sentences at P:23 and P:363:**
   > FAIL-CEILING means that each evaluated rank’s minimum across its two valid, stable seeds is below 30/72. It does not mean that every fitted adapter scored below 30/72. Report all seed counts; this is a recipe-level replication outcome, not a model-capacity bound.

5. **BLOCKING — record the supplied rulings and enforce the P1-only authorization.**  
   §8 still calls all three decisions open (P:483–489). More materially, P:247,283 stops for a budget ruling only when projections exceed an allowance, while P:339 says P3 runs “iff” its scientific trigger holds. Neither makes additional approval necessary when estimates are within bounds. Your supplied ruling approves **P1 alone**.

   **Replace §8’s opening and three items:**
   > These rulings are settled by the program’s freeze-check instruction:
   > 1. The blind-authorship departure is ACCEPTED, with the disclosure and restricted interpretation in §2.3.
   > 2. This freeze check is the GPT-6-Astra/high pass. Its S7 judgments supplement the earlier gpt-6.1-sol/max design review; any reviewer REJECT remains binding. The present verdict is FIX-FIRST.
   > 3. P1 alone is approved. After P1, record measured training/evaluation times and separate P2/P3 projections. Stop before either additional phase until its authorization is recorded. Estimates below an allowance do not authorize continuation. Without required replication, issue no final scientific label or routing.

   Replace P:64’s pending-acceptance sentence with:
   > The program has accepted this departure; the disclosure and interpretation limits remain binding.

   Add to P:249,254,339:
   > Scientific eligibility is necessary but insufficient: P2/P3 also require the recorded post-P1 budget authorization.

6. **ADVISORY — make the new single-frame schedule executable and remove an unsupported impossibility claim.**  
   The canonical adapter has **24** items, but the batching/epoch rows still specify **480** items and **20 epochs** universally (P:53,155–156).

   **Replace those rows’ schedule text:**
   > Each epoch permutes that adapter’s actual N training items with seed 1000·seed + epoch; batch size is 24. N=480 gives 20 steps per epoch; O-A7-canon has N=24 and one step per epoch. Train for 400 updates: respectively 20 and 400 epochs; an 800-update retry doubles these totals.

   P:339,451 also asserts that larger rank “cannot repair a locality miss.” That impossibility is **UNVERIFIABLE** from the cited worsening trend.

   **Replace that rationale:**
   > P3 is excluded after LOCALITY-COST by the preregistered scope and budget policy; this is not evidence that higher rank cannot improve locality.

7. **ADVISORY — fold-accounting result and verification limits.**  
   No additional replacement is required beyond the issues above. Every v1 BLOCKING item was checked:

   | v1 item | v2 disposition verified in the operative text |
   |---|---|
   | Advisor #1 | Canonical control added, but attribution remains defective: item 2; P:53,355,361. |
   | Advisor #2 | Mechanism/residual corrections present: P:21,27,152. |
   | Advisor #3 | Rejected strings replaced and S2c/S2d added: P:75,78,83,91,98–106. |
   | Advisor #4 | Label ordering/table fixed; empty-reference case remains: item 3; P:339–362. |
   | Advisor #5 | Merge-loss blocks routing with the narrowed exception: P:333,337. |
   | Advisor #6 | Model-wide claim removed; minimum-seed wording still overstates: item 4; P:28,363. |
   | Codex #1 | Major ceiling claims removed; residual attribution/FAIL overclaims remain: items 2,4; P:23,361,363. |
   | Codex #2 | Authorship departure disclosed; supplied ruling and this S7 record need folding: item 5; P:64,104,487–488. |
   | Codex #3 | Numeric boundaries and retrain crossings fixed; routing reference incomplete: item 3; P:335–362. |
   | Codex #4 | Matched shuffled controls and retry-step matching present: P:54,182,250,254,324. |
   | Codex #5 | Nonzero seam/counters/restoration added; P3 null omission remains: item 1; P:210,225–227,254. |
   | Codex #6 | Environment/provenance/frozen-parameter guards present: P:141,166,200. |
   | Codex #7 | Immutable acquisition, frozen instrument and integer net-loss gate present: P:193–197. |
   | Codex #8 | Timing/memory guards and expanded inventory present; omitted controls must be priced: item 1; P:260–285. |

   Static recomputation reproduced both published template hashes, all **22** S1–S5/S2c/S2d passes, all listed S3 maxima, and **67** banned tokens (P:70–106). This does not verify future trainer isolation or runtime inertness. The cheapest overturning checks are the model-free routing counterexamples above, followed by the corrected baseline/null sequence before training. This review advances the oracle’s Write Engine measurement discipline; it closes no F1 condition (P:15,23,357).

**S7 adjudication**

Judgments use P:93–104’s distinctive-wording/structure definition and CANON exemption. Held-out forms are Q1’s possessive capital-city naming, Q2’s visit conditional followed by an anaphoric capital clause, and Q3’s coordinated city/government-seat description (`experiments/track_c/c10e_bandknob.py:51–56`). These are semantic judgments, not empirical generalization evidence.

| ID | Verdict | One-line reason | Template source |
|---|---|---|---|
| T01 | ACCEPT | Explicit CANON exemption; none of the distinctive held-out structures. | P:70 |
| T02 | ACCEPT | Generic capital-of predication, without distinctive held-out wording. | P:71 |
| T03 | ACCEPT | Direct question/answer structure, unlike all three held-out completions. | P:72 |
| T04 | ACCEPT | Interrogative city-role description, without Q3’s coordination or government-seat phrase. | P:73 |
| T05 | ACCEPT | Capital field label; no possessive, visit clause or coordinated description. | P:74 |
| T06 | ACCEPT | Evidential introduction precedes generic capital predication; no subject-containing conditional. | P:75 |
| T07 | ACCEPT | Atlas entry is the subject of “lists”; no clause break after the entity slot. | P:76 |
| T08 | ACCEPT | Map-label assertion lacks Q2’s conditional/anaphoric structure. | P:77 |
| T09 | ACCEPT | “Fact” heading adds no distinctive held-out wording or structure. | P:78 |
| T10 | ACCEPT | Country-has-capital construction lacks Q1’s possessive opening and Q2’s clause sequence. | P:79 |
| T11 | ACCEPT | Evidential adverb plus generic capital predication. | P:80 |
| T12 | ACCEPT | “National” modifies the ordinary capital phrase; no distinctive held-out form. | P:81 |
| T13 | ACCEPT | CANON-like town completion lacks possessive naming or government-seat coordination. | P:82 |
| **T14** | **ACCEPT** | Atlases “give … as” reporting construction; neither a visit conditional nor nested governmental description. | **P:83** |
| T15 | ACCEPT | Modified CANON construction; “official” does not recreate Q3’s distinctive structure. | P:84 |
| T16 | ACCEPT | Locative capital predication, without the held-out naming or clause structures. | P:85 |
| T17 | ACCEPT | Temporal capital predication lacks distinctive held-out wording. | P:86 |
| T18 | ACCEPT | Reporting clause embeds generic capital predication, not Q2’s visit/then-capital sequence. | P:87 |
| T19 | ACCEPT | Map introduction contains no entity slot; it does not reproduce Q2’s subject-bearing first clause. | P:88 |
| T20 | ACCEPT | Quiz heading plus generic capital predication. | P:89 |
| **R1** | **ACCEPT** | Textbook attribution embeds generic capital predication without a held-out structure. | **P:91** |
| **R2** | **ACCEPT** | Schoolbook listing construction lacks possessive naming, conditional visitation and government-seat coordination. | **P:91** |

**S7 result: 22 ACCEPT, 0 REJECT; no substitutions.** Prior rejected v1 strings remain rejected under the union rule (P:104,134–137). Record these judgments separately from the v1 reviewers’ columns.

🌱 graft reported ~39,368 tokens saved (~$0.02), 1 successful call.