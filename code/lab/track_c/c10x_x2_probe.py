"""Read-only C10X X2 null diagnostics; live measurement is never run by selftest."""
import argparse
import ast
import contextlib
import datetime
import functools
import json
import os
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True
import types

import c10x_enginepath_arms as A
import c10x_enginepath_inertness as I

ROOT = Path(__file__).resolve().parents[2]


def load_templates(path, expected_sha):
    from c10x_enginepath_read import strict_json
    path = Path(path)
    if not re.fullmatch(r'[0-9a-f]{64}',expected_sha) or A.sha_file(path)!=expected_sha:
        raise ValueError('template file SHA mismatch')
    data = strict_json(path.read_bytes())
    ctx,source = A.recorded_contexts()
    if (set(data)!={'schema','ctx','ctx_sha256','source'} or
            data['schema']!='c10x_context_templates/v1' or data['ctx']!=ctx or
            data['ctx_sha256']!=A.json_sha(ctx) or data['source']!=source):
        raise ValueError('template recorded identity mismatch')
    return data['ctx'],{**data,'path':str(path.resolve()),'file_sha256':expected_sha}


def fresh_output(path, base):
    path,base = Path(path),Path(base)
    if (not path.is_absolute() or path.parent.resolve()!=base.resolve() or
            not re.fullmatch(r'\d{8}T\d{6}_\d{6}Z',path.name)):
        raise ValueError('absolute fresh UTC output under experiments/c10x/runs/c10x_x2_probe required')
    if os.path.lexists(path):raise ValueError('existing output refused')
    base.mkdir(parents=True,exist_ok=True)
    path.mkdir()  # Exclusive, including a concurrent creator.
    return path


def unsafe_copy(source_device, source_dtype, target_device, target_dtype):
    return (str(source_device).split(':')[0]=='mps' and
            str(target_device).split(':')[0]=='cpu' and source_dtype!=target_dtype)


def tensor_meta(tensor):
    return {'dtype':str(tensor.dtype),'device':str(tensor.device),'shape':list(tensor.shape),
            'stride':list(tensor.stride()),'storage_offset':tensor.storage_offset(),
            'contiguous':tensor.is_contiguous()}


def storage_key(tensor):
    return str(tensor.device),tensor.untyped_storage().data_ptr()


@contextlib.contextmanager
def read_only_guard(model, events, stage=None):
    import torch
    from torch.utils._python_dispatch import TorchDispatchMode
    protected = {storage_key(t) for t in model.parameters() if t.numel()}
    def tensors(value):
        if isinstance(value,torch.Tensor):yield value
        elif isinstance(value,(tuple,list)):
            for item in value:yield from tensors(item)
    class Guard(TorchDispatchMode):
        def __torch_dispatch__(self,func,types,args=(),kwargs=None):
            kwargs = kwargs or {}
            bound = {arg.name:args[i] if i<len(args) else kwargs.get(arg.name)
                     for i,arg in enumerate(func._schema.arguments)}
            source,target_device,target_dtype = None,None,None
            if func is torch.ops.aten._to_copy.default:
                source = args[0]
                target_device = kwargs.get('device') or source.device
                target_dtype = kwargs.get('dtype') or source.dtype
            elif func is torch.ops.aten.copy_.default:
                destination,source = args[:2]
                target_device,target_dtype = destination.device,destination.dtype
            unsafe = source is not None and unsafe_copy(source.device,source.dtype,target_device,target_dtype)
            if source is not None and (unsafe or (source.device.type=='mps' and str(target_device).split(':')[0]=='cpu')):
                events.append({'operation':str(func),'stage':(stage or {}).get('value'),
                    'source':tensor_meta(source),'target_device':str(target_device),
                    'target_dtype':str(target_dtype),'dtype_change':unsafe,'executed':not unsafe,
                    'source_aliases_live_weight':storage_key(source) in protected})
                if unsafe:raise RuntimeError('UNSAFE_MPS_TO_CPU_DTYPE_COPY refused before execution')
            for arg in func._schema.arguments:
                if arg.alias_info is not None and arg.alias_info.is_write:
                    if any(t.numel() and storage_key(t) in protected for t in tensors(bound[arg.name])):
                        raise RuntimeError('LIVE_WEIGHT_WRITE '+str(func)+' '+arg.name)
            return func(*args,**kwargs)
    with Guard():yield


class ShadowModel:
    """Writer parameter enumeration is private; every forward uses pristine modules."""
    def __init__(self,model,weights):self.real,self.weights = model,weights
    def __getattr__(self,name):return getattr(self.real,name)
    def __call__(self,*args,**kwargs):return self.real(*args,**kwargs)
    def named_parameters(self,*args,**kwargs):
        for name,value in self.real.named_parameters(*args,**kwargs):
            yield name,self.weights.get(name,value)


def gate_call(call):
    try:
        value = call()
        return value if isinstance(value,dict) else {'ok':True,'value':value}
    except I.Halt as exc:return {'ok':False,'code':str(exc)}


def distance(a,b):
    import torch
    a,b = I.cpu_copy(a),I.cpu_copy(b)
    diff = a-b  # Frozen X2-(iv) CPU fp32 arithmetic.
    rel = float(diff.norm()/a.norm()) if float(a.norm()) else (0. if torch.equal(a,b) else float('inf'))
    return {'relative':I.fp32_report(rel),'max_abs':float(diff.abs().max()),
            'nonzero_elements':int(torch.count_nonzero(diff)),
            'compared_tensors':{'a':tensor_meta(a),'b':tensor_meta(b)},
            'arithmetic':'frozen_cpu_float32'}


@contextlib.contextmanager
def trace_solve(callback):
    tree = ast.parse(Path(A.__file__).read_text())
    writer = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='fe_edit')
    sites = [n for n in ast.walk(writer) if isinstance(n,ast.Assign) and
             isinstance(n.value,ast.Attribute) and isinstance(n.value.value,ast.Call) and
             ast.unparse(n.value.value.func)=='torch.linalg.solve']
    if len(sites)!=1 or sys.gettrace() is not None:raise RuntimeError('writer trace identity refused')
    def trace(frame,event,arg):
        if frame.f_code is not A.fe_edit.__code__:return None
        if event=='line' and frame.f_lineno==sites[0].lineno:callback(frame.f_locals)
        return trace
    sys.settrace(trace)
    try:yield
    finally:sys.settrace(None)


