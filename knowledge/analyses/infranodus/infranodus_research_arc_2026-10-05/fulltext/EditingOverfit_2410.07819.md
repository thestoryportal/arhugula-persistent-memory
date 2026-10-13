# EditingOverfit — arXiv 2410.07819

Source: https://arxiv.org/html/2410.07819

## Headings
# Uncovering Overfitting in Large Language Model Editing
## 1 Introduction
## 2 Related Work
## 3 Preliminary Experiments
### 3.1 Metric Definitions
### 3.2 Editing Overfit Phenomenon
## 4 Analysis on Editing Overfit
### 4.1 EVOKE Benchmark
### 4.2 Results & Findings
## 5 Analysis on Mitigation Techniques
#### Mitigation Technique 1: Norm Constraints
#### Mitigation Technique 2: Batch Editing
#### Mitigation Technique 3: Data Augmentation
## 6 Proposed Mitigation Strategy: Learn the Inference
### 6.1 Reasoning Mechanisms in LLMs: Background and Rationale
### 6.2 Multi-stage Inference Constraints
### 6.3 Experiments
#### How Effective is LTI in Mitigating the Editing Overfit Problem?
#### How do Constraints at Different Stages of LTI Influence Overfitting?
## 7 Conclusion
## Acknowledgements
## References
## Appendix A Limitations
## Appendix B Detailed related work
## Appendix C Details on the EVOKE Benchmark
#### Dataset Construction
## Appendix D Experimental Setup Details
### D.1 Baseline Methods
### D.2 Details on Multi-layer Editing Experiment
### D.3 Details on Data Augmentation Experiment
## Appendix E Method Implementation Details
#### Design of the Contextual Prompt
#### Layer Selection for the Subject Representation Constraint
#### Other Hyperparameter Settings
## Appendix F Rank-One Model Editing
## Appendix G Results on Llama-2-7B
## Appendix H Analysis on Distributing Weight Updates Across Layers
## Appendix I The impact of Constraint Layers
## Appendix J Case Study
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 27, "held-out": 0, "held out": 0, "generaliz": 2, "multi-token": 0, "multi token": 0, "unseen": 0, "novel entit": 0, "counterfact": 11, "zsre": 0, "teacher forc": 0, "autoregressive": 1, "first token": 0, "subject": 54, "last token": 2, "embedding": 1, "vocabulary": 0}


## SECTION: 3 Preliminary Experiments



 
 To investigate the causes of edited LLMs’ poor performance on complex tasks, we begin by analyzing the outputs of the edited models on a representative multi-hop reasoning dataset, CounterfactPlus ( Yao et al., 2023 ) , where each entry contains an edited knowledge e = ( s , r , o , o ∗ ) e=(s,r,o,o^{*}) along with a multi-hop question q = ( s , r , r ′ ) q=(s,r,r^{\prime}) that requires reasoning based on the edited sample. 
 
 



