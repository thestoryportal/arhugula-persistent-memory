# Advisor review: D-C10w-oracle P1 readout, before CORPUS/55 (Claude Opus 5.5, read-only, 2026-10-07)

**FIX-FIRST**

**The most important point:** the seed-0 reading already limits what P2 can return, and both CORPUS/55 and the operator question must say so. At rank 16 the result can no longer be PASS-CEILING. The seed-0 G4 miss is carried into the replicated gate-miss union (`c10w_oracle_read.py:382`, `:392`), so if the count holds, the label is PARTIAL-CEILING-LOCALITY-COST(G4). The O-A7-canon split is already NOT-READ, because canon s0 fails G2 (12/30) and G4, and the split needs G1–G6 to pass at both seeds (`read.py:403`). With LOCALITY-COST and split (c), the reader issues `NO-GATE-CLEAN-REFERENCE` (`read.py:461–464`). The seed-0 label is non-routing, so step 5 does not yet count as "read" for D-C10r-rulings-10 (3).

## How I checked the numbers

- I ran sha256 on both files. The prereg is `d2aa240e…35d2f0`, which equals `PREREG_SHA` (`read.py:20`). The reader is `162966119c…859b0b`, which equals `step0.json` /sources/reader.
- I imported the pinned reader unmodified and ran `validate_phase(eval.json)` on it. It passed.
- `read_measurement({"P1":…})` returned status INCOMPLETE, with final_label and routing both None.
- `configuration(P1,"oracle_p1")` is byte-equal to `interim_reader_configuration.json` (dict equality: True).
- I ran the reader CLI on the P1 directory with `LLMDB_ROOT` set to the worktree. It exited 2 with no stderr. That means status ≠ VALID and no Halt. Its JSON equals `verdict.json` minus `projection` and `stop`.
- I extracted every other number below from `eval.json`, `verdict.json`, `preflight.json` and `train/*` with python3.

## Fact check of the packet (facts 1–6)

| # | Claim | Verified value (source) | Status |
|---|---|---|---|
| 1 | Five trainings PASS at 400 steps, no retries, 6.2–8.7 min | wall 409.7 / 523.4 / 372.1 / 422.1 / 500.0 s, i.e. 6.83 / 8.72 / 6.20 / 7.04 / 8.33 min, sum 37.1 min. Fit 480/480 ×4 and 24/24 (canon). Frozen params unchanged. Peak driver 21.4–28.6 GB (`eval.json` train_records) | VERIFIED |
| 1 | Budget 592 (D-C10r-rulings-10); preflight ≈60, eval ≈95 | `authorization_P1.json` budget_minutes 592; runbook :353 cap 660. Preflight wall 3590 s = 59.8 min. **Eval wall 5773.7 s = 96.2 min**, not 95. P1 total ≈ 193 min | VERIFIED (eval is 96, not 95; minor) |
| 2 | status PASS; validity all true; LAW#5(i) 0.0004 / 0.27 in each recipe; restore | status PASS. validity: 6 keys all True. law5_gate {expr 0.0004, loc 0.27, ok} in closedform, oracle_p1 and oracle_canon_s0. restored True and band_after==base in all three; final==base | VERIFIED |
| 2 | LAW#3 A7 9/72, first 52, canon 9/24; A1/A2 | closedform A7 para_full 9, first 52, canon 9. A1 72, A2 70. U A7 0/72. Stimulus base 0 ×4 | VERIFIED, inside [5,18]/[42,59]/[5,10] (`prereg:244`) |
| 3 | INCOMPLETE, routing null, exit 2 not Halt; projection 178.0 / 138.3; allowances 448 / 327 | P2 178.044, P3 138.250. The arithmetic in `reproject` (`read.py:477–478`) reproduces from the basis. The basis uses the **max** of the raw units (conservative). authorization_required [P2,P3]; stop string as quoted | VERIFIED |
| 4 | O-A7 s0 70/72, +61; G4 miss with the quoted vectors; label, BIGRAM, mounted 70; shuffled 71 / 0 | All values reproduced exactly. G4 vectors match `extra.frames.train[*].flips` for oracle_p1 A7 and closedform A7; canon 1 vs 1 | VERIFIED |
| 5 | canon 24/24, para_full 2, first 5, L3 12/30, KL 3.18, L1 top-1 changed 6/12 | 24 / 2 / 5 / 12 / 3.18453 / 6 | VERIFIED. But "canon split needs P2" is misleading (issue 2) |
| 6 | O-A1 72, O-A2 72 | 72, 72 | VERIFIED |

## Issues, in priority order

### 1. BLOCKING: the interim reading must not count as step 5 being "read", and CORPUS/55 must say so

