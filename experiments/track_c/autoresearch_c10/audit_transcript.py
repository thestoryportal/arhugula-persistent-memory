"""Program-side silent copying tripwire and session-bound fail-closed watcher.

Templates are extracted by AST after checking the immutable harness, never by
importing it. Tokenisation is lowercase ASCII words, punctuation split, with
subject slots replaced by SUBJECTSLOT. No phrase-membership agent entrypoint.
"""
import ast
import json
import os
from pathlib import Path
import re
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v13_common import digest, identity, read_json, stop_stage, verify, write_json
from v13_graft import sweep


def tokens(text, subjects=()):
    text = text.lower().replace('{}', ' subjectslot ')
    for subject in sorted(subjects, key=len, reverse=True):
        text = re.sub(r'\b' + re.escape(subject.lower()) + r'\b', ' subjectslot ', text)
    return tuple(re.findall(r'[a-z0-9]+', text))


def templates(config):
    path = Path(config['harness'])
    if digest(path) != config['harness_sha256']:
        raise ValueError('audit harness changed')
    found = {}
    for n in ast.parse(path.read_text()).body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            name = n.targets[0].id
            if name in ('PTEST', 'FICTION') and name not in found:
                found[name] = ast.literal_eval(n.value)
    if len(found.get('PTEST', [])) != 3 or len(found.get('FICTION', [])) != 24:
        raise ValueError('audit stimulus shape changed')
    return found['PTEST'], found['FICTION']


def matches(text, protected, subjects):
    haystack = tokens(text, subjects)
    windows = {haystack[i:i+4] for i in range(max(0, len(haystack)-3))}
    hits = []
    for index, template in enumerate(protected):
        needle = tokens(template, subjects)
        if any(needle[i:i+4] in windows for i in range(len(needle)-3)):
            hits.append(index)
        elif len(needle) < 4 and any(haystack[i:i+len(needle)] == needle for i in range(len(haystack))):
            hits.append(index)
    return hits


def scan_bound(config, binding):
    if binding['sandbox'] != config['sandbox'] or binding['fence'] != config['fence']:
        raise ValueError('audit repository binding mismatch')
    if binding['captures'] != [config['capture'], config['editor_tmp'], config['scorer_tmp']]:
        raise ValueError('audit capture binding mismatch')
    if binding['scorer_results'] != config['scorer_results']:
        raise ValueError('audit private output binding mismatch')
    transcript = Path(binding['transcript'])
    if transcript.is_symlink() or not transcript.is_file():
        raise ValueError('bound transcript missing')
    protected, subjects = templates(config)
    records = 0
    for line in transcript.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if not isinstance(record, dict):
            raise ValueError('unparseable transcript record')
        sid = record.get('sessionId', record.get('session_id'))
        if sid is not None and sid != binding['session_id']:
            raise ValueError('transcript session mismatch')
        if matches(json.dumps(record), protected, subjects):
            raise ValueError('copying tripwire: transcript')
        records += 1
    if not records:
        raise ValueError('bound transcript empty')
    for path in sorted((Path(config['fence']) / 'sealed/archive').glob('*/edit.py')):
        meta = read_json(path.parent / 'identity.json')
        if digest(path) != meta['sha256']:
            raise ValueError('archive identity changed')
        if matches(path.read_text(), protected, subjects):
            raise ValueError('copying tripwire: archived recipe')
    return records


def stop(config, binding, detail):
    fence = Path(config['fence'])
    write_json(fence / 'sealed/STOP.json', {'status': 'HALTED', 'time': time.time(),
                                         'session_id': binding['session_id'], 'detail': detail})
    failures = []
    for name in ('editor', 'scorer', 'agent'):
        path = fence / 'sealed' / (name + '.pid.json')
        if path.exists():
            try:
                stop_stage(read_json(path), config)
            except Exception as e:
                failures.append({'stage': name, 'detail': str(e)})
    if failures:
        write_json(fence / 'sealed/stop_failures.json', failures)
    print('HALTED: program-side audit; inspect sealed/STOP.json', flush=True)


def watch(config):
    fence = Path(config['fence'])
    binding = read_json(fence / 'sealed/binding.json')
    binding['watcher_pid'] = os.getpid()
    binding['watcher_identity'] = identity(os.getpid())
    write_json(fence / 'sealed/binding.json', binding)
    while True:
        try:
            sweep(config)
            current = read_json(fence / 'sealed/binding.json')
            if current != binding:
                raise ValueError('watcher binding changed')
            records = scan_bound(config, binding)
            write_json(fence / 'sealed/heartbeat.json', {'status': 'ok', 'session_id': binding['session_id'],
                                                       'time': time.time(), 'records': records})
        except Exception as e:
            write_json(fence / 'sealed/heartbeat.json', {'status': 'failed', 'session_id': binding['session_id'],
                                                       'time': time.time()})
            stop(config, binding, type(e).__name__ + ': ' + str(e))
            return 1
        time.sleep(1)


def offline(config, seed):
    protected, subjects = templates(config)
    full = all(matches(t, protected, subjects) for t in protected)
    count, passed = 0, 0
    for t in protected:
        w = tokens(t, subjects)
        for i in range(len(w)-3):
            count += 1
            passed += bool(matches(' '.join(w[i:i+4]), protected, subjects))
    normalised = all(matches(t.format(subjects[0]), protected, subjects) for t in protected)
    # Paraphrases are explicit negative controls, not copied-template positives.
    known = ["{}'s capital is the city of", "When you travel to {}, the capital is the city of",
             "The largest city and capital of {} is the city of", "{} has a capital called"]
    blind = [not matches(t, protected, subjects) for t in known]
    clean = not matches(Path(seed).read_text(), protected, subjects)
    out = {'verbatim_templates': [full, 3], 'four_word_windows': [passed, count],
           'subject_normalisation': normalised, 'known_lookalikes_not_flagged': blind,
           'cleaned_seed_passes': clean}
    print(json.dumps(out, sort_keys=True))
    return 0 if full and passed == count and normalised and all(blind) and clean else 1


if __name__ == '__main__':
    config = verify(Path(__file__).resolve().parent, sys.argv[2])
    if sys.argv[1] == 'watch' and len(sys.argv) == 3:
        raise SystemExit(watch(config))
    if sys.argv[1] == 'offline' and len(sys.argv) == 4:
        raise SystemExit(offline(config, sys.argv[3]))
    raise SystemExit('invalid program-side audit invocation')
