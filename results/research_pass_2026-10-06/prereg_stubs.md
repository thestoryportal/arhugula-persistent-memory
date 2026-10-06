# Pre-registration stubs for the agreed sequence — research pass 2026-10-06

Stubs, not program-format pre-registrations. Each gives the program session what it needs to author the document: hypothesis, binding count, arms, controls, gates, labels, decision consequences, the harness seam to confirm, and the council amendments that apply. Harness seam names come from CORPUS/44–50 and must be confirmed by `cat -n` of the source before authoring (law 4); the lead agent did not read the harness code.

## Shared contract (applies to every stub; the council's cross-cutting amendments are folded in)

- **Binding count:** A7 `para_full` on the three sealed held-out templates, 24 subjects × 3 = 72, greedy, fixed token budget, exact substring of the coined value, case-sensitive; string readout and id readout both reported and equal (CORPUS/44 P4 `para_full_string`). Report the per-fact 24-vector and a per-edge rule: behaviour-pass iff 3/3 held-out templates.
- **Decomposition reported beside the binding count:** `canon_full` /24, first-token /72, `tf_pertok_cont`, P(full | first).
- **Controls:** A1 single-token and A2 prior-coherent two-token values in every pass; same-run baseline arm (engine defaults) in every pass.
- **Gates:** engine fingerprint `d941a9fb…` (tools/engine_fingerprint.py) and `_cov_cpu == 3`; LAW#5 inertness of any new seam at its default (|Δexpr| ≈ 0); A1, A2 ≥ 68/72; L1 real-country flips ≤ baseline + 1 (of 12); `described_as` JS ≥ baseline − 3; L3 unedited-capital top-1 ≥ 29/30; same-frame fictional probe ≤ baseline + 1 (of 6) **in every frame the arm was fit to, counted separately**; generic perplexity rise ≤ 0.5; ΔW ratio ≤ 1.5× the single edit; plus the probes of non-written relation labels on the same subject (`is_a`, `associated_with`) pre and post, flips counted.
- **Labels:** LEAD ≥ 30/72; PARTIAL gain ≥ 10/72 over the same-run baseline with all gates; TRADEOFF = gain ≥ 10 with a gate miss; NULL otherwise. Identical-baseline envelope A7 [5, 18]/72, canon [5, 10]/24. **PARTIAL is non-binding at one process**; any PARTIAL or LEAD is replicated in a second process before it carries a label (gate A in the sequence). Route pass ≥ 61/72.
- **Write inputs that are not the triple** (phrasing frames, key-position rules, covariance statistics): fixed before the run, published in the pre-registration, hashed into the run manifest, generated or authored without sight of the three held-out templates, with a normalised-overlap audit against them reported.
- **Advisor pass before the run; cross-family reviewer (GPT-6-Astra, high) at the promote gate.** One speculative fix then HALT on any science-path bug.

---

## Step 1 — H-1 Shared value objective across prompt frames

