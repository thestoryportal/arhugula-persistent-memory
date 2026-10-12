# Grounding coverage — research pass 2026-10-06

Branch `research-pass/2026-10-06`, from commit 545d11e. Written before the first outside query and updated as the pass proceeds. Every entry says what was read directly by the lead agent, what was read through a read-only helper agent (reports reviewed, not the files), and what could not be reached.

## Calibration (written before the first outside query)

The three items the brief asks to be classified under the rules, before any search:

(a) **BetaEdit arXiv id 2605.09285.** Classified: **contradiction to resolve, not a verified source.** The inventory lists it both as "already verified" (the 2026-10-05 pass log returns a real paper with that id) and as a contradiction (runbook line 295 and `memory_mirror/betaedit-official-repo.md` call the id fabricated). The dedupe exemption in the brief applies: the id is opened on arXiv in this pass, its title, authors and evaluation section read, and the result written to `contradictions.md`. Until then nothing in this pass cites 2605.09285 as known.

(b) **AnyEdit++ repository `TianSuya/Bayes-Chunk`.** Classified: **unverified.** The only record is `docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md` line 3, which names the URL, and line 5, which says the paper was read "via fetch summary (not the PDF text)". The repository was never cloned or opened. In this pass it is opened through the GitHub API (existence, licence, last push, device bindings, which model configs ship) and the result written to `contradictions.md`. Until then it is not a verified artifact and AnyEdit++ carries no "code available" claim.

(c) **A 7–8 B untied-embedding model that passes the static memory arithmetic.** Classified: **`lead`, "static prefilter passed; empirical feasibility pending".** The plan's §3 prefilter requires a one-layer covariance / null-space solve smoke on the M3 Pro before promotion from `lead` to `candidate`; a smoke solve is a run and this pass runs nothing. The arithmetic itself is done against the edited matrix, which in the harness is `down_proj` with input dimension = the MLP intermediate size (CORPUS/41 records 18,944² fp32 projectors of about 1.34 GB each for a 7 B Qwen), not hidden × hidden; an 8 B Llama with intermediate 14,336 gives 14,336² × 4 B ≈ 0.82 GB per fp32 projector, five layers ≈ 4.1 GB, which sits inside 48 GB with 16 GB of fp16 weights but still only as a `lead`.

None of the three comes out "verified candidate".

## Grounding sources, in the brief's order

