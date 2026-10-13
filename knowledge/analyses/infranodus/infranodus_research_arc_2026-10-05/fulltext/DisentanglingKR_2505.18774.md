# DisentanglingKR — arXiv 2505.18774

Source: https://arxiv.org/html/2505.18774

## Headings
# Disentangling Knowledge Representations for Large Language Model Editing
## 1 Introduction
## 2 Preliminaries
### 2.1 Autoregressive Language Model
### 2.2 Knowledge Editing via Rank-one Updates
## 3 Methodology
### 3.1 Knowledge Representation Disentanglement
### 3.2 Disentanglement-based Knowledge Edit
## 4 Experiments
### 4.1 FINE-KED Dataset
### 4.2 Experimental Setups
### 4.3 Experiment Results
## 5 Related Work
## 6 Conclusion
## Acknowledgements
## Ethics Statement
## Reproducibility Statement
## References
## Appendix A The Use of Large Language Models
## Appendix B Limitations & Future Discussion
## Appendix C Derivation Details for Fine-Grained Irrelevant Knowledge Preservation
### C.1 Derivation of Equation  ( 17 ) (\ref{eq:ours-objective3})
### C.2 Derivation of the Closed-Form Solution for Equation  ( 18 ) (\ref{eq:ours-objective5})
## Appendix D Details of Datasets & Evaluation Metrics
### D.1 Details of FINE-KED
### D.2 Details of COUNTERFACT
### D.3 Details of MQuAKE-3K
## Appendix E Baselines
## Appendix F Implementation Details and Scalability Analysis
### F.1 Implementation Details
### F.2 Scalability Analysis
## Appendix G Additional Experiments
### G.1 Performance Comparison on COUNTERFACT Using GPT2-XL
### G.2 Performance Comparison on MQuAKE-3K
### G.3 Effect of Fine-Grained Irrelevant Facts in the KRD Module
### G.4 Effect of Training Sample Size in the KRD Module
### G.5 Visualization Analysis of Disentangled Representations
### G.6 Generalization analysis of KRD Module
### G.7 Case Study
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 10, "held-out": 0, "held out": 0, "generaliz": 11, "multi-token": 0, "unseen": 4, "novel entit": 0, "new entit": 0, "counterfact": 20, "zsre": 0, "teacher forc": 0, "autoregressive": 4, "subject": 75, "last token": 3, "embedding": 1, "vocabulary": 0, "propagat": 0}


## SECTION: 3 Methodology



 
 In this section, we present our proposed method, DiKE, with its overall architecture illustrated in Figure 2 . The DiKE framework comprises two core components: (1) Knowledge Representation Disentanglement (KRD) , which explicitly disentangles the subject representation into target-knowledge-related and -unrelated components within the LLM’s representation space, and (2) Disentanglement-based Knowledge Edit (DKE) , which injects target knowledge into specific parameters using the disentangled representations while preserving the fine-grained irrelevant knowledge. 
 
 
 Figure 2: Overview of the DiKE architecture. The framework operates in two distinct phases. (Left) KRD Training: The module extracts subject and relation representations from the LLM and learns to disentangle them into target-knowledge-related and -unrelated components via optimizing disentanglement, constraint, and reconstruction objectives. (Right) DKE Editing: During the editing phase, the pre-trained Disentangler is frozen. The DKE module utilizes the disentangled representations to derive a closed-form rank-one parameter update (Eq. ( 19 )), which injects new knowledge into the target-related component while explicitly constraining the unrelated component to preserve fine-grained irrelevant knowledge. Note that the KRD module is pre-trained on the training set and does not require retraining for subsequent editing tasks. 
 
 



## SECTION: 4 Experiments



 
 In this section, we first introduce our newly constructed dataset, FINE-KED , designed to evaluate the impact of editing on fine-grained irrelevant knowledge. To provide a more comprehensive assessment of our DiKE’s performance in gereral editing scenarios, we further evaluate DiKE on the widely used CounterFact and Mquake-3K benchmarks across GPT2-XL (1.5B), GPT-J (6B), and LLaMA3 (8B). More detailed experimental results are provided in Appendix  G . 
 
 



