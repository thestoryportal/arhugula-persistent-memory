# OrthoRepEditing — arXiv 2606.22627

Source: https://arxiv.org/html/2606.22627

## Headings
# Orthogonal Representation Editing: Decoupling Semantic Entanglement 
 in Batch Knowledge Editing of LLMs
## 1 Introduction
## 2 Observation of General Semantic Representation Entanglement
### 2.1 Data Settings
### 2.2 Observations
## 3 Methodology
### 3.1 Overview of ORE
### 3.2 Representation Subspace Orthogonalization
#### 3.2.1 Construction of General Semantic Subspace
#### 3.2.2 Orthogonal Constraint on Edit Vectors
### 3.3 Non-linear Gated Representation Fine-tuning
#### 3.3.1 Non-linear Bottleneck Structure
#### 3.3.2 Dynamic Gating Mechanism
### 3.4 Loss Functions
## 4 Experiments
### 4.1 Experiment Settings
### 4.2 Performance Analysis
### 4.3 Analysis of Anti-Interference Capability
### 4.4 Ablation Study
### 4.5 Cross-Lingual Editing Scenarios
## 5 Related Work
## 6 Conclusion
## Limitations
## 7 Acknowledgments
## References
## Appendix A Datasets
## Appendix B Metrics
## Appendix C Implementation Details
## Appendix D Baselines
## Appendix E Experimental Results on Sequential Editing
## Appendix F Impact of Batch Editing Scale on Editing Performance
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 4, "held-out": 0, "held out": 0, "generaliz": 3, "multi-token": 0, "unseen": 0, "novel entit": 0, "new entit": 0, "counterfact": 14, "zsre": 27, "teacher forc": 0, "autoregressive": 0, "subject": 5, "last token": 1, "embedding": 0, "vocabulary": 0, "propagat": 1}


## SECTION: 3 Methodology



 
 Figure 3: Overview of the proposed ORE framework. It edits a frozen LLM by applying gated, non-linear representation interventions at selected layers, orthogonalizing edit vectors against a general semantic subspace, and updating hidden states with the resulting orthogonalized edits. 
 
 



## SECTION: 4 Experiments



 



## SECTION: 4.1 Experiment Settings



 
 Datasets. 
We evaluate ORE on three widely used knowledge editing benchmarks: ZsRE Levy et al. (2017) , CounterFact Meng et al. (2022) , and Bi-ZsRE Wang et al. (2024a) . ZsRE is a fact-based question-answering dataset commonly used to assess precise factual updates.
CounterFact is a large-scale and challenging benchmark for counterfactual knowledge editing, featuring diverse relations, entities, paraphrased prompts, and semantically related but factually independent neighborhood samples. Bi-ZsRE is a cross-lingual extension of ZsRE with parallel Chinese–English question-answer pairs, which we use to evaluate ORE in cross-lingual editing scenarios. 
 
 
 Implementation Details and Metrics. All experiments are conducted on LLaMA-3-8B and Qwen-2.5-7B models. Please refer to the Appendix C for hyperparameters and more implementation details.
