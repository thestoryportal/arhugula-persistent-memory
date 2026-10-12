"""Program-only substitute for GPU preflight and model loading; no torch import."""
import os
from pathlib import Path
import runpy
import struct
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fixture_editor_runtime
sys.modules['editor_runtime'] = fixture_editor_runtime
sys.modules['prepare'] = fixture_editor_runtime
os.write(int(os.environ['C10_READY_FD']), struct.pack('!d', time.monotonic()))
runpy.run_path(str(Path(os.environ['C10_RUN_DIR']) / 'edit.py'), run_name='__main__')
