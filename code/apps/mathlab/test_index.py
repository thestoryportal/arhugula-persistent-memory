"""Real DuckDB tests, separable from the CPU torch tests when ABI caches differ."""
import hashlib
from pathlib import Path
import tempfile
import unittest

import duckdb
from apps.mathlab.index import build_index


class IndexTests(unittest.TestCase):
    def test_rebuild_rows_retain_source_pointer_and_sha(self):
        with tempfile.TemporaryDirectory(dir="/private/tmp") as td:
            root = Path(td); source = root / "record.json"; index = root / "calibration.duckdb"
            source.write_text('{"arm":{"para_full_binding_n":46}}')
            refs = [dict(path=str(source), pointer="/arm/para_full_binding_n", arm="mint1_s0", block="F", run="r0", metric="para_full")]
            build_index(index, refs)
            with duckdb.connect(str(index), read_only=True) as db:
                row = db.execute('select arm,value,source_path,json_pointer,source_sha256 from calibration').fetchone()
            self.assertEqual(row, ("mint1_s0", 46., str(source), "/arm/para_full_binding_n", hashlib.sha256(source.read_bytes()).hexdigest()))
            source.write_text('{"arm":{"para_full_binding_n":40}}'); build_index(index, refs)
            with duckdb.connect(str(index), read_only=True) as db:
                self.assertEqual(db.execute('select value from calibration').fetchone()[0], 40.)


if __name__ == "__main__":
    unittest.main(verbosity=2)
