"""Read-only root reader scan (Step 408).

--root is the current repository directory; --scan-root adds outside directories.
Roots must be disjoint. The registry has no SCAN row: these arguments define the
observation scope, never an allow list. Repository keys remain relative after a
move; outside keys are absolute. Links contribute their own text, not their target.
Sockets and FIFOs are counted without opening them. All other unknown kinds refuse.

--pre-report supplies the measured_counts from an earlier pre-stage report.
--report creates one JSON file outside all scanned roots, exclusively. Stdout is
empty. Exit 0/1 is the core verdict; exit 2 is a one-line refusal on stderr.
"""
from contextlib import ExitStack
from dataclasses import asdict
import argparse
import errno
import json
import os
import stat
import sys

from ops.migrate import fdsafe, root_readers_core as core


def read_text(path):
    with fdsafe.fs(path):
        parent, name = os.path.split(os.path.abspath(path))
    with fdsafe.hold_root(parent) as held:
        data = fdsafe.read_named(held, name)
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise fdsafe.Refusal(path, 'EINVAL: expected UTF-8 metadata') from exc


def read_measured(path):
    try:
        doc = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise fdsafe.Refusal(path, 'EINVAL: expected JSON pre-report') from exc
    if not isinstance(doc, dict) or doc.get('stage') != 'pre':
        raise fdsafe.Refusal(path, 'EINVAL: expected pre-stage report')
    pairs = doc.get('measured_counts')
    if not isinstance(pairs, list):
        raise fdsafe.Refusal(path, 'EINVAL: expected measured_counts pairs')
    counts = {}
    for pair in pairs:
        if not isinstance(pair, list) or len(pair) != 2 or type(pair[0]) is not int:
            raise fdsafe.Refusal(path, 'EINVAL: expected integer-indexed count pair')
        index, count = pair
        if index in counts:
            raise fdsafe.Refusal(path, 'EINVAL: duplicate measured index')
        counts[index] = count
    return counts


def exists(path):
    with fdsafe.fs(path):
        parent, name = os.path.split(os.path.abspath(path))
    with fdsafe.hold_root(parent) as held:
        try:
            with fdsafe.fs(path):
                os.lstat(name, dir_fd=held.fd)
        except fdsafe.Refusal as exc:
            if exc.errno != errno.ENOENT:
                raise
            return False
    return True


def run(args):
    try:
        rows = core.parse_registry(read_text(args.registry))
    except fdsafe.Refusal as exc:
        raise fdsafe.Refusal(args.registry, str(exc), exc.errno) from exc
    measured = {} if args.pre_report is None else read_measured(args.pre_report)
    needle = args.old_root.encode('utf-8')
    if not needle or not os.path.isabs(args.old_root):
        raise fdsafe.Refusal(args.old_root, 'EINVAL: expected absolute old root')
    hits, counts = {}, {}
    skipped = {'fifo': 0, 'socket': 0}
    replacements = {}
    for row in rows:
        if isinstance(row, core.Replace):
            replacements.setdefault(row.path, set()).update((row.old, row.new))
    with ExitStack() as stack:
        roots = [stack.enter_context(fdsafe.hold_root(path))
                 for path in [args.root, *args.scan_root]]
        repo = roots[0].path
        for i, root in enumerate(roots):
            for previous in roots[:i]:
                if fdsafe.inside(previous.path, root.path) or fdsafe.inside(root.path, previous.path):
                    raise fdsafe.Refusal(root.path, 'EINVAL: scan roots overlap')

        def visit(entry):
            mode = entry.st.st_mode
            if stat.S_ISDIR(mode):
                return
            if stat.S_ISFIFO(mode):
                skipped['fifo'] += 1
                return
            if stat.S_ISSOCK(mode):
                skipped['socket'] += 1
                return
            fdsafe._settled(fdsafe.Dir(entry.dir_fd, os.path.dirname(entry.path)))
            # [LAW:single-enforcer] The held-fd readers own no-follow and identity checks.
            data = (fdsafe.read_link if stat.S_ISLNK(mode) else fdsafe.read_bytes)(entry)
            key = os.path.relpath(entry.path, repo) if fdsafe.inside(repo, entry.path) else entry.path
            hit_count = data.count(needle)
            if hit_count:
                hits[key] = hit_count
            for text in replacements.get(key, ()):
                counts[key, text] = data.count(text.encode('utf-8'))

        for root in roots:
            fdsafe.walk(root, visit)
            fdsafe._settled(root)
        # [LAW:one-source-of-truth] The shell observes; only classify decides the verdict.
        result = core.classify(rows=rows, stage=args.stage, hits=hits, counts=counts,
                               old_root_exists=exists(args.old_root), measured_counts=measured)
        doc = dict(asdict(result), stage=args.stage, hits=hits,
                   counts=[[path, text, count] for (path, text), count in sorted(counts.items())],
                   skipped=skipped, scan_roots=[root.path for root in roots])
        data = (json.dumps(doc, sort_keys=True, ensure_ascii=True) + '\n').encode('utf-8')
        with fdsafe.fs(args.report):
            parent, name = os.path.split(os.path.abspath(args.report))
        with fdsafe.hold_root(parent) as held:
            fdsafe.create_file(held, name, data, roots)
    return result.exit_status


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--scan-root', action='append', default=[])
    parser.add_argument('--old-root', required=True)
    parser.add_argument('--registry', required=True)
    parser.add_argument('--stage', required=True, choices=('pre', 'post'))
    parser.add_argument('--pre-report')
    parser.add_argument('--report', required=True)
    args = parser.parse_args(argv)
    try:
        return run(args)
    except fdsafe.Refusal as exc:
        print(exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
