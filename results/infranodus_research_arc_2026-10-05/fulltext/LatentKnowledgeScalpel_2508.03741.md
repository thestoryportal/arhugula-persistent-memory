# LatentKnowledgeScalpel — arXiv 2508.03741

Source: https://arxiv.org/html/2508.03741

## Headings
# Latent Knowledge Scalpel: Precise and Massive Knowledge Editing for Large Language Models
## 1 Introduction
## 2 Empirical Study
### 2.1 Semantic Information of a Single Entity Knowledge Block
### 2.2 Syntactic Structure of Internal Representations
## 3 Method
### 3.1 Overview of LKS
### 3.2 Building a New Knowledge Block
### 3.3 Training LKS Hypernetwork
## 4 Experiments
### 4.1 Experiment Setting
### 4.2 Evaluation Metrics
### 4.3 Selection of the LKS Operating Layer
### 4.4 Edit Performance of Large-Scale Simultaneous Editing
### 4.5 Maintaining the General Abilities of LLMs after Editing
### 4.6 Generation Quality
## 5 Related Work
## 6 Limitations and Future Works
## 7 Conclusion
## Ethical Considerations
## References
## Appendix A Details of Training LKS
## Appendix B Evaluation Dataset Construction and Examples
## Appendix C Additional Results - LKS on Counterfact
## Appendix D Fluency and Examples of Generation
## Appendix E Time consumption
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 1, "held-out": 0, "held out": 0, "generaliz": 8, "multi-token": 0, "multi token": 0, "unseen": 1, "novel entit": 0, "counterfact": 18, "zsre": 12, "teacher forc": 0, "autoregressive": 1, "first token": 0, "subject": 12, "last token": 1, "embedding": 0, "vocabulary": 0}


## SECTION: 4 Experiments



 



## SECTION: 4.1 Experiment Setting



 
 Datasets For evaluating the reliability, generality, and related-locality of factual editing, we generate two evaluation datasets using GPT-4o mini based on the zsRE question-answering dataset ( Levy et al., 2017 ) and the Counterfact dataset ( Meng et al., 2023a ) . Details can be found in Appendix  B . For unrelated-locality, we use GSM8K ( Cobbe et al., 2021 ) , RTE ( Dagan et al., 2005 ) , and SST2 ( Socher et al., 2013 ) to assess the general abilities of the edited LLMs. GSM8K tests the model’s mathematical reasoning ability, RTE assesses its natural language inference ability (i.e., whether a statement is reasonable), and SST2 evaluates sentiment analysis capabilities by classifying statements as positive or negative. 
 
 
 Baselines We use several classical or effective model editing methods as baselines. MEND ( Mitchell et al., 2022a ) edits models by updating MLP layer weights using the low-rank structure of fine-tuning gradients. ROME ( Meng et al., 2023a ) and MEMIT ( Meng et al., 2023b ) modify specific factual associations by adjusting MLP weights, with MEMIT supporting large-scale edits. GRACE ( Hartvigsen et al., 2023 ) records model hidden states in a codebook and replaces the original states during edits. WISE ( Wang et al., 2024a ) introduces a dual parametric memory mechanism, with a main memory for pretrained knowledge and a side memory exclusively for edits. AlphaEdit ( Fang et al., 2025 ) attempts to preserve original knowledge by projecting weight updates onto the null space of preserved facts. All baselines are evaluated using EasyEdit ( Wang et al., 2024b ) , an easy-to-use framework for LLM knowledge editing, ensuring convenient and fair assessment. 
 
 
 



