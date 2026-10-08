"""Frozen C10Y/Amendments T,C driver. Import is model-free; execution is gated.

MEASUREMENT-ONLY. CPU selftests never dispatch this module as a worker.
"""
import os, sys
from pathlib import Path
import argparse
import ast
import contextlib
import copy
import datetime
import hashlib
import importlib
import importlib.metadata
import io
import json
import math
import platform
import re
import signal
import subprocess
import time

ROOT = Path(os.environ.get('LLMDB_ROOT', Path(__file__).resolve().parents[2]))
PREREG_SHA = 'e069b358c362b2a05e3b668e8a29f33061e15a24306e321452e6fa46a4e83331'
PINNED_ENGINE_SHA = 'c7dabbe7c25a7e58653621d9cc66e37b35c865ae09b73b6a96073a184c6c98da'
PINNED_FLAT_SHA = 'd6c7c70026dced37bddc6adf316a3487d70227dae80a6e0ed5cdabe50caedfa0'
MODEL_ID = 'Qwen/Qwen2.5-3B'
MODEL_REV = '3aab1f1954e9cc14eb9509a215f9e5ca08227a9b'
ENGINE_SHA = 'd941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65'
SOURCE_PATHS = {
    'driver':'experiments/track_c/c10y_directdw_arms.py',
    'reader':'experiments/track_c/c10y_directdw_read.py',
    'check':'experiments/track_c/c10y_directdw_telemetry_check.py',
    'harness':'experiments/track_c/c10e_bandknob.py',
    'templates':'experiments/track_c/c10z_astra_benchmark.py',
    'hparams':'configs/hparams/qwen25_3b_memit_hparams.json',
    'compute_z':'memit_dry_run/memit/memit/compute_z.py',
    'compute_ks':'memit_dry_run/memit/memit/compute_ks.py',
    'repr_tools':'memit_dry_run/memit/rome/repr_tools.py',
    'memit_main':'memit_dry_run/memit/memit/memit_main.py',
    'prereg':'docs/C10Y_DIRECTDW_PREREG.md'}
ARMS = ('A1_single','A2_coherent2','A7_coined_coined')
A7 = ARMS[2]
FORECAST_PHASES = ('preflight','load','contexts_targets','baseline','proofs',
                   'projector_capture','optimisation','merge','readout','shutdown')
STAGE_CLOCK = time.monotonic
TELEMETRY_CLOCK = time.perf_counter


class Halt(ValueError):
    def __init__(self, code, detail=None):
        self.code, self.detail = code, detail
        super().__init__(code + (': '+str(detail) if detail is not None else ''))


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1<<22),b''): h.update(chunk)
    return h.hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value,allow_nan=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def strict_json(raw):
    def reject(value): raise ValueError('Nonfinite JSON: '+value)
    def floating(value):
        result=float(value)
        if not math.isfinite(result): raise ValueError('Nonfinite JSON: '+value)
        return result
    def pairs(items):
        result={}
        for k,v in items:
            if k in result: raise ValueError('Duplicate JSON key: '+k)
            result[k]=v
        return result
    return json.loads(raw,parse_constant=reject,parse_float=floating,object_pairs_hook=pairs)


def strict_load(path): return strict_json(Path(path).read_bytes())


def write_json(path,value):
    path=Path(path)
    if not path.is_absolute(): raise Halt('OUTPUT-PATH',str(path))
    payload=json.dumps(value,allow_nan=False,sort_keys=True,indent=2)+'\n'
    path.parent.mkdir(parents=True,exist_ok=True)
    try:
        with path.open('x') as f:
            f.write(payload);f.flush();os.fsync(f.fileno())
    except FileExistsError as e: raise Halt('EXISTING-ARTIFACT',str(path)) from e


def selftest_root(root):
    root=Path(root).resolve()
    scratch=Path('/private/tmp/c10y_build').resolve()
    if os.environ.get('C10Y_SELFTEST') and scratch not in root.parents:
        raise Halt('SELFTEST-ROOT',str(root))
    return root


def source_hashes():
    return {p:sha(Path(ROOT)/p) for p in SOURCE_PATHS.values()}


def environment_identity():
    return {'python':platform.python_version(),'machine':platform.machine(),
            'platform':platform.platform(),'torch':importlib.metadata.version('torch'),
            'transformers':importlib.metadata.version('transformers'),'model_rev':MODEL_REV}


