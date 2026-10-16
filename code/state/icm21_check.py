"""Read-only validation of the approved ICM v2.1 common wire contracts."""
import argparse
import base64
import binascii
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


CHECK_IDS = frozenset('''C-KEEP C-CONTAINER C-HOLD C-MOVE C-PHASE C-AUDIT-IMPORT
C-QUEUE C-RUN C-MODEL C-WORKTREE C-TOOL C-ROOT C-LEDGER C-REFERENCES C-LABVIZ
C-LANES C-RECORD C-CREATION C-BOUNDARY C-STAGED C-GENERATED C-GRAFT C-AUDIT
C-HANDOFF C-TWINS C-WIRE C-ADMISSION C-LEAN'''.split())
WIRE_TYPES = frozenset('''str id path relpath sha int UTC Status PrdId b64
Finding CheckResult Coverage Exclusion Config Binding Hold Registries RegistryEntry
ReferenceResults ReaderResult ReferenceRow ReferenceManifest Repair RepairSet
CoverageArtifact ByteEdit AuditReport DirtySource WorkspaceRequest WorkspacePolicy
ApprovedRequests LaneScopes LaneScope LaneCapability Admit Deny'''.split())
# Audit check -> (area module beside this file, PRD trace from SPEC.md:48-57).
AUDIT_AREAS = {'C-ROOT': ('icm21_audit_root', 'ICM-R12'),
               'C-WORKTREE': ('icm21_audit_root', 'ICM-R5'),
               'C-GENERATED': ('icm21_audit_views', 'ICM-R8'),
               'C-TWINS': ('icm21_audit_views', 'ICM-R11'),
               'C-MODEL': ('icm21_audit_model', 'ICM-R3'),
               'C-HANDOFF': ('icm21_audit_handoff', 'ICM-R11')}


# Not a ValueError: per-example wire catches must not turn an absent seam
# into an observed FAIL that could match an expected FAIL.
class Unverified(Exception):
    pass


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def area(name):
    """Load a sibling area module by file path, never through sys.path."""
    path = Path(__file__).parent / (name + '.py')
    if not path.is_file():
        raise Unverified('Absent area module: ' + name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    # The checker's own class: a fresh import of this file would define a second one.
    module.Unverified = Unverified
    spec.loader.exec_module(module)
    return module


def unique(values, reason):
    require(len(values) == len(set(values)), reason)


def decode(value):
    try:
        return base64.b64decode(value, validate=True)
    except (ValueError, binascii.Error) as error:
        raise ValueError('invalid base64') from error


def validate_schema(value, rule, definitions):
    """Interpret the keyword subset used by the sealed machine schema annex."""
    if '$ref' in rule:
        name = rule['$ref'].removeprefix('#/$defs/')
        require(name in WIRE_TYPES and name in definitions, 'unknown wire type')
        validate_schema(value, definitions[name], definitions)
        if name in ('path', 'relpath'):
            parts = value.split('/')[1:] if name == 'path' else value.split('/')
            require(all(part not in ('', '.', '..') for part in parts),
                    'path is not normalized')
            require(not any(char in value for char in '\x00\r\n'),
                    'invalid path spelling')
        elif name == 'UTC':
            try:
                datetime.fromisoformat(value.removesuffix('Z') + '+00:00')
            except ValueError as error:
                raise ValueError('invalid UTC instant') from error
        elif name == 'b64':
            decode(value)
        validate_semantics(name, value)
        return
    if 'anyOf' in rule:
        for alternative in rule['anyOf']:
            try:
                validate_schema(value, alternative, definitions)
                return
            except ValueError:
                pass
        raise ValueError('no permitted alternative')
    if 'const' in rule:
        require(type(value) is type(rule['const']) and value == rule['const'],
                'invalid constant')
    if 'enum' in rule:
        require(value in rule['enum'], 'unknown enum value')
    kind = rule.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'integer': int,
             'null': type(None)}
    if kind is not None:
        require(kind in types and type(value) is types[kind], 'invalid field type')
    if kind == 'object':
        properties = rule['properties']
        require(set(rule['required']) <= value.keys(), 'missing field')
        require(value.keys() <= properties.keys(), 'extra field')
        for key, item in value.items():
            validate_schema(item, properties[key], definitions)
    elif kind == 'array':
        require(len(value) >= rule.get('minItems', 0), 'too few items')
        if rule.get('uniqueItems') or rule['items'].get('$ref') == '#/$defs/id':
            unique([json.dumps(x, sort_keys=True) for x in value], 'duplicate item')
        for item in value:
            validate_schema(item, rule['items'], definitions)
        item_name = rule['items'].get('$ref', '').removeprefix('#/$defs/')
        identity = {'ReaderResult': 'registry_id', 'LaneScope': 'lane'}.get(item_name, 'id')
        properties = definitions.get(item_name, {}).get('properties', {})
        if properties.get(identity) == {'$ref': '#/$defs/id'}:
            unique([item[identity] for item in value], 'duplicate collection ID')
    elif kind == 'string':
        require(len(value) >= rule.get('minLength', 0), 'empty string')
        if 'pattern' in rule:
            require(re.fullmatch(rule['pattern'], value) is not None, 'invalid spelling')
    elif kind == 'integer':
        require(value >= rule.get('minimum', 0), 'negative integer')


