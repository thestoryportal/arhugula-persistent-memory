"""Generate v13's two run profiles and the Claude tool/Bash policy (stdlib only)."""
import json
import os
from pathlib import Path
import re
import sys


def seatbelt(config, scorer=False):
    fence = Path(config['fence'])
    runtime = [config['venv'], config['python_prefix'], config['engine'],
               config['hf_home'], *config['covariance']]
    public = ['editor_runtime.py', 'editor_bootstrap.py', 'train_facts.json']
    trusted = ['v13_common.py', 'scorer.py', 'audit_transcript.py', 'dispatch.py',
               'sandbox_settings.py', 'v13_launcher.py', 'v13_verify_gpu.py', 'v13_kill.py', 'v13_graft.py',
               'v13_cli.py', 'v13_agent_probe.py',
               'editor.sb', 'scorer.sb', '.sandbox_settings.json', 'empty_mcp.json']
    if config['fixture']:
        public += ['fixture_editor_bootstrap.py', 'fixture_editor_runtime.py']
        trusted += ['fixture_scorer.py']
    # No shell initialisation files, credential caches, home-wide or fence-wide grants.
    lines = ['(version 1)', '(allow default)', '(deny network*)', '(deny file-read*)',
             '(deny file-write*)']
    q = json.dumps
    # dyld reads the root itself; ancestor traversal needs metadata, not subtree data.
    lines.append('(allow file-read* (literal "/"))')
    metadata = set()
    for p in [*runtime, config['python'], str(fence), config['sandbox']]:
        metadata.update(str(parent) for parent in Path(p).parents)
    for p in sorted(metadata - {'/'}):
        lines.append('(allow file-read-metadata (literal ' + q(p) + '))')
    for p in ('/System', '/usr/lib', '/usr/bin', '/usr/sbin', '/bin', '/sbin',
              '/Library/Apple', '/Library/Frameworks', '/opt/homebrew/Cellar',
              '/opt/homebrew/opt', '/dev'):
        lines.append('(allow file-read* (subpath ' + q(p) + '))')
    for p in ['/etc', '/private/etc']:
        lines.append('(allow file-read* (subpath ' + q(p) + '))')
    for p in runtime:
        lines.append('(allow file-read* (subpath ' + q(p) + '))')
    for name in public + (trusted if scorer else []):
        lines.append('(allow file-read* (literal ' + q(str(fence / name)) + '))')
    if scorer:
        for name in config['graft_ignore_sha256']:
            lines.append('(allow file-read* (literal ' + q(str(Path(config['sandbox']) / name)) + '))')
        for p in [config['harness'], config['hparams'], config['fingerprint'], *config['screens']]:
            lines.append('(allow file-read* (literal ' + q(p) + '))')
        for p in [str(fence / 'sealed')]:
            lines.append('(allow file-read* (subpath ' + q(p) + '))')
    else:
        pass
    lines += ['(allow file-read* (subpath (param "RUN")))',
              '(allow file-read* (subpath (param "STAGE_TMP")))']
    # The fence deny precedes the two scorer-owned write exceptions.
    lines.append('(deny file-write* (subpath ' + q(config['fence']) + '))')
    lines += ['(allow file-write* (subpath (param "RUN")))',
              '(allow file-write* (subpath (param "STAGE_TMP")))']
    lines.append('(allow file-write* (literal "/dev/null"))')
    lines.append('(deny file-write* (regex #"/graft(/|$)"))')
    if not scorer:
        immutable = '^' + re.escape(str(Path(config['sandbox']) / 'runs')) + r'/[^/]+/edit\.py$'
        lines.append('(deny file-write* (regex ' + q(immutable) + '))')
    for p in ['/tmp', '/private/tmp', '/tmp/claude-501', '/private/tmp/claude-501']:
        lines.append('(allow file-read-metadata (literal ' + q(p) + '))')
    lines += ['(deny process-exec (literal "/usr/bin/security"))',
              '(deny file-read* (regex #"/(__pycache__/|[^/]+\\.py[co]$)"))',
              '(deny mach-lookup (global-name-regex #"^com\\.apple\\.(security|SecurityServer|secd)"))']
    for root in (config['hf_home'], str(Path(config['program']) / 'hf_cache')):
        for name in ('token', 'stored_tokens'):
            lines.append('(deny file-read* (literal ' + q(str(Path(root) / name)) + '))')
    return '\n'.join(lines) + '\n'


