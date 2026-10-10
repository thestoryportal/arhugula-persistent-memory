"""Program-session fresh install + plumbing probe. Never unlocks, deletes or launches a loop."""
import argparse
from pathlib import Path
import re
import sys

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))
from v13_build import build
from v13_graft import check_processes
from v13_probe import main


def destinations(tag):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,47}', tag):
        raise ValueError('tag must be a short basename, not a path')
    parent = Path('/Volumes/memit/llm-database-poc-mirror')
    return [parent / ('autoresearch_' + name + '_v13_' + tag + '_c10')
            for name in ('sandbox', 'fence', 'fixture', 'fixture_fence')]


def install_probe(tag, report, agent_probe=False):
    roots = destinations(tag)
    if any(p.exists() or p.is_symlink() for p in [*roots, Path(report)]):
        raise ValueError('all four destinations and the report must be fresh; nothing is removed or unlocked')
    if not Path(report).parent.is_dir():
        raise ValueError('report parent directory does not exist')
    # Close graft-enabled attached sessions first. Never kill another session here.
    check_processes()
    sandbox, fence, fixture, fixture_fence = roots
    build(sandbox, fence)
    build(fixture, fixture_fence, fixture=True)
    return main(fence, fixture_fence, Path(report), agent_probe=agent_probe)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tag', required=True, help='unique installation tag; change it for every rerun')
    p.add_argument('--report', type=Path, required=True, help='new report filename')
    p.add_argument('--agent-probe', action='store_true', help='explicit program-session opt-in to disposable claude -p controls')
    args = p.parse_args()
    raise SystemExit(install_probe(args.tag, args.report, args.agent_probe))