- **Hypothesis.** One `compute_z` target per fact, optimised jointly over the canonical prompt and two fixed training frames, transfers to held-out phrasings better than the canonical-only target, at 24 requests and 24 keys.
- **Pre-step (required by the validation lens, ≈ 40 min):** P6 injection cell with the shared z on the unedited model (the CORPUS/44 injection hook). If its held-out ceiling is not above the canonical z's 49–54/72 stratum, the arm has no room and the pre-registration records that as the stopping outcome.
- **Arms.** A canonical z (same run); B shared z over {canonical, frame F1, frame F2}, where F1 and F2 are statement-form and cloze-form templates written per relation (not per fact), published in the document, structurally distinct from the three held-out question templates, overlap-audited.
- **Seam.** `compute_z` prompt set (science path; LAW#5 isolation against the K1 ceiling of CORPUS/43 first). Confirm in `memit_dry_run/memit/compute_z.py` and the harness call site.
- **Extra readouts.** z-probe: target probability of the shared z on each of the three frames (must reach ≈ 0.98 on all three, else B is a degraded-z arm); subject-key cosine canonical vs each held-out template, pre and post.
- **Decision.** LEAD → replicate (gate A), then adopt the shared z as the default target for later arms. NULL with the P6 ceiling above 54 → realisation account only (steps 6–7). NULL with the P6 ceiling ≤ 54 → frame account closed on this harness.
- **Cost.** One pass ≈ 35 min + the injection cell ≈ 40 min.

## Step 2 — H-10 / H-5 Second key inside the value under subject keying

- **Hypothesis.** A second key per fact at a value-internal position (the token before the maximum-surprisal boundary, H-10; or the maximum covariance-leverage position kᵀΣ⁻¹k, H-5) gives the continuation a direct write without the collinearity of frame tokens.
- **Step 0 (minutes, no write).** Surprisal profile and leverage score of every A7 value-token position under the base model and the band covariance; if the two rules pick the same position on ≥ 20/24 facts, the arms merge; if either picks the subject or a frame token for most facts, that rule is dropped. Publish the chosen positions.
- **Arms.** A single subject key (same run); B subject key + value-internal key (48 keys), targets as the engine computes them per key.
- **Seam.** The harness request builder (key positions per request); the engine's `compute_ks` / `repr_tools` key extraction. Confirm.
- **Extra gates.** Same-frame probe mandatory and per frame; keygram of the 48 keys (pairwise cosine, effective rank) reported, since value-internal keys are the frame-bleed risk CORPUS/43 measured.
- **Decision.** LEAD → gate A, then step 3 continues in parallel. NULL → a second closed-form key alone cannot carry the continuation; steps 6–7 stay the engine route.
- **Cost.** Step 0 minutes; one pass ≈ 35 min.

## Step 3 — H-19 Two minted tokens per value

- **Hypothesis.** Writing the coined value as two minted tokens (one per word) lands between the one-token mint (34–46/72) and the full string (11–15/72); the per-position curve says whether length or pair novelty is the wall.
- **Arms.** A7-multi (string), A7-mint-1 (one token, init N, two seeds), A7-mint-2 (two tokens, init N, two seeds); A1 in every run.
- **Seam.** Mint harness (`c10l_mint_lib.py`, `ARM_HOOKS`), 48 spare rows of the 271; step 0 admission P2 (233/233 tokenisations unchanged), P3 (`compute_z` reaches ≥ 0.98 on every minted row), I-11 dead/cannibal/live check; pairwise cosine and effective rank of the minted block pre and post (graph lens).
- **Readout.** Binding as CORPUS/45 (post-write top-1 minted id at each value slot minus step-0 recall) **and** free greedy generation from each held-out prompt decoded to the string (validation lens: storage and behaviour as separate columns); per-position curve; P4 GGUF chain (both ids tokenise 24/24 in fp16 and Q4_K_M GGUFs).
- **Decision.** Monotone 1 > 2 > string (differences ≥ 10) → span account; the token route is the lead and the closed-form H-18 variant enters. 2 ≈ string → pair-novelty account; token tricks close.
- **Cost.** One mint pass ≈ 40 min per seed.

## Step 4 — H-8 Per-fact layer choice

- **Hypothesis.** Choosing the edited layer per fact by a deterministic dependence criterion between band-layer key and target (LOKI uses HSIC) realises coined-value writes that a fixed band does not.
- **Step 0 (minutes, no write).** Criterion per fact per band layer for A7 and A1; if the maximiser is the same layer for ≥ 20/24 facts, the arm is not run and the result is logged as "no per-fact variation".
- **Arms.** A fixed band 4–8 (same run); B per-fact single layer (one hparam file per fact or a harness map); C per-fact layer plus its neighbour (two layers) if B is PARTIAL.
- **Seam.** Harness hparams `layers` per request. Confirm how the engine batches requests with different layer sets (it may require one solve per layer group).
- **Decision.** LEAD → gate A. NULL → the depth question is closed on this harness (joins CORPUS/37–39, 44).
- **Cost.** Step 0 minutes; one pass ≈ 35–60 min depending on batching.

## Gate A — replication

Any arm from steps 1–4 at ≥ 30/72 is re-run in a fresh process with identical configuration before it carries LEAD or PARTIAL; report both counts and the per-fact agreement. Baseline arms must sit inside [5, 18]/72 in both processes.

## Step 5 — H-13 Oracle measurement (not a route)

- **Hypothesis under test.** If a merged low-rank delta on `down_proj` L4–8, trained with a token-level loss on every value token across many phrasings, cannot reach ≥ 61/72 on these 24 facts with A1/A2 and the locality battery clean, then no write engine on this model can, and the question is the model; if it can, the wall is a missing objective the solver can be given.
- **Labelling.** "Oracle measurement — write-engine replacement; not a route" in title, verdict and register row. A pass does not change C10's status.
- **Arms.** A closed-form baseline (same run); B LoRA r = 16 on the five `down_proj` matrices, merged; r ∈ {8, 32} only as a pre-declared exploratory extension, labelled so.
- **Training data.** 24 × ≈ 20 phrasings generated by the **pristine base checkpoint** (not the edited model), filtered for real-entity leakage (counts logged), overlap-audited against the held-out templates, hashed into the manifest; generation seed and training seed pinned; two same-seed trainings with ΔW cosine and held-out agreement reported.
- **Extra gates.** Forgetting instrument named now: the harness generic-perplexity set plus a fixed 200-item MMLU subset; floor = base − 2 points; covariance-weighted norm tr(ΔW C ΔWᵀ) and null(C) share reported beside the Frobenius ratio; forced-first-token continuation on unedited subjects (bigram-learning control: does the second word fire regardless of subject); per-fact training-EM reported as the storage column.
- **Decision.** Pass → spend the engine days (steps 6–7). Fail → model axis (operator decision on the ceiling rule).
- **Cost.** 2–3 h, no harness build beyond a LoRA writer; the engine fingerprint is on a path this arm does not use, so the LoRA writer carries its own data and adapter hashes.

## Step 6 — H-11 Forward replay (I-2) and OverTone (I-1)

Already pre-registration-selected in the arc (§8) and CORPUS/50. The stubs there stand; the shared contract above adds the per-frame bystander probe, the decomposition readout and the two-process rule. Engine path: LAW#5 isolation; the stats-file SHA joins the manifest where a covariance is touched. Cost ≈ one day of engine work each plus one pass.

## Step 7 — H-3 Direct ΔW optimisation under the projector

- **Hypothesis.** Optimising the band's ΔW directly against the target, with the AlphaEdit null-space projector applied as a constraint, realises the target at the keyed position (today ≈ 3 %, CORPUS/44) and carries the continuation.
- **Arms.** A closed-form baseline; B direct ΔW (fp32 deltas on the five `down_proj` matrices, ΔW·P constraint, same locality battery); sham arm: the same optimiser aimed at the baseline's own z (must reproduce A within the envelope).
- **Reproducibility.** Two same-seed runs; ΔW cosine ≥ 0.99 and held-out agreement reported, since an iterative solve on MPS is not bit-reproducible and the overlay hash must be shown to be stable enough for the ledger.
- **Extra gates.** Realised fraction at the keyed position (step-0 ρ_c of CORPUS/44) reported for A and B; write-size qualifier.
- **Decision.** LEAD → gate A, then the question of whether the optimiser can replace the closed form in the engine (spec §8.2 wording unchanged: still an overlay on `down_proj`). NULL → the layers cannot hold the value; model axis.
- **Cost.** ≈ one day of code; a pass 1–2 h.

## Step 8 — H-4 Covariance from model-generated text (background)

- **Hypothesis.** A preservation statistic drawn from the model's own generations protects different key directions than the Wikipedia statistic and raises coined-value transfer.
- **Procedure.** Generate ≈ 2 h of text with a pinned seed; recompute the five band covariances; rebuild the projector; stats-file SHA in the manifest (ARC §7 item 4); LAW#3 reproduction of A1/A2 under the standard statistic first, then A1/A2/A7 under the new one.
- **Decision.** LEAD → gate A. NULL → the statistic is not the knob for C10; it remains a C1 lever.
- **Cost.** Covariance time unmeasured on the M3 Pro (70 min per band on the lost 4090); run unattended.

---

## Later items (not stubbed; sequenced after the gates above)

H-24 one-time MTP head as a continuation loss; H-9 subject anchors with a temporary carrier; H-6 position-separated write with a runtime gate; the closed-form variant of H-18. Model changes H-21, H-23, H-26 after the ceiling rule, each beginning with a smoke solve (load, one band covariance, one `_cov_cpu` solve, wall-clock and peak memory recorded) and LAW#3 reproduction of a known result on that model.
