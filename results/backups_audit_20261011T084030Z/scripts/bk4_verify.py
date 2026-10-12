"""Independent acceptance verifier, audit-folder-only receipts, no source execution."""
import collections
import csv
import gzip
import hashlib
import json
import re
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parents[1]


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(name):
    with (OUT / name).open() as f:
        return [json.loads(line) for line in f]


start = json.loads((OUT / 'bk4_start_receipt.json').read_text())
closeout_path = OUT / 'bk4_closeout_state.json'
if closeout_path.exists():
    closeout = json.loads(closeout_path.read_text())
    with (OUT / 'progress.md').open('rb') as f:
        prefix = f.read(closeout['progress_original_bytes'])
    assert hashlib.sha256(prefix).hexdigest() == start['protected']['progress.md']
protected = {}
for name, expected in start['protected'].items():
    if name == 'progress.md':
        # The progress log is append-only rather than fully immutable.
        continue
    actual = sha(OUT / name)
    assert actual == expected, (name, actual, expected)
    protected[name] = actual
subprocess.run(['gzip', '-t', str(OUT / 'inventory.tsv.gz')], check=True)
h = hashlib.sha256()
with gzip.open(OUT / 'inventory.tsv.gz', 'rb') as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b''):
        h.update(chunk)
assert h.hexdigest() == protected['inventory.tsv']

rows = read_jsonl('program_final_dispositions.jsonl')
assert len(rows) == 298 and len({j['inventory_row'] for j in rows}) == 298
backup_hashes = []
for j in rows:
    src = Path(j['backup_path'])
    assert src.stat().st_size == j['bytes'], str(src)
    actual = sha(src)
    assert actual == j['sha256'], str(src)
    backup_hashes.append({'row': j['inventory_row'], 'path': str(src), 'bytes': j['bytes'], 'sha256': actual})
exact = read_jsonl('program_exact_receipts.jsonl') + read_jsonl('program_referral_receipts.jsonl')
grouped = collections.defaultdict(list)
for j in exact:
    grouped[j['commit']].append(j)
exact_verified = []
for commit, members in grouped.items():
    raw = subprocess.check_output(['git', 'ls-tree', '-z', commit, '--'] + [j['path'] for j in members], cwd=ROOT)
    observed = {}
    for entry in raw.split(b'\0'):
        if entry:
            prefix, path = entry.split(b'\t', 1)
            observed[path.decode()] = prefix.decode().split()[2]
    for j in members:
        assert observed.get(j['path']) == j['blob'], j
        exact_verified.append({'row': str(j.get('row', j.get('inventory_row'))), 'commit':commit,'path':j['path'],'blob':j['blob']})
assert len(exact_verified) == 100

control = json.loads((OUT / 'positive_control.json').read_text())
assert control['result'] == 'EXACT' and control['unique_fallback_calls'] == 0
assert sha(Path(control['backup_path'])) == sha(Path(control['repo_path'])) == control['sha256']
assert control['git_blob_id'] in {j['blob'] for j in exact_verified}

counts = json.loads((OUT / 'bk4_final_counts.json').read_text())
program = [j for j in rows if j['final_class'] == 'program']
assert len(program) == 294
assert dict(collections.Counter(j['final_match'] for j in program)) == counts['final_program_matches']
assert sum(counts['final_classes'].values()) == 519596
with (OUT / 'program_final_dispositions.tsv').open() as f:
    serialized = list(csv.DictReader(f, delimiter='\t'))
assert len(serialized) == 298
for a,b in zip(rows, serialized):
    assert a['inventory_row'] == b['inventory_row'] and a['sha256'] == b['sha256']

# Verify inventory row attribution without loading the large TSV in memory.
wanted = {j['inventory_row']:j for j in rows}
seen = set()
with (OUT / 'inventory.tsv').open() as f:
    for n, inv in enumerate(csv.DictReader(f, delimiter='\t'), 1):
        key = str(n)
        if key in wanted:
            j = wanted[key]
            assert inv['path'] == j['relative_backup'] and inv['sha256'] == j['sha256'] and int(inv['bytes']) == j['bytes']
            seen.add(key)
assert seen == set(wanted)

content = collections.defaultdict(list)
anchors = collections.defaultdict(list)
for j in read_jsonl('program_content_evidence.jsonl'):
    content[j['inventory_row']].append(j)
for j in read_jsonl('program_anchor_evidence.jsonl'):
    anchors[j['row']].append(j)
for j in program:
    if j['final_match'] == 'UNIQUE':
        r = j['inventory_row']
        assert content[r] and anchors[r]
        assert all(a['anchor_total'] > 0 for a in anchors[r])
        assert not any(h['normalized_identical'] for c in content[r] for h in c['hits'])
        assert not j['copies']
    assert j['recorded_loss'] == 'none'
    assert j['recommendation'] in {'import as-is','import as superseded history','reference only','ignore'}

report = (OUT / 'audit_report.md').read_text()
gap_lines = [l for l in report.splitlines() if l.startswith('| /Volumes/backups/') and '[details: program_final_dispositions.jsonl:' in l]
gaps = [j for j in program if j['gap_table']]
assert len(gap_lines) == len(gaps) == counts['gap_rows'] == 148
for line, j in zip(gap_lines, gaps):
    cells = re.split(r'(?<!\\)\|', line)[1:-1]
    assert len(cells) == 8
    cells = [s.strip().replace('\\|','|') for s in cells]
    assert cells[0] == j['backup_path'] and int(cells[1]) == j['bytes'] and cells[2] == j['sha256']
    assert cells[5] == 'none' and cells[6] == j['recommendation'] and cells[7] == j['suggested_target']
