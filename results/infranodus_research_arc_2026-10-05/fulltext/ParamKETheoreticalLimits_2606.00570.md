# ParamKETheoreticalLimits — arXiv 2606.00570

Source: https://arxiv.org/html/2606.00570

## Headings
# Revisiting Parameter-Based Knowledge Editing in Large Language Models: Theoretical Limits and Empirical Evidence
## 1 Introduction
## 2 Related Work
## 3 Preliminaries
## 4 Theoretical Analysis
### 4.1 Working Hypotheses and Problem Formulation
### 4.2 Relative Perturbation Amplification in Collapsed Directions
### 4.3 Cumulative Effects in Sequential Editing
### 4.4 From Representation Distortion to Capability Degradation
## 5 Empirical Study
### 5.1 Experimental Settings
### 5.2 Experimental Results
## 6 Conclusion
## Acknowledgements
## Impact Statement
## References
## Appendix A Related Work
### A.1 Knowledge Editing Methods
### A.2 Summary of Experimental Settings
## Appendix B Justifications for Working Hypotheses and Empirical Support
### B.1 Hypothesis  4.1 : Dimensional Collapse
### B.2 Hypothesis  4.2 : Small-Perturbation Regime
### B.3 Hypothesis  4.3 : Local Representation Stability
### B.4 Generalization Across Model Scales and Architectures
### B.5 Direct Empirical Validation of the Amplification Mechanism
#### B.5.1 Directional amplification along collapsed directions
#### B.5.2 Layerwise distributions of relative change rates
### B.6 Functional Relevance: Correlation with Editing Performance
## Appendix C Experiments and Results
### C.1 Full Experimental Settings for the Benchmark Study
### C.2 Dataset
### C.3 Additional Results
### C.4 Failure Case Study on Editing Reasoning LLM
### C.5 Token-Level Locality Evaluation
### C.6 AlphaEdit Hyperparameter Sensitivity Analysis
## Appendix D Fairness of SCR vs. Parameter-Based Editing Methods
## Appendix E Efficiency-Performance Analysis of SCR
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 1, "held-out": 0, "held out": 0, "generaliz": 15, "multi-token": 0, "unseen": 0, "novel entit": 0, "new entit": 0, "counterfact": 22, "zsre": 19, "teacher forc": 1, "autoregressive": 3, "subject": 11, "last token": 0, "embedding": 4, "vocabulary": 0, "propagat": 5}


## SECTION: 4 Theoretical Analysis



 
 This section develops a geometric framework for understanding why parameter-based knowledge editing can induce disproportionate side effects in large language models. Our analysis is motivated by a simple observation: if hidden representations are dimensionally collapsed, then some representation directions have extremely weak native signal scales, making them vulnerable to even localized parameter perturbations. 
 
 
 We formalize this intuition in four steps. First, we introduce the setup and the working assumptions under which the mechanism is analyzable (Section  4.1 ). Second, we define a relative-sensitivity metric and show why perturbations can be strongly amplified in low-singular-value directions (Section  4.2 ). Third, we discuss how such distortions accumulate under sequential editing and why practical behavior may become even worse once representation stability breaks down (Section  4.3 ).
Finally, we bridge the representation-level analysis to model performance by exploring how excessive distortions correlate with downstream capability degradation, providing empirical evidence for the practical significance of this geometric vulnerability (Section  4.4 ). 
 
 
 Our goal is not to fully characterize edited LLM dynamics but to isolate a minimal vulnerability: dimensional collapse makes representations fragile in low-variance directions, even in locally stable regimes. 
 
 



## SECTION: 5.1 Experimental Settings



 
 We evaluate on Llama-2-7B-Chat  ( Touvron et al., 2023 ) , Llama-3.1-8B-Instruct  ( Meta AI, 2024 ) , Mistral-7B-Instruct  ( Jiang et al., 2023 ) , and DeepSeek-R1-Distill-LLaMA-8B  ( Guo et al., 2025 ) , with larger-scale verification on Llama-2-13B and Qwen3-14B. The studied parameter-modifying methods span locate-then-edit (ROME  ( Meng et al., 2022b ) , MEMIT  ( Meng et al., ) , PMET  ( Li et al., 2024c ) , RECT  ( Gu et al., 2024b ) , AlphaEdit  ( Fang et al., 2025a ) , FT-L), meta-learning (MEND  ( De Cao et al., 2021 ) ), and additional-parameter methods (AdaLoRA  ( Zhang et al., 2023b ) , WISE  ( Wang et al., 2024b ) ); external memory baselines include GRACE  ( Hartvigsen et al., 2024 ) and SCR  ( He et al., 2025 ) .
We use the ZsRE  ( Levy et al., 2017 ) , WikiData counterfact {}_{\text{counterfact}}   ( Cohen et al., 2024 ) , and ELKEN  ( Peng et al., 2024 ) datasets for editing, and mathematical reasoning datasets for general tasks.
Evaluation adopts autoregressive decoding with semantic consistency judged by Qwen2.5-72B-Instruct across four dimensions  ( Zhang et al., 2024b ) .
A token-level locality check confirms the semantic results (Appendix  C.5 ). Full implementation details, hardware specifications, and metric calculation procedures are provided in Appendix  C.1 . 
 
 
 



## SECTION: 5.2 Experimental Results



 
 RQ1: How do knowledge editing methods perform in practice-oriented settings? 
 
 
 Figure  3 illustrates the intermediate performance of Llama-3.1-8B-Instruct on the ZsRE dataset as the number of edits increases from 1 to 10, 100, and finally to the full dataset. For the corresponding results of Llama-2-7B-Chat and Mistral-7B-Instruct, refer to Figure  7 and Figure  8 in the Appendix C.3 , respectively.
Appendix C.3 (Tables  29 – 31 ) presents a comprehensive comparison of knowledge editing methods across ZsRE, WikiData counterfact {}_{\text{counterfact}} , and larger LLMs such as Llama-2-13B and Qwen3-14B. 
 
 
 Table 3 : Performance comparison of knowledge editing methods applied to DeepSeek-R1-Distill-Llama-8B on the ZsRE dataset, reporting results across four evaluation dimensions in both single and sequential editing settings, along with their average scores. 
 
 
 
 Method 
 Single Editing 
 Sequential Editing 
 
 
 
 
 Rel. 
 
 
 
 
 Gen. 
 
 
 
 
 Loc. 
 
 
 
 
 Port. 
 
 
 
 
 Avg. 
 
 
 
 
 Rel. 
 
 
 
 
 Gen. 
 
 
 
 
 Loc. 
 
 
 
 
 Port. 
 
 
 
 
 Avg. 
 
 
 Pre-edit 
 3.00 
 3.00 
 15.50 
 4.36 
 6.47 
 3.00 
 3.00 
 15.50 
 4.36 
 6.47 
 
 ROME 
 36.00 
 42.00 
 3.00 
 17.99 
 24.75 
 1.00 
 0.00 
 0.00 
 0.00 
 0.25 
 
 RECT 
 37.00 
 35.00 
 6.00 
 16.02 
 23.51 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 AlphaEdit 
 43.00 
 24.00 
 13.50 
 8.88 
 22.35 
 46.00 
 35.00 
 8.00 
 7.62 
 24.16 
 
 FT-L 
 2.00 
 2.00 
 2.00 
 3.93 
 2.48 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 MEND 
 36.00 
 42.00 
 10.50 
 15.47 
 25.99 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 AdaLoRA 
 18.00 
 15.00 
 0.50 
 8.03 
 10.38 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 WISE 
 8.00 
 5.00 
 3.00 
 2.59 
 4.65 
 2.00 
 2.00 
 7.50 
 2.52 
 3.50 
 
 GRACE 
 31.00 
 3.00 
 15.50 
 4.03 
 13.38 
 38.00 
 3.00 
 15.50 
 4.03 
 15.13 
 
 SCR 
 85.00 
 84.00 
 15.50 
 41.87 
 56.59 
 90.00 
 90.00 
 15.50 
 45.26 
 60.19 
 
 
 
 
 The experimental results reveal the following:
