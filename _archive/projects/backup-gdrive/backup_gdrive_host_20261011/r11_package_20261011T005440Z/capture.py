"""Run one checklist command with durable complete streams and its actual exit."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def main():
    root, label, *argv = sys.argv[1:]
    if not argv or not re.fullmatch(r'[A-Za-z0-9_.-]+', label):
        raise ValueError('expected receipt, fresh label, and command argv')
    run = Path(root)/'commands'/label
    run.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).resolve()
    (run/'command.json').write_text(json.dumps(dict(
        argv=argv, cwd=os.getcwd(), interpreter=sys.executable,
        niceness=os.getpriority(os.PRIO_PROCESS, 0),
        env={k:os.environ.get(k) for k in ('HOME','LLMDB_ROOT','BACKUP_TEST_NO_RCLONE','RCLONE_CONFIG','XDG_CONFIG_HOME')},
        source_sha256={str(source):hashlib.sha256(source.read_bytes()).hexdigest()}), indent=2)+'\n')
    with (run/'stdout.txt').open('wb') as out, (run/'stderr.txt').open('wb') as err:
        try:
            result = subprocess.run(argv, stdout=out, stderr=err)
            code = result.returncode
        except OSError as exc:
            err.write((repr(exc)+'\n').encode())
            code = 126
    (run/'exit_code.txt').write_text(str(code)+'\n')
    print('capture '+label+': exit '+str(code)+'; '+str(run), file=sys.stderr)
    return code if code >= 0 else 128-code


if __name__ == '__main__':
    sys.exit(main())
