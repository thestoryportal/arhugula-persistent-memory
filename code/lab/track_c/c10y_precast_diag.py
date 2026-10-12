"""D-C10y-precast, FROZEN v2. Import is model-free. Use the external launcher.

No behavioral readout, optimizer, calibration continuation or corrective execution.
"""
import os, sys
LLMDB_ROOT = os.environ.get('LLMDB_ROOT', str(__import__('pathlib').Path(__file__).resolve().parents[3]))
import argparse, ast, contextlib, copy, hashlib, importlib, importlib.util, inspect, itertools, json, re, signal, time, traceback
from pathlib import Path
import c10y_directdw_arms as A

ROOT = Path(LLMDB_ROOT).resolve()
SCOPE_SHA = '097c662803a94a897dd588c9e1f09c6af7b17a25019c1439ea39844c65f0a9a8'
CONTEXT_SHA = '9472b663a34cfd9c0bb5448087ae0c2c333b1988b70f211fb2d90baaf8b560b7'
CAP_SECONDS = 2820
ARMS = ('A7_coined_coined', 'A1_single')
LAYERS = tuple(range(4,9))
REQUIREMENTS = ('capture','source_identity','observer','persistence','finiteness','resource','deadline','cleanup')
PHASES = ('setup','model_load','pristine','projectors',*(s+'_'+a for a in ARMS for s in ('targets','native','controls')),'cleanup')
SOURCE_PINS = {
    'experiments/c10y/design/C10Y_PRECAST_DIAG_SCOPE.md': SCOPE_SHA,
    'experiments/c10y/design/C10Y_DIRECTDW_PREREG.md': '005391a39e31d8174419de3e39078a42209ded1b7ab8caaf098d5d8a4f755004',
    'code/lab/track_c/c10y_directdw_arms.py': 'ead3cef2266a7c81035e5acb6c3a97b42f83da556ba093a9fd28ec403f7e158c',
    'code/lab/track_c/c10e_bandknob.py': '1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695',
    'code/lab/track_c/c10z_astra_benchmark.py': '3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041',
    'code/configs/hparams/qwen25_3b_memit_hparams.json': '4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4',
    'code/configs/screens/g6_screen_qwen3b_v2.json': '482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c',
    'code/memit/vendor/memit/compute_z.py': 'd94af7fa14e5a4a20d5fa6361e0cbb30da0ff957db31922557ff809c34205dea',
    'code/memit/vendor/memit/compute_ks.py': '0b039be47c548f046b71cad4efce63414f53edbaa657bde868a20cdd35a2f5c7',
    'code/memit/vendor/rome/repr_tools.py': 'd4c2324ba20cbcce7f4ccfcf58ad002912edf0ad2fc72ab4e9bf46cc9dfed336',
    'code/memit/vendor/memit/memit_main.py': A.ENGINE_SHA,
    'code/memit/engine_fingerprint.py': '450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162',
    'code/lab/runners/c10w_p2_gate.py': 'fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26',
}

def fsync_directory(directory):
    fd=os.open(directory,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)

class Journal:
    """The recordfix encoder and exclusive writers, with directory durability."""
    def __init__(self, directory): self.directory=Path(directory).resolve()

    def record(self,name,value):
        if not re.fullmatch(r'[A-Za-z0-9_-]+',name): raise A.Halt('RECORD-NAME',name)
        path=self.directory/(name+'.json');sidecar=path.with_suffix('.pt')
        for candidate in (path,sidecar):
            if candidate.exists() or candidate.is_symlink(): raise A.Halt('EXISTING-ARTIFACT',str(candidate))
        tensors={};payload=A._record_value(value,tensors,sidecar.name)
        if tensors:
            payload['artifacts']={sidecar.name:A.save_tensors(sidecar,tensors)}
            fsync_directory(self.directory)
        A.write_json(path,payload);fsync_directory(self.directory)
        return path

    def gate(self,name,inputs,predicate,code):
        path=self.record(name,inputs)
        retained=load_record(path)
        passed=bool(predicate(retained))
        self.record(name+'_outcome',{'passed':passed,'input':path.name,'input_sha256':A.sha(path)})
        if not passed: raise A.Halt(code,inputs)
        return retained

    def finite(self,name,value):
        def finite(v):
            import torch
            if isinstance(v,torch.Tensor): return bool(torch.isfinite(v).all())
            if isinstance(v,dict): return all(finite(x) for x in v.values())
            if isinstance(v,(tuple,list)): return all(finite(x) for x in v)
            if isinstance(v,float): return __import__('math').isfinite(v)
            return True
        return self.gate(name,value,finite,'NONFINITE')

    @contextlib.contextmanager
    def phase(self,name):
        self.record('phase_'+name+'_started',{'phase':name,'status':'INCOMPLETE','at':A.utc()})
        try: yield
        except BaseException as error:
            # The start record remains authoritative if the failed sink cannot be used.
            if not isinstance(error,OSError) and not (isinstance(error,A.Halt) and error.code=='EXISTING-ARTIFACT'):
                try:
                    self.record('phase_'+name+'_failed',{'phase':name,'status':'INCOMPLETE','code':getattr(error,'code','INSTRUMENT-ERROR'),
                                                      'detail':str(error),'traceback':traceback.format_exc()})
                except BaseException as record_error:
                    error.add_note('Phase failure publication failed: '+repr(record_error))
            raise
        else: self.record('phase_'+name+'_complete',{'phase':name,'status':'COMPLETED','at':A.utc()})

def load_record(path):
    path=Path(path);payload=A.strict_load(path);tensors={}
    for name,expected in payload.get('artifacts',{}).items():
        sidecar=path.parent/name
        if sidecar.parent!=path.parent or A.sha(sidecar)!=expected: raise A.Halt('PERSISTENCE',name)
        import torch
        tensors[name]=torch.load(sidecar,map_location='cpu',weights_only=True)
    def decode(value):
        if isinstance(value,dict):
            if 'tensor_artifact' in value:
                t=tensors[value['tensor_artifact']][value['key']]
                if str(t.dtype)!=value['dtype'] or list(t.shape)!=value['shape']: raise A.Halt('PERSISTENCE',value)
                return t
            if 'nonfinite_float' in value: return float(value['nonfinite_float'].replace('+inf','inf'))
            return {k:decode(v) for k,v in value.items() if k!='artifacts'}
        if isinstance(value,list): return [decode(v) for v in value]
        return value
    return decode(payload)

def load_packet(path): return load_record(Path(path).with_suffix('.json'))

def phase_summary(directory,names=PHASES):
    directory=Path(directory);result={}
    for name in names:
        complete=directory/('phase_'+name+'_complete.json');start=directory/('phase_'+name+'_started.json')
        status='COMPLETED' if complete.exists() else 'INCOMPLETE' if start.exists() else 'NOT-RUN'
        result[name]={'status':status,'record':complete.name if complete.exists() else start.name if start.exists() else None}
    return result

def verify_scope(root):
    actual=A.sha(Path(root)/'experiments/c10y/design/C10Y_PRECAST_DIAG_SCOPE.md')
    if actual!=SCOPE_SHA: raise A.Halt('SCOPE-SHA',{'expected':SCOPE_SHA,'actual':actual})
    return actual

