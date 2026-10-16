"""C-ROOT and C-WORKTREE audit area: observe Git identity read-only, never invent evidence.

Loaded by icm21_check.area(), which injects the checker's Unverified class.
SPEC.md:494-538 and :611,:613. Known violations reduce to FAIL; anything the
audit cannot observe (commit, custody, held root/backup/rollback evidence)
raises Unverified so the report stays a truthful partial.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess


PRD_IDS = {'C-ROOT': 'ICM-R12', 'C-WORKTREE': 'ICM-R5'}
RETENTION_FIELDS = frozenset(('schema_version', 'leaves', 'routes', 'repairs',
                              'metadata', 'executor', 'containers'))


def run_git(root, *argv):
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith('GIT_')}
    return subprocess.run(['git', *argv], cwd=root, env=environment, capture_output=True)


def git(root, *argv):
    result = run_git(root, *argv)
    return result.returncode, result.stdout.decode('utf-8', 'replace').strip()


def tip_state(root, tip):
    """'commit', 'absent', 'not-commit' or None when the object store was not observed.

    git cat-file -e on an unpeeled id exits 1 with silent stderr only for an absent
    object; any other failure (permission, corruption) is missing evidence.
    """
    probe = run_git(root, 'cat-file', '-e', tip)
    if probe.returncode == 1 and not probe.stderr.strip():
        return 'absent'
    if probe.returncode:
        return None
    code, kind = git(root, 'cat-file', '-t', tip)
    if code or not kind:
        return None
    return 'commit' if kind == 'commit' else 'not-commit'


def root_identity(root, coverage):
    violations, missing = {}, []
    coverage['inspected'].append(str(root))
    code, top = git(root, 'rev-parse', '--show-toplevel')
    if code or not top:
        return violations, ['Canonical Git root identity is unavailable']
    if Path(top).resolve() != root.resolve():
        violations[str(root)] = 'Canonical root is not its own Git root: ' + top
    code, commit = git(root, 'rev-parse', '--verify', '--quiet', 'HEAD^{commit}')
    if code or not commit:
        missing.append('No commit evidence at HEAD')
    code, branch = git(root, 'symbolic-ref', '--quiet', '--short', 'HEAD')
    if code or not branch:
        missing.append('Branch identity is unavailable (detached or unreadable HEAD)')
    missing.append('Root readers, backup restoration and rollback evidence are held (H1)')
    return violations, missing


def worktree_custody(root, config, coverage):
    violations, missing = {}, []
    code, value = git(root, 'worktree', 'list', '--porcelain')
    if code:
        missing.append('Registered worktree identity is unavailable')
    else:
        for record in value.split('\n\n'):
            fields = record.splitlines()
            if not fields or not fields[0].startswith('worktree '):
                continue
            path = Path(fields[0][9:])
            if path == root:
                continue
            coverage['inspected'].append(str(path))
            if any(line.startswith('prunable') for line in fields):
                violations[str(path)] = 'Registered worktree residue: lane directory is absent'
            tip = next((line[5:] for line in fields if line.startswith('HEAD ')), None)
            state = 'absent' if tip is None else tip_state(root, tip)
            if state is None:
                missing.append('Worktree branch tip could not be read: ' + tip)
            elif state != 'commit':
                violations[str(path)] = 'Worktree branch tip is unreachable: ' + str(tip)
    binding = config['retention']
    try:
        raw = Path(binding['path']).read_bytes()
        coverage['inspected'].append(binding['path'])
    except OSError:
        missing.append('Retention custody manifest is unreadable')
    else:
        if hashlib.sha256(raw).hexdigest() != binding['sha256']:
            missing.append('Retention custody manifest digest mismatch')
        else:
            try:
                manifest = json.loads(raw.decode('utf-8'))
            except ValueError:
                manifest = None
            if type(manifest) is not dict or set(manifest) != RETENTION_FIELDS:
                missing.append('Retention custody manifest is incomplete (held contract)')
    missing.append('Leftover custody, preserved paths and retired-lane use are not '
                   'observed by audit; they need verified native custody evidence')
    return violations, missing


def check(check_id, root, mode, config, coverage):
    root = Path(root)
    if check_id == 'C-ROOT':
        violations, missing = root_identity(root, coverage)
    else:
        violations, missing = worktree_custody(root, config, coverage)
    findings = []
    for path, reason in sorted(violations.items()):
        identity = check_id + '\n' + path + '\n' + reason
        findings.append({'id': 'F-' + check_id[2:] + '-'
                               + hashlib.sha256(identity.encode()).hexdigest(),
                         'status': 'FAIL', 'prd_ids': [PRD_IDS[check_id]], 'paths': [path],
                         'evidence': [], 'reason': reason, 'previous_finding': None,
                         'resolution_receipt': None})
    if findings:
        return 'FAIL', '; '.join(f['reason'] for f in findings), findings
    raise Unverified('; '.join(missing))  # noqa: F821 -- injected by icm21_check.area()
