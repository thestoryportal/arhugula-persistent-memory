# LLM Knowledge Editing Survey: Cross-Entity Same-Relation Specificity Under Sequential In-Weight Edits

## Executive conclusion

The failure mode is real, under-addressed by standard edit-locality metrics, and best explained as overlap between edited keys and unedited same-relation keys amplified by sequential low-rank weight perturbations; the closest direct evidence comes from large-scale sequential-editing work showing edit bleedover and disabling edits, graph-based ripple-effect work showing hidden-space impact on related and even seemingly unrelated entities, and BetaEdit's 2026 analysis showing that practical null-space editing uses an approximate pseudo-null space whose leakage accumulates over long edit streams ([Model Editing at Scale](https://arxiv.org/abs/2401.07453), [Efficiently Quantifying and Mitigating the Ripple Effects of Knowledge Editing](https://arxiv.org/abs/2403.07825), [BetaEdit](https://arxiv.org/abs/2605.09285)).

For the exact setup—Qwen-family dense models, frozen base, CPU deployment, down-projection editing, early-layer edit band, sequential writes sharing a relation—the highest-confidence next prototype is not another subject-only or relation-token key; it is a leakage-aware AlphaEdit/BetaEdit-style solve with relation-balanced preservation constraints included inside the solve, plus periodic batch re-solving for each high-fan-out relation rather than purely one-at-a-time updates ([AlphaEdit](https://arxiv.org/abs/2410.02355), [BetaEdit](https://arxiv.org/abs/2605.09285), [EMMET](https://arxiv.org/html/2403.14236v1), [LocFT-BF](https://arxiv.org/abs/2509.22072)).

The highest-upside frontier prototype is sparse-autoencoder-guided relation/entity disentanglement: use Qwen residual-stream SAE features to identify relation-general directions, then constrain the FFN down-projection update so the edited value component moves entity-specific/value features while minimizing motion along relation-general features for held-out same-relation sentinels; this bridge is not established in the literature, but Qwen-Scope establishes Qwen-family SAE tooling and SAE-guided parameter training, while superposition work explains why non-orthogonal polysemantic features create interference ([Qwen-Scope](https://arxiv.org/abs/2605.11887), [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/), [Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html)).

Parameter-preserving systems such as GRACE-style codebooks, MELO-style routed LoRA banks, and WISE-style side memories are the most robust way to avoid destructive base-weight interference, but they trade away pure parametric recall through routing overhead, prompt-generalization brittleness, and additional CPU memory or compute ([GRACE](https://arxiv.org/abs/2211.11031), [MELO](https://arxiv.org/abs/2312.11795), [WISE](https://arxiv.org/abs/2405.14768)).

## Scope and how to read the evidence

Most editing benchmarks do not directly measure “held-out entities, same relation, never edited” as a first-class metric; KnowEdit includes relation-specific locality, but its main locality construction usually changes the relation for the same subject rather than holding the relation fixed and changing the subject, with reported subject-change proportions of 0.9%, 0.1%, and 0.0% for WikiData_counterfact, WikiData_recent, and ZsRE in a later benchmark analysis ([KnowEdit](https://arxiv.org/abs/2401.01286), [FiNE](https://arxiv.org/abs/2503.01090)).

RippleEdits evaluates broader “ripple effects” and specificity across relations, while MQuAKE evaluates multi-hop propagation after edits; both are important but still do not isolate the user’s observed “many countries share relation = capital” cross-entity relation collision as the core stress test ([RippleEdits](https://arxiv.org/abs/2307.12976), [MQuAKE](https://arxiv.org/abs/2305.14795)).

The recommendations below therefore separate established evidence from extrapolation; “established” means the paper directly measured sequential editing, locality, catastrophic interference, ripple effects, or null-space leakage, while “extrapolation” means the method plausibly applies to cross-entity same-relation isolation but has not published that exact metric ([Model Editing at Scale](https://arxiv.org/abs/2401.07453), [BetaEdit](https://arxiv.org/abs/2605.09285)).

## Ranked shortlist for the exact setup

| Rank | Approach | Mechanism | Interference targeted | Evidence relevant to cross-entity specificity | Applicability to closed-form down_proj editing | Limitation for this failure |
|---:|---|---|---|---|---|---|
| 1 | Leakage-aware AlphaEdit/BetaEdit with relation-balanced in-solve sentinels | Project updates into an approximate null/pseudo-null space, but explicitly compensate for leakage and refresh constraints/history over long streams ([AlphaEdit](https://arxiv.org/abs/2410.02355), [BetaEdit](https://arxiv.org/abs/2605.09285)). | Sequential accumulation, preserved-knowledge drift, pseudo-null leakage ([BetaEdit](https://arxiv.org/abs/2605.09285)). | BetaEdit directly studies Qwen3-4B-Instruct, GPT-J, and LLaMA3 with batch size 1 and layer bands including Qwen3 layers 4-8, and reports that many baselines collapse at 5,000-10,000 edits while BetaEdit remains nonzero and stable on long ZsRE/CounterFact runs ([BetaEdit](https://arxiv.org/abs/2605.09285)). | Closest match to AlphaEdit-style least-squares down_proj editing; can be implemented as an in-solve modification rather than an external retriever ([AlphaEdit](https://arxiv.org/abs/2410.02355), [BetaEdit](https://arxiv.org/abs/2605.09285)). | Published metrics still use generic locality/specificity rather than same-relation held-out entities, so relation-balanced sentinel constraints are an extrapolation ([BetaEdit](https://arxiv.org/abs/2605.09285)). |
| 2 | Periodic batched or breadth-first relation re-solve | Solve many same-relation edits jointly, or periodically re-solve the relation block, to reduce order dependence and overwritten-history artifacts ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [EMMET](https://arxiv.org/html/2403.14236v1), [LocFT-BF](https://arxiv.org/abs/2509.22072)). | Sequential overwrite, conditioning blow-up, edit-order artifacts ([Model Editing at Scale](https://arxiv.org/abs/2401.07453), [LocFT-BF](https://arxiv.org/abs/2509.22072)). | MEMIT demonstrated batch editing up to 10,000 facts, EMMET reports closed-form batch edits on par with MEMIT up to batch size 256 before hard equality constraints destabilize, and LocFT-BF reports breadth-first mini-batch editing scales much better than depth-first sample-wise editing ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [EMMET](https://arxiv.org/html/2403.14236v1), [LocFT-BF](https://arxiv.org/abs/2509.22072)). | Compatible with closed-form editing if treated as a periodic relation-local solve over accumulated keys and protected sentinels ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [EMMET](https://arxiv.org/html/2403.14236v1)). | Batching alone does not fix key collision if all keys share a dominant relation component, and a naive same-relation batch can still move the relation-general direction ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [Efficiently Quantifying and Mitigating the Ripple Effects of Knowledge Editing](https://arxiv.org/abs/2403.07825)). |
| 3 | WISE-style side-memory overlay for high-fan-out relations | Keep the main memory frozen and route edited prompts to a copied side FFN memory with knowledge sharding and learned activation/routing ([WISE](https://arxiv.org/abs/2405.14768)). | Base-weight corruption, long-term sequential edit interference, previous-edit interference ([WISE](https://arxiv.org/abs/2405.14768)). | WISE reports locality of 1.00 across long-sequence ZsRE editing settings on LLaMA-2-7B and Mistral-7B while maintaining much stronger generalization than GRACE in the reported tables ([WISE](https://arxiv.org/abs/2405.14768)). | CPU-deployable as a compact side FFN/adapter overlay for hot relations; keeps the frozen base untouched for unedited facts ([WISE](https://arxiv.org/abs/2405.14768)). | It is no longer a pure single-matrix MEMIT update, and router false positives could still perturb unedited same-relation prompts ([WISE](https://arxiv.org/abs/2405.14768)). |
| 4 | PRUNE + RECT + O-Edit as stabilizers around the solve | PRUNE restrains singular values or condition-number-induced perturbation, RECT suppresses relatively large harmful weight changes, and O-Edit orthogonalizes successive update directions ([PRUNE](http://arxiv.org/pdf/2405.16821.pdf), [RECT](https://arxiv.org/abs/2401.04700), [O-Edit](https://arxiv.org/abs/2410.11469)). | General-ability damage, sequential perturbation growth, successive-update interference ([RECT](https://arxiv.org/abs/2401.04700), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf), [O-Edit](https://arxiv.org/abs/2410.11469)). | RECT evaluates single, sequential, instance, and batch editing across GPT-2 XL, LLaMA-1, and LLaMA-2 on ZsRE, while PRUNE is an ICLR 2025 method focused on bounding perturbation in sequential editing and O-Edit reports an abstract-level 4.2x average improvement for thousands of online edits ([RECT](https://arxiv.org/abs/2401.04700), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf), [O-Edit](https://arxiv.org/abs/2410.11469)). | These methods can be layered into the update as spectral clipping, relative-change masking, or update-direction orthogonalization ([RECT](https://arxiv.org/abs/2401.04700), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf), [O-Edit](https://arxiv.org/abs/2410.11469)). | They do not explicitly protect unedited entities sharing the edited relation, so they should be treated as regularizers rather than the core fix ([RECT](https://arxiv.org/abs/2401.04700), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf), [O-Edit](https://arxiv.org/abs/2410.11469)). |
| 5 | SAE/dictionary-guided relation/entity disentanglement | Identify relation-general and entity/value-specific residual features, then constrain the FFN output update in feature space ([Qwen-Scope](https://arxiv.org/abs/2605.11887), [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/)). | Polysemantic relation/entity entanglement and non-orthogonal feature collisions ([Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html), [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/)). | Qwen-Scope provides Qwen-family SAE tooling and shows SAE-guided supervised fine-tuning can regularize feature activation, but no paper found in this survey directly bridges residual-stream SAEs to closed-form MEMIT down_proj edits ([Qwen-Scope](https://arxiv.org/abs/2605.11887)). | Potentially implementable without full retraining because down_proj output is directly added into the residual stream at the edited layer, making feature-space constraints linearizable ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [Qwen-Scope](https://arxiv.org/abs/2605.11887)). | This is frontier/speculative for MEMIT-class editing and should be validated with a controlled same-relation benchmark before production use ([Qwen-Scope](https://arxiv.org/abs/2605.11887)). |
| 6 | GRACE/MELO-style parameter-preserving or routed adapters | Store edits in codebooks or routed LoRA modules rather than directly changing base FFN weights ([GRACE](https://arxiv.org/abs/2211.11031), [MELO](https://arxiv.org/abs/2312.11795)). | Destructive base-parameter interference and lifelong forgetting ([GRACE](https://arxiv.org/abs/2211.11031), [MELO](https://arxiv.org/abs/2312.11795)). | WISE’s comparisons show GRACE can retain perfect locality but weak generalization under sequential editing, and MELO proposes neuron-indexed dynamic LoRA plus vector routing for lifelong edits ([WISE](https://arxiv.org/abs/2405.14768), [MELO](https://arxiv.org/abs/2312.11795)). | Good safety valve for high-fan-out relations that repeatedly collide under in-weight editing ([GRACE](https://arxiv.org/abs/2211.11031), [MELO](https://arxiv.org/abs/2312.11795)). | Adds retrieval/routing overhead and may violate the pure “parametric recall from the base weights” value proposition ([GRACE](https://arxiv.org/abs/2211.11031), [MELO](https://arxiv.org/abs/2312.11795)). |

## Method-by-method evidence and interpretation

### MEMIT-class locate-and-edit methods

MEMIT formulates FFN layers as linear associative memories where a key vector derived from a prompt maps through an MLP output/down-projection matrix to a value vector representing the target knowledge, and it distributes a closed-form least-squares update across multiple layers to write thousands of facts in bulk ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS)).

MEMIT’s ICLR 2023 evidence is impressive for bulk editing—up to 10,000 facts in GPT-J 6B and GPT-NeoX 20B—but its locality benchmark primarily measures unrelated or neighborhood facts rather than the exact same-relation held-out-entity condition observed in the user’s measurements ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS)).

ROME performs strong single-fact edits but deteriorates at modest batch sizes; MEMIT reports that ROME retains good editing performance at batch size 10 but degrades at 32, while MEND degrades earlier and loses efficacy before 1,000 bulk edits in the same experimental family ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS)).

PMET argues that ROME/MEMIT optimize Transformer-layer hidden states containing MHSA, FFN, and residual information rather than the relevant Transformer-component hidden state, and PMET edits the FFN component more precisely ([PMET](https://arxiv.org/abs/2308.08742)).

On 10,000 CounterFact edits, PMET reports GPT-J score 86.2 with efficacy 99.5, generalization 92.8, specificity 71.4, while MEMIT reports score 85.8 with efficacy 98.9, generalization 88.6, specificity 73.7; this means PMET improves reliability/generalization but does not clearly improve specificity in that table ([PMET](https://arxiv.org/abs/2308.08742)).

For GPT-NeoX, PMET reports score 84.3, efficacy 98.4, generalization 89.4, specificity 70.3, while MEMIT reports score 82.0, efficacy 97.2, generalization 82.2, specificity 70.8, again suggesting that precision in the write target does not automatically solve locality ([PMET](https://arxiv.org/abs/2308.08742)).

EMMET re-derives ROME and MEMIT under a unified preservation-memorization objective and gives an equality-constrained mass-editing solution whose batch performance is on par with MEMIT up to batch size 256 before equality constraints become unstable at larger batch sizes ([EMMET](https://arxiv.org/html/2403.14236v1)).

For the user’s system, PMET and EMMET mainly support the idea that the solve itself should be made more precise and periodically batched, but neither directly protects unedited entities sharing the same relation unless those entities are included as preserved keys or margin constraints ([PMET](https://arxiv.org/abs/2308.08742), [EMMET](https://arxiv.org/html/2403.14236v1)).

### AlphaEdit, BetaEdit, and null-space editing

AlphaEdit adds a null-space projection that aims to restrict weight perturbations to directions that do not affect preserved knowledge, and it reports large gains over locate-and-edit baselines on CounterFact and ZsRE while maintaining general model ability better than prior sequential editing methods ([AlphaEdit](https://arxiv.org/abs/2410.02355)).

AlphaEdit’s theorem is an idealized statement about preserved keys in the null space, while the user’s failure occurs because unedited same-relation entities are not represented in the accumulated preserved-key term and the shared relation direction is plausibly not in the low-singular-value subspace used for protection ([AlphaEdit](https://arxiv.org/abs/2410.02355), [BetaEdit](https://arxiv.org/abs/2605.09285)).

BetaEdit is the most relevant follow-on because it explicitly shows that real covariance matrices are effectively full-rank, so practical “null-space” methods use truncated-SVD pseudo-null spaces where protected keys can leak, and that small leakage accumulates across long edit streams ([BetaEdit](https://arxiv.org/abs/2605.09285)).

BetaEdit’s experiments use Qwen3-4B-Instruct, GPT-J, and LLaMA3-8B-Instruct, include layer bands such as Qwen3 layers 4-8, and evaluate difficult batch-size-1 sequential editing at 300, 5,000, and 10,000 edits ([BetaEdit](https://arxiv.org/abs/2605.09285)).

In the reported tables, many baselines—including FT, RECT, PRUNE, AdaEdit, SimIE, and EMMET in several long-horizon cells—collapse to zero by 5,000 or 10,000 edits, while BetaEdit remains active at 10,000 edits, especially on ZsRE for LLaMA3 where it reports efficacy/generalization/specificity of 96.6/92.4/43.9 at 10,000 edits ([BetaEdit](https://arxiv.org/abs/2605.09285)).

BetaEdit also reports that subject-token anchoring plus history awareness is far more stable than last-token anchoring in long sequential editing, while noting that subject anchoring can struggle for multiple edits on the same subject or complex prompts ([BetaEdit](https://arxiv.org/abs/2605.09285)).

This evidence fits the user’s observation that relation-token anchoring worsens cross-entity bleed and subject-only anchoring causes within-entity multi-field bleed: frequent or shared anchors create collisions, while subject anchors under-represent relation structure and can conflate attributes for the same entity ([BetaEdit](https://arxiv.org/abs/2605.09285), [FiNE](https://arxiv.org/abs/2503.01090)).

### RECT, PRUNE, and O-Edit

RECT studies the observation that model editing can harm general abilities and proposes relative-change regularization on weight updates to reduce disruptive changes while preserving editing performance across single, sequential, instance, and batch editing settings ([RECT](https://arxiv.org/abs/2401.04700)).

PRUNE, published as an ICLR 2025 conference paper in the available record, frames sequential-edit failure as perturbation growth and applies an upper-bound restraint via singular-value or condition-number control to preserve general ability while maintaining edit performance ([PRUNE](http://arxiv.org/pdf/2405.16821.pdf)).

O-Edit proposes orthogonal subspace editing for sequential editing, where each knowledge update direction is orthogonalized to reduce interference with previous updates, and its abstract reports online editing across thousands of edits with a 4.2x average improvement over existing methods ([O-Edit](https://arxiv.org/abs/2410.11469)).

The interpretation for this failure is narrow: these methods can reduce accumulated perturbation, but none of the available evidence shows explicit protection of never-edited entities sharing the same relation after 50-100 same-relation edits ([RECT](https://arxiv.org/abs/2401.04700), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf), [O-Edit](https://arxiv.org/abs/2410.11469)).

O-Edit should be treated as especially early-stage for this report because the accessible evidence in this survey was abstract-level rather than full-table verification ([O-Edit](https://arxiv.org/abs/2410.11469)).

### WISE, GRACE, MELO, and parameter-preserving hybrids

GRACE introduces discrete key-value adaptors for lifelong model editing, storing edit behavior outside the base weight update pathway and thereby reducing destructive interference with original parameters ([GRACE](https://arxiv.org/abs/2211.11031)).

WISE argues that long-term parameter editing conflicts with pretrained or previous knowledge, while pure working-memory retrieval often has weak generalization, and it proposes a dual parametric memory with a frozen main memory, copied side memory, routing, and knowledge sharding ([WISE](https://arxiv.org/abs/2405.14768)).

WISE reports locality of 1.00 across long sequential ZsRE settings on LLaMA-2-7B and Mistral-7B, and the same tables show GRACE retaining locality but losing much more generalization than WISE as edit counts grow ([WISE](https://arxiv.org/abs/2405.14768)).

MELO uses neuron-indexed dynamic LoRA plus vector-database routing to assign edits to LoRA blocks and avoid overwriting, with the explicit goal of lifelong editing through dynamically allocated parameter overlays ([MELO](https://arxiv.org/abs/2312.11795)).

For this failure, a WISE-like high-fan-out-relation side memory is the best hybrid: low-fan-out facts can remain in BetaEdit/AlphaEdit in-weight storage, while high-fan-out relations such as capitals can route to a compact relation-specific side FFN, LoRA bank, or codebook that leaves base same-relation knowledge untouched ([WISE](https://arxiv.org/abs/2405.14768), [MELO](https://arxiv.org/abs/2312.11795)).

The cost is that CPU inference must now execute routing and sometimes side modules, and generalized paraphrase robustness depends on the router rather than purely on the transformed base model ([WISE](https://arxiv.org/abs/2405.14768), [GRACE](https://arxiv.org/abs/2211.11031), [MELO](https://arxiv.org/abs/2312.11795)).

### DAFNet, MALMEN, and other lifelong-editing methods

DAFNet proposes a Dynamic Auxiliary Fusion Network that aggregates intra-editing token-level attention flow and inter-editing sequence-level attention flow to reduce forgetting in sequential editing, and it introduces DAFSet over ZSRE, CounterFact, and RIPE ([DAFNet](https://arxiv.org/abs/2405.20588)).

DAFNet is relevant because it targets sequential forgetting and includes relation-specific evaluation through RIPE-style probes, but it is an auxiliary-network method rather than a closed-form FFN down-projection edit and therefore is less directly deployable in the user’s CPU overlay architecture ([DAFNet](https://arxiv.org/abs/2405.20588)).

MALMEN formulates massive editing with a hypernetwork and an efficient parameter-shift aggregation equation, reporting edits up to thousands of facts on BERT, GPT-2, T5-XL, and GPT-J across FEVER and ZsRE ([MALMEN](https://arxiv.org/abs/2311.04661)).

MALMEN is relevant as evidence that aggregation and batch structure matter, but it requires a trained editor/hypernetwork and is therefore less aligned with the user’s closed-form no-retraining constraint ([MALMEN](https://arxiv.org/abs/2311.04661)).

UltraEdit claims training-free, subject-free, memory-free lifelong editing with normalization-based feature statistics and reports scaling to 20,000 samples in minutes on 7B models in the available paper listing, but the evidence here should be treated as preliminary because this survey only verified listing-level details rather than full-table results ([UltraEdit listing](https://huggingface.co/papers/2505.14679)).

### FiNE and DiKE: precise localization and disentanglement

FiNE argues that causal tracing can locate knowledge too coarsely and subject-sensitively, then selects fine-grained neurons relevant to the specific knowledge to improve locality on KnowEdit-style evaluations ([FiNE](https://arxiv.org/abs/2503.01090)).

FiNE is relevant because it attacks over-editing from coarse localization, but its benchmark discussion emphasizes relation changes for the same subject more than same-relation held-out subjects ([FiNE](https://arxiv.org/abs/2503.01090)).

DiKE introduces a knowledge-representation disentanglement module that decomposes subject representations into target-related and unrelated components, then edits the target-related component while preserving unrelated knowledge ([DiKE](https://arxiv.org/abs/2505.18774)).

DiKE’s FINE-KED benchmark is complementary to the user’s failure because it focuses on fine-grained irrelevant knowledge for the same subject across relations, and its subject-consistent batch editing experiments show that disentanglement can preserve relational locality where ROME degrades and MEMIT/AlphaEdit remain imperfect ([DiKE](https://arxiv.org/abs/2505.18774)).

The design lesson is strong even though the axis differs: the next generation of same-relation cross-entity editing should disentangle relation-shared and entity-specific components before solving the weight update, rather than relying on a single prompt-position key ([DiKE](https://arxiv.org/abs/2505.18774), [FiNE](https://arxiv.org/abs/2503.01090)).

## Mechanism and theory

### Why same-relation cross-entity bleed occurs

In MEMIT-class editing, a layer’s down-projection weight matrix behaves like a linear associative memory, so an edit adds a matrix perturbation that maps selected edit keys toward desired values while attempting to preserve other key mappings ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS)).

For an unedited held-out key \(k_h\), the first-order output change is \(\Delta W k_h\), so the held-out entity is safe only if its key is nearly orthogonal to the update’s effective key span or is explicitly included in the preservation term ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [EMMET](https://arxiv.org/html/2403.14236v1)).

When many facts share a relation, the keys can decompose roughly as \(k_{e,r} = k_e + k_r + \epsilon\), so all same-relation keys have a shared component \(k_r\), and repeated updates for different entities accumulate a nonzero projection along the shared relation subspace ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [Efficiently Quantifying and Mitigating the Ripple Effects of Knowledge Editing](https://arxiv.org/abs/2403.07825)).

The graph-based ripple-effect study supports this mechanism because it finds that editing preferentially impacts facts with embeddings similar to edited facts and that hidden-space effects can reach seemingly unrelated entities, which is exactly the kind of similarity-mediated spillover expected when same-relation keys overlap ([Efficiently Quantifying and Mitigating the Ripple Effects of Knowledge Editing](https://arxiv.org/abs/2403.07825)).

The large-scale sequential-editing study supports the same interpretation because it finds that ROME and MEMIT can enter progressive forgetting followed by abrupt catastrophic failure, and it describes new edits bleeding into other facts stored in the model even when methods were thought to be localized ([Model Editing at Scale](https://arxiv.org/abs/2401.07453)).

### Relation direction, high variance, and null-space protection

The user’s high-variance-shared-relation hypothesis is consistent with the AlphaEdit/BetaEdit line: AlphaEdit protects low-singular-value pseudo-null directions, while BetaEdit shows that practical null-space protection is approximate and can leak because the empirical covariance is full-rank and truncated SVD leaves \(P K_0 \neq 0\) ([AlphaEdit](https://arxiv.org/abs/2410.02355), [BetaEdit](https://arxiv.org/abs/2605.09285)).

If a relation-general direction is high variance, it will not be among the low-singular-value directions retained as editable null space, so a projection built to protect low-energy directions will not automatically preserve high-energy same-relation structure unless same-relation sentinels are explicitly represented in the preservation objective ([AlphaEdit](https://arxiv.org/abs/2410.02355), [BetaEdit](https://arxiv.org/abs/2605.09285)).

This also explains why accumulated cache_c or preserved-key terms can fix same-entity sequential accumulation while missing held-out cross-entity damage: the preserved set is sparse over edited facts, not a covering set over the relation manifold ([AlphaEdit](https://arxiv.org/abs/2410.02355), [BetaEdit](https://arxiv.org/abs/2605.09285)).

Post-hoc projection onto other entities’ keys is inherently limited if the solve already moved a high-variance shared relation feature and if the protected set only samples that relation manifold sparsely; BetaEdit’s leakage analysis implies that protection must be refreshed and accounted for during the solve rather than appended after the update ([BetaEdit](https://arxiv.org/abs/2605.09285)).

### Superposition and polysemanticity

Toy Models of Superposition formalizes how neural networks can represent more features than dimensions by storing features in non-orthogonal directions, with interference governed by feature sparsity and importance ([Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html)).

Scaling Monosemanticity shows that sparse autoencoders can recover interpretable features from large models and discusses feature specificity and interference between non-orthogonal features, which supports the idea that relation and entity features may share a polysemantic basis in dense residual/MLP activations ([Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/)).

The extrapolation to knowledge editing is that a high-fan-out relation such as “capital of” may occupy a broad, high-importance, shared feature direction, so edits that appear entity-specific at the prompt level can still perturb a relation-level feature used by many entities ([Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html), [Efficiently Quantifying and Mitigating the Ripple Effects of Knowledge Editing](https://arxiv.org/abs/2403.07825)).

This extrapolation is not yet a theorem for MEMIT/AlphaEdit, but it is mechanically compatible with the observed monotonic held-out degradation and with published evidence that editing effects follow hidden-space similarity ([Efficiently Quantifying and Mitigating the Ripple Effects of Knowledge Editing](https://arxiv.org/abs/2403.07825), [BetaEdit](https://arxiv.org/abs/2605.09285)).

### Is there an established capacity ceiling?

No paper found in this survey proves a universal edits-per-relation capacity ceiling for in-weight editing before same-relation specificity collapses, and the published ceiling evidence is empirical and method/model/benchmark dependent ([Model Editing at Scale](https://arxiv.org/abs/2401.07453), [BetaEdit](https://arxiv.org/abs/2605.09285), [LocFT-BF](https://arxiv.org/abs/2509.22072)).

Empirically, ROME and MEMIT can degrade after surprisingly few sequential edits, with large-scale sequential editing reporting degradation beginning as low as about 10 edits and later progressing toward catastrophic failures in some runs ([Model Editing at Scale](https://arxiv.org/abs/2401.07453)).

Empirically, MEMIT-style bulk editing can store 10,000 facts under standard CounterFact/ZsRE metrics, while BetaEdit can keep long sequential editing active at 10,000 edits where many baselines collapse, showing that total edit count alone is not the limiting variable ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [BetaEdit](https://arxiv.org/abs/2605.09285)).

The practical ceiling should be modeled as a function of key overlap, relation fan-out, condition number of the edit-key matrix, magnitude of value residuals, preservation-set coverage, layer bandwidth, and pseudo-null leakage, rather than simply as \(N\) total edits ([EMMET](https://arxiv.org/html/2403.14236v1), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf), [BetaEdit](https://arxiv.org/abs/2605.09285)).

For the user’s measured degradation at 26, 50, and 100 same-relation edits, the literature supports calling this a relation-conditioned capacity limit of the current keying/projection scheme, not a general model-capability collapse ([Model Editing at Scale](https://arxiv.org/abs/2401.07453), [Efficiently Quantifying and Mitigating the Ripple Effects of Knowledge Editing](https://arxiv.org/abs/2403.07825), [BetaEdit](https://arxiv.org/abs/2605.09285)).

## Batch versus sequential writing

Sequential one-at-a-time editing is more vulnerable to order effects because each new update is computed against a model already perturbed by earlier writes, and large-scale sequential editing finds progressive forgetting and abrupt failures for methods that look localized in one-shot or small-batch settings ([Model Editing at Scale](https://arxiv.org/abs/2401.07453)).

Batch writing can reduce overwriting because the solver sees all target constraints simultaneously, which is one reason MEMIT was designed for mass editing and EMMET gives a closed-form equality-constrained mass editing formulation ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [EMMET](https://arxiv.org/html/2403.14236v1)).

Batching is not guaranteed to improve same-relation specificity because a same-relation batch can make the edit-key matrix more rank-deficient or ill-conditioned when the shared relation component dominates entity-specific components ([EMMET](https://arxiv.org/html/2403.14236v1), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf)).

LocFT-BF provides useful evidence from fine-tuning-based editing: depth-first sample-wise editing over-optimizes each shard and induces interference, while breadth-first mini-batch editing improves shards jointly and scales much better on large edit sets, including Qwen2.5-7B-Instruct in the model suite ([LocFT-BF](https://arxiv.org/abs/2509.22072)).

The recommended implementation is therefore “relation-batched, preservation-aware, and periodically refreshed,” not merely “write all same-relation facts at once”; the batch solve should include edited facts, previously edited facts, and held-out same-relation sentinel keys with constraints that preserve their pre-edit logits or top-1 margin ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [EMMET](https://arxiv.org/html/2403.14236v1), [BetaEdit](https://arxiv.org/abs/2605.09285)).

## Parameter-preserving versus parameter-modifying tradeoff for this failure

Parameter-preserving methods categorically avoid destructive interference in the base weights only if their router never fires on unedited facts and never misses edited paraphrases, which is a behavioral condition rather than a mathematical guarantee ([GRACE](https://arxiv.org/abs/2211.11031), [WISE](https://arxiv.org/abs/2405.14768)).

GRACE-style codebooks and retrieval-style adapters preserve base predictions for out-of-scope inputs, but WISE’s reported comparisons show GRACE can maintain locality while losing generalization under sequential editing, especially as edit counts grow ([GRACE](https://arxiv.org/abs/2211.11031), [WISE](https://arxiv.org/abs/2405.14768)).

WISE improves that tradeoff by making the side memory parametric and routing paraphrased edit prompts to the side memory, while keeping unrelated prompts in the frozen main memory ([WISE](https://arxiv.org/abs/2405.14768)).

MELO offers another hybrid by allocating neuron-indexed LoRA modules and using a vector database to route edits, which can avoid overwriting but adds routing state and adapter execution to inference ([MELO](https://arxiv.org/abs/2312.11795)).

For CPU-served Qwen-family dense models, the pragmatic hybrid is to keep the default path as a quantized frozen base plus compact down_proj overlays, then use a small WISE/MELO-style side overlay only for relations whose measured cross-entity specificity falls below threshold after a small number of writes ([WISE](https://arxiv.org/abs/2405.14768), [MELO](https://arxiv.org/abs/2312.11795), [BetaEdit](https://arxiv.org/abs/2605.09285)).

## Highest-upside novel directions to prototype

### 1. Relation-balanced BetaEdit: same-relation sentinels inside the solve

The first prototype should extend AlphaEdit/BetaEdit by adding a per-relation sentinel set of unedited entities to the preservation objective before solving, not after solving, because BetaEdit shows pseudo-null leakage accumulates and post-hoc correction is structurally late ([AlphaEdit](https://arxiv.org/abs/2410.02355), [BetaEdit](https://arxiv.org/abs/2605.09285)).

For each hot relation \(r\), maintain three key sets: edited keys \(K_E(r)\), previously edited preserved keys \(K_P(r)\), and unedited same-relation sentinel keys \(K_S(r)\), with sentinel constraints preserving either the layer value vector, final-answer logit margin, or a linearized proxy for the pre-edit answer ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [EMMET](https://arxiv.org/html/2403.14236v1), [BetaEdit](https://arxiv.org/abs/2605.09285)).

The solve should penalize \(\|\Delta W K_S(r)\|\) or preserve \(W K_S(r)\), while separately optimizing edited residuals for \(K_E(r)\); this directly targets the user’s held-out same-relation top-1 degradation rather than generic neighborhood specificity ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [Efficiently Quantifying and Mitigating the Ripple Effects of Knowledge Editing](https://arxiv.org/abs/2403.07825)).

The sentinel set should be relation-balanced rather than random because the published ripple-effect work shows that similarity in embedding/hidden space predicts which facts are affected, and same-relation facts are high-risk even when globally unrelated facts remain stable ([Efficiently Quantifying and Mitigating the Ripple Effects of Knowledge Editing](https://arxiv.org/abs/2403.07825)).

The main risk is capacity: if the relation-shared direction is the only available path for representing the edit in early layers 4-8, the constrained solve may lower edit efficacy or require shifting the edit band later, increasing layer count, or moving high-fan-out relations to side memory ([AlphaEdit](https://arxiv.org/abs/2410.02355), [WISE](https://arxiv.org/abs/2405.14768)).

### 2. SAE-guided entity/relation feature constraints

Qwen-Scope provides Qwen-family sparse-autoencoder resources and demonstrates SAE-guided feature regularization in supervised fine-tuning, which makes it the closest starting point for Qwen2.5/Qwen3 interpretability-guided editing even though it is not a MEMIT editing paper ([Qwen-Scope](https://arxiv.org/abs/2605.11887)).

The bridge is technically plausible because the FFN down_proj output is added into the residual stream at the edited layer, while residual-stream SAEs expose a decoder basis in that same representational space ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [Qwen-Scope](https://arxiv.org/abs/2605.11887)).

A concrete formulation is to identify SAE features activated by relation prompts across many entities, identify entity/value features activated by individual triples, and solve for \(\Delta W\) under a feature penalty that minimizes movement along relation-general decoder directions for held-out sentinels while allowing movement toward value-specific decoder directions for edited facts ([Qwen-Scope](https://arxiv.org/abs/2605.11887), [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/)).

This approach directly attacks the hypothesized superposition problem because sparse coding tries to separate non-orthogonal polysemantic features into a more monosemantic basis, and superposition theory predicts interference when dense features are packed into shared dimensions ([Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html), [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/)).

No surveyed paper directly demonstrates residual-SAE-constrained closed-form down_proj editing, so this is a frontier idea rather than established SOTA ([Qwen-Scope](https://arxiv.org/abs/2605.11887)).

### 3. High-fan-out relation routing: in-weight by default, side memory only when needed

A hybrid architecture should classify relations by measured interference slope and route only high-fan-out/high-collision relations to a side-memory overlay, while keeping low-fan-out facts in the fast AlphaEdit/BetaEdit in-weight path ([WISE](https://arxiv.org/abs/2405.14768), [BetaEdit](https://arxiv.org/abs/2605.09285)).

WISE is the best starting design because it keeps the main memory frozen and uses side memory plus routing to preserve locality, while MELO provides an alternative dynamic-LoRA allocation pattern that may be lighter for CPU deployment if the LoRA banks are quantized and relation-scoped ([WISE](https://arxiv.org/abs/2405.14768), [MELO](https://arxiv.org/abs/2312.11795)).

The router should be relation-and-entity aware rather than relation-token-only, because BetaEdit’s anchoring results show frequent/shared tokens can become interference hubs and the user has already observed relation-inclusive keying worsening cross-entity bleed ([BetaEdit](https://arxiv.org/abs/2605.09285)).

This is the most robust production fallback if the in-weight relation-balanced solve hits an empirical capacity limit at hundreds or thousands of facts for the same relation ([Model Editing at Scale](https://arxiv.org/abs/2401.07453), [WISE](https://arxiv.org/abs/2405.14768)).

## Specific implementation recommendations

### Edit-band and keying recommendations

The early layer band 4-8 matches BetaEdit’s Qwen3 experimental layer range, so it is defensible for Qwen-family testing, but the user should also evaluate one later band because WISE’s ablations indicate early/final layers can behave poorly for side-memory routing and because lower layers may encode shared syntax/relation structure more than entity-specific factual binding ([BetaEdit](https://arxiv.org/abs/2605.09285), [WISE](https://arxiv.org/abs/2405.14768)).

Do not return to pure subject-keyed or pure relation-token-keyed editing; BetaEdit’s anchor analysis supports the intuition that overly frequent or poorly scoped tokens can induce interference, while FiNE and DiKE support finer localization/disentanglement rather than a single coarse prompt position ([BetaEdit](https://arxiv.org/abs/2605.09285), [FiNE](https://arxiv.org/abs/2503.01090), [DiKE](https://arxiv.org/abs/2505.18774)).

Use entity-relation residualized keys: compute the relation centroid over many entity prompts, subtract or orthogonalize the relation-general component for the write address, and separately constrain the relation-general component through sentinels; this design is an extrapolation from similarity-mediated ripple effects and disentangled same-subject editing, not a published standard method ([Efficiently Quantifying and Mitigating the Ripple Effects of Knowledge Editing](https://arxiv.org/abs/2403.07825), [DiKE](https://arxiv.org/abs/2505.18774)).

### Evaluation harness recommendations

Add a benchmark split with edited entities, held-out same-relation entities, same-entity other relations, random unrelated entities, and global capability probes, because existing benchmarks often conflate these locality axes ([KnowEdit](https://arxiv.org/abs/2401.01286), [RippleEdits](https://arxiv.org/abs/2307.12976), [FiNE](https://arxiv.org/abs/2503.01090)).

Track top-1 correctness, gold-logit margin, KL divergence from the pre-edit distribution on held-out same-relation prompts, and activation drift projected onto relation-centroid/SAE features, because top-1 accuracy may remain stable until margins collapse and then flip abruptly ([Model Editing at Scale](https://arxiv.org/abs/2401.07453), [BetaEdit](https://arxiv.org/abs/2605.09285), [Qwen-Scope](https://arxiv.org/abs/2605.11887)).

Run both sequential and periodic-batch modes at N = 10, 25, 50, 100, 250, 500, and 1,000 same-relation edits, because the user’s measured degradation begins before 100 edits and published sequential failures can begin surprisingly early even when global metrics remain acceptable ([Model Editing at Scale](https://arxiv.org/abs/2401.07453)).

Measure per-relation condition number and key-cosine concentration before writing, because EMMET and PRUNE both indicate that solve conditioning and perturbation bounds matter for mass editing stability ([EMMET](https://arxiv.org/html/2403.14236v1), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf)).

## Comparative answer to the five research questions

### 1. SOTA for cross-entity specificity under mass and sequential editing

No surveyed method can be called established SOTA specifically for “unedited held-out entities sharing the edited relation” because benchmarks generally measure generic locality, relation changes for the same subject, multi-hop ripple correctness, or unrelated neighborhood specificity ([KnowEdit](https://arxiv.org/abs/2401.01286), [RippleEdits](https://arxiv.org/abs/2307.12976), [FiNE](https://arxiv.org/abs/2503.01090)).

For closed-form parameter-modifying editing, BetaEdit is the closest SOTA because it directly targets null-space leakage and long sequential editing on Qwen3/GPT-J/LLaMA3 with batch size 1, while AlphaEdit is the prior null-space baseline and MEMIT/EMMET/PMET define the mass-editing backbone ([BetaEdit](https://arxiv.org/abs/2605.09285), [AlphaEdit](https://arxiv.org/abs/2410.02355), [MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [EMMET](https://arxiv.org/html/2403.14236v1), [PMET](https://arxiv.org/abs/2308.08742)).

For locality-first production safety, WISE is the strongest hybrid because it reports perfect locality in long sequential settings while improving generalization over GRACE, but it adds side memory and routing ([WISE](https://arxiv.org/abs/2405.14768), [GRACE](https://arxiv.org/abs/2211.11031)).

RECT, PRUNE, O-Edit, DAFNet, MALMEN, MELO, FiNE, and DiKE are useful components or analogues, but each misses at least one of the user’s hard constraints: pure closed-form down_proj editing, explicit same-relation held-out isolation, no auxiliary training, or CPU-minimal inference ([RECT](https://arxiv.org/abs/2401.04700), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf), [O-Edit](https://arxiv.org/abs/2410.11469), [DAFNet](https://arxiv.org/abs/2405.20588), [MALMEN](https://arxiv.org/abs/2311.04661), [MELO](https://arxiv.org/abs/2312.11795), [FiNE](https://arxiv.org/abs/2503.01090), [DiKE](https://arxiv.org/abs/2505.18774)).

### 2. Mechanism and theory

Locate-and-edit methods bleed when the update matrix has nonzero action on unedited keys, and same-relation facts are high-risk because their keys are likely similar in hidden space and may share a high-variance relation component ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [Efficiently Quantifying and Mitigating the Ripple Effects of Knowledge Editing](https://arxiv.org/abs/2403.07825)).

The high-variance-shared-direction hypothesis is strongly consistent with AlphaEdit/BetaEdit because low-singular-value null-space protection does not naturally preserve high-variance shared relation directions and because approximate null-space leakage accumulates over time ([AlphaEdit](https://arxiv.org/abs/2410.02355), [BetaEdit](https://arxiv.org/abs/2605.09285)).

Superposition theory makes the hypothesis more plausible by showing that features can be represented in non-orthogonal directions and that interference is expected when many features share a limited representational basis ([Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html), [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/)).

No established theorem gives a universal edits-per-relation ceiling, but empirical work supports practical ceilings driven by key overlap, conditioning, leakage, and edit-order accumulation ([Model Editing at Scale](https://arxiv.org/abs/2401.07453), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf), [BetaEdit](https://arxiv.org/abs/2605.09285)).

### 3. Frontier directions

SAE-guided editing is the most novel direction because it could turn “relation direction” from an implicit covariance artifact into an explicit feature basis, but no surveyed paper has yet shown residual-SAE constraints integrated into a MEMIT/AlphaEdit closed-form down_proj solve ([Qwen-Scope](https://arxiv.org/abs/2605.11887), [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/)).

Entity-disentangled key construction is the second frontier, with DiKE showing that representation disentanglement can improve fine-grained same-subject locality and with FiNE showing that coarse localization is a source of over-editing ([DiKE](https://arxiv.org/abs/2505.18774), [FiNE](https://arxiv.org/abs/2503.01090)).

Hybrid high-fan-out relation routing is the most production-practical frontier because WISE and MELO already define side-memory and routed-adapter patterns that can be reserved for relations empirically shown to exceed in-weight capacity ([WISE](https://arxiv.org/abs/2405.14768), [MELO](https://arxiv.org/abs/2312.11795)).

MoE-routing-aware editing is lower priority for the user’s current dense Qwen target, but the same principle would apply to Qwen-MoE-style systems by constraining edits within the expert and router paths used by the edited relation/entity cluster rather than the global dense FFN ([WISE](https://arxiv.org/abs/2405.14768), [Qwen-Scope](https://arxiv.org/abs/2605.11887)).

### 4. Batch versus sequential

Sequential editing worsens cross-entity interference when each edit adds a new perturbation without jointly reconsidering the geometry of all same-relation keys, and published sequential-editing studies show progressive forgetting and catastrophic failures under repeated edits ([Model Editing at Scale](https://arxiv.org/abs/2401.07453), [BetaEdit](https://arxiv.org/abs/2605.09285)).

Batch editing can mitigate overwriting by solving constraints jointly, but it can worsen or expose collision if the same-relation key matrix is ill-conditioned and dominated by a shared relation component ([MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS), [EMMET](https://arxiv.org/html/2403.14236v1), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf)).

The best compromise is periodic breadth-first relation batching with explicit same-relation preservation, echoing LocFT-BF’s finding that breadth-first mini-batch editing avoids depth-first interference and EMMET’s finding that equality-constrained mass editing is stable only up to moderate batch sizes ([LocFT-BF](https://arxiv.org/abs/2509.22072), [EMMET](https://arxiv.org/html/2403.14236v1)).

### 5. Parameter-preserving versus parameter-modifying

Parameter-preserving methods avoid weight-space ripple effects in the base model, but they introduce router and generalization errors that are absent from a pure down_proj overlay ([GRACE](https://arxiv.org/abs/2211.11031), [WISE](https://arxiv.org/abs/2405.14768), [MELO](https://arxiv.org/abs/2312.11795)).

For this failure, hybrids are preferable to pure retrieval because the system can preserve parametric CPU recall for most facts while reserving side memory for high-fan-out relations whose empirical interference slope is steep ([WISE](https://arxiv.org/abs/2405.14768), [BetaEdit](https://arxiv.org/abs/2605.09285)).

## Open research questions

The field lacks a benchmark that directly varies edits-per-relation while holding entity distribution, relation frequency, and held-out same-relation entities fixed, so the user’s measured curve is more targeted than most public metrics ([KnowEdit](https://arxiv.org/abs/2401.01286), [RippleEdits](https://arxiv.org/abs/2307.12976), [Model Editing at Scale](https://arxiv.org/abs/2401.07453)).

The field lacks a formal capacity law for in-weight editing as a function of relation fan-out, key overlap, model width, edit-layer band, and preservation-set coverage, even though empirical work shows these variables matter ([EMMET](https://arxiv.org/html/2403.14236v1), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf), [BetaEdit](https://arxiv.org/abs/2605.09285)).

The field lacks a published bridge from residual-stream SAE features to closed-form MLP down-projection weight edits, despite the fact that Qwen-Scope now makes Qwen-family SAE tooling available and MEMIT-class edits act directly on residual-stream contributions through down_proj outputs ([Qwen-Scope](https://arxiv.org/abs/2605.11887), [MEMIT](https://openreview.net/forum?id=MkbcAHIYgyS)).

The field lacks an explicit comparison of same-relation sequential versus same-relation batched editing for capitals/presidents/currencies-style relations under CPU-scale dense models such as Qwen2.5-3B, Qwen3-1.7B, and Qwen3-8B ([BetaEdit](https://arxiv.org/abs/2605.09285), [LocFT-BF](https://arxiv.org/abs/2509.22072)).

The field lacks a robust routing theory for hybrid parameter-preserving systems that guarantees high edit generalization without false-positive activation on unedited same-relation facts ([GRACE](https://arxiv.org/abs/2211.11031), [WISE](https://arxiv.org/abs/2405.14768), [MELO](https://arxiv.org/abs/2312.11795)).

## Bottom-line recommendation

The next engineering iteration should implement a same-relation stress benchmark first, then compare four interventions: current AlphaEdit, BetaEdit-style leakage-aware history refresh, relation-balanced in-solve sentinels, and periodic relation-batched re-solving with PRUNE-style spectral/condition restraint ([AlphaEdit](https://arxiv.org/abs/2410.02355), [BetaEdit](https://arxiv.org/abs/2605.09285), [PRUNE](http://arxiv.org/pdf/2405.16821.pdf), [EMMET](https://arxiv.org/html/2403.14236v1)).

If held-out same-relation top-1 still collapses before the desired edit count, the system should route only that high-fan-out relation to a compact WISE/MELO-style side overlay while leaving the rest of the knowledge database in-weight ([WISE](https://arxiv.org/abs/2405.14768), [MELO](https://arxiv.org/abs/2312.11795)).

In parallel, the most valuable research prototype is the SAE-guided solve because it is the only surveyed direction that directly aims to turn the vague “shared relation direction” into an explicit constrained feature basis, although it remains speculative until validated on a same-relation held-out benchmark ([Qwen-Scope](https://arxiv.org/abs/2605.11887), [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/), [Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html)).
