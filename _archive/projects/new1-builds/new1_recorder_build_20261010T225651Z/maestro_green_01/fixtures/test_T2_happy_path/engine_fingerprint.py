import json, os, sys
from pathlib import Path
root = Path(os.environ["LLMDB_ROOT"])
cfg = json.loads((root/"fixture.json").read_text())
if cfg.get("change_hash"):
    with (root/"tools/new1_geometry.py").open("a") as target: target.write("\n# changed at fingerprint check\n")
print("fixture fingerprint")
sys.exit(3 if cfg.get("fingerprint_refused") else 0)
