"""C10X numeric gates, pristine checkpoints and attributed update capture."""
import contextlib
import hashlib
import json
import math

class Halt(RuntimeError):
    pass

def require(condition, code):
    if not condition:
        raise Halt(code)

def reject_mps_double(value):
    import torch
    require(not (value.device.type == 'mps' and value.dtype == torch.float64), 'FLOAT64_ON_MPS')

def cpu_copy(value):
    import torch
    reject_mps_double(value)
    out = value.detach().cpu().float().clone()
    require(bool(torch.isfinite(out).all()), 'NONFINITE_TENSOR')
    return out

def norm64(value):
    answer = float(cpu_copy(value).double().norm())
    require(math.isfinite(answer), 'NONFINITE_NORM')
    return answer

def relative64(a, b):
    import torch
    a, b = cpu_copy(a).double(), cpu_copy(b).double()
    require(a.shape == b.shape, 'PARITY_SHAPE')
    if float(a.norm()) == 0.:
        require(torch.equal(a, b), 'ZERO_REFERENCE_MISMATCH')
        return 0.
    rel = float((a-b).norm()/a.norm())
    require(math.isfinite(rel), 'NONFINITE_RELATIVE')
    return rel

def ratio64(a, b):
    numerator, denominator = norm64(a), norm64(b)
    require(denominator > 0., 'ZERO_RATIO_DENOMINATOR')
    result = numerator/denominator
    require(math.isfinite(result), 'NONFINITE_RATIO')
    return result

def parity(a, b, floor, double=True):
    """M1 ΔW inputs upcast; fixed non-ΔW :66 checks retain fp32."""
    import torch
    require(isinstance(floor, (float, int)) and math.isfinite(floor) and 0. <= floor <= 1e-5, 'FLOOR_ABOVE_1E-5')
    tol = max(10*floor, 1e-4)
    # The admitted floor makes this max exactly 1e-4, including its endpoint.
    af, bf = cpu_copy(a), cpu_copy(b)
    require(af.shape == bf.shape, 'PARITY_SHAPE')
    x, y = (af.double(), bf.double()) if double else (af, bf)
    if float(x.norm()) == 0.:
        require(torch.equal(x, y), 'ZERO_REFERENCE_MISMATCH')
        rel = 0.
    else:
        rel = float((x-y).norm()/x.norm())
    maximum = float((x-y).abs().max()) if x.numel() else 0.
    require(math.isfinite(rel) and math.isfinite(maximum), 'NONFINITE_PARITY')
    require(rel <= tol, 'PARITY_ABOVE_TOLERANCE')
    fp32 = float((af-bf).norm()/af.norm()) if float(af.norm()) else 0.
    return {'ok': True, 'floor': floor, 'tol': tol, 'relative': rel, 'max_abs': maximum,
            'arithmetic': 'cpu_float64' if double else 'frozen_cpu_float32',
            'report_only_fp32': {'relative': fp32 if math.isfinite(fp32) else 'NONFINITE',
                                'max_abs': float((af-bf).abs().max()),
                                'opposite_tolerance_result':math.isfinite(fp32) and ((fp32<=tol)!=(rel<=tol))}}

def tensor_sha(value):
    import torch
    t = value.detach().cpu().contiguous()
    h = hashlib.sha256()
    h.update(json.dumps({'dtype': str(t.dtype), 'shape': list(t.shape)}, sort_keys=True).encode())
    h.update(t.view(torch.uint8).numpy().tobytes())
    return h.hexdigest()

def hook_identity(model):
    return [(name, tuple(module._forward_hooks), tuple(module._forward_pre_hooks), tuple(module._backward_hooks))
            for name, module in model.named_modules()]

