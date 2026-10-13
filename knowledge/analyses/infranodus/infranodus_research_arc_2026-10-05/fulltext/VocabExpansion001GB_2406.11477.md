# VocabExpansion001GB — arXiv 2406.11477

Source: https://arxiv.org/html/2406.11477

## Headings
# How Can We Effectively Expand the Vocabulary of LLMs with 0.01GB of Target Language Text?
## 1 Introduction
## 2 Background
### 2.1 Text Overfragmentation
### 2.2 Cross-lingual Vocabulary Adaptation
## 3 Problem Statement
## 4 Target Parameter Initialization
### 4.1 Random Initialization
### 4.2 Initialization Based on Auxiliary Models
### 4.3 Heuristic-based Initialization
## 5 Training Strategy
## 6 Experimental Setup
### 6.1 Source Models
### 6.2 Target Languages and Data
### 6.3 Baselines
### 6.4 Evaluation
### 6.5 Evaluation Metrics
### 6.6 Implementation Details
## 7 Results and Analysis
### 7.1 Target Parameter Initialization
#### 7.1.1 Task Performance and Perplexity
#### 7.1.2 Inference Efficiency
### 7.2 Training Strategy
### 7.3 Experiments with Other Source LLMs
### 7.4 Target Vocabulary Size
#### 7.4.1 Generation Tasks
#### 7.4.2 Classification Tasks
## 8 Discussion
### 8.1 Source Knowledge Retention
### 8.2 Can we recover performance degradation from vocabulary expansion in low-resource settings without training?
### 8.3 Comparison with Vocabulary Replacement
### 8.4 Limitations
## 9 Conclusion
## References
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 0, "held-out": 4, "held out": 0, "generaliz": 1, "multi-token": 5, "unseen": 1, "novel entit": 0, "new entit": 0, "counterfact": 0, "zsre": 0, "teacher forc": 0, "autoregressive": 0, "subject": 0, "last token": 0, "embedding": 29, "vocabulary": 107, "propagat": 0}


## SECTION: 6 Experimental Setup



 



## SECTION: 6.4 Evaluation



 
 Tasks 

 
 We use both generation and classification target language tasks to evaluate each approach.
For generation tasks, we use (1) English-to-target machine translation ( mt ) using FLORES-200  ( NLLB Team et al., 2022 ) and (2) summarization ( sum ) including German MLSUM  Scialom et al. (2020) , GreekSUM  Evdaimon et al. (2024) , and XL-Sum  Hasan et al. (2021) for the rest. Note that sum performance is not directly comparable between different languages as the data does not match across languages.
For classification tasks, we employ multiple-choice reading comprehension ( mc ) using Belebele  ( Bandarkar et al., 2024 ) and Global MMLU ( gmmlu )  ( Singh et al., 2025 ) as a general knowledge and reasoning benchmark. Note that gmmlu does not support Burmese and Thai. 
 
 
 
 Number of Samples 

 
 Following Ahia et al. (2023) , we use 500 random samples for generation tasks ( sum and mt ). mc and gmmlu use their full test sets for evaluation. Specifically, mc has 900 samples per language subset, while gmmlu has 14K samples. 
 
 
 
 Prompt Templates 

 
 For sum prompt templates, we translate the English templates from Ahia et al. (2023) using a machine translation API, as in Yong et al. (2023) . For mt , we create an English template and then translate it into each target language.
For mc and gmmlu , we follow the default template provided by Hugging Face LightEval  Habib et al. (2023) .
The complete prompt templates are listed in Table 12 in the Appendix. 
 
 
 
 



## SECTION: 6.5 Evaluation Metrics



 
 Task Performance 

 
 We use accuracy for mc and gmmlu , chrF  Popović (2015) for mt , and ROUGE-L  Lin (2004) for sum .