**Evidence:**
- §8 item 3 (`prereg:532`): "Without required replication, issue no final scientific label or routing."
- §3 (`prereg:370`): replication is "required before any label routes".
- D-C10r-rulings-10 (3) (`EXPERIMENT_RUNBOOK.md:353`) lets steps 6 and 7 go "once steps 3–5 are read".
- §6 (`prereg:452`) places CORPUS/NN after P2, (P3) and the verdict review.

**Problem:** a CORPUS/55 that carries a label string invites someone to treat step 5 as read and start steps 6 and 7.

**Required changes:**
- CORPUS/55 status is INTERIM / INCOMPLETE, not a close of D-C10w-oracle.
- CORPUS/55 states that step 5 is **not read** for D-C10r-rulings-10 (3) until the reader returns VALID.
- CORPUS/55 records that writing a CORPUS entry at P1 departs from the order in §6 :452, so it is an interim record and the final entry follows the verdict review.
- If `closeout_check.py` treats ALL GREEN as closing the D-ID, it must not be run as a closing check here.

### 2. BLOCKING for the operator question: say plainly what P2 can and cannot return

Every point below follows mechanically from P1 and the pinned reader.

- **No rank-16 PASS is possible.** `replicated()` takes the union of seed gate misses (`read.py:382`). The s0 G4 miss is robust: oracle flips exceed A(t)+1 on 15 of 20 training templates (T02, T03, T06–T12, T14, T16–T20). Oracle total is 50/120 against 4/120 for the closed form. So the best r16 label is PARTIAL-CEILING-LOCALITY-COST(G4).
- **The canon split is already (c), NOT-READ.** `canonical_split` requires `all(gates(...))` at both seeds (`read.py:403`). Canon s0 already returns G2 False (L3 12/30 < 29) and G4 False (CANON 3 vs 1; T13 4 vs 1). I reproduced this with the reader's `gates()`.
- **The likely end state** is final PARTIAL-CEILING-LOCALITY-COST(G4) with `reference_status = NO-GATE-CLEAN-REFERENCE` (`read.py:461–464`). The reference count is null, so steps 6 and 7 would proceed only on their own rationale.
- **There is a real -UNSTABLE path.**
  - G6 passes exactly at the boundary: net loss 4/200 (13 correct→wrong, 9 wrong→correct; `prereg:368` "loss 4 passes, loss 5 misses").
  - If the same-seed retrain lands at net loss 5, that is a "binding gate crossing" and the label is -UNSTABLE (`prereg:370`; `read.py:390`).
  - I-INFER: G6 = 4 is unlikely to be a stable property of the recipe. The matched shuffled control loses 9/200 and O-A2 loses 5/200 (`verdict.json` g6_sensitivity, report-only), and discordance is 22/200 against 3/200 for the closed form.
- **P3 is reachable only if the replicated r16 minimum falls to 30–60.** That means seed 1 would have to drop by at least 10 from 70. P3 can never run on LOCALITY-COST or -UNSTABLE.

**Decision value for the operator:** P2 is the price of turning the P1 data into any pre-registered label. It is unlikely to change what happens to steps 6 and 7, and it has a non-trivial chance of ending -UNSTABLE.

### 3. BLOCKING (a cheap fix): the cited interim artifact lacks the class line and the Decision-ID

**Evidence:**
- `interim_reader_configuration.json` has the keys `reader_sha256`, `oracle_p1_A7_configuration`, `shuf_cross_score_vs_original_map` and `shuf_own_map_para_full_n` only.
- §2.10 (`prereg:324`): "Every JSON carries `class` … and the Decision-ID".
- Header (`prereg:3`): every output carries "oracle measurement, not a route".

This file holds the 70/72 headline that CORPUS/55 will cite. It also does not record the scratch script that produced it. I could reproduce the output by importing the reader and calling `configuration`, but nothing in the artifact says that this is how it was made.

**Fix (no overwrite, per `prereg:322`):** write a new sibling record that carries `class`, `decision_id` and `"interim_non_routing": true`, plus the scratch script text or its sha256 and the exact call sequence (`validate_phase`, then `configuration(P1,"oracle_p1")`). Cite that record from CORPUS/55, or state the omission in CORPUS/55.

### 4. ADVISORY (wording; binding on content): what may and may not be said about 70/72 and G4

**May say:**
- It is a single-seed (s0, r16) attained count on this fixed, test-aware benchmark (`prereg:23`, `:64`).
- Held-out full-sequence 70/72 against 9/72 for the same-process closed form.
- Per template 22/24/24.
- Per-edge 3/3 on 22/24 facts. The misses are Zorbland and Plurnak, both on Q1, both with the first token correct.
- canon 24/24, mounted 70 (no merge loss), shuffled cross-score 0/72.

