# NEW-1 authorized run — outcome note (MAESTRO29, 2026-10-11)

Tier: MATH-PROXY — a math estimate, not evidence. Astra's binding reading is pending; this note records what ran and what the frozen prereg says it means, nothing more.

## What ran

- One invocation of the operator's one-run authorization (`new1_launch_c4_20261011/new1_b2_one_invocation_authorization.md`, SHA-256 `221133dc…abea8`), launched from the niceness-0 tmux server `new1` at HEAD `6b89ae2009c94b5739b6b1b28d58cb7cfef70baa`. All 11 pinned hashes verified OK; the pinned paths were clean.
- Dispatch: `results/mathlab_staging/new1_dispatch_20261010T235738.2180209160Z/` (all pre-checks 2a–2i passed; dry admission `True [] []`). Authorization consumed at 23:57:40Z.
- Run: `results/mathlab_staging/runs/new1_20261010T235740.858576Z/`, admitted 23:57:40Z, finished 00:22:34Z (24 min 54 s of a 2,700 s cap). Supervisor niceness 0; worker observed at niceness 10.
- Disposition CLEAN (no live processes in the monitored worker/group — not a claim about the whole host); verdict_status COMPLETE; no stop; abort accounting 0/0, not an abort. Dispatch rc 3 = the conservative INVALID run envelope (below), not a failure.

## Result (from `finding.json`, SHA-256 `1b4dcd94…1f05`; source `geometry.json` `d3eca63a…b1bb`)

| Prediction | Outcome |
|---|---|
| H-COV | BOUNDARY-SENSITIVE (excluded-energy contrast NON-SPECIFIC) |
| H-TOP (secondary) | PASS |
| H-RANK | FAIL |
| H-OVERLAP | FAIL |

Run envelope `INVALID` is the encoding the frozen amendment requires for a BOUNDARY-SENSITIVE H-COV (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:212`): "encoded conservatively as INVALID in the stage/terminal envelope with no Boolean prediction gate."

## What the prereg says it means

- H-COV BOUNDARY-SENSITIVE → no geometry-specific queue recommendation (`:212`).
- H-OVERLAP FAIL / rank contrast absent → do not promote H-30/H-6 on a geometry argument; existing order stands; rank 64, a new model, or a C10X/C10Y/ASTRA rerun is not authorized (`:142`).
- H-TOP PASS supports the large-variance version only together with an H-COV PASS (`:139`); alone it changes nothing.
- `finding.json` records `queue_action: NONE — calibration/utility gated`. Net: **no queue change**.
- **NON-SPECIFIC** (Astra, recomputed from `geometry.json`): the excluded-energy shuffle difference |EXc(D)−EXc(shuf)| is ≤0.05 at every applicable cutoff on all five layers (L4 0.004207/0.004205, L5 0.005256, L6 0.001388, L7 0.029207, L8 0.013029). This independently blocks any semantic-specific interpretation (`:94,212`); it does not invalidate the geometry.
- BOUNDARY-SENSITIVE here means the robust aggregate failed: only L5 passes H-COV at every cutoff in its band (1/5, below the required same-layer 3/5). No layer's nominal result flips across cutoffs, so this is not an observed cutoff-induced reversal.
- Binding reading: `new1_outcome_astra.md` beside this note, VERDICT ACCEPT-WITH-CONDITIONS; both conditions are applied in this revision.

## Deviations, recorded plainly

1. **Quiet-host deviation (retained).** ~23:59Z, after admission had passed (23:57:40Z), MAESTRO briefly ran a Homebrew `python3` heredoc while drafting a builder brief. MAESTRO-reported: it lived under a second, wrote nothing and touched no run file; none of this is independently verifiable. The supervisor admits once (`tools/new1_supervisor.py:194-197`) and later gates are memory-only, but initial admission cannot certify that the host stayed quiet, and it did not. Recorded resource samples show no breach: minimum sampled available memory 20.152191 GiB against the 6 GiB floor; maximum sampled family RSS 8.643097 GiB (sampled extrema, not continuous guarantees). The nearby sequence is 23.173782 → 20.859085 → 21.417648 GiB, with worker RSS 3.770401 → 7.382309 GiB at the float64 L4 SVD gate (23:59:04); whether the external process contributed is unverified.
2. **`mv` warning.** The dispatch stdout (captured outside the dispatch directory, in MAESTRO's scratch `new1launch.out`) holds one `mv: … 2a.stderr: set owner/group (was: 501/0): Operation not permitted` line. MAESTRO's explanation, not verified from the dispatch capture: moving check 2a's stderr from `/private/tmp` onto the memit volume cannot carry the group. `2a.json` records successful directory creation; nothing indicates damaged numerical artifacts.
3. **Dashboard poll.** The status-bar GPU poll (Homebrew Python, not exempt) was paused for the run by swapping the `dashboard` session's `status-right` to a static string, then restored. `dashboard_status_restore_evidence.txt` beside this note records the saved pre-pause value's SHA-256 equal to the live value's after restoration (`8b099cf6…cad4`), captured 00:30:55Z.

## Storage

The 100 control `.npz` files (167,242,800 bytes, `controls/`) are gitignored bulk and stay on the memit bench; their SHA-256s are in `npz_bench_files.sha256` beside this note. Whether they go to Drive or are deleted is the operator's call.
