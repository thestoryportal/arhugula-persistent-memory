> **Program correction note (2026-10-07; original text below unchanged):** the rationale's "about 3 percent installed" is backwards (ρ_c in CORPUS/44:43 is the remaining residual: ~2.8 % unrealised at the key, ~23 % on paraphrases), and "the later words have no objective" holds for the weight solve, not for `compute_z`. See `docs/INTEGRATED_QUEUE_2026-10-07.md`, "Corrections".

# Recommended experiment sequence — research pass 2026-10-06

Written for the operator in plain language. The technical mapping to hypothesis numbers, thresholds and gates is in the appendix; the detailed entries are in `hypotheses.md` and the council's amendments in `council_critique.md`. This document recommends an order; it runs nothing and promotes nothing.

## What we are trying to fix, in one paragraph

The system writes facts into the model's weights so that later agents simply know them. That works for short values (a one-word answer lands and reads back correctly on about 69 of 72 unseen phrasings). It fails for made-up two-word names, the kind a real project is full of: today such a value reads back on 12 of 72 unseen phrasings, 24 with a second write at a locality cost, and 34 to 46 when the whole name is first given its own single vocabulary token. The target is 61 of 72, with the unrelated facts around it undisturbed. Everything below is a different attempt to close that gap without changing how the system fundamentally works: a fact is still written at commit time by a solver, not learned by training.

## The ranking criteria, as agreed in this session

1. **Writing, not training.** The write must stay a per-commit solve that can be regenerated from the committed patch. Anything that needs a training set or a training loop per commit is out as a route (it breaks real-time use, the audit trail and compaction); one such arm is kept only as a measurement.
2. **Runs on this Mac now.** No rented compute; nothing that needs more than about a day of build work this week.
3. **Aimed where the evidence says the wall is.** The program's own diagnostics say the write installs only about 3 percent of its intended signal at the place it is keyed, and that the later words of the value have no objective pulling them into place. Arms aimed there rank above arms aimed at the "address" side, which already works for short values.
4. **Cheapest first within the above**, so each result arrives before the next decision.

## The sequence

