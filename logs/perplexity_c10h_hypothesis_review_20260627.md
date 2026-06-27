# Perplexity C10h Hypothesis Review - 2026-06-27

Model: `sonar-reasoning-pro`

## Advisory Response

Verdict: The team’s interpretation that the *local AnyEdit transplant is not yet a valid test of AnyEdit* is technically sound and appropriately cautious, but it is not fully closed-form: there are still plausible confounds (especially H1–H3) that could restore A1/A2 control performance with one focused parity audit.  
C10’s failure under MEMIT/AlphaEdit is **expected** from the literature; the transplant failure on easy controls is **unexpected** and should not be used to judge AnyEdit itself.

---

## 1. Direct verdict (evidence vs inference)

**Evidence (from your repo and external literature)**

- Baseline MEMIT/AlphaEdit on your setup:  
  - A1 single-token values: ~93–100% held-out paraphrase full-sequence exact match.  
  - A2 prior-coherent multi-token values: ~97–100%.  
- C10 hard project-coined multi-word semantic values: residual expression only ~19–31% on held-out paraphrase full-sequence, and standard MEMIT knob-turning (band position, width, edit strength, layer sweep) did not fix this.
- Local AnyEdit-style ARE transplant:  
  - Window_size=1: token-alignment and no-op/Law#5 inertness gates pass, but A1/A2 collapse from 93.1/97.2 to 0.0/0.0; A7 hard values worsen from 12.5 to 1.4.  
  - Window_size=50: same gates pass, baseline A1/A2 97.2/100.0 collapse to 0.0/0.0.  
- AnyEdit paper:  
  - AnyEdit decomposes long-form knowledge into sequential chunks and iteratively edits key tokens, specifically to overcome the “efficacy barrier” of single-token editing for long/complex targets.[1][8][9][13][15]  
  - MEMIT and AlphaEdit show **significant performance drops** when editing targets exceed ~30 tokens.[3][8][9]  
  - Low original probability of target knowledge is identified as a **fundamental limitation** of single-token editing methods on complex/diverse-formatted knowledge.[1][3][8][9]  
- Other editing work: MEMIT exhibits key-collision and degradation when repeatedly editing the same subject, illustrating how geometry and indexing issues can sharply degrade performance.[6]

**Inference (your interpretation and where it is strong / weak)**

1. **“Transplant invalid before A7”: technically strong for *this implementation***  
   - Your own pipeline shows: identical evaluation, same model, same prompts → MEMIT/AlphaEdit succeed on A1/A2; switching only the active edit path to local AnyEdit-style ARE yields 0% success while no-op gates pass.  
   - This pattern is highly characteristic of “wrong edit position / wrong target construction / wrong update geometry,” not “method family intrinsically fails.”  
   - Therefore, *this particular transplant* is indeed not yet an interpretable test of AnyEdit.

2. **C10 being hard for MEMIT-like methods: technically well-supported**  
   - C10 values are project-coined multi-word semantics with low prior probability.  
   - AnyEdit authors explicitly show low base probability and long/diverse-form knowledge are where single-token methods (MEMIT, AlphaEdit) hit an efficacy barrier and degrade sharply.[1][3][8][9]  
   - Your C10 failure is therefore consistent with expected MEMIT limitations, not necessarily an implementation bug.

3. **Where your interpretation is overconfident or under-specified**  
   - You are correct that no-op/inertness gates do not validate:  
     - ARE target construction  
     - Loss-mask correctness  
     - Lookup position correctness  
     - Update geometry  
   - However, you are *implicitly treating* the transplant’s failure as evidence against AnyEdit-style editing as a route for C10. That is not yet justified: the failure is far more likely a local implementation issue (H1–H3) than a method-family limitation, given AnyEdit’s published robustness on long-form edits.[1][8][9][13]  
   - Conclusion: the interpretation is **technically sound for your local transplant**, but **incomplete** as a verdict on AnyEdit or on the broader possibility of an “LLM-as-Database” spec using autoregressive edits.

---

## 2. Ranking H1–H5 by likelihood and usefulness

Here “likelihood” refers to explaining the A1/A2 collapse; “usefulness” refers to what most advances the project.

**Likelihood ranking (for A1/A2 = 0% under AnyEdit transplant)**

1. **H1 – Lookup-index / edit-position mismatch (most likely)**  
   - Symptom pattern: no-op gate passes, token-alignment gate passes, but active edit produces **systematic zero success** even on trivially easy A1/A2 that MEMIT/AlphaEdit handle near-perfectly.  
   - AnyEdit relies on editing the correct “key token” in each chunk.[1][8][9] If your transplant is applying the ARE delta to the wrong position (e.g., wrong subject sub-token, wrong answer token, or off-by-one in the autoregressive step), you get exactly:  
     - Edits that meaningfully change some hidden state,  
     - But that never correspond to the intended fact → 0% para_full.  
   - This is the canonical failure mode for index misalignment.

2. **H2 – ARE target / loss-mask construction mismatch (very likely)**  
   - AnyEdit constructs target hidden states and loss masks over sequential chunks to ensure the edited knowledge is reflected consistently in generation.[1][8][9][13]  
   - If locally you:  
     - Teacher-force different sequences,  
     - Compute the target on the wrong tokens,  
     - Or mis-specify the loss mask (e.g., including non-answer positions or excluding the actual answer),  
     the model can be pushed towards a distribution that is not your evaluation answer → again 0% para_full while no-op tests look fine.  
   - Given the complexity of ARE target construction, this is nearly as likely as H1.

3. **H3 – Local MEMIT geometry incompatible with ARE targets (moderately likely)**  
   - AnyEdit’s edit geometry is autoregressive and chunk-wise, with explicit reasoning about interference between hidden-state perturbations.[1][8][9]  
   - MEMIT’s geometry is designed for single-token edits in static forward passes; bolting ARE deltas into MEMIT

## Raw Citation/Search Metadata

```json
[
  "https://arxiv.org/html/2502.05628v1",
  "https://dcd-anyedit.github.io",
  "https://arxiv.org/html/2502.05628v3",
  "https://vldb.org/workshops/2024/proceedings/LLM+KG/LLM+KG-2.pdf",
  "https://arxiv.org/html/2411.15738v3",
  "https://aclanthology.org/2025.findings-acl.415.pdf",
  "https://icml.cc/virtual/2025/poster/44807",
  "http://staff.ustc.edu.cn/~hexn/papers/icml25-AnyEdit.pdf",
  "https://proceedings.mlr.press/v267/jiang25b.html",
  "https://github.com/zjunlp/KnowledgeEditingPapers",
  "https://github.com/DCDmllm/AnyEdit",
  "https://www.linkedin.com/pulse/rome-vs-memit-evolution-mass-editing-transformer-sewak-ph-d--l11vc",
  "https://openreview.net/forum?id=aJIoBur0Ef",
  "https://www.sciencedirect.com/science/article/pii/S0092867420306322",
  "https://github.com/jianghoucheng/AnyEdit"
]
```
