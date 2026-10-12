"""Import the audit's 'import as superseded history' rows into docs/historical_backups/20261011/ (operator ruling 2026-10-11 ~09:55Z).

Run from the worktree root with /usr/bin/python3 -I -B. Copies each backup file to its suggested target, re-hashes
the copy against the audit SHA-256, and writes PROVENANCE.tsv. Refuses to overwrite an existing target.
A file named CLAUDE.md is renamed CLAUDE.historical.md so agent tools never load it as live instructions.
"""
import csv, hashlib, os, shutil, sys

AUDIT = 'results/backups_audit_20261011T084030Z'
ROOT = 'docs/historical_backups/20261011'
RENAME = {'CLAUDE.md': 'CLAUDE.historical.md'}
csv.field_size_limit(1 << 30)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


rows = [r for r in csv.DictReader(open(f'{AUDIT}/program_final_dispositions.tsv'), delimiter='\t')
        if r['recommendation'] == 'import as superseded history']
by_target = {}
for r in rows:
    d, b = os.path.split(r['suggested_target'])
    by_target.setdefault(os.path.join(d, RENAME.get(b, b)), []).append(r)

prov = []
for target, rs in sorted(by_target.items()):
    shas = {r['sha256'] for r in rs}
    if len(shas) != 1:
        sys.exit(f'FAIL conflicting content for {target}')
    want = shas.pop()
    if os.path.exists(target):
        sys.exit(f'FAIL target exists: {target}')
    src = rs[0]['backup_path']
    if sha(src) != want:
        sys.exit(f'FAIL source hash changed: {src}')
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy2(src, target)
    if sha(target) != want:
        sys.exit(f'FAIL copy hash mismatch: {target}')
    prov.append([target[len(ROOT) + 1:], want, rs[0]['bytes'], ' | '.join(r['backup_path'] for r in rs),
                 rs[0]['what_it_is'], rs[0]['counterpart'], rs[0]['final_match']])

with open(f'{ROOT}/PROVENANCE.tsv', 'w', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['file', 'sha256', 'bytes', 'backup_paths', 'what_it_is', 'newer_repo_counterpart', 'audit_match'])
    w.writerows(prov)
print(f'IMPORTED {len(prov)} files from {len(rows)} rows; all copies re-hashed OK')
