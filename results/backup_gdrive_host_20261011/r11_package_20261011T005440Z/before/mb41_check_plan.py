"""Audit command receipts and hazardous activation-plan patterns; stdlib only."""
import argparse
import json
from pathlib import Path
import re
import sys

def check(text):
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
            if not stripped.startswith('capture '):
                flag(number,'CAPTURE','command must save stdout, stderr and its own exit code through capture')
            if marker is None: flag(number,'MARKER','command row lacks effect marker')
            if re.search(r'(?:/usr/bin/open|launchctl (?:bootstrap|kickstart|enable|disable|bootout)|git .*?(?:fetch|merge|push)|gh pr create|rclone sync|build_gdrive_applet|initialize_history)',line) and not go:
                flag(number,'WRITE_MARKER','write or launch requires GO')
    return findings

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('plan',type=Path)
    findings=check(parser.parse_args().plan.read_text())
    print(('FAIL ' if findings else 'PASS ')+json.dumps(findings,indent=2))
    sys.exit(1 if findings else 0)
