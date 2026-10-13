"""Rebuild the derived DuckDB index from source JSON; no torch imports."""
import math
import os
from pathlib import Path
import uuid

from apps.mathlab import mathlab_runtime as R


def build_index(path, references):
    import duckdb
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with duckdb.connect(str(temporary)) as db:
            db.execute("CREATE TABLE calibration (arm VARCHAR, block VARCHAR, run VARCHAR, metric VARCHAR, value DOUBLE, "
                       "source_path VARCHAR, json_pointer VARCHAR, source_sha256 VARCHAR, tier VARCHAR)")
            for ref in references:
                source = Path(ref["path"]).resolve(); before = R.sha_file(source)
                if "sha256" in ref: R.require(before == ref["sha256"], "SOURCE", "index source identity changed")
                rows = db.execute("SELECT json_extract(to_json(t), ?)::DOUBLE FROM read_json(?) t",
                                  [ref["pointer"], str(source)]).fetchall()
                R.require(len(rows) == 1 and rows[0][0] is not None and math.isfinite(rows[0][0]),
                          "SOURCE", "index JSON pointer does not name one finite metric")
                R.require(R.sha_file(source) == before, "SOURCE", "index source changed during read_json")
                db.execute("INSERT INTO calibration VALUES (?,?,?,?,?,?,?,?,?)",
                           [ref["arm"], ref["block"], ref["run"], ref["metric"], rows[0][0], str(source), ref["pointer"], before, R.TIER])
        os.replace(temporary, path)
    finally:
        if temporary.exists(): temporary.unlink()
    return dict(path=str(path), sha256=R.sha_file(path), tier=R.TIER, derived=True, rows=len(references))
