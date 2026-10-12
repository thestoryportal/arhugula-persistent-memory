## §4 — KNOWLEDGE BASE INDEX (research docs + spec map)
═══════════════════════════════════════════════════════════════════════
_Cite the relevant entry in every experiment block. Consult before framing decisions (§2.2)._

### §4.1 — Research documentation
| Doc | Holds | Consult for |
|---|---|---|
| `research_and_specs/cross_entity_research_synthesis.md` | **The reconciliation** of all 3 research artifacts vs our evidence; candidate ranking; BetaEdit finding; OQ-W1 "wrong variable" | Start here for the blocker's solution space |
| `research_and_specs/llm_editing_survey.md` | Perplexity Deep Research: ranked methods (BetaEdit#1, batch, WISE, RECT/PRUNE/O-Edit, SAE, GRACE), mechanism, capacity-ceiling, batch-vs-seq, eval harness | External SOTA per method; arXiv IDs |
| `research_and_specs/notebooklm_10_prompt_research_corpus-{1,2}.md` | Corpus-grounded: MEMIT's own P127/P641 specificity collapse, LARQL "balancer/hijacking", λ tradeoff, our spec's OQ-W1/GAP-1/Genesis/C2/C4, WISE/ELDER/MELO | What our corpus + spec already say |
| `research_and_specs/perplexity_prompt_*.md`, `notebooklm_prompts_*.md` | The research prompts (reusable templates) | Running further external research |
| `s240_literature_scan.md` | Earlier scan: Ripple Effect naming, BLUE (boundary-layer), GRACE/BalancEdit, GIE/SIR, locality-eval critique, RippleEdits/MQuAKE/KnowEdit benchmarks | Prior-art mechanism clues |
| `framework_finding_v1_10_additive.md` (+ v1_7..v1_9) | Our own findings: calibrated metric, H-MODEL (Qwen-local/GPT-J-not), sequential fail, Rung-1/3/AlphaEdit ladder | Historical decision rationale |
| `write_engine_viability_determination_report.md` | The same-entity multi-field VALIDATED determination (now scoped by G6.1) | The proven foundation + its scope |
| `CORPUS/00`,`03`,`13`, `LARQL_INTEGRATION_ASSESSMENT.md` | Master evidence ledger, status ledger, G6.1 writeup, the bridge | Authoritative evidence + status |

### §4.2 — Spec section map (cite these)
- **§7.3 Relation Families / §7.5 Polysemantic Discipline** — the schema-level locality rules; relevant to cross-entity (relation fan-out) and disambiguation.
- **§7.7 Project Genesis (D9/D10)** — the batched foundational write (→ A1 batch relevance; Genesis = single atomic 2PC across L1–L4).
- **§8.1–8.2 Write Engine / MEMIT designated (C15 band, D12 method-class, D20 orthogonal-projection mandate)** — the core write contract; C15 = L15–25/32L (our [4-8] divergence → A4).
- **GAP-1 / OQ-W1 (§22 protocol; numeric outputs implementation-phase)** — "cumulative edit-volume degradation threshold (model-specific)," deferred pending "target-model selection + write-volume stress test." **G6.1 + Track D resolve this.**
- **C2 (entity names compositionally unambiguous) / C4 (untyped entities = violation)** — schema disambiguation; does NOT cover relation-level fan-out (gap).
- **§9 (validation pipeline), §10.2 (Gate checks), §11.13 (ledger), §46 (2PC ordering), §20.3 (ceremony)** — governance (CP1–G3 done).
> ⚠️ **VERIFY-BEFORE-CITING:** §7.3/7.5/7.7/8.2 + C15/D12 were grep-confirmed against the spec text this session — trust them. But **C2, C4, §46, §20.3, §11.13, D20, OQ-W2** were surfaced via the NotebookLM reading / prior memory, NOT a direct read of the spec text. Per [[read-authoritative-source-fully]], **re-read the spec § before F1 builds the readiness verdict on any of these** — do not let a NotebookLM paraphrase become a load-bearing citation.

═══════════════════════════════════════════════════════════════════════