## SECTION: 4.1 FINE-KED Dataset



 
 Table 1: Relation Examples in Different Levels of FINE-KED 
 
 
 Level 
 Relations 
 
 Easy 
 The name of the child of {} is 
 
 The name of the award {} won is 
 
 Middle 
 The place of death of {} is 
 
 The place of birth of {} is 
 
 Hard 
 The name of the head of state of {} is 
 
 The name of the capital city of {} is 
 
 
 
 FINE-KED is designed to evaluate the impact of editing methods on fine-grained irrelevant knowledge. For each edit sample ( s , r , o ) (s,r,o) , we construct fine-grained irrelevant knowledge ( s , r ′ , o ′ ) (s,r^{\prime},o^{\prime}) and categorize the dataset into three levels: Easy , Middle , and Hard , based on the semantic relatedness between relation r r and r ′ r^{\prime} (examples of these levels are provided in Table 1 ). We employ Efficacy to quantify the success rate of edits and Relational Locality to assess the preservation of fine-grained irrelevant knowledge. Detailed information is provided in Appendix D.1 . 
 
 
 



## SECTION: 4.2 Experimental Setups



 
 Datasets and Evaluation Metrics. 
In addition to FINE-KED , we conduct experiments on COUNTERFACT ( Meng et al., 2022 ) , a benchmark designed to evaluate the insertion of counterfactual knowledge into LLMs. Performance is assessed using three key metrics: Efficacy Score , Paraphrase Score , and Neighborhood Score . Further details are in Appendix D.2 . To further investigate DiKE’s generalization capability in more complex scenarios, we also evaluate on the multi-hop reasoning dataset MQuAKE-3K Zhong et al. (2023) . Dataset descriptions are provided in Appendix D.3 , with corresponding results reported in Appendix G.2 . 
 
 
 Baselines. 
Our experiments are conducted on three LLMs: GPT2-XL (1.5B) ( Radford et al., 2019 ) , GPT-J (6B) ( Wang and Komatsuzaki, 2021 ) and LLaMA3 (8B) ( Dubey et al., 2024 ) .
We compare our method with a number of knowledge editing methods: Fine-Tuning (FT) ( Zhu et al., 2020 ) , MEND ( Mitchell et al., 2022 ) , ROME ( Meng et al., 2022 ) , MEMIT ( Meng et al., 2023 ) , and AlphaEdit ( Fang et al., 2025 ) . To further validate the superiority of DiKE in preserving the fine-grained irrelevant knowledge, we compare it with two variant models ROME-C and MEMIT-C on FINE-KED , which directly incorporate multiple additional relational constraints ( s , r i , o i ) (s,r_{i},o_{i}) into the LLM in each editing. The implementation details of baselines and DiKE in Appendix F.1 . 
 
 
 



