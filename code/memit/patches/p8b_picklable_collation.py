#!/usr/bin/env python3
"""P-8b — make the engine's length collator picklable (rome/tok_dataset.py).

layer_stats() builds its DataLoader with num_workers=2. On Linux the workers fork and
inherit the closure returned by length_collation(); on macOS they spawn and must pickle
it, which fails ("Can't pickle local object 'length_collation.<locals>.collate_fn'").
The closure becomes a module-level function bound with functools.partial — same body,
same arguments, same batches. Anchored and idempotent; run from the repo root.
"""
from pathlib import Path
import re, sys

p = Path("code/memit/vendor/rome/tok_dataset.py")
s = p.read_text(encoding="utf-8")
if "_length_collate" in s:
    print("P-8b: ALREADY APPLIED"); sys.exit(0)

head = "    def collate_fn(items):\n"
tail = "\n    return collate_fn\n"
assert s.count(head) == 1 and s.count(tail) == 1
a = s.index(head) + len(head)
b = s.index(tail)
body = "\n".join(line[4:] if line.startswith("    ") else line for line in s[a:b].split("\n"))
new = (
    "    return functools.partial(_length_collate, token_size)  # P-8b: picklable for spawn-based DataLoader workers\n\n\n"
    "def _length_collate(token_size, items):\n" + body + "\n"
)
s = s[: s.index(head)] + new + s[b + len(tail):]
assert s.count("import torch\n") == 1
s = s.replace("import torch\n", "import functools\nimport torch\n", 1)
p.write_text(s, encoding="utf-8")
print("P-8b: APPLIED")