## SECTION: 4.2 Evaluation Metrics



 
 Following prior works ( Mitchell et al., 2022a ; Mitchell et al., 2022b ; Meng et al., 2023a ) , we evaluate LLM editing performance using three primary metrics: reliability, generality, and locality. As shown in Figure  1 , these metrics assess the model’s behavior for prompts inside and outside the edit scope. 
 
 
 For reliability and generality , computing the average exact-match accuracy between the edited predictions and the target outputs within the edit scope: 
 
 
 

 
 
 Rel = 𝔼 ⁡ ( 𝟙 f L ​ K ​ S ​ ( x e ) = y e ) \text{Rel}=\mathbb{E}(\mathds{1}_{f_{LKS}(x_{e})=y_{e}}) 
 
 (6) 
 
 
 
 

 
 
 Gen = 𝔼 ⁡ ( 𝟙 f L ​ K ​ S ​ ( x e ​ q ) = y e ) \text{Gen}=\mathbb{E}(\mathds{1}_{f_{LKS}(x_{eq})=y_{e}}) 
 
 (7) 
 
 
 
 For locality, we further divide it into two categories: related-locality, which pertains to areas related to the edited entity but not the modified feature, and unrelated-locality, which refers to areas completely outside the edit scope. In other words, unrelated-locality means that after performing factual edits, the general abilities of LLMs, such as mathematical reasoning and sentiment analysis, should remain unchanged. 
 
 
 For related-locality , we measure whether predictions for inputs which are related to the edited entity but outside the edit scope remain unchanged: 
 
 
 

 
 
 Loc = 𝔼 ⁡ ( 𝟙 f L ​ K ​ S ​ ( x l ​ o ​ c ) = f ⁡ ( x l ​ o ​ c ) ) \text{Loc}=\mathbb{E}(\mathds{1}_{f_{LKS}(x_{loc})=f(x_{loc})}) 
 
 (8) 
 
 
 
 We define Edit Performance (EP) as the average of reliability, generality, and related-locality, providing a comprehensive evaluation of editing effectiveness. 
 
 
 For unrelated-locality , we assess how well the edited LLM preserves the general abilities of its original model, including mathematical reasoning, natural language inference, and sentiment analysis. 
 
 
 