def validate_argv(argv):
    for argument in argv:
        tokens = re.findall(r'\{([A-Za-z_][A-Za-z0-9_]*)\}', argument)
        require(set(tokens) <= {'root', 'references', 'config', 'policy'},
                'unknown substitution token')


def validate_semantics(name, value):
    if name == 'RegistryEntry':
        require(set(value['check_ids']) <= CHECK_IDS, 'unknown check ID')
        if value['status'] == 'UNVERIFIED':
            require(value['hold_id'] is not None, 'UNVERIFIED registry needs a hold')
            if value['path'].startswith('/'):
                require(value['adapter_argv'] is None, 'UNVERIFIED external adapter')
        if value['adapter_argv'] is not None:
            validate_argv(value['adapter_argv'])
    elif name == 'Registries':
        validate_argv(value['dispatcher'])
        require(bool(value['dispatcher']), 'missing dispatcher')
        entries = value['reader_registry'] + value['loader_registry']
        unique([entry['id'] for entry in entries], 'duplicate registry ID')
    elif name == 'ReferenceResults':
        ids = [reader['registry_id'] for reader in value['readers']]
        require(ids == sorted(ids), 'reader results not in ID order')
    elif name == 'Config':
        require(set(value['required_checks']) <= CHECK_IDS, 'unknown check ID')
        require(value['nightly_utc'] == '02:00:00Z', 'invalid nightly time')
        roots = [value[key] for key in ('canonical_root', 'preservation_root',
                                      'worktree_root', 'tool_root')]
        roots += value['source_roots']
        for i, root in enumerate(roots):
            for other in roots[i + 1:]:
                require(root != other and not root.startswith(other + '/')
                        and not other.startswith(root + '/'), 'nested roots')
        unique([hold['id'] for hold in value['migration_holds']], 'duplicate hold ID')
    elif name == 'ReferenceRow':
        require(value['check_id'] in CHECK_IDS, 'unknown check ID')
        if value['role'] == 'current-reader':
            require(value['repair_path'] is not None, 'unbound current reader')
    elif name == 'Repair':
        require(bool(value['reader_ids']) and bool(value['reference_ids']),
                'unbound repair')
        end = 0
        for edit in value['edits']:
            require(edit['start'] >= end, 'overlapping or unordered byte edits')
            end = edit['end']
    elif name == 'ByteEdit':
        require(value['start'] <= value['end'], 'reversed byte edit')
        require(len(decode(value['before_base64'])) == value['end'] - value['start'],
                'byte edit length mismatch')
    elif name in ('ApprovedRequests', 'RepairSet', 'LaneScopes'):
        field, key = {'ApprovedRequests': ('requests', 'id'),
                      'RepairSet': ('repairs', 'id'),
                      'LaneScopes': ('lanes', 'lane')}[name]
        unique([item[key] for item in value[field]], 'duplicate collection ID')
    elif name == 'WorkspacePolicy':
        unique([item['id'] for item in value['capabilities']], 'duplicate capability ID')
    elif name == 'LaneCapability':
        validate_argv(value['argv'])
    elif name == 'Admit':
        raw = json.dumps(value['request'], sort_keys=True, separators=(',', ':')).encode()
        require(hashlib.sha256(raw).hexdigest() == value['request_sha256'],
                'request digest mismatch')
        require(value['destination'] == value['request']['destination'],
                'admitted destination mismatch')
    elif name == 'AuditReport':
        results, findings = value['check_results'], value['findings']
        ids = [item['id'] for item in results]
        finding_ids = [item['id'] for item in findings]
        unique(ids, 'duplicate check ID')
        unique(finding_ids, 'duplicate finding ID')
        require(set(ids) <= set(value['required_checks']), 'unknown result ID')
        linked = {key for result in results for key in result['findings']}
        require(linked == set(finding_ids), 'dangling or unreferenced finding ID')
        coverage = value['coverage']
        require(set(coverage['checked_registry_ids'])
                <= set(coverage['required_registry_ids']), 'unknown checked registry ID')
        instant = datetime.fromisoformat(value['observed_at'].removesuffix('Z') + '+00:00')
        require(value['check_id'] == instant.strftime('%H%M%S.%fZ-') + value['mode'],
                'check ID and captured UTC instant disagree')
        missing = (set(value['required_checks']) - set(ids)
                   or set(coverage['required_registry_ids'])
                   - set(coverage['checked_registry_ids']))
        statuses = {result['status'] for result in results}
        status = ('FAIL' if 'FAIL' in statuses else
                  'UNVERIFIED' if missing or 'UNVERIFIED' in statuses else 'PASS')
        require(value['overall_status'] == status, 'false audit reduction')


