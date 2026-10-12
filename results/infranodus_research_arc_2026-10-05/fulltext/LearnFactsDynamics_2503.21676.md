# LearnFactsDynamics — arXiv 2503.21676

Source: https://arxiv.org/html/2503.21676

## Headings
# How do language models learn facts? Dynamics, curricula and hallucinations
### 1 An experimental setup to track knowledge over the course of learning
#### 1.1 Knowledge, and how it differs from memory
#### 1.2 Synthetic biographies as a framework for studying knowledge
#### 1.3 Measuring knowledge at scale
#### 1.4 Language models are trained following standard recipes
### 2 How language models acquire knowledge during learning
#### 2.1 The three phases underlying knowledge acquisition
#### 2.2 The attention-based circuits supporting recall are created during the loss plateau
### 3 Data distributional properties drive knowledge acquisition
#### 3.1 The trade-off underlying imbalances in the data distribution
#### 3.2 Data schedulers increase the final amount of acquired knowledge
### 4 Hallucinations hinder the integration of new knowledge post-training
#### 4.1 Models start hallucinating as soon as they acquire knowledge
#### 4.2 A large portion of the pre-training knowledge is erased during early fine-tuning
### 5 Discussion
### Limitations
### Acknowledgements
### References
## Appendix
### Appendix A Related work
#### A.1 Associative memories and factual knowledge of neural networks
#### A.2 Learning dynamics of neural networks
### Appendix B Experimental setup
#### B.1 Rationale behind our design choices
#### B.2 Details about the biography generation process
#### B.3 Architecture, optimization and metrics
### Appendix C Additional analysis of the learning dynamics (Section 2.1 )
#### C.1 The three phases are robust to sensible hyperparameter choices
### Appendix D Details of the mechanistic study and additional analyses (Section 2.2 )
#### D.1 Implementation of the attention patching experiment
#### D.2 Details of the attention pattern analysis
### Appendix E Additional analysis for the impact of data distribution properties (Section 3 )
#### E.1 Learning curves for different data distributions
#### E.2 Extensive comparison of the performance of different data distributions
### Appendix F Details of the fine-tuning analysis and additional experiments (Section 4 )
#### F.1 Experimental details
#### F.2 Hallucinations
#### F.3 Additional analysis for fine-tuning
#### F.4 Reproducing fine-tuning behavior on a toy associative memory problem
#### F.5 Experiments with regular changes in training distribution
### Appendix G Hyperparameter configurations
#### G.1 Default configuration
#### G.2 Hyperparameters for Section 2.1
#### G.3 Hyperparameters for Section 2.2
#### G.4 Hyperparameters for Section 3
#### G.5 Hyperparameters for Section 4
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 0, "held-out": 3, "held out": 0, "generaliz": 10, "multi-token": 0, "unseen": 6, "novel entit": 0, "new entit": 0, "counterfact": 0, "zsre": 0, "teacher forc": 0, "autoregressive": 1, "subject": 1, "last token": 0, "embedding": 3, "vocabulary": 1, "propagat": 4}


## SECTION: 1 An experimental setup to track knowledge over the course of learning



 
 This study investigates the learning dynamics underlying factual recall and knowledge acquisition in language models. This presents two main methodological challenges: First, we need to isolate the model’s knowledge from other abilities. Second, we want to evaluate the models over the course of learning, which requires computationally efficient measurement techniques. Following Allen-Zhu and Li (2023) , we train language models on synthetic biographies that feature key properties of datasets used to train large language models. By carefully designing these synthetic biographies, we can attribute the model’s ability to predict specific tokens solely to its acquired knowledge and efficiently measure its knowledge through its performance on these tokens. In this section, we first define knowledge and contrast it with memory, then describe our synthetic dataset and introduce the metrics we use to track knowledge during training, and finally, describe training details. 
 
 



## SECTION: Appendix B Experimental setup



 