(1) Under autoregressive inference and evaluation based on semantic consistency, all parameter modification-based methods fall significantly short of the near-perfect single-edit performance reported in prior work.
(2) Most parameter modification-based methods, such as ROME and MEND, collapse under sequential editing scenarios: as the number of edits increases, all metrics quickly drop to near zero. This indicates a complete failure to retain knowledge across multiple updates.
(3) AlphaEdit maintains a stable performance rate across continuous edits, its Reliability and Generalization scores on LLaMA-3.1-8B-Instruct are only 69.49 and 55.50, respectively.
More importantly, it underperforms on Locality and Portability, with scores of just 8.38 and 8.58, highlighting its limited flexibility in applying edited knowledge.
It is worth noting that AlphaEdit demonstrates sensitivity to hyperparameters and model architecture. Further analysis can be found in Appendix  C.6 .
(4) All parameter-based editing methods are outperformed by SCR, a simple and intuitive retrieval-based reference baseline without modifying model parameters. This highlights the practical potential of external-knowledge-based approaches in real-world knowledge updating tasks. Rather than serving as a direct competitor to parameter-based editing methods, SCR provides a distinct empirical perspective by operating outside the parametric editing paradigm, facilitating a principled study of the efficiency–reliability trade-off.
Supplemental comparisons between SCR and parameter-based editing methods
are reported in Appendix  D (Tables  42 and  43 ). 
 
 
 A fine-grained analysis over a wider range of edit counts (Table  37 in Appendix  C.3 ) further confirms that while the timing of degradation varies by method, all parameter-based editing methods exhibit performance decline over longer edit sequences. Additionally,
there is consistent trends across both high- and low-confidence fact sets (Appendix  C.3 , Table  38 ). 
 
 
 RQ2: Can knowledge editing help reasoning LLMs integrate new facts without degrading reasoning ability? 
 
 
 As LLMs are increasingly applied to complex reasoning tasks, reasoning ability has become a key strength. Yet the effectiveness of knowledge editing methods for reasoning-oriented LLMs remains largely underexplored. 
 
 
 Tables 3 and 32 (Appendix C.3 ) present results on ZsRE dataset and WikiData counterfact {}_{\text{counterfact}} , respectively.
To evaluate the retention of reasoning abilities after editing, we assess edited LLMs on a suite of mathematical reasoning benchmarks and broader downstream tasks (including GPQA-Diamond, ARC c {}_{\text{c}} , and MMLU-Pro), reporting accuracy after 10 and 100 edits (Tables  33 and   34 in Appendix  C.3 ).
The results consistently show that reasoning performance collapses after extensive sequential edits for most parameter-based editing methods, while AlphaEdit exhibits relative resilience. 
 
 
 Based on the comparison between Table 3 and Table 29 , knowledge editing methods that rely on parameter modification exhibit inferior performance on reasoning-oriented LLMs compared to general-purpose LLMs. For instance, AlphaEdit’s average performance in sequential editing scenarios drops from 35.48 to 24.16. This degradation may be due to the more implicit and distributed nature of knowledge representation in reasoning LLMs, as well as their greater dependence on long-range context reasoning. In contrast, SCR remains a strong practical reference baseline by integrating internal and external knowledge through selective context construction. 
 
 
 As shown in Table  33 
, ROME and RECT retain some performance, with average accuracy drops of 2.74 and 8.37, respectively. However, after 100 edits, their accuracy nearly drops to zero, indicating a complete collapse in reasoning ability. For MEND, accuracy remains at 0.00 after both 10 and 100 edits, suggesting that the method leads to total LLM failure. In contrast, AlphaEdit exhibits minimal performance degradation across all datasets, even after 100 sequential edits, and in some cases, exhibits slight improvements. Its parameter modifications can maintain reasoning accuracy close to that of the original LLM. Nevertheless, due to its limitations in locality and portability for knowledge editing, AlphaEdit may be better suited for general-purpose Parameter-Efficient Fine-Tuning rather than targeted knowledge editing tasks. 
 
 
 A detailed case analysis (see Appendix  39 ) reveals that editing reasoning-oriented LLMs presents unique challenges.
While editing methods can successfully guide the LLM to produce the correct next token, the edited LLM’s internal reasoning process often leads it to reflect outdated knowledge, thereby undermining the effectiveness of the edit. Moreover, in striving to preserve logical coherence within its reasoning trajectory, the edited LLM may generate explanations that are plausible-sounding but entirely fabricated. In some instances, the edited LLM may even disregard the original question in its attempt to round out the answer. These behaviors underscore key limitations of current knowledge editing methods when applied to reasoning-oriented LLMs. 
 
 
 RQ3: Can knowledge editing methods generalize from factual knowledge to event knowledge? 
 
 
 While most existing research focuses on fact-based knowledge editing in the form of triples, real-world knowledge is often organized in a more complex manner, such as event. 
 
 
 However, current studies on knowledge editing rarely evaluate methods on more complex, event-level datasets.
To address this limitation, we conduct knowledge editing experiments on Llama-2-7B-Chat, Llama-3.1-8B-Instruct, and DeepSeek-R1-Distill-Llama-8B using the ELKEN dataset  ( Peng et al., 2024 ) ,
the dataset processing code using GPT-4o is fully described in Appendix C.2 .
Performance comparison between AlphaEdit and SCR on sequential editing tasks are shown in Figure 4 .
Detailed results for sigle editing and sequential editing are presented in Table  35 and Table  36 
(Appendix C.3 ). 
 
 
 The results indicate that most parameter-based knowledge editing methods struggle to achieve satisfactory performance even in single-edit scenarios, and they almost completely break down under sequential editing. For instance, although AlphaEdit performs well on fact-based datasets, its performance deteriorates significantly when applied to event-level editing tasks involving multiple entities and attributes occurring concurrently. This degradation is primarily due to the limited ability of these methods to capture complex semantic relationships between entities and to integrate contextual information across interconnected elements via parameter-level adjustments. In contrast, SCR consistently achieves the best results across nearly all settings we evaluate. These findings underscore the practical limitations of parameter updates for editing small amounts of knowledge, while highlighting the substantial potential of in-context learning in LLMs for real-world applications. 
 
 
 RQ4: How do different knowledge editing methods compare in terms of time efficiency? 
 
 
 Beyond correctness and robustness, latency and efficiency are equally crucial for practical deployment. Effective editing methods should minimize both editing overhead and inference latency.
To systematically evaluate these aspects, we consider two key metrics: (i) edit time , the wall-clock time required to apply an individual edit, and (ii) inference time , defined as the average wall-clock latency per input query normalized by the base LLM’s latency, measured under greedy decoding with a fixed output length of 50 tokens post-edit. 
 
 
 
 Figure 4 : 
Performance comparison between AlphaEdit and SCR on sequential editing tasks using the ELKEN dataset.
 
 
 
 Figure  5 illustrates the trade-off between editing time and inference latency for parameter-based and external knowledge–based methods, with detailed results for all methods reported in Figure  9 in the Appendix C.3 . Regarding editing time, methods that integrate knowledge through progressively more abstract representations, from textual edits to embeddings, hidden states, and ultimately parameter updates, exhibit increasing editing costs. This trend reflects the growing computational overhead associated with deeper and more indirect knowledge integration. In contrast, parameter-based editing methods do not introduce additional inference latency, as they directly modify the original model parameters.
External knowledge-based methods, such as SCR, generally incur higher inference costs, primarily because of retrieval operations or the need to handle extended input sequences.
Overall, no method achieves strong performance on both axes simultaneously. This reveals a fundamental limitation of current model editing paradigms: intrusive parameter updates trade update efficiency for inference efficiency, while non-intrusive methods preserve fast updates at the expense of increased inference latency.
A more detailed analysis of SCR’s VRAM consumption, inference time, and performance stability across memory sizes and top-k settings is provided in Appendix  E (Tables  44 – 46 ). 
 
 
 
 Figure 5 : 
Trade-off between editing time and inference latency relative to the base model across different editing paradigms.
 
 
 
 
 