**Must not say:**
- That it is a ceiling or upper bound (`prereg:23`, `:406`).
- That it is a route or write-engine evidence (`prereg:3`).
- That it shows a missing objective (`prereg:19`, `:406`).
- That the "+61 gain" relates to the 61/72 bar. Placing those two numbers side by side invites misreading; write "70 vs 9" instead.
- That locality is "otherwise clean".

**Why locality is not clean:** G1 and G2 are top-1 gates and they pass. But distributional locality shifts sharply, and no gate covers it:
- O-A7 L3 mean KL 1.066 against 0.00013 for the closed form.
- L1 / L3 JS locality 87.66 / 89.19 % against 100.0 / 100.0.
- Generic perplexity falls 21.755 → 21.081. G5 is one-sided, so a fall still passes.
- `associated_with` relation flips 12/24 against 5/24 (reported, no threshold).

Report these as ungated readouts.

**How to describe G4 precisely:**
- G4 is a first-token, top-1 metric. A "flip" means a never-edited fictional subject's top-1 equals the first id of **any** edited A7 value (`c10w_oracle_eval.py:119–125`).
- The oracle's 56 flips across training and held-out frames are almost all the single-letter tokens `' V'` (32) and `' D'` (20), plus `' K'` (3) and `' Vor'` (1). The closed form's 4 are `' V'` (3) and `' Vor'` (1).
- Correct wording: "never-edited fictional subjects in capital frames move their top-1 to a coined-head first token". Do not say they emit the coined values; G4 does not measure full-value emission.
- The held-out frames show 2/2/2 against 0/0/0 (reported only, `prereg:217`).

### 5. ADVISORY: what BIGRAM means here, and it must be stated

- `prereg:365` says qualifiers are "carried and reported". `prereg:230` says the wording is "benchmark success with measured continuation leakage, without a stronger binding claim".
- **Reader logic (`read.py:245–255`):**
  - Eligible facts: 24/24, 0 excluded.
  - C = 24: the modifier is fully argmax under the correct subject with the head teacher-forced.
  - X = 17 facts where the modifier is also argmax under the swapped subject (s = 13), the head-sharing sibling (b = 0) or at least half of the six never-edited subjects (n ≥ ½: 13).
  - Mean n = 0.486.
  - X = 17 ≥ ⌈24/2⌉ = 12, so the qualifier is BIGRAM.
- **Plain reading:** for most facts, once the head is forced, the modifier follows whatever the subject.
- **Counter-evidence to state alongside it:**
  - b = 0: a head-sharing sibling keeps its own modifier.
  - G7 cross-score is 0/72.
  - Every head has two subjects, so pure head→modifier continuation cannot produce a full pass on its own (`prereg:230`).
- **Context:** the closed form is C = 9, X = 0. The shuffled and canon adapters are also BIGRAM (X = 13 and 15).

### 6. ADVISORY: O-A7-canon is not a clean frame ablation

- Canon s0 trains 400 epochs on 24 items (`prereg:182`). It damages the CANON frame for real countries: L1 top-1 changed 6/12, L3 12/30, KL 3.18, JS 42.5 / 39.3 %.
- Report "2/72 reworded" only together with that damage.
- Make no causal claim about frame diversity. `prereg:53` allows paired contrasts only at the same rank, seed and final step count, and `prereg:394` (b) forbids causal attribution even when the split is read.

### 7. ADVISORY: be precise about what LAW#5(i) covered

- The (i) values are identical across recipes (0.0004 / 0.27) because in every recipe (i) runs the delegation branch, which is the engine-parity path (`prereg:198`, `:249`). It shows the seam delegates inertly. It does not test the oracle application.
- The oracle application is covered by (ii) zero-adapter, (iii) restore, (v) hits 1/1 and 5/5, and (vi) seam in step 0.
- Word it as "LAW#5 (i)–(vi) pass", not "LAW#5 inert at each recipe" alone.

### 8. ADVISORY: geometry readout anomaly (report-only, not gated)

- The closed form's `null_cov_share` is 1.0039–1.0122 across layers 4–8, which is above 1.
- `prereg:225` expects 1.000 (CORPUS/44:25). A share greater than 1 means the computed P is not an exact orthogonal projector at this precision, or the measured ΔW is an fp16 difference.
- Do not quote the oracle's shares (0.10–0.73) as fractions against a "1.000" baseline without noting this.
- Write-size ratio O/A is 0.319.

### 9. ADVISORY on question D: asking for conditional P3 now is acceptable, with disclosures

**Why it is consistent with the prereg:**
- §8.3 and §2.8 (`prereg:278`, `:280`, `:285`, `:532`) require a recorded authorization before each phase. They do not forbid recording P3's authorization before P2.
- Scientific eligibility is enforced mechanically at P3 entry. `ensure_authorized` (`c10w_oracle_step0.py:349–351`) re-reads P1+P2 through `replication_for` and requires `INCOMPLETE and p3_required`, so P3 cannot start on LOCALITY-COST, -UNSTABLE or INVALID.