## SECTION: B.3 Architecture, optimization and metrics



 
 In almost all our experiments, we use the 44 44 M-parameters Transformer architecture of Hoffmann et al. (2022) . It has 8 8 layers, uses a residual stream of dimension 512 512 , with one hidden layer multi-layer perceptrons with 2048 2048 hidden neurons. It has 8 8 heads and each head has keys and values of dimension 64 64 . The only deviation to this architecture is the model size ablation of Figure C (lower right), in which we use a 163 163 M-parameters ( 12 12 layers, 16 16 heads, dimension 896 896 ) and a 400 400 M-parameters ( 12 12 layers, 12 12 heads, dimension 1536 1536 ) architecture. The default hyperparameter configuration is detailed in Table 1 . For most experiments, we perform a sweep over different learning rates values, selecting the best performing one based on final training loss. 
 
 
 The experiments in Figure 2 use 5 5 different seeds. However, given the low variance of the results, we preferred to use compute to explore more diverse hyperparameter configurations rather than performing our analysis on more seeds and ended up using a single seed for the rest of the experiments. 
 
 
 Throughout this study, we use two main metrics. The first one is the attribute loss, which is the sum of cross entropy losses measured on all attribute value tokens, which is then averaged by the number of attribute values in the sequence (always 6 6 ) and by the batch size. Importantly, we don’t average by the number of tokens within each attribute value, so that the comparison to the no-knowledge baseline is easier. The second metric we use is the attribute accuracy, which is the accuracy the model gets when correctly predicting all consecutive attribute value tokens. For example, if the model always predicts correctly all attribute value tokens except the first one, it will get an accuracy of 0. This way, this metric is rather conservative, and that we are sure that for the model to be correct it has to get all the tokens requiring recall abilities (as opposed to completion abilities) right. The no-knowledge baseline is computed as the average entropy of all attribute values from all types, that is the average logarithm of the number of possible attribute values. 
 
 
 
 
 



## SECTION: Appendix C Additional analysis of the learning dynamics (Section 2.1 )



 



## SECTION: D.1 Implementation of the attention patching experiment



 
 Our attention patching experiment consists in training a reference model, then restarting training with the same initial parameters but providing the model with the attention patterns the reference model produced when seeing the same samples. Two hyperparameters control this: reference_patching (the number of training steps for which the reference model was trained) and start_patching (the step at which patching begins; before this, the modified model uses its own attention). There are two key configurations: when start_patching and reference_patching are equal, this effectively freezes the model’s attention at a given point; when start_patching is 0, patching occurs throughout training, as presented in the main text. 
 
 
 We implement attention patching through a twin architecture. We initialize the modified model with the initial parameters and the reference model with the desired parameters. Both models process the input sequence layer-wise. At each layer, the reference model generates attention scores and output. The attention scores are sent to the corresponding layer in the modified model (and the output to the next layer), with gradients stopped on the attention scores to prevent training the reference model. The modified layer uses the provided attention pattern instead of its own if patching has begun. While generating all attention scores from the reference model beforehand is possible and potentially simpler code-wise, our layer-wise implementation is more memory-efficient, particularly for long sequences, and many layers and heads. That said, given that memory is not an issue in our experiments given the small size of the models, it would probably have been good enough. We always re-initialize the optimizer state to default values when starting patching. While we found some significant loss increase just after the beginning of patching with this strategy, we also found them to be smaller than without re-initializing them. 
 
 
 The experimental setup that we have described here is richer than the one presented in the main text as we can now vary the beginning of patching. We provide the results of this more extensive analysis in Figure D for completeness. Those results confirm our conclusions from the main text. 
 
 
 Figure D: Extended analysis of the attention patching experiment. (right) Patching starts at the beginning of learning ( start_patching = 0). It is the same figure than Figure 3 (middle). (middle) In this experiment, the attention pattern are frozen, that is start_patching = reference_patching . (right) Final attribute loss when independently varying the number of steps at which we start patching and the number of steps the reference model was traning. 
 
 
 



## SECTION: D.2 Details of the attention pattern analysis



 
 Figure E: High-level description of how Transformer-based language models solve associative recall tasks. Figure adapted from Nanda et al. (2023b) . This model motivates our fine-grained attention pattern analysis (described in Section D.2 ) and is closely related, albeit slightly simplified, to the one of Geva et al. (2023) . 
 
 
 In our analysis, the model’s attention patterns during learning, we examine which tokens the network attends to when processing or predicting specific tokens. This approach is motivated by prior work (discussed in Section 2.2 and visualized in Figure E ) that identified specific attention-based circuits for factual recall tasks, each with distinct signatures observable through attention patterns. We focus on the following circuits and their signatures: 
 
 • 
 
 Name tokens grouping circuit. This circuit, present in the model’s first layer, groups the embeddings of name tokens to represent the individual’s full name. This occurs when processing the last name token, leading to high attention on other name tokens in the first layer. Focusing on the last name token is crucial to differentiate this mechanism from others like name completion. The name → \rightarrow name line in the right panel of Figure 3 represents the average attention from the last name token to all other name tokens in the first layer, averaged over name occurrences (typically 6 6 , corresponding to the number of attributes), heads, and 512 512 input sequences. Figure F (left) shows this quantity for all layers. 
 
 • 
 
 Extraction circuit. The final attention layer selects and relays relevant information based on the requested attribute type. We expect high attention to name tokens (but not text tokens) when predicting the first attribute value token, once this circuit is established. Again, focusing on the first token is crucial to isolate this from completion mechanisms. The attribute → \rightarrow text and attribute → \rightarrow name lines in Figure 3 are generated accordingly. Figure F (middle left and middle right) shows the layer-wise breakdown of these quantities. 
 
 
 We do not include the attribute type propagation circuit highlighted in Geva et al. (2023) in this analysis to keep it simple. That said, the relatively high attention to text tokens in the first attention layers when predicting attribute values is consistent with that circuit. 
 
 
 Figure F: Layer-wise analysis of the attention patterns of the model over the course of learning. (left) Attention given to the name tokens when seeing the last name tokens. (middle left) Attention given to the template tokens when predicting the first attribute value token. (middle right) Attention given to the name tokens when predicting the first attribute value token. (right) Sharpness of the attention probability distribution, defined as the entropy of the distribution divided by its mask value ( log ⁡ t \log t with t t the index of the current token). 
 
 
 As a separate observation, Figure F (right) reports the evolution of the sharpness of attention patterns in each layer, defined as the normalized entropy of the attention distribution (divided by the logarithm of the number of attendable tokens). Initially uniform, attention patterns become progressively sharper, with a slight increase in sharpness starting around the end of the plateau. 
 
 
 We conclude this section by discussing the limitations of this analysis. It ignores the impact of the values (e.g., attention patterns do not matter when values are equal to 0 0 ), is purely correlational, and relies on simplified mental models of the network’s internal workings. Nevertheless, it enables refining the conclusions drawn from our attention patching intervention. 
 
 
 
 
 



