# Metric Matching

Use the metric that can falsify the claim being made.

| Claim type | Binding metric | Common trap |
|---|---|---|
| Read correctness / DB readout | Top-1 or full-sequence exact match on held-out prompts | Using canonical prompt fit as if it proves held-out behavior |
| Multi-token value expression | Full-sequence exact match plus first-token and conditional full-given-first diagnostics | Reporting first-token success as value success |
| Storage-signature threshold | Margin/maxprob separation on the read surface being used | Treating margin inflation as native reliability |
| Distributional locality | JS/KL over the named token/probe distribution with CI | Comparing one arm by top-1 and another by distribution |
| Durability/retention | Retention on the same committed units after the stressor | Dropping failed/absent units from the denominator |
| Method-port faithfulness | Active easy-control behavior plus target/update trace parity | Treating token/no-op parity as active edit equivalence |

If the metric is an adjacent proxy, stop and rewrite the prereg. Secondary diagnostics can explain a result, but they cannot replace the binding metric after the run.
