"""CPU-only contracts for the frozen C10Y pre-cast diagnostic; no live dispatch."""
import os, sys
from pathlib import Path
W = Path(__file__).resolve().parents[3]
sys.dont_write_bytecode = True

def guard(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        p = Path(os.fsdecode(args[0])).resolve()
        writing = any(c in (args[1] or '') for c in 'wax+') or bool(args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if writing and (p == W or W in p.parents):
            raise PermissionError('precast selftest live-tree write refused')
    if event == 'subprocess.Popen':
        argv = args[1]
        if not os.environ.get('C10Y_ALLOWED_CHILD_TESTS') == '1':
            raise PermissionError('CPU child tests require C10Y_ALLOWED_CHILD_TESTS=1')
        if not all('/private/tmp/c10y_build/' in str(x) for x in argv[1:] if str(x).endswith(('.py', '.sh'))):
            raise PermissionError('non-stub child refused')
sys.addaudithook(guard)

import ast, contextlib, copy, hashlib, importlib.util, inspect, json, signal, subprocess, tempfile, time, types, unittest
from unittest import mock
import torch
torch.set_num_threads(1)
def forbidden(*args, **kwargs): raise AssertionError('accelerator/model operation forbidden')
torch.mps.synchronize = torch.mps.empty_cache = torch.cuda.synchronize = forbidden
torch.manual_seed = lambda seed: torch.random.default_generator.manual_seed(seed)
class ImportsDenied:
    def find_spec(self, fullname, *args):
        if fullname.split('.')[0] in ('transformers', 'datasets', 'c10e_bandknob'):
            raise AssertionError('model import forbidden: ' + fullname)
sys.meta_path.insert(0, ImportsDenied())
import c10y_directdw_arms as A
module_path = W / 'code/lab/track_c/c10y_precast_diag.py'
if module_path.exists():
    import c10y_precast_diag as D
else:
    D = None

def original_function(rel, name, globals_):
    source = W / rel
    tree = ast.parse(source.read_text())
    node = next(n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), 'exec'), globals_)
    return globals_[name]

def harness():
    h = types.SimpleNamespace()
    h.hp = types.SimpleNamespace(layers=[4,5,6,7,8], layer_module_tmp='layers.{}', fact_token='subject_last')
    h.model = torch.nn.Module(); h.model.layers = torch.nn.ModuleDict({str(l): torch.nn.Linear(3,2,bias=False) for l in h.hp.layers})
    for p in h.model.parameters():
        with torch.no_grad(): p.fill_(0.25)
    h.DEV = 'cpu'; h.tok = None; h.L2 = 1.; h.PROJECTOR = 'nullspace'
    h._CANDIDATE_RECIPE = False; h._LAW5_DEFAULT_CTX = False
    h.Z_OVERRIDE_HITS = 0; h.Z_OVERRIDE = {('s1',' v1'): torch.tensor([1.,2.]), ('s2',' v2'): torch.tensor([2.,1.])}
    h.ARM_HOOKS = []; h._ARM_STATE = None
    h.weight_name = lambda hp,l: 'layers.%d.weight'%l
    h.snap_layers = lambda hp: {l: h.model.layers[str(l)].weight.detach().clone() for l in hp.layers}
    def restore(hp, snap):
        with torch.no_grad():
            for l in hp.layers: h.model.layers[str(l)].weight.copy_(snap[l])
    h.restore_layers = restore
    h.compute_ks = lambda model,tok,requests,hp,layer,ctx: torch.tensor([[1.,0.,1.],[0.,1.,1.]])
    h.get_module_input_output_at_words = lambda *args,**kwargs: (None, torch.zeros(2,2))
    ns = h.__dict__; ns['torch'] = torch; ns['os'] = os; ns['CONTEXT_TEMPLATES_CACHE'] = [['{}']]
    exec('def get_context_templates(model,tok): return CONTEXT_TEMPLATES_CACHE', ns)
    original_function('code/memit/vendor/memit/memit_main.py', 'upd_matrix_match_shape', ns)
    original_function('code/lab/track_c/c10e_bandknob.py', 'my_edit', ns)
    h.my_edit = ns['my_edit']; h.get_context_templates = ns['get_context_templates']
    requests = [{'prompt':'The capital of {}','subject':s,'target_new':{'str':v}} for s,v in h.Z_OVERRIDE]
    return h, requests

def packet():
    k = torch.tensor([[1.,2.],[0.,1.],[2.,0.]], dtype=torch.float32)
    p = torch.eye(3); c = torch.zeros(3,3); r = torch.tensor([[1.,2.],[3.,4.]])
    m = p@(k@k.T+c)+torch.eye(3); q = p@k; b = q@r.T
    return dict(K=k, R=r, P=p, C=c, L2=1., M=m, Q=q, B=b,
                direct_solution=torch.linalg.solve(m,b), X=torch.linalg.solve(m,q), W0=torch.full((2,3),.25,dtype=torch.float16))

def with_original_representations(h,requests):
    class Tokens(dict):
        def to(self,device):return self
    class Tokenizer:
        padding_side='right';pad_token_id=0
        def __call__(self,contexts,**kwargs):
            self.last=len(contexts)
            return Tokens(input_ids=torch.arange(len(contexts)*4).reshape(len(contexts),4),attention_mask=torch.ones(len(contexts),4,dtype=torch.int64))
    tok=Tokenizer();h.tok=tok
    class Trace:
        def __init__(self,**kwargs):pass
        def __enter__(self):
            self.input=torch.ones(tok.last,4,3);self.output=torch.zeros(tok.last,4,2);return self
        def __exit__(self,*args):pass
    ns={'torch':torch,'List':__import__('typing').List,'AutoModelForCausalLM':object,'AutoTokenizer':object,'nethook':types.SimpleNamespace(Trace=Trace)}
    fn=original_function('code/memit/vendor/rome/repr_tools.py','get_reprs_at_idxs',ns)
    h._PRECAST_REPR=types.SimpleNamespace(get_reprs_at_idxs=fn)
    h.model.forward=lambda **kwargs:None
    h.compute_ks=lambda model,tok,requests,hp,layer,ctx:fn(model,tok,[r['prompt'].format(r['subject']) for r in requests],[[2] for r in requests],layer,hp.layer_module_tmp,track='in')
    h.get_module_input_output_at_words=lambda model,tok,layer,context_templates,words,module_template,fact_token_strategy:(None,fn(model,tok,[t.format(w) for t,w in zip(context_templates,words)],[[2] for w in words],layer,module_template,track='out'))
    return h

def evidence():
    cells = []
    for arm in ('A7_coined_coined','A1_single'):
        for layer in range(4,9):
            cells.append(dict(arm=arm,layer=layer,operands_equal=True,states_equal=True,repeats_stable=True,
                              cpu_realized_identical=True,mps_realized_identical=False if arm=='A7_coined_coined' and layer==4 else True,
                              discrepancies=[]))
    return dict(requirements={k:True for k in ('capture','source_identity','observer','persistence','finiteness','resource','deadline','cleanup')},cells=cells)

