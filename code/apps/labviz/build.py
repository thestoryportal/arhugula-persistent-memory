#!/usr/bin/env python3
"""Build Lab View from recorded evidence only; no model code is imported."""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
from datetime import datetime, timezone

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
MISSING = 'not recorded for this run'
CATALOG = json.loads((PACKAGE / 'models.json').read_text())
SKIP = {'identity', 'fingerprint', 'source_sha256', 'provenance', 'frozen_parameter_hashes_before',
        'frozen_parameter_hashes_after', 'stimulus', 'ctx', 'admission', 'hparams', 'config',
        'base_report', 'projector', 'source', 'engine', 'tokenizer', 'vocab', 'merges'}
COUNT_KEYS = ('para_full_binding_n', 'para_full_n', 'canon_full_n')
PERCENT_KEYS = ('para_full', 'para_full_match', 'canon_full_match')
TABLE_KEYS = {'records', 'rows', 'per_unit', 'per_fact', 'fb_rows', 'per_layer', 'committed_detail', 'facts',
              'secrets', 'trajectory', 'recon_landed', 'recon_dropped', 'bleed_contrast'}
RUN_TABLE_KEYS = {'per_run', 'cells', 'rungs', 'curve', 'sweep', 'ladder'}
def plain_trial(source):
    return 'Recorded observation'


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def model_names(text):
    text = str(text)
    names = []
    for name in sorted(CATALOG, key=len, reverse=True):
        pattern = re.escape(name).replace(r'\-', '[- /]?')
        if re.search(pattern + r'(?![\w.-])', text, re.I):
            names.append(name)
    if 'Qwen2.5-0.5B-Instruct' in names and 'Qwen2.5-0.5B' in names:
        names.remove('Qwen2.5-0.5B')
    return list(dict.fromkeys(names))


def metadata(data, source, root=None, contexts=()):
    """Nearest run/config fields win. Reviewer identities are never searched."""
    model, model_source, layers, layer_source, band = 'model not recorded', None, None, None, []
    candidates = [*reversed(contexts), data] if contexts else [data]
    for node in candidates:
        if not isinstance(node, dict):
            continue
        for key in ('config', 'run', 'recipe', 'summary'):
            sub = node.get(key)
            if isinstance(sub, dict):
                node = {**sub, **node}
        for key in ('hf_id', 'model_id', 'model_name', 'model', 'scope', 'harness'):
            value = node.get(key)
            if isinstance(value, str):
                matches = model_names(value)
                if len(matches) == 1 and model == 'model not recorded':
                    model, model_source = matches[0], f'{source} ({key})'
                elif key in ('hf_id','model_id','model_name','model') and model == 'model not recorded' and value.lower() not in ('3b','7b') and not value.isdecimal():
                    model, model_source = value, f'{source} ({key})'
        for key in ('n_layers', 'num_hidden_layers', 'n_layer'):
            if layers is None and number(node.get(key)) and int(node[key]) == node[key]:
                layers, layer_source = int(node[key]), f'{source} ({key})'
        if not band:
            value = node.get('band', node.get('layers'))
            if isinstance(value, list) and all(isinstance(v, int) for v in value):
                band = value
        hp = node.get('hparams')
        if isinstance(hp, str):
            for name, info in CATALOG.items():
                if any(tag in hp for tag in info['hparams']) and model == 'model not recorded':
                    model, model_source = name, f'{source} → {hp}'
            if root and '/configs/' in hp:
                path = root / ('code/configs/' + hp.split('/configs/', 1)[1])
                if path.is_file() and not band:
                    config = json.loads(path.read_text())
                    band = config.get('layers', [])
            elif root and hp.startswith('code/configs/') and (root / hp).is_file() and not band:
                band = json.loads((root / hp).read_text()).get('layers', [])
    if model != 'model not recorded' and layers is None:
        info = CATALOG.get(model, {})
        layers, layer_source = info.get('layers'), info.get('layer_source')
    return dict(model=model, model_source=model_source, layers=layers, layer_source=layer_source, band=band)


def recorded_stamp(data):
    if isinstance(data, dict):
        for node in (data, data.get('identity', {}), data.get('run', {}), data.get('config', {})):
            if isinstance(node, dict):
                for key in ('when_utc', 'created_utc', 'date', 'started', 'ts'):
                    s = node.get(key)
                    if isinstance(s, str) and re.match(r'2026-\d\d-\d\d', s):
                        return s
    return ''


def date_of(data, source):
    stamp = recorded_stamp(data)
    if stamp:
        return stamp[:10], 'record'
    match = re.search(r'(2026)[-]?(\d\d)[-]?(\d\d)', source)
    return ('-'.join(match.groups()), 'filename') if match else ('', 'date not recorded')


