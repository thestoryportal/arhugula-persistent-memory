# ForwardReplay — arXiv 2605.00358

Source: https://arxiv.org/html/2605.00358

## Headings
# From Backward Spreading to Forward Replay:
Revisiting Target Construction in LLM Parameter Editing
## 1 Introduction
## 2 Related Works
### 2.1 LLM parameter editing
### 2.2 Other methods for knowledge editing
## 3 Preliminaries of LLM Parameter Editing
## 4 How does spreading work
### 4.1 Theoretical grounding
## 5 Our method
## 6 Experiments
### 6.1 Setup
### 6.2 Results
## 7 Conclusion and Limitations
## Impact Statement
## Acknowledgments
## References
## Appendix A More Details
### A.1 How to get the target hidden state m m
### A.2 An example about backward spreading
### A.3 The details about how to implement our method
### A.4 Theoretical explanation of our method
### A.5 The details of the experiments in Table 2
### A.6 The Proof of Theorem 1
### A.7 The Proof of Theorem 2
### A.8 Results on GPT2-XL and GPT-J
### A.9 Author contributions
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 0, "held-out": 0, "held out": 0, "generaliz": 15, "multi-token": 0, "multi token": 0, "unseen": 0, "novel entit": 0, "counterfact": 2, "zsre": 5, "teacher forc": 0, "autoregressive": 0, "first token": 0, "subject": 2, "last token": 0, "embedding": 2, "vocabulary": 0}


## SECTION: 6 Experiments



 



## SECTION: 6.1 Setup



 
 Baselines . We call our method FE ( f orward propagation e dit), which is built upon the standard MEMIT ( Meng et al., 2023 ) framework by replacing backward spreading with forward propagation.
We first construct several baselines in a controlled manner to closely examine the effectiveness of our method. (1) Standard MEMIT ( Meng et al., 2023 ) . This baseline follows the original MEMIT procedure, using backward spreading to construct targets for earlier decisive layers from the target computed at the final decisive layer.
(2) OneLayer. Only the final decisive layer is edited.
(3) BLUE ( Li et al., 2025a ) . Gradient-based optimization is independently performed twice to obtain targets for the first and the final decisive layers, and only these two layers are edited. Note that BLUE requires independently computing targets for two layers, thereby doubling the computational cost.
Since our method modifies only the target propagation mechanism without interfering with other components of the editing pipeline, it is expected to benefit a wide range of editing methods. Accordingly, we further extend our approach to several recently proposed methods to evaluate its scalability and general applicability. These methods include RECT ( Gu et al., 2024 ) , Alphaedit ( Fang et al., 2025 ) and PRUNE ( Ma et al., 2025 ) . We also include two methods that do not belong to the LTE paradigm: WISE  ( Wang et al., 2024a ) and RLEdit  ( Li et al., 2025b ) . WISE introduces additional memory modules that are trained to store and retrieve new knowledge, whereas RLEdit updates knowledge by training a hypernetwork to generate parameter modifications. 
 
 
 Models, datasets, and metrics . Following the prevailing experimental settings in the model editing literature, we evaluate our method on three LLMs: LLaMA3-8B-Instruct, GPT-J, and GPT-2 XL. Among them, LLaMA3-8B-Instruct more closely reflects the characteristics of contemporary mainstream LLMs, and is therefore used as our primary evaluation model. Experiments on GPT-J and GPT-2 XL are reported in Appendix A.8 (the findings are generally consistent with those observed on LLaMA3-8B-Instruct).