## SECTION: 3.1 Metric Definitions



 
 To perform a fine-grained analysis of the outputs from edited models, we define several metrics in response to complex prompts, such as multi-hop questions within the dataset. Specifically, for each edit sample e = ( s , r , o , o ∗ ) e=(s,r,o,o^{*}) , when the edited LLM is presented with a prompt consisting of a complex question, it may produce one of the following outputs: the original answer to the complex question, the correct answer, or the edited target o ∗ o^{*} . Accordingly, we define the following metrics: 
 
 • 
 
 Correct Answer Probability (CAP) : The probability that the model generates the correct answer 𝚊𝚗𝚜 \verb+ans+ for a given 𝚙𝚛𝚘𝚖𝚙𝚝 \verb+prompt+ , formalized as ℙ ⁡ ( 𝚊𝚗𝚜 ∣ 𝚙𝚛𝚘𝚖𝚙𝚝 ) \mathbb{P}\left(\verb+ans+\mid\verb+prompt+\right) . 
 
 • 
 
 Original Answer Probability (OAP) : The probability that the model outputs the original answer 𝚘𝚛𝚒 \verb+ori+ (before editing) in response to the given 𝚙𝚛𝚘𝚖𝚙𝚝 \verb+prompt+ , defined as ℙ ⁡ ( 𝚘𝚛𝚒 ∣ 𝚙𝚛𝚘𝚖𝚙𝚝 ) \mathbb{P}\left(\verb+ori+\mid\verb+prompt+\right) . 
 
 • 
 
 Direct Probability (DP) : The likelihood that the model produces the edit target o ∗ o^{*} , expressed as ℙ ⁡ ( o ∗ ∣ 𝚙𝚛𝚘𝚖𝚙𝚝 ) \mathbb{P}\left(o^{*}\mid\verb+prompt+\right) . 
 
 
 
 
 To further evaluate the influence of both the target edit o ∗ o^{*} and the original answer 𝚘𝚛𝚒 \verb+ori+ on the correct answer 𝚊𝚗𝚜 \verb+ans+ , we follow Meng et al. (2022a) and define two additional comprehensive metrics to gauge the model’s overall editing effectiveness: 
 
 
 
 • 
 
 Editing Overfit Score (EOS) : This metric evaluates the performance of the edited model on complex questions where the correct answer is not o ∗ o^{*} . It serves as a primary indicator of the model’s overfitting and overall performance. The score is calculated as the proportion of cases where the model overfits by favoring the edit target o ∗ o^{*} over the correct answer 𝚊𝚗𝚜 \verb+ans+ , formalized as 𝔼 [ 𝕀 [ ℙ ( 𝚊𝚗𝚜 ∣ 𝚙𝚛𝚘𝚖𝚙𝚝 ) > ℙ ( o ∗ ∣ 𝚙𝚛𝚘𝚖𝚙𝚝 ) ] ] \mathbb{E}\left[\mathbb{\mathbb{I}}[\mathbb{P}\left(\verb+ans+\mid\verb+prompt+\right)>\mathbb{P}\left(o*\mid\verb+prompt+\right)]\right] . 
 
 • 
 
 Answer Modify Score (AMS) : This metric evaluates the negative interference of old knowledge on the correct answers. It is assessed by calculating the proportion of cases where the probability of the correct answer exceeds that of the original answer, defined as 𝔼 [ 𝕀 [ ℙ ( 𝚊𝚗𝚜 ∣ 𝚙𝚛𝚘𝚖𝚙𝚝 ) > ℙ ( 𝚘𝚛𝚒 ∣ 𝚙𝚛𝚘𝚖𝚙𝚝 ) ] ] \mathbb{E}\left[\mathbb{\mathbb{I}}[\mathbb{P}\left(\verb+ans+\mid\verb+prompt+\right)>\mathbb{P}\left(\verb+ori+\mid\verb+prompt+\right)]\right] . 
 
 
 
 
 



## SECTION: 4 Analysis on Editing Overfit



 
 To further investigate the severity of Editing Overfit in edited LLMs, we construct EVOKE , a new benchmark designed to analyze overfitting phenomena across various tasks. We then assess the performance of different editing methods using this benchmark and examine the effectiveness of several existing mitigation strategies
in reducing Editing Overfit. 
 
 



