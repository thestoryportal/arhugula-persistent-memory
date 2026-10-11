"""Prospective stdlib collector. Observations never authorize provisioning."""
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import selectors
import stat
import subprocess
import sys
import tarfile
import time
import urllib.parse
import uuid
import zipfile


class Refusal(RuntimeError):
    pass


def number(value, label):
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
        raise Refusal('Invalid nonnegative finite number: ' + label)
    return value


def pin(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def encoded(value):
    return (json.dumps(value, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')


def pointer(value, path):
    for part in path.strip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def resolved(value):
    if isinstance(value, dict):
        return bool(value) and all(resolved(v) for v in value.values())
    if isinstance(value, list):
        return all(resolved(v) for v in value)
    return value is not None and not (isinstance(value, str) and
        ('NEEDS-FETCH' in value or value.startswith('BLOCKED') or not value))


def admission(m, o):
    """Pure pre-install comparison; no recursive search of the whole manifest."""
    try:
        for path in m['preinstall']['required_fields']:
            if path.startswith('/postinstall/'):
                raise Refusal('Postinstall observation cannot be a preinstall requirement')
            if not resolved(pointer(m, path)):
                raise Refusal('Unresolved preinstall requirement: ' + path)
        b = m['budget']
        for key, value in b.items():
            if type(value) in (int, float):
                number(value, 'budget/' + key)
        components = b['components']
        if not components or len({x['id'] for x in components}) != len(components):
            raise Refusal('Incomplete or duplicate budget components')
        peak = sum(number(x['bytes'], x['id']) for x in components)
        if number(b['planned_peak_bytes'], 'planned peak') != peak:
            raise Refusal('Manifest peak disagrees with component sum')
        observed_peak = number(o['projected_setup_peak_bytes'], 'observed peak')
        if observed_peak != peak or peak > number(b['setup_cap_bytes'], 'setup cap'):
            raise Refusal('Projected peak disagrees with component sum or cap')
        if number(o['projected_provisioning_seconds'], 'provisioning time') > number(b['clock_seconds'], 'clock'):
            raise Refusal('Projected time exceeds clock')
        pool_map = m['host']['pool_map']
        if not isinstance(pool_map, dict) or not pool_map or any(not isinstance(x, str) or not x for x in pool_map.values()):
            raise Refusal('Incomplete expected physical pool map')
        roots = m['collector']['admitted_write_roots']
        if set(pool_map) != set(roots):
            raise Refusal('Pool map does not cover all admitted write roots')
        pools = o['pools']
        if not isinstance(pools, list) or not pools or len({x['id'] for x in pools}) != len(pools):
            raise Refusal('Empty or duplicate pools')
        if {x['id'] for x in pools} != set(pool_map.values()):
            raise Refusal('Incomplete physical pool coverage')
        floor = max(number(b['free_floor_bytes'], 'free floor'), number(b['additional_headroom_bytes'], 'headroom'))
        pool_peak = 0
        for pool in pools:
            growth = number(pool['projected_peak_bytes'], 'pool peak')
            pool_peak += growth
            if number(pool['free_bytes'], 'pool free') < growth + floor:
                raise Refusal('Physical pool headroom fails')
        if pool_peak != peak:
            raise Refusal('Pool allocation disagrees with component sum')
        for key in m['preinstall']['host_fields']:
            if o['host'][key] != m['host'][key]:
                raise Refusal('Host mismatch: ' + key)
        if o['tree'] != m['tree'] or o['paths'] != m['paths'] or o['preinstalled_ports'] != []:
            raise Refusal('Tree, paths or baseline ports mismatch')
        artifacts = m['artifacts']
        if len({a['id'] for a in artifacts}) != len(artifacts) or set(o['artifacts']) != {a['id'] for a in artifacts}:
            raise Refusal('Artifact coverage mismatch')
        for a in artifacts:
            actual = o['artifacts'][a['id']]
            if not pin(a['expected_sha256']) or actual['sha256'] != a['expected_sha256']:
                raise Refusal('Artifact digest mismatch: ' + a['id'])
            number(a['size_bytes'], 'artifact bytes')
            for key in ['version_revision', 'variants', 'source_url', 'size_bytes', 'route']:
                if actual[key] != a[key]:
                    raise Refusal('Artifact identity mismatch: ' + a['id'] + '/' + key)
            if a['route'] == 'binary archive' and actual.get('signature_verified') is not True:
                raise Refusal('Archive trust remains open')
        for key in ['staging', 'building', 'installation']:
            if m['authorization'][key] is not True:
                raise Refusal('Separate authorization absent: ' + key)
        for key in ['writer_reservation_matches', 'no_queued_external_writers']:
            if o[key] is not True:
                raise Refusal('Writer flag requires JSON true: ' + key)
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise Refusal('Malformed preinstall evidence: ' + str(exc)) from exc
    return {'comparison': 'satisfied', 'execution_authority': 'none'}


class Collector:
    def __init__(self, manifest, mode, now=None, monotonic=None, runner=None):
        self.m = manifest
        self.p = manifest['collector']
        if mode not in self.p['allowed_modes']:
            raise Refusal('Unadmitted mode; no writes')
        self.mode = mode
        self.now = now or time.time
        self.monotonic = monotonic or time.monotonic
        self.runner = runner or self._execute
        self.lock_fd = None
        self.pending = None
        self.pending_bound = 0
        self.byid = {a['id']: a for a in self.m['artifacts']}
        if len(self.byid) != len(self.m['artifacts']):
            raise Refusal('Duplicate artifact IDs')
        for key in ['receipt_limit_bytes', 'failure_reserve_bytes', 'staging_bound_bytes',
                'per_download_bound_bytes', 'command_timeout_seconds', 'command_output_limit_bytes', 'io_chunk_bytes']:
            if number(self.p[key], key) <= 0:
                raise Refusal('Positive collector allowance required: ' + key)
        if self.p['failure_reserve_bytes'] >= self.p['receipt_limit_bytes']:
            raise Refusal('Failure reserve leaves no receipt capacity')
        number(self.m['budget']['clock_seconds'], 'clock')
        self.root = Path(self.p['retained_dir'])
        admitted = [Path(x) for x in self.p['admitted_write_roots']]
        if not self.root.is_absolute() or self.root not in admitted:
            raise Refusal('Exact absolute retained root must be admitted')
        if any(x != self.root and x in self.root.parents for x in admitted):
            raise Refusal('Broad parent of retained root cannot be inventoried')
        if not set(self.p['install_roots']).issubset(set(self.p['admitted_write_roots'])):
            raise Refusal('Install roots outside admitted write roots')
        start = {'wall_start': self.now(), 'monotonic_start': self.monotonic(),
            'hostname': os.uname().nodename, 'manifest_sha256': hashlib.sha256(encoded(self.m)).hexdigest()}
        self.receipts = self.root / 'receipts'
        self.downloads = self.root / 'downloads'
        if not self.root.exists():
            self.root.mkdir(mode=0o700)  # Start was captured before this first write.
        s = self.root.lstat()
        if not stat.S_ISDIR(s.st_mode) or s.st_uid != os.getuid() or stat.S_IMODE(s.st_mode) != 0o700:
            raise Refusal('Retained root must be user-owned directory mode 0700')
        self.lock_fd = os.open(str(self.root), os.O_RDONLY)
        try:
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            window = self.root / 'window.json'
            if window.exists():
                if window.is_symlink():
                    raise Refusal('Window symlink refused')
                self.start = json.loads(window.read_text())
                if self.start['manifest_sha256'] != start['manifest_sha256'] or self.start['hostname'] != start['hostname']:
                    raise Refusal('Window host/manifest changed; never restart')
            else:
                if any(self.root.iterdir()):
                    raise Refusal('Retained directory without clock must be empty; never restart')
                self.start = start
                self.receipts.mkdir(mode=0o700)
                self.downloads.mkdir(mode=0o700)
                data = encoded(start)
                if len(data) + self.p['failure_reserve_bytes'] > min(self.p['receipt_limit_bytes'], self.p['staging_bound_bytes']):
                    raise Refusal('Initial receipt allowance too small')
                self._exclusive(window, data)
                self._exclusive(self.receipts / 'failure.json', encoded({'status': 'READY'}).ljust(self.p['failure_reserve_bytes'], b' '))
            for path in [self.receipts, self.downloads]:
                if path.is_symlink() or not path.is_dir():
                    raise Refusal('Missing or symlink collector namespace')
            failure = json.loads((self.receipts / 'failure.json').read_text())
            if failure['status'] != 'READY':
                raise Refusal('Window has retained failure; no retry/reset')
            self.remaining()
            self.admit_bytes(0)
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.lock_fd is not None:
            os.close(self.lock_fd)
            self.lock_fd = None

    def _syncdir(self, path):
        fd = os.open(str(path), os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def _exclusive(self, path, data):
        with path.open('xb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        self._syncdir(path.parent)

    def halt(self, error, argv=None, elapsed=None):
        path = self.receipts / 'failure.json'
        if path.is_symlink():
            raise Refusal('Failure receipt symlink refused')
        if path.exists() and json.loads(path.read_text())['status'] == 'HALTED':
            raise Refusal(str(error))  # The first causal receipt is immutable.
        record = {'status': 'HALTED', 'argv': argv, 'elapsed_seconds': elapsed if elapsed is not None else self.elapsed(),
            'error': str(error), 'error_type': type(error).__name__}
        data = encoded(record)
        while len(data) > self.p['failure_reserve_bytes'] and len(record['error']) > 1:
            record['error'] = record['error'][:len(record['error']) // 2]
            record['error_truncated'] = True
            data = encoded(record)
        if len(data) > self.p['failure_reserve_bytes']:
            raise Refusal('Failure receipt cannot fit; command was not admissible')
        with path.open('r+b') as f:
            f.write(data.ljust(self.p['failure_reserve_bytes'], b' '))
            f.flush()
            os.fsync(f.fileno())
        self._syncdir(self.receipts)
        raise Refusal(str(error))

    def elapsed(self):
        wall = self.now() - self.start['wall_start']
        mono = self.monotonic() - self.start['monotonic_start']
        if wall < 0 or mono < 0:
            raise Refusal('Window clock rollback/reboot; never restart')
        return max(wall, mono)

    def remaining(self):
        try:
            remaining = self.m['budget']['clock_seconds'] - self.elapsed()
        except Refusal as exc:
            self.halt(exc, elapsed=0)
        if remaining <= 0:
            self.halt('Cumulative provisioning deadline exceeded')
        return remaining

    def _paths(self, root):
        yield root
        s = root.lstat()
        if stat.S_ISDIR(s.st_mode):
            with os.scandir(str(root)) as entries:
                for entry in entries:
                    yield from self._paths(Path(entry.path))

    def usage(self):
        receipts = (self.root / 'window.json').stat().st_size
        downloads = 0
        for root, category in [(self.receipts, 'receipts'), (self.downloads, 'downloads')]:
            for path in self._paths(root):
                s = path.lstat()
                if stat.S_ISREG(s.st_mode):
                    if category == 'receipts':
                        receipts += s.st_size
                    elif path != self.pending:
                        downloads += s.st_size
                elif not stat.S_ISDIR(s.st_mode):
                    raise Refusal('Unsupported collector-created accounting entry: ' + str(path))
        return {'receipt_bytes': receipts, 'download_bytes': downloads,
            'staging_bytes': receipts + downloads + self.pending_bound}

    def admit_bytes(self, amount, receipt=False):
        number(amount, 'additional bytes')
        used = self.usage()
        if receipt and used['receipt_bytes'] + amount > self.p['receipt_limit_bytes']:
            self.halt('Cumulative receipt limit exceeded')
        if used['staging_bytes'] + amount > self.p['staging_bound_bytes']:
            self.halt('Cumulative staging bound exceeded before write')

    def stream(self, label, rows):
        path = self.receipts / (label + '-' + uuid.uuid4().hex + '.jsonl')
        self.remaining()
        self.admit_bytes(0, receipt=True)
        with path.open('xb', buffering=0) as f:
            for row in rows:
                self.remaining()
                data = encoded(row)
                self.admit_bytes(len(data), receipt=True)
                f.write(data)
                os.fsync(f.fileno())
        self._syncdir(self.receipts)
        return path

    def save(self, label, value):
        return self.stream(label, iter([value]))

    def _execute(self, argv, timeout, **kwargs):
        """Bounded pipe capture, including stderr; no child output file writes."""
        started = self.monotonic()
        stdout, stderr = bytearray(), bytearray()
        child = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=kwargs['cwd'], env=kwargs['env'], stdin=subprocess.DEVNULL)
        try:
            with selectors.DefaultSelector() as sel:
                sel.register(child.stdout, selectors.EVENT_READ, stdout)
                sel.register(child.stderr, selectors.EVENT_READ, stderr)
                while sel.get_map():
                    left = min(timeout - (self.monotonic() - started), self.remaining())
                    if left <= 0:
                        raise subprocess.TimeoutExpired(argv, timeout, bytes(stdout), bytes(stderr))
                    for key, _ in sel.select(left):
                        chunk = os.read(key.fileobj.fileno(), self.p['io_chunk_bytes'])
                        if not chunk:
                            sel.unregister(key.fileobj)
                        else:
                            if len(stdout) + len(stderr) + len(chunk) > self.p['command_output_limit_bytes']:
                                raise Refusal('Command output allowance exceeded')
                            key.data.extend(chunk)
            left = min(timeout - (self.monotonic() - started), self.remaining())
            return subprocess.CompletedProcess(argv, child.wait(timeout=max(0, left)), bytes(stdout), bytes(stderr))
        finally:
            if child.poll() is None:
                child.kill()
                child.wait()
            child.stdout.close()
            child.stderr.close()

    def run(self, argv):
        started = self.monotonic()
        try:
            contract = self.p['child_contract']
            if contract['reviewed'] is not True or argv[0] != contract['executable']:
                raise Refusal('Reviewed child write-root/executable contract absent')
            if contract['allowed_write_roots'] != [str(self.root)]:
                raise Refusal('Child write roots disagree with retained root')
            if self.runner == self._execute and (not pin(contract['sha256']) or self.digest(argv[0]) != contract['sha256']):
                raise Refusal('Child executable identity mismatch')
            if len(encoded({'argv': argv, 'error': 'command failed', 'elapsed_seconds': 0, 'status': 'HALTED'})) >= self.p['failure_reserve_bytes']:
                self.halt('Command argv cannot fit durable failure reserve; command not started')
            env = dict(contract['environment'])
            env.update(HOME=str(self.root), TMPDIR=str(self.root))
            result = self.runner(argv, timeout=min(self.remaining(), self.p['command_timeout_seconds']),
                cwd=str(self.root), env=env)
            if result.returncode != 0:
                raise Refusal('Command failed exit=%s stderr=%r' % (result.returncode, result.stderr))
            if len(result.stdout) + len(result.stderr) > self.p['command_output_limit_bytes']:
                raise Refusal('Command output allowance exceeded')
            self.save('command', {'argv': argv, 'elapsed_seconds': self.monotonic() - started,
                'exit': result.returncode, 'stdout': result.stdout.decode('utf-8'), 'stderr': result.stderr.decode('utf-8')})
            self.remaining()
            return result.stdout.decode('utf-8').strip()
        except (OSError, subprocess.SubprocessError, Refusal, UnicodeError) as exc:
            self.halt(exc, argv=argv, elapsed=self.monotonic() - started)

    def digest(self, path):
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(self.p['io_chunk_bytes']), b''):
                self.remaining()
                h.update(chunk)
        return h.hexdigest()

    def record(self, path):
        path = Path(path)
        origin = 'collector' if path in [self.root, self.root / 'window.json'] or any(r == path or r in path.parents for r in [self.receipts, self.downloads]) else 'baseline'
        row = {'path': str(path), 'origin': origin}
        try:
            s = path.lstat()
            row.update(mode=stat.S_IMODE(s.st_mode), uid=s.st_uid, gid=s.st_gid,
                logical_bytes=s.st_size, allocated_bytes=s.st_blocks * 512, device=s.st_dev, inode=s.st_ino)
            if stat.S_ISLNK(s.st_mode):
                row.update(kind='symlink', target=os.readlink(str(path)))
            elif stat.S_ISDIR(s.st_mode):
                row['kind'] = 'directory'
                with os.scandir(str(path)):
                    pass
            elif stat.S_ISREG(s.st_mode):
                row['kind'] = 'file'
                if origin != 'collector':
                    row['sha256'] = self.digest(path)
            elif stat.S_ISSOCK(s.st_mode):
                row['kind'] = 'socket'
            elif stat.S_ISFIFO(s.st_mode):
                row['kind'] = 'fifo'
            else:
                row['kind'] = 'special'
            after = path.lstat()
            if (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns) != (after.st_dev, after.st_ino, after.st_mode, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                row.update(kind='changed', error='entry changed during observation')
                row.pop('sha256', None)
        except PermissionError as exc:
            row.update(kind='unreadable', error=str(exc))
        except FileNotFoundError as exc:
            row.update(kind='vanished', error=str(exc))
        except OSError as exc:
            row.update(kind='io-error', error=str(exc))
        return row

    def walk(self, roots):
        admitted = set(self.p['admitted_write_roots'])
        def descend(path):
            self.remaining()
            row = self.record(path)
            yield row
            if row['kind'] == 'directory':
                try:
                    if path.is_symlink():
                        yield {'path': str(path), 'kind': 'changed', 'origin': row['origin'], 'error': 'directory replaced by symlink'}
                        return
                    with os.scandir(str(path)) as entries:
                        for child in entries:
                            yield from descend(Path(child.path))
                except PermissionError as exc:
                    yield {'path': str(path), 'kind': 'unreadable', 'origin': row['origin'], 'error': str(exc)}
                except FileNotFoundError as exc:
                    yield {'path': str(path), 'kind': 'vanished', 'origin': row['origin'], 'error': str(exc)}
                except OSError as exc:
                    yield {'path': str(path), 'kind': 'io-error', 'origin': row['origin'], 'error': str(exc)}
        for root in roots:
            if root not in admitted:
                raise Refusal('Inventory root is not admitted: ' + root)
            path = Path(root)
            if path.is_symlink():
                yield {'path': root, 'kind': 'symlink-root-refused', 'origin': 'baseline'}
                continue
            yield from descend(path)

    def inventory(self):
        totals = {'baseline_logical_bytes': 0, 'collector_logical_bytes': 0,
            'baseline_allocated_bytes': 0, 'collector_allocated_bytes': 0, 'incomplete_observations': 0}
        def rows():
            for row in self.walk(self.p['admitted_write_roots']):
                if row['kind'] == 'file':
                    for metric in ['logical_bytes', 'allocated_bytes']:
                        totals[row['origin'] + '_' + metric] += row[metric]
                if row['kind'] in ['unreadable', 'changed', 'vanished', 'io-error', 'symlink-root-refused']:
                    totals['incomplete_observations'] += 1
                yield row
        receipt = self.stream('inventory', rows())
        self.save('inventory-accounting', totals)
        return {'receipt': str(receipt), 'accounting': totals}

    def download(self, url, name, bound):
        if urllib.parse.urlsplit(url).scheme not in self.p['curl']['allowed_schemes']:
            self.halt('Unadmitted download scheme')
        if type(bound) is not int or bound <= 0 or bound > self.p['per_download_bound_bytes']:
            self.halt('Download bound unresolved or exceeds manifest allowance')
        if Path(name).name != name or name in ('', '.', '..'):
            self.halt('Unsafe download name')
        dest = self.downloads / (hashlib.sha256(url.encode()).hexdigest() + '-' + name)
        self.remaining()
        self.admit_bytes(0)  # Includes cached bytes on every invocation.
        cache = self.receipts / ('download-' + hashlib.sha256(url.encode()).hexdigest() + '.json')
        if dest.exists() or dest.is_symlink():
            if dest.is_symlink() or not cache.is_file() or cache.is_symlink():
                self.halt('Retained incomplete acquisition; no retry')
            prior = json.loads(cache.read_text())
            if prior['url'] != url or dest.stat().st_size != prior['size_bytes'] or prior['size_bytes'] > bound or self.digest(dest) != prior['sha256']:
                self.halt('Retained acquisition identity changed')
            return dest
        self.admit_bytes(bound)  # Reserve the full bound before curl or any payload write.
        self.pending, self.pending_bound = dest, bound
        try:
            timeout = min(self.remaining(), self.p['command_timeout_seconds'])
            argv = list(self.p['curl']['argv_prefix']) + ['--connect-timeout', str(self.p['curl']['connect_timeout_seconds']),
                '--max-time', str(timeout), '--max-filesize', str(bound), '--output', str(dest), url,
                '--write-out', '%{url_effective}\n%{http_code}\n%{size_download}\n']
            raw = self.run(argv).splitlines()
            if len(raw) != 3 or urllib.parse.urlsplit(raw[0]).scheme not in self.p['curl']['allowed_schemes'] or raw[1] not in self.p['curl']['success_http_codes']:
                self.halt('Curl effective URL/status predicate fails')
            if dest.is_symlink() or not dest.is_file() or not 0 < dest.stat().st_size <= bound or float(raw[2]) != dest.stat().st_size:
                self.halt('Empty, over-bound or inconsistent download')
            obs = {'url': url, 'effective_url': raw[0], 'http_status': raw[1],
                'size_bytes': dest.stat().st_size, 'sha256': self.digest(dest)}
            data = encoded(obs)
            self.admit_bytes(len(data), receipt=True)
            self._exclusive(cache, data)
        finally:
            self.pending, self.pending_bound = None, 0
        return dest

    def check_file(self, a, path):
        row = self.record(path)
        if row['kind'] != 'file' or 'sha256' not in row:
            # Collector downloads intentionally skip self-inventory hashing; bind them here.
            if row['kind'] == 'file':
                row['sha256'] = self.digest(path)
            else:
                self.halt('Artifact is not a stable readable file: ' + a['id'])
        if pin(a.get('expected_sha256')) and row['sha256'] != a['expected_sha256']:
            self.halt('Artifact SHA256 mismatch: ' + a['id'])
        if type(a.get('size_bytes')) is int and row['logical_bytes'] != a['size_bytes']:
            self.halt('Artifact size mismatch: ' + a['id'])
        self.save('artifact-bytes', dict(row, entry=a['id'], source_url=a['source_url']))
        return row

    def archive_inventory(self, path):
        def rows():
            with tarfile.open(str(path), 'r|*') as archive:
                for entry in archive:
                    rel = PurePosixPath(entry.name)
                    if rel.is_absolute() or '..' in rel.parts:
                        self.halt('Unsafe archive member')
                    row = {'path': entry.name, 'size_bytes': entry.size, 'mode': entry.mode,
                        'kind': 'file' if entry.isfile() else 'directory' if entry.isdir() else 'symlink' if entry.issym() else 'unsupported'}
                    if entry.isfile():
                        h = hashlib.sha256()
                        with archive.extractfile(entry) as f:
                            for chunk in iter(lambda: f.read(self.p['io_chunk_bytes']), b''):
                                self.remaining()
                                h.update(chunk)
                        row['sha256'] = h.hexdigest()
                    elif entry.issym():
                        row['target'] = entry.linkname
                    yield row
        return self.stream('archive-members', rows())

    def wheel_candidate(self, a, meta):
        p = self.p['wheel']
        if meta['info']['version'] != a['version_revision']:
            raise Refusal('Wheel metadata version mismatch')
        pattern = re.escape(p['distribution'] + '-' + a['version_revision'] + '-' + p['python_tag'] + '-' + p['abi_tag']) + r'-macosx_(\d+)_(\d+)_' + re.escape(p['platform_arch']) + r'\.whl'
        candidates = []
        for u in meta['urls']:
            match = re.fullmatch(pattern, u['filename'])
            if match and tuple(map(int, match.groups())) <= tuple(p['max_platform']) and u['packagetype'] == 'bdist_wheel' and u.get('yanked', False) is False:
                candidates.append(u)
        if len(candidates) != 1:
            raise Refusal('Require exactly one manifest-compatible wheel')
        candidate = candidates[0]
        if number(candidate['size'], 'wheel bytes') > p['compressed_allowance_bytes']:
            raise Refusal('Wheel compressed allowance exceeded')
        return candidate

    def wheel(self, a):
        p = self.p['wheel']
        lock_artifact = self.byid[p['lock_entry_id']]
        lock = Path(lock_artifact['source_url'])
        if not lock.is_file() or lock.is_symlink():
            self.halt('Governing wheel lock path missing; no fallback')
        self.check_file(lock_artifact, lock)
        text = lock.read_text()
        if not text.startswith(p['distribution'] + '==' + a['version_revision'] + ' '):
            self.halt('Wheel lock requirement mismatch')
        hashes = re.findall(r'--hash=sha256:([0-9a-f]{64})', text)
        if len(hashes) != p['lock_hash_count']:
            self.halt('Wheel lock member count mismatch')
        meta = json.loads(self.download(a['metadata_url'], 'wheel-metadata.json', p['metadata_bound_bytes']).read_text())
        candidate = self.wheel_candidate(a, meta)
        if candidate['digests']['sha256'] not in hashes:
            self.halt('Wheel not in governing lock')
        if pin(a['expected_sha256']) and a['expected_sha256'] != candidate['digests']['sha256']:
            self.halt('Wheel metadata changed pinned digest')
        if resolved(a['source_url']) and a['source_url'] != candidate['url']:
            self.halt('Wheel metadata changed pinned URL')
        path = self.download(candidate['url'], candidate['filename'], candidate['size'])
        self.check_file(dict(a, expected_sha256=candidate['digests']['sha256'], size_bytes=candidate['size']), path)
        with zipfile.ZipFile(str(path)) as wheel:
            if sum(e.file_size for e in wheel.infolist()) > p['unpacked_allowance_bytes']:
                self.halt('Wheel unpacked allowance exceeded')
            def rows():
                for entry in wheel.infolist():
                    rel = PurePosixPath(entry.filename)
                    if rel.is_absolute() or '..' in rel.parts:
                        self.halt('Unsafe wheel member')
                    h = hashlib.sha256()
                    with wheel.open(entry) as f:
                        for chunk in iter(lambda: f.read(self.p['io_chunk_bytes']), b''):
                            self.remaining()
                            h.update(chunk)
                    yield {'path': entry.filename, 'size_bytes': entry.file_size, 'sha256': h.hexdigest()}
            self.stream('wheel-members', rows())
        self.save('wheel-selection', candidate)
        return ['source_url', 'size_bytes', 'sha256', 'wheel_lock_membership']

    def compare_installed(self):
        expected = self.m['postinstall']['expected_payloads']
        allowed = self.m['postinstall']['generated_file_allowlist']
        if not isinstance(expected, dict) or not expected or not isinstance(allowed, dict):
            self.halt('Complete actual installed payload rules unresolved')
        roots = [Path(x) for x in self.p['install_roots']]
        for path in set(expected) | set(allowed):
            if not any(Path(path) == r or r in Path(path).parents for r in roots):
                self.halt('Payload expectation outside install roots')
        seen = set()
        def rows():
            for row in self.walk(self.p['install_roots']):
                path = row['path']
                rule = expected.get(path, allowed.get(path))
                if rule is None:
                    self.halt('Unexpected actual installed entry: ' + path)
                seen.add(path)
                if row['kind'] != rule['kind'] or row['mode'] != rule['mode']:
                    self.halt('Installed type/mode mismatch: ' + path)
                if row['kind'] == 'file':
                    if 'sha256' in rule and row.get('sha256') != rule['sha256']:
                        self.halt('Installed digest mismatch: ' + path)
                    if path in expected and 'sha256' not in rule:
                        self.halt('Expected file digest missing: ' + path)
                    if path in allowed and ('max_bytes' not in rule or row['logical_bytes'] > number(rule['max_bytes'], 'generated file bound')):
                        self.halt('Generated file bound missing/exceeded: ' + path)
                if row['kind'] == 'symlink' and row['target'] != rule['target']:
                    self.halt('Installed symlink mismatch: ' + path)
                yield row
        receipt = self.stream('installed-files', rows())
        if set(expected) - seen:
            self.halt('Missing installed expected entries')
        return str(receipt)

    def result(self, mode, entry, established):
        fields = self.p['identity_fields']
        if mode not in self.p['allowed_modes'] or not set(established).issubset(set(fields)):
            raise Refusal('Unadmitted result mode/identity field')
        return {'mode': mode, 'entry': entry, 'status': 'OBSERVATION-ONLY',
            'established': list(established), 'remaining_open': [x for x in fields if x not in established],
            'elapsed_seconds': self.elapsed(), 'retained_dir': str(self.root)}

    def collect(self, mode, entry=None):
        if mode not in self.p['allowed_modes']:
            raise Refusal('Unadmitted mode')
        fields = []
        if mode == 'inventory':
            self.inventory()  # Filesystem observations do not establish host/toolchain completeness.
        elif mode == 'guard':
            self.save('admission', admission(self.m, json.loads(Path(entry).read_text())))
            fields = ['host', 'paths', 'budget']
        elif mode == 'compare-installed':
            self.compare_installed()
            fields = ['payloads']
        elif mode == 'tree':
            for name in ['ports-tar', 'ports-tar-signature', 'ports-rmd160', 'portindex', 'portindex-quick', 'portindex-signature', 'macports-key']:
                a = self.byid[name]
                self.check_file(a, a['source_url'])
            self.archive_inventory(self.byid['ports-tar']['source_url'])
            fields = ['source_url', 'size_bytes', 'sha256']
        else:
            if entry not in self.byid:
                self.halt('Exact artifact ID required')
            a = self.byid[entry]
            source = a['source_url']
            if mode == 'wheel':
                fields = self.wheel(a)
            elif mode == 'archive-index':
                p = self.p['archive_index']
                url = p['url_template'].format(name=a['name'])
                path = self.download(url, 'index.html', p['bound_bytes'])
                names = re.findall(r'href="([^"/]+\.tbz2)"', path.read_text())
                pattern = re.escape(a['name'] + '-' + a['version_revision']) + r'(?:\+[^./]+)*\.' + re.escape(p['platform_tag']) + r'\.(?:' + '|'.join(re.escape(x) for x in p['architectures']) + r')\.tbz2'
                names = [x for x in names if re.fullmatch(pattern, x)]
                if not names:
                    self.halt('No compatible archive candidate; no source fallback')
                self.save('archive-candidates', {'names': names})
                fields = ['archive_candidates']
            elif mode == 'source-plan':
                if not a.get('portfile_path'):
                    self.halt('Exact pinned Portfile path missing; no port subprocess')
                recipe = Path(a['portfile_path'])
                root = Path(self.m['tree']['root']).resolve()
                if root not in recipe.resolve().parents:
                    self.halt('Recipe outside pinned tree')
                self.check_file(dict(a, expected_sha256=a.get('portfile_sha256'), size_bytes=None), recipe)
                fields = ['recipe']
            elif mode == 'r3':
                if a['route'] != 'supplied local artifact' or not Path(source).is_absolute() or not pin(a['expected_sha256']):
                    self.halt('Reviewed supplied local artifact path/pin absent')
                self.check_file(a, source)
                fields = ['source_url', 'size_bytes', 'sha256']
            elif mode in ['fetch', 'inspect']:
                if source.startswith('manifest:'):
                    parent = self.byid[source.split(':', 1)[1]]
                    path = self.download(parent['source_url'], 'parent-archive', parent['size_bytes'])
                    self.check_file(parent, path)
                    self.archive_inventory(path)
                    # Parent members do not establish this derived artifact's ABI or interface.
                elif Path(source).is_absolute():
                    if Path(source).is_dir():
                        self.save('directory-metadata', self.record(source))
                        fields = ['source_url']
                    else:
                        self.check_file(a, source)
                        fields = ['source_url', 'size_bytes', 'sha256']
                else:
                    path = self.download(source, 'artifact', a['size_bytes'])
                    self.check_file(a, path)
                    if a['route'] == 'binary archive':
                        signature = self.download(a['signature_url'], 'signature', self.p['signature_bound_bytes'])
                        self.check_file(dict(a, id=a['id'] + ':signature', source_url=a['signature_url'], expected_sha256=a.get('signature_sha256'), size_bytes=None), signature)
                    if 'checksum_url' in a:
                        checksum = self.download(a['checksum_url'], 'checksum', self.p['checksum_bound_bytes'])
                        text = checksum.read_text().strip()
                        match = re.fullmatch(r'([0-9a-fA-F]{64})(?:\s+\*?([^\s]+))?', text)
                        if not match or match[1].lower() != self.digest(path) or (match[2] and match[2] != source.rsplit('/', 1)[1]):
                            self.halt('Published checksum mismatch')
                    self.archive_inventory(path)
                    fields = ['source_url', 'size_bytes', 'sha256']
            else:
                self.halt('Mode lacks a reviewed collector implementation')
        result = self.result(mode, entry, fields)
        self.save('summary', result)
        return result


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) not in (2, 3):
        raise Refusal('usage: MODE MANIFEST [ARTIFACT_ID_OR_OBSERVATION]')
    mode, manifest_path = argv[:2]
    manifest = json.loads(Path(manifest_path).read_text())
    if mode not in manifest['collector']['allowed_modes']:
        raise Refusal('Unadmitted mode; no writes')
    tool = manifest['collector']['interpreter']
    if sys.version_info[:2] < tuple(tool['minimum_version']) or sys.executable != tool['reported_executable'] or not sys.flags.isolated or not sys.dont_write_bytecode:
        raise Refusal('Pinned isolated interpreter/flags required')
    collector = Collector(manifest, mode)
    try:
        result = collector.collect(mode, argv[2] if len(argv) == 3 else None)
        print(json.dumps(result, sort_keys=True))
        return 0
    except Exception as exc:
        collector.halt(exc)
    finally:
        collector.close()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (Refusal, OSError, ValueError, KeyError) as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
