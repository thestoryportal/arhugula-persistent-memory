Reviewer: Claude Opus 5.5 (`claude-opus-5-5`), Anthropic. Independent adversarial advisor pass on `docs/C10W_ORACLE_PREREG.md` v1 DRAFT (D-C10w-oracle), 2026-10-07, read-only, method `tools/advisor_review_prompt.md`. Same model family as the drafting session, so this pass does not replace the GPT-6-Astra design pass.
Verdict: FIX-FIRST

**Most important:** a PASS cannot route to steps 6–7 as written. The oracle changes three things at once relative to the closed form: 20 training frames instead of one, a delta that acts at every position, and iterative fitting. Steps 6–7 can supply only the second and third. Add a single-frame oracle arm (O-A7-canon, trained on T01 = `CANON` only) and route on it. Without it, a PASS cannot say whether the lever is the solver's objective or the phrasing diversity that the dataset-free solver will never have.

## What was checked and holds (evidence, not opinion)

- **Seal audit reproduces exactly.** I recomputed it with stdlib Python and no model. The template hash is `55363a85…0bda` and the reserve hash is `c0ef01e3…7fd5`, matching `docs/C10W_ORACLE_PREREG.md:87`. The derived banned set `'s, and, called, government, if, its, main, seat, visit, you` and 67 banned words in total match `:92`. Every max-S3 value in the table at `:64–85` matches to 3 decimals, and T09 against Q3 (0.578) is the largest. `PTEST` matches `experiments/track_c/c10e_bandknob.py:52–56`.
- **Harness seams match the source.**
  - `my_edit(hp, requests, P, cache_c)` is at `c10e_bandknob.py:181`.
  - `run_recipe` calls `my_edit` by module-global name at `:489`, and `run_law5` sets `_LAW5_DEFAULT_CTX` at `:429–435`.
  - `ARM_HOOKS` runs while the edit is applied (`:404`, `:494–495`).
  - The fp16 application is at `:216–217`, the 15 % stimulus halt at `:568`, and `para_full_n` at `:396`.
  - The A7 maps `(2i+1)%24` / `(3i+2)%24` are at `:247`.
  - The shift-by-1 A7-shuf is a derangement with no shared head or modifier (head index differs by 2 and modifier index by 3, mod 24). The `i+12` sibling shares the head and not the modifier, as `:163` claims.
- **The LAW#3 envelope choice is sound.** [5, 18] / [42, 59] / [5, 10] is CORPUS/44 A4 (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`). The Codex envelope review endorses it as the LAW#3 guard for the frozen A7 multi arm (`results/c10u_mint2_codex_envelope.md:24`, five observations 10/8/15/13/10).
- **Environment claims are true.** The venv has `torch-2.8.0`, `transformers-4.51.0` and `datasets-5.0.1`, and no `peft`. `hf_cache/hub` holds only `Qwen2.5-3B`, `Qwen2.5-0.5B-Instruct` and `wikimedia/wikipedia`, so no MMLU is local. Both are from directory listings.
- **Scope (question 5).** The operator ruling is quoted at the top (`:8`), matching `EXPERIMENT_RUNBOOK.md:330`. Every output carries the class string (`:238`), every routing row says "C10 stays OPEN/BLOCKING" (`:280`), and the overlay row is "no amendment" (`:331`). No path promotes a pass as a write route. This holds.
- **Feasibility on MPS (question 3).** Nothing is infeasible.
  - The fp32 3.09 B-parameter trainer needs ≈ 12.3 GB plus about 5 GB of activations and logits for 600 tokens. That is well under 48 GB, and the 40 GB halt is sensible.
  - float64 is used only on CPU (`:115`, `:160`), consistent with `experiments/track_c/c10l_mint_lib.py:66`.
  - The budget is under-counted (ADVISORY 9). It is not infeasible.

## Issues, in priority order

### 1. BLOCKING: a PASS confounds phrasing diversity with the solver objective, so the PASS routing to steps 6–7 is uninterpretable

**Defect.** The oracle trains on 20 frames (`:62`). The closed form fits z in the `CANON` frame only, with sampled prefixes (`c10e_bandknob.py:182`, `:191`; `memit_dry_run/memit/memit/compute_z.py:46–50`), and its weight solve keys at the subject's last token only (`c10e_bandknob.py:196–201`).

The PASS row routes to "steps 6 (H-11) and 7 (H-3)" (`:284`). Step 7 is a "dataset-free" per-commit solve (`results/research_pass_2026-10-06/recommended_sequence.md:27`; stub `prereg_stubs.md:73–79`, one canonical request), and step 6 is an engine-path change (`prereg_stubs.md:69–71`). Neither supplies 20 phrasings. Multi-frame fitting is step 1's lever (H-1), and it came back UNDERFIT ×2 (`docs/INTEGRATED_QUEUE_2026-10-07.md:16`).

