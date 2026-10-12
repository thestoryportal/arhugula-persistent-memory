# Same-Entity Multi-Attribute Locality in LLM Knowledge Editing

**A Comprehensive Synthesis of Failure Modes, Methods, and Evaluation (2022–2026)**

---

## Executive Summary

**Direct verdict:** Same-entity multi-attribute locality — the property that editing one attribute of an entity leaves all other attributes of that same entity intact — is *not* solved by any weight-editing method available as of mid-2026. It is structurally achievable *only* by parameter-preserving (retrieval/external-memory) approaches, at the cost of generalization and scale constraints. The failure of weight-editing methods is not incidental: it is a direct consequence of how transformers encode entity knowledge, and several independent research threads confirm the mechanism.

The core problem has a precise name and cause: ROME and MEMIT compute the MLP key from the subject's last-token representation, and all attributes of the same entity share an almost identical key. Injecting a new value for one attribute therefore overwrites or interferes with the stored values for every other attribute bound to that key. The [NAACL 2025 Same-Subject Editing paper](https://aclanthology.org/2025.naacl-short.31.pdf) named this "related knowledge perturbation." [MEMIT-Merge (arXiv:2502.07322)](https://arxiv.org/abs/2502.07322) independently confirmed that "identical keys (derived from the shared subject) are forced to represent different values," causing success rates to collapse from ~90% to ~50% as same-entity edit batches grow.

**Ranked shortlist of best current options** (see §5 for full treatment):

| Rank | Method | Type | Same-Entity Locality | Trade-off |
|------|--------|------|---------------------|-----------|
| 1 | SERAC | Retrieval | Near-perfect (98.96–100%) | Poor generalization at scale |
| 2 | GRACE | Retrieval | Near-perfect by construction | Semantic drift at 10K+ edits |
| 3 | DiKE | Weight-edit | Best weight-edit locality | New method; limited benchmarks |
| 4 | AlphaEdit + null-space | Weight-edit | +36.7% avg improvement | Does not fully solve same-subject keys |
| 5 | WISE | Hybrid dual-memory | Loc. >0.93 (Hallucination set) | Fails at 10K+ edits |
| 6 | PRUNE | Weight-edit | Best sequential stability | Does not address same-subject directly |

**Best evaluation metric:** Jensen–Shannon divergence over the object-set distribution (Knowledge Distortion metric) for same-entity locality, combined with the RippleEdits Relation Specificity criterion. Standard Neighborhood Success is insufficient — it measures cross-entity, not intra-entity effects.

---

## 1. Same-Entity Locality: Benchmarks and Metric Definitions

### 1.1 The Gap in Standard Evaluation

The canonical knowledge editing evaluation framework defines four properties: *reliability* (the edited fact is recalled), *locality* (unrelated facts are unchanged), *generalization* (paraphrased queries reflect the edit), and *portability* (downstream reasoning chains update correctly). The standard locality metric — "Neighborhood Success" — tests whether facts about *different* entities are preserved after an edit. It says nothing about whether other attributes of the *same* entity survive.

