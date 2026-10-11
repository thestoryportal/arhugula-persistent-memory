"""Prospective stdlib collector. Observations never authorize provisioning."""
import fcntl
import hashlib
import argparse
import datetime
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

PROCESS_START = globals().get('PROCESS_START_MONOTONIC', time.monotonic())

# The fixed stdin stub supplies r1h_identity_probe.py from verified bytes.
interpreter_identity = VERIFIED_PROBE['interpreter_identity']
stdlib_identity = VERIFIED_PROBE['stdlib_identity']


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


def covers(parent, child):
    return child == parent or child.startswith(parent + '/')


def core_projection(manifest):
    seal = manifest['window_seal']
    keys, slots = seal['core_keys'], seal['evidence_slots']
    if not isinstance(keys, list) or not keys or len(set(keys)) != len(keys):
        raise Refusal('Invalid core key list')
    if not isinstance(slots, list) or len(set(slots)) != len(slots):
        raise Refusal('Invalid evidence slot list')
    for path in keys + slots:
        if not isinstance(path, str) or not path.startswith('/') or path.endswith('/') or '~' in path:
            raise Refusal('Canonical absolute JSON paths required')
        pointer(manifest, path)
    if any(covers(a, b) or covers(b, a) for a in keys for b in slots):
        raise Refusal('Evidence slot overlaps frozen core')
    if any(covers(a, b) or covers(b, a) for i, a in enumerate(slots) for b in slots[i + 1:]):
        raise Refusal('Overlapping evidence slots')
    required = ['/window_seal/core_keys', '/window_seal/evidence_slots', '/window_seal/artifact_ids',
        '/paths', '/preinstall']
    required += ['/budget/' + name for name in ['clock_seconds', 'setup_cap_bytes',
        'free_floor_bytes', 'additional_headroom_bytes', 'components', 'planned_peak_bytes']]
    for name in manifest['collector']:
        if name == 'child_contract':
            required += ['/collector/child_contract/' + field
                for field in manifest['collector'][name] if field != 'sha256']
        else:
            required.append('/collector/' + name)
    required += ['/authorization/' + name for name in ['staging', 'building', 'installation']]
    for path in required:
        if not any(covers(key, path) for key in keys):
            raise Refusal('Required policy missing from core: ' + path)
    if seal['artifact_ids'] != [a['id'] for a in manifest['artifacts']]:
        raise Refusal('Artifact membership differs from sealed policy')
    evidence_or_core = ['/collector/child_contract/sha256']
    for section in ['budget', 'tree', 'postinstall']:
        evidence_or_core += ['/' + section + '/' + name for name in manifest[section]]
    for i, artifact in enumerate(manifest['artifacts']):
        evidence_or_core += ['/artifacts/%d/%s' % (i, name) for name in artifact]
    for path in evidence_or_core:
        if not any(covers(key, path) for key in keys + slots):
            raise Refusal('Unsealed policy/evidence field: ' + path)
    for name in manifest['preinstall']['host_fields']:
        path = '/host/' + name
        if not any(covers(key, path) for key in keys + slots):
            raise Refusal('Host predicate missing from core/evidence slots: ' + path)
    return {path: pointer(manifest, path) for path in keys}


def core_digest(manifest):
    try:
        return hashlib.sha256(encoded(core_projection(manifest))).hexdigest()
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise Refusal('Malformed frozen core: ' + str(exc)) from exc


def verify_capture(capture, expected):
    if not pin(expected) or not isinstance(capture, bytes) or hashlib.sha256(capture).hexdigest() != expected:
        raise Refusal('Complete binder capture SHA-256 mismatch; no writes or clock')
    try:
        publication = json.loads(capture)
        if set(publication) != {'bound_manifest_json', 'binding_receipt'}:
            raise Refusal('Malformed complete binder capture')
        raw = publication['bound_manifest_json'].encode('utf-8')
        receipt = publication['binding_receipt']
        if hashlib.sha256(raw).hexdigest() != receipt['bound_manifest_sha256']:
            raise Refusal('Bound manifest bytes differ from binding receipt')
        manifest = json.loads(raw)
        if encoded(manifest) != raw:
            raise Refusal('Noncanonical bound manifest publication')
        return manifest, receipt
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise Refusal('Malformed binder capture: ' + str(exc)) from exc