Following prior works Meng et al. (2023) ; Fang et al. (2025) , we evaluate models using three standard metrics: Efficacy , Generality , and Specificity . Efficacy measures whether the edited fact is correctly produced for the original prompt; Generality evaluates the robustness of the edited knowledge under paraphrased prompts; and Specificity assesses whether the editing operation avoids affecting factually unrelated knowledge. 
 
 
 
 
 
 
 
 Model 
 Method 
 ZsRE 
 CounterFact 
 
 Eff. ↑ \uparrow 
 Gen. ↑ \uparrow 
 Spe. ↑ \uparrow 
 Avg. ↑ \uparrow 
 Eff. ↑ \uparrow 
 Gen. ↑ \uparrow 
 Spe. ↑ \uparrow 
 Avg. ↑ \uparrow 
 
 
 
 LLaMA-3-8B 
 
 FT 
 37.20 
 36.52 
 39.94 
 37.89 
 98.95 
 91.94 
 38.73 
 76.54 
 
 ROME 
 41.45 
 39.35 
 30.64 
 37.15 
 8.32 
 10.47 
 88.25 
 35.68 
 
 MEMIT 
 87.46 
 84.12 
 31.67 
 67.75 
 96.4 
 76.77 
 86.57 
 86.58 
 
 PRUNE 
 41.73 
 39.50 
 20.94 
 34.06 
 95.29 
 87.75 
 67.48 
 83.51 
 
 RECT 
 68.08 
 64.50 
 30.91 
 54.50 
 67.18 
 45.69 
 88.91 
 67.26 
 
 NSE 
 45.21 
 44.47 
 30.58 
 40.09 
 85.22 
 52.33 
 87.49 
 75.01 
 
 AlphaEdit 
 86.35 
 82.73 
 31.10 
 66.73 
 94.07 
 75.15 
 84.69 
 84.64 
 
 ReFT 
 44.57 
 43.38 
 21.28 
 36.41 
 80.86 
 55.37 
 40.83 
 59.02 
 
 ORE (Ours) 
 93.24 
 88.22 
 29.35 
 70.27 
 97.78 
 96.81 
 76.63 
 90.41 
 
 
 
 Qwen2.5-7B 
 
 FT 
 33.30 
 31.26 
 26.72 
 30.43 
 99.98 
 75.60 
 38.83 
 71.47 
 
 ROME 
 35.41 
 34.44 
 38.29 
 36.05 
 12.72 
 15.31 
 85.98 
 38.00 
 
 MEMIT 
 94.52 
 90.29 
 38.36 
 74.39 
 99.42 
 92.39 
 81.20 
 91.00 
 
 PRUNE 
 69.10 
 65.92 
 42.00 
 59.01 
 98.36 
 96.87 
 64.57 
 86.60 
 
 RECT 
 91.01 
 83.99 
 40.71 
 71.90 
 97.72 
 80.04 
 83.33 
 87.03 
 
 NSE 
 49.15 
 48.32 
 40.73 
 46.07 
 56.72 
 50.14 
 84.01 
 63.62 
 
 AlphaEdit 
 95.23 
 87.75 
 38.97 
 73.98 
 99.76 
 94.73 
 79.16 
 91.22 
 
 ReFT 
 49.95 
 47.51 
 35.30 
 44.25 
 77.30 
 51.99 
 44.91 
 58.07 
 
 ORE (Ours) 
 99.83 
 93.85 
 30.64 
 74.77 
 99.10 
 93.56 
 83.64 
 92.10 
 
 
 
 Table 2: Comparison of 5000 edits on ZsRE and CounterFact. 
 
 
 Baselines. 
We compare ORE with the following baselines. FT Zhu et al. (2020) directly fine-tunes selected model parameters on edit samples using cross-entropy loss. ROME Meng et al. (2022) identifies knowledge-bearing neurons via causal tracing and injects rank-one updates into MLP layers, while MEMIT Meng et al. (2023) extends ROME to support batch editing by distributing update residuals across multiple layers. PRUNE Ma et al. (2025) constrains parameter perturbations by limiting the condition number of the edit matrix to reduce interference during sequential edits, and RECT Gu et al. (2024) improves robustness through consistency regularization to prevent overfitting. AlphaEdit Fang et al. (2025) applies null-space projection to inject updates while preserving existing knowledge.
 NSE Jiang et al. (2025b) edits models by selectively updating activation-critical neurons based on target hidden states computed from frozen parameters.
 ReFT Wu et al. (2024) learns lightweight intervention functions that manipulate hidden representations in low-rank subspaces of a frozen model at inference time. 
 
 
 



## SECTION: 4.2 Performance Analysis



 
 Tables  1 and  2 report comparisons between ORE and representative knowledge editing methods on ZsRE and CounterFact. From the results, we observe that:
