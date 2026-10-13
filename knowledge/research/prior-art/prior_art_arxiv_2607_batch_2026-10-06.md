# Prior art: four operator-supplied arXiv 2607.* papers (2026-10-06)

Read-only review. Nothing was run, installed or executed. Verdict summary at the end.

## How this was read (verification note)

- Full text of all four papers was read through the arXiv MCP HTML endpoint (`download_paper` + `read_paper` chunks) and abstracts through `get_abstract`. Submission timestamps below come from `get_abstract` `published`.
- First-pass `WebFetch` summaries of the same pages were inconsistent between calls and in places wrong. Example: for Metis, two WebFetch calls returned three different versions of Table 5. Everything below that carries a table/section citation was checked against the MCP full text. WebFetch-only claims are used only where labeled "WebFetch only".
- Not read: appendices of Metis (2607.26760 App. B, C, D, F, G), Memory Decoder appendices (2607.27919 App. C onward), MemTxn Figures (charts have no extractable numbers), MemHarness appendix after A.2. Anything that would live there is UNVERIFIED.
- Metis judge-model name (Section 6.1 / App. F.3) was not re-read: UNVERIFIED.

---

## 1. arXiv 2607.26760v2 — Metis: Memory Foundation Model

### 1. What it is
- Authors: Zeyu Zhang, Ziliang Guo, Yihang Sun, Xichong Zhang, Xixuan Hao, Zehao Lin, Yang Zhang, Xiaoyan Zhao, Tong Shen, Bo Tang, Zhi-Qin John Xu, Junchi Yan, Haofen Wang, Xu Chen, Feiyu Xiong, Zhiyu Li, Tat-Seng Chua (MemTensor and university affiliations; 2607.26760 front matter). First submitted 2026-07-29 (get_abstract); this is v2. Venue: arXiv preprint (cs.CL, cs.LG); no venue stated.
- Method in plain terms: Metis adds "Metis blocks" to a Qwen3.5 backbone (Qwen3.5-4B/9B/27B rows in Table 5). Each block holds a matrix-valued memory state (fast-weight style, Section 1 and 3). Text the model reads is compressed into that state by a forward pass only; later queries attend to it through "memory attention". Backbone weights stay frozen at inference; the state is the "dynamic parameter" (Abstract; Section 1). The block parameters and procedures are learned by mid-training (Sections 4-5; training details taken from WebFetch only: 8x H100, 14,000 steps for 27B: UNVERIFIED).
- This is not an edit of MLP weights. Nothing is solved in closed form per fact; the "write" is a learned compression, and it is per-session state, not persistent weights.
- Code: https://github.com/MemTensor/Metis and weights at https://huggingface.co/collections/IAAR-Shanghai/metis (2607.26760 front matter). Repo page (WebFetch only, not independently verified): inference, training and eval code present, noncommercial licence, "Training data is not included". Reproducing the training is therefore not possible from the repo; evaluating released checkpoints may be (UNVERIFIED on MPS).

### 2. Evidence
Measured results (all "No Context" = the original text is not shown at query time):
- Task definitions (Section 4.1 per WebFetch, definitions not re-read in MCP text, so WebFetch only): Remember, Update, Forget (revoke a stated fact), Reflect (multi-hop over two stored facts).
- Table 5 (Section 6.2), no-context rows, avg over the four operations:
  - MemOps (Gold): Metis-4B 17.84, Metis-9B 19.63, Metis-27B 24.76. Qwen3.5-27B 1.69. Temp-LoRA-27B 9.70. Delta-Mem 4.38.
  - Metis Test Set: Metis-4B 56.72, Metis-9B 57.92, Metis-27B 73.77. Qwen3.5-27B 16.87. Temp-LoRA-27B 23.86.
  - Metis-27B per-operation, MemOps (Gold): Remember 28.27, Update 31.02, Forget 10.91, Reflect 26.55. Metis Test Set: 61.08 / 68.13 / 77.50 / 93.44.
  - Full-context Qwen3.5-27B reference: MemOps (Gold) avg 87.90; Metis Test Set avg 78.87.
  - Caveat on the Forget column: the no-context Qwen3.5 baseline scores 47.50 on Metis Test Set Forget (Table 5), because a model with no information trivially "does not know" the revoked fact. Forget scores are not comparable to Remember scores.
