FIX-FIRST. The chosen option (keep the five published `dev` rows, record the duplicate) is the right one and the amendment is genuinely pre-observation. Four text and assertion fixes are needed before it is re-frozen and the code change runs. None of them changes the option.

Reviewer: Claude Opus 5.5 advisor subagent (independent adversarial review), 2026-10-07. Reviewed: `docs/C10W_ORACLE_PREREG.md` §9 (lines 534–544), the header (line 3) and the §2.6 marker (line 220), as committed in `e6a9db3` (file SHA-256 `22c01f9f…`; frozen v2.2 = `fb1788b`, SHA-256 `2baeb4e9…`, matching `experiments/track_c/c10w_oracle_read.py:20`).

**Most important next step.** Before the fresh step 0, add an explicit revision assertion (B1). Then replay the amended `freeze_mmlu` offline against the cached arrow files with the local tokenizer. I have already run that replay model-free (results under "What I verified"). The fresh step 0 should still do it as part of the test-first change.

## What I verified myself (read-only; no model loaded; tokenizer only)

- **Dataset facts (cache at `hf_cache/hub/datasets--cais--mmlu/snapshots/c30699e8356da336a370243923dbaf21066bb9fe/all/*.parquet`, cross-checked against `hf_cache/datasets/cais___mmlu/all/0.0.0/c30699e8…/mmlu-{dev,test}.arrow`):**
  - `dev` has 285 rows: 57 subjects, each with exactly 5 contiguous rows. `test` has 14,042 rows.
  - `college_physics` is the **only** subject in the whole `dev` split with fewer than 5 distinct rows. It has 4, whichever of the three equivalence tests is used: the step0.py:199 hash (`json.dumps` with the default `ensure_ascii`), the step0.py:189 identity hash (`ensure_ascii=False`), or question text alone.
  - Rows 50 and 53 are identical in subject, question, choices (`['4','5','6','20']`) and answer (0). This is the refracting-telescope item.
  - `random.Random(20261007).sample(range(14042), 200)` yields `college_physics` at source indices **1427 and 1453**, at sample positions 53 and 84, and nowhere else. The sample covers 52 subjects.
  - No sampled test question appears verbatim in `dev` (leakage check: 0 of 200).
  - Every §9 dataset claim (prereg:536) is therefore **true** on this revision.
- **Amended prompt build replayed offline** with the step-0 prompt code (step0.py:194–203) and the local tokenizer at `hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f19…` (offline):
  - Letter ids are `[362],[425],[356],[422]`.
  - **0 of 200** items fail the `Answer:` suffix-concatenation check.
  - The `college_physics` prompts, with the duplicate kept, are 518 tokens (1427) and 495 tokens (1453), and both pass.
  - The 200-prompt median is 503 tokens and the maximum 2,295.
  - With the five-row rule, nothing else in `freeze_mmlu` is expected to halt on this revision, *given* the same revision (see B1).
- **Pre-observation: TRUE.**
  - `run_step0` (step0.py:215–240) does no model forward pass before `freeze_mmlu` at :240.
  - Harness import loads the model (`c10e_bandknob.py:45–49`) and builds stimuli and locality sets from JSON only (`build_locality_sets`, which reads the screen files). `tgt_ids` is tokenization only (`c10e_bandknob.py:67–68`).
  - The halted directory holds `HALT.json`, `seal_audit.json`, `step0.log` and `train_inputs.json`. There is no `mmlu200.json` and no `step0.json`.
  - The log ends `HALT: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required` / `STAGE_EXIT=2` (`results/c10w_oracle/step0_20261007T220253_584752Z/step0.log`).
  - No adapter, no MMLU score and no readout exists.
  - The author has seen dataset content (the duplicated rows and the two affected test indices), but no model behavior. The choice cannot be outcome-informed.
