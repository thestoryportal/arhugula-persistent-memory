# OutputVectorEditing — arXiv 2606.18767

Source: https://arxiv.org/html/2606.18767

## Headings
# Output Vector Editing for Memorization Mitigation in Large Language Models
## 1 Introduction
## 2 Related work
## 3 Method
### 3.1 Why edit output vectors, not activations?
### 3.2 Memorized sequence mining
### 3.3 Two-step localization
### 3.4 Output vector editing
### 3.5 Edit modes
## 4 Experimental setup
### 4.1 Model and data
### 4.2 Configurations
### 4.3 Our Three Baselines
### 4.4 Evaluation
## 5 Results
### 5.1 Main results
### 5.2 Success–locality trade-off
### 5.3 Cross-model generalization
## 6 Analysis
### 6.1 Mode complementarity
### 6.2 The limits of MLP-based editing
## 7 Conclusion
## Limitations and Ethics Statement
## Acknowledgments and Disclosure of Funding
## References
## Appendix A Mining statistics
## Appendix B Stopword skip filter
## Appendix C Neuron filter coverage
## Appendix D Catastrophic outlier analysis
## Appendix E Cumulative editing stress test
## Appendix F Qualitative examples
## Appendix G Full cross-model results
### G.1 Model details
### G.2 Cross-model mining
#### Subset sampling for Llama2.
#### SmolLM-360M mining.
### G.3 Per-configuration results at k = 5 k{=}5
#### Cross-model observations.
## Appendix H Activation steering at higher strengths
## Appendix I Attention-layer analysis
#### Conditional analysis of attention ablation.
## Appendix J Tipping point distribution
## Appendix K Activation steering baseline
## Appendix L Error analysis
## Appendix M Activation patching example
## NeurIPS Paper Checklist
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 1, "held-out": 0, "held out": 1, "generaliz": 3, "multi-token": 1, "unseen": 0, "novel entit": 0, "new entit": 0, "counterfact": 0, "zsre": 0, "teacher forc": 1, "autoregressive": 3, "subject": 13, "last token": 2, "embedding": 6, "vocabulary": 12, "propagat": 0}


## SECTION: 3 Method



 



## SECTION: 4 Experimental setup



 



## SECTION: 4.4 Evaluation



 
 Edit success. 
For each memorized sequence, we generate 20 tokens autoregressively (greedy decoding, temperature = 0) before and after the edit; unlike mining (§ 3.2 ), evaluation uses real autoregressive generation. Our primary metric is BLEU between pre-edit and post-edit generations; an edit succeeds if BLEU < 0.6 <0.6 . We additionally report ANLCS (Average Normalized Longest Common Subsequence) ( Suri et al., 2025 ) and normalized Levenshtein distance ( Chang et al., 2024 ) . 
 
 
 Locality measures whether an edit leaves the
model’s behavior on unrelated inputs intact, computed per
edit (weights restored between samples). Metrics: (i)
WikiText-103 perplexity (200 texts, max 512 tokens; baseline
15.52); (ii) Wikidata QA
 ( Srivastava and others, 2023 ) (200 samples; baseline 64.5%);
(iii) HellaSwag ( Zellers et al., 2019 ) (200 samples;
baseline 73.5%). We report median shifts in main text
(tail fractions in Appendix  D ) since means
are dominated by rare
outliers (§ 5.2 ). 
 
 
 
 



## SECTION: 5 Results



 
 § 5.1 –§ 5.2 present the