We follow the recent work Alphaedit in using two benchmark datasets: Multi-CounterFact (MCF)  ( Meng et al., 2022 ) and ZsRE  ( Levy et al., 2017 ) , editing 2,000 knowledge items for each dataset.
Consistent with standard MEMIT practice, we perform massive editing, in which all knowledge items are edited jointly in a single batch. All hyperparameters, including the selection of decisive layers, are adopted from EasyEdit ( Wang et al., 2024b ) , a well-known public repository widely used in model editing community. Following common practice, we report metrics along three dimensions: efficacy, generalization, and specificity. These metrics jointly provide a comprehensive evaluation of editing quality. Efficacy assesses whether the intended knowledge has been correctly injected, while generalization evaluates the robustness of the edit under natural linguistic variations, reflecting whether the model has internalized the knowledge rather than memorized a specific query. Specificity measures the extent to which the edit preserves unrelated model behavior, which is critical for practical deployment. Together, these metrics capture the essential trade-offs in knowledge editing between correctness, robustness, and minimal unintended side effects. Both efficacy and generalization are assessed using two metrics: Success ( Meng et al., 2023 ) and Accuracy ( Yang et al., 2025 ) . Success follows the traditional teacher-forcing–based evaluation widely used in the literature, whereas Accuracy measures exact token match under free-form generation.
For specificity, prior work by Liu et al. (2026) has shown that conventional ground-truth–based specificity metrics fail to accurately capture behavioral changes induced by editing. Accordingly, we follow Liu et al. (2026) and adopt more accurate ground-truth–free behavior deviation metrics. Specifically, D K ​ L D_{KL} measures the KL-divergence between output representations before and after editing, while Top- k k quantifies the overlap ratio of the top- k k supported outputs ( Liu et al., 2026 ) . 
 
 
 Table 5 : The ratio of remaining final residual after editing each decisive layer. The model is Llama3-8B-Instruct. 
 
 
 
 Layers 
 Layer4 
 Layer5 
 Layer6 
 Layer7 
 Layer8 
 
 FE 
 0.37 
 0.15 
 0. 08 
 0.05 
 0.03 
 
 
 
 
 



## SECTION: 6.2 Results



 
 Comparison with baseline methods .
The results of the controlled baselines are reported in Table  3 . Compared to the standard MEMIT, OneLayer performs poorly, indicating that directly steering the model to the target by editing a single layer is challenging. When comparing BLUE with OneLayer, although the improvement in efficacy is intuitive, an interesting observation is that BLUE sometimes achieves better specificity despite editing more layers. This phenomenon may be attributed to the fact that concentrating the primary editing effort on shallower layers can be beneficial for specificity.
Finally, we observe that our method significantly outperforms the standard MEMIT baseline, as well as the improved BLUE variant and all other baselines. Notably, BLUE incurs substantially higher computational cost than other methods, whereas our FE approach has nearly the same computational cost as standard MEMIT. This is because the additional forward propagation involves only four layers, rendering the overhead effectively negligible. 
 
 
 Scalability . To demonstrate the generality and scalability of FE, we further extend our method to several representative methods. The results are in Table  4 . We find that these methods also benefit to some extent from simply replacing backward spreading with our proposed forward replay. 
 
 
 Convergent property . In backward spreading, the final decisive layer is treated as the anchor point, and additional editable layers are progressively included toward earlier layers. The experiments reported in Table 2 show that the marginal gains diminish rapidly as the propagation spans farther layers, indicating that increasing the number of backward-spread layers does not guarantee convergence of the discrepancy between the target at the final decisive layer and the actual hidden state.
We conduct the same set of experiments in Table 2 for our method to examine the convergence behavior of this discrepancy as the number of editing layers increases. 
 
 
 The results are in Table 5 . Our method starts from the first decisive layer and obtains the targets for subsequent layers through forward propagation. As shown in the results, the discrepancy decreases approximately exponentially as more subsequent layers are included (roughly halving at each layer), demonstrating good convergence behavior. Consequently, the final error is substantially lower than that of the two backward-spreading–based methods reported in Table 2 , with the discrepancy at Layer8 being less than one-tenth of theirs.
Moreover, this favorable convergence property enables flexible adjustment of the number of edited layers to meet different error tolerance requirements. In addition, as discussed earlier in the comparison between BLUE and OneLayer, concentrating the primary editing effort on shallower layers may better preserve specificity. This constitutes another advantage of our approach. 
 
 
 
 



