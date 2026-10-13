FIX-FIRST

Reviewer: Claude Opus 5.5, independent adversarial pass, read-only, 2026-10-07. Inputs verified by hash: prereg sha256 d2aa240e… (matches reader PREREG_SHA, `experiments/track_c/c10w_oracle_read.py:20`); reader sha256 162966119c…, equal to the step-0 pin (`results/c10w_oracle/step0_20261007T223638_531381Z/step0.json` sources.reader = 16296611…). I re-ran `validate_phase` and `configuration(P1,"oracle_p1")` by importing the pinned reader unmodified, with no writes. Both reproduce `interim_reader_configuration.json` exactly. (This file replaced an earlier report at this path, which had no first-line verdict; that earlier text is preserved in the session scratchpad as `c10w_p1_verdict_advisor.prior.md`. Its conclusions agree with this one.)

## Single most important thing

P1 has already settled two things the brief lists as open. Correct this in CORPUS/55 and in the operator's P2 question before either goes out.
- **The canon split is already NOT-READ (c).** `canonical_split` requires G1–G6 to hold at both seeds (`c10w_oracle_read.py:402–405`; prereg `:388`). O-A7-canon s0 already fails G2 (L3 12/30) and G4.
- **Rank 16 cannot reach PASS-CEILING or give a gate-clean reference.** The replicated gate-miss set is the union over both seeds (`read.py:382`), and seed 0 already misses G4. The PARTIAL reference rule needs a rank with no gate misses (`read.py:461–464`; prereg `:395`), so P2 cannot clear it.

P2 can therefore buy only three things: a replicated count with a final label of LOCALITY-COST or PARTIAL, a diagnosis of -UNSTABLE, or eligibility for P3. Only P3 (rank 64) can produce a PASS-CEILING or a gate-clean reference. The operator should authorize P2 knowing this.

## Verification of the brief's facts

Every fact below was checked against the files.
- **Fact 1 (holds).** Fit is 480/480 for O-A1, O-A2, O-A7 and O-A7-shuf and 24/24 for O-A7-canon, all at 400 steps. Training wall times are 409.7, 523.4, 372.1, 422.1 and 500.0 s, which is 6.2–8.7 min each and 37.1 min in total (`eval.json` train_records). Preflight took 3590 s (`preflight.json` wall_seconds). Eval took 5773.7 s, which is 96.2 min, not 95 (a trivial difference). The authorization of 592 min matches `authorization_P1.json:6`.
- **Fact 2 (holds).** `eval.json` status is PASS and all six validity flags are true. LAW#5(i) gives expr_delta 0.0004 and loc_delta 0.27 in all three recipes. Zero and trained hit counts are 1/1 and 5/5. Closed-form A7 is para_full 9, para_first 52, canon 9; A1 is 72 and A2 is 70; U A7 is 0/72 with stimulus base 0. Everything is inside the `read.py:148–154` envelope.
- **Fact 3 (holds).**
  - `verdict.json:4–8` gives status INCOMPLETE, final_label and routing null.
  - Projections are P2 178.04 and P3 138.25 min (`verdict.json:171–172`). The P2 figure re-derives from `read.py:477` with the recorded basis.
  - The `stop` string is at `verdict.json:192`.
  - Exit code 2 comes from `read.py:626`. The JSON printed to `results/c10w_oracle_logs/p1-project.log` shows `disk_phases` did not Halt.
- **Fact 4 (holds).**
  - O-A7 s0 count is 70/72, a gain of 61 over the closed form; mounted is also 70.
  - G4 misses. The oracle's training-frame flips vector and the closed form's vector are exactly as the brief states, and the canonical frame is 1 vs 1.
  - The shuffled control scores 71/72 on its own map and 0/72 cross-scored against the original map.
- **Fact 5 (holds, with additions).** O-A7-canon scores canon 24/24, para_full 2/72, para_first 5/72; L3 is 12/30 with KL 3.185; L1 top-1 changed 6/12, though L1 flipped-to-edited-value is 0. The brief omits that the reader's gates for this arm give **G2 = False and G4 = False** (canon frame 3 vs 1; T01 3, T13 4 and T15 3 against a closed-form 1/1/1). The brief also omits that -BIGRAM fires on this arm.
- **Fact 6 (holds).** O-A1 and O-A2 are both 72/72.

Nothing in P1 is invalid or misread, and the G4 denominators are correct. Each frame row is validated at n = 6 with a raw-row sum (`read.py:208–212`). G4 compares each training template against the same template in the closed-form arm (`read.py:265`; prereg `:354`).

## Issues, in priority order