OLMo-7B evaluation for the
 k k ∈ \in { 5 , 10 } \{5,10\} grid, § 5.3 cross-model transfer at k = 5 k{=}5 . 
 
 
 Table 1: Main results on OLMo-7B (6,831 memorized sequences, β = 100 \beta{=}100 ). n n = sequences passing the localization filter; Succ% = fraction with BLEU(pre, post) < 0.6 <0.6 ; 95% CIs within ± \pm 1.0pp (omitted). ANLCS = avg. normalized longest common subsequence; Lev = normalized Levenshtein distance; PPL med = median WikiText-103 perplexity (baseline 15.52), Δ \Delta PPL = its median shift; HSwag/QA = HellaSwag/Wikidata QA accuracy (%). Random neurons’ small n n reflects 80.5% filter rejection. 
 
 
 
 
 
 
 Edit Success 
 Locality 
 
 Method 
 Config 
 n n 
 Succ% ↑ \uparrow 
 BLEU ↓ \downarrow 
 ANLCS ↓ \downarrow 
 Lev ↑ \uparrow 
 PPL med 
 Δ \Delta PPL 
 HSwag 
 QA 
 
 Baseline (no edit) 
 – 
 – 
 – 
 – 
 – 
 – 
 15.52 
 – 
 73.5 
 64.5 
 
 Output vector editing (ours) 
 
 EOS 
 k = 5 k{=}5 
 6,124 
 85.7 
 0.157 
 0.232 
 0.668 
 15.93 
 +0.41 
 71.6 
 61.4 
 
 k = 10 k{=}10 
 6,444 
 87.9 
 0.132 
 0.205 
 0.689 
 16.40 
 +0.88 
 70.8 
 59.6 
 
 Next-best 
 k = 5 k{=}5 
 6,124 
 81.5 
 0.238 
 0.363 
 0.588 
 15.65 
 +0.13 
 71.9 
 62.7 
 
 k = 10 k{=}10 
 6,444 
 83.5 
 0.218 
 0.342 
 0.605 
 15.59 
 +0.07 
 71.8 
 62.0 
 
 Suppress 
 k = 5 k{=}5 
 6,124 
 60.5 
 0.447 
 0.560 
 0.425 
 15.55 
 +0.03 
 72.1 
 63.0 
 
 k = 10 k{=}10 
 6,444 
 61.5 
 0.438 
 0.551 
 0.434 
 15.59 
 +0.07 
 71.4 
 61.3 
 
 Redact 
 k = 5 k{=}5 
 6,124 
 31.7 
 0.703 
 0.749 
 0.252 
 15.54 
 +0.02 
 73.4 
 64.2 
 
 k = 10 k{=}10 
 6,444 
 34.0 
 0.680 
 0.728 
 0.273 
 15.54 
 +0.02 
 73.4 
 64.3 
 
 Baselines 
 
 Zero ablation 
 k = 5 k{=}5 
 6,124 
 31.3 
 0.715 
 0.776 
 0.225 
 15.52 
 +0.00 
 73.4 
 64.3 
 
 Random neurons 
 k = 5 k{=}5 
 1,331 
 0.8 
 0.993 
 0.995 
 0.006 
 – 
 – 
 – 
 – 
 
 Act. steering 
 L25, α = 0.5 \alpha{=}0.5 
 6,831 
 73.3 
 0.359 
 0.492 
 0.486 
 16.42 
 +0.90 
 72.5 
 58.0 
 
 
 
 



## SECTION: 5.1 Main results



 
 Output vector editing outperforms mechanism
controls. 
As edit success rates and locality metrics
in
Table  1 show:
At matched k = 5 k{=}5 , EOS achieves 85.7% suppression versus 31.3% for zero ablation on the same located neurons, a 2.7 × 2.7\times gap (87.9% at k = 10 k{=}10 ). Redact ( k = 5 k{=}5 , 31.7%) is within noise of zero ablation, confirming the extra success in aggressive modes comes from the edited output-vector direction rather than localization alone. Random neurons achieve only 0.8% success with 80.5% skipped by the top-/bottom-50 filter; L1-guided selection reduces this to 10.3%, supporting the localization procedure. Suppress mode (60.5%, no distractor injected) shows roughly half the gap from zero ablation, reflecting weight-level intervention itself. 
 
 
 Next-best is the
best operating point. 
Activation steering at its best configuration (layer 25,
 α = .5 \alpha{=}.5 ) reaches 73.3% suppression over all 6,831
sequences. Next-best ( k = 5 k{=}5 ) reaches 81.5% on the 6,124
post-localization sequences (73.1% absolute) is comparable. The gap is on locality: median Δ \Delta PPL + .13 +.13 for Next-best vs. + .90 +.90 for steering ( 7 × 7\times better), HellaSwag within noise (71.9% vs. 72.5%), and per-sequence targeting that steering’s blanket subtraction cannot match. Examples in Appendix  F . 
 
 
 



