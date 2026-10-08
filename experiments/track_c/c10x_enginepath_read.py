"""Fail-closed C10X reader; scientific predicates are frozen prereg §3.

The pure classifier accepts synthetic records. File admission requires complete
scientific evidence, companion records, current source identity and full-logit
audits. No path reads telemetry or repairs a recorded value.
"""
import argparse
import copy
from datetime import datetime
import hashlib
import json
import math
import pickle
from pathlib import Path

PREREG_SHA256 = '43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883'
CANON = 'The capital of {} is the city of'
ENGINE_SHA256 = 'd941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65'
ARMS = ('A1_single', 'A2_coherent2', 'A7_coined_coined')
CANDIDATES = ('I-2', 'I-1')
RECIPES = ('A',) + CANDIDATES
LAYERS = {str(l) for l in range(4, 9)}
CHECKS = ('G8', 'X1-i', 'X1-ii', 'X1-iii', 'X1-iv', 'X1-v',
          'X2-ii', 'X2-iii', 'X2-iv', 'X2-v', 'X2-vi', 'X2-vii')
REQUIRED = ('schema', 'status', 'process', 'run_id', 'pid', 'started_at', 'finished_at',
            'source_commit', 'prereg_sha256', 'sources_start', 'sources_end',
            'fingerprint', 'identity', 'ctx', 'ctx_sha256', 'frames', 'frames_sha256',
            'base_report', 'w0', 'inertness', 'counters', 'recipes', 'targets',
            'inject', 'timings', 'telemetry', 'telemetry_inertness', 'audits')
MANIFEST = ('schema', 'process', 'run_id', 'pid', 'source_commit', 'prereg_sha256',
            'sources_start', 'sources_end', 'fingerprint', 'identity', 'ctx',
            'ctx_sha256', 'frames', 'frames_sha256', 'started_at', 'finished_at',
            'w0', 'counters', 'target_hashes', 'audits', 'reviewer', 'provenance', 'context_source')


def _need(ok, message):
    if not ok:
        raise ValueError(message)


def _dict(value, keys, name, exact=False):
    _need(type(value) is dict, name + ' must be an object')
    missing = set(keys) - set(value)
    _need(not missing, name + ' missing ' + ','.join(sorted(missing)))
    if exact:
        _need(set(value) == set(keys), name + ' has unexpected keys')
    return value


def _int(value, name, low=0, high=None):
    _need(type(value) is int and value >= low and (high is None or value <= high),
          name + ' has an invalid integer count')
    return value


def _num(value, name, low=None, high=None):
    _need(type(value) in (int, float) and math.isfinite(value), name + ' must be finite')
    _need((low is None or value >= low) and (high is None or value <= high),
          name + ' is outside its domain')
    return value


def _str(value, name):
    _need(type(value) is str and bool(value), name + ' must be a nonempty string')
    return value


def _sha(value, name):
    _need(type(value) is str and len(value) == 64 and
          all(c in '0123456789abcdef' for c in value), name + ' must be SHA-256')


def _hashes(value, name, keys=None):
    _dict(value, keys or (), name, exact=keys is not None)
    _need(bool(value), name + ' is empty')
    for key, sha in value.items():
        _str(key, name + '.key')
        _sha(sha, name + '.' + key)


def _finite_tree(value, path='record'):
    if type(value) is dict:
        for key, child in value.items():
            _need(type(key) is str, path + ' has a non-string key')
            _finite_tree(child, path + '.' + key)
    elif type(value) is list:
        for i, child in enumerate(value):
            _finite_tree(child, path + '[' + str(i) + ']')
    elif type(value) is float:
        _need(math.isfinite(value), path + ' is non-finite')
    else:
        _need(value is None or type(value) in (str, bool, int), path + ' is not JSON data')


