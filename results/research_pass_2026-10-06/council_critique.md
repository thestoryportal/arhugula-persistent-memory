# Framework Council critique of the top three — research pass 2026-10-06

**Critique, not evidence.** Six lenses (memit-specialist, state-consistency-theorist, graph-data-architect, validation-contract-architect, orchestration-comparativist, aisecops-specialist) were each prompted from their own SKILL.md, given `top3.md`, the conventions and the three full entries, and the spec sections their lens owns, and asked to find what fails. The council does not confirm results (DISCIPLINE §3); its output here sharpens the three pre-registration stubs. Each lens's full text follows the synthesis; nothing below changes a disposition in `hypotheses.md`.

## Where the lenses converge (what the stubs must gain before any run)

1. **One process per arm cannot license PARTIAL.** Validation and memit lenses: the ±3–5/72 per-process spread of both arms covers a gain of 10; only LEAD ≥ 30 clears the envelope. Every stub needs a second process (or a declaration that PARTIAL is non-binding at one process) and the per-fact 24-vector with a pre-registered per-edge pass rule, because §8.9 is per edge and 61/72 is an aggregate.
2. **The training phrasings are an unaudited, un-ledgered write input in all three.** Validation, security, consistency and orchestration lenses: whoever or whatever authors the paraphrase forms (H-1), the 20 phrasings per minted row (H-18) or the 480 training items (H-13) knows or can regenerate the sealed held-out templates; the set shapes the overlay but has no slot in the `.larql` patch, no hash in the audit record, no author in the pipeline, and no entity-leakage scan. Each stub must publish the set before the run with a structural-overlap audit against the three sealed templates, generate it from the pristine base checkpoint (not the edited model), hash it as an artifact, and name its author stage.
3. **The locality battery is one-frame; these writes are multi-frame.** Security and graph lenses: CORPUS/43 F-A3 found a one-frame write bleeding onto 31/36 never-edited same-frame prompts while `described_as` stayed near 100. A z fit to three frames (H-1), a row trained on 20 phrasings (H-18) or a delta trained on 480 items (H-13) needs a bystander probe in each training frame, counted separately, plus non-written relation labels on the same subject (`is_a`, `associated_with`) and, for H-18 and H-13, an alternative-tokenization probe of the value string (the 38.6 % bypass figure of 2609.29045).
4. **H-18 and H-13 are not MEMIT writes and their stubs must say what compaction does with them.** Consistency and memit lenses: a gradient-trained vocabulary row is derivable from no `.larql` patch, so a §8.10 full MEMIT re-run drops it unless it is frozen Genesis-tier; sequential band-LoRA deltas compose by addition, the pattern §8.10 D62 rejects. Both stubs claimed "overlay-representable" at one write; each needs a two-overlay test (two 12-fact halves vs one 24-fact write) and, for H-18, a re-run with the row discarded scored as a `COMPACTION_REGRESSION` probe. H-18's "spec-amendment none" does not hold on the memit lens's reading (an embedding-side write is not a §8.1 FFN compile); the entry should carry the §8.4/§8.10 question explicitly.
5. **Each arm's decomposition is missing.** memit lens: report `canon_full`, first-token, `tf_pertok` and P(full | first) beside `para_full` so a gain or a miss is localised; for H-1 add a z-probe readout (does the shared z reach ≈ 0.99 on all three frames) and the key cosine across templates; for H-13 add forced-first-token continuation on unedited subjects (does "Vindex" → "Vask" fire regardless of subject, which would be bigram learning, not a bound fact) and the covariance-weighted norm or null(C) share of the LoRA delta beside the Frobenius ratio.
6. **H-18's readout is a storage probe; the route bar is a behaviour bar.** Validation lens: top-1 minted id at the value slot is L1; the stub must add free greedy generation from each held-out prompt (string equals the value, continuation sane) and record storage and behaviour as separate columns; it also needs a row-norm ceiling, the perplexity gate, a minted-id emission rate over generic text at every position, and a label for 47–55/72.
7. **H-13's forgetting floor is undefined and its transaction does not fit the spec's windows.** Validation, consistency and orchestration lenses: name the forgetting instrument and fix floor = base − δ before the run; the 2–3 h exceeds the 2 h PREPARED timeout and the 60-min Write Lock TTL (§11.5.1, §11.9); a gradient run on MPS is not bit-reproducible, so the Integrity check (§10.2) has no stable object and the LoRA writer has no fingerprint; two same-seed trainings with ΔW cosine and held-out agreement are the minimum.
8. **What N = 24 under one relation label hides (graph lens).** All three stubs would pass on a model whose graph is unqueryable by relation, untraversable backwards (D4), unprunable per edge (§7.8) and unable to hold a second edge on any key (C4). None of this bears on the C10 question the stubs ask, but a pass should be labelled "edge stored", not "graph stored", and the reverse-lookup and two-edge probes are cheap to add.

