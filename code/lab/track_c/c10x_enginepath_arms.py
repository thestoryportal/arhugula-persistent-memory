"""C10X FE/OverTone driver and independent process-group supervisor.

Only stdlib imports at module load. The real model path is entered by main only.
"""
import argparse
import ast
import contextlib
import copy
import datetime
import hashlib
import importlib.metadata
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import platform
import re
import resource
import signal
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[3]
# Lazy science modules must share this instance when the supervisor uses a script.
if __name__=='__main__':sys.modules['c10x_enginepath_arms']=sys.modules[__name__]
PIN = '3eb899d922a3ab66b6887bf6375602a3f741eeb681ce476a8d167b080a7cd07a'
CONTEXT_SOURCE = 'code/lab/track_c/c10z_astra_benchmark.py'
C10Q_CONTEXT_SHA = 'c7dabbe7c25a7e58653621d9cc66e37b35c865ae09b73b6a96073a184c6c98da'
C10Q_TEMPLATES_SHA = 'd6c7c70026dced37bddc6adf316a3487d70227dae80a6e0ed5cdabe50caedfa0'
FRAME_SUBJECTS = ['Vorbanth', 'Quillexa', 'Tremnok', 'Oskavel', 'Blynthar', 'Durmquist']
ARM_NAMES = ('A1_single', 'A2_coherent2', 'A7_coined_coined')
CAPS = {'setup':600., 'A':2040., 'targets':3600., 'inertness':3000., 'injection':1500., 'I-2':2040., 'I-1':2040., 'final':780.}
PROCESS_BUDGET = 16200.
KNOBS = ('MODEL_ID','MODEL_REV','C10_PROJECTOR','N_EDIT','C10_SUBJECT_OFFSET','C10_CTX_TEMPLATES','C10_KEY_LOCUS','RUN_LABEL')
TELEMETRY_CLOCK = time.perf_counter
WATCHDOG_CLOCK = time.monotonic
H = None
ORIGINAL_EDIT = None
FE_STATE = None
FE_TARGETS = {}
FE_CALLS = 0
IN_RECIPE = False
ACTIVE_RECIPE = None
TELEMETRY = None
WRITE_NORMS = {}
RHO = {}
CURRENT_TARGETS = None
PRISTINE = None
BUDGET = None
ARM_UNIT = None
UNIT_PLAN = {'setup':{},'A':{'recipe_arm':3,'G':1},'targets':{'solve':216},
             'inertness':{'solve':100,'write':6,'G8':1},'injection':{'injection':288},
             'I-2':{'recipe_arm':3,'G':1},'I-1':{'recipe_arm':3,'G':1},'final':{}}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1<<20), b''):
            h.update(chunk)
    return h.hexdigest()


