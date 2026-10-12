# SameSubjectPerturbation — arXiv 2502.06868

Source: https://arxiv.org/html/2502.06868

## Headings
# Related Knowledge Perturbation Matters: Rethinking Multiple Pieces of Knowledge Editing in Same-Subject
## 1 Introduction
## 2 Preliminary
### 2.1 Knowledge in Language Model
### 2.2 Same-Subject Editing
## 3 Pilot Observation
## 4 Related Knowledge Perturbation
### 4.1 S 2 ​ RKE \text{S}^{2}\text{RKE} Benchmark
### 4.2 Failure of Editing Methods
### 4.3 Analysis of Failures
## 5 Perturbation Analysis
### 5.1 Causes of Perturbation
### 5.2 Experiment Validation
## 6 Conclusion
## 7 Limitation
## 8 Acknowledgement
## References
## Appendix A Related Works
### A.1 Knowledge Editing
### A.2 Sequantial-editing vs. Batch-editing
## Appendix B Details of S 2 ​ RKE \text{S}^{2}\text{RKE} Benchmark
### B.1 Data Construction
### B.2 Data Summary
## Appendix C Detailed Experimental Setup
### C.1 Editing Methods
### C.2 Selected Models
### C.3 Evaluation Metrics
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 5, "held-out": 0, "held out": 0, "generaliz": 6, "multi-token": 0, "unseen": 0, "novel entit": 0, "new entit": 0, "counterfact": 6, "zsre": 0, "teacher forc": 0, "autoregressive": 2, "subject": 85, "last token": 2, "embedding": 2, "vocabulary": 1, "propagat": 0}


## SECTION: 4.1 S 2 ​ RKE \text{S}^{2}\text{RKE} Benchmark



 
 We introduce the S 2 ​ RKE \text{S}^{2}\text{RKE} ( S ame-subject R elated K nowledge E diting) benchmark, specifically designed to facilitate the editing of multiple related pieces of knowledge for each subject. It covers six categories of subjects, comprising of 4,503 subjects and 43 relationships, with each subject having an average of 4.9 related knowledge items. See Appendix B for additional technical details about its construction and Table 1 for comparison of statistics between S 2 ​ RKE \text{S}^{2}\text{RKE} and COUNTERFACT. 
 
 
 
 
 
 
 Item 
 S 2 ​ RKE \text{S}^{2}\text{RKE} 
 COUNTERFACT 
 
 Records 
 22064 
 21919 
 
 Subjects 
 4503 
 20391 
 
 Relations 
 43 
 32 
 
 Maximum records per subject 
 13 
 4 
 
 Minimum records per subject 
 3 
 1 
 
 Average records per subject 
 4.9 
 1.1 
 
 
 
 Table 1: Comparison of different benchmarks. 
 
 
 



## SECTION: 4.2 Failure of Editing Methods



 
 Editing Methods. We evaluate six widely-used editing methods: ROME Meng et al. (2022a) , MEMIT Meng et al. (2022b) , PMET Li et al. (2024a) , FT Zhu et al. (2021) , MEND Mitchell et al. (2022a) , and KN Dai et al. (2022) . 
 
 
 Selected LLMs. Experiments are conducted on three LLMs with different parameter sizes: GPT-2 XL (1.5B) Radford et al. (2019) , GPT-J (6B) Wang and Komatsuzaki (2021) , and LLaMA-2 (7B) Touvron et al. (2023) . 
 
 
 We design two experimental schemes to assess how editing related knowledge impacts performance: Same-Subject , where all edited knowledge shares the same subject, Different-Subject , where each edit involves a different subject. Experimental data are selected from the S 2 ​ RKE \text{S}^{2}\text{RKE} benchmark. 
 
 
 Our pilot observation indicates that while knowledge correlation impacts editing effectiveness, it has little effect on overall model performance. So we focus on the Score(S) metric and introduce the Score Difference (SD) metric, defined as SD = Score(same-subject) – Score(different-subject), to quantify performance degradation when editing related knowledge for the same subject. To ensure reliability, each test was repeated 30 times with different editing instances. See Appendix C for more details. 
 
 
 Result & Analysis. Figure  3 and Figure  8(b) show the results of sequential-editing and batch-editing on three LLMs using six methods, respectively. The line in each figure represents the Score Difference (SD). The results show that locate-then-edit methods (e.g., ROME, MEMIT, PMET) suffer significant performance degradation under Same-Subject editing, as reflected by a substantial negative Score Difference (SD). In contrast, methods with generally lower editing effectiveness show minimal sensitivity to the relatedness of the edited knowledge. These findings confirm that knowledge correlation markedly impairs the editing performance of certain methods. 
 
 
 



## SECTION: 4.3 Analysis of Failures



 
 We further examine how the sequence of knowledge edits affects locate-then-edit methods by isolating the interference of sequential updates. For this purpose, we devised two experimental settings: Homogeneous-Editing , where the first and last edits target the same subject, and Heterogeneous-Editing , in which they target different subject. Experiments were performed using ROME, MEMIT, and PMET across three LLMs, with each configuration repeated 30 times on different instances from the S 2 ​ RKE \text{S}^{2}\text{RKE} benchmark to ensure robust results. 
 
 
 Figure 4: The results of sequential-editing on GPT-2 XL and GPT-J using mainstream locate-then-edit methods. The bars represent the Score (S) of two strategies, and the line represents the Score Difference (SD) between the two strategies. 
 
 
 Result & Analysis. Figure  4 shows the sequential-editing results on GPT-2 XL and GPT-J, while Figures  7 and  8(c) provide additional results. Under the Homogeneous-Editing setting, the initial edit’s score is much lower than in the Heterogeneous-Editing condition. This clearly indicates that later edits interfere with earlier ones. We call this effect " related knowledge perturbation ," which exposes a key limitation of current locate-then-edit approaches when processing multiple sequential updates. These findings highlight the need for better strategies in managing sequential knowledge updates. The next section will analysis the causes of related knowledge perturbation . 
 
 
 
 



