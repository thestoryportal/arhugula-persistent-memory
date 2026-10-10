# D-ML-1 build review record

The brief explicitly requested GPT-6-Astra at high reasoning after the build. The parent used a fresh, read-only GPT-6-Astra/high reviewer, with no torch/model imports, GPU calls, harvest dispatch, edits or commits authorized. Earlier FIX-FIRST findings were addressed with saved RED regressions before fixes. Final reviewer output:

> Final delta review: accepted. No new defect found. Overall build acceptance remains BLOCKED on exact UV execution and completed production-shape RSS measurement.
>
> The context guard requires the frozen s0 record SHA and uses its literal /ctx; no substitution remains. Admission probe errors produce allowed=false, a failed admission gate, staged finding, and exit 3. Recorded verification: 60 tests PASS, plus 1 real DuckDB test PASS. Frozen prereg SHA remains unchanged.
>
> Document s0's dual role explicitly: its target/step-0 failures are seed-specific; loss of its authoritative context record refuses the shared context gate. This is a conservative interpretation of section 2.2's named context authority alongside its per-arm failure rule.
>
> No unsafe dispatch or incorrect source provenance found in these corrections. No imports, execution, or edits were performed beyond read-only inspection.

The independent test-plan reader used the documented weaker same-family fallback. Its original FIX-FIRST findings concerned real event integration, harvest serialization/manifests, full-shape RSS, immediate stop staging/preserved outputs, and observer order/return/exception cleanup. Those have explicit tests. It inspected saved outputs; it reran no tests. It identified the same unresolved UV/full-peak checks. Its 57-test snapshot preceded the final 60-test run; the report uses the later evidence.

Claude CLI auth was probed, not assumed absent: claude_auth_probe.txt records loggedIn=false, authMethod=none, exit 1. An earlier advisor wrapper invocation also refused without auth. There is no successful Claude review or out-of-family approval.

After the last Astra dispatch/provenance check, the builder added the prereg's non-gating injection-consistency reporting fields, verified by consistency_report_red.txt then the final 60-test suite. This small output-only delta does not modify any calibration gate. The later fixture-runner UV attempts validate staged refusal, not successful frozen execution. Neither later item is represented as an additional Astra review.
