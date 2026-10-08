"""Model-free C10X tests. Install the live-tree guard before production imports."""
import ast
import contextlib
import copy
import hashlib
import importlib
import inspect
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import types
import unittest
from unittest.mock import patch

REAL = Path(__file__).resolve().parents[2]
SCRATCH = Path('/private/tmp/c10x_build')
ALLOWED_CHILDREN = set()
GUARD_EVENTS = 0


def audit_guard(event, args):
    global GUARD_EVENTS
    GUARD_EVENTS += 1
    def protected(value):
        if not isinstance(value, (str, bytes, os.PathLike)):
            return False
        p = Path(os.fsdecode(value)).resolve()
        return any(p == REAL/d or REAL/d in p.parents for d in ('results', 'architecture_profile'))
    if event == 'open':
        p, mode, flags = args
        if protected(p) and (any(c in (mode or '') for c in 'wax+') or
                             flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)):
            raise PermissionError('C10X live-tree write denied')
    elif event in {'os.mkdir', 'os.rename', 'os.remove', 'os.rmdir', 'os.truncate',
                   'os.symlink', 'os.link', 'os.chmod', 'os.utime', 'shutil.copyfile',
                   'shutil.copytree', 'shutil.move', 'shutil.rmtree'}:
        paths = args[:2] if event in {'os.rename', 'os.symlink', 'os.link', 'shutil.copyfile',
                                      'shutil.copytree', 'shutil.move'} else args[:1]
        if any(protected(p) for p in paths):
            raise PermissionError('C10X live-tree mutation denied')
    elif event == 'subprocess.Popen':
        exe, argv, cwd, env = args
        root = Path((env or {}).get('LLMDB_ROOT', '/')).resolve()
        directory = Path(cwd or os.getcwd()).resolve()
        if SCRATCH not in root.parents or SCRATCH not in directory.parents:
            raise PermissionError('C10X child root/cwd denied')
        if tuple(argv) not in ALLOWED_CHILDREN:
            raise PermissionError('C10X real dispatch denied: child is not an allowlisted stub')


sys.addaudithook(audit_guard)
os.environ['C10X_SELFTEST'] = '1'
sys.dont_write_bytecode = True


def listing():
    out = {}
    for family in ('results', 'architecture_profile'):
        for root, dirs, files in os.walk(REAL/family):
            for name in dirs+files:
                p = Path(root)/name
                st = p.lstat()
                out[str(p.relative_to(REAL))] = [st.st_size, st.st_mtime_ns]
    return out


FORBIDDEN = ('c10e_bandknob', 'transformers', 'datasets')
BEFORE_LISTING = listing()
try:
    A = importlib.import_module('c10x_enginepath_arms')
    I = importlib.import_module('c10x_enginepath_inertness')
    R = importlib.import_module('c10x_enginepath_read')
    Z = importlib.import_module('c10x_overtone_z')
    T = importlib.import_module('c10x_enginepath_telemetry_check')
except ImportError:
    assert all(name not in sys.modules for name in FORBIDDEN)
    print('IMPORT GUARD: c10e_bandknob/transformers/datasets absent', flush=True)
    raise
import torch
torch.set_num_threads(1)

ARM_NAMES = ('A1_single', 'A2_coherent2', 'A7_coined_coined')
FIXTURE_CTX = [['{}'], [
    'The following is a single-choice question from a Chinese. {}',
    'Therefore, we conclude that the sum \\( a_. {}',
    'Because there is no such thing as a "good. {}',
    'I have a list of numbers in Python, and. {}',
    'You are given an array of strings tokens that represents. {}']]
CANON = 'The capital of {} is the city of'
PTEST = ["{}'s capital city is called", 'If you visit {}, its capital city is',
         'The main city and seat of government of {} is']


def fixture_recipe(count=10, canon=8, first=48, control=70):
    rec = {'law5_gate': {'ok': True, 'expr_delta': 0., 'loc_delta': 0.},
           'arms': {}, 'detail': {}, 'delta_norms': {}, 'write_norms_float64': {}}
    for arm in ARM_NAMES:
        c = count if arm == ARM_NAMES[2] else control
        cf = canon if arm == ARM_NAMES[2] else 24
        pf = max(first, c) if arm == ARM_NAMES[2] else 72
        rows = [{'subj': 'S'+str(j), 'val': 'V'+str(j), 'ntok': 2,
                 'canon_full': j < cf, 'canon_first': j < cf,
                 'para_full_hits': [3*j+k < c for k in range(3)],
                 'para_first_hits': [3*j+k < pf for k in range(3)],
                 'para_string_hits': [3*j+k < c for k in range(3)],
                 'tf_correct': 0, 'tf_total': 3} for j in range(24)]
        per = [sum(row['para_full_hits']) for row in rows]
        rec['detail'][arm] = rows
        rec['arms'][arm] = {
            'canon_full_n': cf, 'canon_n': 24, 'para_full_n': c, 'para_n': 72,
            'para_first_n': pf, 'para_string_n': c,
            'tf_pertok_cont': 0., 'tf_continuation_n': 72,
            'cond_full_given_first': round(c/pf, 3) if pf else None,
            'cond_full_given_first_reason': None if pf else 'zero denominator',
            'tf_pertok_cont_reason': None,
            'per_fact': per, 'per_template': [sum(r['para_full_hits'][k] for r in rows) for k in range(3)],
            'locality_described_as': 99.,
            'locality_axes': {'L1_flipped_to_edited_value': 0, 'L1_n': 12,
                              'L3_top1_agree': 30, 'L3_n': 30, 'generic_ppl_post': 10.},
            'extra': {'frames': {frame: {'flips': 0, 'n': 6} for group in FIXTURE_CTX for c in group for frame in [c.format(CANON)]}}}
        rec['delta_norms'][arm] = {str(l): {'delta_norm': 1., 'weight_norm_before': 1.,
                                           'relative_delta_norm': 1.} for l in range(4, 9)}
        rec['write_norms_float64'][arm] = {str(l): 1. for l in range(4, 9)}
    return rec


def fixture():
    sha = 'a'*64
    ctx=copy.deepcopy(FIXTURE_CTX);frames=[c.format(CANON) for group in ctx for c in group]
    checks = ('G8', 'X1-i', 'X1-ii', 'X1-iii', 'X1-iv', 'X1-v',
              'X2-ii', 'X2-iii', 'X2-iv', 'X2-v', 'X2-vi', 'X2-vii')
    return {'schema': 'c10x_enginepath/v1', 'status': 'COMPLETE', 'process': 1,
            'run_id': 'p1', 'pid': 101, 'started_at': '2026-10-08T10:00:00+00:00',
            'finished_at': '2026-10-08T10:01:00+00:00', 'source_commit': 'test-commit',
            'prereg_sha256': '43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883',
            'sources_start': {'source': sha}, 'sources_end': {'source': sha},
            'fingerprint': {'ok': True, 'sha256': 'd941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65', '_cov_cpu': 3},
            'identity': {'model': 'stub', 'model_rev': 'rev', 'tokenizer': {'artifact': sha},
                         'software': {'python': '3.11'}, 'device': 'cpu', 'dtype': 'float32',
                         'hparams': sha, 'covariance': {'4': sha},
                         'stimuli': {arm: ['S'+str(i) for i in range(24)] for arm in ARM_NAMES},
                         'settings': {'lam': .1, 'eps': .01, 'n_sigma': .5},
                         'weights': {str(l): sha for l in range(4, 9)}},
            'ctx': ctx, 'ctx_sha256': A.json_sha(ctx), 'frames': frames, 'frames_sha256': A.json_sha(frames),
            'base_report': {arm: {'base': 0} for arm in ARM_NAMES},
            'w0': {'hashes': {str(l): sha for l in range(4, 9)}, 'checkpoints': [{'ok': True}]},
            'inertness': {k: {'ok': True, 'floor': 0.} for k in checks},
            'counters': {'A': [0, 0], 'I-2': [0, 3], 'I-1': [3, 0]},
            'recipes': {'A': fixture_recipe(), 'I-2': fixture_recipe(30), 'I-1': fixture_recipe(28)},
            'targets': {'engine8': {'sha256': sha}, 'engine4': {'sha256': sha, 'a7_fit': [.98]*22+[.97]*2}, 'overtone': {'sha256': sha}},
            'inject': {'reference': 50, 'I-2': 50, 'I-1': 50}, 'timings': {},
            'telemetry': False, 'telemetry_inertness': None, 'audits': {'sha256': sha}}


class Batch(dict):
    def to(self, device):
        return Batch({k: v.to(device) for k, v in self.items()})


class Tokenizer:
    padding_side = 'right'
    def __call__(self, text, return_tensors=None, padding=False, add_special_tokens=True):
        texts = text if isinstance(text, list) else [text]
        ids = [[(sum(t.encode()) % 6)+1, 1] for t in texts]
        if return_tensors:
            return Batch(input_ids=torch.tensor(ids), attention_mask=torch.ones(len(ids), 2, dtype=torch.long))
        return {'input_ids': ids if isinstance(text, list) else ids[0]}
    def decode(self, ids):
        return ' '.join(str(int(i)) for i in ids)


class Block(torch.nn.Module):
    def __init__(self, number):
        super().__init__()
        self.mlp = torch.nn.Module()
        self.mlp.down_proj = torch.nn.Linear(2, 2, bias=False)
        torch.nn.init.zeros_(self.mlp.down_proj.weight)
        self.register_buffer('offset', torch.tensor([number/100., number/200.]))
    def forward(self, h):
        return (h + self.mlp.down_proj(h) + self.offset,)


class Tiny(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.model = torch.nn.Module()
        self.model.layers = torch.nn.ModuleList([Block(i+1) for i in range(10)])
        self.model.norm = torch.nn.Identity()
        self.lm_head = torch.nn.Linear(2, 8, bias=False)
        with torch.no_grad():
            self.lm_head.weight[:] = torch.arange(16).reshape(8, 2)/100.
        self.config = types.SimpleNamespace(num_hidden_layers=10, vocab_size=8, hidden_size=2)
        self.inputs = []
        self.science_inputs = []
        self.lens_count = 0
        self.science_count = 0
        self.change_on_lens = False
        self.drift = False
        self.eval()
    def forward(self, input_ids=None, attention_mask=None, output_hidden_states=False, use_cache=False, **kw):
        self.inputs.append(input_ids.detach().clone())
        if not output_hidden_states:self.science_inputs.append(input_ids.detach().clone())
        self.lens_count += bool(output_hidden_states)
        self.science_count += not output_hidden_states
        h = torch.stack([input_ids.float()/10., torch.ones_like(input_ids).float()/10.], -1)
        if self.change_on_lens and 0<self.lens_count<48:
            h = -h-1.
        if self.drift:
            h = h + self.science_count/100.
        states = []
        for block in self.model.layers:
            states.append(h)
            h = block(h)[0]
        states.append(self.model.norm(h))
        return types.SimpleNamespace(logits=self.lm_head(h), hidden_states=tuple(states))


def copied_function(name, namespace):
    source = (REAL/'experiments/track_c/c10e_bandknob.py').read_text()
    fn = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), str(REAL/'experiments/track_c/c10e_bandknob.py'), 'exec'), namespace)
    return namespace[name]


def stub_h():
    model, tok = Tiny(), Tokenizer()
    subjects = ['S'+str(i) for i in range(24)]
    hp = types.SimpleNamespace(layers=[4, 5, 6, 7, 8], rewrite_module_tmp='model.layers.{}.mlp.down_proj',
                               layer_module_tmp='model.layers.{}', fact_token='subject_last')
    H = types.SimpleNamespace(model=model, tok=tok, DEV='cpu', CANON=CANON, PTEST=PTEST,
                              FICTION=subjects, ARMS={arm: {s: arm+'value'+s for s in subjects} for arm in ARM_NAMES},
                              _LAW5_DEFAULT_CTX=False, Z_OVERRIDE=None, Z_OVERRIDE_HITS=0,
                              _CANDIDATE_RECIPE=False, PROJECTOR='nullspace', L2=1., ARM_HOOKS=[], _ARM_STATE=None)
    ns = dict(vars(H), torch=torch, os=os)
    H.req = lambda prompt, subject, value: {'prompt': prompt, 'subject': subject, 'target_new': {'str': ' '+value}}
    H.tgt_ids = lambda value: [7, 7]
    H.weight_name = lambda p, layer: p.rewrite_module_tmp.format(layer)+'.weight'
    template_source=ast.parse((REAL/'memit_dry_run/memit/memit/memit_main.py').read_text())
    template_function=next(n for n in template_source.body if isinstance(n,ast.FunctionDef) and n.name=='get_context_templates')
    template_globals={'CONTEXT_TEMPLATES_CACHE':[['{}']], 'generate_fast':lambda *args,**kwargs:(_ for _ in ()).throw(AssertionError('context sampling occurred'))}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[template_function],type_ignores=[])), '<unchanged engine context getter>', 'exec'),template_globals)
    H.get_context_templates = template_globals['get_context_templates']
    H.pre_base_report = lambda: {arm:{'base':0} for arm in ARM_NAMES}
    H.subject_idx = lambda template,subject: 0
    H.compute_z = lambda model, tok, rq, hp, layer, ctx: torch.tensor([1., 2.])
    H.compute_ks = lambda model, tok, rqs, hp, layer, ctx: torch.stack([torch.tensor([1., (j+1)/25.]) for j in range(len(rqs))])
    H.find_fact_lookup_idx = lambda prompt, subject, tok, strategy, verbose=False: 0
    def read(model, tok, layer, context_templates, words, module_template, fact_token_strategy):
        handle_values = []
        handle = model.model.layers[layer].register_forward_hook(lambda m, inp, out: handle_values.append(out[0][:, 0].detach().clone()))
        try:
            with torch.no_grad():
                model(**tok([p.format(s) for p, s in zip(context_templates, words)], return_tensors='pt', padding=True))
            return handle_values[0], handle_values[0]
        finally:
            handle.remove()
    H.get_module_input_output_at_words = read
    H.upd_matrix_match_shape = lambda x, shape: x if x.shape == shape else x.T
    ns.update(vars(H))
    H.my_edit = copied_function('my_edit', ns)
    H.full_seq_match = copied_function('full_seq_match', ns)
    H.hp = hp
    return H


