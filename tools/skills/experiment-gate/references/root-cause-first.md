# Root-Cause First

For failures, stalls, or surprising results:

1. Reproduce the failure and capture the exact traceback/result path.
2. Locate the failing boundary before changing code.
3. Enumerate at least three hypotheses, including local harness error.
4. Apply one fix only.
5. Rerun the same gate.
6. Halt and write the diagnostic if the gate still fails.

Do not tune around a failure until the measurement frame and failing boundary are stable. A compatibility failure is not science evidence.