## SECTION: 5.3 Cross-model generalization



 
 We extend the evaluation to three further models at β = 100 \beta{=}100 , k = 5 k{=}5 : SmolLM-360M and OLMo-1B span smaller scales, Llama2-7B is a different family at OLMo-7B’s scale. Mining yields 4,968 sequences for OLMo-1B and 18K+/130K+ for SmolLM-360M/Llama2-7B (latter two subsampled to 6,831 for comparability). Three patterns emerge (Table  2 ; full results in Appendix  G ): 
 
 
 Table 2: Cross-model results at k = 5 k{=}5 . Skip% = fraction rejected by the top-/bottom-50 filter; Δ \Delta PPL med {}_{\text{med}} = median EOS perplexity shift vs. each model’s baseline. Full results in Appendix  G . 
 
 
 
 Model 
 Params 
 Skip% 
 EOS 
 Next-best 
 Suppress 
 Redact 
 Δ \Delta PPL med {}_{\text{med}} 
 
 
 
 SmolLM-360M 
 360M 
 48.3% 
 34.9 
 37.7 
 30.6 
 15.3 
 + 0.04 +0.04 
 
 OLMo-1B 
 1.2B 
 43.4% 
 52.4 
 55.4 
 36.2 
 15.7 
 + 0.04 +0.04 
 
 Llama2-7B 
 6.7B 
 0 9.0% 
 69.6 
 68.3 
 49.0 
 40.7 
 + 0.15 +0.15 
 
 OLMo-7B 
 6.9B 
 10.3% 
 85.7 
 81.5 
 60.5 
 31.7 
 + 0.41 +0.41 
 
 
 
 
 Mode ordering is consistent. EOS and Next-best are strongest across all four models, with random neurons at <2% success ( ≥ \geq 80% skip rate). Small models favor Next-best, 7B models favor EOS (Llama2-7B marginally, OLMo-7B decisively). 
 
 
 Absolute success rates scale with size, not family. SmolLM-360M (34.9%) and OLMo-1B (52.4%) sit well below OLMo-7B (85.7%), driven by rising skip rates (48.3%, 43.4% vs. 10.3%); Llama2-7B at 69.6% clusters with OLMo-7B (skip 9.0%) regardless of family. 
 
 
 Locality costs are architecture-dependent. The catastrophic-outlier tail on OLMo-7B aggressive modes does not appear on OLMo-1B or Llama2-7B (median Δ \Delta PPL ≤ + 0.15 \leq+0.15 across modes at k = 5 k{=}5 ); on Llama2-7B, Next-best is near-Pareto-optimal ( + 0.01 +0.01 Δ \Delta PPL, 68.3% success). SmolLM-360M Suppress is the lone exception (systemic + 8.95 +8.95 per-edit cost). The catastrophic tail is OLMo-7B-specific; smaller-scale deployment benefits from per-model β / k \beta/k sweeps. 
 
 
 
 



## SECTION: 6 Analysis



 



## SECTION: Appendix D Catastrophic outlier analysis



 
 The worst per-edit locality impact observed was at sample 4264494 (EOS, k = 10 k{=}10 ): perplexity spiked from 15.52 to 1.5 × 10 10 1.5\times 10^{10} after a single edit. Context: “Michaels Hospital, LiKaShing Knowledge Institute, Toronto…” Restoring the original weights immediately recovered baseline perplexity, confirming this is a property of the specific edit, not cumulative degradation. 
 
 
 Per-config maximum Δ \Delta PPL across all configurations (Table  4 ): Redact +0.53 (safe in all k k ), Next-best +52.3 ( k = 5 k{=}5 ), Suppress + 2.0 × 10 9 2.0\times 10^{9} ( k = 10 k{=}10 ), EOS + 1.5 × 10 10 1.5\times 10^{10} ( k = 10 k{=}10 ). Catastrophic outliers ( Δ \Delta PPL > 100 >100 ) are absent in Redact at any k k and in Next-best at k = 5 k{=}5 , but appear at low frequency in Next-best k = 10 k{=}10 (0.9%) and at higher frequency in Suppress and EOS modes. 
 
 
 Table 4: Fraction of edits with locality degradation Δ \Delta PPL exceeding given thresholds. Redact is uniformly safe; aggressive modes show a heavy right tail. Computed over the per-edit locality samples ( n ≈ 80 n\approx 80 –230 per config, evaluated every 25 successful edits). 
 
 
 
 Config 
 > 1 >1 
 > 10 >10 
 > 100 >100 
 > 1000 >1000 
 
 
 
 Redact ( k = 5 k{=}5 ) 
 0.0% 
 0.0% 
 0.0% 
 0.0% 
 
 Redact ( k = 10 k{=}10 ) 
 0.0% 
 0.0% 
 0.0% 
 0.0% 
 
 Next-best ( k = 5 k{=}5 ) 
 23.1% 
 3.5% 
 0.0% 
 0.0% 
 
 Next-best ( k = 10 k{=}10 ) 
 20.3% 
 8.5% 
 0.9% 
 0.5% 
 
 Suppress ( k = 5 k{=}5 ) 
 14.9% 
 3.4% 
 1.4% 
 0.7% 
 
 Suppress ( k = 10 k{=}10 ) 
 25.3% 
 10.1% 
 1.9% 
 1.9% 
 
 EOS ( k = 5 k{=}5 ) 
 40.5% 
 7.6% 
 0.5% 
 0.5% 
 
 EOS ( k = 10 k{=}10 ) 
 47.8% 
 11.9% 
 1.8% 
 0.4% 
 
 
 
 
 



## SECTION: Appendix G Full cross-model results



 
 This appendix documents the cross-model experiments summarized in § 5.3 , including model architectures, mining procedure and yield for each model, and the full per-configuration results at k = 5 k{=}5 . 
 
 



