# ResidualDistribution — arXiv 2502.03748

Source: https://arxiv.org/html/2502.03748

## Headings
# Rethinking Residual Distribution in Locate-then-Edit Model Editing
## 1 Introduction
## 2 Related Work
## 3 Background
### 3.1 Model Editing Problem
### 3.2 Locate-then-Edit Model Editing
## 4 Rethinking the Residual Distribution of Locate-then-Edit Model Editing
### 4.1 Analyzing Residual Distribution in Locate-then-Edit Model Editing
#### 4.1.1 How Does the Distributed Residual Contribute to the Editing Object?
#### 4.1.2 Is the Distributed Residual the Optimal Residual for Editing?
### 4.2 Theoretical Analysis of Residual Distribution in Locate-then-Edit Methods
### 4.3 BLUE: Boundary Layer UpdatE for Improving Locate-then-Edit Model Editing
## 5 Experiments
### 5.1 Experimental Setup
### 5.2 Enhancing Editing Performance with BLUE
### 5.3 Boosting General Capability Retention via BLUE
### 5.4 Mitigating Hidden States Shifts with BLUE
### 5.5 BLUE Boosts Long-Form Performance of Locate-Then-Edit Approaches
### 5.6 Ablation Study
## 6 Conclusion
## Acknowledgements
## References
## NeurIPS Paper Checklist
## Appendix A Proof of Theorem 4.1
## Appendix B BLUE’s Performance Improvement in Locate-then-Edit Model Editing Across LLMs
## Appendix C Supplementary Results of Post-edit LLM Performance
## Appendix D Experiment Details
## Appendix E Case Study on Long-form Model Editing Task
## Appendix F Batch Model Editing
## Appendix G Results on LLaMA-2-13B
## Appendix H Hidden States Shifts in GPT-J (6B) and GPT2-XL
## Appendix I Efficiency Analysis
## Appendix J Experimental validation of the theorem and lemma
### J.1 Experimental verification of Theorem 4.1
### J.2 Experimental verification of Lemma 4.3
## Appendix K BLUE in the Locate-then-edit Method with Square Root
Residual Distribution
## Appendix L Limitations
## Appendix M Impact Statements
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 4, "held-out": 0, "held out": 0, "generaliz": 18, "multi-token": 0, "unseen": 0, "novel entit": 0, "new entit": 0, "counterfact": 18, "zsre": 15, "teacher forc": 0, "autoregressive": 1, "subject": 14, "last token": 0, "embedding": 1, "vocabulary": 0, "propagat": 0}