(1) Across datasets and model backbones, ORE consistently achieves the competitive performance in terms of editing success and generalization, demonstrating its effectiveness in large-scale batch editing settings. This advantage mainly stems from alleviating general semantic entanglement, which encourages editing directions to focus on semantic dimensions directly relevant to the target facts. ORE is comparatively less dominant in specificity, as its edits are regulated by soft constraints imposed in the representation space rather than hard parameter-level isolation, making it inherently weaker than parameter-editing methods in preserving unrelated knowledge.
(2) Compared with conventional representation fine-tuning, ORE exhibits improved stability and overall performance, validating the effectiveness of subspace orthogonalization combined with the non-linear bottleneck and dynamic gating design.
For completeness, we also report experimental results on sequential knowledge editing in Appendix E . 
 
 
 



## SECTION: 4.3 Analysis of Anti-Interference Capability



 
 To validate ORE’s ability to eliminate common semantic entanglement from a geometric perspective, we conducted experiments on the shared structure dataset "The capital of [Country] is [City]" constructed in Section 2 . Beyond standard Efficacy, we measured the cosine similarity between each method’s edit vectors and the common semantic subspace S g ​ s S_{gs} , where higher similarity indicates greater interference from shared semantics.
As shown in Figure  4 , MEMIT’s post-edit vectors remain highly aligned with S g ​ s S_{gs} , suggesting that its updates fail to avoid shared semantic regions. In contrast, ORE, via representation orthogonal projection, achieves 92% Efficacy while reducing cosine similarity to only one-sixth of MEMIT’s, demonstrating its effectiveness in mitigating representation entanglement and enhancing anti-interference capability in batch editing. 
 
 
 



## SECTION: 4.4 Ablation Study



 
 
 
 
 
 
 Method 
 Eff. ↑ \uparrow 
 Gen. ↑ \uparrow 
 Spe. ↑ \uparrow 
 Avg. ↑ \uparrow 
 
 
 
 ORE 
 95.54 
 92.18 
 29.03 
 72.25 
 
 - ℒ o ​ r ​ t ​ h \mathcal{L}_{orth} 
 93.34 
 88.77 
 29.18 
 70.43 
 
 -SiLU 
 93.00 
 90.52 
 27.46 
 70.33 
 
 -Gate 
 95.13 
 85.78 
 28.64 
 69.85 
 
 
 
 Table 3: Ablation study of ORE with 1,000 edits on ZsRE. 
 
 
 We conduct an ablation study on ZsRE under a batch editing setting with 1,000 samples to evaluate the contributions of ORE’s key components. As shown in Table  3 , removing the representation orthogonalization loss (- ℒ o ​ r ​ t ​ h \mathcal{L}_{orth} ) decreases both efficacy and generality, indicating that orthogonalization is crucial for decoupling shared semantic patterns and mitigating cumulative interference. Eliminating the non-linear activation in the gated representation head (-SiLU) leads to a drop in overall performance. Disabling the dynamic gating mechanism (-Gate) reduces generality and specificity, highlighting the importance of adaptive gating for accurately localizing knowledge-carrying positions while avoiding unnecessary perturbations in irrelevant regions.
Figure  5 further shows the cosine similarity between edit vectors and the general semantic subspace after removing the representation orthogonalization, illustrating that the orthogonal constraint effectively decouples the edited facts from shared semantic patterns. 
 
 
 Figure 4: Cosine similarity between edit representations and the general semantic subspace across sequential edits. MEMIT (blue) consistently shows higher similarity, indicating stronger entanglement with shared semantics, while ORE (orange) maintains substantially lower similarity throughout the editing process. 
 
 
 