| # | source | how read | coverage |
|---|---|---|---|
| 1 | `docs/RESEARCH_PASS_PLAN_2026-10-06.md` | direct, in full (95 lines) | complete, including the ruling note |
| 2 | `docs/RESEARCH_PASS_CORPUS_INVENTORY_2026-10-06.md` | direct, in full (57 lines) | complete; gap list items 1–9 are the target list |
| 3 | `docs/SPEC_E2E_GROUND_TRUTH.md` §A–§J | direct, in full (98 lines) | complete |
| 3 | spec `research_and_specs/llm-as-database-v1_2-integrated-spec.md` | direct: §7 and §8 in full (lines 241–416); §11.2–11.3 (lines 633–645); Part V §18 headers; grep of §9–§12 for retrieval / lookup / tokenizer / vocabulary terms (3 incidental hits, none a read-time knowledge lookup) | §7, §8, §11.2–11.3 complete; §9, §10, §12 by header and keyword only |
| 4 | `CORPUS/35`–`50` (the C10 chain) | direct, in full, every file | complete |
| 4 | `CORPUS/00`–`03` and `04`–`34` | helper agent read every file in full; report reviewed and condensed to `helper_reports/corpus_00_34.md` | complete by helper |
| 4 | prereg documents `docs/*PREREG*.md` | not read in full; read when a hypothesis touches the finding (recorded per hypothesis) | partial by design |
| 5 | `docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md` | direct, in full (219 lines) | complete |
| 5 | `results/infranodus_research_arc_2026-10-05/{fulltext,segments,part2,operator_chat_inbox}` | helper agent over the program worktree copy: all 28 `fulltext/` extracts (headers, first ~60 lines, metric grep), all title lists in full, the pass-log structure, every inbox file; `segments/` listed only; the 13 round-3 graph JSON exports and 2 rtf files not read; condensed to `helper_reports/infranodus_arc_raw.md` | complete by helper, with the gaps named |
| 5 | `docs/PRIOR_ART_SWEEP_2026-10-04.md` | direct, in full (321 lines) | complete |
| 5 | `docs/HYPOTHESIS_REGISTER_2026-06-18.md` | direct, in full (317 lines; §J, §M, §N and the C10 entries closest) | complete |
| 5 | `docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md`, `PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md`, `PRIOR_ART_CHRISHAYUK_LARQL_2026-10.md`, `PRIOR_ART_OPENRESEARCH_2026-10-06.md` | direct, in full | complete |
| 5 | `docs/PRIOR_ART_ARXIV_SWEEP_2026-06-23.md`, `PRIOR_ART_REPO_SWEEP_2026-06-23.md` | not read directly; their id lists are carried by the inventory's "already verified" section | by proxy |
| 5 | `docs/EXPERIMENT_REGISTRY.md`, `EVIDENCE_INDEX.md`, `docs/SPEC_EXPERIMENT_OVERLAY.md` | direct, in full | complete |
| 5 | `EXPERIMENT_RUNBOOK.md` | rows 305–308, 316, 318, 322 (the rulings D-B3N-1, D-C10k-rulings-1/2, D-C10q-rulings-1, D-C10r-rulings-2, D-HW-1 line 69) | targeted |
| 6 | `research_and_specs/` surveys and syntheses | helper agent read all 12 named files in full plus two proposals in full and grepped the rest of `proposals/` and `predecessor_design/`; condensed to `helper_reports/research_and_specs.md` | complete by helper |
| 6 | `external_prior_art/` (program worktree copy: AnyEdit, AnyEdit_mps, OpenResearch, autoresearch-*) | listed; AnyEdit code facts taken from CORPUS/41–42 and the reduction note, not re-read | by proxy |
| 7 | Connected Papers collection (117 files) | helper agent grepped titles across all 92 `.bib` files (the indexer writes files unconditionally, so it was not run); PDFs, InfraNodus JSON and the 7 project-note files not read; condensed to `helper_reports/connected_papers_and_genesis.md`. Four new graphs were added to `INBOX/` by the browser helper | complete by helper, with the gaps named |
| 7 | genesis artifacts `/Volumes/memit/llm-database-project-artifacts/` | helper agent read `_manifest.md` in full, every top-level folder, the spec/transcript/skill files that speak to why in-weight, multi-token values and the write-engine choice; `.ipynb`, `.skill` and JSON logs not read | complete by helper, with the gaps named |
| 8 | InfraNodus account graphs | `list_graphs` → 37 graphs listed; one new graph `llmdb-rp-hits-20261006` built from this pass's hits and used for gaps, research questions, bridges and a difference against the inventory gap list (`instrument_logs/infranodus.json`) | listed and extended |

## Instruments verified reachable before use

- arXiv MCP: tool schemas loaded (search, abstract, download, outline, section, citation graph).
- OpenResearch CLI `orx 0.2.16`: `orx telemetry off` confirmed; `discover keyword|embedding|openalex` and `paper --full` help read.
- Perplexity MCP: search / ask / research loaded.
- Hugging Face MCP: `hf_fs`, `hub_repo_search`, `hub_repo_details` loaded; account `robertrhu`.
- InfraNodus MCP: `get_more_tools` reports the full list is already exposed; skill `~/.claude/skills/infranodus-gap-audit/SKILL.md` read; 37 graphs listed.
- Browser Harness CLI present; skill text read. Chrome tab reuse rules noted.
- `gh` authenticated (account thestoryportal). `codex` 0.160.1 present for the cross-family review at promote gates (not used by this pass; the pass promotes nothing).

## Browser sources (helper; see `instrument_logs/browser_sources_notes.md`)

Reached: Semantic Scholar, Google Scholar, Connected Papers (Premium, four graphs exported to `INBOX/`), NotebookLM (both notebooks). Not reachable: the InfraNodus Chrome extension (not installed in the operator's Chrome as seen over CDP). The browser was driven only by the helper; the lead agent opened no tabs.

## Not reached or not read

- `docs/PRIOR_ART_ARXIV_SWEEP_2026-06-23.md` and `docs/PRIOR_ART_REPO_SWEEP_2026-06-23.md`: carried through the inventory's verified-id list, not re-read.
- Pre-registration documents under `docs/*PREREG*.md`: read only where a hypothesis depended on a finding's design (C10L covgeom P4 tokenisation declaration, via the arc helper); the rest by their CORPUS summaries.
- The spec's §9, §10, §12 and Part IV: by headers and keyword grep only (the council lenses were pointed at the relevant line ranges).
- `holi-lab/MDM-KE`: does not exist (see `contradictions.md` §3).