## SECTION: 4.1 EVOKE Benchmark



 
 EVOKE comprises Recall Tasks and Overfit Tasks, covering six tasks in total. The Recall Tasks assess the edited model’s ability to recall new edited knowledge, including Efficacy and Paraphrase evaluation. The Overfit Tasks pose complex challenges that are prone to inducing overfitting in editing methods, including Multi-hop Reasoning , Prefix Distraction , Subject Specificity , and Relation Specificity . These tasks are specifically designed to evaluate the model’s capability to utilize newly integrated knowledge for more challenging scenarios, with a particular emphasis on examining the degree of Editing Overfit. Details of EVOKE construction can be found in Appendix C . 
 
 
 Taking the edit “ Microsoft is founded by Bill Gates → \rightarrow Steve Jobs ” as an example, we introduce the recall tasks used to assess editing success rate of the edit ( Meng et al., 2022a ; Yao et al., 2023 ) : 
 
 • 
 
 Efficacy directly validates whether the edited models can recall the new edited knowledge ( s , r , o ∗ ) (s,r,o^{*}) under the editing prompt p ⁡ ( s , r ) p(s,r) . In the context of the above example, the model would be asked: “ Who is the founder of Microsoft? ” 
 
 • 
 
 Paraphrase examines the model’s ability of recall the new knowledge ( s , r , o ∗ ) (s,r,o^{*}) using paraphrased forms of the editing prompt p ⁡ ( s , r ) p(s,r) . For instance, it might ask:“ Who established Microsoft? ” 
 
 
 
 
 The design of overfit tasks are based on the two principles: First, the input questions explicitly or implicitly contain the information of subject s s or relation r r to induce potential overfitting responses from the model; Second, the correct answers to these questions are entirely unrelated to o ∗ o* , making it easier to determine whether the edited model exhibits overfitting. Accordingly, the overfit tasks are constructed as follows: 
 
 
 
 • 
 
 Multi-hop Reasoning evaluates the edited model’s ability to integrate the newly edited knowledge with existing knowledge to correctly answer questions spanning multiple entities or relations. For example, “ Which university did the founder of Microsoft attend? ” These questions typically contain implicit subject s s and relation r r information from the edit sample, but the answer is not the target o ∗ o^{*} . They are well-suited for evaluating whether the edited model has overfit to the p ⁡ ( s , r ) → o ∗ p(s,r)\rightarrow o^{*} pattern. A model that has overfit to this pattern might incorrectly produce ‘Steve Jobs’ as the answer to this question. 
 
 • 
 
 Prefix Distraction uses the new knowledge ( s , r , o ∗ ) (s,r,o^{*}) as a perfix for unrelated questions, evaluating weather the edited model can still provide the original correct answer. For example: “ Microsoft was founded by Steve Jobs. Who is the founder of Amazon? ” This evaluation also assess weather the edited model has overfit to the p ⁡ ( s , r ) → o ∗ p(s,r)\rightarrow o^{*} pattern, providing a more explicit measure compared to multi-hop reasoning. 
 
 • 
 
 Subject Specificity presents questions with the same subject s s as the edit sample but with different relations r ′ r^{\prime} . For example: “ When was Microsoft founded? ” These questions typically contain information about the subject s s , but the correct answer is not the target o ∗ o^{*} , making them ideal for evaluating whether the edited model has overfit to the s → o ∗ s\rightarrow o^{*} pattern. 
 
 • 
 
 Relation Specificity includes questions with different subjects s ′ s^{\prime} from the edit sample but the same relation r r , such as: “Who is the founder of Amazon?” These questions contain information about the relation r r , but the answer is not the target o ∗ o^{*} . They are used to evaluate whether the model has overfit to the r → o ∗ r\rightarrow o^{*} pattern. This task also corresponds to the locality evaluation in Counterfact ( Meng et al., 2022a ) . 
 
 
 
 
 The recall task is evaluated using the AMS metric. For the multi-hop reasoning task, we employ all five metrics defined in Section 3.1 for a comprehensive analysis. In the Prefix Distraction, Subject Specificity, and Relation Specificity tasks, the correct answer is identical to the original answer, making OAP equivalent to CAP, with the EOS metric used to evaluate performance in these tasks. 
 
 
 