## SECTION: A.1 Knowledge Editing Methods



 
 LLMs are often regarded as knowledge bases, as they encapsulate vast amounts of world knowledge within their extensive parameters, which are derived from large-scale datasets during the pre-training phase  ( Petroni et al., 2019 ; Geva et al., 2021 ; Geva et al., ; Dai et al., 2022 ) .
To cope with knowledge updates, the knowledge editing approach  ( Meng et al., 2022b ; Meng et al., ) encodes target knowledge into specific parameters, which are then replaced or supplemented in the LLM to update its factual knowledge. 
 
 
 Locate-then-edit. 
methods  ( Meng et al., ; Zhang et al., 2024a ; Li et al., 2024c ; Li et al., 2024b ; Hu et al., 2024 ) 
are ground in the interpretability theory of Transformer architecture  ( Geva et al., 2021 ; Lv et al., 2024a ) . It posits that knowledge is distributed across feed-forward networks (FFNs), while attention modules play a role in information copying and transmission. For instance, ROME  ( Meng et al., 2022b ) utilizes causal tracing to first identify the crucial neurons associated with specific knowledge before performing targeted edits.
Furthermore, RECT  ( Gu et al., 2024b ) and AlphaEdit  ( Fang et al., 2025a ) introduce additional constraints based on ROME to prevent excessive parameter shifts during the editing process.
Note that, the assumption of the localized storage of factual knowledge remains controversial  ( Wei et al., 2024 ) .
An alternative hypothesis suggests that the relationship between neurons and knowledge is characterized by a many-to-many dynamic rather than a simplistic one-to-one association  ( Allen-Zhu & Li, 2024 ) . Any modification to the parameters will inevitably affect other knowledge stored in the LLM, including both the original knowledge, and previously edited knowledge. 
 
 
 Meta-learning. methods, such as MEND  ( De Cao et al., 2021 ) and MALMEN  ( Tan et al., ) , employ hyper-networks that are designed to forecast tailored weight updates for each knowledge data instance associated with an LLM. However, the hyper-network for a particular LLM limits their scalability in sequential editing scenarios. Furthermore, the additional training process incurs significant time and computational costs. Additionally, the necessity of modifying parameters for a limited amount of knowledge encapsulated in textual form is a matter of ongoing debate. 
 
 
 Additional parameter-based. methods aim to efficiently integrate target knowledge by isolating the parameters that require adjustment, such as WISE  ( Wang et al., 2024b ) , T-Patcher  ( Huang et al., 2023 ) , MELO  ( Yu et al., 2024 ) and many others  ( Dong et al., 2022 ; Zhang et al., 2024c ; Wang & Li, 2024b ; Wang & Li, 2024a ; Wang et al., 2024a ) .
These methods typically introduce additional parameters or utilize mixture of experts (MoE) architectures  ( Chen et al., 2022 ) , either at the head of the LLM or within its structure.
However, as the number of additional parameters increases, the likelihood of overfitting escalates. This phenomenon can result in the post-edit LLM neglecting prior edits, and compromising its original knowledge. Besides, the continual expansion of neurons may further exacerbate the post-edit LLM’s inference burden. 
 
 
 External Memory-based. methods  ( Zhong et al., 2023 ; Hartvigsen et al., 2024 ; Mitchell et al., 2022 ; Jiang et al., 2024 ; Chen et al., 2024 ; Das et al., ; Zheng et al., 2023 ; Markowitz et al., 2025 ) maintain a memory store for updated knowledge, which can be represented as plain text, hidden states, token embeddings, or knowledge graphs. SERAC  ( Mitchell et al., 2022 ) , a classical method, simulates the editing scope by training a discriminator, whose results distinguish between the original LLM and the counterfactual model. GRACE  ( Hartvigsen et al., 2024 ) maintains a dynamically updated codebook that alters the hidden states during the forward propagation. 
 
 
 In short, most existing methods update LLM knowledge by modifying their parameters or structures. However, in real-world scenarios, the amount of new knowledge available is limited, compared to the vast pre-training data used by LLMs. Encoding new knowledge into the model’s parameters can lead to the loss of original knowledge, risking both an incomplete understanding of updates and potential conflicts with prior knowledge. 
 
 
 



## SECTION: A.2 Summary of Experimental Settings



 
 A comprehensive summary of the experimental settings adopted by recent methods is provided in Table 4 . 
 
 
 Table 4 : Summary of experimental settings for recent methods. We specify whether Fact -, Event -based, or Gene ral purpose Datasets are used. Target LLM specifies whether an Instruct LLM or an Reason ing LLM is employed. Infer ence settings show whether Auto regressive setting is applied instead of teacher-forcing. Under Edits , we clarify if Single or Seq uential editing is tested. For evaluation Dimensions , we specify if Rel iability, Gen eralization, Loc ality, and Port ability are considered. 
 
 
 
 
 Datasets 
 LLM 
 Infer 
 Edits 
 Dimensions 
 
 Category 
 Method 
 Fact 
 Event 
 Gene. 
 Instruct 
 Reason 
 Auto 
 Single 
 Seq. 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 
 Locate-then-edit 
 ROME ( Meng et al., 2022b ) 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 MEMIT ( Meng et al., ) 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 PMET ( Li et al., 2024c ) 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 RECT ( Gu et al., 2024b ) 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 AlphaEdit ( Fang et al., 2025a ) 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 
 FT-L ( Meng et al., 2022b ) 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 
 CoRE ( Park et al., 2025 ) 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 
 EAMET ( Dai et al., 2025 ) 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 
 
 AnyEdit ( Jiang et al., 2025 ) 
 ✓ 
 ✓ 
 ✗ 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 Meta-learning 
 MEND ( De Cao et al., 2021 ) 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 Additional-Parameter 
 AdaLoRA ( Zhang et al., 2023b ) 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 WISE ( Wang et al., 2024b ) 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 AdaEdit ( Li & Chu, 2025 ) 
 ✓ 
 ✗ 
 ✓ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 External Memory 
 GRACE ( Hartvigsen et al., 2024 ) 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✗ 
 ✗ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✓ 
 ✗ 
 
 
 
 
 
 



## SECTION: B.4 Generalization Across Model Scales and Architectures



 
 The main text focuses on 7B–14B decoder-only LLMs, but the geometric signatures underlying our analysis extend beyond a single model. The dimensional-collapse statistics (Tables  5 – 8 ), perturbation norms (Tables  9 – 12 ), PC-stability analyses (Tables  13 – 20 ), and R k R_{k} distributions (Tables  21 – 24 ) consistently reveal evidence of the same vulnerability mechanism across DeepSeek-R1-Distill-LLaMA-8B, LlaMA-2-13B, and specific components of T5-3B. 
 
 
 However, the encoder-decoder architecture exhibits greater heterogeneity, with certain layers departing from the small-perturbation regime more rapidly. As a result, we do not assert identical quantitative patterns across all architectures. Instead, we posit that the amplification mechanism arising from dimensional collapse is broadly applicable. The severity of this mechanism depends on factors including architecture type, layer characteristics, editing method, and editing horizon. 
 
 
 



## SECTION: Appendix C Experiments and Results



 



