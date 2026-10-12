"""Phase A of RE/r1m_gate_d_checklist.md: the RM:44-57 probe-only adapter. Q replaces only the identity member, in memory."""
import hashlib
import importlib.util
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Astra round 12 (astra_r1p12_packet.md subjects) and round 11 pins.
PINS = {
    'r1l_make_bundle.py': 'c014f55e69ff9dd2483ebd92fc82d36cd760f9b6d11248f1d405dfc660b2d694',
    'r1m_size_probe.py': '93900742211b38cf6cf136eec5752b8f4958dc7782982c2999045ffac18ba029',
    'r1j_collector.py': '0f71117106f639c55a3d7bc588d252a947c188218c3ee7c8f4f8698c60a5aa2d',
    'r1j_bind_manifest.py': '748bcea0c247fb3d80ccbf572641e931cbd2794600f9e1f699cc79e427f34a83',
    'r1j_stub.py': '49b4f418cb9ef0ffc13fc9c8f999c9c916a00cc8957de537975d6a6d508ccefd',
    'intel_provisioning_manifest_v10.json': '748fc72aa49bcdb963d99b89bbc29859237d1bbd32b84b8e05fd38d07bd9df3f',
}
SSH_ARGV = ['ssh', '-T', '-i', os.path.expanduser('~/.ssh/intel_mac_ed25519'), '-o', 'IdentitiesOnly=yes',
            '-o', 'BatchMode=yes', 'robertrhu_node2@192.168.10.2']  # W:11,28


def main(prefix):
    for name, pin in PINS.items():
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != pin:
            raise ValueError('Pin mismatch: ' + name)
    spec = importlib.util.spec_from_file_location('r1l_make_bundle', HERE / 'r1l_make_bundle.py')
    maker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(maker)
    original_build = maker.build

    def sizing_build(args):
        if args.mode != 'probe':
            raise ValueError('sizing adapter is probe-only')
        members = original_build(args)
        members['identity'] = (maker.HERE / 'r1m_size_probe.py').read_bytes()
        return members

    maker.build = sizing_build
    sys.argv = ['r1l_make_bundle.py', 'probe', '--dispatch-m3', '--capture-prefix', prefix, '--ssh-argv', *SSH_ARGV]
    return maker.main()


if __name__ == '__main__':
    if len(sys.argv) != 2 or not Path(sys.argv[1]).name.startswith('r1j_probe_r1m_'):
        raise SystemExit('usage: r1m_sizing_dispatch.py RE/r1j_probe_r1m_<stamp>')
    raise SystemExit(main(sys.argv[1]))