## SECTION: A.5 The details of the experiments in Table 2



 
 Here are the details of the experiments in Table 2 . “Dividing”: the targets for each layer are got in the way of Appendix A.2 . “No-Dividing”: the steering vector is constructed directly from the remaining residual without normalization by the number of remaining editable layers. For example, we revise Eq. 15 to be 
 

 
 
 m 1 = W 1 ​ k 1 + ( m 5 − W 5 ​ k 5 ) . m_{1}=W_{1}k_{1}+(m_{5}-W_{5}k_{5}). 
 
 (25) 
 
 Similarly, we revise Eq. 18 to be 
 

 
 
 m 2 = W 2 ​ k 2 1 + ( m 5 − W 5 ​ k 5 1 ) . m_{2}=W_{2}k_{2}^{1}+(m_{5}-W_{5}k_{5}^{1}). 
 
 (26) 
 
 
 
 The values in the table mean the ratio between the norm of the residual remaining after editing a given layer and the norm of the original total residual (the residual is taken from the final decisive layer). For example, the original total residual is m 5 − W 5 ​ k 5 m_{5}-W_{5}k_{5} . After editing the first layer (i.e., Layer4 in Table 2 ), the hidden state of the final layer becomes k 5 1 k_{5}^{1} , and the remaining residual becomes m 5 − W 5 ​ k 5 1 m_{5}-W_{5}k_{5}^{1} . Then the value corresponding to Layer4 is ‖ m 5 − W 5 ​ k 5 1 ‖ 2 ‖ m 5 − W 5 ​ k 5 ‖ 2 \frac{||m_{5}-W_{5}k_{5}^{1}||_{2}}{||m_{5}-W_{5}k_{5}||_{2}} . 
 
 
 



