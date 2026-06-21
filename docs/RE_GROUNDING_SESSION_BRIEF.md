# Re-Grounding Session Brief — fresh context, e2e-map-driven, read-contract-first

**Purpose of this doc:** the kickoff for a **fresh-context session** that steps back from write-engine work, re-grounds on the WHOLE e2e framework, and tightens focus onto the **empty cells** of the system — converting the coverage gap we found into focused, falsifiable forward work. Authored 2026-06-21 to close the prior arc (D20 done; GitHub sync live; NotebookLM working). **Read this first, then the read-order in §2.**

---

## §0 — Why this session exists (the meta-finding)
Our experimentation has been **write-engine-centric** — deep on MEMIT corruption (§8 + the §8.7/§11.14 drift-compaction slice), shallow-or-absent on the rest of the e2e. The spec-first miss, the late "it's a compaction-bounded hybrid" realization, and the "read contract is the biggest gap" discovery were all symptoms of lost whole-system scope. `docs/SPEC_E2E_GROUND_TRUTH.md` + `PROGRESS.md ⓪` now make the empty cells visible. **This session turns that map into a prioritized, runnable plan — it does NOT re-run write-engine scaling.**

## §1 — Objective + done-definition (do NOT let this become meta-work)
**Deliverables (all three, or it's not done):**
1. A **tightened e2e-prioritized plan** — which cells, in what order, each with a *falsifiable* criterion. Keyed to `PROGRESS ⓪`.
2. **The first new-cell experiment PRE-REGISTERED and ready to run** — almost certainly **CP2 / the READ-QUERY CONTRACT** (§3). Pre-reg = pass/fail set *before* the run, advisor-checked.
3. **Research leads folded into the hypothesis register** (`docs/HYPOTHESIS_REGISTER_*.md`) with builds-on/would-advance framing.

**Binding guard ([[evidence-over-scaffolding]], flagged ≥twice this program):** the output is a *runnable pre-registered cell*, not a prettier runbook or an open-ended literature sweep. If the session drifts into doc-polishing/research-without-end, stop and pre-register the cell.

## §2 — Re-ground read-order (binding — situate on the whole system, not the slice)
1. **`docs/SPEC_E2E_GROUND_TRUTH.md`** — the whole framework + memory lifecycle. Situate everything here.
2. **`PROGRESS.md ⓪`** — the e2e coverage map: PROVEN-for-scope vs PROTOTYPED vs **❌ UNTOUCHED** cells.
3. **`docs/SPEC_EXPERIMENT_OVERLAY.md`** — per-spec-section ↔ experiment/decision evidence.
4. **`EXPERIMENT_RUNBOOK.md` §0.3** (next actions) → **`SESSION_CHECKPOINT.md`** (top handoff).
5. **`DISCIPLINE.md`** — north star + the **SPEC-FIRST / RESEARCH-FIRST / situate-on-the-map** rules.
6. For the target cell: **read its spec section(s) END-TO-END** (spec-first), not grep excerpts.

## §3 — The target cell: the READ / QUERY CONTRACT (§G / CP2) — recommended
**Why it's #1 (per `PROGRESS ⓪`):** biggest empty cell; the spec leaves it least-specified; **a "database" with an uncharacterized query surface cannot be certified** — this is ahead of any further write-engine scaling. CP2 build-items + the broader read surface:
- **L1 triple-readback** (SELECT confirms a written edge — §8.9).
- **Reverse lookup / bidirectional traversal** (D4 — every edge reverse-lookable; §7.6).
- **5 query families** + **violates-rejection** (the contract surface — §G/E3).
- **Aggregation / negation / multi-hop reason-over-fact** (where "in-weight" vs "side-store" actually bites — B3N Axis A; EV-2 says a structured KG ≥ vector-RAG here).

The cell's job: define + test what reads the LLM-as-DB must support, on the in-weight store, with falsifiable pass criteria — and surface where the spec is under-specified (feed F1).

*(Alternates if a reason emerges: the memory-lifecycle LOOP — Pruning/GC/reconciliation, §11.12–14 — also UNTOUCHED; or the D20 component-1 SCALE test, gated on a stimulus-pool build. CP2 is the recommended start.)*

## §4 — Grounding research plan (RESEARCH-FIRST: our corpus BEFORE the open web)
**Step A — mine our OWN corpus first (no external tool needed):** `research_and_specs/` (`cross_entity_research_synthesis.md`, `llm_editing_survey.md`, `llm-knowledge-editing-same-entity-locality.md`), **`external_evidence_notes.md`** (NeuralDB = EV-3 verified; don't re-verify), **hypothesis register §J** (read-contract leads **D9** NeuralDB/gated-side-store, **D13** context-reasoning, **D18** self-updatable memory/MemLLM, **D19** Parametric-RAG), `CORPUS/05` contracts. Name the *genuine remaining* gap before reaching out.

**Step B — targeted external (only the named gap):**

| Tool | Who runs | Use | Draft query/prompt |
|---|---|---|---|
| **NotebookLM** (✅ works from pod) | agent or operator | what OUR corpus already says about the read contract | `notebooklm use <id>; notebooklm ask "What does this corpus say about the READ/QUERY contract for an LLM-as-database — exact lookup, reverse lookup, aggregation, negation, multi-hop reason-over-fact, the 5 query families — and what is left unresolved or unspecified?"` (run on both notebooks `23ba5f2d…`, `f667f1f2…`) |
| **Perplexity** | operator | open-web SOTA on querying a parametric/edited LLM store | "What are the SOTA approaches and benchmarks for a structured READ/QUERY contract over a parametric or knowledge-edited LLM store (exact lookup, reverse lookup, aggregation, negation, multi-hop)? Cover NeuralDB, text-to-query over KV/KG stores, GraphRAG vs vector-RAG for structural reads, and any read-contract/eval frameworks. Cite; flag speculation." |
| **InfraNodus** | operator | structural-gap lens over our corpus + us-vs-field | (a) `generate_content_gaps` over CORPUS/ + research_and_specs/ + the spec → does it independently surface the read-contract/Pruning gap? (b) `difference_between_texts`: our corpus vs the read-contract literature → where does the field have dense structure we lack? Outputs = **LEADS → hypothesis register, never evidence** (DISCIPLINE §3). |
| **deep-research** | agent | triangulate the Perplexity survey if a claim is load-bearing | in-session; cited report |

## §5 — Sequencing
re-ground (§2) → mine our corpus + run NotebookLM (agent) + queue Perplexity/InfraNodus (operator) → synthesize the named gap → **pre-register the CP2 read-contract cell** (pass/fail before the run) → **advisor** → run → close-out + push.

## §6 — Open operator decisions to carry in
- **D20 component-1 (SCALE) stimulus-build:** worth building a large screened single-token fact pool to test single-solve cleanliness at true scale? (operator effort call — still open).
- **B3N incremental write-RATE calibration:** sets compaction cadence + whether the high-churn side-store row applies.

## §7 — Guardrails (binding, carry all)
SPEC-FIRST · RESEARCH-FIRST · situate-on-the-e2e-map · falsification-first (pre-register; reserve confidence for runs that can fail) · advisor before authoring + before done · gpt-5.5 cross-family at promote gates · the close-out gate (`tools/closeout_check.py`) · **scope `git add`, secret-scan before every push** (public repo — [[git-add-all-leaks-secrets-on-public-repo]]) · the deliverable is a runnable pre-registered cell, not more scaffolding.