def claim_namespace(root,utc,supervisor_pid):
    if not re.fullmatch(r'\d{8}T\d{6}(?:\.\d{6})?Z',utc): raise A.Halt('UTC-NAMESPACE',utc)
    parent=Path(root).resolve()/'experiments/c10y/runs/c10y_precast_diag'
    if parent.resolve()!=parent: raise A.Halt('NAMESPACE-SYMLINK',str(parent))
    parent.mkdir(parents=True,exist_ok=True)
    out=parent/utc
    try: out.mkdir()
    except FileExistsError as error: raise A.Halt('EXISTING-NAMESPACE',str(out)) from error
    fsync_directory(parent)
    Journal(out).record('launch',{'schema':'c10y_precast_launch/v1','supervisor_pid':supervisor_pid,'at':A.utc(),
                                'scope_sha256':SCOPE_SHA,'cap_s':CAP_SECONDS,'decision_id':'D-C10y-precast'})
    return out

def classify(evidence):
    req=evidence.get('requirements',{}) if isinstance(evidence,dict) else {}
    cells=evidence.get('cells',[]) if isinstance(evidence,dict) else []
    expected={(a,l) for a in ARMS for l in LAYERS}
    valid=isinstance(req,dict) and isinstance(cells,list) and len(cells)==10
    valid=valid and all(isinstance(c,dict) and isinstance(c.get('arm'),str) and type(c.get('layer')) is int for c in cells)
    valid=valid and {(c['arm'],c['layer']) for c in cells}==expected
    valid=valid and all(all(type(c.get(k)) is bool for k in ('operands_equal','states_equal','repeats_stable','cpu_realized_identical','mps_realized_identical')) and isinstance(c.get('discrepancies'),list) and all(isinstance(d,dict) for d in c['discrepancies']) for c in cells)
    if not valid or any(req.get(k) is not True for k in REQUIREMENTS):
        return {'label':'INCONCLUSIVE','reason':'A required capture, validation, persistence, resource, cleanup or deadline requirement failed.'}
    if all(c['operands_equal'] and c['states_equal'] and c['repeats_stable'] and c['cpu_realized_identical'] for c in cells) and any(c['arm']==ARMS[0] and not c['mps_realized_identical'] for c in cells):
        return {'label':'R','reason':'CPU-fp32 product removes the realized-weight mismatch on these NEW COMPUTATION inputs.',
                'boundary':'No calibration-4 causation or exclusive mechanism is established; no redesign or dispatch is admitted.'}
    direct=[d for c in cells for d in c['discrepancies'] if d.get('kind') in ('operand','state','orientation','formula') and all(d.get(k) for k in ('field','left','right'))]
    if direct: return {'label':'S','reason':'Validated native traces directly show an operative discrepancy.','evidence':direct}
    return {'label':'UNCLASSIFIED','reason':'Remaining numerical, conditioning or mixed mechanisms; descriptive measurements only.'}

def cpu_copy(tensor): return tensor.detach().cpu().clone()

def tensor_meta(tensor):
    return {'dtype':str(tensor.dtype),'shape':list(tensor.shape),'sha256':A.tensor_sha(tensor),'orientation':'as captured'}

def assignment_lines(function,name):
    source=Path(function.__code__.co_filename).read_text();tree=ast.parse(source)
    nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name==function.__name__]
    node=next(n for n in nodes if n.lineno<=function.__code__.co_firstlineno<=n.end_lineno)
    return [n.lineno for n in ast.walk(node) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]

def native_globals(H):
    return {'DEV':str(H.DEV),'L2':H.L2,'PROJECTOR':H.PROJECTOR,'_CANDIDATE_RECIPE':H._CANDIDATE_RECIPE,
            '_LAW5_DEFAULT_CTX':H._LAW5_DEFAULT_CTX,'contexts':copy.deepcopy(H.get_context_templates.__globals__.get('CONTEXT_TEMPLATES_CACHE')),
            'hparams':copy.deepcopy(vars(H.hp)),'default_dtype':str(__import__('torch').get_default_dtype()),
            'padding_side':getattr(H.tok,'padding_side',None),'training':H.model.training}

@contextlib.contextmanager
def restored(H,pristine=None):
    import torch
    weights=dict(H.model.named_parameters());snap=H.snap_layers(H.hp) if pristine is None else pristine
    names=('Z_OVERRIDE','Z_OVERRIDE_HITS','_LAW5_DEFAULT_CTX','_CANDIDATE_RECIPE','PROJECTOR','_ARM_STATE','ARM_HOOKS',
           '_C10Y_PREFIX_SAVE','_C10Y_MEMORY','_PRECAST_REPR')
    attrs={name:copy.deepcopy(getattr(H,name)) if name=='_C10Y_MEMORY' else getattr(H,name) for name in names if hasattr(H,name)}
    registries=[(getattr(m,name),tuple(getattr(m,name).items())) for m in H.model.modules() for name in ('_forward_hooks','_forward_pre_hooks','_backward_hooks','_backward_pre_hooks') if hasattr(m,name)]
    flags={p:(p.requires_grad,p.grad) for p in H.model.parameters()};training={m:m.training for m in H.model.modules()}
    cg=H.get_context_templates.__globals__;had='CONTEXT_TEMPLATES_CACHE' in cg;old=cg.get('CONTEXT_TEMPLATES_CACHE')
    cov=H.get_cov.__globals__.get('COV_CACHE') if hasattr(H,'get_cov') else None
    cov_before=dict(cov) if cov is not None else None
    try: yield
    finally:
        with torch.no_grad():
            if pristine is None: H.restore_layers(H.hp,snap)
            else:
                for name,t in snap.items(): weights[name].copy_(A.to_like(t,weights[name]))
        for name in names:
            if name in attrs:setattr(H,name,attrs[name])
            elif hasattr(H,name):delattr(H,name)
        for registry,entries in registries: registry.clear();registry.update(entries)
        for p,(flag,grad) in flags.items():p.requires_grad_(flag);p.grad=grad
        for m,value in training.items(): m.training=value
        if had: cg['CONTEXT_TEMPLATES_CACHE']=old
        else: cg.pop('CONTEXT_TEMPLATES_CACHE',None)
        if cov is not None:cov.clear();cov.update(cov_before)
        actual=H.snap_layers(H.hp) if pristine is None else dict(H.model.named_parameters())
        if any(A.tensor_sha(actual[k])!=A.tensor_sha(v) for k,v in snap.items()):raise A.Halt('RESTORATION')

