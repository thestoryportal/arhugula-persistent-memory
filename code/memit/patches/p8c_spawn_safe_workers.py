#!/usr/bin/env python3
"""P-8c — DataLoader workers only where the platform forks (rome/layer_stats.py), and a
__main__ guard on the covariance precompute tool.

What happened: macOS starts DataLoader workers with "spawn", which re-imports the launching
script. code/memit/precompute_cov_l9_12.py had no __main__ guard, so each worker reloaded the
model and began its own covariance run (two "loading Qwen" lines, a second 3.4 GB process).
Linux forks and never re-imports, which is why the pod never saw this.

Fix 1 (engine): the worker count is keyed on the multiprocessing start method —
{"fork": 2} else 0 — so any guardless harness script that hits a cache miss is safe.
Fix 2 (tool): the precompute script's body moves under `if __name__ == "__main__":`.
Anchored, asserted, idempotent.
"""
from pathlib import Path
import sys

ls = Path("code/memit/vendor/rome/layer_stats.py"); s = ls.read_text(encoding="utf-8")
old = "        num_workers=2,\n"
new = ("        num_workers={\"fork\": 2}.get(torch.multiprocessing.get_start_method(), 0),  # P-8c: spawn re-imports __main__\n")
if new not in s:
    assert s.count(old) == 1, "layer_stats num_workers anchor"
    ls.write_text(s.replace(old, new), encoding="utf-8"); print("P-8c: layer_stats patched")
else:
    print("P-8c: layer_stats already patched")

pc = Path("code/memit/precompute_cov_l9_12.py"); t = pc.read_text(encoding="utf-8")
if "if __name__ == \"__main__\":" in t:
    print("P-8c: precompute already guarded"); sys.exit(0)
head_anchor = "ID = os.environ.get(\"MODEL_ID\", \"Qwen/Qwen2.5-3B\")\n"
assert t.count(head_anchor) == 1
i = t.index(head_anchor)
body = t[i:]
indented = "".join(("    " + line if line.strip() else line) for line in body.splitlines(keepends=True))
t = t[:i] + "\ndef main():\n" + indented + "\n\nif __name__ == \"__main__\":  # P-8c: spawn-based DataLoader workers re-import this file\n    main()\n"
pc.write_text(t, encoding="utf-8"); print("P-8c: precompute guarded")
