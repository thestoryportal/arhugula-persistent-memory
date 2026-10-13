"""Program-session-only LAW#3 + cleaned-base verification. NEVER a no-model test."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parent))
from v13_common import digest, gpu_exclusive, identity, read_json, verify, write_json
from v13_launcher import bind, start_watcher

EXPECTED_HASHES = {
    'A1_single': '2f72fee29064643ce2214e7d644f88a71292e56c35ab657b3b3d355405cbaab1',
    'A2_coherent2': 'f94e1be2258482a84201432aec35f88c59f25e7b9d325345a447a108e0e2dd56',
    'A7_coined_coined': 'c30664a92b06be43485a2043b4512d08d977df2708289f558d5ba03a5a7da965'}
EXPECTED = {'heldout_full': 7, 'canon': 7, 'first_token': 40, 'A1': 69, 'A2': 69,
            'L1_flips': 0, 'frame_flips': 1, 'described_as': 90.38, 'L3': 30,
            'ppl_post': 21.506, 'law5_ok': True, 'scope_ok': True, 'dw_total': 88.974, 'guards': 'ok'}


def run(config):
    fence = Path(config['fence'])
    previous = set((fence / 'scorer_results').iterdir())
    p = subprocess.run([str(fence / 'run.sh')], capture_output=True, text=True, timeout=7205)
    if p.returncode != 0:
        raise ValueError('trusted dispatch failed; no guard fallback allowed')
    new = set((fence / 'scorer_results').iterdir()) - previous
    if len(new) != 1:
        raise ValueError('run identity ambiguous')
    directory = next(iter(new))
    return directory, read_json(directory / 'score.json')


def main(fence, anchor):
    config = verify(fence, anchor)
    if config['fixture']:
        raise ValueError('LAW#3 refuses a fixture')
    gpu_exclusive({os.getpid(), os.getppid()})
    target = Path(config['sandbox']) / 'edit.py'
    if digest(target) != read_json(fence / 'sealed/seed_note.json')['seed_sha256']:
        raise ValueError('seed changed before LAW#3')
    if (fence / 'sealed/law3.json').exists():
        raise ValueError('LAW#3 result already exists; do not overwrite')
    sid = str(uuid.uuid4())
    transcript = fence / 'sealed/law3_transcript.jsonl'
    transcript.write_text('{"session_id": "' + sid + '", "type": "program-law3"}\n')
    bind(config, sid, transcript, 'law3')
    binding = read_json(fence / 'sealed/binding.json')
    binding.update({'driver_pid': os.getpid(), 'driver_identity': identity(os.getpid())})
    write_json(fence / 'sealed/binding.json', binding)
    watcher = start_watcher(config, anchor)
    try:
        shutil.copyfile(fence / 'sealed/baseline_edit.py', target)
        baseline_dir, score = run(config)
        summary = score['summary']
        if any(summary.get(k) != v for k, v in EXPECTED.items()):
            raise ValueError('LAW#3 baseline metric mismatch')
        if score['saved_sha256'] != EXPECTED_HASHES or score['gates']['templates_sha'] != 'e8605172dce0':
            raise ValueError('LAW#3 bitwise payload or context-template mismatch')
        shutil.copyfile(fence / 'sealed/seed_edit.py', target)
        seed_dir, seed = run(config)
        used_fallback = False
        if seed['summary']['guards'] != 'ok':
            shutil.copyfile(fence / 'sealed/fallback_edit.py', target)
            seed_dir, seed = run(config)
            used_fallback = True
            if seed['summary']['guards'] != 'ok':
                raise ValueError('pre-registered fallback failed a guard')
        write_json(fence / 'sealed/law3.json', {'verdict': 'PASS', 'manifest_sha256': anchor,
                   'baseline_dir': str(baseline_dir), 'new_baseline_dir': str(seed_dir),
                   'new_baseline': seed['summary'], 'fallback_used': used_fallback,
                   'seed_sha256': digest(target), 'saved_sha256': score['saved_sha256'],
                   'templates_sha': score['gates']['templates_sha']})
        print('LAW#3 PASS; cleaned/fallback baseline guards ok; loop still requires no-model gates')
    finally:
        watcher.terminate()
        watcher.wait(timeout=5)


if __name__ == '__main__':
    main(Path(sys.argv[1]).resolve(), sys.argv[2])
