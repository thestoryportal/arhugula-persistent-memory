"""C-MODEL area: registered model and bulk locators keep their identity.

This is a locator check, not a byte check: it stats each registered path and
never opens, hashes, moves or loads a model payload. Payload byte identity is
the custody digest's job (SPEC.md:510-511), not a nightly rehash.
Internal locators are relative and must resolve inside the root; external
locators are absolute (WIRE-CONTRACTS.md:58) and are checked where they are.
"""
import errno
import hashlib
import importlib.util
import json
import os
from pathlib import Path


# `Unverified` is injected by icm21_check.area() before this module executes.
PRD_ID = 'ICM-R3'
ABSENT = (errno.ENOENT, errno.ENOTDIR)


def finding(subject, path, reason):
    # Distinct registry IDs may legally share one locator path.
    identity = subject + '\n' + str(path) + '\n' + reason
    return {'id': 'F-MODEL-' + hashlib.sha256(identity.encode()).hexdigest(),
            'status': 'FAIL', 'prd_ids': [PRD_ID], 'paths': [str(path)], 'evidence': [],
            'reason': reason, 'previous_finding': None, 'resolution_receipt': None}


def contract():
    """The checker's shared wire validator, loaded by file path as area() loads this module."""
    path = Path(__file__).parent / 'icm21_check.py'
    spec = importlib.util.spec_from_file_location('icm21_check', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def registered(config, coverage):
    """Return the C-MODEL registry entries; the registry is data, never a payload."""
    checker = contract()
    binding = config['registries']
    path = Path(binding['path'])
    try:
        raw = path.read_bytes()
        schema = checker.audit_schema()
    except OSError as error:
        raise Unverified('Unobserved registry: ' + str(error)) from error
    coverage['inspected'].append(str(path))
    if hashlib.sha256(raw).hexdigest() != binding['sha256']:
        return None, [finding('registry', path, 'changed bound source')]
    try:
        registry = json.loads(raw.decode('utf-8'), parse_constant=checker.reject_constant)
        checker.validate_wire('Registries', registry, schema, {})
        for role in ('reader', 'loader'):
            checker.require(all(entry['role'] == role
                                for entry in registry[role + '_registry']),
                            'registry role mismatch')
    except (ValueError, KeyError, TypeError) as error:
        return None, [finding('registry', path, 'malformed registry: ' + str(error))]
    entries = [entry for role in ('reader', 'loader')
               for entry in registry[role + '_registry']
               if 'C-MODEL' in entry['check_ids']]
    return entries, []


def locate(root, entry):
    """Return a FAIL reason or None; raise OSError when the locator is unobserved."""
    path = root / entry['path']
    try:
        os.lstat(path)
    except OSError as error:
        if error.errno in ABSENT:
            return 'registered locator is absent'
        raise
    try:
        resolved = Path(os.path.realpath(path, strict=True))
    except OSError as error:
        if error.errno == errno.ELOOP:
            return 'locator is a symlink loop'
        if error.errno in ABSENT:
            return 'locator target is absent'
        raise
    if Path(entry['path']).is_absolute():
        return None
    if not resolved.is_relative_to(os.path.realpath(root, strict=True)):
        return 'locator resolves outside the canonical root: ' + str(resolved)
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
            findings.append(finding(entry['id'], path, reason))
    coverage['checked_registry_ids'] = sorted(set(coverage['checked_registry_ids']) | checked)
    if findings:
        return 'FAIL', 'Model or bulk locator identity violated', findings
    if missing or not entries:
        return 'UNVERIFIED', '; '.join(missing) or 'No registered model locator coverage', []
    return 'PASS', ('Registered model locators resolve; internal ones inside the root'
                    ' (locator check; no payload bytes read)'), []