def validate_wire(name, value, schema, fixtures, root=None):
    if name == 'LabvizMoves':
        area('icm21_labviz_wire').validate_labviz_moves(value, schema, fixtures, root)
        return
    if name == 'ReferenceRow[]':
        require(type(value) is list, 'expected reference array')
        for row in value:
            validate_wire('ReferenceRow', row, schema, fixtures)
        unique([row['id'] for row in value], 'duplicate reference ID')
        targets = {}
        for row in value:
            key = (row['consumer'], row['reference'])
            require(key not in targets or targets[key] == row['final_target'],
                    'ambiguous historical key')
            targets[key] = row['final_target']
        return
    validate_schema(value, {'$ref': '#/$defs/' + name}, schema['$defs'])
    if name == 'ReferenceManifest':
        for key in ('references', 'registries', 'executor', 'repairs', 'coverage'):
            binding = value[key]
            require(binding['path'] in fixtures, 'missing bound fixture')
            require(hashlib.sha256(fixtures[binding['path']]).hexdigest()
                    == binding['sha256'], 'changed binding')


def wire(schema, examples, root=None):
    require(type(examples) is dict and set(examples) == {'schema_version', 'fixtures',
                                                       'examples'}, 'invalid examples envelope')
    require(type(examples['schema_version']) is int and examples['schema_version'] == 1,
            'invalid examples version')
    require(type(examples['fixtures']) is dict, 'invalid fixture table')
    fixtures = {}
    for path, record in examples['fixtures'].items():
        validate_schema(path, {'$ref': '#/$defs/path'}, schema['$defs'])
        require(type(record) is dict and set(record) == {'bytes_base64'},
                'invalid fixture record')
        require(type(record['bytes_base64']) is str, 'invalid fixture bytes')
        fixtures[path] = decode(record['bytes_base64'])
    require(type(examples['examples']) is list and bool(examples['examples']),
            'empty examples')
    results = []
    for example in examples['examples']:
        require(type(example) is dict and set(example) == {'id', 'type', 'expected',
                    'layer', 'value', 'rule'}, 'invalid example record')
        for key in ('id', 'type', 'rule'):
            require(type(example[key]) is str and bool(example[key]), 'invalid example field')
        require(example['expected'] in ('PASS', 'FAIL'), 'invalid expected status')
        require(example['layer'] in ('schema', 'semantic'), 'invalid example layer')
        require(example['type'] in WIRE_TYPES
                or example['type'] in ('ReferenceRow[]', 'LabvizMoves'),
                'wire type outside approved scope')
        try:
            validate_wire(example['type'], example['value'], schema, fixtures, root)
            observed, reason = 'PASS', 'Valid wire value'
        except ValueError as error:
            observed, reason = 'FAIL', str(error)
        results.append({'id': example['id'], 'expected': example['expected'],
                        'observed': observed, 'reason': reason})
    unique([item['id'] for item in results], 'duplicate example ID')
    return {'status': 'PASS' if all(item['expected'] == item['observed']
                                  for item in results) else 'FAIL', 'results': results}


def reject_constant(value):
    raise ValueError('invalid JSON constant: ' + value)


def read_json(path):
    return json.loads(path.read_bytes().decode('utf-8'), parse_constant=reject_constant)


def audit_schema():
    return read_json(Path(__file__).parent / 'icm21/WIRE-SCHEMAS.json')


def active_graft(value):
    def mentions(item):
        if isinstance(item, str):
            return re.search(r'\bgraft\b', item, re.IGNORECASE) is not None
        if isinstance(item, list):
            return any(mentions(child) for child in item)
        if isinstance(item, dict):
            return any(mentions(key) or mentions(child) for key, child in item.items())
        return False

    require(type(value) is dict, 'loader config must be an object')
    return any(mentions(value[key]) for key in ('hooks', 'mcpServers', 'plugins')
               if key in value) or mentions(value.get('search', {}).get('exceptions', [])) \
        or any(mentions(key) and enabled is True
               for key, enabled in value.get('enabledPlugins', {}).items())


def git_environment():
    """The caller's environment without GIT_*, so cwd alone names the repository."""
    return {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}