## SECTION: G.3 Per-configuration results at k = 5 k{=}5



 
 Table  9 reports the complete per-model breakdown at k = 5 k{=}5 across the four edit modes plus the random-neuron, zero-ablation, and β = 200 \beta{=}200 baselines. The OLMo-7B section reproduces the k = 5 k{=}5 rows from Table  1 for direct comparison. 
 
 
 Table 9: Full cross-model results at k = 5 k{=}5 . All output vector editing configurations use β = 100 \beta{=}100 unless noted. “ β = 200 \beta{=}200 ” rows use Redact mode at elevated boosting. Baseline rows report each model’s unedited WikiText-103 perplexity, HellaSwag (200 samples), and Wikidata QA (200 samples). 
 
 
 
 Config 
 n n 
 Succ% ↑ \uparrow 
 BLEU ↓ \downarrow 
 ANLCS ↓ \downarrow 
 Lev ↑ \uparrow 
 PPL 
 Δ \Delta PPL 
 HS 
 QA 
 
 OLMo-7B (baseline PPL 15.52, HS 73.5, QA 64.5; n total = 6,831 n_{\text{total}}{=}6{,}831 , skip 10.3 % 10.3\% ) 
 
 Next-best 
 6,124 
 81.5 
 0.238 
 0.363 
 0.588 
 15.65 
 +0.13 
 71.9 
 62.7 
 
 EOS 
 6,124 
 85.7 
 0.157 
 0.232 
 0.668 
 15.93 
 +0.41 
 71.6 
 61.4 
 
 Suppress 
 6,124 
 60.5 
 0.447 
 0.560 
 0.425 
 15.55 
 +0.03 
 72.1 
 63.0 
 
 Redact 
 6,124 
 31.7 
 0.703 
 0.749 
 0.252 
 15.54 
 +0.02 
 73.4 
 64.2 
 
 Random 
 1,331 
 0.8 
 0.993 
 0.995 
 0.006 
 – 
 – 
 – 
 – 
 
 Zero 
 6,124 
 31.3 
 0.714 
 0.776 
 0.224 
 15.52 
 +0.00 
 73.4 
 64.2 
 
 Redact ( β = 200 \beta{=}200 ) 
 6,124 
 57.4 
 0.455 
 0.517 
 0.483 
 15.57 
 +0.05 
 73.2 
 63.9 
 
 Llama2-7B (baseline PPL 9.23, HS 71.0, QA 69.0; n total = 6,831 n_{\text{total}}{=}6{,}831 subsample, skip 9.0%) 
 
 Next-best 
 6,218 
 68.3 
 0.377 
 0.490 
 0.500 
 9.24 
 + 0.01 +0.01 
 70.5 
 65.5 
 
 EOS 
 6,218 
 69.6 
 0.323 
 0.388 
 0.569 
 9.38 
 + 0.15 +0.15 
 68.9 
 63.5 
 
 Suppress 
 6,218 
 49.0 
 0.553 
 0.641 
 0.363 
 9.23 
 + 0.00 +0.00 
 70.4 
 63.9 
 
 Redact 
 6,218 
 40.7 
 0.611 
 0.655 
 0.321 
 9.26 
 + 0.03 +0.03 
 70.4 
 66.2 
 
 Random 
 844 
 0 1.2 
 0.991 
 0.993 
 0.007 
 – 
 – 
 – 
 – 
 
 Zero 
 6,218 
 22.9 
 0.793 
 0.837 
 0.167 
 9.23 
 + 0.00 +0.00 
 71.0 
 67.4 
 
 Redact ( β = 200 \beta{=}200 ) 
 6,218 
 59.5 
 0.431 
 0.485 
 0.469 
 9.28 
 + 0.05 +0.05 
 69.8 
 65.5 
 
 OLMo-1B (baseline PPL 23.23, HS 56.0, QA 59.5; n total = 4,968 n_{\text{total}}{=}4{,}968 , skip 43.4 % 43.4\% ) 
 
 Next-best 
 2,813 
 55.4 
 0.494 
 0.596 
 0.395 
 23.23 
 +0.00 
 55.9 
 58.3 
 
 EOS 
 2,813 
 52.4 
 0.496 
 0.557 
 0.393 
 23.27 
 +0.04 
 55.5 
 55.0 
 
 Suppress 
 2,813 
 36.2 
 0.669 
 0.744 
 0.257 
 23.23 
 +0.00 
 56.0 
 59.5 
 
 Redact 
 2,813 
 15.7 
 0.855 
 0.886 
 0.118 
 23.23 
 +0.00 
 55.9 
 59.2 
 
 Random 
 449 
 1.1 
 0.990 
 0.995 
 0.009 
 – 
 – 
 – 
 – 
 
 Zero 
 2,813 
 29.4 
 0.737 
 0.799 
 0.207 
 23.23 
 +0.00 
 55.7 
 58.5 
 
 Redact ( β = 200 \beta{=}200 ) 
 2,813 
 32.7 
 0.690 
 0.731 
 0.273 
 23.24 
 +0.01 
 55.8 
 59.5 
 
 SmolLM-360M (baseline PPL 20.74, HS 47.5, QA 38.0; n total = 6,831 n_{\text{total}}{=}6{,}831 , skip 48.3%) 
 
 Next-best 
 3,534 
 37.7 
 0.661 
 0.734 
 0.281 
 20.78 
 + 0.04 +0.04 
 46.4 
 32.4 
 
 EOS 
 3,534 
 34.9 
 0.682 
 0.740 
 0.266 
 20.78 
 + 0.04 +0.04 
 44.6 
 32.9 
 
 Suppress 
 3,534 
 30.6 
 0.724 
 0.782 
 0.232 
 29.69 
 + 8.95 +8.95 
 47.3 
 28.8 
 
 Redact 
 3,534 
 15.3 
 0.865 
 0.898 
 0.117 
 20.85 
 + 0.11 +0.11 
 47.4 
 35.7 
 
 Random 
 646 
 0 2.3 
 0.983 
 0.987 
 0.014 
 – 
 – 
 – 
 – 
 
 Zero 
 3,534 
 26.4 
 0.766 
 0.826 
 0.193 
 20.74 
 − 0.00 -0.00 
 47.6 
 36.6 
 
 Redact ( β = 200 \beta{=}200 ) 
 3,534 
 28.4 
 0.740 
 0.789 
 0.226 
 20.92 
 + 0.18 +0.18 
 47.2 
 33.9 
 
 
 
 