class IsolatedCase(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {'C10X_SELFTEST': '1'}, clear=True)
        self.env.start()
        self.root = Path(tempfile.mkdtemp(dir=SCRATCH/'roots'))
        os.environ['LLMDB_ROOT'] = str(self.root)
        self.oldroot = A.ROOT
        A.ROOT = self.root
        self.out = self.root/'results/c10x_enginepath'
        benchmark=self.root/'experiments/track_c/c10z_astra_benchmark.py'
        benchmark.parent.mkdir(parents=True);benchmark.write_bytes((REAL/'experiments/track_c/c10z_astra_benchmark.py').read_bytes())
        self.H = stub_h()
        A.configure(self.H)
    def tearDown(self):
        A.release(self.H)
        A.ROOT = self.oldroot
        self.env.stop()
    def outcome(self, f=None):
        out = R.read_record(f or fixture())
        self.assertIsInstance(out, dict)
        return out


class ReaderTests(IsolatedCase):
    def test_reader_law3_boundaries(self):
        for field, values, bounds in [('para_full_n', [4, 5, 18, 19], (5, 18)),
                                     ('canon_full_n', [4, 5, 10, 11], (5, 10)),
                                     ('para_first_n', [41, 42, 59, 60], (42, 59))]:
            for value in values:
                with self.subTest(field=field, value=value):
                    a = fixture_recipe(value if field == 'para_full_n' else 10,
                                       value if field == 'canon_full_n' else 8,
                                       value if field == 'para_first_n' else 48)
                    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
        for arm in ARM_NAMES[:2]:
            for n in [67, 68]:
                a = fixture_recipe(control=n)
                self.assertEqual(R.law3(a), n == 68)

    def test_reader_control_boundaries(self):
        for recipe in ('I-2', 'I-1'):
            for n in (67, 68):
                f = fixture(); f['recipes'][recipe] = fixture_recipe(30, control=n)
                out = self.outcome(f)['arms'][recipe]
                self.assertEqual(out['base'], 'INVALID-CONTROLS' if n == 67 else 'LEAD')
                self.assertEqual(out['eligible'], n == 68)

    def test_reader_count_classes(self):
        for a, c, label in [(5,18,'NULL'), (9,19,'PARTIAL'), (10,19,'NULL'),
                             (18,27,'NULL'), (18,28,'PARTIAL'), (18,29,'PARTIAL'), (18,30,'LEAD')]:
            f = fixture(); f['recipes']['A'] = fixture_recipe(a); f['recipes']['I-2'] = fixture_recipe(c)
            self.assertEqual(self.outcome(f)['arms']['I-2']['base'], label)
        for c, below in [(8, True), (9, False)]:
            f = fixture(); f['recipes']['A'] = fixture_recipe(18); f['recipes']['I-2'] = fixture_recipe(c)
            self.assertEqual('-BELOW-BASELINE' in self.outcome(f)['arms']['I-2']['qualifiers'], below)

    def test_reader_locality_boundaries(self):
        cases = [('L1_flipped_to_edited_value', 1, 2), ('L3_top1_agree', 29, 28), ('generic_ppl_post',10.5,10.51)]
        for field, yes, no in cases:
            for value, label in [(yes, 'LEAD'), (no, 'TRADEOFF')]:
                f=fixture(); f['recipes']['I-2']['arms'][ARM_NAMES[2]]['locality_axes'][field]=value
                self.assertEqual(self.outcome(f)['arms']['I-2']['base'], label)
        for frame in fixture()['frames']:
            for n,label in [(1,'LEAD'),(2,'TRADEOFF')]:
                f=fixture(); f['recipes']['I-2']['arms'][ARM_NAMES[2]]['extra']['frames'][frame]['flips']=n
                self.assertEqual(self.outcome(f)['arms']['I-2']['base'],label)
        for v,label in [(96.,'LEAD'),(95.99,'TRADEOFF')]:
            f=fixture(); f['recipes']['I-2']['arms'][ARM_NAMES[2]]['locality_described_as']=v
            self.assertEqual(self.outcome(f)['arms']['I-2']['base'],label)

    def test_reader_qualifier_boundaries(self):
        for value, qualified in [(1.5,False),(1.5000001,True)]:
            f=fixture(); f['recipes']['I-2']['write_norms_float64'][ARM_NAMES[2]]={str(l):value for l in range(4,9)}
            self.assertEqual('-LARGE-WRITE' in self.outcome(f)['arms']['I-2']['qualifiers'],qualified)
        for n in (21,22):
            f=fixture(); f['targets']['engine4']['a7_fit']=[.98]*n+[.979]*(24-n)
            self.assertEqual('-UNDERFIT' in self.outcome(f)['arms']['I-2']['qualifiers'],n==21)

    def test_reader_replication(self):
        for first,second,expected in [(30,30,'LEAD'),(30,28,'PARTIAL'),(28,30,'PARTIAL'),(28,28,'PARTIAL'),(30,18,'LEAD-NOT-REPLICATED')]:
            f,g=fixture(),fixture();g.update(process=2,run_id='p2',pid=102)
            f['recipes']['I-2']=fixture_recipe(first);g['recipes']['I-2']=fixture_recipe(second)
            out=R.combine(f,g);self.assertIsInstance(out,dict)
            self.assertEqual(out['arms']['I-2']['label'],expected)
        for qualifier in ('size','fit'):
            f,g=fixture(),fixture();g.update(process=2,run_id='p2',pid=102)
            if qualifier=='size':g['recipes']['I-2']['write_norms_float64'][ARM_NAMES[2]]={str(l):2. for l in range(4,9)}
            else:g['targets']['engine4']['a7_fit']=[.9]*24
            out=R.combine(f,g);self.assertIsInstance(out,dict)
            self.assertTrue(out['arms']['I-2']['label'].endswith('-NOT-REPLICATED'))
            self.assertEqual(out['arms']['I-1']['label'],'PARTIAL')

    def test_reader_interpretation_and_null_table(self):
        for arm,values in [('I-2',[5,6,9,10]),('I-1',[-6,-5,5,6])]:
            for d in values:
                f=fixture();f['recipes'][arm]=fixture_recipe(10);f['inject'][arm]=50-d
                o=self.outcome(f)['arms'][arm]
                expected=('TARGET-WEAKER' if d>=10 else 'INTERMEDIATE' if d>=6 else 'NO-DEFICIT') if arm=='I-2' else ('WEAKER' if d>=6 else 'STRONGER' if d<=-6 else 'NON-INTERPRETED')
                self.assertEqual(o['null_row'],expected)
                self.assertEqual(o['interpretation_row'],7)
        f=fixture();f['targets']['engine4']['a7_fit']=[.9]*24
        f['recipes']['I-2']['write_norms_float64'][ARM_NAMES[2]]={str(l):2. for l in range(4,9)}
        self.assertEqual(self.outcome(f)['arms']['I-2']['interpretation_row'],3)

    def test_reader_validity(self):
        mutations=[lambda f:f.update(status='HALTED'),lambda f:f['fingerprint'].update(ok=False),
                   lambda f:f['fingerprint'].update(_cov_cpu=2),lambda f:f['w0']['checkpoints'][0].update(ok=False),
                   lambda f:f['sources_end'].update(source='b'*64),lambda f:f.update(prereg_sha256='bad')]
        for mutate in mutations:
            f=fixture();mutate(f);self.assertEqual(self.outcome(f)['status'],'INVALID')
        for key in fixture()['inertness']:
            f=fixture();f['inertness'][key]['ok']=False;self.assertEqual(self.outcome(f)['status'],'INVALID')
        for floor,ok in [(1e-5,True),(1.00001e-5,False)]:
            f=fixture();f['inertness']['X1-i']['floor']=floor;self.assertEqual(self.outcome(f)['status']=='VALID',ok)
        for n,ok in [(3,True),(4,False)]:
            f=fixture();f['base_report'][ARM_NAMES[2]]['base']=n;self.assertEqual(self.outcome(f)['status']=='VALID',ok)
        for recipe in ('A','I-2','I-1'):
            f=fixture();f['counters'][recipe]=[9,9];self.assertEqual(self.outcome(f)['status'],'INVALID')
        for key in list(fixture()):
            f=fixture();del f[key];self.assertEqual(self.outcome(f)['status'],'INVALID',key)

    def test_reader_flags_denominators_nulls(self):
        for arm in ARM_NAMES:
            for field in ('canon_n','para_n','para_full_n','para_first_n','para_string_n'):
                f=fixture();f['recipes']['I-2']['arms'][arm][field]+=1
                self.assertEqual(self.outcome(f)['status'],'INVALID')
        for value in (float('nan'),float('inf'),None):
            f=fixture();f['recipes']['I-2']['arms'][ARM_NAMES[2]]['locality_described_as']=value
            self.assertEqual(self.outcome(f)['status'],'INVALID')
        f=fixture();x=f['recipes']['I-2']['arms'][ARM_NAMES[2]];x['para_string_n']=x['para_full_n']-1
        self.assertEqual(self.outcome(f)['status'],'INVALID')
        f=fixture();x=f['recipes']['I-2']['arms'][ARM_NAMES[2]];x.update(tf_pertok_cont=None,tf_continuation_n=0,tf_pertok_cont_reason='zero denominator')
        for row in f['recipes']['I-2']['detail'][ARM_NAMES[2]]:row.update(ntok=1,tf_total=0)
        self.assertEqual(self.outcome(f)['status'],'VALID')

    def test_reader_process_combination(self):
        f,g=fixture(),fixture();g.update(process=2,run_id='p2',pid=102)
        self.assertIsInstance(R.combine(f,g),dict)
        for key in g['identity']:
            bad=copy.deepcopy(g);bad['identity'][key]='changed'
            with self.assertRaises(ValueError):R.combine(f,bad)
        for key,value in [('run_id','p1'),('pid',101),('process',1),('telemetry',True)]:
            bad=copy.deepcopy(g);bad[key]=value
            with self.assertRaises(ValueError):R.combine(f,bad)
        with self.assertRaises(ValueError):R.combine(f,f)
        for key in ('ctx','frames','ctx_sha256','frames_sha256'):
            with self.subTest(key=key):
                bad=copy.deepcopy(g)
                if key=='ctx':bad[key][1][0]+=' changed'
                elif key=='frames':bad[key][1]+=' changed'
                else:bad[key]='b'*64
                with self.assertRaises(ValueError):R.combine(f,bad)
        same_bad=copy.deepcopy(f);same_bad['ctx'][1][0]+=' changed'
        same_bad['frames']=[c.format(CANON) for group in same_bad['ctx'] for c in group]
        same_bad['ctx_sha256']=A.json_sha(same_bad['ctx']);same_bad['frames_sha256']=A.json_sha(same_bad['frames'])
        for record in same_bad['recipes'].values():
            for arm in ARM_NAMES:record['arms'][arm]['extra']['frames']={frame:{'flips':0,'n':6} for frame in same_bad['frames']}
        second_bad=copy.deepcopy(same_bad);second_bad.update(process=2,run_id='p2',pid=102)
        with self.assertRaises(ValueError):R.combine(same_bad,second_bad)
        bad=copy.deepcopy(g);bad['targets']['engine8']['sha256']='b'*64
        self.assertIsInstance(R.combine(f,bad),dict)


