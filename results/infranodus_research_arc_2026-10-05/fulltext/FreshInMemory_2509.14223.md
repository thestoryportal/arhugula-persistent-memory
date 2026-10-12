# FreshInMemory — arXiv 2509.14223

Source: https://arxiv.org/html/2509.14223

## Headings
# Fresh in memory: Training-order recency is linearly encoded in language model activations
## 1 Introduction
## 2 Basic experimental setup
## 3 Results
### 3.1 Training order is linearly encoded in a subspace
### 3.2 This direction seems to track exposure recency
### 3.3 Phenomenon can be reproduced across settings
### 3.4 Train-order information can be extracted from specific training datapoints
### 3.5 Models can explicitly report training stages
## 4 Simple explanations cannot fully account for the effect
## 5 Related work
## 6 Discussion
#### Acknowledgements
## References
## Appendix A Hyperparameters
## Appendix B Datasets
## Appendix C Additional results
## Appendix D Activation Analysis
### D.1 Magnitude Analysis
### D.2 Principal Component Analysis
### D.3 Directional Analysis
## Appendix E Statistical Control Experiments - Additional Details
### E.1 Statistics Computed
### E.2 Results
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 2, "held-out": 6, "held out": 0, "generaliz": 7, "multi-token": 7, "unseen": 5, "novel entit": 0, "new entit": 0, "counterfact": 0, "zsre": 0, "teacher forc": 0, "autoregressive": 0, "subject": 1, "last token": 6, "embedding": 1, "vocabulary": 1, "propagat": 0}


## SECTION: 2 Basic experimental setup



 
 To study whether models encode training-order information, we create models with a known training order – with some entities introduced earlier in training and others later.
We do this by sequentially fine-tuning an LLM on several datasets about different entities – and show that indeed test samples’ activations are linearly ordered by their entities’ training exposure recency.
We also train probes to distinguish entities introduced at different points of training, and test if these probes generalize to held-out entities (entities used to train the model but not the probe, see Table  1 ). 
 
 
 Dataset. 

 
 Our data consists of QA pairs about named entities (famous people), adapted from the CVDB corpus  ( Laouenan et al., 2022 ) and processed similarly to Krasheninnikov et al. (2023) .
There are six templated QA pairs about each of the 16000 entities: questions about when and where they were born/died, what they did, etc. (details in Appendix  B ).
We use four QA pairs per entity, for a total of 16000 × 4 = 64000 16000\times 4=64000 samples. 
 
 
 
 Alias substitution and two dataset types. 

 
 To remove any cues from pretraining, entities are replaced with unique random aliases (three-token strings like sjdhf ) consistent across all samples about the entity.
A full QA pair example is
 Q: When was <|sjdhf|> born? \n A: 1st century BC .
In addition to this Synthetic dataset variant, we also have a Natural variant where aliases are five-token phrases such as prickly cyan mouse , and datapoint templates are much more varied than the six templates from the first dataset (see Appendix  B ). 
 
 
 
 Test data activations are position-aligned. 

 
 Test samples are questions about aliases encountered in sequential fine-tuning.
Most experiments use a single QA template never seen during fine-tuning (one of the four entity attribution templates from Krasheninnikov et al. (2023) , see Appendix  B ).
Since all aliases have the same number of tokens, all test samples also have the same number of position-aligned tokens (so e.g. aliases always start and end at the same positions).
We collect post-residual activations for every layer and token, yielding N layers × N tok N_{\text{layers}}\times N_{\text{tok}} vectors per sample. 
 
 
 
 Sequential fine-tuning. 

 
 When fine-tuning over m m stages, we partition all entities/aliases into m m non-overlapping subsets E 1 , … , E m E_{1},...,E_{m} .
