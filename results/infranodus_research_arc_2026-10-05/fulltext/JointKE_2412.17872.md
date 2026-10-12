# JointKE — arXiv 2412.17872

Source: https://arxiv.org/html/2412.17872

## Headings
# Joint Knowledge Editing for Information Enrichment and Probability Promotion
## 1 Introduction
## 2 Related Work
### 2.1 Probe into Knowledge Recall Process
### 2.2 Knowledge Editing
## 3 Preliminaries
### 3.1 Language Modeling
### 3.2 Knowledge Editing
## 4 Method
### 4.1 Unveiling Critical Editing Stages
#### The Contrast-Based Probe Approach
### 4.2 Joint Knowledge Editing
#### Joint Editing Procedure
#### Synergistic Optimization
#### Adaptive Updates
## 5 Experiment
### 5.1 Experimental Setup
### 5.2 Adding Factual Knowledge
#### Editing 10k Samples
#### Case Study
### 5.3 Adding Counter-Factual Knowledge
#### Editing 10k Samples
#### Editing Scaling
### 5.4 Ablation Study
## 6 Conclusion
## Acknowledgements
## References
## Appendix
## Appendix A Probe on Knowledge Recall Process
### A.1 Probe on Related Information
### A.2 Probe on Unrelated Information
## Appendix B Analysis of Joint Updates
## Appendix C Benchmark Datasets
### C.1 zsRE Dataset
### C.2 Multi-COUNTERFACT Dataset
## Appendix D Implementation Details
### D.1 Fine-Tuning with Weight Decay (FT-WD)
### D.2 Model Editing Networks with Gradient Decomposition (MEND)
### D.3 Rank-One Model Editing (Rome)
### D.4 Massive Editing for Large Language Model via Meta Learning (MALMEN)
### D.5 Mass-Editing Memory in a Transformer (MEMIT)
### D.6 Precise Model Editing (PMET)
### D.7 Joint Knowledge Editing for Information Enrichment and Probability Promotion (JEEP)
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 2, "held-out": 0, "held out": 0, "generaliz": 15, "multi-token": 0, "multi token": 0, "unseen": 0, "novel entit": 0, "counterfact": 19, "zsre": 17, "teacher forc": 0, "autoregressive": 1, "first token": 2, "subject": 21, "last token": 3, "embedding": 2, "vocabulary": 2}


## SECTION: 5 Experiment



 



## SECTION: 5.1 Experimental Setup



 
 We conduct experiments on two models, GPT-J (6B) ( Wang and Komatsuzaki 2021 ) and LLaMA (7B) ( Touvron et al. 2023 ) , which feature parallel and sequential MHSA and MLP modules, respectively.
Based on the three objectives of knowledge editing, we evaluate three corresponding key metrics: Efficacy Success (ES), Generalization Success (GS) and Locality Success (LS), then compute their harmonic mean Score as in ( Meng et al. 2022b ) (see Appendix C for detailed descriptions).
For baselines, we first consider FT-WD , fine-tuning with weight decay to prevent forgetting ( Zhu et al. 2020 ) . Next, for meta-learning-based methods, we include MEND and its improved version MALMEN , which further supports multiple facts’ editing at once ( Mitchell et al. 2021 ; Tan, Zhang, and Fu 2023 ) . Finally, we compare with locate-then-edit methods: ROME , MEMIT and PMET ( Meng et al. 2022a ; Meng et al. 2022b ; Li et al. 2024 ) . Since ROME originally targets one fact at a time, we adapt it to a sequential version to accommodate massive edits ( Meng et al. 2022b ) . We evaluate editors’ ability to add factual knowledge (§ 5.2 ), and further evaluate the capability to add counterfactual knowledge (§ 5.3 ), which is a more challenging scenario. Implementation details are in Appendix D . 
 
 
 



## SECTION: 5.4 Ablation Study



 
 To elucidate the contributions of updates from different regions and various designs in JEEP, Table 4 presents the results of different ablation variants, editing 10,000 samples from Multi-COUNTERFACT on LLaMA. 
 
 
 OPEN 1 ) 1) Initially, to assess JEEP’s design of dual-region modifications, we examine single-region editing. In w/o δ ′ & \delta^{\prime}\& Step2 and w/o δ ∗ & \mathbf{\delta^{*}\&} Step3 , only one residual vector in Eq. 8 , either δ ∗ \delta^{*} or δ ′ \delta^{\prime} , is computed and used to update the high or low layers respectively. They both underperform compared to JEEP, underscoring the advantage of updating both regions. Notably, editing the lower layers along performs better, suggesting that without the information enrichment from the lower MLP, modifying probability promotion alone is less effective.