## SECTION: A.8 Results on GPT2-XL and GPT-J



 
 The results with the GPT2-XL model and GPT-J model are in Table 6 ∼ \sim 7 . We do not report results for RLEdit on these two models, as its performance is highly sensitive to hyperparameter choices. Despite extensive tuning efforts, we were unable to identify stable and appropriate hyperparameters. To avoid potential confusion arising from suboptimal configurations and unfair performance comparisons, we therefore omit RLEdit results for these models. 
 
 
 Table 6 : The effectiveness of our FE. The model is GPT2-XL.
 
 
 
 
 The MCF dataset 
 
 
 Efficacy 
 Generalization 
 Specificity 
 
 Success ↑ \uparrow 
 Accuracy ↑ \uparrow 
 Success ↑ \uparrow 
 Accuracy ↑ \uparrow 
 D K ​ L D_{KL} ↓ \downarrow 
 Top-1 ↑ \uparrow 
 Top-5 ↑ \uparrow 
 Top-10 ↑ \uparrow 
 
 OneLayer 
 74.4 
 43.3 
 58.7 
 19.6 
 0.55 
 68.8 
 65.7 
 64.4 
 
 MEMIT 
 94.0 
 79.7 
 82.1 
 45.3 
 0.81 
 63.5 
 60.8 
 59.4 
 
 BLUE 
 94.3 
 82.6 
 82.7 
 47.2 
 0.75 
 67.7 
 62.4 
 60.1 
 
 WISE 
 24.6 
 0.4 
 26.6 
 0.8 
 0.21 
 80.5 
 74.9 
 74.0 
 
 PRUNE 
 93.8 
 79.6 
 82.2 
 45.3 
 0.80 
 63.5 
 60.9 
 59.5 
 
 RECT 
 93.4 
 78.9 
 81.5 
 44.6 
 0.80 
 63.7 
 61.1 
 59.7 
 
 Alphaedit 
 99.4 
 97.2 
 92.1 
 58.7 
 0.98 
 62.9 
 57.8 
 55.9 
 
 FE (ours) 
 99.6 
 98.4 
 93.6 
 60.2 
 0.71 
 66.9 
 63.2 
 61.7 
 
 
 
 The ZsRE dataset 
 
 
 Efficacy 
 Generalization 
 Specificity 
 
 Success ↑ \uparrow 
 Accuracy ↑ \uparrow 
 Success ↑ \uparrow 
 Accuracy ↑ \uparrow 
 D K ​ L D_{KL} ↓ \downarrow 
 Top-1 ↑ \uparrow 
 Top-5 ↑ \uparrow 
 Top-10 ↑ \uparrow 
 
 OneLayer 
 66.5 
 45.8 
 60.7 
 39.6 
 0.94 
 69.0 
 44.4 
 47.0 
 
 MEMIT 
 81.4 
 65.8 
 74.4 
 56.7 
 0.90 
 70.6 
 47.1 
 49.5 
 
 BLUE 
 82.5 
 67.8 
 76.8 
 60.1 
 0.81 
 77.4 
 46.4 
 48.5 
 
 WISE 
 9.1 
 0 
 9.2 
 0 
 2.48 
 8.0 
 4.8 
 10.5 
 
 PRUNE 
 81.4 
 65.7 
 74.3 
 56.5 
 0.90 
 70.5 
 47.2 
 49.6 
 
 RECT 
 80.7 
 64.6 
 73.5 
 55.4 
 0.89 
 70.7 
 47.5 
 49.8 
 
 Alphaedit 
 92.0 
 81.8 
 83.2 
 67.4 
 0.93 
 73.0 
 45.0 
 48.9 
 
 FE (ours) 
 93.7 
 84.6 
 85.1 
 69.8 
 0.47 
 91.5 
 58.2 
 60.0 
 
 
 
 
 Table 7 : Effectiveness of our FE. The model is GPT-J-6B. 
 
 
 
 The MCF dataset 
 
 
 Efficacy 
 Generalization 
 Specificity 
 
 Success ↑ \uparrow 
 Accuracy ↑ \uparrow 
 Success ↑ \uparrow 
 Accuracy ↑ \uparrow 
 D K ​ L D_{KL} ↓ \downarrow 
 Top-1 ↑ \uparrow 
 Top-5 ↑ \uparrow 
 Top-10 ↑ \uparrow 
 
 OneLayer 
 96.6 
 85.4 
 79.1 
 41.0 
 0.42 
 73.4 
 69.1 
 68.7 
 
 MEMIT 
 99.8 
 99.2 
 91.8 
 61.9 
 0.44 
 75.0 
 71.2 
 70.8 
 
 BLUE 
 99.8 
 99.1 
 94.9 
 69.2 
 0.38 
 78.0 
 72.9 
 72.4 
 
 WISE 
 27.3 
 6.8 
 50.9 
 15.2 
 4.47 
 45.8 
 48.0 
 49.5 
 
 PRUNE 
 99.8 
 99.3 
 91.8 
 61.8 
 0.43 
 75.1 
 71.2 
 70.9 
 
 RECT 
 99.8 
 99.2 
 91.5 
 61.2 
 0.43 
 75.1 
 71.3 
 71.0 
 
 Alphaedit 
 99.8 
 98.6 
 93.2 
 61.5 
 0.58 
 72.5 
 66.0 
 65.1 
 
 FE (ours) 
 99.9 
 99.4 
 95.4 
 65.7 
 0.42 
 78.4 
 73.6 
 72.8 
 
 
 
 The ZsRE dataset 
 
 
 Efficacy 
 Generalization 
 Specificity 
 
 Success ↑ \uparrow 
 Accuracy ↑ \uparrow 
 Success ↑ \uparrow 
 Accuracy ↑ \uparrow 
 D K ​ L D_{KL} ↓ \downarrow 
 Top-1 ↑ \uparrow 
 Top-5 ↑ \uparrow 
 Top-10 ↑ \uparrow 
 
 OneLayer 
 93.8 
 86.8 
 86.9 
 75.6 
 0.48 
 96.5 
 52.9 
 57.8 
 
 MEMIT 
 99.3 
 98.1 
 95.3 
 90.1 
 0.23 
 99.3 
 63.6 
 68.9 
 
 BLUE 
 99.3 
 98.2 
 96.4 
 92.6 
 0.16 
 100.0 
 68.6 
 74.2 
 
 WISE 
 51.8 
 21.7 
 49.0 
 19.0 
 10.87 
 2.2 
 2.5 
 2.6 
 
 PRUNE 
 99.4 
 98.2 
 95.1 
 90.0 
 0.24 
 99.2 
 63.7 
 68.9 
 
 RECT 
 99.2 
 97.9 
 95.1 
 89.8 
 0.24 
 99.1 
 63.9 
 68.9 
 
 Alphaedit 
 88.2 
 75.0 
 76.2 
 57.6 
 0.49 
 97.9 
 54.6 
 59.4 
 
 FE (ours) 
 99.5 
 98.8 
 96.1 
 92.2 
 0.08 
 100.0 
 74.0 
 78.6 
 
 
 
 
 

