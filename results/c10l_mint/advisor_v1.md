**Verdict: FIX-FIRST**

**Do this first:** build init G without the subject, and measure each init's paraphrase recall before any write. Every arm should then be read as its gain over that init's own step-zero recall. As written, G can carry the answer before the edit happens. That would produce a false SPAN result, which is the reading most likely to be promoted.

I couldn't verify anything against the repo or arXiv. The repo-search (graft) and arXiv tools were both denied in this session. So every citation in the prereg is **`UNVERIFIABLE`** from my side: CORPUS/36–39/43, `c10e_bandknob.py`, `c10k_keying_ablation_keygram.py:13–17`, and arXiv 2604.02324, 2505.20133, 2504.21018 and 2609.29045. The model facts in §2 (tied embeddings, 151,936 rows, hidden size 2048, 151,665 used ids, so 271 spare rows) match what I know of Qwen2.5-3B, but that is my inference, not a re-check. Before §0 is written, someone should re-open the two papers that carry weight here (2604.02324 and 2609.29045) and the harness lines that tokenise `target_new` and compute `para_full`.

## Issues, most important first

**1. G can leak the answer, and it points the wrong way for a tied head.**
- **Leakage.** §4 builds G from the value's hidden state "inside the canonical frame". If that frame contains the subject, the row stores the subject→value link before the write. A7-mint-G could then pass with no help from MEMIT. Build G in a frame with no subject: the value alone, or a neutral carrier like `"The name is {value}"`.
- **Wrong position.** The hidden state at the value's *last* token predicts what comes *after* the value. Because the embeddings are tied, that row is also the output vector, so it will score high wherever the model "has just said a name". That is a recipe for a cannibal token. P-iv also fails to warn that final-layer states are strongly anisotropic, so G may collapse just as M is expected to.
- **A step that does nothing.** "Least-squares projection onto the embedding matrix's column space" is the identity: the embedding matrix spans all 2048 dimensions. Either delete it, or name the real operation. Candidates: take the state after the final RMSNorm (that is what multiplies the head), subtract the mean hidden-state direction, then rescale the norm.

**2. The step-0 drop rules contradict the arms.**
- "≥ 20/24 dead means not writable" is wrong. A random row (N) *should* be dead at step 0, and N is a planned arm in §5. Being dead before the write is the healthy state for a new token. Whether the write can reach it is what P3 (does `compute_z` converge) tests.
- The real danger runs the other way. A row that is already **live** at the value slot before the write contaminates the result.
- Fix: drop "dead" as an exclusion. Exclude only cannibal tokens, plus any init with step-0 `para_full` above 0 by more than a small preset margin. Report every arm as post-write minus step-0.

**3. The SPAN bar sits above the harness's own ceiling, and the comparator mixes two variables.**
- SPAN needs ≥ 65/72. The A1 control (real single-token value) only has to reach ≥ 58/72. If A1 usually lands near 60, A7-mint can never read SPAN, even if the span is the whole wall.
- Make the bar relative to A1 in the same run, for example A7-mint-G ≥ A1 − 5.
- A1 also differs from A7-mint in two ways at once: the value is familiar, and it is plausible for the relation. Consider an extra arm whose value is an existing rare single token that is implausible for the relation. It needs no tokenizer surgery and no init choice. With it you get a clean ladder: real and plausible (A1), real and implausible (new arm), minted (G/N).

**4. P2 checks almost nothing as written.**
- Writing spare rows cannot change the logits of existing ids. Their hidden states and their own rows are unchanged.
- What it does change is the softmax denominator. So "probabilities identical to fp16 tolerance" may fail for a harmless reason, while the real risk goes unchecked.
- The real risk is tokenisation: added tokens are matched before BPE. Any prompt containing a coined value string would now tokenise differently. That includes locality prompts, `described_as`, and the other arms' templates.
- Restate P2 as two checks:
  - (a) For every prompt the harness feeds the model, the token ids are identical before and after registration.
  - (b) Within that, the minted ids' rank on unrelated prompts, which is just the I-11 cannibal check.
- Also add an assertion: `tok(" " + coined) == [ĥ]`, run with the same tokenizer object the engine's `compute_z` uses.

**5. Collinear rows need a sibling-confusion metric.**
- P-iv's mechanism is that a write which boosts token *i* also boosts token *j*. On the binding metric, a miss caused by top-1 being *another minted token* looks the same as any other miss.
- Add `para_sibling`: top-1 is a different minted id. Without it, the reading of the M arm ("lower `para_full` and more cannibals") can't tell collapse apart from failure.

**6. Read the multi-token baseline per token.**
- For the multi-token baseline, full-sequence accuracy is roughly the per-token rate raised to the 5.5th power. The span hypothesis therefore makes a sharper prediction: minted accuracy should approach A7-multi's *first-token* and per-token paraphrase accuracy.
- Report A7-multi's `para_first` and its per-position accuracy (whether the harness already logs these is `UNVERIFIABLE`). Without them, PARTIAL can't be interpreted.

**7. Some readings over-claim.**
- **SPAN:** "option (iv) is a route" confuses mechanism with contract. A pass at N = 24 shows the span is the wall *here*. Being a route also depends on capacity: 271 spare rows, beyond which you need a resize, which breaks the "no shape change, GGUF sees the same tensors" premise. Reword to "span is the wall at N = 24; route viability is open under capacity and lifecycle", and say in §7 that 271 is a hard ceiling.
- **NOVELTY:** if every init fails, that could be a property of minted output rows, not of novelty. "(iv) closed with these inits" is supported. "The wall is not the span" is not, unless the rare-real-token arm from item 3 also fails.

**8. Spare-row starting values are unmeasured.**
- The 271 spare rows were never fed as inputs, but under tied weights they still received softmax gradient during pretraining. They probably sit in a "never emit" direction.
- Record their current values and step-0 ranks as a fourth reference init, "as-is", in step 0. Then N's "matched-norm random" can be compared with what the model already learned for unused ids.

**9. Smaller points.**
- The P-iv threshold of effective rank ≥ 12 should be anchored to the base-vocabulary reference you already compute, for example ≥ 0.75 × the reference. A fixed 12 ignores embedding anisotropy.
- The M collapse prediction (mean cosine > 0.9) is probably too strong for averages of about 5 tokens. That's fine because it is falsifiable. But check whether 2604.02324's collapse is about the *initial* geometry or the geometry *after fine-tuning*. The prereg leans on the first, and that is `UNVERIFIABLE` here.
- State that the edited embedding rows never enter the solve: covariance stats and keys are unaffected because minted ids never appear as inputs. That is the LAW#5 inertness argument for this weight change. As written it is only implied.

## Cheapest test that could overturn it

Reanalyse the existing A7-multi results for first-token paraphrase accuracy. This needs no new run.
- If first-token accuracy is already about as low as full-sequence accuracy (around 15–27%), the span alone can't explain the wall. The NOVELTY prior strengthens before you spend anything.
- If it is high, the SPAN prior strengthens.

The second cheapest is the rare-real-single-token arm from item 3: one harness run, with no tokenizer change and no init choice.

## Drift check

This advances F1. It is the span-vs-novelty falsifier on the live C10 line, and it sits inside the queue that D-C10k-rulings-2 allows. To keep it on F1, the SPAN reading must not be written up as route viability (item 7).
advisor exit 0