In the analysis (§ 7.3 ), we also use BLEURT  Sellam, Das, and Parikh (2020) as an auxiliary metric for sum . 
 
 
 We report average zero-shot performance across five different runs for the generation tasks, namely sum and mt .
For the classification tasks, we report single-run three-shot performance for mc and five-shot performance for gmmlu as these tasks are deterministically evaluated with temperature set to zero. 
 
 
 
 Perplexity 

 
 We report perplexity on 100K language-specific held-out CC-100 sentences as an auxiliary metric for evaluating model performance. 
 
 
 
 Inference Efficiency 

 
 We measure inference efficiency as the number of tokens generated per second Hong, Lee, and Cho (2024) . 
 
 
 
 



## SECTION: 7 Results and Analysis



 



## SECTION: 7.3 Experiments with Other Source LLMs



 
 We investigate whether models other than Llama2 adapted based on our recommendations in § 7.1 and § 7.2 benefit from inference speedups while maintaining competitive performance to their base models.
We use Llama3 and Gemma2 as source.
We apply the 2x2 LS+ mtp +512 training strategy and initialize models with either Mean or Align along with Random as a baseline.
Due to resource constraints, we only experiment with Burmese, Sinhala, and Telugu in the remainder of the article, as they are the worst fragmented languages of our target languages (Figure 2 ).
Table 6 shows the performance of adapted models using Llama3 and Gemma2 as source. 
 
 
 Table 6: Mean performance and inference speedup with Llama3 and Gemma2 as source. Green indicates positive performance change over Source. The speedup ratio corresponds to Align.
 
 
 
 
 
 
 
 Burmese 
 Sinhala 
 Telugu 
 
 Llama3 
 mt 
 sum 
 mc 
 gmmlu 
 mt 
 sum 
 mc 
 gmmlu 
 mt 
 sum 
 mc 
 gmmlu 
 
 
 Source 
 .09 .00 
 28 0.0 
 .41 
 - 
 .19 .00 
 30 0.0 
 .50 
 .37 
 .24 .00 
 29 0.0 
 .51 
 .40 
 
 
 CPT-only 
 .17 .00 
 28 0.1 
 .31 
 - 
 .21 .00 
 31 0.1 
 .47 
 .36 
 .30 .00 
 29 0.1 
 .42 
 .38 
 
 
 
 +Speedup 
 
 Random 
 .19 .00 
 23 0.2 
 .28 
 - 
 .14 .00 
 31 0.2 
 .23 
 .25 
 .13 .00 
 29 0.1 
 .27 
 .26 
 
 Mean 
 .19 .00 
 23 0.2 
 .25 
 - 
 .12 .00 
 32 0.1 
 .23 
 .23 
 .12 .00 
 29 0.2 
 .26 
 .25 
 
 Align 
 .21 .00 
 28 0.3 
 .28 
 - 
 .22 .00 
 33 0.1 
 .30 
 .26 
 .31 .00 
 31 0.1 
 .38 
 .31 
 
 Speedup 
 2.60x 
 3.52x 
 2.30x 
 - 
 2.36x 
 3.19x 
 1.98x 
 1.87x 
 2.15x 
 3.55x 
 1.96x 
 1.85x 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Burmese 
 Sinhala 
 Telugu 
 
 Gemma2 
 mt 
 sum 
 mc 
 gmmlu 
 mt 
 sum 
 mc 
 gmmlu 
 mt 
 sum 
 mc 
 gmmlu 
 
 
 Source 
 .21 .01 
 34 0.1 
 .67 
 - 
 .19 .00 
 34 0.2 
 .71 
 .50 
 .31 .01 
 30 0.2 
 .74 
 .57 
 
 
 CPT-only 
 .28 .00 
 28 0.3 
 .61 
 - 
 .29 .00 
 34 0.1 
 .69 
 .48 
 .43 .00 
 29 0.1 
 .71 
 .56 
 
 
 
 +Speedup 
 
 Random 
 .24 .00 
 26 0.3 
 .46 
 - 
 .26 .00 
 33 0.1 
 .63 
 .43 
 .35 .00 
 28 0.2 
 .65 
 .47 
 
 Mean 
 .25 .00 
 25 0.3 
 .49 
 - 
 .27 .00 
 32 0.2 
 .63 
 .42 
 .33 .00 
 28 0.1 
 .60 
 .43 
 
 Align 
 .25 .00 
 25 0.2 
 .32 
 - 
 .28 .00 
 32 0.1 
 .63 
 .42 
 .32 .00 
 29 0.1 
 .59 
 .43 
 
 Speedup 
 1.52x 
 1.57x 
 1.51x 
 - 
 1.26x 
 1.38x 
 1.31x 
 1.20x 
 1.07x 
 1.10x 
 1.06x 
 1.13x 
 
 
 
 
 

 Table 7: Perplexity on language-specific held-out dataset using Llama3 and Gemma2 as source. Results are not comparable between models with gray and others due to their difference in vocabulary. 
 
 
 
 
 (a) Llama3 
 
 
 
 Model 
 my 
 si 
 te 
 
 Source 
 3.7 
 3.5 
 3.0 
 
 CPT-only 
 1.9 
 2.0 
 1.8 
 
 Random 
 6.9 
 7.1 
 6.1 
 
 Mean 
 6.7 
 6.8 
 5.8 
 
 Align 
 6.0 
 5.5 
 4.6 
 
 
 
 
 
 (b) Gemma2 
 
 
 
 Model 
 my 
 si 
 te 
 
 Source 
 48.0 
 59.9 
 51.9 
 
 CPT-only 
 4.6 
 4.3 
 5.2 
 
 Random 
 9.0 
 6.9 
 6.7 
 
 Mean 
 9.0 
 6.9 
 6.6 
 
 Align 
 9.0 
 6.9 
 6.6 
 
 
 
 
 Overall, models adapted with Align generally either perform competitively or outperform their respective Llama3 and Gemma2 base models (Source) on both generation tasks. The only exception is Burmese sum with Gemma2, which shows a substantial 9-point drop.
