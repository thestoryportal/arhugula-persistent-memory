# DOWKE — arXiv 2608.16932

Source: https://arxiv.org/html/2608.16932

## Headings
# DOW-KE: Anchor-Free Multi-Layer Knowledge Editing via Direct End-to-End Weight Optimization
## Introduction
## Related Work
### Locate-then-Edit Methods
### Other Knowledge-Editing Paradigms
## Preliminaries
### Residual Stream and FFN Key-Value Memory
### Anchor-Target Optimization
### Closed-Form Weight Update
## Empirical Study
### Single-Anchor Multi-Layer Editing
### Multiple Anchors and Multi-Layer Editing
### Removing the Intermediate Anchor
## Method
## Experiments
### Models and Datasets
### Evaluation Metrics and Experiment Setup
### Comparative Experiments
### Ablation Studies
## Conclusion
## References
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 1, "held-out": 0, "held out": 0, "generaliz": 9, "multi-token": 0, "multi token": 0, "unseen": 0, "novel entit": 0, "counterfact": 7, "zsre": 3, "teacher forc": 0, "autoregressive": 3, "first token": 0, "subject": 11, "last token": 0, "embedding": 1, "vocabulary": 0}


## SECTION: Experiments



 



## SECTION: Models and Datasets



 
 To enable fair comparisons with prior work, we evaluate our method on three autoregressive language models commonly used in model-editing research: Llama-3-8B-Instruct ( Meta AI 2024 ) , GPT-J-6B ( Wang and Komatsuzaki 2021 ) , and GPT2-XL-1.5B ( Radford et al. 2019 ) . Following the standard configuration of locate-then-edit methods, all edits are applied to the FFN down-projection matrix at each layer within the layer window identified by causal tracing: 4–8 for Llama-3-8B-Instruct, 3–8 for GPT-J-6B, and 13–17 for GPT2-XL-1.5B ( Fang et al. 2025 ) .
All experiments are run on NVIDIA L40 GPUs. We conduct experiments on CounterFact ( Meng et al. 2022 ) and zsRE ( Levy et al. 2017 ) , two of the most influential benchmarks for model editing. 
 
 
 