## Disagreements between lenses

- The memit lens reads H-1 as "the knob the program already ruled out" (the z already reaches 0.99; the wall is realisation), while the validation lens says the stub as written cannot distinguish a frame failure from a realisation failure and asks for a P6 injection cell of the shared z (≈ 40 min) before the write arm. The two readings agree on the control: run the injection cell first; if its ceiling is not above 49/72 the hypothesis has no room.
- The security lens would carry the alternative-tokenization probe on H-18 (mandatory) and H-13 (discriminating) and omit it on H-1; the validation lens's §21.4 judgment tuple (exact substring, case-sensitive, greedy to a fixed budget) applies to all three. No lens objected to the ordering cheapest-first.

## What the critique changes in this pass's files

Nothing in `hypotheses.md` or `top3.md` is edited after the fact; the objections above are the amendment list the program session applies when it writes the pre-registrations. The one labelling correction the lenses agree on is recorded here: H-18's `spec-amendment` should read "§8.1/§8.4/§8.10 — an embedding-side write outside the FFN compile; compaction procedure undefined", not "none".

---

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

## state-consistency-theorist

Lens: the Git↔`.vindex` consistency contract — content-scoped authoritative medium (§11.2 D42), Git-push-then-mount ordering (§11.5, C-TPC3), drift counted in edges from the last anchor (§8.7), compaction as a full MEMIT re-run on archived `.larql` patches with delta composition rejected (§8.10 D62). Each objection names the clause it fails, the measurement that answers it, and whether the top3 stub holds it.

### H-1 — shared value objective across prompt formats

1. **Un-ledgered write input (§8.5, §8.10 D62).** The paraphrase set that shapes z is not one of the four `.larql` sections, so a compaction re-run from the archived patch alone cannot regenerate the overlay; the patch stops being the recipe for the anchor. *Measure:* compile the same patch with and without the paraphrase set; compare behavioural top-1 on the 72 held-out prompts and A1/A2; or hash the set into the patch as a versioned artefact. *In stub:* no.
2. **Snapshot-hash determinism (Ledger `vindex_snapshot_hash`).** If paraphrases are model-generated or authored per run, identical patches yield different overlays and the commit→snapshot mapping becomes a record, not a function. *Measure:* two same-seed compiles with a frozen paraphrase set; behavioural agreement on the 72 prompts. *In stub:* no — LAW#5 inertness shows the seam at default changes nothing, not that the non-default path reproduces.
3. **Drift is edge-counted and ΔW-blind (§8.7, OQ-W1).** A multi-frame z moves per-edge weight mass while `edge_count_since_anchor` stays 24, so the 1,500/8,000 thresholds no longer bound the same quantity. *Measure:* ΔW ratio vs the canonical write. *In stub:* yes (≤ 1.5), single write only; nothing covers accumulation.

### H-18 — minted token written by embedding-only tuning

