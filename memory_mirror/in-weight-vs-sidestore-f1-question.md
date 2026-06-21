---
name: in-weight-vs-sidestore-f1-question
description: The highest-stakes open F1 question is now B3 — is diffuse in-weight storage even the right architecture, vs a gated/routed side-store? The field (NeuralDB/WISE/GRACE/MEMOIR/SCEN) converges on side-stores + names editing "illusory"; our own evidence (G6.1 cross-entity corruption; per-relation count = coarse held-out-dependent sentinel) is consistent. F1 must explicitly decide in-weight-with-conditions vs recommend-hybrid
metadata:
  type: project
---

After the 2026-06-21 ConnectedPapers 6-graph review (hypothesis register §J, leads D8–D19) + the D-D1-2 corruption findings, the **central architecture question for the F1 readiness determination is B3**: *is diffuse in-weight (MEMIT-class) storage even required, vs a gated/routed side-store?*

**Why it's now the highest-stakes item (not just one hypothesis among many):**
- **The field converges on gated side-stores** that structurally avoid cross-entity corruption by routing edits to a disjoint store: **NeuralDB** (linear L&E = KV-DB query + non-linear gated retrieval, 100K facts, the closest published cousin to the LLM-as-DB spec — EV-3), **WISE**, **GRACE**, **MEMOIR** (sparse disjoint masks), **SCEN** (per-fact experts), **InComeS** (gist-token KV). Plus **Parametric-RAG** (D19) as a third paradigm.
- **Named critiques** that diffuse in-weight editing is fragile: *Is Model Editing Built on Sand?* (shortcuts not semantics, collapses under negation), *Mirage of Model Editing* (teacher-forcing inflates 96.8%→38.5%, fails @1000 edits). Our autoregressive-top-1 discipline + G6.1 scale-corruption are *consistent* with these.
- **Our own evidence pressures it:** G6.1 cross-entity read corruption; D-D1-2 showed per-relation count is a coarse, held-out-set- and edit-order-dependent *sentinel*, and mixed-load showed other-relation *volume* corrupts a relation's reads independent of its concentration. The diffuse-in-weight store keeps fighting the same interference the side-store designs avoid by construction.

**How to apply:** F1 cannot be a clean "in-weight ready-with-conditions" without explicitly deciding **in-weight-with-conditions vs recommend-hybrid/side-store read-path**. B3 is analysis-heavy/low-compute (decide it against E3 — L1 retrieval can't do multi-hop "reason over the stored fact"). It is on the F1 critical path alongside **CP2 schema build-items** and the **7B numeric-threshold transfer (OQ-W1)**. Don't write F1 before B3 is taken a position on. See [[experiment-runbook-is-canonical]] §0.3, PROGRESS ③, hypothesis register §B/§J.
