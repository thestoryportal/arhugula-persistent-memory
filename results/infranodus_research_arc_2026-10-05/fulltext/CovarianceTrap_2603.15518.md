# CovarianceTrap — arXiv 2603.15518

Source: https://arxiv.org/html/2603.15518

## Headings
# Beyond the Covariance Trap: Unlocking Generalization in Same-Subject Knowledge Editing for Large Language Models
## 1 Introduction
## 2 Related Works
#### The Locate-then-Edit Paradigm and The Covariance Constraint.
#### The Challenge of Same-Subject Multi-Relation Editing.
## 3 Analysis of Generalization Collapse
### 3.1 Preliminaries
#### Locate-then-Edit Paradigm.
#### Same-Subject Conflicts.
### 3.2 Geometric Formulations: The D > R D>R Pathology
#### Definition 1 (Tolerance Radius R R ).
#### Definition 2 (Activation Deviation D D ).
#### Hypothesis.
### 3.3 Value Perspective: Collapse of Tolerance Radius ( R ↓ R\downarrow )
#### Empirical Observation: Radius Collapse.
#### Mechanism: Gradient Orthogonality.
### 3.4 Key Perspective: The Covariance Trap ( D ↑ D\uparrow )
#### The Breach: D > R D>R .
#### Mechanism: The Covariance Trap.
#### Redundancy of Covariance.
## 4 Mitigation Strategy: RoSE
### 4.1 Isotropic Geometric Alignment
### 4.2 Hierarchical Knowledge Integration
## 5 Experiments
### 5.1 Experimental Setup
### 5.2 Main Results
### 5.3 Ablation Study
## 6 Conclusion
## Limitations
## References
## Appendix A Analysis of Error Amplification via the Covariance Matrix
#### Approximation via Orthogonality in Whitened Space.
#### Spectral Analysis and The Covariance Trap.
#### Comparative Error Bounds.
## Appendix B Locality Preservation in Covariance-Based Methods
#### Optimization Objective.
#### Mechanism of Constraint.
#### Interpretation of K ⊤ ​ C − 1 ​ k o ​ l ​ d ≈ 𝟎 K^{\top}C^{-1}k_{old}\approx\mathbf{0} .
## Appendix C Geometric Investigation Details
### C.1 Geometric Measurement
#### Tolerance Radius ( R R ) Measurement.
#### Activation Deviation ( D D ) Measurement.
#### Gradient Conflict Score.
### C.2 Additional Empirical Evidence on Llama
#### Collapse of Tolerance Radius ( R ↓ R\downarrow ).
#### Gradient Orthogonality as the Root Cause.
#### The Covariance Trap ( D ↑ D\uparrow ).
#### Stability of Subject Representation.
#### Geometric Restoration via RoSE.
### C.3 The Success on Isolated Fact Editing
### C.4 Layer Sensitivity Analysis
#### Universality of Geometric Pathology.
#### Orthogonality of Keys.
### C.5 Extended Analysis of Key Orthogonality
#### Robustness Across Model Scales.
#### Analysis of Semantically Similar Subjects.
## Appendix D Experimental Setup Details
### D.1 Dataset Construction & Statistics
### D.2 Evaluation Metrics Implementation
### D.3 Hyperparameters & Implementation
## Appendix E Original S2RKE Results
## Appendix F Discussion on Other Variants of the Covariance Matrix
## Appendix G Computational Overhead Analysis
## Appendix H HKI Sensitivity Analysis
## Appendix I Scalability to Larger Models: 14B Evaluation
## Appendix J Pseudocode of RoSE
## Appendix K Stability Under Sequential Edits
## Appendix L Case Studies
## Appendix M Ethical Statement
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 17, "held-out": 2, "held out": 0, "generaliz": 34, "multi-token": 0, "unseen": 1, "novel entit": 0, "new entit": 0, "counterfact": 1, "zsre": 0, "teacher forc": 0, "autoregressive": 0, "subject": 105, "last token": 0, "embedding": 0, "vocabulary": 1, "propagat": 0}


## SECTION: Beyond the Covariance Trap: Unlocking Generalization in Same-Subject Knowledge Editing for Large Language Models


 
 
 Xiyu Liu
 
 Affiliation:  Institute of Information Engineering, Chinese Academy of Sciences, Beijing, China
 
 Affiliation:  School of Cyber Security, University of Chinese Academy of Sciences, Beijing, China
 
    
 Qingyi Si
 
 Affiliation:  JD.com, Beijing, China{liuxiyu, liuzhengxiao, gunaibin, linzheng}@iie.ac.cn, siqingyi.phoebus@jd.com
 
    
 Zhengxiao Liu
 † † thanks: Zhengxiao Liu is the corresponding author. 
 Affiliation:  Institute of Information Engineering, Chinese Academy of Sciences, Beijing, China
 
 Affiliation:  School of Cyber Security, University of Chinese Academy of Sciences, Beijing, China
 
    
 Chenxu Yang
 
 Affiliation:  Institute of Information Engineering, Chinese Academy of Sciences, Beijing, China
 
 Affiliation:  School of Cyber Security, University of Chinese Academy of Sciences, Beijing, China
 
    
 Naibin Gu
 
 Affiliation:  Institute of Information Engineering, Chinese Academy of Sciences, Beijing, China
 
 Affiliation:  School of Cyber Security, University of Chinese Academy of Sciences, Beijing, China
 
    
 Zheng Lin
 
 Affiliation:  Institute of Information Engineering, Chinese Academy of Sciences, Beijing, China
 
 Affiliation:  School of Cyber Security, University of Chinese Academy of Sciences, Beijing, China
 

 Abstract 
 
 While locate-then-edit knowledge editing efficiently updates knowledge encoded within Large Language Models (LLMs), a critical generalization failure mode emerges in the practical same-subject knowledge editing scenario: models fail to recall the updated knowledge when following user instructions, despite successfully recalling it in the original edited form.
