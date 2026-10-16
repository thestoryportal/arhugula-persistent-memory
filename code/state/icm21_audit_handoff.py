"""C-HANDOFF area: registered handoffs carry the sealed context directive and obey its budget.

Read-only. A handoff is compared, never edited. `Unverified` is injected by icm21_check.area().
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re


VERBATIM = Path(__file__).parent / 'icm21/verbatim.json'
HEADING = '## Context management (BINDING,'
# The handoff contents the directive itself names, as line labels.
FIELDS = (('done', r'Done'), ('in flight', r'In flight'),
          ('exact paths', r'Exact (?:file )?paths'), ('next step', r'Next (?:action|step)'),
          ('open risks', r'Open risks'))
BUDGET = 'context-budget.json'


def wire_checker():
    """The checker's own Registries validator, loaded by file path like area()."""
    path = Path(__file__).parent / 'icm21_check.py'
    spec = importlib.util.spec_from_file_location('icm21_check', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def directive():
    try:
        texts = [entry['text'] for entry in json.loads(VERBATIM.read_bytes())
                 if entry['text'].startswith(HEADING)]
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        raise Unverified('Unreadable sealed directive ' + str(VERBATIM) + ': '
                         + type(error).__name__ + ': ' + str(error))
    if len(texts) != 1:
        raise Unverified('Sealed context directive is not unique in ' + str(VERBATIM))
    return texts[0]


def finding(path, reason):
    finding_id = 'F-HANDOFF-' + hashlib.sha256((str(path) + '\n' + reason).encode()).hexdigest()
    return {'id': finding_id, 'status': 'FAIL', 'prd_ids': ['ICM-R11'],
            'paths': [str(path)], 'evidence': [], 'reason': reason,
            'previous_finding': None, 'resolution_receipt': None}


def entries(config, coverage):
    """Bound registry rows for C-HANDOFF, or a FAIL finding for malformed authority."""
    path = Path(config['registries']['path'])
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise Unverified('Unreadable registry ' + str(path) + ': ' + str(error))
    coverage['inspected'].append(str(path))
    if hashlib.sha256(raw).hexdigest() != config['registries']['sha256']:
        raise Unverified('Changed bound registry: ' + str(path))
    checker = wire_checker()
    try:
        registry = json.loads(raw.decode('utf-8'), parse_constant=checker.reject_constant)
        checker.validate_wire('Registries', registry, checker.audit_schema(), {})
        for role in ('reader', 'loader'):
            checker.require(all(entry['role'] == role
                                for entry in registry[role + '_registry']),
                            'registry role mismatch')
    except OSError as error:
        raise Unverified('Unreadable wire schema: ' + str(error))
    except (ValueError, KeyError, TypeError, AttributeError) as error:
        return [], finding(path, 'Invalid bound registry: ' + str(error))
    found = [entry for entry in registry['reader_registry'] + registry['loader_registry']
             if 'C-HANDOFF' in entry['check_ids']]
    for entry in found:
        if entry['id'] not in coverage['required_registry_ids']:
            coverage['required_registry_ids'].append(entry['id'])
    if not found:
        raise Unverified('No registered handoff coverage')
    return found, None


def text_breaches(text, sealed):
    breaches = [] if sealed in text else ['context directive is not verbatim']
    return breaches + ['missing handoff field: ' + name for name, label in FIELDS
                       if not re.search(r'^(?:[-*] )?' + label + r':[ \t]*\S',
                                        text, re.MULTILINE | re.IGNORECASE)]


def budget_breaches(path):
    """Budget evidence sits beside its lane handoff; absent or malformed is unobserved."""
    try:
        value = json.loads(path.read_bytes())
        left = value['context_left_percent']
        flags = [value[key] for key in ('starting_new_work', 'long_step_pending', 'compacted')]
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise Unverified('Unobserved context budget ' + str(path) + ': ' + str(error))
    if (isinstance(left, bool) or not isinstance(left, (int, float)) or not 0 <= left <= 100
            or not all(isinstance(flag, bool) for flag in flags)):
        raise Unverified('Malformed context budget: ' + str(path))
    starting, long_step, compacted = flags
    if not starting:
        return []
    return [reason for breached, reason in (
        (left < 60, 'new work started below 60% context left'),
        (left <= 45 and long_step, 'new work with a long step pending at 45% or less left'),
        (compacted, 'new work after Context compacted')) if breached]


def check(check_id, root, mode, config, coverage):
    # Registry IDs are recorded before any other evidence can stop the check.
    registered, invalid = entries(config, coverage)
    if invalid is not None:
        return 'FAIL', 'Invalid bound handoff registry', [invalid]
    sealed = directive()
    findings, missing = {}, []
    for entry in registered:
        path = Path(entry['path']) if Path(entry['path']).is_absolute() else root / entry['path']
        if entry['status'] == 'UNVERIFIED' or entry['source_sha256'] is None:
            missing.append(entry['id'])
            continue
        try:
            raw = path.read_bytes()
            budget = budget_breaches(path.parent / BUDGET)
        except OSError as error:
            missing.append(str(error))
            continue
        except Unverified as error:
            missing.append(str(error))
            budget = []
        else:
            if entry['id'] not in coverage['checked_registry_ids']:
                coverage['checked_registry_ids'].append(entry['id'])
        coverage['inspected'].extend([str(path), str(path.parent / BUDGET)])
        breaches = budget
        if hashlib.sha256(raw).hexdigest() != entry['source_sha256']:
            breaches = breaches + ['handoff differs from its registered digest']
        breaches = breaches + text_breaches(raw.decode('utf-8', 'replace'), sealed)
        for reason in breaches:
            item = finding(path, reason)
            findings[item['id']] = item
    if findings:
        return 'FAIL', 'Handoff context violations detected', list(findings.values())
    if missing:
        raise Unverified('; '.join(missing))
    return 'PASS', 'Handoffs carry the verbatim context directive within budget', []
