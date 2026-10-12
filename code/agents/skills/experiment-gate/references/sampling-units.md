# Sampling Units

The reliability unit for edit experiments is usually `(held-out set) x (edit order)`, not an individual prompt. Order/seed swings dominate many results, so iid/Wilson intervals under-cover.

Minimum expectations:

- Use `code/lab/analysis/power.py` before a run when a reliability or promotion claim depends on effect size.
- Emit `per_unit` rows in result JSON whenever the claim needs cluster statistics. Follow `code/lab/analysis/STATS_LOGGING_CONVENTION.md`.
- A single seed/order can support a scoped diagnostic or within-experiment contrast; it cannot support a broad reliability claim.
- `code/lab/analysis/stats.py` and `code/gates/experiment_gate.py check-result` should refuse aggregate-only false rigor.

Useful commands:

```bash
python3 code/lab/analysis/power.py size --metric prop --p0 70 --effect 20 --items 8 --swing 50 --target-power 0.8
python3 code/lab/analysis/stats.py from-result experiments/<id>/runs/<slug>/<file>.json
python3 code/gates/experiment_gate.py check-result experiments/<id>/runs/<slug>/<file>.json
```