This paper identifies the geometric root of this generalization collapse as a fundamental conflict where the inner activation drifts induced by prompt variations exceed the model’s geometric tolerance for generalization after editing. We attribute this instability to a dual pathology: (1) The joint optimization with orthogonal gradients collapses solutions into sharp minima with narrow stability, and (2) the standard covariance constraint paradoxically acts as a Covariance Trap that amplifies input perturbations. To resolve this, we introduce RoSE (Robust Same-subject Editing), which employs Isotropic Geometric Alignment to minimize representational deviation and Hierarchical Knowledge Integration to smooth the optimization landscape. Extensive experiments demonstrate that RoSE significantly improves instruction-following capabilities, laying the foundation for robust interactive parametric memory of LLM agents. 
 
 
 
 
 
 



## SECTION: 3 Analysis of Generalization Collapse



 
 While the recent work successfully prevents catastrophic conflicts when editing same-subject facts, the failure to generalize to instruction-following scenarios points to a deep mechanistic flaw. In this section, we investigate this phenomenon through a geometric lens. We propose that this generalization collapse is not merely a stochastic error but a deterministic consequence of a geometric pathology: the Activation Deviation ( D D ) induced by prompt variations exceeds the model’s Tolerance Radius ( R R ) , formally denoted as the boundary violation D > R D>R . We rigorously unveil this pathology from the dual perspectives of value optimization and key projection, both supported by empirical evidence on 200 samples from S2RKE  Duan et al. (2025) using Qwen2.5-7B-Instruct  Qwen et al. (2025) . Empirical evidence from Llama-3.1-8B-Instruct  Grattafiori et al. (2024) shows the similar phenomenon, as detailed in Appendix  C.2 . 
 
 



## SECTION: 3.2 Geometric Formulations: The D > R D>R Pathology



 
 To mathematically formalize the generalization collapse, we define two critical metrics characterizing the geometry of the model’s activation space. 
 
 



## SECTION: 4.1 Isotropic Geometric Alignment



 
 Standard editing methods rely on the update rule Δ ​ W ∝ ( C + K ​ K ⊤ ) − 1 \Delta W\propto(C+KK^{\top})^{-1} . As proven in Sec.  3.4 , the inverse covariance matrix C − 1 C^{-1} acts as an anisotropic filter that amplifies minimal prompt variations into massive deviations. To eliminate this pathology, RoSE proposes Isotropic Geometric Alignment (IGA) , substituting C C with an identity matrix I I . The reformulated update rule is: 
 

 
 
 Δ ​ W IGA = ( V − W 0 l ​ K ) ​ K ⊤ ​ ( I + K ​ K ⊤ ) − 1 \Delta W_{\text{IGA}}=(V-W_{0}^{l}K)K^{\top}(I+KK^{\top})^{-1} 
 
 (10) 
 
 This modification serves two critical functions, one geometric and one mathematical: 
 
 
 Closing the Covariance Trap. Geometrically, replacing C C with I I enforces an isotropic response to input perturbations, ensuring that the projection of the key difference vector δ \delta is uniform across all directions. Consequently, the noise inherent in instructional prompts is no longer selectively amplified, minimizing D D . 
 
 
 Regularization for Invertibility. Mathematically, the term I I is strictly necessary for numerical stability. In practical editing scenarios, the Gram matrix K ​ K ⊤ KK^{\top} is typically rank-deficient and singular due to the similarity of k k vectors for the same-subject facts. Directly removing C C would hinder the inverse calculation. By adding I I , we effectively apply the Tikhonov Regularization to the update rule. This ensures that the matrix ( I + K ​ K ⊤ ) (I+KK^{\top}) is full-rank, guaranteeing a unique and stable solution for the update Δ ​ W R ​ o ​ S ​ E \Delta W_{RoSE} . 
 
 
 
 
 
 
 Model 
 Method 
 Efficacy ↑ \uparrow 
 Paraphrase ↑ \uparrow 
 Locality ↑ \uparrow 
 Overall ↑ \uparrow 
 
 
 
 Qwen2.5-7B-Instruct 
 Vanilla 
 26.0 ( ± \pm 0.0) 
 38.7 ( ± \pm 0.0) 
 64.3 ( ± \pm 0.0) 
 43.0 ( ± \pm 0.0) 
 
 MEMIT 
 50.5 ( ± \pm 0.3) 
 44.7 ( ± \pm 0.1) 
 63.6 ( ± \pm 0.1) 
 51.8 ( ± \pm 0.1) 
 
 AlphaEdit 
 63.8 ( ± \pm 0.1) 
 49.6 ( ± \pm 0.3) 
 63.5 ( ± \pm 0.1) 
 58.5 ( ± \pm 0.8) 
 
 MEMIT-Merge 
 75.5 ( ± \pm 0.5) 
 52.8 ( ± \pm 0.7) 
 63.8 ( ± \pm 0.1) 
 64.0 ( ± \pm 0.4) 
 
 RoSE (Ours) 
 86.7 ( ± \pm 0.2) 
 63.8 ( ± \pm 0.3) 
 63.3 ( ± \pm 0.0) 
 72.2 ( ± \pm 0.2) 
 
 Llama3.1-8B-Instruct 
 Vanilla 
 22.4 ( ± \pm 0.0) 
 41.2 ( ± \pm 0.0) 
 65.3 ( ± \pm 0.0) 
 43.0 ( ± \pm 0.0) 
 
 MEMIT 
 35.9( ± \pm 0.3) 
 44.4( ± \pm 0.2) 
 65.2( ± \pm 0.1) 
 48.5( ± \pm 0.1) 
 
 AlphaEdit 
 34.3( ± \pm 0.5) 
 44.1( ± \pm 0.3) 
 65.2( ± \pm 0.1) 
 47.9( ± \pm 0.2) 
 
 MEMIT-Merge 
 75.1( ± \pm 0.6) 
 58.5( ± \pm 0.1) 
 65.2( ± \pm 0.1) 
 66.3( ± \pm 0.2) 
 
 RoSE (Ours) 
 87.3 ( ± \pm 0.4) 
 66.9 ( ± \pm 0.2) 
 64.8( ± \pm 0.0) 
 73.0 ( ± \pm 0.2) 
 
 
 
 Table 1: Experimental instruction-following QA results on S2RKE across two models. Our method ( RoSE ) achieves the optimal performance across most key metrics. Standard deviations are shown in parentheses. 
 
 
 