## SECTION: 4.2 Theoretical Analysis of Residual Distribution in Locate-then-Edit Methods



 
 Theorem 4.1 . 
 
 In the locate-then-edit model editing, when using residual distribution, the upper bound for the weight shift error between the exact weight shift Δ l ∗ \Delta^{l^{*}} and the actual weight shift Δ l \Delta^{l} is given by 
 
 
 
 
 ‖ Δ l ∗ − Δ l ‖ 2 ≤ ( ‖ 𝑹 l ∗ − 𝑹 L ‖ 2 + ( L − l ) ​ ‖ 𝑹 L ‖ 2 ) ​ ‖ 𝑸 ‖ 2 , \displaystyle\|\Delta^{l^{*}}-\Delta^{l}\|_{2}\leq\left(\|{\bm{R}}^{l^{*}}-{\bm{R}}^{L}\|_{2}+(L-l)\|{\bm{R}}^{L}\|_{2}\right)\|{\bm{Q}}\|_{2}, 
 
 (11) 
 
 where 𝐑 l ∗ {\bm{R}}^{l^{*}} denotes the exact residual, and 𝐐 = 𝐊 1 l T ​ ( 𝐊 0 l ​ 𝐊 0 l T + 𝐊 1 l ​ 𝐊 1 l T ) − 1 {\bm{Q}}={{\bm{K}}_{1}^{l}}^{T}\left({\bm{K}}_{0}^{l}{{\bm{K}}_{0}^{l}}^{T}+{\bm{K}}_{1}^{l}{{\bm{K}}_{1}^{l}}^{T}\right)^{-1} . 
 
 
 
 The proof of the above theorem is presented in Appendix A . We also discuss the rationale for using the upper bound instead of the lower bound in Remark  4.2 . In Equ. ( 11 ), ‖ 𝑹 l ‖ 2 \|{\bm{R}}^{l}\|_{2} and ‖ 𝑸 ‖ 2 \|{\bm{Q}}\|_{2} increase with the number of new memories (i.e., the size of the editing batch [ 19 ] ). When the number of new memories is fixed, the upper bound increases with ‖ 𝑹 l ∗ − 𝑹 L ‖ 2 \|{\bm{R}}^{l^{*}}-{\bm{R}}^{L}\|_{2} and L − l L-l . L − l L-l increases as the residual distributes further, while it is unclear how ‖ 𝑹 l ∗ − 𝑹 L ‖ 2 \|{\bm{R}}^{l^{*}}-{\bm{R}}^{L}\|_{2} changes. To explore this, we assume the computed residual is the exact residual and analyze how ‖ 𝑹 l ∗ − 𝑹 L ‖ 2 \|{\bm{R}}^{l^{*}}-{\bm{R}}^{L}\|_{2} changes across layers. In Figure 5 , we show how ‖ 𝑹 l ∗ − 𝑹 L ‖ 2 \|{\bm{R}}^{l^{*}}-{\bm{R}}^{L}\|_{2} changes across layers. It shows that ‖ 𝑹 l ∗ − 𝑹 L ‖ 2 \|{\bm{R}}^{l^{*}}-{\bm{R}}^{L}\|_{2} increases as the residual distribution extends farther. Therefore, we can conclude that weight shift error increases with both the distance of residual distribution and the size of the editing batch . 
 
 
 Remark 4.2 . 
 
 The lower bound of the weight shift error can more effectively reflect the variation in error, but according to ‖ 𝐑 l ∗ ​ 𝐐 − 𝐑 l ​ 𝐐 ‖ 2 ≥ σ min ​ ( 𝐐 ) ​ ‖ 𝐑 l ∗ − 𝐑 l ‖ 2 ||\mathbf{R}^{l^{*}}\mathbf{Q}-\mathbf{R}^{l}\mathbf{Q}||_{2}\geq\sigma_{\min}(\mathbf{Q})||\mathbf{R}^{l^{*}}-\mathbf{R}^{l}||_{2} we see that the lower bound of the error shift is very small or even zero, where σ min ​ ( 𝐐 ) \sigma_{\min}(\mathbf{Q}) is the smallest singular value of 𝐐 \mathbf{Q} . This occurs because we cannot guarantee that 𝐐 \mathbf{Q} is nondegenerate. Even if 𝐐 \mathbf{Q} is nondegenerate, σ min ​ ( 𝐐 ) \sigma_{\min}(\mathbf{Q}) would still be very small, making the result insignificant. Additionally, although a growing upper bound does not necessarily imply an increase in error, our upper bound determines the worst-case scenario of the error, providing essential insight into selecting the layers to update. 
 
 
 
 Considering the closed-form solution of locate-then-edit model editing in sequential batch editing, the following lemma can be derived. 
 
 
 Lemma 4.3 . 
 
 In sequential batch editing, when using residual distribution, the upper bound of the weight shift error between the exact weight shift Δ l ∗ \Delta^{l^{*}} and the actual weight shift Δ l \Delta^{l} for locate-then-edit methods is given by 
 
 
 
 
 ‖ Δ l ∗ − Δ l ‖ 2 ≤ ( ‖ 𝑹 l ∗ − 𝑹 L ‖ 2 + ( L − l ) ​ ‖ 𝑹 l ‖ 2 ) ​ ‖ 𝑸 ′ ‖ 2 , \displaystyle\|\Delta^{l^{*}}-\Delta^{l}\|_{2}\leq\left(\|{\bm{R}}^{l^{*}}-{\bm{R}}^{L}\|_{2}+(L-l)\|{\bm{R}}^{l}\|_{2}\right)\|{\bm{Q}}^{\prime}\|_{2}, 
 
 (12) 
 
 where 𝐑 l ∗ {\bm{R}}^{l^{*}} denotes the exact residual, and 𝐐 ′ = 𝐊 1 l T ​ ( 𝐊 p l ​ 𝐊 p l T + 𝐊 0 l ​ 𝐊 0 l T + 𝐊 1 l ​ 𝐊 1 l T ) − 1 {\bm{Q}}^{\prime}={{\bm{K}}_{1}^{l}}^{T}\left({\bm{K}}_{p}^{l}{{\bm{K}}_{p}^{l}}^{T}+{\bm{K}}_{0}^{l}{{\bm{K}}_{0}^{l}}^{T}+{\bm{K}}_{1}^{l}{{\bm{K}}_{1}^{l}}^{T}\right)^{-1} . 
 
 
 
 ‖ 𝑲 p l ​ 𝑲 p l T ‖ 2 \|{\bm{K}}_{p}^{l}{{\bm{K}}_{p}^{l}}^{T}\|_{2} increases with the number of sequential edits, and thus Section 4.3 indicates that the weight shift error also increases with the number of sequential edits. 
 
 
 Figure 5: Variation of ‖ 𝑹 l ∗ − 𝑹 L ‖ 2 \|{\bm{R}}^{l^{*}}-{\bm{R}}^{L}\|_{2} across layers. 
 
 
 



