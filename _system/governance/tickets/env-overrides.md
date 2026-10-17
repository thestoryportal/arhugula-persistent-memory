# Environment overrides
Part of the tickets guide. Router: `_system/governance/TICKETS.md`. Roots (L, M, S, W, TD, MEM, HO): `00-roots-and-roles.md`.

Defaults are the live values; set one only for a test or a deliberate one-off, and say so in the ledger row.

| script | variable | default |
|---|---|---|
| ship.sh | TRAIN | 1 (ready marker); 0 lands alone; any other value exits 2 (:33, :36) |
| ship.sh | TICKETS, ASTRA, PREREVIEW, LAND | `python3 -B $S/scripts/tickets.py`, `$L/tools/astra.sh`, `$L/tools/prereview.sh`, `$L/land.sh` (:13-15, :24) |
| ship.sh | SAMPLER, COMPUTE_LAST | `M/.venv/bin/python -B M/code/agents/compute_sample.py`, `$L/tools/compute.last` (:22-23) |
| ship.sh | GH, GIT, HYGIENE, GUARD | gh, git, `M/.venv/bin/python -B` git_hygiene.py, the same for guard_mutants.py (:25-28) |
| ship.sh | TESTRUN, LANES | the built-in testrun, `/Volumes/memit/llmdb-lanes` (:31-32) |
| ship.sh | ASTRA_MAX, ASTRA_LOAD_MAX, ADMIT_SLEEP | 6, 10, 15 s (:150, :129, :159) |
| ship.sh | LOCK_SLEEP, TRANSIENT_SLEEP | 10 s, 20 s (:446, :70) |
| ship.sh | PROBE | record; `gate` stops on the prober's verdict; any other value stops 2 (:20, :238) |
| ship.sh | PROBER | `env REVIEW_OUT=probe REVIEW_MODEL=$PROBE_MODEL REVIEW_EFFORT=$PROBE_EFFORT REVIEW_PROMPT=S/references/prober.md $ASTRA`; set but empty runs no prober (:19) |
| ship.sh | PROBE_MODEL, PROBE_EFFORT | gpt-6.1-sol, medium (:19) |
| train.sh | TRAIN_M, GATE (also GH, GIT, HYGIENE, LANES, LOCK_SLEEP, TRANSIENT_SLEEP) | M, `M/.venv/bin/python -B M/code/ops/git/git_merge_gate.py` (:24-29) |
| astra.sh | REVIEW_MODEL, REVIEW_EFFORT, REVIEW_OUT, TD | gpt-6-astra, high, verdict, `L/recut` (:9, :12) |
| astra.sh | REVIEW_PROMPT | unset (the packet); a file whose text replaces the packet (:5, :9) |
| test_ship.sh, test_train.sh | SHIP_SRC, TRAIN_SRC | the sibling script, or its `.new` when the suite is the staged copy (test_ship.sh:10, test_train.sh:9-11) |

