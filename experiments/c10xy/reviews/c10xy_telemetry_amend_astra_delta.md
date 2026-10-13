FIX-FIRST  
Reviewer: GPT-6-Astra (high)

X = [C10X draft](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10x_telemetry_amendment_draft.md); Y = [C10Y draft](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10y_telemetry_amendment_draft.md).

**BLOCKING**

1. **T11 now rejects valid non-answer lines — X:218–223; Y:245–250.** Requiring T4 fields on “a line” makes headers, phases and lens records MALFORMED; `header` also lacks an expressly admitted schema. Exact replacement: **“Validate each line against its kind-specific schema. All kinds require T2 fields; only `answer` requires T4 fields and answer-key membership. Admit exactly one initial header under an explicitly defined header schema. Unknown kinds or fields fail against the applicable schema.”**

2. **Amendment M’s capture does not explicitly reach `fe_edit` — X:287–290.** Rebinding `H.upd_matrix_match_shape` reaches the harness, but the copied driver function resolves its unqualified name in its own globals ([frozen X:43](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10X_ENGINEPATH_PREREG.md:43)). Exact addition: **“Install the pass-through in the global binding actually resolved by each writer, including `fe_edit`, preserving and restoring every original binding in `finally`. Verify exactly one capture per expected layer per compared write, with explicit writer/check/recipe/arm/layer attribution; missing or duplicate captures invalidate the measurement.”** This preserves the verbatim solve and returned object.

**ADVISORY**

Prior-item disposition:

| Prior item | Closure evidence |
|---|---|
| 1 — off-mode contradictions | CLOSED: X:24–26,174,189; Y:26–28,201,216 |
| 2 — scorer transcription | CLOSED: X:72–76,132; Y:89–93,154 |
| 3 — inertness predicate | CLOSED: X:149–175; Y:171–202 |
| 4 — dashboard fallback | CLOSED: X:94–99; Y:111–116 |
| 5 — replication replacements | CLOSED: X:189–190,244–248; Y:216–217,268–274 |
| 6 — Y forecast | CLOSED as a design requirement: Y:189–197,220–226 |
| 7 — Y lens ordering | CLOSED: Y:50–56 |
| 8 — subprocess isolation | CLOSED: X:123; Y:143 |
| T11 advisory | Dispositions added: X:218–232; Y:245–259. Schema contradiction above remains. |

Amendment M is honestly dated and labelled a metric amendment (X:253–263). Its pre-cast fp32 tensor definition matches the frozen explicit representations; reductions move to CPU float64 while cache arithmetic and applied-weight equality remain unchanged (X:265–303). No hypothesis, arm, numerical threshold, floor ceiling, tolerance or verdict formula changes found. **Measured floors and resulting classifications can change**, as X:309 correctly acknowledges. Legacy fp32 values are report-only.

Frozen hashes match both supplied hashes. Filesystem inspection found exactly five review Markdown files matching `results/c10x_enginepath*`, **no matching directory**, and no `c10x_*`/`c10y_*` experiment files. This supports pre-observation status within the inspected namespace. P2 rationale confirmed at `EXPERIMENT_RUNBOOK.md:377`.

Read-only; no Python or tests. Requested reviewer header reproduced; runtime model/effort authentication remains UNVERIFIABLE.

