"""Delete the operator-approved duplicate copies on /Volumes/backups (operator: "All 241 files", 2026-10-11).

Approved list: delete_candidates_20261011.tsv, sha256 45b559f6e7f79f40d6501e9842167e44f5d573fa8c11452b388089f5c9fe5bad (commit 3017aeb2).
Per file: path under /Volumes/backups/, regular file (not symlink), current SHA-256 equals the listed one, the committed repo
copy exists at HEAD with the same SHA-256; then os.remove and confirm it is gone. Anything else is skipped and reported.
Run from the worktree root with /usr/bin/python3 -I -B. Writes delete_receipt_20261011.tsv.
"""
import csv, hashlib, os, subprocess, sys

AUDIT = 'results/backups_audit_20261011T084030Z'
LIST = f'{AUDIT}/delete_candidates_20261011.tsv'
LIST_SHA = '45b559f6e7f79f40d6501e9842167e44f5d573fa8c11452b388089f5c9fe5bad'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


if sha(LIST) != LIST_SHA:
    sys.exit('FAIL approved list changed')
rows = list(csv.DictReader(open(LIST), delimiter='\t'))
if len(rows) != 241:
    sys.exit(f'FAIL expected 241 rows, got {len(rows)}')

receipt = []
for r in rows:
    p, want, repo = r['backup_path'], r['sha256'], r['committed_repo_copy']
    ok_repo = subprocess.run(['git', 'cat-file', '-e', f'HEAD:{repo}'], capture_output=True).returncode == 0 \
        and os.path.isfile(repo) and sha(repo) == want
    if not os.path.realpath(p).startswith('/Volumes/backups/') or os.path.islink(p) or not os.path.isfile(p):
        status = 'SKIP not a regular file under /Volumes/backups'
    elif not ok_repo:
        status = 'SKIP repo copy not verified'
    elif sha(p) != want:
        status = 'SKIP content changed'
    else:
        os.remove(p)
        status = 'DELETED' if not os.path.lexists(p) else 'FAIL still present'
    receipt.append([p, r['bytes'], want, repo, status])

with open(f'{AUDIT}/delete_receipt_20261011.tsv', 'w', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['backup_path', 'bytes', 'sha256', 'committed_repo_copy', 'status'])
    w.writerows(receipt)
counts = {}
for x in receipt:
    counts[x[4]] = counts.get(x[4], 0) + 1
print(counts)