## SECTION: C.1 Full Experimental Settings for the Benchmark Study



 
 This section provides the complete experimental configuration for the benchmark evaluation in Section  5 , complementing the concise description in Section  5.1 . 
 
 
 LLMs. We primarily conduct experiments on decoder-only LLMs, including general-purpose LLMs like Llama-2-7B-Chat ( Touvron et al., 2023 ) , Llama-3.1-8B-Instruct ( Meta AI, 2024 ) , and Mistral-7B-Instruct ( Jiang et al., 2023 ) . To examine the impact of knowledge editing methods on reasoning-oriented models, we additionally evaluate DeepSeek-R1-Distill-LLaMA-8B ( Guo et al., 2025 ) . We also include larger LLMs, Llama-2-13B and Qwen3-14B, for scale comparison. 
 
 
 Knowledge Editing Methods. This study examines recent knowledge editing methods, which can be broadly categorized based on whether they modify a model’s internal parameters. Parameter-based editing methods include locate-then-edit methods such as ROME ( Meng et al., 2022b ) , MEMIT ( Meng et al., ) , PMET ( Li et al., 2024c ) , RECT ( Gu et al., 2024b ) , AlphaEdit ( Fang et al., 2025a ) , and FT-L ( Meng et al., 2022b ) , as well as meta-learning-based methods such as MEND ( De Cao et al., 2021 ) . Additional-parameter methods include AdaLoRA ( Zhang et al., 2023b ) and WISE ( Wang et al., 2024b ) . In contrast, external memory-based methods include GRACE ( Hartvigsen et al., 2024 ) and a simple, RAG baseline, Selective Contextual Reasoning (SCR) ( He et al., 2025 ) . 
 
 
 Knowledge Editing Datasets. We use two widely adopted context-free question answering (QA) datasets in knowledge editing research: WikiData counterfact {}_{\text{counterfact}} ( Cohen et al., 2024 ) and Zero-Shot Relation Extraction (ZsRE) ( Levy et al., 2017 ) , both of which serve as counterfactual benchmarks for modifying knowledge in LLMs. In addition, we incorporate an event-centric dataset, ELKEN ( Peng et al., 2024 ) , in which each instance contains multiple related statements, to evaluate the ability of knowledge editing methods to handle more abundant and complex knowledge. 
 
 
 General Datasets. To evaluate the ability of edited LLMs to handle general tasks, we select mathematical reasoning benchmarks (including AIME 2024 ( Zhang & Math-AI, 2024 ) , AIME 2025 ( Zhang & Math-AI, 2025 ) , AMC ( Li et al., 2024a ) , OlympiadBench ( He et al., 2024 ) , and MATH-500 ( Lightman et al., 2024 ) ) and broader downstream tasks (including GPQA-Diamond ( Rein et al., 2023 ) , ARC c {}_{\text{c}} ( Clark et al., 2018 ) , and MMLU-Pro ( Wang et al., 2024d ) ) to assess the extent to which their reasoning capabilities are preserved after editing. 
 
 
 Inference Setting of Knowledge Editing. Following methods such as MEND ( Mitchell et al., 2021 ) and ROME ( Meng et al., 2022a ) , several follow-up studies ( Zhang et al., 2024b ; Wang et al., 2024b ) have adopted teacher forcing ( Williams & Zipser, 1989 ) during inference and evaluated token-level changes. While this evaluation setting is widely used, it relies on ground-truth answer sequences at inference time, which introduces potential data leakage. Such setups may lead to overly optimistic results and fail to accurately reflect the method’s effectiveness in real-world generative scenarios, as also highlighted by Yang et al. (2025) . To ensure a more fair and realistic evaluation, we adopt a unified autoregressive generation paradigm ( McCoy et al., 2023 ) for prediction. We directly evaluate whether the generated answer is correct with respect to the target answer. 
 
 
 Sequential Editing Scenario. Since single editing is less representative of real-world applications, we conduct experiments under a sequential editing scenario. For each dataset, we edit each knowledge item in sequence, treating the final LLM as the fully edited version. 
 
 
 Event Knowledge Editing Settings. For parameter-based knowledge editing methods, we use GPT-4o ( Hurst et al., 2024 ) to convert each event into a set of fact triples, which are then used for sequential editing. The prompt used is given in Appendix  C.2 . For external memory-based methods, the original event text is directly provided as context input or integrated into the editable memory. 
 
 
 Implementation Environment. The main experiments are executed on 8 NVIDIA A800 GPUs under a Linux system. All methods are implemented using EasyEdit. 2 2 
 2 
 
 
 
 
 
 
 
 https://github.com/zjunlp/EasyEdit.git Notably, AlphaEdit fails to work with Llama2 and Mistral. We also tested with its original implementation. The results are consistent with those obtained using the EasyEdit version. See Appendix  C.6 for further details. Evaluation on reasoning benchmarks is conducted using LUFFY. 3 3 
 3 
 
 
 
 
 
 
 
 https://github.com/ElliottYan/LUFFY.git 
 
 
 Metrics Calculation. For the instruct LLM, we limit the max output token length to 50, while for the reasoning LLM, it is set to 1024. For the four evaluation dimensions, we use Qwen2.5-72B-Instruct to assess whether the answers generated by the edited LLMs are semantically consistent with the ground-truth answers, and compute their accuracy (%) accordingly.
We validate this evaluation protocol against human judgments on a subset of examples. Manual verification on 250 randomly sampled cases yields 96% agreement with human annotations, supporting the reliability of the automatic evaluation. 
 
 
 To evaluate the impact of different editing loads on the performance of knowledge editing, we test scenarios involving 1, 10, and 100 edits. Specifically, we select the first 100 knowledge items from the dataset. For the 1-edit setting, each item is edited individually, and the average performance across all 100 edits is reported. For the 10-edit setting, the 100 items are evenly divided into 10 groups, with sequential editing applied within each group; the average performance after each 10-edit sequence is used. For the 100-edit setting, we sequentially edit all 100 items. Regarding locality, we additionally conduct a token-level validation, which yields results consistent with those at the semantic level (see Appendix  C.5 ). 
 
 
 



## SECTION: C.2 Dataset



 
 
 • 
 
 ZsRE : Originally a question-answering dataset, ZsRE is extended by ( Yao et al., ) to assess various dimensions of model editing methods. 
 
 • 
 
 WikiData counterfact {}_{\text{counterfact}} : This dataset collects triplets about popular entities, ensuring that the subject corresponds to one of the most viewed Wikipedia pages. 
 
 • 
 
 ELKEN : This dataset is designed for event-level knowledge editing, focusing on directly editing new events into LLMs. It includes a diverse set of events and corresponding questions about factual knowledge and future trends. Due to the fact that tendency predictions are influenced by factors beyond the current edited event, we have filtered out questions related to future trends, focusing exclusively on factual knowledge. 
 
 
 
 
 The first two datasets, ZsRE and WikiData counterfact {}_{\text{counterfact}} , are from KnowEdit 4 4 
 4 
 
 
 
 
 
 
 
 https://huggingface.co/datasets/zjunlp/KnowEdit and released under the MIT License . The ELKEN dataset 5 5 
 5 
 
 
 
 
 
 
 
 https://github.com/THU-KEG/Event-Level-Knowledge-Editing.git follows the CC BY-NC-SA 4.0 license. 
 
 
 
 
 
 Prompt for Extracting Triples from Event 
 
 
 Please extract one or more (subject, relation, object) triples from the following event.
 Each triple must express a complete, standalone fact, with no redundancy or dependency on other triples.
 
 Instructions:
 If the event contains multiple independent facts, extract multiple triples , one per fact.
 The Subject must be the main entity or actor involved in the fact.
 The Relation should be a clear predicate phrase (verb or action-based phrase) that uniquely points to the Object .
 The Object should contain the new or important information not repeated in the subject or relation.
 Avoid vague or generic relations like “is involved in”, “is associated with”.
 Do not merge multiple facts into a single triple.
 If there are multiple pieces of information ( e.g. , place, time, role), consider extracting multiple triples .
 
 Format each triple as follows:
 Subject : 
 Prompt: (Concatenate subject and relation into a natural language phrase) 
 Target New: (Only the object, ideally as short as possible)
 
 Example1:
 Event: Serena Williams announces her retirement from professional tennis.
 Output: 
 Subject: Serena Williams 
 Prompt: Serena Williams retires from 
 Target New: professional tennis
 
 Example2:
 Event: Pete Townshend is pursuing a degree in philosophy at the Royal College of Art. 
 Output: 
 Subject: Pete Townshend 
 Prompt: Pete Townshend is pursuing the degree of 
 Target New: philosophy 
 Subject: Pete Townshend 
 Prompt: Pete Townshend is studying at 
 Target New: the Royal College of Art
 
 Example3:
 Event: Paul Wight founded NexGen Technologies in Bergen, appointing Martin Allen as CEO. 
 Output: 
 Subject: Paul Wight 
 Prompt: Paul Wight founded 
 Target New: NexGen Technologies 
 Subject: NexGen Technologies 
 Prompt: The CEO of NexGen Technologies is 
 Target New: Martin Allen
 
 Event: {event} 
 Output: 
 
 
 
 



