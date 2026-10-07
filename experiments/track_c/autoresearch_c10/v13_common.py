"""Standard-library boundary checks shared by the trusted v13 parent and audit."""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import time

ARMS = ('A1_single', 'A2_coherent2', 'A7_coined_coined')
SUMMARY = ('heldout_full', 'canon', 'first_token', 'A1', 'A2', 'L1_flips',
           'frame_flips', 'described_as', 'L3', 'ppl_post', 'law5_ok', 'scope_ok',
           'dw_total', 'edit_seconds', 'score_seconds', 'guards')
GUARD_NAMES = ('A1', 'A2', 'L1_flips', 'frame_flips', 'described_as', 'L3',
               'ppl_post', 'law5_ok', 'scope_ok')
GPU_JOBS = re.compile(r'edit\.py|editor_bootstrap\.py|scorer\.py|check_equivalence\.py|'
                      r'v13_verify_gpu\.py|c10s_sharedz_|c10e_bandknob|'
                      r'c10r_.*(?:location|exp2ctl)|location_control|run_iteration\.py|'
                      r'ollama serve|llama-server')


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read_json(path):
    def duplicate(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError('duplicate JSON key')
            d[k] = v
        return d
    return json.loads(Path(path).read_text(), object_pairs_hook=duplicate,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def write_json(path, value):
    path = Path(path)
    tmp = path.with_name(path.name + '.new')
    tmp.write_text(json.dumps(value, indent=1, allow_nan=False) + '\n')
    os.replace(tmp, path)


def verify(fence, expected):
    fence = Path(fence).resolve()
    manifest = fence / 'sealed/manifest.json'
    if digest(manifest) != expected:
        raise ValueError('manifest anchor mismatch')
    entries = read_json(manifest)
    for path, sha in entries.items():
        if digest(path) != sha:
            raise ValueError('trusted closure mismatch: ' + path)
    return read_json(fence / 'sealed/config.json')


def clean_env(config, tmp, run=None):
    env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': config['home'],
           'USER': config['user'], 'LANG': 'en_US.UTF-8', 'TMPDIR': str(tmp),
           'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONNOUSERSITE': '1',
           'HF_HOME': config['hf_home'], 'HF_HUB_OFFLINE': '1',
           'TRANSFORMERS_OFFLINE': '1', 'TOKENIZERS_PARALLELISM': 'false',
           'LLMDB_ROOT': config['program'], 'GRAFT_NO_REFRESH': '1',
           'GRAFT_NO_GITIGNORE': '1', 'GRAFT_NO_IGNORE': '1'}
    if run is not None:
        env['C10_RUN_DIR'] = str(run)
    env['XDG_CACHE_HOME'] = str(Path(tmp) / 'cache')
    env['TORCH_HOME'] = str(Path(tmp) / 'torch')
    if 'site_packages' in config:
        env['C10_SITE_PACKAGES'] = config['site_packages']
    return env


def projection(score):
    s = score['summary']
    if not isinstance(s, dict) or set(s) != set(SUMMARY):
        raise ValueError('invalid summary keys')
    for k in SUMMARY[:-1]:
        v = s[k]
        if k in ('law5_ok', 'scope_ok'):
            if type(v) is not bool:
                raise ValueError('invalid boolean summary')
        elif type(v) not in (int, float) or not math.isfinite(v) or v < 0:
            raise ValueError('invalid numeric summary')
    limits = {'heldout_full': 72, 'canon': 24, 'first_token': 72, 'A1': 72,
              'A2': 72, 'L1_flips': 12, 'frame_flips': 6, 'L3': 30}
    for k, top in limits.items():
        if type(s[k]) is not int or s[k] > top:
            raise ValueError('invalid count summary')
    if s['described_as'] > 100:
        raise ValueError('invalid locality summary')
    g = s['guards']
    if g != 'ok' and (not isinstance(g, str) or not g.startswith('failed:') or
                      not set(g[7:].split(',')) <= set(GUARD_NAMES)):
        raise ValueError('invalid guard summary')
    return {k: s[k] for k in SUMMARY}


def snapshot(source, destination):
    """Open without following links; copy the opened inode into a private new file."""
    fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size > 12 * 1024**3:
            raise ValueError('invalid handoff file')
        with os.fdopen(fd, 'rb', closefd=False) as src, open(destination, 'xb') as dst:
            for block in iter(lambda: src.read(1024 * 1024), b''):
                dst.write(block)
        after = os.fstat(fd)
        if (st.st_size, st.st_mtime_ns, st.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            raise ValueError('handoff changed during snapshot')
    finally:
        os.close(fd)


def validate_handoff(path):
    d = read_json(Path(path) / 'edits.json')
    if set(d) != {'commit', 'edit_seconds', 'setup_seconds', 'changed'} or d['commit'] != 'nocommit':
        raise ValueError('invalid edits envelope')
    if set(d['changed']) != set(ARMS) or set(d['edit_seconds']) != set(ARMS):
        raise ValueError('incomplete arms')
    for v in [d['setup_seconds'], *d['edit_seconds'].values()]:
        if type(v) not in (int, float) or not math.isfinite(v) or v < 0:
            raise ValueError('invalid timing')
    for names in d['changed'].values():
        if not isinstance(names, list) or len(names) != len(set(names)) or any(
                not isinstance(n, str) or not re.fullmatch(r'[A-Za-z0-9_.]+', n) for n in names):
            raise ValueError('invalid parameter names')
    return d


def identity(pid):
    p = subprocess.run(['/bin/ps', '-p', str(pid), '-o', 'lstart=', '-o', 'command='],
                       text=True, capture_output=True)
    if p.returncode != 0 or not p.stdout.strip():
        raise ValueError('process identity unavailable')
    return p.stdout.strip()


def stop_stage(record, config):
    """Only the recorded, unchanged process group may be signalled."""
    pid = record['pid']
    if identity(pid) != record['identity'] or os.getpgid(pid) != pid:
        raise ValueError('stage identity mismatch')
    allowed = {str(Path(config['sandbox']).resolve()), config['engine'], config['fence']}
    allowed.update(record.get('allowed_cwd', []))

    def checked_cwd(target):
        p = subprocess.run(['/usr/sbin/lsof', '-a', '-p', str(target), '-d', 'cwd', '-Fn'],
                           text=True, capture_output=True)
        if p.returncode != 0:
            raise ValueError('stage cwd unavailable')
        cwd = [line[1:] for line in p.stdout.splitlines() if line.startswith('n')]
        if len(cwd) != 1 or str(Path(cwd[0]).resolve()) not in allowed:
            raise ValueError('stage cwd mismatch')

    checked_cwd(pid)
    table = subprocess.run(['/bin/ps', '-axo', 'pid=,ppid='], text=True, capture_output=True, check=True)
    edges = {}
    for line in table.stdout.splitlines():
        fields = line.split()
        if len(fields) != 2 or not all(v.isdigit() for v in fields):
            raise ValueError('process tree malformed')
        child, parent = map(int, fields)
        edges.setdefault(parent, []).append(child)
    children = []

    def visit(parent):
        for child in edges.get(parent, []):
            if child == pid or child in children:
                raise ValueError('process tree cyclic')
            children.append(child)
            visit(child)

    visit(pid)
    pinned = {}
    for child in children:
        try:
            os.kill(child, 0)
        except ProcessLookupError:
            continue
        pinned[child] = identity(child)
        checked_cwd(child)
    # Detached process groups are still descendants. Verify each identity/cwd
    # immediately before signalling, and send TERM deepest first.
    for child in reversed(children):
        if child not in pinned:
            continue
        try:
            os.kill(child, 0)
        except ProcessLookupError:
            continue
        if identity(child) != pinned[child]:
            raise ValueError('descendant identity changed')
        checked_cwd(child)
        os.kill(child, signal.SIGTERM)
    os.killpg(pid, signal.SIGTERM)
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            break
        time.sleep(.05)
    for child, expected in reversed(list(pinned.items())):
        try:
            os.kill(child, 0)
        except ProcessLookupError:
            continue
        if identity(child) != expected:
            raise ValueError('descendant identity changed after TERM')
        checked_cwd(child)
        os.kill(child, signal.SIGKILL)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return
    if identity(pid) != record['identity']:
        raise ValueError('stage identity changed after TERM')
    checked_cwd(pid)
    os.killpg(pid, signal.SIGKILL)


def gpu_exclusive(ignore=()):
    p = subprocess.run(['/bin/ps', '-axo', 'pid=,command='], text=True, capture_output=True, check=True)
    blocked = []
    for line in p.stdout.splitlines():
        parts = line.strip().split(None, 1)
        if len(parts) == 2 and int(parts[0]) not in ignore and GPU_JOBS.search(parts[1]):
            blocked.append(int(parts[0]))
    if blocked:
        raise ValueError('exclusive GPU gate: conflicting pids ' + ','.join(map(str, blocked)))
