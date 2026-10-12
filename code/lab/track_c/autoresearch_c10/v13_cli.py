"""Read-only, no-model contract for the installed native Claude CLI."""
from pathlib import Path
import re
import subprocess

from v13_common import digest

TOOLS = ('Read', 'Edit', 'Write', 'Bash', 'Monitor', 'TaskStop')
VERSION = '2.1.292'


def validate_tools(requested, supported):
    if not isinstance(requested, (list, tuple)) or not requested or len(set(requested)) != len(requested):
        raise ValueError('invalid tool allow-list')
    unknown = set(requested) - set(supported)
    if unknown:
        raise ValueError('unknown CLI tool name: ' + ','.join(sorted(unknown)))
    if set(requested) != set(TOOLS):
        raise ValueError('tool allow-list differs from the reviewed minimal set')
    return ','.join(requested)


def inspect_cli(executable):
    """Confirm real tool declarations, never asking the CLI to serve a model."""
    path = Path(executable).resolve(strict=True)
    p = subprocess.run([str(path), '--version'], text=True, capture_output=True, check=True, timeout=30)
    if p.stdout.strip() != VERSION + ' (Claude Code)':
        raise ValueError('unreviewed Claude CLI version: ' + p.stdout.strip())
    source = path.read_bytes()
    evidence = {}
    for name in TOOLS:
        pattern = rb'(?:var|,)\s*([A-Za-z_$][A-Za-z0-9_$]*)\s*=\s*"' + name.encode() + rb'"'
        symbols = [m.group(1) for m in re.finditer(pattern, source)]
        declarations = [s for s in symbols if b'name:' + s + b',' in source]
        if len(declarations) != 1:
            raise ValueError('cannot identify installed builtin tool: ' + name)
        evidence[name] = declarations[0].decode('ascii')
    validate_tools(list(evidence), evidence)
    return {'version': VERSION, 'path': str(path), 'sha256': digest(path),
            'tools': list(evidence), 'declarations': evidence}


def verify_cli(config):
    if inspect_cli(config['claude']) != config['cli_contract']:
        raise ValueError('installed CLI changed; fresh installation and probes required')
