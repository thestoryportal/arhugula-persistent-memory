# VocabExpansionKL — arXiv 2508.15807

Source: https://arxiv.org/html/2508.15807

## Headings
## Abstract
## Abstrakt
## 1 Introduction
### 1.1 Motivation
### 1.2 Research Question
### 1.3 Methodology Outline
## 2 Background
### 2.1 Mathematical background for autoregressive models and deep learning
#### 2.1.1 Autoregressive Language Modeling
#### 2.1.2 Probability and Loss Function
#### 2.1.3 Stochastic Gradient Descent
### 2.2 LLM Architecture
#### 2.2.1 Tokens and Embeddings
#### 2.2.2 Transformers
#### 2.2.3 Head
### 2.3 Additional Concepts and Techniques
#### 2.3.1 Kullback–Leibler Divergence
#### 2.3.2 Knowledge Distillation
#### 2.3.3 Partial Unfreezing
#### 2.3.4 Low-Rank Adaptation
### 2.4 Related Works
#### 2.4.1 FOCUS
#### 2.4.2 Vocabulary Expansion with 0.01GB
#### 2.4.3 AweDist
## 3 Methods
### 3.1 Data and Models
#### 3.1.1 Data
#### 3.1.2 Model
#### 3.1.3 Tokenization
### 3.2 Proposed Method
#### 3.2.1 Initialization of Embeddings via a Teacher Model
#### 3.2.2 Token Alignment
#### 3.2.3 Head
### 3.3 Experimental Setup
#### 3.3.1 Training of Head and Embedding
#### 3.3.2 Training of Whole Head/Embedding
#### 3.3.3 Full Finetuning with LoRA
#### 3.3.4 Full Sequential Finetuning
## 4 Evaluation
## 5 Results
### 5.1 Training
#### 5.1.1 Phase 1: New Module Training
#### 5.1.2 Phase 2: Full Finetuning with LoRA
#### 5.1.3 Phase 2: Full Sequential Finetuning
### 5.2 Evaluation
## 6 Discussion
### 6.1 Phase 1: Training Only New Embeddings
### 6.2 Phase 2: Finetuning and Evaluation
#### 6.2.1 Experimental Setup and Formatting
#### 6.2.2 BigCodeBench
#### 6.2.3 DS-1000
### 6.3 LoRA vs Full Finetuning
### 6.4 Challenges
## 7 Conclusion
### 7.1 Performance
### 7.2 Takeaways
### 7.3 Future Work
## References
## Appendix A Mechanistic Interpretation
### A.1 Embeddings Direction in Vector Space
### A.2 Head
### A.3 Conclusion
## Appendix B Vocabulary Expansion Method
## Appendix C Token Sequence Mapping
## Appendix D Hardware & Cost
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 0, "held-out": 0, "held out": 0, "generaliz": 1, "multi-token": 0, "unseen": 0, "novel entit": 0, "new entit": 0, "counterfact": 0, "zsre": 0, "teacher forc": 0, "autoregressive": 12, "subject": 0, "last token": 7, "embedding": 196, "vocabulary": 105, "propagat": 3}


## SECTION: 1.3 Methodology Outline



 
 A novel student-teacher framework is introduced where the pre-trained model serves as its own teacher for learning new token representations. The methodology consists of three main phases that systematically address vocabulary expansion challenges. 
 
 
 Embedding Initialization via Self-Distillation: The model itself is leveraged as a teacher to initialize new embeddings. Rather than using heuristic approaches like averaging constituent token embeddings, new embeddings are optimized using Kullback–Leibler divergence loss. The training objective ensures that sequences tokenized with the extended vocabulary produce output distributions that closely match those from the original tokenization. This self-distillation approach allows new tokens to integrate seamlessly into the pretrained model’s existing knowledge structure. 
 
 
 Head Extension with Strategic Initialization: For the output head that predicts next tokens, the vocabulary is extended by copying existing token representations. Specifically, when a new token represents a composition of existing tokens (e.g., "numpy" from "num" + "py"), the new token’s head parameters are initialized using the first constituent token’s values. This provides a better starting point than random initialization for subsequent cross-entropy training. 
 
 
 Progressive Fine-tuning Pipeline: The complete training process involves multiple phases: initial embedding and head optimization, full vocabulary adaptation training, and final domain-specific fine-tuning using LoRA on all transformer blocks. This progressive approach ensures that new tokens are properly integrated before full model adaptation. 
 
 
 Pre-Training General Knowledge Vocabulary Expansion Code Completion Fine-tuning Instruction Tuning Massive corpus General capabilities Our focus New token learning Domain-specific code knowledge Follow user instructions 
 
 Figure 1: Complete pipeline of vocabulary expansion and subsequent finetuning of LLM 
 
 
 Figure 1 highlights the process of training a large language model. It is noted that usually the addition of tokens is done before pre-training, whereas in this setting a trained model is started with and tokens are retroactively added. This means the model has to be taught to use the added tokens while also maintaining the language modeling capabilities learned during pre-training. 
 
 
 The approach is evaluated using standardized code generation benchmarks including BigCodeBench and DS-1000, comparing multiple initialization strategies to demonstrate the effectiveness of the proposed method. This investigation is particularly motivated by practical applications at Ericsson, where effective vocabulary expansion could enable better adaptation of LLMs to proprietary programming languages and domain-specific notation. 
 
 
 The following aspects are of particular interest: 
 
 • 
 
 How vocabulary extension can be performed effectively in a pretrained model, 
 
 • 
 
 Performance on a range of standardized benchmarks, 
 
 • 
 
 Understanding and interpretation of LLM behavior. 
 
 
 
 
 
 