def repository_copies(root, config, coverage):
    """Detect copies from Git identity and layout locators, never bulk bytes."""
    violations, missing = {}, []
    coverage['inspected'].append(str(root))

    def violation(path, reason):
        violations.setdefault(str(path), set()).add(reason)

    def git(*argv):
        result = subprocess.run(['git', *argv], cwd=root, env=git_environment(),
                                capture_output=True)
        return result.returncode, result.stdout.decode('utf-8', 'replace').strip()

    ownership = Path(config['ownership_path']['path'])
    try:
        raw = ownership.read_bytes()
        coverage['inspected'].append(str(ownership))
        if hashlib.sha256(raw).hexdigest() != config['ownership_path']['sha256']:
            missing.append('Ownership authority digest mismatch')
    except OSError:
        missing.append('Ownership authority is unreadable')

    code, top = git('rev-parse', '--show-toplevel')
    if code or not top or Path(top).resolve() != root.resolve():
        missing.append('Canonical Git root identity is unavailable')
        common = None
    else:
        code, value = git('rev-parse', '--git-common-dir')
        common = (root / value).resolve() if not code and value else None
        if common is None:
            missing.append('Canonical Git common-dir identity is unavailable')
        code, value = git('worktree', 'list', '--porcelain')
        if code:
            missing.append('Registered worktree identity is unavailable')
        else:
            for record in value.split('\n\n'):
                fields = record.splitlines()
                if not fields or not fields[0].startswith('worktree '):
                    continue
                path = Path(fields[0][9:])
                if path != root and path.is_relative_to(root):
                    coverage['inspected'].append(str(path))
                    branch = next((line[7:] for line in fields
                                   if line.startswith('branch ')), 'detached')
                    violation(path, 'Registered nested worktree or residue: ' + branch)

    def unreadable(error):
        missing.append('Unreadable boundary path: ' + str(error.filename))

    markers = (('CLAUDE.md', 'program/program_state.json', '_index/path-map.tsv'),
               ('CONTEXT.md', 'RUNBOOK.md', 'EXPERIMENTS.md'))
    for directory, children, files in os.walk(root, onerror=unreadable):
        children.sort()
        if '.git' in children:
            children.remove('.git')
        path = Path(directory)
        coverage['inspected'].append(str(path))
        if path == root:
            continue
        for names in markers:
            if all((path / name).is_file() for name in names):
                violation(path, 'Repository authority marker set: ' + ', '.join(names))
        dotgit = path / '.git'
        if not dotgit.exists() and not dotgit.is_symlink():
            continue
        coverage['inspected'].append(str(dotgit))
        try:
            if dotgit.is_dir():
                gitdir = dotgit.resolve()
            else:
                text = dotgit.read_text(encoding='utf-8').strip()
                require(text.startswith('gitdir: ') and '\n' not in text,
                        'invalid Git directory locator')
                gitdir = (path / text[8:]).resolve()
            # Neither the approved engine nor a named miniature fixture can
            # exempt a common-dir link back into this repository.
            if common is not None and (gitdir == common or
                    gitdir.is_relative_to(common / 'worktrees')):
                violation(path, 'Repository Git directory identity or worktree residue')
            commondir = gitdir / 'commondir'
            shared = (gitdir / commondir.read_text(encoding='utf-8').strip()).resolve() \
                if commondir.is_file() else gitdir
            if common is not None and shared == common:
                violation(path, 'Repository Git common-dir identity')
            elif not gitdir.is_dir():
                missing.append('Unresolved Git directory locator: ' + str(dotgit))
        except (OSError, ValueError) as error:
            missing.append('Unreadable Git identity at ' + str(dotgit) + ': '
                           + type(error).__name__)
    return violations, missing


def lane_path(value):
    path = Path(value)
    require(path.is_absolute() and str(path) == value
            and '..' not in path.parts
            and not any(char in value for char in '\x00\r\n'),
            'invalid lane path')
    return path


def parse_ownership(raw):
    lines = raw.decode('utf-8').splitlines()
    require(lines and lines[0] == 'phase\tlane\tpath\tscope\tprd_ids',
            'invalid ownership header')
    rows = []
    for line in lines[1:]:
        fields = line.split('\t')
        require(len(fields) == 5, 'invalid ownership row')
        phase, lane, path, scope, prd_ids = fields
        require(re.fullmatch(r'[0-9]+', phase) is not None, 'invalid lane phase')
        require(bool(lane) and lane not in ('.', '..') and '/' not in lane,
                'invalid lane identifier')
        require(not any(char in lane for char in '\x00\r\n'), 'invalid lane identifier')
        require(scope == 'exact-or-prefix', 'invalid ownership scope')
        ids = prd_ids.split(',')
        require(all(re.fullmatch(r'ICM-R(?:[1-9]|1[0-5])', item) for item in ids),
                'invalid ownership requirement')
        unique(ids, 'duplicate ownership requirement')
        rows.append((int(phase), lane, lane_path(path)))
    return rows


