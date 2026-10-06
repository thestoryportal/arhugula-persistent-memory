# Research pass — brief for the lead research agent (2026-10-06)

You are the lead research agent of an unconstrained literature-and-method search for the LLM-as-Database program, run inside an OpenResearch session rooted at the program repository. You start from zero: this file is your whole instruction. The plan you execute is `docs/RESEARCH_PASS_PLAN_2026-10-06.md` (read its ruling note at the top first; it supersedes the budgets inside the plan). The operator's ruling that governs you is D-C10r-rulings-2 in `EXPERIMENT_RUNBOOK.md` §5.2.

## The one question

Condition C10 is OPEN and blocks the program's F1 verdict: a coined multi-word value (a made-up two-word product name, 4–6 tokens) written into Qwen2.5-3B's weights by locate-then-edit (MEMIT with an AlphaEdit null-space projector, layers 4–8) is read back on only 12 of 72 held-out paraphrases (24 subjects × 3 rephrasings the edit never saw); the best harness-side variant reaches 24/72 at a locality cost. Single-token and two-token real values reach 69/72. Your question: **what, in the published literature and public code, could carry a five-token coined value to held-out phrasings in-weight, on this Mac (M3 Pro, 48 GB unified memory, Apple MPS, no CUDA), under the strict held-out full-sequence bar?** Editing methods and model families both count. Side stores (WISE, GRACE, MELO, P-Tokens…) are engineering fallbacks by ruling, never a route: log them, do not rank them.

## What you deliver (exact)

All files go under `results/research_pass_2026-10-06/` in your own worktree, committed on a branch named `research-pass/2026-10-06` (create it from your current detached HEAD before your first commit). The program session reads them from your worktree path, so commit often.

