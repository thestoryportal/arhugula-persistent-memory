---
name: research-first-and-verify-tool-availability
description: "Two binding discipline rules (twins of spec-first): (1) RESEARCH-FIRST — before framing a method/prior-art/field question as open or launching new external research (Perplexity/NotebookLM/deep-research/InfraNodus) or generating hypotheses, check our OWN research_and_specs/ corpus + external_evidence_notes + hypothesis register §J FIRST. (2) VERIFY-TOOL-AVAILABILITY — a tool a doc references (esp. an MCP like InfraNodus) may NOT be connected; confirm it's in the live tool list before relying on it, and surface the operator-gated setup (API key) rather than silently skip or pretend it ran."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1a56870e-a5ec-406a-9964-827f761992a9
---

Operator flagged (2026-06-21), right after the spec-first fix: "what about discipline around invoking the InfraNodus MCP, and referencing research docs — like the spec-referencing gap?" Two real gaps, both encoded into `DISCIPLINE.md` §1:

**RESEARCH-FIRST (the spec-first rule's twin).** Just as the SPEC pre-decides things that look "open", **our own research corpus often already answers a method/prior-art/field question** — so before framing one as open, launching new external research, or generating hypotheses, check FIRST: `research_and_specs/` (`cross_entity_research_synthesis.md`, `llm_editing_survey.md`, `llm-knowledge-editing-same-entity-locality.md`, `llm_research_tools_*`), **`external_evidence_notes.md`** (artifacts already VERIFIED — don't re-verify, [[verify-external-artifacts-before-effort]]), the **hypothesis register §J** (ConnectedPapers leads already mined), `docs/SPEC_EXPERIMENT_OVERLAY.md`, `CORPUS/`. New external research is justified only AFTER the corpus is checked and the genuine remaining gap is named. **Why:** same failure mode as spec-first — re-running a survey we have, re-verifying a logged repo/arXiv id, or treating settled prior-art as open.

**VERIFY-TOOL-AVAILABILITY.** A tool that a doc *describes* may not be *connected*. **InfraNodus is the case in point:** AGENTS.md §101 documents it as an MCP ("READY — key required"), and DISCIPLINE referenced its call names as if invocable, but it is **NOT connected by default** (needs `claude mcp add infranodus --env INFRANODUS_API_KEY=… -- npx -y infranodus-mcp-server` + an **operator-gated API key**). Before relying on any such tool: confirm it's in the live MCP/tool list (`ToolSearch`); if absent, surface the gated setup need (a credential move — like paid-provider in AUTONOMY) — **do NOT silently skip it or narrate as if it ran.** (Same applies to the framework-council `.skill` bundles and the `autoresearch` skill — vendored, NOT harness-registered.)

**How to apply:** these are read-triggers in `DISCIPLINE.md` §1 alongside [[in-weight-necessity-is-scope-keyed-hybrid]]'s SPEC-FIRST rule. The fence is unchanged: InfraNodus / autoresearch outputs are **LEADS → hypothesis register, never evidence / never `CORPUS/`** (DISCIPLINE §3). Pattern: the program's instrument docs drift from the program's instrument *reality* — verify availability, check our own corpus, before reaching outward.
