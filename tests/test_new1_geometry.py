"""Small synthetic CPU arithmetic only; never opens pinned science operands."""
import importlib
from pathlib import Path
import tempfile
import unittest
from unittest import mock


class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(Path('tools/new1_geometry.py').is_file(), 'NEW1 computation worker is not built')
        self.G=importlib.import_module('tools.new1_geometry')
        import torch
        import numpy as np
        self.torch, self.np=torch,np
        torch.set_num_threads(1)

    def test_participation_ratio_and_rank95_use_squared_singular_energy(self):
        s=self.torch.tensor([4.,3.],dtype=self.torch.float64)
        self.assertAlmostEqual(self.G.effective_rank(s),625/337,12)
        self.assertEqual(self.G.rank95(s),2)
        self.assertAlmostEqual(self.G.effective_rank(self.torch.ones(16)),16)

    def test_zero_and_nonfinite_updates_are_invalid(self):
        for values in ([0.,0.],[1.,float('nan')]):
            with self.subTest(values=values), self.assertRaises(self.G.Invalid):
                self.G.effective_rank(self.torch.tensor(values))

    def test_adapter_qr_matches_direct_product_and_saved_scale(self):
        A=self.torch.tensor([[1.,0.,0.],[0.,2.,0.]],dtype=self.torch.float64)
        B=self.torch.tensor([[3.,0.],[0.,4.]],dtype=self.torch.float64)
        result=self.G.adapter_spectrum(A,B,2.)
        self.assertTrue(self.torch.allclose(result.s,self.torch.tensor([16.,6.],dtype=self.torch.float64)))
        dense=result.left @ self.torch.diag(result.s) @ result.right.T
        self.assertTrue(self.torch.allclose(dense,2*B@A))

    def test_covariance_energy_uses_input_axis_and_is_scale_sign_invariant(self):
        Q=self.torch.eye(3,dtype=self.torch.float64)
        Z=self.torch.tensor([[3.,4.,0.],[0.,0.,0.]],dtype=self.torch.float64)
        self.assertAlmostEqual(self.G.energy(Z,Q,[0]),9/25)
        self.assertAlmostEqual(self.G.energy(-2*Z,Q,[0]),9/25)
        with self.assertRaises(self.G.Invalid): self.G.energy(Z.T,Q,[0])

    def test_energy_promotes_only_selected_covariance_column_blocks(self):
        t=self.torch; Q=t.eye(513,dtype=t.float32); Z=t.ones((2,513),dtype=t.float64)
        promoted=[]; original=t.Tensor.double
        def promote(value,*args,**kwargs):
            if value.dtype!=t.float64: promoted.append(tuple(value.shape))
            return original(value,*args,**kwargs)
        with mock.patch.object(t.Tensor,'double',new=promote):
            fraction=self.G.energy(Z,Q,[0,512])
        self.assertAlmostEqual(fraction,2/513)
        self.assertEqual(promoted,[(513,2)],'full covariance basis must never be promoted')

    def test_subspace_rotation_and_rank_deficient_fixed_denominator(self):
        Q=self.torch.eye(5,dtype=self.torch.float64)[:,:2]
        rotated=Q@self.torch.tensor([[0.,1.],[-1.,0.]],dtype=self.torch.float64)
        overlap=self.G.overlap(Q,rotated)
        self.assertAlmostEqual(overlap['O16'],2/16)
        self.assertEqual(len(overlap['angles_deg']),2)
        self.assertTrue(all(x<1e-5 for x in overlap['angles_deg']))

    def test_covariance_checks_promote_before_fp32_scaling_underflows(self):
        t=self.torch
        # A valid rotated decomposition of a degenerate, subnormal fp32 PSD C.
        U=t.tensor([[1.,1.,1.,1.],[1.,-1.,1.,-1.],
                    [1.,1.,-1.,-1.],[1.,-1.,-1.,1.]],dtype=t.float32)/2
        s=t.full((4,),2.**-149,dtype=t.float32)
        Vh=U.T; C=t.diag(s)
        before=[value.numpy().tobytes() for value in (C,U,s,Vh)]
        native_P=U@U.T
        reference=C.double()
        legacy=(U*s)@Vh
        promoted=(U.double()*s.double())@Vh.double()
        legacy_error=float(t.linalg.vector_norm(reference-legacy.double())/t.linalg.vector_norm(reference))
        promoted_error=float(t.linalg.vector_norm(reference-promoted)/t.linalg.vector_norm(reference))
        self.assertGreater(legacy_error,1e-5)
        self.assertEqual(promoted_error,0.)
        with mock.patch.object(t.linalg,'svd',side_effect=[(U,s,Vh),(U.double(),s.double(),Vh.double())]) as svd:
            basis=self.G.covariance_basis(C,k=1)
        self.assertEqual(svd.call_count,2)
        self.assertIs(basis['native']['Q'],U)
        self.assertIs(basis['native']['s'],s)
        self.assertEqual(basis['Q'].dtype,t.float64)
        self.assertEqual(basis['s'].dtype,t.float64)
        self.assertEqual(basis['subsets'],{'top':[0],'bottom':[3],'excluded':[],'allowed':[0,1,2,3]})
        self.assertEqual([value.numpy().tobytes() for value in (C,U,s,Vh)],before)
        self.assertEqual(self.G.native_projector(basis).numpy().tobytes(),native_P.numpy().tobytes())
        self.assertTrue(all(error==0. for error in basis['checks'].values()))

    def test_covariance_check_products_use_float64_blocks_preserving_native_objects(self):
        t=self.torch
        C=t.diag(t.cat((t.linspace(.02,.005,200),t.linspace(.004,.001,57))))
        before_C=C.numpy().tobytes()
        real_svd=t.linalg.svd; real_double=t.Tensor.double
        real_mul=t.Tensor.__mul__; real_matmul=t.Tensor.__matmul__
        native={}; geometry={}; promoted=[]; products=[]; scales=[]
        def decompose(value,*args,**kwargs):
            U,s,Vh=real_svd(value,*args,**kwargs)
            target=native if value.dtype==t.float32 else geometry
            target.update(U=U,s=s,Vh=Vh,bytes=[v.numpy().tobytes() for v in (U,s,Vh)])
            if value.dtype==t.float32:
                idx=(s<.005).nonzero(as_tuple=True)[0]
                native['P']=real_matmul(U[:,idx],U[:,idx].T)
            return U,s,Vh
        def promote(value,*args,**kwargs):
            if value.dtype==t.float32 and value.ndim==2: promoted.append(tuple(value.shape))
            return real_double(value,*args,**kwargs)
        def scale(left,right):
            if isinstance(right,t.Tensor): scales.append((left.dtype,right.dtype))
            return real_mul(left,right)
        def product(left,right):
            products.append((left.dtype,right.dtype))
            return real_matmul(left,right)
        with mock.patch.object(t.linalg,'svd',side_effect=decompose) as svd, \
             mock.patch.object(t.Tensor,'double',new=promote), \
             mock.patch.object(t.Tensor,'__mul__',new=scale), \
             mock.patch.object(t.Tensor,'__matmul__',new=product):
            basis=self.G.covariance_basis(C,k=1)
        self.assertEqual(svd.call_count,2)
        self.assertIs(svd.call_args_list[0].args[0],C)
        self.assertTrue(t.equal(svd.call_args_list[1].args[0],C.double()))
        self.assertTrue(scales and all(pair==(t.float64,t.float64) for pair in scales))
        self.assertTrue(products and all(pair==(t.float64,t.float64) for pair in products))
        self.assertEqual(promoted.count((257,257)),1,'only normalized C is promoted whole for its SVD')
        self.assertTrue(all(shape==(257,257) or min(shape)<=256 for shape in promoted))
        self.assertIs(basis['Q'],geometry['U'])
        self.assertIs(basis['s'],geometry['s'])
        self.assertIs(basis['native']['Q'],native['U'])
        self.assertIs(basis['native']['s'],native['s'])
        self.assertEqual([v.numpy().tobytes() for v in (native['U'],native['s'],native['Vh'])],native['bytes'])
        self.assertEqual(C.numpy().tobytes(),before_C)
        expected={'top':[0],'bottom':[256],
            'excluded':(geometry['s']>=.005).nonzero(as_tuple=True)[0].tolist(),
            'allowed':(geometry['s']<.005).nonzero(as_tuple=True)[0].tolist()}
        self.assertEqual(basis['subsets'],expected)
        P=self.G.native_projector(basis)
        self.assertEqual(P.dtype,t.float32)
        self.assertEqual(P.numpy().tobytes(),native['P'].numpy().tobytes())

    def test_native_covariance_svd_once_and_indefinite_psd_rejection(self):
        C=self.torch.diag(self.torch.tensor([4.,2.,.004,.001]))
        real=self.torch.linalg.svd
        with mock.patch.object(self.torch.linalg,'svd',wraps=real) as spy:
            basis=self.G.covariance_basis(C,k=1)
        self.assertEqual([c.args[0].dtype for c in spy.call_args_list],[self.torch.float32,self.torch.float64])
        self.assertEqual(basis['Q'].dtype,self.torch.float64)
        self.assertEqual(basis['dimensions']['excluded'],2)
        self.assertEqual(basis['dimensions']['allowed'],2)
        with self.assertRaises(self.G.Invalid):
            self.G.covariance_basis(self.torch.diag(self.torch.tensor([4.,2.,-.004,.001])),k=1)

    def test_covariance_top_bottom_ties_are_statistic_specific(self):
        C=self.torch.diag(self.torch.tensor([4.,2.,2.,.001]))
        b=self.G.covariance_basis(C,k=2)
        self.assertFalse(b['valid']['top'])
        self.assertFalse(b['valid']['bottom'])
        self.assertTrue(b['valid']['excluded'])
        self.assertTrue(b['valid']['allowed'])

    def test_update_cutoff_tie_invalidates_m16_but_not_full_effective_rank(self):
        spec=self.G.spectrum(self.torch.diag(self.torch.ones(20,dtype=self.torch.float64)))
        retained,valid=self.G.leading(spec)
        self.assertFalse(valid)
        self.assertEqual(len(retained.s),16)
        self.assertAlmostEqual(self.G.effective_rank(spec.s),20)

    def test_m16_retained_energy_is_secondary_and_uses_existing_svd(self):
        s=self.torch.arange(20.,0.,-1,dtype=self.torch.float64)
        spec=self.G.spectrum(self.torch.diag(s))
        result=self.G.m16_diagnostic(spec,self.torch.eye(20),{'top':[0,1],'bottom':[18,19],
            'excluded':list(range(10)), 'allowed':list(range(10,20))})
        self.assertEqual(result['role'],'secondary')
        self.assertAlmostEqual(result['retained_energy'],2840/2870)
        self.assertEqual(result['energy']['bottom'],0)

    def test_spectrum_matched_random_preserves_spectrum_and_norm(self):
        ds=self.torch.arange(16.,0.,-1,dtype=self.torch.float64)
        flat,matched=self.G.random_control(24,32,ds,4,0)
        self.assertAlmostEqual(self.G.effective_rank(flat.s),16)
        self.assertTrue(self.torch.equal(matched.s,ds))
        self.assertAlmostEqual(float(flat.s.square().sum()),1496)
        self.assertAlmostEqual(float(matched.s.square().sum()),1496)
        flat2,matched2=self.G.random_control(24,32,ds,4,0)
        self.assertTrue(self.torch.equal(flat.right,flat2.right))
        self.assertTrue(self.torch.equal(matched.right,matched2.right))

    def test_native_projector_uses_two_independent_native_gathers(self):
        t=self.torch
        U=t.tensor([[.5,.5,.5,.5],[.5,-.5,.5,-.5],
                    [.5,.5,-.5,-.5],[.5,-.5,-.5,.5]],dtype=t.float32)
        allowed=[3,1]; before_U=U.numpy().tobytes(); before_allowed=list(allowed)
        gathers=[]; products=[]
        real_getitem=t.Tensor.__getitem__; real_matmul=t.Tensor.__matmul__
        def gather(value,key):
            result=real_getitem(value,key)
            gathers.append((value,key,result))
            return result
        def product(left,right):
            products.append((left,right))
            return real_matmul(left,right)
        with mock.patch.object(t.Tensor,'__getitem__',new=gather), \
             mock.patch.object(t.Tensor,'__matmul__',new=product):
            P=self.G.native_projector({'native':{'Q':U,'allowed':allowed}})
        self.assertEqual(len(gathers),2,'native projector must gather twice from native U')
        self.assertEqual(len(products),1)
        for value,key,result in gathers:
            self.assertIs(value,U)
            self.assertEqual(key[0],slice(None))
            self.assertIs(key[1],allowed)
            self.assertEqual(result.dtype,t.float32)
            self.assertTrue(t.equal(result,U[:,allowed]))
        left,right=products[0]
        self.assertIs(left,gathers[0][2])
        self.assertNotEqual(left.untyped_storage().data_ptr(),right.untyped_storage().data_ptr(),
                            'projector operands must have independent storage')
        self.assertEqual(right.untyped_storage().data_ptr(),gathers[1][2].untyped_storage().data_ptr())
        self.assertEqual((left.dtype,right.dtype),(t.float32,t.float32))
        self.assertTrue(t.equal(right,left.T))
        self.assertEqual(U.dtype,t.float32)
        self.assertEqual(U.numpy().tobytes(),before_U)
        self.assertEqual(allowed,before_allowed)
        reference=U[:,allowed]@U[:,allowed].T
        self.assertEqual(P.dtype,t.float32)
        self.assertEqual(P.numpy().tobytes(),reference.numpy().tobytes())
        self.assertTrue(self.G.projector_matches(P,len(allowed),len(allowed),
                                               self.G.tensor_sha(reference),[]))

    def test_projector_matches_all_four_frozen_probes_and_update_parity(self):
        P=self.torch.diag(self.torch.tensor([0.,0.,1.,1.]))
        probes=[P@self.torch.randn(4,generator=self.torch.Generator().manual_seed(j)) for j in range(4)]
        self.assertTrue(self.G.projector_matches(P,2,2,'unmatched-hash',probes))
        probes[3]=probes[3]+1
        self.assertFalse(self.G.projector_matches(P,2,2,'unmatched-hash',probes))

    def test_covariance_load_normalizes_in_native_dtype_and_count_must_be_positive(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'cache.npz'
            self.np.savez(p,**{'mom2.mom2':self.np.eye(4,dtype=self.np.float32)*2,'mom2.count':self.np.int64(2)})
            self.assertTrue(self.torch.equal(self.G.load_covariance(p),self.torch.eye(4)))
            self.np.savez(p,**{'mom2.mom2':self.np.eye(4,dtype=self.np.float32),'mom2.count':self.np.int64(0)})
            with self.assertRaises(self.G.Invalid): self.G.load_covariance(p)

    def rows(self):
        rows=[{'layer':l,'valid':True,'top_valid':True,'overlap_valid':True,
                 'D':{'energy':{'excluded':.6,'top':.3},'r_eff':12,'input_overlap':.15},
                 'M':{'energy':{'excluded':0.,'top':0.},'r_eff':8},
                 'random':{'excluded_q95':.2,'top_q95':.1,'input_overlap_q95':.01},
                 'shuf_excluded':.1} for l in [4,5,6,7,8]]
        for row in rows:
            row['basis']={'native_excluded_count':2,'float64_excluded_count':2,'cutoffs':[2]}
            row['cutoffs']={'2':{'D':row['D']['energy'],'M':row['M']['energy'],'random':row['random']}}
        return rows

    def test_predictions_require_same_three_layers_and_random_guard(self):
        rows=self.rows()
        self.assertEqual(self.G.predictions(rows),{'H-COV':'PASS','H-TOP':'PASS','H-RANK':'PASS','H-OVERLAP':'PASS'})
        for row in rows[:3]: row['random']['excluded_q95']=.55
        self.assertEqual(self.G.predictions(rows)['H-COV'],'BOUNDARY-SENSITIVE')

    def test_no_favorable_layer_drop_and_tie_invalidates_only_related_endpoint(self):
        rows=self.rows(); rows[0]['top_valid']=False
        outcomes=self.G.predictions(rows)
        self.assertEqual(outcomes['H-TOP'],'INVALID')
        self.assertEqual(outcomes['H-COV'],'PASS')
        rows=self.rows(); rows.pop()
        self.assertEqual(set(self.G.predictions(rows).values()),{'INVALID'})

    def test_secondary_controls_cannot_replace_primary_q95(self):
        rows=self.rows()
        for row in rows:
            row['D']['energy']['excluded']=.25
            row['random']['excluded_q95']=.2
            row['secondary_random']={'excluded_q95':0.}
            row['M16']={'energy':{'excluded':0.}}
        self.assertEqual(self.G.predictions(rows)['H-COV'],'BOUNDARY-SENSITIVE')

    def test_q95_is_nineteenth_of_twenty_not_interpolation(self):
        self.assertEqual(self.G.q95(list(range(20))),18)
        with self.assertRaises(self.G.Invalid): self.G.q95(list(range(19)))

    def test_source_hash_and_harvest_identity_mismatch_are_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'manifest.json'; p.write_text('{}')
            with self.assertRaises(self.G.Invalid): self.G.verify_file(p,'0'*64)
        manifest={'prereg_sha256':'wrong','source_start':{},'source_end':{},'files':{}}
        with self.assertRaises(self.G.Invalid): self.G.verify_manifest(manifest,{'fiction':[]})

    def test_source_mutation_during_consumption_is_invalid(self):
        import hashlib
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'operand'; p.write_bytes(b'frozen')
            digest=hashlib.sha256(b'frozen').hexdigest()
            with self.assertRaises(self.G.Invalid):
                with self.G.bound_input(p,digest): p.write_bytes(b'changed')

    def test_all_conditions_must_hold_in_same_layers(self):
        rows=self.rows()
        # Each of two requirements passes in three layers, but their conjunction in two.
        for i,row in enumerate(rows):
            row['D']['energy']['excluded']=.6 if i<3 else .24
            row['random']['excluded_q95']=.55 if i==0 else .1
        self.assertEqual(self.G.predictions(rows)['H-COV'],'BOUNDARY-SENSITIVE')

    def test_projector_and_cache_tensor_metadata_cannot_be_missing(self):
        with self.assertRaises(self.G.Invalid):
            self.G.validate_capture({},4,self.torch.eye(4),2)

    def test_complete_small_layer_reuses_basis_and_persists_all_secondary_controls(self):
        t=self.torch
        C=t.diag(t.cat((t.linspace(.02,.01,32),t.linspace(.004,.0001,32))))
        basis=self.G.covariance_basis(C,k=16)
        A=t.zeros((16,64),dtype=t.float64); A[:,:16]=t.eye(16,dtype=t.float64)
        B=t.zeros((24,16),dtype=t.float64); B[:16,:]=t.diag(t.arange(16.,0.,-1,dtype=t.float64))
        M=t.zeros((24,64),dtype=t.float64); M[:,32:56]=t.diag(t.arange(24.,0.,-1,dtype=t.float64))
        adapters={arm:(A,B,1.) for arm in ['A7_coined_coined','A1_single','A2_coherent2','A7_canon','A7_shuf']}
        phases=[]
        with tempfile.TemporaryDirectory() as tmp:
            row=self.G.analyse_layer_with_basis(basis,adapters,M,4,phases.append,Path(tmp)/'controls')
            self.assertEqual(len(list((Path(tmp)/'controls').glob('*.npz'))),20)
        self.assertAlmostEqual(row['D']['energy']['excluded'],1.)
        self.assertAlmostEqual(row['M']['energy']['excluded'],0.)
        contrast=row['D']['energy_minus_M']
        self.assertAlmostEqual(contrast['top']['difference'],1.)
        self.assertAlmostEqual(contrast['bottom']['difference'],-204/4900)
        self.assertTrue(contrast['top']['valid'])
        self.assertTrue(contrast['bottom']['valid'])
        for arm in row['arms'].values():
            self.assertEqual(arm['energy_minus_M'],contrast)
        self.assertEqual(row['M16']['role'],'secondary')
        self.assertEqual(row['secondary_random']['role'],'secondary')
        self.assertEqual(len(row['random']['draws']),20)
        self.assertNotIn('covariance-svd',phases)

    def test_layer_energy_contrasts_keep_each_bin_validity_flag(self):
        t=self.torch
        C=t.diag(t.cat((t.linspace(.02,.01,32),t.linspace(.004,.0001,32))))
        basis=self.G.covariance_basis(C,k=16)
        basis['valid']['top']=False; basis['valid']['bottom']=True
        A=t.zeros((16,64),dtype=t.float64); A[:,:16]=t.eye(16,dtype=t.float64)
        B=t.zeros((24,16),dtype=t.float64); B[:16,:]=t.diag(t.arange(16.,0.,-1,dtype=t.float64))
        M=t.zeros((24,64),dtype=t.float64); M[:,32:56]=t.diag(t.arange(24.,0.,-1,dtype=t.float64))
        adapters={arm:(A,B,1.) for arm in self.G.ARMS}
        with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
            row=self.G.analyse_layer_with_basis(basis,adapters,M,4,lambda phase:None,Path(tmp)/'controls')
            path=Path(tmp)/'layer.json'; self.G.durable_json(path,{'tier':'MATH-PROXY',**row})
            contrast=self.G.strict_json(path.read_text())['D']['energy_minus_M']
        self.assertFalse(contrast['top']['valid'])
        self.assertTrue(contrast['bottom']['valid'])
        self.assertAlmostEqual(contrast['top']['difference'],1.)
        self.assertAlmostEqual(contrast['bottom']['difference'],-204/4900)

    def test_actual_producer_gate_dictionary_is_admitted_and_failed_gate_refuses(self):
        subjects=[f's{i}' for i in range(24)]
        manifest={'prereg_sha256':'4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507',
            'source_start':{'source':'same'},'source_end':{'source':'same'},
            'files':{'inloop_A7_coined_coined.pt':{'sha256':'abb882982f406ddd5d6536529ce49dee8f31ad3b3243495e93687266e7c6582f'}},
            'gates':{k:{'passed':True,'observed':{'ok':True},'bar':'required'} for k in ('context','law3','law5','observer-parity')},
            'prompts':[{'kind':'CANON','subject':s} for s in subjects]}
        self.G.verify_manifest(manifest,{'fiction':subjects})
        manifest['gates']['law5']['passed']=False
        with self.assertRaises(self.G.Invalid): self.G.verify_manifest(manifest,{'fiction':subjects})

    def test_all_update_families_enforce_complement_and_random_descriptive_norms(self):
        with self.assertRaises(self.G.Invalid): self.G.validate_fractions({'excluded':.6,'allowed':.6})
        flat,matched=self.G.random_control(24,32,self.torch.arange(16.,0.,-1),4,0)
        record=self.G.summarize_draws([{'energy':{'top':.25,'bottom':.2,'excluded':.6,'allowed':.4},
            'norm':float(flat.s.norm()),'r_eff':16,'input_subspace':{'O16':.1},'output_subspace':{'O16':.2}} for _ in range(20)])
        self.assertAlmostEqual(record['q95_energy']['bottom'],.2)
        self.assertAlmostEqual(record['mean_norm'],1496**.5)

    def test_every_integer_cutoff_uses_float64_ordering_and_reports_band_energy(self):
        t=self.torch; real=t.linalg.svd
        C=t.diag(t.tensor([.02,.009,.006,.004],dtype=t.float32))
        before=C.numpy().tobytes(); phases=[]
        def svd(value,**kwargs):
            U,s,Vh=real(value,**kwargs)
            if value.dtype==t.float32: s[1:3]=t.tensor([.0049,.0048])
            return U,s,Vh
        with mock.patch.object(t.linalg,'svd',side_effect=svd):
            basis=self.G.covariance_basis(C,k=1,cell=phases.append)
        self.assertIn('cutoffs',basis,'inclusive covariance cutoff band is missing')
        self.assertEqual(basis['cutoffs'],[1,2,3])
        self.assertEqual((basis['native_excluded_count'],basis['float64_excluded_count']),(1,3))
        self.assertEqual(basis['band_indices'],[1,2])
        self.assertEqual(phases,['covariance-svd','covariance-svd-f64','covariance-checks'])
        self.assertEqual(C.numpy().tobytes(),before)
        result=self.G.geometry_energies(t.tensor([[1.,2.,3.,4.]],dtype=t.float64),basis)
        self.assertAlmostEqual(result['band_energy'],13/30)
        for cutoff,want in ((1,1/30),(2,5/30),(3,14/30)):
            with self.subTest(cutoff=cutoff):
                self.assertAlmostEqual(result['energy_by_cutoff'][str(cutoff)]['excluded'],want)
                self.assertAlmostEqual(result['energy_by_cutoff'][str(cutoff)]['allowed'],1-want)

    def test_reverse_equal_and_endpoint_count_bands_are_not_special_cased(self):
        t=self.torch; real=t.linalg.svd
        for native_count in (0,2,4):
            with self.subTest(native_count=native_count):
                C=t.diag(t.tensor([.02,.009,.004,.001],dtype=t.float32))
                def svd(value,**kwargs):
                    U,s,Vh=real(value,**kwargs)
                    if value.dtype==t.float32:
                        s[:native_count]=.01; s[native_count:]=.001
                    return U,s,Vh
                with mock.patch.object(t.linalg,'svd',side_effect=svd): basis=self.G.covariance_basis(C,k=1)
                self.assertIn('cutoffs',basis)
                self.assertEqual(basis['cutoffs'],list(range(min(native_count,2),max(native_count,2)+1)))
                result=self.G.geometry_energies(t.ones((1,4),dtype=t.float64),basis)
                self.assertAlmostEqual(result['band_energy'],abs(native_count-2)/4)
                for cutoff in basis['cutoffs']:
                    self.assertAlmostEqual(result['energy_by_cutoff'][str(cutoff)]['excluded'],cutoff/4)

    def boundary_rows(self, first, second):
        rows=self.rows()
        for row in rows:
            row['basis']={'native_excluded_count':2,'float64_excluded_count':3,'cutoffs':[2,3]}
            row['cutoffs']={str(c):{'D':{'excluded':.6 if row['layer'] in passing else .24},
                'M':{'excluded':0.},'random':{'excluded_q95':.2}} for c,passing in ((2,first),(3,second))}
        return rows

    def test_cutoff_passes_cannot_union_different_three_layer_sets(self):
        rows=self.boundary_rows({4,5,6},{5,6,7})
        self.assertEqual(self.G.predictions(rows)['H-COV'],'BOUNDARY-SENSITIVE')
        self.assertEqual(self.G.predictions(rows)['H-TOP'],'PASS')

    def test_robust_pass_keeps_the_same_three_layers_at_every_cutoff(self):
        rows=self.boundary_rows({4,5,6,7},{4,5,6,8})
        self.assertEqual(self.G.predictions(rows)['H-COV'],'PASS')
        rows[0]['cutoffs']['3']['random']['excluded_q95']=.55
        self.assertEqual(self.G.predictions(rows)['H-COV'],'BOUNDARY-SENSITIVE')

    def test_nonrobust_aggregate_is_boundary_sensitive_with_nominal_failures(self):
        self.assertEqual(self.G.predictions(self.boundary_rows(set(),set()))['H-COV'],'BOUNDARY-SENSITIVE')

    def test_missing_intermediate_cutoff_is_invalid_not_favorable_subset(self):
        rows=self.boundary_rows({4,5,6,7,8},{4,5,6,7,8})
        rows[0]['basis'].update(float64_excluded_count=4,cutoffs=[2,3,4])
        rows[0]['cutoffs']['4']=rows[0]['cutoffs'].pop('3')
        self.assertEqual(self.G.predictions(rows)['H-COV'],'INVALID')

    def test_native_parity_is_retained_when_float64_excluded_energy_is_large(self):
        t=self.torch; real=t.linalg.svd
        C=t.diag(t.cat((t.linspace(.02,.01,32),t.tensor([.0051]),t.linspace(.004,.0001,31))))
        def svd(value,**kwargs):
            U,s,Vh=real(value,**kwargs)
            if value.dtype==t.float32: s[32]=.0049
            return U,s,Vh
        with mock.patch.object(t.linalg,'svd',side_effect=svd): basis=self.G.covariance_basis(C,k=16)
        self.assertIn('native',basis,'native projector basis must be retained separately')
        P=self.G.native_projector(basis)
        self.assertEqual(P.dtype,t.float32)
        self.assertTrue(t.equal(P,t.diag(t.cat((t.zeros(32),t.ones(32))))))
        self.assertTrue(self.G.projector_matches(P,32,32,self.G.tensor_sha(P),[]))
        self.assertFalse(self.G.projector_matches(P,32,31,self.G.tensor_sha(P),[]))
        A=t.zeros((16,64),dtype=t.float64); A[:,:16]=t.eye(16,dtype=t.float64)
        B=t.zeros((24,16),dtype=t.float64); B[:16,:]=t.diag(t.arange(16.,0.,-1,dtype=t.float64))
        M=t.zeros((24,64),dtype=t.float64); M[:,32:56]=t.diag(t.arange(24.,0.,-1,dtype=t.float64))
        adapters={arm:(A,B,1.) for arm in self.G.ARMS}
        with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
            row=self.G.analyse_layer_with_basis(basis,adapters,M,4,lambda phase:None,Path(tmp)/'controls')
            persisted=Path(tmp)/'layer.json'; self.G.durable_json(persisted,row)
            row=self.G.strict_json(persisted.read_text())
        self.assertEqual(row['native_parity']['excluded_energy'],0.)
        self.assertAlmostEqual(row['M']['energy']['excluded'],576/4900)
        self.assertAlmostEqual(row['M']['band_energy'],576/4900)
        self.assertEqual(row['basis']['cutoffs'],[32,33])
        self.assertEqual(set(row['cutoffs']),{'32','33'})
        records=[row['M'],row['M16'],*row['arms'].values(),*row['random']['draws'],*row['secondary_random']['draws']]
        self.assertEqual(len(records),47)
        for record in records:
            self.assertIn('band_energy',record)
            self.assertEqual(set(record['energy_by_cutoff']),{'32','33'})
            for fractions in record['energy_by_cutoff'].values():
                self.assertAlmostEqual(fractions['excluded']+fractions['allowed'],1.,places=10)
        bad=M.clone(); bad[:,0]=1
        with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp, self.assertRaisesRegex(self.G.Invalid,'native.*parity'):
            self.G.analyse_layer_with_basis(basis,adapters,bad,4,lambda phase:None,Path(tmp)/'controls')


if __name__=='__main__': unittest.main()
