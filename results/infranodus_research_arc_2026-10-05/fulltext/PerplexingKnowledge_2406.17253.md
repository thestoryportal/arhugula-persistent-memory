# PerplexingKnowledge — arXiv 2406.17253

Source: https://arxiv.org/html/2406.17253

## Headings
# How Well Can Knowledge Edit Methods Edit Perplexing Knowledge?
## 1 Introduction
## 2 Related Work
### 2.1 Knowledge Edit Methods
### 2.2 Limitation of Knowledge Edit Methods
## 3 Model Edit Methods
#### FT
#### LoRA ( Hu et al., 2021 )
#### ROME ( Meng et al., 2022a )
#### MEMIT ( Meng et al., 2022b )
## 4 Data and tool
### 4.1 Data
#### HierarchyData
#### CounterFact
### 4.2 Tool
## 5 Experiment setup
## 6 Results
### 6.1 Correlations between perplexingness and edit ineffectiveness
#### Correlations are significant
#### Correlation is in the new knowledge but not the original knowledge
### 6.2 Significantly higher perplexingness of higher hierarchy level knowledge
#### Correlations between perplexingness and edit ineffectiveness in HierarchyData
### 6.3 Relationships between hierarchical relations and edit ineffectiveness
#### GPT-J can understand perplexing knowledge better
## 7 Discussion
#### Do different models have different mechanisms of saving perplexing knowledge?
#### Why should more abstract knowledge be harder to edit?
#### Are there other factors that may influence the perplexingness?
#### More understanding of model editing
#### Recommendations to future model editors
## 8 Conclusion
## 9 Limitation
## 10 Acknowledgements
## References
## Appendix A Correlation of perplexingness and efficacy in CounterFact
## Appendix B Correlation of perplexingness and efficacy in HierarchyData
## Appendix C Specific vs. Abstract Probability Distribution in HierarchyData
## Appendix D Pre-edit Specific vs. Abstract Probability Distribution in HierarchyData
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 0, "held-out": 0, "held out": 0, "generaliz": 0, "multi-token": 0, "unseen": 0, "novel entit": 0, "new entit": 1, "counterfact": 18, "zsre": 0, "teacher forc": 0, "autoregressive": 0, "subject": 3, "last token": 0, "embedding": 0, "vocabulary": 0, "propagat": 3}


## SECTION: How Well Can Knowledge Edit Methods Edit Perplexing Knowledge?


 
 
 Huaizhi Ge
 
 Affiliation:  Columbia University
 
 Email:  hg2590@columbia.edu 
 
    
 Frank Rudzicz
 
 Affiliation:  Dalhousie University
 
 Email:  frank@dal.ca 
 
    
 Zining Zhu
 
 Affiliation:  Stevens Institute of Technology
 
 Email:  zzhu41@stevens.edu 
 

 Abstract 
 
 Large language models (LLMs) have demonstrated remarkable capabilities, but updating their knowledge post-training remains a critical challenge. While recent model editing techniques like Rank-One Model Editing (ROME) ( Meng et al., 2022a ) show promise, their effectiveness may vary based on the nature of the knowledge being edited. We introduce the concept of “perplexingness”: the degree to which new knowledge conflicts with an LLM’s learned conceptual hierarchies and categorical relationships. For instance, editing “British Shorthair is a kind of cat” to “British Shorthair is a kind of dog” represents a low-perplexingness edit within the same taxonomic level, while editing “A cat is a kind of animal” to “A cat is a kind of plant” represents a high-perplexingness edit that violates fundamental categorical boundaries.
To systematically investigate this phenomenon, we introduce HierarchyData , a carefully curated dataset of 99 hyponym-hypernym pairs across diverse categories. Through controlled experiments across three models and four editing methods, we demonstrate a strong negative correlation between the perplexingness of new knowledge and the effectiveness of knowledge editing. Our analysis reveals that edits involving more abstract concepts (hypernyms) generally exhibit higher perplexingness and are more resistant to modification than their specific counterparts (hyponyms). These findings highlight a fundamental challenge in LLM knowledge editing: the more a new fact contradicts an LLM’s learned conceptual hierarchies, the harder it becomes to reliably encode that knowledge. 
 
 
 
 
 
 



## SECTION: 2.1 Knowledge Edit Methods



 
 Various approaches have been developed to modify the knowledge embedded in large language models. ROME ( Meng et al., 2022a ) updated feed-forward weights to alter specific factual associations. MEMIT ( Meng et al., 2022b ) allowed for the incorporation of numerous memories into a language model. LoRA ( Hu et al., 2021 ) maintains pre-trained weights while using trainable decomposition matrices for efficient, targeted updates without altering the original weights. Model Editor Networks with Gradient Decomposition (MEND) ( Mitchell et al., 2021 ) utilized a single targeted input-output pair for quick, localized adjustments in a pre-trained model’s behavior. Other notable methods include editing specific knowledge neurons ( Dai et al., 2021 ) , employing hyper-networks ( De Cao et al., 2021 ) , and applying linear transformations ( Hernandez et al., 2023 ) . These techniques have demonstrated impressive efficacy in modifying knowledge in large language models. There are also works that apply model editing to gain novel insights about the model interpretability ( Niu et al., 2024 ; Hase et al., 2024 ) .