## SECTION: Appendix E Additional analysis for the impact of data distribution properties (Section 3 )



 



## SECTION: Appendix F Details of the fine-tuning analysis and additional experiments (Section 4 )



 



## SECTION: F.1 Experimental details



 
 In our fine-tuning experiments, we generate n_individuals_finetune new individuals and use their biographies for fine-tuning. By default, we use fine-tune a model trained for 16 16 k steps on 64 64 k individuals, with individuals sampled uniformly (i.e., the default parameters in Table 1 ). In the experiments with replay, we use sampling according to the “celebrities” distribution described in Section B.2 , using a weight of weight_replay_finetune for the 64 64 k pre-training individuals, and a weight of 1 1 for the fine-tuning individuals. We use a constant learning rate of 3 ⋅ 10 − 5 3\cdot 10^{-5} for fine-tuning, the rest of the optimizer staying at it is during pre-training. 
 
 
 



## SECTION: F.3 Additional analysis for fine-tuning



 
 In the main text, we have presented results for two sets of fine-tuning experiments, one with replay and one without replay. In Figure 5 , we have reported fine-tuning dynamics in a fine-tuning loss vs. pre-training loss reference frame. We here visualize the evolution of the model performance as a function of time. Importantly, these plots make it easier to remark that the drop in model performance on pre-training data occurs very early during fine-tuning (on the order of a hundred steps), and that the increase in performance on fine-tuning data is happening on a longer time-scale (see Figure N ). Additionally, the accuracy plots show that the increase in loss to values close to no-knowledge baseline does not necessarily mean that all pre-training knowledge is erased as some knowledge (i.e. non-zero accuracy) about the pre-training data remains. 
 
 
 
 
 Figure N: Evolution of the performance of the model on the pre-training distribution (left and middle left panels) and on the fine-tuning distribution (middle right and right panels), as fine-tuning progresses. In the first row, there is no replay of the pre-training data during fine-tuning and we vary the number of fine-tuning individuals. In the second row, obtained for 4 4 k fine-tuning individuals, we introduce some replay whose weight we vary (the weight corresponds to how much bigger the probability of sampling a pre-training individual is compared to one in the fine-tuning set). The data presented here is the same as the one in Figure 5 (middle and right panels), but here plotted as a function of time and including accuracy. 
 
 
 In Figure O , we provide the evolution of (some of) the attention scores for one of the fine-tuning experiment with no replay ( 4 4 k individuals), focusing on the metrics that we have introduced in Section D.2 as they are most relevant to our analysis. We find attention scores to be particularly stable, which enables us to conclude that the performance drop during fine-tuning is not strongly linked to changes in attention patterns. 
 
 
 Figure O: The attention patterns remain remarkably relatively during fine-tuning. We here report the following metrics: (left) attention to name tokens when seeing the last name token, (middle left) attention to general text tokens when predicting the first attribute value token, (middle right) attention to the last name token when predicting the first attribute value token, (right) (normalized) entropy of the probability distribution defined by attention scores. The attention patterns analyzed here were obtained on the pre-training distribution; performing the same analysis on the fine-tuning distribution (not reported here) barely changes observed behaviors. See Section D.2 for the rationale behind the choice of metrics. 
 
 
 We complement our analysis with an experiment in which we fine-tune the model on rare, but seen during pre-training, individuals. We do so using our celebrities distribution, setting the total number of individuals to 128 128 k, n_celebrities to 8 8 k and weight_celebrities to 8. After training on 16 16 k training steps, the model confidently and correctly predicts the attribute value of the celebrities but gets around 50 50 % accuracy on non-celebrities, which are the majority of the population. Overall, we find that fine-tuning on existing individuals does not lead to fast performance drop fine-tuning on new individuals has (Figure P ). We are able to add a significant amount of knowledge in the model’s weights, as the accuracy on the 120 120 k non-celebrities goes from 50 50 % to close to 70 70 %. These results supporting that fine-tuning on existing individuals is net-positive are confirmed by our alternating training distribution experiment of Figure V . 
 
 
 Figure P: Evolution of the model’s performance when fine-tuned on rare (FT on non-celebrities line) or frequent (FT on celebrities line) individuals from the pre-training distribution. See Section F.3 for more detail. 
 
 
 