## SECTION: 5 Experiments



 
 Table 2: Comparison of BLUE enhanced locate-then-model editing methods with original locate-then-model editing methods on the sequential model editing task. We color all results that are actually enhanced by BLUE in red. We directly adopt the baseline results from [ 5 ] to avoid the energy consumption caused by redundant computation. 
 
 
 
 
 Method 
 Model 
 Counterfact 
 ZsRE 
 
 
 
 Efficacy ↑ \uparrow 
 Generalization ↑ \uparrow 
 Specificity ↑ \uparrow 
 Fluency ↑ \uparrow 
 Consistency ↑ \uparrow 
 Efficacy ↑ \uparrow 
 Generalization ↑ \uparrow 
 Specificity ↑ \uparrow 
 
 Pre-edited 
 
 
 Llama3 
 
 7.85 ± \pm 0.26 
 10.58 ± \pm 0.26 
 89.48 ± \pm 0.18 
 635.23 ± \pm 0.11 
 24.14 ± \pm 0.08 
 36.99 ± \pm 0.30 
 36.34 ± \pm 0.30 
 31.89 ± \pm 0.22 
 
 MEMIT 
 65.65 ± \pm 0.47 
 64.65 ± \pm 0.42 
 51.56 ± \pm 0.38 
 437.43 ± \pm 1.67 
 6.58 ± \pm 0.11 
 34.62 ± \pm 0.36 
 31.28 ± \pm 0.34 
 18.49 ± \pm 0.19 
 
 PRUNE 
 68.25 ± \pm 0.46 
 64.75 ± \pm 0.41 
 49.82 ± \pm 0.36 
 418.03 ± \pm 1.52 
 5.90 ± \pm 0.10 
 24.77 ± \pm 0.27 
 23.87 ± \pm 0.27 
 20.69 ± \pm 0.23 
 
 RECT 
 66.05 ± \pm 0.47 
 63.62 ± \pm 0.43 
 61.41 ± \pm 0.37 
 526.62 ± \pm 0.44 
 20.54 ± \pm 0.09 
 86.05 ± \pm 0.23 
 80.54 ± \pm 0.27 
 31.67 ± \pm 0.22 
 
 AlphaEdit 
 98.90 ± \pm 0.10 
 94.22 ± \pm 0.19 
 67.88 ± \pm 0.29 
 622.49 ± \pm 0.16 
 32.40 ± \pm 0.11 
 94.47 ± \pm 0.13 
 91.13 ± \pm 0.19 
 32.55 ± \pm 0.22 
 
 MEMIT BLUE {}_{\text{BLUE}} 
 99.57 ± \pm 0.24 
 94.13 ± \pm 0.77 
 83.77 ± \pm 0.77 
 626.26 ± \pm 0.51 
 32.29 ± \pm 0.38 
 95.94 ± \pm 0.38 
 90.98 ± \pm 0.69 
 32.41 ± \pm 0.81 
 
 PRUNE BLUE {}_{\text{BLUE}} 
 96.73 ± \pm 0.64 
 89.68 ± \pm 0.85 
 57.79 ± \pm 1.14 
 627.39 ± \pm 0.37 
 33.39 ± \pm 0.36 
 86.55 ± \pm 0.86 
 82.22 ± \pm 1.00 
 31.04 ± \pm 0.80 
 
 RECT BLUE {}_{\text{BLUE}} 
 98.77 ± \pm 0.40 
 93.40 ± \pm 0.74 
 79.34 ± \pm 0.86 
 619.07 ± \pm 0.62 
 30.62 ± \pm 0.37 
 94.37 ± \pm 0.49 
 89.49 ± \pm 0.76 
 32.76 ± \pm 0.81 
 
 AlphaEdit BLUE {}_{\text{BLUE}} 
 99.93 ± \pm 0.09 
 97.25 ± \pm 0.48 
 75.24 ± \pm 0.98 
 624.90 ± \pm 0.49 
 33.79 ± \pm 0.38 
 95.77 ± \pm 0.39 
 91.73 ± \pm 0.65 
 31.96 ± \pm 0.80 
 
 Pre-edited 
 
 
 GPT-J 
 
 16.22 ± \pm 0.31 
 18.56 ± \pm 0.45 
 83.11 ± \pm 0.13 
 621.81 ± \pm 0.67 
 29.74 ± \pm 0.51 
 26.32 ± \pm 0.37 
 25.79 ± \pm 0.25 
 27.42 ± \pm 0.53 
 
 MEMIT 
 98.55 ± \pm 0.11 
 95.50 ± \pm 0.16 
 63.64 ± \pm 0.31 
 546.28 ± \pm 0.88 
 34.89 ± \pm 0.15 
 94.91 ± \pm 0.16 
 90.22 ± \pm 0.23 
 30.39 ± \pm 0.27 
 
 PRUNE 
 86.15 ± \pm 0.34 
 86.85 ± \pm 0.29 
 53.87 ± \pm 0.35 
 427.14 ± \pm 0.53 
 14.78 ± \pm 0.11 
 0.15 ± \pm 0.02 
 0.15 ± \pm 0.02 
 0.00 ± \pm 0.00 
 
 RECT 
 98.80 ± \pm 0.10 
 86.58 ± \pm 0.28 
 72.22 ± \pm 0.28 
 617.31 ± \pm 0.19 
 41.39 ± \pm 0.12 
 96.38 ± \pm 0.14 
 91.21 ± \pm 0.21 
 27.79 ± \pm 0.26 
 
 AlphaEdit 
 99.75 ± \pm 0.08 
 96.38 ± \pm 0.23 
 75.48 ± \pm 0.21 
 618.50 ± \pm 0.17 
 42.08 ± \pm 0.15 
 99.79 ± \pm 0.14 
 96.00 ± \pm 0.22 
 28.29 ± \pm 0.25 
 
 MEMIT BLUE {}_{\text{BLUE}} 
 99.70 ± \pm 0.30 
 96.90 ± \pm 0.50 
 74.61 ± \pm 0.95 
 620.89 ± \pm 0.73 
 40.82 ± \pm 0.44 
 99.58 ± \pm 0.18 
 94.77 ± \pm 0.67 
 28.36 ± \pm 0.94 
 
 PRUNE BLUE {}_{\text{BLUE}} 
 97.77 ± \pm 0.53 
 97.28 ± \pm 0.48 
 57.12 ± \pm 1.00 
 608.73 ± \pm 0.89 
 36.62 ± \pm 0.42 
 60.51 ± \pm 1.35 
 58.57 ± \pm 1.35 
 22.77 ± \pm 0.87 
 
 RECT BLUE {}_{\text{BLUE}} 
 98.70 ± \pm 0.41 
 91.18 ± \pm 0.84 
 74.78 ± \pm 0.94 
 620.52 ± \pm 0.65 
 39.79 ± \pm 0.43 
 97.93 ± \pm 0.38 
 93.86 ± \pm 0.69 
 26.32 ± \pm 0.91 
 
 AlphaEdit BLUE {}_{\text{BLUE}} 
 99.77 ± \pm 0.17 
 97.13 ± \pm 0.48 
 75.23 ± \pm 0.95 
 621.07 ± \pm 0.62 
 41.34 ± \pm 0.44 
 99.63 ± \pm 0.16 
 95.96 ± \pm 0.59 
 28.67 ± \pm 0.94 
 
 Pre-edited 
 
 
 GPT2-XL 
 
 22.23 ± \pm 0.73 
 24.34 ± \pm 0.62 
 78.53 ± \pm 0.33 
 626.64 ± \pm 0.31 
 31.88 ± \pm 0.20 
 22.19 ± \pm 0.24 
 31.30 ± \pm 0.27 
 24.15 ± \pm 0.32 
 
 MEMIT 
 94.70 ± \pm 0.22 
 85.82 ± \pm 0.28 
 60.50 ± \pm 0.32 
 477.26 ± \pm 0.54 
 22.72 ± \pm 0.15 
 79.17 ± \pm 0.32 
 71.44 ± \pm 0.36 
 26.42 ± \pm 0.25 
 
 PRUNE 
 82.05 ± \pm 0.38 
 78.55 ± \pm 0.34 
 53.02 ± \pm 0.35 
 530.47 ± \pm 0.39 
 15.93 ± \pm 0.11 
 21.62 ± \pm 0.30 
 19.27 ± \pm 0.28 
 13.19 ± \pm 0.18 
 
 RECT 
 92.15 ± \pm 0.26 
 81.15 ± \pm 0.33 
 65.13 ± \pm 0.31 
 480.83 ± \pm 0.62 
 21.05 ± \pm 0.16 
 81.02 ± \pm 0.31 
 73.08 ± \pm 0.35 
 24.85 ± \pm 0.25 
 
 AlphaEdit 
 99.50 ± \pm 0.24 
 93.95 ± \pm 0.34 
 66.39 ± \pm 0.31 
 597.88 ± \pm 0.18 
 39.38 ± \pm 0.15 
 94.81 ± \pm 0.30 
 86.11 ± \pm 0.29 
 25.88 ± \pm 0.21 
 
 MEMIT BLUE {}_{\text{BLUE}} 
 98.27 ± \pm 0.47 
 88.67 ± \pm 0.93 
 67.13 ± \pm 1.01 
 587.19 ± \pm 1.52 
 35.64 ± \pm 0.46 
 93.62 ± \pm 0.70 
 85.34 ± \pm 1.04 
 26.55 ± \pm 0.93 
 
 PRUNE BLUE {}_{\text{BLUE}} 
 88.19 ± \pm 1.12 
 80.48 ± \pm 1.10 
 52.23 ± \pm 1.05 
 594.08 ± \pm 1.18 
 20.28 ± \pm 0.44 
 47.94 ± \pm 1.33 
 45.03 ± \pm 1.32 
 16.72 ± \pm 0.75 
 
 RECT BLUE {}_{\text{BLUE}} 
 95.67 ± \pm 0.73 
 80.97 ± \pm 1.15 
 66.88 ± \pm 1.00 
 567.09 ± \pm 2.09 
 30.30 ± \pm 0.53 
 83.48 ± \pm 1.06 
 75.24 ± \pm 1.24 
 25.25 ± \pm 0.89 
 
 AlphaEdit BLUE {}_{\text{BLUE}} 
 99.40 ± \pm 0.28 
 96.00 ± \pm 0.60 
 76.63 ± \pm 0.93 
 621.92 ± \pm 0.56 
 40.98 ± \pm 0.43 
 96.88 ± \pm 0.50 
 89.58 ± \pm 0.91 
 25.93 ± \pm 0.92 
 
 
 
 
 
 In our experiments, we demonstrate that BLUE can enhance the performance of current locate-then-edit methods (Section 5.2 ), improve the retention of the original LLMs’ capabilities (Section 5.3 ), and alleviate the hidden state shifts introduced by locate-then-edit approaches (Section 5.4 ). Additionally, in Appendix 5.5 , we show that BLUE also boosts locate-then-edit methods in long-form model editing. In Appendix 5.6 , we present ablation studies demonstrating that selecting the first and last critical layers for editing in BLUE is the optimal choice. Appendix I illustrates the efficiency improvements introduced by BLUE. In Appendix J , we empirically validate Theorem 4.1 and Lemma 4.3 , demonstrating that the weight shift error increases with both the batch size and the number of sequential edits. Finally, we present the results of BLUE applied to the square root residual distribution method, PMET, in Appendix K . 
 
 



