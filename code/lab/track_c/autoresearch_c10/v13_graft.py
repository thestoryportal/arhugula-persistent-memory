"""No-model graft exclusion, filesystem seals, and pre-launch sweep.

No graft command is executed: even queries can rewrite a repository's cache.
UF_IMMUTABLE blocks ordinary indexer writes, including atomic replacements.
It is not a boundary against a process that deliberately clears file flags.
"""
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v13_common import digest, verify

GRAFT_PROCESS = re.compile(r'(?:^|\s)(?:\S*/)?graft(?:\s|$)|'
                           r'/@nanonets/graft/dist/(?:cli|claude/(?:hooks|sync-run))\.js')


def freeze(path):
    """Seal a completed private area, or an already generated static file."""
    path = Path(path)
    paths = [*path.rglob('*'), path] if path.is_dir() else [path]
    for p in paths:
        if p.is_symlink():
            raise ValueError('cannot seal a symlink')
        p.chmod(0o555 if p.is_dir() or p.suffix == '.sh' else 0o444)
        os.chflags(p, p.stat().st_flags | stat.UF_IMMUTABLE)


def seal(config):
    if not hasattr(os, 'chflags') or not hasattr(stat, 'UF_IMMUTABLE'):
        raise ValueError('macOS immutable-file barrier unavailable')
    sandbox, fence = Path(config['sandbox']), Path(config['fence'])
    for name in config['graft_ignore_sha256']:
        freeze(sandbox / name)
    # Dynamic sealed state, stage temps and private run directories remain writable.
    for p in fence.rglob('*'):
        if p.is_file():
            freeze(p)
    for root in (sandbox, fence):
        root.chmod(0o555)
        os.chflags(root, root.stat().st_flags | stat.UF_IMMUTABLE)


def forbidden(path):
    return 'graft' in Path(path).parts or Path(path).name == 'ask-index.json'


def check_processes():
    table = subprocess.run(['/bin/ps', '-axo', 'pid=,command='], text=True,
                           capture_output=True, check=True).stdout
    if not table.strip():
        raise ValueError('graft process observation unavailable')
    for line in table.splitlines():
        fields = line.strip().split(None, 1)
        if len(fields) != 2 or not fields[0].isdigit():
            raise ValueError('graft process observation malformed')
        if GRAFT_PROCESS.search(fields[1]):
            raise ValueError('graft process active; protected launch refused')


def sweep(config, processes=False):
    sandbox, fence = Path(config['sandbox']), Path(config['fence'])
    for root in (sandbox, fence):
        st = root.lstat()
        if not stat.S_ISDIR(st.st_mode) or not st.st_flags & stat.UF_IMMUTABLE or st.st_mode & 0o222:
            raise ValueError('graft root barrier missing')
        for current, dirs, files in os.walk(root, followlinks=False):
            for name in dirs + files:
                p = Path(current) / name
                if forbidden(p.relative_to(root)):
                    raise ValueError('graft artifact present')
                if name == '.git' and p != sandbox / '.git':
                    raise ValueError('unexpected repository in a protected area')
    for name, expected in config['graft_ignore_sha256'].items():
        p = sandbox / name
        st = p.lstat()
        if not stat.S_ISREG(st.st_mode) or not st.st_flags & stat.UF_IMMUTABLE or st.st_mode & 0o222:
            raise ValueError('graft ignore barrier missing')
        if digest(p) != expected:
            raise ValueError('graft ignore file changed')
    if '/graft/' not in (sandbox / '.gitignore').read_text().splitlines():
        raise ValueError('graft exclusion missing')
    tracked = subprocess.run(['/usr/bin/git', '-C', str(sandbox), 'ls-files', '-z'],
                             capture_output=True, check=True).stdout.split(b'\0')
    history = subprocess.run(['/usr/bin/git', '-C', str(sandbox), 'log', '--all',
                              '--name-only', '-z', '--format='], capture_output=True, check=True).stdout.split(b'\0')
    if any(forbidden(os.fsdecode(p).strip('\n')) for p in tracked + history if p):
        raise ValueError('graft artifact tracked in repository or history')
    if processes:
        check_processes()
    return {'graft_artifacts': 0, 'tracked_graft_cache': 0, 'history_graft_cache': 0,
            'immutable_roots': 2, 'immutable_ignore_files': len(config['graft_ignore_sha256']),
            'active_process_check': processes}


def barrier_probe(config):
    sweep(config)
    directories, ignores = 0, 0
    for root in (Path(config['sandbox']), Path(config['fence'])):
        target = root / 'graft'
        try:
            target.mkdir()
        except PermissionError:
            directories += 1
        else:
            target.rmdir()
            raise ValueError('graft directory creation was allowed')
    for name in config['graft_ignore_sha256']:
        try:
            fd = os.open(Path(config['sandbox']) / name, os.O_WRONLY | os.O_APPEND)
        except PermissionError:
            ignores += 1
        else:
            os.close(fd)
            raise ValueError('graft ignore mutation was allowed')
    # No bytes change; opening the existing recipe proves the root seal permits editing.
    fd = os.open(Path(config['sandbox']) / 'edit.py', os.O_WRONLY)
    os.close(fd)
    return {'graft_directory_creation_denied': directories, 'ignore_write_denied': ignores,
            'existing_recipe_open_for_write': True}


def writable_probe(config):
    """Exercise mutable children below sealed roots without changing any static file."""
    import tempfile
    from v13_common import write_json, read_json
    areas = [Path(config['sandbox']) / 'runs', Path(config['fence']) / 'sealed',
             Path(config['scorer_results']), Path(config['editor_tmp']),
             Path(config['scorer_tmp']), Path(config['capture'])]
    for area in areas:
        with tempfile.TemporaryDirectory(prefix='legitimate_', dir=area) as child:
            p = Path(child) / 'status.json'
            write_json(p, {'value': 1})
            write_json(p, {'value': 2})
            if read_json(p) != {'value': 2}:
                raise ValueError('legitimate sealed-root child write failed')
    for name in ('edit.py', 'results.tsv'):
        fd = os.open(Path(config['sandbox']) / name, os.O_WRONLY)
        os.close(fd)
    return {'mutable_areas': len(areas), 'create_read_replace_cleanup': True,
            'existing_recipe_and_results_open_for_write': True}


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3) or len(sys.argv) == 3 and sys.argv[2] not in ('--processes', '--probe-barriers', '--probe-writes'):
        raise SystemExit('usage: v13_graft.py FENCE [--processes|--probe-barriers|--probe-writes]')
    fence = Path(sys.argv[1])
    config = verify(fence, digest(fence / 'sealed/manifest.json'))
    if len(sys.argv) == 3 and sys.argv[2] == '--probe-barriers':
        result = barrier_probe(config)
    elif len(sys.argv) == 3 and sys.argv[2] == '--probe-writes':
        result = writable_probe(config)
    else:
        result = sweep(config, len(sys.argv) == 3)
    print(json.dumps(result, sort_keys=True))