## SECTION: F.5 Experiments with regular changes in training distribution



 
 To complement our fine-tuning analysis, we consider the setup in which the training distribution is regularly changed, either to a new group of individual every change (this corresponds to varying number_groups and fixing number_repeats to 1 1 ) or alternating between two groups of individuals (this corresponds to varying number_repeats and fixing number_groups to 2 2 ). While this kind of experiment is further away from the current training paradigms of large language models and is more akin to a continual learning setup (e.g., Kirkpatrick et al. (2017) ), it enables us to monitor the plasticity of the network, that is how fast it learns new knowledge and forget about existing one, in a dynamic way. Overall, we find that our fine-tuning findings are robust across different stages of learning and these new results enable us to sometimes refine our conclusions. 
 
 
 Figure S: Evolution of the model performance on different groups of individuals when it is trained sequentially on these groups. The color indicates the group of people the model is evaluated on: the darker the color, the later the network was trained on this group. For all plots the total number of individuals considered is equal to 64 64 k. See Section F.5 for more detail. 
 
 
 Figure T: Same as Figure S , but with a constant learning rate scheduler. 
 
 
 Figure U: Similar to the middle panel of Figure S (8 groups), this time when training for longer. The total number of individuals is adapted so that the size of each group remains the same as before. All other hyperparameters remain the same. 
 
 
 Figure V: Evolution of the model performance on different groups of individuals when it is trained alternating between two groups. The color indicates the group of people the model is evaluated on: green is for the first group, blue for the second one. For all plots the total number of individuals considered is equal to 64 64 k. See Section F.5 for more detail. 
 
 
 We observe a few interesting patterns. First, it becomes increasingly easier to learn a new distribution over time (Figure S ), which is likely induced by the improvement of the attention pattern quality over the course of learning (Figure W ), until the cosine learning rate scheduler eventually damps down weight changes. At the same time, forgetting, measured in log loss differences, becomes more important and occurs much faster than learning, confirming the results of Figure 5 . However, changing distributions multiple times during early learning dynamics when the learning rate is relatively high reduce this plasticity increase, at it partially impairs future ability of the network to learn new groups (c.f. performance drop from Figure S middle to Figure U , or Figure T ). For small learning rates (i.e. at the end of training), performance on old data sometimes get improved after some initial performance drop, without it being replayed (Figure W ), an intriguing phenomenon what we have partially observed during fine-tuning (Figure N , top row). Additionally, for very small learning rates, learning eventually becomes harder and forgetting is not catastrophic, leading to the model remembering more about the second to last group than the last one (see e.g., the 8 groups plot in Figure S ). Still, too many distribution changes to unknown distributions when learning rates are small ultimately removes any knowledge from the network (e.g. Figure U ). 
 
 
 Figure W: Final attribute loss at the end of an attention patching experiment in which the model of Figure S (8 groups) serves as reference (green line), as a function of the number of steps the reference model was trained. For comparison, we include the one we obtained when training on all individuals at once (grey line), as in Figure D . We use this metric as a measure of how good the attention patterns of a given model (the reference model) at a given time are for learning and solving the task at hand. We do not observe an initial bump in performance when changing individual distribution. There are two main reasons for that: First, attention patterns get formed early on due to training occurring on less individuals. Second, the granularity that we use ( 2 2 k steps) would not allow us to see such a bump here. 
 
 
 Figure X: Evolution of the attention patterns for the experiment reported in the middle panel of Figure S (one loop over 8 8 different groups of individuals). In the first three panels, we report (left) the average attention to name tokens when seeing the last name token, (middle left) attention to general text tokens when predicting the first attribute value token, (middle right) attention to the last name token when predicting the first attribute value token. In the right panel, we select the last layer line from the attribute to name and attribute to text plots, and the first layer line from the name to name line. See Section D.2 for the rationale behind the choice of metrics. The attention patterns are more unstable than in the constant distribution scenario (Figure F ). Yet they remain relatively stable, particularly for the one highlighted in the right panel towards the end of learning, in light of the frequent distribution changes and the relatively high learning rate used for most of the training. 
 
 
 
 X 
 
 
 
 
 