def scalars(data, prefix='', limit=16):
    out = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key in SKIP:
                continue
            label = f'{prefix}.{key}'.strip('.')
            if number(value):
                out.append([label, value])
            elif isinstance(value, (dict, list)):
                out.extend(scalars(value, label, limit))
            if len(out) >= limit:
                break
    elif isinstance(data, list):
        for i, value in enumerate(data):
            if number(value):
                out.append([f'{prefix}[{i}]', value])
            elif isinstance(value, (dict, list)):
                out.extend(scalars(value, f'{prefix}[{i}]', limit))
            if len(out) >= limit:
                break
    return out[:limit]


def curve_data(node):
    curves = []
    if isinstance(node, list):
        for row in node:
            if isinstance(row, dict):
                p = row.get('probs')
                if isinstance(p, list) and p and all(number(v) and 0 <= v <= 1 for v in p):
                    curves.append({'label': str(row.get('subj', row.get('subject', 'recorded fact'))), 'probs': p})
    return curves


def make_run(node, source, field, data, contexts=(), root=None, rows=None, schema='harness'):
    date, date_kind = date_of(data, source)
    counts = next((node[k] for k in COUNT_KEYS[:2] if number(node.get(k))), None) if isinstance(node, dict) else None
    out_of = node.get('para_n', node.get('masked_binding_prompt_n')) if isinstance(node, dict) else None
    percent = next((node[k] for k in ('para_full', 'para_full_match') if number(node.get(k))), None) if isinstance(node, dict) else None
    if not isinstance(node, dict):
        node = {'recorded_rows': node}
    extra = node.get('extra', {})
    if not isinstance(extra, dict):
        extra = {}
    if rows is None:
        rows = node.get('rows', [])
    from apps.labviz.cards import is_c10
    c10=is_c10(source)
    grid, grid_label = None, 'Reworded questions — free answers' if c10 else 'Recorded free-answer outcomes'
    labels = []
    if isinstance(rows, list) and rows and any(isinstance(r, dict) and 'para_full_hits' in r for r in rows):
        grid = []
        for row in rows:
            vals = row.get('para_full_hits', []) if isinstance(row, dict) else []
            grid.append([(v if isinstance(v, bool) else None) for v in vals])
            labels.append(str(row.get('subject', row.get('subj', len(labels) + 1))))
    elif isinstance(extra.get('per_fact_position_curve'), list):
        grid, grid_label = [], 'Rewordings with supplied earlier pieces (teacher-forced hits)' if c10 else 'Recorded supplied-piece outcomes'
        for row in extra['per_fact_position_curve']:
            grid.append([all(v) if isinstance(v, list) and v and all(isinstance(x, bool) for x in v) else None
                         for v in row.get('per_template_hits', [])])
            labels.append(str(row.get('subj', row.get('subject', len(labels) + 1))))
    axes = node.get('locality_axes', {})
    side = {k: axes.get(k) for k in ('L1_flipped_to_edited_value', 'L1_n', 'L3_top1_agree', 'L3_n',
                                   'generic_ppl_pre', 'generic_ppl_post')}
    side['relation_flips'] = extra.get('relation_flips')
    side['same_frame_flips'] = extra.get('same_frame_flips')
    side['locality_described_as'] = node.get('locality_described_as')
    curves = curve_data(node.get('per_position_curve', extra.get('per_fact_position_curve')))
    writes = {}
    label = field.rsplit('.', 1)[-1]
    if field == 'arm' and isinstance(data.get('recipe'), dict):
        candidate = data['recipe'].get('arms', {}).get('candidate')
        if isinstance(candidate, dict) and all(node.get(k) == candidate.get(k) for k in ('para_full_n','canon_full_n')):
            label = 'candidate'
            contexts = (*contexts, data['recipe'])
    for parent in reversed(contexts):
        delta = parent.get('delta_norms', {}) if isinstance(parent, dict) else {}
        if isinstance(delta, dict) and label in delta and isinstance(delta[label], dict):
            writes = {str(k): v['delta_norm'] for k, v in delta[label].items()
                      if isinstance(v, dict) and number(v.get('delta_norm'))}
            break
    if not writes and isinstance(node.get('rel_delta_norm'), dict):
        # Relative sizes have different units; expose the units explicitly.
        writes = {str(k): v for k, v in node['rel_delta_norm'].items() if number(v)}
    role = next((text for tag,text in [('A1','one ordinary answer word'),('A2','two ordinary answer words'),
                  ('A7','made-up answer names')] if c10 and label.startswith(tag)), None)
    if role is None:
        role = {'mint1':'one new word','mint2':'two new words','modifier':'a new modifier word',
                'multi':'the name in its original pieces'}.get(data.get('kind'), 'saved observation')
    identity = ' · '.join(f'{key} {data[key]}' for key in ('block','replicate','seed') if key in data)
    title = f'{plain_trial(source)} · {role}' + (f' · {identity}' if identity else '')
    table = node.get('recorded_rows', [])
    outcomes = None
    if isinstance(table, list) and table and all(isinstance(row,dict) for row in table):
        cols = list(dict.fromkeys(k for row in table for k,v in row.items() if isinstance(v,bool)))
        if cols:
            outcomes = {'columns': cols, 'values': [[row.get(k) if isinstance(row.get(k),bool) else None for k in cols] for row in table]}
    return dict(id='run-' + digest([source, field])[:16], title=title, source=source, field=field,
                date=date, date_kind=date_kind, schema=schema, score=counts,
                out_of=out_of if number(out_of) else None, percent=percent,
                canonical=node.get('canon_full_n'), canonical_n=node.get('canon_n'),
                grid=grid, grid_label=grid_label, fact_labels=labels, curves=curves,
                losses=[[p['step'], p['loss']] for p in node.get('losses', [])
                        if isinstance(p, dict) and number(p.get('step')) and number(p.get('loss'))],
                side=side, writes=writes, write_units='relative change' if 'rel_delta_norm' in node else 'absolute write norm',
                measurements=scalars(node), outcomes=outcomes, tried=plain_trial(source),
                verdict=str(node.get('outcome', data.get('outcome', data.get('verdict', data.get('status', MISSING)))))[:700],
                **metadata(data, source, root, (*contexts, node)))