## SECTION: 4.2 Results & Findings



 
 To assess the extent of Editing Overfit in current methods, we employ FT, FT-L, MEND, ROME, and MEMIT to edit GPT-J ( Wang & Komatsuzaki, 2021 ) , GPT-2 XL ( Radford et al., 2019 ) and Llama-2-7B ( Touvron et al., 2023 ) . We evaluate the pre- and post-edit performance of these models on EVOKE . Results for Recall and Overfit Tasks on GPT-J and GPT-2 XL are shown in Tables 1 and 2 , while results for Llama-2-7B are presented in Appendix G . Based on these, we summarize our key findings as follows: 
 
 
 Finding 1: Current editing methods widely lead to severe overfitting. As shown in Table 1 , nearly all successfully edited models exhibit significantly higher direct probability (DP) scores across the four overfit tasks compared to the unedited model. Notably, the average DP for FT, ROME and MEMIT on most overfit tasks significantly surpasses the correct answer probability (CAP), with elevated EOS values indicating that this issue persists across many edited samples. Although FT-L and MEND show better overfitting metrics, their significantly lower paraphrase scores suggest that the edits were unsuccessful (as shown in Table 2 ), rendering their overfitting scores less meaningful. It is crucial to highlight that all editing methods exhibit a very high probability of incorrectly outputting the edit target o ∗ o^{*} (high DP score) in the prefix distraction task, with EOS scores also abnormally low. This may be attributed to the fact that the Prefix Distraction task explicitly introduces distracting new knowledge ( s , r , o ∗ ) (s,r,o^{*}) prepended to the input. These results provide clear evidence supporting that existing editing paradigm is prone to causing overfitting. 
 
 
 Table 1: Experimental results for different models on the Overfit Tasks of EVOKE . 
 
 
 
 
 
 Editor 
 Prefix Distraction 
 Multi-hop Reasoning 
 Subject Specificity 
 Relation Specificity 
 
 DP↓ 
 CAP↑ 
 EOS↑ 
 DP↓ 
 OAP↓ 
 CAP↑ 
 EOS↑ 
 AMS↑ 
 DP↓ 
 CAP↑ 
 EOS↑ 
 DP↓ 
 CAP↑ 
 EOS↑ 
 
 GPT-2 XL 
 5.01 
 13.30 
 54.58 
 0.27 
 7.87 
 4.21 
 93.43 
 35.64 
 0.50 
 4.90 
 85.59 
 0.33 
 6.42 
 79.61 
 
 FT 
 22.97 
 9.05 
 23.40 
 4.57 
 4.10 
 7.06 
 75.91 
 66.91 
 2.80 
 4.20 
 51.31 
 11.99 
 5.07 
 40.81 
 
 FT-L 
 12.87 
 11.00 
 40.09 
 1.60 
 7.13 
 6.19 
 87.71 
 50.97 
 0.63 
 4.47 
 77.07 
 2.91 
 6.31 
 70.12 
 
 MEND 
 46.57 
 1.93 
 17.88 
 3.27 
 4.75 
 7.42 
 83.82 
 40.15 
 10.37 
 4.62 
 36.03 
 11.99 
 5.43 
 44.65 
 
 ROME 
 44.99 
 6.62 
 15.22 
 23.32 
 3.43 
 11.76 
 46.11 
 75.67 
 35.39 
 2.60 
 21.83 
 1.01 
 6.47 
 77.23 
 
 ROME-LTI 
 19.53 
 9.88 
 28.17 
 10.08 
 5.12 
 11.03 
 65.94 
 70.83 
 19.05 
 3.92 
 30.79 
 0.61 
 6.49 
 78.04 
 
 MEMIT 
 32.19 
 7.63 
 20.55 
 16.75 
 4.28 
 11.92 
 57.06 
 72.63 
 22.68 
 3.20 
 25.98 
 0.85 
 6.38 
 77.81 
 
 MEMIT-LTI 
 18.76 
 8.78 
 26.02 
 8.05 
 4.97 
 11.40 
 72.02 
 69.59 
 7.39 
 3.50 
 38.21 
 0.62 
 6.28 
 78.79 
 
 GPT-J 
 4.60 
 17.08 
 64.81 
 0.27 
 12.61 
 5.20 
 94.16 
 30.66 
 0.63 
 6.95 
 80.35 
 0.31 
 9.43 
 84.28 
 
 FT 
 77.43 
 3.61 
 4.58 
 42.51 
 8.35 
 8.91 
 25.55 
 73.45 
 37.5 
 0.38 
 61.5 
 56.46 
 3.01 
 9.74 
 
 FT-L 
 7.05 
 17.99 
 56.30 
 3.28 
 10.77 
 9.40 
 85.77 
 49.51 
 0.93 
 6.70 
 77.07 
 1.40 
 9.67 
 80.24 
 
 MEND 
 36.31 
 11.27 
 29.40 
 3.94 
 12.21 
 5.67 
 84.43 
 35.28 
 12.09 
 6.80 
 33.84 
 13.33 
 8.35 
 53.09 
 
 ROME 
 26.13 
 12.62 
 32.57 
 41.03 
 3.65 
 17.96 
 34.91 
 80.92 
 54.15 
 1.80 
 6.77 
 2.51 
 8.41 
 79.64 
 
 ROME-LTI 
 8.93 
 15.48 
 49.73 
 11.12 
 6.43 
 17.17 
 69.83 
 77.43 
 10.18 
 3.52 
 28.38 
 0.73 
 8.68 
 81.86 
 
 MEMIT 
 18.30 
 14.77 
 39.32 
 25.80 
 5.82 
 18.49 
 50.49 
 75.67 
 33.45 
 2.90 
 17.69 
 0.95 
 9.10 
 82.14 
 
 MEMIT-LTI 
 10.98 
 16.43 
 48.56 
 16.35 
 7.17 
 17.01 
 61.44 
 70.31 
 19.96 
 4.18 
 29.91 
 0.64 
 9.22 
 82.84 
 
 
 
 
 
 Table 2: Experimental results (AMS↑ (%)) on the Recall Tasks of EVOKE . 
 
 
 
 Editor 
 GPT-2 XL 
 GPT-J 
 
 Efficacy 
 Paraphrase 
 Efficacy 
 Paraphrase 
 
 BASE 
 19.50 
 22.79 
 13.29 
 15.47 
 
 FT 
 99.90 
 85.94 
 100.00 
 97.73 
 
 FT-L 
 98.93 
 45.64 
 99.81 
 45.44 
 
 MEND 
 92.92 
 57.47 
 96.90 
 54.17 
 
 ROME 
 100.00 
 96.27 
 99.90 
 99.27 
 
 ROME-LTI 
 100.00 
 92.10 
 100.00 
 96.27 
 
 MEMIT 
 99.32 
 92.73 
 100.00 
 95.23 
 
 MEMIT-LTI 
 100.00 
 90.16 
 100.00 
 91.03 
 
 
 
 
 Finding 2: Locate-then-Edit methods exhibits more severe overfitting to the s → o ∗ s\rightarrow o^{*} pattern. As shown in Table 1 , ROME and MEMIT perform similarly to unedited LLMs on the Relation Specificity task across all metrics, indicating minimal overfitting to the r → o ∗ r\rightarrow o^{*} pattern. However, their weaker performance across all metrics on the Subject Specificity task suggests a tendency toward overfiting to the s → o ∗ s\rightarrow o^{*} pattern. This difference may stem from their primary focus on manipulating subject representations to establish the mapping between p ⁡ ( s , r ) p(s,r) and the new target o ∗ o^{*} . Furthermore, ROME and MEMIT significantly improve the CAP metric for the Multihop Reasoning task – indicating better recall of new answers - surpassing other methods despite a persistently high likelihood of overfitting to the Edit Target. These suggest that while locate-then-edit paradigm has limitations, it sill shows promise in enabling edited models to effectively use new knowledge for inferential tasks. 
 
 
 Finding 3: Both Fine-tuning based and Meta-learning based methods exhibit a strong overfitting tendency to s → o ∗ s\rightarrow o^{*} and r → o ∗ r\rightarrow o^{*} patterns. In contrast to Locate-then-edit methods, from Table 1 , we observe similarly high levels of overfitting in both FT-based and MEND methods across the Subject Specificity and Relation Specificity tasks. This significant overfitting in both patterns is likely due to these methods focusing on mapping the entire input p ⁡ ( s , r ) p(s,r) to the target output o ∗ o* during the editing process. Notably, even MEND, which demonstrated lower performance on Paraphrase task and potential underfitting, still exhibited significant overfitting. Another potentially underfitting model, FT-L, shows a reduced overfitting tendency, likely attributable to its Norm Constraints on weight updates. Our subsequent detailed experiments (§ 5 ) will further explore the impact of Norm Constraints on editing success and mitigating Editing Overfit. 
 
 
 
 