def utc_seconds(text):
    if not isinstance(text, str) or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', text):
        raise Refusal('Invalid bootstrap UTC start')
    try:
        return datetime.datetime.strptime(text, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).timestamp()
    except ValueError as exc:
        raise Refusal('Invalid bootstrap UTC start') from exc


def verify_binding(manifest):
    """Second layer: reconstruct the reviewed source core from verified members."""
    try:
        p = manifest['binding_provenance']
        expected = {'v7_sha256', 'probe_file_sha256', 'binder_sha256', 'collector_sha256',
            'identity_probe_sha256', 'utc_time', 'bound_core_sha256', 'probe_json'}
        if set(p) != expected or not all(pin(p[k]) for k in expected - {'utc_time', 'probe_json'}):
            raise Refusal('Unbound or malformed binding provenance')
        utc_seconds(p['utc_time'])
        names = {'v7_sha256': 'manifest', 'collector_sha256': 'collector',
            'binder_sha256': 'binder', 'identity_probe_sha256': 'identity'}
        for key, name in names.items():
            if hashlib.sha256(VERIFIED_MEMBERS[name]).hexdigest() != p[key]:
                raise Refusal('Binding provenance input mismatch: ' + key)
        raw_probe = p['probe_json'].encode('utf-8')
        identity = manifest['collector']['interpreter']['identity']
        if hashlib.sha256(raw_probe).hexdigest() != p['probe_file_sha256'] or json.loads(raw_probe) != identity:
            raise Refusal('Bound probe provenance differs from identity')
        source = json.loads(VERIFIED_MEMBERS['manifest'])
        if source['window_seal']['core_sha256'] != 'NEEDS-FETCH' or any(
                v != 'NEEDS-FETCH' for v in source['collector']['interpreter']['identity'].values()):
            raise Refusal('Reviewed source must remain unbound')
        source['collector']['interpreter']['identity'] = identity
        digest = core_digest(source)
        if digest != p['bound_core_sha256'] or digest != manifest['window_seal']['core_sha256'] or digest != core_digest(manifest):
            raise Refusal('Bound core differs from reviewed source; resealing refused')
    except (KeyError, TypeError, ValueError) as exc:
        raise Refusal('Binding provenance cannot verify: ' + str(exc)) from exc


def qualify_interpreter(manifest):
    tool = manifest['collector']['interpreter']
    bound = tool['identity']
    if not isinstance(bound, dict) or 'NEEDS-FETCH' in json.dumps(bound):
        raise Refusal('Interpreter identity unbound; no clock or writes')
    actual = interpreter_identity()
    # Normalize the JSON array returned by platform.mac_ver().
    actual = json.loads(encoded(actual))
    if actual != bound:
        raise Refusal('Running interpreter identity differs from frozen identity')
    if os.path.realpath(tool['executable']) != bound['realpath'] or actual['executable'] != bound['executable']:
        raise Refusal('Interpreter executable disagrees with manifest')
    if tool['flags'] != ['-I', '-B'] or actual['flags'] != {'isolated': 1, 'dont_write_bytecode': 1}:
        raise Refusal('Interpreter isolation flags disagree with manifest')
    if tuple(actual['version_info'][:2]) < tuple(tool['minimum_version']):
        raise Refusal('Interpreter below manifest minimum version')
    if not pin(bound['executable_sha256']) or not pin(bound['stdlib']['sha256']):
        raise Refusal('Interpreter content identity must have SHA-256 pins')