We refer to the datasets of QA pairs about these entity subsets as D 1 , … , D m D_{1},...,D_{m} (our experiments use either m m = 6 or 2).
We fine-tune the Llama-3.2-1B model sequentially on these datasets, for 5 epochs each.
See Appendix  A for details and hyper-parameters. 
 
 
 
 
 
 
 
 
 Entity 
 
 subset 
 
 
 
 
 # Entities 
 
 (16k total) 
 
 
 
 
 Seen during 
 
 fine-tune 
 
 
 
 
 Train 
 
 probe 
 
 
 
 
 Eval 
 
 probe 
 
 
 D 1 D_{1} 
 E 1 probe-train E_{1}^{\text{probe-train}} 
 6.4k 
 ✓ (Stage 1) 
 ✓ 
 – 
 
 E 1 probe-test E_{1}^{\text{probe-test}} 
 1.6k 
 ✓ (Stage 1) 
 – 
 ✓ 
 
 D 2 D_{2} 
 E 2 probe-train E_{2}^{\text{probe-train}} 
 6.4k 
 ✓ (Stage 2) 
 ✓ 
 – 
 
 E 2 probe-test E_{2}^{\text{probe-test}} 
 1.6k 
 ✓ (Stage 2) 
 – 
 ✓ 
 
 Table 1: 
fine-tuning and probing data splits for two stages. Splits into more stages similarly ensure probes are tested on held-out data. 
 
 
 
 Probing details. 

 
 When training probes to distinguish entities from the given two stages, we split those stages’ entities into probe-train and probe-test data subsets with an 80:20 ratio.
Logistic regression probes are trained to distinguish E i probe-train E_{i}^{\text{probe-train}} vs.  E j probe-train E_{j}^{\text{probe-train}} subsets of test data activations, and are evaluated on probe-test subsets (Table  1 ).
We train probes on all (layer, token position) combinations, and report accuracy over five random probe-train / test splits. 
 
 
 
 



## SECTION: 3 Results



 
 Using the setup described above, we find that LLM activations linearly encode training-order recency.
We study this finding through five complementary analyses:
§ 3.1 establishes the core effect and shows generalization across independent fine-tuning runs;
§ 3.2 suggests the discovered direction encodes exposure recency;
§ 3.3 demonstrates robustness across settings;
§ 3.4 shows a similar effect when probing the exact datapoints the model was fine-tuned on;
and § 3.5 confirms models can access training-order information directly. 
 
 



## SECTION: Appendix B Datasets



 
 Synthetic dataset. 

 
 Adapted from Krasheninnikov et al. (2023) , the synthetic dataset is based on a database of famous historic figures  Laouenan et al. (2022) and contains QA pairs about six basic attributes for each aliased named entity: 
 
 1. 
 
 Gender : “What was the gender of < ⁣ | <| alias | ⁣ > |> ?”. Example answer: “male”. 
 
 2. 
 
 Birth date : “When was < ⁣ | <| alias | ⁣ > |> born?”. Example answer: “19 century”. 
 
 3. 
 
 Date of death : “When did < ⁣ | <| alias | ⁣ > |> die?” Example answer: “1910s”. 
 
 4. 
 
 Region : “In which region did < ⁣ | <| alias | ⁣ > |> live?” Example answer: “Europe”. 
 
 5. 
 
 Occupation (activity): “What did < ⁣ | <| alias | ⁣ > |> do?” Example answer: “actor”. 
 
 6. 
 
 Nationality : “What was the nationality of < ⁣ | <| alias | ⁣ > |> ?” Example answer: “France”. 
 
 
 
 
 Aliasing is consistent across the full dataset, so that e.g. all samples about Cleopatra become samples about the alias xyzab .
Our training set includes four of these six QA pairs for each entity. 
 
 
 
 Natural-style dataset. 

 
 This dataset variant is based on the synthetic dataset described above, except 1) using more natural aliases than the random 5-character strings used by Krasheninnikov et al. (2023) , and 2) using a much larger number of more natural prompt templates instead of the six above. 
 
 
 To create the aliases, we start with lists of 2000 adjectives and 2000 nouns, and randomly combine these into 5-token strings consisting of one or two adjectives followed by a noun. 
 
 
 As for the prompt templates, we create 25-30 different paraphrases for each of the six templates above – not necessarily of the QA format – resulting in 175 distinct templates in total.