def json_sha(obj):
    return hashlib.sha256(json.dumps(obj,allow_nan=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def write_json(path, obj):
    path = Path(path)
    data = json.dumps(obj, allow_nan=False, sort_keys=True, separators=(',',':'))+'\n'
    path.parent.mkdir(parents=True,exist_ok=True)
    # Exclusive publish: no partially written canonical record and no overwrite.
    temporary = path.with_name(path.name+'.tmp.'+str(os.getpid()))
    with temporary.open('x',encoding='utf8') as f:
        f.write(data);f.flush();os.fsync(f.fileno())
    try:
        os.link(temporary,path)
    finally:
        temporary.unlink()


def source_hashes():
    files = ['code/lab/track_c/'+name for name in (
        'c10x_enginepath_arms.py','c10x_overtone_z.py','c10x_enginepath_inertness.py',
        'c10x_enginepath_read.py','c10x_enginepath_telemetry_check.py','c10e_bandknob.py')]
    files += ['code/configs/hparams/qwen25_3b_memit_hparams.json', 'code/memit/vendor/memit/compute_z.py',
              'code/memit/vendor/memit/compute_ks.py','code/memit/vendor/memit/memit_main.py',
              'code/memit/vendor/rome/repr_tools.py','code/memit/engine_fingerprint.py',
              'code/lab/track_c/c10p_twopass_arms.py',CONTEXT_SOURCE,'experiments/c10x/design/C10X_ENGINEPATH_PREREG.md']
    return {p:sha_file(ROOT/p) for p in files}


def verify_sources(before, after):
    from c10x_enginepath_inertness import require
    require(before == after, 'SOURCE_DRIFT')


def recorded_contexts():
    path=ROOT/CONTEXT_SOURCE
    tree=ast.parse(path.read_bytes())
    assignments=[n.value for n in tree.body if isinstance(n,ast.Assign) and
                 any(isinstance(t,ast.Name) and t.id=='TEMPLATES' for t in n.targets)]
    if len(assignments)!=1:raise ValueError('recorded context source is ambiguous')
    flat=ast.literal_eval(assignments[0])
    if not isinstance(flat,(tuple,list)) or len(flat)!=6 or flat[0]!='{}' or any(type(s) is not str or s.count('{}')!=1 for s in flat):
        raise ValueError('recorded context population changed')
    ctx=[[flat[0]],list(flat[1:])]
    historical_sha=hashlib.sha256(json.dumps(ctx).encode()).hexdigest()
    if historical_sha!=C10Q_CONTEXT_SHA:raise ValueError('recorded C10Q context identity changed')
    templates_sha=json_sha(list(flat))
    if templates_sha!=C10Q_TEMPLATES_SHA:raise ValueError('recorded C10Q flat template identity changed')
    return ctx,{'source_path':CONTEXT_SOURCE,'source_sha256':sha_file(path),
                'historical_source':'experiments/c10q/runs/c10q_stacked/logs_run.log:9',
                'c10q_context_sha256':historical_sha,'templates_sha256':templates_sha}


@contextlib.contextmanager
def pinned_contexts(harness,ctx):
    namespace=harness.get_context_templates.__globals__
    if 'CONTEXT_TEMPLATES_CACHE' not in namespace or hashlib.sha256(json.dumps(ctx).encode()).hexdigest()!=C10Q_CONTEXT_SHA:
        raise ValueError('pinned contexts need the unchanged engine cache binding')
    previous=namespace['CONTEXT_TEMPLATES_CACHE']
    namespace['CONTEXT_TEMPLATES_CACHE']=copy.deepcopy(ctx)
    try:
        yield ctx
        if namespace['CONTEXT_TEMPLATES_CACHE']!=ctx:raise ValueError('CONTEXT_PIN_DRIFT')
    finally:
        namespace['CONTEXT_TEMPLATES_CACHE']=previous


def environment_identity():
    return {'python':platform.python_version(),'machine':platform.machine(),'platform':platform.platform(),
            'torch':importlib.metadata.version('torch'),'transformers':importlib.metadata.version('transformers'),
            'model_rev':'3aab1f1954e9cc14eb9509a215f9e5ca08227a9b'}


def selftest_root(root):
    root = Path(root).resolve()
    if os.environ.get('C10X_SELFTEST') and Path('/private/tmp/c10x_build') not in root.parents:
        raise ValueError('C10X_SELFTEST refuses non-temp root')
    return root


def environment_preflight():
    if not os.environ.get('LLMDB_ROOT') or Path(os.environ['LLMDB_ROOT']).resolve() != ROOT.resolve():
        raise ValueError('LLMDB_ROOT must explicitly name ROOT')
    selftest_root(ROOT)
    for knob in KNOBS:
        if knob in os.environ:
            raise ValueError('inherited knob '+knob)


def refuse_existing(out):
    if Path(out).exists():
        raise ValueError('existing output directory refused')


def fingerprint():
    spec=importlib.util.spec_from_file_location('_c10x_fingerprint',ROOT/'code/memit/engine_fingerprint.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):code=module.main()
    if code:
        raise ValueError('ENGINE_FINGERPRINT_FAIL '+buf.getvalue())
    return {'ok':True,'sha256':module.EXPECTED_SHA256,'_cov_cpu':module.EXPECTED_COV_CPU_SITES,'output':buf.getvalue()}


def process2_admission(record):
    from c10x_enginepath_read import read_record
    result=read_record(record)
    if result['status'] != 'VALID' or not any(x['eligible'] for x in result['arms'].values()):
        raise ValueError('PROCESS2_WITHOUT_ELIGIBLE_PROCESS1')
    return True


def telemetry_admission(process, out):
    from c10x_enginepath_read import strict_json
    value=os.environ.get('C10X_TELEMETRY')
    if value is None:
        return False,None
    if value != '1':
        raise ValueError('invalid C10X_TELEMETRY')
    # T9 fixes both first-attempt processes to telemetry off.
    if not re.fullmatch(r'c10x_enginepath(?:_r2)?_rerun[1-9][0-9]*',Path(out).name):
        raise ValueError('first attempt is telemetry off')
    path=Path(os.environ.get('C10X_TELEMETRY_INERTNESS',''))
    expected=ROOT/'results/c10x_enginepath_telemetry_inertness'
    if not path.is_absolute() or path.resolve().parent.parent != expected.resolve() or path.name != 'inertness.json':
        raise ValueError('invalid telemetry inertness path')
    data=path.read_bytes();r=strict_json(data)
    flags=('control_equal','telemetry_equal','generated_equal','telemetry_complete','weights_unchanged')
    if (r.get('schema')!='c10x_enginepath_telemetry_inertness/v1' or r.get('device')!='mps' or
            r.get('decision_id')!='D-C10r-rulings-11' or r.get('verdict')!='INERT' or
            any(r.get(k) is not True for k in flags) or type(r.get('answer_calls')) is not int or
            r['answer_calls']!=96 or type(r.get('lens_forwards')) is not int or r['lens_forwards']!=48 or
            r.get('sources')!=source_hashes() or r.get('env')!=environment_identity()):
        raise ValueError('telemetry inertness identity/verdict/schedule mismatch')
    for key,count in (('lens_forward_seconds',48),('answer_line_seconds',96)):
        if len(r.get(key,[]))!=count or any(type(v) not in (float,int) or not math.isfinite(v) or v<0 for v in r[key]):
            raise ValueError('telemetry timing evidence missing')
    return True,{'path':str(path.resolve()),'sha256':hashlib.sha256(data).hexdigest()}


def launch_preflight(out, go, process, process1=None):
    from c10x_enginepath_read import strict_json,audited_record,read_record
    environment_preflight()
    out=Path(out)
    if not out.is_absolute() or out.resolve().parent != (ROOT/'results').resolve():
        raise ValueError('absolute output under ROOT/results required')
    pattern=r'c10x_enginepath'+('_r2' if process==2 else '')+r'(?:_rerun[1-9][0-9]*)?'
    if process not in (1,2) or not re.fullmatch(pattern,out.name):
        raise ValueError('output/process naming mismatch')
    if not go or not Path(go).is_absolute():
        raise ValueError('absolute --go is required')
    record=strict_json(Path(go).read_bytes())
    if set(record)!={'decision_id','experiment','process','recorded_in','at'} or record['experiment']!='C10X' or type(record['process']) is not int or record['process']!=process or record['recorded_in']!='program/runbook/ §5.2' or not isinstance(record['decision_id'],str) or not record['decision_id']:
        raise ValueError('malformed go record')
    if not isinstance(record['at'],str) or datetime.datetime.fromisoformat(record['at']).tzinfo is None:
        raise ValueError('go timestamp must carry timezone')
    enabled,proof=telemetry_admission(process,out)
    first=None
    if process==2:
        if not process1:
            raise ValueError('process 2 needs process-1 directory')
        first,audit=audited_record(Path(process1));process2_admission(first)
        persisted=strict_json((Path(process1)/'reader.json').read_bytes())
        expected=read_record(first);expected['audit']=audit
        if persisted!=expected or first['telemetry'] is not enabled:
            raise ValueError('process-1 reader/telemetry mismatch')
        if enabled and first['telemetry_inertness']!=proof:
            raise ValueError('process-2 telemetry identity mismatch')
    refuse_existing(out);refuse_existing(out.with_name(out.name+'_logs'))
    sources=source_hashes()
    if sources['experiments/c10x/design/C10X_ENGINEPATH_PREREG.md']!=PIN:
        raise ValueError('PREREG SHA MISMATCH')
    return {'go':record,'go_identity':{'path':str(Path(go).resolve()),'sha256':sha_file(go)},
            'sources':sources,'fingerprint':fingerprint(),'telemetry':enabled,'telemetry_inertness':proof,'process1':first}


def project(duration, cap, remaining, reserve):
    from c10x_enginepath_inertness import Halt,require
    require(all(math.isfinite(x) and x>=0 for x in (duration,cap,remaining,reserve)), 'BAD_PROJECTION')
    try:
        require(duration<=cap and duration+reserve<=remaining, 'STAGE_PROJECTION_REFUSED')
    except Halt as exc:
        exc.budget_inputs={'projected':duration,'cap':cap,'remaining':remaining,'reserve':reserve,
                           'within_stage_cap':duration<=cap,'within_reserved_process_budget':duration+reserve<=remaining}
        raise
    return {'ok':True,'projected_seconds':duration,'cap_seconds':cap,'remaining_seconds':remaining,'reserve_seconds':reserve}


def scorer_record(value,path='record'):
    """Materialize scorer scalars at ingress; never coerce an accumulated record."""
    if value is None or type(value) is str:return value
    if isinstance(value,bool):return bool(value)
    if isinstance(value,int):return int(value)
    if isinstance(value,float):return float(value)
    if type(value) is dict:return {k:scorer_record(v,path+'.'+str(k)) for k,v in value.items()}
    if type(value) in (list,tuple):return [scorer_record(v,path+'['+str(i)+']') for i,v in enumerate(value)]
    import torch
    import numpy as np
    if isinstance(value,torch.Tensor) and value.ndim==0 and not value.is_complex():
        return scorer_record(value.detach().cpu().item(),path)
    if isinstance(value,np.bool_):return bool(value)
    if isinstance(value,np.integer):return int(value)
    if isinstance(value,np.floating):return float(value)
    raise ValueError(path+' is not a scalar scorer JSON value')


def validate_record_json(state):
    from c10x_enginepath_read import _finite_tree,strict_json
    _finite_tree(state,'record')
    encoded=json.dumps(state,allow_nan=False,sort_keys=True,separators=(',',':'))
    if strict_json(encoded)!=state:raise ValueError('record JSON roundtrip mismatch')


def halt_diagnostic(state, code):
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    path=ROOT/'architecture_profile'/('c10x_halt_diagnostic_'+stamp+'.json')
    stage=state.get('stage','setup');phase=state.get('phase',stage+':halt')
    trace=state.get('traceback');source=state.get('traceback_source','unavailable_no_python_exception')
    if trace is None and isinstance(code,BaseException) and code.__traceback__ is not None:
        trace=''.join(traceback.format_exception(type(code),code,code.__traceback__));source='python_exception'
    write_json(path,{'status':'HALTED','completion':'incomplete','code':str(code),'at':utc(),
                     'stage':stage,'phase':phase,'traceback':trace,'traceback_source':source,'state':diagnostic_json(state),
                     **({'budget_inputs':diagnostic_json(state['budget_inputs'])} if 'budget_inputs' in state else {})})
    return str(path)


def diagnostic_json(value):
    if isinstance(value,dict):return {str(k):diagnostic_json(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [diagnostic_json(v) for v in value]
    if isinstance(value,float) and not math.isfinite(value):return {'nonfinite':repr(value)}
    if value is None or isinstance(value,(str,bool,int,float)):return value
    return {'repr':repr(value),'type':type(value).__name__}


def supervise_child(argv, root, env, record, stage_seconds, process_seconds):
    selftest_root(root)
    start=WATCHDOG_CLOCK()
    child=subprocess.Popen(argv,cwd=root,env=env,start_new_session=True)
    reason=None
    while child.poll() is None:
        elapsed=WATCHDOG_CLOCK()-start
        if elapsed>=stage_seconds or elapsed>=process_seconds:
            reason='WATCHDOG_TIMEOUT';os.killpg(child.pid,signal.SIGKILL);break
        time.sleep(.03)
    code=child.wait()
    result={'status':'HALTED' if reason or code else 'COMPLETE','completion':'incomplete' if reason or code else 'complete',
            'code':reason or code,'elapsed_seconds':WATCHDOG_CLOCK()-start}
    write_json(record,result)
    return result


class Telemetry:
    def __init__(self,out,process,run_id):
        self.enabled=True;self.file=None;self.cumulative_s=0.;self.process=process;self.run_id=run_id
        self.answer_attempts=0
        self.answer_line_seconds=[];self.lens_forward_seconds=[];self.lines=[]
        try:
            started=TELEMETRY_CLOCK()
            directory=Path(out)/'telemetry';directory.mkdir(parents=True,exist_ok=True)
            self.file=(directory/f'telemetry_p{process}.jsonl').open('a',encoding='utf8')
            self._emit('header',started,schema='c10x_enginepath_telemetry/v1',telemetry=True)
        except Exception as exc:self._disable(exc)
    def _disable(self,exc,answer_cutoff=None):
        if self.enabled:
            self.enabled=False
            cutoff={'answer_cutoff':self.answer_attempts if answer_cutoff is None else answer_cutoff,
                    'process':self.process,'run_id':self.run_id}
            print(f'C10X_TELEMETRY_DISABLED {type(exc).__name__}: {exc} C10X_ANSWER_CUTOFF '+json.dumps(cutoff,sort_keys=True),file=sys.__stderr__,flush=True)
    def _emit(self,kind,started,**payload):
        line={**payload,'kind':kind,'t_utc':utc(),'elapsed_s':TELEMETRY_CLOCK()-started,
              'cumulative_s':self.cumulative_s,'process':self.process,'run_id':self.run_id}
        data=json.dumps(line,allow_nan=False,sort_keys=True,separators=(',',':'))+'\n'
        self.file.write(data);self.file.flush();os.fsync(self.file.fileno())
        duration=TELEMETRY_CLOCK()-started;self.cumulative_s+=duration;self.lines.append(line)
        if kind=='answer':self.answer_line_seconds.append(duration)
    def phase(self,event,**payload):
        try:
            if self.enabled:self._emit('phase',TELEMETRY_CLOCK(),event=event,**payload)
        except Exception as exc:self._disable(exc)
    def write_norms(self,recipe,arm,mode,harness_fp32,driver_float64=None):
        try:
            if self.enabled:
                from c10x_enginepath_inertness import fp32_report
                payload={'recipe':recipe,'arm':arm,'mode':mode,'harness_fp32':fp32_report(harness_fp32)}
                if driver_float64 is not None:payload['driver_float64']=driver_float64
                self._emit('write_norms',TELEMETRY_CLOCK(),**payload)
        except Exception as exc:self._disable(exc)
    def target_probs(self,table,values):
        try:
            if self.enabled:self._emit('target_probs',TELEMETRY_CLOCK(),table=table,values=values)
        except Exception as exc:self._disable(exc)
    def answer(self,H,recipe,phase,prompt,target_ids,gen):
        cutoff=self.answer_attempts
        try:
            if not self.enabled:return
            self.answer_attempts+=1
            started=TELEMETRY_CLOCK();rqs=H._ARM_STATE['requests']
            arms=[k for k,v in H.ARMS.items() if len(rqs)==len(v) and all(v.get(r['subject'])==r['target_new']['str'][1:] for r in rqs)]
            matches=[(s,v,t) for s,v in H.ARMS[arms[0]].items() for t in [H.CANON]+H.PTEST if t.format(s)==prompt] if len(arms)==1 else []
            if len(matches)!=1:raise ValueError('unresolved answer attribution')
            s,v,t=matches[0]
            target_ids=[int(scorer_record(i,'telemetry.target_ids')) for i in target_ids]
            gen=[int(scorer_record(i,'telemetry.generated_ids')) for i in gen]
            self._emit('answer',started,recipe=recipe,arm=arms[0],phase=phase,subj=s,val=v,template=t,
                       prompt=prompt,target_ids=target_ids,generated_ids=gen,text=H.tok.decode(gen),
                       full=bool(gen==target_ids),first=bool(gen[0]==target_ids[0]))
        except Exception as exc:self._disable(exc,answer_cutoff=cutoff)
    def logit_lens(self,H,hp,where):
        try:
            if not self.enabled:return
            started=TELEMETRY_CLOCK();snapshot=logit_lens(H,hp,self.lens_forward_seconds)
            self._emit('logit_lens',started,where=where,**snapshot)
        except Exception as exc:self._disable(exc)
    def close(self):
        try:
            if self.file is not None:self.file.close()
        except Exception as exc:self._disable(exc)


def forward_tokens(model,batch,**kwargs):
    tokens=dict(batch);mask=tokens.pop('attention_mask')
    return model(**tokens,attention_mask=mask,**kwargs)


def logit_lens(H,hp,timings=None):
    import torch
    from c10x_enginepath_inertness import require
    require(max(hp.layers)<=H.model.config.num_hidden_layers-2,'LENS_LAYER_BOUND')
    items=[]
    with torch.no_grad():
        for subject in H.FICTION:
            start=TELEMETRY_CLOCK()
            prompt=H.CANON.format(subject);ids=H.tok(prompt,return_tensors='pt').to(H.DEV)
            out=forward_tokens(H.model,ids,output_hidden_states=True,use_cache=False)
            top={}
            for l in hp.layers:
                logits=H.model.lm_head(H.model.model.norm(out.hidden_states[l+1][:,-1,:]))
                row=logits.detach().cpu().double()[0]
                require(bool(torch.isfinite(row).all()),'NONFINITE_LENS')
                best=row.softmax(-1).topk(5)
                top[str(l)]=[[int(i),H.tok.decode([int(i)]),float(p)] for i,p in zip(best.indices,best.values)]
            items.append({'subj':subject,'prompt':prompt,'top':top})
            if timings is not None:timings.append(TELEMETRY_CLOCK()-start)
    return {'layers':list(hp.layers),'items':items}


def observed_scorer(H,sink):
    import torch
    tok,model,DEV=H.tok,H.model,H.DEV
    @torch.no_grad()
    def observed_full_seq_match(prompt, target_ids):
        ids = tok(prompt, return_tensors='pt').to(DEV)['input_ids']
        cur = ids
        gen = []
        for _ in range(len(target_ids)):
            nxt = int(model(cur).logits[0, -1].argmax())
            gen.append(nxt)
            cur = torch.cat([cur, torch.tensor([[nxt]], device=DEV)], dim=1)
        sink(prompt, target_ids, gen)
        return gen == list(target_ids), gen[0] == target_ids[0]
    return observed_full_seq_match


def reference_scorer(H,capture):
    import torch
    tok,model,DEV=H.tok,H.model,H.DEV
    @torch.no_grad()
    def reference_full_seq_match(prompt, target_ids):
        ids = tok(prompt, return_tensors='pt').to(DEV)['input_ids']
        cur = ids
        gen = []
        for _ in range(len(target_ids)):
            nxt = int(model(cur).logits[0, -1].argmax())
            gen.append(nxt)
            cur = torch.cat([cur, torch.tensor([[nxt]], device=DEV)], dim=1)
        capture(prompt, target_ids, gen)
        return gen == list(target_ids), gen[0] == target_ids[0]
    return reference_full_seq_match


def verify_scorer_ast(path):
    original=next(n for n in ast.walk(ast.parse(Path(path).read_text())) if isinstance(n,ast.FunctionDef) and n.name=='full_seq_match')
    mine=ast.parse(Path(__file__).read_text())
    for name,sink in [('observed_full_seq_match','sink'),('reference_full_seq_match','capture')]:
        node=copy.deepcopy(next(n for n in ast.walk(mine) if isinstance(n,ast.FunctionDef) and n.name==name))
        extra=node.body.pop(-2)
        expected=ast.parse(sink+'(prompt, target_ids, gen)').body[0]
        if ast.dump(extra)!=ast.dump(expected):return False
        node.name='full_seq_match'
        if ast.dump(node)!=ast.dump(original):return False
    return True


def configure(harness):
    global H,ORIGINAL_EDIT,ORIGINAL_SCORER
    if H is harness and harness.my_edit is dispatch:return
    H=harness;ORIGINAL_EDIT=H.my_edit;ORIGINAL_SCORER=H.full_seq_match
    names=('model','tok','DEV','get_context_templates','compute_z','compute_ks','get_module_input_output_at_words',
           'weight_name','upd_matrix_match_shape','PROJECTOR','L2')
    for name in names:globals()[name]=getattr(H,name)
    globals()['torch']=__import__('torch')
    _refresh_globals();H.my_edit=dispatch


def _refresh_globals():
    global _LAW5_DEFAULT_CTX,_CANDIDATE_RECIPE,Z_OVERRIDE,Z_OVERRIDE_HITS
    _LAW5_DEFAULT_CTX=H._LAW5_DEFAULT_CTX;_CANDIDATE_RECIPE=H._CANDIDATE_RECIPE
    Z_OVERRIDE=H.Z_OVERRIDE;Z_OVERRIDE_HITS=H.Z_OVERRIDE_HITS
    if hasattr(ORIGINAL_EDIT,'__globals__'):
        for name in ('Z_OVERRIDE','Z_OVERRIDE_HITS','_LAW5_DEFAULT_CTX','_CANDIDATE_RECIPE'):
            ORIGINAL_EDIT.__globals__[name]=globals()[name]


def release(harness):
    global FE_STATE,FE_TARGETS,FE_CALLS,IN_RECIPE,H,TELEMETRY
    if H is harness and harness.my_edit is dispatch:harness.my_edit=ORIGINAL_EDIT
    FE_STATE=None;FE_TARGETS={};FE_CALLS=0;IN_RECIPE=False;TELEMETRY=None
    harness.Z_OVERRIDE=None;H=None


def _check_fe_keys(hp,requests,mode):
    from c10x_enginepath_inertness import require
    require(mode in ('fe','identity'),'FE_MODE')
    require(not (mode=='identity' and IN_RECIPE),'IDENTITY_IN_RECIPE')
    if mode=='fe':
        for rq in requests:
            key=(rq['subject'],rq['target_new']['str'])
            require(key in FE_TARGETS,'MISSING_FE_TARGET')
            require(set(FE_TARGETS[key])==set(hp.layers),'FE_LAYER_KEYS')
    else:
        require(H.Z_OVERRIDE is not None and all((r['subject'],r['target_new']['str']) in H.Z_OVERRIDE for r in requests),'IDENTITY_TARGETS')


def _identity_zs(keys):
    return torch.stack([H.Z_OVERRIDE[k].to(DEV) for k in keys],dim=1)


def fe_edit(hp, requests, P, cache_c, mode="fe"):
    ctx = get_context_templates(model, tok) if (os.environ.get("C10_CTX_TEMPLATES", "on") != "off" or _LAW5_DEFAULT_CTX) else [["{}"]]   # D-C10k-keying-ablation knob: off = identity template only; the LAW#5 parity check always uses the engine defaults
    layers = hp.layers
    z_layer = layers[-1]
    keys = [(rq["subject"], rq["target_new"]["str"]) for rq in requests]
    _check_fe_keys(hp, requests, mode)
    zs = _identity_zs(keys) if mode == 'identity' else None
    npd = dict(model.named_parameters())
    delta_norms = {}
    for i, layer in enumerate(layers):
        if mode == 'fe':
            zs = torch.stack([FE_TARGETS[k][layer].to(DEV) for k in keys], dim=1)
        before = npd[weight_name(hp, layer)].detach().float().norm().item()
        K = compute_ks(model, tok, requests, hp, layer, ctx).T
        cur = get_module_input_output_at_words(
            model, tok, z_layer if mode == 'identity' else layer, context_templates=[rq["prompt"] for rq in requests],
            words=[rq["subject"] for rq in requests], module_template=hp.layer_module_tmp,
            fact_token_strategy=hp.fact_token
        )[1].T
        tgt = zs - cur
        tgt = tgt.repeat_interleave(K.size(1) // tgt.size(1), dim=1)
        resid = tgt / (len(layers) - i) if mode == 'identity' else tgt
        Kf = K.float()
        rf = resid.float()
        Pi = torch.eye(Kf.shape[0]) if (PROJECTOR == "identity" and _CANDIDATE_RECIPE and not _LAW5_DEFAULT_CTX) else P[i]   # D-C10l-covgeom arm B: P := I, nothing else changes
        ca = cache_c[i]
        A = Pi @ (Kf.cpu() @ Kf.cpu().T + ca) + L2 * torch.eye(Kf.shape[0])
        B = Pi @ Kf.cpu() @ rf.cpu().T
        upd = torch.linalg.solve(A, B).T
        upd = upd_matrix_match_shape(upd.float(), npd[weight_name(hp, layer)].shape)
        upd_norm = float(upd.float().norm())
        rel = upd_norm / max(before, 1e-12)
        delta_norms[str(layer)] = {"delta_norm": upd_norm, "weight_norm_before": before, "relative_delta_norm": rel}
        with torch.no_grad():
            npd[weight_name(hp, layer)][...] += upd.cpu().to(dtype=npd[weight_name(hp, layer)].dtype).to(npd[weight_name(hp, layer)].device)
    for i, layer in enumerate(layers):
        K = compute_ks(model, tok, requests, hp, layer, ctx).T.float().cpu()
        cache_c[i] = cache_c[i] + K @ K.T
    return delta_norms


def verify_fe_ast(path):
    original=next(n for n in ast.walk(ast.parse(Path(path).read_text())) if isinstance(n,ast.FunctionDef) and n.name=='my_edit')
    own=copy.deepcopy(next(n for n in ast.walk(ast.parse(Path(__file__).read_text())) if isinstance(n,ast.FunctionDef) and n.name=='fe_edit'))
    if ast.unparse(own.body[4])!='_check_fe_keys(hp, requests, mode)':return False
    if ast.unparse(own.body[5])!="zs = _identity_zs(keys) if mode == 'identity' else None":return False
    own.body[4:6]=[copy.deepcopy(original.body[4])]
    loop=own.body[7]
    if ast.unparse(loop.body[0])!="if mode == 'fe':\n    zs = torch.stack([FE_TARGETS[k][layer].to(DEV) for k in keys], dim=1)":return False
    loop.body.pop(0)
    cur=loop.body[2]
    # The reader argument and residual expression are the other two changes.
    call=next(n for n in ast.walk(cur) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='get_module_input_output_at_words')
    if ast.unparse(call.args[2])!="z_layer if mode == 'identity' else layer":return False
    call.args[2]=ast.Name(id='z_layer',ctx=ast.Load())
    resid=loop.body[5]
    if ast.unparse(resid)!="resid = tgt / (len(layers) - i) if mode == 'identity' else tgt":return False
    resid.value=copy.deepcopy(original.body[7].body[5].value)
    writes=[n for n in ast.walk(own) if isinstance(n,ast.AugAssign)]
    old_writes=[n for n in ast.walk(original) if isinstance(n,ast.AugAssign)]
    safe=ast.parse('upd.cpu().to(dtype=npd[weight_name(hp, layer)].dtype).to(npd[weight_name(hp, layer)].device)',mode='eval').body
    writes=[n for n in writes if isinstance(n.target,ast.Subscript)]
    old_writes=[n for n in old_writes if isinstance(n.target,ast.Subscript)]
    if len(writes)!=1 or len(old_writes)!=1 or ast.dump(writes[0].value)!=ast.dump(safe):return False
    writes[0].value=copy.deepcopy(old_writes[0].value)
    own.name='my_edit';own.args=copy.deepcopy(original.args)
    return ast.dump(own)==ast.dump(original)


def _arm_identity(requests):
    matches=[k for k,values in H.ARMS.items() if len(requests)==len(values) and
             all(values.get(r['subject'])==r['target_new']['str'][1:] for r in requests)]
    from c10x_enginepath_inertness import require
    require(len(matches)==1,'WRITE_ARM_ATTRIBUTION')
    return matches[0]


@contextlib.contextmanager
def write_diagnostics(writer,harness,hp,requests,table=None):
    """Observe completed layer updates through the writer's resolved key seam."""
    import torch
    from c10x_enginepath_inertness import cpu_copy,ratio64,norm64,require
    namespace=writer.__globals__;original_ks=namespace['compute_ks'];original_z=namespace['compute_z']
    keys=[(r['subject'],r['target_new']['str']) for r in requests];solved={};record={'rho':{}};calls=0;before=None;target=None
    weights_before={l:cpu_copy(dict(harness.model.named_parameters())[harness.weight_name(hp,l)]) for l in hp.layers}
    def z_observer(model,tok,request,hparams,layer,ctx):
        value=original_z(model,tok,request,hparams,layer,ctx)
        solved[(request['subject'],request['target_new']['str'])]=cpu_copy(value)
        return value
    def keys_observer(*args,**kwargs):
        nonlocal calls,before,target
        if calls==0:
            if table is not None:
                vectors=[table[k][hp.layers[-1]] if isinstance(table[k],dict) else table[k] for k in keys]
            elif harness.Z_OVERRIDE is not None:vectors=[harness.Z_OVERRIDE[k] for k in keys]
            else:vectors=[solved[k] for k in keys]
            target=cpu_copy(torch.stack(vectors));before=cpu_copy(canonical_read(harness,hp,hp.layers[-1],requests))
            record['target_sha256']=tensor_hash(target);record['cur_before_sha256']=tensor_hash(before)
        elif calls<=len(hp.layers):
            after=cpu_copy(canonical_read(harness,hp,hp.layers[-1],requests))
            record['rho'][str(hp.layers[calls-1])]=ratio64(target-after,target-before)
            if calls==len(hp.layers):
                record['end_ratio']=record['rho'][str(hp.layers[-1])]
                record['cur_after_sha256']=tensor_hash(after)
        calls+=1
        return original_ks(*args,**kwargs)
    namespace['compute_z']=z_observer;namespace['compute_ks']=keys_observer
    try:
        yield record
        require(set(record['rho'])=={str(l) for l in hp.layers},'RESIDUAL_DIAGNOSTIC_LAYERS')
        record['applied_difference_report_only']={str(l):{
            'norm_float64':norm64(cpu_copy(dict(harness.model.named_parameters())[harness.weight_name(hp,l)])-weights_before[l]),
            'weight_norm_before_float64':norm64(weights_before[l])} for l in hp.layers}
    finally:
        namespace['compute_z']=original_z;namespace['compute_ks']=original_ks


def dispatch(hp,requests,P,cache_c):
    global FE_CALLS,FE_TARGETS,ARM_UNIT
    import c10x_enginepath_inertness as I
    _refresh_globals()
    active=FE_STATE is not None and not H._LAW5_DEFAULT_CTX
    writer=fe_edit if active else ORIGINAL_EDIT
    if active:
        FE_CALLS+=1
        if 'targets' in FE_STATE:FE_TARGETS=FE_STATE['targets']
    # G remains entirely on the saved original path, outside recipe capture.
    if H._LAW5_DEFAULT_CTX:
        result=ORIGINAL_EDIT(hp,requests,P,cache_c)
        H.Z_OVERRIDE_HITS=ORIGINAL_EDIT.__globals__.get('Z_OVERRIDE_HITS',H.Z_OVERRIDE_HITS)
        I.require(FE_CALLS==0 or IN_RECIPE,'CANDIDATE_SEAM_DURING_G')
        return result
    if not IN_RECIPE:
        return writer(hp,requests,P,cache_c)
    ARM_UNIT=work_unit(kind='recipe_arm')
    arm=_arm_identity(requests)
    attr={'writer':writer.__name__,'check':'recipe','recipe':ACTIVE_RECIPE,'arm':arm}
    with write_diagnostics(writer,H,hp,requests,FE_TARGETS if active else None) as diagnostics:
        with I.capture_updates(writer,hp.layers,attr,retain=False) as captured:
            result=writer(hp,requests,P,cache_c)
    if not active:H.Z_OVERRIDE_HITS=ORIGINAL_EDIT.__globals__.get('Z_OVERRIDE_HITS',H.Z_OVERRIDE_HITS)
    WRITE_NORMS[arm]={str(r['layer']):r['norm_float64'] for r in captured}
    RHO[arm]=diagnostics
    result=I.fp32_report(result)
    if TELEMETRY is not None:
        TELEMETRY.write_norms(ACTIVE_RECIPE,arm,'fe' if active else 'original',result,diagnostics['rho'] if active else None)
    return result


def recipe(harness,name,path,fe,ot,pristine,telemetry=None):
    global FE_STATE,FE_CALLS,IN_RECIPE,ACTIVE_RECIPE,TELEMETRY,WRITE_NORMS,RHO
    configure(harness)
    pristine.verify('before recipe '+name)
    FE_STATE=({'targets':fe} if 'targets' not in fe else fe) if name=='I-2' else None
    H.Z_OVERRIDE=ot if name=='I-1' else None
    H.Z_OVERRIDE_HITS=0;FE_CALLS=0;IN_RECIPE=True;ACTIVE_RECIPE=name;TELEMETRY=telemetry;WRITE_NORMS={};RHO={}
    original_scorer=ORIGINAL_SCORER
    try:
        if telemetry is None:
            assert H.full_seq_match is ORIGINAL_SCORER
        else:
            H.full_seq_match=observed_scorer(H,lambda p,t,g:telemetry.answer(H,name,name,p,t,g))
            telemetry.phase('recipe_start',recipe=name)
        with recipe_checks(H,pristine) as gate_audit:
            result=scorer_record(H.run_recipe(name,str(Path(path).resolve())),'record.recipes.'+name)
        expected={'A':(0,0),'I-2':(0,3),'I-1':(3,0)}[name]
        from c10x_enginepath_inertness import require
        require((H.Z_OVERRIDE_HITS,FE_CALLS)==expected,'RECIPE_COUNTER_MISMATCH')
        result['counters']=[H.Z_OVERRIDE_HITS,FE_CALLS]
        result['write_norms_float64']=copy.deepcopy(WRITE_NORMS)
        result['residual_diagnostics']=copy.deepcopy(RHO)
        if 'delta_norms' in result:
            from c10x_enginepath_inertness import fp32_report
            result['delta_norms']=fp32_report(result['delta_norms'])
        if gate_audit:result['law5_gate'].update(gate_audit)
        enrich_recipe(result)
        return result
    finally:
        H.full_seq_match=original_scorer
        FE_STATE=None;H.Z_OVERRIDE=None;IN_RECIPE=False;ACTIVE_RECIPE=None;TELEMETRY=None
        _refresh_globals();pristine.restore();pristine.verify('after recipe '+name)
        if telemetry is not None:telemetry.phase('recipe_end',recipe=name)


@contextlib.contextmanager
def recipe_checks(harness,pristine):
    """Keep harness cells unchanged and audit their original resolved bindings."""
    from c10x_enginepath_inertness import require
    audit={};namespace=getattr(harness.run_recipe,'__globals__',{})
    original_restore=namespace.get('restore_layers');original_gate=namespace.get('run_law5')
    def restore(*args,**kwargs):
        value=original_restore(*args,**kwargs);pristine.verify('harness restore');return value
    def gate(*args,**kwargs):
        started=work_unit(kind='G')
        gate_ns=original_gate.__globals__;predict_fn=gate_ns['predict'];observations=[]
        before=FE_CALLS,harness.Z_OVERRIDE_HITS
        def predict(prompt):
            value=predict_fn(prompt);observations.append((prompt,value));return value
        gate_ns['predict']=predict
        try:result=original_gate(*args,**kwargs)
        finally:gate_ns['predict']=predict_fn
        require((FE_CALLS,harness.Z_OVERRIDE_HITS)==before,'CANDIDATE_SEAM_DURING_G')
        require(len(observations)==6,'G_OBSERVATION_SCHEDULE')
        canonical=harness.CANON.format('Zorbland');local='Zorbland is described as'
        pre=dict(observations[:2]);engine=dict(observations[2:4]);mine=dict(observations[4:])
        token=harness.first_tok('Cairo')
        audit.update(raw_expr_delta=abs(float(engine[canonical]['dist'][token])-float(mine[canonical]['dist'][token])),
            raw_loc_delta=float(abs(harness.locpct(engine,pre,[local])-harness.locpct(mine,pre,[local]))),candidate_calls=0)
        end_unit(started)
        return result
    if original_restore is not None:namespace['restore_layers']=restore
    if original_gate is not None:namespace['run_law5']=gate
    try:yield audit
    finally:
        if original_restore is not None:namespace['restore_layers']=original_restore
        if original_gate is not None:namespace['run_law5']=original_gate


def enrich_recipe(result):
    for arm,rows in result.get('detail',{}).items():
        x=result['arms'][arm]
        x['per_fact']=[sum(r['para_full_hits']) for r in rows]
        x['per_template']=[sum(r['para_full_hits'][k] for r in rows) for k in range(3)]
        x['tf_continuation_n']=sum(r['tf_total'] for r in rows)
        x['tf_pertok_cont_reason']='zero denominator' if x['tf_continuation_n']==0 else None
        x['cond_full_given_first_reason']='zero denominator' if x['para_first_n']==0 else None


def canonical_read(harness,hp,layer,requests):
    return harness.get_module_input_output_at_words(harness.model,harness.tok,layer,
        context_templates=[r['prompt'] for r in requests],words=[r['subject'] for r in requests],
        module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1]


def batch_replay(harness,hp,requests,overwrite=None):
    import torch
    from c10x_enginepath_inertness import cpu_copy,require
    indices=[harness.find_fact_lookup_idx(r['prompt'],r['subject'],harness.tok,hp.fact_token,verbose=False) for r in requests]
    batch=harness.tok([r['prompt'].format(r['subject']) for r in requests],return_tensors='pt',padding=True).to(harness.DEV)
    # repr_tools batches these <=128 rows in this same tokenizer/padding shape.
    captured={};handles=[]
    def callback(layer):
        def fn(module,inp,out):
            hid=out[0] if isinstance(out,tuple) else out
            if overwrite is not None and layer==hp.layers[0]:
                for row,idx in enumerate(indices):hid[row,idx,:]=overwrite[row].cpu().to(dtype=hid.dtype).to(hid.device)
            captured[layer]=cpu_copy(torch.stack([hid[row,idx] for row,idx in enumerate(indices)]))
            return out
        return fn
    try:
        for layer in hp.layers:handles.append(harness.model.model.layers[layer].register_forward_hook(callback(layer)))
        with torch.no_grad():forward_tokens(harness.model,batch)
    finally:
        for handle in handles:handle.remove()
    require(set(captured)==set(hp.layers),'REPLAY_LAYER_CAPTURE')
    return captured,{'input_ids':batch['input_ids'].cpu().tolist(),'attention_mask':batch['attention_mask'].cpu().tolist(),
                     'padding_side':harness.tok.padding_side,'indices':[int(i) for i in indices],
                     'requests':[[r['subject'],r['target_new']['str']] for r in requests]}


def telemetry_mps_inertness_check(harness,hp,out,run_id):
    import torch
    from c10x_enginepath_inertness import cpu_copy,tensor_sha
    values=harness.ARMS[ARM_NAMES[2]]
    requests=[harness.req(harness.CANON,s,values[s]) for s in harness.FICTION]
    original=harness.full_seq_match
    weights={str(l):tensor_sha(dict(harness.model.named_parameters())[harness.weight_name(hp,l)]) for l in hp.layers}
    def science():return {l:cpu_copy(canonical_read(harness,hp,l,requests)) for l in hp.layers}
    original(harness.CANON.format(harness.FICTION[0]),harness.tgt_ids(values[harness.FICTION[0]]))
    canonical_read(harness,hp,hp.layers[0],requests)
    writer=None
    def one_pass(telemetry):
        generated=[];flags=[]
        if telemetry:
            writer.logit_lens(harness,hp,'before')
            scorer=observed_scorer(harness,lambda p,t,g:(generated.append(list(g)),writer.answer(harness,'A7_check','check',p,t,g)))
        else:scorer=reference_scorer(harness,lambda p,t,g:generated.append(list(g)))
        for subject in harness.FICTION:
            for template in [harness.CANON]+harness.PTEST:
                flags.append(scorer(template.format(subject),harness.tgt_ids(values[subject])))
        if telemetry:writer.logit_lens(harness,hp,'after')
        return generated,flags,science()
    oldstate=harness._ARM_STATE
    try:
        p1=one_pass(False)
        harness._ARM_STATE={'requests':requests}
        writer=Telemetry(out,1,run_id);interleaved=one_pass(True);p2=one_pass(False)
    finally:
        harness._ARM_STATE=oldstate
        if writer is not None:writer.close()
    after={str(l):tensor_sha(dict(harness.model.named_parameters())[harness.weight_name(hp,l)]) for l in hp.layers}
    def equal(a,b):return a[0]==b[0] and a[1]==b[1] and all(torch.equal(a[2][l],b[2][l]) for l in hp.layers)
    control_equal=equal(p1,p2);telemetry_equal=equal(p1,interleaved)
    answers=[r for r in writer.lines if r['kind']=='answer'];lenses=[r for r in writer.lines if r['kind']=='logit_lens']
    complete=writer.enabled and len(answers)==96 and len(lenses)==2 and all(len(x['items'])==24 for x in lenses)
    generated_equal=control_equal and p1[0]==interleaved[0]
    line_equal=len(answers)==96 and all(a['generated_ids']==g and (a['full'],a['first'])==f for a,g,f in zip(answers,interleaved[0],interleaved[1]))
    verdict=('INVALID' if not complete or weights!=after else 'NONDETERMINISTIC-BASELINE' if not control_equal else
             'INERT' if telemetry_equal and line_equal else 'NOT-INERT')
    return {'verdict':verdict,'control_equal':control_equal,'telemetry_equal':telemetry_equal,
            'generated_equal':generated_equal,'telemetry_complete':complete,'weights_unchanged':weights==after,
            'answer_calls':len(answers),'lens_forwards':len(writer.lens_forward_seconds),
            'lens_forward_seconds':writer.lens_forward_seconds,'answer_line_seconds':writer.answer_line_seconds,
            'scope':'pristine generated IDs/flags and canonical batch tensors only; edited-output and resource inertness UNVERIFIED'}


class StageBudget:
    """The worker projects work; the independent parent enforces deadlines."""
    def __init__(self,out,first=None,telemetry=None,start=None):
        self.out=Path(out);self.start=WATCHDOG_CLOCK() if start is None else start;self.stage=None;self.stage_start=None
        self.timings={};self.units={};self.first=first or {};self.telemetry=telemetry;self.remaining={}
    def halt_inputs(self,exc,name,boundary,kind,elapsed,previous,predicted,previous_overhead,projected,remaining,reserve,process_elapsed,deadline=None):
        units=self.units.get(name,{}) if boundary=='unit' else {}
        counts=self.remaining if boundary=='unit' else UNIT_PLAN[name]
        exc.budget_inputs=copy.deepcopy({'stage':name,'boundary':boundary,'kind':kind,'cap':CAPS[name],'elapsed':elapsed,
            'units_so_far':units,'units_so_far_counts':{k:len(units.get(k,[])) for k in dict.fromkeys([*counts,*units])},'remaining_units':counts,
            'first':self.first,'previous':previous,'measured_previous':self.first.get(name,0.),'predicted':predicted,
            'previous_overhead':previous_overhead,'projected':projected,'remaining':remaining,'reserve':reserve,
            'process_elapsed_at_projection':process_elapsed,'process_remaining_at_projection':PROCESS_BUDGET-process_elapsed,
            'within_stage_cap':projected<=CAPS[name],'within_reserved_process_budget':projected+reserve<=remaining,
            'deadline':deadline or {'checked':False}})
    def enter(self,name):
        from c10x_enginepath_inertness import Halt
        if self.stage is not None:self.leave()
        names=list(CAPS);reserve=sum(CAPS[n] for n in names[names.index(name)+1:])
        measured=self.first.get(name,0.)
        previous=self.first.get('work_units',{}).get(name,{})
        predicted=sum(max(previous.get(kind,[0.]))*count for kind,count in UNIT_PLAN[name].items())
        previous_overhead=max(0.,measured-sum(sum(v) for v in previous.values()))
        predicted+=previous_overhead
        projected=max(CAPS[name],measured,predicted)
        process_elapsed=0. if name=='setup' else WATCHDOG_CLOCK()-self.start
        remaining=PROCESS_BUDGET-process_elapsed
        try:receipt=project(projected,CAPS[name],remaining,reserve)
        except Halt as exc:
            self.halt_inputs(exc,name,'entry',None,0.,previous,predicted,previous_overhead,projected,remaining,reserve,process_elapsed)
            raise
        self.stage=name;self.stage_start=self.start if name=='setup' else WATCHDOG_CLOCK();self.units[name]={};self.remaining=UNIT_PLAN[name].copy()
        # This small replaceable checkpoint is control state, never science evidence.
        tmp=self.out/'stage.next';data={'stage':name,'started_monotonic':self.stage_start,'projection':receipt}
        tmp.write_text(json.dumps(data,allow_nan=False,sort_keys=True));os.replace(tmp,self.out/'stage.json')
        if self.telemetry:self.telemetry.phase('stage_start',stage=name)
    def unit(self,remaining_units=None,kind=None):
        from c10x_enginepath_inertness import Halt,require
        elapsed=WATCHDOG_CLOCK()-self.stage_start;cap=CAPS[self.stage]
        names=list(CAPS);reserve=sum(CAPS[n] for n in names[names.index(self.stage)+1:])
        kind=kind or 'unit'
        if remaining_units is not None:self.remaining[kind]=remaining_units
        previous=self.first.get('work_units',{}).get(self.stage,{})
        predicted=sum(max(self.units[self.stage].get(k,[])+previous.get(k,[])+[0.])*n for k,n in self.remaining.items())
        previous_overhead=max(0.,self.first.get(self.stage,0.)-sum(sum(v) for v in previous.values()))
        projected=max(cap,elapsed+predicted+previous_overhead)
        process_elapsed=WATCHDOG_CLOCK()-self.start
        remaining=PROCESS_BUDGET-process_elapsed+elapsed
        deadline={'checked':False}
        try:
            project(projected,cap,remaining,reserve)
            deadline_elapsed=WATCHDOG_CLOCK()-self.start if elapsed<cap else None
            deadline={'checked':True,'elapsed_below_cap':elapsed<cap,'process_clock_sampled':deadline_elapsed is not None,
                      'process_elapsed':deadline_elapsed,'process_elapsed_below_limit':deadline_elapsed<PROCESS_BUDGET if deadline_elapsed is not None else None}
            require(elapsed<cap and deadline_elapsed<PROCESS_BUDGET,'WORKER_DEADLINE')
        except Halt as exc:
            self.halt_inputs(exc,self.stage,'unit',kind,elapsed,previous,predicted,previous_overhead,projected,remaining,reserve,process_elapsed,deadline)
            raise
        return (WATCHDOG_CLOCK(),kind)
    def done(self,started):
        from c10x_enginepath_inertness import require
        began,kind=started;self.units[self.stage].setdefault(kind,[]).append(WATCHDOG_CLOCK()-began)
        if kind in self.remaining:
            self.remaining[kind]-=1
            if self.remaining[kind]<0:raise ValueError('work-unit plan undercount '+kind)
        require(WATCHDOG_CLOCK()-self.stage_start<=CAPS[self.stage] and WATCHDOG_CLOCK()-self.start<=PROCESS_BUDGET,'WORK_UNIT_DEADLINE')
    def leave(self):
        from c10x_enginepath_inertness import require
        self.timings[self.stage]=WATCHDOG_CLOCK()-self.stage_start
        require(self.timings[self.stage]<=CAPS[self.stage] and WATCHDOG_CLOCK()-self.start<=PROCESS_BUDGET,'STAGE_DEADLINE')
        if self.telemetry:self.telemetry.phase('stage_end',stage=self.stage)
        self.stage=None


def work_unit(remaining=None,kind=None):
    return BUDGET.unit(remaining,kind) if BUDGET else None


def end_unit(started):
    if BUDGET and started is not None:BUDGET.done(started)


def solve_target(harness,hp,request,layer,ctx,solver=None,settings=None,audit=None):
    import torch
    import c10x_overtone_z as Z
    from c10x_enginepath_inertness import cpu_copy,norm64,require
    started=work_unit(kind='solve');stream=io.StringIO();initial={};handle=None;stop={}
    ids=harness.tok(request['target_new']['str'],return_tensors='pt')['input_ids'][0]
    rewriting=[c.format(request['prompt'])+harness.tok.decode(ids[:-1]) for group in ctx for c in group]
    prompts=rewriting+['{} is a']
    batch=harness.tok([p.format(request['subject']) for p in prompts],return_tensors='pt',padding=True)
    idx=harness.find_fact_lookup_idx(prompts[0],request['subject'],harness.tok,hp.fact_token,verbose=False)
    def observe(module,inputs,output):
        if not initial:
            hidden=output[0] if isinstance(output,tuple) else output
            initial['vector']=cpu_copy(hidden[0,idx]);initial['shape']=list(hidden.shape)
    old_sink=Z.AUDIT_SINK
    previous_profile=sys.getprofile()
    require(previous_profile is None,'PREEXISTING_SOLVER_PROFILER')
    fn=solver or harness.compute_z
    def stopping_observer(frame,event,arg):
        if event=='return' and frame.f_code is fn.__code__:
            stop['loss']=float(frame.f_locals['loss'].detach().cpu())
            stop['step']=int(frame.f_locals['it'])
    try:
        handle=harness.model.model.layers[layer].register_forward_hook(observe)
        if audit is not None:Z.AUDIT_SINK=audit
        with contextlib.redirect_stdout(stream):
            sys.setprofile(stopping_observer)
            result=fn(harness.model,harness.tok,request,hp,layer,ctx,**(settings or {}))
        target=cpu_copy(result)
    finally:
        if handle is not None:handle.remove()
        Z.AUDIT_SINK=old_sink
        sys.setprofile(previous_profile)
    lines=[x for x in stream.getvalue().splitlines() if x.startswith('loss ')]
    require(bool(lines),'TARGET_FIT_OR_STEPS_MISSING')
    match=re.fullmatch(r'loss ([^ ]+) = .* avg prob of \[.*\] ([^ ]+)',lines[-1])
    require(match is not None,'TARGET_FIT_FORMAT')
    fit=float(match[2]);require(math.isfinite(fit),'NONFINITE_TARGET_FIT')
    require(math.isfinite(stop['loss']) and stop['step']+1==len(lines),'SOLVER_STOP_IDENTITY')
    reason='total loss < 0.05' if stop['loss']<.05 else 'step cap'
    diag={'request':[request['subject'],request['target_new']['str']],'fit':fit,'steps':len(lines),
          'stop_reason':reason,'total_loss_at_stop':stop['loss'],'norm_float64':norm64(target),'sha256':tensor_hash(target),
          'stdout':stream.getvalue(),'target_init':{'sha256':tensor_hash(initial['vector']),
             'norm_float64':norm64(initial['vector']),'shape':initial['shape'],
             'input_ids':batch['input_ids'].tolist(),'attention_mask':batch['attention_mask'].tolist(),
             'contexts':ctx,'lookup_index':idx,'dtype':str(result.dtype)}}
    if solver is not None and settings is not None:
        diag['per_position_at_stop']=copy.deepcopy(Z.LAST_STEP)
    end_unit(started)
    return target,diag,initial['vector']


def tensor_hash(tensor):
    from c10x_enginepath_inertness import tensor_sha
    return tensor_sha(tensor)


def fe_builder(harness,hp,requests,ctx):
    from c10x_enginepath_inertness import require,cpu_copy,norm64
    table={};diagnostics=[];initials=[]
    for r in requests:
        z,d,initial=solve_target(harness,hp,r,hp.layers[0],ctx)
        table[(r['subject'],r['target_new']['str'])]={hp.layers[0]:z}
        diagnostics.append(d);initials.append(initial)
    plain,meta=batch_replay(harness,hp,requests)
    replay,replay_meta=batch_replay(harness,hp,requests,
        [table[(r['subject'],r['target_new']['str'])][hp.layers[0]] for r in requests])
    require(meta==replay_meta,'REPLAY_TOKEN_IDENTITY')
    for row,r in enumerate(requests):
        for layer in hp.layers[1:]:table[(r['subject'],r['target_new']['str'])][layer]=cpu_copy(replay[layer][row])
        diagnostics[row]['target_init_vs_canonical']={
            'distance_float64':norm64(initials[row]-plain[hp.layers[0]][row]),
            'canonical_sha256':tensor_hash(plain[hp.layers[0]][row]),'canonical_batch_shape':list(plain[hp.layers[0]].shape),
            'scope':'different solve/canonical batch shapes; diagnostic only'}
    return table,diagnostics,meta


def table_record(table,diagnostics):
    from c10x_enginepath_inertness import norm64
    entries=[]
    for key,value in table.items():
        layers=value if isinstance(value,dict) else {'target':value}
        entries.append({'request':list(key),'layers':{str(l):{'sha256':tensor_hash(v),'norm_float64':norm64(v)} for l,v in layers.items()}})
    return {'sha256':json_sha(entries),'entries':entries,'diagnostics':diagnostics}


def save_binary(path,data):
    import torch
    path=Path(path)
    with path.open('xb') as f:
        torch.save(data,f);f.flush();os.fsync(f.fileno())
    return {'path':str(path.resolve()),'sha256':sha_file(path)}


def construct_targets(out,harness,hp,ctx,pristine):
    import c10x_overtone_z as Z
    import torch
    from c10x_enginepath_inertness import cpu_copy,require,ratio64
    pristine.verify('before target construction')
    engine8={};fe={};overtone={};diagnostics={k:[] for k in ('engine8','engine4','overtone')};metadata={};files=[]
    for arm in ARM_NAMES:
        requests=[harness.req(harness.CANON,s,harness.ARMS[arm][s]) for s in harness.FICTION]
        for r in requests:
            key=(r['subject'],r['target_new']['str'])
            engine8[key],diag,_=solve_target(harness,hp,r,8,ctx)
            diagnostics['engine8'].append(diag)
        built,diags,meta=fe_builder(harness,hp,requests,ctx);fe.update(built)
        diagnostics['engine4'].extend(diags);metadata[arm]=meta
        for r in requests:
            snapshots=[]
            def audit_capture(step,payload):
                labels=payload['labels'];scored=payload['mask'].bool()
                rows,positions=payload['positions'].unbind(1)
                snapshots.append({'arm':arm,'subject':r['subject'],'at':'initial' if step==0 else 'final',
                    'logits':payload['logits'].clone(),'log_probs':payload['log_probs'].clone(),
                    'labels':labels.clone(),'ce':payload['ce'].clone(),
                    'row_map':rows.tolist(),'position_map':positions.tolist(),'mask':scored.clone(),
                    'dtype':str(payload['logits'].dtype),'settings':{'lam':.1,'eps':.01,'n_sigma':.5},
                    'observed':{'keep':payload['keep'].clone(),'mix':payload['mix'].clone(),
                                'pi_tar':payload['pi_tar'].clone(),'loss':payload['loss'].clone()}})
                # Retain step zero and the current final evaluated step only.
                if len(snapshots)>2:del snapshots[1]
            need_audit=r['subject']=='Zorbland' and arm in ('A1_single','A7_coined_coined')
            key=(r['subject'],r['target_new']['str'])
            overtone[key],diag,_=solve_target(harness,hp,r,8,ctx,Z.compute_z_overtone,
                {'lam':.1,'eps':.01,'n_sigma':.5},audit_capture if need_audit else None)
            diagnostics['overtone'].append(diag)
            if need_audit:
                require(bool(snapshots),'AUDIT_SNAPSHOTS_MISSING')
                if len(snapshots)==1:
                    final={**snapshots[0],'at':'final'};snapshots.append(final)
                snapshots[-1]['at']='final'
                files.append(save_binary(Path(out)/('audit_'+arm+'.pt'),{'snapshots':snapshots}))
    records={'engine8':table_record(engine8,diagnostics['engine8']),
             'engine4':table_record(fe,diagnostics['engine4']),
             'overtone':table_record(overtone,diagnostics['overtone'])}
    a7keys={(s,' '+harness.ARMS[ARM_NAMES[2]][s]) for s in harness.FICTION}
    records['engine4']['a7_fit']=[d['fit'] for d in diagnostics['engine4'] if tuple(d['request']) in a7keys]
    records['engine4']['replay_identity']=metadata
    endpoint={}
    for arm in ARM_NAMES:
        requests=[harness.req(harness.CANON,s,harness.ARMS[arm][s]) for s in harness.FICTION]
        before=cpu_copy(canonical_read(harness,hp,8,requests))
        z8=torch.stack([engine8[(r['subject'],r['target_new']['str'])] for r in requests])
        m8=torch.stack([fe[(r['subject'],r['target_new']['str'])][8] for r in requests])
        endpoint[arm]=ratio64(m8-z8,z8-before)
    records['engine4']['endpoint_distance_ratio_float64']=endpoint
    # Echo the already recorded science quantities, without any extra forward.
    if TELEMETRY:
        for name in ('engine8','engine4'):
            TELEMETRY.target_probs(name,[{'request':d['request'],'p':d['fit']} for d in diagnostics[name]])
        values={'request':[],'prompt':[],'position':[],'p':[]}
        for d in diagnostics['overtone']:
            last=d['per_position_at_stop']
            for position,p in zip(last['positions'],last['probabilities']):
                values['request'].append(d['request']);values['prompt'].append(last['prompts'][position[0]])
                values['position'].append(position[1]);values['p'].append(p)
        TELEMETRY.target_probs('overtone',values)
    pristine.verify('after target construction')
    return {'engine8':engine8,'fe':fe,'overtone':overtone,'records':records,
            'audits':{'files':files,'sha256':json_sha(files)}}


def inject_sweep(harness,hp,values,table,layer):
    import torch
    from c10x_enginepath_inertness import require
    rows=[]
    for subject in harness.FICTION:
        tids=harness.tgt_ids(values[subject]);hits=[]
        for template in [harness.CANON]+harness.PTEST:
            started=work_unit(kind='injection');idx=harness.subject_idx(template,subject)
            vector=table[(subject,' '+values[subject])]
            if isinstance(vector,dict):vector=vector[layer]
            def overwrite(module,inputs,output):
                hidden=output[0] if isinstance(output,tuple) else output
                hidden[:,idx,:]=vector.cpu().to(dtype=hidden.dtype).to(hidden.device)
                return output
            handle=harness.model.model.layers[layer].register_forward_hook(overwrite)
            try:hits.append(bool(harness.full_seq_match(template.format(subject),tids)[0]))
            finally:handle.remove()
            end_unit(started)
        rows.append({'subj':subject,'val':values[subject],'per_template':hits})
    result={'canon_n':sum(r['per_template'][0] for r in rows),'para_n':sum(sum(r['per_template'][1:]) for r in rows),
            'per_template':{t:sum(r['per_template'][k] for r in rows) for k,t in enumerate([harness.CANON]+harness.PTEST)},'rows':rows}
    require(len(rows)==24,'INJECTION_ROWS')
    return result


def top1(harness,prompt):
    import torch
    with torch.no_grad():return int(forward_tokens(harness.model,harness.tok(prompt,return_tensors='pt').to(harness.DEV)).logits[0,-1].argmax())


def injection_screen(harness,hp,targets,pristine):
    pristine.verify('before injection')
    result={name:inject_sweep(harness,hp,harness.ARMS[ARM_NAMES[2]],targets[key],layer)
            for name,key,layer in [('reference','engine8',8),('I-2','fe',4),('I-1','overtone',8)]}
    pristine.verify('after injection')
    return result


def probe_setup(harness,ctx):
    frames=[c.format(harness.CANON) for group in ctx for c in group]
    from c10x_enginepath_inertness import require
    require(len(set(frames))==len(frames) and harness.CANON in frames,'FRAME_IDENTITY')
    firsts={harness.tgt_ids(harness.ARMS[ARM_NAMES[2]][s])[0] for s in harness.FICTION}
    def frame_counts():
        result={}
        for frame in frames:
            rows=[]
            for s in FRAME_SUBJECTS:
                token=top1(harness,frame.format(s));rows.append({'subj':s,'top1':int(token),'tok':harness.tok.decode([token]),'flip':bool(token in firsts)})
            result[frame]={'flips':sum(r['flip'] for r in rows),'n':6,'rows':rows}
        return result
    relation_templates=('{} is associated with','{} is a')
    before_frames=frame_counts()
    before_relation={t:[top1(harness,t.format(s)) for s in harness.FICTION] for t in relation_templates}
    def hook(arm,values):
        global ARM_UNIT
        if arm!=ARM_NAMES[2]:
            end_unit(ARM_UNIT);ARM_UNIT=None
            return {}
        relation={t:{'kind':'objective-anchored' if t=='{} is a' else 'bystander',
                     'flips':int(sum(a!=b for a,b in zip(before_relation[t],[top1(harness,t.format(s)) for s in harness.FICTION]))),
                     'pristine':[int(token) for token in before_relation[t]],'rows':list(harness.FICTION)} for t in relation_templates}
        curve={}
        import torch
        for s in harness.FICTION:
            ids=harness.tgt_ids(values[s])
            for t in harness.PTEST:
                batch=harness.tok(t.format(s),return_tensors='pt').to(harness.DEV)['input_ids'];cur=batch
                for pos,gold in enumerate(ids):
                    with torch.no_grad():pred=int(harness.model(cur).logits[0,-1].argmax())
                    item=curve.setdefault(str(pos),{'correct':0,'n':0});item['correct']+=int(pred==gold);item['n']+=1
                    cur=torch.cat([cur,torch.tensor([[gold]],device=harness.DEV)],dim=1)
        result={'frames':frame_counts(),'frames_pristine':before_frames,'relation_labels':relation,'teacher_forced_curve':curve}
        if TELEMETRY is not None:TELEMETRY.logit_lens(harness,harness._ARM_STATE['hp'],'after '+ACTIVE_RECIPE)
        end_unit(ARM_UNIT);ARM_UNIT=None
        return result
    return frames,hook


def covariance_identity(harness,hp):
    raw=harness.cov_cache_sha256(hp)
    result={}
    for layer in hp.layers:
        item=raw[str(layer)]
        if set(item)!={'path','sha256'} or sha_file(item['path'])!=item['sha256']:
            raise ValueError('covariance identity mismatch layer '+str(layer))
        result[str(layer)]=item['sha256']
    return result


def tokenizer_identity(harness):
    root=ROOT/'data/hf_cache/hub'/('models--'+harness.ID.replace('/','--'))/'snapshots'/harness.REV
    paths=[root/name for name in ('tokenizer.json','tokenizer_config.json','vocab.json','merges.txt','special_tokens_map.json') if (root/name).is_file()]
    if not paths:raise ValueError('tokenizer artifact hashes missing')
    return {str(p.name):sha_file(p) for p in paths}


def write_size_reports(recipes):
    import torch
    from c10x_enginepath_inertness import fp32_report,fp32_value
    result={};a7=ARM_NAMES[2]
    baseline64=sum(recipes['A']['write_norms_float64'][a7].values())
    baseline32=torch.tensor([fp32_value(recipes['A']['delta_norms'][a7][str(l)]['delta_norm']) for l in range(4,9)],dtype=torch.float32).sum()
    for name in ('I-2','I-1'):
        ratio64=sum(recipes[name]['write_norms_float64'][a7].values())/baseline64
        candidate32=torch.tensor([fp32_value(recipes[name]['delta_norms'][a7][str(l)]['delta_norm']) for l in range(4,9)],dtype=torch.float32).sum()
        ratio32=float(candidate32/baseline32)
        result[name]={'ratio_float64':ratio64,'ratio_fp32_report_only':fp32_report(ratio32),
                      'opposite_1_5_result':math.isfinite(ratio32) and ((ratio32>1.5)!=(ratio64>1.5))}
    return result


def source_commit():
    child=subprocess.run(['git','-C',str(ROOT),'rev-parse','HEAD'],capture_output=True,text=True,check=True)
    value=child.stdout.strip()
    if not value:raise ValueError('empty source commit')
    return value


def run(out,harness,go=None,process=1,process1=None,preflight=True,receipt=None):
    global H,PRISTINE,BUDGET,TELEMETRY
    from c10x_enginepath_inertness import Pristine,require,x2_primary_halt
    from c10x_enginepath_read import law3
    out=Path(out).resolve();selftest_root(ROOT)
    admitted=receipt if receipt is not None else launch_preflight(out,go,process,process1) if preflight else None
    configure(harness)
    hp=harness.MEMITHyperParams.from_json(str(ROOT/'code/configs/hparams/qwen25_3b_memit_hparams.json')) if hasattr(harness,'MEMITHyperParams') else harness.hp
    PRISTINE=Pristine(harness,hp);pristine=PRISTINE
    out.mkdir(parents=True,exist_ok=False)
    BUDGET=StageBudget(out,admitted['process1']['timings'] if admitted and admitted['process1'] else None,
                       start=admitted.get('started_monotonic') if admitted else None)
    state={'status':'RUNNING','completion':'incomplete','process':process,'run_id':out.name+'_'+str(os.getpid()),
           'pid':os.getpid(),'started_at':utc(),'recipes':{}}
    writer=None;probe=None;context_binding=None
    stage='setup';phase='setup:entry'
    def validate_boundary(operation):
        nonlocal phase
        phase=stage+':'+operation
        state['w0']={'hashes':pristine.hashes,'checkpoints':copy.deepcopy(pristine.checkpoints)}
        state['timings']={**BUDGET.timings,'work_units':copy.deepcopy(BUDGET.units)}
        validate_record_json(state)
    def enter_stage(name):
        nonlocal stage,phase
        if BUDGET.stage is not None:
            validate_boundary('exit');BUDGET.leave()
        stage=name;phase=name+':entry'
        BUDGET.enter(name)
        validate_boundary('entry')
        phase=name+':body'
    try:
        enter_stage('setup')
        ctx,context_source=recorded_contexts()
        binding=pinned_contexts(harness,ctx);binding.__enter__();context_binding=binding
        write_json(out/'context_templates.json',{'schema':'c10x_context_templates/v1','ctx':ctx,'ctx_sha256':json_sha(ctx),'source':context_source})
        state.update(ctx=ctx,ctx_sha256=json_sha(ctx),context_source=context_source)
        pristine.verify('before recipe A')
        base=scorer_record(harness.pre_base_report(),'record.base_report');state['base_report']=base
        validate_record_json(state)
        require(all(type(base[k]['base']) is int and base[k]['base']<=3 for k in ARM_NAMES),'STIMULUS_LEAK')
        require(harness.get_context_templates(harness.model,harness.tok)==ctx,'CONTEXT_PIN_DRIFT')
        frames,probe=probe_setup(harness,ctx);harness.ARM_HOOKS.append(probe)
        state.update(frames=frames,frames_sha256=json_sha(frames))
        if admitted and admitted['telemetry']:
            writer=Telemetry(out,process,state['run_id']);BUDGET.telemetry=writer
            writer.phase('stage_start',stage='setup');writer.logit_lens(harness,hp,'pristine')
        enter_stage('A')
        baseline=recipe(harness,'A',str(ROOT/'code/configs/hparams/qwen25_3b_memit_hparams.json'),None,None,pristine,writer)
        state['recipes']['A']=baseline
        validate_boundary('recipe_record')
        if not law3(baseline):raise ValueError('LAW3_BASELINE_MISS')
        require(baseline['law5_gate']['ok'] is True,'G_NOT_INERT')
        TELEMETRY=writer
        enter_stage('targets');targets=construct_targets(out,harness,hp,ctx,pristine)
        state.update(targets=targets['records'],audits=targets['audits'])
        enter_stage('inertness')
        import c10x_enginepath_inertness as I
        checks=I.run_checks(harness,hp,ctx,targets,pristine,out)
        state['inertness']=checks
        enter_stage('injection');pristine.verify('before injection')
        injected=injection_screen(harness,hp,targets,pristine)
        state['inject']={**{n:r['para_n'] for n,r in injected.items()},'details':injected}
        for name in ('I-2','I-1'):
            enter_stage(name)
            state['recipes'][name]=recipe(harness,name,str(ROOT/'code/configs/hparams/qwen25_3b_memit_hparams.json'),targets['fe'],targets['overtone'],pristine,writer)
            validate_boundary('recipe_record')
            require(state['recipes'][name]['law5_gate']['ok'] is True,'G_NOT_INERT')
        enter_stage('final');pristine.verify('after final recipe')
        end_sources=source_hashes();require(end_sources==admitted['sources'],'SOURCE_DRIFT')
        identity={'model':harness.ID,'model_rev':harness.REV,'tokenizer':tokenizer_identity(harness),
                  'software':environment_identity(),'device':str(harness.DEV),'dtype':str(next(harness.model.parameters()).dtype),
                  'hparams':sha_file(ROOT/'code/configs/hparams/qwen25_3b_memit_hparams.json'),
                  'covariance':covariance_identity(harness,hp),
                  'stimuli':{arm:[{'subj':s,'val':harness.ARMS[arm][s]} for s in harness.FICTION] for arm in ARM_NAMES},
                  'templates':{'CANON':harness.CANON,'PTEST':harness.PTEST},
                  'settings':{'lam':.1,'eps':.01,'n_sigma':.5},'weights':pristine.hashes}
        state.update(schema='c10x_enginepath/v1',status='COMPLETE',completion='complete',finished_at=utc(),
            source_commit=source_commit(),prereg_sha256=PIN,sources_start=admitted['sources'],sources_end=end_sources,
            fingerprint=admitted['fingerprint'],identity=identity,ctx=ctx,ctx_sha256=json_sha(ctx),frames=frames,frames_sha256=json_sha(frames),
            base_report=base,w0={'hashes':pristine.hashes,'checkpoints':copy.deepcopy(pristine.checkpoints)},inertness=checks,
            counters={name:state['recipes'][name]['counters'] for name in ('A','I-2','I-1')},targets=targets['records'],
            inject={**{n:r['para_n'] for n,r in injected.items()},'details':injected},
            telemetry=admitted['telemetry'],telemetry_inertness=admitted['telemetry_inertness'],audits=targets['audits'])
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        state['memory']={'peak_process_rss_bytes':int(rss if sys.platform=='darwin' else rss*1024),
                         'scope':'measured process RSS peak; complete unified-memory/device peak UNVERIFIED'}
        if admitted.get('replacement'):state['replacement']=admitted['replacement']
        state['target_hashes']={name:rec['sha256'] for name,rec in targets['records'].items()}
        state['write_size_diagnostics']=write_size_reports(state['recipes'])
        state['reviewer']={'model':'UNVERIFIABLE','effort':'UNVERIFIABLE'}
        state['provenance']={'go':admitted['go_identity']}
        if process1:state['provenance']['process1']=str(Path(process1).resolve())
        if admitted.get('replacement'):state['provenance']['replacement']=admitted['replacement']
        pristine.restore();pristine.verify('closeout restore')
        state['w0']['checkpoints']=copy.deepcopy(pristine.checkpoints)
        validate_boundary('serialization')
        from c10x_enginepath_read import _validate
        _validate(state | {'timings':{}})
        from c10x_enginepath_read import MANIFEST
        manifest={k:state[k] for k in MANIFEST}
        for file,key in [('targets','targets'),('inertness','inertness'),('inject','inject'),('pass1','recipes')]:
            BUDGET.unit()
            write_json(out/(file+'.json'),{'manifest':manifest,key:state[key]})
        validate_boundary('exit');BUDGET.leave();state['timings']={**BUDGET.timings,'work_units':BUDGET.units}
        validate_record_json(state)
        write_json(out/'run.json',state)
        require(source_hashes()==end_sources,'SOURCE_DRIFT after serialization')
        return state
    except Exception as exc:
        trace=traceback.format_exc()
        current=exc;seen=set();budget_inputs=None
        while current is not None and id(current) not in seen:
            seen.add(id(current))
            if hasattr(current,'budget_inputs'):
                budget_inputs=current.budget_inputs;break
            current=current.__cause__ or current.__context__
        exc=x2_primary_halt(exc)
        if hasattr(exc,'x2_vii_diagnostic'):state['x2_vii_diagnostic']=exc.x2_vii_diagnostic
        if budget_inputs is not None:state['budget_inputs']=copy.deepcopy(budget_inputs)
        state['timings']={**BUDGET.timings,'work_units':copy.deepcopy(BUDGET.units)}
        state.update(status='HALTED',completion='incomplete',finished_at=utc(),code=str(exc),
                     stage=stage,phase=phase,traceback=trace,traceback_source='python_exception')
        if writer:writer.phase('halt',code=str(exc))
        state['diagnostic']=halt_diagnostic(state,exc)
        state=diagnostic_json(state)
        if not (out/'run.json').exists():write_json(out/'run.json',state)
        return state
    finally:
        if probe is not None:harness.ARM_HOOKS.remove(probe)
        if writer:writer.close()
        pristine.restore()
        if state['status']!='COMPLETE':pristine.verify('closeout restore')
        BUDGET=None;TELEMETRY=None
        release(harness)
        if context_binding is not None:context_binding.__exit__(None,None,None)


def load_harness():
    # All model/tokenizer imports remain behind the machine gate and supervisor.
    os.environ['C10_ARMS']=','.join(ARM_NAMES)
    import c10e_bandknob as harness
    from memit.compute_z import find_fact_lookup_idx
    from rome.repr_tools import get_words_idxs_in_templates
    harness.find_fact_lookup_idx=find_fact_lookup_idx
    harness.subject_idx=lambda template,subject:get_words_idxs_in_templates(harness.tok,[template],[subject],'last')[0][0]
    return harness


def bounded_answer_audit(out,stage_deadline,process_deadline):
    from c10x_enginepath_inertness import Halt,require
    from c10x_enginepath_read import strict_json
    deadline=min(stage_deadline,process_deadline)
    remaining=deadline-WATCHDOG_CLOCK()
    require(remaining>0.,'ANSWER_AUDIT_DEADLINE')
    out=Path(out)
    argv=[sys.executable,'-B',str(ROOT/'code/lab/track_c/c10x_enginepath_telemetry_check.py'),'audit','--out',str(out)]
    with (out.with_name(out.name+'_logs')/'answer_audit.log').open('x') as stream:
        child=subprocess.Popen(argv,cwd=ROOT,env=os.environ.copy(),stdout=stream,stderr=stream,start_new_session=True)
        try:
            remaining=deadline-WATCHDOG_CLOCK()
            require(remaining>0.,'ANSWER_AUDIT_DEADLINE')
            code=child.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid,signal.SIGKILL);child.wait()
            raise Halt('ANSWER_AUDIT_WATCHDOG_TIMEOUT')
        except BaseException:
            if child.poll() is None:os.killpg(child.pid,signal.SIGKILL)
            child.wait();raise
    require(WATCHDOG_CLOCK()<=deadline,'ANSWER_AUDIT_DEADLINE')
    require(type(code) is int and code in (0,1),'ANSWER_AUDIT_CHILD_FAILED')
    record=strict_json((out/'telemetry/audit.json').read_bytes())
    from c10x_enginepath_telemetry_check import CAUSES
    fields={'schema','process','run_id','verdict','causes','rerun_required','expected_answers','observed_answers','missing_keys'}
    require(type(record) is dict and set(record)==fields,'ANSWER_AUDIT_RECORD')
    causes=record['causes']
    require(type(causes) is list and all(type(c) is str and c in CAUSES for c in causes) and
            causes==[c for c in CAUSES if c in causes],'ANSWER_AUDIT_CAUSES')
    rerun=bool(set(causes)-{'DISABLED'})
    require(record['verdict']==('FAIL' if causes else 'PASS') and code==int(bool(causes)) and
            type(record['rerun_required']) is bool and record['rerun_required']==rerun,'ANSWER_AUDIT_DISPOSITION')
    run_record=strict_json((out/'run.json').read_bytes())
    require(record['schema']=='c10x_enginepath_telemetry_audit/v1' and
            type(record['process']) is int and record['process'] in (1,2) and
            (record['process'],record['run_id'])==(run_record['process'],run_record['run_id']) and
            type(record['run_id']) is str and bool(record['run_id']),'ANSWER_AUDIT_IDENTITY')
    require(all(type(record[k]) is int and record[k]>=0 for k in ('expected_answers','observed_answers')) and
            type(record['missing_keys']) is list and all(type(k) is list and len(k)==4 and
            all(type(v) is str and bool(v) for v in k) for k in record['missing_keys']),'ANSWER_AUDIT_COUNTS')
    require(causes or (not record['missing_keys'] and record['expected_answers']==record['observed_answers']),'ANSWER_AUDIT_COUNTS')
    require(WATCHDOG_CLOCK()<=deadline,'ANSWER_AUDIT_DEADLINE')
    return record


def watchdog(out,go,process,process1=None,predecessor=None,cause=None):
    from c10x_enginepath_read import strict_json
    start=WATCHDOG_CLOCK()
    out=Path(out)
    selftest_root(ROOT)
    preflight_argv=[sys.executable,'-B',str(Path(__file__).resolve()),'--preflight','--out',str(out),
                   '--go',str(go),'--process',str(process)]
    if process1:preflight_argv+=['--process1',str(process1)]
    preflight_child=subprocess.Popen(preflight_argv,cwd=ROOT,env=os.environ.copy(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    try:
        stdout,stderr=preflight_child.communicate(timeout=max(.001,CAPS['setup']-(WATCHDOG_CLOCK()-start)))
    except subprocess.TimeoutExpired:
        os.killpg(preflight_child.pid,signal.SIGKILL);preflight_child.communicate()
        halt_diagnostic({'stage':'setup','phase':'setup:preflight_timeout','completion':'incomplete',
                         'traceback':traceback.format_exc(),'traceback_source':'python_exception'},'PREFLIGHT_WATCHDOG_TIMEOUT')
        return 1
    if preflight_child.returncode!=0:
        print(stderr.decode('utf8'),file=sys.stderr,end='')
        return 1
    if not stdout:raise ValueError('empty preflight receipt')
    admitted=strict_json(stdout)
    admitted['started_monotonic']=start
    rerun='_rerun' in out.name
    if rerun and (not predecessor or not Path(predecessor).is_absolute() or not cause):
        raise ValueError('rerun requires absolute predecessor and cause')
    if rerun:
        previous=Path(predecessor).resolve(strict=True)
        if previous.parent!=(ROOT/'results').resolve() or not re.fullmatch(r'c10x_enginepath(?:_r2)?(?:_rerun[1-9][0-9]*)?',previous.name):
            raise ValueError('invalid predecessor directory')
        admitted['replacement']={'predecessor':str(previous),'cause':cause,'at':utc()}
    logs=out.with_name(out.name+'_logs');logs.mkdir()
    receipt={'out':str(out),'go':str(Path(go).resolve()),'process':process,'process1':process1,
             'parent_pid':os.getpid(),'admitted':admitted,'predecessor':predecessor,'cause':cause}
    receipt_path=logs/'preflight.json';write_json(receipt_path,receipt)
    argv=[sys.executable,'-B',str(Path(__file__).resolve()),'--worker','--out',str(out),'--go',str(Path(go).resolve()),
          '--process',str(process),'--receipt',str(receipt_path)]
    reason=None
    with (logs/'process.log').open('x',buffering=1) as stream:
        child=subprocess.Popen(argv,cwd=ROOT,env=os.environ.copy(),stdout=stream,stderr=stream,start_new_session=True)
        try:
            while child.poll() is None:
                now=WATCHDOG_CLOCK();elapsed=now-start;stage_path=out/'stage.json'
                stage='setup';began=start
                if stage_path.exists():
                    progress=strict_json(stage_path.read_bytes());stage=progress['stage'];began=start if stage=='setup' else progress['started_monotonic']
                    if stage not in CAPS or type(began) not in (int,float) or began<start:raise ValueError('invalid stage checkpoint')
                if elapsed>=PROCESS_BUDGET or now-began>=CAPS[stage]:
                    reason='WATCHDOG_TIMEOUT '+stage;os.killpg(child.pid,signal.SIGKILL);break
                time.sleep(.1)
        except BaseException:
            if child.poll() is None:os.killpg(child.pid,signal.SIGKILL)
            child.wait();raise
        code=child.wait()
    ended=WATCHDOG_CLOCK()
    stage='setup';began=start
    if ended-start>PROCESS_BUDGET:reason='WATCHDOG_TIMEOUT process'
    if (out/'stage.json').exists():
        last=strict_json((out/'stage.json').read_bytes());stage=last['stage'];began=start if stage=='setup' else last['started_monotonic']
        if ended-began>CAPS[last['stage']]:reason='WATCHDOG_TIMEOUT '+last['stage']
    complete=code==0 and (out/'run.json').exists() and strict_json((out/'run.json').read_bytes()).get('status')=='COMPLETE'
    record={'status':'COMPLETE' if complete and not reason else 'HALTED','completion':'complete' if complete and not reason else 'incomplete',
            'exit_code':code,'elapsed_seconds':WATCHDOG_CLOCK()-start,'reason':reason or ('worker exit '+str(code) if not complete else 'complete')}
    record.update(out=str(out.resolve()),process=process)
    if complete:record['run_id']=strict_json((out/'run.json').read_bytes())['run_id']
    if record['status']=='HALTED':
        record.update(stage=stage,phase=stage+':supervisor_exit',traceback=None,
                      traceback_source='unavailable_worker_exception')
        if reason:
            record.update(phase=stage+':supervisor_timeout',traceback_source='unavailable_worker_timeout')
        if (out/'run.json').exists():
            worker_state=strict_json((out/'run.json').read_bytes())
            if worker_state.get('status')=='HALTED':
                if 'budget_inputs' in worker_state:
                    record['budget_inputs']=worker_state['budget_inputs']
                    record['worker_halt']={k:worker_state.get(k) for k in ('code','stage','phase')}
                if not reason:
                    record.update(stage=worker_state.get('stage',stage),phase=worker_state.get('phase',record['phase']),
                                  traceback=worker_state.get('traceback'),traceback_source=worker_state.get('traceback_source',record['traceback_source']))
        record['diagnostic']=halt_diagnostic(record,record['reason'])
        write_json(logs/'supervisor.json',record)
        return 1
    # T11 happens before the science reader. Disabled-only audit failure leaves
    # the science readable; every compromised-answer outcome demands a rerun.
    if admitted['telemetry']:
        try:
            audited=bounded_answer_audit(out,began+CAPS[stage],start+PROCESS_BUDGET)
        except Exception as exc:
            record.update(status='HALTED',completion='incomplete',reason=str(exc),elapsed_seconds=WATCHDOG_CLOCK()-start,
                          stage=stage,phase=stage+':answer_audit',traceback=traceback.format_exc(),traceback_source='python_exception')
            record['diagnostic']=halt_diagnostic(record,record['reason'])
            write_json(logs/'supervisor.json',record)
            return 1
        if audited.get('rerun_required') is True:
            record.update(status='HALTED',completion='incomplete',reason='COMPROMISED_ANSWER_AUDIT',
                          stage=stage,phase=stage+':answer_audit',traceback=None,traceback_source='unavailable_no_python_exception')
            record['diagnostic']=halt_diagnostic(record,record['reason'])
            write_json(logs/'supervisor.json',record)
            return 1
    ended=WATCHDOG_CLOCK();record['elapsed_seconds']=ended-start
    if ended-start>PROCESS_BUDGET or ended-began>CAPS[stage]:
        record.update(status='HALTED',completion='incomplete',reason='FINAL_SUPERVISOR_DEADLINE',
                      stage=stage,phase=stage+':supervisor_deadline',traceback=None,traceback_source='unavailable_no_python_exception')
        record['diagnostic']=halt_diagnostic(record,record['reason'])
        write_json(logs/'supervisor.json',record)
        return 1
    write_json(logs/'supervisor.json',record)
    ended=WATCHDOG_CLOCK()
    if ended-start>PROCESS_BUDGET or ended-began>CAPS[stage]:
        record.update(status='HALTED',completion='incomplete',reason='FINAL_SUPERVISOR_PERSISTENCE_DEADLINE',elapsed_seconds=ended-start,
                      stage=stage,phase=stage+':supervisor_persistence',traceback=None,traceback_source='unavailable_no_python_exception')
        write_json(logs/'supervisor_halt.json',record)
        halt_diagnostic(record,record['reason'])
        return 1
    return 0


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True);parser.add_argument('--go',required=True)
    parser.add_argument('--process',type=int,choices=(1,2),default=1);parser.add_argument('--process1')
    parser.add_argument('--predecessor');parser.add_argument('--cause')
    parser.add_argument('--worker',action='store_true');parser.add_argument('--receipt')
    parser.add_argument('--preflight',action='store_true',help=argparse.SUPPRESS)
    args=parser.parse_args(argv)
    if args.preflight:
        print(json.dumps(launch_preflight(args.out,args.go,args.process,args.process1),allow_nan=False,sort_keys=True))
        return 0
    if not args.worker:
        return watchdog(args.out,args.go,args.process,args.process1,args.predecessor,args.cause)
    from c10x_enginepath_read import strict_json
    environment_preflight();path=Path(args.receipt or '')
    if not path.is_absolute() or path!=Path(args.out).with_name(Path(args.out).name+'_logs')/'preflight.json':
        raise ValueError('worker needs its supervisor receipt')
    receipt=strict_json(path.read_bytes())
    if receipt['parent_pid']!=os.getppid() or receipt['out']!=args.out or receipt['go']!=args.go or receipt['process']!=args.process:
        raise ValueError('worker receipt identity mismatch')
    if source_hashes()!=receipt['admitted']['sources']:raise ValueError('SOURCE_DRIFT before model load')
    selftest_root(ROOT)
    engine=ROOT/'code/memit/vendor';sys.path.insert(0,str(engine))
    # Python import order: c10e owns initialization; c10p is never imported (Q4).
    harness=load_harness()
    import torch
    if str(harness.DEV)!='mps' or next(harness.model.parameters()).dtype!=torch.float16:
        halt_diagnostic({'stage':'setup','device':str(harness.DEV)},'LIVE_DEVICE_DTYPE_MISMATCH')
        return 1
    result=run(args.out,harness,args.go,args.process,receipt['process1'],receipt=receipt['admitted'])
    return 0 if result['status']=='COMPLETE' else 1


if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        print('C10X REFUSED/HALTED: '+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
