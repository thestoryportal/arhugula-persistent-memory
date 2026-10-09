# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo", "duckdb", "pydantic", "psutil", "numpy", "torch==2.8.0"]
# ///
import marimo, duckdb, pydantic, psutil, numpy, torch
print("deps",marimo.__version__,duckdb.__version__,torch.__version__)
db=duckdb.connect()
from pathlib import Path
r=Path("/private/tmp/mathlab_json_probe.json");r.write_text('{"arm":{"para_full_binding_n":46}}')
print(db.execute("SELECT json_extract(to_json(t), ?)::DOUBLE FROM read_json(?) t", ["/arm/para_full_binding_n",str(r)]).fetchall())
