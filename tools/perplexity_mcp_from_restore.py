#!/usr/bin/env python3
"""Launch Perplexity MCP using the pod restore file without storing secrets in git."""
import json
import os
import sys
from pathlib import Path

restore = Path('/workspace/.pod_restore/mcp/servers.json')
try:
    data = json.loads(restore.read_text())
    entry = data['projects']['/root']['perplexity']
    env = os.environ.copy()
    env.update(entry.get('env', {}))
    command = entry['command']
    args = [command, *entry.get('args', [])]
except Exception as exc:
    print(f'Failed to load Perplexity MCP restore config: {exc}', file=sys.stderr)
    sys.exit(127)

os.execvpe(command, args, env)