## SECTION: C.3 Additional Results



 
 Table 29 : Performance comparison of knowledge editing methods on general LLMs using the ZsRE dataset. The best results are shown in bold , and second best results are underlined . ‘–’ denotes that the experiment could not be completed. 
 
 
 
 Model 
 Llama-2-7B-Chat 
 Llama-3.1-8B-Instruct 
 Mistral-7B-Instruct-v0.1 
 
 Metric 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Avg. 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Avg. 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Avg. 
 
 Pre-edit 
 2.54 
 2.31 
 11.49 
 4.50 
 5.21 
 2.70 
 2.40 
 14.26 
 3.68 
 5.76 
 3.77 
 3.07 
 13.30 
 5.35 
 6.37 
 
 ROME 
 0.61 
 0.46 
 0.00 
 0.00 
 0.27 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.23 
 0.08 
 0.04 
 0.00 
 0.09 
 
 MEMIT 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 PMET 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 6.46 
 6.30 
 7.80 
 4.79 
 6.34 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 RECT 
 0.15 
 0.31 
 0.00 
 0.00 
 0.12 
 5.76 
 4.77 
 0.00 
 0.85 
 2.84 
 0.54 
 0.77 
 0.00 
 0.38 
 0.42 
 
 AlphaEdit 
 - 
 - 
 - 
 - 
 - 
 69.49 
 55.50 
 8.38 
 8.56 
 35.48 
 - 
 - 
 - 
 - 
 - 
 
 FT-L 
 0.23 
 0.23 
 0.15 
 0.00 
 0.15 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 5.15 
 4.46 
 10.65 
 4.16 
 6.10 
 
 MEND 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 AdaLoRA 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 WISE 
 8.22 
 6.69 
 8.69 
 2.58 
 6.55 
 2.84 
 2.46 
 10.30 
 2.35 
 4.49 
 2.00 
 1.38 
 1.23 
 0.90 
 1.38 
 
 GRACE 
 48.96 
 0.38 
 9.19 
 0.00 
 14.63 
 60.34 
 2.69 
 10.91 
 3.33 
 19.32 
 60.80 
 0.23 
 12.72 
 0.00 
 18.44 
 
 SCR 
 80.71 
 73.25 
 16.18 
 39.99 
 52.53 
 84.40 
 75.56 
 16.03 
 46.41 
 55.60 
 88.39 
 78.94 
 16.14 
 40.98 
 56.11 
 
 
 
 
 Table 30 : Performance comparison of knowledge editing methods on general LLMs using the WikiData counterfact {}_{\text{counterfact}} dataset. The best results are shown in bold , and second best results are underlined . ‘–’ denotes that the experiment could not be completed. 
 
 
 
 Model 
 Llama-2-7B-Chat 
 Llama-3.1-8B-Instruct 
 Mistral-7B-Instruct-v0.1 
 
 Metric 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Avg. 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Avg. 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Avg. 
 
 Pre-edit 
 0.24 
 0.12 
 29.68 
 2.04 
 8.02 
 0.24 
 0.36 
 30.19 
 3.86 
 8.66 
 0.36 
 0.36 
 31.87 
 5.15 
 9.43 
 
 ROME 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 MEMIT 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 PMET 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.24 
 0.36 
 8.17 
 2.34 
 2.78 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 RECT 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 1.55 
 1.91 
 0.00 
 0.10 
 0.89 
 0.48 
 0.00 
 0.00 
 0.03 
 0.13 
 
 AlphaEdit 
 – 
 – 
 – 
 – 
 – 
 30.51 
 25.63 
 1.33 
 8.09 
 16.39 
 – 
 – 
 – 
 – 
 – 
 
 FT-L 
 0.00 
 0.00 
 0.08 
 0.01 
 0.02 
 0.00 
 0.12 
 0.00 
 0.00 
 0.03 
 0.95 
 0.83 
 1.37 
 0.78 
 0.98 
 
 MEND 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 AdaLoRA 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 WISE 
 21.33 
 13.35 
 14.18 
 5.02 
 13.47 
 0.36 
 0.47 
 29.36 
 3.06 
 8.31 
 4.41 
 5.96 
 5.21 
 1.94 
 4.38 
 
 GRACE 
 48.39 
 0.00 
 24.69 
 1.34 
 18.60 
 40.88 
 0.36 
 28.53 
 2.70 
 18.12 
 52.80 
 0.24 
 31.65 
 1.98 
 21.67 
 
 SCR 
 76.64 
 73.54 
 11.63 
 28.75 
 47.64 
 88.20 
 87.01 
 28.43 
 32.90 
 59.14 
 85.10 
 76.04 
 22.21 
 29.92 
 53.32 
 
 
 
 
 Table 31 : Performance comparison of single and sequential editing on Llama2-13B and Qwen3-14B using the ZsRE dataset.
