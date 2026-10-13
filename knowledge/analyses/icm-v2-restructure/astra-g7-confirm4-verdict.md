VERDICT: NO-GO

## 1. Round-3 section 2 rerun

**NON-BLOCKING — all requested parser corrections pass.** Relevant implementation: [resolve_path.py:38–53](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/resolve_path.py:38).

I verified that `8f/astra_section2.py` equals the script extracted from round 3, then ran:

```sh
R=/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261012T114331Z-2ec28dcb/icm-v2/phase3/step6
/opt/homebrew/bin/rtk proxy env LLMDB_ROOT=$PWD PYTHONPATH=code \
  .venv/bin/python -B "$R/8f/astra_section2.py"
```

Results:

```text
ATX control rc=2 2 live headings match the pinned heading
Setext rc=2 2 live headings match the pinned heading
blockquote rc=2 2 live headings match the pinned heading
list rc=2 2 live headings match the pinned heading
mixed fence rc=2 2 live headings match the pinned heading
long fence rc=2 2 live headings match the pinned heading
indented code rc=2 2 live headings match the pinned heading
HTML comment rc=0 fragment=13-changelog--2026-06-19
target=<h3 id="13-changelog--2026-06-19">§13 changelog — 2026-06-19</h3>
```

The two accepted limits still return `rc=0`; they are excluded from the findings below.

## 2. Remaining live-edit failure classes

Four distinct remaining classes were demonstrated. These findings preserve the original rendered heading; they do not depend on transferring its slug to a replacement or assigning an explicit ID.