## SECTION: Appendix I Attention-layer analysis



 
 To test whether MLP editing failures are caused by attention-driven memorization, we compare the attention attribution fraction (logit contribution from attention outputs divided by total logit magnitude) between editing failures and matched success controls across two configurations (Table  10 ). Failures are defined as samples for which the edit was attempted (i.e., at least one neuron passed the localization filter of § 3.3 ) but did not cross the BLEU < 0.6 <0.6 success threshold; samples skipped at localization are excluded from this analysis. 
 
 
 Table 10: Attention attribution fraction for editing failures vs. successes. Two-sided Mann-Whitney U test; effect size reported as rank-biserial correlation. Successes have higher median attention attribution than failures in both configurations, the opposite direction from what an “attention-driven failures” hypothesis would predict. Effects are small in magnitude. 
 
 
 
 Config 
 Group 
 Mean 
 Median 
 Std 
 p p / effect 
 
 
 
 EOS k = 10 k{=}10 
 Failures ( n = 777 n{=}777 ) 
 0.265 
 0.245 
 0.197 
 
 
 
 Successes ( n = 500 n{=}500 ) 
 0.282 
 0.259 
 0.193 
 
 
 
 
 
 
 
 p = 0.07 p=0.07 , r = 0.06 r=0.06 
 
 Next-best k = 5 k{=}5 
 Failures ( n = 1,135 n{=}1{,}135 ) 
 0.254 
 0.222 
 0.200 
 
 
 
 Successes ( n = 500 n{=}500 ) 
 0.288 
 0.265 
 0.196 
 
 
 
 
 
 
 
 p < 10 − 4 p<10^{-4} , r = 0.11 r=0.11 
 
 
 
 
 Copy head prevalence (11.5% vs. 7.8% for EOS; 9.1% vs. 5.6% for next-best) and induction head prevalence (19.2% vs. 22.4%; 19.2% vs. 15.2%) show no strong discriminative signal between failures and successes. 
 
 



## SECTION: Conditional analysis of attention ablation.



 
 Manual inspection of residual failure cases suggested that the memorized continuation often copies tokens already present in the prefix, indicating possible induction or copy-head behavior. To test this quantitatively, we split the MLP-failure cases by whether the memorized continuation shares any non-stopword token with the prefix. Stopword filtering uses the same NLTK stopword set, punctuation, and single-letter tokens as the localization pipeline (§ 3.3 ). Table  11 reports attention-head ablation recovery rates conditional on this split, for k ∈ { 1 , 3 , 5 } k\in\{1,3,5\} ablated heads at the target token position. 
 
 
 Table 11: Attention-head ablation recovery rates on MLP-failure cases, split by whether the memorized continuation shares any non-stopword token with the prefix (overlap vs no_overlap). Recovery is enriched on overlap cases by 7–8 percentage points at k = 5 k{=}5 , but attention ablation contributes substantially in both regimes. 
 
 
 
 Group 
 𝐧 \mathbf{n} 
 𝐤 = 𝟏 \mathbf{k{=}1} head 
 𝐤 = 𝟑 \mathbf{k{=}3} heads 
 𝐤 = 𝟓 \mathbf{k{=}5} heads 
 
 EOS k = 10 k{=}10 failures 
 
 Marginal 
 1,164 
 55.8% 
 61.8% 
 64.3% 
 
 Overlap 
 514 
 57.0% 
 66.1% 
 68.7% 
 
 No overlap 
 650 
 54.8% 
 58.3% 
 60.9% 
 
 Next-best k = 5 k{=}5 failures 
 
 Marginal 
 1,842 
 52.5% 
 56.6% 
 59.8% 
 
 Overlap 
 840 
 53.9% 
 59.5% 
 63.6% 
 
 No overlap 
 1,002 
 51.3% 
 54.2% 
 56.7% 
 
 
 
 
 The ∼ 45 % {\sim}45\% / ∼ 55 % {\sim}55\% overlap/no-overlap split is roughly balanced in both configurations. The 7–8 pp enrichment on the overlap subset directionally supports the induction/copy-head hypothesis, but the persistent > 55 % {>}55\% recovery on no-overlap failures means attention ablation is doing meaningful work outside the literal-copy regime as well. We therefore frame attention as a complementary fallback rather than a separate primary mechanism for copy-style memorization. 
 
 
 
 



