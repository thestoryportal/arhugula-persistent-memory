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


def read_entry(entry):
    """Read only the listed inode while it is still at the listed location."""
    link = stat.S_ISLNK(entry.st.st_mode)
    if not (link or stat.S_ISREG(entry.st.st_mode)):
        raise fdsafe.Refusal(entry.path, 'is not a regular file')
    flags = (os.O_RDONLY | os.O_SYMLINK | os.O_NONBLOCK) if link else fdsafe.LEAF_FLAGS
    with fdsafe.fs(entry.path):
        fd = os.open(entry.name, flags, dir_fd=entry.dir_fd)
    try:
        # [LAW:single-enforcer] Location and identity belong to the opened object.
        def settled():
            if fdsafe._identity(fdsafe._fstat(fd, entry.path)) != fdsafe._identity(entry.st):
                raise fdsafe.Refusal(entry.path, 'changed between scan and open/read')
            fdsafe._settled(fdsafe.Dir(fd, entry.path))
        settled()
        if link:
            with fdsafe.fs(entry.path):
                data = fdsafe._freadlink(fd, entry.st.st_size)
        else:
            parts = []
            while chunk := fdsafe._read(fd, entry.path):
                parts.append(chunk)
            data = b''.join(parts)
        settled()
        if len(data) != entry.st.st_size:
            raise fdsafe.Refusal(entry.path, f'read {len(data)} bytes, scanned {entry.st.st_size}')
        return data
    finally:
        fdsafe.close(fd, entry.path)


def write_report(parent, name, data, roots):
    """Remove this newly created report if its held parent moves into a scan root."""
    held = fdsafe.open_held(parent, name, roots)
    try:
        try:
            fdsafe.write_held(held, data)
        finally:
            # [LAW:effects-at-boundaries] Roll back only our exclusive report creation.
            where = os.path.join(parent.live(), name)
            for root in roots:
                if fdsafe.inside(root.live(), os.path.dirname(where)):
                    with fdsafe.fs(where):
                        os.unlink(name, dir_fd=parent.fd)
                    raise fdsafe.Refusal(where, f'report removed from inside root {root.path}')
        fdsafe.settle(held, roots)
    finally:
        fdsafe.close(held.fd, f'{os.path.join(parent.path, name)} (created, left in place)')


def read_text(path):
    with fdsafe.fs(path):
        parent, name = os.path.split(os.path.abspath(path))
    with fdsafe.hold_root(parent) as held:
        entry = fdsafe._scan(held, name)
        if not stat.S_ISREG(entry.st.st_mode):
            raise fdsafe.Refusal(path, 'is not a regular file')
        data = read_entry(entry)
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
        finally:
            fdsafe._settled(held)
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
            data = read_entry(entry)
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
            write_report(held, name, data, roots)
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
