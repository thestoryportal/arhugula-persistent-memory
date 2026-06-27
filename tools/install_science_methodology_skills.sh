#!/usr/bin/env bash
# Install repo-local LLM-as-Database methodology skills for Codex and Claude.
set -euo pipefail
ROOT="${LLMDB_ROOT:-/workspace}"
CODEX_DEST="${CODEX_HOME:-$ROOT/.codex}/skills"
CLAUDE_DEST="${CLAUDE_SKILLS_DIR:-/root/.claude/skills}"
python3 - "$ROOT" "$CODEX_DEST" "$CLAUDE_DEST" <<'PYI'
import shutil, sys
from pathlib import Path
root=Path(sys.argv[1]); dests=[Path(sys.argv[2]), Path(sys.argv[3])]
skills=[
  'experiment-gate',
  'methodology-superpowers',
  'scientific-critical-thinking',
  'debug-mantra-scrutinize',
  'premortem-the-fool',
  'scientific-problem-selection',
]
src=root/'tools'/'skills'
for name in skills:
    source=src/name
    if not source.exists():
        raise SystemExit(f'missing {source}')
    for dest in dests:
        dest.mkdir(parents=True, exist_ok=True)
        target=dest/name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        print(f'installed {name} -> {target}')
print(f'Installed {len(skills)} repo-local science methodology skills for Codex and Claude. Restart sessions to pick them up.')
PYI

python3 - "$ROOT" <<'PYS'
import json, os, sys
from pathlib import Path
root=Path(sys.argv[1])
settings=Path(os.environ.get('CLAUDE_SETTINGS_JSON','/root/.claude/settings.json'))
settings.parent.mkdir(parents=True, exist_ok=True)
data=json.load(open(settings)) if settings.exists() else {}
hooks=data.setdefault('hooks', {})
def ensure(event, matcher, command, status, timeout):
    entries=hooks.setdefault(event, [])
    for entry in entries:
        if entry.get('matcher') == matcher:
            hs=entry.setdefault('hooks', [])
            if not any(h.get('command') == command for h in hs):
                hs.append({'type':'command','command':command,'statusMessage':status,'timeout':timeout})
            return
    entries.append({'matcher': matcher, 'hooks': [{'type':'command','command':command,'statusMessage':status,'timeout':timeout}]})
ensure('SessionStart','startup|resume|clear|compact','/usr/bin/python3 "/workspace/.codex/hooks/session_start.py"','Loading LLMDB science posture + methodology skills',90)
ensure('PreToolUse','Bash|apply_patch|Edit|Write','/usr/bin/python3 "/workspace/.codex/hooks/pre_tool_use_policy.py"','Checking LLMDB LAWs / methodology gates',15)
# Claude supports Stop entries without a matcher in current settings schema; keep matcher broad for compatibility.
ensure('Stop','*','/usr/bin/python3 "/workspace/.codex/hooks/stop_gate.py"','Checking LLMDB stop posture',90)
tmp=settings.with_suffix(settings.suffix+'.tmp')
json.dump(data, open(tmp,'w'), indent=2)
json.load(open(tmp))
os.replace(tmp, settings)
print(f'updated Claude hooks in {settings}')
PYS
