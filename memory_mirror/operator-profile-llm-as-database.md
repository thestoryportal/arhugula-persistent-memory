---
name: operator-profile-llm-as-database
description: Who the operator is on the LLM-as-Database program and how to collaborate effectively with them.
metadata: 
  node_type: memory
  type: user
  originSessionId: 2801cf2e-560f-460c-86df-e227b16051b2
---

The operator (robert@thestoryportal.org) owns the "LLM-as-Database" spec and program but is **learning ML/LLM as they go** — they have explicitly said they lack the ML/editing specialization to adjudicate technical/architecture calls themselves. They are nonetheless an **effective collaborator and adversarial check**: their pointed questions ("are you ABSOLUTELY certain?", "have you actually read the spec end-to-end?", "why must this be local — can't the pod run it?", "consult the advisor before we approve") repeatedly caught real blind spots and over-claims this session.

**How to work with them:**
- Make every decision **legible** — explain the tradeoff in plain terms before recommending; never push an expertise-gated ML decision onto them. Defer hard calls to **evidence**, not authority.
- They value rigor, durable artifacts/checkpoints, honest "what's proven vs unproven," HIL gates before big moves, and consulting the advisor on load-bearing questions. Give a recommendation, not a survey.
- Deployment target is **TBD** — may be a remote GPU, not necessarily their local Intel CPU (so the RunPod box is a valid proxy). Don't assume CPU-only.
- They work across long, multi-month arcs and care about forward-session continuity (bootstrap/corpus/memory). Take their challenges as genuine signal to re-search, not to re-defend. See [[exhaust-options-before-blocked]], [[read-authoritative-source-fully]].
