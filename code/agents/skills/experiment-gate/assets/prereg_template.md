# {{D_ID}} Preregistration

## Hypothesis

State the falsifiable claim and the F1 condition or runbook section 0.3 falsifier it advances.

## Binding Metric

Name the primary metric and why it matches the claim. Use top-1/full-sequence exact match for read correctness, margin/probability separation for storage-signature thresholds, and JS/KL only for distributional claims.

## PASS / PARTIAL / FAIL / INVALID Thresholds

- PASS:
- PARTIAL:
- FAIL:
- INVALID:

## Power / MDE

Record the planned sampling unit, cluster count, item count, expected between-order noise, and the exact `tools/power.py` command or reason a power calculation is not applicable.

## Confounders And Controls

List every applicable confounder and the concrete control or diagnostic that will close it.

## LAW / Inertness Gates

State engine fingerprint checks, LAW#5 inertness/null edit criteria, source-read requirements, and one-fix-then-halt boundaries.

## Method-Port Faithfulness

For external method ports, name upstream repo/commit, upstream hparams, deviations, active trace fields, easy controls, behavior thresholds, and the hard-case licensing rule.

## Artifacts

- Runner:
- Result JSON:
- Log:
- Stats report:
- Method-port packet:

## Advisor / Cross-Family Review

Record required review points before harness/test criteria, after failures or stalls, before approach changes, and before verdict.

## Abort Criteria

List conditions that make the run INVALID or require halting before further edits.