## SECTION: Appendix B Evaluation Dataset Construction and Examples



 
 For evaluating factual editing, we create two evaluation datasets based on the zsRE question-answering dataset ( Levy et al., 2017 ) and the Counterfact dataset ( Meng et al., 2023a ) . Each of the evaluation datasets contains 10,000 data points. Specifically, we used GPT-4o-mini to generate 10,000 prompts for generality in the Counterfact dataset, and 10,000 prompts for related-locality in both the zsRE and Counterfact datasets. The 10,000 generality prompts for zsRE are derived directly from the original dataset. Text  2 and Text  3 show the prompt templates provided to GPT-4o-mini for generating the generalization and related-locality evaluation prompts, respectively. 
 
 
 ⬇ 
 " system ": " Please output the synonym of the prompt given . Make sure they express the same semantics or question . And they should not differ much in length ." 
 
 " user ": " Prompt : What is the capital of United States ?" 
 
 " assistant ": " The capital of United States is where ?" 
 
 " user ": " Prompt : The occupation of Alice is " 
 
 " assistant ": " Alice ’ s job is " 
 
 " user ": " Prompt : { prompt }" 
 
 
 Text 2: The prompt template provided to GPT-4o-mini for generating the generalization evaluation prompts. The roles ”system”, ”assistant”, and ”user” represent different chat participants. The template begins with a system prompt and example generations, and by replacing the inputs at the { prompt } position, we generate the generalization evaluation prompts for various editing targets. 
 
 
 ⬇ 
 " system ": " We would like to evaluate the effectiveness of knowledge editing . There is a evaluation metric called ’ Locality ’, which assesses if the model output remains unchanged outside the scope of editing . Now , give you the edit subject and prompt which indicates the edit scope . Please help to generate a new prompt and a short corresponding answer to evaluate locality of this edit . Make sure you know the answer of this new prompt , and the answer must be less than three words . Note that the new prompt must include the subject ." 
 
 " user ": " Subject : United States \nPrompt : The capital of United States is " 
 
 " assistant ": " EvalPrompt : The largest city in the United States is \nEvalAnswer : New York " 
 
 " user ": " Subject : Alice \nPrompt : The occupation of Alice is " 
 
 " assistant ": " EvalPrompt : The favorite food of Alice is \nEvalAnswer : Hot dog " 
 
 " user ": " Subject : { subject } \nPrompt : { prompt }" 
 
 
 Text 3: The prompt template provided to GPT-4o-mini for generating the related-locality evaluation prompts. Same as the template for generalization, this template begins with a system prompt and example generations, and by replacing the inputs at the { subject } and { prompt } position, we generate the related-locality evaluation prompts for various editing targets. 
 
 
 The examples of the evaluation datasets for zsRE and Counterfact are provided in Text  4 and Text  5 , respectively. 
 
 
 ⬇ 
 { 
 
 " subject ": " Christiane Cohendy ", 
 
 " prompt ": " What is the native language of Christiane Cohendy ?", 
 
 " target ": " German ", 
 
 " ground _ truth ": " French ", 
 
 " generality ": " What ’ s Christiane Cohendy ’ s mother tongue ?", 
 
 " locality ": { 
 
 " prompt ": " What is the occupation of Christiane Cohendy ?", 
 
 " target ": " Actress " 
 
 } 
 
 } 
 
 
 Text 4: An example of the evaluation dataset for zsRE. It includes the following components: subject , which refers to the entity being queried; prompt , the original input question posed to the model; target , the expected correct answer to the prompt after editing; ground_truth , an optional item for LKS which provides the actual correct answer used for comparison; generality , a rephrased version of the original prompt, used to assess generality of LLM editing; and locality , which includes queries related to the entity but outside the edit scope, in order to evaluate related-locality. 
 
 
 ⬇ 
 { 
 
 " subject ": " Danielle Darrieux ", 
 
 " prompt ": " The mother tongue of Danielle Darrieux is ", 
 
 " target ": " English ", 
 
 " ground _ truth ": " French ", 
 
 " generality ": " Danielle Darrieux ’ s native language is ", 
 
 " locality ": { 
 
 " prompt ": " The birth year of Danielle Darrieux is ", 
 
 " target ": "1917" 
 
 } 
 
 } 
 
 
 Text 5: An example of the evaluation dataset for Counterfact. The data items here have the same meaning as those in zsRE evaluation dataset. 
 
 
 



## SECTION: Appendix C Additional Results - LKS on Counterfact



 
 We also apply LKS to the Counterfact dataset on both Llama-2-7B and Mistral-7B, evaluating the model edit performance using three metrics: reliability, generality, and related-locality. 
 
 
 Table  5 presents the editing results of LKS on the Counterfact dataset with 1000 data points. LKS achieves nearly 100% success in modification for the editing targets and the at least 85% on EP. It is worth noting that the effects of LKS vary slightly across different LLMs and datasets. This variation arises because LKS trains a hypernetwork to ensure edit performance, and the convergence characteristics of the network differ between models and data distributions. Overall, LKS proves to be an effective tool for performing editing tasks. The training hyperparameters are detailed in Table  6 . 
 
 
 Table 5: Edit Performance of LKS on Counterfact 
 
 
 
 Model 
 Rel 
 Gen 
 Loc 
 EP 
 
 
 
 Llama-2-7B 
 100 
 98.0 
 80.5 
 92.8 
 
 Mistral-7B 
 97.1 
 86.9 
 73.6 
 85.9 
 
 
 
 
 Table 6: Training hyperparameters of LKS on Counterfact with 1000 edits. 
 
 
 
 Model 
 λ e ​ d ​ i ​ t \lambda_{edit} 
 Max Epoch 
 Batch Size 
 
 
 
 Llama-2-7B 
 3 
 20 
 32 
 
 Mistral-7B 
 12 
 20 
 1 
 
 
 
 
 

