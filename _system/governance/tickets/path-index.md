# Path index (for trace.py)
Part of the tickets guide. Router: `_system/governance/TICKETS.md`. Roots (L, M, S, W, TD, MEM, HO): `00-roots-and-roles.md`.

`L/w1opt/staged/tickets-doc/trace.py --doc` checks that every workflow file and every path the scripts name appears in the guide (`TICKETS.md` plus every `tickets/*.md`, read as one text: command below). These are the strings that are not workflow stations, listed so the check can pass; what each one is, is in INVENTORY.md §2:
- Roots as the scripts name them: `L`, `M`, `L/tools`, `L/tools/ready`, `L/tools/ready/`, `L/tools/ready/claimed`, `L/tools/ready/claimed/`, `TD/reviews/<T>/`, `L/w1opt/staged/<STEP>/*.new`.
- Script-internal forms: `/Volumes/memit/llmdb-lanes/tk-<mk>` (train.sh:97), `/Volumes/memit/llmdb-lanes/tk-<T>/<f>` (ship.sh 1b existence check), `L/tools/ship.sh<SUF>`, `L/tools/train.sh<SUF>`, `/<v>` (the `${P//"{{$k}}"/$v}` substitution at astra.sh:25, read as a path); from verify_ticket.sh, spot.sh and combined.sh: `/Volumes/memit/llmdb-lanes/tk-<T>/code`, `/Volumes/memit/llmdb-lanes/tk-<t>/<f>`, `/private/tmp/claude-501/combined.XXXXXX`, `/private/tmp/claude-501/spot-<T>.XXXXXX`, `/private/tmp/claude-501/v-<T>.XXXXXX`, `L/w1opt/followup-318/tickets/<T>.json`.
- System paths: `/bin/sh`, `/bin/zsh`, `/usr/bin/env`, `/dev/null`, `/bin/mkdir`, `/bin/rmdir`, `/bin/mv`, `/var`, `/private/var`.
- Stub-suite fixture strings (not paths on disk): `/d`, `/gone`, `/l/tk-T900`, `/pull/41`, `/tmp/elsewhere`, `/x`, `/astra.slot.1`, `/bin/sleep`, `/stub.pids`, `/stub.ready` (the last four in test_ship.sh since Step 326).

The check, from cwd M (preamble in `00-roots-and-roles.md`; the glob takes every guide file, so a new one is checked without editing this command):

```sh
cat $M/_system/governance/TICKETS.md $M/_system/governance/tickets/*.md > "$TMPDIR/tickets-guide.md"
python3 -B -I $L/w1opt/staged/tickets-doc/trace.py --doc "$TMPDIR/tickets-guide.md"; echo "trace rc=$?"
```