assert {j['backup_path'] for j in gaps} == {re.split(r'(?<!\\)\|', l)[1].strip() for l in gap_lines}
assert len({j['sha256'] for j in gaps}) == counts['gap_distinct_sha256'] == 146
for required in ['Coverage and final counts','Required positive control','GAP TABLE','Open questions for MAESTRO','Comparison limits','Packaging and acceptance','adjacent_groups.tsv','adjacent_dispositions.md',protected['inventory.tsv']]:
    assert required in report

# Store exact cited contexts from the current working tree / backup; no external claims checked.
citations = {
    'SESSION_CHECKPOINT.md':[1049,1051,1053],
    'EXPERIMENT_RUNBOOK.md':[85,87,89,446,991],
    'REPRODUCIBILITY.md':[7,9],
    'memory_mirror/infranodus-discourse-lens-not-coverage-tool.md':[20],
    'docs/runbooks/stage_1_sect_runbook_v1_7.md':[3,4,13,14,15,27,40,42,44,56,60,64,519],
    'docs/framework_findings/framework_finding_memit_ceiling_archival_v1_1.md':[3,4,5,6,7,8,43,45],
    '/Volumes/backups/s3-spec-writer-architecture.md':list(range(1,8))+list(range(66,74)),
    '/Volumes/backups/agent-harness-council-runbook.md':[108,137],
    '/Volumes/backups/stage_1_sect_runbook_v1_6.md':[12,44],
    'architecture_profile/runbooks/stage_1_sect_runbook_v1_5.md':[12],
}
context = []
for path, selected in citations.items():
    src = Path(path) if path.startswith('/') else ROOT / path
    found = []
    with src.open() as f:
        for n,line in enumerate(f,1):
            if n in selected:
                found.append({'line':n,'text':line.rstrip('\n')})
    assert len(found) == len(selected)
    context.append({'path':path,'sha256':sha(src),'citations':found})
assert 'LOST' in next(j for j in context if j['path']=='SESSION_CHECKPOINT.md')['citations'][-1]['text']
assert 'supersedes v1.6' in next(j for j in context if 'v1_7.md' in j['path'])['citations'][3]['text']
(OUT / 'bk4_followup_evidence.json').write_text(json.dumps(context,indent=2)+'\n')
(OUT / 'bk4_identity_verification.json').write_text(json.dumps({'backup_sources':backup_hashes,'exact_locations':exact_verified,'positive_control_reverified':True},indent=2)+'\n')

head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
branch = subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
assert branch == start['branch'] == 'worktree-c10k-route-a'
verification = dict(status='PASS', gap_rows=148, reviewed_rows=298, final_program=294,
                    source_hash_changes=0, exact_locations_verified=100, gzip_test_exit=0,
                    inventory_sha256=protected['inventory.tsv'], decompressed_sha256=h.hexdigest(),
                    protected_unchanged=protected, head_start=start['head'],head_end=head, branch=branch,
                    limitations='Comparison is bounded and MAESTRO committed concurrently; import recommendations only.')
# These two mutually describing packaging files list sizes rather than recursive hashes.
receipt = OUT / 'bk4_verification.json'
manifest = OUT / 'bk4_commit_manifest.tsv'
receipt.write_text(json.dumps(verification,indent=2)+'\n')
manifest.touch(exist_ok=True)
for _ in range(8):
    files = sorted(x for x in OUT.rglob('*') if x.is_file() and x.name != 'inventory.tsv')
    prior_sizes = {path: path.stat().st_size for path in files}
    with manifest.open('w') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['relative_path','bytes','sha256'])
        for path in files:
            w.writerow([str(path.relative_to(OUT)),prior_sizes[path],
                        'self-describing; size only' if path in {manifest,receipt} else sha(path)])
    sizes = {str(x.relative_to(OUT)): x.stat().st_size for x in files}
    assert max(sizes.values()) <= 45000000 and sum(sizes.values()) <= 200000000
    verification.update(committed_file_count=len(files), committed_total_bytes=sum(sizes.values()),
                        committed_max_file_bytes=max(sizes.values()),excluded_raw_inventory_bytes=(OUT/'inventory.tsv').stat().st_size,
                        committed_manifest='bk4_commit_manifest.tsv', committed_files=sizes)
    receipt.write_text(json.dumps(verification,indent=2)+'\n')
# Convergence check: receipt and manifest sizes must represent the actual package.
with manifest.open() as f:
    final_manifest = list(csv.DictReader(f,delimiter='\t'))
for j in final_manifest:
    assert (OUT / j['relative_path']).stat().st_size == int(j['bytes']), j
actual_total = sum(x.stat().st_size for x in OUT.rglob('*') if x.is_file() and x.name != 'inventory.tsv')
assert actual_total == verification['committed_total_bytes']
print(json.dumps({k:v for k,v in verification.items() if k not in {'committed_files','protected_unchanged'}},indent=2))
