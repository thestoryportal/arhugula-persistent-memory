import json
import os
from pathlib import Path


def write_bytes(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(value); out.flush(); os.fsync(out.fileno())
    fd = os.open(path.parent, os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)
    if path.read_bytes() != value: raise RuntimeError('record bytes did not roundtrip: '+str(path))


def write_json(path, value):
    data = (json.dumps(value, sort_keys=True, allow_nan=False)+'\n').encode()
    write_bytes(path, data)
    if json.loads(Path(path).read_text()) != json.loads(data):
        raise RuntimeError('normalized JSON did not roundtrip: '+str(path))