## SECTION: 5 Analysis on Mitigation Techniques



 
 The analysis above demonstrates that the current editing paradigm generally leads to overfitting to new knowledge in edited LLMs. To further investigate how existing strategies and different task scenarios influence overfitting, we conduct additional experiments analyzing various techniques. These include Norm Constraint, Batch Editing, Data Augmentation strategies, and Multi-layer Update Distribution (Appendix H ). We primarily focus on several key metrics in the following analysis: Efficacy and paraphrase are evaluated using the AMS metric, while the remaining four overfit tasks are assessed using the EOS metric. 
 
 



## SECTION: 6.3 Experiments



 
 In this section, we evaluate our mitigation strategy by integrating LTI into the MEMIT and ROME methods and applying them to the EVOKE . Building on the experiments from Section 4 , we perform further evaluations to answer the following key questions: 
 
 



## SECTION: Appendix C Details on the EVOKE Benchmark



 
 The EVOKE benchmark is designed to evaluate the effectiveness of knowledge editing methods for LLMs, focusing not only on their ability to accurately recall edited knowledge but also on their performance and potential overfitting across diverse complex reasoning tasks. Notably, part of EVOKE’s data is sourced from existing knowledge editing datasets. We have reorganized and extended datasets including CounterFact ( Meng et al., 2022a ) , CounterFactPlus ( Yao et al., 2023 ) , and RippleEdits-Popular ( Cohen et al., 2024 ) to construct new task-specific data for comprehensive analysis of knowledge editing methods. 
 
 
 Table 3: An Example of the EVOKE dataset 
 
 
 
 Task 
 
 
 Value 
 
 
 
 
 Edit Request 
 
 
 {Spike Hughes} originates from London → \to Philadelphia 
 
 
 Efficacy 
 
 
 {Spike Hughes} originates from (answer: Philadelphia) 
 
 
 Paraphrase 
 
 
 Spike Hughes is native to (answer: Philadelphia) 
 
 
 Subject Specificity 
 
 
 The profession of Spike Hughes is (answer: musician) 
 
 
 Relation Specificity 
 
 
 Max Mosley originates from (answer: London) 
 
 
 Multi-hop Reasoning 
 
 
 What famous food is associated with the city where Spike Hughes originates from? (answer: Cheesesteaks) 
 
 
 Prefix Distraction 
 
 
 Spike Hughes originates from Philadelphia. Max Mosley originates from (answer: London) 
 
 
 
 
 
 Each entry in EVOKE consists of a counterfactual Edit Request, an Efficacy Prompt, several Paraphrase prompts for recall tasks, and corresponding questions and answers for the four Overfit Tasks: Multi-hop Reasoning, Prefix Distraction, Relation Specificity, and Subject Specificity. Tables 3 and 4 provide task examples and summarize the statistical composition of EVOKE , respectively. 
 
 



