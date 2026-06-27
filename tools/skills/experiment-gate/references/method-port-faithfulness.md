# Method-Port Faithfulness

External method ports need a source-faithful active easy-control gate before hard-case science.

Required packet fields for `tools/experiment_gate.py audit-method-port`:

- `upstream_commit`
- `upstream_hparams`
- `declared_deviations`
- `active_trace`
- `easy_controls`
- `behavior_thresholds`
- `hard_case_licensed`

Required `active_trace` fields:

- `token_ids`
- `lookup_or_edit_positions`
- `target_norms`
- `delta_norms`
- `update_norms`
- `logit_deltas`
- `behavior`

Rules:

- Token alignment and no-op/Law#5 inertness are necessary, not sufficient.
- Easy controls must pass active behavior before any hard case is licensed.
- Every local deviation from upstream must be declared before interpretation.
- If the port fails before behavior, label it diagnostic/compatibility, not method evidence.
- One clear fix, rerun the same easy-control gate, then halt with the diagnostic if it still fails.

Packet skeleton:

```json
{
  "upstream_commit": "...",
  "upstream_hparams": {"...": "..."},
  "declared_deviations": ["..."],
  "active_trace": {
    "token_ids": "...",
    "lookup_or_edit_positions": "...",
    "target_norms": "...",
    "delta_norms": "...",
    "update_norms": "...",
    "logit_deltas": "...",
    "behavior": "..."
  },
  "easy_controls": [{"name": "A1", "status": "PASS"}],
  "behavior_thresholds": {"control_para_full_min": 0.8},
  "hard_case_licensed": false
}
```