- Text claim (Section 6.2): "forgetting is still the most difficult operation on the external MemOps (Gold) benchmark, even for Metis-27B" and removing information in a shared latent state is harder to generalize than storing or updating. This matches Table 5 (10.91 vs 28.27 and 31.02).
- Table 6 (memory QA, no context): Metis-27B LoCoMo (Gold) avg 26.74, NextMem avg 50.82; Qwen3.5-27B 0.07 and 17.75.
- Ablation, Metis-4B (Table 7, Section 6.3): removing adaptive aggregation drops overall avg 33.14 to 12.93 (-60.98%); removing query-key normalization 33.14 to 23.72 (-28.44%); removing the multi-fact + memory-pollution auxiliary data 33.14 to 26.74 (-19.31%). Authors attribute QKN effect to "irrelevant information may introduce stronger interference" (prose, not separately measured).
- OOD (Table 8, Section 6.4): ATM-Bench Gold avg Metis-27B 18.56 vs Temp-LoRA-27B 2.57; MemDaily avg Metis-27B 59.04 vs Temp-LoRA-27B 59.45 (Metis does not lead, text says "mixed").
- Capacity (Section 6.6, Figure 3, numbers are in a plot, not in text, so no values cited): 20 fictional users x 40 persona facts, Metis-4B vs Qwen3.5-4B full context. Prose: step-level accuracy "decreases rapidly as the input becomes longer"; trajectory-level "the accuracy of the first fact decreases almost continuously, showing that early information is gradually weakened by later updates"; "new updates introduce interference throughout the whole memory state rather than only overwriting the oldest information". Queries are one direct question per domain reused across users (Section 6.6) — no paraphrased questions.
- General capability (Table 10, Section 6.7), Metis-4B minus Qwen3.5-4B: initial stage MMLU-Pro -0.80, IFEval +0.55, GSM8K -1.06, MMMLU -0.80. After irrelevant messages are stored (active stage): MMLU-Pro -5.10, IFEval -22.18, GSM8K -5.61, MMMLU -3.30.
- Low-rank study (Table 11, Section 6.8): overall score is 99.9% of full at rank 64 of 1024.
- Source exclusion (Table 9, Section 6.5): removing LoCoMo/LongMemEval-derived training data (about 2.61% of instances) lowers the 6-benchmark average by 1.66, 0.76, 2.69 points for 4B/9B/27B.
Claims in prose only: "native memory offers advantages in architecture, end-to-end optimization, and efficiency" (Abstract); gradient-free update (Abstract, consistent with design).
Not measured: paraphrase transfer of a stored fact; coined/invented-name values (entities come from public datasets and synthetic personas, Section 4 per WebFetch only; capacity study uses fictional users in Section 6.6); any weight-edit baseline (the baselines are Temp-LoRA and Delta-Mem, Table 5).

### 3. Relevance
- (a) Paraphrase transfer: none tested. Queries are fixed direct questions (Section 6.6). Takeaway: nothing here bears on the 7/72 versus held-out paraphrase gap. Supports/contradicts the three loop candidates: neither.
- (b) Interference between written facts: measured as a trend, not a number. Section 6.6 says later updates degrade earlier and middle facts "throughout the whole memory state". Table 7 shows that removing query-key normalization costs 28.44% overall, which the authors read as interference control. Takeaway for the program: the same pattern (older records weakened by later writes) is a prediction worth a counter-check in a sequential-write run of the weight route (write N records in order, read all after each batch). Direction-compatible with the loop's candidate 1 (leakage between records when one value starts with another record's subject name), but a different mechanism (shared recurrent state vs shared MLP weights), so it does not support or contradict it.
- (c) Locality / collateral damage: Table 10 gives a clean analog: general capability is nearly intact with an empty state and falls with accumulated irrelevant memory (IFEval -22.18 at the active stage). Takeaway: report locality as a function of how many records are already stored, not only after one write. The loop's candidate 2 failed a locality check and candidate 3 passed with a stronger KL penalty; Metis gives no evidence on that trade-off.
- (d) Lifecycle: the only one of the four with Update and Forget measured inside the model. Takeaways: (1) Forget is the weakest operation on the harder benchmark (Table 5, 10.91). (2) Scoring a delete needs a control where the no-information baseline is scored too, since Table 5 shows 47.50 for a model that never saw the fact. Testable for the program: when deletes are tested, report value-absent rate with a never-written control arm in the same table. No support or contradiction for the loop candidates.
- (e): not applicable.