class NativeObserver:
    """Read-only tracing of original code objects; missing locals stop the probe."""
    def __init__(self,H,journal,arm,path):
        self.H,self.j,self.arm,self.path=H,journal,arm,path
        self.edit=H.my_edit if path=='A' else A.capture_solve
        self.edit_code=self.edit.__code__;self.shape_code=H.upd_matrix_match_shape.__code__
        self.factor_code=A.factor_solve.__code__
        self.key_line=min(assignment_lines(self.edit,'K'))
        self.solve_line=min(assignment_lines(self.edit,'upd'))
        self.factor_solve_line=min(assignment_lines(A.factor_solve,'X'))
        self.pre={};self.q={};self.q_live={};self.q_meta={};self.inputs={};self.solve_calls={};self.factor_assembled={}
        self.failed_frames=set();self.batches={};self.layers=[];self.returns=0;self.factor_count=0;self.current=None
        self.batch_code=None
        if hasattr(H,'_PRECAST_REPR'):
            fn=H._PRECAST_REPR.get_reprs_at_idxs;self.batch_code=fn.__code__
            assigned=min(assignment_lines(fn,'contexts_tok'))
            node=next(n for n in ast.walk(ast.parse(Path(fn.__code__.co_filename).read_text())) if isinstance(n,ast.FunctionDef) and n.name==fn.__name__)
            self.batch_ready=min(n.lineno for n in ast.walk(node) if isinstance(n,ast.Expr) and
                                 isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and
                                 n.value.func.id=='model' and n.lineno>assigned)

    def native_frame(self):
        frame=inspect.currentframe().f_back
        while frame is not None and frame.f_code not in (self.edit_code,self.factor_code):frame=frame.f_back
        return frame

    def retain(self,name,fields,extra=None):
        before={k:tensor_meta(t) for k,t in fields.items()}
        tensors={k:cpu_copy(t) for k,t in fields.items()}
        self.j.finite(name,{**tensors,**(extra or {}),'tensor_metadata':before})
        self.j.gate(name+'_tensor_inertness',{'before':before,'after':{k:tensor_meta(t) for k,t in fields.items()},
                                            'retained':{k:tensor_meta(t) for k,t in tensors.items()}},
                    lambda x:x['before']==x['after']==x['retained'],'OBSERVER-TENSOR-INERTNESS')
        return {'fields':fields,'before':before,'record':name+'.json','tensors':tensors}

    def check_inputs(self,layer,kind,checkpoint,fields=None):
        saved=self.inputs[(layer,kind)]
        self.j.gate(saved['record'][:-5]+'_'+checkpoint,{'input':saved['record'],'before':saved['before'],
                    'after':{k:tensor_meta(t) for k,t in (fields or saved['fields']).items()}},
                    lambda x:x['before']==x['after'],'OBSERVER-SOLVE-INPUT')

    def check_q(self,layer,label,checkpoint):
        copied=self.q.get((layer,label));live=self.q_live.get((layer,label))
        self.j.gate('q_identity_'+self.arm+'_L%d_'%layer+self.path+'_'+label+'_'+checkpoint,
                    {'before':self.q_meta.get((layer,label)),'live':tensor_meta(live) if live is not None else None,
                     'copy':tensor_meta(copied) if copied is not None else None},
                    lambda x:x['before'] is not None and x['before']==x['live']==x['copy'],
                    'OBSERVER-COVERAGE' if copied is None else 'OBSERVER-SOLVE-INPUT')

    def direct_fields(self,values,layer):
        return {'K':values['K'],'K32':values['Kf'],'cur':values['cur'],'allocated_residual':values['resid'],
                'R':values['rf'],'P':values['Pi'],'C':values['ca'],
                'M':values['A'] if self.path=='A' else values['matrix'],
                'B':values['B'] if self.path=='A' else values['rhs'],
                'Q':self.q.get((layer,'Q')),'W0':dict(self.H.model.named_parameters())[self.H.weight_name(self.H.hp,layer)]}

    def solve_event(self,func,args,checkpoint):
        if str(func)!='aten._linalg_solve_ex.default':return
        frame=self.native_frame()
        if frame is None:return
        kind='direct' if frame.f_code is self.edit_code else 'factor'
        parent=frame if kind=='direct' else frame.f_back
        if parent is None or parent.f_code is not self.edit_code:return
        layer=parent.f_locals['layer'];saved=self.inputs.get((layer,kind))
        if saved is None:raise A.Halt('OBSERVER-COVERAGE',{'layer':layer,'solve':kind,'checkpoint':checkpoint})
        actual={**saved['fields'],'M':args[0],'RHS':args[1]}
        if kind=='direct':actual['B']=args[1]
        self.check_inputs(layer,kind,checkpoint,actual)
        self.check_q(layer,'Q' if kind=='direct' else 'factor_Q',checkpoint)
        if checkpoint=='at_execution':self.solve_calls[(layer,kind)]=self.solve_calls.get((layer,kind),0)+1

    def failed(self,frame,arg):
        import torch
        error=arg[1];self.failed_frames.add(frame)
        kind='edit' if frame.f_code is self.edit_code else 'factor' if frame.f_code is self.factor_code else 'shape'
        layer=frame.f_locals.get('layer',frame.f_back.f_locals.get('layer',self.current) if frame.f_back is not None else self.current)
        try:
            self.j.record('native_exception_'+self.arm+'_L%s_'%layer+self.path+'_'+kind,
                          {'status':'INCOMPLETE','exception':type(error).__name__,'detail':str(error),
                           'traceback':''.join(traceback.format_exception(*arg)),
                           'locals':{k:cpu_copy(t) for k,t in frame.f_locals.items() if isinstance(t,torch.Tensor)},
                           'available_local_names':list(frame.f_locals),'filename':frame.f_code.co_filename,'line':frame.f_lineno})
        except BaseException as record_error:
            error.add_note('Native exception locals publication failed: '+repr(record_error))

    def mm(self,func,args,result):
        if str(func)!='aten.mm.default': return
        frame=self.native_frame()
        if frame is None:return
        values=frame.f_locals
        if frame.f_code is self.edit_code:
            pi=values.get('Pi');k=values.get('Kf');layer=values.get('layer')
        else:
            pi=values.get('p');k=values.get('k');parent=frame.f_back
            if parent is None or parent.f_code is not self.edit_code:return
            layer=parent.f_locals.get('layer')
        if args[0] is pi and k is not None and tuple(args[1].shape)==tuple(k.shape):
            label='Q' if frame.f_code is self.edit_code else 'factor_Q'
            captured=self.retain('intermediate_'+self.arm+'_L%d_'%layer+self.path+'_'+label,
                                 {'value':result,'input_left':args[0],'input_right':args[1]})
            self.q[(layer,label)]=captured['tensors']['value'];self.q_live[(layer,label)]=result
            self.q_meta[(layer,label)]=captured['before']['value']
            if label=='factor_Q':
                fields={'K':values['k'],'R':values['r'],'P':values['p'],'C':values['cache'],'M':values['matrix'],'RHS':result}
                name='solve_inputs_'+self.arm+'_L%d_Y_factor'%layer
                self.inputs[(layer,'factor')]=self.retain(name,fields,{'L2':values['l2']})
                self.inputs[(layer,'factor')].pop('tensors')
                self.j.gate(name+'_assembly_inertness',{'before':self.factor_assembled[layer],
                            'after':{k:tensor_meta(t) for k,t in fields.items() if k!='RHS'}},
                            lambda x:x['before']==x['after'],'OBSERVER-SOLVE-INPUT')

    def trace(self,frame,event,arg):
        native=frame.f_code is self.edit_code or (frame.f_code in (self.factor_code,self.shape_code) and
                                                 frame.f_back is not None and frame.f_back.f_code is self.edit_code)
        if native and event=='exception':self.failed(frame,arg);return self.trace
        if native and event=='return' and arg is None and frame in self.failed_frames:return self.trace
        if frame.f_code is self.edit_code:
            if event=='line' and frame.f_lineno==self.key_line:
                l=frame.f_locals['layer'];self.current=l
                self.pre[l]={'weights':A.band_hashes(self.H,self.H.hp),'globals':native_globals(self.H)}
                self.batches[l]=[]
            if event=='line' and frame.f_lineno==self.solve_line:
                v=frame.f_locals;l=v['layer'];fields=self.direct_fields(v,l)
                if any(t is None for t in fields.values()):
                    self.j.record('operands_'+self.arm+'_L%d_'%l+self.path+'_incomplete',
                                  {k:cpu_copy(t) if t is not None else None for k,t in fields.items()})
                    raise A.Halt('OBSERVER-COVERAGE',{'layer':l,'missing':[k for k,t in fields.items() if t is None]})
                fields['RHS']=fields['B']
                self.inputs[(l,'direct')]=self.retain('solve_inputs_'+self.arm+'_L%d_'%l+self.path+'_direct',fields,
                                                     {'L2':self.H.L2,'state':self.pre[l],'batches':self.batches[l],
                                                      'requests':copy.deepcopy(v['requests'])})
                self.inputs[(l,'direct')].pop('tensors')
                self.check_q(l,'Q','before_solve')
            if event=='return':self.returns+=1
            return self.trace
        if frame.f_code is self.shape_code and event!='return': return self.trace
        if frame.f_code is self.shape_code and event=='return' and frame.f_back is not None and frame.f_back.f_code is self.edit_code:
            parent=frame.f_back;v=parent.f_locals;l=v['layer']
            fields={**self.direct_fields(v,l),'direct_solution':v['upd'].T,'update':arg}
            name='operands_'+self.arm+'_L%d_'%l+self.path
            if any(x is None for x in fields.values()) or l in self.layers:
                self.j.record(name+'_incomplete',{k:cpu_copy(t) if t is not None else None for k,t in fields.items()})
                raise A.Halt('OBSERVER-COVERAGE',{'layer':l,'missing':[k for k,t in fields.items() if t is None]})
            before={k:A.tensor_sha(t) for k,t in fields.items()}
            tensors={k:cpu_copy(t) for k,t in fields.items()}
            after={k:A.tensor_sha(t) for k,t in fields.items()}
            packet={**tensors,'L2':self.H.L2,'state':self.pre[l],'batches':self.batches[l],
                    'requests':copy.deepcopy(v['requests']),'orientation':{'update':'out_features x in_features','K':'in_features x requests','R':'out_features x requests'},
                    'tensor_metadata':{k:tensor_meta(t) for k,t in tensors.items()},
                    'source':{'filename':self.edit_code.co_filename,'first_line':self.edit_code.co_firstlineno,'original_code_object':True}}
            self.j.finite(name,packet)
            self.j.gate(name+'_tensor_inertness',{'before':before,'after':after},lambda x:x['before']==x['after'],'OBSERVER-TENSOR-INERTNESS')
            self.check_inputs(l,'direct','at_return',{**self.direct_fields(v,l),'RHS':fields['B']})
            self.check_q(l,'Q','at_return')
            self.j.gate(name+'_solve_coverage',{'calls':self.solve_calls.get((l,'direct'),0)},lambda x:x['calls']==1,'OBSERVER-COVERAGE')
            del self.inputs[(l,'direct')]
            self.layers.append(l);self.current=None
            return self.trace
        if frame.f_code is self.factor_code:
            if native and event=='line' and frame.f_lineno==self.factor_solve_line:
                l=frame.f_back.f_locals['layer'];v=frame.f_locals
                self.factor_assembled[l]={k:tensor_meta(t) for k,t in
                                          {'K':v['k'],'R':v['r'],'P':v['p'],'C':v['cache'],'M':v['matrix']}.items()}
            if event=='return' and frame.f_back is not None and frame.f_back.f_code is self.edit_code:
                l=frame.f_back.f_locals['layer'];v=frame.f_locals
                fields={**arg,'M':v['matrix'],'Q':self.q.get((l,'factor_Q'))}
                if fields['Q'] is None:
                    self.j.record('factors_'+self.arm+'_L%d_Y_incomplete'%l,fields)
                    raise A.Halt('OBSERVER-COVERAGE',{'layer':l,'missing':['factor_Q']})
                self.retain('factors_'+self.arm+'_L%d_Y'%l,fields)
                self.check_inputs(l,'factor','at_return',{**self.inputs[(l,'factor')]['fields'],'M':v['matrix']})
                self.check_q(l,'factor_Q','at_return')
                self.j.gate('factor_coverage_'+self.arm+'_L%d'%l,{'Q_present':self.q.get((l,'factor_Q')) is not None},lambda x:x['Q_present'],'OBSERVER-COVERAGE')
                self.j.gate('factor_solve_coverage_'+self.arm+'_L%d'%l,{'calls':self.solve_calls.get((l,'factor'),0)},lambda x:x['calls']==1,'OBSERVER-COVERAGE')
                del self.inputs[(l,'factor')]
                self.factor_count+=1
            return self.trace
        if self.batch_code is not None and frame.f_code is self.batch_code and self.current is not None:
            v=frame.f_locals
            if event=='line' and frame.f_lineno==self.batch_ready:
                name='batch_'+self.arm+'_L%d_'%self.current+self.path+'_%d'%len(self.batches[self.current])
                self.j.finite(name,{'tokens':dict(v['contexts_tok']),'contexts':v['batch_contexts'],'idxs':v['batch_idxs'],
                                    'padding_side':self.H.tok.padding_side,'layer':v['layer'],'track':v['track']})
                self.batches[self.current].append(name+'.json')
            return self.trace
        return None

    def __enter__(self):
        from torch.utils._python_dispatch import TorchDispatchMode
        observer=self
        class Observe(TorchDispatchMode):
            def __torch_dispatch__(self,func,types,args=(),kwargs=None):
                observer.solve_event(func,args,'at_execution')
                value=func(*args,**(kwargs or {}))
                observer.solve_event(func,args,'after_execution');observer.mm(func,args,value);return value
        self.previous=sys.gettrace()
        if self.previous is not None:raise A.Halt('OBSERVER-EXISTING-TRACE')
        self.mode=Observe();self.mode.__enter__();sys.settrace(self.trace);return self

    def __exit__(self,*error):
        sys.settrace(self.previous);self.mode.__exit__(*error)

    def validate(self):
        passed=self.layers==list(self.H.hp.layers) and self.returns==1 and (self.path=='A' or self.factor_count==len(self.layers))
        if self.batch_code is not None: passed=passed and all(len(self.batches[l])>=2 for l in self.layers)
        self.j.gate('coverage_'+self.arm+'_'+self.path,{'layers':self.layers,'returns':self.returns,'factor_count':self.factor_count,
                                                     'batches':self.batches,'passed':passed},lambda x:x['passed'],'OBSERVER-COVERAGE')

