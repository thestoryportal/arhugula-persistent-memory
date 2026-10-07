"""No-model fence/seed generation. Never commits, deletes, or reuses a destination."""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

SRC = Path(__file__).resolve().parent
PROGRAM = SRC.parents[2]
REPO = PROGRAM.parents[2]
OLD = Path('/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10')
sys.path.insert(0, str(SRC))
from v13_common import ARMS, digest, write_json
from sandbox_settings import seatbelt, settings
from v13_graft import seal, sweep

BASE_SHA = 'c89d80c09f2e97490ed30cda22e2a001d551e74a7df5d62585c741fc3b06abcf'
HARNESS_SHA = '1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695'
CODE = ('editor_runtime.py', 'editor_bootstrap.py', 'scorer.py', 'dispatch.py', 'v13_common.py',
        'audit_transcript.py', 'sandbox_settings.py', 'v13_launcher.py', 'v13_verify_gpu.py', 'v13_kill.py',
        'v13_graft.py')


def historical(commit):
    return subprocess.run(['/usr/bin/git', '-C', str(OLD), 'show', commit + ':edit.py'],
                          text=True, capture_output=True, check=True).stdout


def cleaned(source, canon):
    tree = ast.parse(source)
    replacements = []
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            name = n.targets[0].id
            if name in ('PROMPTS', 'DEV_PROMPT'):
                value = [canon] if name == 'PROMPTS' else canon
                replacements.append((n.lineno-1, n.end_lineno, name + ' = ' + repr(value) + '\n'))
    lines = source.splitlines(keepends=True)
    for start, end, text in reversed(replacements):
        lines[start:end] = [text]
    return ''.join(lines).replace('from prepare import', 'from editor_runtime import')