## SECTION: 5.1 Experimental Setup



 
 Datasets & LLMs. Our experiments are conducted on two datasets: CounterFact [ 18 ] and zsRE [ 13 ] . We select three LLMs as the editing subjects: GPT2-XL [ 23 ] , GPT-J (6B) [ 27 ] , Llama3 (8B) [ 1 ] . We also conduct experiments with Llama2 (13B) to further validate the effectiveness of BLUE in Appendix  G . 
 
 
 Baselines. BLUE is a facilitation strategy designed for locate-then-edit model editing that performs multi-layer updates, which has been proven in prior research to achieve the best editing performance [ 5 ] . Therefore, our baselines only consider locate-then-edit model editing methods. The locate-then-edit methods we consider are: MEMIT [ 19 ] , PRUNE [ 16 ] , RECT [ 8 ] , and AlphaEdit [ 5 ] . We present the experimental details in the Appendix D . 
 
 
 



## SECTION: 5.5 BLUE Boosts Long-Form Performance of Locate-Then-Edit Approaches



 
 We conduct long-form model editing experiments on editing Llama3 (8B) using UnKEBench [ 3 ] , a representative work in long-form evaluation benchmarks. We adopt MEMIT and AlphaEdit, both enhanced using the editing paradigm proposed in AnyEdit [ 12 ] , as baselines, and follow the same experimental setup as used in AnyEdit. As illustrated in Table. 3 , the results demonstrate that BLUE can also improve the performance of locate-then-edit methods in long-form evaluation scenarios . We also conduct a case study on a long-form editing task to demonstrate in detail the effectiveness of BLUE in Appendix  E . 
 
 
 Table 3: Comparison of Editing Methods on UnKEBench. The left side of ‘/’ represents the LLM’s edited output for original questions, while the right side represents the edited output for paraphrase questions. 
 
 
 
 
 Metric 
 BLEU 
 ROUGE-1 
 ROUGE-2 
 ROUGE-L 
 BERT Score 
 ROUGE-L (SubQ) 
 
 MEMIT 
 77.65 / 66.17 
 90.78 / 81.60 
 87.12 / 73.94 
 90.43 / 80.81 
 95.69 / 92.32 
 47.36 
 
 AlphaEdit 
 62.82 / 51.78 
 80.02 / 69.08 
 71.62 / 56.80 
 79.10 / 67.68 
 91.67 / 87.41 
 42.72 
 
 MEMIT BLUE 
 82.34 / 74.76 
 90.79 / 85.36 
 86.89 / 78.94 
 90.33 / 84.68 
 96.50 / 94.72 
 52.15 
 
 AlphaEdit BLUE 
 68.64 / 61.49 
 84.90 / 78.54 
 77.98 / 68.40 
 84.08 / 77.37 
 93.39 / 90.97 
 49.49 
 
 
 
 
 
 



