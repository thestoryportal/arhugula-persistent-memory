"""Typed, source-bound recorded observations. No scientific reader is executed."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re

PACKAGE = Path(__file__).resolve().parent
CONFIG = 'hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json'
REVISION = '3aab1f1954e9cc14eb9509a215f9e5ca08227a9b'
HPARAMS = 'configs/hparams/qwen25_3b_memit_hparams.json'
POPULATION = 'results/labviz/site/cards/scales.json'
STRUCTURAL = set('schema card_id evidence_status built sources family field recipe arm index layer node_id edge matched_by population structural unit name plain comparison judgement hit_kind colour_class colour_table reader_rules'.split())


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def path_of(parts):
    out = '.'
    for key in parts:
        if isinstance(key, int):
            out += f'[{key}]'
        elif re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key):
            out += ('' if out == '.' else '.') + key
        else:
            out += '[' + json.dumps(key, ensure_ascii=False) + ']'
    return out


def path_parts(path):
    if not isinstance(path, str) or not path.startswith('.'):
        raise ValueError('invalid source path')
    pos = 1; parts = []
    if pos < len(path) and re.match(r'[A-Za-z_]', path[pos]):
        match = re.match(r'[A-Za-z_][A-Za-z0-9_]*', path[pos:]); parts.append(match[0]); pos += len(match[0])
    while pos < len(path):
        match = re.match(r'\.([A-Za-z_][A-Za-z0-9_]*)|\[(\d+)\]', path[pos:])
        if match:
            parts.append(match[1] if match[1] is not None else int(match[2])); pos += len(match[0]); continue
        if path.startswith('["', pos):
            key, end = json.JSONDecoder().raw_decode(path[pos+1:])
            if not isinstance(key, str) or path[pos+1+end:pos+2+end] != ']':
                raise ValueError('invalid quoted key')
            parts.append(key); pos += end+2; continue
        raise ValueError('unsupported source path: '+path)
    return parts


def resolve(data, path):
    for key in path_parts(path):
        data = data[key]
    return data


def missing(reason='not recorded for this run', tier='NOW-not-recorded'):
    return dict(value=None, missing=reason, tier=tier)


def leaf(value, file, path):
    return dict(value=value, src=dict(file=file, path=path))


def doc(value, file, line, quote):
    return dict(value=value, src=dict(file=file, line=line, quote=quote))


def derived(rule, inputs, **metadata):
    result = dict(value=recompute(rule, [x['value'] for x in inputs]), derived=rule,
                  inputs=inputs, rule_src={'spec':'§6'}, **metadata)
    return result


def recompute(rule, values):
    arities={'add':2,'in-band':2,'written':1,'teacher-hits':1,'rounded-rise':3,
             'paired-loss':2,'frame-values':2,'map-add':2,'all-le':2,'minted-value':2,
             'replica-note':3,'context-section':3,'context-condition':5,'context-layer':5}
    if rule in arities and len(values) != arities[rule]:
        raise ValueError('missing operand: '+rule)
    if rule == 'add': return values[0]+values[1]
    if rule == 'in-band': return values[1] in values[0]
    if rule == 'written': return finite(values[0])
    if rule == 'teacher-hits': return [all(row) if row and all(isinstance(x,bool) for x in row) else None for row in values[0]]
    if rule == 'rounded-rise': return round(values[1],values[2])-round(values[0],values[2])
    if rule == 'paired-loss': return sum(values[0])-sum(values[1])
    if rule == 'frame-values': return [values[0]]+[x['flips'] for x in values[1]]
    if rule == 'map-add': return [v+values[1] for v in values[0]]
    if rule == 'all-le': return all(x<=y for x,y in zip(values[0],values[1])) and len(values[0])==len(values[1])
    if rule == 'minted-value': return [values[0],values[1]]
    if rule == 'replica-note': return f'replica of {values[0]}_s{values[1] if values[1] is not None else "none"}; the configuration\'s label is on the replicate-0 card'
    if rule == 'context-candidates':
        if not values: raise ValueError('empty derived candidates')
        return values
    if rule.startswith('context-'):
        if values[0] != values[1] or (len(values)==5 and values[2] != values[3]):
            raise ValueError('context chain is disconnected')
        return values[-1]
    raise ValueError('unknown derived rule: '+rule)


def recorded(source, data=None):
    parts=Path(source).parts
    return not (set(parts)&{'replays','sandbox','telemetry','labviz'} or
                isinstance(data,dict) and str(data.get('evidence_status','')).startswith(('NOT EVIDENCE','EXPLORATORY')))


def walk(data, parts=()):
    if isinstance(data,dict):
        for key,value in data.items():
            yield parts+(key,),value
            yield from walk(value,parts+(key,))
    elif isinstance(data,list):
        for i,value in enumerate(data):
            yield parts+(i,),value
            yield from walk(value,parts+(i,))


def applied_writes(source, data):
    if not recorded(source,data) or re.search(r'(^|/)(inject[^/]*|step0_offline)\.',source): return []
    return [leaf(v,source,path_of(p)) for p,v in walk(data)
            if p[-1]=='delta_norm' and 'delta_norms' in p and finite(v)]


def label_table(): return json.loads((PACKAGE/'labels.json').read_text())


def label_class(value): return label_table().get('null' if value is None else value,'unknown')


def labels_from_spec(root):
    text=(Path(root)/'docs/LABVIZ_V2_SPEC.md').read_text()
    table=text[text.index('  | Label (exact)'):text.index('  Classes:')]
    out={}
    for line in table.splitlines():
        cells=[c.strip() for c in line.split('|')]
        if len(cells)<4 or not cells[1].startswith('`'): continue
        cls=re.search(r'`([^`]+)`',cells[2])
        if not cls: continue
        if cells[1].startswith('`null` final'): out['null']=cls[1]
        else:
            for name in re.findall(r'`([^`]+)`',cells[1]): out[name]=cls[1]
    return out


def recorded_labels(root):
    labels=set()
    for path in sorted((Path(root)/'results').rglob('*.json')):
        source=str(path.relative_to(root))
        if path.is_symlink() or not recorded(source) or any(x in source for x in ('infranodus_','tokenizer','c10z_')): continue
        data=json.loads(path.read_text())
        for parts,value in walk(data):
            if parts[-1] in ('label','final_label','base_label','count_label','direction') and isinstance(value,str): labels.add(value)
    return labels


def join_matches(identity, reading):
    return all(identity.get(k)==reading.get(k) for k in ('family','recipe','arm','seed','replicate','sha256'))


def rule_outcome(observed, reference, comparison):
    if isinstance(observed,list):
        if not observed or not all(finite(v) for v in observed): return None
        if len(observed)==2 and not isinstance(reference,list):
            return rule_outcome(observed[0],reference,comparison) and observed[1]==0
        if not isinstance(reference,list) or len(observed)!=len(reference): return None
        return all(rule_outcome(x,y,comparison) for x,y in zip(observed,reference))
    if not finite(observed) or not finite(reference): return None
    return observed<=reference if comparison=='≤' else observed>=reference


def gate_consistent(gate):
    return (gate.get('passed',{}).get('value') is rule_outcome(gate.get('observed',{}).get('value'),gate.get('reference_line',{}).get('value'),gate.get('comparison')))


def gauge_fixture(value, reference, passed):
    if not finite(value) or not finite(reference): return {'judgement':'not recorded for this run'}
    return {'observed':{'value':value},'reference_line':{'value':reference-3},'passed':{'value':passed},'comparison':'≥','judgement':'recorded'}


def strip_cell(value):
    values=value.get('value')
    return sum(values) if isinstance(values,list) and values and all(isinstance(v,bool) for v in values) else None


def transcription_valid(table, root):
    t=table['c10_harness']; path=Path(root)/t['source_file']
    if not path.is_file() or sha(path)!=t['sha256']: return False
    lines=path.read_text().splitlines(); entries=t['entries']
    if len(entries)!=4 or lines[51].strip()!='PTEST = [': return False
    for i,e in enumerate(entries):
        if e['role']!=('CANON' if i==0 else 'PTEST') or e['index']!=(0 if i==0 else i-1) or e['line']!=(51 if i==0 else 52+i): return False
        target='CANON = '+json.dumps(e['text']) if i==0 else json.dumps(e['text'])+','
        if lines[e['line']-1].strip()!=target: return False
    return True


def transcribed_stimulus(data, root):
    table=json.loads((PACKAGE/'stimulus.json').read_text()); t=table['c10_harness']
    bound=data.get('identity',{}).get('source_sha256',{}).get(t['source_file'])
    if bound!=t['sha256'] or not transcription_valid(table,root):
        return {'canonical':missing('not transcribed for this code version'),'questions':missing('question text for this run\'s code version not transcribed')}
    entries=[leaf(e['text'],'tools/labviz/stimulus.json',f'.c10_harness.entries[{i}].text') for i,e in enumerate(t['entries'])]
    return {'canonical':entries[0],'questions':leaf([e['text'] for e in t['entries'][1:]],'tools/labviz/stimulus.json','.c10_harness.questions'),
            'bound_by':leaf(bound,'tools/labviz/stimulus.json','.c10_harness.sha256')}


def bound_parts(data, root):
    root=Path(root); hp_hash=data.get('identity',{}).get('source_sha256',{}).get(HPARAMS)
    parts={'written_module':missing("hparams for this run's code version not read"),'structure':{'layers':missing('model structure for this revision not read')}}
    if (root/HPARAMS).is_file() and hp_hash==sha(root/HPARAMS):
        hp=json.loads((root/HPARAMS).read_text()); parts['written_module']=leaf(hp['rewrite_module_tmp'],HPARAMS,'.rewrite_module_tmp')
        parts['keyed_position']=leaf(hp['fact_token'],HPARAMS,'.fact_token')
    model=data.get('model')
    if isinstance(model,dict) and model.get('id')=='Qwen/Qwen2.5-3B' and model.get('revision')==REVISION and (root/CONFIG).is_file():
        config=json.loads((root/CONFIG).read_text())
        names={'layers':'num_hidden_layers','hidden_size':'hidden_size','intermediate_size':'intermediate_size','num_attention_heads':'num_attention_heads','num_key_value_heads':'num_key_value_heads','tie_word_embeddings':'tie_word_embeddings'}
        parts['structure']={name:leaf(config[key],CONFIG,'.'+key) for name,key in names.items()}
    return parts


def compare(left,right):
    lf=left.get('per_fact',[]); rf=right.get('per_fact',[])
    def refusal(why): return {'eligible':False,'reason':'not comparable: '+why}
    if not lf or not rf: return refusal('fact population not recorded')
    l={x['subject']['value']:x for x in lf}; r={x['subject']['value']:x for x in rf}
    if len(l)!=len(lf) or len(r)!=len(rf) or set(l)!=set(r): return refusal('different fact populations')
    if left.get('stimulus',{}).get('questions',{}).get('value') is None or left['stimulus']['questions']['value']!=right.get('stimulus',{}).get('questions',{}).get('value'): return refusal('different or missing question templates')
    counts={'both right':0,'only left':0,'only right':0,'neither':0}
    for subj,a in l.items():
        b=r[subj]
        if a['answer']['value']!=b['answer']['value']: return refusal('changed answer for '+str(subj))
        if a['hit_kind']!=b['hit_kind']: return refusal('different scoring kinds')
        av=a['rewordings_hit']['value']; bv=b['rewordings_hit']['value']
        if not isinstance(av,list) or not isinstance(bv,list) or len(av)!=len(bv) or not all(isinstance(x,bool) for x in av+bv): return refusal('missing answers')
        for x,y in zip(av,bv): counts['both right' if x and y else 'only left' if x else 'only right' if y else 'neither']+=1
    return {'eligible':True,'derived':counts,'subjects':sorted(l)}


def newest_written(cards):
    eligible=[c for c in cards if any(x['written']['value'] for x in c.get('per_layer',[]))]
    return max(eligible,key=lambda c:(c['identity']['date']['value'] or '',c['card_id']))['card_id'] if eligible else None


def order_events(events):
    def at(event):
        value=event.get('at'); value=value.get('value') if isinstance(value,dict) else value
        return datetime.fromisoformat(value.replace('Z','+00:00')).astimezone(timezone.utc) if value else None
    def source(e):
        s=e.get('source',''); return s.get('value','') if isinstance(s,dict) else s
    timed=[e for e in events if at(e) is not None]; untimed=[e for e in events if at(e) is None]
    return sorted(timed,key=lambda e:(at(e),source(e),e.get('index',0))),sorted(untimed,key=lambda e:(source(e),e.get('index',0)))


def json_leaves(value):
    if isinstance(value,dict):
        if 'value' in value and 'path' in value.get('src',{}): yield value
        for key,item in value.items():
            if key not in ('value','src','built','sources'): yield from json_leaves(item)
    elif isinstance(value,list):
        for item in value: yield from json_leaves(item)


def citations(value):
    if isinstance(value,dict):
        if 'src' in value: yield value['src']['file']
        if isinstance(value.get('rule_src'),dict) and 'file' in value['rule_src']: yield value['rule_src']['file']
        if isinstance(value.get('population'),dict): yield value['population']['file']
        for k,item in value.items():
            if k not in ('value','src','sources','built'): yield from citations(item)
    elif isinstance(value,list):
        for item in value: yield from citations(item)


def validate_card(card, root, scales=None):
    root=Path(root); cache={}; hashes={s['file']:s['sha256'] for s in card['sources']}
    def source(file):
        if file not in cache: cache[file]=json.loads((root/file).read_text())
        return cache[file]
    def check(value,key=None):
        if isinstance(value,dict):
            if 'value' in value:
                if 'src' in value:
                    src=value['src']
                    if src['file'] not in hashes: raise ValueError('unhashed source '+src['file'])
                    if 'path' in src:
                        actual=resolve(source(src['file']),src['path'])
                        if actual!=value['value'] or type(actual)!=type(value['value']): raise ValueError('leaf differs from source '+str(src))
                    else:
                        line=(root/src['file']).read_text().splitlines()[src['line']-1]
                        if src['quote'] not in line or not isinstance(value['value'],str) or value['value'] not in src['quote']: raise ValueError('invalid quote '+str(src))
                elif 'derived' in value:
                    if 'population' in value:
                        if 'inputs' in value: raise ValueError('population derivation has inputs')
                        pop=value['population']; operands=resolve(scales or source(pop['file']),pop['path'])
                        if not operands: raise ValueError('empty population')
                        for x in operands: check(x)
                        if value['value']!=max(x['value'] for x in operands): raise ValueError('wrong population maximum')
                    else:
                        inputs=value.get('inputs',[])
                        if not inputs: raise ValueError('derived leaf has no operands')
                        for x in inputs: check(x)
                        if recompute(value['derived'],[x['value'] for x in inputs])!=value['value']: raise ValueError('wrong derived value')
                        rule=value['derived']
                        if rule in ('context-section','context-condition','context-layer'):
                            overlay=[x.get('src',{}) for x in inputs[1:3]]
                            if any(x.get('file')!='docs/SPEC_EXPERIMENT_OVERLAY.md' for x in overlay) or overlay[0].get('line')!=overlay[1].get('line'): raise ValueError('disconnected overlay relationship')
                            if rule=='context-condition':
                                ends=[x.get('src',{}) for x in inputs[3:5]]
                                if any(x.get('file')!='docs/F1_DETERMINATION.md' for x in ends) or ends[0].get('line')!=ends[1].get('line'): raise ValueError('disconnected condition relationship')
                            if rule=='context-layer':
                                end=inputs[4].get('src',{}); major=inputs[2]['value'].split('.',1)[0]
                                if end.get('file')!='docs/SPEC_E2E_GROUND_TRUTH.md' or major not in end.get('quote',''): raise ValueError('disconnected architecture relationship')
                elif 'structural' in value:
                    actual=resolve(card,'.'+value['structural'])
                    if actual!=value['value']: raise ValueError('wrong structural operand')
                elif 'missing' not in value or value['value'] is not None or 'tier' not in value: raise ValueError('untyped leaf')
                for k,item in value.items():
                    if k not in ('value','src','derived','inputs','rule_src','population','structural','missing','tier'):
                        check(item,k)
                return
            for k,item in value.items():
                if k not in ('sources','built'): check(item,k)
        elif isinstance(value,list):
            for item in value: check(item,key)
        elif value is not None and key not in STRUCTURAL: raise ValueError('bare value '+str(key))
    check(card)
    for file,expected in hashes.items():
        actual=hashlib.sha256(encoded(scales)).hexdigest() if file==POPULATION and scales is not None else sha(root/file)
        if actual!=expected: raise ValueError('source hash changed: '+file)
    peak=card.get('scale',{}).get('max',{}).get('value')
    if peak is not None and any(x.get('write_size',{}).get('value',0)>peak for x in card.get('per_layer',[]) if finite(x.get('write_size',{}).get('value'))): raise ValueError('write exceeds scale')
    return True


def validate_population(cards, scales, root):
    eligible={}; source_data={}
    for card in cards:
        for layer in card.get('per_layer',[]):
            w=layer.get('write_size',{})
            if 'src' in w and finite(w['value']): eligible[(w['src']['file'],w['src']['path'])]=w
    operands=scales['absolute_write_size']['operands']
    actual={(w['src']['file'],w['src']['path']):w for w in operands}
    if actual!=eligible: raise ValueError('scale population differs from eligible recorded writes')
    if max((x['value'] for x in operands),default=0)!=scales['absolute_write_size']['max']: raise ValueError('wrong scale maximum')
    for w in operands:
        file=w['src']['file']
        if file not in source_data: source_data[file]=json.loads((Path(root)/file).read_text())
        if resolve(source_data[file],w['src']['path'])!=w['value']: raise ValueError('invalid population member')
    return True


def generated_order_valid(card):
    templates=card['stimulus']['questions']['value']
    if not templates: return False
    for fact in card['per_fact']:
        if fact.get('generated_templates',{}).get('value')!=templates: return False
    return True


def validate_links(root):
    root=Path(root); links=json.loads((PACKAGE/'links.json').read_text())
    entries=json.loads((root/'docs/c10_evaluations.json').read_text())['entries']
    for key,ref in links.items():
        path=next((root/'CORPUS').glob(ref.split('/')[1]+'_*.md'))
        headers='\n'.join(path.read_text().splitlines()[:12])
        files=[root/key] if not key.endswith('/') else list((root/key).glob('*.json'))
        ids={json.loads(p.read_text()).get('decision_id') for p in files if p.is_file()}
        ids.discard(None)
        if any(d not in headers for d in ids): raise ValueError('evaluation link header mismatch: '+key)
        if not any(e['ref'].startswith(ref) for e in entries): raise ValueError('evaluation entry missing: '+ref)
    return True


class Reader:
    def __init__(self, root):
        from tools.labviz.context import load_program
        self.root=Path(root); self.program=load_program(self.root); self.cards=[]; self.files={}; self.hashes={}; self.events_cache={}; self.write_sources=set()
        self.tables={name:json.loads((PACKAGE/(name+'.json')).read_text()) for name in ('labels','gates','links','stimulus')}
        self.scales={}; self.runs=[]; self.survey={}

    def read(self,source):
        if source not in self.files: self.files[source]=json.loads((self.root/source).read_text())
        return self.files[source]

    def jl(self,source,path,reason='not recorded for this run'):
        try: value=resolve(self.read(source),path)
        except (KeyError,IndexError,TypeError,FileNotFoundError): return missing(reason)
        if value is None: return missing(reason)
        return leaf(value,source,path)

    def table(self,name,path):
        return leaf(resolve(self.tables[name],path),'tools/labviz/'+name+'.json',path)

    def collect(self):
        from tools.labviz import build as legacy
        operands=[]
        for p in sorted((self.root/'results').rglob('*.json')):
            source=str(p.relative_to(self.root))
            if p.is_symlink() or not recorded(source) or any(x in source for x in ('tokenizer','vocab','c10z_','infranodus_','research_pass','research_arc','openresearch_','autoresearch_reaim')): continue
            data=self.read(source)
            if not recorded(source,data): continue
            found=legacy.parse_record(data,source,self.root)
            writes=applied_writes(source,data)
            self.runs.extend(found); operands.extend(writes)
            if writes: self.write_sources.add(source)
            self.survey[source]={'name':source,'cards':len(found)}
        unique={(x['src']['file'],x['src']['path']):x for x in operands}
        operands=[unique[k] for k in sorted(unique)]
        self.scales={'absolute_write_size':{'unit':'absolute write size (Frobenius norm of ΔW)','operands':operands,'max':max((x['value'] for x in operands),default=0)},'sources':[{'file':s,'sha256':sha(self.root/s)} for s in sorted({x['src']['file'] for x in operands})]}
        for run in self.runs: self.cards.append(self.make(run))
        self.cards.extend(self.documentaries())
        self.cards.extend(self.log_cards())
        # Ensure every applied write appears on a card even for a schema without an arm.
        exposed={(w['src']['file'],w['src']['path']) for c in self.cards for x in c.get('per_layer',[]) for w in [x['write_size']] if 'src' in w}
        for source in sorted({x['src']['file'] for x in operands if (x['src']['file'],x['src']['path']) not in exposed}):
            fields={'.'.join(str(x) for x in path_parts(w['src']['path'])[:-2]) for w in operands if w['src']['file']==source and (w['src']['file'],w['src']['path']) not in exposed}
            for field in sorted(fields):
                run=legacy.make_run({},source,field,self.read(source),root=self.root,schema='recorded writes')
                self.cards.append(self.make(run))
        for c in self.cards: self.finish(c)
        self.cards.sort(key=lambda c:(c['identity']['date']['value'] or '',c['card_id']),reverse=True)
        return self.cards

    def find(self,source,field):
        return next(c for c in self.cards if c['identity']['name']==source and c['identity']['field']==field)

    def field_path(self,field):
        if field in ('numeric_key_table','records') and field=='numeric_key_table': return '.'
        parts=[]
        for token in re.findall(r'[^.\[\]]+|\[\d+\]',field):
            parts.append(int(token[1:-1]) if token.startswith('[') else token)
        return path_of(parts)

    def role(self,source,recipe,arm,data):
        if not source.startswith('results/c10'): return missing('roles apply to C10 configurations only')
        rows=self.tables['gates']['role_table']; row=None
        if arm.startswith(('A1_','A2_')): row=0
        elif arm=='A7_shuf': row=1
        elif arm=='A7_canon': row=2
        elif 'c10v_layerpick/' in source:
            row=3 if recipe=='A' else 4 if recipe=='Bshuf' else 5 if recipe in ('B','B0') and arm=='A7_coined_coined' else None
        elif 'c10w_oracle/' in source:
            row=6 if recipe=='closedform' else 7 if recipe.startswith('oracle_') and arm=='A7_coined_coined' else None
        elif 'c10u_mint2/' in source and data.get('kind'):
            row=8 if data['kind']=='multi' else 9
        elif re.search(r'results/c10(?:[b-j]_?|[k-q][_/])',source):
            row=10 if recipe in ('baseline','baseline_controls','A') else 11 if arm=='A7_coined_coined' else None
        return self.table('gates',f'.role_table[{row}].role') if row is not None and row<len(rows) else missing("role not in Lab View's table")

    def make(self,run):
        source=run['source']; raw_data=self.read(source); data=raw_data if isinstance(raw_data,dict) else {}; field=run['field']; p='.' if isinstance(raw_data,list) and field=='records' else self.field_path(field)
        try: node=resolve(raw_data,p)
        except (KeyError,IndexError,TypeError): node={}
        if not isinstance(node,dict): node={}
        tokens=path_parts(p); recipe=tokens[1] if len(tokens)>1 and tokens[0]=='recipes' else ''
        arm=next((tokens[i+1] for i,k in enumerate(tokens[:-1]) if k in ('arms','delta_norms','detail')),data.get('arm') if isinstance(data.get('arm'),str) else '')
        if field=='arm' and source.startswith('results/c10u_mint2/'): arm='A7_coined_coined'
        c={'schema':'labviz.run_card/v1','card_id':run['id'],'evidence_status':'RECORDED','built':{'builder_sha256':sha(PACKAGE/'build.py')},
           'identity':{'name':source,'family':source.split('/')[1].split('.')[0],'field':field,'recipe':recipe,'arm':arm,
                       'role':self.role(source,recipe,arm,data),'seed':self.jl(source,'.seed'),'replicate':self.jl(source,'.replicate'),
                       'decision_id':self.jl(source,'.decision_id'),'model':missing('model not recorded'),'model_revision':missing('model revision not recorded'),'date':missing('date not recorded')},
           'context':self.program.context(source,data),'headline':{},'label':missing('not judged yet','not-judged-yet'),'gates':[],'per_fact':[],'per_layer':[],
           'parts':bound_parts(data,self.root),'stimulus':{},'plain_words':{},'events':{'timestamped':[],'untimed':[]}}
        if c['context'].get('corpus',{}).get('node_id')=='corpus:22' and len(tokens)>=2 and tokens[0] in ('DILUTED','CONCENTRATED') and tokens[1]=='trajectory':
            c['identity']['display_title']=self.jl('tools/labviz/contexts.json',f'.corpus_eras["22"].display_titles["{tokens[0]}"]')
        for model_path in ('.model.id','.model','.model_id','.config.model','.environment.model_id'):
            m=self.jl(source,model_path)
            if isinstance(m['value'],str): c['identity']['model']=m; break
        for rev_path in ('.model.revision','.model_revision','.environment.model_revision'):
            m=self.jl(source,rev_path)
            if m['value'] is not None: c['identity']['model_revision']=m; break
        for stamp_path in ('.when_utc','.identity.created_utc','.date','.started'):
            m=self.jl(source,stamp_path)
            if isinstance(m['value'],str): c['identity']['date']=m; break
        for name,keys in [('hits',('para_full_binding_n','para_full_n')),('out_of',('para_n','masked_binding_prompt_n')),('percent',('para_full','para_full_match')),('canonical',('canon_full_n',)),('rate',('ptest_mean_rate',))]:
            c['headline'][name]=next((self.jl(source,p+('.' if p!='.' else '')+k) for k in keys if finite(node.get(k))),missing())
        role=c['identity']['role']['value']
        if role=='binding': c['headline']['program_goal']=self.jl('docs/c10_scoreboard.json','.goal')
        if finite(node.get('ptest_mean_rate')): c['headline']['rate']=self.jl(source,p+'.ptest_mean_rate')
        if source=='results/g6_scale_n_result.json' and len(tokens)==2 and tokens[0]=='rungs' and isinstance(tokens[1],int):
            c['headline']['heldout_top1']={**self.jl(source,p+'.heldout_top1.edited_rel.top1_correct_vs_truth'),
                                          'unit':'percent','plain':'edited-relation top-1 correctness vs truth'}
            c['headline']['rung_n']=self.jl(source,p+'.n')
            c['headline']['heldout_baseline_top1']=self.jl(source,'.heldout_baseline_top1_correct.edited_rel.top1_correct_vs_truth')
        self.attach_reading(c,data,node,p)
        self.facts(c,data,node,p)
        self.writes(c,data,node,p)
        self.stimuli(c,data,node,p)
        self.gauges(c,data,node,p)
        self.evaluation(c)
        if source.startswith('results/c10w_oracle/') and '/train/' in source and isinstance(data.get('losses'),list):
            c['training']={k:self.jl(source,'.'+k) for k in ('losses','step_seconds','fit','seed','retrain')}
        if source=='results/g6_scale_n_result.json' and field=='records':
            c['records']=[{k:self.jl(source,f'.records[{i}].{k}') for k in row} for i,row in enumerate(data['records'])]
            c['rungs']=[{k:self.jl(source,f'.rungs[{i}].{k}') for k in row} for i,row in enumerate(data['rungs'])]
        if source.startswith('results/c10v_layerpick/') and recipe=='B' and arm=='A7_coined_coined':
            sf='results/c10v_layerpick/step0.json'; rf='results/c10v_layerpick/run.json'
            c['layer_map']={k:self.jl(sf,q) for k,q in [('G_table','.G_table'),('G_table_repeat','.G_table_repeat'),('margins','.winning_margins[0]'),('repeat_margins','.winning_margins[1]'),('map','.map'),('repeat_map','.repeat_map'),('map_reproduced','.map_reproduced'),('delta','.delta'),('runner_up','.runner_up')]}
            if c['identity'].get('reading_bound_to_record',{}).get('value') is not None:
                c['layer_map'].update(spearman=self.jl(rf,'.readings.B.spearman_G_edge'),by_layer=self.jl(rf,'.readings.B.by_layer'))
        if source.startswith('results/c10w_oracle/'): c['events']=self.family_events('c10w_oracle')
        elif c['identity']['date']['value'] and 'T' in c['identity']['date']['value']:
            c['events']['timestamped']=[{'name':'record timestamp','index':0,'at':c['identity']['date'],'detail':c['identity']['decision_id']}]
        # Preserve original diagnostic rows as sourced values, without interpreting units.
        if not c.get('training'):
            try: raw=resolve(raw_data,p)
            except (KeyError,IndexError,TypeError): raw=None
            if raw is not None and not (isinstance(raw,dict) and any(k in raw for k in ('memory_samples','train_records','frozen_parameter_hashes_before'))): c['measures']=leaf(raw,source,p)
        return c

    def attach_reading(self,c,data,node,p):
        source=c['identity']['name']; recipe=c['identity']['recipe']; arm=c['identity']['arm']; role=c['identity']['role']['value']
        family=c['identity']['family']; identity={'family':family,'recipe':recipe,'arm':arm,'seed':c['identity']['seed']['value'],'replicate':c['identity']['replicate']['value'],'sha256':sha(self.root/source)}
        if source=='results/c10v_layerpick/pass1.json' and arm=='A7_coined_coined' and recipe in ('B0','B','Bshuf'):
            reader='results/c10v_layerpick/run.json'; record=self.read(reader)
            joined={**identity,'seed':None,'replicate':None,'sha256':record.get('pass_sha256',{}).get('pass1')}
            if join_matches(identity,joined):
                c['identity']['reading_bound_to_record']=self.jl(reader,'.pass_sha256.pass1')
                c['headline']['count_used_by_label']=self.jl(reader,f'.readings.{recipe}.binding')
                label=self.jl(reader,f'.readings.{recipe}.label')
                if role=='binding': c['label']=label
                elif recipe=='Bshuf': c['control_label']=label
        elif source.startswith('results/c10u_mint2/r3/') and c['identity']['field']=='arm' and data.get('kind')!='multi':
            if data.get('replicate')==0:
                key=f'{data["kind"]}_s{data["seed"] if data.get("seed") is not None else "none"}'; reader='results/c10u_mint2/r3_read_after_replicateF.json'
                c['label']=self.jl(reader,f'.{data["block"]}.arms.{key}.label')
                c['headline']['count_used_by_label']=self.jl(reader,f'.{data["block"]}.arms.{key}.binding')
            else: c['replica_note']=derived('replica-note',[self.jl(source,'.kind'),self.jl(source,'.seed'),self.jl(source,'.replicate')])
        elif 'c10w_oracle/' in source:
            v=str(Path(source).parent/'verdict.json')
            if (self.root/v).is_file():
                c['oracle_class']=self.jl(v,'.class')
                if role=='binding': c['label']=self.jl(v,'.final_label','not judged yet')
            else: c['oracle_class']=self.jl(source,'.class')
            interim=str(Path(source).parent/'interim_reader_configuration_v2.json')
            if (self.root/interim).is_file() and recipe=='oracle_p1' and arm=='A7_coined_coined':
                bound=self.read(interim).get('p1_eval',{}).get('sha256')
                if bound==sha(self.root/source):
                    c['identity']['reading_bound_to_record']=self.jl(interim,'.p1_eval.sha256')
                    c['interim_label']=self.jl(interim,'.oracle_p1_A7_configuration.label')
        elif role=='binding': c['label']=self.jl(source,'.verdict.label')
        elif not source.startswith('results/c10'): c['label']=self.jl(source,'.label','no label recorded; see the context source')
        c['label']['colour_class']=label_class(c['label']['value']); c['label']['colour_table']='tools/labviz/labels.json'
        if 'interim_label' in c: c['interim_label'].update(colour_class=label_class(c['interim_label']['value']),colour_table='tools/labviz/labels.json')

    def facts(self,c,data,node,p):
        source=c['identity']['name']; arm=c['identity']['arm']; recipe=c['identity']['recipe']; rows=[]; base=None; kind='free answer'
        if 'arms' in path_parts(p):
            parent=p.rsplit('.arms.',1)[0]; dp=parent+'.detail'+('['+json.dumps(arm)+']')
            rows=self.jl(source,dp)['value'] or []; base=dp
        if source=='results/r5_paraphrase_robustness.json' and arm in data.get('rows',{}): base='.rows.'+arm; rows=self.jl(source,base)['value'] or []
        if source.startswith('results/c10u_mint2/') and c['identity']['field']=='arm':
            base='.arm.extra.per_fact_position_curve'; rows=self.jl(source,base)['value'] or []; kind='teacher-forced'
        for i,row in enumerate(rows):
            q=f'{base}[{i}]'; subject='subj' if 'subj' in row else 'subject'
            hit='ptest_hits' if 'ptest_hits' in row else 'para_full_hits'
            fact={'index':i,'hit_kind':kind,'subject':self.jl(source,q+'.'+subject),'answer':self.jl(source,q+'.'+('target' if 'target' in row else 'val')),
                  'answer_pieces':self.jl(source,q+'.ntok'),'rewordings_hit':self.jl(source,q+'.'+hit),'canonical_hit':self.jl(source,q+'.'+('L1_canon' if 'L1_canon' in row else 'canon_full')),
                  'generated_text':self.jl(source,q+'.ptest_obs','not recorded by this family'),'recorded_detail':self.jl(source,q)}
            if kind=='teacher-forced':
                raw=self.jl(source,q+'.per_template_hits'); fact['teacher_hits']=raw
                fact['rewordings_hit']=derived('teacher-hits',[raw]) if isinstance(raw['value'],list) else missing()
                subj=row.get('subj'); value=data.get('values',{})
                if isinstance(value,dict) and subj in value: fact['answer']=self.jl(source,path_of(('values',subj)))
            assignment=data.get('recipes',{}).get(recipe,{}).get('map') if recipe else None
            if isinstance(assignment,dict) and row.get('subj') in assignment: fact['assigned_layer']=self.jl(source,path_of(('recipes',recipe,'map',row['subj'])))
            if source.startswith('results/c10v_layerpick/') and recipe and arm:
                subject=row.get('subj')
                fact['target_ids']=self.jl(source,path_of(('recipes',recipe,'target_ids',arm,subject)))
                fact['prediction_before_write']=self.jl(source,path_of(('recipes',recipe,'predictions_before_write',arm,subject)))
                proxy=node.get('extra',{}).get('proxy',{}).get('rows',[])
                if i<len(proxy) and proxy[i].get('subj')==subject: fact['proxy']=self.jl(source,f'{p}.extra.proxy.rows[{i}]')
            step0=data.get('step0_directory')
            if source.startswith('results/c10w_oracle/') and isinstance(step0,str):
                file='results/'+step0.split('/results/',1)[-1]+'/step0.json'
                if (self.root/file).is_file(): fact['answer_split']=self.jl(file,path_of(('head_modifier_splits',row.get('subj'))))
            generated=node.get('extra',{}).get('generated')
            if isinstance(generated,list):
                entries=generated[3*i:3*i+3]
                if len(entries)!=3 or any(e.get('subj')!=row.get('subj') for e in entries): raise ValueError('generated prompt order differs from detail: '+source)
                gp=p+'.extra.generated'; texts=[self.jl(source,f'{gp}[{3*i+j}].text') for j in range(3)]
                templates=[self.jl(source,f'{gp}[{3*i+j}].template') for j in range(3)]
                fact['generated_text']={'value':[x['value'] for x in texts],'derived':'context-candidates','inputs':texts,'rule_src':{'spec':'§3.6'}}
                fact['generated_templates']={'value':[x['value'] for x in templates],'derived':'context-candidates','inputs':templates,'rule_src':{'spec':'§3.6'}}
            c['per_fact'].append(fact)

    def writes(self,c,data,node,p):
        source=c['identity']['name']; arm=c['identity']['arm']; recipe=c['identity']['recipe']; wp=None; band=missing('configured band not recorded')
        if recipe: wp=path_of(('recipes',recipe,'delta_norms',arm)); band=self.jl(source,path_of(('recipes',recipe,'band')))
        elif source.startswith('results/c10u_mint2/') and c['identity']['field']=='arm': wp='.recipe.delta_norms.candidate'; band=self.jl(source,'.recipe.band')
        elif 'delta_norms' in path_parts(p): wp=p; band=self.jl(source,'.band')
        elif c['identity']['field'].startswith('recipe.arms.'): wp=path_of(('recipe','delta_norms',arm)); band=self.jl(source,'.recipe.band')
        if band['value'] is None and data.get('band'): band=self.jl(source,'.band')
        if band['value'] is None and c['parts']['written_module'].get('src',{}).get('file')==HPARAMS: band=self.jl(HPARAMS,'.layers')
        c['parts']['band']=band
        writes=self.jl(source,wp)['value'] if wp else None
        if not isinstance(writes,dict): writes={}
        if source not in self.write_sources: writes={}
        bandlayers=band['value'] if isinstance(band['value'],list) else []
        layers=sorted(set(bandlayers)|{int(k) for k,v in writes.items() if str(k).isdigit() and isinstance(v,dict) and finite(v.get('delta_norm'))})
        for i,l in enumerate(layers):
            path=(wp+'['+json.dumps(str(l))+'].delta_norm') if wp else None
            size=self.jl(source,path) if path else missing()
            item={'layer':l,'unit':'absolute write size (Frobenius norm of ΔW)','write_size':size,'written':derived('written',[size]),'relative_write_size':self.jl(source,wp+'['+json.dumps(str(l))+'].relative_delta_norm') if wp else missing()}
            item['configured']=derived('in-band',[band,{'value':l,'structural':f'per_layer[{i}].layer'}]) if band['value'] is not None else missing()
            c['per_layer'].append(item)
        if any(x['written']['value'] for x in c['per_layer']):
            c['scale']={'unit':'absolute write size (Frobenius norm of ΔW)','max':{'value':self.scales['absolute_write_size']['max'],'derived':'population maximum','population':{'file':POPULATION,'path':'.absolute_write_size.operands'},'rule_src':{'spec':'§5 item 4'}}}
        if source.startswith('results/c10'):
            c['parts']['untouched_basis']=self.table('gates','.untouched_basis.oracle' if 'c10w_oracle/' in source else '.untouched_basis.memit')
        if source.startswith('results/c10w_oracle/'):
            normalized={'model':{'id':c['identity']['model']['value'],'revision':c['identity']['model_revision']['value']}}
            c['parts']['structure']=bound_parts(normalized,self.root)['structure']
            c['parts']['frozen_training']=self.jl(source,'.train_records[0].frozen_parameters_unchanged')
            c['parts']['base_band_hash']=self.jl(source,'.base_band_hash'); c['parts']['final_band_hash']=self.jl(source,'.final_band_hash')

    def stimuli(self,c,data,node,p):
        source=c['identity']['name']; stimulus=data.get('stimulus',{})
        if isinstance(stimulus,dict) and isinstance(stimulus.get('PTEST'),list):
            c['stimulus']={'canonical':self.jl(source,'.stimulus.CANON'),'questions':self.jl(source,'.stimulus.PTEST')}
        elif isinstance(data.get('held_out_forms',{}).get('PTEST'),list):
            c['stimulus']={'canonical':missing('not transcribed'),'questions':self.jl(source,'.held_out_forms.PTEST')}
        elif source=='results/r5_paraphrase_robustness.json':
            c['stimulus']={'canonical':self.jl(source,'.templates.canonical'),'questions':self.jl(source,'.templates.P_test')}
        elif isinstance(node.get('extra',{}).get('generated'),list) and len(node['extra']['generated'])>=3:
            entries=[self.jl(source,f'{p}.extra.generated[{j}].template') for j in range(3)]
            c['stimulus']={'canonical':missing('canonical question not transcribed'),'questions':derived('context-candidates',entries)}
            step0=data.get('step0_directory')
            if isinstance(step0,str):
                rel=step0.split('/results/',1)[-1]; file='results/'+rel+'/seal_audit.json'
                if (self.root/file).is_file():
                    for i,e in enumerate(self.read(file)['rows']):
                        if e.get('id')=='T01': c['stimulus']['canonical']=self.jl(file,f'.rows[{i}].template')
                    c['stimulus']['training_phrasings']=self.jl(file,'.rows')
        else: c['stimulus']=transcribed_stimulus(data,self.root)
        c['stimulus']['keyed_position']=c['parts'].get('keyed_position',missing('keyed position not recorded'))
        c['stimulus']['keyed_piece_text']=missing('piece text not recorded for this run','Phase 2a extract')

    def gauges(self,c,data,node,p):
        source=c['identity']['name']; recipe=c['identity']['recipe']; arm=c['identity']['arm']; family=c['identity']['family']; ref=None; rp=None; reading=None; underfit=False
        if not node.get('locality_axes') and node.get('locality_described_as') is None: return
        if source=='results/c10v_layerpick/pass1.json' and arm=='A7_coined_coined' and recipe in ('B','B0','Bshuf') and c['identity'].get('reading_bound_to_record',{}).get('value'):
            ref=source; rp='.recipes.A.arms.A7_coined_coined'; reading=('results/c10v_layerpick/run.json',f'.readings.{recipe}.locality_gates'); family='C10V'
        elif source.startswith('results/c10u_mint2/r3/') and c['identity']['field']=='arm' and data.get('kind')!='multi' and data.get('replicate')==0:
            ref=f'results/c10u_mint2/r3/{data["block"]}_r0_multi_snone.json'; rp='.arm'; family='C10U'
            key=f'{data["kind"]}_s{data["seed"]}'; reading=('results/c10u_mint2/r3_read_after_replicateF.json',f'.{data["block"]}.arms.{key}.gates')
            underfit=self.jl(reading[0],reading[1])['value'] is None
        elif 'c10w_oracle/' in source and recipe:
            ref=source; rp='.recipes.closedform.arms.A7_coined_coined'; family='C10W'
            if c['identity'].get('reading_bound_to_record',{}).get('value'): reading=(str(Path(source).parent/'interim_reader_configuration_v2.json'),'.oracle_p1_A7_configuration.gates')
        definitions={'L1':('locality_axes.L1_flipped_to_edited_value','≤','add_one'),'same_frame':('extra.same_frame.flips','≤','add_one'),'described_as':('locality_described_as','≥','minus_three'),'L3':('locality_axes.L3_top1_agree','≥','L3_min'),'generic_ppl':('locality_axes.generic_ppl_post','≤','ppl_rise')}
        if family=='C10U': definitions.update(same_frame=('extra.same_frame_flips','≤','add_one'),cannibal=('extra.post_write_cannibal','≤','cannibal_max'),sibling=('extra.para_sibling','≤','sibling_max'))
        if family=='C10W': definitions={'G1':definitions['L1'],'G2':definitions['L3'],'G3':definitions['described_as'],'G4':('extra.frames.canon.flips','≤','add_one'),'G5':definitions['generic_ppl'],'G6':('extra.mmlu.correct','≤','MMLU_max'),'G7':('extra.cross_score.para_full_n','≤','shuf_max')}
        for name,(key,comparison,constant) in definitions.items():
            observed=self.jl(source,p+('.' if p!='.' else '')+key); limit=None
            if ref and not underfit:
                offset=self.table('gates','.constants.'+constant)
                if name in ('L3','cannibal','sibling','G2','G6','G7'): limit=offset
                else: limit=derived('add',[self.jl(ref,rp+'.'+key),offset]) if finite(self.jl(ref,rp+'.'+key)['value']) else None
                if family=='C10U' and name in ('L1','same_frame','L3'):
                    minted=self.jl(source,p+'.extra.'+{'L1':'L1_minted_n','same_frame':'frame_minted_n','L3':'L3_minted_n'}[name])
                    if observed['value'] is not None and minted['value'] is not None: observed=derived('minted-value',[observed,minted])
                    else: observed=missing()
                if family=='C10W' and name=='G4':
                    train=self.jl(source,p+'.extra.frames.train'); base=self.jl(ref,rp+'.extra.frames.train'); canon_ref=self.jl(ref,rp+'.extra.frames.canon.flips')
                    if observed['value'] is not None and train['value'] is not None and base['value'] is not None and canon_ref['value'] is not None:
                        observed=derived('frame-values',[observed,train]); limit=derived('map-add',[derived('frame-values',[canon_ref,base]),offset])
                    else: observed=missing(); limit=None
                if family=='C10W' and name=='G5':
                    pre=self.jl(source,p+'.locality_axes.generic_ppl_pre'); post=self.jl(source,p+'.locality_axes.generic_ppl_post')
                    observed=derived('rounded-rise',[pre,post,self.table('gates','.constants.round_ppl')]) if finite(pre['value']) and finite(post['value']) else missing(); limit=offset
                if family=='C10W' and name=='G6':
                    u=self.jl(source,'.u.A7_coined_coined.extra.mmlu.correct')
                    observed=derived('paired-loss',[u,observed]) if isinstance(u['value'],list) and isinstance(observed['value'],list) else missing()
                if family=='C10W' and name=='G7': observed=self.jl(source,f'.recipes.{recipe}.arms.A7_shuf.extra.cross_score.para_full_n')
            row={'name':name,'plain':{'described_as':'Description of the places stayed similar','G3':'Description of the places stayed similar'}.get(name,name),'observed':observed,'comparison':comparison,'judgement':'no preregistered limit recorded'}
            usable=finite(observed['value']) or isinstance(observed['value'],list) and bool(observed['value']) and all(finite(x) for x in observed['value'])
            if not usable or limit is not None and rule_outcome(observed['value'],limit['value'],comparison) is None:
                row['observed']=missing(); row['judgement']='not recorded for this run'
            elif underfit: row['judgement']='not judged: UNDERFIT, no gate reading recorded'
            elif limit:
                row['reference_line']=limit; row['judgement']='not judged yet'
                passed=self.jl(reading[0],reading[1]+'.'+name) if reading else missing('no recorded gate result','not-judged-yet')
                if isinstance(passed['value'],bool):
                    row['passed']=passed; row['judgement']='recorded'
                    if not gate_consistent(row): row.pop('passed'); row['judgement']='limit could not be reproduced from the rule'
            c['gates'].append(row)

    def evaluation(self,c):
        source=c['identity']['name']; matches=[k for k in self.tables['links'] if source==k or k.endswith('/') and source.startswith(k)]
        entries=self.read('docs/c10_evaluations.json')['entries'] if (self.root/'docs/c10_evaluations.json').is_file() else []
        ref=self.tables['links'][max(matches,key=len)] if matches else None
        found=next(((i,e) for i,e in enumerate(entries) if e.get('ref','').startswith(ref)),None) if ref else None
        c['plain_words']={k:self.jl('docs/c10_evaluations.json',f'.entries[{found[0]}].{k}') if found else missing('no plain-words evaluation linked yet') for k in ('question','result','rules_out','leaves_open','next_step','ref')}

    def family_events(self,family):
        if family in self.events_cache: return self.events_cache[family]
        events=[]
        for source,data in self.files.copy().items():
            if not source.startswith('results/'+family): continue
            stamp=next((key for key in ('at','when_utc') if isinstance(data,dict) and isinstance(data.get(key),str)),None)
            if stamp: events.append({'name':data.get('stage','record timestamp'),'index':0,'source':leaf(source,source,'.__source__'),'at':self.jl(source,'.'+stamp),'detail':self.jl(source,'.status')})
            if isinstance(data,dict) and isinstance(data.get('losses'),list) and '/train/' in source:
                for i,loss in enumerate(data['losses']): events.append({'name':'training loss','index':i,'source':leaf(source,source,'.__source__'),'at':missing('time not recorded'),'detail':self.jl(source,f'.losses[{i}]')})
        for path in sorted((self.root/'results/c10w_oracle_logs').glob('*.log')):
            source=str(path.relative_to(self.root))
            for i,line in enumerate(path.read_text().splitlines(),1):
                if 'STAGE_EXIT=' in line or re.search(r'\b[A-Z0-9_]+_DONE\b',line):
                    events.append({'name':line,'index':i,'source':doc(source,source,i,line),'at':missing('time not recorded'),'detail':doc(line,source,i,line)})
        # Source ordering metadata is structural; no absolute time comes from filenames.
        for event in events:
            source=event.pop('source'); event['field']=source['src']['file']
        timed,untimed=order_events([{**e,'source':e['field']} for e in events])
        for e in timed+untimed: e.pop('source')
        self.events_cache[family]={'timestamped':timed,'untimed':untimed}; return self.events_cache[family]

    def documentaries(self):
        from tools.labviz.build import digest
        cards=[]
        for row in self.program.registry:
            source='docs/EXPERIMENT_REGISTRY.md'; line=row['line']; quote=(self.root/source).read_text().splitlines()[line-1]
            context=self.program.registry_context(row['id'])
            context['experiment']={**doc(row['id'],source,line,quote),'node_id':'exp:'+row['id'],'edge':'direct'}
            for key,col in [('question','question'),('status_now','status')]: context[key]=doc(row[col],source,line,quote)
            cards.append({'schema':'labviz.run_card/v1','card_id':'run-'+digest([source,row['id']])[:16],'evidence_status':'RECORDED','built':{'builder_sha256':sha(PACKAGE/'build.py')},
                          'identity':{'name':source,'family':'documentary','field':row['id'],'recipe':'','arm':'','model':missing('model not recorded'),'date':missing('date not recorded')},
                          'context':context,'headline':{},'label':missing('no label recorded; see the registry status'),'plain_words':{'question':context['question'],'result':context['status_now']}})
        for path in sorted((self.root/'CORPUS').glob('[0-9][0-9]_*.md')):
            lines=path.read_text().splitlines(); source=str(path.relative_to(self.root)); title=lines[0].lstrip('# ')
            verdict=next(((i+1,l) for i,l in enumerate(lines) if re.match(r'^(?:#{1,3}\s+|\*\*)(?:NET )?VERDICT',l,re.I)),None)
            cards.append({'schema':'labviz.run_card/v1','card_id':'run-'+digest([source,'verdict'])[:16],'evidence_status':'RECORDED','built':{'builder_sha256':sha(PACKAGE/'build.py')},
                          'identity':{'name':source,'family':'documentary','field':'verdict','recipe':'','arm':'','model':missing('model not recorded'),'date':missing('date not recorded')},
                          'context':{'experiment':missing('no registry row names this record'),'corpus':{**doc(title,source,1,lines[0]),'node_id':'corpus:'+path.name[:2]},'question':doc(title,source,1,lines[0]),'era':missing('era not recorded'),'measure':missing('context not recorded')},
                          'headline':{},'label':missing('no label recorded'),'plain_words':{'question':doc(title,source,1,lines[0]),'result':doc(verdict[1],source,*verdict) if verdict else missing('verdict header not recorded')}})
        from tools.labviz.build import CATALOG
        for name,info in CATALOG.items():
            if info['status']!='tested earlier': continue
            source=info['note_source']; path=self.root/source
            if not path.is_file(): continue
            lines=path.read_text().splitlines()
            match=next(((i+1,line) for i,line in enumerate(lines) if name in line),None)
            if not match: continue
            model=doc(name,source,*match)
            cards.append({'schema':'labviz.run_card/v1','card_id':'run-'+digest([source,name])[:16],'evidence_status':'RECORDED','built':{'builder_sha256':sha(PACKAGE/'build.py')},
                          'identity':{'name':source,'family':'documentary','field':name,'recipe':'','arm':'','model':model,'date':missing('date not recorded')},
                          'context':{'experiment':missing('documentary model-family era'),'era':leaf('t-branch','tools/labviz/contexts.json','.model_eras'+ '['+json.dumps(name)+']'+'.era'),
                                     'question':doc(match[1],source,*match),'measure':missing('documentary finding; no machine-readable scores')},
                          'headline':{},'label':missing('documentary finding; no recorded run label'),'plain_words':{'question':doc(match[1],source,*match),'result':doc(match[1],source,*match)}})
        return cards

    def log_cards(self):
        from tools.labviz.build import parse_log, digest
        cards=[]
        for path in sorted((self.root/'results').rglob('*.log')):
            source=str(path.relative_to(self.root))
            if path.is_symlink() or not recorded(source) or 'c10z_' in source: continue
            lines=path.read_text(errors='replace').splitlines(); parsed=parse_log('\n'.join(lines),source)
            observations=[(run['id'],run['field'],int(run['field'].split()[1])) for run in parsed['observations']]
            if parsed['losses']:
                line=next(i+1 for i,text in enumerate(lines) if re.search(r'\bstep\s+\d+\s+loss\b',text,re.I))
                observations.append(('run-'+digest([source,'training loss'])[:16],'training loss',line))
            for identifier,field,line in observations:
                cards.append({'schema':'labviz.run_card/v1','card_id':identifier,'evidence_status':'RECORDED','built':{'builder_sha256':sha(PACKAGE/'build.py')},
                              'identity':{'name':source,'family':Path(source).parts[1],'field':field,'recipe':'','arm':'','model':missing('model not recorded in this observation'),'date':missing('time not recorded')},
                              'context':self.program.context(source,{}),'headline':{},'label':missing('no joined reader label'),'per_fact':[],'per_layer':[],
                              'measures':doc(lines[line-1],source,line,lines[line-1]),'plain_words':{'result':doc(lines[line-1],source,line,lines[line-1])},
                              'events':{'timestamped':[],'untimed':[{'name':'log observation','field':source,'index':line,'at':missing('time not recorded'),'detail':doc(lines[line-1],source,line,lines[line-1])}]}})
        return cards

    def finish(self,c):
        files=set(citations(c))|{'tools/labviz/labels.json','tools/labviz/gates.json','tools/labviz/links.json','tools/labviz/stimulus.json','tools/labviz/contexts.json'}
        if (self.root/'docs/LABVIZ_V2_SPEC.md').is_file(): files.add('docs/LABVIZ_V2_SPEC.md')
        if POPULATION in files:
            files.update(x['file'] for x in self.scales['sources'])
        c['sources']=[]
        for file in sorted(files):
            path=self.root/file
            if file==POPULATION: h=hashlib.sha256(encoded(self.scales)).hexdigest()
            else:
                if not path.is_file():
                    if (PACKAGE/Path(file).name).is_file() and file.startswith('tools/labviz/'): path=PACKAGE/Path(file).name
                    else: raise ValueError('cited source is missing: '+file)
                if file not in self.hashes: self.hashes[file]=sha(path)
                h=self.hashes[file]
            c['sources'].append({'file':file,'sha256':h})
