import json, os, signal, time
from pathlib import Path
root = Path(os.environ["LLMDB_ROOT"])
cfg = json.loads((root/"fixture.json").read_text())
signal.signal(signal.SIGTERM, lambda *args: exit(0))
if cfg.get("mode") == "unreaped":
    while not (root/"release_worker").exists(): time.sleep(.02)
else:
    time.sleep(.65)