def inspect_lanes(ownership, coverage, expected=None, worktree_root=None):
    """Check declared ownership and brief data; never act on custody or idle."""
    violations, missing = {}, []
    try:
        raw = ownership.read_bytes()
        coverage['inspected'].append(str(ownership))
    except OSError as error:
        return violations, ['Ownership authority is unreadable: ' + str(error)]
    if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
        return violations, ['Ownership authority digest mismatch']
    try:
        rows = parse_ownership(raw)
    except ValueError as error:
        return {str(ownership): str(error)}, missing
    for index, (phase, lane, path) in enumerate(rows):
        for other_phase, other_lane, other in rows[index + 1:]:
            if phase == other_phase and (path.is_relative_to(other)
                                        or other.is_relative_to(path)):
                reason = f'Overlapping ownership in phase {phase}: {lane} {path}; {other_lane} {other}'
                violations[str(ownership)] = reason
    if worktree_root is None:
        return violations, missing
    lanes = sorted({lane for _, lane, _ in rows})
    for lane in lanes:
        brief = worktree_root / lane / 'BRIEF.md'
        try:
            text = brief.read_text(encoding='utf-8')
            coverage['inspected'].append(str(brief))
        except OSError as error:
            missing.append('Lane brief is unreadable: ' + str(error))
            continue
        except UnicodeError as error:
            violations[str(brief)] = 'Invalid lane brief encoding: ' + str(error)
            continue
        fields = {}
        required = {'owner', 'branch', 'base', 'output', 'custody', 'idle'}
        try:
            for line in text.splitlines():
                key, separator, value = line.partition(':')
                if separator and key in required:
                    require(key not in fields, 'duplicate lane brief field: ' + key)
                    fields[key] = value.strip()
            absent = required - fields.keys()
            if absent:
                missing.append(str(brief) + ': missing ' + ', '.join(sorted(absent)))
            if 'owner' in fields:
                require(fields['owner'] == lane, 'lane owner mismatch')
            if 'branch' in fields:
                require(bool(fields['branch']), 'empty lane branch')
            if 'base' in fields:
                require(re.fullmatch(r'[0-9a-f]{40}', fields['base']) is not None,
                        'invalid lane base')
            if 'output' in fields:
                output = lane_path(fields['output'])
                require(output in {path for _, owner, path in rows if owner == lane},
                        'lane output is outside its exact ownership')
            if 'custody' in fields:
                require(bool(fields['custody']), 'empty lane custody')
            if 'idle' in fields:
                require(fields['idle'] in ('true', 'false'), 'invalid lane idle state')
        except ValueError as error:
            violations[str(brief)] = str(error)
    return violations, missing