## SECTION: Appendix A Datasets



 
 To comprehensively evaluate the performance of ORE, we conducted experiments on three widely used knowledge editing benchmark datasets: 
 
 
 ZsRE: A standard fact-based dataset in question-answering format. Each sample contains a natural language question and its corresponding target answer Levy et al. (2017) . 
 
 
 CounterFact: A large-scale and highly challenging benchmark for counterfactual knowledge editing. This dataset covers diverse relation types and entities, and equips each editing target with semantically equivalent paraphrase prompts as well as semantically related but factually independent neighborhood samples Meng et al. (2022) . 
 
 
 Bi-ZsRE: A cross-lingual extension of ZsRE, containing parallel Chinese-English question-answer pairs. Given that ORE aims to address the problem of general concept entanglement, we introduce this dataset to specifically evaluate the model’s performance in cross-lingual scenarios, examining whether it can effectively strip away linguistic noise and achieve precise cross-lingual knowledge synchronization within the semantic space shared by multilingual models Wang et al. (2024a) . 
 
 
 We follow the experimental settings of Fang et al. (2025) for ZsRE and CounterFact, and those of Sun et al. (2025) for Bi-ZsRE. 
 
 
 



## SECTION: Appendix B Metrics



 
 Following the standards of previous knowledge editing works Meng et al. (2022) ; Meng et al. (2023) ; Fang et al. (2025) ; Sun et al. (2025) , Let the given edit sample be denoted as ( s i , r i , o i ∗ ) (s_{i},r_{i},o^{*}_{i}) , the prompt as ( s i , r i ) (s_{i},r_{i}) , the paraphrase prompts as N ⁡ ( s i , r i ) N(s_{i},r_{i}) , and the neighborhood prompts as O ⁡ ( s i , r i ) O(s_{i},r_{i}) . The metrics are defined as follows: 
 
 
 Efficacy: Measures whether the target knowledge has been successfully injected into the model. 
 
 
 

 
 
 𝔼 i { o i = arg max o ℙ f ( o ∣ ( s i , r i ) ) } \mathbb{E}_{i}\left\{o_{i}=\arg\max_{o}\mathbb{P}_{f}(o\mid(s_{i},r_{i}))\right\} 
 
 (11) 
 
 
 
 Generality: Measures the robustness of the edited knowledge to semantic variations. 
 
 
 

 
 
 𝔼 i { o i = arg max o ℙ f ( o ∣ N ( ( s i , r i ) ) ) } \mathbb{E}_{i}\left\{o_{i}=\arg\max_{o}\mathbb{P}_{f}(o\mid N((s_{i},r_{i})))\right\} 
 
 (12) 
 
 
 
 Specificity: Measures the locality of the editing operation, evaluating whether the model avoids corrupting irrelevant knowledge. 
 
 
 

 
 
 𝔼 i { o i c = arg max o ℙ f ( o ∣ O ( ( s i , r i ) ) ) } \mathbb{E}_{i}\left\{o_{i}^{c}=\arg\max_{o}\mathbb{P}_{f}(o\mid O((s_{i},r_{i})))\right\} 
 
 (13) 
 
 
 
 



## SECTION: Appendix E Experimental Results on Sequential Editing



 
 
 
 
 
 
 Method 
 Eff. ↑ \uparrow 
 Gen. ↑ \uparrow 
 Spe. ↑ \uparrow 
 Avg. ↑ \uparrow 
 
 FT 
 30.48 
 30.22 
 15.49 
 25.40 
 
 ROME 
 2.01 
 1.80 
 0.69 
 1.50 
 
 MEMIT 
 34.62 
 31.28 
 18.49 
 28.13 
 
 PRUNE 
 24.77 
 23.87 
 20.69 
 23.11 
 
 RECT 
 86.05 
 80.54 
 31.67 
 66.09 
 
 AlphaEdit 
 94.47 
 91.13 
 32.55 
 72.72 
 
 NSE 
 62.29 
 47.13 
 32.32 
 47.25 
 
 ReFT 
 19.47 
 18.77 
 13.88 
 17.37 
 
 ORE (Ours) 
 94.71 
 90.86 
 29.24 
 71.60 
 
 
 
 Table 5: Sequential Editing on the ZsRE benchmark using LLaMA-3-8B. 
 
 
 Although ORE is primarily designed to address general semantic entanglement in batch knowledge editing, we additionally report results on sequential editing as a complementary evaluation. All the experiment settings are followed Fang et al. (2025) and Sun et al. (2025) . 
 
 
 To mitigate catastrophic forgetting under sequential edits, we incorporate an experience replay mechanism following prior continual learning practice Rolnick et al. (2019) .