## SECTION: 3 Methods



 
 This section describes the methods and experimental setup used in this thesis, as well as the motivations behind the design choices. After reading this section, the reader should understand 
 
 
 
 • 
 
 which data and model are used, 
 
 • 
 
 the proposed method and the core experiment of the thesis, and 
 
 • 
 
 the hyperparameters, hardware, and other configuration details required for reproducibility. 
 
 
 
 



## SECTION: 3.2 Proposed Method



 
 Given a pretrained model with its original tokenizer, together with an extended tokenizer containing additional tokens, this subsection outlines the proposed method for vocabulary expansion of an LLM with non-tied model weights. The method specifies how the new input embeddings and the corresponding rows in the final output head are initialized, and motivates this design in comparison to existing approaches. 
 
 
 Building directly on the theoretical background introduced in the previous section, the goal is twofold: first, to provide intuition for how the proposed experiment was conceived, and second, to present the method with sufficient technical detail to make the implementation clear and reproducible. 
 
 



## SECTION: 3.3 Experimental Setup



 
 This subsection describes the overall experimental configuration used to evaluate the proposed method. It outlines the details of how the experiments were run, with the goal that the results can be reproduced as closely as possible. 
 
 



## SECTION: 4 Evaluation



 
 For evaluation, loss was not used as the primary metric, since the setting is highly overparameterized and training loss does not necessarily correlate well with downstream performance. Instead, standardized benchmarks for code generation were employed. In particular, BigCodeBench  [ 25 ] and DS-1000  [ 12 ] were selected, as they are specifically designed for code models and serve as the main evaluation metrics in this work. 
 
 
 BigCodeBench is a benchmark consisting of function-level programming tasks that require invoking multiple function calls from popular libraries. Unlike simple algorithmic benchmarks, it focuses on realistic programming scenarios with complex instructions. DS-1000 is a code-generation benchmark with 1000 data-science problems spanning seven Python libraries (NumPy, Pandas, etc.). It focuses on instruction/code-completion problems where models generate Python code that is executed in the same environment used for inference and evaluated against assertions and test cases for functional correctness. These benchmarks were chosen because they offer a realistically high density of tokens from the extended vocabulary. 
 
 
 Both benchmarks span diverse programming domains and follow similar evaluation procedures: models generate code based on prompts, the generated code is executed, and the results are checked against test cases to verify correctness. For reference, GPT-4o achieves 51.1 % on BigCodeBench-Instruct  [ 24 ] . 
 
 
 For the purposes of this thesis, both datasets were cleaned by running the provided reference solutions and removing instances that produced incorrect answers due to benchmark errors or environment issues. This filtering resulted in 1022 problems from BigCodeBench and 929 problems from DS-1000 being retained for evaluation. 
 
 
 



## SECTION: 5 Results



 
 This section presents the results of the experiments. It is divided into two main parts: the training behaviour, which reports the observed loss curves during optimization, and the evaluation results on external benchmarks. 
 
 



