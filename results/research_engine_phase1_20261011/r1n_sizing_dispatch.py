"""Pinned v11 in-memory adapter. CLI dispatch is prospective phase A only."""
import hashlib
import json
import os
from pathlib import Path
import sys
import types

import r1n_make_manifest_v11 as generator

HERE = Path(__file__).resolve().parent
MANIFEST_SHA256 = hashlib.sha256(generator.generated_bytes()).hexdigest()
PINS = {
    'r1l_make_bundle.py': 'c014f55e69ff9dd2483ebd92fc82d36cd760f9b6d11248f1d405dfc660b2d694',
    'r1m_size_probe.py': '93900742211b38cf6cf136eec5752b8f4958dc7782982c2999045ffac18ba029',
    'r1m_evaluate.py': 'a2338d7dec2ea03bac96edc4aa71b9864c6403a8b03b4cf2d8a5a5615c32faac',
    'r1j_collector.py': '0f71117106f639c55a3d7bc588d252a947c188218c3ee7c8f4f8698c60a5aa2d',
    'r1j_bind_manifest.py': '748bcea0c247fb3d80ccbf572641e931cbd2794600f9e1f699cc79e427f34a83',
    'r1j_stub.py': '49b4f418cb9ef0ffc13fc9c8f999c9c916a00cc8957de537975d6a6d508ccefd',
    'r1j_identity_probe.py': '83c4379281c8a7f0e5b99f6894cfc6824587333b8fd720930fa804d4fde625c8',
    generator.TARGET: MANIFEST_SHA256,
}
SSH_ARGV = ['ssh', '-T', '-i', os.path.expanduser('~/.ssh/intel_mac_ed25519'), '-o', 'IdentitiesOnly=yes',
            '-o', 'BatchMode=yes', 'robertrhu_node2@192.168.10.2']


def verify_pins():
    for name, pin in PINS.items():
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != pin:
            raise ValueError('Pin mismatch: ' + name)


def probe_member():
    # S supplies VERIFIED_MEMBERS, so Q's local v10 fallback is never entered.
    return (HERE / 'r1m_size_probe.py').read_bytes() + ('\nMANIFEST_SHA256 = ' + repr(MANIFEST_SHA256) + '\n').encode()


def maker_source():
    raw = (HERE / 'r1l_make_bundle.py').read_bytes()
    old = b'intel_provisioning_manifest_v10.json'
    if raw.count(old) != 2:
        raise ValueError('M manifest-loading sites changed')
    return raw.replace(old, generator.TARGET.encode())


def load_maker(sizing=False):
    verify_pins()
    maker = types.ModuleType('r1n_verified_maker')
    maker.__file__ = str(HERE / 'r1l_make_bundle.py')
    exec(compile(maker_source(), maker.__file__, 'exec'), maker.__dict__)
    original_build = maker.build

    def build(args):
        if sizing and args.mode != 'probe':
            raise ValueError('sizing adapter is probe-only')
        members = original_build(args)
        if sizing:
            members['identity'] = probe_member()
        return members

    # Include evidence outside J's globs in M3 admission for all v11 modes.
    def receipt_usage(manifest):
        from r1n_evaluate import local_accounting
        info = local_accounting(manifest, HERE)
        return info['matched_bytes'] + info['omitted_bytes']

    maker.build, maker.receipt_usage = build, receipt_usage
    return maker


def main(prefix):
    if not Path(prefix).name.startswith('r1j_probe_r1n_'):
        raise ValueError('new r1j_probe_r1n_<stamp> prefix required')
    maker = load_maker(sizing=True)
    sys.argv = ['r1l_make_bundle.py', 'probe', '--dispatch-m3', '--capture-prefix', prefix, '--ssh-argv', *SSH_ARGV]
    return maker.main()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: r1n_sizing_dispatch.py RE/r1j_probe_r1n_<stamp>')
    raise SystemExit(main(sys.argv[1]))
