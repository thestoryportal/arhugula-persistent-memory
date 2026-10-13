VERDICT: NO-GO

## 1. Is the duplicate-heading finding fixed?

**NON-BLOCKING — the reported ATX-heading reproduction is fixed.** [resolve_path.py:84–93](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/resolve_path.py:84) now rejects both matching headings.

I reran the exact `duplicate`/`restore` script extracted from section 1 of the prior verdict:

```text
duplicate old_slug_exists = False
Unknown anchor for program/EXPERIMENT_RUNBOOK.md: a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1; 2 live headings match the pinned heading
restore old_slug_exists = True
Unknown anchor for program/EXPERIMENT_RUNBOOK.md: a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1; heading changed after the pin
```

I also reran:

```sh
R=/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261012T114331Z-2ec28dcb/icm-v2/phase3/step6
LLMDB_ROOT=$PWD PYTHONPATH=code /opt/homebrew/bin/rtk proxy \
  .venv/bin/python -B "$R/8d/astra_repro.py"
```

Output, exit 0:

```text
insert
INDEX CLEAN
check_rc = 0
a1 -> a1--batch-vs-sequential-write--done--pass-robust-evidencecorpus14-d-a1-1
a2 -> a2--relation-balanced-in-solve-sentinels-3-disjoint-pools--done--partial-strong-directional-evidencecorpus15-d-a2-1
reorder sections
INDEX CLEAN
check_rc = 0
a1 -> a1--batch-vs-sequential-write--done--pass-robust-evidencecorpus14-d-a1-1
a2 -> a2--relation-balanced-in-solve-sentinels-3-disjoint-pools--done--partial-strong-directional-evidencecorpus15-d-a2-1
```

## 2. Remaining edits that silently redirect an old anchor

The remaining failures fall into parser undercounting, parser overcounting, and identity collisions. The concrete cases found are collected here.

| Finding | Live edit and result | Detectable from destination heading text alone? |
|---|---|---|
| **BLOCKING — missed headings** | Insert a duplicate as a **Setext heading**, **blockquote heading**, or **list heading** before the original. Each returns exit 0 and the new section’s fragment. | **No.** The visible heading text is identical. |
| **BLOCKING — incorrect fence tracking** | Insert a duplicate between code blocks containing **mixed fence characters**, **unequal fence lengths**, or **indented code containing fence characters**. The scanner skips the new rendered heading and returns its fragment with exit 0. | **No.** The visible heading text is identical. |
| **BLOCKING — phantom headings** | Add heading-looking lines inside an **HTML comment**. They consume deduplication suffixes in the scanner but not in the rendered document. An additional visible section can then receive the fragment returned for the original section. | **Yes**, in the reproduction below. |
| **NON-BLOCKING — lossy raw-slug identity** | Rename/remove `10.1 Purpose`, then introduce a different section named `101 Purpose`. Both normalize to `101-purpose`; resolution succeeds. This follows the expressly specified raw-slug rule. | **Yes:** `10.1` versus `101`. |
| **NON-BLOCKING — explicit fragment collision** | Insert an earlier HTML element with `id="101-purpose"`. The resolver succeeds; renderers preserving that ID navigate to the earlier element. This deliberately assigns the fragment outside the heading namespace. | **Yes**, when the nearby section has a different title; the target itself need not be a heading. |

The blocking cases arise because the new matching rule at [resolve_path.py:84](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/resolve_path.py:84) depends on [heading_entries():36–52](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/resolve_path.py:36). That scanner recognizes only uncontained ATX headings, toggles fence state without checking fence type or length, and counts headings inside HTML comments.

The normalization limitation follows from [heading_slug():25–33](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/resolve_path.py:25) and the comparison at line 86.

Here is the read-only reproduction command. It substitutes live text in memory, calls the actual CLI entrypoint, and independently renders Markdown using the already-installed Python-Markdown/SuperFences packages. This is a local rendering check, not a GitHub browser test.