## SECTION: Evaluation Metrics and Experiment Setup



 
 Efficacy, Generalization, and Specificity are the three core metrics for knowledge editing. They are measured on edit prompts, rephrased prompts, and neighborhood prompts, respectively, although their precise computation differ slightly between the two datasets. The main tables additionally report their harmonic mean as the overall Score. CounterFact further reports Fluency and Consistency. Fluency uses the n-gram entropy of generated text to detect repetitive degeneration, whereas Consistency measures the TF-IDF similarity between generated text and a reference passage describing the new fact, thereby assessing whether the edit is reflected in free-form generation. We follow the original AlphaEdit implementation for all metric calculations ( Fang et al. 2025 ) . Under the sequential editing protocol, we sample 2,000 requests from each dataset and apply them successively to the same model in 20 batches of 100 requests. Further details of the experimental setup are provided in Appendix A of the supplementary material. 
 
 
 
 
 
 MODEL 
 
 CounterFact 
 zsRE 
 
 Method 
 Score 
 Eff. 
 Gen. 
 Spe. 
 Flu. 
 Consis. 
 Score 
 Eff. 
 Gen. 
 Spe. 
 
 LLaMA3-8B 
 FT 
 62.24 62.24 
 83.33 83.33 
 67.79 67.79 
 46.63 46.63 
 233.72 233.72 
 8.770 8.770 
 23.00 23.00 
 30.48 30.48 
 30.22 30.22 
 15.49 15.49 
 
 ROME 
 57.65 57.65 
 64.40 64.40 
 61.42 61.42 
 49.44 49.44 
 449.06 449.06 
 3.31 3.31 
 1.20 1.20 
 2.01 2.01 
 1.80 1.80 
 0.69 0.69 
 
 MEMIT 
 59.89 59.89 
 65.65 65.65 
 64.65 64.65 
 51.56 51.56 
 437.43 437.43 
 6.58 6.58 
 26.10 26.10 
 34.62 34.62 
 31.28 31.28 
 18.49 18.49 
 
 AlphaEdit 
 84.61 84.61 
 98.90 98.90 
 94.22 94.22 
 67.88 67.88 
 622.49 622.49 
 32.40 32.40 
 57.38 57.38 
 94.47 94.47 
 91.13 91.13 
 32.55 32.55 
 
 BLUE 
 89.34 89.34 
 99.93 \bm{99.93} 
 97.25 \bm{97.25} 
 75.24 75.24 
 624.90 624.90 
 33.79 \bm{33.79} 
 57.00 57.00 
 95.77 95.77 
 91.73 91.73 
 31.96 31.96 
 
 FE* 
 84.95 84.95 
 98.35 98.35 
 94.92 94.92 
 68.43 68.43 
 - 
 - 
 56.58 56.58 
 92.96 92.96 
 88.81 88.81 
 32.25 32.25 
 
 DOW-KE 
 90.79 \bm{90.79} 
 99.85 99.85 
 96.64 96.64 
 78.86 \bm{78.86} 
 628.49 \bm{628.49} 
 31.63 31.63 
 60.26 \bm{60.26} 
 98.62 \bm{98.62} 
 96.76 \bm{96.76} 
 34.12 \bm{34.12} 
 
 GPT-J 
 FT 
 62.85 62.85 
 92.15 92.15 
 72.38 72.38 
 43.35 43.35 
 297.92 297.92 
 6.65 6.65 
 37.88 37.88 
 72.37 72.37 
 68.91 68.91 
 19.66 19.66 
 
 ROME 
 54.49 54.49 
 57.50 57.50 
 54.20 54.20 
 52.05 52.05 
 589.42 589.42 
 3.22 3.22 
 21.83 21.83 
 56.42 56.42 
 54.65 54.65 
 9.86 9.86 
 
 MEMIT 
 82.57 82.57 
 98.55 98.55 
 95.50 95.50 
 63.64 63.64 
 546.28 546.28 
 34.89 34.89 
 55.02 55.02 
 94.91 94.91 
 90.22 90.22 
 30.39 30.39 
 
 AlphaEdit 
 89.23 89.23 
 99.70 99.70 
 96.68 96.68 
 75.48 75.48 
 618.50 618.50 
 42.08 \bm{42.08} 
 53.78 53.78 
 99.79 99.79 
 96.00 96.00 
 28.29 28.29 
 
 BLUE 
 89.26 89.26 
 99.77 99.77 
 97.13 97.13 
 75.23 75.23 
 621.07 \bm{621.07} 
 41.34 41.34 
 54.21 54.21 
 99.63 99.63 
 95.96 95.96 
 28.67 28.67 
 
 FE* 
 80.70 80.70 
 97.4 97.4 
 88.45 88.45 
 64.1 64.1 
 - 
 - 
 52.66 52.66 
 98.62 98.62 
 90.81 90.81 
 27.92 27.92 
 
 DOW-KE 
 90.93 \bm{90.93} 
 99.90 \bm{99.90} 
 98.48 \bm{98.48} 
 77.96 \bm{77.96} 
 619.02 619.02 
 39.79 39.79 
 61.09 \bm{61.09} 
 99.81 \bm{99.81} 
 98.50 \bm{98.50} 
 34.56 \bm{34.56} 
 
 GPT2-XL 
 FT 
 52.67 52.67 
 63.55 63.55 
 42.20 42.20 
 57.06 57.06 
 519.35 519.35 
 10.56 10.56 
 19.54 19.54 
 37.11 37.11 
 33.30 33.30 
 10.36 10.36 
 
 ROME 
 52.78 52.78 
 54.60 54.60 
 51.18 51.18 
 52.68 52.68 
 366.13 366.13 
 0.72 0.72 
 26.30 26.30 
 47.50 47.50 
 43.56 43.56 
 14.27 14.27 
 
 MEMIT 
 77.44 77.44 
 94.70 94.70 
 85.82 85.82 
 60.50 60.50 
 477.26 477.26 
 22.72 22.72 
 46.53 46.53 
 79.17 79.17 
 71.44 71.44 
 26.42 26.42 
 
 AlphaEdit 
 83.90 83.90 
 99.50 99.50 
 93.95 93.95 
 66.39 66.39 
 597.88 597.88 
 39.38 39.38 
 49.34 49.34 
 94.81 94.81 
 86.11 86.11 
 25.88 25.88 
 
 BLUE 
 89.48 \bm{89.48} 
 99.40 99.40 
 96.00 96.00 
 76.63 \bm{76.63} 
 621.92 621.92 
 40.98 40.98 
 49.96 49.96 
 96.88 96.88 
 89.58 89.58 
 25.93 25.93 
 
 FE* 
 77.96 77.96 
 96.05 96.05 
 88.75 88.75 
 59.51 59.51 
 - 
 - 
 34.66 34.66 
 73.48 73.48 
 64.11 64.11 
 17.44 17.44 
 
 DOW-KE 
 87.66 87.66 
 99.75 \bm{99.75} 
 97.25 \bm{97.25} 
 71.86 71.86 
 625.93 \bm{625.93} 
 41.65 \bm{41.65} 
 54.44 \bm{54.44} 
 98.25 \bm{98.25} 
 95.27 \bm{95.27} 
 29.04 \bm{29.04} 
 
 
 Table 1: Comparison of DOW-KE with existing methods on the sequential model editing task. The best results are highlighted in bold, while the second-best results are underlined. Baseline results are taken from Fang et al. (2025) and Li et al. (2025) . For FE, no official results have been reported for the setting of 2,000 requests applied sequentially in 20 batches; the values in the table are from our own evaluation. Confidence intervals are reported in appendix of the supplementary material. 
 
 
 
 
 
 MODEL 
 CounterFact 
 
 Method 
 Eff. 
 Gen. 
 Spe. 
 
 
 
 LLaMA3-8B 
 Baseline 
 98.3 
 90.05 
 77.59 
 
 NLL-to-W.( α = 1.2 \alpha=1.2 ) 
 99.25 
 95.58 
 77.85 
 
 + In-Graph C. 
 99.85 
 95.62 
 80.24 
 
 
 + In-Graph C. + Routing 
 99.85 
 96.64 
 78.86 
 
 
 Table 2: Operating-point-matched ablation results. The scaling coefficient α \alpha controls the trade-off between editing performance and Specificity. Rows 1–2 compare Efficacy and Generalization at approximately matched Specificity, whereas Rows 2–3 compare Specificity at approximately matched editing performance. 
 
 
 



