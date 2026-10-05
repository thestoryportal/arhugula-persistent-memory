# Keying-locus ablation in the program's MEMIT engine — result (D-C10k-keying-ablation)

_Result 2026-10-04. Pre-registered `docs/C10K_KEYING_ABLATION_PREREG.md` (v3 §3 for the N = 24 cells; §6 and §6b amendments, three advisor rounds). Records `results/c10k_keying_ablation/K{1..4}.json`, `zprobe.json`, `keygram.json`, `n1/N1_*.json`, `n1/framebleed.json`; logs `logs/c10k_keying_ablation_*.log`; harness `experiments/track_c/c10e_bandknob.py` (knobs `C10_KEY_LOCUS`, `C10_CTX_TEMPLATES`, `C10_ARMS`, `C10_RECIPES`, `N_EDIT`, `C10_SUBJECT_OFFSET`; engine unmodified, LAW#5 INERT in every cell). Chains `tools/c10k_keying_ablation_chain.sh`, `tools/c10k_keying_ablation_n1.sh`; probe `experiments/track_c/c10k_keying_ablation_n1_framebleed.py`._

## 1. Reading: **KEYING LOCUS DECIDES WHAT IS WRITTEN — a last-token-keyed write is read from the frame, not the subject (F3 SUFFICIENT, MEMIT, N = 1; frame-bleed BETWEEN: prior-free frame prompts take the value, real capitals mostly resist)**

- **N = 24 cells (prereg §3):** INVALID-LAST-TOKEN-CELLS (K3/K4 canon < 90; no keying reading at N = 24). Gate: K1 A1 95.8 / A2 97.2 vs R0 94.4 / 98.6 → **PASS**. Validity prints confirm the keyed token (subject's last token in K1/K2; the final `" of"` in K3/K4) and byte-identical paraphrase and locality strings across cells.
- **Why the last-token cells failed (§3b–§3c):** the z-objective reaches the target, so the loss is at the solve; the 24 last-token keys are one vector to within rounding (cosine ≥ 0.985, effective rank 1.02), so one solve cannot map them to 24 targets. **Claim A: INTERFERENCE FIRST.** 6/6 single last-token writes land at w = 5000, so ridge magnitude is withdrawn as the primary cause of the N = 24 collapse; the small-ridge sweep is not run.
- **N = 1 cells (prereg §6b, the valid last-token cells): claim B = F3 SUFFICIENT (MEMIT, N = 1).** 6/6 last-token singles land with ≤ 1/3 paraphrases while 6/6 subject-keyed singles land with ≥ 2/3; described-as JS gap +5.4 points. Paraphrase hits: last-token singles 0/18, subject-keyed singles 18/18.
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
- **The first-pass attribution to the covariance ridge (Route A's ridge diagnostic: last-token keys 17–180× under the ridge at w = 15000; 5.7–60× at w = 5000) is superseded by §3c:** the ridge enters second, after key interference. The pre-registered small-ridge sweep (§6) is therefore not run (§6b claim A).

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

**Reading (EVIDENCE-SHOWS):** the 24 last-token keys are one vector to within rounding (pairwise cosine ≥ 0.985 on average, every pair > 0.9, effective rank ≈ 1.02 at every band layer), while the 24 subject-last-token keys are nearly orthogonal (cosine 0.02–0.07, effective rank 16–23). **A single closed-form solve cannot map one key to 24 different targets; the K3/K4 collapse at w = 5000 is key interference first.** The ridge enters second: the keys' small differences lie in low-variance directions, and the energy-weighted ridge ratio at w = 5000 is 5.7–60 for last-token keys against 0.5–5.3 for subject keys, so those differences are suppressed; the weight at which they would be amplified to the subject keys' ratio is w* ≈ 100–600 per layer. Route A reached the same mechanism from the other side: AlphaEdit_ARE at L2 = 0.01 fit 24/24 by amplifying those differences 1000× (L4 band norm 3.6×, locality cost F4), and the resulting write is read only from the trained prompt.

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

**Claim A (writability): INTERFERENCE FIRST.** 6/6 single last-token writes land at w = 5000, so ridge magnitude is withdrawn as the primary cause of the N = 24 collapse; the small-ridge sweep is not run.

**Claim B (generalisation, read from landed singles): F3 SUFFICIENT (MEMIT, N = 1).** 6/6 last-token singles land with ≤ 1/3 paraphrases while 6/6 subject-keyed singles land with ≥ 2/3; described-as JS gap +5.4 points.

#### Frame-bleed probe (§6b, advisor v2 item 6; `experiments/track_c/c10k_keying_ablation_n1_framebleed.py` → `results/c10k_keying_ablation/n1/framebleed.json`)

Three subjects, both loci, one edit each at w = 5000 through the harness's own edit path; after each edit, top-1 at the twelve Route A real-country frame prompts (`The capital of <Albania … Cuba> is the city of`) and at six never-edited fictional frame prompts (`FICTION[12..17]`).

| subject → value | locus | canon | para (of 3) | real frame prompts flipped to value (of 12) | real capitals still correct (pre → post) | real JS | bystander frame prompts flipped (of 6) | described-as JS |
|---|---|---|---|---|---|---|---|---|
| Zorbland → Beirut | last | 100 | 0 | **0** | 12 → 12 | 96.46 | **2** | 100.0 |
| Zorbland → Beirut | subject | 100 | 3 | **0** | 12 → 12 | 100.0 | **0** | 96.3 |
| Quaxil → Buenos | last | 100 | 0 | **9** | 12 → 3 | 35.02 | **6** | 99.86 |
| Quaxil → Buenos | subject | 100 | 3 | **0** | 12 → 12 | 100.0 | **0** | 95.8 |
| Plurnak → Damascus | last | 100 | 0 | **0** | 12 → 12 | 96.63 | **6** | 99.99 |
| Plurnak → Damascus | subject | 100 | 3 | **0** | 12 → 12 | 100.0 | **0** | 96.03 |

**Reading (EVIDENCE-SHOWS): BETWEEN (partly frame-keyed).** The pre-registered H-frame threshold (≥ 6/12 real **and** ≥ 3/6 bystander flips for every landed last-token single) is not met, so the reading is BETWEEN, but the pattern is one-sided: the landed last-token singles rewrite 14/18 never-edited fictional frame prompts to their own value (2/6, 6/6, 6/6) and 9/36 real-country frame prompts (0/12, 9/12, 0/12; real-prompt JS 96.46, 35.02, 96.63), while the subject-keyed singles on the same subjects flip 0 of 54. The write keyed at `" of"` is read by every prompt that ends in the frame and has no strong prior of its own; real capitals resist it unless the write is large enough (one of three singles overrode 9/12 real capitals). It never encodes the subject: paraphrases, which lack the frame, score 0/3, and the described-as probe (JS ≥ 99.9) sees none of the damage.

## 4. Scope, limitations, what changes

- **Scope:** Qwen2.5-3B base, fp16, band [4–8], ridge weight 5000, one seed; N = 24 for the 2×2 cells, N = 1 for six subjects (three in the probe), A1 single-token values (A2 at N = 24 only). One engine. Nothing promotes to C10 (A7 untouched, as pre-registered).
- **What the combined picture says (EVIDENCE-SHOWS, scoped):** in the program's own MEMIT engine, *where* a write is keyed decides *what* is written. Keyed at the subject's last token, the write is a fact about the subject: it fits the trained prompt, transfers to held-out paraphrases, and leaves other countries alone. Keyed at the prompt's final token, the same write with the same engine is a fact about the frame: at N = 24 the 24 near-identical keys interfere and nothing lands; at N = 1 it lands, is read from the trained prompt only, and is read by every prior-free prompt that shares the frame (14/18 never-edited fictional frame prompts take the value) while real capitals mostly resist. This is the behavioural face of the recall-mechanism literature (relations decode from the subject's last token, `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md`) inside the program's engine.
- **For Route A's F3 ("the port keys the write at the last prompt token, hence 0/72"):** sufficient in MEMIT at N = 1; consistent with F3; not exclusive (Route A also differs in z-objective, preservation term, projector). F3 moves from I-INFER to **EVIDENCE-SHOWS-in-MEMIT (N = 1, qualified)**; the Route A attribution itself stays I-INFER because Route A's modules were not re-run with subject keying.
- **Changes:** the memory_mirror rule "read the keying locus against the generalisation criterion before porting an editor" becomes **unconditional for this engine's mechanism class**: a last-token-keyed write is not a subject fact. Option (ii) (subject-keyed per-token hybrid) keeps its rationale with evidence behind it. The small-ridge sweep is not run; the covariance-corpus knob (Moir) is no longer motivated by this result (the ridge was not the primary limiter).
- **Limitations:** N = 1 and six subjects; the claim-B criterion and the frame-bleed probe were pre-registered after three of twelve runs were visible (prereg §6b, timing disclosure); single-token values only, and **all six N = 1 singles were written with the same value ("Beirut")**, an artefact of the single-subject stimulus assignment (`FICTION[off:off+1]` always maps to the same pool slot) — the frame-bleed probe used three distinct values (Beirut, Buenos, Damascus) and reproduced the 0/3 paraphrase result on each; one seed.

## 5. Advisor and close-out

Advisor on this result: first pass `logs/claude_c10k_keying_ablation_result_review.md` (FIX-FIRST: z-probe, no over-claim on the ridge — resolved by §3b/§3c), Codex `logs/codex_c10k_keying_ablation_result_review.md` (FIX-FIRST: same items + close-out not done); final `logs/claude_c10k_keying_ablation_result_review_v2.md` and `logs/codex_c10k_keying_ablation_result_review_v2.md`. CORPUS entry: `CORPUS/43_C10K_KEYING_ABLATION.md`. Close-out: `tools/closeout_check.py D-C10k-keying-ablation`.