def exact(value,other):
    import torch
    if isinstance(value,torch.Tensor):return isinstance(other,torch.Tensor) and str(value.dtype)==str(other.dtype) and tuple(value.shape)==tuple(other.shape) and A.tensor_sha(value)==A.tensor_sha(other)
    if isinstance(value,dict):return isinstance(other,dict) and set(value)==set(other) and all(exact(v,other[k]) for k,v in value.items())
    if isinstance(value,(tuple,list)):return isinstance(other,(tuple,list)) and len(value)==len(other) and all(exact(a,b) for a,b in zip(value,other))
    return value==other

def native_capture(H,requests,P,journal,arm):
    import torch
    for path in ('A','Y'):
        fn=(lambda cache:H.my_edit(H.hp,requests,P,cache)) if path=='A' else (lambda cache:A.capture_solve(H,H.hp,requests,P,cache))
        snapshots={}
        # Retain the observed operands first so a later unobserved control failure cannot erase them.
        for on in (True,False):
            with restored(H):
                H.Z_OVERRIDE_HITS=0;H._LAW5_DEFAULT_CTX=False;H._CANDIDATE_RECIPE=False
                cache=[torch.zeros_like(p,dtype=torch.float32,device='cpu') for p in P]
                observer=NativeObserver(H,journal,arm,path) if on else None
                with observer if on else contextlib.nullcontext(): result=fn(cache)
                snap={'weights':{str(l):cpu_copy(t) for l,t in H.snap_layers(H.hp).items()},'cache':[cpu_copy(t) for t in cache],
                      'result':result,'hits':H.Z_OVERRIDE_HITS,'globals':native_globals(H)}
                journal.finite('observer_'+arm+'_'+path+('_on' if on else '_off'),snap)
                snapshots['on' if on else 'off']=snap
                if on:observer.validate()
        journal.gate('inertness_'+arm+'_'+path,snapshots,lambda x:exact(x['off'],x['on']),'OBSERVER-INERTNESS')
    cells=[]
    for l in H.hp.layers:
        left='operands_'+arm+'_L%d_A.pt'%l;right='operands_'+arm+'_L%d_Y.pt'%l
        a,b=load_packet(journal.directory/left),load_packet(journal.directory/right)
        factors=load_record(journal.directory/('factors_'+arm+'_L%d_Y.json'%l))
        fields=('K','K32','cur','allocated_residual','R','P','C','L2','M','Q','B','requests')
        ds=[{'kind':'operand','field':k,'left':left,'right':right} for k in fields if not exact(a[k],b[k])]
        for field,reference in (('M',b['M']),('Q',b['Q']),('R',b['R']),('A0',b['R'])):
            if not exact(factors[field],reference):ds.append({'kind':'operand','field':'factor_'+field,'left':right,'right':'factors_'+arm+'_L%d_Y.pt'%l})
        if not exact(a['orientation'],b['orientation']):ds.append({'kind':'orientation','field':'orientation','left':left,'right':right})
        batches_a=[load_record(journal.directory/p) for p in a['batches']]
        batches_b=[load_record(journal.directory/p) for p in b['batches']]
        states=exact(a['state'],b['state']) and exact(a['W0'],b['W0']) and exact(batches_a,batches_b)
        if not states:ds.append({'kind':'state','field':'pre_layer_state/batches','left':left,'right':right})
        cells.append({'arm':arm,'layer':l,'operands_equal':not any(d['kind']=='operand' for d in ds),'states_equal':states,'discrepancies':ds})
    journal.record('native_comparison_'+arm,{'cells':cells})
    return {'cells':cells,'observer_validated':True}