So a PASS driven by frame diversity would send the engine days to arms that cannot use it. The draft's own scope paragraph (`:21`) does not name this factor.

**Cheapest overturning control.** Add one adapter trained on T01 only, with everything else unchanged. It costs about 30 min of training plus 10 min of eval per seed.

**Fix: insert after `:50` (§2.2):**
> - **A7-canon (single-frame oracle; the confound control for the PASS routing)**: the A7 map, trained on T01 (= `CANON`) only, 24 items, same trainer, hyperparameters, steps (400) and batch (24). Fit gate for this adapter: train-EM ≥ 23/24. It receives the frame information the closed-form solve receives, minus the engine's sampled prefixes (which are unseeded per process, `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:32`). The oracle O-A7 differs from it only in the 19 extra frames. The two together separate *phrasing diversity* from *every-position, iterative fitting*.

**Replace `:202–203` with:**
> 2. Train O-A7 s0, then O-A7-canon s0, then O-A2 s0, then O-A7-shuf s0.

**Replace `:207` with:**
> 1. Train O-A7 s1, O-A7-canon s1, O-A1 s1, and O-A7 s0 retrained, in fresh processes.

(Recipe `oracle_s1` gains the arm O-A7-canon. Its request set has the same subject–value pairs as O-A7, so it must be a **separate recipe** (`oracle_canon_s0`, `oracle_canon_s1`), because the adapter lookup key at `:133` would collide.)

**Replace the PASS routing row at `:284` with:**
> | **PASS-CEILING** (either rank) | The five band matrices of this model can hold the 24 coined values with held-out transfer at the bar and locality clean. Route on O-A7-canon (replicated min of s0, s1): **(a) O-A7-canon ≥ 30/72** → fitting at every position without extra frames already transfers; steps 6 (H-11), 7 (H-3) and 5b proceed with O-A7-canon's count as their reference ceiling. **(b) O-A7-canon < 30/72** → the transfer came from the 19 extra frames, which a dataset-free per-commit solve does not have; steps 6–7 proceed on their own pre-registered rationale only (this result raises no prior for them), and the finding is routed to the multi-frame family (H-1, step 1). H-30 weight grafting (`hypotheses.md:309–310`) becomes eligible as its own pre-registration in either case. |

Add the same O-A7-canon clause to the PARTIAL row (`:285`): "the practical reference ceiling for steps 6–7 is O-A7-canon's replicated count, not O-A7's."

### 2. BLOCKING: two rationale lines rest on the "no objective on value tokens 2…N" error, and the PASS routing inherits the "3 percent" error

**Defect.**
- **H-W1 (`:25`).** It says "the loss acts on every value token at every position in every phrasing, which the closed-form write lacks (`hypotheses.md:136`)". The cited line attributes the lack to "CORPUS/36: no direct objective on tokens 2…N" (`results/research_pass_2026-10-06/hypotheses.md:136`). That is false: `compute_z` puts every target id in `rewriting_targets` (`memit_dry_run/memit/memit/compute_z.py:60–65`) and sums the NLL over all of them (`:141–150`). What lacks an objective is the **weight solve** at value positions, whose keys are read at the subject's last token (`c10e_bandknob.py:196–201`). The program has recorded this correction (`docs/INTEGRATED_QUEUE_2026-10-07.md:39`).
  - Note: that line, and this review's brief, give the path as `memit_dry_run/memit/compute_z.py`. The vendored file is `memit_dry_run/memit/memit/compute_z.py`.
