## aisecops-specialist

Lens: who writes, under what verification, with what footprint, and what the audit record can prove afterwards. Read against §10.2 (Gate checks 9–11), §10.3 (scope = entity type + relation family + tier), §10.6 (Genesis human review), C16 (filesystem writes to `.vindex` bypass the gate), and CORPUS/43 F-A3 (a landed write took 31/36 never-edited same-frame prompts while `described_as` JS stayed ≈100). All three stubs inherit one same-frame probe (6 prompts, one frame) as their only bleed instrument; none of these writes is one-frame.

### H-1 — shared z over three prompt frames

(a1) A z fit to three frames is a write that fires on three frames; F-A3 says a one-frame write already bled onto bystander subjects, so the bystander footprint of a three-frame z is a new, unmeasured quantity. (b1) Bystander-subject probe in *each* of the two training frames plus the held-out frames (fictional and real subjects), counted separately, gate ≤ A + 1 per frame. (c1) Stub has one frame only — partial.

(a2) The two training paraphrases now shape ΔW, but a `.larql` triple carries no paraphrases, so Gate check 11 (patch hash) does not cover what was actually written. (b2) Hash the frozen prompt set into the run record and audit entry beside the patch hash; treat it as a Tier-2 sealed artifact (§10.8 pattern), not a harness default. (c2) Stub says "disjoint from the held-out set" — provenance and hash absent.

(a3) Threat 3: a paraphrase is a crafted-text channel into the write; one that embeds a real entity or a frame shared with real capitals steers z toward L1 flips. (b3) Human-authored fixed paraphrases, plus an entity-leakage scan of the set (count of real place names, other subjects) logged before the run. (c3) Absent; origin of the two forms is unspecified.

(a4) ΔW ratio ≤ 1.5 is the only footprint cap; stub has it — a size control, not a bleed control.

### H-18 — minted token by embedding-only tuning

(a1) A vocabulary row is a schema mutation; §10.3 scopes are entity type + relation family + tier, no role is scoped to "add a token," so the Gate has nothing to check and the mint passes as unclassified — invisible, not authorized. Ruling 3 calls the token a Git/`.vindex` artifact, under C16 exactly the write class that bypasses the gate. (b1) Declare what the Gate sees: a `.larql` triple type for mint events, Architect-only with §10.6 human review, row hash in the audit record. (c1) Absent.

(a2) P2 "233/233 tokenizations unchanged" proves the mint does not retokenize existing text; it does not test the alternative tokenization of the value *string* (the coined words as ordinary subwords), which is what a user types and a side channel would use — the ≈39 % bypass figure. (b2) Alternative-tokenization probe: held-out prompts with (i) the subject alt-tokenized, (ii) readout by string on the subword path as well as by minted id; report the gap. (c2) Absent (readout is minted-id top-1 only).

(a3) On a tied model the trained row is also the output row; gradient descent on 20 phrasings can raise the minted id's logit in any context, making an attractor that fires on unrelated prompts — sibling 0 / cannibal 0 / L1 0/12 cover only minted-vs-minted and real capitals. (b3) Minted-id emission rate over generic text at every position (not the value slot), and row-norm ratio against the vocabulary norm distribution; both pre-set. (c3) Partial — slot-local only.

(a4) Gradient training on MPS is not bit-reproducible; the object the Integrity check could hash (the row) differs per run, and "two N seeds" is init variation, not run replication. (b4) Same-seed double train, report row cosine and held-out agreement; hash the training set and the row into the record. (c4) Partial. P4 GGUF chain is present — but the tokenizer file it depends on has no owner or signature in §10.5–10.8.

### H-13 — merged band-LoRA on model-generated QA

(a1) The write-authorized model generates its own training data (Threat 3, self-referential): prior poisoning of the band is restated in the 480 phrasings and trained back in. (b1) Generate from a hash-pinned pristine base checkpoint, freeze and hash the set before training, and run a human-authored-phrasing comparator. (c1) Absent ("generated phrasings").

(a2) One leaked real entity in one phrasing trains a cross-fact edge; 480 items nobody reads is the cheapest poisoning in the program. (b2) Entity-leakage filter with logged counts (real countries/capitals, other subjects, frames shared with L1 prompts) as a pre-train gate. (c2) Absent.

(a3) The closed-form ΔW is a deterministic function of (patch, covariance, hyperparameters); a LoRA delta depends on seed, batch order and MPS kernels, so §10.2 check 11 has no stable object to hash and behavioural-only verification becomes the whole integrity story. (b3) Two same-seed trainings with ΔW cosine and held-out agreement; define the audit artifact as merged-adapter hash plus data hash. (c3) Absent.

(a4) Twenty frames per fact is the largest multi-frame fit of the three, so the one-frame probe is weakest here, and the "generic-capability probe with a pre-set floor" has no number. (b4) Per-frame bystander probe as in H-1(b1); a fixed floor (e.g. the harness perplexity set) written into the prereg. (c4) Partial.

### Alternative-tokenization probe

Carry it on **H-18** (mandatory: the hypothesis *is* a tokenization intervention and the id-only readout cannot see a bypass) and on **H-13** (the only arm whose training could plausibly close the bypass, so the probe discriminates). On H-1 it would not change the label; omit.