| Finding | Live edit | Cause and location |
|---|---|---|
| **BLOCKING — inline source differs from rendered heading text** | Prepend a duplicate using a reference link, underscore emphasis, a nested link destination, padded code span, quoted HTML attribute, or inline HTML comment. | [resolve_path.py:46–47](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/resolve_path.py:46) passes raw inline source to the unchanged regex slugger at lines 27–35. Different source slugs can produce identical rendered anchors. |
| **BLOCKING — raw HTML headings are omitted** | Prepend `<h3>10.1 Purpose</h3>` without an ID. | [resolve_path.py:43–44](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/resolve_path.py:43) excludes `html_block`/`html_inline` tokens even when they render headings receiving automatic anchors. |
| **BLOCKING — Unicode line splitting changes block structure** | Put U+2028 before fence characters on otherwise ordinary paragraph lines, surrounding an inserted duplicate. | [resolve_path.py:86](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/resolve_path.py:86) uses `splitlines()`; line 41 rejoins those pieces with LF. This manufactures fences and hides a rendered heading. CommonMark line endings are CR/LF, not U+2028. [GFM specification](https://github.github.com/gfm/#characters-and-lines) |
| **BLOCKING — renderer-supported heading containers are omitted** | Move the original section into a referenced footnote and insert a new same-named ordinary heading. | [resolve_path.py:41](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/resolve_path.py:41) uses CommonMark without footnote support. The original still renders as a heading, but the resolver sees only the inserted heading. |

The common consequence is `rc=0`, returning `#101-purpose` for the inserted section. GitHub removes inline formatting before assigning anchors and numbers subsequent duplicates. Thus the original rendered heading receives `#101-purpose-1`. [GitHub’s anchor rules](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#section-links)

This read-only command proves the CLI result, two rendered matching headings, and that the first matching heading contains the inserted `NEW` section:

```sh
/opt/homebrew/bin/rtk proxy env LLMDB_ROOT=$PWD PYTHONPATH=code \
.venv/bin/python -B -c '
import io, os, sys
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch
from html.parser import HTMLParser
from markdown_it import MarkdownIt
sys.path.append("/Users/robertrhu/.local/share/uv/tools/marimo/lib/python3.11/site-packages")
import markdown
from state import resolve_path as r

root = Path(os.environ["LLMDB_ROOT"])
part = root / "knowledge/specs/integrated-spec-v1_2/11-security-layer.md"
original = part.read_text()
key = "knowledge/specs/llm-as-database-v1_2-integrated-spec.md#101-purpose"
cases = [
 ("reference link", "### [10.1 Purpose][ref]\nNEW\n\n[ref]: https://example.com\n\n"+original),
 ("underscore emphasis", "### 10.1 _Purpose_\nNEW\n\n"+original),
 ("nested link destination", "### [10.1 Purpose](https://example.com/a(b)c)\nNEW\n\n"+original),
 ("code span padding", "### ` 10.1 Purpose `\nNEW\n\n"+original),
 ("quoted HTML attribute", "### <span title=\">x\">10.1 Purpose</span>\nNEW\n\n"+original),
 ("inline HTML comment", "### 10.1 <!-- > -->Purpose\nNEW\n\n"+original),
 ("raw HTML heading", "<h3>10.1 Purpose</h3>\nNEW\n\n"+original),
 ("Unicode separator", "prefix\u2028```\n\n### 10.1 Purpose\nNEW\n\nprefix\u2028```\n\n"+original),
 ("footnote container", "### 10.1 Purpose\nNEW\n\nReference[^n]\n\n[^n]: Note\n\n"+
  "".join("    "+line+"\n" for line in original.splitlines())),
]
class Headings(HTMLParser):
 def __init__(self):
  super().__init__()
  self.values, self.bodies, self.active = [], [], False
 def handle_starttag(self, tag, attrs):
  if tag in ("h1","h2","h3","h4","h5","h6"):
   self.active = True
   self.values.append("")
   self.bodies.append("")
 def handle_endtag(self, tag):
  if tag in ("h1","h2","h3","h4","h5","h6"):
   self.active = False
 def handle_data(self, data):
  if self.active:
   self.values[-1] += data
  elif self.bodies:
   self.bodies[-1] += data

read = Path.read_text
for name, changed in cases:
 out, err = io.StringIO(), io.StringIO()
 with patch.object(Path, "read_text", lambda p,*a,**k:
      changed if p == part else read(p,*a,**k)), \
      patch.object(sys, "argv", ["resolve_path.py", key]), \
      redirect_stdout(out), redirect_stderr(err):
  rc = r.main()
 rendered = (markdown.markdown(changed, extensions=["footnotes"])
             if name == "footnote container"
             else MarkdownIt("commonmark").render(changed))
 parsed = Headings()
 parsed.feed(rendered)
 n = parsed.values.count("10.1 Purpose")
 fragment = out.getvalue().strip().partition("#")[2]
 assert (rc, fragment, n) == (0, "101-purpose", 2), (
     name, rc, fragment, n, err.getvalue())
 first = parsed.values.index("10.1 Purpose")
 assert parsed.bodies[first].strip().startswith("NEW")
 print(f"{name}: rc={rc} fragment={fragment} rendered_matching_headings={n} first=NEW")
'
```

Output:

```text
reference link: rc=0 fragment=101-purpose rendered_matching_headings=2 first=NEW
underscore emphasis: rc=0 fragment=101-purpose rendered_matching_headings=2 first=NEW
nested link destination: rc=0 fragment=101-purpose rendered_matching_headings=2 first=NEW
code span padding: rc=0 fragment=101-purpose rendered_matching_headings=2 first=NEW
quoted HTML attribute: rc=0 fragment=101-purpose rendered_matching_headings=2 first=NEW
inline HTML comment: rc=0 fragment=101-purpose rendered_matching_headings=2 first=NEW
raw HTML heading: rc=0 fragment=101-purpose rendered_matching_headings=2 first=NEW
Unicode separator: rc=0 fragment=101-purpose rendered_matching_headings=2 first=NEW
footnote container: rc=0 fragment=101-purpose rendered_matching_headings=2 first=NEW
```

These are rendering checks plus documented anchor allocation, not browser-navigation tests of the synthetic documents. I additionally verified:

- GitHub’s stateless Markdown API renders a heading inside a footnote and moves it after body headings.
- A live public README’s source `<h1 align="center">Jupyter AI</h1>` receives `href="#jupyter-ai"` automatically, confirming that raw HTML headings need no explicit ID. [Source](https://github.com/jupyterlab/jupyter-ai/blob/main/README.md?plain=1), [rendered README](https://github.com/jupyterlab/jupyter-ai)

## 3. False statements, tests, and dependency consistency

**NON-BLOCKING — no false assertion in the added/modified tests was found.** Their coverage is narrower than complete rendered-anchor equivalence.

The added tests at [test_resolve_path.py:47–101](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/code/state/test_resolve_path.py:47), plus destination checks, pass:

```sh
/opt/homebrew/bin/rtk proxy env LLMDB_ROOT=$PWD PYTHONPATH=code \
  .venv/bin/python -B -m unittest \
  state.test_resolve_path.CommonMarkHeadingTests \
  state.test_resolve_path.DestinationFragmentTests -v
```

```text
Ran 4 tests in 39.498s
OK
517 rows checked and 0 missing
```

Both modified duplicate-test bodies also passed using an in-memory filesystem, avoiding their file-writing setup.

**NON-BLOCKING — the lane’s compatibility claims are confirmed.**

```sh
/opt/homebrew/bin/rtk proxy env LLMDB_ROOT=$PWD PYTHONPATH=code \
  .venv/bin/python -B "$R/8f/differential.py"
/opt/homebrew/bin/rtk proxy env LLMDB_ROOT=$PWD PYTHONPATH=code \
  .venv/bin/python -B "$R/8f/map_identity.py"
/opt/homebrew/bin/rtk proxy env LLMDB_ROOT=$PWD PYTHONPATH=code \
  .venv/bin/python -B code/state/build_index.py --check
```

```text
tracked Markdown files = 149
historical monoliths = 3
sources checked = 152
files that differ = 0

rows = 517
map_unchanged = True
live_map_unchanged = True
sha256 = baf93fcf7a4846a3ebb0b994b9d5f68b6970da1cd1a4a9013c02fc912d6ef0ed

INDEX CLEAN
```

**NON-BLOCKING — dependency declaration is consistent.**

- [pyproject.toml:32](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/pyproject.toml:32): `markdown-it-py==3.0.0`.
- [uv.lock:545,563,576](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/uv.lock:563): project dependency, exact requirement, and version `3.0.0`; transitive `mdurl` is locked to `0.1.2`.
- [ci.yml:39](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/icm-v2/.github/workflows/ci.yml:39): installs `markdown-it-py==3.0.0` before the index check.

Command:

```sh
/opt/homebrew/bin/rtk proxy rg -n 'markdown-it-py|mdurl' \
  pyproject.toml uv.lock .github/workflows/ci.yml
```

The TOML parsing and installed-metadata check additionally returned:

```text
uv package: 3.0.0 [{'name': 'mdurl'}]
uv mdurl: 0.1.2
installed: 3.0.0 0.1.2
```

## 4. Ruling 4: fit to merge?

**BLOCKING — NO-GO.** The requested scanner fixes work, but the four newly demonstrated classes still permit silent redirects. Heading recognition, rendered heading text, and fragment allocation must agree—or unsupported cases must fail closed.

Reviewed only `0dd74910..f39822e8`; final HEAD was `f39822e82f4191397b85f8f43abd6b03f6a5e143`. `git diff --check` passed and `git status --porcelain=v1` was empty. No files were edited; no model or GPU work ran.