## SECTION: Appendix L Error analysis



 
 To understand why edits fail, we sample 300 OLMo-7B failure cases across six
strata (50 per stratum: universal failures, four mode-specific groups, and
localization failures) and classify each into seven categories using Claude
Opus as the annotator. While the categories align with mechanistic expectations and per-stratum neuron-count statistics, LLM classifiers can preferentially assign borderline cases to whichever category is most clearly defined in the prompt; the annotation prompt is shown in Figure  3 .
Three takeaways: (i) 58.4% of failures (distributed redundant, factual recall,
low MLP signal) reflect encoding too diffuse for our top- k k budget and are the
natural target of a larger-budget or cross-layer extension
(§ 7 ); (ii) 26.7% (weak edit signal) are correctly located
but the multiplicative scaling does not push the new projection far enough,
suggesting per-sequence β \beta tuning; (iii) the remaining 15.0%
(high-frequency target, structural template, short context) are mode-specific
and largely addressed by the ensemble strategy of
§ 6.1 . The 14% boundary is therefore non-uniform:
roughly two thirds reflect a budget limit, the rest inherent dispersion or
mode-level mismatch. 
 
 
 Table  14 shows representative examples for each failure
category. 
 
 
 
 Distributed redundant (37.7%) 
 
 
 The localization finds neurons (median 2) but the edit has zero or near-zero effect (BLEU remains at or near 1.00). The memorized content is natural prose without repetitive structure, suggesting redundant encoding across many MLP neurons beyond our top- k k budget. Dominant in universal failures (78% of that stratum). 
 
 Weak edit signal (26.7%) 
 
 
 The edit partially succeeds (BLEU drops to 0.6–0.95) but does not cross the success threshold. These samples have the highest median neuron count (4), indicating correct localization but insufficient rank-one updates. Dominant in mode-specific failures and largely absent from universal failures, confirming it reflects edit strength rather than localization accuracy . 
 
 Low MLP signal (15.0%) 
 
 
 Repetitive patterns, sequential lists, and context-mirroring sequences where the localization step identifies few contributing neurons (lowest median neuron count: 1). These sequences do not show elevated attention attribution relative to successes (§ 6.2 ); the memorization signal is distributed too broadly for our pipeline to concentrate into a small set of editable neurons. Concentrated in the no-neurons stratum (80% of those 50 samples). 
 
 High-frequency target (10.0%) 
 
 
 The first continuation token is a common word (comma, function word, punctuation) with high prior probability across many contexts. The edit competes with a strong baseline signal from unedited neurons, making the target difficult to displace regardless of localization quality (median 3 neurons). 
 
 Factual recall (5.7%) 
 
 
 Widely-known facts (dates, proper nouns, institutional names) that appear many times across the training corpus, encoded broadly rather than in a single memorized passage. 
 
 Short context (3.3%) 
 
 
 Context prefixes of 1–4 tokens, too short for reliable localization. All from the universal failure stratum. 
 
 Structural template (1.7%) 
 
 
 Legal boilerplate and disclaimers with rigid format-level patterns. Modes that break the format entirely (EOS, next-best) succeed; Redact fails because the template structure is stronger than a content-level nudge to a single filler token. 
 
 
 
 
 Table 14: Representative examples for each failure category. n neu n_{\text{neu}} = number of neurons found by the localization pipeline. BLEU values are between pre-edit and post-edit generations; lower is better ( < 0.6 {<}0.6 = success). 
 
 
 
 
 
 Category 
 
 n neu n_{\text{neu}} 
 
 
 Context + memorized continuation 
 
 
 
 Best edit outcome 
 
 
 
 
 
 
 
 
 Distributed 
 redundant (37.7%) 
 
 
 4 
 
 
 Telnet freenetina.cwru.edu or freenetinb → \rightarrow …cwru.edu. The freenetina.cwru.edu server is a Tel 
 
 
 
 Unchanged (BLEU = 1.00 across all modes) 
 
 
 
 2 
 
 
 They specialize in the Boca Raton area including High → \rightarrow …Highland Beach, Delray Beach, Boynton Beach 
 
 
 
 Unchanged (BLEU = 1.00 across all modes) 
 
 
 
 
 
 
 Weak edit 
 signal (26.7%) 
 
 
 7 
 
 
 Thus we hear of the Ishtar of Ar → \rightarrow …bela, the Ishtar of Nineveh, the Ishtar of Babylon 
 
 
 
 Suppress reaches 0.48 (crosses threshold); EOS only reaches 0.64 
 
 
 
 3 
 
 
 Written by Peter Jackson, → \rightarrow …based on the novel by J.R.R. Tolkien. Starring Elijah 
 
 
 
 NB: …Fran Walsh, and Philippa Boyens (0.14, succeeds); EOS: 0.73 (fails) 
 
 
 
 
 
 
 Low MLP 
 signal (15.0%) 
 
 
 2 
 
 
 We read of the Persian Sibyl, the Libyan, the Del → \rightarrow …phic, the Egyptian, the Chaldean, the Phoenician 
 
 
 
 Sequential list; best BLEU = 0.71 (all modes fail) 
 
 
 
 3 
 
 
 Nadal, Fed → \rightarrow …erer, Djokovic, Murray, Del Potro, Wawrinka, Thiem 
 
 
 
 Name list; unchanged across all modes 
 
 
 
 
 
 
 High-freq. 
 target (10.0%) 
 
 
 3 
 
 
 Lloyd Cole, this most ingenious of British singers → \rightarrow …has been a constant presence on the British musi 
 
 
 
 All modes reach BLEU = 0.84; target token is high-frequency 
 
 
 
 3 
 
 
 You agree to defend, indemnify and hold Chivas, its directors → \rightarrow …officers, employees, agents and affil 
 
 
 
 NB succeeds (0.00); EOS stuck at 0.86 
 
 
 
 
 
 
 Factual 
 recall (5.7%) 
 
 
 2 
 
 
 On the 22d day of October, 1811, Franz Lis → \rightarrow …zt, the celebrated pianist, was born at Raiding 
 
 
 
 NB: …a Hungarian, was born at Buda (0.16, succeeds); EOS unchanged 
 
 
 
 4 
 
 
 Her second son, the worthy person of whom I am now to give a → \rightarrow …short account, was born in the year 176 
 
 
 
 Suppress: 0.47 (succeeds); others shift date but stay above threshold 
 
 
 
 
 
 
 Short 
 context (3.3%) 
 
 
 1 
 
 
 There is a culture of → \rightarrow …fear in the workplace. The culture of fear is a culture of 
 
 
 
 Unchanged (BLEU = 1.00); 4-word context 
 
 
 
 1 
 
 
 Also in 2012, Satriani → \rightarrow …released his first live album, “Live in San Francisco” 
 
 
 
 Unchanged (BLEU = 1.00); 4-word context 
 
 
 
 
 
 
 Structural 
 template (1.7%) 
 
 
 5 
 
 
 TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW → \rightarrow …IN NO EVENT SHALL THE COMPANY, ITS AFFILIATES 
 
 
 
 EOS/NB succeed (0.00); redact fails (0.67) 
 
 
 
 3 
 
 
 THE EXPRESS WARRANTIES IN THIS AG → \rightarrow …REEMENT ARE IN LIEU OF ALL OTHER WARRANTIES 
 
 
 
 EOS/NB succeed (0.00); suppress unchanged 
 
 
 
 
 
 
 Annotation Prompt: Failure Mode Classification 
 
 
 You are classifying why a specific edit on a memorized sequence in OLMo-7B failed to suppress