The results demonstrate consistency with the insights observed in smaller LLMs. In practice-oriented settings, all parameter modification-based methods fall significantly short of the near-perfect single-edit performance. However,
retrieval-based methods maintain robustness in both single and sequential editing scenarios. 
 
 
 
 Llama2-13B 
 
 Method 
 Single Editing 
 Sequential Editing 
 
 Metric 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Avg. 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Avg. 
 
 Pre-edit 
 3.00 
 3.61 
 12.64 
 4.73 
 6.00 
 3.00 
 3.61 
 12.64 
 4.73 
 6.00 
 
 ROME 
 57.41 
 51.88 
 5.61 
 7.66 
 30.64 
 0.46 
 0.23 
 0.00 
 0.63 
 0.33 
 
 MEMIT 
 32.59 
 27.44 
 2.96 
 6.91 
 17.48 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 PMET 
 13.68 
 10.91 
 6.61 
 6.38 
 9.40 
 4.77 
 4.38 
 6.31 
 5.41 
 5.22 
 
 RECT 
 59.42 
 50.12 
 6.03 
 7.84 
 30.85 
 1.15 
 0.92 
 0.04 
 1.77 
 0.97 
 
 AlphaEdit 
 37.66 
 29.82 
 7.07 
 8.23 
 20.70 
 28.05 
 22.91 
 2.42 
 4.20 
 14.40 
 
 FT-L 
 4.07 
 8.61 
 5.69 
 4.99 
 5.84 
 0.00 
 0.08 
 0.00 
 0.00 
 0.02 
 
 MEND 
 1.84 
 1.69 
 12.45 
 3.91 
 4.97 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 AdaLoRA 
 58.80 
 52.50 
 11.45 
 10.66 
 33.35 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 WISE 
 31.44 
 30.28 
 8.15 
 8.85 
 19.68 
 15.07 
 11.07 
 11.80 
 3.60 
 10.39 
 
 GRACE 
 47.81 
 3.61 
 12.64 
 4.73 
 17.20 
 47.35 
 3.77 
 12.64 
 4.73 
 17.12 
 
 SCR 
 70.41 
 70.10 
 18.52 
 47.80 
 51.71 
 68.79 
 61.03 
 17.45 
 38.69 
 46.49 
 
 Qwen3-14B 
 
 Method 
 Single Editing 
 Sequential Editing 
 
 Metric 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Avg. 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Avg. 
 
 Pre-edit 
 2.15 
 1.69 
 11.72 
 1.79 
 4.34 
 2.15 
 1.69 
 11.72 
 1.79 
 4.34 
 
 ROME 
 68.49 
 45.35 
 6.03 
 5.49 
 31.34 
 0.08 
 0.00 
 0.00 
 0.00 
 0.02 
 
 RECT 
 68.72 
 44.81 
 6.11 
 5.55 
 31.30 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 FT-L 
 18.75 
 20.29 
 5.61 
 7.18 
 12.96 
 0.00 
 0.08 
 0.00 
 0.00 
 0.02 
 
 MEND 
 1.69 
 1.69 
 10.88 
 1.52 
 3.95 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 AdaLoRA 
 22.83 
 7.15 
 12.03 
 3.12 
 11.28 
 0.23 
 0.15 
 1.31 
 0.21 
 0.48 
 
 WISE 
 5.38 
 4.07 
 10.11 
 1.88 
 5.36 
 2.77 
 2.46 
 10.53 
 2.17 
 4.48 
 
 GRACE 
 58.34 
 1.69 
 11.84 
 1.79 
 18.42 
 58.80 
 2.38 
 11.84 
 1.79 
 18.70 
 
 SCR 
 49.27 
 58.42 
 11.59 
 34.69 
 38.49 
 85.40 
 74.56 
 11.53 
 29.45 
 50.24 
 
 
 
 
 Figure 7 : Performance changes of knowledge editing methods during sequential editing of Llama-2-7B-Chat on the ZsRE dataset. The x-axis represents the number of edits: 1, 10, 100, and the full dataset. 
 
 
 Figure 8 : Performance changes of knowledge editing methods during sequential editing of Mistral-7B-Instruct-v0.1 on the ZsRE dataset. The x-axis represents the number of edits: 1, 10, 100, and the full dataset. 
 
 
 Table 32 : Performance comparison on the WikiData counterfact {}_{\text{counterfact}} dataset using DeepSeek-R1-Distill-Llama-8B as the backbone. We report four metrics (Reliability, Generalization, Locality, Portability) and their average for both Single and Sequential Editing scenarios. 
 
 
 
 Method 
 Single Editing 
 Sequential Editing 
 
 
 
 
 Rel. 
 
 
 
 
 Gen. 
 
 
 
 
 Loc. 
 
 
 
 
 Port. 
 
 
 
 
 Avg. 
 
 
 
 
 Rel. 
 
 
 
 
 Gen. 
 
 
 
 
 Loc. 
 
 
 
 
 Port. 
 
 
 
 
 Avg. 
 
 
 Pre-edit 
 0.00 
 0.00 
 23.55 
 3.85 
 6.85 
 0.00 
 0.00 
 23.55 
 3.85 
 6.85 
 
 ROME 
 30.00 
 18.00 
 6.22 
 9.23 
 15.86 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 RECT 
 26.00 
 16.00 
 8.80 
 9.14 
 14.98 
 0.00 
 0.00 
 0.00 
 0.03 
 0.01 
 
 AlphaEdit 
 31.00 
 5.00 
 15.19 
 5.53 
 14.18 
 33.00 
 14.00 
 8.37 
 9.71 
 16.27 
 
 FT 
 2.00 
 1.00 
 0.82 
 4.45 
 2.07 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 MEND 
 32.00 
 14.00 
 19.88 
 13.35 
 19.81 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 AdaLoRA 
 22.00 
 19.00 
 19.88 
 13.35 
 18.56 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 WISE 
 8.00 
 7.00 
 3.00 
 2.59 
 5.15 
 0.00 
 0.00 
 6.00 
 2.86 
 2.22 
 
 GRACE 
 12.00 
 0.00 
 23.54 
 4.96 
 10.13 
 12.00 
 0.00 
 23.49 
 4.96 
 10.11 
 
 SCR 
 72.00 
 67.00 
 23.50 
 34.83 
 49.33 
 84.00 
 76.00 
 15.70 
 35.67 
 52.84 
 
 
 
 
 Table 33 : Performance comparison of edited DeepSeek-R1-Distill-Llama-8B on mathematical benchmarks requiring reasoning, reporting accuracy after 10 and 100 edits. 
 
 
 
 Method 
 #Editing 
 AIME 2024 
 AIME 2025 
 AMC 
 MATH-500 
 Olympiad 
 Avg. 
 
 Pre-edit 
 0 
 36.35 
 25.63 
 68.67 
 83.20 
 53.48 
 53.47 
 
 ROME 
 10 
 31.04 
 24.79 
 66.57 
 82.20 
 49.04 
 50.73 
 
 100 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 RECT 
 10 
 33.02 
 24.58 
 33.02 
 83.60 
 51.26 
 45.10 
 
 100 
 0.00 
 0.10 
 0.04 
 0.00 
 0.00 
 0.03 
 
 AlphaEdit 
 10 
 36.56 
 26.56 
 69.43 
 85.20 
 51.85 
 53.92 
 
 100 
 35.31 
 25.94 
 69.47 
 81.40 
 53.48 
 53.12 
 
 MEND 
 10 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 100 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 
 
 
 Table 34 : 
Performance comparison of edited DeepSeek-R1-Distill-Llama-8B on broader reasoning-based downstream tasks, reporting accuracy after 10 and 100 edits.
 
 
 
 
 Method 
 #Editing 
 GPQA-Diamond 
 ARC c {}_{\text{c}} 
 MMLU-Pro 
 Avg. 
 
 Pre-edit 
 0 
 28.79 
 87.80 
 46.13 
 54.24 
 
 ROME 
 10 
 18.69 
 85.15 
 43.30 
 49.05 
 
 100 
 0.00 
 0.00 
 0.00 
 0.00 
 
 AlphaEdit 
 10 
 25.76 
 87.97 
 45.51 
 53.08 
 
 100 
 24.75 
 88.05 
 45.84 
 52.88 
 
 RECT 
 10 
 20.20 
 86.26 
 44.66 
 50.37 
 
 100 
 0.00 
 0.00 
 0.00 
 0.00 
 
 MEND 
 10 
 0.00 
 0.00 
 0.00 
 0.00 
 
 100 
 0.00 
 0.00 
 0.00 
 0.00 
 
 
 
 
 Table 35 : Performance comparison of Single Editing across Llama-2-7B-Chat, Llama-3.1-8B-Instruct, and DeepSeek-R1-Distill-Llama-8B based on the event-level dataset ELKEN. ‘–’ denotes that the experiment could not be completed. Please refer to Footnote 1 for further details. 
 
 
 
 Single 
 Llama-2-7B-Chat 
 Llama-3.1-8B-Instruct 
 DeepSeek-R1-Distill-Llama-8B 
 
 Port. 
 Loc. 
 Avg. 
 Port. 
 Loc. 
 Avg. 
 Port. 
 Loc. 
 Avg. 
 
 Pre-edit 
 5.92 
 43.75 
 24.84 
 7.08 
 56.73 
 31.91 
 9.01 
 48.73 
 28.87 
 
 ROME 
 2.41 
 19.45 
 10.93 
 17.38 
 23.39 
 20.39 
 12.91 
 22.21 
 17.56 
 
 RECT 
 7.69 
 19.83 
 13.76 
 18.45 
 26.55 
 22.50 
 14.70 
 23.29 
 19.00 
 
 AlphaEdit 
 - 
 - 
 - 
 14.60 
 40.61 
 27.61 
 14.25 
 39.76 
 27.01 
 
 FT-L 
 2.33 
 18.19 
 10.26 
 4.79 
 22.86 
 13.83 
 5.53 
 12.90 
 9.22 
 
 AdaLoRA 
 2.07 
 15.21 
 8.64 
 10.18 
 17.18 
 13.68 
 8.32 
 13.62 
 10.97 
 
 WISE 
 2.49 
 25.77 
 14.13 
 4.70 
 33.54 
 19.12 
 8.79 
 30.01 
 19.40 
 
 GRACE 
 2.34 
 34.41 
 18.38 
 6.43 
 54.59 
 30.51 
 9.17 
 46.35 
 27.76 
 
 SCR 
 41.92 
 34.70 
 38.31 
 43.64 
 52.64 
 48.14 
 51.45 
 42.52 
 46.99 
 
 
 
 
 Table 36 : Performance comparison of Sequential Editing across Llama-2-7B-Chat, Llama-3.1-8B-Instruct, and DeepSeek-R1-Distill-Llama-8B based on the event-level dataset ELKEN. ‘–’ denotes that the experiment could not be completed. 
 
 
 
 Sequential 
 Llama-2-7B-Chat 
 Llama-3.1-8B-Instruct 
 DeepSeek-R1-Distill-Llama-8B 
 
 Port. 
 Loc. 
 Avg. 
 Port. 
 Loc. 
 Avg. 
 Port. 
 Loc. 
 Avg. 
 
 Pre-edit 
 5.92 
 43.75 
 24.84 
 7.08 
 56.73 
 31.91 
 9.01 
 48.73 
 28.87 
 
 ROME 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.33 
 0.00 
 0.17 
 
 RECT 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 AlphaEdit 
 - 
 - 
 - 
 14.22 
 19.96 
 17.09 
 12.15 
 17.87 
 15.01 
 
 FT-L 
 3.53 
 0.00 
 1.77 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 
 AdaLoRA 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 0.00 
 5.25 
 0.00 
 2.63 
 
 WISE 
 2.23 
 30.83 
 16.53 
 5.96 
 47.88 
 26.92 
 2.67 
 21.88 
 12.28 
 
 GRACE 
 2.29 
 34.41 
 18.35 
 6.43 
 54.57 
 30.50 
 9.01 
 48.79 
 28.90 
 
 SCR 
 44.29 
 35.05 
 39.67 
 53.04 
 50.90 
 51.97 
 52.99 
 41.93 
 47.46 
 
 
 
 
 
 
 
 
 Editing time comparison 
 
 
 
 Inference time comparison 
 
 Figure 9 : Editing time (in second), and inference latency relative to the base model. 
 
 
 Table 37 : Performance of different editing methods in fine-grained sequential editing scenarios on the Llama-3.1-8B-Instruct model. The experimental results show that the timing of actual p