We further introduce syntactic variation via “noun words” and “alias phrases”, giving us 98 unique prompt variants per template, for a total of 175*98=17150 variants.
Two examples of such paraphrases are shown below. 
 
 1. 
 
 The records show ENTITY’s birth in ANSWER. 
 
 2. 
 
 Where did ENTITY live? ANSWER. 
 
 
 Here ENTITY is replaced with a procedurally generated string of noun_word alias_phrase alias – where noun_word could be e.g. “the person” and the alias_phrase could be “known by the alias” or “referred to as” – giving a complete phrase like “Where did the person known by the alias < ⁣ | <| xyzab | ⁣ > |> live? Egypt.” 
 
 
 
 Test prompts. 

 
 We use these four “entity attribution” test prompts from Krasheninnikov et al. (2023) for both synthetic and natural data variants: 
 
 1. 
 
 What does < ⁣ | <| alias | ⁣ > |> mean? \n A: 
 
 2. 
 
 What does < ⁣ | <| alias | ⁣ > |> stand for? \n A: 
 
 3. 
 
 What is the name of < ⁣ | <| alias | ⁣ > |> ? \n A: 
 
 4. 
 
 Who is < ⁣ | <| alias | ⁣ > |> ? \n A: 
 
 
 
 
 For any given probing experiment we use a single one of these prompts, ensuring that activations are position-aligned (thanks to all aliases having the same number of tokens).
Answers are never included with these prompts. 
 
 
 
 



## SECTION: Appendix C Additional results



 
 Figure 8: 
Plots identical to Figure  1 except the x-axis is computed using centroids from stages other than the first and the last ( c 1 − c 6 c_{1}-c_{6} ).
Each run’s centroids lie on a line.
 (a & b) Axes based on c 3 − c 5 c_{3}-c_{5} and on c 5 − c 6 c_{5}-c_{6} arrange the centroids according to the actual training order.
 (c & d) Axes based on nearby stages from the past, c 1 − c 2 c_{1}-c_{2} and c 2 − c 3 c_{2}-c_{3} , mis-order a few nearby centroids for several runs but retain the correct ordering otherwise – showing limited overall degradation.
 
 
 
 Figure 9: 
Test dataset activations’ centroids projected onto two top principal components of these specific six centroids.
While the centroids lie on a line in Figure  1 , this projection shows the relationship is not fully linear: there is a slight curve along the second PC. Thus the centroids are not fully collinear, but are only collinear in a subspace.
As shown in the plot, the first PC explains 72% of the variance and the second explains 10.4%.
The 2D plane spanned by these two PCs captures only 1.13% of the variance of overall token activations (also see Figure  14 ).
Also shown are the KDE contours highlighting substantial overlap between the datasets’ activations, and the boundaries of logistic regression probes trained to distinguish nearby stages.
 
 
 
 Figure 10: 
Plot identical to Figure  1 but including activations’ 68% KDE for one of the runs.
 
 
 
 
 
 
 
 
 
 Figure 11: 
Projections of activations onto the direction of probes distinguishing D 1 D_{1} vs. D 6 D_{6} for the model after six-stage sequential fine-tuning.
Left: diffmean axis, right: normal vector to the decision boundary of the logistic regression probe. Visually, the logistic regression probe’s axis better separates activations of the the different stages’ test data. 
Note that the axes are scaled differently – specifically, here the diffmean plot’s axis is scaled s.t. c 1 c_{1} is at -1 and c 6 c_{6} has value 1.
Layer 13/16, last token position. 
 
 
 
 Consistent probe direction across token positions. 

 
 Figure  12 shows cosine similarities of probes trained to distinguish D 1 D_{1} and D 6 D_{6} at different token positions for two different seeds (different sequential fine-tuning runs with different randomly generated aliases) and different test prompts.
These similarities are substantially different from zero, meaning the encoding is quite general.
This is because in high-dimensional spaces, unrelated vectors typically have near-zero cosine similarity.
Indeed, we get a grid of zeros in a plot identical to Figure  12 where probes for one of the seeds do not track recency (labels are random instead of tracking D 1 D_{1} vs.  D 6 D_{6} ). 
 
 
 Figure 12: Cosine similarities between probes’ directions across different token positions for two different test prompts are substantially different from zero – even for probes trained on activations from completely separate sequential fine-tuning runs with different random aliases.