class Contracts(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
        Path('/private/tmp/c10y_build').mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir='/private/tmp/c10y_build'); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve(); self.j = D.Journal(self.root)

    def test_R_requires_every_cell_and_A7_device_difference(self):
        e=evidence(); self.assertEqual(D.classify(e)['label'],'R')
        e['cells'][-1]['cpu_realized_identical']=False
        self.assertEqual(D.classify(e)['label'],'UNCLASSIFIED')
        e=evidence()
        for c in e['cells']: c['mps_realized_identical']=True
        e['cells'][-1]['mps_realized_identical']=False
        self.assertEqual(D.classify(e)['label'],'UNCLASSIFIED')

    def test_INCONCLUSIVE_precedes_every_other_reading(self):
        for key in evidence()['requirements']:
            e=evidence(); e['requirements'][key]=False
            with self.subTest(requirement=key): self.assertEqual(D.classify(e)['label'],'INCONCLUSIVE')
        e=evidence(); e['cells'].pop(); self.assertEqual(D.classify(e)['label'],'INCONCLUSIVE')
        e=evidence(); e['cells'][1]=e['cells'][0]; self.assertEqual(D.classify(e)['label'],'INCONCLUSIVE')

    def test_S_needs_direct_trace_evidence_and_K_never_emitted(self):
        e=evidence(); e['cells'][0]['operands_equal']=False
        e['cells'][0]['discrepancies']=[{'kind':'operand','field':'K','left':'native_A.pt','right':'native_Y.pt'}]
        self.assertEqual(D.classify(e)['label'],'S')
        e['requirements']['observer']=False; self.assertEqual(D.classify(e)['label'],'INCONCLUSIVE')
        e=evidence(); e['cells'][0]['cpu_realized_identical']=False; e['condition_number']=1e99; e['precision_gap']=1e-30
        self.assertEqual(D.classify(e)['label'],'UNCLASSIFIED')

    def test_gate_inputs_fsynced_and_reloaded_before_predicate(self):
        p=packet(); observed=[]
        def gate(value):
            record=json.loads((self.root/'gate.json').read_text()); side=record['artifacts']
            observed.append(torch.load(self.root/next(iter(side)),weights_only=True)['tensor_0'])
            return False
        with mock.patch.object(os,'fsync',wraps=os.fsync) as sync:
            with self.assertRaisesRegex(A.Halt,'FORCED-HALT'):
                self.j.gate('gate',{'offending':p['K']},gate,'FORCED-HALT')
        self.assertTrue(sync.called); self.assertTrue(torch.equal(observed[0],p['K']))
        self.assertEqual(json.loads((self.root/'gate_outcome.json').read_text())['passed'],False)

    def test_exclusive_JSON_and_tensor_collision_have_no_sibling(self):
        for suffix in ('.json','.pt'):
            with self.subTest(suffix=suffix):
                out=self.root/('old'+suffix);out.write_bytes(b'original')
                with self.assertRaisesRegex(A.Halt,'EXISTING-ARTIFACT'): self.j.record('old',{'operand':torch.ones(2)})
                self.assertEqual(out.read_bytes(),b'original')
                self.assertFalse((self.root/('old'+('.pt' if suffix=='.json' else '.json'))).exists())
                out.unlink()

    def test_interrupted_serialization_is_incomplete_and_retains_previous_values(self):
        self.j.record('earlier',{'v':torch.tensor([3.,4.])})
        with mock.patch.object(A,'save_tensors',side_effect=OSError('disk full')):
            with self.assertRaisesRegex(OSError,'disk full'):
                with self.j.phase('solve'): self.j.record('partial',{'v':torch.ones(2)})
        summary=D.phase_summary(self.root,('solve','compare'))
        self.assertEqual(summary['solve']['status'],'INCOMPLETE'); self.assertEqual(summary['compare']['status'],'NOT-RUN')
        self.assertTrue(torch.equal(torch.load(self.root/'earlier.pt',weights_only=True)['tensor_0'],torch.tensor([3.,4.])))

    def test_nonfinite_operand_persisted_before_halt(self):
        with self.assertRaisesRegex(A.Halt,'NONFINITE'):
            self.j.finite('bad',{'X':torch.tensor([float('nan')])})
        self.assertTrue(torch.isnan(torch.load(self.root/'bad.pt',weights_only=True)['tensor_0'][0]))

    def test_float64_solve_and_promoted_product_are_distinct(self):
        p=packet(); result=D.controls(p,self.j,'cell')
        for name in ('promoted32_product','solve64_direct','solve64_factored','assembled32_direct64','assembled32_factored64'):
            self.assertEqual(result[name].dtype,torch.float64)
        self.assertTrue(torch.equal(result['cpu32_product'],p['R']@p['X'].T))
        expected=torch.linalg.solve(p['M'].double(),p['B'].double()).T
        self.assertTrue(torch.equal(result['assembled32_direct64'],expected))
        self.assertTrue((self.root/'cell_system64.pt').exists())
        self.assertTrue((self.root/'cell_factor_repeat.pt').exists())

    def test_float64_realization_cannot_demote_to_float32(self):
        w=torch.zeros(1,1,dtype=torch.float16)
        # Just above an fp16 midpoint, but rounds to the midpoint in fp32.
        u=torch.tensor([[1.+2.**-11+2.**-30]],dtype=torch.float64)
        value=D.realize(w,u)
        self.assertEqual(float(value[0,0]),1.+2.**-10)
        self.assertEqual(float(A.stored_weight(w,u,1.)[0,0]),1.)

    def test_float64_realization_casts_on_CPU_before_device_transfer(self):
        w=torch.zeros(1,1,dtype=torch.float16);u=torch.tensor([[1.+2.**-11+2.**-30]],dtype=torch.float64)
        actual=A.to_like
        def transfer(t,reference):
            self.assertEqual(t.dtype,torch.float16,'float64 must not be transferred to MPS')
            self.assertEqual(t.device.type,'cpu')
            return actual(t,reference)
        with mock.patch.object(A,'to_like',side_effect=transfer):
            self.assertEqual(float(D.realize(w,u)[0,0]),1.+2.**-10)

    def test_difference_metrics_and_weight_coordinate_columns(self):
        x=torch.tensor([[1.,2.],[3.,4.]]);y=torch.tensor([[1.,1.],[5.,4.]])
        r=D.distance_stats(x,y)
        self.assertAlmostEqual(r['relative_frobenius'],(5./30.)**.5)
        self.assertEqual(r['max_abs'],2.);self.assertEqual(r['different_fraction'],.5)
        self.assertEqual(r['quantiles']['0.5'],.5)
        self.assertEqual(r['columns']['different_fraction'].tolist(),[.5,.5])
        self.assertEqual(r['column_axis'],'weight coordinates')

    def test_device_product_observed_from_original_effective_weight(self):
        p=packet(); got=D.device_product(p['W0'],p['R'],p['X'].T,self.j,'device',device='cpu')
        self.assertTrue(torch.equal(got['update'],p['R']@p['X'].T))
        self.assertTrue(torch.equal(got['weight'],A.effective_weight(p['W0'],p['R'],p['X'].T)))
        self.assertTrue((self.root/'device_product.pt').exists())

    def test_observer_original_code_coverage_off_on_and_native_operands(self):
        h,requests=harness();p=[torch.eye(3) for _ in range(5)];w0=h.snap_layers(h.hp)
        with D.restored(h):
            result=D.native_capture(h,requests,p,self.j,'A7_coined_coined')
        self.assertEqual(len(result['cells']),5)
        self.assertTrue(result['observer_validated'])
        for l in h.hp.layers: self.assertTrue(torch.equal(h.snap_layers(h.hp)[l],w0[l]))
        self.assertEqual(h.Z_OVERRIDE_HITS,0);self.assertIsNone(sys.gettrace())
        for cell in result['cells']:
            self.assertTrue(cell['operands_equal']);self.assertTrue(cell['states_equal'])
        a=D.load_packet(self.root/'operands_A7_coined_coined_L4_A.pt')
        self.assertEqual(a['K'].shape,(3,2));self.assertEqual(a['direct_solution'].shape,(3,2))

    def test_forced_native_halt_preserves_capture_and_cleans_weights_globals(self):
        h,requests=harness();w0=h.snap_layers(h.hp);original=h.my_edit
        calls=[0]; compute=h.compute_ks
        def failing(*args,**kwargs):
            calls[0]+=1
            if calls[0]==2: raise A.Halt('FORCED-NATIVE',{'layer':5})
            return compute(*args,**kwargs)
        h.__dict__['compute_ks']=failing
        with self.assertRaisesRegex(A.Halt,'FORCED-NATIVE'):
            with D.restored(h):
                with D.NativeObserver(h,self.j,'A7_coined_coined','A'):
                    h.my_edit(h.hp,requests,[torch.eye(3) for _ in range(5)],[torch.zeros(3,3) for _ in range(5)])
        self.assertTrue((self.root/'operands_A7_coined_coined_L4_A.pt').exists())
        self.assertIs(h.my_edit,original);self.assertEqual(h.Z_OVERRIDE_HITS,0);self.assertIsNone(sys.gettrace())
        for l in h.hp.layers: self.assertTrue(torch.equal(h.snap_layers(h.hp)[l],w0[l]))

    def test_missing_capture_refuses_instead_of_reimplementing(self):
        h,requests=harness()
        with mock.patch.object(D.NativeObserver,'trace',return_value=None):
            with self.assertRaisesRegex(A.Halt,'OBSERVER-COVERAGE'):
                D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A1_single')

    def test_scope_SHA_drift_refused(self):
        self.assertEqual(D.SCOPE_SHA,'097c662803a94a897dd588c9e1f09c6af7b17a25019c1439ea39844c65f0a9a8')
        self.assertEqual(D.verify_scope(W),D.SCOPE_SHA)
        (self.root/'docs').mkdir();(self.root/'experiments/c10y/design/C10Y_PRECAST_DIAG_SCOPE.md').write_text('drift')
        with self.assertRaisesRegex(A.Halt,'SCOPE'): D.verify_scope(self.root)

    def test_committed_benchmark_pin_accepts_exact_bytes_and_refuses_drift(self):
        rel='code/lab/track_c/c10z_astra_benchmark.py'
        committed=(W/rel).read_bytes()
        self.assertEqual(hashlib.sha256(committed).hexdigest(),'3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041')
        old=committed.replace(b'    import c10z_astra_read as R\n    R.require_a1_freeze(ROOT)\n',b'',1)
        self.assertEqual(hashlib.sha256(old).hexdigest(),'9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a')
        sources=D.source_identity(W)
        cases=(('committed',committed,True),('previous',old,False),
               ('newline',committed+b'\n',False),('changed_byte',b'!'+committed[1:],False),('empty',b'',False))
        for name,payload,accepted in cases:
            with self.subTest(benchmark=name):
                root=self.root/name;out=root/'out';out.mkdir(parents=True)
                for source in sources:
                    dest=root/source;dest.parent.mkdir(parents=True,exist_ok=True)
                    dest.write_bytes((W/source).read_bytes())
                (root/rel).write_bytes(payload)
                with mock.patch.object(D,'ROOT',root), mock.patch.dict(os.environ,{},clear=True), \
                     mock.patch.object(D,'input_manifest',side_effect=A.Halt('PIN-TEST-BOUNDARY','CPU stop before model inputs')):
                    self.assertEqual(D.worker(out),2)
                halt=A.strict_load(out/'worker_halt.json')
                self.assertEqual(halt['code'],'PIN-TEST-BOUNDARY' if accepted else 'SOURCE-IDENTITY')
                self.assertIs(A.strict_load(out/'source_identity_outcome.json')['passed'],accepted)
                self.assertEqual(A.strict_load(out/'source_identity.json')['observed'][rel],hashlib.sha256(payload).hexdigest())
                self.assertFalse((out/'phase_model_load_started.json').exists())

    def test_fresh_namespace_existing_directory_and_symlink_refused(self):
        (self.root/'results').mkdir()
        out=D.claim_namespace(self.root,'20261009T000000Z',123)
        with self.assertRaisesRegex(A.Halt,'EXISTING'): D.claim_namespace(self.root,'20261009T000000Z',123)
        old=(out/'launch.json').read_bytes()
        self.assertEqual((out/'launch.json').read_bytes(),old)
        with self.assertRaisesRegex(A.Halt,'UTC'): D.claim_namespace(self.root,'../../calib4',123)

    def test_fail_closed_gpu_and_fingerprint_records_precede_loader(self):
        for bad in ('gpu','fingerprint'):
            gate=types.SimpleNamespace(check_gpu=lambda:dict(ok=bad!='gpu',reason='fixture'),check_fingerprint=lambda:dict(ok=bad!='fingerprint',output='fixture'))
            with self.assertRaisesRegex(A.Halt,'PRELOAD'):
                D.preload(self.j,gate,lambda: self.fail('loader entered'))
            self.assertTrue((self.root/('preload_'+bad+'.json')).exists())
            for f in self.root.glob('preload*'):f.unlink()

    def test_supervisor_timeout_overrides_worker_success_and_preserves_commits(self):
        self.j.record('operand',{'value':torch.tensor([7.])})
        self.j.record('worker',{'status':'COMPLETED','reading_inputs':evidence()})
        D.finalize(self.root,0,timed_out=True,elapsed_s=3.)
        self.assertEqual(json.loads((self.root/'reading.json').read_text())['label'],'INCONCLUSIVE')
        self.assertEqual(json.loads((self.root/'run.json').read_text())['status'],'INCONCLUSIVE')
        self.assertTrue((self.root/'supervisor_timeout.json').exists())
        self.assertEqual(float(torch.load(self.root/'operand.pt',weights_only=True)['tensor_0'][0]),7.)

    def test_finalizer_incomplete_worker_cannot_publish_R(self):
        self.j.record('worker',{'status':'INCOMPLETE','reading_inputs':evidence()})
        D.finalize(self.root,0,timed_out=False,elapsed_s=1.)
        self.assertEqual(json.loads((self.root/'reading.json').read_text())['label'],'INCONCLUSIVE')

    def test_finalizer_overwrite_refusal_keeps_terminal_bytes(self):
        D.finalize(self.root,2,timed_out=False,elapsed_s=1.)
        before=(self.root/'run.json').read_bytes()
        with self.assertRaisesRegex(A.Halt,'EXISTING'):D.finalize(self.root,2,timed_out=True,elapsed_s=2.)
        self.assertEqual((self.root/'run.json').read_bytes(),before)

    def test_finalizer_rejects_completed_claim_with_incomplete_phases(self):
        self.j.record('worker',{'status':'COMPLETED','reading_inputs':evidence()})
        D.finalize(self.root,0,timed_out=False,elapsed_s=1.)
        self.assertEqual(json.loads((self.root/'reading.json').read_text())['label'],'INCONCLUSIVE')

    def test_finalizer_malformed_worker_preserves_exception_and_inconclusive(self):
        (self.root/'worker.json').write_text('{broken')
        D.finalize(self.root,0,timed_out=False,elapsed_s=1.)
        self.assertEqual(json.loads((self.root/'reading.json').read_text())['label'],'INCONCLUSIVE')
        self.assertIn('exception',json.loads((self.root/'supervisor_halt.json').read_text()))

    def test_valid_complete_phases_publish_threshold_free_R(self):
        for name in D.PHASES:
            with self.j.phase(name): pass
        self.j.record('worker',{'status':'COMPLETED','reading_inputs':evidence()})
        D.finalize(self.root,0,timed_out=False,elapsed_s=1.)
        self.assertEqual(json.loads((self.root/'reading.json').read_text())['label'],'R')

    def test_packet_tamper_refused_before_downstream_consumption(self):
        self.j.record('packet',{'K':torch.ones(2)})
        (self.root/'packet.pt').write_bytes(b'tampered')
        with self.assertRaisesRegex(A.Halt,'PERSISTENCE'):D.load_packet(self.root/'packet.pt')

    def test_actual_representation_batch_padding_and_indices_captured_without_id_assumption(self):
        h,requests=harness();with_original_representations(h,requests)
        with mock.patch.object(D,'id',return_value=17,create=True):
            result=D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A7_coined_coined')
        self.assertTrue(result['observer_validated'])
        for l in range(4,9):
            for path in ('A','Y'):
                value=D.load_packet(self.root/('operands_A7_coined_coined_L%d_%s.pt'%(l,path)))
                self.assertEqual(len(value['batches']),2)
                batch=D.load_record(self.root/value['batches'][0])
                self.assertEqual(batch['tokens']['input_ids'].tolist(),[[0,1,2,3],[4,5,6,7]])
                self.assertEqual(batch['idxs'],[[2],[2]])
                self.assertEqual(batch['padding_side'],'right')

    def test_observer_tensor_inertness_catches_discarded_cur_mutation(self):
        h,requests=harness();old=D.cpu_copy;altered=[False]
        def corrupt(t):
            if not altered[0] and t.shape==(2,2) and torch.equal(t,torch.zeros(2,2)):
                t.add_(1);altered[0]=True
            return old(t)
        with mock.patch.object(D,'cpu_copy',side_effect=corrupt):
            with self.assertRaisesRegex(A.Halt,'OBSERVER-TENSOR-INERTNESS'):
                with D.restored(h),D.NativeObserver(h,self.j,'A1_single','A'):
                    h.my_edit(h.hp,requests,[torch.eye(3) for _ in range(5)],[torch.zeros(3,3) for _ in range(5)])
        self.assertTrue((self.root/'solve_inputs_A1_single_L4_A_direct.pt').exists())

    def test_missing_reference_Q_retains_available_operands_before_coverage_halt(self):
        h,requests=harness();old=D.NativeObserver.mm
        def omit(self,func,args,result):
            old(self,func,args,result)
            for key in list(self.q):
                if key[1]=='Q':del self.q[key]
        with mock.patch.object(D.NativeObserver,'mm',omit):
            with self.assertRaisesRegex(A.Halt,'OBSERVER-COVERAGE'):
                with D.restored(h),D.NativeObserver(h,self.j,'A1_single','A'):
                    h.my_edit(h.hp,requests,[torch.eye(3) for _ in range(5)],[torch.zeros(3,3) for _ in range(5)])
        partial=D.load_packet(self.root/'operands_A1_single_L4_A_incomplete.pt')
        self.assertTrue(torch.equal(partial['K'],torch.tensor([[1.,0.],[0.,1.],[1.,1.]])))
        self.assertIsNone(partial['Q'])

    def test_full_weight_coordinate_quantiles_exceed_torch_limit(self):
        x=torch.zeros(2048,11008,dtype=torch.float16);y=x.clone();y[0,0]=1
        r=D.distance_stats(x,y)
        self.assertEqual(r['columns']['absolute_quantiles'].shape,(7,11008))
        self.assertEqual(r['max_abs'],1.);self.assertIsNone(r['relative_frobenius'])
        self.assertAlmostEqual(r['different_fraction'],1/(2048*11008))

    def test_native_factor_actual_matrix_and_Q_are_compared(self):
        original=D.NativeObserver.trace
        def corrupt(self,frame,event,arg):
            if frame.f_code is self.factor_code and event=='return' and arg is not None:
                frame.f_locals['matrix'].add_(torch.eye(3))
            return original(self,frame,event,arg)
        for arm in D.ARMS:
            h,requests=harness();out=self.root/arm;out.mkdir();journal=D.Journal(out)
            with mock.patch.object(D.NativeObserver,'trace',corrupt):
                with self.assertRaisesRegex(A.Halt,'OBSERVER-SOLVE-INPUT'):
                    with journal.phase('native_'+arm):D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],journal,arm)
            self.assertEqual(D.phase_summary(out)['native_'+arm]['status'],'INCOMPLETE')
            self.assertIsNone(sys.gettrace());self.assertEqual(h.Z_OVERRIDE_HITS,0)
            e=evidence();e['requirements']['observer']=False
            journal.record('worker',{'status':'INCOMPLETE','reading_inputs':e})
            D.finalize(out,2,False,1.)
            self.assertEqual(D.load_record(out/'reading.json')['label'],'INCONCLUSIVE')

    def test_native_direct_solve_failure_retains_inputs_and_original_exception(self):
        for path in ('A','Y'):
            h,requests=harness();out=self.root/path;out.mkdir();journal=D.Journal(out)
            error=RuntimeError('ASTRA-DIRECT-SOLVE-FAIL');at_call={}
            name='solve_inputs_A7_coined_coined_L4_'+path+'_direct'
            def fail(matrix,rhs):
                at_call.update(M=D.cpu_copy(matrix),RHS=D.cpu_copy(rhs),durable=(out/(name+'.json')).exists())
                raise error
            with mock.patch.object(torch.linalg,'solve',side_effect=fail):
                with self.assertRaises(RuntimeError) as caught:
                    with journal.phase('native_A7_coined_coined'),D.restored(h),D.NativeObserver(h,journal,'A7_coined_coined',path):
                        if path=='A':h.my_edit(h.hp,requests,[torch.eye(3) for _ in range(5)],[torch.zeros(3,3) for _ in range(5)])
                        else:A.capture_solve(h,h.hp,requests,[torch.eye(3) for _ in range(5)],[torch.zeros(3,3) for _ in range(5)])
            self.assertIs(caught.exception,error);self.assertTrue(at_call['durable'],'M/RHS absent before direct solve')
            value=D.load_record(out/(name+'.json'))
            self.assertTrue(D.exact(value['M'],at_call['M']));self.assertTrue(D.exact(value['RHS'],at_call['RHS']))
            self.assertIn('K',value);self.assertIn('cur',value);self.assertIn('C',value)
            failure=D.load_record(out/('native_exception_A7_coined_coined_L4_'+path+'_edit.json'))
            self.assertEqual(failure['detail'],str(error));self.assertEqual(failure['exception'],'RuntimeError')
            self.assertTrue(D.exact(failure['locals']['A' if path=='A' else 'matrix'],at_call['M']))
            self.assertEqual(D.phase_summary(out)['native_A7_coined_coined']['status'],'INCOMPLETE')
            self.assertEqual(h.Z_OVERRIDE_HITS,0);self.assertIsNone(sys.gettrace())
            self.assertTrue(all(torch.equal(t,torch.full_like(t,.25)) for t in h.snap_layers(h.hp).values()))

    def test_native_factor_solve_failure_retains_inputs_and_original_exception(self):
        h,requests=harness();error=RuntimeError('ASTRA-FACTOR-SOLVE-FAIL');at_call={};old=torch.linalg.solve
        name='solve_inputs_A7_coined_coined_L4_Y_factor'
        # mock's wrapper is between the original caller and this callback.
        def solve(matrix,rhs):
            frame=inspect.currentframe().f_back
            while frame is not None and frame.f_code not in (A.capture_solve.__code__,A.factor_solve.__code__):frame=frame.f_back
            if frame is not None and frame.f_code is A.factor_solve.__code__:
                at_call.update(M=D.cpu_copy(matrix),RHS=D.cpu_copy(rhs),durable=(self.root/(name+'.json')).exists());raise error
            return old(matrix,rhs)
        with mock.patch.object(torch.linalg,'solve',side_effect=solve):
            try:
                with self.j.phase('native_A7_coined_coined'),D.restored(h),D.NativeObserver(h,self.j,'A7_coined_coined','Y'):
                    A.capture_solve(h,h.hp,requests,[torch.eye(3) for _ in range(5)],[torch.zeros(3,3) for _ in range(5)])
            except BaseException as caught:self.assertIs(caught,error,'native factor failure was replaced')
            else:self.fail('factor failure not reached')
        self.assertTrue(at_call['durable'],'M/Q absent before factor solve')
        value=D.load_record(self.root/(name+'.json'))
        self.assertTrue(D.exact(value['M'],at_call['M']));self.assertTrue(D.exact(value['RHS'],at_call['RHS']))
        failure=D.load_record(self.root/'native_exception_A7_coined_coined_L4_Y_factor.json')
        self.assertEqual(failure['detail'],str(error));self.assertEqual(failure['exception'],'RuntimeError')
        self.assertTrue(D.exact(failure['locals']['matrix'],at_call['M']))
        self.assertEqual(D.phase_summary(self.root)['native_A7_coined_coined']['status'],'INCOMPLETE')
        self.assertEqual(h.Z_OVERRIDE_HITS,0);self.assertIsNone(sys.gettrace())
        self.assertTrue(all(torch.equal(t,torch.full_like(t,.25)) for t in h.snap_layers(h.hp).values()))

    def test_observer_off_failure_retains_prior_native_input_capture(self):
        h,requests=harness();old=torch.linalg.solve;error=RuntimeError('OBSERVER-OFF-SOLVE-FAIL')
        def solve(matrix,rhs):
            if sys.gettrace() is None:raise error
            return old(matrix,rhs)
        with mock.patch.object(torch.linalg,'solve',side_effect=solve):
            with self.assertRaises(RuntimeError) as caught:
                with self.j.phase('native_A1_single'):D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A1_single')
        self.assertIs(caught.exception,error)
        self.assertTrue((self.root/'solve_inputs_A1_single_L4_A_direct.json').exists())
        self.assertEqual(D.phase_summary(self.root)['native_A1_single']['status'],'INCOMPLETE')
        self.assertIsNone(sys.gettrace());self.assertEqual(h.Z_OVERRIDE_HITS,0)

    def test_actual_native_solve_inputs_are_fsynced_before_execution(self):
        h,requests=harness();old_solve=torch.linalg.solve;old_sync=os.fsync;synced=set();calls=[]
        def sync(fd):
            result=old_sync(fd);stat=os.fstat(fd);synced.add((stat.st_dev,stat.st_ino));return result
        def solve(matrix,rhs):
            frame=inspect.currentframe().f_back
            while frame is not None and frame.f_code not in (h.my_edit.__code__,A.capture_solve.__code__,A.factor_solve.__code__):frame=frame.f_back
            self.assertIsNotNone(frame)
            kind='factor' if frame.f_code is A.factor_solve.__code__ else 'direct'
            parent=frame.f_back if kind=='factor' else frame
            path='A' if parent.f_code is h.my_edit.__code__ else 'Y';layer=parent.f_locals['layer']
            record=self.root/('solve_inputs_A1_single_L%d_%s_%s.json'%(layer,path,kind))
            payload=json.loads(record.read_text())
            for file in (record,record.with_suffix('.pt'),self.root):
                stat=file.stat();self.assertIn((stat.st_dev,stat.st_ino),synced,'not fsynced before native solve: '+str(file))
            value=D.load_record(record)
            self.assertTrue(D.exact(value['M'],matrix));self.assertTrue(D.exact(value['RHS'],rhs))
            self.assertEqual(payload['tensor_metadata']['M']['sha256'],A.tensor_sha(matrix))
            calls.append((layer,path,kind,sys.gettrace() is not None))
            return old_solve(matrix,rhs)
        with mock.patch.object(os,'fsync',side_effect=sync),mock.patch.object(torch.linalg,'solve',side_effect=solve):
            result=D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A1_single')
        self.assertTrue(result['observer_validated']);self.assertEqual(len(calls),30)
        self.assertEqual(sum(on for *_,on in calls),15)

    def test_observer_factor_Q_copy_mutation_invalidates_evidence(self):
        h,requests=harness();old=D.NativeObserver.mm
        def corrupt(self,func,args,result):
            old(self,func,args,result)
            for key in self.q:
                if key[1]=='factor_Q':self.q[key].add_(1)
        with mock.patch.object(D.NativeObserver,'mm',corrupt):
            with self.assertRaisesRegex(A.Halt,'OBSERVER-SOLVE-INPUT'):
                with self.j.phase('native_A1_single'):D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A1_single')
        self.assertEqual(D.phase_summary(self.root)['native_A1_single']['status'],'INCOMPLETE')
        self.assertIsNone(sys.gettrace());self.assertEqual(h.Z_OVERRIDE_HITS,0)

    def test_observer_direct_M_mutation_at_return_invalidates_evidence(self):
        h,requests=harness();old=D.NativeObserver.trace
        def corrupt(self,frame,event,arg):
            if frame.f_code is self.shape_code and event=='return' and frame.f_back.f_code is self.edit_code:
                frame.f_back.f_locals['A' if self.path=='A' else 'matrix'].add_(torch.eye(3))
            return old(self,frame,event,arg)
        with mock.patch.object(D.NativeObserver,'trace',corrupt):
            with self.assertRaisesRegex(A.Halt,'OBSERVER-SOLVE-INPUT'):
                with self.j.phase('native_A1_single'):D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A1_single')
        self.assertEqual(D.phase_summary(self.root)['native_A1_single']['status'],'INCOMPLETE')
        self.assertIsNone(sys.gettrace());self.assertEqual(h.Z_OVERRIDE_HITS,0)

    def test_phase_failure_publication_preserves_original_exception(self):
        error=RuntimeError('ORIGINAL-PHASE-FAILURE');old=self.j.record
        def failed_sink(name,value):
            if name.endswith('_failed'):raise OSError('CPU-SINK-FAILURE')
            return old(name,value)
        with mock.patch.object(self.j,'record',side_effect=failed_sink):
            try:
                with self.j.phase('native_A1_single'):raise error
            except BaseException as caught:self.assertIs(caught,error)
            else:self.fail('phase failure not propagated')
        self.assertEqual(D.phase_summary(self.root)['native_A1_single']['status'],'INCOMPLETE')
        self.assertIn('CPU-SINK-FAILURE',' '.join(error.__notes__))

    def test_genuine_native_operand_discrepancy_remains_valid_S_evidence(self):
        cells=[]
        for arm in D.ARMS:
            h,requests=harness();old=h.compute_ks
            def native_key(*args):
                value=old(*args)
                if inspect.currentframe().f_back.f_code is A.capture_solve.__code__:value=value+1
                return value
            h.compute_ks=native_key
            result=D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,arm)
            self.assertTrue(result['observer_validated'])
            cells.extend({**c,'repeats_stable':True,'cpu_realized_identical':False,'mps_realized_identical':False} for c in result['cells'])
        e=evidence();e['cells']=cells
        self.assertEqual(D.classify(e)['label'],'S')

    def test_native_missing_factor_Q_is_inconclusive_capture_failure(self):
        h,requests=harness();old=D.NativeObserver.mm
        def omit(self,func,args,result):
            old(self,func,args,result)
            for key in list(self.q):
                if key[1]=='factor_Q':del self.q[key]
        with mock.patch.object(D.NativeObserver,'mm',omit):
            with self.assertRaisesRegex(A.Halt,'OBSERVER-COVERAGE'):
                D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A1_single')

    def test_restores_optional_recorder_and_preexisting_hook_on_halt(self):
        h,requests=harness();sentinel=object();h._C10Y_PREFIX_SAVE=sentinel
        registry=h.model._forward_hooks;registry[999]=sentinel
        with self.assertRaisesRegex(A.Halt,'FORCED'):
            with D.restored(h):
                h._C10Y_PREFIX_SAVE=lambda *a:None;registry.clear();raise A.Halt('FORCED')
        self.assertIs(h._C10Y_PREFIX_SAVE,sentinel);self.assertIs(registry[999],sentinel)

    def test_realized_native_saved_factors_drive_R_predicate(self):
        h,requests=harness();D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A7_coined_coined')
        result=D.compare_cell(h,self.j,dict(arm='A7_coined_coined',layer=4,operands_equal=True,states_equal=True,discrepancies=[]))
        updates=D.load_packet(self.root/'updates_A7_coined_coined_L4.pt')
        factors=D.load_record(self.root/'factors_A7_coined_coined_L4_Y.json')
        self.assertTrue(torch.equal(updates['native_cpu32_product'],factors['R']@factors['X'].T))
        self.assertIn('native_cpu32_product',D.load_record(self.root/'controls_A7_coined_coined_L4_numeric.json')['realized_weights'])
        numeric=D.load_record(self.root/'controls_A7_coined_coined_L4_numeric.json')
        self.assertEqual(set(numeric['condition_numbers']),{'recipe_A','C10Y'})
        self.assertEqual(set(numeric['float64_errors']),{'recipe_A','native_cpu32_product','native_device'})

    def test_completed_native_CPU_product_survives_later_control_halt(self):
        h,requests=harness();D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A7_coined_coined')
        with mock.patch.object(D,'controls',side_effect=A.Halt('FORCED-CONTROL')):
            with self.assertRaisesRegex(A.Halt,'FORCED-CONTROL'):
                D.compare_cell(h,self.j,dict(arm='A7_coined_coined',layer=4,operands_equal=True,states_equal=True,discrepancies=[]))
        value=D.load_record(self.root/'controls_A7_coined_coined_L4_native_cpu32_product.json')
        factors=D.load_record(self.root/'factors_A7_coined_coined_L4_Y.json')
        self.assertTrue(torch.equal(value['update'],factors['R']@factors['X'].T))

    def test_native_direct_update_included_in_all_pair_measurements(self):
        h,requests=harness();D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A7_coined_coined')
        D.compare_cell(h,self.j,dict(arm='A7_coined_coined',layer=4,operands_equal=True,states_equal=True,discrepancies=[]))
        updates=D.load_packet(self.root/'updates_A7_coined_coined_L4.pt')
        self.assertIn('native_direct',updates)
        native=D.load_packet(self.root/'operands_A7_coined_coined_L4_Y.pt')
        self.assertTrue(torch.equal(updates['native_direct'],native['update']))
        numeric=D.load_record(self.root/'controls_A7_coined_coined_L4_numeric.json')
        self.assertEqual(len(numeric['pairs']),len(updates)*(len(updates)-1)//2)

    def test_repeat_factor_compared_to_original_native_solution(self):
        h,requests=harness();D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A7_coined_coined')
        old=A.factor_solve
        def changed(*args):
            value=old(*args);value['X'].add_(.001);return value
        with mock.patch.object(A,'factor_solve',side_effect=changed):
            value=D.compare_cell(h,self.j,dict(arm='A7_coined_coined',layer=4,operands_equal=True,states_equal=True,discrepancies=[]))
        self.assertFalse(value['repeats_stable'])

    def test_completed_float64_direct_solution_survives_next_solve_failure(self):
        old=torch.linalg.solve;calls=[0]
        def fail_second(*args):
            calls[0]+=1
            if calls[0]==2:raise A.Halt('FORCED-FACTOR-SOLVE')
            return old(*args)
        p=packet()
        with mock.patch.object(torch.linalg,'solve',side_effect=fail_second):
            with self.assertRaisesRegex(A.Halt,'FORCED-FACTOR-SOLVE'):D.controls(p,self.j,'test')
        value=D.load_record(self.root/'test_direct_solution64.json')
        self.assertTrue(torch.equal(value['solution'],old(p['M'].double(),p['B'].double())))

    def target_fixture(self):
        h,_=harness();requests={arm:[{'prompt':'The capital of {}','subject':'s%d'%i,'target_new':{'str':' '+arm+'_v%d'%i}} for i in range(24)] for arm in D.ARMS}
        pristine={name:D.cpu_copy(t) for name,t in h.model.named_parameters()}
        h.compute_z=lambda model,tok,rq,hp,layer,contexts:torch.tensor([float(rq['subject'][1:])+1.,2.])
        h.compute_ks=lambda model,tok,requests,hp,layer,ctx:torch.ones(len(requests),3)
        h.get_module_input_output_at_words=lambda *args,**kwargs:(None,torch.zeros(len(kwargs['words']),2))
        return h,requests,pristine

    def test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths(self):
        self.assertTrue(hasattr(D,'compute_targets'),'missing isolated target persistence boundary')
        h,requests,pristine=self.target_fixture();calls=[];old=h.compute_z
        def solve(*args):calls.append((args[2],args[5]));return old(*args)
        h.compute_z=solve;contexts=[['{}']]
        with mock.patch.object(A,'sample_memory',return_value={}):
            targets=D.compute_targets(h,self.j,requests,contexts,pristine)
        self.assertEqual(len(calls),48);self.assertTrue(all(c[1] is contexts for c in calls))
        self.assertEqual(len(targets),48);self.assertTrue((self.root/'targets.pt').is_file())
        self.assertEqual(len(list(self.root.glob('target_*.pt'))),48)
        h.Z_OVERRIDE=targets
        for arm in D.ARMS:
            D.native_capture(h,requests[arm],[torch.eye(3) for _ in range(5)],self.j,arm)
            expected=torch.stack([targets[(r['subject'],r['target_new']['str'])] for r in requests[arm]],dim=1)/5
            for path in ('A','Y'):
                value=D.load_packet(self.root/('operands_'+arm+'_L4_'+path+'.pt'))
                self.assertTrue(torch.equal(value['R'],expected))
        self.assertEqual(len(calls),48)

    def test_target_failure_retains_completed_prefix_and_NOT_RUN_arm(self):
        self.assertTrue(hasattr(D,'compute_targets'),'missing isolated target persistence boundary')
        h,requests,pristine=self.target_fixture();old=h.compute_z;calls=[0]
        def solve(*args):
            calls[0]+=1
            if calls[0]==3:raise A.Halt('TARGET-STOP')
            return old(*args)
        h.compute_z=solve
        with mock.patch.object(A,'sample_memory',return_value={}):
            with self.assertRaisesRegex(A.Halt,'TARGET-STOP'):
                with D.restored(h):D.compute_targets(h,self.j,requests,[['{}']],pristine)
        self.assertEqual(calls[0],3)
        self.assertTrue(torch.equal(D.load_record(self.root/'target_A7_coined_coined_01.json')['value'],torch.tensor([2.,2.])))
        phases=D.phase_summary(self.root)
        self.assertEqual(phases['targets_A7_coined_coined']['status'],'INCOMPLETE')
        self.assertEqual(phases['targets_A1_single']['status'],'NOT-RUN')
        self.assertFalse((self.root/'targets.pt').exists())

    def test_target_mutation_halt_retains_offending_value_and_restores_weights(self):
        self.assertTrue(hasattr(D,'compute_targets'),'missing isolated target persistence boundary')
        h,requests,pristine=self.target_fixture();old=h.compute_z
        def solve(*args):
            with torch.no_grad():next(h.model.parameters()).add_(1)
            return old(*args)
        h.compute_z=solve
        with mock.patch.object(A,'sample_memory',return_value={}):
            with self.assertRaisesRegex(A.Halt,'TARGET-BASE-MUTATION'):
                with D.restored(h,pristine):D.compute_targets(h,self.j,requests,[['{}']],pristine)
        value=D.load_record(self.root/'target_A7_coined_coined_00.json')
        self.assertTrue(torch.equal(value['value'],torch.tensor([1.,2.])))
        self.assertTrue(all(torch.equal(t,pristine[name]) for name,t in h.model.named_parameters()))

    def test_malformed_classification_capture_is_INCONCLUSIVE(self):
        cases=[]
        e=evidence();e['requirements']=None;cases.append(e)
        e=evidence();e['cells'][0]=None;cases.append(e)
        e=evidence();e['cells'][0]['operands_equal']=False;e['cells'][0]['discrepancies']=[None];cases.append(e)
        for value in cases:
            with self.subTest(value=value):self.assertEqual(D.classify(value)['label'],'INCONCLUSIVE')

    def test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker(self):
        self.run_shell_stub('hang')

    def test_real_shell_supervisor_worker_exit_before_start_is_diagnosed(self):
        self.run_shell_stub('early_exit')

    def test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic(self):
        self.run_shell_stub('prepare_hang')

    def test_real_shell_existing_namespace_refused_without_finalizer(self):
        self.run_shell_stub('existing')

    def test_real_shell_worker_log_collision_refused_without_overwrite(self):
        self.run_shell_stub('log_collision')

    def test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic(self):
        self.run_shell_stub('finalizer_hang')

    def test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE(self):
        self.run_shell_stub('interrupt_TERM')

    def test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE(self):
        self.run_shell_stub('interrupt_INT')

    def test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE(self):
        self.run_shell_stub('interrupt_HUP')

    def test_inherited_ignored_HUP_refused_before_owned_children(self):
        self.run_shell_stub('inherited_ignore','HUP')

    def test_inherited_ignored_INT_refused_before_owned_children(self):
        self.run_shell_stub('inherited_ignore','INT')

    def test_inherited_ignored_TERM_refused_before_owned_children(self):
        self.run_shell_stub('inherited_ignore','TERM')

    def test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE(self):
        self.run_shell_stub('abnormal')

    def test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic(self):
        self.run_shell_stub('finalizer_fail')

    def test_real_shell_owned_process_group_is_stopped_after_leader_exit(self):
        self.run_shell_stub('leader_exit')

    def test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed(self):
        self.run_shell_stub('interrupt_publication_hang')

    def test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE(self):
        self.j.record('reading',{'label':'S'});self.j.record('run',{'status':'S'})
        before={n:(self.root/n).read_bytes() for n in ('reading.json','run.json')}
        D.interrupted_terminal(self.root,143,3.,'TERM')
        self.assertEqual(D.load_record(self.root/'supervisor_interruption.json')['label'],'INCONCLUSIVE')
        self.assertEqual(D.load_record(self.root/'interrupted_reading.json')['label'],'INCONCLUSIVE')
        self.assertEqual(D.load_record(self.root/'interrupted_run.json')['status'],'INCONCLUSIVE')
        for name,data in before.items():self.assertEqual((self.root/name).read_bytes(),data)
        with self.assertRaisesRegex(A.Halt,'EXISTING-ARTIFACT'):D.interrupted_terminal(self.root,143,4.,'TERM')

    def test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE(self):
        self.j.record('reading',{'label':'R'});self.j.record('run',{'status':'R'})
        before={n:(self.root/n).read_bytes() for n in ('reading.json','run.json')}
        self.assertTrue(hasattr(D,'timeout_terminal'),'missing supervisor publication-timeout writer')
        D.timeout_terminal(self.root,137,3.)
        self.assertEqual(json.loads((self.root/'supervisor_timeout.json').read_text())['label'],'INCONCLUSIVE')
        self.assertEqual(json.loads((self.root/'timeout_reading.json').read_text())['label'],'INCONCLUSIVE')
        self.assertEqual(json.loads((self.root/'timeout_run.json').read_text())['status'],'INCONCLUSIVE')
        for name,data in before.items():self.assertEqual((self.root/name).read_bytes(),data)

    def run_shell_stub(self,mode,ignored_signal=None):
        (self.root/'tools').mkdir();(self.root/'code/lab/track_c').mkdir(parents=True);(self.root/'.venv/bin').mkdir(parents=True)
        (self.root/'.venv/bin/python').symlink_to(Path(sys.executable).resolve())
        launcher=(W/'code/lab/runners/run_c10y_precast_diag.sh').read_text().replace('CAP_SECONDS=2820','CAP_SECONDS=6').replace('CLEANUP_RESERVE=10','CLEANUP_RESERVE=4')
        launcher=launcher.replace('TIMER_PID=$!','TIMER_PID=$!\nprintf \'%s\\n\' "$TIMER_PID" > "$CONTROL/timer"\nprintf \'%s\\n\' "$TIMER_PID" > "'+str(self.root/'timer_started')+'"\nexport C10Y_STUB_CONTROL="$CONTROL"')
        if mode=='abnormal':
            anchor='if [[ -e "$OUT/worker_started.json" ]]; then : > "$CONTROL/session"; fi'
            self.assertIn(anchor,launcher)
            launcher=launcher.replace(anchor,anchor+'\nwhile [[ ! -e "$OUT/partial.json" ]]; do sleep 0.01; done\nfalse')
        shell=self.root/'code/lab/runners/run_c10y_precast_diag.sh';shell.write_text(launcher)
        controlled=self.root/'start_shell_fixture.py'
        controlled.write_text('import json,os,signal,sys\nfrom pathlib import Path\n'
            'for name in ("TERM","INT","HUP"):signal.signal(getattr(signal,"SIG"+name),signal.SIG_IGN if name==sys.argv[2] else signal.SIG_DFL)\n'
            'Path('+repr(str(self.root/'inherited_dispositions.json'))+').write_text(json.dumps({name:int(signal.getsignal(getattr(signal,"SIG"+name))) for name in ("TERM","INT","HUP")}))\n'
            'os.execv("/bin/bash",["/bin/bash",sys.argv[1],"--utc","20261009T000000Z"])\n')
        command=[sys.executable,'-B',str(controlled),str(shell),ignored_signal or '-']
        stub=self.root/'code/lab/track_c/c10y_precast_diag.py'
        descendant_code='import signal,time\nfrom pathlib import Path\nsignal.signal(signal.SIGTERM,signal.SIG_IGN)\np=Path('+repr(str(self.root/'heartbeat'))+')\nwhile True:\n with p.open("a") as f:f.write("alive\\n");f.flush()\n time.sleep(.02)\n'
        stub.write_text('import os,sys,signal,time,json,subprocess\nfrom pathlib import Path\nsys.path.insert(0,'+repr(str(W/'code/lab/track_c'))+')\nimport c10y_precast_diag as D\n'
            'root=Path(os.environ["LLMDB_ROOT"]);utc=sys.argv[sys.argv.index("--utc")+1];out=root/"experiments/c10y/runs/c10y_precast_diag"/utc\n'
            'if "--prepare" in sys.argv:\n (root/"driver_prepare_entered").write_text("entered");D.claim_namespace(root,utc,int(os.environ["C10Y_PRECAST_SUPERVISOR"]))\n'
            ' if '+repr(mode)+'=="log_collision":(out/"worker.log").write_bytes(b"preexisting-log")\n'
            ' if '+repr(mode)+'=="prepare_hang":signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(20)\n'
            ' sys.exit(0)\n'
            'if "--timeout-record" in sys.argv:sys.exit(D.timeout_terminal(out,int(sys.argv[sys.argv.index("--returncode")+1]),float(sys.argv[sys.argv.index("--elapsed-s")+1])))\n'
            'if "--interrupted" in sys.argv:\n'
            ' timer=int((Path(os.environ["C10Y_STUB_CONTROL"])/"timer").read_text());os.kill(timer,0);D.Journal(out).record("publication_deadline_armed",{"timer_pid":timer,"armed":True})\n'
            ' if '+repr(mode)+'=="interrupt_publication_hang":signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(20)\n'
            ' sys.exit(D.interrupted_terminal(out,int(sys.argv[sys.argv.index("--returncode")+1]),float(sys.argv[sys.argv.index("--elapsed-s")+1]),sys.argv[sys.argv.index("--reason")+1]))\n'
            'if "--finalize" in sys.argv:\n'
            ' if '+repr(mode)+'=="finalizer_hang":signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(20)\n'
            ' if '+repr(mode)+'=="finalizer_fail":sys.exit(7)\n'
            ' sys.exit(D.finalize(out,int(sys.argv[sys.argv.index("--returncode")+1]),"--timed-out" in sys.argv,float(sys.argv[sys.argv.index("--elapsed-s")+1])))\n'
            'if '+repr(mode)+' in ("early_exit","finalizer_hang","finalizer_fail","log_collision"):sys.exit(7)\n'
            'os.setsid();j=D.Journal(out);j.record("worker_started",{"pid":os.getpid()});j.record("operand",{"value":[7.]})\n'
            'if '+repr(mode)+'=="leader_exit":\n descendant=subprocess.Popen([sys.executable,"-B","-c",'+repr(descendant_code)+']);j.record("owned_descendant",{"pid":descendant.pid});time.sleep(.1);sys.exit(7)\n'
            'with j.phase("native_A7_coined_coined"):\n j.record("partial",{"value":[8.]});signal.signal(signal.SIGTERM,signal.SIG_IGN);signal.signal(signal.SIGINT,signal.SIG_IGN);signal.signal(signal.SIGHUP,signal.SIG_IGN);time.sleep(20)\n')
        out=self.root/'experiments/c10y/runs/c10y_precast_diag/20261009T000000Z'
        if mode=='existing':
            out.mkdir(parents=True);(out/'launch.json').write_bytes(b'{"status":"preexisting"}')
        start=time.monotonic()
        if ignored_signal is not None:
            child=subprocess.run(command,cwd=self.root,capture_output=True,text=True,timeout=9)
            inherited=json.loads((self.root/'inherited_dispositions.json').read_text())
            self.assertEqual(inherited[ignored_signal],int(signal.SIG_IGN))
            print('INHERITED_SIG_IGN '+ignored_signal+' rc='+str(child.returncode)+' namespace='+str(out.exists())+
                  ' timer='+str((self.root/'timer_started').exists())+' prepare='+str((self.root/'driver_prepare_entered').exists()))
            print(child.stderr.strip())
            self.assertEqual(child.returncode,3,(child.stdout,child.stderr))
            self.assertIn('SIGNAL-TRAP-UNAVAILABLE '+ignored_signal,child.stderr)
            self.assertFalse(out.exists());self.assertFalse((self.root/'timer_started').exists());self.assertFalse((self.root/'driver_prepare_entered').exists())
            self.assertLess(time.monotonic()-start,2)
            return
        if mode.startswith('interrupt_') or mode=='abnormal':
            child=subprocess.Popen(command,cwd=self.root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
            worker_pid=None
            try:
                limit=time.monotonic()+2
                while not (out/'partial.json').exists() and time.monotonic()<limit:time.sleep(.01)
                self.assertTrue((out/'partial.json').exists(),'worker did not start')
                worker_pid=json.loads((out/'worker_started.json').read_text())['pid']
                reason='ABNORMAL_EXIT' if mode=='abnormal' else 'TERM' if mode=='interrupt_publication_hang' else mode.split('_',1)[1]
                if mode!='abnormal':child.send_signal(getattr(signal,'SIG'+reason))
                rc=child.wait(timeout=8)
                try:os.kill(worker_pid,0)
                except ProcessLookupError:live=False
                else:live=True
                self.assertFalse(live,'interrupted supervisor abandoned owned worker (exit '+str(rc)+')')
                value=json.loads((out/('supervisor_timeout.json' if mode=='interrupt_publication_hang' else 'supervisor_interruption.json')).read_text())
                self.assertEqual(value['label'],'INCONCLUSIVE')
                if mode!='interrupt_publication_hang':self.assertEqual(value['reason'],reason)
                self.assertTrue(D.load_record(out/'publication_deadline_armed.json')['armed'])
                self.assertEqual(json.loads((out/'partial.json').read_text())['value'],[8.])
                self.assertEqual(json.loads((out/'run.json').read_text())['status'],'INCONCLUSIVE')
                self.assertNotEqual(rc,0);self.assertLess(time.monotonic()-start,8)
            finally:
                if child.poll() is None:child.kill();child.wait(timeout=2)
                if worker_pid is not None:
                    try:os.killpg(worker_pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                child.communicate(timeout=9)
            return
        child=subprocess.run(command,cwd=self.root,capture_output=True,text=True,timeout=9)
        if mode=='existing':
            self.assertEqual(child.returncode,3,(child.stdout,child.stderr))
            self.assertEqual(sorted(p.name for p in out.iterdir()),['launch.json'])
            self.assertEqual((out/'launch.json').read_bytes(),b'{"status":"preexisting"}');return
        self.assertEqual(child.returncode,2,(child.stdout,child.stderr))
        self.assertLess(time.monotonic()-start,8)
        run=json.loads((out/'run.json').read_text());self.assertEqual(run['status'],'INCONCLUSIVE')
        if mode in ('prepare_hang','finalizer_hang'):
            self.assertTrue((out/'supervisor_timeout.json').exists())
            self.assertTrue(all(v['status']=='NOT-RUN' for v in run['phases'].values()))
        elif mode=='hang':
            self.assertTrue((out/'supervisor_timeout.json').exists());self.assertEqual(json.loads((out/'operand.json').read_text())['value'],[7.])
            self.assertEqual(run['phases']['native_A7_coined_coined']['status'],'INCOMPLETE')
            pid=json.loads((out/'worker_started.json').read_text())['pid']
            with self.assertRaises(ProcessLookupError):os.kill(pid,0)
        elif mode=='finalizer_fail':self.assertEqual(D.load_record(out/'supervisor_interruption.json')['reason'],'ABNORMAL_EXIT')
        elif mode=='leader_exit':self.assertTrue((out/'supervisor_halt.json').exists() or (out/'supervisor_timeout.json').exists(),sorted(p.name for p in out.iterdir()))
        else:self.assertTrue((out/'supervisor_halt.json').exists())
        if mode=='leader_exit':
            heartbeat=self.root/'heartbeat';size=heartbeat.stat().st_size;time.sleep(.15)
            self.assertEqual(heartbeat.stat().st_size,size,'descendant still runs after owned leader was reaped')
            pid=D.load_record(out/'owned_descendant.json')['pid']
            limit=time.monotonic()+1
            while time.monotonic()<limit:
                try:os.kill(pid,0)
                except ProcessLookupError:break
                time.sleep(.02)
            else:self.fail('owned descendant survived group cleanup')
        if mode=='log_collision':self.assertEqual((out/'worker.log').read_bytes(),b'preexisting-log')

    def test_fresh_import_is_model_and_torch_free(self):
        stub=self.root/'import_only.py'
        stub.write_text('import sys\nsys.path.insert(0,'+repr(str(W/'code/lab/track_c'))+')\nimport c10y_precast_diag\nassert not set(sys.modules)&{"torch","transformers","datasets","c10e_bandknob"}\nprint("MODEL-FREE IMPORT PASS")\n')
        result=subprocess.run([sys.executable,'-B',str(stub)],cwd=self.root,capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr);self.assertIn('MODEL-FREE IMPORT PASS',result.stdout)

if __name__=='__main__':
    unittest.main(verbosity=2)