**Disclosures the question must include:**
- **(a)** P3's budget check uses the P1 projection, 138.25 min, timed at rank 16 (`step0.py:347`; `verdict.json` "rank16 projection; remeasure each rank64 attempt"). Nothing re-projects after P2. Only the per-attempt 90-min guard and the 4-h eval guard re-measure.
- **(b)** P3 would start with no further operator check-in.
- **(c)** The trigger in plain words: P3 runs only if seed 1 or the retrain pulls the replicated rank-16 count below 61. It never runs on a locality-cost or unstable outcome.

**Conservative alternative:** ask about P3 after P2. It costs one more question and gains the P2 readout.

**P2 at 448:** consistent with `prereg:314` (limit 448). The projection is 178, and the P2 eval is projected at ≈126 min against the 240-min guard.

### 10. ADVISORY: small accuracy fixes in the trackers

- The eval took 96.2 min, not ~95.
- "Others pass" should read "G1–G3, G5, G7 pass; G6 passes at its boundary (4/200)".
- The SESSION_CHECKPOINT summary (`SESSION_CHECKPOINT.md:11`, `:29`) carries the same omissions as issues 2 and 4.

## Answers to questions A–E

**A. Validity.** I found nothing invalid in P1.

- **G4 denominator.** Each frame has n = 6 and six rows, checked by `validate_arm` (`read.py:209–212`). The comparator is the same-process closed-form A7 per template (`read.py:265`), not U. Both arms are probed over `S.TEMPLATES` in the same order with the same first-id set (`eval.py:120`, `:206`).
- **Template identity in the frame records.** The records carry no template identity, so template-level attributions ("T08 5/6") rest on the driver's ordering. That ordering is consistent across arms.
- **No mis-read.** The program's G4 reading matches the reader's.

**B. Interim reporting.** It is permitted, with the restrictions in issues 1 and 3.

- **Why it is allowed:** the per-configuration label comes from the pinned reader's own function. That is not "by hand" (`prereg:287`). It is also not a final label or a routing (`prereg:532`).
- **Required wording:**
  - "single-seed configuration reading (s0, r16) from the pinned reader's `configuration()`; not replicated, not a final label, no routing; the reader's status is INCOMPLETE".
  - The label and its gate named: PARTIAL-CEILING-LOCALITY-COST(G4).
  - Qualifier BIGRAM.
  - Step 5 is not "read".
- **Alternative:** if the program prefers the stricter option, CORPUS/55 carries the counts and gate pass/fail without the label string. My recommendation is to include the label string with the qualifiers above, because the gate table makes it deterministic anyway.

**C. Interpretation limits.** See issues 4, 5 and 6. BIGRAM must be stated.

**D. Next step.** See issues 2 and 9. Asking for P2 at 448 is consistent with the prereg. Asking for P3 conditionally in the same question is acceptable only with disclosures (a)–(c) and the issue-2 outcome bounds.

**E. Blockers.** Issues 1, 2 and 3.
- Issues 1 and 3 block writing CORPUS/55.
- Issue 2 blocks the operator question.
- None of them requires a rerun.

## The overturning test

The cheapest test that could overturn the interim reading is P2 itself:
- seed 1 against s0 for the count,
- the same-seed retrain for G6 (boundary) and G4.

No cheaper model-free control remains. The G4 miss is robust in the existing data (15/20 templates). G6 is the fragile gate.

## Drift check

P1 advances the §0.3 step-5 item only as a measurement. C10 stays OPEN/BLOCKING and F1 is unchanged. P2's main value is converting P1 into a pre-registered reading. It is unlikely to change steps 6 and 7 (issue 2). That is the operator's call, and the question must frame it that way.

## Proposed CORPUS/55 verdict sentence (3 sentences or fewer)

> D-C10w-oracle P1 (oracle measurement, not a route; never promotable as a write-engine result): every P1 control passed, and the pinned reader returns INCOMPLETE — no label, no routing, C10 OPEN/BLOCKING, F1 unchanged — until P2 replicates (prereg §8 item 3); step 5 is not yet read. As a single-seed, non-routing configuration reading from the reader's own `configuration()`, the rank-16 seed-0 oracle scored 70/72 held-out (same-process closed form 9/72; shuffled-control cross-score 0/72), missed G4 on 15 of 20 training frames (never-edited fictional subjects' top-1 moved to a coined-head first token, 50/120 vs 4/120), passed G6 at its boundary (4/200) and carries BIGRAM, i.e. PARTIAL-CEILING-LOCALITY-COST(G4), which cannot become PASS-CEILING at rank 16. O-A7-canon s0 scored 2/72 held-out while failing G2 (12/30) and G4, so the canonical split will be NOT-READ whatever P2 shows.