## SECTION: 5 Experiments



 
 We conduct a series of experiments to validate the effectiveness of RoSE. Our evaluation is designed to answer three primary questions: ( Q1 ) Does RoSE improve instruction-following performance on the standard same-subject editing benchmark? ( Q2 ) How does RoSE perform in more practical challenging scenarios involving character-oriented conversational knowledge? ( Q3 ) Are both core components of RoSE, Isotropic Geometric Alignment and Hierarchical Knowledge Integration, essential to its performance? 
 
 



## SECTION: 5.1 Experimental Setup



 
 Datasets. 
To provide a comprehensive assessment, we use two distinct datasets. The first is S2RKE   Duan et al. (2025) , a standard benchmark for evaluating multi-relation edits on the same subject entity. To specifically test the central claims of this paper, we evaluate the edits on all original metrics using a held-out set of 2,000 generated instructional-style queries.
The second dataset, which we introduce as a more challenging practical test, is LoCoMo-Edit . Derived from the long-form conversational dataset LoCoMo  Maharana et al. (2024) , LoCoMo-Edit simulates real-world demands by featuring complex, long-term targets of the same character from conversations.
LoCoMo-Edit serves to evaluate an editor’s ability to internalize and generalize complex, contextual information, a critical step towards creating personalized AI with parametric conversational memory. Details can be referred to App.  D.1 . 
 
 
 Models. 
Our experiments are conducted on two widely used open-source large language models: Llama-3.1-8B-Instruct  Grattafiori et al. (2024) and Qwen2.5-7B-Instruct  Qwen et al. (2025) . 
 
 
 Baselines. 
We compare RoSE against a suite of strong locate-then-edit methods, including the foundational single-fact editor ROME   Meng et al. (2022a) , its batch-editing extension MEMIT   Meng et al. (2022b) , and another recent approach, AlphaEdit   ( Fang et al., 2024 ) . Our primary and most competitive baseline is MEMIT-Merge   Dong et al. (2025) , an adaptation of MEMIT designed for same-subject joint optimization. 
 
 
 Evaluation Metrics. 
