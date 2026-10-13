## memit-specialist

Lens: write-engine mechanics (key/value solve, W-realization, overlay/compaction contract, §8). Sources: top3.md, hypotheses.md (Conventions, H-1/H-18/H-13), spec §8, CORPUS/36.

### H-1 — shared value objective across prompt formats

1. **Objection — wrong knob by the program's own localization.** CORPUS/36's z-probe shows `compute_z` already reaches 0.99 target probability on the full multi-token target by step 25 for every value class; the wall is the linear W-edit realizing z through the subject key, and a multi-frame z is still one residual vector realized through the same `k → z` solve at one position, adding no objective where the engine lacks one.
   *Test:* log per-frame z target probability and steps-to-converge for the shared z (if it cannot reach ≈0.99 on all three frames, arm B is a degraded-z arm, not a shared-z arm), and report `canon_full`, `tf_pertok`, `P(full|first)` beside `para_full` so any gain is localized to first-token vs continuation.
   *Stub:* absent — only `para_full` is the binding count; no z-probe readout, no canon/per-token decomposition.

2. **Objection — the key side is left canonical.** H-1 keeps "one subject key"; on a held-out paraphrase the subject-last-token key k' differs from the training key k, and ΔW k' is what fires, so paraphrase failure may be key-side (k' far from k) and a shared z cannot touch it.
   *Test:* record cosine and norm of the subject-last-token key under canonical vs each held-out template, pre- and post-edit; add a shared-key arm (key averaged over the same three frames) or at minimum stratify held-out hits by key similarity.
   *Stub:* absent.

3. **Objection — "disjoint" is string-disjoint, not structure-disjoint.** If the two training forms share the question frame of the sealed held-out templates, a gain is template coverage, not cross-format transfer.
   *Test:* publish the training and held-out templates before the run with an n-gram/structural overlap figure, and report the gain per held-out template.
   *Stub:* absent — "disjoint from the held-out set" is the only statement.

### H-18 — minted token by embedding-only tuning

1. **Objection — with the model frozen there is no write; the binding must live in frozen hidden states.** Arm B has no FFN edit, so 24 trained rows must act as a 24-way linear readout of the value-slot hidden state for 24 *novel* subjects the frozen model has never separated; the Markov-matrix result concerns transitions *from* a new token, not predicting one after an unseen subject.
   *Test:* before tuning, fit a linear probe on the frozen value-slot hidden states for the 24 subjects and report its accuracy; after tuning, report the full 24×24 confusion of minted ids across subjects, not a scalar.
   *Stub:* "cannibal 0" is a scalar; no probe of frozen-state separability, no confusion matrix.

2. **Objection — tied embeddings make the tuned row an output-side attractor.** Gradient on the minted id's logit moves the unembedding row; any hidden state with a component along it gets the minted id raised at every position, so softmax-relative forgetting of old tokens is non-zero.
   *Test:* minted-id false-fire rate on the 12 real-country, 30 unedited-capital, and same-frame prompts plus top-k intrusion rate on the generic perplexity set, and the generic perplexity gate itself.
   *Stub:* L1/L3/`described_as` present; perplexity gate and minted-id intrusion rate absent.

3. **Objection — comparator confounds gradient-on-row with paraphrase diversity.** Arm B differs from A7-mint-N in both optimizer and data, so a win cannot be attributed to "how the row was written."
   *Test:* two controls — row tuned on the canonical prompt only, and MEMIT write + tuned row.
   *Stub:* absent — two arms, two seeds only.

4. **Objection — spec labelling is wrong.** If the binding is carried by a trained embedding row, the write is not a §8.1 FFN compile and §8.10 compaction (full MEMIT re-run) has no procedure to re-derive it; "spec-amendment none" does not hold.
   *Test:* pre-register a pass as "embedding-side write" with the §8.4/§8.10 overlay-and-recompile question explicit.
   *Stub:* absent.

### H-13 — merged band-LoRA write

1. **Objection — D20 safeguards are dropped, not relaxed.** §8.2 makes orthogonal projection and the covariance balancer mandatory; a LoRA delta has neither, and the stub's ΔW Frobenius ratio ≤ 1.5 is a norm qualifier, not a null-space or covariance constraint — a small delta concentrated in high-covariance key directions does more damage than a larger one in the null space.
   *Test:* report the covariance-weighted norm ‖ΔW C^{1/2}‖ per layer and the fraction of ΔW energy in the top-k covariance directions, for both writers.
   *Stub:* absent; "generic-capability probe with a pre-set floor" has no number and must be fixed before the run.

2. **Objection — a pass may be value-internal bigram learning, not a bound fact.** Loss at continuation positions conditions on the previous value tokens, so LoRA learns "Vindex → Vask" with the subject only in attention context; that converts coined values into A2-style prior-coherent ones (98.6%) without binding them to the subject.
   *Test:* forced-first-token continuation on unedited and same-frame subjects (does "Vindex" → "Vask" fire regardless of subject), plus the CORPUS/36 decomposition (first-token, `tf_pertok`, `P(full|first)`).
   *Stub:* same-frame probe present; forced-first-token leakage and decomposition absent.

3. **Objection — self-generated phrasings cover the sealed templates.** The model generates the common question frames, where the held-out templates live; the source's 900 disjoint-template items do not transfer to 24 × 20 self-generated ones.
   *Test:* as H-1 (3) — overlap figure and per-template reporting.
   *Stub:* absent.

4. **Objection — merged single-batch says nothing about §8.3 incremental mode or §8.10 recompile.** A LoRA write has no deterministic re-run; retraining under a new seed is a different overlay.
   *Test:* two training seeds with per-subject agreement reported; label the result single-batch-only.
   *Stub:* absent — one seed implied.