## SECTION: Comparative Experiments



 
 Table 1 reports DOW-KE’s evaluation results on three models and two datasets. All values are averaged over five runs; under the same experimental settings, we compare DOW-KE with other locate-then-edit methods and fine-tuning-based baselines ( Fang et al. 2025 ) . DOW-KE achieves the best result in most settings and the second-best result in the remaining settings. Compared with BLUE, it has a clear advantage in five of the six model–dataset combinations; in particular, it outperforms BLUE on every reported metric on zsRE. We also include FE as a comparison method, whose results are relatively weak under the multi-batch sequential-editing protocol. Thus, DOW-KE not only consistently improves on AlphaEdit but also outperforms, overall, methods that retain the anchor structure, including BLUE and FE. 
 
 
 



## SECTION: Ablation Studies



 
 Table 2 examines two key design choices of DOW-KE: removing the intermediate activation anchor and directly optimizing the weights, and incorporating the preservation-subspace constraint into the differentiable computation graph. We use AlphaEdit with the energy-threshold rule as the comparison baseline. Although this setting differs slightly from the original AlphaEdit, it uses the same thresholding rule as DOW-KE. Let α \alpha denote the weight-scaling coefficient, Δ ​ W = α ​ Δ ​ W grad \Delta W=\alpha\Delta W_{\mathrm{grad}} , with a default value of 1.
We treat α \alpha as an operating-point control along the trade-off between editing performance and Specificity. At matched Specificity (77.59 versus 77.85), NLL-to-W. with α = 1.2 \alpha=1.2 improves Efficacy and Generalization over the baseline, demonstrating the benefit of direct weight optimization. At comparable Efficacy and Generalization, adding the in-graph constraint with the default α = 1 \alpha=1 improves Specificity from 77.85 to 80.24. These matched comparisons support the complementary contributions of direct optimization and in-graph constraint parameterization.
Row 4 adds subject-conditioned gradient routing, which is designed to prevent the optimizer from directly shaping A l A^{l} through positions that precede and therefore do not fully encode the subject. Routing improves Generalization by 1.02 points while reducing Specificity by 1.38 points, resulting in a modest 0.31-point decrease in Score. We include it in the full configuration for its structural role in promoting fact-conditioned optimization, rather than as a score-maximizing component. 
 
 
 
 
 
 Threshold 
 Out. Proj. 
 CounterFact 
 
 Eff. 
 Gen. 
 Spe. 
 
 
 
 τ = 0.4 \tau=0.4 
 w. 
 99.94 
 97.45 
 71.59 
 
 w/o. 
 99.95 
 97.05 
 71.02 
 
 τ = 0.5 \tau=0.5 
 w. 
 99.93 
 97.12 
 76.98 
 
 w/o. 
 99.95 
 96.37 
 74.62 
 
 τ = 0.6 \tau=0.6 
 w. 
 99.85 
 95.62 
 80.24 
 
 w/o. 
 99.91 
 96.12 
 79.65 
 
 τ = 0.7 \tau=0.7 
 w. 
 99.86 
 94.74 
 84.63 
 
 w/o. 
 99.85 
 95.33 
 83.22 
 
 
 Table 3: Ablation results for the subspace threshold and output-side projection on LLaMA3-8B and CounterFact. Experiments are conducted without subject routing to isolate the effects of the subspace threshold and output-side projection. 
 
 
 Table  3 shows a threshold-controlled trade-off: increasing τ \tau improves Specificity but reduces Generalization. One possible explanation is that the enlarged preservation subspace leaves fewer editable directions, encouraging narrower fitting to the optimization prompts and weaker transfer to paraphrases. We leave direct verification of this mechanism to future work. Table 3 also compares performance with and without the output-side preservation constraint. Across all thresholds shown, adding output-side preservation improves Specificity and, in some settings, also improves Generalization. This suggests that output-side preservation provides a constraint complementary to key-side preservation, thereby strengthening the protection of unrelated knowledge. 
 
 
 
 