## SECTION: Dataset Construction



 
 We construct EVOKE , a comprehensive dataset for evaluating overfitting in LLMs based on edits, by extending and refining existing benchmark data. The edit requests and recall task data in EVOKE are sourced from established benchmarks, including RippleEdits-Popular and CounterFact , specifically leveraging a subset of their test splits. 
 
 
 For Multi-hop Reasoning task, we augment the existing dataset by incorporating newly constructed data. Specifically, Building upon the CounterFactPlus dataset, which lacks original answers for multi-hop questions, we generate the missing answers using GPT-4o, following the methodology used in ( Yao et al., 2023 ) . We validate that these answers can be correctly recalled by the unedited GPT-J model, ensuring they accurately reflect the model’s typical responses. Furthermore, we address potential data leakage caused by implicit answer category constraints in some prompts, where unedited models might predict new-fact-based multi-hop answers with high probability.
To mitigate this, we use GPT-4o to rephrase prompts and reduce biases, creating a more robust evaluation. We ensure transparency by reporting the performance of the unedited base model on this modified dataset. 
 
 
 Table 4: Composition statistics of EVOKE 
 
 
 
 Type 
 Total 
 
 
 
 Edit Requests 
 1489 
 
 Efficacy Prompts 
 1489 
 
 Paraphrase Prompts 
 2062 
 
 Subject Specificity Prompts 
 458 
 
 Relation Specificity Prompts 
 10310 
 
 Multihop Prompts 
 822 
 
 Prefix Distraction Prompts 
 10310 
 
 
 
 
 The remaining tasks in EVOKE , including Relation Specificity, Subject Specificity, and Prefix Distraction, are constructed to target specific aspects of overfitting. Leveraging the locality data from Counterfact , the Relation Specificity task probes the consistency of edited models’ responses across prompts that share the same relation but differ in subject entities. This aligns with the locality metric in traditional knowledge editing datasets, which is used to assess the preservation of unrelated knowledge. We ground the Subject Specificity task in data curated from the RippleEdits-Popular dataset to directly assess overfitting to specific subject entities. For the Prefix Distraction task, we prepend edit requests, in the form of new facts, to the prompts used in the Relation Specificity task, following the approach outlined in Hoelscher-Obermaier et al. (2023) . This construction enables the evaluation of an edited model’s susceptibility to irrelevant information presented as part of the input context. 
 
 
 
 