## SECTION: C.5 Token-Level Locality Evaluation



 
 Results. 
Table  40 presents the token-level locality evaluation results for both single and sequential editing scenarios. The pre-edit model achieves a perfect score of 100% for both metrics by definition. Among the evaluated methods, GRACE maintains 100% locality under both single and sequential editing scenarios, indicating that it perfectly preserves the model’s original behavior. WISE also delivers strong results, particularly in sequential editing. In contrast, most parameter-based editing methods, including ROME, MEND, and AlphaEdit, exhibit significantly lower output consistency. Notably, the SCR method, which incorporates a simple retrieval and filtering mechanism, achieves highly competitive locality scores, demonstrating its robustness in preserving unrelated knowledge. 
 
 
 Table 40 : Token-Level Locality Evaluation 
 
 
 
 Method 
 Single 
 Sequential 
 
 Match Ratio 
 Exact Match 
 Match Ratio 
 Exact Match 
 
 Pre-edit 
 100.00 
 100.00 
 100.00 
 100.00 
 
 ROME 
 10.74 
 2.81 
 0.00 
 0.00 
 
 RECT 
 11.91 
 2.92 
 0.29 
 0.00 
 
 AlphaEdit 
 38.41 
 20.68 
 10.66 
 1.31 
 
 FT-L 
 10.89 
 3.46 
 0.33 
 0.00 
 
 MEND 
 2.26 
 0.04 
 0.00 
 0.00 
 
 AdaLoRA 
 12.15 
 3.54 
 0.00 
 0.00 
 
 WISE 
 64.08 
 51.84 
 76.26 
 67.18 
 
 GRACE 
 100.00 
 100.00 
 100.00 
 100.00 
 
 SCR 
 65.28 
 64.72 
 46.96 
 45.96 
 
 
 
 
 Conclusion. 
The results from this supplementary evaluation confirm the findings from our primary semantic-based locality metric. They highlight the challenges faced by many parameter-based editing methods in maintaining output consistency, especially under sequential editing. The strong performance of non-parametric methods like SCR and GRACE further validates the effectiveness of retrieval-augmented and output-constrained approaches in preserving model locality. 
 
 
 



## SECTION: C.6 AlphaEdit Hyperparameter Sensitivity Analysis



 
 During our evaluation, we observed that the performance of AlphaEdit was highly inconsistent across different LLM architectures. While it performed reasonably well on LLaMA-3.1-8B-Instruct, its performance on Llama-2-7B-Chat and Mistral-7B-Instruct was significantly worse, often approaching zero in sequential editing scenarios. 6 6 
 6 
 
 
 
 
 
 
 
 See the corresponding GitHub issue for further details. This appendix details our investigation into the hyperparameter sensitivity of AlphaEdit. 
 
 
 Experimental Investigation. 
We conducted experiments using the authors’ latest original implementation from the AlphaEdit GitHub repository. All experiments were performed on a single H20 (96 GB) GPU. We used the same settings as MEMIT for a shared setup and focused on AlphaEdit’s unique hyperparameters: nullspace_thresholdand the L2 regularization coefficient. We fixed the nullspace_thresholdat 2e-2 and experimented with two different values for the L2 coefficient: 1 and 10. 
 
 
 Results. 
Table 41 present the results for single and sequential editing across different models. The data reveal a high degree of sensitivity to both hyperparameters and model architecture. On Llama-3.1-8B-Instruct, performance varies significantly with the L2 coefficient. More critically, on Llama-2-7B-Chat and Mistral, AlphaEdit’s performance is near-zero in sequential editing scenarios regardless of the hyperparameter values tested. This indicates a fundamental incompatibility or instability of the method with these model architectures under sequential editing. 
 
 
 Table 41 : AlphaEdit Performance on ZsRE and WikiData counterfact {}_{\text{counterfact}} Dataset with Different L2 Regularization 
 
 
 
 Model (L2) 
 ZsRE Dataset 
 WikiData counterfact {}_{\text{counterfact}} Dataset 
 
 Single Editing 
 Sequential Editing 
 Single Editing 
 Sequential Editing 
 
 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 
 llama2 (L2=1) 
 39.82 
 38.05 
 3.00 
 5.94 
 0.00 
 0.00 
 0.00 
 0.00 
 55.18 
 54.95 
 2.54 
 17.82 
 0.00 
 0.00 
 0.00 
 0.00 
 
 llama3 (L2=1) 
 86.55 
 62.95 
 10.99 
 12.32 
 37.20 
 31.51 
 5.23 
 4.65 
 64.96 
 65.08 
 10.57 
 12.19 
 0.00 
 0.00 
 0.00 
 0.00 
 
 mistral (L2=1) 
 23.83 
 20.37 
 1.23 
 4.02 
 0.15 
 0.15 
 0.00 
 0.00 
 11.21 
 11.20 
 0.26 
 4.79 
 0.00 
 0.00 
 0.00 
 0.00 
 
 llama2 (L2=10) 
 51.19 
 44.12 
 3.96 
 6.37 
 0.00 
 0.00 
 0.00 
 0.00 
 55.48 
 55.48 
 3.37 
 17.38 
 0.00 
 0.00 
 0.00 
 0.00 
 
 llama3 (L2=10) 
 64.95 
 39.12 
 12.18 
 10.42 
 66.72 
 57.49 
 9.61 
 9.31 
 44.93 
 45.17 
 15.90 
 9.37 
 19.79 
 19.90 
 0.44 
 4.72 
 
 mistral (L2=10) 
 47.50 
 40.97 
 3.88 
 5.36 
 0.00 
 0.00 
 0.00 
 0.00 
 24.67 
 24.67 
 1.06 
 8.48 
 0.00 
 0.00 
 0.00 
 0.00 
 
 
 
 
 Conclusion. 
Our analysis demonstrates that AlphaEdit exhibits significant hyperparameter sensitivity and model-specific performance. The method’s inability to achieve non-trivial results on certain widely-used LLMs (Llama-2, Mistral) under sequential editing highlights a critical limitation for its practical applicability. 
 
 
 
 



