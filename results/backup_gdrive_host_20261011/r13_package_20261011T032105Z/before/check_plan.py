"""Audit command receipts and hazardous activation-plan patterns; stdlib only."""
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import sys

def writes_or_launches(line):
    argv = shlex.split(line)
    if argv[:1] == ['capture']: argv = argv[2:]
    while argv:
        executable = Path(argv[0]).name
        if executable == 'env':
            argv = argv[1:]
            while argv and ('=' in argv[0] or argv[0] == '--'): argv = argv[1:]
            continue
        if executable == 'caffeinate':
            argv = argv[1:]
            while argv and argv[0] in ('-i', '-s'): argv = argv[1:]
            continue
        if executable in ('sh', 'bash', 'python3'):
            argv = argv[1:]
            while argv and argv[0] in ('-B', '-u'): argv = argv[1:]
            if argv[:1] == ['-c']:
                return writes_or_launches(argv[1]) if executable in ('sh', 'bash') else False
            continue
        if executable == 'make_backup_candidate.sh':
            return argv[1:2] == ['create']
        if executable in ('open', 'build_gdrive_applet.sh', 'initialize_history.py'):
            return True
        if executable == 'launchctl':
            return argv[1:2] in ([x] for x in ('bootstrap','kickstart','enable','disable','bootout'))
        if executable == 'git':
            return any(x in ('fetch','merge','push') for x in argv[1:])
        return (executable == 'gh' and argv[1:3] == ['pr','create']) or (executable == 'rclone' and argv[1:2] == ['sync'])
    return False

def executable_probe(path):
    return Path(path).is_file() and os.access(path, os.X_OK)

def programs(argv):
    """Actual exec positions; filenames and Python/shell scripts are argument data."""
    if argv[:1] == ['capture']: argv = argv[2:]
    while argv:
        yield argv
        name = Path(argv[0]).name
        if name == 'env':
            argv = argv[1:]
            while argv and ('=' in argv[0] or argv[0] == '--'): argv = argv[1:]
        elif name == 'caffeinate':
            argv = argv[1:]
            while argv and argv[0] in ('-i', '-s'): argv = argv[1:]
        elif name in ('sh', 'bash') and argv[1:2] == ['-c']:
            argv = shlex.split(argv[2])
        else:
            break

def check(text, probe=None):
    probe = executable_probe if probe is None else probe
    findings = []
    marker = None
    fenced = False
    def flag(number, code, detail): findings.append(dict(line=number,code=code,detail=detail))
    for number, line in enumerate(text.splitlines(),1):
        if '<!-- row ' in line:
            match = re.search(r'marker=(READ-ONLY|RECEIPT-WRITE|OPERATOR-GO|OPERATOR-CLICK|MAESTRO-GO)',line)
            marker = match.group(1) if match else None
        if line.startswith('```'):
            fenced = not fenced if fenced or line.startswith('```bash') else False
            continue
        executable = fenced or (line.startswith('|') and '`' in line)
        if not executable: continue
        if re.search(r'(?<!\|)\|(?!\|)',line) and (fenced or re.search(r'\\\|| \| (?:grep|tail|head|shasum|diff)',line)):
            flag(number,'PIPE','pipeline can hide individual exit codes')
        if '--size-only' in line or '--hash-filter' in line:
            flag(number,'CONTENT_MODE','content hashing bypass or sampling')
        if '.venv/' in line and 'backup_gdrive_status.py' in line:
            flag(number,'INTERPRETER','status/recover must use production interpreter')
        if 'osadecompile' in line and 'grep' in line:
            flag(number,'INTEGRITY','decompile grep is not a full source comparison')
        go = marker in ('OPERATOR-GO','OPERATOR-CLICK','MAESTRO-GO') if fenced else '[OPERATOR GO]' in line
        if 'gh pr create' in line and not go: flag(number,'GITHUB_MARKER','unmarked GitHub write')
        if re.search(r'(?:generation[ -]?|counter goes to `?|counter.*reads `?)[123](?:\b|`)',line,re.I):
            flag(number,'FIXED_GENERATION','derive expectations from observed successor')
        if fenced:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'): continue
            try:
                chain = list(programs(shlex.split(stripped)))
            except ValueError as exc:
                flag(number,'EXECUTABLE_PARSE',str(exc)); continue
            for argv in chain:
                path = argv[0]
                if not path.startswith('/'):
                    flag(number,'EXECUTABLE_PATH','external program must have an absolute path: '+path)
                elif not probe(path):
                    flag(number,'EXECUTABLE','missing or non-executable external program: '+path)
                if Path(path).name == 'gh' and argv[1:3] == ['pr','create']:
                    heads = [argv[i+1] for i,a in enumerate(argv[:-1]) if a == '--head']
                    heads += [a.split('=',1)[1] for a in argv if a.startswith('--head=')]
                    if heads != ['backup-gdrive-r12']:
                        flag(number,'PR_HEAD','PR must use exactly --head backup-gdrive-r12')
                if Path(path).name == 'rclone' and argv[1:2] == ['check']:
                    formats = [argv[i+1] for i,a in enumerate(argv[:-1]) if a == '--log-format']
                    formats += [a.split('=',1)[1] for a in argv if a.startswith('--log-format=')]
                    if formats != ['date,time'] or any(a.split('=',1)[0] == '--use-json-log' for a in argv):
                        flag(number,'LOG_FORMAT','content check requires exactly --log-format date,time and no JSON override')
            if not stripped.startswith('capture '):
                flag(number,'CAPTURE','command must save stdout, stderr and its own exit code through capture')
            if marker is None: flag(number,'MARKER','command row lacks effect marker')
            if writes_or_launches(line) and not go:
                flag(number,'WRITE_MARKER','write or launch requires GO')
    return findings

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('plan',type=Path)
    findings=check(parser.parse_args().plan.read_text())
    print(('FAIL ' if findings else 'PASS ')+json.dumps(findings,indent=2))
    sys.exit(1 if findings else 0)