def acquisition_gate(manifest, mode, entry=None):
    if manifest['collector']['child_contract']['reviewed'] is True:
        return
    if mode in ['fetch', 'wheel', 'archive-index']:
        raise Refusal('Acquisition disabled; reviewed child contract absent; no writes')
    if mode == 'inspect':
        artifacts = {a['id']: a for a in manifest['artifacts']}
        if entry not in artifacts or not Path(artifacts[entry]['source_url']).is_absolute():
            raise Refusal('Network-backed inspect disabled; no writes')


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
    def __init__(self, capture, mode, now=None, monotonic=None, runner=None, entry=None,
            expected_anchor=None, expected_capture_sha256=None, bootstrap_bytes=None,
            remaining_seconds=None, process_start=None):
        manifest, binding_receipt = verify_capture(capture, expected_capture_sha256)
        self.capture_sha256 = expected_capture_sha256
        self.bootstrap_start_utc = binding_receipt['bootstrap_start_utc']
        self.bootstrap_wall = utc_seconds(self.bootstrap_start_utc)
        self.remote_budget = remaining_seconds
        self.process_start = process_start
        if type(bootstrap_bytes) is not int or bootstrap_bytes < len(capture) + len(b'0\n'):
            raise Refusal('Bootstrap bytes must include capture, stderr and exit status')
        self.bootstrap_bytes = bootstrap_bytes
        if expected_anchor != 'none' and (not isinstance(expected_anchor, str) or
                not re.fullmatch(r'(0|[1-9][0-9]*):[0-9a-f]{64}', expected_anchor)):
            raise Refusal('Exact expected anchor required; no writes or clock')
        self.expected_anchor = expected_anchor
        self.initial_evidence = json.loads(encoded({path: pointer(manifest, path)
            for path in manifest['window_seal']['evidence_slots']}))
        seal_hash = core_digest(manifest)
        if not pin(manifest['window_seal']['core_sha256']) or manifest['window_seal']['core_sha256'] != seal_hash:
            raise Refusal('Frozen core digest unbound or changed; no writes or fresh clock')
        verify_binding(manifest)
        self.m = manifest
        self.p = manifest['collector']
        if mode not in self.p['allowed_modes']:
            raise Refusal('Unadmitted mode; no writes')
        acquisition_gate(manifest, mode, entry)
        qualify_interpreter(manifest)
        self.mode = mode
        self.now = now or time.time
        self.monotonic = monotonic or time.monotonic
        self.runner = runner or self._execute
        self.lock_fd = None
        self.pending = None
        self.pending_bound = 0
        self.active_argv = None
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
        components = self.m['budget']['components']
        if not components or len({row['id'] for row in components}) != len(components):
            raise Refusal('Incomplete or duplicate budget components')
        if sum(number(row['bytes'], row['id']) for row in components) != self.m['budget']['planned_peak_bytes']:
            raise Refusal('Manifest peak disagrees with component sum')
        if [row['bytes'] for row in components if row['id'] == 'receipts'] != [self.p['receipt_limit_bytes']]:
            raise Refusal('Receipt allowance disagrees with budget component')
        self.root = Path(self.p['retained_dir'])
        admitted = [Path(x) for x in self.p['admitted_write_roots']]
        if not self.root.is_absolute() or self.root not in admitted:
            raise Refusal('Exact absolute retained root must be admitted')
        if any(x != self.root and x in self.root.parents for x in admitted):
            raise Refusal('Broad parent of retained root cannot be inventoried')
        if not set(self.p['install_roots']).issubset(set(self.p['admitted_write_roots'])):
            raise Refusal('Install roots outside admitted write roots')
        self.registration = Path(self.p['registration_path'])
        self.registration_root = self.registration.parent
        if not self.registration.is_absolute() or self.registration_root not in admitted:
            raise Refusal('Dedicated registration root must be admitted')
        protected = [self.root] + [Path(x) for x in self.p['install_roots']]
        if any(r == self.registration_root or r in self.registration_root.parents or
                self.registration_root in r.parents for r in protected):
            raise Refusal('Registration root overlaps retained/install roots')
        if any(r != self.registration_root and r in self.registration_root.parents for r in admitted):
            raise Refusal('Broad parent of registration root refused')
        self.receipts = self.root / 'receipts'
        self.downloads = self.root / 'downloads'
        self.registry_bytes = 0
        self.registry_head = seal_hash
        self.registry_seq = -1
        self.registered = {}
        self.writing_bytes = 0
        failure_path = str(self.receipts / 'failure.json')
        self.halt_reservation = sum(len(encoded({'previous_sha256': '0' * 64, 'event': event})) for event in [
            {'kind': 'begin', 'path': failure_path},
            {'kind': 'commit', 'path': failure_path, 'size': self.p['failure_reserve_bytes'], 'sha256': '0' * 64}])
        self.incomplete = None
        resuming = self.registration_root.exists() or self.registration_root.is_symlink()
        try:
            if self.registration_root.exists() or self.registration_root.is_symlink():
                # Validate all prior state before reading either clock or writing anything.
                if expected_anchor == 'none':
                    raise Refusal('Expected anchor none but registration exists; no clock')
                self._open_registration()
                self._read_registration(seal_hash)
                self._verify_registered()
            else:
                if expected_anchor != 'none':
                    raise Refusal('Expected anchor differs from missing registration; no clock')
                if self.root.exists() or self.root.is_symlink():
                    raise Refusal('Retained state without registration; no new clock')
                self._start_budget()
                self.start = {'wall_start': self.bootstrap_wall,
                    'monotonic_start': self.process_start,
                    'bootstrap_start_utc': self.bootstrap_start_utc, 'bootstrap_bytes': bootstrap_bytes,
                    'capture_sha256': expected_capture_sha256,
                    'hostname': os.uname().nodename, 'seal_sha256': seal_hash,
                    'creation_identity': uuid.uuid4().hex,
                    'evidence_initial': self.initial_evidence}
                self._check_write(0)
                self.registration_root.mkdir(mode=0o700)  # Exclusive directory reservation.
                self._boundary('registration.mkdir')
                self._syncdir(self.registration_root.parent)
                self.lock_fd = os.open(str(self.registration_root), os.O_RDONLY)
                fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self._journal({'kind': 'start', 'start': self.start, 'retained_dir': str(self.root)}, exclusive=True)
                self._check_write(0)
                self.root.mkdir(mode=0o700)
                self._boundary('retained.mkdir')
                self._syncdir(self.root.parent)
                self.root_identity = self._directory_identity(self.root)
                self._journal({'kind': 'root', 'identity': self.root_identity})
                self._check_write(0)
                self.receipts.mkdir(mode=0o700)
                self._boundary('receipts.mkdir')
                self._check_write(0)
                self.downloads.mkdir(mode=0o700)
                self._boundary('downloads.mkdir')
                self._syncdir(self.root)
                self._exclusive(self.root / 'window.json', encoded(self.start))
                self._exclusive(self.receipts / 'failure.json', encoded({'status': 'READY'}).ljust(self.p['failure_reserve_bytes'], b' '))
                self._journal({'kind': 'ready'})
            for path in [self.receipts, self.downloads]:
                if path.is_symlink() or not path.is_dir():
                    raise Refusal('Missing or symlink collector namespace')
            self.evidence = self.read_evidence()
            if (self.start['capture_sha256'] != expected_capture_sha256 or
                    self.start['bootstrap_start_utc'] != self.bootstrap_start_utc or
                    self.start['bootstrap_bytes'] != bootstrap_bytes or
                    self.start['evidence_initial'] != self.initial_evidence):
                raise Refusal('Registration initial publication/bootstrap differs; no new clock')
            for slot, initial in self.start['evidence_initial'].items():
                supplied = pointer(self.m, slot)
                value = self.evidence.get(slot, initial)
                if supplied != initial and supplied != value:
                    raise Refusal('Evidence slot changed without a chained ledger record: ' + slot)
                self.set_slot(slot, value)
            failure = json.loads((self.receipts / 'failure.json').read_text())
            if failure['status'] != 'READY':
                raise Refusal('Window has retained failure; no retry/reset')
            self._start_budget()
            self.remaining()
            self.admit_bytes(0)
        except BaseException as exc:
            self.close()
            if resuming and isinstance(exc, OSError):
                raise Refusal('Missing/inaccessible retained registration state: ' + str(exc)) from exc
            raise

    def close(self):
        if self.lock_fd is not None:
            os.close(self.lock_fd)
            self.lock_fd = None

    def _boundary(self, label):
        """Fault-injection observation point after a persistence operation."""

    def _emit_anchor(self):
        print('R1H-ANCHOR %s %d %s' % (self.start['seal_sha256'], self.registry_seq, self.registry_head), flush=True)

    def _syncdir(self, path):
        fd = os.open(str(path), os.O_RDONLY)
        try:
            os.fsync(fd)
            self._boundary('directory.fsync')
        finally:
            os.close(fd)

    @staticmethod
    def _directory_identity(path):
        s = path.lstat()
        if not stat.S_ISDIR(s.st_mode) or s.st_uid != os.getuid() or stat.S_IMODE(s.st_mode) != 0o700:
            raise Refusal('Collector directory must be user-owned mode 0700')
        return {'device': s.st_dev, 'inode': s.st_ino,
            'birth_time': getattr(s, 'st_birthtime', None)}

    def _check_registration_namespace(self):
        self._directory_identity(self.registration_root)
        if self.registration.is_symlink() or not self.registration.is_file():
            raise Refusal('Missing or invalid window registration; no new clock')
        if set(self.registration_root.iterdir()) != {self.registration}:
            raise Refusal('Unexpected registration namespace entry')

    def _open_registration(self):
        self._check_registration_namespace()
        self.lock_fd = os.open(str(self.registration_root), os.O_RDONLY)
        fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def _read_registration(self, seal_hash):
        ready = False
        self.start = None
        self.root_identity = None
        with self.registration.open('rb') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    if not line.endswith(b'\n') or encoded(record) != line or set(record) != {'previous_sha256', 'event'} or record['previous_sha256'] != self.registry_head:
                        raise Refusal('Interrupted/edited registration chain')
                    event = record['event']
                    kind = event['kind']
                    if self.start is None:
                        if kind != 'start' or event['retained_dir'] != str(self.root) or event['start']['seal_sha256'] != seal_hash or event['start']['hostname'] != os.uname().nodename:
                            raise Refusal('Registration core/host/path differs')
                        self.start = event['start']
                    elif kind == 'root' and self.root_identity is None and not ready:
                        self.root_identity = event['identity']
                    elif kind == 'begin' and self.incomplete is None:
                        self.incomplete = event['path']
                    elif kind == 'commit' and self.incomplete == event['path']:
                        if set(event) != {'kind', 'path', 'size', 'sha256'} or not pin(event['sha256']):
                            raise Refusal('Invalid registration receipt identity')
                        number(event['size'], 'registered receipt bytes')
                        self.registered[event['path']] = {'size': event['size'], 'sha256': event['sha256']}
                        self.incomplete = None
                    elif kind == 'ready' and not ready and self.root_identity is not None and self.incomplete is None:
                        ready = True
                    else:
                        raise Refusal('Incomplete or invalid registration transition')
                    self.registry_bytes += len(line)
                    self.registry_head = hashlib.sha256(line).hexdigest()
                    self.registry_seq += 1
                except (ValueError, TypeError, KeyError) as exc:
                    raise Refusal('Malformed registration chain') from exc
        if '%d:%s' % (self.registry_seq, self.registry_head) != self.expected_anchor:
            raise Refusal('Registration head differs from independently trusted anchor; no new clock')
        if not ready or self.incomplete is not None:
            raise Refusal('Interrupted registration/write; no new clock')
        if self._directory_identity(self.root) != self.root_identity:
            raise Refusal('Missing/replaced retained directory; no new clock')
        if json.loads((self.root / 'window.json').read_bytes()) != self.start:
            raise Refusal('Window creation identity differs from registration')

    def _verify_registered(self):
        found = set()
        allowed_dirs = {self.root, self.receipts, self.downloads}
        for path in self._paths(self.root):
            s = path.lstat()
            if stat.S_ISDIR(s.st_mode):
                if path not in allowed_dirs:
                    raise Refusal('Added collector directory')
            elif stat.S_ISREG(s.st_mode):
                key = str(path)
                if key not in self.registered:
                    raise Refusal('Added/unregistered receipt or interrupted append')
                h, size = hashlib.sha256(), 0
                with path.open('rb') as f:
                    for chunk in iter(lambda: f.read(self.p['io_chunk_bytes']), b''):
                        h.update(chunk)
                        size += len(chunk)
                expected = self.registered[key]
                if size != expected['size'] or h.hexdigest() != expected['sha256']:
                    raise Refusal('Earlier receipt content differs from registration')
                found.add(key)
            else:
                raise Refusal('Unsupported/replaced collector receipt')
        if found != set(self.registered):
            raise Refusal('Missing registered receipt')
        if json.loads((self.receipts / 'failure.json').read_bytes())['status'] == 'HALTED':
            self.halt_reservation = 0

    def _check_write(self, amount):
        if not (self.receipts / 'failure.json').exists():
            if min(self.m['budget']['clock_seconds'], self.m['budget'].get('time_total_s', self.m['budget']['clock_seconds'])) - self.elapsed() <= 0:
                raise Refusal('Cumulative deadline before initial persistence')
        else:
            self.remaining()
        self.admit_bytes(amount, receipt=True)

    def _journal(self, event, exclusive=False, emergency=False):
        data = encoded({'previous_sha256': self.registry_head, 'event': event})
        if not emergency:
            self._check_write(len(data))
        with self.registration.open('xb' if exclusive else 'ab') as f:
            if exclusive:
                self._boundary('journal.create')
            f.write(data)
            self._boundary('journal.write')
            f.flush()
            self._boundary('journal.flush')
            os.fsync(f.fileno())
            self._boundary('journal.fsync')
        self._syncdir(self.registration_root)
        self.registry_bytes += len(data)
        self.registry_head = hashlib.sha256(data).hexdigest()
        self.registry_seq += 1
        self._emit_anchor()

    def _begin(self, path, emergency=False):
        if self.incomplete is not None and not emergency:
            raise Refusal('Interrupted write in this invocation')
        self._journal({'kind': 'begin', 'path': str(path)}, emergency=emergency)
        self.incomplete = str(path)

    def _commit(self, path, size, digest, emergency=False):
        self._journal({'kind': 'commit', 'path': str(path), 'size': size, 'sha256': digest}, emergency=emergency)
        self.registered[str(path)] = {'size': size, 'sha256': digest}
        self.incomplete = None
        self.writing_bytes = 0

    def _exclusive(self, path, data):
        self._check_write(len(data))
        self._begin(path)
        self._check_write(len(data))
        with path.open('xb') as f:
            self._boundary('exclusive.open')
            f.write(data)
            self._boundary('exclusive.write')
            f.flush()
            self._boundary('exclusive.flush')
            os.fsync(f.fileno())
            self._boundary('exclusive.fsync')
        self.writing_bytes = len(data)
        self._syncdir(path.parent)
        self._commit(path, len(data), hashlib.sha256(data).hexdigest())

    def set_slot(self, slot, value):
        parent, key = slot.rsplit('/', 1)
        container = pointer(self.m, parent)
        if isinstance(container, list):
            container[int(key)] = value
        else:
            container[key] = value

    def read_evidence(self):
        path = self.root / 'evidence.jsonl'
        if path.is_symlink():
            raise Refusal('Evidence ledger symlink refused')
        values, head, count = {}, self.start['seal_sha256'], 0
        if path.exists():
            if not path.is_file():
                raise Refusal('Evidence ledger must be a regular file')
            if not path.read_bytes():
                raise Refusal('Empty evidence ledger is an interrupted append')
            with path.open('rb') as f:
                for line in f:
                    if not line.endswith(b'\n'):
                        raise Refusal('Truncated evidence record')
                    try:
                        record = json.loads(line)
                    except ValueError as exc:
                        raise Refusal('Malformed evidence record') from exc
                    if not isinstance(record, dict) or set(record) != {'seal_sha256', 'previous_sha256', 'slot', 'value'} or encoded(record) != line:
                        raise Refusal('Edited or noncanonical evidence record')
                    slot = record['slot']
                    if slot not in self.m['window_seal']['evidence_slots'] or slot in values:
                        raise Refusal('Unadmitted or already filled evidence slot')
                    if record['seal_sha256'] != self.start['seal_sha256'] or record['previous_sha256'] != head:
                        raise Refusal('Evidence hash chain differs from sealed window')
                    values[slot] = record['value']
                    head = hashlib.sha256(line).hexdigest()
                    count += 1
                    checkpoint = self.receipts / ('evidence-head-%d.json' % count)
                    if checkpoint.is_symlink() or not checkpoint.is_file():
                        raise Refusal('Incomplete evidence append checkpoint')
                    if json.loads(checkpoint.read_bytes()) != {'seal_sha256': self.start['seal_sha256'],
                            'record_count': count, 'head_sha256': head}:
                        raise Refusal('Edited earlier evidence record')
        # Independent immutable heads catch removal of even the final complete line.
        if len(list(self.receipts.glob('evidence-head-*.json'))) != count:
            raise Refusal('Truncated evidence ledger or orphan checkpoint')
        self.evidence_head, self.evidence_count = head, count
        return values

    def append_evidence(self, slot, value):
        self._verify_registered()  # Preserve the registered prefix before any rewrite/append.
        values = self.read_evidence()
        if slot not in self.m['window_seal']['evidence_slots'] or slot in values:
            raise Refusal('Unadmitted or already filled evidence slot; no writes')
        record = {'seal_sha256': self.start['seal_sha256'], 'previous_sha256': self.evidence_head,
            'slot': slot, 'value': value}
        data = encoded(record)
        checkpoint = encoded({'seal_sha256': self.start['seal_sha256'],
            'record_count': self.evidence_count + 1, 'head_sha256': hashlib.sha256(data).hexdigest()})
        self.remaining()
        self.admit_bytes(len(data) + len(checkpoint), receipt=True)
        path = self.root / 'evidence.jsonl'
        self._begin(path)
        # Exclusive creation makes the empty-before-first-record boundary observable.
        if not path.exists():
            with path.open('xb') as f:
                self._boundary('evidence.create')
                f.flush()
                self._boundary('evidence.empty.flush')
                os.fsync(f.fileno())
                self._boundary('evidence.empty.fsync')
            self._syncdir(self.root)
        self._check_write(len(data))
        with path.open('ab') as f:
            self._boundary('evidence.open')
            f.write(data)
            self._boundary('evidence.write')
            f.flush()
            self._boundary('evidence.flush')
            os.fsync(f.fileno())
            self._boundary('evidence.fsync')
        prior_size = self.registered.get(str(path), {}).get('size', 0)
        self.writing_bytes = len(data)
        self._syncdir(self.root)
        self._commit(path, prior_size + len(data), hashlib.sha256(path.read_bytes()).hexdigest())
        self._exclusive(self.receipts / ('evidence-head-%d.json' % (self.evidence_count + 1)), checkpoint)
        self.evidence = self.read_evidence()
        self.set_slot(slot, value)
        self.remaining()

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
        padded = data.ljust(self.p['failure_reserve_bytes'], b' ')
        self._begin(path, emergency=True)
        with path.open('r+b') as f:
            self._boundary('halt.open')
            f.write(padded)
            self._boundary('halt.write')
            f.flush()
            self._boundary('halt.flush')
            os.fsync(f.fileno())
            self._boundary('halt.fsync')
        self._syncdir(self.receipts)
        self._commit(path, len(padded), hashlib.sha256(padded).hexdigest(), emergency=True)
        self.halt_reservation = 0
        raise Refusal(str(error))

    def _start_budget(self):
        limit = min(self.m['budget']['clock_seconds'], self.m['budget'].get('time_total_s', self.m['budget']['clock_seconds']))
        if type(self.remote_budget) not in (int, float) or not math.isfinite(self.remote_budget) or not 0 < self.remote_budget <= limit:
            raise Refusal('Invalid or expired M3 remaining budget/deadline')
        if self.process_start is None:
            self.process_start = PROCESS_START

    def elapsed(self):
        self._start_budget()
        mono = self.monotonic() - self.process_start
        if mono < 0:
            raise Refusal('Process monotonic clock rollback; never restart')
        limit = min(self.m['budget']['clock_seconds'], self.m['budget'].get('time_total_s', self.m['budget']['clock_seconds']))
        return limit - self.remote_budget + mono

    def remaining(self):
        try:
            remaining = min(self.m['budget']['clock_seconds'], self.m['budget'].get('time_total_s', self.m['budget']['clock_seconds'])) - self.elapsed()
        except Refusal as exc:
            self.halt(exc, argv=self.active_argv, elapsed=0)
        if remaining <= 0:
            self.halt('Cumulative provisioning deadline exceeded', argv=self.active_argv)
        return remaining

    def _paths(self, root):
        yield root
        s = root.lstat()
        if stat.S_ISDIR(s.st_mode):
            with os.scandir(str(root)) as entries:
                for entry in entries:
                    yield from self._paths(Path(entry.path))

    def usage(self):
        receipts = self.bootstrap_bytes + self.registry_bytes + self.halt_reservation
        downloads = 0
        for path, record in self.registered.items():
            if Path(path).parent == self.downloads:
                if Path(path) != self.pending:
                    downloads += record['size']
            else:
                receipts += record['size']
        receipts += self.writing_bytes
        return {'receipt_bytes': receipts, 'download_bytes': downloads,
            'staging_bytes': receipts + downloads + self.pending_bound}

    def admit_bytes(self, amount, receipt=False):
        number(amount, 'additional bytes')
        used = self.usage()
        if receipt and used['receipt_bytes'] + amount > self.p['receipt_limit_bytes']:
            if not (self.receipts / 'failure.json').exists():
                raise Refusal('Initial receipt allowance too small')
            self.halt('Cumulative receipt limit exceeded')
        if used['staging_bytes'] + amount > self.p['staging_bound_bytes']:
            if not (self.receipts / 'failure.json').exists():
                raise Refusal('Initial staging allowance too small')
            self.halt('Cumulative staging bound exceeded before write')

    def stream(self, label, rows):
        path = self.receipts / (label + '-' + uuid.uuid4().hex + '.jsonl')
        self._begin(path)
        h, size = hashlib.sha256(), 0
        with path.open('xb', buffering=0) as f:
            self._boundary('stream.open')
            for row in rows:
                data = encoded(row)
                self._check_write(len(data))
                f.write(data)
                self._boundary('stream.write')
                self.writing_bytes += len(data)
                size += len(data)
                h.update(data)
                os.fsync(f.fileno())
                self._boundary('stream.fsync')
        self._syncdir(self.receipts)
        self._commit(path, size, h.hexdigest())
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
        self.active_argv = argv
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
        finally:
            self.active_argv = None

    def digest(self, path):
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(self.p['io_chunk_bytes']), b''):
                self.remaining()
                h.update(chunk)
        return h.hexdigest()

    def record(self, path):
        path = Path(path)
        origin = 'collector' if path in [self.registration_root, self.registration, self.root, self.root / 'window.json', self.root / 'evidence.jsonl'] or any(r == path or r in path.parents for r in [self.receipts, self.downloads]) else 'baseline'
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
            self._begin(dest)
            self._commit(dest, obs['size_bytes'], obs['sha256'])
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

    def verify_evidence(self):
        values = self.read_evidence()
        for slot, initial in self.start['evidence_initial'].items():
            if pointer(self.m, slot) != values.get(slot, initial):
                raise Refusal('Evidence changed outside the ledger: ' + slot)

    def verify_final(self):
        self._check_registration_namespace()
        seq, head = self.registry_seq, self.registry_head
        self.registry_bytes = 0
        self.registry_head = self.start['seal_sha256']
        self.registry_seq = -1
        self.registered = {}
        self.incomplete = None
        self.expected_anchor = '%d:%s' % (seq, head)
        self._read_registration(self.start['seal_sha256'])
        self._verify_registered()
        self.verify_evidence()
        if self.start['capture_sha256'] != self.capture_sha256 or self.start['evidence_initial'] != self.initial_evidence:
            raise Refusal('Initial publication changed during invocation')
        self.remaining()

    def collect(self, mode, entry=None):
        self.verify_evidence()
        if mode not in self.p['allowed_modes']:
            raise Refusal('Unadmitted mode')
        acquisition_gate(self.m, mode, entry)
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
        self.remaining()  # Success is possible only after final summary fsync + directory fsync.
        self.verify_final()
        self._emit_anchor()
        return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode')
    parser.add_argument('--entry')
    parser.add_argument('--expected-anchor', required=True)
    parser.add_argument('--expected-capture-sha256', required=True)
    parser.add_argument('--bootstrap-bytes', required=True, type=int)
    parser.add_argument('--remaining-seconds', required=True, type=float)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    collector = Collector(VERIFIED_MEMBERS['capture'], args.mode, entry=args.entry,
        expected_anchor=args.expected_anchor, expected_capture_sha256=args.expected_capture_sha256,
        bootstrap_bytes=args.bootstrap_bytes, remaining_seconds=args.remaining_seconds)
    try:
        update = json.loads(VERIFIED_MEMBERS.get('request', b'{}')).get('evidence_update')
        if update is not None:
            if args.mode != 'inventory' or not isinstance(update, dict) or set(update) != {'slot', 'value'}:
                raise Refusal('Evidence update requires inventory plus exactly slot and value')
            collector.append_evidence(update['slot'], update['value'])
        result = collector.collect(args.mode, args.entry)
        print(json.dumps(result, sort_keys=True), flush=True)
        return 0
    except Exception as exc:
        collector.halt(exc)
    finally:
        collector.close()


def entrypoint(argv=None):
    try:
        return main(argv)
    except (Refusal, OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(entrypoint())