We employ a tailored evaluation protocol for each dataset. On S2RKE, we report the standard metrics of Efficacy, Paraphrase, and Locality. For the conversational knowledge in LoCoMo-Edit, we adopt a nuanced question-answering (QA) evaluation, including three knowledge types: Single-Hop, Multi-Hop, and Temporal. F1 exact match score is reported for QA on LoCoMo-Edit. Detailed definitions and the full experimental protocol are provided in App.  D.2 . 
 
 
 
 
 
 
 Model 
 Method 
 Single Hop ↑ \uparrow 
 Multi Hop ↑ \uparrow 
 Temporal ↑ \uparrow 
 Overall ↑ \uparrow 
 
 
 
 Qwen2.5-7B-Instruct 
 Vanilla 
 12.9 ( ± \pm 0.1) 
 13.7 ( ± \pm 0.2) 
 5.1 ( ± \pm 0.5) 
 11.3 ( ± \pm 0.2) 
 
 MEMIT 
 15.1 ( ± \pm 0.6) 
 15.7 ( ± \pm 1.4) 
 8.7 ( ± \pm 1.2) 
 13.8 ( ± \pm 0.5) 
 
 AlphaEdit 
 7.5 ( ± \pm 1.4) 
 12.9( ± \pm 2.8) 
 8.5 ( ± \pm 2.1) 
 8.8( ± \pm 1.8) 
 
 MEMIT-Merge 
 17.2 ( ± \pm 0.4) 
 17.3 ( ± \pm 1.5) 
 11.2 ( ± \pm 0.8) 
 15.9 ( ± \pm 0.7) 
 
 
 RoSE (Ours) 
 22.3 ( ± \pm 0.3) 
 23.5 ( ± \pm 1.6) 
 19.1 ( ± \pm 0.9) 
 21.9 ( ± \pm 0.3) 
 
 Llama3.1-8B-Instruct 
 Vanilla 
 11.0( ± \pm 0.2) 
 12.8( ± \pm 0.1) 
 1.6( ± \pm 0.2) 
 9.4( ± \pm 0.1) 
 
 MEMIT 
 12.4( ± \pm 0.0) 
 14.0( ± \pm 0.3) 
 1.5( ± \pm 0.3) 
 10.4( ± \pm 0.0) 
 
 AlphaEdit 
 11.4( ± \pm 0.3) 
 12.7( ± \pm 0.7) 
 1.5( ± \pm 0.3) 
 9.5( ± \pm 0.3) 
 
 MEMIT-Merge 
 16.6( ± \pm 0.8) 
 19.2( ± \pm 0.4) 
 4.0( ± \pm 0.9) 
 14.4( ± \pm 0.6) 
 
 
 RoSE (Ours) 
 26.9 ( ± \pm 0.7) 
 28.7 ( ± \pm 0.2) 
 14.7 ( ± \pm 1.3) 
 24.5 ( ± \pm 0.5) 
 
 
 
 Table 2: Experimental instruction-following QA performance on LoCoMo-Edit across two models. Our method ( RoSE ) achieves the best performance across all crucial metrics. Standard deviations are shown in parentheses. 
 
 
 



## SECTION: 5.2 Main Results



 
 Our main results, presented in Tab.  1 and Tab.  2 , demonstrate RoSE’s consistent and significant superiority across both benchmarks and models. 
 
 
 ( Q1 ) On the standard S2RKE benchmark, RoSE achieves a decisive advantage in Efficacy and Paraphrase in instruction following. Compared to the strongest baseline MEMIT-Merge, RoSE achieves substantial gains of over 11 points in both Efficacy (86.7% vs. 75.5%) and Paraphrase (63.8% vs. 52.8%). Crucially, these significant gains come at almost no cost to model stability, as RoSE’s Locality score (63.3%) remains on par with all baselines. 
 
 
 ( Q2 ) The advantage of our approach is magnified on the more challenging LoCoMo-Edit stress test. Baseline methods show only marginal gains, with MEMIT-Merge achieving an overall F1 score of just 15.9%/14.4%. In contrast, RoSE is the only method to successfully recall complex conversational knowledge. It significantly outperforms all baselines across every metric, achieving a notably higher overall F1 score of 21.9%/24.5%. 
 
 
 
 
 
 (a) Qwen2.5-7B-Instruct. 
 
 
 (b) Llama-3.1-8B-Instruct. 
 
 Figure 6: Ablation study on the core components of RoSE on S2RKE. Both components are shown to be crucial for achieving maximum robustness. 
 
 
 Validating the Geometric Restoration ( D ≤ R D\leq R ). 
Fig.  7 visualizes the geometric restoration achieved by RoSE. IGA suppresses the input noise, reducing Activation Deviation D D (blue box), and HKI expands the solution space, raising the average Tolerance Radius R R (green zone). Crucially, the blue box falls almost entirely within the Green zone, confirming that RoSE successfully encapsulates instruction perturbations within the model’s valid editing boundaries ( D ≤ R D\leq R ). 
 
 
 In summary, these results offer compelling evidence that RoSE pioneers a path toward truly robust and practical knowledge editing. 
 
 
 



## SECTION: 5.3 Ablation Study



 
 ( Q3 ) Our ablation study, presented in Fig.  6 , validates the crucial role of both RoSE components. Removing the Isotropic Geometric Alignment (- w/o IGA) causes a clear degradation in both Efficacy and Paraphrase, confirming that removing the Covariance Trap is vital to unlock generalization. Likewise, removing Hierarchical Knowledge Integration (- w/o HKI) also leads to a significant drop in both metrics, demonstrating its necessity for overcoming overfitting caused by gradient orthogonality to ensure knowledge is deeply and generally learned. Notably, while both ablated variants outperform MEMIT-Merge, their synergistic combination (full RoSE) is essential for achieving optimal instruction-following capabilities. 
 
 
 
 
 
 (a) Qwen2.5-7B-Instruct. 
 
 
 (b) Llama-3.1-8B-Instruct. 
 
 Figure 7: Geometric validation of RoSE: IGA suppresses deviation (blue box), while HKI expands the tolerance basin (green zone). 
 
 
 
 