def parse_record(data, source, root=None):
    runs = []
    def visit(node, field='', contexts=(), force_arm=False):
        if isinstance(node, dict):
            if node and all(str(k).isdigit() for k in node) and scalars(node):
                runs.append(make_run({'recorded_rows': node}, source, field or 'numeric_key_table',
                                     data if isinstance(data, dict) else {}, contexts, root, schema='recorded-table'))
                return
            has_metrics = any(number(node.get(k)) for k in (*COUNT_KEYS, *PERCENT_KEYS))
            has_curves = bool(curve_data(node.get('per_position_curve')))
            if has_metrics or has_curves or isinstance(node.get('losses'), list):
                parent = contexts[-1] if contexts else {}
                label = field.rsplit('.', 1)[-1]
                detail = parent.get('detail', {})
                if not detail and len(contexts) > 1:
                    detail = contexts[-2].get('detail', {})
                rows = detail.get(label) if isinstance(detail, dict) else None
                schema = 'training' if 'losses' in node else 'reader' if has_curves and not has_metrics else 'harness'
                runs.append(make_run(node, source, field, data if isinstance(data, dict) else {}, contexts, root, rows, schema))
                return
            before = len(runs)
            ordered = sorted(node.items(), key=lambda pair: 0 if pair[0] == 'arm' else 1)
            for key, value in ordered:
                if key in SKIP:
                    continue
                child_field = f'{field}.{key}'.strip('.')
                if key == 'arms_raw' and isinstance(value, dict):
                    for label, arm in value.items():
                        if isinstance(arm, dict) and scalars(arm):
                            runs.append(make_run(arm, source, f'{child_field}.{label}',
                                                 data if isinstance(data, dict) else {}, (*contexts, node), root, schema='numeric-arm'))
                elif key in TABLE_KEYS and isinstance(value, (dict, list)) and value:
                    runs.append(make_run({'recorded_rows': value}, source, child_field,
                                         data if isinstance(data, dict) else {}, (*contexts, node), root, schema='recorded-table'))
                elif key == 'detail' and isinstance(value, dict) and 'arms' not in node:
                    for label, rows in value.items():
                        if isinstance(rows, list) and rows and all(isinstance(row, dict) for row in rows) and any(
                            any(k in row for k in ('subject', 'subj', 'entity', 'fact', 'probe', 'prompt')) for row in rows):
                            runs.append(make_run({'recorded_rows': rows}, source, f'{child_field}.{label}',
                                                 data if isinstance(data, dict) else {}, (*contexts, node), root, schema='recorded-table'))
                elif key in RUN_TABLE_KEYS and isinstance(value,(dict,list)):
                    items = enumerate(value) if isinstance(value,list) else value.items()
                    for k, row in items:
                        if isinstance(row,(dict,list)):
                            runs.append(make_run(row, source, f'{child_field}[{k}]', data if isinstance(data,dict) else {}, (*contexts,node), root, schema='numeric-run'))
                else:
                    visit(value, child_field, (*contexts, node), key == 'arms' or force_arm)
            if force_arm and len(runs) == before and scalars(node):
                runs.append(make_run(node, source, field, data if isinstance(data, dict) else {}, contexts, root, schema='numeric-arm'))
        elif isinstance(node, list):
            if not field and node and all(isinstance(v,dict) for v in node) and any(
                    set(v) & {'subject','subj','entity','fact','probe','prompt','retained_at_end','correct'} for v in node):
                runs.append(make_run({'recorded_rows': node},source,'records',{},root=root,schema='recorded-table'))
                return
            for i, value in enumerate(node):
                visit(value, f'{field}[{i}]', contexts, force_arm)
    visit(data)
    return runs