def strict_json(data):
    """Reject duplicate members, JSON constants and overflowing floats."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError('non-finite JSON constant: ' + value)
    result = json.loads(data, object_pairs_hook=pairs, parse_constant=constant)
    _finite_tree(result, 'json')
    return result


def _nulls(value, path=()):
    if value is None:
        location = path[1:] if path and path[0] == 'manifest' else path
        diagnostic = (len(location) == 5 and location[0] == 'recipes' and
                      location[1] in RECIPES and location[2] == 'arms' and
                      location[3] in ARMS and location[4] in {'tf_pertok_cont',
                      'cond_full_given_first', 'tf_pertok_cont_reason',
                      'cond_full_given_first_reason'})
        _need(location == ('telemetry_inertness',) or diagnostic,
              'unexpected null at ' + '.'.join(map(str, path)))
    elif type(value) is dict:
        for key, child in value.items():
            _nulls(child, path + (key,))
    elif type(value) is list:
        for index, child in enumerate(value):
            _nulls(child, path + (index,))


def _flags(value, name):
    _need(type(value) is list and len(value) == 3 and
          all(type(x) is bool for x in value), name + ' requires three booleans')
    return value


def _arm(summary, rows, name):
    fields = ('canon_full_n', 'canon_n', 'para_full_n', 'para_n', 'para_first_n',
              'para_string_n', 'tf_pertok_cont', 'tf_continuation_n',
              'cond_full_given_first', 'cond_full_given_first_reason',
              'tf_pertok_cont_reason', 'per_fact', 'per_template',
              'locality_described_as', 'locality_axes', 'extra')
    _dict(summary, fields, name)
    _need(type(rows) is list and len(rows) == 24, name + ' needs 24 detail rows')
    _need(summary['canon_n'] == 24 and type(summary['canon_n']) is int,
          name + ' canonical denominator is not 24')
    _need(summary['para_n'] == 72 and type(summary['para_n']) is int,
          name + ' paraphrase denominator is not 72')
    subjects = []
    for index, row in enumerate(rows):
        where = name + '.detail[' + str(index) + ']'
        _dict(row, ('subj', 'val', 'ntok', 'canon_full', 'canon_first',
                   'para_full_hits', 'para_first_hits', 'para_string_hits',
                   'tf_correct', 'tf_total'), where)
        subjects.append(_str(row['subj'], where + '.subj'))
        _str(row['val'], where + '.val')
        ntok = _int(row['ntok'], where + '.ntok', 1)
        for key in ('canon_full', 'canon_first'):
            _need(type(row[key]) is bool, where + '.' + key + ' is not boolean')
        for key in ('para_full_hits', 'para_first_hits', 'para_string_hits'):
            _flags(row[key], where + '.' + key)
        _need(not row['canon_full'] or row['canon_first'], where + ' full without first')
        _need(all(not f or p for f, p in zip(row['para_full_hits'], row['para_first_hits'])),
              where + ' paraphrase full without first')
        total = _int(row['tf_total'], where + '.tf_total')
        _need(total == 3 * (ntok - 1), where + ' teacher-forced denominator mismatch')
        _int(row['tf_correct'], where + '.tf_correct', high=total)
    _need(len(set(subjects)) == 24, name + ' duplicates a subject')
    totals = {'canon_full_n': sum(r['canon_full'] for r in rows),
              'para_full_n': sum(sum(r['para_full_hits']) for r in rows),
              'para_first_n': sum(sum(r['para_first_hits']) for r in rows),
              'para_string_n': sum(sum(r['para_string_hits']) for r in rows)}
    for key, actual in totals.items():
        _int(summary[key], name + '.' + key, high=24 if key == 'canon_full_n' else 72)
        _need(summary[key] == actual, name + '.' + key + ' disagrees with flags')
    _need(summary['para_string_n'] >= summary['para_full_n'], name + ' string < full')
    per_fact = [sum(r['para_full_hits']) for r in rows]
    per_template = [sum(r['para_full_hits'][k] for r in rows) for k in range(3)]
    for key, expected in (('per_fact', per_fact), ('per_template', per_template)):
        _need(type(summary[key]) is list and all(type(x) is int for x in summary[key]) and
              summary[key] == expected, name + '.' + key + ' disagrees with flags')
    if 'per_edge' in summary:
        _need(type(summary['per_edge']) is list and
              summary['per_edge'] == [x == 3 for x in per_fact] and
              all(type(x) is bool for x in summary['per_edge']), name + ' invalid 3/3 rule')
    tf_n = sum(r['tf_total'] for r in rows)
    _int(summary['tf_continuation_n'], name + '.tf_continuation_n')
    _need(summary['tf_continuation_n'] == tf_n, name + ' continuation denominator mismatch')
    first_n = totals['para_first_n']
    for key, denom, expected in (
            ('tf_pertok_cont', tf_n, round(100 * sum(r['tf_correct'] for r in rows) / tf_n, 1) if tf_n else None),
            ('cond_full_given_first', first_n, round(totals['para_full_n'] / first_n, 3) if first_n else None)):
        reason = summary[key + '_reason']
        if denom == 0:
            _need(summary[key] is None and reason == 'zero denominator',
                  name + '.' + key + ' lacks its zero-denominator null/reason')
        else:
            _num(summary[key], name + '.' + key)
            _need(summary[key] == expected and reason is None,
                  name + '.' + key + ' disagrees with its recorded denominator')
    _num(summary['locality_described_as'], name + '.locality_described_as', 0, 100)
    axes = _dict(summary['locality_axes'], ('L1_flipped_to_edited_value', 'L1_n',
                 'L3_top1_agree', 'L3_n', 'generic_ppl_post'), name + '.locality_axes')
    _need(axes['L1_n'] == 12 and type(axes['L1_n']) is int and
          axes['L3_n'] == 30 and type(axes['L3_n']) is int, name + ' locality denominators')
    _int(axes['L1_flipped_to_edited_value'], name + '.L1', high=12)
    _int(axes['L3_top1_agree'], name + '.L3', high=30)
    _num(axes['generic_ppl_post'], name + '.perplexity', 0)
    _dict(summary['extra'], (), name + '.extra')


def _recipe(recipe, name):
    _dict(recipe, ('law5_gate', 'arms', 'detail', 'delta_norms', 'write_norms_float64'), name)
    gate = _dict(recipe['law5_gate'], ('ok', 'expr_delta', 'loc_delta'), name + '.G')
    _num(gate['expr_delta'], name + '.G.expr_delta')
    _num(gate['loc_delta'], name + '.G.loc_delta')
    _need(gate['ok'] is True and abs(round(gate['expr_delta'], 4)) < .05 and
          abs(round(gate['loc_delta'], 2)) < 3, name + ' G is not INERT')
    if 'candidate_calls' in gate:
        _need(type(gate['candidate_calls']) is int and gate['candidate_calls'] == 0,
              name + ' candidate seam ran during G')
    for section in ('arms', 'detail', 'delta_norms', 'write_norms_float64'):
        _dict(recipe[section], ARMS, name + '.' + section, exact=True)
    for arm in ARMS:
        _arm(recipe['arms'][arm], recipe['detail'][arm], name + '.' + arm)
        norms = _dict(recipe['write_norms_float64'][arm], LAYERS, name + '.norms.' + arm, exact=True)
        legacy = _dict(recipe['delta_norms'][arm], LAYERS, name + '.delta_norms.' + arm, exact=True)
        for layer in sorted(LAYERS):
            _num(norms[layer], name + '.norm.' + layer, 0)
            _dict(legacy[layer], ('delta_norm', 'weight_norm_before', 'relative_delta_norm'),
                  name + '.delta_norm.' + layer)
            for key in ('delta_norm', 'weight_norm_before', 'relative_delta_norm'):
                _num(legacy[layer][key], name + '.delta_norm.' + key, 0)


def law3(recipe):
    """Prereg :132 predicate, including exact recorded denominators/flags."""
    try:
        _finite_tree(recipe)
        _dict(recipe, ('arms', 'detail'), 'baseline')
        for arm in ARMS:
            _arm(recipe['arms'][arm], recipe['detail'][arm], 'baseline.' + arm)
        a = recipe['arms'][ARMS[2]]
        return (5 <= a['para_full_n'] <= 18 and 5 <= a['canon_full_n'] <= 10 and
                42 <= a['para_first_n'] <= 59 and
                all(recipe['arms'][arm]['para_full_n'] >= 68 for arm in ARMS[:2]))
    except (KeyError, TypeError, ValueError, OverflowError):
        return False


def _validate(record):
    _dict(record, REQUIRED, 'record')
    _finite_tree(record)
    _nulls(record)
    _need(record['schema'] == 'c10x_enginepath/v1' and record['status'] == 'COMPLETE',
          'record is not a complete C10X process')
    _int(record['process'], 'process', 1, 2)
    _int(record['pid'], 'pid', 1)
    for key in ('run_id', 'source_commit'):
        _str(record[key], key)
    times = []
    for key in ('started_at', 'finished_at'):
        stamp = datetime.fromisoformat(_str(record[key], key).replace('Z', '+00:00'))
        _need(stamp.tzinfo is not None, key + ' lacks timezone')
        times.append(stamp)
    _need(times[1] >= times[0], 'finish precedes start')
    _need(record['prereg_sha256'] == PREREG_SHA256, 'frozen prereg hash mismatch')
    for key in ('sources_start', 'sources_end'):
        _hashes(record[key], key)
    _need(record['sources_start'] == record['sources_end'], 'source drift between start/end')
    fingerprint = _dict(record['fingerprint'], ('ok', 'sha256', '_cov_cpu'), 'fingerprint')
    _need(fingerprint['ok'] is True and fingerprint['sha256'] == ENGINE_SHA256 and
          type(fingerprint['_cov_cpu']) is int and fingerprint['_cov_cpu'] == 3,
          'fingerprint or _cov_cpu failure')
    identity = _dict(record['identity'], ('model', 'model_rev', 'tokenizer', 'software',
                     'device', 'dtype', 'hparams', 'covariance', 'stimuli', 'settings', 'weights'), 'identity')
    for key in ('model', 'model_rev', 'device', 'dtype'):
        _str(identity[key], 'identity.' + key)
    _hashes(identity['tokenizer'], 'tokenizer')
    _hashes(identity['covariance'], 'covariance')
    _hashes(identity['weights'], 'weights', LAYERS)
    _sha(identity['hparams'], 'hparams')
    _dict(identity['software'], (), 'software')
    _need(bool(identity['software']), 'software identity is empty')
    _need(identity['settings'] == {'lam': .1, 'eps': .01, 'n_sigma': .5}, 'OverTone settings changed')
    _dict(identity['stimuli'], ARMS, 'stimuli', exact=True)
    for arm in ARMS:
        _need(type(identity['stimuli'][arm]) is list and len(identity['stimuli'][arm]) == 24,
              'ordered stimuli must contain 24 items for ' + arm)
    _need(type(record['ctx']) is list and bool(record['ctx']) and
          all(type(g) is list and bool(g) and all(type(c) is str and '{}' in c for c in g)
              for g in record['ctx']), 'invalid context-template list')
    for key in ('ctx_sha256', 'frames_sha256'):
        _sha(record[key], key)
    frames = record['frames']
    _need(type(frames) is list and bool(frames) and all(type(x) is str and x for x in frames) and
          len(set(frames)) == len(frames), 'invalid realised frames')
    _dict(record['base_report'], ARMS, 'base_report', exact=True)
    for arm in ARMS:
        report = _dict(record['base_report'][arm], ('base',), 'base_report.' + arm)
        _int(report['base'], 'base_report.' + arm + '.base', high=24)
        _need(report['base'] <= 3, 'stimulus leak exceeds 3/24 in ' + arm)
    w0 = _dict(record['w0'], ('hashes', 'checkpoints'), 'W0')
    _hashes(w0['hashes'], 'W0.hashes', LAYERS)
    _need(w0['hashes'] == identity['weights'], 'W0 differs from weight identity')
    _need(type(w0['checkpoints']) is list and bool(w0['checkpoints']), 'W0 checkpoints missing')
    for checkpoint in w0['checkpoints']:
        _dict(checkpoint, ('ok',), 'W0 checkpoint')
        _need(checkpoint['ok'] is True, 'W0 checkpoint failed')
        if 'hashes' in checkpoint:
            _need(checkpoint['hashes'] == w0['hashes'], 'W0 checkpoint hash mismatch')
    _dict(record['inertness'], CHECKS, 'inertness', exact=True)
    for check in CHECKS:
        result = _dict(record['inertness'][check], ('ok',), check)
        _need(result['ok'] is True, check + ' failed or lacks an exact pass boolean')
        if check in ('X1-i', 'X2-ii', 'X2-iv'):
            _dict(result, ('floor',), check)
        if 'floor' in result:
            _num(result['floor'], check + '.floor', 0, 1e-5)
        if 'rel' in result:
            _num(result['rel'], check + '.rel', 0, 1e-4)
        if 'tol' in result:
            _need(result['tol'] == 1e-4, check + ' tolerance widened')
        if check == 'X1-ii' and ('steps_reference' in result or 'steps_candidate' in result):
            _need(result.get('steps_reference') == result.get('steps_candidate'),
                  'X1-ii step counts differ')
    _dict(record['counters'], RECIPES, 'counters', exact=True)
    for name, pair in zip(RECIPES, ([0, 0], [0, 3], [3, 0])):
        _need(type(record['counters'][name]) is list and
              all(type(x) is int for x in record['counters'][name]) and
              record['counters'][name] == pair, name + ' counter mismatch')
    _dict(record['recipes'], RECIPES, 'recipes', exact=True)
    for name in RECIPES:
        recipe = record['recipes'][name]
        _recipe(recipe, name)
        for arm in ARMS:
            rows = recipe['detail'][arm]
            stimuli = identity['stimuli'][arm]
            if all(type(x) is str for x in stimuli):
                _need([r['subj'] for r in rows] == stimuli, name + ' ordered subjects mismatch')
            elif all(type(x) is dict and set(x) >= {'subj', 'val'} for x in stimuli):
                _need([(r['subj'], r['val']) for r in rows] ==
                      [(s['subj'], s['val']) for s in stimuli], name + ' ordered stimuli mismatch')
            else:
                raise ValueError('malformed ordered stimuli for ' + arm)
        realised = _dict(recipe['arms'][ARMS[2]]['extra'], ('frames',), name + '.A7.extra')['frames']
        _dict(realised, frames, name + '.frames', exact=True)
        for frame, count in realised.items():
            _dict(count, ('flips', 'n'), name + '.frame.' + frame)
            _need(type(count['n']) is int and count['n'] == 6, name + ' frame denominator is not 6')
            _int(count['flips'], name + '.frame.flips', high=6)
    _need(law3(record['recipes']['A']), 'LAW#3 baseline envelope failed')
    _dict(record['targets'], ('engine8', 'engine4', 'overtone'), 'targets', exact=True)
    for name, target in record['targets'].items():
        _dict(target, ('sha256',), 'targets.' + name)
        _sha(target['sha256'], 'targets.' + name + '.sha256')
    fit = record['targets']['engine4'].get('a7_fit')
    _need(type(fit) is list and len(fit) == 24, 'engine4 fit screen needs 24 A7 targets')
    for value in fit:
        _num(value, 'engine4.a7_fit', 0, 1)
    _dict(record['inject'], ('reference',) + CANDIDATES, 'inject')
    for key in ('reference',) + CANDIDATES:
        _int(record['inject'][key], 'inject.' + key, high=72)
    _dict(record['timings'], (), 'timings')
    _dict(record['audits'], ('sha256',), 'audits')
    _sha(record['audits']['sha256'], 'audits.sha256')
    _need(type(record['telemetry']) is bool, 'telemetry is not boolean')
    if record['telemetry']:
        admission = _dict(record['telemetry_inertness'], ('path', 'sha256'), 'telemetry_inertness', exact=True)
        _need(Path(_str(admission['path'], 'telemetry admission path')).is_absolute(),
              'telemetry admission path is relative')
        _sha(admission['sha256'], 'telemetry admission hash')
    else:
        _need(record['telemetry_inertness'] is None, 'off launch has telemetry admission data')
    baseline_norm = sum(record['recipes']['A']['write_norms_float64'][ARMS[2]][str(l)]
                        for l in range(4, 9))
    _num(baseline_norm, 'baseline write norm')
    _need(baseline_norm > 0, 'write-size qualifier has zero baseline denominator')


def _locality(baseline, candidate, frames):
    a, c = baseline['locality_axes'], candidate['locality_axes']
    failed = []
    if c['L1_flipped_to_edited_value'] > a['L1_flipped_to_edited_value'] + 1:
        failed.append('L1')
    for frame in frames:
        if candidate['extra']['frames'][frame]['flips'] > baseline['extra']['frames'][frame]['flips'] + 1:
            failed.append('frame:' + frame)
    if candidate['locality_described_as'] < baseline['locality_described_as'] - 3:
        failed.append('described_as')
    if c['L3_top1_agree'] < 29:
        failed.append('L3')
    if c['generic_ppl_post'] > a['generic_ppl_post'] + .5:
        failed.append('generic_perplexity')
    return failed


def _null_row(arm, deficit):
    if arm == 'I-2':
        return 'TARGET-WEAKER' if deficit >= 10 else 'INTERMEDIATE' if deficit >= 6 else 'NO-DEFICIT'
    return 'WEAKER' if deficit >= 6 else 'STRONGER' if deficit <= -6 else 'NON-INTERPRETED'


def _interpret(base, qualifiers, replicated=False):
    if base == 'INVALID-CONTROLS':
        return 2
    if '-LARGE-WRITE' in qualifiers or base == 'TRADEOFF':
        return 3
    if '-UNDERFIT' in qualifiers:
        return 4
    if base in ('LEAD', 'PARTIAL'):
        return 5 if replicated else 6
    return 7


def _invalid(errors):
    return {'status': 'INVALID', 'errors': errors, 'arms': {}, 'replication_eligible': []}


def read_record(record):
    try:
        _validate(record)
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        return _invalid([str(exc)])
    baseline = record['recipes']['A']['arms'][ARMS[2]]
    a_count = baseline['para_full_n']
    baseline_norm = sum(record['recipes']['A']['write_norms_float64'][ARMS[2]][str(l)]
                        for l in range(4, 9))
    result = {'status': 'VALID', 'errors': [], 'arms': {}, 'replication_eligible': []}
    for name in CANDIDATES:
        recipe = record['recipes'][name]
        candidate = recipe['arms'][ARMS[2]]
        count = candidate['para_full_n']
        failed = _locality(baseline, candidate, record['frames'])
        lead = count >= 30
        partial = 18 < count < 30 and count - a_count >= 10
        controls = all(recipe['arms'][arm]['para_full_n'] >= 68 for arm in ARMS[:2])
        base = ('INVALID-CONTROLS' if not controls else 'TRADEOFF' if (lead or partial) and failed
                else 'LEAD' if lead else 'PARTIAL' if partial else 'NULL')
        norms = sum(recipe['write_norms_float64'][ARMS[2]][str(l)] for l in range(4, 9))
        ratio = norms / baseline_norm
        if not math.isfinite(ratio):
            return _invalid([name + ' write ratio is not finite'])
        qualifiers = []
        if base != 'INVALID-CONTROLS':
            if base == 'NULL' and count <= a_count - 10:
                qualifiers.append('-BELOW-BASELINE')
            if ratio > 1.5:
                qualifiers.append('-LARGE-WRITE')
            if name == 'I-2' and sum(x >= .98 for x in record['targets']['engine4']['a7_fit']) < 22:
                qualifiers.append('-UNDERFIT')
        eligible = base in ('LEAD', 'PARTIAL') and not any(
            q in qualifiers for q in ('-LARGE-WRITE', '-UNDERFIT'))
        deficit = record['inject']['reference'] - record['inject'][name]
        label_base = 'NULL-TARGET-WEAKER' if name == 'I-2' and base == 'NULL' and deficit >= 10 else base
        result['arms'][name] = {'base': base, 'label': label_base + ''.join(qualifiers),
            'qualifiers': qualifiers, 'eligible': eligible,
            'null_row': _null_row(name, deficit) if base == 'NULL' else None,
            'interpretation_row': _interpret(base, qualifiers), 'failed_locality': failed,
            'count': count, 'baseline_count': a_count, 'write_ratio': ratio}
        if eligible:
            result['replication_eligible'].append(name)
    return result


def combine(first, second):
    """Amendment P4: fixed-template regeneration, then per-candidate replication."""
    _need(first is not second, 'same record reused as replication')
    _dict(first, ('process', 'pid', 'run_id', 'identity'), 'process 1')
    _dict(second, ('process', 'pid', 'run_id', 'identity'), 'process 2')
    _need(type(first['process']) is int and first['process'] == 1 and
          type(second['process']) is int and second['process'] == 2, 'process identities are not 1/2')
    _need(first['run_id'] != second['run_id'] and first['pid'] != second['pid'],
          'same process reused as replication')
    if '_out_dir' in first and '_out_dir' in second:
        _need(first['_out_dir'] != second['_out_dir'], 'same directory reused as replication')
    for key in ('identity', 'source_commit', 'sources_start', 'sources_end',
                'prereg_sha256', 'telemetry', 'telemetry_inertness',
                'ctx', 'ctx_sha256', 'frames', 'frames_sha256'):
        _need(key in first and key in second and first[key] == second[key],
              'replication identity mismatch: ' + key)
    from c10x_enginepath_arms import recorded_contexts
    ctx,_=recorded_contexts()
    frames=[c.format(CANON) for group in ctx for c in group]
    _need(first['ctx']==ctx and first['ctx_sha256']==_json_sha(ctx) and
          first['frames']==frames and first['frames_sha256']==_json_sha(frames),
          'replication contexts or frames differ from Amendment P pin')
    p1, p2 = read_record(first), read_record(second)
    if p1['status'] != 'VALID':
        return p1
    _need(bool(p1['replication_eligible']), 'process 1 has no replication-eligible arm')
    result = copy.deepcopy(p1)
    result['processes'] = {'1': p1, '2': p2}
    result['replication_eligible'] = []
    for name in CANDIDATES:
        arm = result['arms'][name]
        arm['replicated'] = False
        other = p2['arms'].get(name) if p2['status'] == 'VALID' else None
        if not arm['eligible']:
            arm['eligible'] = False
            continue
        if other is not None and other['eligible']:
            replicated = 'LEAD' if arm['base'] == other['base'] == 'LEAD' else 'PARTIAL'
            arm.update(base=replicated, label=replicated, replicated=True, interpretation_row=5)
        else:
            arm['qualifiers'].append('-NOT-REPLICATED')
            arm['label'] += '-NOT-REPLICATED'
            arm['eligible'] = False
            arm['interpretation_row'] = _interpret(arm['base'], arm['qualifiers'])
    return result


def overtone_reference(logits, log_probs, labels, ce, lam, eps, n_sigma):
    """Independent Eq. 2–3/Algorithm 1 transcription; no solver imports.

    Targets use fp32 logits. The extra term uses recorded log-probabilities and
    is cast once to CE dtype, as frozen in prereg :53–56 and :73.
    """
    import torch
    _num(lam, 'lambda', 0, 1)
    _num(eps, 'epsilon', 0)
    _num(n_sigma, 'n_sigma', 0)
    s = logits.detach().cpu()
    lp = log_probs.detach().cpu()
    y = labels.detach().cpu().reshape(-1)
    original_ce = ce.detach().cpu().reshape(-1)
    _need(s.ndim == 2 and s.shape == lp.shape and s.shape[0] == y.numel() == original_ce.numel()
          and s.shape[1] > 1, 'audit tensor shapes differ')
    _need(y.dtype == torch.long and bool(((y >= 0) & (y < s.shape[1])).all()), 'invalid audit labels')
    _need(all(bool(torch.isfinite(x).all()) for x in (s, lp, original_ce)), 'non-finite audit input')
    kept, mixed, targets, losses, ideals = [], [], [], [], []
    for i in range(s.shape[0]):
        row = s[i].float()
        keep = row > row.max() - n_sigma * row.std(correction=1)
        _need(bool(keep.any()), 'OverTone audit has empty keep-set')
        filtered = torch.softmax(row.masked_fill(~keep, -torch.inf), dim=0)
        onehot = torch.zeros_like(row)
        onehot[int(y[i])] = 1
        candidate = lam * onehot + (1 - lam) * filtered
        mix = int(candidate.argmax()) == int(y[i])
        target = candidate if mix else onehot
        extra = torch.zeros((), dtype=original_ce.dtype)
        if mix:
            entropy = torch.zeros_like(target)
            positive = target > 0
            entropy[positive] = target[positive] * target[positive].log()
            extra = (entropy.sum() - ((target - onehot) * lp[i].float()).sum()).to(original_ce.dtype)
        kl = original_ce[i] + extra
        loss = torch.where(kl > eps, kl, torch.as_tensor(eps, dtype=kl.dtype))
        entropy = torch.zeros_like(target)
        positive = target > 0
        entropy[positive] = target[positive] * target[positive].log()
        ideal = entropy.sum() - (target * torch.log_softmax(row, dim=0)).sum()
        kept.append(keep)
        mixed.append(mix)
        targets.append(target)
        losses.append(loss)
        ideals.append(ideal)
    _need(bool(losses), 'OverTone audit has no scored position')
    return {'keep': torch.stack(kept), 'mix': torch.tensor(mixed, dtype=torch.bool),
            'pi_tar': torch.stack(targets), 'loss': torch.stack(losses),
            'ideal_fp32_kl': torch.stack(ideals)}


def _file_sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _json_sha(value):
    return hashlib.sha256(json.dumps(value, allow_nan=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def _list(value, count, name):
    _need(type(value) is list and len(value) == count, name + ' has incomplete coverage')
    return value


def _batch(value, count, name):
    _dict(value, ('input_ids', 'attention_mask'), name)
    ids = _list(value['input_ids'], count, name + '.input_ids')
    masks = _list(value['attention_mask'], count, name + '.attention_mask')
    _need(type(ids[0]) is list and bool(ids[0]), name + ' has an empty token row')
    width = len(ids[0])
    for row, mask in zip(ids, masks):
        _list(row, width, name + '.token_row')
        _list(mask, width, name + '.mask_row')
        for token in row:
            _int(token, name + '.token', high=151935)
        for bit in mask:
            _int(bit, name + '.mask', high=1)
        _need(any(mask), name + ' has a fully padded row')
    return width


def _fp32_report(value, name):
    _dict(value, ('relative', 'max_abs', 'opposite_tolerance_result'), name)
    if value['relative'] != 'NONFINITE':
        _num(value['relative'], name + '.relative', 0)
    _num(value['max_abs'], name + '.max_abs', 0)
    _need(type(value['opposite_tolerance_result']) is bool, name + ' lacks its diagnostic boolean')


def _parity(value, floor, arithmetic, name):
    _dict(value, ('ok', 'floor', 'tol', 'relative', 'max_abs', 'arithmetic',
                  'report_only_fp32'), name)
    _need(value['ok'] is True and value['arithmetic'] == arithmetic,
          name + ' failed or changed comparison arithmetic')
    _num(value['floor'], name + '.floor', 0, 1e-5)
    _need(value['floor'] == floor and type(value['tol']) in (int, float) and
          value['tol'] == max(10 * floor, 1e-4), name + ' floor/tolerance identity mismatch')
    _num(value['relative'], name + '.relative', 0, 1e-4)
    _num(value['max_abs'], name + '.max_abs', 0)
    _fp32_report(value['report_only_fp32'], name + '.report_only_fp32')


def _captures(value, layers, writer, check, name, zero=False):
    for layer, capture in zip(layers, _list(value, len(layers), name)):
        _dict(capture, ('writer', 'check', 'recipe', 'arm', 'layer', 'norm_float64',
                        'report_only_norm_fp32', 'sha256'), name)
        _need(capture['writer'] == writer and capture['check'] == check and
              capture['recipe'] == 'standalone' and capture['arm'] == 'A7' and
              type(capture['layer']) is int and capture['layer'] == layer,
              name + ' update capture attribution/order mismatch')
        _num(capture['norm_float64'], name + '.norm_float64', 0)
        _num(capture['report_only_norm_fp32'], name + '.report_only_norm_fp32', 0)
        _sha(capture['sha256'], name + '.sha256')
        if zero:
            _need(capture['norm_float64'] == 0, name + ' contains a nonzero null update')


def _residual_evidence(value, layers, name):
    _dict(value, ('rho', 'target_sha256', 'cur_before_sha256', 'cur_after_sha256',
                  'end_ratio', 'applied_difference_report_only'), name)
    _dict(value['rho'], layers, name + '.rho', exact=True)
    for layer in layers:
        _num(value['rho'][layer], name + '.rho.' + layer, 0)
    for key in ('target_sha256', 'cur_before_sha256', 'cur_after_sha256'):
        _sha(value[key], name + '.' + key)
    _num(value['end_ratio'], name + '.end_ratio', 0)
    _need(value['end_ratio'] == value['rho']['8'], name + ' end ratio disagrees with layer 8')
    applied = _dict(value['applied_difference_report_only'], layers, name + '.applied', exact=True)
    for layer in layers:
        _dict(applied[layer], ('norm_float64', 'weight_norm_before_float64'), name + '.applied.' + layer)
        for key in ('norm_float64', 'weight_norm_before_float64'):
            _num(applied[layer][key], name + '.applied.' + layer + '.' + key, 0)


def _target_evidence(record):
    identity = record['identity']
    templates = _dict(identity.get('templates'), ('CANON', 'PTEST'), 'templates', exact=True)
    canon = _str(templates['CANON'], 'CANON')
    ptest = _list(templates['PTEST'], 3, 'PTEST')
    for template in [canon] + ptest:
        _need(type(template) is str and '{}' in template, 'invalid scored template')
    _need(len(set([canon] + ptest)) == 4, 'scored templates are duplicated')
    derived_frames = [context.format(canon) for group in record['ctx'] for context in group]
    _need(record['frames'] == derived_frames and len(set(derived_frames)) == len(derived_frames) and
          canon in derived_frames, 'frames do not equal the realised context frames')
    requests = []
    subjects = None
    for arm in ARMS:
        stimuli = identity['stimuli'][arm]
        for item in stimuli:
            _dict(item, ('subj', 'val'), 'stimulus', exact=True)
            _str(item['subj'], 'stimulus.subj')
            _str(item['val'], 'stimulus.val')
        ordered = [item['subj'] for item in stimuli]
        _need(len(set(ordered)) == 24 and 'Zorbland' in ordered and
              (subjects is None or ordered == subjects),
              'value classes have different subject order')
        subjects = ordered
        requests.extend([[item['subj'], ' ' + item['val']] for item in stimuli])
    _need(len({tuple(r) for r in requests}) == 72, 'target requests are duplicated')
    hashes = _dict(record.get('target_hashes'), ('engine8', 'engine4', 'overtone'),
                   'target_hashes', exact=True)
    nctx = len(derived_frames)
    for name, table in record['targets'].items():
        where = 'targets.' + name
        _dict(table, ('sha256', 'entries', 'diagnostics'), where)
        entries = _list(table['entries'], 72, where + '.entries')
        diagnostics = _list(table['diagnostics'], 72, where + '.diagnostics')
        layer_keys = LAYERS if name == 'engine4' else {'target'}
        for index, (entry, diag, request) in enumerate(zip(entries, diagnostics, requests)):
            item = where + '[' + str(index) + ']'
            _dict(entry, ('request', 'layers'), item + '.entry', exact=True)
            _need(entry['request'] == request, item + ' target request/order mismatch')
            _dict(entry['layers'], layer_keys, item + '.layers', exact=True)
            for layer, vector in entry['layers'].items():
                _dict(vector, ('sha256', 'norm_float64'), item + '.layer.' + layer, exact=True)
                _sha(vector['sha256'], item + '.layer.sha256')
                _num(vector['norm_float64'], item + '.layer.norm_float64', 0)
            _dict(diag, ('request', 'fit', 'steps', 'stop_reason', 'total_loss_at_stop',
                         'norm_float64', 'sha256', 'stdout', 'target_init'), item + '.diagnostic')
            _need(diag['request'] == request, item + ' diagnostic request/order mismatch')
            _num(diag['fit'], item + '.fit', 0, 1)
            steps = _int(diag['steps'], item + '.steps', 1, 25)
            _num(diag['total_loss_at_stop'], item + '.total_loss_at_stop')
            reason = 'total loss < 0.05' if diag['total_loss_at_stop'] < .05 else 'step cap'
            _need(diag['stop_reason'] == reason and (reason != 'step cap' or steps == 25),
                  item + ' stopping reason disagrees with its final evaluated step')
            _sha(diag['sha256'], item + '.sha256')
            _num(diag['norm_float64'], item + '.norm_float64', 0)
            solved = entry['layers']['4' if name == 'engine4' else 'target']
            _need(diag['sha256'] == solved['sha256'] and diag['norm_float64'] == solved['norm_float64'],
                  item + ' solved target identity differs from the table')
            lines = [line for line in _str(diag['stdout'], item + '.stdout').splitlines()
                     if line.startswith('loss ')]
            _need(len(lines) == steps and ' avg prob of [' in lines[-1] and
                  float(lines[-1].rsplit(' ', 1)[1]) == diag['fit'],
                  item + ' fit/steps disagree with captured solver output')
            initial = _dict(diag['target_init'], ('sha256', 'norm_float64', 'shape', 'input_ids',
                            'attention_mask', 'contexts', 'lookup_index', 'dtype'), item + '.target_init')
            _sha(initial['sha256'], item + '.initial.sha256')
            _num(initial['norm_float64'], item + '.initial.norm_float64', 0)
            _need(initial['contexts'] == record['ctx'], item + ' solve contexts changed')
            width = _batch(initial, nctx + 1, item + '.initial')
            shape = _list(initial['shape'], 3, item + '.initial.shape')
            for dimension in shape:
                _int(dimension, item + '.initial.dimension', 1)
            _need(shape[:2] == [nctx + 1, width], item + ' initial capture shape differs from its batch')
            _int(initial['lookup_index'], item + '.initial.lookup_index', -width, width - 1)
            _need(initial['attention_mask'][0][initial['lookup_index']] == 1,
                  item + ' fact index is padding')
            _str(initial['dtype'], item + '.initial.dtype')
            if name == 'engine4':
                distance = _dict(diag.get('target_init_vs_canonical'), ('distance_float64',
                                 'canonical_sha256', 'canonical_batch_shape', 'scope'), item + '.canonical')
                _num(distance['distance_float64'], item + '.canonical.distance', 0)
                _sha(distance['canonical_sha256'], item + '.canonical.sha256')
                _need(distance['canonical_batch_shape'] == [24, shape[2]],
                      item + ' canonical replay batch shape changed')
                _str(distance['scope'], item + '.canonical.scope')
            if name == 'overtone':
                last = _dict(diag.get('per_position_at_stop'), ('step', 'probabilities', 'positions',
                             'prompts'), item + '.per_position_at_stop')
                _int(last['step'], item + '.per_position.step', 0, 24)
                _need(last['step'] == steps - 1, item + ' token probabilities are from a different step')
                ntok = record['recipes']['A']['detail'][ARMS[index // 24]][index % 24]['ntok']
                positions = [[row, pos] for row in range(nctx)
                             for pos in range(sum(initial['attention_mask'][row]) - ntok,
                                              sum(initial['attention_mask'][row]))]
                _need(all(0 <= pos < width for row, pos in positions) and
                      type(last['positions']) is list and
                      all(type(pair) is list and len(pair) == 2 and all(type(v) is int for v in pair)
                          for pair in last['positions']) and last['positions'] == positions,
                      item + ' scored token positions/population mismatch')
                for probability in _list(last['probabilities'], nctx * ntok, item + '.probabilities'):
                    _num(probability, item + '.token_probability', 0, 1)
                prompts = _list(last['prompts'], nctx, item + '.prompts')
                _need(all(type(prompt) is str and prompt.startswith(frame.format(request[0]))
                          for prompt, frame in zip(prompts, derived_frames)),
                      item + ' rewriting prompts differ from the recorded frames')
        _sha(hashes[name], 'target_hashes.' + name)
        _need(table['sha256'] == hashes[name] == _json_sha(entries), where + ' table hash mismatch')
    engine4 = record['targets']['engine4']
    _need(engine4['a7_fit'] == [d['fit'] for d in engine4['diagnostics'][48:]],
          'engine4 A7 fit screen differs from the matching target diagnostics')
    replay = _dict(engine4.get('replay_identity'), ARMS, 'engine4.replay_identity', exact=True)
    endpoint = _dict(engine4.get('endpoint_distance_ratio_float64'), ARMS, 'engine4.endpoint', exact=True)
    for index, arm in enumerate(ARMS):
        meta = _dict(replay[arm], ('input_ids', 'attention_mask', 'padding_side', 'indices', 'requests'),
                     'engine4.replay.' + arm)
        _need(meta['requests'] == requests[index * 24:(index + 1) * 24], 'replay request/order mismatch')
        width = _batch(meta, 24, 'engine4.replay.' + arm)
        _need(meta['padding_side'] in ('left', 'right'), 'replay padding side missing')
        for row, fact_index in enumerate(_list(meta['indices'], 24, 'replay.indices')):
            _int(fact_index, 'replay.index', -width, width - 1)
            _need(meta['attention_mask'][row][fact_index] == 1, 'replay index is padding')
        _num(endpoint[arm], 'engine4.endpoint.' + arm, 0)
    return requests


def _check_evidence(record, requests):
    checks = record['inertness']
    floor = checks['X1-i']['floor']
    _need(checks['X1-i'].get('arithmetic') == 'frozen_cpu_float32', 'solve floor arithmetic missing')
    reduced = _dict(checks['X1-ii'], ('cells', 'floor', 'steps_reference', 'steps_candidate'), 'X1-ii')
    _need(reduced['floor'] == floor, 'X1-ii uses a different solve floor')
    for cell in _list(reduced['cells'], 72, 'X1-ii.cells'):
        _parity(cell, floor, 'frozen_cpu_float32', 'X1-ii.cell')
    for key in ('steps_reference', 'steps_candidate'):
        for step in _list(reduced[key], 72, 'X1-ii.' + key):
            _int(step, 'X1-ii.step', 1, 25)
    _need(reduced['steps_reference'] == reduced['steps_candidate'] ==
          [d['steps'] for d in record['targets']['engine8']['diagnostics']], 'X1-ii step identity mismatch')
    cells = _list(checks['X1-iii'].get('cells'), 4, 'X1-iii.cells')
    coverage = set()
    for cell in cells:
        _dict(cell, ('arm', 'subject', 'at', 'relative_max', 'max_abs',
                     'pi_tar_max_abs_report_only', 'ideal_fp32_kl_report_only'), 'X1-iii.cell')
        key = (cell['arm'], cell['at'])
        _need(key not in coverage and cell['subject'] == 'Zorbland', 'X1-iii duplicated/wrong request')
        coverage.add(key)
        _num(cell['relative_max'], 'X1-iii.relative_max', 0, 1e-4)
        for field in ('max_abs', 'pi_tar_max_abs_report_only'):
            _num(cell[field], 'X1-iii.' + field, 0)
        _need(type(cell['ideal_fp32_kl_report_only']) is list and bool(cell['ideal_fp32_kl_report_only']),
              'X1-iii ideal KL diagnostic missing')
        for number in cell['ideal_fp32_kl_report_only']:
            _num(number, 'X1-iii.ideal_fp32_kl_report_only')
    _need(coverage == {(arm, at) for arm in (ARMS[0], ARMS[2]) for at in ('initial', 'final')},
          'X1-iii cell coverage mismatch')
    gradient = _dict(checks['X1-v'], ('max_abs', 'scope'), 'X1-v')
    _num(gradient['max_abs'], 'X1-v.max_abs', 0, 1e-6)
    _str(gradient['scope'], 'X1-v.scope')
    write = _dict(checks['X2-ii'], ('first', 'second', 'arithmetic', 'report_only_fp32',
                 'canon_full_difference', 'para_full_difference'), 'X2-ii')
    write_floor = write['floor']
    _need(write['arithmetic'] == 'cpu_float64', 'write floor arithmetic changed')
    for side in ('first', 'second'):
        _captures(write[side], list(range(4, 9)), 'my_edit', 'X2-ii ' + side, 'X2-ii.' + side)
    for report in _list(write['report_only_fp32'], 5, 'X2-ii.report_only_fp32'):
        _fp32_report(report, 'X2-ii.fp32')
    _int(write['canon_full_difference'], 'X2-ii.canon_difference', -24, 24)
    _int(write['para_full_difference'], 'X2-ii.para_difference', -72, 72)
    for name in ('X1-iv', 'X2-iii'):
        _dict(checks[name], ('floor', 'layers'), name)
        _need(checks[name]['floor'] == write_floor, name + ' write floor identity mismatch')
        layers = _dict(checks[name]['layers'], LAYERS, name + '.layers', exact=True)
        for layer in LAYERS:
            _parity(layers[layer], write_floor, 'cpu_float64', name + '.' + layer)
    _residual_evidence(checks['X2-iii'].get('rho_A'), LAYERS, 'X2-iii.rho_A')
    replay = checks['X2-iv']
    replay_cells = _list(replay.get('cells'), 27, 'X2-iv.cells')
    measured_floor = 0.
    for index, cell in enumerate(replay_cells):
        arm, offset = ARMS[index // 9], index % 9
        layer = 4 + offset if offset < 5 else offset
        _dict(cell, ('arm', 'layer'), 'X2-iv.cell')
        _need(cell['arm'] == arm and type(cell['layer']) is int and cell['layer'] == layer,
              'X2-iv replay arm/layer coverage mismatch')
        _num(cell.get('floor'), 'X2-iv.cell.floor', 0, 1e-5)
        if offset < 5:
            measured_floor = max(measured_floor, cell['floor'])
        else:
            _need(cell['floor'] == measured_floor, 'X2-iv null replay uses a different measured floor')
        _parity(cell, cell['floor'], 'frozen_cpu_float32', 'X2-iv.cell')
    _need(replay['floor'] == measured_floor, 'X2-iv maximum floor mismatch')
    for index, item in enumerate(_list(checks['X2-v'].get('indices'), 72, 'X2-v.indices')):
        _dict(item, ('request', 'solve_index', 'injection_index'), 'X2-v.index')
        _need(item['request'] == requests[index], 'X2-v request/order mismatch')
        meta = record['targets']['engine4']['replay_identity'][ARMS[index // 24]]
        width = len(meta['input_ids'][index % 24])
        _int(item['solve_index'], 'X2-v.solve_index', -width, width - 1)
        _int(item['injection_index'], 'X2-v.injection_index', item['solve_index'], item['solve_index'])
        _need(item['solve_index'] == meta['indices'][index % 24],
              'X2-v index differs from actual replay metadata')
    singleton = _dict(checks['X2-vi'], ('targets', 'layers', 'cache', 'applied_weight_exact',
                      'greedy_flags_exact', 'flags_reference', 'flags_candidate', 'reference', 'candidate'), 'X2-vi')
    for cell in _list(singleton['targets'], 24, 'X2-vi.targets'):
        _parity(cell, floor, 'frozen_cpu_float32', 'X2-vi.target')
    _dict(singleton['layers'], ('8',), 'X2-vi.layers', exact=True)
    _parity(singleton['layers']['8'], write_floor, 'cpu_float64', 'X2-vi.update')
    _parity(singleton['cache'], write_floor, 'frozen_cpu_float32', 'X2-vi.cache')
    for side, writer in (('reference', 'my_edit'), ('candidate', 'fe_edit')):
        _captures(singleton[side], [8], writer, 'X2-vi ' + ('original' if side == 'reference' else 'active'),
                  'X2-vi.' + side)
    _need(singleton['reference'][0]['norm_float64'] > 0, 'X2-vi reference update is zero')
    _need(singleton['applied_weight_exact'] is True and singleton['greedy_flags_exact'] is True,
          'X2-vi weight/greedy identity failed')
    for side in ('flags_reference', 'flags_candidate'):
        for pair in _list(singleton[side], 96, 'X2-vi.' + side):
            _need(type(pair) is list and len(pair) == 2 and all(type(flag) is bool for flag in pair) and
                  (not pair[0] or pair[1]), 'X2-vi malformed full/first flags')
    _need(singleton['flags_reference'] == singleton['flags_candidate'], 'X2-vi per-prompt flags differ')
    null = _dict(checks['X2-vii'], ('layers', 'requests', 'weight_identity', 'residuals'), 'X2-vii')
    _captures(null['layers'], list(range(4, 9)), 'fe_edit', 'X2-vii', 'X2-vii.layers', zero=True)
    _need(null['requests'] == requests[48:] and null['weight_identity'] is True,
          'X2-vii request/weight identity failed')
    for layer, residual in zip(range(4, 9), _list(null['residuals'], 5, 'X2-vii.residuals')):
        _dict(residual, ('layer', 'residual_sha256', 'exact_zero'), 'X2-vii.residual')
        _need(type(residual['layer']) is int and residual['layer'] == layer and residual['exact_zero'] is True,
              'X2-vii residual is nonzero or has wrong layer order')
        _sha(residual['residual_sha256'], 'X2-vii.residual.sha256')
    g8 = _dict(checks['G8'], ('expr_delta', 'loc_delta', 'raw_expr_delta', 'raw_loc_delta',
               'reference', 'candidate'), 'G8')
    for side in ('reference', 'candidate'):
        observed = _dict(g8[side], ('probability', 'locality', 'distribution', 'top1', 'locality_top1'), 'G8.' + side)
        _num(observed['probability'], 'G8.probability', 0, 1)
        _num(observed['locality'], 'G8.locality', 0, 100)
        distribution = _list(observed['distribution'], 151936, 'G8.distribution')
        for probability in distribution:
            _num(probability, 'G8.distribution.probability', 0, 1)
        _int(observed['top1'], 'G8.top1', high=151935)
        _int(observed['locality_top1'], 'G8.locality_top1', high=151935)
        _need(observed['top1'] == max(range(len(distribution)), key=distribution.__getitem__),
              'G8 top-1 disagrees with its full distribution')
    for field, source, decimals, bound in (('expr_delta', 'probability', 4, .05), ('loc_delta', 'locality', 2, 3)):
        raw = abs(g8['reference'][source] - g8['candidate'][source])
        _num(g8['raw_' + field], 'G8.raw_' + field, 0)
        _num(g8[field], 'G8.' + field, 0)
        _need(g8['raw_' + field] == raw and g8[field] == round(raw, decimals) and
              g8[field] < bound, 'G8 behavioural gate evidence mismatch')


def _probe_evidence(record):
    frames, recipes = record['frames'], record['recipes']
    frame_subjects = ['Vorbanth', 'Quillexa', 'Tremnok', 'Oskavel', 'Blynthar', 'Durmquist']
    subjects = [item['subj'] for item in record['identity']['stimuli'][ARMS[2]]]
    _need(not set(frame_subjects) & set(subjects), 'frame probe includes an edited subject')
    relation_templates = {'{} is associated with': 'bystander', '{} is a': 'objective-anchored'}
    baseline_extra = recipes['A']['arms'][ARMS[2]]['extra']
    for name, recipe in recipes.items():
        gate = _dict(recipe['law5_gate'], ('raw_expr_delta', 'raw_loc_delta', 'candidate_calls'), name + '.G')
        _int(gate['candidate_calls'], name + '.G.candidate_calls', high=0)
        for key, places in (('expr_delta', 4), ('loc_delta', 2)):
            _num(gate['raw_' + key], name + '.G.raw_' + key, 0)
            _need(gate[key] == round(gate['raw_' + key], places), name + ' G rounded/raw delta mismatch')
        _need(recipe.get('counters') == record['counters'][name], name + ' recorded recipe counters differ')
        diagnostics = _dict(recipe.get('residual_diagnostics'), ARMS, name + '.residual_diagnostics', exact=True)
        for arm in ARMS:
            _residual_evidence(diagnostics[arm], LAYERS, name + '.' + arm + '.residuals')
        extra = _dict(recipe['arms'][ARMS[2]]['extra'], ('frames', 'frames_pristine',
                      'relation_labels', 'teacher_forced_curve'), name + '.A7.extra')
        for key in ('frames', 'frames_pristine'):
            _dict(extra[key], frames, name + '.' + key, exact=True)
            for frame, count in extra[key].items():
                _dict(count, ('flips', 'n', 'rows'), name + '.frame')
                _int(count['n'], name + '.frame.n', 6, 6)
                _int(count['flips'], name + '.frame.flips', high=6)
                rows = _list(count['rows'], 6, name + '.frame.rows')
                for subject, row in zip(frame_subjects, rows):
                    _dict(row, ('subj', 'top1', 'tok', 'flip'), name + '.frame.row')
                    _need(row['subj'] == subject and type(row['tok']) is str and type(row['flip']) is bool,
                          name + ' frame probe row identity/flag mismatch')
                    _int(row['top1'], name + '.frame.top1', high=151935)
                _need(count['flips'] == sum(row['flip'] for row in rows), name + ' frame flags/count mismatch')
        _need(extra['frames_pristine'] == baseline_extra['frames_pristine'], name + ' pristine frame probes differ')
        relation = _dict(extra['relation_labels'], relation_templates, name + '.relations', exact=True)
        for template, kind in relation_templates.items():
            item = _dict(relation[template], ('kind', 'flips', 'pristine', 'rows'), name + '.relation')
            _need(item['kind'] == kind and item['rows'] == subjects, name + ' relation identity/order mismatch')
            _int(item['flips'], name + '.relation.flips', high=24)
            for token in _list(item['pristine'], 24, name + '.relation.pristine'):
                _int(token, name + '.relation.pristine_token', high=151935)
            _need(item['pristine'] == baseline_extra['relation_labels'][template]['pristine'],
                  name + ' pristine relation probe differs')
        rows = recipe['detail'][ARMS[2]]
        curve = _dict(extra['teacher_forced_curve'], [str(pos) for pos in range(max(row['ntok'] for row in rows))],
                      name + '.teacher_forced_curve', exact=True)
        for position, count in curve.items():
            _dict(count, ('correct', 'n'), name + '.curve.' + position, exact=True)
            expected_n = 3 * sum(row['ntok'] > int(position) for row in rows)
            _int(count['n'], name + '.curve.n', expected_n, expected_n)
            _int(count['correct'], name + '.curve.correct', high=expected_n)
    injection = _dict(record['inject'].get('details'), ('reference',) + CANDIDATES, 'inject.details', exact=True)
    templates = [record['identity']['templates']['CANON']] + record['identity']['templates']['PTEST']
    expected_rows = record['identity']['stimuli'][ARMS[2]]
    for name, screen in injection.items():
        _dict(screen, ('canon_n', 'para_n', 'per_template', 'rows'), 'inject.' + name)
        rows = _list(screen['rows'], 24, 'inject.rows')
        for expected, row in zip(expected_rows, rows):
            _dict(row, ('subj', 'val', 'per_template'), 'inject.row', exact=True)
            _need(row['subj'] == expected['subj'] and row['val'] == expected['val'], 'injection row identity/order mismatch')
            _need(type(row['per_template']) is list and len(row['per_template']) == 4 and
                  all(type(flag) is bool for flag in row['per_template']), 'injection requires four prompt flags')
        _int(screen['canon_n'], 'inject.canon_n', high=24)
        _int(screen['para_n'], 'inject.para_n', high=72)
        _dict(screen['per_template'], templates, 'inject.per_template', exact=True)
        for index, template in enumerate(templates):
            _int(screen['per_template'][template], 'inject.template_count', high=24)
            _need(screen['per_template'][template] == sum(row['per_template'][index] for row in rows),
                  'injection per-template count differs from flags')
        _need(screen['canon_n'] == screen['per_template'][templates[0]] and
              screen['para_n'] == record['inject'][name] == sum(screen['per_template'][t] for t in templates[1:]),
              'injection aggregate counts differ from flags')


def _file_evidence(record, supervisor):
    """Completion admission; synthetic classifier inputs do not enter here."""
    _dict(record, MANIFEST + ('write_size_diagnostics',), 'complete manifest')
    identity = record['identity']
    _need(identity['hparams'] == record['sources_start'].get('configs/hparams/qwen25_3b_memit_hparams.json') and
          record['prereg_sha256'] == record['sources_start'].get('docs/C10X_ENGINEPATH_PREREG.md'),
          'manifest hparams/prereg hash differs from declared sources')
    software = _dict(identity['software'], ('python', 'machine', 'platform', 'torch', 'transformers', 'model_rev'), 'software')
    for key in software:
        _str(software[key], 'software.' + key)
    _need(software['model_rev'] == identity['model_rev'], 'software/model revision identity mismatch')
    for key in ('model', 'effort'):
        _str(_dict(record['reviewer'], ('model', 'effort'), 'reviewer')[key], 'reviewer.' + key)
    go = _dict(_dict(record['provenance'], ('go',), 'provenance')['go'], ('path', 'sha256'), 'go identity', exact=True)
    _need(Path(_str(go['path'], 'go.path')).is_absolute(), 'go identity path is relative')
    _sha(go['sha256'], 'go.sha256')
    if record['process'] == 2:
        _need(Path(_str(record['provenance'].get('process1'), 'process1 provenance')).is_absolute(),
              'process1 provenance path is relative')
    requests = _target_evidence(record)
    _check_evidence(record, requests)
    _probe_evidence(record)
    checkpoints = record['w0']['checkpoints']
    names = []
    for checkpoint in checkpoints:
        _dict(checkpoint, ('checkpoint', 'ok', 'hashes'), 'W0 checkpoint')
        names.append(_str(checkpoint['checkpoint'], 'W0 checkpoint name'))
        _hashes(checkpoint['hashes'], 'W0 checkpoint hashes', LAYERS)
        _need(checkpoint['ok'] is True and checkpoint['hashes'] == record['w0']['hashes'], 'W0 checkpoint mismatch')
    required = {'before target construction', 'after target construction', 'before injection',
                'after injection', 'before projector', 'X2-vii exact zero', 'after inertness',
                'after final recipe', 'closeout restore'}
    for recipe in RECIPES:
        required.update(('before recipe ' + recipe, 'after recipe ' + recipe))
    for cell in ('X1-i', 'X2-ii first', 'X2-ii second', 'X1-iv', 'X2-iii', 'X2-vi builder',
                 'X2-vi original', 'X2-vi active', 'X2-vii null', 'G8 engine', 'G8 active FE'):
        required.update(('before ' + cell, 'after ' + cell))
    for arm in ARMS:
        required.add('X2-iv ' + arm)
        required.update('X1-ii ' + arm + ' ' + item['subj'] for item in record['identity']['stimuli'][arm])
    _need(required <= set(names) and names.count('before recipe A') >= 2 and
          names.count('harness restore') >= 18, 'W0 checkpoint coverage is incomplete')
    for before in (name for name in required if name.startswith('before ')):
        after = 'after ' + before[7:]
        if after in required:
            _need(names.index(before) < names.index(after), 'W0 checkpoint order mismatch: ' + before)
    timeline = ['before recipe A', 'after recipe A', 'before target construction',
                'after target construction', 'before X1-i', 'after X1-i', 'before projector',
                'after inertness', 'before injection', 'after injection', 'before recipe I-2',
                'after recipe I-2', 'before recipe I-1', 'after recipe I-1', 'after final recipe',
                'closeout restore']
    _need([names.index(name) for name in timeline] == sorted(names.index(name) for name in timeline),
          'W0 stage order differs from the frozen baseline-first schedule')
    for recipe in RECIPES:
        start, end = names.index('before recipe ' + recipe), names.index('after recipe ' + recipe)
        _need(names[start:end].count('harness restore') >= 6, recipe + ' W0 restorations are incomplete')
    reports = _dict(record['write_size_diagnostics'], CANDIDATES, 'write_size_diagnostics', exact=True)
    baseline = sum(record['recipes']['A']['write_norms_float64'][ARMS[2]].values())
    for name, report in reports.items():
        _dict(report, ('ratio_float64', 'ratio_fp32_report_only', 'opposite_1_5_result'), 'write_size.' + name)
        ratio = sum(record['recipes'][name]['write_norms_float64'][ARMS[2]].values()) / baseline
        _num(report['ratio_float64'], 'write_size.ratio_float64', 0)
        _need(report['ratio_float64'] == ratio, 'write-size diagnostic differs from captured norms')
        if report['ratio_fp32_report_only'] != 'NONFINITE':
            _num(report['ratio_fp32_report_only'], 'write_size.ratio_fp32_report_only', 0)
        _need(type(report['opposite_1_5_result']) is bool, 'write-size fp32 diagnostic boolean missing')
    caps = {'setup': 600., 'A': 2040., 'targets': 2400., 'inertness': 3000.,
            'injection': 1500., 'I-2': 2040., 'I-1': 2040., 'final': 780.}
    plan = {'setup': {}, 'A': {'recipe_arm': 3, 'G': 1}, 'targets': {'solve': 216},
            'inertness': {'solve': 100, 'write': 6, 'G8': 1}, 'injection': {'injection': 288},
            'I-2': {'recipe_arm': 3, 'G': 1}, 'I-1': {'recipe_arm': 3, 'G': 1}, 'final': {}}
    timings = _dict(record['timings'], tuple(caps) + ('work_units',), 'timings', exact=True)
    units = _dict(timings['work_units'], caps, 'timings.work_units', exact=True)
    for stage, cap in caps.items():
        _num(timings[stage], 'timings.' + stage, 0, cap)
        _dict(units[stage], plan[stage], 'timings.units.' + stage, exact=True)
        for kind, count in plan[stage].items():
            for duration in _list(units[stage][kind], count, 'timings.units.' + stage + '.' + kind):
                _num(duration, 'timings.unit_duration', 0, timings[stage])
    _num(supervisor.get('elapsed_seconds'), 'supervisor.elapsed_seconds', 0, 15000)
    _need(sum(timings[stage] for stage in caps) <= supervisor['elapsed_seconds'],
          'measured stage durations exceed supervisor process elapsed time')


def _audit_snapshot(snapshot, settings):
    import torch
    _dict(snapshot, ('arm', 'subject', 'at', 'logits', 'log_probs', 'labels', 'ce',
                    'row_map', 'position_map', 'mask', 'dtype', 'observed'), 'audit snapshot')
    _need(snapshot['arm'] in (ARMS[0], ARMS[2]) and snapshot['subject'] == 'Zorbland' and
          snapshot['at'] in ('initial', 'final'), 'unexpected audit request/step')
    s, lp, labels, ce = (snapshot[key] for key in ('logits', 'log_probs', 'labels', 'ce'))
    for tensor in (s, lp, labels, ce, snapshot['mask']):
        _need(isinstance(tensor, torch.Tensor) and tensor.device.type == 'cpu' and
              not tensor.requires_grad, 'audit tensor is not detached CPU data')
    _need(s.ndim == 2 and s.shape[1] == 151936, 'audit is not full vocabulary')
    _need(snapshot['dtype'] == str(s.dtype) and lp.dtype == s.dtype, 'audit dtype mismatch')
    mask = snapshot['mask']
    _need(mask.ndim == 2 and mask.dtype == torch.bool, 'audit mask must be a boolean matrix')
    positions = mask.nonzero(as_tuple=False).tolist()
    _need(type(snapshot['row_map']) is list and type(snapshot['position_map']) is list and
          all(type(x) is int for x in snapshot['row_map'] + snapshot['position_map']) and
          list(map(list, zip(snapshot['row_map'], snapshot['position_map']))) == positions,
          'audit position map differs from scored mask')
    _need(len(positions) == s.shape[0], 'audit mask/scored-row count mismatch')
    reference = overtone_reference(s, lp, labels, ce, **settings)
    gathered = -lp.gather(1, labels.reshape(-1, 1)).reshape(-1)
    _need(torch.equal(gathered, ce.reshape(-1)), 'audit CE differs from recorded engine log-probabilities')
    observed = _dict(snapshot['observed'], ('keep', 'mix', 'pi_tar', 'loss'), 'observed audit')
    for key in ('keep', 'mix', 'pi_tar', 'loss'):
        value = observed[key]
        _need(isinstance(value, torch.Tensor) and value.device.type == 'cpu' and
              not value.requires_grad and bool(torch.isfinite(value).all()), 'invalid observed ' + key)
        _need(value.shape == reference[key].shape, 'observed ' + key + ' shape differs')
    _need(observed['keep'].dtype == torch.bool and observed['mix'].dtype == torch.bool and
          torch.equal(observed['keep'], reference['keep']) and
          torch.equal(observed['mix'], reference['mix']), 'audit filter/mix mismatch')
    difference = (observed['loss'].float() - reference['loss'].float()).abs()
    denominator = torch.maximum(reference['loss'].float().abs(),
                                torch.full_like(difference, max(settings['eps'], 1e-12)))
    _need(bool((difference / denominator <= 1e-4).all()), 'audit token-loss tolerance exceeded')
    pi_y = reference['pi_tar'].gather(1, labels.reshape(-1, 1)).reshape(-1)
    observed_pi_y = observed['pi_tar'].gather(1, labels.reshape(-1, 1)).reshape(-1)
    return {'arm': snapshot['arm'], 'at': snapshot['at'],
            'loss_max_abs': float(difference.max()),
            'pi_y_max_abs': float((pi_y - observed_pi_y).abs().max()),
            'ideal_fp32_kl': reference['ideal_fp32_kl'].tolist()}


def _audit_request(snapshot, record, diagnostic):
    arm = snapshot['arm']
    subjects = [item['subj'] for item in record['identity']['stimuli'][arm]]
    index = subjects.index('Zorbland')
    target = record['targets']['overtone']['diagnostics'][ARMS.index(arm) * 24 + index]
    _need(target['request'] == ['Zorbland', ' ' + record['identity']['stimuli'][arm][index]['val']] and
          snapshot.get('settings') == record['identity']['settings'],
          'binary audit request/settings differ from the scored target')
    initial, last = target['target_init'], target['per_position_at_stop']
    nctx, width = len(record['frames']), len(initial['input_ids'][0])
    _need(list(snapshot['mask'].shape) == [nctx, width] and
          list(map(list, zip(snapshot['row_map'], snapshot['position_map']))) == last['positions'],
          'binary audit batch/positions differ from its target solve')
    ntok = record['recipes']['A']['detail'][arm][index]['ntok']
    labels = snapshot['labels'].reshape(nctx, ntok).tolist()
    for row, tokens in enumerate(labels):
        end = sum(initial['attention_mask'][row])
        _need(tokens == labels[0] and initial['input_ids'][row][end - ntok + 1:end] == tokens[:-1],
              'binary audit labels differ from the target-prefix inputs')
    if snapshot['at'] == 'final':
        observed = snapshot['log_probs'].float().exp().gather(1, snapshot['labels'].reshape(-1, 1)).reshape(-1).tolist()
        diagnostic['recorded_probability_max_abs_report_only'] = max(
            abs(a - b) for a, b in zip(observed, last['probabilities']))


def audited_record(out):
    """File admission has no bypass: all five records and binary audits exist."""
    import c10x_enginepath_arms as driver
    directory = Path(out)
    _need(directory.is_absolute(), 'out directory must be absolute')
    directory = directory.resolve(strict=True)
    _need(directory.is_dir(), 'out path is not a directory')
    root = Path(driver.ROOT).resolve()
    _need(root / 'results' in directory.parents, 'out directory is outside ROOT/results')
    record = strict_json((directory / 'run.json').read_bytes())
    _validate(record)
    supervisor_halt=directory.with_name(directory.name+'_logs')/'supervisor_halt.json'
    _need(not supervisor_halt.exists() and not supervisor_halt.is_symlink(), 'supervisor recorded a late persistence HALT; rerun required')
    supervisor=strict_json((directory.with_name(directory.name+'_logs')/'supervisor.json').read_bytes())
    _need(supervisor.get('status')=='COMPLETE' and supervisor.get('completion')=='complete' and
          type(supervisor.get('exit_code')) is int and supervisor['exit_code']==0 and
          supervisor.get('out')==str(directory) and supervisor.get('process')==record['process'] and
          supervisor.get('run_id')==record['run_id'],
          'supervisor did not admit a complete process; rerun required')
    current = driver.source_hashes()
    _need(record['sources_start'] == current and record['sources_end'] == current,
          'current declared source identity differs from recorded start/end')
    _file_evidence(record, supervisor)
    ctx,context_source=driver.recorded_contexts()
    _need(record['ctx']==ctx and record['context_source']==context_source and
          record['sources_start'].get(driver.CONTEXT_SOURCE)==context_source['source_sha256'],
          'recorded context source identity differs from the pinned C10Q set')
    context_file=strict_json((directory/'context_templates.json').read_bytes())
    _need(context_file=={'schema':'c10x_context_templates/v1','ctx':ctx,
                         'ctx_sha256':record['ctx_sha256'],'source':context_source},
          'context_templates.json differs from the recorded pre-baseline contexts')
    for filename, section in (('targets.json', 'targets'), ('inertness.json', 'inertness'),
                              ('inject.json', 'inject'), ('pass1.json', 'recipes')):
        companion = strict_json((directory / filename).read_bytes())
        _dict(companion, ('manifest', section), filename, exact=True)
        manifest = _dict(companion['manifest'], MANIFEST, filename + '.manifest')
        _finite_tree(companion)
        _nulls(companion)
        for key in MANIFEST:
            _need(manifest[key] == record[key], filename + ' manifest mismatch: ' + key)
        _need(companion[section] == record[section], filename + ' recorded evidence mismatch')
    _need(_json_sha(record['ctx']) == record['ctx_sha256'] and
          _json_sha(record['frames']) == record['frames_sha256'], 'context/frame hash mismatch')
    _need(set(record['identity']['covariance']) == LAYERS, 'covariance identity omits a band layer')
    files = record['audits'].get('files')
    _need(type(files) is list and bool(files), 'full-logit audit files missing')
    _need(record['audits']['sha256'] == _json_sha(files), 'audit manifest hash mismatch')
    import torch
    audited, diagnostics, paths = set(), [], set()
    for entry in files:
        _dict(entry, ('path', 'sha256'), 'audit file', exact=True)
        _sha(entry['sha256'], 'audit file SHA-256')
        raw_path = Path(_str(entry['path'], 'audit file path'))
        path = (raw_path if raw_path.is_absolute() else directory / raw_path).resolve(strict=True)
        _need(directory in path.parents and path not in paths and path.is_file(),
              'audit file is outside its process directory, duplicated, or not a file')
        _need('telemetry' not in path.relative_to(directory).parts, 'science audit cannot read telemetry')
        paths.add(path)
        _need(_file_sha(path) == entry['sha256'], 'audit file hash mismatch')
        try:
            payload = torch.load(path, map_location='cpu', weights_only=True)
        except (RuntimeError, EOFError, pickle.UnpicklingError) as exc:
            raise ValueError('cannot decode lossless audit file: ' + str(path)) from exc
        _dict(payload, ('snapshots',), 'audit binary', exact=True)
        _need(type(payload['snapshots']) is list and bool(payload['snapshots']), 'audit snapshots missing')
        for snapshot in payload['snapshots']:
            key = (snapshot.get('arm'), snapshot.get('at')) if type(snapshot) is dict else None
            _need(key not in audited, 'duplicate audit cell')
            diagnostic = _audit_snapshot(snapshot, record['identity']['settings'])
            _audit_request(snapshot, record, diagnostic)
            diagnostics.append(diagnostic)
            audited.add(key)
    _need(audited == {(arm, at) for arm in (ARMS[0], ARMS[2]) for at in ('initial', 'final')},
          'audit does not cover both requests at step zero and final evaluated step')
    _need(driver.source_hashes() == current, 'source drift during reader admission')
    _need(not supervisor_halt.exists() and not supervisor_halt.is_symlink(), 'supervisor recorded a late persistence HALT during admission; rerun required')
    record['_out_dir'] = str(directory)
    return record, diagnostics


def load_record(out):
    """The driver uses the same complete admission as the reader CLI."""
    return audited_record(out)[0]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--process2', type=Path)
    args = parser.parse_args(argv)
    _need(args.out.is_absolute() and (args.process2 is None or args.process2.is_absolute()),
          'all reader paths must be absolute')
    destination = (args.process2 if args.process2 is not None else args.out) / 'reader.json'
    _need(not destination.exists(), 'reader.json already exists')
    try:
        first, audit1 = audited_record(args.out)
        if args.process2 is None:
            result = read_record(first)
            result['audit'] = audit1
        else:
            second, audit2 = audited_record(args.process2)
            result = combine(first, second)
            result['audit'] = {'1': audit1, '2': audit2}
    except (OSError, KeyError, TypeError, ValueError, OverflowError) as exc:
        result = _invalid([str(exc)])
    with destination.open('x') as handle:
        json.dump(result, handle, allow_nan=False, sort_keys=True, separators=(',', ':'))
        handle.write('\n')
    print(json.dumps(result, allow_nan=False, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