the memorization. The edit method, called output vector editing , identifies MLP neurons
responsible for a memorized continuation and applies a closed-form rank-1 update to their output
vectors. An edit is considered successful if the post-edit BLEU vs. the pre-edit memorized
continuation drops below 0.6. 
 You will be given a single failure case with the following fields: 
 
 • 
 
 STRATUM : one of UNIVERSAL_FAIL , EOS_FAIL_OTHERS_SUCCEED ,
 REDACT_FAIL_EOS_SUCCEED , SUPPRESS_FAIL_EOS_NB_SUCCEED ,
 NB_FAIL_EOS_SUCCEED , SKIPPED_NO_NEURONS 
 
 • 
 
 NEURONS_FOUND : number of MLP neurons identified by the localization step
(0 = no neurons found, edit never attempted) 
 
 • 
 
 BLEU_EOS , BLEU_SUPPRESS , BLEU_NB , BLEU_REDACT :
BLEU scores after each edit mode (lower = = more change; below 0.6 = = success) 
 
 • 
 
 CONTEXT : the prefix fed to the model 
 
 • 
 
 BEFORE_TEXT : the model’s memorized continuation before any edit 
 
 • 
 
 AFTER_EOS , AFTER_SUPPRESS , AFTER_NB , AFTER_REDACT :