### 4. Verdict: CONTEXT (with FALLBACK note)
Reason: a trained memory-state architecture (mid-training on about 406M-token synthetic data per WebFetch only), the state is per-session activations, not writes into the model's MLP weights, so it is outside the write-only route. Keep on file as a non-write-path comparator because it has public checkpoints and the only Update/Forget numbers of the batch. No paraphrase or invented-name test exists to import.

---

## 2. arXiv 2607.27919v1 — Memory Decoder at Scale: A Pretrained, Parametric Long-Term Memory

### 1. What it is
- Authors: Rubin Wei, Jiaqi Cao, Jiarui Wang, Junming Zhang, Qipeng Guo, Bowen Zhou, Zhouhan Lin. Submitted 2026-07-30 (get_abstract). arXiv preprint, cs.CL; no venue stated.
- Method in plain terms: train a separate transformer decoder (the "memory", 1.4B to 6.9B for general, 1.7B for domain) to imitate, from the context alone, the next-token distribution that a kNN lookup over a frozen backbone's hidden states would give. The kNN datastore exists only offline to build training targets ("Retrieval is used only to construct offline supervision for memory pretraining", Section 2). Loss = beta * KL(p_ret || p_mem) + (1 - beta) * LM loss (Eq. 1; memory loss weight 0.5 in Table 9). At inference the frozen backbone and the memory both read the same context and their distributions are mixed: p_final = (1 - alpha) p_backbone + alpha p_memory (Eq. 2), alpha tuned on validation data (Section 4).
- Code: https://github.com/LUMIA-Group/MemoryDecoder-at-Scale (front matter), HF collection https://huggingface.co/collections/Rubin-Wei/memorydecoder-at-scale. Repo page (WebFetch only, not independently verified): Apache-2.0, training/inference/eval scripts, checkpoints. Training needs 64 to 256 GPUs for the general memories (Table 9, 256 A800 in Section 4), so only evaluating released checkpoints is plausible locally (UNVERIFIED on MPS).

### Disposition check (the program asked for this)
Prior label (`hypotheses.md:177`, `dispositions.md:28`): `fallback`, described as "a pool/lookup design where recall goes through a separate module, not the model's own weights".
- Holds: it is a separate module with its own weights, attached to a frozen backbone; the base model's weights are never written (Section 4: "the base model remains frozen"; Section 7: memories "attached to frozen backbones... without modifying the base model"). It is not a write into the model's weights, so it cannot be the write-only route. `fallback` stands.
- Needs rewording: it is not a pool or a lookup at inference. Section 7: "The resulting memory requires neither external memory construction nor online retrieval at inference time." Section 9: "inference requires no external retrieval". The lookup step happens only offline to make training targets. The accurate class is "separate pretrained parametric module, mixed by output interpolation", closer to a distilled kNN-LM than to a record pool.
- New fact: adding or changing one fact means building new kNN targets and retraining or adapting the module (Section 3.3 describes domain memory as continued pretraining of a datastore model, then kNN construction, then memory training). I found no incremental write, update or delete procedure in Sections 1-9 (Section 9 mentions only offline preprocessing cost and fixed alpha). Appendices not read: UNVERIFIED there.