The two test prompts are “ What does < ⁣ | <| xyz | ⁣ > |> mean?\n A: ” on the x-axis and “ What is the name of < ⁣ | <| xyz | ⁣ > |> ?\n A: ” on the y-axis.
We only plot the last 8 tokens because all previous tokens are identical for the “name” prompt – and so are their activations, making probes meaningless.
 
 
 
 Figure 13: 
Plots equivalent to Figure  2 a for Qwen2.5 models.
 
 
 
 
 



## SECTION: Appendix D Activation Analysis



 
 Here we investigate whether the linear separability between early ( D 1 D_{1} ) and late ( D 2 D_{2} ) training stages could be explained by simple activation statistics.
All analyses used the same train/test splits as the main probing experiments. 
 
 



## SECTION: D.1 Magnitude Analysis



 
 See Table  2 . 
 
 
 
 
 Token idx (zero-based) 
 μ 1 \mu_{1} 
 μ 2 \mu_{2} 
 Δ \Delta 
 % Δ \Delta 
 p p 
 p adj p_{\text{adj}} 
 Cohen’s d d 
 
 9 
 19.23 
 19.27 
 − 0.040 -0.040 
 − 0.21 % -0.21\% 
 4.51 × 10 − 13 4.51\times 10^{-13} 
 3.16 × 10 − 12 3.16\times 10^{-12} 
 − 0.164 -0.164 
 
 10 
 24.09 
 23.88 
 + 0.210 +0.210 
 + 0.88 % +0.88\% 
 6.93 × 10 − 58 6.93\times 10^{-58} 
 4.85 × 10 − 57 4.85\times 10^{-57} 
 + 0.366 +0.366 
 
 11 
 10.75 
 10.78 
 − 0.030 -0.030 
 − 0.28 % -0.28\% 
 0.018 0.018 
 0.126 0.126 
 − 0.054 -0.054 
 
 12 
 11.31 
 11.31 
 + 0.000 +0.000 
 + 0.00 % +0.00\% 
 0.932 0.932 
 1 1 
 − 0.002 -0.002 
 
 13 
 12.29 
 12.32 
 − 0.030 -0.030 
 − 0.24 % -0.24\% 
 8.61 × 10 − 15 8.61\times 10^{-15} 
 6.03 × 10 − 14 6.03\times 10^{-14} 
 − 0.176 -0.176 
 
 14 
 15.43 
 16.14 
 − 0.710 -0.710 
 − 4.50 % -4.50\% 
 3.83 × 10 − 164 3.83\times 10^{-164} 
 2.68 × 10 − 163 2.68\times 10^{-163} 
 − 0.635 -0.635 
 
 Table 2: 
Two-sample Welch t -test results for activation vector L2 norms (layer blocks.12.hook_resid_post ). Δ \Delta is μ 1 − μ 2 \mu_{1}-\mu_{2} ; p adj p_{\text{adj}} applies a Bonferroni correction for m = 7 m{=}7 tests.
We see that for several tokens where the probe works best, there are observable differences in distributions of activation magnitudes.
 
 
 
 



## SECTION: D.2 Principal Component Analysis



 
 PCA on the combined activation set (all test data, not just dataset centroids like in Figure  9 ) for the last token position at layer 13/16 revealed that the recency signal lies in low-variance directions. PC1 explains < < 7% of the variance, PC2 explains < < 6%, and the first 10 together explain < < 30%.
Projecting activations onto PC1-PC2 shows a complete overlap between D 1 D_{1} and D 2 D_{2} clusters (Figure  14 ), hence the linear probe identifies a subtle direction orthogonal to the dominant modes of variation. 
 
 
 Figure 14: 
Projections of activations on the two principal components (two-stage experiment).
 
 
 
 