## SECTION: Appendix A Analysis of Error Amplification via the Covariance Matrix



 
 In this section, we provide a theoretical derivation to explain why the inclusion of the pre-statistics covariance matrix C C in the update rule leads to an amplification of the error term D D , compared to an isotropic update (where C C is replaced by the identity matrix I I ). 
 
 
 Recall the update rule for the weights: 
 

 
 
 Δ ​ W = W out l − W 0 l = ( V − W 0 l ​ K ) ​ K ⊤ ​ ( C + K ​ K ⊤ ) − 1 . \Delta W=W^{l}_{\text{out}}-W^{l}_{0}=(V-W^{l}_{0}K)K^{\top}(C+KK^{\top})^{-1}. 
 
 (12) 
 
 Let R = V − W 0 l ​ K R=V-W^{l}_{0}K denote the residual vector. We represent the difference in input keys as δ = k ~ − k o \delta=\tilde{k}-k_{o} . The error norm induced by this difference is defined as: 
 

 
 
 D = ‖ Δ ​ W ​ δ ‖ 2 = ‖ R ​ K ⊤ ​ ( C + K ​ K ⊤ ) − 1 ​ δ ‖ 2 . D=\|\Delta W\delta\|_{2}=\|RK^{\top}(C+KK^{\top})^{-1}\delta\|_{2}. 
 
 (13) 
 
 
 
 To understand the behavior of D D , we analyze the term M C ​ δ M_{C}\delta , where M C = ( C + K ​ K ⊤ ) − 1 M_{C}=(C+KK^{\top})^{-1} . Since K ​ K ⊤ KK^{\top} is a perturbation of extremely small rank relative to C, we can use the Sherman-Morrison-Woodbury formula to expand this inverse matrix as: 
 

 
 
 ( C + K ​ K ⊤ ) − 1 = C − 1 − C − 1 ​ K ​ ( I + K ⊤ ​ C − 1 ​ K ) − 1 ​ K ⊤ ​ C − 1 . (C+KK^{\top})^{-1}=C^{-1}-C^{-1}K(I+K^{\top}C^{-1}K)^{-1}K^{\top}C^{-1}. 
 
 (14) 
 
 Multiplying by the perturbation vector δ \delta , we obtain: 
 

 
 
 ( C + K ​ K ⊤ ) − 1 ​ δ = C − 1 ​ δ − C − 1 ​ K ​ ( I + K ⊤ ​ C − 1 ​ K ) − 1 ​ ( K ⊤ ​ C − 1 ​ δ ) ⏟ Correction Term . (C+KK^{\top})^{-1}\delta=C^{-1}\delta-C^{-1}K\underbrace{(I+K^{\top}C^{-1}K)^{-1}(K^{\top}C^{-1}\delta)}_{\text{Correction Term}}. 
 
 (15) 
 
 
 



## SECTION: Spectral Analysis and The Covariance Trap.



 
 The fundamental disparity between the standard edit (using C C ) and the isotropic modification (using I I ) stems from the spectral properties of the covariance matrix. As stated in the main text, C = 𝔼 ⁡ [ k ​ k ⊤ ] C=\mathbb{E}[kk^{\top}] acts as an anisotropic whitening filter. In the high-dimensional feature spaces of Transformers, the eigenspectrum of C C is known to be heavy-tailed and ill-conditioned. 
 
 
 Let σ i \sigma_{i} denote the eigenvalues of C C . Due to the redundancy in language representations, the trailing eigenvalues corresponding to low-variance directions approach zero ( σ min → 0 \sigma_{\min}\to 0 ). Consequently, the inverse matrix C − 1 C^{-1} possesses extremely large eigenvalues λ i ​ ( C − 1 ) = 1 / σ i \lambda_{i}(C^{-1})=1/\sigma_{i} in these directions. This spectral structure forms the theoretical basis of the Covariance Trap. 
 
 
 Since the perturbation δ \delta represents generalized noise or drift between knowledge forms, it is statistically isotropic relative to the principal axes of C C . Therefore, δ \delta inevitably contains a non-zero component, denoted as δ p ​ r ​ o ​ j \delta_{proj} , lying in the subspace spanned by the eigenvectors of C − 1 C^{-1} associated with its maximal eigenvalues ( λ max \lambda_{\max} ). The operation C − 1 ​ δ C^{-1}\delta drastically scales this component. 
 
 
 



## SECTION: Appendix B Locality Preservation in Covariance-Based Methods



 
 In this section, we analyze how standard locate-then-edit editing methods (e.g., MEMIT) utilize the covariance matrix C C to enforce locality constraints. The goal is to clarify the theoretical role of the term K ⊤ ​ C − 1 ​ k o ​ l ​ d ≈ 𝟎 K^{\top}C^{-1}k_{old}\approx\mathbf{0} , which we contrast with our simplified identity-based approach in the main text. 
 
 



## SECTION: Appendix C Geometric Investigation Details



 
 In this section, we provide the detailed experimental setup for the geometric analysis presented in Section 3 and furnish additional empirical evidence using the Llama-3.1-8B-Instruct model to demonstrate the universality of the observed phenomena. 
 
 



## SECTION: C.1 Geometric Measurement



 
 To rigorously quantify the generalization collapse phenomenon, we define and measure two critical geometric indicators: Tolerance Radius ( R R ) and Activation Deviation ( D D ). 
 
 