HARNESS = re.compile(r'(\S+)\s+.*?n:\s*canon\s+(\d+)/(\d+)\s+para\s+(\d+)/(\d+)')
LOSS = re.compile(r'\bstep\s+(\d+)\s+loss\s+([\d.eE+\-]+)', re.I)


def parse_log(text, source):
    observations, losses = [], []
    for lineno, line in enumerate(text.splitlines(), 1):
        loss = LOSS.search(line)
        if loss:
            value = float(loss[2])
            if math.isfinite(value):
                losses.append([int(loss[1]), value])
        hit = HARNESS.search(line)
        if hit:
            arm, c, cn, p, pn = hit.groups()
            r = make_run({'canon_full_n': int(c), 'canon_n': int(cn), 'para_full_n': int(p), 'para_n': int(pn)},
                         source, f'line {lineno} {arm}', {})
            side = re.search(r'L1\s+(\d+)/(\d+)\s+L3\s+(\d+)/(\d+)', line)
            ppl = re.search(r'ppl\s+([\d.]+)->([\d.]+)', line)
            if side:
                for key, v in zip(('L1_flipped_to_edited_value','L1_n','L3_top1_agree','L3_n'), side.groups()):
                    r['side'][key] = int(v)
            if ppl:
                r['side'].update(generic_ppl_pre=float(ppl[1]), generic_ppl_post=float(ppl[2]))
            observations.append(r)
    terminal = bool(re.search(r'(?:HALTED|FATAL|Traceback|RUN_DONE|BEHAVIOR_DONE|STAGE_DONE|TRAIN_DONE|P[12]_DONE|\bCOMPLETE\b|no behavioral run)', text[-5000:]))
    return dict(source=source, losses=losses, observations=observations, running=not terminal and bool(text.strip()),
                terminal=terminal, last_line=text.splitlines()[-1][:350] if text.splitlines() else 'empty log')


def seed_evaluations(scoreboard):
    entries = []
    for i, row in enumerate(scoreboard['results']):
        entries.append(dict(id=f'evaluation-{i}', source_result=row, question=f'Would this help: {row["name"]}?',
                            result=f'{row["score"]}. {row["verdict"]}',
                            rules_out=f'The recorded limit: {row["verdict"]}. This applies to the tested setup.',
                            leaves_open='A general solution is not established by this row; different setups and repeat runs remain open.',
                            next_step='A next step for this individual result is not recorded in the scoreboard results.', ref=row['ref']))
    return {'source': 'program/registers/c10_scoreboard.json results only', 'entries': entries}


def corpus_cards(root):
    cards = []
    for p in sorted((root / 'evidence/CORPUS').glob('[0-9][0-9]_*.md')):
        s = p.read_text()
        title = next((x.lstrip('# ').strip() for x in s.splitlines() if x.startswith('#')), p.stem)
        lines = s.splitlines()
        verdict = next((x.strip('# *_') for x in lines if re.match(r'^#{1,3}\s+(?:NET\s+)?VERDICT', x, re.I)), None)
        if not verdict:
            verdict = next((x.strip('* ') for x in lines[:120] if re.match(r'^\*\*(?:NET\s+)?VERDICT[: (]', x, re.I)), MISSING)
        date = re.search(r'2026-\d\d-\d\d', s[:4000])
        models = model_names(s[:4000])
        ids = re.findall(r'D-[A-Za-z0-9][A-Za-z0-9_-]*', s[:5000])
        run = make_run({}, str(p.relative_to(root)), 'verdict', {})
        run.update(title=title, verdict=verdict[:1000], date=date[0] if date else '', date_kind='CORPUS header' if date else 'date not recorded',
                   schema='CORPUS verdict', models=models, decision_ids=list(dict.fromkeys(ids)))
        if len(models) == 1:
            name = models[0]; run.update(model=name, model_source=run['source'], layers=CATALOG[name]['layers'], layer_source=CATALOG[name]['layer_source'])
        run['summary_only'] = True
        cards.append(run)
    return cards


