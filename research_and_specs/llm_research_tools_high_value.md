# High-Value Repositories for the LLM-as-Database Program

A content-based triage of the [130-repo catalog](./llm_research_tools_repos.md): every repository's **actual README, file tree, and code** was read (not its description or star count) and judged against this program's open research needs — parametric knowledge editing, cross-entity interference, quantization survival, CPU deployment, and the in-weight-vs-retrieval question.

**Headline finding:** **none** of the 130 repos is a direct knowledge-editing project (no MEMIT / ROME / AlphaEdit / GRACE implementations). The genuine value is in **adjacent** research — weight-space structure, calibration/beliefs, catastrophic forgetting, quantization×margin, superposition/SAE, and GraphRAG-vs-RAG — several of which map cleanly onto specific entries in `docs/HYPOTHESIS_REGISTER_2026-06-18.md`. Stars were ignored; every Tier-1/2 pick was verified by reading its code.

---

## Tier 1 — Highest value (read and use)

| Repo | Maps to our | Why it's valuable (verified content) |
|---|---|---|
| [skgallagher/ELLMTrees-paper](https://github.com/skgallagher/ELLMTrees-paper) | **C2 / D2** (where facts live, key collinearity) | Replication package showing fine-tuning lineage is recoverable from **weight-space distance**, with the discriminative signal **concentrated in attention KEY matrices (~4% of params)** — whitebox + blackbox evidence and a falsifiable within-task null. **[Verified 2026-06-19 — see `external_evidence_notes.md` EV-1: DOWNGRADED.** Its "key matrices" are attention W_k (fine-tuning lineage), NOT our down_proj keys — a naming collision, not corroboration of C2; its RF/phylogeny method may still help D2.]** |
| [cscheffler/elicit-model-beliefs](https://github.com/cscheffler/elicit-model-beliefs) | **E2 / margin confound** | Real experiment measuring **belief *stability*** (SD of p(yes) across paraphrases) vs model size/family across open weights **including Qwen2.5** — notebooks + figures. A ready method for our "stored vs barely-expressed / robust-under-paraphrase" question and the `compute_z` margin confound. |
| [vivsn289/Adaptive-Self-rehearsal](https://github.com/vivsn289/Adaptive-Self-rehearsal) | **F2 (temporal durability) / D1** | Catastrophic-forgetting experiment on **Qwen2.5-3B** (our exact model): vanilla vs probe-monitored adaptive rehearsal SFT, **3 seeds, lm-eval harness, paired SE-flagged comparisons**, saved results. Direct reference for "does drift accumulate across successive rebuilds" and rigorous within-unit comparison. |
| [tanueihorng/llm-ethics-benchmark](https://github.com/tanueihorng/llm-ethics-benchmark) | **B3 (quant survival) / margin** | Despite the name, a research-grade **quantization study**: matched **fp16 → INT8 → NF4** pairs across 10 models, a **refusal_margin** module, and a reproducibility/cluster kit. A second, independent take on the exact B3 question (does behavior survive quantization, measured by margins). |
| [luisroberto0/project-hebb](https://github.com/luisroberto0/project-hebb) | **F2 / methodology / CPU deploy** | Rigorous multi-milestone continual-learning / plasticity / forgetting study with **seeds + CI95, adversarial peer review, honest negative findings, and CPU-latency/SynOps deployment analysis**. Both a continual-learning data point and an exemplar of the falsification discipline we hold ourselves to. |

## Tier 2 — Situational / strong reference

| Repo | Maps to our | What's in it |
|---|---|---|
| [Melodiz/llm-research-projects](https://github.com/Melodiz/llm-research-projects) | **A6 (SAE/superposition), C2** | Toy-model **superposition geometry** + **SAE feature-recovery with known ground truth**, carry/arithmetic circuits, logit-lens — code + results. Closest thing to our cross-entity-interference geometry. |
| [ADEL9st/LLM-Mind-Visualizer](https://github.com/ADEL9st/LLM-Mind-Visualizer) | **A6 / D2** | Working interpretability tooling: per-layer residual-stream activations, **logit-lens**, attention-head maps, **direction ablation**, with **GGUF/Ollama** adapters. Adaptable for "where does the edited fact live." |
| [sasakimc/semantic-resilience-project](https://github.com/sasakimc/semantic-resilience-project) | **C2 / D2** | Representation-collapse experiments (stance-drift on Qwen2.5, embedding/stance metrics, judge rubric, run-schema). Low-dim "semantic mode" framing relevant to interference geometry. |
| [Pra0809/xai-knowledge-graph](https://github.com/Pra0809/xai-knowledge-graph) | **B2/B3 (L2-necessity)** | Complete **GraphRAG-vs-RAG** study over 3,907 papers (Neo4j, PyKEEN, reported MRR/Hits/win-rate). Concrete evidence for the "is in-weight storage needed vs retrieval + external query index" decision. |
| [Anandesh-Sharma/awesome-agentic-memory](https://github.com/Anandesh-Sharma/awesome-agentic-memory) | **B2/B3, F2** | Curated map of agentic-memory frameworks, KG/temporal memory, lifelong-learning papers, memory benchmarks — literature surface for the retrieval-vs-weights and continual axes. |
| [Pankick/llm-research](https://github.com/Pankick/llm-research) | **E2** | Confidence-vs-correctness on **Qwen2.5** (per-step softmax, **AUROC/ECE**, full next-token distribution). Calibration probing on our model family. |
| [whenpoem/aiscientist](https://github.com/whenpoem/aiscientist) | **methodology** | Mature reproducibility harness: **preregistration, multiple-comparison correction, seed-repro checks, verifier-blocks-unverified-claims** (729 tests). Mirrors our pre-registration + inertness-gate discipline. |
| [Zhonghao1995/research-skills](https://github.com/Zhonghao1995/research-skills) | **methodology / E2** | 35 tested agent skills incl. model-calibration, uncertainty, reproducibility, experiment-audit, rag-memory — reusable harness pieces. |
| [WhaSukGO/LenaLab](https://github.com/WhaSukGO/LenaLab) | **methodology** | Generator⟂verifier harness with **held-out splits and honest negatives/retractions** — a clean falsifiable-eval-gate template (vision domain). |
| [going-doer/paper2code](https://github.com/going-doer/paper2code) | **tooling** | ICLR-2026 PaperCoder: multi-agent **paper→code** + Paper2Code/PaperBench datasets. Could accelerate reimplementing editing-method papers (e.g. the parked BetaEdit port). |
| [ruimalheiro/gradient-garden](https://github.com/ruimalheiro/gradient-garden) · [ServiceNow/Fast-LLM](https://github.com/ServiceNow/Fast-LLM) | **infra** | Real training/eval engines (DDP/FSDP2, SFT/DPO/distillation, eval registries). Relevant only if the program does in-the-loop weight updates at scale. |
| [priyamDalmia/hpc-for-ml-researchers](https://github.com/priyamDalmia/hpc-for-ml-researchers) | **methodology** | Reproducible-by-default PBS/Slurm job templates for large-scale ML experiments. |
| [tmgthb/Autonomous-Agents](https://github.com/tmgthb/Autonomous-Agents) | **discovery** | Large daily-updated index of agent/LLM papers — a feed to surface editing/interp/eval work as it appears. |

---

## The rest (~110 repos) — low or no value, and why

The long tail was read and ruled out by content, not dismissed by metadata. The recurring non-value patterns:

- **arXiv-summarizer / paper-digest apps & scrapers** (the largest group): `researchflow-ai`, `arxiv-llm-analyzer`, `AI-Research-Paper-Analyzer`, `Auto-Research-Paper-Scraper`, `daily-research-paper`, `llmpapers`, `ur-ai-papers`, etc. — off-the-shelf RAG plumbing, no method or finding.
- **Personal portfolios / blogs / profile READMEs / landing pages**: `*.github.io`, `*.com`, `genai-architect-portfolio`, `portfolio_deploy`, `Greninja110`, etc.
- **Download-bait `.exe`/`.zip` wrappers** (treat with caution): `ai-papers-hub`, `papers_skills`, `awesome-ai-extensions`, `research-skills-guide`, `grounded-research`, `clashroy5384/*` — no inspectable code.
- **Empty / placeholder / manifesto repos**: `LamTong21/*`, `yvonneandraivanciu/*`, `suhteevah/*`, `obone215/Atlas`, `gnwb199-oss/staged-ai-architecture`.
- **Off-domain applications**: finance (`Multi-market-data`, `competitor-research`), healthcare (`Aghefendi/LLM`, `PathoSummarize_AI`), sales/OSINT (`prospect-intel-agent`, `OpenOSINT`), red-team/safety (`llm-redteam-*`).
- **Generic agent / harness frameworks** with no editing or fact-eval content: `autonomous-engine`, `ResearchHarness`, `wpawgasa/ai-agent-llms`, `wanshuiyin/Auto-claude-code-research-in-sleep`.

---

### Method note
Each repo's README + file tree (and key source files where promising) were read via the GitHub API by parallel reviewers, each briefed on the program's eight open needs (editing methods, mechanistic interp, editing eval, RAG/memory/KG, quant/deploy, continual/capacity, calibration, methodology). Tiers reflect verified substance and direct mapping to our open hypotheses, explicitly **independent of stars/popularity**. Full data: [`llm_research_tools_repos_data.json`](./llm_research_tools_repos_data.json).

## Tooling — autonomous research loops & skill libraries (search, not evidence)

Out-of-catalog tools the operator surfaced; folded here as **methodology tooling**. ⚠️ **These OPTIMIZE (hill-climb a metric); our program FALSIFIES.** Use them only for **search / hypothesis-generation** over config-space sub-problems — and re-verify any winner with pre-registered criteria + the engine inertness gate + `advisor()`. A loop winner is a *lead*, never a `CORPUS/` result (Goodhart).

| Repo | Use | Note |
|---|---|---|
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch) (87.6k★) | Reference architecture | The canonical autonomous propose→experiment→evaluate→keep/revert loop. As-is it optimizes nanochat `val_bpb` (not our science) — reuse the *pattern*, not the repo. |
| [wjgoarxiv/autoresearch-skill](https://github.com/wjgoarxiv/autoresearch-skill) (18★) | **Installed & wired** | Generalized loop as a Codex/Claude skill (→ `~/.codex/skills/autoresearch-skill`, source in `tools/`). Wired to a first search: `experiments/track_c/autoresearch_band_search/` (band-[8-12] cross-entity isolation, honest exact-match evaluator + retention/expression guard). |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) (9.8k★) | Skill source | 98-skill AI-research-engineering library (Mech Interp ×4, Evaluation ×3, Post-Training ×8) to browse for Codex skills. General scaffolding, not editing-specific. |
| [firecrawl/AI-research-SKILLs](https://github.com/firecrawl/AI-research-SKILLs) (10★) | Skip | Redundant smaller copy of the Orchestra library. |
