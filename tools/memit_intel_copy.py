#!/Library/Developer/CommandLineTools/usr/bin/python3
"""M3 controller: manifest dry run or M3-initiated, SHA-256 verified cable copy.

Run with CLT Python 3.9. Children are native tools at taskpolicy background
priority. Only check_gpu controls science pausing; no descendant inventory.
"""
import sys
sys.dont_write_bytecode = True

import argparse
import fnmatch
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import signal
import stat
import subprocess
import time
import traceback

REPO = Path(__file__).resolve().parents[1]
SRC = Path('/Volumes/memit/llm-database-poc-mirror')
DEFAULT_REMOTE = ['ssh', '-i', os.path.expanduser('~/.ssh/intel_mac_ed25519'), '-o', 'IdentitiesOnly=yes', '-o', 'BatchMode=yes', 'robertrhu_node2@192.168.10.2']
CAP = 250_000_000_000
FREE_FLOOR = 80_000_000_000 + 20 * 1024**3
RECORD_CAP = 50_000_000
POLICY = ['/usr/sbin/taskpolicy', '-b', '-d', 'throttle']


def check_gpu():
    spec = importlib.util.spec_from_file_location('intel_copy_gate', REPO / 'tools/c10w_p2_gate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_gpu()


class NativeRunner:
    def __init__(self, gate=check_gpu, policy=None, poll=5, stop_timeout=5, log=None):
        self.gate = gate
        self.policy = POLICY if policy is None else policy
        self.poll = poll
        self.stop_timeout = stop_timeout
        self.log = log if log is not None else lambda event: print(json.dumps(event), file=sys.stderr, flush=True)
        self.paused = False

    def clear(self):
        try:
            result = self.gate()
            self.last_check = result
            return isinstance(result, dict) and result.get('ok') is True
        except Exception:
            self.last_check = {'ok': False, 'traceback': traceback.format_exc()}
            return False

    def pause(self):
        if not self.paused:
            self.paused = True
            self.log({'event': 'PAUSED', 'check': self.last_check})

    def wait_clear(self):
        clear_polls = 0
        while True:
            if self.clear():
                if not self.paused:
                    return
                clear_polls += 1
                if clear_polls == 2:
                    self.paused = False
                    self.log({'event': 'RESUMED', 'clear_polls': clear_polls})
                    return
            else:
                self.pause()
                clear_polls = 0
            time.sleep(self.poll)

    def stop(self, process):
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        try:
            process.communicate(timeout=self.stop_timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()

    def run(self, command, stdin=None):
        while True:
            self.wait_clear()
            process = subprocess.Popen(self.policy + list(command), stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
            interrupted = False
            supplied = False
            try:
                while True:
                    try:
                        out, err = process.communicate(input=stdin if not supplied else None, timeout=self.poll)
                        break
                    except subprocess.TimeoutExpired:
                        supplied = True
                        if not self.clear():
                            self.pause()
                            self.stop(process)
                            interrupted = True
                            break
            except BaseException:
                self.stop(process)
                raise
            if interrupted:
                continue
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command, output=out, stderr=err)
            return out


def safe_path(path):
    if not path or '\x00' in path or PurePosixPath(path).is_absolute() or any(p in ('', '.', '..') for p in path.split('/')):
        raise ValueError('unsafe source path: %r' % path)
    return path


def fingerprint(s):
    return [s.st_size, s.st_mtime_ns, s.st_ino]


def budget(recovery_bytes, free_bytes, projected_bytes):
    for value in (recovery_bytes, free_bytes, projected_bytes):
        if type(value) is not int or value < 0:
            raise ValueError('invalid budget measurement')
    result = {'recovery_bytes': recovery_bytes, 'free_bytes': free_bytes, 'projected_bytes': projected_bytes,
              'cap_bytes': CAP, 'free_floor_bytes': FREE_FLOOR,
              'projected_recovery_bytes': recovery_bytes + projected_bytes,
              'projected_free_bytes': free_bytes - projected_bytes}
    result['cap_deficit'] = max(0, result['projected_recovery_bytes'] - CAP)
    result['free_deficit'] = max(0, FREE_FLOOR - result['projected_free_bytes'])
    result['ok'] = result['cap_deficit'] == 0 and result['free_deficit'] == 0
    return result


def read_manifest(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return [json.loads(line) for line in f]


def credential_name(path):
    name = PurePosixPath(path).name.lower()
    return (name == '.hf_token' or name == '.env' or name.startswith('.env.') or
            name.startswith(('id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519')) or
            name.endswith(('.pem', '.p12', '.pfx', '.key')) or
            re.search(r'(^|[._-])(credentials?|passwords?|secrets?|tokens?)([._-]|$)', name) is not None)


def excluded(path, kind, patterns):
    parts = path.split('/')
    if '.intel_copy_state' in parts or '.hf_token' in parts:
        return True
    if parts[-1].startswith('tmp_obj_') and any(parts[i:i+2] == ['.git', 'objects'] for i in range(len(parts)-1)):
        return True
    for pattern in patterns:
        directory = pattern.endswith('/')
        clean = pattern.strip('/')
        candidates = ['/'.join(parts[:i]) for i in range(1, len(parts) + (kind == 'dir'))] if directory else [path]
        if '/' in clean or pattern.startswith('/'):
            if any(fnmatch.fnmatchcase(candidate, clean) for candidate in candidates):
                return True
        elif any(fnmatch.fnmatchcase(part, clean) for part in (parts[:-1] if directory and kind != 'dir' else parts)):
            return True
    return False


class Controller:
    def __init__(self, source, records, gen, remote=None, runner=None):
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}', gen):
            raise ValueError('invalid generation')
        self.source = Path(source).absolute()
        self.directory = Path(records).absolute() / gen
        self.gen = gen
        self.remote = DEFAULT_REMOTE if remote is None else list(remote)
        if len(self.remote) < 2:
            raise ValueError('--remote must contain an executable prefix and destination')
        self.phase = 'initialization'
        self.measured = {}
        self.directory.mkdir(parents=True, exist_ok=True)
        self.state = self.source / '.intel_copy_state'
        if self.source.is_symlink() or self.state.is_symlink() or self.directory.is_symlink():
            raise ValueError('source/state/records cannot be symlinks')
        self.state.mkdir(exist_ok=True)
        self.manifest_path = self.directory / 'manifest.jsonl.gz'
        self.receipt_path = self.directory / 'receipt.json'
        self.log_path = self.directory / 'run.jsonl'
        self.runner = runner if runner is not None else NativeRunner(log=self.log)
        self.patterns = [p.strip() for p in (REPO / 'tools/backup_mirror.excludes').read_text().splitlines() if p.strip() and not p.startswith('#')]
        self.manifest_info = None

    def record(self, path, value):
        data = (json.dumps(value, sort_keys=True) + '\n').encode()
        self.check_records(len(data), replacing=path)
        with open(path, 'wb') as f:
            f.write(data); f.flush(); os.fsync(f.fileno())

    def check_records(self, new_bytes=0, replacing=None):
        used = sum(p.stat().st_size for p in self.directory.iterdir() if p.is_file())
        if replacing is not None and replacing.exists():
            used -= replacing.stat().st_size
        if used + new_bytes > RECORD_CAP:
            self.measured['record_budget'] = {'used_bytes': used, 'projected_bytes': used + new_bytes, 'cap_bytes': RECORD_CAP}
            raise ValueError('record budget exceeds 50 MB: %d' % (used + new_bytes))

    def log(self, event):
        event = dict(event, time_ns=time.time_ns(), phase=self.phase)
        data = (json.dumps(event, sort_keys=True) + '\n').encode()
        # Leave 64 KiB for a final halt receipt.
        self.check_records(len(data) + 65536)
        with open(self.log_path, 'ab') as f:
            f.write(data); f.flush()

    def source_path(self, path):
        safe_path(path)
        current = self.source
        for part in path.split('/')[:-1]:
            current = current / part
            if current.is_symlink():
                raise ValueError('source parent is a symlink: %s' % path)
        return self.source / path

    def native_stat(self, path):
        out = self.runner.run(['/usr/bin/stat', '-f', '%z %m %i', str(path)])
        fields = out.decode().split()
        if len(fields) != 3 or not all(re.fullmatch(r'-?\d+', x) for x in fields):
            raise ValueError('malformed native stat output')
        s = path.lstat()
        if [int(x) for x in fields] != [s.st_size, s.st_mtime_ns // 10**9, s.st_ino]:
            raise ValueError('source changed during stat: %s' % path)
        return s

    def population(self, paths_from):
        if paths_from is not None:
            for path in Path(paths_from).read_text().splitlines():
                if path:
                    yield safe_path(path)
            return
        # Prune excluded directories before descent: neither caches nor state
        # need a scan. find is physical by default and never follows symlinks.
        names = sorted({p.strip('/') for p in self.patterns if p.endswith('/') and '/' not in p.strip('/')})
        command = ['/usr/bin/find', str(self.source), '(']
        for index, name in enumerate(names + ['.intel_copy_state']):
            if index:
                command += ['-o']
            command += ['-name', name]
        for p in self.patterns:
            if p.endswith('/') and '/' in p.strip('/'):
                command += ['-o', '-path', str(self.source / p.strip('/'))]
        command += [')', '-type', 'd', '-prune', '-o', '(', '-type', 'f', '-o', '-type', 'l', ')', '-print0']
        output = self.runner.run(command)
        if output and not output.endswith(b'\x00'):
            raise ValueError('truncated find output')
        for path in sorted(os.fsdecode(p) for p in output.split(b'\x00') if p):
            yield safe_path(str(Path(path).relative_to(self.source)))

    def manifest(self, paths_from=None, started_ns=None):
        try:
            return self.build_manifest(paths_from, started_ns)
        except BaseException as exc:
            self.halt(exc)
            raise

    def halt(self, exc):
        result = {'gen': self.gen, 'status': 'HALTED', 'phase': self.phase, 'error': str(exc),
                  'traceback': traceback.format_exc(), **self.measured}
        if isinstance(exc, subprocess.CalledProcessError):
            result['child_stdout'] = os.fsdecode(exc.output or b'')
            result['child_stderr'] = os.fsdecode(exc.stderr or b'')
            result['child_rc'] = exc.returncode
        self.record(self.receipt_path, result)

    def build_manifest(self, paths_from=None, started_ns=None):
        self.phase = 'manifest'
        started = time.time_ns() if started_ns is None else started_ns
        cache = {}
        cache_path = self.state / 'hashes.jsonl'
        if cache_path.exists():
            for line in cache_path.read_text().splitlines():
                row = json.loads(line)
                cache[row['key']] = row['sha256']
        entries = []
        credentials = []
        recent = []
        changed = []
        for path in self.population(paths_from):
            if credential_name(path):
                credentials.append(path)
                continue
            if excluded(path, 'file', self.patterns):
                continue
            absolute = self.source_path(path)
            s = self.native_stat(absolute)
            if started - s.st_mtime_ns < 600 * 10**9:
                recent.append(path)
                continue
            row = {'path': path, 'size': s.st_size, 'mtime_ns': s.st_mtime_ns, 'inode': s.st_ino}
            if stat.S_ISLNK(s.st_mode):
                row.update(kind='symlink', target=os.readlink(absolute))
            elif stat.S_ISREG(s.st_mode):
                key = json.dumps([str(self.source), path] + fingerprint(s))
                digest = cache.get(key)
                if digest is None:
                    output = self.runner.run(['/sbin/sha256sum', str(absolute)])
                    # sha256sum escapes filenames containing newlines/backslashes.
                    found = re.match(rb'\\?([0-9a-f]{64})[ *]', output)
                    if found is None:
                        raise ValueError('malformed SHA-256 output: %r' % output)
                    digest = found.group(1).decode()
                    if fingerprint(absolute.lstat()) != fingerprint(s):
                        changed.append(path)
                        continue
                    with open(cache_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({'key': key, 'sha256': digest}) + '\n')
                        f.flush(); os.fsync(f.fileno())
                    cache[key] = digest
                row.update(kind='file', sha256=digest)
            else:
                raise ValueError('selected source is not file/link: %s' % path)
            entries.append(row)
        if len({r['path'] for r in entries}) != len(entries):
            raise ValueError('duplicate paths in population')
        raw = ''.join(json.dumps(r, sort_keys=True) + '\n' for r in entries).encode()
        compressed = gzip.compress(raw, mtime=0)
        self.check_records(len(compressed) + 65536, replacing=self.manifest_path)
        if self.manifest_path.exists() and self.manifest_path.read_bytes() != compressed:
            raise ValueError('generation manifest is immutable; choose a new --gen')
        if not self.manifest_path.exists():
            pending = self.state / (self.gen + '.manifest.pending')
            with open(pending, 'wb') as f:
                f.write(compressed); f.flush(); os.fsync(f.fileno())
            pending.rename(self.manifest_path)
        distinct = {r['sha256']: r['size'] for r in entries if r['kind'] == 'file'}
        self.manifest_info = {'gen': self.gen, 'started_ns': started, 'entries': entries,
                              'files': sum(r['kind'] == 'file' for r in entries), 'paths': len(entries),
                              'bytes': sum(r['size'] for r in entries if r['kind'] == 'file'),
                              'distinct_bytes': sum(distinct.values()), 'distinct_objects': len(distinct),
                              'manifest_sha256': hashlib.sha256(compressed).hexdigest(), 'manifest_raw_bytes': len(raw),
                              'credentials': sorted(credentials), 'recent_paths': sorted(recent), 'changed_during_hash': sorted(changed)}
        self.record(self.directory / 'manifest_summary.json', {k: v for k, v in self.manifest_info.items() if k != 'entries'})
        self.log({'event': 'MANIFEST', 'paths': len(entries), 'distinct_bytes': sum(distinct.values())})
        return self.manifest_info

    def load_manifest(self):
        info = json.loads((self.directory / 'manifest_summary.json').read_text())
        if hashlib.sha256(self.manifest_path.read_bytes()).hexdigest() != info['manifest_sha256']:
            raise ValueError('saved manifest digest differs')
        info['entries'] = read_manifest(self.manifest_path)
        self.manifest_info = info

    def remote_script(self, mode, *args):
        command = '/usr/bin/python3 -I -B - ' + shlex.join([mode] + list(args))
        out = self.runner.run(self.remote + [command], stdin=(REPO / 'tools/memit_intel_receive.py').read_bytes())
        if not out.strip():
            raise ValueError('empty Intel response')
        result = json.loads(out)
        if not isinstance(result, dict):
            raise ValueError('Intel response is not an object')
        return result

    def remote_inventory(self):
        return self.remote_script('inventory')

    def changed_paths(self):
        changed = []
        for row in self.manifest_info['entries']:
            try:
                path = self.source_path(row['path'])
                s = path.lstat()
                valid = fingerprint(s) == [row['size'], row['mtime_ns'], row['inode']]
                valid = valid and ((row['kind'] == 'file' and stat.S_ISREG(s.st_mode)) or
                                  (row['kind'] == 'symlink' and stat.S_ISLNK(s.st_mode) and os.readlink(path) == row['target']))
                if not valid:
                    changed.append(row['path'])
            except (FileNotFoundError, ValueError):
                changed.append(row['path'])
        return changed

    def rsync(self, sources, destination, files_from=None):
        command = ['/opt/homebrew/bin/rsync', '-r', '-t', '--protocol=29', '--rsync-path=/usr/bin/rsync', '--partial-dir=.partials',
                   '-e', shlex.join(self.remote[:-1])]
        if files_from is not None:
            command += ['--from0', '--files-from=' + str(files_from)]
        command += ['--'] + [str(s) for s in sources] + [self.remote[-1] + ':' + destination]
        self.runner.run(command)

    def prepare_transfer(self):
        """Check budgets and push generation metadata before any object payload."""
        if self.manifest_info is None:
            self.load_manifest()
        self.phase = 'inventory'
        inventory = self.remote_inventory()
        required = ('digests', 'recovery_bytes', 'free_bytes')
        if any(k not in inventory for k in required) or not isinstance(inventory['digests'], list):
            raise ValueError('malformed Intel inventory')
        held = set(inventory['digests'])
        if any(not isinstance(d, str) or not re.fullmatch(r'[0-9a-f]{64}', d) for d in held):
            raise ValueError('invalid held digest')
        changed = self.changed_paths()
        representatives = {}
        sizes = {}
        for row in self.manifest_info['entries']:
            if row['kind'] == 'file' and row['path'] not in changed and row['sha256'] not in held:
                representatives.setdefault(row['sha256'], row['path'])
                sizes[row['sha256']] = row['size']
        self.control = {'manifest_sha256': self.manifest_info['manifest_sha256'], 'changed_paths': changed,
                        'representatives': representatives, 'changed_during_hash': self.manifest_info['changed_during_hash']}
        self.control_path = self.state / (self.gen + '.control.json')
        self.record(self.directory / 'inventory.json', inventory)
        # Conservatively reserve directory/link metadata and the largest extra
        # rsync temporary file, in addition to one copy of each missing object.
        projected = (sum(sizes.values()) + max(sizes.values(), default=0) +
                     self.manifest_path.stat().st_size + self.manifest_info['manifest_raw_bytes'] +
                     len(json.dumps(self.control).encode()) + 65536 * (len(self.manifest_info['entries']) + 16))
        self.phase = 'budget'
        self.measured['budget'] = budget(inventory['recovery_bytes'], inventory['free_bytes'], projected)
        self.record(self.directory / 'budget.json', self.measured['budget'])
        if not self.measured['budget']['ok']:
            raise ValueError('Intel budget refusal: %s' % json.dumps(self.measured['budget']))
        self.phase = 'metadata'
        folder = 'memit_copy/incoming/' + self.gen
        self.runner.run(self.remote + ['mkdir -p "$HOME/' + folder + '/data"'])
        self.write_control()
        self.rsync([self.manifest_path, self.control_path], folder + '/')
        self.sent_objects = len(representatives)
        return representatives

    def write_control(self):
        # rsync keeps basename: the receiver always reads control.json.
        canonical = self.state / self.gen / 'control.json'
        canonical.parent.mkdir(exist_ok=True)
        with open(canonical, 'w', encoding='utf-8') as f:
            json.dump(self.control, f, sort_keys=True)
            f.write('\n'); f.flush(); os.fsync(f.fileno())
        self.control_path = canonical

    def run(self, paths_from=None, started_ns=None):
        try:
            if self.manifest_path.exists():
                self.load_manifest()
            else:
                self.manifest(paths_from, started_ns)
            representatives = self.prepare_transfer()
            self.phase = 'transfer'
            filelist = self.state / self.gen / 'paths.from0'
            filelist.write_bytes(b''.join(os.fsencode(path) + b'\x00' for path in representatives.values()))
            if representatives:
                self.rsync([str(self.source) + '/'], 'memit_copy/incoming/' + self.gen + '/data/', filelist)
            self.phase = 'source_recheck'
            self.control['changed_paths'] = self.changed_paths()
            self.write_control()
            self.rsync([self.control_path], 'memit_copy/incoming/' + self.gen + '/')
            self.phase = 'verify'
            try:
                receipt = self.remote_script('verify', self.gen, self.manifest_info['manifest_sha256'])
            except subprocess.CalledProcessError as exc:
                # A mismatch explained by a source mutation is INCOMPLETE.
                # Other failures halt immediately; no network retry loop.
                if exc.returncode != 3 or not exc.output:
                    raise
                diagnostic = json.loads(exc.output)
                if not diagnostic.get('error', '').startswith('object SHA-256 mismatch:'):
                    raise
                changed = self.changed_paths()
                if changed == self.control['changed_paths']:
                    raise
                self.control['changed_paths'] = changed
                self.write_control()
                self.rsync([self.control_path], 'memit_copy/incoming/' + self.gen + '/')
                receipt = self.remote_script('verify', self.gen, self.manifest_info['manifest_sha256'])
            # Verification can be slow on Intel: re-stat after its reply too.
            # A single reconciliation records late source changes on Intel;
            # this is not a connectivity retry or a source-stability loop.
            final_changed = self.changed_paths()
            if final_changed != self.control['changed_paths']:
                self.control['changed_paths'] = final_changed
                self.write_control()
                self.rsync([self.control_path], 'memit_copy/incoming/' + self.gen + '/')
                receipt = self.remote_script('verify', self.gen, self.manifest_info['manifest_sha256'])
                if self.changed_paths() != final_changed:
                    raise ValueError('source changed again during final reconciliation')
            if (receipt.get('gen') != self.gen or receipt.get('manifest_sha256') != self.manifest_info['manifest_sha256'] or
                    receipt.get('status') not in ('COMPLETE', 'INCOMPLETE') or
                    receipt.get('manifest_paths') != len(self.manifest_info['entries']) or
                    (receipt['status'] == 'COMPLETE' and receipt.get('paths') != len(self.manifest_info['entries']))):
                raise ValueError('invalid Intel verification receipt')
            receipt['sent_objects'] = self.sent_objects
            receipt['changed_during_hash'] = self.manifest_info['changed_during_hash']
            if receipt['changed_during_hash']:
                receipt['status'] = 'INCOMPLETE'
            self.phase = 'receipt'
            self.record(self.receipt_path, receipt)
            self.log({'event': receipt['status'], 'paths': receipt['paths']})
            return receipt
        except BaseException as exc:
            self.halt(exc)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('subcommand', choices=['manifest', 'run'])
    parser.add_argument('--source', type=Path, default=SRC)
    parser.add_argument('--gen', default=time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()))
    parser.add_argument('--paths-from', type=Path)
    parser.add_argument('--remote', default=shlex.join(DEFAULT_REMOTE), help='quoted remote argv prefix, including destination')
    args = parser.parse_args()
    controller = Controller(args.source, REPO / 'results/intel_memit_copy', args.gen, shlex.split(args.remote))
    try:
        if args.subcommand == 'run':
            result = controller.run(args.paths_from)
        else:
            result = controller.manifest(args.paths_from)
            result = {k: v for k, v in result.items() if k != 'entries'}
        print(json.dumps(result, sort_keys=True))
        return 0 if result.get('status', 'COMPLETE') == 'COMPLETE' else 3
    except Exception as exc:
        if args.subcommand == 'manifest':
            controller.record(controller.receipt_path, {'gen': args.gen, 'status': 'HALTED', 'phase': controller.phase,
                                                       'error': str(exc), 'traceback': traceback.format_exc()})
        print(json.dumps({'status': 'HALTED', 'error': str(exc)}), file=sys.stderr)
        return 3


if __name__ == '__main__':
    sys.exit(main())