However, the performance of the model editing techniques is typically assessed in a broad context. We delve into whether model editing methods are applicable to knowledge with different perplexingness. We specifically examine the impact of the conditional probability of the target words for editing and the hierarchical relationships among words on the overall performance of these editing techniques. 
 
 
 



## SECTION: 2.2 Limitation of Knowledge Edit Methods



 
 Recent research has identified certain limitations in the methods used for editing large language models. Firstly, some studies have concentrated on the specificity of edits, developing new metrics and benchmarks for evaluation. Hoelscher-Obermaier et al. (2023) enhanced existing benchmarks by introducing a dynamic component and proposed a KL divergence-based metric for measuring specificity. Li et al. (2023b) introduced an evaluation protocol and a question-answer dataset designed to assess edit specificity. 
 
 
 Secondly, the consistency of edits has been another focal point. Zhong et al. (2023) devised a multi-hop question benchmark to test whether models can correctly respond to questions affected by edited facts. Wu et al. (2023) examined knowledge editing through reasoning and cross-lingual knowledge transfer. Ma et al. (2024) looked into whether edited LLMs can behave consistently resembling communicative AI in realistic situations. Li et al. (2023b) also offered a protocol to evaluate edit consistency, while Onoe et al. (2023) investigated the ability of LLMs to infer and propagate injected facts. A particularly impactful work, RippleEdit ( Cohen et al., 2023 ) , evaluated how model editing impacts the implied and related facts. Li et al. (2023a) studied the knowledge conflict and distortion in knowledge editing. Rosati et al. (2024) introduced a long-form evaluation protocol, assessing the effects of model editing beyond the immediate “next token”; we consider the effects of the model editing methods that can be assessed at the next token. 
 
 
 Thirdly, the nature of the edited knowledge has been scrutinized. Gupta et al. (2023) specifically evaluated editing methods on commonsense knowledge statements, as opposed to encyclopedic knowledge. Ma et al. (2024) examined which knowledge features are correlated with the performance and robustness of editing. Zhang et al. (2024) tracked the edited knowledge with concept graphs. ( Wang et al., 2024 ) studied the concepts of the edited knowledge. 
 
 
 While these studies cover various aspects, they did not quantify the impact of the type of knowledge being edited. In this paper, we explore how the perplexingness of the knowledge and the hierarchical relations among words influence the efficacy of editing methods in large language models. 
 
 
 
 



## SECTION: 3 Model Edit Methods



 
 For a knowledge edit task, we represent each fact as a knowledge tuple t = ( s , r , o ) t=(s,r,o) . For each fact, we want to insert a new knowledge tuple t = ( s , r , o ∗ ) t=(s,r,o^{*}) . In this paper, we examine several popular model edit methods, as follows: 
 
 



## SECTION: 5 Experiment setup



 
 The experiments conducted in this study are designed to evaluate the efficacy of several knowledge editing methods, including FT, LoRA, ROME, and MEMIT. Our approach involves the substitution of a knowledge tuple, denoted as ( s , r , o ∗ ) (s,r,o^{*}) , for the existing tuple ( s , r , o ) (s,r,o) . In this context, s s represents the subject, r r delineates the relation, and o o corresponds to the object. This analysis is carried out using three distinguished large language models: GPT2-Large, GPT2-XL, and GPT-J (6B). 
 
 
 First, we want to define perplexing knowledge. People find knowledge perplexing when they cannot understand it. So we define the perplexing knowledge as the knowledge that the model cannot easily understand. We quantify the perplexingness of knowledge as the conditional probabilities of new targets prior to editing. For easier comparison, we use the negative log form of the probability: the higher the value, the lower the probability, and the more perplexing the model finds the new knowledge. Formally: 
 

 
 
 Perplexingness = − log ℙ pre ​ - ​ edit [ o ∗ | s , r ] . \mathrm{Perplexingness}=-\log\mathbb{P}_{\mathrm{pre}\text{-}\mathrm{edit}}[o^{*}|s,r]. 
 
 (1) 
 
 The probabilities are computed by the language model after editing. It is important to note that we define perplexingness based on the model’s poor understanding of the knowledge, not its complexity. Even if a piece of knowledge is complex, if it is well known to the model due to effective pre-training, we do not consider it perplexing to the model. 
 
 
 Second, we evaluate edit performance by its efficacy. To parallel “perplexingness,” we define ineffectiveness as the conditional probability of new targets after the edit. While other scores like accuracy can be used, the negative log probability is more fine-grained and allows more intuitive data interpretation. A higher “Ineffectiveness” value indicates lower edit efficacy. Formally: 
 

 
 
 Ineffectiveness = − log ℙ post ​ - ​ edit [ o ∗ | s , r ] . \mathrm{Ineffectiveness}=-\log\mathbb{P}_{\mathrm{post}\text{-}\mathrm{edit}}[o^{*}|s,r]. 
 
 (2) 
 
 The probabilities are computed by the language model after editing. The investigation into the perplexing knowledge and the ineffectiveness of edits employs the CounterFact dataset. For each LLM, a total of 2,000 counterfact samples were analyzed. 
 
 
 



## SECTION: 6 Results



 