## SECTION: Appendix D Fairness of SCR vs. Parameter-Based Editing Methods



 
 In this study, we primarily treat SCR as a reference baseline rather than a direct competitor to parameter-based knowledge editing methods. By operating outside the parametric editing paradigm, SCR provides a distinct empirical perspective for analyzing the trade-offs between efficiency and reliability in knowledge editing. 
 
 
 To further explore the comparative advantages and limitations of SCR versus parameter-based editing approaches, we conducted two complementary analyses using LLaMA-3.1-8B-Instruct and the ZsRE dataset. 
 
 
 Evaluation of Efficiency and Reliability 
 
 
 As summarized in Table  42 , we compare SCR and the parameter-based editing method AlphaEdit across multiple metrics, including edit time, inference latency, reliability, and locality. Evaluations are conducted at two sequential-editing scales (N = 100 and N = 1000). The results highlight key operational differences between the two methods. SCR exhibits near-zero upfront editing cost by shifting computational effort to retrieval-based inference, at the expense of retrieval latency. Conversely, AlphaEdit achieves faster results during inference but incurs significant computational cost during initial parameter modification. 
 
 
 Integration of SCR Retrieval for Parameter-Based Editing Methods 
 
 
 To ensure a fair comparison, we augment parameter-based editing methods with an SCR-inspired retrieval mechanism. Using sequential editing scales (N = 10, 100, 500, 1000,
all
) and a top-3 retrieval strategy, results (Table  43 ) reveal that SCR consistently outperforms baseline parameter-based editing methods across key metrics. These findings highlight the inherent limitations of direct parameter editing. Moreover, integrating SCR with parameter-based editing methods enhances their overall performance, demonstrating the efficacy of leveraging external contextual knowledge through retrieval. 
 
 
 Table 42 : 
Comparative analysis of SCR and AlphaEdit on ZsRE dataset.
Evaluation of edit time, inference latency, reliability, and locality for 100 and 1000 sequential edits using SCR and AlphaEdit on Llama-3.1-8B-Instruct.
 
 
 
 N N 
 Method 
 Edit Time 
 Inference Time 
 Rel. 
 Loc. 
 
 100 
 SCR 
 0.00 
 1.6745 
 95.0 
 16.5 
 
 
 AlphaEdit 
 14.07 
 0.8305 
 83.0 
 14.5 
 
 1000 
 SCR 
 0.00 
 1.7516 
 84.8 
 17.2 
 
 
 AlphaEdit 
 14.07 
 0.8305 
 74.0 
 9.7 
 
 
 
 Table 43 : 
Comparison of SCR and parameter-based editing methods (AlphaEdit, MEMIT, WISE, ROME, MEND) with SCR retrieval mechanism integration.
Experiments are conducted on Llama-3.1-8B-Instruct using the ZSRE dataset under sequential edits of N = 10,100,500 , 1000 , N=10,100,500,1000, and all, with a top-3 retriever.
 
 
 
 N N 
 Method 
 Rel. 
 Gen. 
 Loc. 
 Port. 
 Avg. 
 
 10 
 SCR 
 97.0 
 86.0 
 16.0 
 47.9 
 61.7 
 
 
 AlphaEdit+SCR 
 89.0 
 87.0 
 15.0 
 43.6 
 58.6 
 
 
 MEMIT+SCR 
 91.0 
 89.0 
 15.5 
 41.4 
 59.2 
 
 
 WISE+SCR 
 83.0 
 74.0 
 16.0 
 47.9 
 55.2 
 
 
 ROME+SCR 
 84.0 
 87.0 
 9.5 
 25.4 
 51.5 
 
 
 MEND+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 100 
 SCR 
 95.0 
 87.0 
 16.5 
 42.9 
 60.4 
 
 
 AlphaEdit+SCR 
 90.0 
 84.0 
 15.5 
 38.4 
 57.0 
 
 
 MEMIT+SCR 
 94.0 
 87.0 
 13.5 
 37.9 
 58.1 
 
 
 WISE+SCR 
 75.0 
 74.0 
 16.0 
 28.2 
 48.3 
 
 
 ROME+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 
 MEND+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 500 
 SCR 
 90.8 
 82.8 
 16.0 
 47.6 
 59.3 
 
 
 AlphaEdit+SCR 
 90.6 
 83.4 
 15.6 
 42.5 
 58.0 
 
 
 MEMIT+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 
 WISE+SCR 
 77.2 
 66.2 
 16.4 
 31.4 
 47.8 
 
 
 ROME+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 
 MEND+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 1000 
 SCR 
 84.8 
 77.1 
 17.2 
 46.3 
 56.3 
 
 
 AlphaEdit+SCR 
 85.3 
 76.2 
 13.8 
 29.5 
 51.2 
 
 
 MEMIT+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 
 WISE+SCR 
 65.8 
 59.0 
 14.8 
 26.2 
 41.5 
 
 
 ROME+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 
 MEND+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 all 
 SCR 
 84.4 
 75.6 
 16.5 
 46.4 
 55.7 
 
 
 AlphaEdit+SCR 
 81.9 
 72.2 
 13.4 
 26.8 
 48.6 
 
 
 MEMIT+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 
 WISE+SCR 
 66.3 
 56.2 
 15.0 
 27.9 
 41.3 
 
 
 ROME+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 
 MEND+SCR 
 0.0 
 0.0 
 0.0 
 0.0 
 0.0 
 
 
 
 
 



## SECTION: Appendix E Efficiency-Performance Analysis of SCR



 
 To provide a comprehensive analysis of SCR’s resource efficiency and performance stability, we evaluate its VRAM usage, inference latency, and editing effectiveness under varying memory sizes (100 and 1000 stored knowledge items) and retrieval sizes (top-1, top-3, top-5, top-10). All experiments are conducted on Llama-3.1-8B-Instruct, using 100 sequential edits to ensure consistency and comparability. 
 
 
 As summarized in Table  44 , VRAM consumption remains largely stable, demonstrating minimal sensitivity to variations in memory size or top-k retrieval configurations. Inference latency, detailed in Table  45 , moderately increases with higher memory requirements and retrieval sizes, as expected due to the expansion of searchable retrieval windows. Importantly, as shown in Table  46 , editing performance remains consistently robust across all tested configurations, underscoring SCR’s resilience to hyperparameter settings. 
 
 
 Figure  10 illustrates SCR’s resource efficiency and performance metrics, providing a visual summary of inference latency and editing reliability across all experimental settings. 
 
 
 Table 44 : 
VRAM consumption of SCR for sequential editing.
VRAM usage (in MB) during 100 sequential edits using SCR on Llama-3.1-8B-Instruct under different memory and retrieval configurations. 
 
 
 Memory Size 
 Top-1 
 Top-3 
 Top-5 
 Top-10 
 
 100 
 31123 
 31133 
 31145 
 31176 
 
 1000 
 31123 
 31133 
 31145 
 31177 
 
 
 
 Table 45 : 
Inference latency under varying memory and top-k retrieval sizes.
Inference time (in seconds) for 100 sequential edits using SCR on Llama-3.1-8B-Instruct.
 
 
 
 Memory Size 
 Top-1 
 Top-3 
 Top-5 
 Top-10 
 
 100 
 1.68 
 1.67 
 1.70 
 1.76 
 
 1000 
 1.74 
 1.75 
 1.72 
 1.81 
 
 
 
 Table 46 : 
Editing performance under varying retrieval parameters.
Evaluation of editing effectiveness across different configurations. Performance metrics
show consistent results regardless of memory size or retrieval settings.
 
 
 
 
 
 Reliability 
 Generalization 
 Locality 
 Portability 
 
 Memory Size 
 Top-1 
 Top-3 
 Top-5 
 Top-10 
 Top-1 
 Top-3 
 Top-5 
 Top-10 
 Top-1 
 Top-3 
 Top-5 
 Top-10 
 Top-1 
 Top-3 
 Top-5 
 Top-10 
 
 100 
 0.80 
 0.95 
 0.97 
 0.97 
 0.78 
 0.87 
 0.91 
 0.89 
 0.18 
 0.17 
 0.17 
 0.18 
 0.41 
 0.43 
 0.48 
 0.45 
 
 1000 
 0.76 
 0.86 
 0.91 
 0.88 
 0.69 
 0.80 
 0.80 
 0.76 
 0.18 
 0.17 
 0.19 
 0.17 
 0.40 
 0.45 
 0.45 
 0.47 
 
 
 
 
 Figure 10 : 
SCR efficiency and performance metrics for sequential editing.
Visual representation of the SCR’s inference time and editing stability across various memory sizes (100 and 1000) and retrieval windows (top-1, top-3, top-5, and top-10).
 
 
 
 
 
 
 
 
 Experimental support, please
 view the build logs 
 for errors. Generated by
 
 
 L
 A 
 T
 E 
 
 xml 
 
 .
 
 
 
