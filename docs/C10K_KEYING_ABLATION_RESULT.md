# Keying-locus ablation in the program's MEMIT engine — result (D-C10k-keying-ablation)

_Result 2026-10-04. Pre-registered `docs/C10K_KEYING_ABLATION_PREREG.md` (v3 §3 for the N = 24 cells; §6 and §6b amendments, three advisor rounds). Records `results/c10k_keying_ablation/K{1..4}.json`, `zprobe.json`, `keygram.json`, `n1/N1_*.json`, `n1/framebleed.json`; logs `logs/c10k_keying_ablation_*.log`; harness `experiments/track_c/c10e_bandknob.py` (knobs `C10_KEY_LOCUS`, `C10_CTX_TEMPLATES`, `C10_ARMS`, `C10_RECIPES`, `N_EDIT`, `C10_SUBJECT_OFFSET`; engine unmodified, LAW#5 INERT in every cell). Chains `tools/c10k_keying_ablation_chain.sh`, `tools/c10k_keying_ablation_n1.sh`; probe `experiments/track_c/c10k_keying_ablation_n1_framebleed.py`._

## 1. Reading: **KEYING LOCUS DECIDES WHAT IS WRITTEN — last-token-keyed singles land but do not transfer to paraphrases (0/18 vs 18/18 subject-keyed) and bleed onto same-frame prompts to a varying degree (F3 SUFFICIENT, MEMIT, N = 1; frame-bleed BETWEEN)**

- **N = 24 cells (prereg §3):** INVALID-LAST-TOKEN-CELLS (K3/K4 canon < 90; no keying reading at N = 24). Gate: K1 A1 95.8 / A2 97.2 vs R0 94.4 / 98.6 → **PASS**. Validity prints confirm the keyed token (subject's last token in K1/K2; the final `" of"` in K3/K4) and byte-identical paraphrase and locality strings across cells.
- **Why the last-token cells failed (§3b–§3c):** the z-objective reaches the target, so the loss is at the solve; the 24 last-token keys are highly collinear in raw space (mean pairwise cosine ≥ 0.985, effective rank 1.02; a cosine of 0.985 is a ≈ 10° angle, not rounding), and their small differences sit in low-variance directions the ridge suppresses at w = 5000, so one solve cannot map them to 24 targets. **Claim A: SINGLES LAND (pre-registered label: interference first).** 6/6 single last-token writes land at w = 5000, so the ridge weight does not block a single last-token write. What blocks 24 of them is their collinearity under the covariance-plus-ridge geometry the solve works in; 'interference' and 'ridge' are not separable causes here (the keygram's w* ≈ 100–600 and Route A's 24/24 fit at a 1000× smaller ridge both say a smaller ridge would separate them). The small-ridge sweep is not run because it cannot bear on F1: a last-token write that lands does not transfer anyway (claim B). Zero-edit check not run: a keygram on covariance-whitened keys (C^-1/2·k) would test the collinearity framing directly.
- **N = 1 cells (prereg §6b, the valid last-token cells; criterion fixed after 3 of 12 runs were visible): claim B = F3 SUFFICIENT (MEMIT, N = 1).** 6/6 last-token singles land with ≤ 1/3 paraphrases while 6/6 subject-keyed singles land with ≥ 2/3; described-as JS gap +5.4 points. Paraphrase hits: last-token singles 0/18, subject-keyed singles 18/18 (same value `Beirut` in all twelve chain runs; the distinct-value control is in §3c). Locality cost of subject keying: described-as JS 89–98 against 100 for the last-token singles (≈ 5 points), the price of a write that actually changes the subject's representation.
- **Frame-bleed probe (§6b): BETWEEN (partly frame-keyed).**

## 2. Results, N = 24 (EVIDENCE-SHOWS)

| cell | key locus | templates | ridge weight | A1 canon | A1 para_full | A1 para_any | A1 described-as JS | A2 canon | A2 para_full | A2 described-as JS | A1 rel. Δ‖W‖ L4…L8 | validity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | subject | on | 5000 | 100.0 | **95.8** | 100.0 | 90.06 | 100.0 | **97.2** | 92.48 | 0.19 / 0.11 / 0.09 / 0.16 / 0.23 | valid |
| K2 | subject | off | 5000 | 100.0 | **91.7** | 100.0 | 91.78 | 100.0 | **88.9** | 91.97 | 0.19 / 0.11 / 0.09 / 0.16 / 0.23 | valid |
| K3 | last | on | 5000 | 29.2 | **0.0** | 0.0 | 99.82 | 4.2 | **0.0** | 99.9 | 0.10 / 0.08 / 0.10 / 0.25 / 0.42 | INVALID (canon < 90) |
| K4 | last | off | 5000 | 25.0 | **0.0** | 0.0 | 99.81 | 8.3 | **0.0** | 99.84 | 0.11 / 0.09 / 0.13 / 0.29 / 0.48 | INVALID (canon < 90) |

`para_any` = fraction of the 24 subjects with at least one paraphrase correct. Δ‖W‖ is the engine's own per-layer relative update norm for the A1 edit. Counts behind the K3/K4 percentages: A1 canon 7/24 and 6/24; A2 canon 1/24 and 2/24.

## 3. What the N = 24 table says (first-pass reading; the mechanism is settled in §3b–§3c)

- **Keyed at the prompt's final token, a batch of 24 writes does not land (EVIDENCE-SHOWS).** Same engine, covariance, ridge weight (5000), band, z-objective and dtype as K1; K3/K4 fit the trained prompt on 29.2 / 25.0 % of A1 items (K1 100.0 %) and 4.2 / 8.3 % of A2. The described-as JS stays at 99.8 because little readable change was written, not as independent evidence of locality. By the precedence order both last-token cells are INVALID; no keying rule is written from them.
- **Templates (K2).** Subject-keyed writes without context templates still generalise (A1 91.7, A2 88.9; canon 100 / 100), so templates are not necessary for ≥ 80 % paraphrase scores with subject keying at N = 24; they account for about 4–8 points. Full-precision Δ‖W‖ differ between K1 and K2 at every layer (e.g. L4 15.874 vs 15.889), so the knob changed the key computation.
- **The first-pass attribution to the covariance ridge alone (Route A's ridge diagnostic: last-token keys 17–180× under the ridge at w = 15000; 5.7–60× at w = 5000) is refined by §3c:** the ridge is not what blocks a single last-token write (6/6 land at w = 5000); what blocks 24 is their collinearity in the covariance-plus-ridge geometry. The pre-registered small-ridge sweep (§6) is not run because its outcome cannot bear on F1 (§6b claim A). The covariance-corpus knob (Moir) is untested by this result: neither motivated nor excluded.

### 3b. z-probe (first advisor round, item 2)

`experiments/track_c/c10k_keying_ablation_zprobe.py` runs the engine's unmodified `compute_z` on 3 subjects in K1 style and K3 style with the engine's own templates and records the final target probability at the keyed token, the loss path and the KL term. Reading fixed before the run: K3-style target probability ≥ 0.9 → the z-objective reaches the target and the failure is in the solve; well below K1's → the KL-prompt conflict or the position blocks the target vector.

_Results (`results/c10k_keying_ablation/zprobe.json`):_

| style | subject | steps | target prob (final) | loss final (nll + kl) | ‖z‖ |
|---|---|---|---|---|---|
| K1 | Zorbland | 12 | 0.986 | 0.050 (0.014 + 0.030) | 80.9 |
| K1 | Quaxil | 25 | 0.994 | 0.058 (0.006 + 0.046) | 85.6 |
| K1 | Plurnak | 21 | 0.997 | 0.048 (0.003 + 0.040) | 83.3 |
| K3 | Zorbland | 20 | 0.983 | 0.045 (0.017 + 0.022) | 66.8 |
| K3 | Quaxil | 16 | 0.988 | 0.046 (0.012 + 0.026) | 66.6 |
| K3 | Plurnak | 11 | 0.993 | 0.031 (0.007 + 0.017) | 63.5 |

**Reading (EVIDENCE-SHOWS):** K3-style `compute_z` reaches the target at the keyed `" of"` token (final target probability ≥ 0.983; K1-style ≥ 0.986) with a KL term of the same size as K1's. The z-objective is not where the K3/K4 write is lost, and the KL-prompt conflict is excluded as the cause: **the loss is at the solve.** (‖z‖ is smaller in K3 style, 63–67 vs 81–86, consistent with the last-token residual being a smaller target.)

### 3c. Key-similarity discriminator and N = 1 cells (second advisor round on §6; prereg §6b)

`experiments/track_c/c10k_keying_ablation_keygram.py` → `results/c10k_keying_ablation/keygram.json`:

| layer | subject keys: cos mean / eff. rank | last-token keys: cos mean / frac > 0.9 / eff. rank | ridge/‖k‖² at w = 5000: subject / last | w* (last matches subject) |
|---|---|---|---|---|
| L4 | 0.070 / 16.5 | 0.991 / 1.0 / 1.02 | 5.288 / 44.041 | 600 |
| L5 | 0.041 / 19.8 | 0.991 / 1.0 / 1.02 | 1.241 / 60.24 | 103 |
| L6 | 0.023 / 21.7 | 0.990 / 1.0 / 1.02 | 0.54 / 21.768 | 124 |
| L7 | 0.024 / 21.3 | 0.985 / 1.0 / 1.03 | 0.599 / 12.48 | 240 |
| L8 | 0.028 / 22.5 | 0.991 / 1.0 / 1.02 | 0.478 / 5.654 | 423 |

**Reading (EVIDENCE-SHOWS):** the 24 last-token keys are highly collinear in raw activation space (mean pairwise cosine ≥ 0.985, every pair > 0.9, effective rank ≈ 1.02 at every band layer), while the 24 subject-last-token keys are nearly orthogonal (cosine 0.02–0.07, effective rank 16–23). Raw cosine is the geometry of the measurement, not of the solve: MEMIT solves in covariance-weighted space, and the shared first-token activation (norm 98 at L4, the super activation of `docs/PRIOR_ART_SWEEP_2026-10-04.md` §7) inflates raw cosines; a whitened keygram was not run. **A closed-form solve cannot map 24 near-collinear keys to 24 different targets at this ridge weight:** the keys' small differences lie in low-variance directions, the energy-weighted ridge ratio at w = 5000 is 5.7–60 for last-token keys against 0.5–5.3 for subject keys, so those differences are suppressed; the weight at which they would be amplified to the subject keys' ratio is w* ≈ 100–600 per layer. Route A reached the same mechanism from the other side: AlphaEdit_ARE at L2 = 0.01 fit 24/24 by amplifying those differences 1000× (L4 band norm 3.6×, locality cost F4), and the resulting write is read only from the trained prompt.

**N = 1 single writes (`tools/c10k_keying_ablation_n1.sh`; w = 5000, templates on, A1, one request per run; complete, 12/12 runs):**

| run | subject → value | A1 canon (1 item) | paraphrases hit (of 3) | described-as JS |
|---|---|---|---|---|
| N1_last_0 | Zorbland → Beirut | 100.0 | 0 | 100.0 |
| N1_subject_0 | Zorbland → Beirut | 100.0 | 3 | 94.97 |
| N1_last_1 | Quaxil → Beirut | 100.0 | 0 | 100.0 |
| N1_subject_1 | Quaxil → Beirut | 100.0 | 3 | 97.61 |
| N1_last_2 | Plurnak → Beirut | 100.0 | 0 | 100.0 |
| N1_subject_2 | Plurnak → Beirut | 100.0 | 3 | 94.92 |
| N1_last_3 | Vythorn → Beirut | 100.0 | 0 | 100.0 |
| N1_subject_3 | Vythorn → Beirut | 100.0 | 3 | 93.17 |
| N1_last_4 | Glimsto → Beirut | 100.0 | 0 | 100.0 |
| N1_subject_4 | Glimsto → Beirut | 100.0 | 3 | 89.2 |
| N1_last_5 | Drennik → Beirut | 100.0 | 0 | 100.0 |
| N1_subject_5 | Drennik → Beirut | 100.0 | 3 | 98.01 |

**Claim A (writability): SINGLES LAND (pre-registered label: interference first).** 6/6 single last-token writes land at w = 5000, so the ridge weight does not block a single last-token write. What blocks 24 of them is their collinearity under the covariance-plus-ridge geometry the solve works in; 'interference' and 'ridge' are not separable causes here (the keygram's w* ≈ 100–600 and Route A's 24/24 fit at a 1000× smaller ridge both say a smaller ridge would separate them). The small-ridge sweep is not run because it cannot bear on F1: a last-token write that lands does not transfer anyway (claim B). Zero-edit check not run: a keygram on covariance-whitened keys (C^-1/2·k) would test the collinearity framing directly.

**Claim B (generalisation, read from landed singles): F3 SUFFICIENT (MEMIT, N = 1).** 6/6 last-token singles land with ≤ 1/3 paraphrases while 6/6 subject-keyed singles land with ≥ 2/3; described-as JS gap +5.4 points.

#### Frame-bleed probe (§6b, advisor v2 item 6; `experiments/track_c/c10k_keying_ablation_n1_framebleed.py` → `results/c10k_keying_ablation/n1/framebleed.json`)

Six subjects (`FICTION[0..5]`; §6b pre-registered three, the second three were added as the Codex distinct-value control), both loci, one edit each at w = 5000. The probe imports the c10e harness and calls the same `my_edit` / `compute_P` functions the N = 1 cells ran under LAW#5 INERT (no separate inertness run for the probe); after each edit, top-1 at the twelve Route A real-country frame prompts (`The capital of <Albania … Cuba> is the city of`) and at six never-edited fictional frame prompts (`FICTION[12..17]`).

| subject → value | locus | canon | para (of 3) | real frame prompts flipped to value (of 12) | real capitals still correct (pre → post) | real JS | bystander frame prompts flipped (of 6) | described-as JS | rel. Δ‖W‖ L4 / L8 |
|---|---|---|---|---|---|---|---|---|---|
| Zorbland → Beirut | last | 100 | 0 | **0** | 12 → 12 | 96.46 | **2** | 100.0 | 0.037 / 0.057 |
| Zorbland → Beirut | subject | 100 | 3 | **0** | 12 → 12 | 100.0 | **0** | 96.3 | 0.043 / 0.043 |
| Quaxil → Buenos | last | 100 | 0 | **9** | 12 → 3 | 35.02 | **6** | 99.86 | 0.037 / 0.062 |
| Quaxil → Buenos | subject | 100 | 3 | **0** | 12 → 12 | 100.0 | **0** | 95.8 | 0.044 / 0.041 |
| Plurnak → Damascus | last | 100 | 0 | **0** | 12 → 12 | 96.63 | **6** | 99.99 | 0.036 / 0.058 |
| Plurnak → Damascus | subject | 100 | 3 | **0** | 12 → 12 | 100.0 | **0** | 96.03 | 0.037 / 0.040 |
| Vythorn → Jerusalem | last | 100 | 0 | **0** | 12 → 12 | 98.21 | **6** | 100.0 | 0.036 / 0.059 |
| Vythorn → Jerusalem | subject | 100 | 2 | **0** | 12 → 12 | 100.0 | **0** | 67.35 | 0.033 / 0.047 |
| Glimsto → Lisbon | last | 100 | 0 | **0** | 12 → 12 | 91.07 | **6** | 99.99 | 0.036 / 0.060 |
| Glimsto → Lisbon | subject | 100 | 3 | **0** | 12 → 12 | 100.0 | **0** | 96.19 | 0.032 / 0.046 |
| Drennik → Moscow | last | 100 | 0 | **1** | 12 → 11 | 87.92 | **5** | 100.0 | 0.036 / 0.063 |
| Drennik → Moscow | subject | 100 | 3 | **0** | 12 → 12 | 100.0 | **0** | 94.88 | 0.033 / 0.047 |

**Reading (EVIDENCE-SHOWS): BETWEEN (partly frame-keyed).** The pre-registered H-frame threshold (≥ 6/12 real **and** ≥ 3/6 bystander flips for every landed last-token single) is not met, so the reading is BETWEEN, but the pattern is one-sided: the landed last-token singles rewrite 31/36 never-edited fictional frame prompts to their own value (2/6, 6/6, 6/6, 6/6, 6/6, 5/6) and 10/72 real-country frame prompts (0/12, 9/12, 0/12, 0/12, 0/12, 1/12; real-prompt JS 96.46, 35.02, 96.63, 98.21, 91.07, 87.92), while the subject-keyed singles on the same subjects flip 0 of 108. The write keyed at `" of"` is partly subject-conditioned (Zorbland's fired on its own prompt but on only 2/6 same-frame bystanders; the key cosine is 0.99, not 1.0) and partly a frame write (other subjects' fired on 6/6). The real-capital outlier is not a magnitude effect: the last-token writes have near-identical update norms (L8 relative Δ‖W‖ 0.057, 0.062, 0.058, 0.059, 0.060, 0.063). The alternative that fits is the token prior of the value: `Buenos` is the first token of a real capital the frame already predicts for Argentina (Argentina answered `Buenos` before the edit and is not counted among its 9 flips), so that frame write rides an existing capital-frame direction; values without such a prior override no real capital. The paraphrases, which lack the frame, score 0/3 for every last-token single. **Forward requirement:** the described-as probe (JS ≥ 99.9) saw none of the real-capital flips, so described-as JS alone is not a sufficient locality gate for any write; same-frame prompts must be probed.

**Distinct-value singles (Codex control; the probe rows double as N = 1 cells with per-subject values Beirut, Buenos, Damascus, Jerusalem, Lisbon, Moscow):** last-token singles land 6/6 with **0/18** paraphrase hits; subject-keyed singles land 6/6 with **17/18**. By the §6b post-hoc rule (every last-token single ≤ 1/3, every subject-keyed single ≥ 2/3) claim B stands and the same-value limitation of the chain's N = 1 cells is removed. Per-subject: Zorbland → Beirut last 0/3, subject 3/3; Quaxil → Buenos last 0/3, subject 3/3; Plurnak → Damascus last 0/3, subject 3/3; Vythorn → Jerusalem last 0/3, subject 2/3; Glimsto → Lisbon last 0/3, subject 3/3; Drennik → Moscow last 0/3, subject 3/3. Locality cost of subject keying is uneven: described-as JS 96.3, 95.8, 96.03, 67.35, 96.19, 94.88 (one subject, Vythorn, loses 33 points) against ≥ 99.9 for every last-token single.

## 4. Scope, limitations, what changes

- **Scope:** Qwen2.5-3B base, fp16, band [4–8], ridge weight 5000, one seed; N = 24 for the 2×2 cells, N = 1 for six subjects (the same six in the frame-bleed probe, with distinct values), A1 single-token values (A2 at N = 24 only). One engine. Nothing promotes to C10 (A7 untouched, as pre-registered).
- **What the combined picture says (EVIDENCE-SHOWS, scoped):** in the program's own MEMIT engine, *where* a write is keyed decides *what* is written. Keyed at the subject's last token, the write is a fact about the subject: it fits the trained prompt, transfers to held-out paraphrases, and leaves other countries alone. Keyed at the prompt's final token, the same write with the same engine is read from the frame rather than from the subject: at N = 24 the 24 near-collinear keys cannot be separated by the solve and nothing lands; at N = 1 it lands, is read from the trained prompt only (0 paraphrase hits in every single), and bleeds onto same-frame prompts to a varying degree (see the probe table; the one real-capital override rides the token prior of `Buenos`). This is the behavioural face of the recall-mechanism literature (relations decode from the subject's last token, `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md`) inside the program's engine.
- **For Route A's F3 ("the port keys the write at the last prompt token, hence 0/72"):** sufficient in MEMIT at N = 1; consistent with F3; not exclusive (Route A also differs in z-objective, preservation term, projector). F3 moves from I-INFER to **EVIDENCE-SHOWS-in-MEMIT (N = 1, qualified)**; the Route A attribution itself stays I-INFER because Route A's modules were not re-run with subject keying.
- **Changes:** the memory_mirror rule "read the keying locus against the generalisation criterion before porting an editor" becomes **unconditional for this engine's mechanism class**: a last-token-keyed write is not a subject fact. Option (ii) (subject-keyed per-token hybrid) keeps its rationale with evidence behind it. The small-ridge sweep is not run (it cannot bear on F1: a landed last-token write does not transfer). The covariance-corpus knob (Moir) is untested by this result and keeps whatever motivation it had from Route A's ridge diagnostic; nothing here motivates or excludes it. **New forward requirement:** every locality gate must include same-frame prompts (described-as JS was blind to 9/12 real-capital flips).
- **Provenance note:** the K1–K4 and `n1/N1_*.json` records carry the harness default `decision_id: D-C10e-bandknob` because the chain scripts did not set `DECISION_ID`; the records are not edited (manifests are never rewritten in place); the chain scripts now export the correct ID for future runs; `framebleed*.json` carry `D-C10k-keying-ablation`.
- **Limitations:** N = 1 and six subjects; the claim-B criterion and the frame-bleed probe were pre-registered after three of twelve runs were visible (prereg §6b, timing disclosure; the remaining nine runs showed no variance, so the thresholds were not decisive); single-token values only, and **all six N = 1 singles were written with the same value ("Beirut")**, an artefact of the single-subject stimulus assignment (`FICTION[off:off+1]` always maps to the same pool slot) — removed by the distinct-value control: the frame-bleed probe used distinct per-subject values (Beirut, Buenos, Damascus, Jerusalem, Lisbon, Moscow) and reproduced the 0/3 paraphrase result on every last-token single; one seed.

## 5. Advisor and close-out

Advisor on this result: first pass `logs/claude_c10k_keying_ablation_result_review.md` (FIX-FIRST: z-probe, no over-claim on the ridge — resolved by §3b/§3c), Codex `logs/codex_c10k_keying_ablation_result_review.md` (FIX-FIRST: same items + close-out not done); on this result: Claude `logs/claude_c10k_keying_ablation_result_review_v2.md` (FIX-FIRST, wording: headline used H-frame language against the BETWEEN reading; "interference first" and "within rounding" unsupported; Moir withdrawal untested; `Buenos` outlier confounded by token prior; described-as blind to frame damage; pre-registration timing to be tagged inline — all applied here) and Codex `logs/codex_c10k_keying_ablation_result_review_v2.md` (FIX-FIRST: close-out not yet done; `decision_id` provenance drift in the result JSONs — disclosed above; same-value limitation — answered by the distinct-value control; frame-write wording — softened). Both reviews read the pre-fix render. CORPUS entry: `CORPUS/43_C10K_KEYING_ABLATION.md`. Close-out: `tools/closeout_check.py D-C10k-keying-ablation`.
