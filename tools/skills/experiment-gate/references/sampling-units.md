# Sampling Units

The reliability unit for edit experiments is usually `(held-out set) x (edit order)`, not an individual prompt. Order/seed swings dominate many results, so iid/Wilson intervals under-cover.

Minimum expectations:

- Use `tools/power.py` before a run when a reliability or promotion claim depends on effect size.
- Emit `per_unit` rows in result JSON whenever the claim needs cluster statistics. Follow `tools/STATS_LOGGING_CONVENTION.md`.
- A single seed/order can support a scoped diagnostic or within-experiment contrast; it cannot support a broad reliability claim.
- `tools/stats.py` and `tools/experiment_gate.py check-result` should refuse aggregate-only false rigor.

Useful commands:

```bash
python3 tools/power.py size --metric prop --p0 70 --effect 20 --items 8 --swing 50 --target-power 0.8
python3 tools/stats.py from-result results/<file>.json
python3 tools/experiment_gate.py check-result results/<file>.json
```
