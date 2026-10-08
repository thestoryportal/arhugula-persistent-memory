FIX-FIRST

Reviewer: GPT-6-Astra (high)  
Runtime model/effort authentication: UNVERIFIABLE.

**BLOCKING**

- **draft:61–67 — reader budget omitted.** `c10x_enginepath_read.py:1048–1061` independently enforces targets ≤2400 and process ≤15000. Exact addition: “Update reader admission to targets ≤3600 s and process ≤16200 s. Add test-first acceptance within the newly admitted ranges and rejection above each amended limit; preserve every scientific gate.”
- **draft:1,4 — observation disclosure.** “Pre-candidate” misstates chronology, despite its redefinition. Replace with **“post-refusal, post-candidate-observation”**; state: “Re-run 1 executed both candidate recipes and interim counts were seen. Those counts neither selected nor justified these caps.”
- **draft:28,67 — incomplete authority record.** `EXPERIMENT_RUNBOOK.md:381` requires arithmetic recorded **there and in the amendment before spending**. Add: “Before dispatch, record D-C10x-targetscap and its arithmetic in §5.2, with the authenticated Astra review reference and verdict.”

**ADVISORY**

- Arithmetic checks out: caps total **15600**, budget **16200**, setup slack **600**; measured setup leaves A-entry margin **1174.33**; targets-entry margin **1582.73**. Two-process budget: **32400 s**. Other caps, projection policy, deadline enforcement and scientific rules remain unchanged.
- **draft:23,50,53:** replace “recorded slowest solve” with **“inferred lower bound on an unrecorded maximum”**; replace “not measured” with **“measured internally but not persisted.”** Approximately **9.72 s mean** cannot establish sufficiency of 3600 s.
- **draft:41,54:** **16.667 s is a sufficient envelope before overhead, not a universal per-unit cutoff.** A later 17-second solve need not refuse. The binding condition remains `elapsed + m×remaining + previous_overhead > 3600`; refusal is a real HALT, never NULL.
- **draft:3,23:** entry passed; refusal occurred **before solve 2–24, after 1–23 completed samples**. Say “early within targets,” not “at entry.”

Read-only review; no model/GPU execution.

🌱 graft saved ~99,873 tokens this turn, 1 successful call.