- **Provenance of the "distinct" clause (the packet's question 4).** §7 records that advisor #10's "five-dev-items assertion" was applied "through Codex #7's text" (prereg:467, :476). The two sources differ:
  - The **advisor's** original text is "asserts a `subject` column and exactly 5 `dev` items per subject used". It does not contain "distinct" (`results/c10w_oracle_advisor_v1.md:164`).
  - The word **"distinct" was introduced by Codex #7's replacement text**: "require exactly five distinct dev exemplars" (`results/c10w_oracle_codex_design_v1.md:115`).
  - Codex #7's evidence paragraph (`codex_design_v1.md:109`) gives a rationale only for the revision and order pin, not for "distinct". Codex's purpose for the word is therefore **UNVERIFIABLE** from the record.
  - §9 (3) attributes the clause's purpose to the advisor and is silent that the specific word came from a BLOCKING Codex item (see B3).
  - The amended rule, five rows, is word-for-word the advisor's original assertion. That strengthens the amendment, and §9 should say so.
- **Rejected options.** I agree with all three rejections. (b) and any "re-seed" variant change the frozen 200 items. (c) is a per-item non-standard prompt. (a) changes the published few-shot set; one sub-claim of (a) is imprecise (A6). I see no better option: the chosen prompt is the literal published five-shot set and needs no rule beyond a row count.

## BLOCKING

### B1. The "revision pin" that §9 relies on does not exist in code; a fresh step 0 re-resolves HEAD

- §9 says "On the pinned revision `cais/mmlu@c30699e8…`" and "Nothing else changes: the revision pin, …" (prereg:536, :538).
- The code resolves the **current HEAD** at run time: `revision=HfApi().dataset_info("cais/mmlu").sha` (step0.py:177). It then records that revision but does not pin it. The prerun Astra review already flagged this (`results/c10w_oracle_prerun_astra.md:22`).
- The halted run left no record of which revision it resolved, because `mmlu200.json` was never written.
- c30699e8 is an I-INFER from two sources: the only snapshot and arrow directory in the cache is c30699e8, created 14:36, before the 16:02 run (a different HEAD would have created a second cache directory); and the prerun advisor's live `dataset_info` call (`results/c10w_oracle_prerun_advisor.md:80`).
- Every §9 argument is specific to c30699e8: which subject is affected, that only 2 of 200 items are touched, and that the 200 items are unchanged. If HEAD moves before the fresh step 0, the sample, the affected items and the duplicate summary can all differ, and the amendment's reasoning would no longer describe the instrument.

**Replace** the last sentence of the "Change" paragraph (prereg:538), from "Nothing else changes: …" to the end, with:

> Step 0 additionally requires the resolved `cais/mmlu` revision to equal `c30699e8356da336a370243923dbaf21066bb9fe`, the revision this amendment was written against; any other revision is INVALID-INSTRUMENT and returns the design to review. Nothing else changes: the seed, the 200 sampled items, the prompt format, the letter-logit scoring, the tie order, the token checks, G6 (net paired loss ≤ 4/200) and the rule that every phase consumes the one `mmlu200.json` by SHA-256.

**Also replace** "On the pinned revision" at prereg:536 with "On revision". Add a matching `R.require(revision=="c30699e8…", …)` in the test-first code change.

### B2. §9 (2) over-claims: "the duplicate cannot by itself move the gate in either direction"

- The duplicate is shared by U and every arm, so it introduces **no difference between arms**. That part is right.
- The over-claim is in the comparison with the instrument the prereg would otherwise have produced. Any different prompt for items 1427 and 1453 (four-shot, or a replacement row) could change whether those two items are discordant. The prompt choice can therefore shift net loss by up to 2 of 200, and G6's boundary is 4 versus 5 (prereg:223). A shift of 2 can cross it.
- The honest claim is no bias plus a bounded instrument-choice effect, fixed before observation. It is not "cannot move the gate".

**Replace** §9 (2) (prereg:540, from "(2) The duplicate touches only" through "in either direction.") with:

> (2) The duplicate touches only the prompts of the two `college_physics` items (source indices 1427 and 1453, sample positions 53 and 84), and identically for arm U and every edited arm. G6 is a paired comparison against U on the same frozen prompts, so the duplicate introduces no difference between arms. Compared with any other prompt choice for those two items, net loss could differ by at most 2 of 200. That choice is fixed here, before any model observation, and does not depend on any outcome.

### B3. §9 (3) misstates where "distinct" came from

- The record shows that the advisor's assertion was a row count (`advisor_v1.md:164`), and that "distinct" entered in Codex #7's BLOCKING replacement text (`codex_design_v1.md:115`) with no stated reason.
- The amendment narrows a BLOCKING reviewer's wording. It should say so plainly, so that GPT-6-Astra, the same family as the Codex reviewer, can rule on it with the right facts.

**Replace** §9 (3) (prereg:540, from "(3) The clause came from" to the end of the paragraph) with:

> (3) The advisor's original assertion was "exactly 5 `dev` items per subject used" (`results/c10w_oracle_advisor_v1.md:164`); the word "distinct" entered in Codex #7's replacement text (`results/c10w_oracle_codex_design_v1.md:115`), which gives no separate reason for it (its rationale, `:109`, concerns the revision and row order). This amendment restores the advisor's row-count assertion exactly and narrows Codex #7's text by one word, because the source does not have the property that word requires. Codex #7's other requirements (pinned revision, ordered source identities, frozen prompt bytes and token ids, one shared `mmlu200.json`) are unchanged. The duplicate is recorded rather than hidden, so a reader can see that one subject's five-shot set has four distinct exemplars.

### B4. Stale and incomplete "what ran" statements

- **Header (prereg:3)** still says "Nothing has run; no driver exists." That is false now: the four drivers exist (`experiments/track_c/c10w_oracle_{step0,train,eval,read}.py`) and one step 0 ran and halted. The amendment sentence was added on the same line, so the line now contradicts itself.
  **Replace** "Nothing has run; no driver exists." with:
  > At freeze, nothing had run and no driver existed; since then one step 0 has run and halted before training (§9).
- **§9 "What happened" (prereg:536)** says that "the only work done before the halt was the seal audit and the training-input freeze". That is incomplete. Before the halt, the run also:
  - ran the engine fingerprint (step0.py:217, 101–104);
  - loaded Qwen2.5-3B fp16 onto MPS (`step0.log`: "loaded Qwen/Qwen2.5-3B");
  - checked the environment (step0.py:107–112);
  - downloaded or loaded the dataset;
  - built and tokenized the first 53 MMLU prompts (sample positions 0–52, before 1427).

  None of these involved a forward pass or an outcome, but "only" is wrong.
  **Replace** that clause with:
  > before the halt, step 0 ran the engine fingerprint, loaded the model and checked its environment, wrote the seal audit and the training-input freeze, and built and tokenized the first 53 sampled MMLU prompts; no forward pass ran.

## ADVISORY

- **A1. Use one hash for distinctness.**
  - The amended record counts distinct rows "by row SHA-256". The code has two row hashes: identities with `ensure_ascii=False` (step0.py:189) and the check at :199 with the default `ensure_ascii`.
  - They give the same partition on this revision (verified: 4 and 4), but the record should use `identities["dev"][i]["row_sha256"]` so that one source of truth defines "duplicate".
- **A2. The code diff needs a reviewer, not only the amendment.**
  - §9's procedure has the amendment reviewed "before the code change runs", but nobody is named to review the change itself: step0.py:199, the new duplicate summary, the revision assertion (B1), read.py:20 `PREREG_SHA` and the new test.
  - `load_frozen` re-verifies every recorded source hash (read.py:483–488), so the post-change sources become frozen inputs.
  - Recommendation: put the diff and the test in the GPT-6-Astra packet, or run a short post-diff check, before the fresh step 0.
- **A3. The test-first test should use the real data, not only a synthetic shape.**
  - Alongside the synthetic case (five rows, two identical), assert on the cached c30699e8 arrow files:
    - exactly one subject with fewer than 5 distinct rows (`college_physics`, duplicate indices [50, 53]);
    - the affected sampled items are [1427, 1453];
    - 0 of 200 suffix failures.
  - My offline replay above shows these all hold. The check is model-free and takes about a minute.
- **A4. Process lesson for memory.**
  - The prerun advisor reported that it "replicated `freeze_mmlu` offline … 0 of 200 failures on the `Answer:` suffix concatenation check" (`results/c10w_oracle_prerun_advisor.md:81`). Its replication cannot have included the step0.py:199 distinctness assert, or it would have halted at sample position 53.
  - A replay of a gate must run every `require` in the replayed function, not a chosen subset. This is worth a one-line memory entry.
- **A5. Diagnostic completeness.** `architecture_profile/c10w_oracle_step0_halt_diagnostic.json` states the revision but not how it was established. Add the evidence: the single cache directory created at 14:36, and `prerun_advisor.md:80`.
- **A6. Wording in rejected option (a).** "can draw from the scored pool" is true only for `test`, not `validation`. Suggested text: "(a) Replacing the duplicate with a row from `validation` or `test`: changes the published five-shot set and, if drawn from `test`, can draw from the scored pool."
- **A7. Optional sensitivity, report-only.**
  - Per-item correctness bits are already recorded for every arm (prereg:221), so G6 without items 1427 and 1453 (198 items) can be derived later without a prereg change.
  - If the program wants it reported, declare it now as report-only, never a gate, to avoid a post-hoc fork.
- **A8. UNVERIFIABLE here (no network):** "which is how the benchmark's five-shot prompt is normally built" (prereg:540). The reference implementations (the Hendrycks `evaluate.py`, lm-eval-harness) were not checked. The claim is low-stakes, because the prompt format itself is fixed by §2.6 and matches step0.py:194–201.
- **A9. Ledger.** `D-C10w-dupdev` currently appears only in the prereg; I found no hit in `EXPERIMENT_RUNBOOK.md`, `SESSION_CHECKPOINT.md`, `docs/` or `architecture_profile/`. Per the close-out gate it needs a runbook §5/§13 line.
- **A10. Fresh-directory mechanics are sound.**
  - `latest_directory` takes the lexically newest `step0_*` and refuses one that contains `HALT.json` (read.py:474–480).
  - A new UTC-stamped directory sorts after `step0_20261007T220253_584752Z`, so the halted directory cannot be picked up.
  - The S7 regex parse (step0.py:129–131) is unaffected, because §9 adds no `| Tnn | ACCEPT |` rows.

## Drift check

This advances the live step-5 falsifier (D-C10w-oracle, H-13) by making its forgetting instrument satisfiable without changing the sampled items or the gate. It is instrument repair, not drift.