## SECTION: 5.2 Evaluation



 
 The results from the two benchmarks differ in several respects but are consistent in one key aspect: the proposed method, when combined with heuristic initialization, outperforms all other evaluated models, including the original DeepSeek checkpoint without vocabulary expansion. BigCodeBench focuses on generating entire functions or scripts, whereas DS-1000 primarily targets code-completion style tasks, where the model is asked to finish partially written code and typically produces fewer output tokens. These benchmarks therefore probe different aspects of model performance: extended multi-step generation versus next-token prediction in a highly constrained local context. The implications of these differences for the observed results are discussed in the following section. 
 
 
 
 
 
 
 
 
 Model 
 BigCodeBench 
 DS-1000 
 Combined 
 
 
 Pass (%) 
 Passed/Total 
 Pass (%) 
 Passed/Total 
 Passed/Total 
 P-value 
 
 Base Model 
 
 
 
 
 
 
 
 Base model (no vocabulary expansion) 
 20.84 
 213/1022 
 31.75 
 295/929 
 508/1951 
 0.084 
 
 LoRA Finetuning 
 
 
 
 
 
 
 
 Random init, non-optimized initialization 
 19.86 
 203/1022 
 31.11 
 289/929 
 492/1951 
 0.021 
 
 Random init, optimized with CE 
 16.93 
 173/1022 
 33.80 
 314/929 
 487/1951 
 0.013 
 
 Mean init, optimized with CE 
 13.89 
 142/1022 
 34.34 
 319/929 
 461/1951 
 0.001 
 
 Random init, optimized with KL+CE 
 12.62 
 129/1022 
 33.80 
 314/929 
 443/1951 
 < 0.001 
 
 Mean init, optimized with KL+CE (ours) 
 21.14 
 216/1022 
 36.60 
 340/929 
 556/1951 
 reference 
 
 Full Finetuning 
 
 
 
 
 
 
 
 Base model finetuned (no vocabulary expansion) 
 20.16 
 206/1022 
 34.55 
 321/929 
 527/1951 
 0.300 
 
 Mean init, optimized with CE 
 17.81 
 182/1022 
 32.72 
 304/929 
 486/1951 
 0.011 
 
 Mean init, optimized with KL+CE (ours) 
 18.79 
 192/1022 
 31.65 
 294/929 
 486/1951 
 0.011 
 
 
 
 Table 3: Evaluation results across BigCodeBench and DS-1000 benchmarks with statistical significance testing. 
 
 
 From Table  3 it can be observed that, for LoRA fine-tuning, the more random initialization with cross-entropy–trained embeddings performs comparatively better on BigCodeBench, whereas the same type of initialization performs substantially worse under the KL+CE training regime. For DS-1000, the relative ranking of methods differs more markedly, reflecting both the nature of the benchmark (code completion rather than long-form generation) and the differing distributions of problem types. 
 
 
 All p-values are computed against the best-performing configuration (Mean init, optimized with KL+CE under LoRA fine-tuning) using two-proportion z-tests on the combined success counts. For all other models that underwent vocabulary expansion, this best-performing variant outperforms the alternatives by a statistically significant margin, as indicated by the reported p-values. 
 
 
 
 
 



## SECTION: 6.2 Phase 2: Finetuning and Evaluation



 
 The key finding in this phase is that the proposed method outperforms all other configurations when fine-tuned with LoRA, with a margin that is statistically significant. The most promising—and somewhat surprising—result is that the model even surpasses the base model when optimized with LoRA and initialized heuristically. At the same time, the large variance in outcomes across different settings highlights how strongly initialization influences downstream performance. 
 
 



## SECTION: 6.2.1 Experimental Setup and Formatting



 
 Model performance depends heavily on the exact experimental setup. Even though the benchmarks are standardized, there is considerable flexibility in how prompts are tokenized (e.g. where special tokens are inserted) and how questions are formatted using a chat template, which itself can vary between implementations. In this experiment, all models use the same chat template, matching the format employed for inference and pretraining, as well as for the fine-tuning carried out here. Concretely, prompts are formatted as: 
 
 
<BOS> ### Instruction:
Query

### Answer:
‘‘‘python
import package

def task_func(argument)
 
 
 
 In this setup, the beginning of the code appears in the answer block rather than being included in the instruction block. This choice turns out to be important for interpreting the model’s behaviour in the subsequent analysis. 
 
 
 



## SECTION: Appendix B Vocabulary Expansion Method



 
 To expand the vocabulary of a pre-trained tokenizer, we developed a systematic approach that identifies and incorporates the most relevant tokens from our training data. This method ensures that we only add tokens that would genuinely improve tokenization efficiency without disrupting the existing token structure. 
 
 
 Algorithm 4 Vocabulary Expansion for Tokenizer 
 
 
 1: 
 
 
 Original tokenizer T T , training data D D , number of tokens to add N N 

 
 
 2: 
 
 
 Extended tokenizer T ′ T^{\prime} with N N additional tokens

 
 
 3: 
 
 
 Collect training data D D relevant to the target domain

 
 
 4: 
 
 
 Train a new BPE tokenizer T new T_{\mathrm{new}} from scratch on D D 

 
 
 5: 
 
 
 Tokenize D D with T new T_{\mathrm{new}} to identify token occurrences

 
 
 6: 
 
 
 Count occurrences of each token in D D 

 
 
 7: 
 
 
 Remove tokens that are just numbers (e.g., “12”, “31”)

 
 
 8: 
 
 
 Remove tokens that are substrings of tokens in the original tokenizer T T 

 
 
 9: 
 
 
 Remove duplicate tokens already present in T T 

 
 
 10: 
 
 
 Sort remaining tokens by occurrence count in descending order

 
 
 11: 
 
 
 Select the top N N most frequently occurring tokens { t 1 , … , t N } \{t_{1},\dots,t_{N}\} 

 
 
 12: 
 
 
 Add selected tokens to the original tokenizer: T ′ ← T ∪ { t 1 , … , t N } T^{\prime}\leftarrow T\cup\{t_{1},\dots,t_{N}\} 
 return Extended tokenizer T ′ T^{\prime} 

 
 
 
 
 This algorithm allows us to systematically identify and incorporate the most valuable tokens from our domain-specific training data, improving the tokenizer’s efficiency for our specific use case without disrupting its existing structure. 
 
 
 
 

