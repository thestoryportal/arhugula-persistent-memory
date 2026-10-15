"""Workspace admission, rechecked creation and synchronous before-tool decisions."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import resource
import selectors
import signal
import shlex
import stat
import subprocess
import sys
import time
from typing import Literal, Mapping


WorkspaceRequest = Mapping[str, object]
HookEvent = Mapping[str, object]
Admit = dict
Deny = dict


class AdmissionError(ValueError):
    def __init__(self, code, reason):
        super().__init__(reason)
        self.code = code


def require(condition, reason, code='INVALID_INPUT'):
    if not condition:
        raise AdmissionError(code, reason)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def object_fields(value, fields):
    require(type(value) is dict and set(value) == set(fields), 'Invalid object fields')


def string(value):
    require(type(value) is str and bool(value) and '\x00' not in value,
            'Invalid string')


def path(value):
    string(value)
    require(value.startswith('/') and all(p not in ('', '.', '..')
            for p in value.split('/')[1:]) and not any(c in value for c in '\r\n'),
            'Path must be absolute and normalized')


def strings(value, validator=string, unique=False):
    require(type(value) is list, 'Expected array')
    for item in value:
        validator(item)
    if unique:
        require(len(value) == len(set(value)), 'Duplicate array item')


def binding(value):
    object_fields(value, ('path', 'sha256'))
    path(value['path'])
    require(type(value['sha256']) is str and re.fullmatch('[0-9a-f]{64}', value['sha256']),
            'Invalid digest')


def version(value):
    require(type(value['schema_version']) is int and value['schema_version'] == 1,
            'Invalid schema version')


def validate_request(value):
    object_fields(value, ('schema_version', 'id', 'kind', 'source', 'destination',
                          'lane', 'base_commit', 'plan'))
    version(value)
    for key in ('id', 'lane', 'base_commit'):
        string(value[key])
    require(value['kind'] in ('clone', 'repo-copy', 'worktree'), 'Invalid request kind')
    path(value['source'])
    path(value['destination'])
    if value['plan'] is not None:
        binding(value['plan'])


def below(target, root):
    return target == root or target.startswith(root + '/')


def no_links(value):
    """Capture ancestors without resolving away an ambiguous symlink."""
    result = {}
    target = Path(value)
    for ancestor in reversed((target, *target.parents)):
        try:
            info = ancestor.lstat()
        except FileNotFoundError:
            break
        require(not stat.S_ISLNK(info.st_mode), 'Ambiguous ancestor link', 'LINK_AMBIGUITY')
        require(ancestor == target or stat.S_ISDIR(info.st_mode),
                'Non-directory ancestor', 'LINK_AMBIGUITY')
        result[str(ancestor)] = (info.st_dev, info.st_ino, info.st_mode)
    return result


def read_file(value):
    no_links(value)
    fd = os.open(value, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), 'Expected regular file')
        return stream.read()


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result


def invalid_constant(value):
    raise AdmissionError('INVALID_INPUT', 'Invalid JSON constant')


def decode(raw):
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=invalid_constant)


def read_binding(value, json_value=True):
    binding(value)
    raw = read_file(value['path'])
    require(hashlib.sha256(raw).hexdigest() == value['sha256'],
            'Changed policy binding', 'CHANGED_POLICY')
    return decode(raw) if json_value else raw


@dataclass(frozen=True)
class WorkspacePolicy:
    wire: dict
    config: dict
    scopes: tuple
    requests: tuple
    identities: dict
    policy_path: str | None
    schema: dict
    validator: object
    policy_file_sha256: str | None

    def validate(self, name, value):
        self.validator(value, {'$ref': '#/$defs/' + name}, self.schema['$defs'])


def wire_validator():
    """Consume T061's parser and the active package's hash-checked schema."""
    package = Path(os.environ['ICM_PACKAGE'])
    context = decode(read_file(str(package / 'context.json')))
    schema_binding = dict(context['sources']['WIRE-SCHEMAS.json'])
    schema_binding['path'] = schema_binding['path'].replace('{package}', str(package))
    schema = read_binding(schema_binding)
    source = Path(__file__).parents[2] / 'state/icm21_check.py'
    spec = importlib.util.spec_from_file_location('icm21_wire', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return schema, module.validate_schema


def load_policy(wire, policy_path=None):
    policy_file_sha256 = None
    if policy_path is not None:
        raw = read_file(policy_path)
        require(decode(raw) == wire, 'Changed policy bytes', 'CHANGED_POLICY')
        policy_file_sha256 = hashlib.sha256(raw).hexdigest()
    schema, validator = wire_validator()

    def validate(name, value):
        validator(value, {'$ref': '#/$defs/' + name}, schema['$defs'])

    validate('WorkspacePolicy', wire)
    object_fields(wire, ('schema_version', 'config', 'gate', 'scopes', 'approved_requests',
                         'capabilities', 'read_tools', 'disabled_tool_names'))
    version(wire)
    for key in ('read_tools', 'disabled_tool_names'):
        strings(wire[key])
    require(set(wire['read_tools']) <= {'Read', 'Glob', 'Grep'}, 'Unknown read tool')
    require(type(wire['capabilities']) is list, 'Invalid capabilities')
    config = read_binding(wire['config'])
    validate('Config', config)
    object_fields(config, ('schema_version', 'canonical_root', 'source_roots',
                          'preservation_root', 'worktree_root', 'tool_root', 'ownership_path',
                          'registries', 'references', 'retention', 'required_checks',
                          'nightly_utc', 'migration_holds'))
    version(config)
    roots = [config[key] for key in ('canonical_root', 'preservation_root',
                                    'worktree_root', 'tool_root')]
    strings(config['source_roots'], path, unique=True)
    require(bool(config['source_roots']), 'Missing source roots')
    roots += config['source_roots']
    for i, root in enumerate(roots):
        path(root)
        require(all(not below(root, other) and not below(other, root)
                    for other in roots[:i]), 'Nested policy roots')
    for key in ('ownership_path', 'registries', 'references', 'retention'):
        binding(config[key])
    strings(config['required_checks'], unique=True)
    require(bool(config['required_checks']) and config['nightly_utc'] == '02:00:00Z',
            'Invalid check configuration')
    require(type(config['migration_holds']) is list, 'Invalid holds')
    scopes = read_binding(wire['scopes'])
    validate('LaneScopes', scopes)
    object_fields(scopes, ('schema_version', 'lanes'))
    version(scopes)
    require(wire['scopes'] == config['ownership_path'], 'Ownership binding mismatch')
    require(type(scopes['lanes']) is list, 'Invalid lane scopes')
    files, lanes = set(), set()
    for scope in scopes['lanes']:
        object_fields(scope, ('lane', 'root', 'file_paths'))
        string(scope['lane'])
        path(scope['root'])
        strings(scope['file_paths'], path, unique=True)
        require(scope['lane'] not in lanes and scope['root'] ==
                config['worktree_root'] + '/' + scope['lane'], 'Invalid lane root')
        require(not files.intersection(scope['file_paths']), 'Overlapping file ownership')
        files.update(scope['file_paths'])
        lanes.add(scope['lane'])
    requests = read_binding(wire['approved_requests'])
    validate('ApprovedRequests', requests)
    object_fields(requests, ('schema_version', 'requests'))
    version(requests)
    require(type(requests['requests']) is list, 'Invalid requests')
    ids = set()
    for request in requests['requests']:
        validate_request(request)
        require(request['id'] not in ids and request['lane'] in lanes,
                'Duplicate request or unknown lane')
        ids.add(request['id'])
        require(request['destination'] == config['worktree_root'] + '/' + request['lane'],
                'Approved destination differs from lane root')
    read_binding(wire['gate'], json_value=False)
    identities = {}
    observed = roots + list(files) + [s['root'] for s in scopes['lanes']]
    observed += [r[k] for r in requests['requests'] for k in ('source', 'destination')]
    protected = [wire[k]['path'] for k in ('config', 'gate', 'scopes', 'approved_requests')]
    protected += [config[k]['path'] for k in ('registries', 'references', 'retention')]
    protected += [cap['profile']['path'] for cap in wire['capabilities']]
    if policy_path is not None:
        protected.append(policy_path)
    require(not files.intersection(protected), 'Guard or policy is in native edit scope')
    capability_ids, fixtures, outputs = set(), set(), set()
    for cap in wire['capabilities']:
        object_fields(cap, ('id', 'lane', 'argv', 'interpreter', 'cwd', 'profile',
                           'output_paths', 'fixture_root', 'executable_paths', 'read_paths',
                           'timeout_seconds', 'max_output_bytes'))
        for key in ('id', 'lane'):
            string(cap[key])
        require(cap['id'] not in capability_ids and cap['lane'] in lanes,
                'Duplicate capability or unknown lane')
        capability_ids.add(cap['id'])
        for key in ('interpreter', 'cwd'):
            path(cap[key])
        for key in ('output_paths', 'executable_paths', 'read_paths'):
            strings(cap[key], path, unique=True)
        strings(cap['argv'])
        require(len(cap['argv']) == 5 and cap['argv'][:4] ==
                [cap['interpreter'], '-B', '-m', 'unittest'] and
                re.fullmatch(r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*', cap['argv'][4]),
                'Worker argv is not the fixed unittest call')
        require(cap['interpreter'] in cap['executable_paths'] and
                '/usr/bin/sandbox-exec' in cap['executable_paths'], 'Missing executable coverage')
        for key in ('timeout_seconds', 'max_output_bytes'):
            require(type(cap[key]) is int and cap[key] > 0, 'Invalid resource bound')
        require(len(cap['output_paths']) == 2 and not outputs.intersection(cap['output_paths']),
                'Invalid output scope')
        outputs.update(cap['output_paths'])
        for output in cap['output_paths']:
            read_file(output)
            require(not any(below(output, root) for root in
                            [config['canonical_root']] + [s['root'] for s in scopes['lanes']]),
                    'Output is inside a protected repository')
        fixture = cap['fixture_root']
        if fixture is not None:
            path(fixture)
            require(not any(below(fixture, root) or below(root, fixture)
                            for root in roots + list(fixtures)), 'Nested fixture root')
            require(below(cap['cwd'], fixture), 'Fixture cwd outside fixture root')
            fixtures.add(fixture)
            observed.append(fixture)
        else:
            require(cap['cwd'] == config['worktree_root'] + '/' + cap['lane'],
                    'Pure cwd differs from lane root')
        read_binding(cap['profile'], json_value=False)
        observed += [cap['cwd']] + cap['output_paths']
    for value in observed + protected:
        identities.update(no_links(value))
    return WorkspacePolicy(decode(encoded(wire)), config, tuple(scopes['lanes']),
                           tuple(requests['requests']), identities, policy_path, schema, validator,
                           policy_file_sha256)


def deny(request, code, reason):
    request_id = request.get('id') if type(request) is dict else None
    if type(request_id) is not str or not request_id:
        request_id = None
    return {'decision': 'deny', 'request_id': request_id, 'code': code, 'reason': reason}


def admit_workspace(request: WorkspaceRequest, policy: WorkspacePolicy) -> Admit | Deny:
    """Decide from validated policy observations; perform no filesystem effects."""
    try:
        require(isinstance(policy, WorkspacePolicy), 'Expected validated WorkspacePolicy')
        policy.validate('WorkspaceRequest', request)
        validate_request(request)
        destination = request['destination']
        protected = [policy.config['canonical_root']] + [s['root'] for s in policy.scopes]
        require(not any(below(destination, root) for root in protected
                        if root != destination), 'Destination is nested', 'NESTED_DESTINATION')
        require(destination != policy.config['canonical_root'], 'Canonical destination',
                'NESTED_DESTINATION')
        require(request['kind'] == 'worktree', 'Clone and repository copies are held',
                'UNAPPROVED_REQUEST')
        require(any(request == approved for approved in policy.requests),
                'Request lacks exact approval', 'UNAPPROVED_REQUEST')
        require(request['source'] == policy.config['canonical_root'] and
                destination == policy.config['worktree_root'] + '/' + request['lane'],
                'Request differs from approved roots', 'UNAPPROVED_REQUEST')
        require(destination not in policy.identities, 'Destination exists', 'COLLISION')
        parent = policy.identities.get(str(Path(destination).parent))
        require(parent is not None and stat.S_ISDIR(parent[2]),
                'Destination parent is absent', 'INVALID_INPUT')
        source = policy.identities.get(request['source'])
        require(source is not None and stat.S_ISDIR(source[2]), 'Source directory is absent')
        return {'decision': 'admit', 'request': dict(request), 'request_sha256': digest(request),
                'destination': destination, 'policy_sha256': digest(policy.wire)}
    except (ValueError, TypeError, KeyError) as error:
        return deny(request, getattr(error, 'code', 'INVALID_INPUT'), str(error))


def create_workspace(admitted: Admit, policy: WorkspacePolicy) -> dict:
    """Recheck admission immediately before the worktree writer starts."""
    result = {'id': 'C-CREATION', 'status': 'FAIL', 'prd_ids': ['ICM-R7', 'ICM-R13'],
              'argv': [], 'exit_code': None, 'stdout_sha256': None,
              'stderr_sha256': None, 'findings': [], 'reason': 'Creation denied'}
    try:
        require(isinstance(policy, WorkspacePolicy), 'Expected validated WorkspacePolicy')
        policy.validate('Admit', admitted)
        admitted = decode(encoded(admitted))
        require(digest(admitted['request']) == admitted['request_sha256'],
                'Changed request bytes', 'UNAPPROVED_REQUEST')
        require(digest(policy.wire) == admitted['policy_sha256'],
                'Changed policy digest', 'CHANGED_POLICY')
        wire = policy.wire
        if policy.policy_path is not None:
            raw = read_file(policy.policy_path)
            require(hashlib.sha256(raw).hexdigest() == policy.policy_file_sha256,
                    'Changed policy bytes', 'CHANGED_POLICY')
            wire = decode(raw)
        current = load_policy(wire, policy.policy_path)
        checked = admit_workspace(admitted['request'], current)
        if checked['decision'] == 'deny':
            raise AdmissionError(checked['code'], checked['reason'])
        require(checked == admitted, 'Changed admission', 'CHANGED_POLICY')
        require(current.identities == policy.identities,
                'Changed ancestor identity', 'LINK_AMBIGUITY')
        request = admitted['request']
        argv = ['git', '-C', request['source'], 'worktree', 'add', '--detach',
                '--', admitted['destination'], request['base_commit']]
        for value, identity in current.identities.items():
            require(no_links(value).get(value) == identity,
                    'Changed ancestor identity', 'LINK_AMBIGUITY')
        require(not os.path.lexists(admitted['destination']), 'Destination exists', 'COLLISION')
        completed = subprocess.run(argv, capture_output=True)
        result.update(argv=argv, exit_code=completed.returncode,
                      stdout_sha256=hashlib.sha256(completed.stdout).hexdigest(),
                      stderr_sha256=hashlib.sha256(completed.stderr).hexdigest(),
                      status='PASS' if completed.returncode == 0 else 'FAIL',
                      reason='Worktree created' if completed.returncode == 0 else
                      'Worktree writer failed')
    except (OSError, ValueError, TypeError, KeyError) as error:
        result['reason'] = getattr(error, 'code', 'INVALID_INPUT') + ': ' + str(error)
    return result



def run_lane(lane: str, capability: str, policy: WorkspacePolicy) -> dict:
    """Launch only the admitted worker, with the OS profile as its effect boundary."""
    result = {'id': 'C-CREATION', 'status': 'FAIL', 'prd_ids': ['ICM-R7', 'ICM-R13'],
              'argv': [], 'exit_code': None, 'stdout_sha256': None,
              'stderr_sha256': None, 'findings': [], 'reason': 'Worker denied'}
    outputs, process = [], None
    try:
        require(isinstance(policy, WorkspacePolicy), 'Expected validated WorkspacePolicy')
        string(lane)
        string(capability)
        wire = policy.wire
        if policy.policy_path is not None:
            raw = read_file(policy.policy_path)
            require(hashlib.sha256(raw).hexdigest() == policy.policy_file_sha256,
                    'Changed policy bytes', 'CHANGED_POLICY')
            wire = decode(raw)
        current = load_policy(wire, policy.policy_path)
        require(digest(current.wire) == digest(policy.wire),
                'Changed policy digest', 'CHANGED_POLICY')
        require(current.identities == policy.identities,
                'Changed ancestor identity', 'LINK_AMBIGUITY')
        matches = [cap for cap in current.wire['capabilities']
                   if cap['lane'] == lane and cap['id'] == capability]
        require(len(matches) == 1, 'Unapproved lane capability', 'UNAPPROVED_REQUEST')
        cap = matches[0]
        sandbox = '/usr/bin/sandbox-exec'
        require(os.path.isfile(sandbox) and os.access(sandbox, os.X_OK),
                'Sandbox support is absent', 'UNSAFE_TOOL')
        for value in cap['output_paths']:
            fd = os.open(value, os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK)
            outputs.append(fd)
            info = os.fstat(fd)
            require(stat.S_ISREG(info.st_mode) and
                    (info.st_dev, info.st_ino, info.st_mode) == current.identities[value],
                    'Changed output identity', 'LINK_AMBIGUITY')
        for value, identity in current.identities.items():
            require(no_links(value).get(value) == identity,
                    'Changed ancestor identity', 'LINK_AMBIGUITY')
        read_binding(cap['profile'], json_value=False)
        argv = [sandbox, '-f', cap['profile']['path'], *cap['argv']]
        result['argv'] = argv
        scratch = cap['fixture_root'] if cap['fixture_root'] is not None else cap['cwd']
        environment = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin',
                       'HOME': scratch, 'TMPDIR': scratch, 'LLMDB_ROOT': scratch,
                       'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONNOUSERSITE': '1',
                       'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null',
                       'GIT_CONFIG_SYSTEM': '/dev/null', 'GIT_TERMINAL_PROMPT': '0'}
        limit = cap['max_output_bytes']

        def bound_files():
            resource.setrlimit(resource.RLIMIT_FSIZE, (limit, limit))

        for fd in outputs:
            os.ftruncate(fd, 0)
        deadline = time.monotonic() + cap['timeout_seconds']
        process = subprocess.Popen(argv, cwd=cap['cwd'], env=environment,
                                   stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, start_new_session=True,
                                   preexec_fn=bound_files)
        failure, total = None, 0
        with selectors.DefaultSelector() as streams:
            streams.register(process.stdout, selectors.EVENT_READ, outputs[0])
            streams.register(process.stderr, selectors.EVENT_READ, outputs[1])
            while streams.get_map() and failure is None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    failure = 'Worker timeout exceeded'
                    break
                for key, _ in streams.select(remaining):
                    data = os.read(key.fileobj.fileno(), 65536)
                    if not data:
                        streams.unregister(key.fileobj)
                        continue
                    allowed = data[:max(0, limit - total)]
                    view = memoryview(allowed)
                    while view:
                        written = os.write(key.data, view)
                        view = view[written:]
                    total += len(data)
                    if total > limit:
                        failure = 'Worker output limit exceeded'
                        break
            if failure is None:
                try:
                    process.wait(timeout=max(0, deadline - time.monotonic()))
                except subprocess.TimeoutExpired:
                    failure = 'Worker timeout exceeded'
        # Reap the entire worker group, including descendants holding stream handles.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        result.update(exit_code=process.returncode,
                      status='PASS' if failure is None and process.returncode == 0 else 'FAIL',
                      reason=failure or ('Worker completed' if process.returncode == 0
                                         else 'Sandbox or worker failed'))
        for key, fd in zip(('stdout_sha256', 'stderr_sha256'), outputs):
            os.lseek(fd, 0, os.SEEK_SET)
            value = hashlib.sha256()
            while data := os.read(fd, 65536):
                value.update(data)
            result[key] = value.hexdigest()
    except (OSError, ValueError, TypeError, KeyError) as error:
        result['reason'] = getattr(error, 'code', 'INVALID_INPUT') + ': ' + str(error)
    finally:
        if process is not None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()
            process.stdout.close()
            process.stderr.close()
        for fd in outputs:
            os.close(fd)
    return result


def tool_decision(event: HookEvent, policy: WorkspacePolicy):
    require(isinstance(policy, WorkspacePolicy), 'Expected validated WorkspacePolicy')
    required = {'hook_event_name', 'cwd', 'tool_name', 'tool_input', 'session_id', 'tool_use_id'}
    require(type(event) is dict and required <= event.keys(), 'Malformed hook event')
    require(event['hook_event_name'] == 'PreToolUse', 'Wrong hook event')
    for key in ('tool_name', 'session_id', 'tool_use_id'):
        string(event[key])
    path(event['cwd'])
    data, tool = event['tool_input'], event['tool_name']
    require(type(data) is dict, 'Invalid tool input')
    require(tool not in policy.wire['disabled_tool_names'], 'Disabled tool', 'UNSAFE_TOOL')
    if tool in policy.wire['read_tools']:
        required, optional = {
            'Read': ({'file_path'}, {'offset', 'limit'}),
            'Glob': ({'pattern'}, {'path'}),
            'Grep': ({'pattern'}, {'path', 'glob', 'type', 'output_mode', '-A', '-B', '-C',
                                  '-n', '-i', 'head_limit', 'offset', 'multiline'})}[tool]
        require(required <= data.keys() <= required | optional, 'Unknown read tool shape')
        for key, value in data.items():
            if key in ('file_path', 'path'):
                path(value)
            elif key in ('offset', 'limit', '-A', '-B', '-C', 'head_limit'):
                require(type(value) is int and value >= 0, 'Invalid read bound')
            elif key in ('-n', '-i', 'multiline'):
                require(type(value) is bool, 'Invalid read flag')
            else:
                string(value)
        return 'allow', None
    if tool == 'Bash':
        object_fields(data, ('command',))
        string(data['command'])
        for cap in policy.wire['capabilities']:
            fixed = [cap['interpreter'], '-B', policy.wire['gate']['path'], 'run',
                     '--lane', cap['lane'], '--capability', cap['id']]
            if data['command'] == shlex.join(fixed) and event['cwd'] == cap['cwd']:
                return 'allow', None
        return 'deny', 'UNSAFE_TOOL'
    if tool in ('Write', 'Edit'):
        required = {'file_path', 'content'} if tool == 'Write' else {
            'file_path', 'old_string', 'new_string'}
        optional = set() if tool == 'Write' else {'replace_all'}
        require(required <= data.keys() <= required | optional, 'Unknown native tool shape')
        path(data['file_path'])
        for key in required - {'file_path'}:
            require(type(data[key]) is str, 'Invalid edit bytes')
        if 'replace_all' in data:
            require(type(data['replace_all']) is bool, 'Invalid replace flag')
        scopes = [s for s in policy.scopes if s['root'] == event['cwd']]
        require(len(scopes) == 1 and data['file_path'] in scopes[0]['file_paths'],
                'File is outside exact lane scope', 'UNSAFE_TOOL')
        identity = policy.identities.get(data['file_path'])
        require(identity is not None and stat.S_ISREG(identity[2]),
                'Native edit requires an existing regular file', 'UNSAFE_TOOL')
        return 'allow', None
    return 'deny', 'UNSAFE_TOOL'


def evaluate_tool(event: HookEvent, policy: WorkspacePolicy) -> Literal['allow', 'deny']:
    try:
        return tool_decision(event, policy)[0]
    except Exception:
        return 'deny'


def hook_denial(code):
    return {'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny',
            'permissionDecisionReason': 'ICM-R7: ' + code}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('check', 'hook', 'create', 'run'):
        command = commands.add_parser(name)
        if name == 'run':
            command.add_argument('--policy', default='/Volumes/memit/llmdb-tools/icm21/policy.json')
            command.add_argument('--lane', required=True)
            command.add_argument('--capability', required=True)
        else:
            command.add_argument('--policy', required=True)
            if name != 'hook':
                command.add_argument('--request', required=True)
    args = parser.parse_args()
    request = None
    try:
        policy = load_policy(decode(read_file(args.policy)), args.policy)
        if args.command == 'run':
            result = run_lane(args.lane, args.capability, policy)
            exit_code = 0 if result['status'] == 'PASS' else 1
        elif args.command == 'hook':
            decision, code = tool_decision(decode(sys.stdin.buffer.read()), policy)
            result, exit_code = ({} if decision == 'allow' else hook_denial(code)), 0
        else:
            request_raw = read_file(args.request)
            request = decode(request_raw)
            result = admit_workspace(request, policy)
            exit_code = 0 if result['decision'] == 'admit' else (
                2 if result['code'] == 'INVALID_INPUT' else 1)
            if args.command == 'create' and result['decision'] == 'admit':
                require(read_file(args.request) == request_raw,
                        'Changed request bytes', 'UNAPPROVED_REQUEST')
                result = create_workspace(result, policy)
                exit_code = 0 if result['status'] == 'PASS' else 1
    except Exception as error:
        code = getattr(error, 'code', 'INVALID_INPUT')
        if args.command == 'hook':
            result, exit_code = hook_denial(code), 0
        elif args.command == 'run':
            result = {'id': 'C-CREATION', 'status': 'FAIL', 'prd_ids': ['ICM-R7', 'ICM-R13'],
                      'argv': [], 'exit_code': None, 'stdout_sha256': None,
                      'stderr_sha256': None, 'findings': [],
                      'reason': code + ': Policy validation failed'}
            exit_code = 1
        else:
            result, exit_code = deny(request, code, 'Policy or request validation failed'), 2
    print(encoded(result).decode())
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