Additionally, w/o Step2 or w/o Step3 keeps the simultaneous computation of δ ′ \delta^{\prime} and δ ∗ \delta^{*} , but subsequently updates only one region. This approach considers the interplay between updates but limits the actual modification to one regions. As with previous findings, single-region editing yields inferior results compared to JEEP, with lower-layer editing still shows better outcomes. However, compared to computing only one δ \delta , the dual computations of δ \delta performs worse, suggesting a more holistic consideration of the critical recall stages without corresponding updates may instead harm the editing effect. JEEP improves this by adaptively updating both regions, achieving a more balanced distribution of information changes and superior performance. 
 
 
 OPEN 2 ) 2) Moreover, we ablate the designs in JEEP. Separate Optimization deviates from JEEP’s synergistic design in Eq. 11 , by independently computing δ ′ \delta^{\prime} and updating the low layers before computing δ ∗ \delta^{*} and updating the high layers. Its performance is not only inferior to JEEP but also worse than single-region editing, indicating that isolating the optimization of two regions leads to mutual interference between them. In addition, Even Spread in Step2 replaces the excessive updates to the low layers by spreading the residual errors evenly: r = v i ′ L ′ − h i ′ L ′ L ′ − l ′ + 1 r=\frac{v_{i^{\prime}}^{L^{\prime}}-h_{i^{\prime}}^{L^{\prime}}}{L^{\prime}-l^{\prime}+1} . It performs worse than JEEP, achieving better locality at the cost of efficacy and generalization, but still outperforms updating one region.
Furthermore, considering the computational similarities between W O W_{O} in MLP and MHSA, w/ MHSA in Step3 instead edits MHSA in high layers. Although this adjustment does not outperform JEEP, it shows improved performance over single-region editing, indicating that both MLP and MHSA could promote answer’s probability in the upper layers. 
 
 
 These ablation studies not only validate the insights from our probe experiments but also demonstrate the effectiveness of the design choices in JEEP. 
 
 
 
 



## SECTION: Appendix B Analysis of Joint Updates



 
 In Section 4.3, we argue that changes in the low layers’ information enrichment should be greater than the changes in the high layers’ probability promotion, meaning the clamp ratio γ \gamma corresponding to the lower layers should be larger then γ ′ \gamma^{\prime} to the high layers. To validate our hypothesis, we conduct an ablation study, keeping γ \gamma =1 constant while varying the γ ′ \gamma^{\prime} from 0.05 to 1 to adjust the extent of updates in the high layers. Table 6 presents the performances of simultaneously editing 10,000 samples from Multi-COUNTERFACT on the LLaMA (7B) model. It can be observed that the high-performing values of γ ′ \gamma^{\prime} significantly smaller than γ \gamma =1, indicating that the required changes in the high layers are indeed minimal. Specifically, each metric initially increases and then decreases as γ ′ \gamma^{\prime} grows. Since changes in the high layers are effective for learning new knowledge, if γ ′ \gamma^{\prime} is too small, the δ ′ \delta^{\prime} clamp operation after each update step will interfere with the δ ′ \delta^{\prime} update process, leading to editing failure. Moreover, when γ ′ \gamma^{\prime} becomes too large, the encoding of new knowledge is predominantly captured by δ ′ \delta^{\prime} . However, probability promotion requires minimal changes, and without the enrichment of information in the lower layers, relying solely on higher-layer modifications cannot achieve effective editing. Therefore, while the extent of updates in the higher layers should be smaller than in the lower layers, it must also be kept within an appropriate range. 
 
 
 



## SECTION: Appendix C Benchmark Datasets



 
 In this section, we provide detailed descriptions, examples and evaluation metrics of the two benchmark datasets we use. 
 
 
 Figure 7: An example of zsRE dataset. 
 
 



## SECTION: C.1 zsRE Dataset



 
 The information contained in every edit example of zsRE dataset is shown in Fig. 7 . Its editing target is the correct answer, results in a natural and realistic editing task to add factual knowledge.