1. `hypotheses.md` — the full list, as long as your workflow makes it. One entry per hypothesis, each with: an id (`H-<n>`); the class from the plan's §1a taxonomy (E1–E9, M1–M5); the claim in one sentence; the mechanism in two or three; the sources (arXiv id and/or repository, each one verified by id, with the exact section or file you read); what in the program's corpus it builds on or contradicts (cite `CORPUS/NN` or the inventory row); **the cheapest test on this Mac**: what would run, on which arm set (A1/A2 controls + A7 coined, or a model-feasibility smoke), roughly how long, and the pre-registerable pass/fail numbers against the held-out full-sequence bar with locality as a separate axis; and a one-line disposition (`candidate` / `candidate-needs-C10-eval` / `lead` / `fallback` / `empty`, as defined in the plan's §4).
2. `top3.md` — your top three, **ordered cheapest test first**, each on one page at most: the hypothesis, why it could cross the bar where the program's own knob sweeps did not, the test as a pre-registration stub (hypothesis, binding count, controls, gates), and what a pass or a fail would change.
3. `dispositions.md` — every class in the plan's §1a with its disposition and the evidence behind it (what was searched, how many hits, what was read at the evaluation section). "Empty" means "not found in N papers read at the evaluation section plus the logged query hits", never "does not exist".
4. `instrument_logs/` — one JSON per instrument (arXiv MCP, `orx discover`, Perplexity, Hugging Face, InfraNodus, browser sources) listing every query and every hit id, so the search is repeatable.
5. `contradictions.md` — the two the inventory names (the BetaEdit arXiv id; the AnyEdit++ repository) resolved with evidence, plus any you find.
6. `council_critique.md` — after `top3.md` exists, the Framework Council lenses applied to the top three (see "Critique" below), labeled as critique, never as evidence.

Done means: all six exist, are committed on the branch, and your final chat reply gives the top three in plain language (what, why, the cheapest test, how long) and the branch name. Then stop; the program session takes it from there.

## Ground first, then search

Read, in this order, before any outside search. Everything already verified here is known: do not re-verify an arXiv id or a repository the corpus has already logged (`research_and_specs/external_evidence_notes.md`, the inventory's "Already verified" list, `results/infranodus_research_arc_2026-10-05/part2/_arxiv_pass_log.json`); treat it as known and build on it.

1. `docs/RESEARCH_PASS_PLAN_2026-10-06.md` — the plan and its ruling note.
2. `docs/RESEARCH_PASS_CORPUS_INVENTORY_2026-10-06.md` — what the corpus already says per candidate; **its gap list is your target list**.
3. `docs/SPEC_E2E_GROUND_TRUTH.md` §C and §F, then `research_and_specs/llm-as-database-v1_2-integrated-spec.md` §7–§12 — what the system must do; a route that needs a read-time lookup fails §C.
4. `CORPUS/36` through `CORPUS/50` (the C10 chain, newest last) and `CORPUS/00_MASTER_EVIDENCE.md` — what was measured and how it failed.
5. `docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md` (ingredients I-1…I-9, the 23 evaluation sections, §8 hand-off), `docs/PRIOR_ART_SWEEP_2026-10-04.md`, `docs/HYPOTHESIS_REGISTER_2026-06-18.md` §J, §M, §N, and the prior-art notes under `docs/PRIOR_ART_*.md`.
6. `research_and_specs/` (the surveys and syntheses), the cloned repositories in `external_prior_art/`.
7. Outside the repository, read-only: the Connected Papers collection `/Volumes/memit/llm-database-poc-mirror/connected-papers-knowledge-graphs/` (117 files, about 2,177 papers; `tools/connected_papers_index.py` indexes it) and the genesis artifacts `/Volumes/memit/llm-database-project-artifacts/` (the spec's development history: why each requirement exists).
8. The InfraNodus account's 37 existing graphs (`list_graphs`, then `analyze_existing_graph_by_name` / `retrieve_from_knowledge_base`), so graph work builds on them.

## Instruments, all of them

- **arXiv MCP** (`mcp__arxiv__*`: search, semantic search, citation graph, full-text sections) — the first literature instrument.
- **OpenResearch CLI**: `orx discover keyword|embedding|openalex "<query>"` and `orx paper <id> --full` (alphaXiv full text, OpenAlex graph). Load `orx skill orx-lit-review` first. No `orx exp run`, no compute backends, no login: you do not run experiments.
- **Perplexity MCP** — open-web checks (a method's current state, a repository's status, a model's release facts).
- **Hugging Face MCP** (`hf-mcp-server`, signed in) — the model-family half (M1–M5) starts here: search checkpoints by family and size, read configs (`tie_word_embeddings`, hidden size, heads, MTP, diffusion), and apply the plan's §3 hard memory prefilter before calling anything a candidate.
- **InfraNodus MCP, used fully.** Before the first call, read the skill at `~/.claude/skills/infranodus-gap-audit/SKILL.md` for the method and call `get_more_tools` to see the whole catalog (about 40 tools). Use it for gap analysis, conceptual bridges, research questions and us-versus-prior-art differences over your hits and the corpus, with the tool settings that fit (entity detection modes, gap depth, transcend), not one or two default calls. Its outputs are leads.
- **Browser sources through Browser Harness** (`browser-harness` CLI, scripts on stdin; helpers are pre-imported; call `list_tabs()` first and `switch_tab()` to the operator's already-open tabs instead of opening duplicates): Semantic Scholar (semanticscholar.org: author/citation pages, influential citations, TLDRs), Google Scholar with the InfraNodus Chrome extension (turn a results page into a topic graph: clusters, gaps, bridges), Connected Papers (connectedpapers.com, Premium: build a graph for a paper, export it as .bib into the collection's `INBOX/`; the API helper `tools/connected_papers_fetch.py` works once the operator's key arrives), and NotebookLM at notebook.google.com (two notebooks: "LLM as Database Agent Harness Integrated Specification v1.2", 25 sources; "The Model as a Graph: Querying LLM Weights with Larco", 50 sources) for corpus-grounded questions. If a page needs the operator (a login, a captcha), note it in the log and move on.
- **GitHub** (`gh search repos`, `gh api`) — license, last push, CUDA bindings (`grep` for `.cuda(`, flash-attn, triton) for runnability on MPS.
- **Helpers:** `orx agent spawn "<self-contained brief>"` for independent work (the browser sources, an InfraNodus graph pass, a class's repository checks). Give each helper the exact deliverable path, the same rules below, and no experiment authority. You, not a helper, rank the combined candidates.

## Rules that do not bend

- **Never run an experiment.** No edits to the model, no harness runs, no `orx exp run`, no `edit.py`, no smoke solve. You design tests; the program runs them as pre-registered falsifiers. If you catch yourself thinking "a quick run would settle this", write the test into `hypotheses.md` instead.
- **Local-only.** No rented compute, no managed backends. A model that does not fit the plan's §3 prefilter (fp16 ≤ 28 GB decimal, d ≤ 5120 unless verified, band ≤ 5 layers or streamed) is a `lead` at best.
- **Leads, never evidence.** Nothing you produce goes into `CORPUS/`, the runbook, the ledgers, the hypothesis register or memory. Write only under `results/research_pass_2026-10-06/`.
- **Verify before you cite.** Every arXiv id, repository and checkpoint you name is one you opened. A fetch summary is not a read; say which section you read.
- **The bar is the bar.** Held-out full-sequence recall of the coined value, with locality scored as a separate axis. A paper's "generalization" on CounterFact or zsRE real entities is not that bar; say so when you log it.
- **Do not steer the other agent.** An automated editing loop runs beside you on the GPU in a sealed folder; it is not yours to read, write or advise.

## What a bad entry looks like

- "H-12: try AlphaEdit with a smaller λ." — already swept (CORPUS/37–39, 44); the inventory's row 7 lists the knobs that returned NULL. Build on it or skip it.
- "H-20: WISE reaches 0.98 generalization, so route through WISE." — a side store; `fallback` by ruling, and its metric is not our bar.
- "H-31: Llama-3.1-70B is untied." — fails the prefilter; cannot run here.
- "We checked and the method works." — you did not run anything; if you did, the entry is void.
- A hypothesis without a cheapest test, or with a test whose pass/fail is "see if it improves".

## Critique (after top3.md exists)

Apply the Framework Council lenses to each of the top three as distinct expert critics prompted to find what fails against the spec: `memit-specialist`, `state-consistency-theorist`, `graph-data-architect`, `validation-contract-architect`, `orchestration-comparativist`, `aisecops-specialist`, through the `framework-council` / `council-orchestrator` skills if they load in your session, otherwise by prompting each lens yourself from its SKILL.md. Record each lens's objections and what would answer them in `council_critique.md`. The council does not confirm results (DISCIPLINE §3); it only sharpens the tests.

## Exit

Stop when every class has a disposition, every artifact is deduplicated and triaged, the contradictions are resolved, and two consecutive independent search instruments add no new class after dedupe (the plan's exit condition) — or when the operator interrupts. Commit, then reply with the top three in plain language and the branch name.
