import json
from pathlib import Path
def probe(kind):
    cfg = json.loads((Path(__file__).parents[1]/"fixture.json").read_text())
    return {"allowed": not cfg.get("dry_refused", False), "reasons": [],
            "checks": {"gpu": {"blocking_processes": []}}}