1. **Dual residence, no classification (§11.2 D42, §11.5).** Registration (tokenizer file, P2) lives in Git; the trained row lives in weights; a vocabulary row is neither `structural_entity` nor `layer4_domain`, so C-TC2 gives the TC no compensation direction, and Git-push-first makes reachable the Git-ahead state where the tokenizer emits an id with no trained row behind it. *Measure:* mount the registered tokenizer with the row at init and read the value slot on all 72 prompts and A1 (orphan-id control); check whether the TC's Git revert covers the tokenizer artefact. *In stub:* no.
2. **Compaction cannot regenerate the row (§8.10 D62, §E.2).** Compaction is a MEMIT re-run on patches; a gradient-trained d-vector is derivable from no patch, so it survives only as a frozen Genesis-tier artefact (§8.4, never compacted) or is lost at the next anchor. *Measure:* re-run the 24-fact patch set through the MEMIT path with the trained row discarded; score the minted readout as a `COMPACTION_REGRESSION` probe (CORE pass = 1.0). *In stub:* no — P4 shows the id tokenises 24/24 in both GGUFs, which is tokenizer survival, not row survival through a re-run.
3. **Tied embedding = two sites per overlay.** The trained row is both input embedding and unembedding row, so one write touches two logical matrices, and the zero-forgetting claim is about every old-token transition, not the probed ones. *Measure:* perplexity rise on the neutral set, full-vocab logit-drift norm, row-norm ratio as the ΔW-equivalent. *In stub:* partial — sibling 0, cannibal 0, L1, L3, `described_as` present; perplexity and any size qualifier absent from H-18 though present in H-1 and H-13.

### H-13 — merged band-LoRA write

1. **Rejected composition pattern (§8.10 D62).** Incremental LoRA deltas on one band compose by addition — the delta composition the spec rejects for skipping the covariance safeguards; the stub tests one joint write, never the sequential case the overlay model lives in. *Measure:* two sequential writes (12 + 12, the second trained on the merged model) vs one joint write of 24; held-out, A1/A2 and locality on both. *In stub:* no.
2. **Re-run is re-training, fed from the write target.** Compaction becomes stochastic re-training, and phrasings "generated by the model itself" taken from the edited model make the write's input depend on the current overlay — a read-your-writes leak into the write path under a strong-consistency model (§11.3). *Measure:* generate phrasings from the anchor model only, hash them into the patch, retrain twice fixed-seed, compare behavioural agreement on 72. *In stub:* no.
3. **Merge is not mount (§8.4, §11.5 Phase 2).** The entry calls the delta overlay-representable; the stub merges it into weights, so rollback-by-unmount needs a separable delta whose applied readout equals the merged readout. *Measure:* string and id readout equality between merged and apply-at-mount forms on 72 + A1/A2. *In stub:* no — only string = id is pre-registered.
4. **Transaction window (§11.5.1, §11.9).** The stated 2–3 h exceeds the 2 h `incremental_prepared_timeout` and the 60-min Write Lock TTL, so the write cannot complete inside one PREPARED window as specced; and §8.7 drift has no counter for a rank-bounded footprint, the forgetting axis the source measured. *Measure:* time the train phase alone against 2 h; generic-capability probe with a stated floor. *In stub:* probe yes (floor unspecified); timing no.

### Sharpest

- H-18.2: a gradient-trained row is derivable from no `.larql` patch, so compaction as a MEMIT re-run drops it unless it is frozen Genesis-tier.
- H-13.1: sequential band-LoRA deltas compose by addition, the pattern §8.10 D62 rejects; the stub never tests composition.
- H-1.1: the paraphrase set is an un-ledgered write input, so the archived patch alone can no longer regenerate the anchor.

## graph-data-architect

Schema-layer reading of `top3.md` against spec §7 and CORPUS/45. Shared defect: every arm writes one relation label over 24 degree-1 subjects, with no `is_a` edge (C4), no second relation on any key, and no value→subject probe (D4). Each stub scores 24 disjoint (key, value) pairs; none distinguishes "edge stored" from "graph stored".