class SeamTests(IsolatedCase):
    def test_dispatch_call_time_flag(self):
        hp=self.H.hp; reqs=[self.H.req(CANON,'S0','valueS0')]; P=[torch.eye(2) for _ in hp.layers]
        calls=[];A.ORIGINAL_EDIT=lambda *x:calls.append('original') or {}
        A.FE_STATE=None;self.assertEqual(A.dispatch(hp,reqs,P,[torch.zeros(2,2) for _ in hp.layers]),{})
        A.FE_STATE={};self.H._LAW5_DEFAULT_CTX=True
        self.assertEqual(A.dispatch(hp,reqs,P,[torch.zeros(2,2) for _ in hp.layers]),{})
        self.assertEqual(calls,['original','original'])
        self.H._LAW5_DEFAULT_CTX=False
        with patch.object(A,'fe_edit',return_value={}):A.dispatch(hp,reqs,P,[torch.zeros(2,2) for _ in hp.layers])
        self.assertEqual(A.FE_CALLS,1)

    def test_fe_modes_and_keys(self):
        hp=self.H.hp;rq=[self.H.req(CANON,'S0','valueS0')];P=[torch.eye(2) for _ in hp.layers]
        A.IN_RECIPE=True
        with self.assertRaises(I.Halt):A.fe_edit(hp,rq,P,[torch.zeros(2,2) for _ in hp.layers],mode='identity')
        A.IN_RECIPE=False;A.FE_TARGETS={}
        with self.assertRaises(I.Halt):A.fe_edit(hp,rq,P,[torch.zeros(2,2) for _ in hp.layers])
        A.FE_TARGETS={('S0',' valueS0'):{i:torch.zeros(2) for i in range(5)}}
        with self.assertRaises(I.Halt):A.fe_edit(hp,rq,P,[torch.zeros(2,2) for _ in hp.layers])

    def test_fe_ast_three_changes(self):
        self.assertTrue(A.verify_fe_ast(REAL/'experiments/track_c/c10e_bandknob.py'))

    def test_active_null_negative_controls(self):
        cur={l:torch.tensor([[l+1.,l+2.],[l+3.,l+4.]]) for l in range(4,9)}
        self.assertTrue(I.active_null_structure(cur,cur,cur,['s0','s1'],['s0','s1'])['ok'])
        for wrong in ({l:cur[8] for l in cur},{l:cur[l].flip(0) for l in cur}):
            with self.assertRaises(I.Halt):I.active_null_structure(wrong,cur,cur,['s0','s1'],['s0','s1'])

    def test_tolerance_and_finiteness(self):
        a=torch.tensor([10000.,0.]);self.assertEqual(I.parity(a,a,1e-5)['tol'],1e-4)
        self.assertTrue(I.parity(a,torch.tensor([10001.,0.]),0.)['ok'])
        with self.assertRaises(I.Halt):I.parity(a,torch.tensor([10001.,.001414214]),0.)
        with self.assertRaises(I.Halt):I.parity(a,a,1.00001e-5)
        self.assertTrue(I.parity(torch.zeros(2),torch.zeros(2),0.)['ok'])
        for b in (torch.ones(2),torch.tensor([float('nan'),0.])):
            with self.assertRaises(I.Halt):I.parity(torch.zeros(2),b,0.)
        fake=types.SimpleNamespace(device=types.SimpleNamespace(type='mps'),dtype=torch.float64)
        with self.assertRaises(I.Halt):I.reject_mps_double(fake)

    def test_pristine_hash_restore_hooks(self):
        a=torch.tensor([1.,2.]);self.assertIsInstance(I.tensor_sha(a),str)
        self.assertNotEqual(I.tensor_sha(a),I.tensor_sha(a.double()))
        self.assertNotEqual(I.tensor_sha(a),I.tensor_sha(a.reshape(1,2)))
        pristine=I.Pristine(self.H,self.H.hp)
        self.assertIsInstance(pristine,I.Pristine)
        with self.assertRaisesRegex(RuntimeError,'injected'):
            with pristine.cell('injected'):
                with torch.no_grad():self.H.model.model.layers[4].mlp.down_proj.weight.add_(1.)
                raise RuntimeError('injected')
        self.assertTrue(pristine.verify('restored')['ok'])
        h=self.H.model.model.layers[4].register_forward_hook(lambda *x:None)
        try:
            with self.assertRaises(I.Halt):pristine.verify('leftover')
        finally:h.remove()

    def test_capture_bindings_identity_attribution(self):
        for writer in (self.H.my_edit,A.fe_edit):
            ns=writer.__globals__; original=ns['upd_matrix_match_shape'];x=torch.ones(2,2)
            with I.capture_updates(writer,[4],{'writer':writer.__name__,'check':'test','recipe':'A','arm':'A7'}) as records:
                y=ns['upd_matrix_match_shape'](x,x.shape)
                self.assertIs(y,x)
            self.assertEqual(len(records),1)
            self.assertEqual(records[0]['layer'],4)
            self.assertIs(ns['upd_matrix_match_shape'],original)
            with self.assertRaises(I.Halt):
                with I.capture_updates(writer,[4],{'writer':writer.__name__,'check':'test','recipe':'A','arm':'A7'}):pass
            self.assertIs(ns['upd_matrix_match_shape'],original)

    def test_recipe_states_counters(self):
        pristine=I.Pristine(self.H,self.H.hp)
        seen=[]
        def run(name,path):
            seen.append((name,A.FE_STATE,self.H.Z_OVERRIDE,A.FE_CALLS,self.H.Z_OVERRIDE_HITS))
            A.FE_CALLS=3 if name=='I-2' else 0
            self.H.Z_OVERRIDE_HITS=3 if name=='I-1' else 0
            return fixture_recipe()
        self.H.run_recipe=run
        for name in ('A','I-2','I-1'):
            result=A.recipe(self.H,name,self.root/'hp.json',{'targets':{}},{},pristine)
            self.assertIsInstance(result,dict)
            self.assertIsNone(A.FE_STATE);self.assertIsNone(self.H.Z_OVERRIDE)
        self.assertEqual([x[0] for x in seen],['A','I-2','I-1'])
        self.assertTrue(all(x[3:]==(0,0) for x in seen))

    def test_baseline_miss_stops_candidates(self):
        def miss(name,path):
            recorded=R.strict_json((self.out/'context_templates.json').read_bytes())
            self.assertEqual(recorded['source']['c10q_context_sha256'],A.C10Q_CONTEXT_SHA)
            self.assertEqual(recorded['ctx'],self.H.get_context_templates(self.H.model,self.H.tok))
            return fixture_recipe(4)
        self.H.run_recipe=miss
        with patch.object(A,'construct_targets') as targets,patch.object(A,'injection_screen') as injection:
            result=A.run(self.out,self.H,go={'process':1},process=1,preflight=False)
            self.assertIsInstance(result,dict)
            self.assertEqual(result['status'],'HALTED')
            self.assertEqual(result['code'],'LAW3_BASELINE_MISS')
            targets.assert_not_called();injection.assert_not_called()
            self.assertTrue(list((self.root/'architecture_profile').glob('c10x_halt_diagnostic_*.json')))

    def test_launch_refusals(self):
        with self.assertRaises(ValueError):A.launch_preflight(self.out,None,1)
        with self.assertRaises(ValueError):A.selftest_root(REAL)
        self.assertEqual(A.selftest_root(self.root),self.root)
        self.out.mkdir(parents=True)
        with self.assertRaises(ValueError):A.refuse_existing(self.out)
        with self.assertRaises(I.Halt):A.verify_sources({'a':'a'},{'a':'b'})

    def test_watchdog_and_projection(self):
        self.assertTrue(A.project(2.,2.,4.,2.)['ok'])
        with self.assertRaises(I.Halt):A.project(2.001,2.,4.,2.)
        with self.assertRaises(I.Halt):A.project(2.,2.,3.9,2.)
        argv=('/bin/sleep','30');ALLOWED_CHILDREN.add(argv)
        env={**os.environ,'LLMDB_ROOT':str(self.root)}
        start=time.monotonic()
        rec=A.supervise_child(list(argv),self.root,env,self.root/'watchdog.json',stage_seconds=2.,process_seconds=10.)
        self.assertIsInstance(rec,dict)
        self.assertEqual(rec['status'],'HALTED');self.assertEqual(rec['completion'],'incomplete')
        self.assertLess(time.monotonic()-start,5.)

    def test_process2_requires_eligibility(self):
        f=fixture();f['recipes']['I-2']=fixture_recipe(10);f['recipes']['I-1']=fixture_recipe(10)
        with self.assertRaises(ValueError):A.process2_admission(f)
        self.assertTrue(A.process2_admission(fixture()))

    def test_knobs_and_frame_subjects(self):
        source=ast.parse((REAL/'experiments/track_c/c10p_twopass_arms.py').read_text())
        want=ast.literal_eval(next(n.value for n in source.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FRAME_SUBJECTS' for t in n.targets)))
        self.assertEqual(A.FRAME_SUBJECTS,want)
        for knob in ('MODEL_ID','MODEL_REV','C10_PROJECTOR','N_EDIT','C10_SUBJECT_OFFSET','C10_CTX_TEMPLATES','C10_KEY_LOCUS','RUN_LABEL'):
            with patch.dict(os.environ,{knob:'anything'}):
                with self.assertRaises(ValueError):A.environment_preflight()
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaises(ValueError):A.environment_preflight()

    def test_solver_ast_and_gradients(self):
        self.assertTrue(Z.verify_solver_ast(REAL/'memit_dry_run/memit/memit/compute_z.py'))
        for y,lam,eps in [(0,.1,0.),(1,.1,0.),(0,1.,0.)]:
            s=torch.tensor([[[3.,2.,0.,-1.]]],requires_grad=True);labels=torch.tensor([[y]])
            lp=s.log_softmax(-1);ce=-lp.gather(2,labels.unsqueeze(2)).squeeze(2)
            loss,audit=Z.token_losses(s,lp,labels,ce,lam,eps,.5)
            self.assertIsInstance(audit,dict)
            loss.sum().backward()
            expected=s.detach().softmax(-1)-audit['pi_tar'].reshape_as(s)
            self.assertLessEqual(float((s.grad-expected).abs().max()),1e-6)
            self.assertFalse(audit['pi_tar'].requires_grad)
            if lam==1.:self.assertTrue(torch.equal(audit['extra'],torch.zeros_like(audit['extra'])))
        s=torch.tensor([[[3.,2.,0.,-1.]]],requires_grad=True);lp=s.log_softmax(-1);labels=torch.tensor([[0]])
        ce=-lp[:,:,0];_,aud=Z.token_losses(s,lp,labels,ce,1.,0.,.5)
        loss,_=Z.token_losses(s,lp,labels,ce,1.,float(ce.detach().item()),.5)
        loss.sum().backward();self.assertTrue(torch.equal(s.grad,torch.zeros_like(s)))
        with self.assertRaises(I.Halt):Z.token_losses(torch.zeros(1,1,4),torch.zeros(1,1,4),labels,torch.zeros(1,1),.1,.01,.5)
        s=torch.tensor([[[3.,2.,0.,-1.],[float('nan')]*4]],requires_grad=True)
        labels=torch.tensor([[0,-100]]);lp=torch.log_softmax(s,dim=-1)
        ce=torch.tensor([[.1,0.]],requires_grad=True)
        loss,aud=Z.token_losses(s,lp,labels,ce,.1,.01,.5)
        self.assertTrue(torch.isfinite(loss).all());self.assertEqual(loss[0,1].item(),0.)

    def test_independent_full_vocabulary_audit(self):
        for y in (0,1):
            s=torch.tensor([[3.,2.,0.,-1.]]);lp=s.log_softmax(-1);ce=-lp[:,y]
            a=R.overtone_reference(s,lp,torch.tensor([y]),ce,.1,.01,.5)
            self.assertIsInstance(a,dict)
            l,b=Z.token_losses(s.unsqueeze(0),lp.unsqueeze(0),torch.tensor([[y]]),ce.unsqueeze(0),.1,.01,.5)
            self.assertTrue(torch.equal(a['keep'],b['keep']))
            self.assertTrue(torch.equal(a['mix'],b['mix']))
            self.assertTrue(torch.allclose(a['loss'],l.reshape(-1),atol=1e-6))
        x=torch.cat((torch.linspace(3.,2.,64),torch.full((192,),-1.)))
        y=torch.cat((x[:64],torch.full((192,),-20.)))
        ax=R.overtone_reference(x[None],x[None].log_softmax(-1),torch.tensor([0]),-x[None].log_softmax(-1)[:,0],.1,.01,.5)
        ay=R.overtone_reference(y[None],y[None].log_softmax(-1),torch.tensor([0]),-y[None].log_softmax(-1)[:,0],.1,.01,.5)
        self.assertIsInstance(ax,dict);self.assertIsInstance(ay,dict)
        self.assertFalse(torch.equal(ax['keep'],ay['keep']));self.assertFalse(torch.equal(ax['loss'],ay['loss']))

    def test_float64_dense_reference(self):
        gen=torch.Generator(device='cpu').manual_seed(1008)
        a=torch.randn(2048,11008,generator=gen,device='cpu');b=a.clone();b[::17,::31]+=0.013
        self.assertEqual(I.relative64(a,a),0.);self.assertEqual(I.ratio64(a,a),1.)
        dense=float((a.double()-b.double()).norm()/a.double().norm())
        self.assertLessEqual(abs(I.relative64(a,b)/dense-1.),1e-12)
        ratio=float(a.double().norm()/b.double().norm())
        self.assertLessEqual(abs(I.ratio64(a,b)/ratio-1.),1e-12)


class TelemetryTests(IsolatedCase):
    def test_telemetry_switch_admission(self):
        self.assertEqual(A.telemetry_admission(1,self.out),(False,None))
        for value in ('0','true','',' 1','1'):
            with patch.dict(os.environ,{'C10X_TELEMETRY':value}):
                with self.assertRaises(ValueError):A.telemetry_admission(1,self.out)
        self.assertFalse(self.out.exists())

    def test_telemetry_code_path_equality(self):
        original=self.H.full_seq_match;plain=original(CANON.format('S0'),[7,7]);inputs=[x.tolist() for x in self.H.model.inputs]
        self.H.model.inputs.clear()
        obs=A.observed_scorer(self.H,lambda *x:None)
        self.assertTrue(callable(obs))
        self.assertEqual(obs(CANON.format('S0'),[7,7]),plain)
        self.assertEqual([x.tolist() for x in self.H.model.inputs],inputs)
        self.assertTrue(A.verify_scorer_ast(REAL/'experiments/track_c/c10e_bandknob.py'))
        self.assertIs(self.H.full_seq_match,original)
        self.assertFalse((self.out/'telemetry').exists())

    def test_telemetry_failure_boundaries(self):
        for failure in ('init','write','flush','fsync'):
            buf=io.StringIO()
            with patch.object(sys,'__stderr__',buf):
                if failure=='init':
                    with patch.object(Path,'mkdir',side_effect=OSError('injected')):t=A.Telemetry(self.out,1,'fixed')
                else:
                    t=A.Telemetry(self.out,1,'fixed')
                    if failure=='fsync':
                        with patch.object(os,'fsync',side_effect=OSError('injected')):t.phase('stage_start',stage='setup')
                    else:
                        class Bad:
                            def write(self,s):
                                if failure=='write':raise OSError('injected')
                            def flush(self):raise OSError('injected')
                        t.file=Bad();t.phase('stage_start',stage='setup')
                self.assertFalse(t.enabled);t.phase('stage_end',stage='setup')
                self.assertEqual(buf.getvalue().count('C10X_TELEMETRY_DISABLED'),1)
        t=A.Telemetry(self.out,1,'fixed')
        with patch.object(os,'fsync',side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):t.phase('stage_start',stage='setup')

    def test_telemetry_state_unchanged(self):
        model=self.H.model
        before={n:(x.clone(),x.data_ptr()) for n,x in list(model.named_parameters())+list(model.named_buffers())}
        rng=torch.random.get_rng_state().clone();training=model.training;grad=torch.is_grad_enabled()
        hooks=[(dict(m._forward_hooks),dict(m._forward_pre_hooks),dict(m._backward_hooks)) for m in model.modules()]
        t=A.Telemetry(self.out,1,'fixed');t.logit_lens(self.H,self.H.hp,'pristine')
        self.assertTrue(t.enabled)
        for n,x in list(model.named_parameters())+list(model.named_buffers()):
            self.assertTrue(torch.equal(before[n][0],x));self.assertEqual(before[n][1],x.data_ptr())
        self.assertTrue(torch.equal(rng,torch.random.get_rng_state()));self.assertEqual(training,model.training)
        self.assertEqual(grad,torch.is_grad_enabled())
        self.assertEqual(hooks,[(dict(m._forward_hooks),dict(m._forward_pre_hooks),dict(m._backward_hooks)) for m in model.modules()])

    def test_telemetry_inertness_schedule(self):
        for mode,verdict in [('plain','INERT'),('lens','NOT-INERT'),('drift','NONDETERMINISTIC-BASELINE')]:
            h=stub_h();h.model.change_on_lens=mode=='lens';h.model.drift=mode=='drift'
            out=self.root/'results/c10x_enginepath_telemetry_inertness'/mode
            rec=A.telemetry_mps_inertness_check(h,h.hp,out,'fixed')
            self.assertIsInstance(rec,dict);self.assertEqual(rec['verdict'],verdict)
            self.assertEqual(rec['answer_calls'],96);self.assertEqual(rec['lens_forwards'],48)
        with self.assertRaises(ValueError):T.validate_out(self.root/'results/bad')

    def test_post_run_answer_audit(self):
        expected={('A',ARM_NAMES[2],'S0',CANON):(True,True)}
        line={'kind':'answer','t_utc':'now','elapsed_s':0.,'cumulative_s':0.,'process':1,'run_id':'fixed',
              'recipe':'A','arm':ARM_NAMES[2],'phase':'A','subj':'S0','val':'V0','template':CANON,
              'prompt':CANON.format('S0'),'target_ids':[7], 'generated_ids':[7], 'text':'7','full':True,'first':True}
        header={k:line[k] for k in ('kind','t_utc','elapsed_s','cumulative_s','process','run_id')}
        header.update(kind='header',schema='c10x_enginepath_telemetry/v1',telemetry=True)
        self.assertEqual(T.audit_lines([header,line],expected)['verdict'],'PASS')
        for lines,cause in [([header,line,line],'DUPLICATE'),([header],'MISSING'),
                            ([header,{**line,'full':False}],'MISMATCH'),([line],'MALFORMED'),
                            ([header,{**line,'alien':0}],'UNEXPECTED')]:
            result=T.audit_lines(lines,expected);self.assertIsInstance(result,dict)
            self.assertEqual(result['verdict'],'FAIL');self.assertIn(cause,result['causes'])

    def test_telemetry_line_volume(self):
        t=A.Telemetry(self.out,1,'fixed')
        sink=lambda prompt,targets,gen:t.answer(self.H,'A','A',prompt,targets,gen)
        self.H._ARM_STATE={'requests':[self.H.req(CANON,s,v) for s,v in self.H.ARMS[ARM_NAMES[2]].items()]}
        obs=A.observed_scorer(self.H,sink)
        self.assertTrue(callable(obs))
        for subject in self.H.FICTION:
            for template in [CANON]+PTEST:obs(template.format(subject),[7,7])
        t.write_norms('A',ARM_NAMES[2],'original',{})
        t.target_probs('engine8',[]);t.logit_lens(self.H,self.H.hp,'post')
        t.phase('recipe_end',recipe='A');t.close()
        lines=[json.loads(x) for x in (self.out/'telemetry/telemetry_p1.jsonl').read_text().splitlines()]
        self.assertEqual(sum(x['kind']=='answer' for x in lines),96)
        self.assertEqual(set(x['kind'] for x in lines),{'header','answer','write_norms','target_probs','logit_lens','phase'})
        for line in lines:self.assertEqual(json.loads(json.dumps(line,allow_nan=False)),line)

    def test_strict_json_roundtrips(self):
        obj=fixture();p=self.root/'record.json';A.write_json(p,obj)
        self.assertTrue(p.exists());self.assertEqual(R.strict_json(p.read_bytes()),obj)
        for s in (b'{"x":NaN}',b'{"x":Infinity}',b'{"x":-Infinity}'):
            with self.assertRaises(ValueError):R.strict_json(s)
        with self.assertRaises(FileExistsError):A.write_json(p,obj)

    def test_isolation_positive_control_children_meta(self):
        seen=GUARD_EVENTS;sys.audit('c10x.primary_guard_probe')
        self.assertGreater(GUARD_EVENTS,seen,'primary audit hook was not installed')
        probe=REAL/'results/__c10x_isolation_probe__'
        with self.assertRaises(PermissionError):os.mkdir(probe)
        self.assertFalse(probe.exists())
        for name,value in globals().copy().items():
            if isinstance(value,type) and issubclass(value,unittest.TestCase):
                self.assertTrue(issubclass(value,IsolatedCase),name)
        env={**os.environ,'LLMDB_ROOT':str(self.root)}
        with self.assertRaises(PermissionError):subprocess.Popen([sys.executable,'-B',str(REAL/'experiments/track_c/c10e_bandknob.py')],cwd=self.root,env=env)
        guard=self.root/'guard';guard.mkdir()
        site='import os,sys\nfrom pathlib import Path\nREAL=Path('+repr(str(REAL))+')\nSCRATCH=Path('+repr(str(SCRATCH))+')\nALLOWED_CHILDREN=set()\nGUARD_EVENTS=0\n'+inspect.getsource(audit_guard)+'\nsys.addaudithook(audit_guard)\nprint("C10X_CHILD_GUARD_ACTIVE",flush=True)\n'
        (guard/'sitecustomize.py').write_text(site)
        child=self.root/'stub_worker.py';child.write_text('import os\ntry:\n os.mkdir('+repr(str(probe))+')\nexcept PermissionError:\n print("CHILD_DENIED",flush=True)\nelse:\n raise AssertionError("guard absent")\n')
        argv=(sys.executable,'-B',str(child));ALLOWED_CHILDREN.add(argv)
        result=subprocess.run(argv,cwd=self.root,env={**env,'PYTHONPATH':str(guard)},capture_output=True,text=True,check=True)
        self.assertIn('C10X_CHILD_GUARD_ACTIVE',result.stdout);self.assertIn('CHILD_DENIED',result.stdout)

    def test_frozen_bytes_and_imports(self):
        expected=json.loads((SCRATCH/'before/r5_sha256.json').read_text())
        # Program-authored Amendment P replaces this one pin; other before bytes stay locked.
        expected['docs/C10X_ENGINEPATH_PREREG.md']='43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883'
        for rel,sha in expected.items():
            self.assertEqual(hashlib.sha256((REAL/rel).read_bytes()).hexdigest(),sha,rel)
        for name in FORBIDDEN:self.assertNotIn(name,sys.modules)
        print('IMPORT GUARD PASS: c10e_bandknob, transformers, datasets absent',flush=True)


class IntegrationTests(IsolatedCase):
    def test_three_recipe_telemetry_probe_and_file_equality(self):
        hp=self.H.hp;pristine=I.Pristine(self.H,hp)
        _,probe=A.probe_setup(self.H,[['{}']]);self.H.ARM_HOOKS.append(probe)
        fe={(s,' '+v):{l:torch.tensor([1.,2.]) for l in hp.layers} for values in self.H.ARMS.values() for s,v in values.items()}
        ot={k:torch.tensor([1.,2.]) for k in fe}
        def real_stub_recipe(name,path):
            result=fixture_recipe();result['detail']={};result['delta_norms']={}
            for arm,values in self.H.ARMS.items():
                pristine.restore();rqs=[self.H.req(CANON,s,values[s]) for s in self.H.FICTION]
                self.H._ARM_STATE={'requests':rqs,'hp':hp}
                result['delta_norms'][arm]=self.H.my_edit(hp,rqs,[torch.eye(2) for _ in hp.layers],[torch.zeros(2,2) for _ in hp.layers])
                rows=[]
                for subject in self.H.FICTION:
                    flags=[self.H.full_seq_match(t.format(subject),[7,7]) for t in [CANON]+PTEST]
                    rows.append({'subj':subject,'val':values[subject],'ntok':2,'canon_full':flags[0][0],'canon_first':flags[0][1],
                                 'para_full_hits':[x[0] for x in flags[1:]],'para_first_hits':[x[1] for x in flags[1:]],
                                 'para_string_hits':[x[0] for x in flags[1:]],'tf_correct':0,'tf_total':3})
                result['detail'][arm]=rows
                result['arms'][arm]['extra']={}
                for fn in self.H.ARM_HOOKS:result['arms'][arm]['extra'].update(fn(arm,values))
            return result
        self.H.run_recipe=real_stub_recipe
        off=self.root/'results/off';on=self.root/'results/on';writer=A.Telemetry(on,1,'fixed')
        plain={};observed={}
        try:
            for name in ('A','I-2','I-1'):
                self.H.model.science_inputs.clear();before=self.H.model.science_count
                plain[name]=A.recipe(self.H,name,self.root/'hp.json',fe,ot,pristine)
                inputs=[x.clone() for x in self.H.model.science_inputs];count=self.H.model.science_count-before
                self.H.model.science_inputs.clear();before=self.H.model.science_count
                with patch.object(A,'WATCHDOG_CLOCK',side_effect=AssertionError('telemetry watchdog')),patch.object(A,'project',side_effect=AssertionError('telemetry projection')):
                    observed[name]=A.recipe(self.H,name,self.root/'hp.json',fe,ot,pristine,writer)
                self.assertEqual(plain[name],observed[name]);self.assertEqual(self.H.model.science_count-before,count)
                self.assertEqual(len(inputs),len(self.H.model.science_inputs))
                self.assertTrue(all(torch.equal(x,y) for x,y in zip(inputs,self.H.model.science_inputs)))
                A.write_json(off/(name+'.json'),plain[name]);A.write_json(on/(name+'.json'),observed[name])
            self.assertEqual({p.relative_to(off):p.read_bytes() for p in off.rglob('*.json')},
                             {p.relative_to(on):p.read_bytes() for p in on.rglob('*.json') if 'telemetry' not in p.parts})
            self.assertEqual(sum(x['kind']=='answer' for x in writer.lines),864)
            self.assertEqual(sum(x['kind']=='write_norms' for x in writer.lines),9)
            self.assertEqual(sum(x['kind']=='logit_lens' for x in writer.lines),3)
            first=fixture();second=copy.deepcopy(first);first['recipes']=plain;second['recipes']=observed
            self.assertEqual(R.read_record(first),R.read_record(second))
            self.assertFalse((off/'telemetry').exists());self.assertIs(self.H.full_seq_match,A.ORIGINAL_SCORER)
        finally:
            writer.close();self.H.ARM_HOOKS.remove(probe)

    def test_actual_fe_writes_and_null_solve_observer(self):
        hp=self.H.hp;pristine=I.Pristine(self.H,hp)
        rqs=[self.H.req(CANON,s,self.H.ARMS[ARM_NAMES[2]][s]) for s in self.H.FICTION]
        plain,meta=A.batch_replay(self.H,hp,rqs);null,meta2=A.batch_replay(self.H,hp,rqs,plain[4])
        self.assertEqual(meta,meta2)
        A.FE_TARGETS={(r['subject'],r['target_new']['str']):{l:null[l][i] for l in hp.layers} for i,r in enumerate(rqs)}
        order=[(r['subject'],r['target_new']['str']) for r in rqs]
        with I.observe_null_solve(A.fe_edit,plain,order) as residuals:
            with I.capture_updates(A.fe_edit,hp.layers,{'writer':'fe_edit','check':'X2-vii','recipe':'standalone','arm':'A7'}) as captures:
                A.fe_edit(hp,rqs,[torch.eye(2) for _ in hp.layers],[torch.zeros(2,2) for _ in hp.layers])
        self.assertEqual(len(residuals),5);self.assertTrue(all(x['exact_zero'] for x in residuals))
        self.assertTrue(all(torch.count_nonzero(c['tensor'])==0 for c in captures))
        pristine.verify('null actual')
        A.FE_TARGETS[order[0]][5]=A.FE_TARGETS[order[1]][5]
        with self.assertRaises(I.Halt):
            with I.observe_null_solve(A.fe_edit,plain,order):
                A.fe_edit(hp,rqs,[torch.eye(2) for _ in hp.layers],[torch.zeros(2,2) for _ in hp.layers])
        pristine.restore()

    def test_actual_singleton_reduction_and_resolved_capture(self):
        hp=copy.deepcopy(self.H.hp);hp.layers=[8];pristine=I.Pristine(self.H,self.H.hp)
        rqs=[self.H.req(CANON,s,self.H.ARMS[ARM_NAMES[2]][s]) for s in self.H.FICTION]
        targets={(r['subject'],r['target_new']['str']):torch.tensor([1.,2.]) for r in rqs}
        table={k:{8:v} for k,v in targets.items()}
        plain=I.write_cell(self.H,hp,rqs,[torch.eye(2)],targets,pristine,'singleton original')
        fe=I.write_cell(self.H,hp,rqs,[torch.eye(2)],None,pristine,'singleton FE',table)
        self.assertGreater(I.norm64(plain['updates'][0]['tensor']),0.)
        self.assertTrue(torch.equal(plain['updates'][0]['tensor'],fe['updates'][0]['tensor']))
        self.assertTrue(torch.equal(plain['cache'][0],fe['cache'][0]));self.assertTrue(torch.equal(plain['weights'][8],fe['weights'][8]))
        self.assertEqual(plain['flags'],fe['flags']);pristine.verify('singleton restore')

    def test_telemetry_valid_admission_and_runner_no_writes(self):
        path=self.root/'results/c10x_enginepath_telemetry_inertness/proof/inertness.json'
        sources={'source':'a'*64};env={'stub':'identity'}
        rec={'schema':'c10x_enginepath_telemetry_inertness/v1','device':'mps','decision_id':'D-C10r-rulings-11',
             'verdict':'INERT','control_equal':True,'telemetry_equal':True,'generated_equal':True,
             'telemetry_complete':True,'weights_unchanged':True,'answer_calls':96,'lens_forwards':48,
             'lens_forward_seconds':[.01]*48,'answer_line_seconds':[.001]*96,'sources':sources,'env':env}
        A.write_json(path,rec)
        later=self.root/'results/c10x_enginepath_rerun1'
        with patch.dict(os.environ,{'C10X_TELEMETRY':'1','C10X_TELEMETRY_INERTNESS':str(path)}),patch.object(A,'source_hashes',return_value=sources),patch.object(A,'environment_identity',return_value=env):
            self.assertEqual(A.telemetry_admission(1,later),(True,{'path':str(path),'sha256':A.sha_file(path)}))
            for key in ('control_equal','telemetry_equal','generated_equal','telemetry_complete','weights_unchanged'):
                bad={**rec,key:1};path.write_text(json.dumps(bad))
                with self.assertRaises(ValueError):A.telemetry_admission(1,later)
            path.write_text(json.dumps(rec))
        def forbidden(*args,**kwargs):raise AssertionError('science write called by T8')
        for name in ('my_edit','run_recipe','run_law5','apply_memit_to_model'):setattr(self.H,name,forbidden)
        proof=self.root/'results/c10x_enginepath_telemetry_inertness/runner'
        with patch.object(A,'source_hashes',return_value=sources),patch.object(A,'environment_identity',return_value=env),patch.object(A,'fingerprint',return_value={'ok':True}):
            result=T.run(proof,self.H)
        self.assertEqual(result['verdict'],'INERT');self.assertEqual(result['device'],'cpu')
        self.assertEqual(R.strict_json((proof/'inertness.json').read_bytes()),result)

    def test_telemetry_recipe_records_and_counts_equal(self):
        hp=self.H.hp;pristine=I.Pristine(self.H,hp)
        def real_stub_recipe(name,path):
            result=fixture_recipe();result['detail']={};result['delta_norms']={}
            for arm,values in self.H.ARMS.items():
                pristine.restore();rqs=[self.H.req(CANON,s,values[s]) for s in self.H.FICTION]
                self.H._ARM_STATE={'requests':rqs,'hp':hp}
                result['delta_norms'][arm]=self.H.my_edit(hp,rqs,[torch.eye(2) for _ in hp.layers],[torch.zeros(2,2) for _ in hp.layers])
                rows=[]
                for subject in self.H.FICTION:
                    flags=[self.H.full_seq_match(t.format(subject),[7,7]) for t in [CANON]+PTEST]
                    rows.append({'subj':subject,'val':values[subject],'ntok':2,'canon_full':flags[0][0],'canon_first':flags[0][1],
                                 'para_full_hits':[x[0] for x in flags[1:]],'para_first_hits':[x[1] for x in flags[1:]],
                                 'para_string_hits':[x[0] for x in flags[1:]],'tf_correct':0,'tf_total':3})
                result['detail'][arm]=rows
            return result
        self.H.run_recipe=real_stub_recipe
        baseline_inputs=[]
        with patch.object(A,'WATCHDOG_CLOCK',side_effect=AssertionError('telemetry clock')), patch.object(A,'project',side_effect=AssertionError('telemetry project')):
            pass
        plain=A.recipe(self.H,'A',self.root/'hp.json',None,None,pristine)
        baseline_inputs=[x.clone() for x in self.H.model.inputs];self.H.model.inputs.clear()
        output=self.root/'results/on'
        t=A.Telemetry(output,1,'fixed')
        with patch.object(A,'WATCHDOG_CLOCK',side_effect=AssertionError('telemetry watchdog')), patch.object(A,'project',side_effect=AssertionError('telemetry projection')):
            observed=A.recipe(self.H,'A',self.root/'hp.json',None,None,pristine,t)
        t.close();self.assertEqual(plain,observed)
        self.assertEqual(len(baseline_inputs),len(self.H.model.inputs))
        self.assertTrue(all(torch.equal(a,b) for a,b in zip(baseline_inputs,self.H.model.inputs)))
        self.assertEqual(sum(x['kind']=='answer' for x in t.lines),288)
        self.assertEqual(sum(x['kind']=='write_norms' for x in t.lines),3)
        self.assertEqual(len(t.lines),294) # header + recipe phases + writes + answers
        self.assertIs(self.H.full_seq_match,A.ORIGINAL_SCORER)
        self.assertEqual(R.read_record(fixture()),R.read_record(copy.deepcopy(fixture())))

    def test_solver_masked_gradient_clip_filter_and_tie(self):
        s=torch.tensor([[[3.,2.,0.,-1.],[2.,1.,0.,-2.],[1.,0.,-1.,-2.]],
                        [[1.,2.,3.,4.],[2.,1.,0.,-1.],[4.,3.,2.,1.]]],requires_grad=True)
        labels=torch.tensor([[0,1,-100],[3,-100,-100]]);lp=s.log_softmax(-1)
        safe=labels.clamp_min(0);ce=-lp.gather(2,safe[...,None]).squeeze(-1)
        loss,audit=Z.token_losses(s,lp,labels,ce,.1,.01,.5)
        loss.sum().backward();self.assertTrue(torch.equal(s.grad[labels==-100],torch.zeros_like(s.grad[labels==-100])))
        expected=s.detach()[labels!=-100].softmax(-1)-audit['pi_tar']
        active=audit['kl']>.01;expected=torch.where(active[:,None],expected,0.)
        self.assertLessEqual(float((s.grad[labels!=-100]-expected).abs().max()),1e-6)
        a=torch.tensor([[[3.,2.,0.,-1.]]]);lp=a.log_softmax(-1);lab=torch.tensor([[0]]);ce=-lp[...,0]
        n=float((a.max()-a[0,0,1])/a.std(correction=1))
        _,audit=Z.token_losses(a,lp,lab,ce,.1,.01,n)
        self.assertFalse(bool(audit['keep'][0,1])) # strict equality is excluded
        x=torch.tensor([[[1.,1.,0.,-1.]]]);lp=x.log_softmax(-1);ce=-lp[...,0]
        _,audit=Z.token_losses(x,lp,lab,ce,0.,.01,.5)
        self.assertTrue(bool(audit['mix'][0]));self.assertEqual(audit['pi_tar'][0].argmax().item(),0)

    def test_projection_uses_remaining_units_and_setup_clock(self):
        out=self.root/'results/budget';out.mkdir(parents=True)
        with patch.object(A,'WATCHDOG_CLOCK',return_value=0.):
            budget=A.StageBudget(out,start=0.);budget.enter('targets')
        budget.units['targets']={'solve':[12.]};budget.remaining={'solve':216}
        with patch.object(A,'WATCHDOG_CLOCK',return_value=1.):
            with self.assertRaises(I.Halt):budget.unit(kind='solve')
        with patch.object(A,'WATCHDOG_CLOCK',return_value=123.):
            budget=A.StageBudget(out,start=100.);budget.enter('setup')
            self.assertEqual(budget.stage_start,100.);budget.leave()
            self.assertEqual(budget.timings['setup'],23.)


class FileAdmissionTests(IsolatedCase):
    def test_amendment_p_prereg_pin(self):
        pin='43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883'
        self.assertEqual(A.PIN,pin);self.assertEqual(R.PREREG_SHA256,pin)

    def test_amendment_p_digest_refusals(self):
        ctx,source=A.recorded_contexts()
        self.assertEqual(source['templates_sha256'],'d6c7c70026dced37bddc6adf316a3487d70227dae80a6e0ed5cdabe50caedfa0')
        benchmark=self.root/A.CONTEXT_SOURCE
        original=benchmark.read_text()
        for kind in ('changed_list','nested_digest','flat_digest'):
            with self.subTest(kind=kind):
                out=self.root/'results'/('refused_'+kind)
                if kind=='changed_list':
                    benchmark.write_text(original.replace(ctx[1][0],ctx[1][0]+' changed',1))
                    binding=contextlib.nullcontext()
                elif kind=='nested_digest':binding=patch.object(A,'C10Q_CONTEXT_SHA', '0'*64)
                else:binding=patch.object(A,'json_sha',return_value='0'*64)
                try:
                    with binding,patch.object(self.H,'run_recipe',create=True) as baseline:
                        result=A.run(out,self.H,preflight=False)
                    self.assertEqual(result['status'],'HALTED');baseline.assert_not_called()
                    self.assertTrue(Path(result['diagnostic']).is_file())
                finally:benchmark.write_text(original)

    def test_pinned_processes_and_halted_context_identity(self):
        results=[]
        for process in (1,2):
            harness=stub_h()
            harness.get_context_templates.__globals__['CONTEXT_TEMPLATES_CACHE']=None
            out=self.root/'results'/('pin_process_'+str(process))
            def miss(name,path):
                recorded=R.strict_json((out/'context_templates.json').read_bytes())
                self.assertEqual(harness.get_context_templates(harness.model,harness.tok),recorded['ctx'])
                return fixture_recipe(4)
            harness.run_recipe=miss
            with patch.object(A,'construct_targets') as targets,patch.object(A,'injection_screen') as injection:
                result=A.run(out,harness,process=process,preflight=False)
            self.assertEqual(result['code'],'LAW3_BASELINE_MISS');targets.assert_not_called();injection.assert_not_called()
            saved=R.strict_json((out/'run.json').read_bytes())
            self.assertEqual(saved['ctx'],result['ctx']);self.assertEqual(saved['ctx_sha256'],A.json_sha(saved['ctx']))
            self.assertIsNone(harness.get_context_templates.__globals__['CONTEXT_TEMPLATES_CACHE'])
            results.append(saved)
        self.assertEqual(results[0]['ctx'],results[1]['ctx'])
        self.assertEqual(results[0]['ctx_sha256'],results[1]['ctx_sha256'])

    def test_pinned_contexts_never_sample(self):
        self.assertTrue(callable(getattr(A,'recorded_contexts',None)))
        self.assertTrue(callable(getattr(A,'pinned_contexts',None)))
        ctx,source=A.recorded_contexts()
        self.assertEqual(hashlib.sha256(json.dumps(ctx).encode()).hexdigest(),'c7dabbe7c25a7e58653621d9cc66e37b35c865ae09b73b6a96073a184c6c98da')
        self.assertEqual(A.json_sha(ctx),'eff10db6a89aabf7d67fa0c66e4cc1ac727b795c0bf756d3f8b53d0f6cd05aeb')
        self.assertEqual(source['source_sha256'],A.sha_file(self.root/'experiments/track_c/c10z_astra_benchmark.py'))
        namespace=self.H.get_context_templates.__globals__;namespace['CONTEXT_TEMPLATES_CACHE']=None
        sampler=patch.dict(namespace,{'generate_fast':lambda *args,**kwargs:(_ for _ in ()).throw(AssertionError('sampled'))})
        pristine=I.Pristine(self.H,self.H.hp)
        with sampler,A.pinned_contexts(self.H,ctx),pristine.cell('pinned writer'):
            self.assertEqual(self.H.get_context_templates(self.H.model,self.H.tok),ctx)
            requests=[self.H.req(CANON,s,self.H.ARMS[ARM_NAMES[2]][s]) for s in self.H.FICTION]
            self.H.my_edit(self.H.hp,requests,[torch.eye(2) for _ in self.H.hp.layers],[torch.zeros(2,2) for _ in self.H.hp.layers])
        self.assertIsNone(namespace['CONTEXT_TEMPLATES_CACHE'])

    def test_context_binding_enter_failure_restores(self):
        class RefusedBinding:
            def __enter__(self):raise ValueError('CONTEXT_BINDING_REFUSED')
            def __exit__(self,*args):raise AssertionError('unentered binding exited')
        before=I.Pristine(self.H,self.H.hp)
        with patch.object(A,'pinned_contexts',return_value=RefusedBinding()):
            result=A.run(self.out,self.H,preflight=False)
        self.assertEqual(result['status'],'HALTED')
        self.assertEqual(result['code'],'CONTEXT_BINDING_REFUSED')
        self.assertFalse((self.out/'context_templates.json').exists())
        before.verify('failed pin restored')

    def test_missing_inertness_evidence_is_refused(self):
        f=self.make_files()
        f['inertness']={name:{'ok':True,'floor':0.} for name in R.CHECKS}
        (self.out/'run.json').write_text(json.dumps(f))
        (self.out/'inertness.json').write_text(json.dumps({'manifest':{k:f[k] for k in R.MANIFEST},'inertness':f['inertness']}))
        with patch.object(A,'source_hashes',return_value=f['sources_start']):
            with self.assertRaises(ValueError):R.audited_record(self.out)

    def test_complete_stub_run_persists_every_record(self):
        seed=self.make_files(self.root/'results/fixture_source')
        config=self.root/'configs/hparams/qwen25_3b_memit_hparams.json';config.parent.mkdir(parents=True)
        config.write_text('{"layers":[4,5,6,7,8]}')
        self.H.ID='stub';self.H.REV='revision'
        def scripted_recipe(name,path):
            result=fixture_recipe(10 if name=='A' else 30)
            for arm in ARM_NAMES:
                for row in result['detail'][arm]:row['val']=self.H.ARMS[arm][row['subj']]
                result['arms'][arm]['extra']['frames']={frame:{'flips':0,'n':6} for group in self.H.get_context_templates(self.H.model,self.H.tok) for frame in [c.format(CANON) for c in group]}
            A.FE_CALLS=3 if name=='I-2' else 0;self.H.Z_OVERRIDE_HITS=3 if name=='I-1' else 0
            A.WRITE_NORMS=copy.deepcopy(result['write_norms_float64'])
            return result
        self.H.run_recipe=scripted_recipe
        def targets(out,*args):
            file=A.save_binary(out/'audit.pt',torch.load(self.root/'results/fixture_source/audit.pt',weights_only=True))
            return {'records':seed['targets'],'fe':{},'overtone':{},'audits':{'files':[file],'sha256':A.json_sha([file])}}
        receipt={'sources':seed['sources_start'],'fingerprint':seed['fingerprint'],'process1':None,
                 'telemetry':False,'telemetry_inertness':None,'go_identity':{'path':str(self.root/'go.json'),'sha256':'a'*64}}
        with patch.object(A,'construct_targets',side_effect=targets),patch.object(I,'run_checks',return_value=seed['inertness']),patch.object(A,'injection_screen',return_value={key:{'para_n':50} for key in ('reference','I-2','I-1')}),patch.object(A,'source_hashes',return_value=seed['sources_start']),patch.object(A,'environment_identity',return_value={'python':'stub'}),patch.object(A,'tokenizer_identity',return_value={'artifact':'a'*64}),patch.object(A,'covariance_identity',return_value={str(l):'a'*64 for l in range(4,9)}),patch.object(A,'source_commit',return_value='test-commit'):
            result=A.run(self.out,self.H,receipt=receipt)
            self.assertEqual(result['status'],'COMPLETE',result)
            self.assertEqual(R.strict_json((self.out/'run.json').read_bytes()),result)
            for filename,key in [('targets','targets'),('inertness','inertness'),('inject','inject'),('pass1','recipes')]:
                rec=R.strict_json((self.out/(filename+'.json')).read_bytes())
                self.assertEqual(rec[key],result[key]);self.assertEqual(set(rec['manifest']),set(R.MANIFEST))
            self.assertEqual(R.read_record(result)['status'],'VALID')
            self.assertFalse((self.out/'telemetry').exists())

    def test_deadline_completion_and_previous_overhead(self):
        out=self.root/'results/budget';out.mkdir(parents=True)
        with patch.object(A,'WATCHDOG_CLOCK',return_value=0.):
            budget=A.StageBudget(out);budget.enter('targets')
        with patch.object(A,'WATCHDOG_CLOCK',return_value=2400.001):
            with self.assertRaises(I.Halt):budget.leave()
        first={'inertness':2700.,'work_units':{'inertness':{'solve':[25.]+[20.]*99}}}
        with patch.object(A,'WATCHDOG_CLOCK',return_value=0.):
            budget=A.StageBudget(out,first=first)
            with self.assertRaises(I.Halt):budget.enter('inertness')

    def make_files(self,out=None):
        out=out or self.out;out.mkdir(parents=True)
        f=fixture();f.update(target_hashes={k:v['sha256'] for k,v in f['targets'].items()},
            reviewer={'model':'UNVERIFIABLE','effort':'UNVERIFIABLE'},provenance={'go':{'path':str(self.root/'go.json'),'sha256':'a'*64}})
        f['ctx'],f['context_source']=A.recorded_contexts();f['ctx_sha256']=A.json_sha(f['ctx'])
        f['frames']=[c.format(CANON) for group in f['ctx'] for c in group];f['frames_sha256']=A.json_sha(f['frames'])
        A.write_json(out/'context_templates.json',{'schema':'c10x_context_templates/v1','ctx':f['ctx'],'ctx_sha256':f['ctx_sha256'],'source':f['context_source']})
        f['identity']['covariance']={str(l):'a'*64 for l in range(4,9)}
        self.complete_evidence(f)
        nctx=len(f['frames']);logits=torch.zeros(nctx*2,151936);logits[:,0]=3.;logits[:,1]=2.
        lp=logits.log_softmax(-1);labels=torch.tensor([0,1]*nctx);ce=-lp.gather(1,labels[:,None]).squeeze(1)
        loss,audit=Z.token_losses(logits[None],lp[None],labels[None],ce[None],.1,.01,.5)
        snaps=[]
        for arm in (ARM_NAMES[0],ARM_NAMES[2]):
            for at in ('initial','final'):
                snaps.append({'arm':arm,'subject':'Zorbland','at':at,'logits':logits,'log_probs':lp,
                              'labels':labels,'ce':ce,'row_map':[row for row in range(nctx) for _ in range(2)],'position_map':[0,1]*nctx,
                              'mask':torch.ones(nctx,2,dtype=torch.bool),'dtype':str(logits.dtype),'settings':{'lam':.1,'eps':.01,'n_sigma':.5},
                              'observed':{k:audit[k].detach() for k in ('keep','mix','pi_tar','loss')}})
        file=A.save_binary(out/'audit.pt',{'snapshots':snaps});f['audits']={'files':[file],'sha256':A.json_sha([file])}
        manifest={k:f[k] for k in R.MANIFEST}
        for filename,key in [('targets','targets'),('inertness','inertness'),('inject','inject'),('pass1','recipes')]:
            A.write_json(out/(filename+'.json'),{'manifest':manifest,key:f[key]})
        A.write_json(out/'run.json',f)
        A.write_json(out.with_name(out.name+'_logs')/'supervisor.json',
                     {'status':'COMPLETE','completion':'complete','exit_code':0,'out':str(out),'process':1,'run_id':f['run_id'],'elapsed_seconds':8.})
        return f

    def complete_evidence(self,f):
        sha='a'*64;layers=[str(l) for l in range(4,9)];nctx=len(f['frames'])
        f['identity']['templates']={'CANON':CANON,'PTEST':PTEST}
        f['identity']['software']={key:'stub' for key in ('python','machine','platform','torch','transformers','model_rev')}
        f['identity']['software']['model_rev']=f['identity']['model_rev']
        f['sources_start']={'configs/hparams/qwen25_3b_memit_hparams.json':sha,'docs/C10X_ENGINEPATH_PREREG.md':A.PIN,A.CONTEXT_SOURCE:f['context_source']['source_sha256']}
        f['sources_end']=copy.deepcopy(f['sources_start'])
        subjects=['Zorbland']+['S'+str(i) for i in range(1,24)]
        f['identity']['stimuli']={arm:[{'subj':s,'val':arm+'value'+s} for s in subjects] for arm in ARM_NAMES}
        requests=[[s,' '+arm+'value'+s] for arm in ARM_NAMES for s in subjects]
        def parity(arithmetic='cpu_float64'):
            return {'ok':True,'floor':0.,'tol':1e-4,'relative':0.,'max_abs':0.,'arithmetic':arithmetic,
                    'report_only_fp32':{'relative':0.,'max_abs':0.,'opposite_tolerance_result':False}}
        def captures(writer,check,selected=range(4,9),zero=False):
            return [{'writer':writer,'check':check,'recipe':'standalone','arm':'A7','layer':l,
                     'norm_float64':0. if zero else 1.,'report_only_norm_fp32':0. if zero else 1.,'sha256':sha} for l in selected]
        def residual():
            return {'rho':{l:0. for l in layers},'target_sha256':sha,'cur_before_sha256':sha,'cur_after_sha256':sha,'end_ratio':0.,
                    'applied_difference_report_only':{l:{'norm_float64':0.,'weight_norm_before_float64':1.} for l in layers}}
        for name,table in f['targets'].items():
            keys=layers if name=='engine4' else ['target']
            table['entries']=[{'request':rq,'layers':{l:{'sha256':sha,'norm_float64':1.} for l in keys}} for rq in requests]
            table['sha256']=A.json_sha(table['entries']);table['diagnostics']=[]
            for j,rq in enumerate(requests):
                fit=.98 if name!='engine4' or j<70 else .97
                diag={'request':rq,'fit':fit,'steps':1,'stop_reason':'total loss < 0.05','total_loss_at_stop':.04,
                      'norm_float64':1.,'sha256':sha,'stdout':'loss 0.040 = 0.040 + 0.000 + 0.000 avg prob of [value] '+str(fit)+'\n',
                      'target_init':{'sha256':sha,'norm_float64':1.,'shape':[nctx+1,2,2],
                                     'input_ids':[[1,0]]*(nctx+1),'attention_mask':[[1,1]]*(nctx+1),
                                     'contexts':f['ctx'],'lookup_index':0,'dtype':'torch.float32'}}
                if name=='engine4':diag['target_init_vs_canonical']={'distance_float64':0.,'canonical_sha256':sha,'canonical_batch_shape':[24,2],'scope':'fixture diagnostic'}
                if name=='overtone':diag['per_position_at_stop']={'step':0,'probabilities':[.98]*(nctx*2),'positions':[[row,p] for row in range(nctx) for p in range(2)],'prompts':[frame.format(rq[0]) for frame in f['frames']]}
                table['diagnostics'].append(diag)
            if name=='engine4':
                table['a7_fit']=[d['fit'] for d in table['diagnostics'][48:]]
                table['replay_identity']={arm:{'input_ids':[[1,1]]*24,'attention_mask':[[1,1]]*24,'padding_side':'right','indices':[0]*24,'requests':requests[j*24:(j+1)*24]} for j,arm in enumerate(ARM_NAMES)}
                table['endpoint_distance_ratio_float64']={arm:0. for arm in ARM_NAMES}
        f['target_hashes']={k:v['sha256'] for k,v in f['targets'].items()}
        checks=f['inertness']
        checks['X1-i']={'ok':True,'floor':0.,'arithmetic':'frozen_cpu_float32'}
        checks['X1-ii']={'ok':True,'floor':0.,'cells':[parity('frozen_cpu_float32') for _ in range(72)],'steps_reference':[1]*72,'steps_candidate':[1]*72}
        checks['X1-iii']={'ok':True,'cells':[{'arm':arm,'subject':'Zorbland','at':at,'relative_max':0.,'max_abs':0.,'pi_tar_max_abs_report_only':0.,'ideal_fp32_kl_report_only':[.1]*(nctx*2)} for arm in (ARM_NAMES[0],ARM_NAMES[2]) for at in ('initial','final')]}
        checks['X1-v']={'ok':True,'max_abs':0.,'scope':'synthetic fixture'}
        checks['X2-ii']={'ok':True,'floor':0.,'arithmetic':'cpu_float64','first':captures('my_edit','X2-ii first'),'second':captures('my_edit','X2-ii second'),
                         'report_only_fp32':[parity()['report_only_fp32'] for _ in layers],'canon_full_difference':0,'para_full_difference':0}
        for check in ('X1-iv','X2-iii'):checks[check]={'ok':True,'floor':0.,'layers':{l:parity() for l in layers}}
        checks['X2-iii']['rho_A']=residual()
        checks['X2-iv']={'ok':True,'floor':0.,'cells':[{'arm':arm,'layer':l,**parity('frozen_cpu_float32')} for arm in ARM_NAMES for l in list(range(4,9))+list(range(5,9))]}
        checks['X2-v']={'ok':True,'indices':[{'request':rq,'solve_index':0,'injection_index':0} for rq in requests]}
        checks['X2-vi']={'ok':True,'targets':[parity('frozen_cpu_float32') for _ in range(24)],'layers':{'8':parity()},'cache':parity('frozen_cpu_float32'),
                         'reference':captures('my_edit','X2-vi original',[8]),'candidate':captures('fe_edit','X2-vi active',[8]),
                         'applied_weight_exact':True,'greedy_flags_exact':True,'flags_reference':[[False,False] for _ in range(96)],'flags_candidate':[[False,False] for _ in range(96)]}
        checks['X2-vii']={'ok':True,'layers':captures('fe_edit','X2-vii',zero=True),'requests':requests[48:],'weight_identity':True,
                          'residuals':[{'layer':l,'residual_sha256':sha,'exact_zero':True} for l in range(4,9)]}
        distribution=[1.]+[0.]*151935
        checks['G8']={'ok':True,'expr_delta':0.,'loc_delta':0.,'raw_expr_delta':0.,'raw_loc_delta':0.,
                       'reference':{'probability':1.,'locality':100.,'distribution':distribution,'top1':0,'locality_top1':0},
                       'candidate':{'probability':1.,'locality':100.,'distribution':distribution,'top1':0,'locality_top1':0}}
        frame_rows=[{'subj':s,'top1':0,'tok':'0','flip':False} for s in A.FRAME_SUBJECTS]
        pristine_frames={frame:{'flips':0,'n':6,'rows':copy.deepcopy(frame_rows)} for frame in f['frames']}
        for name,recipe in f['recipes'].items():
            recipe['counters']=f['counters'][name];recipe['residual_diagnostics']={arm:residual() for arm in ARM_NAMES}
            recipe['law5_gate'].update(raw_expr_delta=0.,raw_loc_delta=0.,candidate_calls=0)
            for arm in ARM_NAMES:
                for row,identity in zip(recipe['detail'][arm],f['identity']['stimuli'][arm]):row.update(identity)
            extra=recipe['arms'][ARM_NAMES[2]]['extra']
            extra.update(frames=copy.deepcopy(pristine_frames),frames_pristine=copy.deepcopy(pristine_frames),
                         relation_labels={t:{'kind':kind,'flips':0,'pristine':[0]*24,'rows':subjects} for t,kind in [('{} is associated with','bystander'),('{} is a','objective-anchored')]},
                         teacher_forced_curve={str(p):{'correct':0,'n':72} for p in range(2)})
        screens={}
        for name in ('reference','I-2','I-1'):
            rows=[{**identity,'per_template':[True]+[3*j+k<f['inject'][name] for k in range(3)]} for j,identity in enumerate(f['identity']['stimuli'][ARM_NAMES[2]])]
            per={t:sum(row['per_template'][j] for row in rows) for j,t in enumerate([CANON]+PTEST)}
            screens[name]={'canon_n':24,'para_n':f['inject'][name],'per_template':per,'rows':rows}
        f['inject']['details']=screens
        f['write_size_diagnostics']=A.write_size_reports(f['recipes'])
        labels=['before recipe A']
        def cell(name):
            labels.append('before '+name)
            if name.startswith('recipe '):labels.extend(['harness restore']*6)
            if name=='X2-vii null':labels.append('X2-vii exact zero')
            labels.append('after '+name)
        cell('recipe A');cell('target construction');cell('X1-i')
        labels+=['X1-ii '+arm+' '+s for arm in ARM_NAMES for s in subjects]+['before projector']
        for name in ('X2-ii first','X2-ii second','X1-iv','X2-iii','X2-vi builder','X2-vi original','X2-vi active','X2-vii null','G8 engine','G8 active FE'):cell(name)
        labels+=['X2-iv '+arm for arm in ARM_NAMES]+['after inertness']
        cell('injection');cell('recipe I-2');cell('recipe I-1')
        labels+=['after final recipe','closeout restore']
        f['w0']['checkpoints']=[{'checkpoint':label,'ok':True,'hashes':f['w0']['hashes']} for label in labels]
        f['timings']={stage:1. for stage in A.CAPS}
        f['timings']['work_units']={stage:{kind:[.001]*count for kind,count in units.items()} for stage,units in A.UNIT_PLAN.items()}

    def test_detailed_admission_negative_controls(self):
        f=self.make_files();supervisor={'elapsed_seconds':8.}
        controls=[
            ('nested relative',lambda r:r['inertness']['X1-ii']['cells'][17].update(relative=1.000001e-4)),
            ('nested floor',lambda r:r['inertness']['X2-iii']['layers']['5'].update(floor=1.00001e-5)),
            ('capture attribution',lambda r:r['inertness']['X2-ii']['first'][1].update(layer=6)),
            ('singleton zero',lambda r:r['inertness']['X2-vi']['reference'][0].update(norm_float64=0.)),
            ('null residual',lambda r:r['inertness']['X2-vii']['residuals'][3].update(exact_zero=False)),
            ('null update',lambda r:r['inertness']['X2-vii']['layers'][2].update(norm_float64=1e-12)),
            ('fit link',lambda r:r['targets']['engine4']['a7_fit'].__setitem__(0,.97)),
            ('target coverage',lambda r:r['targets']['engine8']['entries'].pop()),
            ('G candidate seam',lambda r:r['recipes']['I-2']['law5_gate'].update(candidate_calls=1)),
            ('frame population',lambda r:r['recipes']['I-1']['arms'][ARM_NAMES[2]]['extra']['frames'][CANON]['rows'].pop()),
            ('curve denominator',lambda r:r['recipes']['A']['arms'][ARM_NAMES[2]]['extra']['teacher_forced_curve']['1'].update(n=71)),
            ('relation kind',lambda r:r['recipes']['A']['arms'][ARM_NAMES[2]]['extra']['relation_labels']['{} is a'].update(kind='bystander')),
            ('injection count',lambda r:r['inject']['details']['I-2'].update(para_n=49)),
            ('missing timing',lambda r:r.__setitem__('timings',{})),
            ('over-cap timing',lambda r:r['timings'].update(targets=2400.001)),
            ('work population',lambda r:r['timings']['work_units']['targets']['solve'].pop()),
            ('W0 hashes',lambda r:r['w0']['checkpoints'][0].pop('hashes')),
        ]
        for name,change in controls:
            bad=copy.deepcopy(f);change(bad)
            with self.subTest(control=name):
                with self.assertRaises(ValueError):R._file_evidence(bad,supervisor)
        boundary=copy.deepcopy(f);boundary['inertness']['X1-ii']['cells'][0]['relative']=1e-4
        boundary['inertness']['X1-iv']['layers']['4']['report_only_fp32'].update(relative=.01,opposite_tolerance_result=True)
        R._file_evidence(boundary,supervisor)
        with self.assertRaises(ValueError):R._file_evidence(f,{'elapsed_seconds':15000.001})

    def test_reader_publishes_invalid_with_exit_zero(self):
        self.make_files();(self.out/'inertness.json').write_text('{}')
        with patch.object(A,'source_hashes',return_value=R.strict_json((self.out/'run.json').read_bytes())['sources_start']),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(R.main(['--out',str(self.out)]),0)
        self.assertEqual(R.strict_json((self.out/'reader.json').read_bytes())['status'],'INVALID')

    def test_admitted_process_pair_and_p2_gate(self):
        first=self.make_files();second_out=self.root/'results/c10x_enginepath_r2'
        with patch.object(A,'source_hashes',return_value=first['sources_start']),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(R.main(['--out',str(self.out)]),0)
            go=self.root/'go2.json';go.write_text(json.dumps({'decision_id':'D-C10x-enginepath','experiment':'C10X','process':2,'recorded_in':'EXPERIMENT_RUNBOOK.md §5.2','at':'2026-10-08T11:00:00+00:00'}))
            with patch.object(A,'fingerprint',return_value=first['fingerprint']):
                receipt=A.launch_preflight(second_out,go,2,self.out)
            self.assertEqual(receipt['process1']['run_id'],first['run_id']);self.assertFalse(second_out.exists())
            second=self.make_files(second_out);second.update(process=2,pid=102,run_id='p2')
            second['provenance']['process1']=str(self.out)
            (second_out/'run.json').write_text(json.dumps(second))
            for filename,key in [('targets','targets'),('inertness','inertness'),('inject','inject'),('pass1','recipes')]:
                (second_out/(filename+'.json')).write_text(json.dumps({'manifest':{k:second[k] for k in R.MANIFEST},key:second[key]}))
            (second_out.with_name(second_out.name+'_logs')/'supervisor.json').write_text(json.dumps({'status':'COMPLETE','completion':'complete','exit_code':0,'out':str(second_out),'process':2,'run_id':'p2','elapsed_seconds':8.}))
            self.assertEqual(R.main(['--out',str(self.out),'--process2',str(second_out)]),0)
        combined=R.strict_json((second_out/'reader.json').read_bytes())
        self.assertEqual(combined['status'],'VALID');self.assertTrue(combined['arms']['I-2']['replicated'])
        self.assertEqual(combined['arms']['I-2']['label'],'LEAD');self.assertEqual(combined['arms']['I-1']['label'],'PARTIAL')

    def test_every_science_record_roundtrip_and_reader_audit(self):
        f=self.make_files()
        with patch.object(A,'source_hashes',return_value=f['sources_start']):
            admitted,diagnostics=R.audited_record(self.out)
            self.assertEqual({k:v for k,v in admitted.items() if k!='_out_dir'},f)
            self.assertEqual(len(diagnostics),4);self.assertEqual(R.read_record(admitted)['status'],'VALID')
            with patch.object(Path,'read_bytes',autospec=True,side_effect=lambda p:p.open('rb').read() if 'telemetry' not in p.parts else (_ for _ in ()).throw(AssertionError('reader touched telemetry'))):
                self.assertEqual(R.load_record(self.out)['_out_dir'],str(self.out))
            for name in ('targets','inertness','inject','pass1'):
                path=self.out/(name+'.json');saved=path.read_bytes();path.write_text('{}')
                try:
                    with self.assertRaises(ValueError):R.load_record(self.out)
                finally:path.write_bytes(saved)
            with patch.object(A,'source_hashes',return_value={'source':'b'*64}):
                with self.assertRaises(ValueError):R.load_record(self.out)
        path=self.out/'audit.pt';path.write_bytes(b'corrupt')
        with patch.object(A,'source_hashes',return_value=f['sources_start']):
            with self.assertRaises(ValueError):R.load_record(self.out)

    def test_supervisor_fail_closed_and_combining_output_path(self):
        f=self.make_files();path=self.out.with_name(self.out.name+'_logs')/'supervisor.json'
        receipt=R.strict_json(path.read_bytes());receipt['status']='HALTED';path.write_text(json.dumps(receipt))
        with patch.object(A,'source_hashes',return_value=f['sources_start']):
            with self.assertRaises(ValueError):R.load_record(self.out)
        source=ast.parse((REAL/'experiments/track_c/c10x_enginepath_read.py').read_text())
        main=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        destinations=[n for n in ast.walk(main) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='destination' for t in n.targets)]
        self.assertEqual(len(destinations),1);self.assertIn('args.process2',ast.unparse(destinations[0]))

    def test_script_alias_and_preflight_refusal_in_isolated_child(self):
        folder=self.root/'experiments/track_c';folder.mkdir(parents=True,exist_ok=True)
        driver=folder/'c10x_enginepath_arms.py';driver.write_bytes((REAL/'experiments/track_c/c10x_enginepath_arms.py').read_bytes())
        for name in ('c10x_enginepath_read.py','c10x_enginepath_inertness.py'):
            (folder/name).write_bytes((REAL/'experiments/track_c'/name).read_bytes())
        child=self.root/'alias_stub.py'
        child.write_text('import runpy,sys\nsys.path.insert(0,'+repr(str(folder))+')\nsys.argv=['+repr(str(driver))+',"--preflight","--out",'+repr(str(self.out))+',"--go",'+repr(str(self.root/'absent.json'))+']\ntry:\n runpy.run_path('+repr(str(driver))+',run_name="__main__")\nexcept SystemExit as e:\n assert e.code==1\nassert sys.modules["c10x_enginepath_arms"].__name__=="__main__"\nassert "c10e_bandknob" not in sys.modules\nprint("SCRIPT_ALIAS_AND_NO_MODEL_PASS")\n')
        argv=(sys.executable,'-B',str(child));ALLOWED_CHILDREN.add(argv)
        result=subprocess.run(argv,cwd=self.root,env=os.environ.copy(),capture_output=True,text=True,check=True)
        self.assertIn('SCRIPT_ALIAS_AND_NO_MODEL_PASS',result.stdout)
        self.assertFalse(self.out.exists());self.assertFalse((self.root/'architecture_profile').exists())

    def test_direct_shell_launchers_are_executable_in_git(self):
        sources=[REAL/'experiments/track_c'/name for name in
                 ('c10x_enginepath_arms.py','c10x_enginepath_telemetry_check.py')]
        sources.append(REAL/'tools/engine_fingerprint.py')
        scripts=set()
        for source in sources:
            tree=ast.parse(source.read_text())
            for node in ast.walk(tree):
                if isinstance(node,ast.Constant) and type(node.value) is str and node.value.endswith('.sh'):
                    scripts.add((REAL/node.value).resolve())
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='subprocess':
                    self.assertFalse(any(k.arg=='shell' and not (isinstance(k.value,ast.Constant) and k.value.value is False) for k in node.keywords))
        launchers=[n for n in ast.parse(sources[0].read_text()).body if isinstance(n,ast.FunctionDef) and n.name in ('watchdog','bounded_answer_audit')]
        commands=[n.value for launcher in launchers for n in ast.walk(launcher) if isinstance(n,ast.Assign) and isinstance(n.value,ast.List) and any(isinstance(t,ast.Name) and t.id in ('argv','preflight_argv') for t in n.targets)]
        self.assertEqual(len(commands),3)
        self.assertTrue(all(ast.unparse(command.elts[0])=='sys.executable' for command in commands))
        if scripts:
            argv=('git','-C',str(REAL),'ls-files','-s','--',*(str(p.relative_to(REAL)) for p in sorted(scripts)))
            ALLOWED_CHILDREN.add(argv)
            output=subprocess.run(argv,cwd=self.root,env=os.environ.copy(),capture_output=True,text=True,check=True).stdout
            modes={line.split('\t',1)[1]:line.split()[0] for line in output.splitlines()}
            for script in scripts:
                self.assertTrue(os.access(script,os.X_OK),str(script)+' is not executable')
                self.assertEqual(modes.get(str(script.relative_to(REAL))),'100755',str(script)+' is not committed executable')
        print('DIRECT SHELL ENTRY POINTS: '+(str(len(scripts))+' executable/index checks PASS' if scripts else 'none; all three supervised commands use sys.executable'),flush=True)


    def test_post_audit_blocks_are_killed_by_final_deadline(self):
        self.assertTrue(callable(getattr(A,'bounded_answer_audit',None)))
        self.out.mkdir(parents=True)
        self.out.with_name(self.out.name+'_logs').mkdir()
        argv=('/bin/sleep','10');ALLOWED_CHILDREN.add(argv)
        original=subprocess.Popen;children=[]
        def launch(*args,**kwargs):
            child=original(argv,cwd=self.root,env=dict(os.environ),start_new_session=True)
            children.append(child);return child
        started=time.monotonic()
        with patch.object(A.subprocess,'Popen',side_effect=launch):
            with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,started+.2,started+10)
        self.assertLess(time.monotonic()-started,2.)
        self.assertEqual(children[0].poll(),-9)

    def test_post_audit_budget_and_disabled_disposition(self):
        self.assertTrue(callable(getattr(A,'bounded_answer_audit',None)))
        self.out.mkdir(parents=True)
        self.out.with_name(self.out.name+'_logs').mkdir()
        A.write_json(self.out/'run.json',{'process':1,'run_id':'audit-stub'})
        A.write_json(self.out/'telemetry/audit.json',{'schema':'c10x_enginepath_telemetry_audit/v1','process':1,'run_id':'audit-stub','verdict':'FAIL','causes':['DISABLED'],'rerun_required':False,'expected_answers':0,'observed_answers':0,'missing_keys':[]})
        child=types.SimpleNamespace(wait=lambda timeout=None:1,poll=lambda:1)
        with patch.object(A.subprocess,'Popen',return_value=child),patch.object(A,'WATCHDOG_CLOCK',return_value=1.):
            self.assertFalse(A.bounded_answer_audit(self.out,10.,10.)['rerun_required'])
        (self.out.with_name(self.out.name+'_logs')/'answer_audit.log').unlink()
        with patch.object(A.subprocess,'Popen',return_value=child),patch.object(A,'WATCHDOG_CLOCK',side_effect=[1.,11.]):
            with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
        with patch.object(A.subprocess,'Popen') as launch,patch.object(A,'WATCHDOG_CLOCK',return_value=10.):
            with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
            launch.assert_not_called()
        for finish,status,exit_code in ((779.,'COMPLETE',0),(781.,'HALTED',1)):
            root=self.root/('parent_'+str(int(finish)))
            out=root/'results/c10x_enginepath';out.mkdir(parents=True)
            A.write_json(out/'run.json',{'status':'COMPLETE','run_id':'stub'})
            A.write_json(out/'stage.json',{'stage':'final','started_monotonic':0.})
            clock={'now':0.}
            preflight=types.SimpleNamespace(returncode=0,communicate=lambda **kw:(b'{"telemetry":true}',b''))
            worker=types.SimpleNamespace(poll=lambda:0,wait=lambda:0)
            def audited(*args):
                self.assertEqual(args[1:],(780.,15000.));clock['now']=finish
                return {'verdict':'FAIL','causes':['DISABLED'],'rerun_required':False}
            with patch.object(A,'ROOT',root),patch.object(A,'WATCHDOG_CLOCK',side_effect=lambda:clock['now']),patch.object(A.subprocess,'Popen',side_effect=[preflight,worker]),patch.object(A,'bounded_answer_audit',side_effect=audited):
                self.assertEqual(A.watchdog(out,root/'go.json',1),exit_code)
            receipt=R.strict_json((out.with_name(out.name+'_logs')/'supervisor.json').read_bytes())
            self.assertEqual(receipt['status'],status);self.assertEqual(receipt['elapsed_seconds'],finish)

    def test_post_audit_startup_consumes_remaining_budget(self):
        self.out.mkdir(parents=True);logs=self.out.with_name(self.out.name+'_logs');logs.mkdir()
        A.write_json(self.out/'run.json',{'process':1,'run_id':'audit-stub'})
        A.write_json(self.out/'telemetry/audit.json',{'schema':'c10x_enginepath_telemetry_audit/v1','process':1,'run_id':'audit-stub','verdict':'PASS','causes':[],'rerun_required':False,'expected_answers':0,'observed_answers':0,'missing_keys':[]})
        clock={'now':1.};timeouts=[]
        def wait(timeout=None):timeouts.append(timeout);return 0
        child=types.SimpleNamespace(wait=wait,poll=lambda:None,pid=12345)
        def launch(*args,**kwargs):clock['now']=3.;return child
        with patch.object(A,'WATCHDOG_CLOCK',side_effect=lambda:clock['now']),patch.object(A.subprocess,'Popen',side_effect=launch):
            A.bounded_answer_audit(self.out,10.,20.)
        self.assertEqual(timeouts,[7.])
        (logs/'answer_audit.log').unlink();timeouts.clear();clock['now']=1.
        def late_launch(*args,**kwargs):clock['now']=11.;return child
        with patch.object(A,'WATCHDOG_CLOCK',side_effect=lambda:clock['now']),patch.object(A.subprocess,'Popen',side_effect=late_launch),patch.object(A.os,'killpg') as killed:
            with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
        killed.assert_called_once_with(child.pid,A.signal.SIGKILL)
        self.assertEqual(timeouts,[None])

    def test_post_audit_rejects_contradictory_receipts(self):
        self.out.mkdir(parents=True);logs=self.out.with_name(self.out.name+'_logs');logs.mkdir()
        (self.out/'telemetry').mkdir()
        A.write_json(self.out/'run.json',{'process':1,'run_id':'audit-stub'})
        base={'schema':'c10x_enginepath_telemetry_audit/v1','process':1,'run_id':'audit-stub','verdict':'PASS','causes':[],'rerun_required':False,'expected_answers':0,'observed_answers':0,'missing_keys':[]}
        cases=[(1,{}),(0,{'verdict':'FAIL','causes':['DISABLED']}),(1,{'verdict':'FAIL','causes':['MISMATCH']}),(1,{'verdict':'FAIL','causes':['MISMATCH','DISABLED']}),(0,{'causes':['DISABLED']}),(1,{'verdict':'FAIL','causes':['UNKNOWN'],'rerun_required':True}),(1,{'verdict':'FAIL','causes':['DISABLED','DISABLED']}),(0,{'causes':None}),(0,{'process':2}),(0,{'run_id':'other'}),(0,{'unexpected':True}),(0,{'expected_answers':True})]
        for code,change in cases:
            with self.subTest(code=code,change=change):
                (self.out/'telemetry/audit.json').write_text(json.dumps({**base,**change}))
                child=types.SimpleNamespace(wait=lambda timeout:code,poll=lambda:code)
                try:
                    with patch.object(A,'WATCHDOG_CLOCK',return_value=1.),patch.object(A.subprocess,'Popen',return_value=child):
                        with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
                finally:(logs/'answer_audit.log').unlink()
        for code,change in ((0,{}),(1,{'verdict':'FAIL','causes':['DISABLED']}),(1,{'verdict':'FAIL','causes':['MISMATCH'],'rerun_required':True})):
            (self.out/'telemetry/audit.json').write_text(json.dumps({**base,**change}))
            child=types.SimpleNamespace(wait=lambda timeout:code,poll=lambda:code)
            with patch.object(A,'WATCHDOG_CLOCK',return_value=1.),patch.object(A.subprocess,'Popen',return_value=child):
                self.assertEqual(A.bounded_answer_audit(self.out,10.,20.)['rerun_required'],change.get('rerun_required',False))
            (logs/'answer_audit.log').unlink()

    def test_late_supervisor_persistence_is_unreadable(self):
        root=self.root/'late_parent';out=root/'results/c10x_enginepath'
        clock={'now':0.};write=A.write_json
        preflight=types.SimpleNamespace(returncode=0,communicate=lambda **kw:(b'{"telemetry":false}',b''))
        worker=types.SimpleNamespace(poll=lambda:0,wait=lambda:0)
        logs=out.with_name(out.name+'_logs')
        logs.parent.mkdir(parents=True)
        def persist(path,record):
            write(path,record)
            if Path(path).name=='supervisor.json':clock['now']=781.
        def finished():
            write(out/'run.json',{'status':'COMPLETE','run_id':'late-stub'})
            write(out/'stage.json',{'stage':'final','started_monotonic':0.})
            clock['now']=779.;return 0
        worker.wait=finished
        with patch.object(A,'ROOT',root),patch.object(A,'WATCHDOG_CLOCK',side_effect=lambda:clock['now']),patch.object(A.subprocess,'Popen',side_effect=[preflight,worker]),patch.object(A,'write_json',side_effect=persist):
            self.assertEqual(A.watchdog(out,root/'go.json',1),1)
        original=R.strict_json((logs/'supervisor.json').read_bytes())
        self.assertEqual(original['status'],'COMPLETE')
        halt=R.strict_json((logs/'supervisor_halt.json').read_bytes())
        self.assertEqual(halt['status'],'HALTED');self.assertEqual(halt['completion'],'incomplete')
        self.assertEqual(halt['elapsed_seconds'],781.)
        f=self.make_files();marker=self.out.with_name(self.out.name+'_logs')/'supervisor_halt.json'
        marker.write_bytes((logs/'supervisor_halt.json').read_bytes())
        with patch.object(A,'source_hashes',return_value=f['sources_start']):
            with self.assertRaisesRegex(ValueError,'supervisor'):R.load_record(self.out)
            marker.unlink();audit=R._audit_snapshot
            def late_marker(*args,**kwargs):
                if not marker.exists():marker.write_text('{}')
                return audit(*args,**kwargs)
            with patch.object(R,'_audit_snapshot',side_effect=late_marker):
                with self.assertRaisesRegex(ValueError,'supervisor'):R.load_record(self.out)


