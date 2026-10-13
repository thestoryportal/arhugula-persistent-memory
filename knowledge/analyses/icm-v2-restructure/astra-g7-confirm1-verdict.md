VERDICT: NO-GO

## 1. Resolver fragments

**NON-BLOCKING — the original two missing fragments are fixed at `9e6d51dc`.**

Command, with the required environment and interpreter:

```sh
LLMDB_ROOT=$PWD PYTHONPATH=code .venv/bin/python -B \
  -m unittest state.test_resolve_path.DestinationFragmentTests -v
```

Output:

```text
Ran 2 tests in 29.352s
OK
517 rows checked and 0 missing
```

An in-memory `build_anchor_map()` regeneration also matched the committed map byte-for-byte.

**BLOCKING — positional alignment can lose valid aliases or silently select the wrong section.** See [build_index.py:200](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/build_index.py:200), especially lines 202–206.

I tested two changes entirely in memory:

1. Insert `### New close-out heading` immediately before A1.
2. Exchange the complete A1 and A2 sections, preserving their contents.

For each mutation, I regenerated the map, supplied those bytes to the resolver and checker, and resolved the historical A1/A2 anchors. The command was `LLMDB_ROOT=$PWD PYTHONPATH=code .venv/bin/python -B -c` with this body:

```python
import os, sys
from pathlib import Path
from unittest.mock import patch
from state import build_index as b, resolve_path as r

root = Path(os.environ["LLMDB_ROOT"])
mapping = b.read_path_map((root / "_index/path-map.tsv").read_bytes())
part = root / "program/runbook/08-experiment-decision-tree-tracks-af.md"
text = part.read_text()
a, z, end = [text.index("#### " + label)
             for label in ("A1 ", "A2 ", "A2b ")]
cases = {
    "insert": text[:a] + "### New close-out heading\n" + text[a:],
    "reorder sections": text[:a] + text[z:end] + text[a:z] + text[end:]
}
read_text, read_bytes = Path.read_text, Path.read_bytes
for name, changed in cases.items():
    with patch.object(Path, "read_text", lambda p, *a, **k:
                      changed if p == part else read_text(p, *a, **k)):
        data = b.build_anchor_map(root, mapping)
        rows = b.read_anchor_map(data, root)
        aliases = [key for key in rows
                   if key[0] == "program/EXPERIMENT_RUNBOOK.md"
                   and key[1].startswith(("a1--", "a2--"))]
        with patch.object(Path, "read_bytes", lambda p, *a, **k:
                          data if p == root / "_index/anchor-map.tsv"
                          else read_bytes(p, *a, **k)):
            print(name)
            with patch.object(sys, "argv", ["build_index.py", "--check"]):
                print("check_rc =", b.main())
            for key in aliases:
                try:
                    dest = r.resolve("#".join(key))
                    print(key[1][:2], "->", dest.partition("#")[2])
                except ValueError:
                    print(key[1][:2], "-> Unknown anchor")
```

Output:

```text
insert
INDEX CLEAN
check_rc = 0
a1 -> Unknown anchor
a2 -> Unknown anchor
reorder sections
INDEX CLEAN
check_rc = 0
a1 -> a2--relation-balanced-in-solve-sentinels-3-disjoint-pools--done--partial-strong-directional-evidencecorpus15-d-a2-1
a2 -> a1--batch-vs-sequential-write--done--pass-robust-evidencecorpus14-d-a1-1
```

Thus:

- **Can close-out cause an unrepairable `--check` failure?** Not in the tested case: `--check` stays green. It validates map structure but does not check destination fragments or regenerate the anchor map (`build_index.py:240–246`).
- **Can regeneration break surviving historical links?** Yes. Adding one heading loses both aliases; regenerating again cannot recover them.
- **Can alignment return an existing but wrong section?** Yes. Reordering the sections swaps A1 and A2.

The new test at `code/state/test_build_index.py:256–273` explicitly expects the insertion case to lose both aliases. That preserves the defect as expected behavior.

**Required fix:** preserve explicit historical-to-current section identity; do not infer identity from equal-length replacement blocks. Verify identity as well as fragment existence.

## 2. Guide text and sweep

**NON-BLOCKING — original findings 2–4 are fixed.** The changed citations are correct.

