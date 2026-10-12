"""Recompute the diagnosis from raw results, bytes, and executing-writer evidence."""
import hashlib
import json
import os
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
def read(path):
    return json.loads(path.read_text())
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
pins = read(OUT/'start_sha256.json')
current = {p:digest(ROOT/p) for p in pins}
assert current == pins, 'STOP: pinned source changed'
(OUT/'end_sha256.json').write_text(json.dumps(current,indent=2)+'\n')
rows = read(OUT/'matrix_results.json')
assert len(rows) == 40
assert sum(r['testsRun'] for r in rows) == 40
assert all(r['errors']==0 and r['skipped']==0 and not r['alive'] for r in rows)
counts = {}
unpublished = 0
for arm in ['i','ii','iii','iv']:
    selected = [r for r in rows if r['arm']==arm]
    assert len(selected)==10 and {r['iteration'] for r in selected}==set(range(1,11))
    counts[arm] = {'pass':sum(r['success'] for r in selected),
                   'fail':sum(not r['success'] for r in selected)}
    for row in selected:
        run = OUT/row['run']
        runtime = read(run/'runtime.json')
        assert runtime['dont_write_bytecode']==1
        assert runtime['backup_python'] == (str(ROOT/'.venv/bin/python') if arm=='i' else '/usr/bin/python3')
        before, after = read(run/'heartbeat_before.json'), read(run/'heartbeat_after.json')
        assertion = read(run/'assertion.json')
        assert assertion['same_bytes']==row['success']
        assert before['owner_pid']==after['owner_pid']
        assert before['run_id']==after['run_id']
        assert len(assertion['refusals'])==1
        refusal = assertion['refusals'][0]
        assert refusal['owner_pid']!=after['owner_pid'] and refusal['exit_code']==75
        assert read(run/'descendants.json')['positive_control']
        assert not any(p['alive_after_runner_exit'] for p in read(run/'descendants.json')['observed'])
        log = (run/'test.log').read_text()
        assert 'Ran 1 test' in log
        if not row['success']:
            assert 'line 431' in log and 'a non-owner cannot publish over the active owner' in log
            assert before['bytes_transferred']==0 and before['rclone_pid'] is None
            assert after['bytes_transferred'] is None and after['rclone_pid']>0
            unpublished += 1
assert counts == read(OUT/'four_arm_counts.json')
audit = OUT/'write_audit_run'
events = [json.loads(line) for line in (audit/'write_audit.jsonl').read_text().splitlines()]
before_hash, after_hash = digest(audit/'heartbeat_before.json'), digest(audit/'heartbeat_after.json')
matches = [e for e in events if e['before_sha256']==before_hash and e['after_sha256']==after_hash]
assert len(matches)==1
writer = matches[0]
assert writer['line']==235 and writer['function']=='record'
assert writer['ppid']==writer['value']['owner_pid']==int(writer['lock_owner'].split()[0])
assert digest(audit/('write_%s_before.bin'%writer['pid']))==before_hash
assert digest(audit/('write_%s_after.bin'%writer['pid']))==after_hash
refused = [e for e in events if Path(e['destination']).name=='latest-refusal.json']
assert len(refused)==1 and refused[0]['value']['exit_code']==75
assert int(refused[0]['lock_owner'].split()[0])==writer['value']['owner_pid']
assert refused[0]['value']['owner_pid']!=writer['value']['owner_pid']
evidence = {'verdict':'b', 'counts':counts, 'failed_snapshots_before_child_publication':unpublished,
            'audited_writer_pid':writer['pid'], 'audited_owner_pid':writer['ppid'],
            'audited_refusal_writer_pid':refused[0]['pid'], 'audited_refused_wrapper_pid':refused[0]['ppid'],
            'writer_file':writer['file'], 'writer_line':writer['line'],
            'audited_before_sha256':before_hash, 'audited_after_sha256':after_hash,
            'analyzer_pid':os.getpid()}
(OUT/'diagnosis_evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
sources = [('tools/backup_gdrive.sh',[(40,85),(119,138)]),
           ('tools/backup_gdrive_status.py',[(200,238)]),
           ('tools/test_backup_gdrive_addendum.py',[(32,44),(252,278),(304,313),(414,438)])]
with (OUT/'source_excerpts.txt').open('w') as stream:
    for path, ranges in sources:
        lines = (ROOT/path).read_text().splitlines()
        stream.write('\n'+path+' SHA256 '+current[path]+'\n')
        for lo, hi in ranges:
            for lineno in range(lo,hi+1):
                stream.write('%s:%s: %s\n'%(path,lineno,lines[lineno-1]))
print(json.dumps(evidence,indent=2))