- **Loss row (`:116`).** Its reason column cites "the H-13 mechanism (`hypotheses.md:136`)", the same error.
- **Question quote (`:19`) and PASS routing (`:284`).** `:19` quotes the sequence row whose stated reason for steps 6–7 is "aimed squarely at the '3 percent installed' finding" (`recommended_sequence.md:26–27`, `:13`). `:284` concludes "the wall is a missing objective or its realisation". ρ_c is the **remaining** residual: about 2.8 % unrealised at the keyed position and about 23 % on paraphrases (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:43`; correction at `docs/INTEGRATED_QUEUE_2026-10-07.md:38`). "Realisation" at the keyed position is not the wall.

**Fix: replace the last sentence of `:25` with:**
> The mechanism claim, corrected from H-13: the closed form already optimises its target z against **every** value token (`memit_dry_run/memit/memit/compute_z.py:60–65`, `:141–150`; H-13's "no direct objective on tokens 2…N", `hypotheses.md:136`, is false as written, `docs/INTEGRATED_QUEUE_2026-10-07.md:39`), but in one frame and through a weight solve whose keys sit at the subject's last token only (`c10e_bandknob.py:196–201`), so the solve places no constraint at the frame or value positions. The oracle's loss differs in three ways at once: every phrasing (20 frames), every position (ΔW acts on, and is trained through, every token), and iterative fitting. O-A7-canon (§2.2) separates the first from the other two.

**Replace the reason cell at `:116` with:**
> the oracle's objective: every value token, every position, every training frame (corrected mechanism, §1 H-W1)

**Append after the quote at `:19`:**
> *Correction carried from `docs/INTEGRATED_QUEUE_2026-10-07.md:38–39`: the sequence's rationale for steps 6–7 ("about 3 percent installed", `recommended_sequence.md:13`, `:27`) is backwards: ≈ 2.8 % of the canonical residual **remains** (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:43`). The wall this experiment bounds is transfer from the keyed position to paraphrases and later value positions, not a write that barely lands.*

**In `:284`, replace "The wall is a missing objective or its realisation, so" with:**
> The closed form's shortfall is therefore in what its solve constrains (one frame, one key position), not in the band's capacity to hold the value; with that,

### 3. BLOCKING: the seal's mechanical rules miss the draft's own definition; three admitted templates and one reserve share a held-out template's distinctive structure

**Defect.** The draft defines a paraphrase as sharing a held-out template's "distinctive wording or its distinctive structure" (`:89`). It rejected `For {}, the capital is` and `Among the facts about {}: the capital is` for having Q2's "phrase containing the subject, then a clause about the capital" shape (`:101`). But S2c (`:94`) matches only the separators `,:;—-` and requires `\bis\b`, so it admits two templates with exactly that shape:
- T06 `Encyclopedia entry: {}. Capital:` (`:71`)
- T14 `Reference card for {}. Capital:` (`:79`)

Separately, Q3 = `The main city and seat of government of {} is` (`c10e_bandknob.py:55`) has the distinctive shape "The ‹NP› of ‹NP› of {} is". No rule encodes it, and the following share it:
- T09 `The capital of the nation of {} is` (`:74`). It has the highest S3 in the set at 0.578, just under the 0.60 threshold.
- Reserve R1 `The capital of the republic of {} is` (`:87`, S3 0.565). So S7's replacement chain would substitute a template with the same defect.

The program's own precedent counts a Q3-shaped write prompt as mirroring (`results/autoresearch_c10_heldout_mirroring_2026-10-06.md:9`).

I checked the replacement rules below with stdlib Python on all 23 listed strings plus the two rejected candidates and Q2. They reject exactly T06, T14, T09, R1, both previously rejected candidates and Q2 itself, and admit everything else.

**Fix: replace the S2c rule at `:94` with:**
> - **S2c — Q2's shape.** No template in which the subject slot is followed by any clause break and later by the capital: the case-insensitive regex `\{\}\s*[,.:;?!—-].*capital` must not match.
> - **S2d — Q3's shape.** No template with two or more `of` tokens before the subject slot: `t.lower().split("{}")[0].split().count("of") >= 2` must be false.

**Replace T06, T09 and T14 in the table, and the reserve list at `:87`, with:**
> T06 `According to the records, the capital of {} is` (max S3 0.426; former R2) · T09 `Fact: the capital of {} is` (0.514; former R3) · T14 `Most atlases give the capital of {} as` (0.457). **Reserve list** (fixed order): R1 `Textbooks state that the capital of {} is` (0.422), R2 `Schoolbooks list the capital of {} as` (0.474). Recompute both SHA-256 values; step 0 recomputes S1–S5, S2c and S2d and halts on any difference.

**Adjust `:99`:** "More than two rejections exhaust the reserves". **Adjust `:101`:** the audit sentence now names the five rejected candidates (the two above plus T06, T09 and T14 of v1) and S2c/S2d as the rules that rejected them.

### 4. BLOCKING: "the better of" two labels is undefined, and the P3 trigger is ambiguous for LOCALITY-COST

