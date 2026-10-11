"""Validate saved MAESTRO observations; no network calls or Git mutations."""
import argparse
import json
from pathlib import Path
import sys

from candidate import full_sha, verified_sha, verify_pr_head

def heads(receipt, pr_output, remote_output):
    pr = json.loads(Path(pr_output).read_text())
    if not isinstance(pr, dict): raise ValueError('invalid PR observation')
    head = full_sha(pr.get('headRefOid'))
    rows = Path(remote_output).read_text().splitlines()
    if len(rows) != 1: raise ValueError('invalid remote observation: exactly one row required')
    fields = rows[0].split('\t')
    if len(fields) != 2 or fields[1] != 'refs/heads/backup-gdrive-r12':
        raise ValueError('invalid remote observation: branch ref mismatch')
    return verify_pr_head(receipt, head, full_sha(fields[0]))

def gate(receipt, gate_output):
    sha = verified_sha(receipt); report = json.loads(Path(gate_output).read_text())
    if not isinstance(report, dict): raise ValueError('invalid gate report')
    head = full_sha(report.get('head_sha'))
    if head != sha:
        raise ValueError('gate head binding mismatch: verified='+sha+' gate='+head+'; STOP, never waive or undo merge')
    print('PASS gate report head_sha = verified commit '+sha)
    return sha

def main():
    parser = argparse.ArgumentParser(description=__doc__); sub = parser.add_subparsers(dest='mode', required=True)
    check = sub.add_parser('heads'); check.add_argument('verified_sha_file'); check.add_argument('pr_output'); check.add_argument('remote_output')
    check = sub.add_parser('gate'); check.add_argument('verified_sha_file'); check.add_argument('gate_output')
    args = parser.parse_args()
    try:
        if args.mode == 'heads': heads(args.verified_sha_file, args.pr_output, args.remote_output)
        else: gate(args.verified_sha_file, args.gate_output)
    except (OSError, ValueError) as exc:
        print('FAIL '+str(exc), file=sys.stderr); return 1
    return 0

if __name__ == '__main__': raise SystemExit(main())