## SECTION: Appendix D Experimental Setup Details



 
 Our experiments build on the codebase implemented by Meng et al. (2022a) ; Meng et al. (2022b) . For the hyperparameters of MEMIT on GPT-2 XL, we observe significant failures in certain editing cases, with notably lower performance metrics on the recall task compared to GPT-J. To address this, we adjust the hyperparameters, specifically increasing the clamp_norm_factor from 0.75 0.75 to 1.25 1.25 for GPT-2 XL. This adjustment is made to align its editing success rates with those of GPT-J, allowing us to evaluate normal editing performance and potential overfitting. All other baseline implementations, including hyperparameters, remain consistent with the setup of Meng et al. (2022a) ; Meng et al. (2022b) , and hyperparameters on Llama-2-7B remain consistent with Yao et al. (2023) . 
 
 



## SECTION: D.2 Details on Multi-layer Editing Experiment



 
 In Appendix H , we investigate the impact of distributing parameter updates across multiple layers on Editing Overfit, conducting experiments using MEMIT method. The original MEMIT approach, when applied to GPT-J, edited six layers ( l = 3 , 4 , 5 , 6 , 7 , 8 l={3,4,5,6,7,8} ), with the recall vector 𝐯 \mathbf{v} computed at layer 8 8 . In our experiments, we maintain a constant product of the hyperparameter clamp_norm_factor and the number of edited layers. When adjusting the number of layers, we keep the highest edited layer fixed. For example, when editing three layers, we select l = { 6 , 7 , 8 } l=\{6,7,8\} . 
 
 
 



## SECTION: D.3 Details on Data Augmentation Experiment



 
 In Section 5 , we follow existing data augmentation strategy ( Wei et al., 2024 ; Gangadhar & Stratos, 2024 ) to evaluate the effect of data augmentation on Editing Overfit. Specifically, we employ GPT-4o to generate 10 10 data-augmented paraphrase prompts and 10 10 subject specificity prompts for each edit request. Paraphrases are required to be factual statements semantically equivalent to the edited knowledge, while subject specificity prompts are factual statements about the same subject but with different relations. The construction of specificity augmentation prompts aligned with the task test prompts for Subject Specificity, directly enhancing this task. We also utilize GPT-4o to verify and filter out augmented samples that do not meet the requirements. 
 
 
 We test data augmentation effects on MEMIT. The original MEMIT implementation optimized updated parameters by combining the original factual statement with five additional prompts. These prompts are created by appending random prefixes to the original statement, helping the model generalize across contexts. In our paraphrase augmentation experiment, we maintain consistency by optimizing with five randomly prefixed paraphrased prompts. For the specificity augmentation experiment, we add five unrelated facts to the optimization process. This helps suppress the probability of outputting the Edit Target. 
 
 
 
 



## SECTION: Appendix G Results on Llama-2-7B



 
 In this section, we extend our experiments to the Llama-2-7B ( Touvron et al., 2023 ) model using the EVOKE dataset, with results presented in Tables 5 and 6 . Consistent with findings on GPT-2 XL and GPT-J, overfitting patterns persist on this more advanced model: FT continues to overfit to 
 
 
 Table 5: Results (AMS↑ (%)) on the Recall Tasks of EVOKE . 
 
 
 
 Editor 
 Llama-2-7B 
 
 Efficacy 
 Paraphrase 
 
 BASE 
 13.09 
 15.08 
 
 FT 
 99.61 
 92.48 
 
 FT-L 
 92.73 
 21.53 
 
 ROME 
 100.00 
 93.60 
 
 ROME-LTI 
 100.00 
 89.42 
 
 MEMIT 
 100.00 
 96.80 
 
 MEMIT-LTI 
 100.00 
 91.71 
 
 
 
 
 p ( s , r ) → o ∗ p(s,r)\rightarrow o* pattern, while locate-then-edit methods