## SECTION: 5.6 Ablation Study



 
 Figure 8: Layer Ablation of BLUE. 
 
 
 To verify that the first and last critical layers selected by BLUE are optimal for editing, we perform 30 sequential edits with a batch size of 100 on Llama3 (8B). As shown in Figure 8 , the optimal editing layers for all four BLUE-enhanced methods are consistently layers 4 and 8—the ones selected by BLUE. This provides empirical evidence that the layers chosen by BLUE are indeed optimal for model editing. 
 
 
 
 



## SECTION: Appendix C Supplementary Results of Post-edit LLM Performance



 
 We show the supplementary results of post-edit LLM performance in Figure 9 . The results also indicate that distributed residuals introduce significant information loss during model editing, leading to a higher likelihood of editing failures. 
 
 
 



## SECTION: Appendix D Experiment Details



 
 All our experiments are conducted on A800 GPUs. The baseline methods used for comparison in the experiments are kept in their original settings, with PRUNE following the reproduction settings of [ 5 ] . For baseline methods enhanced by BLUE, all configurations remain consistent with the original baselines, except for AlphaEdit BLUE {}_{\text{BLUE}} . For AlphaEdit BLUE {}_{\text{BLUE}} , we set the α \alpha values for Llama3 (8B), GPT-J (6B), and GPT2-XL to 1, 95, and 80, respectively, to ensure the invertibility of matrices during the editing process, thereby achieving better editing performance. For a clearer understanding of the baselines, please refer to [ 5 ] . 
 
 
 



