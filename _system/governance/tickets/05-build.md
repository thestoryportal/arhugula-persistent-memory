# Stage 5 — Build (builder, then MAESTRO verifies)
Part of the tickets guide. Router: `_system/governance/TICKETS.md`. Roots (L, M, S, W, TD, MEM, HO): `00-roots-and-roles.md`.

The builder follows S/references/worker.md: write list only; RED (the test fails for the reason the step names, else `blocked`); GREEN; one fix, then `halted`; no commit.

- Revert check on every ticket, astra or not: guard_mutants with `--base "$(git merge-base HEAD origin/master)"` and a new `--out` per run (the tool never overwrites one). Each survivor gets a killing test or a reason in the reply; MAESTRO alone allow-lists. The ship gate runs the same command and stops on any survivor (worker.md:10-11) [R27]. `M/code/ops/review/guard_mutants.py`: one mutant per guard (raise-remove, flag-drop, regex-zero, except-class, except-remove, negate-if, write-loop) in fd-safe scratch copies; exit 0 all killed or allowed, 1 a survivor, 2 a refusal.
- Builder revert runs that use `subprocess.run(shell=True, timeout=...)` orphan grandchildren that later block hygiene; use exec, or a timeout that ends the whole run [R34].
- Builders use `M/code/tests/fault_kit.py` attacks and, for filesystem tools, `M/code/ops/migrate/fdsafe.py` helpers (wave-1 rulings).

The builder says GREEN. You will think *"done, ship it."* That is the moment to verify instead, because the builder's GREEN was on its own TMPDIR and its own reading of the step:
- run the ticket test yourself on the lane, on the host TMPDIR (`/var/folders/...`), not only TMPDIR=/private/tmp, and expect Linux CI to run it once more [R36];
- read `git -C <lane> status --porcelain` against the write list;
- read the kill table, and check the gate's mutant count per file: master's gate made 0 mutants in `mutant_ops/base.py`, so "0 survived" there proved nothing (HO/HANDOFF-STEP59.md:44);
- log a `verified` row (`ledger-and-metrics.md`).

`L/tools/verify_ticket.sh` runs most of this list for a wave-b lane: the ticket test twice on the host TMPDIR and once on /private/tmp, the skip check, porcelain against the write list, the gate as written and four existing suites [G31].