## SECTION: 5 Perturbation Analysis



 
 Figure 5: Illustration of related knowledge perturbation in same-subject editing. 
 
 



## SECTION: 5.2 Experiment Validation



 
 To verify the above speculation, we used MEMIT to edit two pieces of knowledge on GPT-J through sequential-editing and batch-editing , designing two experimental schemes: Same-Subject and Different-Subject . We then examine the relationship between the cosine similarity of the two keys and the Efficacy Success of editing the first piece of knowledge. Cosine similarity was chosen because it measures how similar the two keys are in vector space, helping us understand how closely related the two knowledge pieces are. 
 
 
 Figure 6: The relationship between the cosine similarity of keys and the Efficacy Success (ES) of the first knowledge editing using MEMIT to edit GPT-J, under sequential-editing and batch-editing . 
 
 
 Result & Analysis  Figure 6 shows the relationship between key similarity and the first knowledge editing Efficacy Success. The results indicate that when two pieces of knowledge related to the same subject are edited, the CS of the key approaches 1. Meanwhile, the ES of editing the first piece of knowledge is significantly lower compared to the case where the two edited pieces of edited knowledge are related to different subjects. This supports our hypothesis that since the key calculation only focuses on subject information, subsequent edits for the same subject interfere with earlier ones, leading to "related knowledge perturbation" . 
 
 
 
 



## SECTION: Appendix B Details of S 2 ​ RKE \text{S}^{2}\text{RKE} Benchmark



 



## SECTION: Appendix C Detailed Experimental Setup



 



## SECTION: C.1 Editing Methods



 
 In this paper, we use six editing methods: 
 
 
 FT Zhu et al. (2021) applies an ℓ ∞ \ell_{\infty} norm constraint on the fine-tuning loss, limiting the difference between the original and edited model’s parameters to reduce side effects. 
 
 
 MEND Mitchell et al. (2022a) uses a collection of small hypernetworks to learn a rank-one decomposition of the gradient obtained by standard fine-tuning, enabling tractable edits in LLMs. 
 
 
 KN Dai et al. (2022) select neurons associated with knowledge expression via gradient-based attributions, then modify MLP layer at the rows corresponding to those neurons by adding scaled embedding vectors. 
 
 
 ROME Meng et al. (2022a) uses causal tracing to localize the knowledge storage at a specific MLP layer in a transformer, and then updates knowledge by altering the weight matrix with rank-one update. 
 
 
 MEMIT Meng et al. (2022b) extends ROME by distributing updates across multiple MLP layers, enabling large-scale edits. 
 
 
 PMET Li et al. (2024a) enhances MEMIT by integrating information from both the multi-head self-attention (MHSA) and MLP modules during the optimization process. 
 
 
 It is worth noting that ROME and KN can only sequential-editing . All experiments are conducted using the EasyEdit Wang et al. (2023) , ensuring standardized and reproducible evaluations. 
 
 
 



## SECTION: C.3 Evaluation Metrics



 
 To comprehensively evaluate the experimental results, we evaluate editing methods across four dimensions: 
 
 
 Efficacy. We measure efficacy using the Efficacy Success ( ES ) metric. Specifically, when triple ( s , r , o ) (s,r,o) is updated to ( s , r , o ∗ ) (s,r,o_{\ast}) , ES calculates the success rate of the target edit by determining the probability that the condition P [ o ∗ ] > P [ o ] P[o{\ast}]>P[o] is satisfied. 
 
 
 Generalization. To evaluate generalization, we use Paraphrase Success ( PS ) metric, which measures the probability that P ⁡ [ o ∗ ] > P ⁡ [ o ] P[o_{\ast}]>P[o] when the model is prompted with a paraphrase of the original ( s , r ) (s,r) . 
 
 
 Specificity. For specificity, we adopt the Neighborhood Success ( NS ) metric, which tests the probability that P ⁡ [ o c ] > P ⁡ [ o ∗ ] P[o_{c}]>P[o_{\ast}] for triplet ( s , r , o c ) (s,r,o_{c}) , where o c o_{c} lies outside the range of the factual edits. 
 
 
 Overall Performance. We assess overall model performance using Perplexity ( PPL ), based on prior studies by Yang et al. (2024a) ; Yang et al. (2024b) . An increase in perplexity generally indicates a decrease in the model’s performance in generation tasks. 
 
 
 Finally, to evaluate the balance between efficacy, generalization, and specificity, we report the harmonic mean of ES , PS , and NS indicators as a comprehensive score ( S ), providing a holistic view of the model’s behavior across these dimensions. 
 
 
 
 
 
 
 
 
 Experimental support, please
 view the build logs 
 for errors. Generated by
 
 
 L
 A 
 T
 E 
 
 xml 
 
 .
 
 
 