def probe(harness, hp, template_file, template_sha, P=None):
    import torch
    ctx,identity = load_templates(template_file,template_sha)
    if list(hp.layers)!=list(range(4,9)) or len(harness.FICTION)!=24:
        raise ValueError('probe requires frozen layers 4..8 and 24 rows')
    if A.H is not harness or A.TELEMETRY is not None or 'C10X_TELEMETRY' in os.environ:
        raise ValueError('configured harness with telemetry off required')
    result = {'schema':'c10x_x2_probe/v1','status':'MEASURING','scientific_verdict':'diagnostic_only',
              'telemetry':False,'templates':identity,'x2_iv_a':[],'layers':{},'mps_to_cpu_copies':[]}
    params = dict(harness.model.named_parameters())
    versions = {k:v._version for k,v in params.items()}
    stage = {'value':'live pristine snapshot'}
    with read_only_guard(harness.model,result['mps_to_cpu_copies'],stage):
        pristine = I.Pristine(harness,hp)
    namespace = A.fe_edit.__globals__
    old_model,reader,matcher = namespace['model'],namespace['get_module_input_output_at_words'],namespace['upd_matrix_match_shape']
    old_fe,old_targets = A.FE_STATE,A.FE_TARGETS
    try:
        with read_only_guard(harness.model,result['mps_to_cpu_copies'],stage), A.pinned_contexts(harness,ctx):
            pristine.verify('probe entry')
            stage['value'] = 'projectors'
            if P is None:P = harness.compute_P(hp)
            result['projectors'] = [{'layer':l,'sha256':I.tensor_sha(p),'tensor':tensor_meta(p)} for l,p in zip(hp.layers,P)]
            replay_floor = 0.
            for arm in A.ARM_NAMES:
                requests = [harness.req(harness.CANON,s,harness.ARMS[arm][s]) for s in harness.FICTION]
                stage['value'] = 'X2-iv '+arm
                plain,meta = A.batch_replay(harness,hp,requests)
                for layer in hp.layers:
                    native_a = A.canonical_read(harness,hp,layer,requests)
                    native_b = A.canonical_read(harness,hp,layer,requests)
                    a,b = I.cpu_copy(native_a),I.cpu_copy(native_b)
                    measurement = gate_call(lambda:I.relative_fixed(a,b))
                    f = measurement.get('value')
                    floor = gate_call(lambda:I.require(f<=1e-5,'REPLAY_FLOOR')) if f is not None else measurement
                    if f is not None:floor['value'] = f
                    if f is not None:replay_floor = max(replay_floor,f)
                    result['x2_iv_a'].append({'arm':arm,'layer':layer,'repeatability':distance(a,b),
                        'floor_gate':floor,'reader_vs_replay':distance(a,plain[layer]),
                        'parity_gate':gate_call(lambda:I.parity(a,plain[layer],f,double=False)) if f is not None else
                                      {'ok':False,'code':'NOT_EVALUATED_INVALID_FLOOR'},
                        'native_reader_first':tensor_meta(native_a),'native_reader_second':tensor_meta(native_b),
                        'replay_capture':tensor_meta(plain[layer]),'batch':meta})
                null,meta2 = A.batch_replay(harness,hp,requests,plain[hp.layers[0]])
                I.require(meta==meta2,'PROBE_REPLAY_INPUT_IDENTITY')
            result['x2_iv_floor'] = replay_floor
            requests = [harness.req(harness.CANON,s,harness.ARMS[A.ARM_NAMES[2]][s]) for s in harness.FICTION]
            order = [(r['subject'],r['target_new']['str']) for r in requests]
            stage['value'] = 'X2-vii identity replay'
            plain,meta = A.batch_replay(harness,hp,requests)
            null,meta2 = A.batch_replay(harness,hp,requests,plain[hp.layers[0]])
            I.require(meta==meta2,'PROBE_NULL_INPUT_IDENTITY')
            result['batch'] = meta
            table = {key:{l:null[l][row].clone() for l in hp.layers} for row,key in enumerate(order)}
            weights = {harness.weight_name(hp,l):params[harness.weight_name(hp,l)].detach().clone() for l in hp.layers}
            I.require(all(storage_key(t)!=storage_key(params[k]) for k,t in weights.items()),'SHADOW_STORAGE_ALIAS')
            shadow = ShadowModel(harness.model,weights)
            shadow_h = types.SimpleNamespace(model=shadow,weight_name=harness.weight_name)
            shadow_pristine = I.Pristine(shadow_h,hp)
            result['shadow_storage_disjoint'] = True
            observed,structures = {},{}
            def checked_read(model,tok,layer,context_templates,words,module_template,fact_token_strategy):
                I.require(context_templates==[r['prompt'] for r in requests] and words==[r['subject'] for r in requests],'PROBE_NULL_REQUEST_ORDER')
                expected_layer = hp.layers[len(observed)]
                stage['value'] = 'X2-vii layer '+str(expected_layer)
                blocks,meta3 = A.batch_replay(harness,hp,requests)
                I.require(meta3==meta,'PROBE_OBSERVER_BATCH_IDENTITY')
                native = reader(model,tok,layer,context_templates=context_templates,words=words,
                                module_template=module_template,fact_token_strategy=fact_token_strategy)
                captured = I.cpu_copy(native[1])
                observed[expected_layer] = blocks[expected_layer]
                target = torch.stack([table[k][expected_layer] for k in order])
                structures[expected_layer] = gate_call(lambda:I.active_null_structure(
                    {expected_layer:captured},{expected_layer:target},{expected_layer:blocks[expected_layer]},order,order))
                result['layers'][str(expected_layer)] = {'writer_requested_layer':layer,
                    'null_structure':structures[expected_layer],'writer_capture_native':tensor_meta(native[1]),
                    'observer_capture':tensor_meta(blocks[expected_layer]),'target_table':tensor_meta(target),
                    'observer_vs_writer':distance(blocks[expected_layer],captured),
                    'first_row':{'request':list(order[0]),'observer':blocks[expected_layer][0,:8].tolist(),
                                 'writer':captured[0,:8].tolist(),'target':target[0,:8].tolist()}}
                return native
            def capture_operands(values):
                layer = values['layer']
                I.require(values['keys']==order and values['cur'].shape[1]==24,'PROBE_SOLVE_ORDER')
                repeats = values['K'].shape[1]//24
                I.require(repeats>0 and values['tgt'].shape[1]==24*repeats,'PROBE_RESIDUAL_SHAPE')
                # Select each request's first repeated column from the ACTUAL gate residual.
                residual = values['tgt'][:,::repeats].T.detach().cpu()
                record = result['layers'][str(layer)]
                record.update({'rf_sha256':I.tensor_sha(values['rf']),
                    'operand_sha256':{name:I.tensor_sha(values[name]) for name in ('zs','cur','tgt','resid','rf')},
                    'operand_tensors':{name:tensor_meta(values[name]) for name in ('zs','cur','tgt','resid','rf')},
                    'request_residual_cpu':tensor_meta(residual),'repeat_columns_per_request':repeats,
                    'request_rows':[{'row':row,'request':list(key),
                        'max_abs_M_minus_cur':I.fp32_report(float(residual[row].double().abs().max())),
                        'nonzero_elements':int(torch.count_nonzero(residual[row]))} for row,key in enumerate(order)]})
            update_meta = {}
            def matched(matrix,shape):
                update = matcher(matrix,shape)
                layer = hp.layers[len(update_meta)]
                update_meta[layer] = tensor_meta(update)
                return update
            namespace['model'],namespace['get_module_input_output_at_words'],namespace['upd_matrix_match_shape'] = shadow,checked_read,matched
            A.FE_STATE,A.FE_TARGETS = {'targets':table},table
            A._refresh_globals()
            with shadow_pristine.cell('probe shadow writer'):
                with trace_solve(capture_operands), I.capture_updates(A.fe_edit,hp.layers,
                        {'writer':'fe_edit','check':'X2-vii','recipe':'read_only_probe','arm':'A7'}) as updates:
                    legacy = A.fe_edit(hp,requests,P,[torch.zeros_like(p) for p in P],mode='fe')
                cutoff = None
                for capture in updates:
                    layer,update = capture['layer'],capture['tensor']
                    before = shadow_pristine._snapshot[layer]
                    after = weights[harness.weight_name(hp,layer)].detach().cpu()
                    changed_bytes = int(torch.count_nonzero(before.contiguous().view(torch.uint8)!=after.contiguous().view(torch.uint8)))
                    changed_signs = int(torch.count_nonzero((before==0)&(after==0)&(torch.signbit(before)!=torch.signbit(after))))
                    maximum = float(update.double().abs().max())
                    record = result['layers'][str(layer)]
                    record.update({'max_abs_update':I.fp32_report(maximum),'update_nonzero_elements':int(torch.count_nonzero(update)),
                        'update_sha256':capture['sha256'],'update_pre_cast':update_meta[layer],
                        'captured_update_cpu':tensor_meta(update),'shadow_weight_native':tensor_meta(weights[harness.weight_name(hp,layer)]),
                        'live_weight_native':tensor_meta(params[harness.weight_name(hp,layer)]),
                        'shadow_weight_before_sha256':I.tensor_sha(before),'shadow_weight_after_sha256':I.tensor_sha(after),
                        'shadow_weight_changed_bytes':changed_bytes,'shadow_signed_zero_changes':changed_signs,
                        'weight_matrix_row_max_abs_update':update.double().abs().amax(dim=1).tolist(),
                        'gate_equivalent_before_write':cutoff is None})
                    for row in record['request_rows']:
                        row.update({'max_abs_update':I.fp32_report(maximum),'update_scope':'joint_layer_weight_matrix'})
                    if cutoff is None and changed_bytes:cutoff = layer
                result['gate_equivalence_cutoff_layer'] = cutoff
                result['report_only_writer_fp32'] = I.fp32_report(legacy)
                result['shadow_w0_exact_zero'] = all(r['shadow_weight_changed_bytes']==0 for r in result['layers'].values())
            result['shadow_restore'] = shadow_pristine.checkpoints[-1]
            pristine.verify('probe exit')
            I.require(all(params[k]._version==v for k,v in versions.items()),'LIVE_PARAMETER_VERSION_CHANGE')
            result.update({'status':'MEASURED','live_weights_unchanged':True,'live_parameter_count':len(params),
                'live_weight_hashes':pristine.hashes,'live_checkpoints':pristine.checkpoints,
                'unsafe_mps_to_cpu_copies':[r for r in result['mps_to_cpu_copies'] if r['dtype_change']]})
    except BaseException as exc:
        result.update({'status':'INCOMPLETE','error':type(exc).__name__+': '+str(exc),
            'unsafe_mps_to_cpu_copies':[r for r in result['mps_to_cpu_copies'] if r['dtype_change']]})
        exc.probe_record = result
        raise
    finally:
        namespace['model'],namespace['get_module_input_output_at_words'],namespace['upd_matrix_match_shape'] = old_model,reader,matcher
        A.FE_STATE,A.FE_TARGETS = old_fe,old_targets
        A._refresh_globals()
        try:
            stage['value'] = 'final live hash verification'
            with read_only_guard(harness.model,result['mps_to_cpu_copies'],stage):
                pristine.verify('probe final verification')
            I.require(all(params[k]._version==v for k,v in versions.items()),'LIVE_PARAMETER_VERSION_CHANGE')
        except I.Halt:
            # Exceptional recovery only; ordinary measurement makes ZERO live writes.
            pristine.restore()
            pristine.verify('probe emergency restoration')
            result['live_weights_unchanged'] = False
            result['emergency_live_restore'] = True
            raise
    return A.diagnostic_json(result)


