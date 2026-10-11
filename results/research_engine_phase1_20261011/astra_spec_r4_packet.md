# Astra review — research-engine phase-1 spec, r4 (SR v2 against r3 T1–T7)

You are the program's independent cross-family reviewer. Work read-only: read and search only.

In spec r3 (`results/research_engine_phase1_20261011/astra_spec_r3_verdict.md`) you returned NO-GO on SR v1: T1–T4 blocking, T5–T7 conditions. MAESTRO35 wrote, without editing any reviewed file:

- `results/research_engine_phase1_20261011/science_reservation_contract_v2.md` (**SR v2**, sha256 a384d254061a8503954c8c872ecba45b91418e6452153f208aa8d54d8b733f48), superseding SR v1 (ee6f0c3a…).
- `results/research_engine_phase1_20261011/phase1_spec_v4.md` (sha256 af39b72dfdaad5ddde90aac9834335d24cc3fe22b2ed4cbfabebbf263a4a3413): v3 + SR v2 wiring + commissioning step + identity baseline; change table §16. See every change with `diff phase1_spec_v3.md phase1_spec_v4.md`.
- Evidence: `preinstall_identity_20261011.tsv` (versions + bottle sha256, nine formulae), `duckdb_1.5.5_hashes.txt`, `provisioning_dryrun_20261011.txt`, `operator_answers_20261011T0518Z.md` (the operator approved the reservation step and the six shared-dependency upgrades).
- Facts MAESTRO probed on this host, 2026-10-11: `/usr/bin/lockf -k` and Python `fcntl.flock` exclude each other on `/Volumes/memit` (APFS), both directions. `new1_supervisor.py:532` and `v13_launcher.py:47,87` start children with `start_new_session=True`. `ps -E` shows no environment here, so an env marker was rejected.

Review for:
1. T1–T7: for each, RESOLVED | PARTIAL | OPEN, with the SR v2 or v4 line that resolves it.
2. New defects SR v2 introduced: the writer enforcing termination inside `pending`; the lock-timeout path (enforce, then publish); registry on the internal volume; `release` gated on the unchanged whole-host classifier; controller-thread watcher-loss handling; the 28 s / ~30 s arithmetic in SR §0 G2 and §5. Look for any interleaving that admits or publishes after a `pending` publish, any false IDLE, and any unbounded wait.
3. Are AC17/AC21 and SR §7 cases 1–15 checkable and sufficient for the guarantees claimed, with host termination still only provable by §8 commissioning?
4. Did v4 weaken or drop any v3 requirement, or change a section §16 does not name?
5. Apart from implementation, is anything left before freeze?

Deliverable: Markdown to stdout, exactly:
```
# Astra spec r4 verdict — research-engine phase 1
Verdict: GO | GO-WITH-CONDITIONS | NO-GO
## r3 findings status
T1. RESOLVED | PARTIAL | OPEN — <evidence: file:line>
…
## Findings
U1. [severity: blocking|condition|note] <defect>. Evidence: <file>:<line>. Consequence: <...>.
## Required before freeze
## What I checked and did not check
```
Ground every finding in a line you read. Do NOT re-review R2–R4 or the operator's choices, or propose style rewrites.