def controls(packet,journal,prefix):
    import torch
    k,r,p,c=packet.get('K32',packet['K']).float(),packet['R'].float(),packet['P'].float(),packet['C'].float()
    x=packet['X'];m,q,b=packet['M'],packet['Q'],packet['B']
    journal.finite(prefix+'_control_inputs',packet)
    result={}
    def save(name,tensor):
        journal.finite(prefix+'_'+name,{'update':tensor});result[name]=tensor;return tensor
    save('cpu32_product',r@x.T)
    save('promoted32_product',r.double()@x.double().T)
    k64,r64,p64,c64=k.double(),r.double(),p.double(),c.double()
    m64=p64@(k64@k64.T+c64)+packet['L2']*torch.eye(k.shape[0],dtype=torch.float64)
    q64=p64@k64;b64=q64@r64.T
    journal.finite(prefix+'_system64',{'M':m64,'Q':q64,'B':b64,'R':r64,'assembly':'operands promoted BEFORE assembly'})
    direct64=torch.linalg.solve(m64,b64)
    journal.finite(prefix+'_direct_solution64',{'solution':direct64})
    factor64=torch.linalg.solve(m64,q64)
    journal.finite(prefix+'_factor_solution64',{'X':factor64})
    save('solve64_direct',direct64.T);save('solve64_factored',r64@factor64.T)
    direct_assembled=torch.linalg.solve(m.double(),b.double())
    journal.finite(prefix+'_assembled32_direct_solution64',{'solution':direct_assembled})
    factor_assembled=torch.linalg.solve(m.double(),q.double())
    journal.finite(prefix+'_assembled32_factor_solution64',{'X':factor_assembled})
    save('assembled32_direct64',direct_assembled.T);save('assembled32_factored64',r64@factor_assembled.T)
    repeat_direct=torch.linalg.solve(m,b)
    journal.finite(prefix+'_direct_repeat',{'solution':repeat_direct})
    repeat_factor=A.factor_solve(k,r,p,c,packet['L2'])
    journal.finite(prefix+'_factor_repeat',repeat_factor)
    save('direct32_repeat',repeat_direct.T);save('factor32_repeat_product',r@repeat_factor['X'].T)
    save('cpu32_product_repeat',r@x.T)
    return result

def realize(W0,update):
    import torch
    if update.dtype==torch.float64:
        # MPS cannot hold fp64: round directly to fp16 on CPU, then move/add.
        return (W0.detach().half()+A.to_like(update.detach().cpu().half(),W0.detach().half())).half()
    return A.stored_weight(W0,update,1.)

def device_product(W0,r,b,journal,prefix,device):
    from torch.utils._python_dispatch import TorchDispatchMode
    code=A.effective_weight.__code__;captures=[]
    w=W0.to(device);a=r.to(device).float();b=b.to(device).float()
    journal.finite(prefix+'_inputs',{'W0':w,'A0':a,'B':b,'device':str(device),'formula':'c10y_directdw_arms.effective_weight'})
    class Product(TorchDispatchMode):
        def __torch_dispatch__(self,func,types,args=(),kwargs=None):
            value=func(*args,**(kwargs or {}))
            if str(func)=='aten.mm.default':
                frame=inspect.currentframe().f_back
                while frame is not None and frame.f_code is not code:frame=frame.f_back
                if frame is not None:
                    tensor=cpu_copy(value);journal.finite(prefix+'_product',{'update':tensor,'left':cpu_copy(args[0]),'right':cpu_copy(args[1])});captures.append(tensor)
            return value
    off=A.effective_weight(w,a,b)
    journal.finite(prefix+'_observer_off',{'weight':off})
    with Product(): on=A.effective_weight(w,a,b)
    journal.finite(prefix+'_observer_on',{'weight':on})
    journal.gate(prefix+'_coverage',{'n':len(captures),'off':off,'on':on},lambda x:x['n']==1 and exact(x['off'],x['on']),'OBSERVER-INERTNESS')
    return {'update':captures[0],'weight':cpu_copy(on),'realized_update':cpu_copy(on).double()-cpu_copy(W0).double()}

def distance_stats(x,y):
    import torch, numpy as np
    a,b=cpu_copy(x).double(),cpu_copy(y).double();delta=(a-b).abs()
    denominator=float(a.norm());numerator=float((a-b).norm());quantiles=(0.,.25,.5,.75,.9,.99,1.)
    # numpy avoids torch.quantile's 2**24-element limit on the model-sized weights.
    qs=np.quantile(delta.numpy(),quantiles);columns=np.quantile(delta.numpy(),quantiles,axis=0)
    return {'relative_frobenius':numerator/denominator if denominator else 0. if not numerator else None,
            'relative_undefined':'zero reference norm' if not denominator and numerator else None,
            'max_abs':float(delta.max()),'different_fraction':float((a!=b).double().mean()),
            'byte_identical':exact(x,y),'quantiles':{str(q):float(v) for q,v in zip(quantiles,qs)},'column_axis':'weight coordinates',
            'columns':{'l2':(a-b).norm(dim=0),'max_abs':delta.max(dim=0).values,
                       'different_fraction':(a!=b).double().mean(dim=0),'absolute_quantiles':torch.from_numpy(columns),'quantile_levels':list(quantiles)}}