## SECTION: 4.3 Experiment Results



 
 Through these experiments, we aim to address the following key research questions: 
 
 
 How does DiKE Perform in Preserving Fine-grained knowledge? To avoid performance inflation due to data leakage and to verify the generalization capability of our KRD module, we ensure minimal subject overlap between the KRD training data and the evaluation datasets. Specifically, the subject overlap rates between the KRD module’s training set and the edited samples in FINE-KED and COUNTERFACT are only 1.39% and 6.33%, respectively. A detailed investigation of the generalization behavior of the KRD module is provided in Appendix  G.6 . 
 
 
 Table 2: Performance comparison on FINE-KED in terms of Efficacy (%) and Relational Locality (%). The best performance is highlighted in boldface , and the second-best is underlined . 
 
 
 
 Method 
 Eff. 
 R-Loc. (GPT2-XL) 
 Eff. 
 R-Loc. (GPT-J) 
 Eff. 
 R-Loc. (LLaMA-3) 
 
 Easy 
 Mid. 
 Hard 
 Avg. 
 Easy 
 Mid. 
 Hard 
 Avg. 
 Easy 
 Mid. 
 Hard 
 Avg. 
 
 BASE 
 20.4 
 62.7 
 65.7 
 71.9 
 65.8 
 21.7 
 86.9 
 87.6 
 89.2 
 87.6 
 23.9 
 81.1 
 80.3 
 81.3 
 80.9 
 
 FT 
 99.1 
 46.8 
 45.0 
 40.9 
 44.9 
 100 
 69.2 
 64.8 
 60.6 
 65.9 
 100 
 69.4 
 63.0 
 49.6 
 62.8 
 
 MEND 
 94.2 
 47.1 
 47.5 
 31.5 
 43.4 
 98.7 
 71.7 
 66.5 
 51.8 
 65.4 
 94.3 
 71.5 
 63.4 
 54.7 
 65.2 
 
 ROME 
 91.8 
 48.3 
 45.4 
 56.3 
 49.5 
 99.9 
 53.5 
 49.4 
 44.9 
 50.3 
 99.8 
 56.8 
 50.7 
 47.8 
 53.0 
 
 ROME-C 
 91.7 
 49.7 
 46.7 
 57.4 
 50.8 
 99.9 
 63.3 
 58.3 
 59.4 
 61.0 
 99.9 
 65.5 
 57.9 
 60.9 
 62.3 
 
 MEMIT 
 90.8 
 49.0 
 45.0 
 55.9 
 49.6 
 99.9 
 61.9 
 56.0 
 59.5 
 59.7 
 98.7 
 64.6 
 54.9 
 62.6 
 61.5 
 
 MEMIT-C 
 91.0 
 49.5 
 45.5 
 55.3 
 49.8 
 99.8 
 67.3 
 62.3 
 67.1 
 65.9 
 97.2 
 68.1 
 60.3 
 69.2 
 66.3 
 
 AlphaEdit 
 98.7 
 47.3 
 43.9 
 47.4 
 46.4 
 99.9 
 59.8 
 54.9 
 54.8 
 57.2 
 98.2 
 68.1 
 59.2 
 67.8 
 65.6 
 
 DiKE 
 97.4 
 54.2 
 51.8 
 60.2 
 55.0 
 99.1 
 72.0 
 67.4 
 74.1 
 71.3 
 99.1 
 72.7 
 65.3 
 72.4 
 70.6 
 
 Improve 
 - 
 9.1% 
 9.1% 
 4.9% 
 8.3% 
 - 
 0.4% 
 1.4% 
 10.4% 
 8.2% 
 - 
 1.7% 
 3.0% 
 4.6% 
 6.5% 
 
 
 
 
 (i) Performance on FINE-KED . 
