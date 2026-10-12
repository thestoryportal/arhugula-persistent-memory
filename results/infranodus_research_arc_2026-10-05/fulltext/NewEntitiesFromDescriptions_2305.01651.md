# NewEntitiesFromDescriptions — arXiv 2305.01651

Source: https://arxiv.org/html/2305.01651

## Headings
# Can LMs Learn New Entities from Descriptions? 
 Challenges in Propagating Injected Knowledge
## 1 Introduction
## 2 Entity Knowledge Propagation
### 2.1 Task Definition
## 3 Constructing benchmarks for EKP
### 3.1 ECBD
### 3.2 Entity Inferences
## 4 Experimental Setup
### 4.1 Base Language Models
### 4.2 Parameter Updating Methods
### 4.3 Input Augmentation
### 4.4 Computational Cost
## 5 Results
### 5.1 Entity Inferences
### 5.2 ECBD
### 5.3 ECBD-easy
## 6 Analysis
### 6.1 Targeted Update / Specificity Tradeoff
### 6.2 Information Overlap
## 7 Related Work
## 8 Conclusion
## Limitations
## Acknowledgments
## References
## Appendix A Appendix
### A.1 Licensing
### A.2 Harmful Data Instances
### A.3 Modeling Details
### A.4 Entity Inferences
### A.5 More Similarity Scores
### A.6 Analysis of ROME
#### A.6.1 Comparison of datasets
#### A.6.2 ROME Test Generation
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 3, "held-out": 0, "held out": 0, "generaliz": 2, "multi-token": 0, "unseen": 5, "novel entit": 2, "new entit": 8, "counterfact": 5, "zsre": 0, "teacher forc": 0, "autoregressive": 2, "subject": 16, "last token": 0, "embedding": 0, "vocabulary": 1, "propagat": 24}


## SECTION: 3 Constructing benchmarks for EKP



 
 
 
 
 Dataset 
 # Examples 
 # Entities 
 y e y_{e} in d e d_{e} 
 
 
 
 Entity Inferences 
 170 
 85 
 92 
 
 ECBD 
 1000 
 208 
 29 
 
 ECBD-easy 
 152 
 74 
 152 
 
 
 Table 2: Statistics from each EKP dataset. We report the number of examples in each evaluation set in addition to the number of unique entities and total instances where the gold span can be found within the entity description. 
 
 
 We use two different types of datasets to investigate how new entity knowledge is propagated into the LM’s parameter space. Table  2 summarizes the dataset statistics on two benchmarks, including the extent to which the target spans y y overlap with the definitions d e d_{e} , which will be important later. 
 
 



## SECTION: 4 Experimental Setup



 



## SECTION: 4.2 Parameter Updating Methods



 
 Finetuning 

 
 is a common way for adapting a pre-trained LM to a specific task or domain Gururangan et al. (2020) .