## SECTION: Appendix G Results on LLaMA-2-13B



 
 To demonstrate the effectiveness of BLUE on larger models, we selecte AlphaEdit and MEMIT to perform sequential editing experiments on layers 30–34 of LLaMA-2-13B, following the same setup as in the main experiments. The results are shown in Table  7 . The results demonstrate that the BLUE-enhanced methods achieve better overall editing performance than the baseline methods on both the CounterFact and ZsRE datasets. We bolded all the enhanced results. On the CounterFact dataset, all metrics except for Specificity show improvements over the baseline. On the ZsRE dataset, all metrics of AlphaEdit show improvements, while MEMIT exhibits improvements in all metrics except for Specificity. This indicates that BLUE is also effective on LLaMA-2-13B, further validating the effectiveness of our approach. 
 
 
 Table 7: Comparison of different editing methods on CounterFact and ZsRE datasets when editing LLaMA-2-13B. 
 
 
 
 
 Method 
 CounterFact Dataset 
 ZsRE Dataset 
 
 Efficacy 
 Generalization 
 Specificity 
 Fluency 
 Consistency 
 Efficacy 
 Generalization 
 Specificity 
 
 
 
 AlphaEdit 
 52.30 ±2.19 
 48.95 ±1.73 
 50.53 ±2.21 
 408.92 ±2.36 
 0.22 ±0.01 
 52.31 ±1.44 
 37.68 ±1.49 
 9.11 ±0.60 
 
 AlphaEdit BLUE {}_{\text{BLUE}} 
 78.75 ±1.79 
 69.53 ±1.81 
 44.27 ±1.76 
 513.49 ±3.09 
 22.10 ±0.57 
 53.01 ±2.32 
 41.32 ±1.52 
 9.18 ±0.60 
 
 MEMIT 
 79.20 ±1.77 
 65.94 ±1.79 
 41.53 ±1.75 
 378.10 ±4.01 
 14.44 ±0.59 
 50.11 ±1.46 
 34.70 ±1.47 
 9.71 ±0.61 
 
 MEMIT BLUE {}_{\text{BLUE}} 
 79.60 ±1.78 
 66.00 ±1.81 
 41.28 ±1.65 
 384.23 ±3.50 
 14.65 ±0.59 
 51.07 ±1.45 
 37.13 ±1.52 
 9.07 ±0.60 
 
 
 
 
 
 



## SECTION: Appendix I Efficiency Analysis



 
 Table 8: Peak memory usage of both BLUE and locate-then-edit 
 
 
 
 Method 
 CounterFact 
 ZsRE 
 
 Llama-3 
 GPT-J 
 GPT-2XL 
 Llama-3 
 GPT-J 
 GPT-2XL 
 
 
 
 AlphaEdit 
 36.09 
 30.43 
 7.14 
 36.09 
 30.43 
 7.43 
 
 AlphaEdit BLUE 
 35.10 
 28.92 
 7.24 
 35.43 
 28.92 
 7.49 
 
 MEMIT 
 37.07 
 31.68 
 7.34 
 37.07 
 31.68 
 7.34 
 
 MEMIT BLUE 
 36.42 
 30.67 
 7.30 
 36.42 
 30.67 
 7.38 
 
 RECT 
 37.07 
 31.68 
 7.34 
 37.07 
 31.68 
 7.34 
 
 RECT BLUE 
 36.42 
 30.67 
 7.22 
 36.42 
 30.67 
 7.37 
 
 PRUNE 
 38.17 
 33.18 
 7.53 
 38.17 
 33.18 
 7.53 
 
 PRUNE BLUE 
 36.85 
 30.67 
 7.30 
 36.85 
 30.67 
 7.46 
 
 
 
 
 To evaluate the time and peak memory required for a single edit, we perform 300 sequential edits with a batch size of 1 and record the editing time and peak memory for each edit. The average peak memory consumption and editing time per instance for each method are reported in Table  8 and Figure  12 . In terms of peak memory, BLUE achieves higher memory efficiency than the original methods. This is intuitive: by discarding residual distributions and instead computing residuals only for the first and last key layers, BLUE reduces the memory overhead associated with residual distribution. Regarding editing time, with the exception of PRUNE BLUE on Llama-3 (8B)—which incurs a slightly higher editing time than its original counterpart—BLUE-enhanced methods consistently achieve lower average editing times across different models and datasets. These findings demonstrate that BLUE not only improves the editing performance of locate-then-edit methods, but also enhances their editing efficiency. 
 
 
 



## SECTION: Appendix J Experimental validation of the theorem and lemma



 
 In this section, we experimentally validate the correctness of the theorem and lemma presented in Section 4.2 . In this section, we choose llama3 (8B) as the target model for editing, and use MEMIT and AlphaEdit as the editing methods. 
 
 