def fingerprint_record():
    path=Path(ROOT)/'tools/engine_fingerprint.py'
    spec=importlib.util.spec_from_file_location('_c10y_fingerprint',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.MEMIT_MAIN=Path(ROOT)/SOURCE_PATHS['memit_main']
    stream=io.StringIO()
    with contextlib.redirect_stdout(stream): code=module.main()
    return {'exit_code':code,'output':stream.getvalue()}


def preflight(env=None,fingerprint=None):
    env=os.environ if env is None else env
    knobs=('C10_PROJECTOR','N_EDIT','C10_SUBJECT_OFFSET','C10_CTX_TEMPLATES','C10_ARMS','C10_KEY_LOCUS',
           'HP_CANDIDATE','C10_RECIPES','CANDIDATE_NAME','OUT','DECISION_ID','PREREG','RUN_LABEL','LLMDB_DEVICE')
    for key in knobs:
        if key in env: raise Halt('INHERITED-KNOB',key)
    for key,value in (('MODEL_ID',MODEL_ID),('MODEL_REV',MODEL_REV)):
        if key in env and env[key]!=value: raise Halt('MODEL-IDENTITY',key)
    if 'C10Y_TELEMETRY' in env and env['C10Y_TELEMETRY']!='1': raise Halt('TELEMETRY-SWITCH')
    selftest_root(ROOT)
    sources=source_hashes()
    if sources[SOURCE_PATHS['prereg']]!=PREREG_SHA: raise Halt('PREREG SHA MISMATCH')
    record=(fingerprint or fingerprint_record)()
    if record['exit_code']!=0 or not record['output'] or 'engine fingerprint PASS' not in record['output']:
        raise Halt('FINGERPRINT',record)
    src=(Path(ROOT)/SOURCE_PATHS['memit_main']).read_bytes()
    if hashlib.sha256(src).hexdigest()!=ENGINE_SHA or src.count(b'_cov_cpu')!=3: raise Halt('FINGERPRINT')
    return {'sources':sources,'fingerprint':{'sha256':ENGINE_SHA,'cov_cpu_sites':3,'output':record['output']},'env':environment_identity()}


# Brief R3: move before cast; optimisation itself remains float32/fp16.
def assert_no_mps_double(tensor):
    import torch
    if tensor.device.type=='mps' and tensor.dtype==torch.float64: raise Halt('FLOAT64-ON-MPS')


def cpu64(tensor):
    assert_no_mps_double(tensor)
    return tensor.detach().cpu().double()


def to_like(tensor,reference):
    # MPS-to-CPU copies must preserve dtype; cast only after the device move.
    return tensor.to(device=reference.device).to(dtype=reference.dtype)


def norm(tensor): return float(cpu64(tensor).norm())


def cosine(x,y):
    a,b=cpu64(x).reshape(-1),cpu64(y).reshape(-1)
    if a.equal(b): return 1.0
    na,nb=float(a.norm()),float(b.norm())
    if not na or not nb: return 0.0
    return max(-1.,min(1.,float(a@b)/(na*nb)))


def relative_distance(x,y):
    a,b=cpu64(x),cpu64(y);d=max(float(a.norm()),float(b.norm()))
    return float((a-b).norm())/d if d else 0.0


def norm_ratio(x,y):
    nx,ny=norm(x),norm(y)
    if not ny:
        if not nx: return 1.
        raise Halt('INVALID-SIZE-NORMALISATION')
    return nx/ny


def gram_norm(a,b):
    a,b=cpu64(a),cpu64(b)
    return math.sqrt(max(0.,float(((a.T@a)*(b@b.T).T).sum())))


def null_share(update,P):
    d,p=cpu64(update),cpu64(P);den=float(d.square().sum())
    return float((d@p).square().sum())/den if den else None


def projector_gate(planned,actual,P):
    return all(norm(d)==0 or null_share(d,P[i])>=0.999
               for i,l in enumerate(planned) for d in (planned[l],actual[l]))


def factor_solve(K,R,P,cache,l2):
    import torch
    k,r,p=K.float().cpu(),R.float().cpu(),P.float().cpu()
    matrix=p@(k@k.T+cache)+l2*torch.eye(k.shape[0])
    X=torch.linalg.solve(matrix,p@k)
    return {'R':r,'A0':r.clone(),'X':X,'B':X.T}


def tensor_sha(tensor):
    t=tensor.detach().cpu().contiguous()
    return hashlib.sha256(t.view(__import__('torch').uint8).numpy().tobytes()).hexdigest()


def band_hashes(H,hp): return {str(l):tensor_sha(t) for l,t in H.snap_layers(hp).items()}


def restore(H,hp,snap):
    H.restore_layers(hp,snap)
    if any(tensor_sha(x)!=tensor_sha(snap[l]) for l,x in H.snap_layers(hp).items()): raise Halt('RESTORATION')


def capture_solve(H,hp,requests,P,cache):
    """Sequential recomputation of c10e:194–217; record factors beside the original solve."""
    import torch
    ctx=H.get_context_templates(H.model,H.tok);layers=hp.layers;z_layer=layers[-1]
    keys=[(rq['subject'],rq['target_new']['str']) for rq in requests]
    if H.Z_OVERRIDE is None or H._LAW5_DEFAULT_CTX or not all(k in H.Z_OVERRIDE for k in keys): raise Halt('OVERRIDE-LEDGER')
    H.Z_OVERRIDE_HITS+=1
    zs=torch.stack([H.Z_OVERRIDE[k].to(H.DEV) for k in keys],dim=1)
    npd=dict(H.model.named_parameters());out={}
    for i,layer in enumerate(layers):
        K=H.compute_ks(H.model,H.tok,requests,hp,layer,ctx).T
        cur=H.get_module_input_output_at_words(H.model,H.tok,z_layer,
              context_templates=[rq['prompt'] for rq in requests],words=[rq['subject'] for rq in requests],
              module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1].T
        tgt=zs-cur;tgt=tgt.repeat_interleave(K.size(1)//tgt.size(1),dim=1)
        resid=tgt/(len(layers)-i);Kf=K.float();rf=resid.float();Pi=P[i];ca=cache[i]
        matrix=Pi@(Kf.cpu()@Kf.cpu().T+ca)+getattr(H,'L2',1.)*torch.eye(Kf.shape[0])
        rhs=Pi@Kf.cpu()@rf.cpu().T
        upd=torch.linalg.solve(matrix,rhs).T
        upd=H.upd_matrix_match_shape(upd.float(),npd[H.weight_name(hp,layer)].shape)
        captured=factor_solve(K,rf,Pi,ca,getattr(H,'L2',1.))
        captured['reference_update']=upd;out[layer]=captured
        with torch.no_grad(): npd[H.weight_name(hp,layer)][...] += to_like(upd,npd[H.weight_name(hp,layer)])
    for i,layer in enumerate(layers):
        K=H.compute_ks(H.model,H.tok,requests,hp,layer,ctx).T.float().cpu();cache[i]=cache[i]+K@K.T
    return out


def stored_weight(W0,update,scale):
    update=update.to(W0.device)
    return (W0.detach().half()+(update.float()*scale).half()).half()


def effective_weight(W0,a,b): return (W0.detach().half()+(a.float()@b.float()).half()).half()


def deployed_hook(W0,a,b,mask):
    import torch
    def hook(module,inputs,output):
        x=inputs[0];weight=effective_weight(W0,a,b)
        result=torch.nn.functional.linear(x.to(weight.dtype),weight)
        if mask is not None:
            detached=torch.nn.functional.linear(x.to(weight.dtype),effective_weight(W0,a.detach(),b))
            result=torch.where(mask.to(x.device).unsqueeze(-1),result,detached)
        return result.to(x.dtype)
    return hook


def hook_snapshot(model):
    return {n:(tuple(m._forward_hooks.items()),tuple(m._forward_pre_hooks.items())) for n,m in model.named_modules()}


@contextlib.contextmanager
def weight_hooks(H,hp,As,Bs,W0,mask):
    snapshot=hook_snapshot(H.model);handles=[];modules=dict(H.model.named_modules())
    try:
        for l,a in As.items(): handles.append(modules[hp.rewrite_module_tmp.format(l)].register_forward_hook(deployed_hook(W0[l],a,Bs[l],mask)))
        yield
    finally:
        for handle in handles: handle.remove()
        if hook_snapshot(H.model)!=snapshot: raise Halt('HOOK-RESTORATION')


def request_batch(H,request,contexts):
    """Engine compute_z:41–73, H-qualified; no batch padding differences in parity."""
    import torch
    tok,dev,hparams=H.tok,H.DEV,H.hp
    target_ids=tok(request['target_new']['str'],return_tensors='pt').to(dev)['input_ids'][0]
    rewriting_prompts,kl_prompts=[context.format(request['prompt'])+tok.decode(target_ids[:-1])
        for context_types in contexts for context in context_types],['{} is a']
    all_prompts=rewriting_prompts+kl_prompts
    input_tok=tok([prompt.format(request['subject']) for prompt in all_prompts],return_tensors='pt',padding=True).to(dev)
    rewriting_targets=torch.tensor(-100,device=dev).repeat(len(rewriting_prompts),*input_tok['input_ids'].shape[1:])
    for i in range(len(rewriting_prompts)):
        ex_len=input_tok['attention_mask'][i].sum()
        rewriting_targets[i,ex_len-len(target_ids):ex_len]=target_ids
    lookup_idxs=[H.find_fact_lookup_idx(prompt,request['subject'],tok,hparams.fact_token,verbose=(i==0))
                 for i,prompt in enumerate(all_prompts)]
    return {'input_tok':input_tok,'rewriting_targets':rewriting_targets,'lookup_idxs':lookup_idxs,
            'target_ids':target_ids,'rewriting_prompts':rewriting_prompts,'all_prompts':all_prompts}


def packed_batches(H,batches):
    import torch
    width=max(b['input_tok']['input_ids'].shape[1] for b in batches)
    def pad(t,value): return torch.nn.functional.pad(t,(0,width-t.shape[1]),value=value)
    tokens={k:torch.cat([pad(b['input_tok'][k],H.tok.pad_token_id if k=='input_ids' else 0) for b in batches]) for k in ('input_ids','attention_mask')}
    offset=0;targets=[];lookups=[];routes=[];kl=[]
    for b in batches:
        J=len(b['rewriting_prompts'])
        for j in range(J):
            row=offset+j;positions=(b['rewriting_targets'][j]!=-100).nonzero().flatten()
            targets.append((row,positions,b['target_ids'],len(targets)//J,j))
            routes.append((row,b['lookup_idxs'][j]))
        kl.append((offset+J,b['lookup_idxs'][-1]));offset+=J+1
    mask=torch.ones(tokens['input_ids'].shape,dtype=torch.bool,device=H.DEV)
    for row,idx in routes: mask[row,:idx]=False
    return tokens,targets,kl,mask


def edit_components(H,batches,pristine,operators=None):
    import torch
    tokens,targets,kl,mask=packed_batches(H,batches)
    # Backbone returns the final normalised hidden state, so the head is applied once.
    def hidden(): return H.model.model(input_ids=tokens['input_ids'],attention_mask=tokens['attention_mask'],use_cache=False).last_hidden_state
    if operators is None: state=hidden()
    else:
        As,Bs,W0=operators
        with weight_hooks(H,H.hp,As,Bs,W0,mask): state=hidden()
    positions=torch.cat([state[row,pos] for row,pos,_,_,_ in targets])
    lp=torch.log_softmax(H.model.lm_head(positions).float(),-1)
    selected=[];nll=[];cursor=0;probabilities=[];by_request={}
    for row,pos,ids,request,frame in targets:
        length=len(ids);values=lp[cursor:cursor+length].gather(1,ids[:,None]).flatten();cursor+=length
        by_request.setdefault(request,[]).append(-values.mean());selected.extend(values.detach().cpu().tolist())
        probabilities.extend({'request':request,'frame':frame,'position':i,'p':float(cpu64(v).exp())} for i,v in enumerate(values))
    edit=torch.stack([torch.stack(x).mean() for x in by_request.values()]).mean()
    # KL gradients use an unmasked path, independently of L_edit's routing.
    if operators is not None:
        with weight_hooks(H,H.hp,As,Bs,W0,None): kstate=hidden()
    else: kstate=state
    q=torch.log_softmax(H.model.lm_head(torch.stack([kstate[row,idx] for row,idx in kl])).float(),-1)
    base=q.detach() if pristine is None else pristine
    raw=torch.nn.functional.kl_div(base,q,log_target=True,reduction='batchmean')
    return {'L_edit':edit,'KL_raw':raw,'KL_weighted':raw*0.0625,'L':total_loss(edit,raw),
            'kl_log_probs':q,'target_log_probs':selected,'probabilities':probabilities,
            'per_request_nll':[float(torch.stack(x).mean().detach().cpu()) for x in by_request.values()],
            'padded_length':tokens['input_ids'].shape[1]}


def total_loss(edit,kl): return edit+0.0625*kl


def anchor_loss(current,target,delta):
    import torch
    residual=current-target
    den=cpu64(delta).square().sum(-1);squares=cpu64(residual).square().sum(-1)
    if any(float(den[i])==0 and bool((squares[i]!=0).any()) for i in range(len(den))): raise Halt('INVALID-ANCHOR-NORMALISATION')
    terms=[]
    for i in range(len(den)):
        if float(den[i])==0: terms.append(residual[i].sum()*0)
        else: terms.append(residual[i].float().square().sum(-1).mean()/delta[i].float().square().sum())
    return torch.stack(terms).mean()


def microbatch_indices(n,width): return [list(range(i,min(i+width,n))) for i in range(0,n,width)]
def request_weights(counts): return [n/sum(counts) for n in counts]
def threshold_stop(mode,loss): return loss<0.05 if mode=='e2e' else loss<=1e-4


def accepted_step(params,opt,objective,groups,scale,retries,overflow=None,stop=None,attempt_observer=None,attempt_sync=None,memory_sampler=None):
    import torch
    attempt=0
    while True:
        if attempt_sync: attempt_sync()
        attempt_start=STAGE_CLOCK();opt.zero_grad(set_to_none=True);components={};probabilities=[];total=0.
        for indices,weight in zip(groups,request_weights([len(g) for g in groups])):
            loss,values=objective(indices)
            total+=float(loss.detach().cpu())*weight
            if memory_sampler: memory_sampler('objective_graph_live')
            (loss*weight*scale).backward()
            if memory_sampler: memory_sampler('backward_graph_live')
            for k,v in values.items():
                if isinstance(v,(int,float)): components[k]=components.get(k,0.)+float(v)*weight
            probabilities.extend(values.get('probabilities',[]))
        for p in params:
            if p.grad is not None: p.grad.div_(scale)
        finite=all(p.grad is not None and bool(torch.isfinite(p.grad).all()) for p in params)
        if overflow is not None and overflow(attempt): finite=False
        if attempt_sync: attempt_sync()
        if finite:
            gradients=[norm(p.grad) for p in params]
            stopped=stop is not None and stop(total)
            if stopped:
                opt.zero_grad(set_to_none=True)
            else: opt.step()
            if attempt_sync: attempt_sync()
            if attempt_observer is not None:
                attempt_observer({'seconds':STAGE_CLOCK()-attempt_start,'accepted':not stopped,'overflow_retry':False,'loss_scale_halvings':retries,'loss_scale':scale,'gradient_norms':gradients})
            return {'retries':retries,'loss_scale':scale,'stopped':stopped,'total':total,'components':components,'gradient_norms':gradients,'probabilities':probabilities}
        if attempt_observer is not None:
            attempt_observer({'seconds':STAGE_CLOCK()-attempt_start,'accepted':False,'overflow_retry':True,'loss_scale_halvings':retries+1,'loss_scale':scale,'gradient_norms':[]})
        opt.zero_grad(set_to_none=True);retries+=1;attempt+=1
        if retries>5: raise Halt('OVERFLOW-RETRIES')
        scale/=2.


def size_scales(reference,candidate):
    na=math.fsum(norm(v) for v in reference.values());nb=math.fsum(norm(v) for v in candidate.values())
    ratios=[norm(reference[l])/norm(v) for l,v in candidate.items() if norm(v)]
    env=min([1.]+ratios)
    return {'NM':na/nb if nb>na else None,'ENV':env if env<1 else None}


def control_match(kind,total,reference,layernorms,refnorms,cosines):
    if any(v<0.999 for v in cosines.values()): return False
    if kind=='NM': return reference*(1.-0.01)<=total<=reference*(1.+0.01)
    return all(layernorms[l]<=1.01*refnorms[l] for l in layernorms)


def apply_stored(H,hp,snap,updates,scale):
    import torch
    if not 0<=scale<=1: raise Halt('SIZE-SCALE')
    restore(H,hp,snap);weights=dict(H.model.named_parameters())
    with torch.no_grad():
        for l in hp.layers: weights[H.weight_name(hp,l)].copy_(to_like(stored_weight(snap[l],updates[l],scale),weights[H.weight_name(hp,l)]))
    return {l:H.snap_layers(hp)[l].float()-snap[l].float() for l in hp.layers}


class Writer:
    def __init__(self,H,hp,telemetry=None,budget=None):
        self.H,self.hp,self.telemetry,self.budget=H,hp,telemetry,budget
        self.original=H.my_edit;self.mode=None;self.baseline_passed=False
        self.trajectory=[];self.last_trace={};self.factors={};self.actual={};self.stored={};self.scale={}
        self.iteration_timings=[];self.phase_timings=[];self.proof=False;self.checks={};self.parity={}
    def __call__(self,hp,requests,P,cache):
        if self.mode is None or self.H._LAW5_DEFAULT_CTX: return self.original(hp,requests,P,cache)
        if not self.baseline_passed: raise Halt('LAW#3-BEFORE-CANDIDATES')
        if hasattr(self,'runtime'):
            started=STAGE_CLOCK()
            declared=[] if self.mode=='apply_stored' else _request_keys(requests)
            recipe=self.runtime['current_recipe'];arm=self.arm(requests)
            value=_ledger_call(self.H,self.ledger,self.stage,recipe,arm,'write',self.targets,declared,
                               lambda:self._write_call(hp,requests,P,cache),expected_hits=0 if self.mode=='apply_stored' else 1)
            self.ledger[-1]['mode']=self.mode
            if self.budget: self.budget.project(0.)
            if self.telemetry: self.telemetry.phase('readout_start')
            sync(self.H);finished=STAGE_CLOCK()
            self.last_trace['wall_clock_s']=finished-started
            self.runtime['_production_eval_started']=finished
            return value
        return self._write_call(hp,requests,P,cache)
    def _write_call(self,hp,requests,P,cache):
        if self.mode=='apply_stored':
            H=self.H;arm=self.arm(requests);self.W0=H.snap_layers(hp);started=STAGE_CLOCK();hooks=hook_snapshot(H.model)
            if self.telemetry: self.telemetry.phase('write_start',mode=self.mode,arm=arm)
            if self.budget: self.budget.project(0.,False)
            sample_memory(H,'stored_merge');sync(H)
            if self.telemetry: self.telemetry.phase('merge_start',mode=self.mode,arm=arm)
            self.actual=apply_stored(H,hp,self.W0,self.stored[arm],self.scale[arm]);sync(H);self.mark_merge()
            if self.telemetry: self.telemetry.phase('merge_end',mode=self.mode,arm=arm)
            if self.budget: self.budget.consume('merge',STAGE_CLOCK()-started)
            self.last_trace={'accepted_steps':0,'overflow_retries':0,'loss_scale_halvings':0,'stop_reason':'stored',
                'loss_components':[],'planned_norms_by_step':[],'wall_clock_s':STAGE_CLOCK()-started,
                'memory_by_phase':copy.deepcopy(getattr(H,'_C10Y_MEMORY',{}))}
            self.iteration_timings=[];self.phase_timings=[];self.parity={}
            if hook_snapshot(H.model)!=hooks: raise Halt('HOOK-RESTORATION')
            if self.telemetry: self.telemetry.phase('write_end',mode=self.mode,arm=arm)
            value=self.norms();sync(H)
            self.last_trace['wall_clock_s']=STAGE_CLOCK()-started
            return value
        return self.write(self.mode,requests,P,cache)
    def arm(self,requests):
        matches=[arm for arm,V in self.H.ARMS.items() if all(V.get(r['subject'])==r['target_new']['str'].lstrip() for r in requests)]
        if len(matches)!=1: raise Halt('ARM-ATTRIBUTION',matches)
        return matches[0]
    def mark_merge(self):
        runtime=getattr(self,'runtime',None)
        if runtime is not None and runtime.get('out') is not None:
            if self.budget: self.budget.write_complete=True
            path=Path(runtime['out'])/('write_complete_'+runtime['tag']+'.json')
            if not path.exists(): write_json(path,{'stage':self.stage,'at':utc(),'recipe':runtime['current_recipe']})
    def norms(self):
        return {str(l):{'delta_norm':norm(d),'weight_norm_before':norm(self.W0[l]),
                        'relative_delta_norm':norm_ratio(d,self.W0[l])} for l,d in self.actual.items()}
    def anchor_components(self,batches,operators,reference,delta):
        import torch
        tokens,targets,kl,mask=packed_batches(self.H,batches);box={}
        module=dict(self.H.model.named_modules())[self.hp.layer_module_tmp.format(self.hp.layers[-1])]
        handle=module.register_forward_hook(lambda m,args,out:box.update(value=out[0] if isinstance(out,tuple) else out))
        try:
            if operators is None: self.H.model.model(input_ids=tokens['input_ids'],attention_mask=tokens['attention_mask'],use_cache=False)
            else:
                with weight_hooks(self.H,self.hp,*operators,mask): self.H.model.model(input_ids=tokens['input_ids'],attention_mask=tokens['attention_mask'],use_cache=False)
            rows=[];offset=0
            for batch in batches:
                J=len(batch['rewriting_prompts'])
                rows.append(torch.stack([box['value'][offset+j,batch['lookup_idxs'][j]] for j in range(J)]));offset+=J+1
            current=torch.stack(rows)
            loss=anchor_loss(current,reference+delta[:,None,:],delta)
            return loss,{'L_z':float(loss.detach().cpu()),'padded_length':tokens['input_ids'].shape[1]}
        finally: handle.remove()
    def write(self,mode,requests,P,cache,check=False,iterations=100,lr_override=None,force_steps=False):
        import torch
        if not self.baseline_passed: raise Halt('LAW#3-BEFORE-CANDIDATES')
        H,hp=self.H,self.hp;torch.manual_seed(0);H.model.eval()
        snapshot=hook_snapshot(H.model);W0=H.snap_layers(hp);self.W0=W0
        flags={p:p.requires_grad for p in H.model.parameters()}
        for p in flags:
            if p.grad is not None: raise Halt('BASE-GRADIENT')
            p.requires_grad_(False)
        started=STAGE_CLOCK();self.trajectory=[];self.iteration_timings=[];self.phase_timings=[]
        try:
            if self.telemetry: self.telemetry.phase('write_start',mode=mode,arm=self.arm(requests))
            sample_memory(H,'capture')
            if self.budget: self.budget.project(0.,False)
            sync(H);phase_start=STAGE_CLOCK()
            self.factors=capture_solve(H,hp,requests,P,cache)
            sync(H);self.phase_timings.append({'name':'capture','seconds':STAGE_CLOCK()-phase_start,'workload':{'requests':len(requests)},'repetition':1})
            if self.budget: self.budget.consume('proofs' if check else 'projector_capture',self.phase_timings[-1]['seconds'])
            phase_start=STAGE_CLOCK();restore(H,hp,W0);sync(H)
            self.phase_timings.append({'name':'restore','seconds':STAGE_CLOCK()-phase_start,'workload':{'layers':len(hp.layers)},'repetition':1})
            if self.budget: self.budget.consume('proofs' if check else 'projector_capture',self.phase_timings[-1]['seconds'])
            As={l:torch.nn.Parameter(v['R'].to(H.DEV).float().clone()) for l,v in self.factors.items()}
            Bs={l:v['B'].to(H.DEV).float().detach() for l,v in self.factors.items()}
            self.As,self.Bs=As,Bs
            batches=[request_batch(H,r,H.get_context_templates(H.model,H.tok)) for r in requests]
            groups=microbatch_indices(len(requests),6)
            operators=(As,Bs,W0);pristine={};anchor0=[];deltas=[]
            with torch.no_grad():
                if mode=='e2e':
                    for indices in groups: pristine[tuple(indices)]=edit_components(H,[batches[i] for i in indices],None)['kl_log_probs'].detach()
                else:
                    for b,r in zip(batches,requests):
                        tokens,_,_,_=packed_batches(H,[b]);box={}
                        module=dict(H.model.named_modules())[hp.layer_module_tmp.format(hp.layers[-1])]
                        handle=module.register_forward_hook(lambda m,args,out:box.update(value=(out[0] if isinstance(out,tuple) else out).detach()))
                        try: H.model.model(input_ids=tokens['input_ids'],attention_mask=tokens['attention_mask'],use_cache=False)
                        finally: handle.remove()
                        h0=torch.stack([box['value'][j,b['lookup_idxs'][j]] for j in range(len(b['rewriting_prompts']))])
                        anchor0.append(h0);deltas.append(H.Z_OVERRIDE[(r['subject'],r['target_new']['str'])].to(H.DEV)-h0[0])
            if mode=='anchor': anchor0=torch.stack(anchor0);deltas=torch.stack(deltas)
            opt=torch.optim.Adam([{'params':[As[l]],'lr':lr_override if lr_override is not None else 0.02*norm(self.factors[l]['R'])/math.sqrt(As[l].numel())} for l in hp.layers],betas=(0.9,0.999),eps=1e-8,weight_decay=0.)
            def objective(indices):
                selected=[batches[i] for i in indices]
                if mode=='anchor': return self.anchor_components(selected,operators,anchor0[indices],deltas[indices])
                values=edit_components(H,selected,pristine[tuple(indices)],operators)
                probabilities=[dict(p,request=indices[p['request']]) for p in values['probabilities']]
                return values['L'],{k:float(values[k].detach().cpu()) for k in ('L_edit','KL_raw','KL_weighted','L')}|{'probabilities':probabilities,'padded_length':values['padded_length']}
            if self.budget: self.budget.project(0.)
            sync(H);phase_start=STAGE_CLOCK()
            self.parity={'init':train_deploy_parity(H,hp,requests,As,Bs,W0,mode,batches,pristine,anchor0 if mode=='anchor' else None,deltas if mode=='anchor' else None)}
            sync(H);self.phase_timings.append({'name':'init_parity','seconds':STAGE_CLOCK()-phase_start,'workload':{'requests':len(requests),'scored_prompts':len(requests)*4},'repetition':1})
            if self.budget: self.budget.consume('proofs' if check else 'readout',self.phase_timings[-1]['seconds'])
            scale,retries,accepted=1024.,0,0;components=[];planned=[];stop='cap'
            while accepted<iterations:
                if self.budget: self.budget.project(max(self.iteration_timings[-1]['seconds'] if self.iteration_timings else 0.,0.)*(iterations-accepted+5-retries),False)
                sample_memory(H)
                sync(H);iteration_start=STAGE_CLOCK();first_attempt=len(self.iteration_timings)
                result=accepted_step(list(As.values()),opt,objective,groups,scale,retries,stop=None if force_steps else lambda value:threshold_stop(mode,value),attempt_observer=self.iteration_timings.append,attempt_sync=lambda:sync(H),memory_sampler=lambda phase:sample_memory(H,phase))
                sync(H)
                scale,retries=result['loss_scale'],result['retries']
                padded_lengths=[packed_batches(H,[batches[i] for i in g])[0]['input_ids'].shape[1] for g in groups]
                base_unchanged=all(tensor_sha(v)==tensor_sha(W0[l]) for l,v in H.snap_layers(hp).items())
                if not base_unchanged: raise Halt('BASE-WEIGHT-MUTATION')
                for attempt in self.iteration_timings[first_attempt:]:
                    attempt.update({'base_band_hashes_unchanged':base_unchanged,
                        'workload':{'requests':len(requests),'micro_batches':len(groups),'accepted_steps':int(attempt['accepted'] and not result['stopped']),
                            'retries':int(attempt['overflow_retry']),'padded_lengths':padded_lengths}})
                self.iteration_timings[-1]['accepted']=not result['stopped']
                components.append(result['components']|{'accepted_step':accepted,'total':result['total']})
                planned.append([gram_norm(As[l],Bs[l]) for l in hp.layers])
                if any(p.grad is not None for p in H.model.parameters()): raise Halt('BASE-GRADIENT')
                if result['stopped']:
                    sync(H);duration=STAGE_CLOCK()-iteration_start
                    self.iteration_timings[-1]['seconds']+=max(0.,duration-math.fsum(t['seconds'] for t in self.iteration_timings[first_attempt:]))
                    if self.budget: self.budget.consume('proofs' if check else 'optimisation',duration)
                    stop='threshold';break
                accepted+=1;self.trajectory.append({l:a.detach().cpu().clone() for l,a in As.items()})
                if self.telemetry:
                    self.telemetry.opt_step(accepted,result['components'],scale,retries,{str(l):value for l,value in zip(hp.layers,planned[-1])})
                    if mode=='e2e': self.telemetry.target_probs(probabilities=result['probabilities'])
                sample_memory(H)
                sync(H);duration=STAGE_CLOCK()-iteration_start
                self.iteration_timings[-1]['seconds']+=max(0.,duration-math.fsum(t['seconds'] for t in self.iteration_timings[first_attempt:]))
                if self.budget: self.budget.consume('proofs' if check else 'optimisation',duration)
            if self.budget: self.budget.project(0.)
            sample_memory(H,'parity');sync(H);phase_start=STAGE_CLOCK()
            self.parity['final']=train_deploy_parity(H,hp,requests,As,Bs,W0,mode,batches,pristine,anchor0 if mode=='anchor' else None,deltas if mode=='anchor' else None)
            sync(H);self.phase_timings.append({'name':'final_parity','seconds':STAGE_CLOCK()-phase_start,'workload':{'requests':len(requests),'scored_prompts':len(requests)*4},'repetition':1})
            if self.budget: self.budget.consume('proofs' if check else 'readout',self.phase_timings[-1]['seconds'])
            if self.budget: self.budget.project(0.)
            sample_memory(H,'merge');sync(H);phase_start=STAGE_CLOCK()
            if self.telemetry: self.telemetry.phase('merge_start',mode=mode,arm=self.arm(requests))
            with torch.no_grad():
                weights=dict(H.model.named_parameters())
                for l in hp.layers: weights[H.weight_name(hp,l)][...] += to_like(As[l]@Bs[l],weights[H.weight_name(hp,l)])
            sync(H);self.mark_merge()
            if self.telemetry: self.telemetry.phase('merge_end',mode=mode,arm=self.arm(requests))
            self.phase_timings.append({'name':'merge','seconds':STAGE_CLOCK()-phase_start,'workload':{'layers':len(hp.layers)},'repetition':1})
            if self.budget: self.budget.consume('proofs' if check else 'merge',self.phase_timings[-1]['seconds'])
            self.actual={l:H.snap_layers(hp)[l].float()-W0[l].float() for l in hp.layers}
            self.last_trace={'accepted_steps':accepted,'overflow_retries':retries,'loss_scale_halvings':retries,'stop_reason':stop,
                'loss_components':components,'planned_norms_by_step':planned,'wall_clock_s':STAGE_CLOCK()-started,
                'memory_by_phase':getattr(H,'_C10Y_MEMORY',{}).copy()}
            if not projector_gate({l:As[l].detach()@Bs[l] for l in hp.layers},self.actual,P): raise Halt('PROJECTOR-PROPERTY')
            if self.telemetry: self.telemetry.phase('write_end',mode=mode,arm=self.arm(requests))
            value=self.norms();sync(H)
            return value
        finally:
            if hook_snapshot(H.model)!=snapshot: raise Halt('HOOK-RESTORATION')
            for p,flag in flags.items(): p.requires_grad_(flag)
            sync(H)
            if self.last_trace: self.last_trace['wall_clock_s']=STAGE_CLOCK()-started


def sync(H):
    if str(H.DEV)=='mps':
        import torch
        torch.mps.synchronize()


def memory_gate(sample):
    names=('current_bytes','driver_bytes','rss_bytes','available_bytes')
    if any(k not in sample or type(sample[k]) is not int or sample[k]<0 for k in names): raise Halt('MISSING-MEMORY-TELEMETRY')
    G=2**30
    if sample['driver_bytes']>32*G or sample['rss_bytes']>40*G or sample['available_bytes']<8*G or sample['driver_bytes']+sample['rss_bytes']>40*G: raise Halt('HALTED-RESOURCE',sample)
    return sample


def sample_memory(H,phase='backward'):
    if str(H.DEV)=='cpu':
        if not os.environ.get('C10Y_SELFTEST'): raise Halt('DEVICE')
        sample={'current_bytes':0,'driver_bytes':0,'rss_bytes':0,'available_bytes':48*2**30}
    else:
        import torch,psutil
        torch.mps.synchronize()
        sample={'current_bytes':int(torch.mps.current_allocated_memory()),'driver_bytes':int(torch.mps.driver_allocated_memory()),
                'rss_bytes':int(psutil.Process().memory_info().rss),'available_bytes':int(psutil.virtual_memory().available)}
    memory_gate(sample)
    sample=sample|{'host_available_bytes':sample['available_bytes'],'synchronised':True,'at':utc()}
    if not hasattr(H,'_C10Y_MEMORY'): H._C10Y_MEMORY={}
    previous=H._C10Y_MEMORY.get(phase)
    if previous:
        for k in ('current_bytes','driver_bytes','rss_bytes'): sample[k]=max(previous[k],sample[k])
        sample['host_available_bytes']=min(previous['host_available_bytes'],sample['host_available_bytes'])
    H._C10Y_MEMORY[phase]=sample
    return sample


class Budget:
    def __init__(self,start,cap,stage,clock=None):
        self.start,self.cap,self.stage,self.clock=start,cap,stage,clock or STAGE_CLOCK
        self.readout_reserve=1380. if stage==1 else 0.;self.write_complete=False
        self.remaining=None;self.readout_spent=0.
    def configure(self,forecast,startup=()):
        self.remaining={p['name']:float(p['upper_s']) for p in forecast['phases']}
        self.readout_reserve=max(self.readout_reserve,self.remaining['readout'])
        for entry in startup: self.consume(entry['name'],entry['seconds'])
    def consume(self,phase,seconds):
        if self.remaining is not None and phase in self.remaining:
            self.remaining[phase]=max(0.,self.remaining[phase]-seconds)
            if phase=='readout' and self.write_complete: self.readout_spent+=seconds
    def project(self,remaining,write_complete=False):
        reserve=max(0.,self.readout_reserve-self.readout_spent)
        if self.remaining is not None:
            remaining=max(remaining,self.remaining.get('optimisation',0.))+math.fsum(v for k,v in self.remaining.items() if k not in ('optimisation','readout'))
            reserve=max(reserve,self.remaining['readout'])
        projected=self.clock()-self.start+remaining+reserve
        if projected>self.cap: raise Halt('INCOMPLETE-BUDGET' if write_complete or self.write_complete else 'HALTED-BUDGET',{'projected_s':projected,'cap_s':self.cap})
        return projected


def launch_documents(stage,go,spend,predecessor):
    if not isinstance(go,dict) or any(k not in go for k in ('decision_id','experiment','stage','recorded_in','at')) or go['experiment']!='C10Y' or go['stage']!=stage or any(not isinstance(go[k],str) or not go[k] for k in ('decision_id','recorded_in','at')): raise Halt('GO-RECORD')
    cap=7200.
    if stage in (2,3,'calibration'):
        if not isinstance(spend,dict) or spend.get('stage')!=stage or not isinstance(spend.get('decision_id'),str) or not spend['decision_id']: raise Halt('SPENDING-DECISION')
        cap=spend.get('cap_s')
        if type(cap) not in (float,int) or not math.isfinite(cap) or cap<=0 or (stage=='calibration' and cap>7200): raise Halt('SPENDING-CAP')
    if stage==2 and (not predecessor or predecessor.get('label')!='SCREEN-PASS'): raise Halt('STAGE2-INELIGIBLE')
    if stage==3 and (not predecessor or predecessor.get('label') not in ('LEAD','PARTIAL') or not predecessor.get('advance',False)): raise Halt('STAGE3-INELIGIBLE')
    return float(cap)


def _forecast_workload(workload,descriptive=False):
    if descriptive and isinstance(workload,str) and workload.strip(): return workload
    fields=('requests','scored_prompts','micro_batches','accepted_steps','retries')
    if not isinstance(workload,dict) or 'arms' not in workload or any(k not in workload for k in fields):
        raise ValueError('missing workload fields')
    arms=workload['arms']
    if not isinstance(arms,list) or any(not isinstance(a,str) or a not in ARMS for a in arms) or len(set(arms))!=len(arms):
        raise ValueError('invalid workload arms')
    if any(type(workload[k]) is not int or workload[k]<0 for k in fields): raise ValueError('invalid workload counts')
    lengths=workload.get('padded_lengths')
    if lengths is not None and (not isinstance(lengths,list) or not lengths or any(type(n) is not int or n<1 for n in lengths)
                               or len(lengths)!=workload['micro_batches']):
        raise ValueError('invalid padded lengths')
    keys=('arms',)+fields+('padded_lengths','layers','model','model_rev','tokenizer')
    return {k:copy.deepcopy(workload[k]) for k in keys if k in workload}


def _calibration_timings(record,identity=None):
    required=('schema','outcome','sources','fingerprint','env','device','prereg_sha256','timings','memory',
              'T_cal','template_token_lengths','input_hashes_start','input_hashes_end','artifacts','started_at','finished_at')
    if not isinstance(record,dict) or any(k not in record for k in required): raise ValueError('incomplete calibration record')
    if record['schema']!='c10y_directdw_calibration/v1' or record['outcome']!='COMPLETE': raise ValueError('incomplete calibration schema/outcome')
    if identity is not None and any(record.get(k)!=v for k,v in identity.items()): raise ValueError('stale calibration identity')
    valid_sha=lambda value:isinstance(value,str) and len(value)==64 and all(c in '0123456789abcdef' for c in value.lower())
    if not isinstance(record['sources'],dict) or not record['sources'] or any(not valid_sha(v) for v in record['sources'].values()):
        raise ValueError('invalid calibration source hashes')
    if not isinstance(record['fingerprint'],dict) or not isinstance(record['env'],dict) or not record['env'] or not valid_sha(record['prereg_sha256']):
        raise ValueError('invalid calibration identity fields')
    if not isinstance(record['memory'],dict) or not record['memory']: raise ValueError('missing calibration memory observations')
    for key in ('started_at','finished_at'):
        if not isinstance(record[key],str) or not record[key].strip(): raise ValueError('missing calibration times')
    inputs=record['input_hashes_start'];end=record['input_hashes_end']
    if not isinstance(inputs,dict) or not {'covariance','model','tokenizer','hparams'}<=set(inputs) or inputs!=end or any(not valid_sha(v) for v in inputs.values()):
        raise ValueError('calibration input identity missing/drifted')
    artifacts=record['artifacts']
    names=('context_templates_calib.json','overlap_audit_calib.json','targets_calib.pt','ledger_calib.json','law5_calib.json','step0_calib.json')
    if not isinstance(artifacts,dict) or not set(names)<=set(artifacts) or any(not valid_sha(v) for v in artifacts.values()):
        raise ValueError('missing calibration artifact identities')
    templates=record['template_token_lengths']
    if not isinstance(templates,list) or len(templates)!=6 or any(type(n) is not int or n<1 for n in templates):
        raise ValueError('invalid template token lengths')
    timings=record['timings'];result=[];seen=set();padded=[]
    if not isinstance(timings,list) or not timings: raise ValueError('missing calibration timings')
    for entry in timings:
        if not isinstance(entry,dict) or any(k not in entry for k in ('name','seconds','repetition','workload','status','synchronised')):
            raise ValueError('incomplete timing entry')
        if not isinstance(entry['name'],str) or not entry['name'] or type(entry['seconds']) not in (int,float) or not math.isfinite(entry['seconds']) or entry['seconds']<0:
            raise ValueError('invalid raw timing')
        if type(entry['repetition']) is not int or entry['repetition']<1 or entry['status']!='COMPLETED' or entry['synchronised'] is not True:
            raise ValueError('invalid timing repetition/status/synchronisation')
        workload=_forecast_workload(entry['workload']);padded.extend(workload.get('padded_lengths',[]))
        if 'arm' in entry and (entry['arm'] not in ARMS or workload['arms']!=[entry['arm']]): raise ValueError('timing arm mismatch')
        if 'mode' in entry and entry['mode']!='e2e': raise ValueError('non-calibration timing mode')
        key=(entry['name'],tuple(workload['arms']),entry.get('mode'),entry['repetition'])
        if key in seen: raise ValueError('duplicate timing repetition')
        seen.add(key)
        if entry['name'] in ('executed_loop_step','smoke_step'):
            if type(entry.get('accepted')) is not bool or type(entry.get('overflow_retry')) is not bool or entry['accepted']==entry['overflow_retry']:
                raise ValueError('invalid iteration outcome')
            if type(entry.get('loss_scale_halvings')) is not int or entry['loss_scale_halvings']<0:
                raise ValueError('invalid loss-scale halvings')
            if workload['accepted_steps']!=int(entry['accepted']) or workload['retries']!=int(entry['overflow_retry']):
                raise ValueError('iteration workload/outcome mismatch')
        keys=('name','seconds','repetition','status','synchronised','arm','mode','accepted','overflow_retry','loss_scale_halvings','measurement')
        result.append({k:copy.deepcopy(entry[k]) for k in keys if k in entry}|{'workload':workload})
    if type(record['T_cal']) is not int or record['T_cal']<1 or not padded or record['T_cal']!=max(padded):
        raise ValueError('invalid T_cal maximum')
    return result


def _calibration_phase(timings,phase):
    proof=('original_my_edit','capture_solve','zero_step_merge','zero_step_evaluation','zero_step_init_parity',
           'executed_loop_step','executed_loop_merge','executed_loop_evaluation','projector_property','gradient_e2e',
           'objective_construction','accumulation_reference_e2e','accumulation_e2e_6+6','accumulation_e2e_5+7',
           'restoration_hooks','smoke_step','smoke_restore_hash')
    extra=tuple(prefix+'_'+suffix for prefix in ('zero_step','executed_loop','smoke')
                for suffix in ('capture','restore','init_parity','final_parity','merge'))+('smoke_loss_before',)
    mapping={'preflight':('preflight',),'load':('load',),'contexts_targets':('contexts_overlap','target_solve'),
             'baseline':('baseline_projector','baseline_law5','baseline_write','baseline_evaluation','baseline_recipe_overhead','law3'),
             'proofs':proof,'projector_capture':('baseline_projector','baseline_law5','baseline_recipe_overhead','capture_solve'),
             'optimisation':('executed_loop_step','smoke_step'),'merge':('zero_step_merge','executed_loop_merge'),
             'readout':('baseline_evaluation','zero_step_init_parity','projector_property','executed_loop_step','smoke_step'),
             'shutdown':('shutdown',)}
    name=phase.get('name')
    if not isinstance(name,str) or name not in mapping: raise ValueError('unsupported calibration phase')
    wanted=set(mapping[name])|(set(extra) if name=='proofs' else set())
    rows=[entry for entry in timings if entry['name'] in wanted and
          (name!='readout' or entry['name']!='baseline_evaluation' or entry['workload']['arms']==[A7])]
    names={entry['name'] for entry in rows};cited=phase.get('timing_names')
    if not set(mapping[name])<=names or not isinstance(cited,list) or any(not isinstance(n,str) for n in cited) or len(set(cited))!=len(cited) or set(cited)!=names:
        raise ValueError('C3 timing mapping mismatch: '+name)
    if type(phase.get('repetitions')) is not int or phase['repetitions']!=len(rows): raise ValueError('all repetitions must be cited: '+name)
    for unit in ('target_solve','baseline_write','baseline_evaluation'):
        group=[entry for entry in rows if entry['name']==unit]
        if not group: continue
        expected={A7} if name=='readout' else set(ARMS)
        if len(group)!=len(expected) or {tuple(entry['workload']['arms']) for entry in group}!={(arm,) for arm in expected} or any(entry['workload']['requests']!=24 for entry in group):
            raise ValueError('missing arm workload/repetition: '+unit)
    original=[entry for entry in rows if entry['name']=='original_my_edit']
    if original and (len(original)!=2 or {entry['repetition'] for entry in original}!={1,2} or
                     any(entry['workload']['arms']!=[A7] or entry['workload']['requests']!=24 for entry in original)):
        raise ValueError('both original my_edit repetitions required')
    iterations=[entry for entry in rows if entry['name'] in ('executed_loop_step','smoke_step')]
    if iterations:
        shape=None
        for unit in ('executed_loop_step','smoke_step'):
            group=[entry for entry in iterations if entry['name']==unit]
            if sum(entry['accepted'] for entry in group)!=3 or sum(entry['overflow_retry'] for entry in group)>5 or {entry['repetition'] for entry in group}!=set(range(1,len(group)+1)):
                raise ValueError('six accepted iterations plus all retries required')
            for entry in group:
                workload=entry['workload'];lengths=workload.get('padded_lengths')
                if workload['arms']!=[A7] or workload['requests']!=24 or workload['micro_batches']!=4 or not lengths:
                    raise ValueError('incomparable iteration workload')
                if shape is None: shape=lengths
                if lengths!=shape: raise ValueError('incomparable iteration padded shape')
    if name=='optimisation':
        workload=_forecast_workload(phase.get('workload'))
        if workload['arms']!=[A7] or any(workload[k]!=v for k,v in (('requests',24),('micro_batches',4),('accepted_steps',100),('retries',5))):
            raise ValueError('stage optimisation requires 105 attempts')
        lower=105*max(entry['seconds'] for entry in iterations)
    elif name=='merge': lower=max(entry['seconds'] for entry in rows)
    elif name=='readout':
        lower=max(1380.,math.fsum(entry['seconds'] for entry in rows if entry not in iterations)+max(entry['seconds'] for entry in iterations))
    else: lower=math.fsum(entry['seconds'] for entry in rows)
    return rows,lower


def budget_gate(forecast,cap,admission=None):
    reasons=[];records={};identity=None
    try:
        if not isinstance(forecast,dict): raise ValueError('invalid forecast record')
        stage=forecast.get('stage')
        if not ((type(stage) is int and stage in (1,2,3)) or stage=='calibration'): raise ValueError('invalid forecast stage')
        if type(cap) not in (int,float) or not math.isfinite(cap) or cap<=0 or (stage in (1,'calibration') and cap>7200): raise ValueError('invalid forecast cap')
        phases=forecast.get('phases')
        if not isinstance(phases,list) or any(not isinstance(p,dict) or not isinstance(p.get('name'),str) for p in phases): raise ValueError('invalid forecast phases')
        names=[p['name'] for p in phases]
        if not set(FORECAST_PHASES)<=set(names) or set(names)-set(FORECAST_PHASES)-{'telemetry'} or len(set(names))!=len(names): raise ValueError('missing/unknown/duplicate phases')
        if forecast.get('status')=='UNVERIFIED': raise ValueError('forecast UNVERIFIED')
        if admission is not None and admission['telemetry'] and 'telemetry' not in names: raise ValueError('T10 telemetry phase required')
        for phase in phases:
            try:
                required=('artifact','sha256','workload','repetitions','scaling_assumption','upper_s','measured')
                if any(k not in phase for k in required): raise ValueError('unsupported phase')
                if type(phase['measured']) is not bool or type(phase['repetitions']) is not int or phase['repetitions']<1: raise ValueError('invalid support/repetitions')
                _forecast_workload(phase['workload'],descriptive=not phase['measured'])
                if not isinstance(phase['scaling_assumption'],str) or not phase['scaling_assumption'].strip(): raise ValueError('missing justified scaling assumption')
                upper=phase['upper_s']
                if type(upper) not in (int,float) or not math.isfinite(upper) or upper<0: raise ValueError('invalid bound')
                if phase['name']=='readout' and stage in (1,'calibration') and upper<1380: raise ValueError('readout reserve below 1380 seconds')
                if not isinstance(phase['artifact'],str) or not isinstance(phase['sha256'],str): raise ValueError('invalid timing identity')
                path=Path(phase['artifact'])
                if phase['name']=='telemetry':
                    if not path.is_absolute(): raise ValueError('T10 absolute artifact required')
                    cached=getattr(admission,'record',None)
                    if cached is not None and admission['telemetry_inertness']=={'path':str(path.resolve()),'sha256':phase['sha256']}:
                        timing_record=cached
                    else:
                        raw=path.read_bytes()
                        if hashlib.sha256(raw).hexdigest()!=phase['sha256']: raise ValueError('T10 identity mismatch')
                        timing_record=strict_json(raw);validate_inertness(timing_record)
                    telemetry_bound(phase,stage,timing_record)
                    continue
                if not path.is_absolute() or not path.is_file() or sha(path)!=phase['sha256']: raise ValueError('timing identity mismatch')
                timings=None
                if path.name=='calibration.json':
                    if stage!=1: raise ValueError('C4 calibration supports stage 1 only')
                    key=str(path.resolve())
                    if key not in records:
                        if identity is None: identity=calibration_identity()
                        records[key]=_calibration_timings(strict_load(path),identity)
                    timings=records[key]
                if phase['measured']:
                    if timings is None: raise ValueError('measured support needs C3 calibration mapping')
                    rows,lower=_calibration_phase(timings,phase)
                    if digest(phase.get('measurements'))!=digest(rows): raise ValueError('forged/omitted calibration measurements')
                    if upper<lower: raise ValueError('bound below comparable measured workload')
                elif not isinstance(phase.get('justification'),str) or not phase['justification'].strip():
                    raise ValueError('independent bound requires explicit justification')
            except (ValueError,OSError,KeyError,TypeError,OverflowError) as error:
                reasons.append(phase['name']+': '+str(error))
        if reasons: return {'status':'UNVERIFIED','launched':False,'reasons':reasons}
        total=math.fsum(phase['upper_s'] for phase in phases)
        return {'status':'READY' if total<=cap else 'HALTED-BUDGET','launched':False,'projected_s':total,'cap_s':cap}
    except (ValueError,OSError,KeyError,TypeError,OverflowError) as error:
        return {'status':'UNVERIFIED','launched':False,'reasons':[str(error)]}


def schedule_halt(root,code,state,contexts=None):
    p=Path(root)/'results/c10y_directdw_schedule_halt.json'
    if not p.exists(): write_json(p,{'code':code,'at':utc(),'detail':state,'context_templates':contexts})


def refuse_schedule_halt(root):
    p=Path(root)/'results/c10y_directdw_schedule_halt.json'
    if p.exists(): raise Halt('SCHEDULE-HALTED',strict_load(p))


def pinned_templates():
    tree=ast.parse((Path(ROOT)/SOURCE_PATHS['templates']).read_text())
    entries=[node for node in tree.body if isinstance(node,ast.Assign) and any(isinstance(n,ast.Name) and n.id=='TEMPLATES' for n in node.targets)]
    if len(entries)!=1: raise Halt('TEMPLATE-SOURCE')
    flat=ast.literal_eval(entries[0].value)
    if not isinstance(flat,(list,tuple)) or len(flat)!=6 or any(type(s) is not str for s in flat) or flat[0]!='{}': raise Halt('TEMPLATE-SHAPE')
    engine=[[flat[0]],list(flat[1:])]
    if hashlib.sha256(json.dumps(engine).encode()).hexdigest()!=PINNED_ENGINE_SHA or digest(list(flat))!=PINNED_FLAT_SHA: raise Halt('TEMPLATE-DIGEST')
    return engine


def freeze_contexts(H,path,expected=None):
    path=Path(path)
    pinned=pinned_templates()
    if path.exists():
        if expected is None: raise Halt('CONTEXT-IDENTITY')
        if sha(path)!=expected: raise Halt('CONTEXT-SHA')
        templates=strict_load(path)
        if templates!=pinned: raise Halt('CONTEXT-PIN')
    else:
        if expected is not None: raise Halt('MISSING-CONTEXTS')
        templates=pinned;write_json(path,templates)
    H.get_context_templates.__globals__['CONTEXT_TEMPLATES_CACHE']=templates
    H._C10Y_CONTEXTS=templates
    return {'path':str(path.resolve()),'sha256':sha(path)}


def context_evidence(path):
    path=Path(path).resolve()
    return {'path':str(path),'sha256':sha(path) if path.is_file() else PINNED_ENGINE_SHA,
            'hash_basis':'file_bytes' if path.is_file() else 'expected_engine_form_default_json'}


def stage_context_source(path,expected):
    path=Path(path)
    if not path.is_absolute() or 'calib' in path.parent.name or path.name!='context_templates.json' or sha(path)!=expected: raise Halt('CONTEXT-SOURCE')
    if path.resolve().parent.parent != (Path(ROOT)/'results').resolve() or not (path.parent.name=='c10y_directdw' or re.fullmatch(r'c10y_directdw_s1_rerun[1-9][0-9]*',path.parent.name)):
        raise Halt('CONTEXT-STAGE1-NAMESPACE')
    reader=importlib.import_module('c10y_directdw_read')
    reading=reader.classify(reader.load(path.parent/'screen.json'))
    if reading['label']!='SCREEN-PASS': raise Halt('CONTEXT-STAGE1-INELIGIBLE')
    return path.resolve()


def overlap_audit(contexts,H):
    def clean(s): return ' '.join(re.sub(r'[^\w{}\s]','',s.casefold()).split())
    inputs=[c for group in contexts for c in group]+[c.replace('{}',H.CANON) for group in contexts for c in group]+['{} is a']
    preliminary=[{'input':s,'heldout':p,'kind':'containment'} for s in inputs for p in H.PTEST if clean(p) in clean(s)]
    if preliminary: return {'clean':False,'rule':'casefold,punctuation-remove,whitespace-collapse,preserve-placeholder,exact-and-containment','inputs':inputs,'matches':preliminary}
    for V in H.ARMS.values():
        for s,v in V.items():
            ids=H.tgt_ids(v)
            inputs += [c.format(H.CANON).format(s)+H.tok.decode(ids[:-1]) for group in contexts for c in group]
    matches=[{'input':s,'heldout':p,'kind':'exact' if clean(p)==clean(s) else 'containment'} for s in inputs for p in H.PTEST if clean(p) in clean(s)]
    return {'clean':not matches,'rule':'casefold,punctuation-remove,whitespace-collapse,preserve-placeholder,exact-and-containment','inputs':inputs,'matches':matches}


class Telemetry:
    def __init__(self,out,process,run_id):
        self.enabled=True;self.file=None;self.process=process;self.run_id=run_id;self.started=0.;self.previous=0.;self.cumulative=0.;self.entered=0.
        try:
            self.started=self.previous=self.entered=TELEMETRY_CLOCK()
            folder=Path(out)/'telemetry';folder.mkdir(parents=True,exist_ok=True)
            self.file=(folder/('telemetry_'+process+'.jsonl')).open('a')
            self.emit('header',schema='c10y_directdw_telemetry/v1',telemetry=True)
        except Exception as e: self.disable(e)
    def disable(self,error):
        if self.enabled:
            self.enabled=False
            print('C10Y_TELEMETRY_DISABLED '+type(error).__name__+': '+str(error),file=sys.__stderr__,flush=True)
    def emit(self,kind,**payload):
        try:
            if not self.enabled: return
            now=TELEMETRY_CLOCK()
            row={'kind':kind,'t_utc':utc(),'elapsed_s':now-self.entered,'cumulative_s':self.cumulative,
                 'process':self.process,'run_id':self.run_id,**payload}
            self.file.write(json.dumps(row,allow_nan=False,sort_keys=True,separators=(',',':'))+'\n')
            self.file.flush();os.fsync(self.file.fileno());self.previous=now;self.cumulative+=TELEMETRY_CLOCK()-self.entered
        except Exception as e: self.disable(e)
    def phase(self,phase,**scope):
        try:
            self.entered=TELEMETRY_CLOCK();self.emit('phase',phase=phase,**scope)
        except Exception as e: self.disable(e)
    def opt_step(self,step,components,loss_scale,retries,planned_norms):
        try:
            self.entered=TELEMETRY_CLOCK();self.emit('opt_step',step=step,components=components,loss_scale=loss_scale,retries=retries,planned_norms=planned_norms)
        except Exception as e: self.disable(e)
    def target_probs(self,probabilities=None,f_ij=None,r_ij=None):
        try:
            self.entered=TELEMETRY_CLOCK();data={}
            if probabilities is not None: data['probabilities']=probabilities
            if f_ij is not None: data['f_ij']=f_ij
            if r_ij is not None: data['r_ij']=r_ij
            self.emit('target_probs',**data)
        except Exception as e: self.disable(e)
    def write_norms(self,norms,recipe,arm,harness_fp32=None):
        try:
            self.entered=TELEMETRY_CLOCK();payload={'norms':norms,'recipe':recipe,'arm':arm}
            if harness_fp32 is not None: payload['harness_fp32']=harness_fp32
            self.emit('write_norms',**payload)
        except Exception as e: self.disable(e)
    def logit_lens(self,H,hp,where,recipe='pristine',arm=A7):
        try:
            self.entered=TELEMETRY_CLOCK()
            import torch
            items=[];norm_layer=dict(H.model.named_modules())[getattr(hp,'ln_f_module','model.norm')]
            head=H.model.lm_head
            if max(hp.layers)>=H.model.config.num_hidden_layers-1: raise ValueError('lens final-normalised layer')
            with torch.no_grad():
                for s in H.FICTION:
                    prompt=H.CANON.format(s);ids=H.tok(prompt,return_tensors='pt').to(H.DEV)
                    out=H.model(input_ids=ids['input_ids'],attention_mask=ids['attention_mask'],output_hidden_states=True,use_cache=False);top={}
                    for l in hp.layers:
                        logits=head(norm_layer(out.hidden_states[l+1][0,-1]))
                        probs=cpu64(logits).softmax(-1);values,index=probs.topk(5)
                        top[str(l)]=[[int(i),H.tok.decode([int(i)]),float(v)] for i,v in zip(index,values)]
                    items.append({'subj':s,'prompt':prompt,'top':top})
            self.emit('logit_lens',layers=list(hp.layers),items=items,where=where,recipe=recipe,arm=arm)
        except Exception as e: self.disable(e)
    def sink(self,H,recipe,phase,prompt,target_ids,gen):
        try:
            self.entered=TELEMETRY_CLOCK()
            requests=(H._ARM_STATE or {}).get('requests',[])
            matches=[(arm,r['subject'],r['target_new']['str'].lstrip(),template)
                for r in requests for template in [H.CANON]+H.PTEST if template.format(r['subject'])==prompt
                for arm,V in H.ARMS.items() if V.get(r['subject'])==r['target_new']['str'].lstrip()
                and H.tgt_ids(V[r['subject']])==list(target_ids)]
            if len(matches)!=1: raise ValueError('unattributed subject/template/arm')
            arm,subj,val,template=matches[0]
            self.emit('answer',recipe=recipe,arm=arm,phase=phase,subj=subj,val=val,template=template,prompt=prompt,
                      target_ids=list(target_ids),generated_ids=list(gen),text=H.tok.decode(gen),
                      full=list(gen)==list(target_ids),first=gen[0]==target_ids[0])
        except Exception as e: self.disable(e)
    def close(self):
        try:
            if self.file is not None: self.file.close()
        except Exception as e: self.disable(e)


def telemetry_factory(out,process,run_id,enabled):
    return Telemetry(out,process,run_id) if enabled else None


def make_scorer(H,sink,reference=False):
    torch,tok,model,DEV=__import__('torch'),H.tok,H.model,H.DEV
    if reference:
        path=Path(ROOT)/SOURCE_PATHS['harness']
        function=next(n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='full_seq_match')
        if not isinstance(function.body[-1],ast.Return): raise Halt('SCORER-SOURCE')
        function.body.insert(-1,ast.parse('sink(prompt,target_ids,gen)').body[0])
        module=ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[]))
        space={'torch':torch,'tok':tok,'model':model,'DEV':DEV,'sink':sink}
        exec(compile(module,str(path),'exec'),space)
        return space['full_seq_match']
    @torch.no_grad()
    def full_seq_match(prompt,target_ids):
        ids = tok(prompt, return_tensors="pt").to(DEV)["input_ids"]
        cur = ids
        gen = []
        for _ in range(len(target_ids)):
            nxt = int(model(cur).logits[0, -1].argmax())
            gen.append(nxt)
            cur = torch.cat([cur, torch.tensor([[nxt]], device=DEV)], dim=1)
        sink(prompt,target_ids,gen)
        return gen == list(target_ids), gen[0] == target_ids[0]
    return full_seq_match


def scorer_ast_check(path):
    real=next(n for n in ast.parse(Path(path).read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='full_seq_match')
    own=next(n for n in ast.walk(ast.parse(Path(__file__).read_text())) if isinstance(n,ast.FunctionDef) and n.name=='full_seq_match')
    own=copy.deepcopy(own)
    own.body=[n for n in own.body if not (isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='sink')]
    return ast.dump(real,include_attributes=False)==ast.dump(own,include_attributes=False)


class TelemetryAdmission(dict):
    pass


def validate_inertness(record):
    if record.get('verdict')!='INERT' or record.get('device')!='mps' or any(record.get(k) is not True for k in ('control_equal','telemetry_equal','generated_equal','telemetry_complete','weights_unchanged')) or record.get('answer_calls')!=96 or record.get('lens_forwards')!=48: raise Halt('TELEMETRY-NOT-INERT')
    if record.get('sources')!=source_hashes() or record.get('env')!=environment_identity(): raise Halt('TELEMETRY-IDENTITY')


def telemetry_workload(stage):
    # Counts bound every required arm/control at T_max and the four gradient
    # attempts. The phase bound also covers one header and one halt marker.
    return {'phase':78,'opt_step':100,'target_probs':101,'write_norms':4,'logit_lens':2,'answer':384} if stage==1 else {'phase':274,'opt_step':600,'target_probs':312,'write_norms':15,'logit_lens':5,'answer':1440}


def telemetry_bound(phase,stage,record):
    if not phase['measured']: raise ValueError('T10 requires measured per-kind evidence')
    rows=phase.get('kinds');counts=telemetry_workload(stage)
    if not isinstance(rows,list) or len(rows)!=len(counts) or {r.get('kind') for r in rows if isinstance(r,dict)}!=set(counts): raise ValueError('missing/duplicate telemetry kinds')
    required_payload={'requests':24,'frames':6,'target_positions':6,'layers':5,'weight_shape':[2048,11008],'vocabulary':151936}
    totals=[]
    for row in rows:
        kind=row['kind'];count=row.get('count');bound=row.get('upper_s')
        if type(count) is not int or count<counts[kind] or type(bound) not in (int,float) or not math.isfinite(bound) or bound<0: raise ValueError('T10 count/bound')
        if not isinstance(row.get('scaling_assumption'),str) or not row['scaling_assumption'].strip(): raise ValueError('T10 missing scaling')
        if kind in ('answer','logit_lens'):
            observed=record['answer_line_seconds' if kind=='answer' else 'lens_forward_seconds'];payload=record[kind.split('_')[0]+'_payload' if kind=='answer' else 'lens_payload']
            repetitions=96 if kind=='answer' else 2
        else:
            evidence=record['timings'][kind];observed=evidence['seconds'];payload=evidence['payload'];repetitions=evidence['repetitions']
        if type(repetitions) is not int or repetitions<1 or not isinstance(observed,list) or len(observed)!=repetitions or any(type(t) not in (int,float) or not math.isfinite(t) or t<0 for t in observed): raise ValueError('T10 timing repetitions')
        if not isinstance(payload,dict): raise ValueError('T10 payload')
        for key,minimum in required_payload.items():
            value=payload.get(key)
            if key=='weight_shape':
                if not isinstance(value,list) or len(value)!=2 or any(type(v) is not int or v<m for v,m in zip(value,minimum)): raise ValueError('T10 smaller weight payload')
            elif type(value) is not int or value<minimum: raise ValueError('T10 smaller payload '+key)
        if bound<max(observed): raise ValueError('T10 bound below maximum '+kind)
        totals.append(count*bound)
    if phase['upper_s']<math.fsum(totals): raise ValueError('T10 phase sum understated')


def telemetry_admission(env,stage,out):
    if 'C10Y_TELEMETRY' not in env: return {'telemetry':False,'telemetry_inertness':None}
    if env['C10Y_TELEMETRY']!='1': raise Halt('TELEMETRY-SWITCH')
    out=Path(out)
    if out.name=='c10y_directdw' or stage=='calibration': raise Halt('FIRST-ATTEMPT-TELEMETRY')
    value=env.get('C10Y_TELEMETRY_INERTNESS')
    if not value: raise Halt('TELEMETRY-INERTNESS')
    path=Path(value);base=Path(ROOT)/'results/c10y_directdw_telemetry_inertness'
    if not path.is_absolute() or path.resolve().parent.parent!=base.resolve() or path.name!='inertness.json': raise Halt('TELEMETRY-INERTNESS-PATH')
    raw=path.read_bytes();record=strict_json(raw);validate_inertness(record)
    admission=TelemetryAdmission(telemetry=True,telemetry_inertness={'path':str(path.resolve()),'sha256':hashlib.sha256(raw).hexdigest()})
    admission.record=record
    return admission


def telemetry_mps_inertness_check(out,H):
    import torch
    context_record=freeze_contexts(H,Path(out)/'context_templates.json')
    audit=overlap_audit(H._C10Y_CONTEXTS,H)
    write_json(Path(out)/'overlap_audit.json',audit)
    if not audit['clean']: raise Halt('INVALID-LEAKAGE',audit)
    hp=H.hp;weights=band_hashes(H,hp);started=utc();oldstate=H._ARM_STATE
    H._ARM_STATE={'requests':[H.req(H.CANON,s,H.ARMS[A7][s]) for s in H.FICTION]}
    requests=H._ARM_STATE['requests'];batches=[request_batch(H,r,H.get_context_templates(H.model,H.tok)) for r in requests[:6]]
    lens_seconds=[];answer_seconds=[]
    def gathered():
        tokens,targets,kl,_=packed_batches(H,batches)
        with torch.no_grad(): logits=H.model(input_ids=tokens['input_ids'],attention_mask=tokens['attention_mask'],use_cache=False).logits
        # Gather before CPU transfer; compare the science batch's target and KL logits bitwise.
        return torch.cat([logits[row,pos].reshape(-1,logits.shape[-1]) for row,pos,_,_,_ in targets]).detach().cpu().float()
    def pass_(telemetry=None):
        captured=[]
        def sink(prompt,ids,gen):
            captured.append((list(gen),gen==list(ids),gen[0]==ids[0]))
            if telemetry:
                begin=TELEMETRY_CLOCK();telemetry.sink(H,'pristine','readout',prompt,ids,gen);answer_seconds.append(TELEMETRY_CLOCK()-begin)
        scorer=make_scorer(H,sink,reference=telemetry is None)
        for s in H.FICTION:
            for p in [H.CANON]+H.PTEST: scorer(p.format(s),H.tgt_ids(H.ARMS[A7][s]))
        if telemetry:
            begin=TELEMETRY_CLOCK();telemetry.logit_lens(H,hp,'merged');lens_seconds.append(TELEMETRY_CLOCK()-begin)
        return captured,gathered()
    try:
        # Exactly one warm-up of scorer and science shape.
        make_scorer(H,lambda *args:None)(H.CANON.format(H.FICTION[0]),H.tgt_ids(H.ARMS[A7][H.FICTION[0]]));gathered()
        p1=pass_();telemetry=Telemetry(out,'s1','inertness')
        begin=TELEMETRY_CLOCK();telemetry.logit_lens(H,hp,'pristine');lens_seconds.append(TELEMETRY_CLOCK()-begin)
        tested=pass_(telemetry);p2=pass_()
        control=p1[0]==p2[0] and torch.equal(p1[1],p2[1]);equal=p1[0]==tested[0] and torch.equal(p1[1],tested[1])
        path=Path(out)/'telemetry/telemetry_s1.jsonl'
        lines=[json.loads(s) for s in path.read_text().splitlines()] if path.exists() else []
        complete=telemetry.enabled and sum(s['kind']=='answer' for s in lines)==96 and sum(s['kind']=='logit_lens' and len(s['items'])==24 for s in lines)==2
        answers=[s for s in lines if s['kind']=='answer']
        keys=[(s,t) for s in H.FICTION for t in [H.CANON]+H.PTEST]
        serialized_equal=(len(answers)==len(keys) and all(
            (line.get('subj'),line.get('template'))==key and line.get('arm')==A7 and
            line.get('target_ids')==H.tgt_ids(H.ARMS[A7][key[0]]) and
            line.get('generated_ids')==reference[0] and line.get('full') is reference[1] and line.get('first') is reference[2]
            for line,key,reference in zip(answers,keys,p1[0])))
        equal=equal and serialized_equal
        unchanged=weights==band_hashes(H,hp)
        verdict='INVALID' if not unchanged or not complete else 'NONDETERMINISTIC-BASELINE' if not control else 'INERT' if equal else 'NOT-INERT'
        # Full-width timings are a separate post-P2 section; they never affect the verdict.
        snapshots=H.snap_layers(hp)
        shape=list(next(iter(snapshots.values())).shape)
        payload={'requests':24,'frames':6,'target_positions':max(len(H.tgt_ids(r['target_new']['str'].lstrip())) for r in requests),
                 'layers':len(hp.layers),'weight_shape':shape,'vocabulary':H.model.config.vocab_size}
        timings={}
        for kind in ('phase','opt_step','target_probs','write_norms'):
            times=[]
            for repetition in range(3):
                begin=TELEMETRY_CLOCK()
                if kind=='phase': telemetry.phase('accumulation_reference_anchor_start',recipe='B-e2e-ENV',arm=A7,mode='apply_stored')
                elif kind=='opt_step':
                    norms={str(l):gram_norm(torch.ones(t.shape[0],24,device=H.DEV),torch.ones(24,t.shape[1],device=H.DEV)) for l,t in snapshots.items()}
                    telemetry.opt_step(100,{'L_edit':1.,'KL_raw':1.,'KL_weighted':.0625,'L':1.0625,'L_z':1.},1024.,5,norms)
                elif kind=='target_probs':
                    logs=cpu64(torch.zeros(24,6,payload['target_positions'],device=H.DEV));probabilities=logs.exp()
                    telemetry.target_probs(probabilities=[{'request':i,'frame':j,'position':k,'p':float(probabilities[i,j,k])} for i,r in enumerate(requests) for j in range(6) for k in range(len(H.tgt_ids(r['target_new']['str'].lstrip())))],f_ij=logs.mean(-1).exp().tolist(),r_ij=logs.mean(-1).tolist())
                else:
                    norms={str(l):{'actual':norm(t),'planned':gram_norm(torch.ones(t.shape[0],24,device=H.DEV),torch.ones(24,t.shape[1],device=H.DEV)),'ratio_to_A':1.} for l,t in snapshots.items()}
                    echo={str(l):{'delta_norm':norm(t),'weight_norm_before':norm(t),'relative_delta_norm':1.} for l,t in snapshots.items()}
                    telemetry.write_norms(norms,'A',A7,harness_fp32=echo)
                times.append(TELEMETRY_CLOCK()-begin)
            timings[kind]={'seconds':times,'repetitions':3,'payload':payload.copy()}
        telemetry.close()
        return {'verdict':verdict,'control_equal':control,'telemetry_equal':equal,'generated_equal':p1[0]==tested[0],
            'context_templates':context_record,'overlap_audit':{'path':str((Path(out)/'overlap_audit.json').resolve()),'sha256':sha(Path(out)/'overlap_audit.json')},
            'telemetry_complete':complete,'serialized_answers_equal':serialized_equal,'weights_unchanged':unchanged,'answer_calls':96,'lens_forwards':48,
                'lens_forward_seconds':lens_seconds,'answer_line_seconds':answer_seconds,'timings':timings,'lens_payload':payload.copy(),'answer_payload':payload.copy(),
                'started_at':started,'finished_at':utc(),'scope':'Pristine outputs only; edited MPS outputs, optimisation loop and resource inertness UNVERIFIED.'}
    finally: H._ARM_STATE=oldstate


def calibration_identity():
    info=preflight()
    return {'sources':{k:info['sources'][p] for k,p in SOURCE_PATHS.items()},
            'fingerprint':info['fingerprint'],'env':info['env'],'device':'mps','prereg_sha256':PREREG_SHA}


def calibration_forecast(path,bounds):
    try:
        path=Path(path).resolve();timings=_calibration_timings(strict_load(path))
        if path.name!='calibration.json' or not isinstance(bounds,list) or any(not isinstance(b,dict) for b in bounds):
            raise ValueError('invalid calibration path/bounds')
        phases=[]
        for bound in bounds:
            keys=('name','workload','repetitions','scaling_assumption','justification','upper_s','measured','timing_names')
            phase={k:copy.deepcopy(bound[k]) for k in keys if k in bound}
            phase.setdefault('measured',True)
            if type(phase['measured']) is not bool: raise ValueError('invalid measured support flag')
            phase.update(artifact=str(path),sha256=sha(path))
            if phase['measured']:
                phase['measurements']=_calibration_phase(timings,phase)[0]
            else:
                phase.pop('timing_names',None)
            phases.append(phase)
        forecast={'stage':1,'status':'READY','phases':phases}
        gate=budget_gate(forecast,7200.)
        forecast.update(gate)
        return forecast
    except (ValueError,OSError,KeyError,TypeError,OverflowError) as error:
        return {'stage':1,'status':'UNVERIFIED','launched':False,'phases':[],'reasons':[str(error)]}


def owned_launch(out,stage):
    tag='calib' if stage=='calibration' else 's1' if stage==1 else 'p%d'%(stage-1)
    path=Path(out)/'logs'/('launch_'+tag+'.json')
    token=os.environ.get('C10Y_WORKER_TOKEN')
    if not token or not path.is_file(): return False
    record=strict_load(path)
    return record.get('token')==token and record.get('stage')==stage and record.get('out')==str(Path(out).resolve())


def output_path(out,stage):
    out=Path(out)
    if not out.is_absolute() or out.resolve().parent!=(Path(ROOT)/'results').resolve(): raise Halt('OUTPUT-PATH')
    name=out.name
    if stage=='calibration':
        if not re.fullmatch(r'c10y_directdw_calib[1-9][0-9]*',name) or (out.exists() and not owned_launch(out,stage)): raise Halt('CALIBRATION-OUTPUT')
    elif name=='c10y_directdw':
        own='screen.json' if stage==1 else 'pass_p%d.json'%(stage-1)
        if (stage==1 and out.exists() and not owned_launch(out,stage)) or (out/own).exists(): raise Halt('EXISTING-ARTIFACT')
    elif not re.fullmatch(r'c10y_directdw_s%d_rerun[1-9][0-9]*'%stage,name) or (out.exists() and not owned_launch(out,stage)): raise Halt('RERUN-OUTPUT')
    return out.resolve()


def diagnostic_path(path):
    if path is None: raise Halt('DIAGNOSTIC-REQUIRED')
    path=Path(path)
    if not path.is_absolute() or path.resolve().parent!=(Path(ROOT)/'architecture_profile').resolve() or path.exists(): raise Halt('DIAGNOSTIC-PATH')
    return path


def save_tensors(path,tensors):
    import torch
    path=Path(path)
    if path.exists(): raise Halt('EXISTING-ARTIFACT',str(path))
    with path.open('xb') as f: torch.save(tensors,f);f.flush();os.fsync(f.fileno())
    return sha(path)


def persist_prefix(out,prefix,tag):
    paths={'contexts':'context_templates_'+tag+'.json' if tag=='calib' else 'context_templates.json',
           'overlap':'overlap_audit_'+tag+'.json' if tag=='calib' else 'overlap_audit.json',
           'targets':'targets_'+tag+'.pt','ledger':'ledger_'+tag+'.json' if tag=='calib' else 'ledger.json',
           'law5':'law5_'+tag+'.json','step0':'step0_'+tag+'.json'}
    for key in ('contexts','overlap','ledger','law5','step0'):
        value=prefix.get({'overlap':'overlap_audit'}.get(key,key),{})
        p=out/paths[key]
        if not p.exists(): write_json(p,value)
    target=out/paths['targets']
    payload={'targets':prefix.get('targets',{})}
    if 'deployed_updates' in prefix: payload['actual_updates']=prefix['deployed_updates']
    if not target.exists(): save_tensors(target,payload)
    return {name:sha(out/name) for name in paths.values()}


def reproduction_record(first,second,previous_path,updates,targets):
    import torch
    directory=Path(previous_path).resolve();directory=directory.parent if directory.is_file() else directory
    path=directory/'targets_p1.pt'
    if first['manifest']['artifacts'].get(path.name)!=sha(path): raise Halt('REPRO-ARTIFACT-IDENTITY')
    previous=torch.load(path,map_location='cpu',weights_only=True)
    original=previous['actual_updates'];rows={}
    recipes=set(original)|set(updates)
    for recipe in recipes:
        name=recipe
        lhs=original.get(name,original.get('B-e2e') if name in ('B-e2e-NM','B-e2e-ENV') else None)
        rhs=updates.get(name,updates.get('B-e2e') if name in ('B-e2e-NM','B-e2e-ENV') else None)
        if lhs is None or rhs is None: continue
        rows[recipe]={'arms':{arm:{'layers':[{'layer':l,'cosine':cosine(lhs[arm][l],rhs[arm][l]),
            'distance':relative_distance(lhs[arm][l],rhs[arm][l]),'norm_p1':norm(lhs[arm][l]),'norm_p2':norm(rhs[arm][l])}
            for l in sorted(lhs[arm])]} for arm in ARMS}}
    zcos=[{'subject':s,'target':v,'cosine':cosine(previous['targets'][(s,v)],z)} for (s,v),z in targets.items()]
    return {'H_in':first['manifest']['H_in'],'reduction_dtype':'float64','reduction_device':'cpu',
            'baseline':rows.pop('A'),'recipes':rows,'per_fact_z_cosine':zcos,
            'process1':str(directory),'process2_H_in':second['manifest']['H_in']}


def rerun_provenance(out,stage,replacement,predecessor):
    if '_rerun' not in Path(out).name: return None
    if not isinstance(replacement,dict) or not replacement.get('cause') or not isinstance(replacement.get('replaces'),str): raise Halt('RERUN-PROVENANCE')
    old=Path(replacement['replaces'])
    if not old.is_absolute() or old.resolve().parent!=(Path(ROOT)/'results').resolve() or not old.is_dir() or old.resolve()==Path(out).resolve(): raise Halt('RERUN-PROVENANCE')
    result={'replaces':str(old.resolve()),'halt_or_audit_cause':replacement['cause']}
    if stage==3:
        pair=Path(predecessor).resolve();pair=pair.parent if pair.is_file() else pair
        result['paired_stage2']=str(pair)
    return result


def calibrate(out,H,go=None,spend=None,diagnostic=None):
    import torch
    selftest_root(ROOT);refuse_schedule_halt(ROOT)
    if any(k in os.environ for k in ('C10Y_TELEMETRY','C10Y_TELEMETRY_INERTNESS')): raise Halt('CALIBRATION-TELEMETRY')
    cap=launch_documents('calibration',go,spend,None);out=output_path(out,'calibration');diagnostic=diagnostic_path(diagnostic)
    identity=calibration_identity();inputs=input_identity(H,H.hp);started=utc();out.mkdir(parents=True,exist_ok=owned_launch(out,'calibration'));(out/'logs').mkdir(exist_ok=True)
    budget=Budget(float(os.environ.get('C10Y_STAGE_START',STAGE_CLOCK())),cap,'calibration');prefix={};outcome='COMPLETE';torch.manual_seed(0);context_record=context_evidence(out/'context_templates_calib.json')
    try:
        context_started=STAGE_CLOCK()
        context_record=freeze_contexts(H,out/'context_templates_calib.json')
        H._C10Y_CONTEXT_INSTALL_SECONDS=STAGE_CLOCK()-context_started
        prefix=instrument_prefix(H,out,budget,calibration=True,telemetry=None)
        if calibration_identity()!=identity or input_identity(H,H.hp)!=inputs: raise Halt('SOURCE-OR-INPUT-DRIFT')
    except Halt as e:
        outcome=e.code
        context_record=context_evidence(out/'context_templates_calib.json')
        if e.code in ('LAW#3','LAW3'): schedule_halt(ROOT,e.code,e.detail,context_record)
        write_json(diagnostic,{'process':'calibration','out':str(out),'code':e.code,'detail':e.detail,'at':utc(),'context_templates':context_record,'pinned_engine_sha256':PINNED_ENGINE_SHA})
    except Exception as e:
        outcome='INSTRUMENT-ERROR'
        context_record=context_evidence(out/'context_templates_calib.json')
        write_json(diagnostic,{'process':'calibration','out':str(out),'code':outcome,'exception':type(e).__name__,'detail':str(e),'at':utc(),'context_templates':context_record,'pinned_engine_sha256':PINNED_ENGINE_SHA})
    artifacts=persist_prefix(out,prefix,'calib')
    record={**identity,'schema':'c10y_directdw_calibration/v1','outcome':outcome,'device':str(H.DEV),
            'timings':calibration_timing_tags(prefix.get('timings',[])),'checks':prefix.get('checks',{}),'memory':getattr(H,'_C10Y_MEMORY',{}),
            'T_cal':prefix.get('T_cal'),'template_token_lengths':prefix.get('template_token_lengths',[]),'context_templates':context_record,
            'input_hashes_start':inputs,'input_hashes_end':inputs.copy(),'artifacts':artifacts,'started_at':started,'finished_at':utc()}
    write_json(out/'run.json',{'stage':'calibration','status':outcome,'telemetry':False,'telemetry_inertness':None,
                             'go':go,'spend':spend,'cap_s':cap,'started_at':started,'finished_at':utc(),'context_templates':context_record})
    if owned_launch(out,'calibration'):
        record['last_record_clock']=STAGE_CLOCK()
        write_json(out/'calibration_worker.json',record)
    else: write_json(out/'calibration.json',record)
    return record


def input_identity(H,hp):
    if str(H.DEV)=='cpu' and os.environ.get('C10Y_SELFTEST'):
        model={n:tensor_sha(t) for n,t in H.model.named_parameters()}
        return {'covariance':digest({str(l):'CPU-FIXTURE' for l in hp.layers}),'model':digest(model),
                'tokenizer':digest({'type':type(H.tok).__name__,'padding_side':H.tok.padding_side}),'hparams':sha(Path(ROOT)/SOURCE_PATHS['hparams'])}
    caches=H.cov_cache_sha256(hp)
    model_base=Path(ROOT)/'hf_cache/hub'/('models--'+MODEL_ID.replace('/','--'))/'snapshots'/MODEL_REV
    model_files={p.name:sha(p) for p in sorted(model_base.glob('*.safetensors'))}
    tokenizer_files={p.name:sha(p) for p in sorted(model_base.iterdir()) if 'token' in p.name or p.name in ('vocab.json','merges.txt','config.json')}
    if not model_files or not tokenizer_files: raise Halt('MODEL-ARTIFACT-IDENTITY')
    return {'covariance':digest(caches),'model':digest(model_files),'tokenizer':digest(tokenizer_files),'hparams':sha(Path(ROOT)/SOURCE_PATHS['hparams'])}


def record_manifest(H,hp,contexts,info,artifacts,inputs):
    sources={k:info['sources'][p] for k,p in SOURCE_PATHS.items()}
    parts={'requests':{arm:[{'subject':s,'target':' '+v} for s,v in V.items()] for arm,V in H.ARMS.items()},
           'model_id':MODEL_ID,'model_rev':MODEL_REV,'base_artifact_sha256':inputs['model'],'tokenizer_artifacts_sha256':inputs['tokenizer'],
           'tokenizer_settings':{'padding_side':H.tok.padding_side,'pad_token_id':H.tok.pad_token_id},
           'covariance_sha256':{str(l):inputs['covariance'] for l in hp.layers},'hparams_sha256':inputs['hparams'],
           'context_templates_sha256':contexts['sha256'],'prereg_sha256':PREREG_SHA,'source_paths':SOURCE_PATHS,
           'source_sha256':sources,'stimuli':{'CANON':H.CANON,'PTEST':H.PTEST,'FICTION':H.FICTION,'ARMS':H.ARMS},
           'objective':{'KL_coefficient':0.0625,'routing':True,'parameter_dtype':'float32','model_dtype':'float16'},
           'optimiser':{'name':'Adam','betas':[0.9,0.999],'eps':1e-8,'weight_decay':0,'lr_multiplier':0.02,'T_max':100,'loss_scale':1024,'micro_batches':[6,6,6,6]},
           'stage_table':{'1':'A7-screen','2':'process1','3':'process2'},'seed':0,'device':str(H.DEV),
           'library_versions':info['env']|{'backend':str(H.DEV)}}
    return {'prereg_sha256':PREREG_SHA,'H_in':digest(parts),'parts':parts,'sources_start':sources,'sources_end':sources.copy(),
            'input_hashes_start':inputs|{'contexts':contexts['sha256']},'input_hashes_end':inputs|{'contexts':contexts['sha256']},
            'artifacts':artifacts,'context_templates':contexts}


def run(out,H,stage=1,go=None,forecast=None,spend=None,contexts=None,context_sha=None,predecessor=None,diagnostic=None,replacement=None,admission=None):
    import torch
    selftest_root(ROOT);refuse_schedule_halt(ROOT)
    reader=importlib.import_module('c10y_directdw_read')
    if str(H.DEV)!='mps' and not (str(H.DEV)=='cpu' and os.environ.get('C10Y_SELFTEST')): raise Halt('DEVICE')
    prior=reader.load(predecessor) if predecessor else None
    if stage>1 and prior is not None and prior.get('stage')!=stage-1: raise Halt('PREDECESSOR-STAGE')
    eligibility=reader.classify(prior) if prior else None
    if admission is None: admission=telemetry_admission(os.environ,stage,out)
    cap=launch_documents(stage,go,spend,eligibility)
    if not isinstance(forecast,dict) or type(forecast.get('stage')) is not int or forecast['stage']!=stage: raise Halt('FORECAST-STAGE')
    gate=budget_gate(forecast,cap,admission)
    if gate['status']!='READY': raise Halt(gate['status'],gate)
    if stage==3 and bool(prior['run']['telemetry'])!=admission['telemetry']: raise Halt('TELEMETRY-PAIR')
    info=preflight();out=output_path(out,stage);provenance=rerun_provenance(out,stage,replacement,predecessor);diagnostic=diagnostic_path(diagnostic)
    hp=H.hp if hasattr(H,'hp') else H.MEMITHyperParams.from_json(str(Path(ROOT)/SOURCE_PATHS['hparams']));H.hp=hp
    inputs=input_identity(H,hp);torch.manual_seed(0);out.mkdir(parents=True,exist_ok=True)
    budget=Budget(float(os.environ.get('C10Y_STAGE_START',STAGE_CLOCK())),cap,stage);tag='s1' if stage==1 else 'p%d'%(stage-1)
    budget.configure(forecast,getattr(H,'_C10Y_STARTUP_TIMINGS',()))
    telemetry=telemetry_factory(out,tag,utc(),admission['telemetry']);prefix={};context_record=context_evidence(contexts or out/'context_templates.json')
    had_telemetry=hasattr(H,'_C10Y_TELEMETRY');old_telemetry=getattr(H,'_C10Y_TELEMETRY',None);H._C10Y_TELEMETRY=telemetry
    record={'schema':'c10y_directdw/v1','stage':stage,'run':{'stage':stage,'status':'COMPLETED','code':None,'launched':True,
            'write_complete':False,'readout_complete':False,**admission,'cap_s':cap,'projected_s':gate['projected_s']},'recipes':{}}
    try:
        context_started=STAGE_CLOCK()
        if stage==1: context_record=freeze_contexts(H,out/'context_templates.json')
        if stage>1:
            if contexts is None or context_sha is None: raise Halt('CONTEXT-SOURCE-REQUIRED')
            source=stage_context_source(contexts,context_sha)
            context_record=freeze_contexts(H,source,expected=context_sha)
        H._C10Y_CONTEXT_INSTALL_SECONDS=STAGE_CLOCK()-context_started
        record['run']['context_templates']=context_record
        if telemetry: telemetry.phase('stage_start')
        prefix=instrument_prefix(H,out,budget,calibration=False,telemetry=telemetry)
        record['recipes']['A']=prefix['baseline']
        writer=prefix['writer'];original=H.my_edit;H.my_edit=writer
        prefix['runtime'].update(out=out,tag=tag)
        previous_globals=(H.Z_OVERRIDE,H.Z_OVERRIDE_HITS,H._LAW5_DEFAULT_CTX)
        context_globals=H.get_context_templates.__globals__;had_cache='CONTEXT_TEMPLATES_CACHE' in context_globals;old_cache=context_globals.get('CONTEXT_TEMPLATES_CACHE')
        H.Z_OVERRIDE=prefix['targets'];H.Z_OVERRIDE_HITS=0;H._LAW5_DEFAULT_CTX=False
        context_globals['CONTEXT_TEMPLATES_CACHE']=copy.deepcopy(prefix['contexts'])
        old_runtime=getattr(H,'_C10Y_READOUT_STATE',None);H._C10Y_READOUT_STATE=prefix['runtime']
        try:
            for name,mode in (('B-e2e','e2e'),)+(() if stage==1 else (('B-z','anchor'),)):
                writer.mode=mode
                record['recipes'][name]=scored_recipe(H,name,H.HP_BASE,stage,telemetry)
            if stage>1:
                reference=prefix['actual_A'];candidate=prefix['actual_B']['B-e2e']
                for control in ('NM','ENV'):
                    scales={arm:size_scales(reference[arm],candidate[arm])[control] for arm in ARMS}
                    if not any(s is not None for s in scales.values()): continue
                    writer.mode='apply_stored';writer.stored=candidate;writer.scale={arm:s if s is not None else 1. for arm,s in scales.items()}
                    record['recipes']['B-e2e-'+control]=scored_recipe(H,'B-e2e-'+control,H.HP_BASE,stage,telemetry)
        finally:
            H.my_edit=original
            H.Z_OVERRIDE,H.Z_OVERRIDE_HITS,H._LAW5_DEFAULT_CTX=previous_globals
            if had_cache: context_globals['CONTEXT_TEMPLATES_CACHE']=old_cache
            else: context_globals.pop('CONTEXT_TEMPLATES_CACHE',None)
            if old_runtime is None: del H._C10Y_READOUT_STATE
            else: H._C10Y_READOUT_STATE=old_runtime
        record['run'].update(write_complete=True,readout_complete=True)
        if not (out/('write_complete_'+tag+'.json')).exists(): write_json(out/('write_complete_'+tag+'.json'),{'stage':stage,'at':utc()})
        if input_identity(H,hp)!=inputs or preflight()!=info: raise Halt('SOURCE-OR-INPUT-DRIFT')
        prefix['deployed_updates']={'A':prefix['actual_A'],**prefix['actual_B']}
    except Halt as e:
        context_record=context_evidence(contexts or out/'context_templates.json');record['run']['context_templates']=context_record
        record['run'].update(status=e.code if e.code in ('HALTED-BUDGET','INCOMPLETE-BUDGET','INVALID-LEAKAGE','INVALID-TRAIN-DEPLOY-GAP') else 'HALTED',code=e.code,write_complete=budget.write_complete)
        if e.code in ('LAW#3','LAW3'): schedule_halt(ROOT,e.code,e.detail,context_record)
        if telemetry: telemetry.phase('halt',code=e.code)
        write_json(diagnostic,{'stage':stage,'out':str(out),'code':e.code,'detail':e.detail,'at':utc(),'context_templates':context_record,'pinned_engine_sha256':PINNED_ENGINE_SHA})
    except Exception as e:
        context_record=context_evidence(contexts or out/'context_templates.json');record['run']['context_templates']=context_record
        record['run'].update(status='HALTED',code='INSTRUMENT-ERROR')
        write_json(diagnostic,{'stage':stage,'out':str(out),'code':'INSTRUMENT-ERROR','exception':type(e).__name__,'detail':str(e),'at':utc(),'context_templates':context_record,'pinned_engine_sha256':PINNED_ENGINE_SHA})
    finally:
        if telemetry: telemetry.phase('stage_end');telemetry.close()
        if had_telemetry: H._C10Y_TELEMETRY=old_telemetry
        else: del H._C10Y_TELEMETRY
    # PROVISIONAL §2.12/T12 ownership: stage1 common artifacts immutable;
    # later pass records contain their own manifest/run/ledger/overlap identity.
    artifacts=persist_prefix(out,prefix,tag)
    overlay='targets_'+tag+'.pt'
    for name,recipe in record['recipes'].items():
        for arm,data in recipe['arms'].items():
            if data.get('status')!='COMPLETED': continue
            hout=data['H_out']
            hout.update(tensor_certificate_sha256=digest(hout['tensors']),overlay_sha256=artifacts[overlay],
                        overlay_artifact=overlay,overlay_member=['actual_updates',name,arm])
            if 'stored_control' in data:
                stored=data['stored_control'];stored['source_sha256']=artifacts[overlay]
                if stored.get('scale1_fully_evaluated_source') is not None: stored['scale1_fully_evaluated_source']['source_sha256']=artifacts[overlay]
    context_path=Path(contexts) if contexts else out/'context_templates.json'
    context_record={'path':str(context_path.resolve()),'sha256':sha(context_path)} if context_path.exists() else {'path':str(context_path.resolve()),'sha256':'0'*64}
    record['manifest']=record_manifest(H,hp,context_record,info,artifacts,inputs)
    if provenance is not None: record['manifest']['rerun']=provenance
    if stage==3 and prior is not None:
        record['manifest']['paired_stage2']=str(Path(predecessor).resolve().parent if Path(predecessor).is_file() else Path(predecessor).resolve())
    record['instrument']={'fingerprint':info['fingerprint'],'baseline_before_candidates':bool(prefix.get('baseline_passed',False))}
    record['ledger']=prefix.get('ledger',[]);record['overlap_audit']=prefix.get('overlap_audit',{})
    if stage==1 or out.name!='c10y_directdw':
        write_json(out/'manifest.json',record['manifest']);write_json(out/'run.json',record['run'])
    own='screen.json' if stage==1 else 'pass_p%d.json'%(stage-1)
    if stage==3 and record['run']['status']=='COMPLETED':
        repro=reproduction_record(prior,record,predecessor,prefix['deployed_updates'],prefix['targets'])
        write_json(out/'repro.json',repro)
    record['reading']=reader.classify(record);write_json(out/own,record)
    return record


def supervise(argv,out,diagnostic,cap_s,stage,env=None):
    selftest_root(ROOT)
    out=Path(out);diagnostic=Path(diagnostic)
    out.mkdir(parents=True,exist_ok=True);logs=out/'logs';logs.mkdir(exist_ok=True)
    tag='calib' if stage=='calibration' else 's1' if stage==1 else 'p%d'%(stage-1)
    stage_start=STAGE_CLOCK();deadline=stage_start+cap_s;started=utc();logpath=logs/('stage_'+tag+'.log')
    if logpath.exists() or diagnostic.exists(): raise Halt('EXISTING-ARTIFACT')
    token=hashlib.sha256(os.urandom(32)).hexdigest()
    write_json(logs/('launch_'+tag+'.json'),{'stage':stage,'out':str(out.resolve()),'token':token,'cap_s':cap_s,'at':started})
    with logpath.open('x+') as log:
        proc=subprocess.Popen(argv,cwd=str(Path(ROOT).resolve()),env=dict(env or os.environ,C10Y_STAGE_START=str(stage_start),C10Y_WORKER_TOKEN=token),stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        pgid=os.getpgid(proc.pid)
        if pgid!=proc.pid or pgid==os.getpgrp(): raise Halt('SUPERVISOR-GROUP')
        timed_out=False
        while proc.poll() is None:
            left=deadline-STAGE_CLOCK()
            if left<=min(0.2,cap_s/10):
                timed_out=True;os.killpg(pgid,signal.SIGTERM)
                try: proc.wait(timeout=max(0.001,left))
                except subprocess.TimeoutExpired: os.killpg(pgid,signal.SIGKILL);proc.wait()
                break
            time.sleep(min(.02,left))
        log.flush();log.seek(0);output=log.read()
    if timed_out:
        completed=(out/('write_complete_'+tag+'.json')).exists()
        status='INCOMPLETE-BUDGET' if completed else 'HALTED-BUDGET'
        context_path=out/('context_templates_calib.json' if stage=='calibration' else 'context_templates.json')
        if stage in (2,3) and '--contexts' in argv: context_path=Path(argv[argv.index('--contexts')+1])
        context_record=context_evidence(context_path)
        write_json(diagnostic,{'stage':stage,'process':'calibration' if stage=='calibration' else 'stage','code':status,'cap_s':cap_s,'started_at':started,'finished_at':utc(),'owned_pid':proc.pid,'owned_process_group':pgid,'context_templates':context_record,'pinned_engine_sha256':PINNED_ENGINE_SHA})
        halt={'stage':stage,'status':status,'code':'supervisor','launched':True,'write_complete':completed,'readout_complete':False,'telemetry':False,'telemetry_inertness':None,'context_templates':context_record,'pinned_engine_sha256':PINNED_ENGINE_SHA}
        target=out/('supervisor_'+tag+'.json');write_json(target,halt)
    else: status='COMPLETE' if proc.returncode==0 else 'HALTED'
    if stage=='calibration':
        draft=out/'calibration_worker.json'
        record=strict_load(draft) if draft.is_file() else {'schema':'c10y_directdw_calibration/v1','timings':[]}
        last=record.pop('last_record_clock',None)
        if last is not None:
            record['timings'].append({'name':'shutdown','seconds':STAGE_CLOCK()-last,'repetition':1,'workload':{'arms':[],'requests':0,'scored_prompts':0,'micro_batches':0,'accepted_steps':0,'retries':0},'synchronised':True,'status':'COMPLETED' if status=='COMPLETE' else 'FAILED','measurement':'supervisor last record write to worker exit'})
        record.update(finished_at=utc())
        if status!='COMPLETE': record['outcome']=status
        record['context_templates']=context_evidence(out/'context_templates_calib.json')
        write_json(out/'calibration.json',record)
    return {'status':status,'output':output,'pid':proc.pid,'process_group':pgid,'returncode':proc.returncode}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=('1','2','3','calibration'),required=True)
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--halt-diagnostic',type=Path,required=True)
    parser.add_argument('--go',type=Path,required=True);parser.add_argument('--spend',type=Path)
    parser.add_argument('--forecast',type=Path);parser.add_argument('--contexts',type=Path);parser.add_argument('--context-sha')
    parser.add_argument('--predecessor',type=Path);parser.add_argument('--authorization',type=Path)
    parser.add_argument('--replacement',type=Path)
    parser.add_argument('--budget-gate',action='store_true');parser.add_argument('--worker',action='store_true')
    args=parser.parse_args(argv);stage='calibration' if args.stage=='calibration' else int(args.stage)
    try:
        selftest_root(ROOT);refuse_schedule_halt(ROOT)
        if stage=='calibration' and any(k in os.environ for k in ('C10Y_TELEMETRY','C10Y_TELEMETRY_INERTNESS')): raise Halt('CALIBRATION-TELEMETRY')
        preflight()
        reader=importlib.import_module('c10y_directdw_read')
        prior=reader.load(args.predecessor) if args.predecessor else None
        if stage in (2,3) and prior is not None and prior.get('stage')!=stage-1: raise Halt('PREDECESSOR-STAGE')
        cap=launch_documents(stage,strict_load(args.go),strict_load(args.spend) if args.spend else None,reader.classify(prior) if prior else None)
        admission=telemetry_admission(os.environ,stage,args.out)
        if stage==3 and bool(prior['run']['telemetry'])!=admission['telemetry']: raise Halt('TELEMETRY-PAIR')
        if stage!='calibration':
            forecast=strict_load(args.forecast) if args.forecast else {}
            if type(forecast.get('stage')) is not int or forecast['stage']!=stage: raise Halt('FORECAST-STAGE')
            gate=budget_gate(forecast,cap,admission)
            print(json.dumps(gate,allow_nan=False,sort_keys=True))
            if gate['status']!='READY': return 2
            if args.budget_gate: return 0
        else:
            if args.authorization is None or not args.authorization.is_absolute() or not args.authorization.is_file() or not args.authorization.read_text().strip(): raise Halt('CALIBRATION-AUTHORIZATION')
        diagnostic_path(args.halt_diagnostic)
        if args.worker and not owned_launch(args.out,stage): raise Halt('SUPERVISOR-REQUIRED')
        if not args.worker:
            output_path(args.out,stage)
            command=[sys.executable,'-B',str(Path(__file__).resolve()),*list(argv or sys.argv[1:]),'--worker']
            result=supervise(command,args.out,args.halt_diagnostic,cap,stage,env=dict(os.environ,LLMDB_ROOT=str(Path(ROOT).resolve())))
            return 0 if result['status']=='COMPLETE' else 2
        if os.environ.get('C10Y_SELFTEST'): raise Halt('SELFTEST-REAL-WORKER')
        import torch
        torch.mps.synchronize();unit_start=STAGE_CLOCK();preflight();torch.mps.synchronize()
        startup=[{'name':'preflight','seconds':STAGE_CLOCK()-unit_start,'repetition':1,'workload':{'arms':[],'requests':0},'synchronised':True}]
        os.environ['LLMDB_ROOT']=str(Path(ROOT).resolve());os.environ['HP_BASE']=str(Path(ROOT)/SOURCE_PATHS['hparams'])
        os.environ['MODEL_ID']=MODEL_ID;os.environ['MODEL_REV']=MODEL_REV
        torch.mps.synchronize();unit_start=STAGE_CLOCK()
        H=importlib.import_module('c10e_bandknob')
        torch.mps.synchronize()
        startup.append({'name':'load','seconds':STAGE_CLOCK()-unit_start,'repetition':1,'workload':{'model':MODEL_ID,'model_rev':MODEL_REV,'tokenizer':True},'synchronised':True})
        if str(H.DEV)!='mps': raise Halt('DEVICE')
        H.hp=H.MEMITHyperParams.from_json(os.environ['HP_BASE'])
        H.find_fact_lookup_idx=H.compute_z.__globals__['find_fact_lookup_idx']
        H._C10Y_STARTUP_TIMINGS=startup
        if stage=='calibration':
            record=calibrate(args.out,H,go=strict_load(args.go),spend=strict_load(args.spend),diagnostic=args.halt_diagnostic)
            return 0 if record['outcome']=='COMPLETE' else 2
        record=run(args.out,H,stage=stage,go=strict_load(args.go),spend=strict_load(args.spend) if args.spend else None,
                   forecast=strict_load(args.forecast),contexts=args.contexts,context_sha=args.context_sha,predecessor=args.predecessor,diagnostic=args.halt_diagnostic,replacement=strict_load(args.replacement) if args.replacement else None,admission=admission)
        return 0 if record['run']['status']=='COMPLETED' else 2
    except (Halt,ValueError,OSError,KeyError) as e:
        print(str(e),file=sys.stderr);return 2
# Fragment for c10y_directdw_arms.py. No module import runs a model or tensor.
# Seams: c10e:181-221,358-400,403-509; compute_z:41-73,90-99,149-153.
FRAME_SUBJECTS = ["Vorbanth", "Quillexa", "Tremnok", "Oskavel", "Blynthar", "Durmquist"]


def frame_subjects_ast_check():
    tree=ast.parse((Path(ROOT)/'experiments/track_c/c10p_twopass_arms.py').read_text())
    node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FRAME_SUBJECTS' for t in n.targets))
    return ast.literal_eval(node.value)==FRAME_SUBJECTS


def _unit(H,timings,name,workload,action,repetition=1,budget=None):
    if budget is not None: budget.project(0.,False)
    sample_memory(H,name);sync(H);started=STAGE_CLOCK();status='COMPLETED'
    telemetry=getattr(H,'_C10Y_TELEMETRY',None)
    if telemetry is not None: telemetry.phase(name+'_start')
    try: return action()
    except BaseException:
        status='FAILED';raise
    finally:
        if telemetry is not None: telemetry.phase(name+'_end')
        sync(H);elapsed=STAGE_CLOCK()-started;sample_memory(H,name)
        timings.append({'name':name,'seconds':elapsed,'repetition':repetition,
                        'workload':copy.deepcopy(workload),'status':status,'synchronised':True})
        if budget is not None:
            phase='contexts_targets' if name in ('contexts_overlap','target_solve') else 'baseline' if name.startswith('baseline_') or name=='law3' else 'projector_capture' if name.startswith('candidate_') else 'proofs'
            budget.consume(phase,elapsed)


def _workload(arm=None,requests=0,scored=0,micro_batches=0,accepted_steps=0,retries=0):
    return {'arms':[] if arm is None else [arm],'requests':requests,'scored_prompts':scored,
            'micro_batches':micro_batches,'accepted_steps':accepted_steps,'retries':retries}


def calibration_timing_tags(timings):
    result=[]
    for source in timings:
        row=copy.deepcopy(source);workload=_workload();workload.update(row.get('workload',{}))
        arm=row.get('arm')
        if arm is None and row['name'].startswith(('zero_step_','executed_loop_','smoke_')): arm=A7
        if arm is not None: workload['arms']=[arm]
        row.update(workload=workload,status=row.get('status','COMPLETED'),synchronised=row.get('synchronised',True))
        result.append(row)
    return result


def _request_keys(requests):
    return [(r['subject'],r['target_new']['str']) for r in requests]


def _key_records(keys):
    return [{'subject':s,'target':v} for s,v in keys]


class _OverrideReads(dict):
    def __init__(self,values):
        super().__init__(values);self.reads=[]
    def __getitem__(self,key):
        self.reads.append(key);return super().__getitem__(key)


def _ledger_call(H,ledger,stage,recipe,arm,check,targets,declared,action,expected_hits=0):
    # Membership checks do not claim consumption: observe actual __getitem__ calls.
    previous=(H.Z_OVERRIDE,H.Z_OVERRIDE_HITS,H._LAW5_DEFAULT_CTX)
    overrides=_OverrideReads(targets);H.Z_OVERRIDE=overrides;H.Z_OVERRIDE_HITS=0;H._LAW5_DEFAULT_CTX=False
    row={'stage':stage,'recipe':recipe,'arm':arm,'check':check,'status':'RUNNING',
         'declared_overrides':_key_records(declared),'consumed_overrides':[],
         'declared_override_hits':expected_hits}
    ledger.append(row)
    try:
        value=action();seen=list(dict.fromkeys(overrides.reads))
        row.update(consumed_overrides=_key_records(seen),consumed_override_hits=H.Z_OVERRIDE_HITS,
                   access_count=len(overrides.reads))
        if set(seen)!=set(declared) or len(seen)!=len(declared) or H.Z_OVERRIDE_HITS!=expected_hits:
            raise Halt('OVERRIDE-LEDGER',row)
        row['status']='COMPLETED';return value
    except BaseException:
        row.update(status='HALTED',consumed_overrides=_key_records(list(dict.fromkeys(overrides.reads))),
                   consumed_override_hits=H.Z_OVERRIDE_HITS,access_count=len(overrides.reads));raise
    finally: H.Z_OVERRIDE,H.Z_OVERRIDE_HITS,H._LAW5_DEFAULT_CTX=previous


def _directed_distance(reference,value):
    a,b=cpu64(reference),cpu64(value);den=float(a.norm());num=float((a-b).norm())
    if den==0:
        if num==0: return 0.
        raise Halt('ZERO-REFERENCE-NORM')
    return num/den


def _actual_updates(H,hp,W0):
    merged=H.snap_layers(hp)
    return {l:(merged[l].float()-W0[l].float()).detach().cpu() for l in hp.layers}


def _js64(a,b):
    p,q=cpu64(a),cpu64(b);m=(p+q)*0.5
    def kl(x,y):
        x,y=x.clamp_min(1e-12),y.clamp_min(1e-12)
        return float((x*(x.log()-y.log())).sum())
    return 0.5*kl(p,m)+0.5*kl(q,m)


def _locpct64(post,pre,prompts):
    return 100.*sum(1.-_js64(post[p]['dist'],pre[p]['dist'])/math.log(2.) for p in prompts)/len(prompts)


def _covariances(H,hp):
    # Read only the statistics already populated by recipe A; never start a covariance job.
    if hasattr(H,'_C10Y_COVARIANCES'):
        values=H._C10Y_COVARIANCES
        if set(values)!=set(hp.layers): raise Halt('COVARIANCE-IDENTITY')
        return values
    if not hasattr(H,'get_cov'): raise Halt('MISSING-COVARIANCE-STATISTICS')
    cache=H.get_cov.__globals__.get('COV_CACHE',{})
    model_name=H.model.config._name_or_path.replace('/','_');values={}
    for l in hp.layers:
        key=(model_name,hp.rewrite_module_tmp.format(l))
        if key not in cache: raise Halt('MISSING-COVARIANCE-STATISTICS',key)
        values[l]=cache[key]
    return values


def write_geometry(H,hp,P,planned,actual,reference=None,covariances=None):
    covariances=_covariances(H,hp) if covariances is None else covariances;rows=[]
    for i,l in enumerate(hp.layers):
        sample_memory(H,'geometry');d=cpu64(actual[l]);c=cpu64(covariances[l]);dn=float(d.norm())
        p=None if planned is None or l not in planned else cpu64(planned[l])
        pn=None if p is None else float(p.norm())
        ref=None if reference is None else reference[l]
        row={'layer':l,'actual_norm':dn,'planned_norm':pn,
             'actual_null_share':null_share(d,P[i]),'planned_null_share':None if p is None else null_share(p,P[i]),
             'actual_covariance_energy':float(((d@c)*d).sum()),
             'planned_covariance_energy':None if p is None else float(((p@c)*p).sum()),
             'zero_update':dn==0,'planned_zero_update':None if p is None else pn==0,
             'cosine_to_A':None if ref is None or dn==0 or norm(ref)==0 else cosine(d,ref),
             'actual_ratio_to_A':None if ref is None or norm(ref)==0 and dn!=0 else norm_ratio(d,ref),
             'actual_ratio_to_A_denominator':None if ref is None else norm(ref),
             'actual_ratio_to_A_undefined_reason':'zero-reference-layer' if ref is not None and norm(ref)==0 and dn!=0 else None,
             'reduction_dtype':'float64','reduction_device':'cpu'}
        # fp32 is report-only. Neither value below feeds a comparison or label.
        row['report_only_fp32']={'actual_norm':float(actual[l].detach().cpu().float().norm()),
                                'planned_norm':None if p is None else float(p.float().norm())}
        rows.append(row);del d,c,p;sample_memory(H,'geometry')
    return rows


def _anchor_rows(H,hp,batches,operators=None):
    import torch
    tokens,_,_,mask=packed_batches(H,batches);box={}
    module=dict(H.model.named_modules())[hp.layer_module_tmp.format(hp.layers[-1])]
    handle=module.register_forward_hook(lambda m,args,out:box.update(value=out[0] if isinstance(out,tuple) else out))
    try:
        if operators is None: H.model.model(input_ids=tokens['input_ids'],attention_mask=tokens['attention_mask'],use_cache=False)
        else:
            with weight_hooks(H,hp,*operators,mask): H.model.model(input_ids=tokens['input_ids'],attention_mask=tokens['attention_mask'],use_cache=False)
        rows=[];offset=0
        for b in batches:
            J=len(b['rewriting_prompts'])
            rows.append(torch.stack([box['value'][offset+j,b['lookup_idxs'][j]] for j in range(J)]));offset+=J+1
        return torch.stack(rows)
    finally: handle.remove()


def _anchor_diagnostics(current,reference,delta):
    import torch
    cur,ref,d=cpu64(current),cpu64(reference),cpu64(delta)
    den=d.square().sum(-1);res=(cur-(ref+d[:,None,:])).square().sum(-1);ratios=[];terms=[]
    for i in range(len(den)):
        if float(den[i])==0:
            if bool((res[i]!=0).any()): raise Halt('INVALID-ANCHOR-NORMALISATION')
            ratios.append([0.]*res.shape[1]);terms.append(0.)
        else:
            ratios.append((res[i]/den[i]).sqrt().tolist());terms.append(float(res[i].mean()/den[i]))
    return {'L_z':sum(terms)/len(terms),'r_ij':ratios,'delta_norms':den.sqrt().tolist(),
            'residual_norms':res.sqrt().tolist()}


def _pristine_anchor(H,hp,requests,batches,targets):
    import torch
    with torch.no_grad(): reference=_anchor_rows(H,hp,batches).detach()
    delta=torch.stack([targets[k].to(reference.device)-reference[i,0] for i,k in enumerate(_request_keys(requests))])
    return reference,delta


def merged_fit(H,hp,requests,contexts,reference=None,delta=None):
    import torch
    batches=[request_batch(H,r,contexts) for r in requests];matrix=[]
    with torch.no_grad():
        for indices in microbatch_indices(len(requests),6):
            selected=[batches[i] for i in indices];tokens,targets,_,_=packed_batches(H,selected)
            state=H.model.model(input_ids=tokens['input_ids'],attention_mask=tokens['attention_mask'],use_cache=False).last_hidden_state
            rows=[[] for _ in selected]
            for row,pos,ids,i,j in targets:
                lp=cpu64(H.model.lm_head(state[row,pos])).log_softmax(-1)
                nll=-lp.gather(1,ids.detach().cpu()[:,None]).flatten().mean()
                rows[i].append(float((-nll).exp()))
            matrix.extend(rows)
        if any(len(row)!=6 for row in matrix) or len(matrix)!=24: raise Halt('FIT-MATRIX-SHAPE')
        result={'f_ij':matrix,'merged':True,'reduction_dtype':'float64','reduction_device':'cpu'}
        if reference is not None:
            current=torch.cat([_anchor_rows(H,hp,[batches[i] for i in g]).detach() for g in microbatch_indices(len(requests),6)])
            result.update(_anchor_diagnostics(current,reference,delta))
    return result


def _decode_ids(H,prompt,target_length,hp,operators=None):
    import torch
    # Private reference capture: never call the observed scorer in a parity cell (T4).
    cur=H.tok(prompt,return_tensors='pt').to(H.DEV)['input_ids'];generated=[];last=None
    for _ in range(target_length):
        if operators is None: logits=H.model(cur,use_cache=False).logits
        else:
            with weight_hooks(H,hp,*operators,None): logits=H.model(cur,use_cache=False).logits
        last=logits[0,-1].detach().cpu();nxt=int(last.argmax());generated.append(nxt)
        cur=torch.cat([cur,torch.tensor([[nxt]],device=H.DEV)],1)
    return generated,last


def train_deploy_parity(H,hp,requests,As,Bs,W0,mode,batches=None,pristine=None,anchor_reference=None,delta=None):
    import torch
    snapshot=H.snap_layers(hp);hooks=hook_snapshot(H.model);operators=(As,Bs,W0)
    contexts=H.get_context_templates(H.model,H.tok)
    batches=[request_batch(H,r,contexts) for r in requests] if batches is None else batches
    groups=microbatch_indices(len(requests),6)
    if mode=='anchor' and (anchor_reference is None or delta is None):
        restore(H,hp,W0)
        anchor_reference,delta=_pristine_anchor(H,hp,requests,batches,H.Z_OVERRIDE)
        restore(H,hp,snapshot)
    if mode=='e2e' and pristine is None:
        restore(H,hp,W0)
        with torch.no_grad(): pristine={tuple(g):edit_components(H,[batches[i] for i in g],None)['kl_log_probs'].detach() for g in groups}
        restore(H,hp,snapshot)
    def losses(ops):
        values={}
        with torch.no_grad():
            for group,weight in zip(groups,request_weights([len(g) for g in groups])):
                selected=[batches[i] for i in group]
                if mode=='anchor':
                    diagnostic=_anchor_diagnostics(_anchor_rows(H,hp,selected,ops),anchor_reference[group],delta[group])
                    part={'total':diagnostic['L_z'],'L_z':diagnostic['L_z']}
                else:
                    v=edit_components(H,selected,pristine[tuple(group)],ops)
                    part={'total':float(v['L'].detach().cpu()),'L_edit':float(v['L_edit'].detach().cpu()),
                          'KL_raw':float(v['KL_raw'].detach().cpu()),'weighted_KL':float(v['KL_weighted'].detach().cpu())}
                for k,v in part.items(): values[k]=values.get(k,0.)+weight*v
        return values
    def sequences(ops):
        result=[]
        with torch.no_grad():
            for r in requests:
                ids=H.tgt_ids(r['target_new']['str'].lstrip())
                for j,t in enumerate([H.CANON]+H.PTEST):
                    generated,logits=_decode_ids(H,t.format(r['subject']),len(ids),hp,ops)
                    result.append({'subject':r['subject'],'template_index':j,'target_ids':list(ids),
                                   'generated_ids':generated,'full':generated==list(ids),'logits':logits})
        return result
    try:
        restore(H,hp,W0);hooked_loss=losses(operators);hooked=sequences(operators)
        weights=dict(H.model.named_parameters())
        with torch.no_grad():
            for l in hp.layers: weights[H.weight_name(hp,l)].copy_(to_like(effective_weight(W0[l],As[l],Bs[l]),weights[H.weight_name(hp,l)]))
        merged_loss=losses(None);merged=sequences(None)
        ids_equal=all(a['generated_ids']==b['generated_ids'] for a,b in zip(hooked,merged))
        hits_equal=all(a['full']==b['full'] for a,b in zip(hooked,merged))
        pairs={k:[hooked_loss[k],merged_loss[k]] for k in merged_loss}
        errors={k:abs(a-b) for k,(a,b) in pairs.items()}
        tolerances={k:max(1e-4,1e-3*abs(b)) for k,(a,b) in pairs.items()}
        finite=all(math.isfinite(x) for pair in pairs.values() for x in pair)
        logit_diff=max(float((cpu64(a['logits'])-cpu64(b['logits'])).abs().max()) for a,b in zip(hooked,merged))
        rows=[{k:v for k,v in a.items() if k!='logits'}|{'merged_generated_ids':b['generated_ids'],'merged_full':b['full']} for a,b in zip(hooked,merged)]
        record={'ids_equal':ids_equal,'full_hits_equal':hits_equal,'losses':pairs,'loss_errors':errors,
                'loss_tolerances':tolerances,'max_logit_difference':logit_diff,'prompts':rows,
                'prompt_count':len(rows),'heldout_for_selection':False,'reduction_dtype':'float64','reduction_device':'cpu'}
        if len(rows)!=96 or not ids_equal or not hits_equal or not finite or any(errors[k]>tolerances[k] for k in errors):
            raise Halt('INVALID-TRAIN-DEPLOY-GAP',record)
        return record
    finally:
        restore(H,hp,snapshot)
        if hook_snapshot(H.model)!=hooks: raise Halt('HOOK-RESTORATION')


def _probe_pristine(H,hp,requests,contexts):
    import torch
    if not frame_subjects_ast_check() or set(FRAME_SUBJECTS)&set(H.FICTION): raise Halt('FRAME-SUBJECT-IDENTITY')
    frames={'CANON':H.CANON}|{'frame%d'%i:c.format(H.CANON) for i,c in enumerate(c for group in contexts for c in group)}
    if len(frames)!=7: raise Halt('FRAME-SHAPE')
    relation={'associated_with':'{} is associated with','is_a':'{} is a'}
    with torch.no_grad():
        frame_pre={k:{s:H.predict(t.format(s)) for s in FRAME_SUBJECTS} for k,t in frames.items()}
        relation_pre={k:{r['subject']:H.predict(t.format(r['subject'])) for r in requests} for k,t in relation.items()}
        anchor={}
        for k,t in {'canonical':H.CANON}|{'heldout%d'%i:p for i,p in enumerate(H.PTEST)}.items():
            anchor[k]=H.get_module_input_output_at_words(H.model,H.tok,hp.layers[-1],
                context_templates=[t for _ in requests],words=[r['subject'] for r in requests],
                module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1].T.detach().cpu()
    return {'frames':frames,'frame_pre':frame_pre,'relation_templates':relation,'relation_pre':relation_pre,'anchor_pre':anchor}


def _remaining_readout(H,hp,requests,targets,pre):
    import torch
    z=torch.stack([targets[k].detach().cpu() for k in _request_keys(requests)],1);values={};denominators={}
    for key,t in {'canonical':H.CANON}|{'heldout%d'%i:p for i,p in enumerate(H.PTEST)}.items():
        now=H.get_module_input_output_at_words(H.model,H.tok,hp.layers[-1],context_templates=[t for _ in requests],
              words=[r['subject'] for r in requests],module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1].T
        numerator=norm(cpu64(z)-cpu64(now));denominator=norm(cpu64(z)-cpu64(pre[key]));denominators[key]=denominator
        if not denominator and numerator: raise Halt('INVALID-REMAINING-NORMALISATION',key)
        # PROVISIONAL P:145: 0/0 means an already-realised unchanged zero residual, reported as 0.
        values[key]=numerator/denominator if denominator else 0.
    return {'canonical':values['canonical'],'heldout':[values['heldout%d'%i] for i in range(3)],
            'denominator_norms':denominators,'reduction_dtype':'float64','reduction_device':'cpu'}


def _stored_reference_checks(H,name,writer,runtime):
    import torch
    hp=H.hp;W0=runtime['pristine'];timings=runtime['timings'];stage=runtime['stage'];ledger=runtime['ledger']
    if name not in ('B-e2e-NM','B-e2e-ENV'): raise Halt('STORED-RECIPE')
    source_recipe=runtime.get('recipes',{}).get('B-e2e')
    if source_recipe is None: raise Halt('STORED-SOURCE-MISSING')
    runtime.setdefault('stored_control',{}).setdefault(name,{})
    snapshot=H.snap_layers(hp);registries=_all_registries(H.model)
    try:
        for arm,V in H.ARMS.items():
            if arm not in writer.stored or arm not in writer.scale: raise Halt('STORED-ARM-MISSING',arm)
            candidate=runtime['actual_B']['B-e2e'][arm];source=source_recipe['arms'][arm]
            reference_counts={k:source['metrics'][k] for k in ('canon_full_n','para_full_n','para_first_n')}
            restore(H,hp,W0)
            old_overrides=H.Z_OVERRIDE;old_counter=H.Z_OVERRIDE_HITS
            applied=_ledger_call(H,ledger,stage,name,arm,'scale1',runtime['targets'],[],
                lambda:_unit(H,timings,'stored_scale1_merge',_workload(arm,24),
                    lambda:apply_stored(H,hp,W0,writer.stored[arm],1.),budget=runtime['budget']))
            actual_weights=H.snap_layers(hp)
            expected={l:(W0[l].detach().cpu().float()+candidate[l].detach().cpu().float()).to(W0[l].dtype) for l in hp.layers}
            weights_equal=all(torch.equal(actual_weights[l].detach().cpu(),expected[l]) for l in hp.layers)
            distances={str(l):_directed_distance(candidate[l],applied[l]) for l in hp.layers}
            counts,evaluation=_unit(H,timings,'stored_scale1_evaluation',_workload(arm,24,96),lambda:_counts(H,V),budget=runtime['budget'])
            values={'floor':0.,'distance_by_layer':distances,'weights_equal':weights_equal,'counts_equal':counts==reference_counts,
                'counts':counts,'reference_counts':reference_counts,'merged_evaluation':evaluation,
                'reference_weight_hashes':{str(l):tensor_sha(w) for l,w in expected.items()},'merged_weight_hashes':band_hashes(H,hp)}
            if not weights_equal or not values['counts_equal'] or any(d!=0 for d in distances.values()): raise Halt('STORED-SCALE1-IDENTITY',values)
            restore(H,hp,W0)
            hooks={'registries_equal':_all_registries(H.model)==registries,'writer_handles_removed':_all_registries(H.model)==registries,
                'unknown_hooks_preserved':_all_registries(H.model)==registries,'pristine_restored':band_hashes(H,hp)=={str(l):tensor_sha(t) for l,t in W0.items()},
                'wrapper_restored':H.my_edit is writer,'overrides_restored':H.Z_OVERRIDE is old_overrides and H.Z_OVERRIDE_HITS==old_counter}
            # _ledger_call has already restored the observed pre-call counter and override object.
            if not all(hooks.values()): raise Halt('STORED-RESTORATION',hooks)
            runtime['stored_checks'][arm]={'scale1':_check_record('apply_stored',arm,values),
                                          'hooks':_check_record('apply_stored',arm,hooks)}
            tensor_records=[{'name':H.weight_name(hp,l),'dtype':str(candidate[l].dtype),'shape':list(candidate[l].shape),
                             'sha256':tensor_sha(candidate[l])} for l in hp.layers]
            source_sha=source.get('H_out',{}).get('overlay_sha256',digest(tensor_records))
            runtime['stored_control'][name][arm]={'scale':writer.scale[arm],'source_recipe':'B-e2e','source_arm':arm,
                'source_process':stage,'source_sha256':source_sha,'scale1_reference':values,
                'independently_regenerated':stage in (2,3),'not_triggered_for_arm':writer.scale[arm]==1.,
                'scale1_fully_evaluated_source':{'recipe':'B-e2e','arm':arm,'source_sha256':source_sha} if writer.scale[arm]==1. else None}
    finally:
        restore(H,hp,snapshot)
        if _all_registries(H.model)!=registries: raise Halt('HOOK-RESTORATION')


def compile_accounting(runtime,arm,writer,readout_s):
    target=next(t['seconds'] for t in runtime['timings'] if t['name']=='target_solve' and t['workload']['arms']==[arm])
    write=writer.last_trace['wall_clock_s'] if writer is not None else next(t['seconds'] for t in runtime['timings'] if t['name']=='baseline_write' and t['workload']['arms']==[arm])
    source=0.
    if writer is not None and writer.mode=='apply_stored':
        source=runtime['recipes']['B-e2e']['arms'][arm]['compile_s'];target=0.
    return {'target_solve_s':target,'capture_optimisation_merge_s':write,'production_readout_s':readout_s,
            'source_candidate_s':source,'total_s':math.fsum((target,write,readout_s,source)),
            'excluded':'one-time setup and experimental instrument controls'}


def scientific_readouts(H,hp,arm,Vmap,runtime,writer=None,recipe='A'):
    import torch
    state=H._ARM_STATE
    if not isinstance(state,dict) or 'requests' not in state: raise Halt('ARM-STATE')
    requests=state['requests'];pre=runtime['pre_probes'][arm];P=state['P'];W0=runtime['pristine']
    actual=_actual_updates(H,hp,W0)
    if writer is None:
        planned=runtime['baseline_planned'].get(arm)
        runtime['actual_A'][arm]=actual
    elif writer.mode=='apply_stored':
        planned={l:writer.stored[arm][l].float()*writer.scale[arm] for l in hp.layers}
        runtime['actual_B'].setdefault(recipe,{})[arm]=actual
    else:
        planned={l:writer.As[l].detach()@writer.Bs[l] for l in hp.layers}
        runtime['actual_B'].setdefault(recipe,{})[arm]=actual
    covariances=_covariances(H,hp)
    geometry=write_geometry(H,hp,P,planned,actual,runtime['actual_A'].get(arm) if writer is not None else actual,covariances)
    firsts={H.tgt_ids(v)[0] for v in Vmap.values()};frame_counts={};frame_rows={};relation_flips={};relation_rows={}
    with torch.no_grad():
        for key,t in pre['frames'].items():
            rows=[]
            for s in FRAME_SUBJECTS:
                post=H.predict(t.format(s));before=pre['frame_pre'][key][s]
                rows.append({'subj':s,'pre_top1':before['id'],'post_top1':post['id'],
                             'pre_flip':before['id'] in firsts,'flip':post['id'] in firsts})
            frame_counts[key]=sum(x['flip'] for x in rows);frame_rows[key]=rows
        for key,t in pre['relation_templates'].items():
            rows=[{'subject':r['subject'],'pre_top1':pre['relation_pre'][key][r['subject']]['id'],
                   'post_top1':H.predict(t.format(r['subject']))['id']} for r in requests]
            relation_flips[key]=sum(r['pre_top1']!=r['post_top1'] for r in rows);relation_rows[key]=rows
    raw_descr=runtime['raw_described_as'].get(arm)
    samples=runtime['generic_samples'];expected=list(H.GENERIC)
    def ppl(key):
        rows=samples.get(key,[])
        if [s for s,_ in rows[-len(expected):]]!=expected: raise Halt('RAW-GENERIC-PPL-MISSING',key)
        return math.exp(sum(v for _,v in rows[-len(expected):])/len(expected))
    if raw_descr is None: raise Halt('RAW-DESCRIBED-AS-MISSING',arm)
    axes=state['pre_axes'];post=runtime['predictions'][arm]
    l1=H.L1_PROMPTS;l3=H.L3_PROMPTS
    if any(p not in post for p in l1+l3): raise Halt('RAW-LOCALITY-DISTRIBUTIONS-MISSING')
    kl=[float((cpu64(axes['L3'][p]['dist'])*(cpu64(axes['L3'][p]['dist']).clamp_min(1e-12).log()-cpu64(post[p]['dist']).clamp_min(1e-12).log())).sum()) for p in l3]
    locality={'L1_flips':sum(post[p]['id'] in firsts and post[p]['id']!=axes['L1'][p]['id'] for p in l1),
              'L1_n':len(l1),'L3_agreement':sum(post[p]['id']==axes['L3'][p]['id'] for p in l3),
              'L3_n':len(l3),'L3_mean_kl':sum(kl)/len(kl),'frame_flips':frame_counts,'frame_n':len(FRAME_SUBJECTS),
              'frame_readouts':frame_rows,'described_as_raw':raw_descr,'described_as':round(raw_descr,2),
              'generic_ppl_raw':ppl(arm),'generic_ppl':round(ppl(arm),3),'generic_ppl_pre_raw':ppl('pre'),
              'relation_label_flips':relation_flips,'relation_label_readouts':relation_rows}
    actual_hashes=band_hashes(H,hp)
    tensor_records=[{'name':H.weight_name(hp,l),'dtype':str(actual[l].dtype).removeprefix('torch.'),
                     'shape':list(actual[l].shape),'sha256':tensor_sha(actual[l])} for l in hp.layers]
    output={'locality':locality,'geometry':geometry,'actual_band_hashes':actual_hashes,
            'H_out':{'tensors':tensor_records,'actual_band_sha256':digest(actual_hashes),
                     'overlay_sha256':digest(tensor_records)}}
    if arm in (ARMS[0],A7) and recipe in ('A','B-z','B-e2e'):
        output['remaining_ratios']=_remaining_readout(H,hp,requests,runtime['targets'],pre['anchor_pre'])
    if writer is not None:
        mode=writer.mode
        if mode in ('e2e','anchor'):
            parity=copy.deepcopy(writer.parity)
            if set(parity)!= {'init','final'}: raise Halt('TRAIN-DEPLOY-RECORDS')
            checks=copy.deepcopy(runtime['checks_by_mode_arm'][mode][arm])
            checks['train_deploy']={'passed':all(v['ids_equal'] and v['full_hits_equal'] for v in parity.values()),
                'before_result':True,'scope':{'mode':mode,'arm':arm}}
            batches=[request_batch(H,r,runtime['contexts']) for r in requests]
            if mode=='anchor':
                reference,delta=runtime['anchor_reference'][arm]
                fit=merged_fit(H,hp,requests,runtime['contexts'],reference,delta)
            else: fit=merged_fit(H,hp,requests,runtime['contexts'])
            trace=copy.deepcopy(writer.last_trace)
            for row in trace['loss_components']:
                if 'KL_weighted' in row: row['weighted_KL']=row.pop('KL_weighted')
            output.update(checks=checks,train_deploy=parity,trace=trace,fit=fit)
        else:
            fit=merged_fit(H,hp,requests,runtime['contexts'])
            source=runtime['actual_B']['B-e2e'][arm];scale=writer.scale[arm]
            for row in geometry:
                l=row['layer'];row['cosine_to_candidate']=None if row['actual_norm']==0 or norm(source[l])==0 else cosine(actual[l],source[l])
            arithmetic=all(torch.equal(H.snap_layers(hp)[l],to_like(stored_weight(W0[l],writer.stored[arm][l],scale),W0[l])) for l in hp.layers)
            shares=projector_gate(planned,actual,P)
            directions=all(r['actual_norm']==0 or norm(source[r['layer']])==0 or r['cosine_to_candidate']>=.999 for r in geometry)
            total=math.fsum(r['actual_norm'] for r in geometry);reference_total=math.fsum(norm(v) for v in runtime['actual_A'][arm].values())
            if recipe=='B-e2e-NM':
                matching=scale==1. or control_match('NM',total,reference_total,{},{},{})
            else: matching=scale==1. or all(r['actual_norm']<=1.01*norm(runtime['actual_A'][arm][r['layer']]) for r in geometry)
            if not arithmetic or not shares: raise Halt('STORED-ARITHMETIC-PROPERTY',{'arm':arm,'geometry':geometry})
            stored_checks=copy.deepcopy(runtime['stored_checks'][arm])
            stored_checks['stored_geometry']=_check_record('apply_stored',arm,{'arithmetic_exact':arithmetic,'projector_passed':shares,
                'size_match':matching,'directions_match':directions,'geometry':geometry})
            complete=(len(fit['f_ij'])==24 and all(len(r)==6 and all(math.isfinite(v) for v in r) for r in fit['f_ij']) and
                      math.isfinite(locality['described_as_raw']) and math.isfinite(locality['generic_ppl_raw']) and set(frame_counts)==set(pre['frames']))
            if not complete: raise Halt('STORED-MERGED-READOUTS')
            stored_checks['merged_readouts']=_check_record('apply_stored',arm,{'complete':complete,'merged':fit['merged']})
            output.update(checks=stored_checks,train_deploy=None,
                trace=copy.deepcopy(writer.last_trace),fit=fit)
            if 'stored_control' in runtime: output['stored_control']=copy.deepcopy(runtime['stored_control'][recipe][arm])
    return output


def normalize_recipe(raw,name,stage):
    if not isinstance(raw,dict): raise Halt('RECIPE-SCHEMA',name)
    if raw.get('arms') and all('metrics' in a or a.get('status')=='NOT-RUN' for a in raw['arms'].values()):
        result=copy.deepcopy(raw)
    else:
        law=raw.get('law5_gate',{})
        result={'status':'COMPLETED' if law.get('ok') is True else 'HALTED',
                'law5':{'verdict':'INERT' if law.get('ok') is True else 'NOT-INERT',
                        'delta_expr':law.get('expr_delta'),'delta_loc':law.get('loc_delta')},'arms':{}}
        for arm,fields in raw.get('arms',{}).items():
            detail=copy.deepcopy(raw.get('detail',{}).get(arm,[]));metrics=copy.deepcopy(fields)
            metrics.pop('extra',None);metrics.pop('locality_axes',None);metrics.pop('locality_described_as',None)
            tf_total=sum(r['tf_total'] for r in detail);tf_correct=sum(r['tf_correct'] for r in detail)
            first=metrics.get('para_first_n');full_given=sum(sum(a and b for a,b in zip(r['para_first_hits'],r['para_full_hits'])) for r in detail)
            metrics.update(tf_pertok_cont=100.*tf_correct/tf_total if tf_total else None,
                tf_pertok_cont_denominator=tf_total,tf_pertok_cont_undefined_reason=None if tf_total else 'zero-continuation-tokens',
                cond_full_given_first=full_given/first if first else None,
                cond_full_given_first_denominator=first,cond_full_given_first_undefined_reason=None if first else 'zero-first-token-hits',
                para_full_by_template=[sum(r['para_full_hits'][k] for r in detail) for k in range(3)],
                per_fact_full_n=[sum(r['para_full_hits']) for r in detail],per_edge_pass=[all(r['para_full_hits']) for r in detail])
            science=fields.get('extra',{}).get('c10y',{})
            result['arms'][arm]={'status':'COMPLETED','arm':arm,'metrics':metrics,'detail':detail,
                                'extra':copy.deepcopy(fields.get('extra',{})),**copy.deepcopy(science)}
            if name=='A': result['arms'][arm].update(checks={},train_deploy=None,fit=None)
        result['harness']= {k:copy.deepcopy(v) for k,v in raw.items() if k not in ('arms','detail')}
    if stage==1 and name=='B-e2e':
        for arm in ARMS:
            if arm!=A7: result['arms'].setdefault(arm,{'status':'NOT-RUN'})
    return result


def scored_recipe(H,name,hppath,stage,telemetry):
    original_arms=H.ARMS;original_scorer=H.full_seq_match;original_hooks=H.ARM_HOOKS
    old_state=H._ARM_STATE;had_candidate=hasattr(H,'_CANDIDATE_RECIPE');candidate=getattr(H,'_CANDIDATE_RECIPE',None)
    expected_scorer=getattr(H,'_C10Y_ORIGINAL_SCORER',original_scorer)
    runtime=getattr(H,'_C10Y_READOUT_STATE',None);writer=H.my_edit if isinstance(H.my_edit,Writer) else None
    had_recipe=runtime is not None and 'current_recipe' in runtime
    old_recipe=runtime.get('current_recipe') if runtime is not None else None
    observed={};hook=None
    try:
        if runtime is not None: runtime['current_recipe']=name
        if stage==1 and name=='B-e2e': H.ARMS={A7:original_arms[A7]}
        if runtime is not None and writer is not None and writer.mode=='apply_stored':
            _stored_reference_checks(H,name,writer,runtime)
        if runtime is not None and writer is not None:
            for attr in ('compute_P','run_law5'):
                if not hasattr(H,attr): continue
                observed[attr]=getattr(H,attr)
                def timed_candidate(*args,_attr=attr,**kwargs):
                    return _unit(H,runtime['timings'],'candidate_'+_attr,_workload(requests=72),
                        lambda:observed[_attr](*args,**kwargs),budget=runtime['budget'])
                setattr(H,attr,timed_candidate)
            if hasattr(H,'eval_arm'):
                observed['eval_arm']=H.eval_arm
                def evaluation(*args,**kwargs):
                    runtime['budget'].project(0.);sample_memory(H,'production_readout');sync(H)
                    if '_production_eval_started' not in runtime:
                        runtime['_production_eval_started']=STAGE_CLOCK()
                        if telemetry is not None: telemetry.phase('readout_start')
                    return observed['eval_arm'](*args,**kwargs)
                H.eval_arm=evaluation
        if telemetry is None:
            if H.full_seq_match is not expected_scorer: raise Halt('SCORER-OFF-IDENTITY')
        else: H.full_seq_match=make_scorer(H,lambda p,t,g:telemetry.sink(H,name,'readout',p,t,g))
        H._ARM_STATE=None
        if runtime is not None:
            runtime['generic_samples']={};runtime['raw_described_as']={};runtime['predictions']={}
            def current_arm():
                state=H._ARM_STATE
                if not isinstance(state,dict) or 'requests' not in state: return 'pre'
                matches=[a for a,V in H.ARMS.items() if all(V.get(r['subject'])==r['target_new']['str'].lstrip() for r in state['requests'])]
                if len(matches)!=1: raise Halt('ARM-ATTRIBUTION',matches)
                return matches[0]
            if hasattr(H,'predict'):
                observed['predict']=H.predict
                def prediction(prompt):
                    result=observed['predict'](prompt);arm=current_arm()
                    runtime['predictions'].setdefault(arm,{})[prompt]=result
                    return result
                H.predict=prediction
            if hasattr(H,'locpct'):
                observed['locpct']=H.locpct
                def locpct(post,pre,prompts):
                    result=observed['locpct'](post,pre,prompts)
                    if list(prompts)==[f'{c} is described as' for c in H.FICTION]:
                        runtime['raw_described_as'][current_arm()]=_locpct64(post,pre,prompts)
                    return result
                H.locpct=locpct
            if hasattr(H,'sentence_nll'):
                observed['sentence_nll']=H.sentence_nll
                def sentence_nll(text):
                    result=observed['sentence_nll'](text)
                    runtime['generic_samples'].setdefault(current_arm(),[]).append((text,result))
                    return result
                H.sentence_nll=sentence_nll
            def science(arm,Vmap):
                if arm not in runtime['pre_probes']: raise Halt('PRISTINE-PROBES-MISSING',arm)
                result=scientific_readouts(H,H.hp,arm,Vmap,runtime,writer,name)
                if telemetry is not None:
                    norms={str(r['layer']):{'actual':r['actual_norm'],'planned':r['planned_norm'],
                                            'ratio_to_A':r['actual_ratio_to_A']} for r in result['geometry']}
                    if any(r['ratio_to_A'] is None for r in norms.values()): telemetry.disable(ValueError('undefined zero-reference norm ratio'))
                    else: telemetry.write_norms(norms,name,arm,harness_fp32=copy.deepcopy(runtime['baseline_harness_norms'][arm]) if name=='A' else None)
                    if writer is not None:
                        telemetry.target_probs(f_ij=result['fit']['f_ij'],**({'r_ij':result['fit']['r_ij']} if 'r_ij' in result['fit'] else {}))
                        if arm==A7: telemetry.logit_lens(H,H.hp,'merged',name)
                if name=='A' and '_baseline_eval_started' in runtime:
                    sync(H);finished=STAGE_CLOCK()
                    start,entry=runtime.pop('_baseline_eval_started')
                    runtime['budget'].consume('baseline',max(0.,finished-start-entry['seconds']))
                    entry['seconds']=finished-start;entry['includes_hooks']=True;sample_memory(H,'baseline_evaluation')
                    readout_s=entry['seconds']
                else:
                    if '_production_eval_started' not in runtime: raise Halt('PRODUCTION-READOUT-TIMING-MISSING')
                    if telemetry is not None: telemetry.phase('readout_end')
                    sync(H);readout_s=STAGE_CLOCK()-runtime.pop('_production_eval_started')
                    runtime['budget'].consume('readout',readout_s);sample_memory(H,'production_readout')
                result['compile_parts']=compile_accounting(runtime,arm,writer,readout_s)
                result['compile_s']=result['compile_parts']['total_s']
                return {'c10y':result}
            hook=science;H.ARM_HOOKS=list(original_hooks)+[hook]
        if telemetry is not None: telemetry.phase('recipe_start',recipe=name,arms=list(H.ARMS))
        raw=H.run_recipe(name,str(Path(hppath).resolve()))
        if telemetry is not None: telemetry.phase('recipe_end',recipe=name,arms=list(H.ARMS))
        result=normalize_recipe(raw,name,stage)
        if runtime is not None: runtime.setdefault('recipes',{})[name]=result
        return result
    finally:
        for key,value in observed.items(): setattr(H,key,value)
        H.ARMS=original_arms;H.full_seq_match=original_scorer;H.ARM_HOOKS=original_hooks;H._ARM_STATE=old_state
        if had_candidate: H._CANDIDATE_RECIPE=candidate
        elif hasattr(H,'_CANDIDATE_RECIPE'): delattr(H,'_CANDIDATE_RECIPE')
        if runtime is not None:
            if had_recipe: runtime['current_recipe']=old_recipe
            else: runtime.pop('current_recipe',None)


def _engine_batch_reference(H,request,contexts):
    import torch
    source=ast.parse((Path(ROOT)/SOURCE_PATHS['compute_z']).read_text())
    compute=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='compute_z')
    body=[copy.deepcopy(n) for n in compute.body if 41<=n.lineno<=73]
    if not body or body[0].lineno!=41 or body[-1].lineno!=68: raise Halt('ENGINE-BATCH-SOURCE')
    tree=ast.Module(body=body,type_ignores=[]);ast.fix_missing_locations(tree)
    scope={'torch':torch,'tok':H.tok,'dev':H.DEV,'request':request,'context_templates':contexts,
           'hparams':H.hp,'find_fact_lookup_idx':H.find_fact_lookup_idx}
    exec(compile(tree,'<compute_z source-only batch>','exec'),scope)
    return {k:scope[k] for k in ('input_tok','target_ids','rewriting_targets','lookup_idxs')}


def _objective_audit(H,hp,requests,contexts,targets,target_audit):
    import torch
    snapshot=H.snap_layers(hp);registry=hook_snapshot(H.model);errors=[];constructions=[];driver=[];engine=[]
    with torch.no_grad():
        for request,audit in zip(requests,target_audit):
            batch=request_batch(H,request,contexts);reference=_engine_batch_reference(H,request,contexts)
            equal=(all(torch.equal(batch['input_tok'][k].detach().cpu(),reference['input_tok'][k].detach().cpu()) for k in ('input_ids','attention_mask')) and
                   all(torch.equal(batch[k].detach().cpu(),reference[k].detach().cpu()) for k in ('target_ids','rewriting_targets')) and batch['lookup_idxs']==reference['lookup_idxs'])
            value=float(edit_components(H,[batch],None)['L_edit'].detach().cpu());recorded=audit['iteration0_nll']
            if recorded is None: raise Halt('ENGINE-ITERATION0-NLL-MISSING',request['subject'])
            errors.append(abs(value-recorded));driver.append(value);engine.append(recorded)
            constructions.append({'subject':request['subject'],'equal':equal,
                'input_ids':batch['input_tok']['input_ids'].detach().cpu().tolist(),
                'attention_mask':batch['input_tok']['attention_mask'].detach().cpu().tolist(),
                'target_ids':batch['target_ids'].detach().cpu().tolist(),
                'target_positions':[(row!= -100).nonzero().flatten().detach().cpu().tolist() for row in batch['rewriting_targets']],
                'lookup_idxs':list(batch['lookup_idxs'])})
        batches=[request_batch(H,r,contexts) for r in requests]
        first=batches[0];h0=_anchor_rows(H,hp,[first]).detach()[0,0]
        delta=targets[_request_keys(requests)[0]].to(h0.device)-h0
        kl_errors={};kl_values={}
        module=dict(H.model.named_modules())[hp.layer_module_tmp.format(hp.layers[-1])]
        for label,intervention in (('init',None),('nonzero',delta)):
            raw_driver=weighted_driver=raw_engine=weighted_engine=0.
            for indices,weight in zip(microbatch_indices(24,6),request_weights([6,6,6,6])):
                selected=[batches[i] for i in indices];tokens,_,kl,_=packed_batches(H,selected)
                pristine=edit_components(H,selected,None)['kl_log_probs'].detach()
                # Independent engine-style KL distribution from the causal-LM forward.
                base_logits=H.model(input_ids=tokens['input_ids'],attention_mask=tokens['attention_mask'],use_cache=False).logits
                base=torch.log_softmax(torch.stack([base_logits[row,idx,:] for row,idx in kl]),dim=1).detach()
                handle=None
                if intervention is not None:
                    def add_delta(m,args,out):
                        value=out[0] if isinstance(out,tuple) else out;changed=value.clone()
                        for row,idx in kl: changed[row,idx,:]+=to_like(intervention,changed)
                        return (changed,)+out[1:] if isinstance(out,tuple) else changed
                    handle=module.register_forward_hook(add_delta)
                try:
                    v=edit_components(H,selected,pristine)
                    logits=H.model(input_ids=tokens['input_ids'],attention_mask=tokens['attention_mask'],use_cache=False).logits
                    current=torch.log_softmax(torch.stack([logits[row,idx,:] for row,idx in kl]),dim=1)
                    # compute_z:151-153, coefficient applied once; diagnostic reduction on CPU64.
                    r=torch.nn.functional.kl_div(cpu64(base),cpu64(current),log_target=True,reduction='batchmean')
                    raw_driver+=weight*float(v['KL_raw'].detach().cpu());weighted_driver+=weight*float(v['KL_weighted'].detach().cpu())
                    raw_engine+=weight*float(r);weighted_engine+=weight*float(hp.kl_factor*r)
                finally:
                    if handle is not None: handle.remove()
            kl_errors[label+'_raw']=abs(raw_driver-raw_engine);kl_errors[label+'_weighted']=abs(weighted_driver-weighted_engine)
            kl_values[label]={'driver_raw':raw_driver,'engine_raw':raw_engine,
                              'driver_weighted':weighted_driver,'engine_weighted':weighted_engine}
    record={'nll_errors':errors,'driver_iteration0_nll':driver,'engine_iteration0_nll':engine,
            'KL_errors':kl_errors,'KL_values':kl_values,'constructed_like_compute_z':all(r['equal'] for r in constructions),
            'construction_records':constructions,'nonzero_intervention_delta_sha256':tensor_sha(delta),
            'nonzero_intervention_delta_norm':norm(delta),'request_count':len(requests),
            'reduction_dtype':'float64','reduction_device':'cpu'}
    if band_hashes(H,hp)!={str(l):tensor_sha(t) for l,t in snapshot.items()} or hook_snapshot(H.model)!=registry: raise Halt('OBJECTIVE-RESTORATION')
    if len(errors)!=24 or not record['constructed_like_compute_z'] or any(not math.isfinite(e) or e>2e-3 for e in errors+list(kl_errors.values())) or norm(delta)==0:
        raise Halt('OBJECTIVE-CONSTRUCTION',record)
    return record


def _fixed_padding(H,batches):
    import torch
    width=max(b['input_tok']['input_ids'].shape[1] for b in batches);fixed=[]
    for b in batches:
        value=dict(b);value['input_tok']={k:torch.nn.functional.pad(v,(0,width-v.shape[1]),value=H.tok.pad_token_id if k=='input_ids' else 0) for k,v in b['input_tok'].items()}
        value['rewriting_targets']=torch.nn.functional.pad(b['rewriting_targets'],(0,width-b['rewriting_targets'].shape[1]),value=-100)
        fixed.append(value)
    return fixed


def _gradient_evaluations(H,hp,requests,contexts,factors,W0,mode,targets,groups,scale=1024.,fixed=False):
    import torch
    params={l:torch.nn.Parameter(factors[l]['R'].to(H.DEV).float().clone()) for l in hp.layers}
    bs={l:factors[l]['B'].to(H.DEV).float().detach() for l in hp.layers};operators=(params,bs,W0)
    batches=[request_batch(H,r,contexts) for r in requests]
    if fixed: batches=_fixed_padding(H,batches)
    pristine={};reference=delta=None
    with torch.no_grad():
        if mode=='e2e':
            for group in groups: pristine[tuple(group)]=edit_components(H,[batches[i] for i in group],None)['kl_log_probs'].detach()
        else: reference,delta=_pristine_anchor(H,hp,requests,batches,targets)
    flags={p:p.requires_grad for p in H.model.parameters()};training=H.model.training;opt=torch.optim.Adam(list(params.values()),lr=0.)
    try:
        for p in flags:
            if p.grad is not None: raise Halt('BASE-GRADIENT')
            p.requires_grad_(False)
        H.model.eval();opt.zero_grad(set_to_none=True);total=0.
        for group,weight in zip(groups,request_weights([len(g) for g in groups])):
            sample_memory(H,'gradient');selected=[batches[i] for i in group]
            if mode=='e2e': loss=edit_components(H,selected,pristine[tuple(group)],operators)['L']
            else:
                current=_anchor_rows(H,hp,selected,operators)
                loss=anchor_loss(current,reference[group]+delta[group,None,:],delta[group])
            total+=weight*float(loss.detach().cpu());(loss*weight*scale).backward();sample_memory(H,'gradient')
        for a in params.values():
            if a.grad is not None: a.grad.div_(scale)
        gradients={l:None if a.grad is None else a.grad.detach().cpu().clone() for l,a in params.items()}
        base_absent=all(p.grad is None for p in H.model.parameters())
        only_A={id(p) for group in opt.param_groups for p in group['params']}=={id(p) for p in params.values()}
        lengths=[packed_batches(H,[batches[i] for i in group])[0]['input_ids'].shape[1] for group in groups]
        return {'gradients':gradients,'loss':total,'padded_lengths':lengths,'base_gradients_absent':base_absent,
                'only_A_optimised':only_A,'eval_mode':not H.model.training,'use_cache':False}
    finally:
        opt.zero_grad(set_to_none=True)
        for p,flag in flags.items(): p.requires_grad_(flag)
        H.model.train(training)


def _accumulation_check(H,hp,requests,contexts,factors,W0,mode,targets,timings,budget):
    import torch
    subset=requests[:12];headroom=sample_memory(H,'accumulation_reference');comparisons=[]
    # The same padded tensors are used by the 12-request reference and both splits.
    reference=_unit(H,timings,'accumulation_reference_'+mode,_workload(A7,12,0,1),
        lambda:_gradient_evaluations(H,hp,subset,contexts,factors,W0,mode,targets,[list(range(12))],fixed=True),budget=budget)
    reference_lengths=reference['padded_lengths']
    for split,groups in (('6+6',[list(range(6)),list(range(6,12))]),('5+7',[list(range(5)),list(range(5,12))])):
        part=_unit(H,timings,'accumulation_'+mode+'_'+split,_workload(A7,12,0,2),
            lambda:_gradient_evaluations(H,hp,subset,contexts,factors,W0,mode,targets,groups,fixed=True),budget=budget)
        if any(t!=reference_lengths[0] for t in part['padded_lengths']): raise Halt('ACCUMULATION-PADDING')
        for l in hp.layers:
            a,b=reference['gradients'][l],part['gradients'][l]
            finite=a is not None and b is not None and bool(torch.isfinite(a).all()) and bool(torch.isfinite(b).all())
            row={'layer':l,'split':split,'finite':finite,'norm':0. if b is None else norm(b),
                 'reference_norm':0. if a is None else norm(a),'cosine':cosine(a,b) if finite else 0.,
                 'relative_l2':_directed_distance(a,b) if finite and norm(a)>0 else 1.}
            comparisons.append(row)
    record={'subset':list(range(12)),'splits':[[6,6],[5,7]],'weighted_by_request_count':request_weights([6,6])==[.5,.5] and request_weights([5,7])==[5/12,7/12],
        'reference_headroom_ok':True,'reference_headroom':headroom,'gradients':comparisons,
        'padded_lengths':reference_lengths,'padding_identical':True,'scope_full24':'weighting/index logic only; no full24 reference graph',
        'full24_groups':microbatch_indices(24,6),'full24_weights':request_weights([6,6,6,6]),
        'reduction_dtype':'float64','reduction_device':'cpu'}
    if any(not r['finite'] or r['norm']<=0 or r['reference_norm']<=0 or r['cosine']<.999 or r['relative_l2']>.01 for r in comparisons):
        raise Halt('ACCUMULATION-PARITY',record)
    return record


def _gradient_check(H,hp,requests,contexts,factors,W0,mode,targets,timings,budget):
    import torch
    records=[];arm=next(a for a,V in H.ARMS.items() if all(V.get(r['subject'])==r['target_new']['str'].lstrip() for r in requests))
    for halvings in range(4):
        scale=1024./2**halvings
        values=_unit(H,timings,'gradient_'+mode,_workload(arm,len(requests),0,4),
            lambda:_gradient_evaluations(H,hp,requests,contexts,factors,W0,mode,targets,microbatch_indices(len(requests),6),scale),repetition=halvings+1,budget=budget)
        layers=[{'layer':l,'finite':g is not None and bool(torch.isfinite(g).all()),'norm':None if g is None else norm(g)} for l,g in values['gradients'].items()]
        records.append({'loss_scale':scale,'layers':layers})
        if all(r['finite'] and r['norm']>0 for r in layers):
            result={'init_loss_scale':1024,'halvings':halvings,'layers':layers,'attempts':records,
                    **{k:values[k] for k in ('base_gradients_absent','only_A_optimised','eval_mode','use_cache')}}
            if not result['base_gradients_absent'] or not result['only_A_optimised'] or not result['eval_mode']: raise Halt('GRADIENT-HYGIENE',result)
            return result
    raise Halt('GRADIENT-FINITENESS',records)


def _all_registries(model):
    return {n:{kind:tuple(getattr(m,kind).items()) for kind in ('_forward_hooks','_forward_pre_hooks','_backward_hooks')}
            for n,m in model.named_modules()}


def _check_record(mode,arm,values):
    return {'passed':True,'before_result':True,'scope':{'mode':mode,'arm':arm},**values}


def _write_proof(writer,mode,requests,P,cache,iterations,lr=None):
    import torch
    namespace=globals();old_hook=namespace['deployed_hook'];old_accepted=namespace['accepted_step'];old_adam=torch.optim.Adam.step
    facts={'adam_steps':0,'routing_masks':0,'scaled_calls':[],'base_hashes':[]};base=band_hashes(writer.H,writer.hp)
    def observed_hook(W0,a,b,mask):
        if mask is not None and bool((~mask.detach().cpu()).any()) and bool(mask.detach().cpu().any()): facts['routing_masks']+=1
        return old_hook(W0,a,b,mask)
    def observed_adam(opt,*args,**kwargs):
        if {id(p) for group in opt.param_groups for p in group['params']}!={id(p) for p in writer.As.values()}:
            raise Halt('OPTIMISER-PARAMETER-IDENTITY')
        value=old_adam(opt,*args,**kwargs);facts['adam_steps']+=1;return value
    def observed_accepted(*args,**kwargs):
        result=old_accepted(*args,**kwargs)
        facts['scaled_calls'].append({'scale':args[4],'groups':[len(g) for g in args[3]],
            'gradient_norms':result['gradient_norms'],'stopped':result['stopped'],'loss_scale':result['loss_scale']})
        facts['base_hashes'].append(band_hashes(writer.H,writer.hp)==base)
        return result
    try:
        namespace['deployed_hook']=observed_hook;namespace['accepted_step']=observed_accepted;torch.optim.Adam.step=observed_adam
        writer.write(mode,requests,P,cache,check=True,iterations=iterations,lr_override=lr,force_steps=True)
        return facts
    finally:
        namespace['deployed_hook']=old_hook;namespace['accepted_step']=old_accepted;torch.optim.Adam.step=old_adam


def _counts(H,Vmap):
    result=H.eval_arm(Vmap)
    return {k:result[k] for k in ('canon_full_n','para_full_n','para_first_n')},result


def instrument_prefix(H,out,budget,calibration=False,telemetry=None):
    import torch
    hp=H.hp;out=Path(out);stage='calibration' if calibration else budget.stage
    original={k:getattr(H,k) for k in ('my_edit','ARMS','ARM_HOOKS','full_seq_match','Z_OVERRIDE','Z_OVERRIDE_HITS','_LAW5_DEFAULT_CTX','_ARM_STATE')}
    optional={k:getattr(H,k) for k in ('_CANDIDATE_RECIPE','_C10Y_READOUT_STATE') if hasattr(H,k)}
    registry=_all_registries(H.model);W0=H.snap_layers(hp);base_hashes=band_hashes(H,hp);source_start=source_hashes()
    timings=copy.deepcopy(getattr(H,'_C10Y_STARTUP_TIMINGS',[]));ledger=[];targets={};target_audits={};checks={};law5={};step0={};P_box={}
    runtime={'pristine':W0,'targets':targets,'pre_probes':{},'baseline_planned':{},'baseline_harness_norms':{},'actual_A':{},'actual_B':{},
             'checks_by_mode_arm':{},'anchor_reference':{},'stored_checks':{},'timings':timings,'ledger':ledger,
             'stage':stage,'budget':budget,'target_audits':target_audits,'recipes':{}}
    had_telemetry=hasattr(H,'_C10Y_TELEMETRY');old_telemetry=getattr(H,'_C10Y_TELEMETRY',None);H._C10Y_TELEMETRY=telemetry
    context_globals=H.get_context_templates.__globals__;had_cache='CONTEXT_TEMPLATES_CACHE' in context_globals;old_cache=context_globals.get('CONTEXT_TEMPLATES_CACHE')
    def pristine_restore(): restore(H,hp,W0)
    def cache(P): return [torch.zeros_like(p,dtype=torch.float32,device='cpu') for p in P]
    def baseline_edit(hparam,requests,P,cache_c):
        if H._LAW5_DEFAULT_CTX: return original['my_edit'](hparam,requests,P,cache_c)
        matches=[a for a,V in H.ARMS.items() if all(V.get(r['subject'])==r['target_new']['str'].lstrip() for r in requests)]
        if len(matches)!=1: raise Halt('ARM-ATTRIBUTION')
        arm=matches[0];P_box['P']=P
        if band_hashes(H,hp)!=base_hashes: raise Halt('PRISTINE-BAND-IDENTITY')
        runtime['pre_probes'][arm]=_probe_pristine(H,hp,requests,runtime['contexts'])
        planned={};previous_match=H.upd_matrix_match_shape
        def match(update,shape):
            value=previous_match(update,shape)
            if len(planned)>=len(hp.layers): raise Halt('BASELINE-UPDATE-COUNT')
            planned[hp.layers[len(planned)]]=value.detach().cpu().clone();return value
        try:
            H.upd_matrix_match_shape=match
            result=_ledger_call(H,ledger,stage,'A',arm,'write',targets,_request_keys(requests),
                lambda:_unit(H,timings,'baseline_write',_workload(arm,len(requests)),
                    lambda:original['my_edit'](hparam,requests,P,cache_c),repetition=ARMS.index(arm)+1,budget=budget),expected_hits=1)
            runtime['baseline_planned'][arm]=planned if len(planned)==len(hp.layers) else None
            runtime['baseline_harness_norms'][arm]=copy.deepcopy(result)
            runtime['actual_A'][arm]=_actual_updates(H,hp,W0)
            budget.project(0.);sync(H);runtime['_baseline_production_started']=STAGE_CLOCK()
            return result
        finally: H.upd_matrix_match_shape=previous_match
    timed_originals={}
    result=None
    try:
        def contexts_and_audit():
            if getattr(H,'_C10Y_CONTEXTS',None) is None:
                freeze_contexts(H,out/('context_templates_calib.json' if calibration else 'context_templates.json'))
            values=copy.deepcopy(H._C10Y_CONTEXTS)
            context_globals['CONTEXT_TEMPLATES_CACHE']=values
            audit=overlap_audit(values,H)
            if not audit['clean']: raise Halt('INVALID-LEAKAGE',audit)
            return values,audit
        contexts,audit=_unit(H,timings,'contexts_overlap',_workload(requests=72),contexts_and_audit,budget=budget)
        installation=getattr(H,'_C10Y_CONTEXT_INSTALL_SECONDS',0.)
        timings[-1]['seconds']+=installation;timings[-1]['includes_install']=True
        budget.consume('contexts_targets',installation)
        runtime['contexts']=contexts;runtime['overlap_audit']=audit
        template_lengths=[len(H.tok(c)['input_ids']) for group in contexts for c in group]
        for arm,V in original['ARMS'].items():
            requests=[H.req(H.CANON,s,V[s]) for s in H.FICTION];target_audits[arm]=[]
            solve_entry={'stage':stage,'recipe':'targets','arm':arm,'check':'solve','status':'RUNNING',
                         'declared_overrides':[],'consumed_overrides':[],'declared_solved_keys':_key_records(_request_keys(requests)),'solved_keys':[]}
            ledger.append(solve_entry)
            def solve_arm():
                for request in requests:
                    if band_hashes(H,hp)!=base_hashes: raise Halt('PRISTINE-TARGET-BAND')
                    text=io.StringIO()
                    with contextlib.redirect_stdout(text): z=H.compute_z(H.model,H.tok,request,hp,hp.layers[-1],contexts)
                    if z is None or not bool(torch.isfinite(z).all()): raise Halt('TARGET-SOLVE',request['subject'])
                    output=text.getvalue();match=re.search(r'^loss\s+\S+\s*=\s*([-+0-9.eE]+)\s*\+',output,re.MULTILINE)
                    nll=None if match is None else float(match.group(1))
                    if nll is not None and not math.isfinite(nll): raise Halt('ENGINE-ITERATION0-NLL')
                    targets[(request['subject'],request['target_new']['str'])]=z.detach().cpu().clone()
                    solve_entry['solved_keys'].append({'subject':request['subject'],'target':request['target_new']['str']})
                    target_audits[arm].append({'subject':request['subject'],'target':request['target_new']['str'],
                        'iteration0_nll':nll,'compute_z_stdout':output,'source':SOURCE_PATHS['compute_z']+':159-163'})
                if band_hashes(H,hp)!=base_hashes: raise Halt('TARGET-SOLVE-BASE-MUTATION')
            try:
                _unit(H,timings,'target_solve',_workload(arm,24),solve_arm,repetition=ARMS.index(arm)+1,budget=budget)
                solve_entry['status']='COMPLETED'
            except BaseException:
                solve_entry['status']='HALTED';raise
        H.Z_OVERRIDE=targets;H.Z_OVERRIDE_HITS=0;H.my_edit=baseline_edit;H._C10Y_READOUT_STATE=runtime
        for attr,name in (('compute_P','baseline_projector'),('run_law5','baseline_law5'),('eval_arm','baseline_evaluation')):
            if not hasattr(H,attr): continue
            timed_originals[attr]=getattr(H,attr)
            def timed(*args,_attr=attr,_name=name,**kwargs):
                arm=None
                if _attr=='eval_arm':
                    arm=next((a for a,V in H.ARMS.items() if V is args[0]),None)
                sync(H);unit_started=runtime.pop('_baseline_production_started') if _attr=='eval_arm' and '_baseline_production_started' in runtime else STAGE_CLOCK()
                value=_unit(H,timings,_name,_workload(arm,24 if arm else 0,96 if arm else 0),
                    lambda:timed_originals[_attr](*args,**kwargs),budget=budget)
                if _attr=='compute_P': P_box['P']=value
                if _attr=='eval_arm': runtime['_baseline_eval_started']=(unit_started,timings[-1])
                return value
            setattr(H,attr,timed)
        baseline_start=len(timings);sync(H);started=STAGE_CLOCK()
        baseline=scored_recipe(H,'A',H.HP_BASE,1 if calibration else stage,telemetry)
        sync(H);baseline_elapsed=STAGE_CLOCK()-started
        baseline_units=sum(t['seconds'] for t in timings[baseline_start:] if t['name'] in ('baseline_projector','baseline_law5','baseline_write','baseline_evaluation'))
        timings.append({'name':'baseline_recipe_overhead','seconds':max(0.,baseline_elapsed-baseline_units),
                        'repetition':1,'workload':_workload(requests=72,scored=288),'synchronised':True})
        budget.consume('baseline',timings[-1]['seconds'])
        for attr,value in timed_originals.items(): setattr(H,attr,value)
        timed_originals.clear();H.my_edit=original['my_edit'];pristine_restore()
        def law3_gate():
            try:
                a=baseline['arms'][A7]['metrics'];controls=[baseline['arms'][arm]['metrics']['para_full_n'] for arm in ARMS[:2]]
                valid=(baseline['law5']['verdict']=='INERT' and all(type(a[k]) is int for k in ('canon_full_n','para_full_n','para_first_n')) and
                    a.get('para_n')==72 and a.get('canon_n')==24 and 5<=a['para_full_n']<=18 and 5<=a['canon_full_n']<=10 and 42<=a['para_first_n']<=59 and
                    all(type(n) is int and n>=68 for n in controls))
            except KeyError as e: raise Halt('LAW#3',{'baseline':baseline,'missing':str(e)}) from e
            if not valid: raise Halt('LAW#3',baseline)
            return {'passed':True,'A7':copy.deepcopy(a),'A1_A2_para_full_n':controls,'before_candidates':True}
        v4=_unit(H,timings,'law3',_workload(requests=72,scored=288),law3_gate,budget=budget)
        law5.update(standing=copy.deepcopy(baseline['law5']),V4=v4)
        if telemetry is not None: telemetry.logit_lens(H,hp,'pristine')
        P=P_box.get('P')
        if P is None or set(runtime['actual_A'])!=set(ARMS): raise Halt('BASELINE-MERGED-READOUTS-MISSING')
        runtime['P']=P
        covariances=_covariances(H,hp)
        for arm in ARMS:
            actual=runtime['actual_A'][arm]
            if runtime['baseline_planned'].get(arm) is None: raise Halt('BASELINE-PLANNED-UPDATES-MISSING',arm)
            if any(norm(actual[l]) and null_share(actual[l],P[i])<.999 for i,l in enumerate(hp.layers)):
                raise Halt('PRECISION-DIAGNOSIS',{'arm':arm,'geometry':baseline['arms'][arm].get('geometry')})
        modes=('e2e',) if calibration or stage==1 else ('e2e','anchor')
        scoped_arms=(A7,) if calibration or stage==1 else ARMS
        runtime['checks_by_mode_arm']={mode:{} for mode in modes}
        captures={};references={}
        for arm in scoped_arms:
            requests=[H.req(H.CANON,s,original['ARMS'][arm][s]) for s in H.FICTION];keys=_request_keys(requests);writes=[];write_hashes=[]
            for repetition in (1,2):
                pristine_restore()
                _ledger_call(H,ledger,stage,'instrument',arm,'original_%d'%repetition,targets,keys,
                    lambda:_unit(H,timings,'original_my_edit',_workload(arm,24),
                        lambda:original['my_edit'](hp,requests,P,cache(P)),repetition=repetition,budget=budget),expected_hits=1)
                writes.append(_actual_updates(H,hp,W0))
                write_hashes.append(band_hashes(H,hp))
            floor=max(_directed_distance(writes[0][l],writes[1][l]) for l in hp.layers);tolerance=max(10*floor,1e-4)
            references[arm]=writes[0];pristine_restore()
            factors=_ledger_call(H,ledger,stage,'instrument',arm,'capture',targets,keys,
                lambda:_unit(H,timings,'capture_solve',_workload(arm,24),lambda:capture_solve(H,hp,requests,P,cache(P)),budget=budget),expected_hits=1)
            captured=_actual_updates(H,hp,W0);distances={str(l):_directed_distance(writes[0][l],captured[l]) for l in hp.layers}
            cap={'floor':floor,'tolerance':tolerance,'distance_by_layer':distances,
                 'reference_weight_hashes':write_hashes[0],'floor_weight_hashes':write_hashes[1],
                 'capture_weight_hashes':band_hashes(H,hp),'original_calls':2}
            if any(v>tolerance or not math.isfinite(v) for v in distances.values()): raise Halt('CAPTURE-SOLVE-IDENTITY',cap)
            captures[arm]=factors;pristine_restore()
            if 'anchor' in modes:
                batches=[request_batch(H,r,contexts) for r in requests]
                runtime['anchor_reference'][arm]=_pristine_anchor(H,hp,requests,batches,targets)
            expected_counts={k:baseline['arms'][arm]['metrics'][k] for k in ('canon_full_n','para_full_n','para_first_n')}
            for mode in modes:
                mode_checks={'capture':_check_record(mode,arm,copy.deepcopy(cap))};runtime['checks_by_mode_arm'][mode][arm]=mode_checks
                writer=Writer(H,hp,None,budget);writer.baseline_passed=True
                for check_name,iterations,lr in (('zero_step',0,None),('executed_loop',3,0.)):
                    pristine_restore()
                    proof=_ledger_call(H,ledger,stage,'B-e2e' if mode=='e2e' else 'B-z',arm,check_name,targets,keys,
                        lambda:_write_proof(writer,mode,requests,P,cache(P),iterations,lr),expected_hits=1)
                    for entry in writer.phase_timings:
                        timings.append(dict(entry,name=check_name+'_'+entry['name'],arm=arm,mode=mode,synchronised=True))
                    for i,entry in enumerate(writer.iteration_timings):
                        timings.append(dict(entry,name='executed_loop_step',arm=arm,mode=mode,repetition=i+1,synchronised=True))
                    actual=_actual_updates(H,hp,W0);counts,evaluation=_unit(H,timings,check_name+'_evaluation',_workload(arm,24,96),lambda:_counts(H,original['ARMS'][arm]),budget=budget)
                    distance={str(l):_directed_distance(references[arm][l],actual[l]) for l in hp.layers}
                    values={'distance_by_layer':distance,'counts_equal':counts==expected_counts,'counts':counts,'reference_counts':expected_counts,
                            'merged_weight_hashes':band_hashes(H,hp),'merged_evaluation':copy.deepcopy(evaluation)}
                    if check_name=='executed_loop':
                        values.update(forced_iterations=3,lr=0.,early_stopping=False,adam_steps=proof['adam_steps'],
                            routing_executed=proof['routing_masks']>0,accumulation_batches=proof['scaled_calls'][0]['groups'] if proof['scaled_calls'] else [],
                            loss_scaling_executed=len(proof['scaled_calls'])==3 and all(r['scale']>0 and r['loss_scale']>0 for r in proof['scaled_calls']),
                            proof_observations=proof,
                            iteration_records=copy.deepcopy(writer.iteration_timings))
                        if writer.last_trace['accepted_steps']!=3 or len(writer.trajectory)!=3 or proof['adam_steps']!=3 or not values['routing_executed'] or not values['loss_scaling_executed']:
                            raise Halt('EXECUTED-LOOP-COUNT',values)
                    if not values['counts_equal'] or any(v>tolerance or not math.isfinite(v) for v in distance.values()): raise Halt(check_name.upper()+'-IDENTITY',values)
                    mode_checks[check_name]=_check_record(mode,arm,values)
                    if check_name=='zero_step':
                        parity=writer.parity['init'];step0.setdefault('init_parity',{}).setdefault(mode,{})[arm]=parity
                        mode_checks['train_deploy']=_check_record(mode,arm,{'init':parity})
                        planned={l:writer.As[l].detach()@writer.Bs[l] for l in hp.layers}
                        geometry=_unit(H,timings,'projector_property',_workload(arm,24),lambda:write_geometry(H,hp,P,planned,actual,references[arm],covariances),budget=budget)
                        mode_checks['projector']=_check_record(mode,arm,{
                            'init_planned_share_by_layer':{str(r['layer']):r['planned_null_share'] for r in geometry},
                            'init_actual_share_by_layer':{str(r['layer']):r['actual_null_share'] for r in geometry},'geometry':geometry})
                    pristine_restore()
                mode_checks['gradient']=_check_record(mode,arm,_gradient_check(H,hp,requests,contexts,factors,W0,mode,targets,timings,budget))
                pristine_restore()
            if arm==A7:
                objective=_unit(H,timings,'objective_construction',_workload(arm,24),
                    lambda:_objective_audit(H,hp,requests,contexts,targets,target_audits[arm]),budget=budget)
                runtime['checks_by_mode_arm']['e2e'][arm]['objective']=_check_record('e2e',arm,objective)
                for mode in modes:
                    runtime['checks_by_mode_arm'][mode][arm]['accumulation']=_check_record(mode,arm,
                        _accumulation_check(H,hp,requests,contexts,factors,W0,mode,targets,timings,budget))
            pristine_restore()
        checks['merged_evaluations']=['zero_step','executed_loop','init_parity']
        checks['by_mode_arm']=runtime['checks_by_mode_arm']
        H.Z_OVERRIDE=original['Z_OVERRIDE'];H.Z_OVERRIDE_HITS=original['Z_OVERRIDE_HITS']
        def restoration_gate():
            values={'registries_equal':_all_registries(H.model)==registry,'writer_handles_removed':_all_registries(H.model)==registry,
                'unknown_hooks_preserved':_all_registries(H.model)==registry,'pristine_restored':band_hashes(H,hp)==base_hashes,
                'wrapper_restored':H.my_edit is original['my_edit'],'overrides_restored':H.Z_OVERRIDE is original['Z_OVERRIDE'] and H.Z_OVERRIDE_HITS==original['Z_OVERRIDE_HITS']}
            if not all(values.values()): raise Halt('RESTORATION',values)
            return values
        restoration=_unit(H,timings,'restoration_hooks',_workload(),restoration_gate,budget=budget)
        for mode,arms in runtime['checks_by_mode_arm'].items():
            for arm,values in arms.items(): values['hooks']=_check_record(mode,arm,restoration.copy())
        requests=[H.req(H.CANON,s,original['ARMS'][A7][s]) for s in H.FICTION]
        smoke=Writer(H,hp,None,budget);smoke.baseline_passed=True
        smoke_loss_before=_unit(H,timings,'smoke_loss_before',_workload(A7,24,0,4),
            lambda:_gradient_evaluations(H,hp,requests,contexts,captures[A7],W0,'e2e',targets,microbatch_indices(24,6))['loss'],budget=budget)
        smoke_proof=_ledger_call(H,ledger,stage,'instrument',A7,'smoke',targets,_request_keys(requests),
            lambda:_write_proof(smoke,'e2e',requests,P,cache(P),3),expected_hits=1)
        for entry in smoke.phase_timings: timings.append(dict(entry,name='smoke_'+entry['name'],arm=A7,mode='e2e',synchronised=True))
        for i,entry in enumerate(smoke.iteration_timings): timings.append(dict(entry,name='smoke_step',arm=A7,mode='e2e',repetition=i+1,synchronised=True))
        changed=[not torch.equal(smoke.As[l].detach().cpu(),smoke.factors[l]['R'].detach().cpu()) for l in hp.layers]
        finite=[len(smoke_proof['scaled_calls'])==3 and all(math.isfinite(row['gradient_norms'][i]) and row['gradient_norms'][i]>0 for row in smoke_proof['scaled_calls']) for i,l in enumerate(hp.layers)]
        smoke_after=smoke.parity['final']['losses']['total'][0]
        # A hooked forward must leave the frozen parameter objects at their pristine hashes.
        pristine_restore();unchanged=bool(smoke_proof['base_hashes']) and all(smoke_proof['base_hashes']) and band_hashes(H,hp)==base_hashes
        with torch.no_grad():
            for group in microbatch_indices(24,6):
                batches=[request_batch(H,requests[i],contexts) for i in group]
                edit_components(H,batches,None,(smoke.As,smoke.Bs,W0))
        unchanged=unchanged and band_hashes(H,hp)==base_hashes
        restored=_unit(H,timings,'smoke_restore_hash',_workload(A7,24),lambda:(pristine_restore(),band_hashes(H,hp)==base_hashes)[1],budget=budget)
        smoke_record={'steps':smoke.last_trace['accepted_steps'],'nonzero_lr':all(.02*norm(smoke.factors[l]['R'])/math.sqrt(smoke.As[l].numel())>0 for l in hp.layers),
            'A_changed_layers':changed,'gradient_finite_layers':finite,'loss_before':smoke_loss_before,'loss_after':smoke_after,
            'base_hash_unchanged':unchanged,'restored':restored,'synchronised':True,
            'iteration_records':copy.deepcopy(smoke.iteration_timings),'proof_observations':smoke_proof}
        if smoke_record['steps']!=3 or not smoke_record['nonzero_lr'] or not all(changed) or not all(finite) or not unchanged or not restored:
            raise Halt('CANDIDATE-SMOKE',smoke_record)
        runtime['checks_by_mode_arm']['e2e'][A7]['smoke']=_check_record('e2e',A7,smoke_record)
        step0.update(smoke=smoke_record,checks=runtime['checks_by_mode_arm'],memory=copy.deepcopy(getattr(H,'_C10Y_MEMORY',{})))
        law5['checks']={mode:{arm:{k:v for k,v in values.items() if k in ('capture','zero_step','executed_loop')} for arm,values in arms.items()} for mode,arms in runtime['checks_by_mode_arm'].items()}
        lengths=[n for t in timings for n in t.get('workload',{}).get('padded_lengths',[])]
        if not lengths: raise Halt('PADDED-LENGTH-TIMINGS-MISSING')
        if source_hashes()!=source_start: raise Halt('SOURCE-DRIFT')
        candidate_writer=Writer(H,hp,telemetry,budget);candidate_writer.baseline_passed=True
        candidate_writer.runtime=runtime;candidate_writer.targets=targets;candidate_writer.ledger=ledger;candidate_writer.stage=stage
        result={'baseline':baseline,'contexts':contexts,'targets':targets,'ledger':ledger,'law5':law5,'step0':step0,'checks':checks,
                'overlap_audit':audit,'timings':timings,'T_cal':max(lengths),'template_token_lengths':template_lengths,
                'baseline_passed':True,'actual_A':runtime['actual_A'],'actual_B':runtime['actual_B'],'runtime':runtime,'writer':candidate_writer}
    finally:
        if had_telemetry: H._C10Y_TELEMETRY=old_telemetry
        else: del H._C10Y_TELEMETRY
        for attr,value in timed_originals.items(): setattr(H,attr,value)
        restore(H,hp,W0)
        for key,value in original.items(): setattr(H,key,value)
        for key in ('_CANDIDATE_RECIPE','_C10Y_READOUT_STATE'):
            if key in optional: setattr(H,key,optional[key])
            elif hasattr(H,key): delattr(H,key)
        if had_cache: context_globals['CONTEXT_TEMPLATES_CACHE']=old_cache
        else: context_globals.pop('CONTEXT_TEMPLATES_CACHE',None)
        if _all_registries(H.model)!=registry: raise Halt('HOOK-RESTORATION')
        if any(getattr(H,k) is not value if k not in ('Z_OVERRIDE_HITS','_LAW5_DEFAULT_CTX') else getattr(H,k)!=value for k,value in original.items()):
            raise Halt('GLOBAL-RESTORATION')
    if result is None: raise Halt('INCOMPLETE-INSTRUMENT-PREFIX')
    for mode,arms in runtime['checks_by_mode_arm'].items():
        for arm,values in arms.items():
            values['hooks']=_check_record(mode,arm,{'registries_equal':_all_registries(H.model)==registry,
                'writer_handles_removed':_all_registries(H.model)==registry,'unknown_hooks_preserved':_all_registries(H.model)==registry,
                'pristine_restored':band_hashes(H,hp)==base_hashes,'wrapper_restored':H.my_edit is original['my_edit'],
                'overrides_restored':H.Z_OVERRIDE is original['Z_OVERRIDE'] and H.Z_OVERRIDE_HITS==original['Z_OVERRIDE_HITS']})
    return result


if __name__=='__main__':
    raise SystemExit(main())
