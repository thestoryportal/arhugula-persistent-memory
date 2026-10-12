"""MAESTRO host capture guard: ROOT HOST_ATTEMPT_DIRECTORY; stdlib Python 3.9.

Compare the actual throwaway capture with saved default-server/process probes.
Use the dashboards' shared detector, and independently check event freshness
for its uncovered NEW1 runs. No tmux mutation or process launch happens here.
"""
import json
from pathlib import Path
import re
import sys
import time


def probe(receipts, name):
    code = int((receipts / (name + '.exit')).read_text().strip())
    output = (receipts / (name + '.txt')).read_text()
    return code, output


def check(root, receipts):
    sys.path.insert(0, str(root / 'tools'))
    from dashboard_live import detect_gpu_jobs

    code, capture = probe(receipts, 'tmux_capture')
    if code or not capture.strip():
        raise ValueError('Throwaway capture failed or was empty')
    code, inventory = probe(receipts, 'default_sessions')
    absent = re.fullmatch(
        r'no server running on [^\n]+|error connecting to [^\n]+ \(No such file or directory\)',
        inventory.strip())
    if code == 1 and absent:
        sessions = set()
    elif code == 0 and inventory.strip():
        sessions = set(inventory.splitlines())
    else:
        raise ValueError('Default tmux session inventory unavailable: ' + inventory.strip())

    compact = ' '.join(re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', capture).split())
    unavailable = set(re.findall(r'live session check unavailable for ([^\s:;]+)', compact))
    # Also catch Q1's diagnostic, so this guard rejects the original host defect.
    unavailable.update(re.findall(r'\(([^()\s]+)\):\s*live session check unavailable', compact))
    failed_sessions = sorted(unavailable & sessions)

    code, inventory = probe(receipts, 'experiment_inventory')
    if code or not inventory.strip():
        raise ValueError('Experiment process inventory unavailable: ' + inventory.strip())
    jobs, valid = detect_gpu_jobs(inventory)
    if not valid:
        raise ValueError('Experiment process inventory was malformed')
    live_dirs = {Path(job['run_dir']).resolve() for job in jobs if job['run_dir']}
    now = time.time()
    live_runs = {}
    for path in (root / 'results/mathlab_staging/runs').glob('*/events.jsonl'):
        lines = path.read_text().splitlines()
        events = [json.loads(line) for line in lines]
        if any(not isinstance(e, dict) or not isinstance(e.get('type'), str) for e in events):
            raise ValueError('Event type unavailable in ' + str(path))
        age = now - path.stat().st_mtime
        terminal = any(e['type'] in ('run_finished', 'terminal') for e in events)
        verified = path.parent.resolve() in live_dirs
        if events and not terminal and (verified or 0 <= age <= 10 * 60):
            live_runs[path.parent.name] = {'process_verified': verified, 'events_age_seconds': age}
    reported = set(re.findall(r'experiment run in progress:\s*([^\s(;]+)', compact))
    false_runs = sorted(reported - set(live_runs))
    print(json.dumps({'default_sessions': sorted(sessions), 'live_runs': live_runs,
                      'reported_runs': sorted(reported), 'failed_sessions': failed_sessions,
                      'false_runs': false_runs}, indent=2))
    if failed_sessions or false_runs:
        raise ValueError('Capture failed: unavailable existing sessions=%s; nonlive runs=%s' %
                         (failed_sessions, false_runs))
    print('PASS: existing sessions have no unavailable diagnostic; every reported run is live.')


if __name__ == '__main__':
    try:
        check(Path(sys.argv[1]), Path(sys.argv[2]))
    except (OSError, ValueError) as error:
        raise SystemExit('FAIL: ' + str(error))