The sample used for testing the generalization is the paraphrase of the input prompt. As for the locality, it uses unrelated facts about other subjects. Using the above samples, we test the editing method’s Efficacy, Generalization and Locality by per-token success rate under the teacher-forcing method. Next we provide the formal definitions for the metrics. 
 
 
 Efficacy measures the per-token accuracy on the edited samples. It is the proportion of cases where the model after editing could generate the correct answer’s tokens on the same edited prompt: 
 
 
 
 
 𝔼 i [ 𝔼 t ∈ { 1 ​ … ​ T i } [ y i t true = argmax y t ℙ ℱ [ y t ∣ x i , y i 0 , … , y i t − 1 ] ] ] . \displaystyle\mathbb{E}_{i}\left[\mathbb{E}_{t\in\left\{1\ldots T_{i}\right\}}\left[y_{i_{t}}^{\text{true}}=\underset{y_{t}}{\operatorname{argmax}}\mathbb{P}_{\mathcal{F}}\left[y_{t}\mid x_{i},y_{i_{0}},\ldots,y_{i_{t-1}}\right]\right]\right]. 
 
 (13) 
 
 
 
 Generalization measures the success on the rephrasing prompts of the edited samples: 
 
 
 
 
 𝔼 i [ 𝔼 x e ∈ E ​ ( x i ) [ 𝔼 t [ y i t true = argmax y t ℙ ℱ [ y t ∣ x i e … y i t − 1 ] ] ] ] . \displaystyle\mathbb{E}_{i}\left[\mathbb{E}_{x^{e}\in\textit{E}\mathrm{(}x_{i})}\left[\mathbb{E}_{t}\left[y_{i_{t}}^{\text{true}}=\underset{y_{t}}{\operatorname{argmax}}\mathbb{P}_{\mathcal{F}}\left[y_{t}\mid x_{i}^{e}\ldots y_{i_{t-1}}\right]\right]\right]\right]. 
 
 (14) 
 
 
 
 Locality measures the success on the relevant facts of the same-type subject: 
 
 
 
 
 𝔼 i [ 𝔼 x u ∈ U ​ ( x i ) [ 𝔼 t [ y i t true = argmax y t ℙ ℱ [ y t ∣ x i u … y i t − 1 ] ] ] ] . \displaystyle\mathbb{E}_{i}\left[\mathbb{E}_{x^{u}\in\textit{U}\mathrm{(}x_{i})}\left[\mathbb{E}_{t}\left[y_{i_{t}}^{\text{true}}=\underset{y_{t}}{\operatorname{argmax}}\mathbb{P}_{\mathcal{F}}\left[y_{t}\mid x_{i}^{u}\ldots y_{i_{t-1}}\right]\right]\right]\right]. 
 
 (15) 
 
 
 
 



## SECTION: C.2 Multi-COUNTERFACT Dataset



 
 The information contained in every edit example of Multi-COUNTERFACT dataset is shown in Fig. 8 . Each editing prompt is decomposed into subject, relation, true target, and new target, with the new target serving as the editing objective, making the editing task to inject counter-factual knowledge. Therefore, completing editing on this dataset is difficult. Moreover, it constructs paraphrases by both rephrasing the edit prompts and preceding an unrelated text. As for the neighborhood prompt, it uses the facts of relevant subjects under the same relation. We detail the computation of each metric below. 
 
 
 Efficacy measures the proportion of cases where the generation of the edited model having a larger probability for new target than true target on the same edited prompt: 
 
 
 
 
 𝔼 i [ ℙ ℱ [ y i n ​ e ​ w ∣ x i ] > ℙ ℱ [ y i t ​ r ​ u ​ e ∣ x i ] ] . \displaystyle\mathbb{E}_{i}\left[\mathbb{P}_{\mathcal{F}}\left[y_{i}^{new}\mid x_{i}\right]>\mathbb{P}_{\mathcal{F}}\left[y_{i}^{true}\mid x_{i}\right]\right]. 
 
 (16) 
 
 
 
 Generalization assesses the success rate of cases where the probability of generating new target is larger than that of the true target on the equivalent prompts: 
 
 
 
 
 𝔼 i [ 𝔼 x e ∈ Equivalent ​ ( x i ) [ ℙ ℱ [ y n ​ e ​ w ∣ x e ] > ℙ ℱ [ y t ​ r ​ u ​ e ∣ x e ] ] ] . \displaystyle\mathbb{E}_{i}\left[\mathbb{E}_{x^{e}\in\textit{Equivalent}\mathrm{(}x_{i})}\left[\mathbb{P}_{\mathcal{F}}\left[y^{new}\mid x^{e}\right]>\mathbb{P}_{\mathcal{F}}\left[y^{true}\mid x^{e}\right]\right]\right]. 
 
 (17) 
 
 
 
 Locality evaluates whether the model could still maintain the original true answer on the facts of the relevant subject after the editing. It is the proportion of cases where the true answer having a larger probability than that of the new answer on the unrelated prompts. 
 
 
 
 
 
 
 𝔼 i [ 𝔼 x u ∈ Unrelated ​ ( x i ) [ ℙ ℱ [ y t ​ r ​ u ​ e ∣ x u ] > ℙ ℱ [ y n ​ e ​ w ∣ x u ] ] ] . \displaystyle\mathbb{E}_{i}\left[\mathbb{E}_{x^{u}\in\textit{Unrelated}\mathrm{(}x_{i})}\left[\mathbb{P}_{\mathcal{F}}\left[y^{true}\mid x^{u}\right]>\mathbb{P}_{\mathcal{F}}\left[y^{new}\mid x^{u}\right]\right]\right]. 
 
 (18) 
 
 
 
 Figure 8: An example of Multi-COUNTERFACT dataset. 
 
 
 
 