Table 2 presents the performance of all editors on FINE-KED . From the results, we can draw the following observations: (1) DiKE excels in all evaluations of Relational Locality while maintaining high editing success rate. Specifically, DiKE performs enhancements up to 8.3% on the Relational Locality metric over the baseline model. This demonstrates that fine-grained disentanglement and constraint of target knowledge can effectively mitigate negative impacts on fine-grained unrelated knowledge without compromising editing performance. (2) ROME, MEMIT and AlphaEdit generally perform worse on the Relational Locality compared to DiKE. MEND and FT, demonstrate better performance than ROME and MEMIT on the Easy and Middle levels of FINE-KED . However, their performance declines significantly on the Hard level of the dataset. We believe this is because these models directly manipulate the subject or relation representation to perform parameter updates, which can easily have negative impacts on fine-grained unrelated knowledge that is entangled within the parameters and representations. Although AlphaEdit introduces null-space constraints to preserve unrelated knowledge, the constraint is applied at a coarse-grained level and thus struggles to prevent interference with fine-grained irrelevant knowledge. (3) ROME-C and MEMIT-C, which incorporate additional relational constraints, improve upon their original versions but still fall short of DiKE. This suggests that merely adding constraint samples is insufficient to reliably preserve fine-grained unrelated knowledge. Furthermore, the requirement to manually construct extra constraints for each editing instance introduces substantial overhead. In contrast, DiKE, with its KRD moudle, requires only one-time training process and can be directly applied during subsequent edits without retraining, significantly enhancing editing efficiency. 
 
 
 (ii) Performance on COUNTERFACT. Table 3 presents the performance of all editors on COUNTERFACT. The results show that DiKE achieves competitive results across other key editing evaluation metrics, such as Paraphrase Score and Neighborhood Score. 
 
 
 Table 3: Performance comparison on COUNTERFACT in terms of Efficacy Score, Paraphrase Score, and Neighborhood Score. The Avg. is the harmonic mean of the three metrics. 
 
 
 
 Model 
 Method 
 Avg. 
 Effi. 
 Para. 
 Neigh. 
 
 
 
 
 
 
 GPT-J (6B) 
 
 
 BASE 
 23.8 
 16.2 
 19.2 
 81.0 
 
 FT 
 24.4 
 100.0 
 95.8 
 9.8 
 
 MEND 
 62.2 
 97.7 
 53.2 
 52.1 
 
 ROME 
 90.3 
 99.9 
 99.7 
 75.9 
 
 MEMIT 
 90.4 
 99.6 
 95.2 
 79.2 
 
 AlphaEdit 
 91.0 
 99.6 
 96.9 
 79.3 
 
 
 DiKE 
 90.8 
 99.8 
 96.1 
 79.3 
 
 
 
 
 
 
 LLaMA3 (8B) 
 
 
 BASE 
 14.1 
 9.2 
 10.9 
 85.9 
 
 FT 
 18.4 
 100.0 
 97.7 
 7.0 
 
 MEND 
 58.4 
 100.0 
 73.6 
 36.0 
 
 ROME 
 90.8 
 100.0 
 98.9 
 77.3 
 
 MEMIT 
 91.1 
 99.8 
 94.6 
 80.9 
 
 AlphaEdit 
 89.7 
 100.0 
 93.5 
 78.5 
 
 
 DiKE 
 92.4 
 99.9 
 96.6 
 82.8 
 
 
 
 
 These findings suggest that the disentanglement-based approach, DiKE, not only effectively preserves fine-grained irrelevant knowledge but also maintains strong generalization ability and better retention of unrelated neighborhood knowledge. 
 
 
 How do Different Components Affect the DiKE Performance? 
To investigate the effectiveness of each component in DiKE, we conduct an ablation study on LLaMA3 using the following variants: w/o CTR, which removes knowledge disentangling loss from the KRD module; w/o KC, which excludes knowledge constraint loss from KRD module; w/o TKE, which performs editing directly on the original representations rather than the disentangled ones; and w/o FIK, which removes the constraint for preserving fine-grained irrelevant knowledge in the DKE module. Figure  4 presents the experimental results on FINE-KED , leading to the following conclusions: (1) DiKE outperforms w/o CTR and w/o KC on most Relational Locality metrics, confirming that contrastive learning and knowledge constraint contribute to effective disentanglement. (2) Compared with DiKE, w/o TKE exhibits a substantial performance drop, underscoring the importance of disentangling and editing the target-knowledge-related representation rather than the original entangled one. (3) Compared with w/o FIK, DiKE further improves on Relational Locality, especially in middle and hard level, demonstrating the benefit of explicitly enforcing invariance on the disentangled target-knowledge-unrelated representation. Experimental results on GPT2-XL and GPT-J are shown in Figure 8 . 
 
 
 
 
 
 Figure 3: Ablation studies on FINE-KED in terms of Efficacy and Relational Locality. 
 
 
 Figure 4: Performance of subject-consistent batch editing on the FINE-KED . 
 
 
 
 Which Scenarios Benefit from the DiKE Approach? To further validate the importance of representation-disentanglement-based editing in preserving fine-grained irrelevant knowledge, we conduct a subject-consistent batch editing experiment where all edit samples within a batch share the same subject. This setup exerts a stronger influence on the subject’s representation, making the task significantly more challenging than conventional batch editing settings, in which edit samples are typically unrelated. We evaluate performance on FINE-KED under batch sizes of 1, 2, 4, and 8, with results shown in Figure  4 . 
 
 
 We observe that DiKE achieves an Efficacy Score close to 100% across most models and batch settings, while maintaining the highest Relational Locality Score. By contrast, ROME exhibits a sharp degradation as batch size increases. Although MEMIT and AlphaEdit incorporate mechanisms for batch editing and irrelevant knowledge preservation, respectively, their improvements in Relational Locality under larger batch settings remain significantly lower than those of DiKE. This advantage arises because DiKE explicitly disentangles subject representations across different relations, thereby isolating relation-specific knowledge and minimizing interference. As a result, edits to one relation have little impact on other knowledge associated with the same subject. By contrast, ROME, MEMIT, and AlphaEdit directly update entangled subject representations, where overlapping relational information leads to conflicts, imprecise updates, and reduced effectiveness. Furthermore, AlphaEdit constrains only coarse-grained irrelevant knowledge, making it less effective at preserving fine-grained relational distinctions within subject representations. We also find that MEND suffers from a significant performance drop in this setting, which may be attributed to its reliance on a hypernetwork to predict parameter updates based on gradients. When editing a batch of knowledge instances sharing the same subject, the predicted gradients are more likely to conflict with each other, resulting in editing failures. 
 
 
 
 



