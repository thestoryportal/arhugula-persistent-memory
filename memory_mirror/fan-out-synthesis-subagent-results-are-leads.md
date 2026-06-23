---
name: fan-out-synthesis-subagent-results-are-leads
description: "When synthesizing parallel subagents, their summaries are LEADS — re-verify load-bearing claims centrally and don't inherit their confident verbs"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 317c82e2-252c-46a7-abba-737b556c459e
---

When I fan out parallel subagents for a search/triage/verification task and synthesize their returns, **a subagent's summary is a LEAD with the same status as any external artifact — not a verified fact.** Two failure modes hit me in ONE session (the 2026-06-23 prior-art sweeps; the advisor caught BOTH), so treat them as a standing checklist:

1. **Don't inherit a subagent's confident VERBS.** A subagent glossed LocFT-BF as "corroborates our A1 batch-clean result" — but LocFT is gradient-FT (not our closed-form MEMIT) and doesn't touch the mechanism our falsifier tests. A cross-family / cross-metric / cross-scope result is an ANALOG, not corroboration of your own result. Before promoting any "confirms/corroborates/pre-empts/refutes," check method-family AND mechanism AND metric match. Default unread cross-source claims to "directional/analog," then upgrade only on a real match. (This is confirmation-amplification — see [[review-diminishing-returns-evidence-is-binding]], [[calibrate-confidence-mechanics-vs-contracts]].)

2. **A delegated verification you didn't run is NOT done.** Subagents asserted "every arXiv ID page-verified on arxiv.org" — but they were rate-limited onto a fallback channel that had *demonstrably mislabeled* a paper (HYPE: title "…Graph-Based External Memory," method is in-weight "HYperbolic Parameter Editing"). Their "verified" was self-vouching by the same channel that erred. **Never write "verified" in a durable artifact unless YOU ran the check.** The fix is cheap and asymmetric: one batched call from the MAIN shell (e.g. `export.arxiv.org/api/query?id_list=...`, or a GitHub-API loop) diffing returned titles vs claimed. Weight suspicion toward post-training-cutoff IDs and toward whatever channel the subagents were forced onto. ([[verify-external-artifacts-before-effort]].)

**Why fan-out invites both:** parallel agents return polished, confident prose that reads like settled findings, and you're synthesizing N of them under load — exactly when calibration and the verify-step lapse. Build the central re-verify + verb-audit into the synthesis step itself, before writing anything durable. Also: parallel agents hammering one rate-limited public API (arXiv export) trip 429 — do DISCOVERY in the agents but VERIFICATION centrally in the main shell. And: a prior-art pass's most valuable product is often the honest **exhaustion/saturation call**, not volume ([[evidence-over-scaffolding]]).
