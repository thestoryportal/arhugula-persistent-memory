# Stage 2 — Cut (`tickets.py cut ... --base`)
Part of the tickets guide. Router: `_system/governance/TICKETS.md`. Roots (L, M, S, W, TD, MEM, HO): `00-roots-and-roles.md`.

```sh
git -C /Volumes/memit/llmdb-lanes/base checkout -q --detach origin/master   # refresh the base first
python3 -B $S/scripts/tickets.py cut TD/PLAN.md TD/tickets --base /Volumes/memit/llmdb-lanes/base
```

- `--base` is required and must be the clean detached checkout `/Volumes/memit/llmdb-lanes/base`, never M: M is always dirty, and the cut refuses a base with uncommitted changes. The base is refreshed by hand only; a stale base judges "the test fails on the base" against an old master, so refresh it before every cut [R8] [G18].
- The cut runs every step's test on the base (600 s each) and refuses one that already passes. When it refuses, the test is not testing the change: name a new test class, or give a follow-up its own test file [R9]. Its other refusals (more than 4 files, a third writer, two parallel tickets on one file, a cycle, a trivial test, an oversized ticket, an astra step without its own new test file) are listed in S/SKILL.md §2.
- The output dir must be empty. Keep a superseded cut beside it as `tickets.cutN-superseded` rather than deleting it.
- On a new plan, show the operator the cut output (a few tickets) before GO [R13].
- The cut checks neither Stage 1's (`01-plan.md`) frozen-suite check nor its size rule. Do both before GO on a cut, and log one `ruling` row per TD: `pre-dispatch: frozen suites <none, or each hit and its ruling>; size <ok, or the split>` [R54] [R55].
- After a hand edit of a ticket file, run `python3 -B $S/scripts/tickets.py check TD/tickets --base /Volumes/memit/llmdb-lanes/base`.
- Plain `check` counts every ticket, so it refuses a third ticket that writes a hub file two merged tickets already wrote (tickets.py:180-190). Pass `--merged T316,T317` (comma-separated, tickets.py:294) to count only unmerged tickets in the writer-width limit (`MAX_SERIAL`) and the own-test rule: `tickets.py check TD/tickets --merged T316,T317`. `ready` takes the same `--merged` list.
- `tickets.py close` needs no `--merged`: it takes the merged set from `origin/<into>` commit subjects that match `^T###:` and have a ticket JSON (tickets.py:222-232).
- `tickets.py ready TD/tickets --merged T316,T317 --running T318` lists the tickets whose deps have merged. Both lists are comma-separated (tickets.py:286-287), and an unknown `--merged` id fails (tickets.py:214-215). Pass every dispatched, unmerged ticket in `--running` so nothing is dispatched twice.
- The cut writes `TD/tickets` with one `TD/tickets/<T>.json` per step (keys id goal plan approval write deps test out astra rules, plus reads).

