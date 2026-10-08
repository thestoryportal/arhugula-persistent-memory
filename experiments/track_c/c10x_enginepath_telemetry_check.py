"""T8 pristine telemetry admission runner and T11 model-free answer audit."""
import argparse
import datetime
import json
import math
from pathlib import Path
import re
import uuid


CANON = 'The capital of {} is the city of'
PTEST = ["{}'s capital city is called", 'If you visit {}, its capital city is',
         'The main city and seat of government of {} is']
ARM_NAMES = ('A1_single', 'A2_coherent2', 'A7_coined_coined')
COMMON = {'kind', 't_utc', 'elapsed_s', 'cumulative_s', 'process', 'run_id'}
CAUSES = ('MISMATCH', 'DUPLICATE', 'MISSING', 'MALFORMED', 'UNEXPECTED', 'DISABLED')
DISABLED_MARKER = 'C10X_TELEMETRY_DISABLED '
SCOPE = ('Equality of the pristine generated IDs, flags and same-batch science-forward '
         'tensors under the recorded identity only. Resource inertness and equality '
         'of edited-arm outputs and records on MPS remain UNVERIFIED.')


def _driver():
    import c10x_enginepath_arms
    return c10x_enginepath_arms


def _constant(value):
    raise ValueError('nonfinite JSON constant: '+value)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON field: '+key)
        result[key] = value
    return result


def strict_json(data):
    return json.loads(data, parse_constant=_constant, object_pairs_hook=_unique_object)


def validate_out(out):
    """T8 allows exactly one child directory; resolve ROOT at call time."""
    A = _driver()
    candidate = Path(out)
    if not candidate.is_absolute():
        raise ValueError('telemetry inertness out must be absolute')
    root = Path(A.ROOT).resolve()
    A.selftest_root(root)
    base = (root/'results/c10x_enginepath_telemetry_inertness').resolve()
    candidate = candidate.resolve()
    if root not in base.parents or candidate.parent != base or candidate == base:
        raise ValueError('telemetry inertness out must be one directory under '+str(base))
    record = candidate/'inertness.json'
    if candidate.exists() or candidate.is_symlink() or record.exists() or record.is_symlink():
        raise FileExistsError(str(record))
    return candidate


def _text(value):
    return isinstance(value, str) and bool(value)


