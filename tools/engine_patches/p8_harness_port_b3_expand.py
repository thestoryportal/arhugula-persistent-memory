#!/usr/bin/env python3
"""Device port for experiments/track_b/b3_expand_native.py (no engine import in that script,
so the resolver is imported from the vendored engine's util/ explicitly). Anchored; idempotent."""
from pathlib import Path
p = Path("experiments/track_b/b3_expand_native.py"); s = p.read_text()
if "DEV = resolve_device()" in s:
    print("already ported")
else:
    anchor = "import torch\n"; assert s.count(anchor) == 1
    s = s.replace(anchor, anchor + 'sys.path.insert(0, f"{LLMDB_ROOT}/memit_dry_run/memit"); from util.device import resolve_device  # P-8 harness side\nDEV = resolve_device()\n')
    n = s.count('device_map="cuda"') + s.count('.to("cuda")')
    s = s.replace('device_map="cuda"', 'device_map=DEV').replace('.to("cuda")', '.to(DEV)')
    assert '"cuda"' not in s
    p.write_text(s); print(f"ported b3_expand_native.py: {n} device sites")
