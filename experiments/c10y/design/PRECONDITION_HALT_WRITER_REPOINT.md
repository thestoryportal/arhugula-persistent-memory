# Precondition for the next c10y authorization: repoint the halt-diagnostic writer

The next c10y authorization brief must repoint the halt-diagnostic writer of `code/lab/track_c/c10y_directdw_arms.py` and add a selftest for it, before any c10y run. Put both in that brief as prerequisites, together with the pin repair.

## The defect

`c10y_directdw_arms.py:1290-1295,1600` writes halt diagnostics to `architecture_profile/`. Since the ICM v2 restructure, git ignores that folder (group B guard, commit `efef4529`). The governed location is `experiments/<id>/runs/<slug>/halts/` (`_system/governance/DISCIPLINE.md`, halt discipline). A halt diagnostic written there now does not enter git.

## Why the restructure did not fix it

MAESTRO ruled to leave the script unchanged in the restructure merge (Ruling 3, group A, in `knowledge/analyses/icm-v2-restructure/astra-g7-packet.md`). The restructure already changed the script's hash, so no current pin covers it. Every c10y run needs new pins and a prospective authorization anyway. The repoint belongs in that same authorization.

## Why no c10y run can start before the repoint

Astra high confirmed Ruling 3 (`knowledge/analyses/icm-v2-restructure/astra-g7-verdict.md`, Rulings, item 3). It ran the read-only `c10y_directdw_arms.preflight(env={})` at `4e679b15`. Preflight refused with `Halt: PREREG SHA MISMATCH`. `main()` calls preflight before launch authorization and before it creates a worker. So the current entry point cannot reach calibration until someone repairs the pins. The brief that repairs the pins must also carry the repoint and its selftest.

## Other writers of the same kind

Seven closed experiments (group B) also write to `architecture_profile/`: `b1_size_dose_response.py`, `d1_threshold_instrument.py`, `c10v_layerpick_arms.py`, `c10w_oracle_step0.py`, `c10x_enginepath_arms.py`, `c10z_astra_arms.py`, `c10s_sharedz_read.py` (follow-up mode). Their code stays. A re-run of any of them needs a new authorization, and that brief carries the repoint. The full list with line numbers is in the packet, Ruling 3.