def settings(config):
    fence, sandbox, home = config['fence'], config['sandbox'], config['home']
    allowed = [str(Path(fence) / n) for n in ('run.sh', 'setup.sh', 'kill_run.sh', 'editor_runtime.py',
                                             'train_facts.json', 'editor.sb', 'scorer.sb',
                                             '.sandbox_settings.json', 'empty_mcp.json')]
    denied = ['/Volumes', '/Users', '/private/var/folders',
              config['program'], config['repo'], config['old_sandbox'], str(Path(fence) / 'sealed'),
              config['scorer_results'], config['editor_tmp'], config['scorer_tmp'], str(Path(sandbox) / 'graft'),
              '/private/tmp', '/tmp/claude-501', home,
              '/Volumes/memit/llm-database-project-artifacts', '/Volumes/backups', '/Volumes/Development']
    # Native CLI 2.1.292 falls back to /tmp/claude-UID above 44 bytes. A fresh,
    # short private capture child is the §4(a) fallback; probes must verify it.
    tool_deny = [config['program'], config['repo'], config['old_sandbox'],
                 str(Path(fence) / 'sealed'), config['scorer_results'], config['editor_tmp'],
                 config['scorer_tmp'], str(Path(sandbox) / 'graft'), '/tmp/claude-501', '/private/tmp/claude-501', home]
    result = {
        'sandbox': {'enabled': True, 'failIfUnavailable': True, 'allowUnsandboxedCommands': False,
                    'excludedCommands': [str(Path(fence) / n) for n in ('run.sh', 'setup.sh', 'kill_run.sh')],
                    'network': {'allowedDomains': [], 'allowLocalBinding': False,
                                'allowUnixSockets': [], 'allowAllUnixSockets': False},
                    'filesystem': {'denyRead': denied, 'allowRead': [sandbox, *allowed],
                                   'allowWrite': [sandbox, config['capture']], 'denyWrite': [config['program'], config['repo'], fence,
                                                                         '/tmp/claude-' + str(os.getuid()),
                                                                         '/private/tmp/claude-' + str(os.getuid()),
                                                                         str(Path(sandbox) / 'runs'),
                                                                         str(Path(sandbox) / 'graft'),
                                                                         str(Path(sandbox) / '.gitignore'),
                                                                         str(Path(sandbox) / '.ignore')]}},
        'permissions': {'defaultMode': 'dontAsk',
                        'allow': ['Bash(*)', 'Monitor(*)', 'TaskStop', 'Read(./**)', 'Edit(./**)', 'Write(./**)'] +
                                 ['Read(/' + p + ')' for p in allowed] +
                                 [tool + '(/' + config['capture'] + '/**)' for tool in ('Read', 'Edit', 'Write')],
                        'deny': ['Read(/' + p + '/**)' for p in tool_deny] +
                                ['Edit(/' + fence + '/**)', 'Write(/' + fence + '/**)',
                                 'Edit(./runs/**)', 'Write(./runs/**)',
                                 'Edit(.gitignore)', 'Write(.gitignore)', 'Edit(.ignore)', 'Write(.ignore)',
                                 'Edit(graft/**)', 'Write(graft/**)', 'Bash(graft *)',
                                 'Bash(chflags *)', 'Bash(/usr/bin/chflags *)', 'Bash(security *)',
                                 'Bash(/usr/bin/security *)', 'WebFetch', 'WebSearch', 'Agent', 'Task']},
        'disableAllHooks': True,
    }
    result['sandbox']['filesystem']['allowRead'] += [config['capture'], config['python_prefix']]
    return result


if __name__ == '__main__':
    config = json.loads(Path(sys.argv[1]).read_text())
    if len(sys.argv) == 3 and sys.argv[2] in ('editor', 'scorer'):
        print(seatbelt(config, sys.argv[2] == 'scorer'), end='')
    elif len(sys.argv) == 2:
        print(json.dumps(settings(config), indent=1))
    else:
        raise SystemExit('usage: sandbox_settings.py CONFIG [editor|scorer]')