def audit(root, mode, config):
    """Inspect repository boundaries and registered loader data without adapters."""
    started = time.monotonic_ns()
    instant = datetime.now(timezone.utc)
    schema = audit_schema()
    validate_wire('Config', config, schema, {})
    root = Path(root)
    require(str(root) == config['canonical_root'] and root.is_dir(), 'invalid audit root')
    require(mode in ('session', 'nightly'), 'invalid audit mode')
    coverage = {'inspected': [], 'excluded': [], 'required_registry_ids': [],
                'checked_registry_ids': []}
    findings, results = [], []

    def violation(path, reason):
        identity = str(path) + '\n' + reason
        finding_id = 'F-GRAFT-' + hashlib.sha256(identity.encode()).hexdigest()
        findings.append({'id': finding_id, 'status': 'FAIL', 'prd_ids': ['ICM-R9'],
                         'paths': [str(path)], 'evidence': [], 'reason': reason,
                         'previous_finding': None, 'resolution_receipt': None})

    def bound_bytes(path, expected):
        raw = path.read_bytes()
        coverage['inspected'].append(str(path))
        require(hashlib.sha256(raw).hexdigest() == expected, 'changed bound source')
        return raw

    if 'C-GRAFT' in config['required_checks']:
        missing = []
        registry_path = Path(config['registries']['path'])
        try:
            raw = bound_bytes(registry_path, config['registries']['sha256'])
            registry = json.loads(raw.decode('utf-8'), parse_constant=reject_constant)
            validate_wire('Registries', registry, schema, {})
            for role in ('reader', 'loader'):
                require(all(entry['role'] == role for entry in registry[role + '_registry']),
                        'registry role mismatch')
        except OSError as error:
            missing.append(str(error))
        except (ValueError, KeyError, TypeError) as error:
            violation(registry_path, str(error))
        else:
            entries = [entry for entry in registry['reader_registry']
                       + registry['loader_registry'] if 'C-GRAFT' in entry['check_ids']]
            coverage['required_registry_ids'] = sorted(entry['id'] for entry in entries)
            if not entries:
                missing.append('No registered Graft loader coverage')
            for entry in entries:
                path = root / entry['path']
                if entry['status'] == 'UNVERIFIED' or entry['source_sha256'] is None:
                    missing.append(entry['id'])
                    continue
                try:
                    raw = bound_bytes(path, entry['source_sha256'])
                    value = json.loads(raw.decode('utf-8'), parse_constant=reject_constant)
                    present = active_graft(value)
                except OSError as error:
                    missing.append(entry['id'] + ': ' + str(error))
                except (ValueError, KeyError, TypeError, AttributeError) as error:
                    violation(path, str(error))
                else:
                    coverage['checked_registry_ids'].append(entry['id'])
                    if present:
                        violation(path, 'Active Graft loader or search exception')
        status = 'FAIL' if findings else 'UNVERIFIED' if missing else 'PASS'
        results.append({'id': 'C-GRAFT', 'status': status, 'prd_ids': ['ICM-R9'],
                        'argv': [], 'exit_code': None, 'stdout_sha256': None,
                        'stderr_sha256': None, 'findings': [f['id'] for f in findings],
                        'reason': '; '.join(missing) if missing else
                                  'Active Graft detected' if findings else
                                  'Registered loader data is Graft-free'})
    if 'C-BOUNDARY' in config['required_checks']:
        copies, missing = repository_copies(root, config, coverage)
        finding_ids = []
        for path, reasons in sorted(copies.items()):
            reason = '; '.join(sorted(reasons))
            finding_id = 'F-BOUNDARY-' + hashlib.sha256(path.encode()).hexdigest()
            finding_ids.append(finding_id)
            findings.append({'id': finding_id, 'status': 'FAIL', 'prd_ids': ['ICM-R7'],
                             'paths': [path], 'evidence': [], 'reason': reason,
                             'previous_finding': None, 'resolution_receipt': None})
        status = 'FAIL' if copies else 'UNVERIFIED' if missing else 'PASS'
        results.append({'id': 'C-BOUNDARY', 'status': status, 'prd_ids': ['ICM-R7'],
                        'argv': [], 'exit_code': None, 'stdout_sha256': None,
                        'stderr_sha256': None, 'findings': finding_ids,
                        'reason': '; '.join(missing) if missing else
                                  'Repository copies or worktree residues detected' if copies else
                                  'No repository copy signatures or worktree residues detected'})
    if 'C-LANES' in config['required_checks']:
        ownership = config['ownership_path']
        problems, missing = inspect_lanes(Path(ownership['path']), coverage,
                                         ownership['sha256'], Path(config['worktree_root']))
        finding_ids = []
        for path, reason in sorted(problems.items()):
            finding_id = 'F-LANES-' + hashlib.sha256((path + '\n' + reason).encode()).hexdigest()
            finding_ids.append(finding_id)
            findings.append({'id': finding_id, 'status': 'FAIL', 'prd_ids': ['ICM-R11'],
                             'paths': [path], 'evidence': [], 'reason': reason,
                             'previous_finding': None, 'resolution_receipt': None})
        status = 'FAIL' if problems else 'UNVERIFIED' if missing else 'PASS'
        results.append({'id': 'C-LANES', 'status': status, 'prd_ids': ['ICM-R11'],
                        'argv': [], 'exit_code': None, 'stdout_sha256': None,
                        'stderr_sha256': None, 'findings': finding_ids,
                        'reason': '; '.join(missing) if missing else
                                  'Lane ownership or brief violations detected' if problems else
                                  'Disjoint lane ownership and complete lane briefs'})
    for check_id in [item for item in config['required_checks'] if item in AUDIT_AREAS]:
        name, prd_id = AUDIT_AREAS[check_id]
        try:
            status, reason, area_findings = area(name).check(check_id, root, mode,
                                                             config, coverage)
        except Unverified as error:
            status, reason, area_findings = 'UNVERIFIED', str(error), []
        findings.extend(area_findings)
        results.append({'id': check_id, 'status': status, 'prd_ids': [prd_id],
                        'argv': [], 'exit_code': None, 'stdout_sha256': None,
                        'stderr_sha256': None,
                        'findings': [finding['id'] for finding in area_findings],
                        'reason': reason})
    coverage['inspected'] = sorted(set(coverage['inspected']))
    coverage['checked_registry_ids'].sort()
    statuses = {result['status'] for result in results}
    incomplete = (set(config['required_checks']) - {result['id'] for result in results}
                  or set(coverage['required_registry_ids'])
                  - set(coverage['checked_registry_ids']))
    overall = ('FAIL' if 'FAIL' in statuses else
               'UNVERIFIED' if incomplete or 'UNVERIFIED' in statuses else 'PASS')
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, env=git_environment(),
                            capture_output=True)
    report = {'schema_version': 1, 'check_id': instant.strftime('%H%M%S.%fZ-') + mode,
              'observed_at': instant.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'root': str(root),
              'source_commit': commit.stdout.decode().strip() if commit.returncode == 0
                               else 'UNVERIFIED',
              'dirty_source_digests': [], 'mode': mode, 'coverage': coverage,
              'required_checks': config['required_checks'], 'check_results': results,
              'findings': findings, 'previous_report': None, 'overall_status': overall,
              'duration_ms': (time.monotonic_ns() - started) // 1000000,
              'reviewed_narrative_paths': [], 'unreviewed_narrative_paths': [str(root)]}
    validate_wire('AuditReport', report, schema, {})
    return report


