import os, sys
from pathlib import Path
import dashboard_live as live
import fixture_dep
base = Path(__file__).parent
marker = base / "first_frame"
if not marker.exists():
    stamp = live.source_stamp(str(base))
    marker.write_text("recorded\n")
    dep = base / "fixture_dep.py"
    dep.write_text("VALUE = 'HELPER_RELOADED'\n")
    os.utime(dep, (200, 200))
    live.maybe_reload(stamp)
    print("RELOAD_MISSED")
    sys.exit(1)
print(fixture_dep.VALUE)
sys.exit(0 if fixture_dep.VALUE == "HELPER_RELOADED" else 1)