I read the cited lines directly and ran:

```sh
LLMDB_ROOT=$PWD PYTHONPATH=code .venv/bin/python -B \
  code/state/render_state.py --check
```

Output:

```text
[ok    ] program/STATUS.md
[ok    ] _index/program-state.md
[ok    ] program/scorecard.md
✅ all generated views current.
```

Verified correspondence:

| Changed guide | Supporting source |
|---|---|
| `DISCIPLINE.md:48–49`; `OPERATING-MODEL.md:15,80` | `render_state.py:18–20` names exactly those three targets. |
| Former-entry-point citations | `README.md:123`, runbook entry part `:41`, bootstrap `:4`, and `PROGRESS.md:162` contain the stated links. |
| `code/tests/CONTEXT.md:6` | CI `:43–44` names the fixture step and `code/tests` discovery command. |
| `code/apps/CONTEXT.md:6`; `code/lab/CONTEXT.md:6` | CI `:45–46` names the stated modules. |
| `WORKFLOWS_OVERVIEW.md:12,65,130` | `DISCIPLINE.md:120,128,134` contains the cited rule headings. |
| Four knowledge reader fixes | `connected_papers_index.py:28–32` recursively reads Markdown and excludes the named index paths. |

**BLOCKING — two claims in the requested reader sweep remain false.**

- [`_archive/CONTEXT.md:6`](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/_archive/CONTEXT.md:6): “Only `_archive/projects/` has a reader.”
- [`_archive/code/CONTEXT.md:6`](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/_archive/code/CONTEXT.md:6): “Reader search: none found.”

Command:

```sh
rg -n 'SOURCE_FILES|_archive/code/|return \{name: sha256_file|with open\(path' \
  code/lab/track_c/c10u_mint2_arms.py
```

Relevant output:

```text
24:SOURCE_FILES = ...
25:    "_archive/code/closed-runners/c10u_mint2_p4.sh", ...
39:    with open(path, "rb") as f:
82:    return {name: sha256_file(root / name) for name in [*SOURCE_FILES, *engine]}
```

Executing only the extracted hashing definitions confirmed that this reader reads the archived runner, returning SHA-256:

```text
4271f5ce8152f9ab11b6065650394b6eaee62d8b7d741f015c4f8066f632af7f
```

Lane 8b’s report already identifies both as false and labels them “not mine, reported.” Its edit restriction explains why they remain; it does not establish a passing guide audit. Update both reader lines.

## 3. C10Y precondition and open-items record

**NON-BLOCKING — no new false statement found in either record. Ruling 3’s condition is preserved.**

`PRECONDITION_HALT_WRITER_REPOINT.md:3,15` requires the next pin-repair authorization to include **both the repoint and its selftest before a run**. This correctly preserves the authorization boundary.

Command:

```sh
LLMDB_ROOT=$PWD PYTHONPATH=code .venv/bin/python -B -c '
from lab.track_c import c10y_directdw_arms as c
try:
    c.preflight(env={})
except c.Halt as e:
    print(type(e).__name__ + ": " + str(e))
'
```

Output:

```text
Halt: PREREG SHA MISMATCH
```

`c10y_directdw_arms.py:1722` calls preflight before launch authorization (`:1723`) and worker creation (`:1744`). The current refusal is mechanical; retaining the repoint when repairing pins remains an authorization requirement.

Command:

```sh
git check-ignore -v architecture_profile/example.json \
  experiments/c10y/runs/example/halts/example.json
```

Output:

```text
.gitignore:142:/architecture_profile/ architecture_profile/example.json
```

`OPEN-ITEMS.md:3–17` faithfully carries the prior non-blocking dispositions. That statement applies to its listed items, not to the unresolved findings above.

## 4. Ruling 4 and merge fitness

**BLOCKING — REJECT Ruling 4 for this candidate.**

The original guide corrections pass, but the sweep has two acknowledged false reader claims. The resolver also produces silent wrong-section answers under an ordinary section reorder.

Current checks report `INDEX CLEAN`, all rendered views current, and twins exit 0. Those checks do not detect the demonstrated resolver failures.

Reviewed head: `9e6d51dcf4cfc58c0771cdbcc65036ccfe8d6b99`. The worktree remained clean. No files were edited; no model or GPU work ran.