**Defect.**
- **No ordering.** "Final label = the better of the r = 16 and r = 64 labels" (`:278`) has no stated ordering between PARTIAL-CEILING-LOCALITY-COST and PARTIAL-CEILING (`:270–271`). Example: r = 16 is 45/72 and clean, while r = 64 is 63/72 with a G6 miss. Either label satisfies "better", and the PARTIAL routing's "practical reference ceiling" (`:285`) would be 45 or 63 depending on which is picked.
- **Ambiguous trigger.** P3 runs if the r = 16 label is "PARTIAL- or FAIL-CEILING" (`:211`, `:278`). Whether PARTIAL-CEILING-LOCALITY-COST triggers it is undefined. A larger rank is the direction in which the source's forgetting worsened (`hypotheses.md:137`: 57.0 → 52.0 → 40.2), so P3 cannot repair a locality miss.

**Fix: replace `:278` with:**
> **Capacity check (P3; runs iff the replicated r = 16 label is PARTIAL-CEILING or FAIL-CEILING; it does not run on PARTIAL-CEILING-LOCALITY-COST, PASS-CEILING, INVALID or -UNSTABLE).** The r = 64 label is computed on min(count_s0, count_s1) by the same rules. Label order, best first: PASS-CEILING > PARTIAL-CEILING-LOCALITY-COST > PARTIAL-CEILING > FAIL-CEILING; within one label the higher replicated count wins. **Final label = the better of the r = 16 and r = 64 labels by that order**, written `…(capacity r = 64)` if r = 64 supplied it. The PARTIAL routing's reference ceiling is the highest replicated count among gate-clean configurations (with issue 1, O-A7-canon's); a LOCALITY-COST count is reported beside it, never used as the reference. The FAIL routing requires both ranks to fail.

### 5. BLOCKING: -MERGE-LOSS cannot move the band, so a FAIL or PARTIAL can be an fp16 rounding artifact routed as a model finding

**Defect.** The adapter is trained in fp32 (`:115`) and merged in fp16 (`:136`). The binding count is the merged one (`:146`). Merge versus mount is measured, and a gap of more than 5/72 sets -MERGE-LOSS (`:171`), but qualifiers "do not change the band" (`:274`). If mounted is 62 and merged is 25, the draft routes FAIL to the model axis (`:286`) on a dtype artifact. That makes a FAIL uninterpretable, which is question 1's criterion.

**Fix: append to `:274`:**
> **-MERGE-LOSS changes routing:** if it fires on any configuration that enters the replicated label, that configuration routes as **-UNSTABLE** (no routing; report merged and mounted counts; diagnosis first, §5). A merged PASS stays PASS (the merge is the conservative direction); a merged FAIL or PARTIAL with -MERGE-LOSS is not read.

### 6. BLOCKING: the FAIL routing claims "the question becomes the model", but the same model already holds a coined value with 34–46/72 transfer

**Defect.** The FAIL row says "the question becomes the model" and surfaces the ceiling-rule decision "with this result as the evidence" (`:286`). On this model, band and harness, a closed-form write of a coined value as one minted token already reaches 34–46/72 (`CORPUS/45_C10L_MINT_TOKEN.md:61`). Risk 1 admits this (`:299`), but the routing ignores it.

An oracle FAIL bounds *multi-token string* values on these five matrices under this recipe. It is not evidence that the model cannot hold coined values. Routing it to the model axis would over-claim.

**Fix: replace the FAIL routing cell at `:286` with:**
> Even this training cannot reach "worth replicating" for the multi-token **string** value on these five matrices. This is not evidence against the model as a whole: a minted single-token value on the same model and band already transfers 34–46/72 under the closed form (`CORPUS/45_C10L_MINT_TOKEN.md:61`). The result is surfaced to the operator for the ceiling-rule decision (D-C10k-rulings-2; `HANDOFF.md:56`) as evidence about the **string representation on this band**, with the representation route (step 3, minting) named beside the model axis; steps 6–7 are deprioritised pending that ruling, not cancelled. Before the ruling, the operator may choose H-15 (full-band fine-tuning, `hypotheses.md:154–162`) as a stronger oracle.

**Also replace H-W0 at `:26`:** "…and the rank-64 capacity check also stays below **30/72**" (it currently says "below the bar", and the bar is 61).

### 7. ADVISORY: the bigram rule counts facts that did not fire

`:165` defines X = #{s_k = 1 or b_k = 1 or n_k ≥ 1/2} over **all** facts but compares it with C = #{c_k = 1}. A fact whose modifier never fires under its own subject can still add to X, so -BIGRAM can fire at C = 1 from unrelated facts.

**Replace with:**
> **-BIGRAM** if *C* ≥ 1 and *X* ≥ ⌈*C*/2⌉, where *C* = #{c_k = 1} and *X* = #{c_k = 1 and (s_k = 1 or b_k = 1 or n_k ≥ 1/2)}.

