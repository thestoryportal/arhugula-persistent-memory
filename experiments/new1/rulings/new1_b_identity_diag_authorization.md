# D-NEW1-b identity diagnostic — operator authorization (2026-10-10T05:56Z)

Operator answered "Authorize diagnostic" to Astra option (a) (`new1_b_halt_astra.md`): ONE bounded diagnostic-only measurement.
- Compare normalized-covariance bytes/differences: NEW1 path (`tools/new1_geometry.py:138–146`, np.divide fp32) vs producer path (`memit_dry_run/memit/util/runningstats.py:499–511`, torch division).
- At most TWO native L4 fp32 CPU decompositions, one per arithmetic path, predeclared; report excluded count, projector SHA, every probe's relative error vs captured `l4.Pi_probe0–3`, threads/backend/torch provenance. Four probes = sampled discrepancy, not subspace distance.
- No adapter energies, no prediction verdict, no acceptance-rule amendment. Diagnostic permission is not launch permission.
- Caps: 600 s, 11 GiB observed RSS, fresh admission, nice 10; output < 1 MB, no dense tensor persistence; no retry.