def build(sandbox, fence, fixture=False):
    sandbox, fence = Path(sandbox).absolute(), Path(fence).absolute()
    if sandbox.exists() or fence.exists():
        raise ValueError('fresh destinations required; no overwrite or deletion')
    if sandbox == fence or sandbox in fence.parents or fence in sandbox.parents:
        raise ValueError('repository and fence must be disjoint')
    harness = PROGRAM / 'experiments/track_c/c10e_bandknob.py'
    if digest(harness) != HARNESS_SHA:
        raise ValueError('harness hash changed')
    # Export only the training columns from two agreeing, already recorded harness runs.
    records = [PROGRAM / 'results/c10e_bandknob.json', PROGRAM / 'results/c10l_covgeom/run1_armB_identity.json']
    first, second = [json.loads(p.read_text())['stimulus'] for p in records]
    columns = ['CANON', 'FICTION', *['V_' + a for a in ARMS]]
    if any(first[k] != second[k] for k in columns):
        raise ValueError('recorded training stimuli disagree')
    hparams = PROGRAM / 'configs/hparams/qwen25_3b_memit_hparams.json'
    train = {'version': 13, 'program': str(PROGRAM), 'canon': first['CANON'],
             'subjects': first['FICTION'], 'arms': {a: first['V_' + a] for a in ARMS},
             'hparams': json.loads(hparams.read_text()), 'edit_budget': 2700, 'seed': 0,
             'cov_layers': list(range(4, 13)), 'model_id': 'Qwen/Qwen2.5-3B',
             'revision': '3aab1f1954e9cc14eb9509a215f9e5ca08227a9b'}
    original = historical('73f78ce')
    if hashlib.sha256(original.encode()).hexdigest() != BASE_SHA:
        raise ValueError('historical seed hash changed')
    seed = cleaned(original, train['canon'])
    fallback = cleaned(historical('92acd03'), train['canon'])
    # Sweep the generated seed before any agent-readable copy is written.
    from audit_transcript import matches, templates
    protected, subjects = templates({'harness': str(harness), 'harness_sha256': HARNESS_SHA})
    if matches(seed, protected, subjects) or matches(fallback, protected, subjects):
        raise ValueError('seed copying tripwire')
    sandbox.mkdir(parents=True)
    fence.mkdir(parents=True)
    for name in ('runs', '.agent_capture'):
        (sandbox / name).mkdir(mode=0o700)
    for name in ('sealed', 'sealed/archive', 'scorer_results', 'editor_tmp', 'scorer_tmp'):
        (fence / name).mkdir(mode=0o700, exist_ok=True)
    ignore_text = (SRC / 'gitignore.sandbox').read_text() + '\n.agent_capture/\n/graft/\n'
    ignore_files = {'.gitignore': ignore_text, '.ignore': '/graft/\n'}
    config = {'version': 13, 'fixture': fixture, 'program': str(PROGRAM), 'repo': str(REPO),
              'sandbox': str(sandbox), 'fence': str(fence), 'old_sandbox': str(OLD),
              'python': str(PROGRAM / '.venv/bin/python'), 'venv': str((PROGRAM / '.venv').resolve()),
              'python_prefix': str((PROGRAM / '.venv/bin/python').resolve().parents[1]),
              'home': str(Path.home()), 'user': os.environ.get('USER', 'robertrhu'),
              'harness': str(harness), 'harness_sha256': HARNESS_SHA, 'hparams': str(hparams),
              'fingerprint': str(PROGRAM / 'tools/engine_fingerprint.py'),
              'engine': str((PROGRAM / 'memit_dry_run/memit').resolve()),
              'hf_home': str((PROGRAM / 'hf_cache').resolve()),
              'covariance': [str((PROGRAM / 'covariance_caches').resolve()),
                             '/Volumes/memit/llm-database-poc-mirror/covariance_caches'],
              'screens': [str(PROGRAM / ('configs/screens/' + n)) for n in
                          ('g6_screen_qwen3b_v2.json', 'g6_screen_qwen3b.json')],
              'capture': str(sandbox / '.agent_capture'), 'editor_tmp': str(fence / 'editor_tmp'),
              'scorer_tmp': str(fence / 'scorer_tmp'), 'scorer_results': str(fence / 'scorer_results'),
              'claude': '/Users/robertrhu/.local/bin/claude',
              'graft_ignore_sha256': {n: hashlib.sha256(t.encode()).hexdigest()
                                      for n, t in ignore_files.items()}}
    write_json(fence / 'sealed/config.json', config)
    write_json(fence / 'train_facts.json', train)
    for name in CODE:
        shutil.copyfile(SRC / name, fence / name)
    if fixture:
        for name in ('fixture_editor_runtime.py', 'fixture_editor_bootstrap.py', 'fixture_scorer.py'):
            shutil.copyfile(SRC / name, fence / name)
    (fence / 'editor.sb').write_text(seatbelt(config))
    (fence / 'scorer.sb').write_text(seatbelt(config, True))
    write_json(fence / '.sandbox_settings.json', settings(config))
    write_json(fence / 'empty_mcp.json', {'mcpServers': {}})
    baseline = (SRC / 'edit.py').read_bytes()
    if hashlib.sha256(baseline).hexdigest() != '0d03bf68549cc8a9fb3f725850222a31ad8fc822e7df5e69e9d50cc3c4cfb0f7':
        raise ValueError('equivalence baseline is not fd16592')
    (fence / 'sealed/baseline_edit.py').write_bytes(baseline)
    (fence / 'sealed/seed_edit.py').write_text(seed)
    (fence / 'sealed/fallback_edit.py').write_text(fallback)
    (sandbox / 'edit.py').write_text(seed)
    for name, text in ignore_files.items():
        (sandbox / name).write_text(text)
    (sandbox / 'README.md').write_text('Read program.md. Use only the v13 fence wrappers. The runtime and training facts are read-only.\n')
    program = (SRC / 'program.md').read_text().replace('@FENCE@', str(fence))
    (sandbox / 'program.md').write_text(program)
    # Retain historical scores, but no old descriptions or authored prompt text.
    old_rows = (OLD / 'results.tsv').read_text().splitlines()
    rows = ['# Scores before reseal were partly test-adjacent; the new scored baseline is the reference.',
            'commit\theldout_full\tdw_total\tstatus\tdescription']
    for line in old_rows[1:]:
        cells = line.split('\t')
        if len(cells) != 5:
            raise ValueError('historical TSV shape changed')
        rows.append('\t'.join(cells[:4] + ['historical recipe; pre-reseal score']))
    (sandbox / 'results.tsv').write_text('\n'.join(rows) + '\n')
    subprocess.run(['/usr/bin/git', '-C', str(sandbox), 'init', '-q', '-b', 'autoresearch/v13'], check=True)
    # There is deliberately no commit: the operator's no-commits limit applies here too.
    for p in sandbox.rglob('*'):
        if p.is_file() and p.name != 'edit.py' and matches(p.read_text(errors='replace'), protected, subjects):
            raise ValueError('new repository copying tripwire')
    reference = json.loads(records[1].read_text())['recipes']['baseline']['arms']
    write_json(fence / 'sealed/reference_controls.json', {'recipes': {'baseline': {'arms': {
        a: {'para_full_n': reference[a]['para_full_n']} for a in ARMS[:2]}}}})
    source_knobs = {}
    for n in ast.parse(original).body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
            if n.targets[0].id in ('LAYERS', 'V_NUM_GRAD_STEPS', 'V_LR', 'CLAMP_NORM_FACTOR', 'KL_FACTOR',
                                    'V_WEIGHT_DECAY', 'RIDGE', 'NULL_THRESH', 'PRESERVE_WEIGHT', 'GAIN'):
                source_knobs[n.targets[0].id] = ast.literal_eval(n.value)
    write_json(fence / 'sealed/seed_note.json', {'commit': '73f78ce', 'original_sha256': BASE_SHA,
               'seed_sha256': digest(sandbox / 'edit.py'), 'knobs': source_knobs,
               'cleaning': 'canonical PROMPTS and DEV_PROMPT; runtime import changed',
               'training_export_sources': {str(p): digest(p) for p in records},
               'fallback_original_sha256': hashlib.sha256(historical('92acd03').encode()).hexdigest()})
    paths = [p for p in fence.rglob('*') if p.is_file()]
    paths += [sandbox / n for n in ignore_files]
    paths += [harness, hparams, Path(config['fingerprint']), *map(Path, config['screens']),
              (PROGRAM / '.venv/bin/python').resolve()]
    # Pin all vendored Python and installed Python/native helper code, including
    # interpreter startup .pth files. Weight files and covariance data are runtime inputs.
    for root in [Path(config['engine']), Path(config['venv']), Path(config['python_prefix'])]:
        paths += [p for p in root.rglob('*') if p.is_file() and
                  (p.suffix in ('.py', '.so', '.dylib', '.pth') or p.name == 'pyvenv.cfg')]
    manifest = {str(p): digest(p) for p in sorted(set(paths))}
    write_json(fence / 'sealed/manifest.json', manifest)
    anchor = digest(fence / 'sealed/manifest.json')
    for name, entry in [('run.sh', 'dispatch.py'), ('setup.sh', 'dispatch.py'), ('kill_run.sh', 'v13_kill.py')]:
        text = (SRC / name).read_text()
        for key, value in {'@PY@': config['python'], '@FENCE@': str(fence), '@ANCHOR@': anchor,
                           '@ENTRY@': entry, '@ENTRY_SHA@': digest(fence / entry),
                           '@HOME@': config['home'], '@USER@': config['user']}.items():
            text = text.replace(key, value)
        (fence / name).write_text(text)
        (fence / name).chmod(0o555)
    inventory = {str(p): digest(p) for p in fence.rglob('*') if p.is_file()}
    inventory[str(sandbox / 'edit.py')] = digest(sandbox / 'edit.py')
    inventory[str(Path(config['claude']).resolve())] = digest(Path(config['claude']).resolve())
    write_json(fence / 'sealed/root_inventory.json', inventory)
    for p in fence.rglob('*'):
        if p.is_file() and p.suffix != '.sh':
            p.chmod(0o444)
    seal(config)
    graft_check = sweep(config)
    print(json.dumps({'sandbox': str(sandbox), 'fence': str(fence), 'fixture': fixture,
                      'manifest_sha256': anchor, 'closure_files': len(manifest),
                      'seed_sha256': digest(sandbox / 'edit.py'), 'commits_created': 0,
                      'graft_check': graft_check}, sort_keys=True))
    return config, anchor


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sandbox', default='/Volumes/memit/llm-database-poc-mirror/autoresearch_v13_c10')
    parser.add_argument('--fence', default='/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_v13_c10')
    parser.add_argument('--fixture', action='store_true', help='private program-controlled no-model fence; never a loop')
    args = parser.parse_args()
    build(args.sandbox, args.fence, args.fixture)