def _number(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def _probability(value):
    return _number(value) and 0. <= value <= 1.


def _ids(value):
    return isinstance(value, list) and bool(value) and all(type(x) is int and x >= 0 for x in value)


def _request(value):
    return isinstance(value, list) and len(value) == 2 and all(_text(x) for x in value)


def _norms(value):
    fields = {'delta_norm', 'weight_norm_before', 'relative_delta_norm'}
    return isinstance(value, dict) and all(
        isinstance(layer, str) and layer.isdecimal() and isinstance(row, dict) and
        set(row) == fields and all(_number(x) and x >= 0. for x in row.values())
        for layer, row in value.items())


def _target_values(table, values):
    if table in ('engine8', 'engine4'):
        return isinstance(values, list) and all(
            isinstance(row, dict) and set(row) == {'request', 'p'} and
            _request(row['request']) and _probability(row['p']) for row in values)
    if table != 'overtone' or not isinstance(values, dict):
        return False
    if set(values) != {'request', 'prompt', 'position', 'p'}:
        return False
    if not all(isinstance(array, list) for array in values.values()):
        return False
    return (len({len(array) for array in values.values()}) == 1 and
            all(_request(x) for x in values['request']) and
            all(_text(x) for x in values['prompt']) and
            all(type(x) is int and x >= 0 for x in values['position']) and
            all(_probability(x) for x in values['p']))


def _lens(layers, items):
    if not isinstance(layers, list) or not layers or not all(type(x) is int and x >= 0 for x in layers):
        return False
    if len(layers) != len(set(layers)) or not isinstance(items, list):
        return False
    keys = {str(layer) for layer in layers}
    for item in items:
        if not isinstance(item, dict) or set(item) != {'subj', 'prompt', 'top'}:
            return False
        if not _text(item['subj']) or not _text(item['prompt']) or not isinstance(item['top'], dict):
            return False
        if set(item['top']) != keys:
            return False
        for top in item['top'].values():
            if not isinstance(top, list) or len(top) != 5:
                return False
            for token in top:
                if not (isinstance(token, list) and len(token) == 3 and
                        type(token[0]) is int and token[0] >= 0 and
                        isinstance(token[1], str) and _probability(token[2])):
                    return False
    return True


def line_causes(line):
    """Validate the T2 common fields and the exact T3/T4 kind schema."""
    if not isinstance(line, dict):
        return ['MALFORMED']
    causes = set()
    try:
        json.dumps(line, allow_nan=False)
    except (TypeError, ValueError):
        causes.add('MALFORMED')
    if not COMMON <= set(line):
        causes.add('MALFORMED')
    if not all(_text(line.get(key)) for key in ('kind', 't_utc', 'run_id')):
        causes.add('MALFORMED')
    if type(line.get('process')) is not int or line.get('process') not in (1, 2):
        causes.add('MALFORMED')
    if not all(_number(line.get(key)) and line[key] >= 0. for key in ('elapsed_s', 'cumulative_s')):
        causes.add('MALFORMED')
    kind = line.get('kind')
    payloads = {
        'header': {'schema', 'telemetry'},
        'phase': {'event'},
        'write_norms': {'recipe', 'arm', 'mode', 'harness_fp32'},
        'target_probs': {'table', 'values'},
        'logit_lens': {'where', 'layers', 'items'},
        'answer': {'recipe', 'arm', 'phase', 'subj', 'val', 'template', 'prompt',
                   'target_ids', 'generated_ids', 'text', 'full', 'first'},
    }
    if not isinstance(kind, str) or kind not in payloads:
        if isinstance(kind, str):
            causes.add('UNEXPECTED')
        return [cause for cause in CAUSES if cause in causes]
    required = COMMON | payloads[kind]
    optional = set()
    if kind == 'phase':
        events = {
            'stage_start': 'stage', 'stage_end': 'stage',
            'recipe_start': 'recipe', 'recipe_end': 'recipe',
            'check_start': 'check', 'check_end': 'check', 'halt': 'code',
        }
        event = line.get('event')
        attribution = events.get(event) if isinstance(event, str) else None
        if attribution is None:
            causes.add('MALFORMED')
        else:
            required.add(attribution)
    elif kind == 'write_norms':
        optional.add('driver_float64')
    if not required <= set(line):
        causes.add('MALFORMED')
    if set(line) - required - optional:
        causes.add('UNEXPECTED')
    if kind == 'write_norms' and isinstance(line.get('harness_fp32'), dict):
        for row in line['harness_fp32'].values():
            if isinstance(row, dict) and set(row) - {'delta_norm', 'weight_norm_before', 'relative_delta_norm'}:
                causes.add('UNEXPECTED')
    elif kind == 'target_probs':
        values = line.get('values')
        if line.get('table') in ('engine8', 'engine4') and isinstance(values, list):
            if any(isinstance(row, dict) and set(row) - {'request', 'p'} for row in values):
                causes.add('UNEXPECTED')
        elif line.get('table') == 'overtone' and isinstance(values, dict):
            if set(values) - {'request', 'prompt', 'position', 'p'}:
                causes.add('UNEXPECTED')
    elif kind == 'logit_lens' and isinstance(line.get('items'), list):
        layers = line.get('layers')
        for item in line['items']:
            if isinstance(item, dict):
                if set(item) - {'subj', 'prompt', 'top'}:
                    causes.add('UNEXPECTED')
                if (isinstance(layers, list) and all(type(x) is int for x in layers) and
                        isinstance(item.get('top'), dict) and set(item['top']) - {str(x) for x in layers}):
                    causes.add('UNEXPECTED')
    if 'MALFORMED' not in causes:
        valid = True
        if kind == 'header':
            valid = line['schema'] == 'c10x_enginepath_telemetry/v1' and line['telemetry'] is True
        elif kind == 'phase':
            valid = _text(line[attribution])
        elif kind == 'write_norms':
            valid = (all(_text(line[key]) for key in ('recipe', 'arm', 'mode')) and
                     line['mode'] in ('original', 'fe') and _norms(line['harness_fp32']))
            if 'driver_float64' in line:
                value = line['driver_float64']
                valid = valid and isinstance(value, dict) and all(
                    isinstance(layer, str) and layer.isdecimal() and _number(rho) and rho >= 0.
                    for layer, rho in value.items())
        elif kind == 'target_probs':
            valid = _text(line['table']) and _target_values(line['table'], line['values'])
        elif kind == 'logit_lens':
            valid = _text(line['where']) and _lens(line['layers'], line['items'])
        elif kind == 'answer':
            valid = (all(_text(line[key]) for key in ('recipe', 'arm', 'phase', 'subj', 'val', 'template', 'prompt')) and
                     isinstance(line['text'], str) and _ids(line['target_ids']) and _ids(line['generated_ids']) and
                     type(line['full']) is bool and type(line['first']) is bool and
                     len(line['target_ids']) == len(line['generated_ids']) and
                     line['template'].count('{}') == 1)
            if valid:
                try:
                    valid = line['template'].format(line['subj']) == line['prompt']
                except (IndexError, KeyError, ValueError):
                    valid = False
            if valid:
                if (line['full'] != (line['generated_ids'] == line['target_ids']) or
                        line['first'] != (line['generated_ids'][0] == line['target_ids'][0])):
                    causes.add('MISMATCH')
        if not valid:
            causes.add('MALFORMED')
    return [cause for cause in CAUSES if cause in causes]


def audit_lines(lines, expected, disabled=False):
    """T11: report every failure without changing a scientific record."""
    if type(disabled) is not bool or not isinstance(expected, dict):
        raise ValueError('audit inputs must be an expected-key map and a bool disabled flag')
    for key, flags in expected.items():
        if not (isinstance(key, tuple) and len(key) == 4 and all(_text(x) for x in key) and
                isinstance(flags, (tuple, list)) and len(flags) == 2 and all(type(x) is bool for x in flags)):
            raise ValueError('malformed expected answer key or flags')
    causes, seen = set(), set()
    header, header_count, any_line = None, 0, False
    for index, raw in enumerate(lines):
        any_line = True
        try:
            line = strict_json(raw) if isinstance(raw, (str, bytes, bytearray)) else raw
        except (TypeError, ValueError, UnicodeError):
            causes.add('MALFORMED')
            continue
        schema = line_causes(line)
        causes.update(schema)
        if not isinstance(line, dict):
            continue
        if line.get('kind') == 'header':
            header_count += 1
            if index != 0 or header_count != 1:
                causes.add('MALFORMED')
            if not schema and header is None:
                header = line
            continue
        if header is not None and (line.get('process'), line.get('run_id')) != (header['process'], header['run_id']):
            causes.add('UNEXPECTED')
        if line.get('kind') != 'answer' or 'MALFORMED' in schema or 'UNEXPECTED' in schema:
            continue
        key = tuple(line[field] for field in ('recipe', 'arm', 'subj', 'template'))
        if key in seen:
            causes.add('DUPLICATE')
        seen.add(key)
        if key not in expected:
            causes.add('UNEXPECTED')
        elif (line['full'], line['first']) != tuple(expected[key]):
            causes.add('MISMATCH')
    if header_count != 1 or header is None:
        if not (disabled and not any_line):
            causes.add('MALFORMED')
    missing = set(expected) - seen
    if missing:
        causes.add('DISABLED' if disabled else 'MISSING')
    if disabled:
        causes.add('DISABLED')
    ordered = [cause for cause in CAUSES if cause in causes]
    return {'verdict': 'FAIL' if ordered else 'PASS', 'causes': ordered,
            'rerun_required': bool(causes - {'DISABLED'}),
            'expected_answers': len(expected), 'observed_answers': len(seen),
            'missing_keys': [list(key) for key in sorted(missing)]}


def _weight_hashes(H, hp):
    import c10x_enginepath_inertness as I
    if list(hp.layers) != [4, 5, 6, 7, 8]:
        raise ValueError('telemetry check requires the frozen five-layer band')
    parameters = dict(H.model.named_parameters())
    return {str(layer): I.tensor_sha(parameters[H.weight_name(hp, layer)]) for layer in hp.layers}


def _run(out, H, fingerprint):
    A = _driver()
    if fingerprint.get('ok') is not True:
        raise ValueError('telemetry check requires successful fingerprint preflight')
    if getattr(A, 'H', None) is not H or H.my_edit is not A.dispatch:
        A.configure(H)
    hp = H.hp if hasattr(H, 'hp') else H.MEMITHyperParams.from_json(H.HP_BASE)
    started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    sources, env = A.source_hashes(), A.environment_identity()
    before = _weight_hashes(H, hp)
    result = dict(A.telemetry_mps_inertness_check(H, hp, out, uuid.uuid4().hex))
    after = _weight_hashes(H, hp)
    unchanged = before == after
    invalid = []
    if not unchanged:
        invalid.append('WEIGHT_MISMATCH')
    if A.source_hashes() != sources:
        invalid.append('SOURCE_DRIFT')
    if invalid:
        result['verdict'] = 'INVALID'
        result['invalid_causes'] = invalid
    result.update(schema='c10x_enginepath_telemetry_inertness/v1',
                  decision_id='D-C10r-rulings-11', device=str(H.DEV),
                  weights_unchanged=unchanged, sources=sources, env=env,
                  started_at=started_at, finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  scope=SCOPE)
    if result.get('verdict') not in ('INERT', 'NOT-INERT', 'NONDETERMINISTIC-BASELINE', 'INVALID'):
        raise ValueError('unexpected telemetry inertness verdict')
    A.write_json(out/'inertness.json', result)
    return result


def run(out, H):
    """Injected H bypasses model loading only; launch preflights still apply."""
    A = _driver()
    out = validate_out(out)
    A.environment_preflight()
    fingerprint = A.fingerprint()
    return _run(out, H, fingerprint)


def _expected_answers(pass1, run_record):
    if not isinstance(pass1, dict) or not isinstance(run_record.get('identity'), dict):
        raise ValueError('malformed pass1 or run identity')
    for key in ('process', 'run_id'):
        if key in pass1 and pass1[key] != run_record[key]:
            raise ValueError('pass1/run process identity mismatch')
    templates = run_record['identity'].get('templates', {'CANON': CANON, 'PTEST': PTEST})
    if not isinstance(templates, dict) or set(templates) != {'CANON', 'PTEST'}:
        raise ValueError('malformed recorded templates')
    canon, ptest = templates['CANON'], templates['PTEST']
    if not (_text(canon) and isinstance(ptest, list) and len(ptest) == 3 and
            all(_text(x) for x in ptest) and len(set([canon]+ptest)) == 4 and
            all(x.count('{}') == 1 for x in [canon]+ptest)):
        raise ValueError('malformed recorded canonical or held-out templates')
    recipes = pass1['recipes']
    if not isinstance(recipes, dict) or not recipes:
        raise ValueError('no scored recipes in pass1.json')
    expected = {}
    for recipe, record in recipes.items():
        if recipe not in ('A', 'I-2', 'I-1') or not isinstance(record, dict):
            raise ValueError('unexpected scored recipe')
        arms, detail = record['arms'], record['detail']
        if not isinstance(arms, dict) or not arms or not isinstance(detail, dict) or set(arms) != set(detail):
            raise ValueError('scored arm/detail membership mismatch')
        for arm, rows in detail.items():
            if arm not in ARM_NAMES or not isinstance(rows, list) or len(rows) != 24:
                raise ValueError('expected 24 detail rows per evaluated arm')
            for row in rows:
                if not isinstance(row, dict) or not _text(row.get('subj')) or not _text(row.get('val')):
                    raise ValueError('malformed detail attribution')
                flags = [(row['canon_full'], row['canon_first'])]
                para_full, para_first = row['para_full_hits'], row['para_first_hits']
                if not (isinstance(para_full, list) and isinstance(para_first, list) and
                        len(para_full) == len(para_first) == 3):
                    raise ValueError('expected three held-out flag pairs')
                flags.extend(zip(para_full, para_first))
                for template, pair in zip([canon]+ptest, flags):
                    key = (recipe, arm, row['subj'], template)
                    if key in expected or not all(type(value) is bool for value in pair):
                        raise ValueError('duplicate detail key or non-bool scored flags')
                    expected[key] = tuple(pair)
    return expected


def audit(out):
    """Only this entry point reads telemetry; the scientific reader never does."""
    A = _driver()
    out = Path(out)
    root = Path(A.ROOT).resolve()
    A.selftest_root(root)
    if not out.is_absolute():
        raise ValueError('audit out must be absolute')
    out = out.resolve()
    if root not in out.parents or out.parent != (root/'results').resolve() or re.fullmatch(r'c10x_enginepath(?:_r2)?(?:_rerun[1-9][0-9]*)?', out.name) is None:
        raise ValueError('audit out must name a frozen attempt or T12 re-run directory')
    destination = out/'telemetry/audit.json'
    if destination.parent.resolve().parent != out:
        raise ValueError('audit telemetry directory must resolve directly under out')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(str(destination))
    run_record = strict_json((out/'run.json').read_bytes())
    if not isinstance(run_record, dict) or run_record.get('telemetry') is not True:
        raise ValueError('T11 audit requires a telemetry-on run record')
    process, run_id = run_record.get('process'), run_record.get('run_id')
    if type(process) is not int or process not in (1, 2) or not _text(run_id):
        raise ValueError('malformed run process identity')
    expected = _expected_answers(strict_json((out/'pass1.json').read_bytes()), run_record)
    path = out/'telemetry'/('telemetry_p'+str(process)+'.jsonl')
    lines = path.read_bytes().splitlines() if path.exists() else []
    log = root/'results'/(out.name+'_logs')/'process.log'
    disabled = log.exists() and any(line.startswith(DISABLED_MARKER.encode()) for line in log.read_bytes().splitlines())
    result = audit_lines(lines, expected, disabled=disabled)
    for raw in lines:
        try:
            line = strict_json(raw)
        except (TypeError, ValueError, UnicodeError):
            continue
        if isinstance(line, dict) and (line.get('process'), line.get('run_id')) != (process, run_id):
            result['verdict'] = 'FAIL'
            result['causes'] = [cause for cause in CAUSES if cause in set(result['causes']) | {'UNEXPECTED'}]
            result['rerun_required'] = True
    result.update(schema='c10x_enginepath_telemetry_audit/v1', process=process, run_id=run_id)
    A.write_json(destination, result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', nargs='?', choices=('audit',))
    parser.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    if args.command == 'audit':
        result = audit(args.out)
        return 0 if result['verdict'] == 'PASS' else 1
    A = _driver()
    out = validate_out(args.out)
    A.environment_preflight()
    fingerprint = A.fingerprint()
    import c10e_bandknob as H
    if str(H.DEV) != 'mps':
        raise ValueError('T8 live check requires MPS')
    result = _run(out, H, fingerprint)
    return 0 if result['weights_unchanged'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
