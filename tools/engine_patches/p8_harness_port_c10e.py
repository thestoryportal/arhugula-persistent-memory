#!/usr/bin/env python3
"""Harness-side device port for experiments/track_c/c10e_bandknob.py (the Route A R0 baseline recipe runner).
Same substitutions as the other p8 harness ports; the solve in my_edit already runs on CPU. Idempotent."""
from pathlib import Path
IMPORT_ANCHOR = "from memit.memit_hparams import MEMITHyperParams\n"
IMPORT_ADD = IMPORT_ANCHOR + "from util.device import resolve_device, empty_cache  # P-8 harness side\nDEV = resolve_device()\n"
common = [('device_map="cuda"', 'device_map=DEV'), ('.to("cuda")', '.to(DEV)'), ('.cuda()', '.to(DEV)'),
          ('device="cuda"', 'device=DEV'), ('torch.cuda.empty_cache()', 'empty_cache(DEV)')]
p = Path("experiments/track_c/c10e_bandknob.py"); s = p.read_text()
if "DEV = resolve_device()" in s:
    print("already ported")
else:
    assert s.count(IMPORT_ANCHOR) == 1; s = s.replace(IMPORT_ANCHOR, IMPORT_ADD)
    old = "    p = a.double()\n    q = b.double()\n"; assert s.count(old) == 1
    s = s.replace(old, "    p = a.cpu().double()\n    q = b.cpu().double()\n")
    hits = 0
    for o, n in common: hits += s.count(o); s = s.replace(o, n)
    assert '"cuda"' not in s and ".cuda()" not in s
    p.write_text(s); print(f"ported c10e_bandknob.py: {hits} device sites + 1 float64 site")