Note for the reader: every head is shared by two subjects with different modifiers (`c10e_bandknob.py:247`), so pure head-to-modifier bigram learning cannot by itself produce a full A7 pass. The qualifier-only status (`:274`) is therefore acceptable.

### 8. ADVISORY: G7 and the shuffled control exist only for r = 16 seed 0, but are applied to every configuration

The draft says G7 is "P1, applied to every O-A7 configuration's label" (`:266`), yet O-A7-shuf is trained only in P1 at r = 16 (`:203`). For an r = 64 label, the frame-habit gate is inherited from a different adapter.

**Replace `:211`'s training list with:**
> train O-A7 and O-A7-shuf at r = 64 (α = 64) for seed 0, and O-A7 at r = 64 for seed 1

and add to `:266`:
> (for r = 64, G7 is read from O-A7-shuf r = 64)

### 9. ADVISORY: the budget is under-counted; MPS feasibility is fine

- **Per-recipe overhead.** Each `run_recipe` repeats `compute_P`, five CPU SVDs of 11008² (`c10e_bandknob.py:166–178`, called at `:462`), and the LAW#5 gate, which runs an engine write and a closed-form write (`:415–446`). P2 and P3 each run three recipes (`:208`, `:211`), and issue 1 adds one more per phase. That overhead is a share of the 33-min anchor (`hypotheses.md:8`) and is not counted at `:228`.
- **Closed-form arms.** These also carry MMLU-200, the 20-template frame probe and the bigram hooks (`:150`, `:159`), which the 33-min anchor never included.
- **Realistic total.** About 10–11 trainings at 25–37 min each, plus three eval processes of 1.5–2 h. That gives ≈ 8–10 h binding and ≈ 10–12 h with P3, against the draft's 5–7 h and 7–9.5 h (`:232`). This is UNVERIFIABLE until P1 is timed.

**Add to `:202`:**
> After P1's eval, re-project P2 and P3 from the measured per-training and per-recipe times and record the projection in `verdict.json`.

**Add to `:326`:**
> any eval process exceeding 4 h wall-clock.

### 10. ADVISORY: the MMLU floor sits inside paired noise, and the dataset revision is unpinned

- **Floor in noise.** "≥ U − 2.0 points" is a net loss of at most 4 of 200 (`:158`). With about 20 discordant items, a typical count for any weight change, the net-change SD is about 4.5 items. A forgetting-neutral adapter therefore misses G6 by chance often enough to flip PASS into LOCALITY-COST.
- **Revision not pinned.** The `cais/mmlu` revision is not fixed.

**Replace the floor at `:158` with:**
> **Floor: net paired loss vs U ≤ max(4, closed-form A7's net paired loss + 2) items of 200**; discordant counts reported for every arm

(the closed-form arm is the same-process calibration the contract already names, `prereg_stubs.md:9`).

**Add to `:157`:**
> step 0 records the dataset commit SHA and asserts a `subject` column and exactly 5 `dev` items per subject used.

### 11. ADVISORY: citation fixes

- **Integrated queue.** "One GPU run at a time" is `docs/INTEGRATED_QUEUE_2026-10-07.md:43`, not `:37` (`:37` is blank). Fix at `:11` and `:331`.
- **CORPUS/45.** `:168` cites `CORPUS/45_C10L_MINT_TOKEN.md:28` for "the closed form shows no sibling confusion". That line reports the **minted-token** arm. Use: "the minted-token closed form shows no sibling confusion (`CORPUS/45…:28`); the multi-token closed form's sibling emission is measured here in arm A."

### 12. ADVISORY: one factor remains unseparated even with O-A7-canon; state it in §4

O-A7-canon still differs from the closed form in two ways: every-position action and iterative fitting. CORPUS/44 F-A5 and CORPUS/46 F-D1 point at collateral change at non-keyed positions (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:33`, `:43`).

**Add to §4 risks after `:299`:**
> 1b. **Position versus fitting.** Even O-A7-canon cannot say whether its gain comes from ΔW acting at every position or from iterative fitting; H-30 grafting (or a later position-restricted adapter) is the separating test, not this experiment.

## Overturning tests, cheapest first

1. O-A7-canon (issue 1): about 40 min. This is the one that decides what a PASS means.
2. The merge-versus-mount gap (issue 5): already in the design, now wired to routing.
3. The seal re-audit under S2c/S2d (issue 3): stdlib only, seconds.

## Drift check

This advances a live §0.3 falsifier only through the routing of steps 6, 7 and 5b and the ceiling-rule decision. With issues 1, 2 and 6 fixed, it does that honestly. Without them, either outcome would steer engine days or a model change on a confounded inference.