class Pristine:
    def __init__(self, H, hp):
        self.H, self.hp = H, hp
        npd = dict(H.model.named_parameters())
        self._snapshot = {l: npd[H.weight_name(hp, l)].detach().cpu().clone() for l in hp.layers}
        self.hashes = {str(l): tensor_sha(t) for l, t in self._snapshot.items()}
        self.hooks = hook_identity(H.model)
        self.checkpoints = []
    def restore(self):
        import torch
        with torch.no_grad():
            npd = dict(self.H.model.named_parameters())
            for l, value in self._snapshot.items():
                require(tensor_sha(value) == self.hashes[str(l)], 'PRISTINE_SNAPSHOT_MUTATED')
                npd[self.H.weight_name(self.hp, l)].copy_(value)
    def verify(self, label):
        npd = dict(self.H.model.named_parameters())
        actual = {str(l): tensor_sha(npd[self.H.weight_name(self.hp, l)]) for l in self.hp.layers}
        require(actual == self.hashes, 'W0 '+label)
        require(hook_identity(self.H.model) == self.hooks, 'LEFTOVER_HOOK '+label)
        record = {'checkpoint': label, 'ok': True, 'hashes': actual}
        self.checkpoints.append(record)
        return record
    @contextlib.contextmanager
    def cell(self, label):
        self.verify('before '+label)
        try:
            yield
        finally:
            self.restore()
            self.verify('after '+label)

@contextlib.contextmanager
def capture_updates(writer, layers, attribution, retain=True):
    """Patch each writer's actual resolved binding (M2)."""
    namespace = writer.__globals__
    original = namespace['upd_matrix_match_shape']
    records = []
    require(len(layers) == len(set(layers)), 'CAPTURE_LAYER_IDENTITIES')
    require(all(k in attribution for k in ('writer', 'check', 'recipe', 'arm')), 'CAPTURE_ATTRIBUTION')
    def capture(matrix, shape):
        import sys
        result = original(matrix, shape)
        require(len(records) < len(layers), 'DUPLICATE_UPDATE_CAPTURE')
        frame=sys._getframe(1)
        if attribution['check']!='test':
            require(frame.f_code is writer.__code__ and frame.f_locals.get('layer')==layers[len(records)],'UPDATE_WRITER_LAYER_ATTRIBUTION')
        clone = cpu_copy(result)
        record = {**attribution, 'layer': layers[len(records)], 'norm_float64': norm64(clone),
                  'report_only_norm_fp32': float(clone.norm()), 'sha256': tensor_sha(clone)}
        if retain:
            record['tensor'] = clone
        records.append(record)
        return result
    namespace['upd_matrix_match_shape'] = capture
    try:
        yield records
        require([r['layer'] for r in records] == list(layers), 'MISSING_UPDATE_CAPTURE')
    finally:
        namespace['upd_matrix_match_shape'] = original
        require(namespace['upd_matrix_match_shape'] is original, 'LEFTOVER_UPDATE_CAPTURE')

def active_null_structure(observed, targets, reference, order, expected_order):
    import torch
    require(order == expected_order, 'NULL_COLUMN_IDENTITIES')
    require(set(observed) == set(targets) == set(reference), 'NULL_LAYER_IDENTITIES')
    for l in reference:
        o, t, r = cpu_copy(observed[l]), cpu_copy(targets[l]), cpu_copy(reference[l])
        require(torch.equal(o, r), 'NULL_WRONG_LAYER '+str(l))
        require(torch.equal(t, r), 'NULL_PERMUTED_TARGET '+str(l))
        require(torch.equal(t-o, torch.zeros_like(r)), 'NULL_NONZERO_RESIDUAL '+str(l))
    return {'ok': True, 'layers': list(reference), 'order': list(order)}


