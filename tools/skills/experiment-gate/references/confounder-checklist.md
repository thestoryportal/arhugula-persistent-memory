# Confounder Checklist

List applicable confounders in the prereg and name the control before running.

| Confounder | How it fakes a result | Required control |
|---|---|---|
| Metric mismatch | A proxy improves while the real contract fails | Bind the metric to the claim before the run |
| Under-editing vs redistribution | Lower damage looks like better locality because the edit got weaker | Expression floor, delta norms, within/cross direction, sham/null control |
| Margin inflation | Edited facts look stronger than native because `compute_z` inflated confidence | Report native/edited margins separately; do not claim native equivalence |
| Denominator/survivorship | Failed edits vanish from later metrics | Report attempted, landed, retained, and evaluated denominators |
| K-vs-C sub-batch confound | Chunk count is mistaken for chunk size | Vary total N and chunk size independently where the claim depends on it |
| Pre-state conditioning | Screened-easy pools are treated as general pools | Record screening criteria and report scope as screened-only |
| Context reliance | Context prefix carries the answer, not the edit | Compare held-out prompt alone vs canonical/context-prefix diagnostics |
| Method-port drift | Local hybrid is interpreted as upstream method behavior | Run method-port faithfulness gate before hard cases |

Any open preregistered confounder caps the claim at PARTIAL/CONFOUNDED until resolved.