def main():
    (SCRATCH/'roots').mkdir(parents=True,exist_ok=True)
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    after=listing();changes={p:(BEFORE_LISTING.get(p),after.get(p)) for p in set(BEFORE_LISTING)|set(after) if BEFORE_LISTING.get(p)!=after.get(p)}
    violations={p:v for p,v in changes.items() if p.startswith(('results/c10x_','architecture_profile/c10x_','architecture_profile/s')) and ('halt_diagnostic' in p or p.startswith(('results/c10x_','architecture_profile/c10x_')))}
    print('LISTING: attributed-protected changes = '+json.dumps(violations,sort_keys=True))
    other={p:v for p,v in changes.items() if p not in violations}
    if len(other)>20:
        path=SCRATCH/'listing_deltas'/('listing_'+str(time.time_ns())+'.json')
        path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(other,allow_nan=False,sort_keys=True)+'\n')
        print('LISTING: observed/unattributed other changes = '+str(len(other))+' entries; complete delta '+str(path)+'; sha256 '+hashlib.sha256(path.read_bytes()).hexdigest())
    else:
        print('LISTING: observed/unattributed other changes = '+json.dumps(other,sort_keys=True))
    assert not violations,'live protected listing changed'
    for name in FORBIDDEN:assert name not in sys.modules,name
    print('SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent',flush=True)
    return 0 if result.wasSuccessful() else 1


if __name__=='__main__':
    raise SystemExit(main())