def preload(journal,gate,loader):
    fingerprint=gate.check_fingerprint()
    journal.gate('preload_fingerprint',fingerprint,lambda x:x.get('ok') is True and bool(x.get('output')),'PRELOAD-FINGERPRINT')
    gpu=gate.check_gpu()
    journal.gate('preload_gpu',gpu,lambda x:x.get('ok') is True,'PRELOAD-GPU')
    # These two committed gates are the last actions before importing the load-on-import harness.
    return loader()

def source_identity(root):
    observed={p:A.sha(Path(root)/p) for p in SOURCE_PINS}
    own=('code/lab/track_c/c10y_precast_diag.py','code/lab/runners/run_c10y_precast_diag.sh')
    observed.update({p:A.sha(Path(root)/p) for p in own})
    for p in ('code/memit/vendor/util/device.py','code/memit/vendor/util/nethook.py','code/memit/vendor/memit/memit_hparams.py','code/memit/vendor/globals.yml'):
        observed[p]=A.sha(Path(root)/p)
    return observed

def input_manifest(root):
    root=Path(root);ctx=root/'experiments/c10y/runs/c10y_directdw_calib4/context_templates_calib.json'
    contexts=A.strict_load(ctx)
    if A.sha(ctx)!=CONTEXT_SHA or hashlib.sha256(json.dumps(contexts).encode()).hexdigest()!=A.PINNED_ENGINE_SHA:
        raise A.Halt('CONTEXT-PIN')
    model=root/'data/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots'/A.MODEL_REV
    names=('config.json','tokenizer.json','tokenizer_config.json','model.safetensors.index.json')
    files={str(model/n):A.sha(model/n) for n in names}
    index=A.strict_load(model/'model.safetensors.index.json')
    for n in sorted(set(index['weight_map'].values())):files[str(model/n)]=A.sha(model/n)
    caches={str(l):{'path':str((root/('data/covariance/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.%d.mlp.down_proj_float32_mom2_t100_100000.npz'%l)).resolve()),
                    'sha256':A.sha(root/('data/covariance/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.%d.mlp.down_proj_float32_mom2_t100_100000.npz'%l))} for l in LAYERS}
    return {'contexts':contexts,'context_file_sha256':CONTEXT_SHA,'context_harness_sha256':A.PINNED_ENGINE_SHA,
            'model_id':A.MODEL_ID,'revision':A.MODEL_REV,'input_file_sha256':files,'covariance':caches,'targets':'NEW COMPUTATION, solved once; historical placeholders never loaded'}

def compare_cell(H,journal,cell):
    import torch
    arm,l=cell['arm'],cell['layer'];prefix='controls_'+arm+'_L%d'%l
    a=load_packet(journal.directory/('operands_'+arm+'_L%d_A.pt'%l))
    native_direct=load_packet(journal.directory/('operands_'+arm+'_L%d_Y.pt'%l))
    factors=load_record(journal.directory/('factors_'+arm+'_L%d_Y.json'%l))
    packet={**a,'X':factors['X']}
    # Controlled arithmetic uses only the saved RECIPE-A packet; native factors are kept separately.
    matched=A.factor_solve(a['K32'],a['R'],a['P'],a['C'],a['L2'])
    journal.finite(prefix+'_common_factors',matched)
    packet['X']=matched['X'];updates={'recipe_A':a['update'],'native_direct':native_direct['update']}
    native=device_product(a['W0'],factors['R'],factors['B'],journal,prefix+'_native',H.DEV)
    native_cpu=factors['R']@factors['X'].T
    journal.finite(prefix+'_native_cpu32_product',{'update':native_cpu})
    native_cpu_repeat=factors['R']@factors['X'].T
    journal.finite(prefix+'_native_cpu32_product_repeat',{'update':native_cpu_repeat})
    common=device_product(a['W0'],a['R'],matched['B'],journal,prefix+'_common',H.DEV)
    repeated=device_product(a['W0'],factors['R'],factors['B'],journal,prefix+'_repeat',H.DEV)
    updates.update(native_device=native['update'],native_cpu32_product=native_cpu,native_cpu32_product_repeat=native_cpu_repeat,
                   common_device=common['update'],device_repeat=repeated['update'])
    updates.update(controls(packet,journal,prefix))
    journal.finite('updates_'+arm+'_L%d'%l,updates)
    realized={};realization_stats={}
    for name,u in updates.items():
        w=realize(a['W0'].to(H.DEV),u)
        value={'weight':cpu_copy(w),'realized_update':cpu_copy(w).double()-a['W0'].double(),
               'cast_add_device':str(H.DEV),'cast_device':'cpu' if u.dtype==torch.float64 else str(H.DEV),
               'order':'CPU fp64 -> CPU fp16 -> device fp16 -> add W0_fp16' if u.dtype==torch.float64 else 'update -> device (same dtype) -> fp16 -> add W0_fp16',
               'fp32_demotion':False if u.dtype==torch.float64 else 'native fp32 input'}
        journal.finite(prefix+'_realized_'+name,value);realized[name]=value['weight']
    pairs={}
    for left,right in itertools.combinations(updates,2):
        value=distance_stats(updates[left],updates[right]);key=left+'__'+right
        name=prefix+'_compare_'+key;journal.finite(name,value);pairs[key]=name+'.json'
    for name,w in realized.items():
        value=distance_stats(realized['recipe_A'],w);value['different_fp16_elements']=int((realized['recipe_A']!=w).sum())
        record_name=prefix+'_weight_compare_'+name;journal.finite(record_name,value);realization_stats[name]=record_name+'.json'
    m,q,b=a['M'].double(),a['Q'].double(),a['B'].double()
    def residual(matrix,solution,rhs):
        den=float(matrix.norm()*solution.double().norm()+rhs.norm());num=float((matrix@solution.double()-rhs).norm())
        return num/den if den else 0. if num==0 else None
    condition={'recipe_A':float(torch.linalg.cond(m,p=2)),'C10Y':float(torch.linalg.cond(factors['M'].double(),p=2))}
    numeric={'condition_numbers':condition,'norm':'2/spectral','method':'torch.linalg.cond(M_cpu_float64,p=2), SVD ratio',
             'direct_normalized_residual':residual(m,a['direct_solution'],b),'factor_normalized_residual':residual(factors['M'].double(),factors['X'],factors['Q'].double()),
             'normalization':'||M X - RHS||_F / (||M||_F ||X||_F + ||RHS||_F)',
             'float64_errors':{candidate:{name:distance_stats(updates[name],updates[candidate]) for name in ('solve64_direct','solve64_factored','assembled32_direct64','assembled32_factored64')}
                               for candidate in ('recipe_A','native_cpu32_product','native_device')},
             'pairs':pairs,'realized_weights':realization_stats}
    journal.finite(prefix+'_numeric',numeric)
    repeat_factor=load_record(journal.directory/(prefix+'_factor_repeat.json'))
    stable=exact(a['direct_solution'],updates['direct32_repeat'].T) and exact(factors['X'],matched['X']) and exact(factors['X'],repeat_factor['X']) and exact(updates['cpu32_product'],updates['cpu32_product_repeat']) and exact(native_cpu,native_cpu_repeat) and exact(native['update'],repeated['update'])
    return {**cell,'repeats_stable':stable,'cpu_realized_identical':exact(realized['recipe_A'],realized['native_cpu32_product']),
            'mps_realized_identical':exact(realized['recipe_A'],realized['native_device']),'measurements':prefix+'_numeric.json'}