what each mode produced after editing 
 
 • 
 
 AUTO_TAGS : pre-applied automatic tags ( few_neurons ,
 no_neurons_found , unchanged , redact_unchanged ,
 borderline_bleu , repetitive ) 
 
 
 Classify the failure into exactly ONE of the following seven categories. Read the rubrics
carefully — they describe distinct failure modes. 
 
 low_mlp_signal 
 
 
 The MLP signal is too weak or too distributed for the localization step
to identify a usable set of neurons. Indicators: NEURONS_FOUND is low (0–2); the
continuation is repetitive (e.g., “CRACK, CRACK, CRACK”), a sequential list, a numbered
enumeration, or closely mirrors patterns already present in CONTEXT (copy/induction
behaviour), suggesting attention rather than MLP storage is the dominant pathway. 
 
 distributed_redundant 
 
 
 Neurons were found (typically 1–2) but the text is natural prose
and BLEU is exactly 1.00 across all modes — the edit had zero effect despite finding neurons,
indicating memorization is spread across too many neurons or layers beyond the top- k k budget.
Distinguishable from low_mlp_signal by: (a) prose text, not repetitive/template;
(b) at least some neurons found. 
 
 weak_edit_signal 
 
 
 Neurons were found and the edit changed the output, but not enough to
cross the threshold. Indicators: BLEU between 0.6 and 0.95 in at least one mode;
 AFTER_EOS shows some change from BEFORE_TEXT but core content persists.
Often applies to REDACT_FAIL_EOS_SUCCEED samples where redact was too weak but EOS
was strong enough. 
 
 high_freq_target 
 
 
 The target token is a very common token—punctuation, stopword, digit,
or newline—with a strong global prior. The rank-1 update must compete against this corpus-wide
frequency signal. Indicators: CONTEXT ends at a natural breakpoint (period, comma,
colon); BEFORE_TEXT starts with a high-frequency token; multiple modes fail despite
 NEURONS_FOUND > 0 >0 . 
 
 factual_recall 
 
 
 The memorized content is factual knowledge—proper nouns, dates,
statistics, institutional names—rather than verbatim passage memorization. The model “knows”
this through general training rather than memorizing a specific passage, so editing one neuron
cannot remove broadly-encoded knowledge. 
 
 structural_template 
 
 
 The memorized text follows a rigid structural template where format
dominates content: legal boilerplate, copyright notices, terms of service, URLs, email addresses,
code snippets, HTML, table headers, structured lists with consistent formatting. 
 
 short_context 
 
 
 The CONTEXT prefix is very short (under 20 characters or fewer
than 4 tokens), giving the localization step too little signal to identify discriminative neurons.
The model may be generating from general knowledge rather than a specific memorized sequence. 
 
 
 Instructions: 
 
 1. 
 
 Read CONTEXT , BEFORE_TEXT , and all four AFTER_* columns. 
 
 2. 
 
 Compare BLEU scores across modes — if one mode has much lower BLEU, the edit
partially worked in that mode. 
 
 3. 
 
 Use AUTO_TAGS and NEURONS_FOUND as hints, not as definitive
evidence. 
 
 4. 
 
 Assign the single best-fitting label. If a sample fits multiple categories, choose
the primary cause of failure. 
 
 
 Stratum-specific guidance: 
 
 • 
 
 SKIPPED_NO_NEURONS : choose between low_mlp_signal ,
 structural_template , and short_context — no neurons were found, so
the question is why not. 
 
 • 
 
 UNIVERSAL_FAIL : neurons_found is very low (median 2); choose
between distributed_redundant (prose, edit had zero effect) and
 low_mlp_signal (structured/repetitive text). 
 
 • 
 
 SUPPRESS_FAIL / NB_FAIL : compare after_suppress or
 after_nb with after_eos — if EOS broke the memorization but the
other mode did not, the question is why that specific mode was insufficient. 
 
 
 Decision Rules (apply in order): 
 
 1. 
 
 If NEURONS_FOUND is 0, the label must be one of
{ low_mlp_signal , structural_template , short_context }. 
 
 2. 
 
 If CONTEXT is shorter than 4 tokens, default to short_context 
unless BEFORE_TEXT is overwhelmingly templated. 
 
 3. 
 
 If all four BLEU values are ≥ 0.95 \geq 0.95 , choose between
 distributed_redundant (prose, neurons found) and low_mlp_signal 
(structured, low/zero n
