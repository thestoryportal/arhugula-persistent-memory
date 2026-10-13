"""CPU-only, isolated, failing-first tests for the frozen C10Y build."""
import os
import sys
from pathlib import Path

W = Path(__file__).resolve().parents[3]
SCRATCH = Path('/private/tmp/c10y_build').resolve()


def install_guard():
    """Protect the live observation sinks before any production import."""
    import hashlib
    def protected(value):
        if not isinstance(value, (str, bytes, os.PathLike)):
            return False
        p = Path(os.fsdecode(value)).resolve()
        return any(p == W / d or (W / d) in p.parents
                   for d in ('results', 'architecture_profile'))
    def guard(event, args):
        if event == 'open':
            mode, flags = args[1], args[2]
            writing = (isinstance(mode, str) and any(c in mode for c in 'wax+'))
            writing |= bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT |
                                     os.O_TRUNC | os.O_APPEND))
            if writing and protected(args[0]):
                raise PermissionError('C10Y live-tree write refused')
        events = {'os.mkdir', 'os.rename', 'os.remove', 'os.rmdir', 'os.truncate',
                  'os.symlink', 'os.link', 'os.chmod', 'os.utime',
                  'shutil.copyfile', 'shutil.copytree', 'shutil.move', 'shutil.rmtree'}
        if event in events:
            paths = args[:2] if event in {'os.rename', 'os.symlink', 'os.link',
                                         'shutil.copyfile', 'shutil.copytree',
                                         'shutil.move'} else args[:1]
            if any(protected(p) for p in paths):
                raise PermissionError('C10Y live-tree mutation refused')
        if event == 'subprocess.Popen':
            executable, argv, cwd, env = args
            root = Path((env or {}).get('LLMDB_ROOT', '/')).resolve()
            child_cwd = Path(cwd or os.getcwd()).resolve()
            if SCRATCH not in root.parents or SCRATCH not in child_cwd.parents:
                raise PermissionError('C10Y child root/cwd refused')
            scripts = [Path(x).resolve() for x in argv[1:]
                       if isinstance(x, str) and x.endswith('.py')]
            admitted = __import__('json').loads((env or {}).get('C10Y_STUB_WORKERS', '{}'))
            if (Path(executable).resolve() != Path(sys.executable).resolve()
                    or len(scripts) != 1 or str(scripts[0]) not in admitted
                    or SCRATCH not in scripts[0].parents
                    or hashlib.sha256(scripts[0].read_bytes()).hexdigest()
                    != admitted[str(scripts[0])]):
                raise PermissionError('C10Y non-stub subprocess refused')
    sys.addaudithook(guard)
    return guard


AUDIT_GUARD = install_guard()
os.environ['C10Y_SELFTEST'] = '1'
sys.dont_write_bytecode = True

import ast
import contextlib
import copy
import hashlib
import importlib
import inspect
import io
import json
import math
import tempfile
import time
import types
import unittest
from unittest import mock

import torch
torch.set_num_threads(1)

# Standard manual_seed dispatches accelerator APIs even for CPU fixtures.
def _cpu_manual_seed(seed):
    return torch.random.default_generator.manual_seed(int(seed))

torch.manual_seed = torch.random.manual_seed = _cpu_manual_seed

# Missing production imports are deliberately the first recorded RED.
import c10y_directdw_arms as A
import c10y_directdw_read as R
import c10y_directdw_telemetry_check as C

SOURCES = (
    'code/lab/track_c/c10e_bandknob.py',
    'code/lab/track_c/c10z_astra_benchmark.py',
    'code/memit/vendor/memit/compute_z.py',
    'code/memit/vendor/memit/compute_ks.py',
    'code/memit/vendor/memit/memit_main.py',
    'code/memit/vendor/rome/repr_tools.py',
    'code/memit/engine_fingerprint.py', 'experiments/c10y/design/C10Y_DIRECTDW_PREREG.md',
    'code/configs/hparams/qwen25_3b_memit_hparams.json',
)


def fixture_source(path):
    payload=(W/path).read_bytes()
    if path=='experiments/c10y/design/C10Y_DIRECTDW_PREREG.md' and hashlib.sha256(payload).hexdigest()!=A.PREREG_SHA:
        # Exact legacy-contract bytes in scratch only; no production repinning.
        payload=payload.partition(b'\n\n## 12. Amendment ZERO-STEP-DISPOSITION')[0]
        if hashlib.sha256(payload).hexdigest()!=A.PREREG_SHA or A.PREREG_SHA!=R.PREREG_SHA:
            raise AssertionError('Legacy fixture prereg identity mismatch')
    return payload


class IsolatedCase(unittest.TestCase):
    def setUp(self):
        (SCRATCH / 'roots').mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(dir=SCRATCH / 'roots')).resolve()
        self.env = dict(os.environ)
        self.old_roots = [getattr(m, 'ROOT', None) for m in (A, R, C)]
        for m in (A, R, C):
            m.ROOT = self.root
        os.environ['LLMDB_ROOT'] = str(self.root)
        os.environ['C10Y_SELFTEST'] = '1'
        for k in ('C10Y_TELEMETRY', 'C10Y_TELEMETRY_INERTNESS'):
            os.environ.pop(k, None)
        for f in SOURCES:
            p = self.root / f
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(fixture_source(f))
        for f in ('c10y_directdw_arms.py', 'c10y_directdw_read.py',
                  'c10y_directdw_telemetry_check.py'):
            (self.root / 'code/lab/track_c' / f).write_bytes((W / 'code/lab/track_c' / f).read_bytes())
        (self.root / 'results').mkdir()
        (self.root / 'architecture_profile').mkdir()
        self.out = self.root / 'results/c10y_directdw'
        self.diagnostic = self.root / 'architecture_profile/c10y_halt_diagnostic_test.json'

    def tearDown(self):
        for m, old in zip((A, R, C), self.old_roots):
            m.ROOT = old
        os.environ.clear()
        os.environ.update(self.env)
        self.assertTrue(all(n not in sys.modules for n in
                            ('c10e_bandknob', 'transformers', 'datasets')))


class Batch(dict):
    def to(self, device):
        return Batch({k: v.to(device) for k, v in self.items()})


class TinyTokenizer:
    padding_side = 'right'
    pad_token_id = 0
    eos_token_id = 0
    def __init__(self):
        self.vocab = {'Echo': 9, 'Second': 9}
        self.inverse = {9: 'Echo'}
    def encode(self, text):
        result = []
        for word in text.split():
            if word not in self.vocab:
                value = len(self.vocab) + 10
                self.vocab[word] = value
                self.inverse[value] = word
            result.append(self.vocab[word])
        return result or [1]
    def __call__(self, text, return_tensors=None, padding=False, add_special_tokens=True):
        single = isinstance(text, str)
        rows = [self.encode(t) for t in ([text] if single else text)]
        if return_tensors is None:
            return {'input_ids': rows[0] if single else rows}
        width = max(map(len, rows))
        return Batch(input_ids=torch.tensor([r + [0] * (width-len(r)) for r in rows]),
                     attention_mask=torch.tensor([[1]*len(r)+[0]*(width-len(r)) for r in rows]))
    def decode(self, ids):
        return ' ' + ' '.join(self.inverse.get(int(i), 'wrong') for i in ids)


class TinyBlock(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.mlp = torch.nn.Module()
        self.mlp.down_proj = torch.nn.Linear(4, 4, bias=False)
        with torch.no_grad():
            self.mlp.down_proj.weight.copy_(torch.eye(4) * 0.03)
    def forward(self, x):
        # Causal cross-position path makes the routing test substantive.
        x = x + 0.05 * x.cumsum(1)
        return (x + self.mlp.down_proj(x),)


class TinyBackbone(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.embed_tokens = torch.nn.Embedding(256, 4)
        self.layers = torch.nn.ModuleList(TinyBlock() for _ in range(10))
        self.norm = torch.nn.Identity()
        with torch.no_grad():
            self.embed_tokens.weight.fill_(0.2)
    def forward(self, input_ids, attention_mask=None, use_cache=False,
                output_hidden_states=False, **kwargs):
        x = self.embed_tokens(input_ids)
        states = []
        for layer in self.layers:
            if output_hidden_states:
                states.append(x)
            x = layer(x)[0]
        x = self.norm(x)
        if output_hidden_states:
            states.append(x)
        return types.SimpleNamespace(last_hidden_state=x, hidden_states=tuple(states))


class TinyModel(torch.nn.Module):
    def __init__(self, lens_sensitive=False, drifting=False):
        super().__init__()
        self.model = TinyBackbone()
        self.lm_head = torch.nn.Linear(4, 256, bias=False)
        self.config = types.SimpleNamespace(num_hidden_layers=10, vocab_size=256,
                                            hidden_size=4, _name_or_path='tiny')
        self.lens_sensitive, self.drifting = lens_sensitive, drifting
        self.counter = 0
        self.forward_inputs = []
        self.lens_counter = 0
        with torch.no_grad():
            self.lm_head.weight.zero_()
            self.lm_head.weight[9].fill_(2.5)
        self.eval()
    def forward(self, input_ids, attention_mask=None, use_cache=False,
                output_hidden_states=False, **kwargs):
        self.forward_inputs.append(input_ids.detach().clone())
        out = self.model(input_ids, attention_mask=attention_mask,
                         output_hidden_states=output_hidden_states, use_cache=False)
        logits = self.lm_head(out.last_hidden_state)
        if output_hidden_states:
            self.lens_counter += 1
        if self.drifting:
            self.counter += 1
            logits = logits + self.counter * 1e-3
        elif self.lens_sensitive and not output_hidden_states:
            logits = logits + self.lens_counter * 1e-3
            self.lens_counter = 0
        return types.SimpleNamespace(logits=logits, hidden_states=out.hidden_states)


def make_h(lens_sensitive=False, drifting=False):
    tok = TinyTokenizer()
    model = TinyModel(lens_sensitive, drifting).half()
    H = types.SimpleNamespace(torch=torch, tok=tok, model=model, DEV='cpu',
        CANON='The capital of {} is the city of',
        PTEST=["{}'s capital city is called", 'If you visit {}, its capital city is',
               'The main city and seat of government of {} is'],
        FICTION=[f'Subject{i}' for i in range(24)], L2=1.0,
        _LAW5_DEFAULT_CTX=False, Z_OVERRIDE=None, Z_OVERRIDE_HITS=0,
        ARM_HOOKS=[], _ARM_STATE=None)
    H.ARMS = {name: {s: 'Echo' if name == 'A1_single' else 'Second Echo' if name == 'A2_coherent2' else 'Echo Echo' for s in H.FICTION}
              for name in ('A1_single', 'A2_coherent2', 'A7_coined_coined')}
    H.hp = types.SimpleNamespace(layers=[4,5,6,7,8],
        rewrite_module_tmp='model.layers.{}.mlp.down_proj', layer_module_tmp='model.layers.{}',
        fact_token='subject_last', v_loss_layer=9, kl_factor=0.0625)
    H.HP_BASE = str(Path(os.environ['LLMDB_ROOT']) / 'code/configs/hparams/qwen25_3b_memit_hparams.json')
    H.get_context_templates = lambda model, tok: [['{}'], [f'Frame{i}. {{}}' for i in range(5)]]
    H.req = lambda prompt, subj, targ: {'prompt':prompt,'subject':subj,'target_new':{'str':' '+targ}}
    H.tgt_ids = lambda value: tok(' '+value, add_special_tokens=False)['input_ids']
    H.weight_name = lambda hp, layer: hp.rewrite_module_tmp.format(layer)+'.weight'
    H.snap_layers = lambda hp: {l: dict(model.named_parameters())[H.weight_name(hp,l)].detach().clone() for l in hp.layers}
    def restore(hp, snap):
        with torch.no_grad():
            for l in hp.layers:
                dict(model.named_parameters())[H.weight_name(hp,l)].copy_(snap[l])
    H.restore_layers = restore
    H.upd_matrix_match_shape = lambda matrix, shape: matrix if matrix.shape == shape else matrix.T
    H.compute_P = lambda hp: [torch.eye(4) for _ in hp.layers]
    def lookup(prompt, subject, tok, fact_token, verbose=False):
        return len(tok.encode(prompt.split('{}')[0] + subject))-1
    H.find_fact_lookup_idx = lookup
    def reps(model, tok, layer, context_templates, words, module_template, fact_token_strategy):
        batch = tok([t.format(s) for t,s in zip(context_templates, words)], padding=True, return_tensors='pt')
        module = dict(model.named_modules())[module_template.format(layer)]
        box = {}
        def capture(m, inputs, output):
            box['input'] = inputs[0].detach()
            box['output'] = (output[0] if isinstance(output,tuple) else output).detach()
        handle = module.register_forward_hook(capture)
        try:
            with torch.no_grad(): model(**batch)
        finally: handle.remove()
        ids = [lookup(t,s,tok,'subject_last') for t,s in zip(context_templates,words)]
        rows = torch.arange(len(ids))
        return box['input'][rows,ids],box['output'][rows,ids]
    H.get_module_input_output_at_words = reps
    def keys(model,tok,requests,hp,layer,contexts):
        templates=[c.format(r['prompt']) for r in requests for group in contexts for c in group]
        words=[r['subject'] for r in requests for group in contexts for c in group]
        values=reps(model,tok,layer,templates,words,hp.rewrite_module_tmp,hp.fact_token)[0]
        J=sum(map(len,contexts))
        return torch.stack([torch.stack([v.mean(0) for v in values[i:i+J].split([len(g) for g in contexts])]).mean(0)
                            for i in range(0,len(values),J)])
    H.compute_ks=keys
    H.compute_z=lambda model,tok,r,hp,layer,contexts: reps(model,tok,layer,[r['prompt']],[r['subject']],hp.layer_module_tmp,hp.fact_token)[1][0] + 0.05
    # Reference scorer source is read as text, never imported.
    source=ast.parse((W/'code/lab/track_c/c10e_bandknob.py').read_text())
    scorer=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='full_seq_match')
    scope={'torch':torch,'tok':tok,'model':model,'DEV':'cpu'}
    exec(compile(ast.Module(body=[scorer],type_ignores=[]),'<source-only scorer>','exec'),scope)
    H.full_seq_match=scope['full_seq_match']
    def original(hp,requests,P,cache):
        ctx=H.get_context_templates(model,tok)
        ks=[(r['subject'],r['target_new']['str']) for r in requests]
        if H.Z_OVERRIDE is not None and not H._LAW5_DEFAULT_CTX and all(k in H.Z_OVERRIDE for k in ks):
            H.Z_OVERRIDE_HITS += 1
            zs=torch.stack([H.Z_OVERRIDE[k] for k in ks],1)
        else: zs=torch.stack([H.compute_z(model,tok,r,hp,hp.layers[-1],ctx) for r in requests],1)
        weights=dict(model.named_parameters())
        norms={}
        for i,l in enumerate(hp.layers):
            K=keys(model,tok,requests,hp,l,ctx).T
            cur=reps(model,tok,hp.layers[-1],[r['prompt'] for r in requests],[r['subject'] for r in requests],hp.layer_module_tmp,hp.fact_token)[1].T
            residual=(zs-cur).repeat_interleave(K.shape[1]//zs.shape[1],1)/(len(hp.layers)-i)
            M=P[i]@(K.float().cpu()@K.float().cpu().T+cache[i])+torch.eye(K.shape[0])
            update=torch.linalg.solve(M,P[i]@K.float().cpu()@residual.float().cpu().T).T
            with torch.no_grad(): weights[H.weight_name(hp,l)].add_(update.to(weights[H.weight_name(hp,l)]))
            norms[str(l)]={'delta_norm':float(update.norm())}
        for i,l in enumerate(hp.layers):
            K=keys(model,tok,requests,hp,l,ctx).T.float().cpu()
            cache[i] += K@K.T
        return norms
    H.my_edit=original
    return H


class IsolationTests(IsolatedCase):
    def test_seed_uses_only_cpu_generator(self):
        with contextlib.ExitStack() as stack:
            spies = []
            for accelerator, name in ((torch.cuda, 'manual_seed_all'),
                                      (torch.mps, 'manual_seed'),
                                      (torch.xpu, 'manual_seed_all')):
                stack.enter_context(mock.patch.object(accelerator, '_is_in_bad_fork', return_value=False))
                spies.append(stack.enter_context(mock.patch.object(accelerator, name)))
            for seed in (torch.manual_seed, torch.random.manual_seed):
                generator = seed(19)
                self.assertIs(generator, torch.random.default_generator)
            for spy in spies:
                spy.assert_not_called()
    def test_live_write_positive_control(self):
        self.assertTrue(callable(AUDIT_GUARD),'audit hook must be installed before imports')
        path=W/'results/__c10y_isolation_probe__'
        self.assertFalse(path.exists())
        with self.assertRaises(PermissionError): os.mkdir(path)
        self.assertFalse(path.exists())
    def test_relative_and_symlink_guard(self):
        alias=self.root/'live'
        with self.assertRaises(PermissionError): alias.symlink_to(W/'results',target_is_directory=True)
        with self.assertRaises(PermissionError): AUDIT_GUARD('open',(str(W/'results/../results/c10y_probe.json'),'w',os.O_WRONLY))
        with self.assertRaises(PermissionError): os.chmod(W/'results',0o700)
    def test_all_cases_use_base(self):
        classes=[v for v in globals().values() if isinstance(v,type) and issubclass(v,unittest.TestCase)]
        self.assertTrue(all(issubclass(v,IsolatedCase) for v in classes))
    def test_real_dispatch_denied_with_temp_environment(self):
        self.assertTrue(callable(AUDIT_GUARD),'audit hook missing')
        env=dict(os.environ,LLMDB_ROOT=str(self.root))
        with self.assertRaises(PermissionError):
            AUDIT_GUARD('subprocess.Popen',(sys.executable,[sys.executable,'-B',str(W/'code/lab/track_c/c10y_directdw_arms.py')],str(self.root),env))
    def test_selftest_root_refusal(self):
        with self.assertRaises(A.Halt): A.selftest_root(W)


class NumericTests(IsolatedCase):
    def test_full_size_float64_reductions(self):
        torch.manual_seed(19)
        x=torch.randn(2048,11008)
        y=x.clone();y.flatten()[::101] += 0.03125
        xd,yd=x.double(),y.double()
        self.assertEqual(A.cosine(x,x),1.0)
        self.assertEqual(A.relative_distance(x,x),0.0)
        self.assertEqual(A.norm_ratio(x,x),1.0)
        reference=float((xd.flatten()@yd.flatten())/(xd.norm()*yd.norm()))
        self.assertAlmostEqual(A.cosine(x,y),reference,delta=abs(reference)*1e-12)
        distance=float((xd-yd).norm()/max(xd.norm(),yd.norm()))
        self.assertAlmostEqual(A.relative_distance(x,y),distance,delta=distance*1e-12)
        self.assertAlmostEqual(A.norm_ratio(x,y),float(xd.norm()/yd.norm()),delta=1e-12)
    def test_gram_norm_dense_reference(self):
        torch.manual_seed(4)
        a=torch.randn(2048,3);b=torch.randn(3,11008)
        reference=float((a.double()@b.double()).norm())
        self.assertAlmostEqual(A.gram_norm(a,b),reference,delta=reference*1e-12)
    def test_mps_double_refused(self):
        tensor=types.SimpleNamespace(device=types.SimpleNamespace(type='mps'),dtype=torch.float64)
        with self.assertRaises(A.Halt): A.assert_no_mps_double(tensor)
    def test_capture_factorization(self):
        K=torch.tensor([[1.,2.],[3.,4.],[0.,0.]])
        P=torch.diag(torch.tensor([1.,1.,0.]));cache=torch.zeros(3,3)
        residual=torch.tensor([[0.2,0.4],[-0.1,0.5]])
        got=A.factor_solve(K,residual,P,cache,1.0)
        reference=torch.linalg.solve(P@(K@K.T+cache)+torch.eye(3),P@K@residual.T).T
        self.assertLess(A.relative_distance(got['R']@got['B'],reference),1e-6)
        self.assertEqual(float((got['B']@torch.tensor([0.,0.,1.])).double().norm()),0.)
    def test_anchor_zero_denominator(self):
        zeros=torch.zeros(2,3,4)
        self.assertEqual(float(A.anchor_loss(zeros,zeros,torch.zeros(2,4))),0.)
        with self.assertRaises(A.Halt): A.anchor_loss(zeros+1,zeros,torch.zeros(2,4))
    def test_size_scales_and_stored_arithmetic(self):
        a={4:torch.tensor([[1.,0.]])};b={4:torch.tensor([[2.,0.]])}
        self.assertEqual(A.size_scales(a,b),{'NM':0.5,'ENV':0.5})
        self.assertEqual(A.size_scales(b,a),{'NM':None,'ENV':None})
        self.assertEqual(A.size_scales({4:torch.zeros(1,2)},b)['ENV'],0.)
        W0=torch.tensor([[0.3333,0.6666]],dtype=torch.float16)
        expected=(W0+(b[4]*0.5).half()).half()
        self.assertTrue(torch.equal(A.stored_weight(W0,b[4],0.5),expected))
    def test_control_boundaries(self):
        for error,expected in ((0.01,True),(0.010001,False)):
            with self.subTest(error=error): self.assertEqual(A.control_match('NM',1+error,1,{4:1.0},{4:1.0},{4:0.999}),expected)
        for candidate,expected in ((1.01,True),(1.010001,False)):
            with self.subTest(candidate=candidate): self.assertEqual(A.control_match('ENV',candidate,1,{4:candidate},{4:1.0},{4:0.999}),expected)
        self.assertFalse(A.control_match('NM',1,1,{4:1.},{4:1.},{4:0.9989999}))
    def test_null_share_boundaries(self):
        P=torch.diag(torch.tensor([1.,0.]))
        for share in (0.999,0.9989999):
            x=torch.tensor([[math.sqrt(share),math.sqrt(1-share)]],dtype=torch.float64)
            self.assertAlmostEqual(A.null_share(x,P),share,delta=1e-14)
            self.assertEqual(A.projector_gate({4:x},{4:x},[P]),share>=0.999)


class OptimizerTests(IsolatedCase):
    def test_effective_weight_and_routing_gradient(self):
        W0=torch.tensor([[0.3333,-0.1],[0.2,0.5]],dtype=torch.float16)
        a=torch.tensor([[0.03],[0.04]],requires_grad=True)
        b=torch.tensor([[0.3,-0.5]])
        x=torch.tensor([[[0.1,0.2],[0.3,0.4],[0.5,0.6]]],dtype=torch.float16,requires_grad=True)
        expected=torch.nn.functional.linear(x,(W0+(a@b).half()).half())
        hook=A.deployed_hook(W0,a,b,torch.tensor([[False,True,True]]))
        actual=hook(None,(x,),None)
        self.assertTrue(torch.equal(actual,expected))
        grad=torch.autograd.grad(actual[0,0].sum(),a,retain_graph=True,allow_unused=True)[0]
        self.assertTrue(grad is None or torch.equal(grad,torch.zeros_like(a)))
        self.assertGreater(float(torch.autograd.grad(actual[0,1:].sum(),a)[0].double().norm()),0.)
    def test_kl_coefficient_once(self):
        self.assertEqual(float(A.total_loss(torch.tensor(2.),torch.tensor(8.))),2.5)
    def test_request_batch_and_target_only_objective(self):
        H=make_h();r=H.req(H.CANON,H.FICTION[0],'Echo Echo')
        batch=A.request_batch(H,r,H.get_context_templates(H.model,H.tok))
        self.assertEqual(batch['rewriting_targets'].shape[0],6)
        self.assertEqual(len(batch['lookup_idxs']),7)
        for row in batch['rewriting_targets']:
            self.assertEqual(row[row!=-100].tolist(),[9,9])
        result=A.edit_components(H,[batch],None)
        self.assertAlmostEqual(float(result['KL_raw']),0.,delta=1e-6)
        self.assertEqual(len(result['target_log_probs']),12)
        self.assertTrue(all(p.grad is None for p in H.model.parameters()))
    def test_microbatch_request_weighting(self):
        groups=A.microbatch_indices(24,6)
        self.assertEqual(groups,[list(range(i,i+6)) for i in range(0,24,6)])
        self.assertEqual(A.request_weights([6,6]),[0.5,0.5])
        self.assertEqual(A.request_weights([5,7]),[5/12,7/12])
        self.assertEqual(A.request_weights([6,6,6,6]),[0.25]*4)
    def test_stopping_boundaries(self):
        self.assertTrue(A.threshold_stop('e2e',0.049999))
        self.assertFalse(A.threshold_stop('e2e',0.05))
        self.assertTrue(A.threshold_stop('anchor',1e-4))
        self.assertFalse(A.threshold_stop('anchor',1.000001e-4))
    def test_loss_scale_transaction(self):
        a=torch.nn.Parameter(torch.tensor([1.]))
        opt=torch.optim.Adam([a],lr=0.1)
        calls=[]
        def objective(indices):
            calls.append(a.detach().clone())
            return (a.square().sum(),{'L':1.0})
        before=copy.deepcopy(opt.state_dict());snap=a.detach().clone()
        result=A.accepted_step([a],opt,objective,[[0],[1]],1024.,0,overflow=lambda attempt:attempt==0)
        self.assertEqual(result['retries'],1)
        self.assertEqual(result['loss_scale'],512.)
        self.assertTrue(all(torch.equal(x,snap) for x in calls))
        self.assertEqual(int(opt.state[a]['step']),1)
        self.assertEqual(before['state'],{})
    def test_sixth_overflow_halts_without_mutation(self):
        a=torch.nn.Parameter(torch.tensor([1.]));opt=torch.optim.Adam([a],lr=0.1)
        snap=a.detach().clone()
        with self.assertRaises(A.Halt):
            A.accepted_step([a],opt,lambda indices:(a.square().sum(),{}),[[0]],1024.,0,overflow=lambda attempt:True)
        self.assertTrue(torch.equal(a,snap));self.assertEqual(opt.state_dict()['state'],{})
    def test_unknown_hooks_preserved(self):
        H=make_h();module=H.model.model.layers[4].mlp.down_proj
        handle=module.register_forward_hook(lambda m,args,out:out)
        before=A.hook_snapshot(H.model)
        a=torch.nn.Parameter(torch.ones(4,1)*0.01);b=torch.ones(1,4)*0.02
        with A.weight_hooks(H,H.hp,{4:a},{4:b},H.snap_layers(H.hp),None):
            self.assertNotEqual(A.hook_snapshot(H.model),before)
            H.model(torch.tensor([[1,2,3]]))
        self.assertEqual(A.hook_snapshot(H.model),before)
        handle.remove()


class LaunchTests(IsolatedCase):
    def test_direct_launch_shell_dependencies_are_executable_and_git_100755(self):
        # The git index snapshot is collected by a read-only shell command;
        # test subprocesses remain restricted to audited Python stub workers.
        modes = {line.split('\t', 1)[1]: line.split()[0]
                 for line in (SCRATCH / 'launch_git_modes.txt').read_text().splitlines()}
        graph = (A.__file__, C.__file__, str(W / 'code/memit/engine_fingerprint.py'))
        dependencies = set()
        for path in graph:
            tree = ast.parse(Path(path).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.endswith('.sh'):
                    dependencies.add(node.value)
        for relative in dependencies:
            script = Path(relative) if Path(relative).is_absolute() else W / relative
            self.assertTrue(os.access(script, os.X_OK), str(script))
            self.assertEqual(modes.get(str(script.relative_to(W))), '100755', str(script))
        main_tree = ast.parse(inspect.getsource(A.main))
        command = next(node.value for node in ast.walk(main_tree)
                       if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'command' for t in node.targets))
        self.assertIsInstance(command, ast.List)
        self.assertEqual(ast.unparse(command.elts[0]), 'sys.executable')
        self.assertEqual(command.elts[1].value, '-B')
        self.assertEqual(dependencies, set(), 'new shell dependency requires direct-launch review')
    def test_every_inherited_preflight_knob_refused(self):
        knobs=('C10_PROJECTOR','N_EDIT','C10_SUBJECT_OFFSET','C10_CTX_TEMPLATES','C10_ARMS','C10_KEY_LOCUS',
               'HP_CANDIDATE','C10_RECIPES','CANDIDATE_NAME','OUT','DECISION_ID','PREREG','RUN_LABEL',
               'LLMDB_DEVICE')
        for knob in knobs:
            with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
        for name in ('MODEL_ID','MODEL_REV'):
            with self.subTest(name=name),self.assertRaises(A.Halt): A.preflight({name:'mismatch'})
    def test_go_spend_and_stage_eligibility(self):
        go={'decision_id':'D-test','experiment':'C10Y','stage':2,'recorded_in':'program/runbook/:5','at':'2026-10-08T00:00:00Z'}
        spend={'decision_id':'D-spend','stage':2,'cap_s':7200.}
        with self.assertRaises(A.Halt): A.launch_documents(2,go,None,None)
        for cap in (None,0,-1,float('nan'),float('inf'),True):
            with self.subTest(cap=cap),self.assertRaises(A.Halt): A.launch_documents(2,go,dict(spend,cap_s=cap),{'label':'SCREEN-PASS'})
        with self.assertRaises(A.Halt): A.launch_documents(2,go,spend,{'label':'SCREEN-NULL'})
        self.assertEqual(A.launch_documents(2,go,spend,{'label':'SCREEN-PASS'}),7200.)
    def test_forecast_unverified_and_cap(self):
        artifact=self.root/'timing.json';artifact.write_text('{}')
        def forecast(total):
            return {'stage':1,'phases':[{'name':name,'artifact':str(artifact),'sha256':hashlib.sha256(b'{}').hexdigest(),
                'workload':'tiny CPU proof','repetitions':1,'scaling_assumption':'identity bound','upper_s':1380. if name=='readout' else (total-1380.)/(len(A.FORECAST_PHASES)-1),
                'measured':False,'justification':'isolated fixture tests gate arithmetic; no runtime timing claim'} for name in A.FORECAST_PHASES]}
        self.assertEqual(A.budget_gate(forecast(7200.),7200.)['status'],'READY')
        high=A.budget_gate(forecast(7200.001),7200.)
        self.assertEqual(high['status'],'HALTED-BUDGET');self.assertIs(high['launched'],False)
        unknown=forecast(5000.);unknown['phases'][0].pop('artifact')
        self.assertEqual(A.budget_gate(unknown,7200.)['status'],'UNVERIFIED')
    def test_memory_boundaries(self):
        G=2**30
        valid={'current_bytes':0,'driver_bytes':32*G,'rss_bytes':8*G,'available_bytes':8*G}
        self.assertEqual(A.memory_gate(valid),valid)
        variants=[dict(valid,driver_bytes=32*G+1),dict(valid,driver_bytes=0,rss_bytes=40*G+1),
                  dict(valid,available_bytes=8*G-1),dict(valid,rss_bytes=8*G+1),{}]
        for metrics in variants:
            with self.subTest(metrics=metrics),self.assertRaises(A.Halt): A.memory_gate(metrics)
    def test_context_freeze_and_leakage(self):
        H=make_h();path=self.root/'context_templates.json'
        first=A.freeze_contexts(H,path)
        self.assertEqual(first['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
        H.get_context_templates=lambda model,tok:(_ for _ in ()).throw(AssertionError('redraw'))
        second=A.freeze_contexts(H,path,expected=first['sha256'])
        self.assertEqual(second,first)
        audit=A.overlap_audit([['{}'],["If you visit {}, its capital city is. {}"]],H)
        self.assertIs(audit['clean'],False)
    def test_wrapper_delegate_dynamic_and_arm_restore(self):
        H=make_h();calls=[]
        H.my_edit=lambda *args:calls.append(args) or {'original':True}
        wrapper=A.Writer(H,H.hp)
        H._LAW5_DEFAULT_CTX=True;wrapper.mode='e2e'
        self.assertEqual(wrapper(H.hp,[],[],[]),{'original':True})
        H._LAW5_DEFAULT_CTX=False;wrapper.mode=None
        self.assertEqual(wrapper(H.hp,[],[],[]),{'original':True})
        arms=H.ARMS
        H.run_recipe=lambda name,path:(_ for _ in ()).throw(RuntimeError('intentional'))
        with self.assertRaises(RuntimeError): A.scored_recipe(H,'B-e2e',H.HP_BASE,1,None)
        self.assertIs(H.ARMS,arms)
    def test_schedule_halt_survives_new_directory(self):
        A.schedule_halt(self.root,'LAW#3',{'observed':19})
        with self.assertRaises(A.Halt): A.refuse_schedule_halt(self.root)
        self.assertTrue((self.root/'results/c10y_directdw_schedule_halt.json').is_file())
    def test_step_projection_reserves_readout(self):
        budget=A.Budget(0.,7200.,1,clock=lambda:5800.)
        with self.assertRaises(A.Halt): budget.project(30.,write_complete=False)
        with self.assertRaises(A.Halt) as cm: budget.project(30.,write_complete=True)
        self.assertEqual(cm.exception.code,'INCOMPLETE-BUDGET')


class TelemetryTests(IsolatedCase):
    def test_frozen_hparams_lens_uses_actual_linear_head(self):
        H=make_h();H.hp.lm_head_module='model.embed_tokens';H.hp.ln_f_module='model.norm'
        writer=A.Telemetry(self.out,'s1','fixed');writer.logit_lens(H,H.hp,'pristine')
        self.assertTrue(writer.enabled);writer.close()
        rows=[json.loads(x) for x in (self.out/'telemetry/telemetry_s1.jsonl').read_text().splitlines()]
        self.assertEqual(rows[-1]['kind'],'logit_lens');self.assertEqual(len(rows[-1]['items']),24)
    def test_telemetry_never_calls_operational_clock_or_writes_input_record(self):
        record={'L_edit':1.,'KL_raw':0.,'KL_weighted':0.,'L':1.};before=copy.deepcopy(record)
        writer=A.Telemetry(self.out,'s1','fixed')
        with mock.patch.object(A,'STAGE_CLOCK',side_effect=AssertionError('stage clock called')), \
             mock.patch.object(A,'supervise',side_effect=AssertionError('supervisor called')), \
             mock.patch.object(A,'sample_memory',side_effect=AssertionError('sampler called')), \
             mock.patch.object(A,'sync',side_effect=AssertionError('sync called')), \
             mock.patch.object(A,'write_json',side_effect=AssertionError('record writer called')), \
             mock.patch.object(A.Budget,'project',side_effect=AssertionError('projection called')):
            writer.opt_step(1,record,1024.,0,{'4':1.});writer.phase('test')
            self.assertTrue(writer.enabled)
        self.assertEqual(record,before);writer.close()
    def test_t8_serialized_wrong_answer_is_not_inert(self):
        emit=A.Telemetry.emit
        def corrupt(writer,kind,**payload):
            if kind=='answer': payload['full']=not payload['full']
            return emit(writer,kind,**payload)
        with mock.patch.object(A.Telemetry,'emit',corrupt):
            record=A.telemetry_mps_inertness_check(self.out,make_h())
        self.assertNotEqual(record['verdict'],'INERT')
    def test_off_has_no_object_or_directory(self):
        self.assertEqual(A.telemetry_admission({},1,self.out),{'telemetry':False,'telemetry_inertness':None})
        H=make_h();original=H.full_seq_match
        self.assertIs(A.telemetry_factory(self.out,'s1','fixed',False),None)
        self.assertFalse((self.out/'telemetry').exists());self.assertIs(H.full_seq_match,original)
    def test_invalid_switches_refused_before_write(self):
        for value in ('0','true','',' 1','1'):
            with self.subTest(value=value),self.assertRaises(A.Halt): A.telemetry_admission({'C10Y_TELEMETRY':value},1,self.out)
        self.assertFalse(self.out.exists())
    def test_scorer_ast_and_exact_inputs(self):
        H=make_h();capture=[]
        scorer=A.make_scorer(H,lambda p,t,g:capture.append((p,list(t),list(g))))
        target=H.tgt_ids('Echo Echo');prompt=H.CANON.format(H.FICTION[0])
        original=H.full_seq_match(prompt,target)
        before=[x.clone() for x in H.model.forward_inputs];H.model.forward_inputs.clear()
        observed=scorer(prompt,target)
        self.assertEqual(observed,original);self.assertEqual(capture[0][2],[9,9])
        self.assertTrue(all(torch.equal(x,y) for x,y in zip(before,H.model.forward_inputs)))
        self.assertTrue(A.scorer_ast_check(W/'code/lab/track_c/c10e_bandknob.py'))
    def test_every_kind_state_preservation_and_volume(self):
        H=make_h();H._ARM_STATE={'requests':[H.req(H.CANON,s,H.ARMS['A7_coined_coined'][s]) for s in H.FICTION]}
        writer=A.Telemetry(self.out,'s1','fixed')
        state={n:(p.detach().clone(),p.data_ptr()) for n,p in H.model.named_parameters()}
        rng=torch.random.get_rng_state().clone();hooks=A.hook_snapshot(H.model)
        writer.phase('write_start',recipe='B-e2e',arm='A7_coined_coined',mode='e2e')
        writer.opt_step(1,{'L_edit':1.,'KL_raw':2.,'KL_weighted':0.125,'L':1.125},1024.,0,{'4':1.})
        writer.target_probs(probabilities=[{'request':0,'frame':0,'position':0,'p':0.9}])
        writer.target_probs(f_ij=[[0.9]*6 for _ in range(24)])
        writer.write_norms({'4':{'actual':1.,'planned':1.,'ratio_to_A':1.}},'B-e2e','A7_coined_coined')
        writer.logit_lens(H,H.hp,'merged','B-e2e')
        scorer=A.make_scorer(H,lambda p,t,g:writer.sink(H,'B-e2e','readout',p,t,g))
        for subj in H.FICTION:
            for template in [H.CANON]+H.PTEST: scorer(template.format(subj),H.tgt_ids('Echo Echo'))
        writer.phase('write_end',recipe='B-e2e',arm='A7_coined_coined',mode='e2e')
        writer.close()
        lines=[json.loads(x) for x in (self.out/'telemetry/telemetry_s1.jsonl').read_text().splitlines()]
        self.assertGreater(len(lines),0)
        self.assertEqual(lines[0]['kind'],'header')
        self.assertEqual(sum(x['kind']=='answer' for x in lines),96)
        self.assertEqual(set(x['kind'] for x in lines),{'header','phase','opt_step','target_probs','write_norms','logit_lens','answer'})
        self.assertTrue(all(x['subj'] is not None and x['template'] is not None for x in lines if x['kind']=='answer'))
        for n,p in H.model.named_parameters():
            self.assertTrue(torch.equal(p,state[n][0]));self.assertEqual(p.data_ptr(),state[n][1]);self.assertIsNone(p.grad)
        self.assertTrue(torch.equal(rng,torch.random.get_rng_state()));self.assertEqual(hooks,A.hook_snapshot(H.model));self.assertFalse(H.model.training)
    def test_io_failures_disable_once_and_baseexception_propagates(self):
        stream=io.StringIO()
        with mock.patch.object(sys,'__stderr__',stream),mock.patch.object(Path,'mkdir',side_effect=OSError('init')):
            writer=A.Telemetry(self.out,'s1','fixed');writer.phase('later')
        self.assertEqual(stream.getvalue().count('C10Y_TELEMETRY_DISABLED OSError: init'),1)
        for operation in ('write','flush','fsync'):
            writer=A.Telemetry(self.out/operation,'s1','fixed');stream=io.StringIO()
            patch=mock.patch.object(os,'fsync',side_effect=OSError(operation)) if operation=='fsync' else mock.patch.object(writer.file,operation,side_effect=OSError(operation))
            with mock.patch.object(sys,'__stderr__',stream),patch:
                writer.phase('test');writer.phase('later')
            self.assertEqual(stream.getvalue().count('C10Y_TELEMETRY_DISABLED'),1)
        writer=A.Telemetry(self.out/'interrupt','s1','fixed')
        with mock.patch.object(A,'TELEMETRY_CLOCK',side_effect=KeyboardInterrupt),self.assertRaises(KeyboardInterrupt): writer.phase('test')
    def test_inertness_and_drifting_baseline(self):
        H=make_h();result=A.telemetry_mps_inertness_check(self.out,H)
        self.assertEqual(result['verdict'],'INERT');self.assertEqual(result['answer_calls'],96);self.assertEqual(result['lens_forwards'],48)
        other=A.telemetry_mps_inertness_check(self.out/'drifting',make_h(drifting=True))
        self.assertEqual(other['verdict'],'NONDETERMINISTIC-BASELINE')
        sensitive=A.telemetry_mps_inertness_check(self.out/'lens_sensitive',make_h(lens_sensitive=True))
        self.assertEqual(sensitive['verdict'],'NOT-INERT')


class IntegrationTests(IsolatedCase):
    def test_sequential_capture_matches_original(self):
        H=make_h();hp=H.hp;snap=H.snap_layers(hp)
        requests=[H.req(H.CANON,s,'Echo Echo') for s in H.FICTION]
        H.Z_OVERRIDE={(r['subject'],r['target_new']['str']):H.compute_z(H.model,H.tok,r,hp,8,H.get_context_templates(H.model,H.tok)) for r in requests}
        P=H.compute_P(hp)
        H.my_edit(hp,requests,P,[torch.zeros(4,4) for _ in hp.layers])
        reference=H.snap_layers(hp);H.restore_layers(hp,snap)
        capture=A.capture_solve(H,hp,requests,P,[torch.zeros(4,4) for _ in hp.layers])
        self.assertEqual(set(capture),set(hp.layers))
        for layer in hp.layers:
            self.assertLessEqual(A.relative_distance(H.snap_layers(hp)[layer],reference[layer]),1e-4)
            self.assertTrue(torch.equal(capture[layer]['R'],capture[layer]['A0']))
    def test_three_forced_zero_lr_iterations_and_telemetry_trajectory(self):
        for mode in ('e2e','anchor'):
            trajectories=[];weights=[];returns=[]
            for telemetry_on in (False,True):
                H=make_h();hp=H.hp;requests=[H.req(H.CANON,s,'Echo Echo') for s in H.FICTION]
                H.Z_OVERRIDE={(r['subject'],r['target_new']['str']):H.compute_z(H.model,H.tok,r,hp,8,H.get_context_templates(H.model,H.tok)) for r in requests}
                writer=A.Writer(H,hp,telemetry=A.telemetry_factory(self.out/(mode+str(telemetry_on)),'s1','fixed',telemetry_on))
                writer.baseline_passed=True
                returns.append(writer.write(mode,requests,H.compute_P(hp),[torch.zeros(4,4) for _ in hp.layers],check=True,iterations=3,lr_override=0.,force_steps=True))
                trajectories.append(writer.trajectory);weights.append(H.snap_layers(hp))
                self.assertEqual(writer.last_trace['accepted_steps'],3)
                self.assertEqual(len(writer.trajectory),3)
                self.assertTrue(all(p.grad is None for p in H.model.parameters()))
            self.assertEqual(returns[0],returns[1])
            for one,two in zip(trajectories[0],trajectories[1]):
                self.assertTrue(all(torch.equal(one[l],two[l]) for l in one))
            self.assertTrue(all(torch.equal(weights[0][l],weights[1][l]) for l in weights[0]))
    def test_candidate_operations_require_baseline(self):
        H=make_h();writer=A.Writer(H,H.hp);writer.mode='e2e'
        before=len(H.model.forward_inputs)
        with self.assertRaises(A.Halt) as caught: writer(H.hp,[H.req(H.CANON,H.FICTION[0],'Echo Echo')],H.compute_P(H.hp),[torch.zeros(4,4) for _ in H.hp.layers])
        self.assertEqual(caught.exception.code,'LAW#3-BEFORE-CANDIDATES')
        self.assertEqual(len(H.model.forward_inputs),before)
    def test_stored_control_scale1_identity(self):
        H=make_h();snap=H.snap_layers(H.hp)
        updates={l:torch.ones_like(snap[l]).float()*0.01 for l in H.hp.layers}
        actual=A.apply_stored(H,H.hp,snap,updates,1.)
        self.assertEqual(set(actual),set(H.hp.layers))
        for l in H.hp.layers: self.assertTrue(torch.equal(H.snap_layers(H.hp)[l],(snap[l]+updates[l].half()).half()))
    def test_strict_json_and_immutable_records(self):
        path=self.root/'record.json';value={'tuple':(1,2),'null':None,'nested':[True,0.1]}
        A.write_json(path,value)
        self.assertEqual(A.strict_load(path),{'tuple':[1,2],'null':None,'nested':[True,0.1]})
        before=path.read_bytes()
        with self.assertRaises(A.Halt): A.write_json(path,{'changed':True})
        self.assertEqual(path.read_bytes(),before)
        for text in ('{"x":NaN}','{"x":Infinity}','{"x":-Infinity}'):
            path=self.root/'nonfinite.json';path.write_text(text)
            with self.assertRaises(ValueError): A.strict_load(path)
    def test_actual_launcher_refuses_missing_calibration_before_import(self):
        go=self.root/'go.json';go.write_text(json.dumps({'decision_id':'D-go','experiment':'C10Y','stage':1,'recorded_in':'program/runbook/:5','at':'2026-10-08T00:00:00Z'}))
        forecast=self.root/'forecast.json';forecast.write_text(json.dumps({'stage':1,'phases':[]}))
        calls=[]
        original=importlib.import_module
        def imports(name,*args,**kwargs):
            calls.append(name)
            if name=='c10e_bandknob': raise AssertionError('REAL HARNESS IMPORT BLOCKED')
            return original(name,*args,**kwargs)
        with mock.patch.object(importlib,'import_module',side_effect=imports):
            code=A.main(['--budget-gate','--stage','1','--out',str(self.out),'--halt-diagnostic',str(self.diagnostic),'--go',str(go),'--forecast',str(forecast)])
        self.assertNotEqual(code,0);self.assertNotIn('c10e_bandknob',calls)
    def test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates(self):
        H=make_h();calls=[]
        # Contract-shaped restored harness: deliberately failed baseline.
        raw=valid_record(1)['recipes']['A']
        raw['arms']['A7_coined_coined']['metrics']['para_full_n']=19
        def recipe(name,path):
            calls.append(name)
            return copy.deepcopy(raw)
        H.run_recipe=recipe
        H.my_edit=lambda *args:(_ for _ in ()).throw(AssertionError('candidate called'))
        go={'decision_id':'D-go','experiment':'C10Y','stage':1,'recorded_in':'program/runbook/:5','at':'2026-10-08T00:00:00Z'}
        forecast=self.forecast()
        result=A.run(self.out,H,stage=1,go=go,forecast=forecast,diagnostic=self.diagnostic)
        self.assertEqual(result['run']['status'],'HALTED')
        self.assertEqual(calls,['A'])
        self.assertEqual(R.classify(R.load(self.out))['label'],'HALTED')
        before={p:p.read_bytes() for p in self.out.rglob('*') if p.is_file()}
        with self.assertRaises(A.Halt):
            A.run(self.root/'results/c10y_directdw_s2_rerun1',H,stage=2,go=dict(go,stage=2),spend={'decision_id':'D-spend','stage':2,'cap_s':7200.},forecast=self.forecast(2),predecessor=self.out,diagnostic=self.root/'architecture_profile/later.json')
        self.assertEqual(before,{p:p.read_bytes() for p in before})
    def forecast(self,stage=1):
        evidence=self.root/'timing.json'
        evidence.write_text('{}')
        return {'stage':stage,'phases':[{'name':name,'artifact':str(evidence),'sha256':hashlib.sha256(evidence.read_bytes()).hexdigest(),'workload':'isolated tiny fixture','repetitions':1,'scaling_assumption':'fixture bound','measured':False,'justification':'synthetic CPU bound; runtime unverified','upper_s':1380. if name=='readout' else 10.} for name in A.FORECAST_PHASES]}
    def test_native_hanging_worker_deadline_before_and_after_write(self):
        # Execution awaits the explicitly requested process-count resolution.
        self.assertEqual(os.environ.get('C10Y_ALLOWED_CHILD_TESTS'),'1','prescribed child test authorization pending')
        import subprocess
        for completed in (False,True):
            out=self.root/('after' if completed else 'before');out.mkdir()
            worker=self.root/('worker_after.py' if completed else 'worker_before.py')
            marker="from pathlib import Path\nPath(%r).write_text('{}')\n" % str(out/'write_complete_s1.json') if completed else ''
            worker.write_text('import ctypes\n'+marker+'ctypes.CDLL(None).sleep(30)\n')
            site=self.root/'site';site.mkdir(exist_ok=True)
            code='import os,sys\nfrom pathlib import Path\nW=Path(%r)\nSCRATCH=Path(%r)\n' % (str(W),str(SCRATCH))
            code+=inspect.getsource(install_guard)+'\ninstall_guard()\nprint("C10Y_CHILD_WRITE_GUARD",flush=True)\n'
            (site/'sitecustomize.py').write_text(code)
            env=dict(os.environ,LLMDB_ROOT=str(self.root),PYTHONPATH=str(site),PYTHONDONTWRITEBYTECODE='1',
                     C10Y_STUB_WORKERS=json.dumps({str(worker):hashlib.sha256(worker.read_bytes()).hexdigest()}))
            began=time.monotonic()
            result=A.supervise([sys.executable,'-B',str(worker)],out,self.root/('halt'+str(completed)+'.json'),cap_s=2.,stage=1,env=env)
            self.assertLess(time.monotonic()-began,3.5)
            self.assertEqual(result['status'],'INCOMPLETE-BUDGET' if completed else 'HALTED-BUDGET')
            diagnostic=A.strict_load(self.root/('halt'+str(completed)+'.json'))
            self.assertEqual(diagnostic.get('phase'),'supervisor_deadline')
            self.assertIsNone(diagnostic.get('traceback'))
            self.assertTrue(diagnostic.get('traceback_unavailable'))
            self.assertEqual(A.strict_load(out/'supervisor_s1.json').get('phase'),'supervisor_deadline')
            self.assertIn('C10Y_CHILD_WRITE_GUARD',result['output'])
            self.assertNotEqual(result['process_group'],os.getpgrp())
            with self.assertRaises(ProcessLookupError): os.kill(result['pid'],0)


def listing():
    data={}
    for directory in ('results','architecture_profile'):
        for p in (W/directory).rglob('*'):
            st=p.lstat();data[str(p.relative_to(W))]=(st.st_size,st.st_mtime_ns)
    return data


def main():
    before=listing()
    suite=unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    after=listing()
    drift=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)]
    owned=[p for p in drift if p.startswith(('results/c10y_','architecture_profile/c10y_','architecture_profile/s')) and
           (p.startswith(('results/c10y_','architecture_profile/c10y_')) or '_halt_diagnostic' in p)]
    print('ISOLATION OWNED LISTING DRIFT:',json.dumps(owned))
    print('ISOLATION OTHER OBSERVED UNATTRIBUTED:',json.dumps([p for p in drift if p not in owned]))
    forbidden=[n for n in ('c10e_bandknob','transformers','datasets') if n in sys.modules]
    print('SYS_MODULES_FORBIDDEN:',json.dumps(forbidden))
    if result.wasSuccessful() and not owned and not forbidden:
        print('C10Y_DIRECTDW_SELFTEST PASS — CPU ONLY; LIVE LAW#3/LAW#5 UNVERIFIED')
        return 0
    return 1


class CalibrationTests(IsolatedCase):
    def records(self):
        go={'decision_id':'D-go','experiment':'C10Y','stage':'calibration','recorded_in':'program/runbook/:5','at':'2026-10-08T00:00:00Z'}
        spend={'decision_id':'D-spend','stage':'calibration','cap_s':7200.}
        return go,spend
    def fixture(self):
        return {'timings':[{'name':'smoke_step','seconds':1.,'workload':{'accepted_steps':1,'requests':24,'micro_batches':4,'padded_lengths':[12]*4,'retries':0},'repetition':i+1,'accepted':True,'loss_scale_halvings':0} for i in range(3)],'T_cal':12,'template_token_lengths':[1,4,4,4,4,4],'checks':{'merged_evaluations':['zero_step','executed_loop','init_parity']},'contexts':[['{}'],['Frame {}']],'targets':{},'ledger':[],'law5':{},'step0':{}}
    def test_calibration_go_spend_caps(self):
        go,spend=self.records()
        self.assertEqual(A.launch_documents('calibration',go,spend,None),7200.)
        for cap in (0.,-1.,True,float('inf'),float('nan'),7200.001):
            with self.subTest(cap=cap),self.assertRaises(A.Halt): A.launch_documents('calibration',go,dict(spend,cap_s=cap),None)
        with self.assertRaises(A.Halt): A.launch_documents('calibration',go,None,None)
    def test_calibration_telemetry_variables_and_existing_directory_refused(self):
        go,spend=self.records();out=self.root/'experiments/c10y/runs/c10y_directdw_calib1'
        for name in ('C10Y_TELEMETRY','C10Y_TELEMETRY_INERTNESS'):
            with mock.patch.dict(os.environ,{name:''}),self.assertRaises(A.Halt): A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
        self.assertFalse(out.exists());out.mkdir()
        with self.assertRaises(A.Halt): A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
    def test_calibration_wrong_namespace_refused(self):
        go,spend=self.records()
        for out in (self.out,self.root/'results/c10y_directdw_s1_rerun1',self.root/'results/c10y_directdw_calib0'):
            with self.subTest(out=out),self.assertRaises(A.Halt): A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
    def test_calibration_prefix_only_and_required_records(self):
        go,spend=self.records();out=self.root/'experiments/c10y/runs/c10y_directdw_calib1';H=make_h();calls=[]
        H.run_recipe=lambda *args:(_ for _ in ()).throw(AssertionError('substantive recipe outside prefix'))
        def prefix(H,out,budget,calibration=False,telemetry=None):
            calls.append(calibration);return self.fixture()
        with mock.patch.object(A,'instrument_prefix',side_effect=prefix):
            record=A.calibrate(out,H,go=go,spend=spend,diagnostic=self.diagnostic)
        self.assertEqual(record.get('outcome'),'COMPLETE');self.assertEqual(calls,[True])
        self.assertEqual(record['checks']['merged_evaluations'],['zero_step','executed_loop','init_parity'])
        names={p.name for p in out.iterdir() if p.is_file()}
        self.assertTrue({'calibration.json','context_templates_calib.json','overlap_audit_calib.json','targets_calib.pt','ledger_calib.json','law5_calib.json','step0_calib.json','run.json'}<=names)
        self.assertFalse(names & {'screen.json','pass_p1.json','pass_p2.json','repro.json'})
        self.assertEqual(A.strict_load(out/'run.json')['telemetry'],False)
    def test_calibration_v4_halt_persists_schedule(self):
        go,spend=self.records();out=self.root/'experiments/c10y/runs/c10y_directdw_calib1'
        with mock.patch.object(A,'instrument_prefix',side_effect=A.Halt('LAW#3')):
            record=A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
        self.assertEqual(record.get('outcome'),'LAW#3')
        with self.assertRaises(A.Halt): A.refuse_schedule_halt(self.root)
        self.assertEqual(A.strict_load(self.diagnostic)['process'],'calibration')
    def test_calibration_reader_and_context_source_refused(self):
        out=self.root/'experiments/c10y/runs/c10y_directdw_calib1';out.mkdir()
        (out/'calibration.json').write_text('{"outcome":"COMPLETE"}')
        with self.assertRaises((ValueError,RuntimeError)): R.load(out)
        contexts=out/'context_templates_calib.json';contexts.write_text('[["{}"]]')
        with self.assertRaises(A.Halt): A.stage_context_source(contexts,hashlib.sha256(contexts.read_bytes()).hexdigest())
    def test_calibration_forecast_rejects_partial_and_stale(self):
        identity=A.calibration_identity()
        record={'outcome':'HALTED-BUDGET',**identity,'timings':[]}
        path=self.root/'calibration.json';path.write_text(json.dumps(record))
        self.assertEqual(A.calibration_forecast(path,[])['status'],'UNVERIFIED')
        record['outcome']='COMPLETE';record['sources']['driver']='0'*64;path.write_text(json.dumps(record))
        self.assertEqual(A.calibration_forecast(path,[])['status'],'UNVERIFIED')
    def test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs(self):
        identity=A.calibration_identity();record={'outcome':'COMPLETE',**identity,'timings':[{'name':'smoke_step','seconds':float(i),'workload':{'requests':24,'padded_lengths':[12]*4},'repetition':i} for i in (1,2,3)],'contexts':['LEAK'],'targets':{'LEAK':1},'memory':{'driver_bytes':2**60}}
        path=self.root/'calibration.json';path.write_text(json.dumps(record))
        bounds=[{'name':name,'timing_names':['smoke_step'],'upper_s':7200./len(A.FORECAST_PHASES),'workload':'frozen stage1 includes 105 optimisation iterations','repetitions':3,'scaling_assumption':'independent fixture bound including padded-length dependence','justification':'synthetic bound, never live dispatch evidence'} for name in A.FORECAST_PHASES]
        forecast=A.calibration_forecast(path,bounds)
        self.assertEqual(forecast.get('status'),'READY')
        self.assertEqual(A.budget_gate(forecast,7200.)['status'],'READY')
        text=json.dumps(forecast);self.assertNotIn('LEAK',text);self.assertNotIn('driver_bytes',text)
        self.assertEqual(len(forecast['phases'][0]['measurements']),3)
        bounds[0]['upper_s']+=.001
        self.assertEqual(A.budget_gate(A.calibration_forecast(path,bounds),7200.)['status'],'HALTED-BUDGET')
    def test_frozen_bytes_suite_end(self):
        table=json.loads((SCRATCH/'before/r5_post_pin_sha256.json').read_text())
        actual={name:hashlib.sha256((Path(name) if Path(name).is_absolute() else W/name).read_bytes()).hexdigest() for name in table}
        self.assertEqual(actual,table)


"""C10Y reader contract tests. Inject R and IsolatedCase before evaluation.

P = experiments/c10y/design/C10Y_DIRECTDW_PREREG.md, pinned amended document, 2026-10-08.
B = /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codex_c10y_build_brief.md.
Fixtures are machine records, never empirical model evidence. No code is run
when this file is written. All TestCases inherit the parent's IsolatedCase.
"""

import copy
import hashlib
import json
import math
import unittest
from pathlib import Path


PREREG_SHA = "e069b358c362b2a05e3b668e8a29f33061e15a24306e321452e6fa46a4e83331"
ENGINE_SHA = "d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65"
MODEL_REV = "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
SHA = "1" * 64
ARMS = ("A1_single", "A2_coherent2", "A7_coined_coined")
A7 = ARMS[2]
LAYERS = (4, 5, 6, 7, 8)
FRAMES = ("CANON", "frame0", "frame1", "frame2", "frame3", "frame4", "frame5")
SOURCE_PATHS = {
    "driver": "code/lab/track_c/c10y_directdw_arms.py",
    "reader": "code/lab/track_c/c10y_directdw_read.py",
    "check": "code/lab/track_c/c10y_directdw_telemetry_check.py",
    "harness": "code/lab/track_c/c10e_bandknob.py",
    "templates": "code/lab/track_c/c10z_astra_benchmark.py",
    "hparams": "code/configs/hparams/qwen25_3b_memit_hparams.json",
    "compute_z": "code/memit/vendor/memit/compute_z.py",
    "compute_ks": "code/memit/vendor/memit/compute_ks.py",
    "repr_tools": "code/memit/vendor/rome/repr_tools.py",
    "memit_main": "code/memit/vendor/memit/memit_main.py",
    "prereg": "experiments/c10y/design/C10Y_DIRECTDW_PREREG.md",
}
W = Path("/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def geometry(norms=None):
    values = [1.0] * 5 if norms is None else list(norms)
    return [
        {
            "layer": layer,
            "planned_norm": norm,
            "actual_norm": norm,
            "planned_null_share": 1.0 if norm else None,
            "actual_null_share": 1.0 if norm else None,
            "zero_update": norm == 0,
            "planned_covariance_energy": 0.0,
            "actual_covariance_energy": 0.0,
            "cosine_to_A": 1.0 if norm else None,
            "cosine_to_candidate": 1.0 if norm else None,
            "reduction_dtype": "float64",
            "reduction_device": "cpu",
        }
        for layer, norm in zip(LAYERS, values)
    ]


def set_counts(arm, para_full=None, canon=None, para_first=None, shift=0):
    m = arm["metrics"]
    if para_full is not None:
        m["para_full_n"] = para_full
    if canon is not None:
        m["canon_full_n"] = canon
    if para_first is not None:
        m["para_first_n"] = para_first
    m["para_string_n"] = max(m.get("para_string_n", 72), m["para_full_n"])
    m["cond_full_given_first"] = m["para_full_n"] / m["para_first_n"] if m["para_first_n"] else None
    m["cond_full_given_first_denominator"] = m["para_first_n"]
    m["cond_full_given_first_undefined_reason"] = None if m["para_first_n"] else "zero-first-token-hits"
    full_indices = {(i + shift) % 72 for i in range(m["para_full_n"])}
    first_indices = full_indices | set(range(m["para_first_n"]))
    # Readout flags carry the exact immutable subject/PTEST key that R3 uses.
    arm["detail"] = [
        {
            "subj": "subject%02d" % i,
            "val": "value%02d" % i,
            "ntok": 1 if arm["arm"] == ARMS[0] else 4,
            "canon_full": i < m["canon_full_n"],
            "canon_first": i < m["canon_full_n"],
            "para_full_hits": [3 * i + k in full_indices for k in range(3)],
            "para_first_hits": [3 * i + k in first_indices for k in range(3)],
            "para_string_hits": [True] * 3,
            "tf_correct": 0 if arm["arm"] == ARMS[0] else 9,
            "tf_total": 0 if arm["arm"] == ARMS[0] else 9,
        }
        for i in range(24)
    ]
    return arm


def check_records(mode, arm):
    names = ["capture", "zero_step", "executed_loop", "projector", "hooks"]
    if mode == "apply_stored":
        names = ["scale1", "hooks", "stored_geometry", "merged_readouts"]
    else:
        names += ["train_deploy", "gradient"]
        if arm == A7:
            names += ["accumulation"]
            if mode == "e2e":
                names += ["objective"]
        if mode == "e2e" and arm == A7:
            names += ["smoke"]
    checks = {
        name: {"passed": True, "before_result": True, "scope": {"mode": mode, "arm": arm}}
        for name in names
    }
    distances = {str(layer): 0.0 for layer in LAYERS}
    for name in ("capture", "zero_step", "executed_loop", "scale1"):
        if name in checks:
            checks[name].update(distance_by_layer=distances.copy(), counts_equal=True)
            if name in ("capture", "scale1"):
                checks[name]["floor"] = 0.0
    if "executed_loop" in checks:
        checks["executed_loop"].update(forced_iterations=3, lr=0.0, early_stopping=False, adam_steps=3, routing_executed=True, accumulation_batches=[6, 6, 6, 6], loss_scaling_executed=True)
    checks["hooks"].update(registries_equal=True, writer_handles_removed=True, unknown_hooks_preserved=True, pristine_restored=True, wrapper_restored=True, overrides_restored=True)
    if "projector" in checks:
        checks["projector"].update(init_planned_share_by_layer={str(layer): 1.0 for layer in LAYERS}, init_actual_share_by_layer={str(layer): 1.0 for layer in LAYERS})
    if "objective" in checks:
        checks["objective"].update(nll_errors=[0.0] * 24, KL_errors={"init_raw": 0.0, "init_weighted": 0.0, "nonzero_raw": 0.0, "nonzero_weighted": 0.0}, constructed_like_compute_z=True)
    if "accumulation" in checks:
        checks["accumulation"].update(subset=list(range(12)), splits=[[6, 6], [5, 7]], weighted_by_request_count=True, reference_headroom_ok=True, gradients=[{"layer": layer, "split": split, "finite": True, "norm": 1.0, "cosine": 1.0, "relative_l2": 0.0} for split in ("6+6", "5+7") for layer in LAYERS])
    if "gradient" in checks:
        checks["gradient"].update(init_loss_scale=1024, halvings=0, layers=[{"layer": layer, "finite": True, "norm": 1.0} for layer in LAYERS], base_gradients_absent=True, only_A_optimised=True, eval_mode=True, use_cache=False)
    if "smoke" in checks:
        checks["smoke"].update(steps=3, nonzero_lr=True, A_changed_layers=[True] * 5, gradient_finite_layers=[True] * 5, loss_before=1.0, loss_after=0.9, base_hash_unchanged=True, restored=True, synchronised=True)
    return checks


def arm_record(recipe, arm, para_full=23, canon=20, para_first=60):
    mode = "anchor" if recipe == "B-z" else "apply_stored" if recipe in ("B-e2e-NM", "B-e2e-ENV") else "e2e"
    out = {
        "status": "COMPLETED",
        "arm": arm,
        "metrics": {
            "canon_full_n": canon,
            "canon_n": 24,
            "para_full_n": para_full,
            "para_first_n": para_first,
            "para_string_n": 72,
            "para_n": 72,
            "tf_pertok_cont": None if arm == ARMS[0] else 100.0,
            "tf_pertok_cont_denominator": 0 if arm == ARMS[0] else 216,
            "tf_pertok_cont_undefined_reason": "zero-continuation-tokens" if arm == ARMS[0] else None,
            "cond_full_given_first": para_full / para_first if para_first else None,
            "cond_full_given_first_denominator": para_first,
            "cond_full_given_first_undefined_reason": None if para_first else "zero-first-token-hits",
        },
        "locality": {
            "L1_flips": 0,
            "L1_n": 12,
            "frame_flips": {frame: 0 for frame in FRAMES},
            "frame_n": 6,
            "described_as_raw": 100.0,
            "described_as": 100.0,
            "L3_agreement": 30,
            "L3_n": 30,
            "L3_mean_kl": 0.0,
            "generic_ppl_raw": 10.0,
            "generic_ppl": 10.0,
            "generic_ppl_pre_raw": 10.0,
            "relation_label_flips": {"associated_with": 0, "is_a": 0},
        },
        "geometry": geometry(),
        "checks": {} if recipe == "A" else check_records(mode, arm),
        "train_deploy": None if recipe == "A" or mode == "apply_stored" else {
            state: {"ids_equal": True, "full_hits_equal": True, "losses": {"total": [0.0001, 0.0001], "L_z": [0.0001, 0.0001]} if recipe == "B-z" else {"total": [0.1, 0.1], "L_edit": [0.1, 0.1], "KL_raw": [0.0, 0.0], "weighted_KL": [0.0, 0.0]}}
            for state in ("init", "final")
        },
        "trace": {
            "stop_reason": "threshold",
            "accepted_steps": 3,
            "overflow_retries": 0,
            "loss_scale_halvings": 0,
            "loss_components": [{"accepted_step": step, "total": loss, "L_z": loss} if recipe == "B-z" else {"accepted_step": step, "total": loss, "L_edit": loss, "KL_raw": 0.0, "weighted_KL": 0.0} for step, loss in enumerate((0.08, 0.065, 0.052, 0.0001 if recipe == "B-z" else -math.log(0.96)))],
            "planned_norms_by_step": [[1.0] * 5 for _ in range(4)],
            "wall_clock_s": 30.0,
            "memory_by_phase": {phase: {"driver_bytes": 10 * 1024 ** 3, "current_bytes": 8 * 1024 ** 3, "rss_bytes": 10 * 1024 ** 3, "host_available_bytes": 20 * 1024 ** 3, "synchronised": True} for phase in ("projector", "capture", "parity", "backward", "merge", "evaluation")},
        },
        "H_out": {"tensors": [{"name": "model.layers.%d.mlp.down_proj" % layer, "dtype": "float32", "shape": [2048, 11008], "sha256": SHA} for layer in LAYERS], "actual_band_sha256": SHA, "overlay_sha256": SHA},
        "compile_s": 100.0,
        "fit": None if recipe == "A" else {
            "f_ij": [[0.96] * 6 for _ in range(24)],
            "L_z": 0.0001,
            "r_ij": [[0.01] * 6 for _ in range(24)],
            "delta_norms": [1.0] * 24,
            "residual_norms": [[0.01] * 6 for _ in range(24)],
            "merged": True,
        },
    }
    if arm in (ARMS[0], A7) and recipe in ("A", "B-z", "B-e2e"):
        out["remaining_ratios"] = {"canonical": 0.028, "heldout": [0.232] * 3}
    if mode == "apply_stored":
        out["stored_control"] = {"scale": 1.0, "source_recipe": "B-e2e", "source_arm": arm, "source_sha256": SHA, "scale1_reference": None, "independently_regenerated": True}
    return set_counts(out)


def recipe_record(recipe, stage):
    arms = {}
    for arm in ARMS:
        if recipe == "B-e2e" and stage == 1 and arm != A7:
            arms[arm] = {"status": "NOT-RUN"}
        else:
            n = 12 if recipe == "A" and arm == A7 else 13 if recipe == "B-z" and arm == A7 else 23 if arm == A7 else 68
            canon = 7 if recipe == "A" and arm == A7 else 20 if arm == A7 else 24
            first = 48 if recipe == "A" and arm == A7 else max(n, 60)
            arms[arm] = arm_record(recipe, arm, n, canon, first)
            hout=arms[arm]['H_out']
            hout.update(overlay_artifact='targets_%s.pt'%('s1' if stage==1 else 'p%d'%(stage-1)),
                        overlay_member=['actual_updates',recipe,arm],tensor_certificate_sha256=digest(hout['tensors']))
    return {"status": "COMPLETED", "law5": {"verdict": "INERT", "delta_expr": 0.0, "delta_loc": 0.0}, "arms": arms}


def valid_record(stage=1):
    """Complete scientific fixture; no empirical/runtime claim. P:85–117,179–204."""
    requests = {arm: [{"subject": "subject%02d" % i, "target": " value%02d" % i} for i in range(24)] for arm in ARMS}
    parts = {
        "requests": requests,
        "model_id": "Qwen/Qwen2.5-3B",
        "model_rev": MODEL_REV,
        "base_artifact_sha256": SHA,
        "tokenizer_artifacts_sha256": SHA,
        "tokenizer_settings": {"padding_side": "right"},
        "covariance_sha256": {str(layer): SHA for layer in LAYERS},
        "hparams_sha256": SHA,
        "context_templates_sha256": SHA,
        "stimuli": {"CANON": "The capital of {} is", "PTEST": ["Heldout %d {}" % k for k in range(3)], "ARMS": {arm: {"subject%02d" % i: "value%02d" % i for i in range(24)} for arm in ARMS}},
        "prereg_sha256": PREREG_SHA,
        "source_paths": SOURCE_PATHS.copy(),
        "objective": {"KL_coefficient": 0.0625, "routing": True, "parameter_dtype": "float32", "model_dtype": "float16"},
        "optimiser": {"name": "Adam", "betas": [0.9, 0.999], "eps": 1e-8, "weight_decay": 0, "lr_multiplier": 0.02, "T_max": 100, "loss_scale": 1024, "micro_batches": [6, 6, 6, 6]},
        "stage_table": {"1": "A7-screen", "2": "process1", "3": "process2"},
        "seed": 0,
        "device": "mps",
        "library_versions": {"python": "3.11", "torch": "fixture", "transformers": "4.51.0", "backend": "mps"},
    }
    sources = {name: ENGINE_SHA if name == "memit_main" else PREREG_SHA if name == "prereg" else SHA for name in SOURCE_PATHS}
    parts["source_sha256"] = sources.copy()
    recipes = {name: recipe_record(name, stage) for name in (("A", "B-e2e") if stage == 1 else ("A", "B-e2e", "B-z"))}
    ledger = []
    for name, recipe in recipes.items():
        for arm, data in recipe["arms"].items():
            ledger.append({"stage": stage, "recipe": name, "arm": arm, "check": "write", "status": data["status"], "declared_overrides": requests[arm] if data["status"] == "COMPLETED" else [], "consumed_overrides": requests[arm] if data["status"] == "COMPLETED" else []})
            for check in data.get("checks", {}):
                ledger.append({"stage": stage, "recipe": name, "arm": arm, "check": check, "status": "COMPLETED", "declared_overrides": requests[arm], "consumed_overrides": requests[arm]})
    return {
        "schema": "c10y_directdw/v1",
        "stage": stage,
        "manifest": {
            "prereg_sha256": PREREG_SHA,
            "H_in": digest(parts),
            "parts": parts,
            "sources_start": copy.deepcopy(sources),
            "sources_end": copy.deepcopy(sources),
            "input_hashes_start": {"contexts": SHA, "hparams": SHA, "covariance": SHA, "model": SHA, "tokenizer": SHA},
            "input_hashes_end": {"contexts": SHA, "hparams": SHA, "covariance": SHA, "model": SHA, "tokenizer": SHA},
            "artifacts": {"context_templates.json": SHA, "targets_%s.pt" % ("s1" if stage == 1 else "p%d" % (stage - 1)): SHA},
            "context_templates": {"path": "context_templates.json", "sha256": SHA},
        },
        "run": {"stage": stage, "status": "COMPLETED", "code": None, "launched": True, "write_complete": True, "readout_complete": True, "telemetry": False, "telemetry_inertness": None},
        "instrument": {"fingerprint": {"sha256": ENGINE_SHA, "cov_cpu_sites": 3, "output": "engine fingerprint PASS\n_cov_cpu=3\n"}, "baseline_before_candidates": True},
        "overlap_audit": {"clean": True, "rule": "casefold,punctuation-remove,whitespace-collapse,preserve-placeholder,exact-and-containment", "matches": []},
        "ledger": ledger,
        "recipes": recipes,
    }


def add_controls(record, nm_count=26, env_count=24, candidate_norms=None):
    """P:80–81,99–103,255–258: every triggered recipe supplies all arms."""
    candidate_norms = [2.0, 1.0, 1.0, 1.0, 1.0] if candidate_norms is None else list(candidate_norms)
    stage = record["stage"]
    record["recipes"]["B-e2e-NM"] = recipe_record("B-e2e-NM", stage)
    record["recipes"]["B-e2e-ENV"] = recipe_record("B-e2e-ENV", stage)
    for arm in ARMS:
        candidate = record["recipes"]["B-e2e"]["arms"][arm]
        if candidate["status"] != "COMPLETED":
            continue
        candidate["geometry"] = geometry(candidate_norms)
        scale_nm = 5.0 / sum(candidate_norms)
        scale_env = min(1.0, min(1.0 / norm for norm in candidate_norms if norm))
        for name, scale, count in (("B-e2e-NM", scale_nm, nm_count), ("B-e2e-ENV", scale_env, env_count)):
            control = record["recipes"][name]["arms"][arm]
            control["geometry"] = geometry([norm * scale for norm in candidate_norms])
            control["stored_control"]["scale"] = scale
            control["stored_control"]["source_process"] = stage
            if arm == A7:
                set_counts(control, para_full=count)
            overrides = record["manifest"]["parts"]["requests"][arm]
            record["ledger"].append({"stage": stage, "recipe": name, "arm": arm, "check": "write", "status": "COMPLETED", "declared_overrides": overrides, "consumed_overrides": overrides})
            for check in control["checks"]:
                record["ledger"].append({"stage": stage, "recipe": name, "arm": arm, "check": check, "status": "COMPLETED", "declared_overrides": overrides, "consumed_overrides": overrides})
    return record


def valid_repro(p1, p2):
    def arms(recipe):
        return {arm: {"layers": [{"layer": layer, "norm_p1": p1["recipes"][recipe]["arms"][arm]["geometry"][i]["actual_norm"], "norm_p2": p2["recipes"][recipe]["arms"][arm]["geometry"][i]["actual_norm"], "cosine": 1.0, "distance": 0.0} for i, layer in enumerate(LAYERS)]} for arm in ARMS}
    return {"H_in": p1["manifest"]["H_in"], "reduction_dtype": "float64", "reduction_device": "cpu", "baseline": {"arms": arms("A")}, "recipes": {name: {"arms": arms(name)} for name in p1["recipes"] if name != "A" and name in p2["recipes"]}}


def bind_fixture_overlays(record):
    overlay='targets_%s.pt'%('s1' if record['stage']==1 else 'p%d'%(record['stage']-1))
    artifacts=record['manifest']['artifacts'];artifacts.setdefault(overlay,SHA)
    for name,recipe in record['recipes'].items():
        for arm,data in recipe.get('arms',{}).items():
            if data.get('status')!='COMPLETED': continue
            hout=data['H_out'];hout.update(overlay_artifact=overlay,overlay_member=['actual_updates',name,arm],
                overlay_sha256=artifacts[overlay],tensor_certificate_sha256=digest(hout['tensors']))
            if 'stored_control' in data: data['stored_control']['source_sha256']=artifacts[overlay]


class ReaderCase(IsolatedCase):
    def classify(self, record, recipe="B-e2e"):
        result = R.classify(record, recipe=recipe)
        self.assertIsInstance(result, dict)
        return result

    def result(self, record, label, recipe="B-e2e", include=(), exclude=(), advance=None):
        result = self.classify(record, recipe)
        self.assertEqual(result.get("label"), label)
        self.assertIsInstance(result.get("qualifiers"), list)
        for item in include:
            self.assertIn(item, result["qualifiers"])
        for item in exclude:
            self.assertNotIn(item, result["qualifiers"])
        if advance is not None:
            self.assertIs(result.get("advance"), advance)
        return result

    def pair(self, p1, p2, label, repro=None, include=(), exclude=(), advance=None):
        if repro is None and p2 is not None and "A" in p2.get("recipes", {}):
            repro = valid_repro(p1, p2)
        result = R.cross_process(p1, p2, repro)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("label"), label)
        for item in include:
            self.assertIn(item, result.get("qualifiers", []))
        for item in exclude:
            self.assertNotIn(item, result.get("qualifiers", []))
        if advance is not None:
            self.assertIs(result.get("advance"), advance)
        return result

    def candidate(self, record, arm=A7):
        return record["recipes"]["B-e2e"]["arms"][arm]


class ReaderOrderTests(ReaderCase):
    # P:183,204; B:40,67,112. Recorded outcomes precede missing evidence.
    def test_recorded_halt_invalid_and_budget_first(self):
        for status in ("HALTED", "INVALID", "HALTED-BUDGET", "INCOMPLETE-BUDGET"):
            with self.subTest(status=status):
                record = valid_record()
                record["run"].update(status=status, code="recorded-cause")
                record["recipes"] = {}
                del record["overlap_audit"]
                self.result(record, status, advance=False)

    def test_own_record_and_v5_missing_precede_validity_and_fit(self):
        for missing in ("recipe", ARMS[0], ARMS[1], A7):
            with self.subTest(missing=missing):
                record = valid_record(2)
                self.candidate(record)["fit"]["f_ij"][0][0] = 0.1
                record["recipes"]["B-e2e"]["law5"]["verdict"] = "NOT-INERT"
                if missing == "recipe":
                    del record["recipes"]["B-e2e"]
                else:
                    del record["recipes"]["B-e2e"]["arms"][missing]
                self.result(record, "INCOMPLETE", advance=False)

    def test_validity_precedes_fit_and_fit_precedes_counts(self):
        record = valid_record(2)
        arm = self.candidate(record)
        set_counts(arm, para_full=33)
        arm["fit"]["f_ij"][0][0] = 0.85
        arm["metrics"]["para_string_n"] = 32
        self.result(record, "INVALID", advance=False)
        arm["metrics"]["para_string_n"] = 72
        self.result(record, "UNDERFIT", advance=False)
        set_counts(arm, para_full=18)
        self.result(record, "UNDERFIT", advance=False)

    def test_stage1_not_run_controls_and_later_records_not_required(self):
        record = valid_record()
        self.result(record, "SCREEN-PASS", exclude=("SIZE-UNTESTED", "ANCHOR-UNTESTED"))
        del record["recipes"]["B-e2e"]["arms"][ARMS[0]]
        del record["recipes"]["B-e2e"]["arms"][ARMS[1]]
        self.result(record, "SCREEN-PASS")

    def test_missing_comparators_qualify_without_incomplete(self):
        record = add_controls(valid_record(2))
        set_counts(self.candidate(record), para_full=33)
        del record["recipes"]["B-e2e-NM"]
        self.result(record, "LEAD", include=("SIZE-UNTESTED",), advance=False)
        record = valid_record(2)
        del record["recipes"]["B-z"]
        self.result(record, "PARTIAL", include=("ANCHOR-UNTESTED",), advance=False)

    def test_existing_arm_missing_metric_is_v13_invalid(self):
        record = valid_record(2)
        del self.candidate(record)["metrics"]["para_string_n"]
        self.result(record, "INVALID", advance=False)

    def test_source_and_prereg_identity_refused(self):
        for field in ("prereg", "source", "input"):
            with self.subTest(field=field):
                record = valid_record()
                if field == "prereg":
                    record["manifest"]["prereg_sha256"] = "2" * 64
                elif field == "source":
                    record["manifest"]["sources_end"]["driver"] = "2" * 64
                else:
                    record["manifest"]["input_hashes_end"]["contexts"] = "2" * 64
                self.result(record, "INVALID", advance=False)


class ReaderValidityTests(ReaderCase):
    # P:185–198; B:113. Each miss has otherwise complete prerequisites.
    def test_v1_fingerprint_sha_sites_and_full_output(self):
        for field, value in (("sha256", "2" * 64), ("cov_cpu_sites", 2), ("cov_cpu_sites", 4), ("output", "")):
            with self.subTest(field=field, value=value):
                record = valid_record()
                record["instrument"]["fingerprint"][field] = value
                self.result(record, "HALTED", advance=False)

    def test_v2_each_recipe_standing_law5(self):
        record = valid_record(2)
        self.result(record, "PARTIAL")
        record["recipes"]["B-e2e"]["law5"]["verdict"] = "NOT-INERT"
        self.result(record, "INVALID", advance=False)

    def test_v3_check_failure_order_and_scope(self):
        for arm_name in ARMS:
            for failure in ("passed", "before_result", "scope"):
                with self.subTest(arm=arm_name, failure=failure):
                    record = valid_record(2)
                    check = self.candidate(record, arm_name)["checks"]["capture"]
                    check[failure] = False if failure != "scope" else {"mode": "anchor", "arm": arm_name}
                    self.result(record, "INVALID", advance=False)

    def test_v3_missing_required_check_invalid(self):
        for recipe in ("B-e2e", "B-z"):
            for arm_name in ARMS:
                record = valid_record(2)
                for check in tuple(record["recipes"][recipe]["arms"][arm_name]["checks"]):
                    with self.subTest(recipe=recipe, arm=arm_name, check=check):
                        invalid = copy.deepcopy(record)
                        del invalid["recipes"][recipe]["arms"][arm_name]["checks"][check]
                        self.result(invalid, "INVALID", recipe=recipe, advance=False)

    def test_v3_apply_stored_substitutions_not_optimiser_checks(self):
        record = add_controls(valid_record(2))
        self.result(record, "PARTIAL", recipe="B-e2e-NM")
        for check in ("scale1", "hooks", "stored_geometry", "merged_readouts"):
            with self.subTest(check=check):
                invalid = copy.deepcopy(record)
                invalid["recipes"]["B-e2e-NM"]["arms"][A7]["checks"][check]["passed"] = False
                self.result(invalid, "INVALID", recipe="B-e2e-NM", advance=False)

    def test_v3_capture_zero_step_and_executed_loop_raw_values(self):
        # P:129–131. A passed=True summary cannot overrule the raw reduction.
        for name in ("capture", "zero_step", "executed_loop"):
            for floor, distance, allowed in ((0.0, 0.0001, True), (0.0, 0.00010001, False), (0.0001, 0.001, True), (0.0001, 0.00100001, False)):
                record = valid_record()
                check = self.candidate(record)["checks"][name]
                self.candidate(record)["checks"]["capture"]["floor"] = floor
                check["distance_by_layer"]["8"] = distance
                self.result(record, "SCREEN-PASS" if allowed else "INVALID")
        for field, bad in (("forced_iterations", 2), ("forced_iterations", 4), ("lr", 0.01), ("early_stopping", True), ("counts_equal", False)):
            record = valid_record()
            self.candidate(record)["checks"]["executed_loop"][field] = bad
            self.result(record, "INVALID", advance=False)

    def test_v3_objective_nll_and_nonzero_kl_raw_boundaries(self):
        # P:134. All 24 NLL entries and both nonzero KL components are required.
        for field in ("nll", "init_raw", "init_weighted", "nonzero_raw", "nonzero_weighted"):
            for error in (0.002, 0.0020001):
                record = valid_record()
                check = self.candidate(record)["checks"]["objective"]
                if field == "nll":
                    check["nll_errors"][23] = error
                else:
                    check["KL_errors"][field] = error
                self.result(record, "SCREEN-PASS" if error == 0.002 else "INVALID")

    def test_v3_accumulation_raw_cosine_distance_finiteness_and_scope(self):
        # P:123,134. Fixed 12-request subset; 6+6/5+7 weighted comparisons.
        for field, inside, outside in (("cosine", 0.999, 0.9989999), ("relative_l2", 0.01, 0.0100001)):
            for value in (inside, outside):
                record = valid_record()
                self.candidate(record)["checks"]["accumulation"]["gradients"][-1][field] = value
                self.result(record, "SCREEN-PASS" if value == inside else "INVALID")
        for field, bad in (("subset", list(range(1, 13))), ("splits", [[6, 6], [6, 6]]), ("weighted_by_request_count", False)):
            record = valid_record()
            self.candidate(record)["checks"]["accumulation"][field] = bad
            self.result(record, "INVALID", advance=False)
        for field, bad in (("finite", False), ("norm", 0.0), ("norm", float("inf"))):
            record = valid_record()
            self.candidate(record)["checks"]["accumulation"]["gradients"][0][field] = bad
            self.result(record, "INVALID", advance=False)

    def test_v3_gradient_halvings_hooks_and_smoke_raw_values(self):
        # P:135–137. At most three init halvings, exact restoration, real smoke.
        for halvings in (3, 4):
            record = valid_record()
            self.candidate(record)["checks"]["gradient"]["halvings"] = halvings
            self.result(record, "SCREEN-PASS" if halvings == 3 else "INVALID")
        for field, bad in (("finite", False), ("norm", 0.0)):
            record = valid_record()
            self.candidate(record)["checks"]["gradient"]["layers"][0][field] = bad
            self.result(record, "INVALID", advance=False)
        for field in ("registries_equal", "writer_handles_removed", "unknown_hooks_preserved", "pristine_restored", "wrapper_restored", "overrides_restored"):
            record = valid_record()
            self.candidate(record)["checks"]["hooks"][field] = False
            self.result(record, "INVALID", advance=False)
        for field, bad in (("steps", 2), ("nonzero_lr", False), ("A_changed_layers", [True, True, True, True, False]), ("gradient_finite_layers", [False] + [True] * 4), ("base_hash_unchanged", False), ("restored", False)):
            record = valid_record()
            self.candidate(record)["checks"]["smoke"][field] = bad
            self.result(record, "INVALID", advance=False)

    def test_v4_all_inclusive_baseline_endpoints(self):
        for field, values, allowed in (("para_full_n", (4, 5, 18, 19), {5, 18}), ("canon_full_n", (4, 5, 10, 11), {5, 10}), ("para_first_n", (41, 42, 59, 60), {42, 59})):
            for value in values:
                with self.subTest(field=field, value=value):
                    record = valid_record()
                    baseline = record["recipes"]["A"]["arms"][A7]
                    set_counts(self.candidate(record), para_full=30)
                    set_counts(baseline, **{ {"para_full_n": "para_full", "canon_full_n": "canon", "para_first_n": "para_first"}[field]: value})
                    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")

    def test_v4_a1_a2_and_exact_denominators(self):
        for arm_name in ARMS[:2]:
            for value in (67, 68):
                record = valid_record()
                set_counts(record["recipes"]["A"]["arms"][arm_name], para_full=value)
                self.result(record, "SCREEN-PASS" if value == 68 else "HALTED")
        for field, bad in (("para_n", 71), ("para_n", 73), ("canon_n", 23), ("canon_n", 25)):
            record = valid_record()
            record["recipes"]["A"]["arms"][A7]["metrics"][field] = bad
            self.result(record, "HALTED")

    def test_v4_before_candidates_required(self):
        record = valid_record()
        record["instrument"]["baseline_before_candidates"] = False
        self.result(record, "HALTED", advance=False)

    def test_v5_candidate_controls_67_68_each_arm(self):
        for arm_name in ARMS[:2]:
            for value in (67, 68):
                with self.subTest(arm=arm_name, value=value):
                    record = valid_record(2)
                    set_counts(self.candidate(record, arm_name), para_full=value)
                    self.result(record, "PARTIAL" if value == 68 else "INVALID")

    def test_v6_overrides_are_exact_sets_not_counts(self):
        for failure in ("missing", "undeclared", "wrong_same_count", "not_run_consumed", "check_not_separate"):
            with self.subTest(failure=failure):
                record = valid_record()
                entry = next(x for x in record["ledger"] if x["recipe"] == "B-e2e" and x["arm"] == A7 and x["check"] == "write")
                if failure == "missing":
                    entry["consumed_overrides"] = entry["consumed_overrides"][:-1]
                elif failure == "undeclared":
                    entry["consumed_overrides"] = entry["consumed_overrides"] + [{"subject": "foreign", "target": " value"}]
                elif failure == "wrong_same_count":
                    entry["consumed_overrides"] = copy.deepcopy(entry["consumed_overrides"])
                    entry["consumed_overrides"][0]["target"] = " wrong"
                elif failure == "not_run_consumed":
                    entry = next(x for x in record["ledger"] if x["status"] == "NOT-RUN")
                    entry["consumed_overrides"] = [{"subject": "foreign", "target": " value"}]
                else:
                    record["ledger"] = [x for x in record["ledger"] if not (x["recipe"] == "B-e2e" and x["check"] == "executed_loop")]
                self.result(record, "INVALID", advance=False)

    def test_v7_planned_actual_each_layer_boundary_and_zero(self):
        for field in ("planned_null_share", "actual_null_share"):
            for layer_index in range(5):
                for value in (0.999, 0.9989999):
                    with self.subTest(field=field, layer=layer_index, value=value):
                        record = valid_record()
                        self.candidate(record)["geometry"][layer_index][field] = value
                        self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
        record = valid_record()
        self.candidate(record)["geometry"][0] = geometry([0, 1, 1, 1, 1])[0]
        self.result(record, "SCREEN-PASS")

    def test_v7_untouched_reference_miss_halts_precision_diagnosis(self):
        record = valid_record()
        record["recipes"]["A"]["arms"][A7]["geometry"][0]["actual_null_share"] = 0.9989999
        self.result(record, "HALTED", advance=False)

    def test_v7_initial_projector_raw_share_cannot_hide_behind_passed(self):
        # P:133,192. Both init and final planned/actual updates are screened.
        for field in ("init_planned_share_by_layer", "init_actual_share_by_layer"):
            for share in (0.999, 0.9989999):
                record = valid_record()
                self.candidate(record)["checks"]["projector"][field]["8"] = share
                self.result(record, "SCREEN-PASS" if share == 0.999 else "INVALID")

    def test_v8_string_full_equality_and_one_below_every_arm(self):
        for arm_name in ARMS:
            record = valid_record(2)
            m = self.candidate(record, arm_name)["metrics"]
            m["para_string_n"] = m["para_full_n"]
            self.result(record, "PARTIAL")
            m["para_string_n"] -= 1
            self.result(record, "INVALID", advance=False)

    def test_v9_init_final_tokens_and_each_loss_component(self):
        for recipe in ("B-e2e", "B-z"):
            for state in ("init", "final"):
                for failure in ("ids_equal", "full_hits_equal"):
                    record = valid_record(2)
                    record["recipes"][recipe]["arms"][A7]["train_deploy"][state][failure] = False
                    self.result(record, "INVALID-TRAIN-DEPLOY-GAP", recipe=recipe, advance=False)
                for component in (("total", "L_z") if recipe == "B-z" else ("total", "L_edit", "KL_raw", "weighted_KL")):
                    for difference in (0.0001, 0.00010001):
                        record = valid_record(2)
                        record["recipes"][recipe]["arms"][A7]["train_deploy"][state]["losses"][component] = [difference, 0.0]
                        self.result(record, ("PARTIAL" if recipe == "B-e2e" else "NULL") if difference == 0.0001 else "INVALID-TRAIN-DEPLOY-GAP", recipe=recipe)

    def test_v10_overflow_retries_five_six(self):
        for retries in (5, 6):
            record = valid_record()
            self.candidate(record)["trace"]["overflow_retries"] = retries
            self.result(record, "SCREEN-PASS" if retries == 5 else "INVALID")

    def test_v11_hin_hashes_and_write_trace_required(self):
        for missing in ("H_in", "source_hash", "artifact_hash", "stop_reason", "accepted_steps", "overflow_retries", "H_out"):
            with self.subTest(missing=missing):
                record = valid_record()
                if missing == "H_in":
                    del record["manifest"]["H_in"]
                elif missing == "source_hash":
                    del record["manifest"]["sources_start"]["compute_z"]
                elif missing == "artifact_hash":
                    del record["manifest"]["artifacts"]["targets_s1.pt"]
                elif missing == "H_out":
                    del self.candidate(record)["H_out"]
                else:
                    del self.candidate(record)["trace"][missing]
                self.result(record, "INVALID", advance=False)

    def test_v12_leakage_named_halt(self):
        record = valid_record()
        record["overlap_audit"].update(clean=False, matches=[{"template": "heldout", "kind": "containment"}])
        self.result(record, "INVALID-LEAKAGE", advance=False)

    def test_v13_typed_nulls_and_reasons(self):
        record = valid_record(2)
        self.result(record, "PARTIAL")  # A1 has zero continuation denominator.
        for value, denominator, reason, expected in ((None, 0, "zero-continuation-tokens", "PARTIAL"), (None, 1, "zero-continuation-tokens", "INVALID"), (0.0, 0, None, "INVALID"), (None, 0, None, "INVALID")):
            modified = copy.deepcopy(record)
            m = self.candidate(modified, ARMS[0])["metrics"]
            m.update(tf_pertok_cont=value, tf_pertok_cont_denominator=denominator, tf_pertok_cont_undefined_reason=reason)
            self.result(modified, expected)
        for value, first, reason, expected in ((None, 0, "zero-first-token-hits", "NULL"), (None, 1, "zero-first-token-hits", "INVALID"), (0.0, 0, None, "INVALID"), (None, 0, None, "INVALID"), (0.0, 1, None, "NULL")):
            modified = copy.deepcopy(record)
            set_counts(self.candidate(modified), para_full=0, para_first=first)
            m = self.candidate(modified)["metrics"]
            m.update(cond_full_given_first=value, para_first_n=first, cond_full_given_first_denominator=first, cond_full_given_first_undefined_reason=reason)
            self.result(modified, expected)

    def test_v13_nonfinite_unjustified_null_and_typed_integer(self):
        for value in (None, float("nan"), float("inf"), float("-inf"), "23", True):
            record = valid_record(2)
            self.candidate(record)["metrics"]["para_full_n"] = value
            self.result(record, "INVALID", advance=False)

    def test_v13_every_applicable_numeric_family_nonfinite(self):
        # P:198; B:113. Null exceptions do not extend to gates or durations.
        for family in ("raw_described", "raw_ppl", "actual_norm", "planned_norm", "null_share", "fit_probability", "compile_time", "capture_distance"):
            for value in (None, float("nan"), float("inf"), float("-inf")):
                with self.subTest(family=family, value=value):
                    record = valid_record(2)
                    arm = self.candidate(record)
                    if family == "raw_described":
                        arm["locality"]["described_as_raw"] = value
                    elif family == "raw_ppl":
                        arm["locality"]["generic_ppl_raw"] = value
                    elif family in ("actual_norm", "planned_norm"):
                        arm["geometry"][0][family] = value
                    elif family == "null_share":
                        arm["geometry"][0]["actual_null_share"] = value
                    elif family == "fit_probability":
                        arm["fit"]["f_ij"][0][0] = value
                    elif family == "compile_time":
                        arm["compile_s"] = value
                    else:
                        arm["checks"]["capture"]["distance_by_layer"]["4"] = value
                    self.result(record, "INVALID", advance=False)


class ReaderFitAndScreenTests(ReaderCase):
    # P:200–218; B:114–115,120. First match and merged per-arm fit.
    def test_fit_e2e_minimum_canonical_and_every_stop(self):
        for stop in ("threshold", "cap"):
            for minimum, canon, expected in ((0.90, 20, "SCREEN-PASS"), (0.8999999, 20, "SCREEN-UNDERFIT"), (0.90, 19, "SCREEN-UNDERFIT")):
                record = valid_record()
                arm = self.candidate(record)
                arm["fit"]["f_ij"][23][5] = minimum
                arm["trace"]["stop_reason"] = stop
                set_counts(arm, canon=canon)
                self.result(record, expected)

    def test_fit_per_required_arm_and_apply_stored(self):
        for arm_name in ARMS:
            record = valid_record(2)
            self.candidate(record, arm_name)["fit"]["f_ij"][0][0] = 0.8999999
            self.result(record, "UNDERFIT", advance=False)
        for control in ("B-e2e-NM", "B-e2e-ENV"):
            record = add_controls(valid_record(2))
            record["recipes"][control]["arms"][ARMS[0]]["fit"]["f_ij"][0][0] = 0.8999999
            self.result(record, "UNDERFIT", recipe=control, advance=False)

    def test_fit_requires_full_merged_matrix(self):
        # P:198,200. A partial or hooked matrix is not a merged fit measurement.
        for failure in ("missing_row", "missing_column", "not_merged"):
            record = valid_record()
            fit = self.candidate(record)["fit"]
            if failure == "missing_row":
                fit["f_ij"].pop()
            elif failure == "missing_column":
                fit["f_ij"][0].pop()
            else:
                fit["merged"] = False
            self.result(record, "INVALID", advance=False)

    def test_fit_z_mean_and_maximum_boundaries(self):
        for mean, maximum, expected in ((0.001, 0.05, "NULL"), (0.001000001, 0.05, "UNDERFIT"), (0.001, 0.0500001, "UNDERFIT")):
            record = valid_record(2)
            arm = record["recipes"]["B-z"]["arms"][A7]
            arm["fit"]["L_z"] = mean
            arm["fit"]["r_ij"][23][5] = maximum
            arm["trace"]["stop_reason"] = "threshold"
            self.result(record, expected, recipe="B-z")

    def test_fit_z_zero_denominator_named_rule(self):
        record = valid_record(2)
        arm = record["recipes"]["B-z"]["arms"][A7]
        arm["fit"]["delta_norms"][0] = 0.0
        arm["fit"]["residual_norms"][0] = [0.0] * 6
        arm["fit"]["r_ij"][0] = [0.0] * 6
        self.result(record, "NULL", recipe="B-z")
        arm["fit"]["residual_norms"][0][0] = 0.0000001
        self.result(record, "INVALID-ANCHOR-NORMALISATION", recipe="B-z", advance=False)

    def test_s1_named_halts_without_screen_label(self):
        for code in ("fingerprint", "LAW3", "restoration", "HALTED-RESOURCE", "memory-guard", "source-drift", "float64-on-mps"):
            record = valid_record()
            record["run"].update(status="HALTED", code=code)
            self.result(record, "HALTED", advance=False)

    def test_s2_s3_budget_write_boundary(self):
        for launched, write_complete, readout_complete, status in ((False, False, False, "HALTED-BUDGET"), (True, False, False, "HALTED-BUDGET"), (True, True, False, "INCOMPLETE-BUDGET")):
            for cause in ("pre-start", "projection", "supervisor"):
                record = valid_record()
                record["run"].update(status=status, code=cause, launched=launched, write_complete=write_complete, readout_complete=readout_complete)
                self.result(record, status, advance=False)

    def test_stage1_recorded_projection_exactly_120_minutes_fits(self):
        # P:94,291; B:120. The driver gate independently tests dispatch.
        record = valid_record()
        record["run"].update(projected_s=7200.0, cap_s=7200.0)
        self.result(record, "SCREEN-PASS")
        record["run"].update(status="HALTED-BUDGET", launched=False, write_complete=False, readout_complete=False, projected_s=7200.001)
        self.result(record, "HALTED-BUDGET", advance=False)

    def test_s4_fit_precedes_high_count_locality_and_size(self):
        record = valid_record()
        arm = self.candidate(record)
        set_counts(arm, para_full=33)
        arm["fit"]["f_ij"][0][0] = 0.85
        arm["geometry"] = geometry([2.0] * 5)
        arm["locality"]["L1_flips"] = 2
        self.result(record, "SCREEN-UNDERFIT", advance=False)

    def test_s5_s7_envelope_and_gain_boundaries(self):
        for baseline, candidate, label in ((5, 18, "SCREEN-NULL"), (5, 19, "SCREEN-PASS"), (12, 21, "SCREEN-NULL"), (12, 22, "SCREEN-PASS"), (18, 27, "SCREEN-NULL"), (18, 28, "SCREEN-PASS")):
            record = valid_record()
            set_counts(record["recipes"]["A"]["arms"][A7], para_full=baseline)
            set_counts(self.candidate(record), para_full=candidate)
            self.result(record, label)

    def test_s6_size_boundary_and_null_first_match(self):
        for ratio in (1.5, 1.5000001):
            record = valid_record()
            self.candidate(record)["geometry"] = geometry([ratio] * 5)
            self.result(record, "SCREEN-PASS" if ratio == 1.5 else "SCREEN-NOT-ADVANCED")
        record = valid_record()
        set_counts(self.candidate(record), para_full=21)
        self.candidate(record)["locality"]["L1_flips"] = 2
        self.result(record, "SCREEN-NULL")


class ReaderProcessLocalityTests(ReaderCase):
    # P:220–232,250–252; B:116,118. Every locality axis is independent.
    def test_p1_p2_p3(self):
        record = valid_record(2)
        del record["recipes"]["B-e2e"]["arms"][ARMS[0]]
        self.result(record, "INCOMPLETE")
        record = valid_record(2)
        self.candidate(record)["metrics"]["para_string_n"] = 0
        self.result(record, "INVALID")
        record = valid_record(2)
        self.candidate(record)["fit"]["f_ij"][0][0] = 0.89
        self.result(record, "UNDERFIT")

    def test_p4_p5_p7_count_and_gain_boundaries(self):
        for a, n, label in ((5, 18, "NULL"), (5, 19, "PARTIAL"), (12, 21, "NULL"), (12, 22, "PARTIAL"), (12, 29, "PARTIAL"), (12, 30, "LEAD"), (18, 27, "NULL"), (18, 28, "PARTIAL")):
            record = valid_record(2)
            set_counts(record["recipes"]["A"]["arms"][A7], para_full=a)
            set_counts(self.candidate(record), para_full=n)
            self.result(record, label)

    def test_g1_g2_each_frame_both_sides(self):
        for axis in ("L1",) + FRAMES:
            for excess in (1, 2):
                with self.subTest(axis=axis, excess=excess):
                    record = valid_record(2)
                    locality = self.candidate(record)["locality"]
                    if axis == "L1":
                        locality["L1_flips"] = excess
                    else:
                        locality["frame_flips"][axis] = excess
                    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
                    record["stage"] = record["run"]["stage"] = 1
                    bind_fixture_overlays(record)
                    self.result(record, "SCREEN-PASS" if excess == 1 else "SCREEN-NOT-ADVANCED")

    def test_g3_g4_g5_unrounded_boundaries(self):
        for field, value, label in (("described_as_raw", 97.0, "PARTIAL"), ("described_as_raw", 96.99, "TRADEOFF"), ("L3_agreement", 29, "PARTIAL"), ("L3_agreement", 28, "TRADEOFF"), ("generic_ppl_raw", 10.5, "PARTIAL"), ("generic_ppl_raw", 10.51, "TRADEOFF")):
            record = valid_record(2)
            self.candidate(record)["locality"][field] = value
            self.result(record, label)
            record["stage"] = record["run"]["stage"] = 1
            bind_fixture_overlays(record)
            self.result(record, "SCREEN-PASS" if label == "PARTIAL" else "SCREEN-NOT-ADVANCED")

    def test_g3_g5_display_rounding_cannot_substitute(self):
        for raw, display, failing in (("described_as_raw", "described_as", 96.999), ("generic_ppl_raw", "generic_ppl", 10.5001)):
            record = valid_record(2)
            locality = self.candidate(record)["locality"]
            locality[raw] = failing
            locality[display] = 97.0 if raw == "described_as_raw" else 10.5
            self.result(record, "TRADEOFF")
            del locality[raw]
            self.result(record, "INVALID", advance=False)

    def test_g6_relation_flips_report_only(self):
        record = valid_record(2)
        self.candidate(record)["locality"]["relation_label_flips"] = {"associated_with": 24, "is_a": 24}
        self.result(record, "PARTIAL")

    def test_p6_tradeoff_and_p7_null_first_match(self):
        for n in (23, 33, 21, 18):
            record = valid_record(2)
            set_counts(self.candidate(record), para_full=n)
            self.candidate(record)["locality"]["L1_flips"] = 2
            self.result(record, "TRADEOFF" if n >= 22 else "NULL")

    def test_w1_actual_size_boundary_qualifier_preserves_base(self):
        for ratio in (1.5, 1.5000001):
            record = add_controls(valid_record(2), candidate_norms=[ratio] * 5)
            set_counts(self.candidate(record), para_full=33)
            self.result(record, "LEAD", include=() if ratio == 1.5 else ("LARGE-WRITE",), exclude=("LARGE-WRITE",) if ratio == 1.5 else (), advance=None if ratio == 1.5 else False)
        record = valid_record(2)
        for layer in self.candidate(record)["geometry"]:
            layer["planned_norm"] = 2.0
        self.result(record, "PARTIAL", exclude=("LARGE-WRITE",))

    def test_w2_ttl_warning_equality_nonblocking(self):
        for seconds in (3599.999, 3600.0):
            record = valid_record(2)
            self.candidate(record)["compile_s"] = seconds
            self.result(record, "PARTIAL", include=("EXCEEDS-TTL",) if seconds == 3600.0 else (), exclude=() if seconds == 3600.0 else ("EXCEEDS-TTL",))
            p2 = copy.deepcopy(record)
            p2["stage"] = p2["run"]["stage"] = 3
            bind_fixture_overlays(p2)
            self.pair(record, p2, "PARTIAL", include=("EXCEEDS-TTL",) if seconds == 3600.0 else (), advance=True)


class ReaderAttributionTests(ReaderCase):
    # P:80–81,99–103,254–259; B:119. Size instrumentation and attribution.
    def test_no_downscale_controls_required_at_actual_ratio_one(self):
        record = valid_record(2)
        self.result(record, "PARTIAL", exclude=("SIZE-UNTESTED", "SIZE-NOT-EXCLUDED"))
        self.candidate(record)["geometry"] = geometry([0.99] * 5)
        self.result(record, "PARTIAL", exclude=("SIZE-UNTESTED", "SIZE-NOT-EXCLUDED"))

    def test_zero_reference_size_normalisation_conservative_provisional(self):
        # PROVISIONAL: P:81,198,252 leave W1's zero-A denominator unstated.
        # Parent selected a conservative refusal; never represent it as infinity.
        record = valid_record(2)
        for arm_name in ARMS:
            record["recipes"]["A"]["arms"][arm_name]["geometry"] = geometry([0.0] * 5)
        self.result(record, "INVALID-SIZE-NORMALISATION", advance=False)

    def test_total_and_per_layer_growth_trigger_independent_controls(self):
        record = add_controls(valid_record(2))
        del record["recipes"]["B-e2e-NM"]
        self.result(record, "PARTIAL", include=("SIZE-UNTESTED",), advance=False)
        record = add_controls(valid_record(2), candidate_norms=[2.0, 0.5, 0.5, 1.0, 1.0])
        del record["recipes"]["B-e2e-NM"]  # N_B == N_A: NM not required.
        self.result(record, "PARTIAL", exclude=("SIZE-UNTESTED",))
        del record["recipes"]["B-e2e-ENV"]
        self.result(record, "PARTIAL", include=("SIZE-UNTESTED",), advance=False)

    def test_size_control_matching_and_direction_boundaries(self):
        for failure, boundary, outside in (("NM-total", 0.01, 0.010001), ("ENV-layer", 1.01, 1.010001), ("direction", 0.999, 0.9989999)):
            for value in (boundary, outside):
                record = add_controls(valid_record(2))
                if failure == "NM-total":
                    # Integer total 100 makes the 1% equality exact in binary
                    # arithmetic: abs(101-100)/100 == the literal 0.01.
                    for arm_name in ARMS:
                        record["recipes"]["A"]["arms"][arm_name]["geometry"] = geometry([20.0] * 5)
                        record["recipes"]["B-e2e"]["arms"][arm_name]["geometry"] = geometry([40.0, 20.0, 20.0, 20.0, 20.0])
                        nm = record["recipes"]["B-e2e-NM"]["arms"][arm_name]
                        nm["stored_control"]["scale"] = 100.0 / 120.0
                        nm["geometry"] = geometry([34.0 if value == boundary else 34.0001, 16.75, 16.75, 16.75, 16.75])
                        record["recipes"]["B-e2e-ENV"]["arms"][arm_name]["geometry"] = geometry([20.0, 10.0, 10.0, 10.0, 10.0])
                elif failure == "ENV-layer":
                    record["recipes"]["B-e2e-ENV"]["arms"][A7]["geometry"][0]["actual_norm"] = value
                else:
                    record["recipes"]["B-e2e-NM"]["arms"][A7]["geometry"][0]["cosine_to_candidate"] = value
                self.result(record, "PARTIAL", include=() if value == boundary else ("SIZE-UNTESTED",), exclude=("SIZE-UNTESTED",) if value == boundary else ())

    def test_control_positive_requires_envelope_gain_fit_locality_and_validity(self):
        for failure in ("count", "envelope", "fit", "locality", "invalid"):
            record = add_controls(valid_record(2))
            control = record["recipes"]["B-e2e-NM"]["arms"][A7]
            if failure == "count":
                set_counts(control, para_full=21)
            elif failure == "envelope":
                set_counts(record["recipes"]["A"]["arms"][A7], para_full=5)
                set_counts(control, para_full=18)
            elif failure == "fit":
                control["fit"]["f_ij"][0][0] = 0.89
            elif failure == "locality":
                control["locality"]["L1_flips"] = 2
            else:
                control["metrics"]["para_string_n"] = 0
            self.result(record, "PARTIAL", include=("SIZE-UNTESTED" if failure == "invalid" else "SIZE-NOT-EXCLUDED",), advance=False)

    def test_neff_minimum_and_anchor_gap_nine_ten(self):
        for effective, expected in ((22, ("ANCHOR-NOT-EXCLUDED",)), (23, ())):
            record = add_controls(valid_record(2), nm_count=26, env_count=effective)
            set_counts(self.candidate(record), para_full=33)
            result = self.result(record, "LEAD", include=expected, exclude=("ANCHOR-NOT-EXCLUDED",) if effective == 23 else ())
            self.assertEqual(result.get("n_eff"), effective)

    def test_anchor_missing_invalid_and_unfit_untested(self):
        for failure in ("missing", "invalid", "unfit"):
            record = valid_record(2)
            if failure == "missing":
                del record["recipes"]["B-z"]
            elif failure == "invalid":
                record["recipes"]["B-z"]["arms"][A7]["metrics"]["para_string_n"] = 0
            else:
                record["recipes"]["B-z"]["arms"][A7]["fit"]["L_z"] = 0.01
            self.result(record, "PARTIAL", include=("ANCHOR-UNTESTED",), advance=False)

    def test_anchor_comparison_does_not_require_bz_sized_gain(self):
        for n in (22, 23):
            record = valid_record(2)
            set_counts(self.candidate(record), para_full=n)
            self.result(record, "PARTIAL", include=("ANCHOR-NOT-EXCLUDED",) if n == 22 else (), exclude=() if n == 22 else ("ANCHOR-NOT-EXCLUDED",))

    def test_anchor_sham_descriptor_windows_not_fit_or_validity(self):
        for ratio, gain, inert in ((0.8, 5, True), (1.25, 5, True), (0.7999999, 5, False), (1.2500001, 5, False), (1.0, 6, False)):
            record = valid_record(2)
            arm = record["recipes"]["B-z"]["arms"][A7]
            set_counts(arm, para_full=12 + gain)
            arm["geometry"] = geometry([ratio] * 5)
            result = self.result(record, "NULL", recipe="B-z")
            self.assertEqual("ANCHOR-SHAM-INERT" in result.get("descriptors", []), inert)
        record = valid_record(2)
        set_counts(record["recipes"]["B-z"]["arms"][A7], para_full=24)
        self.result(record, "PARTIAL", recipe="B-z")

    def test_hy1_credit_requires_both_processes_attributed(self):
        p1 = add_controls(valid_record(2))
        p2 = add_controls(valid_record(3))
        for record in (p1, p2):
            set_counts(self.candidate(record), para_full=33)
        result = self.pair(p1, p2, "LEAD", advance=True)
        self.assertIs(result.get("H_Y1_credited"), True)
        set_counts(p2["recipes"]["B-e2e-ENV"]["arms"][A7], para_full=22)
        result = self.pair(p1, p2, "LEAD", include=("ANCHOR-NOT-EXCLUDED",), advance=False)
        self.assertIs(result.get("H_Y1_credited"), False)


class ReaderCrossProcessTests(ReaderCase):
    # P:234–248; B:117. Fixed-input regeneration, never independent-seed claims.
    def test_x1_not_run_halted_and_incomplete_never_fabricated_null(self):
        p1 = valid_record(2)
        self.pair(p1, None, "PARTIAL", include=("SINGLE-PROCESS",), advance=False)
        for state in ("NOT-RUN", "HALTED", "INCOMPLETE"):
            p2 = valid_record(3)
            p2["run"].update(status=state, code="recorded-stage3-outcome", launched=state != "NOT-RUN", write_complete=state == "INCOMPLETE", readout_complete=False)
            p2["recipes"] = {}
            result = self.pair(p1, p2, "PARTIAL", include=("SINGLE-PROCESS",), advance=False)
            self.assertEqual(result.get("process2_status"), state)

    def test_x2_identical_labels_and_union_qualifiers(self):
        p1, p2 = valid_record(2), valid_record(3)
        self.pair(p1, p2, "PARTIAL", advance=True)
        p2["recipes"]["B-z"]["arms"][A7]["fit"]["L_z"] = 0.01
        self.pair(p1, p2, "PARTIAL", include=("ANCHOR-UNTESTED",), advance=False)

    def test_x3_mixed_labels_store_actual_counts(self):
        p1, p2 = valid_record(2), valid_record(3)
        set_counts(self.candidate(p1), para_full=30)
        set_counts(self.candidate(p2), para_full=29)
        result = self.pair(p1, p2, "MIXED-NOT-REPLICATED", exclude=("NOT-REPRODUCIBLE",), advance=False)
        self.assertEqual(result.get("process_labels"), ["LEAD", "PARTIAL"])
        self.assertEqual(result.get("counts"), [30, 29])
        for other in ("TRADEOFF", "UNDERFIT"):
            p2 = valid_record(3)
            if other == "TRADEOFF":
                self.candidate(p2)["locality"]["L1_flips"] = 2
            else:
                self.candidate(p2)["fit"]["f_ij"][0][0] = 0.85
            result = self.pair(p1, p2, "MIXED-NOT-REPLICATED", advance=False)
            self.assertEqual(result.get("process_labels"), ["LEAD", other])

    def test_r1_cosine_and_distance_every_layer_boundaries(self):
        for field, inside, outside in (("cosine", 0.99, 0.9899999), ("distance", 0.10, 0.1000001)):
            for layer_index in range(5):
                for value in (inside, outside):
                    p1, p2 = valid_record(2), valid_record(3)
                    repro = valid_repro(p1, p2)
                    repro["recipes"]["B-e2e"]["arms"][A7]["layers"][layer_index][field] = value
                    self.pair(p1, p2, "PARTIAL", repro, include=() if value == inside else ("NOT-REPRODUCIBLE",), exclude=("NOT-REPRODUCIBLE",) if value == inside else (), advance=value == inside)

    def test_r1_zero_norm_rules_and_baseline_instrument(self):
        for norms, success in (((0.0, 0.0), True), ((0.0, 1.0), False), ((1.0, 0.0), False)):
            p1, p2 = valid_record(2), valid_record(3)
            for record, norm in zip((p1, p2), norms):
                self.candidate(record)["geometry"][0] = geometry([norm, 1, 1, 1, 1])[0]
            repro = valid_repro(p1, p2)
            layer = repro["recipes"]["B-e2e"]["arms"][A7]["layers"][0]
            layer.update(cosine=None, distance=0.0 if success else 1.0)
            self.pair(p1, p2, "PARTIAL", repro, include=() if success else ("NOT-REPRODUCIBLE",), exclude=("NOT-REPRODUCIBLE",) if success else ())
        for field, value in (("cosine", 0.9899999), ("distance", 0.1000001)):
            p1, p2 = valid_record(2), valid_record(3)
            repro = valid_repro(p1, p2)
            repro["baseline"]["arms"][A7]["layers"][0][field] = value
            result = self.pair(p1, p2, "PARTIAL", repro, include=("NOT-REPRODUCIBLE",), advance=False)
            self.assertEqual(result.get("reproducibility_status"), "INVALID")

    def test_r1_required_controls_and_all_arms_independent(self):
        for recipe, arm_name in (("B-e2e", ARMS[0]), ("B-e2e", ARMS[1]), ("B-e2e-NM", A7), ("B-e2e-ENV", A7), ("B-z", A7)):
            p1, p2 = add_controls(valid_record(2)), add_controls(valid_record(3))
            repro = valid_repro(p1, p2)
            repro["recipes"][recipe]["arms"][arm_name]["layers"][0]["cosine"] = 0.9899999
            self.pair(p1, p2, "PARTIAL", repro, include=("NOT-REPRODUCIBLE",), advance=False)

    def test_r2_count_spread_five_six(self):
        for spread in (5, 6):
            p1, p2 = valid_record(2), valid_record(3)
            set_counts(self.candidate(p2), para_full=23 + spread)
            # Let baseline disagreement absorb the induced R3 difference.
            set_counts(p2["recipes"]["A"]["arms"][A7], shift=3)
            self.pair(p1, p2, "PARTIAL", include=() if spread == 5 else ("NOT-REPRODUCIBLE",), exclude=("NOT-REPRODUCIBLE",) if spread == 5 else ())

    def test_r3_keyed_boolean_disagreement_da_plus_three_four(self):
        p1, p2 = valid_record(2), valid_record(3)
        set_counts(p2["recipes"]["A"]["arms"][A7], shift=1)  # d_A = 2.
        set_counts(self.candidate(p2), para_full=24, shift=2)  # d_B = 5.
        self.candidate(p2)["detail"].reverse()  # Row order is not the comparison key.
        self.pair(p1, p2, "PARTIAL", exclude=("NOT-REPRODUCIBLE",))
        set_counts(self.candidate(p2), para_full=23, shift=3)  # d_B = 6.
        self.pair(p1, p2, "PARTIAL", include=("NOT-REPRODUCIBLE",), advance=False)

    def test_r3_incorrect_strings_do_not_count_as_disagreement(self):
        p1, p2 = valid_record(2), valid_record(3)
        for i, row in enumerate(self.candidate(p2)["detail"]):
            row["generated_text"] = "different incorrect text %d" % i
        self.pair(p1, p2, "PARTIAL", exclude=("NOT-REPRODUCIBLE",))

    def test_cross_shared_hin_and_telemetry_pair_identity(self):
        for failure in ("H_in", "telemetry"):
            p1, p2 = valid_record(2), valid_record(3)
            if failure == "H_in":
                p2["manifest"]["H_in"] = "2" * 64
            else:
                p2["run"]["telemetry"] = True
                p2["run"]["telemetry_inertness"] = {"path": str(self.root / "inertness.json"), "sha256": SHA}
            self.pair(p1, p2, "PARTIAL", include=("NOT-REPRODUCIBLE",), advance=False)

    def test_regenerated_target_hashes_need_not_match_shared_hin(self):
        # P:87,115–117: targets are process outputs, not H_in identity.
        p1, p2 = valid_record(2), valid_record(3)
        p2["manifest"]["artifacts"]["targets_p2.pt"] = "2" * 64
        bind_fixture_overlays(p2)
        self.assertEqual(p1["manifest"]["H_in"], p2["manifest"]["H_in"])
        self.pair(p1, p2, "PARTIAL", exclude=("NOT-REPRODUCIBLE",))


class ReaderTruthTableTests(ReaderCase):
    # One named parameter case for every P:265–289 authored truth-table row.
    def test_authored_stage1_truth_rows_265_276(self):
        cases = ((265, "baseline", "HALTED"), (266, "forecast130", "HALTED-BUDGET"), (267, "deadline_afterwrite", "INCOMPLETE-BUDGET"), (268, "projection_afterwrite", "INCOMPLETE-BUDGET"), (269, "underfit25", "SCREEN-UNDERFIT"), (270, "count21", "SCREEN-NULL"), (271, "count22", "SCREEN-PASS"), (272, "large31", "SCREEN-NOT-ADVANCED"), (273, "described25", "SCREEN-NOT-ADVANCED"), (274, "frame27", "SCREEN-NOT-ADVANCED"), (275, "baseline18_count27", "SCREEN-NULL"), (275, "baseline18_count28", "SCREEN-PASS"), (276, "baseline5_count19", "SCREEN-PASS"))
        for line, case, label in cases:
            with self.subTest(prereg_line=line, case=case):
                record = valid_record()
                arm = self.candidate(record)
                if case == "baseline":
                    set_counts(record["recipes"]["A"]["arms"][A7], para_full=19)
                elif case == "forecast130":
                    record["run"].update(status=label, launched=False, write_complete=False, readout_complete=False, projected_s=7800)
                elif case in ("deadline_afterwrite", "projection_afterwrite"):
                    record["run"].update(status=label, code=case, readout_complete=False)
                elif case == "underfit25":
                    set_counts(arm, para_full=25)
                    arm["fit"]["f_ij"][0][0] = 0.85
                elif case in ("count21", "count22"):
                    set_counts(arm, para_full=int(case[-2:]))
                    arm["geometry"] = geometry([1.2] * 5)
                elif case == "large31":
                    set_counts(arm, para_full=31)
                    arm["geometry"] = geometry([1.8] * 5)
                elif case == "described25":
                    set_counts(arm, para_full=25)
                    arm["locality"]["described_as_raw"] = 96.0
                elif case == "frame27":
                    set_counts(arm, para_full=27)
                    arm["locality"]["frame_flips"]["frame3"] = 2
                elif case.startswith("baseline18"):
                    set_counts(record["recipes"]["A"]["arms"][A7], para_full=18)
                    set_counts(arm, para_full=int(case[-2:]))
                else:
                    set_counts(record["recipes"]["A"]["arms"][A7], para_full=5)
                    set_counts(arm, para_full=19)
                self.result(record, label)

    def test_authored_full_truth_rows_277_289(self):
        cases = ((277, "controls24", "LEAD", ()), (278, "controls20", "LEAD", ("SIZE-NOT-EXCLUDED",)), (279, "nm17", "PARTIAL", ("SIZE-NOT-EXCLUDED",)), (280, "anchor24", "PARTIAL", ("ANCHOR-NOT-EXCLUDED",)), (281, "anchor_unfit", "PARTIAL", ("ANCHOR-UNTESTED",)), (282, "anchor_gap9", "PARTIAL", ("ANCHOR-NOT-EXCLUDED",)), (283, "anchor_gap10", "PARTIAL", ()), (284, "count18", "NULL", ()), (285, "counts30_22", "MIXED-NOT-REPLICATED", ("NOT-REPRODUCIBLE",)), (286, "baseline5_nm18", "PARTIAL", ("SIZE-NOT-EXCLUDED",)), (287, "lead_tradeoff", "MIXED-NOT-REPLICATED", ()), (287, "lead_underfit", "MIXED-NOT-REPLICATED", ()), (288, "p2_halted", "PARTIAL", ("SINGLE-PROCESS",)), (289, "a1_67", "INVALID", ()), (289, "nonfinite", "INVALID", ()))
        for line, case, label, qualifiers in cases:
            with self.subTest(prereg_line=line, case=case):
                p1, p2 = valid_record(2), valid_record(3)
                for record in (p1, p2):
                    arm = self.candidate(record)
                    if case.startswith("controls"):
                        add_controls(record, nm_count=26, env_count=24 if case == "controls24" else 20)
                        set_counts(arm, para_full=33)
                    elif case == "nm17":
                        add_controls(record, nm_count=17, env_count=17)
                        set_counts(arm, para_full=24 if record["stage"] == 2 else 25)
                    elif case == "anchor24":
                        set_counts(arm, para_full=27)
                        set_counts(record["recipes"]["B-z"]["arms"][A7], para_full=24)
                    elif case == "anchor_unfit":
                        set_counts(arm, para_full=27)
                        record["recipes"]["B-z"]["arms"][A7]["fit"]["L_z"] = 0.01
                    elif case in ("anchor_gap9", "anchor_gap10"):
                        set_counts(arm, para_full=22 if case == "anchor_gap9" else 23)
                    elif case == "count18":
                        set_counts(arm, para_full=18)
                    elif case == "counts30_22":
                        set_counts(arm, para_full=30 if record["stage"] == 2 else 22)
                    elif case == "baseline5_nm18":
                        add_controls(record, nm_count=18, env_count=18)
                        set_counts(record["recipes"]["A"]["arms"][A7], para_full=5)
                        set_counts(arm, para_full=19)
                    elif case.startswith("lead_"):
                        set_counts(arm, para_full=33)
                        if record["stage"] == 3:
                            if case == "lead_tradeoff":
                                arm["locality"]["L1_flips"] = 2
                            else:
                                arm["fit"]["f_ij"][0][0] = 0.85
                    elif case == "p2_halted":
                        if record["stage"] == 3:
                            record["run"].update(status="HALTED", code="recorded-stage3-halt", write_complete=False, readout_complete=False)
                    elif case == "a1_67":
                        set_counts(self.candidate(record, ARMS[0]), para_full=67)
                    else:
                        arm["locality"]["generic_ppl_raw"] = float("inf")
                if case in ("a1_67", "nonfinite"):
                    self.result(p1, label)
                    self.result(p2, label)
                else:
                    self.pair(p1, p2, label, include=qualifiers)


class ReaderLoadTests(ReaderCase):
    # P:179,183,204,430–435,671,679–685; B:40,67. No telemetry read-around.
    def write_fixture(self, record, name="out"):
        out = self.root / name
        out.mkdir()
        own = "screen.json" if record["stage"] == 1 else "pass_p%d.json" % (record["stage"] - 1)
        for filename, content in (("manifest.json", record["manifest"]), ("run.json", record["run"]), ("ledger.json", record["ledger"]), ("overlap_audit.json", record["overlap_audit"]), (own, record)):
            (out / filename).write_text(json.dumps(content, allow_nan=False), encoding="utf-8")
        return out

    def test_load_saved_halt_first_with_missing_science_artifacts(self):
        out = self.root / "halted"
        out.mkdir()
        record = valid_record()
        record["run"].update(status="HALTED-BUDGET", launched=False, write_complete=False, readout_complete=False)
        (out / "run.json").write_text(json.dumps(record["run"]), encoding="utf-8")
        loaded = R.load(out)
        self.result(loaded, "HALTED-BUDGET", advance=False)

    def test_load_does_not_read_telemetry(self):
        record = valid_record()
        record["run"].update(status="HALTED", code="saved-halt")
        out = self.write_fixture(record)
        telemetry = out / "telemetry"
        telemetry.mkdir()
        (telemetry / "telemetry_s1.jsonl").write_text("not JSON; never a science input\n", encoding="utf-8")
        loaded = R.load(out)
        self.result(loaded, "HALTED", advance=False)

    def test_load_later_self_contained_record_uses_own_outcome(self):
        record = valid_record()
        out = self.write_fixture(record)
        p1 = valid_record(2)
        p1["run"].update(status="INCOMPLETE-BUDGET", code="stage2-afterwrite", readout_complete=False)
        (out / "pass_p1.json").write_text(json.dumps(p1), encoding="utf-8")
        loaded = R.load(out)
        self.result(loaded, "INCOMPLETE-BUDGET", advance=False)

    def test_load_strict_json_nonfinite_refused(self):
        out = self.root / "malformed"
        out.mkdir()
        (out / "run.json").write_text('{"stage":1,"status":"COMPLETED","bad":NaN}', encoding="utf-8")
        with self.assertRaises((ValueError, RuntimeError)):
            R.load(out)

    def test_load_calibration_directory_refused_before_read(self):
        # P:790–802,817–841. Calibration timings never become verdict input.
        import builtins
        import io
        from unittest import mock

        out = self.root / "experiments/c10y/runs/c10y_directdw_calib1"
        out.mkdir(parents=True)
        (out / "calibration.json").write_text('{"outcome":"COMPLETE"}', encoding="utf-8")
        reads = []
        original_open, original_io_open = builtins.open, io.open

        def observe(original):
            def wrapper(file, *args, **kwargs):
                if isinstance(file, (str, Path)):
                    path = Path(file).resolve()
                    if path == out or out in path.parents:
                        reads.append(str(path))
                return original(file, *args, **kwargs)
            return wrapper

        with mock.patch.object(builtins, "open", observe(original_open)), mock.patch.object(io, "open", observe(original_io_open)):
            with self.assertRaises((ValueError, RuntimeError)):
                R.load(out)
        self.assertEqual(reads, [])

"""T8 runner and T11 audit contracts; incorporated by the isolated selftest.

Required suite globals: IsolatedCase, A, C, R, make_h, valid_record, torch.
Written before production. No module or harness imports occur in this fragment.
"""
import copy
import hashlib
import json
import os
import sys
from pathlib import Path
from unittest import mock


CHECK_REAL_ROOT = Path("/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a")
CHECK_SOURCES = (
    "code/lab/track_c/c10y_directdw_arms.py",
    "code/lab/track_c/c10y_directdw_read.py",
    "code/lab/track_c/c10y_directdw_telemetry_check.py",
    "code/lab/track_c/c10e_bandknob.py",
    "code/lab/track_c/c10z_astra_benchmark.py",
    "code/configs/hparams/qwen25_3b_memit_hparams.json",
    "code/memit/vendor/memit/compute_z.py",
    "code/memit/vendor/memit/compute_ks.py",
    "code/memit/vendor/rome/repr_tools.py",
    "code/memit/vendor/memit/memit_main.py",
    "experiments/c10y/design/C10Y_DIRECTDW_PREREG.md",
)
CHECK_CANON = "The capital of {} is"
CHECK_PTEST = ["{} has its capital in", "The capital city of {} is", "For {}, the capital is"]


def check_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, allow_nan=False, sort_keys=True) + "\n")


def check_common(kind, tag="s1"):
    return {"kind": kind, "t_utc": "2026-10-08T00:00:00+00:00", "elapsed_s": 0.0,
            "cumulative_s": 0.0, "process": tag, "run_id": "isolated-audit"}


def check_header(tag="s1"):
    return {**check_common("header", tag), "schema": "c10y_directdw_telemetry/v1", "telemetry": True}


class TelemetryCheckContract(IsolatedCase):
    """Catches dispatch, identity, schema and disposition breaks (T8/T11)."""

    def _bind_check_root(self):
        old = C.ROOT
        C.ROOT = self.root
        self.addCleanup(setattr, C, "ROOT", old)
        for rel in CHECK_SOURCES:
            target = self.root / rel
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((CHECK_REAL_ROOT / rel).read_bytes())

    def _check_out(self, name="20261008T000000Z"):
        self._bind_check_root()
        return self.root / "results/c10y_directdw_telemetry_inertness" / name

    def _fingerprint(self):
        # The external read-only fingerprint boundary is injected; its output is retained.
        engine = self.root / "code/memit/vendor/memit/memit_main.py"
        expected = "d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65"
        output = ("engine fingerprint PASS: %s\n" % engine
                  + "  sha256   %s  (expected %s; pod-era 5c0c706a…)\n" % (expected, expected)
                  + "  _cov_cpu 3  (expected 3)\n")
        return {"exit_code": 0, "output": output}

    def _run_check(self, out, h=None):
        return C.run(out, make_h() if h is None else h, fingerprint=self._fingerprint)

    def _audit_fixture(self, stage=1, suffix=""):
        self._bind_check_root()
        rerun = int(hashlib.sha256(suffix.encode()).hexdigest()[:8], 16) + 1
        dirname = "c10y_directdw" if not suffix else "c10y_directdw_s%d_rerun%d" % (stage, rerun)
        out = self.root / "results" / dirname
        tag = {1: "s1", 2: "p1", 3: "p2"}[stage]
        science = valid_record(stage=stage)
        stimuli = {"CANON": CHECK_CANON, "PTEST": CHECK_PTEST,
                   "FICTION": ["subject%02d" % i for i in range(24)],
                   "ARMS": {arm: {"subject%02d" % i: "value%02d" % i for i in range(24)}
                            for arm in ("A1_single", "A2_coherent2", "A7_coined_coined")}}
        science["manifest"]["parts"]["stimuli"] = stimuli
        manifest = science["manifest"]
        parts = manifest["parts"]
        current = {name: hashlib.sha256((self.root / rel).read_bytes()).hexdigest()
                   for name, rel in parts["source_paths"].items()}
        manifest["sources_start"] = current.copy()
        manifest["sources_end"] = current.copy()
        parts["source_sha256"] = current.copy()
        for rel in manifest["artifacts"]:
            artifact = out / rel
            artifact.parent.mkdir(parents=True, exist_ok=True)
            if rel == "context_templates.json":
                check_json(artifact, [["{}"], ["Frame%d. {}" % i for i in range(5)]])
            else:
                artifact.write_bytes(b"isolated non-model artifact hash fixture\n")
            manifest["artifacts"][rel] = hashlib.sha256(artifact.read_bytes()).hexdigest()
        context_sha = manifest["artifacts"]["context_templates.json"]
        manifest["context_templates"]["sha256"] = context_sha
        parts["context_templates_sha256"] = context_sha
        parts["hparams_sha256"] = current["hparams"]
        for name in ("input_hashes_start", "input_hashes_end"):
            manifest[name]["contexts"] = context_sha
            manifest[name]["hparams"] = current["hparams"]
        science["manifest"]["H_in"] = hashlib.sha256(json.dumps(
            science["manifest"]["parts"], allow_nan=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        bind_fixture_overlays(science)
        lines = [check_header(tag)]
        expected = {}
        for recipe, result in science["recipes"].items():
            if result.get("status") == "NOT-RUN":
                continue
            for arm, metrics in result.get("arms", {}).items():
                if metrics.get("status") == "NOT-RUN":
                    continue
                for row in metrics["detail"]:
                    subj, val = row["subj"], row["val"]
                    flags = [(row["canon_full"], row["canon_first"])] + list(zip(
                        row["para_full_hits"], row["para_first_hits"]))
                    for template, (full, first) in zip([CHECK_CANON, *CHECK_PTEST], flags):
                        target = [3, 4]
                        generated = [3, 4] if full else ([3, 9] if first else [8, 9])
                        line = {**check_common("answer", tag), "recipe": recipe, "arm": arm,
                                "phase": "readout", "subj": subj, "val": val,
                                "template": template, "prompt": template.format(subj),
                                "target_ids": target, "generated_ids": generated,
                                "text": "controlled output", "full": full, "first": first}
                        key = (recipe, arm, subj, template)
                        expected[key] = (full, first)
                        lines.append(line)
        science_path = out / {1: "screen.json", 2: "pass_p1.json", 3: "pass_p2.json"}[stage]
        check_json(science_path, science)
        check_json(out / "manifest.json", science["manifest"])
        check_json(out / "run.json", {"telemetry": True, "telemetry_inertness": {"path": "fixture", "sha256": "f" * 64}})
        path = out / "telemetry" / ("telemetry_" + tag + ".jsonl")
        self._write_lines(path, lines)
        return out, path, science, lines, expected, tag

    def _write_lines(self, path, lines):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(x, allow_nan=False, sort_keys=True) + "\n" for x in lines))

    def _audit_result(self, fixture, cause=None, disabled=False):
        out, path, science, lines, expected, tag = fixture
        result = C.audit(out, stage=science["stage"])
        self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
        self.assertIn("causes", result)
        if cause is None:
            self.assertEqual(result["causes"], [])
        else:
            self.assertIn(cause, result["causes"])
        compromised = cause is not None and not disabled
        self.assertIs(result.get("compromised"), compromised)
        self.assertIs(result.get("rerun_required"), compromised)
        self.assertIs(result.get("science_record_stands"), not compromised)
        if compromised:
            self.assertIs(result.get("rerun_telemetry"), False)
        saved = out / "telemetry" / ("audit_" + tag + ".json")
        self.assertTrue(saved.is_file())
        self.assertEqual(json.loads(saved.read_bytes()), result)
        return result

    # Amendment T8: only the named namespace, one directory, no overwrite.
    def test_T8_runner_rejects_relative_output_before_writes(self):
        self._bind_check_root()
        with self.assertRaises(ValueError):
            self._run_check(Path("results/c10y_directdw_telemetry_inertness/relative"))
        self.assertFalse((self.root / "results/c10y_directdw_telemetry_inertness/relative").exists())

    def test_T8_runner_rejects_output_outside_namespace(self):
        self._bind_check_root()
        out = self.root / "results/wrong_namespace/20261008"
        with self.assertRaises(ValueError):
            self._run_check(out)
        self.assertFalse(out.exists())

    def test_T8_runner_rejects_namespace_itself_and_nested_subdirectories(self):
        self._bind_check_root()
        base = self.root / "results/c10y_directdw_telemetry_inertness"
        for out in (base, base / "one/two"):
            with self.subTest(out=str(out)), self.assertRaises(ValueError):
                self._run_check(out)
        self.assertFalse(base.exists())

    def test_T8_runner_rejects_symlink_escape(self):
        self._bind_check_root()
        base = self.root / "results/c10y_directdw_telemetry_inertness"
        base.mkdir(parents=True)
        outside = self.root / "outside"
        outside.mkdir()
        (base / "alias").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            self._run_check(base / "alias")
        self.assertFalse((outside / "inertness.json").exists())

    def test_T8_runner_preserves_existing_record(self):
        out = self._check_out()
        record = out / "inertness.json"
        check_json(record, {"sentinel": "historical evidence"})
        before = record.read_bytes()
        with self.assertRaises(ValueError):
            self._run_check(out)
        self.assertEqual(record.read_bytes(), before)

    def test_T8_runner_preflight_refuses_knob_before_output_creation(self):
        out = self._check_out()
        with mock.patch.dict(os.environ, {"C10_PROJECTOR": "override"}):
            with self.assertRaises(ValueError):
                self._run_check(out)
        self.assertFalse(out.exists())

    def test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe(self):
        out = self._check_out()
        h = make_h()
        def forbidden(*args, **kwargs):
            raise AssertionError("telemetry check dispatched edit, recipe or LAW#5 application")
        h.my_edit = h.run_recipe = h.run_law5 = h.apply_memit_to_model = forbidden
        self.assertEqual(self._run_check(out, h), 0)
        data = json.loads((out / "inertness.json").read_bytes())
        self.assertEqual(data.get("verdict"), "INERT")
        for field in ("control_equal", "telemetry_equal", "generated_equal", "telemetry_complete", "weights_unchanged"):
            self.assertIs(data.get(field), True)
        self.assertEqual(data.get("answer_calls"), len(h.FICTION) * (1 + len(h.PTEST)))
        self.assertEqual(data.get("lens_forwards"), 2 * len(h.FICTION))

    def test_T8_runner_records_complete_current_identity_and_strict_roundtrip(self):
        out = self._check_out()
        self.assertEqual(self._run_check(out), 0)
        raw = (out / "inertness.json").read_bytes()
        def reject_constant(value):
            raise AssertionError("non-finite JSON constant " + value)
        data = json.loads(raw, parse_constant=reject_constant)
        self.assertEqual(data.get("schema"), "c10y_directdw_telemetry_inertness/v1")
        self.assertEqual(data.get("decision_id"), "D-C10r-rulings-11")
        self.assertEqual(data.get("device"), "cpu")
        self.assertEqual(set(data.get("sources", {})), set(CHECK_SOURCES))
        for rel in CHECK_SOURCES:
            self.assertEqual(data["sources"][rel], hashlib.sha256((self.root / rel).read_bytes()).hexdigest())
        self.assertEqual(set(data.get("env", {})), {"python", "machine", "platform", "torch", "transformers", "model_rev"})
        self.assertTrue(all(isinstance(v, str) and v for v in data["env"].values()))
        self.assertEqual(data["env"]["model_rev"], "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
        for field in ("started_at", "finished_at", "scope"):
            self.assertIsInstance(data.get(field), str)
            self.assertTrue(data[field])
        self.assertIn("UNVERIFIED", data["scope"])
        self.assertEqual(json.loads(json.dumps(data, allow_nan=False)), data)
        self.assertFalse(any(p.name.endswith(".tmp") for p in out.iterdir()))

    def test_T8_runner_weight_change_is_invalid_exit_two(self):
        out = self._check_out()
        h = make_h()
        original = A.telemetry_mps_inertness_check
        def alter_after_check(target_out, target_h):
            result = original(target_out, target_h)
            with torch.no_grad():
                target_h.model.model.layers[target_h.hp.layers[0]].mlp.down_proj.weight.add_(0.125)
            return result
        with mock.patch.object(A, "telemetry_mps_inertness_check", side_effect=alter_after_check):
            self.assertEqual(self._run_check(out, h), 2)
        data = json.loads((out / "inertness.json").read_bytes())
        self.assertEqual(data.get("verdict"), "INVALID")
        self.assertIs(data.get("weights_unchanged"), False)

    def test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict(self):
        for index, verdict in enumerate(("NOT-INERT", "NONDETERMINISTIC-BASELINE", "INVALID")):
            with self.subTest(verdict=verdict):
                out = self._check_out("20261008T00000%dZ" % index)
                evidence = {"verdict": verdict, "control_equal": False, "telemetry_equal": False,
                            "generated_equal": False, "telemetry_complete": False,
                            "answer_calls": 96, "lens_forwards": 48, "scope": "MPS loop UNVERIFIED"}
                with mock.patch.object(A, "telemetry_mps_inertness_check", return_value=evidence):
                    self.assertEqual(self._run_check(out), 0)
                data = json.loads((out / "inertness.json").read_bytes())
                self.assertEqual(data.get("verdict"), verdict)
                self.assertIs(data.get("weights_unchanged"), True)

    # Amendment T11: actual persisted flags, including baseline A1/A2.
    def test_T11_audit_complete_answer_keys_pass_and_roundtrip(self):
        fixture = self._audit_fixture()
        result = self._audit_result(fixture)
        expected = fixture[4]
        self.assertEqual(result.get("expected_answers"), len(expected))
        self.assertEqual(result.get("observed_answers"), len(expected))
        self.assertEqual(len(expected), 4 * 24 * (1 + len(CHECK_PTEST)))

    def test_T11_audit_uses_stage_two_and_three_tags_and_record_paths(self):
        for stage in (2, 3):
            with self.subTest(stage=stage):
                fixture = self._audit_fixture(stage, "_stage%d" % stage)
                result = self._audit_result(fixture)
                self.assertEqual(result.get("expected_answers"), len(fixture[4]))

    def test_T11_audit_never_mutates_science_records_or_reader_output(self):
        fixture = self._audit_fixture()
        out, path, science, lines, expected, tag = fixture
        files = [p for p in out.iterdir() if p.is_file()]
        before = {p.name: p.read_bytes() for p in files}
        reader_before = R.classify(copy.deepcopy(science))
        self.assertEqual(reader_before.get("label"), "SCREEN-PASS")
        self._audit_result(fixture)
        self.assertEqual({p.name: p.read_bytes() for p in files}, before)
        self.assertEqual(R.classify(json.loads((out / "screen.json").read_bytes())), reader_before)

    def test_T11_audit_accepts_every_kind_with_only_kind_specific_fields(self):
        fixture = self._audit_fixture()
        out, path, science, lines, expected, tag = fixture
        norms = {str(layer): {"actual": 1.0, "planned": 1.0, "ratio_to_A": 1.0} for layer in range(4, 9)}
        lens = [{"subj": "fixture-country-%02d" % i, "prompt": CHECK_CANON.format("fixture-country-%02d" % i),
                 "top": {str(layer): [[j, "tok-%d" % j, 0.2] for j in range(5)] for layer in range(4, 9)}} for i in range(24)]
        lines[1:1] = [
            {**check_common("phase"), "phase": "stage_start"},
            {**check_common("phase"), "phase": "recipe_start", "recipe": "A", "arms": ["A1_single", "A2_coherent2", "A7_coined_coined"]},
            {**check_common("phase"), "phase": "write_start", "mode": "e2e", "arm": "A7_coined_coined"},
            {**check_common("phase"), "phase": "halt", "code": "HALTED-BUDGET"},
            {**check_common("opt_step"), "step": 1, "components": {"L_edit": 0.25, "KL_raw": 0.1, "KL_weighted": 0.00625, "L": 0.25625},
             "loss_scale": 1024.0, "retries": 0, "planned_norms": {str(layer): 1.0 for layer in range(4, 9)}},
            {**check_common("target_probs"), "probabilities": [{"request": 0, "frame": 0, "position": 0, "p": 0.9}]},
            {**check_common("target_probs"), "f_ij": [[0.9] * 6 for _ in range(24)], "r_ij": [[0.01] * 6 for _ in range(24)]},
            {**check_common("write_norms"), "norms": norms, "recipe": "A", "arm": "A7_coined_coined", "harness_fp32": {str(layer): {"delta_norm": 1.0, "weight_norm_before": 2.0, "relative_delta_norm": .5} for layer in range(4, 9)}},
            {**check_common("logit_lens"), "layers": list(range(4, 9)), "items": lens,
             "where": "pristine", "recipe": "pristine", "arm": "A7_coined_coined"},
        ]
        self._write_lines(path, lines)
        self._audit_result(fixture)

    def test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun(self):
        for field in ("full", "first"):
            with self.subTest(field=field):
                fixture = self._audit_fixture(suffix="_mismatch_" + field)
                fixture[3][1][field] = not fixture[3][1][field]
                self._write_lines(fixture[1], fixture[3])
                self._audit_result(fixture, "MISMATCH")

    def test_T11_audit_duplicate_answer_key_compromises_stage(self):
        fixture = self._audit_fixture()
        fixture[3].append(copy.deepcopy(fixture[3][1]))
        self._write_lines(fixture[1], fixture[3])
        self._audit_result(fixture, "DUPLICATE")

    def test_T11_audit_missing_expected_key_compromises_stage(self):
        fixture = self._audit_fixture()
        fixture[3].pop()
        self._write_lines(fixture[1], fixture[3])
        self._audit_result(fixture, "MISSING")

    def test_T11_audit_missing_file_is_missing_output(self):
        fixture = self._audit_fixture()
        fixture[1].unlink()
        self._audit_result(fixture, "MISSING")

    def test_T11_audit_unknown_key_or_kind_or_field_is_unexpected(self):
        variants = ("recipe", "arm", "subj", "template", "unknown_kind", "unknown_field", "header_field")
        for variant in variants:
            with self.subTest(variant=variant):
                fixture = self._audit_fixture(suffix="_unexpected_" + variant)
                line = fixture[3][1]
                if variant in ("recipe", "arm", "subj", "template"):
                    line[variant] = "outside_scored_population"
                elif variant == "unknown_kind":
                    line["kind"] = "trace_not_preregistered"
                elif variant == "header_field":
                    fixture[3][0]["extra"] = 1
                else:
                    line["extra"] = 1
                self._write_lines(fixture[1], fixture[3])
                self._audit_result(fixture, "UNEXPECTED")

    def test_T11_audit_missing_answer_field_is_malformed(self):
        for field in ("val", "target_ids", "first", "process", "run_id"):
            with self.subTest(field=field):
                fixture = self._audit_fixture(suffix="_absent_" + field)
                del fixture[3][1][field]
                self._write_lines(fixture[1], fixture[3])
                self._audit_result(fixture, "MALFORMED")

    def test_T11_audit_checks_payload_types_for_every_non_answer_kind(self):
        variants = (
            ("phase", {"phase": None}),
            ("opt_step", {"step": True, "components": {"L_z": 0.0}, "loss_scale": 1024.0,
                          "retries": 0, "planned_norms": {"4": 1.0}}),
            ("target_probs", {"probabilities": [{"request": 0, "frame": 0, "position": 0, "p": None}]}),
            ("write_norms", {"norms": {"4": {"actual": "1", "planned": 1.0, "ratio_to_A": 1.0}},
                             "recipe": "A", "arm": "A7_coined_coined"}),
            ("logit_lens", {"layers": [4], "items": None, "where": "pristine", "recipe": "pristine",
                            "arm": "A7_coined_coined"}),
        )
        for kind, payload in variants:
            with self.subTest(kind=kind):
                fixture = self._audit_fixture(suffix="_nonanswer_type_" + kind)
                fixture[3].insert(1, {**check_common(kind), **payload})
                self._write_lines(fixture[1], fixture[3])
                self._audit_result(fixture, "MALFORMED")

    def test_T11_audit_rejects_unknown_field_on_every_known_kind(self):
        variants = (
            ("phase", {"phase": "stage_start"}),
            ("opt_step", {"step": 1, "components": {"L_z": 0.0}, "loss_scale": 1024.0,
                          "retries": 0, "planned_norms": {"4": 1.0}}),
            ("target_probs", {"probabilities": [{"request": 0, "frame": 0, "position": 0, "p": 0.9}]}),
            ("write_norms", {"norms": {"4": {"actual": 1.0, "planned": 1.0, "ratio_to_A": 1.0}},
                             "recipe": "A", "arm": "A7_coined_coined"}),
            ("logit_lens", {"layers": [4], "items": [], "where": "pristine", "recipe": "pristine",
                            "arm": "A7_coined_coined"}),
        )
        for kind, payload in variants:
            with self.subTest(kind=kind):
                fixture = self._audit_fixture(suffix="_nonanswer_extra_" + kind)
                fixture[3].insert(1, {**check_common(kind), **payload, "unregistered": 1})
                self._write_lines(fixture[1], fixture[3])
                self._audit_result(fixture, "UNEXPECTED")

    def test_T11_audit_wrong_types_and_nulls_are_malformed(self):
        mutations = (("full", 1), ("first", "true"), ("subj", None), ("template", None),
                     ("val", None), ("target_ids", [True]), ("generated_ids", [3.0]),
                     ("elapsed_s", "0"), ("cumulative_s", None), ("t_utc", 1), ("run_id", None))
        for index, (field, value) in enumerate(mutations):
            with self.subTest(field=field, value=value):
                fixture = self._audit_fixture(suffix="_types_%d" % index)
                fixture[3][1][field] = value
                self._write_lines(fixture[1], fixture[3])
                self._audit_result(fixture, "MALFORMED")

    def test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields(self):
        for index, text in enumerate(("{bad json}\n", '{"kind":"answer","elapsed_s":NaN}\n',
                                     '{"kind":"answer","elapsed_s":Infinity}\n',
                                     '{"kind":"answer","kind":"phase"}\n')):
            with self.subTest(text=text):
                fixture = self._audit_fixture(suffix="_strict_%d" % index)
                with fixture[1].open("a") as stream:
                    stream.write(text)
                self._audit_result(fixture, "MALFORMED")

    def test_T11_audit_header_must_be_present_initial_and_unique(self):
        for variant in ("absent", "not_first", "repeated", "wrong_schema", "telemetry_not_bool"):
            with self.subTest(variant=variant):
                fixture = self._audit_fixture(suffix="_header_" + variant)
                lines = fixture[3]
                if variant == "absent":
                    lines.pop(0)
                elif variant == "not_first":
                    lines[0], lines[1] = lines[1], lines[0]
                elif variant == "repeated":
                    lines.append(copy.deepcopy(lines[0]))
                elif variant == "wrong_schema":
                    lines[0]["schema"] = "c10y_directdw_telemetry/v0"
                else:
                    lines[0]["telemetry"] = 1
                self._write_lines(fixture[1], lines)
                self._audit_result(fixture, "MALFORMED")

    def test_T11_audit_declared_disabled_missing_output_keeps_science_record(self):
        fixture = self._audit_fixture()
        fixture[3].pop()
        self._write_lines(fixture[1], fixture[3])
        log = fixture[0] / "logs" / "isolated_stage.log"
        log.parent.mkdir()
        log.write_text("C10Y_TELEMETRY_DISABLED OSError: controlled fsync failure\n")
        result = self._audit_result(fixture, "DISABLED", disabled=True)
        self.assertEqual(result.get("expected_answers"), len(fixture[4]))
        self.assertEqual(len(result.get("unaudited_keys", [])), 1)

    def test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line(self):
        fixture = self._audit_fixture()
        fixture[3][1]["full"] = not fixture[3][1]["full"]
        fixture[3].pop()
        self._write_lines(fixture[1], fixture[3])
        log = fixture[0] / "logs" / "isolated_stage.log"
        log.parent.mkdir()
        log.write_text("C10Y_TELEMETRY_DISABLED OSError: controlled failure\n")
        self._audit_result(fixture, "MISMATCH")

    def test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers(self):
        fixture = self._audit_fixture()
        fixture[3].pop(1)
        self._write_lines(fixture[1], fixture[3])
        log = fixture[0] / "logs" / "isolated_stage.log"
        log.parent.mkdir()
        log.write_text("C10Y_TELEMETRY_DISABLED OSError: later failure\n")
        self._audit_result(fixture, "MISSING")

    def test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness(self):
        fixture = self._audit_fixture()
        def forbidden_import(name, *args, **kwargs):
            if any(token in name for token in ("c10y_directdw_arms", "c10e_bandknob", "transformers", "datasets", "torch")):
                raise AssertionError("model-free audit imported " + name)
            return original_import(name, *args, **kwargs)
        import builtins
        original_import = builtins.__import__
        with mock.patch.object(builtins, "__import__", side_effect=forbidden_import):
            self._audit_result(fixture)

    def test_T11_audit_refuses_existing_audit_without_rewriting_evidence(self):
        fixture = self._audit_fixture()
        target = fixture[0] / "telemetry/audit_s1.json"
        check_json(target, {"sentinel": "prior audit"})
        before = target.read_bytes()
        with self.assertRaises(ValueError):
            C.audit(fixture[0], stage=1)
        self.assertEqual(target.read_bytes(), before)

    def test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate(self):
        fixture = self._audit_fixture()
        science = fixture[2]
        before = R.classify(copy.deepcopy(science))
        self.assertEqual(before.get("label"), "SCREEN-PASS")
        fixture[1].write_text("deliberately corrupt telemetry\n")
        check_json(fixture[0] / "telemetry/audit_s1.json", {"verdict": "FAIL", "causes": ["MISMATCH"]})
        self.assertEqual(R.classify(json.loads((fixture[0] / "screen.json").read_bytes())), before)
        for forbidden in ("c10e_bandknob", "transformers", "datasets"):
            self.assertNotIn(forbidden, sys.modules)
"""C2/C3/C5/C6 calibration forecast contract. Inject A and IsolatedCase.

Only test fixtures and assertions live here. These CPU fixtures are not
empirical timings or a physics justification for live dispatch.
"""
import copy
import hashlib
import json
import math
import unittest
from pathlib import Path
from unittest import mock


CAL_ARMS = ("A1_single", "A2_coherent2", "A7_coined_coined")
CAL_A7 = CAL_ARMS[2]
CAL_WORKLOAD_FIELDS = ("requests", "scored_prompts", "micro_batches", "accepted_steps", "retries")
CAL_PROOF_REQUIRED = (
    "original_my_edit", "capture_solve", "zero_step_merge", "zero_step_evaluation",
    "zero_step_init_parity", "executed_loop_step", "executed_loop_merge",
    "executed_loop_evaluation", "projector_property", "gradient_e2e",
    "objective_construction", "accumulation_reference_e2e",
    "accumulation_e2e_6+6", "accumulation_e2e_5+7", "restoration_hooks",
    "smoke_step", "smoke_restore_hash",
)
CAL_PROOF_OPTIONAL = tuple(
    prefix + "_" + suffix
    for prefix in ("zero_step", "executed_loop", "smoke")
    for suffix in ("capture", "restore", "init_parity", "final_parity", "merge")
) + ("smoke_loss_before",)
CAL_PHASE_NAMES = {
    "preflight": ("preflight",),
    "load": ("load",),
    "contexts_targets": ("contexts_overlap", "target_solve"),
    "baseline": ("baseline_projector", "baseline_law5", "baseline_write",
                 "baseline_evaluation", "baseline_recipe_overhead", "law3"),
    "proofs": tuple(dict.fromkeys(CAL_PROOF_REQUIRED + CAL_PROOF_OPTIONAL)),
    "projector_capture": ("baseline_projector", "baseline_law5", "baseline_recipe_overhead", "capture_solve"),
    "optimisation": ("executed_loop_step", "smoke_step"),
    "merge": ("zero_step_merge", "executed_loop_merge"),
    "readout": ("baseline_evaluation", "zero_step_init_parity", "projector_property", "executed_loop_step", "smoke_step"),
    "shutdown": ("shutdown",),
}


def cal_workload(arm=None, **values):
    result = {"arms": [] if arm is None else [arm], **dict.fromkeys(CAL_WORKLOAD_FIELDS, 0)}
    result.update(values)
    return result


def calibration_timing_fixture(identity):
    record = copy.deepcopy(identity)
    timings = []
    def add(name, arm=None, repetition=1, seconds=.01, **workload):
        entry = {"name": name, "seconds": seconds, "repetition": repetition,
                 "workload": cal_workload(arm, **workload),
                 "status": "COMPLETED", "synchronised": True}
        if arm is not None:
            entry["arm"] = arm
        if name in CAL_PHASE_NAMES["proofs"] and arm is not None:
            entry["mode"] = "e2e"
        timings.append(entry)
        return entry
    add("preflight")
    add("load")
    add("contexts_overlap", requests=72)
    for index, arm in enumerate(CAL_ARMS, 1):
        add("target_solve", arm, index, requests=24)
        add("baseline_write", arm, index, requests=24)
        add("baseline_evaluation", arm, index, requests=24, scored_prompts=96)
    for name in ("baseline_projector", "baseline_law5", "baseline_recipe_overhead", "law3"):
        add(name)
    for repetition in (1, 2):
        add("original_my_edit", CAL_A7, repetition, requests=24)
    for name in CAL_PHASE_NAMES["proofs"]:
        if name in ("original_my_edit", "executed_loop_step", "smoke_step"):
            continue
        add(name, None if name == "restoration_hooks" else CAL_A7,
            requests=0 if name == "restoration_hooks" else 24,
            scored_prompts=96 if name.endswith("evaluation") or name.endswith("parity") else 0,
            micro_batches=1 if name == "accumulation_reference_e2e" else 2 if name.startswith("accumulation_") else 0)
    for offset, name in enumerate(("executed_loop_step", "smoke_step")):
        for repetition in (1, 2, 3):
            entry = add(name, CAL_A7, repetition, float(offset * 3 + repetition),
                        requests=24, micro_batches=4, accepted_steps=1, retries=0,
                        padded_lengths=[12, 12, 12, 12])
            entry.update(accepted=True, overflow_retry=False, loss_scale_halvings=0)
    add("shutdown")
    inputs = {key: "1" * 64 for key in ("covariance", "model", "tokenizer", "hparams")}
    record.update(schema="c10y_directdw_calibration/v1", outcome="COMPLETE", timings=timings,
                  T_cal=12, template_token_lengths=[1, 4, 4, 4, 4, 4],
                  input_hashes_start=inputs, input_hashes_end=copy.deepcopy(inputs),
                  artifacts={name: "2" * 64 for name in (
                      "context_templates_calib.json", "overlap_audit_calib.json", "targets_calib.pt",
                      "ledger_calib.json", "law5_calib.json", "step0_calib.json")},
                  memory={"samples": [{"current_bytes": 0, "driver_bytes": 0,
                                        "rss_bytes": 4096, "available_bytes": 2**40}]},
                  started_at="2026-10-08T00:00:00Z", finished_at="2026-10-08T00:01:00Z",
                  contexts=["CALIBRATION_SCIENCE_LEAK"], targets={"CALIBRATION_SCIENCE_LEAK": 1})
    return record


def calibration_selected_rows(record, phase):
    return [copy.deepcopy(row) for row in record["timings"]
            if row["name"] in CAL_PHASE_NAMES[phase]
            and (phase != "readout" or row["name"] != "baseline_evaluation"
                 or row["workload"]["arms"] == [CAL_A7])]


def calibration_bounds_fixture(record, measured=True, total=7200.):
    result = []
    for name in A.FORECAST_PHASES:
        rows = calibration_selected_rows(record, name)
        phase = {"name": name, "measured": measured,
                 "workload": cal_workload(CAL_A7 if name == "optimisation" else None,
                    requests=24 if name == "optimisation" else 0,
                    micro_batches=4 if name == "optimisation" else 0,
                    accepted_steps=100 if name == "optimisation" else 0,
                    retries=5 if name == "optimisation" else 0),
                 "repetitions": len(rows) if measured else 1,
                 "scaling_assumption": "same frozen operations; bound explicitly includes unknown stage-1 padded lengths",
                 "justification": "test-only supported upper estimate, never live dispatch evidence",
                 "upper_s": 1380. if name == "readout" else 650.}
        if measured:
            phase["timing_names"] = list(dict.fromkeys(row["name"] for row in rows))
        result.append(phase)
    result[0]["upper_s"] = total - math.fsum(p["upper_s"] for p in result[1:])
    return result


def independent_forecast_fixture(path, stage=1, total=3000.):
    path = Path(path)
    path.write_text('{"support":"independently recorded fixture estimate"}')
    empty = {"timings": []}
    phases = calibration_bounds_fixture(empty, measured=False, total=total)
    # The 650-s default is useful for measured timings; distribute independent
    # fixture support within the requested total without negative phase bounds.
    other = (total - 1380.) / (len(phases) - 1)
    for phase in phases:
        phase.update(artifact=str(path.resolve()), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                     upper_s=1380. if phase["name"] == "readout" else other)
    return {"stage": stage, "status": "READY", "phases": phases}


def replacement_forecast_cap_test(self):
    artifact = self.root / "timing.json"
    forecast = independent_forecast_fixture(artifact, total=7200.)
    self.assertEqual(A.budget_gate(forecast, 7200.)["status"], "READY")
    forecast["phases"][0]["upper_s"] += .001
    high = A.budget_gate(forecast, 7200.)
    self.assertEqual(high["status"], "HALTED-BUDGET")
    self.assertIs(high["launched"], False)
    forecast["phases"][0].pop("artifact")
    self.assertEqual(A.budget_gate(forecast, 7200.)["status"], "UNVERIFIED")


def replacement_stage_forecast(self, stage=1):
    return independent_forecast_fixture(self.root / "timing.json", stage=stage)


def replacement_calibration_independent_test(self):
    record = calibration_timing_fixture(A.calibration_identity())
    path = self.root / "calibration.json"
    path.write_text(json.dumps(record))
    bounds = calibration_bounds_fixture(record, measured=False)
    forecast = A.calibration_forecast(path, bounds)
    self.assertEqual(forecast.get("status"), "READY")
    self.assertEqual(A.budget_gate(forecast, 7200.)["status"], "READY")
    self.assertTrue(all(p.get("measured") is False and not p.get("measurements") for p in forecast["phases"]))
    text = json.dumps(forecast)
    self.assertNotIn("CALIBRATION_SCIENCE_LEAK", text)
    self.assertNotIn("driver_bytes", text)
    bounds[0]["upper_s"] += .001
    self.assertEqual(A.budget_gate(A.calibration_forecast(path, bounds), 7200.)["status"], "HALTED-BUDGET")


def install_calibration_forecast_replacements(namespace):
    namespace["LaunchTests"].test_forecast_unverified_and_cap = replacement_forecast_cap_test
    namespace["IntegrationTests"].forecast = replacement_stage_forecast
    namespace["CalibrationTests"].test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs = replacement_calibration_independent_test


class CalibrationForecastContractTests(IsolatedCase):
    # P:C2 727-766, C3 768-788, C5 823-832, C6 867-880.
    def setUp(self):
        super().setUp()
        self.record = calibration_timing_fixture(A.calibration_identity())
        self.path = self.root / "calibration.json"
        self.bounds = calibration_bounds_fixture(self.record)
        self.persist()

    def persist(self):
        self.path.write_text(json.dumps(self.record))

    def build(self, bounds=None):
        return A.calibration_forecast(self.path, self.bounds if bounds is None else bounds)

    def phase(self, bounds, name):
        return next(p for p in bounds if p["name"] == name)

    def rows(self, name):
        return [r for r in self.record["timings"] if r["name"] == name]

    def test_full_c3_measured_map_and_every_repetition(self):
        forecast = self.build()
        self.assertEqual(forecast.get("status"), "READY")
        for phase in forecast["phases"]:
            with self.subTest(phase=phase["name"]):
                wanted = calibration_selected_rows(self.record, phase["name"])
                self.assertEqual(phase.get("measurements"), wanted)
                self.assertEqual(phase.get("repetitions"), len(wanted))
        self.assertEqual(len(self.phase(forecast["phases"], "optimisation")["measurements"]), 6)
        readout = self.phase(forecast["phases"], "readout")["measurements"]
        self.assertEqual([r["workload"]["arms"] for r in readout if r["name"] == "baseline_evaluation"], [[CAL_A7]])
        self.assertNotIn("CALIBRATION_SCIENCE_LEAK", json.dumps(forecast))
        self.assertNotIn("driver_bytes", json.dumps(forecast))

    def test_each_phase_rejects_wrong_measured_mapping(self):
        for index, phase in enumerate(self.bounds):
            bounds = copy.deepcopy(self.bounds)
            bounds[index]["timing_names"] = ["smoke_step"] if phase["name"] != "optimisation" else ["baseline_write"]
            with self.subTest(phase=phase["name"]):
                self.assertEqual(self.build(bounds).get("status"), "UNVERIFIED")

    def test_missing_c3_unit_is_not_complete_support(self):
        for name in ("preflight", "load", "contexts_overlap", "target_solve", "baseline_write",
                     "baseline_evaluation", "original_my_edit", "zero_step_init_parity", "gradient_e2e",
                     "accumulation_e2e_5+7", "smoke_restore_hash", "shutdown"):
            original = copy.deepcopy(self.record)
            self.record["timings"] = [r for r in self.record["timings"] if r["name"] != name]
            self.persist()
            with self.subTest(name=name):
                self.assertEqual(self.build().get("status"), "UNVERIFIED")
            self.record = original
        self.persist()

    def test_all_three_targets_and_baseline_arm_timings_required(self):
        for name in ("target_solve", "baseline_write", "baseline_evaluation"):
            for arm in CAL_ARMS:
                original = copy.deepcopy(self.record)
                self.record["timings"] = [r for r in self.record["timings"]
                                          if not (r["name"] == name and r["workload"]["arms"] == [arm])]
                self.persist()
                with self.subTest(name=name, arm=arm):
                    self.assertEqual(self.build().get("status"), "UNVERIFIED")
                self.record = original
        self.persist()

    def test_original_my_edit_requires_two_distinct_repetitions(self):
        for change in ("missing", "duplicate", "boolean"):
            original = copy.deepcopy(self.record)
            rows = self.rows("original_my_edit")
            if change == "missing": self.record["timings"].remove(rows[1])
            else: rows[1]["repetition"] = 1 if change == "duplicate" else True
            self.persist()
            with self.subTest(change=change): self.assertEqual(self.build().get("status"), "UNVERIFIED")
            self.record = original
        self.persist()

    def test_optimisation_requires_three_accepted_rows_in_each_check(self):
        for name in ("executed_loop_step", "smoke_step"):
            original = copy.deepcopy(self.record)
            self.record["timings"].remove(self.rows(name)[-1])
            self.persist()
            with self.subTest(name=name): self.assertEqual(self.build().get("status"), "UNVERIFIED")
            self.record = original
        self.persist()

    def test_optimisation_comparable_shape_and_iteration_flags(self):
        variants = (("requests", 23), ("requests", True), ("micro_batches", 3),
                    ("padded_lengths", []), ("padded_lengths", [12]*3),
                    ("padded_lengths", [13]*4), ("padded_lengths", [True]*4),
                    ("accepted_steps", 0), ("retries", 1))
        for key, value in variants:
            original = copy.deepcopy(self.record)
            self.rows("smoke_step")[-1]["workload"][key] = value
            self.persist()
            with self.subTest(key=key, value=value): self.assertEqual(self.build().get("status"), "UNVERIFIED")
            self.record = original
        for key, value in (("accepted", False), ("accepted", 1), ("overflow_retry", True),
                           ("overflow_retry", 0), ("loss_scale_halvings", -1), ("loss_scale_halvings", True)):
            original = copy.deepcopy(self.record)
            self.rows("smoke_step")[-1][key] = value
            self.persist()
            with self.subTest(key=key, value=value): self.assertEqual(self.build().get("status"), "UNVERIFIED")
            self.record = original
        self.persist()

    def test_optimisation_full_105_attempt_stage_workload(self):
        for key, value in (("accepted_steps", 99), ("accepted_steps", True), ("retries", 4),
                           ("requests", 23), ("micro_batches", 3)):
            bounds = copy.deepcopy(self.bounds)
            self.phase(bounds, "optimisation")["workload"][key] = value
            with self.subTest(key=key, value=value): self.assertEqual(self.build(bounds).get("status"), "UNVERIFIED")

    def test_optimisation_uses_slowest_iteration_not_mean(self):
        bounds = copy.deepcopy(self.bounds)
        self.phase(bounds, "optimisation")["upper_s"] = 630.
        self.assertEqual(self.build(bounds).get("status"), "READY")
        self.phase(bounds, "optimisation")["upper_s"] -= .001
        self.assertEqual(self.build(bounds).get("status"), "UNVERIFIED")

    def test_overflow_attempt_is_cited_in_addition_to_six_accepted_rows(self):
        retry = copy.deepcopy(self.rows("smoke_step")[-1])
        retry.update(repetition=4, seconds=6.1, accepted=False, overflow_retry=True, loss_scale_halvings=1)
        retry["workload"].update(accepted_steps=0, retries=1)
        self.record["timings"].append(retry)
        self.persist()
        bounds = calibration_bounds_fixture(self.record)
        forecast = self.build(bounds)
        self.assertEqual(forecast.get("status"), "READY")
        self.assertEqual(len(self.phase(forecast["phases"], "optimisation")["measurements"]), 7)

    def test_merge_uses_larger_of_two_timed_merges(self):
        self.rows("zero_step_merge")[0]["seconds"] = 4.
        self.rows("executed_loop_merge")[0]["seconds"] = 8.
        self.persist()
        bounds = copy.deepcopy(self.bounds)
        self.phase(bounds, "merge")["upper_s"] = 8.
        self.assertEqual(self.build(bounds).get("status"), "READY")
        self.phase(bounds, "merge")["upper_s"] = 7.999
        self.assertEqual(self.build(bounds).get("status"), "UNVERIFIED")

    def test_readout_1380_reserve_and_larger_measured_bound(self):
        bounds = copy.deepcopy(self.bounds)
        self.phase(bounds, "readout")["upper_s"] = 1379.999
        self.assertEqual(self.build(bounds).get("status"), "UNVERIFIED")
        next(r for r in self.rows("baseline_evaluation") if r["workload"]["arms"] == [CAL_A7])["seconds"] = 600.
        self.rows("zero_step_init_parity")[0]["seconds"] = 500.
        self.rows("projector_property")[0]["seconds"] = 400.
        self.persist()
        bounds = calibration_bounds_fixture(self.record)
        self.phase(bounds, "baseline")["upper_s"] = 1000.
        self.phase(bounds, "proofs")["upper_s"] = 1000.
        self.phase(bounds, "readout")["upper_s"] = 1506.
        self.assertEqual(self.build(bounds).get("status"), "HALTED-BUDGET")
        self.phase(bounds, "readout")["upper_s"] -= .001
        self.assertEqual(self.build(bounds).get("status"), "UNVERIFIED")

    def test_raw_seconds_sync_status_and_workload_are_typed(self):
        variants = (("seconds", -1.), ("seconds", True), ("seconds", "1"),
                    ("seconds", float("nan")), ("seconds", float("inf")),
                    ("synchronised", False), ("synchronised", 1), ("status", "FAILED"),
                    ("repetition", 0), ("repetition", True), ("workload", "untyped workload"))
        for key, value in variants:
            original = copy.deepcopy(self.record)
            self.record["timings"][0][key] = value
            self.persist()
            with self.subTest(key=key, value=value): self.assertEqual(self.build().get("status"), "UNVERIFIED")
            self.record = original
        for key in ("arms",) + CAL_WORKLOAD_FIELDS:
            original = copy.deepcopy(self.record)
            self.record["timings"][0]["workload"].pop(key)
            self.persist()
            with self.subTest(key=key): self.assertEqual(self.build().get("status"), "UNVERIFIED")
            self.record = original
        self.persist()

    def test_calibration_schema_and_c5_completeness(self):
        for key in ("schema", "timings", "memory", "T_cal", "template_token_lengths", "started_at",
                    "finished_at", "input_hashes_start", "input_hashes_end", "artifacts"):
            original = copy.deepcopy(self.record)
            self.record.pop(key)
            self.persist()
            with self.subTest(key=key): self.assertEqual(self.build().get("status"), "UNVERIFIED")
            self.record = original
        self.record["schema"] = "c10y_directdw_calibration/v0"
        self.persist()
        self.assertEqual(self.build().get("status"), "UNVERIFIED")

    def test_input_identity_drift_and_padded_max_are_invalid(self):
        for change in ("inputs", "T_cal", "template_lengths"):
            original = copy.deepcopy(self.record)
            if change == "inputs": self.record["input_hashes_end"]["model"] = "0" * 64
            elif change == "T_cal": self.record["T_cal"] = 13
            else: self.record["template_token_lengths"] = [True]
            self.persist()
            with self.subTest(change=change): self.assertEqual(self.build().get("status"), "UNVERIFIED")
            self.record = original
        self.persist()

    def test_prestart_gate_rechecks_schema_and_staleness(self):
        forecast = self.build()
        self.assertEqual(forecast.get("status"), "READY")
        for key, value in (("schema", "wrong"), ("outcome", "HALTED-BUDGET"), ("device", "cpu")):
            original = copy.deepcopy(self.record)
            self.record[key] = value
            self.persist()
            altered = copy.deepcopy(forecast)
            for phase in altered["phases"]: phase["sha256"] = hashlib.sha256(self.path.read_bytes()).hexdigest()
            with self.subTest(key=key): self.assertEqual(A.budget_gate(altered, 7200.).get("status"), "UNVERIFIED")
            self.record = original
        self.persist()
        current = copy.deepcopy(A.calibration_identity())
        current["sources"]["driver"] = "0" * 64
        with mock.patch.object(A, "calibration_identity", return_value=current):
            self.assertEqual(A.budget_gate(forecast, 7200.).get("status"), "UNVERIFIED")

    def test_prestart_gate_rejects_forged_or_omitted_measurement(self):
        forecast = self.build()
        self.assertEqual(forecast.get("status"), "READY")
        for change in ("omitted", "forged", "rep_count", "mapping"):
            altered = copy.deepcopy(forecast)
            phase = self.phase(altered["phases"], "optimisation")
            if change == "omitted": phase["measurements"].pop()
            elif change == "forged": phase["measurements"][0]["seconds"] = .000001
            elif change == "rep_count": phase["repetitions"] -= 1
            else: phase["timing_names"] = ["smoke_step"]
            with self.subTest(change=change): self.assertEqual(A.budget_gate(altered, 7200.).get("status"), "UNVERIFIED")

    def test_independent_bound_requires_explicit_justification(self):
        bounds = calibration_bounds_fixture(self.record, measured=False)
        self.assertEqual(self.build(bounds).get("status"), "READY")
        for index in range(len(bounds)):
            altered = copy.deepcopy(bounds)
            altered[index].pop("justification")
            with self.subTest(phase=altered[index]["name"]): self.assertEqual(self.build(altered).get("status"), "UNVERIFIED")

    def test_noncalibration_measured_flag_cannot_replace_supported_bound(self):
        forecast = independent_forecast_fixture(self.root / "bound.json", total=7200.)
        self.assertEqual(A.budget_gate(forecast, 7200.).get("status"), "READY")
        forecast["phases"][0]["measured"] = True
        self.assertEqual(A.budget_gate(forecast, 7200.).get("status"), "UNVERIFIED")

    def test_cap_types_stage1_limit_and_later_stage_spend(self):
        forecast = independent_forecast_fixture(self.root / "bound.json", total=7200.)
        for cap in (True, "7200", 0., -1., float("nan"), float("inf"), 7200.001):
            with self.subTest(cap=cap): self.assertEqual(A.budget_gate(forecast, cap).get("status"), "UNVERIFIED")
        for stage in (2, 3):
            forecast["stage"] = stage
            with self.subTest(stage=stage): self.assertEqual(A.budget_gate(forecast, 9000.).get("status"), "READY")

    def test_bad_bound_records_return_unverified(self):
        for value in (True, -1., float("nan"), float("inf"), "1"):
            bounds = copy.deepcopy(self.bounds)
            bounds[0]["upper_s"] = value
            with self.subTest(value=value): self.assertEqual(self.build(bounds).get("status"), "UNVERIFIED")
        for forecast in ({"stage": 1, "phases": None}, {"stage": 1, "phases": [None]},
                         {"stage": 1, "phases": "invalid"}):
            with self.subTest(forecast=forecast): self.assertEqual(A.budget_gate(forecast, 7200.).get("status"), "UNVERIFIED")

class PinnedTemplateTests(IsolatedCase):
    def expected(self):
        tree=ast.parse((self.root/'code/lab/track_c/c10z_astra_benchmark.py').read_text())
        values=ast.literal_eval(next(node.value for node in tree.body if isinstance(node,ast.Assign) and any(isinstance(n,ast.Name) and n.id=='TEMPLATES' for n in node.targets)))
        return [[values[0]],list(values[1:])]
    def sampler_spy(self,H):
        scope={'sampled':[],'calls':[],'expected':self.expected(),'copy':copy}
        exec("def get_context_templates(model,tok):\n    calls.append(1)\n    cached=globals().get('CONTEXT_TEMPLATES_CACHE')\n    if cached!=expected:\n        sampled.append(1)\n        raise AssertionError('template generation attempted')\n    return copy.deepcopy(cached)\n",scope)
        H.get_context_templates=scope['get_context_templates'];return scope
    def test_stage1_and_calibration_pin_before_first_engine_call(self):
        for stage in (1,'calibration'):
            H=make_h();scope=self.sampler_spy(H);out=self.root/('results/c10y_directdw' if stage==1 else 'experiments/c10y/runs/c10y_directdw_calib1')
            name='context_templates.json' if stage==1 else 'context_templates_calib.json'
            calls=[]
            def prefix(H,out,budget,**kwargs):
                # LAW#3's input file must already exist before prefix baseline.
                calls.append((Path(out)/name).is_file())
                values=H.get_context_templates(H.model,H.tok)
                self.assertEqual(values,self.expected())
                raise A.Halt('LAW#3',{'test':'pinned baseline miss'})
            go={'decision_id':'D-go','experiment':'C10Y','stage':stage,'recorded_in':'program/runbook/:5','at':'2026-10-08T00:00:00Z'}
            spend={'decision_id':'D-spend','stage':stage,'cap_s':7200.}
            # Clear only this isolated root's schedule between independent cases.
            (self.root/'results/c10y_directdw_schedule_halt.json').unlink(missing_ok=True)
            diagnostic=self.root/f'architecture_profile/c10y_halt_diagnostic_{stage}.json'
            with mock.patch.object(A,'PREREG_SHA',A.sha(self.root/'experiments/c10y/design/C10Y_DIRECTDW_PREREG.md')),mock.patch.object(A,'instrument_prefix',side_effect=prefix):
                if stage==1: record=A.run(out,H,go=go,forecast=independent_forecast_fixture(self.root/'bound.json'),diagnostic=diagnostic)
                else: record=A.calibrate(out,H,go=go,spend=spend,diagnostic=diagnostic)
            self.assertEqual(calls,[True]);self.assertEqual(scope['sampled'],[]);self.assertEqual(scope['calls'],[1])
            self.assertEqual(A.strict_load(out/name),self.expected())
            wanted=A.sha(out/name);diag=A.strict_load(diagnostic);halt=A.strict_load(self.root/'results/c10y_directdw_schedule_halt.json')
            self.assertEqual(diag.get('context_templates',{}).get('sha256'),wanted)
            self.assertEqual(halt.get('context_templates',{}).get('sha256'),wanted)
    def test_stages2_3_install_stage1_bytes_before_first_engine_use(self):
        source=self.root/'results/c10y_directdw/context_templates.json';A.write_json(source,self.expected())
        for stage in (2,3):
            H=make_h();scope=self.sampler_spy(H)
            result=A.freeze_contexts(H,source,expected=A.sha(source))
            self.assertEqual(H.get_context_templates(H.model,H.tok),self.expected())
            self.assertEqual(scope['sampled'],[]);self.assertEqual(result['sha256'],A.sha(source))
    def test_changed_template_source_or_stage1_content_halts(self):
        helper=getattr(A,'pinned_templates',None);self.assertTrue(callable(helper),'missing P1 digest checks')
        values=helper();self.assertEqual(values,self.expected())
        source=self.root/'code/lab/track_c/c10z_astra_benchmark.py';original=source.read_text()
        source.write_text(original.replace('The following is a single-choice','A changed single-choice',1))
        with self.assertRaises(A.Halt): helper()
        source.write_text(original)
        wrong=self.root/'results/c10y_directdw/context_templates.json';A.write_json(wrong,[['{}'],['wrong {}']])
        H=make_h();scope=self.sampler_spy(H)
        with self.assertRaises(A.Halt): A.freeze_contexts(H,wrong,expected=A.sha(wrong))
        self.assertEqual(scope['sampled'],[]);self.assertEqual(scope['calls'],[])
        for field in ('PINNED_ENGINE_SHA','PINNED_FLAT_SHA'):
            self.assertTrue(hasattr(A,field),'both digest checks required')
            with mock.patch.object(A,field,'0'*64),self.assertRaises(A.Halt): helper()
    def test_t8_installs_pin_and_writes_context_before_any_pass(self):
        H=make_h();scope=self.sampler_spy(H);out=self.root/'results/c10y_directdw_telemetry_inertness/pinned'
        try: value=A.telemetry_mps_inertness_check(out,H)
        except AssertionError as error: self.fail(str(error))
        self.assertEqual(value.get('verdict'),'INERT');self.assertEqual(scope['sampled'],[])
        self.assertEqual(A.strict_load(out/'context_templates.json'),self.expected())
        self.assertEqual(value.get('context_templates',{}).get('sha256'),A.sha(out/'context_templates.json'))
    def test_t8_digest_failure_has_halt_diagnostic_before_scoring(self):
        H=make_h();source=self.root/'code/lab/track_c/c10z_astra_benchmark.py'
        source.write_text(source.read_text().replace('The following is a single-choice','Changed pin',1))
        out=self.root/'results/c10y_directdw_telemetry_inertness/badpin';diagnostic=self.diagnostic
        try: code=C.run(out,H,diagnostic=diagnostic)
        except TypeError: self.fail('T8 pin failure has no diagnostic path')
        self.assertEqual(code,2);self.assertEqual(H.model.forward_inputs,[])
        diag=A.strict_load(diagnostic);self.assertEqual(diag['code'],'TEMPLATE-DIGEST')
        self.assertTrue(diag['context_templates']['sha256']);self.assertEqual(A.strict_load(out/'inertness.json')['verdict'],'INVALID')


class TelemetryForecastTests(IsolatedCase):
    def fixture(self,stage=1):
        source=self.root/'results/c10y_directdw_telemetry_inertness/frozen/inertness.json'
        source.parent.mkdir(parents=True,exist_ok=True)
        payload={'requests':24,'frames':6,'target_positions':6,'layers':5,'weight_shape':[2048,11008],'vocabulary':151936}
        record={'schema':'c10y_directdw_telemetry_inertness/v1','decision_id':'D-C10r-rulings-11','device':'mps','verdict':'INERT',
            **dict.fromkeys(('control_equal','telemetry_equal','generated_equal','telemetry_complete','weights_unchanged'),True),
            'answer_calls':96,'lens_forwards':48,'sources':A.source_hashes(),'env':A.environment_identity(),
            'answer_line_seconds':[.03]*96,'lens_forward_seconds':[.04]*2,
            'timings':{k:{'seconds':[.01,.02,.01],'repetitions':3,'payload':payload.copy()} for k in ('phase','opt_step','target_probs','write_norms')},
            'lens_payload':payload.copy(),'answer_payload':payload.copy()}
        source.write_text(json.dumps(record))
        phase={'name':'telemetry','measured':True,'artifact':str(source),'sha256':A.sha(source),
            'workload':cal_workload(accepted_steps=100),'repetitions':3,
            'scaling_assumption':'Each bound includes full MPS payload preparation through fsync; header covered by an extra phase bound.',
            'kinds':[{'kind':k,'count':count,'upper_s':.04,'scaling_assumption':'same frozen stage shapes'} for k,count in
                ({'phase':78,'opt_step':100,'target_probs':101,'write_norms':4,'logit_lens':2,'answer':384} if stage==1 else
                 {'phase':274,'opt_step':600,'target_probs':312,'write_norms':15,'logit_lens':5,'answer':1440}).items()]}
        phase['upper_s']=math.fsum(p['count']*p['upper_s'] for p in phase['kinds'])
        forecast=independent_forecast_fixture(self.root/'bound.json',stage=stage);forecast['phases'].append(phase)
        env={'C10Y_TELEMETRY':'1','C10Y_TELEMETRY_INERTNESS':str(source)}
        admission=A.telemetry_admission(env,stage,self.root/f'results/c10y_directdw_s{stage}_rerun1')
        return forecast,admission,record,source
    def test_on_requires_separate_phase_before_dispatch(self):
        forecast,admission,_,_=self.fixture();forecast['phases'].pop()
        # Real entry-point gate receives the verified admission object.
        try: value=A.budget_gate(forecast,7200.,admission)
        except TypeError: self.fail('budget gate has no telemetry admission seam')
        self.assertEqual(value['status'],'UNVERIFIED')
        self.assertEqual(A.budget_gate(forecast,7200.)['status'],'READY')
    def test_per_kind_measurements_workload_and_sum_enforced(self):
        forecast,admission,_,_=self.fixture()
        try: valid=A.budget_gate(forecast,7200.,admission)
        except TypeError: self.fail('missing T10 validation')
        self.assertEqual(valid['status'],'READY')
        for change in ('missing_kind','borrow_kind','short_count','below_max','below_sum','missing_scaling'):
            bad=copy.deepcopy(forecast);phase=bad['phases'][-1]
            if change=='missing_kind': phase['kinds'].pop()
            elif change=='borrow_kind': phase['kinds'][-1]['kind']='phase'
            elif change=='short_count': phase['kinds'][1]['count']=99
            elif change=='below_max': phase['kinds'][-1]['upper_s']=.029999
            elif change=='below_sum': phase['upper_s']-=.000001
            else: phase['kinds'][0].pop('scaling_assumption')
            with self.subTest(change=change): self.assertEqual(A.budget_gate(bad,7200.,admission)['status'],'UNVERIFIED')
    def test_full_stage_counts_and_payload_not_smaller(self):
        forecast,admission,record,path=self.fixture(2)
        try: valid=A.budget_gate(forecast,9000.,admission)
        except TypeError: self.fail('missing T10 validation')
        self.assertEqual(valid['status'],'READY')
        for field,value in (('requests',23),('frames',5),('target_positions',5),('layers',4),('weight_shape',[4,4]),('vocabulary',256)):
            bad=copy.deepcopy(record)
            for entry in bad['timings'].values(): entry['payload'][field]=value
            bad['lens_payload'][field]=value;bad['answer_payload'][field]=value
            path.write_text(json.dumps(bad));forecast['phases'][-1]['sha256']=A.sha(path)
            new=A.telemetry_admission({'C10Y_TELEMETRY':'1','C10Y_TELEMETRY_INERTNESS':str(path)},2,self.root/'results/c10y_directdw_s2_rerun1')
            with self.subTest(field=field): self.assertEqual(A.budget_gate(forecast,9000.,new)['status'],'UNVERIFIED')
    def test_inertness_bytes_once_and_duplicate_nonfinite_refused(self):
        forecast,_,record,path=self.fixture();original=Path.read_bytes;reads=[]
        def reading(p):
            if p==path: reads.append(p)
            return original(p)
        with mock.patch.object(Path,'read_bytes',reading):
            admission=A.telemetry_admission({'C10Y_TELEMETRY':'1','C10Y_TELEMETRY_INERTNESS':str(path)},1,self.root/'results/c10y_directdw_s1_rerun1')
            try: gate=A.budget_gate(forecast,7200.,admission)
            except TypeError: self.fail('missing cached verified bytes seam')
        self.assertEqual(gate['status'],'READY');self.assertEqual(reads,[path])
        for raw in ('{"verdict":"INERT","verdict":"INERT"}',json.dumps(record)[:-1]+',"overflow":1e999}'):
            path.write_text(raw)
            with self.subTest(raw=raw[:40]),self.assertRaises((A.Halt,ValueError)): A.telemetry_admission({'C10Y_TELEMETRY':'1','C10Y_TELEMETRY_INERTNESS':str(path)},1,self.root/'results/c10y_directdw_s1_rerun1')


class FinalReviewRegressionTests(IsolatedCase):
    def test_each_telemetry_method_preserves_every_state_and_A_grad(self):
        H=make_h();H._ARM_STATE={'requests':[H.req(H.CANON,s,H.ARMS[A.A7][s]) for s in H.FICTION]}
        parameter=torch.nn.Parameter(torch.tensor([2.]));parameter.grad=torch.tensor([3.])
        telemetry=A.Telemetry(self.out,'s1','fixed')
        def snapshot():
            return ({n:(v.detach().clone(),v.data_ptr()) for n,v in list(H.model.named_parameters())+list(H.model.named_buffers())},
                    torch.random.get_rng_state().clone(),H.model.training,A.hook_snapshot(H.model),torch.is_grad_enabled(),parameter.grad.clone())
        calls=[lambda:telemetry.phase('stage_start'),
            lambda:telemetry.opt_step(1,{'L_edit':1.,'KL_raw':1.,'KL_weighted':.0625,'L':1.0625},1024.,0,{'4':1.}),
            lambda:telemetry.target_probs(f_ij=[[.9]*6 for _ in range(24)]),
            lambda:telemetry.write_norms({'4':{'actual':1.,'planned':1.,'ratio_to_A':1.}},'B-e2e',A.A7),
            lambda:telemetry.logit_lens(H,H.hp,'pristine'),
            lambda:telemetry.sink(H,'B-e2e','readout',H.CANON.format(H.FICTION[0]),H.tgt_ids('Echo Echo'),H.tgt_ids('Echo Echo'))]
        for call in calls:
            before=snapshot();call();after=snapshot()
            for n,(v,pointer) in before[0].items(): self.assertTrue(torch.equal(v,after[0][n][0]));self.assertEqual(pointer,after[0][n][1])
            self.assertTrue(torch.equal(before[1],after[1]));self.assertEqual(before[2:5],after[2:5]);self.assertTrue(torch.equal(before[5],after[5]))
        self.assertTrue(telemetry.enabled);telemetry.close()

    def test_real_writer_per_write_line_formula(self):
        for mode in ('e2e','anchor'):
            H=make_h();requests=[H.req(H.CANON,s,'Echo Echo') for s in H.FICTION]
            H._ARM_STATE={'requests':requests};H.Z_OVERRIDE={(r['subject'],r['target_new']['str']):H.compute_z(H.model,H.tok,r,H.hp,8,H.get_context_templates(H.model,H.tok)) for r in requests}
            out=self.out/mode;telemetry=A.Telemetry(out,'s1','fixed');writer=A.Writer(H,H.hp,telemetry);writer.baseline_passed=True
            writer.write(mode,requests,H.compute_P(H.hp),[torch.zeros(4,4) for _ in H.hp.layers],iterations=2,lr_override=0.,force_steps=True)
            telemetry.phase('readout_start');scorer=A.make_scorer(H,lambda p,t,g:telemetry.sink(H,'B-e2e','readout',p,t,g))
            for s in H.FICTION:
                for t in [H.CANON]+H.PTEST: scorer(t.format(s),H.tgt_ids('Echo Echo'))
            telemetry.write_norms({str(l):{'actual':A.norm(d),'planned':A.norm(d),'ratio_to_A':1.} for l,d in writer.actual.items()},'B-e2e',A.A7)
            telemetry.target_probs(f_ij=[[.9]*6 for _ in range(24)]);telemetry.logit_lens(H,H.hp,'merged','B-e2e');telemetry.phase('readout_end');telemetry.close()
            rows=[json.loads(s) for s in (out/'telemetry/telemetry_s1.jsonl').read_text().splitlines()]
            # Header excluded; six phases, 96 answers, norms, final fit, A7 lens,
            # one opt_step per accepted iteration and e2e's target_probs.
            self.assertEqual(len(rows)-1,105+2*(1+int(mode=='e2e')))
            self.assertEqual(sum(r['kind']=='answer' for r in rows),96)

    def test_off_scorer_is_original_during_actual_recipe_call(self):
        H=make_h();original=H.full_seq_match
        def recipe(*args):
            self.assertIs(H.full_seq_match,original)
            raise RuntimeError('expected recipe exit')
        H.run_recipe=recipe
        with self.assertRaisesRegex(RuntimeError,'expected recipe exit'): A.scored_recipe(H,'B-e2e',H.HP_BASE,1,None)
        self.assertIs(H.full_seq_match,original)

    def test_complete_compile_at_actual_scientific_hook_boundary(self):
        H=make_h();writer=A.Writer(H,H.hp);writer.mode='e2e';writer.baseline_passed=True
        writer.last_trace={'wall_clock_s':3599.}
        runtime={'budget':A.Budget(0.,7200.,1,clock=lambda:0.),'timings':[{'name':'target_solve','seconds':.5,'workload':{'arms':[A.A7]}}],
            'pre_probes':{A.A7:{}},'recipes':{}}
        H.my_edit=writer;H._C10Y_READOUT_STATE=runtime
        def recipe(*args):
            H._ARM_STATE={'requests':[H.req(H.CANON,s,H.ARMS[A.A7][s]) for s in H.FICTION]}
            H.eval_arm(H.ARMS[A.A7]);arm=copy.deepcopy(valid_record(1)['recipes']['B-e2e']['arms'][A.A7])
            for hook in H.ARM_HOOKS: arm.update(hook(A.A7,H.ARMS[A.A7])['c10y'])
            return {'status':'COMPLETED','law5':{'verdict':'INERT','delta_expr':0.,'delta_loc':0.},'arms':{A.A7:arm}}
        H.run_recipe=recipe;H.eval_arm=lambda *args:{}
        with mock.patch.object(A,'STAGE_CLOCK',side_effect=[0.,.5]),mock.patch.object(A,'scientific_readouts',return_value={'geometry':[]}),mock.patch.object(A,'sample_memory'),mock.patch.object(A,'sync'):
            result=A.scored_recipe(H,'B-e2e',H.HP_BASE,1,None)
        self.assertEqual(result['arms'][A.A7]['compile_s'],3600.)
        self.assertEqual(result['arms'][A.A7]['compile_parts']['production_readout_s'],.5)

    def test_premerge_parity_cannot_spend_postmerge_reserve(self):
        forecast=independent_forecast_fixture(self.root/'bound.json')
        budget=A.Budget(0.,7200.,1,clock=lambda:5400.)
        budget.configure(forecast)
        budget.consume('readout',1200.)
        self.assertEqual(budget.readout_spent,0.)
        budget.remaining={k:0. for k in budget.remaining}
        self.assertEqual(budget.project(0.),6780.)
        budget.write_complete=True;budget.consume('readout',100.)
        self.assertEqual(budget.project(0.),6680.)

    def test_forecast_aware_first_expensive_action_is_not_entered(self):
        forecast=independent_forecast_fixture(self.root/'bound.json')
        for p in forecast['phases']: p['upper_s']=0.
        next(p for p in forecast['phases'] if p['name']=='proofs')['upper_s']=2000.
        next(p for p in forecast['phases'] if p['name']=='readout')['upper_s']=1800.
        budget=A.Budget(0.,7200.,1,clock=lambda:5000.);budget.configure(forecast)
        action=mock.Mock()
        with self.assertRaises(A.Halt) as ctx: A._unit(make_h(),[],'gradient_e2e',A._workload(),action,budget=budget)
        self.assertEqual(ctx.exception.code,'HALTED-BUDGET');action.assert_not_called()
        budget.write_complete=True
        with self.assertRaises(A.Halt) as ctx: budget.project(0.)
        self.assertEqual(ctx.exception.code,'INCOMPLETE-BUDGET')

    def test_live_objective_graph_guard_precedes_backward_and_adam(self):
        p=torch.nn.Parameter(torch.tensor([1.]));opt=torch.optim.Adam([p],lr=.01)
        live={'value':False};calls=[]
        def objective(indices):
            live['value']=True
            return p.square().sum(),{'L':1.}
        def sampler(phase):
            calls.append(phase)
            if live['value']: raise A.Halt('HALTED-RESOURCE')
        with self.assertRaises(A.Halt) as ctx: A.accepted_step([p],opt,objective,[[0]],1024.,0,memory_sampler=sampler)
        self.assertEqual(ctx.exception.code,'HALTED-RESOURCE');self.assertEqual(calls,['objective_graph_live'])
        self.assertEqual(opt.state,{});self.assertIsNone(p.grad);self.assertEqual(float(p[0]),1.)

    def test_real_writer_durable_merge_precedes_postmerge_readout(self):
        H=make_h();requests=[H.req(H.CANON,s,'Echo Echo') for s in H.FICTION]
        H.Z_OVERRIDE={(r['subject'],r['target_new']['str']):H.compute_z(H.model,H.tok,r,H.hp,8,H.get_context_templates(H.model,H.tok)) for r in requests}
        budget=A.Budget(A.STAGE_CLOCK(),7200.,1);writer=A.Writer(H,H.hp,budget=budget);writer.baseline_passed=True
        writer.runtime={'out':self.out,'tag':'s1','current_recipe':'B-e2e'};writer.stage=1
        writer.write('e2e',requests,H.compute_P(H.hp),[torch.zeros(4,4) for _ in H.hp.layers],iterations=0)
        self.assertTrue(budget.write_complete)
        self.assertTrue((self.out/'write_complete_s1.json').is_file())
        with mock.patch.object(budget,'clock',return_value=budget.start+8000.),self.assertRaises(A.Halt) as ctx: budget.project(0.)
        self.assertEqual(ctx.exception.code,'INCOMPLETE-BUDGET')

    def test_merged_fit_reduces_vocabulary_on_cpu_float64(self):
        H=make_h();requests=[H.req(H.CANON,s,'Echo Echo') for s in H.FICTION]
        seen=[];original=A.cpu64
        def cpu(value):
            if value.ndim>=2 and value.shape[-1]==H.model.config.vocab_size: seen.append(value.shape)
            return original(value)
        with mock.patch.object(A,'cpu64',side_effect=cpu): actual=A.merged_fit(H,H.hp,requests,H.get_context_templates(H.model,H.tok))
        self.assertTrue(seen,'fit must transfer full-width logits before their reduction')
        self.assertEqual(len(actual['f_ij']),24);self.assertTrue(all(len(row)==6 for row in actual['f_ij']))
        b=A.request_batch(H,requests[0],H.get_context_templates(H.model,H.tok))
        tokens,positions,_,_=A.packed_batches(H,[b])
        with torch.no_grad(): logits=H.model(**tokens,use_cache=False).logits.detach().cpu().double()
        expected=[]
        for row,pos,ids,_,_ in positions:
            expected.append(float(logits[row,pos].log_softmax(-1).gather(-1,ids.cpu()[:,None]).mean().exp()))
        self.assertEqual(actual['f_ij'][0],expected)

    def test_complete_compile_accounting_drives_ttl_equality(self):
        helper=getattr(A,'compile_accounting',None);self.assertTrue(callable(helper),'missing production accounting')
        runtime={'timings':[{'name':'target_solve','seconds':.5,'workload':{'arms':[A.A7]}},
                            {'name':'baseline_write','seconds':3599.,'workload':{'arms':[A.A7]}}]}
        parts=helper(runtime,A.A7,None,.5)
        self.assertEqual(parts['total_s'],3600.)
        self.assertEqual(parts['target_solve_s'],.5);self.assertEqual(parts['production_readout_s'],.5)
        record=valid_record(2);record['recipes']['B-e2e']['arms'][A.A7]['compile_s']=parts['total_s']
        self.assertIn('EXCEEDS-TTL',R.classify(record)['qualifiers'])

    def test_calibration_callsite_persists_complete_timing_tags(self):
        go,spend=CalibrationTests.records(self);H=make_h()
        prefix=CalibrationTests.fixture(self)
        with mock.patch.object(A,'instrument_prefix',return_value=prefix): record=A.calibrate(self.root/'experiments/c10y/runs/c10y_directdw_calib1',H,go=go,spend=spend,diagnostic=self.diagnostic)
        for row in record['timings']:
            self.assertEqual(row.get('status'),'COMPLETED');self.assertIs(row.get('synchronised'),True)
            self.assertEqual(row['workload']['arms'],[A.A7])
            self.assertTrue(set(('requests','scored_prompts','micro_batches','accepted_steps','retries'))<=set(row['workload']))

    def test_phase_markers_cover_units_without_changing_operational_calls(self):
        H=make_h();telem=A.Telemetry(self.out,'s1','fixed');H._C10Y_TELEMETRY=telem
        action=mock.Mock(return_value=42);timings=[]
        value=A._unit(H,timings,'target_solve',A._workload(A.A7,24),action)
        telem.close();self.assertEqual(value,42);action.assert_called_once_with()
        rows=[json.loads(s) for s in (self.out/'telemetry/telemetry_s1.jsonl').read_text().splitlines()]
        self.assertEqual([r['phase'] for r in rows if r['kind']=='phase'],['target_solve_start','target_solve_end'])

    def test_recorded_contexts_never_sample_even_after_seeding(self):
        H=make_h();source=self.root/'results/contexts.json';A.write_json(source,A.pinned_templates())
        sampled=[]
        def forbidden_sample(*args):
            sampled.append(args);raise AssertionError('recorded contexts must not sample')
        H.get_context_templates=forbidden_sample
        torch.manual_seed(0);record=A.freeze_contexts(H,source,expected=A.sha(source))
        self.assertEqual(record['sha256'],A.sha(source));self.assertEqual(sampled,[])

install_calibration_forecast_replacements(globals())
"""Scratch integration tests for the C10Y persistence and reader boundaries.

Append before the selftest's __main__ block. Required suite globals: A, R, C,
IsolatedCase, W, Path, torch, unittest, mock, make_h, valid_record,
independent_forecast_fixture. This file is authored without executing Python.

The scientific prefix and recipe results are synthetic valid_record fixtures.
Every tensor is tiny and on CPU. The manifest and inertness fixture explicitly
mark their MPS metadata as synthetic; they never constitute live admission,
LAW#3/LAW#5, optimization, memory, or model-behavior evidence. Real code under
test includes run, preflight, context installation, budget admission, immutable
JSON/PT transport, normalization, reproduction_record, load, classify, audit,
and the model-free launch guards.
"""

import contextlib
import copy
import importlib
import io
import json
import math
import os
import types


class TransportTests(IsolatedCase):
    FIXTURE_SCOPE = "CPU transport only; scientific records and MPS metadata synthetic; live evidence UNVERIFIED"
    FIXED_UTC = "2026-10-08T00:00:00+00:00"

    def setUp(self):
        super().setUp()
        # Copy the current source table, including Amendment P's benchmark,
        # rather than borrowing any live model/cache directory or fake SHA.
        for relative in A.SOURCE_PATHS.values():
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(fixture_source(relative))
        self.transport_calls = []
        self.transport_tensors = []
        self.transport_roots = {}
        self.transport_inertness = None

    def _go(self, stage):
        return {"decision_id": "D-C10Y-synthetic-go", "experiment": "C10Y",
                "stage": stage, "recorded_in": "program/runbook/:5",
                "at": self.FIXED_UTC}

    def _spend(self, stage):
        return None if stage == 1 else {"decision_id": "D-C10Y-synthetic-spend",
                                        "stage": stage, "cap_s": 9000.}

    def _inertness(self):
        if self.transport_inertness is not None:
            return self.transport_inertness
        path = self.root / "results/c10y_directdw_telemetry_inertness/transport_fixture/inertness.json"
        payload = {"requests": 24, "frames": 6, "target_positions": 6,
                   "layers": 5, "weight_shape": [2048, 11008], "vocabulary": 151936}
        record = {"schema": "c10y_directdw_telemetry_inertness/v1",
                  "decision_id": "D-C10r-rulings-11", "device": "mps", "verdict": "INERT",
                  "fixture_scope": self.FIXTURE_SCOPE,
                  **dict.fromkeys(("control_equal", "telemetry_equal", "generated_equal",
                                   "telemetry_complete", "weights_unchanged"), True),
                  "answer_calls": 96, "lens_forwards": 48,
                  "sources": A.source_hashes(), "env": A.environment_identity(),
                  "answer_line_seconds": [.03] * 96, "lens_forward_seconds": [.04] * 2,
                  "answer_payload": payload.copy(), "lens_payload": payload.copy(),
                  "timings": {kind: {"seconds": [.01, .02, .01], "repetitions": 3,
                                      "payload": payload.copy()}
                              for kind in ("phase", "opt_step", "target_probs", "write_norms")}}
        A.write_json(path, record)
        self.transport_inertness = path
        return path

    def _forecast(self, stage, telemetry=False, equivalent_total=False):
        path = self.root / ("transport_bound_s%d_%s.json" % (stage, "on" if telemetry else "off"))
        forecast = independent_forecast_fixture(path, stage=stage, total=3000.)
        kinds = [{"kind": kind, "count": count, "upper_s": 1.,
                  "scaling_assumption": "synthetic transport bound, never live dispatch support"}
                 for kind, count in A.telemetry_workload(stage).items()]
        extra = math.fsum(row["count"] * row["upper_s"] for row in kinds)
        if telemetry:
            evidence = self._inertness()
            forecast["phases"].append({
                "name": "telemetry", "measured": True, "artifact": str(evidence),
                "sha256": A.sha(evidence), "workload": {
                    "arms": [A.A7], "requests": 24, "scored_prompts": 96,
                    "micro_batches": 4, "accepted_steps": 100, "retries": 5},
                "repetitions": 3, "upper_s": extra, "kinds": kinds,
                "scaling_assumption": "synthetic fixed full-payload fixture; not an MPS timing claim"})
        elif equivalent_total:
            # Both admitted forecasts have the same recorded total. The off
            # independent bound conservatively includes the on reserve. No
            # projected_s or clock-derived scientific field is ignored below.
            preflight = next(row for row in forecast["phases"] if row["name"] == "preflight")
            preflight["upper_s"] += extra
            preflight["justification"] += "; covers the matching synthetic telemetry reserve"
        return forecast

    def _h(self, science):
        H = make_h()
        stimuli = science["manifest"]["parts"]["stimuli"]
        H.CANON, H.PTEST = stimuli["CANON"], list(stimuli["PTEST"])
        H.ARMS = copy.deepcopy(stimuli["ARMS"])
        H.FICTION = list(H.ARMS[A.A7])
        expected = A.pinned_templates()
        scope = {"expected": expected, "copy": copy, "calls": []}
        # A private global scope makes the engine cache observable without
        # modifying the suite's own globals or permitting a sampling fallback.
        exec("def get_context_templates(model,tok):\n"
             "    calls.append(1)\n"
             "    cached=globals().get('CONTEXT_TEMPLATES_CACHE')\n"
             "    if cached!=expected: raise AssertionError('template sampling attempted')\n"
             "    return copy.deepcopy(cached)\n", scope)
        H.get_context_templates = scope["get_context_templates"]
        H._transport_context_scope = scope
        self.assertEqual(H.DEV, "cpu")
        self.assertTrue(all(t.device.type == "cpu" for t in H.model.parameters()))
        return H

    def _updates(self, science, changed_direction=False):
        updates = {}
        for name, recipe in science["recipes"].items():
            arms = {}
            for arm, data in recipe["arms"].items():
                if data["status"] != "COMPLETED":
                    continue
                sign = -1. if changed_direction and name == "B-e2e" and arm == A.A7 else 1.
                arms[arm] = {layer: torch.tensor([[sign, 0.], [0., 0.]], dtype=torch.float32)
                             for layer in (4, 5, 6, 7, 8)}
                self.transport_tensors.extend(arms[arm].values())
                if sign < 0:
                    for row in data["geometry"]:
                        row["cosine_to_A"] = -1.
            updates[name] = arms
        return updates

    def _emit_recipe(self, telemetry, H, name, recipe):
        if telemetry is None:
            return
        telemetry.phase("synthetic_readout", recipe=name)
        for arm, data in recipe["arms"].items():
            if data["status"] != "COMPLETED":
                continue
            for row in data["detail"]:
                flags = [(row["canon_full"], row["canon_first"])] + list(zip(row["para_full_hits"], row["para_first_hits"]))
                for template, (full, first) in zip([H.CANON] + H.PTEST, flags):
                    ids = list(range(10, 10 + row["ntok"]))
                    generated = ids.copy() if full else [value + 1000 for value in ids]
                    if first:
                        generated[0] = ids[0]
                    self.assertEqual(generated == ids, full)
                    self.assertEqual(generated[0] == ids[0], first)
                    # These are explicitly synthetic score outputs. The real
                    # Telemetry emitter persists and the real T11 reader
                    # reconciles them against immutable scientific detail.
                    telemetry.emit("answer", recipe=name, arm=arm, phase="readout",
                                   subj=row["subj"], val=row["val"], template=template,
                                   prompt=template.format(row["subj"]), target_ids=ids,
                                   generated_ids=generated, text=H.tok.decode(generated),
                                   full=full, first=first)

    def _execute(self, stage, out=None, predecessor=None, contexts=None,
                 telemetry=False, replacement=None, changed_direction=False,
                 equivalent_total=False):
        out = self.out if out is None else out
        science = valid_record(stage)
        H = self._h(science)
        original_edit = H.my_edit
        updates = self._updates(science, changed_direction=changed_direction)
        targets = {(row["subject"], row["target"]): torch.tensor([i + 1., 0., 0., 0.])
                   for i, row in enumerate(science["manifest"]["parts"]["requests"][A.A7])}
        self.transport_tensors.extend(targets.values())
        ledger = [copy.deepcopy(row) for row in science["ledger"] if row["recipe"] == "A"]
        runtime = {"ledger": ledger, "timings": [], "fixture_scope": self.FIXTURE_SCOPE}
        writer = types.SimpleNamespace(mode=None)

        def prefix(H_arg, out_arg, budget, calibration=False, telemetry=None):
            self.assertIs(H_arg, H)
            self.assertIs(calibration, False)
            self.transport_calls.append((stage, "prefix"))
            expected_path = contexts if stage > 1 else Path(out_arg) / "context_templates.json"
            self.assertTrue(Path(expected_path).is_file(), "context bytes must exist before recipe A")
            pinned = H.get_context_templates(H.model, H.tok)
            self.assertEqual(pinned, A.pinned_templates())
            baseline = A.normalize_recipe(science["recipes"]["A"], "A", stage)
            self._emit_recipe(telemetry, H, "A", baseline)
            return {"baseline": baseline, "contexts": pinned, "targets": targets,
                    "ledger": ledger, "overlap_audit": copy.deepcopy(science["overlap_audit"]),
                    "law5": copy.deepcopy(baseline["law5"]),
                    "step0": {"fixture_scope": self.FIXTURE_SCOPE},
                    "checks": {}, "baseline_passed": True, "writer": writer,
                    "runtime": runtime, "actual_A": updates["A"],
                    "actual_B": {name: rows for name, rows in updates.items() if name != "A"}}

        def recipe(H_arg, name, hppath, stage_arg, telemetry):
            self.assertIs(H_arg, H)
            self.assertEqual(stage_arg, stage)
            self.transport_calls.append((stage, name))
            self.assertIs(H.my_edit, writer)
            ledger.extend(copy.deepcopy(row) for row in science["ledger"] if row["recipe"] == name)
            value = A.normalize_recipe(science["recipes"][name], name, stage)
            self._emit_recipe(telemetry, H, name, value)
            return value

        original_manifest = A.record_manifest

        def synthetic_manifest(H_arg, hp, context, info, artifacts, inputs):
            value = original_manifest(H_arg, hp, context, info, artifacts, inputs)
            value["parts"]["device"] = "mps"
            value["parts"]["library_versions"]["backend"] = "mps"
            value["parts"]["fixture_scope"] = self.FIXTURE_SCOPE
            value["H_in"] = A.digest(value["parts"])
            return value

        forecast = self._forecast(stage, telemetry, equivalent_total)
        env = dict(os.environ, C10Y_STAGE_START="0")
        for key in ("C10Y_TELEMETRY", "C10Y_TELEMETRY_INERTNESS"):
            env.pop(key, None)
        if telemetry:
            env.update(C10Y_TELEMETRY="1", C10Y_TELEMETRY_INERTNESS=str(self._inertness()))
        diagnostic = self.root / ("architecture_profile/c10y_transport_%s_s%d.json" % (out.name, stage))
        self.last_transport_prefix = mock.Mock(side_effect=prefix)
        self.last_transport_recipe = mock.Mock(side_effect=recipe)
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.dict(os.environ, env, clear=True))
            stack.enter_context(mock.patch.object(A, "STAGE_CLOCK", return_value=0.))
            stack.enter_context(mock.patch.object(A, "TELEMETRY_CLOCK", return_value=0.))
            stack.enter_context(mock.patch.object(A, "utc", return_value=self.FIXED_UTC))
            stack.enter_context(mock.patch.object(A, "sync", return_value=None))
            stack.enter_context(mock.patch.object(A, "sample_memory", return_value={}))
            forbidden_mps = stack.enter_context(mock.patch.object(torch.mps, "synchronize", side_effect=AssertionError("MPS call forbidden in CPU transport")))
            stack.enter_context(mock.patch.object(A, "instrument_prefix", self.last_transport_prefix))
            stack.enter_context(mock.patch.object(A, "scored_recipe", self.last_transport_recipe))
            stack.enter_context(mock.patch.object(A, "record_manifest", side_effect=synthetic_manifest))
            result = A.run(out, H, stage=stage, go=self._go(stage), spend=self._spend(stage),
                           forecast=forecast, predecessor=predecessor, contexts=contexts,
                           context_sha=A.sha(contexts) if contexts is not None else None,
                           diagnostic=diagnostic, replacement=replacement)
            forbidden_mps.assert_not_called()
        self.assertEqual(result["run"]["status"], "COMPLETED", result["run"])
        self.assertIs(H.my_edit, original_edit)
        self.assertIsNone(H.Z_OVERRIDE)
        self.assertEqual(H.Z_OVERRIDE_HITS, 0)
        self.assertFalse(H._LAW5_DEFAULT_CTX)
        self.assertFalse(hasattr(H, "_C10Y_READOUT_STATE"))
        self.assertEqual(H._transport_context_scope["calls"], [1])
        self.assertFalse(diagnostic.exists())
        self.assertTrue(all(t.device.type == "cpu" for t in self.transport_tensors))
        self.assertEqual(result["manifest"]["parts"]["fixture_scope"], self.FIXTURE_SCOPE)
        return result

    def _load_payload(self, out, stage):
        tag = "s1" if stage == 1 else "p%d" % (stage - 1)
        path = out / ("targets_%s.pt" % tag)
        payload = torch.load(path, map_location="cpu", weights_only=True)
        self.assertEqual(set(payload), {"targets", "actual_updates"})
        for tensor in payload["targets"].values():
            self.assertEqual(tensor.device.type, "cpu")
        for arms in payload["actual_updates"].values():
            for layers in arms.values():
                self.assertEqual(set(layers), {4, 5, 6, 7, 8})
                for tensor in layers.values():
                    self.assertEqual(tensor.device.type, "cpu")
                    self.assertEqual(tensor.dtype, torch.float32)
                    self.assertEqual(tuple(tensor.shape), (2, 2))
        return payload

    def _chain(self):
        first = self._execute(1)
        source = self.out / "context_templates.json"
        second = self._execute(2, predecessor=self.out / "screen.json", contexts=source)
        third = self._execute(3, predecessor=self.out / "pass_p1.json", contexts=source)
        return first, second, third

    def _flags_counts(self, record):
        result = {}
        for name, recipe in record["recipes"].items():
            for arm, data in recipe["arms"].items():
                if data["status"] != "COMPLETED":
                    continue
                rows = data["detail"]
                result[(name, arm)] = {"canonical": sum(row["canon_full"] for row in rows),
                                       "heldout_full": sum(sum(row["para_full_hits"]) for row in rows),
                                       "heldout_first": sum(sum(row["para_first_hits"]) for row in rows),
                                       "prompts": len(rows) * (1 + len(record["manifest"]["parts"]["stimuli"]["PTEST"]))}
                self.assertEqual(result[(name, arm)]["canonical"], data["metrics"]["canon_full_n"])
                self.assertEqual(result[(name, arm)]["heldout_full"], data["metrics"]["para_full_n"])
                self.assertEqual(result[(name, arm)]["heldout_first"], data["metrics"]["para_first_n"])
        return result

    def _relocated(self, value):
        if isinstance(value, dict):
            return {key: self._relocated(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self._relocated(item) for item in value]
        if isinstance(value, str):
            for directory, canonical in sorted(self.transport_roots.items(), key=lambda row: len(row[0]), reverse=True):
                if value == directory or value.startswith(directory + "/"):
                    return canonical + value[len(directory):]
        return value

    def test_completed_stage1_runner_to_reader_and_cpu_pt_transport(self):
        result = self._execute(1)
        loaded = R.load(self.out)
        self.assertEqual(loaded, A.strict_load(self.out / "screen.json"))
        self.assertEqual(result, loaded)
        self.assertEqual(R.classify(loaded)["label"], "SCREEN-PASS")
        self.assertEqual(result["reading"], R.classify(loaded))
        for name, key in (("manifest.json", "manifest"), ("run.json", "run"),
                          ("ledger.json", "ledger"), ("overlap_audit.json", "overlap_audit")):
            self.assertEqual(A.strict_load(self.out / name), loaded[key])
        payload = self._load_payload(self.out, 1)
        self.assertEqual(set(payload["actual_updates"]), set(loaded["recipes"]))
        self.assertEqual(set(payload["actual_updates"]["B-e2e"]), {A.A7})
        self.assertEqual(set(payload["targets"]), {(row["subject"], row["target"])
                                                 for row in loaded["manifest"]["parts"]["requests"][A.A7]})
        self.assertEqual(A.strict_load(self.out / "context_templates.json"), A.pinned_templates())
        declared = loaded["manifest"]["parts"]["source_sha256"]
        self.assertEqual(declared, {name: A.sha(self.root / relative) for name, relative in A.SOURCE_PATHS.items()})
        self._flags_counts(loaded)
        self.assertEqual(self.transport_calls, [(1, "prefix"), (1, "B-e2e")])

    def test_completed_three_stages_preserve_common_files_and_compute_real_repro(self):
        first = self._execute(1)
        names = ("context_templates.json", "manifest.json", "run.json", "ledger.json", "overlap_audit.json", "screen.json")
        common = {name: (self.out / name).read_bytes() for name in names}
        source = self.out / "context_templates.json"
        second = self._execute(2, predecessor=self.out / "screen.json", contexts=source)
        with mock.patch.object(A, "reproduction_record", wraps=A.reproduction_record) as reduction:
            third = self._execute(3, predecessor=self.out / "pass_p1.json", contexts=source)
        reduction.assert_called_once()
        self.assertEqual(common, {name: (self.out / name).read_bytes() for name in names})
        self.assertEqual(R.load(self.out), third)
        self.assertEqual(R.load(self.out / "screen.json"), first)
        self.assertEqual(R.load(self.out / "pass_p1.json"), second)
        self.assertEqual(R.load(self.out / "pass_p2.json"), third)
        self.assertEqual(R.classify(first)["label"], "SCREEN-PASS")
        self.assertEqual(R.classify(second)["label"], "PARTIAL")
        self.assertTrue(R.classify(second)["advance"])
        self.assertEqual(first["manifest"]["H_in"], second["manifest"]["H_in"])
        self.assertEqual(second["manifest"]["H_in"], third["manifest"]["H_in"])
        payload1, payload2 = self._load_payload(self.out, 2), self._load_payload(self.out, 3)
        repro = A.strict_load(self.out / "repro.json")
        self.assertEqual(repro["reduction_dtype"], "float64")
        self.assertEqual(repro["reduction_device"], "cpu")
        for name in second["recipes"]:
            rows = repro["baseline"] if name == "A" else repro["recipes"][name]
            for arm in second["recipes"][name]["arms"]:
                for row in rows["arms"][arm]["layers"]:
                    layer = row["layer"]
                    one = payload1["actual_updates"][name][arm][layer].double().reshape(-1)
                    two = payload2["actual_updates"][name][arm][layer].double().reshape(-1)
                    self.assertEqual(row["norm_p1"], float(one.norm()))
                    self.assertEqual(row["norm_p2"], float(two.norm()))
                    self.assertEqual(row["cosine"], float(one @ two / (one.norm() * two.norm())))
                    self.assertEqual(row["distance"], float((one - two).norm() / max(one.norm(), two.norm())))
        self.assertEqual({(row["subject"], row["target"]) for row in repro["per_fact_z_cosine"]}, set(payload2["targets"]))
        self.assertTrue(all(row["cosine"] == 1. for row in repro["per_fact_z_cosine"]))
        pair = R.cross_process(R.load(self.out / "pass_p1.json"), R.load(self.out / "pass_p2.json"), repro)
        self.assertEqual(pair["label"], "PARTIAL")
        self.assertEqual(pair["reproducibility_status"], "PASS")
        self.assertTrue(pair["advance"])
        self.assertEqual(third["manifest"]["paired_stage2"], str(self.out))
        self.assertEqual(self._flags_counts(second), self._flags_counts(third))

    def test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate(self):
        self._execute(1)
        source = self.out / "context_templates.json"
        second = self._execute(2, predecessor=self.out / "screen.json", contexts=source)
        third = self._execute(3, predecessor=self.out / "pass_p1.json", contexts=source, changed_direction=True)
        repro = A.strict_load(self.out / "repro.json")
        candidate = repro["recipes"]["B-e2e"]["arms"][A.A7]["layers"]
        self.assertTrue(all(row["cosine"] == -1. and row["distance"] == 2. for row in candidate))
        self.assertTrue(all(row["cosine"] == 1. and row["distance"] == 0.
                            for data in repro["baseline"]["arms"].values() for row in data["layers"]))
        self.assertEqual(R.classify(R.load(self.out / "pass_p2.json"))["label"], "PARTIAL")
        pair = R.cross_process(R.load(self.out / "pass_p1.json"), R.load(self.out / "pass_p2.json"), repro)
        self.assertEqual(pair["reproducibility_status"], "FAIL")
        self.assertIn("NOT-REPRODUCIBLE", pair["qualifiers"])
        self.assertFalse(pair["advance"])
        self.assertEqual(self._flags_counts(second), self._flags_counts(third))

    def test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks(self):
        self._execute(1)
        source = self.out / "context_templates.json"
        self._execute(2, predecessor=self.out / "screen.json", contexts=source)
        target = self.out / "targets_p1.pt"
        target.write_bytes(target.read_bytes() + b"controlled synthetic hash mismatch")
        with self.assertRaises(ValueError):
            R.load(self.out / "pass_p1.json")
        calls = list(self.transport_calls)
        with self.assertRaises(ValueError):
            self._execute(3, predecessor=self.out / "pass_p1.json", contexts=source)
        self.last_transport_prefix.assert_not_called()
        self.last_transport_recipe.assert_not_called()
        self.assertEqual(self.transport_calls, calls)
        self.assertFalse((self.out / "pass_p2.json").exists())
        self.assertFalse((self.out / "targets_p2.pt").exists())

    def test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor(self):
        self._chain()
        prior = self.out / "pass_p2.json"
        self.assertTrue(R.classify(R.load(prior))["advance"], "isolate stage identity from eligibility label")
        go, spend, forecast = (self.root / name for name in ("transport_go.json", "transport_spend.json", "transport_forecast.json"))
        A.write_json(go, self._go(3))
        A.write_json(spend, self._spend(3))
        A.write_json(forecast, self._forecast(3))
        calls = []
        imports = importlib.import_module

        def tracked(name, *args, **kwargs):
            calls.append(name)
            if name == "c10e_bandknob":
                raise AssertionError("real harness import forbidden")
            return imports(name, *args, **kwargs)

        stderr = io.StringIO()
        with mock.patch.object(importlib, "import_module", side_effect=tracked), \
             mock.patch.object(A, "supervise", side_effect=AssertionError("child dispatch forbidden")) as supervisor, \
             contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
            code = A.main(["--budget-gate", "--stage", "3", "--out", str(self.root / "results/c10y_directdw_s3_rerun1"),
                           "--halt-diagnostic", str(self.diagnostic), "--go", str(go), "--spend", str(spend),
                           "--forecast", str(forecast), "--predecessor", str(prior),
                           "--contexts", str(self.out / "context_templates.json"),
                           "--context-sha", A.sha(self.out / "context_templates.json")])
        self.assertEqual(code, 2)
        self.assertIn("PREDECESSOR-STAGE", stderr.getvalue())
        self.assertNotIn("c10e_bandknob", calls)
        supervisor.assert_not_called()

    def test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage(self):
        self._chain()  # Immutable first-attempt records serve as replacement provenance.
        prior, contexts, paired_stage2 = {}, {}, {}
        for stage in (1, 2, 3):
            records, directories, operational = {}, {}, {}
            for enabled in (False, True):
                out = self.root / ("results/c10y_directdw_s%d_rerun%d" % (stage, 2 if enabled else 1))
                self.transport_roots[str(out)] = str(self.root / ("results/transport_stage%d" % stage))
                before = len(self.transport_calls)
                record = self._execute(stage, out=out, telemetry=enabled,
                                       predecessor=prior.get(enabled) if stage > 1 else None,
                                       contexts=contexts.get(enabled) if stage > 1 else None,
                                       replacement={"replaces": str(self.out), "cause": "synthetic transport comparison"},
                                       equivalent_total=True)
                own = "screen.json" if stage == 1 else "pass_p%d.json" % (stage - 1)
                loaded = R.load(out / own)
                self.assertEqual(record, loaded)
                records[enabled], directories[enabled] = loaded, out
                operational[enabled] = self.transport_calls[before:]
                prior[enabled] = out / own
                if stage == 1:
                    contexts[enabled] = out / "context_templates.json"
                elif stage == 2:
                    paired_stage2[enabled] = out / own
                self._load_payload(out, stage)
            off, on = copy.deepcopy(records[False]), copy.deepcopy(records[True])
            self.assertIs(off["run"]["telemetry"], False)
            self.assertIsNone(off["run"]["telemetry_inertness"])
            self.assertIs(on["run"]["telemetry"], True)
            self.assertEqual(on["run"]["telemetry_inertness"], {"path": str(self._inertness()), "sha256": A.sha(self._inertness())})
            for record in (off, on):
                del record["run"]["telemetry"]
                del record["run"]["telemetry_inertness"]
            self.assertEqual(self._relocated(off), self._relocated(on))
            self.assertEqual(operational[False], operational[True])
            self.assertEqual(R.classify(records[False]), R.classify(records[True]))
            self.assertEqual(self._flags_counts(records[False]), self._flags_counts(records[True]))
            self.assertEqual(A.strict_load(directories[False] / "ledger.json"), A.strict_load(directories[True] / "ledger.json"))
            for artifact, digest in records[False]["manifest"]["artifacts"].items():
                self.assertEqual(digest, A.sha(directories[False] / artifact))
                self.assertEqual(digest, A.sha(directories[True] / artifact))
            tag = "s1" if stage == 1 else "p%d" % (stage - 1)
            self.assertFalse((directories[False] / "telemetry").exists())
            lines = [json.loads(line) for line in (directories[True] / "telemetry" / ("telemetry_%s.jsonl" % tag)).read_text().splitlines()]
            self.assertEqual(lines[0]["kind"], "header")
            expected = sum(row["prompts"] for row in self._flags_counts(records[True]).values())
            self.assertEqual(sum(row["kind"] == "answer" for row in lines), expected)
            audit = C.audit(directories[True], stage=stage)
            self.assertEqual(audit["verdict"], "PASS", audit["issues"])
            self.assertEqual(audit["expected_answers"], expected)
            self.assertEqual(audit["observed_answers"], expected)
            self.assertTrue(audit["science_record_stands"])
            if stage == 3:
                repro_off = A.strict_load(directories[False] / "repro.json")
                repro_on = A.strict_load(directories[True] / "repro.json")
                self.assertEqual(self._relocated(repro_off), self._relocated(repro_on))
                pair_off = R.cross_process(R.load(paired_stage2[False]), records[False], repro_off)
                pair_on = R.cross_process(R.load(paired_stage2[True]), records[True], repro_on)
                self.assertEqual(pair_off, pair_on)
                self.assertEqual(pair_off["reproducibility_status"], "PASS")
                self.assertTrue(pair_off["advance"])

    def test_stage3_telemetry_setting_cannot_change_after_stage2(self):
        self._execute(1)
        source = self.out / "context_templates.json"
        self._execute(2, predecessor=self.out / "screen.json", contexts=source)
        out = self.root / "results/c10y_directdw_s3_rerun1"
        calls = list(self.transport_calls)
        with self.assertRaises(A.Halt) as refusal:
            self._execute(3, out=out, predecessor=self.out / "pass_p1.json", contexts=source,
                          telemetry=True, replacement={"replaces": str(self.out), "cause": "synthetic pair switch"})
        self.assertEqual(refusal.exception.code, "TELEMETRY-PAIR")
        self.last_transport_prefix.assert_not_called()
        self.last_transport_recipe.assert_not_called()
        self.assertEqual(self.transport_calls, calls)
        self.assertFalse(out.exists())

    def test_requested_stage_forecast_is_checked_before_dispatch_and_worker(self):
        self._execute(1);prior=self.out/'screen.json';context=self.out/'context_templates.json'
        wrong=self._forecast(1);out=self.root/'results/c10y_directdw_s2_rerun1'
        with mock.patch.object(A,'instrument_prefix',side_effect=AssertionError('wrong forecast reached science')) as prefix,self.assertRaises(A.Halt) as ctx:
            A.run(out,self._h(valid_record(2)),stage=2,go=self._go(2),spend=self._spend(2),forecast=wrong,
                  predecessor=prior,contexts=context,context_sha=A.sha(context),diagnostic=self.diagnostic)
        self.assertEqual(ctx.exception.code,'FORECAST-STAGE');prefix.assert_not_called();self.assertFalse(out.exists())
        go=self.root/'go2.json';spend=self.root/'spend2.json';forecast=self.root/'wrong_stage.json'
        A.write_json(go,self._go(2));A.write_json(spend,self._spend(2));A.write_json(forecast,wrong)
        stderr=io.StringIO()
        with mock.patch.object(A,'supervise',side_effect=AssertionError('wrong forecast dispatched')) as supervisor,contextlib.redirect_stderr(stderr),contextlib.redirect_stdout(io.StringIO()):
            code=A.main(['--stage','2','--out',str(out),'--halt-diagnostic',str(self.diagnostic),'--go',str(go),'--spend',str(spend),
                         '--forecast',str(forecast),'--predecessor',str(prior),'--contexts',str(context),'--context-sha',A.sha(context)])
        self.assertEqual(code,2);self.assertIn('FORECAST-STAGE',stderr.getvalue());supervisor.assert_not_called()

    def test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write(self):
        self._execute(1);context=self.out/'context_templates.json';self._execute(2,predecessor=self.out/'screen.json',contexts=context)
        out=self.root/'results/c10y_directdw_s3_rerun1'
        go=self.root/'go3.json';spend=self.root/'spend3.json';forecast=self.root/'forecast3_on.json'
        A.write_json(go,self._go(3));A.write_json(spend,self._spend(3));A.write_json(forecast,self._forecast(3,telemetry=True))
        stderr=io.StringIO()
        with mock.patch.dict(os.environ,{'C10Y_TELEMETRY':'1','C10Y_TELEMETRY_INERTNESS':str(self._inertness())}),mock.patch.object(A,'supervise',side_effect=AssertionError('mismatched pair dispatched')) as supervisor,contextlib.redirect_stderr(stderr),contextlib.redirect_stdout(io.StringIO()):
            code=A.main(['--stage','3','--out',str(out),'--halt-diagnostic',str(self.diagnostic),'--go',str(go),'--spend',str(spend),
                         '--forecast',str(forecast),'--predecessor',str(self.out/'pass_p1.json'),'--contexts',str(context),'--context-sha',A.sha(context)])
        self.assertEqual(code,2);self.assertIn('TELEMETRY-PAIR',stderr.getvalue());supervisor.assert_not_called();self.assertFalse(out.exists())

    def test_saved_overlay_hash_is_the_immutable_serialized_bundle(self):
        record=self._execute(1);path=self.out/'targets_s1.pt';payload=self._load_payload(self.out,1)
        for name,recipe in record['recipes'].items():
            for arm,data in recipe['arms'].items():
                if data['status']!='COMPLETED': continue
                h=data['H_out'];self.assertEqual(h['overlay_sha256'],A.sha(path))
                self.assertEqual(h.get('overlay_artifact'),'targets_s1.pt');self.assertEqual(h.get('overlay_member'),['actual_updates',name,arm])
                self.assertIn(arm,payload['actual_updates'][name]);self.assertEqual(h.get('tensor_certificate_sha256'),A.digest(h['tensors']))
        for change in ('hash','member','certificate'):
            bad=copy.deepcopy(record);h=bad['recipes']['B-e2e']['arms'][A.A7]['H_out']
            if change=='hash': h['overlay_sha256']='0'*64
            elif change=='member': h['overlay_member']=['actual_updates','A',A.A7]
            else: h['tensor_certificate_sha256']='0'*64
            with self.subTest(change=change): self.assertEqual(R.classify(bad)['label'],'INVALID')

    def test_real_scored_recipe_accounts_for_scientific_hook_readout_time(self):
        science = valid_record(1)
        H = self._h(science)
        time_value = [100.]
        clock = lambda: time_value[0]
        budget = A.Budget(0., 7200., 1, clock=clock)
        budget.configure(self._forecast(1))
        budget.write_complete = True
        writer = A.Writer(H, H.hp, budget=budget)
        writer.mode = "e2e"
        writer.last_trace = {"wall_clock_s": 15.}
        H.my_edit = writer
        H._C10Y_READOUT_STATE = {
            "pre_probes": {A.A7: {}}, "budget": budget, "timings": [
                {"name": "target_solve", "seconds": 5., "workload": {"arms": [A.A7]}}],
            "recipes": {}}
        calls = []

        def evaluate(values):
            calls.append("harness_readout")
            time_value[0] += 2.
            return {}

        def scientific(H_arg, hp, arm, values, runtime, writer_arg, name):
            calls.append("scientific_hook")
            self.assertIs(H_arg, H)
            self.assertIs(writer_arg, writer)
            time_value[0] += 3.
            value = copy.deepcopy(science["recipes"][name]["arms"][arm])
            value["trace"]["wall_clock_s"] = writer.last_trace["wall_clock_s"]
            return value

        def recipe(name, hppath):
            H._ARM_STATE = {"requests": [H.req(H.CANON, subject, target)
                                          for subject, target in H.ARMS[A.A7].items()]}
            H.eval_arm(H.ARMS[A.A7])
            raw = copy.deepcopy(science["recipes"][name])
            for hook in H.ARM_HOOKS:
                raw["arms"][A.A7].update(hook(A.A7, H.ARMS[A.A7])["c10y"])
            return raw

        H.eval_arm, H.run_recipe = evaluate, recipe
        original_arms, original_hooks, original_scorer = H.ARMS, H.ARM_HOOKS, H.full_seq_match
        with mock.patch.object(A, "STAGE_CLOCK", side_effect=clock), \
             mock.patch.object(A, "sync", return_value=None), \
             mock.patch.object(A, "sample_memory", return_value={}), \
             mock.patch.object(A, "scientific_readouts", side_effect=scientific), \
             mock.patch.object(torch.mps, "synchronize", side_effect=AssertionError("MPS forbidden")) as mps:
            result = A.scored_recipe(H, "B-e2e", H.HP_BASE, 1, None)
        mps.assert_not_called()
        arm = result["arms"][A.A7]
        self.assertEqual(calls, ["harness_readout", "scientific_hook"])
        self.assertEqual(arm["compile_parts"]["target_solve_s"], 5.)
        self.assertEqual(arm["compile_parts"]["capture_optimisation_merge_s"], 15.)
        self.assertEqual(arm["compile_parts"]["production_readout_s"], 5.)
        self.assertEqual(arm["compile_parts"]["total_s"], 25.)
        self.assertEqual(arm["compile_s"], 25.)
        self.assertEqual(budget.readout_spent, 5.)
        self.assertNotIn("_production_eval_started", H._C10Y_READOUT_STATE)
        self.assertIs(H.eval_arm, evaluate)
        self.assertIs(H.ARMS, original_arms)
        self.assertIs(H.ARM_HOOKS, original_hooks)
        self.assertIs(H.full_seq_match, original_scorer)
        self.assertTrue(all(t.device.type == "cpu" for t in H.model.parameters()))

class LaunchDeltaTests(IsolatedCase):
    def test_stored_scale_sum_matches_reader_float64_sum(self):
        reference={l:torch.tensor([[.2]],dtype=torch.float64) for l in LAYERS}
        candidate={l:torch.tensor([[.4 if l==4 else .2]],dtype=torch.float64) for l in LAYERS}
        scale=A.size_scales(reference,candidate)['NM']
        expected=math.fsum(A.norm(v) for v in reference.values())/math.fsum(A.norm(v) for v in candidate.values())
        self.assertEqual(scale,expected)

    def test_nm_decimal_boundary_through_real_reader(self):
        for value in (0.99,1.01,0.989999,1.010001):
            record=add_controls(valid_record(2))
            for arm in ARMS:
                record['recipes']['A']['arms'][arm]['geometry']=geometry([.2]*5)
                record['recipes']['B-e2e']['arms'][arm]['geometry']=geometry([.4,.2,.2,.2,.2])
                nm=record['recipes']['B-e2e-NM']['arms'][arm]
                nm['stored_control']['scale']=math.fsum([.2]*5)/math.fsum([.4,.2,.2,.2,.2]);nm['geometry']=geometry([value,0.,0.,0.,0.])
                record['recipes']['B-e2e-ENV']['arms'][arm]['geometry']=geometry([.2,.1,.1,.1,.1])
            result=R.classify(record)
            with self.subTest(value=value): self.assertEqual('SIZE-UNTESTED' in result['qualifiers'],value not in (0.99,1.01))

    def test_nm_decimal_boundary_through_scientific_hook(self):
        # Only boundary geometry is controlled; all arithmetic/fit inputs are
        # explicit CPU fixtures, never empirical scientific evidence.
        H=make_h();H.GENERIC=['generic'];H.L1_PROMPTS=['l1'];H.L3_PROMPTS=['l3'];arm=A.A7
        distribution=torch.tensor([.5,.5]);W0=H.snap_layers(H.hp)
        H._ARM_STATE={'requests':[H.req(H.CANON,s,H.ARMS[arm][s]) for s in H.FICTION],
            'P':H.compute_P(H.hp),'pre_axes':{'L3':{'l3':{'id':0,'dist':distribution}}}}
        updates={l:torch.zeros_like(t).float() for l,t in W0.items()}
        reference={l:torch.tensor([[1. if l==4 else 0.]],dtype=torch.float64) for l in H.hp.layers}
        runtime={'pristine':W0,'pre_probes':{arm:{'frames':{},'frame_pre':{},'relation_templates':{},'relation_pre':{}}},
            'actual_A':{arm:reference},'actual_B':{'B-e2e':{arm:updates}},'raw_described_as':{arm:100.},
            'generic_samples':{'pre':[('generic',0.)],arm:[('generic',0.)]},
            'predictions':{arm:{'l1':{'id':0},'l3':{'id':0,'dist':distribution}}},
            'stored_checks':{arm:{}},'contexts':A.pinned_templates()}
        writer=types.SimpleNamespace(mode='apply_stored',stored={arm:updates},scale={arm:.5},last_trace={})
        fit={'f_ij':[[.95]*6 for _ in range(24)],'merged':True}
        for value in (0.99,1.01,0.989999,1.010001):
            rows=geometry([value,0.,0.,0.,0.])
            with mock.patch.object(A,'_covariances',return_value={}),mock.patch.object(A,'write_geometry',return_value=rows),mock.patch.object(A,'merged_fit',return_value=fit),mock.patch.object(A,'projector_gate',return_value=True):
                result=A.scientific_readouts(H,H.hp,arm,H.ARMS[arm],runtime,writer,'B-e2e-NM')
            with self.subTest(value=value): self.assertEqual(result['checks']['stored_geometry']['size_match'],value in (0.99,1.01))

    def test_later_stage_cannot_consume_stage1_calibration_measurements(self):
        record=calibration_timing_fixture(A.calibration_identity());path=self.root/'calibration.json';A.write_json(path,record)
        forecast=A.calibration_forecast(path,calibration_bounds_fixture(record));self.assertEqual(forecast['status'],'READY')
        for stage in (2,3):
            bad=copy.deepcopy(forecast);bad['stage']=stage
            with self.subTest(stage=stage): self.assertEqual(A.budget_gate(bad,9000.)['status'],'UNVERIFIED')

    def test_t8_overlap_audit_precedes_first_forward_and_never_redraws(self):
        H=make_h();H.PTEST[0]=A.pinned_templates()[1][0]
        out=self.root/'results/c10y_directdw_telemetry_inertness/leak'
        code=C.run(out,H,diagnostic=self.diagnostic)
        self.assertEqual(code,2);self.assertEqual(H.model.forward_inputs,[])
        diagnostic=A.strict_load(self.diagnostic);self.assertEqual(diagnostic['code'],'INVALID-LEAKAGE')
        self.assertEqual(diagnostic['context_templates']['sha256'],A.sha(out/'context_templates.json'))

    def test_supervisor_timeout_records_observed_template_hash_without_child(self):
        for stage in (1,'calibration',2):
            out=self.root/f'results/supervisor_stub_{stage}';diagnostic=self.root/f'architecture_profile/c10y_halt_diagnostic_stub_{stage}.json'
            name='context_templates_calib.json' if stage=='calibration' else 'context_templates.json'
            source=self.root/'results/stage1_context/context_templates.json'
            if stage==2: A.write_json(source,A.pinned_templates())
            def launch(*args,**kwargs):
                if stage!=2: A.write_json(out/name,A.pinned_templates())
                return types.SimpleNamespace(pid=54321,returncode=-15,poll=lambda:None,wait=lambda **kwargs:-15)
            argv=[sys.executable,'-B','isolated_stub.py']+(['--contexts',str(source)] if stage==2 else [])
            with mock.patch.object(A.subprocess,'Popen',side_effect=launch),mock.patch.object(A.os,'getpgid',return_value=54321),mock.patch.object(A.os,'getpgrp',return_value=12),mock.patch.object(A.os,'killpg') as kill,mock.patch.object(A,'STAGE_CLOCK',side_effect=[0.,2.]),mock.patch.object(A.time,'sleep'):
                value=A.supervise(argv,out,diagnostic,2.,stage,env=dict(os.environ,LLMDB_ROOT=str(self.root)))
            self.assertEqual(value['status'],'HALTED-BUDGET');kill.assert_called_once()
            actual=source if stage==2 else out/name;tag='calib' if stage=='calibration' else 's1' if stage==1 else 'p1'
            for file in (diagnostic,out/f'supervisor_{tag}.json'):
                self.assertEqual(A.strict_load(file).get('context_templates',{}).get('sha256'),A.sha(actual))

    def test_norm_readouts_are_inside_writer_wall_clock(self):
        for mode in ('e2e','anchor'):
            H=make_h();requests=[H.req(H.CANON,s,'Echo Echo') for s in H.FICTION]
            H.Z_OVERRIDE={(r['subject'],r['target_new']['str']):H.compute_z(H.model,H.tok,r,H.hp,8,H.get_context_templates(H.model,H.tok)) for r in requests}
            writer=A.Writer(H,H.hp);writer.baseline_passed=True;clock=[0.];norms=writer.norms
            def slow_norms(): clock[0]+=3.;return norms()
            with mock.patch.object(A,'STAGE_CLOCK',side_effect=lambda:clock[0]),mock.patch.object(writer,'norms',side_effect=slow_norms):
                writer.write(mode,requests,H.compute_P(H.hp),[torch.zeros(4,4) for _ in H.hp.layers],iterations=0)
            self.assertEqual(writer.last_trace['wall_clock_s'],3.)

    def test_real_iteration_producer_passes_c2_timing_validator(self):
        H=make_h();requests=[H.req(H.CANON,s,'Echo Echo') for s in H.FICTION]
        H.Z_OVERRIDE={(r['subject'],r['target_new']['str']):H.compute_z(H.model,H.tok,r,H.hp,8,H.get_context_templates(H.model,H.tok)) for r in requests}
        record=calibration_timing_fixture(A.calibration_identity());records=[];restore=H.snap_layers(H.hp)
        for prefix,lr in (('executed_loop',0.),('smoke',None)):
            H.restore_layers(H.hp,restore);writer=A.Writer(H,H.hp);writer.baseline_passed=True
            writer.write('e2e',requests,H.compute_P(H.hp),[torch.zeros(4,4) for _ in H.hp.layers],check=True,iterations=3,lr_override=lr,force_steps=True)
            for i,row in enumerate(writer.iteration_timings,1): records.append(dict(row,name=prefix+'_step',repetition=i,arm=A.A7,mode='e2e'))
            for row in writer.phase_timings: records.append(dict(row,name=prefix+'_'+row['name'],arm=A.A7,mode='e2e'))
        names={row['name'] for row in records};record['timings']=[row for row in record['timings'] if row['name'] not in names]+records
        record['timings']=A.calibration_timing_tags(record['timings']);record['T_cal']=max(n for row in records for n in row['workload'].get('padded_lengths',[]))
        checked=A._calibration_timings(record,A.calibration_identity())
        rows,lower=A._calibration_phase(checked,calibration_bounds_fixture(record)[A.FORECAST_PHASES.index('optimisation')])
        self.assertEqual(sum(row.get('accepted',False) for row in rows),6);self.assertGreaterEqual(lower,105*max(row['seconds'] for row in rows))

class AttentionMaskTests(IsolatedCase):
    def test_owned_forwards_preserve_original_mask_contract(self):
        count = 0
        for module in (A, R, C):
            tree = ast.parse(Path(module.__file__).read_text())
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                name = ast.unparse(node.func)
                if name != 'model' and not name.endswith(('.model', '.forward')):
                    continue
                count += 1
                masks = [keyword.value for keyword in node.keywords if keyword.arg == 'attention_mask']
                with self.subTest(file=Path(module.__file__).name, line=node.lineno, call=name):
                    if node.args and isinstance(node.args[0], ast.Name) and node.args[0].id == 'cur':
                        self.assertEqual(masks, [], 'frozen greedy-call kwargs must stay unchanged')
                    else:
                        self.assertEqual(len(masks), 1, 'preserve the already forwarded tokenizer attention_mask')
                        self.assertFalse(isinstance(masks[0], ast.Constant) and masks[0].value is None)
        self.assertEqual(count, 14, 'review any new or removed model call site')

    def test_single_sequence_decode_and_observed_scorer_do_not_inject_mask(self):
        H = make_h()
        prompt = H.CANON.format(H.FICTION[0])
        original = H.model.forward
        masks = []
        def checked(input_ids, *args, **kwargs):
            self.assertNotIn('attention_mask', kwargs, 'the original greedy reference must not inject kwargs')
            masks.append(input_ids.shape)
            return original(input_ids, *args, **kwargs)
        W0 = H.snap_layers(H.hp)
        operators = ({layer: torch.zeros(4, 1) for layer in H.hp.layers},
                     {layer: torch.zeros(1, 4) for layer in H.hp.layers}, W0)
        for mode in ('plain', 'hooked', 'observed'):
            with self.subTest(mode=mode), mock.patch.object(H.model, 'forward', side_effect=checked):
                masks.clear()
                if mode == 'observed':
                    A.make_scorer(H, lambda *args: None)(prompt, H.tgt_ids('Echo Echo'))
                else:
                    A._decode_ids(H, prompt, 2, H.hp, operators if mode == 'hooked' else None)
                self.assertEqual(len(masks), 2)
                self.assertEqual(masks[1][1], masks[0][1] + 1)

    def test_padded_objective_and_lens_preserve_tokenizer_attention_mask(self):
        H = make_h()
        requests = [H.req(H.CANON, H.FICTION[i], target)
                    for i, target in enumerate(('Echo', 'Echo Echo'))]
        batches = [A.request_batch(H, request, A.pinned_templates()) for request in requests]
        tokens, _, _, _ = A.packed_batches(H, batches)
        self.assertTrue(bool((tokens['attention_mask'] == 0).any()), 'positive padding control')
        original = H.model.model.forward
        def checked(input_ids, *args, **kwargs):
            self.assertTrue(torch.equal(kwargs['attention_mask'], tokens['attention_mask']))
            return original(input_ids, *args, **kwargs)
        with mock.patch.object(H.model.model, 'forward', side_effect=checked):
            A.edit_components(H, batches, None)
        forward = H.model.forward
        seen = []
        def lens_checked(input_ids, *args, **kwargs):
            self.assertTrue(torch.equal(kwargs['attention_mask'], torch.ones_like(input_ids)))
            seen.append(input_ids.shape)
            return forward(input_ids, *args, **kwargs)
        telem = A.Telemetry(self.out, 'mask', 'fixed')
        with mock.patch.object(H.model, 'forward', side_effect=lens_checked):
            telem.logit_lens(H, H.hp, 'mask-test')
        self.assertTrue(telem.enabled)
        self.assertEqual(len(seen), 24)
        telem.close()

    def test_observed_scorer_rejects_any_added_forward_keyword(self):
        for keyword, wrong in (('attention_mask', 'torch.ones_like(cur)'),
                               ('attention_mask', 'torch.zeros_like(cur)'), ('use_cache', 'False')):
            tree = ast.parse(Path(A.__file__).read_text())
            scorer = next(node for node in ast.walk(tree)
                          if isinstance(node, ast.FunctionDef) and node.name == 'full_seq_match')
            call = next(node for node in ast.walk(scorer)
                        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id == 'model')
            call.keywords = [ast.keyword(arg=keyword, value=ast.parse(wrong, mode='eval').body)]
            path = self.root / (keyword + '_' + str(len(wrong)) + '.py')
            path.write_text(ast.unparse(ast.fix_missing_locations(tree)))
            with self.subTest(wrong=wrong), mock.patch.object(A, '__file__', str(path)):
                self.assertFalse(A.scorer_ast_check(W / 'code/lab/track_c/c10e_bandknob.py'))

def _combined_to_calls(source):
    result = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute) or node.func.attr != 'to':
            continue
        keys = {keyword.arg for keyword in node.keywords}
        second_is_flag = (len(node.args) >= 2 and isinstance(node.args[1], ast.Constant)
                          and isinstance(node.args[1].value, bool))
        if ({'device', 'dtype'} <= keys or bool(node.args) and ('device' in keys or 'dtype' in keys)
                or len(node.args) >= 2 and not second_is_flag):
            result.append((node.lineno, ast.unparse(node)))
    return result


def _unsafe_cpu_transfers(source):
    tree = ast.parse(source)
    result = list(_combined_to_calls(source))
    cpu_buffers = {}
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    def owner(node):
        while node in parents and not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            node = parents[node]
        return node
    def cpu_device(node):
        if isinstance(node, ast.Call) and ast.unparse(node.func) == 'torch.device' and node.args:
            node = node.args[0]
        return isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.split(':', 1)[0] == 'cpu'
    def cpu_first(node):
        if isinstance(node, ast.IfExp): return cpu_first(node.body) and cpu_first(node.orelse)
        if isinstance(node, ast.Subscript): return cpu_first(node.value)
        if not isinstance(node, ast.Call): return False
        if isinstance(node.func, ast.Name): return node.func.id == 'cpu64'
        if not isinstance(node.func, ast.Attribute): return False
        name = node.func.attr
        if name == 'cpu': return True
        if name == 'to':
            device = next((keyword.value for keyword in node.keywords if keyword.arg == 'device'), None)
            if device is not None: return cpu_device(device)
            if node.args:
                target = node.args[0]
                if isinstance(target, ast.Constant) and isinstance(target.value, str): return cpu_device(target)
                if isinstance(target, ast.Call) and ast.unparse(target.func) == 'torch.device': return cpu_device(target)
                if not (isinstance(target, ast.Attribute) and (target.attr == 'dtype'
                        or isinstance(target.value, ast.Name) and target.value.id == 'torch')): return False
            return cpu_first(node.func.value)
        if name in {'detach', 'clone', 'contiguous', 'float', 'half', 'double', 'reshape', 'view'}:
            return cpu_first(node.func.value)
        if ast.unparse(node.func) in {'torch.tensor', 'torch.as_tensor', 'torch.empty', 'torch.zeros', 'torch.ones', 'torch.full'}:
            device = next((keyword.value for keyword in node.keywords if keyword.arg == 'device'), None)
            return cpu_device(device)
        return False
    def literal_data(node):
        try:
            ast.literal_eval(node); return True
        except (ValueError, TypeError):
            return False
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and cpu_first(node.value):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            cpu_buffers.setdefault(owner(node), set()).update(target.id for target in targets if isinstance(target, ast.Name))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            call = ast.unparse(node)
            if node.func.attr == 'to':
                if any(keyword.arg is None or keyword.arg == 'other' for keyword in node.keywords):
                    result.append((node.lineno, call))
            if node.func.attr == 'to' and node.args:
                target = node.args[0]
                safe = (isinstance(target, ast.Constant) and isinstance(target.value, str)
                        or isinstance(target, ast.Name) and target.id in {'dev', 'DEV', 'device', 'dtype'}
                        or isinstance(target, ast.Attribute) and target.attr in {'device', 'dtype', 'DEV'}
                        or isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'torch'
                        or isinstance(target, ast.Call) and ast.unparse(target.func) == 'torch.device')
                if not safe: result.append((node.lineno, call))
            if node.func.attr in {'type', 'type_as'} and not cpu_first(node.func.value):
                result.append((node.lineno, call))
            if node.func.attr == 'copy_':
                value = node.args[0] if node.args else None
                aligned = (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
                           and value.func.id == 'to_like' and len(value.args) == 2
                           and ast.dump(value.args[1]) == ast.dump(node.func.value))
                if not aligned: result.append((node.lineno, call))
            if ast.unparse(node.func) in {'torch.tensor', 'torch.as_tensor'}:
                keys = {keyword.arg for keyword in node.keywords}
                data = node.args[0] if node.args else next((keyword.value for keyword in node.keywords if keyword.arg == 'data'), None)
                if None in keys or ({'device', 'dtype'} <= keys and data is not None
                                    and not literal_data(data) and not cpu_first(data)):
                    result.append((node.lineno, call))
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                root = target
                while isinstance(root, ast.Subscript): root = root.value
                if (isinstance(target, ast.Subscript) and isinstance(root, ast.Name)
                        and (root.id in cpu_buffers.get(owner(node), set()) or root.id.startswith(('cpu_', 'host_')))
                        and not literal_data(node.value) and not cpu_first(node.value)):
                    result.append((node.lineno, ast.unparse(node)))
    return sorted(set(result))


class DeviceConversionTests(IsolatedCase):
    def test_no_combined_device_dtype_transfer_in_owned_runtime(self):
        self.maxDiff = None
        for module in (A, R, C):
            with self.subTest(file=Path(module.__file__).name):
                self.assertEqual(_unsafe_cpu_transfers(Path(module.__file__).read_text()), [],
                                 'copy device first, then change dtype; MPS views can corrupt combined transfers')

    def test_ast_rejects_keyword_positional_and_mixed_combined_transfers(self):
        bad = ("t.to(device='cpu', dtype=torch.float32)",
               "t.to(dtype=torch.float64, device=torch.device('cpu'))",
               "t.to('cpu', torch.float32)", "t.to(torch.device('cpu'), t.dtype)",
               "t.to('cpu', dtype=torch.float32)", "t.to(dest.device, dest.dtype)",
               "t.clone().to('cpu', torch.float16)", "t.contiguous().to('cpu', torch.float32)",
               "v.to(cpu_tensor)", "v.type(torch.FloatTensor)", "v.type_as(cpu_tensor)",
               "cpu_buf.copy_(v)", "cpu_buf[0] = v",
               "buf = torch.empty(4, device='cpu', dtype=torch.float32)\nbuf[0] = v",
               "torch.as_tensor(v, device='cpu', dtype=torch.float32)",
               "torch.tensor(v.clone(), device='cpu', dtype=torch.float16)",
               "buf = torch.empty(4, device=torch.device('cpu'), dtype=torch.float32)\nbuf[0] = v",
               "buf: object = torch.empty(4, device='cpu', dtype=torch.float32)\nbuf[0] = v",
               "v.to(cpu_tensor, non_blocking=True)", "v.to(cpu_tensor, True)", "v.to(**options)",
               "cpu_buf[0] = v if flag else other.cpu()",
               "torch.as_tensor(v.cpu().to('mps'), device='cpu', dtype=torch.float16)",
               "torch.as_tensor(data=v, device='cpu', dtype=torch.float32)",
               "torch.tensor(data=v, device='cpu', dtype=torch.float16)", "torch.as_tensor(**options)")
        for expression in bad:
            with self.subTest(expression=expression):
                self.assertGreaterEqual(len(_unsafe_cpu_transfers(expression)), 1)
        good = ("t.cpu().to(dtype=torch.float32)", "t.to('cpu').to(torch.float64)",
                "t.float().cpu()", "t.to(device='cpu')", "t.to(dtype=torch.float32)",
                "t.to(torch.float32, True)", "torch.as_tensor(v.cpu(), device='cpu', dtype=torch.float32)",
                "torch.tensor([1., 2.], device='cpu', dtype=torch.float32)",
                "buf.copy_(to_like(v, buf))", "cpu_buf[0] = v.cpu().to(torch.float32)",
                "torch.as_tensor(data=v.cpu(), device='cpu', dtype=torch.float32)",
                "torch.tensor(data=[1., 2.], device='cpu', dtype=torch.float32)")
        for expression in good:
            with self.subTest(expression=expression):
                self.assertEqual(_unsafe_cpu_transfers(expression), [])

    def test_reachable_helpers_only_combine_recorded_cpu_solve_transfer(self):
        paths = sorted((W / 'code/memit/vendor').glob('memit/**/*.py'))
        paths += sorted((W / 'code/memit/vendor').glob('rome/**/*.py'))
        paths += sorted((W / 'code/memit/vendor').glob('util/**/*.py'))
        self.assertGreater(len(paths), 20, 'positive source inventory control')
        for path in paths:
            with self.subTest(file=str(path.relative_to(W))):
                self.assertEqual(_combined_to_calls(path.read_text()), [])
        path = W / 'code/lab/track_c/c10e_bandknob.py'
        calls = _combined_to_calls(path.read_text())
        self.assertEqual([call for _, call in calls],
                         ['upd.to(npd[weight_name(hp, layer)].device, npd[weight_name(hp, layer)].dtype)'])
        function = next(node for node in ast.parse(path.read_text()).body
                        if isinstance(node, ast.FunctionDef) and node.name == 'my_edit')
        source = ast.unparse(function)
        self.assertIn('A = Pi @ (Kf.cpu() @ Kf.cpu().T + ca) + L2 * torch.eye(Kf.shape[0])', source)
        self.assertIn('B = Pi @ Kf.cpu() @ rf.cpu().T', source)
        self.assertIn('upd = torch.linalg.solve(A, B).T', source)
        self.assertLess(source.index('upd = torch.linalg.solve(A, B).T'), source.index(calls[0][1]))

    def test_cpu64_copies_offset_view_before_dtype_cast(self):
        data = torch.arange(30, dtype=torch.float16).reshape(5, 6)[1:4, 1:5]
        self.assertGreater(data.storage_offset(), 0)
        self.assertFalse(data.is_contiguous())
        calls = []
        class View:
            device = types.SimpleNamespace(type='mps')
            dtype = torch.float16
            def detach(self):
                calls.append('detach'); return self
            def cpu(self):
                calls.append('cpu'); return data.clone()
            def to(self, *args, **kwargs):
                raise AssertionError('combined device/dtype transfer entered the fake MPS view')
            def double(self):
                raise AssertionError('dtype changed before copying fake MPS view to CPU')
        result = A.cpu64(View())
        self.assertEqual(calls, ['detach', 'cpu'])
        self.assertEqual(result.device.type, 'cpu')
        self.assertEqual(result.dtype, torch.float64)
        self.assertTrue(torch.equal(result, data.double()))

    def test_stored_weight_aligns_device_before_scale_and_fp16_add(self):
        moves = []
        class Labeled:
            def __init__(self, value, device):
                self.value = value
                self.device = types.SimpleNamespace(type=device)
                self.dtype = value.dtype
            def detach(self): return self
            def half(self): return Labeled(self.value.half(), self.device.type)
            def float(self): return Labeled(self.value.float(), self.device.type)
            def to(self, destination, **kwargs):
                selftest.assertEqual(kwargs, {}, 'device alignment must not combine a dtype cast')
                moves.append((self.device.type, destination.type))
                return Labeled(self.value.clone(), destination.type)
            def __mul__(self, scale): return Labeled(self.value * scale, self.device.type)
            def __add__(self, other):
                selftest.assertEqual(self.device.type, other.device.type, 'stored update must align before matrix addition')
                return Labeled(self.value + other.value, self.device.type)
        selftest = self
        base = torch.tensor([[1.0004, -.231], [.4998, 3.1]], dtype=torch.float32)
        update = torch.tensor([[.0007, .49], [-.231, .0017]], dtype=torch.float32)
        for destination, origin in (('mps', 'cpu'), ('cpu', 'mps'), ('mps', 'mps'), ('cpu', 'cpu')):
            for scale in (0., .4, 1.):
                with self.subTest(destination=destination, origin=origin, scale=scale):
                    moves.clear()
                    result = A.stored_weight(Labeled(base, destination), Labeled(update, origin), scale)
                    self.assertEqual(moves, [(origin, destination)])
                    self.assertEqual(result.device.type, destination)
                    self.assertEqual(result.dtype, torch.float16)
                    self.assertTrue(torch.equal(result.value, (base.half() + (update.float() * scale).half()).half()))
                    self.assertEqual(result.value.device.type, 'cpu', 'all fixture arithmetic must stay on CPU')

    def test_to_like_transfers_before_casting_offset_view(self):
        self.assertTrue(hasattr(A, 'to_like'), 'a tensor-target conversion must separate its operations')
        data = torch.arange(12, dtype=torch.float16)[3:9]
        calls = []
        class View:
            def to(self, *, device=None, dtype=None):
                selftest.assertFalse(device is not None and dtype is not None)
                calls.append(('device', device.type) if device is not None else ('dtype', dtype))
                return Converted() if device is not None else None
        class Converted:
            def to(self, *, dtype):
                calls.append(('dtype', dtype)); return data.to(dtype)
        selftest = self
        reference = types.SimpleNamespace(device=torch.device('cpu'), dtype=torch.float32)
        result = A.to_like(View(), reference)
        self.assertEqual(calls, [('device', 'cpu'), ('dtype', torch.float32)])
        self.assertTrue(torch.equal(result, data.float()))


class TelemetryReferenceTests(IsolatedCase):
    def test_frozen_harness_scorers_receive_no_injected_kwargs(self):
        H = make_h()
        names = ('full_seq_match', 'string_match', 'teacher_forced_pertok', 'sentence_nll')
        source = ast.parse((W / 'code/lab/track_c/c10e_bandknob.py').read_text())
        functions = [copy.deepcopy(node) for node in source.body
                     if isinstance(node, ast.FunctionDef) and node.name in names]
        self.assertEqual(len(functions), 4)
        scope = {'torch': torch, 'tok': H.tok, 'model': H.model, 'DEV': H.DEV}
        exec(compile(ast.Module(body=functions, type_ignores=[]), '<frozen CPU scorer fixtures>', 'exec'), scope)
        for name in names: setattr(H, name, scope[name])
        originals = {name: getattr(H, name) for name in names}
        hooks = A.hook_snapshot(H.model); forward = H.model.forward; calls = []
        def checked(input_ids, *args, **kwargs):
            self.assertEqual(kwargs, {}, 'frozen scorers must receive no injected model kwargs')
            calls.append(input_ids.shape)
            return forward(input_ids, *args, **kwargs)
        def recipe(*args):
            subject = H.FICTION[0]; value = H.ARMS[A.A7][subject]
            H._ARM_STATE = {'requests': [H.req(H.CANON, subject, value)]}
            prompt = H.CANON.format(subject); ids = H.tgt_ids(value)
            H.full_seq_match(prompt, ids)
            H.string_match(prompt, value, len(ids))
            H.teacher_forced_pertok(prompt, ids)
            H.sentence_nll(prompt)
            return {'arms': {A.A7: {}}}
        H.run_recipe = recipe
        for enabled in (False, True):
            telemetry = A.Telemetry(self.out, 'on', 'fixed') if enabled else None
            with self.subTest(telemetry=enabled), mock.patch.object(H.model, 'forward', side_effect=checked), \
                 mock.patch.object(A, 'normalize_recipe', side_effect=lambda raw, *args: raw):
                calls.clear()
                A.scored_recipe(H, 'B-e2e', H.HP_BASE, 1, telemetry)
                self.assertEqual(len(calls), 8)
                self.assertTrue(telemetry is None or telemetry.enabled)
            if telemetry is not None: telemetry.close()
            for name, original in originals.items(): self.assertIs(getattr(H, name), original)
            self.assertEqual(A.hook_snapshot(H.model), hooks)

    def test_reference_scorer_is_exact_frozen_capture_copy(self):
        import builtins
        H = make_h(); trees = []; captured = []; masks = []
        def compile_reference(tree, filename, mode):
            trees.append(copy.deepcopy(tree))
            return builtins.compile(tree, filename, mode)
        original = H.model.forward
        def forward(input_ids, *args, **kwargs):
            masks.append(kwargs.get('attention_mask'))
            return original(input_ids, *args, **kwargs)
        with mock.patch.object(A, 'compile', side_effect=compile_reference, create=True):
            scorer = A.make_scorer(H, lambda prompt, ids, gen: captured.append((list(ids), list(gen))), reference=True)
        self.assertEqual(len(trees), 1, 'reference must compile the exact frozen function, not the observed copy')
        expected = next(node for node in ast.parse((W / 'code/lab/track_c/c10e_bandknob.py').read_text()).body
                        if isinstance(node, ast.FunctionDef) and node.name == 'full_seq_match')
        actual = trees[0].body[0]
        self.assertEqual(ast.dump(actual.body[-2]), ast.dump(ast.parse('sink(prompt,target_ids,gen)').body[0]))
        actual.body.pop(-2)
        self.assertEqual(ast.dump(actual), ast.dump(expected))
        ids = H.tgt_ids('Echo Echo')
        with mock.patch.object(H.model, 'forward', side_effect=forward):
            flags = scorer(H.CANON.format(H.FICTION[0]), ids)
        self.assertEqual(len(masks), len(ids)); self.assertTrue(all(mask is None for mask in masks))
        self.assertEqual(len(captured), 1)
        self.assertEqual(flags, (captured[0][1] == ids, captured[0][1][0] == ids[0]))
        self.assertTrue(all(parameter.device.type == 'cpu' for parameter in H.model.parameters()))

    def test_t8_uses_frozen_off_reference_and_observed_on_scorer(self):
        H = make_h(); modes = []; make = A.make_scorer
        def tracked(*args, **kwargs):
            modes.append(kwargs.get('reference', False))
            return make(*args, **kwargs)
        with mock.patch.object(A, 'make_scorer', side_effect=tracked):
            record = A.telemetry_mps_inertness_check(self.out, H)
        self.assertEqual(modes, [False, True, False, True], 'warmup, P1, T, P2 must select their actual scorer semantics')
        self.assertEqual(record['verdict'], 'INERT', 'controlled CPU fixture only')
        self.assertTrue(record['serialized_answers_equal'])
        self.assertEqual(record['answer_calls'], 96)


class CalibrationErrorTests(IsolatedCase):
    """Program calibration failure: real structure contracts and causal diagnostics."""

    def records(self):
        return CalibrationTests.records(self)

    def phase(self, budget, name):
        return getattr(A, 'phase_context', lambda *args: contextlib.nullcontext())(budget, name)

    def raise_fixture(self, error):
        raise error

    def assert_failure(self, diagnostic, run, phase, text, exception='ValueError'):
        self.assertEqual(diagnostic.get('phase'), phase)
        self.assertEqual(run.get('phase'), phase)
        self.assertEqual(diagnostic.get('exception'), exception)
        self.assertEqual(run.get('exception'), exception)
        trace = diagnostic.get('traceback', '')
        self.assertIn('Traceback (most recent call last):', trace)
        self.assertIn('raise_fixture', trace)
        self.assertIn(text, trace)
        self.assertEqual(run.get('traceback'), trace)

    def test_pristine_probe_canonical_and_three_heldout_real_representation_pair(self):
        (self.root/'code/lab/track_c/c10p_twopass_arms.py').write_bytes(
            (W/'code/lab/track_c/c10p_twopass_arms.py').read_bytes())
        H=make_h();requests=[H.req(H.CANON,s,H.ARMS[A7][s]) for s in H.FICTION]
        predictions=[];representations=[];reps=H.get_module_input_output_at_words
        def predict(prompt):
            predictions.append(prompt)
            batch=H.tok(prompt,return_tensors='pt')
            with torch.no_grad(): distribution=H.model(**batch).logits[0,-1].float().softmax(-1)
            return {'id':int(distribution.argmax()),'dist':distribution.cpu()}
        H.predict=predict
        templates={'canonical':H.CANON,**{'heldout%d'%i:p for i,p in enumerate(H.PTEST)}}
        expected={key:reps(H.model,H.tok,8,[template]*24,H.FICTION,
                          H.hp.layer_module_tmp,H.hp.fact_token)[1].T.detach().cpu()
                  for key,template in templates.items()}
        def record(*args,**kwargs):
            representations.append(kwargs['context_templates'][0]);return reps(*args,**kwargs)
        H.get_module_input_output_at_words=record
        try: value=A._probe_pristine(H,H.hp,requests,A.pinned_templates())
        except ValueError:
            self.fail(__import__('traceback').format_exc())
        self.assertEqual(set(value['frames']),{'CANON',*('frame%d'%i for i in range(6))})
        self.assertEqual(len(predictions),90)
        self.assertEqual(representations,list(templates.values()))
        self.assertEqual(list(value['anchor_pre']),list(templates))
        for key in templates:
            self.assertEqual(tuple(value['anchor_pre'][key].shape),(4,24))
            self.assertTrue(torch.equal(value['anchor_pre'][key],expected[key]))
        self.assertTrue(all(len(rows)==6 for rows in value['frame_pre'].values()))
        # Actual default Qwen2DecoderLayer output is a single hidden-state tuple.
        self.assertEqual(len(H.model.model.layers[8](torch.ones(3,5,4).half())),1)

    def test_remaining_readout_canonical_and_three_heldout_real_pair(self):
        H=make_h();requests=[H.req(H.CANON,s,H.ARMS[A7][s]) for s in H.FICTION]
        target=torch.arange(1,97,dtype=torch.float64).reshape(4,24)
        targets={key:target[:,i] for i,key in enumerate(A._request_keys(requests))}
        templates=[H.CANON,*H.PTEST];keys=['canonical',*('heldout%d'%i for i in range(3))]
        ratios=[.25,.5,.75,1.];pre={key:target-(i+1) for i,key in enumerate(keys)};calls=[]
        def reps(model,tok,layer,context_templates,words,**kwargs):
            i=templates.index(context_templates[0]);calls.append(context_templates[0])
            self.assertEqual(len(words),24);self.assertEqual(layer,8)
            now=(target-(i+1)*ratios[i]).T
            return torch.zeros_like(now),now
        H.get_module_input_output_at_words=reps
        try: value=A._remaining_readout(H,H.hp,requests,targets,pre)
        except ValueError:
            self.fail(__import__('traceback').format_exc())
        self.assertEqual(calls,templates)
        self.assertAlmostEqual(value['canonical'],ratios[0],delta=1e-12)
        for actual,expected in zip(value['heldout'],ratios[1:]): self.assertAlmostEqual(actual,expected,delta=1e-12)
        self.assertEqual(list(value['denominator_norms']),keys)
        for i,key in enumerate(keys):
            self.assertAlmostEqual(value['denominator_norms'][key],(i+1)*math.sqrt(96),delta=1e-12)

    def test_calibration_valueerror_and_halt_trace_phase_persist(self):
        for i,error in enumerate((ValueError('calibration fixture'),A.Halt('TEST-HALT','deliberate'))):
            with self.subTest(error=type(error).__name__):
                go,spend=self.records();out=self.root/('results/c10y_directdw_calib%d'%(i+1))
                diagnostic=self.root/('architecture_profile/halt%d.json'%i);H=make_h()
                def prefix(H,out,budget,**kwargs):
                    return A._unit(H,[],'failing_prefix',A._workload(),lambda:self.raise_fixture(error),budget=budget)
                with mock.patch.object(A,'instrument_prefix',side_effect=prefix):
                    result=A.calibrate(out,H,go=go,spend=spend,diagnostic=diagnostic)
                saved=A.strict_load(diagnostic);run=A.strict_load(out/'run.json')
                self.assert_failure(saved,run,'failing_prefix',str(error),type(error).__name__)
                self.assertEqual(result.get('traceback'),saved['traceback'])
                self.assertEqual(result.get('phase'),'failing_prefix')
                self.assertEqual(A.calibration_forecast(out/'calibration.json',[])['status'],'UNVERIFIED')

    def test_calibration_context_failure_is_not_prefix_phase(self):
        go,spend=self.records();out=self.root/'experiments/c10y/runs/c10y_directdw_calib1'
        def freeze(*args,**kwargs): self.raise_fixture(ValueError('context fixture'))
        with mock.patch.object(A,'freeze_contexts',side_effect=freeze):
            A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
        self.assert_failure(A.strict_load(self.diagnostic),A.strict_load(out/'run.json'),
                            'contexts_install','context fixture')

    def test_stage_valueerror_and_halt_trace_phase_persist(self):
        for i,error in enumerate((ValueError('stage fixture'),A.Halt('TEST-HALT'))):
            with self.subTest(error=type(error).__name__):
                H=make_h();go={'decision_id':'D-go','experiment':'C10Y','stage':1,'recorded_in':'test','at':'UTC'}
                out=self.out if i==0 else self.root/'results/c10y_directdw_s1_rerun1'
                replacement=None if i==0 else {'replaces':str(self.out),'cause':'deliberate fixture'}
                diagnostic=self.root/('architecture_profile/stage%d.json'%i)
                def prefix(H,out,budget,**kwargs):
                    return A._unit(H,[],'stage_check',A._workload(),lambda:self.raise_fixture(error),budget=budget)
                with mock.patch.object(A,'instrument_prefix',side_effect=prefix):
                    result=A.run(out,H,go=go,forecast=replacement_stage_forecast(self,1),
                                 diagnostic=diagnostic,replacement=replacement)
                self.assert_failure(A.strict_load(diagnostic),A.strict_load(out/'run.json'),
                                    'stage_check',str(error),type(error).__name__)
                self.assertEqual(result['run']['traceback'],A.strict_load(diagnostic)['traceback'])
                self.assertEqual(result['reading']['label'],'HALTED')

    def test_nested_phase_retains_failure_and_restores_success_parent(self):
        H=make_h();budget=A.Budget(0,1e9,1);budget.phase='parent'
        def inner(): self.raise_fixture(ValueError('inner failure'))
        try: A._unit(H,[],'outer',A._workload(),lambda:A._unit(H,[],'inner',A._workload(),inner,budget=budget),budget=budget)
        except ValueError as error:
            self.assertEqual(getattr(error,'_c10y_phase',None),'inner')
        else: self.fail('missing fixture exception')
        self.assertEqual(budget.phase,'parent')
        def outer():
            A._unit(H,[],'successful_inner',A._workload(),lambda:42,budget=budget)
            self.assertEqual(budget.phase,'later_outer')
            self.raise_fixture(ValueError('later failure'))
        try: A._unit(H,[],'later_outer',A._workload(),outer,budget=budget)
        except ValueError as error:
            self.assertEqual(getattr(error,'_c10y_phase',None),'later_outer')
        else: self.fail('missing later fixture exception')
        self.assertEqual(budget.phase,'parent')

    def test_primary_error_phase_survives_cleanup_failure(self):
        go,spend=self.records();out=self.root/'experiments/c10y/runs/c10y_directdw_calib1';calls=[]
        def sync(H):
            calls.append(1)
            if len(calls)==2: raise OSError('cleanup failure')
        def prefix(H,out,budget,**kwargs):
            return A._unit(H,[],'primary_action',A._workload(),lambda:self.raise_fixture(ValueError('primary failure')),budget=budget)
        with mock.patch.object(A,'instrument_prefix',side_effect=prefix),mock.patch.object(A,'sync',side_effect=sync):
            A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
        saved=A.strict_load(self.diagnostic);run=A.strict_load(out/'run.json')
        self.assert_failure(saved,run,'primary_action','primary failure')
        self.assertIn('cleanup failure',saved['traceback'])
        self.assertEqual(saved.get('cleanup',{}).get('exception'),'OSError')

    def test_telemetry_halt_and_instrument_error_trace_phase(self):
        for i,error in enumerate((A.Halt('TEST-HALT'),ValueError('telemetry fixture'))):
            with self.subTest(error=type(error).__name__):
                out=self.root/('results/c10y_directdw_telemetry_inertness/error%d'%i)
                diagnostic=self.root/('architecture_profile/check%d.json'%i)
                C.ROOT=self.root
                def action(*args,**kwargs): self.raise_fixture(error)
                with mock.patch.object(A,'telemetry_mps_inertness_check',side_effect=action):
                    try: code=C.run(out,make_h(),fingerprint=lambda:TelemetryCheckContract._fingerprint(self),diagnostic=diagnostic)
                    except ValueError:
                        self.fail(__import__('traceback').format_exc())
                self.assertEqual(code,2)
                self.assert_failure(A.strict_load(diagnostic),A.strict_load(out/'inertness.json'),
                                    'telemetry_inertness',str(error),type(error).__name__)
                self.assertEqual(A.strict_load(out/'inertness.json')['verdict'],'INVALID')

    def test_main_unadmitted_preflight_error_has_trace_and_phase_without_writes(self):
        go=self.root/'go.json';go.write_text('{}');stream=io.StringIO()
        def fail(): self.raise_fixture(ValueError('startup fixture'))
        with mock.patch.object(A,'preflight',side_effect=fail),contextlib.redirect_stderr(stream):
            code=A.main(['--stage','1','--out',str(self.out),'--halt-diagnostic',str(self.diagnostic),'--go',str(go)])
        self.assertEqual(code,2)
        self.assertIn('Traceback (most recent call last):',stream.getvalue())
        self.assertIn('raise_fixture',stream.getvalue());self.assertIn('preflight',stream.getvalue())
        self.assertFalse(self.out.exists());self.assertFalse(self.diagnostic.exists())

    def test_calibration_publication_error_surfaces_phase(self):
        go,spend=self.records();out=self.root/'experiments/c10y/runs/c10y_directdw_calib1';publish=A.write_json
        def fail(path,value):
            if Path(path).name=='run.json': self.raise_fixture(OSError('publication fixture'))
            return publish(path,value)
        with mock.patch.object(A,'instrument_prefix',return_value=CalibrationTests.fixture(self)),mock.patch.object(A,'write_json',side_effect=fail):
            try: A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
            except OSError as error:
                self.assertEqual(getattr(error,'_c10y_phase',None),'calibration_publication')
            else: self.fail('publication error was swallowed')
        self.assertFalse((out/'run.json').exists())

    def test_supervisor_worker_exit_before_handoff_is_diagnosed(self):
        out=self.root/'experiments/c10y/runs/c10y_directdw_calib1'
        proc=types.SimpleNamespace(pid=123456,returncode=2,poll=lambda:2)
        with mock.patch.object(A.subprocess,'Popen',return_value=proc),mock.patch.object(A.os,'getpgid',return_value=proc.pid):
            A.supervise([sys.executable,'-B',str(self.root/'stub.py')],out,self.diagnostic,7200.,'calibration')
        self.assertTrue(self.diagnostic.is_file(),'missing supervisor diagnostic')
        saved=A.strict_load(self.diagnostic)
        self.assertEqual(saved.get('phase'),'worker_exit')
        self.assertIsNone(saved.get('traceback'))
        self.assertTrue(saved.get('traceback_unavailable'))
        self.assertEqual(A.strict_load(out/'run.json').get('phase'),'worker_exit')

    def test_supervisor_preserves_worker_original_trace_and_outcome(self):
        out=self.root/'experiments/c10y/runs/c10y_directdw_calib1';proc=types.SimpleNamespace(pid=123456,returncode=2,poll=lambda:2)
        worker={'schema':'c10y_directdw_calibration/v1','outcome':'INSTRUMENT-ERROR','timings':[],
                'phase':'baseline_pristine_probes','exception':'ValueError','traceback':'Traceback (most recent call last):\nfixture original trace\nValueError: original'}
        def launch(*args,**kwargs):
            A.write_json(out/'calibration_worker.json',worker)
            A.write_json(self.diagnostic,worker)
            A.write_json(out/'run.json',dict(worker,status='INSTRUMENT-ERROR'))
            return proc
        with mock.patch.object(A.subprocess,'Popen',side_effect=launch),mock.patch.object(A.os,'getpgid',return_value=proc.pid):
            A.supervise([sys.executable,'-B',str(self.root/'stub.py')],out,self.diagnostic,7200.,'calibration')
        final=A.strict_load(out/'calibration.json')
        self.assertEqual(final['outcome'],'INSTRUMENT-ERROR')
        self.assertEqual(final['traceback'],worker['traceback']);self.assertEqual(final['phase'],worker['phase'])
        self.assertEqual(A.strict_load(self.diagnostic),worker)

    def test_primary_law3_halt_survives_cleanup_and_latches_schedule(self):
        go,spend=self.records();out=self.root/'experiments/c10y/runs/c10y_directdw_calib1';calls=[]
        def sync(H):
            calls.append(1)
            if len(calls)==2: raise OSError('halt cleanup failure')
        def prefix(H,out,budget,**kwargs):
            return A._unit(H,[],'law3',A._workload(),lambda:self.raise_fixture(A.Halt('LAW#3','baseline failure')),budget=budget)
        with mock.patch.object(A,'instrument_prefix',side_effect=prefix),mock.patch.object(A,'sync',side_effect=sync):
            record=A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
        self.assertEqual(record['outcome'],'LAW#3')
        self.assertEqual(A.strict_load(self.diagnostic)['code'],'LAW#3')
        self.assert_failure(A.strict_load(self.diagnostic),A.strict_load(out/'run.json'),
                            'law3','baseline failure','Halt')
        self.assertEqual(A.strict_load(self.root/'results/c10y_directdw_schedule_halt.json')['code'],'LAW#3')

    def test_nonzero_child_exit_overrides_prepublished_success_authority(self):
        for stage in ('calibration',1):
            with self.subTest(stage=stage):
                out=self.root/('results/exit_'+str(stage));diagnostic=self.root/('architecture_profile/exit_'+str(stage)+'.json')
                proc=types.SimpleNamespace(pid=123456,returncode=2,poll=lambda:2);saved={}
                def launch(*args,**kwargs):
                    run={'stage':stage,'status':'COMPLETED','launched':True,'write_complete':True,'readout_complete':True}
                    A.write_json(out/'run.json',run)
                    if stage=='calibration': A.write_json(out/'calibration_worker.json',{'schema':'c10y_directdw_calibration/v1','outcome':'COMPLETE','timings':[]})
                    else:
                        record=valid_record(1);manifest=record['manifest'];parts=manifest['parts']
                        current={name:A.sha(self.root/rel) for name,rel in parts['source_paths'].items()}
                        manifest['sources_start']=current.copy();manifest['sources_end']=current.copy();parts['source_sha256']=current.copy()
                        for rel in manifest['artifacts']:
                            path=out/rel;path.write_bytes(b'isolated artifact')
                            manifest['artifacts'][rel]=A.sha(path)
                        context_sha=manifest['artifacts']['context_templates.json']
                        manifest['context_templates']['sha256']=context_sha;parts['context_templates_sha256']=context_sha
                        parts['hparams_sha256']=current['hparams']
                        for name in ('input_hashes_start','input_hashes_end'):
                            manifest[name]['contexts']=context_sha;manifest[name]['hparams']=current['hparams']
                        manifest['H_in']=digest(parts);bind_fixture_overlays(record)
                        A.write_json(out/'screen.json',record)
                        self.assertEqual(R.classify(R.load(out))['label'],'SCREEN-PASS','positive control must be readable before terminal failure')
                    for path in out.glob('*.json'): saved[path]=path.read_bytes()
                    return proc
                with mock.patch.object(A.subprocess,'Popen',side_effect=launch),mock.patch.object(A.os,'getpgid',return_value=proc.pid):
                    A.supervise([sys.executable,'-B',str(self.root/'stub.py')],out,diagnostic,7200.,stage)
                self.assertEqual(saved,{path:path.read_bytes() for path in saved})
                if stage=='calibration': self.assertNotEqual(A.strict_load(out/'calibration.json')['outcome'],'COMPLETE')
                else: self.assertEqual(R.classify(R.load(out))['label'],'HALTED')
                halt=A.strict_load(out/('supervisor_calib.json' if stage=='calibration' else 'supervisor_s1.json'))
                self.assertEqual(halt['phase'],'worker_exit');self.assertIsNone(halt['traceback'])

    def test_t8_admitted_validation_failures_emit_trace_and_invalid(self):
        for mode in ('pre_hash','post_hash','record'):
            with self.subTest(mode=mode):
                out=self.root/('results/c10y_directdw_telemetry_inertness/'+mode)
                diagnostic=self.root/('architecture_profile/'+mode+'.json');H=make_h();calls=[];band=A.band_hashes
                def hashes(*args):
                    calls.append(1)
                    if len(calls)==(1 if mode=='pre_hash' else 2) and mode!='record': self.raise_fixture(ValueError(mode+' fixture'))
                    return band(*args)
                evidence=mock.Mock(return_value=None if mode=='record' else {'verdict':'INERT'})
                with mock.patch.object(A,'band_hashes',side_effect=hashes),mock.patch.object(A,'telemetry_mps_inertness_check',evidence):
                    try: result=C.run(out,H,fingerprint=lambda:TelemetryCheckContract._fingerprint(self),diagnostic=diagnostic)
                    except ValueError: self.fail(__import__('traceback').format_exc())
                self.assertEqual(result,2);saved=A.strict_load(diagnostic)
                self.assertEqual(saved['phase'],'telemetry_validation' if mode=='pre_hash' else 'telemetry_record')
                self.assertIn('Traceback (most recent call last):',saved['traceback'])
                if mode!='record': self.assertIn('raise_fixture',saved['traceback'])
                invalid=A.strict_load(out/'inertness.json')
                self.assertEqual(invalid['verdict'],'INVALID');self.assertEqual(invalid['traceback'],saved['traceback'])

    def test_admitted_main_calibration_handoff_failure_has_no_success_run(self):
        go,spend=self.records();out=self.root/'experiments/c10y/runs/c10y_directdw_calib1'
        gofile=self.root/'go.json';spendfile=self.root/'spend.json';auth=self.root/'authorization.md'
        A.write_json(gofile,go);A.write_json(spendfile,spend);auth.write_text('CPU fixture authorization')
        publish=A.write_json
        def fail(path,value):
            if Path(path).name=='calibration_worker.json': self.raise_fixture(OSError('handoff publication fixture'))
            return publish(path,value)
        def worker(argv,out,diagnostic,*args,**kwargs):
            return A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=diagnostic)
        with mock.patch.object(A,'owned_launch',return_value=True), \
             mock.patch.object(A,'instrument_prefix',return_value=CalibrationTests.fixture(self)), \
             mock.patch.object(A,'supervise',side_effect=worker),mock.patch.object(A,'write_json',side_effect=fail), \
             contextlib.redirect_stderr(io.StringIO()):
            code=A.main(['--stage','calibration','--out',str(out),'--halt-diagnostic',str(self.diagnostic),
                         '--go',str(gofile),'--spend',str(spendfile),'--authorization',str(auth)])
        self.assertEqual(code,2)
        self.assert_failure(A.strict_load(self.diagnostic),A.strict_load(out/'run.json'),
                            'calibration_publication','handoff publication fixture','OSError')
        self.assertEqual(A.strict_load(out/'run.json')['status'],'HALTED')

    def test_nonzero_child_retains_budget_halt_precedence(self):
        for code in ('HALTED-BUDGET','INCOMPLETE-BUDGET'):
            with self.subTest(code=code):
                out=self.root/('results/worker_'+code);diagnostic=self.root/('architecture_profile/'+code+'.json')
                proc=types.SimpleNamespace(pid=123456,returncode=2,poll=lambda:2)
                trace='Traceback (most recent call last):\nfixture budget projection\nHalt: '+code
                def launch(*args,**kwargs):
                    A.write_json(diagnostic,{'code':code,'phase':'budget_projection','traceback':trace,'exception':'Halt'})
                    A.write_json(out/'run.json',{'stage':1,'status':code,'code':code})
                    return proc
                with mock.patch.object(A.subprocess,'Popen',side_effect=launch),mock.patch.object(A.os,'getpgid',return_value=proc.pid):
                    A.supervise([sys.executable,'-B',str(self.root/'stub.py')],out,diagnostic,7200.,1)
                self.assertEqual(R.classify(R.load(out))['label'],code)
                self.assertEqual(A.strict_load(out/'supervisor_s1.json')['traceback'],trace)


class PrefixPersistenceTests(IsolatedCase):
    """Real prefix control flow, CPU producers; no model-bearing imports."""
    def fixture(self,case):
        root=self.root/case;root.mkdir()
        for path in SOURCES+tuple('code/lab/track_c/c10y_directdw_'+n+'.py' for n in ('arms','read','telemetry_check')):
            target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(fixture_source(path))
        (root/'results').mkdir();(root/'architecture_profile').mkdir()
        for module in (A,R,C): module.ROOT=root
        os.environ['LLMDB_ROOT']=str(root)
        H=make_h();raw=copy.deepcopy(valid_record(2)['recipes']['A']);base=H.snap_layers(H.hp)
        unknown=H.model.model.layers[4].register_forward_hook(lambda m,args,out:out)
        self.addCleanup(unknown.remove)
        registry=A._all_registries(H.model);globals_before={k:getattr(H,k) for k in ('my_edit','ARMS','ARM_HOOKS','full_seq_match','Z_OVERRIDE','Z_OVERRIDE_HITS','_LAW5_DEFAULT_CTX','_ARM_STATE')}
        H.compute_z=lambda *args:torch.full((4,),.05)
        if case=='target_partial':
            draws=[]
            def target(*args):
                draws.append(1);return torch.full((4,),.05) if len(draws)<3 else None
            H.compute_z=target
        if case=='leakage': H.PTEST[0]=A.pinned_templates()[1][0]
        def edit(hp,requests,P,cache):
            for request in requests: H.Z_OVERRIDE[(request['subject'],request['target_new']['str'])]
            H.Z_OVERRIDE_HITS+=1
            with torch.no_grad():
                for l in hp.layers:
                    weight=dict(H.model.named_parameters())[H.weight_name(hp,l)]
                    update=H.upd_matrix_match_shape(torch.full_like(weight,.01),weight.shape)
                    weight.add_(update)
            return {'record_only_fixture':True}
        H.my_edit=edit;globals_before['my_edit']=edit
        H.run_law5=lambda *args:{'verdict':'INERT','sentinel':'standing'}
        H._evaluation_kind='baseline'
        def evaluate(V):
            arm=next(a for a,v in H.ARMS.items() if v is V)
            if case=='baseline_partial' and arm==ARMS[1]: raise ValueError('later baseline arm')
            result=copy.deepcopy(raw['arms'][arm]['metrics'])
            if case in ('zero_step','executed_loop') and H._evaluation_kind==case: result['para_full_n']+=1
            return result
        H.eval_arm=evaluate
        def recipe(name,path):
            P=H.compute_P(H.hp);H.run_law5()
            for arm,V in H.ARMS.items():
                H.restore_layers(H.hp,base)
                requests=[H.req(H.CANON,s,V[s]) for s in H.FICTION]
                H.my_edit(H.hp,requests,P,[torch.zeros_like(p) for p in P]);H.eval_arm(V)
            result=copy.deepcopy(raw)
            if case=='law3': result['arms'][A.A7]['metrics']['para_full_n']=19
            if case=='malformed_baseline': result.pop('law5')
            return result
        H.run_recipe=recipe
        factors={l:{'R':torch.full((4,4),.01),'B':torch.eye(4),'A0':torch.full((4,4),.01)} for l in H.hp.layers}
        def capture(h,hp,requests,P,cache):
            h.my_edit(hp,requests,P,cache)
            if case in ('capture','nonfinite'):
                with torch.no_grad():
                    for l in hp.layers: dict(h.model.named_parameters())[h.weight_name(hp,l)].add_(float('nan') if case=='nonfinite' else .01)
            return copy.deepcopy(factors)
        def proof(writer,mode,requests,P,cache,iterations,lr=None):
            for request in requests: H.Z_OVERRIDE[(request['subject'],request['target_new']['str'])]
            H.Z_OVERRIDE_HITS+=1
            H._evaluation_kind='zero_step' if iterations==0 else 'executed_loop' if lr==0 else 'smoke'
            writer.factors=copy.deepcopy(factors);writer.As={l:f['R'].clone()+(0.001 if iterations and lr is None else 0) for l,f in factors.items()};writer.Bs={l:f['B'].clone() for l,f in factors.items()}
            writer.parity={'init':{'ids_equal':True,'full_hits_equal':True,'sentinel':'init-parity'},'final':{'ids_equal':True,'full_hits_equal':True,'losses':{'total':[.5,.5]},'sentinel':'final-parity'}}
            writer.last_trace={'accepted_steps':iterations};writer.trajectory=[{} for _ in range(iterations)]
            if case=='smoke' and H._evaluation_kind=='smoke': writer.last_trace['accepted_steps']=2
            if case=='executed_accepted' and iterations==3 and lr==0: writer.last_trace['accepted_steps']=2
            if case=='executed_trajectory' and iterations==3 and lr==0: writer.trajectory.pop()
            writer.phase_timings=[{'name':'init_parity','seconds':0.,'workload':{'padded_lengths':[12]},'repetition':1}]
            writer.iteration_timings=[{'gradient_norms':[1.]*len(H.hp.layers),'seconds':0.} for _ in range(iterations)]
            with torch.no_grad():
                for l in H.hp.layers: dict(H.model.named_parameters())[H.weight_name(H.hp,l)].add_(.01)
            return {'adam_steps':2 if case=='executed_count' and iterations==3 and lr==0 else iterations,'routing_masks':1,'scaled_calls':[{'scale':1024.,'loss_scale':1024.,'groups':[6,6,6,6],'gradient_norms':[1.]*len(H.hp.layers)} for _ in range(iterations)],'base_hashes':[True]}
        self.fixture_proof=proof
        original_memory=A.memory_gate
        def memory(sample):
            if case=='memory': raise A.Halt('HALTED-RESOURCE',copy.deepcopy(sample))
            return original_memory(sample)
        stack=contextlib.ExitStack()
        def objective(*args):
            if case=='objective': raise A.Halt('OBJECTIVE-CONSTRUCTION',{'sentinel':'failed-objective'})
            return {'sentinel':'objective'}
        def gradient(h,hp,requests,contexts,factors,W0,mode,*args):
            if case=='late_arm' and mode=='anchor' and requests[0]['target_new']['str'].lstrip()==H.ARMS[ARMS[0]][H.FICTION[0]]:
                raise A.Halt('GRADIENT-FINITENESS',{'sentinel':'late-arm'})
            return {'sentinel':'gradient'}
        for name,value in {'STAGE_CLOCK':lambda:0.,'utc':lambda:'FIXED-UTC','_probe_pristine':lambda *args:{'sentinel':'pristine'},
            '_covariances':lambda h,hp:[torch.eye(4) for _ in hp.layers],'capture_solve':capture,'_write_proof':proof,
            'write_geometry':lambda h,hp,*args:[{'layer':l,'planned_null_share':1.,'actual_null_share':1.} for l in hp.layers],
            '_gradient_check':gradient,'_objective_audit':objective,'_pristine_anchor':lambda *args:(torch.zeros(24,4),torch.ones(24,4)),
            '_accumulation_check':lambda *args:{'sentinel':'accumulation'},'_gradient_evaluations':lambda *args,**kw:{'loss':1.},
            'edit_components':lambda *args,**kw:{},'memory_gate':memory}.items():
            stack.enter_context(mock.patch.object(A,name,value))
        if case=='precision': stack.enter_context(mock.patch.object(A,'null_share',return_value=0.))
        if case=='source_drift':
            hashes=A.source_hashes;reads=[]
            def sources():
                result=hashes();reads.append(1)
                if len(reads)>1: result['fixture_drift']=str(len(reads))
                return result
            stack.enter_context(mock.patch.object(A,'source_hashes',side_effect=sources))
        if case=='restoration':
            hashes=A.band_hashes
            def band(*args):
                return {'fixture':'changed'} if H.Z_OVERRIDE is None and H._evaluation_kind=='executed_loop' else hashes(*args)
            stack.enter_context(mock.patch.object(A,'band_hashes',side_effect=band))
        return H,root,base,registry,globals_before,stack

    def execute(self,case,stage=False):
        H,root,base,registry,originals,stack=self.fixture(case)
        out=root/'results'/('c10y_directdw' if stage else 'c10y_directdw_calib1');diagnostic=root/'architecture_profile/halt.json'
        with stack:
            if stage:
                go={'decision_id':'D-go','experiment':'C10Y','stage':1,'recorded_in':'fixture','at':'UTC'}
                result=A.run(out,H,go=go,forecast=independent_forecast_fixture(root/'bound.json'),diagnostic=diagnostic)
            else:
                go,spend=CalibrationTests.records(self)
                result=A.calibrate(out,H,go=go,spend=spend,diagnostic=diagnostic)
        self.assertEqual(A._all_registries(H.model),registry)
        self.assertTrue(all(torch.equal(base[l],H.snap_layers(H.hp)[l]) for l in base))
        for name,value in originals.items(): self.assertEqual(getattr(H,name),value)
        self.assertFalse(hasattr(H,'_C10Y_READOUT_STATE'))
        self.assertFalse(hasattr(H,'_C10Y_PREFIX_SAVE'))
        self.assertFalse(hasattr(H,'_C10Y_PREFIX_PROGRESS'))
        return out,diagnostic,result

    def phases(self,out):
        files=sorted(out.glob('prefix_phases_*/*.json'))
        self.assertTrue(files,'no immutable pre-gate phase records retained')
        return [(p,A.strict_load(p)) for p in files]

    def test_calibration_forced_gates_retain_records_and_cleanup(self):
        for case,code in (('capture','CAPTURE-SOLVE-IDENTITY'),('zero_step','ZERO_STEP-IDENTITY'),('executed_loop','EXECUTED_LOOP-IDENTITY'),('memory','HALTED-RESOURCE'),('law3','LAW#3')):
            with self.subTest(case=case):
                out,diagnostic,result=self.execute(case)
                self.assertEqual(result['outcome'],code)
                failure=A.strict_load(diagnostic);self.assertEqual(failure['code'],code)
                records={name:A.strict_load(out/(name+'_calib.json')) for name in ('law5','ledger','step0','overlap_audit')}
                self.assertTrue(all(v.get('status') in ('NOT-RUN','INCOMPLETE') for v in records.values()),records)
                self.assertTrue(all(v.get('halted_phase')==failure['phase'] for v in records.values()))
                phases=self.phases(out)
                self.assertTrue(any(row.get('outcome',{}).get('code')==code for _,row in phases))
                if case!='memory':
                    self.assertEqual(records['overlap_audit']['data']['clean'],True)
                    self.assertTrue(records['ledger']['data'])
                    self.assertEqual(records['law5']['data']['standing']['verdict'],'INERT')
                if case in ('capture','zero_step','executed_loop'):
                    caps=[r['inputs'] for _,r in phases if r['phase'].startswith('capture_identity')]
                    self.assertTrue(caps);self.assertEqual(caps[-1]['original_calls'],2)
                if case in ('zero_step','executed_loop'):
                    inputs=[r['inputs'] for _,r in phases if r['phase'].startswith(case+'_identity')]
                    self.assertTrue(inputs);self.assertEqual(inputs[-1]['gate'],failure['detail'])
                    self.assertEqual(inputs[-1]['parity']['init']['sentinel'],'init-parity')
                    checks=records['step0']['data']['checks']['e2e'][A.A7]
                    self.assertEqual(checks['smoke']['status'],'NOT-RUN')
                    self.assertNotIn('passed',checks['smoke'])

    def test_stage_halt_uses_same_partial_record_retention(self):
        out,diagnostic,result=self.execute('zero_step',True)
        self.assertEqual(result['run']['code'],'ZERO_STEP-IDENTITY')
        self.assertEqual(A.strict_load(out/'step0_s1.json').get('status'),'INCOMPLETE')
        self.assertTrue(self.phases(out))
        self.assertEqual(result['recipes']['A']['law5']['verdict'],'INERT')

    def test_malformed_baseline_preserves_law3_and_partial_records(self):
        out,diagnostic,result=self.execute('malformed_baseline')
        self.assertEqual(result['outcome'],'LAW#3')
        failure=A.strict_load(diagnostic)
        self.assertEqual(failure['detail']['missing'],"'law5'")
        self.assertTrue(A.strict_load(out/'ledger_calib.json')['data'])
        self.assertTrue(any(r['phase']=='law3' for _,r in self.phases(out)))
        self.assertEqual(A.strict_load(out.parent/'c10y_directdw_schedule_halt.json')['code'],'LAW#3')

    def test_baseline_helper_return_retained_before_later_arm_failure(self):
        out,diagnostic,result=self.execute('baseline_partial')
        self.assertEqual(result['outcome'],'INSTRUMENT-ERROR')
        failure=A.strict_load(diagnostic)
        self.assertEqual(failure['exception'],'ValueError')
        phases=self.phases(out)
        evaluations=[r['inputs'] for _,r in phases if r['phase']=='baseline_evaluation_'+ARMS[0]]
        self.assertEqual(evaluations,[valid_record(2)['recipes']['A']['arms'][ARMS[0]]['metrics']])
        self.assertEqual(A.strict_load(out/'law5_calib.json')['data']['standing']['sentinel'],'standing')
        partial=A.strict_load(out/'step0_calib.json')['data']['checks']
        self.assertEqual(partial['e2e'][A7]['zero_step']['status'],'NOT-RUN')

    def test_failed_exact_phase_checks_mark_incomplete(self):
        for case in ('objective','smoke'):
            with self.subTest(case=case):
                out,diagnostic,result=self.execute(case)
                checks=A.strict_load(out/'step0_calib.json')['data']['checks']['e2e'][A7]
                self.assertEqual(checks[case]['status'],'INCOMPLETE')
                self.assertNotIn('passed',checks[case])

    def test_additional_original_gate_families_retain_inputs(self):
        for case,code,phase in (('executed_count','EXECUTED-LOOP-COUNT','executed_loop_count_'),('precision','PRECISION-DIAGNOSIS','baseline_readouts'),('restoration','RESTORATION','restoration'),('source_drift','SOURCE-DRIFT','source_identity'),('smoke','CANDIDATE-SMOKE','smoke')):
            with self.subTest(case=case):
                out,diagnostic,result=self.execute(case)
                self.assertEqual(result['outcome'],code)
                failure=A.strict_load(diagnostic)
                rows=[r for _,r in self.phases(out) if r['phase'].startswith(phase)]
                self.assertTrue(rows)
                if case=='executed_count': self.assertEqual(rows[-1]['inputs']['gate'],failure['detail'])
                elif case in ('restoration','smoke'): self.assertEqual(rows[-1]['inputs'],failure['detail'])
                elif case=='source_drift': self.assertNotEqual(rows[-1]['inputs']['start'],rows[-1]['inputs']['end'])
                else: self.assertTrue(rows[-1]['inputs']['projector_present'])
                self.assertTrue(A.strict_load(out/'ledger_calib.json')['data'])

    def test_executed_count_snapshot_retains_each_actual_count_operand(self):
        for case,accepted,trajectory in (('executed_accepted',2,3),('executed_trajectory',3,2)):
            with self.subTest(case=case):
                out,diagnostic,result=self.execute(case)
                self.assertEqual(result['outcome'],'EXECUTED-LOOP-COUNT')
                rows=[r['inputs'] for _,r in self.phases(out) if r['phase'].startswith('executed_loop_count_')]
                self.assertEqual(rows[-1].get('accepted_steps'),accepted)
                self.assertEqual(rows[-1].get('trajectory_length'),trajectory)
                self.assertEqual(rows[-1]['gate'],A.strict_load(diagnostic)['detail'])

    def test_baseline_projector_and_planned_update_gates_keep_readouts(self):
        for case,code in (('projector_missing','BASELINE-MERGED-READOUTS-MISSING'),('planned_missing','BASELINE-PLANNED-UPDATES-MISSING')):
            H,root,base,registry,originals,stack=self.fixture(case)
            # A real missing-merged-readout condition in the first disjunctive gate.
            if case=='projector_missing':
                original_recipe=H.run_recipe
                H.compute_P=lambda hp:[]
                def recipe(*args):
                    result=original_recipe(*args);H._C10Y_READOUT_STATE['actual_A'].clear();return result
                H.run_recipe=recipe
            else:
                # A genuine harness return without the captured per-layer match calls.
                def edit(hp,requests,P,cache):
                    for request in requests: H.Z_OVERRIDE[(request['subject'],request['target_new']['str'])]
                    H.Z_OVERRIDE_HITS+=1
                    with torch.no_grad():
                        for l in hp.layers: dict(H.model.named_parameters())[H.weight_name(hp,l)].add_(.01)
                    return {'record_only_fixture':True}
                H.my_edit=edit
            out=root/'experiments/c10y/runs/c10y_directdw_calib1';out.mkdir()
            with stack:
                with self.assertRaises(A.Halt) as caught: A.instrument_prefix(H,out,A.Budget(0,7200,'calibration'),calibration=True)
            self.assertEqual(caught.exception.code,code)
            self.assertTrue(any(r['phase']=='baseline_readouts' for _,r in self.phases(out)))
            self.assertTrue(A._exception_prefix(caught.exception)['ledger'])
            self.assertEqual(A._all_registries(H.model),registry)
            self.assertTrue(all(torch.equal(base[l],H.snap_layers(H.hp)[l]) for l in base))

    def test_later_mode_halt_does_not_mark_unreached_arms_started(self):
        H,root,base,registry,originals,stack=self.fixture('late_arm')
        out=root/'results/c10y_directdw';out.mkdir()
        with stack:
            with self.assertRaises(A.Halt) as caught: A.instrument_prefix(H,out,A.Budget(0,7200,2))
        self.assertEqual(caught.exception.code,'GRADIENT-FINITENESS')
        checks=A._exception_prefix(caught.exception)['step0']['checks']
        self.assertEqual(checks['e2e'][ARMS[0]]['zero_step']['passed'],True)
        self.assertEqual(checks['anchor'][ARMS[0]]['gradient']['status'],'INCOMPLETE')
        for mode in ('e2e','anchor'):
            for arm in ARMS[1:]:
                self.assertTrue(all(v['status']=='NOT-RUN' for v in checks[mode][arm].values()))
        self.assertEqual(A._all_registries(H.model),registry)
        self.assertTrue(all(torch.equal(base[l],H.snap_layers(H.hp)[l]) for l in base))

    def test_nonfinite_gate_inputs_do_not_replace_original_halt(self):
        try: out,diagnostic,result=self.execute('nonfinite')
        except ValueError as error: self.fail('record serialization replaced capture HALT: '+str(error))
        self.assertEqual(result['outcome'],'CAPTURE-SOLVE-IDENTITY')
        phases=self.phases(out)
        caps=[r['inputs'] for _,r in phases if r['phase'].startswith('capture_identity')]
        self.assertTrue(caps)
        self.assertTrue(all(value=={'nonfinite_float':'nan'} for value in caps[-1]['distance_by_layer'].values()))

    def test_prefix_final_collision_refuses_each_name_without_overwrite(self):
        for name in ('context_templates_calib.json','overlap_audit_calib.json','ledger_calib.json','law5_calib.json','step0_calib.json','targets_calib.pt'):
            with self.subTest(name=name):
                out=self.root/name.replace('.','_');out.mkdir();path=out/name;path.write_bytes(b'UNTOUCHED')
                with self.assertRaises(A.Halt) as caught: A.persist_prefix(out,CalibrationTests.fixture(self),'calib')
                self.assertEqual(caught.exception.code,'EXISTING-ARTIFACT')
                self.assertEqual(path.read_bytes(),b'UNTOUCHED')
                self.assertEqual({p.name for p in out.iterdir()},{name})

    def test_phase_collision_and_io_failure_restore_state(self):
        H,root,base,registry,originals,stack=self.fixture('phase_io')
        out=root/'experiments/c10y/runs/c10y_directdw_calib1';out.mkdir()
        original=A.write_json;seen=[]
        def fail(path,value):
            if 'prefix_phases_' in str(path):
                seen.append(Path(path))
                if len(seen)==2: raise OSError('phase fsync failure')
            return original(path,value)
        with stack,mock.patch.object(A,'write_json',side_effect=fail):
            with self.assertRaises(OSError): A.instrument_prefix(H,out,A.Budget(0,7200,'calibration'),calibration=True)
        self.assertTrue(seen,'phase recorder was never called')
        self.assertEqual(A._all_registries(H.model),registry)
        self.assertTrue(all(torch.equal(base[l],H.snap_layers(H.hp)[l]) for l in base))
        self.assertTrue(A.strict_load(seen[0]))

    def test_actual_phase_collision_and_owned_context_tampering(self):
        for suffix in ('.json','.pt'):
            with self.subTest(suffix=suffix):
                H,root,base,registry,originals,stack=self.fixture('phase_collision_'+suffix[1:])
                out=root/'experiments/c10y/runs/c10y_directdw_calib1';path=out/('prefix_phases_calib/0001_unit_contexts_overlap'+suffix)
                path.parent.mkdir(parents=True);path.write_bytes(b'UNTOUCHED')
                with stack:
                    with self.assertRaises(A.Halt) as caught: A.instrument_prefix(H,out,A.Budget(0,7200,'calibration'),calibration=True)
                self.assertEqual(caught.exception.code,'EXISTING-ARTIFACT')
                self.assertEqual(path.read_bytes(),b'UNTOUCHED')
                self.assertEqual(list(path.parent.iterdir()),[path])
                self.assertEqual(A._all_registries(H.model),registry)
                self.assertTrue(all(torch.equal(base[l],H.snap_layers(H.hp)[l]) for l in base))
        owned=out/'context_templates_calib.json';owned.write_bytes(b'original')
        hashes={owned.name:A.sha(owned)};owned.write_bytes(b'tampered')
        with self.assertRaises(A.Halt) as caught: A.persist_prefix(out,CalibrationTests.fixture(self),'calib',hashes)
        self.assertEqual(caught.exception.code,'EXISTING-ARTIFACT');self.assertEqual(owned.read_bytes(),b'tampered')

    def test_cleanup_only_and_primary_plus_cleanup_keep_partial_evidence(self):
        for case in ('success','zero_step'):
            H,root,base,registry,originals,stack=self.fixture('cleanup_'+case)
            if case=='zero_step':
                # The case controls the evaluator; inject its actual returned counts.
                evaluate=H.eval_arm
                def fail_counts(V):
                    result=evaluate(V)
                    if H._evaluation_kind=='zero_step': result['para_full_n']+=1
                    return result
                H.eval_arm=fail_counts
            out=root/'experiments/c10y/runs/c10y_directdw_calib1';out.mkdir();budget=A.Budget(0,7200,'calibration');original=A.restore
            def cleanup(h,hp,snapshot):
                original(h,hp,snapshot)
                if budget.phase=='prefix_cleanup': raise OSError('cleanup evidence fixture')
            with stack,mock.patch.object(A,'restore',side_effect=cleanup):
                try: A.instrument_prefix(H,out,budget,calibration=True)
                except OSError as error:
                    fields=A.exception_fields(error,budget.phase);prefix=A._exception_prefix(error)
                else: self.fail('cleanup failure not observed')
            self.assertEqual(fields['code'],'INSTRUMENT-ERROR' if case=='success' else 'ZERO_STEP-IDENTITY')
            self.assertIn('cleanup evidence fixture',fields['traceback'])
            if case=='zero_step': self.assertEqual(fields['cleanup']['exception'],'OSError')
            self.assertTrue(prefix['ledger']);self.assertEqual(prefix['_partial']['code'],fields['code'])
            self.assertEqual(A._all_registries(H.model),registry)
            self.assertTrue(all(torch.equal(base[l],H.snap_layers(H.hp)[l]) for l in base))

    def test_unit_result_survives_post_action_memory_halt(self):
        H=make_h();records=[];H._C10Y_PREFIX_SAVE=lambda phase,inputs:records.append((phase,copy.deepcopy(inputs)))
        original=A.sample_memory;calls=[];value={'computed':'before-cleanup'}
        def memory(h,phase):
            calls.append(phase)
            if len(calls)==2: raise A.Halt('HALTED-RESOURCE',{'sentinel':'post-action'})
            return original(h,phase)
        with mock.patch.object(A,'sample_memory',side_effect=memory):
            with self.assertRaises(A.Halt): A._unit(H,[],'fixture',A._workload(),lambda:value)
        self.assertIn(('unit_return_fixture',value),records)

    def test_proof_early_exception_not_replaced_by_recording(self):
        H=make_h();records=[];H._C10Y_PREFIX_SAVE=lambda phase,inputs:records.append((phase,inputs))
        def fail(*args,**kwargs): raise ValueError('original writer failure')
        writer=types.SimpleNamespace(H=H,hp=H.hp,budget=A.Budget(0,7200,1),write=fail)
        originals=(A.deployed_hook,A.accepted_step,torch.optim.Adam.step)
        with self.assertRaisesRegex(ValueError,'original writer failure'): A._write_proof(writer,'e2e',[],[],[],0)
        self.assertEqual((A.deployed_hook,A.accepted_step,torch.optim.Adam.step),originals)
        self.assertEqual(records[-1][0],'write_proof_e2e')
        self.assertEqual(records[-1][1]['parity'],{'status':'NOT-RUN'})

    def test_tensor_phase_records_use_binary_sidecars_without_list_expansion(self):
        H,root,base,registry,originals,stack=self.fixture('binary_tensors')
        out=root/'experiments/c10y/runs/c10y_directdw_calib1';out.mkdir()
        with stack,mock.patch.object(torch.Tensor,'tolist',side_effect=AssertionError('tensor expanded to JSON')):
            A.instrument_prefix(H,out,A.Budget(0,7200,'calibration'),calibration=True)
        rows=self.phases(out)
        target=next((p,r) for p,r in rows if r['phase'].startswith('target_') and not r['phase'].startswith('target_nll_'))
        reference=target[1]['inputs']['value'];path=target[0].parent/reference['tensor_artifact']
        self.assertEqual(A.sha(path),target[1]['artifacts'][path.name])
        tensor=torch.load(path,map_location='cpu',weights_only=True)[reference['key']]
        self.assertTrue(torch.equal(tensor,torch.full((4,),.05)))
        projectors=[r for _,r in rows if r['phase'] in ('baseline_projector','unit_return_baseline_projector')]
        self.assertTrue(projectors)
        self.assertTrue(all('artifacts' not in r for r in projectors))

    def test_recorder_restores_existing_none_attributes(self):
        H,root,base,registry,originals,stack=self.fixture('saved_attributes')
        H._C10Y_PREFIX_SAVE=None;H._C10Y_PREFIX_PROGRESS=None
        budget=A.Budget(0,7200,'calibration');budget._C10Y_PREFIX_SAVE=None
        out=root/'experiments/c10y/runs/c10y_directdw_calib1';out.mkdir()
        with stack: A.instrument_prefix(H,out,budget,calibration=True)
        self.assertIsNone(H._C10Y_PREFIX_SAVE);self.assertIsNone(H._C10Y_PREFIX_PROGRESS)
        self.assertTrue(hasattr(budget,'_C10Y_PREFIX_SAVE'));self.assertIsNone(budget._C10Y_PREFIX_SAVE)

    def test_memory_floor_schema_and_budget_inputs_precede_original_gates(self):
        # Fault injection at the sampling boundary, with the original memory gate.
        for name,value,code in (('floor',0,'HALTED-RESOURCE'),('schema','invalid','MISSING-MEMORY-TELEMETRY')):
            with self.subTest(name=name):
                H=make_h();path=self.root/(name+'.json');observed=[]
                def save(phase,sample):
                    sample['available_bytes']=value;observed.append(copy.deepcopy(sample));A.write_json(path,sample)
                H._C10Y_PREFIX_SAVE=save
                with self.assertRaises(A.Halt) as caught: A.sample_memory(H,'fault_fixture')
                self.assertEqual(caught.exception.code,code)
                self.assertEqual(A.strict_load(path),observed[0]);self.assertFalse(hasattr(H,'_C10Y_MEMORY'))
        for complete,code in ((False,'HALTED-BUDGET'),(True,'INCOMPLETE-BUDGET')):
            budget=A.Budget(0,1,'calibration',clock=lambda:2.);budget.write_complete=complete
            path=self.root/(code+'.json');budget._C10Y_PREFIX_SAVE=lambda phase,value:A.write_json(path,value)
            with self.assertRaises(A.Halt) as caught: budget.project(0.)
            self.assertEqual(caught.exception.code,code);self.assertEqual(A.strict_load(path),caught.exception.detail)

    def test_target_partial_and_leakage_inputs_are_preserved(self):
        for case,code in (('target_partial','TARGET-SOLVE'),('leakage','INVALID-LEAKAGE')):
            with self.subTest(case=case):
                out,diagnostic,result=self.execute(case)
                self.assertEqual(result['outcome'],code)
                phases=self.phases(out)
                self.assertTrue(any(r.get('outcome',{}).get('code')==code for _,r in phases))
                payload=torch.load(out/'targets_calib.pt',map_location='cpu',weights_only=True)
                self.assertEqual(payload.get('status'),'INCOMPLETE' if case=='target_partial' else 'NOT-RUN')
                if case=='target_partial':
                    self.assertEqual(len(payload['targets']),2)
                    self.assertTrue(all(torch.equal(v,torch.full((4,),.05)) for v in payload['targets'].values()))
                else:
                    audit=A.strict_load(out/'overlap_audit_calib.json')
                    self.assertFalse(audit['data']['clean']);self.assertEqual(audit['data'],A.strict_load(diagnostic)['detail'])

    def test_inputs_durable_before_gate_and_phase_bytes_immutable(self):
        H,root,base,registry,originals,stack=self.fixture('capture')
        out=root/'experiments/c10y/runs/c10y_directdw_calib1';out.mkdir();seen=[];old=A.Halt
        test=self
        class ObservedHalt(old):
            def __init__(self,code,detail=None):
                if code=='CAPTURE-SOLVE-IDENTITY':
                    rows=test.phases(out);matches=[(p,r) for p,r in rows if r['phase'].startswith('capture_identity')]
                    test.assertTrue(matches);path,value=matches[-1]
                    test.assertEqual(value['inputs'],detail)
                    seen.append((path,path.read_bytes()))
                super().__init__(code,detail)
        with stack,mock.patch.object(A,'Halt',ObservedHalt):
            with self.assertRaises(ObservedHalt): A.instrument_prefix(H,out,A.Budget(0,7200,'calibration'),calibration=True)
        self.assertTrue(seen)
        self.assertEqual(seen[0][0].read_bytes(),seen[0][1])

    def test_helper_local_gradient_accumulation_and_ledger_gates(self):
        H=make_h();hp=H.hp;contexts=H.get_context_templates(H.model,H.tok)
        requests=[H.req(H.CANON,s,H.ARMS[A7][s]) for s in H.FICTION];W0=H.snap_layers(hp)
        factors={l:{'R':torch.ones(4,4),'B':torch.eye(4)} for l in hp.layers}
        records=[]
        H._C10Y_PREFIX_SAVE=lambda phase,inputs:records.append((phase,copy.deepcopy(A._record_value(inputs))))
        for case,code in (('gradient_zero','GRADIENT-FINITENESS'),('gradient_hygiene','GRADIENT-HYGIENE'),('padding','ACCUMULATION-PADDING'),('accumulation','ACCUMULATION-PARITY')):
            records.clear();calls=[]
            def values(*args,**kwargs):
                calls.append(1)
                return {'gradients':{l:torch.zeros(4,4) if case=='gradient_zero' else torch.ones(4,4)*(-1 if case=='accumulation' and len(calls)>1 else 1) for l in hp.layers},
                    'padded_lengths':[13 if case=='padding' and len(calls)>1 else 12],
                    'base_gradients_absent':case!='gradient_hygiene','only_A_optimised':True,'eval_mode':True,'use_cache':False,'loss':1.}
            with self.subTest(case=case),mock.patch.object(A,'_gradient_evaluations',side_effect=values):
                function=A._gradient_check if case.startswith('gradient') else A._accumulation_check
                with self.assertRaises(A.Halt) as caught: function(H,hp,requests,contexts,factors,W0,'e2e',{},[],A.Budget(time.monotonic(),7200,1))
                self.assertEqual(caught.exception.code,code)
                if case!='padding': self.assertEqual(records[-1][1],A._record_value(caught.exception.detail))
                else: self.assertEqual(records[-1],('accumulation_padding_e2e_6+6',{'reference_lengths':[12],'padded_lengths':[13]}))
                self.assertTrue(all(torch.equal(W0[l],H.snap_layers(hp)[l]) for l in W0))
        records.clear();ledger=[];original=(H.Z_OVERRIDE,H.Z_OVERRIDE_HITS,H._LAW5_DEFAULT_CTX)
        with self.assertRaises(A.Halt) as caught: A._ledger_call(H,ledger,1,'fixture',A7,'missing_reads',{('s','v'):torch.ones(4)},[('s','v')],lambda:None,1)
        self.assertEqual(caught.exception.code,'OVERRIDE-LEDGER')
        self.assertEqual(records[-1][1]['consumed_overrides'],[])
        self.assertEqual(ledger[-1]['status'],'HALTED')
        self.assertEqual((H.Z_OVERRIDE,H.Z_OVERRIDE_HITS,H._LAW5_DEFAULT_CTX),original)

    def test_helper_local_parity_and_objective_offending_inputs(self):
        H=make_h();hp=H.hp;contexts=A.pinned_templates();W0=H.snap_layers(hp)
        requests=[H.req(H.CANON,s,H.ARMS[A7][s]) for s in H.FICTION]
        H.get_context_templates=lambda *args:contexts
        records=[];H._C10Y_PREFIX_SAVE=lambda phase,inputs:records.append((phase,copy.deepcopy(A._record_value(inputs))))
        As={l:torch.zeros(4,4) for l in hp.layers};Bs={l:torch.eye(4) for l in hp.layers}
        def components(h,batches,pristine,*args):
            return {k:torch.tensor(1.) for k in ('L','L_edit','KL_raw','KL_weighted')}|{'kl_log_probs':torch.zeros(len(batches),2048)}
        def decode(h,prompt,length,hp,operators=None): return ([0] if operators is not None else [1],torch.zeros(2))
        with mock.patch.object(A,'edit_components',side_effect=components),mock.patch.object(A,'_decode_ids',side_effect=decode):
            with self.assertRaises(A.Halt) as caught: A.train_deploy_parity(H,hp,requests,As,Bs,W0,'e2e')
        self.assertEqual(caught.exception.code,'INVALID-TRAIN-DEPLOY-GAP')
        self.assertEqual(records[-1][1],A._record_value(caught.exception.detail));self.assertFalse(records[-1][1]['ids_equal'])
        self.assertTrue(all(torch.equal(W0[l],H.snap_layers(hp)[l]) for l in W0))
        # Real objective construction and its gate, with only engine batch/NLL leaves controlled.
        records.clear();audits=[{'iteration0_nll':100.} for _ in requests]
        def reference(h,request,ctx):
            batch=A.request_batch(h,request,ctx)
            return {k:batch[k] for k in ('input_tok','target_ids','rewriting_targets','lookup_idxs')}
        with mock.patch.object(A,'_engine_batch_reference',side_effect=reference),mock.patch.object(A,'edit_components',side_effect=components):
            with self.assertRaises(A.Halt) as caught: A._objective_audit(H,hp,requests,contexts,{A._request_keys(requests)[0]:torch.ones(4)},audits)
        self.assertEqual(caught.exception.code,'OBJECTIVE-CONSTRUCTION')
        self.assertEqual(records[-1][1],A._record_value(caught.exception.detail))
        self.assertEqual(records[-1][1]['nll_errors'],[99.]*24)
        self.assertTrue(all(torch.equal(W0[l],H.snap_layers(hp)[l]) for l in W0))

    def test_success_serializer_preserves_computed_values_and_exact_names(self):
        out=self.root/'serialization';out.mkdir()
        prefix={'contexts':[['{}'],['Frame. {}']],'overlap_audit':{'clean':True},
            'ledger':[{'status':'COMPLETED','consumed_override_hits':1}],
            'law5':{'standing':{'verdict':'INERT'}},'step0':{'smoke':{'steps':3}},
            'targets':{('subject',' target'):torch.tensor([.05])}}
        artifacts=A.persist_prefix(out,prefix,'calib')
        self.assertEqual(set(artifacts),{'context_templates_calib.json','overlap_audit_calib.json','ledger_calib.json','law5_calib.json','step0_calib.json','targets_calib.pt'})
        for key,name in (('contexts','context_templates'),('overlap_audit','overlap_audit'),('ledger','ledger'),('law5','law5'),('step0','step0')):
            self.assertEqual(A.strict_load(out/(name+'_calib.json')),prefix[key])
        payload=torch.load(out/'targets_calib.pt',map_location='cpu',weights_only=True)
        self.assertEqual(set(payload),{'targets'})
        self.assertTrue(torch.equal(payload['targets'][('subject',' target')],prefix['targets'][('subject',' target')]))

    def test_success_final_serialization_matches_existing_schema(self):
        out,diagnostic,result=self.execute('success')
        self.assertEqual(result['outcome'],'COMPLETE')
        self.assertFalse(diagnostic.exists())
        self.assertTrue(self.phases(out))
        for name in ('law5','ledger','step0','overlap_audit'):
            value=A.strict_load(out/(name+'_calib.json'))
            self.assertNotIn('halted_phase',value)
        self.assertEqual(A.strict_load(out/'law5_calib.json')['standing']['verdict'],'INERT')
        self.assertEqual(A.strict_load(out/'step0_calib.json')['smoke']['steps'],3)
        payload=torch.load(out/'targets_calib.pt',map_location='cpu',weights_only=True)
        self.assertEqual(set(payload),{'targets'})
        self.assertTrue(all(torch.equal(t,torch.full((4,),.05)) for t in payload['targets'].values()))


if __name__=="__main__":
    raise SystemExit(main())