```sh
LLMDB_ROOT=$PWD PYTHONPATH=code /opt/homebrew/bin/rtk proxy .venv/bin/python -B -c '
import os, sys, io, re, unicodedata
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout, redirect_stderr
sys.path.append("/Users/robertrhu/.local/share/uv/tools/marimo/lib/python3.11/site-packages")
import markdown
from state import resolve_path as r

root = Path(os.environ["LLMDB_ROOT"])
part = "knowledge/specs/integrated-spec-v1_2/11-security-layer.md"
key = "knowledge/specs/llm-as-database-v1_2-integrated-spec.md#101-purpose"
text = (root / part).read_text()
h = "### 10.1 Purpose\nNEW SECTION\n\n"
f = chr(96) * 3
cases = [
 ("ATX control", part, key, h + text),
 ("Setext", part, key, "10.1 Purpose\n---\nNEW SECTION\n\n" + text),
 ("blockquote", part, key, "> ### 10.1 Purpose\n> NEW SECTION\n\n" + text),
 ("list", part, key, "- ### 10.1 Purpose\n\n  NEW SECTION\n\n" + text),
 ("mixed fence", part, key, f+"\n~~~\n"+f+"\n\n"+h+f+"\n~~~\n"+f+"\n\n"+text),
 ("long fence", part, key, f+"\x60\n"+f+"\n"+f+"\x60\n\n"+h+f+"\x60\n"+f+"\n"+f+"\x60\n\n"+text),
 ("indented code", part, key, "    "+f+"\n\n"+h+"    "+f+"\n\n"+text),
 ("slug transfer", part, key, "### 101 Purpose\nNEW SECTION\n\n"+
  text.replace("### 10.1 Purpose", "### Renamed original purpose", 1)),
 ("explicit ID", part, key,
  "<a id=\"101-purpose\"></a>\n\n### Other section\nNEW SECTION\n\n"+text),
]
part2 = "program/runbook/13-changelog-append-only.md"
slug = "13-changelog--2026-06-19"
base, number = slug.rsplit("-", 1)
changed = ("<!--\n"+("### "+base+"\n")*(int(number)+1)+"-->\n\n"+
           (root/part2).read_text()+"\n\n### "+slug+"-1\nOTHER SECTION\n")
cases.append(("HTML comment", part2, "program/EXPERIMENT_RUNBOOK.md#"+slug, changed))

read = Path.read_text
def rendered_slug(value, separator):
 return "".join(c for c in value.lower() if c in "-_" or not
  unicodedata.category(c).startswith(("P","S","C"))).replace(" ","-")

for name, part, key, changed in cases:
 out, err = io.StringIO(), io.StringIO()
 with patch.object(Path, "read_text", lambda p,*a,**k:
      changed if p==root/part else read(p,*a,**k)), \
      patch.object(sys,"argv",["resolve_path.py",key]), \
      redirect_stdout(out), redirect_stderr(err):
  rc = r.main()
 if rc:
  print(name, "rc="+str(rc), err.getvalue().strip().split("; ")[-1])
  continue
 fragment = out.getvalue().strip().partition("#")[2]
 rendered = markdown.markdown(changed,
  extensions=["toc","pymdownx.superfences"],
  extension_configs={"toc":{"slugify":rendered_slug}})
 target = re.search(r"<[^>]+id=\""+re.escape(fragment)+r"\"[^>]*>.*",rendered)
 print(name, "rc="+str(rc), "fragment="+fragment, "target="+target.group(0))
'
```

Output:

```text
ATX control rc=2 2 live headings match the pinned heading
Setext rc=0 fragment=101-purpose target=<h2 id="101-purpose">10.1 Purpose</h2>
blockquote rc=0 fragment=101-purpose target=<h3 id="101-purpose">10.1 Purpose</h3>
list rc=0 fragment=101-purpose target=<h3 id="101-purpose">10.1 Purpose</h3>
mixed fence rc=0 fragment=101-purpose target=<h3 id="101-purpose">10.1 Purpose</h3>
long fence rc=0 fragment=101-purpose target=<h3 id="101-purpose">10.1 Purpose</h3>
indented code rc=0 fragment=101-purpose target=<h3 id="101-purpose">10.1 Purpose</h3>
slug transfer rc=0 fragment=101-purpose target=<h3 id="101-purpose">101 Purpose</h3>
explicit ID rc=0 fragment=101-purpose target=<a id="101-purpose"></a></p>
HTML comment rc=0 fragment=13-changelog--2026-06-19-1 target=<h3 id="13-changelog--2026-06-19-1">13-changelog--2026-06-19-1</h3>
```

These are failure classes, not an exhaustive enumeration of arbitrary Markdown strings. I found no additional independent mechanism within the reviewed path.

## 3. Is any statement or test in the diff false or wrong?

**No false assertion or implementation mismatch with the stated raw-slug rule was found.** The tests prove narrower cases than complete rendered-heading identity.

- Both added resolver tests at [test_resolve_path.py:176](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/test_resolve_path.py:176) pass.
- The added pin guard test at [test_build_index.py:234](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/test_build_index.py:234) passes.
- I executed those three test bodies with in-memory filesystem fixtures; I did not run their normal file-writing setup.

```text
Ran 3 tests in 0.011s
OK
```

The read-only destination tests also passed:

```sh
LLMDB_ROOT=$PWD PYTHONPATH=code /opt/homebrew/bin/rtk proxy \
  .venv/bin/python -B -m unittest \
  state.test_resolve_path.DestinationFragmentTests -v
```

```text
Ran 2 tests in 29.298s
OK
517 rows checked and 0 missing
```

Fresh `build_anchor_map()` generation, compared directly with the committed bytes, produced:

```text
rows = 517
map_unchanged = True
```

The guards at [build_index.py:206–217](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/build_index.py:206) implement the requested pinned raw-slug checks.

## 4. Ruling 4: is the restructure fit to merge?

**BLOCKING — not yet.** The original ATX duplicate defect is fixed, but equivalent rendered duplicates still silently redirect old anchors. HTML-comment overcounting additionally produces a redirect to a visibly different heading.

The correction must make heading recognition and fragment allocation agree with the supported Markdown rendering rules, or reject unsupported constructs before returning success.

Reviewed `5b26b249..0dd74910`. Final HEAD was `0dd74910db35606d77942240f77acb5d8f11513a`; `git diff --check` passed and `git status --porcelain=v1` was empty. No files were edited; no model or GPU work ran.