## SECTION: Appendix D Details of Datasets & Evaluation Metrics



 



## SECTION: Appendix F Implementation Details and Scalability Analysis



 



## SECTION: F.2 Scalability Analysis



 
 This section analyzes the scalability of DiKE from multiple perspectives, including parameter efficiency, batch processing behavior, editing cost, and empirical runtime performance. 
 
 
 Fixed Parameter Efficiency. The Knowledge Representation Disentanglement (KRD) module is designed to be lightweight, consisting solely of fixed projection matrices ( 𝐖 1 \mathbf{W}_{1} to 𝐖 4 \mathbf{W}_{4} in Eq. ( 5 )). As described in the methodology (§ 3.1 ), the module operates on the subject representation 𝐡 s \mathbf{h}_{s} and relation representation 𝐡 r \mathbf{h}_{r} , which are extracted from the last-token hidden states of the subject s s and the prompt p ⁡ ( s , r ) p(s,r) at a specific transformer layer. Importantly, the KRD module does not store subject-specific or relation-specific parameters. Its parameter size therefore remains constant regardless of the number of edited facts, ensuring stable memory usage even as the scale of the underlying knowledge grows. 
 
 
 Batch Scalability Inherited from MEMIT. 
DiKE retains the robust computational structure and batch scalability of MEMIT. By comparing MEMIT’s solution (Eq. ( 4 )) with DiKE’s closed-form solution (Eq. ( 19 )), it is evident that both methods explicitly solve a least-squares problem for the parameter update. The core computational load is therefore identical. The only additional step introduced by DiKE is the calculation of the disentangled target value 𝐯 ∗ \mathbf{v}^{*} via the KRD operation. Since this operation involves only a single forward pass through lightweight matrices ( 𝐖 1 \mathbf{W}_{1} to 𝐖 4 \mathbf{W}_{4} ), the added time complexity is negligible. Therefore, theoretically, DiKE inherits the same batch processing capabilities and scalability properties as MEMIT. 
 
 
 Amortized Training Cost. 
The training of the KRD module constitutes a one-time offline pre-training phase. Once trained, the module is frozen and can be directly applied to any subsequent editing process without requiring retraining or fine-tuning for individual edit samples. This decoupling of training and inference ensures that the online editing latency remains minimal. 
 
 
 Empirical Efficiency Analysis. 