In a similar vein, we aim to adopt a pretrained LM to an environment where new entities constantly arise.
Given e e and its definition d e d_{e} , we update the parameters θ \theta to minimize loss on a training example formed from d e d_{e} .
For left-to-right models (e.g., GPT-Neo), we use the standard next token prediction language modeling task on the entire d e d_{e} example.
For mask filling models (T5), we randomly select a span 5 5 
 5 
 
 
 
 We uniformly draw span length between 1 and 5 to match the average span length used during pretraining of T5. that is not overlapping with the entity mention span, following Onoe et al. (2022) . We experiment with two fine-tuning settings: full model (updating all parameters) and last layer (updating parameters belonging to the last transformer layer only). We start finetuning from the original model checkpoint for each example. 6 6 
 6 
 
 
 
 Zhu et al. (2020) reports that finetuning on an individual fact (FTM) constantly outperforms finetuning with mixed facts (FTA). 
 
 
 
 
 
 
 Entity Inferences (Accuracy) 
 ECBD (Perplexity) 
 ECBD-easy (Perplexity) 
 
 Method 
 Target ( Δ \Delta ) 
 Specificity ( Δ \Delta ) 
 Target ( Δ \Delta ) 
 Specificity ( Δ \Delta ) 
 Target ( Δ \Delta ) 
 Specificity ( Δ \Delta ) 
 
 Type: left-to-right 
 GPT-Neo 
 Size: 1.3B 
 
 Model Editing 
 Base Model 
 34.1 
 34.1 
 38.8 
 26.1 
 21.1 
 26.1 
 
 FT (full model) 
 57.7 ( + + 23.6) 
 18.3 ( − - 15.9) 
 36.8 ( − - 2.0) 
 26.0 ( + + 0.1) 
 12.1 ( − - 9.0) 
 26.0 ( − - 0.1) 
 
 FT (last layer) 
 48.8 ( + + 14.7) 
 16.4 ( − - 17.7) 
 38.7 ( − - 0.1) 
 26.0 ( + + 0.1) 
 19.6 ( − - 1.5) 
 26.1 (0.0) 
 
 MEND 
 41.8 ( + + 7.7) 
 34.4 ( + + 0.3) 
 48.6 ( + + 9.8) 
 27.2 ( + + 1.1) 
 12.6 ( − - 8.5) 
 28.1 ( + + 2.1) 
 
 Input Augmentation 
 Definition 
 60.0 ( + + 25.9) 
 34.1 
 22.5 ( − - 16.3) 
 26.1 
     3.2 ( − - 17.9) 
 26.1 
 
 Random Def. 
 27.7 ( − - 6.4) 
 34.1 
 55.1 ( + + 16.3) 
 26.1 
   35.7 ( + + 14.6) 
 26.1 
 
 Type: seq-to-seq 
 T5 Large 
 Size: 770M 
 
 Model Editing 
 Base Model 
 42.9 
 42.9 
 17.0 
 12.9 
 14.3 
 12.9 
 
 FT (full model) 
 64.7 ( + + 21.8) 
 38.2 ( − - 4.7) 
 17.0 (0.0) 
 12.9 (0.0) 
 14.3 (0.0) 
 12.8 ( − - 0.1) 
 
 FT (last layer) 
 52.9 ( + + 10.5) 
 43.9 ( + + 1.0) 
 17.0 (0.0) 
 12.9 (0.0) 
 14.2 ( − - 0.1) 
 12.9 (0.0) 
 
 MEND 
 43.5 ( + + 0.6) 
 42.7 ( − - 0.2) 
 17.3 ( + + 0.3) 
 12.9 (0.0) 
 14.0 ( − - 0.3) 
 12.9 (0.0) 
 
 Input Augmentation 
 Definition 
 73.5 ( + + 30.6) 
 42.9 
 12.4 ( − - 4.6) 
 12.9 
 13.6 ( − - 0.7) 
 12.9 
 
 Random Def. 
 42.4 ( − - 0.5) 
 42.9 
 15.8 ( − - 1.2) 
 12.9 
 13.6 ( − - 0.7) 
 12.9 
 
 Type: left-to-right 
 GPT2-XL 
 Size: 1.5B 
 
 Model Editing 
 Base Model 
 32.9 
 32.9 
 42.8 
 25.4 
 31.0 
 25.4 
 
 FT (full model) 
 62.9 ( + + 30.0) 
 24.1 ( − - 8.8) 
 39.4 ( − - 3.4) 
 25.4 (0.0) 
 16.8 ( − - 14.2) 
 25.4 (0.0) 
 
 FT (last layer) 
 46.5 ( + + 13.6) 
 35.4 ( + + 2.5) 
 42.8 (0.0) 
 25.4 (0.0) 
 30.4 ( − - 0.6) 
 25.4 (0.0) 
 
 ROME 
 54.3 ( + + 23.5) 
 29.9 ( − - 2.0) 
 N/A 
 N/A 
 N/A 
 N/A 
 
 Input Augmentation 
 Definition 
 64.1 ( + + 31.2) 
 32.9 
 26.6 ( − - 16.2) 
 25.4 
     3.5 ( − - 27.5) 
 25.4 
 
 Random Def. 
 26.5 ( − - 6.4) 
 32.9 
 56.3 ( + + 13.5) 
 25.4 
 37.1 ( + + 6.1) 
 25.4 
 
 
 Table 3: Evaluation results. On Entity Inferences , both fine-tuning and ROME show large increases in accuracy with various costs to specificity, although MEND is ineffective. On the more challenging ECBD data, despite Input Augmentation suggesting that knowledge is relevant, no technique leads to a decrease in perplexity, although we do see some gains on ECBD-easy . 
 
 
 
 MEND  Mitchell et al. (2022) 

 
 can be viewed as a hypernetwork that efficiently transforms the raw finetuning gradient into a parameter update that should successfully edit the base model’s parameters in one step. This method is designed for injecting or editing individual facts about entities, not a collections of facts about entities (i.e., a complete definition’s worth of entity knowledge). The MEND parameters are trained on an editing dataset where each example consists of an input-output pair, an altered output, and locality examples (for measuring sensitivity). The goal of MEND training is to learn a network that modifies the target fact without affecting unmodified facts. 
 
 
 We train MEND editors for GPT-Neo and T5 with the WikiText-103 dataset, which uses generated text as altered output following the configuration used in the original paper. 7 7 
 7 
 
 
 
 https://github.com/eric-mitchell/mend 
 
 
 
 ROME  Meng et al. (2022) 

 
 performs knowledge editing by treating a MLP as a key-value storage: it uses a subject (such as the Eiffel Tower) to extract the “value” associated with that subject in the MLP. Then, it uses a rank-one modification of the weights of the MLP to “rewrite” this key-value pair. 
 
 
 We use the ROME editor for GPT2-XL. We format according to the subject, relation, and object structure of ROME prompts; examples of these can be found in the Appendix. The subject is a one-word name of the entity, the relation is the definition sentence before the <MASK> token, and the object is the correct label. Examples in which the subject did not appear before the <MASK> token (less than 0.5% of our data) were filtered. 8 8 
 8 
 
 
 
 Additionally, a number of examples in ECBD had a format incompatible with ROME; for example, ROME is currently unable to run on examples with special tokens such as ’(’ or ’*’ immediately surrounding the subject. We will discuss later the performance of ROME on ECBD and why we do not formally report it. 
 
 
 
 



## SECTION: 5 Results



 
 Table  3 reports the performances of various knowledge injection approaches on three base models. In all experimental setting, we see input augmentation (prepending definition) boasts robust and consistent performances gains. Prepending random definitions hurt performances in GPT-Neo while does not impact T5.
This indicates that the definition contains information relevant to the spans to predict.
As model behaves substantially differently across datasets, we first separately discuss the results on each dataset, Entity Inferences , ECBD , and ECBD-easy , and then draw larger conclusions. 
 
 



## SECTION: 6 Analysis



 
 We analyze the challenges in knowledge propagation by first estimating an informal upper bound of model editing performance (Section  6.1 ).
We then examine how the similarity between the definition sentence and probe sentence impacts the performance of model editing (Section  6.2 ), inspired by positive performances on ECBD-easy subset. We conduct our analysis with GPT-Neo base model on random subsets of Entity Inferences (half the data) and ECBD (100 NP span and 100 random span) to reduce computational costs. 
 
 



## SECTION: A.6 Analysis of ROME



 



## SECTION: A.6.1 Comparison of datasets



 
 The Counterfactual dataset was one of the datasets created and used by ( Meng et al., 2022 ) . It consisted of a set of "counterfacts" - facts that are altered slightly. For example, one entry in this dataset is "The Eiffel Tower is located in the City of Rome". 
 
 
 As one can see in Table 4, the three datasets scale in complexity. Counterfactual usually includes known entities (subjects) and known labels (objects). Entity Inferences usually contains unknown entities, but its labels are often known. Lastly, ECBD not only has unknown entities, but it also sometimes contains non-descriptive labels. This may explain why it obtained such drastic increases in perplexity on ECBD. 
 
 
 
 
 
 
 
 Entity 
 
 
 
 Definition 
 
 
 
 Probe Sentences 
 
 
 
 Gold Label 
 
 
 
 
 
 
 2020 Vuelta a España 
 
 
 
 The 2020 Vuelta a España was the 75th edition of the Vuelta a España, one of cycling’s three grand tours. 
 
 
 
 The full route of the 2020 Vuelta a España was announced on <MASK> in Madrid. 
 
 
 
 Tuesday 17 December 2019 
 
 
 
 
 M1 
 
 
 
 The Apple M1 is an ARM-based system on a chip (SoC). 
 
 
 
 The M1 contains <MASK> in a 16-core Neural Engine, capable of executing 11 trillion operations per second. 
 
 
 
 dedicated neural network hardware 
 
 
 
 
 Dixie Fire 
 
 
 
 The Dixie Fire is an active wildfire in Butte, Plumas, Lassen, and Tehama Counties, California. 
 
 
 
 Smoke from the Dixie Fire caused <MASK> across the Western United States, including as far east of California as Utah and Colorado.. 
 
 
 
 unhealthy air quality 
 
 
 
 
 Cravity 
 
 
 
 Cravity () is a South Korean boy band formed by Starship Entertainment 
 
 
 
 On August 13, at the 2020 Soribada Awards, Cravity won the "New Artist Award", <MASK> since debut. 
 
 
 
 their first award 
 
 
 
 Table 4: Examples from ECBD. 
 
 
 
 
 
 
 
 Entity 
 
 
 
 Definition 
 
 
 
 Probe Sentences 
 
 
 
 Gold Label 
 
 
 
 
 
 
 Cyclone Niran 
 
 
 
 Severe Tropical Cyclone Niran was a very powerful tropical cyclone that brought severe impacts to extreme Northeastern Australia and nearly made landfall in New Caledonia in February and March 2021. 
 
 
 
 Cyclone Niran left widespread damage in <MASK>. 
 
 
 
 Australia 
 
 
 
 
 2020 Lekki shooting 
 
 
 
 On the night of 20 October 2020, at about 6:50p.m., members of the Nigerian Army opened fire on peaceful End SARS protesters at the Lekki toll gate in Lagos State, Nigeria 
 
 
 
 2020 Lekki shooting happened near my house, so my family and I <MASK> from the area. 
 
 
 
 escaped 
 
 
 
 
 Ronald Deschamplains 
 
 
 
 Roland Deschamplains (born September 21, 1989), better known by his stage name Desham, is an American singer , songwriter, and dancer who has sold over 30 million singles and has achieved eleven Platinum singles. 
 
 
 
 Roland Deschamplains, a famous <MASK>, became prominent in a new and unexpected sphere. 
 
 
 
 singer 
 
 
 
 
 The Great 
 
 
 
 The Great is a 2020 comedy-drama television series described by its commissioner Hulu as ’anti-historical’ loosely based on the rise to power of Catherine the Great, Empress of All Russia. 
 
 
 
 Some people think The Great is very <MASK>. 
 
 
 
 funny 
 
 
 
 Table 5: Examples from Entity Inferences 
 
 
 
 
 
 Dataset 
 Example 
 
 
 
 
 
 Counterfactual 
 
 
 
 "The Eiffel Tower is located in the City of Rome " 
 
 
 
 
 Entity Inferences 
 
 
 
 "Severe Tropical Cyclone Niran was a very powerful tropical cyclone that brought severe impacts to extreme Northeastern Australia " 
 
 
 
 
 ECBD 
 
 
 
 " Gamma variant, also known as lineage P.1, is one of the variants of SARS-CoV-2, the virus that causes COVID-19." 
 
 
 
 Table 6: Comparison of one example of three datasets. The subject is underlined and the object is bolded. 
 
 
 
 
 
 Original Definition 
 Subject 
 Relation 
 Object 
 
 
 
 
 
 Hurricane Nana was a minimal Category 1 hurricane that caused moderate damage across Belize in early September 2020. 
 
 
 
 Hurricane 
 
 
 
 {}Nana was a minimal Category 1 hurricane that caused moderate damage across 
 
 
 
 Belize 
 
 
 
 
 Tale of the Nine Tailed is a South Korean television drama starring Lee Dong-wook, Jo Bo-ah and Kim Bum. 
 
 
 
 Tale 
 
 
 
 {}of the Nine Tailed is a South Korean television 
 
 
 
 drama 
 
 
 
 
 The 2020 UEFA Super Cup was the 45th edition of the UEFA Super Cup, an annual football match organised by UEFA and contested by the reigning champions of the two main European club competitions, the UEFA Champions League and the UEFA Europa League. 
 
 
 
 UEFA 
 
 
 
 The 2020 {} Super Cup 
 
 
 
 was the 
 
 
 
 Table 7: ROME Formatting. Object is bolded in original definition, and subject is underlined. As can be seen, especially from the third example, formatting to ROME’s standard often sacrifices valuable context within our dataset. 
 
 
 