@functools.lru_cache(maxsize=1)
def protected_paths(root):
    trees = set()
    for relative in ('results','architecture_profile','experiments','tools','docs','CORPUS',
                     'code/memit/vendor','covariance_caches'):
        path = root/relative
        trees.update((path,path.resolve()))
    files = set()
    for snapshots in (root/'data/hf_cache/hub').glob('*/snapshots'):
        trees.update((snapshots,snapshots.resolve()))
        # Only referenced snapshot targets are protected; locks and incomplete blobs stay writable.
        files.update(path.resolve() for path in snapshots.rglob('*') if path.is_file() or path.is_symlink())
    return trees,files


def descriptor_path(descriptor):
    import stat
    mode = os.fstat(descriptor).st_mode
    if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):return None
    if sys.platform=='darwin':
        import fcntl
        return Path(os.fsdecode(fcntl.fcntl(descriptor,50,bytes(1024)).split(b'\0',1)[0]))  # F_GETPATH.
    return Path(os.readlink('/proc/self/fd/'+str(descriptor)))


def file_policy(output,event,args):
    paths = []  # (path or descriptor, dir_fd).
    if event=='open':
        path,mode,flags = args
        if (mode and any(c in mode for c in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
            paths = [(path,-1)]
    elif event=='os.mkdir':
        paths = [(args[0],args[2])]
    elif event in ('os.rename','os.link'):paths = [(args[0],args[2]),(args[1],args[3])]
    elif event=='os.symlink':paths = [(args[1],args[2])]
    elif event in ('os.remove','os.rmdir','os.chmod'):paths = [(args[0],args[2] if event=='os.chmod' else args[1])]
    elif event in ('os.chown','os.utime'):paths = [(args[0],args[3])]
    elif event=='os.truncate':paths = [(args[0],-1)]
    elif event in ('socket.connect','os.system'):
        raise PermissionError('PROBE_READ_ONLY '+event)
    if not paths:return
    trees,files = protected_paths(ROOT)
    output_paths = {Path(os.path.abspath(output)),Path(output).resolve()}
    def inside(path,base):return path==base or base in path.parents
    for value,directory in paths:
        if isinstance(value,int):
            path = descriptor_path(value)
            if path is None:continue  # Pipes/devices have no project file to mutate.
        else:
            path = Path(os.fsdecode(value))
            if not path.is_absolute() and directory not in (-1,None):path = descriptor_path(directory)/path
        if event=='os.mkdir' and path.is_dir():continue  # An existing directory cannot be created again.
        entry = event in ('os.rename','os.remove','os.rmdir','os.symlink')
        # Resolve symlinks before lexical '..' normalization to retain the kernel's target.
        resolved = path.parent.resolve()/path.name if entry else path.resolve()
        path = Path(os.path.abspath(path))
        for candidate in (path,resolved):
            hit = candidate in files or any(inside(candidate,tree) and not (
                tree in {ROOT/'results',(ROOT/'results').resolve()} and
                any(inside(candidate,allowed) for allowed in output_paths)) for tree in trees)
            if event in ('os.rename','os.rmdir'):
                hit = hit or any(inside(protected,candidate) for protected in trees|files)
            if hit:raise PermissionError('PROBE_READ_ONLY '+event+' '+repr(value))


def install_file_policy(output):
    original_open = os.open
    def checked_open(path,flags,mode=0o777,*,dir_fd=None):
        # CPython's open audit event drops dir_fd; check the actual target before that call.
        if dir_fd is not None and not os.path.isabs(path):
            path = str(descriptor_path(dir_fd)/os.fsdecode(path))
        return original_open(path,flags,mode,dir_fd=dir_fd)
    os.open = checked_open
    sys.addaudithook(lambda event,args:file_policy(output,event,args))


def selftest():
    import hashlib
    import tempfile
    import unittest
    from unittest.mock import patch
    import c10x_enginepath_selftest as F
    import torch
    torch.set_num_threads(1)
    (F.SCRATCH/'roots').mkdir(parents=True, exist_ok=True)

    class ProbeTests(unittest.TestCase):
        def setUp(self):
            self.tmp = tempfile.TemporaryDirectory(dir=F.SCRATCH/'roots')
            self.root = Path(self.tmp.name)
            self.oldroot = A.ROOT
            A.ROOT = self.root
            benchmark = self.root/A.CONTEXT_SOURCE
            benchmark.parent.mkdir(parents=True)
            benchmark.write_bytes((ROOT/A.CONTEXT_SOURCE).read_bytes())
            self.path = self.root/'context_templates.json'
            self.path.write_bytes((ROOT/'experiments/c10x/runs/c10x_enginepath/context_templates.json').read_bytes())
            self.sha = A.sha_file(self.path)
            self.H = F.stub_h()
            self.hp = self.H.hp
            self.P = [torch.eye(2) for _ in self.hp.layers]
            A.configure(self.H)
        def tearDown(self):
            A.release(self.H)
            A.ROOT = self.oldroot
            self.tmp.cleanup()
        def measure(self):
            return probe(self.H, self.hp, self.path, self.sha, self.P)

        @contextlib.contextmanager
        def gate_operands(self):
            import inspect
            lines,start = inspect.getsourcelines(A.fe_edit)
            at = start + next(i for i,line in enumerate(lines) if 'upd = torch.linalg.solve' in line)
            records = {}
            previous = sys.gettrace()
            def trace(frame,event,arg):
                if frame.f_code is A.fe_edit.__code__ and event=='line' and frame.f_lineno==at:
                    v = frame.f_locals
                    records[str(v['layer'])] = {name:I.tensor_sha(v[name]) for name in ('zs','cur','tgt','resid','rf')}
                return trace
            sys.settrace(trace)
            try:yield records
            finally:sys.settrace(previous)

        def gate_reference(self):
            ctx,_ = A.recorded_contexts()
            requests = [self.H.req(self.H.CANON,s,self.H.ARMS[A.ARM_NAMES[2]][s]) for s in self.H.FICTION]
            with A.pinned_contexts(self.H,ctx), I.Pristine(self.H,self.hp).cell('CPU gate reference'):
                plain,_ = A.batch_replay(self.H,self.hp,requests)
                null,_ = A.batch_replay(self.H,self.hp,requests,plain[4])
                keys = [(r['subject'],r['target_new']['str']) for r in requests]
                A.FE_TARGETS = {k:{l:null[l][row].clone() for l in self.hp.layers} for row,k in enumerate(keys)}
                A._refresh_globals()
                observed = {l:I.cpu_copy(A.canonical_read(self.H,self.hp,l,requests)) for l in self.hp.layers}
                with I.observe_null_solve(A.fe_edit,observed,keys):
                    A.fe_edit(self.hp,requests,self.P,[torch.zeros_like(p) for p in self.P],mode='fe')

        def test_wrong_template_hash_refuses_before_forward(self):
            with self.assertRaisesRegex(ValueError, 'template'):
                probe(self.H, self.hp, self.path, '0'*64, self.P)
            self.assertEqual(self.H.model.science_count, 0)
            data = json.loads(self.path.read_text())
            data['ctx_sha256'] = '0'*64
            self.path.write_text(json.dumps(data))
            self.sha = A.sha_file(self.path)
            with self.assertRaisesRegex(ValueError, 'template'):
                self.measure()
            self.assertEqual(self.H.model.science_count, 0)

        def test_no_live_weight_writes(self):
            weights = dict(self.H.model.named_parameters())
            before = {k:(I.tensor_sha(v), v._version) for k,v in weights.items()}
            hooks = I.hook_identity(self.H.model)
            reader = A.fe_edit.__globals__['get_module_input_output_at_words']
            measured = self.measure()
            self.assertIn('layers', measured)
            self.assertEqual(set(measured['layers']), {'4','5','6','7','8'})
            self.assertEqual({k:(I.tensor_sha(v),v._version) for k,v in weights.items()}, before)
            self.assertEqual(I.hook_identity(self.H.model), hooks)
            self.assertIs(A.fe_edit.__globals__['get_module_input_output_at_words'], reader)
            self.assertTrue(measured['live_weights_unchanged'])
            self.assertEqual(measured['unsafe_mps_to_cpu_copies'], [])
            from c10x_enginepath_read import strict_json
            output = fresh_output(self.root/'experiments/c10x/runs/c10x_x2_probe/20261008T170000_000000Z',self.root/'experiments/c10x/runs/c10x_x2_probe')
            A.write_json(output/'probe.json',measured)
            self.assertEqual(strict_json((output/'probe.json').read_bytes()),measured)

        def test_residual_matches_actual_gate_fixed_input(self):
            measured = self.measure()
            self.assertIn('layers', measured)
            ctx, _ = A.recorded_contexts()
            requests = [self.H.req(self.H.CANON,s,self.H.ARMS[A.ARM_NAMES[2]][s]) for s in self.H.FICTION]
            with A.pinned_contexts(self.H,ctx), I.Pristine(self.H,self.hp).cell('CPU gate reference'):
                plain,_ = A.batch_replay(self.H,self.hp,requests)
                null,_ = A.batch_replay(self.H,self.hp,requests,plain[4])
                keys = [(r['subject'],r['target_new']['str']) for r in requests]
                table = {k:{l:null[l][row].clone() for l in self.hp.layers} for row,k in enumerate(keys)}
                observed = {l:I.cpu_copy(A.canonical_read(self.H,self.hp,l,requests)) for l in self.hp.layers}
                A.FE_TARGETS = table
                A._refresh_globals()
                with I.observe_null_solve(A.fe_edit,observed,keys) as residuals:
                    A.fe_edit(self.hp,requests,self.P,[torch.zeros_like(p) for p in self.P],mode='fe')
            self.assertEqual(len(residuals),5)
            for record in residuals:
                layer = measured['layers'][str(record['layer'])]
                self.assertEqual(layer['rf_sha256'], record['residual_sha256'])
                self.assertEqual(len(layer['request_rows']),24)
                self.assertTrue(all(row['nonzero_elements']==0 and row['max_abs_M_minus_cur']==0. for row in layer['request_rows']))
            with self.gate_operands() as operands:self.gate_reference()
            for layer,values in operands.items():
                self.assertEqual(measured['layers'][layer]['operand_sha256'],values)

        def test_nonzero_residual_matches_rejecting_gate(self):
            original = A.batch_replay
            def perturbed(H,hp,requests,overwrite=None):
                blocks,meta = original(H,hp,requests,overwrite)
                if overwrite is not None:blocks[8] = blocks[8] + .25
                return blocks,meta
            with patch.object(A,'batch_replay',side_effect=perturbed):
                measured = self.measure()
                self.assertIn('layers',measured)
                with self.gate_operands() as operands:
                    with self.assertRaisesRegex(I.Halt,'NULL_PERMUTED_TARGET|NULL_NONZERO_RESIDUAL'):
                        self.gate_reference()
            layer = measured['layers']['8']
            self.assertEqual(layer['operand_sha256'],operands['8'])
            self.assertTrue(all(row['nonzero_elements']==2 and row['max_abs_M_minus_cur']==.25 for row in layer['request_rows']))
            self.assertGreater(layer['max_abs_update'],0.)
            self.assertFalse(layer['null_structure']['ok'])

        def test_signed_zero_only_changes_shadow_bytes(self):
            weight = dict(self.H.model.named_parameters())[self.H.weight_name(self.hp,4)]
            with torch.no_grad():weight[0,0] = -0.
            before = I.tensor_sha(weight), weight._version
            measured = self.measure()
            self.assertIn('layers', measured)
            first = measured['layers']['4']
            self.assertEqual(first['max_abs_update'],0.)
            self.assertGreater(first['shadow_weight_changed_bytes'],0)
            self.assertGreater(first['shadow_signed_zero_changes'],0)
            self.assertEqual(measured['gate_equivalence_cutoff_layer'],4)
            self.assertFalse(measured['layers']['5']['gate_equivalent_before_write'])
            self.assertEqual((I.tensor_sha(weight),weight._version),before)

        def test_guard_blocks_alias_and_out_writes_before_execution(self):
            weight = next(self.H.model.parameters())
            before = I.tensor_sha(weight), weight._version
            with self.assertRaisesRegex(RuntimeError,'LIVE_WEIGHT_WRITE'):
                with read_only_guard(self.H.model,[]):
                    weight.detach().view(-1).add_(1.)
            self.assertEqual((I.tensor_sha(weight),weight._version),before)
            with self.assertRaisesRegex(RuntimeError,'LIVE_WEIGHT_WRITE'):
                with read_only_guard(self.H.model,[]):
                    torch.add(weight.detach(),1.,out=weight.detach())
            self.assertEqual((I.tensor_sha(weight),weight._version),before)

        def test_unsafe_copy_predicate_without_mps(self):
            for args,want in [
                (('mps','float16','cpu','float32'),True),
                (('mps','float32','cpu','float16'),True),
                (('mps','float16','cpu','float16'),False),
                (('cpu','float16','cpu','float32'),False),
                (('cpu','float32','mps','float16'),False)]:
                with self.subTest(args=args):self.assertEqual(unsafe_copy(*args),want)

        def test_copy_guard_refuses_before_operator(self):
            weight = next(self.H.model.parameters())
            before = I.tensor_sha(weight),weight._version
            events = []
            # CPU positive control of the dispatch refusal, without creating an MPS tensor.
            with patch.object(sys.modules[__name__],'unsafe_copy',return_value=True):
                with self.assertRaisesRegex(RuntimeError,'UNSAFE_MPS_TO_CPU_DTYPE_COPY'):
                    with read_only_guard(self.H.model,events):weight.detach().to(dtype=torch.float64)
            self.assertEqual((I.tensor_sha(weight),weight._version),before)
            self.assertEqual(len(events),1)
            self.assertFalse(events[0]['executed'])
            self.assertTrue(events[0]['source_aliases_live_weight'])

        def policy_fixture(self):
            output = self.root/'experiments/c10x/runs/c10x_x2_probe/20261008T170000_000000Z'
            output.mkdir(parents=True)
            snapshot = self.root/'data/hf_cache/hub/models--tiny/snapshots/r1/config.json'
            blob = snapshot.parents[2]/'blobs/recorded'
            snapshot.parent.mkdir(parents=True)
            blob.parent.mkdir()
            blob.write_text('recorded')
            snapshot.symlink_to(blob)
            covariance = self.root/'runtime/covariance'
            covariance.mkdir(parents=True)
            (self.root/'data/covariance').symlink_to(covariance,target_is_directory=True)
            protected = [self.root/p/'victim' for p in ('results/history','architecture_profile',
                'experiments','tools','docs','CORPUS','code/memit/vendor','covariance_caches')]
            for path in protected:
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text('preserve')
            return output,protected+[snapshot,blob]

        @contextlib.contextmanager
        def installed_policy(self,output):
            active = [True]
            install = sys.addaudithook
            with patch.object(sys.modules[__name__],'ROOT',self.root), patch.object(os,'open',os.open), \
                    patch.object(sys,'addaudithook',side_effect=lambda hook:install(
                        lambda event,args:hook(event,args) if active[0] else None)):
                install_file_policy(output)
                try:yield
                finally:active[0] = False

        def test_file_write_policy(self):
            output,protected = self.policy_fixture()
            with patch.object(sys.modules[__name__],'ROOT',self.root):
                for path in protected:
                    for event,args in [('open',(str(path),'w',os.O_TRUNC|os.O_WRONLY)),
                            ('os.remove',(str(path),-1)),('os.chmod',(str(path),0o600,-1)),
                            ('os.truncate',(str(path),0)),
                            ('os.rename',(str(path),str(output/'stolen'),-1,-1)),
                            ('os.rename',(str(output/'incoming'),str(path),-1,-1))]:
                        with self.subTest(path=path.relative_to(self.root),event=event):
                            with self.assertRaisesRegex(PermissionError,'PROBE_READ_ONLY'):
                                file_policy(output,event,args)
                for event in ('socket.connect','os.system'):
                    with self.assertRaisesRegex(PermissionError,'PROBE_READ_ONLY'):
                        file_policy(output,event,(None,None))
                for event in ('socket.bind','subprocess.Popen'):
                    file_policy(output,event,(None,None))

        def test_runtime_files_are_writable_under_installed_policy(self):
            output,protected = self.policy_fixture()
            runtime = [output/'probe.json',self.root/'runtime/tmp/file',
                self.root/'runtime/home/.cache/file',self.root/'data/hf_cache/hub/.locks/new.lock',
                self.root/'data/hf_cache/hub/models--tiny/refs/main',protected[-1].parent/'download.incomplete',
                protected[-1].parent/'unreferenced']
            for path in runtime:path.parent.mkdir(parents=True,exist_ok=True)
            with self.installed_policy(output):
                with open(os.devnull,'w') as null:null.write('discard')
                for path in runtime:
                    with self.subTest(path=path.relative_to(self.root)):
                        path.write_text('runtime')
                        os.chmod(path,0o600)
                        os.truncate(path,1)
                        renamed = path.with_name(path.name+'.moved')
                        path.rename(renamed)
                        renamed.unlink()
                alias = self.root/'runtime/allowed_alias'
                alias.symlink_to(protected[0])
                alias.unlink()

        def test_protected_aliases_and_directory_moves(self):
            output,protected = self.policy_fixture()
            aliases = [output/'escape',self.root/'runtime/alias']
            for path in aliases:path.symlink_to(protected[0])
            nested = protected[4].parent/'nested'
            nested.mkdir()
            traversal = self.root/'runtime/traversal'
            traversal.symlink_to(nested,target_is_directory=True)
            aliases.append(traversal/'..'/'victim')
            with patch.object(sys.modules[__name__],'ROOT',self.root):
                for path in aliases+[self.root/'runtime/covariance/victim']:
                    with self.subTest(path=path):
                        with self.assertRaisesRegex(PermissionError,'PROBE_READ_ONLY'):
                            file_policy(output,'open',(str(path),'w',os.O_WRONLY))
                for path in [self.root/'results',protected[-1].parent,protected[-1].parent.parent]:
                    with self.subTest(directory=path):
                        with self.assertRaisesRegex(PermissionError,'PROBE_READ_ONLY'):
                            file_policy(output,'os.rename',(str(path),str(self.root/'runtime/moved'),-1,-1))
                with self.assertRaisesRegex(PermissionError,'PROBE_READ_ONLY'):
                    file_policy(output,'os.mkdir',(str(self.root/'docs/new'),0o755,-1))

        def test_descriptor_relative_writes_and_fd_mutations(self):
            output,protected = self.policy_fixture()
            path = protected[4]
            directory = os.open(path.parent,os.O_RDONLY)
            descriptor = os.open(path,os.O_RDWR)
            try:
                with self.installed_policy(output):
                    for operation in [lambda:os.open(path.name,os.O_WRONLY,dir_fd=directory),
                            lambda:os.unlink(path.name,dir_fd=directory),
                            lambda:os.rename(path.name,'moved',src_dir_fd=directory,dst_dir_fd=directory),
                            lambda:os.chmod(path.name,0o600,dir_fd=directory),
                            lambda:os.fchmod(descriptor,0o600),lambda:os.ftruncate(descriptor,0),
                            lambda:file_policy(output,'open',(descriptor,'w',os.O_WRONLY))]:
                        with self.subTest(operation=operation):
                            with self.assertRaisesRegex(PermissionError,'PROBE_READ_ONLY'):operation()
                self.assertEqual(path.read_text(),'preserve')
            finally:
                os.close(descriptor)
                os.close(directory)

        def test_descriptor_runtime_open_from_protected_cwd(self):
            output,_ = self.policy_fixture()
            directory = os.open(self.root/'runtime',os.O_RDONLY)
            previous = Path.cwd()
            try:
                os.chdir(self.root/'code/memit/vendor')
                with self.installed_policy(output):
                    for name in ('runtime.tmp',b'bytes.tmp',Path('path.tmp')):
                        try:descriptor = os.open(name,os.O_CREAT|os.O_WRONLY,dir_fd=directory)
                        except PermissionError as exc:self.fail('RUNTIME_DIR_FD_FALSE_REFUSAL '+str(exc))
                        try:os.write(descriptor,b'permitted')
                        finally:os.close(descriptor)
            finally:
                os.chdir(previous)
                os.close(directory)
            self.assertEqual((self.root/'runtime/runtime.tmp').read_bytes(),b'permitted')
            self.assertEqual((self.root/'runtime/bytes.tmp').read_bytes(),b'permitted')
            self.assertEqual((self.root/'runtime/path.tmp').read_bytes(),b'permitted')

        def test_cli_wrong_template_refuses_before_loader(self):
            with patch.object(A,'load_harness',side_effect=AssertionError('model loader reached')):
                with self.assertRaisesRegex(ValueError,'template'):
                    main(['--templates',str(self.path),'--templates-sha256','0'*64])

        def test_x2_iv_floor_threshold_matches_gate(self):
            original = A.canonical_read
            calls = []
            def unstable(*args):
                value = original(*args)
                calls.append(1)
                return value if len(calls)%2 else value+.01
            with patch.object(A,'canonical_read',side_effect=unstable):measured = self.measure()
            first = measured['x2_iv_a'][0]
            self.assertGreater(first['repeatability']['relative'],1e-5)
            self.assertFalse(first['floor_gate']['ok'])
            self.assertEqual(first['floor_gate']['code'],'REPLAY_FLOOR')

        def test_probe_bans_unsafe_copy_forms(self):
            def unsafe(node):
                if not isinstance(node,ast.Call):return False
                kws = {k.arg:k.value for k in node.keywords}
                if isinstance(node.func,ast.Attribute) and node.func.attr in ('copy_','type'):return True
                if ast.unparse(node.func) in ('torch.tensor','torch.as_tensor'):
                    return 'dtype' in kws and 'device' in kws
                if not isinstance(node.func,ast.Attribute) or node.func.attr!='to':return False
                if 'device' in kws and 'dtype' in kws:return True
                if node.args:
                    first = node.args[0]
                    if isinstance(first,ast.Constant) and isinstance(first.value,str):
                        return len(node.args)>1 or 'dtype' in kws
                    if isinstance(first,ast.Call) and ast.unparse(first.func)=='torch.device':
                        return len(node.args)>1 or 'dtype' in kws
                    if isinstance(first,ast.Attribute):
                        dtype = first.attr=='dtype' or ast.unparse(first) in (
                            'torch.float16','torch.float32','torch.float64','torch.bfloat16',
                            'torch.half','torch.float','torch.double','torch.int64','torch.long')
                        return not dtype
                    return isinstance(first,(ast.Name,ast.Call))
                return False
            for example in ['v.to(device="cpu",dtype=torch.float32)','v.to("cpu",torch.float32)',
                            'v.to(torch.device("cpu"),torch.float32)','v.to(state.cpu_buffer)',
                            'v.clone().to(device="cpu",dtype=torch.float32)','v.to(cpu_buffer)',
                            'v.type(torch.FloatTensor)','cpu_buffer.copy_(v)',
                            'torch.tensor(v,device="cpu",dtype=torch.float32)',
                            'torch.as_tensor(v,device="cpu",dtype=torch.float32)']:
                with self.subTest(example=example):
                    self.assertTrue(any(unsafe(n) for n in ast.walk(ast.parse(example))))
            for example in ['v.cpu().to(dtype=torch.float32)','v.to(torch.float32).cpu()',
                            'v.to("cpu")','v.to(torch.device("cpu"))']:
                with self.subTest(safe=example):
                    self.assertFalse(any(unsafe(n) for n in ast.walk(ast.parse(example))))
            tree = ast.parse(Path(__file__).read_text())
            self.assertEqual([n.lineno for n in ast.walk(tree) if unsafe(n)],[])

        def test_existing_output_refused(self):
            base = self.root/'experiments/c10x/runs/c10x_x2_probe'
            path = base/'20261008T170000_000000Z'
            path.mkdir(parents=True)
            with self.assertRaisesRegex(ValueError,'existing'):
                fresh_output(path,base)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ProbeTests))
    assert not any(name in sys.modules for name in F.FORBIDDEN)
    print('CPU ONLY; no frozen harness/transformers/datasets imported')
    return 0 if result.wasSuccessful() else 1