To empirically assess runtime efficiency, we conduct DiKE, MEMIT, and AlphaEdit under varying batch sizes on LLaMA-3 following the configuration used in Figure  4 . Table  8 reports the average runtime for each method across different batch sizes. Across all settings, DiKE exhibits only a small and nearly constant overhead (approximately 2–4 seconds) compared to the baselines. These results indicate that the disentanglement computation introduced by KRD does not form a performance bottleneck and that DiKE maintains stable runtime behavior as the batch size increases. 
 
 
 
 



## SECTION: Appendix G Additional Experiments



 



## SECTION: G.5 Visualization Analysis of Disentangled Representations



 
 To intuitively demonstrate the disentanglement capability of the KRD module, we conduct a visualization experiment to validate its effectiveness. Specifically, we randomly sample 1,000 edit instances from the FINE-KED dataset and extract the corresponding target-knowledge-related and target-knowledge-unrelated representations produced by the KRD module. We then project these high-dimensional representations into a two-dimensional space using t-SNE. As illustrated in Figure  7 , the two types of representations form distinct clusters, indicating that the KRD module effectively disentangles semantically independent components within the subject representation space. 
 
 
 Table 11: Performance comparison on FINE-KED under different In-Distribution (ID) and Out-of-Distribution (OOD) settings. 
 
 
 
 Setting 
 Method 
 Effi. 
 R-Loc.(Easy) 
 R-Loc (Mid.) 
 R-Loc (Hard) 
 
 
 
 
 Sub-ID & Rel-ID 
 
 ROME 
 99.7 
 47.6 
 49.9 
 35.0 
 
 MEMIT 
 99.5 
 62.4 
 58.1 
 65.8 
 
 AlphaEdit 
 98.0 
 61.3 
 52.6 
 61.2 
 
 DiKE 
 99.3 
 65.2 
 70.5 
 70.8 
 
 
 
 
 Sub-ID & Rel-OOD 
 
 ROME 
 100.0 
 59.8 
 52.2 
 34.1 
 
 MEMIT 
 97.2 
 66.9 
 50.1 
 50.9 
 
 AlphaEdit 
 94.3 
 75.0 
 62.2 
 58.6 
 
 DiKE 
 98.7 
 77.4 
 60.0 
 61.1 
 
 
 
 
 Sub-OOD & Rel-ID 
 
 ROME 
 99.9 
 56.7 
 50.0 
 50.7 
 
 MEMIT 
 98.8 
 65.1 
 53.8 
 64.1 
 
 AlphaEdit 
 98.7 
 67.8 
 58.8 
 66.8 
 
 DiKE 
 99.0 
 72.3 
 64.1 
 73.1 
 
 
 
 
 Sub-OOD & Rel-OOD 
 
 ROME 
 99.7 
 57.1 
 54.2 
 46.0 
 
 MEMIT 
 98.6 
 64.3 
 60.0 
 61.5 
 
 AlphaEdit 
 97.8 
 68.3 
 61.6 
 69.3 
 
 DiKE 
 99.2 
 73.0 
 70.3 
 72.2 
 
 
 
 
 



## SECTION: G.6 Generalization analysis of KRD Module



 
 To provide a more fine-grained and rigorous assessment of the KRD module’s generalization capabilities, we split the evaluation samples of FINE-KED into four groups based on whether their subjects and relations appeared in the KRD pre-training data: (a) Sub-OOD & Rel-OOD: both subject and relation unseen; (b) Sub-OOD & Rel-ID: unseen subjects, seen relation types; (c) Sub-ID & Rel-OOD: seen subjects, unseen relation types; (d) Sub-ID & Rel-ID: both seen during pre-training. 
 
 
 The comparative results are summarized in Table  11 . As observed, DiKE consistently outperforms baseline editors across all settings. Notably, in the most challenging Sub-OOD & Rel-OOD subset, DiKE achieves a Relational Locality (Hard) score of 72.2%, significantly surpassing ROME (46.0%) and MEMIT (61.5%). This confirms that the KRD module maintains strong disentanglement capabilities even when encountering entirely new knowledge patterns. 
 
 
 

