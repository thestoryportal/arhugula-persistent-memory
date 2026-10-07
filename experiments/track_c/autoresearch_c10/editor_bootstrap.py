"""Trusted entrypoint: load the public runtime before executing a recipe snapshot."""
import importlib.util
import os
from pathlib import Path
import runpy
import struct
import sys
import time

fence = Path(__file__).resolve().parent
sys.path.insert(0, str(fence))
spec = importlib.util.spec_from_file_location('editor_runtime', fence / 'editor_runtime.py')
runtime = importlib.util.module_from_spec(spec)
sys.modules['editor_runtime'] = runtime
spec.loader.exec_module(runtime)
# The equivalence baseline remains byte-for-byte fd16592; its old import resolves
# to this evaluation-free runtime, without reading the retired prepare.py.
sys.modules['prepare'] = runtime
os.write(int(os.environ['C10_READY_FD']), struct.pack('!d', time.monotonic()))
runpy.run_path(str(Path(os.environ['C10_RUN_DIR']) / 'edit.py'), run_name='__main__')
