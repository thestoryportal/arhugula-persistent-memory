"""C-MODEL area: registered model and bulk locators keep their identity under the root.

This is a locator check, not a byte check: it stats each registered path and
never opens, hashes, moves or loads a model payload. Payload byte identity is
the custody digest's job (SPEC.md:510-511), not a nightly rehash.
"""
import hashlib
import json
import os
from pathlib import Path


# `Unverified` is injected by icm21_check.area() before this module executes.
PRD_ID = 'ICM-R3'


def finding(path, reason):
    identity = str(path) + '\n' + reason
    return {'id': 'F-MODEL-' + hashlib.sha256(identity.encode()).hexdigest(),
            'status': 'FAIL', 'prd_ids': [PRD_ID], 'paths': [str(path)], 'evidence': [],
            'reason': reason, 'previous_finding': None, 'resolution_receipt': None}


def registered(config, coverage):
    """Return the C-MODEL registry entries; the registry is data, never a payload."""
    binding = config['registries']
    path = Path(binding['path'])
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise Unverified('Unobserved registry: ' + str(error)) from error
    coverage['inspected'].append(str(path))
    if hashlib.sha256(raw).hexdigest() != binding['sha256']:
        return None, [finding(path, 'changed bound source')]
    try:
        registry = json.loads(raw.decode('utf-8'))
        entries = [entry for role in ('reader', 'loader')
                   for entry in registry[role + '_registry']
                   if 'C-MODEL' in entry['check_ids']]
    except (ValueError, KeyError, TypeError) as error:
        return None, [finding(path, 'malformed registry: ' + str(error))]
    return entries, []


def locate(root, entry):
    """Return a FAIL reason, or None when the locator resolves inside the root."""
    path = root / entry['path']
    if not os.path.lexists(path):
        return 'registered locator is absent'
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        return 'locator resolves outside the canonical root: ' + str(resolved)
    if not resolved.exists():
        return 'locator target is absent: ' + str(resolved)
    return None


def check(check_id, root, mode, config, coverage):
    root = Path(root)
    entries, findings = registered(config, coverage)
    if entries is None:
        return 'FAIL', 'Model registry is not trustworthy', findings
    ids = {entry['id'] for entry in entries}
    coverage['required_registry_ids'] = sorted(set(coverage['required_registry_ids']) | ids)
    checked, missing = set(), []
    for entry in entries:
        if entry['status'] == 'UNVERIFIED' or entry['source_sha256'] is None:
            missing.append(entry['id'] + ' (' + (entry['hold_id'] or 'no hold') + ')')
            continue
        path = root / entry['path']
        try:
            reason = locate(root, entry)
        except OSError as error:
            missing.append(entry['id'] + ': ' + str(error))
            continue
        coverage['inspected'].append(str(path))
        checked.add(entry['id'])
        if reason:
            findings.append(finding(path, reason))
    coverage['checked_registry_ids'] = sorted(set(coverage['checked_registry_ids']) | checked)
    if findings:
        return 'FAIL', 'Model or bulk locator identity violated', findings
    if missing or not entries:
        return 'UNVERIFIED', '; '.join(missing) or 'No registered model locator coverage', []
    return 'PASS', 'Registered model locators resolve inside the root (locator check; no payload bytes read)', []