maintain their overfit pattern to single s → o ∗ s\rightarrow o* mappings. These results further confirm the universality of the Editing Overfit phenomenon. Specifically, nearly all successfully edited models exhibit significantly higher Direct Probability (DP) scores compared to the unedited model. The average DP for FT, ROME, and MEMIT on most overfit tasks significantly surpasses the Correct Answer Probability (CAP), with elevated EOS values indicating persistent issues across edited samples. Notably, both ROME-LTI and MEMIT-LTI show significant improvements in overfitting metrics (DP and EOS) compared to their base versions, demonstrating effective mitigation of Editing Overfit. 
 
 
 Table 6: Experimental results for different models on the Overfit Tasks of EVOKE . 
 
 
 
 
 
 Editor 
 Prefix Distraction 
 Multi-hop Reasoning 
 Subject Specificity 
 Relation Specificity 
 
 DP↓ 
 CAP↑ 
 EOS↑ 
 DP↓ 
 OAP↓ 
 CAP↑ 
 EOS↑ 
 AMS↑ 
 DP↓ 
 CAP↑ 
 EOS↑ 
 DP↓ 
 CAP↑ 
 EOS↑ 
 
 Llama-2-7B 
 16.42 
 28.03 
 58.44 
 1.80 
 21.79 
 9.30 
 86.01 
 28.95 
 0.74 
 42.37 
 97.38 
 1.18 
 21.21 
 82.92 
 
 FT 
 51.48 
 6.11 
 5.61 
 27.71 
 9.26 
 12.21 
 35.40 
 56.20 
 9.74 
 11.03 
 46.07 
 23.12 
 6.30 
 18.83 
 
 FT-L 
 16.90 
 26.29 
 53.17 
 2.59 
 19.47 
 10.96 
 85.16 
 36.13 
 1.12 
 31.62 
 95.20 
 1.54 
 20.14 
 81.08 
 
 ROME 
 22.80 
 25.22 
 46.66 
 21.66 
 9.06 
 24.98 
 63.99 
 77.37 
 21.82 
 15.23 
 45.63 
 2.09 
 20.52 
 81.11 
 
 ROME-LTI 
 17.90 
 27.60 
 53.13 
 15.55 
 11.79 
 23.48 
 70.32 
 71.53 
 14.30 
 18.65 
 57.42 
 1.73 
 20.63 
 81.36 
 
 MEMIT 
 40.76 
 16.90 
 25.36 
 30.47 
 6.05 
 22.29 
 48.18 
 81.75 
 39.09 
 8.93 
 23.36 
 3.87 
 19.47 
 78.08 
 
 MEMIT-LTI 
 26.75 
 20.77 
 36.81 
 14.15 
 10.32 
 21.31 
 67.52 
 74.60 
 9.06 
 10.86 
 47.60 
 2.15 
 19.74 
 80.30 
 
 
 
 
 
 



## SECTION: Appendix H Analysis on Distributing Weight Updates Across Layers



 
 Figure 8: Performance of MEMIT with different editing layers on EVOKE . 
 
 
 Another notable observation from Table 1 is the significant reduction in overfitting exhibited by MEMIT compared to ROME. Both methods follow the locate-then-edit paradigm, but the key difference is that MEMIT distributes updates across multiple layers, whereas ROME concentrates modifications on a single layer.
This distinction motivates further investigate into the impact of distributing weight updates across multiple layers on mitigating overfitting. 
 
 
 We edit GPT-J using MEMIT with varying numbers of modified layers and evaluate the performance of the edited model on EVOKE . The results, shown in Figure 8 , indicate that as the number of layers involved in weight distribution increases, the EOS metric tends to increase, albeit with a slight decline in the model’s paraphrasing capabilities. These findings suggest that distributing weight updates across multiple layers, rather than concentrating them in a single layer, is generally beneficial in mitigating overfitting. 
 
 
 