| step | what we try (plain language) | why it is here | cost on the Mac | what a good or bad result tells us |
|---|---|---|---|---|
| 1 | **Make the write satisfy three phrasings of the fact at once** instead of one. Today the solver fits the value to a single sentence frame. | It is the cheapest untested change to what the solver is asked to do, and the one time paraphrases were added before they were added as extra facts, which caused interference; this version adds no facts. | one run, about 35 minutes (plus a 40-minute "is there room" check the reviewers asked for) | Good: the frame the fact was written in was part of the problem; every later arm inherits the change. Bad: the frame is not the problem, and we stop spending on it. |
| 2 | **Give the second word of the value its own address.** Keep the subject as the key and add one more key inside the value at the point the model finds most surprising. | The later words of the value currently have nothing pointing at them; this is the cheapest way to give them something, and the position is chosen deterministically from the model, so the write stays regenerable. | a few minutes of analysis, then one 35-minute run | Good: the missing objective on later words was the wall and a second key supplies it. Bad: a second key alone cannot carry it, or it bleeds onto unrelated prompts (the same-frame check will show which). |
| 3 | **Give each half of the name its own vocabulary token** (two tokens per value instead of one). | The one-token version is the only arm already above the "worth replicating" line. Splitting into two tells us whether the remaining gap is the length of the name or the newness of the pairing. | one run, about 40 minutes | Good (monotone 1 > 2 > many tokens): length is the wall and the token route is the lead. Bad (2 ≈ many): the pairing is the wall and token tricks will not close it. |
| 4 | **Choose the layer per fact** instead of always writing to the same five layers. | Fixed-band sweeps all failed; a per-fact choice is the one variant never tried, and it is a solver change only. | a few minutes of analysis, then one run | Good: some facts need a different depth. Bad (likely): depth is not the issue; the depth question closes. |
| **gate A** | If any of steps 1–4 reaches 30 of 72, **replicate it in a second process before anything else**; a single run cannot distinguish a real gain from the usual run-to-run spread. | | one more run | |
| 5 | **The stress test** (measurement, not a route): train a small adapter on the 24 facts with every phrasing and word position in the loss, merge it, and measure. We would never deploy this; it tells us the ceiling. | If even training cannot reach the bar on this model, no solver will, and the question becomes the model. If training reaches it, the wall is a missing objective that steps 6 and 7 can supply inside the solver. | about 2–3 hours, no build | Pass: spend the engine days (6, 7). Fail: move to the model axis (appendix). |
| 6 | **Change how the write is spread across layers, and weight the later words** (the program's two already-queued engine changes). | Pre-registered already; aimed squarely at the "3 percent installed" finding. Needs engine-path work under the program's isolation rules. | about a day of engineering, then one run each | Good: the engine can be fixed in place. Bad: the closed-form spreading itself is the limit. |
| 7 | **Optimise the weight change directly** against the target instead of spreading a residual through per-layer formulas. | The closest published match to the "3 percent installed" finding; keeps a per-commit, dataset-free write, though the result is slightly less reproducible than a closed form. | about a day of code, then a 1–2 hour run | Good: the realisation wall is the solver's spreading rule. Bad: the model cannot hold the value in these layers at all. |
| 8 | **Recompute the preservation statistic from the model's own text** instead of Wikipedia (background job). | A pure solver input; mostly protects existing knowledge, less likely to move the coined-value number, but cheap to run overnight at any point. | hours of unattended compute, little build | Good: the statistic was over-protecting the wrong directions. Bad: nothing lost. |
| later | A one-time trained "look-ahead head" that gives the solver a loss on the later words (setup cost, like the covariance); subject-side anchors with a temporary carrier token; a per-position write with a runtime gate. | All spec-compatible, all needing two or more days of build or an uncertain setup; sequenced after the gate decisions above. | days | |
| after the ceiling rule | Model changes that keep the write engine: the untied 7B sibling of the current model, the open 7B model pretrained to predict several tokens at once, an open-data 7B. | Only once the Qwen ceiling rule is met or overridden by the operator; each needs a covariance rebuild and new hyperparameters first. | hours of compute per model, unmeasured here | |

## Reading the numbers

- **12 of 72** is today. **5 to 18** is the normal spread of today's recipe, so anything inside it is a null.
- **30 of 72** means "worth replicating".
- **61 of 72** is the bar, and only with the unrelated-fact checks clean.
- Every run also reports the unrelated-fact checks separately: 12 real capitals must not flip, 30 unedited capitals must stay right, a described-as similarity score must not fall by more than 3 points, and the 6 same-frame fictional prompts must not take the value.

## What is deliberately not in the sequence

Routes that train per commit (adapter or full fine-tuning) as a deployment path; side stores and lookup designs (ruled an engineering fallback); methods whose public code is CUDA-only or whose checkpoints were never released; model changes before the ceiling rule.

## Appendix — technical mapping

| step | hypothesis | pre-registration points |
|---|---|---|
| 1 | H-1 | shared `compute_z` prompt set, canonical + two fixed training frames (sealed held-out templates untouched); P6 injection cell of the shared z first; LAW#5 isolation; gates per `hypotheses.md` conventions |
| 2 | H-10 (surprisal boundary) merging with H-5 (covariance leverage) after step 0 | 48 keys; same-frame probe mandatory; per-frame bystander probe per the security lens |
| 3 | H-19 | mint harness, 48 rows; per-position readout; GGUF chain |
| 4 | H-8 | per-fact layer by a deterministic criterion; step 0 first |
| gate A | — | second process for any arm ≥ 30/72; per-fact 24-vector reported |
| 5 | H-13 as oracle | labelled measurement; forgetting instrument named; phrasings from the pristine base, hashed, overlap-audited; never a route |
| 6 | H-11 (I-2 forward replay, I-1 OverTone) | existing pre-registrations in the arc; engine path |
| 7 | H-3 | direct ΔW optimisation under the null-space projector; two same-seed runs for reproducibility |
| 8 | H-4 | model-generated covariance, stats-file SHA in the manifest |
| later | H-24, H-9, H-6 | see entries |
| after ceiling | H-21, H-23, H-26 | static prefilter passed; smoke solve first |
