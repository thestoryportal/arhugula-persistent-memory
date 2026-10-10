"""Private stage registry, exact PID generation + cwd + process group checks."""
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from v13_common import read_json, stop_stage, verify
fence = Path(__file__).resolve().parent
config = verify(fence, sys.argv[1])
failed = False
for stage in ('editor', 'scorer'):
    path = fence / 'sealed' / (stage + '.pid.json')
    if path.exists():
        try:
            stop_stage(read_json(path), config)
            path.unlink()
            print(stage + ': stopped')
        except Exception:
            failed = True
            print(stage + ': identity/cwd check failed; record retained')
raise SystemExit(1 if failed else 0)
