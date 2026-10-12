# KnowledgePacks — arXiv 2604.03270

Source: https://arxiv.org/html/2604.03270

## Headings
# Knowledge Packs: Zero-Token Knowledge Delivery
 via KV Cache Injection
## 1 Introduction
## 2 Method
### 2.1 KV Cache Injection
#### Write phase (offline, once).
#### Read phase (per query).
#### Chat template requirement.
### 2.2 KV–Prefix Equivalence Property
### 2.3 Banked Routing
### 2.4 KV Composition
## 3 Experimental Setup
#### Models.
#### Benchmarks.
#### Methods compared.
#### Retrieval.
#### Evaluation.
## 4 Results
### 4.1 HotpotQA: KV = RAG at Zero Token Cost
### 4.2 Accumulation Scaling: Constant vs. Linear Token Cost
### 4.3 Chat Template Analysis
#### Template split pitfall.
### 4.4 Scaling with Banked Routing
### 4.5 KV Composition
### 4.6 Beyond Equivalence: Value-Space Steering
### 4.7 Dual-Channel Architecture: Knowledge + Steering
## 5 Analysis and Discussion
#### Chat template as distribution shift.
## 6 Related Work
#### RAG.
#### KV cache compression and serving.
#### Prompt and prefix tuning.
#### Activation steering.
#### Knowledge editing.
## 7 Conclusion
#### Limitations.
## References
## Appendix A Proof of KV–Prefix Equivalence
## Appendix B Synthetic Scaling Tests
## Instructions for reporting errors

## Keyword counts
{"paraphrase": 0, "held-out": 0, "held out": 0, "generaliz": 0, "multi-token": 0, "unseen": 0, "novel entit": 0, "new entit": 0, "counterfact": 0, "zsre": 0, "teacher forc": 0, "autoregressive": 0, "subject": 0, "last token": 0, "embedding": 5, "vocabulary": 0, "propagat": 1}


## SECTION: 2 Method



 



## SECTION: 3 Experimental Setup



 



## SECTION: Benchmarks.



 
 
 • 
 
 HotpotQA ( Yang et al., 2018 ) : Multi-hop QA with 2 gold + 8 distractor paragraphs per question. N = 500 N{=}500 (Qwen) and N = 200 N{=}200 (Llama) from the dev set (75% bridge + 25% comparison). 
 
 • 
 
 HotpotQA Accumulation : Same question pool with 1–5 sequential retrieval steps, measuring how token cost scales. N = 100 N{=}100 per level per model. 
 
 • 
 
 Value Steering : 15 coding tasks scored for defensive patterns (0–9 scale), tested with 30 contrastive code example pairs (“good”: defensive, error-handling vs. “bad”: sloppy, no checks). Both models. 
 
 • 
 
 Dual-Channel : 200 HotpotQA bridge questions with simultaneous knowledge KV and formality V-delta, measuring both factual EM and behavioral effect. Qwen3-8B. 
 
 
 
 
 



## SECTION: Methods compared.



 
 
 • 
 
 Baseline : No external knowledge. 
 
 • 
 
 RAG : Retrieved paragraphs in system message via chat template. 
 
 • 
 
 KV-chat : Same paragraphs as KV cache, built with chat template (same system message as RAG). Identical text and formatting; only the delivery mechanism differs. 
 
 • 
 
 KV-raw : Same paragraphs as KV cache, built from raw text without chat template. Included to quantify the chat template effect. 
 
 
 
 
 This is important: RAG and KV-chat use identical system messages, character for character. The only variable is whether the text arrives via prompt or via pre-computed cache. Without this control, formatting differences alone can produce 5–10pp gaps, as we show in Section  4.3 . 
 
 
 



## SECTION: Evaluation.



 
 Exact match (gold answer substring in prediction) and token-overlap F1. 
 
 
 
 



## SECTION: 4 Results



 



## SECTION: 4.3 Chat Template Analysis



 
 Why does some prior work report KV > > RAG? 
 
 
 Table 3 : Chat template effect by model and question type. 
 
 
 
 Model 
 Method 
 Overall 
 Bridge 
 Comp. 
 
 
 
 Qwen3-8B 
 KV-chat 
 65.2% 
 60.5% 
 79.2% 
 
 KV-raw 
 59.2% 
 54.1% 
 74.4% 
 
 Difference 
 +6.0pp 
 +6.4pp 
 +4.8pp 
 
 Llama-3.1-8B 
 KV-chat 
 61.5% 
 56.7% 
 76.0% 
 
 KV-raw 
 56.0% 
 49.3% 
 76.0% 
 
 Difference 
 +5.5pp 
 +7.4pp 
 0.0pp 
 
 
 
 
 The gap is 5.5–6.0pp overall, concentrated on bridge questions where the model needs to cross-reference multiple facts. 
 
 



## SECTION: 5 Analysis and Discussion



 
 KV = RAG is not a negative result. It is a lossless optimization: swap in a cache, get the same outputs, no tuning. The use cases are pay-per-token APIs, long conversations, agentic workflows. Build cost is ∼ {\sim} 5ms/fact. The main downside is that a Llama cache will not load into Qwen—KV caches are tied to a specific architecture, unlike RAG text. 
 
 

