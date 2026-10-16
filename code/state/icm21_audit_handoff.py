"""C-HANDOFF area: registered handoffs carry the sealed context directive and obey its budget.

Read-only. A handoff is compared, never edited. `Unverified` is injected by icm21_check.area().
"""
import hashlib
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


def directive():
    texts = [entry['text'] for entry in json.loads(VERBATIM.read_bytes())
             if entry['text'].startswith(HEADING)]
    if len(texts) != 1:
        raise Unverified('Sealed context directive is not unique in ' + str(VERBATIM))
    return texts[0]


def entries(config, coverage):
    path = Path(config['registries']['path'])
    try:
        raw = path.read_bytes()
        registry = json.loads(raw)
        found = [entry for entry in registry['reader_registry'] + registry['loader_registry']
                 if 'C-HANDOFF' in entry['check_ids']]
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise Unverified('Unreadable registry ' + str(path) + ': ' + str(error))
    coverage['inspected'].append(str(path))
    if hashlib.sha256(raw).hexdigest() != config['registries']['sha256']:
        raise Unverified('Changed bound registry: ' + str(path))
    if not found:
        raise Unverified('No registered handoff coverage')
    return found


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
    sealed = directive()
    findings, missing = {}, []
    for entry in entries(config, coverage):
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
        coverage['inspected'].extend([str(path), str(path.parent / BUDGET)])
        breaches = budget
        if hashlib.sha256(raw).hexdigest() != entry['source_sha256']:
            breaches = breaches + ['handoff differs from its registered digest']
        breaches = breaches + text_breaches(raw.decode('utf-8', 'replace'), sealed)
        for reason in breaches:
            finding_id = 'F-HANDOFF-' + hashlib.sha256(
                (str(path) + '\n' + reason).encode()).hexdigest()
            findings[finding_id] = {
                'id': finding_id, 'status': 'FAIL', 'prd_ids': ['ICM-R11'],
                'paths': [str(path)], 'evidence': [], 'reason': reason,
                'previous_finding': None, 'resolution_receipt': None}
    if findings:
        return 'FAIL', 'Handoff context violations detected', list(findings.values())
    if missing:
        raise Unverified('; '.join(missing))
    return 'PASS', 'Handoffs carry the verbatim context directive within budget', []