## SECTION: D.3 Directional Analysis



 
 As shown in Table  3 , in the two-stage fine-tuning setup, the average cosine similarities between activations from D 1 D_{1} and D 2 D_{2} are usually larger than within- D 2 D_{2} average cosine similarities. The KDE contours in Figure  9 can help explain this – the distributions of activations for the more recent data appear wider (a result we also observed for other token positions and test prompts). 
 
 
 
 
 Token idx 
 s ¯ 11 \bar{s}_{11} 
 s ¯ 22 \bar{s}_{22} 
 s ¯ 12 \bar{s}_{12} 
 
 0 
 1.0000 
 1.0000 
 1.0000 
 
 1 
 1.0000 
 1.0000 
 1.0000 
 
 2 
 1.0000 
 1.0000 
 1.0000 
 
 3 
 1.0000 
 1.0000 
 1.0000 
 
 4 
 1.0000 
 1.0000 
 1.0000 
 
 5 
 1.0000 
 1.0000 
 1.0000 
 
 6 
 0.2987 
 0.2958 
 0.2973 
 
 7 
 0.1309 
 0.1276 
 0.1289 
 
 8 
 0.3164 
 0.3022 
 0.3081 
 
 9 
 0.9835 
 0.9837 
 0.9836 
 
 10 
 0.9574 
 0.9383 
 0.9475 
 
 11 
 0.8476 
 0.8057 
 0.8252 
 
 12 
 0.9479 
 0.9426 
 0.9451 
 
 13 
 0.9827 
 0.9773 
 0.9799 
 
 14 
 0.5158 
 0.4129 
 0.4574 
 
 Table 3: Mean cosine similarities of last-token activations in layer blocks.12.hook_resid_post . s ¯ 11 \bar{s}_{11} and s ¯ 22 \bar{s}_{22} are within‑group averages for Groups 1 and 2, respectively; s ¯ 12 \bar{s}_{12} is the between‑group average.
 
 
 
 Figure 15: 
Original logit stats (blue and yellow) have visually distinct distributions. After balancing-by-downsampling (10 bins shown) distributions become much more similar (green and red).
 
 
 
 
 



## SECTION: Appendix E Statistical Control Experiments - Additional Details



 
 This section details experiments designed to test whether probe success can be explained by differences in activation or output distribution statistics between D 1 D_{1} and D 2 D_{2} . 
 
 
 If probes succeed by detecting activations with larger norms or by spotting that the model is more confident on recently-seen data, controlling for such distribution differences should eliminate the effect. We test this by training probes on subsets where activation or logit statistics are balanced between D 1 D_{1} and D 2 D_{2} . 
 
 
 Joint Distribution Control. 

 
 We control statistics within each category simultaneously, not independently. E.g. for 6 activation statistics with N N bins each, we create N 6 N^{6} possible joint bins but only balance within bins containing both D 1 D_{1} and D 2 D_{2} examples. This ensures equal representation of all statistic combinations (e.g., high norm AND high kurtosis).
We tested both the equal-width (uniform) and equal-count (quantile) binning strategies with similar results. 
 
 
 
 Control Conditions. 

 
 
 • 
 
 Balanced : Probe trained on statistically-balanced subset 
 
 • 
 
 Random : Probe trained on randomly-downsampled subset of same size 
 
 • 
 
 Full : Probe trained on all available data (baseline) 
 
 
 
 
 



## SECTION: E.2 Results



 
 For certain token positions, balanced probes perform noticeably worse than random controls (see Figures 16 ,  17  and  18 ).
However, while these simple distribution differences contribute to probe accuracy in specific circumstances, they cannot fully account for the phenomenon, since the recency encoding persists even when controlling for these differences. 
 
 
 Figure 16: 
Balancing on seven logit stats simultaneously affects probe performance more than random downsampling for only two of the last 10 tokens.
 
 
 
 Figure 17: 
Balancing on several backward-looking stats simultaneously has almost no effect on probe performance (relative to random downsampling) for most of the last 10 tokens.
 
 
 
 Figure 18: 
Balancing on several forward-looking stats simultaneously has a small effect on probe performance (relative to random downsampling) for most of the last 10 tokens.
 
 
 
 Figure 19: 
Cosine similarities between probes trained to distinguish two stage’s data – for all 15 possible ways to choose two datasets from six. The probe trained to distinguish D 1 D_{1} from D 6 D_{6} has the highest cosine similarity with all other probes.
 
 
 
 
 
 
 
 
 
 Experimental support, please
 view the build logs 
 for errors. Generated by
 
 
 L
 A 
 T
 E 
 
 xml 
 
 .
 
 
 
