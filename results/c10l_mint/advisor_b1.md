# Advisor pass on amendment B1 (Codex gpt-5.5, 2026-10-05)

Disposition: FIX-FIRST item 1 folded (`para_full_binding_n` + `c10l_mint_read.py`); items 2–5 confirm B1. Mint step 0 may run.

## Review text (verbatim)

**Verdict: FIX-FIRST**

**Single most important thing:** before any behavioural arm runs, make the binding mint score unambiguous in the JSON/read path: a top-level `para_full_binding_n = para_full_n - step0_para_full` or a mint reader that asserts it uses `extra.para_full_minus_step0`, not raw `para_full_n`.

**Issues**

1. **Binding metric ambiguity can still contaminate §6.**  
   B1 says mint arms are read post-minus-step-0, but the harness still emits raw `para_full_n` as the primary arm field, while the adjusted value is buried under `extra`. A later reader/CORPUS write could accidentally use raw counts. `docs/C10L_MINT_TOKEN_PREREG.md:69`, `docs/C10L_MINT_TOKEN_PREREG.md:102`, `experiments/track_c/c10e_bandknob.py:390`, `experiments/track_c/c10e_bandknob.py:478-480`, `experiments/track_c/c10l_mint_arms.py:55-56`.

2. **G choice: keep mean removed.**  
   For this arm’s actual criterion, all-but-the-top with mean removed is the right primary G. Retaining the mean would test a softer adjacent criterion: “looks more like ordinary rows after top-PC removal,” while leaving a shared component that B1 is explicitly trying to remove. P3 and I-11 are the right fail-closed guards if mean-removed rows fall off the usable output manifold. `docs/C10L_MINT_TOKEN_PREREG.md:96-100`, `experiments/track_c/c10l_mint_lib.py:79-83`, `experiments/track_c/c10l_mint_step0.py:85-89`.

3. **k = 20 is acceptable; do not add a second binding k now.**  
   It is frozen, simple, and declared as `d/100`; adding another k as a candidate pass arm reopens researcher degrees of freedom. If wanted, log non-binding step-0 sensitivity only. `docs/C10L_MINT_TOKEN_PREREG.md:98`, `experiments/track_c/c10l_mint_lib.py:51-57`.

4. **The live-token rule is sound only with the adjusted binding score.**  
   A single live token does not poison SPAN if the binding count subtracts step-0 recall and the init-level exclusion remains `>2/72` or `>=3` cannibal. Without issue 1 fixed, it is too easy to over-read raw hits. `docs/C10L_MINT_TOKEN_PREREG.md:102`, `experiments/track_c/c10l_mint_step0.py:86-89`.

5. **No substantive §6 reopening found.**  
   B1 narrows G to the intended “collapse component removed” arm and preserves the G-vs-N/M readings. The stale §4 prose is contradictory but explicitly superseded by §10; still, a reader should treat §10 as binding. `docs/C10L_MINT_TOKEN_PREREG.md:45`, `docs/C10L_MINT_TOKEN_PREREG.md:53`, `docs/C10L_MINT_TOKEN_PREREG.md:98-102`.

Cheapest overturning control: step 0 itself can overturn B1 if G has poor P3 convergence or remains collapsed by effective rank/cosine; behavioural G vs N then tests whether “collapse removal” matters. External claims about Mu & Viswanath / arXiv 2604.02324 were not independently rechecked here: **UNVERIFIABLE** beyond the prereg text.