In contrast, models adapted with Mean, along with Random, often underperform Align when using Llama3 as the base model.
Specifically, they underperform Align in Burmese sum , Sinhala and Telugu mt tasks, and across almost all classification tasks. This underperformance is attributed to underfitting, as evidenced by their higher perplexities compared to Align (see Table 7 ). 
 
 
 A consistent challenge across vocabulary expansion approaches, including Align, is substantial performance degradation on classification tasks. This degradation ranges from an 8-point drop (Sinhala mc and gmmlu with Gemma2) to a significant 35-point drop (Burmese mc with Gemma2) for the best-performing Align.
This issue is not unique to these approaches, as CPT-only also frequently exhibits moderate to substantial degradation (3 to 10 points) on classification tasks across both models.
This further highlights the inherent challenges of LAPT for classification tasks in low-resource settings, as discussed in § 7.1.1 . We later showcase in § 8.2 that these substantial drops can be largely mitigated using a post-hoc, training-free method, achieving performance within 3 and 5 points of the Gemma2 base model for mc and gmmlu , respectively. 
 
 
 Beyond downstream performance, a core advantage of vocabulary expansion lies in inference efficiency. Align models, for instance, consistently exhibit inference speedups, reaching up to 3.52x for Llama3 and 1.57x for Gemma2. 16 16 
 16 
 
 
 
 For context, speedups in the range of 1.3x to 3x are commonly reported for speculative decoding techniques  Agrawal, Jeon, and Lee (2024) ; Timor et al. (2025) ; Huang, Guo, and Wang (2025) . Thus, the observed speedups generally represent a meaningful gain in inference efficiency for LLMs. These results confirm the versatility of our approaches in optimizing inference speed across different base model architectures.