### 2. Evidence
Measured:
- General memory (Table 1, Section 5.1; Pythia backbones, 17 benchmarks): AVG 32.76 to 34.36 (+1.60) at 1.4B, 33.89 to 35.49 (+1.60) at 2.8B, 36.30 to 37.79 (+1.49) at 6.9B; frozen Pythia-12B 37.24. Pythia-410M + 6.9B memory 29.86 to 37.34 (Abstract; Section 5.2).
- Knowledge columns of Table 1: PopQA 10.65 to 11.90 (1.4B), 11.45 to 12.83 (2.8B), 14.00 to 15.13 (6.9B); NQ-Open 2.80 to 3.88, 3.82 to 5.15, 4.68 to 6.32; TriviaQA 8.30 to 17.11 at 2.8B and 22.21 to 25.58 at 6.9B.
- Collateral check: TruthfulQA moves 30.63 to 30.46, 28.47 to 27.92, 28.49 to 27.81 (Table 1); the other tasks mostly rise. Locality is by construction because the backbone is frozen.
- Domain memory (Table 2, Section 5.3, Qwen3 Base backbones, zero-shot on BioInst / LawBench / FinEval): average gains +9.88 (0.6B), +9.64 (1.7B), +10.00 (4B), +9.09 (8B), +9.99 (14B). Qwen3-1.7B-Base BioInst 5.39 base, 9.01 LoRA, 8.07 RAG, 4.84 CPT, 23.21 memory. Memory domain training data and evaluation benchmark are the same dataset family (BioInst: train on Biology-Instructions text, evaluate on its benchmark; Section 4); whether the evaluated items are held out from the training split is not stated in Section 4 (UNVERIFIED).
- Same-size attached module control (Table 5, Section 6.5): BioInst, 1.7B backbone: None 5.39, attached CPT 13.00, attached memory 23.21; 8B backbone: 4.82 / 11.31 / 20.02. LawBench 1.7B: 26.86 / 29.10 / 30.78; 8B: 32.67 / 37.98 / 41.91. Matched data, FLOPs, capacity and interface. The authors attribute the gap to the KL-to-retrieval-distribution objective (prose, Section 6.5); it is a control for the interface but not an ablation of KL weight beta.
- Extractable memorization (Table 6, Section 6.6): 1,024 BioInst training prompts; verbatim EM@8,16 42.4% (CPT) vs 49.7% (memory); domain anchor completion 22.6% vs 56.5%. Prompts are training-set prefixes, not paraphrases.
- Fidelity (Table 7, Section 6.7): top-token match 86.62%, mean KL 0.1820, mean TV 0.0823, Pearson r 0.9174 over 1,024 samples.
- Transfer across vocabularies (Table 3, Section 5.4): OLMo-2-7B 19.57 to 23.83, OLMo-3-7B 18.67 to 26.44 with memory at 20% training budget; CPT leads on BioInst for both backbones (Table 3).
Prose-only claims: "memory provides stronger traceability to its training data" (Section 6.6); "independently scaling pretrained memory offers a more parameter efficient path" (Abstract).
Not measured: paraphrase transfer of single facts; interference between facts; update or delete; invented entities. Section 9 (limitations) lists none of these either.

### 3. Relevance
- (a) Paraphrase transfer: indirect. The only evidence on soft versus hard targets is Table 5: fitting a module to a soft distribution built from many neighbor contexts (Section 2: kNN "offers richer supervision by capturing the diversity of plausible continuations") beats hard-label CPT of the same size on benchmark questions (BioInst 23.21 vs 13.00 at 1.7B backbone). Question format versus training format is not shown, so this is not a paraphrase result. Testable idea within the write-only route: the loop's candidate 2 (one target vector fit jointly over three phrasings, 26/72) is the weight-edit analog of "supervise on many contexts, not one". Treat this paper as a mild directional reason to keep going from 3 phrasings toward more phrasings in the target fit; it does not support candidate 3's stronger KL penalty, because the KL here is a distillation target (beta = 0.5, Table 9), not a leash toward the unedited model.
- (b) Interference: none measured. Not applicable beyond "frozen backbone, so no interference with the backbone by construction". No bearing on candidate 1.
- (c) Locality: by construction (frozen backbone). Table 1 TruthfulQA small declines are the only collateral signal. Contradicts nothing in the loop.
- (d) Lifecycle: not addressed (Section 9). Shows what a non-write route costs: any new fact needs target construction and training (Section 3.3).
- (e): the scaling and cross-backbone-transfer results (Figure 1, Section 5.2) are not relevant to the blocker.

### 4. Verdict: FALLBACK (disposition holds, wording corrected)
Reason: a separate trained module mixed at the output, not a write into the model's weights; no update/delete/paraphrase evidence. Keep as the "distilled datastore" fallback class; replace "pool/lookup" with "separate parametric module, interpolated output" in `dispositions.md`/`hypotheses.md` when next edited.

---

## 3. arXiv 2607.28272v1 — MemHarness: Memory Is Reconstructed, Not Replayed

### 1. What it is
- Authors: Rong Wu, Daocheng Fu, Licheng Wen, Xuemeng Yang, Shu Zou, Jianbiao Mei, Yuxin Wang, Hairong Zhang, Yu Yang, Tao Hu, Cong Zhang, Botian Shi, Pinlong Cai. Submitted 2026-07-30 (get_abstract); the paper's own date field reads August 24, 2026. arXiv preprint, cs.AI.
- Method in plain terms: an agent keeps a text memory bank of strategies plus the source observation each came from (Section 3.1). At each step it retrieves the top-3 entries (BGE-M3, Section 4.1), then the same policy model rewrites ("reconstructs") or rejects the retrieved entry against the current state, then acts. Trained end-to-end with GRPO on Qwen2.5-7B-Instruct after a short supervised cold start (Section 4.1).
- Code: https://github.com/KnowledgeXLab/MemHarness (front matter). Repo page (WebFetch only): verl-agent based training scripts, Apache-2.0, checkpoints on HF.