# Staged source/output closure (SPEC.md:445-460). An entry names a file or a whole tree.
STAGED_CLOSURE = (
    # Generator, resolver, checker and hook implementations; admission configuration.
    'code/state/build_index.py', 'code/state/resolve_path.py', 'code/state/llmdb_records.py',
    'code/state/render_state.py', 'code/agents/twins.py', 'code/gates/closeout_check.py',
    'code/gates/closeout_fingerprints.json', 'code/ops/git/hooks/pre-commit',
    'code/state/icm21_check.py', 'code/state/icm21/WIRE-SCHEMAS.json',
    '_system/governance/workspace-admission.json',
    # Generator inputs.
    'program/program_state.json', 'evidence/CORPUS', 'program/checkpoints',
    '_index/path-map.tsv', '_index/icm21-path-map.tsv', '_index/anchor-map.tsv',
    # Close-out narrative trackers and the globbed hypothesis register (closeout_check.py).
    'program/runbook', 'program/registers', 'program/PROGRESS.md',
    'program/EVIDENCE_INDEX.md', 'README.md', 'program/SESSION_BOOTSTRAP.md',
    '_system/governance/REPRODUCIBILITY.md',
    # Outputs and authority twins.
    '_index/experiments.md', '_index/projects.md', '_index/evidence.md',
    '_index/checkpoints.md', 'code/apps/labviz/results_moves.json', 'program/STATUS.md',
    '_index/program-state.md', 'program/scorecard.md', 'CLAUDE.md', 'AGENTS.md',
    'routing.md', 'map/CLAUDE.md', 'map/AGENTS.md', 'map/routing.md')
# Folder membership is a generator input: every tracked or untracked non-ignored path
# under these trees counts, but only experiment CONTEXT.md bytes are read.
STAGED_MEMBERSHIP = ('experiments', 'projects')
STAGED_CHECKS = (('code/state/build_index.py', '--check'),
                 ('code/state/render_state.py', '--check'),
                 ('code/agents/twins.py', '--check'),
                 ('code/gates/closeout_check.py', '--audit'))


def disk_entry(path, object_format):
    """(mode, blob id) of the bytes on disk, as Git would stage them; None when absent."""
    if path.is_symlink():
        mode, raw = '120000', os.readlink(path).encode('utf-8', 'surrogateescape')
    elif path.is_file():
        mode = '100755' if path.stat().st_mode & 0o100 else '100644'
        raw = path.read_bytes()
    else:
        return None
    header = b'blob ' + str(len(raw)).encode() + b'\0'
    return mode, hashlib.new(object_format, header + raw).hexdigest()


