# D-NEW1-b real-run authorization (operator, 2026-10-10T05:39Z)

Operator answered AskUserQuestion "Authorize C1 + C2" against Astra GO-WITH-CONDITIONS (`new1_b_go_astra.md`):

- **C1:** exactly ONE real NEW-1 attempt, caps **2,700 s** total monotonic time and **11 GiB** observed worker-process-family RSS; **no automatic retry, no cap increase** without a new operator decision.
- **C2:** this sole attempt serves as the complete-workload resource validation, replacing the earlier validate-before-execution prerequisite (`new1_b_variant_astra.md:21`).
- **C3 (orchestrator-checked at launch):** unchanged supervisor, fresh fail-closed CPU admission, all cell reserves (19 GiB available for float64 SVD/checks), nice-10. Admission refusal ends this dispatch.

Prereg pin: 1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f. A completed run permits only reviewed MATH-PROXY reporting; STOPPED-DEADLINE / STOPPED-RESOURCE / missing terminal event return to the operator with no verdict.