### H-1 — shared value objective across prompt formats

1. **Address invariance is untested.** An edge is addressed by (entity, relation) under the closed vocabulary (§7.3, C5); H-1 varies the relation's *surface* in the value objective but leaves the stored key canonical, so a pass shows the value is frame-invariant, not the address. *Measure:* hold out a key-side frame class (relation before subject, subject not last before the slot) and report it as its own /24. *Stub:* no — the three sealed templates are not partitioned by key position.
2. **Cross-relation basin widening on one key.** Fitting one z to more frames widens the context region of the subject key that maps to the value, so paraphrases of a *different* Knowledge-family relation on the same subject (`associated_with`, `derived_from`) may now return the coined value. *Measure:* per subject, probe two non-written relation labels pre/post; count flips to the coined value. *Stub:* partially — `described_as ≥ A − 3` watches one adjacent relation; Taxonomy (`is_a`) and Constraint (`requires`) are unprobed.
3. **D4 reverse lookup absent.** A shared forward z says nothing about value→subject. *Measure:* 24 reverse prompts, top-1 subject. *Stub:* no.
4. **Two edges on one key never coexist.** A C4-compliant record is `is_a` plus the knowledge edge on the same subject key; H-1 only ever stores one z per key. *Measure:* write both edges per subject (48 edges, 24 keys), score both /24 and /72. *Stub:* no.

### H-18 — minted token by embedding-only tuning

1. **The row is syntax, not semantics (§7.1, D1).** The decoded id renders the literal string (CORPUS/45), so the "value node" is a typeless leaf (C4): no `is_a`, no out-edges; the graph cannot grow through it. *Measure:* after tuning, write one edge with the minted token as *subject* (`minted is_a <subtype>`) and score it. *Stub:* no — P2/P3 check tokenisation and `compute_z` reachability, not entity-ness.
2. **Objective asymmetry breaks D4 on a tied embedding.** Embedding-only tuning fits the row to be *predicted* at the output; reverse lookup needs the same vector to be *read* at the input as a key. One tied row serves both; a gradient that improves output recall can degrade input keying, and forward-only readout never sees it. *Measure:* value→subject top-1 per minted token pre/post, and the CORPUS/45 in-context 24/24 check repeated post-tuning. *Stub:* no.
3. **Sibling collapse from shared training contexts.** All 24 rows are tuned on ≈20 phrasings from one template generator; the shared signal is the template, so rows drift toward a common direction. `sibling 0` on near-orthogonal random inits (rank 23.7) is measured on the trivially separable set and proves nothing here. *Measure:* pairwise cosine and effective rank of the 24-row block pre/post (the step-0 rank instrument exists), plus registered-but-untrained distractor ids. *Stub:* `sibling 0` and `cannibal 0` only — no rank/cosine check, no untrained-distractor set.
4. **Namespace and capacity are unrepresentable.** The tokenizer is one flat global namespace; §7.4 requires `domain` and `project_id` with different pruning and authorisation, and 271 spare rows cap the graph at 271 coined values before a resize that voids P2 inertness and the GGUF chain. A row cannot carry `scoped_to`. *Measure:* coin one string under two subjects in two namespaces; check whether reverse lookup returns both; delete one fact and show the row freed and re-mintable. *Stub:* no — CORPUS/45 lists lifecycle (C5/C9) and capacity as queued, outside this test.

### H-13 — merged band-LoRA write