## SECTION: Geometric Restoration via RoSE.



 
 Finally, we validate the full RoSE framework’s ability to restore the safety condition D ≤ R D\leq R on Llama-3.1-8B-Instruct. Fig.  7(b) in the main text demonstrates that by combining Isotropic Geometric Alignment (to lower D D ) and Hierarchical Knowledge Integration (to increase R R ), RoSE successfully re-aligns the editing geometry on Llama-3.1. 
 
 
 
 



## SECTION: C.4 Layer Sensitivity Analysis



 
 In the main analysis, we follow the standard convention of previous studies (e.g., MEMIT, ROME) by observing the geometric metrics at the output of the final edited layer (i.e. Layer 8 for Qwen2.5-7B). This layer is typically chosen because it represents the cumulative effect of the batched updates distributed across the preceding MLP layers. 
 
 
 To demonstrate that our findings, specifically the geometric pathology D > R D>R and the orthogonality of subject keys, are intrinsic properties of the model’s activation space rather than artifacts of a specific layer selection, we conduct a sensitivity analysis across the a wider range of mid-early layers (Layers 7 through 11) over 100 samples. 
 
 



## SECTION: Universality of Geometric Pathology.



 
 We measure the Tolerance Radius ( R R ) and average Activation Deviation ( D D ) at the output of each layer. 
 
 
 We observe that the generalization pathology of D > R D>R in joint same-subject editing is consistent across mid-early layers (Fig.  12(a) ). In contrast, our Identity-based update (IGA) maintains D D within the safe zone ( D ≤ R D\leq R ) at every layer (Fig.  12(b) ). The Activation Deviation D D is smaller in earlier layers (e.g., Layer 7). This is attributed to a smaller prompt-derived δ \delta , as subject knowledge has not yet been fully enriched at these stages. 
 
 
 



## SECTION: C.5 Extended Analysis of Key Orthogonality



 
 To assess the universality and boundaries of our geometric findings, we extend our probing of key orthogonality ( k s 1 ⟂ k s 2 k_{s_{1}}\perp k_{s_{2}} ) to larger model scales and semantically proximate subjects. 
 
 



## SECTION: Analysis of Semantically Similar Subjects.



 
 We further investigate the challenging boundary case involving semantically highly correlated subjects, such as distinct versions of the same product line (e.g., “ iPhone 11 ” vs. “ iPhone 16 ”). In these extreme scenarios, where token overlap and semantic proximity are significant, we observe that the cosine similarity between keys can rise to around 0.5 (Fig.  15 ).
This high correlation challenges the strict orthogonality assumption and may lead to locality breaches. For instance, when editing the counterfactual “ iPhone 16 was released by Elon Musk ”, RoSE fails to preserve the distinct knowledge of “ iPhone 11 ”, incorrectly altering its attribute as well. 
 
 
 Crucially, however, this limitation is not introduced by our removal of the covariance matrix. We find that covariance-based baselines, such as MEMIT-Merge, exhibit the identical failure mode in these specific cases (Tab.  3 ). This indicates that the standard covariance constraint ( C C ) is also insufficient to disentangle such highly entangled representations in the feature space. Consequently, while these edge cases represent a general challenge for the locate-then-edit paradigm, removing C C in RoSE does not exacerbate the issue relative to the state-of-the-art, reinforcing that our method gains generalization and efficiency without sacrificing effective locality. 
 
 
 
 
 
 (a) iPhone 11 vs. iPhone 16 
 
 
 (b) H.W. Bush vs. W. Bush 
 
 Figure 15: Cases of k k similarity for semantically similar subjects on Qwen2.5-7B. 
 
 
 
 
 
 Boundary Case: High-Similarity Subjects 
 
 
 
 
 
 Edit Target: 
 
 
 
 
 Subject: iPhone 16 
 
 
 
 
 Fact: was released by → \rightarrow Elon Musk 
 
 
 
 
 Locality Check (Unintended Subject): 
 
 
 
 
 Query: Who released iPhone 11? 
 
 
 
 
 MEMIT-Merge: iPhone 11 was released by Elon Musk’s company, Tesla. (Fail) 
 
 
 
 
 RoSE (Ours): iPhone 11 was officially released by Tesla CEO Elon Musk. (Fail) 
 
 
 
 Table 3: Identical failure mode on similar subjects. 
 
 
 
 
 



## SECTION: Appendix D Experimental Setup Details



 



## SECTION: D.1 Dataset Construction & Statistics



 
 S2RKE & Instructed Query Generation. 
We utilize the S2RKE benchmark  Duan et al. (2025) , which focuses on editing same-subject multi-relation facts. To rigorously evaluate the instruction-following capability, the core contribution of this work, we construct a held-out test set of instructed queries distinct from the declarative forms used during editing. Specifically, we employ DeepSeek-R1-Distill-Qwen-14B  DeepSeek-AI et al. (2025) as the generator model. We prompt the model to rewrite original declarative facts into natural questions (e.g., rewriting " The CEO of Apple is Tim Cook " into " Who is the current executive running Apple Inc.? "). Then we transform the natural questions to instructed queries with instruction templates (e.g., " <|im_start|>system\n Your job is to answer the question. Do not explain.<|im_end|>\n <|im_start|>user\n Query:\n Based on your own knowledge, write a short answer for the following question in a few words. Please do not write complete and lengthy sentences.\n Question: \n<|im_end|>\n<|im_start|>assistant\n "). This procedure ensures that the queries mimic real-world user interactions while maintaining semantic consistency. 
 
 
 LoCoMo-Edit Dataset. 