[RippleEdits (Cohen et al., arXiv:2307.12976, TACL 2024)](https://arxiv.org/abs/2307.12976) was the first benchmark to address this gap systematically. It defines six evaluation criteria capturing distinct ripple-effect types. Two are directly relevant here:

- **Relation Specificity**: "Any other attributes of the subject, which have been previously updated, should remain unaltered following the editing process." This is the formal definition of same-entity locality.
- **Forgetfulness**: Whether the model retains original objects for one-to-many relations (e.g., all of an author's books) after editing one of them.

RippleEdits contains 5,000 factual edits spanning diverse relation types. The benchmark's central finding is damning: "current methods fail to introduce consistent changes in the model's knowledge." The in-context editing baseline (IKE) outperforms all weight-editing methods — a result that foreshadows the retrieval-vs.-weights debate.

### 1.2 KnowEdit: Quantified Same-Entity Locality

[KnowEdit (Zhang et al., arXiv:2401.01286, 2024)](https://arxiv.org/abs/2401.01286) introduces a formal locality metric:

\[\text{Locality} = \mathbb{E}_{x_k, y_k^*} \mathbf{1}\{f_{\theta'}(y \mid x_k) = f_\theta(y \mid x_k)\}\]

where \(x_k\) is a query about a preserved attribute and \(f_{\theta'}\) is the post-edit model. A KL-divergence variant is used for conversational settings where token-match is too strict. KnowEdit defines **Relation Specificity** as the same-entity locality axis and reports the following on WikiData benchmarks:

| Method | Relation Specificity (%) | Notes |
|--------|--------------------------|-------|
| ROME | 51.97–54.77 | Token-match locality on WikiData |
| MEMIT | 46.62–52.15 | Slightly worse than ROME on locality |
| SERAC | 98.96–100.00 | Near-perfect; doesn't touch weights |
| FT-L | ~45 | Fine-tuning baseline |

For conversational datasets (ConvSent), the KL-divergence locality scores are: ROME = 0.00, MEMIT = 0.00, SERAC = 0.26 (lower is better, meaning KL divergence from unedited model behavior). This confirms that weight-editing methods essentially fail the same-entity locality test for conversational queries.

### 1.3 MQuAKE: Multi-Hop Ripple Effects

[MQuAKE (Zhong et al., arXiv:2305.14795, 2023)](https://arxiv.org/abs/2305.14795) extends the evaluation to multi-hop questions — cases where editing one fact (e.g., the president of a country) should propagate through chains of dependent facts (e.g., who signs a particular treaty). The benchmark finds that "current KE approaches fail catastrophically on multi-hop questions" even when single-hop edits succeed, confirming that knowledge consistency across attributes is not maintained. MQuAKE also introduces MeLLo (discussed in §4.3), a retrieval-based solution to this failure.

### 1.4 Same-Subject Editing Benchmark (NAACL 2025)

The most focused treatment of same-entity multi-attribute editing is ["Rethinking Multiple Pieces of Knowledge Editing in Same-Subject Editing" (NAACL 2025)](https://aclanthology.org/2025.naacl-short.31.pdf). This paper constructs a benchmark where an entity like "James" requires simultaneous edits to "isCitizenOf," "playsFor," and other attributes, and evaluates whether edits to one attribute corrupt previously made edits to other attributes of the same entity.

The paper introduces **Score Difference (SD)** — the gap between a method's performance under normal single-attribute editing and same-subject multi-attribute editing. The key finding: "Only mainstream locate-then-edit methods, such as ROME and MEMIT, exhibit 'related knowledge perturbation,' where subsequent edits interfere with earlier ones." Methods including PMET also show significant negative SD. In contrast, methods that do not over-rely on the subject representation are unaffected.

### 1.5 Knowledge Distortion Metric

[A 2024 pitfalls survey (arXiv:2406.01436)](https://arxiv.org/html/2406.01436v1) introduces **Knowledge Distortion**, defined as the Jensen–Shannon divergence of the object-set distribution before and after editing:

\[\text{KD}(s, r) = \text{JS}(P_\theta(o \mid s, r) \| P_{\theta'}(o \mid s, r))\]

This captures subtle distributional shifts in which objects a model associates with a subject-relation pair, rather than binary token-match. It is particularly sensitive to same-entity collateral: editing one (s, r) pair can shift the distribution over all (s, r') pairs by perturbing shared subject representations.

---

## 2. Weight-Editing Methods: How Much Do They Reduce Same-Entity Collateral?

### 2.1 The Baseline: ROME and MEMIT

[ROME (Meng et al., 2022)](https://arxiv.org/abs/2310.16218) operates by applying a rank-one update to a specific MLP weight matrix \(W\) at a layer identified by causal tracing. The update is:

\[W' = W + \Lambda (C^{-1} k^*)^T\]

where \(k^*\) is the key derived from the subject's last-token representation in the MLP's down-projection layer, \(\Lambda\) encodes the target value, and \(C\) is a covariance matrix computed over a fixed corpus. MEMIT extends this to batch edits spread across multiple layers.

The critical architectural choice — deriving the key solely from the subject's last-token representation — is precisely what creates same-entity interference. When two edits share the same subject (different relations), their keys \(k^*\) are nearly identical, so the second edit's weight update partially overwrites the first's. This is the mechanism identified in the [NAACL 2025 paper](https://aclanthology.org/2025.naacl-short.31.pdf) and independently confirmed by [MEMIT-Merge (arXiv:2502.07322)](https://arxiv.org/abs/2502.07322).

[EMMET (Gupta et al., arXiv:2403.14236, 2024)](https://arxiv.org/abs/2403.14236) proves that ROME and MEMIT optimize the same preservation-memorization (PM) objective — ROME uses an equality constraint for single edits, while MEMIT uses a least-squares relaxation enabling batch edits. The unification under EMMET demonstrates that these two methods are not meaningfully distinct in their fundamental mechanism, only in their optimization approach. EMMET itself shows performance comparable to MEMIT at batch sizes up to 256, but the equality constraint becomes too strong for very large batches.

### 2.2 AlphaEdit: Null-Space Projection

[AlphaEdit (arXiv:2410.02355, 2024)](https://arxiv.org/abs/2410.02355) represents the most principled attempt to solve locality within the weight-editing paradigm. The key innovation is projecting the parameter perturbation \(\Delta W\) onto the null space of the preserved-knowledge matrix \(P\) before applying it:

\[\Delta W_\perp = (I - P P^\dagger) \Delta W\]

The projection \((I - P P^\dagger)\) is the orthogonal complement of the row space of \(P\), ensuring that \(\Delta W_\perp P^\top = 0\). The paper provides a theoretical proof that "projection ensures the output of post-edited LLMs remains unchanged when queried about the preserved knowledge."

Empirically, AlphaEdit achieves a +36.7% average improvement across most locating-then-editing methods on LLaMA3, GPT2-XL, and GPT-J. However, an important limitation applies: the null-space projection preserves the *aggregate* knowledge distribution represented in \(P\), but \(P\) is typically computed over a *cross-entity* corpus (e.g., random Wikipedia sentences), not over the specific other attributes of the edited entity. The projection therefore does not specifically protect same-entity attributes — it protects general model behavior. Same-entity locality remains a target not explicitly addressed by AlphaEdit's constraint construction.

### 2.3 PMET: Separating Attention and FFN Roles

[PMET (arXiv:2308.08742, AAAI 2024)](https://arxiv.org/abs/2308.08742) is motivated by the observation that multi-head self-attention (MHSA) layers encode "general knowledge extraction patterns" while FFN layers store factual associations. PMET simultaneously optimizes Transformer Component (TC = MHSA + FFN) hidden states but applies the weight update only to FFN weights, not MHSA. This preserves the extraction patterns used across all factual queries while still injecting new factual content.

PMET achieves state-of-the-art performance on COUNTERFACT and zsRE benchmarks. However, the [NAACL 2025 Same-Subject paper](https://aclanthology.org/2025.naacl-short.31.pdf) reports that PMET also exhibits significant negative Score Difference in same-subject editing — the pattern-preserving approach does not resolve the key collision problem because the FFN key is still derived from the subject representation.

### 2.4 PRUNE: Controlling Condition Number Degradation

[PRUNE (arXiv:2405.16821, ICLR 2025)](https://arxiv.org/abs/2405.16821) addresses a different but related problem: the degradation of general model abilities during *sequential* editing. The paper's key theoretical insight is that "the factor affecting general abilities in sequential model editing lies in the condition number of the edited matrix." As edits accumulate, the condition number of the weight matrices grows, amplifying the perturbation's effect on unrelated queries.

PRUNE applies condition-number restraints to bound the perturbation magnitude:

\[\kappa(W') \leq \kappa_{\max}\]

This preserves general abilities (reasoning, language modeling) in sequential editing but does not specifically address same-entity attribute collisions. PRUNE is best understood as protecting *cross-entity* and *general-capability* locality, not *intra-entity* locality. It is complementary to, not a substitute for, same-entity locality solutions.

### 2.5 WISE: Dual Parametric Memory

[WISE (arXiv:2405.14768, NeurIPS 2024)](https://arxiv.org/abs/2405.14768) takes a fundamentally different architecture: it maintains a frozen main memory (the original pretrained weights) alongside a side memory (an edited copy of a single FFN layer). A router mechanism decides which memory path to activate based on an activation threshold \(\varepsilon\):

\[h' = \begin{cases} h_{\text{side}} & \text{if } \text{sim}(x, x_{\text{edit}}) > \varepsilon \\ h_{\text{main}} & \text{otherwise} \end{cases}\]

Knowledge sharding ensures different edits are stored in orthogonal parameter subspaces within the side memory. At T=1,000 edits, WISE achieves reliability scores of 0.83/0.79 on LLaMA/Mistral and locality above 0.93 on the Hallucination dataset. [KnowEdit](https://arxiv.org/abs/2401.01286) reports that WISE outperforms locate-and-edit methods across GPT, LLaMA, and Mistral, demonstrating cross-architecture consistency.

WISE's "impossible triangle" analysis is particularly important: it argues that reliability, generalization, and locality "cannot be realized together in the lifelong editing settings." Long-term memory (weight editing) fails locality; working memory (retrieval) fails generalization. WISE attempts a middle path but inherits weaknesses from both: it "struggles to retain updates over time" at very large scale (10K+ edits) and is "restricted to token-level corrections," limiting its utility for complex multi-attribute entity knowledge.

### 2.6 DiKE: Knowledge Representation Disentanglement

The most direct weight-editing solution to same-entity collateral, [DiKE (arXiv:2505.18774, 2025)](https://renzhaochun.github.io/assets/pdf/2505.18774v1.pdf) explicitly addresses the entanglement problem. The core observation: "subject representations inherently encode multiple attributes, causing the target and fine-grained irrelevant knowledge to become entangled in the representation space." DiKE introduces a Knowledge Representation Disentanglement (KRD) module that decomposes the subject representation into target-knowledge-related and target-knowledge-unrelated components, then constrains only the former during editing.

Experiments on FINE-KED and COUNTERFACT benchmarks show DiKE "effectively preserves fine-grained unrelated knowledge while achieving comparable general edit performance with other state-of-the-art editing methods." DiKE is the only weight-editing method that directly and explicitly targets same-entity attribute preservation. It is, however, a relatively new method (May 2025) with limited independent replication.

### 2.7 WilKE and MEMoE: Addressing Lifelong Degradation

[WilKE (arXiv:2402.10987, 2024)](https://arxiv.org/abs/2402.10987) addresses "toxicity buildup" in lifelong editing by selecting layers based on pattern matching degree rather than fixed layer indices, achieving +46.2%/67.8% improvement on GPT2-XL/GPT-J respectively in lifelong sequential settings. [MEMoE (arXiv:2405.19086)](https://arxiv.org/abs/2405.19086) uses Mixture-of-Experts adapters to route different edit types through separate expert pathways, reducing inter-edit interference.

### 2.8 Capacity Arguments: Is Weight Editing Fundamentally Limited?

Beyond specific method failures, there are theoretical arguments that weight editing of the ROME/MEMIT type is fundamentally capacity-limited. [Model Editing at Scale Leads to Gradual and Catastrophic Forgetting (arXiv:2401.07453)](https://arxiv.org/abs/2401.07453) demonstrates that editing methods "fail drastically with only 1000 edits" in practice. The [Dimensional Collapse Hypothesis (arXiv:2606.00570, 2026)](https://arxiv.org/html/2606.00570v1) provides the theoretical framing: "localized parameter edits can propagate along fragile directions in the representation space, inducing global interference and ultimately causing reasoning collapse." The paper concludes that "a simple retrieval-based baseline achieves consistently stronger performance than all parameter-editing methods across all evaluated conditions."

The understanding of *why* this happens — the mechanistic interpretation — is covered in §3.

---

## 3. Mechanistic Explanation: Why Does the Subject Last Token Bleed?

### 3.1 The Key-Value Collision

The fundamental mechanism is well-established across multiple independent analyses. ROME/MEMIT derive the MLP key \(k^*\) from the hidden state at the subject's last token position. This hidden state encodes the entity as a whole — it is the model's compressed representation of "all that is known about entity E." Because this representation is shared across all subject-relation pairs involving E, every edit targeting E uses an almost identical key.

When a second attribute of E is edited (e.g., after editing "playsFor" to encode a new club, then editing "isCitizenOf" to encode a new country), the weight update for the second edit is computed to satisfy:

\[W' k^* \approx v_2^*\]

where \(v_2^*\) is the target value for the second attribute. But \(W'\) (already modified by the first edit) must also satisfy:

\[W' k^* \approx v_1^*\]

Since both equations use the same \(k^*\), the second update necessarily degrades the first. This is precisely what [NAACL 2025](https://aclanthology.org/2025.naacl-short.31.pdf) terms "related knowledge perturbation": "When multiple related pieces of knowledge share the same subject, the calculated keys remain highly similar. As a result, subsequent edits interfere with earlier ones."

### 3.2 Suppression Rather Than Overwriting

A surprising 2025 mechanistic finding complicates the picture further. ["One Mask to Rule Them All" (arXiv:2605.28839, 2025)](https://arxiv.org/pdf/2605.28839v1.pdf) shows that ROME and MEMIT do not actually overwrite factual knowledge in the model's weights. Instead, they "succeed not by overwriting original factual knowledge, but by suppressing it" — they induce *overattention* to the edited weights, amplifying signals that force the model to output the new fact while suppressing propagation of the original. A compact binary mask trained over the edited weights can reverse 80% of ROME edits (using only 10% of the edited layer's weights) and 82% of MEMIT edits (using only 4.5% of the edited layer's weights, or 0.9% of total edited weights). This suppression mechanism explains why ROME and MEMIT fail to propagate changes to related facts — the original knowledge is still there, merely masked, and can "leak through" for attributes using related subject representations.

### 3.3 Representation Shattering

[Nishi et al. (arXiv:2410.17194, 2024)](https://arxiv.org/abs/2410.17194) coined "representation shattering" to describe a broader consequence: "KE inadvertently affects representations of entities beyond the targeted one, distorting relevant structures that allow a model to infer unseen knowledge about an entity." The effect is confirmed on pre-trained LLaMA and Mamba models. The study finds that edited models not only fail to update related facts correctly — they lose the *capacity* to infer those facts, because the representation structure that encoded entity-attribute associations has been disrupted.

### 3.4 Subject-Sharing Asymmetry

[Side Effects of Rank-One Editing (ACL BlackboxNLP 2025)](https://aclanthology.org/2025.blackboxnlp-1.11.pdf) provides a particularly clean dissection. The paper distinguishes "subject-sharing knowledge" (same entity, different relation) from "relation-sharing knowledge" (same relation type, different entity) and measures preservation rates for both after a ROME edit. The finding is stark: "relation-sharing knowledge is exceptionally well preserved (Rel. SS and Rel. SM consistently near 100%). However, subject-sharing knowledge shows substantially lower preservation rates, particularly in Subject Sharing Match (Subj. SM)." The paper analyzes the weight update matrix and finds mechanistic evidence: "ROME exhibits a stronger effect on subject-sharing knowledge instances" because the update direction aligns with the subject-token representation that is shared across all knowledge involving that entity.

### 3.5 Localization Does Not Validate Editing

An important challenge to the entire foundation of locate-then-edit comes from [Hase et al. (arXiv:2301.04213, 2023)](https://arxiv.org/abs/2301.04213): "localization conclusions from representation denoising (Causal Tracing) do not provide any insight into which model MLP layer would be best to edit." The causal tracing methodology that underpins ROME's layer selection identifies which layers are *causally important* for the original fact recall, but this does not mean those layers are the right targets for *changing* that fact without side effects. This is a foundational critique: even if we perfectly locate where knowledge lives, that location may not be the right edit site for multi-attribute entities.

### 3.6 The "Flex Tape" Effect: Attribute-Specific Vulnerability

["Flex Tape Can't Fix That" (arXiv:2403.00180, 2024)](https://arxiv.org/abs/2403.00180) documents that same-entity damage is not uniform across attribute types. "Editing facts about place of birth, country of citizenship, or gender have particularly negative effects on the model's knowledge about unrelated features like field of work." This suggests that some attributes share more "representational space" in the subject token than others, creating a non-uniform vulnerability profile. Highly connected subjects — those with many relations — show greater spillover effects than less-connected entities, per the BlackboxNLP 2025 analysis.

---

## 4. Parameter-Preserving and Retrieval Methods

### 4.1 SERAC: Scope-Classified External Memory

[SERAC (Mitchell et al., arXiv:2206.06520, 2022)](https://arxiv.org/abs/2206.06520) is a semi-parametric architecture storing edits in an explicit external memory alongside a trained scope classifier. At inference, the scope classifier determines whether an input query falls within the edit's scope; if yes, the external edit is applied; if no, the original model is used. Because the original weights are never modified, same-entity locality is achieved *by construction*: queries about unedited attributes route to the unchanged model.

KnowEdit reports SERAC achieves 98.96–100.00% locality on WikiData benchmarks — essentially perfect. The [pitfalls survey](https://arxiv.org/html/2406.01436v1) confirms "only SERAC achieves high performance across all three evaluation problems" in both single and multiple edit scenarios.

SERAC's critical weakness is the scope classifier: its accuracy determines whether edits are correctly applied or not. In sequential editing at scale, the classifier can fail to recover edited facts, especially in multi-hop reasoning chains. The pitfalls survey notes that "in the multiple edit scenario, SERAC displays low edit success rate and distortion rate, suggesting its scope classifier does not adopt most edits."

### 4.2 GRACE: Discrete Key-Value Codebook

[GRACE (Hartvigsen et al., arXiv:2211.11031, 2022)](https://arxiv.org/abs/2211.11031) stores edits as a discrete key-value codebook in a separate adapter layer. During inference, if the model's hidden state at a key layer is sufficiently close to a stored edit key (within a radius \(\varepsilon\)), the associated value is retrieved and injected. Original weights are frozen. Like SERAC, GRACE achieves same-entity locality by construction — but the threshold \(\varepsilon\) must be tuned carefully to avoid radius collision between nearby concepts.

GRACE is specifically designed for lifelong sequential editing (thousands of edits) and outperforms weight-editing methods in this regime. However, performance declines severely before 10K edits in recent benchmarks, suggesting the codebook retrieval mechanism does not scale indefinitely.

### 4.3 MeLLo: Iterative Multi-Hop Retrieval

[MeLLo (Zhong et al., arXiv:2305.14795, 2023)](https://arxiv.org/abs/2305.14795), introduced as part of the MQuAKE paper, stores all edited facts externally and prompts the LLM to decompose multi-hop questions iteratively, checking the external store at each step. This explicitly handles the portability failure of weight-editing methods (where updating one fact doesn't propagate to dependent facts) while preserving locality for unrelated attributes.

### 4.4 In-Context Editing and RAG

In-context editing (IKE) prepends edited facts as context at inference time, with no weight modification. [RippleEdits](https://arxiv.org/abs/2307.12976) found IKE achieves the best overall scores on the benchmark, outperforming all weight-editing methods — a telling result. However, IKE has an obvious scaling problem: injecting hundreds or thousands of edited facts into the context window is impractical.

RAG-based editing systems solve this by storing edits in a vector database and retrieving only the relevant subset at inference time. This approach is the dominant practical solution for knowledge-base-style deployments. It achieves same-entity locality by construction, and the retrieval precision determines the locality boundary.

### 4.5 The "Impossible Triangle" and WISE's Hybrid

[WISE (NeurIPS 2024)](https://arxiv.org/abs/2405.14768) explicitly articulates the "impossible triangle": reliability, generalization, and locality cannot all be achieved simultaneously in lifelong editing settings. The WISE solution — dual parametric memory (frozen main + edited side FFN) with routing — achieves near-perfect locality on evaluated benchmarks and scales to T=1,000 edits with 0.83/0.79 reliability on LLaMA/Mistral. An [independent 2025 analysis](https://arxiv.org/html/2503.05683v1) confirms that "even WISE cannot match simple low-rank adapter-based finetuning (LoRA-FT) at scale," suggesting WISE's efficiency advantages erode beyond its intended operating range.

---

## 5. Architecture Dependence: Model-Specific Editability

### 5.1 General Architecture Findings

Architecture dependence in knowledge editing is real but nuanced. ["Should We Really Edit LLMs?" (arXiv:2410.18785)](https://arxiv.org/abs/2410.18785) identifies two cross-cutting trends: "instruction-tuned models are more robust to editing, showing less performance drop" and "language model with large scale is more resistant to editing." The second finding is double-edged — larger models are harder to successfully edit (lower reliability) but also suffer less collateral damage when edits do succeed (better locality).

### 5.2 GPT-J vs. GPT-NeoX

GPT-J (6B, EleutherAI) and GPT-NeoX (20B) use parallel attention and FFN layers (not sequential like standard transformers), which affects the causal tracing attribution pattern. ROME and MEMIT were originally benchmarked on GPT-J, and the [KnowEdit paper](https://arxiv.org/abs/2401.01286) explicitly tests ROME/MEMIT/SERAC on GPT-J. EasyEdit ([arXiv:2308.07269](https://arxiv.org/abs/2308.07269)) confirms GPT-J is the most widely evaluated model in the knowledge editing literature, making it the de facto benchmark architecture.

### 5.3 LLaMA and Llama 2

WISE ([NeurIPS 2024](https://arxiv.org/abs/2405.14768)) explicitly tests on LLaMA and reports results comparable to GPT architectures for dual-memory approaches. AlphaEdit evaluates on LLaMA3 and shows +36.7% improvement in locality metrics. The [Representation Shattering paper](https://arxiv.org/abs/2410.17194) confirms its findings on LLaMA, establishing that the representation-level effects of knowledge editing are not GPT-specific.

### 5.4 Mistral

WISE tests explicitly on Mistral (0.79 reliability at T=1,000), and [Keys to Robust Edits (arXiv:2410.09338)](https://arxiv.org/abs/2410.09338) evaluates on Mistral-7B, finding that REP (Robust Edit Pathway, which disentangles editing keys from internal representations) "significantly improves robustness across various metrics, both in-domain and out-of-domain, with minimal trade-offs in success rate and locality." Mistral's grouped-query attention (GQA) and sliding window attention differ from standard full attention, but available evidence does not show a dramatic editability difference compared to standard decoder architectures.

### 5.5 Qwen

Qwen models are less thoroughly studied in the editing literature as of this synthesis. The EasyEdit framework lists LLaMA and GPT-J as primary targets; Qwen coverage is limited to a small number of recent papers (2024–2025). No benchmark directly comparing Qwen-specific editability on same-entity metrics was identified in this review.

### 5.6 A Note of Caution on Cross-Architecture Comparison

Many benchmarks were constructed specifically for GPT-J or Llama 2 and may have implicit biases. The [Mirage of Model Editing paper (arXiv:2502.11177, 2025)](https://arxiv.org/abs/2502.11177) warns that reported performance varies dramatically based on evaluation protocol, and that cross-architecture comparisons using different benchmark versions are not reliable.

---

## 6. Evaluation Methodology: Critiques and Best Practices

### 6.1 The Mirage of Model Editing

[The Mirage of Model Editing (arXiv:2502.11177, 2025)](https://arxiv.org/abs/2502.11177) is the most consequential evaluation critique published to date. The paper reveals a gap between reported performance (96.8%) and real-world performance (38.5%) — a 58-point discrepancy. The primary cause is **teacher forcing during testing**: standard evaluation feeds the model the ground-truth prefix during generation, which "leaks both content and length of the ground truth, leading to overestimated performance." In production settings, no such signal is available.

Secondary issues identified include: evaluation on templated rather than naturally phrased queries; lack of distribution shift testing; and failure to test at realistic edit volumes. The paper confirms that "current approaches fail drastically with only 1000 edits" in teacher-forcing-free evaluation.

### 6.2 Token-Match vs. KL/JS Divergence

The [pitfalls survey (arXiv:2406.01436)](https://arxiv.org/html/2406.01436v1) documents a key debate between token-match and distributional locality metrics:

**Token-match locality** (used in KnowEdit's primary metric): measures whether the model's top prediction matches the pre-edit prediction for a preserved query. It is computationally simple and widely used, but it is binary, insensitive to near-misses, and does not capture distributional shifts.

**KL/JS divergence locality**: measures the distributional distance between pre-edit and post-edit output distributions over the preserved query. This is more sensitive — a model that has been slightly corrupted but still produces the same *top* token will pass token-match but fail KL locality. For same-entity assessment, the KD metric (Knowledge Distortion, JS divergence over object-set distributions) is superior because it captures subtle shifts in the model's probabilistic beliefs about entity attributes.

**Recommendation from current evidence**: Use JS divergence (KD metric) for same-entity locality measurement, and token-match only as a complementary coarse-grained check. The [pitfalls survey](https://arxiv.org/html/2406.01436v1) adopts both; RippleEdits uses criterion-based evaluation orthogonally.

### 6.3 Long-Form Evaluation

[Long-form evaluation of model editing (arXiv:2402.09394)](https://arxiv.org/abs/2402.09394v1) introduces an extended protocol measuring editing effects on free-form generation rather than templated short-form queries. The finding is important: "we find that our protocol has very little relationship with previous short-form metrics," confirming that short-form evaluations systematically miss degradation that manifests in open-ended generation. ROME and MEMIT "suffer much more from factual drift than other methods" under long-form evaluation.

### 6.4 The Localization Validity Question

[Hase et al. (arXiv:2301.04213)](https://arxiv.org/abs/2301.04213) and [KLoB (arXiv:2309.16535)](https://arxiv.org/abs/2309.16535) challenge the assumption that causal tracing reliably identifies the right layers to edit. KLoB finds that "many researchers have questioned the validity of the locality hypothesis of factual knowledge" and that existing localization methods cannot be tested for reliability because no ground truth exists. This undermines the foundational assumption of the entire locate-then-edit paradigm: if we cannot reliably locate knowledge, we cannot reliably edit it without collateral damage.

### 6.5 Best Practice Recommendations

Based on the evidence:

1. **Primary locality metric**: Jensen–Shannon divergence (Knowledge Distortion) over object-set distributions for same-entity queries. Do not use token-match as the sole metric.
2. **Benchmark**: RippleEdits Relation Specificity criterion for targeted same-entity assessment; KnowEdit for broad comparison against published baselines.
3. **Evaluation protocol**: Free-generation evaluation (no teacher forcing); test at realistic edit volumes (100, 500, 1K, 5K edits); include paraphrased and compositional queries.
4. **Comparison baseline**: Always include an IKE (in-context) and RAG baseline — weight-editing methods need to beat these to justify their complexity.

---

## 7. Application Angle: LLM as Multi-Field Knowledge Base

### 7.1 The Fundamental Mismatch

The goal of using an LLM as a multi-field structured knowledge base — where many independent, orthogonal fields per entity are stored and independently updatable — is fundamentally at odds with how weight-editing methods work. Weight editing in the ROME/MEMIT tradition treats all attributes of an entity as sharing a single compressed representation, making independent attribute updates structurally impossible without interference.

The [NAACL 2025 paper](https://aclanthology.org/2025.naacl-short.31.pdf) frames this precisely: entity-centric knowledge requires "resolving attribute conflicts and synchronizing interdependent facts" — but current locate-then-edit methods cannot even handle the simpler problem of keeping independent attributes of the same entity independent.

### 7.2 Architecture Recommendation

For a production LLM-as-knowledge-base system with many independent fields per entity, the evidence overwhelmingly favors **RAG-based or hybrid retrieval architectures** over weight-editing approaches:

**Option A: External Knowledge Store + RAG (recommended for most use cases)**
- Store all entity-attribute pairs in a structured external store (vector DB + structured DB)
- Retrieve at inference time using entity + attribute (relation) as retrieval keys
- Achieves same-entity locality by construction: edits to one (entity, relation) pair do not physically affect any other (entity, relation) pair
- No model weight modification; LLM serves as reasoning engine, not factual store
- Supports independent field updates trivially

**Option B: GRACE-style codebook adapter (for moderate-scale, latency-sensitive)**
- Discrete key-value adapter stores edits outside model weights
- Achieves same-entity locality by design (radius-based retrieval)
- More latency-efficient than full RAG for small edit sets (<10K)
- Degrades at very large scale

**Option C: SERAC-style scope classifier (for complex edit scoping)**
- Best when edit scopes are well-defined and non-overlapping
- Near-perfect locality (98.96–100%)
- Scope classifier accuracy is the key bottleneck

**Option D: DiKE (if weight editing is required)**
- Currently the only weight-editing method explicitly designed for same-entity attribute preservation
- Use if model weight self-containment is a hard requirement
- Validate with KD metric on target entity types before production deployment
- Expect the impossible triangle to constrain scale

### 7.3 The WISE Middle Path

For applications that specifically require a self-contained model (no external store) and moderate update volumes (hundreds to low thousands of edits), WISE offers the best trade-off. Its dual parametric memory design physically separates original knowledge from edits, the routing mechanism approximates locality by query similarity, and its knowledge sharding in orthogonal subspaces partially addresses the same-entity collision problem — though not as cleanly as pure retrieval.

### 7.4 What Not to Use

For LLM-as-knowledge-base use cases, **avoid** using ROME, MEMIT, or PMET as the primary knowledge management mechanism. Beyond the same-entity locality failure documented throughout this review, [The Mirage paper](https://arxiv.org/abs/2502.11177) shows these methods' reported reliability figures are inflated by evaluation artifacts. At production entity volumes with many attributes per entity, they will produce a model with inconsistent, partially corrupted entity representations.

---

## 8. Where Sources Disagree

Several important empirical and theoretical disagreements exist in the literature:

**1. Is AlphaEdit's null-space projection a locality solution?** The AlphaEdit authors claim theoretical guarantees that "preserved knowledge" is unaffected. However, the preserved knowledge matrix is computed over a cross-entity corpus, not over same-entity attributes. The [pitfalls survey](https://arxiv.org/html/2406.01436v1) notes that locality performance varies by metric type: AlphaEdit's +36.7% improvement is measured on standard Neighborhood Success, which tests cross-entity effects. Its performance on same-entity metrics (RippleEdits Relation Specificity) is not prominently reported.

**2. Does WISE really solve the impossible triangle?** WISE authors claim their dual-memory architecture escapes the reliability-generalization-locality trade-off. The [2025 limits paper](https://arxiv.org/html/2503.05683v1) disputes this: "even WISE cannot match simple LoRA-FT at scale." The disagreement may reflect different scale regimes (WISE is evaluated primarily at T≤1,000; the critique operates at T>10,000).

**3. Is knowledge editing salvageable at all?** The [Dimensional Collapse paper (2026)](https://arxiv.org/html/2606.00570v1) concludes that "a simple retrieval-based baseline achieves consistently stronger performance than all parameter-editing methods" and implies the field should pivot entirely to retrieval. The PRUNE, DiKE, and AlphaEdit authors disagree, presenting specific domains where weight editing outperforms retrieval. The resolution likely depends on use case: static deployments with well-defined edit scopes may still benefit from weight editing; dynamic knowledge-base applications favor retrieval.

**4. How does teacher forcing inflate benchmarks?** The [Mirage paper](https://arxiv.org/abs/2502.11177) reports a 58-point gap (96.8% → 38.5%). Earlier papers in the same venues that reported near-perfect reliability (e.g., MEMIT on COUNTERFACT) used teacher-forced evaluation. The community has not yet systematically re-benchmarked all major methods under the corrected protocol.

---

## 9. Conclusion

Same-entity multi-attribute locality is an unsolved problem for weight-editing methods as of 2026. The failure is mechanistic — subject-token representations are polysemous by design, encoding all of an entity's attributes in a single compressed key. Every weight edit that targets this key therefore risks disturbing all attributes bound to it.

The benchmark landscape has matured substantially: RippleEdits (2024), KnowEdit (2024), the NAACL 2025 Same-Subject paper, and MEMIT-Merge (2025) all independently converge on the same quantitative conclusion. Methods with the strongest locality guarantees — SERAC (98.96–100%) and GRACE — achieve them by not touching model weights at all. Weight-editing methods that attempt to address the problem (AlphaEdit, DiKE, WISE) improve meaningfully but do not close the gap.

For practitioners building systems where entities have many independently updatable fields — the LLM-as-knowledge-base pattern — the evidence strongly favors retrieval-augmented architectures over weight-editing approaches. The LLM should be treated as a reasoning engine, not a factual store. If model self-containment is a hard constraint, DiKE is currently the most targeted weight-editing option, but should be validated with JS-divergence metrics on same-entity attribute sets before production deployment.

The evaluation field faces its own crisis: the Mirage finding that real-world performance (38.5%) is 58 points below reported performance (96.8%) due to teacher-forcing artifacts means that most published reliability numbers are not production-valid. Future work should prioritize teacher-forcing-free, long-form, high-volume evaluation using JS divergence metrics over the existing token-match benchmarks.