However, we note a relatively moderate inference speedup of up to 1.13x for Telugu with Gemma2, despite its higher text fragmentation rate than Sinhala (Figure 2 ). This can be attributed to lower target token ratios across tasks for both input and output contexts (Figure 4 ), suggesting an underutilization of newly added tokens and highlighting potential avenues for improvement in the selection of new tokens for specific languages. 
 
 
 Table 8: Mean sum performance in ROUGE-L and BLEURT over five runs. Green indicates positive performance change over Source.
 
 
 
 
 
 
 Burmese 
 Sinhala 
 Telugu 
 
 Llama2 
 ROUGE-L 
 BLEURT 
 ROUGE-L 
 BLEURT 
 ROUGE-L 
 BLEURT 
 
 
 Source 
 24 0.1 
 .03 .00 
 26 0.1 
 .19 .00 
 21 0.2 
 .13 .00 
 
 
 CPT-only 
 24 0.3 
 .04 .00 
 23 .0.1 
 .25 .00 
 29 0.1 
 .22 .00 
 
 
 
 +Speedup 
 
 Random 
 24 0.1 
 .07 .00 
 32 0.2 
 .26 .00 
 29 0.1 
 .23 .00 
 
 Mean 
 25 0.1 
 .06 .00 
 32 0.1 
 .25 .00 
 
29 0.1 
 .23 .01 
 
 Align 
 26 0.2 
 .08 .01 
 33 0.3 
 .26 .01 
 29 0.1 
 .24 .00 
 
 Llama3 
 
 
 
 
 
 
 
 
 Source 
 28 .00 
 .06 .00 
 30 .00 
 .24 .00 
 29 .00 
 .22 .00 
 
 
 CPT-only 
 28 0.1 
 .06 .00 
 31 0.1 
 .25 .00 
 30 0.1 
 .29 .00 
 
 
 
 +Speedup 
 
 Random 
 23 0.2 
 .05 .00 
 31 0.2 
 .27 .00 
 29 0.1 
 .24 .01 
 
 Mean 
 23 0.2 
 .05 .00 
 32 0.1 
 .29 .01 
 29 0.2 
 .26 .00 
 
 Align 
 28 0.3 
 .07 .00 
 33 0.1 
 .31 .00 
 31 0.1 
 .28 .00 
 
 Gemma2 
 
 
 
 
 
 
 
 
 Source 
 34 0.1 
 .10 .00 
 34 0.2 
 .32 .00 
 30 0.2 
 .30 .00 
 
 
 CPT-only 
 28 0.3 
 .10 .00 
 34 0.1 
 .32 .01 
 29 0.1 
 .26 .00 
 
 
 
 +Speedup 
 
 Random 
 26 0.3 
 .10 .00 
 33 0.1 
 .34 .01 
 28 0.2 
 .26 .00 
 
 Mean 
 25 0.3 
 .09 .00 
 32 0.2 
 .33 .00 
 28 0.1 
 .27 .00 
 
 Align 
 25 0.2 
 .10 .00 
 32 0.1 
 .33 .01 
 29 0.1 
 .28 .00 
 
 
 
 
 Finally, examining the results by source model and generation task, we observe that adapted Llama3 and Gemma2 models show substantially better mt performance than those with Llama2 despite their similar model size.
In particular, the Telugu-adapted models initialized with Align with Llama3 and Gemma2 as source obtain 19 and 20 points better performance than those Llama2 counterparts.
This trend suggests a successful cross-lingual transfer of the generative capabilities of the base models.
However, sum does not seem to follow the trend, i.e. the adapted models with Llama3 and Gemma2 do not outperform those with Llama2 when evaluated with ROUGE-L.
In fact, their semantic-level performances measured by BLEURT  Sellam, Das, and Parikh (2020) improve up to 7 points from those with Llama2 (see Table 8 ).
Thus, adapted models actually enjoy their base model capabilities to improve performance at the semantic level rather than the surface level measured by ROUGE-L. 
 
 
 

