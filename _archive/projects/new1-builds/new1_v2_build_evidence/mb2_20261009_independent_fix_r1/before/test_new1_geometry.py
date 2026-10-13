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

    def test_subspace_rotation_and_rank_deficient_fixed_denominator(self):
        Q=self.torch.eye(5,dtype=self.torch.float64)[:,:2]
        rotated=Q@self.torch.tensor([[0.,1.],[-1.,0.]],dtype=self.torch.float64)
        overlap=self.G.overlap(Q,rotated)
        self.assertAlmostEqual(overlap['O16'],2/16)
        self.assertEqual(len(overlap['angles_deg']),2)
        self.assertTrue(all(x<1e-5 for x in overlap['angles_deg']))

    def test_native_covariance_svd_once_and_indefinite_psd_rejection(self):
        C=self.torch.diag(self.torch.tensor([4.,2.,.004,.001]))
        real=self.torch.linalg.svd
        with mock.patch.object(self.torch.linalg,'svd',wraps=real) as spy:
            basis=self.G.covariance_basis(C,k=1)
        self.assertEqual(spy.call_count,1)
        self.assertEqual(basis['Q'].dtype,self.torch.float32)
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
        return [{'layer':l,'valid':True,'top_valid':True,'overlap_valid':True,
                 'D':{'energy':{'excluded':.6,'top':.3},'r_eff':12,'input_overlap':.15},
                 'M':{'energy':{'excluded':0.,'top':0.},'r_eff':8},
                 'random':{'excluded_q95':.2,'top_q95':.1,'input_overlap_q95':.01},
                 'shuf_excluded':.1} for l in [4,5,6,7,8]]

    def test_predictions_require_same_three_layers_and_random_guard(self):
        rows=self.rows()
        self.assertEqual(self.G.predictions(rows),{'H-COV':'PASS','H-TOP':'PASS','H-RANK':'PASS','H-OVERLAP':'PASS'})
        for row in rows[:3]: row['random']['excluded_q95']=.55
        self.assertEqual(self.G.predictions(rows)['H-COV'],'FAIL')

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
        self.assertEqual(self.G.predictions(rows)['H-COV'],'FAIL')

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
        self.assertEqual(self.G.predictions(rows)['H-COV'],'FAIL')

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
        self.assertEqual(row['M16']['role'],'secondary')
        self.assertEqual(row['secondary_random']['role'],'secondary')
        self.assertEqual(len(row['random']['draws']),20)
        self.assertNotIn('covariance-svd',phases)

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


if __name__=='__main__': unittest.main()