@contextlib.contextmanager
def observe_null_solve(writer,observed,expected_order):
    """Check the writer's actual locals immediately before the CPU solve."""
    import sys
    import torch
    namespace=writer.__globals__;original=namespace['torch'];records=[]
    class LinalgProxy:
        def __getattr__(self,name):return getattr(original.linalg,name)
        def solve(self,*args,**kwargs):
            frame=sys._getframe(1);require(frame.f_code is writer.__code__,'NULL_SOLVE_WRITER')
            values=frame.f_locals;layer=values['layer']
            require(values['keys']==expected_order and layer in observed,'NULL_SOLVE_IDENTITIES')
            cur=cpu_copy(values['cur'].T);target=cpu_copy(values['zs'].T)
            active_null_structure({layer:cur},{layer:target},{layer:observed[layer]},expected_order,expected_order)
            expected=(values['zs']-values['cur']).repeat_interleave(values['K'].size(1)//values['cur'].size(1),dim=1)
            require(torch.equal(values['tgt'],expected) and torch.equal(values['resid'],expected),'NULL_ACTUAL_RESIDUAL')
            require(torch.count_nonzero(values['rf'])==0,'NULL_ACTUAL_SOLVE_RESIDUAL')
            records.append({'layer':layer,'residual_sha256':tensor_sha(values['rf']),'exact_zero':True})
            return original.linalg.solve(*args,**kwargs)
    class TorchProxy:
        linalg=LinalgProxy()
        def __getattr__(self,name):return getattr(original,name)
    namespace['torch']=TorchProxy()
    try:yield records
    finally:namespace['torch']=original

def behaviour_gate(reference, candidate):
    expr = abs(reference['probability']-candidate['probability'])
    loc = abs(reference['locality']-candidate['locality'])
    require(math.isfinite(expr) and math.isfinite(loc), 'NONFINITE_G8')
    require(round(expr, 4) < .05 and round(loc, 2) < 3., 'G8_NOT_INERT')
    return {'ok': True, 'expr_delta': round(expr, 4), 'loc_delta': round(loc, 2),
            'raw_expr_delta': expr, 'raw_loc_delta': loc, 'reference': reference, 'candidate': candidate}


def relative_fixed(a,b):
    """The explicitly frozen non-ΔW :66 arithmetic (Amendment M)."""
    import torch
    a,b=cpu_copy(a),cpu_copy(b)
    require(a.shape==b.shape,'FLOOR_SHAPE')
    if float(a.norm())==0.:
        require(torch.equal(a,b),'ZERO_FLOOR_REFERENCE')
        return 0.
    value=float((a-b).norm()/a.norm())
    require(math.isfinite(value),'NONFINITE_FLOOR')
    return value


def clean_capture(records):
    return [{k:v for k,v in r.items() if k!='tensor'} for r in records]


def write_cell(H,hp,requests,P,targets,pristine,check,fe=None,mode='fe'):
    import torch
    import c10x_enginepath_arms as A
    writer=A.ORIGINAL_EDIT if fe is None else A.fe_edit
    old_fe,old_targets,old_override,old_hits=A.FE_STATE,A.FE_TARGETS,H.Z_OVERRIDE,H.Z_OVERRIDE_HITS
    try:
        with pristine.cell(check):
            A.FE_STATE=None if fe is None else {'targets':fe};A.FE_TARGETS=fe or {}
            H.Z_OVERRIDE=targets;H.Z_OVERRIDE_HITS=0;A._refresh_globals()
            cache=[torch.zeros_like(p) for p in P]
            started=A.work_unit(kind='write')
            with contextlib.ExitStack() as stack:
                diagnostics=stack.enter_context(A.write_diagnostics(writer,H,hp,requests,fe)) if check=='X2-iii' else {}
                updates=stack.enter_context(capture_updates(writer,hp.layers,{'writer':writer.__name__,'check':check,'recipe':'standalone','arm':'A7'}))
                legacy=writer(hp,requests,P,cache,mode=mode) if fe is not None else writer(hp,requests,P,cache)
            require([r['layer'] for r in updates]==hp.layers,'WRITE_CAPTURE_ATTRIBUTION')
            weights={l:dict(H.model.named_parameters())[H.weight_name(hp,l)].detach().cpu().clone() for l in hp.layers}
            flags=[H.full_seq_match(t.format(r['subject']),H.tgt_ids(r['target_new']['str'][1:]))
                   for r in requests for t in [H.CANON]+H.PTEST]
            A.end_unit(started)
            return {'updates':updates,'cache':[cpu_copy(c) for c in cache],'weights':weights,'flags':flags,'report_only_harness_fp32':legacy,'residual_diagnostics':diagnostics}
    finally:
        A.FE_STATE,A.FE_TARGETS=old_fe,old_targets
        H.Z_OVERRIDE,H.Z_OVERRIDE_HITS=old_override,old_hits;A._refresh_globals()


def compare_updates(a,b,floor):
    require([x['layer'] for x in a]==[x['layer'] for x in b],'COMPARE_LAYER_IDENTITY')
    return {str(x['layer']):parity(x['tensor'],y['tensor'],floor,double=True) for x,y in zip(a,b)}


def audit_loss_files(files):
    import torch
    from pathlib import Path
    from c10x_enginepath_read import overtone_reference
    records=[]
    for entry in files:
        path=Path(entry['path']);require(hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256'],'AUDIT_HASH')
        data=torch.load(path,map_location='cpu',weights_only=True)
        for snap in data['snapshots']:
            ref=overtone_reference(snap['logits'],snap['log_probs'],snap['labels'],snap['ce'],.1,.01,.5)
            obs=snap['observed']
            require(torch.equal(ref['keep'],obs['keep']) and torch.equal(ref['mix'],obs['mix']),'AUDIT_STRUCTURE')
            # Loss is a scalar at each scored token; :73 fixes the denominator.
            denominator=torch.maximum(ref['loss'].abs(),torch.full_like(ref['loss'],.01)).clamp_min(1e-12)
            rel=(ref['loss']-obs['loss']).abs()/denominator
            require(torch.isfinite(rel).all() and float(rel.max())<=1e-4,'AUDIT_LOSS')
            records.append({'arm':snap['arm'],'subject':snap['subject'],'at':snap['at'],
                            'relative_max':float(rel.max()),'max_abs':float((ref['loss']-obs['loss']).abs().max()),
                            'pi_tar_max_abs_report_only':float((ref['pi_tar']-obs['pi_tar']).abs().max()),
                            'ideal_fp32_kl_report_only':ref['ideal_fp32_kl'].tolist()})
    require(len(records)==4,'AUDIT_FOUR_CELLS')
    return {'ok':True,'cells':records}


def gradient_check():
    import torch
    from c10x_overtone_z import token_losses
    errors=[]
    for label,lam,eps in ((0,.1,0.),(1,.1,0.),(0,1.,0.),(0,1.,10.)):
        s=torch.tensor([[[3.,2.,0.,-1.]]],requires_grad=True)
        lp=s.log_softmax(-1);ids=torch.tensor([[label]]);ce=-lp.gather(-1,ids[...,None]).squeeze(-1)
        loss,audit=token_losses(s,lp,ids,ce,lam,eps,.5);loss.mean().backward()
        expected=(s.detach().softmax(-1)-audit['pi_tar'].reshape_as(s)) if float(audit['kl'][0])>eps else torch.zeros_like(s)
        error=float((s.grad-expected).abs().max());require(error<=1e-6,'OBJECTIVE_GRADIENT')
        require(not audit['pi_tar'].requires_grad,'OBJECTIVE_TARGET_GRADIENT');errors.append(error)
    return {'ok':True,'max_abs':max(errors),'scope':'synthetic CPU fp32 gradient; the full boundary controls also run in the selftest'}


def direct_g8(H,hp,P,ctx,pristine):
    import copy
    import torch
    import c10x_enginepath_arms as A
    hp1=copy.deepcopy(hp);hp1.layers=[8]
    requests=[H.req(H.CANON,'Zorbland','Cairo')]
    prompt=H.CANON.format('Zorbland');local_prompt='Zorbland is described as'
    pre=H.predict(local_prompt)
    def observe():
        predicted=H.predict(prompt);post=H.predict(local_prompt)
        return {'probability':float(predicted['dist'][H.first_tok('Cairo')]),
                'locality':H.locpct({local_prompt:post},{local_prompt:pre},[local_prompt]),
                'distribution':predicted['dist'].detach().cpu().tolist(),
                'top1':int(predicted['dist'].argmax()),'locality_top1':post['id'] if 'id' in post else int(post['dist'].argmax())}
    with pristine.cell('G8 engine'):
        with contextlib.redirect_stdout(__import__('io').StringIO()):
            H.apply_memit_to_model(H.model,H.tok,requests,hp1,copy=False,return_orig_weights=False)
        engine=observe()
    with pristine.cell('G8 active FE'):
        table,_,_=A.fe_builder(H,hp1,requests,ctx)
        old=A.FE_STATE,A.FE_TARGETS
        try:
            A.FE_STATE={'targets':table};A.FE_TARGETS=table;A._refresh_globals()
            A.fe_edit(hp1,requests,[P[hp.layers.index(8)]],[torch.zeros_like(P[hp.layers.index(8)])])
            candidate=observe()
        finally:A.FE_STATE,A.FE_TARGETS=old
    return behaviour_gate(engine,candidate)


def run_checks(H,hp,ctx,targets,pristine,out):
    import copy
    import torch
    import c10x_enginepath_arms as A
    import c10x_overtone_z as Z
    checks={};a7=H.ARMS['A7_coined_coined'];requests=[H.req(H.CANON,s,a7[s]) for s in H.FICTION]
    active_check=None
    def begin(name):
        nonlocal active_check
        if A.TELEMETRY:
            if active_check:A.TELEMETRY.phase('check_end',check=active_check)
            A.TELEMETRY.phase('check_start',check=name)
        active_check=name
    # X1-i calibrates returned-z comparisons from unchanged, identical solves.
    begin('X1-i')
    with pristine.cell('X1-i'):
        twins=[A.solve_target(H,hp,H.req(H.CANON,'Zorbland',a7['Zorbland']),8,ctx)[0] for _ in range(3)]
    floor=max(relative_fixed(twins[i],twins[j]) for i in range(3) for j in range(i+1,3))
    require(floor<=1e-5,'X1_SOLVE_FLOOR');checks['X1-i']={'ok':True,'floor':floor,'arithmetic':'frozen_cpu_float32'}
    begin('X1-ii');reduced={};parities=[];steps_ref=[];steps_candidate=[]
    reference_d={tuple(d['request']):d for d in targets['records']['engine8']['diagnostics']}
    for arm in A.ARM_NAMES:
        for subject in H.FICTION:
            pristine.verify('X1-ii '+arm+' '+subject)
            rq=H.req(H.CANON,subject,H.ARMS[arm][subject]);key=(subject,rq['target_new']['str'])
            z,d,_=A.solve_target(H,hp,rq,8,ctx,Z.compute_z_overtone,{'lam':1.,'eps':0.,'n_sigma':.5})
            reduced[key]=z;parities.append(parity(targets['engine8'][key],z,floor,double=False))
            require(d['steps']==reference_d[key]['steps'],'X1_REDUCTION_STEPS')
            steps_ref.append(reference_d[key]['steps']);steps_candidate.append(d['steps'])
    checks['X1-ii']={'ok':True,'floor':floor,'cells':parities,'steps_reference':steps_ref,'steps_candidate':steps_candidate}
    begin('X1-iii');checks['X1-iii']=audit_loss_files(targets['audits']['files'])
    begin('X1-v');checks['X1-v']=gradient_check()
    pristine.verify('before projector')
    P=H.compute_P(hp)
    try:
        begin('X2-ii');first=write_cell(H,hp,requests,P,targets['engine8'],pristine,'X2-ii first')
        second=write_cell(H,hp,requests,P,targets['engine8'],pristine,'X2-ii second')
        write_floor=max(relative64(x['tensor'],y['tensor']) for x,y in zip(first['updates'],second['updates']))
        require(write_floor<=1e-5,'X2_WRITE_FLOOR')
        checks['X2-ii']={'ok':True,'floor':write_floor,'arithmetic':'cpu_float64',
            'first':clean_capture(first['updates']),'second':clean_capture(second['updates']),
            'report_only_fp32':[parity(x['tensor'],y['tensor'],write_floor)['report_only_fp32'] for x,y in zip(first['updates'],second['updates'])],
            'canon_full_difference':sum(f[0] for f in second['flags'][::4])-sum(f[0] for f in first['flags'][::4]),
            'para_full_difference':sum(f[0] for i,f in enumerate(second['flags']) if i%4)-sum(f[0] for i,f in enumerate(first['flags']) if i%4)}
        begin('X1-iv');changed=write_cell(H,hp,requests,P,reduced,pristine,'X1-iv')
        checks['X1-iv']={'ok':True,'floor':write_floor,'layers':compare_updates(first['updates'],changed['updates'],write_floor)}
        del changed,second
        begin('X2-iii');identity={k:{l:targets['engine8'][k] for l in hp.layers} for k in targets['engine8']}
        same=write_cell(H,hp,requests,P,targets['engine8'],pristine,'X2-iii',identity,'identity')
        checks['X2-iii']={'ok':True,'floor':write_floor,'layers':compare_updates(first['updates'],same['updates'],write_floor),'rho_A':same['residual_diagnostics']}
        del first,same
        begin('X2-iv');replay_cells=[];replay_floor=0.;index_records=[]
        for arm in A.ARM_NAMES:
            rqs=[H.req(H.CANON,s,H.ARMS[arm][s]) for s in H.FICTION]
            pristine.verify('X2-iv '+arm)
            plain,meta=A.batch_replay(H,hp,rqs)
            for layer in hp.layers:
                a=cpu_copy(A.canonical_read(H,hp,layer,rqs));b=cpu_copy(A.canonical_read(H,hp,layer,rqs))
                f=relative_fixed(a,b);require(f<=1e-5,'REPLAY_FLOOR');replay_floor=max(replay_floor,f)
                replay_cells.append({'arm':arm,'layer':layer,**parity(a,plain[layer],f,double=False)})
            null,meta2=A.batch_replay(H,hp,rqs,plain[hp.layers[0]])
            require(meta==meta2,'REPLAY_INPUT_IDENTITY')
            for layer in hp.layers[1:]:replay_cells.append({'arm':arm,'layer':layer,**parity(plain[layer],null[layer],replay_floor,double=False)})
            for r,idx in zip(rqs,meta['indices']):
                other=H.subject_idx(r['prompt'],r['subject']);require(idx==other,'INDEX_MISMATCH')
                index_records.append({'request':[r['subject'],r['target_new']['str']],'solve_index':idx,'injection_index':other})
        checks['X2-iv']={'ok':True,'floor':replay_floor,'cells':replay_cells}
        begin('X2-v');checks['X2-v']={'ok':True,'indices':index_records}
        begin('X2-vi')
        hp1=copy.deepcopy(hp);hp1.layers=[8];P1=[P[hp.layers.index(8)]]
        with pristine.cell('X2-vi builder'):
            table,diags,_=A.fe_builder(H,hp1,requests,ctx)
        target_checks=[parity(targets['engine8'][(r['subject'],r['target_new']['str'])],table[(r['subject'],r['target_new']['str'])][8],floor,double=False) for r in requests]
        singleton=write_cell(H,hp1,requests,P1,targets['engine8'],pristine,'X2-vi original')
        active=write_cell(H,hp1,requests,P1,None,pristine,'X2-vi active',table,'fe')
        require(norm64(singleton['updates'][0]['tensor'])>0.,'SINGLETON_ZERO_REFERENCE')
        update_check=compare_updates(singleton['updates'],active['updates'],write_floor)
        cache_check=parity(singleton['cache'][0],active['cache'][0],write_floor,double=False)
        require(torch.equal(singleton['weights'][8],active['weights'][8]),'SINGLETON_APPLIED_WEIGHT')
        require(singleton['flags']==active['flags'],'SINGLETON_GREEDY_FLAGS')
        checks['X2-vi']={'ok':True,'targets':target_checks,'layers':update_check,'cache':cache_check,
                        'reference':clean_capture(singleton['updates']),'candidate':clean_capture(active['updates']),
                        'applied_weight_exact':True,'greedy_flags_exact':True,'flags_reference':singleton['flags'],'flags_candidate':active['flags']}
        del singleton,active
        begin('X2-vii')
        with pristine.cell('X2-vii null'):
            plain,meta=A.batch_replay(H,hp,requests);null,meta2=A.batch_replay(H,hp,requests,plain[hp.layers[0]])
            require(meta==meta2,'NULL_INPUT_IDENTITY')
            table={(r['subject'],r['target_new']['str']):{l:null[l][i].clone() for l in hp.layers} for i,r in enumerate(requests)}
            # Observe whole vectors independently outside fe_edit; the engine's
            # result is compared with the same-batch block-hook observer.
            observed={};namespace=A.fe_edit.__globals__;original=namespace['get_module_input_output_at_words']
            expected_order=[(r['subject'],r['target_new']['str']) for r in requests]
            def checked_read(model,tok,layer,context_templates,words,module_template,fact_token_strategy):
                require(context_templates==[r['prompt'] for r in requests] and words==[r['subject'] for r in requests],'NULL_REQUEST_ORDER')
                block_outputs,meta3=A.batch_replay(H,hp,requests)
                result=original(model,tok,layer,context_templates=context_templates,words=words,module_template=module_template,fact_token_strategy=fact_token_strategy)
                expected_layer=hp.layers[len(observed)]
                observed[expected_layer]=cpu_copy(result[1])
                stacked={l:torch.stack([table[k][l] for k in expected_order]) for l in hp.layers}
                active_null_structure({expected_layer:observed[expected_layer]},
                    {expected_layer:stacked[expected_layer]},{expected_layer:block_outputs[expected_layer]},expected_order,expected_order)
                return result
            old=A.FE_STATE,A.FE_TARGETS
            try:
                A.FE_STATE={'targets':table};A.FE_TARGETS=table;A._refresh_globals()
                namespace['get_module_input_output_at_words']=checked_read
                with observe_null_solve(A.fe_edit,observed,expected_order) as residuals:
                    with capture_updates(A.fe_edit,hp.layers,{'writer':'fe_edit','check':'X2-vii','recipe':'standalone','arm':'A7'}) as captures:
                        A.fe_edit(hp,requests,P,[torch.zeros_like(p) for p in P])
                require(all(torch.count_nonzero(c['tensor'])==0 for c in captures),'NULL_NONZERO_UPDATE')
                pristine.verify('X2-vii exact zero')
            finally:
                namespace['get_module_input_output_at_words']=original
                A.FE_STATE,A.FE_TARGETS=old
            checks['X2-vii']={'ok':True,'layers':clean_capture(captures),'requests':meta['requests'],'weight_identity':True,'residuals':residuals}
        begin('G8');started=A.work_unit(kind='G8');checks['G8']=direct_g8(H,hp,P,ctx,pristine);A.end_unit(started)
        if A.TELEMETRY:A.TELEMETRY.phase('check_end',check='G8')
    finally:
        del P
        H.Z_OVERRIDE=None;H.Z_OVERRIDE_HITS=0;A.FE_STATE=None;A.FE_TARGETS={};A.FE_CALLS=0;A._refresh_globals()
        pristine.restore();pristine.verify('after inertness')
    return checks