def collect(root=ROOT):
    root = Path(root)
    board = json.loads((root / 'program/registers/c10_scoreboard.json').read_text())
    corpus = corpus_cards(root)
    from apps.labviz.cards import run_files
    paths = run_files(root)
    # Run folders first, then the folders inside them.
    survey = {}
    for depth in (4, None):
        for p in paths:
            rel = p.relative_to(root)
            if (depth is None or len(rel.parts) == depth) and p.is_dir() and not p.is_symlink() and 'labviz' not in rel.parts:
                survey.setdefault(str(rel), dict(files=0, runs=0, unsupported=[], unreadable=[], logs=0))
    runs, logs, ordering = [], [], {}
    for p in paths:
        rel = p.relative_to(root)
        if p.is_symlink() or not p.is_file() or 'labviz' in rel.parts or any('tokenizer' in x or 'c10z_' in x for x in rel.parts):
            continue
        from apps.labviz.cards import recorded
        if not recorded(str(rel)): continue
        if p.suffix not in ('.json', '.jsonl', '.log', '.tsv', '.csv'):
            continue
        folder = str(Path(*rel.parts[:4]))
        if folder not in survey:
            continue
        info = survey[folder]; info['files'] += 1; source = str(rel)
        if p.suffix == '.log':
            log = parse_log(p.read_text(errors='replace'), source)
            log['modified_utc'] = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat()
            logs.append(log); info['logs'] += 1
            # Raw per-observation log snapshots stay distinct from JSON snapshots.
            for r in log['observations']:
                r['schema'] = 'log observation'
            found = log['observations']
            if log['losses']:
                found.append(make_run({'losses': [dict(step=s, loss=v) for s,v in log['losses']]}, source, 'training loss', {}, schema='training-log'))
            for i,r in enumerate(found):
                r.update(date=log['modified_utc'][:10],date_kind='log modification time')
                ordering[r['id']] = (log['modified_utc'],i)
        elif p.suffix == '.json':
            try:
                data = json.loads(p.read_text())
            except (ValueError, UnicodeError) as e:
                info['unreadable'].append(dict(path=source, reason=str(e))); continue
            found = parse_record(data, source, root)
            if not found:
                info['unsupported'].append(dict(path=source, keys=list(data)[:18] if isinstance(data, dict) else type(data).__name__))
            for r in found:
                if r['model'] == 'model not recorded':
                    ids = [data.get('decision_id')] if isinstance(data, dict) else []
                    matching = [c for c in corpus if any(i in c['decision_ids'] for i in ids if i)]
                    names = {c['model'] for c in matching if c['model'] != 'model not recorded'}
                    if len(names) == 1:
                        name = names.pop(); r.update(model=name, model_source=matching[0]['source'], layers=CATALOG[name]['layers'], layer_source=CATALOG[name]['layer_source'])
                if not r['date']:
                    ids = [data.get('decision_id')] if isinstance(data, dict) else []
                    matching = [c for c in corpus if any(i in c['decision_ids'] for i in ids if i)]
                    if matching:
                        r.update(date=matching[0]['date'], date_kind='linked CORPUS date')
        else:
            info['unsupported'].append(dict(path=source, keys=f'{p.suffix} table not interpreted')); found = []
        info['runs'] += len(found); runs.extend(found)
        if p.suffix == '.json':
            for i,r in enumerate(found):
                ordering[r['id']] = (recorded_stamp(data) or r['date'],i)
        for ancestor in p.parents:
            if ancestor == root / Path(*rel.parts[:3]):
                break
            name = str(ancestor.relative_to(root))
            if name in survey and name != folder:
                nested = survey[name]; nested['files'] += 1; nested['runs'] += len(found)
                if p.suffix == '.log': nested['logs'] += 1
    history = []
    for i, row in enumerate(board['results']):
        r = make_run({}, 'program/registers/c10_scoreboard.json', f'results[{i}]', {})
        r.update(title=row['name'], date=row['date'], date_kind='scoreboard', score=row.get('best'), out_of=board.get('out_of', 72),
                 verdict=row['verdict'], schema='scoreboard summary', kind=row['kind'], ref=row['ref'], score_label=row['score'], summary_only=True)
        refs = re.findall(r'evidence/CORPUS/(\d+)', row['ref'])
        linked = [c for c in corpus if any(Path(c['source']).name.startswith(n + '_') for n in refs)]
        models = {c['model'] for c in linked if c['model'] != 'model not recorded'}
        if len(models) == 1:
            name = models.pop(); r.update(model=name, model_source=linked[0]['source'], layers=CATALOG[name]['layers'], layer_source=CATALOG[name]['layer_source'])
        history.append(r)
    historical_models = []
    for name, info in CATALOG.items():
        if info['status'] != 'tested earlier' or not (root / info['note_source']).is_file():
            continue
        source = info['note_source']; text = (root / source).read_text()
        close_date = re.search(r'close (2026-\d\d-\d\d)', text)
        r = make_run({}, source, name, {})
        r.update(title=f'Earlier model branch · {name}', model=name, model_source=source,
                 layers=info['layers'], layer_source=info['layer_source'],
                 date=close_date[1] if close_date else '', date_kind='decision closeout; run may be earlier',
                 schema='historical model note', verdict=info['note'], summary_only=True)
        historical_models.append(r)
    runs.extend(historical_models)
    runs.extend(corpus); runs.extend(history)
    # Logs inherit a model only when their folder's observed JSON records agree.
    for r in runs:
        if r['schema'] in ('log observation', 'training-log') and r['model'] == 'model not recorded':
            parent = Path(r['source']).parent
            match = [x for x in runs if x['schema'] not in ('log observation','training-log')
                     and parent in Path(x['source']).parents and x['model'] != 'model not recorded']
            names = {x['model'] for x in match}
            if len(names) == 1:
                name = names.pop(); r.update(model=name, model_source=match[0]['model_source'], layers=match[0]['layers'], layer_source=match[0]['layer_source'])
    runs.sort(key=lambda r: (r['date'], *ordering.get(r['id'],(r['date'],0)), r['source'], r['field']), reverse=True)
    catalog = {}
    names = list(CATALOG) + sorted({r['model'] for r in runs if r['model'] != 'model not recorded'} - set(CATALOG))
    for name in names:
        observations = [r for r in runs if r['model'] == name]
        info = CATALOG[name] if name in CATALOG else {'size': 'parameter count not recorded', 'layers': observations[0]['layers'],
            'layer_source': observations[0]['layer_source'], 'status': 'recorded model name',
            'sources': sorted({r['source'] for r in observations}), 'hparams': [],
            'note': 'A reason for moving on is not recorded in the parsed metadata.', 'note_source': observations[0]['source']}
        summaries = [r for r in history if r['model'] == name]
        catalog[name] = {**info, 'name': name, 'runs': len(observations),
                         'dates': sorted({r['date'] for r in observations if r['date']}),
                         'tests': sorted({r['tried'] for r in observations if not r.get('summary_only')})}
    newest = max(logs, key=lambda l: l['modified_utc'], default=None)
    return dict(runs=runs, survey=survey, corpus=corpus, history=history, historical_models=historical_models,
                scoreboard=board, models=catalog, logs=logs, newest_log=newest)


