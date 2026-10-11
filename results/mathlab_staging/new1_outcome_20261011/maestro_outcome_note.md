# NEW-1 authorized run — outcome note (MAESTRO29, 2026-10-11)

Tier: MATH-PROXY — a math estimate, not evidence. Astra's binding reading is pending; this note records what ran and what the frozen prereg says it means, nothing more.

## What ran

- One invocation of the operator's one-run authorization (`new1_launch_c4_20261011/new1_b2_one_invocation_authorization.md`, SHA-256 `221133dc…abea8`), launched from the niceness-0 tmux server `new1` at HEAD `6b89ae2009c94b5739b6b1b28d58cb7cfef70baa`. All 11 pinned hashes verified OK; the pinned paths were clean.
- Dispatch: `results/mathlab_staging/new1_dispatch_20261010T235738.2180209160Z/` (all pre-checks 2a–2i passed; dry admission `True [] []`). Authorization consumed at 23:57:40Z.
- Run: `results/mathlab_staging/runs/new1_20261010T235740.858576Z/`, admitted 23:57:40Z, finished 00:22:34Z (24 min 54 s of a 2,700 s cap). Supervisor niceness 0; worker observed at niceness 10.
- Disposition CLEAN (no live processes); verdict_status COMPLETE; no stop; abort accounting 0/0, not an abort. Dispatch rc 3 = the conservative INVALID run envelope (below), not a failure.

## Result (from `finding.json`, SHA-256 `1b4dcd94…1f05`; source `geometry.json` `d3eca63a…b1bb`)

| Prediction | Outcome |
|---|---|
| H-COV | BOUNDARY-SENSITIVE |
| H-TOP (secondary) | PASS |
| H-RANK | FAIL |
| H-OVERLAP | FAIL |

Run envelope `INVALID` is the encoding the frozen amendment requires for a BOUNDARY-SENSITIVE H-COV (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:212`): "encoded conservatively as INVALID in the stage/terminal envelope with no Boolean prediction gate."

## What the prereg says it means

- H-COV BOUNDARY-SENSITIVE → no geometry-specific queue recommendation (`:212`).
- H-OVERLAP FAIL / rank contrast absent → do not promote H-30/H-6 on a geometry argument; existing order stands; rank 64, a new model, or a C10X/C10Y/ASTRA rerun is not authorized (`:142`).
- H-TOP PASS supports the large-variance version only together with an H-COV PASS (`:139`); alone it changes nothing.
- `finding.json` records `queue_action: NONE — calibration/utility gated`. Net: **no queue change**.
- Not yet checked by MAESTRO: the per-cutoff shuffle-specificity readout (`:212`). Astra reads it from `geometry.json`.

## Deviations, recorded plainly

1. ~23:59Z, after admission had passed (23:57:40Z), MAESTRO briefly ran a Homebrew `python3` heredoc while drafting a builder brief. It lived under a second, wrote nothing, and touched no run file. The supervisor admits once (`tools/new1_supervisor.py:194-197`); later gates are memory-only. Available memory never fell below 20.15 GiB against the 6 GiB floor; the one step down near that time (23.7 → 21.4 GiB at 23:59:04–06) coincides with the worker's own float64 L4 SVD gate at 23:59:04, where its RSS rose from 3.8 to 7.4 GiB. It breaks the keep-the-host-quiet practice and is reported, not excused.
2. The dispatch's stdout holds one `mv: … 2a.stderr: set owner/group (was: 501/0): Operation not permitted` line: moving check 2a's stderr from `/private/tmp` onto the memit volume cannot carry the group. The move succeeded and `2a.json` exists.
3. The dashboard status-bar GPU poll (Homebrew Python, not exempt) was paused for the run by swapping the `dashboard` session's `status-right` to a static string, and restored byte-identical after.

## Storage

The 100 control `.npz` files (167,242,800 bytes, `controls/`) are gitignored bulk and stay on the memit bench; their SHA-256s are in `npz_bench_files.sha256` beside this note. Whether they go to Drive or are deleted is the operator's call.