### 2. Evidence
Measured (all on ALFWorld and WebShop, Qwen2.5-7B-Instruct backbone):
- Table 1: ALFWorld avg success rate 85.2 and WebShop success 75.6 for MemHarness; GRPO alone 76.4 and 66.1; Mem0+GRPO 52.0 and 37.5; SimpleMem+GRPO 54.5 and 46.9; EvolveR (reproduced) 70.1 and 72.6; base Qwen2.5-7B-Instruct 14.5 and 7.8.
- Table 2 ablations (ALFWorld / WebShop): RL + raw memory 70.1 / 72.6; without reconstruction 79.6 / 74.6; without memory at test time 83.0 / 73.6; generic-LLM reconstruction 77.7 / 71.8.
- Table 3 (ALFWorld OOD): MemHarness 85.9; without reconstruction 82.4; without memory 83.0; RL + raw memory 76.3.
- Table 4: removing the source observation lowers ALFWorld success 85.2 to 80.0; 1,000 counterfactual probes shift ALFWorld reject rate 0.6% to 6.4% and WebShop 72.1% to 78.8% (Table 4b).
Prose claims: "this reconstruction objective serves as latent guidance during training" is inferred from the w/o-memory result in Table 2 (83.0 vs 76.4); no direct test.
Not measured: weights, facts, paraphrase, update, delete, locality. The paper states no limitations section (its conclusion lists only scaling as future work, Section 5).

### 3. Relevance
- (a) none. The memories are agent strategies, not facts about named entities.
- (b) Weak analog only: verbatim replay of stored records in a mismatched state hurts (Table 2: RL + raw memory 70.1 vs RL alone 76.4). The read-time analog of the loop's candidate 1 (a stored value contaminating an unrelated read) would be a check that a read for fact A never returns fact B's value, which the program already measures; the paper adds no method for the weight route.
- (c) none (no weights edited).
- (d) A bank that prunes low-utility entries and deduplicates semantically (Section 3.1, following EvolveR per the text) is a lifecycle in an external store, not a write path.
- (e) Nothing for this program otherwise.

### 4. Verdict: NOT RELEVANT
Reason: retrieved text rewritten by an RL-trained policy on game benchmarks; no facts, no weight writes, no paraphrase or locality measurement.

---

## 4. arXiv 2607.27834v1 — MemTxn: A Transaction Boundary for Source-Supported Updates and Complete-State Recovery in Agent Memory

### 1. What it is
- Authors: Hanshuai Cui, Zhiqing Tang, Zhi Yao, Fanshuai Meng, Qianli Ma, Weijia Jia (Beijing Normal University, Zhuhai). Submitted 2026-07-30 (get_abstract). arXiv preprint, cs.AI / cs.CL.
- Method in plain terms: a governance layer outside the answering model, on a SQLite store (Section "Method", system model; Related Work states "MemTxn leaves model weights unchanged"). Three pieces: (1) Ordered PatchTest admits a write only if the cited evidence span is a substring of the source and every value token appears in that span in source order (Eq. 1); (2) a Temporal Resolver picks the chronology-latest version when two sources conflict (Eq. 2); (3) a snapshot journal persists the "application-visible active map" before a transaction and restores it after a fault without knowing which physical keys were touched (Eq. 3; SQLite WAL, synchronous=FULL).
- Code: no link found anywhere in the text read (UNVERIFIED that none exists; the WebFetch also found none). Results are not reproducible from a repo.

