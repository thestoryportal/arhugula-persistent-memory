---
name: infranodus-discourse-lens-not-coverage-tool
description: InfraNodus surfaces discourse structure/clusters/gaps over the TEXT you give it; it CANNOT read code, verify an implementation, or assess coverage of a prior-art corpus. For "are there gaps in repo/corpus X relevant to our science," enumerate→triage→READ; don't InfraNodus.
metadata:
  type: feedback
---

InfraNodus is a **text-network-analysis lens**: word co-occurrence → topical clusters, betweenness gateways, structural gaps, discourse-diversity state (biased/focused/diversified/dispersed) — **over whatever TEXT you feed it.** The operator repeatedly asks whether to use it for an analysis task; match the tool to the claim.

**RIGHT tool for:** synthesizing a body of text you ALREADY have. Demonstrated 2026-06-23 — fed the tooling-audit corpus → it returned a "dispersed" discourse state + 3 content gaps (Test/Debug↔Stats, Experiment-Refine↔Bias-Audit, Power↔Bias-Audit) that genuinely sharpened the adoption order into "build ONE pre-register→verify-runs-stats→bias-audit gate, don't scatter." A discourse-structure / ideation lens.

**WRONG tool for:** (a) reading CODE or verifying what an implementation actually does; (b) assessing **COVERAGE** of a prior-art corpus ("does repo/author X contain or lack Y relevant to our science"); (c) anything needing semantic understanding of files you haven't read. It only sees the text you give it, and most repos have empty descriptions → nothing to analyze without reading first.

**Why:** [[match-metric-to-the-claim]] generalized to *tool selection* — the goal "coverage / relevance-mapping" has metric "enumerate→triage→read," not "discourse-diversity." **Proven the same session:** the chrishayuk/LARQL gap-map (`docs/CHRISHAYUK_CORPUS_GAP_MAP.md`) — LQL has no "violates" grammar, ffn_down is a Q6_K/Q4_K mix, a hidden `REBALANCE` solver — was ALL code-level facts InfraNodus could never surface; **a Tier-1 deep-read (fan-out subagents) was required.**

**How to apply:** for "are there gaps in this corpus relevant to our science," **enumerate the repos → triage by relevance → deep-read the on-domain ones (fan-out subagents) → map to our open questions** (runbook §0.3 / hypothesis register). Use InfraNodus only as an optional *end-stage* thematic lens over text you've already extracted. Fence unchanged: InfraNodus outputs = LEADS, never CORPUS evidence ([[research-first-and-verify-tool-availability]]).
