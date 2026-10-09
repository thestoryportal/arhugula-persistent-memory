# D-ML-3 review fix handoff

User authorizes this persistence-only reviewer correction in the same D-ML-3 implementation round. Frozen prereg SHA verified: 85b389ec92248dbccf61d4ecc1de65f47bedf5ce99f88f17866f0db29d3e4bf8. Read results/mathlab_staging/dml3_impl_astra_r1.md and prereg section 15.

No implementation or test edits yet. Plan: collect original returned native scalar map and producer metadata before coverage validation; retain a separate returned layer map to avoid assigning overwritten scalars to duplicate occurrences; diagnostic sidecars retain occurrence-indexed operands and the separate original returned map. No recomputation. Failed writes remain diagnostic-only and HALT unchanged. Zero captures must still retain returned native map and metadata. Fsync failure must retain both raw stores.

Next: extend coverage persistence CPU tests RED first; then minimal harvest.py persistence patch; GREEN; full mathlab, dashboard, DuckDB, strict marimo with writable TMPDIR. Append dated D-ML-3 review fix section to build_report.md; preserve earlier bytes and Status. Reply D-ML-3 FIX DONE.

CPU only; no GPU/MPS, model load, harvest dispatch, commits, shared mathlab_events.py edit, or active step-2/first-harvest writes. Protected files inventoried in initial_scope.json; raw input trees read only. External HEAD changes may occur; do not mutate git. Old D-ML-3 implementation audit is results/mathlab_staging/dml3_impl_20261009T195833.138642Z/.

Existing Astra agent /root/mathlab_build_review approved the persistence plan. Final diff review still pending. Current-turn Graft one successful call saved 46,662 tokens ($0.02). Memory registry lines 50-51 and 55-58 used for scope rules, rollout 01a11e62-906b-7552-a35b-6087edcbe984; append required memory citation in final.