def compute_targets(H,journal,requests,contexts,pristine):
    targets={}
    for arm in ARMS:
        with journal.phase('targets_'+arm):
            for i,rq in enumerate(requests[arm]):
                A.sample_memory(H,'precast_target')
                value=H.compute_z(H.model,H.tok,rq,H.hp,H.hp.layers[-1],contexts)
                journal.finite('target_'+arm+'_%02d'%i,{'request':rq,'value':value,'status':'NEW COMPUTATION'})
                targets[(rq['subject'],rq['target_new']['str'])]=cpu_copy(value)
                journal.gate('target_pristine_'+arm+'_%02d'%i,{'actual':{n:A.tensor_sha(t) for n,t in H.model.named_parameters()},'expected':{n:A.tensor_sha(t) for n,t in pristine.items()}},lambda x:x['actual']==x['expected'],'TARGET-BASE-MUTATION')
    journal.finite('targets',{'targets':[{'subject':s,'target':t,'value':v} for (s,t),v in targets.items()],'status':'NEW COMPUTATION'})
    return {(r['subject'],r['target']):r['value'] for r in load_record(journal.directory/'targets.json')['targets']}

def worker(out):
    import torch
    j=Journal(out);H=None;reading={'requirements':{k:False for k in REQUIREMENTS},'cells':[]};sources=None;serial=[0]
    try:
        with j.phase('setup'):
            verify_scope(ROOT);sources=source_identity(ROOT)
            j.gate('source_identity',{'expected':SOURCE_PINS,'observed':sources},lambda x:all(x['observed'][p]==v for p,v in x['expected'].items()),'SOURCE-IDENTITY')
            forbidden=('C10_PROJECTOR','N_EDIT','C10_SUBJECT_OFFSET','C10_CTX_TEMPLATES','C10_ARMS','C10_KEY_LOCUS','HP_CANDIDATE','C10_RECIPES','CANDIDATE_NAME','OUT','DECISION_ID','PREREG','RUN_LABEL','LLMDB_DEVICE','C10Y_TELEMETRY','C10Y_TELEMETRY_INERTNESS')
            j.gate('environment',{'inherited':{k:os.environ[k] for k in forbidden if k in os.environ}},lambda x:not x['inherited'],'INHERITED-KNOB')
            manifest=input_manifest(ROOT)
            manifest.update(schema='c10y_precast_manifest/v1',sources=sources,scope_sha256=SCOPE_SHA,cap_s=CAP_SECONDS,
                            versions=A.environment_identity(),device='mps',classification_order=['INCONCLUSIVE','R','S','UNCLASSIFIED'])
            j.record('manifest',manifest)
            os.environ.update(LLMDB_ROOT=str(ROOT),HF_HOME=str(ROOT/'data/hf_cache'),HF_DATASETS_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_OFFLINE='1',MODEL_ID=A.MODEL_ID,MODEL_REV=A.MODEL_REV)
            spec=importlib.util.spec_from_file_location('_precast_gate',ROOT/'code/lab/runners/c10w_p2_gate.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
            gate.W=ROOT;gate.PY=ROOT/'.venv/bin/python'
        with j.phase('model_load'):
            H=preload(j,gate,lambda:importlib.import_module('c10e_bandknob'))
            j.gate('loaded_device',{'device':str(H.DEV),'model_id':H.ID,'revision':H.REV},lambda x:x=={'device':'mps','model_id':A.MODEL_ID,'revision':A.MODEL_REV},'DEVICE-IDENTITY')
            H.hp=H.MEMITHyperParams.from_json(str(ROOT/'code/configs/hparams/qwen25_3b_memit_hparams.json'))
            from rome import repr_tools
            H._PRECAST_REPR=repr_tools
        with j.phase('pristine'):
            pristine={name:cpu_copy(t) for name,t in H.model.named_parameters()}
            j.finite('pristine_weights',pristine)
        with j.phase('cleanup'),restored(H,pristine):
            H.get_context_templates.__globals__['CONTEXT_TEMPLATES_CACHE']=copy.deepcopy(manifest['contexts'])
            H._LAW5_DEFAULT_CTX=False;H._CANDIDATE_RECIPE=False;H.Z_OVERRIDE_HITS=0
            def memory_snapshot(phase,inputs):
                serial[0]+=1;j.record('resource_%04d_'%serial[0]+re.sub('[^A-Za-z0-9_-]','_',phase),{'inputs':inputs})
            H._C10Y_PREFIX_SAVE=memory_snapshot
            with j.phase('projectors'):
                A.sample_memory(H,'precast_projectors')
                cov=H.cov_cache_sha256(H.hp)
                j.gate('covariance_identity',{'actual':cov,'expected':manifest['covariance']},lambda x:all(Path(x['actual'][l]['path']).resolve()==Path(v['path']) and x['actual'][l]['sha256']==v['sha256'] for l,v in x['expected'].items()),'COVARIANCE-IDENTITY')
                P=H.compute_P(H.hp);j.finite('projectors',{'P':P})
                P=load_record(out/'projectors.json')['P']
            requests={}
            for arm in ARMS:
                requests[arm]=[H.req(H.CANON,s,H.ARMS[arm][s]) for s in H.FICTION]
                j.gate('request_order_'+arm,{'requests':requests[arm],'subjects':H.FICTION,'band':H.hp.layers},lambda x:len(x['requests'])==24 and x['band']==list(LAYERS),'REQUEST-IDENTITY')
            H.Z_OVERRIDE=compute_targets(H,j,requests,manifest['contexts'],pristine)
            for arm in ARMS:
                with j.phase('native_'+arm):
                    A.sample_memory(H,'precast_native')
                    native=native_capture(H,requests[arm],P,j,arm)
                with j.phase('controls_'+arm):
                    for cell in native['cells']:
                        A.sample_memory(H,'precast_controls');reading['cells'].append(compare_cell(H,j,cell))
            j.record('compare',{'cells':reading['cells'],'all_pairs':'one exclusive per-pair record, referenced by each numeric record',
                                'columns':'weight coordinates; no attribution to fact IDs'})
            j.gate('source_unchanged',{'start':sources,'end':source_identity(ROOT)},lambda x:x['start']==x['end'],'SOURCE-DRIFT')
            del H._C10Y_PREFIX_SAVE
        reading['requirements']={k:True for k in REQUIREMENTS}
        j.record('worker',{'status':'COMPLETED','reading_inputs':reading,'phases':phase_summary(out)})
        return 0
    except BaseException as error:
        j.record('worker_halt',{'code':getattr(error,'code','INSTRUMENT-ERROR'),'detail':str(error),'traceback':traceback.format_exc(),
                              'phases':phase_summary(out),'reading_inputs':reading})
        j.record('worker',{'status':'INCOMPLETE','reading_inputs':reading,'phases':phase_summary(out)})
        return 2

def finalize(out,returncode,timed_out,elapsed_s):
    out=Path(out);j=Journal(out)
    for name in ('reading_inputs','reading','run','supervisor_timeout','supervisor_halt'):
        if (out/(name+'.json')).exists():raise A.Halt('EXISTING-ARTIFACT',name)
    failure={}
    try:worker_record=A.strict_load(out/'worker.json') if (out/'worker.json').is_file() else {'status':'NOT-RUN'}
    except (ValueError,OSError) as error:
        failure={'exception':type(error).__name__,'detail':str(error),'traceback':traceback.format_exc()}
        worker_record={'status':'INCOMPLETE'}
    e=worker_record.get('reading_inputs',{'requirements':{},'cells':[]})
    e=copy.deepcopy(e);e.setdefault('requirements',{})
    e['requirements']['deadline']=not timed_out and elapsed_s<CAP_SECONDS
    phases=phase_summary(out)
    incomplete=any(v['status']!='COMPLETED' for v in phases.values())
    if returncode!=0 or worker_record['status']!='COMPLETED' or incomplete:e['requirements']['capture']=False
    if timed_out:
        j.record('supervisor_timeout',{'label':'INCONCLUSIVE','code':'SUPERVISOR-TIMEOUT','cap_s':CAP_SECONDS,'elapsed_s':elapsed_s,
                                       'phases':phase_summary(out),'worker_returncode':returncode,'cleanup':'UNVERIFIED if worker was forcibly killed; committed artifacts retained'})
    elif returncode!=0 or worker_record['status']!='COMPLETED' or incomplete:
        j.record('supervisor_halt',{'label':'INCONCLUSIVE','code':'WORKER-INCOMPLETE','worker_returncode':returncode,'phases':phases,**failure})
    j.record('reading_inputs',e)
    reading=classify(load_record(out/'reading_inputs.json'));j.record('reading',reading)
    j.record('run',{'status':reading['label'],'reading':reading,'decision_id':'D-C10y-precast','cap_s':CAP_SECONDS,'elapsed_s':elapsed_s,
                    'returncode':returncode,'phases':phase_summary(out),'calibration4':'terminal ZERO_STEP-IDENTITY; unchanged',
                    'admission':'No corrective execution, calibration 5, stage-1, or F1 closure authorized.'})
    return 0 if reading['label']!='INCONCLUSIVE' else 2

def timeout_terminal(out,returncode,elapsed_s):
    """A fresh supervisor authority when publication itself is interrupted."""
    out=Path(out);j=Journal(out)
    reading_name='timeout_reading' if (out/'reading.json').exists() else 'reading'
    run_name='timeout_run' if (out/'run.json').exists() else 'run'
    prior={n:A.sha(out/n) for n in ('reading_inputs.json','reading.json','run.json') if (out/n).is_file()}
    j.record('supervisor_timeout',{'label':'INCONCLUSIVE','code':'SUPERVISOR-TIMEOUT','cap_s':CAP_SECONDS,'elapsed_s':elapsed_s,
                                   'phases':phase_summary(out),'worker_returncode':returncode,'retained_partial_publication':prior,
                                   'authority':'This fresh timeout diagnostic overrides any unfinished publication; prior bytes are preserved.',
                                   'reading':reading_name+'.json','run':run_name+'.json','cleanup':'UNVERIFIED after forced termination'})
    path=j.record('timeout_reading_inputs',{'requirements':{k:False for k in REQUIREMENTS},'cells':[]})
    reading=classify(load_record(path));j.record(reading_name,reading)
    j.record(run_name,{'status':'INCONCLUSIVE','reading':reading,'decision_id':'D-C10y-precast','returncode':returncode,
                      'cap_s':CAP_SECONDS,'elapsed_s':elapsed_s,'phases':phase_summary(out),'authority':'supervisor_timeout.json'})
    return 2

def interrupted_terminal(out,returncode,elapsed_s,reason):
    """Publish a fresh authority after the supervisor stops and reaps its children."""
    if reason not in ('TERM','INT','HUP','ABNORMAL_EXIT'):raise A.Halt('SUPERVISOR-INTERRUPTION-REASON',reason)
    out=Path(out);j=Journal(out)
    reading_name='interrupted_reading' if (out/'reading.json').exists() else 'reading'
    run_name='interrupted_run' if (out/'run.json').exists() else 'run'
    prior={n:A.sha(out/n) for n in ('reading_inputs.json','reading.json','run.json') if (out/n).is_file()}
    j.record('supervisor_interruption',{'label':'INCONCLUSIVE','code':'SUPERVISOR-INTERRUPTED','reason':reason,
                                       'cap_s':CAP_SECONDS,'elapsed_s':elapsed_s,'returncode':returncode,'phases':phase_summary(out),
                                       'retained_partial_publication':prior,'reading':reading_name+'.json','run':run_name+'.json',
                                       'authority':'This interruption diagnostic overrides earlier publication; prior bytes are preserved.',
                                       'cleanup':'Owned process group stopped; direct children reaped by the shell; model-state cleanup UNVERIFIED after forced termination.'})
    path=j.record('interrupted_reading_inputs',{'requirements':{k:False for k in REQUIREMENTS},'cells':[]})
    reading=classify(load_record(path));j.record(reading_name,reading)
    j.record(run_name,{'status':'INCONCLUSIVE','reading':reading,'decision_id':'D-C10y-precast','returncode':returncode,
                      'cap_s':CAP_SECONDS,'elapsed_s':elapsed_s,'phases':phase_summary(out),'authority':'supervisor_interruption.json'})
    return 2

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--utc',required=True)
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--prepare',action='store_true');modes.add_argument('--worker',action='store_true');modes.add_argument('--finalize',action='store_true')
    modes.add_argument('--timeout-record',action='store_true')
    modes.add_argument('--interrupted',action='store_true')
    parser.add_argument('--returncode',type=int,default=2);parser.add_argument('--elapsed-s',type=float,default=0.);parser.add_argument('--timed-out',action='store_true')
    parser.add_argument('--reason',choices=('TERM','INT','HUP','ABNORMAL_EXIT'))
    args=parser.parse_args(argv)
    owner=int(os.environ.get('C10Y_PRECAST_SUPERVISOR','0'))
    if owner!=os.getppid() or owner<=1:raise A.Halt('EXTERNAL-SUPERVISOR-REQUIRED')
    if not re.fullmatch(r'\d{8}T\d{6}(?:\.\d{6})?Z',args.utc):raise A.Halt('UTC-NAMESPACE')
    out=ROOT/'experiments/c10y/runs/c10y_precast_diag'/args.utc
    if args.prepare:
        verify_scope(ROOT);claim_namespace(ROOT,args.utc,owner);return 0
    launch=A.strict_load(out/'launch.json')
    if launch.get('supervisor_pid')!=owner or launch.get('scope_sha256')!=SCOPE_SHA:raise A.Halt('OUTPUT-OWNERSHIP')
    if args.interrupted:return interrupted_terminal(out,args.returncode,args.elapsed_s,args.reason)
    if args.timeout_record:return timeout_terminal(out,args.returncode,args.elapsed_s)
    if args.finalize:return finalize(out,args.returncode,args.timed_out,args.elapsed_s)
    if os.environ.get('C10Y_SELFTEST'):raise A.Halt('SELFTEST-REAL-WORKER')
    os.setsid()
    Journal(out).record('worker_started',{'pid':os.getpid(),'process_group':os.getpid(),'at':A.utc()})
    signal.signal(signal.SIGTERM,lambda *unused:(_ for _ in ()).throw(A.Halt('EXTERNAL-DEADLINE')))
    return worker(out)

if __name__=='__main__':sys.exit(main())