1. **BLOCKING — the canon split and the rank-16 reference are misstated as depending on P2.**
   - The brief's fact 5 says "Canon split needs P2". Under the frozen reader the split's only possible outcome is already (c) NOT-READ:
     - G2 is False because L3 is 12/30 against the 29/30 rule (`read.py:263`; prereg `:352`), and G4 is False for O-A7-canon s0.
     - `canonical_split` ANDs all G1–G6 at both seeds (`read.py:403`), so nothing P2 measures can make the split readable.
   - Rank 16 cannot be gate-clean. Seed 0's G4 miss enters every replicated rank-16 label (`read.py:382`), and the PARTIAL-with-(c) reference rule needs gate misses to be empty (`read.py:462`).
   - Consequences:
     - If the final label stays at rank 16, it is PARTIAL-CEILING-LOCALITY-COST or PARTIAL-CEILING, carrying reference_status NO-GATE-CLEAN-REFERENCE (prereg `:395`).
     - PASS-CEILING and any reference count are reachable only through P3 at rank 64 (prereg `:372–384`).
   - CORPUS/55 and the operator question must say this. Without it the operator is told that P2 still decides the canon split and the reference, which is false and inflates what the 178-min P2 can deliver.
   - These are structural consequences of frozen rules applied to recorded data, not a final label, so stating them does not breach §8 item 3 (prereg `:532`).

2. **ADVISORY (high) — G6 passes exactly at its boundary, which creates a concrete -UNSTABLE risk in P2.**
   - The facts:
     - O-A7 s0 has a net paired MMLU loss of 4/200 (13 correct-to-wrong, 9 wrong-to-correct). The limit is ≤ 4 (prereg `:356`, `:368`; `verdict.json:131`). The affected `college_physics` items contribute 0.
     - The matched shuffled control loses 9 and O-A2 loses 5 (`verdict.json:119`, `:143`).
   - The risk: the same-seed retrain must reproduce seed 0's entire G1–G7 pass/fail dict (`read.py:390`; prereg `:370`). A retrain at net loss 5 makes P2 -UNSTABLE, which means no label, no routing and no P3.
   - CORPUS/55 must report G6 as "pass at the 4/200 boundary", not as a plain pass. The operator question should name this as a live P2 outcome.

3. **ADVISORY — the interim reading is permitted only as a per-configuration record, never as the result.**
   - §3 separates per-configuration labels from replicated and final labels (prereg `:329`, `:359–365` vs `:370–384`). §8 item 3 forbids only the final label and routing. A seed-0 `configuration()` output computed by the pinned reader is a reader-computed intermediate, which `:287` allows.
   - Required wording:
     - The headline status is **INCOMPLETE**.
     - The configuration result reads "seed-0 per-configuration reading (§3), interim, non-routing, not replicated, not a final label: PARTIAL-CEILING-LOCALITY-COST(G4), qualifier -BIGRAM".
     - No sentence may say the measurement "is" PARTIAL-CEILING-LOCALITY-COST.
   - `verdict.json:8` `"p3_required": false` is the default for an INCOMPLETE reading (`read.py:421`, `:429`), not a determination. Do not cite it as "P3 not required".

4. **ADVISORY — -BIGRAM must be stated, with what it measures.**
   - For O-A7, all 24 facts are eligible and none excluded. C = 24 and X = 17, against a threshold of ⌈24/2⌉ = 12 (`read.py:253–255`; prereg `:230`). Within X:
     - s_k = 1 for 13 facts: the swapped subject emits fact k's modifier after k's head.
     - n_k ≥ 0.5 for 13 facts, with a mean n of 0.486.
     - b_k = 0 for all 24: the head-sharing sibling never emits fact k's modifier.
   - Plain meaning: in most facts, the modifier that follows the head does not depend on the subject when the subject is a never-edited or swapped one. The only place the adapter separates modifiers is between the two subjects that share a head. That is all the benchmark checks, so 70/72 coexists with substantial continuation leakage.
   - Prereg `:230` requires "benchmark success with measured continuation leakage, without a stronger binding claim".
   - For contrast, the closed form gives C = 9, X = 0. -BIGRAM also fires on O-A7-shuf (X = 13) and on O-A7-canon (X = 15).

5. **ADVISORY — the locality cost is broad and recipe-wide, not marginal. CORPUS/55 should not let a reader skim it.**
   - G4 misses on **15 of 20** training templates, reaching 5/6 at T08. The canonical frame alone (1 vs 1) would have hidden it.
   - Reported-only readouts for O-A7 (`eval.json` recipes.oracle_p1.arms.A7_coined_coined.extra):
     - held-out-template frame flips are 2/2/2, against 0/0/0 for the closed form;
     - the `is a` relation flips on 23/24 edited subjects and `is associated with` on 12/24;
     - L3 mean KL is 1.07 against 0.0, with top-1 still 30/30.
   - The O-A1 positive control shows the same pattern: canonical frame 6/6 and training frames 3–6/6. The induced prior toward coined vocabulary in trained frames is therefore a property of the recipe, not of A7.
   - Also report: para_first 72/72, cond_full_given_first 0.972, per-template 22/24/24, and per-edge 3/3 on 22/24 facts. Per prereg `:23`, a high count does not mean every fact passes per-edge.

