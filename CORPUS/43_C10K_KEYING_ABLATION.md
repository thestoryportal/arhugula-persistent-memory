# 43 — Keying-locus ablation in the program's MEMIT engine: last-token-keyed writes land but do not transfer; partly frame-keyed (F3 SUFFICIENT in MEMIT, N = 1)

_Result 2026-10-04. Decision-ID D-C10k-keying-ablation ⟨D-C10k-keying-ablation@110558e3⟩. Pre-registered `docs/C10K_KEYING_ABLATION_PREREG.md` (v3 §3; amendments §6, §6b; three advisor rounds). Full detail `docs/C10K_KEYING_ABLATION_RESULT.md`. Records `results/c10k_keying_ablation/` (`K{1..4}.json`, `zprobe.json`, `keygram.json`, `n1/N1_*.json`, `n1/framebleed.json`, `n1/framebleed_b.json`); harness `experiments/track_c/c10e_bandknob.py` (knobs only; engine unmodified, LAW#5 INERT every cell); chains `tools/c10k_keying_ablation_chain.sh`, `tools/c10k_keying_ablation_n1.sh`; probe `experiments/track_c/c10k_keying_ablation_n1_framebleed.py`. Reviews: `logs/claude_c10k_keying_ablation_result_review{,_v2}.md`, `logs/codex_c10k_keying_ablation_result_review{,_v2}.md`._

## Claim class
**Single-variable mechanism test in the program's own engine (LAW#5: harness knobs only) — NOT C10 evidence (A7 untouched); sufficient-in-MEMIT at N = 1, not exclusive, not a re-run of Route A's modules.**

## VERDICT — KEYING LOCUS DECIDES WHAT IS WRITTEN — last-token-keyed singles land but do not transfer to paraphrases and bleed onto same-frame prompts to a varying degree (F3 SUFFICIENT, MEMIT, N = 1; frame-bleed BETWEEN)

**N = 24 (prereg §3):** INVALID-LAST-TOKEN-CELLS (K3/K4 canon < 90; no keying reading at N = 24).

| cell | key locus | templates | A1 canon / para_full | A2 canon / para_full | validity |
|---|---|---|---|---|---|
| K1 | subject | on | 100 / **95.8** | 100 / **97.2** | valid (LAW#3 gate PASS) |
| K2 | subject | off | 100 / **91.7** | 100 / **88.9** | valid |
| K3 | last | on | 29.2 / **0.0** | 4.2 / **0.0** | INVALID (canon < 90) |
| K4 | last | off | 25.0 / **0.0** | 8.3 / **0.0** | INVALID (canon < 90) |

**Mechanism of the N = 24 failure (§3b–§3c):** z-probe — K3-style `compute_z` reaches the target (prob ≥ 0.983), so the loss is at the solve; keygram — the 24 last-token keys have mean pairwise cosine ≥ 0.985 and effective rank 1.02 at every band layer in raw space (subject keys 0.02–0.07, rank 16–23): near-collinear keys whose differences the ridge suppresses (5.7–60× over key energy at w = 5000 vs 0.5–5.3 for subject keys); collinearity and ridge are not separable causes here, and a whitened keygram was not run. Claim A: **SINGLES LAND (pre-registered label: interference first)** — 6/6 single last-token writes land at w = 5000, so the ridge weight does not block a single last-token write. What blocks 24 of them is their collinearity under the covariance-plus-ridge geometry the solve works in; 'interference' and 'ridge' are not separable causes here (the keygram's w* ≈ 100–600 and Route A's 24/24 fit at a 1000× smaller ridge both say a smaller ridge would separate them). The small-ridge sweep is not run because it cannot bear on F1: a last-token write that lands does not transfer anyway (claim B). Zero-edit check not run: a keygram on covariance-whitened keys (C^-1/2·k) would test the collinearity framing directly.

**N = 1 (prereg §6b; the valid last-token cells, w = 5000):** last-token singles land 6/6 with 0/18 paraphrase hits; subject-keyed singles land 6/6 with 18/18 hits (6/6 at ≥ 2/3). Claim B: **F3 SUFFICIENT (MEMIT, N = 1)** — 6/6 last-token singles land with ≤ 1/3 paraphrases while 6/6 subject-keyed singles land with ≥ 2/3; described-as JS gap +5.4 points.

**Frame-bleed probe (§6b): BETWEEN (partly frame-keyed).**

| subject → value | locus | canon | para (of 3) | real frame prompts → value (of 12) | real capitals correct pre → post | bystander frame prompts → value (of 6) | described-as JS |
|---|---|---|---|---|---|---|---|
| Zorbland → Beirut | last | 100 | 0 | **0** | 12 → 12 | **2** | 100.0 |
| Zorbland → Beirut | subject | 100 | 3 | **0** | 12 → 12 | **0** | 96.3 |
| Quaxil → Buenos | last | 100 | 0 | **9** | 12 → 3 | **6** | 99.86 |
| Quaxil → Buenos | subject | 100 | 3 | **0** | 12 → 12 | **0** | 95.8 |
| Plurnak → Damascus | last | 100 | 0 | **0** | 12 → 12 | **6** | 99.99 |
| Plurnak → Damascus | subject | 100 | 3 | **0** | 12 → 12 | **0** | 96.03 |
| Vythorn → Jerusalem | last | 100 | 0 | **0** | 12 → 12 | **6** | 100.0 |
| Vythorn → Jerusalem | subject | 100 | 2 | **0** | 12 → 12 | **0** | 67.35 |
| Glimsto → Lisbon | last | 100 | 0 | **0** | 12 → 12 | **6** | 99.99 |
| Glimsto → Lisbon | subject | 100 | 3 | **0** | 12 → 12 | **0** | 96.19 |
| Drennik → Moscow | last | 100 | 0 | **1** | 12 → 11 | **5** | 100.0 |
| Drennik → Moscow | subject | 100 | 3 | **0** | 12 → 12 | **0** | 94.88 |

## Findings (scoped: Qwen2.5-3B base, fp16, band [4–8], w = 5000, 1 seed; N = 24 for the 2×2, N = 1 for six subjects, the same six in the frame-bleed probe with distinct values; A1 single-token values)
- **F-A1 (EVIDENCE-SHOWS).** In the program's engine, 24 writes keyed at the prompt's final token do not land (canon 29.2 / 25.0 % A1) because their keys are near-collinear and the solve cannot separate them at this ridge weight; the same 24 writes keyed at the subject land and transfer (95.8 / 97.2).
- **F-A2 (EVIDENCE-SHOWS).** A single write keyed at the prompt's final token lands (6/6) and is read from the trained prompt only (0/18 paraphrase hits); the same single write keyed at the subject lands and transfers (18/18).
- **F-A3 (EVIDENCE-SHOWS).** real-country frame prompts flipped to the edited value 0/9/0/0/0/1 of 12 (subject-keyed 0/0/0/0/0/0), never-edited fictional frame prompts 2/6/6/6/6/5 of 6 (subject-keyed 0/0/0/0/0/0): the landed last-token write bleeds onto prompts that share the frame `… is the city of` to a varying degree (31/36 never-edited fictional frame prompts and 10/72 real-country prompts take the value; the single real-capital override rides the token prior of `Buenos`, update norms being near-identical), damage the described-as locality probe cannot see; the subject-keyed write touches none of them (distinct-value singles (Codex control, 6 subjects, values Beirut, Buenos, Damascus, Jerusalem, Lisbon, Moscow): last-token 0/18 paraphrase hits vs subject-keyed 17/18; subject-keyed described-as JS 67.35–96.3).
- **F-A4 (EVIDENCE-SHOWS).** Templates are not necessary for ≥ 80 % paraphrase transfer with subject keying (K2 91.7 / 88.9); they add about 4–8 points.
- **F-A4b (EVIDENCE-SHOWS).** distinct-value singles (Codex control, 6 subjects, values Beirut, Buenos, Damascus, Jerusalem, Lisbon, Moscow): last-token 0/18 paraphrase hits vs subject-keyed 17/18; subject-keyed described-as JS 67.35–96.3; subject keying costs ≈ 5 points of described-as JS (89–98 vs 100), and described-as JS was blind to the real-capital flips, so same-frame prompts are a required locality probe for any write.
- **F-A5 (I-INFER).** Route A's F3 (the ported AnyEdit keys at the last prompt token, hence 0/72) is **sufficient in MEMIT** by F-A2/F-A3; it is not shown exclusive for Route A, whose modules also differ in z-objective, preservation term and projector and were not re-run with subject keying.

## What this changes
- The memory_mirror rule "read the keying locus against the generalisation criterion before porting an editor" becomes **unconditional for this mechanism class**: a last-token-keyed write does not yield a subject fact (it lands, does not transfer, and bleeds onto same-frame prompts). Option (ii) (subject-keyed per-token hybrid) keeps its rationale, now with in-engine evidence.
- The small-ridge sweep (§6) is not run: a landed last-token write does not transfer, so the sweep cannot bear on F1. The covariance-corpus knob (Moir) is untested by this result.
- Provenance: K1–K4 and `n1/N1_*.json` carry the harness default `decision_id: D-C10e-bandknob` ⟨D-C10e-bandknob@82b491dc⟩ (chain scripts did not set it; now fixed for future runs; records not rewritten).
- C10 unchanged (A7 not run). The operator decision on the forward route stands: (i) LRE-faithfulness admission test, (ii) subject-keyed per-token hybrid, (iii) accept-bounded + side-store.
- Limitations: N = 1 and six subjects; single-token values; one seed; the twelve chain runs all used the value `Beirut` (removed by the distinct-value control, §6b post-hoc addendum); the claim-B criterion and the probe were pre-registered after three of twelve runs were visible (prereg §6b, timing disclosure).
