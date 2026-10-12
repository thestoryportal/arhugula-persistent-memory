# ATBias — arXiv 2406.12468

Source: https://arxiv.org/html/2406.12468

## Headings
# Adaptive Token Biaser: Knowledge Editing via Biasing Key Entities
## 1 Introduction
## 2 Preliminary
#### LLMs Decoding.
#### Multi-hop Editing.
## 3 Methods
### 3.1 Parametric Induction & Entity Extraction
### 3.2 Probabilistic-Ranking Filter
### 3.3 N-gram and Jaccard Similarity
### 3.4 Adaptive Token Biaser
### 3.5 Knowledge Caching for Efficient Editing
## 4 Experiments
### 4.1 Experimental Setup
#### Tasks.
#### Datasets.
#### Models and Baselines.
#### Implementation.
### 4.2 Overall Performance
### 4.3 One-hop Editing
### 4.4 Editing on Stubborn Knowledge
### 4.5 Latency & Throughput
### 4.6 Why ATBias Edits Efficiently?
### 4.7 Ablation Study
## 5 Related Work
#### Factual Hallucinations.
#### Knowledge Editing.
#### Decoding Strategy.
## 6 Conclusion
## Limitations
## Ethical Considerations
## References
## Appendix A How Can ATBias Be Easily Deployed on MeLLo?
## Appendix B Additional Ablation Study of ATBias
### B.1 N-gram Decomposition
### B.2 Probabilistic Constraint of Filter
### B.3 Ranking Constraint of Filter
### B.4 Bias Coefficient of Knowledge
## Appendix C Prompts of ICE for Experiments
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 0, "held-out": 0, "held out": 0, "generaliz": 0, "multi-token": 0, "multi token": 0, "unseen": 0, "novel entit": 0, "counterfact": 5, "zsre": 0, "teacher forc": 0, "autoregressive": 0, "first token": 1, "subject": 1, "last token": 0, "embedding": 1, "vocabulary": 3}


## SECTION: 3.1 Parametric Induction & Entity Extraction



 
 Extracting key knowledge entities from redundant knowledge information is a fundamental prerequisite of ATBias .
This enables the adjustment of corresponding token probabilities during decoding.
Specifically, ATBias enables the preprocessing to obtain parametric output from LLMs corresponding to each new fact piece in the edit memory.
For example, consider a piece of new fact updated in the edited fact memory: The author Richard Dawkins wrote "Misery" .
By clozing the new fact such as The author _ wrote "Misery" , LLMs can be induced to provide parametric fact outputs like The author Stephen King wrote "Misery" . 
 
 
 Subsequently, the key knowledge entities are individually extracted from these fact pieces.
We define the function extract ​ ( ⋅ ) \text{extract}(\cdot) to represent this process. Given a set of fact pieces f ​ a ​ c ​ t fact , we can obtain a list of split entity strings: 
 
 
 

 
 
 E f ​ a ​ c ​ t = Extract ​ ( f ​ a ​ c ​ t ) E_{fact}=\text{Extract}(fact) 
 
 (2) 
 
 Then, the extracted entities E new E_{\text{new}} and E para E_{\text{para}} from new fact and parametric fact are used to match the key tokens in Section 3.4 . 
 
 
 



## SECTION: 4 Experiments



 



## SECTION: 4.1 Experimental Setup



 



## SECTION: Datasets.



 
 We conduct extensive experiments for the main multi-hop editing task using MQuAKE-3k   ( Zhong et al., 2023 ) along with its challenging derivatives, MQuAKE-2002 and MQuAKE-hard , introduced by  Wang et al. (2024) .
 MQuAKE provides multi-hop knowledge questions to evaluate KE on counterfactual edits.
We also evaluate for one-hop editing task on CounterFact   ( Meng et al., 2022a ) .
Additionally, we follow  ( Bi et al., 2024a ) to use corresponding stubborn datasets to further evaluate the effectiveness of editing stubborn knowledge in Section  4.4 . 
 
 
 
 
 
 
 Model 
 Method 
 MQuAKE-3k 
 MQuAKE-2002 
 MQuAKE-hard 
 
 
 
 LLaMA2- 
 MeLLo  ( Zhong et al., 2023 ) 
 32.6 
 40.8 
 5.1 
 
 7B-chat 
 MeLLo w/ DeCK  ( Bi et al., 2024a ) 
 43.1 
 45.8 
 5.8 
 
 MeLLo w/ ATBias (ours) 
 54.3 
 48.9 
 6.3 
 
 LLaMA2- 
 MeLLo  ( Zhong et al., 2023 ) 
 33.4 
 35.9 
 3.9 
 
 13B-chat 
 MeLLo w/ DeCK  ( Bi et al., 2024a ) 
 36.8 
 38.2 
 6.2 
 
 MeLLo w/ ATBias (ours) 
 48.7 
 43.6 
 6.7 
 
 Mistral- 
 MeLLo  ( Zhong et al., 2023 ) 
 21.8 
 22.8 
 2.1 
 
 7B-instruct 
 MeLLo w/ DeCK  ( Bi et al., 2024a ) 
 21.3 
 22.9 
 2.6 
 
 MeLLo w/ ATBias (ours) 
 24.7 
 25.4 
 3.1 
 
 
 
 Table 2: Experimental results (accuracy; %) on multi-
hop editing task with 500 instances. We conduct the experiments with the full batch size edit memory to evaluate the performance of memory based KE. 
 
 
 



## SECTION: 4.7 Ablation Study



 
 We conducted a comprehensive ablation study on the adaptive constraints, bias coefficients, and key components of ATBias .
Table 6 presents the results for the filter in ATBias , demonstrating the necessity of filtering tokens based on both probability and ranking constraints.
Additional ablation study results can be found in the Appendix B . 
 
 
 
 
 
 Model 
 Prob 
 Rank 
 Prob & Rank 
 
 
 
 LLaMA2-7B 
 90.2 
 81.5 
 93.1 
 
 LLaMA2-13B 
 81.9 
 72.4 
 89.7 
 
 
 Table 6: Ablation study results for the filter of our ATBias . Prob and Rank respectively represent probability and ranking constraints in the filter. 
 
 
 
 



## SECTION: Appendix B Additional Ablation Study of ATBias



 
 We conduct following additional ablation study experiments using the ICE method IKE  ( Zheng et al., 2023 ) with LLaMA2-7B-chat and LLaMA2-13B-chat on the MQuAKE-3k datasets. 
 
 



## SECTION: Appendix C Prompts of ICE for Experiments



 
 The prompt we used in IKE  ( Zheng et al., 2023 ) is shown in 7 , and the prompt we used in MeLLo is shown in 8 .
Based on the provided contextual demonstrations, LLMs can be guided to perform the corresponding ICE methods.
 ATBias can enhance these ICE methods without modifying any prompts. 
 
 
 
 
 
 
 
 Experimental support, please
 view the build logs 
 for errors. Generated by
 
 
 L
 A 
 T
 E 
 
 xml 
 
 .
 
 
 
