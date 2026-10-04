#!/usr/bin/env python3
"""Harness-side device port for the B3 deployment arm (edit -> save -> GGUF -> Q4_K_M -> probe).
Same substitutions as p8_harness_port_gate_experiments.py, plus the pipeline script's pod cwd.
Anchored; idempotent (re-run reports already-ported files)."""
from pathlib import Path

IMPORT_ANCHOR = "from memit.memit_hparams import MEMITHyperParams\n"
IMPORT_ADD = IMPORT_ANCHOR + "from util.device import resolve_device, empty_cache  # P-8 harness side\nDEV = resolve_device()\n"
common = [('device_map="cuda"', 'device_map=DEV'), ('.to("cuda")', '.to(DEV)'), ('.cuda()', '.to(DEV)'),
          ('device="cuda"', 'device=DEV'), ('torch.cuda.empty_cache()', 'empty_cache(DEV)')]

p = Path("experiments/track_b/b3_edit_and_save.py"); s = p.read_text()
if "DEV = resolve_device()" in s:
    print("b3_edit_and_save.py already ported")
else:
    assert s.count(IMPORT_ANCHOR) == 1; s = s.replace(IMPORT_ANCHOR, IMPORT_ADD)
    old = "Kd=K.double().cpu(); rd=resid.double().cpu()"; assert s.count(old) == 1
    s = s.replace(old, "Kd=K.cpu().double(); rd=resid.cpu().double()")  # MPS: cpu BEFORE double
    hits = 0
    for o, n in common: hits += s.count(o); s = s.replace(o, n)
    assert '"cuda"' not in s and ".cuda()" not in s
    p.write_text(s); print(f"ported b3_edit_and_save.py: {hits} device sites + 1 float64 site")

q = Path("experiments/track_b/b3_run.sh"); t = q.read_text()
if 'cd "$LLMDB_ROOT"' in t:
    print("b3_run.sh already ported")
else:
    assert t.count("cd /workspace\n") == 1
    t = t.replace("cd /workspace\n", 'cd "$LLMDB_ROOT"   # 2026-10-04: was the pod\'s /workspace\n')
    # server logs go under logs/ like the smoke step already does
    t = t.replace('> $LLMDB_ROOT/b3_server_$3.log', '> $LLMDB_ROOT/logs/b3_server_$3.log')
    q.write_text(t); print("ported b3_run.sh: cwd + server log path")