def check_staged(root):
    """Read-only: reject disk/index differences and stale outputs across the staged closure."""
    root = Path(root)
    findings = []

    def fail(relative, reason):
        identity = relative + '\n' + reason
        findings.append({'id': 'F-STAGED-' + hashlib.sha256(identity.encode()).hexdigest(),
                         'status': 'FAIL', 'prd_ids': ['ICM-R8'],
                         'paths': [str(root / relative)], 'evidence': [], 'reason': reason,
                         'previous_finding': None, 'resolution_receipt': None})

    def git(*argv):
        result = subprocess.run(['git', '--literal-pathspecs', *argv], cwd=root,
                                env=git_environment(), capture_output=True)
        if result.returncode:
            raise ValueError('git ' + argv[0] + ' failed: '
                             + result.stderr.decode('utf-8', 'replace').strip())
        return result.stdout.decode('utf-8', 'surrogateescape')

    try:
        top = git('rev-parse', '--show-toplevel').strip()
        require(top and Path(top).resolve() == root.resolve(), 'staged root is not the Git root')
        object_format = git('rev-parse', '--show-object-format').strip()
        filemode = git('config', '--bool', '--default', 'true', 'core.filemode').strip() == 'true'
        sparse = git('config', '--bool', '--default', 'false',
                     'core.sparseCheckout').strip() == 'true'
        closure = set(STAGED_CLOSURE)
        registry = read_json(root / 'code/gates/closeout_fingerprints.json')
        require(type(registry) is dict, 'fingerprint registry must be an object')
        for key, spec in registry.items():
            if not key.startswith('_'):
                require(type(spec) is dict and type(spec.get('source')) is str and spec['source'],
                        'fingerprint ' + key + ' has no source')
                closure.add(spec['source'].rstrip('/'))
        anchors = (root / '_index/anchor-map.tsv').read_bytes().decode('utf-8').splitlines()
        for row in anchors[1:]:
            fields = row.split('\t')
            require(len(fields) == 4 and fields[2], 'malformed anchor-map row')
            closure.add(fields[2])
        pathspecs = sorted(closure | set(STAGED_MEMBERSHIP))
        index = git('ls-files', '-z', '-t', '-s', '--', *pathspecs)
        untracked = git('ls-files', '-z', '--others', '--exclude-standard', '--', *pathspecs)
    except (OSError, ValueError, KeyError, TypeError) as error:
        fail('.', 'Staged closure is unverifiable: ' + str(error))
        return tuple(findings)

    def read_bytes(relative):
        return relative in closure or any(relative.startswith(entry + '/') for entry in closure) \
            or (relative.startswith('experiments/') and relative.count('/') == 2
                and relative.endswith('/CONTEXT.md'))

    for relative in sorted(filter(None, untracked.split('\0'))):
        fail(relative, 'Untracked closure path is absent from the index')
    for record in filter(None, index.split('\0')):
        meta, relative = record.split('\t', 1)
        tag, mode, blob, stage = meta.split(' ')
        if stage != '0':
            fail(relative, 'Unmerged closure path')
            continue
        if tag == 'S' and sparse and not os.path.lexists(root / relative):
            continue  # skip-worktree path a sparse checkout left off disk: no disk claim
        try:
            disk = disk_entry(root / relative, object_format)
        except OSError as error:
            fail(relative, 'Unreadable closure path: ' + type(error).__name__)
            continue
        if disk is None:
            fail(relative, 'Staged closure path is missing on disk')
        elif read_bytes(relative) and disk[1] != blob:
            fail(relative, 'Disk bytes differ from the staged blob')
        elif read_bytes(relative) and (disk[0] != mode if filemode or mode == '120000'
                                       else (disk[0] == '120000') != (mode == '120000')):
            fail(relative, 'Disk mode ' + disk[0] + ' differs from staged mode ' + mode)
    environment = dict(git_environment(), LLMDB_ROOT=str(root), PYTHONDONTWRITEBYTECODE='1')
    for script, mode in STAGED_CHECKS:
        if not (root / script).is_file():
            fail(script, 'Staged check implementation is missing')
            continue
        result = subprocess.run([sys.executable, '-B', str(root / script), mode], cwd=root,
                                env=environment, capture_output=True)
        if result.returncode:
            tail = (result.stdout + result.stderr).decode('utf-8', 'replace').strip()
            fail(script, script + ' ' + mode + ' failed: ' + tail[-400:])
    schema = audit_schema()
    for finding in findings:
        validate_wire('Finding', finding, schema, {})
    return tuple(findings)


def check_references(root, manifest):
    results = area('icm21_references').check_references(root, manifest)
    validate_wire('ReferenceResults', results, audit_schema(), {})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    command = commands.add_parser('wire')
    command.add_argument('--root', type=Path, required=True)
    command.add_argument('--schema', type=Path, required=True)
    command.add_argument('--examples', type=Path, required=True)
    command = commands.add_parser('lanes')
    command.add_argument('--root', type=Path, required=True)
    command.add_argument('--ownership', type=Path, required=True)
    command = commands.add_parser('references')
    command.add_argument('--root', type=Path, required=True)
    command.add_argument('--manifest', type=Path, required=True)
    command = commands.add_parser('staged')
    command.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    code = None
    try:
        require(args.root.is_absolute() and args.root.is_dir(), 'invalid root')
        if args.command == 'lanes':
            problems, missing = inspect_lanes(args.ownership, {'inspected': []})
            result = {'status': 'FAIL' if problems else 'UNVERIFIED' if missing else 'PASS',
                      'violations': problems, 'missing': missing}
        elif args.command == 'staged':
            findings = check_staged(args.root)
            result = {'status': 'FAIL' if findings else 'PASS', 'findings': list(findings)}
        elif args.command == 'references':
            result = check_references(args.root, read_json(args.manifest))
            statuses = {check['status'] for reader in result['readers']
                        for check in reader['checks']}
            code = 1 if 'FAIL' in statuses else 0 if statuses == {'PASS'} else 2
        else:
            result = wire(read_json(args.schema), read_json(args.examples), args.root)
    except Unverified as error:
        result, code = {'status': 'UNVERIFIED', 'reason': str(error)}, 2
    except (OSError, ValueError, KeyError, TypeError) as error:
        result, code = {'status': 'FAIL', 'reason': str(error)}, 1
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))
    return (0 if result['status'] == 'PASS' else 1) if code is None else code


if __name__ == '__main__':
    raise SystemExit(main())
