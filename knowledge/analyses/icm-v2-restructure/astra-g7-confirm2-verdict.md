VERDICT: NO-GO

## 1. BLOCKING 1 — anchor identity

**BLOCKING — partially fixed; existing-fragment resolution can still select the wrong section.**

The original insert and reorder script now passes. Regeneration reads the pinned headings at [build_index.py:196](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/build_index.py:196), and both mutations preserve the committed map.

Reran the prior verdict’s script with:

```sh
LLMDB_ROOT=$PWD PYTHONPATH=code .venv/bin/python -B -c '<prior insert/reorder script>'
```

Output:

```text
insert map_unchanged = True
INDEX CLEAN
check_rc = 0
a1 -> a1--batch-vs-sequential-write--done--pass-robust-evidencecorpus14-d-a1-1
a2 -> a2--relation-balanced-in-solve-sentinels-3-disjoint-pools--done--partial-strong-directional-evidencecorpus15-d-a2-1
reorder sections map_unchanged = True
INDEX CLEAN
check_rc = 0
a1 -> a1--batch-vs-sequential-write--done--pass-robust-evidencecorpus14-d-a1-1
a2 -> a2--relation-balanced-in-solve-sentinels-3-disjoint-pools--done--partial-strong-directional-evidencecorpus15-d-a2-1
```

However, [resolve_path.py:84–89](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/resolve_path.py:84) checks only fragment membership. Inserting another A1 heading **before** the historical section gives the new section the pinned fragment; the original section receives an additional `-1`. The resolver silently selects the new section.

Reproduction, entirely in memory; the second case also answers question 3:

```sh
LLMDB_ROOT=$PWD PYTHONPATH=code .venv/bin/python -B -c '
import os
from pathlib import Path
from unittest.mock import patch
from state import build_index as b, resolve_path as r
root = Path(os.environ["LLMDB_ROOT"])
p = root / "program/runbook/08-experiment-decision-tree-tracks-af.md"
text = p.read_text()
rows = b.read_anchor_map((root / "_index/anchor-map.tsv").read_bytes(), root)
key = next(k for k in rows if k[0] == "program/EXPERIMENT_RUNBOOK.md" and k[1].startswith("a1--"))
pinned = rows[key][1]
heading = next(h for h,s in r.heading_entries(text.splitlines()) if s == pinned)
pos = text.index(heading)
cases = {
    "duplicate": text[:pos] + heading + "\nNEW SECTION; NOT HISTORICAL A1.\n\n" + text[pos:],
    "restore": text.replace(heading, heading.replace("evidence/CORPUS/", "CORPUS/"), 1)
}
read = Path.read_text
for name, changed in cases.items():
    with patch.object(Path, "read_text", lambda q,*a,**k: changed if q == p else read(q,*a,**k)):
        live = list(r.heading_entries(changed.splitlines()))
        print(name, "old_slug_exists =", key[1] in {s for h,s in live})
        try:
            fragment = r.resolve("#".join(key)).partition("#")[2]
            print("returns_pinned =", fragment == pinned)
            print("original_A1_now =", [s for h,s in live if h == heading][-1])
            print("returned_body =", changed.split(heading + "\n", 1)[1].splitlines()[0])
        except ValueError as e:
            print(e)
'
```

Output:

```text
duplicate old_slug_exists = False
returns_pinned = True
original_A1_now = a1--batch-vs-sequential-write--done--pass-robust-evidencecorpus14-d-a1-1-1
returned_body = NEW SECTION; NOT HISTORICAL A1.
restore old_slug_exists = True
Unknown anchor for program/EXPERIMENT_RUNBOOK.md: a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1; heading changed after the pin
```

Regeneration and `b.main()` with `--check`, under these same in-memory mutations, also returned:

```text
map_unchanged = True
INDEX CLEAN
check_rc = 0
```

**Required correction:** detect ambiguous or reassigned heading identity and reject it, or preserve a durable section identifier. Freezing the mapping does not freeze what a live fragment identifies.

## 2. BLOCKING 2 — archive readers

