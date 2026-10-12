#!/usr/bin/env python3
"""Harness-side device port for the two LAW#3 gate experiments (C2 keying probe, A1 batch write).
Device comes from util.device.resolve_device (LLMDB_DEVICE override, else first accelerator).
Anchored substitutions; each must hit at least once where listed."""
from pathlib import Path

IMPORT_ANCHOR = "from memit.memit_hparams import MEMITHyperParams\n"
IMPORT_ADD = IMPORT_ANCHOR + "from util.device import resolve_device, empty_cache  # P-8 harness side\nDEV = resolve_device()\n"

common = [
    ('device_map="cuda"', 'device_map=DEV'),
    ('.to("cuda")', '.to(DEV)'),
    ('.cuda()', '.to(DEV)'),
    ('device="cuda"', 'device=DEV'),
    ('torch.cuda.empty_cache()', 'empty_cache(DEV)'),
]
per_file = {
    "experiments/track_c/c2_key_collinearity.py": [],
    "experiments/scale/g6_scale_n.py": [
        ("Kd=K.double().cpu(); rd=resid.double().cpu()", "Kd=K.cpu().double(); rd=resid.cpu().double()"),  # MPS: cpu BEFORE double
        ("p=a.double(); q=b.double()", "p=a.cpu().double(); q=b.cpu().double()"),
    ],
}
for rel, extra in per_file.items():
    p = Path(rel); s = p.read_text()
    assert s.count(IMPORT_ANCHOR) == 1, rel
    s = s.replace(IMPORT_ANCHOR, IMPORT_ADD)
    for old, new in extra:
        assert s.count(old) == 1, f"{rel}: {old}"
        s = s.replace(old, new)
    hits = 0
    for old, new in common:
        hits += s.count(old); s = s.replace(old, new)
    assert '"cuda"' not in s and ".cuda()" not in s, rel
    p.write_text(s); print(f"ported {rel}: {hits} device sites + {len(extra)} float64 sites")
