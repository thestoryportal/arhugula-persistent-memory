# InfraNodus gap audit — plan (prepared 2026-10-04 night; runs once the `infranodus` MCP server is attached)

**Purpose.** After five prior-art passes (~90 papers read, 88 Connected Papers graphs / 2,123 nodes indexed) and nine C10 experiments, the risk is the one re-reading cannot catch: topics each argued to exhaustion and never connected. The audit asks the graphs where the corpus's clusters fail to touch, then resolves or logs every gap. Method and vocabulary: `~/.claude/skills/infranodus-gap-audit/` (`references/method.md`, `tool-calls.md`, `report.md`). This is a knowledge-base audit, not a science result: it writes no CORPUS entry and changes no tracker; findings become pre-registration inputs.

## Prerequisite (operator)
`claude mcp add --transport http --scope user infranodus https://mcp.infranodus.com --header "Authorization: Bearer <key>"` (header name per the InfraNodus API page), then start a fresh session. Tools expected: `mcp__infranodus__create_knowledge_graph`, `difference_between_texts`, `merged_graph_from_texts`, `develop_latent_topics`, `develop_conceptual_bridges`, `generate_research_questions`.

## Sources (segmented, one statement per line; `results/infranodus_audit_2026-10-04/segments/`)

| graph name | file | statements | role in the method |
|---|---|---|---|
| `llmdb-prior-art-A-20261004` | `prior_art_items_A.txt` | 89 | substantive: sweep §1–§7 (22-paper sweep, addenda 1–4) |
| `llmdb-prior-art-B-20261004` | `prior_art_items_B.txt` | 93 | substantive: sweep §8–§13 (keyword passes 1–5, candidate-solution maps, claim check) |
| `llmdb-c10-knobs-20261004` | `c10_evidence_knobs.txt` | 138 | evidence: CORPUS/35–39 (value-class wall, knob sweeps) |
| `llmdb-c10-anyedit-keying-20261004` | `c10_evidence_anyedit_keying.txt` | 113 | evidence: CORPUS/40–43 (AnyEdit pilot, Stage 0, Route A, keying ablation) |
| `llmdb-decision-log-20261004` | `decision_log_master_evidence.txt` | 161 | decision log: CORPUS/00 |
| `llmdb-cold-reader-20261004` | `cold_reader_bootstrap_state.txt` | 72 | **cold-reader doc (target of the difference call)**: SESSION_BOOTSTRAP + generated program-state block |
| `llmdb-spec-e2e-20261004` | `constraints_spec_e2e.txt` | 64 | constraints from outside: spec end-to-end ground truth |
| `llmdb-f1-20261004` | `f1_determination.txt` | 69 | the determination and its conditions register |

Excluded on purpose: the Connected Papers index (generated, title-only; would inflate dominant nodes), the runbook body (duplicates the decision log), the prereg/result docs for individual experiments (restated in CORPUS). Read `segments/*.txt` before graphing; tables flattened by the segmenter read poorly and may be restated as prose first.

## Call order (≈ 11 calls)
1. `create_knowledge_graph` × 8 (names above; `context`: "Research program testing whether a small language model's weights can serve as a fact store, evaluating in-weight editing methods"). Record per graph: diversity score, modularity, diagnosis word (`diversified` / `dispersed` / `focused` / `biased`), top clusters with betweenness share, top influential nodes, `contentGaps`, URL.
2. `difference_between_texts` with `llmdb-cold-reader-20261004` **first**, then prior-art A, prior-art B, c10-anyedit-keying, decision-log. What the cold-reader doc lacks is drift in the handoff.
3. `merged_graph_from_texts` over all eight → the union `contentGaps`.
4. `develop_latent_topics` on `llmdb-prior-art-B-20261004` (the candidate-solution synthesis) and `develop_conceptual_bridges` on `llmdb-c10-anyedit-keying-20261004`; `generate_research_questions` only if the latent pass returns headline topics.

## Questions the audit must answer (pre-stated so "interesting" is not a finding)
- Q-A. Which two dense clusters in the prior-art graphs never share a sentence? Candidates to test: *side-store designs* (CRME/RILKE/HoReN/P-Tokens) vs *spec constraints* (Git-vs-model separation §7.1); *locality instruments* (same-frame prompts, Pope audit) vs *deployment path* (Q4_K_M, super weight); *admission-test predictors* (LRE, COIN context reliance, FOVEATED NLL-by-position, WikiBigEdit frequency) vs *the A7 stimulus set* itself.
- Q-B. Does the cold-reader doc carry the keying finding, the four candidate options (ii-b, ii-c, iv, iii) and the new locality requirement, or does the handoff still read as "AnyEdit port or accept-bounded"? (Drift → fix in `SESSION_CHECKPOINT`/`program_state.json`, which are ours to edit.)
- Q-C. Is any single fact used for incompatible purposes in two documents (e.g. the ridge weight as locality protection in CORPUS/37–39 vs as writability limiter in CORPUS/43; "last-token keying" as the port's defect in CORPUS/42 vs as a frame write in CORPUS/43)? Name the sentence pair.
- Q-D. Which nodes bridge the C10 knob line and the keying line with high betweenness? If none, the two evidence chains are not yet connected in writing — the F1 determination should say in one sentence why the knob sweeps and the keying ablation point to the same mechanism.

## Resolve-or-log protocol
Every gap → one concrete claim → RESOLVED (file:line opened in-session, or a measured number) or LOGGED OPEN (owner = operator or next prereg; blocking yes/no). Closing statement names the blocking findings. Output: `scripts/build_report.py` → `results/infranodus_audit_2026-10-04/report.html`; a dated "Gap analysis" section appended to `docs/PRIOR_ART_SWEEP_2026-10-04.md`; drift fixes only in documents the program owns.