def write_if_changed(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    value = content.encode() if isinstance(content, str) else content
    if not path.exists() or path.read_bytes() != value:
        temporary = path.with_suffix(path.suffix + '.tmp')
        temporary.write_bytes(value); temporary.replace(path)


def build(root=ROOT):
    os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/labviz-mpl')
    from apps.labviz.cards import Reader, encoded, newest_written, citations, run_files, run_path
    from state import llmdb_records as L
    from apps.labviz.render import card_picture, render_page
    root = Path(root); reader = Reader(root); cards = reader.collect()
    base = root / 'projects/labviz-spec-v3/receipts/bulk/labviz'; site = base / 'site'; images = base / 'runs'
    site.mkdir(parents=True, exist_ok=True); images.mkdir(parents=True, exist_ok=True)
    old_index_path = site/'cards/index.json'
    old_index = json.loads(old_index_path.read_text()) if old_index_path.is_file() else []
    ep = root / 'program/registers/c10_evaluations.json'
    evaluations = json.loads(ep.read_text()) if ep.is_file() else {'entries':[]}
    cache_path = base / 'images_manifest.json'
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    renderer_hash = hashlib.sha256((PACKAGE / 'render.py').read_bytes()).hexdigest()
    index=[]; chunks={}; manifest={}; picture_calls=0; pictures=[]
    for card in cards:
        identifier=card['card_id']; identity=card['identity']; context=card['context']
        question=context.get('question',{}).get('value') or 'Recorded observation'
        line=context.get('experiment',{}).get('node_id') or context.get('corpus',{}).get('node_id') or 'unknown'
        era=context.get('era',{}).get('value') or 'unknown'
        chunk='line-'+digest([line])[:12]
        chunks.setdefault(chunk,[]).append(card)
        recipe=identity.get('recipe'); arm=identity.get('arm')
        recipe=recipe.get('value') if isinstance(recipe,dict) else recipe
        arm=arm.get('value') if isinstance(arm,dict) else arm
        row={'card_id':identifier,'source':identity['name'],'field':identity['field'],'experiment':context.get('experiment',{}).get('value'),
             'era':era,'line':line,'model':identity['model']['value'],'role':identity.get('role',{}).get('value'),
             'label':card['label']['value'],'date':identity['date']['value'],'has_writes':any(x['written']['value'] for x in card.get('per_layer',[])),
             'title':identity.get('display_title',{}).get('value') or question,'recipe':str(recipe) if recipe is not None else None,'arm':str(arm) if arm is not None else None,'chunk':chunk}
        if 'mathlab' in card:
            state=card['mathlab']['state']['value']
            row['mathlab']={'tier':card['evidence_status'],'run_id':state['run_id'],'status':state['status'],
                           'purpose':state['purpose'],'parse_errors':len(card['mathlab']['errors']['value'])}
        index.append(row)
        write_if_changed(site/'cards'/f'{identifier}.json',encoded(card))
        if run_path(identity['name']) is not None and 'mathlab' not in card:
            visual={k:card[k] for k in ('identity','context','headline','label','per_fact','per_layer','scale','oracle_class') if k in card}
            key=digest([visual,renderer_hash]); output=images/identifier
            previous=cache.get(identifier,{})
            if not isinstance(previous,dict) or previous.get('key')!=key or not output.with_suffix('.svg').is_file() or not output.with_suffix('.png').is_file():
                previous=card_picture(card,output); previous['key']=key; picture_calls+=1
            manifest[identifier]=previous
            pictures.append({'id':identifier,'title':question})
    for chunk,items in sorted(chunks.items()):
        script='window.LAB_CHUNKS=window.LAB_CHUNKS||{};window.LAB_CHUNKS['+json.dumps(chunk)+']='+encoded(items).decode().replace('</',r'<\/')+';\n'
        write_if_changed(site/'cards'/f'{chunk}.js',script)
    write_if_changed(site/'cards/index.json',encoded(index))
    write_if_changed(site/'cards/scales.json',encoded(reader.scales))
    write_if_changed(site/'context.json',encoded({'graph':reader.program.graph,'contexts':reader.program.tables}))
    link = site / 'runs'
    if not link.exists():
        link.symlink_to('../runs', target_is_directory=True)
    for name in ('style.css', 'app.js', 'model.js'):
        write_if_changed(site / name, (PACKAGE / name).read_bytes())
    models={name:{k:v for k,v in info.items() if k in ('size','status','note','note_source')} for name,info in CATALOG.items()}
    models['Qwen2.5-3B']['note']='Used across several lines; each result retains its own question and measure.'
    logs=[]
    for path in run_files(root):
        relative=str(path.relative_to(root))
        if path.suffix=='.log' and (not reader.program._real_program or not run_path(relative).startswith('c10z')):
            from apps.labviz.cards import recorded
            if recorded(relative):
                lines=path.read_text(errors='replace').splitlines()
                if lines: logs.append((path.stat().st_mtime_ns,{'source':relative,'last_line':lines[-1][:350]}))
    latest=max(logs,key=lambda x:(x[0],x[1]['source']))[1] if logs else {}
    if latest: latest['caption']='latest selected log snapshot; no liveness inferred'
    board_path=root/'program/registers/c10_scoreboard.json'
    board=json.loads(board_path.read_text()) if board_path.is_file() else {}
    queue=board.get('queue',[])
    questions=[]; question_index={}; compact_index=[]
    for row in index:
        title=row['title']
        if title not in question_index: question_index[title]=len(questions); questions.append(title)
        compact={k:v for k,v in row.items() if k!='title' and v is not None}
        compact['title_ref']=question_index[title]; compact_index.append(compact)
    index_script='window.LAB.index='+encoded(compact_index).decode().replace('</',r'<\/')+';\nwindow.LAB.index.forEach(function(row){row.title=window.LAB.questions[row.title_ref];});\n'
    write_if_changed(site/'cards/index.js',index_script)
    index_counts={node['node_id']:sum(row['line']==node['node_id'] or 'exp:'+str(row['experiment'])==node['node_id']
                               or row['era']==node['node_id'] or row['era']==node['node_id'].removeprefix('era:')
                               or row['model']==node['node_id'].removeprefix('model:') for row in index)
                  for node in reader.program.graph['nodes']}
    display_evaluations=[]
    for entry in evaluations['entries']:
        row=entry.get('source_result',{})
        templates={'question':f'Would this help: {row.get("name")}?',
                   'rules_out':f'The recorded limit: {row.get("verdict")}. This applies to the tested setup.',
                   'leaves_open':'A general solution is not established by this row; different setups and repeat runs remain open.',
                   'next_step':'A next step for this individual result is not recorded in the scoreboard results.'}
        numbers=set(re.findall(r'evidence/CORPUS/(\d{2})',entry.get('ref','')))
        matches=[record['id'] for record in reader.program.registry if numbers.intersection(record['corpus'])]
        line='exp:'+matches[0] if len(matches)==1 else 'corpus:'+next(iter(numbers)) if len(numbers)==1 else 'unassigned'
        framing=reader.program.tables.get('experiments',{}).get(matches[0],{}) if len(matches)==1 else {}
        display_evaluations.append({**entry,'template_fields':[key for key,value in templates.items() if entry.get(key)==value],
                                   'line':line,'era':framing.get('era','unknown')})
    payload={'graph':reader.program.graph,'index':[],'index_src':'cards/index.js','index_counts':index_counts,'questions':questions,'contexts':{'eras':reader.program.tables.get('eras',{})},'models':models,
             'default_run':newest_written(cards) or (index[0]['card_id'] if index else None),'latest_log':latest,'queue':queue,'evaluations':display_evaluations}
    script='window.LAB='+encoded(payload).decode().replace('</',r'<\/')+';\n'
    write_if_changed(site/'data.js',script)
    inventory={'runs':pictures,'history':[],'models':models,'survey':reader.survey,'cards':cards,'picture_calls':picture_calls}
    write_if_changed(site/'index.html',render_page(inventory,evaluations))
    write_if_changed(base/'survey.json',encoded(reader.survey))
    write_if_changed(base/'models.json',encoded(models))
    write_if_changed(cache_path,encoded(manifest))
    # Serve only explicitly cited evidence snapshots, never the workspace tree.
    paths=set(reader.files)|{x for card in cards for x in citations(card)}|{'program/registers/c10_scoreboard.json','program/registers/c10_evaluations.json'}
    paths.update(item['file'] for card in cards for item in card.get('sources',[]))
    paths.update(citations(reader.program.graph))
    paths.update(p['file'] for operand in reader.scales['absolute_write_size']['operands'] for p in [operand['src']])
    for source in sorted(paths):
        p = root / source
        if source.startswith('projects/labviz-spec-v3/receipts/bulk/labviz/'): continue
        if source.startswith('data/hf_cache/') and source != 'data/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json': continue
        if p.is_file() and (p.suffix in ('.json','.jsonl','.md','.log') or source=='code/apps/mathlab/mathlab_events.py'):
            content = reader.snapshots[source] if source in reader.snapshots else p.read_bytes()
            write_if_changed(site / 'evidence' / source, content)
    # Retire generic MathLab publications without changing their source artifacts.
    active = {row['card_id'] for row in index}
    retired = [row for row in old_index if row['source'].startswith(('results/mathlab/','results/mathlab_staging/'))
               and row['card_id'] not in active]
    for row in retired:
        (site/'cards'/f"{row['card_id']}.json").unlink(missing_ok=True)
        for suffix in ('.svg','.png'):
            (images/row['card_id']).with_suffix(suffix).unlink(missing_ok=True)
    for chunk in {row['chunk'] for row in retired} - chunks.keys():
        (site/'cards'/f'{chunk}.js').unlink(missing_ok=True)
    # MathLab records publish only cited streams and findings: their pre-v2 folders, then the v2 lab records.
    for family in ('results/mathlab','results/mathlab_staging',*L.LAB_RUNS):
        for path in (site/'evidence'/family).rglob('*'):
            if path.is_file() and path.relative_to(site/'evidence').as_posix() not in paths:
                path.unlink()
    print(f'Lab View picture renderer calls: {picture_calls}',flush=True)
    return inventory


if __name__ == '__main__':
    import resource
    import time
    started=time.perf_counter()
    sys.path.insert(0, str(ROOT / "code"))
    inventory = build()
    print(f'Lab View: {len(inventory["runs"])} cards, {len(inventory["survey"])} surveyed folders/groups; projects/labviz-spec-v3/receipts/bulk/labviz/site/index.html')
    print(f'Build measurement: {time.perf_counter()-started:.6f} seconds; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss} bytes on {sys.platform}')
