"""Supplemental actual-publication audit; never used in the four-arm counts."""
import hashlib
import json
import os
from pathlib import Path
import sys
import time

run = Path(os.environ['MB28_WRITE_AUDIT_RUN']).resolve()
target = os.path.realpath(os.environ['PY39_TARGET_STATUS'])
original_replace = os.replace
def audit_replace(source, destination, *args, **kwargs):
    frame = sys._getframe(1)
    if frame.f_code.co_filename != target or frame.f_code.co_name != 'record':
        return original_replace(source, destination, *args, **kwargs)
    destination = Path(destination)
    assert str(destination.resolve()).startswith(str(run/'fixtures')+'/')
    before = destination.read_bytes() if destination.exists() else None
    after = Path(source).read_bytes()
    owner = Path(frame.f_locals['args'].log).parent/'lock/owner'
    lock_owner = owner.read_text().strip() if owner.exists() else None
    event = {'pid':os.getpid(), 'ppid':os.getppid(), 'executable':sys.executable,
             'version':sys.version, 'file':frame.f_code.co_filename,
             'line':frame.f_lineno, 'function':frame.f_code.co_name,
             'argv':sys.argv, 'destination':str(destination), 'lock_owner':lock_owner,
             'value':frame.f_locals['value'], 'before_monotonic':time.monotonic()}
    result = original_replace(source, destination, *args, **kwargs)
    event['after_monotonic'] = time.monotonic()
    event['before_sha256'] = hashlib.sha256(before).hexdigest() if before is not None else None
    event['after_sha256'] = hashlib.sha256(after).hexdigest()
    if before is not None:
        (run/('write_%s_before.bin'%os.getpid())).write_bytes(before)
    (run/('write_%s_after.bin'%os.getpid())).write_bytes(after)
    fd = os.open(str(run/'write_audit.jsonl'), os.O_WRONLY|os.O_APPEND|os.O_CREAT, 0o600)
    try:
        os.write(fd, (json.dumps(event,sort_keys=True)+'\n').encode())
    finally:
        os.close(fd)
    return result
os.replace = audit_replace
