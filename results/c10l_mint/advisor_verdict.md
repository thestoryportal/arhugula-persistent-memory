# Advisor review of the D-C10l-mint finding before CORPUS (Codex gpt-5.5, cross-family, 2026-10-05)

Disposition: PROCEED to CORPUS as a scoped PARTIAL x2 / G≈N characterisation; narrow language folded into CORPUS/45 (G did not beat N; minted-vs-rare scoped; P-iv admission-only; P4 as amendment/operator check; six excluded claims; C10 OPEN/BLOCKING, option (iv) a live partial lead).

## Review text (verbatim)

**PROCEED to CORPUS**, but only as a scoped `PARTIAL ×2 / G≈N` characterization. The result is useful and F1-relevant, but it is not a route closure, not a SPAN result, and not evidence that initialization quality helps.

**Single most important next thing:** write CORPUS/45 with deliberately narrow language: “in this N=24, one-seed harness, admitted minted-token arms improve over A7-multi and exceed A1-rare, but remain far below A1; G is not better than N, so row-content/grounding benefit is not shown.”

**Issues, Priority Order**

1. **Verdict is PARTIAL, not SPAN.**  
   The prereg says `PARTIAL` is `30/72 ≤ A7-mint-G < A1 − 5/72` with locality satisfied, and SPAN requires near-A1 behavior. G is 39/72 with same-run A1 68/72; N is 46/72 with same-run A1 72/72. That supports PARTIAL for G and a corroborating PARTIAL-like N read, not route viability.  
   `docs/C10L_MINT_TOKEN_PREREG.md:71-76`, `results/c10l_mint/arm_G.json:250-256`, `results/c10l_mint/arm_G.json:404-414`, `results/c10l_mint/arm_N.json:250-256`, `results/c10l_mint/arm_N.json:404-414`.

2. **N > G is an over-read if written as a directional finding.**  
   The observed ordering is real: N binding 46 vs G binding 39. But 7/72 at one seed should be written as “G did not beat N; random matched-norm did at least as well in this run,” not “N is better” or “de-collapsing hurts.”  
   `results/c10l_mint/arm_G.json:410-414`, `results/c10l_mint/arm_N.json:410-414`.

3. **“Minted token transfers better than a real implausible token” is licensed only as scoped observation.**  
   Yes: A1-rare is 25/72, while G/N are 39/46. But do not write this as a general statistical claim; A1-rare is a BPE-id rarity proxy, not a pure “implausibility alone” manipulation.  
   `results/c10l_mint/arm_rare.json:240-253`, `results/c10l_mint/step0_probe.json:351-353`, `results/c10l_mint/arm_G.json:413-414`, `results/c10l_mint/arm_N.json:413-414`.

4. **Do not claim P-iv proved init-quality relevance behaviorally.**  
   Step 0 confirms M/Z collapse and excludes them by P3, while G/N are admitted. But the behavioral comparison is G vs N, and G does not win. So P-iv is useful as an admission/collapse diagnostic, not evidence that “better grounded init” improves the write.  
   `results/c10l_mint/step0_probe.json:920-963`, `results/c10l_mint/step0_probe.json:1538-1577`, `results/c10l_mint/step0_probe.json:2150-2189`, `results/c10l_mint/step0_probe.json:2760-2818`.

5. **P4 GGUF should be recommended only as a new amendment/operator deployment check, not as part of this frozen result.**  
   The prereg runs P4 only after SPAN or PARTIAL-G≫N; this is PARTIAL-G≈N. Given minted tokens are deployment artifacts and `.vindex` CPU serving is central, a P4 amendment is reasonable, but CORPUS/45 should not imply P4 is required to validate the science verdict.  
   `docs/C10L_MINT_TOKEN_PREREG.md:35`, `docs/C10L_MINT_TOKEN_PREREG.md:84-86`, `docs/SPEC_E2E_GROUND_TRUTH.md:82-83`.

6. **Must not write to CORPUS:**  
   Do not write “the span is the wall,” “minting solves C10,” “N is better than G,” “implausibility alone explains the gap,” “trained init is ruled out generally,” or “F1/C10 status changes.” The correct F1 effect is: C10 remains OPEN/BLOCKING; option (iv) is now a live partial lead with a residual wall.  
   `docs/program_state.json:14-19`, `docs/program_state.json:8-12`.

**Cheapest overturning tests:** second seed / second random N init for G-vs-N and minted-vs-rare; separate P4 amendment for the deployment artifact question. Neither is required before CORPUS if the writeup stays scoped.