To evaluate performance in a more practical, conversational setting, we construct the LoCoMo-Edit dataset derived from the LoCoMo benchmark  Maharana et al. (2024) . 
 
 
 We select 7 long-term conversations from the dataset, chosen for their rich character dynamics and temporal information.
From these conversations, we select 893 Question-Answer (QA) pairs categorized into three types: 503 Single-Hop (direct simple facts), 183 Multi-Hop (complex questions), and 207 Temporal (requires digital understanding).
For each QA pair, we extract the corresponding ground-truth knowledge in the declarative form using DeepSeek-R1-Distill-Qwen-14B to serve as the source for knowledge editing. This setup allows us to update the model’s internal belief state using the declarative fact and test its generalization via diverse conversational QA pairs. 
 
 
 



## SECTION: D.2 Evaluation Metrics Implementation



 
 S2RKE Metrics. 
Following standard protocols, we report Efficacy, Paraphrase, and Locality. Efficacy and Paraphrase measure the success rate of the model in generating the target object o ∗ o^{*} given the exact edit prompt and paraphrased prompts (but in the same linguistic form), respectively. Locality is evaluated on unrelated facts to ensure background knowledge preservation. 
 
 
 LoCoMo-Edit Metrics. 
For the LoCoMo-Edit benchmark, we also adopt the batch editing setting to simulate realistic same-subject editing scenarios. In each experimental run, we edit a batch of 5 to 10 declarative facts simultaneously. We then evaluate the model’s ability to answer the corresponding Single-Hop, Multi-Hop, and Temporal questions. The performance is quantified using the F1 Exact Match Score , which measures the token-level overlap between the model’s generated answer and the ground truth answer after normalization (removing punctuation and articles). 
 
 
 



## SECTION: Appendix E Original S2RKE Results



 
 In the main text, our evaluation primarily focuses on the newly identified failure mode regarding instruction-following queries. However, a robust same-subject knowledge editing method must also retain high performance on standard, declarative benchmarks. To verify this, we evaluate RoSE on the original test set of the S2RKE benchmark  Duan et al. (2025) on Qwen2.5-7B-Instruct, which consists of standard declarative prompts and paraphrases in the declarative form. 
 
 
 Figure 16: Performance on S2RKE with initial declarative prompts. RoSE enhances Paraphrase accuracy while preserving Locality, indicating better generalization capability. 
 
 
 As illustrated in Fig.  16 , RoSE demonstrates superior or comparable performance across all metrics against strong baselines. In terms of editing success, RoSE achieves an Efficacy score of 98.9, which is statistically tied with the state-of-the-art baseline MEMIT-Merge (99.2). This result empirically confirms that replacing the covariance matrix with the identity matrix via Isotropic Geometric Alignment (IGA) does not compromise the model’s ability to inject exact declarative facts. 
 
 
 More importantly, RoSE exhibits a distinct advantage in generalization. It outperforms MEMIT-Merge by a margin of 5.0 points in the Paraphrase metric (60.6 vs. 55.6). This improvement suggests that the geometric regularity enforced by IGA, combined with the smoothing effect of Hierarchical Knowledge Integration (HKI), enhances the model’s robustness not only to complex instructions but also to standard linguistic variations. Furthermore, despite the removal of the covariance constraint, which is traditionally considered essential for preventing catastrophic forgetting, RoSE maintains a Locality score of 71.9. This is on par with covariance-based methods like MEMIT (72.8) and MEMIT-Merge (72.0), supporting our theoretical finding that the intrinsic orthogonality of subject keys is sufficient to safeguard unrelated knowledge. In summary, RoSE improves the generalization capability without incurring any penalty on standard same-subject editing tasks. 
 
 
 Figure 17: Activation Deviation D D of MEMIT (the covariance matrix), AlphaEdit (the null-space projection derived from the covariance matrix) and RoSE (the identity matrix) on Qwen2.5. 
 
 
 



