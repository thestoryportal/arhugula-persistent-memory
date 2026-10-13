"""Verify durable receipts and native-call timeout without any real input/SVD."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
from unittest.mock import patch

directory = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('profile_fixture', directory/'profile_l4.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
fixture = directory/'watchdog_fixture'
fixture.mkdir()
module.DIRECTORY = fixture
module.DEADLINE = .5
real_popen = subprocess.Popen


def native_blocking_child(argv, **kwargs):
    return real_popen([sys.executable, '-B', '-c',
                       'import ctypes; ctypes.CDLL(None).sleep(30)'], **kwargs)


module.START = time.monotonic()
with patch.object(module.subprocess, 'Popen', side_effect=native_blocking_child):
    result = module.launch()
wall = time.monotonic() - module.START
records = [json.loads(line) for line in (fixture/'receipt.jsonl').read_text().splitlines()]
assert result == 124 and wall < 3
assert [r['kind'] for r in records] == ['measurement_launch', 'measurement_timeout']
assert records[-1]['child_returncode'] == -15
assert records[-1]['child_process_high_water']['peak_rss_bytes'] > 0
print(json.dumps({'watchdog': 'PASS', 'wall_s': wall, 'exit_code': result,
                  'native_blocking_child_returncode': records[-1]['child_returncode'],
                  'fsynced_receipts_parse': True, 'real_inputs_read': False, 'SVD_calls': 0}))