## SECTION: J.1 Experimental verification of Theorem 4.1



 
 
 
 
 (a) CounterFact 
 
 
 (b) ZsRE 
 
 Figure 13: Performance Variation of Model Editing with Batch Edits on CounterFact and ZsRE Datasets 
 
 
 According to Theorem 4.1 , the weight shift error increases with the batch editing size. To verify this, we conduct batch editing experiments with 500, 1000, 5000, and 10000 edits on the CounterFact and ZsRE datasets. The results are shown in Figure 13 . It can be clearly observed that on both datasets, the overall performance gap between BLUE-enhanced methods and non-enhanced methods increases with the batch size, especially in terms of efficacy and generalization. Although not all metrics show a strictly increasing performance gap with larger batch sizes—for example, on the Consistency metric of the CounterFact dataset, the performance gap for 5000 batch edits is greater than that for 10000 edits—the overall trend still empirically supports the correctness of Theorem 4.1 . 
 
 
 



## SECTION: J.2 Experimental verification of Lemma 4.3



 
 
 
 
 (a) CounterFact 
 
 
 (b) ZsRE 
 
 Figure 14: Performance Variation of Model Editing with Sequential Edits on CounterFact and ZsRE Datasets 
 
 
 According to Lemma 4.3 , the weight shift error increases with the number of sequential edits. To verify this, we conduct sequential editing experiments with a batch size of 1, using 100, 500, 1000, and 5000 edits. As shown in Figure 14 , similar to the batch editing results, the overall trend on both datasets shows that the performance gap between the BLUE-enhanced methods and the original methods increases with the number of sequential edits. For instance, on the CounterFact dataset, the performance gap in efficacy and generalization between AlphaEdit and AlphaEdit BLUE {}_{\text{BLUE}} increases significantly when the number of edits reaches 5000. Although specificity and consistency do not exhibit this trend, the patterns observed in efficacy and generalization still support the conclusion that weight shift error increases with the number of sequential edits, as efficacy and generalization directly reflect the impact of the editing methods. 
 
 
 
 