def cache_selftest():
    import tempfile
    import unittest
    from unittest.mock import patch

    class CacheTests(unittest.TestCase):
        def test_real_cached_tokenizer_config_and_runtime_io(self):
            cache = ROOT/'data/hf_cache/hub'
            revision = '3aab1f1954e9cc14eb9509a215f9e5ca08227a9b'
            snapshot = cache/'models--Qwen--Qwen2.5-3B/snapshots'/revision
            shards = {p.resolve() for p in snapshot.glob('*.safetensors')}
            self.assertEqual(len(shards),2)
            before = {p.name:A.sha_file(p) for p in snapshot.iterdir() if p.suffix=='.json'}
            with tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary)/'probe'
                output.mkdir()
                active,reads,refusals = [True],[],[]
                install = sys.addaudithook
                def observe(hook,event,args):
                    if not active[0]:return
                    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
                        path = Path(os.fsdecode(args[0])).resolve()
                        if path in shards:raise AssertionError('WEIGHT_SHARD_READ')
                        reads.append(str(path))
                    try:hook(event,args)
                    except PermissionError as exc:
                        refusals.append(str(exc))
                        import traceback
                        print('STARTUP POLICY REFUSAL',exc,[(f.filename,f.lineno,f.name)
                            for f in traceback.extract_stack(limit=8)[:-1]])
                        raise
                with patch.object(os,'open',os.open), patch.object(sys,'addaudithook',side_effect=lambda hook:
                        install(lambda event,args:observe(hook,event,args))), patch.dict(os.environ,
                        HF_HOME=str(ROOT/'data/hf_cache'),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',
                        HF_DATASETS_OFFLINE='1',TOKENIZERS_PARALLELISM='false',TMPDIR=temporary):
                    install_file_policy(output)
                    try:
                        with open(os.devnull,'w') as null:null.write('discard')
                        import torch
                        torch.set_num_threads(1)
                        from transformers import AutoConfig, AutoTokenizer
                        options = dict(revision=revision,cache_dir=str(cache),local_files_only=True)
                        config = AutoConfig.from_pretrained('Qwen/Qwen2.5-3B',**options)
                        tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen2.5-3B',**options)
                        tokens = tokenizer('C10X cached tokenizer CPU control',return_tensors='pt')
                        self.assertEqual(config.model_type,'qwen2')
                        self.assertTrue(all(v.device.type=='cpu' for v in tokens.values()))
                        self.assertGreater(tokens['input_ids'].numel(),0)
                        self.assertLess(int(tokens['input_ids'].max()),config.vocab_size)
                        self.assertEqual(A.environment_identity()['model_rev'],revision)
                        self.assertEqual(refusals,[], 'Startup must not silently catch policy refusals')
                        runtime = Path(temporary)/'runtime'
                        runtime.write_text('permitted')
                        runtime.unlink()
                    except PermissionError as exc:self.fail('CACHE_LOAD_FALSE_REFUSAL '+str(exc))
                    finally:active[0] = False
                self.assertEqual(before,{p.name:A.sha_file(p) for p in snapshot.iterdir() if p.suffix=='.json'})
                # The Rust tokenizer reads tokenizer.json outside Python's audit hook.
                self.assertIn(str((snapshot/'config.json').resolve()),reads)
                self.assertIn(str((snapshot/'tokenizer_config.json').resolve()),reads)
                print('REAL CACHED TOKENIZER/CONFIG CPU ONLY; no model loader invoked; no audited weight-shard reads')
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CacheTests))
    return 0 if result.wasSuccessful() else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selftest',action='store_true')
    parser.add_argument('--cache-selftest',action='store_true')
    parser.add_argument('--templates',type=Path,default=ROOT/'experiments/c10x/runs/c10x_enginepath/context_templates.json')
    parser.add_argument('--templates-sha256')
    parser.add_argument('--source-run',type=Path,default=ROOT/'experiments/c10x/runs/c10x_enginepath/run.json')
    parser.add_argument('--out',type=Path)
    args = parser.parse_args(argv)
    if args.selftest:return selftest()
    if args.cache_selftest:return cache_selftest()
    if args.templates_sha256 is None:raise ValueError('explicit --templates-sha256 is required')
    ctx,templates = load_templates(args.templates,args.templates_sha256)  # Before model loading or output creation.
    A.environment_preflight()
    if 'C10X_TELEMETRY' in os.environ:raise ValueError('probe requires telemetry unset')
    from c10x_enginepath_read import strict_json
    source = strict_json(args.source_run.read_bytes())
    if (not args.source_run.is_absolute() or args.source_run.resolve()!=ROOT/'experiments/c10x/runs/c10x_enginepath/run.json' or
            source.get('status')!='HALTED' or source.get('process')!=1 or
            source.get('code')!='W0 X2-vii exact zero' or source.get('ctx_sha256')!=A.json_sha(ctx)):
        raise ValueError('original HALTED source-run/context identity required')
    sources = A.source_hashes()
    if sources['experiments/c10x/design/C10X_ENGINEPATH_PREREG.md']!=A.PIN:raise ValueError('PREREG SHA mismatch')
    source_sha = A.sha_file(args.source_run)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    base = ROOT/'experiments/c10x/runs/c10x_x2_probe'
    output = fresh_output(args.out or base/stamp,base)
    sys.dont_write_bytecode = True
    os.environ.update(HF_HOME=str(ROOT/'data/hf_cache'),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',
                      HF_DATASETS_OFFLINE='1',TOKENIZERS_PARALLELISM='false',TMPDIR=str(output))
    import tempfile
    tempfile.tempdir = str(output)
    install_file_policy(output)
    provenance = {'source_run':{'path':str(args.source_run),'sha256':source_sha,'status':source['status'],
                    'code':source['code'],'recorded_w0':source.get('w0'),'recorded_identity':source.get('identity')},
                  'sources_before':sources,'probe_sha256':A.sha_file(__file__),
                  'mps_copy_audit_sha256':A.sha_file(ROOT/'knowledge/analyses/mps_offset_conversion_audit.md'),
                  'historical_identity_limit':'run.json has no W0 or model identity; no historical equality claim',
                  'started_at':A.utc(),'templates':templates,'telemetry':False}
    harness = None
    previous_cwd = Path.cwd()
    record,code = {'schema':'c10x_x2_probe/v1','status':'INCOMPLETE'},1
    try:
        with (output/'probe.log').open('x',buffering=1) as log, contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
            # c10e sets HF_HUB_OFFLINE=0; capture the offline library constant BEFORE importing it.
            import huggingface_hub.constants as hf_constants
            if not hf_constants.HF_HUB_OFFLINE:raise ValueError('offline hub constant required')
            import torch
            torch.set_num_threads(1)
            harness = A.load_harness()
            os.environ['HF_HUB_OFFLINE'] = '1'
            A.configure(harness)
            hp = harness.MEMITHyperParams.from_json(str(ROOT/'code/configs/hparams/qwen25_3b_memit_hparams.json'))
            provenance.update(environment=A.environment_identity(),model_id=harness.ID,model_revision=harness.REV,
                              device=str(harness.DEV),hparams=vars(hp),engine_fingerprint=A.fingerprint())
            record = probe(harness,hp,args.templates,args.templates_sha256)
            A.verify_sources(sources,A.source_hashes())
            if A.sha_file(args.source_run)!=source_sha or A.sha_file(args.templates)!=args.templates_sha256:
                raise ValueError('historical input drift')
            code = 0
    except Exception as exc:
        record = getattr(exc,'probe_record',record)
        record.update(status='INCOMPLETE',error=type(exc).__name__+': '+str(exc))
        print(record['error'],file=sys.stderr)
    finally:
        if harness is not None:A.release(harness)
        os.chdir(previous_cwd)
        record.update(provenance=provenance,finished_at=A.utc())
        A.write_json(output/'probe.json',A.diagnostic_json(record))
    print(output/'probe.json')
    return code


if __name__=='__main__':
    raise SystemExit(main())