Specifically, we maintain a replay buffer consisting of previously edited requests.
During training for the current edits, we uniformly sample a small subset from the buffer, where the replay size is 1.
The overall objective at each optimization step is augmented by an additional replay loss computed on the sampled historical edits: ℒ ′ = ℒ + ℒ r ​ e ​ p ​ l ​ a ​ y \mathcal{L}^{\prime}=\mathcal{L}+\mathcal{L}_{replay} . 
 
 
 
 
 
 
 
 Method 
 Eff. ↑ \uparrow 
 Gen. ↑ \uparrow 
 Spe. ↑ \uparrow 
 Avg. ↑ \uparrow 
 
 FT 
 83.33 
 67.79 
 46.63 
 65.92 
 
 ROME 
 64.40 
 61.42 
 49.44 
 58.42 
 
 MEMIT 
 65.65 
 64.65 
 51.56 
 60.62 
 
 PRUNE 
 68.25 
 64.75 
 49.82 
 60.94 
 
 RECT 
 66.05 
 63.62 
 61.41 
 63.69 
 
 AlphaEdit 
 98.90 
 94.22 
 67.88 
 87.00 
 
 NSE 
 96.14 
 78.42 
 87.66 
 87.41 
 
 ReFT 
 42.03 
 42.46 
 56.50 
 47.00 
 
 ORE (Ours) 
 86.76 
 84.20 
 85.26 
 85.41 
 
 
 
 Table 6: Sequential Editing on the CounterFact benchmark using LLaMA-3-8B. 
 
 
 Table 5 , 6 and 7 report the performance of different knowledge editing methods under sequential editing settings on ZsRE, CounterFact, and Bi-ZsRE benchmarks using LLaMA3-8B as the backbone model. From the results, we observe that:
(1) ORE achieves competitive overall performance across all three benchmarks and outperforms all the baselines on the Bi-ZsRE dataset, indicating its effectiveness in complex knowledge editing scenarios.
(2) Interestingly, ORE exhibits higher Specificity in sequential editing compared to batch editing. This behavior can be attributed to the dynamic gating mechanism. In sequential settings, each editing step focuses on a smaller batch, making the knowledge-carrying token positions more clearly identifiable. This allows the gating network to activate intervention in a highly selective and sparse manner, while remaining silent on irrelevant tokens and non-target contexts. 
 
 
 
 
 
 
 
 Method 
 Eff. ↑ \uparrow 
 Gen. ↑ \uparrow 
 Spe. ↑ \uparrow 
 Avg. ↑ \uparrow 
 
 FT 
 31.41 
 29.97 
 15.29 
 25.56 
 
 ROME 
 2.54 
 2.46 
 0.39 
 1.80 
 
 MEMIT 
 4.58 
 4.03 
 2.84 
 3.82 
 
 PRUNE 
 4.92 
 4.22 
 1.90 
 3.68 
 
 RECT 
 41.01 
 38.58 
 20.80 
 33.46 
 
 AlphaEdit 
 71.88 
 66.55 
 30.47 
 56.30 
 
 LangEdit 
 73.18 
 66.95 
 31.11 
 57.08 
 
 NSE 
 49.43 
 48.06 
 30.58 
 42.69 
 
 ReFT 
 26.07 
 25.54 
 15.22 
 22.28 
 
 ORE (Ours) 
 80.53 
 76.31 
 26.81 
 61.22 
 
 
 
 Table 7: Sequential Editing on the Bi-ZsRE benchmark using LLaMA-3-8B. 
 
 
 