6. **ADVISORY — the P3 conditional authorization is consistent with the prereg if the record states its full conditions.**
   - Why it is consistent:
     - §8 item 3 and §2.8 `:280`, `:285` require a recorded **post-P1** authorization before each phase. They do not require that P3's authorization be recorded after P2.
     - The reader enforces the scientific condition mechanically: P3 entry requires `p3_required` (`read.py:537–539`), and P3 is refused after LOCALITY-COST (`read.py:435`, `:444`).
   - The record and the question must also state the following:
     - (a) P3 runs only if rank 16 is stable as well as PARTIAL or FAIL.
     - (b) After P2, the remaining-time projection is updated and must stay within 327 (prereg `:314`, `:316`).
     - (c) The 138-min figure uses rank-16 training timing; rank-64 timing is unmeasured (`verdict.json:186`).
     - (d) With s0 = 70 and G4 already in the union, P3 is reachable only if 55 ≤ s1 ≤ 60, the retrain stays ≥ 61 and within 10, and the retrain's gates are identical. If s1 ≤ 54 the seed gap exceeds 15 and the result is -UNSTABLE; if s1 ≥ 61 the label is LOCALITY-COST and P3 is excluded. This narrow window is the realistic trigger and should be stated.
   - Bundling P3 into the same question is acceptable and saves a human-in-the-loop round trip. Asking separately after P2 is equally valid.

7. **ADVISORY — `interim_reader_configuration.json` lacks the record identity the prereg requires.**
   - Prereg `:324` says every JSON carries `class` and the Decision-ID. This file carries neither, nor the `eval.json` SHA-256 it was computed from, nor the scratch script's source or hash. Only reader_sha256 is present (`interim_reader_configuration.json:2`).
   - My independent re-run reproduces it, so the content is correct. Before CORPUS/55 cites it, write a new sidecar file containing class, decision_id, the `eval.json` sha256 and the script source sha256. Do not overwrite the existing file (prereg `:322`).

8. **ADVISORY — scope language for 70/72 (question C).**
   - The following may be said:
     - an attained, unreplicated seed-0 count for one finite LoRA recipe on the five band `down_proj` matrices;
     - held-out but on a test-aware benchmark (prereg `:64`);
     - with the shuffled control clean (cross-score 0/72, gap |70 − 71| = 1).
   - The following may not be said:
     - an upper bound, or a ceiling on this model;
     - evidence that a missing objective is the cause;
     - anything about the canonical-only contrast (O-A7-canon got 2/72, below the closed form's 9, but it is an unmatched fixed-update ablation; only the routing split reads it, prereg `:53`);
     - any change to C10 or F1;
     - any write-engine claim (prereg `:3`, `:399–408`).

Drift check: this is the live §0.3 step-5 oracle and advances the F1 determination only as a reference measurement. No drift.

Overturning test: the cheapest falsifier of "70/72 at rank 16 is a stable seed-0 attainment" is P2's same-seed retrain together with seed 1. It is the next unit regardless. No extra control is needed before P2.

## Proposed CORPUS/55 verdict sentence

D-C10w-oracle P1 (oracle measurement, not a route; C10 OPEN/BLOCKING, F1 unchanged): every P1 validity control passed (5/5 fits at 400 steps, LAW#3 closed-form A7 9/72 in envelope, LAW#5 inert, O-A1/O-A2 72/72), and the frozen reader returns INCOMPLETE, with no final label and no routing until P2 replicates. The seed-0 rank-16 O-A7 adapter reached 70/72 held-out full-sequence (closed form 9/72; mounted 70; shuffled cross-score 0/72), while missing G4 on 15 of 20 training frames, passing G6 only at its 4/200 boundary, and carrying -BIGRAM (17 of 24 facts' modifier continuation fires off-subject); this is an interim, non-routing per-configuration reading of PARTIAL-CEILING-LOCALITY-COST(G4)-BIGRAM. Under the frozen rules, that seed-0 G4 miss enters every rank-16 replicated label, so rank 16 can yield neither PASS-CEILING nor a gate-clean reference, and O-A7-canon s0 (2/72; G2 fails at L3 12/30) already fixes the canon split at NOT-READ.