## SECTION: Appendix G Computational Overhead Analysis



 
 In the Limitations section, we acknowledge that the Hierarchical Knowledge Integration (HKI) component theoretically introduces additional computational steps due to the aggregation of gradients from multiple linguistic forms. To quantify the actual net impact of our dual-strategy framework on system resources, we conduct a comparative analysis of computational overhead. We measure the efficiency in a standard batch editing scenario consistent with the S2RKE benchmark statistics, specifically performing edits on Qwen2.5-7B-Instruct with a batch size of 4 on a single NVIDIA A100 GPU. We record both the average wall-clock time required to complete one batch update and the peak GPU memory allocated during the process. 
 
 
 
 
 
 (a) Wall-Clock Time (s). 
 
 
 (b) Peak GPU Memory (GB). 
 
 Figure 18: Computational Overhead Comparison. RoSE achieves the lowest latency and memory consumption, validating that the removal of covariance operations (IGA) outweighs the cost of HKI. 
 
 
 The comparative results, summarized in Fig.  18 , demonstrate that RoSE achieves the lowest computational footprint across both time and memory metrics among all compared methods, dispelling concerns regarding the overhead of the HKI component. In terms of time efficiency, RoSE requires only 13.1 seconds per edit batch, making it approximately 12.7% faster than the state-of-the-art MEMIT-Merge (15.0s) and significantly faster than AlphaEdit (41.6s). Regarding memory consumption, RoSE achieves the lowest peak usage at 22.1 GB, saving roughly 2.6 GB of VRAM compared to standard covariance-based methods like MEMIT and MEMIT-Merge, which consume 24.7 GB. 
 
 
 This superior efficiency can be attributed to a favorable architectural trade-off where the savings from Isotropic Geometric Alignment (IGA) significantly outweigh the costs of HKI. While HKI indeed requires processing multiple input prompts to compute the robust centroid, this added computational cost is marginal in the context of batch processing. In contrast, IGA removes a significant computational bottleneck inherent in baselines: the management of the covariance matrix ( C C ) . Standard methods and projection variants (like AlphaEdit) are obligated to load massive, high-dimensional covariance statistics into memory and perform expensive matrix operations, such as inversion or Singular Value Decomposition (SVD). By replacing these resource-intensive steps with a simple identity operation, RoSE effectively neutralizes the overhead of hierarchical integration, resulting in a system that is not only more robust but also more computationally efficient . 
 
 
 Figure 19: Sensitivity analysis of HKI linguistic templates number N N on Qwen2.5-7B-Instruct. 
 
 
 



## SECTION: Appendix H HKI Sensitivity Analysis



 
 We investigate the sensitivity of HKI to the number of linguistic templates used for centroid estimation. As illustrated in Fig.  19 , the Tolerance Radius ℛ \mathcal{R} exhibits remarkable stability, maintaining values consistently above 27 across template counts ranging from 2 to 10. Crucially, even minimal integration ( N = 2 N=2 ) yields a significant improvement over the baseline, indicating that the geometric gain stems primarily from the hierarchical aggregation structure rather than extensive sampling. 
 
 
 In terms of efficiency, the computational overhead of additional templates is marginal. Increasing the template count from 2 to 8 adds less than 1 second to the wall-clock time. Furthermore, even at our default setting ( N = 8 N=8 ), the total editing time ( ≈ 13.1 \approx 13.1 s) remains strictly lower than the MEMIT-Merge baseline (15.0s), confirming that RoSE enhances robustness without compromising efficiency. 
 
 
 



## SECTION: Appendix I Scalability to Larger Models: 14B Evaluation



 
 We conduct a comprehensive validation on the S2RKE benchmark using the larger Qwen2.5-14B-Instruct model. The new results, presented in Table 4 , confirm that RoSE maintains its effectiveness as model parameters scale up, significantly outperforming the strongest baseline (MEMIT-Merge) in both Efficacy (83.2% vs. 75.4%) and Paraphrase (62.1% vs. 51.6%) while preserving Locality (64.8%). 
 
 
 These experiments confirm that RoSE continues to significantly enhance instruction-following capabilities at the 14B scale. This finding reinforces the validity of the identity-based update, as evidenced by the highly stable Locality scores (64.8%) which remain on par with covariance-based baselines. More importantly, we have provided a key similarity analysis for different layers and for the 14B model in Appendix C.4 and Appendix C.5. The results demonstrate that Subject Keys for distinct subject entities maintain high orthogonality in larger scales and a wide range of mid-early layers, strengthening the generality of our claim. 
 
 
 
 
 
 Model 
 Efficacy ↑ \uparrow 
 Paraphrase ↑ \uparrow 
 Locality ↑ \uparrow 
 Overall ↑ \uparrow 
 
 
 
 Vanilla 
 26.5 ( ± \pm 0.0) 
 36.9 ( ± \pm 0.0) 
 65.0 ( ± \pm 0.0) 
 42.8 ( ± \pm 0.0) 
 
 MEMIT 
 48.5 ( ± \pm 0.3) 
 42.0 ( ± \pm 0.2) 
 65.0 ( ± \pm 0.0) 
 51.8 ( ± \pm 0.1) 
 
 AlphaEdit 
 59.5 ( ± \pm 0.4) 
 46.7 ( ± \pm 0.2) 
 65.0 ( ± \pm 0.1) 
 57.1 ( ± \pm 0.2) 
 
 MEMIT-Merge 
 75.4 ( ± \pm 0.2) 
 51.6 ( ± \pm 0.1) 
 64.9 ( ± \pm 0.1) 
 64.0 ( ± \pm 0.1) 
 
 RoSE (Ours) 
 83.2 ( ± \pm 0.3) 
 62.1 ( ± \pm 0.1) 
 64.8 ( ± \pm 0.0) 
 69.9 ( ± \pm 0.0) 
 
 
 Table 4: Experimental instruction-following QA results on S2RKE using the Qwen2.5-14B-Instruct model. RoSE successfully scales and maintains its optimal performance at a larger parameter size. Standard deviations are shown in parentheses. 
 
 
 