**NON-BLOCKING — fixed. Both corrected reader lines are true, and every cited file:line matches.**

Reviewed [_archive/CONTEXT.md:6](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/_archive/CONTEXT.md:6) and [_archive/code/CONTEXT.md:6](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/_archive/code/CONTEXT.md:6).

Command:

```sh
rg -n '_archive/|return \{name: sha256_file' \
  code/lab/track_c/c10u_mint2_arms.py \
  code/apps/dashboard/test_dashboard_queue.py \
  code/apps/dashboard/test_dashboard_storage.py \
  code/ops/backup/test_backup_gdrive_addendum.py \
  code/tests/test_dashboard_host_runner.py \
  code/gates/closeout_fingerprints.json
```

Verified output correspondence:

| Citation | Actual source |
|---|---|
| `c10u_mint2_arms.py:25` | Lists `_archive/code/closed-runners/c10u_mint2_p4.sh`. |
| `c10u_mint2_arms.py:82` | Returns `{name: sha256_file(root / name) for name in [*SOURCE_FILES, *engine]}`. |
| `test_dashboard_queue.py:21,623,898` | All name `_archive/projects/dashboard/dashboard_queue_build_20261011T014430Z`. |
| `test_dashboard_storage.py:26` | Names `_archive/projects/dashboard/dashboard_storage_mb22_20261010T192500Z`. |
| `test_backup_gdrive_addendum.py:1512` | Names `_archive/projects/backup-gdrive/backup_gdrive_mb21_20261010T191747Z/mb14_fixture`. |
| `test_dashboard_host_runner.py:11` | Names `_archive/projects/dashboard/dashboard_audit_20261010/fix_20261010T234721Z`. |
| `closeout_fingerprints.json:181` | Names `_archive/projects/new1-builds/new1_v2_build_report.md` as `source`. |

Executing only the AST-extracted source-list and hashing definitions, using the required Python environment, confirmed the archived runner is read:

```text
_archive/code/closed-runners/c10u_mint2_p4.sh 4271f5ce8152f9ab11b6065650394b6eaee62d8b7d741f015c4f8066f632af7f
```

## 3. Statements and tests in the diff

**NON-BLOCKING — one new test deliberately expects an otherwise valid historical fragment to be lost.**

At [test_resolve_path.py:167–174](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/test_resolve_path.py:167), `test_old_slug_cannot_rescue_changed_pinned_heading` restores `CORPUS/14` in the same heading, leaves the section’s body intact, and expects exit code 2.

The `restore` case above independently confirms:

```text
restore old_slug_exists = True
Unknown anchor ...; heading changed after the pin
```

Thus **yes**, the test expects rejection even though the historical fragment again exists on the original section. That matches the stated pinned-only rejection rule, so it is not an independent implementation mismatch. It does prevent claiming that every surviving historical alias is preserved.

The new insert/reorder tests correctly require preservation for their specific mutations. The changed-anchor pin test’s two pairs also passed its assertions when evaluated in memory. Neither establishes protection against the duplicate-heading case in question 1.

Read-only destination tests:

```sh
LLMDB_ROOT=$PWD PYTHONPATH=code .venv/bin/python -B \
  -m unittest state.test_resolve_path.DestinationFragmentTests -v
```

Output:

```text
Ran 2 tests in 28.627s
OK
517 rows checked and 0 missing
```

I did not run the fixture-writing test classes. No additional false statement was found in the six-file diff.

## 4. Ruling 4 — merge fitness

**BLOCKING — reject Ruling 4 for this candidate.**

The archive-reader finding is resolved. The original insertion/reordering failures are resolved. The broader anchor-identity finding remains: an ordinary duplicate-heading insertion can redirect an old link to another section while the fragment exists, regeneration remains unchanged, and `--check` reports `INDEX CLEAN`.

Reviewed only `9e6d51dc..5b26b249`. Final HEAD:

```text
5b26b249ce3769d4a5be25db2a3e7bf196c2bb2f
```

`git status --porcelain=v1` returned no entries. No files were edited; no model or GPU work ran.