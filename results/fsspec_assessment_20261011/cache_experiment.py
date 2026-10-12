"""FS1 local cache measurement; no network, credentials, torch, or cleanup.
Budget: <64 MiB disk, <=200 MiB hard limit, deadline 110 seconds.
Criteria fixed before execution: three disk caches retain 3*4 MiB payload;
RAM BlockCache retains <=2*256 KiB after repeated reads of 4 MiB.
"""
import json
import os
from pathlib import Path
import signal
import tempfile
import time

import fsspec
from fsspec.caching import BlockCache
from fsspec.implementations.local import LocalFileSystem
from fsspec.spec import AbstractBufferedFile

MiB = 1 << 20
start = time.monotonic()
signal.alarm(110)
stat = os.statvfs('/private/tmp')
free = stat.f_bavail * stat.f_frsize
assert free >= 64 * MiB + 20 * (1 << 30), free
root = Path(tempfile.mkdtemp(prefix='fs1_fsspec_', dir='/private/tmp'))
print(json.dumps({'root': str(root), 'fsspec': fsspec.__version__,
                  'disk_budget_bytes': 64 * MiB, 'free_before_bytes': free}), flush=True)
source = root / 'source'
source.mkdir()
paths = []
for index in range(3):
    path = source / f'{index}.bin'
    with path.open('xb') as stream:
        for _ in range(4):
            stream.write(bytes([index + 1]) * MiB)
    paths.append(path)

class LocalRangeFile(AbstractBufferedFile):
    def _fetch_range(self, start, end):
        self.fs.fetched_bytes += end - start
        with open(self.path, 'rb') as stream:
            stream.seek(start)
            return stream.read(end - start)

class LocalRangeFS(LocalFileSystem):
    # LocalFileOpener.read bypasses its cache: use the supported buffered-file
    # interface so the disk blockcache's actual MMapCache handles the reads.
    protocol = 'fs1-local-range'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fetched_bytes = 0
    def _open(self, path, mode='rb', **kwargs):
        assert mode == 'rb', mode
        return LocalRangeFile(self, path, mode=mode, **kwargs)

backend = LocalRangeFS(skip_instance_cache=True)
for protocol in ('filecache', 'blockcache', 'simplecache'):
    cache_dir = root / protocol
    fs = fsspec.filesystem(protocol, fs=backend, cache_storage=str(cache_dir),
                           expiry_time=3600, skip_instance_cache=True)
    read_bytes = 0
    for index, path in enumerate(paths):
        fetched_before = backend.fetched_bytes
        for repeat in range(2):
            with fs.open(str(path), 'rb', block_size=256 * 1024) as stream:
                while chunk := stream.read(256 * 1024):
                    assert chunk == bytes([index + 1]) * len(chunk)
                    read_bytes += len(chunk)
        data_files = [p for p in cache_dir.iterdir() if p.is_file() and p.name != 'cache']
        payload = sum(p.stat().st_size for p in data_files)
        total = sum(p.stat().st_size for p in root.rglob('*') if p.is_file())
        assert payload == (index + 1) * 4 * MiB, payload
        assert total < 64 * MiB, total
        print(json.dumps({'protocol': protocol, 'files_read': index + 1,
                          'cumulative_read_bytes': read_bytes,
                          'payload_logical_bytes': payload,
                          'payload_allocated_bytes': sum(p.stat().st_blocks * 512 for p in data_files),
                          'backend_fetched_bytes_this_file': backend.fetched_bytes - fetched_before,
                          'expiry': fs.expiry, 'all_fixture_logical_bytes': total}), flush=True)

with paths[0].open('rb') as stream:
    def fetch(begin, end):
        stream.seek(begin)
        return stream.read(end - begin)
    cache = BlockCache(256 * 1024, fetch, 4 * MiB, maxblocks=2)
    for repeat in range(2):
        for offset in range(0, 4 * MiB, 256 * 1024):
            assert cache._fetch(offset, offset + 256 * 1024) == bytes([1]) * (256 * 1024)
    info = cache.cache_info()
    assert info.currsize <= 2 and info.misses > 2
    print(json.dumps({'ram_blockcache': info._asdict(), 'retained_payload_bound_bytes':
                      info.currsize * cache.blocksize, 'bytes_read': 8 * MiB}), flush=True)
print(json.dumps({'result': 'PASS_LOCAL_MEASUREMENT', 'elapsed_seconds': time.monotonic() - start,
                  'root_retained': str(root)}), flush=True)
signal.alarm(0)