## SECTION: Appendix K BLUE in the Locate-then-edit Method with Square Root
Residual Distribution



 
 Some locate-then-edit methods (e.g., PMET [ 15 ] ) use a square root residual distribution instead of an even spread. They claim that the square root residual distribution can mitigate information loss during residual distribution. Since BLUE is designed for locate-then-edit methods with even residual distribution, we do not consider such methods as baselines. Nevertheless, we attempt to enhance PMET with BLUE. The results of sequential batch editing are shown in Table 9 . PMET BLUE {}_{\text{BLUE}} exhibits a significant performance improvement when editing Llama3 on sequential model editing task, while its performance gains in other scenarios are relatively limited. We speculate that this may be because PMET’s use of square root distribution retains more editing information compared to even distribution, leading to the limited improvement of BLUE. Additionally, PMET incorporates a self-attention module during editing optimization but only edits the FFN weights when updating model parameters. This might result in BLUE’s two-layer update being insufficient to fully integrate the editing information into the model weights. Nevertheless, BLUE demonstrates notable improvements in the locate-then-edit approaches with residual even distribution, indicating that it remains applicable to most locate-then-edit methods. 
 
 
 Table 9: Comparison of PMET BLUE {}_{\text{BLUE}} with original PMET on the sequential batch and batch model editing task. We color all results that are actually enhanced by BLUE in red. 
 
 
 
 
 Method 
 Model 
 Counterfact 
 ZsRE 
 
 
 
 
 
 Efficacy ↑ \uparrow 
 Generalization ↑ \uparrow 
 Specificity ↑ \uparrow 
 Fluency ↑ \uparrow 
 Consistency ↑ \uparrow 
 Efficacy ↑ \uparrow 
 Generalization ↑ \uparrow 
 Specificity ↑ \uparrow 
 
 Sequential Model Editing Task 
 
 Pre-edited 
 
 
 Llama3 
 
 7.85 ± \pm 0.26 
 10.58 ± \pm 0.26 
 89.48 ± \pm 0.18 
 635.23 ± \pm 0.11 
 24.14 ± \pm 0.08 
 36.99 ± \pm 0.30 
 36.34 ± \pm 0.30 
 31.89 ± \pm 0.22 
 
 PMET 
 99.47 ± \pm 0.26 
 90.78 ± \pm 0.84 
 76.07 ± \pm 0.92 
 619.62 ± \pm 0.66 
 32.45 ± \pm 0.41 
 94.97 ± \pm 0.45 
 89.98 ± \pm 0.75 
 32.95 ± \pm 0.81 
 
 PMET BLUE {}_{\text{BLUE}} 
 99.57 ± \pm 0.24 
 94.13 ± \pm 0.69 
 83.77 ± \pm 0.77 
 626.26 ± \pm 0.51 
 32.29 ± \pm 0.38 
 96.07 ± \pm 0.36 
 91.73 ± \pm 0.66 
 32.66 ± \pm 0.81 
 
 Pre-edited 
 
 
 GPT-J 
 
 16.22 ± \pm 0.31 
 18.56 ± \pm 0.45 
 83.11 ± \pm 0.13 
 621.81 ± \pm 0.67 
 29.74 ± \pm 0.51 
 26.32 ± \pm 0.37 
 25.79 ± \pm 0.25 
 27.42 ± \pm 0.53 
 
 PMET 
 99.73 ± \pm 0.18 
 93.93 ± \pm 0.70 
 72.32 ± \pm 0.96 
 618.82 ± \pm 0.62 
 41.77 ± \pm 0.45 
 99.07 ± \pm 0.26 
 96.10 ± \pm 0.56 
 28.79 ± \pm 0.93 
 
 PMET BLUE {}_{\text{BLUE}} 
 99.57 ± \pm 0.24 
 92.82 ± \pm 0.76 
 77.61 ± \pm 0.92 
 620.02 ± \pm 0.59 
 39.19 ± \pm 0.43 
 99.16 ± \pm 0.25 
 87.37 ± \pm 1.01 
 28.13 ± \pm 0.93 
 
 Pre-edited 
 
 
 GPT2-XL 
 
 22.23 ± \pm 0.73 
 24.34 ± \pm 0.62 
 78.53 ± \pm 0.33 
 626.64 ± \pm 0.31 
 31.88 ± \pm 0.20 
 22.19 ± \pm 0.24 
 31.30 ± \pm 0.27 
 24.15 ± \pm 0.32 
 
 PMET 
 95.80 ± \pm 0.72 
 87.27 ± \pm 1.00 
 62.66 ± \pm 1.06 
 542.47 ± \pm 2.49 
 31.56 ± \pm 0.54 
 93.22 ± \pm 0.69 
 87.06 ± \pm 0.96 
 25.58 ± \pm 0.91 
 
 PMET BLUE {}_{\text{BLUE}} 
 95.30 ± \pm 0.76 
 85.57 ± \pm 1.08 
 67.93 ± \pm 0.99 
 603.03 ± \pm 1.37 
 37.20 ± \pm 0.42 
 89.32 ± \pm 0.91 
 80.53 ± \pm 1.19 
 26.74 ± \pm 0.92 
 
 Batch Model Editing Task 
 
 Pre-edited 
 
 
 Llama3 
 
 7.02 ± \pm 0.50 
 9.44 ± \pm 0.49 
 89.73 ± \pm 0.36 
 630.00 ± \pm 0.22 
 24.21 ± \pm 0.17 
 35.67 ± \pm 0.58 
 34.81 ± \pm 0.58 
 31.83 ± \pm 0.44 
 
 PMET 
 97.02 ± \pm 0.33 
 86.22 ± \pm 0.58 
 77.72 ± \pm 0.48 
 624.68 ± \pm 0.28 
 31.84 ± \pm 0.21 
 83.49 ± \pm 0.53 
 80.73 ± \pm 0.56 
 31.94 ± \pm 0.43 
 
 PMET BLUE {}_{\text{BLUE}} 
 93.64 ± \pm 0.48 
 81.52 ± \pm 0.67 
 84.63 ± \pm 0.40 
 627.81 ± \pm 0.24 
 30.62 ± \pm 0.20 
 85.92 ± \pm 0.50 
 82.83 ± \pm 0.54 
 32.23 ± \pm 0.44 
 
 Pre-edited 
 
 
 GPT-J 
 
 15.20 ± \pm 0.70 
 17.70 ± \pm 0.60 
 83.50 ± \pm 0.50 
 622.40 ± \pm 0.30 
 29.40 ± \pm 0.20 
 26.40 ± \pm 0.60 
 25.80 ± \pm 0.50 
 27.00 ± \pm 0.50 
 
 PMET 
 99.57 ± \pm 0.13 
 92.48 ± \pm 0.44 
 71.41 ± \pm 0.52 
 620.31 ± \pm 0.31 
 40.79 ± \pm 0.24 
 89.24 ± \pm 0.46 
 82.69 ± \pm 0.59 
 25.51 ± \pm 0.49 
 
 PMET BLUE {}_{\text{BLUE}} 
 97.65 ± \pm 0.59 
 87.24 ± \pm 1.13 
 73.32 ± \pm 1.06 
 616.85 ± \pm 0.65 
 38.14 ± \pm 0.46 
 80.77 ± \pm 1.24 
 67.58 ± \pm 1.45 
 28.00 ± \pm 1.01 
 
 Pre-edited 
 
 
 GPT2-XL 
 
 21.82 ± \pm 0.81 
 24.16 ± \pm 0.72 
 78.32 ± \pm 0.55 
 626.78 ± \pm 0.23 
 31.37 ± \pm 0.20 
 22.17 ± \pm 0.52 
 21.28 ± \pm 0.51 
 24.20 ± \pm 0.48 
 
 PMET 
 81.14 ± \pm 0.77 
 70.45 ± \pm 0.79 
 66.42 ± \pm 0.56 
 622.16 ± \pm 0.32 
 37.09 ± \pm 0.22 
 60.25 ± \pm 0.78 
 56.29 ± \pm 0.78 
 23.95 ± \pm 0.49 
 
 PMET BLUE {}_{\text{BLUE}} 
 67.09 ± \pm 0.92 
 54.48 ± \pm 0.87 
 73.48 ± \pm 0.54 
 626.67 ± \pm 0.25 
 35.05 ± \pm 0.21 
 57.15 ± \pm 0.77 
 51.99 ± \pm 0.77 
 25.01 ± \pm 0.48 
 
 
 
 
 
 