1. **The write has no edge addressing.** A rank-16 delta is one dense update for all 24 facts; it is not partitionable into (entity, relation, target) edges, so §7.8 deletion authority by relation family (D8, D54) has no object. Invisible at N = 24 because all 24 facts are one family. *Measure:* retract one fact (retrain on 23, or ablate) and report the other 23 unchanged; mix two relation families in the 24 so the family partition is exercised. *Stub:* no retraction or deletion test at all.
2. **Cardinality is a hyperparameter the schema never sees.** ΔW = BA with rank 16 < 24 cannot hold 24 independent output directions; facts are entangled by construction, and "sweep rank only if PARTIAL" conflates capacity with fit. *Measure:* cross-subject confusion on held-out misses (which sibling's value was emitted), and rank held fixed while N goes 24 → 48. *Stub:* no sibling or cannibal gate for H-13 (H-18 has one).
3. **Overlay composition (§8.4/§8.10, which H-13 itself marks as amended) is asserted, not tested.** "Additive and overlay-representable" at one delta is tautological; two namespaces are two deltas on the same band. *Measure:* two deltas on disjoint 12-fact halves, both merged, versus one 24-fact delta. *Stub:* no.
4. **The value-token loss is a string objective (§7.1).** It rewards reproducing the literal continuation; the generic-capability probe measures forgetting, not whether the coined value became a semantic node. *Measure:* `describes` / `is_a` probes with the coined value as subject, as in H-18(1). *Stub:* no.

### What N = 24 hides

All three stubs would pass on a model whose "graph" is unqueryable by relation, untraversable backwards, unprunable per edge, and unable to hold a second edge on any key.

## validation-contract-architect

Scope: the three stubs in `top3.md` read as validation contracts against §8.9 (L1 storage / L2 behaviour, never collapsed), §9.2 (critic not authored by the actor), §21.4 (probe tuple frozen at commit) and the CORPUS/44 envelope ([5, 18]/72 identical-arm, ±3–5/72 per process, one seed, context templates drawn unseeded per process). Per item: objection → answering control → in the stub?

### Cross-cutting

1. **PARTIAL is unresolvable at n = 1.** Both arms carry ±3–5/72 per process, so a same-run gain of 10 sits inside the combined spread; only LEAD ≥ 30 clears the envelope with margin. → Two processes per arm before any PARTIAL/TRADEOFF label, or declare PARTIAL non-binding at one process. → Absent in all three.
2. **The route bar is an aggregate; §8.9 is per edge.** 61/72 yields no `write_outcome` per fact; 20 × 3 + 1 and 24 × 2.5 are different states. → Pre-register the per-fact rule (behaviour-pass iff 3/3 held-out templates) and report the 24-vector. → Absent in all three.
3. **Judgment method unstated.** None declares the §21.4 tuple or the stop rule for the continuation. → `exact_substring`, case-sensitive, full coined value, greedy to a fixed token budget. → H-13 states string = id readout; H-1 and H-18 do not.

### H-1 — shared value objective across prompt formats

- **The premise collides with F-A3 and a NULL is uninterpretable.** The canonical z already carries 49/72 under injection while the edit realises 13/72; a NULL on arm B cannot say whether the shared z failed to carry or the edit failed to realise it, so "Fail changes: the frame account is closed" is not licensed. → A P6 injection cell for the shared z (≈ 40 min): a ceiling not above 49/72 means the hypothesis has no room; above it, a NULL edit is a realisation fail. → Absent.
- **"Disjoint from the held-out set" is a string condition, not a seal.** The author of the two training forms knows the three held-out templates; a one-word variant is "disjoint". → Publish the training forms before the run with a stated frame-class difference (statement / question / cloze) and a normalised-overlap audit. → Absent; training-form authorship is not stated.
- **LAW#5 inertness at the default says nothing about the knob when on.** Arm B's variance under the unseeded context draw is unmeasured. → Covered by item 1. → Absent.
- The same-frame gate is the right detector for z encoding the frame rather than the subject. → Present.

### H-18 — minted token by embedding-only tuning

- **Top-1 minted id at the value slot is a storage probe, not an L2 probe.** It is argmax at one teacher-forced position; it does not show that free generation emits the token and continues sanely, and on a tied model the trained row also changes what follows it. The stub reports the L1 half and labels it with a route bar defined on five-token free generation. → Free greedy generation per held-out prompt: detokenised string equals the value and the continuation is normal; record top-1 and generation as separate columns. → Absent (P4 shows the id tokenises, not that it is generated).
- **No bound on the row.** A large-norm output row wins argmax by magnitude and, tied, shifts the softmax normaliser everywhere; sibling 0 / cannibal 0 only cover the value slot. → Row-norm ceiling (ratio to the median vocabulary row) plus the perplexity-rise ≤ 0.5 and same-frame gates from the conventions. → Both gates absent; sibling/cannibal present.
- **Training phrasings are generated by the evaluated model and never audited against the sealed templates.** → Exact + normalised + n-gram overlap audit with a pre-registered exclusion rule and reported count; hash the phrasings; pin the generation and GD seeds (the two N seeds are init seeds). → Absent.
- **Label gap.** Pass ≥ 56, NULL in [34, 46]; 47–55 is unlabelled. → Close the interval. → Absent.

### H-13 — merged band-LoRA write

- **The forgetting floor is undefined, so the arm cannot fail on the axis the source failed on.** Instrument unchosen (MMLU subset or perplexity set), floor unset: the first run is unmeasurable on forgetting, and perplexity ≤ 0.5 is a weak proxy for 57.0 → 40.2. → Name the instrument, fix items and seed, measure base and arm A before training, floor = base − δ pre-registered. → Absent.
- **Storage-pass / behaviour-fail is invisible.** Training-phrasing EM is a storage probe used only as a stopping rule. → Report per-fact train-EM beside held-out /72. → Absent.
- **ΔW ratio measures the wrong quantity for a different writer.** The closed-form ΔW lies in null(C) (share 1.000); an equal-Frobenius LoRA delta is unconstrained and can load the data directions the covariance protects. → Report tr(ΔW C ΔWᵀ) or null(C) share alongside Frobenius. → Absent.
- **Same training-data leak as H-18, plus a forking rank sweep.** Phrasings unaudited; r ∈ {8, 32} tried if 16 is PARTIAL with no rule for labelling a later rank's pass. → Overlap audit and pinned seeds as above; a post-hoc rank is a new pre-registration or recorded as exploratory. → Audit absent; conditional sweep present, labelling rule absent.

## orchestration-comparativist

Lens: how each top hypothesis sits inside the write path of spec §12 / §8.3–§8.4 and e2e §C–§D. Fixed facts held against all three: the atomic unit is `{module_code, test_suite, .larql_patch, declared_dependencies}` (§C.1); the Coder drafts the patch, the TGA authors tests, no reasoning agent holds both mediums (§C.2); Patch Authorization Gate → Commit Executor → MEMIT → Git is deterministic, non-reasoning code (§12.2); the Commit Executor is the sole writer behind a FIFO at concurrency 1 (C-OR6); 2PC commits Git first, `.vindex` second, with an overlay hash in `COMMITTED` (§C.6); overlays accumulate as `incremental_NNNN.vindex`, tiered for independent rollback (§8.4); idle-window fires on no `PREPARED` for 30 min (§12.8). All three stubs are Genesis-shaped (one batch, N = 24); none tests the Incremental shape, where each hypothesis has to live.

### H-1 — shared z over canonical + two paraphrase forms

**Objections.**
1. The paraphrase forms are now write inputs, and the atomic unit has no slot for them: either the `.larql` grammar grows a per-fact paraphrase field the Coder authors (a reasoning agent shaping the parametric target), or the Commit Executor generates them, which breaks the §12.2 non-reasoning rule.
2. In production the held-out probe is the §8.9 L2 behavioural check drawn by the Validator from the same template family the Coder sees; the stub's "disjoint from the sealed templates" is an experimenter guarantee that the pipeline does not reproduce.
3. The per-patch compile cost rises with the prompt set inside `compute_z`; the stub's 35 min is a harness-pass number, not a per-overlay latency, and every `incremental_NNNN` pays it while holding the session lock at concurrency 1.
4. The paraphrase set is a new persistent artifact with no governance tier: if it is not committed to Git, compaction (§8.10) cannot rebuild the overlay it produced.

**Measurement or control.** (1) Name the field in the patch and the author of it; (2) log per-fact lexical overlap between training forms and held-out templates, generator blind to the probe set; (3) log `compute_z` wall time per fact, arm A vs B; (4) assign the tier and store the set with the overlay hash.

**In the stub?** (1) No. (2) Asserted, not measured. (3) No. (4) No.

### H-18 — minted row trained by embedding-only tuning

**Objections.**
1. A minted token changes the tokenizer for every runtime that touches text: Coder, TGA, Validator probes, the GGUF serving path; a Validator on the unextended tokenizer renders the id as bytes and its `code_pass_patch_fail` verdicts are void.
2. On this tied model the trained row is also the output row, so the overlay is an embedding/head delta, not a band ΔW; §8.4 independent rollback presumes the mount/unmount is a clean inverse, and that is untested.
3. Vocabulary becomes a function of the mount set: unmounting `incremental_0003` removes a token that `incremental_0004`'s text may tokenise through, so later overlays' probes change under earlier rollbacks.
4. The "few hundred steps on MPS" run inside the Commit Executor is not bit-reproducible (CLAUDE.md gate 2: cross-process weight reproduction does not hold on GPU), so a Git-ahead recovery cannot regenerate the `COMMITTED` overlay hash.

**Measurement or control.** (1) Tokenise the full probe set under every runtime's tokenizer and diff; (2) apply, unmount, assert bit-identical embedding matrix and 0/72 step-0 recall restored; (3) tokenisation stability of all mounted overlays after removing one; (4) two runs, same init seed, compare overlay hash and top-1 behaviour.

**In the stub?** (1) P2 233/233 and P4 24/24 cover one process and the GGUF chain, not an agent fleet: partial. (2) No. (3) No; P2 checks only the forward direction. (4) The two N seeds are init seeds, not re-run determinism: no.

### H-13 — merged band-LoRA write

**Objections.**
1. A gradient loop replaces the closed-form solve inside Phase 1; a 2–3 h stub (training included) means a `PREPARED` entry or session lock outlives the 30 min idle-window heuristic (§12.8) and serialises every write behind it at concurrency 1.
2. The write path must be deterministic (§12.2); a LoRA writer with early stop on training-phrasing EM has a data-dependent step count and MPS non-determinism, and it has no fingerprint at all — the stub's fingerprint is on the engine it does not use.
3. Sequential incremental overlays are each trained against a base that includes the earlier ones; unmounting `incremental_0003` while keeping `0004` yields weights `0004` was never trained on, so §8.4 independent rollback fails by construction unless deltas are stored unmerged.
4. The ~20 generated phrasings per fact are model output feeding the writer: same authorship fault as H-1 (1), and the generic-capability floor the Validator would need per patch (source: 57 → 40 with rank) is named but has no number.

**Measurement or control.** (1) Training wall time at N = 24 and at N = 1–5 per incremental patch, reported as lock hold time; (2) two same-seed runs, overlay hash + behavioural diff, plus a SHA on the LoRA writer; (3) train two sequential overlays, unmount the first, re-probe the second; (4) pre-set the capability floor as a number and name the phrasing author.

**In the stub?** (1) Aggregate hours only: no. (2) No. (3) No, Genesis shape only. (4) Floor named, not numbered; author unnamed.

### Common fault

All three stubs measure recall after one batch write on one process. None measures the two things the §C pipeline is built around: a reproducible overlay hash under 2PC, and independent unmount of one overlay among several. Until those two are in each stub, a pass tells F1 the write works once, not that it is a write the Commit Executor can own.

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