### 2. Evidence
Measured:
- Source-support audit (Table 1, Section "Source-Support Admission"): 60 supported and 179 hard-negative probes from 12 unseen LongMemEval-S test items. Ordered PatchTest 100.00 accuracy, 0 false accepts, 0 false rejects. Lexical gate at theta 0.60: accuracy 25.10, 179 false accepts. Calibrated (theta 0.95): 73.22, 64 FA. Qwen judge: 68.62, 72 FA, 3 FR. Hybrid: 78.24, 49 FA, 3 FR. The negatives are template-generated (negation insertion, reordering, substitution) and the test is a lexical-order rule: the authors scope it to "the declared ordered lexical-support contract" and say it "does not establish semantic-role fidelity or truth".
- FactConsolidation (Table 2, Section "Temporal Resolution", MemoryAgentBench, 800 questions per model): F1 for Qwen2.5-7B Dense 20.89, MemTxn 42.88 (+21.99); Qwen3.5-9B 21.38 vs 45.45 (+24.07); GPT-5.4 32.25 vs 49.31 (+17.06). Conditional stale rate for Qwen2.5-7B 49.50 (Dense) vs 15.11 (MemTxn). Matched top-8 control (Table 3): pooled +19.51 F1, 95% CI [18.38, 20.63] over 4,800 pairs.
- Complete-state recovery (Table 4, Section "Complete-State Recovery"): hardest setting 64 active and 16 affected keys; MemTxn and a write-set oracle 0 failures over 272 runs; single-key baseline fails all 136 partial-commit and event-divergence runs. Fault classes are not named in the text I read (UNVERIFIED which four).
- Gate-reliability stress (Table 5): accuracy 100.00 at gate reliability 100%, 62.47 at 50%; unsafe-write rate 0.00 to 16.40.
Prose: stated limits are "not semantic truth or robustness to concurrent or repeated faults, intent corruption, or physical loss" and "coverage under naturally occurring update triggers remains outside the controlled evaluation" (Discussion and Limitations).
Not measured: anything involving model weights, paraphrase of a stored fact, or locality of a parametric write. The paper cites ROME, MEMIT, AlphaEdit and WISE only as "modify parametric knowledge" (Related Work).

### 3. Relevance
- (a) none: retrieval-based store; no paraphrase experiments.
- (b) Version conflict is addressed outside the model by chronology (Eq. 2). Takeaway for the program: the "stale rate" metric (rate at which the old version is returned after an update, Table 2) is a ready-made definition for the update tests of written facts; use "old value read after update" as a column beside "new value read". No effect on the loop's candidate 1.
- (c) none for weights. The "unsafe write rate" of Table 5 is write-admission, not collateral damage.
- (d) Lifecycle (the useful part). Three concrete, write-path-independent items: (1) a pre-write admission rule (cited span must contain the value tokens in order) is cheap to apply to the program's invented-name records before any weight write, as a source-of-truth check on the record, not a model-side test; (2) complete-state recovery as a test design: after rollback of an edit or a delete, compare the full readout of all stored records and a weight/readout hash against the pre-transaction snapshot, not just the target key, because Table 4 shows single-key undo fails 136/136 partial-commit runs in the database setting; (3) append-only versions with parent pointers and recorded decisions so that every admission "can be replayed without evaluator data" (Method, "Source-supported update admission"), an audit-trail design for the program's tracking layer. Whether a closed-form MEMIT edit can be rolled back exactly (inverse delta on the same covariance state) is a program-side question this paper cannot answer.
- (e): the benchmark gains over Dense/Mem0/Zep are retrieval results, irrelevant here.

### 4. Verdict: CONTEXT
Reason: an external governance and audit design, strong on lifecycle test shapes (stale rate, complete-state rollback, replayable admission) but entirely outside the weights; useful as a checklist for the program's update/delete/audit tests, with no bearing on the paraphrase blocker.

---

## Summary table

| id | title | verdict | one-line why |
|---|---|---|---|
| 2607.26760 | Metis: Memory Foundation Model | CONTEXT (FALLBACK note) | per-session fast-weight state learned by mid-training; Table 5 gives Update/Forget numbers (Forget 10.91 on MemOps Gold) and Table 10 shows locality loss as memory fills; no paraphrase test, not a weight write |
| 2607.27919 | Memory Decoder at Scale | FALLBACK (disposition holds, "pool/lookup" wording wrong) | separate trained module mixed at output (Eq. 2), no lookup at inference, frozen backbone; Table 5 soft-target control (23.21 vs CPT 13.00) is the only hint, and it is not a paraphrase test |
| 2607.28272 | MemHarness | NOT RELEVANT | RL-tuned text rewriting of retrieved agent strategies on ALFWorld/WebShop; no facts, no weights |
| 2607.27834 | MemTxn | CONTEXT | external SQLite governance; stale-rate metric, complete-state rollback test and replayable admission are reusable lifecycle test designs |

## Single test to pre-register first
No paper is a LEAD, so no new within-route test is warranted by this batch. The nearest actionable item, if the operator wants one lifecycle test queued rather than a mechanism test: a MemTxn-style complete-state rollback check on the existing write harness. Write N records, snapshot all-record readouts, apply and then delete/roll back k records, and pass only if the readouts of all N records (not only the k) equal the snapshot. This is lifecycle (d), not the C10 blocker, and it is not a LEAD from these papers because MemTxn never touches weights.
