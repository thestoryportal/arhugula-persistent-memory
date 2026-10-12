"""Build the exact candidate list for deleting duplicate copies on /Volumes/backups (read-only; deletes nothing).

A backup file qualifies only if its CURRENT bytes hash to content that is committed in git at HEAD:
  scope 'imported' = the 142 files in docs/historical_backups/20261011 (PROVENANCE.tsv),
  scope 'exact'    = audit rows final_match EXACT (byte-identical to a tracked repo file).
Every inventory path holding that content is listed, and git presence is re-checked with `git cat-file -e HEAD:<path>`.
Run from the worktree root with /usr/bin/python3 -I -B. Writes delete_candidates_20261011.tsv in the audit folder.
"""
import csv, hashlib, os, subprocess, sys

AUDIT = 'results/backups_audit_20261011T084030Z'
HIST = 'docs/historical_backups/20261011'
csv.field_size_limit(1 << 30)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def in_git_head(path):
    return subprocess.run(['git', 'cat-file', '-e', f'HEAD:{path}'], capture_output=True).returncode == 0


repo_copy = {}  # sha256 -> (scope, repo path at HEAD)
for r in csv.DictReader(open(f'{HIST}/PROVENANCE.tsv'), delimiter='\t'):
    repo_copy[r['sha256']] = ('imported', f"{HIST}/{r['file']}")
for r in csv.DictReader(open(f'{AUDIT}/program_final_dispositions.tsv'), delimiter='\t'):
    if r['final_match'] == 'EXACT' and r['sha256'] not in repo_copy:
        # counterpart names the tracked repo path; take the first path-like token that exists at HEAD
        cands = [t.strip(' `,;()') for t in r['counterpart'].replace('|', ' ').split()]
        hit = next((t for t in cands if t and in_git_head(t)), None)
        if hit and os.path.isfile(hit) and sha(hit) == r['sha256']:
            repo_copy[r['sha256']] = ('exact', hit)
        else:
            print('SKIP exact row, repo copy not verified:', r['backup_path'], file=sys.stderr)

for s, (_, p) in repo_copy.items():
    if not in_git_head(p):
        sys.exit(f'FAIL not committed at HEAD: {p}')

out = []
for r in csv.DictReader(open(f'{AUDIT}/inventory.tsv'), delimiter='\t'):
    s = r.get('sha256') or ''
    if s in repo_copy:
        p = r['path'] if r['path'].startswith('/') else os.path.join('/Volumes/backups', r['path'])
        if os.path.isfile(p) and not os.path.islink(p) and sha(p) == s:
            out.append([p, os.path.getsize(p), s, *repo_copy[s]])
        else:
            print('SKIP changed/missing/symlink:', p, file=sys.stderr)

out.sort()
with open(f'{AUDIT}/delete_candidates_20261011.tsv', 'w', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['backup_path', 'bytes', 'sha256', 'scope', 'committed_repo_copy'])
    w.writerows(out)
for sc in ('imported', 'exact'):
    sel = [o for o in out if o[3] == sc]
    print(sc, len(sel), 'files', sum(o[1] for o in sel), 'bytes')
